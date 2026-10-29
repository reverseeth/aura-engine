import json
import tempfile
import unittest
from pathlib import Path

from _pageqa import band, write_capture
import copy_fit
import geodiff


class CopyFit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ref = write_capture(self.root / "ref", [band(0)], texts=["x" * 300])

    def tearDown(self):
        self.tmp.cleanup()

    def test_copy_do_mesmo_tamanho_cabe(self):
        out = copy_fit.run([self.ref], geodiff.parse_map("0:0:hero"), {"hero": "y" * 320})
        self.assertTrue(out["all_fit"])

    def test_copy_tres_vezes_maior_nao_cabe(self):
        out = copy_fit.run([self.ref], geodiff.parse_map("0:0:hero"), {"hero": ["y" * 500, "z" * 400]})
        self.assertFalse(out["sections"][0]["fits"])
        self.assertEqual(out["sections"][0]["ratio"], 3.0)

    def test_geodiff_nao_cobra_altura_de_copy_que_nao_cabe(self):
        page = write_capture(self.root / "page", [band(0, height=1800, section="hero")])
        mapping = geodiff.parse_map("0:0:hero")
        fit = copy_fit.run([self.ref], mapping, {"hero": "y" * 900})
        self.assertLess(geodiff.run([self.ref], page, mapping)["min_score"], 70)
        out = geodiff.run([self.ref], page, mapping, fit)
        self.assertEqual(out["min_score"], 100)
        self.assertIn("altura livre (copy 3.0×)", out["sections"][0]["top_diffs"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
