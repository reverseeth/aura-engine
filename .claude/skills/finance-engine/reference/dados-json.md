# Finance Engine · Referência: Output schema, o dados.json

> O schema completo do `finance-engine/dados.json` com as notas sobre os números ilustrativos, os campos que nunca se estimam e a nomenclatura do cânone. Abra ao gravar o `dados.json`.

## Output Schema — `finance-engine/finance-engine.md` + `finance-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills `offer-builder`, `ad-strategy`, `ad-analysis`, `scale-engine` e `retention-engine`.

```json
{
  "finance_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "currency": "USD",
  "mode": "A_plan | B_measure",
  "mode_reason": "sem mês fechado com ad spend e clientes novos do Shopify",
  "closed_months_available": 0,
  "inputs": {
    "aov_first_order": 118.00,
    "aov_repeat_order": 97.00,
    "aov_blended": 108.00,
    "orders_monthly": 0,
    "cogs_breakdown_source": "offer-builder/dados.json",
    "variable_cost_stack": {
      "product_delivered": 18.00,
      "shipping_to_customer": 6.50,
      "pick_pack": 2.50,
      "payment_processing": 3.50,
      "taxes_and_duties": 1.50,
      "subscription_app_fee": 0.90,
      "agency_fee_variable": 0.00,
      "refund_chargeback_provision": 2.10
    },
    "fixed_costs_monthly": null,
    "fixed_costs_source": "member | manifest | offer-builder | unknown",
    "fixed_costs_breakdown": {},
    "ad_spend_monthly": null,
    "new_customers_period": null,
    "period_days": 30,
    "cac_real": null,
    "cac_basis": "shopify_new_customer",
    "returning_customer_pct": null,
    "cash_available": null,
    "payout_lag_days": null,
    "payout_lag_source": "member | conservative_new_store_default"
  },
  "monthly_model": {
    "revenue": 0,
    "cogs_fully_loaded": 0,
    "gross_profit": 0,
    "gross_margin_pct": 0,
    "variable_costs_total": 0,
    "contribution_margin": 0,
    "contribution_margin_pct": 0,
    "fixed_costs_monthly": null,
    "operating_income": null,
    "operating_income_status": "not_computable_fixed_costs_missing | computed",
    "gross_margin_needed_to_exist": null,
    "revenue_at_gross_margin_to_exist": null,
    "revenue_to_cover_fixed": null,
    "fixed_cost_coverage_ratio": null
  },
  "first_vs_repeat": {
    "first_order": { "aov": 118.00, "variable_costs_total": 0, "contribution_margin": 0, "contribution_margin_pct": 0 },
    "repeat_order": { "aov": 97.00, "variable_costs_total": 0, "contribution_margin": 0, "contribution_margin_pct": 0 },
    "note": "o primeiro pedido carrega o CAC inteiro e os fees atrelados a spend; a recompra não carrega nenhum dos dois"
  },
  "cac": {
    "cac_real": null,
    "cac_floor_reference_usd": [15, 25],
    "cac_max_first_order": 72.00,
    "target_cpa_from_04": { "primary_2x": 36.00, "primary_3x": 24.00 },
    "target_reachable_vs_floor": "yes | no | unknown",
    "first_order_profitable": null,
    "aov_supports_paid_traffic": true,
    "barometer_order_of_attack": ["cac", "ltv", "cogs", "aov"]
  },
  "roas_spiral": {
    "margin_rate": 0.61,
    "breakeven_roas_variable_only": 1.64,
    "breakeven_roas_with_fixed": null,
    "current_roas": null,
    "current_ad_spend_monthly": null,
    "spend_to_breakeven_with_fixed": null,
    "roas_above_variable_breakeven": null,
    "cut_spend_recommendation_allowed": false,
    "verdict": "blocked_pending_fixed_costs | covers_fixed_costs | scale_up_accept_lower_roas | cut_spend_below_variable_breakeven",
    "explanation": "frase em report_language explicando a decisão com os números do membro"
  },
  "cash": {
    "days_covered_target": 90,
    "cash_needed_90d": null,
    "cash_needed_90d_with_float_stack": null,
    "cash_available": null,
    "runway_months": null,
    "float_stack": {
      "active": false,
      "invoicing_net_days": null,
      "bill_pay_fee_pct": null,
      "charge_card_net_days": null,
      "statement_credit_pct": null,
      "total_float_days": null,
      "net_cost_pct": null,
      "cash_out_date": null
    },
    "guardrails_acknowledged": [
      "cash_out_date_known",
      "float_does_not_fix_broken_offer",
      "debt_not_faster_than_fulfillment",
      "no_financing_operational_chaos"
    ],
    "verdict": "..."
  },
  "levers": {
    "baseline": { "aov": 0, "cac": null, "ad_spend_monthly": null, "returning_pct": null },
    "simulations": [
      { "lever": "aov | cac | ad_spend | returning_pct", "from": 0, "to": 0,
        "contribution_margin_delta": 0, "operating_income_delta": null, "rank": 1 }
    ],
    "highest_impact_lever": null
  },
  "cohorts": {
    "source": "lifetimely | triple_whale | shopify_manual | member_pasted | none",
    "aov_month_0": null,
    "ltv_pct_by_month": [],
    "decay_factor": null,
    "decay_source": "calculated | assumed",
    "months_of_actuals": 0,
    "calibrated": false,
    "revenue_by_month": [],
    "margin_by_month": [],
    "total_margin_by_month": [],
    "crossover_month": null,
    "churn_spike_day": null,
    "sensitivity_note": "erro de 5% no cohort pode inverter o sinal do resultado; enquanto não calibrado, payback é modelado no mês 2"
  },
  "payback": {
    "window_days_target": 90,
    "payback_window_days_measured": null,
    "modeled_with_safety_margin": true,
    "cac_increase_ratio_reference": "4:1",
    "cac_increase_per_1k_spend": null,
    "scale_ceiling_monthly_spend": null,
    "scale_ceiling_note": null
  },
  "banking_sheet": {
    "cadence": "weekly",
    "columns": ["date", "cash_in", "business_expense", "payroll", "ad_spend", "investment", "partner_draw", "personal_expense", "net_cash_flow"],
    "template_path": "finance-engine/banking-sheet.csv",
    "last_reconciled": null
  },
  "stress_test": [
    { "scenario": "cac_plus_20pct", "contribution_margin": 0, "operating_income": null, "survives": null },
    { "scenario": "ltv_minus_20pct", "contribution_margin": 0, "operating_income": null, "survives": null },
    { "scenario": "cogs_plus_5pts", "contribution_margin": 0, "operating_income": null, "survives": null },
    { "scenario": "refund_plus_2pts", "mode_b_only": true, "contribution_margin": 0, "operating_income": null, "survives": null },
    { "scenario": "processor_payout_delay_7_14d", "mode_b_only": true, "contribution_margin": 0, "operating_income": null, "survives": null }
  ],
  "benchmarks": {
    "gross_margin_pct": { "actual": 0, "reference": 70, "status": "ok | below | above | unknown" },
    "contribution_margin_pct": { "actual": 0, "reference": "10-20", "status": "..." },
    "fixed_costs_pct_of_revenue": { "actual": null, "reference": "<10", "status": "unknown" },
    "cogs_pct_of_revenue": { "actual": 0, "reference": "<=30", "status": "..." },
    "four_quarter_accounting": { "cogs_pct": 0, "fixed_costs_pct": null, "acquisition_pct": 0, "operating_result_pct": null }
  },
  "monthly_notes": [
    { "month": "2026-08", "event": "ruptura de estoque", "effect": "spend cortado 12 dias; CAC do mês não é comparável" }
  ],
  "decision_memo": {
    "why": null, "what": null, "how": null, "now_next": null
  },
  "pending_inputs": [],
  "handoff": {
    "for_skill_11": ["roas_spiral.breakeven_roas_with_fixed", "roas_spiral.cut_spend_recommendation_allowed", "roas_spiral.verdict", "roas_spiral.spend_to_breakeven_with_fixed"],
    "for_skill_12": ["cash.cash_needed_90d", "cash.float_stack.total_float_days", "cash.runway_months", "monthly_model.fixed_costs_monthly", "payback.scale_ceiling_monthly_spend", "roas_spiral.cut_spend_recommendation_allowed"],
    "for_skill_04": ["monthly_model.fixed_costs_monthly", "payback.payback_window_days_measured", "monthly_model.contribution_margin_pct", "cash.runway_months"],
    "for_skill_13": ["cohorts.ltv_pct_by_month", "cohorts.decay_factor", "cohorts.crossover_month", "cohorts.churn_spike_day"],
    "for_skill_10": ["cac.cac_floor_reference_usd", "cac.cac_max_first_order", "cac.target_reachable_vs_floor"]
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo são ILUSTRATIVOS e independentes entre si** — mostram o formato de cada campo, não compõem um caso econômico coerente. Não re-derive um campo a partir de outro usando os valores do exemplo; as fórmulas canônicas estão nas ETAPAs 2, 5, 6 e 9.

**Campos que a skill NUNCA preenche por estimativa:** `inputs.fixed_costs_monthly`, `inputs.cac_real` e `inputs.new_customers_period`. Faltando qualquer um, o campo fica `null`, entra em `pending_inputs[]`, e todo bloco derivado dele fica marcado como não calculável — nunca preenchido com plausível. `cohorts.ltv_pct_by_month` segue a mesma regra: sem série real, `decay_source: "assumed"` e `calibrated: false`, declarados.

**Nomenclatura (cânone §1):** nenhum campo deste schema chama-se "profit". `contribution_margin` é margem de contribuição; `operating_income` é o único que pode ser chamado de lucro, e é `null` enquanto `fixed_costs_monthly` for `null`.

**Se `finance-engine/dados.json` falhar as checagens da ETAPA 14, NÃO salvar o `.md`.**
