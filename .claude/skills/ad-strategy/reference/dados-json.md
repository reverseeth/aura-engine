# Ad Strategy · Referência: JSON companion, o schema do dados.json

> O schema completo do `ad-strategy/dados.json` (`test_capacity`, `cac_floor_check`, campanha, `ad_sets[]` como lista, eixo de página, warmup, cadência, `protections`, credibilidade, criação via MCP, UTM) e as notas sobre cada bloco. Abra ao gravar o `dados.json`.

### JSON companion — `ad-strategy/dados.json`

```json
{
  "strategy_id": "uuid",
  "product_slug": "...",
  "creative_batch_ref": "creative-engine/dados.json batch_id (concepts[].id é o handoff `creative-engine`→`ad-strategy`→`ad-analysis`)",
  "target_cpa": 40,
  "breakeven_cpa": 80,
  "member_daily_budget": 240,
  "test_capacity": {
    "max_assets": 6,
    "max_adsets": 2,
    "adsets_planned": 2,
    "assets_planned": 6,
    "concepts_available": 4,
    "concepts_deferred": 2,
    "binding_constraint": "max_adsets|floor|adset_cap_5|batch_size|margin_warning|none",
    "floor_applied": false,
    "below_floor_directional_only": false
  },
  "cac_floor_check": {
    "source": "finance-engine|none",
    "cac_floor_reference_usd": null,
    "cac_max_first_order": null,
    "target_reachable_vs_floor": "yes|no|unknown",
    "binding": false,
    "max_assets_at_floor": null
  },
  "test_budget_daily": 240,
  "test_method": "marksman|sniper|mixed",
  "structure": "1_campaign_cbo_1_adset_per_concept",
  "campaign": {
    "name": "...",
    "objective": "Sales",
    "optimization": "purchase_max_conversion",
    "budget_level": "campaign_cbo",
    "daily_budget": 240,
    "attribution": "7d_click_1d_view",
    "placements": "advantage_plus",
    "targeting": "advantage_plus_broad",
    "one_account_per_product": true
  },
  "ad_sets": [
    {
      "name": "...",
      "concept_id": "...",
      "angle": "a razão de compra em uma frase",
      "testing_method": "marksman|sniper",
      "landing_url": "https://...",
      "landing_url_source": "08_etapa6|manifest_fallback",
      "landing_url_b": null,
      "creative_count": 3,
      "primary_texts": 2,
      "headlines": 2,
      "daily_max_spending_limit": 120,
      "ad_set_id": "",
      "ad_ids": []
    }
  ],
  "page_axis": { "enabled_322_2": false, "budget_gate_daily_usd": 2000 },
  "account_warmup": { "required": false, "days": 3, "engagement_budget_daily": 50 },
  "cadence": { "launch_day": "wednesday", "decision_checkpoint": "sunday", "max_days": 7 },
  "protections": {
    "adset_daily_maximum": { "enabled": true, "value_per_adset": 120, "basis": "3x_target_cpa" },
    "spend_spike_rule": { "created": false, "active": false, "condition": "spend_5x_24h", "action": "pause" },
    "url_mismatch_rule": { "created": false, "active": false, "condition": "destination_url_not_store_domain", "action": "pause_ad" },
    "automated_performance_kill": false,
    "automated_performance_scaling": false
  },
  "pgs_enabled": false,
  "store_credibility": { "instagram": "ok", "reviews_count": 0, "comment_management": "flagged", "gaps": [] },
  "mcp_creation": { "path": "official|pipeboard|manual", "status": "created_paused|fallback_manual", "campaign_id": "", "ad_set_ids": [], "ad_ids": [] },
  "utm_schema": {}
}
```

> **Todos os números do exemplo são ilustrativos** — grave sempre os números reais deste produto, calculados na ordem da ETAPA 3.1. `target_cpa` é o divisor da capacidade (`unit_economics.target_cpa_primary_2x` ou `manifest.target_cpa`); `breakeven_cpa` (`weighted_margin_per_order`) continua gravado porque a Skill `ad-analysis` e a `scale-engine` leem por ele.
>
> **`test_capacity`:** a conta inteira, auditável. `binding_constraint` diz QUAL restrição limitou o teste (a que apertou primeiro) — é o campo que a Skill `ad-analysis` lê pra saber se a leitura nasceu apertada. `below_floor_directional_only: true` marca o caminho (b) da ETAPA 3.1 (budget abaixo do piso de US$ 100/dia): nesse estado o resultado é direcional e **não autoriza kill nem escala** — a `ad-analysis` precisa dizer isso ao membro em vez de classificar.
>
> **`cac_floor_check`** é o registro da checagem do item 1b da ETAPA 3.1 e existe **só quando `finance-engine/dados.json` está presente** — sem ele, `source: "none"`, `target_reachable_vs_floor: "unknown"` e a capacidade é calculada pelo target como sempre foi. Os três primeiros campos são **cópias** do bloco `cac` da `finance-engine`; esta skill não recalcula piso nem CAC máximo. `max_assets_at_floor` guarda a capacidade recalculada com o piso no lugar do target (a conta conservadora que o membro vê ao lado da otimista quando o veredito é `no`). **Cuidado com o vocabulário:** o `floor` de `binding_constraint`/`floor_applied` é o **piso de BUDGET** (US$ 100-150/dia); o piso deste bloco é o **piso de CAC** do leilão. São coisas diferentes e não se misturam.
>
> **`ad_sets[]` é uma LISTA** (antes era o objeto único `ad_set`): 1 entrada por conceito, com o `ad_set_id` retornado pelo MCP dentro da própria entrada. `daily_max_spending_limit` é o teto de proteção da ETAPA 6 (~3× `target_cpa`), não um budget de ad set — o budget vive em `campaign.daily_budget` com `budget_level: "campaign_cbo"`.
>
> **`ad_sets[].testing_method` é o campo operativo de método** (contrato `creative-engine`→`ad-strategy`, ETAPA 3.2): copiado de `concepts[].testing_method` da `creative-engine`; em batch legado sem o campo, gravado como `"sniper"` com `data_gap` marcado (fallback da 3.2 — legado sem `angles[]` se lê por execução). O `test_method` batch-level é só RESUMO — o método único quando todos os ad sets coincidem, `mixed` quando variam. A pergunta que cada pack responde ("qual ângulo venceu?" em Marksman, "qual execução venceu?" em Sniper) a Skill `ad-analysis` decide lendo `concepts[]` direto da `creative-engine` — e batch legado sem esses campos ela trata como sniper.
>
> **`ad_sets[].landing_url` (+ `landing_url_source`, `landing_url_b`):** o destino do conceito (ETAPA 3.3) — `08_etapa6` quando veio do mapeamento de congruência da `creative-engine`, `manifest_fallback` quando caiu na URL canônica `manifest.storefront.page_url`. `landing_url_b` fica `null` a menos que o eixo de página esteja ativo (`page_axis.enabled_322_2: true`, que exige budget ≥ US$ 2k/dia E 2 páginas publicadas pro conceito) — aí carrega a segunda LP do ad set, lida por KPI da página, nunca por spend.
>
> **`cadence.decision_checkpoint`** substitui o antigo `kill_by`: domingo é checkpoint de leitura (ETAPA 5), não data de execução. Kill de ad set é régua do cânone §3, decretada pela Skill `ad-analysis`; kill de PRODUTO exige ≥ 2 batches com learnings processados OU régua do cânone — nunca calendário sozinho.
>
> **`protections`:** substitui os antigos campos `pgs_*`. `automated_performance_kill`/`automated_performance_scaling` ficam `false` SEMPRE — não são configuráveis, são o registro explícito de que essa automação não existe nesta estrutura (cânone §6). **`pgs_enabled` permanece no schema apenas como campo de compatibilidade, fixo em `false`**, porque a receita `full-deploy.md` e a Skill `ad-analysis` ainda o leem pra decidir se prometem escala automática; com `false`, as duas degradam pro comportamento certo (não prometem). Nunca gravar `true`.
