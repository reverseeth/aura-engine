import json
import sys
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

    def test_provision_bate_com_o_que_a_page_build_le(self):
        # deploy.md da page-build: `local_files`, `google_fonts` ou `system`
        block = '@font-face{font-family:"Brand Serif";src:url(assets/fonts/a.woff2)}'
        self.assertEqual(tokens.provision(block, "Brand Serif"), "local_files")
        self.assertEqual(tokens.provision("", "Arial"), "system")

    def test_google_fonts_por_link_e_reconhecido(self):
        html = CLEAN.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600&display=swap"></head>')
        html = html.replace("--font-body:Helvetica,Arial,sans-serif", "--font-body:'Inter Tight',sans-serif")
        fams = {f["name"]: f["provision"] for f in tokens.from_page(html, "manual", None, {})["type"]["families"]}
        self.assertEqual(fams.get("Inter Tight"), "google_fonts")
        pesos = {f["name"]: f["weights"] for f in tokens.from_page(html, "manual", None, {})["type"]["families"]}
        self.assertEqual(pesos.get("Inter Tight"), [400, 600])

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

    def test_from_dtcg_le_o_formato_2025_do_dembrandt(self):
        # dembrandt 0.39: color.semantic.<papel>, $value como objeto e famílias por referência
        c = lambda hx: {"$type": "color", "$value": {"colorSpace": "srgb", "components": [0, 0, 0], "hex": hx}}
        out = tokens.from_dtcg({
            "color": {"semantic": {"background": c("#fafafa"), "text": c("#202020"), "primary": c("#0b6e4f")},
                      "palette": {"palette-1": c("#202020"), "palette-2": c("#e8e8e8"), "palette-3": c("#666666")}},
            "border": {"color": {"border-color-1": c("#dddddd")}},
            "typography": {"font-family": {"serif-x": {"$value": "Serif X"}},
                           "style": {"text-display": {"$value": {"fontFamily": "{typography.font-family.serif-x}"}}}}})
        cor = {k: v["$value"] for k, v in out["color"].items()}
        self.assertEqual((cor["background"], cor["foreground"], cor["primary"]), ("#fafafa", "#202020", "#0b6e4f"))
        self.assertEqual((cor["surface"], cor["muted"], cor["border"]), ("#e8e8e8", "#666666", "#dddddd"))
        self.assertEqual(out["typography"]["heading"]["fontFamily"]["$value"], "Serif X")

    def test_diff_live_acusa_cor_fora_da_paleta(self):
        t = tokens.from_page(CLEAN, "manual", None, {})
        comp = {"sections": [{"section": "hero", "text": "rgb(26, 26, 26)", "background": "rgb(255, 0, 0)",
                              "button": None, "fonts": {"h1": "Georgia, serif"}}]}
        out = tokens.diff_live(comp, t)
        self.assertEqual([c["key"] for c in out["changed"]], ["hero.background"])

    def test_brand_tokens_gerado_e_valido_no_schema(self):
        sys.path.insert(0, str(tokens.ROOT / "tools"))
        import schema_validate
        schema = json.loads((tokens.ROOT / ".claude/templates/schemas/brand.brand-tokens.schema.json").read_text())
        t = tokens.from_page(CLEAN, "manual", None, {})
        brand = tokens.to_dtcg(t["colors"], t["type"]["heading_font"], t["type"]["body_font"], "manual")
        self.assertEqual(schema_validate.validate(brand, schema), [])
        self.assertEqual(schema_validate.validate({"$extensions": {"aura": {"source": "none"}}}, schema), [])
        self.assertNotEqual(schema_validate.validate({"$extensions": {"aura": {"source": "manual"}}}, schema), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
