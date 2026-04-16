#!/usr/bin/env python3
"""
liquid-converter.py — Aura Engine design-clone pipeline (step 3 of 3) · v2

Recebe uma seção (HTML+CSS) identificada pelo analyzer.py e converte em Shopify
Liquid section editável via theme editor. Substitui textos fixos por
{{ section.settings.* }}, imagens por image_picker settings, cores por CSS
custom properties, e padrões repetíveis por blocks separados.

v2 melhorias:
- Strip de artefatos Shopify: <link> tags CDN, web components (product-info,
  media-gallery, use-animate, etc), data-* attributes específicos do tema
- Detecção de blocks corrigida (acontecia ANTES do namespace, agora corretamente)
- Dedup de settings quando texto default é idêntico
- Naming semântico (heading_1, paragraph_2, button_label_3) ao invés de slugs
  baseados em texto completo
- SVGs grandes substituídos por placeholder
- Remoção de scripts, noscript, iframe, style tags externos

Uso (Modo C — HTML fresh do frontend-design, padrão da skill 06):
    python3 liquid-converter.py \\
        --html /tmp/fresh-<produto>/<tipo>.html \\
        --css /tmp/fresh-<produto>/<tipo>.css \\
        --type hero \\
        --output <path.liquid> \\
        --blocks-dir <path> \\
        --namespace page-<produto>-<tipo> \\
        --product-slug <produto>

Uso (Modo B legacy — clone direto do HTML do concorrente via sections.json):
    python3 liquid-converter.py \\
        --sections-json <path> \\
        --section-index <N> \\
        --output <path.liquid> \\
        --blocks-dir <path> \\
        --namespace page-<produto> \\
        --product-slug <produto>

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
TEXT_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "span", "a", "button", "li",
    "blockquote", "em", "strong", "small", "label",
    "dt", "dd", "summary", "figcaption", "cite",
}
# Inline tags aceitas dentro de texto misto — convertido como inline_richtext
INLINE_TAGS = {"em", "strong", "span", "i", "b", "small", "br", "sup", "sub", "mark", "u"}
LONG_TEXT_THRESHOLD = 80  # chars — acima disso usa richtext

# Rótulos semânticos de fallback por tag quando a classe não dá pista
TAG_LABEL_FALLBACK = {
    "h1": "Heading", "h2": "Heading", "h3": "Subheading",
    "h4": "Subheading", "h5": "Label", "h6": "Label",
    "p": "Paragraph",
    "a": "Link", "button": "Button",
    "li": "List item",
    "span": "Text", "strong": "Emphasis", "em": "Emphasis",
    "dt": "Label", "dd": "Value",
    "summary": "Summary", "figcaption": "Caption",
    "cite": "Citation",
    "small": "Note", "label": "Label",
}

# Web components Shopify/Dawn/Horizon a desembrulhar (preserva filhos, remove wrapper)
SHOPIFY_CUSTOM_ELEMENTS = {
    "product-info", "product-form", "product-gallery", "product-modal",
    "product-recently-viewed", "media-gallery", "modal-opener", "modal-dialog",
    "slider-component", "slideshow-component", "variant-selects", "variant-radios",
    "deferred-media", "cart-notification", "cart-drawer", "cart-remove-button",
    "quantity-input", "quick-order-list", "pickup-availability", "pickup-availability-drawer",
    "price-per-item", "bulk-add", "show-more-button", "use-animate", "gift-card-recipient",
    "predictive-search", "search-form", "menu-drawer", "header-drawer",
    "localization-form", "store-availability", "recipient-form",
    "share-button", "details-disclosure", "details-modal",
}

# Data attributes Shopify-específicos a remover
SHOPIFY_DATA_ATTRS = re.compile(
    r"^data-(product-id|variant-id|section|section-id|section-type|update-url|url|"
    r"template|product-handle|shopify|aos|oke|yotpo|judgeme|intrinsic-width|"
    r"media-id|media-position|gallery-id|modal|zoom|animate|aria-controls|"
    r"target|handle|action|index)"
)

BUTTON_CLASS_PATTERN = re.compile(r"(btn|button|cta|add-to-cart|buy-now)", re.IGNORECASE)

MIN_TEXT_LENGTH = 2
INLINE_SVG_MAX_LENGTH = 500  # SVGs maiores viram placeholder


def slugify(text, max_len=40):
    s = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return s[:max_len] or "field"


HEX_COLOR_RE_VALIDATE = re.compile(r"^[0-9a-fA-F]{3,8}$")
CSS_CLASS_SELECTOR_RE = re.compile(r"\.([a-zA-Z_][\w-]*)")
CSS_ID_SELECTOR_RE = re.compile(r"#([a-zA-Z_][\w-]*)")
CSS_COLOR_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


def semantic_label_from_classes(el, tag_name, namespace=None):
    """Deriva rótulo humano a partir das classes BEM. Se `namespace` é passado (ex: 'page-[produto]-hero'),
    remove o prefixo e o segmento final duplicado pra um label limpo (ex: 'page-[produto]-hero__hero_pill' → 'Pill')."""
    classes = el.get("class", []) or []
    for cls in classes:
        rest = None
        if namespace and cls.startswith(namespace + "__"):
            rest = cls[len(namespace) + 2:]
            last_seg = namespace.split("-")[-1] if "-" in namespace else namespace
            if rest.startswith(last_seg + "_"):
                rest = rest[len(last_seg) + 1:]
            elif rest == last_seg:
                rest = ""
        elif "__" in cls:
            _, rest = cls.split("__", 1)
        if rest is not None:
            rest = rest.split("--")[0].replace("_", " ").replace("-", " ").strip()
            if rest:
                return rest[0].upper() + rest[1:]
    return TAG_LABEL_FALLBACK.get(tag_name, "Text")


def extract_colors_from_css(css):
    """Acha todos os hex únicos no CSS. Retorna dict {hex_normalized: setting_id}."""
    seen = []
    for m in CSS_COLOR_RE.finditer(css):
        c = m.group(0).lower()
        if len(c) == 4:
            c = "#" + "".join(ch * 2 for ch in c[1:])
        if c not in seen:
            seen.append(c)
    return {hx: f"color_{i + 1}" for i, hx in enumerate(seen)}


def replace_colors_with_vars(css, color_map):
    """Substitui hex codes em VALORES CSS (não selectors) por var(--color-N)."""
    if not color_map:
        return css
    def repl(m):
        c = m.group(0).lower()
        if len(c) == 4:
            c = "#" + "".join(ch * 2 for ch in c[1:])
        sid = color_map.get(c)
        return f"var(--{sid})" if sid else m.group(0)
    # split por blocks pra só processar dentro de { ... }
    out = []
    i = 0
    n = len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            out.append(css[i:])
            break
        out.append(css[i:brace + 1])
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            c = css[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            j += 1
        block_content = css[brace + 1:j - 1]
        out.append(CSS_COLOR_RE.sub(repl, block_content))
        out.append("}")
        i = j
    return "".join(out)


def rewrite_css_for_namespace(css, namespace):
    """Reescreve classes/IDs em selectors CSS pra casar com o namespace aplicado no HTML.
    Só mexe em selectors (antes do {), não em valores (pra não quebrar hex colors, content: "#foo")."""
    if not css or not namespace:
        return css

    def rewrite_selector_text(selector_text):
        def class_sub(m):
            return f".{namespace}__{slugify(m.group(1))}"

        def id_sub(m):
            ident = m.group(1)
            if HEX_COLOR_RE_VALIDATE.match(ident) and len(ident) in (3, 4, 6, 8):
                return m.group(0)
            return f"#{namespace}-{slugify(ident)}"

        result = CSS_CLASS_SELECTOR_RE.sub(class_sub, selector_text)
        result = CSS_ID_SELECTOR_RE.sub(id_sub, result)
        return result

    out = []
    i = 0
    n = len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            out.append(css[i:])
            break
        selector_part = css[i:brace]
        if selector_part.lstrip().startswith("@"):
            out.append(selector_part)
        else:
            out.append(rewrite_selector_text(selector_part))
        out.append("{")
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            c = css[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            j += 1
        block_content = css[brace + 1:j - 1]
        if selector_part.lstrip().startswith("@"):
            out.append(rewrite_css_for_namespace(block_content, namespace))
        else:
            out.append(block_content)
        out.append("}")
        i = j
    return "".join(out)


def looks_like_noise(text):
    """Texto muito curto, só símbolo, ou emoji isolado — não vira setting."""
    if not text:
        return True
    stripped = text.strip()
    if len(stripped) < MIN_TEXT_LENGTH:
        return True
    if len(stripped) < 4 and not any(c.isalnum() for c in stripped):
        return True
    return False


def strip_shopify_artifacts(soup):
    """Remove artefatos específicos de temas Shopify que não funcionam fora do contexto original."""
    # Remove <link> tags (CSS externo do CDN do concorrente)
    for tag in soup.find_all("link"):
        tag.decompose()

    # Remove <style> tags (CSS que pode referenciar assets externos)
    for tag in soup.find_all("style"):
        tag.decompose()

    # Remove scripts, noscript, iframe
    for tag in soup.find_all(["script", "noscript", "iframe"]):
        tag.decompose()

    # Desembrulha web components Shopify (mantém filhos, remove o wrapper customElement)
    for tag in soup.find_all(True):
        if tag.name and tag.name.lower() in SHOPIFY_CUSTOM_ELEMENTS:
            tag.unwrap()

    # Remove data-* attributes específicos de temas Shopify
    for tag in soup.find_all(True):
        if not isinstance(tag, Tag):
            continue
        attrs_to_remove = [a for a in list(tag.attrs.keys()) if SHOPIFY_DATA_ATTRS.match(a)]
        for a in attrs_to_remove:
            del tag[a]

    # Substitui SVGs grandes por placeholder (mantém ícones pequenos)
    for svg in soup.find_all("svg"):
        svg_str = str(svg)
        if len(svg_str) > INLINE_SVG_MAX_LENGTH:
            placeholder = soup.new_tag("span")
            placeholder["class"] = ["icon-placeholder"]
            svg.replace_with(placeholder)

    return soup


def namespace_classes(soup, namespace):
    """Substitui classes do concorrente por namespace próprio."""
    for el in soup.find_all(True):
        if el.has_attr("class"):
            mapped = []
            seen = set()
            for c in el["class"]:
                new_c = f"{namespace}__{slugify(c)}"
                if new_c not in seen:
                    mapped.append(new_c)
                    seen.add(new_c)
            el["class"] = mapped
        if el.has_attr("id"):
            el["id"] = f"{namespace}-{slugify(el['id'])}"


def clean_inline_styles(soup):
    """Remove url() de inline styles (assets externos do concorrente)."""
    for el in soup.find_all(style=True):
        style = el["style"]
        style = re.sub(r"url\((?!\{\{)[^)]*\)", "", style)
        style = re.sub(r";\s*;", ";", style).strip("; ").strip()
        if style:
            el["style"] = style
        else:
            del el["style"]


def derive_setting_label(el, namespace=None):
    tag = el.name if el else "text"
    if el is not None:
        label = semantic_label_from_classes(el, tag, namespace=namespace)
        if label and label not in TAG_LABEL_FALLBACK.values():
            return label
    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return "Heading"
    if tag == "button":
        return "Button label"
    if el and any(BUTTON_CLASS_PATTERN.search(c or "") for c in el.get("class", []) or []):
        return "Button label"
    return TAG_LABEL_FALLBACK.get(tag, "Text")


def derive_setting_id(el, counter):
    tag = el.name if el else "text"
    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return f"heading_{counter}"
    if tag == "button":
        return f"button_{counter}"
    if tag == "a":
        return f"link_{counter}"
    if tag == "p":
        return f"paragraph_{counter}"
    if tag == "li":
        return f"item_{counter}"
    if tag == "label":
        return f"form_label_{counter}"
    return f"text_{counter}"


class LiquidBuilder:
    def __init__(self, namespace, product_slug):
        self.namespace = namespace
        self.product_slug = product_slug
        self.settings = []
        self.settings_by_default = {}  # (s_type, default) -> setting_id (dedup)
        self.blocks_schemas = {}
        self.used_ids = set()
        self.counter = 0

    def unique_id(self, base):
        candidate = base
        i = 2
        while candidate in self.used_ids:
            candidate = f"{base}_{i}"
            i += 1
        self.used_ids.add(candidate)
        return candidate

    def add_setting(self, s_id, s_type, label, default=None, info=None):
        # Dedup: se mesmo texto já existe como setting do mesmo tipo, reutiliza ID
        if default and s_type in ("text", "richtext"):
            key = (s_type, default)
            if key in self.settings_by_default:
                return self.settings_by_default[key]

        entry = {"type": s_type, "id": s_id, "label": label}
        if default is not None:
            entry["default"] = default
        if info:
            entry["info"] = info
        self.settings.append(entry)

        if default and s_type in ("text", "richtext"):
            self.settings_by_default[(s_type, default)] = s_id
        return s_id

    def convert_text_node(self, el):
        text = el.get_text(strip=True)
        if looks_like_noise(text):
            return

        self.counter += 1
        s_type = "richtext" if (el.name == "p" and len(text) > LONG_TEXT_THRESHOLD) else "text"
        label = derive_setting_label(el, namespace=self.namespace)
        base_id = derive_setting_id(el, self.counter)
        s_id = self.unique_id(base_id)
        default = text if s_type == "text" else f"<p>{text}</p>"
        real_id = self.add_setting(s_id, s_type, label, default=default)

        new_tag = BeautifulSoup("", "html.parser").new_tag(el.name)
        new_tag.attrs = dict(el.attrs)
        placeholder = "{{ section.settings." + real_id + " }}"
        new_tag.append(BeautifulSoup(placeholder, "html.parser"))
        el.replace_with(new_tag)

    def convert_mixed_text_node(self, el):
        """Converte tag com texto misto + inline tags como inline_richtext (preserva <em>, <strong>, <br>, etc)."""
        if looks_like_noise(el.get_text(strip=True)):
            return

        # Sanitiza inner HTML: inline_richtext do Shopify só aceita tags simples sem attributes (a/em/strong/br/span/p/u)
        ALLOWED_INLINE = {"em", "strong", "br", "span", "a", "u", "p"}
        clone = BeautifulSoup(str(el), "html.parser").find(el.name)
        for t in clone.find_all(True):
            if t.name not in ALLOWED_INLINE:
                t.unwrap()
            else:
                t.attrs = {}
        inner_html = "".join(str(c) for c in clone.children).strip()

        self.counter += 1
        label = derive_setting_label(el, namespace=self.namespace)
        base_id = derive_setting_id(el, self.counter)
        s_id = self.unique_id(base_id)
        real_id = self.add_setting(s_id, "inline_richtext", label, default=inner_html)

        new_tag = BeautifulSoup("", "html.parser").new_tag(el.name)
        new_tag.attrs = dict(el.attrs)
        new_tag.append(BeautifulSoup("{{ section.settings." + real_id + " }}", "html.parser"))
        el.replace_with(new_tag)

    def convert_image(self, el):
        self.counter += 1
        alt = el.get("alt") or f"image_{self.counter}"
        original_classes = el.get("class", []) or []
        class_attr = " ".join(original_classes) if original_classes else ""

        image_id = self.unique_id(f"image_{self.counter}")
        ratio_id = self.unique_id(f"{image_id}_ratio")
        fit_id = self.unique_id(f"{image_id}_fit")

        label = semantic_label_from_classes(el, "img", namespace=self.namespace)
        if label == "Text":
            label = f"Image: {alt[:40]}"

        self.settings.append({"type": "header", "content": label})
        self.add_setting(image_id, "image_picker", "File")
        self.settings.append({
            "type": "select",
            "id": ratio_id,
            "label": "Aspect ratio",
            "options": [
                {"value": "adapt", "label": "Adaptive (fit the image)"},
                {"value": "1 / 1", "label": "Square (1:1)"},
                {"value": "4 / 5", "label": "Portrait (4:5)"},
                {"value": "3 / 4", "label": "Portrait (3:4)"},
                {"value": "16 / 9", "label": "Landscape (16:9)"},
                {"value": "3 / 2", "label": "Landscape (3:2)"},
            ],
            "default": "adapt",
        })
        self.settings.append({
            "type": "select",
            "id": fit_id,
            "label": "Image fit",
            "options": [
                {"value": "cover", "label": "Cover (crop to fill)"},
                {"value": "contain", "label": "Contain (fit inside, no crop)"},
            ],
            "default": "cover",
        })

        class_str = f"{class_attr} {self.namespace}__responsive_image".strip()
        liquid = (
            '<div class="' + self.namespace + '__image_wrap"'
            ' data-adapt="{% if section.settings.' + ratio_id + ' == \'adapt\' %}true{% else %}false{% endif %}"'
            ' style="{% if section.settings.' + ratio_id + ' != \'adapt\' %}aspect-ratio: {{ section.settings.' + ratio_id + ' }};{% endif %} --img-fit: {{ section.settings.' + fit_id + ' }}">'
            '{% if section.settings.' + image_id + ' %}'
            '{{ section.settings.' + image_id + " | image_url: width: 1600 | image_tag: loading: 'lazy', widths: '400, 800, 1200, 1600', sizes: '(min-width: 900px) 50vw, 100vw', class: '" + class_str + "' }}"
            '{% endif %}'
            '</div>'
        )
        el.replace_with(BeautifulSoup(liquid, "html.parser"))

    def convert_link(self, el):
        text = el.get_text(strip=True)
        href = el.get("href") or ""
        self.counter += 1
        label_id = self.unique_id(f"link_label_{self.counter}")
        url_id = self.unique_id(f"link_url_{self.counter}")
        self.add_setting(label_id, "text", "Link label", default=text or "Click here")
        # Shopify url settings only accept absolute URLs or paths starting with "/". Anchors/relative fail push validation. Omit default when invalid.
        url_default = href if href.startswith(("http://", "https://", "/")) else None
        self.add_setting(url_id, "url", "Link URL", default=url_default)
        new_a = BeautifulSoup("", "html.parser").new_tag("a")
        new_a["href"] = "{{ section.settings." + url_id + " }}"
        if el.has_attr("class"):
            new_a["class"] = el["class"]
        new_a.append(BeautifulSoup("{{ section.settings." + label_id + " }}", "html.parser"))
        el.replace_with(new_a)

    def process(self, section_dict):
        html = section_dict["html"]
        soup = BeautifulSoup(html, "html.parser")

        # Step 1: limpa artefatos Shopify ANTES do namespacing (pra classes/tags originais ainda existirem)
        strip_shopify_artifacts(soup)

        # Step 2: extrai block template SE houver padrão repetitivo (usa classes originais pré-namespace)
        repeating = section_dict.get("repeating_pattern", {})
        if repeating.get("detected") and repeating.get("count", 0) >= 2:
            self._extract_block_from_repeating(soup, repeating, section_dict.get("semantic_type", "item"))

        # Step 3: namespace classes (após extrair blocks)
        namespace_classes(soup, self.namespace)
        clean_inline_styles(soup)

        # Step 4: converte texto, imagens, links
        self._convert_element_recursive(soup, self)

        return str(soup)

    def _extract_block_from_repeating(self, soup, repeating, semantic_hint):
        """Encontra o primeiro elemento do padrão repetitivo e usa como template de block."""
        child_tag = repeating.get("child_tag")
        child_classes = set(repeating.get("child_classes") or [])

        first_match = None
        container = None
        for el in soup.find_all(child_tag):
            el_classes = set(el.get("class", []) or [])
            if child_classes and child_classes.issubset(el_classes):
                first_match = el
                container = el.parent
                break

        # Fallback: se não achou por classes, usa o primeiro child_tag dentro do container mais provável
        if first_match is None:
            for potential_container in soup.find_all(True):
                kids = [k for k in potential_container.find_all(child_tag, recursive=False)]
                if len(kids) >= 2:
                    first_match = kids[0]
                    container = potential_container
                    break

        if first_match is None or container is None:
            return

        block_type = slugify(semantic_hint) or "item"

        # Constrói o block a partir do primeiro match (HTML copiado antes do namespacing)
        block_html = str(first_match)
        block_soup = BeautifulSoup(block_html, "html.parser")
        strip_shopify_artifacts(block_soup)
        namespace_classes(block_soup, f"{self.namespace}-{block_type}")
        clean_inline_styles(block_soup)

        block_builder = LiquidBuilder(f"{self.namespace}-{block_type}", self.product_slug)
        block_builder._convert_element_recursive(block_soup, block_builder)
        block_markup = str(block_soup)

        self.blocks_schemas[block_type] = {
            "markup": block_markup,
            "settings": block_builder.settings,
        }

        # Substitui todos os filhos repetidos no container principal por {% content_for 'blocks' %}
        siblings_to_remove = list(container.find_all(child_tag, recursive=False))
        for s in siblings_to_remove:
            s.decompose()
        container.append(BeautifulSoup("{% content_for 'blocks' %}", "html.parser"))

    def _convert_element_recursive(self, root, builder):
        if not isinstance(root, Tag):
            return
        children = list(root.children)
        for child in children:
            if not isinstance(child, Tag):
                continue
            if child.name in ("script", "style", "noscript", "iframe", "link"):
                child.decompose()
                continue
            if child.name == "img":
                builder.convert_image(child)
                continue
            if child.name == "a" and child.get_text(strip=True):
                has_only_text = all(
                    isinstance(c, NavigableString) or c.name == "span"
                    for c in child.children
                )
                if has_only_text:
                    builder.convert_link(child)
                    continue
            text_children = [c for c in child.children if isinstance(c, NavigableString) and c.strip()]
            tag_children = [c for c in child.children if isinstance(c, Tag)]
            if child.name in TEXT_TAGS and text_children and not tag_children:
                builder.convert_text_node(child)
                continue
            if child.name in TEXT_TAGS and text_children and tag_children and all(c.name in INLINE_TAGS for c in tag_children):
                builder.convert_mixed_text_node(child)
                continue
            builder._convert_element_recursive(child, builder)

    def build_block_file(self, block_type, block_data):
        schema = {
            "name": f"{self.product_slug}-{block_type} item",
            "settings": block_data["settings"],
        }
        content = (
            f"<div class=\"{self.namespace}-{block_type}\">\n"
            f"{block_data['markup']}\n"
            f"</div>\n\n"
            f"{{% stylesheet %}}\n"
            f".{self.namespace}-{block_type} {{ /* block-scoped styles */ }}\n"
            f"{{% endstylesheet %}}\n\n"
            f"{{% schema %}}\n"
            f"{json.dumps(schema, indent=2)}\n"
            f"{{% endschema %}}\n"
        )
        return content

    def build_section_file(self, markup, section_name, section_tag_class, base_stylesheet="", asset_type="section"):
        scope = "block" if asset_type == "block" else "section"

        # Extrai cores do CSS e transforma em settings + vars
        color_map = extract_colors_from_css(base_stylesheet)
        if color_map:
            base_stylesheet = replace_colors_with_vars(base_stylesheet, color_map)
            color_settings = [{"type": "header", "content": "Colors"}]
            for hex_color, s_id in color_map.items():
                color_settings.append({
                    "type": "color",
                    "id": s_id,
                    "label": f"Color {s_id.split('_')[1]}",
                    "default": hex_color,
                })
            self.settings = color_settings + self.settings
            inline_vars = "; ".join(
                f"--{s_id}: {{{{ {scope}.settings.{s_id} }}}}"
                for s_id in color_map.values()
            )
            if "<section" in markup[:200]:
                extra = f' {{{{ block.shopify_attributes }}}}' if asset_type == "block" else ""
                markup = re.sub(
                    r"(<section[^>]*?)(>)",
                    lambda m: f'{m.group(1)} style="{inline_vars}"{extra}{m.group(2)}',
                    markup,
                    count=1,
                )

        # Reescreve toda referência section.settings → block.settings se asset_type=block
        if asset_type == "block":
            markup = markup.replace("section.settings.", "block.settings.")
            # Adiciona shopify_attributes no primeiro elemento se não tiver <section>
            if "{{ block.shopify_attributes }}" not in markup:
                markup = re.sub(
                    r"(<(?:section|div|article|aside)[^>]*?)(>)",
                    r"\1 {{ block.shopify_attributes }}\2",
                    markup,
                    count=1,
                )

        block_types = list(self.blocks_schemas.keys())
        if asset_type == "block":
            schema = {
                "name": section_name,
                "tag": None,
                "settings": self.settings,
                "presets": [{"name": section_name}],
            }
        else:
            schema = {
                "name": section_name,
                "tag": "section",
                "class": section_tag_class,
                "settings": self.settings,
                "blocks": [{"type": t} for t in block_types],
                "presets": [{
                    "name": section_name,
                    "blocks": ([{"type": t} for t in block_types] * 3) if block_types else [],
                }],
            }

        image_helpers = (
            f".{self.namespace}__image_wrap {{ position: relative; width: 100%; overflow: hidden; }}\n"
            f".{self.namespace}__image_wrap img, .{self.namespace}__image_wrap .{self.namespace}__responsive_image {{ width: 100%; display: block; }}\n"
            f".{self.namespace}__image_wrap[data-adapt='true'] img, .{self.namespace}__image_wrap[data-adapt='true'] .{self.namespace}__responsive_image {{ height: auto; object-fit: initial; }}\n"
            f".{self.namespace}__image_wrap:not([data-adapt='true']) img, .{self.namespace}__image_wrap:not([data-adapt='true']) .{self.namespace}__responsive_image {{ height: 100%; object-fit: var(--img-fit, cover); }}\n"
        )
        doc_header = ""
        if asset_type == "block":
            doc_header = (
                f"{{% doc %}}\n"
                f"  Renders the {section_name} block.\n"
                f"  @example\n"
                f"  {{% content_for 'block', type: '{self.namespace}', id: 'example' %}}\n"
                f"{{% enddoc %}}\n\n"
            )
        return (
            f"{doc_header}"
            f"{markup}\n\n"
            f"{{% stylesheet %}}\n"
            f"{base_stylesheet}\n"
            f"{image_helpers}"
            f".{self.namespace} {{ /* {scope}-scoped styles */ }}\n"
            f".{self.namespace}__icon_placeholder {{ display: inline-block; width: 1em; height: 1em; background: currentColor; opacity: 0.2; border-radius: 2px; }}\n"
            f"{{% endstylesheet %}}\n\n"
            f"{{% schema %}}\n"
            f"{json.dumps(schema, indent=2)}\n"
            f"{{% endschema %}}\n"
        )


def main():
    parser = argparse.ArgumentParser()
    # Dois modos de input: sections.json (legacy, do analyzer) ou HTML/CSS fresh (Modo C)
    parser.add_argument("--sections-json", help="(Modo B legacy) Path to sections.json from analyzer")
    parser.add_argument("--section-index", type=int, help="(Modo B legacy) 1-based index of section to convert")
    parser.add_argument("--html", help="(Modo C) Path to fresh HTML file from frontend-design")
    parser.add_argument("--css", help="(Modo C) Path to fresh CSS file (injected into {% stylesheet %})")
    parser.add_argument("--type", help="(Modo C) Semantic type of the section (hero/features/faq/etc)")
    parser.add_argument("--output", required=True, help="Path to output .liquid file")
    parser.add_argument("--blocks-dir", required=True, help="Directory where blocks/*.liquid files go")
    parser.add_argument("--namespace", required=True, help="CSS namespace (e.g. page-[produto]-hero)")
    parser.add_argument("--product-slug", required=True, help="Product slug (e.g. [produto])")
    parser.add_argument("--asset-type", choices=["section", "block"], default="section",
                        help="Output as Shopify section (default) or theme block (for Horizon-style composability)")
    args = parser.parse_args()

    output_path = Path(args.output).expanduser().resolve()
    blocks_dir = Path(args.blocks_dir).expanduser().resolve()

    # Decide modo pelo input fornecido
    if args.html:
        # Modo C — HTML fresh do frontend-design
        html_path = Path(args.html).expanduser().resolve()
        if not html_path.exists():
            print(f"ERRO: {html_path} não encontrado", file=sys.stderr)
            sys.exit(1)
        html_content = html_path.read_text(encoding="utf-8")
        base_css = ""
        if args.css:
            css_path = Path(args.css).expanduser().resolve()
            if css_path.exists():
                base_css = rewrite_css_for_namespace(css_path.read_text(encoding="utf-8"), args.namespace)
        section = {
            "html": html_content,
            "semantic_type": args.type or "section",
            "repeating_pattern": {"detected": False, "count": 0},
            "images": [],
        }
        print(f"[liquid-converter v2] Modo C — convertendo HTML fresh ({args.type or 'section'})")
    elif args.sections_json and args.section_index:
        # Modo B legacy — sections.json do analyzer
        sections_json = Path(args.sections_json).expanduser().resolve()
        if not sections_json.exists():
            print(f"ERRO: {sections_json} não encontrado", file=sys.stderr)
            sys.exit(1)
        data = json.loads(sections_json.read_text(encoding="utf-8"))
        sections = data.get("sections", [])
        if args.section_index < 1 or args.section_index > len(sections):
            print(f"ERRO: section-index {args.section_index} inválido (tem {len(sections)} seções)", file=sys.stderr)
            sys.exit(1)
        section = sections[args.section_index - 1]
        base_css = ""
        print(f"[liquid-converter v2] Modo B — convertendo seção {args.section_index}: {section.get('semantic_type')}")
    else:
        print("ERRO: forneça --html (Modo C) ou --sections-json + --section-index (Modo B legacy)", file=sys.stderr)
        sys.exit(1)

    builder = LiquidBuilder(args.namespace, args.product_slug)
    converted_markup = builder.process(section)

    section_name = f"Page {args.product_slug} — {section.get('semantic_type', 'section')}"
    section_tag_class = f"{args.namespace} {args.namespace}--{slugify(section.get('semantic_type', 'section'))}"
    file_content = builder.build_section_file(converted_markup, section_name, section_tag_class, base_stylesheet=base_css, asset_type=args.asset_type)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(file_content, encoding="utf-8")

    print(f"[liquid-converter v2] section salva em {output_path}")
    print(f"[liquid-converter v2] stats: {len(builder.settings)} settings · {len(builder.blocks_schemas)} block type(s)")

    if builder.blocks_schemas:
        blocks_dir.mkdir(parents=True, exist_ok=True)
        for block_type, block_data in builder.blocks_schemas.items():
            block_content = builder.build_block_file(block_type, block_data)
            block_file = blocks_dir / f"{args.namespace}-{block_type}.liquid"
            block_file.write_text(block_content, encoding="utf-8")
            print(f"[liquid-converter v2] block salvo em {block_file}")

    print("[liquid-converter v2] ATENÇÃO: sempre valide o arquivo gerado com a skill `shopify-plugin:shopify-liquid` antes de instalar no tema. Edge cases podem precisar ajuste manual.")


if __name__ == "__main__":
    main()
