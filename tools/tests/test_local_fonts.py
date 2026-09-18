#!/usr/bin/env python3
"""
Testes do inventário de fontes locais `.claude/lib/design-presets/local_fonts.py`.

Os arquivos de fonte dos testes são SFNT sintéticos montados byte a byte (tabelas `OS/2`,
`head`, `name` e `fvar`): nenhum binário de fonte entra no repositório, e o teste consegue
declarar exatamente o metadado que quer conferir.
"""
import base64
import importlib.util
import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / ".claude" / "lib" / "design-presets"
SCRIPT = LIB / "local_fonts.py"

spec = importlib.util.spec_from_file_location("local_fonts", SCRIPT)
lf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lf)


# ---------------------------------------------------------------- SFNT sintético

def _os2_table(weight, italic=False):
    table = bytearray(78)
    struct.pack_into(">H", table, 0, 4)          # version
    struct.pack_into(">H", table, 2, 500)        # xAvgCharWidth
    struct.pack_into(">H", table, 4, weight)     # usWeightClass
    struct.pack_into(">H", table, 6, 5)          # usWidthClass
    struct.pack_into(">H", table, 62, 0x01 if italic else 0x40)  # fsSelection
    return bytes(table)


def _head_table(italic=False):
    table = bytearray(54)
    struct.pack_into(">H", table, 44, 0x02 if italic else 0x00)  # macStyle
    return bytes(table)


def _name_table(records):
    """records: lista de (name_id, texto), gravados como registro Windows (UTF-16BE)."""
    header = struct.pack(">HHH", 0, len(records), 6 + 12 * len(records))
    entries, strings = b"", b""
    for name_id, text in records:
        raw = text.encode("utf-16-be")
        entries += struct.pack(">HHHHHH", 3, 1, 0x0409, name_id, len(raw), len(strings))
        strings += raw
    return header + entries + strings


def _fvar_table(axis_min=100, axis_max=900):
    header = struct.pack(">HHHHHHHH", 1, 0, 16, 0, 1, 20, 0, 0)
    axis = b"wght" + struct.pack(">iii", axis_min << 16, 400 << 16, axis_max << 16)
    axis += struct.pack(">HH", 0, 256)
    return header + axis


def build_sfnt(tables, flavor=b"\x00\x01\x00\x00"):
    names = sorted(tables)
    header = struct.pack(">4sHHHH", flavor, len(names), 0, 0, 0)
    offset = 12 + 16 * len(names)
    records, body = b"", b""
    for name in names:
        data = tables[name]
        padded = data + b"\x00" * (-len(data) % 4)
        records += struct.pack(">4sII I".replace(" ", ""), name.encode("latin-1").ljust(4), 0, offset, len(data))
        body += padded
        offset += len(padded)
    return header + records + body


def build_woff(tables):
    names = sorted(tables)
    dir_size = 20 * len(names)
    offset = 44 + dir_size
    directory, body = b"", b""
    for name in names:
        data = tables[name]
        comp = zlib.compress(data)
        if len(comp) >= len(data):
            comp = data
        padded = comp + b"\x00" * (-len(comp) % 4)
        directory += struct.pack(">4sIIII", name.encode("latin-1").ljust(4), offset, len(comp), len(data), 0)
        body += padded
        offset += len(padded)
    header = struct.pack(
        ">4sIIHHIHHIIIII",
        b"wOFF", 0x00010000, 44 + dir_size + len(body), len(names), 0,
        12 + 16 * len(names) + sum(len(t) for t in tables.values()),
        1, 0, 0, 0, 0, 0, 0,
    )
    return header + directory + body


def write_font(directory, filename, weight=400, family="Test Family", italic=False,
               variable=False, with_metadata=True, woff=False):
    path = Path(directory) / filename
    if not with_metadata:
        path.write_bytes(b"wOF2" + b"\x00" * 64)  # woff2: comprimido com Brotli, ilegível aqui
        return path
    tables = {
        "OS/2": _os2_table(weight, italic=italic),
        "head": _head_table(italic=italic),
        "name": _name_table([(1, family), (16, family), (2, "Regular")]),
    }
    if variable:
        tables["fvar"] = _fvar_table()
    blob = build_woff(tables) if woff else build_sfnt(tables)
    path.write_bytes(blob)
    return path


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, cwd=str(ROOT)
    )


# ---------------------------------------------------------------- leitura de metadado

class LeituraDeMetadado(unittest.TestCase):
    def test_peso_do_metadado_vence_o_nome_do_arquivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            # o arquivo se chama Regular, mas o metadado diz 700
            write_font(tmp, "ABCOracle-Regular.otf", weight=700, family="ABC Oracle")
            report = lf.scan_dir(tmp)
            item = report["families"][0]["files"][0]
            self.assertEqual(item["weight"], 700)
            self.assertEqual(item["source"], "metadata")

    def test_familia_vem_do_metadado(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "arquivo-sem-pista.otf", weight=400, family="ABC Oracle")
            report = lf.scan_dir(tmp)
            self.assertEqual(report["families"][0]["family"], "ABC Oracle")

    def test_italico_pelo_fsselection(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "Familia-Qualquer.otf", weight=400, italic=True)
            report = lf.scan_dir(tmp)
            self.assertEqual(report["families"][0]["files"][0]["style"], "italic")

    def test_woff_comprimido_com_zlib_e_legivel(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Qualquer.woff", weight=500, family="ABC Oracle", woff=True)
            report = lf.scan_dir(tmp)
            item = report["families"][0]["files"][0]
            self.assertEqual(item["weight"], 500)
            self.assertEqual(item["source"], "metadata")

    def test_woff2_sem_irmao_cai_pro_nome_do_arquivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-SemiBold.woff2", with_metadata=False)
            report = lf.scan_dir(tmp)
            item = report["families"][0]["files"][0]
            self.assertEqual(item["weight"], 600)
            self.assertEqual(item["source"], "filename")
            self.assertTrue(any("nome do arquivo" in w for w in report["warnings"]))

    def test_woff2_pega_o_metadado_do_irmao_de_mesmo_nome(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=350, family="ABC Oracle")
            write_font(tmp, "ABCOracle-Regular.woff2", with_metadata=False)
            report = lf.scan_dir(tmp)
            woff2 = [f for f in report["families"][0]["files"] if f["ext"] == "woff2"][0]
            self.assertEqual(woff2["weight"], 350)
            self.assertEqual(woff2["source"], "metadata")

    def test_variavel_declara_a_faixa_do_eixo_wght(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "Geist-Variable.ttf", weight=400, family="Geist", variable=True)
            report = lf.scan_dir(tmp)
            item = report["families"][0]["files"][0]
            self.assertTrue(item["variable"])
            self.assertEqual(item["weight_range"], [100, 900])


# ---------------------------------------------------------------- dedução por nome

class DeducaoPorNome(unittest.TestCase):
    def test_apelidos_de_peso(self):
        casos = {
            "X-Thin": 100, "X-UltraLight": 200, "X-Light": 300, "X-Book": 350,
            "X-Regular": 400, "X-Medium": 500, "X-SemiBold": 600, "X-DemiBold": 600,
            "X-Bold": 700, "X-ExtraBold": 800, "X-Heavy": 800, "X-Black": 900, "X-Ultra": 950,
        }
        for stem, esperado in casos.items():
            with self.subTest(stem=stem):
                self.assertEqual(lf.weight_from_name(stem), esperado)

    def test_semibold_nunca_e_lido_como_bold(self):
        # o apelido longo tem que ser testado antes do curto, senão 600 vira 700
        self.assertEqual(lf.weight_from_name("ABCOracle-SemiBold"), 600)
        self.assertEqual(lf.weight_from_name("ABCOracle-ExtraBold"), 800)
        self.assertEqual(lf.weight_from_name("ABCOracle-UltraLight"), 200)

    def test_sem_apelido_nenhum_o_peso_e_400(self):
        self.assertEqual(lf.weight_from_name("ABCOracle"), 400)

    def test_italico_pelo_nome(self):
        self.assertEqual(lf.style_from_name("ABCOracle-BoldItalic"), "italic")
        self.assertEqual(lf.style_from_name("ABCOracle-Bold"), "normal")

    def test_familia_pelo_nome_do_arquivo(self):
        self.assertEqual(lf.family_from_name("ABCOracle-SemiBold"), "ABC Oracle")
        self.assertEqual(lf.family_from_name("GeistVariable"), "Geist")
        self.assertEqual(lf.family_from_name("geist_mono_regular"), "Geist Mono")
        self.assertEqual(lf.family_from_name("ABCOracle-BoldItalic"), "ABC Oracle")

    def test_humanize_separa_camelcase_preservando_sigla(self):
        self.assertEqual(lf.humanize_family("ABCOracle"), "ABC Oracle")
        self.assertEqual(lf.humanize_family("GeistMono"), "Geist Mono")


# ---------------------------------------------------------------- inventário

class Inventario(unittest.TestCase):
    def test_duas_familias_na_mesma_pasta_viram_duas_entradas(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            write_font(tmp, "Geist-Regular.otf", weight=400, family="Geist")
            report = lf.scan_dir(tmp)
            self.assertEqual([f["family"] for f in report["families"]], ["ABC Oracle", "Geist"])

    def test_subpasta_entra_no_inventario(self):
        with tempfile.TemporaryDirectory() as tmp:
            sub = Path(tmp) / "abc-oracle" / "web"
            sub.mkdir(parents=True)
            write_font(sub, "ABCOracle-Bold.otf", weight=700, family="ABC Oracle")
            report = lf.scan_dir(tmp)
            self.assertEqual(report["families"][0]["weights"], [700])

    def test_mesmo_peso_em_dois_formatos_prefere_woff2(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            write_font(tmp, "ABCOracle-Regular.woff2", with_metadata=False)
            fam = lf.scan_dir(tmp)["families"][0]
            self.assertEqual(len(fam["files"]), 2)
            self.assertEqual(len(fam["preferred"]), 1)
            self.assertEqual(fam["preferred"][0]["ext"], "woff2")

    def test_aviso_quando_nao_ha_woff2(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            report = lf.scan_dir(tmp)
            self.assertTrue(any(".woff2" in w for w in report["warnings"]))

    def test_family_declarada_renomeia_a_unica_familia_da_pasta(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "oracle_web_400.otf", weight=400, family="oracle_web_400")
            report = lf.scan_dir(tmp, family="ABC Oracle")
            self.assertEqual(report["families"][0]["family"], "ABC Oracle")
            self.assertIn("'ABC Oracle'", report["families"][0]["stack"])

    def test_family_declarada_filtra_quando_ha_varias(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            write_font(tmp, "Geist-Regular.otf", weight=400, family="Geist")
            report = lf.scan_dir(tmp, family="Geist")
            self.assertEqual([f["family"] for f in report["families"]], ["Geist"])

    def test_pasta_sem_fonte_nenhuma(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "leiame.txt").write_text("nada aqui", encoding="utf-8")
            self.assertEqual(lf.scan_dir(tmp)["families"], [])

    def test_pasta_ausente_levanta(self):
        with self.assertRaises(FileNotFoundError):
            lf.scan_dir("/caminho/que/nao/existe/fontes")


# ---------------------------------------------------------------- seleção e CSS

class SelecaoEcss(unittest.TestCase):
    def _familia(self, tmp):
        for nome, peso in (("ABCOracle-Regular.otf", 400), ("ABCOracle-Medium.otf", 500),
                           ("ABCOracle-Bold.otf", 700)):
            write_font(tmp, nome, weight=peso, family="ABC Oracle")
        return lf.scan_dir(tmp)["families"][0]

    def test_selecao_por_peso(self):
        with tempfile.TemporaryDirectory() as tmp:
            fam = self._familia(tmp)
            escolhidos = lf.select_files(fam, weights=[400, 700])
            self.assertEqual([i["weight"] for i in escolhidos], [400, 700])

    def test_selecao_de_variavel_ignora_a_lista_de_pesos(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "Geist-Variable.ttf", weight=400, family="Geist", variable=True)
            fam = lf.scan_dir(tmp)["families"][0]
            escolhidos = lf.select_files(fam, weights=[600])
            self.assertEqual(len(escolhidos), 1)
            self.assertTrue(escolhidos[0]["variable"])

    def test_relative_aponta_pros_arquivos_ao_lado_do_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            fam = self._familia(tmp)
            css = lf.css_relative(fam, lf.select_files(fam, weights=[500]))
            self.assertIn('data-aura-fonts="ABC Oracle"', css)
            self.assertIn("url(assets/fonts/ABCOracle-Medium.otf)", css)
            self.assertNotIn("base64", css)

    def test_relative_aceita_outro_prefixo_e_o_prefixo_vazio(self):
        with tempfile.TemporaryDirectory() as tmp:
            fam = self._familia(tmp)
            itens = lf.select_files(fam, weights=[400])
            self.assertIn("url(fonts/ABCOracle-Regular.otf)",
                          lf.css_relative(fam, itens, prefix="fonts/"))
            self.assertIn("url(ABCOracle-Regular.otf)", lf.css_relative(fam, itens, prefix=""))

    def test_inline_embute_o_arquivo_em_base64(self):
        with tempfile.TemporaryDirectory() as tmp:
            fam = self._familia(tmp)
            item = lf.select_files(fam, weights=[400])
            css = lf.css_inline(fam, item)
            self.assertIn('data-aura-fonts="ABC Oracle"', css)
            self.assertIn("font-weight:400", css)
            self.assertIn("format('opentype')", css)
            payload = css.split("base64,")[1].split(")")[0]
            self.assertEqual(base64.b64decode(payload), Path(item[0]["path"]).read_bytes())

    def test_asset_aponta_pro_asset_url_do_tema(self):
        with tempfile.TemporaryDirectory() as tmp:
            fam = self._familia(tmp)
            css = lf.css_asset(fam, lf.select_files(fam, weights=[700]))
            self.assertIn("{{ 'ABCOracle-Bold.otf' | asset_url }}", css)
            self.assertIn("font-weight:700", css)
            self.assertNotIn("base64", css)

    def test_face_de_variavel_declara_a_faixa_inteira(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "Geist-Variable.ttf", weight=400, family="Geist", variable=True)
            fam = lf.scan_dir(tmp)["families"][0]
            css = lf.css_asset(fam, lf.select_files(fam))
            self.assertIn("font-weight:100 900", css)

    def test_todo_face_pede_font_display_swap(self):
        with tempfile.TemporaryDirectory() as tmp:
            fam = self._familia(tmp)
            css = lf.css_asset(fam, lf.select_files(fam))
            self.assertEqual(css.count("font-display:swap"), 3)


# ---------------------------------------------------------------- CLI

class Cli(unittest.TestCase):
    def test_scan_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Bold.otf", weight=700, family="ABC Oracle")
            proc = run_cli("scan", tmp, "--format", "json")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            self.assertEqual(data["families"][0]["weights"], [700])

    def test_scan_md_lista_o_arquivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Bold.otf", weight=700, family="ABC Oracle")
            proc = run_cli("scan", tmp)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("ABCOracle-Bold.otf", proc.stdout)
            self.assertIn("ABC Oracle", proc.stdout)

    def test_scan_de_pasta_vazia_sai_com_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run_cli("scan", tmp).returncode, 1)

    def test_pasta_ausente_sai_com_1(self):
        proc = run_cli("scan", "/caminho/que/nao/existe")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("pasta não encontrada", proc.stderr)

    def test_css_relative_pela_linha_de_comando(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            proc = run_cli("css", tmp, "--mode", "relative")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("url(assets/fonts/ABCOracle-Regular.otf)", proc.stdout)

    def test_modo_de_css_desconhecido_sai_com_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            self.assertEqual(run_cli("css", tmp, "--mode", "data-uri").returncode, 2)

    def test_peso_inexistente_sai_com_1_e_lista_os_disponiveis(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            proc = run_cli("css", tmp, "--mode", "asset", "--weights", "900")
            self.assertEqual(proc.returncode, 1)
            self.assertIn("400", proc.stderr)

    def test_duas_familias_sem_family_pede_o_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_font(tmp, "ABCOracle-Regular.otf", weight=400, family="ABC Oracle")
            write_font(tmp, "Geist-Regular.otf", weight=400, family="Geist")
            proc = run_cli("css", tmp, "--mode", "asset")
            self.assertEqual(proc.returncode, 1)
            self.assertIn("--family", proc.stderr)

    def test_copy_leva_so_os_pesos_pedidos(self):
        with tempfile.TemporaryDirectory() as tmp:
            for nome, peso in (("ABCOracle-Regular.otf", 400), ("ABCOracle-Bold.otf", 700),
                               ("ABCOracle-Black.otf", 900)):
                write_font(tmp, nome, weight=peso, family="ABC Oracle")
            destino = Path(tmp) / "destino"
            proc = run_cli("copy", tmp, "--to", str(destino), "--weights", "400,700")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            copiados = sorted(p.name for p in destino.iterdir())
            self.assertEqual(copiados, ["ABCOracle-Bold.otf", "ABCOracle-Regular.otf"])

    def test_uso_incorreto_sai_com_2(self):
        self.assertEqual(run_cli("modo-que-nao-existe", "/tmp").returncode, 2)


if __name__ == "__main__":
    unittest.main()
