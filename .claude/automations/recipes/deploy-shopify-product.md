# Recipe: Deploy Shopify Product + Wire Variants

## Triggers
- "cria o produto no Shopify"
- "deploy Shopify product com variants"
- "wire variant IDs na PDP"

## Input
- `product_slug` — do manifest
- `offer_tiers` — do `04-offer.json` (Starter, Popular, BestValue com preços e SKUs)
- `description_md` — caminho do `05-copy.md` (seção PDP ou description)
- `images` — array de paths locais

## Pre-flight
- [ ] Shopify MCP conectado
- [ ] `04-offer.json` existe com 3 tiers
- [ ] `05-copy.md` existe
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

### 2. Criar 3 variants
```
for tier in offer_tiers:     // lê do 04-offer.json
    variant = shopify.variant.create(product.id, {
      title: tier.name,
      price: tier.price,
      compare_at_price: tier.compare_price,
      sku: tier.sku,
      inventory_quantity: tier.initial_inventory,
      inventory_management: "shopify",
      weight: tier.weight_kg,
      weight_unit: "kg",
      option1: tier.name
    })
    wire_variant_ids[tier.name] = variant.id
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
Ler o template gerado pela skill 06 (caminho derivado do product_slug do manifest).

```
template_path = f"/workspace/{product_slug}/06-page/staging/templates/page.{product_slug}.json"
sections_to_patch = ["offer"]
for section_id in sections_to_patch:
    replace(
      template[section_id].settings,
      placeholders={
        variant_placeholder: wire_variant_ids[tier.name]
        for tier in offer_tiers
      }
    )
```

Salvar template atualizado:
```
shopify.theme.asset.update(
  theme_id=profile.shopify_theme_id,
  key=f"templates/page.{product_slug}.json",
  value=json.dumps(template)
)
```

### 5. Log + reportar
```json
{
  "action": "deploy_shopify_product",
  "product_id": "gid://shopify/Product/8123456",
  "variant_ids": {
    "Starter": "gid://shopify/ProductVariant/40123",
    "Popular": "gid://shopify/ProductVariant/40124",
    "BestValue": "gid://shopify/ProductVariant/40125"
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
shopify.product.delete(product.id)  # remove produto + variants
# template.json reverter via git
```

## Edge cases
- **Imagens já existentes**: MCP detecta hash; não duplica
- **SKU conflito**: falha explicitamente, não sobrescreve
- **Theme published**: requer `--allow-live` flag; por default usa tema unpublished
