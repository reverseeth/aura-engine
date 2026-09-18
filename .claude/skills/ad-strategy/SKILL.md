---
name: ad-strategy
description: Configuração e criação da estrutura de teste no Meta Ads Manager. Uma campanha com CBO (Advantage+ broad, Max Conversion) → um ad set por conceito (3 criativos, 2 primary texts e 2 headlines), cada ad set com o testing_method do conceito lido da creative-engine e o destino de página do mapeamento de congruência (fallback na URL canônica do manifest), com o número de conceitos governado pela capacidade de teste do cânone ad-taxonomy (criativos = budget diário ÷ target CPA, piso e tetos), 3 dias sem mexer, uma conta por produto, warmup de conta nova e cadência de quarta a domingo, com o domingo como checkpoint de decisão informada pela ad-analysis. Cria tudo em PAUSED via Meta Ads MCP, com gates de pré-launch, leitura de credibilidade da loja e as proteções que funcionam em CBO. Use quando o membro disser "ad strategy", "estratégia de ads", "montar campanha", "setup Meta Ads", "configurar campanha", ou depois dos briefings de criativos prontos.
---

# Ad Strategy · Passo 16 · apelido antigo: 10 <!-- gen:title -->

## Quando usar

Quando o membro tem criativos prontos (`creative-engine`), página publicada (`page-design` e `page-build`), tracking validado (`tracking-setup`) e oferta ativa (`offer-builder`), e precisa configurar e criar a estrutura de teste no Meta Ads Manager. É a camada de execução: monta a campanha exata e a cria em PAUSED pro membro revisar e ativar.

Cânone: `.claude/lib/ad-taxonomy/README.md`, §1 (capacidade de teste e estrutura), §6 (automações) e §7 (métodos de teste). Onde o texto divergir do cânone, o cânone vence. Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

- [ ] `creative-engine/dados.json`: cada conceito vira um ad set (handoff `concepts[].id` e `concepts[].testing_method`); quantos entram é a capacidade da 3.1, não o tamanho do batch
- [ ] `offer-builder/dados.json`: `unit_economics.target_cpa_primary_2x` (target), `weighted_margin_per_order` (breakeven), `breakeven_roas`; `manifest.target_cpa` e `manifest.breakeven_roas` prevalecem quando existem (a `checkout-aov` atualiza)
- [ ] `workspace/profile.md` e `manifest.budget_daily` (o budget diário canônico)
- [ ] `manifest.margin_warning`: se `true`, ficar no piso operacional e cortar conceitos, nunca esticar budget
- [ ] `manifest.tracking.tracking_ready == true` (Pixel e CAPI, EMQ de 6.0 ou mais; `emq_pending: true` aceito em loja pré-launch, com a `ad-analysis` relendo o EMQ no dia 3); senão, redirecionar pra 'tracking'
- [ ] `manifest.storefront.page_url` preenchido; senão, redirecionar pra 'build page'

Arquivo crítico ausente (ES1 e ES2): (A) re-rodar a skill que o gera ou (B) seguir com default marcando `manifest.skipped_preflight`.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`) em todo output interno; copy de ad e VOC literal sempre em inglês US. Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar; sem `resumo`, leia inteiro.
2. `offer-builder/offer-builder.md` (legado `relatorio.md`) e `dados.json`: target CPA e breakeven CPA pelos campos diretos, sem re-derivar; só na falta, os fallbacks com `data_gap`. O target passa pela checagem do piso físico de CAC (item 1b da 3.1) antes de virar setpoint.
3. `finance-engine/dados.json` se existir, bloco `cac` (`cac_floor_reference_usd`, `cac_max_first_order`, `target_reachable_vs_floor`): esta skill lê e aplica, nunca recalcula; ausente ou `unknown`, o target entra direto.
4. O cânone (§1, §6, §7), a URL canônica `manifest.storefront.page_url` (nunca a do relatório da `copy-engine`), `creative-engine/dados.json` com o mapeamento de congruência da ETAPA 6 dela, e o stage do membro, que define tom e não número de criativos.
5. Analytics stack é decisão da `tracking-setup`: `manifest.tracking.tracking_ready` e `analytics_stack` precisam existir, senão parar e mandar pra 'tracking'.
6. Base pelo índice (domínios `meta-ads-strategy` e `persuasion-psychology`): `python3 .claude/lib/kb-index/kb_lookup.py --skill ad-strategy --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas por etapa; as queries embutidas em `reference/` são o mínimo garantido; nunca query genérica nem busca repetida. Os quatro sistemas de leitura estão em `reference/contexto.md`.

## Fluxo da skill

### ETAPA 1 · Gates de pré-launch (bloqueantes)

Leia `reference/gates-pre-launch.md`. `consistency-audit/dados.json`: `BLOCK` aborta (só segue com pedido explícito, registrado em `skipped_preflight`); `CAUTION` pede OK explícito; `GO` segue; arquivo ausente = rodar a `consistency-audit` inline por default, avisando o membro. Metadados limpos (regra 12): só sobe arquivo `asset-xxxx`; outro nome passa antes por `bash tools/strip-metadata.sh <arquivo>`.

### ETAPA 2 · Leitura de credibilidade da loja

Leia `reference/credibilidade-da-loja.md`. Checklist de leitura (WARN, não bloqueia) fundamentado nos sistemas do arquivo: Instagram e página do Facebook ativos, cerca de 100 reviews na PDP, sinais de confiança visíveis, flows de recuperação da `retention-engine` Fase A ativos (`manifest.retention.phase_a_done`), rotina de gestão de comentários. Zero reviews: o playbook legítimo de 4 passos do arquivo. Proibido comprar reviews, importar reviews de outro produto ou condicionar incentivo a nota positiva. Starter sem prova social: rodar pequeno enquanto acumula review.

### ETAPA 3 · Capacidade de teste e estrutura (o playbook)

Leia `reference/playbook-e-sistemas.md` e puxe os sistemas que ancoram a estrutura. Uma campanha com CBO, um conceito por ad set, audiência broad: onde o CBO concentra gasto é o sinal que a `ad-analysis` lê.

- **3.1 Capacidade** (`reference/capacidade-de-teste.md`): `max_assets = floor(budget ÷ target_cpa)` e `max_adsets = floor(budget ÷ (3 × target_cpa))`. Quatro restrições juntas: piso de US$ 100 a 150 por dia, teto de cerca de 3× o target CPA por ad set, no máximo 5 ad sets abaixo de US$ 1k por dia, ad sets nunca acima dos conceitos disponíveis. Ordem de cálculo gravada no `dados.json`: `target_cpa`; 1b, veredito `target_reachable_vs_floor` (`no` = calcular também a capacidade pelo piso de CAC, mostrar os dois números, apontar a correção pra `offer-builder` e rodar pela conservadora com `cac_floor_check.binding: true`); `budget_diário`; `max_assets` e `max_adsets`; `adsets_planejados = min(max_adsets, conceitos, 5 abaixo de US$ 1k)`; `test_budget_daily`; `assets_planejados`. Casos de contorno: `max_assets < 3` = um conceito por vez em fila; budget abaixo do piso = (a) adiar ou (b) um conceito só, resultado direcional que não autoriza kill nem escala; capacidade maior que o batch = mais conceitos na `creative-engine`, nunca budget a mais nos mesmos ad sets; `margin_warning` = piso e menos conceitos. O stage apresenta os caminhos, não define o número.
- **3.2 Método** (`reference/metodo-de-teste.md`): o método se lê de `concepts[].testing_method`, conceito a conceito (batch misto vira `test_method: mixed`); batch legado sem o campo grava `sniper` em todos com `data_gap`, nunca reclassifica como Marksman. Marksman acontece dentro de um ad set (3 ângulos num pack); Sniper é um ângulo em 3 execuções. O método não muda o número de ad sets. Dois conceitos com a mesma embalagem da mesma razão de compra: o mais forte entra, o outro espera.
- **3.3 Estrutura** (`reference/estrutura-da-campanha.md`): campanha `[Produto]_[YYYYMMDD]_Test`, objetivo Sales, CBO ligado com `daily_budget = test_budget_daily`, uma conta por produto. Ad sets `[Produto]_[concept_id]_[YYYYMMDD]`, otimização Purchase (sem descer pra ViewContent), sem budget próprio (só o daily maximum da ETAPA 6), um pack 3-2-2 por ad set, audiência idêntica e broad (Advantage+ sem interests, placements automáticos, 7-day click e 1-day view, sem Incremental Attribution). Ads `[concept_id]_[creative-n]_[YYYYMMDD]`, diversidade genuína entre conceitos, CTA Shop Now ou Learn More, URL = destino do conceito pelo mapeamento da `creative-engine` com fallback na URL canônica (sempre página publicada), UTM pelo schema do arquivo (`utm_content` por criativo, `utm_term` e `utm_id` por macro). Eixo de página 3:2:2:2 só com budget de US$ 2k por dia ou mais e 2 páginas publicadas, lido por KPI. Batch maior que a capacidade: priorizar ângulos distintos, guardar o resto, nunca comprimir dois conceitos num ad set.

### ETAPA 4 · Warmup de conta nova

Leia `reference/warmup-e-cadencia.md`. Conta nova: 3 dias de campanha de engajamento (US$ 50 por dia ou o budget do membro, o menor) começando no domingo, pra que o Day 4 caia na quarta. Conta com histórico de Purchase pula. Warmup é higiene legítima; account farming e contingência pra driblar ban não existem aqui.

### ETAPA 5 · Cadência de teste e janela de decisão

Mesmo arquivo. Três dias sem mexer. Lançar quarta, deixar até domingo; 7 dias é o teto por ad set (cânone §3). Domingo é checkpoint de decisão informada com três coisas na mesa: réguas de kill do §3, checks de precedência da `ad-analysis` (funil, conta, entrega) e Execution Problem (um ângulo tem 3 tentativas). Produto só morre com 2 ou mais batches de learnings processados ou régua do cânone, nunca por calendário. Dias 1 a 3 só conferem entrega (ad set sem gasto sob CBO não é erro); a partir do dia 3, rodar a `ad-analysis`. Escala é da `scale-engine`, depois de um breakthrough.

### ETAPA 6 · Criação em PAUSED via Meta Ads MCP

Leia `reference/criacao-em-paused.md`. Cascade: MCP oficial (`mcp__meta__ads_*`), Pipeboard (`mcp__meta-ads__*`, obrigatório pro upload de binário), manual (passo a passo pra colar). Proteções (cânone §6): Automated Rule de performance não existe em CBO; entram o daily maximum por ad set (cerca de 3× o target CPA), a automação A (spend 5× em 24h pausa) e a automação B (URL fora do domínio da loja desliga o ad), gravadas em `protections`. Regras invioláveis: tudo nasce em PAUSED e rules desativadas; auditoria da ETAPA 1 antes; receitas `upload-creative-to-meta.md` e `setup-mcps.md`; guardar campaign_id, ad_set_ids por conceito e ad_ids; toda criação vira linha no `ad-log.md` na mesma execução (executor `skill-ad-strategy`; no manual, `membro`). Mensagem ao membro com o modelo do arquivo. Falha de MCP: ES6, backoff, depois (A) retomar em 1h ou (B) manual.

### ETAPA 7 · Erros comuns a evitar

Leia `reference/erros-comuns.md` e inclua os doze erros no checklist do relatório.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/ad-strategy/`; `ad-strategy.md` com os doze itens do arquivo; `.html` por `python3 tools/render_report.py <md>`; `dados.json` no schema de `reference/dados-json.md` (`test_capacity` com `binding_constraint` e `below_floor_directional_only`, `cac_floor_check`, `ad_sets[]` como lista com `testing_method`, `landing_url` e `daily_max_spending_limit`, `protections`, `pgs_enabled: false`). Depois `python3 tools/manifest.py <slug> complete ad-strategy` e `set` com `strategy_id`, `creative_batch_ref`, `test_budget_daily`, `target_cpa`, `breakeven_cpa`, `10_campaign_name`, `10_campaign_id`, `10_ad_set_ids`, `10_ad_set_id` e `pgs_enabled: false`; então `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft pra revisão: a estrutura criada em PAUSED com budget no nível da campanha e um ad set por conceito, por que N conceitos e não mais (a conta de capacidade em uma frase), o plano quarta a domingo com 3 dias sem mexer, o checkpoint de domingo com a leitura da `ad-analysis` decidindo kill e escala (nunca regra automática), a credibilidade da loja e a pergunta de ajuste.
