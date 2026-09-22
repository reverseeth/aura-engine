#!/usr/bin/env python3
"""
aura-check.py: lint do framework Aura Engine.

Roda da raiz do repositório e confere a consistência mecânica do framework (nunca o
conteúdo metodológico). Cada falha sai numa linha `ARQUIVO:LINHA  REGRA  mensagem`.
No fim imprime `OK` (exit 0) ou `N falhas` (exit 1).

Regras:
  paths          referência entre crases a `.claude/...`, `tools/...` ou `docs/...` (em .md, .json,
                 .py e .sh rastreados) aponta para arquivo ou pasta existente. Ignora padrões com
                 `[`, `<`, `{` ou `*` e os que começam com `workspace/`. Exceção: `.claude/.no-auto-update`.
  queries        nas skills, frase entre crases com 4 ou mais palavras (que não seja comando nem
                 caminho) que casa com uma `best_query` do índice em 80% das palavras, mas não
                 exatamente, é query digitada errada.
  skill-ids      número de skill só vive em `legacy_ids`/`legacy_folder` do registro, em
                 `use_in_skill` do índice e no changelog do OVERVIEW (§14). Em qualquer outro lugar,
                 número como identificador de skill é falha: pasta ou arquivo `NN-slug` (com qualquer
                 número), a forma abreviada `NN-<começo do slug>` (`04-offer`, `06-copy`) quando o
                 número é o apelido daquela skill, `skill NN`, `skill-NN`, `(NN)` depois do nome de uma skill, apelido com letra
                 solto (`07a`), `a NN`/`da NN`/`pela NN`/`→ NN` fora de contexto numérico, lista ligada
                 a um desses e faixa entre apelidos (`skills 00-20`). O filtro de contexto numérico
                 (o que separa "a 08" de "chega a 12") é o do `tools/migrate_ids.py`, importado: tudo
                 que aquele script converteria é falha aqui. Número em contexto numérico nunca é
                 candidato (dígito colado antes ou depois, vírgula ou ponto seguidos de dígito, %,
                 moeda, unidade colada, data AAAA-MM-DD, barra com dígito dos dois lados, palavra de
                 quantidade depois: "12,000 reviews", "18,7%", "$12", "20% do budget", "2026-09-01",
                 "11/11", "10 alternativas"); só número isolado como palavra ("a 08", "skill 12") conta. A
                 regra de palavra isolada vive no `migrate_ids.py` (ISOLATED_BEFORE/ISOLATED_AFTER),
                 com testes em `tools/tests/test_migrate_ids.py`. Também confere: `file`, `consumers` e
                 `launch_after` do registro; cada arquivo de skill (`.claude/skills/<id>.md` ou
                 `<id>/SKILL.md`) com entrada; o enum de
                 `skills_completed` só com ids; os apelidos citados em `use_in_skill`. Ficam fora:
                 trechos gerados (`gen:`), linhas com "apelido antigo" ou `SUPERSEDED`, a seção
                 "Produtos legados" do layout, o catálogo `kb-index/`, o `OVERVIEW.html` (gerado do
                 .md pelo gen_docs.py), o código que cita os nomes antigos de propósito (ALIAS_AWARE_FILES e
                 este lint), os campos do manifest com número no nome (MANIFEST_NUMERIC_FIELDS) e os
                 nomes legados de relatório de LEGACY_REPORT_NAMES (lista do migrate_ids.py, uma só
                 para o lint e o conversor).
  counts         nas skills, "N sistemas" / "N entradas" ao lado do nome de um domínio bate com a
                 contagem real do `frameworks.json`.
  removed-terms  termos do modelo antigo de policy/compliance não aparecem em skills, rules, libs,
                 templates, CLAUDE.md e OVERVIEW.md (exceto `kb-index/` e o changelog do OVERVIEW).
  sections       "ETAPA N", "GATE N", "ES N" e "Regra N" citados numa skill ou rule existem como
                 cabeçalho (ETAPA/GATE no mesmo arquivo ou na skill citada ao lado; ES na rule de
                 escape paths, que também precisa ter numeração contígua; Regra no CLAUDE.md).
  skill-size     cada `SKILL.md` do registro cabe em 12 KB (12.288 bytes): é o roteiro curto, e o
                 material longo vive em `reference/<tema>.md`. Quando a regra passa, ela ainda
                 imprime um aviso por skill com 300 bytes ou menos de folga — serve pra quem VAI
                 escrever saber antes de escrever, e não muda o código de saída.
  secrets        nenhum arquivo rastreado contém a chave antiga da base, `?key=` na URL da base
                 nem os padrões de token do pre-commit guard.
  member-data    nenhum arquivo rastreado contém nome de produto, loja ou marca do workspace do
                 membro (regra 11 do CLAUDE.md). A lista de termos é montada em tempo de execução
                 a partir dos `manifest.json` de `workspace/` (`product_slug`, o nome da pasta,
                 `product_name` inteiro e a parte antes do primeiro parêntese) mais os domínios
                 `*.myshopify.com` que aparecerem neles e o handle de cada um. Termo curto demais,
                 igual a um id, pasta ou relatório do registro, ou de uma palavra só e genérica
                 (GENERIC_TERMS) não entra na lista, para não acusar vocabulário comum. A falha
                 nunca imprime o termo encontrado: só arquivo, linha e o aviso. Sem `workspace/`
                 (clone novo) a lista fica vazia e a regra passa.
  gen            `python3 tools/gen_docs.py --check` passa.

Uso:
  python3 tools/aura-check.py                      todas as regras
  python3 tools/aura-check.py --only secrets,paths  subconjunto
  python3 tools/aura-check.py --list-rules

Só biblioteca padrão. Exit 0 = OK; exit 1 = falhas (ou erro de leitura do registro/índice).
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "skills.json"
INDEX = ROOT / ".claude" / "lib" / "kb-index" / "frameworks.json"
SCHEMA = ROOT / ".claude" / "templates" / "manifest-schema.json"
CLAUDE_MD = ROOT / ".claude" / "CLAUDE.md"
OVERVIEW_MD = ROOT / ".claude" / "OVERVIEW.md"
ESCAPE_RULE = ROOT / ".claude" / "rules" / "emergency-escape-paths.md"
SELF_AUDIT_RULE = ROOT / ".claude" / "rules" / "post-task-self-audit.md"
LAYOUT_MD = ROOT / ".claude" / "lib" / "workspace-index" / "workspace-layout.md"
GUARD = ROOT / ".claude" / "hooks" / "pre-commit-guard.sh"
SELF = Path(__file__).resolve()

RULES = ["paths", "queries", "skill-ids", "counts", "removed-terms", "sections", "skill-size", "secrets",
         "member-data", "gen"]

TEXT_EXT = (".md", ".json", ".py", ".sh")

# Termos do modelo antigo de policy/compliance que não podem voltar (regra 8b do CLAUDE.md).
REMOVED_TERMS = [
    "ad-safe", "ad-flag", "viola policy", "AI Info", "claims_unverified", "compliance_override",
    "pre-launch-gates", "Data Quality Summary", "Source Audit",
]

# Mesma regex do CHECK 3 do pre-commit guard (tokens reais + chave antiga da base).
SECRET_RE = re.compile(
    r"EAA[A-Za-z0-9]{100,}|ya29\.[A-Za-z0-9_-]{30,}|sk_live_[A-Za-z0-9]{20,}|pk_live_[A-Za-z0-9]{20,}"
    r"|AIza[A-Za-z0-9_-]{35}|ghp_[A-Za-z0-9]{36}|xox[bp]-[A-Za-z0-9-]{20,}|shpat_[a-fA-F0-9]{32}"
    r"|shpss_[a-fA-F0-9]{32}|shpca_[a-fA-F0-9]{32}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}"
    r"|pk_[a-f0-9]{30,}|AURADTC[A-Z0-9]{4,}|railway\.app/mcp\?key="
    # Chave do AI Gateway da Vercel. Pega o prefixo conhecido e,
    # principalmente, a atribuição colada num arquivo — que é como a chave da base
    # vazou neste repositório antes.
    r"|vck_[A-Za-z0-9_-]{20,}"
    r"|AI_GATEWAY_API_KEY\s*[:=]\s*[\"\']?[A-Za-z0-9_\-]{20,}"
    r"|VERCEL_OIDC_TOKEN\s*[:=]\s*[\"\']?[A-Za-z0-9._\-]{20,}"
)

# Seções históricas: número antigo de skill é registro, não referência. (Arquivo → cabeçalhos que
# abrem uma seção a pular, até o próximo cabeçalho de nível igual ou maior.)
HISTORICAL_SECTIONS = {
    ".claude/OVERVIEW.md": [r"^## 14\b"],
    ".claude/lib/workspace-index/workspace-layout.md": [r"^## Produtos legados"],
}
# Arquivos que descrevem o catálogo/histórico do índice: ficam fora de skill-ids e removed-terms.
CATALOG_DIRS = (".claude/lib/kb-index/",)
# Arquivos gerados a partir de outro (o OVERVIEW.html é o render do OVERVIEW.md pelo gen_docs.py).
GENERATED_FILES = (".claude/OVERVIEW.html",)
# Campos do manifest com número no nome: são nomes de campo gravados em manifests reais dos
# produtos, nunca referência a skill. Não se renomeiam e não contam como apelido numérico.
MANIFEST_NUMERIC_FIELDS = ("10_campaign_name", "10_campaign_id", "10_ad_set_ids", "10_ad_set_id")
MANIFEST_FIELDS_RE = re.compile("|".join(re.escape(f) for f in MANIFEST_NUMERIC_FIELDS))
# Nomes legados de relatório (`07-page.html`): não são referência a skill. A lista vive no
# tools/migrate_ids.py (LEGACY_REPORT_NAMES), que a esconde antes de converter; aqui ela é importada
# (mig.LEGACY_REPORT_RE) e mascarada na varredura, para o lint e o conversor nunca divergirem.
# Código que cita os apelidos e os nomes antigos de propósito (conversor de referências e migração
# do workspace). Fica fora da varredura de texto de skill-ids, junto com este lint.
# Os testes (tools/tests/) escrevem "skill 12" de propósito, para provar que o lint acusa.
ALIAS_AWARE_FILES = ("tools/migrate_ids.py", "tools/migrate.py", "tools/migrations/", "tools/tests/")
# Linhas do registro em que o número é o dado (apelido, pasta antiga, card do painel), não referência.
REGISTRY_LEGACY_LINE_RE = re.compile(r'^\s*(?:"(?:legacy_ids|legacy_folder|panel_card)"\s*:|"\d{2}[a-e]?",?\s*$)')
# Extensões varridas pela regra skill-ids (as mesmas do migrate_ids.py).
SKILL_IDS_EXT = TEXT_EXT + (".html", ".txt", ".template")
# Pasta do workspace do membro: nunca é lida como conteúdo, só como fonte dos termos proibidos.
WORKSPACE = ROOT / "workspace"
# Binários: a regra member-data não tenta lê-los como texto.
BINARY_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svgz", ".pdf", ".zip", ".gz", ".tgz",
              ".mp4", ".mov", ".mp3", ".wav", ".woff", ".woff2", ".ttf", ".otf", ".eot")
# Palavra comum de categoria ou de idioma: sozinha, nunca identifica o produto de um membro, e como
# termo proibido acusaria vocabulário normal do framework. Só filtra termo de UMA palavra.
GENERIC_TERMS = {
    "produto", "product", "suplemento", "supplement", "supplements", "skincare", "beleza", "beauty",
    "creatina", "creatine", "colageno", "colágeno", "collagen", "probiotico", "probiótico", "probiotic",
    "melatonina", "melatonin", "magnesio", "magnésio", "magnesium", "cacau", "cacao", "cocoa", "patch",
    "menopausa", "menopause", "protocolo", "protocol", "reset", "club", "clube", "loja", "store", "shop",
    "brand", "marca", "teste", "test", "demo", "exemplo", "example", "sample",
}
# Termo mais curto que isso não é distintivo o bastante para virar regra.
MEMBER_TERM_MIN = 5
TOOLS_DIR = ROOT / "tools"


# ----------------------------------------------------------------------------- utilidades
class Fail:
    __slots__ = ("file", "line", "rule", "msg")

    def __init__(self, file, line, rule, msg):
        self.file, self.line, self.rule, self.msg = str(file), int(line or 0), rule, msg

    def render(self):
        return f"{self.file}:{self.line}  {self.rule}  {self.msg}"


def rel(p):
    try:
        return str(Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def tracked_files():
    """Arquivos rastreados pelo git (relativos à raiz). Fallback: varredura do disco."""
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotePath=false", "ls-files", "-z"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace")
        files = [f for f in out.split("\0") if f]
    except Exception:
        files = []
        for base, dirs, names in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__", "workspace")]
            for n in names:
                files.append(rel(Path(base) / n))
    return sorted(f for f in files if (ROOT / f).is_file())


_LINES = {}


def lines_of(relpath):
    if relpath not in _LINES:
        try:
            _LINES[relpath] = (ROOT / relpath).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            _LINES[relpath] = []
    return _LINES[relpath]


def skipped_lines(relpath):
    """Números de linha (1-based) dentro de seções históricas do arquivo."""
    pats = HISTORICAL_SECTIONS.get(relpath)
    if not pats:
        return set()
    skip, level = set(), None
    for i, l in enumerate(lines_of(relpath), 1):
        m = re.match(r"^(#{1,6})\s", l)
        if m:
            if level is not None and len(m.group(1)) <= level:
                level = None
            if level is None and any(re.match(p, l) for p in pats):
                level = len(m.group(1))
        if level is not None:
            skip.add(i)
    return skip


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def skill_files():
    files = sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".claude" / "skills").glob("*.md"))
    files += sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".claude" / "skills").glob("*/SKILL.md"))
    return files


def skill_reference_files():
    """Material de apoio das skills no formato nativo: `.claude/skills/<id>/reference/*.md`.
    Não são arquivos de skill (não têm entrada no registro), mas carregam queries, contagens e
    referências a etapas, então entram em queries, counts e sections."""
    return sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".claude" / "skills").glob("*/reference/*.md"))


REFERENCE_RE = re.compile(r"^(\.claude/skills/[^/]+)/reference/[^/]+\.md$")


def skill_home(relpath):
    """O SKILL.md da pasta de um arquivo de apoio; para qualquer outro arquivo, ele mesmo."""
    m = REFERENCE_RE.match(relpath)
    return f"{m.group(1)}/SKILL.md" if m else relpath


def rule_files():
    return sorted(str(p.relative_to(ROOT)) for p in (ROOT / ".claude" / "rules").glob("*.md"))


_MIG = None


def migrate_ids_module():
    """O conversor tools/migrate_ids.py é a fonte única do filtro de contexto numérico e das linhas
    que ficam fora (blocos gerados, "apelido antigo", SUPERSEDED, seções históricas)."""
    global _MIG
    if _MIG is None:
        if str(TOOLS_DIR) not in sys.path:
            sys.path.insert(0, str(TOOLS_DIR))
        import migrate_ids
        _MIG = migrate_ids
    return _MIG


def _delta(old, new, ctx=28):
    """Trecho mínimo que muda entre duas versões de uma linha: (antes, depois), com contexto curto."""
    ops = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes() if op[0] != "equal"]
    if not ops:
        return old.strip(), new.strip()
    i1, j1 = ops[0][1], ops[0][3]
    i2, j2 = ops[-1][2], ops[-1][4]
    a = re.sub(r"\s+", " ", old[max(0, i1 - ctx):i2 + ctx]).strip()
    b = re.sub(r"\s+", " ", new[max(0, j1 - ctx):j2 + ctx]).strip()
    return a, b


def words(s):
    return re.findall(r"[a-z0-9]+", s.lower())


# ----------------------------------------------------------------------------- registro
class Registry:
    def __init__(self):
        data = load_json(REGISTRY)
        self.skills = data["skills"]
        self.launch_after = data.get("launch_after")
        self.ids = [s["id"] for s in self.skills]
        self.by_id = {s["id"]: s for s in self.skills}
        self.legacy = {}      # apelido → id
        for s in self.skills:
            for lg in s.get("legacy_ids") or []:
                self.legacy[lg] = s["id"]
        self.legacy_folders = {s["legacy_folder"] for s in self.skills if s.get("legacy_folder")}
        self.folders = {s["folder"] for s in self.skills if s.get("folder")}
        # slug → apelidos válidos (id da skill, pasta nova e pasta antiga sem o número)
        self.slug_aliases = {}
        for s in self.skills:
            lgs = set(s.get("legacy_ids") or [])
            self.slug_aliases.setdefault(s["id"], set()).update(lgs)
            if s.get("folder"):
                self.slug_aliases.setdefault(s["folder"], set()).update(lgs)
            if s.get("legacy_folder"):
                m = re.match(r"^(\d{2}[a-e]?)-(.+)$", s["legacy_folder"])
                if m:
                    self.slug_aliases.setdefault(m.group(2), set()).add(m.group(1))
        # começo de slug (por segmento) → {id a sugerir: apelidos daquela skill}. `04-offer` e
        # `06-copy` são referência a skill tanto quanto `04-offer-builder`; o slug completo já está
        # no slug_aliases. Exigir que o número seja o apelido DAQUELA skill é o que mantém
        # `90-day` e `19-point` fora da regra.
        self.slug_prefixes = {}
        for s in self.skills:
            lgs = set(s.get("legacy_ids") or [])
            parts = s["id"].split("-")
            for n in range(1, len(parts)):
                pre = "-".join(parts[:n])
                if pre in self.slug_aliases:
                    continue
                self.slug_prefixes.setdefault(pre, {}).setdefault(s["id"], set()).update(lgs)

    def resolve(self, token):
        """id ou apelido → id (ou None)."""
        if token in self.by_id:
            return token
        return self.legacy.get(token)


# ----------------------------------------------------------------------------- regras
def rule_paths(files, reg, index):
    fails = []
    pat = re.compile(r"`((?:\.claude|tools|docs)/[^`\s]*)`")
    for f in files:
        if not f.endswith(TEXT_EXT):
            continue
        for i, l in enumerate(lines_of(f), 1):
            for m in pat.finditer(l):
                p = m.group(1)
                if any(c in p for c in "[<{*") or p.startswith("workspace/"):
                    continue
                p = re.sub(r":\d+(?:-\d+)?$", "", p)      # sufixo :linha
                p = p.rstrip(",.;:)").rstrip("/")
                if p == ".claude/.no-auto-update" or not p:
                    continue
                if not (ROOT / p).exists():
                    fails.append(Fail(f, i, "paths", f"caminho inexistente: `{p}`"))
    # skills no formato nativo: `reference/<tema>.md` é relativo à pasta da skill (onde está o SKILL.md)
    ref_pat = re.compile(r"`(reference/[A-Za-z0-9_.-]+\.md)`")
    for f in files:
        m_dir = re.match(r"^(\.claude/skills/[^/]+)/", f)
        if not m_dir or not f.endswith(".md"):
            continue
        for i, l in enumerate(lines_of(f), 1):
            for m in ref_pat.finditer(l):
                if not (ROOT / m_dir.group(1) / m.group(1)).is_file():
                    fails.append(Fail(f, i, "paths", f"arquivo de apoio inexistente: `{m.group(1)}` (relativo a {m_dir.group(1)}/)"))
    return fails


def _is_command_or_path(p):
    if "/" in p or "=" in p or "(" in p or "{" in p or "[" in p or "<" in p or "|" in p or ":" in p:
        return True
    first = p.split()[0].lower() if p.split() else ""
    return first in ("python", "python3", "bash", "git", "npx", "npm", "claude", "curl", "ls", "cd",
                     "pip", "brew", "winget", "cat", "grep", "rm", "mv", "cp") or p.startswith(("-", ".", "$", "#"))


def rule_queries(files, reg, index):
    fails = []
    queries = set()
    for entries in index["domains"].values():
        for e in entries:
            queries.add(e["best_query"])
    qwords = {q: set(words(q)) for q in queries}
    cand = re.compile(r"`([^`\n]{12,})`")
    for f in skill_files() + skill_reference_files():
        seen = set()
        for i, l in enumerate(lines_of(f), 1):
            for m in cand.finditer(l):
                p = m.group(1).strip()
                if p in queries or p in seen or _is_command_or_path(p):
                    continue
                w = set(words(p))
                if len(w) < 4:
                    continue
                best, score = None, 0.0
                for q, qw in qwords.items():
                    s = len(w & qw) / max(len(w), len(qw))
                    if s > score:
                        best, score = q, s
                if score >= 0.8:
                    seen.add(p)
                    fails.append(Fail(f, i, "queries",
                                      f"query quase igual a uma best_query do índice (não exata): `{p}` ≈ `{best}`"))
    return fails


TOKEN_RE = re.compile(r"(?<![\w-])(\d{2}[a-e]?)-([a-z][a-z0-9-]*[a-z0-9])(?![\w-])")
RANGE_RE = re.compile(r"(?<![\w.\-:])(\d{2}[a-e]?)-(\d{2}[a-e]?)(?![\w\-]|\.\d)")
SKILL_BEFORE_RE = re.compile(r"\b[Ss]kills?\s+(?:\*\*|__|\*|_|`)?$")


def rule_skill_ids(files, reg, index):
    fails = []
    rf = rel(REGISTRY)
    # 1. registro: file existe, ids dos consumers/launch_after válidos
    for s in reg.skills:
        if not (ROOT / s["file"]).is_file():
            fails.append(Fail(rf, 0, "skill-ids", f"{s['id']}: `file` não existe: {s['file']}"))
        for c in s.get("consumers") or []:
            if c not in reg.by_id:
                fails.append(Fail(rf, 0, "skill-ids", f"{s['id']}: consumer desconhecido: {c}"))
    if reg.launch_after and reg.launch_after not in reg.by_id:
        fails.append(Fail(rf, 0, "skill-ids", f"launch_after desconhecido: {reg.launch_after}"))
    # 2. cada arquivo de skill tem entrada
    registered = {s["file"] for s in reg.skills}
    for f in skill_files():
        if f not in registered:
            fails.append(Fail(f, 0, "skill-ids", "arquivo de skill sem entrada no skills.json"))
    # 3. enum do manifest-schema
    try:
        schema = load_json(SCHEMA)
        enum = schema["properties"]["skills_completed"]["items"]["enum"]
        for v in enum:
            if v not in reg.by_id:
                fails.append(Fail(rel(SCHEMA), 0, "skill-ids", f"enum de skills_completed com id inválido: {v} (só ids do registro)"))
    except (KeyError, OSError, ValueError) as e:
        fails.append(Fail(rel(SCHEMA), 0, "skill-ids", f"não consegui ler o enum de skills_completed: {e}"))
    # 4. use_in_skill do índice
    for dom, entries in index["domains"].items():
        for e in entries:
            for t in re.findall(r"\b\d{2}[a-e]?\b", e.get("use_in_skill", "") or ""):
                if t not in reg.legacy:
                    fails.append(Fail(rel(INDEX), 0, "skill-ids",
                                      f"[{dom}] {e.get('name')}: use_in_skill cita apelido desconhecido: {t}"))
            for sid in e.get("skills") or []:
                if sid not in reg.by_id:
                    fails.append(Fail(rel(INDEX), 0, "skill-ids", f"[{dom}] {e.get('name')}: skills cita id desconhecido: {sid}"))
    # 5. referências em texto: número como identificador de skill é falha fora das exceções
    try:
        mig = migrate_ids_module()
        mreg = mig.Registry()
    except Exception as e:                         # import ou registro quebrado: uma falha, não um traceback
        fails.append(Fail("tools/migrate_ids.py", 0, "skill-ids", f"não consegui importar o migrate_ids.py: {e}"))
        return fails

    def blank(m):
        return " " * len(m.group(0))

    for f in files:
        if not f.endswith(SKILL_IDS_EXT):
            continue
        if not (f.startswith((".claude/", "tools/", "docs/")) or f == "README.md"):
            continue
        if (f.startswith(CATALOG_DIRS) or f in GENERATED_FILES or f.startswith(ALIAS_AWARE_FILES)
                or (ROOT / f).resolve() == SELF):
            continue
        lines = lines_of(f)
        skip = mig.skipped_lines(f, lines)
        is_registry = f == rel(REGISTRY)
        html = f.endswith(".html")
        for i, raw in enumerate(lines, 1):
            if i in skip or (is_registry and REGISTRY_LEGACY_LINE_RE.match(raw)):
                continue
            l = mig.LEGACY_REPORT_RE.sub(blank, MANIFEST_FIELDS_RE.sub(blank, raw))
            # a. pasta ou arquivo de skill com número na frente, inteiro (`04-offer-builder`, com
            #    qualquer número) ou abreviado (`04-offer`, só com o apelido daquela skill)
            hits = []
            for m in TOKEN_RE.finditer(l):
                if m.group(2) in reg.slug_aliases:      # slug de skill; `90-day`, `19-point` não são
                    hits.append((m, m.group(2)))
                    continue
                for sid, lgs in reg.slug_prefixes.get(m.group(2), {}).items():
                    if m.group(1) in lgs:
                        hits.append((m, sid))
                        break
            for m, name in hits:
                fails.append(Fail(f, i, "skill-ids", f"número no nome de skill ou pasta: `{m.group(0)}` (escreva `{name}`)"))
            for m, _ in reversed(hits):
                l = l[:m.start()] + " " * (m.end() - m.start()) + l[m.end():]
            # b. tudo que o migrate_ids.py converteria: `skill NN`, `skill-NN`, `(NN)`, `07a`, `a NN`, listas
            new, n = mig.convert_line(l, mreg, html=html)
            if n:
                a, b = _delta(l, new)
                fails.append(Fail(f, i, "skill-ids", f"número como identificador de skill: \"{a}\" (escreva \"{b}\")"))
            # c. faixa entre apelidos (`skills 00-20`, `07a-07d`)
            for m in RANGE_RE.finditer(l):
                x, y = m.group(1), m.group(2)
                if x in reg.legacy and y in reg.legacy and (re.search(r"[a-e]$", x + y) or SKILL_BEFORE_RE.search(l[:m.start()])):
                    fails.append(Fail(f, i, "skill-ids", f"faixa de apelidos numéricos: `{m.group(0)}` (cite cada skill pelo id)"))
    return fails


def rule_counts(files, reg, index):
    fails = []
    counts = {d: len(v) for d, v in index["domains"].items()}
    dom_re = re.compile("|".join(re.escape(d) for d in sorted(counts, key=len, reverse=True)))
    num_re = re.compile(r"(\d+)\s+(sistemas|entradas)")
    for f in skill_files() + skill_reference_files():
        for i, l in enumerate(lines_of(f), 1):
            for m in num_re.finditer(l):
                before = l[max(0, m.start() - 40):m.start()]
                after = l[m.end():m.end() + 40]
                dm = list(dom_re.finditer(before)) + list(dom_re.finditer(after))
                if not dm:
                    continue
                # domínio mais próximo do número
                dom = min(dm, key=lambda x: abs((x.start() + x.end()) / 2 - (len(before) if x.string is before else len(before) + (m.end() - m.start()) + x.start()))).group(0)
                n = int(m.group(1))
                if n != counts[dom]:
                    fails.append(Fail(f, i, "counts", f"`{dom}` tem {counts[dom]} entradas no índice, o texto diz {n}"))
    return fails


def rule_removed_terms(files, reg, index):
    fails = []
    terms = [(t, re.compile(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", 0 if t != t.lower() else re.I))
             for t in REMOVED_TERMS]
    scope = (".claude/skills/", ".claude/rules/", ".claude/lib/", ".claude/templates/", ".claude/automations/")
    for f in files:
        if not (f.startswith(scope) or f in (rel(CLAUDE_MD), rel(OVERVIEW_MD))):
            continue
        if f.startswith(CATALOG_DIRS):
            continue
        skip = skipped_lines(f)
        for i, l in enumerate(lines_of(f), 1):
            if i in skip:
                continue
            for t, pat in terms:
                if pat.search(l):
                    fails.append(Fail(f, i, "removed-terms", f"termo do modelo antigo de policy: \"{t}\""))
    return fails


HEAD_RE = re.compile(r"^#{1,6}\s+(.*)")
ETAPA_RE = re.compile(r"\bETAPA\s?(\d+(?:\.\d+)?[A-Z]?)\b")
GATE_RE = re.compile(r"\b(?:GATE|Gate)\s?(\d+)\b")
ES_RE = re.compile(r"\bES\s?(\d+)\b")
REGRA_RE = re.compile(r"\b(?:[Rr]egra|REGRA|[Rr]ule|RULE)\s?(\d{1,2}[a-e]?)\b")
NEAR_SKILL_RE = re.compile(
    r"(?:\b(?i:da|na|de|do|pela|pelo|pra|para|com|a|o|as|os|e|skills?)\s+|\(|→\s*|←\s*)(\d{2}[a-e]?)(?![\w-])"
    r"|(?<![\w-])(\d{2}[a-e]?)-[a-z][a-z0-9-]*"
)
CODE_SPAN_RE = re.compile(r"`[^`]*`")
MD_PATH_RE = re.compile(r"`((?:\.claude|tools|docs)/[^`\s]+\.md)`")


def _labels(relpath, kind):
    """Rótulos definidos no arquivo: cabeçalhos (e, para GATE, também linhas em negrito)."""
    out = set()
    pat = {"ETAPA": ETAPA_RE, "GATE": GATE_RE}[kind]
    for l in lines_of(relpath):
        h = HEAD_RE.match(l)
        text = None
        if h:
            text = h.group(1)
        elif kind == "GATE" and l.lstrip().startswith(("**GATE", "**Gate", "GATE", "Gate")):
            text = l
        if text is not None:
            for m in pat.finditer(text):
                out.add(m.group(1).upper())
    return out


def _claude_rules():
    out = set()
    for l in lines_of(rel(CLAUDE_MD)):
        m = re.match(r"^\s*(?:\*\*)?(\d{1,2}[a-e]?)\.\s+\S", l)
        if m:
            out.add(m.group(1).lower())
    return out


def rule_sections(files, reg, index):
    fails = []
    skill_by_legacy = {lg: s["file"] for s in reg.skills for lg in (s.get("legacy_ids") or [])}
    skill_by_id = {s["id"]: s["file"] for s in reg.skills}
    es_labels = set()
    for l in lines_of(rel(ESCAPE_RULE)):
        h = HEAD_RE.match(l)
        if h:
            for m in ES_RE.finditer(h.group(1)):
                es_labels.add(int(m.group(1)))
    # numeração contígua da rule de escape
    if es_labels:
        for n in range(1, max(es_labels) + 1):
            if n not in es_labels:
                fails.append(Fail(rel(ESCAPE_RULE), 0, "sections", f"ES{n} não existe (a numeração vai de ES1 a ES{max(es_labels)} com esse buraco)"))
    claude_rules = _claude_rules()
    label_cache = {}

    def labels(path, kind):
        key = (path, kind)
        if key not in label_cache:
            label_cache[key] = _labels(path, kind)
        return label_cache[key]

    names = [(s["id"], s["file"], s["id"].replace("-", " "), (s.get("name") or "").lower()) for s in reg.skills]

    def cited_file(raw_line, here, start, end):
        """Arquivo citado perto da referência: skill (ex.: 'ETAPA 3F da 03', 'na 07a', '08-creative-engine',
        'do product research') ou caminho `.md` entre crases (ex.: 'ETAPA 2 do `.claude/lib/<lib>/<arquivo>.md`')."""
        window = raw_line[max(0, start - 60):end + 60]
        for m in MD_PATH_RE.finditer(window):
            if (ROOT / m.group(1)).is_file() and m.group(1) != here:
                return m.group(1)
        # a própria referência não conta como skill citada
        w2 = raw_line[max(0, start - 60):start] + " " * (end - start) + raw_line[end:end + 60]
        for m in NEAR_SKILL_RE.finditer(w2):
            f = skill_by_legacy.get(m.group(1) or m.group(2))
            if f and f != here:
                return f
        low = w2.lower()
        for sid, f, spaced, name in names:
            if f != here and (sid in low or spaced in low or (name and name in low)):
                return f
        return None

    def etapa_defined(path, lab):
        defined = labels(path, "ETAPA")
        return lab in defined or re.match(r"\d+", lab).group(0) in defined

    for f in skill_files() + skill_reference_files() + rule_files():
        home = skill_home(f)            # arquivo de apoio: as etapas vivem no SKILL.md da pasta
        in_fence = False
        for i, raw in enumerate(lines_of(f), 1):
            if raw.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or HEAD_RE.match(raw):
                continue
            l = CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), raw)
            for m in ETAPA_RE.finditer(l):
                lab = m.group(1).upper()
                if etapa_defined(f, lab) or (home != f and etapa_defined(home, lab)):
                    continue
                tgt = cited_file(raw, f, m.start(), m.end())
                if tgt and etapa_defined(tgt, lab):
                    continue
                where = f" (nem em {tgt})" if tgt else ""
                fails.append(Fail(f, i, "sections", f"ETAPA {lab} citada, mas não existe como cabeçalho neste arquivo{where}"))
            for m in GATE_RE.finditer(l):
                lab = m.group(1)
                if lab in labels(f, "GATE") or (home != f and lab in labels(home, "GATE")):
                    continue
                tgt = cited_file(raw, f, m.start(), m.end())
                if tgt is None and re.search(r"self-audit|auditoria silenciosa|gates internos|gates expandidos", raw, re.I):
                    tgt = rel(SELF_AUDIT_RULE)
                if tgt and lab in labels(tgt, "GATE"):
                    continue
                where = f" (nem em {tgt})" if tgt else ""
                fails.append(Fail(f, i, "sections", f"GATE {lab} citado, mas não existe como cabeçalho neste arquivo{where}"))
            for m in ES_RE.finditer(l):
                if int(m.group(1)) not in es_labels:
                    fails.append(Fail(f, i, "sections", f"ES{m.group(1)} citado, mas não existe em {rel(ESCAPE_RULE)}"))
            for m in REGRA_RE.finditer(l):
                lab = m.group(1).lower()
                if lab not in claude_rules and lab.upper() not in labels(f, "GATE"):
                    fails.append(Fail(f, i, "sections", f"Regra {lab} citada, mas o CLAUDE.md não tem regra com esse número"))
    return fails


SKILL_MAX_BYTES = 12 * 1024
SKILL_NEAR_BYTES = 300


def skills_near_cap(reg):
    """Skills perto do teto. Não é falha: é aviso pra quem VAI escrever, antes de escrever."""
    perto = []
    for sk in reg.skills:
        rel_ = sk.get("file")
        if not rel_ or not rel_.endswith("SKILL.md"):
            continue
        f = ROOT / rel_
        if not f.is_file():
            continue
        n = f.stat().st_size
        folga = SKILL_MAX_BYTES - n
        if 0 <= folga <= SKILL_NEAR_BYTES:
            perto.append((folga, sk.get("id", rel_), n))
    perto.sort()
    return perto


def rule_skill_size(files, reg, index):
    """O SKILL.md é o roteiro; passou de 12 KB, o excedente vira `reference/<tema>.md`."""
    fails = []
    for sk in reg.skills:
        rel = sk.get("file")
        if not rel or not rel.endswith("SKILL.md"):
            continue
        f = ROOT / rel
        if not f.is_file():
            continue
        n = f.stat().st_size
        if n > SKILL_MAX_BYTES:
            fails.append(Fail(rel, 0, "skill-size",
                              f"{n:,} bytes, acima do teto de {SKILL_MAX_BYTES:,}: mova o excedente para reference/"))
    return fails


def rule_secrets(files, reg, index):
    fails = []
    for f in files:
        if (ROOT / f).resolve() in (GUARD.resolve(), SELF):
            continue
        for i, l in enumerate(lines_of(f), 1):
            if SECRET_RE.search(l):
                fails.append(Fail(f, i, "secrets", "parece conter um token real ou a chave antiga da base"))
    return fails


def member_terms(reg):
    """Termos proibidos, montados em tempo de execução a partir dos manifests de `workspace/`.

    Nunca são impressos: servem só para localizar a linha. Fonte: `product_slug`, o nome da pasta do
    produto, `product_name` (inteiro e a parte antes do primeiro parêntese) e os domínios
    `*.myshopify.com` que aparecerem no manifest, mais o handle de cada domínio."""
    reserved = set()
    for s in reg.skills:
        for k in ("id", "folder", "legacy_folder", "report_stem"):
            v = s.get(k)
            if v:
                reserved.add(str(v).lower())
    terms = set()

    def add(value):
        v = re.sub(r"\s+", " ", str(value or "")).strip().lower().strip(" .,:;-")
        if len(v) < MEMBER_TERM_MIN or v in reserved:
            return
        if " " not in v and "-" not in v and "." not in v and v in GENERIC_TERMS:
            return
        terms.add(v)

    if not WORKSPACE.is_dir():
        return terms
    for mf in sorted(WORKSPACE.glob("*/manifest.json")):
        add(mf.parent.name)
        try:
            raw = mf.read_text(encoding="utf-8", errors="replace")
            data = json.loads(raw)
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        add(data.get("product_slug"))
        name = str(data.get("product_name") or "")
        add(name)
        add(name.split("(")[0])
        for dom in re.findall(r"[A-Za-z0-9][A-Za-z0-9-]*\.myshopify\.com", raw):
            add(dom)
            add(dom.split(".")[0])
    return terms


def rule_member_data(files, reg, index):
    """Nome de produto, loja ou marca do workspace do membro não pode viver em arquivo do framework."""
    terms = member_terms(reg)
    if not terms:
        return []
    pattern = re.compile("|".join(re.escape(x) for x in sorted(terms, key=len, reverse=True)), re.IGNORECASE)
    fails = []
    for f in files:
        if f.endswith(BINARY_EXT) or (ROOT / f).resolve() == SELF:
            continue
        for i, l in enumerate(lines_of(f), 1):
            if pattern.search(l):
                fails.append(Fail(f, i, "member-data", "termo de workspace em arquivo do framework"))
    return fails


def rule_gen(files, reg, index):
    fails = []
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_docs.py"), "--check"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        out = (r.stdout + r.stderr).strip().splitlines() or ["gen_docs.py --check falhou"]
        for l in out:
            if re.search(r"trecho\(s\) desatualizado", l):
                continue                              # linha-resumo do gen_docs: as linhas por arquivo já bastam
            m = re.match(r"^DESATUALIZADO\s+(\S+)\s+\((.+)\)", l.strip())
            if m:
                fails.append(Fail(m.group(1), 0, "gen", f"trecho gerado desatualizado ({m.group(2)}); rode python3 tools/gen_docs.py"))
            else:
                fails.append(Fail("tools/gen_docs.py", 0, "gen", l.strip()))
    return fails


RULE_FUNCS = {
    "paths": rule_paths,
    "queries": rule_queries,
    "skill-ids": rule_skill_ids,
    "counts": rule_counts,
    "removed-terms": rule_removed_terms,
    "sections": rule_sections,
    "skill-size": rule_skill_size,
    "secrets": rule_secrets,
    "member-data": rule_member_data,
    "gen": rule_gen,
}


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Lint mecânico do framework Aura Engine.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="Regras: " + ", ".join(RULES))
    ap.add_argument("--only", default="", help="lista de regras separadas por vírgula (ex.: secrets,paths,skill-ids)")
    ap.add_argument("--list-rules", action="store_true", help="lista as regras e sai")
    args = ap.parse_args()

    if args.list_rules:
        print("\n".join(RULES))
        return 0
    selected = [r.strip() for r in args.only.split(",") if r.strip()] or RULES
    unknown = [r for r in selected if r not in RULE_FUNCS]
    if unknown:
        print(f"ERRO  regra desconhecida: {', '.join(unknown)} (válidas: {', '.join(RULES)})")
        return 1

    os.chdir(ROOT)
    try:
        reg = Registry()
    except (OSError, ValueError, KeyError) as e:
        print(f"ERRO  não consegui ler {rel(REGISTRY)}: {e}")
        return 1
    try:
        index = load_json(INDEX)
    except (OSError, ValueError) as e:
        print(f"ERRO  não consegui ler {rel(INDEX)}: {e}")
        return 1

    files = tracked_files()
    fails = []
    for r in selected:
        fails.extend(RULE_FUNCS[r](files, reg, index))
    fails.sort(key=lambda x: (x.file, x.line, x.rule, x.msg))
    for x in fails:
        print(x.render())
    if fails:
        print(f"{len(fails)} falhas")
        return 1
    if "skill-size" in selected:
        for folga, sid, n in skills_near_cap(reg):
            print(f"aviso  {sid}: SKILL.md com {n:,} bytes, {folga} livres do teto de "
                  f"{SKILL_MAX_BYTES:,}. Texto novo nasce em reference/, com uma linha de roteiro aqui.")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
