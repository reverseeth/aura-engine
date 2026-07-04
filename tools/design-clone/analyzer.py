#!/usr/bin/env python3
"""
analyzer.py — Aura Engine design-clone pipeline (passo 2)

Lê o output do downloader.py e identifica as seções semanticamente (hero,
features, benefits, testimonials, faq, pricing, footer, etc). Retorna
sections.json, consumido pelos dois caminhos do aura_clone.py:
o pattern-extractor.py (modo signals) e o skeleton-builder in-process
(modo clone-and-adapt).

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
SEMANTIC_HINTS = {
    "hero": ["hero", "banner", "jumbotron", "masthead", "above-fold", "page-header", "intro"],
    "features": ["features", "benefits", "why", "how-it-works", "how-works", "advantages", "highlights", "perks"],
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


def score_semantic_type(tag, classes, section_id, aria_label, text_sample):
    """Retorna (tipo, confiança 0-1) baseado em heurísticas."""
    tokens, normed = _tokenize(tag, *(classes or []), section_id, aria_label)
    scores = {}
    for sem_type, hints in SEMANTIC_HINTS.items():
        s = sum(1 for hint in hints if _hint_matches(hint, tokens, normed))
        if s > 0:
            scores[sem_type] = s

    text_lower = (text_sample or "")[:200].lower()
    if "frequently asked" in text_lower or "perguntas frequentes" in text_lower:
        scores["faq"] = scores.get("faq", 0) + 2
    if "testimonial" in text_lower or "customers say" in text_lower or "reviews" in text_lower:
        scores["testimonials"] = scores.get("testimonials", 0) + 1
    if "pricing" in text_lower or "plans" in text_lower or "$" in text_lower[:50]:
        scores["pricing"] = scores.get("pricing", 0) + 1

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

    body = soup.body or soup
    sections = []
    seen_ids = set()

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
            "description": describe_section(sem_type, el, text_sample),
        })

    output = {
        "source_dir": str(clone_dir),
        "source_url": source_url,
        "total_sections": len(sections),
        "sections": sections,
        "stylesheet_length": len(css_text),
        "images_count": len(images_map),
    }
    out_path = clone_dir / "sections.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"[analyzer] {len(sections)} seções identificadas")
    for s in sections:
        print(f"  {s['index']}. {s['semantic_type']} (conf {s['confidence']}) — {s['description']}")
    print(f"[analyzer] sections.json salvo em {out_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[analyzer] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
