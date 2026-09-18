#!/usr/bin/env python3
"""
manifest.py: lê e grava o `manifest.json` de um produto do workspace com backup e validação.

É o único caminho pelo qual uma skill deve alterar o manifest (nunca editando o JSON à mão).
Toda escrita faz backup (`.manifest-backup-AAAAMMDD-HHMMSS.json`, o mesmo padrão da skill
`setup` e do `tools/migrate.py`), atualiza `updated_at` (UTC, ISO-8601), valida o resultado
contra `.claude/templates/manifest-schema.json` e só então grava. Uma falha de validação que já
existia antes da escrita é avisada e não bloqueia; uma falha NOVA, introduzida pela escrita,
bloqueia (nada é gravado, exit 1).

Uso:
  python3 tools/manifest.py <slug> get <chave>
      Imprime o valor (JSON) da chave. Chave em caminho pontuado: `stage`, `tracking.emq_score`,
      `skills_completed.0`. Chave ausente: imprime `null` no stderr e sai com 1.

  python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]
      Grava um ou mais campos numa escrita só (um backup). O valor é JSON: `50`, `true`,
      `'"US"'`, `'["a","b"]'`, `'{"pixel_installed": true}'`. Caminho pontuado cria os objetos
      intermediários que faltarem (`tracking.pixel_installed true`). Com `--string`, todos os
      valores são gravados como texto sem precisar das aspas.

  python3 tools/manifest.py <slug> complete <skill-id> [--skip-dados]
      Acrescenta o id (canônico, do `.claude/skills.json`) em `skills_completed`, sem duplicar.
      Se a skill tem schema em `.claude/templates/schemas/<id>.dados.schema.json` e o
      `<pasta>/dados.json` existe, valida o arquivo antes: falha bloqueia a marcação (corrija o
      dados.json e rode de novo), ou passe `--skip-dados` para marcar mesmo assim.

  python3 tools/manifest.py <slug> validate
      Valida o manifest contra o schema e imprime cada falha (`CAMPO  motivo`). `OK` = válido.

Depois de `set`/`complete`, regenere o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>`.
A variável de ambiente AURA_WORKSPACE aponta para outra pasta de workspace (só para testes).
Só biblioteca padrão. Exit 0 = ok; 1 = erro (produto inexistente, manifest que não parseia, chave
ausente no `get`, valor que não é JSON, id desconhecido, falha nova de validação).
"""
import argparse
import datetime
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
WORKSPACE = Path(os.environ["AURA_WORKSPACE"]) if os.environ.get("AURA_WORKSPACE") else ROOT / "workspace"
REGISTRY = ROOT / ".claude" / "skills.json"
MANIFEST_SCHEMA = ROOT / ".claude" / "templates" / "manifest-schema.json"
DADOS_SCHEMAS = ROOT / ".claude" / "templates" / "schemas"
PREFIX = "[aura] manifest:"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import schema_validate  # noqa: E402


class ManifestError(Exception):
    pass


def rel(path):
    """Caminho legível: relativo ao repo quando está dentro dele, senão relativo à pasta do produto."""
    path = Path(path)
    for base in (ROOT, WORKSPACE.parent):
        try:
            return str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


# ----------------------------------------------------------------------------- leitura e escrita
def product_dir(slug):
    p = WORKSPACE / slug
    if not (p / "manifest.json").is_file():
        raise ManifestError(f"produto não encontrado: workspace/{slug}/manifest.json")
    return p


def read_manifest(product):
    path = product / "manifest.json"
    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except ValueError as e:
        raise ManifestError(f"{rel(path)} não parseia ({e}); recupere pelo ES2 da rule "
                            f"emergency-escape-paths (backup em .manifest-backup-*.json)")
    if not isinstance(data, dict):
        raise ManifestError(f"{rel(path)} não é um objeto JSON")
    return data, raw.endswith("\n")


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)


def backup_manifest(product, when):
    dst = product / f".manifest-backup-{when.strftime('%Y%m%d-%H%M%S')}.json"
    n = 1
    while dst.exists():
        dst = product / f".manifest-backup-{when.strftime('%Y%m%d-%H%M%S')}-{n}.json"
        n += 1
    dst.write_bytes((product / "manifest.json").read_bytes())
    return dst.name


def write_manifest(product, data, trailing_newline):
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if trailing_newline:
        text += "\n"
    (product / "manifest.json").write_text(text, encoding="utf-8")


def load_schema():
    return json.loads(MANIFEST_SCHEMA.read_text(encoding="utf-8"))


def registry_ids():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {s["id"]: s for s in reg["skills"]}


# ----------------------------------------------------------------------------- caminhos pontuados
def split_key(key):
    parts = [p for p in key.split(".") if p != ""]
    if not parts:
        raise ManifestError(f"chave vazia: {key!r}")
    return parts


def get_path(data, key):
    cur = data
    for part in split_key(key):
        if isinstance(cur, dict):
            if part not in cur:
                raise KeyError(key)
            cur = cur[part]
        elif isinstance(cur, list) and part.lstrip("-").isdigit():
            try:
                cur = cur[int(part)]
            except IndexError:
                raise KeyError(key)
        else:
            raise KeyError(key)
    return cur


def set_path(data, key, value):
    parts = split_key(key)
    cur = data
    for part in parts[:-1]:
        if isinstance(cur, list) and part.isdigit():
            cur = cur[int(part)]
            continue
        if not isinstance(cur, dict):
            raise ManifestError(f"não dá para descer em `{part}` (chave {key}): o valor no caminho não é um objeto")
        if part not in cur or not isinstance(cur[part], (dict, list)):
            cur[part] = {}
        cur = cur[part]
    last = parts[-1]
    if isinstance(cur, list) and last.isdigit():
        cur[int(last)] = value
    elif isinstance(cur, dict):
        cur[last] = value
    else:
        raise ManifestError(f"não dá para gravar `{last}` (chave {key}): o valor no caminho não é um objeto")


def parse_value(text, as_string):
    if as_string:
        return text
    try:
        return json.loads(text)
    except ValueError:
        raise ManifestError(f"valor não é JSON: {text!r}. Texto precisa de aspas (ex.: '\"US\"'), "
                            f"ou use --string para gravar todos os valores como texto.")


# ----------------------------------------------------------------------------- validação e commit
def fails_of(data):
    return schema_validate.validate(data, load_schema())


def commit(product, before, after, trailing, what):
    """Valida `after` contra o schema; grava com backup se não houver falha nova."""
    old = set(fails_of(before))
    new = fails_of(after)
    introduced = [f for f in new if f not in old]
    if introduced:
        print(f"{PREFIX} {product.name}: a escrita ({what}) violaria o manifest-schema; nada foi gravado:")
        for f in introduced:
            print(f"    {f}")
        return False
    when = now_utc()
    after["updated_at"] = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    name = backup_manifest(product, when)
    write_manifest(product, after, trailing)
    print(f"{PREFIX} {product.name}: {what} (backup {name})")
    remaining = [f for f in new if f in old]
    if remaining:
        print(f"{PREFIX} {product.name}: o manifest já tinha {len(remaining)} falha(s) de schema antes desta escrita "
              f"(rode `python3 tools/manifest.py {product.name} validate` para ver)")
    return True


# ----------------------------------------------------------------------------- comandos
def cmd_get(product, args):
    data, _ = read_manifest(product)
    try:
        value = get_path(data, args.key)
    except KeyError:
        print("null", file=sys.stderr)
        return 1
    print(json.dumps(value, ensure_ascii=False, indent=2 if isinstance(value, (dict, list)) else None))
    return 0


def cmd_set(product, args):
    if len(args.pairs) % 2 != 0:
        raise ManifestError("`set` recebe pares <chave> <valor-json>")
    data, trailing = read_manifest(product)
    before = json.loads(json.dumps(data))
    changed = []
    for key, raw in zip(args.pairs[::2], args.pairs[1::2]):
        set_path(data, key, parse_value(raw, args.string))
        changed.append(key)
    return 0 if commit(product, before, data, trailing, "set " + ", ".join(changed)) else 1


def cmd_complete(product, args):
    ids = registry_ids()
    if args.skill_id not in ids:
        raise ManifestError(f"id desconhecido: {args.skill_id}. Ids válidos: {', '.join(ids)}")
    skill = ids[args.skill_id]
    folder = skill.get("folder")
    schema_path = DADOS_SCHEMAS / f"{args.skill_id}.dados.schema.json"
    dados = product / folder / "dados.json" if folder else None
    if not args.skip_dados and schema_path.is_file() and dados is not None and dados.is_file():
        fails = schema_validate.validate_file(dados, schema_path)
        if fails:
            print(f"{PREFIX} {product.name}: {rel(dados)} falha no schema ({len(fails)} problema(s)); "
                  f"`{args.skill_id}` NÃO foi marcada. Corrija o arquivo ou use --skip-dados:")
            for f in fails[:12]:
                print(f"    {f}")
            if len(fails) > 12:
                print(f"    ... e mais {len(fails) - 12}")
            return 1
    data, trailing = read_manifest(product)
    before = json.loads(json.dumps(data))
    completed = data.get("skills_completed")
    if not isinstance(completed, list):
        completed = []
    if args.skill_id in completed:
        print(f"{PREFIX} {product.name}: `{args.skill_id}` já estava em skills_completed (nada a fazer)")
        return 0
    data["skills_completed"] = completed + [args.skill_id]
    return 0 if commit(product, before, data, trailing, f"complete {args.skill_id}") else 1


def cmd_validate(product, args):
    data, _ = read_manifest(product)
    fails = fails_of(data)
    for f in fails:
        path, _, msg = f.partition(": ")
        print(f"{path}  {msg}")
    print("OK" if not fails else f"{len(fails)} falha(s)")
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description="Lê e grava o manifest.json de um produto (backup + validação).",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("Uso:")[1])
    ap.add_argument("slug", help="pasta do produto em workspace/")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get", help="imprime o valor de uma chave (caminho pontuado)")
    g.add_argument("key")
    s = sub.add_parser("set", help="grava pares <chave> <valor-json>")
    s.add_argument("pairs", nargs="+", metavar="CHAVE VALOR")
    s.add_argument("--string", action="store_true", help="grava os valores como texto, sem parse de JSON")
    c = sub.add_parser("complete", help="acrescenta o id da skill em skills_completed")
    c.add_argument("skill_id")
    c.add_argument("--skip-dados", action="store_true", help="não valida o dados.json da fase antes de marcar")
    sub.add_parser("validate", help="valida o manifest contra o manifest-schema")
    args = ap.parse_args()
    try:
        product = product_dir(args.slug)
        return {"get": cmd_get, "set": cmd_set, "complete": cmd_complete, "validate": cmd_validate}[args.cmd](product, args)
    except ManifestError as e:
        print(f"{PREFIX} ERRO: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"{PREFIX} ERRO de leitura/escrita: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
