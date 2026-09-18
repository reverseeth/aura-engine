# Marketplace Engine · Referência: Output schema, o dados.json

> O schema completo do `marketplace-engine/dados.json` (gate com os sinais, canais avaliados e abertos, fees e comissões, métricas por canal, pendências e handoff). Abra ao gravar o `dados.json`.

## Output Schema — `marketplace-engine/marketplace-engine.md` + `marketplace-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills `scale-engine`, `retention-engine`, `finance-engine` e `creator-engine`.

```json
{
  "marketplace_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "run_type": "evaluation | status_update",
  "gate": {
    "meta_site_proven": null,
    "proof_source": "manifest.ad_classification | finance-engine | member_declared | none",
    "signals": {
      "brand_search_rising": null,
      "customers_asking_marketplace": null,
      "resellers_or_hijack_detected": null,
      "cross_channel_lift_observed": null
    },
    "anti_signal_flight_from_meta": false,
    "verdict": "expand | not_yet | blocked_pending_proof",
    "verdict_reason": "frase em report_language com o sinal decisivo",
    "next_review_trigger": "ex.: busca de marca no Search Console > X/mês, ou 1º breakthrough na `ad-analysis`"
  },
  "channels": [
    {
      "channel": "amazon",
      "verdict": "go | no_go | not_yet | not_evaluated",
      "reasons": [],
      "entry_requirements": {
        "trademark_registered": null,
        "brand_registry_active": null,
        "reviews_plan_defined": null,
        "fulfillment": "fba | fbm | undefined"
      },
      "fees_and_commissions": {
        "referral_fee_pct": null,
        "custom_link_fee_pct": null,
        "fulfillment_cost_per_order": null
      },
      "status": "not_evaluated | preparing | live | paused",
      "metrics": { "revenue_monthly": null, "tacos_pct": null, "ltv_to_cac": null, "organic_share_pct": null },
      "owner": "member | agency | specialist | undefined",
      "opened_at": null
    },
    {
      "channel": "tiktok_shop",
      "verdict": "go | no_go | not_yet | not_evaluated",
      "reasons": [],
      "commission_organic_pct": null,
      "commission_ads_pct": null,
      "samples_policy": null,
      "bootstrap_plan": null,
      "status": "not_evaluated | preparing | live | paused",
      "metrics": { "gmv_monthly": null, "active_affiliates": null, "effective_commission_pct": null, "brand_search_in_platform": null },
      "content_dependency": "creator-engine",
      "opened_at": null
    },
    {
      "channel": "affiliate_program",
      "verdict": "go | no_go | not_yet | not_evaluated",
      "reasons": [],
      "paid_recruitment": { "active": null, "recruitment_offer": null, "recruitment_roas": null },
      "customer_affiliates": { "active": null, "enrollment": "thank_you_page_auto | manual | none" },
      "commission_ladder": [
        { "tier": "primeiros_usd", "up_to_usd": 10000, "pct": 10 },
        { "tier": "faixa_2", "up_to_usd": null, "pct": 5 },
        { "tier": "faixa_3", "up_to_usd": null, "pct": 2.5 },
        { "tier": "acima", "up_to_usd": null, "pct": 1 }
      ],
      "commission_base": "revenue | ad_spend | undefined",
      "monthly_cap_usd": null,
      "attribution": "per_affiliate_link_or_code | undefined",
      "status": "not_evaluated | preparing | live | paused",
      "metrics": { "affiliate_gmv_share_pct": null, "program_roi": null },
      "opened_at": null
    }
  ],
  "sequence_recommendation": [],
  "out_of_scope_redirects": [
    { "request": "portar campanha pra AppLovin/Axon/TikTok Ads", "goto": "content-recycler (Movimento 4)" }
  ],
  "handoff": {
    "for_skill_15": ["channels[].fees_and_commissions", "channels[].commission_organic_pct", "channels[].commission_ladder"],
    "for_skill_16": ["channels[tiktok_shop].commission_organic_pct", "channels[tiktok_shop].samples_policy", "channels[tiktok_shop].metrics.gmv_monthly"],
    "for_skill_12": ["gate.verdict", "channels[].status"],
    "for_skill_13": ["amazon buyer list anual (cross-match de email)", "compradores de marketplace pro ecossistema de email/SMS"]
  },
  "pending_inputs": [],
  "sanity_checks": { "total": 8, "passed": 8, "failed": [] }
}
```

Os valores do exemplo (escada de comissão inclusive) são o default da fonte — ajuste às faixas reais que o membro definir.
