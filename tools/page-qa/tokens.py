#!/usr/bin/env python3
"""
tokens.py — tokens de design por código: page.html → design-tokens.json, DTCG do
dembrandt → brand-tokens.json, e drift entre dois arquivos de tokens.

Contrato de nomes (docs/designs/page-design-2.md, item 5): as variáveis do :root
`--color-<papel>` (8 papéis), `--font-heading`/`--font-body`, `--text-*`, `--space-*`,
`--radius-*`, `--shadow-*`; no brand-tokens.json, `color.<papel>`,
`typography.heading|body.fontFamily`, `dimension.*`, cada um com `$value`/`$type`, e o
`source` em `$extensions.aura.source`.

USO:
    tokens.py PAGE.html --out design-tokens.json --source ENUM [--preset-base ID]
              [--brand-out brand-tokens.json]
    tokens.py --from-dtcg dembrandt.json --brand-out brand-tokens.json
    tokens.py --diff A.json B.json
    tokens.py --diff-live computed.json design-tokens.json

Exit: 0 ok · 1 mais de 5 cores soltas fora das variáveis · 2 entrada inválida ·
      4 --brand-out recusado (a marca já existe).
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "design-clone"))
sys.path.insert(0, str(ROOT / ".claude" / "lib" / "design-presets"))
from _css_utils import CSS_COLOR_LITERAL_RE  # noqa: E402
import palette_engine as pe  # noqa: E402

ROLES = ("background", "surface", "foreground", "primary", "on_primary", "accent", "muted", "border")
SOURCES = ("dembrandt", "brand_tokens", "palette_engine", "refero", "manual")
MAX_LOOSE = 5
DTCG_ALIASES = {"text": "foreground", "on-primary": "on_primary", "onprimary": "on_primary"}


# ---------------------------------------------------------------- page.html

def root_vars(html):
    out = {}
    for block in re.findall(r":root\s*\{([^}]*)\}", html):
        for name, value in re.findall(r"--([\w-]+)\s*:\s*([^;]+);?", block):
            out[name] = value.strip()
    return out


def first_family(value):
    return value.split(",")[0].strip().strip("'\"") if value else None


def provision(fonts_block, family):
    if re.search(rf"@font-face[^}}]*{re.escape(family)}[^}}]*url\(", fonts_block, flags=re.I):
        return "local_files"
    if "fonts.googleapis" in fonts_block and family.replace(" ", "+") in fonts_block:
        return "google_fonts"
    return "system"


def loose_colors(html):
    css = " ".join(re.findall(r"<style(?![^>]*data-aura-fonts)[^>]*>(.*?)</style>", html, flags=re.S | re.I))
    css = re.sub(r"--[\w-]+\s*:[^;}]+", "", css)
    inline = " ".join(re.findall(r"(?:style|fill|stroke)=\"([^\"]*)\"", html))
    inline = re.sub(r"--[\w-]+\s*:[^;]+", "", inline)
    return CSS_COLOR_LITERAL_RE.findall(css + " " + inline)


def scale(vars_, prefix):
    return {k[len(prefix):]: v for k, v in vars_.items() if k.startswith(prefix)}


def from_page(html, source, preset_base, existing):
    v = root_vars(html)
    missing = [r for r in ROLES if f"color-{r.replace('_', '-')}" not in v]
    if missing:
        raise ValueError(f"papéis ausentes no :root: {', '.join(missing)}")
    fonts_block = " ".join(re.findall(r"<style[^>]*data-aura-fonts[^>]*>(.*?)</style>", html, flags=re.S | re.I))
    heading, body = first_family(v.get("font-heading")), first_family(v.get("font-body"))
    fams = []
    for name in dict.fromkeys(f for f in (heading, body) if f):
        role = "both" if heading == body else ("heading" if name == heading else "body")
        fams.append({"name": name, "role": role, "provision": provision(fonts_block, name),
                     "weights": sorted({int(w) for w in re.findall(
                         rf"{re.escape(name)}[^}}]*font-weight:\s*(\d+)", fonts_block)}) or [400],
                     "files_dir": "page/design/assets/fonts" if provision(fonts_block, name) == "local_files" else None})
    out = dict(existing)
    out.update({
        "colors": {r: v[f"color-{r.replace('_', '-')}"].lower() for r in ROLES},
        "type": {**existing.get("type", {}), "heading_font": v.get("font-heading"),
                 "body_font": v.get("font-body"), "families": fams, "scale": scale(v, "text-")},
        "spacing": {**existing.get("spacing", {}), "scale": scale(v, "space-")},
        "radii": scale(v, "radius-"),
        "shadow": scale(v, "shadow-"),
        "source": source,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    if preset_base:
        out["preset_base"] = preset_base
    return out


# ---------------------------------------------------------------- brand-tokens (DTCG)

def to_dtcg(colors, heading, body, source):
    return {
        "$schema": "https://www.designtokens.org/schemas/2025.10/format.json",
        "$extensions": {"aura": {"source": source}},
        "color": {r: {"$value": colors[r], "$type": "color"} for r in ROLES},
        "typography": {"heading": {"fontFamily": {"$value": heading, "$type": "fontFamily"}},
                       "body": {"fontFamily": {"$value": body, "$type": "fontFamily"}}},
    }


def flatten_colors(dtcg):
    """{nome normalizado: hex} de qualquer árvore DTCG (color.*.$value)."""
    out = {}

    def walk(node, path):
        if isinstance(node, dict):
            if "$value" in node and isinstance(node["$value"], str) and node["$value"].startswith("#"):
                key = path[-1].lower() if path else ""
                out[DTCG_ALIASES.get(key, key)] = node["$value"][:7].lower()
            for k, child in node.items():
                if not k.startswith("$"):
                    walk(child, path + [k])
    walk(dtcg.get("color", dtcg), [])
    return out


def from_dtcg(dtcg):
    found = flatten_colors(dtcg)
    colors = {r: found[r] for r in ROLES if r in found}
    if "primary" not in colors:
        raise ValueError("o DTCG não tem cor primary")
    bg = colors.setdefault("background", "#ffffff")
    colors.setdefault("foreground", "#111111" if pe.relative_luminance(bg) > 0.4 else "#f5f5f5")
    if "on_primary" not in colors:
        colors["on_primary"] = max(("#ffffff", "#111111"),
                                   key=lambda c: pe.contrast_ratio(c, colors["primary"]))
    colors.setdefault("surface", bg)
    colors.setdefault("border", colors["surface"])
    colors.setdefault("accent", colors["primary"])
    colors.setdefault("muted", colors["foreground"])
    typo = dtcg.get("typography", {})

    def fam(*keys):
        for k in keys:
            v = typo.get(k, {})
            v = v.get("fontFamily", v) if isinstance(v, dict) else {}
            if isinstance(v, dict) and v.get("$value"):
                val = v["$value"]
                return ", ".join(val) if isinstance(val, list) else val
        return "system-ui, sans-serif"
    return to_dtcg(colors, fam("heading", "display", "h1"), fam("body", "text", "base"), "dembrandt")


def write_brand(path, data):
    p = Path(path)
    if p.exists():
        cur = json.loads(p.read_text() or "{}")
        if cur.get("$extensions", {}).get("aura", {}).get("source", "none") != "none":
            print(f"recusado: {p} já tem uma marca (source != none)", file=sys.stderr)
            return 4
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return 0


# ---------------------------------------------------------------- drift

def as_flat(data):
    """design-tokens.json ou brand-tokens.json → {chave: valor normalizado}."""
    if "color" in data:
        colors = {r: data["color"][r]["$value"].lower() for r in ROLES if r in data["color"]}
        typo = data.get("typography", {})
        fams = {k: first_family(typo.get(k, {}).get("fontFamily", {}).get("$value", "")) for k in ("heading", "body")}
    else:
        colors = {r: v.lower() for r, v in data.get("colors", {}).items() if r in ROLES}
        t = data.get("type", {})
        fams = {"heading": first_family(t.get("heading_font")), "body": first_family(t.get("body_font"))}
    flat = {f"color.{k}": v for k, v in colors.items()}
    flat.update({f"font.{k}": (v or "").lower() for k, v in fams.items() if v})
    return flat


def diff(a, b):
    fa, fb = as_flat(a), as_flat(b)
    keys = sorted(set(fa) | set(fb))
    changed = [{"key": k, "a": fa.get(k), "b": fb.get(k)} for k in keys if fa.get(k) != fb.get(k)]
    return {"drift": round(100 * len(changed) / len(keys)) if keys else 0, "changed": changed}


def rgb_hex(css):
    nums = [float(n) for n in re.findall(r"[\d.]+", css or "")]
    return pe.rgb_to_hex(nums[:3]).lower() if len(nums) >= 3 else None


def diff_live(computed, tokens):
    flat = as_flat(tokens)
    palette = {v for k, v in flat.items() if k.startswith("color.")}
    fonts = {v for k, v in flat.items() if k.startswith("font.")}
    changed, checks = [], 0
    for s in computed.get("sections", []):
        for field in ("text", "background", "button"):
            h = rgb_hex(s.get(field))
            if h:
                checks += 1
                if h not in palette:
                    changed.append({"key": f"{s['section']}.{field}", "a": h, "b": "fora da paleta"})
        for tag, fam in (s.get("fonts") or {}).items():
            if fam:
                checks += 1
                name = first_family(fam).lower()
                if name not in fonts:
                    changed.append({"key": f"{s['section']}.{tag}", "a": name, "b": "fora das famílias"})
    return {"drift": round(100 * len(changed) / checks) if checks else 0, "changed": changed}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("page", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--source", choices=SOURCES)
    ap.add_argument("--preset-base")
    ap.add_argument("--brand-out")
    ap.add_argument("--from-dtcg")
    ap.add_argument("--diff", nargs=2)
    ap.add_argument("--diff-live", nargs=2)
    a = ap.parse_args(argv)
    try:
        if a.diff or a.diff_live:
            x, y = (json.loads(Path(p).read_text()) for p in (a.diff or a.diff_live))
            print(json.dumps(diff(x, y) if a.diff else diff_live(x, y), indent=2, ensure_ascii=False))
            return 0
        if a.from_dtcg:
            if not a.brand_out:
                raise ValueError("--from-dtcg exige --brand-out")
            return write_brand(a.brand_out, from_dtcg(json.loads(Path(a.from_dtcg).read_text())))
        if not (a.page and a.out and a.source):
            raise ValueError("uso: tokens.py PAGE.html --out design-tokens.json --source ENUM")
        html = Path(a.page).read_text(encoding="utf-8", errors="replace")
        loose = loose_colors(html)
        if len(loose) > MAX_LOOSE:
            print(f"ERRO: {len(loose)} cores soltas fora das variáveis (máx. {MAX_LOOSE}): "
                  f"{', '.join(loose[:8])}", file=sys.stderr)
            return 1
        out = Path(a.out)
        existing = json.loads(out.read_text()) if out.exists() else {}
        tokens = from_page(html, a.source, a.preset_base, existing)
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2
    out.write_text(json.dumps(tokens, indent=2, ensure_ascii=False) + "\n")
    print(f"design-tokens em {out}")
    if a.brand_out:
        c = tokens["colors"]
        return write_brand(a.brand_out, to_dtcg(c, tokens["type"]["heading_font"],
                                                tokens["type"]["body_font"], a.source))
    return 0


if __name__ == "__main__":
    sys.exit(main())
