# Scale Engine · Referência: SALVAR, schema do dados.json e atualização do manifest

> O texto integral da seção SALVAR: o conteúdo do `scale-engine.md` seção a seção, o `scale-directives.md`, as linhas do ad-log, o schema completo do `dados.json` com as notas de cada bloco (`abo_promotions[]`, campos que nunca se estimam, campos que só existem com a `finance-engine`) e os campos do manifest gravados por `tools/manifest.py`. Abra ao gravar.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `scale-engine.md` → `scale-engine.html`). **Isentos** (arquivos operacionais de handoff — rule 6b do CLAUDE.md, lista completa em `.claude/lib/workspace-index/workspace-layout.md`): `scale-directives.md`, `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/scale-engine/` antes de salvar.

Outputs em `workspace/[produto]/scale-engine/`:

- `scale-engine.md` contendo:
  1. Classificação de estágio + sub-fase de escala (Etapa 2)
  2. Análise de prontidão com bloqueios identificados, incluindo a classe do(s) criativo(s) que liberou (ou não) a escala (Etapa 3)
  2b. **Scaling Protocol aplicado ao caso do membro** (Etapa 3.5): status dos dois gates (consistência 48-72h + as duas portas do click-based), a última mudança de budget do `ad-log.md` e há quanto tempo, exceção ativa do cânone se houver (promo com data-fim / "new reason to be scaling"), qual o próximo passo de budget e quando, a régua de descida (−20% só após 24-48h persistentes abaixo do breakeven), e — em destaque — **a regra de reset da meia-noite com o número calculado** pro budget vigente
  3. **Escola de escala escolhida** (variante de intensidade) + bidding efetivo + setup operacional concreto (cost cap value / bid cap + budget / cadência de doubling) (Etapa 4)
  3b. **Promoções de breakthrough pra ABO** (Etapa 4.4): quais criativos foram promovidos (ou estão na fila), o budget inicial de cada ad set (~10% da campanha principal), a confirmação de que o ad original segue no CBO, e o registro no ad-log
  4. Política de conta nova quando entrega trava (Etapa 4.5) + status da execução via MCP, se usada: o que foi criado em PAUSED e os IDs (Etapas 4.4/4.6)
  5. Credibilidade da loja — gaps a resolver (Etapa 5)
  6. Cash flow check + gap projetado — com a necessidade de caixa, o float e o runway da `finance-engine` quando ela existir (Etapa 6)
  7. Projeção 30/60/90 base + pessimista + template cash flow, com a coluna de resultado operacional e o teto de escala quando os fixos estiverem na mesa (Etapa 7)
  8. Creative diversity plan (Etapa 8)
  9. Checklist operacional semanal (Etapa 9)
  10. Sinais de alerta (Etapa 10)

- `scale-directives.md` (fecha ciclo `scale-engine`→`creative-engine`):
  - Budget atual + budget alvo (30d)
  - Escola de escala em uso + ritmo de criativo que ela exige
  - **Breakthrough(s) em escala** — o que a `creative-engine` precisa produzir pra sustentá-los; e, se só há `KPI winner`/`spend winner`, dizer isso explicitamente (o pedido vira conceito novo, não variação)
  - PSM real atual
  - Sinais que trigam volta pra `creative-engine` (creative refresh) + se a escala está estagnada (a ação fora do ad account que cabe à `creative-engine`)
  - Bloqueios de cash flow (se houver)

- **`workspace/[produto]/ad-log.md`** (append-only, cânone `.claude/lib/ad-log/README.md` — arquivo operacional, isento de dual output): as linhas desta execução já foram gravadas **no momento de cada mudança** (degraus, resets da meia-noite, promoções pra ABO, graduação ASC, ações via MCP — ETAPAS 3.5/4.4/4.6/9), nunca em lote no fim. Antes de fechar, conferir que nenhuma mudança instruída/executada ficou sem linha.

- `dados.json` (JSON companion):

```json
{
  "plan_id": "uuid",
  "product_slug": "...",
  "stage": "starter|validating|scaling",
  "scale_phase": "testing|traction|initial_scale|aggressive|optimization",
  "scaling_school": "A_cost_cap_surf|B_bid_cap|C_budget_doubling",
  "current_daily_spend": 0,
  "target_daily_spend_30d": 0,
  "breakeven_cpa": 0,
  "max_cpa": 0,
  "psm_real": 0,
  "psm_real_basis": "shopify_new_customer|platform_cpa_proxy",
  "psm_theoretical": 0,
  "readiness_blockers": [],
  "scale_trigger": {
    "class": "breakthrough|spend_winner|kpi_winner|loser|none",
    "breakthrough_ids": [],
    "source": "ad-analysis/dados.json",
    "reclassified_from_legacy_winners": false,
    "scale_unlocked": false
  },
  "scaling_protocol": {
    "hours_above_target": 0,
    "consistency_gate_passed": false,
    "click_based_purchase_share": 0,
    "click_based_share_source": "manifest|member|none",
    "click_based_roas_beats_kpi": false,
    "click_gate_passed": false,
    "hours_below_breakeven": 0,
    "active_exception": "none|promo_end_date|new_reason_to_be_scaling",
    "step_up_pct": 20,
    "step_down_pct": 20,
    "next_step_allowed_at": null,
    "last_budget_change_from_ad_log": null,
    "stagnated": false,
    "scale_ceiling_monthly_spend": null,
    "scale_ceiling_source": "finance-engine|empirical|unknown",
    "outside_ad_account_actions": []
  },
  "midnight_reset": {
    "rule": "next_day_budget = ~50% of REAL spend, never of nominal budget",
    "ad_account_timezone": null,
    "last_real_spend": 0,
    "next_day_budget": 0
  },
  "bidding": {
    "main_campaign": "highest_volume",
    "cost_cap_scope": "zombie_graveyard_only | school_a_duplication",
    "bid_cap_used": false,
    "bid_cap_caveat_acknowledged": false
  },
  "fixed_cost_gate": {
    "source": "finance-engine|member|manifest|none",
    "monthly_fixed_costs_known": false,
    "monthly_fixed_costs": null,
    "finance_verdict": "covers_fixed_costs|scale_up_accept_lower_roas|cut_spend_below_variable_breakeven|blocked_pending_fixed_costs|null",
    "spend_to_breakeven_with_fixed": null,
    "roas_cut_recommendation": "blocked_pending_fixed_costs|blocked_by_roas_spiral|cleared|not_applicable"
  },
  "vertical_plan": {
    "cost_cap_value": null,
    "cost_cap_duplication_steps": [],
    "bid_cap_value": null,
    "bid_cap_budget": null,
    "doubling_cadence_days": null,
    "surf_enabled": false
  },
  "abo_promotions": [
    {
      "creative_id": "c-01",
      "abo_campaign_id": null,
      "adset_id": null,
      "initial_daily_budget": 0,
      "promoted_at": null,
      "original_stays_in_cbo": true
    }
  ],
  "new_account_policy": {
    "trigger": "delivery_throttled_or_account_cpm_too_high",
    "legitimate_only": true
  },
  "mcp_execution": {
    "path": "official|pipeboard|manual",
    "created_paused_campaign_ids": [],
    "automated_rules_created_disabled": []
  },
  "cash_flow": {
    "source": "finance-engine|local_estimate",
    "cash_gap_projected": 0,
    "cash_needed_90d": null,
    "total_float_days": null,
    "runway_months": null,
    "safe_to_escalate": true
  },
  "supply_confirmation": {
    "source": "sourcing-01b|member|none",
    "volume_confirmation_30_60_90": null,
    "reorder_point_days": null
  },
  "triggers_back_to_08": [
    "top_3_creatives_older_than_14_days",
    "frequency_max_over_1.4_with_ctr_drop_over_20pct",
    "scaled_past_2x_budget",
    "new_account_opened_needs_creative_fuel",
    "scale_stagnated_fix_is_outside_ad_account",
    "no_breakthrough_only_kpi_or_spend_winners"
  ]
}
```

**`abo_promotions[]`** registra cada promoção da ETAPA 4.4 — uma entrada por breakthrough promovido (`initial_daily_budget` = ~10% do budget diário da campanha principal; `abo_campaign_id` repete entre entradas porque a campanha ABO é reusada; `original_stays_in_cbo` fica `true` sempre — a promoção duplica, não move). Array vazio enquanto nenhum breakthrough foi promovido.

**Campos que a skill NUNCA preenche por estimativa:** `scale_trigger.class` (vem da classificação do cânone §2 sobre dados reais da `ad-analysis`), `scaling_protocol.click_based_purchase_share` (vem de `manifest.click_based_purchase_share` gravado pela `ad-analysis` — ou do membro via Ads Manager, quando o manifest não tem), `psm_real_basis` (cópia de `manifest.psm_real_basis`; ausente = tratar como `platform_cpa_proxy`), `supply_confirmation` (vem do `sourcing/dados.json` da `sourcing` ou do membro) e `fixed_cost_gate.monthly_fixed_costs` (vem do membro ou da `finance-engine`). Faltando qualquer um, o campo fica nulo, o gate correspondente fica bloqueado, e o relatório diz o que falta pra destravar.

**Campos que só existem quando a `finance-engine` rodou:** `fixed_cost_gate.finance_verdict` / `.spend_to_breakeven_with_fixed`, `scaling_protocol.scale_ceiling_monthly_spend`, `cash_flow.cash_needed_90d` / `.total_float_days` / `.runway_months`. São **cópias** do `finance-engine/dados.json` — esta skill não os recalcula com fórmula própria. Sem o arquivo da `finance-engine`, ficam `null`, os campos `source` registram a origem local, e cada ponto de uso cai no fallback descrito no Contexto (item 5d).

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete scale-engine` marca a skill em `skills_completed` (e valida o `scale-engine/dados.json` contra `.claude/templates/schemas/scale-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:
- Adicionar `scale-engine` em `skills_completed`
- Registrar `plan_id`, `psm_real`, `scaling_school`
- Registrar `manifest.fixed_costs_monthly` quando o membro informar (a `ad-analysis` e a `finance-engine` usam o mesmo número; se já existir e o membro deu outro, o valor novo prevalece e a mudança é avisada)
- Gravar `manifest.stage` com o vocabulário canônico (`starter` | `validating` | `scaling`). Se a sub-fase de escala importar, ela vive em `scale_phase` no `scale-engine/dados.json` — **NUNCA** em `stage`.
- Se o membro graduou de stage durante esta análise (ex: `validating` → `scaling`), atualizar `manifest.stage` e avisar (ver `member-stage-awareness.md`).
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html, onde `<slug>` é o product_slug).
