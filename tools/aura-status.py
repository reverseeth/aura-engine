#!/usr/bin/env python3
"""
aura-status.py: estado verificável de um produto do workspace. Não altera nada.

Cruza três fontes e aponta onde elas divergem: o `manifest.json` (o que as skills marcaram como
feito), os arquivos da pasta do produto (o que existe de fato) e o layout canônico (o que cada
skill declara escrever no `.claude/skills.json`, mais a infraestrutura de
`.claude/lib/workspace-index/workspace-layout.md`). Para cada fase mostra se o relatório existe
e se a skill está marcada, e lista:

  - fase marcada em `skills_completed` sem nenhum artefato na pasta;
  - artefato de uma fase presente sem a marca no manifest (o ES3 da rule de escape paths:
    `python3 tools/manifest.py <slug> complete <skill-id>` reconcilia);
  - arquivo ou pasta fora do layout canônico;
  - `dados.json` que falha no schema da fase (`.claude/templates/schemas/<id>.dados.schema.json`);
  - manifest ausente, que não parseia ou que falha no `manifest-schema.json`.

Além das issues, imprime avisos informativos, por produto e por fase. Hoje há um: `dados.json` de
uma fase cujo schema prevê o bloco `resumo` e que não tem o bloco no arquivo, porque a fase
seguinte vai ler o arquivo inteiro em vez do resumo. Aviso não é falha: não conta como issue, não
muda o exit code e não aparece no painel do workspace.

Uso:
  python3 tools/aura-status.py <slug>            um produto, texto legível
  python3 tools/aura-status.py --all             todos os produtos de workspace/
  python3 tools/aura-status.py <slug> --json     saída em JSON (o painel e o hook leem daqui)
  python3 tools/aura-status.py <slug> --brief    até 10 linhas com prefixo [aura-status] (modo do hook)

Como módulo (o `build_index.py` importa a leitura de estado daqui):
  state = aura_status.product_state(product_dir)   # dict com manifest, fases, relatórios, issues e avisos

A variável de ambiente AURA_WORKSPACE aponta para outra pasta de workspace (só para testes).
Só biblioteca padrão. Exit 0 = rodou (com ou sem issues); 1 = não conseguiu rodar (workspace ou
produto inexistente, registro ilegível).
"""
import argparse
import fnmatch
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
WORKSPACE = Path(os.environ["AURA_WORKSPACE"]) if os.environ.get("AURA_WORKSPACE") else ROOT / "workspace"
REGISTRY = ROOT / ".claude" / "skills.json"
MANIFEST_SCHEMA = ROOT / ".claude" / "templates" / "manifest-schema.json"
DADOS_SCHEMAS = ROOT / ".claude" / "templates" / "schemas"
PREFIX = "[aura-status]"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import schema_validate  # noqa: E402

# Relatório humano de cada fase: <folder>/<report_stem>.html; nomes legados aceitos por um ciclo.
LEGACY_REPORTS = ["relatorio.html"]
LEGACY_PAGE_REPORTS = ["07-page.html"]
# Arquivos de infraestrutura na raiz do produto (não são fase).
ROOT_INFRA = {"manifest.json", "brand.md", "ABRIR-AQUI.html", "ad-log.md", "troubleshooting-log.md",
              "escape-paths-log.json"}
ROOT_INFRA_DIRS = {"brand", "creative-dna"}
# Permitidos dentro de qualquer pasta de fase (artefatos de runtime das rules e nomes legados).
PHASE_EXTRAS = ["iterations-log.json", ".partial-state.json", "relatorio.md", "relatorio.html"]
PAGE_LEGACY = ["07-page.html", "07-plan.json", "07-design-system.md", "07-design-system.html", "07-deploy-report.json"]
# Fases cuja marca no manifest só entra num status específico do dados.json (sourcing: cotação fechada).
MANIFEST_ONLY = {"sourcing": ("status", "closed")}
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}
# Escritas do registro que não são artefato da fase (infra ou arquivo de outro dono).
NOT_ARTIFACT = {"manifest.json", "../profile.md", "../profile.html", "ABRIR-AQUI.html", "ad-log.md", "brand.md",
                "creative-dna/"}


# ----------------------------------------------------------------------------- registro
def load_registry():
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return reg["skills"]


def pattern_of(write):
    """Converte um caminho do registro (`creative-engine/concept-NN.md`, `retention-engine/[fluxo]/email-N.html`)
    num padrão fnmatch."""
    p = re.sub(r"\[[^\]]*\]|<[^>]*>", "*", write)
    p = p.replace("AAAA-MM-DD", "*").replace("NN", "*")
    p = re.sub(r"-N(?=\.)", "-*", p)
    return p


def phase_specs(skills):
    """Uma entrada por skill com pasta: padrões de artefato, relatório, tag."""
    specs = []
    for s in skills:
        folder = s.get("folder")
        if not folder:
            continue
        writes = [w for w in (s.get("writes") or []) if w not in NOT_ARTIFACT]
        specs.append({
            "id": s["id"], "folder": folder, "legacy_folder": s.get("legacy_folder"),
            "report_stem": s.get("report_stem") or folder, "lane": s.get("lane"), "tag": s.get("panel_tag"),
            "title_pt": s.get("title_pt"), "title_en": s.get("title_en"), "cmd": s.get("panel_cmd"),
            "artifact_patterns": [pattern_of(w) for w in writes],
        })
    return specs


# ----------------------------------------------------------------------------- leitura do produto
def read_manifest(product):
    """(manifest|None, erro|None)."""
    path = product / "manifest.json"
    if not path.is_file():
        return None, "manifest.json ausente"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"manifest.json não parseia ({e})"
    if not isinstance(data, dict):
        return None, "manifest.json não é um objeto JSON"
    return data, None


def completed_ids(manifest):
    out = []
    for v in (manifest or {}).get("skills_completed") or []:
        out.append(re.sub(r"^\d{2}[a-e]?-", "", str(v)))
    return out


def phase_dirs(spec):
    dirs = [spec["folder"]]
    if spec["legacy_folder"] and spec["legacy_folder"] != spec["folder"]:
        dirs.append(spec["legacy_folder"])
    return dirs


def find_report(product, spec):
    names = [f"{spec['report_stem']}.html"] + (LEGACY_PAGE_REPORTS if spec["folder"] == "page" else LEGACY_REPORTS)
    for d in phase_dirs(spec):
        for n in names:
            if (product / d / n).is_file():
                return f"{d}/{n}"
    return None


def list_files(product, folder):
    base = product / folder
    if not base.is_dir():
        return []
    out = []
    for p in base.rglob("*"):
        if p.name in IGNORED_NAMES or any(part == "__pycache__" for part in p.parts):
            continue
        rel = p.relative_to(product).as_posix()
        out.append(rel + ("/" if p.is_dir() else ""))
    return out


def matches(rel, patterns):
    for pat in patterns:
        if pat.endswith("/"):
            if rel == pat or rel.startswith(pat):
                return True
        elif fnmatch.fnmatchcase(rel.rstrip("/"), pat):
            return True
    return False


def artifacts_present(product, spec):
    """Caminhos (relativos ao produto) de artefatos desta skill que existem."""
    found = []
    for d in phase_dirs(spec):
        for rel in list_files(product, d):
            if rel.endswith("/"):
                continue
            pats = spec["artifact_patterns"]
            if d != spec["folder"]:   # pasta numerada antiga: os mesmos padrões com o prefixo antigo
                pats = [p.replace(spec["folder"] + "/", d + "/", 1) for p in pats]
            if matches(rel, pats):
                found.append(rel)
    return found


def sourcing_closed(product, spec):
    key, value = MANIFEST_ONLY[spec["id"]]
    for d in phase_dirs(spec):
        p = product / d / "dados.json"
        if p.is_file():
            try:
                return json.loads(p.read_text(encoding="utf-8")).get(key) == value
            except (OSError, ValueError):
                return False
    return False


def dados_check(product, spec):
    """(caminho relativo|None, falhas|None). None em falhas = sem schema ou sem arquivo."""
    schema = DADOS_SCHEMAS / f"{spec['id']}.dados.schema.json"
    for d in phase_dirs(spec):
        p = product / d / "dados.json"
        if p.is_file():
            rel = f"{d}/dados.json"
            if not schema.is_file():
                return rel, None
            return rel, schema_validate.validate_file(p, schema)
    return None, None


_SCHEMA_CACHE = {}


def schema_of(skill_id):
    """Schema de fase (dict) ou None. Cache por id."""
    if skill_id not in _SCHEMA_CACHE:
        path = DADOS_SCHEMAS / f"{skill_id}.dados.schema.json"
        try:
            _SCHEMA_CACHE[skill_id] = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
        except (OSError, ValueError):
            _SCHEMA_CACHE[skill_id] = None
    return _SCHEMA_CACHE[skill_id]


def expects_resumo(skill_id):
    """True quando o schema da fase prevê o bloco `resumo` (as fases produtoras da Fase 9e)."""
    schema = schema_of(skill_id)
    return bool(schema) and "resumo" in (schema.get("properties") or {})


def resumo_missing(product, rel):
    """True quando o `dados.json` existe, parseia e não tem o bloco `resumo`. Arquivo ilegível não vira
    aviso: quem acusa isso é o schema, como issue."""
    try:
        data = json.loads((product / rel).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and "resumo" not in data


def layout_extras(product, specs):
    """Arquivos e pastas fora do layout canônico. Pasta desconhecida inteira vira uma linha só."""
    allowed_by_folder = {}
    for s in specs:
        for d in phase_dirs(s):
            pats = allowed_by_folder.setdefault(d, [])
            base = s["artifact_patterns"]
            if d != s["folder"]:
                base = [p.replace(s["folder"] + "/", d + "/", 1) for p in base]
            pats.extend(base)
            pats.append(f"{d}/dados.json")
            pats.extend(f"{d}/{x}" for x in PHASE_EXTRAS)
            if s["folder"] == "page":
                pats.extend(f"{d}/{x}" for x in PAGE_LEGACY)
    extras = []
    for entry in sorted(product.iterdir()):
        name = entry.name
        if name in IGNORED_NAMES or name.startswith("."):
            continue                      # backups, logs, snapshots e arquivos ocultos são infra
        if entry.is_file():
            if name not in ROOT_INFRA:
                extras.append(name)
            continue
        if name in ROOT_INFRA_DIRS:
            continue
        if name not in allowed_by_folder:
            extras.append(name + "/")
            continue
        pats = allowed_by_folder[name]
        seen_dirs = []
        for rel in list_files(product, name):
            if any(rel.startswith(d) for d in seen_dirs):
                continue                  # já listamos a pasta inteira
            if matches(rel, pats):
                continue
            if rel.endswith("/"):
                # pasta que contém algo permitido não é "extra" inteira; senão, lista a pasta e pula o conteúdo
                inside = [x for x in list_files(product, rel.rstrip("/")) if not x.endswith("/")]
                if inside and not any(matches(x, pats) for x in inside):
                    extras.append(rel)
                    seen_dirs.append(rel)
                elif not inside:
                    extras.append(rel)
                    seen_dirs.append(rel)
                continue
            extras.append(rel)
    return extras


# ----------------------------------------------------------------------------- estado
def product_state(product, skills=None):
    product = Path(product)
    skills = skills if skills is not None else load_registry()
    specs = phase_specs(skills)
    manifest, merr = read_manifest(product)
    completed = completed_ids(manifest)
    issues = []
    if merr:
        issues.append({"kind": "manifest", "phase": None, "path": "manifest.json", "msg": merr})
    else:
        try:
            for f in schema_validate.validate(manifest, json.loads(MANIFEST_SCHEMA.read_text(encoding="utf-8"))):
                path, _, msg = f.partition(": ")
                issues.append({"kind": "manifest_schema", "phase": None, "path": "manifest.json",
                               "msg": f"{path} {msg}"})
        except (OSError, ValueError) as e:
            issues.append({"kind": "manifest", "phase": None, "path": str(MANIFEST_SCHEMA), "msg": f"schema ilegível ({e})"})
    notes = []
    phases, reports = [], {}
    for spec in specs:
        report = find_report(product, spec)
        reports.setdefault(spec["folder"], None)
        if report and (spec["folder"] != "page" or spec["id"] == "page-build"):
            reports[spec["folder"]] = report
        present = artifacts_present(product, spec)
        marked = spec["id"] in completed
        dados_rel, dados_fails = dados_check(product, spec)
        row = {"id": spec["id"], "folder": spec["folder"], "lane": spec["lane"], "tag": spec["tag"],
               "report": report, "marked": marked, "artifacts": present,
               "dados": dados_rel, "dados_fails": dados_fails}
        phases.append(row)
        if marked and not present:
            issues.append({"kind": "marked_without_artifact", "phase": spec["id"], "path": spec["folder"] + "/",
                           "msg": f"{spec['id']}: marcada em skills_completed, mas nenhum artefato em {spec['folder']}/"})
        elif present and not marked and not merr:
            if spec["id"] in MANIFEST_ONLY and not sourcing_closed(product, spec):
                pass                  # sourcing em cotação: a marca só entra quando fecha
            else:
                issues.append({"kind": "artifact_without_mark", "phase": spec["id"], "path": present[0],
                               "msg": f"{spec['id']}: artefato presente ({present[0]}) sem marca em skills_completed"})
        if dados_rel and expects_resumo(spec["id"]) and resumo_missing(product, dados_rel):
            notes.append({"kind": "dados_sem_resumo", "phase": spec["id"], "path": dados_rel,
                          "msg": f"{spec['id']} ({dados_rel}) sem bloco resumo: "
                                 "a fase seguinte vai ler o arquivo inteiro"})
        if dados_fails:
            issues.append({"kind": "dados_invalid", "phase": spec["id"], "path": dados_rel,
                           "msg": f"{dados_rel} falha no schema ({len(dados_fails)} problema(s)): " + "; ".join(dados_fails[:3])
                                  + (" ..." if len(dados_fails) > 3 else ""),
                           "fails": dados_fails})
    for rel in layout_extras(product, specs):
        issues.append({"kind": "outside_layout", "phase": None, "path": rel, "msg": f"fora do layout canônico: {rel}"})
    return {"slug": product.name, "product_name": (manifest or {}).get("product_name") or product.name,
            "manifest": manifest, "manifest_error": merr, "completed": completed,
            "phases": phases, "reports": reports, "issues": issues, "notes": notes}


def products(slug=None):
    if slug:
        p = WORKSPACE / slug
        return [p] if p.is_dir() else []
    if not WORKSPACE.is_dir():
        return []
    return sorted(p for p in WORKSPACE.iterdir() if p.is_dir() and (p / "manifest.json").is_file())


# ----------------------------------------------------------------------------- saída
def render_text(state):
    lines = []
    n_marked = len(state["completed"])
    n_reports = sum(1 for r in state["phases"] if r["report"])
    n_notes = len(state.get("notes") or [])
    lines.append(f"{PREFIX} {state['slug']} ({state['product_name']}) · {n_marked} skill(s) marcada(s) · "
                 f"{n_reports} relatório(s) · {len(state['issues'])} issue(s)"
                 + (f" · {n_notes} aviso(s)" if n_notes else ""))
    if state["manifest_error"]:
        lines.append(f"  manifest: {state['manifest_error']}")
    lines.append(f"  {'fase':22s} {'relatório':10s} {'manifest':9s} {'dados.json'}")
    seen_page = False
    for r in state["phases"]:
        if r["folder"] == "page":
            if seen_page and r["id"] == "page-build":
                pass
            seen_page = True
        rep = "ok" if r["report"] else "-"
        mark = "ok" if r["marked"] else "-"
        if r["dados"] is None:
            dados = "-"
        elif r["dados_fails"] is None:
            dados = "presente"
        elif r["dados_fails"]:
            dados = f"FALHA ({len(r['dados_fails'])})"
        else:
            dados = "válido"
        lines.append(f"  {r['id']:22s} {rep:10s} {mark:9s} {dados}")
    if state["issues"]:
        lines.append("  issues:")
        for it in state["issues"]:
            lines.append(f"  - {it['msg']}")
    if state.get("notes"):
        lines.append("  avisos (informativos, não são falha):")
        for note in state["notes"]:
            lines.append(f"  - {note['msg']}")
    return "\n".join(lines)


def render_brief(state, limit=10):
    """Modo do hook: até `limit` linhas, cada uma com o prefixo. Issues primeiro; os avisos entram no
    espaço que sobrar."""
    notes = state.get("notes") or []
    head = (f"{PREFIX} {state['slug']}: {len(state['completed'])} skill(s) marcada(s), "
            f"{sum(1 for r in state['phases'] if r['report'])} relatório(s), {len(state['issues'])} issue(s)"
            + (f", {len(notes)} aviso(s)" if notes else ""))
    lines = [head]
    pending = list(state["issues"]) + notes
    for i, it in enumerate(pending):
        if len(lines) >= limit:
            rest = len(pending) - i + 1
            lines[-1] = f"{PREFIX} ... e mais {rest} linha(s): python3 tools/aura-status.py {state['slug']}"
            break
        lines.append(f"{PREFIX} {it['msg']}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Estado verificável de um produto do workspace (não altera nada).",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("Uso:")[1])
    ap.add_argument("slug", nargs="?", help="pasta do produto em workspace/")
    ap.add_argument("--all", action="store_true", help="todos os produtos de workspace/")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--brief", action="store_true", help="até 10 linhas com prefixo [aura-status] (modo do hook)")
    args = ap.parse_args()
    if not args.slug and not args.all:
        ap.error("informe um <slug> ou --all")
    try:
        skills = load_registry()
    except (OSError, ValueError, KeyError) as e:
        print(f"{PREFIX} ERRO ao ler {REGISTRY.relative_to(ROOT)}: {e}", file=sys.stderr)
        return 1
    if not WORKSPACE.is_dir():
        print(f"{PREFIX} workspace/ não existe", file=sys.stderr)
        return 1
    prods = products(None if args.all else args.slug)
    if not prods:
        print(f"{PREFIX} produto não encontrado: workspace/{args.slug}" if args.slug else f"{PREFIX} nenhum produto em workspace/",
              file=sys.stderr)
        return 1
    states = [product_state(p, skills) for p in prods]
    if args.json:
        print(json.dumps(states if args.all else states[0], ensure_ascii=False, indent=2))
    elif args.brief:
        print("\n".join(render_brief(s) for s in states))
    else:
        print("\n\n".join(render_text(s) for s in states))
    return 0


if __name__ == "__main__":
    sys.exit(main())
