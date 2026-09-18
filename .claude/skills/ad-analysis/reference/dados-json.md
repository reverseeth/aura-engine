# Ad Analysis · Referência: Schema do dados.json e atualização do manifest

> O handoff pra `scale-engine` e `content-recycler`: o schema completo do `ad-analysis/dados.json` com as notas de cada campo (`ad_class`, `breakthroughs[]`, `winners[]` legado, `roas_spiral_check`, `winning_sub_avatar_id`, `test_capacity_check`, `iteration_zone_check[]`, `click_based_purchase_share`) e a lista canônica dos campos do manifest gravados por `tools/manifest.py`. Abra ao gravar.

### Panorama para skill `scale-engine` e skill `content-recycler` — handoff

Se ações próximas = 'scale', skill `scale-engine` lerá este JSON SEM precisar perguntar.
Se membro invoca `recycle winner`, skill `content-recycler` lerá esse JSON pra achar o criativo — e o que ela lê é **`breakthroughs[]`**, não mais um genérico "winners".

O arquivo de análise é `workspace/[produto]/ad-analysis/dados.json` (cópia do último análise — nome literal `dados.json` dentro da pasta `ad-analysis/`):

```json
{
  "analysis_id": "uuid",
  "analyzed_at": "ISO timestamp",
  "current_daily_spend": 0,
  "current_cpa_avg": 0,
  "current_roas_avg": 0,
  "campaign_kpi": {
    "campaign_cpa": 0,
    "campaign_roas": 0,
    "account_spend_7d": 0,
    "window_days": 7,
    "stable": true
  },
  "batch_rates": {
    "concepts_tested": 0,
    "hit_rate": 0,
    "breakthrough_rate": 0,
    "volume_up_rate_down": false
  },
  "test_capacity_check": {
    "source": "ad-strategy|none",
    "binding_constraint": "max_adsets|floor|adset_cap_5|batch_size|margin_warning|none|null",
    "below_floor_directional_only": false,
    "directional_only_analysis": false
  },
  "active_breakthroughs_count": 0,
  "active_losers_count": 0,
  "breakthroughs": [
    { "creative_id": "c-01", "ad_set_id": "...", "ad_class": "breakthrough", "cpa": 0, "roas": 0, "spend_total": 0, "spend_share_7d": 0, "ad_kpi_vs_campaign": true, "hook_rate": 0, "hold_rate": 0, "days_active": 0, "winning_sub_avatar_id": "sa-01|null" }
  ],
  "spend_winners": [
    { "creative_id": "c-02", "ad_class": "spend_winner", "cpa": 0, "roas": 0, "spend_total": 0, "spend_share_7d": 0, "ad_kpi_vs_campaign": false, "hook_rate": 0, "hold_rate": 0, "days_active": 0, "next_action": "iterate" }
  ],
  "kpi_winners": [
    { "creative_id": "c-04", "ad_class": "kpi_winner", "cpa": 0, "roas": 0, "spend_total": 0, "spend_share_7d": 0, "ad_kpi_vs_campaign": true, "hook_rate": 0, "hold_rate": 0, "days_active": 0, "treated_as": "loser_for_decision", "next_action": "force_spend_test|drop" }
  ],
  "losers": [
    { "creative_id": "c-03", "ad_class": "loser", "reason": "adset_7d_no_spend_no_kpi|kill_8x_target_cpa_no_purchase|spend_share_under_2pct_7d|creative_policy", "spend_share_7d": 0, "hook_rate": 0, "hold_rate": 0, "days_active": 0 }
  ],
  "winners": [],
  "champions": [
    { "creative_id": "c-01", "post_id": "...", "promoted_at": "ISO timestamp" }
  ],
  "health_signals": {
    "frequency_max": 0,
    "cpm_trend": "up|flat|down",
    "creative_age_days_oldest": 0,
    "creative_age_days_newest": 0,
    "account_cpm_suspect": false,
    "hook_rate_avg": 0,
    "hold_rate_avg": 0,
    "funnel_atc_to_purchase_rate": 0,
    "funnel_checkout_to_purchase_rate": 0,
    "funnel_broken": false
  },
  "page_diagnosis": {
    "specimen_primary": "agora-11-blocos|null",
    "specimen_fit": "fit|mismatch_awareness|mismatch_page_type|mismatch_sophistication|mismatch_vertical|unknown",
    "markup_audit_verdict": "pass|rewrite_lead|unknown",
    "markup_audit_layer_failed": null,
    "defects_still_open": []
  },
  "iteration_zone_check": [
    { "iteration_creative_id": "c-07", "original_ref": "c-03", "zone_original": "positive/low|unknown", "zone_iteration": "negative/high|unknown", "zone_changed": true, "verdict": "zone_shift_suspected|variable_isolated|no_data" }
  ],
  "roas_spiral_check": {
    "source": "finance-engine|offer-builder|none",
    "fixed_costs_monthly": null,
    "breakeven_roas_with_fixed": null,
    "spend_to_breakeven_with_fixed": null,
    "finance_verdict": "covers_fixed_costs|scale_up_accept_lower_roas|cut_spend_below_variable_breakeven|blocked_pending_fixed_costs|null",
    "spend_cut_considered": false,
    "spend_cut_recommended": false,
    "blocked_reason": "fixed_costs_unknown|null"
  },
  "click_based_purchase_share": null,
  "psm_real": 0,
  "psm_real_basis": "shopify_new_customer|platform_cpa_proxy",
  "cac_real": 0,
  "new_customers_period": 0,
  "margin_per_order_weighted": 0,
  "recommended_action": "continue|scale|iterate_creatives|refresh_creatives|kill|fix_funnel|fix_copy_specimen|test_other_account|ask_fixed_costs|raise_spend_accept_lower_roas|raise_budget_or_reduce_concepts"
}
```

**Importante:**
- **`ad_class` é o campo canônico de classificação** desta skill, com os quatro valores do cânone `.claude/lib/ad-taxonomy/README.md` §2: `breakthrough` · `spend_winner` · `kpi_winner` · `loser`. Todo criativo classificado carrega esse campo, e é por ele que as skills `scale-engine` e `content-recycler` devem decidir — nunca por "CPA ≤ target".
- **`breakthroughs[]` substitui `winners[]`** como gatilho de escala (skill `scale-engine`) e de reciclagem (skill `content-recycler`). Ele contém **apenas** `ad_class == "breakthrough"`.
- **`winners[]` fica como alias legado, e só pode conter exatamente o mesmo conteúdo de `breakthroughs[]`** — existe para que um leitor antigo não quebre e, principalmente, não receba um `kpi_winner` disfarçado de winner. Está deprecado: leitores novos usam `breakthroughs[]`. **Nunca** coloque `kpi_winner` ou `spend_winner` nesse array.
- Skill `content-recycler` apenas LÊ `breakthroughs[]` e ordena por `spend_total`/`days_active` (NÃO re-filtra nem recomputa threshold nenhum — a classificação é responsabilidade exclusiva da skill `ad-analysis`). Se `breakthroughs[]` vier vazio, a resposta honesta ao membro **não** é "aguardar mais dados": é "você ainda não tem um ad que escala — o próximo passo é a `creative-engine`, não a `content-recycler`".
- `psm_real` é o mesmo valor gravado em `manifest.psm_real`, e `psm_real_basis` diz em que base ele foi calculado (`shopify_new_customer` = comparável com o `psm_theoretical` da `offer-builder`; `platform_cpa_proxy` = otimista, **não** comparável e não libera escala).
- **`roas_spiral_check` registra de ONDE veio a decisão de spend.** Com `finance-engine/dados.json` na mão, `source: "finance-engine"` e os quatro campos vêm copiados de lá (`breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed`, `finance_verdict`, mais `fixed_costs_monthly` de `monthly_model`) — esta skill não recalcula nenhum deles. Sem o arquivo, `source: "offer-builder"` (ou `"none"`), os três campos novos ficam `null` e o `blocked_reason` volta a operar como hoje. `recommended_action: "raise_spend_accept_lower_roas"` só pode ser gravado quando `finance_verdict == "scale_up_accept_lower_roas"` — nunca por leitura própria de ROAS.
- **`winning_sub_avatar_id`** (por item de `breakthroughs[]`) fecha o loop com a pesquisa: aponta o item de `sub_avatars[]` da `market-research` que produziu o vencedor (num Marksman, o do item de `angles[]` do criativo vencedor). `null` em batch legado sem o campo. É o alvo da mini-passada de re-research da ETAPA 5.
- **`test_capacity_check`** copia `binding_constraint` e `below_floor_directional_only` da `ad-strategy`; `directional_only_analysis: true` marca que ESTA análise inteira saiu direcional (gate de piso) — as skills `scale-engine` e `content-recycler` não devem tratar `breakthroughs[]` vazio dessa análise como veredito. `source: "none"` = estratégia legada sem `test_capacity`.
- **`iteration_zone_check[]`** registra o diagnóstico de valência da ETAPA 4 (iteração que trocou de zona emocional); `original_ref` vem de `concepts[].iteration_of` da `creative-engine` quando presente (linhagem declarada), com fallback = pareamento por prosa do briefing (batch legado); `verdict: "no_data"` quando o batch é anterior ao schema de `valence`/`intensity` da `creative-engine`.
- **`click_based_purchase_share`** espelha o que vai pro manifest (bloco da ETAPA 2): fração das purchases da janela em 7-day click. `null` = breakdown indisponível — **nunca estimado**; o gate de escala da `scale-engine` fica bloqueado até existir.
- `champions[]` permanece por compatibilidade (Post ID dedicado). A rota vigente de promoção de breakthrough é o ABO paralelo da skill `scale-engine` (cânone §5).

### Atualização do manifest (OBRIGATÓRIO — single source of truth)

Após gerar `dados.json`, atualizar o manifest com os campos canônicos pelo script `tools/manifest.py` (`python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]`; nunca editar o JSON à mão: o script faz backup, valida contra o `manifest-schema.json` e grava `updated_at`):

- `manifest.psm_real` ← `psm_real` calculado nesta análise pela fórmula canônica `LTV / (CAC_real + COGS)`, com CAC = ad spend ÷ clientes novos do Shopify. **A skill `ad-analysis` é a ÚNICA fonte que grava `manifest.psm_real`** (skill `scale-engine` lê daqui, nunca recalcula).
- `manifest.psm_real_basis` ← `"shopify_new_customer"` ou `"platform_cpa_proxy"`. A skill `scale-engine` compara `psm_real` com `psm_theoretical` (tolerância de 20%) — **essa comparação só é válida quando a base é `shopify_new_customer`**; com proxy, o número está otimista e não pode liberar escala.
- `manifest.ad_classification[]` ← **TODOS os criativos classificados nesta análise**, no shape do `manifest-schema.json`: `{creative_id, class, spend_share_7d, ad_kpi, campaign_kpi, hook_rate, hold_rate}`. `class` = o `ad_class` canônico; `ad_kpi`/`campaign_kpi` = o par usado na comparação de classificação (CPA do ad vs CPA da campanha — ou ROAS vs ROAS quando a régua de desempate for ROAS, bloco Winner picking; grave os dois lados na MESMA métrica); `hook_rate`/`hold_rate` = os medidos na ETAPA 2 (`null` pra estático). **Substitui o array inteiro a cada análise** (é estado atual, não histórico — o histórico vive nos `dados.json` datados). É a fonte de verdade que o schema declara como substituta de `winners[]`: a `scale-engine` e a `member-stage-awareness` leem `class == "breakthrough"` daqui. Análise direcional (gate de piso): não grave — sem classificação formal não há o que espelhar.
- `manifest.click_based_purchase_share` ← fração das purchases da janela atribuídas em 7-day click (bloco da ETAPA 2). É o gate de escala da `scale-engine` (≥ 0.60, cânone §5). **NUNCA estimar** (regra do manifest-schema): sem o breakdown de atribuição, NÃO grave o campo — o gate fica bloqueado e o relatório diz onde buscar o número.
- `manifest.breakthroughs[]` ← lista de creative_ids com `ad_class == "breakthrough"` nesta análise (espelha `dados.json.breakthroughs[]`). **É este o campo que as skills `scale-engine` e `content-recycler` devem ler.**
- `manifest.winners[]` ← alias legado, com **exatamente** os mesmos ids de `manifest.breakthroughs[]` (nunca `kpi_winner` nem `spend_winner`). Existe só pra não quebrar leitor antigo; deprecado.
- `manifest.kpi_winners[]` / `manifest.spend_winners[]` ← creative_ids das outras duas classes, pra que a skill `scale-engine` saiba que existe sinal sem que ele seja confundido com liberação de escala.
- `manifest.champions[]` ← acrescentar creative_ids promovidos a Post ID dedicado (não sobrescrever os já existentes; merge sem duplicar)
- `manifest.last_analysis_date` ← timestamp desta análise
- `manifest.analysis_count` ← incrementar +1
- `manifest.last_cpa_avg` ← `current_cpa_avg`
- `manifest.last_roas_avg` ← `current_roas_avg`
- `manifest.last_recommended_action` ← `recommended_action` (inclui `fix_funnel` e `test_other_account` do playbook — sinaliza pra skill `scale-engine` que o bloqueio não é escala)
- `manifest.account_cpm_suspect` / `manifest.funnel_broken` ← espelham `dados.json.health_signals` (sinalizam que matar produto/criativo seria erro — é conta ou página)
- `manifest.breakthrough_rate` ← `batch_rates.breakthrough_rate` desta análise (a skill `scale-engine` usa como leitura de saúde do pipeline de criativo; benchmark de super winner: 1-3%)
- Se `manifest.skipped_preflight` foi marcado no pré-flight (estratégia faltante), manter a flag.

Por que atualizar manifest: skills `scale-engine` e `content-recycler` leem `manifest.psm_real` (+ `psm_real_basis`), `manifest.breakthroughs[]` e `manifest.champions[]` como fonte canônica. O `dados.json` é histórico por análise; manifest é o estado atual consolidado.
