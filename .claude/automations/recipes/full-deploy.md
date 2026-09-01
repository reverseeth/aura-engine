# Recipe: Full Deploy (end-to-end)

Receita orquestradora que faz deploy completo de produto em Shopify + estrutura de campanha no Meta Ads, com um único comando do membro. Estrutura canônica de campanha: **1 campanha com CBO → N ad sets broad/Advantage+ (1 ad set = 1 conceito) → 3 criativos + 2 primary texts + 2 headlines cada** — a MESMA que a Skill 10 define e que o cânone `.claude/lib/ad-taxonomy/README.md` §1 governa; esta receita nunca inventa estrutura própria nem recalcula capacidade (quantos ad sets sobem já foi decidido na ETAPA 3.1 da Skill 10 e está gravado em `10-ad-strategy/dados.json`). Tudo nasce PAUSED (inclusive Automated Rules, que nascem DESATIVADAS) até aprovação humana.

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
- [ ] `10-ad-strategy/dados.json` com `campaign` (incluindo `budget_level: "campaign_cbo"` e `daily_budget`), `ad_sets[]` (uma entrada por conceito) e `test_budget_daily` definidos
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

### Stage 2 — Estrutura de campanha no Meta (1 campanha CBO → N ad sets → 3 ads cada)

Ler `strategy = 10-ad-strategy/dados.json`. **Primeiro, checar se a Skill 10 ETAPA 6 já criou a estrutura via MCP** (não duplicar):

```
if strategy.mcp_creation.status == "created_paused":
    campaign_id = strategy.mcp_creation.campaign_id
    ad_set_ids  = strategy.mcp_creation.ad_set_ids   // LISTA — um ID por conceito
    // estrutura já existe em PAUSED — pular pra Stage 3
else:
    // criar agora, com os campos REAIS do schema da 10
    campaign = meta_ads.campaign.create(
      ad_account_id,
      name=strategy.campaign.name,
      objective="OUTCOME_SALES",
      status="PAUSED",
      special_ad_categories=[],
      buying_type="AUCTION",
      daily_budget=strategy.campaign.daily_budget * 100  // cents — CBO NA CAMPANHA
      // strategy.campaign.budget_level == "campaign_cbo", e daily_budget == strategy.test_budget_daily.
      // Se os dois divergirem, PARAR e reportar: a Skill 10 é a fonte do número,
      // esta receita nunca recalcula budget nem capacidade.
      // (budget na campanha E no ad set ao mesmo tempo é rejeitado pela Marketing API —
      //  por isso os ad sets abaixo sobem SEM budget próprio)
    )

    ad_set_ids = []
    for entry in strategy.ad_sets:   // uma entrada por conceito: concept_id, angle, name, daily_max_spending_limit
        ad_set = meta_ads.ad_set.create(
          campaign.id,
          name=entry.name,
          // SEM daily_budget / lifetime_budget: o budget vive na campanha (CBO)
          daily_spend_cap=entry.daily_max_spending_limit * 100,
          // cents — é o "Ad set spending limit → daily maximum" do Ads Manager: TETO de proteção
          // (~3× target CPA, cânone §1), nunca piso. Daily MINIMUM continua proibido (Skill 10 ETAPA 7).
          optimization_goal="OFFSITE_CONVERSIONS",        // Purchase
          billing_event="IMPRESSIONS",
          bid_strategy="LOWEST_COST_WITHOUT_CAP",
          targeting={
            // IDÊNTICO em todos os ad sets — a variável do teste é o CONCEITO, não a audiência.
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
        ad_set_ids.append(ad_set.id)
        entry.ad_set_id = ad_set.id   // devolver pro `ad_sets[]` do 10-ad-strategy/dados.json
```

`resolved_pixel_id`: via `mcp__meta__ads_get_dataset_details` (oficial) ou, sem o oficial, perguntar 1× ao membro (Events Manager → Data Sources) e gravar `manifest.meta_pixel_id` pra reuso (mesma chave que `upload-creative-to-meta.md` usa).

> **Regra estrutural (Skill 10 ETAPA 7):** NÃO subir mais ad sets do que `strategy.ad_sets[]` traz (a capacidade já foi calculada na ETAPA 3.1 pela régua do cânone §1 — esta receita aplica, não recalcula), NÃO misturar 2 conceitos no mesmo ad set, NÃO adicionar interests (o criativo faz o targeting), NÃO dar budget próprio a ad set (o CBO está na campanha) e NÃO usar daily **minimum** — o único controle de budget no nível do ad set é o daily **maximum** de proteção acima. Diversificação em campanhas ABO paralelas é assunto da Skill 12 (escala, cânone §5), não desta receita.

### Stage 3 — Upload criativos (se .mp4 existirem)

Convenção real da Skill 08: vídeos renderizados vivem em `/workspace/[produto]/08-creative-engine/renders/`, **um arquivo por EXECUÇÃO do pack 3-2-2** — `c0X-[creative-n].mp4` (geração contínua) ou `c0X-[creative-n]-shot-N.mp4` (split em takes). A fonte dos paths é a lista `concepts[].production_prompts.video.rendered_files[]` do `08-creative-engine/dados.json` — 1 item por execução, `{creative_n: 1..3, file}`, com `file: null` pra execução ainda não renderizada. **Fallback legado:** produto antigo sem `rendered_files[]` tem só o escalar `rendered_file` (1 arquivo por CONCEITO, nomes `c0X.mp4`/`c0X-shot-N.mp4`) — use esse arquivo como execução 1 e peça ao membro os paths das outras execuções. Se o membro editou fora (CapCut etc.), pedir os paths finais.

Percorrer `strategy.ad_sets[]` e subir as execuções do pack de cada conceito **no ad set daquele conceito** — criativo de um conceito nunca entra no ad set de outro (é isso que mantém legível qual conceito funcionou):

```
for entry in strategy.ad_sets:                  // uma entrada = um conceito
    rendered = concepts[entry.concept_id].production_prompts.video.rendered_files
               // legado sem a lista: montar [{creative_n: 1, file: rendered_file}] + paths que o membro passar
    for item in rendered where item.file != null:   // item.creative_n = 1..3, na ordem do pack
        invoke_recipe("upload-creative-to-meta", {
          creative_id: "<entry.concept_id>",
          ad_set_name: entry.name,              // o ad set DAQUELE conceito
          video_path: "/workspace/[produto]/08-creative-engine/<item.file>",   // file já vem com "renders/"
          status: "PAUSED"
        })
        entry.ad_ids.append(<ad id retornado>)  // devolver pro `ad_sets[]` do 10-ad-strategy/dados.json
```

Ad Name segue a convenção da 10: `[concept_id]_[creative-n]_[YYYYMMDD]` (ex: `RootCauseAngle_2_20260620`). O `concept_id` preserva o handoff 08→10→11 e o índice `n` (o `creative_n` do item de `rendered_files[]` — 1..3, na ordem das execuções do pack) mantém os 3 ads do conceito distinguíveis no relatório — sem ele, os 3 ads de um mesmo conceito colidiriam no nome. O `utm_content` acompanha, `[concept-id]-[creative-n]`, um por criativo (schema da Skill 10 ETAPA 3.3): nunca subir 2 ads com o mesmo `utm_content`.

Se vídeos ainda não existem, logar warning mas prosseguir — Stage 3 roda depois quando o membro disser "sobe os vídeos".

### Stage 4 — Proteções obrigatórias (as duas do cânone §6, nascem DESATIVADAS)

**Automated Rule de PGS não existe nesta estrutura.** Regra com condição de performance (CPA, ROAS, frequency) é **recusada pelo Meta** em campanha que usa CBO — o erro retornado é literalmente *"performance-related conditions are not available for assets that use CBO"*. Não oferecer, não tentar criar, não prometer ao membro. O teto que substitui o PGS é o `daily maximum` por ad set, já criado no Stage 2.

O que entra aqui são as **duas automações de proteção obrigatórias** do cânone `.claude/lib/ad-taxonomy/README.md` §6. Elas não são opcionais como a antiga PGS (são doutrina), mas nascem **DESATIVADAS** — o membro ativa junto com a campanha:

```
// A — pico de gasto: protege contra conta comprometida e contra um zero a mais digitado no budget
meta_ads.automated_rule.create(
  ad_account_id,
  name="AURA_Spend_Spike_Guard",
  evaluation_spec={ ...spend das últimas 24h ≥ 5× o spend do período anterior equivalente... },
  execution_spec={"execution_type": "PAUSE"},   // pausa os ads/ad sets que dispararam
  status="DISABLED"
)

// B — URL de destino errada: protege contra ad rodando pra página errada, removida ou de terceiro
meta_ads.automated_rule.create(
  ad_account_id,
  name="AURA_URL_Mismatch_Guard",
  evaluation_spec={ ...destination URL do ad ≠ domínio de manifest.storefront.page_url... },
  execution_spec={"execution_type": "PAUSE"},   // desliga o ad
  status="DISABLED"
)
```

Se o caminho MCP ativo não criar a rule ou não expuser a condição, **não improvisar com condição de performance como substituto** (o Meta recusaria de qualquer jeito em CBO): entregar o passo-a-passo pro membro montar em Ads Manager > Automated Rules e marcar `created: false`. A proteção não é opcional por doutrina — só por limite de ferramenta.

> **Kill automatizado por performance NÃO se faz** — nem aqui, nem na 11, nem na 12. Duas razões independentes: (a) tecnicamente o Meta não aceita a condição em CBO; (b) mesmo onde aceitasse, a métrica do Ads Manager engana — um ad a 1× ROAS na plataforma pode estar excelente no 1-day click de uma ferramenta de atribuição de terceiro, e desligar por metadado mata winner. **Kill é leitura, não regra:** quem decide é a Skill 11, com as réguas do cânone §3.

Gravar no bloco `protections` (mesmo shape do `10-ad-strategy/dados.json`) o que foi efetivamente criado:

```json
"protections": {
  "adset_daily_maximum": { "enabled": true, "value_per_adset": "<daily_max_spending_limit>", "basis": "3x_target_cpa" },
  "spend_spike_rule":    { "created": false, "active": false, "condition": "spend_5x_24h", "action": "pause" },
  "url_mismatch_rule":   { "created": false, "active": false, "condition": "destination_url_not_store_domain", "action": "pause_ad" },
  "automated_performance_kill": false,
  "automated_performance_scaling": false
}
```

`automated_performance_kill` e `automated_performance_scaling` ficam `false` SEMPRE — não são configuráveis, são o registro explícito de que essa automação não existe nesta estrutura. `pgs_enabled` permanece no dados.json/manifest **fixo em `false`** (campo de compatibilidade): com `false`, esta receita e a Skill 11 degradam pro comportamento certo — não prometem escala automática ao membro. Nunca gravar `true`.

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
  "10_ad_set_ids": ad_set_ids,          // LISTA — um ID por conceito; é por aqui que a 11 puxa insights por conceito
  "10_ad_set_id": ad_set_ids[0],        // compat: primeiro ad set, pras receitas que ainda esperam o campo único
  "pgs_enabled": false,                 // fixo — Automated Rule de performance não existe em CBO (Stage 4)
  "shopify_product_id": result_1.product_id,
  "shopify_variant_ids": result_1.variant_ids,
  "full_deploy_completed_at": timestamp,
  "full_deploy_status": "paused_awaiting_approval"
})
```

Devolver também pro `10-ad-strategy/dados.json` o `ad_set_id` e os `ad_ids` de cada entrada de `ad_sets[]` (preenchidos nos Stages 2 e 3) e o bloco `protections` do Stage 4 — é o estado que a Skill 11 lê pra saber o que existe de verdade na conta.

Se a estrutura veio da Skill 10 (`mcp_creation`), os IDs já estavam no manifest — confirmar, não sobrescrever com null nem truncar a lista `10_ad_set_ids` para um único ID.

**Ad log (cânone `.claude/lib/ad-log/README.md`) — na MESMA execução:** append em `workspace/[produto]/ad-log.md` (criar com o cabeçalho da tabela se não existir), uma linha por mudança que ESTE deploy executou na conta — a campanha, cada ad set, as duas automated rules. Os ads são registrados pela sub-receita de upload no Stage 3 (não duplicar aqui). O que a Skill 10 já criou antes (`mcp_creation`) também não entra — ela mesma logou na hora. Modo `dry-run` não escreve nada (nenhuma mudança real aconteceu).

```
| YYYY-MM-DD HH:MM | campaign:[nome] | criada em PAUSED (CBO $[test_budget_daily]/dia) | recipe:full-deploy | full deploy inicial |
| YYYY-MM-DD HH:MM | adset:[concept_id] | criado em PAUSED (daily maximum $[limite]/dia) | recipe:full-deploy | full deploy inicial |
| YYYY-MM-DD HH:MM | automation:AURA_Spend_Spike_Guard | criada DESATIVADA | recipe:full-deploy | proteção obrigatória cânone §6 |
| YYYY-MM-DD HH:MM | automation:AURA_URL_Mismatch_Guard | criada DESATIVADA | recipe:full-deploy | proteção obrigatória cânone §6 |
```

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
    "structure": "1_campaign_cbo_1_adset_per_concept",
    "budget_level": "campaign_cbo",
    "daily_budget": "<test_budget_daily>",
    "ad_sets_created": "<N>",
    "ad_set_ids": ["<id por conceito>"],
    "ads_uploaded": "<N>",
    "ads_pending_video": "<N>",
    "protections": {
      "adset_daily_maximum": "<valor por ad set>",
      "spend_spike_rule": "<created|manual_steps>",
      "url_mismatch_rule": "<created|manual_steps>",
      "rules_status": "DISABLED",
      "automated_performance_kill": false
    }
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
  ✓ Campaign: <campaign_name> — budget $<test_budget_daily>/dia NA CAMPANHA (CBO)
  ✓ <N> ad sets broad/Advantage+, um por conceito (<lista dos concept_ids>) — sem budget próprio,
    cada um com teto de gasto de $<daily_max_spending_limit>/dia
  ✓ <N> criativos uploaded (3 por conceito, cada um no ad set do seu conceito)
  ⏳ <N> criativos aguardando vídeos
  ✓ Proteções criadas DESATIVADAS: pico de gasto (5× em 24h → pausa) e URL de destino
    fora do domínio da loja (→ desliga o ad). Ative junto com a campanha.
    [se o MCP não criou: passo-a-passo pra montar em Ads Manager > Automated Rules]
  · Kill e escala automáticos por performance não existem aqui — quem lê e decide é a
    "ad analysis" (Skill 11), depois de 3 dias de dados

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
- Stage 2 (Meta setup — campanha + N ad sets): 30-60s (ou 0s, se a Skill 10 já criou)
- Stage 3 (upload vídeos — só os existentes): 20-40s por vídeo
- Stage 4 (proteções): 10-20s
- Stage 5 (sync): 20-30s
- **Total: 2-5 minutos** pra campanha típica de N ad sets × 3 ads (N = `adsets_planned` da Skill 10)
