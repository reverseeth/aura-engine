# Recipe: Deploy Shopify Product + Wire Variants

## Triggers
- "cria o produto no Shopify"
- "deploy Shopify product com variants"
- "wire variant IDs na PDP"

## Input
- `product_slug` — do manifest
- `bundle_tiers` — do `07d-checkout-aov/dados.json` → `levers.bundles.tiers` (array `{qty, price, label}` — ex: Solo qty 1 / 3-pack "Popular" / 6-pack "Best Value"). **Se a 07d não rodou ou `bundles.active == false`:** produto single-variant no `pricing.main_sku_price` do `04-offer-builder/dados.json`.
- `description_md` — caminho do `06-copy-engine/copy-engine.md` (seção PDP ou description; se não existir, use o legado `relatorio.md`)
- `images` — array de paths locais. Não há convenção de pasta de imagens no workspace — se vazio, perguntar ao membro os paths (ou confirmar stock placeholders).

**Dados operacionais que NENHUMA skill grava (perguntar ao membro na 1ª run, 1 mensagem só):** SKU base, estoque inicial e peso da unidade. Derivar por tier: `sku = <SKU_BASE>-<qty>pk`, `inventory = estoque ÷ mix esperado`, `weight = peso_unidade × qty`. Gravar as respostas em `manifest.shopify_product_ops` (`{sku_base, initial_inventory, unit_weight_kg}`) pra não perguntar de novo.

## Cascade (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md`)

**Caminho 1 — Shopify MCP (`mcp__shopify__*`, AI Toolkit):** caminho preferencial. Cria produto, variants, imagens e patcheia o template via tool calls. Opcionalmente o **Shopify Dev MCP** (`mcp__shopify_dev__*`) valida o GraphQL/Liquid antes de aplicar (reduz hallucination).

**Caminho 2 — Playwright headless:** fallback pra operações que o MCP não cobre (ex: criar a Shopify Page que vincula o template). Login: primeira run abre browser headed pro membro logar no Admin e salva `storage_state` local — ver `setup-mcps.md` passo 6.

**Caminho 3 — manual:** membro cria produto/page no Admin e cola os IDs.

> **Nota:** o `body_html`/template push respeita `shopify-theme-safety.md` (pull antes de editar, `--nodelete`, marker verification). Por default usa tema unpublished; tema live exige `--allow-live`.

## Pre-flight
- [ ] Shopify MCP conectado (`mcp__shopify__*`) OU Playwright disponível como fallback (ver cascade acima)
- [ ] `07d-checkout-aov/dados.json` com `levers.bundles.tiers` (OU decisão explícita de single-variant via 04)
- [ ] `06-copy-engine/copy-engine.md` existe
- [ ] `manifest.storefront.theme_id` preenchido (gravado pela 07b no deploy da página)
- [ ] SKU base / estoque / peso confirmados (ver Input)
- [ ] Imagens disponíveis (ou stock placeholders marcados)

## Steps

### 1. Criar produto base
```
product = shopify.product.create({
  title: product_name,           // lê do manifest.product_name
  vendor: brand_name,            // lê do manifest.brand_name
  product_type: derived_from_category,  // da skill 01
  status: "draft",               // sempre draft, humano publica
  tags: derived_tags_from_category_and_brand,
  body_html: extract_description_from_copy(description_md)
})
```

### 2. Criar variants (1 por tier de bundle)
```
for tier in bundle_tiers:        // do 07d-checkout-aov/dados.json (levers.bundles.tiers)
    tier_name = tier.label or f"{tier.qty}-pack" if tier.qty > 1 else "Solo"
    variant = shopify.variant.create(product.id, {
      title: tier_name,
      price: tier.price,
      compare_at_price: round(main_sku_price * tier.qty, 2) if tier.qty > 1 else null,  // "was" = N× o preço solo (âncora da 07d)
      sku: f"{ops.sku_base}-{tier.qty}pk",
      inventory_quantity: derived_inventory(tier),
      inventory_management: "shopify",
      weight: ops.unit_weight_kg * tier.qty,
      weight_unit: "kg",
      option1: tier_name
    })
    wire_variant_ids[tier.qty] = variant.id
```

### 3. Upload imagens
```
for img_path in images:
    shopify.product.image.create(product.id, {
      src: upload_to_cdn(img_path),
      alt: derive_alt(img_path)
    })
```

### 4. Wire Variant IDs no template.json
Ler o template gerado pela skill 07b (caminho derivado do product_slug do manifest). **Backup local ANTES de mexer** (workspace é local-only, sem git — o backup é a única rota de rollback):

```
template_path = f"/workspace/{product_slug}/07-page/staging/templates/page.{product_slug}.json"
copy(template_path, f"{template_path}.bak-{timestamp}")

# A 07b emite blocks `pricing_tier` na section de pricing, cada um com um
# setting `variant_id`. Casar block ↔ variant pela quantidade (qty do tier):
for block in template.pricing_section.blocks where block.type == "pricing_tier":
    block.settings.variant_id = wire_variant_ids[block.settings.qty]
```

Salvar template atualizado:
```
shopify.theme.asset.update(
  theme_id=manifest.storefront.theme_id,   // fonte canônica — gravado pela 07b
  key=f"templates/page.{product_slug}.json",
  value=json.dumps(template)
)
```

### 5. Log + reportar
```json
{
  "action": "deploy_shopify_product",
  "source": "shopify_mcp",
  "product_id": "<Shopify GID>",
  "variant_ids": {
    "Solo": "<gid variant>",
    "3-pack": "<gid variant>",
    "6-pack": "<gid variant>"
  },
  "status": "draft",
  "theme_patched": true
}
```

Mensagem ao membro (estrutura — valores vêm do manifest do membro):
```
✓ Produto <product_name> criado no Shopify (draft).
  <N> variants: <tier_list_com_preços>
  Variant IDs wired no template page.<product_slug>.
  Imagens uploaded: <N>

  Next steps:
  1. Abra Admin → Products → review → Publish
  2. Admin → Pages → criar Page vinculada ao template
  3. Preview: https://<store>.myshopify.com/products/<product_slug>
```

## Rollback
Se falhar:
```
shopify.product.delete(product.id)   # remove produto + variants
# template.json: restaurar do backup local criado no step 4
copy(f"{template_path}.bak-{timestamp}", template_path)
shopify.theme.asset.update(...)      # re-push do template restaurado
```

(workspace/ é local-only e gitignored — NÃO existe "reverter via git"; o backup `.bak-<timestamp>` é a fonte de restore.)

## Edge cases
- **Imagens já existentes**: MCP detecta hash; não duplica
- **SKU conflito**: falha explicitamente, não sobrescreve
- **Theme published**: requer `--allow-live` flag; por default usa tema unpublished
- **Oferta single-SKU (sem bundles da 07d)**: 1 variant no `pricing.main_sku_price`; o wire do step 4 preenche o único `variant_id`
