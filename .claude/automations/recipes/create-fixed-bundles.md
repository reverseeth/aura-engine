# Recipe: Create Fixed Bundles (Admin GraphQL `productBundleCreate`)

Automação CLI-first dos bundles fixos da oferta (tiers 3-pack/6-pack do 04/07d) via mutation nativa do Shopify — **sem app de terceiro, sem painel**. É o único pedaço do stack de AOV 100% automatizável por API hoje: o bundle nasce como produto de verdade (componentes + inventário calculado deles), rastreável em analytics e utilizável no block `pricing_tier` da PDP buildada pela 07b. Funciona em **qualquer plano** (não é Plus-only).

## Triggers
- "cria os bundles no Shopify" / "bundle nativo"
- Skill 07d (checkout-aov), Alavanca 3 — caminho 2 (bundle fixo nativo)
- Depois da recipe `deploy-shopify-product.md` (o produto principal precisa existir)

## Input
- `product_slug` — do manifest
- `bundle_tiers` — do `07d-checkout-aov/dados.json` → `levers.bundles.tiers` (array `{qty, price, label}`). Fallback 1: `04-offer-builder/dados.json` → `aov_levers.bundles[]` (`{qty, price, label, savings_pct}`). Fallback 2 (legado): Etapa 3 do `04-offer-builder/offer-builder.md`. **Só tiers com `qty > 1` viram bundle** (o Solo É o produto principal — não criar bundle de 1).
- `main_product_gid` — GID do produto principal (`gid://shopify/Product/...`), do log da recipe `deploy-shopify-product.md` (`automation-log.jsonl`) ou perguntado ao membro (1 mensagem).
- `main_sku_price` — do `04-offer-builder/dados.json` → `pricing.main_sku_price` (usado no `compareAtPrice` = âncora "was" = N× o solo).

## Cascade (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md`)

**Caminho 1 — Shopify MCP (`mcp__shopify__*`, AI Toolkit):** rodar as mutations GraphQL via tool calls. O **Shopify Dev MCP** (`mcp__shopify_dev__*`), se presente, valida o GraphQL antes de executar.

**Caminho 2 — Admin GraphQL direto (curl):** token de app do **Dev Dashboard** (mesma org da loja) via grant `client_credentials` — o caminho pós-sunset dos tokens `shpat_` criados in-admin. Requer o app com scope `write_products` instalado na loja. Endpoint: `https://$STORE/admin/api/2026-04/graphql.json` com header `X-Shopify-Access-Token`.

**Caminho 3 — manual:** membro cria os bundles no app nativo **Shopify Bundles** (grátis, admin → Apps). A recipe entrega o spec exato (título, componentes, quantidade, preço, compare-at) pra ele preencher — nunca abandonar sem caminho.

## Pre-flight
- [ ] MCP Shopify conectado OU token client_credentials com scope `write_products` (Caminho 2) — senão, cair direto pro Caminho 3
- [ ] Feature de bundles habilitada na loja (default nas lojas atuais; se a mutation retornar erro de feature, instalar o app nativo Shopify Bundles habilita)
- [ ] `main_product_gid` existe e responde (query `product(id:)`)
- [ ] `bundle_tiers` com pelo menos 1 tier `qty > 1`
- [ ] **Conflito de Cart Transform:** perguntar se o membro tem app de bundle de terceiro instalado (Fast Bundle, Bundler etc.) — só pode existir **1 Cart Transform ativa por loja**; app de terceiro por cima dos bundles nativos = comportamento imprevisível no carrinho. Se tem, escolher UM caminho (desinstalar o app OU usar só o app e pular esta recipe).

## Steps

### 1. Criar o bundle de cada tier (`qty > 1`) — assíncrono

```graphql
mutation CreateBundle($input: ProductBundleCreateInput!) {
  productBundleCreate(input: $input) {
    productBundleOperation { id status }
    userErrors { field message }
  }
}
```

```json
{
  "input": {
    "title": "<product_name> — <label ou '<qty>-pack'>",
    "components": [
      { "productId": "<main_product_gid>", "quantity": <qty>, "optionSelections": [] }
    ]
  }
}
```

- `optionSelections` mapeia opções do componente pra opções do bundle — obrigatório quando o produto principal tem options/variantes múltiplas; vazio/default pra produto single-variant.
- `userErrors` não-vazio → abortar este tier e reportar (não seguir criando os outros às cegas).

### 2. Polling da `ProductBundleOperation` (NUNCA assumir criado sem status final)

```graphql
query BundleOp($id: ID!) {
  node(id: $id) {
    ... on ProductBundleOperation {
      id status
      product { id title variants(first: 5) { nodes { id price } } }
      userErrors { field message }
    }
  }
}
```

Poll a cada 2s (backoff até 30s, timeout 2min). `status == "COMPLETE"` → capturar `product.id` (o bundle) e o variant ID. Erro/timeout → reportar e cair pro Caminho 3 com o spec pronto.

### 3. Preço + âncora do bundle

O bundle nasce com preço derivado dos componentes — aplicar o preço do tier (charm pricing do 04/07d) e a âncora:

```graphql
mutation SetBundlePrice($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id price compareAtPrice }
    userErrors { field message }
  }
}
```

```json
{ "productId": "<bundle_gid>", "variants": [ { "id": "<bundle_variant_gid>", "price": "<tier.price>", "compareAtPrice": "<main_sku_price × qty>" } ] }
```

### 4. Status draft + wire na PDP

- Manter os bundles em `status: DRAFT` (`productUpdate`) — humano revisa e publica, como toda automação Aura.
- Wire dos variant IDs nos blocks `pricing_tier` do template: reaproveitar o **step 4 da recipe `deploy-shopify-product.md`** (casa block ↔ variant pelo setting `qty` do block; o Solo aponta pro variant do produto principal, os packs pros variants dos bundles criados aqui).

### 5. Log + reportar

```json
// /workspace/[produto]/automation-log.jsonl (append)
{
  "action": "create_fixed_bundles",
  "source": "shopify_mcp | admin_api_client_credentials | manual",
  "bundles": [
    { "tier_qty": 3, "label": "Popular", "product_gid": "<gid>", "variant_gid": "<gid>", "price": 119.00, "compare_at": 147.00, "operation_status": "COMPLETE" }
  ],
  "status": "draft",
  "template_wired": true,
  "ts": "ISO-8601"
}
```

Mensagem ao membro (estrutura):
```
✓ Bundles criados no Shopify (draft): <lista tiers com preços e savings>.
  Inventário calculado automaticamente do estoque do produto principal.
  Variant IDs wired nos pricing tiers da página.

  Next steps:
  1. Admin → Products → revisar os bundles → Publish
  2. Conferir o tier "Popular" na PDP (preview)
```

## Rollback

```
productDelete de cada bundle criado (o produto principal NÃO é tocado)
template.json: restaurar o backup .bak-<timestamp> criado no wire (padrão do step 4 da deploy-shopify-product.md)
```

## Edge cases / limitações conhecidas
- **Operação assíncrona** — sem polling até `COMPLETE`, o bundle pode "existir pela metade". Nunca reportar sucesso sem o status final.
- **Cart Transform `lineUpdate`** (override de preço na LINHA do carrinho, tipo "desconto dinâmico por quantidade") é **Plus/dev-store only** — bundles fixos desta recipe não precisam disso (o preço vive no próprio produto-bundle), mas NÃO prometa quantity-break dinâmico por este caminho.
- **1 Cart Transform ativa por loja** — conflito com app de bundle de terceiro (ver pre-flight).
- **Inventário**: calculado dos componentes (3-pack com 90 unidades do solo em estoque = 30 disponíveis). Não setar inventário manual no bundle.
- **Produto com múltiplas variantes**: `optionSelections` obrigatório — se o mapeamento ficar ambíguo, cair pro Caminho 3 (app nativo resolve visualmente) em vez de chutar.
- **Feature de bundles ausente** (erro na mutation): instalar o app nativo Shopify Bundles habilita a infra; re-rodar depois.
