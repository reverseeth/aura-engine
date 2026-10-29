import json
import tempfile
import unittest
from pathlib import Path

from _pageqa import FIXTURES
import tokens

CLEAN = (FIXTURES / "clean.html").read_text()


class Tokens(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_root_completo_vira_design_tokens_com_os_8_papeis(self):
        out = tokens.from_page(CLEAN, "palette_engine", "atelier", {"produto": "x"})
        self.assertEqual(set(out["colors"]), set(tokens.ROLES))
        self.assertEqual(out["colors"]["primary"], "#1f4d3a")
        self.assertEqual([f["name"] for f in out["type"]["families"]], ["Georgia", "Helvetica"])
        self.assertEqual((out["produto"], out["preset_base"]), ("x", "atelier"))

    def test_seis_cores_soltas_reprovam(self):
        html = CLEAN.replace("</style></head>", "a{color:#111}b{color:#222}i{color:#333}"
                             "u{color:#444}s{color:#555}em{color:rgb(1,2,3)}</style></head>", 1)
        page = self.root / "p.html"
        page.write_text(html)
        code = tokens.main([str(page), "--out", str(self.root / "t.json"), "--source", "manual"])
        self.assertEqual(code, 1)

    def test_diff_de_arquivos_iguais_da_zero(self):
        t = tokens.from_page(CLEAN, "manual", None, {})
        self.assertEqual(tokens.diff(t, t)["drift"], 0)

    def test_diff_entre_design_tokens_e_brand_tokens(self):
        t = tokens.from_page(CLEAN, "manual", None, {})
        brand = tokens.to_dtcg(t["colors"], t["type"]["heading_font"], t["type"]["body_font"], "manual")
        self.assertEqual(tokens.diff(t, brand)["drift"], 0)
        brand["color"]["primary"]["$value"] = "#000000"
        self.assertEqual([c["key"] for c in tokens.diff(t, brand)["changed"]], ["color.primary"])

    def test_brand_out_recusa_marca_existente(self):
        p = self.root / "brand-tokens.json"
        p.write_text(json.dumps({"$extensions": {"aura": {"source": "dembrandt"}}}))
        self.assertEqual(tokens.write_brand(p, {"x": 1}), 4)
        p.write_text(json.dumps({"$extensions": {"aura": {"source": "none"}}}))
        self.assertEqual(tokens.write_brand(p, {"x": 1}), 0)

    def test_from_dtcg_deriva_on_primary_com_contraste(self):
        out = tokens.from_dtcg({"color": {"brand": {"primary": {"$value": "#1F4D3A"}},
                                          "background": {"$value": "#FFFFFF"}}})
        on = out["color"]["on_primary"]["$value"]
        self.assertGreaterEqual(tokens.pe.contrast_ratio(on, "#1f4d3a"), 4.5)
        self.assertEqual(set(out["color"]), set(tokens.ROLES))

    def test_diff_live_acusa_cor_fora_da_paleta(self):
        t = tokens.from_page(CLEAN, "manual", None, {})
        comp = {"sections": [{"section": "hero", "text": "rgb(26, 26, 26)", "background": "rgb(255, 0, 0)",
                              "button": None, "fonts": {"h1": "Georgia, serif"}}]}
        out = tokens.diff_live(comp, t)
        self.assertEqual([c["key"] for c in out["changed"]], ["hero.background"])

    def test_brand_tokens_gerado_e_valido_no_schema(self):
        import schema_validate
        schema = json.loads((tokens.ROOT / ".claude/templates/schemas/brand.brand-tokens.schema.json").read_text())
        t = tokens.from_page(CLEAN, "manual", None, {})
        brand = tokens.to_dtcg(t["colors"], t["type"]["heading_font"], t["type"]["body_font"], "manual")
        self.assertEqual(schema_validate.validate(brand, schema), [])
        self.assertEqual(schema_validate.validate({"$extensions": {"aura": {"source": "none"}}}, schema), [])
        self.assertNotEqual(schema_validate.validate({"$extensions": {"aura": {"source": "manual"}}}, schema), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
