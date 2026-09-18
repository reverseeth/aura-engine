#!/usr/bin/env python3
"""
migrate.py: aplica aos produtos de `workspace/` as migrações de layout pendentes.

Cada produto guarda em `manifest.framework_version` a versão do layout que ele segue (campo
ausente = 1). As migrações vivem em `tools/migrations/NNN_<nome>.py`; a migração NNN leva o
produto à versão NNN + 1. O executor lê a versão de cada produto, aplica em ordem as migrações
com número maior ou igual à versão, faz backup do manifest antes de qualquer mudança
(`.manifest-backup-AAAAMMDD-HHMMSS.json`, o mesmo padrão da skill `setup`), grava a versão nova
e registra cada passo em `.migrations.log` na pasta do produto. Idempotente: rodar duas vezes
não muda nada. Migração sem nenhum passo a executar só carimba a versão (sem backup).

Um produto é qualquer pasta `workspace/<slug>/` que contenha `manifest.json`. Se a pasta de
destino de um rename já existir, a migração não mescla: registra no log, avisa e pula (o membro
resolve à mão). Manifest que não parseia é avisado e pulado (exit 1 no fim).

Uso:
  python3 tools/migrate.py --all [--dry-run] [--verbose]
  python3 tools/migrate.py --product <slug> [--dry-run] [--verbose]
  python3 tools/migrate.py --list

  --dry-run   imprime o que faria em cada produto, sem gravar nada (sempre detalhado).
  --verbose   também lista os produtos que já estão em dia; sem ele, produto em dia é silêncio
              (é o modo do hook de início de sessão: uma linha por produto migrado, nada mais).
  --list      lista as migrações conhecidas e sai.

Contrato de cada módulo de migração: `NUMBER`, `NAME`, `SUMMARY`, `plan(product_dir, manifest,
registry)` (devolve a lista de passos), `apply(product_dir, manifest, step)` (executa um passo;
passos `manifest` alteram o dict, e o executor grava) e `describe(step)` (uma linha legível).

Só biblioteca padrão. Exit 0 = ok; exit 1 = erro (workspace ou produto inexistente, manifest
inválido, falha ao aplicar um passo).
"""
import argparse
import datetime
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "skills.json"
WORKSPACE = ROOT / "workspace"
MIGRATIONS_DIR = ROOT / "tools" / "migrations"
PREFIX = "[aura] migrate:"
MODULE_RE = re.compile(r"^(\d{3})_([a-z0-9_]+)\.py$")


def load_migrations():
    mods = []
    for path in sorted(MIGRATIONS_DIR.glob("*.py")):
        m = MODULE_RE.match(path.name)
        if not m:
            continue
        spec = importlib.util.spec_from_file_location(f"aura_migration_{m.group(1)}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for attr in ("NUMBER", "NAME", "SUMMARY", "plan", "apply", "describe"):
            if not hasattr(mod, attr):
                raise RuntimeError(f"{path.name}: falta `{attr}` no módulo de migração")
        if mod.NUMBER != int(m.group(1)):
            raise RuntimeError(f"{path.name}: NUMBER={mod.NUMBER} não bate com o nome do arquivo")
        mods.append(mod)
    mods.sort(key=lambda x: x.NUMBER)
    return mods


def current_version(mods):
    return (mods[-1].NUMBER + 1) if mods else 1


def products(slug=None):
    if not WORKSPACE.is_dir():
        return []
    if slug:
        p = WORKSPACE / slug
        return [p] if (p / "manifest.json").is_file() else []
    return sorted(p for p in WORKSPACE.iterdir() if p.is_dir() and (p / "manifest.json").is_file())


def now_stamp():
    return datetime.datetime.now(datetime.timezone.utc)


def read_manifest(product):
    raw = (product / "manifest.json").read_text(encoding="utf-8")
    return json.loads(raw), raw.endswith("\n")


def write_manifest(product, manifest, trailing_newline):
    text = json.dumps(manifest, indent=2, ensure_ascii=False)
    if trailing_newline:
        text += "\n"
    (product / "manifest.json").write_text(text, encoding="utf-8")


def backup_manifest(product, when):
    dst = product / f".manifest-backup-{when.strftime('%Y%m%d-%H%M%S')}.json"
    n = 1
    while dst.exists():
        dst = product / f".manifest-backup-{when.strftime('%Y%m%d-%H%M%S')}-{n}.json"
        n += 1
    dst.write_bytes((product / "manifest.json").read_bytes())
    return dst.name


def log(product, when, name, line):
    stamp = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    with (product / ".migrations.log").open("a", encoding="utf-8") as fh:
        fh.write(f"{stamp}  {name}  {line}\n")


def migrate_product(product, mods, registry, dry_run, verbose):
    """Devolve (migrou_algo, erro)."""
    slug = product.name
    try:
        manifest, trailing = read_manifest(product)
    except (OSError, ValueError) as e:
        print(f"{PREFIX} {slug}: manifest.json não parseia, produto pulado ({e})")
        return False, True
    version = manifest.get("framework_version")
    version = int(version) if isinstance(version, int) and version >= 1 else 1
    pending = [m for m in mods if m.NUMBER >= version]
    if not pending:
        if verbose or dry_run:
            print(f"{PREFIX} {slug}: em dia (framework_version {version})")
        return False, False

    changed, failed, backup_name = False, False, None
    for mod in pending:
        target = mod.NUMBER + 1
        steps = mod.plan(product, manifest, registry)
        if dry_run:
            print(f"{PREFIX} {slug}: {mod.NAME} (framework_version {version} -> {target})"
                  + ("" if steps else "  nada a migrar, só carimba a versão"))
            for st in steps:
                print(f"    {mod.describe(st)}")
            version = target
            continue
        when = now_stamp()
        if steps and backup_name is None:
            backup_name = backup_manifest(product, when)
        summary = {"rename": 0, "skip": 0, "manifest": 0, "note": 0}
        for st in steps:
            try:
                mod.apply(product, manifest, st)
            except Exception as e:      # falha num passo: registra, avisa e não carimba a versão
                log(product, when, mod.NAME, f"error   {mod.describe(st)}  ({e})")
                print(f"{PREFIX} {slug}: ERRO em {mod.NAME}: {mod.describe(st)} ({e})")
                failed = True
                break
            log(product, when, mod.NAME, mod.describe(st))
            summary[st["op"]] = summary.get(st["op"], 0) + 1
            if st["op"] == "skip":
                print(f"{PREFIX} {slug}: PULADO {st['src']}/ -> {st['dst']}/ ({st['reason']}; resolva à mão)")
        if failed:
            write_manifest(product, manifest, trailing)      # o que já mudou no dict fica gravado
            break
        manifest["framework_version"] = target
        write_manifest(product, manifest, trailing)
        tail = f"framework_version {version} -> {target}" + (f"  (backup {backup_name})" if backup_name else "")
        log(product, when, mod.NAME, ("done  " if steps else "done  nada a migrar  ") + tail)
        if steps:
            parts = []
            if summary["rename"]:
                parts.append(f"{summary['rename']} pasta{'s' if summary['rename'] > 1 else ''} renomeada{'s' if summary['rename'] > 1 else ''}")
            if summary["skip"]:
                parts.append(f"{summary['skip']} pulada{'s' if summary['skip'] > 1 else ''}")
            if summary["manifest"]:
                parts.append("skills_completed traduzido")
            print(f"{PREFIX} {slug}: {mod.NAME}: {', '.join(parts) or 'sem mudança'} ({tail})")
            changed = True
        elif verbose:
            print(f"{PREFIX} {slug}: {mod.NAME}: nada a migrar ({tail})")
        version = target
    return changed, failed


def main():
    ap = argparse.ArgumentParser(description="Aplica aos produtos de workspace/ as migrações de layout pendentes.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("Uso:")[1] if "Uso:" in __doc__ else None)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="todos os produtos de workspace/")
    g.add_argument("--product", metavar="SLUG", help="um produto só")
    g.add_argument("--list", action="store_true", help="lista as migrações conhecidas e sai")
    ap.add_argument("--dry-run", action="store_true", help="mostra o que faria, sem gravar")
    ap.add_argument("--verbose", action="store_true", help="lista também os produtos em dia")
    args = ap.parse_args()

    try:
        mods = load_migrations()
    except Exception as e:
        print(f"{PREFIX} ERRO ao carregar as migrações: {e}", file=sys.stderr)
        return 1
    if args.list:
        for m in mods:
            print(f"{m.NUMBER:03d}  {m.NAME}  (framework_version {m.NUMBER} -> {m.NUMBER + 1})  {m.SUMMARY}")
        print(f"versão atual do layout: {current_version(mods)}")
        return 0
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"{PREFIX} ERRO ao ler {REGISTRY.relative_to(ROOT)}: {e}", file=sys.stderr)
        return 1

    if not WORKSPACE.is_dir():
        if args.product or args.verbose or args.dry_run:
            print(f"{PREFIX} workspace/ não existe", file=sys.stderr)
            return 1
        return 0
    prods = products(args.product)
    if args.product and not prods:
        print(f"{PREFIX} produto não encontrado: workspace/{args.product}/manifest.json", file=sys.stderr)
        return 1
    if args.dry_run and not prods:
        print(f"{PREFIX} nenhum produto em workspace/")

    any_error = False
    for p in prods:
        _, err = migrate_product(p, mods, registry, args.dry_run, args.verbose)
        any_error = any_error or err
    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main())
