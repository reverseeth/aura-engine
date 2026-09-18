---
name: ad-analysis
description: Diagnóstico e decisão sobre a campanha de teste no Meta Ads, depois de 3 a 7 dias de veiculação. Lê a estrutura da ad-strategy (ad set = conceito, ad = criativo), puxa os dados pela cascade Meta MCP oficial → Pipeboard → manual, cruza com o ad-log, roda o 4Pi (Spend → Frequency → CPM → Cost per Result), classifica cada criativo nas 4 classes do cânone ad-taxonomy (só breakthrough libera escala e reciclagem) e aplica as réguas de kill, mede Hook e Hold rate, diagnostica funil quebrado e página pelo espécime da copy, extrai learnings, calcula PSM real e share de compras em 7-day click e devolve NEXT_BATCH_IDEAS.md pra creative-engine. Sem corte de spend por queda de ROAS fora da espiral do ROAS (cânone unit-economics). Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "ver resultado", "diagnóstico", ou depois de rodar a campanha da ad-strategy.
---

# Ad Analysis · Passo 17 · apelido antigo: 11 <!-- gen:title -->

## Quando usar

Quando a campanha está rodando e o membro precisa diagnosticar o que acontece e decidir os próximos passos. Não é "reportar dados": é diagnóstico mais decisão, com ações concretas (hoje, 3 a 7 dias, 2 a 4 semanas). A leitura é em dois níveis: entre ad sets (qual CONCEITO o CBO financiou) e entre os 3 ads do ad set (execução ou ângulo, pelo `testing_method`).

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Playbook (a camada de execução manda na decisão de kill)

Leia `reference/playbook.md` antes de classificar ou recomendar corte. Seis itens: (0) os cânones `.claude/lib/ad-taxonomy/README.md` (classes §2, kill §3, Hook e Hold §4) e `.claude/lib/unit-economics/README.md` (espiral do ROAS §4) vencem o playbook onde divergirem. (1) Kill de criativo pelas três réguas do §3 (conta madura, conta nova e ad novo overspendando), com a carência de cada uma. CTR não decide, a média da janela decide, 2+ checkouts seguram. (2) CPM é saúde da CONTA: testar em outra conta antes de matar produto. (3) Os benchmarks de funil do arquivo separam criativo de página. (4) Só breakthrough (KPI do ad melhor que o da CAMPANHA e puxando spend) escala; `kpi_winner` é loser para decisão. (5) Nenhuma recomendação de cortar spend por ROAS sem os custos fixos na mesa; com `finance-engine/dados.json`, o `roas_spiral.verdict` decide pela tabela do arquivo. (6) Teste nascido abaixo do piso (`below_floor_directional_only`) é resultado direcional: sem `ad_class`, sem kill, sem escala.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

- [ ] `ad-strategy/dados.json` existe
- [ ] `workspace/[produto]/ad-analysis/` existe (`mkdir -p`)
- [ ] Análises anteriores: as 2 a 3 mais recentes e o `dados.json` consolidado

`ad-strategy/dados.json` faltando (ES1): oferecer (A) rodar a `ad-strategy` agora ou (B) seguir com target provisório (`breakeven_cpa` da `offer-builder`, mais frouxo, classificações otimistas) marcando `manifest.skipped_preflight`. Profile e manifest ausentes: oferecer o `setup` inline. Íntegra em `reference/contexto.md`.

## Contexto a carregar

Leia nesta ordem (detalhe em `reference/contexto.md`). Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar; sem `resumo`, leia inteiro.

1. `workspace/profile.md` (budget, `report_language`) e `offer-builder/offer-builder.md` (fallback legado `relatorio.md`) mais `offer-builder/dados.json`: `unit_economics` (target, breakeven, `cac_basis`, `cogs_breakdown`) e `budget_viability.fixed_costs_monthly`
2. `ad-strategy/ad-strategy.md` e `ad-strategy/dados.json`: estrutura, `protections`, `test_capacity` (`binding_constraint`, `below_floor_directional_only`)
3. `ad-analysis/` anterior, se existir
4. Se existirem: `copy-engine/dados.json` (`voc_forced_continue`, `specimen_primary`, `markup_audit`), `finance-engine/dados.json` (`roas_spiral`, que ela produz e esta skill só lê), `creative-engine/dados.json → concepts[]` (`testing_method`, `angles[]`, `sub_avatar_id`, zona emocional, `iteration_of`) e `creator-engine/dados.json → performance_by_creator`
5. `workspace/[produto]/ad-log.md`, SEMPRE (cânone `.claude/lib/ad-log/README.md`): cruzar a janela com as mudanças executadas; mudança relatada pelo membro entra no log na hora com executor `membro`
6. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill ad-analysis --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas por etapa; as queries embutidas em `reference/` são o mínimo garantido; nunca query genérica nem busca repetida

Batch anterior a esses contratos: leitura por execução, zona `unknown`, sub-avatar `null`; nada trava, nada é inventado. Idioma: output interno e conversa no `report_language`; copy e VOC literal sempre em inglês US.

## Fluxo da skill

### ETAPA 0.5 · ETAPA 0.6 · MCPs opcionais

Com tools `mcp__trendtrack__` ou `mcp__foreplay__`, leia `reference/mcps-opcionais.md`: benchmark dos breakthroughs contra o mercado (1 a 3 chamadas; nunca em `kpi_winner` nem em loser) e contexto pro `NEXT_BATCH_IDEAS.md`. Sem MCP, siga.

### ETAPA 1 · Obter dados (cascade oficial → Pipeboard → manual)

Leia `reference/obter-dados.md`. Caminho 1: tools `mcp__meta__ads_*` e conta não "disabled", receita `sync-campaign-from-meta.md`, pull em `raw-pull-[timestamp].json`. Caminho 2: `mcp__meta-ads__*` (Pipeboard), mesma receita com `force_path` e `fallback_reason`. Caminho 3: erros em `mcp-errors.log` e pedido ao membro dos números por AD (spend, frequency, CPM, CPC, CPA, ROAS, ATC, checkouts, dias). O cabeçalho do relatório declara o modo. Com pull oficial, integre benchmark da vertical, anomalias, auction ranking e opportunity score (higiene, nunca comando: não desligue o CBO nem junte conceitos) e marque warning se `match_quality_score < 6.0`.

### ETAPA 2 · 4Pi Analysis (ordem exata)

Leia `reference/decision-thresholds.md` e fixe uma vez o bloco Decision Thresholds: `breakeven_cpa`, `target` = `target_cpa_primary_2x`, COGS = somatório de todas as chaves de `cogs_breakdown`, `fair_share`, KPI da campanha na janela de 7 dias (`campaign_cpa`, `spend_share_7d`, `ad_kpi_vs_campaign`; menos de ~50 conversões = comparação preliminar), PSM real = LTV ÷ (CAC_real + COGS) com CAC do Shopify (proxy de plataforma marca `psm_real_basis`), as réguas de kill, a fórmula das 4 classes com benchmarks, `hit_rate` e `breakthrough_rate`. Cheque dados insuficientes, CPM subindo, montanha-russa (ad log primeiro) e winner picking. Depois leia `reference/quatro-pi.md` e aplique Spend → Frequency (diária) → CPM (com freq; `account_cpm_suspect`) → Cost per Result (classificação e réguas de kill; breakdown por placement). Meça Hook rate e Hold rate por criativo (onde falhou, nunca critério de kill). Grave `psm_real` e `click_based_purchase_share` (nunca estimado).

### ETAPA 3 · Diagnóstico por ad (criativo)

Leia `reference/diagnostico-por-ad.md`. Grave `ad_class` por ad com o `concept_id` (e por creator, quando o nome do ad traz o sufixo). Gate de piso: análise direcional não grava classe. Sniper responde "qual execução venceu"; Marksman, "qual ângulo venceu", nomeado pela frase de `angles[]`, com os 3 strikes do Execution Problem antes de enterrar um ângulo e a próxima entrada em Sniper. Ação por classe e estado (breakthrough, spend winner, KPI winner, fadiga com refresh em 2 a 4 semanas, loser, funil quebrado, conta suspeita, aprendizado). Checkpoint de kill de produto no domingo: piso, funil, conta, entrega, nessa ordem; produto só morre com 2+ batches processados ou régua do §3.

### ETAPA 4 · Diagnóstico profundo de losers

Leia `reference/diagnostico-de-losers.md`. 19-Point em cinco camadas para todo `loser`, `kpi_winner` e `spend_winner`, entrando na camada de hook com Hook e Hold já medidos. Para toda iteração que fracassou, `iteration_zone_check`: zona igual, a variável explica; zona mudou, a causa é a zona e a diretiva é refazer na zona original.

### ETAPA 5 · Diagnóstico de breakthroughs

Leia `reference/breakthroughs.md`. Learnings só de `breakthrough`: o que, por que, qual variável do mapa da `creative-engine`, como replicar, iteração de UMA variável, onde ganhou (hook ou hold), `winning_sub_avatar_id`, learning sobre o CLIENTE, AI Ad Review como segunda opinião. Recomende a mini-passada da `market-research` no ângulo vencedor.

### ETAPA 6 · Saúde do funil

Leia `reference/saude-do-funil.md`. 6A posição pelas signatures. 6B conversão com amostra mínima (dez checkouts ou vinte ATC) antes de `funnel_broken`. 6C página pelo espécime (`specimen_fit`) e pela camada do markup audit já reprovada, com a tabela de roteamento. 6D `voc_forced_continue` muda a hipótese para VOC insuficiente.

### ETAPA 7 · 15 perguntas de feedback

Leia `reference/perguntas-e-recomendacoes.md` e responda as 15 perguntas num bloco objetivo, incluindo hook vs hold, `breakthrough_rate` e os achados do ad log.

### ETAPA 8 · Recomendações acionáveis

Mesmo arquivo. Imediato (pausar losers por nome, técnico, conferir as duas automações de proteção e o daily maximum), curto prazo (fadiga, funil, placement) e médio prazo (breakthrough pronto pra ABO pela `scale-engine`, oferta, página). Qualquer ação que reduza spend passa antes pela espiral do ROAS.

### ETAPA 9 · Decisão de scaling

Leia `reference/decisao-de-scaling.md`. Escala automática não existe em CBO; o que é automatizável já foi montado pela `ad-strategy`. Gates em ordem: piso (direcional vira `raise_budget_or_reduce_concepts`), escala (só com ≥ 1 `breakthrough`), corte (unit-economics §4 com os fixos). Use o texto do cenário.

### ETAPA 10 · Learnings documentados

Leia `reference/learnings-e-dna.md`. Hipóteses confirmadas por reaplicação, levantadas, rejeitadas, em teste e ideias pro próximo batch.

### ETAPA 11 · DNA update (silent)

Mesmo arquivo. Por criativo: `ad_class` mais o `outcome` legado pelo mapeamento fixo, perf JSON com Hook em `thumbstop_3s` e Hold em `hold_15s`, `registry.py update`; a cada 5 criativos a partir de 10, `registry.py dna`. Antes de persistir qualquer dump, redação de PII.

### NEXT_BATCH_IDEAS.md

Leia `reference/next-batch-ideas.md`. Critério de parada: com menos de 50% das ideias anteriores testadas, devolver a versão anterior com "Validation pending". Conteúdo obrigatório listado lá.

## SALVAR

Todo relatório `.md` ganha `.html` por `python3 tools/render_report.py <md>` (isentos: `NEXT_BATCH_IDEAS.md`, `raw-pull-*.json`, `mcp-errors.log`, `dados.json`). Em `workspace/[produto]/ad-analysis/`: `[YYYYMMDD]-analysis.md`, `ad-analysis.md` (cópia da última rodada), `NEXT_BATCH_IDEAS.md` e `dados.json` no schema de `reference/dados-json.md` (schema em `.claude/templates/schemas/`). Depois `python3 tools/manifest.py <slug> complete ad-analysis` e `set` com os campos canônicos de `reference/dados-json.md` (`psm_real` e `psm_real_basis`, `ad_classification[]` substituindo o array inteiro, `click_based_purchase_share` só se medido, `breakthroughs[]` e o alias `winners[]`, as outras duas classes, `champions[]` em merge, datas, médias, `recommended_action` e sinais de saúde); então `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/salvar-e-mensagem-final.md`. Termine com a próxima ação clara: continuar rodando, `'scale'` (só com breakthrough, mais a re-research do ângulo vencedor), `'creatives'`, `'offer'`, `'copy'` ou `'page'`, a pergunta dos custos fixos (e `'finanças'`), o spend alvo quando o veredito é subir, ou o resultado direcional com a ação de subir o budget até o piso. Sem breakthrough, diga: "você ainda não tem um ad que escala".
