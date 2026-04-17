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
  title: product_name,           // "<brand> <product> System"
  vendor: brand_name,            // "<brand>"
  product_type: "Beauty & Personal Care",
  status: "draft",               // sempre draft, humano publica
  tags: ["skincare", "at-home", "anti-aging", brand_name],
  body_html: extract_description_from_copy(description_md)
})
```

### 2. Criar 3 variants
```
for tier in offer_tiers:
    variant = shopify.variant.create(product.id, {
      title: tier.name,              // "Starter", "Popular", "BestValue"
      price: tier.price,             // 49, 119, 199
      compare_at_price: tier.compare_price,  // se tiver "de"
      sku: tier.sku,                 // "<BRAND>-MI-01", etc
      inventory_quantity: 100,
      inventory_management: "shopify",
      weight: 0.12,                  // kg
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
Ler `/workspace/[produto]/06-page/staging/templates/page.<brand>-<product-slug>.json`:

```
sections_to_patch = ["offer"]
for section_id in sections_to_patch:
    replace(
      template[section_id].settings,
      placeholders={
        "VARIANT_ID_STARTER": wire_variant_ids["Starter"],
        "VARIANT_ID_POPULAR": wire_variant_ids["Popular"],
        "VARIANT_ID_BESTVALUE": wire_variant_ids["BestValue"]
      }
    )
```

Salvar template atualizado:
```
shopify.theme.asset.update(
  theme_id=profile.shopify_theme_id,
  key="templates/page.<brand>-<product-slug>.json",
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

Mensagem:
```
✓ Produto <brand> <product> criado no Shopify (draft).
  3 variants: Starter $49, Popular $119, BestValue $199
  Variant IDs wired no template page.<brand>-<product-slug>.
  Imagens uploaded: 5

  Next steps:
  1. Abra Admin → Products → review → Publish
  2. Admin → Pages → criar Page vinculada ao template
  3. Preview: https://[store].myshopify.com/products/<brand>-<product-slug>
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
