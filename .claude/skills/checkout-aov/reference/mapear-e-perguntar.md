# Checkout & AOV · Referência: Carregar a oferta, mapear o que existe e perguntar só o input externo (ETAPAs 1 e 2)

> Onde cada spec vive no dados.json da offer-builder (`aov_levers` e o fallback legado), a tabela das 5 alavancas, o Gate de Complementaridade aplicado às superfícies de checkout e as três perguntas de input externo. Abra na ETAPA 1.

### ETAPA 1 — Carregar a oferta e mapear o que já existe

**Onde cada spec vive no `offer-builder` (fontes reais, não campos imaginários):** o `offer-builder/dados.json` traz os campos estruturados `pricing` (`main_sku_price`, `aov_expected`), `unit_economics`, `guarantee`, `offer_stack` (string), `bonuses[]` e — **fonte primária dos detalhes de alavanca** — o bloco **`aov_levers`**: `bump` (name, price, copy, take_projected), `upsell` (name, price, anchor_was, oto_structure, take_projected) e `bundles[]` (`{qty, price, label, savings_pct}`). Leia os detalhes de bump/upsell/bundle DESSE bloco. **Fallback legado** (dados.json gerado antes do contrato, sem `aov_levers`): os mesmos detalhes vivem na **Etapa 3 do `offer-builder/offer-builder.md`** (prosa estruturada) — leia de lá; se nem o relatório existir, reconstrua com o membro em vez de inventar. Alavanca `null` no bloco (ex: `"upsell": null`) = a oferta não tem essa alavanca → registre `not_in_offer`, não force. Monte a tabela do que a oferta JÁ definiu vs. o que falta implementar:

| Alavanca | Definido no `offer-builder`? | Valor/spec (fonte) | Caminho Shopify escolhido | Status |
|---|---|---|---|---|
| Post-purchase upsell | `aov_levers.upsell` (fallback: Etapa 3 do offer-builder.md) | nome, preço, take projetado | app / extension / thank-you | a configurar |
| Cart/order bump | `aov_levers.bump` (fallback: Etapa 3 do offer-builder.md) | complemento, preço, copy | tema / extension / app | a configurar |
| Bundles | `aov_levers.bundles[]` + `pricing` (fallback: Etapa 3 do offer-builder.md) | Solo/3/6, savings, Popular | variantes PDP / native_bundle / function / app | a configurar |
| Free-shipping threshold | derivado de `pricing.aov_expected` | threshold = 1.3-1.5× AOV | shipping rate + bar | a configurar |
| Checkout trust | `guarantee` + reviews | tipo de garantia, # reviews | checkout extension / branding / PDP | a configurar |

**O que a loja já tem, antes de preencher a coluna Status:** leia `manifest.storefront` (`product_id`, `variant_ids` por quantidade, `selling_plan_id`, `published_online_store`). A `page-build` já pôs de pé na 6.1b o produto, as variantes de cada tier, a assinatura e os descontos da oferta, e já ligou os IDs à página. Tier que já tem variante entra como `applied`, não como "a configurar"; o que esta skill faz com ele é conferir preço, âncora e rótulo. Tier sem variante é o que falta criar. Sem esse bloco no manifest (loja ausente ou `page-build` não rodou), a tabela segue como está e o `pending_store` do pré-flight decide.

Se uma alavanca não foi definida no `offer-builder` (ex: oferta sem upsell), não a force — registre como `not_in_offer` e siga. Não inventar um upsell que a unit economics não sustenta.

**Gate de Complementaridade (o mesmo gate da `offer-builder`, aplicado às superfícies de checkout):** todo componente de AOV que passar por aqui (bump, upsell, bundle-mate, GWP) já deve ter passado no Gate da `offer-builder` ETAPA 3 — as 4 categorias, nesta ordem de prioridade: **(1) more-of-same** (mais unidades do próprio produto), **(2) consumption chaining** (item consumido JUNTO no mesmo ritual de uso), **(3) aceleração de resultado** (encurta o time-to-result do desejo central), **(4) problema adjacente** (o próximo problema depois do resultado). Se o membro trocar o produto de um bump/upsell NESTA skill (ex: "usa o sérum X no lugar"), re-rode o gate: em qual das 4 categorias o novo componente cai? Nenhuma → reprove e derive candidatos do market research (ritual de uso, desejo central, jornada), como a `offer-builder` faz. Registre a categoria no `dados.json` (`complementarity_category`).

### ETAPA 2 — Pergunta ao membro (APENAS o que é input externo)

Não pergunte estratégia. Pergunte só o que você não consegue inferir:

1. **Apps já instalados?** "Você já tem algum app de upsell/bump/bundle/desconto instalado? Se sim, qual?" — define caminho no-code vs. nativo, E dispara o gate anti-Shopify-Scripts da Alavanca 3 (app legado = desconto que some no checkout).
2. **Gateway de pagamento**: "Qual gateway você usa — Shopify Payments/cartão, ou o checkout é majoritariamente wallet (Apple Pay/Shop Pay/PayPal)?" — post-purchase one-click funciona em qualquer plano, mas o OTO NÃO aparece pra pagamento via wallet; se a loja é wallet-heavy, desconte o take projetado e reforce cart bump/bundle (que não dependem do método de pagamento). Pergunte também se a loja é Plus SÓ se algum caminho escolhido exigir (order bump in-checkout, trust blocks no checkout, custom Function via CLI).
3. **In-box gift?** (só se algum bonus do `offer-builder` for físico/in-box): "O brinde físico vai junto na caixa? Aí é coordenação com fulfillment, não config de loja." — separa o que é config do que é operação.

Para **starter**, default no-code: app único que cobre bump + upsell + bar, ou caminho do tema pros bundles. Não recomendar app pago se o membro tem budget apertado e o caminho nativo resolve.
