# Recipe: Sync Campaign from Meta Ads (cascade: oficial → Pipeboard → manual)

Puxa estado completo de uma campanha Meta Ads e salva estruturado pra Skill 11 processar sem print. Receita ÚNICA com cascade interno: tenta o **MCP oficial da Meta** (`mcp.facebook.com/ads`, open beta desde 2026-04-29, rollout gradual sem GA), cai pro **Pipeboard MCP** (3rd party) automaticamente, e devolve pro caller pedir dados manuais se nenhum MCP responder.

Os dois degraus produzem o MESMO shape de output e usam a MESMA matemática de métricas/outcome (blocos únicos abaixo — steps 5-6). O que muda por degrau: as tools chamadas (steps 1-4) e os blocos `dataset_health` + `market_context`, exclusivos do oficial.

## Triggers (linguagem natural)
- "sync campanha [nome]"
- "pull dados do Meta"
- Invocado automaticamente pela Skill 11 ETAPA 1, pelo `full-deploy.md` (Stage 5) e pelo `creative-loop.md`

## Input
- `campaign_name` OU `campaign_id` — identificador (do manifest `10_campaign_name` / `10_campaign_id`)
- `date_preset` — default `"last_7d"`. Opções: `today`, `yesterday`, `last_3d`, `last_14d`, `last_30d`, `maximum`
- `include_creative_hashes` — default `true` (útil pro Creative DNA)
- `pull_industry_benchmarks` — default `true` (só tem efeito no caminho oficial)
- `force_path` — opcional: `"pipeboard"` se o membro forçar o fallback (gravar `fallback_reason: "forced_by_member"`)

## Cascade (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md`)

```
if tools `mcp__meta__ads_*` disponíveis E ad account não está "disabled" E force_path != "pipeboard":
    caminho 1 — MCP oficial (source: "meta_mcp_official")
elif tools `mcp__meta-ads__*` (Pipeboard) disponíveis:
    caminho 2 — Pipeboard (source: "meta_mcp_pipeboard" + fallback_reason)
else:
    devolver ao caller — Skill 11 ETAPA 1 caminho 3 (membro cola screenshot/números)
```

Motivos canônicos de `fallback_reason`: `account_disabled_in_official_beta` | `oauth_failed` | `official_unreachable` | `forced_by_member`. Sempre logar o motivo em `mcp-errors.log`.

## Pre-flight
- [ ] Ao menos um dos dois MCPs Meta conectado (ver cascade)
- [ ] `10-ad-strategy/dados.json` existe (referência do que deveria estar rodando + `pgs_*`/target)
- [ ] `manifest.target_cpa` disponível (gravado pela Skill 04) — necessário pro classify_outcome

## Steps

### 1. Resolver campaign ID

**Caminho 1 — oficial:**
```
ad_accounts = mcp__meta__ads_get_ad_accounts()
target_account = filtra por scope do membro (do profile.md ou manifest)

entities = mcp__meta__ads_get_ad_entities(
  ad_account_id=target_account.id,
  entity_type="campaign",
  filter={"name": campaign_name}
)
if not entities:
    raise OfficialMCPError(f"Campaign not found: {campaign_name}")
campaign_id = entities[0].id
```

Se `ads_get_ad_accounts` retorna 401/403 ou a conta está "disabled" → cair pro caminho 2 e logar o motivo em `mcp-errors.log`.

**Caminho 2 — Pipeboard:**
```
campaigns = meta_ads.list_campaigns(ad_account_id, filter={"name": campaign_name})
if not campaigns:
    raise MCPError(f"Campaign not found: {campaign_name}")
campaign_id = campaigns[0].id
```

### 2. Pull campaign-level insights

Campos (idênticos nos dois caminhos):
```
CAMPAIGN_FIELDS = [
  "spend", "impressions", "clicks", "reach", "frequency",
  "cpm", "cpc", "ctr", "cost_per_action_type",
  "purchase_roas", "conversions", "actions"
]
```

**Caminho 1:** `mcp__meta__ads_insights_performance_trend(entity_id=campaign_id, date_preset=date_preset, fields=CAMPAIGN_FIELDS)`
**Caminho 2:** `meta_ads.insights(campaign_id, level="campaign", date_preset=date_preset, fields=CAMPAIGN_FIELDS)`

### 3. Pull ad sets + insights

Campos de insights (idênticos nos dois caminhos — `actions` INCLUÍDO: é dele que o `derive_metrics` extrai purchases):
```
ADSET_FIELDS = [
  "spend", "impressions", "clicks", "reach", "frequency",
  "cpm", "cpc", "ctr", "cost_per_action_type",
  "purchase_roas", "conversions", "actions",
  "video_3_sec_watched_actions",
  "video_15_sec_watched_actions",
  "video_avg_time_watched_actions",
  "thruplays"
]
```

**Caminho 1:**
```
ad_sets = mcp__meta__ads_get_ad_entities(
  parent_id=campaign_id, entity_type="adset",
  fields=["id", "name", "status", "daily_budget", "targeting",
          "optimization_goal", "bid_strategy", "created_time"]
)
for ad_set in ad_sets:
    ad_set.insights = mcp__meta__ads_insights_performance_trend(
      entity_id=ad_set.id, date_preset=date_preset, fields=ADSET_FIELDS)
    ad_set.insights_by_placement = mcp__meta__ads_insights_performance_trend(
      entity_id=ad_set.id, date_preset=date_preset,
      breakdowns=["publisher_platform", "platform_position"])
```

**Caminho 2:**
```
ad_sets = meta_ads.list_ad_sets(
  campaign_id,
  fields=["id", "name", "status", "daily_budget", "targeting",
          "optimization_goal", "bid_strategy", "created_time"]
)
for ad_set in ad_sets:
    ad_set.insights = meta_ads.insights(
      ad_set.id, level="adset", date_preset=date_preset, fields=ADSET_FIELDS)
    ad_set.insights_by_placement = meta_ads.insights(
      ad_set.id, breakdowns=["publisher_platform", "platform_position"])
```

### 4. Pull ads (criativos)

Campos de insights (idênticos — `actions` incluído):
```
AD_FIELDS = [
  "spend", "impressions", "clicks", "reach", "frequency",
  "cpm", "cpc", "ctr", "cost_per_action_type",
  "purchase_roas", "conversions", "actions",
  "video_3_sec_watched_actions",   # thumbstop
  "video_15_sec_watched_actions",  # hold
  "video_p25_watched_actions",
  "video_p50_watched_actions",
  "video_p75_watched_actions",
  "video_p100_watched_actions"
]
```

**Caminho 1:**
```
for ad_set in ad_sets:
    ads = mcp__meta__ads_get_ad_entities(
      parent_id=ad_set.id, entity_type="ad",
      fields=["id", "name", "status", "creative", "created_time"])
    for ad in ads:
        ad.insights = mcp__meta__ads_insights_performance_trend(
          entity_id=ad.id, date_preset=date_preset, fields=AD_FIELDS)
        if include_creative_hashes:
            ad.creative_details = mcp__meta__ads_get_ad_entities(
              entity_id=ad.creative.id, entity_type="ad_creative",
              fields=["object_story_spec", "video_id", "image_hash",
                      "effective_authorization_category", "url_tags"])
```

**Caminho 2:**
```
for ad_set in ad_sets:
    ads = meta_ads.list_ads(
      ad_set.id, fields=["id", "name", "status", "creative", "created_time"])
    for ad in ads:
        ad.insights = meta_ads.insights(
          ad.id, level="ad", date_preset=date_preset, fields=AD_FIELDS)
        if include_creative_hashes:
            ad.creative_details = meta_ads.ad_creative.get(
              ad.creative.id,
              fields=["object_story_spec", "video_id", "image_hash",
                      "effective_authorization_category", "url_tags"])
```

### 4.5. Blocos exclusivos do oficial (pular no caminho 2)

**Dataset (Pixel/CAPI) quality:**
```
datasets = mcp__meta__ads_get_dataset_details(ad_account_id=target_account.id)
for dataset in datasets:
    dataset.quality = mcp__meta__ads_get_dataset_quality(dataset_id=dataset.id)
    dataset.stats = mcp__meta__ads_get_dataset_stats(dataset_id=dataset.id, date_preset=date_preset)
    dataset.errors = mcp__meta__ads_get_errors(dataset_id=dataset.id, limit=20)
```
Salva em `dataset_health` no JSON final. A Skill 11 usa pra detectar problemas de tracking que dão falso-positivo de LOSER.

**Industry benchmarks + auction + anomalias:**
```
if pull_industry_benchmarks:
    vertical = read_manifest("product_vertical") or read_profile("vertical")
    benchmark = mcp__meta__ads_insights_industry_benchmark(
      vertical=vertical, geo=read_profile("market") or "US",
      placement="all", objective="OUTCOME_SALES", date_preset=date_preset)
    auction_ranking = mcp__meta__ads_insights_auction_ranking_benchmarks(
      ad_account_id=target_account.id, date_preset=date_preset)
    opportunity_score = mcp__meta__ads_get_opportunity_score(ad_account_id=target_account.id)
    anomalies = mcp__meta__ads_insights_anomaly_signal(
      ad_account_id=target_account.id, date_preset=date_preset)
```

Esses 4 endpoints **não existem** no Pipeboard. Skill 11 ganha:
- CPM/CPA do vertical (não só do membro) → distingue "fadiga real" vs "vertical inteiro subiu"
- Auction ranking benchmark → confirma se o creative tá competitivo
- Opportunity score da Meta → reforça vs contradiz o 4Pi diagnostic (higiene, nunca comando — ver Skill 11)
- Anomaly signal → pode disparar análise antes do membro pedir

> **Guardrail do Opportunity Score:** o score (0-100) mede aderência ao playbook da Meta, NÃO performance. Nunca aplicar as recomendações dele em lote pra "subir o score" — em particular, IGNORAR a sugestão de ligar CBO/Advantage+ campaign budget durante o teste 1-1-N (budget no ad set é variável de controle da Skill 10). Texto completo do guardrail na Skill 11 ETAPA 1.

No caminho 2, gravar `dataset_health: null` e `market_context: null` no JSON (a Skill 11 trata a ausência).

### 5. Computar métricas derivadas (bloco ÚNICO — os dois caminhos)

Pra cada ad + ad set, calcular em Python:

```python
def derive_metrics(insights, created_time):
    days_running = (now - created_time).days + 1
    spend = insights.spend
    conversions = extract_purchases(insights.actions)
    impressions = insights.impressions

    cpa = spend / conversions if conversions > 0 else None
    video_views_3s = extract_thumbstop(insights.video_3_sec_watched_actions)
    video_views_15s = extract_hold(insights.video_15_sec_watched_actions)
    thumbstop_rate = video_views_3s / impressions if impressions else 0
    hold_rate_15s = video_views_15s / impressions if impressions else 0

    return {
        "cpa": cpa, "ctr": insights.ctr, "cpm": insights.cpm,
        "frequency": insights.frequency, "spend": spend,
        "roas": insights.purchase_roas or 0,
        "thumbstop_3s": thumbstop_rate,
        "hold_15s": hold_rate_15s,
        "days_running": days_running,
        "impressions": impressions,
        "clicks": insights.clicks,
        "conversions": conversions
    }
```

### 6. Detectar outcome (bloco ÚNICO — pra Creative DNA)

Pré-classificação pro registry. **A decisão operacional (kill/pause/scale) é da Skill 11** — os critérios canônicos vivem no bloco Decision Thresholds dela; aqui é o mesmo racional em versão resumida, alinhado à estrutura 1-1-N:

```python
def classify_outcome(metrics, target_cpa, fair_share, adset_delivery_healthy, min_spend=100):
    """target_cpa: do manifest (gravado pela Skill 04).
    fair_share: spend total do ad set ÷ N ads ativos (régua canônica da Skill 11 —
    NUNCA usar '% fixo do spend total': com 10-12 ads, 10% do total É o fair share).
    adset_delivery_healthy: o ad set como um todo está gastando (se NADA gastou,
    o problema é review/policy/conta — não é loser individual)."""
    if metrics.conversions == 0 and metrics.spend >= target_cpa * 1.5:
        return "zero_conversions"   # gastou 1.5× o target sem venda — negativo forte
    if (metrics.days_running >= 3 and adset_delivery_healthy
            and metrics.spend < fair_share * 0.5):
        return "loser"              # sub-entrega: Meta não está confiante no criativo
    if metrics.spend < min_spend:
        return "insufficient_data"
    if metrics.cpa is None:
        return "zero_conversions"
    if metrics.cpa < target_cpa * 0.8 and metrics.spend > 300:
        return "winner"
    if metrics.cpa > target_cpa * 2 and metrics.days_running >= 7:
        return "loser"              # CPA > 2× target SUSTENTADO após 7 dias (régua canônica da Skill 11;
                                    # entre 1× e 2× = needs optimization → aqui fica "neutral")
    return "neutral"
```

### 7. Salvar pull estruturado

`/workspace/[produto]/11-ad-analysis/raw-pull-[YYYYMMDDTHHMMSS].json` (shape único — campos exclusivos do oficial ficam `null` no caminho Pipeboard):

```json
{
  "pulled_at": "<ISO timestamp>",
  "source": "meta_mcp_official | meta_mcp_pipeboard",
  "fallback_reason": "<null no oficial | account_disabled_in_official_beta | oauth_failed | official_unreachable | forced_by_member>",
  "date_preset": "last_7d",
  "campaign": {
    "id": "<Meta campaign ID>",
    "name": "<campaign_name do manifest>",
    "status": "<ACTIVE|PAUSED>",
    "daily_budget": "<cents>",
    "insights": { "spend": "...", "roas": "...", "cpm": "...", "...": "..." }
  },
  "ad_sets": [
    {
      "id": "<Meta ad set ID>",
      "name": "<ad set name da strategy>",
      "status": "<ACTIVE|PAUSED>",
      "days_running": "<int>",
      "insights": { "...": "..." },
      "derived": { "cpa": "...", "roas": "...", "...": "..." },
      "placements": { "...": "..." },
      "ads": [
        {
          "id": "<Meta ad ID>",
          "name": "Ad_<creative_id_do_aura>",
          "creative_id_aura": "<id do briefing>",
          "days_running": "<int>",
          "insights": { "...": "..." },
          "derived": {
            "cpa": "...", "ctr": "...", "thumbstop_3s": "...",
            "hold_15s": "...", "roas": "..."
          },
          "outcome": "<winner|loser|neutral|zero_conversions|insufficient_data>",
          "creative_hash": "abc123def"
        }
      ]
    }
  ],
  "dataset_health": {
    "_comment": "null no caminho Pipeboard",
    "pixel_id": "<id>",
    "match_quality_score": "<EMQ 0-10>",
    "events_volume_last_7d": "<int>",
    "deduplication_rate": "<decimal>",
    "recent_errors": [ ]
  },
  "market_context": {
    "_comment": "null no caminho Pipeboard",
    "industry_benchmark": {
      "cpm_p50": "...", "cpa_p50": "...", "ctr_p50": "...",
      "vertical": "...", "geo": "..."
    },
    "auction_ranking": {
      "quality_ranking": "<above_avg|avg|below_avg>",
      "engagement_ranking": "...",
      "conversion_ranking": "..."
    },
    "opportunity_score": "<0-100>",
    "anomalies_detected": [ ]
  }
}
```

### 8. Notificar Creative DNA Registry (silent)

Pra cada ad com `outcome != "insufficient_data"` (**`zero_conversions` ENTRA no registry** — é o negativo mais forte que existe; cross-product learning precisa dele tanto quanto dos winners):

```
registry_update = {
    "cpa": ad.derived.cpa,
    "ctr": ad.derived.ctr,
    "thumbstop_3s": ad.derived.thumbstop_3s,
    "hold_15s": ad.derived.hold_15s,
    "roas": ad.derived.roas,
    "spend": ad.derived.spend,
    "days_active": ad.days_running,
    "outcome": ad.outcome
}
if source == "meta_mcp_official" and market_context:
    registry_update["market_context_at_pull"] = {
        "industry_cpm_p50": market_context.industry_benchmark.cpm_p50,
        "industry_cpa_p50": market_context.industry_benchmark.cpa_p50,
        "auction_quality": market_context.auction_ranking.quality_ranking
    }
write_to_file(f"/workspace/[produto]/creative-dna/perf-{creative_id}.json", registry_update)
shell(f"python3 .claude/lib/creative-dna/registry.py update /workspace/[produto] {creative_id} /workspace/[produto]/creative-dna/perf-{creative_id}.json")
```

O `market_context_at_pull` (só oficial) permite cross-product learning ponderar "este ad teve CPA $X mas o vertical estava em $Y" em vez de comparar absolutos entre produtos diferentes.

### 9. Log de automação

```json
// /workspace/[produto]/automation-log.jsonl (append) — shape, valores reais do pull
{
  "timestamp": "<ISO>",
  "action": "sync_campaign",
  "source": "meta_mcp_official | meta_mcp_pipeboard",
  "fallback_reason": "<null no oficial | motivo do fallback>",
  "campaign_id": "<Meta ID>",
  "ads_synced": "<N>",
  "outcomes": {"winner": "<N>", "neutral": "<N>", "loser": "<N>", "zero_conversions": "<N>", "insufficient_data": "<N>"},
  "dna_registry_updated": "<N>",
  "market_context_pulled": "<true só no oficial>",
  "output_file": "/workspace/[produto]/11-ad-analysis/raw-pull-<timestamp>.json"
}
```

### 10. Retornar pro caller (Skill 11)

Skill 11 recebe o path do JSON e lê direto. No caminho oficial, os blocos `dataset_health` e `market_context` são processados em sub-passes adicionais da ETAPA 2 (4Pi analysis ganha contexto de mercado real). No caminho Pipeboard, esses blocos vêm `null` e a análise segue sem eles.

## Output esperado

- `raw-pull-[timestamp].json` salvo (shape único, source declarado)
- DNA Registry atualizado com outcomes (+ market context quando oficial)
- automation-log.jsonl apenda entrada
- Nenhuma mensagem pro membro (silent backend)

## Error handling

- **OAuth expirou no Business Suite (oficial)**: prompt único pro membro re-autorizar; se ele recusar, cair pro Pipeboard (`fallback_reason: "oauth_failed"`).
- **Ad account "disabled" no rollout gradual (oficial)**: log `account_disabled_in_official_beta` em `mcp-errors.log`, cair pro Pipeboard automaticamente.
- **Token Pipeboard expirado**: tentar refresh via long-lived token. Se falhar, devolver ao caller (Skill 11 caminho manual).
- **Rate limit**: exponential backoff (60s, 120s, 240s). No oficial, após 3 retries → cair pro Pipeboard; no Pipeboard, após 3 retries → devolver ao caller.
- **Campaign não existe**: erro explícito pro caller, que aborta.
- **Zero ad sets ativos**: warning mas segue (campaign pode estar pausada pra investigação).
- **Tool específico falha mas outros funcionam**: continuar pull parcial, marcar campos faltantes como `data_gap: true` no JSON.

## Performance e rate limit

- Oficial: ~20-40s pra campanha 1 ad set × 9 ads (~35-45 chamadas, incluindo dataset health + market context). **Rate limit: a Meta não publicou tetos na beta — hipótese de trabalho = herança da Marketing API (~200 calls/hora/ad account); ver troubleshooting do `setup-mcps.md`.** Com ~35-45 calls por sync, manter ≤4 syncs/hora por ad account.
- Pipeboard: ~15-30s (~30 chamadas — sem os blocos exclusivos). Rate limit documentado: 200/hora + 100k/48h em dev.

## Custo

$0 nos dois caminhos (oficial grátis na open beta; Marketing API grátis pra uso regular de advertiser).

## Diferenças entre os degraus do cascade

| Aspecto | Oficial (caminho 1) | Pipeboard (caminho 2) |
|---|---|---|
| URL | `mcp.facebook.com/ads` | `meta-ads-mcp` (binary local) |
| Auth | OAuth Business Suite | Long-lived token (60d) |
| Setup | 3 cliques (cola URL + OAuth) | 6 passos (Developer App + token) |
| Token management | Zero (Meta renova) | Manual a cada 60 dias |
| Industry benchmarks | ✅ Nativo | ❌ Não tem |
| Auction ranking | ✅ Nativo | ❌ Não tem |
| Opportunity score | ✅ Nativo | ❌ Não tem |
| Anomaly signal | ✅ Nativo | ❌ Não tem |
| Dataset/CAPI quality | ✅ Nativo | Parcial (via Marketing API direto) |
| Status | Oficial, open beta (rollout gradual) | 3rd party, 100% disponível |

## Quando o cascade NÃO resolve

- Upload de criativo (não é caso desta receita — fica no `upload-creative-to-meta.md`; o oficial é remoto e não lê arquivo local, então o upload força Pipeboard ou Playwright)
- Nenhum MCP conectado → Skill 11 ETAPA 1 caminho 3 (membro cola screenshot/números)
