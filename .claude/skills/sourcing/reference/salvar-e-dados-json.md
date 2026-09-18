# Sourcing · Referência: SALVAR, o relatório, o schema do dados.json e o manifest

> O conteúdo do `sourcing.md` na ordem, o `.html` pelo `render_report.py`, o schema completo do `sourcing/dados.json` e a atualização do manifest pelo script. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**: `mkdir -p workspace/[produto]/sourcing/`.

1. **`workspace/[produto]/sourcing/sourcing.md`** — relatório no report_language: a operação explicada (ETAPA 1), due diligence dos candidatos com o tipo real de cada um, rota do produto com prazo e orçamento, mensagem de cotação pronta, exigências de conformidade da categoria, agentes (se recomendados pro caso), tabela comparativa (quando houver cotações), o plano de condições de pagamento, os contratos a assinar antes de produzir, o plano de qualidade com a matemática do defeito nos números do membro, as decisões de embalagem, o calendário com as datas-limite, e a decisão com os próximos passos. Segue `.claude/rules/report-only-results.md`.
2. **`workspace/[produto]/sourcing/sourcing.html`** — companion gerado com `python3 tools/render_report.py workspace/[produto]/sourcing/sourcing.md` (nunca escrito à mão).
3. **`workspace/[produto]/sourcing/dados.json`**:

```json
{
  "product_slug": "",
  "status": "quoting|samples|closed",
  "category": "skincare|supplement|electronics|apparel|pet|home|other",
  "product_route": "ready_stock_white_label|custom_formula|odm",
  "suppliers": [
    {
      "name": "", "channel": "alibaba|1688|private|us_manufacturer|agent|trade_show|public_database|linkedin",
      "supplier_type": "factory|trade_company|dropshipping_agent|sourcing_company|unknown",
      "type_evidence": "", "factory_size": "small|medium|large|unknown",
      "contact": "", "wechat_ok": false,
      "unit_cost": 0, "moq": 0, "incoterm": "EXW|FOB|DDP|DDU_DAP",
      "ddp_to_3pl": 0, "lead_time_days": 0, "slowest_component": "", "slowest_component_days": 0,
      "payment_terms_offered": "",
      "spec_confirmed": false, "bom_provided": false,
      "compliance": { "gmp_gmpc": false, "coa_per_batch": false, "third_party_lab": "", "category_tests": [], "certificate_verified": false },
      "sample": { "label": "", "received": false, "verdict": "" },
      "role": "start|scale|discarded", "red_flags": [], "notes": ""
    }
  ],
  "chosen_supplier": "",
  "logistics_route": "ddp_to_3pl|dropship_direct|fba|home",
  "three_pl": { "provider": "", "pick_pack_per_order": 0, "shipping_to_customer_per_order": 0, "storage_monthly": 0, "payment_terms": "" },
  "landed_cost_per_unit": 0,
  "landed_cost_includes_duty": true,
  "target_price_declared": 0,
  "payment_terms": {
    "model": "standard_30_70|30_40_30|rolling_deposit|pay_as_you_ship|line_of_credit",
    "deposit_pct": 0, "balance_trigger": "", "net_days": 0,
    "incoterm_clock": "EXW|FOB|DDP", "effective_days_including_transit": 0,
    "never_100_upfront_confirmed": false, "next_threshold_to_unlock": ""
  },
  "quality": {
    "golden_sample_signed": false, "qc_chain": { "sub_vendor_oqc": false, "iqc": false, "inline": false, "final": false },
    "third_party_qc": false, "inspection_pct": 0, "report_before_balance_payment": false,
    "go_no_go_criteria": "", "aql_in_contract": false,
    "defect_rate_assumption": 0, "defect_rate_basis": "benchmark|measured",
    "defect_split": { "replacement_pct": 0, "refund_pct": 0 },
    "defect_provision_per_order": 0,
    "warranty_policy": ""
  },
  "contracts": { "msa": false, "brand_authorization_letter": false, "ip_agreement_before_design": false, "production_waiver": false },
  "packaging": { "decoration": "label_wrap|direct_print", "print_effects": [], "travel_element": false, "print_ready_files_ok": false, "cost_per_unit": 0 },
  "calendar": { "cny_exposure": "none|watch|critical", "order_by_date": "", "supplier_shutdown_window": "", "reorder_point_days": 0, "volume_confirmation_30_60_90": "" },
  "cogs_payload_for_04": {
    "product_delivered": 0, "shipping_to_customer": 0, "pick_pack": 0, "taxes_and_duties": 0,
    "refund_chargeback_provision_floor": 0,
    "fields_not_owned_here": ["payment_processing", "subscription_app_fee", "agency_fee_variable"]
  },
  "quote_message_sent_at": "",
  "pending_from_supplier": []
}
```

**Atualize o manifest pelo script** (nunca editar o JSON à mão): `python3 tools/manifest.py <slug> complete sourcing` (só quando `status: "closed"`), `python3 tools/manifest.py <slug> set cogs_estimate <soma das linhas de domínio do sourcing>` (quando fechada; o script faz backup e grava `updated_at`), e regenere o painel (`python3 .claude/lib/workspace-index/build_index.py <slug>`).
