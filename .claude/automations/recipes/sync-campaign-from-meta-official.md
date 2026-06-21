# Recipe: Sync Campaign from Meta Ads (via official Meta MCP)

Puxa estado completo de uma campanha Meta Ads via **MCP oficial da Meta** (`mcp.facebook.com/ads`, lançado em open beta 2026-04-29) e salva estruturado pra Skill 11 processar sem print.

Esta é a receita **preferencial** desde maio/2026. A receita legada (`sync-campaign-from-meta.md`, via Pipeboard 3rd party) continua como fallback automático.

## Triggers (linguagem natural)
- "sync campanha [nome]"
- "pull dados do Meta"
- Invocado automaticamente pela Skill 11 ETAPA 1 (caminho preferencial)

## Pré-requisito: detecção do MCP oficial

Antes de invocar esta receita, a Skill 11 verifica se o MCP oficial está conectado:

```
oficial_tools = tools com prefixo `mcp__meta__ads_`
if oficial_tools disponíveis e ad_account não está "disabled":
    invocar ESTA receita
elif tools com prefixo `mcp__meta-ads__` (Pipeboard legacy) disponíveis:
    invocar `sync-campaign-from-meta.md`
else:
    fallback manual (membro cola screenshot/números)
```

## Input
- `campaign_name` OU `campaign_id` — identificador (do manifest `10_campaign_name`)
- `date_preset` — default `"last_7d"`. Opções: `last_3d`, `last_14d`, `last_30d`, `maximum`
- `include_creative_hashes` — default `true`
- `pull_industry_benchmarks` — default `true` (exclusivo do MCP oficial)

## Pre-flight
- [ ] MCP oficial conectado (verificar tool `ads_get_ad_accounts` retorna lista não-vazia)
- [ ] Ad account específico desta campanha não está marcado "disabled" no rollout gradual do beta
- [ ] `10-ad-strategy/dados.json` existe

## Steps

### 1. Resolver campaign ID via tool oficial

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

Se `ads_get_ad_accounts` retorna 401/403 ou conta marcada "disabled" → fall back pra `sync-campaign-from-meta.md` (Pipeboard) e logar o motivo em `mcp-errors.log`.

### 2. Pull campaign-level insights

```
campaign_insights = mcp__meta__ads_insights_performance_trend(
  entity_id=campaign_id,
  date_preset=date_preset,
  fields=[
    "spend", "impressions", "clicks", "reach", "frequency",
    "cpm", "cpc", "ctr", "cost_per_action_type",
    "purchase_roas", "conversions", "actions"
  ]
)
```

### 3. Pull ad sets + insights

```
ad_sets = mcp__meta__ads_get_ad_entities(
  parent_id=campaign_id,
  entity_type="adset",
  fields=["id", "name", "status", "daily_budget", "targeting",
          "optimization_goal", "bid_strategy", "created_time"]
)

for ad_set in ad_sets:
    ad_set.insights = mcp__meta__ads_insights_performance_trend(
      entity_id=ad_set.id,
      date_preset=date_preset,
      fields=[
        "spend", "impressions", "clicks", "reach", "frequency",
        "cpm", "cpc", "ctr", "cost_per_action_type",
        "purchase_roas", "conversions",
        "video_3_sec_watched_actions",
        "video_15_sec_watched_actions",
        "video_avg_time_watched_actions",
        "thruplays"
      ]
    )
    ad_set.insights_by_placement = mcp__meta__ads_insights_performance_trend(
      entity_id=ad_set.id,
      date_preset=date_preset,
      breakdowns=["publisher_platform", "platform_position"]
    )
```

### 4. Pull ads (criativos)

```
for ad_set in ad_sets:
    ads = mcp__meta__ads_get_ad_entities(
      parent_id=ad_set.id,
      entity_type="ad",
      fields=["id", "name", "status", "creative", "created_time"]
    )
    for ad in ads:
        ad.insights = mcp__meta__ads_insights_performance_trend(
          entity_id=ad.id,
          date_preset=date_preset,
          fields=[
            "spend", "impressions", "clicks", "reach", "frequency",
            "cpm", "cpc", "ctr", "cost_per_action_type",
            "purchase_roas", "conversions",
            "video_3_sec_watched_actions",
            "video_15_sec_watched_actions",
            "video_p25_watched_actions",
            "video_p50_watched_actions",
            "video_p75_watched_actions",
            "video_p100_watched_actions"
          ]
        )
        if include_creative_hashes:
            ad.creative_details = mcp__meta__ads_get_ad_entities(
              entity_id=ad.creative.id,
              entity_type="ad_creative",
              fields=["object_story_spec", "video_id", "image_hash",
                      "effective_authorization_category", "url_tags"]
            )
```

### 5. Pull dataset (Pixel/CAPI) quality — exclusivo do oficial

```
datasets = mcp__meta__ads_get_dataset_details(ad_account_id=target_account.id)
for dataset in datasets:
    dataset.quality = mcp__meta__ads_get_dataset_quality(dataset_id=dataset.id)
    dataset.stats = mcp__meta__ads_get_dataset_stats(
      dataset_id=dataset.id,
      date_preset=date_preset
    )
    dataset.errors = mcp__meta__ads_get_errors(
      dataset_id=dataset.id,
      limit=20
    )
```

Salva em `dataset_health` no JSON final. A Skill 11 usa pra detectar problemas de tracking que dão falso-positivo de LOSER.

### 6. Pull industry benchmarks — exclusivo do oficial

```
if pull_industry_benchmarks:
    vertical = read_manifest("product_vertical") or read_profile("vertical")
    benchmark = mcp__meta__ads_insights_industry_benchmark(
      vertical=vertical,
      geo=read_profile("market") or "US",
      placement="all",
      objective="OUTCOME_SALES",
      date_preset=date_preset
    )
    auction_ranking = mcp__meta__ads_insights_auction_ranking_benchmarks(
      ad_account_id=target_account.id,
      date_preset=date_preset
    )
    opportunity_score = mcp__meta__ads_get_opportunity_score(ad_account_id=target_account.id)
    anomalies = mcp__meta__ads_insights_anomaly_signal(
      ad_account_id=target_account.id,
      date_preset=date_preset
    )
```

Esses 4 endpoints **não existem** no Pipeboard MCP. Skill 11 ganha:
- CPM/CPA do vertical (não só do membro) → distingue "fadiga real" vs "vertical inteiro subiu"
- Auction ranking benchmark → confirma se o creative tá competitivo
- Opportunity score da Meta → reforça vs contradiz o 4Pi diagnostic
- Anomaly signal → pode disparar análise antes do membro pedir

### 7. Computar métricas derivadas (igual ao legacy)

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

### 8. Detectar outcome (igual ao legacy)

```python
def classify_outcome(metrics, target_cpa, min_spend=100):
    if metrics.spend < min_spend:
        return "insufficient_data"
    if metrics.cpa is None:
        return "zero_conversions"
    if metrics.cpa < target_cpa * 0.8 and metrics.spend > 300:
        return "winner"
    if metrics.cpa > target_cpa * 1.5:
        return "loser"
    return "neutral"
```

### 9. Salvar pull estruturado

`/workspace/[produto]/11-ad-analysis/raw-pull-[YYYYMMDDTHHMMSS].json` (mesmo shape do legacy + 2 blocos novos):

```json
{
  "pulled_at": "<ISO timestamp>",
  "source": "meta_mcp_official",
  "mcp_url": "https://mcp.facebook.com/ads",
  "date_preset": "last_7d",
  "campaign": {
    "id": "<Meta campaign ID>",
    "name": "<campaign_name do manifest>",
    "status": "<ACTIVE|PAUSED>",
    "daily_budget": "<cents>",
    "insights": { "spend": "...", "roas": "...", "cpm": "...", ... }
  },
  "ad_sets": [ /* mesmo schema do legacy */ ],
  "dataset_health": {
    "pixel_id": "<id>",
    "match_quality_score": "<0-10>",
    "events_volume_last_7d": "<int>",
    "deduplication_rate": "<decimal>",
    "recent_errors": [ /* últimos N erros do CAPI */ ]
  },
  "market_context": {
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
    "anomalies_detected": [ /* lista de KPIs deviando de baseline */ ]
  }
}
```

### 10. Notificar Creative DNA Registry (igual ao legacy)

```
for ad com outcome != "insufficient_data":
    registry_update = {
        "cpa": ad.derived.cpa,
        "ctr": ad.derived.ctr,
        "thumbstop_3s": ad.derived.thumbstop_3s,
        "hold_15s": ad.derived.hold_15s,
        "roas": ad.derived.roas,
        "spend": ad.derived.spend,
        "days_active": ad.days_running,
        "outcome": ad.outcome,
        "market_context_at_pull": {
            "industry_cpm_p50": market_context.industry_benchmark.cpm_p50,
            "industry_cpa_p50": market_context.industry_benchmark.cpa_p50,
            "auction_quality": market_context.auction_ranking.quality_ranking
        }
    }
    write_to_file(f"/workspace/[produto]/creative-dna/perf-{creative_id}.json", registry_update)
    shell(f"python3 .claude/lib/creative-dna/registry.py update /workspace/[produto] {creative_id} /workspace/[produto]/creative-dna/perf-{creative_id}.json")
```

O `market_context_at_pull` é novo — permite cross-product learning ponderar "este ad teve CPA $X mas o vertical estava em $Y" em vez de comparar absolutos entre produtos diferentes.

### 11. Log de automação

```json
// /workspace/[produto]/automation-log.jsonl (append) — shape, valores reais do pull
{
  "timestamp": "<ISO>",
  "action": "sync_campaign",
  "source": "meta_mcp_official",
  "campaign_id": "<Meta ID>",
  "ads_synced": "<N>",
  "outcomes": {"winner": "<N>", "neutral": "<N>", "loser": "<N>", "insufficient_data": "<N>"},
  "dna_registry_updated": "<N>",
  "market_context_pulled": true,
  "output_file": "/workspace/[produto]/11-ad-analysis/raw-pull-<timestamp>.json"
}
```

### 12. Retornar pro caller (Skill 11)

Skill 11 recebe o path do JSON e lê direto. Os blocos `dataset_health` e `market_context` são processados em sub-passes adicionais da ETAPA 2 (4Pi analysis ganha contexto de mercado real).

## Output esperado

- `raw-pull-[timestamp].json` salvo (shape estendido)
- DNA Registry atualizado com outcomes + market context
- automation-log.jsonl apenda entrada com `source: "meta_mcp_official"`
- Nenhuma mensagem pro membro (silent backend)

## Error handling

- **OAuth expirou no Business Suite**: prompt único pro membro re-autorizar; se ele recusar, fallback Pipeboard.
- **Ad account marcado "disabled" no rollout gradual**: log `account_disabled_in_official_beta` em `mcp-errors.log`, fallback automático pro `sync-campaign-from-meta.md` (Pipeboard).
- **Rate limit (~200 calls/hora/ad account, herdado da Marketing API)**: exponential backoff (60s, 120s, 240s). Após 3 retries, fallback Pipeboard. Atenção: cada sync completo gasta ~35-45 calls, então 4-5 syncs/hora no mesmo ad account encostam no teto — espaçar pulls automáticos.
- **Campaign não existe**: erro explícito pro Skill 11, que aborta.
- **Tool específico falha mas outros funcionam**: continuar pull parcial, marcar campos faltantes como `data_gap: true` no JSON.

## Performance

- ~20-40s pra campanha com 3 ad sets × 3 ads = 9 ads + dataset health + market context
- ~35-45 chamadas MCP totais (10 a mais que o legacy por causa dos blocos novos)
- Rate limit ~200 calls/hora/ad account (herdado da Marketing API). Com ~35-45 calls por sync, mantenha-se em ≤4 syncs/hora por ad account pra não estourar.

## Custo

$0 durante a open beta. Long-term pricing não-anunciado pela Meta até maio/2026.

## Diferenças vs. `sync-campaign-from-meta.md` (Pipeboard legacy)

| Aspecto | Oficial | Pipeboard (legacy) |
|---|---|---|
| URL | `mcp.facebook.com/ads` | `meta-ads-mcp` (binary local) |
| Auth | OAuth Business Suite | Long-lived token (60d) |
| Setup | 3 cliques (cola URL + OAuth) | 6 passos (Developer App + token) |
| Token management | Zero (Meta renova) | Manual a cada 60 dias |
| Rate limit | ~200/hora/ad account (herda Marketing API) | 200/hora + 100k/48h |
| Industry benchmarks | ✅ Nativo | ❌ Não tem |
| Auction ranking | ✅ Nativo | ❌ Não tem |
| Opportunity score | ✅ Nativo | ❌ Não tem |
| Anomaly signal | ✅ Nativo | ❌ Não tem |
| Dataset/CAPI quality | ✅ Nativo | Parcial (via Marketing API direto) |
| Status legal | Oficial sancionado | 3rd party (risco suspensão) |
| Risco de breaking change | Baixo (Meta governa) | Médio (Pipeboard governa) |
| Rollout | Gradual (alguns accounts disabled) | 100% disponível |

## Quando esta receita NÃO deve ser usada

- Membro está em ad account ainda não liberado pelo rollout gradual → cai pro Pipeboard
- Membro não quer / não pode conectar Business Suite via OAuth (raro)
- Upload de criativo (não é caso desta receita — fica no `upload-creative-to-meta.md` que continua via Pipeboard ou Playwright pelo problema do file local)
