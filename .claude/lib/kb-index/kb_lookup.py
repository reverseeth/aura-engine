#!/usr/bin/env python3
"""
kb_lookup.py — lista as entradas do índice de frameworks marcadas para uma skill.

É o caminho de consulta ao índice: em vez de abrir o `frameworks.json` inteiro (cerca de
200 mil tokens), a skill roda este script e trabalha com a lista impressa. Cada linha traz
o nome do sistema, a `best_query` exata (nunca truncada) e o resumo de uma linha.

Uso:
  python3 .claude/lib/kb-index/kb_lookup.py --skill copy-engine
  python3 .claude/lib/kb-index/kb_lookup.py --skill 08 --domain creatives-hooks-formats
  python3 .claude/lib/kb-index/kb_lookup.py --skill offer-builder --domain offer-mechanism --domain offer-pricing-guarantee
  python3 .claude/lib/kb-index/kb_lookup.py --skill ad-analysis --grep "4Pi"
  python3 .claude/lib/kb-index/kb_lookup.py --skill retention-engine --format json

  --skill    obrigatório; id do registro (`copy-engine`) ou apelido numérico antigo (`06`)
  --domain   opcional, repetível; limita a um ou mais domínios do índice
  --grep     opcional; filtra por texto (sem distinção de maiúsculas) em `name` e `one_line`
  --format   md (padrão) ou json
  --list-domains  imprime os domínios do índice com a contagem total e sai

Só biblioteca padrão. Exit 0 = lista impressa (mesmo vazia); exit 1 = skill ou domínio desconhecido.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from normalize_index import INDEX, REGISTRY, derive_skills, load_registry  # noqa: E402


def resolve_skill(value, ids, legacy):
    value = value.strip()
    if value in ids:
        return value
    if value in legacy:
        return legacy[value]
    low = value.lower().lstrip("0") or value
    for old, sid in legacy.items():
        if old.lstrip("0") == low:
            return sid
    return None


def collect(data, skill, legacy, domains=None, grep=None):
    """Devolve lista de (domínio, entrada) marcadas para a skill, na ordem do arquivo."""
    needle = grep.lower() if grep else None
    found = []
    for domain, entries in data["domains"].items():
        if domains and domain not in domains:
            continue
        for entry in entries:
            skills = entry.get("skills")
            if skills is None:
                skills = derive_skills(entry.get("use_in_skill", ""), legacy)
            if skill not in skills:
                continue
            if needle and needle not in (entry.get("name", "") + " " + entry.get("one_line", "")).lower():
                continue
            found.append((domain, entry))
    return found


def render_md(skill, aliases, found, domains, grep):
    lines = []
    head = f"# kb-index · skill `{skill}`"
    if aliases:
        head += f" (apelido antigo: {', '.join(aliases)})"
    if domains:
        head += f" · domínio(s): {', '.join(domains)}"
    if grep:
        head += f" · grep: \"{grep}\""
    lines.append(head)
    by_domain = {}
    for domain, entry in found:
        by_domain.setdefault(domain, []).append(entry)
    for domain, entries in by_domain.items():
        lines.append("")
        lines.append(f"## {domain} ({len(entries)} entrada{'s' if len(entries) != 1 else ''})")
        for e in entries:
            lines.append(f"- **{e['name']}** · `{e['best_query']}` — {e['one_line']}")
    lines.append("")
    n = len(found)
    lines.append(f"Total: {n} entrada{'s' if n != 1 else ''} · {len(by_domain)} domínio{'s' if len(by_domain) != 1 else ''} · skill `{skill}`")
    return "\n".join(lines) + "\n"


def render_json(skill, aliases, found, domains, grep):
    out = {
        "skill": skill,
        "legacy_ids": aliases,
        "domains_filter": domains or [],
        "grep": grep,
        "count": len(found),
        "entries": [dict(domain=domain, **entry) for domain, entry in found],
    }
    return json.dumps(out, ensure_ascii=False, indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lista as entradas do índice marcadas para uma skill.")
    parser.add_argument("--skill", help="id da skill (ex: copy-engine) ou apelido numérico antigo (ex: 06)")
    parser.add_argument("--domain", action="append", default=[], help="domínio do índice (repetível)")
    parser.add_argument("--grep", default=None, help="texto a procurar em name e one_line")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--list-domains", action="store_true", help="lista os domínios e sai")
    parser.add_argument("--index", default=str(INDEX), help="caminho do frameworks.json")
    parser.add_argument("--registry", default=str(REGISTRY), help="caminho do skills.json")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.index).read_text(encoding="utf-8"))
    if args.list_domains:
        for domain, entries in data["domains"].items():
            print(f"{domain:35s} {len(entries):5d}")
        return 0
    if not args.skill:
        print("ERRO  --skill é obrigatório (ou use --list-domains). Veja --help.", file=sys.stderr)
        return 1

    ids, legacy, aliases = load_registry(args.registry)
    skill = resolve_skill(args.skill, ids, legacy)
    if skill is None:
        valid = ", ".join(f"{sid} ({'/'.join(aliases[sid])})" for sid in ids)
        print(f"ERRO  skill desconhecida: {args.skill!r}. Válidas: {valid}", file=sys.stderr)
        return 1
    unknown = [d for d in args.domain if d not in data["domains"]]
    if unknown:
        print(f"ERRO  domínio desconhecido: {', '.join(unknown)}. Válidos: {', '.join(data['domains'])}", file=sys.stderr)
        return 1

    found = collect(data, skill, legacy, domains=args.domain or None, grep=args.grep)
    render = render_json if args.format == "json" else render_md
    sys.stdout.write(render(skill, aliases.get(skill, []), found, args.domain, args.grep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
