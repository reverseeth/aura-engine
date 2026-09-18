# Finance Engine · Referência: Contrato de leitura, quem lê o quê

> A tabela dos campos que a ad-analysis, a scale-engine, a offer-builder, a retention-engine e a ad-strategy passam a ler desta skill, e a regra da leitura aditiva. Abra ao fechar o `dados.json`.

## Contrato de leitura (quem lê o quê)

Esta skill é a **produtora** dos números abaixo. As consumidoras leem por estes caminhos exatos e não recalculam com fórmula própria.

| Skill | Campo que passa a ler | O que muda |
|---|---|---|
| **11** ad-analysis | `roas_spiral.breakeven_roas_with_fixed`, `roas_spiral.cut_spend_recommendation_allowed`, `roas_spiral.verdict`, `roas_spiral.spend_to_breakeven_with_fixed` | Hoje a `ad-analysis` lê `offer-builder/dados.json.budget_viability.fixed_costs_monthly` e bloqueia o corte quando é `null`. Com a `finance-engine` rodada, a decisão deixa de ser bloqueio e vira número: sobe, segura ou corta, com o spend de breakeven calculado. |
| **12** scale-engine | `cash.cash_needed_90d`, `cash.float_stack.total_float_days`, `cash.runway_months`, `monthly_model.fixed_costs_monthly`, `payback.scale_ceiling_monthly_spend`, `roas_spiral.cut_spend_recommendation_allowed` | A ETAPA 6 da `scale-engine` estima o gap de caixa sozinha e a ETAPA 7 projeta 30/60/90 sem camada de custo fixo. Com estes campos, a projeção passa a ter resultado operacional, e o teto de escala vira número em vez de sensação. |
| **04** offer-builder | `monthly_model.fixed_costs_monthly`, `monthly_model.contribution_margin_pct`, `payback.payback_window_days_measured`, `cash.runway_months` | `budget_viability.result_after_fixed_monthly` deixa de ser `null`. E para membro em `scaling` com LTV **medido**, `payback_window_days_measured ≤ 90` é a alternativa ao gate de margem mínima por pedido — com `cash.runway_months` fechando a segunda perna da alternativa (o caixa aguenta a janela: `runway_months × 30 ≥ payback_window_days_measured`). |
| **13** retention-engine | `cohorts.ltv_pct_by_month`, `cohorts.decay_factor`, `cohorts.crossover_month`, `cohorts.churn_spike_day` | Os flows deixam de mirar LTV estimado e passam a mirar o mês real de cruzamento e o pico de churn medido. |
| **10** ad-strategy | `cac.cac_floor_reference_usd`, `cac.cac_max_first_order`, `cac.target_reachable_vs_floor` | O CPA-alvo da campanha passa por checagem contra o piso físico antes de virar setpoint. |

Quando o `finance-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — a leitura é aditiva, nunca pré-requisito.
