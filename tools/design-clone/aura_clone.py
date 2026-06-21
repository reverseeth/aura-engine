#!/usr/bin/env python3
"""
aura_clone.py — CLI wrapper unificado do pipeline design-clone.

Dois modos:

  1) signals (default) — orquestra downloader → analyzer → pattern-extractor.
     Produz `patterns.json` (design_system abstrato) pra rota de brand-signals
     da 07a-page-design. NÃO copia código do concorrente.

  2) clone-and-adapt — orquestra downloader → analyzer → skeleton-builder.
     Dada uma URL de referência, captura a ESTRUTURA de sections (ordem + tipo +
     layout) e produz um ESQUELETO HTML (`skeleton.html`) com sections vazias /
     placeholder, preservando hierarquia/layout do concorrente mas SEM nenhuma
     copy/imagem/marca dele. A 07a entrega esse esqueleto ao Claude, que o
     preenche com a copy/brand/produto do membro (06-copy / 04-offer) gerando
     `design/page.html`. Herda a hierarquia de conversão validada, não o conteúdo.

Robustez: se o scraping de DOM falha (anti-bot/Cloudflare/timeout), o downloader
cai num fallback de screenshot full-page (`raw/fallback-screenshot.png`) que serve
à rota screenshot→visão da 07a. O clone-and-adapt detecta esse caso e reporta.

Uso:
    # Modo signals (default)
    python3 aura_clone.py <url> --output=<dir> [--product=<slug>]
                              [--skip-images] [--pattern-only]

    # Modo clone-and-adapt (esqueleto HTML estrutural)
    python3 aura_clone.py clone-and-adapt <url> --output=<dir> [--product=<slug>]

Output (modo signals):
    <dir>/
        raw/           (HTML, CSS, imagens, computed-styles.json)
        analysis.json  (output do analyzer)
        patterns.json  (output do pattern-extractor)
        manifest.json  (URL, timestamp, versão do wrapper)

Output (modo clone-and-adapt):
    <dir>/
        raw/           (HTML/CSS/screenshot do concorrente — referência LOCAL, não vai pro tema)
        analysis.json  (sections detectadas — ordem + tipo + layout)
        skeleton.html  (ESQUELETO estrutural: placeholders, zero conteúdo do concorrente)
        skeleton.json  (mesma estrutura em dados, pra a 07a/Claude consumir)
        manifest.json  (URL, timestamp, versão, status de cada passo)
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


# --------------------------- skeleton builder (clone-and-adapt) ------------- #

# Placeholder neutro por tipo semântico — descreve o PAPEL da section, nunca
# repete copy do concorrente. A 07a/Claude substitui pelo conteúdo do membro.
_SKELETON_ROLE = {
    "header": "Navegação / topo do site",
    "hero": "Hero — promessa principal + CTA primário",
    "trust-bar": "Trust bar — logos / 'as seen in' / selos",
    "features": "Features / benefícios — blocos do mecanismo",
    "stats": "Stats / números de prova",
    "steps": "Como funciona — passos / processo",
    "gallery": "Galeria / carrossel de imagens do produto",
    "testimonials": "Depoimentos / reviews",
    "pricing": "Oferta / pricing / bundle",
    "faq": "FAQ — perguntas frequentes",
    "cta": "CTA de fechamento",
    "footer": "Rodapé",
    "unknown": "Section genérica (tipo não detectado)",
}


def _layout_hint(section: dict) -> dict:
    """Deriva hints de layout COARSE (não copia CSS) a partir da analysis.

    Usa só os campos estruturais que o analyzer já expôs: repeating_pattern
    (grid de N colunas), presença de heading e contagem de imagens. Nenhum hex,
    nenhuma fonte, nenhum texto do concorrente entra aqui.
    """
    rp = section.get("repeating_pattern", {}) or {}
    count = rp.get("count", 0) if rp.get("detected") else 0
    sem = section.get("semantic_type", "unknown") or "unknown"
    # FAQ/steps são listas verticais (accordion/timeline), não grids multi-coluna.
    _list_types = {"faq", "steps"}
    if count >= 2 and sem in _list_types:
        layout = "list"
    elif count >= 2:
        cols = min(count, 4)  # clamp visual; a 07a decide o número final
        layout = f"grid-{cols}col" if cols >= 2 else "stack"
    else:
        layout = "stack"
    img_count = len(section.get("images", []) or [])
    return {
        "layout": layout,
        "repeat_items": count,
        "media": "image" if img_count else "none",
        "media_slots": img_count,
    }


def _esc(text: str) -> str:
    return (
        (text or "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_skeleton(analysis: dict, url: str, product: Optional[str]) -> tuple[str, dict]:
    """Constrói o esqueleto HTML + a estrutura em dados a partir do analysis.json.

    O esqueleto preserva ORDEM + TIPO + layout coarse de cada section, mas cada
    section é um PLACEHOLDER vazio: zero copy, zero imagem, zero marca do
    concorrente. Comentários e data-attributes guiam o Claude a preencher com o
    conteúdo do membro (06-copy / 04-offer).
    """
    sections_in = analysis.get("sections", []) or []
    skel_sections: list[dict] = []
    body_parts: list[str] = []

    for i, sec in enumerate(sections_in, start=1):
        sem = sec.get("semantic_type", "unknown") or "unknown"
        role = _SKELETON_ROLE.get(sem, _SKELETON_ROLE["unknown"])
        hint = _layout_hint(sec)
        slug = f"section-{i:02d}-{sem}"

        skel_sections.append(
            {
                "order": i,
                "semantic_type": sem,
                "role": role,
                "layout": hint["layout"],
                "repeat_items": hint["repeat_items"],
                "media": hint["media"],
                "media_slots": hint["media_slots"],
                "tag": sec.get("tag"),
            }
        )

        # Placeholders de itens repetíveis (cards), se houver.
        items_html = ""
        if hint["repeat_items"] >= 2:
            cards = "\n".join(
                f'        <div class="placeholder-card" data-item="{n}">'
                f"<!-- item {n}: preencher com conteúdo do membro --></div>"
                for n in range(1, hint["repeat_items"] + 1)
            )
            items_html = (
                f'\n      <div class="placeholder-grid" '
                f'data-layout="{hint["layout"]}">\n{cards}\n      </div>'
            )

        media_html = ""
        if hint["media_slots"]:
            media_html = (
                f'\n      <div class="placeholder-media" '
                f'data-slots="{hint["media_slots"]}">'
                f"<!-- {hint['media_slots']} slot(s) de imagem do produto do MEMBRO --></div>"
            )

        body_parts.append(
            f'    <section class="{slug}" data-semantic="{sem}" '
            f'data-layout="{hint["layout"]}">\n'
            f"      <!-- {role}. Layout: {hint['layout']}. "
            f"PREENCHER com copy/brand/imagens do MEMBRO — NÃO usar conteúdo do concorrente. -->\n"
            f'      <div class="placeholder-heading"><!-- headline/subhead --></div>\n'
            f'      <div class="placeholder-body"><!-- corpo da copy --></div>'
            f"{media_html}{items_html}\n"
            f'      <div class="placeholder-cta"><!-- CTA se aplicável --></div>\n'
            f"    </section>"
        )

    skeleton_data = {
        "kind": "clone-and-adapt-skeleton",
        "source_url": url,
        "product_slug": product,
        "wrapper_version": WRAPPER_VERSION,
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "total_sections": len(skel_sections),
        "sections": skel_sections,
        "notice": (
            "Esqueleto ESTRUTURAL apenas. Nenhuma copy/imagem/marca do concorrente. "
            "A 07a preenche cada placeholder com o conteúdo do membro (06-copy / 04-offer). "
            "Adaptar estrutura + trocar todo o conteúdo é defensável; copiar 1:1 não."
        ),
    }

    notice = _esc(skeleton_data["notice"])
    html = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>Skeleton — {_esc(product or 'aura-clone-and-adapt')}</title>\n"
        f"  <!-- {notice} -->\n"
        f"  <!-- source (referência local, NÃO publicar): {_esc(url)} -->\n"
        "</head>\n"
        "<body>\n"
        f"  <!-- {len(skel_sections)} sections, na ordem do concorrente. "
        "Cada uma é um placeholder pra preencher. -->\n"
        + "\n".join(body_parts)
        + "\n</body>\n</html>\n"
    )
    return html, skeleton_data


def _run_clone_and_adapt(
    url: str, output_dir: Path, raw_dir: Path, product: Optional[str], python_exe: str
) -> int:
    """Orquestra o modo clone-and-adapt: download → analyzer → skeleton."""
    steps_status: dict = {}
    analysis_path = output_dir / "analysis.json"
    skeleton_html_path = output_dir / "skeleton.html"
    skeleton_json_path = output_dir / "skeleton.json"
    manifest_path = output_dir / "manifest.json"

    # Passo 1: downloader (com fallback de screenshot embutido nele)
    downloader_cmd = [python_exe, str(_THIS_DIR / "downloader.py"), url, str(raw_dir)]
    rc = _run_step("downloader", downloader_cmd)
    steps_status["downloader"] = {"returncode": rc, "ok": rc == 0}

    fallback_only = (raw_dir / "fallback.json").exists()
    has_dom = (raw_dir / "page.html").exists()

    if rc != 0 or fallback_only or not has_dom:
        # DOM scraping falhou → só temos (talvez) o screenshot full-page.
        steps_status["mode"] = "screenshot_fallback"
        manifest_path.write_text(
            json.dumps(
                {
                    **_manifest(url, output_dir, product, steps_status),
                    "clone_mode": "clone-and-adapt",
                    "skeleton": None,
                    "fallback_screenshot": (
                        "raw/fallback-screenshot.png"
                        if (raw_dir / "fallback-screenshot.png").exists()
                        else None
                    ),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print("\n[aura_clone] ===== CLONE-AND-ADAPT (FALLBACK) =====", file=sys.stderr)
        print(
            "[aura_clone] scraping de DOM falhou (anti-bot/Cloudflare/timeout). "
            "Sem esqueleto estrutural.",
            file=sys.stderr,
        )
        if (raw_dir / "fallback-screenshot.png").exists():
            print(
                f"[aura_clone] screenshot full-page disponível: "
                f"{raw_dir / 'fallback-screenshot.png'}",
                file=sys.stderr,
            )
            print(
                "[aura_clone] → siga pela rota screenshot→visão da 07a "
                "(Claude lê a imagem e reconstrói a estrutura).",
                file=sys.stderr,
            )
        return 2

    # Passo 2: analyzer
    analyzer_cmd = [python_exe, str(_THIS_DIR / "analyzer.py"), str(raw_dir)]
    rc = _run_step("analyzer", analyzer_cmd)
    steps_status["analyzer"] = {"returncode": rc, "ok": rc == 0}
    if rc != 0 or not (raw_dir / "sections.json").exists():
        print(
            "[aura_clone] analyzer falhou — sem sections pra montar esqueleto.",
            file=sys.stderr,
        )
        manifest_path.write_text(
            json.dumps(_manifest(url, output_dir, product, steps_status), indent=2),
            encoding="utf-8",
        )
        return 2

    _move_analyzer_output(raw_dir, analysis_path)

    # Passo 3: skeleton builder (in-process, sem subprocess)
    print("\n[aura_clone] ===== skeleton-builder =====")
    try:
        analysis = json.loads((raw_dir / "sections.json").read_text(encoding="utf-8"))
        skeleton_html, skeleton_data = build_skeleton(analysis, url, product)
        skeleton_html_path.write_text(skeleton_html, encoding="utf-8")
        skeleton_json_path.write_text(
            json.dumps(skeleton_data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        steps_status["skeleton"] = {
            "ok": True,
            "sections": skeleton_data["total_sections"],
        }
        skeleton_ok = True
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("skeleton-builder falhou: %s", exc)
        steps_status["skeleton"] = {"ok": False, "error": str(exc)}
        skeleton_ok = False

    manifest_path.write_text(
        json.dumps(
            {
                **_manifest(url, output_dir, product, steps_status),
                "clone_mode": "clone-and-adapt",
                "skeleton": "skeleton.html" if skeleton_ok else None,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n[aura_clone] ===== CLONE-AND-ADAPT SUMMARY =====")
    print(f"[aura_clone] url:          {url}")
    print(f"[aura_clone] output_dir:   {output_dir}")
    print(f"[aura_clone] analysis:     {analysis_path}")
    print(
        f"[aura_clone] skeleton:     "
        f"{'OK (' + str(skeleton_data['total_sections']) + ' sections)' if skeleton_ok else 'MISSING'}"
    )
    print(f"[aura_clone] manifest:     {manifest_path}")
    print(
        "[aura_clone] NOTA: esqueleto é ESTRUTURA apenas. A 07a preenche com a "
        "copy/brand do membro. Zero conteúdo do concorrente vai pro tema."
    )
    return 0 if skeleton_ok else 2


_VALID_MODES = {"signals", "clone-and-adapt"}


def main(argv: Optional[list[str]] = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)

    # `mode` é um subcomando opcional no início. Se o primeiro token for um modo
    # conhecido, consome-o; senão assume "signals" (preserva a CLI antiga
    # `aura_clone.py <url> --output=...`).
    mode = "signals"
    if raw_argv and raw_argv[0] in _VALID_MODES:
        mode = raw_argv.pop(0)

    parser = argparse.ArgumentParser(
        prog="aura_clone.py [signals|clone-and-adapt]",
        description=(
            "Aura Engine design-clone pipeline wrapper. "
            "Modo 'signals' (default): design_system abstrato. "
            "Modo 'clone-and-adapt': esqueleto HTML estrutural pra 07a preencher."
        ),
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
    args = parser.parse_args(raw_argv)

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

    # Modo clone-and-adapt: download → analyzer → skeleton estrutural.
    if mode == "clone-and-adapt":
        return _run_clone_and_adapt(url, output_dir, raw_dir, args.product, python_exe)

    # Modo signals (default): download → analyzer → pattern-extractor.
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
