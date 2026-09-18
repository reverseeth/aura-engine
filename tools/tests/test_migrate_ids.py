#!/usr/bin/env python3
"""
Testes do filtro de contexto numérico ("palavra isolada") do tools/migrate_ids.py e da regra
skill-ids do tools/aura-check.py, que importa o mesmo conversor.

Um número só é candidato a apelido de skill quando aparece isolado como palavra ("a 08", "skill 12").
Dígito colado, vírgula ou ponto seguidos de dígito, %, moeda, unidade colada, data AAAA-MM-DD, barra
com dígito dos dois lados e palavra de quantidade depois do número nunca viram id de skill, em nenhuma
âncora. As linhas abaixo citam apelidos de propósito; por isso a pasta
tools/tests/ fica fora da varredura do lint e do conversor.

A classe LintSlugAbreviado cobre a forma abreviada do apelido (`04-offer` no lugar de
`04-offer-builder`): ela reprova em texto do framework e passa nos quatro contextos em que o número
é o dado (registro, mapa de pastas do build_index.py, use_in_skill do índice, changelog do OVERVIEW).

Rodar da raiz do repositório:
  python3 -m unittest discover -s tools/tests
  python3 tools/tests/test_migrate_ids.py

Só biblioteca padrão.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
import migrate_ids as mig  # noqa: E402

# Número em contexto numérico: o conversor não toca, o relatório não lista, o lint não acusa.
NEGATIVOS = [
    '"Featured in Forbes · 4.8★ (12,000 reviews) · Dermatologist-tested"',   # vírgula + dígito, dentro de parêntese
    "a margem de contribuição do primeiro pedido é US$ 18,70 (18,7%)",         # vírgula + dígito + %
    "o plano custa $12 por mês",                                               # moeda colada antes
    "rodado em 2026-09-01",                                                    # data AAAA-MM-DD
    "reserve 20% do budget pra teste",                                         # % colado depois
    "US$ 12 de CPA e R$12 de frete",                                           # moeda com e sem espaço
    "12k reviews, 12h de espera, 12min de vídeo",                              # unidade colada
    "PSM de 1,12 e ticket de 3.12",                                            # dígito + vírgula/ponto antes
    "Singles' Day (11/11) eclipsa a BFCM na Ásia; Boxing Day (26/12) é forte",  # data com barra
    "Aplique as 15 perguntas (12 numeradas mais 3b, 3c e 3d) aos dados",        # palavra de quantidade depois
    "### ETAPA 7 — Hooks Bank (10 Alternativas)",                               # palavra de quantidade depois
    "pare quando a pesquisa produziu de 5 a 10 boas ideias de anúncio",         # faixa em português
    "ETAPAs 1 a 6 e 12 a 14 rodam nos dois modos",                              # faixa em português
    "ofertas finais aprovadas até 10/nov; flows testados até 15/nov",           # data com mês abreviado
]

# Número isolado como palavra, com âncora de skill: continua convertendo.
POSITIVOS = [
    ("rode a skill 12 antes de escalar", "rode a skill `scale-engine` antes de escalar"),
]


def load_lint():
    spec = importlib.util.spec_from_file_location("aura_check", TOOLS / "aura-check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ContextoNumerico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = mig.Registry()

    def test_convert_line_ignora_contexto_numerico(self):
        for linha in NEGATIVOS:
            with self.subTest(linha=linha):
                self.assertEqual(mig.convert_line(linha, self.reg), (linha, 0))

    def test_report_line_ignora_contexto_numerico(self):
        for linha in NEGATIVOS:
            with self.subTest(linha=linha):
                self.assertEqual(mig.report_line(linha, self.reg), [])

    def test_convert_line_converte_skill_isolada(self):
        for antes, depois in POSITIVOS:
            with self.subTest(linha=antes):
                self.assertEqual(mig.convert_line(antes, self.reg), (depois, 1))

    def test_report_line_lista_skill_isolada(self):
        tags = [t for t, _, _ in mig.report_line(POSITIVOS[0][0], self.reg)]
        self.assertEqual(tags, ["skill"])


class LintSkillIds(unittest.TestCase):
    """A regra skill-ids do aura-check.py sobre um arquivo virtual: só a linha positiva é falha."""

    @classmethod
    def setUpClass(cls):
        cls.ac = load_lint()
        cls.reg = cls.ac.Registry()
        cls.index = cls.ac.load_json(cls.ac.INDEX)

    def test_regra_skill_ids(self):
        virtual = ".claude/skills/_fixture-de-teste.md"          # nunca existe em disco
        linhas = NEGATIVOS + [antes for antes, _ in POSITIVOS]
        self.ac._LINES[virtual] = linhas
        try:
            fails = [f for f in self.ac.rule_skill_ids([virtual], self.reg, self.index) if f.file == virtual]
        finally:
            self.ac._LINES.pop(virtual, None)
        self.assertEqual([f.line for f in fails], [len(linhas)], [f.render() for f in fails])
        self.assertIn("`scale-engine`", fails[0].msg)


# Forma abreviada do apelido (`04-offer` em vez de `04-offer-builder`): é referência a skill e o
# lint acusa, menos nos quatro contextos em que o número é o dado e não a referência.
ABREVIADOS = [
    "aponta pro `upsell` do 04-offer",
    "a copy toda vem de 06-copy",
]
# Número seguido de hífen e de palavra que NÃO é começo de slug de skill, ou com o apelido de outra
# skill: continua fora da regra, em qualquer arquivo.
ABREVIADOS_NEGATIVOS = [
    "a garantia roda numa 90-day window",
    "o checklist é de 19-point",
    "12-copy não é apelido do copy-engine",
]
# Um contexto permitido por entrada: (arquivo, linhas, quantas falhas esperadas).
CONTEXTOS_PERMITIDOS = [
    # registro: legacy_folder e legacy_ids são o dado
    (".claude/skills.json", ['    "legacy_folder": "04-offer-builder",', '    "legacy_ids": ["04"],'], 0),
    # mapa de pastas antigas do build_index.py: bloco gerado pelo gen_docs.py
    (".claude/lib/workspace-index/build_index.py",
     ["# gen:phases:start", 'LEGACY_FOLDERS = {', '    "offer-builder": "04-offer-builder",',
      '    "copy-engine": "06-copy-engine",', "}", "# gen:phases:end"], 0),
    # use_in_skill do índice: texto original do catálogo
    (".claude/lib/kb-index/frameworks.json", ['      "use_in_skill": "04-offer, 06-copy",'], 0),
    # changelog do OVERVIEW: registro histórico (e só ele — a linha antes da seção reprova)
    (".claude/OVERVIEW.md",
     ["a oferta é da 04-offer", "## 14. Mudanças recentes", "| data | renomeou 04-offer-builder |"], 1),
]


class LintSlugAbreviado(unittest.TestCase):
    """`04-offer`/`06-copy` reprovam; os quatro contextos em que o número é o dado passam."""

    @classmethod
    def setUpClass(cls):
        cls.ac = load_lint()
        cls.reg = cls.ac.Registry()
        cls.index = cls.ac.load_json(cls.ac.INDEX)

    def _fails(self, arquivo, linhas):
        anterior = self.ac._LINES.get(arquivo)
        self.ac._LINES[arquivo] = linhas
        try:
            return [f for f in self.ac.rule_skill_ids([arquivo], self.reg, self.index) if f.file == arquivo]
        finally:
            if anterior is None:
                self.ac._LINES.pop(arquivo, None)
            else:
                self.ac._LINES[arquivo] = anterior

    def test_abreviado_reprova(self):
        virtual = ".claude/skills/_fixture-de-teste.md"
        fails = self._fails(virtual, ABREVIADOS)
        self.assertEqual([f.line for f in fails], [1, 2], [f.render() for f in fails])
        self.assertIn("`offer-builder`", fails[0].msg)
        self.assertIn("`copy-engine`", fails[1].msg)

    def test_numero_com_hifen_fora_da_regra(self):
        virtual = ".claude/skills/_fixture-de-teste.md"
        fails = self._fails(virtual, ABREVIADOS_NEGATIVOS)
        self.assertEqual(fails, [], [f.render() for f in fails])

    def test_contextos_permitidos(self):
        for arquivo, linhas, esperadas in CONTEXTOS_PERMITIDOS:
            with self.subTest(arquivo=arquivo):
                fails = self._fails(arquivo, linhas)
                self.assertEqual(len(fails), esperadas, [f.render() for f in fails])


if __name__ == "__main__":
    unittest.main()
