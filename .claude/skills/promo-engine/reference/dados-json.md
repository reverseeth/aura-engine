# Promo Engine · Referência: Output schema, o dados.json

> O schema completo do `promo-engine/dados.json` (janela, preparação, oferta, economics, campanhas, briefs, escala, aterrissagem, resultado, cofre sazonal e handoff) e a lista dos campos que a skill nunca preenche por estimativa. Abra ao gravar o `dados.json`.

## Output Schema — `promo-engine/promo-engine.md` + `promo-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills `creative-engine`, `ad-analysis`, `scale-engine`, `retention-engine`, `content-recycler` e `finance-engine`.

```json
{
  "promo_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "currency": "USD",
  "event": "bfcm | holiday_tail | valentines | mothers_day | labor_day | fall_halloween | flash | custom",
  "event_name": "Black Friday Sale 2026",
  "window": {
    "start": "2026-11-02",
    "end": "2026-12-01T00:00:00",
    "ad_account_timezone": null,
    "phases": [
      { "phase": "early_sale | bf_weekend | cyber_monday | holiday_tail", "start": "", "end": "" }
    ]
  },
  "prep": {
    "evergreen_momentum": { "breakthroughs_live": 0, "assessment": "conta com momentum | conta fria — expectativa ajustada" },
    "offer_contrast": { "evergreen_offer": "", "distance_plan": "store_credit_layer | price_up_then_down | degrade_after | ok" },
    "vip_leadgen": {
      "decision": "skip | run",
      "criteria": { "returning_rate": null, "organic_share_high": null, "unique_brand": null },
      "calculator": { "total_spend": null, "cpl_max": null, "aov_vip": null, "cvr_assumed": null, "offer_margin_with_vip_discount": null, "breakeven_roas": null, "projected_leads": null, "projected_revenue": null }
    },
    "inventory": { "source": "sourcing/dados.json", "volume_confirmation_30_60_90": null, "reorder_point_days": null, "fallback": "none | preorder" },
    "ops_backups": { "owner": "ops-engine", "member_has": [], "gaps": [] },
    "site_ready": { "automatic_discount_scheduled": false, "savings_visible_everywhere": false, "qa_done": false, "dev_on_standby": false }
  },
  "offer": {
    "core_type": "percent_off | dollar_off | buy_x_get_x_free | buy_x_gift_x | store_credit | avatar_specific | quiz | free_express_shipping",
    "headline_language_en": "25% off EVERYTHING",
    "stack": [],
    "discount_effective_pct": null,
    "compare_at_math_verified": false,
    "bf_weekend_bonus": null,
    "holiday_tail_offer": null,
    "vip_offer": null,
    "store_credit": { "face_value": null, "real_cost": null, "breakage_assumed_pct": null },
    "sale_reason_declared": ""
  },
  "promo_economics": {
    "status": "computed | blocked_pending_inputs",
    "source_fields": ["manifest.target_cpa | offer-builder/dados.json | member"],
    "aov_expected_full": null,
    "discount_effective_per_order": null,
    "aov_promo": null,
    "margin_per_order_promo": null,
    "margin_rate_promo": null,
    "gross_margin_promo_pct": null,
    "floor_check": "above_60 | between_55_60 | below_55_redesign",
    "breakeven_roas_promo": null,
    "breakeven_cpa_promo": null,
    "target_cpa_promo": null,
    "breakeven_roas_with_fixed_promo": null,
    "kpi_of_the_window": "blended_roas",
    "blended_caveat": "organic_share_high → decidir por click-based/incremental"
  },
  "campaigns": [
    {
      "name": "", "role": "promo_cbo", "ad_sets": ["broad", "warm60", "hot90"],
      "budget_initial_daily": null, "budget_share_of_total_pct": null,
      "created_via": "mcp_official | mcp_pipeboard | manual", "status": "PAUSED",
      "end_rule": { "created": false, "active": false, "fires_at": "" },
      "campaign_id": null, "ad_set_ids": []
    }
  ],
  "creative_brief_08": {
    "priority": ["winner_plus_banner", "product_photo_plus_offer_statics", "seasonal_revival_rebanner", "early_scarcity", "complements"],
    "best_ad_source": "manifest.ad_classification breakthrough | spend_winner | none → statics only",
    "banner_copy_en": "", "subtle_callout_test": true,
    "bfcm_wording_on_friday_creatives": "Black Friday Cyber Monday Sale",
    "batches_planned": "2-3 (~9-12 statics/semana)",
    "revival_candidates": [],
    "handed_off": false
  },
  "email_sms_calendar_13": {
    "phases": [], "send_windows": [], "segments_guidance": "", "creative_by_phase_awareness": "",
    "vip_warmup_flow_included": false, "cutoffs_confirmed_with_ops": false, "handed_off": false
  },
  "scaling_window": {
    "governed_by": ".claude/lib/ad-taxonomy/README.md §5 (exceção a; surf + reset)",
    "attribution_tool": "triple_whale | northbeam | hyros | meta_only_low_spend",
    "surf_cadence_hours": null,
    "period_sheet_timezone": "ad_account",
    "decision_order": "blended_first_then_per_campaign",
    "midnight_resets": [ { "date": "", "spent_real": null, "reset_to": null, "logged_in_ad_log": true } ]
  },
  "landing": {
    "end_rule_fired_or_manual": null, "post_cyber_dip_managed": null,
    "holiday_tail_offer_live": null, "evergreen_budget_restored_to": null,
    "protocol_restart_note": "sazonalidade = new reason (§5 exceção b) — leitura do evergreen reinicia limpa"
  },
  "result": {
    "revenue_window": null, "spend_window": null, "blended_roas_window": null,
    "contribution_margin_window": null, "operating_income_window": null,
    "new_customers": null, "returning_share": null,
    "offer_winner_note": "", "curve_by_day": [],
    "promo_cohort_flagged_for_15": false,
    "next_year_notes": ""
  },
  "seasonal_vault": [
    { "creative_id": "", "period": "bfcm", "revive_month": "novembro", "rebanner_required": true, "note": "" }
  ],
  "handoff": {
    "for_skill_08": ["creative_brief_08"],
    "for_skill_11": ["window", "scaling_window.midnight_resets", "result.curve_by_day"],
    "for_skill_12": ["window", "promo_economics.breakeven_roas_promo", "landing.evergreen_budget_restored_to", "seasonal_vault"],
    "for_skill_13": ["email_sms_calendar_13", "offer", "window.phases"],
    "for_skill_14": ["seasonal_vault"],
    "for_skill_15": ["result.promo_cohort_flagged_for_15", "result.revenue_window", "result.spend_window"]
  },
  "pending_inputs": [],
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

**Campos que a skill NUNCA preenche por estimativa:** `promo_economics.margin_per_order_promo` (e derivados), `prep.vip_leadgen.calculator.offer_margin_with_vip_discount` e `prep.inventory.volume_confirmation_30_60_90`. Faltando, o campo fica `null`, entra em `pending_inputs[]` e o bloco dependente fica bloqueado — nunca preenchido com plausível.
