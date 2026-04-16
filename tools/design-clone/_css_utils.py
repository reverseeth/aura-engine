#!/usr/bin/env python3
"""
_css_utils.py — Shared CSS rewrite utilities for design-clone pipeline.

Consolida o `rewrite_css_for_namespace` que antes estava duplicado em
`liquid-converter.py` e `preview.py`. Inclui proteção contra recursão infinita
e tratamento correto de at-rules (@media, @supports, @keyframes).
"""

from __future__ import annotations

import re


HEX_COLOR_RE_VALIDATE = re.compile(r"^[0-9a-fA-F]{3,8}$")
CSS_CLASS_SELECTOR_RE = re.compile(r"\.([a-zA-Z_][\w-]*)")
CSS_ID_SELECTOR_RE = re.compile(r"#([a-zA-Z_][\w-]*)")

# At-rules cujo bloco interno contém regras CSS aninhadas (precisam recursão).
NESTED_AT_RULES = ("@media", "@supports", "@document", "@container")
# At-rules cujo bloco interno NÃO é CSS regular (keyframes, font-face) — não
# devemos reescrever selectors dentro deles.
OPAQUE_AT_RULES = ("@keyframes", "@-webkit-keyframes", "@font-face", "@page", "@counter-style")


def _slugify(text: str, max_len: int = 40) -> str:
    """Slugify consistente com liquid-converter.py."""
    s = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return s[:max_len] or "field"


def rewrite_css_for_namespace(css: str, namespace: str, max_depth: int = 5) -> str:
    """
    Reescreve classes e IDs nos selectors do CSS pra casar com o namespace
    aplicado no HTML. Só mexe em selectors (antes do `{`), não em valores.

    - `@media`, `@supports`, `@container`, `@document`: recursão no conteúdo interno.
    - `@keyframes`, `@font-face`, `@page`, `@counter-style`: preserva conteúdo
      interno sem rewrite (são opacos para selector rewriting).
    - `max_depth` protege contra loops infinitos em CSS mal-formado.
    """
    if not css or not namespace:
        return css
    if max_depth <= 0:
        return css

    def rewrite_selector_text(selector_text: str) -> str:
        def class_sub(m: re.Match) -> str:
            return f".{namespace}__{_slugify(m.group(1))}"

        def id_sub(m: re.Match) -> str:
            ident = m.group(1)
            if HEX_COLOR_RE_VALIDATE.match(ident) and len(ident) in (3, 4, 6, 8):
                return m.group(0)
            return f"#{namespace}-{_slugify(ident)}"

        result = CSS_CLASS_SELECTOR_RE.sub(class_sub, selector_text)
        result = CSS_ID_SELECTOR_RE.sub(id_sub, result)
        return result

    out: list[str] = []
    i = 0
    n = len(css)
    while i < n:
        brace = css.find("{", i)
        if brace == -1:
            out.append(css[i:])
            break

        selector_part = css[i:brace]
        stripped = selector_part.lstrip()
        is_at_rule = stripped.startswith("@")
        at_rule_name = ""
        if is_at_rule:
            match = re.match(r"@[\w-]+", stripped)
            at_rule_name = match.group(0).lower() if match else ""

        # Encontra o `}` correspondente respeitando aninhamento
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

        if is_at_rule:
            out.append(selector_part)
            out.append("{")
            if at_rule_name in OPAQUE_AT_RULES:
                out.append(block_content)
            elif at_rule_name in NESTED_AT_RULES:
                out.append(rewrite_css_for_namespace(block_content, namespace, max_depth - 1))
            else:
                # Desconhecido — seguro não mexer.
                out.append(block_content)
        else:
            out.append(rewrite_selector_text(selector_part))
            out.append("{")
            out.append(block_content)

        out.append("}")
        i = j
    return "".join(out)


__all__ = ["rewrite_css_for_namespace"]
