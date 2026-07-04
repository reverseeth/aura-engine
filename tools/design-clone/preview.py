#!/usr/bin/env python3
"""
preview.py — Renderiza um .liquid gerado pelo liquid-converter como HTML standalone.

O arquivo .liquid normalmente só funciona dentro de um tema Shopify. Este script
lê a section, extrai os defaults do {% schema %}, substitui {{ section.settings.X }}
pelos valores default, expande os blocks LOCAIS do schema ({% for block in
section.blocks %} + {% case block.type %} — uma instância por entrada do preset,
com a copy real), resolve {% if %}/{% else %} com comparações (== / != blank /
== 'valor'), injeta o CSS, e gera um HTML standalone pra visualização no browser.

Imagens: {{ ... | image_url | image_tag }} vira <img> com placeholder; se
--images-dir tiver arquivos (ou --images-json tiver URLs), eles são usados em
rotação no lugar do placeholder.

Uso:
    python3 preview.py \\
        --section <path.liquid> \\
        --styles <path/page.css> \\
        --images-dir <path/images> \\
        --images-json <path/images.json> \\
        --output <preview.html> \\
        [--blocks-dir <path>]        # legacy: blocks antigos em arquivos separados
        [--blocks-count 3]           # instâncias quando o schema não tem preset

Exemplo:
    python3 preview.py \\
        --section /tmp/liquid-test/sections/page-mybrand-hero.liquid \\
        --output /tmp/preview.html

Depois:
    open /tmp/preview.html
"""

import argparse
import json
import logging
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

# Módulo compartilhado (consolidação do CSS rewrite antes duplicado)
try:
    from _css_utils import rewrite_css_for_namespace
except ImportError:
    _THIS_DIR = Path(__file__).resolve().parent
    if str(_THIS_DIR) not in sys.path:
        sys.path.insert(0, str(_THIS_DIR))
    from _css_utils import rewrite_css_for_namespace  # noqa: E402


logger = logging.getLogger("design_clone.preview")
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


SECTION_SPLIT_RE = re.compile(r"\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}", re.DOTALL)
STYLESHEET_RE = re.compile(r"\{%\s*stylesheet\s*%\}(.*?)\{%\s*endstylesheet\s*%\}", re.DOTALL)
CONTENT_FOR_BLOCKS_RE = re.compile(r"\{%\s*content_for\s+['\"]blocks['\"]\s*%\}")
FOR_BLOCKS_RE = re.compile(r"\{%\s*for\s+block\s+in\s+section\.blocks\s*%\}(.*?)\{%\s*endfor\s*%\}", re.DOTALL)
CASE_BLOCK_RE = re.compile(r"\{%\s*case\s+block\.type\s*%\}(.*?)\{%\s*endcase\s*%\}", re.DOTALL)
WHEN_SPLIT_RE = re.compile(r"\{%\s*when\s+['\"]([^'\"]+)['\"]\s*%\}")
SHOPIFY_ATTRS_RE = re.compile(r"\{\{\s*block\.shopify_attributes\s*\}\}")

# Token intermediário: {{ x | image_url | image_tag }} vira <img src="TOKEN">, e o
# passo final troca cada TOKEN por imagem local (--images-dir), URL (--images-json)
# ou um SVG placeholder inline.
IMG_PLACEHOLDER_TOKEN = "__AURA_IMG_PLACEHOLDER__"
PLACEHOLDER_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='800' height='500'>"
    "<rect width='100%' height='100%' fill='#e8e6e1'/></svg>"
)
PLACEHOLDER_DATA_URI = "data:image/svg+xml;charset=utf-8," + quote(PLACEHOLDER_SVG, safe="")


def _settings_var_re(scope: str) -> re.Pattern:
    return re.compile(r"\{\{\s*" + scope + r"\.settings\.(\w+)(?:\s*\|\s*([^}]+?))?\s*\}\}")


def _if_block_re(scope: str) -> re.Pattern:
    """Regex do if INNERMOST (corpo sem if/else/endif aninhado) — aplicado em loop
    até estabilizar, resolve aninhamento de dentro pra fora. Suporta:
    {% if x %} · {% if x == 'v' %} · {% if x != blank %} · branch {% else %}."""
    return re.compile(
        r"\{%\s*if\s+" + scope + r"\.settings\.(\w+)\s*"
        r"(?:(==|!=)\s*(blank|'[^']*'|\"[^\"]*\"))?\s*%\}"
        r"((?:(?!\{%\s*(?:if|else|endif)\b).)*?)"
        r"(?:\{%\s*else\s*%\}((?:(?!\{%\s*(?:if|endif)\b).)*?))?"
        r"\{%\s*endif\s*%\}",
        re.DOTALL,
    )


def _path_allowlist() -> list[Path]:
    """Allowlist para paths de input/output (anti path-traversal)."""
    roots: list[Path] = [
        Path(tempfile.gettempdir()).resolve(),
        Path("/tmp").resolve(),  # macOS: TMPDIR aponta pra /var/folders, mas o staging usual é /tmp
        Path.cwd().resolve(),
        # workspace derivado do próprio repo (funciona em qualquer path de clone)
        (Path(__file__).resolve().parents[2] / "workspace").resolve(),
    ]
    home = os.environ.get("HOME")
    if home:
        roots.append((Path(home) / "aura-engine" / "workspace").resolve())
    seen: set[str] = set()
    out: list[Path] = []
    for r in roots:
        if str(r) not in seen:
            seen.add(str(r))
            out.append(r)
    return out


def validate_path(path_str: str, must_exist: bool = False) -> Path:
    """Resolve e valida path dentro da allowlist."""
    if not path_str:
        raise ValueError("Path vazio")
    candidate = Path(path_str).expanduser().resolve()
    allowed = _path_allowlist()
    for root in allowed:
        try:
            candidate.relative_to(root)
            if must_exist and not candidate.exists():
                raise ValueError(f"Path {candidate!r} não existe")
            return candidate
        except ValueError as exc:
            if "não existe" in str(exc):
                raise
            continue
    raise ValueError(
        f"Path {candidate!r} fora da allowlist. Permitido em: "
        + ", ".join(str(p) for p in allowed)
    )


def parse_liquid_file(liquid_path):
    """Lê um arquivo .liquid e retorna (markup, stylesheet, schema_dict)."""
    content = liquid_path.read_text(encoding="utf-8")

    schema_match = SECTION_SPLIT_RE.search(content)
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
    """Converte lista de settings do schema em dict {id: {type, default}}.

    Entradas sem id (type: header/paragraph) são puladas — o conversor SEMPRE
    emite headers de grupo ('Colors', 'Design tokens', por imagem)."""
    out = {}
    for s in settings or []:
        if not isinstance(s, dict):
            continue
        sid = s.get("id")
        if not sid:
            continue
        out[sid] = {"type": s.get("type"), "default": s.get("default", "")}
    return out


def apply_settings(markup, defaults, scope="section"):
    """Substitui {{ scope.settings.X }} e resolve {% if scope.settings.X ... %} pelos defaults."""

    def _resolve_if(m):
        sid, op, rhs = m.group(1), m.group(2), m.group(3)
        inner = m.group(4)
        else_part = m.group(5) or ""
        entry = defaults.get(sid) or {}
        default = entry.get("default") or ""
        # image_picker sem comparação: preview sempre mostra o placeholder
        if entry.get("type") == "image_picker" and not op:
            return inner
        if op:
            if rhs == "blank":
                is_blank = str(default).strip() == ""
                truthy = is_blank if op == "==" else not is_blank
            else:
                rhs_val = rhs[1:-1]  # tira as aspas
                truthy = (str(default) == rhs_val) if op == "==" else (str(default) != rhs_val)
        else:
            truthy = bool(default)
        return inner if truthy else else_part

    # Innermost-first em loop: resolve ifs aninhados de dentro pra fora.
    if_re = _if_block_re(scope)
    prev = None
    while prev != markup:
        prev = markup
        markup = if_re.sub(_resolve_if, markup)

    def replace_var(m):
        sid = m.group(1)
        filters = (m.group(2) or "").strip()
        entry = defaults.get(sid)
        if entry is None:
            return ""
        default = entry.get("default") or ""
        s_type = entry.get("type")

        if s_type == "image_picker":
            # | image_tag produz um <img> no Shopify — o preview emite um <img>
            # de verdade (com a classe do image_tag) apontando pro token.
            if "image_tag" in filters:
                cls_m = re.search(r"class:\s*'([^']*)'", filters)
                cls = f' class="{cls_m.group(1)}"' if cls_m else ""
                return f'<img src="{IMG_PLACEHOLDER_TOKEN}" alt=""{cls}>'
            return IMG_PLACEHOLDER_TOKEN
        if not default and "default:" in filters:
            dm = re.search(r"default:\s*'([^']*)'", filters)
            if dm:
                default = dm.group(1)
        if s_type == "url":
            return str(default) if default else "#"
        return str(default)

    markup = _settings_var_re(scope).sub(replace_var, markup)
    if scope == "block":
        markup = SHOPIFY_ATTRS_RE.sub("", markup)
    return markup


def expand_inline_blocks(markup, schema, blocks_count):
    """Expande {% for block in section.blocks %} + {% case block.type %} usando os
    blocks LOCAIS do schema.

    Instâncias vêm de presets[0].blocks (copy real por instância, como o conversor
    emite); sem preset, renderiza `blocks_count` instâncias com os defaults."""
    block_defs = {}
    for bd in schema.get("blocks", []) or []:
        if isinstance(bd, dict) and bd.get("type"):
            block_defs[bd["type"]] = settings_to_defaults(bd.get("settings", []))
    if not block_defs:
        return markup

    presets = schema.get("presets") or []
    preset_blocks = []
    if presets and isinstance(presets[0], dict):
        preset_blocks = presets[0].get("blocks") or []

    instances = []
    for pb in preset_blocks:
        if not isinstance(pb, dict):
            continue
        t = pb.get("type")
        if t not in block_defs:
            continue
        merged = {sid: dict(entry) for sid, entry in block_defs[t].items()}
        for sid, val in (pb.get("settings") or {}).items():
            base = merged.get(sid, {"type": None, "default": ""})
            merged[sid] = {**base, "default": val}
        instances.append((t, merged))
    if not instances:
        for t, defs in block_defs.items():
            instances.extend((t, defs) for _ in range(blocks_count))

    def _expand(m):
        body = m.group(1)
        case_m = CASE_BLOCK_RE.search(body)
        rendered = []
        for t, defaults in instances:
            if case_m:
                parts = WHEN_SPLIT_RE.split(case_m.group(1))
                # parts = [prefixo, type1, corpo1, type2, corpo2, ...]
                chosen = ""
                for k in range(1, len(parts), 2):
                    if parts[k] == t:
                        chosen = parts[k + 1]
                        break
                inst_markup = body[:case_m.start()] + chosen + body[case_m.end():]
            else:
                inst_markup = body
            rendered.append(apply_settings(inst_markup, defaults, scope="block"))
        return "\n".join(rendered)

    return FOR_BLOCKS_RE.sub(_expand, markup)


def inject_image_url_placeholders(markup, images_url_map, images_dir):
    """Troca cada token de imagem por: arquivo local (--images-dir) → URL do
    images.json (--images-json) → SVG placeholder inline (sempre renderiza algo)."""
    sources: list[str] = []
    if images_dir and images_dir.is_dir():
        sources = [f"file://{p}" for p in sorted(images_dir.glob("*")) if p.is_file()]
    if not sources and images_url_map:
        candidates = []
        if isinstance(images_url_map, dict):
            candidates = list(images_url_map.values())
        elif isinstance(images_url_map, list):
            candidates = images_url_map
        for c in candidates:
            if isinstance(c, str) and c:
                sources.append(c)
            elif isinstance(c, dict):
                u = c.get("url") or c.get("src")
                if u:
                    sources.append(u)

    counter = [0]

    def _next(_m):
        if not sources:
            return PLACEHOLDER_DATA_URI
        s = sources[counter[0] % len(sources)]
        counter[0] += 1
        return s

    return re.sub(re.escape(IMG_PLACEHOLDER_TOKEN), _next, markup)


def render_blocks(blocks_dir, namespace, count):
    """LEGACY: renderiza N instâncias de cada block em arquivo separado
    (outputs antigos do conversor, pré-blocks-inline)."""
    if not blocks_dir or not blocks_dir.exists():
        return ""

    rendered = []
    block_files = sorted(blocks_dir.glob(f"{namespace}-*.liquid"))
    for block_file in block_files:
        markup, _, schema = parse_liquid_file(block_file)
        defaults = settings_to_defaults(schema.get("settings", []))
        for _ in range(count):
            # Arquivos legados referenciam section.settings dentro do block.
            instance = apply_settings(markup, defaults, scope="section")
            instance = apply_settings(instance, defaults, scope="block")
            rendered.append(instance)

    return "\n".join(rendered)


def detect_namespace(schema):
    cls = schema.get("class", "")
    parts = cls.split()
    for p in parts:
        if "__" not in p and "--" not in p:
            return p
    return "page-preview"


def build_html(markup, stylesheet, external_css_path, namespace):
    external_css = ""
    if external_css_path and external_css_path.exists():
        raw = external_css_path.read_text(encoding="utf-8")
        external_css = rewrite_css_for_namespace(raw, namespace)

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

/* CSS externo opcional (escopo global — pode conflitar) */
{external_css}

/* CSS da section gerada */
{stylesheet}

/* Placeholder pra imagens faltantes */
img[src=""], img:not([src]) {{ display: none; }}
.icon-placeholder, [class*='icon_placeholder'] {{ display: inline-block; width: 1em; height: 1em; background: #ccc; border-radius: 2px; }}
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
    parser.add_argument("--blocks-dir", default=None, help="(legacy) Directory with block .liquid files")
    parser.add_argument("--styles", default=None, help="Path to external page CSS (optional)")
    parser.add_argument("--images-dir", default=None, help="Directory with downloaded images")
    parser.add_argument("--images-json", default=None, help="images.json from downloader (map/list of URLs)")
    parser.add_argument("--output", required=True, help="Path to output .html")
    parser.add_argument("--blocks-count", type=int, default=3,
                        help="Block instances to render when schema has no preset (default 3)")
    args = parser.parse_args()

    # Validação uniforme de paths (mesma allowlist pra todos os args de path).
    try:
        section_path = validate_path(args.section, must_exist=True)
    except ValueError as exc:
        print(f"ERRO: --section inválido: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        markup, stylesheet, schema = parse_liquid_file(section_path)
    except json.JSONDecodeError as exc:
        print(
            f"ERRO: schema inválido em {section_path} (linha {exc.lineno} col {exc.colno}): {exc.msg}",
            file=sys.stderr,
        )
        sys.exit(1)
    defaults = settings_to_defaults(schema.get("settings", []))

    images_dir = None
    if args.images_dir:
        try:
            images_dir = validate_path(args.images_dir, must_exist=False)
        except ValueError as exc:
            print(f"ERRO: --images-dir inválido: {exc}", file=sys.stderr)
            sys.exit(1)
        if not images_dir.is_dir():
            images_dir = None

    images_url_map: dict = {}
    if args.images_json:
        try:
            p = validate_path(args.images_json, must_exist=False)
        except ValueError as exc:
            print(f"ERRO: --images-json inválido: {exc}", file=sys.stderr)
            sys.exit(1)
        if p.exists():
            try:
                images_url_map = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(
                    f"ERRO: JSON inválido em {p} (linha {exc.lineno} col {exc.colno}): {exc.msg}",
                    file=sys.stderr,
                )
                sys.exit(1)

    # 1) Blocks inline PRIMEIRO ({% if block.settings %} tem que resolver com o
    #    escopo do block, não com os defaults da section).
    markup_filled = expand_inline_blocks(markup, schema, args.blocks_count)

    # 2) Legacy: {% content_for 'blocks' %} + arquivos em --blocks-dir.
    if args.blocks_dir and CONTENT_FOR_BLOCKS_RE.search(markup_filled):
        try:
            blocks_dir = validate_path(args.blocks_dir, must_exist=False)
        except ValueError as exc:
            print(f"ERRO: --blocks-dir inválido: {exc}", file=sys.stderr)
            sys.exit(1)
        namespace = detect_namespace(schema)
        blocks_markup = render_blocks(blocks_dir, namespace, args.blocks_count)
        markup_filled = CONTENT_FOR_BLOCKS_RE.sub(lambda _: blocks_markup, markup_filled)

    # 3) Settings da section.
    markup_filled = apply_settings(markup_filled, defaults, scope="section")

    # 4) Imagens (tokens → local files / URLs / SVG placeholder).
    markup_filled = inject_image_url_placeholders(markup_filled, images_url_map, images_dir)

    external_css = None
    if args.styles:
        try:
            external_css = validate_path(args.styles, must_exist=False)
        except ValueError as exc:
            print(f"ERRO: --styles inválido: {exc}", file=sys.stderr)
            sys.exit(1)
    namespace = detect_namespace(schema)

    html = build_html(markup_filled, stylesheet, external_css, namespace)
    try:
        output_path = validate_path(args.output, must_exist=False)
    except ValueError as exc:
        print(f"ERRO: --output inválido: {exc}", file=sys.stderr)
        sys.exit(1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    n_block_defs = len(schema.get("blocks", []) or [])
    print(f"[preview] gerado: {output_path}")
    print(f"[preview] settings aplicados: {len(defaults)} · block types no schema: {n_block_defs}")
    print(f"[preview] abra no browser:")
    print(f"  open {output_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[preview] interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        logger.error("falha inesperada: %s", exc)
        sys.exit(1)
