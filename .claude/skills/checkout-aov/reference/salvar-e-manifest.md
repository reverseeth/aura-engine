# Checkout & AOV · Referência: SALVAR, o schema do dados.json e o manifest

> O conteúdo do relatório com a seção de configuração da loja, o dual output com as convenções, o schema do `checkout-aov/dados.json` com as notas de `store_config`, `aov_reconciliation` e `levers.bundles.tiers`, e a atualização do manifest pelo script. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

Salvar em `workspace/[produto]/`:

**`checkout-aov/checkout-aov.md`** (humano) contendo:
1. Mapa das 5 alavancas: definida no `offer-builder`? caminho Shopify? status (aplicada/pending/not_in_offer) + categoria do Gate de Complementaridade
2. Spec de cada alavanca ativa (pricing com charm, copy real, caminho técnico, onde aplicar/config spec do app, aceitação projetada)
3. Reconciliação de AOV (sem alavancas → projeção do `offer-builder` → ajustes de escopo, se houver) + o target CPA que vale pra Skill `ad-strategy` (explicitando: "2×" = 2× o ROAS de breakeven, metade da margem vira lucro)
4. Resultado do check anti-Scripts (se houve app instalado)
5. Passos de aplicação (tema / admin / app / recipe nativa) e o que ficou pending
6. Seção **"Configuração da loja"**: o que esta rodada criou na loja, o que já existia e foi conferido, e o que o membro precisa abrir no admin (cada item com o que fazer lá e o que ele destrava)

**`checkout-aov/checkout-aov.html`** (companion humano) — gerado com `python3 tools/render_report.py workspace/[produto]/checkout-aov/checkout-aov.md` (nunca escrito à mão). No `.md`: tabela `KPI | Valor` pro AOV antes/depois, tabela normal pro mapa de alavancas, citações `**Atenção:**`/`**Nota:**`/`**Risco:**` pros gates (convenções em `.claude/templates/aura-html-components.md`). Ícones SVG, nunca emoji, em qualquer preview de checkout/cart consumidor-final (regra 7).

**`checkout-aov/dados.json`** (estruturado; o contrato com a Skill `ad-strategy` passa pelo MANIFEST — `aov_baseline`/`target_cpa` — e as recipes de automação leem `levers.bundles.tiers` daqui):

```json
{
  "product_slug": "<do manifest>",
  "store_url": "<do manifest ou null>",
  "theme_id": "<manifest.storefront.theme_id ou null>",
  "applied_to_store": false,
  "pending_store": false,
  "levers": {
    "post_purchase_upsell": { "active": true, "path": "app|extension|thankyou", "app": "reconvert|aftersell|zipify_ocu|rebuy|null", "complementarity_category": "more_of_same|consumption_chaining|result_acceleration|adjacent_problem", "price": 49, "anchor_was": 79, "take_projected": 0.08, "oto_structure": "more_of_same|next_thing|do_it_faster|need_help", "status": "applied|pending|not_in_offer" },
    "cart_bump": { "active": true, "path": "theme|extension|app", "complementarity_category": "consumption_chaining", "price": 17, "take_projected": 0.20, "status": "applied" },
    "bundles": { "active": true, "path": "pdp_variants|native_bundle|function|app", "tiers": [{ "qty": 1, "price": 49 }, { "qty": 3, "price": 119, "label": "Popular" }, { "qty": 6, "price": 199, "label": "Best Value" }], "psychology": ["extremeness_aversion", "decoy", "charm_pricing"], "status": "applied" },
    "free_shipping_threshold": { "active": true, "threshold": 75, "path": "shipping_rate+bar", "status": "applied" },
    "checkout_trust": { "active": true, "path": "pdp_trust_row|checkout_extension|branding", "guarantee": "90-day money-back", "review_count": 2300, "status": "applied" }
  },
  "store_config": {
    "created": [{"what": "tarifa de frete grátis acima de $75", "where": "configurações de envio"}],
    "already_existed": [{"what": "app de upsell instalado", "where": "admin, Apps", "checked": true}],
    "member_review": [{"what": "colar o config spec do upsell no painel do app", "where": "admin, app de upsell", "unlocks": "o upsell pós-compra roda"}],
    "cart_surface": {"applied": false, "theme_id": null, "checks_passed": 0, "checks_total": 6}
  },
  "aov_reconciliation": {
    "aov_no_levers": 97.00,
    "aov_projected_04": 118.00,
    "scope_diff": [],
    "aov_final": 118.00,
    "weighted_margin_final": 72.00,
    "target_cpa_2x_breakeven_multiple": 36.00,
    "target_cpa_3x_breakeven_multiple": 24.00,
    "manifest_updated": false
  }
}
```

Notas do schema:
- `aov_reconciliation` substitui a antiga "projeção nova": no caso normal (alavancas = as que o `offer-builder` projetou), `aov_final == aov_projected_04` e `scope_diff` fica vazio — o delta é ≈ 0 por definição (ETAPA 4) e `manifest_updated: false`. Só quando `scope_diff` lista alavancas que entraram/saíram fora do plano do `offer-builder` é que `aov_final`/`weighted_margin_final` divergem e o manifest é atualizado.
- Os campos `target_cpa_*_breakeven_multiple` seguem a convenção do `offer-builder`/`ad-analysis`: margem final ÷ N — múltiplo do ROAS de BREAKEVEN, não ROAS literal.
- `levers.bundles.tiers` (`{qty, price, label}`) é o contrato lido pelas recipes `deploy-shopify-product.md` e `create-fixed-bundles.md`.
- `store_config` é o registro do que esta skill mexeu na loja, nas mesmas três listas que a `page-build` usa no `deploy-report.json`, para o membro ler um estado só da loja em vez de descobrir buraco no dia do lançamento. `cart_surface.checks_total` é 6, os seis testes de `reference/carrinho-e-drawer.md`; a superfície só entra como aplicada com os seis verdes.

Atualizar o manifest pelo script (nunca editar o JSON à mão): `python3 tools/manifest.py <slug> complete checkout-aov`; se aplicado de fato na loja, `python3 tools/manifest.py <slug> set aov_baseline <aov_final>` e — SÓ se `scope_diff` não-vazio — `python3 tools/manifest.py <slug> set target_cpa <n> breakeven_roas <n>` (a Skill `ad-strategy` lê do manifest). Não sobrescrever `offer-builder/dados.json`.

Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html), onde `<slug>` é o `product_slug`.
