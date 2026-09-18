#!/usr/bin/env python3
"""
normalize_index.py — deriva o campo `skills` de cada entrada do `frameworks.json`.

O campo `use_in_skill` de cada entrada é texto livre com os apelidos numéricos antigos
das skills ("06 (copy); 08 (creatives)"). Este script lê esse texto, traduz cada número
pelo `legacy_ids` do registro `.claude/skills.json` e grava o campo novo `skills`
(lista de ids, sem repetição, na ordem em que aparecem no texto). "—" ou vazio vira [].

Não altera `name`, `source`, `one_line`, `use_in_skill` nem `best_query`. Grava com a
mesma ordem de domínios e de entradas, a mesma indentação do arquivo (1 espaço) e
`ensure_ascii=False`; a lista `skills` fica numa linha só, para o diff mostrar uma
linha por entrada. Rodar duas vezes não muda nada.

Uso:
  python3 .claude/lib/kb-index/normalize_index.py            grava e imprime a contagem por skill
  python3 .claude/lib/kb-index/normalize_index.py --check    não grava; exit 1 se o arquivo mudaria
  python3 .claude/lib/kb-index/normalize_index.py --quiet    grava sem imprimir a contagem

Só biblioteca padrão. Exit 0 = em dia (ou gravado); exit 1 = desatualizado (--check),
registro ausente ou token de skill que o registro não conhece.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INDEX = HERE / "frameworks.json"
REGISTRY = ROOT / ".claude" / "skills.json"

# apelido numérico antigo de skill: "06", "07a", "01b" (nunca um dígito solto nem "3-2-2")
TOKEN = re.compile(r"\b(\d{2}[a-e]?)\b")


def load_registry(path=REGISTRY):
    """Devolve (ids na ordem do registro, mapa apelido -> id, mapa id -> apelidos)."""
    reg = json.loads(Path(path).read_text(encoding="utf-8"))
    ids, legacy, aliases = [], {}, {}
    for s in reg["skills"]:
        ids.append(s["id"])
        aliases[s["id"]] = list(s.get("legacy_ids", []))
        for old in s.get("legacy_ids", []):
            legacy[old] = s["id"]
    return ids, legacy, aliases


def derive_skills(text, legacy, unknown=None):
    """Lista de ids (sem repetição, na ordem do texto) a partir do texto de `use_in_skill`."""
    out = []
    for tok in TOKEN.findall(text or ""):
        sid = legacy.get(tok)
        if sid is None:
            if unknown is not None:
                unknown.append(tok)
            continue
        if sid not in out:
            out.append(sid)
    return out


def with_skills(entry, skills):
    """Devolve a entrada com `skills` logo depois de `use_in_skill`; os outros campos ficam na mesma ordem."""
    new = {}
    for key, value in entry.items():
        if key == "skills":
            continue
        new[key] = value
        if key == "use_in_skill":
            new["skills"] = skills
    if "skills" not in new:
        new["skills"] = skills
    return new


def normalize(data, legacy):
    """Devolve (dados com `skills`, contagem por id, tokens desconhecidos)."""
    counts = {}
    unknown = []
    for domain, entries in data["domains"].items():
        data["domains"][domain] = []
        for entry in entries:
            skills = derive_skills(entry.get("use_in_skill", ""), legacy, unknown)
            for sid in skills:
                counts[sid] = counts.get(sid, 0) + 1
            data["domains"][domain].append(with_skills(entry, skills))
    return data, counts, unknown


_SKILLS_BLOCK = re.compile(r'"skills": \[\s*((?:"[^"]*",?\s*)*)\]')


def dump(data):
    """Serializa como o arquivo original (indent=1, ensure_ascii=False) com `skills` em uma linha."""
    text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"

    def collapse(match):
        items = re.findall(r'"([^"]*)"', match.group(1))
        return '"skills": [' + ", ".join('"%s"' % item for item in items) + "]"

    return _SKILLS_BLOCK.sub(collapse, text)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Deriva o campo `skills` das entradas do frameworks.json.")
    parser.add_argument("--check", action="store_true", help="não grava; exit 1 se o arquivo mudaria")
    parser.add_argument("--quiet", action="store_true", help="não imprime a contagem por skill")
    parser.add_argument("--index", default=str(INDEX), help="caminho do frameworks.json (padrão: o desta pasta)")
    parser.add_argument("--registry", default=str(REGISTRY), help="caminho do skills.json")
    args = parser.parse_args(argv)

    index_path = Path(args.index)
    if not index_path.exists():
        print(f"ERRO  índice não encontrado: {index_path}", file=sys.stderr)
        return 1
    if not Path(args.registry).exists():
        print(f"ERRO  registro não encontrado: {args.registry}", file=sys.stderr)
        return 1

    ids, legacy, _ = load_registry(args.registry)
    raw = index_path.read_text(encoding="utf-8")
    data, counts, unknown = normalize(json.loads(raw), legacy)
    text = dump(data)

    if unknown:
        seen = sorted(set(unknown))
        print(f"ERRO  {len(unknown)} menção(ões) a apelido que o registro não conhece: {', '.join(seen)}", file=sys.stderr)
        return 1

    changed = text != raw
    if args.check:
        if changed:
            print(f"DESATUALIZADO  {index_path}  (rode normalize_index.py)")
            return 1
        print("OK")
        return 0

    if changed:
        index_path.write_text(text, encoding="utf-8")
        print(f"gravado  {index_path}")
    else:
        print(f"em dia   {index_path}")

    if not args.quiet:
        total = sum(len(v) for v in data["domains"].values())
        empty = sum(1 for v in data["domains"].values() for e in v if not e["skills"])
        print(f"\nEntradas: {total}  ·  sem skill (dormant): {empty}\n")
        print("skill                  entradas")
        for sid in sorted(ids, key=lambda i: (-counts.get(i, 0), i)):
            print(f"{sid:22s} {counts.get(sid, 0):5d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
