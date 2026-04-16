#!/usr/bin/env python3
"""
liquid-converter.py — Aura Engine design-clone pipeline (step 3 of 3)

Recebe uma seção (HTML+CSS) identificada pelo analyzer.py e converte em Shopify
Liquid section editável via theme editor. Substitui textos fixos por
{{ section.settings.* }}, imagens por image_picker settings, cores por CSS
custom properties, e padrões repetíveis por blocks separados.

Uso:
    python3 liquid-converter.py \\
        --section <path-to-section-json> \\
        --sections-json <path-to-sections.json-from-analyzer> \\
        --output <path-to-.liquid-output> \\
        --blocks-dir <path-to-blocks-dir-output> \\
        --namespace page-<produto> \\
        --product-slug <produto>

Exemplo:
    python3 liquid-converter.py \\
        --section-index 1 \\
        --sections-json /tmp/clone-undone-1/sections.json \\
        --output ~/shopify-theme/sections/page-undone-hero.liquid \\
        --blocks-dir ~/shopify-theme/blocks \\
        --namespace page-undone \\
        --product-slug undone

Dependências:
    pip install beautifulsoup4
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print("ERRO: BeautifulSoup4 não instalado. Rode: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


# Tags cujo texto direto vira setting
TEXT_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "span", "a", "button", "li", "blockquote", "em", "strong", "small", "label"}
RICHTEXT_TAGS = {"p"}
LONG_TEXT_THRESHOLD = 80  # chars — acima disso usa richtext


def slugify(text, max_len=40):
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:max_len] or "field"


def is_script_or_style(el):
    return el.name in ("script", "style", "noscript", "iframe")


def remove_junk(soup):
    """Remove tracking, scripts, analytics, frameworks."""
    for tag in soup.find_all(["script", "noscript", "iframe"]):
        tag.decompose()
    for attr in ("data-tracking", "data-analytics", "data-gtm", "data-fbpixel"):
        for el in soup.find_all(attrs={attr: True}):
            del el[attr]


def namespace_classes(soup, namespace):
    """Substitui classes do concorrente por namespace próprio."""
    for el in soup.find_all(True):
        if el.has_attr("class"):
            original = el["class"]
            mapped = []
            for c in original:
                mapped.append(f"{namespace}__{slugify(c)}")
            el["class"] = mapped
        if el.has_attr("id"):
            el["id"] = f"{namespace}-{slugify(el['id'])}"


def clean_inline_styles(soup):
    """Remove CSS inline que referencia assets externos do concorrente."""
    for el in soup.find_all(style=True):
        style = el["style"]
        style = re.sub(r"url\((?!\{\{)[^)]*\)", "", style)
        style = re.sub(r";\s*;", ";", style).strip("; ").strip()
        if style:
            el["style"] = style
        else:
            del el["style"]


class LiquidBuilder:
    def __init__(self, namespace, product_slug):
        self.namespace = namespace
        self.product_slug = product_slug
        self.settings = []
        self.blocks_schemas = {}
        self.used_ids = set()
        self.repeating_pattern = None

    def unique_id(self, base):
        candidate = base
        i = 2
        while candidate in self.used_ids:
            candidate = f"{base}_{i}"
            i += 1
        self.used_ids.add(candidate)
        return candidate

    def add_setting(self, s_id, s_type, label, default=None, info=None):
        entry = {"type": s_type, "id": s_id, "label": label}
        if default is not None:
            entry["default"] = default
        if info:
            entry["info"] = info
        self.settings.append(entry)
        return s_id

    def convert_text_node(self, el, context_label):
        text = el.get_text(strip=True)
        if not text or not text.strip():
            return
        s_type = "richtext" if (el.name in RICHTEXT_TAGS or len(text) > LONG_TEXT_THRESHOLD) else "text"
        s_id = self.unique_id(slugify(context_label or text[:30]))
        default = text if s_type == "text" else f"<p>{text}</p>"
        self.add_setting(s_id, s_type, context_label or text[:40], default=default)
        new_tag = BeautifulSoup("", "html.parser").new_tag(el.name)
        new_tag.attrs = dict(el.attrs)
        placeholder = "{{ section.settings." + s_id + " }}"
        new_tag.append(BeautifulSoup(placeholder, "html.parser"))
        el.replace_with(new_tag)

    def convert_image(self, el):
        s_id = self.unique_id(slugify((el.get("alt") or "image")))
        self.add_setting(s_id, "image_picker", f"Image: {el.get('alt', '')}"[:60])
        liquid = (
            '{% if section.settings.' + s_id + ' %}'
            '<img src="{{ section.settings.' + s_id + ' | image_url: width: 1600 }}" '
            'alt="{{ section.settings.' + s_id + '.alt | default: \'\' }}" loading="lazy">'
            '{% endif %}'
        )
        el.replace_with(BeautifulSoup(liquid, "html.parser"))

    def convert_link(self, el):
        text = el.get_text(strip=True)
        href = el.get("href") or "#"
        label_id = self.unique_id(slugify((text or "link") + "_label"))
        url_id = self.unique_id(slugify((text or "link") + "_url"))
        self.add_setting(label_id, "text", "Link label", default=text)
        self.add_setting(url_id, "url", "Link URL", default=href)
        new_a = BeautifulSoup("", "html.parser").new_tag("a")
        new_a["href"] = "{{ section.settings." + url_id + " }}"
        if el.has_attr("class"):
            new_a["class"] = el["class"]
        new_a.append(BeautifulSoup("{{ section.settings." + label_id + " }}", "html.parser"))
        el.replace_with(new_a)

    def process(self, section_dict):
        html = section_dict["html"]
        soup = BeautifulSoup(html, "html.parser")
        remove_junk(soup)
        namespace_classes(soup, self.namespace)
        clean_inline_styles(soup)

        repeating = section_dict.get("repeating_pattern", {})
        if repeating.get("detected") and repeating.get("count", 0) >= 2:
            child_tag = repeating["child_tag"]
            child_classes = repeating["child_classes"]
            container = None
            for el in soup.find_all(child_tag):
                if child_classes and set(child_classes).issubset(set(el.get("class", []))):
                    container = el.parent
                    break
            if container:
                block_type = slugify(section_dict.get("semantic_type") or "item")
                block_builder = LiquidBuilder(f"{self.namespace}-{block_type}", self.product_slug)
                first_child = container.find(child_tag)
                if first_child:
                    self._convert_element_recursive(first_child, block_builder)
                    block_html = str(first_child)
                    block_file = self._build_block_file(block_builder, block_type, block_html)
                    self.blocks_schemas[block_type] = block_file
                    for child in list(container.find_all(child_tag, recursive=False)):
                        child.decompose()
                    placeholder = f"{{% content_for 'blocks' %}}"
                    container.append(BeautifulSoup(placeholder, "html.parser"))

        self._convert_element_recursive(soup, self)
        return str(soup)

    def _convert_element_recursive(self, root, builder):
        if isinstance(root, Tag):
            children = list(root.children)
            for child in children:
                if isinstance(child, Tag):
                    if is_script_or_style(child):
                        child.decompose()
                        continue
                    if child.name == "img":
                        builder.convert_image(child)
                        continue
                    if child.name == "a" and child.get_text(strip=True):
                        is_button = bool(child.find_parent(lambda t: t.name == "button")) or any(
                            "btn" in c or "button" in c or "cta" in c for c in child.get("class", [])
                        )
                        if is_button or child.find(["img"]) is None:
                            builder.convert_link(child)
                            continue
                    text_children = [c for c in child.children if isinstance(c, NavigableString) and c.strip()]
                    tag_children = [c for c in child.children if isinstance(c, Tag)]
                    if child.name in TEXT_TAGS and text_children and not tag_children:
                        label = f"{child.name}_{slugify(child.get_text(strip=True)[:30])}"
                        builder.convert_text_node(child, label)
                        continue
                    builder._convert_element_recursive(child, builder)

    def _build_block_file(self, block_builder, block_type, block_html):
        schema = {
            "name": f"{self.product_slug}-{block_type} item",
            "settings": block_builder.settings,
        }
        content = (
            f"<div class=\"{self.namespace}-{block_type}\">\n"
            f"{block_html}\n"
            f"</div>\n\n"
            f"{{% stylesheet %}}\n"
            f".{self.namespace}-{block_type} {{ /* block-scoped styles */ }}\n"
            f"{{% endstylesheet %}}\n\n"
            f"{{% schema %}}\n"
            f"{json.dumps(schema, indent=2)}\n"
            f"{{% endschema %}}\n"
        )
        return content

    def build_section_file(self, markup, section_name, section_tag_class, base_stylesheet=""):
        schema = {
            "name": section_name,
            "tag": "section",
            "class": section_tag_class,
            "settings": self.settings,
            "blocks": [{"type": t} for t in self.blocks_schemas.keys()],
            "presets": [{
                "name": section_name,
                "blocks": [{"type": t} for t in self.blocks_schemas.keys()],
            }],
        }
        return (
            f"{markup}\n\n"
            f"{{% stylesheet %}}\n"
            f"{base_stylesheet}\n"
            f".{self.namespace} {{ /* section-scoped styles */ }}\n"
            f"{{% endstylesheet %}}\n\n"
            f"{{% schema %}}\n"
            f"{json.dumps(schema, indent=2)}\n"
            f"{{% endschema %}}\n"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sections-json", required=True, help="Path to sections.json from analyzer")
    parser.add_argument("--section-index", type=int, required=True, help="1-based index of section to convert")
    parser.add_argument("--output", required=True, help="Path to output .liquid file")
    parser.add_argument("--blocks-dir", required=True, help="Directory where blocks/*.liquid files go")
    parser.add_argument("--namespace", required=True, help="CSS namespace (e.g. page-undone)")
    parser.add_argument("--product-slug", required=True, help="Product slug (e.g. undone)")
    args = parser.parse_args()

    sections_json = Path(args.sections_json).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    blocks_dir = Path(args.blocks_dir).expanduser().resolve()

    if not sections_json.exists():
        print(f"ERRO: {sections_json} não encontrado", file=sys.stderr)
        sys.exit(1)

    data = json.loads(sections_json.read_text(encoding="utf-8"))
    sections = data.get("sections", [])
    if args.section_index < 1 or args.section_index > len(sections):
        print(f"ERRO: section-index {args.section_index} inválido (tem {len(sections)} seções)", file=sys.stderr)
        sys.exit(1)
    section = sections[args.section_index - 1]

    print(f"[liquid-converter] convertendo seção {args.section_index}: {section.get('semantic_type')}")

    builder = LiquidBuilder(args.namespace, args.product_slug)
    converted_markup = builder.process(section)

    section_name = f"Page {args.product_slug} — {section.get('semantic_type', 'section')}"
    section_tag_class = f"{args.namespace} {args.namespace}--{slugify(section.get('semantic_type', 'section'))}"
    file_content = builder.build_section_file(converted_markup, section_name, section_tag_class)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(file_content, encoding="utf-8")
    print(f"[liquid-converter] section salva em {output_path}")

    if builder.blocks_schemas:
        blocks_dir.mkdir(parents=True, exist_ok=True)
        for block_type, block_content in builder.blocks_schemas.items():
            block_file = blocks_dir / f"{args.namespace}-{block_type}.liquid"
            block_file.write_text(block_content, encoding="utf-8")
            print(f"[liquid-converter] block salvo em {block_file}")

    print("[liquid-converter] ATENÇÃO: valide o arquivo gerado com a skill `shopify-plugin:shopify-liquid` antes de instalar no tema. Este script não substitui a validação — ele gera o Liquid, mas edge cases podem precisar ajuste manual.")


if __name__ == "__main__":
    main()
