"""
001_slug_folders: pastas de fase por nome da skill, sem número, e `skills_completed` com os ids novos.

Desde a Fase 5 da reforma mecânica, cada fase do produto mora em `workspace/<slug>/<id>/`
(`market-research/`, `page/`), e não mais em `02-market-research/` ou `07-page/`. Esta
migração renomeia cada pasta numerada para o nome novo, usando o par `legacy_folder` →
`folder` do registro `.claude/skills.json`, e traduz os valores de `skills_completed` do
manifest (`06-copy-engine` → `copy-engine`) pelo `legacy_ids` do mesmo registro.

Regras:
  - Se a pasta de destino já existir, NÃO mescla: registra no log e pula (o membro resolve à mão).
  - Não toca em nenhum outro arquivo do produto (relatórios, dados.json, brand.md ficam como estão).
  - Valor de `skills_completed` cujo número não é apelido conhecido fica como está, com aviso no log.

Contrato com o executor (`tools/migrate.py`): `NUMBER` (número da migração; a versão do layout
depois dela é NUMBER + 1), `NAME`, `SUMMARY`, `plan(product_dir, manifest, registry)` devolve a
lista de passos e `apply(product_dir, manifest, step)` executa um passo. Só biblioteca padrão.
"""
import re
from pathlib import Path

NUMBER = 1
NAME = "001_slug_folders"
SUMMARY = "pastas de fase por nome da skill (sem número) e skills_completed com os ids novos"

LEGACY_VALUE_RE = re.compile(r"^(\d{2}[a-e]?)-(.+)$")


def folder_pairs(registry):
    """Pares (pasta antiga, pasta nova) únicos, na ordem do registro."""
    pairs, seen = [], set()
    for s in registry["skills"]:
        old, new = s.get("legacy_folder"), s.get("folder")
        if not old or not new or old == new or (old, new) in seen:
            continue
        seen.add((old, new))
        pairs.append((old, new))
    return pairs


def legacy_map(registry):
    """apelido numérico → id."""
    out = {}
    for s in registry["skills"]:
        for lg in s.get("legacy_ids") or []:
            out[lg] = s["id"]
    return out


def translate_completed(values, legacy):
    """Traduz a lista `skills_completed`; devolve (lista nova, apelidos desconhecidos)."""
    out, unknown = [], []
    for v in values:
        new = v
        m = LEGACY_VALUE_RE.match(str(v))
        if m:
            if m.group(1) in legacy:
                new = legacy[m.group(1)]
            else:
                unknown.append(v)
        if new not in out:
            out.append(new)
    return out, unknown


def plan(product_dir, manifest, registry):
    steps = []
    for old, new in folder_pairs(registry):
        src = product_dir / old
        if not src.is_dir():
            continue
        if (product_dir / new).exists():
            steps.append({"op": "skip", "src": old, "dst": new, "reason": "destino já existe"})
        else:
            steps.append({"op": "rename", "src": old, "dst": new})
    completed = manifest.get("skills_completed")
    if isinstance(completed, list):
        new_list, unknown = translate_completed(completed, legacy_map(registry))
        for v in unknown:
            steps.append({"op": "note", "text": f"skills_completed mantém `{v}`: número que não é apelido de nenhuma skill"})
        if new_list != completed:
            steps.append({"op": "manifest", "field": "skills_completed", "before": list(completed), "after": new_list})
    return steps


def apply(product_dir, manifest, step):
    op = step["op"]
    if op == "rename":
        src, dst = product_dir / step["src"], product_dir / step["dst"]
        if dst.exists():
            raise RuntimeError(f"destino já existe: {dst}")
        src.rename(dst)
    elif op == "manifest":
        manifest[step["field"]] = step["after"]
    elif op in ("skip", "note"):
        return
    else:
        raise RuntimeError(f"passo desconhecido: {op}")


def describe(step):
    """Uma linha legível por passo (usada pelo executor no terminal e no log)."""
    op = step["op"]
    if op == "rename":
        return f"rename  {step['src']}/ -> {step['dst']}/"
    if op == "skip":
        return f"skip    {step['src']}/ -> {step['dst']}/  ({step['reason']}; resolva à mão)"
    if op == "manifest":
        return f"manifest  {step['field']}: {','.join(map(str, step['before']))} -> {','.join(map(str, step['after']))}"
    if op == "note":
        return f"note    {step['text']}"
    return f"{op}  {step}"
