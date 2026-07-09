#!/usr/bin/env python3
"""
aura_clone.py — CLI wrapper unificado do pipeline design-clone.

Dois modos:

  1) signals (default) — orquestra captura → pattern-extractor (o analyzer é
     OPCIONAL nesse modo: roda só pra produzir analysis.json de contexto; o
     pattern-extractor lê direto o computed-styles.json e não depende dele).
     Produz `patterns.json` (design_system abstrato) pra rota de brand-signals
     da 07a-page-design. NÃO copia código do concorrente.

  2) clone-and-adapt — orquestra captura → analyzer → skeleton-builder.
     Dada uma URL de referência, captura a ESTRUTURA de sections (ordem + tipo +
     layout) e produz um ESQUELETO HTML (`skeleton.html`) com sections vazias /
     placeholder, preservando hierarquia/layout do concorrente mas SEM nenhuma
     copy/imagem/marca dele. Quando a captura veio do downloader (computed-styles
     disponíveis), cada section do `skeleton.json` carrega também um bloco
     `hierarchy` com sinais NUMÉRICOS de hierarquia visual (proporção heading/
     body, padding-block real, densidade, alinhamento dominante, proporção de
     área de mídia). A 07a entrega esse esqueleto ao Claude, que o preenche com
     a copy/brand/produto do membro (06-copy / 04-offer) gerando
     `design/page.html`. Herda a hierarquia de conversão validada, não o conteúdo.

Cascade de captura (--engine=auto, default):

  1. downloader.py — Playwright stealth (DOM + computed-styles + assets)
  2. snapshot.py   — single-file-cli (HTML self-contained; vira page.html via
                     ref.ai.html; sem computed-styles → serve pro clone-and-adapt,
                     mas o modo signals falha honesto: sem CSS computado real
                     não há design_system — nada de paleta inventada)
  3. screenshot-fallback do downloader → rota screenshot→visão da 07a
  4. MANUAL: membro salva a página com a extensão SingleFile no Chrome dele
     (vence Cloudflare/login) e a Aura ingere via --from-file

Uso:
    # Modo signals (default)
    python3 aura_clone.py <url> --output=<dir> [--product=<slug>]
                              [--engine=auto|downloader|singlefile]
                              [--skip-images] [--pattern-only]

    # Modo clone-and-adapt (esqueleto HTML estrutural)
    python3 aura_clone.py clone-and-adapt <url> --output=<dir> [--product=<slug>]
                              [--engine=auto|downloader|singlefile]

    # Ingestão manual (arquivo salvo pela extensão SingleFile do membro)
    python3 aura_clone.py [clone-and-adapt] --from-file=<path.html> --output=<dir>

Output (modo signals):
    <dir>/
        raw/           (HTML, CSS, imagens, computed-styles.json)
        analysis.json  (output do analyzer — opcional; ausente com --pattern-only
                        ou se o analyzer falhar, sem bloquear o patterns.json)
        patterns.json  (output do pattern-extractor)
        manifest.json  (URL, timestamp, versão, engine, status de cada passo)

Output (modo clone-and-adapt):
    <dir>/
        raw/           (HTML/CSS/screenshot do concorrente — referência LOCAL, não vai pro tema)
        analysis.json  (sections detectadas — ordem + tipo + layout + hierarchy)
        skeleton.html  (ESQUELETO estrutural: placeholders, zero conteúdo do concorrente)
        skeleton.json  (mesma estrutura em dados + sinais de hierarquia visual
                        por section, pra a 07a/Claude consumir)
        manifest.json  (URL, timestamp, versão, engine, status de cada passo)

Robustez: se o DOM falha em todas as engines automatizadas, o wrapper reporta o
screenshot-fallback (se houver) e o manifest ganha `"mode": "screenshot_fallback"`
top-level. Se o screenshot capturou uma página de CHALLENGE anti-bot
(`challenge_detected` no fallback.json), o wrapper avisa que ele NÃO serve pra
rota visão e aponta a rota manual (--from-file).
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

# Bootstrap re-exec (mesmo padrão do fetch.py da lib web-fetch): se o python
# atual não tem Playwright e um venv do framework existe, re-executa nele.
# Assim `python3 aura_clone.py` direto funciona E os subprocessos do pipeline
# (invocados com sys.executable) herdam o python do venv. Sem venv, segue —
# a ingestão --from-file não usa browser e os passos avisam o setup.
from _venv_bootstrap import bootstrap as _venv_bootstrap  # noqa: E402
_venv_bootstrap("playwright")

from downloader import validate_url, validate_output_path  # noqa: E402

WRAPPER_VERSION = "1.2.0"

SINGLEFILE_EXTENSION_URL = (
    "https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle"
)

logger = logging.getLogger("design_clone.aura_clone")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


def _run_step(label: str, cmd: list[str], env: Optional[dict] = None) -> int:
    """Executa subprocess com log, retorna return code."""
    print(f"\n[aura_clone] ===== {label} =====")
    print(f"[aura_clone] $ {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=False, env=env)
        return result.returncode
    except FileNotFoundError as exc:
        logger.error("binário não encontrado em %s: %s", label, exc)
        return 127
    except OSError as exc:
        logger.error("falha ao executar %s: %s", label, exc)
        return 1


def _manifest(url: str, output_dir: Path, product: Optional[str], steps: dict,
              engine: Optional[str] = None) -> dict:
    return {
        "url": url,
        "output_dir": str(output_dir),
        "product_slug": product,
        "wrapper_version": WRAPPER_VERSION,
        "engine": engine,
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


def _clear_stale_run_state(raw_dir: Path) -> None:
    """Remove outputs derivados de runs anteriores no mesmo --output.

    Sem isso, um retry após bloqueio herda `fallback.json`/`sections.json`
    velhos: retry bem-sucedido era tratado como fallback (skeleton nunca saía)
    e um sections.json de OUTRA página podia alimentar o pattern-extractor.
    """
    for name in ("fallback.json", "fallback-screenshot.png", "sections.json", "patterns.json"):
        f = raw_dir / name
        try:
            if f.exists():
                f.unlink()
        except OSError as exc:
            logger.warning("não consegui limpar %s: %s", f, exc)


def _fallback_state(raw_dir: Path) -> dict:
    """Lê o estado de fallback gravado pelo downloader (se houver)."""
    state = {
        "fallback_only": (raw_dir / "fallback.json").exists(),
        "has_dom": (raw_dir / "page.html").exists(),
        "challenge": False,
        "screenshot": None,
    }
    fb = raw_dir / "fallback.json"
    if fb.exists():
        try:
            data = json.loads(fb.read_text(encoding="utf-8"))
            state["challenge"] = bool(data.get("challenge_detected"))
        except (OSError, json.JSONDecodeError):
            pass
    shot = raw_dir / "fallback-screenshot.png"
    if shot.exists():
        state["screenshot"] = shot
    return state


def _run_snapshot(source: str, raw_dir: Path, python_exe: str, steps_status: dict) -> bool:
    """Roda snapshot.py e promove ref.ai.html → raw/page.html pro analyzer."""
    rc = _run_step(
        "snapshot (single-file-cli)",
        [python_exe, str(_THIS_DIR / "snapshot.py"), source, "--output", str(raw_dir)],
    )
    steps_status["snapshot"] = {"returncode": rc, "ok": rc == 0}
    if rc != 0:
        return False
    ai_html = raw_dir / "ref.ai.html"
    if not ai_html.exists():
        steps_status["snapshot"]["ok"] = False
        return False
    try:
        (raw_dir / "page.html").write_text(
            ai_html.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (raw_dir / "meta.json").write_text(
            json.dumps(
                {"url": source, "fetched_at": _dt.datetime.now(_dt.timezone.utc).isoformat()},
                indent=2,
            ),
            encoding="utf-8",
        )
    except OSError as exc:
        logger.error("falha promovendo ref.ai.html → page.html: %s", exc)
        steps_status["snapshot"]["ok"] = False
        return False
    return True


def _acquire(url: Optional[str], raw_dir: Path, args, python_exe: str,
             env: dict, steps_status: dict) -> dict:
    """Cascade de captura. Retorna {"dom_ready": bool, "engine": str|None}."""
    if args.from_file:
        src = str(Path(args.from_file).expanduser().resolve())
        ok = _run_snapshot(src, raw_dir, python_exe, steps_status)
        if not ok:
            print(
                f"[aura_clone] ingestão de {src} falhou — o arquivo está legível/completo? "
                "Re-salve a página com a extensão SingleFile e tente de novo.",
                file=sys.stderr,
            )
        return {"dom_ready": ok, "engine": "from-file" if ok else None}

    if args.engine == "singlefile":
        ok = _run_snapshot(url, raw_dir, python_exe, steps_status)
        return {"dom_ready": ok, "engine": "singlefile" if ok else None}

    # auto | downloader: Playwright stealth primeiro (único que extrai
    # computed-styles — melhor fidelidade pro design_system).
    rc = _run_step(
        "downloader",
        [python_exe, str(_THIS_DIR / "downloader.py"), url, str(raw_dir)],
        env=env,
    )
    steps_status["downloader"] = {"returncode": rc, "ok": rc == 0}
    state = _fallback_state(raw_dir)
    if rc == 0 and state["has_dom"] and not state["fallback_only"]:
        return {"dom_ready": True, "engine": "downloader"}

    if args.engine == "auto":
        print(
            "[aura_clone] DOM via downloader falhou — tentando snapshot single-file-cli...",
            file=sys.stderr,
        )
        if _run_snapshot(url, raw_dir, python_exe, steps_status):
            return {"dom_ready": True, "engine": "singlefile"}

    return {"dom_ready": False, "engine": None}


def _abort_screenshot_fallback(
    mode: str,
    url: str,
    output_dir: Path,
    raw_dir: Path,
    product: Optional[str],
    steps_status: dict,
    manifest_path: Path,
) -> int:
    """Saída padronizada quando nenhuma engine automatizada conseguiu DOM."""
    state = _fallback_state(raw_dir)
    steps_status["mode"] = "screenshot_fallback"
    manifest = {
        **_manifest(url, output_dir, product, steps_status, engine=None),
        "mode": "screenshot_fallback",
        "clone_mode": mode,
        "challenge_detected": state["challenge"],
        "fallback_screenshot": (
            "raw/fallback-screenshot.png" if state["screenshot"] else None
        ),
    }
    if mode == "clone-and-adapt":
        manifest["skeleton"] = None
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\n[aura_clone] ===== {mode.upper()} (FALLBACK) =====", file=sys.stderr)
    print(
        "[aura_clone] scraping de DOM falhou em todas as engines automatizadas "
        "(anti-bot/Cloudflare/timeout).",
        file=sys.stderr,
    )
    if state["screenshot"] and state["challenge"]:
        print(
            "[aura_clone] ATENÇÃO: o screenshot capturado é a PÁGINA DE CHALLENGE "
            "anti-bot, não a página real — NÃO use na rota screenshot→visão.",
            file=sys.stderr,
        )
    elif state["screenshot"]:
        print(
            f"[aura_clone] screenshot full-page disponível: {state['screenshot']}",
            file=sys.stderr,
        )
        print(
            "[aura_clone] → siga pela rota screenshot→visão da 07a "
            "(Claude lê a imagem e reconstrói a estrutura).",
            file=sys.stderr,
        )
    print(
        "[aura_clone] Rota manual (vence Cloudflare/login): membro instala a extensão "
        f"SingleFile ({SINGLEFILE_EXTENSION_URL}), salva a página no Chrome dele e a Aura "
        "ingere com: aura_clone.py "
        + ("clone-and-adapt " if mode == "clone-and-adapt" else "")
        + "--from-file=<arquivo.html> --output=<dir>",
        file=sys.stderr,
    )
    return 2


# --------------------------- skeleton builder (clone-and-adapt) ------------- #

# Placeholder neutro por tipo semântico — descreve o PAPEL da section, nunca
# repete copy do concorrente. A 07a/Claude substitui pelo conteúdo do membro.
_SKELETON_ROLE = {
    "header": "Navegação / topo do site",
    "hero": "Hero — promessa principal + CTA primário",
    "trust-bar": "Trust bar — logos / 'as seen in' / selos",
    "features": "Features / benefícios — blocos do mecanismo",
    "stats": "Stats / números de prova",
    "steps": "Passos / processo / timeline",
    "how-it-works": "Como funciona — mecanismo em passos",
    "ingredients": "Ingredientes / fórmula — o que tem dentro e por quê",
    "before-after": "Antes/depois — prova visual de transformação",
    "comparison-table": "Tabela comparativa — nós vs. alternativas",
    "guarantee": "Garantia / reversão de risco — selo + termos",
    "founder-story": "História do fundador / da marca — conexão e razão de existir",
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
    img_count = len(section.get("images", []) or [])
    # FAQ/steps são listas verticais (accordion/timeline), não grids multi-coluna.
    _list_types = {"faq", "steps"}
    if sem == "comparison-table":
        # Linhas repetíveis de tabela comparativa não são cards de grid.
        layout = "table"
    elif sem == "before-after" and (count == 2 or img_count >= 2):
        layout = "split-2col"
    elif count >= 2 and sem in _list_types:
        layout = "list"
    elif count >= 2:
        cols = min(count, 4)  # clamp visual; a 07a decide o número final
        layout = f"grid-{cols}col" if cols >= 2 else "stack"
    else:
        layout = "stack"
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


def _hierarchy_comment(hierarchy: Optional[dict]) -> str:
    """Comentário compacto de hierarquia visual pro skeleton.html (se houver).

    Direção de ênfase/espaçamento pra quem preenche — nunca CSS literal.
    """
    if not hierarchy:
        return ""
    bits: list[str] = []
    fs = hierarchy.get("font_scale") or {}
    if fs.get("heading_to_body"):
        bits.append(f"heading/body {fs['heading_to_body']}x")
    pad = hierarchy.get("padding_block_px") or {}
    if pad.get("top") is not None and pad.get("bottom") is not None:
        bits.append(f"padding-block {int(pad['top'])}/{int(pad['bottom'])}px")
    dens = hierarchy.get("density") or {}
    if dens.get("label"):
        bits.append(f"densidade {dens['label']}")
    if hierarchy.get("dominant_alignment"):
        bits.append(f"alinhamento {hierarchy['dominant_alignment']}")
    mtb = hierarchy.get("media_text_balance") or {}
    if mtb.get("media_area_ratio") is not None:
        bits.append(f"mídia {int(round(mtb['media_area_ratio'] * 100))}% da área")
    if not bits:
        return ""
    return (
        f"\n      <!-- Hierarquia da referência: {'; '.join(bits)}. "
        "Usar como DIREÇÃO de ênfase/espaçamento ao preencher, não como CSS literal. -->"
    )


def build_skeleton(analysis: dict, url: str, product: Optional[str]) -> tuple[str, dict]:
    """Constrói o esqueleto HTML + a estrutura em dados a partir do analysis.json.

    O esqueleto preserva ORDEM + TIPO + layout coarse de cada section, mas cada
    section é um PLACEHOLDER vazio: zero copy, zero imagem, zero marca do
    concorrente. Comentários e data-attributes guiam o Claude a preencher com o
    conteúdo do membro (06-copy / 04-offer).

    Quando o analyzer extraiu `hierarchy` (computed-styles disponíveis), cada
    section do skeleton.json carrega os sinais de hierarquia visual da
    referência (proporção heading/body, padding-block, densidade, alinhamento,
    proporção de mídia) — a 07a usa isso como direção ao preencher, pra não
    achatar a hierarquia que fazia a página converter.
    """
    sections_in = analysis.get("sections", []) or []
    skel_sections: list[dict] = []
    body_parts: list[str] = []

    for i, sec in enumerate(sections_in, start=1):
        sem = sec.get("semantic_type", "unknown") or "unknown"
        role = _SKELETON_ROLE.get(sem, _SKELETON_ROLE["unknown"])
        hint = _layout_hint(sec)
        hierarchy = sec.get("hierarchy") or None
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
                "hierarchy": hierarchy,
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
            f"PREENCHER com copy/brand/imagens do MEMBRO — NÃO usar conteúdo do concorrente. -->"
            f"{_hierarchy_comment(hierarchy)}\n"
            f'      <div class="placeholder-heading"><!-- headline/subhead --></div>\n'
            f'      <div class="placeholder-body"><!-- corpo da copy --></div>'
            f"{media_html}{items_html}\n"
            f'      <div class="placeholder-cta"><!-- CTA se aplicável --></div>\n'
            f"    </section>"
        )

    hierarchy_count = sum(1 for s in skel_sections if s.get("hierarchy"))
    skeleton_data = {
        "kind": "clone-and-adapt-skeleton",
        "source_url": url,
        "product_slug": product,
        "wrapper_version": WRAPPER_VERSION,
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "total_sections": len(skel_sections),
        "hierarchy_sections": hierarchy_count,
        "hierarchy_available": hierarchy_count > 0,
        "sections": skel_sections,
        "notice": (
            "Esqueleto ESTRUTURAL apenas. Nenhuma copy/imagem/marca do concorrente. "
            "A 07a preenche cada placeholder com o conteúdo do membro (06-copy / 04-offer). "
            "O bloco `hierarchy` de cada section (quando presente) traz sinais NUMÉRICOS "
            "de hierarquia visual da referência (proporções, espaçamento, densidade) — "
            "direção de ênfase pro preenchimento, nunca CSS/conteúdo do concorrente. "
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
    url: str,
    output_dir: Path,
    raw_dir: Path,
    args,
    python_exe: str,
    env: dict,
) -> int:
    """Orquestra o modo clone-and-adapt: captura (cascade) → analyzer → skeleton."""
    steps_status: dict = {}
    analysis_path = output_dir / "analysis.json"
    skeleton_html_path = output_dir / "skeleton.html"
    skeleton_json_path = output_dir / "skeleton.json"
    manifest_path = output_dir / "manifest.json"

    # Passo 1: captura via cascade (downloader → singlefile → screenshot)
    acq = _acquire(url, raw_dir, args, python_exe, env, steps_status)
    if not acq["dom_ready"]:
        return _abort_screenshot_fallback(
            "clone-and-adapt", url, output_dir, raw_dir, args.product,
            steps_status, manifest_path,
        )

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
            json.dumps(
                _manifest(url, output_dir, args.product, steps_status, engine=acq["engine"]),
                indent=2,
            ),
            encoding="utf-8",
        )
        return 2

    _move_analyzer_output(raw_dir, analysis_path)

    # Passo 3: skeleton builder (in-process, sem subprocess)
    print("\n[aura_clone] ===== skeleton-builder =====")
    try:
        analysis = json.loads((raw_dir / "sections.json").read_text(encoding="utf-8"))
        skeleton_html, skeleton_data = build_skeleton(analysis, url, args.product)
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
                **_manifest(url, output_dir, args.product, steps_status, engine=acq["engine"]),
                "clone_mode": "clone-and-adapt",
                "skeleton": "skeleton.html" if skeleton_ok else None,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n[aura_clone] ===== CLONE-AND-ADAPT SUMMARY =====")
    print(f"[aura_clone] url:          {url}")
    print(f"[aura_clone] engine:       {acq['engine']}")
    print(f"[aura_clone] output_dir:   {output_dir}")
    print(f"[aura_clone] analysis:     {analysis_path}")
    print(
        f"[aura_clone] skeleton:     "
        f"{'OK (' + str(skeleton_data['total_sections']) + ' sections)' if skeleton_ok else 'MISSING'}"
    )
    if skeleton_ok:
        hc = skeleton_data.get("hierarchy_sections", 0)
        print(
            f"[aura_clone] hierarchy:    "
            + (
                f"{hc}/{skeleton_data['total_sections']} sections com sinais de hierarquia visual"
                if hc
                else "ausente (captura sem computed-styles — engine singlefile/--from-file)"
            )
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
            "Modo 'clone-and-adapt': esqueleto HTML estrutural pra 07a preencher. "
            "Captura em cascade: downloader (Playwright stealth) → snapshot "
            "(single-file-cli) → screenshot-fallback → --from-file (manual)."
        ),
    )
    parser.add_argument(
        "url", nargs="?", default=None,
        help="URL do site a clonar (dispensável com --from-file)",
    )
    parser.add_argument("--output", required=True, help="Diretório de saída")
    parser.add_argument("--product", default=None, help="Slug do produto (opcional)")
    parser.add_argument(
        "--engine",
        choices=("auto", "downloader", "singlefile"),
        default="auto",
        help=(
            "Engine de captura. auto (default): downloader com fallback pra "
            "single-file-cli; downloader: só Playwright; singlefile: só "
            "single-file-cli (sem computed-styles — serve pro clone-and-adapt; "
            "no modo signals não gera patterns.json)"
        ),
    )
    parser.add_argument(
        "--from-file",
        default=None,
        metavar="PATH",
        help=(
            "Ingere um .html local já salvo (ex: pela extensão SingleFile no "
            "Chrome do membro — rota manual que vence Cloudflare/login). "
            "Dispensa a URL."
        ),
    )
    parser.add_argument(
        "--skip-images",
        action="store_true",
        help="Não baixa imagens (mais rápido, só pra extrair design signals)",
    )
    parser.add_argument(
        "--pattern-only",
        action="store_true",
        help=(
            "Pula o analyzer e gera só o patterns.json (o pattern-extractor "
            "lê direto o computed-styles.json — não requer sections.json)"
        ),
    )
    args = parser.parse_args(raw_argv)

    # Validação de input
    url: Optional[str] = None
    if args.from_file:
        from_path = Path(args.from_file).expanduser()
        if not from_path.is_file():
            print(f"ERRO: --from-file não existe: {from_path}", file=sys.stderr)
            return 1
        if args.url:
            print(
                "ERRO: use URL OU --from-file, não os dois "
                "(--from-file ingere um arquivo já salvo).",
                file=sys.stderr,
            )
            return 1
        url = f"file://{from_path.resolve()}"
    else:
        if not args.url:
            print("ERRO: informe a URL (ou --from-file=<path.html>).", file=sys.stderr)
            return 1
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

    # Estado limpo: outputs derivados de runs anteriores no mesmo --output são
    # removidos (retry pós-bloqueio não pode herdar fallback.json/sections.json
    # velhos).
    _clear_stale_run_state(raw_dir)

    python_exe = sys.executable or "python3"
    env = os.environ.copy()
    if args.skip_images:
        env["AURA_SKIP_IMAGES"] = "1"

    # Modo clone-and-adapt: captura → analyzer → skeleton estrutural.
    if mode == "clone-and-adapt":
        return _run_clone_and_adapt(url, output_dir, raw_dir, args, python_exe, env)

    # Modo signals (default): captura → analyzer → pattern-extractor.
    steps_status: dict = {}

    # Passo 1: captura via cascade
    acq = _acquire(url, raw_dir, args, python_exe, env, steps_status)
    if not acq["dom_ready"]:
        return _abort_screenshot_fallback(
            "signals", url, output_dir, raw_dir, args.product, steps_status, manifest_path
        )

    # O modo signals precisa de computed-styles REAIS (anti-alucinação: o
    # pattern-extractor recusa gerar design_system sem eles). Engines
    # singlefile/from-file não extraem CSS computado — falha honesta e cedo.
    if not (raw_dir / "computed-styles.json").exists():
        print(
            f"[aura_clone] engine '{acq['engine']}' não extrai computed-styles — o modo "
            "signals exige eles pra sinais reais (nada de paleta inventada). "
            "Use --engine=downloader (ou o default auto com o site acessível), "
            "ou a rota screenshot→visão da 07a. Esta captura continua útil pro "
            "modo clone-and-adapt (estrutura).",
            file=sys.stderr,
        )
        steps_status["pattern_extractor"] = {
            "ok": False,
            "skipped": "sem computed-styles.json (engine não extrai CSS computado)",
        }
        manifest_path.write_text(
            json.dumps(
                _manifest(url, output_dir, args.product, steps_status, engine=acq["engine"]),
                indent=2,
            ),
            encoding="utf-8",
        )
        return 2

    # Passo 2: analyzer — OPCIONAL no modo signals. O pattern-extractor lê
    # direto o computed-styles.json (não requer sections.json); o analyzer só
    # agrega o analysis.json de contexto. Com --pattern-only, pula inteiro;
    # se rodar e falhar, avisa e segue — nunca bloqueia o patterns.json.
    analyzer_ok = False
    if args.pattern_only:
        steps_status["analyzer"] = {
            "ok": False,
            "skipped": "--pattern-only (pattern-extractor não requer o analyzer)",
        }
    else:
        analyzer_cmd = [python_exe, str(_THIS_DIR / "analyzer.py"), str(raw_dir)]
        rc = _run_step("analyzer (opcional)", analyzer_cmd)
        steps_status["analyzer"] = {"returncode": rc, "ok": rc == 0}
        if rc == 0:
            analyzer_ok = _move_analyzer_output(raw_dir, analysis_path)
        else:
            logger.warning(
                "analyzer falhou (rc=%s) — seguindo sem analysis.json "
                "(o pattern-extractor não depende dele)", rc
            )

    # Passo 3: pattern-extractor
    pattern_cmd = [python_exe, str(_THIS_DIR / "pattern-extractor.py"), str(raw_dir)]
    rc = _run_step("pattern-extractor", pattern_cmd)
    pattern_ok = False
    if rc == 0:
        pattern_ok = _move_pattern_output(raw_dir, patterns_path)
    else:
        logger.warning("pattern-extractor falhou (rc=%s)", rc)
    # "ok" reflete o ARQUIVO copiado, não só o rc do subprocess.
    steps_status["pattern_extractor"] = {"returncode": rc, "ok": pattern_ok}

    # Manifest final
    manifest_path.write_text(
        json.dumps(
            _manifest(url, output_dir, args.product, steps_status, engine=acq["engine"]),
            indent=2,
        ),
        encoding="utf-8",
    )

    print("\n[aura_clone] ===== SUMMARY =====")
    print(f"[aura_clone] url:          {url}")
    print(f"[aura_clone] engine:       {acq['engine']}")
    print(f"[aura_clone] output_dir:   {output_dir}")
    print(f"[aura_clone] raw/:         {raw_dir}")
    analysis_label = "OK" if analyzer_ok else (
        "SKIPPED (--pattern-only)" if args.pattern_only else "MISSING (opcional)"
    )
    print(f"[aura_clone] analysis:     {analysis_label}")
    print(f"[aura_clone] patterns:     {'OK' if pattern_ok else 'MISSING'}")
    print(f"[aura_clone] manifest:     {manifest_path}")

    # Return 0 só se o patterns.json realmente existe no root
    return 0 if pattern_ok else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[aura_clone] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
