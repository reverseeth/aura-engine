#!/usr/bin/env python3
"""
Testes do validador `tools/schema_validate.py` para `additionalProperties` como schema.

O manifest declara `storefront.variant_ids` como um mapa de chaves livres (a quantidade do tier)
para GID de variante em texto. Sem este suporte, a restrição do valor seria decorativa: qualquer
coisa passaria no mapa e o erro só apareceria na loja, com o botão de compra apontando para nada.
Os testes provam os dois lados: o mapa certo passa, o mapa com valor de outro tipo reprova, e o
comportamento antigo de `additionalProperties: false` e de schema sem a palavra continua igual.

Rodar da raiz do repositório:
  python3 -m unittest discover -s tools/tests
  python3 tools/tests/test_schema_validate.py

Só biblioteca padrão.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import schema_validate  # noqa: E402

MAPA_DE_TEXTO = {"type": "object", "additionalProperties": {"type": "string"}}


class TestAdditionalPropertiesComoSchema(unittest.TestCase):
    def test_mapa_de_chaves_livres_com_valor_certo_passa(self):
        instancia = {"1": "gid://shopify/ProductVariant/1", "3": "gid://shopify/ProductVariant/3"}
        self.assertEqual(schema_validate.validate(instancia, MAPA_DE_TEXTO), [])

    def test_valor_de_outro_tipo_reprova_e_nomeia_a_chave(self):
        fails = schema_validate.validate({"1": 123}, MAPA_DE_TEXTO, "$.storefront.variant_ids")
        self.assertEqual(len(fails), 1)
        self.assertIn("$.storefront.variant_ids.1", fails[0])

    def test_reprova_uma_vez_por_chave_errada(self):
        fails = schema_validate.validate({"1": 123, "3": None, "6": "ok"}, MAPA_DE_TEXTO)
        self.assertEqual(len(fails), 2)

    def test_mapa_vazio_passa(self):
        self.assertEqual(schema_validate.validate({}, MAPA_DE_TEXTO), [])

    def test_chave_declarada_em_properties_nao_e_revalidada_pelo_mapa(self):
        schema = {
            "type": "object",
            "properties": {"nome": {"type": "number"}},
            "additionalProperties": {"type": "string"},
        }
        fails = schema_validate.validate({"nome": 7, "extra": "texto"}, schema)
        self.assertEqual(fails, [])

    def test_additional_properties_false_continua_reprovando_campo_extra(self):
        schema = {"type": "object", "properties": {"a": {"type": "string"}}, "additionalProperties": False}
        fails = schema_validate.validate({"a": "x", "b": "y"}, schema)
        self.assertEqual(len(fails), 1)
        self.assertIn("additionalProperties: false", fails[0])

    def test_sem_a_palavra_o_campo_extra_passa(self):
        schema = {"type": "object", "properties": {"a": {"type": "string"}}}
        self.assertEqual(schema_validate.validate({"a": "x", "b": 9}, schema), [])

    def test_additional_properties_true_nao_restringe_nada(self):
        schema = {"type": "object", "additionalProperties": True}
        self.assertEqual(schema_validate.validate({"a": 1, "b": None}, schema), [])


class TestManifestVariantIds(unittest.TestCase):
    """O schema real do manifest, não uma cópia: se o campo mudar de forma, o teste acusa."""

    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / ".claude" / "templates" / "manifest-schema.json").read_text(encoding="utf-8"))
        cls.storefront = cls.schema["properties"]["storefront"]

    def test_variant_ids_declara_valor_em_texto(self):
        self.assertEqual(self.storefront["properties"]["variant_ids"]["additionalProperties"], {"type": "string"})

    def test_manifest_com_ids_validos_passa(self):
        manifest = {
            "product_slug": "prod-teste",
            "product_name": "Produto Teste",
            "created_at": "2026-09-18T00:00:00Z",
            "updated_at": "2026-09-18T00:00:00Z",
            "skills_completed": ["page-design"],
            "storefront": {
                "product_id": "gid://shopify/Product/123",
                "product_handle": "produto-teste",
                "product_status": "draft",
                "published_online_store": False,
                "variant_ids": {"1": "gid://shopify/ProductVariant/1"},
                "selling_plan_id": None,
            },
            "shopify_product_ops": {"sku_base": "AURA-X", "initial_inventory": 300, "unit_weight_kg": 0.35},
        }
        self.assertEqual(schema_validate.validate(manifest, self.schema), [])

    def test_manifest_com_id_de_variante_numerico_reprova(self):
        manifest = {
            "product_slug": "prod-teste",
            "product_name": "Produto Teste",
            "created_at": "2026-09-18T00:00:00Z",
            "updated_at": "2026-09-18T00:00:00Z",
            "skills_completed": ["page-design"],
            "storefront": {"variant_ids": {"1": 42}},
        }
        fails = schema_validate.validate(manifest, self.schema)
        self.assertEqual(len(fails), 1)
        self.assertIn("variant_ids.1", fails[0])

    def test_product_status_fora_do_enum_reprova(self):
        manifest = {
            "product_slug": "prod-teste",
            "product_name": "Produto Teste",
            "created_at": "2026-09-18T00:00:00Z",
            "updated_at": "2026-09-18T00:00:00Z",
            "skills_completed": ["page-design"],
            "storefront": {"product_status": "publicado"},
        }
        fails = schema_validate.validate(manifest, self.schema)
        self.assertEqual(len(fails), 1)
        self.assertIn("product_status", fails[0])


if __name__ == "__main__":
    unittest.main()
