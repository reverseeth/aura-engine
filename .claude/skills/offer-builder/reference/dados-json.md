# Offer Builder · Referência: Output schema do offer-builder.md e do dados.json

> O schema completo do `offer-builder/dados.json`, as notas de cada bloco de economia unitária, a atualização do manifest pelo `tools/manifest.py`, a nota sobre nomenclatura dos `unit_economics`, o enum canônico de `bonuses[]` e o contrato `aov_levers` com a `checkout-aov`. Abra ao gravar.

### Output Schema — `offer-builder/offer-builder.md` + `offer-builder/dados.json`

O markdown é humano; o JSON é para as skills `copy-engine`, `page-design`, `ad-strategy`, `ad-analysis` e `scale-engine`. Estrutura obrigatória:

## O `resumo`, o bloco que a próxima fase lê primeiro

O `dados.json` abre com um objeto `resumo`: até doze campos curtos com o que a fase seguinte precisa saber de primeira, sem abrir o arquivo inteiro. Ele não guarda dado novo, é espelho do que já está mais abaixo: cada campo copia o valor literal do campo de origem, e onde diverge, o campo de origem vence. Preencha por último, depois que o resto do arquivo estiver fechado.

`.json`:
```json
{
  "resumo": {
    "mechanism_name": "o nome literal do mecanismo",
    "mechanism_one_line": "o que ele faz, em uma frase",
    "price_main": 0,
    "aov_expected": 0,
    "guarantee_line": "a garantia como o cliente lê",
    "offer_stack_lines": ["cada item do stack em meia linha"],
    "bonuses_names": ["nome de cada bônus"],
    "margin_per_order": 0,
    "breakeven_roas": 0,
    "target_cpa": 0,
    "subscription_model": "o modelo de assinatura em meia linha",
    "budget_viability_verdict": "viável | apertado | inviável"
  },
  "offer_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "mechanism": {
    "name": "...",
    "ump": { "name": "nome próprio do mecanismo do problema", "logic": "por que as soluções atuais falham (report_language; cita claim_ids da research foundation)" },
    "ums": { "name": "nome próprio do mecanismo da solução", "logic": "por que a nossa entrega funciona (report_language; cita claim_ids)" },
    "sin_score": { "simplicity": 9, "intuitiveness": 8, "novelty": 7 },
    "validation_source": "improved_validated|crossed_validated|original",
    "copy_left_to_skill_06": true
  },
  "pricing": {
    "main_sku_price": 97.00,
    "aov_expected": 118.00,
    "currency": "USD"
  },
  "subscription_architecture": "subscription_first | onetime_plus_sub_no_reorder | no_subscription",
  "onetime_premium_pct": 15,
  "sub_discount_pct": 0,
  "cogs_breakdown": {
    "product_delivered": 18.00,
    "shipping_to_customer": 6.50,
    "pick_pack": 2.50,
    "payment_processing": 3.50,
    "taxes_and_duties": 1.50,
    "subscription_app_fee": 0.90,
    "agency_fee_variable": 0.00,
    "refund_chargeback_provision": 2.10
  },
  "unit_economics": {
    "basis": "first_order",
    "cac_basis": "shopify_new_customer",
    "margin_per_unit": 58.50,
    "weighted_margin_per_order": 72.00,
    "contribution_margin_pct": 61.0,
    "breakeven_cpa": 72.00,
    "breakeven_roas": 1.64,
    "target_cpa_for_2x": 36.00,
    "target_cpa_for_3x": 24.00,
    "target_cpa_primary_2x": 36.00,
    "target_cpa_primary_3x": 24.00,
    "psm_theoretical": 1.44,
    "repeat_order": {
      "aov": 97.00,
      "variable_costs_total": 32.00,
      "contribution_margin_per_order": 65.00,
      "contribution_margin_pct": 67.0
    },
    "aov_blended": 108.00
  },
  "guarantee": { "type": "...", "duration_days": 30 },
  "offer_stack": "Main product ($97 value) + Bonus 01 ($49 value) + Bonus 02 ($39 value) + Bonus 03 ($29 value) = $214 total value. Today: $97 (you save $117).",
  "aov_levers": {
    "bump": { "name": "...", "price": 14.00, "copy": "1 frase + 1 benefício (inglês US)", "take_projected": 0.20 },
    "upsell": { "name": "...", "price": 67.00, "anchor_was": 97.00, "oto_structure": "more_of_same | next_thing | do_it_faster | need_help", "take_projected": 0.08 },
    "bundles": [
      { "qty": 1, "price": 97.00, "label": "Solo", "savings_pct": 0 },
      { "qty": 3, "price": 197.00, "label": "Popular", "savings_pct": 32 },
      { "qty": 6, "price": 327.00, "label": "Best Value", "savings_pct": 44 }
    ]
  },
  "bonuses": [
    {
      "id": "bonus-01",
      "name": "o ativo nomeado (regra do Not: \"___\", ETAPA 3) — nunca a palavra de formato",
      "description": "o que é / por que vale",
      "value_anchored": 49,
      "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
      "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
      "condition": "unconditional | cart_threshold | tier_specific",
      "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
    }
  ],
  "budget_viability": {
    "cac_ref": 45.00,
    "fixed_costs_monthly": null,
    "fixed_costs_source": "member | manifest | finance-engine | unknown",
    "contribution_margin_pct_measured": null,
    "payback_window_days_measured": null,
    "scenarios": [
      { "daily_budget": 50, "new_customers_per_day": 1.1, "contribution_margin_per_day": 12.00, "monthly_spend": 1500, "new_customers_per_month": 33, "contribution_margin_per_month": 360, "result_after_fixed_monthly": null },
      { "daily_budget": 100, "new_customers_per_day": 2.2, "contribution_margin_per_day": 24.00, "monthly_spend": 3000, "new_customers_per_month": 66, "contribution_margin_per_month": 720, "result_after_fixed_monthly": null }
    ],
    "caveats": "margem de contribuição não é lucro (custos fixos não informados, portanto não descontados); conta só a 1ª compra; CAC tende a subir com o investimento (2× = estimativa de mesma eficiência)",
    "verdict": "..."
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo acima são ILUSTRATIVOS e independentes entre si** — servem pra mostrar o formato de cada campo, não pra compor um caso econômico coerente único. Não re-derive um campo a partir de outro usando os valores do exemplo; as fórmulas canônicas estão na "Nota sobre nomenclatura" abaixo e nas ETAPAs 5-7. (`onetime_premium_pct` só existe quando `subscription_architecture` ≠ `no_subscription`; `repeat_order` é `null` quando o produto não tem recompra prevista, e `aov_blended` só existe quando `repeat_order` existe.)

**Campos de economia unitária — o que cada um significa (cânone: `.claude/lib/unit-economics/README.md`):**
- `cogs_breakdown` traz o stack de custos variáveis item a item (§1). **Todo campo do bloco é valor em dinheiro POR PEDIDO, nunca percentual solto** — a Skill `ad-analysis` SOMA os valores deste bloco pra obter o COGS canônico, e um percentual no meio da soma corromperia o número. Fee que nasce como % (pagamento, app de assinatura, agência) entra aqui já convertido pro valor do pedido médio. `subscription_app_fee` = 0 quando não há assinatura; `agency_fee_variable` = 0 quando a agência cobra valor fixo (aí ela é custo FIXO e vai em `budget_viability.fixed_costs_monthly`) ou quando não há agência. **Ad spend nunca entra aqui** — ele é o CAC do PSM.
- `unit_economics.basis: "first_order"` declara que todos os campos canônicos do bloco (margem, breakeven, tetos de CAC, PSM, `contribution_margin_pct`) são do PRIMEIRO PEDIDO. A economia da recompra vive só em `repeat_order` — com o próprio `contribution_margin_pct` dela —, e nenhum derivado de mídia sai de lá (§2).
- `unit_economics.cac_basis: "shopify_new_customer"` declara que o custo de aquisição do modelo é CAC por cliente novo medido no Shopify (`new customer = TRUE`), não o CPA que a plataforma de ads reporta (§3). Os campos mantêm o nome `*_cpa_*` por contrato com as skills `checkout-aov`/`ad-strategy`/`ad-analysis` — o nome é legado, o conteúdo é CAC.
- `budget_viability` não tem nenhum campo chamado "profit". `contribution_margin_per_day/month` é margem de contribuição; `result_after_fixed_monthly` é o único número que pode ser chamado de lucro, e é `null` enquanto `fixed_costs_monthly` for `null` (§1).
- `contribution_margin_pct_measured` e `payback_window_days_measured` são **cópias** do `finance-engine/dados.json` (`monthly_model.contribution_margin_pct` e `payback.payback_window_days_measured`) — esta skill lê, nunca calcula nem estima. Ficam `null` quando a `finance-engine` não rodou, e nesse estado a ETAPA 8 e o check 8 operam exatamente como antes. `fixed_costs_source` registra de onde veio o número dos fixos.

Atualizar o manifest pelo script (nunca editar o JSON à mão): `python3 tools/manifest.py <slug> set target_cpa <n> breakeven_roas <n> psm_theoretical <n>` e depois `python3 tools/manifest.py <slug> complete offer-builder` (valida o `offer-builder/dados.json` contra `.claude/templates/schemas/offer-builder.dados.schema.json` antes de marcar; faz backup e grava `updated_at`).

Depois de atualizar o manifest, regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza o `ABRIR-AQUI.html`).

**Nota sobre nomenclatura dos unit_economics** — `weighted_margin_per_order` é o denominador de margem CANÔNICO de toda a unit economics. TODOS os derivados saem dele, NÃO de `margin_per_unit`:
- `breakeven_cpa` = `weighted_margin_per_order`
- `target_cpa_primary_2x` = `weighted_margin_per_order / 2`
- `target_cpa_primary_3x` = `weighted_margin_per_order / 3`
- `breakeven_roas` = `aov_expected / weighted_margin_per_order`
- Sanidade: `target_cpa_primary_2x` < `breakeven_cpa` SEMPRE.

No exemplo acima: weighted_margin_per_order 72 → breakeven_cpa 72, target_2x 36 (72/2), target_3x 24 (72/3), breakeven_roas 1.64 (118/72), psm_theoretical 1.44 (118/(36+46), COGS = somatório do breakdown). A Skill `ad-analysis` lê por esses nomes "primary"/"weighted" e assume esse denominador único. Os campos legacy (`margin_per_unit`, `target_cpa_for_2x/3x`, `sub_discount_pct`) são emitidos em paralelo só por compat — `sub_discount_pct` sai SEMPRE `0` desde a inversão do desconto de assinatura (ETAPA 3); o número vivo é `onetime_premium_pct`. `weighted_margin_per_order` = margem média ponderada por AOV (considera bumps + upsells); `margin_per_unit` é a margem unitária do SKU principal. Se a oferta não tem bump/upsell, os dois valores são iguais — mas os derivados de CPA sempre referenciam `weighted_margin_per_order`. `offer_stack` é a string pré-montada que a Skill `copy-engine` consome literal em copy de página/ad — é copy pública: SEMPRE inglês US (é estrutura de oferta com valores, não copy de mecanismo — a copy do mecanismo nasce inteira na Skill `copy-engine` a partir de `ump`/`ums`).

**Enum canônico de `bonuses[]`:** os valores de `type`, `format_hint`, `condition` e `delivery_trigger` do schema acima são o enum ÚNICO do framework — reproduzidos idênticos na ETAPA 3 desta skill e no pré-flight da Skill `bonus-delivery`. Não criar valores fora dessa lista.

**Bloco `aov_levers` (contrato machine-readable com a `checkout-aov`):** espelha ESTRUTURADO o que a ETAPA 3 define em prosa — bump (nome, preço, copy curta, take projetado), upsell (nome, preço, âncora "was", estrutura de OTO, take projetado) e os tiers de bundle (`{qty, price, label, savings_pct}`). A Skill `checkout-aov` lê DAQUI na ETAPA 1 dela (fim do parsing de prosa; a prosa da ETAPA 3 continua sendo a versão humana). Alavanca que a oferta não tem = campo `null` (ex: oferta sem upsell → `"upsell": null`) — a `checkout-aov` registra como `not_in_offer`, nunca inventa. `take_projected` em fração (0.20 = 20%), consistente com as taxas conservadoras da ETAPA 3. `copy` do bump é consumidor-final: inglês US, direta e sem aviso (rule 8b).

**Se `offer-builder/dados.json` falhar validação, NÃO salvar `.md`.**
