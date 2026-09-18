#!/usr/bin/env python3
"""
Testes do gerador de paletas `.claude/lib/design-presets/palette_engine.py`.

Provam as duas metades do contrato: o que o gerador devolve passa sempre nos quatro testes
(saturação viva, harmonia declarada que bate com a distância real de matiz, contraste WCAG AA e
as 3 candidatas distintas entre si), e o validador REPROVA cada violação isolada — é o que
garante que nenhuma paleta sai com aviso em vez de sair corrigida.

Rodar da raiz do repositório:
  python3 -m unittest discover -s tools/tests
  python3 tools/tests/test_palette_engine.py

Só biblioteca padrão.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / ".claude" / "lib" / "design-presets"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))
import palette_engine as pe  # noqa: E402


def sample(vertical="supplements", **kwargs):
    return pe.generate(vertical, **kwargs)


def entry_with(base, **roles):
    """Cópia de uma candidata válida com um ou mais roles trocados."""
    out = copy.deepcopy(base)
    out["palette"].update(roles)
    return out


class Geracao(unittest.TestCase):
    """O que sai do gerador está sempre entregável."""

    def test_toda_vertical_devolve_tres_paletas_validas(self):
        for vertical in sorted(pe.VERTICALS):
            for skepticism in ("baixo", "médio", "alto"):
                with self.subTest(vertical=vertical, skepticism=skepticism):
                    result = pe.generate(vertical, skepticism=skepticism)
                    self.assertEqual(len(result["palettes"]), pe.PALETTE_COUNT)
                    self.assertEqual(pe.validate_set(result["palettes"]), [])
                    for entry in result["palettes"]:
                        self.assertEqual(pe.validate_palette(entry), [], entry["name"])
                        self.assertEqual(sorted(entry["palette"]), sorted(pe.ROLES))
                        self.assertTrue(entry["name"])
                        self.assertTrue(entry["why"].endswith("."))

    def test_varredura_de_entradas_reais_nao_produz_paleta_invalida(self):
        """O caso que só aparece na combinação: semente de marca perto de uma direção da vertical.
        Sem a folga do `_spread`, o matiz medido no hex já arredondado cai abaixo do piso."""
        sementes = ([], ["#9CAF88", "#14213D"], ["#FFD400"], ["#C66B3D"])
        for vertical in sorted(pe.VERTICALS):
            for skepticism in ("baixo", "alto"):
                for seeds in sementes:
                    for avatar in ("", "mulheres de 45 a 65 anos"):
                        with self.subTest(vertical=vertical, skepticism=skepticism, seeds=seeds, avatar=avatar):
                            result = pe.generate(vertical, avatar=avatar, skepticism=skepticism, seeds=seeds)
                            self.assertEqual(pe.validate_set(result["palettes"]), [])
                            for entry in result["palettes"]:
                                self.assertEqual(pe.validate_palette(entry), [], entry["name"])

    def test_tema_forcado_muda_o_fundo_de_verdade(self):
        escuro = pe.generate("health", theme="dark")
        claro = pe.generate("health", theme="light")
        for entry in escuro["palettes"]:
            self.assertLess(pe.hex_to_hsl(entry["palette"]["background"])[2], 0.5, entry["name"])
        for entry in claro["palettes"]:
            self.assertGreater(pe.hex_to_hsl(entry["palette"]["background"])[2], 0.5, entry["name"])

    def test_mesma_entrada_devolve_a_mesma_saida(self):
        a = pe.generate("beauty", avatar="mulheres de 45 a 65 anos", skepticism="alto")
        b = pe.generate("beauty", avatar="mulheres de 45 a 65 anos", skepticism="alto")
        self.assertEqual(json.dumps(a["palettes"], sort_keys=True), json.dumps(b["palettes"], sort_keys=True))

    def test_entradas_diferentes_nao_devolvem_sempre_o_mesmo(self):
        avatares = ("mulheres de 45 a 65 anos", "homens de 30 a 45 que treinam", "mães de primeira viagem", "corredores amadores")
        assinaturas = {json.dumps(pe.generate("home", avatar=a)["palettes"], sort_keys=True) for a in avatares}
        self.assertGreater(len(assinaturas), 1)

    def test_cor_da_marca_vira_a_primeira_candidata(self):
        semente = "#C66B3D"
        result = pe.generate("beauty", seeds=[semente])
        self.assertEqual(result["input"]["anchor"], semente)
        esperado = pe.hex_to_hsl(semente)[0]
        self.assertLess(pe.hue_delta(result["palettes"][0]["hue"]["primary"], esperado), 3.0)

    def test_semente_sem_cor_viva_nao_vira_ancora(self):
        result = pe.generate("beauty", seeds=["#F2F2F2"])
        self.assertNotEqual(result["palettes"][0]["hue"]["primary"], round(pe.hex_to_hsl("#F2F2F2")[0], 1))

    def test_tokens_que_nao_sao_de_cor_vem_literais_do_preset(self):
        presets = pe.load_presets()
        for entry in pe.generate("supplements")["palettes"]:
            preset = presets[entry["base_preset"]]
            for campo in ("heading_font", "body_font", "google_fonts", "radius", "shadow", "density"):
                self.assertEqual(entry["non_color_tokens"][campo], preset[campo], campo)

    def test_saida_css_traz_o_trio_rgb_de_cada_role(self):
        css = pe.render_css(pe.generate("other"))
        self.assertIn("--tk-primary:", css)
        self.assertIn("--tk-on-primary:", css)
        for entry in pe.generate("other")["palettes"]:
            self.assertEqual(len(entry["tokens_rgb"]["primary"].split(",")), 3)

    def test_vertical_e_ceticismo_desconhecidos_sao_recusados(self):
        with self.assertRaises(ValueError):
            pe.generate("pet-care")
        with self.assertRaises(ValueError):
            pe.generate("home", skepticism="altíssimo")


class ValidadorReprova(unittest.TestCase):
    """Cada caso abaixo DEVE falhar: é o que impede a paleta de sair com aviso."""

    @classmethod
    def setUpClass(cls):
        # uma candidata real, de fundo claro, que passa em tudo: cada teste troca UM role e
        # confere que a troca sozinha já reprova a paleta
        candidatas = pe.generate("supplements", skepticism="médio")["palettes"]
        cls.base = next(c for c in candidatas if pe.hex_to_hsl(c["palette"]["background"])[2] > 0.5)

    def test_a_paleta_de_referencia_passa_em_tudo(self):
        self.assertEqual(pe.validate_palette(self.base), [])

    def assertFalha(self, entry, trecho):
        fails = pe.validate_palette(entry)
        self.assertTrue(fails, "a paleta deveria ter sido reprovada")
        self.assertTrue(any(trecho in f for f in fails), f"{trecho!r} não apareceu em {fails}")

    def test_primary_cinza(self):
        self.assertFalha(entry_with(self.base, primary="#6B6B6B", on_primary="#FFFFFF"), "saturação")

    def test_accent_cinza(self):
        self.assertFalha(entry_with(self.base, accent="#767676"), "saturação")

    def test_primary_quase_cinza_tambem_reprova(self):
        # tem cor, mas pouca demais pra ser lida como cor: é exatamente o que o piso existe pra pegar
        quase = pe.hsl_to_hex(158, 0.23, 0.32)
        self.assertFalha(entry_with(self.base, primary=quase, on_primary="#FFFFFF"), "saturação")

    def test_texto_sem_contraste_contra_o_fundo(self):
        self.assertFalha(entry_with(self.base, foreground="#B9C6BD"), "foreground/background")

    def test_texto_do_botao_sem_contraste(self):
        self.assertFalha(entry_with(self.base, primary="#2E7D5B", on_primary="#7ED3AC"), "on_primary/primary")

    def test_texto_secundario_sem_contraste(self):
        self.assertFalha(entry_with(self.base, muted="#C2CCC7"), "muted/background")

    def test_texto_secundario_que_so_falha_dentro_do_cartao(self):
        """Passa contra o fundo e falha contra a superfície. É o caso que some quando o
        contraste é medido só contra o fundo, e que o olho pega no cartão de oferta."""
        background, surface = self.base["palette"]["background"], self.base["palette"]["surface"]
        hue = pe.hex_to_hsl(self.base["palette"]["muted"])[0]
        limite = None
        for passo in range(100):                       # clareia até raspar o mínimo contra o fundo
            candidato = pe.hsl_to_hex(hue, 0.10, 0.30 + passo * 0.01)
            if pe.contrast_ratio(candidato, background) < 4.75:
                limite = candidato
                break
        self.assertIsNotNone(limite)
        self.assertGreaterEqual(pe.contrast_ratio(limite, background), 4.5)
        self.assertLess(pe.contrast_ratio(limite, surface), 4.5)
        self.assertFalha(entry_with(self.base, muted=limite), "muted/surface")

    def test_cor_de_apoio_sem_contraste_grafico(self):
        self.assertFalha(entry_with(self.base, accent="#8FE0C6"), "accent/background")

    def test_harmonia_declarada_que_nao_bate_com_a_distancia_real(self):
        entry = copy.deepcopy(self.base)
        entry["harmony"] = "triad"
        entry["palette"]["primary"] = "#1F6A4E"      # matiz 158
        entry["palette"]["on_primary"] = "#FFFFFF"
        entry["palette"]["accent"] = "#1F6A8A"       # matiz 198: 40 graus, não 120
        self.assertFalha(entry, "harmonia declarada")

    def test_harmonia_declarada_estreita_com_distancia_de_outra_relacao(self):
        entry = copy.deepcopy(self.base)
        entry["harmony"] = "analogous"                  # pede de 20 a 50 graus
        entry["palette"]["primary"] = pe.hsl_to_hex(158, 0.62, 0.30)
        entry["palette"]["on_primary"] = "#FFFFFF"
        entry["palette"]["accent"] = pe.hsl_to_hex(278, 0.60, 0.42)   # 120 graus: é tríade, não análoga
        self.assertFalha(entry, "harmonia declarada")

    def test_harmonia_ausente(self):
        entry = copy.deepcopy(self.base)
        entry["harmony"] = None
        self.assertFalha(entry, "relação de matiz")

    def test_role_faltando_ou_hex_invalido(self):
        entry = copy.deepcopy(self.base)
        del entry["palette"]["border"]
        self.assertFalha(entry, "roles ausentes")
        self.assertFalha(entry_with(self.base, surface="sage green"), "roles ausentes")

    def test_conjunto_precisa_ter_exatamente_tres(self):
        entries = pe.generate("supplements")["palettes"]
        self.assertTrue(any("são sempre" in f for f in pe.validate_set(entries[:2])))

    def test_conjunto_com_tres_versoes_da_mesma_cor(self):
        base = pe.generate("supplements")["palettes"]
        quase_iguais = [
            entry_with(base[0], primary="#1F6A4E"),   # 158
            entry_with(base[1], primary="#1F6A57"),   # 165
            entry_with(base[2], primary="#1F6A61"),   # 172
        ]
        fails = pe.validate_set(quase_iguais)
        self.assertTrue(any("abaixo dos" in f for f in fails), fails)


class Matematica(unittest.TestCase):
    """As contas que sustentam os quatro testes."""

    def test_contraste_conhecido(self):
        self.assertAlmostEqual(pe.contrast_ratio("#FFFFFF", "#000000"), 21.0, places=2)
        self.assertAlmostEqual(pe.contrast_ratio("#FFFFFF", "#FFFFFF"), 1.0, places=2)
        self.assertAlmostEqual(pe.contrast_ratio("#767676", "#FFFFFF"), 4.54, places=1)

    def test_ida_e_volta_entre_hex_e_hsl(self):
        for value in ("#2563EB", "#A6522F", "#0D1117", "#FDF8F1", "#7C9A6D"):
            hue, sat, light = pe.hex_to_hsl(value)
            self.assertEqual(pe.hsl_to_hex(hue, sat, light), value.upper())

    def test_distancia_de_matiz_e_circular(self):
        self.assertAlmostEqual(pe.hue_delta(350, 10), 20.0)
        self.assertAlmostEqual(pe.hue_delta(10, 350), 20.0)
        self.assertAlmostEqual(pe.hue_delta(0, 180), 180.0)

    def test_faixa_de_matiz_nomeia_o_circulo_inteiro(self):
        for hue in range(0, 360, 5):
            self.assertTrue(pe.hue_family(hue)["label"])
            self.assertTrue(pe.hue_family(hue, "en")["label"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
