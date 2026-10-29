#!/usr/bin/env python3
"""
geodiff.py — compara a geometria de cada seção da página com a faixa da referência.

Entrada: capturas do `downloader.py --mode bands` (uma pasta por URL de referência e uma
da própria página). Para cada par do mapa, por largura (1440 e 390):

    nota = 100 − 40·min(1, |Δaltura| ÷ altura_ref)
               − 30·(colunas diferentes ? 1 : 0)
               − 30·min(1, deslocamento_médio ÷ 0,25)

O deslocamento é a distância média entre os centros das caixas do mesmo tipo (texto,
mídia, CTA), em fração da largura da viewport. A nota da seção é a menor das larguras.

USO:
    geodiff.py --ref DIR [--ref DIR ...] --page DIR --map REF:BANDA:SECAO,... --out geodiff.json

Exit: 0 todas as seções com nota ≥ 70 · 1 alguma abaixo de 70 · 2 entrada inválida.
"""
import argparse
import json
import math
import sys
from pathlib import Path

WIDTHS = (1440, 390)
PASS = 70


def load_bands(capture_dir, width):
    return json.loads((Path(capture_dir) / str(width) / "bands.json").read_text())["bands"]


def displacement(ref_boxes, page_boxes):
    dists = []
    for kind in ("text", "media", "cta"):
        a = [b for b in ref_boxes if b["kind"] == kind]
        b = [x for x in page_boxes if x["kind"] == kind]
        for ra in a:
            if b:
                dists.append(min(math.hypot(ra["cx"] - pb["cx"], ra["cy"] - pb["cy"]) for pb in b))
            else:
                dists.append(1.0)
    return sum(dists) / len(dists) if dists else 0.0


def score(ref, page):
    dh = min(1.0, abs(page["height"] - ref["height"]) / ref["height"]) if ref["height"] else 1.0
    cols = 1 if page["columns"] != ref["columns"] else 0
    disp = min(1.0, displacement(ref["boxes"], page["boxes"]) / 0.25)
    diffs = sorted([("altura", 40 * dh), ("colunas", 30 * cols), ("posição dos blocos", 30 * disp)],
                   key=lambda x: -x[1])
    return round(100 - 40 * dh - 30 * cols - 30 * disp), [d for d, v in diffs if v > 0]


def parse_map(text):
    out = []
    for part in text.split(","):
        ref_idx, band_idx, section = part.strip().split(":", 2)
        out.append((int(ref_idx), int(band_idx), section))
    return out


def run(refs, page_dir, mapping):
    sections = []
    for ref_idx, band_idx, section in mapping:
        by_width, diffs = {}, []
        for w in WIDTHS:
            ref = next(b for b in load_bands(refs[ref_idx], w) if b["index"] == band_idx)
            page = next((b for b in load_bands(page_dir, w) if b.get("aura_section") == section), None)
            if page is None:
                by_width[w], d = 0, ["seção ausente na página"]
            else:
                by_width[w], d = score(ref, page)
            diffs += [x for x in d if x not in diffs]
        sections.append({"aura_section": section, "ref": ref_idx, "band": band_idx,
                         "score": min(by_width.values()), "by_width": by_width, "top_diffs": diffs[:5]})
    return {"version": 1, "sections": sections,
            "min_score": min((s["score"] for s in sections), default=100)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--ref", action="append", required=True)
    ap.add_argument("--page", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        result = run(args.ref, args.page, parse_map(args.map))
    except (OSError, ValueError, KeyError, IndexError, StopIteration) as exc:
        print(f"ERRO: entrada inválida — {exc!r}", file=sys.stderr)
        return 2
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for s in result["sections"]:
        print(f"{'✅' if s['score'] >= PASS else '❌'} {s['aura_section']:<24} {s['score']:>3}  {', '.join(s['top_diffs'])}")
    return 0 if result["min_score"] >= PASS else 1


if __name__ == "__main__":
    sys.exit(main())
