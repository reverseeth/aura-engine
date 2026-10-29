#!/usr/bin/env python3
"""
legal_check.py — confere que nada da referência sobrou no page.html (modo referência).

Falha quando encontra no page.html:
  * texto: 6 palavras seguidas iguais às da referência (após normalizar caixa,
    pontuação e espaços), exceto as contidas numa linha de legal_allowlist.txt;
  * asset: URL ou nome de arquivo da referência;
  * fonte: font-family da referência fora das fontes permitidas (bloco
    `## Tipografia` do direction.md ou `typography` do brand-tokens.json);
  * marca: o nome da marca da referência (--ref-brand, ou derivado do domínio).

USO:
    legal_check.py --ref DIR [--ref DIR ...] --page page.html
                   [--allowed-fonts direction.md|brand-tokens.json ...]
                   [--ref-brand NOME ...] --out legal.json

Lê a largura 1440 de cada captura do `downloader.py --mode bands`.
Exit: 0 nada encontrado · 1 encontrou algo · 2 entrada inválida.
"""
import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ALLOWLIST = Path(__file__).with_name("legal_allowlist.txt")
N = 6
GENERIC_FONTS = {"serif", "sans-serif", "monospace", "system-ui", "cursive", "fantasy",
                 "-apple-system", "blinkmacsystemfont", "ui-sans-serif", "ui-serif", "inherit"}


def norm(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text.lower())).strip()


def shingles(text):
    w = norm(text).split()
    return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}


def page_text(html):
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return htmllib.unescape(re.sub(r"<[^>]+>", " ", body))


def families(value):
    return {f.strip().strip("'\"").lower() for f in value.split(",") if f.strip()} - GENERIC_FONTS


def allowed_fonts(paths):
    out = set()
    for p in paths:
        text = Path(p).read_text()
        if p.endswith(".json"):
            for v in json.loads(text).get("typography", {}).values():
                fam = v.get("fontFamily", {}).get("$value") if isinstance(v, dict) else None
                if fam:
                    out |= families(fam)
        else:
            block = re.search(r"^## Tipografia\s*$(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
            for m in re.finditer(r"família:\s*([^()\n]+)", block.group(1) if block else ""):
                out |= families(m.group(1))
    return out


def brand_from_url(url):
    host = urlparse(url).hostname or ""
    parts = [p for p in host.split(".") if p not in ("www", "shop", "store")]
    return parts[0].replace("-", " ") if parts else ""


def run(refs, page_path, allowed_paths, brands):
    html = Path(page_path).read_text(encoding="utf-8", errors="replace")
    text_norm = norm(page_text(html))
    allow = [norm(l) for l in ALLOWLIST.read_text().splitlines() if l.strip() and not l.startswith("#")]
    ok_fonts = allowed_fonts(allowed_paths)
    used_fonts = set()
    for m in re.finditer(r"font-family\s*:\s*([^;}\"]+)", html, flags=re.I):
        used_fonts |= families(m.group(1))
    page_shingles = shingles(page_text(html))
    findings = []
    for idx, ref in enumerate(refs):
        cap = Path(ref) / "1440"
        url = json.loads((cap / "bands.json").read_text())["url"]
        ref_text = " ".join(t["text"] for t in json.loads((cap / "texts.json").read_text()))
        for s in sorted(shingles(ref_text) & page_shingles):
            if not any(s in a for a in allow):
                findings.append({"rule": "texto", "match": s, "ref": idx, "where": "page.html"})
        for a in json.loads((cap / "assets.json").read_text()):
            name = Path(urlparse(a["url"]).path).name
            if a["url"] in html or (len(name) > 4 and name in html):
                findings.append({"rule": "asset", "match": a["url"], "ref": idx, "where": "page.html"})
        ref_fonts = set()
        for f in cap.glob("section-*.json"):
            for el in json.loads(f.read_text()):
                ref_fonts |= families(el["styles"].get("font-family", ""))
        for fam in sorted((ref_fonts & used_fonts) - ok_fonts):
            findings.append({"rule": "fonte", "match": fam, "ref": idx, "where": "font-family"})
        for brand in (brands or [brand_from_url(url)]):
            b = norm(brand)
            if len(b) > 2 and re.search(rf"\b{re.escape(b)}\b", text_norm):
                findings.append({"rule": "marca", "match": brand, "ref": idx, "where": "texto"})
    return {"version": 1, "pass": not findings, "findings": findings}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--ref", action="append", required=True)
    ap.add_argument("--page", required=True)
    ap.add_argument("--allowed-fonts", action="append", default=[])
    ap.add_argument("--ref-brand", action="append", default=[])
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        result = run(args.ref, args.page, args.allowed_fonts, args.ref_brand)
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERRO: entrada inválida — {exc!r}", file=sys.stderr)
        return 2
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for f in result["findings"]:
        print(f"❌ {f['rule']:<6} {f['match']}")
    print("✅ nada da referência no page.html" if result["pass"] else f"{len(result['findings'])} achado(s)")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
