#!/usr/bin/env python3
"""
copy_fit.py — a copy de cada seção cabe na faixa da referência que ela vai seguir?

Roda no passo do mapa do modo referência, antes de construir. Compara os caracteres de
texto visível da faixa (texts.json de 1440) com os caracteres da copy do membro para a
seção. Copy mais de 1,5× maior que a faixa não cabe: a seção vai sair mais alta que a
referência e o geodiff cobraria altura de um problema que não é de layout.

    copy.json: {"<id da seção>": "texto" | ["texto", ...], ...}

USO:
    copy_fit.py --ref DIR [--ref DIR ...] --map REF:BANDA:SECAO,... --copy copy.json --out copy-fit.json

Exit: 0 tudo cabe · 1 alguma seção não cabe · 2 entrada inválida.
"""
import argparse
import json
import sys
from pathlib import Path

from geodiff import parse_map

LIMIT = 1.5
# faixa quase sem texto (imagem, selo): a régua vira um teto absoluto de caracteres
MIN_REF_CHARS = 120


def ref_chars(capture_dir, band):
    texts = json.loads((Path(capture_dir) / "1440" / "texts.json").read_text())
    return sum(len(t["text"]) for t in texts if t["band"] == band)


def copy_chars(value):
    return sum(len(" ".join(v.split())) for v in ([value] if isinstance(value, str) else value))


def run(refs, mapping, copy):
    sections = []
    for ref_idx, band_idx, section in mapping:
        rc, cc = ref_chars(refs[ref_idx], band_idx), copy_chars(copy.get(section, ""))
        ratio = round(cc / max(rc, MIN_REF_CHARS), 2)
        sections.append({"aura_section": section, "ref": ref_idx, "band": band_idx,
                         "ref_chars": rc, "copy_chars": cc, "ratio": ratio, "fits": ratio <= LIMIT})
    return {"version": 1, "limit": LIMIT, "sections": sections,
            "all_fit": all(s["fits"] for s in sections)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--ref", action="append", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--copy", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        result = run(args.ref, parse_map(args.map), json.loads(Path(args.copy).read_text()))
    except (OSError, ValueError, KeyError, IndexError) as exc:
        print(f"ERRO: entrada inválida — {exc!r}", file=sys.stderr)
        return 2
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    for s in result["sections"]:
        print(f"{'✅' if s['fits'] else '⚠️'} {s['aura_section']:<24} copy {s['copy_chars']:>5} · "
              f"faixa {s['ref_chars']:>5} · {s['ratio']}×")
    return 0 if result["all_fit"] else 1


if __name__ == "__main__":
    sys.exit(main())
