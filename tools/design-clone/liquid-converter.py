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
import html as html_lib
import json
import logging
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
except ImportError:
    print("ERRO: BeautifulSoup4 não instalado. Rode: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

# Import consolidado do módulo compartilhado (evita duplicação com preview.py)
try:
    from _css_utils import rewrite_css_for_namespace
except ImportError:
    # Fallback: quando script é invocado de outro cwd, garante o import
    _THIS_DIR = Path(__file__).resolve().parent
    if str(_THIS_DIR) not in sys.path:
        sys.path.insert(0, str(_THIS_DIR))
    from _css_utils import rewrite_css_for_namespace  # noqa: E402

logger = logging.getLogger("design_clone.liquid_converter")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


VALID_SCHEMA_TYPES = {
    "text", "inline_richtext", "richtext", "image_picker", "color", "range",
    "select", "checkbox", "number", "url", "textarea", "header", "paragraph",
    "color_background", "font_picker", "html", "link_list", "liquid",
    "radio", "video", "video_url", "article", "blog", "collection",
    "collection_list", "page", "product", "product_list",
}
SCHEMA_TYPES_WITHOUT_LABEL = {"header", "paragraph"}


def escape_liquid_default(text: str) -> str:
    """Escapa texto pra uso seguro como `default` no schema Shopify.

    - HTML-escape (`<`, `>`, `&`, `"`, `'`) evita XSS ao renderizar.
    - Escapa `{{` / `}}` pra não quebrar parsing Liquid downstream.
    """
    if text is None:
        return ""
    escaped = html_lib.escape(str(text), quote=True)
    escaped = escaped.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")
    escaped = escaped.replace("{%", "&#123;&#37;").replace("%}", "&#37;&#125;")
    return escaped


def validate_shopify_schema(schema: dict) -> list[str]:
    """Valida schema Shopify e retorna lista de erros (vazia = ok)."""
    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["schema deve ser dict"]

    def _check_settings(settings, scope_label: str) -> None:
        if not isinstance(settings, list):
            errors.append(f"{scope_label}: settings deve ser list")
            return
        ids_seen: set[str] = set()
        for idx, setting in enumerate(settings):
            if not isinstance(setting, dict):
                errors.append(f"{scope_label}[{idx}]: entrada deve ser dict")
                continue
            s_type = setting.get("type")
            if not s_type:
                errors.append(f"{scope_label}[{idx}]: campo 'type' obrigatório")
                continue
            if s_type not in VALID_SCHEMA_TYPES:
                errors.append(
                    f"{scope_label}[{idx}]: type {s_type!r} inválido (válidos: {sorted(VALID_SCHEMA_TYPES)})"
                )
            if s_type not in SCHEMA_TYPES_WITHOUT_LABEL:
                if not setting.get("label"):
                    errors.append(f"{scope_label}[{idx}]: label obrigatório para type {s_type!r}")
                sid = setting.get("id")
                if not sid:
                    errors.append(f"{scope_label}[{idx}]: id obrigatório para type {s_type!r}")
                elif sid in ids_seen:
                    errors.append(f"{scope_label}[{idx}]: id duplicado {sid!r}")
                else:
                    ids_seen.add(sid)

    _check_settings(schema.get("settings", []), "settings")
    for block in schema.get("blocks", []) or []:
        if isinstance(block, dict) and "settings" in block:
            _check_settings(block.get("settings", []), f"block[{block.get('type', '?')}].settings")
    return errors


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

# GAP-C: CTA de pricing/offer → form nativo /cart/add. Detecta por classe OU por texto.
CART_CTA_CLASS_PATTERN = re.compile(r"(add-to-cart|add_to_cart|buy-now|buy_now|checkout|cart-add)", re.IGNORECASE)
CART_CTA_TEXT_PATTERN = re.compile(
    r"\b(add to cart|buy now|get yours|order now|checkout|claim|get it now|shop now|buy it now|add to bag)\b",
    re.IGNORECASE,
)

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


# ── GAP-D: tokens de design (shadow/radius/font-size/font-family) → var + setting ──
# Cada token vira (regex de valor, prefixo de setting id, schema type, label, info opcional).
# A migração varre o CSS, coleta valores hardcoded e os substitui por var(--<id>),
# emitindo um setting editável por valor único (everything-editable).
CSS_DECL_BOX_SHADOW_RE = re.compile(r"box-shadow\s*:\s*([^;{}]+?)\s*(?=;|})", re.IGNORECASE)
CSS_DECL_RADIUS_RE = re.compile(r"border-radius\s*:\s*([^;{}]+?)\s*(?=;|})", re.IGNORECASE)
CSS_DECL_FONT_SIZE_RE = re.compile(r"font-size\s*:\s*([^;{}]+?)\s*(?=;|})", re.IGNORECASE)
CSS_DECL_FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;{}]+?)\s*(?=;|})", re.IGNORECASE)


def _normalize_token_value(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def extract_tokens_from_css(css):
    """Coleta valores únicos de box-shadow / border-radius / font-size / font-family hardcoded.

    Retorna lista de dicts {id, type, label, default, info, var}. Já-existentes em var(--x)
    são ignorados (não re-tokeniza). Ordem estável (ordem de aparição no CSS)."""
    specs = [
        (CSS_DECL_BOX_SHADOW_RE, "shadow", "text", "Shadow", "CSS box-shadow value"),
        (CSS_DECL_RADIUS_RE, "radius", "text", "Corner radius", "CSS border-radius value"),
        (CSS_DECL_FONT_SIZE_RE, "font_size", "text", "Font size", "CSS font-size value"),
        (CSS_DECL_FONT_FAMILY_RE, "font_family", "text", "Font family", "CSS font-family stack"),
    ]
    tokens = []
    seen = set()
    for regex, prefix, s_type, label, info in specs:
        idx = 0
        for m in regex.finditer(css):
            raw = _normalize_token_value(m.group(1))
            # Já é uma var() pura? Não tokeniza de novo.
            if not raw or raw.lower().startswith("var(") and raw.count("var(") == 1 and raw.endswith(")"):
                continue
            key = (prefix, raw.lower())
            if key in seen:
                continue
            seen.add(key)
            idx += 1
            s_id = f"{prefix}_{idx}"
            tokens.append({
                "id": s_id,
                "type": s_type,
                "label": f"{label} {idx}",
                "default": raw,
                "info": info,
                "var": f"--{s_id}",
            })
    return tokens


def replace_tokens_with_vars(css, tokens):
    """Substitui cada valor hardcoded de token por var(--<id>) em TODAS as ocorrências.

    Migração everything-editable: usages hardcoded no CSS passam a ler a custom property,
    que é injetada inline no root + exposta como setting."""
    if not tokens:
        return css
    prop_by_prefix = {
        "shadow": "box-shadow",
        "radius": "border-radius",
        "font_size": "font-size",
        "font_family": "font-family",
    }
    out = css
    for tok in tokens:
        prefix = tok["id"].rsplit("_", 1)[0]
        prop = prop_by_prefix.get(prefix)
        if not prop:
            continue
        raw = tok["default"]
        # Substitui `prop: <raw>` → `prop: var(--id)`, preservando o resto da declaração.
        pattern = re.compile(
            re.escape(prop) + r"(\s*:\s*)" + re.escape(raw) + r"(\s*(?=;|}))",
            re.IGNORECASE,
        )
        out = pattern.sub(lambda m, _v=tok["var"]: f"{prop}{m.group(1)}var({_v}){m.group(2)}", out)
    return out


# GAP-A: aplica `| escape` em TODA interpolação dentro de qualquer atributo style="".
# Sem isso, valores controlados por setting injetados inline não passam por escape e o
# theme editor não aplica de forma confiável (e abre vetor de injection no atributo).
_STYLE_ATTR_RE = re.compile(r'(style\s*=\s*")([^"]*)(")', re.IGNORECASE)
_LIQUID_OUTPUT_RE = re.compile(r"\{\{\s*(.*?)\s*\}\}")


def escape_style_interpolations(markup: str) -> str:
    """Garante `| escape` em todo `{{ ... }}` que aparece dentro de um atributo style="".

    Idempotente: não duplica `| escape` se já presente. Preserva expressões com outros
    filtros (ex: `{{ x | downcase }}` → `{{ x | downcase | escape }}`)."""
    def _fix_attr(attr_match: re.Match) -> str:
        body = attr_match.group(2)

        def _fix_output(out_match: re.Match) -> str:
            expr = out_match.group(1).strip()
            filters = [f.strip() for f in expr.split("|")]
            if "escape" in filters:
                return "{{ " + expr + " }}"
            return "{{ " + expr + " | escape }}"

        fixed_body = _LIQUID_OUTPUT_RE.sub(_fix_output, body)
        return attr_match.group(1) + fixed_body + attr_match.group(3)

    return _STYLE_ATTR_RE.sub(_fix_attr, markup)


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
        self.built_schema = None  # preenchido por build_section_file (GAP-B POPULATE)

    def unique_id(self, base):
        candidate = base
        i = 2
        while candidate in self.used_ids:
            candidate = f"{base}_{i}"
            i += 1
        self.used_ids.add(candidate)
        return candidate

    def add_setting(self, s_id, s_type, label, default=None, info=None):
        # XSS/Liquid-injection guard: escapa defaults textuais antes de persistir.
        safe_default = default
        if default is not None and s_type in ("text", "richtext", "inline_richtext", "textarea"):
            safe_default = escape_liquid_default(default)

        # Dedup: se mesmo texto já existe como setting do mesmo tipo, reutiliza ID
        if safe_default and s_type in ("text", "richtext", "inline_richtext"):
            key = (s_type, safe_default)
            if key in self.settings_by_default:
                return self.settings_by_default[key]

        entry = {"type": s_type, "id": s_id, "label": label}
        if safe_default is not None:
            entry["default"] = safe_default
        if info:
            entry["info"] = info
        self.settings.append(entry)

        if safe_default and s_type in ("text", "richtext", "inline_richtext"):
            self.settings_by_default[(s_type, safe_default)] = s_id
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

    def is_cart_cta(self, el):
        """GAP-C: True se o elemento é um CTA de compra (pricing/offer) que deve virar form /cart/add."""
        classes = el.get("class", []) or []
        if any(CART_CTA_CLASS_PATTERN.search(c or "") for c in classes):
            return True
        # Sinal mais forte: o próprio href aponta pro endpoint de cart add.
        href = el.get("href") or ""
        if "/cart/add" in href:
            return True
        text = el.get_text(strip=True)
        return bool(text and CART_CTA_TEXT_PATTERN.search(text))

    def convert_cart_cta(self, el):
        """GAP-C: converte um CTA de compra em <form action="/cart/add" method="post"> nativo.

        Settings: variant_id (line item id), quantity, after_add (cart/checkout/stay) e
        cta_fallback_url (usado quando variant_id está vazio — degrada pra link)."""
        text = el.get_text(strip=True) or "Add to cart"
        self.counter += 1
        n = self.counter
        label_id = self.unique_id(f"cta_label_{n}")
        variant_id = self.unique_id(f"variant_id_{n}")
        qty_id = self.unique_id(f"cta_quantity_{n}")
        after_id = self.unique_id(f"cta_after_add_{n}")
        fallback_id = self.unique_id(f"cta_fallback_url_{n}")

        self.add_setting(label_id, "text", "CTA label", default=text)
        self.settings.append({
            "type": "text", "id": variant_id, "label": "Variant ID",
            "info": "Shopify line-item/variant ID added to cart. Leave empty to use fallback link.",
        })
        self.settings.append({
            "type": "number", "id": qty_id, "label": "Quantity", "default": 1,
        })
        self.settings.append({
            "type": "select", "id": after_id, "label": "After add to cart",
            "options": [
                {"value": "cart", "label": "Go to cart"},
                {"value": "checkout", "label": "Go to checkout"},
                {"value": "stay", "label": "Stay on page"},
            ],
            "default": "checkout",
        })
        self.add_setting(fallback_id, "url", "CTA fallback URL",
                         info="Used when no Variant ID is set.")

        btn_class = " ".join(el.get("class", []) or [])
        s = "section.settings."
        liquid = (
            "{% if " + s + variant_id + " != blank %}"
            '<form action="/cart/add" method="post" enctype="multipart/form-data" class="' + btn_class + '">'
            '<input type="hidden" name="id" value="{{ ' + s + variant_id + ' | escape }}">'
            '<input type="hidden" name="quantity" value="{{ ' + s + qty_id + ' | escape }}">'
            "{% if " + s + after_id + " == 'checkout' %}"
            '<input type="hidden" name="checkout" value="1">'
            "{% endif %}"
            '<button type="submit" class="' + btn_class + '">{{ ' + s + label_id + " }}</button>"
            "</form>"
            "{% else %}"
            '<a href="{{ ' + s + fallback_id + " | default: '/cart' }}\" class=\"" + btn_class + "\">"
            "{{ " + s + label_id + " }}</a>"
            "{% endif %}"
        )
        el.replace_with(BeautifulSoup(liquid, "html.parser"))

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
            # GAP-C: CTA de compra (a/button) vira form /cart/add, antes da conversão normal de link.
            if child.name in ("a", "button") and child.get_text(strip=True) and builder.is_cart_cta(child):
                only_simple = all(
                    isinstance(c, NavigableString) or (isinstance(c, Tag) and c.name in ("span", "strong", "em"))
                    for c in child.children
                )
                if only_simple:
                    builder.convert_cart_cta(child)
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
        schema_errors = validate_shopify_schema(schema)
        if schema_errors:
            raise ValueError(
                "Schema inválido para block '"
                + str(block_type)
                + "': "
                + "; ".join(schema_errors)
            )
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

        # GAP-A + GAP-D: extrai cores E tokens (shadow/radius/font-size/font-family) do CSS,
        # transforma cada um em setting + custom property, e injeta TODAS as vars INLINE no root
        # da section (com | escape em cada interpolação). Sem inline-no-root, o theme editor não
        # aplica os valores; sem | escape, abre injection no atributo style.
        color_map = extract_colors_from_css(base_stylesheet)
        tokens = extract_tokens_from_css(base_stylesheet)
        prepend_settings = []
        inline_pairs = []  # (var_id_sem_hifen, setting_id) → vira "--id: {{ scope.settings.id | escape }}"

        if color_map:
            base_stylesheet = replace_colors_with_vars(base_stylesheet, color_map)
            prepend_settings.append({"type": "header", "content": "Colors"})
            for hex_color, s_id in color_map.items():
                prepend_settings.append({
                    "type": "color",
                    "id": s_id,
                    "label": f"Color {s_id.split('_')[1]}",
                    "default": hex_color,
                })
                inline_pairs.append(s_id)

        if tokens:
            base_stylesheet = replace_tokens_with_vars(base_stylesheet, tokens)
            prepend_settings.append({"type": "header", "content": "Design tokens"})
            for tok in tokens:
                entry = {"type": tok["type"], "id": tok["id"], "label": tok["label"], "default": tok["default"]}
                if tok.get("info"):
                    entry["info"] = tok["info"]
                prepend_settings.append(entry)
                inline_pairs.append(tok["id"])

        if prepend_settings:
            self.settings = prepend_settings + self.settings

        if inline_pairs:
            inline_vars = "; ".join(
                f"--{s_id}: {{{{ {scope}.settings.{s_id} | escape }}}}"
                for s_id in inline_pairs
            )
            extra = ' {{ block.shopify_attributes }}' if asset_type == "block" else ""
            # Injeta no PRIMEIRO elemento de abertura do markup (root da section), não só <section>.
            injected = re.subn(
                r"(<(?:section|div|article|aside|main)\b[^>]*?)(>)",
                lambda m: (
                    f'{m.group(1)} style="{inline_vars}"{extra}{m.group(2)}'
                    if "style=" not in m.group(1)
                    else f'{re.sub(chr(34) + r"$", "; " + inline_vars + chr(34), m.group(1), count=1)}{extra}{m.group(2)}'
                ),
                markup,
                count=1,
            )
            markup = injected[0]
            if injected[1] == 0:
                # Fallback: nenhum container encontrado → embrulha num wrapper com as vars.
                markup = f'<div class="{self.namespace}__root" style="{inline_vars}">{markup}</div>'

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

        # GAP-A (safety net): garante | escape em TODA interpolação dentro de qualquer style=""
        # do markup final (cobre styles vindos de convert_image, inline-vars e edge cases).
        markup = escape_style_interpolations(markup)

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

        schema_errors = validate_shopify_schema(schema)
        if schema_errors:
            raise ValueError(
                "Schema inválido para section: " + "; ".join(schema_errors)
            )

        # GAP-B: guarda o schema construído pra o POPULATE montar templates/page.json.
        self.built_schema = schema

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


def _settings_defaults(settings_list) -> dict:
    """Extrai {id: default} de uma lista de settings de schema (ignora header/paragraph)."""
    out = {}
    for s in settings_list or []:
        if not isinstance(s, dict):
            continue
        if s.get("type") in SCHEMA_TYPES_WITHOUT_LABEL:
            continue
        sid = s.get("id")
        if sid is not None and "default" in s:
            out[sid] = s["default"]
    return out


def build_template_section_node(builder, section_id, block_instances=3):
    """GAP-B: monta o node de UMA section pro templates/page.json a partir do schema construído.

    - settings: defaults reais da copy injetada (section-level).
    - blocks{} / block_order[]: uma instância por block type detectado, com defaults reais.
      Instâncias inseridas em ORDEM REVERSA (rule reverse-order-insertion) pra que o
      block_order final reflita a ordem visual correta no theme editor.
    """
    schema = builder.built_schema or {}
    node = {
        "type": section_id,
        "settings": _settings_defaults(schema.get("settings", [])),
    }

    block_types = list(builder.blocks_schemas.keys())
    if block_types:
        blocks = {}
        block_order = []
        # Insere em ordem reversa: monta a lista na ordem visual, depois popula reverso.
        instances = []
        for t in block_types:
            defaults = _settings_defaults(builder.blocks_schemas[t].get("settings", []))
            for n in range(block_instances):
                instances.append((f"{t}_{n + 1}", t, defaults))
        for inst_id, t, defaults in reversed(instances):
            blocks[inst_id] = {"type": t, "settings": dict(defaults)}
        block_order = [inst_id for inst_id, _, _ in instances]
        node["blocks"] = blocks
        node["block_order"] = block_order
    return node


def emit_template_json(path: Path, page_handle: str, section_nodes: list[tuple[str, dict]]):
    """GAP-B: escreve templates/page.[handle].json com sections{} + order[] populados.

    section_nodes: lista de (section_id, node) na ordem de exibição da página."""
    sections = {}
    order = []
    for section_id, node in section_nodes:
        sections[section_id] = node
        order.append(section_id)
    template = {"sections": sections, "order": order}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(template, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return template


def _convert_one_section(section, namespace, product_slug, output_path, blocks_dir, asset_type, semantic_type):
    """Converte uma única section (dict) → escreve .liquid + blocks, retorna (builder, section_id)."""
    builder = LiquidBuilder(namespace, product_slug)
    converted_markup = builder.process(section)

    section_name = f"Page {product_slug} — {semantic_type}"
    section_tag_class = f"{namespace} {namespace}--{slugify(semantic_type)}"
    file_content = builder.build_section_file(
        converted_markup, section_name, section_tag_class,
        base_stylesheet=section.get("_base_css", ""), asset_type=asset_type,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(file_content, encoding="utf-8")
    print(f"[liquid-converter v2] section salva em {output_path}")
    print(f"[liquid-converter v2] stats: {len(builder.settings)} settings · {len(builder.blocks_schemas)} block type(s)")

    if builder.blocks_schemas:
        blocks_dir.mkdir(parents=True, exist_ok=True)
        for block_type, block_data in builder.blocks_schemas.items():
            block_content = builder.build_block_file(block_type, block_data)
            block_file = blocks_dir / f"{namespace}-{block_type}.liquid"
            block_file.write_text(block_content, encoding="utf-8")
            print(f"[liquid-converter v2] block salvo em {block_file}")

    # section_id = nome do arquivo .liquid sem extensão (= o que vai em sections{}/order[])
    section_id = output_path.stem
    return builder, section_id


def detect_repeating_pattern(html_content):
    """Modo C: detecta o maior grupo de irmãos repetidos (cards/tiers/items) numa section, pra
    extrair como block. Sem isso, conteúdo repetível (benefit cards, pricing tiers, faq items,
    reviews) viraria tudo settings e a página não ficaria "separada por blocos".

    Retorna {detected, count, child_tag, child_classes} — o shape que _extract_block_from_repeating
    consome. Heurística: dentro de cada container, agrupa filhos DIRETOS por (tag, conjunto de
    classes); o maior grupo com >=2 irmãos que tenham texto é o padrão repetível dominante."""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception:  # noqa: BLE001 — entrada malformada não deve derrubar o conversor
        return {"detected": False, "count": 0}
    best = {"detected": False, "count": 0}
    SKIP = {None, "script", "style", "br", "hr", "source", "link", "meta"}
    for container in soup.find_all(True):
        groups = {}
        for child in container.find_all(recursive=False):
            if child.name in SKIP:
                continue
            key = (child.name, frozenset(child.get("class", []) or []))
            groups.setdefault(key, []).append(child)
        for (tag, classes), kids in groups.items():
            if len(kids) >= 2 and len(kids) > best["count"] and any(k.get_text(strip=True) for k in kids):
                best = {
                    "detected": True,
                    "count": len(kids),
                    "child_tag": tag,
                    "child_classes": list(classes),
                }
    return best


def run_batch(args):
    """GAP-E: converte a PÁGINA INTEIRA (loop por section) numa invocação e já chama o POPULATE.

    Manifest JSON (--batch <path>):
    {
      "product_slug": "produto",
      "page_handle": "produto",
      "asset_type": "section",
      "sections": [
        {"html": "...|path", "css": "...|path", "type": "hero", "namespace": "page-produto-hero",
         "output": "<staging>/sections/page-produto-hero.liquid", "blocks_dir": "<staging>/blocks"}
      ]
    }
    html/css aceitam tanto conteúdo inline quanto path (resolve path se o arquivo existir).
    """
    manifest_path = Path(args.batch).expanduser().resolve()
    if not manifest_path.exists():
        print(f"ERRO: batch manifest {manifest_path} não encontrado", file=sys.stderr)
        sys.exit(1)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERRO: JSON inválido em {manifest_path}: {exc.msg}", file=sys.stderr)
        sys.exit(1)

    product_slug = manifest.get("product_slug") or args.product_slug
    page_handle = manifest.get("page_handle") or args.page_handle or product_slug
    asset_type = manifest.get("asset_type", "section")
    section_specs = manifest.get("sections", [])
    if not product_slug:
        print("ERRO: batch manifest precisa de 'product_slug'", file=sys.stderr)
        sys.exit(1)
    if not section_specs:
        print("ERRO: batch manifest sem 'sections'", file=sys.stderr)
        sys.exit(1)

    def _resolve(val):
        """Aceita conteúdo inline OU path. Se for path existente, lê o arquivo."""
        if not val:
            return ""
        p = Path(str(val)).expanduser()
        if len(str(val)) < 4096 and p.exists() and p.is_file():
            return p.read_text(encoding="utf-8")
        return val

    section_nodes = []
    for spec in section_specs:
        namespace = spec["namespace"]
        semantic_type = spec.get("type", "section")
        html_content = _resolve(spec.get("html"))
        css_raw = _resolve(spec.get("css"))
        base_css = rewrite_css_for_namespace(css_raw, namespace) if css_raw else ""
        output_path = Path(spec["output"]).expanduser().resolve()
        blocks_dir = Path(spec.get("blocks_dir", output_path.parent.parent / "blocks")).expanduser().resolve()
        section = {
            "html": html_content,
            "semantic_type": semantic_type,
            "repeating_pattern": spec.get("repeating_pattern") or detect_repeating_pattern(html_content),
            "images": [],
            "_base_css": base_css,
        }
        try:
            builder, section_id = _convert_one_section(
                section, namespace, product_slug, output_path, blocks_dir, asset_type, semantic_type,
            )
        except ValueError as exc:
            print(f"ERRO ao converter section '{semantic_type}': {exc}", file=sys.stderr)
            sys.exit(1)
        node = build_template_section_node(builder, section_id)
        section_nodes.append((section_id, node))

    # POPULATE — emite o template JSON com todas as sections na ordem do manifest.
    tpl_path = (
        Path(args.emit_template_json).expanduser().resolve()
        if args.emit_template_json
        else manifest_path.parent / f"page.{page_handle}.json"
    )
    emit_template_json(tpl_path, page_handle, section_nodes)
    print(f"[liquid-converter v2] POPULATE → template emitido em {tpl_path} ({len(section_nodes)} sections)")
    print("[liquid-converter v2] ATENÇÃO: valide cada .liquid com a skill `shopify-plugin:shopify-liquid` antes de instalar.")


def main():
    parser = argparse.ArgumentParser()
    # Dois modos de input: sections.json (legacy, do analyzer) ou HTML/CSS fresh (Modo C)
    parser.add_argument("--sections-json", help="(Modo B legacy) Path to sections.json from analyzer")
    parser.add_argument("--section-index", type=int, help="(Modo B legacy) 1-based index of section to convert")
    parser.add_argument("--html", help="(Modo C) Path to fresh HTML file from frontend-design")
    parser.add_argument("--css", help="(Modo C) Path to fresh CSS file (injected into the stylesheet block)")
    parser.add_argument("--type", help="(Modo C) Semantic type of the section (hero/features/faq/etc)")
    parser.add_argument("--output", help="Path to output .liquid file (single-section mode)")
    parser.add_argument("--blocks-dir", help="Directory where blocks/*.liquid files go (single-section mode)")
    parser.add_argument("--namespace", help="CSS namespace (e.g. page-[produto]-hero)")
    parser.add_argument("--product-slug", help="Product slug (e.g. [produto])")
    parser.add_argument("--asset-type", choices=["section", "block"], default="section",
                        help="Output as Shopify section (default) or theme block (for Horizon-style composability)")
    # GAP-B / GAP-E
    parser.add_argument("--batch", help="(Modo E batch) Path to batch manifest JSON: converte a página inteira + POPULATE numa invocação")
    parser.add_argument("--emit-template-json", help="(GAP-B POPULATE) Path do templates/page.[handle].json a emitir")
    parser.add_argument("--page-handle", help="(GAP-B POPULATE) Handle da página Shopify (default: product-slug)")
    args = parser.parse_args()

    # GAP-E: modo batch — converte todas as sections + emite o template JSON numa só invocação.
    if args.batch:
        run_batch(args)
        return

    # Single-section: os campos abaixo são obrigatórios fora do batch.
    missing = [f for f in ("output", "blocks_dir", "namespace", "product_slug") if not getattr(args, f)]
    if missing:
        parser.error("argumentos obrigatórios faltando (fora do modo --batch): "
                     + ", ".join("--" + m.replace("_", "-") for m in missing))

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
            "repeating_pattern": detect_repeating_pattern(html_content),
            "images": [],
        }
        print(f"[liquid-converter v2] Modo C — convertendo HTML fresh ({args.type or 'section'})")
    elif args.sections_json and args.section_index:
        # Modo B legacy — sections.json do analyzer
        sections_json = Path(args.sections_json).expanduser().resolve()
        if not sections_json.exists():
            print(f"ERRO: {sections_json} não encontrado", file=sys.stderr)
            sys.exit(1)
        try:
            data = json.loads(sections_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(
                f"ERRO: JSON inválido em {sections_json} (linha {exc.lineno} col {exc.colno}): {exc.msg}",
                file=sys.stderr,
            )
            sys.exit(1)
        except OSError as exc:
            print(f"ERRO: falha ao ler {sections_json}: {exc}", file=sys.stderr)
            sys.exit(1)
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
    try:
        file_content = builder.build_section_file(
            converted_markup,
            section_name,
            section_tag_class,
            base_stylesheet=base_css,
            asset_type=args.asset_type,
        )
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(file_content, encoding="utf-8")

    print(f"[liquid-converter v2] section salva em {output_path}")
    print(f"[liquid-converter v2] stats: {len(builder.settings)} settings · {len(builder.blocks_schemas)} block type(s)")

    if builder.blocks_schemas:
        blocks_dir.mkdir(parents=True, exist_ok=True)
        for block_type, block_data in builder.blocks_schemas.items():
            try:
                block_content = builder.build_block_file(block_type, block_data)
            except ValueError as exc:
                print(f"ERRO: {exc}", file=sys.stderr)
                sys.exit(1)
            block_file = blocks_dir / f"{args.namespace}-{block_type}.liquid"
            block_file.write_text(block_content, encoding="utf-8")
            print(f"[liquid-converter v2] block salvo em {block_file}")

    # GAP-B: POPULATE single-section — emite (ou cria) o template JSON com este section node.
    # Útil pra converter section a section; pra página inteira prefira --batch.
    if args.emit_template_json:
        page_handle = args.page_handle or args.product_slug
        section_id = output_path.stem
        node = build_template_section_node(builder, section_id)
        tpl_path = Path(args.emit_template_json).expanduser().resolve()
        # Se o template já existe, faz merge aditivo (preserva sections já emitidas).
        existing_nodes = []
        if tpl_path.exists():
            try:
                existing = json.loads(tpl_path.read_text(encoding="utf-8"))
                for sid in existing.get("order", []):
                    if sid != section_id and sid in existing.get("sections", {}):
                        existing_nodes.append((sid, existing["sections"][sid]))
            except (json.JSONDecodeError, OSError):
                pass
        emit_template_json(tpl_path, page_handle, existing_nodes + [(section_id, node)])
        print(f"[liquid-converter v2] POPULATE → template atualizado em {tpl_path}")

    print("[liquid-converter v2] ATENÇÃO: sempre valide o arquivo gerado com a skill `shopify-plugin:shopify-liquid` antes de instalar no tema. Edge cases podem precisar ajuste manual.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[liquid-converter v2] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("falha inesperada: %s", exc)
        sys.exit(1)
