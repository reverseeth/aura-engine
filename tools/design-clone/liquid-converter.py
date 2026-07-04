#!/usr/bin/env python3
"""
liquid-converter.py — Aura Engine design-clone pipeline (conversor canônico da 07b) · v3

Recebe uma seção (HTML+CSS) e converte em Shopify Liquid section editável via
theme editor. Substitui textos fixos por {{ section.settings.* }}, imagens por
image_picker settings, cores/tokens por CSS custom properties, e padrões
repetíveis (cards/tiers/reviews/faq) por BLOCKS LOCAIS inline no schema da
section ({% for block in section.blocks %} + {% case block.type %}) — NUNCA
theme blocks em blocks/*.liquid (o validator do Shopify bloqueia
{% content_for 'block' %} com type dinâmico).

v3 melhorias (auditoria 2026-07):
- Blocks locais inline: schema.blocks com {type, name, settings} completos,
  markup com {{ block.settings.* }} + {{ block.shopify_attributes }}
- Copy REAL de cada item repetido preservada (uma instância por item, com os
  defaults daquele item — presets e templates/page.json pré-populados)
- Irmãos que NÃO fazem parte do padrão repetido são preservados no markup
- Defaults de richtext/inline_richtext preservam HTML intencional (<p>, <em>)
- Schema names limitados a 25 chars (regra ValidSchemaName do theme-check)
- CSS da página filtrado por section (sem N cópias do page.css no tema)
- :root/html/body rescopados pro root da section (custom properties resolvem)
- Tokens migrados ANTES das cores (shadow com hex não vira setting morto)

Uso (Modo C — HTML fresh aprovado na 07a, padrão da skill 07b-page-build):
    python3 liquid-converter.py \\
        --html /tmp/fresh-<produto>/<tipo>.html \\
        --css /tmp/fresh-<produto>/<tipo>.css \\
        --type hero \\
        --output <path.liquid> \\
        --namespace page-<produto>-<tipo> \\
        --product-slug <produto>

Uso (Modo B legacy — clone direto do HTML do concorrente via sections.json):
    REQUER --allow-competitor-markup. Este modo injeta copy/markup do
    concorrente no tema — viola o princípio "zero código do concorrente no
    output final". Use apenas pra clonar página SUA de outra loja sua.

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

# Bootstrap re-exec (mesmo padrão do fetch.py da lib web-fetch): se o python
# atual não tem bs4 e um venv do framework existe, re-executa nele —
# `python3 liquid-converter.py` direto funciona desde que o venv exista.
try:
    from _venv_bootstrap import bootstrap as _venv_bootstrap
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _venv_bootstrap import bootstrap as _venv_bootstrap
_venv_bootstrap("bs4")

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

# Shopify/theme-check (ValidSchemaName) limita o `name` de sections e blocks a 25 chars.
SCHEMA_NAME_MAX = 25

# Placeholder textual inserido no lugar do padrão repetido; substituído pelo
# {% for block in section.blocks %} DEPOIS da serialização (pra não re-namespacear
# o markup do block).
BLOCKS_LOOP_TOKEN = "__AURA_BLOCKS_LOOP__"


def escape_liquid_default(text: str, preserve_html: bool = False) -> str:
    """Escapa texto pra uso seguro como `default` no schema Shopify.

    - preserve_html=False (text/textarea): HTML-escape completo (`<`, `>`, `&`, `"`, `'`).
    - preserve_html=True (richtext/inline_richtext): mantém as tags HTML INTENCIONAIS
      (<p>, <em>, <strong> — o Shopify exige richtext envolto em <p>) e escapa apenas
      os delimitadores Liquid.
    """
    if text is None:
        return ""
    if preserve_html:
        escaped = str(text)
    else:
        escaped = html_lib.escape(str(text), quote=True)
    escaped = escaped.replace("{{", "&#123;&#123;").replace("}}", "&#125;&#125;")
    escaped = escaped.replace("{%", "&#123;&#37;").replace("%}", "&#37;&#125;")
    return escaped


def schema_display_name(text: str, max_len: int = SCHEMA_NAME_MAX) -> str:
    """Nome de display pro schema, respeitando o limite de 25 chars do Shopify."""
    clean = re.sub(r"[\s_-]+", " ", str(text or "")).strip()
    if not clean:
        clean = "Section"
    clean = clean[0].upper() + clean[1:]
    return clean[:max_len].rstrip() or "Section"


def validate_shopify_schema(schema: dict) -> list[str]:
    """Valida schema Shopify e retorna lista de erros (vazia = ok)."""
    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["schema deve ser dict"]

    def _check_name(name, scope_label: str) -> None:
        if isinstance(name, str) and len(name) > SCHEMA_NAME_MAX:
            errors.append(
                f"{scope_label}: name {name!r} excede {SCHEMA_NAME_MAX} caracteres "
                f"(regra ValidSchemaName do Shopify)"
            )

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

    _check_name(schema.get("name"), "schema")
    _check_settings(schema.get("settings", []), "settings")
    for block in schema.get("blocks", []) or []:
        if not isinstance(block, dict):
            continue
        b_label = f"block[{block.get('type', '?')}]"
        if not block.get("type"):
            errors.append(f"{b_label}: campo 'type' obrigatório")
        if "settings" in block:
            # Block local (inline no schema da section) exige name.
            if not block.get("name"):
                errors.append(f"{b_label}: campo 'name' obrigatório em block local")
            _check_name(block.get("name"), b_label)
            _check_settings(block.get("settings", []), f"{b_label}.settings")
    return errors


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


# As vars de cor/token são injetadas INLINE no elemento root da section — invisíveis
# pro :root real do documento. Sem rescopar, um `:root { --ink: #14161d }` viraria
# `--ink: var(--color_1)` com --color_1 inalcançável (todo var(--ink) colapsa).
_ROOT_SCOPE_RE = re.compile(r"(?<![\w.#\[-])(?::root|html|body)\b")


def rescope_root_selectors(css: str, target: str, max_depth: int = 5) -> str:
    """Reescreve seletores :root/html/body pro(s) seletor(es) em `target`.

    `target` deve incluir a classe wrapper do schema (.{ns}) E a classe do root do
    markup (ex: '.{ns}, .{ns}__hero') — as vars inline vivem no root do MARKUP
    (filho do wrapper que o Shopify gera), então custom properties tipo --ink só
    resolvem se a regra também casar com esse elemento."""
    if not css or not target or max_depth <= 0:
        return css
    out: list[str] = []
    i, n = 0, len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            out.append(css[i:])
            break
        selector_part = css[i:brace]
        stripped = selector_part.lstrip()
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
        if stripped.startswith("@"):
            m = re.match(r"@[\w-]+", stripped)
            at_name = m.group(0).lower() if m else ""
            out.append(selector_part + "{")
            if at_name in ("@media", "@supports", "@container", "@document"):
                out.append(rescope_root_selectors(block_content, target, max_depth - 1))
            else:
                out.append(block_content)
        else:
            out.append(_ROOT_SCOPE_RE.sub(target, selector_part) + "{")
            out.append(block_content)
        out.append("}")
        i = j
    return "".join(out)


def filter_css_for_markup(css: str, markup: str, extra_classes=(), max_depth: int = 5) -> str:
    """Mantém só as regras cujo selector referencia classes/ids presentes no markup
    da section (+ a classe wrapper do schema).

    Sem o filtro, o page.css INTEIRO seria embutido em cada section (~N cópias no
    tema) e cada section ganharia settings de cor/token da página inteira. Regras
    sem classe/id (element/universal) são mantidas; @keyframes/@font-face também;
    @media/@supports são filtrados recursivamente."""
    if not css:
        return css
    used_classes = set(extra_classes or ())
    for attr in re.findall(r'class="([^"]*)"', markup):
        used_classes.update(attr.split())
    # Classes dentro de params Liquid (ex: image_tag class: '...')
    for attr in re.findall(r"class:\s*'([^']*)'", markup):
        used_classes.update(attr.split())
    used_ids = set(re.findall(r'id="([^"]*)"', markup))

    # Comentários atrapalham o brace-walk (podem conter chaves)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)

    def _keep(selector_list: str) -> bool:
        for sel in selector_list.split(","):
            classes = re.findall(r"\.([A-Za-z_][\w-]*)", sel)
            ids = re.findall(r"#([A-Za-z_][\w-]*)", sel)
            if not classes and not ids:
                return True  # element/universal — global à section, barato
            if any(c in used_classes for c in classes) or any(i in used_ids for i in ids):
                return True
        return False

    def _filter(text: str, depth: int) -> str:
        if depth <= 0:
            return text
        out: list[str] = []
        i, n = 0, len(text)
        while i < n:
            brace = text.find("{", i)
            if brace == -1:
                out.append(text[i:])
                break
            selector_part = text[i:brace]
            stripped = selector_part.lstrip()
            depth_b = 1
            j = brace + 1
            while j < n and depth_b > 0:
                c = text[j]
                if c == "{":
                    depth_b += 1
                elif c == "}":
                    depth_b -= 1
                j += 1
            body = text[brace + 1:j - 1]
            if stripped.startswith(("@media", "@supports", "@container")):
                inner = _filter(body, depth - 1)
                if inner.strip():
                    out.append(selector_part + "{" + inner + "}")
            elif stripped.startswith("@"):
                out.append(selector_part + "{" + body + "}")  # keyframes/font-face: mantém
            elif _keep(selector_part):
                out.append(selector_part + "{" + body + "}")
            i = j
        return "".join(out)

    return _filter(css, max_depth)


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
    que é injetada inline no root + exposta como setting. O pattern usa \\s+ entre as
    partes do valor pra casar valores multi-linha (o default foi normalizado)."""
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
        # Whitespace flexível: o valor no CSS original pode ter quebras de linha.
        value_pattern = r"\s+".join(re.escape(part) for part in raw.split())
        pattern = re.compile(
            re.escape(prop) + r"(\s*:\s*)" + value_pattern + r"(\s*(?=;|}))",
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

    # Remove scripts, noscript, iframe — COM WARNING listando o que foi removido,
    # pra 07b poder reimplementar a interação (ex: <details> nativo) em vez de
    # perder silenciosamente algo aprovado pelo membro na 07a.
    removed_scripts = []
    for tag in soup.find_all(["script", "noscript", "iframe"]):
        if tag.name == "script":
            snippet = (tag.get("src") or tag.get_text() or "").strip().replace("\n", " ")[:80]
            removed_scripts.append(snippet or "<script inline vazio>")
        tag.decompose()
    if removed_scripts:
        logger.warning(
            "%d <script> removido(s) do markup (sections não levam o JS do design "
            "aprovado — reimplemente a interação via Liquid/CSS/<details>): %s",
            len(removed_scripts), " | ".join(removed_scripts),
        )

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
        self._blocks_loops = []  # liquid dos {% for block %} a injetar pós-serialização

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
        # richtext/inline_richtext preservam o HTML intencional (<p>, <em>, <strong>);
        # só os delimitadores Liquid são escapados neles.
        safe_default = default
        if default is not None and s_type in ("text", "richtext", "inline_richtext", "textarea"):
            safe_default = escape_liquid_default(
                default, preserve_html=s_type in ("richtext", "inline_richtext"),
            )

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
        # richtext: o valor do Shopify JÁ vem envolto em <p> — o texto interno é
        # escapado aqui, o wrapper é preservado por add_setting (preserve_html).
        default = text if s_type == "text" else f"<p>{html_lib.escape(text)}</p>"
        real_id = self.add_setting(s_id, s_type, label, default=default)

        # richtext renderiza o próprio <p> — manter o placeholder dentro do <p>
        # original geraria <p><p> aninhado (inválido; browser fecha o externo).
        wrapper_name = "div" if s_type == "richtext" else el.name
        new_tag = BeautifulSoup("", "html.parser").new_tag(wrapper_name)
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
        # O dedup de add_setting pode devolver um id EXISTENTE (texto repetido) —
        # o markup TEM que usar o id retornado, senão referencia setting inexistente.
        real_label_id = self.add_setting(label_id, "text", "Link label", default=text or "Click here")
        # Shopify url settings only accept absolute URLs or paths starting with "/". Anchors/relative fail push validation. Omit default when invalid.
        url_default = href if href.startswith(("http://", "https://", "/")) else None
        real_url_id = self.add_setting(url_id, "url", "Link URL", default=url_default)
        new_a = BeautifulSoup("", "html.parser").new_tag("a")
        new_a["href"] = "{{ section.settings." + real_url_id + " }}"
        if el.has_attr("class"):
            new_a["class"] = el["class"]
        new_a.append(BeautifulSoup("{{ section.settings." + real_label_id + " }}", "html.parser"))
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

        # Dedup-aware: usa o id RETORNADO (CTA duplicado — sticky + pricing — é o
        # caso comum; sem isso o botão renderizaria sem texto).
        real_label_id = self.add_setting(label_id, "text", "CTA label", default=text)
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
        real_fallback_id = self.add_setting(fallback_id, "url", "CTA fallback URL",
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
            '<button type="submit" class="' + btn_class + '">{{ ' + s + real_label_id + " }}</button>"
            "</form>"
            "{% else %}"
            '<a href="{{ ' + s + real_fallback_id + " | default: '/cart' }}\" class=\"" + btn_class + "\">"
            "{{ " + s + real_label_id + " }}</a>"
            "{% endif %}"
        )
        el.replace_with(BeautifulSoup(liquid, "html.parser"))

    def process(self, section_dict, asset_type="section"):
        html = section_dict["html"]
        soup = BeautifulSoup(html, "html.parser")
        self._blocks_loops = []

        # Step 1: limpa artefatos Shopify ANTES do namespacing (pra classes/tags originais ainda existirem)
        strip_shopify_artifacts(soup)

        # Step 2: extrai block local SE houver padrão repetitivo (usa classes originais
        # pré-namespace). Em asset_type=block não há section.blocks — itens repetidos
        # ficam como settings normais.
        repeating = section_dict.get("repeating_pattern", {})
        if asset_type != "block" and repeating.get("detected") and repeating.get("count", 0) >= 2:
            self._extract_block_from_repeating(soup, repeating, section_dict.get("semantic_type", "item"))

        # Step 3: namespace classes (após extrair blocks)
        namespace_classes(soup, self.namespace)
        clean_inline_styles(soup)

        # Step 4: converte texto, imagens, links
        self._convert_element_recursive(soup, self)

        # Step 5: injeta o(s) {% for block %} DEPOIS da serialização — o markup do
        # block já está namespaceado/convertido e não pode passar de novo pelos steps 3-4.
        markup = str(soup)
        for loop_liquid in self._blocks_loops:
            markup = markup.replace(BLOCKS_LOOP_TOKEN, loop_liquid, 1)
        return markup

    def _extract_block_from_repeating(self, soup, repeating, semantic_hint):
        """Extrai o padrão repetido como BLOCK LOCAL (inline no schema da section).

        - TODOS os itens são convertidos: o item 1 vira o markup-template do block e
          a copy REAL de cada item vira uma instância (defaults próprios) que alimenta
          presets + templates/page.json — nunca N clones do item 1.
        - Só os itens que casam com o padrão saem do markup; irmãos diferentes
          (ex: uma cta-row no fim do grid) são preservados.
        - O markup do block usa o MESMO namespace da section (o CSS reescrito continua
          casando) e referencia {{ block.settings.* }} + {{ block.shopify_attributes }}.
        """
        child_tag = repeating.get("child_tag")
        child_classes = set(repeating.get("child_classes") or [])

        matches = []
        container = None
        if child_classes:
            for el in soup.find_all(child_tag):
                el_classes = set(el.get("class", []) or [])
                if child_classes.issubset(el_classes):
                    if container is None:
                        container = el.parent
                    if el.parent is container:
                        matches.append(el)

        # Fallback: se não achou por classes, usa os filhos diretos repetidos do
        # primeiro container plausível
        if not matches:
            for potential_container in soup.find_all(True):
                kids = potential_container.find_all(child_tag, recursive=False)
                if len(kids) >= 2:
                    matches = list(kids)
                    container = potential_container
                    break

        if len(matches) < 2 or container is None:
            return

        block_type = slugify(semantic_hint) or "item"

        # Converte CADA item (não só o primeiro) pra capturar a copy real por instância.
        instance_builders = []
        for el in matches:
            item_soup = BeautifulSoup(str(el), "html.parser")
            strip_shopify_artifacts(item_soup)
            namespace_classes(item_soup, self.namespace)
            clean_inline_styles(item_soup)
            b = LiquidBuilder(self.namespace, self.product_slug)
            b._convert_element_recursive(item_soup, b)
            instance_builders.append((b, item_soup))

        template_builder, template_soup = instance_builders[0]
        block_markup = str(template_soup).replace("section.settings.", "block.settings.")
        # shopify_attributes no root do block (theme editor highlight/reorder)
        block_markup = re.sub(
            r"(<[a-zA-Z][^>]*?)(/?>)",
            r"\1 {{ block.shopify_attributes }}\2",
            block_markup,
            count=1,
        )

        template_defaults = _settings_defaults(template_builder.settings)
        instances = []
        for idx, (b, _) in enumerate(instance_builders):
            item_defaults = _settings_defaults(b.settings)
            if idx > 0 and set(item_defaults) != set(template_defaults):
                logger.warning(
                    "block '%s': item %d tem estrutura diferente do item 1 — settings sem "
                    "correspondência mantêm o default do item 1",
                    block_type, idx + 1,
                )
            inst = dict(template_defaults)
            for sid in inst:
                if sid in item_defaults:
                    inst[sid] = item_defaults[sid]
            instances.append(inst)

        self.blocks_schemas[block_type] = {
            "markup": block_markup,
            "settings": template_builder.settings,
            "instances": instances,
            "name": schema_display_name(f"{semantic_hint} item"),
        }

        loop_liquid = (
            "{% for block in section.blocks %}"
            "{% case block.type %}"
            f"{{% when '{block_type}' %}}"
            f"{block_markup}"
            "{% endcase %}"
            "{% endfor %}"
        )
        self._blocks_loops.append(loop_liquid)

        # Remove APENAS os itens do padrão; o token marca a posição do primeiro item
        # (o loop entra ali, não no fim do container).
        matches[0].insert_before(NavigableString(BLOCKS_LOOP_TOKEN))
        for el in matches:
            el.decompose()

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
            if child.name == "svg":
                continue  # texto interno de SVG não vira setting
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
            if BLOCKS_LOOP_TOKEN in child.get_text():
                # container do padrão repetido — só recursão (o token não vira setting)
                builder._convert_element_recursive(child, builder)
                continue
            text_children = [c for c in child.children if isinstance(c, NavigableString) and c.strip()]
            tag_children = [c for c in child.children if isinstance(c, Tag)]
            # Everything-editable: QUALQUER tag folha com texto direto vira setting
            # (inclui <div class="price">$49</div>, eyebrows em div, etc).
            if text_children and not tag_children:
                builder.convert_text_node(child)
                continue
            if text_children and tag_children and all(c.name in INLINE_TAGS for c in tag_children):
                builder.convert_mixed_text_node(child)
                continue
            builder._convert_element_recursive(child, builder)

    def build_section_file(self, markup, section_name, section_tag_class, base_stylesheet="", asset_type="section"):
        scope = "block" if asset_type == "block" else "section"

        # 1) Rescopa :root/html/body pro wrapper do schema (.{ns}) E pro root do
        #    markup — as vars inline ficam no root do markup (filho do wrapper),
        #    então custom properties do design (tokens tipo --ink) só resolvem se
        #    a regra rescopada casar com esse elemento também.
        rescope_target = f".{self.namespace}"
        root_class_m = re.search(
            r'<(?:section|div|article|aside|main|header|footer)\b[^>]*?class="([^"]+)"',
            markup,
        )
        if root_class_m:
            first_cls = root_class_m.group(1).split()[0]
            if first_cls and first_cls != self.namespace:
                rescope_target += f", .{first_cls}"
        base_stylesheet = rescope_root_selectors(base_stylesheet, rescope_target)
        # 2) Filtra o CSS da página pras regras que ESTA section usa (o page.css inteiro
        #    em cada section = N cópias no tema + settings de outras sections aqui).
        base_stylesheet = filter_css_for_markup(
            base_stylesheet, markup, extra_classes=(section_tag_class or "").split(),
        )

        # GAP-A + GAP-D: extrai tokens E cores do CSS, transforma cada um em setting +
        # custom property, e injeta TODAS as vars INLINE no root da section (com
        # | escape em cada interpolação). Tokens ANTES de cores: um box-shadow com hex
        # migra inteiro pro setting de shadow; se cores rodassem primeiro, o valor
        # tokenizado nunca casaria (setting morto).
        tokens = extract_tokens_from_css(base_stylesheet)
        if tokens:
            base_stylesheet = replace_tokens_with_vars(base_stylesheet, tokens)
        color_map = extract_colors_from_css(base_stylesheet)
        if color_map:
            base_stylesheet = replace_colors_with_vars(base_stylesheet, color_map)

        prepend_settings = []
        inline_pairs = []  # setting_id → vira "--id: {{ scope.settings.id | escape }}"

        if color_map:
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

            def _inject_vars(m: re.Match) -> str:
                open_tag, close = m.group(1), m.group(2)
                if "style=" not in open_tag:
                    return f'{open_tag} style="{inline_vars}"{extra}{close}'
                # Merge DENTRO do atributo style existente (nunca na última aspa do
                # tag — que pode pertencer a class/qualquer outro atributo).
                merged = re.sub(
                    r'(style\s*=\s*")([^"]*)(")',
                    lambda s: s.group(1)
                    + ((s.group(2).rstrip("; ").strip() + "; ") if s.group(2).strip() else "")
                    + inline_vars
                    + s.group(3),
                    open_tag,
                    count=1,
                )
                return f"{merged}{extra}{close}"

            # Injeta no PRIMEIRO elemento de abertura do markup (root da section).
            injected = re.subn(
                r"(<(?:section|div|article|aside|main)\b[^>]*?)(>)",
                _inject_vars,
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

        if asset_type == "block":
            schema = {
                "name": section_name,
                "tag": None,
                "settings": self.settings,
                "presets": [{"name": section_name}],
            }
        else:
            # Blocks LOCAIS inline no schema (com name+settings) — nunca theme blocks.
            blocks_defs = []
            preset_blocks = []
            for t, data in self.blocks_schemas.items():
                blocks_defs.append({
                    "type": t,
                    "name": data.get("name") or schema_display_name(t),
                    "settings": data["settings"],
                })
                for inst in data.get("instances") or []:
                    preset_blocks.append({"type": t, "settings": dict(inst)})
            schema = {
                "name": section_name,
                "tag": "section",
                "class": section_tag_class,
                "settings": self.settings,
                "blocks": blocks_defs,
                "presets": [{
                    "name": section_name,
                    "blocks": preset_blocks,
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


def build_template_section_node(builder, section_id):
    """GAP-B: monta o node de UMA section pro templates/page.json a partir do schema construído.

    - settings: defaults reais da copy injetada (section-level).
    - blocks{} / block_order[]: UMA instância por item REAL detectado no HTML, com os
      defaults daquele item (copy própria preservada — nunca N clones do item 1).
      block_order segue a ordem visual dos itens.
    """
    schema = builder.built_schema or {}
    node = {
        "type": section_id,
        "settings": _settings_defaults(schema.get("settings", [])),
    }

    if builder.blocks_schemas:
        blocks = {}
        block_order = []
        for t, data in builder.blocks_schemas.items():
            instances = data.get("instances") or [_settings_defaults(data.get("settings", []))]
            for n, inst in enumerate(instances):
                inst_id = f"{t}_{n + 1}"
                blocks[inst_id] = {"type": t, "settings": dict(inst)}
                block_order.append(inst_id)
        node["blocks"] = blocks
        node["block_order"] = block_order
    return node


def emit_template_json(path: Path, section_nodes: list[tuple[str, dict]]):
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


def _convert_one_section(section, namespace, product_slug, output_path, asset_type, semantic_type):
    """Converte uma única section (dict) → escreve o .liquid, retorna (builder, section_id).

    Blocks são inline no schema da section — nenhum arquivo blocks/*.liquid é gerado."""
    builder = LiquidBuilder(namespace, product_slug)
    converted_markup = builder.process(section, asset_type=asset_type)

    section_name = schema_display_name(semantic_type)
    section_tag_class = f"{namespace} {namespace}--{slugify(semantic_type)}"
    file_content = builder.build_section_file(
        converted_markup, section_name, section_tag_class,
        base_stylesheet=section.get("_base_css", ""), asset_type=asset_type,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(file_content, encoding="utf-8")
    n_instances = sum(len(d.get("instances") or []) for d in builder.blocks_schemas.values())
    print(f"[liquid-converter v3] section salva em {output_path}")
    print(
        f"[liquid-converter v3] stats: {len(builder.settings)} settings · "
        f"{len(builder.blocks_schemas)} block type(s) inline · {n_instances} instância(s) com copy real"
    )

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
         "output": "<staging>/sections/page-produto-hero.liquid"}
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

    def _resolve(val, field):
        """Aceita conteúdo inline OU path. Se for path existente, lê o arquivo.
        Path aparente (termina em .html/.css) que NÃO existe = erro explícito —
        nunca seguir silenciosamente sem o conteúdo."""
        if not val:
            return ""
        sval = str(val)
        if len(sval) < 4096 and "\n" not in sval:
            p = Path(sval).expanduser()
            if p.exists() and p.is_file():
                return p.read_text(encoding="utf-8")
            if sval.lower().endswith((".html", ".htm", ".css")):
                print(f"ERRO: '{field}' aponta pra arquivo inexistente: {p}", file=sys.stderr)
                sys.exit(1)
        return val

    section_nodes = []
    for spec in section_specs:
        namespace = spec["namespace"]
        semantic_type = spec.get("type", "section")
        html_content = _resolve(spec.get("html"), f"sections[{semantic_type}].html")
        css_raw = _resolve(spec.get("css"), f"sections[{semantic_type}].css")
        base_css = rewrite_css_for_namespace(css_raw, namespace) if css_raw else ""
        output_path = Path(spec["output"]).expanduser().resolve()
        section = {
            "html": html_content,
            "semantic_type": semantic_type,
            "repeating_pattern": spec.get("repeating_pattern") or detect_repeating_pattern(html_content),
            "images": [],
            "_base_css": base_css,
        }
        try:
            builder, section_id = _convert_one_section(
                section, namespace, product_slug, output_path, asset_type, semantic_type,
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
    emit_template_json(tpl_path, section_nodes)
    print(f"[liquid-converter v3] POPULATE → template emitido em {tpl_path} ({len(section_nodes)} sections)")
    print("[liquid-converter v3] ATENÇÃO: valide cada .liquid com a skill `shopify-plugin:shopify-liquid` antes de instalar.")


def main():
    parser = argparse.ArgumentParser()
    # Dois modos de input: sections.json (legacy, do analyzer) ou HTML/CSS fresh (Modo C)
    parser.add_argument("--sections-json", help="(Modo B legacy) Path to sections.json from analyzer — REQUER --allow-competitor-markup")
    parser.add_argument("--section-index", type=int, help="(Modo B legacy) 1-based index of section to convert")
    parser.add_argument("--allow-competitor-markup", action="store_true",
                        help="(Modo B) Confirma que você ENTENDE que copy/markup do HTML de origem "
                             "(concorrente) entrará no tema como defaults — só use com página própria")
    parser.add_argument("--html", help="(Modo C) Path to fresh HTML file from frontend-design")
    parser.add_argument("--css", help="(Modo C) Path to fresh CSS file (injected into the stylesheet block)")
    parser.add_argument("--type", help="(Modo C) Semantic type of the section (hero/features/faq/etc)")
    parser.add_argument("--output", help="Path to output .liquid file (single-section mode)")
    parser.add_argument("--blocks-dir", help="(DEPRECADO — blocks agora são inline no schema da section; "
                                             "flag aceita e ignorada por compatibilidade)")
    parser.add_argument("--namespace", help="CSS namespace (e.g. page-[produto]-hero)")
    parser.add_argument("--product-slug", help="Product slug (e.g. [produto])")
    parser.add_argument("--asset-type", choices=["section", "block"], default="section",
                        help="Output as Shopify section (default) or theme block (for Horizon-style composability)")
    # GAP-B / GAP-E
    parser.add_argument("--batch", help="(Modo E batch) Path to batch manifest JSON: converte a página inteira + POPULATE numa invocação")
    parser.add_argument("--emit-template-json", help="(GAP-B POPULATE) Path do templates/page.[handle].json a emitir")
    parser.add_argument("--page-handle", help="(GAP-B POPULATE) Handle da página Shopify (default: product-slug)")
    args = parser.parse_args()

    if args.blocks_dir:
        logger.info("--blocks-dir é deprecado e foi ignorado: blocks são inline no schema da section (nenhum blocks/*.liquid é gerado)")

    # GAP-E: modo batch — converte todas as sections + emite o template JSON numa só invocação.
    if args.batch:
        run_batch(args)
        return

    # Single-section: os campos abaixo são obrigatórios fora do batch.
    missing = [f for f in ("output", "namespace", "product_slug") if not getattr(args, f)]
    if missing:
        parser.error("argumentos obrigatórios faltando (fora do modo --batch): "
                     + ", ".join("--" + m.replace("_", "-") for m in missing))

    output_path = Path(args.output).expanduser().resolve()

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
            if not css_path.exists():
                # Falha explícita: seguir sem CSS deployaria a section SEM estilo.
                print(f"ERRO: --css {css_path} não encontrado", file=sys.stderr)
                sys.exit(1)
            base_css = rewrite_css_for_namespace(css_path.read_text(encoding="utf-8"), args.namespace)
        section = {
            "html": html_content,
            "semantic_type": args.type or "section",
            "repeating_pattern": detect_repeating_pattern(html_content),
            "images": [],
        }
        print(f"[liquid-converter v3] Modo C — convertendo HTML fresh ({args.type or 'section'})")
    elif args.sections_json and args.section_index:
        # Modo B legacy — sections.json do analyzer (HTML bruto da página de origem)
        if not args.allow_competitor_markup:
            print(
                "ERRO: o Modo B converte HTML BRUTO da página de origem — copy e markup "
                "do concorrente virariam defaults do SEU tema.\n"
                "Isso viola o princípio 'zero código do concorrente no output final'.\n"
                "Use o Modo C (--html/--css com o design próprio aprovado na 07a).\n"
                "Se a página de origem é SUA (ex: migração entre lojas próprias), re-rode "
                "com --allow-competitor-markup.",
                file=sys.stderr,
            )
            sys.exit(1)
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
        print(f"[liquid-converter v3] Modo B — convertendo seção {args.section_index}: {section.get('semantic_type')}")
    else:
        print("ERRO: forneça --html (Modo C) ou --sections-json + --section-index (Modo B legacy)", file=sys.stderr)
        sys.exit(1)

    builder = LiquidBuilder(args.namespace, args.product_slug)
    converted_markup = builder.process(section, asset_type=args.asset_type)

    semantic_type = section.get("semantic_type", "section")
    section_name = schema_display_name(semantic_type)
    section_tag_class = f"{args.namespace} {args.namespace}--{slugify(semantic_type)}"
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

    n_instances = sum(len(d.get("instances") or []) for d in builder.blocks_schemas.values())
    print(f"[liquid-converter v3] section salva em {output_path}")
    print(
        f"[liquid-converter v3] stats: {len(builder.settings)} settings · "
        f"{len(builder.blocks_schemas)} block type(s) inline · {n_instances} instância(s) com copy real"
    )

    # GAP-B: POPULATE single-section — emite (ou atualiza) o template JSON com este section node.
    # Útil pra converter section a section; pra página inteira prefira --batch.
    if args.emit_template_json:
        section_id = output_path.stem
        node = build_template_section_node(builder, section_id)
        tpl_path = Path(args.emit_template_json).expanduser().resolve()
        # Merge aditivo preservando a POSIÇÃO no order[]: re-compilar só o hero não
        # pode mandá-lo pro fim da página.
        merged_nodes: list[tuple[str, dict]] = []
        replaced = False
        if tpl_path.exists():
            try:
                existing = json.loads(tpl_path.read_text(encoding="utf-8"))
                for sid in existing.get("order", []):
                    if sid == section_id:
                        merged_nodes.append((sid, node))
                        replaced = True
                    elif sid in existing.get("sections", {}):
                        merged_nodes.append((sid, existing["sections"][sid]))
            except (json.JSONDecodeError, OSError):
                pass
        if not replaced:
            merged_nodes.append((section_id, node))
        emit_template_json(tpl_path, merged_nodes)
        print(f"[liquid-converter v3] POPULATE → template atualizado em {tpl_path}")

    print("[liquid-converter v3] ATENÇÃO: sempre valide o arquivo gerado com a skill `shopify-plugin:shopify-liquid` antes de instalar no tema. Edge cases podem precisar ajuste manual.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[liquid-converter v3] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("falha inesperada: %s", exc)
        sys.exit(1)
