# Recipe: Sync Campaign from Meta Ads (via MCP)

Puxa estado completo de uma campanha Meta Ads via MCP e salva estruturado pra Skill 09 processar sem precisar de print.

## Triggers (linguagem natural)
- "sync campanha [nome]"
- "pull dados do Meta"
- Invocado automaticamente pela Skill 09 ETAPA 1

## Input
- `campaign_name` OU `campaign_id` — identificador da campanha (do manifest `08_campaign_name`)
- `date_preset` — default `"last_7d"`. Opções: `last_3d`, `last_14d`, `last_30d`, `maximum`
- `include_creative_hashes` — default `true` (útil pra Creative DNA)

## Pre-flight
- [ ] MCP `meta-ads` conectado (test via ping)
- [ ] Ad account ID configurado em env
- [ ] `08-ad-strategy.json` existe (referência do que deveria estar rodando)

## Steps

### 1. Resolver campaign ID
```
if campaign_name:
    campaigns = meta_ads.list_campaigns(
        ad_account_id,
        filter={"name": campaign_name}
    )
    if not campaigns:
        raise MCPError(f"Campaign not found: {campaign_name}")
    campaign_id = campaigns[0].id
```

### 2. Pull campaign-level insights
```
campaign_insights = meta_ads.insights(
    campaign_id,
    level="campaign",
    date_preset=date_preset,
    fields=[
        "spend", "impressions", "clicks", "reach", "frequency",
        "cpm", "cpc", "ctr", "cost_per_action_type",
        "purchase_roas", "conversions", "actions"
    ]
)
```

### 3. Pull ad sets
```
ad_sets = meta_ads.list_ad_sets(
    campaign_id,
    fields=["id", "name", "status", "daily_budget", "targeting",
            "optimization_goal", "bid_strategy", "created_time"]
)

for ad_set in ad_sets:
    ad_set.insights = meta_ads.insights(
        ad_set.id,
        level="adset",
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
    ad_set.insights_by_placement = meta_ads.insights(
        ad_set.id,
        breakdowns=["publisher_platform", "platform_position"]
    )
```

### 4. Pull ads (criativos)
```
for ad_set in ad_sets:
    ads = meta_ads.list_ads(
        ad_set.id,
        fields=["id", "name", "status", "creative", "created_time"]
    )
    for ad in ads:
        ad.insights = meta_ads.insights(
            ad.id,
            level="ad",
            date_preset=date_preset,
            fields=[
                "spend", "impressions", "clicks", "reach", "frequency",
                "cpm", "cpc", "ctr", "cost_per_action_type",
                "purchase_roas", "conversions",
                "video_3_sec_watched_actions",   # thumbstop
                "video_15_sec_watched_actions",  # hold
                "video_p25_watched_actions",
                "video_p50_watched_actions",
                "video_p75_watched_actions",
                "video_p100_watched_actions"
            ]
        )
        if include_creative_hashes:
            ad.creative_details = meta_ads.ad_creative.get(
                ad.creative.id,
                fields=["object_story_spec", "video_id", "image_hash",
                        "effective_authorization_category", "url_tags"]
            )
```

### 5. Computar métricas derivadas
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

### 6. Detectar outcome (pra Creative DNA)
Pra cada ad:
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

### 7. Salvar pull estruturado

`/workspace/[produto]/09-analysis/raw-pull-[YYYYMMDDTHHMMSS].json` (shape do output — valores são preenchidos pela Meta API):

```json
{
  "pulled_at": "<ISO timestamp>",
  "source": "meta_mcp",
  "date_preset": "last_7d",
  "campaign": {
    "id": "<Meta campaign ID>",
    "name": "<campaign_name do manifest>",
    "status": "<ACTIVE|PAUSED>",
    "daily_budget": "<cents>",
    "insights": { "spend": "...", "roas": "...", "cpm": "...", ... }
  },
  "ad_sets": [
    {
      "id": "<Meta ad set ID>",
      "name": "<ad set name da strategy>",
      "status": "<ACTIVE|PAUSED>",
      "daily_budget_share": "<decimal>",
      "days_running": "<int>",
      "insights": { ... },
      "derived": { "cpa": "...", "roas": "...", ... },
      "placements": { ... },
      "ads": [
        {
          "id": "<Meta ad ID>",
          "name": "Ad_<creative_id_do_aura>",
          "creative_id_aura": "<id do briefing>",
          "days_running": "<int>",
          "insights": { ... },
          "derived": {
            "cpa": "...", "ctr": "...", "thumbstop_3s": "...",
            "hold_15s": "...", "roas": "..."
          },
          "outcome": "<winner|loser|neutral|insufficient_data>",
          "creative_hash": "abc123def"
        }
      ]
    }
  ]
}
```

### 8. Notificar Creative DNA Registry (silent)

Pra cada ad com `outcome != "insufficient_data"`:
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
write_to_file(f"/workspace/[produto]/creative-dna/perf-{creative_id}.json", registry_update)
shell(f"python3 .claude/lib/creative-dna/registry.py update /workspace/[produto] {creative_id} /workspace/[produto]/creative-dna/perf-{creative_id}.json")
```

### 9. Log de automação

```json
// /workspace/[produto]/automation-log.jsonl (append) — shape, valores reais do pull
{
  "timestamp": "<ISO>",
  "action": "sync_campaign",
  "campaign_id": "<Meta ID>",
  "ads_synced": "<N>",
  "outcomes": {"winner": "<N>", "neutral": "<N>", "loser": "<N>", "insufficient_data": "<N>"},
  "dna_registry_updated": "<N>",
  "output_file": "/workspace/[produto]/09-analysis/raw-pull-<timestamp>.json"
}
```

### 10. Retornar pro caller (Skill 09)

Skill 09 recebe o path do JSON e lê direto. ETAPA 2 da Skill 09 processa como se tivesse vindo de print, mas com 100% accuracy e sem intervenção humana.

## Output esperado

- `raw-pull-[timestamp].json` salvo
- DNA Registry atualizado com outcomes
- automation-log.jsonl apenda entrada
- Nenhuma mensagem pro membro (silent backend)

## Error handling

- **Token expirado**: tentar refresh via long-lived token. Se falhar, fallback Skill 09 pro modo manual.
- **Rate limit**: exponential backoff (60s, 120s, 240s). Depois de 3 retries, falhar.
- **Campaign não existe**: erro explícito ao Skill 09, que aborta.
- **Zero ad sets ativos**: warning mas segue (campaign pode estar pausada pra investigação).

## Performance

- ~15-30 segundos pra campanha com 3 ad sets × 3 ads = 9 ads
- ~3-5 chamadas MCP por ad set + 2 por ad
- Total ~30 API calls em ~20s
- Bem dentro do rate limit Meta (200/hora)

## Custo
$0. Meta Marketing API é grátis pra uso regular.
