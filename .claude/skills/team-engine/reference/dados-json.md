# Team Engine · Referência: Output schema, o dados.json

> O schema completo do `team-engine/dados.json` (gate de estágio, tempo do fundador, decisão de contratação, organograma, vagas abertas, pipeline de candidatos, métricas do funil, onboarding, indicadores, reviews, incentivos, folha e handoff) e a nota dos números ilustrativos. Abra ao gravar o `dados.json`.

## Output Schema — `team-engine/team-engine.md` + `team-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills `creative-engine`, `consistency-audit`, `ad-analysis`, `scale-engine`, `finance-engine` e `creator-engine`.

```json
{
  "team_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "currency": "USD",
  "doors_run": ["decide", "hire", "run"],
  "hiring_language": "en",
  "stage_check": {
    "stage": "starter | validating | scaling",
    "recommended": false,
    "not_yet_reason": "gargalo atual é oferta/criativo, não braço",
    "reopen_signal": "sinal concreto que reabre a conversa",
    "exception_applied": "none | project_editor"
  },
  "founder_time": {
    "annual_income": null,
    "hourly_rate": null,
    "buyback_rate": null,
    "audit_source": "member_list | tracking_tool | none",
    "tasks": [
      { "task": "", "hours_week": 0, "zone": "incompetence | resentment | luxury | genius",
        "who": "", "market_cost_hour": null, "delegate": null }
    ]
  },
  "hiring_decision": {
    "constraint": "o gargalo nomeado, com o dado que o sustenta",
    "verdict": "hire | not_yet | outsource | upgrade_existing",
    "build_vs_buy": {
      "choice": "in_house | agency | fractional | freelancer | offshore_direct | hybrid",
      "edge_kept_in_house": "o que NUNCA sai de dentro",
      "agency_protocol_done": null
    },
    "sequence": [
      { "order": 1, "role": "", "role_type": "accessory | senior | leadership | partner",
        "hire_for": "skill | potential", "expected_time_to_hire_days": 35, "rationale": "" }
    ],
    "decision_memo": { "why": null, "what": null, "how": null, "now_next": null }
  },
  "org": {
    "current": [ { "seat": "", "person": "", "is_founder_seat": false, "reports_to": "" } ],
    "future_6_12m": [ { "seat": "", "person": null, "reports_to": "" } ],
    "engines": [ { "engine": "campaign | creative | conversion | content", "lead": null, "built": false } ],
    "pods": [ { "pod": "", "segmented_by": "product | avatar", "members": [] } ],
    "max_direct_reports_ok": null,
    "key_man_risk": [ { "person": "", "what_breaks": "", "patch": "" } ],
    "weekly_rhythm_installed": false
  },
  "open_roles": [
    {
      "role": "", "role_type": "accessory | senior | leadership",
      "scorecard": {
        "purpose_one_line": "",
        "core_functions": [],
        "north_star_pair": { "volume": "", "quality": "" },
        "kpi_bands": [ { "kpi": "", "green": "", "red": "", "source": "reference | member" } ]
      },
      "salary_band": { "low": null, "high": null, "source": "reference | member", "posted_top_half": null },
      "posting": { "status": "draft | live | paused", "format": "simple | sales_letter", "channels": [] },
      "sourcing": { "headhunting_active": false, "targets": [], "community_hiring": false }
    }
  ],
  "candidate_pipeline": [
    {
      "candidate": "", "role": "", "source_channel": "", "headhunted": false,
      "stage": "applied | screening_video | culture_interview | assessment | sme_interview | final_interview | reference_check | offer | hired | rejected",
      "assessment": { "sent_at": null, "returned_at": null, "hours_to_return": null, "paid": false, "wow": null },
      "verdict_notes": ""
    }
  ],
  "funnel_metrics": {
    "time_to_hire_days": null,
    "cost_to_hire": null,
    "loss_by_stage": {},
    "outcome_log": [ { "hire": "", "outcome": "bad | average | great", "source_channel": "" } ]
  },
  "onboarding": [
    { "person": "", "week": 1, "phase": "i_do | we_do | you_do",
      "qa_review_pct": 100, "meeting_cadence": "daily | 3x_week | weekly",
      "two_week_diagnosis": "crushing | grinding_up | no_progress | pending" }
  ],
  "team_kpis": {
    "goal": "", "strategy_bet": "",
    "dashboard": { "installed": false, "weekly_target_divisor": 4.3, "weekly_call_day": null },
    "by_person": [
      { "person": "", "role": "", "kpis": [ { "kpi": "", "target": null, "actual": null, "source": "" } ],
        "hit_rate_pct": null, "spend_share_pct": null }
    ],
    "naming_suffix_by_person": {}
  },
  "reviews": {
    "cadence": { "new_hires": "monthly", "team": "quarterly", "survey_nine_box": "jan_jul" },
    "nine_box": [ { "person": "", "box": "", "ab_class": "A | B | C | D", "action": "" } ],
    "pips": [ { "person": "", "opened_at": null, "duration_days": 30, "data_evidence": [], "status": "open | recovered | exit" } ],
    "time_audit": { "last_run": null, "findings": [] }
  },
  "incentives": {
    "gravy": { "active": false, "monthly_target": null, "target_source": "finance-engine | member | null", "pool_pct": 40, "split_private": true },
    "kpi_bonus_pct_of_salary": null,
    "career_ladders": [ { "person": "", "track": "ic | management | partner", "next_step": "" } ],
    "promotions": [ { "person": "", "lever": "title | pay_bump | market_check | try_before_buy | variable_up", "proof": "" } ]
  },
  "payroll": {
    "current_monthly_total": null,
    "payroll_delta_monthly": null,
    "fits_cash": null,
    "finance_source": "finance-engine/dados.json | manifest.finance | member | missing",
    "note": "folha é custo fixo; veredito só com os números da `finance-engine` ou do membro"
  },
  "pending_inputs": [],
  "handoff": {
    "for_skill_08": ["org.pods", "team_kpis.by_person", "open_roles (editor/strategist em contratação)"],
    "for_skill_09": ["onboarding[].qa_review_pct"],
    "for_skill_11": ["team_kpis.naming_suffix_by_person", "team_kpis.by_person[].hit_rate_pct"],
    "for_skill_12": ["org.key_man_risk", "payroll.current_monthly_total", "stage_check", "hiring_decision.constraint"],
    "for_skill_15": ["payroll.payroll_delta_monthly"],
    "for_skill_16": ["fronteira: creators/afiliados/embaixadores não vivem neste arquivo"]
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo são ILUSTRATIVOS** — mostram o formato de cada campo, não um caso real. Benchmarks do material de referência entram sempre com `source: "reference"`; números do membro, com `source: "member"`. Os três dados que nunca se inventam (regra 4): salário/custo real do time, caixa/custo fixo, KPI real de pessoa.
