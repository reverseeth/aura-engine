#!/usr/bin/env python3
"""
schema_validate.py: validador mínimo de JSON Schema (draft-07) só com biblioteca padrão.

Cobre o subconjunto que os schemas da Aura usam: `type` (nome ou lista de nomes), `enum`,
`const`, `properties`, `required`, `additionalProperties: false`, `items`, `minItems`,
`maxItems`, `minimum`, `maximum`, `minLength`, `maxLength`, `pattern`, `anyOf`, `oneOf`,
`allOf` e `not`. Palavras que não conhece (`format`, `$comment`, `description`...) são
ignoradas, como um validador completo faria com anotações.

Uso como módulo (o `tools/manifest.py`, o `tools/aura-status.py` e o `build_index.py` importam):

    import schema_validate
    fails = schema_validate.validate(instance, schema)   # lista de strings "caminho: motivo"
    fails = schema_validate.validate_file(json_path, schema_path)

Uso como script:

    python3 tools/schema_validate.py <schema.json> <arquivo.json> [...]

Imprime uma linha por falha (`ARQUIVO  CAMINHO  motivo`) e `OK` quando não há nenhuma.
Exit 0 = tudo válido; 1 = alguma falha ou arquivo que não parseia.
"""
import argparse
import json
import re
import sys
from pathlib import Path

TYPE_NAMES = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _type_ok(value, expected):
    names = expected if isinstance(expected, list) else [expected]
    return any(TYPE_NAMES.get(n, lambda v: True)(value) for n in names)


def _fmt(value):
    s = json.dumps(value, ensure_ascii=False)
    return s if len(s) <= 60 else s[:57] + "..."


def validate(instance, schema, path="$"):
    """Devolve a lista de falhas (strings `caminho: motivo`); lista vazia = válido."""
    fails = []
    if not isinstance(schema, dict):
        return fails
    if "type" in schema and not _type_ok(instance, schema["type"]):
        exp = schema["type"] if isinstance(schema["type"], str) else "|".join(schema["type"])
        fails.append(f"{path}: esperado {exp}, veio {_fmt(instance)}")
        return fails                     # tipo errado: o resto das checagens não faz sentido
    if "enum" in schema and instance not in schema["enum"]:
        allowed = ", ".join(json.dumps(v, ensure_ascii=False) for v in schema["enum"])
        fails.append(f"{path}: valor {_fmt(instance)} fora do enum [{allowed}]")
    if "const" in schema and instance != schema["const"]:
        fails.append(f"{path}: esperado o valor fixo {_fmt(schema['const'])}, veio {_fmt(instance)}")
    if isinstance(instance, dict):
        for key in schema.get("required") or []:
            if key not in instance:
                fails.append(f"{path}.{key}: campo obrigatório ausente")
        props = schema.get("properties") or {}
        for key, sub in props.items():
            if key in instance:
                fails.extend(validate(instance[key], sub, f"{path}.{key}"))
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    fails.append(f"{path}.{key}: campo não previsto (additionalProperties: false)")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            fails.append(f"{path}: precisa de pelo menos {schema['minItems']} item(ns), tem {len(instance)}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            fails.append(f"{path}: no máximo {schema['maxItems']} item(ns), tem {len(instance)}")
        items = schema.get("items")
        if isinstance(items, dict):
            for i, v in enumerate(instance):
                fails.extend(validate(v, items, f"{path}[{i}]"))
        elif isinstance(items, list):
            for i, (v, sub) in enumerate(zip(instance, items)):
                fails.extend(validate(v, sub, f"{path}[{i}]"))
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            fails.append(f"{path}: {instance} abaixo do mínimo {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            fails.append(f"{path}: {instance} acima do máximo {schema['maximum']}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            fails.append(f"{path}: texto menor que {schema['minLength']} caractere(s)")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            fails.append(f"{path}: texto maior que {schema['maxLength']} caractere(s)")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            fails.append(f"{path}: {_fmt(instance)} não casa com o padrão {schema['pattern']}")
    if "allOf" in schema:
        for sub in schema["allOf"]:
            fails.extend(validate(instance, sub, path))
    if "anyOf" in schema and all(validate(instance, sub, path) for sub in schema["anyOf"]):
        fails.append(f"{path}: não satisfaz nenhuma das alternativas (anyOf)")
    if "oneOf" in schema and sum(1 for sub in schema["oneOf"] if not validate(instance, sub, path)) != 1:
        fails.append(f"{path}: precisa satisfazer exatamente uma alternativa (oneOf)")
    if "not" in schema and not validate(instance, schema["not"], path):
        fails.append(f"{path}: satisfaz o schema proibido (not)")
    return fails


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_file(json_path, schema_path):
    """Valida um arquivo contra um schema. Arquivo que não parseia vira uma falha única."""
    try:
        instance = load(json_path)
    except (OSError, ValueError) as e:
        return [f"$: arquivo não parseia ({e})"]
    return validate(instance, load(schema_path))


def main():
    ap = argparse.ArgumentParser(description="Valida arquivos JSON contra um schema draft-07 (subconjunto).")
    ap.add_argument("schema", help="caminho do schema (.json)")
    ap.add_argument("files", nargs="+", help="arquivos JSON a validar")
    args = ap.parse_args()
    try:
        schema = load(args.schema)
    except (OSError, ValueError) as e:
        print(f"schema não parseia: {args.schema} ({e})", file=sys.stderr)
        return 1
    total = 0
    for f in args.files:
        try:
            instance = load(f)
        except (OSError, ValueError) as e:
            print(f"{f}  $  arquivo não parseia ({e})")
            total += 1
            continue
        for line in validate(instance, schema):
            path, _, msg = line.partition(": ")
            print(f"{f}  {path}  {msg}")
            total += 1
    print("OK" if total == 0 else f"{total} falha(s)")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
