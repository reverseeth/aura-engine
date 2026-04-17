# Recipe: Full Deploy (end-to-end)

Receita orquestradora que faz deploy completo de produto em Shopify + estrutura de campanha no Meta Ads, com um único comando do membro. Tudo paused até aprovação humana.

## Triggers
- "full deploy"
- "deploy completo [produto]"
- "sobe tudo — Shopify + Meta"

## Input
- `product_slug` — do manifest (ex: `<product-slug>`)
- `mode` — `dry-run` | `staging` | `live` (default `staging`)
- `skip_steps[]` — opcional, pra pular partes já feitas (ex: `["shopify_product"]` se produto já existe)

## Pre-flight (OBRIGATÓRIO — falha se faltar)

- [ ] `manifest.json` completo com `08-ad-strategy` em `skills_completed`
- [ ] `04-offer.json` com 3 tiers
- [ ] `05-copy.md` pronto
- [ ] `06-page/staging/` deployed (template + sections)
- [ ] `07-creatives/` com briefings prontos
- [ ] `08-ad-strategy.json` com estrutura de campanha definida
- [ ] MCP `meta-ads` conectado e testado
- [ ] MCP `shopify` conectado e testado
- [ ] Ad Account ID válido
- [ ] Shopify store confirmada no manifest
- [ ] Pixel ID + CAPI access token configurados

Se faltar qualquer um: PARAR, listar o que falta, não executar nada.

## Fluxo (8 stages)

### Stage 1 — Shopify Product Deploy
Invoca `deploy-shopify-product.md`:

```
result_1 = invoke_recipe("deploy-shopify-product", {
  product_slug: manifest.product_slug,
  offer_tiers: offer.tiers,
  description_md: "/workspace/[produto]/05-copy.md",
  images: manifest.images_paths || []
})
```

**Outputs:**
- `product_id`, `variant_ids {Starter, Popular, BestValue}`, status: draft

### Stage 2 — Wire Variant IDs no template da PDP
Ler template `/workspace/[produto]/06-page/staging/templates/page.[slug].json`, substituir placeholders `VARIANT_ID_STARTER|POPULAR|BESTVALUE` pelos IDs reais do Stage 1. Push via Shopify CLI.

```
shopify.theme.asset.update(
  theme_id=manifest.shopify_theme_id,
  key="templates/page.[slug].json",
  value=patched_template_json
)
```

### Stage 3 — Criar Campaign no Meta
```
campaign = meta_ads.campaign.create(
  ad_account_id,
  name=strategy.campaign_name,  // "<brand>_20260417_Main"
  objective="OUTCOME_SALES",
  status="PAUSED",
  special_ad_categories=[],
  buying_type="AUCTION",
  daily_budget=strategy.total_daily_budget_usd * 100,  // cents
  bid_strategy="LOWEST_COST_WITHOUT_CAP"
)
```

### Stage 4 — Criar Ad Sets
Pra cada ad_set em `strategy.ad_sets`:

```
ad_set = meta_ads.ad_set.create(
  campaign.id,
  name=ad_set.name,
  daily_budget=ad_set.budget_allocation_pct * total_daily_budget,
  optimization_goal="OFFSITE_CONVERSIONS",
  billing_event="IMPRESSIONS",
  bid_strategy="LOWEST_COST_WITHOUT_CAP",
  targeting={
    "geo_locations": {"countries": ["US"]},
    "age_min": 35,
    "age_max": 55,
    "genders": [2],  // women
    "advantage_plus_audience": {"enabled": True},
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "story", "reels"],
    "instagram_positions": ["stream", "story", "reels", "explore"]
  },
  status="PAUSED",
  promoted_object={"pixel_id": manifest.pixel_id, "custom_event_type": "PURCHASE"}
)
```

### Stage 5 — Upload criativos (se .mp4 existirem)
Verifica `/workspace/[produto]/07-creatives/videos/` pra cada criativo briefing.

Pra cada vídeo existente, invocar `upload-creative-to-meta.md`:
```
invoke_recipe("upload-creative-to-meta", {
  creative_id: "<creative-id>",
  ad_set_name: "<ad_set_name>",
  video_path: "/workspace/[produto]/07-creatives/videos/<creative-id>.mp4",
  status: "PAUSED"
})
```

Se vídeos ainda não existem, logar warning mas prosseguir — Stage 5 roda depois quando membro diser "sobe os vídeos".

### Stage 6 — Configurar Automated Rules (PGS)
```
meta_ads.automated_rule.create(
  ad_account_id,
  name="PGS_Scale_Rule",
  evaluation_spec={
    "trigger_type": "SCHEDULE",
    "schedule": "MONDAY_WEDNESDAY_FRIDAY_10AM_EST",
    "filters": [
      {"field": "cost_per_action_type.purchase", "operator": "LESS_THAN", "value": strategy.pgs_cpa_threshold},
      {"field": "spend", "operator": "GREATER_THAN", "value": strategy.pgs_spend_threshold},
      {"field": "frequency", "operator": "LESS_THAN_EQUAL", "value": strategy.pgs_freq_max}
    ]
  },
  execution_spec={
    "execution_type": "CHANGE_BUDGET",
    "execution_options": {"change_percentage": 5, "max_budget_increase_pct": 100}
  },
  status="ENABLED"
)
```

### Stage 7 — Initial sync via sync-campaign-from-meta

Invoca a receita pra snapshot do estado zero:
```
invoke_recipe("sync-campaign-from-meta", {
  campaign_name: strategy.campaign_name,
  date_preset: "today"
})
```

Salva state inicial em `/workspace/[produto]/09-analysis/raw-pull-[timestamp].json` como baseline.

### Stage 8 — Update manifest + log

```
manifest.update({
  "meta_campaign_id": campaign.id,
  "meta_ad_set_ids": {name: id for name, id in ad_sets},
  "shopify_product_id": result_1.product_id,
  "shopify_variant_ids": result_1.variant_ids,
  "full_deploy_completed_at": timestamp,
  "full_deploy_status": "paused_awaiting_approval"
})
```

Log consolidado:
```json
{
  "timestamp": "2026-04-17T15:30:00Z",
  "action": "full_deploy",
  "product_slug": "<product-slug>",
  "mode": "staging",
  "stages_completed": 8,
  "shopify": {
    "product_id": "gid://shopify/Product/8123456",
    "product_status": "draft",
    "variants_count": 3,
    "template_patched": true
  },
  "meta": {
    "campaign_id": "23845123",
    "campaign_status": "PAUSED",
    "ad_sets_created": 3,
    "ads_uploaded": 6,
    "ads_pending_video": 3,
    "pgs_rule_enabled": true
  },
  "next_steps": [
    "Produzir 3 vídeos faltantes: [<creative-id>, <creative-id>, <creative-id>]",
    "Quando prontos: 'sobe os vídeos faltantes'",
    "Review Meta Ads Manager — tudo paused",
    "Activate: 'Claude, ativa a campanha <brand>_20260417_Main'"
  ]
}
```

Mensagem final ao membro:
```
✓ FULL DEPLOY concluído — mode: staging

Shopify:
  ✓ Produto criado (draft): <brand> <product> System
  ✓ 3 variants: Starter $49, Popular $119, BestValue $199
  ✓ Variant IDs wired no template page.[slug].json
  ✓ Tema atualizado (unpublished)

Meta Ads (tudo PAUSED):
  ✓ Campaign: <brand>_20260417_Main ($100/dia CBO)
  ✓ Ad Sets:
    - <ad_set_name> ($40/dia, 40%)
    - <ad_set_name> ($35/dia, 35%)
    - <ad_set_name> ($25/dia, 25%)
  ✓ 6 criativos uploaded
  ⏳ 3 criativos aguardando vídeos:
      <creative-id>, <creative-id>, <creative-id>
  ✓ PGS rule enabled: +5% MWF 10AM EST quando CPA < $40.50 & Spend > $90 & Freq ≤ 1.3

Creative DNA Registry:
  ✓ 6 criativos registered com features extraídas
  ⏳ Performance update virá via Skill 09 após 3-7 dias

Quando quiser:
  - "sobe os vídeos faltantes" (quando produzir os 3)
  - "review Meta Ads Manager" (pra checar tudo paused)
  - "ativa a campanha <brand>" (GO)
  - "run analysis" (depois de 3+ dias de dados)
```

## Dry-run mode

Se `mode == "dry-run"`, NADA é criado real — apenas logado o que seria criado. Output idêntico mas com `"dry_run": true` e `action_type: "simulated"` em cada stage.

Útil pra primeira rodada — vê o que vai acontecer antes de confirmar.

## Rollback

Se algum stage falhar:
1. Log explícito do stage que falhou + razão
2. **NÃO reverter automaticamente stages anteriores.**
3. Fornecer ao membro o comando de rollback específico:
   ```
   "Claude, rollback full-deploy até stage N"
   ```

Isso protege contra destruir trabalho acidentalmente. Agent explicitamente pergunta antes de reverter.

## Custo

Tudo grátis (tokens Claude + APIs gratuitas).

## Tempo estimado

- Stage 1-2 (Shopify): 30-60s
- Stage 3-6 (Meta setup): 60-90s
- Stage 5 (upload vídeos — só os existentes): 20-40s por vídeo
- Stage 7 (sync): 20-30s
- **Total: 3-5 minutos** pra campanha típica de 3 ad sets × 3 ads
