#!/usr/bin/env python3
"""
preview.py — Renderiza um .liquid gerado pelo liquid-converter como HTML standalone.

O arquivo .liquid normalmente só funciona dentro de um tema Shopify. Este script
lê a section, extrai os defaults do {% schema %}, substitui {{ section.settings.X }}
pelos valores default, expande {% content_for 'blocks' %} (N instâncias com
defaults do block), injeta o CSS original do concorrente (que foi baixado pelo
downloader), e gera um HTML standalone pra visualização no browser.

Uso:
    python3 preview.py \\
        --section <path.liquid> \\
        --blocks-dir <path> \\
        --styles <path/styles.css> \\
        --images-dir <path/images> \\
        --images-json <path/images.json> \\
        --output <preview.html> \\
        [--blocks-count 3]

Exemplo:
    python3 preview.py \\
        --section /tmp/test-stripe-out/sections/page-mybrand-hero.liquid \\
        --blocks-dir /tmp/test-stripe-out/blocks \\
        --styles /tmp/clone-test-stripe/styles.css \\
        --images-dir /tmp/clone-test-stripe/images \\
        --images-json /tmp/clone-test-stripe/images.json \\
        --output /tmp/preview.html

Depois:
    open /tmp/preview.html
"""

import argparse
import json
import re
import sys
from pathlib import Path


SECTION_SPLIT_RE = re.compile(r"\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}", re.DOTALL)
STYLESHEET_RE = re.compile(r"\{%\s*stylesheet\s*%\}(.*?)\{%\s*endstylesheet\s*%\}", re.DOTALL)
SCHEMA_RE = SECTION_SPLIT_RE
CONTENT_FOR_BLOCKS_RE = re.compile(r"\{%\s*content_for\s+['\"]blocks['\"]\s*%\}")
IF_BLOCK_RE = re.compile(r"\{%\s*if\s+section\.settings\.(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}", re.DOTALL)
SETTINGS_VAR_RE = re.compile(r"\{\{\s*section\.settings\.(\w+)(?:\s*\|\s*([^}]+?))?\s*\}\}")


def parse_liquid_file(liquid_path):
    """Lê um arquivo .liquid e retorna (markup, stylesheet, schema_dict)."""
    content = liquid_path.read_text(encoding="utf-8")

    schema_match = SCHEMA_RE.search(content)
    schema = json.loads(schema_match.group(1).strip()) if schema_match else {}

    stylesheet_match = STYLESHEET_RE.search(content)
    stylesheet = stylesheet_match.group(1).strip() if stylesheet_match else ""

    markup = content
    if schema_match:
        markup = markup.replace(schema_match.group(0), "")
    if stylesheet_match:
        markup = markup.replace(stylesheet_match.group(0), "")

    return markup.strip(), stylesheet, schema


def settings_to_defaults(settings):
    """Converte lista de settings do schema em dict {id: {type, default}}."""
    out = {}
    for s in settings or []:
        out[s["id"]] = {"type": s.get("type"), "default": s.get("default", "")}
    return out


def apply_settings(markup, defaults, images_url_map):
    """Substitui {{ section.settings.X }} e {% if section.settings.X %} pelos defaults."""

    def replace_if(m):
        sid = m.group(1)
        inner = m.group(2)
        entry = defaults.get(sid)
        if entry and entry.get("default"):
            return inner
        return ""

    def replace_var(m):
        sid = m.group(1)
        filters = (m.group(2) or "").strip()
        entry = defaults.get(sid)
        if not entry:
            return ""
        default = entry.get("default") or ""
        s_type = entry.get("type")

        if s_type == "image_picker":
            # No preview, substitui por placeholder (não temos o objeto image do Shopify)
            return "/tmp/preview-placeholder.svg"
        if s_type == "url":
            return str(default) if default else "#"
        if s_type == "richtext":
            return str(default)
        return str(default)

    markup = IF_BLOCK_RE.sub(replace_if, markup)
    markup = SETTINGS_VAR_RE.sub(replace_var, markup)
    return markup


def inject_image_url_placeholders(markup, images_url_map, images_dir):
    """Substitui placeholders de image_picker por imagens locais aleatórias pra preview."""
    local_images = sorted(images_dir.glob("*")) if images_dir.exists() else []
    if not local_images:
        return markup
    counter = [0]

    def replace_placeholder(m):
        rel = local_images[counter[0] % len(local_images)]
        counter[0] += 1
        return f'src="file://{rel}"'

    markup = re.sub(
        r'src="[^"]*preview-placeholder\.svg"',
        replace_placeholder,
        markup,
    )
    return markup


def render_blocks(blocks_dir, namespace, count, images_dir):
    """Renderiza N instâncias de cada block type com defaults."""
    if not blocks_dir or not blocks_dir.exists():
        return ""

    rendered = []
    block_files = sorted(blocks_dir.glob(f"{namespace}-*.liquid"))
    for block_file in block_files:
        markup, _, schema = parse_liquid_file(block_file)
        defaults = settings_to_defaults(schema.get("settings", []))
        for _ in range(count):
            instance = apply_settings(markup, defaults, {})
            instance = inject_image_url_placeholders(instance, {}, images_dir)
            rendered.append(instance)

    return "\n".join(rendered)


def detect_namespace(schema):
    cls = schema.get("class", "")
    parts = cls.split()
    for p in parts:
        if "__" not in p and "--" not in p:
            return p
    return "page-preview"


def build_html(markup, stylesheet, external_css_path):
    external_css = ""
    if external_css_path and external_css_path.exists():
        external_css = external_css_path.read_text(encoding="utf-8")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aura Engine — Design Clone Preview</title>
<style>
/* Reset básico */
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif; }}

/* CSS original do concorrente (escopo global — pode conflitar) */
{external_css}

/* CSS da section gerada */
{stylesheet}

/* Placeholder pra imagens faltantes */
img[src=""], img:not([src]) {{ display: none; }}
.icon-placeholder {{ display: inline-block; width: 1em; height: 1em; background: #ccc; border-radius: 2px; }}
</style>
</head>
<body>
<div style="max-width: 100%; overflow-x: hidden; padding: 20px;">
<div style="background: #fffbea; border: 1px solid #e8b93a; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; font-size: 13px; color: #555;">
<strong>Preview — Aura Engine Design Clone.</strong> Este é um preview do .liquid gerado, renderizado como HTML standalone. Imagens são placeholders. Algumas interações JS não funcionam (web components Shopify foram removidos, animations do concorrente também).
</div>
{markup}
</div>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", required=True, help="Path to .liquid section file")
    parser.add_argument("--blocks-dir", default=None, help="Directory with block .liquid files")
    parser.add_argument("--styles", default=None, help="Path to original styles.css from downloader")
    parser.add_argument("--images-dir", default=None, help="Directory with downloaded images")
    parser.add_argument("--images-json", default=None, help="images.json from downloader")
    parser.add_argument("--output", required=True, help="Path to output .html")
    parser.add_argument("--blocks-count", type=int, default=3, help="How many block instances to render")
    args = parser.parse_args()

    section_path = Path(args.section).expanduser().resolve()
    if not section_path.exists():
        print(f"ERRO: {section_path} não encontrado", file=sys.stderr)
        sys.exit(1)

    markup, stylesheet, schema = parse_liquid_file(section_path)
    defaults = settings_to_defaults(schema.get("settings", []))

    images_dir = Path(args.images_dir).expanduser().resolve() if args.images_dir else None
    if images_dir and not images_dir.exists():
        images_dir = None

    images_url_map = {}
    if args.images_json:
        p = Path(args.images_json).expanduser().resolve()
        if p.exists():
            images_url_map = json.loads(p.read_text(encoding="utf-8"))

    markup_filled = apply_settings(markup, defaults, images_url_map)
    markup_filled = inject_image_url_placeholders(markup_filled, images_url_map, images_dir or Path("/dev/null"))

    if args.blocks_dir:
        blocks_dir = Path(args.blocks_dir).expanduser().resolve()
        namespace = detect_namespace(schema)
        blocks_markup = render_blocks(blocks_dir, namespace, args.blocks_count, images_dir or Path("/dev/null"))
        markup_filled = CONTENT_FOR_BLOCKS_RE.sub(lambda _: blocks_markup, markup_filled)

    external_css = Path(args.styles).expanduser().resolve() if args.styles else None

    html = build_html(markup_filled, stylesheet, external_css)
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"[preview] gerado: {output_path}")
    print(f"[preview] settings aplicados: {len(defaults)}")
    print(f"[preview] blocks: {args.blocks_count if args.blocks_dir else 0} instâncias por tipo")
    print(f"[preview] abra no browser:")
    print(f"  open {output_path}")


if __name__ == "__main__":
    main()
