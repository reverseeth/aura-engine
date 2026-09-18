#!/usr/bin/env python3
"""
check_embedded_queries.py — regressão: as `best_query` embutidas nas skills continuam no índice.

Percorre `.claude/skills/*.md`, `.claude/skills/*/SKILL.md` e os arquivos de apoio
`.claude/skills/*/reference/*.md` (formato nativo), pega toda frase entre crases com 4 ou
mais palavras e conta quantas são exatamente uma `best_query` do `frameworks.json`. Se o total cair abaixo do mínimo, alguma query embutida foi apagada
ou alterada por engano.

Uso:
  python3 .claude/lib/kb-index/check_embedded_queries.py                 mínimo padrão: 670
  python3 .claude/lib/kb-index/check_embedded_queries.py --min 737
  python3 .claude/lib/kb-index/check_embedded_queries.py --show-missing  lista as frases de 4+ palavras
                                                                          que NÃO são best_query (só informação)

Só biblioteca padrão. Exit 0 = total >= mínimo; exit 1 = abaixo do mínimo ou índice ausente.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INDEX = HERE / "frameworks.json"
SKILLS_DIR = ROOT / ".claude" / "skills"

SPAN = re.compile(r"`([^`\n]+)`")
COMMAND_HINTS = ("python3 ", "bash ", "git ", "claude ", "npx ", "--", "/", "search_knowledge(")


def skill_files():
    files = sorted(SKILLS_DIR.glob("*.md")) + sorted(SKILLS_DIR.glob("*/SKILL.md"))
    files += sorted(SKILLS_DIR.glob("*/reference/*.md"))
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(description="Confere que as best_query embutidas nas skills existem no índice.")
    parser.add_argument("--min", type=int, default=670, help="total mínimo de ocorrências exatas (padrão 670)")
    parser.add_argument("--show-missing", action="store_true", help="lista frases de 4+ palavras que não são best_query")
    args = parser.parse_args(argv)

    if not INDEX.exists():
        print(f"ERRO  índice não encontrado: {INDEX}", file=sys.stderr)
        return 1
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    queries = {e["best_query"] for entries in data["domains"].values() for e in entries}

    total = 0
    distinct = set()
    missing = []
    print("arquivo                                        embutidas  candidatas")
    for path in skill_files():
        text = path.read_text(encoding="utf-8")
        cands = [c for c in SPAN.findall(text) if len(c.split()) >= 4]
        hits = [c for c in cands if c in queries]
        total += len(hits)
        distinct.update(hits)
        rel = path.relative_to(ROOT)
        print(f"{str(rel):45s} {len(hits):9d} {len(cands):11d}")
        if args.show_missing:
            for c in cands:
                if c in queries or any(h in c for h in COMMAND_HINTS):
                    continue
                missing.append((rel, c))
    print(f"\nTotal: {total} ocorrências exatas de best_query ({len(distinct)} distintas) · mínimo {args.min}")
    if args.show_missing and missing:
        print("\nFrases de 4+ palavras entre crases que NÃO são best_query (informativo):")
        for rel, c in missing:
            print(f"  {rel}: {c}")
    if total < args.min:
        print("FALHA  total abaixo do mínimo")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
