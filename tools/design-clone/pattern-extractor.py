#!/usr/bin/env python3
"""
pattern-extractor.py — Aura Engine design-clone pipeline · Brand Signals

Lê o output do downloader (computed-styles.json) e extrai APENAS os sinais de
design agregados de um site de referência (cores, fontes, radius, shadow,
densidade de spacing). NÃO copia código. NÃO preserva HTML do concorrente.
Produz patterns.json com o bloco `design_system` que a skill 07a-page-design
(ETAPA 2 — Brand Signals) consome como caminho 3 de signals.

Não requer o analyzer.py: o único input é o computed-styles.json do downloader.

Uso:
    python3 pattern-extractor.py <clone_dir>

Exemplo:
    python3 pattern-extractor.py /tmp/ref-gruns

Output:
    <clone_dir>/patterns.json
"""

import json
import logging
import re
import sys
from collections import Counter
from pathlib import Path

# Bootstrap re-exec (mesmo padrão do fetch.py da lib web-fetch): se o python
# atual não tem chardet e o venv do design-clone existe, re-executa nele.
# Sem venv, segue no python atual — o guard abaixo degrada pro fallback
# utf-8-sig/latin-1 do read_text_robust.
try:
    from _venv_bootstrap import bootstrap as _venv_bootstrap
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _venv_bootstrap import bootstrap as _venv_bootstrap
_venv_bootstrap("chardet")

try:
    import chardet  # type: ignore
    _HAS_CHARDET = True
except ImportError:
    _HAS_CHARDET = False


logger = logging.getLogger("design_clone.pattern_extractor")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


def read_text_robust(path: Path) -> str:
    """Lê arquivo tratando BOM (utf-8-sig) com fallback chardet → latin-1."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        pass
    raw = path.read_bytes()
    if _HAS_CHARDET:
        detected = chardet.detect(raw)
        enc = (detected or {}).get("encoding") or "latin-1"
        try:
            return raw.decode(enc, errors="replace")
        except LookupError:
            pass
    return raw.decode("latin-1", errors="replace")


PX_VALUE_RE = re.compile(r"([\d.]+)(px|rem|em)")


def parse_rgba(value):
    """Converte 'rgba(r, g, b, a)' ou 'rgb(r,g,b)' em tuple (r,g,b) normalizado 0-255. None se inválido."""
    m = re.match(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)", value)
    if m:
        return (int(float(m.group(1))), int(float(m.group(2))), int(float(m.group(3))))
    if value.startswith("#"):
        h = value.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return None


def is_vivid(rgb):
    """True se a cor é saturada (não preto, branco ou cinza próximo)."""
    if rgb is None:
        return False
    r, g, b = rgb
    mx = max(r, g, b)
    mn = min(r, g, b)
    # Rejeita branco puro/quase-branco explicitamente
    if mx > 240 and mn > 240:
        return False
    # Rejeita preto puro/quase-preto explicitamente
    if mx < 30:
        return False
    # Rejeita cinza (saturação baixa)
    if mx - mn < 30:
        return False
    # Guard-rail adicional: luz extremamente alta com saturação baixa == off-white
    if mn > 220:
        return False
    return True


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def extract_design_signals(computed_styles):
    """Analisa computed-styles.json e extrai sinais de design agregados."""
    font_headings = Counter()
    font_body = Counter()
    bg_colors = Counter()
    text_colors = Counter()
    accent_colors = Counter()
    radii = Counter()
    shadows = Counter()
    paddings = []
    margins = []

    for el in computed_styles:
        tag = el.get("tag", "").lower()
        styles = el.get("styles", {})
        rect = el.get("rect", {})

        ff = styles.get("font-family", "").strip().strip("\"'")
        if ff:
            if tag in ("h1", "h2", "h3"):
                font_headings[ff] += 3 if tag == "h1" else 2 if tag == "h2" else 1
            elif tag in ("p", "span", "li", "a"):
                font_body[ff] += 1

        bg = styles.get("background-color", "")
        if bg and "rgba(0, 0, 0, 0)" not in bg and "transparent" not in bg:
            rgb = parse_rgba(bg)
            if rgb:
                area = rect.get("width", 0) * rect.get("height", 0)
                hex_color = rgb_to_hex(rgb)
                if area > 50_000:
                    bg_colors[hex_color] += int(area / 10_000)
                if is_vivid(rgb):
                    accent_colors[hex_color] += int(area / 1_000) if area > 1_000 else 1

        col = styles.get("color", "")
        if col:
            rgb = parse_rgba(col)
            if rgb:
                text_colors[rgb_to_hex(rgb)] += 1

        br = styles.get("border-radius", "0px")
        m = PX_VALUE_RE.search(br)
        if m:
            try:
                val = float(m.group(1))
                if 4 <= val <= 100:
                    radii[int(val)] += 1
            except ValueError:
                pass

        sh = styles.get("box-shadow", "")
        if sh and sh != "none":
            shadows[sh.strip()] += 1

        for prop in ("padding", "margin"):
            val = styles.get(prop, "")
            for m in PX_VALUE_RE.finditer(val):
                try:
                    v = float(m.group(1))
                    if 4 <= v <= 200:
                        (paddings if prop == "padding" else margins).append(int(v))
                except ValueError:
                    pass

    heading_font = font_headings.most_common(1)[0][0] if font_headings else "system-ui"
    body_font = font_body.most_common(1)[0][0] if font_body else "system-ui"

    primary_bg = bg_colors.most_common(1)[0][0] if bg_colors else "#ffffff"
    accent_list = [c for c, _ in accent_colors.most_common(3)]
    text_primary = text_colors.most_common(1)[0][0] if text_colors else "#1a1a1a"

    most_common_radius = radii.most_common(1)[0][0] if radii else 8

    avg_padding = int(sum(paddings) / len(paddings)) if paddings else 24
    if avg_padding < 16:
        density = "tight"
    elif avg_padding < 40:
        density = "medium"
    else:
        density = "generous"

    shadow_style = "none"
    if shadows:
        sh = shadows.most_common(1)[0][0]
        if "rgba" in sh or "rgb" in sh:
            if any(big in sh for big in ("20px", "24px", "30px", "40px")):
                shadow_style = "large"
            elif any(mid in sh for mid in ("8px", "10px", "12px", "16px")):
                shadow_style = "medium"
            else:
                shadow_style = "subtle"

    return {
        "typography": {
            "heading_font": heading_font,
            "body_font": body_font,
        },
        "colors": {
            "background_primary": primary_bg,
            "text_primary": text_primary,
            "accents": accent_list,
        },
        "shape": {
            "border_radius_px": most_common_radius,
            "shadow_style": shadow_style,
        },
        "spacing": {
            "density": density,
            "avg_padding_px": avg_padding,
        },
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 pattern-extractor.py <clone_dir>", file=sys.stderr)
        sys.exit(1)

    clone_dir = Path(sys.argv[1]).expanduser().resolve()
    computed_path = clone_dir / "computed-styles.json"

    # Sem computed-styles.json não existe sinal REAL nenhum — emitir defaults como
    # se fossem a paleta do site violaria o invariante de zero alucinação.
    if not computed_path.exists():
        print(
            f"ERRO: {computed_path} não encontrado. Rode downloader.py primeiro — é ele "
            f"que gera o computed-styles.json de onde os sinais reais saem.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"[pattern-extractor] lendo {computed_path}")
    try:
        computed = json.loads(read_text_robust(computed_path))
    except json.JSONDecodeError as exc:
        print(
            f"ERRO: JSON inválido em {computed_path} (linha {exc.lineno} col {exc.colno}): {exc.msg}. "
            f"Re-rode downloader.py — sem computed styles válidos o design_system seria inventado.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not isinstance(computed, list):
        computed = []

    print("[pattern-extractor] extraindo design signals (cores, fontes, spacing)...")
    design_system = extract_design_signals(computed)
    design_system_source = "extracted" if computed else "defaults_fallback"
    if design_system_source == "defaults_fallback":
        logger.warning(
            "computed-styles.json está vazio — o design_system abaixo contém DEFAULTS "
            "genéricos, NÃO sinais do site. A 07a não deve usar isso como brand signals."
        )

    output = {
        "source": str(clone_dir),
        "design_system": design_system,
        # "extracted" = sinais reais do site; "defaults_fallback" = valores genéricos
        # (a 07a DEVE ignorar o bloco nesse caso e cair pro próximo caminho de signals).
        "design_system_source": design_system_source,
        "meta": {
            "computed_styles_elements": len(computed),
        },
    }

    out_path = clone_dir / "patterns.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    tag = "" if design_system_source == "extracted" else " (DEFAULTS — não são sinais do site)"
    print(f"[pattern-extractor] design system{tag}:")
    print(f"  - fontes: {design_system['typography']['heading_font']} / {design_system['typography']['body_font']}")
    print(f"  - cores: bg={design_system['colors']['background_primary']} · text={design_system['colors']['text_primary']} · accents={design_system['colors']['accents']}")
    print(f"  - shape: radius={design_system['shape']['border_radius_px']}px · shadow={design_system['shape']['shadow_style']}")
    print(f"  - density: {design_system['spacing']['density']} (avg padding {design_system['spacing']['avg_padding_px']}px)")
    print(f"[pattern-extractor] salvo em {out_path}")
    print("\n[pattern-extractor] próximo passo: a skill 07a-page-design (ETAPA 2 — Brand Signals) lê o bloco design_system deste patterns.json")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[pattern-extractor] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
