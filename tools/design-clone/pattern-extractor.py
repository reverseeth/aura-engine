#!/usr/bin/env python3
"""
pattern-extractor.py — Aura Engine design-clone pipeline · Modo C

Lê o output do downloader + analyzer e extrai APENAS a estrutura semântica
e os sinais de design (cores, fontes, spacing, radius) de um concorrente.
NÃO copia código. NÃO preserva HTML do concorrente. Produz patterns.json
que o fresh-generator (orquestrado pela skill 06) usa pra criar um design
novo, inspirado no visual mas limpo, theme-agnostic, e editável.

Uso:
    python3 pattern-extractor.py <clone_dir>

Exemplo:
    python3 pattern-extractor.py /tmp/clone-gruns

Output:
    <clone_dir>/patterns.json

Dependências:
    pip install beautifulsoup4
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("ERRO: BeautifulSoup4 não instalado. Rode: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


HEX_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b|rgba?\([^)]+\)")
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
    """True se a cor é saturada (não preto/branco/cinza)."""
    if rgb is None:
        return False
    r, g, b = rgb
    mx = max(r, g, b)
    mn = min(r, g, b)
    if mx - mn < 30:
        return False
    if mx < 30 or mn > 220:
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


def detect_layout_pattern(section_dict):
    """Infere o padrão de layout da section (split-lr, centered, grid-3col, carousel, full-bleed)."""
    html = section_dict.get("html", "")
    soup = BeautifulSoup(html, "html.parser")

    images = section_dict.get("images", [])
    has_image = len(images) > 0

    has_h1 = bool(soup.find("h1"))
    has_h2 = bool(soup.find("h2"))
    repeating = section_dict.get("repeating_pattern", {})
    repeat_count = repeating.get("count", 0)
    semantic_type = section_dict.get("semantic_type", "unknown")

    if semantic_type == "hero":
        if has_image and (has_h1 or has_h2):
            return "split-lr"
        if has_h1:
            return "centered-bold"
        return "full-bleed"

    if semantic_type in ("features", "benefits"):
        if repeat_count == 3:
            return "grid-3col"
        if repeat_count == 4:
            return "grid-4col"
        if repeat_count >= 5:
            return "grid-multi"
        return "grid-3col"

    if semantic_type == "testimonials":
        if repeat_count >= 4:
            return "grid-multi"
        return "carousel"

    if semantic_type == "faq":
        return "accordion-stacked"

    if semantic_type == "pricing":
        if repeat_count == 2:
            return "tiers-2col"
        if repeat_count == 3:
            return "tiers-3col"
        return "tiers-grid"

    if semantic_type == "cta":
        return "full-bleed-centered"

    if has_image and (has_h1 or has_h2):
        return "split-lr"
    if has_h1 or has_h2:
        return "centered"
    return "stacked"


def detect_content_slots(section_dict):
    """Detecta os 'slots' de conteúdo que a section espera (o que a fresh-gen vai preencher)."""
    html = section_dict.get("html", "")
    soup = BeautifulSoup(html, "html.parser")
    semantic_type = section_dict.get("semantic_type", "unknown")

    slots = {}

    h1 = soup.find("h1")
    h2 = soup.find("h2")
    if h1:
        txt = h1.get_text(strip=True)
        slots["heading"] = {"tag": "h1", "length_hint": len(txt) if txt else 60}
    elif h2:
        txt = h2.get_text(strip=True)
        slots["heading"] = {"tag": "h2", "length_hint": len(txt) if txt else 60}

    paragraphs = soup.find_all("p")
    if paragraphs:
        first_p = paragraphs[0]
        ptxt = first_p.get_text(strip=True)
        slots["subhead"] = {"tag": "p", "length_hint": len(ptxt) if ptxt else 120}

    buttons = soup.find_all(["button", "a"])
    cta_candidates = [b for b in buttons if any(
        kw in " ".join(b.get("class", []) or []).lower()
        for kw in ("btn", "button", "cta")
    )]
    if cta_candidates:
        btn_txt = cta_candidates[0].get_text(strip=True)
        slots["cta_label"] = {"tag": "button", "length_hint": len(btn_txt) if btn_txt else 20}

    images = section_dict.get("images", [])
    if images:
        slots["image"] = {"count": len(images), "has_alt": any(img.get("alt") for img in images)}

    repeating = section_dict.get("repeating_pattern", {})
    if repeating.get("detected"):
        count = repeating.get("count", 0)
        if semantic_type == "testimonials":
            slots["testimonials"] = {"count": count, "fields": ["quote", "author_name", "author_role"]}
        elif semantic_type in ("features", "benefits"):
            slots["features"] = {"count": count, "fields": ["icon_or_image", "title", "description"]}
        elif semantic_type == "faq":
            slots["faq_items"] = {"count": count, "fields": ["question", "answer"]}
        elif semantic_type == "pricing":
            slots["pricing_tiers"] = {"count": count, "fields": ["name", "price", "features_list", "cta"]}
        else:
            slots["items"] = {"count": count, "fields": ["title", "description"]}

    return slots


def build_section_pattern(section_dict):
    """Constrói o pattern objeto final de uma section (sem HTML do concorrente)."""
    return {
        "index": section_dict.get("index"),
        "type": section_dict.get("semantic_type", "unknown"),
        "confidence": section_dict.get("confidence", 0),
        "layout": detect_layout_pattern(section_dict),
        "slots": detect_content_slots(section_dict),
        "visual_hints": {
            "has_repeating_items": section_dict.get("repeating_pattern", {}).get("detected", False),
            "repeating_count": section_dict.get("repeating_pattern", {}).get("count", 0),
            "image_count": len(section_dict.get("images", [])),
        },
        "description": section_dict.get("description", ""),
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 pattern-extractor.py <clone_dir>", file=sys.stderr)
        sys.exit(1)

    clone_dir = Path(sys.argv[1]).expanduser().resolve()
    sections_path = clone_dir / "sections.json"
    computed_path = clone_dir / "computed-styles.json"

    if not sections_path.exists():
        print(f"ERRO: {sections_path} não encontrado. Rode analyzer.py primeiro.", file=sys.stderr)
        sys.exit(1)

    print(f"[pattern-extractor] lendo {sections_path}")
    sections_data = json.loads(sections_path.read_text(encoding="utf-8"))
    computed = json.loads(computed_path.read_text(encoding="utf-8")) if computed_path.exists() else []

    print("[pattern-extractor] extraindo design signals (cores, fontes, spacing)...")
    design_system = extract_design_signals(computed)

    print("[pattern-extractor] detectando patterns por section...")
    patterns = []
    for section in sections_data.get("sections", []):
        patterns.append(build_section_pattern(section))

    output = {
        "source": str(clone_dir),
        "design_system": design_system,
        "sections": patterns,
        "meta": {
            "total_sections": len(patterns),
            "computed_styles_elements": len(computed),
        },
    }

    out_path = clone_dir / "patterns.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"[pattern-extractor] {len(patterns)} patterns extraídos")
    print(f"[pattern-extractor] design system:")
    print(f"  - fontes: {design_system['typography']['heading_font']} / {design_system['typography']['body_font']}")
    print(f"  - cores: bg={design_system['colors']['background_primary']} · text={design_system['colors']['text_primary']} · accents={design_system['colors']['accents']}")
    print(f"  - shape: radius={design_system['shape']['border_radius_px']}px · shadow={design_system['shape']['shadow_style']}")
    print(f"  - density: {design_system['spacing']['density']} (avg padding {design_system['spacing']['avg_padding_px']}px)")
    print(f"[pattern-extractor] salvo em {out_path}")
    print(f"\n[pattern-extractor] próximo passo: o skill 06 (modo C) usa este patterns.json + copy.md pra gerar HTML fresh via frontend-design, depois converter pra Liquid")


if __name__ == "__main__":
    main()
