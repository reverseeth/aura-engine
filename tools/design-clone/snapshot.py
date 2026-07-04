#!/usr/bin/env python3
"""
snapshot.py — Aura Engine design-clone: snapshot fiel de página via SingleFile.

Wrapper subprocess do `single-file-cli` (gildas-lormeau) — licença AGPL, por
isso é invocado SEMPRE como processo externo via npx/binário, NUNCA vendorizado
neste repo. Reusa o Chromium que o Playwright da Aura já instala (zero download
extra de browser).

Aceita DOIS tipos de input:

  1. URL  — captura a página com single-file-cli (self-contained: CSS inline,
     fontes e imagens como data URI, lazy-load disparado antes da captura).
  2. PATH LOCAL — ingere um .html já salvo (ex: pela EXTENSÃO SingleFile no
     Chrome real do membro — a válvula de escape pra Cloudflare/login). Nesse
     caso não precisa de browser nem de npm: só copia e pós-processa.

Gera SEMPRE 2 arquivos no output dir:

  ref.full.html  — verdade visual imutável. A IA NUNCA lê este arquivo cru
                   (14MB+, linhas de ~1M chars = contexto estourado/linhas
                   truncadas). Usos: membro abre no browser; render file://
                   pra screenshot na rota visão.
  ref.ai.html    — versão AI-readable: data-URIs base64 e SVGs url-encoded
                   viram placeholders `data:image/STRIPPED`, linhas longas
                   re-quebradas. MESMO ASSIM a leitura é sempre segmentada
                   (grep por marcos + Read offset/limit) ou programática
                   (analyzer/pattern-extractor) — nunca sequencial.

Uso:
    python3 snapshot.py <url-ou-path-local> --output <dir> [--json]

Exit codes:
    0  ok (ref.full.html + ref.ai.html gerados)
    1  input/output inválido
    2  captura/pós-processamento falhou
    3  Chromium do Playwright não encontrado (rode: playwright install chromium)
    6  single-file-cli indisponível (sem npx/node) — imprime o setup e sai

Setup (uma vez, opcional — só pra captura de URL; ingestão local não precisa):
    Node.js >= 20 (https://nodejs.org) — o single-file-cli baixa on-demand
    via `npx -y -p single-file-cli`. Instalação global opcional:
    npm install -g single-file-cli
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

# Import leve: downloader.py não exige Playwright na import (lazy).
from downloader import USER_AGENT, validate_output_path, validate_url  # noqa: E402

logger = logging.getLogger("design_clone.snapshot")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)

CAPTURE_TIMEOUT_SECONDS = 240
BROWSER_LOAD_MAX_TIME_MS = 60000

EXIT_OK = 0
EXIT_INVALID_INPUT = 1
EXIT_CAPTURE_FAILED = 2
EXIT_NO_CHROMIUM = 3
EXIT_NO_SINGLEFILE = 6

SETUP_INSTRUCTIONS = """\
[snapshot] single-file-cli indisponível: nem `single-file` nem `npx` encontrados no PATH.
[snapshot] Setup (uma vez):
[snapshot]   1. Instale Node.js >= 20: https://nodejs.org (ou `brew install node`)
[snapshot]   2. (opcional) npm install -g single-file-cli
[snapshot] Com o Node instalado, este wrapper usa `npx -y -p single-file-cli` automaticamente.
[snapshot] Alternativa SEM Node: membro salva a página com a extensão SingleFile no Chrome
[snapshot] (https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle)
[snapshot] e ingere o .html salvo: python3 snapshot.py <path-do-arquivo> --output <dir>"""


# --------------------------- Chromium discovery ------------------------------ #


def _playwright_cache_dirs() -> list[Path]:
    home = Path.home()
    return [
        home / "Library" / "Caches" / "ms-playwright",  # macOS
        home / ".cache" / "ms-playwright",  # Linux
        Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright",  # Windows
    ]


_CHROMIUM_RELPATHS = [
    "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "chrome-mac/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "chrome-mac-arm64/Chromium.app/Contents/MacOS/Chromium",
    "chrome-mac/Chromium.app/Contents/MacOS/Chromium",
    "chrome-linux/chrome",
    "chrome-win/chrome.exe",
]


def find_chromium() -> Optional[str]:
    """Descobre o executável do Chromium do Playwright.

    Cascade: env AURA_CHROMIUM → API do Playwright (se importável) → glob no
    cache do ms-playwright (versão mais alta primeiro).
    """
    env_path = os.environ.get("AURA_CHROMIUM")
    if env_path and Path(env_path).exists():
        return env_path

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            exe = p.chromium.executable_path
            if exe and Path(exe).exists():
                return str(exe)
    except Exception:  # noqa: BLE001 — playwright ausente/quebrado: cai pro glob
        pass

    def _version_key(d: Path) -> int:
        digits = re.sub(r"\D", "", d.name)
        return int(digits) if digits else 0

    for base in _playwright_cache_dirs():
        if not base.is_dir():
            continue
        for d in sorted(base.glob("chromium-*"), key=_version_key, reverse=True):
            for rel in _CHROMIUM_RELPATHS:
                cand = d / rel
                if cand.exists():
                    return str(cand)
    return None


def _singlefile_cmd() -> Optional[list[str]]:
    """Comando base do single-file-cli, ou None se indisponível.

    Preferência: binário global `single-file` → `npx -y -p single-file-cli`
    (baixa o pacote on-demand — AGPL invocado como processo externo).
    """
    if shutil.which("single-file"):
        return ["single-file"]
    if shutil.which("npx"):
        return ["npx", "-y", "-p", "single-file-cli", "single-file"]
    return None


# ------------------------------ Pós-processamento ---------------------------- #

# data URI base64 (imagens/fontes embedadas) — é o que transforma 14MB em
# linhas de ~1M chars. Placeholder preserva a estrutura do markup.
_B64_DATA_URI_RE = re.compile(r"data:[a-zA-Z0-9.+/-]+;base64,[A-Za-z0-9+/=]+")
# SVG url-encoded NÃO é base64 (data:image/svg+xml,%3Csvg...) — regex separada.
_SVG_URLENC_RE = re.compile(r"data:image/svg\+xml[^\"'()\s>]+")

_STRIP_PLACEHOLDER = "data:image/STRIPPED"

MAX_LINE_CHARS = 500


def _rewrap_line(line: str) -> list[str]:
    """Quebra uma linha gigante em pedaços legíveis pro Read (best-effort).

    ref.ai.html não é verdade visual (ref.full.html é) — whitespace extra entre
    tags/declarações CSS é aceitável aqui.
    """
    if len(line) <= MAX_LINE_CHARS:
        return [line]
    # 1) quebra entre tags adjacentes
    line = re.sub(r">\s*<", ">\n<", line)
    parts: list[str] = []
    for piece in line.split("\n"):
        if len(piece) <= MAX_LINE_CHARS * 2:
            parts.append(piece)
            continue
        # 2) CSS minificado: quebra após fim de bloco e declarações
        piece = re.sub(r"\}\s*", "}\n", piece)
        piece = re.sub(r";\s*(?=[a-zA-Z@.#*:-])", ";\n", piece)
        for sub in piece.split("\n"):
            # 3) último recurso: hard-wrap em espaço
            while len(sub) > MAX_LINE_CHARS * 4:
                cut = sub.rfind(" ", 0, MAX_LINE_CHARS * 4)
                if cut <= 0:
                    cut = MAX_LINE_CHARS * 4
                parts.append(sub[:cut])
                sub = sub[cut:]
            parts.append(sub)
    return parts


def build_ai_readable(full_html: str) -> str:
    """ref.full.html → ref.ai.html: strip de data-URIs + rewrap de linhas longas."""
    stripped = _B64_DATA_URI_RE.sub(_STRIP_PLACEHOLDER, full_html)
    stripped = _SVG_URLENC_RE.sub(_STRIP_PLACEHOLDER, stripped)
    out_lines: list[str] = []
    for line in stripped.split("\n"):
        out_lines.extend(_rewrap_line(line))
    return "\n".join(out_lines)


# --------------------------------- Capture ----------------------------------- #


def capture_url(url: str, full_path: Path) -> int:
    """Captura `url` com single-file-cli usando o Chromium do Playwright."""
    base_cmd = _singlefile_cmd()
    if base_cmd is None:
        print(SETUP_INSTRUCTIONS, file=sys.stderr)
        return EXIT_NO_SINGLEFILE

    chromium = find_chromium()
    if chromium is None:
        print(
            "[snapshot] Chromium do Playwright não encontrado.\n"
            "[snapshot] Rode: pip install playwright && playwright install chromium\n"
            "[snapshot] (ou aponte um Chrome/Chromium existente via env AURA_CHROMIUM)",
            file=sys.stderr,
        )
        return EXIT_NO_CHROMIUM

    # Flags canônicas: networkAlmostIdle (networkIdle dá timeout em site com
    # trackers), load-max-time como teto duro, viewport desktop padrão da Aura.
    cmd = base_cmd + [
        url,
        str(full_path),
        f"--browser-executable-path={chromium}",
        f"--user-agent={USER_AGENT}",
        "--browser-wait-until=networkAlmostIdle",
        f"--browser-load-max-time={BROWSER_LOAD_MAX_TIME_MS}",
        "--browser-width=1440",
        "--browser-height=900",
    ]
    print(f"[snapshot] $ {' '.join(cmd[:3])} ... (single-file-cli, chromium do Playwright)")
    try:
        result = subprocess.run(cmd, check=False, timeout=CAPTURE_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        print(f"[snapshot] captura excedeu {CAPTURE_TIMEOUT_SECONDS}s — abortada.", file=sys.stderr)
        return EXIT_CAPTURE_FAILED
    except FileNotFoundError:
        print(SETUP_INSTRUCTIONS, file=sys.stderr)
        return EXIT_NO_SINGLEFILE

    if result.returncode != 0 or not full_path.exists() or full_path.stat().st_size == 0:
        print(
            f"[snapshot] single-file-cli falhou (rc={result.returncode}) ou não gerou output. "
            "Se o site tem anti-bot forte, use a rota manual: extensão SingleFile no Chrome "
            "do membro + snapshot.py <arquivo-salvo> --output <dir>.",
            file=sys.stderr,
        )
        return EXIT_CAPTURE_FAILED
    return EXIT_OK


def ingest_local(source: Path, full_path: Path) -> int:
    """Ingere um .html já self-contained (extensão SingleFile do membro)."""
    try:
        data = source.read_bytes()
    except OSError as exc:
        print(f"[snapshot] não consegui ler {source}: {exc}", file=sys.stderr)
        return EXIT_CAPTURE_FAILED
    if not data.strip():
        print(f"[snapshot] arquivo vazio: {source}", file=sys.stderr)
        return EXIT_CAPTURE_FAILED
    full_path.write_bytes(data)
    return EXIT_OK


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="snapshot.py",
        description=(
            "Snapshot fiel de página via single-file-cli (URL) ou ingestão de .html "
            "salvo pela extensão SingleFile (path local). Gera ref.full.html "
            "(verdade visual — a IA nunca lê cru) + ref.ai.html (data-URIs "
            "stripped, linhas re-quebradas — leitura sempre segmentada)."
        ),
    )
    parser.add_argument("source", help="URL (http/https) ou path de um .html local")
    parser.add_argument("--output", required=True, help="Diretório de saída")
    parser.add_argument("--json", action="store_true", help="Imprime resumo JSON no stdout")
    args = parser.parse_args(argv)

    try:
        output_dir = validate_output_path(args.output)
    except ValueError as exc:
        print(f"ERRO: --output inválido: {exc}", file=sys.stderr)
        return EXIT_INVALID_INPUT
    output_dir.mkdir(parents=True, exist_ok=True)

    full_path = output_dir / "ref.full.html"
    ai_path = output_dir / "ref.ai.html"

    local_candidate = Path(args.source).expanduser()
    if local_candidate.is_file():
        source_kind = "local-file"
        source_label = f"file://{local_candidate.resolve()}"
        print(f"[snapshot] ingerindo arquivo local: {local_candidate}")
        rc = ingest_local(local_candidate, full_path)
    else:
        source_kind = "single-file-cli"
        try:
            source_label = validate_url(args.source)
        except ValueError as exc:
            print(
                f"ERRO: {args.source!r} não é um arquivo local existente nem URL válida: {exc}",
                file=sys.stderr,
            )
            return EXIT_INVALID_INPUT
        rc = capture_url(source_label, full_path)
    if rc != EXIT_OK:
        return rc

    print("[snapshot] pós-processando (strip de data-URIs + rewrap)...")
    try:
        full_html = full_path.read_text(encoding="utf-8", errors="replace")
        ai_path.write_text(build_ai_readable(full_html), encoding="utf-8")
    except OSError as exc:
        print(f"[snapshot] pós-processamento falhou: {exc}", file=sys.stderr)
        return EXIT_CAPTURE_FAILED

    summary = {
        "source": source_label,
        "tool": source_kind,
        "captured_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "full_html": str(full_path),
        "full_bytes": full_path.stat().st_size,
        "ai_html": str(ai_path),
        "ai_bytes": ai_path.stat().st_size,
    }
    (output_dir / "snapshot.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"[snapshot] ref.full.html: {summary['full_bytes']:,} bytes (verdade visual — NÃO ler cru)")
    print(f"[snapshot] ref.ai.html:   {summary['ai_bytes']:,} bytes (AI-readable — ler SEGMENTADO)")
    print(f"[snapshot] snapshot.json: {output_dir / 'snapshot.json'}")
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    return EXIT_OK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[snapshot] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
