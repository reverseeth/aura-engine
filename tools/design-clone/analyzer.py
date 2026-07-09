#!/usr/bin/env python3
"""
analyzer.py — Aura Engine design-clone pipeline (passo 2)

Lê o output do downloader.py e identifica as seções semanticamente — tanto as
genéricas de landing (hero, features, testimonials, faq, pricing, footer) quanto
as sections típicas de PDP/landing DTC (guarantee, before-after,
comparison-table, ingredients, how-it-works, founder-story). Retorna
sections.json, consumido pelos dois caminhos do aura_clone.py:
o pattern-extractor.py (modo signals) e o skeleton-builder in-process
(modo clone-and-adapt).

Se `computed-styles.json` existe no clone_dir (captura via downloader.py),
cada section ganha também um bloco `hierarchy` com sinais NUMÉRICOS de
hierarquia visual (proporção heading/body, padding-block real, densidade,
alinhamento dominante, proporção de área de mídia) — é o que preserva a
hierarquia de conversão da referência no modo clone-and-adapt. Sem
computed-styles (engine singlefile/--from-file), `hierarchy` fica null.

Uso:
    python3 analyzer.py <clone_dir>

Exemplo:
    python3 analyzer.py /tmp/clone-mybrand-1

Output:
    <clone_dir>/sections.json

Dependências:
    pip install beautifulsoup4
"""

import json
import re
import statistics
import sys
from pathlib import Path
from urllib.parse import urljoin

# Bootstrap re-exec (mesmo padrão do fetch.py da lib web-fetch): se o python
# atual não tem bs4 e um venv do framework existe, re-executa nele —
# `python3 analyzer.py` direto funciona desde que o venv exista.
try:
    from _venv_bootstrap import bootstrap as _venv_bootstrap
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _venv_bootstrap import bootstrap as _venv_bootstrap
_venv_bootstrap("bs4")

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERRO: BeautifulSoup4 não instalado. Rode: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


# Heurísticas por tipo semântico. Cada entrada = lista de palavras-chave em
# class/id/tag/aria-label que indicam o tipo. Match por TOKEN completo
# (case-insensitive) — nunca substring crua, senão classes hasheadas de
# styled-components/CSS-modules ("sc-qaVxK" contém "qa", "navy" contém "nav")
# viram sections falsas.
#
# ORDEM IMPORTA: em empate de score, vence o tipo que aparece PRIMEIRO no dict
# — por isso os tipos DTC específicos (guarantee, before-after, comparison-table,
# ingredients, how-it-works, founder-story) vêm antes dos genéricos (features,
# pricing), que têm hints mais largas.
SEMANTIC_HINTS = {
    "hero": ["hero", "banner", "jumbotron", "masthead", "above-fold", "page-header", "intro"],
    # ---- sections típicas de PDP/landing DTC (específicas primeiro) ----
    "guarantee": ["guarantee", "guaranteed", "money-back", "moneyback", "risk-free", "refund-policy", "warranty"],
    "before-after": ["before-after", "beforeafter", "before-and-after", "ba-slider", "transformation", "results-slider"],
    "comparison-table": ["comparison", "compare", "versus", "us-vs-them", "vs-table", "comparison-table", "comparison-chart"],
    "ingredients": ["ingredients", "ingredient", "formula", "actives", "whats-inside", "supplement-facts", "nutrition"],
    "how-it-works": ["how-it-works", "how-works", "how-to-use", "usage", "routine"],
    "founder-story": ["founder", "founder-story", "our-story", "brand-story", "about-us", "our-mission", "mission"],
    # ---- genéricas de landing ----
    "features": ["features", "benefits", "why", "advantages", "highlights", "perks"],
    "testimonials": ["testimonials", "reviews", "social-proof", "customer-say", "what-say", "reviews-grid", "user-say"],
    "faq": ["faq", "frequently-asked", "questions", "accordion", "qa"],
    "pricing": ["pricing", "plans", "tiers", "pack", "bundle", "offer", "price-table"],
    "gallery": ["gallery", "carousel", "slider", "lookbook"],
    "cta": ["cta", "call-to-action", "get-started", "signup", "subscribe-form"],
    "stats": ["stats", "numbers", "counters", "metrics"],
    "steps": ["steps", "process", "how-to", "timeline"],
    "trust-bar": ["trust", "logos", "as-seen", "featured-in", "press", "media-logos"],
    "footer": ["footer", "site-footer", "page-footer"],
    "header": ["header", "nav", "navbar", "site-header", "top-bar"],
}

_TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")

# Hints multi-palavra ("how-it-works") casam contra a forma normalizada da
# string ("How_It_Works" → "how-it-works"), com boundary de token nas pontas.
_HINT_PATTERNS = {
    hint: re.compile(rf"(?:^|-){re.escape(hint)}(?:-|$)")
    for hints in SEMANTIC_HINTS.values()
    for hint in hints
    if "-" in hint
}


def _tokenize(*parts):
    """Tokeniza strings (tag/classes/id/aria) em tokens completos.

    Retorna (set de tokens, lista de formas normalizadas por string —
    'How_It_Works grid' → tokens {how,it,works,grid}, normed ['how-it-works-grid']).
    """
    tokens: set = set()
    normed: list = []
    for p in parts:
        if not p:
            continue
        toks = [t for t in _TOKEN_SPLIT_RE.split(str(p).lower()) if t]
        if not toks:
            continue
        tokens.update(toks)
        normed.append("-".join(toks))
    return tokens, normed


def _hint_matches(hint, tokens, normed):
    """Hint simples = token exato; hint composta = sequência com boundary."""
    pat = _HINT_PATTERNS.get(hint)
    if pat is None:
        return hint in tokens
    return any(pat.search(s) for s in normed)


# Marcas de check/cross que tabelas comparativas DTC ("us vs them") usam.
_CHECKMARK_CHARS = ("✓", "✔", "✗", "✖", "×", "❌", "✅")


def score_semantic_type(tag, classes, section_id, aria_label, text_sample, el=None):
    """Retorna (tipo, confiança 0-1) baseado em heurísticas.

    Além dos hints de class/id/tag/aria, aplica boosts de CONTEÚDO (frases
    marcadoras no text_sample) e de ESTRUTURA (quando `el` é passado — ex:
    <table> com check/cross = comparison-table; <table> com supplement facts
    = ingredients). Sections DTC raramente têm class semântica limpa em tema
    customizado, então o conteúdo é o sinal que sobra.
    """
    tokens, normed = _tokenize(tag, *(classes or []), section_id, aria_label)
    scores = {}
    for sem_type, hints in SEMANTIC_HINTS.items():
        s = sum(1 for hint in hints if _hint_matches(hint, tokens, normed))
        if s > 0:
            scores[sem_type] = s

    def _boost(sem_type, pts):
        scores[sem_type] = scores.get(sem_type, 0) + pts

    text_lower = (text_sample or "")[:200].lower()
    if "frequently asked" in text_lower or "perguntas frequentes" in text_lower:
        _boost("faq", 2)
    if "testimonial" in text_lower or "customers say" in text_lower or "reviews" in text_lower:
        _boost("testimonials", 1)
    if "pricing" in text_lower or "plans" in text_lower or "$" in text_lower[:50]:
        _boost("pricing", 1)

    # Boosts de conteúdo pros tipos DTC (usa o text_sample inteiro — o marcador
    # costuma estar no heading da section, mas nem sempre nos primeiros 200 chars).
    tl_full = (text_sample or "").lower()
    if (
        "money-back" in tl_full or "money back" in tl_full
        or "risk-free" in tl_full or "risk free" in tl_full
        or re.search(r"\d+[- ]day guarantee", tl_full)
    ):
        _boost("guarantee", 2)
    if re.search(r"\bbefore\b", tl_full) and re.search(r"\bafter\b", tl_full):
        _boost("before-after", 2)
    if "how it works" in tl_full:
        _boost("how-it-works", 2)
    if "ingredients" in tl_full or "supplement facts" in tl_full:
        _boost("ingredients", 2)
    if (
        "founder" in tl_full or "our story" in tl_full
        or "we started" in tl_full or "my name is" in tl_full
    ):
        _boost("founder-story", 2)

    # Boost estrutural: <table> dentro da section.
    if el is not None:
        table = el.find("table")
        if table is not None:
            table_text = table.get_text(" ", strip=True).lower()
            if "supplement facts" in table_text or "ingredient" in table_text:
                _boost("ingredients", 2)
            elif (
                any(mark in table_text for mark in _CHECKMARK_CHARS)
                or re.search(r"\bvs\.?\b", table_text)
                or "other brands" in table_text
                or "them" in table_text.split()[:12]
            ):
                _boost("comparison-table", 2)
            else:
                _boost("comparison-table", 1)

    if not scores:
        return ("unknown", 0.0)
    best = max(scores.items(), key=lambda x: x[1])
    return (best[0], min(1.0, best[1] / 3.0))


def is_sectionable(el):
    """Retorna True se o elemento é candidato a virar uma section."""
    if el.name in ("section", "header", "footer", "main", "article", "aside"):
        return True
    tokens, normed = _tokenize(*(el.get("class", []) or []), el.get("id") or "")
    for hints in SEMANTIC_HINTS.values():
        for hint in hints:
            if _hint_matches(hint, tokens, normed):
                return True
    return False


def _count_sectionable_descendants(el, limit=2):
    """Conta descendentes sectionable de `el` (early-exit em `limit`)."""
    n = 0
    for d in el.find_all(True, recursive=True):
        if d.name == "main":
            continue
        if is_sectionable(d):
            n += 1
            if n >= limit:
                return n
    return n


def _is_wrapper_container(el):
    """True se `el` é um wrapper de layout que deve ser ATRAVESSADO, não virar section.

    Todo tema Shopify/DTC moderno embrulha o conteúdo em <main> (ex: Dawn:
    <main id="MainContent">). Se o <main> virasse section, TODA a página
    colapsaria em 1 section 'unknown' (o check de ancestral descartaria hero/
    features/reviews/faq internos). Um <main> só vira section quando NÃO contém
    ≥2 blocos sectionable (página degenerada/minimal).
    """
    if el.name != "main":
        return False
    return _count_sectionable_descendants(el, limit=2) >= 2


def get_text_sample(el, max_chars=300):
    txt = el.get_text(separator=" ", strip=True)
    return txt[:max_chars]


def extract_images_in_section(el):
    imgs = []
    for img in el.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if src:
            imgs.append({"src": src, "alt": img.get("alt", "")})
    for node in el.find_all(style=True):
        style = node.get("style", "")
        for m in re.finditer(r"url\(['\"]?([^'\"\)]+)['\"]?\)", style):
            imgs.append({"src": m.group(1), "alt": ""})
    return imgs


MAX_REPEAT_DEPTH = 3

# Tags que nunca são "item de conteúdo" num grid/lista — 2 <script> irmãos não
# são um carrossel.
_NON_CONTENT_TAGS = {"script", "style", "br", "hr", "link", "noscript", "meta", "template"}


def _iter_descendants_bounded(el, max_depth: int = MAX_REPEAT_DEPTH):
    """Itera descendentes de `el` até `max_depth` níveis (helper anti-explosão)."""
    def _walk(node, depth):
        if depth >= max_depth:
            return
        for child in node.find_all(recursive=False):
            yield child
            yield from _walk(child, depth + 1)

    yield from _walk(el, 0)


def _group_key(el):
    return (el.name, " ".join(sorted(el.get("class", []))))


def _eligible_repeat_child(el):
    """Só conta como item repetível: tag de conteúdo COM classe, ou <li>.

    Sem esse filtro, 2 <script> ou 3 <div> wrapper sem classe (heading/body/cta)
    viravam 'grid de 3 itens' e o skeleton gerava placeholder-cards falsos.
    """
    if el.name in _NON_CONTENT_TAGS:
        return False
    return bool(el.get("class")) or el.name == "li"


def extract_repeating_pattern(el):
    """
    Detecta padrões repetíveis (features, testimonials, faq items).
    Retorna lista de elementos filhos com mesma estrutura, ou [] se não houver.
    Prefere o MAIOR grupo (não o primeiro). Procura recursivamente até
    `MAX_REPEAT_DEPTH` (3) níveis pra evitar explosão.
    """
    children_by_tag_class: dict = {}
    for child in el.find_all(recursive=False):
        if not _eligible_repeat_child(child):
            continue
        children_by_tag_class.setdefault(_group_key(child), []).append(child)

    groups = [g for g in children_by_tag_class.values() if len(g) >= 2]
    if groups:
        return max(groups, key=len)

    # Busca descendentes com limite de profundidade
    for container in _iter_descendants_bounded(el, max_depth=MAX_REPEAT_DEPTH):
        if container.name not in ("div", "ul", "ol", "section", "article"):
            continue
        kids = [k for k in container.find_all(recursive=False) if _eligible_repeat_child(k)]
        if len(kids) < 2:
            continue
        first_key = _group_key(kids[0])
        if all(_group_key(k) == first_key for k in kids):
            return kids

    return []


def describe_section(sem_type, el, text_sample):
    """Gera descrição em linguagem natural pra mostrar ao membro."""
    imgs = extract_images_in_section(el)
    img_count = len(imgs)
    has_h1 = bool(el.find("h1"))
    has_h2 = bool(el.find("h2"))
    has_cta = bool(el.find("a", class_=lambda c: c and any(w in " ".join(c).lower() for w in ("btn", "button", "cta"))))
    repeating = extract_repeating_pattern(el)
    repeat_count = len(repeating)

    bits = []
    if sem_type != "unknown":
        bits.append(sem_type.capitalize())
    if has_h1:
        bits.append("com H1")
    elif has_h2:
        bits.append("com H2")
    if img_count:
        bits.append(f"{img_count} imagem(ns)")
    if has_cta:
        bits.append("CTA")
    if repeat_count >= 2:
        bits.append(f"{repeat_count} itens repetíveis")
    if text_sample:
        snippet = text_sample[:80].strip()
        if snippet:
            bits.append(f'texto: "{snippet}..."')

    return " · ".join(bits) if bits else "seção genérica"


# --------------------- hierarquia visual (computed-styles) ------------------ #
#
# O skeleton do clone-and-adapt preservava só ordem + tipo + grid coarse — e
# perdia a hierarquia visual que fazia a página converter (um hero com H1 3.2x
# o body e 120px de respiro não é o mesmo hero com H1 1.4x e 24px). Estes
# helpers extraem, POR SECTION, sinais numéricos de hierarquia a partir do
# computed-styles.json do downloader. São PROPORÇÕES e medidas espaciais —
# nenhum hex, nenhuma fonte, nenhum texto do concorrente.

_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
_TEXT_TAGS = {"p", "li", "blockquote", "a", "span", "button", "label", "figcaption", "td", "th"}
_MEDIA_TAGS = {"img", "picture", "video", "svg", "iframe"}

# Tags que o matcher por tag-solto aceita (sections sem id nem classe).
_BARE_SECTION_TAGS = ("header", "footer", "main", "section", "article", "aside")

_PX_RE = re.compile(r"(-?\d+(?:\.\d+)?)px")


def _parse_px(value):
    """'64px' → 64.0; None se não parseável."""
    if not value:
        return None
    m = _PX_RE.match(str(value).strip())
    return float(m.group(1)) if m else None


def _parse_padding_block(padding_shorthand):
    """Computed 'padding' shorthand → (top_px, bottom_px). Ex: '64px 20px' → (64, 64)."""
    if not padding_shorthand:
        return (None, None)
    parts = [_parse_px(p) for p in str(padding_shorthand).split()]
    if not parts or any(p is None for p in parts):
        return (None, None)
    if len(parts) <= 2:
        return (parts[0], parts[0])
    # 3 ou 4 valores: top é o 1º, bottom é o 3º
    return (parts[0], parts[2])


def _norm_align(value):
    v = (value or "").strip().lower()
    if v in ("start",):
        return "left"
    if v in ("end",):
        return "right"
    if v in ("left", "right", "center", "justify"):
        return v
    return None


def _load_computed_styles(clone_dir: Path):
    """Lê computed-styles.json (só existe quando a captura veio do downloader)."""
    p = clone_dir / "computed-styles.json"
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, list) and data else None


def _match_section_to_computed(el, computed, used, min_index):
    """Encontra a entrada do computed-styles que corresponde ao `el` do soup.

    Precedência: (tag, id) → (tag, classes exatas) → tag solto (só pra tags
    estruturais bare tipo <footer>). Greedy em ordem de documento: prefere o
    primeiro candidato não-usado com index > min_index (as sections do soup e
    as entradas do computed estão ambas em ordem de documento).
    """
    tag = el.name
    el_id = el.get("id") or None
    classes = tuple(sorted(el.get("class", []) or []))

    def _first_free(pred):
        return [c for c in computed if c.get("index") not in used and pred(c)]

    cands = []
    if el_id:
        cands = _first_free(lambda c: c.get("tag") == tag and (c.get("id") or None) == el_id)
    if not cands and classes:
        cands = _first_free(
            lambda c: c.get("tag") == tag and tuple(sorted(c.get("classes") or [])) == classes
        )
    if not cands and not classes and tag in _BARE_SECTION_TAGS:
        cands = _first_free(lambda c: c.get("tag") == tag and not (c.get("classes") or []))
    if not cands:
        return None
    after = [c for c in cands if c.get("index", -1) > min_index]
    return after[0] if after else cands[0]


def extract_hierarchy_signals(el, computed, used, min_index):
    """Sinais de hierarquia visual da section, agregados do computed-styles.

    Retorna (dict|None, novo_min_index). Todos os valores são numéricos/
    categóricos agregados (proporções, px de espaçamento, densidade) —
    zero conteúdo do concorrente.
    """
    cand = _match_section_to_computed(el, computed, used, min_index)
    if cand is None:
        return None, min_index
    idx = cand.get("index", min_index)
    used.add(idx)

    rect = cand.get("rect") or {}
    top = float(rect.get("top") or 0)
    height = float(rect.get("height") or 0)
    width = float(rect.get("width") or 0)
    if height <= 1:
        return None, idx
    bottom = top + height

    # Pool = descendentes visuais: entradas DEPOIS da section em ordem de
    # documento cujo topo cai dentro da faixa vertical dela.
    pool = []
    for c in computed:
        if c.get("index", -1) <= idx:
            continue
        r = c.get("rect") or {}
        c_top = r.get("top")
        if c_top is None:
            continue
        if top - 2 <= float(c_top) < bottom - 1:
            pool.append(c)

    heading_px: dict = {}
    body_sizes: list = []
    align_counts: dict = {}
    media_area = 0.0
    text_count = 0
    media_count = 0
    content_count = 0

    for c in pool:
        tag = c.get("tag") or ""
        styles = c.get("styles") or {}
        r = c.get("rect") or {}
        fs = _parse_px(styles.get("font-size"))
        if tag in _HEADING_TAGS:
            content_count += 1
            text_count += 1
            if fs:
                heading_px[tag] = max(heading_px.get(tag, 0.0), fs)
        elif tag in _TEXT_TAGS:
            content_count += 1
            text_count += 1
            if fs:
                body_sizes.append(fs)
        elif tag in _MEDIA_TAGS:
            content_count += 1
            media_count += 1
            media_area += float(r.get("width") or 0) * float(r.get("height") or 0)
        else:
            continue
        ta = _norm_align(styles.get("text-align"))
        if ta and tag not in _MEDIA_TAGS:
            align_counts[ta] = align_counts.get(ta, 0) + 1

    body_px = round(statistics.median(body_sizes), 1) if body_sizes else None
    h1_px = heading_px.get("h1")
    h2_px = heading_px.get("h2")
    max_heading_px = max(heading_px.values()) if heading_px else None

    def _ratio(a, b):
        return round(a / b, 2) if a and b else None

    pad_top, pad_bottom = _parse_padding_block((cand.get("styles") or {}).get("padding"))

    density_val = round(content_count / height * 1000, 1)
    if density_val < 8:
        density_label = "airy"
    elif density_val <= 20:
        density_label = "medium"
    else:
        density_label = "dense"

    section_area = width * height
    media_ratio = (
        round(min(1.0, media_area / section_area), 2) if section_area > 0 else None
    )

    return {
        "source": "computed-styles",
        "section_height_px": round(height),
        "font_scale": {
            "h1_px": h1_px,
            "h2_px": h2_px,
            "body_px": body_px,
            "h1_to_body": _ratio(h1_px, body_px),
            "h2_to_body": _ratio(h2_px, body_px),
            "heading_to_body": _ratio(max_heading_px, body_px),
        },
        "padding_block_px": {"top": pad_top, "bottom": pad_bottom},
        "density": {
            "content_elements": content_count,
            "per_1000px": density_val,
            "label": density_label,
        },
        "dominant_alignment": (
            max(align_counts.items(), key=lambda kv: kv[1])[0] if align_counts else None
        ),
        "media_text_balance": {
            "media_area_ratio": media_ratio,
            "text_elements": text_count,
            "media_elements": media_count,
        },
    }, idx


def _load_source_url(clone_dir: Path):
    """URL de origem gravada pelo downloader (meta.json) — normaliza srcs relativos."""
    meta_path = clone_dir / "meta.json"
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text(encoding="utf-8")).get("url")
    except (OSError, json.JSONDecodeError, AttributeError):
        return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 analyzer.py <clone_dir>", file=sys.stderr)
        sys.exit(1)

    clone_dir = Path(sys.argv[1]).expanduser().resolve()
    html_path = clone_dir / "page.html"
    styles_path = clone_dir / "styles.css"
    images_json_path = clone_dir / "images.json"

    if not html_path.exists():
        print(f"ERRO: {html_path} não encontrado. Rode downloader.py primeiro.", file=sys.stderr)
        sys.exit(1)

    print(f"[analyzer] lendo {html_path}")
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    css_text = styles_path.read_text(encoding="utf-8") if styles_path.exists() else ""
    images_map = json.loads(images_json_path.read_text(encoding="utf-8")) if images_json_path.exists() else {}
    source_url = _load_source_url(clone_dir)

    computed_styles = _load_computed_styles(clone_dir)
    if computed_styles:
        print(f"[analyzer] computed-styles.json: {len(computed_styles)} elementos — extraindo hierarquia por section")
    else:
        print("[analyzer] sem computed-styles.json (engine singlefile/--from-file) — hierarchy=null")

    body = soup.body or soup
    sections = []
    seen_ids = set()
    matched_computed: set = set()
    last_computed_index = -1

    for el in body.find_all(True, recursive=True):
        if not is_sectionable(el):
            continue
        # Wrapper <main> (tema Shopify) é atravessado — as sections reais são
        # os filhos dele, não ele.
        if _is_wrapper_container(el):
            continue
        el_key = id(el)
        if el_key in seen_ids:
            continue
        ancestor_covered = False
        for ancestor in el.parents:
            if id(ancestor) in seen_ids and is_sectionable(ancestor):
                ancestor_covered = True
                break
        if ancestor_covered:
            continue
        seen_ids.add(el_key)

        text_sample = get_text_sample(el)
        sem_type, confidence = score_semantic_type(
            el.name,
            el.get("class", []),
            el.get("id"),
            el.get("aria-label"),
            text_sample,
            el=el,
        )
        images = extract_images_in_section(el)
        for img in images:
            # images.json guarda URLs ABSOLUTAS (urljoin do downloader); o src
            # do soup é o atributo cru (relativo em loja real: //cdn... ou
            # /cdn/shop/...). Normaliza com a URL de origem antes do lookup.
            candidates = [img["src"]]
            if source_url:
                candidates.append(urljoin(source_url, img["src"]))
            for key in candidates:
                if key in images_map:
                    img["local_path"] = images_map[key]
                    break
        repeating = extract_repeating_pattern(el)

        hierarchy = None
        if computed_styles:
            hierarchy, last_computed_index = extract_hierarchy_signals(
                el, computed_styles, matched_computed, last_computed_index
            )

        sections.append({
            "index": len(sections) + 1,
            "semantic_type": sem_type,
            "confidence": round(min(1.0, max(0.0, confidence)), 2),
            "tag": el.name,
            "id": el.get("id"),
            "classes": el.get("class", []),
            "html": str(el),
            "text_sample": text_sample,
            "images": images,
            "repeating_pattern": {
                "detected": len(repeating) >= 2,
                "count": len(repeating),
                "child_tag": repeating[0].name if repeating else None,
                "child_classes": repeating[0].get("class", []) if repeating else [],
            },
            "hierarchy": hierarchy,
            "description": describe_section(sem_type, el, text_sample),
        })

    output = {
        "source_dir": str(clone_dir),
        "source_url": source_url,
        "total_sections": len(sections),
        "sections": sections,
        "stylesheet_length": len(css_text),
        "images_count": len(images_map),
        "computed_styles_available": bool(computed_styles),
        "hierarchy_sections": sum(1 for s in sections if s.get("hierarchy")),
    }
    out_path = clone_dir / "sections.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"[analyzer] {len(sections)} seções identificadas")
    for s in sections:
        print(f"  {s['index']}. {s['semantic_type']} (conf {s['confidence']}) — {s['description']}")
    if computed_styles:
        print(f"[analyzer] hierarquia visual extraída em {output['hierarchy_sections']}/{len(sections)} sections")
    print(f"[analyzer] sections.json salvo em {out_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[analyzer] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
