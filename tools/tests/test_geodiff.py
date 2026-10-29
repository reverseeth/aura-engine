import tempfile
import unittest
from pathlib import Path

from _pageqa import band, write_capture
import geodiff


class Geodiff(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_mesma_geometria_da_100(self):
        ref = write_capture(self.root / "ref", [band(0)])
        page = write_capture(self.root / "page", [band(0, section="hero")])
        out = geodiff.run([ref], page, geodiff.parse_map("0:0:hero"))
        self.assertEqual(out["min_score"], 100)

    def test_grade_de_3_para_1_coluna_cai_abaixo_de_70(self):
        ref = write_capture(self.root / "ref", [band(0)])
        boxes = [{"kind": "text", "cx": 0.5, "cy": 0.5, "w": 0.8, "h": 0.05},
                 {"kind": "media", "cx": 0.5, "cy": 0.9, "w": 0.8, "h": 0.2}]
        page = write_capture(self.root / "page", [band(0, height=900, columns=1, section="hero", boxes=boxes)])
        out = geodiff.run([ref], page, geodiff.parse_map("0:0:hero"))
        self.assertLess(out["min_score"], 70)
        self.assertIn("colunas", out["sections"][0]["top_diffs"])

    def test_quebra_cabeca_com_duas_referencias(self):
        r0 = write_capture(self.root / "r0", [band(0)])
        r1 = write_capture(self.root / "r1", [band(0), band(1, columns=2)])
        page = write_capture(self.root / "page", [band(0, section="hero"), band(1, columns=2, section="offer")])
        out = geodiff.run([r0, r1], page, geodiff.parse_map("0:0:hero,1:1:offer"))
        self.assertEqual([s["score"] for s in out["sections"]], [100, 100])

    def test_secao_ausente_na_pagina_da_zero(self):
        ref = write_capture(self.root / "ref", [band(0)])
        page = write_capture(self.root / "page", [band(0, section="outra")])
        out = geodiff.run([ref], page, geodiff.parse_map("0:0:hero"))
        self.assertEqual(out["min_score"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
