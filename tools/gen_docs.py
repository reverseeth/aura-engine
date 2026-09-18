#!/usr/bin/env python3
"""
gen_docs.py — gera os trechos de documentação derivados de `.claude/skills.json`.

O `skills.json` é o registro único das skills (identidade, ordem, gatilhos, pastas).
Este script lê o registro e reescreve os trechos marcados nos arquivos abaixo, para que
ordem, posição, gatilhos e ids das skills existam em UM lugar só e os outros sejam gerados:

  README.md                                   tabela de skills            gen:readme-table
  .claude/CLAUDE.md                           lista de gatilhos           gen:claude-triggers
  .claude/CLAUDE.md                           linha ORDEM LÓGICA          gen:claude-order
  .claude/lib/workspace-index/build_index.py  lista PHASES + LEGACY_FOLDERS gen:phases
  .claude/templates/manifest-schema.json      enum de skills_completed    manifest-enum (estrutural, sem marcador)
  .claude/OVERVIEW.md                         cabeçalho de cada skill §4  gen:skill-header:<id>[,<id>...]
  .claude/OVERVIEW.md                         ordem canônica do §13       gen:overview-order
  .claude/skills/<id>.md | <id>/SKILL.md      linha de título (H1)        gen:title
  .claude/OVERVIEW.html                       render do OVERVIEW.md       overview-html (arquivo inteiro,
                                              via tools/render_report.py; nunca editado à mão)

Marcadores:
  bloco     — `<!-- gen:X:start -->` ... `<!-- gen:X:end -->` em Markdown; `# gen:X:start` ... `# gen:X:end`
              em Python. Tudo entre os dois marcadores é substituído pelo texto gerado.
  em linha  — `<!-- gen:X -->` no fim de uma linha: a linha inteira é regenerada (o marcador fica no fim).

Uso:
  python3 tools/gen_docs.py            escreve o que estiver desatualizado e lista os arquivos alterados
  python3 tools/gen_docs.py --check    não escreve; exit 1 se algum trecho estiver desatualizado
  python3 tools/gen_docs.py --diff     mostra o diff do que mudaria, sem escrever
  python3 tools/gen_docs.py --only readme-table,phases

Só biblioteca padrão. Exit 0 = tudo em dia (ou tudo escrito); exit 1 = desatualizado, marcador ausente
ou registro inválido.
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "skills.json"

FILES = {
    "readme": ROOT / "README.md",
    "claude": ROOT / ".claude" / "CLAUDE.md",
    "build_index": ROOT / ".claude" / "lib" / "workspace-index" / "build_index.py",
    "schema": ROOT / ".claude" / "templates" / "manifest-schema.json",
    "overview": ROOT / ".claude" / "OVERVIEW.md",
    "overview_html": ROOT / ".claude" / "OVERVIEW.html",
}
TOOLS_DIR = Path(__file__).resolve().parent

LANES = ("sequence", "two-phase", "parallel", "side")
LANE_RANK = {"sequence": 0, "two-phase": 0, "parallel": 1, "side": 2}
PANEL_TAGS = (None, "post", "two", "opt", "side")


# ----------------------------------------------------------------------------- registro
class RegistryError(Exception):
    pass


def load_registry():
    if not REGISTRY.exists():
        raise RegistryError(f"registro não encontrado: {REGISTRY.relative_to(ROOT)}")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        raise RegistryError("skills.json sem a lista `skills`")
    errors = []
    ids, legacy, positions = set(), set(), {}
    for i, s in enumerate(skills):
        s["_index"] = i
        sid = s.get("id")
        if not sid or not re.fullmatch(r"[a-z][a-z0-9-]*", sid):
            errors.append(f"skill #{i}: id inválido {sid!r}")
            continue
        if sid in ids:
            errors.append(f"{sid}: id repetido")
        ids.add(sid)
        for lg in s.get("legacy_ids") or []:
            if lg in legacy:
                errors.append(f"{sid}: legacy_id {lg} repetido")
            legacy.add(lg)
        if not (ROOT / s.get("file", "")).exists():
            errors.append(f"{sid}: arquivo não existe: {s.get('file')}")
        lane = s.get("lane")
        if lane not in LANES:
            errors.append(f"{sid}: lane inválida {lane!r}")
        if lane == "two-phase":
            a, b = s.get("position_a"), s.get("position_b")
            if not (isinstance(a, int) and isinstance(b, int) and a < b):
                errors.append(f"{sid}: two-phase precisa de position_a < position_b")
            else:
                for p, tag in ((a, "A"), (b, "B")):
                    positions.setdefault(p, []).append(f"{sid} (Fase {tag})")
        else:
            p = s.get("position")
            if not isinstance(p, int) or p < 1:
                errors.append(f"{sid}: position inválida {p!r}")
            elif lane == "sequence":
                positions.setdefault(p, []).append(sid)
        if s.get("panel_tag") not in PANEL_TAGS:
            errors.append(f"{sid}: panel_tag inválido {s.get('panel_tag')!r}")
        cmd = s.get("panel_cmd")
        if cmd and cmd not in (s.get("triggers") or []):
            errors.append(f"{sid}: panel_cmd {cmd!r} não está em triggers")
        for k in ("title_pt", "title_en", "name"):
            if not s.get(k):
                errors.append(f"{sid}: campo {k} vazio")
        if not s.get("triggers"):
            errors.append(f"{sid}: sem triggers")
    if positions:
        want = list(range(1, max(positions) + 1))
        for p in want:
            who = positions.get(p, [])
            if len(who) != 1:
                errors.append(f"passo {p}: {'vazio' if not who else 'ocupado por ' + ' e '.join(who)}")
    # skills que compartilham pasta precisam compartilhar o card do painel
    by_folder = {}
    for s in skills:
        if s.get("folder"):
            by_folder.setdefault(s["folder"], []).append(s)
    for folder, group in by_folder.items():
        if len(group) > 1:
            cards = {g.get("panel_card") for g in group}
            if len(cards) != 1 or None in cards:
                errors.append(f"pasta {folder}: skills que a compartilham precisam do mesmo panel_card")
    for s in skills:
        for c in s.get("consumers") or []:
            if c not in ids:
                errors.append(f"{s['id']}: consumer desconhecido {c!r}")
    launch = data.get("launch_after")
    if launch not in ids:
        errors.append(f"launch_after aponta para skill desconhecida: {launch!r}")
    if errors:
        raise RegistryError("skills.json inválido:\n  " + "\n  ".join(errors))
    return data


# ----------------------------------------------------------------------------- helpers
def first_position(s):
    return s["position_a"] if s["lane"] == "two-phase" else s["position"]


def panel_position(s):
    return s["position_b"] if s["lane"] == "two-phase" else s["position"]


def sort_by_first(skills):
    return sorted(skills, key=lambda s: (first_position(s), LANE_RANK[s["lane"]], s["_index"]))


def sort_by_panel(skills):
    return sorted(skills, key=lambda s: (panel_position(s), LANE_RANK[s["lane"]], s["_index"]))


def legacy_label(s):
    return "/".join(s.get("legacy_ids") or []) or "sem apelido"


def passo_pt(s):
    lane = s["lane"]
    if lane == "sequence":
        return f"Passo {s['position']}"
    if lane == "two-phase":
        return f"Passo {s['position_a']} (Fase A) · Passo {s['position_b']} (Fase B)"
    if lane == "parallel":
        return "Paralela, opcional" if s.get("panel_tag") == "opt" else "Paralela"
    return "Lateral"


def step_en(s):
    lane = s["lane"]
    if lane == "sequence":
        return str(s["position"])
    if lane == "two-phase":
        return f"{s['position_a']} · {s['position_b']} (two-phase)"
    if lane == "parallel":
        return "parallel (optional)" if s.get("panel_tag") == "opt" else "parallel"
    return "side"


def py_str(v):
    return "None" if v is None else json.dumps(v, ensure_ascii=False)


def order_label(s):
    return s.get("order_label_pt") or s["triggers"][0]


# ----------------------------------------------------------------------------- renderizadores
def render_readme_table(data):
    lines = ["| Step | Skill | Legacy ID | Output |", "|---|---|---|---|"]
    for s in sort_by_first(data["skills"]):
        lines.append(f"| {step_en(s)} | {s['name']} (`{s['id']}`) | {legacy_label(s)} | {s['summary_en']} |")
    return "\n".join(lines)


def render_claude_triggers(data):
    lines = [
        "O membro pode acionar qualquer skill por nome. O id de cada skill é o slug (sem número); "
        "o número entre colchetes é o apelido antigo e continua roteando: se o membro disser um número, "
        "é o apelido antigo, roteie pelo `legacy_ids` do `.claude/skills.json`. \"Passo N\" é a posição na "
        "ordem canônica; \"Lateral\" é consulta fora da sequência; \"Paralela\" roda ao lado de um passo.",
        "",
    ]
    for s in sort_by_first(data["skills"]):
        trig = " / ".join(f'"{t}"' for t in s["triggers"])
        # Sem o resumo longo por skill: o CLAUDE.md enxuto (Fase 7) só roteia; a descrição
        # completa vive no frontmatter de cada skill e no §4 do OVERVIEW.md.
        lines.append(f"- {trig} → **{s['id']}** [{s['name']} · {passo_pt(s)} · apelido antigo: {legacy_label(s)}]")
    return "\n".join(lines)


def render_claude_order(data):
    skills = data["skills"]
    steps = []  # (pos, skill, fase)
    for s in skills:
        if s["lane"] == "sequence":
            steps.append((s["position"], s, None))
        elif s["lane"] == "two-phase":
            steps.append((s["position_a"], s, "A"))
            steps.append((s["position_b"], s, "B"))
    steps.sort(key=lambda t: t[0])
    parallel_after = {}
    for s in skills:
        if s["lane"] == "parallel":
            parallel_after.setdefault(s["position"], []).append(s)

    def note_of(s, fase):
        n = s.get("order_note_pt")
        if isinstance(n, dict):
            return n.get(fase.lower()) if fase else None
        return n

    def item(pos, s, fase):
        label = order_label(s) + (f", Fase {fase}" if fase else "")
        note = note_of(s, fase)
        body = f"{label} (Passo {pos}" + (f": {note}" if note else "") + ")"
        return body, bool(note)

    parts = []
    i = 0
    while i < len(steps):
        pos, s, fase = steps[i]
        group = s.get("group_pt") if fase is None else ("PÓS-LAUNCH" if fase == "B" else None)
        if group:
            j = i
            members = []
            while j < len(steps):
                pj, sj, fj = steps[j]
                gj = sj.get("group_pt") if fj is None else ("PÓS-LAUNCH" if fj == "B" else None)
                if gj != group:
                    break
                members.append(item(pj, sj, fj)[0])
                j += 1
            parts.append(f"**{group}: " + " → ".join(members) + "**")
            last_pos = steps[j - 1][0]
            i = j
        else:
            body, bold = item(pos, s, fase)
            parts.append(f"**{body}**" if bold else body)
            last_pos = pos
            i += 1
        for p in parallel_after.get(last_pos, []):
            note = note_of(p, None)
            parts.append(f"**(paralela: {order_label(p)}" + (f", {note}" if note else "") + ")**")
    return "ORDEM LÓGICA DE EXECUÇÃO: " + " → ".join(parts) + "."


def render_phases(data):
    rows, seen_cards = [], set()
    for s in sort_by_panel(data["skills"]):
        card = s.get("panel_card")
        if card:
            if card in seen_cards:
                continue
            seen_cards.add(card)
            sid = card
        else:
            sid = s["legacy_ids"][0]
        folder = s.get("folder") or s["id"]
        names = {"pt-BR": s.get("panel_title_pt") or s["title_pt"], "en": s.get("panel_title_en") or s["title_en"]}
        rows.append(f"    ({py_str(sid)}, {py_str(folder)}, {{\"pt-BR\": {py_str(names['pt-BR'])}, "
                    f"\"en\": {py_str(names['en'])}}}, {py_str(s.get('panel_cmd'))}, {py_str(s.get('panel_tag'))}),")
    # pasta numerada antiga de cada fase: o painel lê dela por um ciclo (produto ainda não migrado)
    legacy = {}
    for s in sort_by_panel(data["skills"]):
        if s.get("folder") and s.get("legacy_folder") and s["legacy_folder"] != s["folder"]:
            legacy.setdefault(s["folder"], s["legacy_folder"])
    legacy_rows = [f"    {py_str(k)}: {py_str(v)}," for k, v in legacy.items()]
    return ("PHASES = [\n" + "\n".join(rows) + "\n]\n"
            "LEGACY_FOLDERS = {\n" + "\n".join(legacy_rows) + "\n}")


def render_enum(data):
    """Enum de `skills_completed`: só os ids do registro, na ordem canônica. A forma antiga com o
    número na frente saiu na Fase 5c (os manifests são traduzidos pela migração 001 do migrate.py)."""
    return [s["id"] for s in sort_by_first(data["skills"])]


def render_skill_header(data, ids_csv):
    by_id = {s["id"]: s for s in data["skills"]}
    ids = [x.strip() for x in ids_csv.split(",") if x.strip()]
    missing = [x for x in ids if x not in by_id]
    if missing:
        raise RegistryError(f"marcador gen:skill-header cita skill desconhecida: {missing}")
    group = [by_id[x] for x in ids]
    if len(group) == 1:
        s = group[0]
        return f"### {s['name']} · {passo_pt(s)} · apelido antigo: {legacy_label(s)}"
    positions = [first_position(s) for s in group]
    title = (group[0].get("group_pt") or "Grupo").capitalize()
    names = " → ".join(s["name"] for s in group)
    legs = " → ".join(legacy_label(s) for s in group)
    return f"### {title} · Passos {min(positions)} a {max(positions)} · {names} · apelidos antigos: {legs}"


def render_overview_order(data):
    skills = data["skills"]
    launch_after = data["launch_after"]
    steps = []
    for s in skills:
        if s["lane"] == "sequence":
            steps.append((s["position"], s, None))
        elif s["lane"] == "two-phase":
            steps.append((s["position_a"], s, "A"))
            steps.append((s["position_b"], s, "B"))
    steps.sort(key=lambda t: t[0])
    attached = {}
    for s in skills:
        if s["lane"] in ("parallel", "side"):
            attached.setdefault(s["position"], []).append(s)

    def note_of(s, fase):
        n = s.get("step_note_pt")
        if isinstance(n, dict):
            return n.get(fase.lower(), "") if fase else ""
        return n or ""

    lines = []
    for pos, s, fase in steps:
        label = s["triggers"][0] + (f", Fase {fase}" if fase else "")
        note = note_of(s, fase)
        lines.append(f"{pos}. **{label}**" + (f": {note}" if note else ""))
        for a in sorted(attached.get(pos, []), key=lambda x: (LANE_RANK[x['lane']], x['_index'])):
            kind = "paralela, opcional" if (a["lane"] == "parallel" and a.get("panel_tag") == "opt") else (
                "paralela" if a["lane"] == "parallel" else "lateral")
            n = note_of(a, None)
            lines.append(f"   - *{kind}:* **{a['name']}**" + (f": {n}" if n else ""))
        if fase is None and s["id"] == launch_after:
            lines.append("")
            lines.append("**LAUNCH**")
            lines.append("")
    return "\n".join(lines)


def render_title(s):
    return f"# {s['name']} · {passo_pt(s)} · apelido antigo: {legacy_label(s)}"


# ----------------------------------------------------------------------------- aplicação
def block_markers(kind, key):
    if kind == "py":
        return f"# gen:{key}:start", f"# gen:{key}:end"
    return f"<!-- gen:{key}:start -->", f"<!-- gen:{key}:end -->"


def replace_block(text, key, new_body, kind="md", path=None):
    start, end = block_markers(kind, key)
    lines = text.split("\n")
    try:
        i = next(n for n, l in enumerate(lines) if l.strip() == start)
        j = next(n for n, l in enumerate(lines) if l.strip() == end and n > i)
    except StopIteration:
        raise RegistryError(f"marcador ausente em {path}: {start} / {end}")
    return "\n".join(lines[: i + 1] + new_body.split("\n") + lines[j:])


INLINE_RE = re.compile(r"\s*<!-- gen:([a-z-]+)(?::([^ >]+))? -->\s*$")


def replace_inline(text, key, render_fn, path=None, require=True):
    lines = text.split("\n")
    hits = 0
    for n, l in enumerate(lines):
        m = INLINE_RE.search(l)
        if not m or m.group(1) != key:
            continue
        param = m.group(2)
        lines[n] = render_fn(param) + f" <!-- gen:{key}" + (f":{param}" if param else "") + " -->"
        hits += 1
    if require and hits == 0:
        raise RegistryError(f"marcador ausente em {path}: <!-- gen:{key} -->")
    return "\n".join(lines)


class Texts:
    """Cache de textos por arquivo: vários alvos podem mexer no mesmo arquivo antes de gravar."""

    def __init__(self):
        self.orig, self.cur = {}, {}

    def get(self, path):
        if path not in self.cur:
            self.orig[path] = self.cur[path] = path.read_text(encoding="utf-8") if path.exists() else ""
        return self.cur[path]

    def set(self, path, new):
        self.cur[path] = new


def target_readme_table(data, tx):
    p = FILES["readme"]
    tx.set(p, replace_block(tx.get(p), "readme-table", render_readme_table(data), "md", p.name))


def target_claude_triggers(data, tx):
    p = FILES["claude"]
    tx.set(p, replace_block(tx.get(p), "claude-triggers", render_claude_triggers(data), "md", p.name))


def target_claude_order(data, tx):
    p = FILES["claude"]
    tx.set(p, replace_block(tx.get(p), "claude-order", render_claude_order(data), "md", p.name))


def target_phases(data, tx):
    p = FILES["build_index"]
    tx.set(p, replace_block(tx.get(p), "phases", render_phases(data), "py", p.name))


def target_manifest_enum(data, tx):
    p = FILES["schema"]
    schema = json.loads(tx.get(p))
    try:
        items = schema["properties"]["skills_completed"]["items"]
    except KeyError:
        raise RegistryError("manifest-schema.json sem properties.skills_completed.items")
    items["enum"] = render_enum(data)
    tx.set(p, json.dumps(schema, indent=2, ensure_ascii=False) + "\n")


def target_overview_headers(data, tx):
    p = FILES["overview"]
    new = replace_inline(tx.get(p), "skill-header", lambda param: render_skill_header(data, param or ""), p.name)
    # toda skill do registro precisa aparecer em algum cabeçalho do §4
    cited = set()
    for m in re.finditer(r"<!-- gen:skill-header:([^ >]+) -->", new):
        cited.update(x.strip() for x in m.group(1).split(","))
    missing = [s["id"] for s in data["skills"] if s["id"] not in cited]
    if missing:
        raise RegistryError(f"OVERVIEW.md §4 sem cabeçalho gerado para: {', '.join(missing)} "
                            f"(acrescente uma linha `### x <!-- gen:skill-header:<id> -->`)")
    tx.set(p, new)


def target_overview_order(data, tx):
    p = FILES["overview"]
    tx.set(p, replace_block(tx.get(p), "overview-order", render_overview_order(data), "md", p.name))


def target_skill_titles(data, tx):
    for s in data["skills"]:
        p = ROOT / s["file"]
        tx.set(p, replace_inline(tx.get(p), "title", lambda _param, s=s: render_title(s), s["file"]))


def target_overview_html(data, tx):
    """O OVERVIEW.html é o render do OVERVIEW.md (tools/render_report.py) e nunca é editado à mão.
    Renderiza o texto já atualizado pelos alvos anteriores (cabeçalhos do §4 e ordem do §13)."""
    if str(TOOLS_DIR) not in sys.path:
        sys.path.insert(0, str(TOOLS_DIR))
    try:
        import render_report
    except ImportError as e:
        raise RegistryError(f"tools/render_report.py indisponível: {e}")
    src, dst = FILES["overview"], FILES["overview_html"]
    tx.get(dst)
    try:
        tx.set(dst, render_report.render_document(tx.get(src), source=src))
    except render_report.RenderError as e:
        raise RegistryError(f"render do OVERVIEW.md falhou: {e}")


TARGETS = {
    "readme-table": target_readme_table,
    "claude-triggers": target_claude_triggers,
    "claude-order": target_claude_order,
    "phases": target_phases,
    "manifest-enum": target_manifest_enum,
    "overview-headers": target_overview_headers,
    "overview-order": target_overview_order,
    "skill-titles": target_skill_titles,
    "overview-html": target_overview_html,
}


def main():
    ap = argparse.ArgumentParser(description="Gera os trechos de documentação derivados de .claude/skills.json.",
                                 epilog="Alvos: " + ", ".join(TARGETS))
    ap.add_argument("--check", action="store_true", help="não escreve; exit 1 se algo estiver desatualizado")
    ap.add_argument("--diff", action="store_true", help="mostra o diff do que mudaria, sem escrever")
    ap.add_argument("--only", default="", help="lista de alvos separados por vírgula")
    args = ap.parse_args()

    try:
        data = load_registry()
    except (RegistryError, json.JSONDecodeError) as e:
        print(f"ERRO  {e}", file=sys.stderr)
        return 1

    names = [x.strip() for x in args.only.split(",") if x.strip()] or list(TARGETS)
    unknown = [n for n in names if n not in TARGETS]
    if unknown:
        print(f"ERRO  alvo desconhecido: {', '.join(unknown)} (válidos: {', '.join(TARGETS)})", file=sys.stderr)
        return 1

    tx = Texts()
    stale = []  # (alvo, arquivo) — alvo cujo trecho estava diferente do gerado
    failed = False
    for name in names:
        before = dict(tx.cur)
        try:
            TARGETS[name](data, tx)
        except RegistryError as e:
            print(f"ERRO  {e}", file=sys.stderr)
            failed = True
            continue
        for path, text in tx.cur.items():
            if before.get(path, tx.orig[path]) != text:
                stale.append((name, path))
    if failed:
        return 1

    changed = [(p, tx.orig[p], tx.cur[p]) for p in tx.cur if tx.orig[p] != tx.cur[p]]
    if args.diff:
        for p, o, n in changed:
            sys.stdout.writelines(difflib.unified_diff(o.splitlines(True), n.splitlines(True),
                                                       fromfile=str(p.relative_to(ROOT)),
                                                       tofile=str(p.relative_to(ROOT)) + " (gerado)"))
        print("OK" if not changed else f"{len(changed)} arquivo(s) mudariam")
        return 0 if not changed else 1
    if args.check:
        if not changed:
            print("OK")
            return 0
        for name, p in stale:
            print(f"DESATUALIZADO  {p.relative_to(ROOT)}  ({name})")
        print(f"{len(stale)} trecho(s) desatualizado(s). Rode: python3 tools/gen_docs.py")
        return 1
    for p, o, n in changed:
        p.write_text(n, encoding="utf-8")
        print(f"atualizado  {p.relative_to(ROOT)}")
    if not changed:
        print("OK  nada a mudar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
