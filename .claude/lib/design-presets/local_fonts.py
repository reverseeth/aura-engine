#!/usr/bin/env python3
"""
local_fonts.py — inventário e provisionamento de arquivos de fonte que o membro baixou.

Por que existe: a `page-design` sugere duas famílias (uma aberta, do Google Fonts, e uma que o
membro baixa da fundição e guarda em `workspace/fontes/`). A família baixada só vira página de
verdade se três coisas saírem certas, e nenhuma delas se faz por leitura de texto:

  1. saber QUAL peso é cada arquivo. O nome do arquivo mente com frequência (uma família com
     nove pesos tem Book, Heavy e Ultra, que ninguém adivinha em CSS), então o peso sai do
     metadado do próprio arquivo (`usWeightClass` da tabela OS/2) quando o formato permite ler,
     e só cai pro nome quando não permite.
  2. declarar o `@font-face` de cada arquivo com o `format()` certo pra extensão, num bloco
     marcado — no design, apontando pros arquivos ao lado do HTML; no tema da Shopify,
     apontando pro asset.
  3. embutir a fonte em base64 quando o HTML precisa viajar sozinho, sem a pasta ao lado.
     Converter binário em base64 é trabalho de código.

Uso:
  python3 .claude/lib/design-presets/local_fonts.py scan workspace/fontes
  python3 .claude/lib/design-presets/local_fonts.py scan workspace/fontes --family "ABC Oracle" --format json
  python3 .claude/lib/design-presets/local_fonts.py css workspace/fontes --mode relative \
      --family "ABC Oracle" --weights 400,500,700
  python3 .claude/lib/design-presets/local_fonts.py css workspace/fontes --mode asset --family "ABC Oracle"
  python3 .claude/lib/design-presets/local_fonts.py css workspace/fontes --mode inline --family "ABC Oracle"
  python3 .claude/lib/design-presets/local_fonts.py copy workspace/fontes --family "ABC Oracle" \
      --weights 400,500,700 --to workspace/<slug>/page/design/assets/fonts

  scan   lista as famílias encontradas, com peso, estilo, formato e tamanho de cada arquivo
  css    imprime os `@font-face`. `--mode relative` aponta pros arquivos ao lado do HTML (o
         padrão do `design/page.html` da `page-design`, mesmo tratamento das imagens);
         `--mode asset` aponta pro asset do tema (pro `<head>` do `theme.liquid`, na
         `page-build`); `--mode inline` embute o arquivo em base64, pra quando o HTML precisa
         abrir sozinho, longe da pasta
  copy   copia pro destino só os arquivos dos pesos pedidos, já no formato preferido

  --family   filtra e nomeia a família (sem ela, o script agrupa pelo que achar nos arquivos)
  --weights  lista de pesos separados por vírgula; sem ela, entram todos os encontrados
  --style    normal | italic | all (default all)
  --prefix   no modo relative, o caminho da pasta das fontes a partir do HTML (default
             `assets/fonts`)
  --format   md (default) ou json, no `scan`
  --out      salva a saída no caminho em vez de imprimir

Preferência de formato, quando o mesmo peso existe em mais de um arquivo: woff2, woff, otf, ttf.
O woff2 é o que carrega mais rápido; os outros funcionam, declarados com o `format()` certo.

Só biblioteca padrão. Exit 0 = tudo certo; 1 = pasta ausente, nenhuma fonte encontrada ou peso
pedido que não existe; 2 = uso incorreto (argparse).
"""
import argparse
import base64
import json
import re
import shutil
import struct
import sys
import zlib
from pathlib import Path

# ---------------------------------------------------------------- constantes

EXT_FORMAT = {
    ".woff2": "woff2",
    ".woff": "woff",
    ".otf": "opentype",
    ".ttf": "truetype",
}
EXT_MIME = {
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".otf": "font/otf",
    ".ttf": "font/ttf",
}
# menor índice = preferido quando o mesmo peso aparece em mais de um formato
EXT_RANK = {".woff2": 0, ".woff": 1, ".otf": 2, ".ttf": 3}

# Apelidos de peso, do mais longo pro mais curto (o match é por substring: procurar
# "ultralight" antes de "ultra" e "semibold" antes de "bold" é o que evita peso trocado).
WEIGHT_TOKENS = [
    ("ultrablack", 950),
    ("extrablack", 950),
    ("ultralight", 200),
    ("extralight", 200),
    ("semilight", 300),
    ("ultrabold", 800),
    ("extrabold", 800),
    ("demibold", 600),
    ("semibold", 600),
    ("hairline", 100),
    ("regular", 400),
    ("medium", 500),
    ("normal", 400),
    ("black", 900),
    ("light", 300),
    ("heavy", 800),
    ("roman", 400),
    ("ultra", 950),
    ("thin", 100),
    ("bold", 700),
    ("book", 350),
    ("text", 400),
]
STYLE_TOKENS = ("italic", "oblique", "kursiv")
VARIABLE_TOKENS = ("variable", "vf")
NAME_TOKENS = {token for token, _ in WEIGHT_TOKENS} | set(STYLE_TOKENS) | set(VARIABLE_TOKENS)

DEFAULT_STACK_TAIL = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
INLINE_BUDGET_BYTES = 1_500_000


# ---------------------------------------------------------------- leitura de SFNT

def _read_sfnt_tables(blob):
    """Mapa {tag: bytes} de um arquivo SFNT cru (.ttf/.otf). None se não for SFNT."""
    if len(blob) < 12:
        return None
    tag = blob[:4]
    if tag not in (b"\x00\x01\x00\x00", b"OTTO", b"true", b"typ1"):
        return None
    (num_tables,) = struct.unpack(">H", blob[4:6])
    tables = {}
    for i in range(num_tables):
        base = 12 + i * 16
        if base + 16 > len(blob):
            break
        name = blob[base:base + 4].decode("latin-1")
        offset, length = struct.unpack(">II", blob[base + 8:base + 16])
        if offset + length <= len(blob):
            tables[name] = blob[offset:offset + length]
    return tables or None


def _read_woff_tables(blob):
    """Mapa {tag: bytes} de um .woff (WOFF 1, compressão zlib da stdlib). None se não for WOFF."""
    if len(blob) < 44 or blob[:4] != b"wOFF":
        return None
    (num_tables,) = struct.unpack(">H", blob[12:14])
    tables = {}
    for i in range(num_tables):
        base = 44 + i * 20
        if base + 20 > len(blob):
            break
        name = blob[base:base + 4].decode("latin-1")
        offset, comp_len, orig_len = struct.unpack(">III", blob[base + 4:base + 16])
        chunk = blob[offset:offset + comp_len]
        if comp_len < orig_len:
            try:
                chunk = zlib.decompress(chunk)
            except zlib.error:
                continue
        tables[name] = chunk
    return tables or None


def read_font_tables(path):
    """Tabelas do arquivo, quando o formato permite ler sem dependência externa.

    `.woff2` usa Brotli, que não vem na biblioteca padrão: pra ele o retorno é None e os dados
    saem do irmão de mesmo nome em outro formato, ou do nome do arquivo.
    """
    try:
        blob = Path(path).read_bytes()
    except OSError:
        return None
    return _read_sfnt_tables(blob) or _read_woff_tables(blob)


def _decode_name_record(raw, platform_id):
    if platform_id == 3:  # Windows: UTF-16BE
        try:
            return raw.decode("utf-16-be").strip()
        except UnicodeDecodeError:
            return ""
    try:
        return raw.decode("mac-roman").strip()
    except (UnicodeDecodeError, LookupError):
        return raw.decode("latin-1").strip()


def parse_name_table(table):
    """{name_id: texto} da tabela `name`, preferindo o registro Windows."""
    if not table or len(table) < 6:
        return {}
    count, string_offset = struct.unpack(">HH", table[2:6])
    found = {}
    for i in range(count):
        base = 6 + i * 12
        if base + 12 > len(table):
            break
        platform_id, _, _, name_id, length, offset = struct.unpack(">HHHHHH", table[base:base + 12])
        start = string_offset + offset
        raw = table[start:start + length]
        if not raw:
            continue
        text = _decode_name_record(raw, platform_id)
        if not text:
            continue
        # o registro Windows sobrescreve o Mac; o primeiro de cada plataforma vence
        if name_id not in found or platform_id == 3:
            found[name_id] = text
    return found


def parse_os2_weight(table):
    if not table or len(table) < 6:
        return None
    (weight,) = struct.unpack(">H", table[4:6])
    return weight if 1 <= weight <= 1000 else None


def parse_italic(tables):
    os2 = tables.get("OS/2")
    if os2 and len(os2) >= 64:
        (fs_selection,) = struct.unpack(">H", os2[62:64])
        if fs_selection & 0x01:
            return True
    head = tables.get("head")
    if head and len(head) >= 46:
        (mac_style,) = struct.unpack(">H", head[44:46])
        if mac_style & 0x02:
            return True
    return False


def parse_weight_axis(tables):
    """(min, max) do eixo `wght` quando o arquivo é variável; None quando não é."""
    fvar = tables.get("fvar")
    if not fvar or len(fvar) < 16:
        return None
    axes_offset, _, axis_count, axis_size = struct.unpack(">HHHH", fvar[4:12])
    for i in range(axis_count):
        base = axes_offset + i * axis_size
        if base + 20 > len(fvar):
            break
        tag = fvar[base:base + 4].decode("latin-1")
        if tag == "wght":
            min_v, _, max_v = struct.unpack(">iii", fvar[base + 4:base + 16])
            return (max(1, min_v >> 16), min(1000, max_v >> 16))
    return None


# ---------------------------------------------------------------- dedução por nome

def _normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def humanize_family(raw):
    """`ABCOracle` → `ABC Oracle`; `geist_sans` → `Geist Sans`.

    Palavra escrita toda em minúsculas ganha inicial maiúscula; palavra que já tem maiúscula
    fica como está, pra sigla de fundição (`ABC`) não virar `Abc`.
    """
    text = re.sub(r"[_\-.]+", " ", raw).strip()
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", text)
    words = [word.capitalize() if word.islower() else word for word in text.split()]
    return " ".join(words) or raw


def weight_from_name(stem):
    flat = _normalize(stem)
    for token, value in WEIGHT_TOKENS:
        if token in flat:
            return value
    return 400


def style_from_name(stem):
    flat = _normalize(stem)
    return "italic" if any(token in flat for token in STYLE_TOKENS) else "normal"


def variable_from_name(stem):
    if "variable" in _normalize(stem):
        return True
    return bool(re.search(r"(^|[^a-z])vf([^a-z]|$)", stem.lower()))


def _is_style_word(word):
    flat = _normalize(word)
    return any(token in flat for token in NAME_TOKENS)


def family_from_name(stem):
    """Tira do nome do arquivo os apelidos de peso e de estilo; o que sobra é a família.

    Com separador (`ABCOracle-SemiBold`, `geist_mono_regular`), saem os segmentos que são
    apelido e ficam os outros — é o que preserva `Geist Mono` como família própria. Sem
    separador (`GeistVariable`), a quebra é por camelCase e o filtro roda palavra a palavra.
    """
    segments = [part for part in re.split(r"[-_.\s]+", stem) if part]
    if not segments:
        return stem
    kept = [part for part in segments if not _is_style_word(part)] or segments[:1]
    if len(segments) > 1:
        return " ".join(humanize_family(part) for part in kept)
    words = humanize_family(kept[0]).split()
    return " ".join([word for word in words if not _is_style_word(word)] or words)


# ---------------------------------------------------------------- inventário

def describe_file(path, sibling_tables=None):
    """Descreve um arquivo de fonte: família, peso, estilo, formato, tamanho e de onde veio o dado."""
    path = Path(path)
    ext = path.suffix.lower()
    stem = path.stem
    entry = {
        "file": path.name,
        "path": str(path),
        "ext": ext.lstrip("."),
        "format": EXT_FORMAT.get(ext, ""),
        "bytes": path.stat().st_size if path.exists() else 0,
        "weight": weight_from_name(stem),
        "style": style_from_name(stem),
        "family": family_from_name(stem),
        "variable": False,
        "weight_range": None,
        "source": "filename",
    }
    tables = read_font_tables(path) or sibling_tables
    if tables:
        weight = parse_os2_weight(tables.get("OS/2"))
        names = parse_name_table(tables.get("name"))
        family = names.get(16) or names.get(1)
        axis = parse_weight_axis(tables)
        if weight:
            entry["weight"] = weight
        if family:
            entry["family"] = family.strip()
        entry["style"] = "italic" if parse_italic(tables) else entry["style"]
        if axis:
            entry["variable"] = True
            entry["weight_range"] = list(axis)
        if weight or family:
            entry["source"] = "metadata"
    if not entry["variable"] and variable_from_name(stem):
        entry["variable"] = True
        entry["weight_range"] = entry["weight_range"] or [100, 900]
    return entry


def _sibling_tables(path):
    """Tabelas de um irmão legível de mesmo nome (o `.woff2` empresta do `.otf` ao lado)."""
    path = Path(path)
    for ext in (".otf", ".ttf", ".woff"):
        candidate = path.with_suffix(ext)
        if candidate.exists():
            tables = read_font_tables(candidate)
            if tables:
                return tables
    return None


def scan_dir(directory, family=None):
    directory = Path(directory)
    if not directory.is_dir():
        raise FileNotFoundError(f"pasta não encontrada: {directory}")

    files = sorted(
        (p for p in directory.rglob("*") if p.suffix.lower() in EXT_FORMAT and p.is_file()),
        key=lambda p: (str(p.parent), p.name),
    )
    entries = []
    for path in files:
        tables = None
        if path.suffix.lower() == ".woff2":
            tables = _sibling_tables(path)
        entries.append(describe_file(path, sibling_tables=tables))

    groups = {}
    for entry in entries:
        groups.setdefault(_normalize(entry["family"]), []).append(entry)

    families = [_build_family(items[0]["family"], items) for items in groups.values()]
    if family:
        wanted = _normalize(family)
        match = [fam for fam in families if _normalize(fam["family"]) == wanted]
        if match:
            families = match
        elif len(groups) == 1:
            # a pasta tem uma família só e o nome do arquivo a escreve de outro jeito:
            # o nome que o membro declarou vence
            families = [_build_family(family, next(iter(groups.values())))]
    families.sort(key=lambda f: f["family"].lower())
    warnings = []
    for fam in families:
        if not fam["has_woff2"]:
            warnings.append(
                f"{fam['family']}: nenhum arquivo .woff2 na pasta. "
                "Os formatos presentes funcionam; o .woff2 carrega mais rápido, quando a fundição oferece."
            )
        guessed = [f["file"] for f in fam["files"] if f["source"] == "filename"]
        if guessed:
            warnings.append(
                f"{fam['family']}: peso lido pelo nome do arquivo em {len(guessed)} arquivo(s) "
                f"({', '.join(guessed[:3])}{'...' if len(guessed) > 3 else ''})."
            )
    return {
        "version": 1,
        "dir": str(directory),
        "families": families,
        "warnings": warnings,
    }


def _build_family(name, items):
    chosen = {}
    for item in items:
        key = (item["weight"], item["style"])
        current = chosen.get(key)
        rank = EXT_RANK.get(f".{item['ext']}", 9)
        if current is None or rank < EXT_RANK.get(f".{current['ext']}", 9):
            chosen[key] = item
    files = sorted(items, key=lambda e: (e["style"], e["weight"], EXT_RANK.get(f".{e['ext']}", 9)))
    preferred = [chosen[key] for key in sorted(chosen)]
    weights = sorted({item["weight"] for item in items})
    styles = sorted({item["style"] for item in items})
    return {
        "family": name,
        "files": files,
        "preferred": preferred,
        "weights": weights,
        "styles": styles,
        "has_woff2": any(item["ext"] == "woff2" for item in items),
        "variable": any(item["variable"] for item in items),
        "bytes_preferred": sum(item["bytes"] for item in preferred),
        "stack": f"'{name}', {DEFAULT_STACK_TAIL}",
    }


# ---------------------------------------------------------------- seleção

def select_files(fam, weights=None, style="all"):
    picked = fam["preferred"]
    if style in ("normal", "italic"):
        picked = [item for item in picked if item["style"] == style]
    if weights:
        wanted = set(weights)
        variable = [item for item in picked if item["variable"]]
        if variable:
            picked = variable
        else:
            picked = [item for item in picked if item["weight"] in wanted]
    return picked


# ---------------------------------------------------------------- saída CSS

def _face_block(item, family, src):
    if item["variable"] and item["weight_range"]:
        weight = f"{item['weight_range'][0]} {item['weight_range'][1]}"
    else:
        weight = str(item["weight"])
    return (
        "@font-face{"
        f"font-family:'{family}';"
        f"font-style:{item['style']};"
        f"font-weight:{weight};"
        "font-display:swap;"
        f"src:{src};"
        "}"
    )


def css_relative(fam, items, prefix="assets/fonts"):
    """`@font-face` apontando pros arquivos ao lado do HTML. É o padrão do `design/page.html`:
    o mesmo tratamento que as imagens da página já têm."""
    prefix = prefix.strip("/")
    lines = []
    for item in items:
        ext = f".{item['ext']}"
        caminho = f"{prefix}/{item['file']}" if prefix else item["file"]
        src = f"url({caminho}) format('{EXT_FORMAT[ext]}')"
        lines.append(_face_block(item, fam["family"], src))
    body = "\n".join(lines)
    return f'<style data-aura-fonts="{fam["family"]}">\n{body}\n</style>'


def css_inline(fam, items):
    """`@font-face` com o arquivo embutido em base64, pra quando o HTML precisa abrir sozinho,
    longe da pasta de assets."""
    lines = []
    for item in items:
        ext = f".{item['ext']}"
        data = base64.b64encode(Path(item["path"]).read_bytes()).decode("ascii")
        src = f"url(data:{EXT_MIME[ext]};base64,{data}) format('{EXT_FORMAT[ext]}')"
        lines.append(_face_block(item, fam["family"], src))
    body = "\n".join(lines)
    return f'<style data-aura-fonts="{fam["family"]}">\n{body}\n</style>'


def css_asset(fam, items):
    """`@font-face` apontando pro asset do tema. Vai no `<head>` do `theme.liquid`, onde o
    Liquid é processado (dentro de `{% stylesheet %}` de section ele sairia literal)."""
    lines = []
    for item in items:
        ext = f".{item['ext']}"
        src = f"url({{{{ '{item['file']}' | asset_url }}}}) format('{EXT_FORMAT[ext]}')"
        lines.append(_face_block(item, fam["family"], src))
    body = "\n".join(lines)
    return f"<style>\n{body}\n</style>"


# ---------------------------------------------------------------- saída md

def render_md(report):
    out = [f"# Fontes em `{report['dir']}`", ""]
    if not report["families"]:
        out.append("Nenhum arquivo de fonte encontrado (`.woff2`, `.woff`, `.otf`, `.ttf`).")
        return "\n".join(out)
    for fam in report["families"]:
        out.append(f"## {fam['family']}")
        out.append("")
        out.append(f"Stack: `{fam['stack']}`")
        pesos = ", ".join(str(w) for w in fam["weights"])
        out.append(f"Pesos: {pesos} · estilos: {', '.join(fam['styles'])}")
        if fam["variable"]:
            out.append("Arquivo variável: um arquivo cobre a faixa inteira de peso.")
        out.append("")
        out.append("| Arquivo | Peso | Estilo | Formato | KB | Peso lido de |")
        out.append("|---|---|---|---|---|---|")
        for item in fam["files"]:
            out.append(
                f"| `{item['file']}` | {item['weight']} | {item['style']} | {item['ext']} | "
                f"{item['bytes'] / 1024:.0f} | {'metadado' if item['source'] == 'metadata' else 'nome do arquivo'} |"
            )
        out.append("")
        out.append(f"Selecionados pra página: {len(fam['preferred'])} arquivo(s), "
                   f"{fam['bytes_preferred'] / 1024:.0f} KB.")
        out.append("")
    if report["warnings"]:
        out.append("## Pontos de atenção")
        out.append("")
        for warning in report["warnings"]:
            out.append(f"- {warning}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------- CLI

def _pick_family(report, family):
    if not report["families"]:
        raise ValueError(f"nenhum arquivo de fonte em {report['dir']}")
    if family:
        for fam in report["families"]:
            if _normalize(fam["family"]) == _normalize(family):
                return fam
        nomes = ", ".join(f["family"] for f in report["families"])
        raise ValueError(f"família '{family}' não encontrada. Encontradas: {nomes}")
    if len(report["families"]) > 1:
        nomes = ", ".join(f["family"] for f in report["families"])
        raise ValueError(f"mais de uma família na pasta ({nomes}); use --family")
    return report["families"][0]


def _parse_weights(raw):
    if not raw:
        return None
    try:
        return [int(part) for part in raw.split(",") if part.strip()]
    except ValueError:
        raise ValueError(f"lista de pesos inválida: {raw}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Inventário e provisionamento de fontes que o membro baixou.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="lista as famílias e os arquivos encontrados")
    p_scan.add_argument("dir")
    p_scan.add_argument("--family")
    p_scan.add_argument("--format", choices=["md", "json"], default="md")
    p_scan.add_argument("--out")

    p_css = sub.add_parser("css", help="imprime os @font-face")
    p_css.add_argument("dir")
    p_css.add_argument("--mode", choices=["relative", "asset", "inline"], required=True)
    p_css.add_argument("--family")
    p_css.add_argument("--weights")
    p_css.add_argument("--style", choices=["normal", "italic", "all"], default="all")
    p_css.add_argument("--prefix", default="assets/fonts")
    p_css.add_argument("--out")

    p_copy = sub.add_parser("copy", help="copia os arquivos escolhidos pro destino")
    p_copy.add_argument("dir")
    p_copy.add_argument("--to", required=True)
    p_copy.add_argument("--family")
    p_copy.add_argument("--weights")
    p_copy.add_argument("--style", choices=["normal", "italic", "all"], default="all")

    args = parser.parse_args(argv)

    try:
        report = scan_dir(args.dir, family=getattr(args, "family", None))
    except FileNotFoundError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1

    if args.command == "scan":
        payload = json.dumps(report, ensure_ascii=False, indent=2) if args.format == "json" else render_md(report)
        if args.out:
            Path(args.out).write_text(payload + ("\n" if args.format == "json" else ""), encoding="utf-8")
            print(f"salvo em {args.out}")
        else:
            print(payload)
        return 0 if report["families"] else 1

    try:
        fam = _pick_family(report, args.family)
        weights = _parse_weights(args.weights)
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1

    items = select_files(fam, weights=weights, style=args.style)
    if not items:
        print(
            f"erro: nenhum arquivo de {fam['family']} com os pesos pedidos "
            f"({args.weights}); disponíveis: {', '.join(str(w) for w in fam['weights'])}",
            file=sys.stderr,
        )
        return 1

    if args.command == "css":
        if args.mode == "inline":
            payload = css_inline(fam, items)
        elif args.mode == "asset":
            payload = css_asset(fam, items)
        else:
            payload = css_relative(fam, items, prefix=args.prefix)
        total = sum(item["bytes"] for item in items)
        if args.mode == "inline" and total > INLINE_BUDGET_BYTES:
            print(
                f"atenção: {total / 1024:.0f} KB de fonte embutida. "
                "Reduza os pesos com --weights pra deixar o arquivo de design leve.",
                file=sys.stderr,
            )
        if args.out:
            Path(args.out).write_text(payload + "\n", encoding="utf-8")
            print(f"salvo em {args.out} ({len(items)} face(s), {total / 1024:.0f} KB de fonte)")
        else:
            print(payload)
        return 0

    destino = Path(args.to)
    destino.mkdir(parents=True, exist_ok=True)
    for item in items:
        shutil.copy2(item["path"], destino / item["file"])
    total = sum(item["bytes"] for item in items)
    print(f"{len(items)} arquivo(s) copiado(s) pra {destino} ({total / 1024:.0f} KB)")
    for item in items:
        print(f"  {item['file']} · peso {item['weight']} · {item['style']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
