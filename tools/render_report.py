#!/usr/bin/env python3
"""
render_report.py: gera o .html companion de um relatório .md da Aura.

O .md é o que a AI escreve e lê nas fases seguintes; o .html é o que o membro abre no
navegador. Este script monta o .html a partir do .md usando
`.claude/templates/aura-report-template.html` como base (o <style> completo, a topbar com a
logo SVG canônica, o hero, a meta-bar, o sumário gerado dos `##`, o rodapé e o <script> de
interação). Nenhuma skill escreve HTML de relatório à mão.

Uso:
  python3 tools/render_report.py workspace/<slug>/market-research/market-research.md
  python3 tools/render_report.py <arquivo.md> --lang en --out /caminho/saida.html
  python3 tools/render_report.py <arquivo.md> --no-dark     (sem alternar bandas escuras)

Sem --out, o .html nasce ao lado do .md, com o mesmo nome. Sem --lang, o idioma do chrome
(sumário, rótulos da meta-bar) vem do frontmatter (`lang`), depois do `report_language` do
manifest do produto, e por fim pt-BR. A copy do relatório sai como está no .md.

Conversor de Markdown (mínimo, por desenho): títulos, parágrafos, listas (aninhadas, com
citação dentro do item), tabelas, negrito, itálico, código (em linha e em bloco), links,
imagens, citações e réguas horizontais. Comentários HTML são descartados. Todo o resto é
texto escapado: o .md nunca injeta HTML cru.

Convenções que viram componentes do design system (detalhes em
`.claude/templates/aura-html-components.md`):
  `# Título`                          → título do relatório (hero); o 1º parágrafo vira o deck
  `## Seção`                          → seção numerada, entra no sumário ("N. " na frente é removido)
  `### Subseção`                      → subseção
  `> **Nota:** ...`                   → card .note         (`**Note:**` em inglês)
  `> **Atenção:** ...`                → card .callout      (`**Attention:**` ou `**Warning:**`)
  `> **Oportunidade:** ...`           → card .opportunity  (`**Opportunity:**`)
  `> **Risco:** ...`                  → card .danger       (`**Risk:**`)
  `> **Vencedor:** Nome` + parágrafo  → card .winner       (`**Winner:**`)
  `> "frase do cliente"` + `> Tradução livre: ...` + `> Fonte: ...`  → citação VOC (.quote)
  tabela de 2 colunas com cabeçalho `KPI | Valor` (ou `KPI | Value`)  → números grandes (.kpi-grid)
  qualquer outra tabela               → .table-wrap

Frontmatter YAML simples (opcional, no topo do .md, entre duas linhas `---`): `produto`,
`mercado`, `data` e `alimenta` preenchem a meta-bar; `titulo`, `subtitulo`, `eyebrow`,
`tipo` e `lang` ajustam o hero e o chrome; qualquer outra chave vira um item extra da
meta-bar (o rótulo é a chave com inicial maiúscula). Sem frontmatter, a meta-bar sai do
manifest do produto (`product_name`, `market`), da data de hoje e dos consumidores da skill
no `.claude/skills.json` (a skill é reconhecida pela pasta onde o .md está).

Nunca trunca conteúdo. Só biblioteca padrão. Exit 0 = .html escrito; exit 1 = erro (arquivo,
template ou permissão).
"""
import argparse
import datetime as _dt
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / ".claude" / "templates" / "aura-report-template.html"
LOGO_SNIPPET = ROOT / ".claude" / "templates" / "aura-logo-snippet.html"
REGISTRY = ROOT / ".claude" / "skills.json"

LANGS = ("pt-BR", "en")
CHROME = {
    "pt-BR": {"skip": "Pular para o conteúdo", "nav": "Navegação", "state": "Relatório validado",
              "toc": "Sumário", "produto": "Produto", "mercado": "Mercado", "data": "Data",
              "alimenta": "Alimenta", "kind": "Relatório"},
    "en": {"skip": "Skip to content", "nav": "Navigation", "state": "Validated report",
           "toc": "Contents", "produto": "Product", "mercado": "Market", "data": "Date",
           "alimenta": "Feeds", "kind": "Report"},
}
META_KEYS = ("produto", "mercado", "data", "alimenta")
META_ALIASES = {"product": "produto", "market": "mercado", "date": "data", "feeds": "alimenta",
                "título": "titulo", "subtítulo": "subtitulo"}
RESERVED_META = {"titulo", "title", "subtitulo", "subtitle", "eyebrow", "tipo", "kind", "lang", "idioma"}
MARKETS = {"US": ("Estados Unidos", "United States"), "BR": ("Brasil", "Brazil"),
           "UK": ("Reino Unido", "United Kingdom"), "GB": ("Reino Unido", "United Kingdom"),
           "CA": ("Canadá", "Canada"), "AU": ("Austrália", "Australia"), "EU": ("Europa", "Europe")}
MONTHS = {"pt-BR": ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"],
          "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}

# rótulo (minúsculo, como escrito no .md) → classe do card
CALLOUT_LABELS = {
    "nota": "note", "note": "note",
    "atenção": "callout", "atencao": "callout", "attention": "callout", "warning": "callout", "aviso": "callout",
    "oportunidade": "opportunity", "opportunity": "opportunity",
    "risco": "danger", "risk": "danger", "perigo": "danger", "danger": "danger",
    "vencedor": "winner", "winner": "winner",
}
KPI_HEADERS = ({"kpi", "métrica", "metrica", "metric"}, {"valor", "value"})

# ----------------------------------------------------------------------------- regexes de bloco
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([\w+.-]*)\s*$")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
QUOTE_RE = re.compile(r"^\s{0,3}>\s?(.*)$")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)*\|?\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])(?:\s+(.*)|\s*$)")
TASK_RE = re.compile(r"^\[([ xX])\]\s+")
LABEL_RE = re.compile(r"^\*\*\s*([^*]+?)\s*:?\s*\*\*\s*:?\s*(.*)$")
TRANS_RE = re.compile(r"^(?:tradu[çc][ãa]o livre|free translation)\s*:", re.I)
SRC_RE = re.compile(r"^(?:(?:fonte|source)\s*:\s*|[—–]\s*)(.+)$", re.I)
LABEL_LINE_RE = re.compile(r"^\*\*[^*]+:\s*\*\*")
NUM_RE = re.compile(r"^([^\d+-]*)([-+]?\d+(?:\.\d{1,2})?)(.*)$")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


class RenderError(Exception):
    pass


# ----------------------------------------------------------------------------- inline
def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def inline(text):
    """Markdown em linha → HTML. Escapa tudo que não for markup reconhecido."""
    codes = []

    def keep_code(m):
        codes.append(m.group(2))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"(`+)(.+?)\1", keep_code, text, flags=re.S)
    text = esc(text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\)",
                  lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+&quot;[^&]*&quot;)?\)",
                  lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text, flags=re.S)
    text = re.sub(r"(?<!\w)__(?=\S)(.+?)(?<=\S)__(?!\w)", r"<strong>\1</strong>", text, flags=re.S)
    text = re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<em>\1</em>", text, flags=re.S)
    text = re.sub(r"(?<!\w)_(?![\s_])(.+?)(?<![\s_])_(?!\w)", r"<em>\1</em>", text, flags=re.S)
    text = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"<del>\1</del>", text, flags=re.S)
    text = text.replace("\x01", "<br>").replace("\n", " ")
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{esc(codes[int(m.group(1))])}</code>", text)


def join_paragraph(lines):
    """Junta as linhas de um parágrafo: quebra dura (dois espaços ou barra no fim, ou linha
    seguinte começando com um rótulo `**Rótulo:**`) vira <br>; o resto vira espaço."""
    out = []
    for k, l in enumerate(lines):
        s = l.strip()
        if k:
            prev = lines[k - 1]
            hard = prev.endswith("  ") or prev.rstrip().endswith("\\") or LABEL_LINE_RE.match(s)
            out.append("\x01" if hard else "\n")
        out.append(s.rstrip("\\").rstrip() if s.endswith("\\") else s)
    return "".join(out)


def plain(html_text):
    return re.sub(r"<[^>]+>", "", html_text)


# ----------------------------------------------------------------------------- blocos
def is_block_start(line):
    return bool(HEADING_RE.match(line) or FENCE_RE.match(line) or HR_RE.match(line)
                or QUOTE_RE.match(line) or TABLE_ROW_RE.match(line) or LIST_RE.match(line))


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def dedent(lines):
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    cut = min(indents) if indents else 0
    return [l[cut:] if l.strip() else "" for l in lines]


def parse_list(lines, i):
    n = len(lines)
    m = LIST_RE.match(lines[i])
    base = len(m.group(1))
    ordered = m.group(2)[0].isdigit()
    start = int(m.group(2)[:-1]) if ordered else 1
    items = []
    while i < n:
        m = LIST_RE.match(lines[i])
        if not m or len(m.group(1)) != base or m.group(2)[0].isdigit() != ordered:
            break
        first = m.group(3) or ""
        body = []
        i += 1
        while i < n:
            l = lines[i]
            if not l.strip():
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j >= n:
                    i = j
                    break
                nxt = lines[j]
                mm = LIST_RE.match(nxt)
                ind = len(nxt) - len(nxt.lstrip())
                if mm and len(mm.group(1)) == base:
                    i = j            # próximo item da mesma lista (lista com linhas em branco)
                    break
                if ind > base:
                    body.extend([""] * (j - i))
                    i = j
                    continue
                i = j
                break
            ind = len(l) - len(l.lstrip())
            mm = LIST_RE.match(l)
            if mm and len(mm.group(1)) <= base:
                break
            if ind > base:
                body.append(l)
                i += 1
                continue
            if (body and not body[-1].strip()) or is_block_start(l):
                break
            body.append(l)          # continuação sem recuo, logo abaixo do item
            i += 1
        items.append((first, dedent(body)))
    return {"t": "list", "ordered": ordered, "start": start, "items": items}, i


def parse_blocks(lines):
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = FENCE_RE.match(line)
        if m:
            fence = m.group(1)[0]
            close = re.compile(r"^\s{0,3}" + re.escape(fence) + r"{3,}\s*$")
            code = []
            i += 1
            while i < n and not close.match(lines[i]):
                code.append(lines[i])
                i += 1
            i += 1
            blocks.append({"t": "code", "lang": m.group(2), "lines": code})
            continue
        m = HEADING_RE.match(line)
        if m:
            blocks.append({"t": "h", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue
        if HR_RE.match(line):
            blocks.append({"t": "hr"})
            i += 1
            continue
        if QUOTE_RE.match(line):
            inner = []
            while i < n and QUOTE_RE.match(lines[i]):
                inner.append(QUOTE_RE.match(lines[i]).group(1))
                i += 1
            blocks.append({"t": "quote", "lines": inner})
            continue
        if TABLE_ROW_RE.match(line) and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            header = split_row(line)
            i += 2
            rows = []
            while i < n and TABLE_ROW_RE.match(lines[i]):
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append({"t": "table", "header": header, "rows": rows})
            continue
        if LIST_RE.match(line):
            block, i = parse_list(lines, i)
            blocks.append(block)
            continue
        para = [line]
        i += 1
        while i < n and lines[i].strip() and not is_block_start(lines[i]):
            para.append(lines[i])
            i += 1
        blocks.append({"t": "p", "lines": para})
    return blocks


# ----------------------------------------------------------------------------- render de blocos
CARD_TYPES = ("table", "quote", "code")


def render_list(b):
    tag = "ol" if b["ordered"] else "ul"
    attrs = f' start="{b["start"]}"' if b["ordered"] and b["start"] != 1 else ""
    out = [f"<{tag}{attrs}>"]
    for first, body in b["items"]:
        first = TASK_RE.sub(lambda m: "☑ " if m.group(1).lower() == "x" else "☐ ", first)
        sub = parse_blocks([first] + body)
        parts = []
        if sub and sub[0]["t"] == "p":
            parts.append(inline(join_paragraph(sub[0]["lines"])))
            sub = sub[1:]
        parts.extend(render_block(s, nested=True) for s in sub)
        out.append("<li>" + "".join(parts) + "</li>")
    out.append(f"</{tag}>")
    return "\n".join(out)


def render_inner(blocks, sep):
    """Conteúdo de um card: parágrafos sem <p> (separados por <br><br>) ou com <p>."""
    out = ""
    prev_p = False
    for b in blocks:
        if b["t"] == "p":
            text = inline(join_paragraph(b["lines"]))
            if sep == "br":
                out += ("<br><br>" if prev_p else "") + text
            else:
                out += f"<p>{text}</p>"
            prev_p = True
        else:
            out += render_block(b, nested=True)
            prev_p = False
    return out


def render_quote(b, nested=False):
    lines = b["lines"]
    rv = "" if nested else " reveal"
    k = next((idx for idx, l in enumerate(lines) if l.strip()), None)
    if k is None:
        return ""
    m = LABEL_RE.match(lines[k].strip())
    kind = CALLOUT_LABELS.get(m.group(1).strip().lower()) if m else None
    if kind:
        label = m.group(1).strip()
        rest = [m.group(2)] + lines[k + 1:]
        if kind == "winner":
            name_idx = next((idx for idx, l in enumerate(rest) if l.strip()), None)
            name = rest[name_idx].strip() if name_idx is not None else ""
            body = rest[name_idx + 1:] if name_idx is not None else []
            inner = render_inner(parse_blocks(body), "p")
            return (f'<div class="winner{rv}"><div class="winner-label">{esc(label)}</div>'
                    f'<div class="winner-name">{inline(name)}</div>{inner}</div>')
        inner = render_inner(parse_blocks(rest), "br")
        return f'<div class="{kind}{rv}"><strong>{esc(label)}</strong> {inner}</div>'
    main, trans, sources = [], [], []
    for l in lines:
        s = l.strip()
        if TRANS_RE.match(s):
            trans.append(s)
        elif SRC_RE.match(s) and not LIST_RE.match(l):
            sources.append(SRC_RE.match(s).group(1).strip())
        else:
            main.append(l)
    out = [f'<div class="quote{rv}">', render_inner(parse_blocks(main), "br")]
    for t in trans:
        out.append(f'<span class="quote-pt">{inline(t)}</span>')
    if sources:
        out.append(f'<span class="quote-source">{inline(" · ".join(sources))}</span>')
    out.append("</div>")
    return "".join(out)


def is_kpi_table(b):
    if len(b["header"]) != 2:
        return False
    h1, h2 = (h.strip().lower() for h in b["header"])
    return h1 in KPI_HEADERS[0] and h2 in KPI_HEADERS[1]


def render_kpi(b, nested=False):
    rv = "" if nested else " reveal"
    cards = []
    for row in b["rows"]:
        label = row[0] if row else ""
        value = row[1] if len(row) > 1 else ""
        m = NUM_RE.match(value.strip())
        count = ""
        exact = bool(m) and (str(int(m.group(2))) == m.group(2) if "." not in m.group(2) else str(float(m.group(2))) == m.group(2))
        if m and exact and len(m.group(1)) <= 6 and len(m.group(3)) <= 12 and not re.search(r"\d", m.group(3)):
            count = f' data-count="{m.group(2)}"'
            if m.group(1):
                count += f' data-prefix="{attr(m.group(1))}"'
            if m.group(3):
                count += f' data-suffix="{attr(m.group(3))}"'
        cards.append(f'<div class="kpi-card"><div class="big-num"{count}>{inline(value)}</div>'
                     f'<div class="big-num-label">{inline(label)}</div></div>')
    return f'<div class="kpi-grid{rv}">' + "".join(cards) + "</div>"


def render_table(b, nested=False):
    if is_kpi_table(b):
        return render_kpi(b, nested)
    rv = "" if nested else " reveal"
    head = "".join(f"<th>{inline(c)}</th>" for c in b["header"])
    rows = []
    for row in b["rows"]:
        cells = list(row) + [""] * (len(b["header"]) - len(row))
        rows.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
    return (f'<div class="table-wrap{rv}"><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def render_code(b):
    lang = f' class="language-{attr(b["lang"])}"' if b["lang"] else ""
    return f"<pre><code{lang}>{esc(chr(10).join(b['lines']))}</code></pre>"


def render_block(b, nested=False):
    t = b["t"]
    if t == "p":
        return f"<p>{inline(join_paragraph(b['lines']))}</p>"
    if t == "h":
        return f"<p><strong>{inline(b['text'])}</strong></p>"
    if t == "hr":
        return "<hr>"
    if t == "code":
        return render_code(b)
    if t == "quote":
        return render_quote(b, nested)
    if t == "table":
        return render_table(b, nested)
    if t == "list":
        return render_list(b)
    raise RenderError(f"bloco desconhecido: {t}")


# ----------------------------------------------------------------------------- frontmatter e contexto
def parse_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    meta = {}
    for k, l in enumerate(lines[1:], 1):
        if l.strip() == "---":
            return meta, "\n".join(lines[k + 1:])
        m = re.match(r"^([^:#][^:]*?)\s*:\s*(.*)$", l)
        if m:
            key = m.group(1).strip().lower()
            key = META_ALIASES.get(key, key)
            val = m.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            meta[key] = val
    return {}, text     # `---` sem fechamento: não é frontmatter (é uma régua)


def norm_lang(value):
    if not value:
        return None
    v = value.strip().lower().replace("_", "-")
    if v.startswith("pt"):
        return "pt-BR"
    if v.startswith("en"):
        return "en"
    return None


def find_manifest(md_path):
    if md_path is None:
        return None, None
    md_path = Path(md_path).resolve()
    for parent in (md_path.parent, md_path.parent.parent):
        mf = parent / "manifest.json"
        if mf.is_file():
            try:
                return json.loads(mf.read_text(encoding="utf-8")), parent
            except (OSError, json.JSONDecodeError):
                return None, None
    return None, None


def load_registry():
    if not REGISTRY.is_file():
        return None
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8")).get("skills") or None
    except (OSError, json.JSONDecodeError):
        return None


def find_skill(md_path, product_dir, skills):
    if not (md_path and product_dir and skills):
        return None
    try:
        rel = Path(md_path).resolve().relative_to(product_dir)
    except ValueError:
        return None
    if len(rel.parts) < 2:
        return None
    folder = rel.parts[0]
    matches = [s for s in skills if s.get("folder") == folder]
    if not matches:
        return None
    for s in matches:
        if s.get("report_stem") == Path(md_path).stem:
            return s
    return matches[0]


def format_date(d, lang):
    if lang == "en":
        return f"{MONTHS['en'][d.month - 1]} {d.day}, {d.year}"
    return f"{d.day} {MONTHS['pt-BR'][d.month - 1]} {d.year}"


def market_label(code, lang):
    if not code:
        return ""
    pair = MARKETS.get(str(code).strip().upper())
    if not pair:
        return str(code)
    return pair[1] if lang == "en" else pair[0]


def default_meta(lang, manifest, skill, skills, today):
    items = []
    if manifest and manifest.get("product_name"):
        items.append((CHROME[lang]["produto"], str(manifest["product_name"])))
    if manifest and manifest.get("market"):
        items.append((CHROME[lang]["mercado"], market_label(manifest["market"], lang)))
    items.append((CHROME[lang]["data"], format_date(today, lang)))
    if skill and skills:
        by_id = {s["id"]: s for s in skills}
        names = [by_id[c]["name"] for c in (skill.get("consumers") or []) if c in by_id]
        if names:
            items.append((CHROME[lang]["alimenta"], " · ".join(names)))
    return items


def meta_items(meta, lang):
    items = []
    for key, val in meta.items():
        if key in RESERVED_META or not val:
            continue
        label = CHROME[lang][key] if key in META_KEYS else key[:1].upper() + key[1:]
        items.append((label, val))
    return items


# ----------------------------------------------------------------------------- template
def load_template():
    if not TEMPLATE.is_file():
        raise RenderError(f"template não encontrado: {TEMPLATE.relative_to(ROOT)}")
    text = TEMPLATE.read_text(encoding="utf-8")
    try:
        head = text[: text.index("</head>")]
        topbar = re.search(r'<header class="topbar".*?</header>', text, re.S).group(0)
        script = text[text.rindex("<script>"): text.rindex("</script>") + len("</script>")]
    except (ValueError, AttributeError):
        raise RenderError("template sem <head>, topbar ou <script> reconhecíveis")
    head = re.sub(r"\s*<!--.*?-->", "", head, flags=re.S)
    if "<svg" not in topbar or "<path" not in topbar:
        raise RenderError("a topbar do template está sem a logo SVG")
    if LOGO_SNIPPET.is_file():
        d_tpl = re.search(r'<path d="([^"]+)"', topbar)
        d_snp = re.search(r'<path d="([^"]+)"', LOGO_SNIPPET.read_text(encoding="utf-8"))
        if d_tpl and d_snp and d_tpl.group(1) != d_snp.group(1):
            print("aviso: a logo da topbar do template diverge do snippet canônico "
                  f"({LOGO_SNIPPET.relative_to(ROOT)})", file=sys.stderr)
    return head, topbar, script


def fill(chunk, mapping):
    for key, val in mapping.items():
        chunk = chunk.replace("{{" + key + "}}", val)
    if "{{" in chunk:
        left = re.findall(r"\{\{[A-Z_]+\}\}", chunk)
        raise RenderError(f"placeholder do template sem valor: {', '.join(sorted(set(left)))}")
    return chunk


# ----------------------------------------------------------------------------- documento
def render_document(md_text, *, lang=None, source=None, dark=True, today=None):
    """Texto do .md → HTML completo (string). `source` é o caminho do .md (usado só para achar
    o manifest do produto e a skill da pasta); `today` fixa a data padrão (testes)."""
    meta, body = parse_frontmatter(md_text)
    manifest, product_dir = find_manifest(source)
    skills = load_registry()
    skill = find_skill(source, product_dir, skills)
    lang = (norm_lang(lang) or norm_lang(meta.get("lang") or meta.get("idioma"))
            or norm_lang(manifest.get("report_language") if manifest else None) or "pt-BR")
    today = today or _dt.date.today()
    chrome = CHROME[lang]

    body = COMMENT_RE.sub("", body)
    blocks = parse_blocks(body.split("\n"))

    title = meta.get("titulo") or meta.get("title") or ""
    subtitle_md = meta.get("subtitulo") or meta.get("subtitle") or ""
    lead, sections = [], []       # sections: dicts {title, html: [..]}
    cur, sub_open = None, False

    def close_sub():
        nonlocal sub_open
        if sub_open and cur is not None:
            cur["html"].append("</div>")
            sub_open = False

    h1_seen = False
    for b in blocks:
        if b["t"] == "h" and b["level"] == 1 and not h1_seen:
            h1_seen = True                  # o 1º H1 é o título (o frontmatter, se tiver `titulo`, vence)
            title = title or b["text"]
            continue
        if b["t"] == "h" and b["level"] <= 2 or (b["t"] == "h" and b["level"] == 3 and cur is None):
            close_sub()
            text = re.sub(r"^\d+[.)]\s+", "", b["text"])
            cur = {"title": text, "html": []}
            sections.append(cur)
            continue
        if b["t"] == "h" and b["level"] == 3:
            close_sub()
            cur["html"].append(f'<div class="subsection reveal"><div class="subsection-title">{inline(b["text"])}</div>')
            sub_open = True
            continue
        if cur is None:
            lead.append(b)
            continue
        if b["t"] in CARD_TYPES:
            close_sub()
            cur["html"].append(render_block(b))
        else:
            cur["html"].append(render_block(b))
    close_sub()

    lead_html = []
    subtitle = inline(subtitle_md) if subtitle_md else None
    for b in lead:
        if b["t"] == "p" and subtitle is None and not lead_html:
            subtitle = inline(join_paragraph(b["lines"]))     # 1º parágrafo do .md = deck do hero
            continue
        if b["t"] == "hr":
            continue
        lead_html.append(render_block(b))
    subtitle = subtitle or ""
    if not title:
        title = Path(source).stem if source else chrome["kind"]

    if meta and any(k not in RESERVED_META for k in meta):
        items = meta_items(meta, lang)
    else:
        items = default_meta(lang, manifest, skill, skills, today)
    date_val = meta.get("data") or meta.get("date") or ""
    m = re.search(r"\b(19|20)\d{2}\b", date_val)
    year = m.group(0) if m else str(today.year)
    kind = meta.get("tipo") or meta.get("kind") or (skill["name"] if skill else chrome["kind"])
    eyebrow = meta.get("eyebrow") or ("Aura Engine / " + skill["name"].lower() if skill else "Aura Engine")

    head, topbar, script = load_template()
    head = head.replace('<html lang="pt-BR">', f'<html lang="{lang}">', 1)
    head = fill(head, {"TITLE": esc(plain(inline(title)))})
    topbar = topbar.replace('aria-label="Navegação"', f'aria-label="{attr(chrome["nav"])}"')
    topbar = topbar.replace('aria-label="Relatório validado"', f'aria-label="{attr(chrome["state"])}"')
    topbar = fill(topbar, {"REPORT_KIND": esc(kind), "YEAR": year})

    out = [head, "</head>", '<body id="top">',
           f'<a class="skip-link" href="#conteudo">{esc(chrome["skip"])}</a>',
           '<div class="progress-line" aria-hidden="true"></div>', "", topbar, "",
           '<main id="conteudo" class="container">', "", '  <header class="hero">',
           f'    <p class="eyebrow reveal">{esc(eyebrow)}</p>',
           f'    <h1 class="page-title reveal">{inline(title)}</h1>']
    if subtitle:
        out.append(f'    <p class="page-subtitle reveal">{subtitle}</p>')
    out.append("  </header>")
    if items:
        out.append(f'  <div class="meta-bar reveal" data-n="{len(items)}">')
        for label, val in items:
            out.append(f"    <div><strong>{esc(label)}</strong> {inline(val)}</div>")
        out.append("  </div>")
    out.extend("  " + h for h in lead_html)
    if sections:
        out.append(f'  <div class="toc reveal"><div class="toc-title">{esc(chrome["toc"])}</div><ol>')
        for n, s in enumerate(sections, 1):
            out.append(f'    <li><a href="#s{n}">{plain(inline(s["title"]))}</a></li>')
        out.append("  </ol></div>")
    for n, s in enumerate(sections, 1):
        cls = "section dark" if dark and n % 2 == 0 else "section"
        out.append("")
        out.append(f'  <section class="{cls}" id="s{n}">')
        out.append(f'    <div class="section-label reveal"><span class="num">{n:02d}</span>{inline(s["title"])}</div>')
        out.extend("    " + h for h in s["html"])
        out.append("  </section>")
    out.extend(["", f"  <p class=\"footer\">Aura © {year}</p>", "", "</main>", "", script, "</body>", "</html>", ""])
    return "\n".join(out)


def render_file(md_path, out_path=None, lang=None, dark=True):
    md_path = Path(md_path)
    if not md_path.is_file():
        raise RenderError(f"arquivo não encontrado: {md_path}")
    try:
        text = md_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise RenderError(f"arquivo não é UTF-8: {md_path}")
    html_text = render_document(text, lang=lang, source=md_path, dark=dark)
    out = Path(out_path) if out_path else md_path.with_suffix(".html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    return out


def main():
    ap = argparse.ArgumentParser(description="Gera o .html companion de um relatório .md da Aura a partir do template.")
    ap.add_argument("md", help="caminho do relatório .md")
    ap.add_argument("--lang", choices=LANGS, help="idioma do chrome (padrão: frontmatter, manifest, pt-BR)")
    ap.add_argument("--out", help="caminho do .html (padrão: ao lado do .md, mesmo nome)")
    ap.add_argument("--no-dark", action="store_true", help="não alterna bandas escuras entre as seções")
    args = ap.parse_args()
    try:
        out = render_file(args.md, args.out, args.lang, dark=not args.no_dark)
    except (RenderError, OSError) as e:
        print(f"ERRO  {e}", file=sys.stderr)
        return 1
    try:
        shown = out.resolve().relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"gerado  {shown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
