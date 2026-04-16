#!/usr/bin/env python3
"""
aura_clone.py — CLI wrapper unificado do pipeline design-clone.

Orquestra downloader → analyzer → pattern-extractor em sequência, com
estrutura de output consistente, validação de URL/path, e error recovery.

Uso:
    python3 aura_clone.py <url> --output=<dir> [--product=<slug>]
                              [--skip-images] [--pattern-only]

Output:
    <dir>/
        raw/           (HTML, CSS, imagens, computed-styles.json)
        analysis.json  (output do analyzer)
        patterns.json  (output do pattern-extractor)
        manifest.json  (URL, timestamp, versão do wrapper)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# Garante import local de downloader.validate_*
_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from downloader import validate_url, validate_output_path  # noqa: E402

WRAPPER_VERSION = "1.0.0"

logger = logging.getLogger("design_clone.aura_clone")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


def _run_step(label: str, cmd: list[str]) -> int:
    """Executa subprocess com log, retorna return code."""
    print(f"\n[aura_clone] ===== {label} =====")
    print(f"[aura_clone] $ {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError as exc:
        logger.error("binário não encontrado em %s: %s", label, exc)
        return 127
    except OSError as exc:
        logger.error("falha ao executar %s: %s", label, exc)
        return 1


def _manifest(url: str, output_dir: Path, product: Optional[str], steps: dict) -> dict:
    return {
        "url": url,
        "output_dir": str(output_dir),
        "product_slug": product,
        "wrapper_version": WRAPPER_VERSION,
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "steps": steps,
    }


def _move_analyzer_output(raw_dir: Path, analysis_path: Path) -> bool:
    """sections.json (saída do analyzer) → analysis.json no root."""
    src = raw_dir / "sections.json"
    if not src.exists():
        return False
    try:
        analysis_path.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return True
    except OSError as exc:
        logger.warning("falha ao copiar sections.json: %s", exc)
        return False


def _move_pattern_output(raw_dir: Path, patterns_path: Path) -> bool:
    """patterns.json (saída do pattern-extractor) → patterns.json no root."""
    src = raw_dir / "patterns.json"
    if not src.exists():
        return False
    try:
        patterns_path.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return True
    except OSError as exc:
        logger.warning("falha ao copiar patterns.json: %s", exc)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aura Engine design-clone pipeline wrapper."
    )
    parser.add_argument("url", help="URL do site a clonar")
    parser.add_argument("--output", required=True, help="Diretório de saída")
    parser.add_argument("--product", default=None, help="Slug do produto (opcional)")
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Não baixa imagens (mais rápido, só pra extrair design signals)",
    )
    parser.add_argument(
        "--pattern-only",
        action="store_true",
        help="Após download, rodar apenas pattern-extractor (pula analyzer)",
    )
    args = parser.parse_args()

    # Validação
    try:
        url = validate_url(args.url)
    except ValueError as exc:
        print(f"ERRO: URL inválida: {exc}", file=sys.stderr)
        return 1
    try:
        output_dir = validate_output_path(args.output)
    except ValueError as exc:
        print(f"ERRO: --output inválido: {exc}", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    analysis_path = output_dir / "analysis.json"
    patterns_path = output_dir / "patterns.json"
    manifest_path = output_dir / "manifest.json"

    python_exe = sys.executable or "python3"
    steps_status: dict = {}

    # Passo 1: downloader
    env = os.environ.copy()
    if args.skip_images:
        env["AURA_SKIP_IMAGES"] = "1"
    downloader_cmd = [python_exe, str(_THIS_DIR / "downloader.py"), url, str(raw_dir)]
    rc = _run_step("downloader", downloader_cmd)
    steps_status["downloader"] = {"returncode": rc, "ok": rc == 0}
    if rc != 0:
        print("[aura_clone] downloader falhou — abortando pipeline.", file=sys.stderr)
        manifest_path.write_text(
            json.dumps(_manifest(url, output_dir, args.product, steps_status), indent=2),
            encoding="utf-8",
        )
        return rc

    # Passo 2: analyzer (opcional se --pattern-only)
    analyzer_ok = False
    if not args.pattern_only:
        analyzer_cmd = [python_exe, str(_THIS_DIR / "analyzer.py"), str(raw_dir)]
        rc = _run_step("analyzer", analyzer_cmd)
        steps_status["analyzer"] = {"returncode": rc, "ok": rc == 0}
        if rc == 0:
            analyzer_ok = _move_analyzer_output(raw_dir, analysis_path)
        else:
            logger.warning(
                "analyzer falhou (rc=%s) — continuando com pattern-extractor mesmo assim", rc
            )
    else:
        # Em pattern-only, ainda precisamos rodar o analyzer pra gerar sections.json
        # que o pattern-extractor consome. Mas não falhamos se der erro.
        analyzer_cmd = [python_exe, str(_THIS_DIR / "analyzer.py"), str(raw_dir)]
        rc = _run_step("analyzer (pré-requisito)", analyzer_cmd)
        steps_status["analyzer"] = {"returncode": rc, "ok": rc == 0, "mode": "prerequisite"}
        if rc == 0:
            analyzer_ok = _move_analyzer_output(raw_dir, analysis_path)

    # Passo 3: pattern-extractor
    if not (raw_dir / "sections.json").exists():
        logger.warning(
            "sections.json ausente — pattern-extractor pode falhar. Tentando mesmo assim."
        )
    pattern_cmd = [python_exe, str(_THIS_DIR / "pattern-extractor.py"), str(raw_dir)]
    rc = _run_step("pattern-extractor", pattern_cmd)
    steps_status["pattern_extractor"] = {"returncode": rc, "ok": rc == 0}
    pattern_ok = False
    if rc == 0:
        pattern_ok = _move_pattern_output(raw_dir, patterns_path)
    else:
        logger.warning("pattern-extractor falhou (rc=%s)", rc)

    # Manifest final
    manifest_path.write_text(
        json.dumps(_manifest(url, output_dir, args.product, steps_status), indent=2),
        encoding="utf-8",
    )

    print("\n[aura_clone] ===== SUMMARY =====")
    print(f"[aura_clone] url:          {url}")
    print(f"[aura_clone] output_dir:   {output_dir}")
    print(f"[aura_clone] raw/:         {raw_dir}")
    print(f"[aura_clone] analysis:     {'OK' if analyzer_ok else 'MISSING'}")
    print(f"[aura_clone] patterns:     {'OK' if pattern_ok else 'MISSING'}")
    print(f"[aura_clone] manifest:     {manifest_path}")

    # Return 0 se pelo menos downloader + pattern passaram
    if steps_status["downloader"]["ok"] and steps_status.get("pattern_extractor", {}).get("ok"):
        return 0
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[aura_clone] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("falha inesperada: %s", exc)
        sys.exit(1)
