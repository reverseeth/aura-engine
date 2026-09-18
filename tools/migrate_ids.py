#!/usr/bin/env python3
"""
migrate_ids.py: troca as referências numéricas a skills pelos ids do registro (.claude/skills.json).

Desde a Fase 5 da reforma mecânica, o identificador de uma skill é o slug (`creative-engine`) e o
número antigo (`08`) sobrevive só como apelido de roteamento, guardado em `legacy_ids`. Este script
faz a troca mecânica no texto do framework e lista o que sobrou para revisão manual.

Escopo: arquivos rastreados pelo git em `.claude/`, `tools/`, `docs/` e o `README.md`, com extensão
.md, .json, .py, .sh, .html, .txt ou .template. Nunca toca em `workspace/` nem no índice `frameworks.json`.
Ficam fora também (ver EXCLUDED_FILES / EXCLUDED_DIRS): os documentos do catálogo do índice, o
`OVERVIEW.html` (gerado do .md pelo gen_docs.py), o `build_index.py` (carrega o mapa LEGACY_FOLDERS, com os
nomes antigos de propósito), o `migrate.py` e a pasta `tools/migrations/` (a migração do workspace
descreve os nomes antigos que ela renomeia) e os scripts que reconhecem os apelidos. No `.claude/skills.json` só os campos
de prosa são reescritos; `legacy_ids` e `legacy_folder` ficam intactos por definição.

Dentro dos arquivos, ficam de fora: trechos gerados pelo gen_docs.py (marcadores `gen:`), linhas
com `SUPERSEDED` ou com a expressão "apelido antigo" (as docs geradas mostram o número assim de
propósito), o changelog do OVERVIEW.md (§14), a seção "Produtos legados" do workspace-layout.md e os
nomes legados de relatório de LEGACY_REPORT_NAMES (`07-page.html`: o build_index.py e o aura-status.py
o leem como fallback por um ciclo, então o nome antigo aparece de propósito no código e nunca é trocado).
O lint `tools/aura-check.py` (regra `skill-ids`) importa `Registry`, `in_scope`, `skipped_lines`,
`convert_line` e `LEGACY_REPORT_RE` daqui: tudo que este script converteria é falha no lint, para o
número nunca voltar, e a lista de nomes legados é uma só para os dois.

Trocas do modo --apply (todas mecânicas):
  token `NN-slug`            → `slug`         (também `07-page/` → `page/` e caminhos de arquivo de skill)
  `skill-NN`                 → `skill-<id>`   (vocabulário de executor do ad-log)
  `skill NN`, `Skill NN`,
  `skills NN e MM`, `NN/MM`  → `skill <id>`, `skills <id> e <id>` (o id vai entre crases)
  `Nome da skill (NN)`       → `Nome da skill`; qualquer outro `(NN)` → `(<id>)`
  `07a`, `01b` soltos        → `<id>` (formas com letra são inequívocas)
  `a NN`, `da NN`, `na NN`, `pela NN`, `pra NN`, `via NN`, `→ NN`, `↔ NN`
                             → mesma preposição + `<id>`, quando o contexto não é numérico
                               (nunca antes de %, unidade, "dias", "buscas", faixa "de X a Y"; nunca no
                               plural: "as 20 mais", "dos 15 fatores" são quantidade)
  Listas ligadas por `/`, `,`, ` e `, ` ou `, `+`, `→` a partir de qualquer token convertido são
  convertidas inteiras (ex.: `01b, 04, 11 e 12` → `sourcing`, `offer-builder`, `ad-analysis` e `scale-engine`).
  Faixas com hífen (`00-20`, `07a-07d`) nunca são tocadas: vão para o relatório.

Palavra isolada (filtro de contexto numérico, comum ao conversor e ao lint): um número só é candidato
a apelido de skill quando aparece isolado como palavra ("a 08", "skill 12", "08-creative-engine").
Nunca é candidato, em nenhuma âncora (nem `skill NN`, nem `(NN)`, nem lista), quando tem dígito colado
antes ou depois, vírgula ou ponto seguidos de dígito ("12,000 reviews", "18,7%", "1,12"), % ou moeda
colados ("20%", "$12", "US$ 12", "R$12"), unidade colada ("12k", "12h", "12min") ou faz parte de data
AAAA-MM-DD ("2026-09-01"). Os fragmentos ISOLATED_BEFORE e ISOLATED_AFTER são a fonte única desse
filtro; os testes vivem em `tools/tests/test_migrate_ids.py` (`python3 -m unittest discover -s tools/tests`).

Modos:
  --report        (padrão) lista, com arquivo e linha, toda menção numérica que sobrou em forma de
                  referência a skill; `--all` lista todo número que coincide com um apelido.
  --dry-run       mostra o que --apply mudaria (contagem por arquivo); com --diff, o diff unificado.
  --apply         grava as trocas.
  --files PREFIX  limita a arquivos cujo começa com PREFIX (repetível).

Só biblioteca padrão. Exit 0 = ok (no --report: nada sobrou); exit 1 = sobrou algo no --report,
ou erro de leitura.
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "skills.json"

SCOPE_PREFIXES = (".claude/", "tools/", "docs/")
SCOPE_FILES = ("README.md",)
TEXT_EXT = (".md", ".json", ".py", ".sh", ".html", ".txt", ".template")

EXCLUDED_FILES = {
    ".claude/lib/kb-index/frameworks.json",             # use_in_skill fica numérico (Fase 5c.2)
    ".claude/OVERVIEW.html",                            # gerado do .md pelo gen_docs.py
    ".claude/lib/workspace-index/build_index.py",       # mapa LEGACY_FOLDERS: nomes antigos de propósito
    "tools/aura-check.py",                              # lint: reconhece os apelidos de propósito
    "tools/gen_docs.py",
    "tools/migrate_ids.py",
    "tools/migrate.py",                                 # migração do workspace: cita os nomes antigos que renomeia
}
EXCLUDED_DIRS = (".claude/lib/kb-index/",               # catálogo e notas históricas do índice
                 "tools/migrations/",                   # migrações do workspace (nomes antigos de propósito)
                 "tools/tests/")                        # testes do conversor e do lint: citam apelidos de propósito
SPECIAL_JSON = ".claude/skills.json"                    # só campos de prosa
PROSE_FIELDS = ("summary_pt", "summary_en", "order_note_pt", "step_note_pt", "title_pt", "title_en",
                "panel_title_pt", "panel_title_en")

HISTORICAL_SECTIONS = {
    ".claude/OVERVIEW.md": [r"^## 14\b"],
    ".claude/lib/workspace-index/workspace-layout.md": [r"^## Produtos legados"],
}
SKIP_LINE_WORDS = ("SUPERSEDED", "apelido antigo", "apelidos antigos", "<!-- gen:", "# gen:")
# Nomes legados de relatório do workspace: não são referência a skill. O conversor os deixa intactos
# (convert_line os esconde antes de qualquer troca) e o lint importa LEGACY_REPORT_RE para mascará-los
# na regra skill-ids. Fonte única: quem acrescentar um nome aqui cobre os dois scripts.
LEGACY_REPORT_NAMES = ("07-page.html",)
LEGACY_REPORT_RE = re.compile("|".join(re.escape(n) for n in LEGACY_REPORT_NAMES))
HIDDEN_MARK = "\ue000"      # marcador sem dígito nem letra: nenhuma regex daqui o reconhece
ENUM_LINE_RE = re.compile(r'^\s*"\d{2}[a-e]?-[a-z][a-z0-9-]*",?\s*$')

# Contexto numérico: o número não é skill quando vem seguido de unidade/percentual ou precedido
# de comparação/faixa. Listas generosas de propósito: sobra vai para o relatório, nunca vira erro.
UNIT_WORDS = set("""
dia dias semana semanas mês meses ano anos hora horas minuto minutos min segundo segundos seg
buscas queries query linhas linha palavras palavra caracteres chars itens item items
criativos criativo ads ad adsets conceitos conceito hooks hook headlines headline vezes vez
pontos ponto perguntas sistemas sistema entradas entrada produtos produto compras
clientes cliente pedidos pedido unidades unidade reviews review frases frase variações variação
versões versão opções opção exemplos exemplo cards card campos campo seções seção etapas
passos features feature defeitos defeito splits split days day domínios domínio skills
fases marcas concorrentes concorrente avatares avatar sub-avatares bônus emails email
flows flow skus sku packs pack checks check sweeps sweep gates gate movimentos movimento regras
regra slots slot tools tool fórmulas fórmula ângulos ângulo temas tema categorias categoria tiers
tier níveis nível degraus degrau ciclos ciclo rodadas lotes lote batches batch frames frame
takes take cenas cena shots shot vídeos vídeo imagens imagem fotos foto creators creator modelos
modelo presets preset rotas rota caminhos caminho colunas coluna arquivos arquivo páginas página
posts post threads thread comentários comentário respostas resposta quadrantes quadrante
elementos elemento ideias ideia candidatos candidatas jogadas jogada mecanismos mecanismo claims
claim provas estudos estudo testes teste amostras amostra eixos eixo critérios critério
questões questão casos caso vagas vaga pessoas pessoa editores editor membros membro países país
mil milhões milhão bilhões pts pp usd dólares dólar reais brl vs versus campanhas campanha
anúncios anúncio keywords keyword bullets bullet parágrafos parágrafo blocos bloco tabelas tabela
cores cor fontes fonte pixels px ms segs pontos-chave benefícios benefício objeções objeção
razões razão motivos motivo gatilhos gatilho métricas métrica kpis kpi cenários cenário
hours minutes seconds weeks months years words lines creatives concepts times points questions
systems entries purchases customers orders units phrases variations versions options examples
fields sections steps defects domains phases brands competitors rules formulas angles themes
categories levels cycles rounds lots scenes videos images photos models routes columns files
pages comments answers elements ideas candidates plays mechanisms proofs studies tests samples
axes criteria cases people editors members countries reasons objections benefits triggers
metrics scenarios primeiros primeiras últimos últimas melhores piores principais maiores menores
top first last best worst main alternativas alternativa alternatives numeradas numerada
numerados numerado numbered
""".split())
UNIT_SYMBOL_RE = re.compile(r"^\s*(?:%|×|x\b|k\b|K\b|-\s*\d|\d|:\d|/\d|/[A-Za-zÀ-ÿ]{3,}|h\b|d\b|s\b|w\b|m\b|US\$|\$|USD\b|pts\b|pp\b|e\s+\d+\s*(?:%|x|×)|\)?\s*(?:%|×))")
NUM_BEFORE_WORDS = set("""
chega chegar chegou chegue chegam sobe subir sobem subiu cai cair caem caiu vai vão ir igual
iguais superior superiores inferior inferiores limite limitado limitada limitar reduz reduzir
reduzido reduzida aumenta aumentar aumentou próximo próxima equivale equivalente corresponde
passa passar passou volta voltar leva levar multiplica dividir elevar acima abaixo mais menos
cerca perto máximo mínimo até entre desde partir soma somar somam total totaliza multiplicado
dividido faixa range from to under over above below around approximately roughly
""".split())

# Só singular: skill é sempre "a 08" / "da 08"; plural com número ("as 20 mais", "dos 15 fatores") é quantidade.
PREP_SAFE = ("a", "à", "o", "da", "do", "na", "no", "pela", "pelo", "pra", "pro", "para", "via")
SKILL_WORD_RE = re.compile(r"\b(?:[Ss]kills?|SKILLS?)\s+(?:\*\*|__|\*|_)?$")
PREP_RE = re.compile(r"(?:^|(?<=[\s(\[|*_\"'“‘]))(" + "|".join(PREP_SAFE) + r")\s+(?:\*\*|__|\*|_)?$", re.I)
ARROW_RE = re.compile(r"[→←↔]\s*$")
PAREN_RE = re.compile(r"(?<![\w])\(\s*$")
# Palavra isolada: o apelido só é candidato quando não tem dígito colado antes ou depois, não vem
# depois de vírgula, ponto ou moeda ("1,12", "$12", "US$ 12") nem antes de vírgula ou ponto seguidos de
# dígito ("12,000", "18,7%"), não tem %, moeda ou unidade colados ("20%", "12k", "12h", "12min") e não
# faz parte de data AAAA-MM-DD ("2026-09-01": o hífen e o dígito colados já excluem). Fonte única do
# filtro, usada por legacy_re, TOKEN_RE e pelas regexes do relatório; o lint importa convert_line.
# O contexto numérico do `looks_numeric` completa o filtro: barra com dígito ou com mês dos dois lados
# é data ou razão ("11/11", "26/12", "10/nov"), faixa em português é medida ("de 5 a 10", "ETAPAs 8 a
# 14") e palavra de quantidade depois do número é contagem ("10 alternativas", "12 numeradas"), nunca
# apelido de skill.
ISOLATED_BEFORE = r"(?<![\w.\-:,$€£])(?<![$€£] )"
ISOLATED_AFTER = r"(?![\w\-$€£]|\s?%|[.,]\d)"
TOKEN_RE = re.compile(ISOLATED_BEFORE + r"(\d{2}[a-e]?)" + ISOLATED_AFTER)
SEP_FWD_RE = re.compile(r"^(?:\*\*|__|\*|_)?(?:\s*(?:/|→|←|↔|\+|;|,)\s*|\s+(?:e|ou|and|or)\s+|,\s+(?:e|ou|and|or)\s+)(?:\*\*|__|\*|_)?$")
SEP_BWD_RE = re.compile(r"^(?:\*\*|__|\*|_)?(?:\s*(?:/|→|←|↔|\+|;|,)\s*|\s+(?:e|ou|and|or)\s+|,\s+(?:e|ou|and|or)\s+)(?:\*\*|__|\*|_)?$")
RANGE_AFTER_RE = re.compile(r"^\s*(?:-|–|—|a|até|to)\s*\d")
TRACE = None   # lista opcional: cada troca de token solto entra como (kind, token, contexto)


# ----------------------------------------------------------------------------- registro
class Registry:
    def __init__(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.data = data
        self.skills = data["skills"]
        self.legacy = {}           # apelido → id
        self.token_map = {}        # (NN, slug) → slug novo
        self.names = {}            # id → nomes reconhecidos (minúsculos) para o caso `Nome (NN)`
        for s in self.skills:
            sid = s["id"]
            for lg in s.get("legacy_ids") or []:
                self.legacy[lg] = sid
                self.token_map[(lg, sid)] = sid
            lf = s.get("legacy_folder")
            if lf:
                m = re.match(r"^(\d{2}[a-e]?)-(.+)$", lf)
                if m:
                    self.token_map[(m.group(1), m.group(2))] = s["folder"]
            names = {sid, sid.replace("-", " "), (s.get("name") or "").lower()}
            self.names[sid] = {n for n in names if n}
        self.legacy_re = re.compile(ISOLATED_BEFORE + "(" + "|".join(sorted(self.legacy, key=len, reverse=True)) + ")" + ISOLATED_AFTER)
        self.slug_token_re = re.compile(
            r"(?<![\w\-])(\d{2}[a-e]?)-(" + "|".join(sorted({k[1] for k in self.token_map}, key=len, reverse=True)) + r")(?![\w\-])")


# ----------------------------------------------------------------------------- arquivos
def tracked_files():
    out = subprocess.run(["git", "-c", "core.quotePath=false", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, check=True).stdout.decode("utf-8", "replace")
    return sorted(f for f in out.split("\0") if f and (ROOT / f).is_file())


def in_scope(f):
    if not (f.startswith(SCOPE_PREFIXES) or f in SCOPE_FILES):
        return False
    if not f.endswith(TEXT_EXT):
        return False
    if f in EXCLUDED_FILES or f.startswith(EXCLUDED_DIRS):
        return False
    return True


def skipped_lines(relpath, lines):
    """Linhas (1-based) fora do alcance: seções históricas, blocos gerados e linhas marcadas."""
    skip = set()
    pats = HISTORICAL_SECTIONS.get(relpath, [])
    level = None
    in_gen = False
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if re.match(r"^(?:<!--|#) gen:[a-z-]+(?::[^ >]+)?:start", s):
            in_gen = True
        if in_gen:
            skip.add(i)
            if re.match(r"^(?:<!--|#) gen:[a-z-]+(?::[^ >]+)?:end", s):
                in_gen = False
            continue
        m = re.match(r"^(#{1,6})\s", l)
        if m and pats:
            if level is not None and len(m.group(1)) <= level:
                level = None
            if level is None and any(re.match(p, l) for p in pats):
                level = len(m.group(1))
        if level is not None or any(w in l for w in SKIP_LINE_WORDS):
            skip.add(i)
        elif relpath.endswith("manifest-schema.json") and ENUM_LINE_RE.match(l):
            skip.add(i)                     # enum de skills_completed: gerado pelo gen_docs.py
    return skip


# ----------------------------------------------------------------------------- conversão de uma linha
def code(sid, html):
    return f"<code>{sid}</code>" if html else f"`{sid}`"


def numeric_context(masked, start, end, prep_start, legacy=()):
    """True se o número em masked[start:end] parece contagem/medida, não skill."""
    after = masked[end:]
    if UNIT_SYMBOL_RE.match(after):
        return True
    m = re.match(r"^\s*\)?\s*([\wÀ-ÿ-]+)", after)
    if m and m.group(1).lower() in UNIT_WORDS:
        return True
    before = masked[:prep_start].rstrip()
    prep = masked[prep_start:start].strip().lower()
    # "da/na/pela/pra/via NN" só é número se vier unidade depois; as checagens de faixa e de
    # verbo numérico ("chega a 12", "de 10 a 20", "volta a 10") valem para a/à/o, setas e parêntese.
    strict = prep in ("a", "à", "o", "→", "←", "↔", "", "(")
    if not strict:
        return False
    if RANGE_AFTER_RE.match(after) or re.match(r"^\s*(?:–|—)\s*\d", after):
        return True
    if prep in ("→", "←", "↔"):
        m = re.search(r"(?<![\w.\-:])(\d{2}[a-e]?)\s*$", before)
        if m and m.group(1) in legacy:
            return False                                  # `08→10→11`: seta entre apelidos
    if re.search(r"\d\s*(?:%|×|x)?\s*$", before):
        return True
    m = re.search(r"([\wÀ-ÿ-]+)\s*$", before)
    if m and m.group(1).lower() in NUM_BEFORE_WORDS:
        return True
    return False


def convert_line(line, reg, html=False, stats=None):
    """Devolve (linha nova, número de trocas). Os nomes de LEGACY_REPORT_NAMES ficam intactos: saem da
    linha antes de qualquer troca (viram HIDDEN_MARK) e voltam, na mesma ordem, no fim."""
    hidden = LEGACY_REPORT_RE.findall(line)
    if not hidden:
        return _convert_line(line, reg, html, stats)
    out, changes = _convert_line(LEGACY_REPORT_RE.sub(HIDDEN_MARK, line), reg, html, stats)
    it = iter(hidden)
    return re.sub(re.escape(HIDDEN_MARK), lambda m: next(it), out), changes


def _convert_line(line, reg, html=False, stats=None):
    changes = 0

    # 1. token NN-slug → slug (inclui caminhos .claude/skills/NN-slug.md e pastas NN-slug/)
    def sub_token(m):
        nonlocal changes
        new = reg.token_map.get((m.group(1), m.group(2)))
        if not new:
            return m.group(0)
        changes += 1
        if stats is not None:
            stats["token"] += 1
        return new
    line = reg.slug_token_re.sub(sub_token, line)

    # 2. skill-NN → skill-<id>
    def sub_exec(m):
        nonlocal changes
        sid = reg.legacy.get(m.group(1))
        if not sid:
            return m.group(0)
        changes += 1
        if stats is not None:
            stats["executor"] += 1
        return "skill-" + sid
    line = re.sub(r"(?<![\w-])skill-(\d{2}[a-e]?)(?![\w-])", sub_exec, line)

    # 3. tokens soltos com âncora + expansão de listas
    tokens = [(m.start(), m.end(), m.group(1)) for m in reg.legacy_re.finditer(line)]
    if not tokens:
        return line, changes
    # máscara: todo token com âncora candidata vira "§§" para as checagens de contexto numérico
    anchors = {}
    for idx, (s, e, t) in enumerate(tokens):
        before = line[:s]
        kind = None
        if re.search(r"[a-e]$", t):
            kind = "letter"
        elif SKILL_WORD_RE.search(before):
            kind = "skill"
        elif PREP_RE.search(before):
            kind = "prep"
        elif PAREN_RE.search(before):
            kind = "paren"
        elif ARROW_RE.search(before):
            kind = "arrow"
        if kind:
            anchors[idx] = kind
    masked = list(line)
    for idx in anchors:
        s, e, _ = tokens[idx]
        masked[s:e] = "§" * (e - s)
    masked = "".join(masked)
    chosen = {}
    for idx, kind in anchors.items():
        s, e, t = tokens[idx]
        if kind == "letter":
            chosen[idx] = kind
            continue
        pm = (SKILL_WORD_RE.search(line[:s]) or PREP_RE.search(line[:s]) or PAREN_RE.search(line[:s])
              or ARROW_RE.search(line[:s]))
        prep_start = pm.start() if pm else s
        if kind == "skill" or (kind == "paren" and re.match(r"^\s*\)", line[e:])):
            chosen[idx] = kind          # `skill NN` e `(NN)` fechado: referência, não contagem
            continue
        if numeric_context(masked, s, e, prep_start, reg.legacy):
            continue
        chosen[idx] = kind
    if not chosen:
        return line, changes
    # expansão de listas: vizinhos ligados por separador (para frente e para trás)
    changed_any = True
    while changed_any:
        changed_any = False
        for idx in list(chosen):
            for nb in (idx + 1, idx - 1):
                if nb < 0 or nb >= len(tokens) or nb in chosen:
                    continue
                if nb == idx + 1:
                    between = line[tokens[idx][1]:tokens[nb][0]]
                    ok = bool(SEP_FWD_RE.fullmatch(between))
                else:
                    between = line[tokens[nb][1]:tokens[idx][0]]
                    ok = bool(SEP_BWD_RE.fullmatch(between))
                if ok and not RANGE_AFTER_RE.match(line[tokens[nb][1]:]):
                    chosen[nb] = "chain"
                    changed_any = True
    # aplicação, da direita para a esquerda
    out = line
    for idx in sorted(chosen, reverse=True):
        s, e, t = tokens[idx]
        sid = reg.legacy[t]
        kind = chosen[idx]
        repl = code(sid, html)
        cut_start = s
        if kind == "paren" and re.match(r"^\s*\)", out[e:]):
            # `Nome (NN)` → `Nome`; `outra coisa (NN)` → `outra coisa (<id>)`
            pm = PAREN_RE.search(out[:s])
            open_at = pm.start()
            prefix = out[:open_at].rstrip().lower()
            if any(prefix.endswith(n) for n in reg.names[sid]) or prefix.endswith(sid):
                close = re.match(r"^\s*\)", out[e:]).end()
                out = out[:open_at].rstrip(" ") + out[e + close:]
                changes += 1
                if stats is not None:
                    stats["paren-drop"] += 1
                continue
        if TRACE is not None:
            TRACE.append((kind, t, line[max(0, s - 55):e + 40]))
        out = out[:cut_start] + repl + out[e:]
        changes += 1
        if stats is not None:
            stats[kind] += 1
    return out, changes


# ----------------------------------------------------------------------------- relatório
REPORT_TAGS = {
    "letter": "forma com letra",
    "skill": "skill NN",
    "prep": "preposição + NN",
    "paren": "(NN)",
    "arrow": "seta + NN",
    "range": "faixa com hífen",
    "list": "lista / tabela",
    "bare": "número solto",
}


def looks_numeric(line, s, e):
    """Número com cara de medida: unidade/percentual depois, ou dígito, `$`, `~`, `/`, `≥`, `<` colado antes."""
    after = line[e:]
    if UNIT_SYMBOL_RE.match(after) or re.match(r"^\s*(?:-|–|—)\s*\d", after):
        return True
    m = re.match(r"^\s*\)?\s*([\wÀ-ÿ-]+)", after)
    if m and m.group(1).lower() in UNIT_WORDS:
        return True
    if re.search(r"\d+\s+a\s+$", line[:s]):
        return True                                       # faixa em português: "de 5 a 10", "ETAPAs 8 a 14"
    return bool(re.search(r"(?:\d|[$~≥≤<>=/×x]|US\$)\s*$", line[:s]))


def report_line(line, reg, all_numbers=False):
    """Menções numéricas que ainda parecem referência a skill: lista de (tag, token, contexto)."""
    found = []
    for m in reg.legacy_re.finditer(line):
        s, e, t = m.start(), m.end(), m.group(1)
        before, after = line[:s], line[e:]
        if not re.search(r"[a-e]$", t) and looks_numeric(line, s, e) and not all_numbers:
            continue
        tag = None
        if re.search(r"[a-e]$", t):
            tag = "letter"
        elif SKILL_WORD_RE.search(before):
            tag = "skill"
        elif PREP_RE.search(before):
            tag = "prep"
        elif PAREN_RE.search(before) and re.match(r"^\s*\)", after):
            tag = "paren"
        elif ARROW_RE.search(before) or re.match(r"^\s*[→←↔]", after):
            tag = "arrow"
        elif re.search(r"(?:^|\|)\s*$", before) and re.match(r"^\s*(?:,|\||$)", after):
            tag = "list"
        elif re.search(r"/\s*$", before) or re.match(r"^\s*/", after):
            tag = "list"
        elif all_numbers:
            tag = "bare"
        if tag:
            found.append((tag, t, line[max(0, s - 45):e + 35].strip()))
    # faixas com hífen (00-20, 07a-07d) e "07" solto: a regex de token não pega
    for m in re.finditer(ISOLATED_BEFORE + r"(\d{2}[a-e]?)-(\d{2}[a-e]?)" + ISOLATED_AFTER, line):
        if m.group(1) in reg.legacy and m.group(2) in reg.legacy:
            if not all_numbers and (looks_numeric(line, m.start(), m.end()) or re.match(r"^\s*(?:%|dias|min)", line[m.end():])):
                continue
            found.append(("range", m.group(0), line[max(0, m.start() - 45):m.end() + 35].strip()))
    for m in re.finditer(ISOLATED_BEFORE + "07" + ISOLATED_AFTER, line):
        found.append(("bare", "07", line[max(0, m.start() - 45):m.end() + 35].strip()))
    return found


# ----------------------------------------------------------------------------- skills.json
def walk_prose(s, fn):
    for k in PROSE_FIELDS:
        v = s.get(k)
        if isinstance(v, str):
            s[k] = fn(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                if isinstance(vv, str):
                    v[kk] = fn(vv)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Troca referências numéricas a skills pelos ids do registro.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__.split("Modos:")[1] if "Modos:" in __doc__ else "")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true", help="grava as trocas mecânicas")
    g.add_argument("--dry-run", action="store_true", help="mostra o que --apply mudaria, sem gravar")
    g.add_argument("--report", action="store_true", help="lista o que sobrou para revisão manual (padrão)")
    ap.add_argument("--diff", action="store_true", help="com --dry-run: imprime o diff unificado")
    ap.add_argument("--all", action="store_true", help="com --report: lista todo número que coincide com um apelido")
    ap.add_argument("--files", action="append", default=[], help="prefixo de caminho (repetível)")
    args = ap.parse_args()
    mode = "apply" if args.apply else "dry-run" if args.dry_run else "report"

    try:
        reg = Registry()
    except (OSError, ValueError, KeyError) as e:
        print(f"ERRO  não consegui ler {REGISTRY.relative_to(ROOT)}: {e}")
        return 1

    files = [f for f in tracked_files() if in_scope(f) or f == SPECIAL_JSON]
    if args.files:
        files = [f for f in files if any(f.startswith(p) for p in args.files)]

    total_changes, total_report = 0, 0
    per_file_stats = {}
    for f in files:
        path = ROOT / f
        html = f.endswith(".html")
        if f == SPECIAL_JSON:
            data = json.loads(path.read_text(encoding="utf-8"))
            stats = {k: 0 for k in ("token", "executor", "letter", "skill", "prep", "paren", "arrow", "chain", "paren-drop")}
            n = 0
            rep = []
            for s in data["skills"]:
                def fn(v):
                    nonlocal n
                    new, c = convert_line(v, reg, False, stats)
                    n += c
                    return new
                def rp(v):
                    for tag, t, ctx in report_line(v, reg, args.all):
                        rep.append((s["id"], tag, t, ctx))
                    return v
                if mode == "report":
                    walk_prose(s, rp)
                else:
                    walk_prose(s, fn)
            if mode == "report":
                for sid, tag, t, ctx in rep:
                    print(f"{f}:{sid}  {REPORT_TAGS[tag]}  [{t}]  …{ctx}…")
                total_report += len(rep)
            elif n:
                new_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
                per_file_stats[f] = stats
                total_changes += n
                if mode == "apply":
                    path.write_text(new_text, encoding="utf-8")
                elif args.diff:
                    old_text = path.read_text(encoding="utf-8")
                    sys.stdout.writelines(difflib.unified_diff(old_text.splitlines(True), new_text.splitlines(True),
                                                               fromfile=f, tofile=f + " (novo)"))
            continue

        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        skip = skipped_lines(f, lines)
        if mode == "report":
            for i, l in enumerate(lines, 1):
                if i in skip:
                    continue
                for tag, t, ctx in report_line(l, reg, args.all):
                    print(f"{f}:{i}  {REPORT_TAGS[tag]}  [{t}]  …{ctx}…")
                    total_report += 1
            continue
        stats = {k: 0 for k in ("token", "executor", "letter", "skill", "prep", "paren", "arrow", "chain", "paren-drop")}
        n = 0
        new_lines = []
        for i, l in enumerate(lines, 1):
            if i in skip:
                new_lines.append(l)
                continue
            nl, c = convert_line(l, reg, html, stats)
            n += c
            new_lines.append(nl)
        if n:
            per_file_stats[f] = stats
            total_changes += n
            new_text = "\n".join(new_lines)
            if mode == "apply":
                path.write_text(new_text, encoding="utf-8")
            elif args.diff:
                sys.stdout.writelines(difflib.unified_diff(text.splitlines(True), new_text.splitlines(True),
                                                           fromfile=f, tofile=f + " (novo)"))

    if mode == "report":
        print(f"{total_report} menção(ões) numérica(s) para revisar" if total_report else "OK  nenhuma menção numérica a skill sobrou")
        return 1 if total_report else 0
    for f, st in sorted(per_file_stats.items()):
        parts = " ".join(f"{k}={v}" for k, v in st.items() if v)
        print(f"{'gravado' if mode == 'apply' else 'mudaria'}  {f}  ({parts})")
    print(f"{total_changes} troca(s) em {len(per_file_stats)} arquivo(s)" + ("" if mode == "apply" else " (nada gravado)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
