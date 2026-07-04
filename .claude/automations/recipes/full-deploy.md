# Recipe: Full Deploy (end-to-end)

Receita orquestradora que faz deploy completo de produto em Shopify + estrutura de campanha no Meta Ads, com um único comando do membro. Estrutura canônica de campanha: **1 campanha Advantage+ → 1 ad set broad → N ads** (os criativos do batch da Skill 08) — a MESMA que a Skill 10 define; esta receita nunca inventa estrutura própria. Tudo nasce PAUSED (inclusive Automated Rules, que nascem DESATIVADAS) até aprovação humana.

## Triggers
- "full deploy"
- "deploy completo [produto]"
- "sobe tudo — Shopify + Meta"

## Input
- `product_slug` — do manifest (ex: `<product-slug>`)
- `mode` — `dry-run` | `staging` | `live` (default `staging`)
- `skip_steps[]` — opcional, pra pular partes já feitas (ex: `["shopify_product"]` se produto já existe)

## Pre-flight (OBRIGATÓRIO — falha se faltar)

- [ ] `manifest.json` completo com `10-ad-strategy` em `skills_completed`
- [ ] `04-offer-builder/dados.json` existe (`pricing.main_sku_price`, `unit_economics`)
- [ ] `06-copy-engine/copy-engine.md` pronto (ou o legado `relatorio.md` em produto antigo)
- [ ] `07-page/staging/` deployed E `manifest.storefront.page_url` preenchido (gravado pela 07b — é a URL de destino dos ads)
- [ ] `manifest.tracking.tracking_ready == true` (gravado pela 07c — pixel + CAPI ativos, EMQ ≥ 6/10)
- [ ] `08-creative-engine/dados.json` com o batch de conceitos
- [ ] `10-ad-strategy/dados.json` com `campaign`, `ad_set`, `test_budget_daily` definidos
- [ ] MCP Meta conectado e testado (oficial `mcp__meta__ads_*` preferencial OU Pipeboard `mcp__meta-ads__*` fallback — ver `.claude/lib/mcp-detect/README.md`)
- [ ] Shopify conectado (plugin AI Toolkit / Shopify CLI autenticado)
- [ ] Ad Account ID válido
- [ ] Shopify store confirmada no manifest

Se faltar qualquer um: PARAR, listar o que falta, não executar nada.

## Fluxo (6 stages)

### Stage 1 — Shopify Product Deploy (inclui wire de Variant IDs)

Invoca `deploy-shopify-product.md` — a sub-receita cria produto + variants E patcheia os Variant IDs no template da PDP (não repetir o wire aqui):

```
result_1 = invoke_recipe("deploy-shopify-product", {
  product_slug: manifest.product_slug,
  bundle_tiers: read("07d-checkout-aov/dados.json").levers.bundles.tiers,  // Solo/3-pack/6-pack; se 07d não rodou, single-SKU do 04 (pricing.main_sku_price)
  description_md: "/workspace/[produto]/06-copy-engine/copy-engine.md",
  images: []  // paths locais fornecidos pelo membro — a sub-receita pergunta se vazio
})
```

**Outputs:** `product_id`, `variant_ids {por tier}`, status: draft, template patched no tema `manifest.storefront.theme_id`.

### Stage 2 — Estrutura de campanha no Meta (1 campanha → 1 ad set → N ads)

Ler `strategy = 10-ad-strategy/dados.json`. **Primeiro, checar se a Skill 10 ETAPA 6 já criou a estrutura via MCP** (não duplicar):

```
if strategy.mcp_creation.status == "created_paused":
    campaign_id = strategy.mcp_creation.campaign_id
    ad_set_id = strategy.mcp_creation.ad_set_id
    // estrutura já existe em PAUSED — pular pra Stage 3
else:
    // criar agora, com os campos REAIS do schema da 10
    campaign = meta_ads.campaign.create(
      ad_account_id,
      name=strategy.campaign.name,
      objective="OUTCOME_SALES",
      status="PAUSED",
      special_ad_categories=[],
      buying_type="AUCTION"
      // SEM daily_budget na campanha: strategy.campaign.budget_level == "ad_set"
      // (setar budget em campanha E ad set ao mesmo tempo é rejeitado pela Marketing API)
    )

    ad_set = meta_ads.ad_set.create(
      campaign.id,
      name=strategy.ad_set.name,
      daily_budget=strategy.test_budget_daily * 100,  // cents — 2× breakeven CPA (doutrina da 10)
      optimization_goal="OFFSITE_CONVERSIONS",        // Purchase
      billing_event="IMPRESSIONS",
      bid_strategy="LOWEST_COST_WITHOUT_CAP",
      targeting={
        // BROAD/Advantage+ — o criativo faz o targeting (Skill 10 ETAPA 3).
        // NUNCA hardcodar demografia: age 18-65+, gender All,
        // a menos que a 02/10 tenham dado claro de produto gênero-específico.
        "geo_locations": {"countries": [read_profile("market") or "US"]},
        "advantage_plus_audience": {"enabled": True}
        // placements: Advantage+ (automáticos) — não restringir manualmente
      },
      status="PAUSED",
      promoted_object={"pixel_id": resolved_pixel_id, "custom_event_type": "PURCHASE"}
    )
```

`resolved_pixel_id`: via `mcp__meta__ads_get_dataset_details` (oficial) ou, sem o oficial, perguntar 1× ao membro (Events Manager → Data Sources) e gravar `manifest.meta_pixel_id` pra reuso (mesma chave que `upload-creative-to-meta.md` usa).

> **Regra estrutural (Skill 10 ETAPA 7):** NÃO criar múltiplos ad sets, NÃO adicionar interests, NÃO setar CBO. 1 ad set broad com N criativos é a estrutura de teste; diversificação é assunto da Skill 12 (escala), não desta receita.

### Stage 3 — Upload criativos (se .mp4 existirem)

Convenção real da Skill 08: vídeos renderizados vivem em `/workspace/[produto]/08-creative-engine/renders/` (`c0X.mp4` ou `c0X-shot-N.mp4`; o campo `concepts[].production_prompts.video.rendered_file` do `08-creative-engine/dados.json` aponta o arquivo). Se o membro editou fora (CapCut etc.), pedir os paths finais.

Pra cada conceito de `strategy.ad_set.creative_concept_ids` com vídeo final disponível, invocar `upload-creative-to-meta.md`:
```
invoke_recipe("upload-creative-to-meta", {
  creative_id: "<concept_id>",
  ad_set_name: strategy.ad_set.name,
  video_path: "/workspace/[produto]/08-creative-engine/renders/<arquivo>.mp4",
  status: "PAUSED"
})
```

Ad Name segue a convenção da 10: `[concept_id]_[YYYYMMDD]` (preserva o handoff 08→10→11).

Se vídeos ainda não existem, logar warning mas prosseguir — Stage 3 roda depois quando o membro disser "sobe os vídeos".

### Stage 4 — Automated Rule de PGS (opcional, nasce DESATIVADA)

Só criar se o membro aprovar explicitamente (mesma regra da Skill 10 ETAPA 6 — escala automática durante o TESTE é o anti-pattern que a 10/11 proíbem; PGS é assunto pós-winner, Skill 12):

```
if membro aprovou PGS:
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
      status="DISABLED"  // NUNCA ENABLED no launch — membro ativa junto com a campanha, quando fizer sentido
    )
```

Gravar a escolha em `pgs_enabled` (dados.json da 10 / manifest) — `true` só quando a rule foi criada E o membro a ativou no Ads Manager. Se recusou ou o MCP não suporta: pular, `pgs_enabled: false`.

### Stage 5 — Initial sync (cascade interno da receita de sync)

Snapshot do estado zero:

```
invoke_recipe("sync-campaign-from-meta", {
  campaign_name: strategy.campaign.name,
  date_preset: "today"
})
```

A receita de sync resolve sozinha o cascade (oficial → Pipeboard → devolve pro manual) e salva o baseline em `/workspace/[produto]/11-ad-analysis/raw-pull-[timestamp].json` com `source` declarado. Sem MCP Meta nenhum: logar warning — baseline será preenchido manualmente na primeira Skill 11.

### Stage 6 — Update manifest + log

```
manifest.update({
  "10_campaign_id": campaign_id,        // chaves que a Skill 11 lê (10-ad-strategy.md)
  "10_ad_set_id": ad_set_id,
  "shopify_product_id": result_1.product_id,
  "shopify_variant_ids": result_1.variant_ids,
  "full_deploy_completed_at": timestamp,
  "full_deploy_status": "paused_awaiting_approval"
})
```

Se a estrutura veio da Skill 10 (`mcp_creation`), os IDs já estavam no manifest — confirmar, não sobrescrever com null.

Log consolidado (shape — valores vêm dos arquivos do membro):
```json
{
  "timestamp": "<ISO timestamp>",
  "action": "full_deploy",
  "product_slug": "<do manifest>",
  "mode": "<staging|live|dry-run>",
  "stages_completed": 6,
  "shopify": {
    "product_id": "<Shopify GID>",
    "product_status": "draft",
    "variants_count": "<N>",
    "template_patched": true
  },
  "meta": {
    "campaign_id": "<id>",
    "campaign_status": "PAUSED",
    "structure": "1_campaign_1_adset_broad",
    "ads_uploaded": "<N>",
    "ads_pending_video": "<N>",
    "pgs_rule_created": "<true|false>",
    "pgs_rule_status": "DISABLED"
  },
  "next_steps": [
    "Produzir <N> vídeos faltantes",
    "Quando prontos: 'sobe os vídeos faltantes'",
    "Review Meta Ads Manager — tudo paused",
    "Activate: 'ativa a campanha <campaign_name>'"
  ]
}
```

Mensagem final ao membro (estrutura):
```
✓ FULL DEPLOY concluído — mode: <mode>

Shopify:
  ✓ Produto criado (draft): <product_name>
  ✓ <N> variants: <tier_list_com_preços>
  ✓ Variant IDs wired no template page.<product_slug>.json
  ✓ Tema atualizado (unpublished)

Meta Ads (tudo PAUSED):
  ✓ Campaign: <campaign_name> — 1 ad set broad/Advantage+, budget $<test_budget_daily>/dia no ad set
  ✓ <N> criativos uploaded (ads separados no mesmo ad set)
  ⏳ <N> criativos aguardando vídeos
  [se criada] ✓ PGS rule criada DESATIVADA — ativa no Ads Manager quando quiser (recomendado: só pós-winner)

Creative DNA Registry (estado herdado — o registro aconteceu na Skill 08 ETAPA 7.6, não neste deploy):
  · <N> criativos registrados pela Skill 08 ETAPA 7.6, com features extraídas
  ⏳ Performance update virá via Skill 11 após 3 dias

Quando quiser:
  - "sobe os vídeos faltantes" (quando produzir)
  - "review Meta Ads Manager" (pra checar tudo paused)
  - "ativa a campanha <campaign_name>" (GO — e aí: 3 dias sem mexer)
  - "ad analysis" (depois de 3+ dias de dados)
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

- Stage 1 (Shopify): 30-60s
- Stage 2 (Meta setup): 30-60s (ou 0s, se a Skill 10 já criou)
- Stage 3 (upload vídeos — só os existentes): 20-40s por vídeo
- Stage 4 (PGS, se aprovada): 10-20s
- Stage 5 (sync): 20-30s
- **Total: 2-5 minutos** pra campanha típica de 1 ad set × 5-8 ads
