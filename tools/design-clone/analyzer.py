#!/usr/bin/env python3
"""
analyzer.py — Aura Engine design-clone pipeline (step 2 of 3)

Lê o output do downloader.py e identifica as seções semanticamente (hero,
features, benefits, testimonials, faq, pricing, footer, etc). Retorna
sections.json com HTML + CSS + metadados de cada seção pra o liquid-converter.py
(step 3) consumir.

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

try:
    from bs4 import BeautifulSoup, NavigableString
except ImportError:
    print("ERRO: BeautifulSoup4 não instalado. Rode: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


# Heurísticas por tipo semântico. Cada entrada = lista de palavras-chave em
# class/id/tag/aria-label que indicam o tipo. Match case-insensitive.
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


def score_semantic_type(tag, classes, section_id, aria_label, text_sample):
    """Retorna (tipo, confiança 0-1) baseado em heurísticas."""
    haystack = " ".join([
        (tag or "").lower(),
        " ".join(classes or []).lower(),
        (section_id or "").lower(),
        (aria_label or "").lower(),
    ])
    scores = {}
    for sem_type, hints in SEMANTIC_HINTS.items():
        s = 0
        for hint in hints:
            if hint in haystack:
                s += 1
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
    classes = " ".join(el.get("class", [])).lower()
    id_attr = (el.get("id") or "").lower()
    for hints in SEMANTIC_HINTS.values():
        for hint in hints:
            if hint in classes or hint in id_attr:
                return True
    return False


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


def _iter_descendants_bounded(el, max_depth: int = MAX_REPEAT_DEPTH):
    """Itera descendentes de `el` até `max_depth` níveis (helper anti-explosão)."""
    def _walk(node, depth):
        if depth >= max_depth:
            return
        for child in node.find_all(recursive=False):
            yield child
            yield from _walk(child, depth + 1)

    yield from _walk(el, 0)


def extract_repeating_pattern(el):
    """
    Detecta padrões repetíveis (features, testimonials, faq items).
    Retorna lista de elementos filhos com mesma estrutura, ou [] se não houver.
    Procura recursivamente até `MAX_REPEAT_DEPTH` (3) níveis pra evitar explosão.
    """
    children_by_tag_class: dict = {}
    for child in el.find_all(recursive=False):
        key = (child.name, " ".join(sorted(child.get("class", []))))
        children_by_tag_class.setdefault(key, []).append(child)

    for _, group in children_by_tag_class.items():
        if len(group) >= 2:
            return group

    # Busca descendentes com limite de profundidade
    for container in _iter_descendants_bounded(el, max_depth=MAX_REPEAT_DEPTH):
        if container.name not in ("div", "ul", "ol", "section", "article"):
            continue
        kids = container.find_all(recursive=False)
        if len(kids) < 2:
            continue
        first_key = (kids[0].name, " ".join(sorted(kids[0].get("class", []))))
        if all((k.name, " ".join(sorted(k.get("class", [])))) == first_key for k in kids):
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

    body = soup.body or soup
    sections = []
    seen_ids = set()

    for el in body.find_all(True, recursive=True):
        if not is_sectionable(el):
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
            if img["src"] in images_map:
                img["local_path"] = images_map[img["src"]]
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
