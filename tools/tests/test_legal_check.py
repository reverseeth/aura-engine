import tempfile
import unittest
from pathlib import Path

from _pageqa import band, write_capture
import legal_check

TEXT = "our patented night formula helps you fall asleep in minutes"
ASSET = "https://cdn.loja-referencia.com/img/hero-bottle-01.webp"


def page(body):
    return f"<html><body><main><section data-aura-section='hero'>{body}</section></main></body></html>"


class LegalCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ref = write_capture(self.root / "ref", [band(0)], texts=[TEXT], assets=[ASSET],
                                 styles=[{"styles": {"font-family": "'Ref Grotesk', sans-serif"}}])

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, html, **kw):
        p = self.root / "page.html"
        p.write_text(html)
        return legal_check.run([self.ref], str(p), kw.get("fonts", []), kw.get("brands", []))

    def test_reutilizar_texto_e_asset_falha(self):
        out = self.check(page(f"<p>{TEXT.upper()}!</p><img src='/x/hero-bottle-01.webp'>"))
        self.assertFalse(out["pass"])
        self.assertEqual({f["rule"] for f in out["findings"]}, {"texto", "asset"})

    def test_frase_da_allowlist_passa(self):
        out = self.check(page("<p>30-day money-back guarantee. Free shipping on all orders.</p>"))
        self.assertTrue(out["pass"], out["findings"])

    def test_pagina_propria_passa(self):
        out = self.check(page("<p>Sleep deeper with magnesium and calm botanicals tonight.</p>"))
        self.assertTrue(out["pass"], out["findings"])

    def test_fonte_da_referencia_so_passa_se_permitida(self):
        html = page("<p style=\"font-family:'Ref Grotesk'\">Hi there</p>")
        self.assertEqual([f["rule"] for f in self.check(html)["findings"]], ["fonte"])
        d = self.root / "direction.md"
        d.write_text("## Tipografia\n- família: Ref Grotesk (heading)\n\n## Paleta\n")
        self.assertTrue(self.check(html, fonts=[str(d)])["pass"])

    def test_nome_da_marca_derivado_do_dominio(self):
        out = self.check(page("<p>Better than Loja Referencia, honestly.</p>"))
        self.assertEqual([f["rule"] for f in out["findings"]], ["marca"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
