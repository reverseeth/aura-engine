---
name: ad-analysis
description: Engine de análise de performance de Meta Ads. Analisa NO NÍVEL DO AD (criativo) dentro do ad set único da estrutura 1-1-N da Skill 10. Aplica a REGRA DE KILL operacional (criativo gasta 1-2× o breakeven CPA sem venda → mata; CPA manda, não CTR), usa CPM como sinal de saúde da conta, diagnostica funil quebrado por benchmarks (ATC→compra, checkout→compra), e lê tudo por 4Pi (Spend → Frequency → CPM → Cost per Result) + PSM como diagnóstico. Faz 19-point diagnostic de losers, extração de learnings de winners, checklist de 12 perguntas de feedback, decide kill de produto (cadência quarta→domingo), e orienta a configuração real de PGS via Automated Rules. Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "ver resultado", "diagnóstico", ou após rodar a campanha da Skill 10. Entrega decisões concretas — matar criativo, testar produto em outra conta, escalar, refresh, ou ajustar oferta/página.
---

# Ad Analysis Engine

## Quando Usar
Quando a campanha está rodando e o membro precisa diagnosticar o que está acontecendo e decidir próximos passos. Esta skill NÃO é "reportar dados" — é **diagnóstico + decisão**. Sai com ações concretas (hoje / 3-7 dias / 2-4 semanas).

## PLAYBOOK — A camada de execução (decisão de KILL real)

A base Aura tem a TEORIA da leitura (4Pi, PSM). Este playbook é a camada de EXECUÇÃO operacional — exatamente o que decidir olhando o Ads Manager. Quando o playbook e a leitura teórica conflitam numa decisão de matar/manter criativo, **o playbook manda na decisão**; o 4Pi/PSM continuam como o RACIOCÍNIO que explica o porquê.

> Os números de breakeven CPA vêm de `04-offer-builder/dados.json` (`unit_economics.weighted_margin_per_order`). Toda regra abaixo é relativa a ESSE breakeven, não a um valor fixo.

**1. Regra de KILL de criativo (CPA manda, não CTR):**
- Criativo que **gastou 1-2× o breakeven CPA SEM nenhuma venda → pausa.** Esse é o gatilho operacional padrão.
- **CTR alto sem venda não salva o criativo.** Um criativo pode ter scroll-stop ótimo, CTR alto, e mesmo assim não converter — se não vende dentro de 1-2× breakeven CPA, morre. O que paga a conta é a compra, não o clique.
- **Exceção — 2+ checkouts no comecinho:** se o criativo já gerou 2+ initiate-checkouts (mesmo sem venda fechada), o Meta tem sinal pra otimizar. Deixa rodar mais um pouco antes de matar.
- **Produto já validado** (outro criativo já vende): criativo novo que gasta sem vender, **mata rápido** — outro vende, não há motivo pra carregar peso morto.

**2. CPM = sinal de saúde da CONTA (não do produto):**
- O MESMO produto/criativo pode dar **CPM $30 numa conta e $100 noutra.** CPM alto demais geralmente é a conta, não o produto.
- Antes de declarar um produto "morto" por CPM alto, **testar o mesmo produto/criativo em OUTRA conta de anúncio.** Só depois de não validar em conta nenhuma é que se mata o PRODUTO.
- Isso muda a ordem da decisão: CPM muito acima do esperado do nicho → primeiro suspeitar da conta (resiliência: ter conta reserva legítima ajuda aqui), não do criativo.

**3. Benchmarks de funil (diagnóstico de funil quebrado — separa criativo de página/oferta):**
- **Add-to-cart → compra = 20-25%** (a cada 10 ATC, ~2 compras fecham).
- **Checkout → compra = 40-50%** (média ~40%; iniciou checkout e finalizou).
- **Abaixo desses números = o bloqueio é funil/página/oferta, NÃO necessariamente o criativo.** Ex: criativo trouxe 3 checkouts e 0 venda → sinal de página/checkout, não do ad. Mas atenção à amostra: 0 venda em 3 checkouts acontece por puro acaso ~1 vez em 5 mesmo com funil saudável — só decrete "funil quebrado" com a amostra mínima da ETAPA 6B. Não mate o criativo por algo que é culpa da página.
- Esse cruzamento evita o erro caro de matar um criativo bom porque a página converte mal.

## Antes de Começar

### Pré-flight
- [ ] `10-ad-strategy/dados.json` existe
- [ ] Dir `workspace/[produto]/11-ad-analysis/` existe (`mkdir -p`)
- [ ] Se houver análises anteriores, ler **as 2-3 mais recentes** + o `dados.json` consolidado (para delta/trend analysis). Ler todas só quando a análise pedir tendência longa (ex: sazonalidade de CPM).

> **report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

> **Se `10-ad-strategy/dados.json` faltar:** não aborte seco. Ofereça (A) rodar a skill 10 agora pra gerar a estratégia, OU (B) prosseguir com targets genéricos (CPA provisório = `breakeven_cpa` do `04-offer-builder/dados.json` se existir, senão default conservador — **avisando que esse target provisório é 2× mais frouxo que o target normal `target_cpa_2x`**, então as classificações saem otimistas) marcando `manifest.skipped_preflight += ["10-ad-strategy/dados.json"]` e avisando no output final que recomenda re-executar. Se profile/manifest estiverem TOTALMENTE ausentes, ofereça rodar o setup (skill 00) inline.

### Contexto a carregar

1. Leia `workspace/profile.md` (budget — contexto pra decisões de scale)
2. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (target CPA, breakeven ROAS, margem — benchmarks pra avaliar performance; se não existir, leia o legado `relatorio.md`)
3. Leia `workspace/[produto]/10-ad-strategy/ad-strategy.md` (estrutura da campanha, conceitos testados, regras de decisão)
4. Leia `workspace/[produto]/11-ad-analysis/` — **SE EXISTIR**, leia as **2-3 análises mais recentes** + o `dados.json` consolidado (evolução, tendências, comparação com rodadas passadas). Todas só quando precisar de tendência longa.
4b. Leia os flags de pré-flight de `workspace/[produto]/06-copy-engine/dados.json` (se existir): `voc_forced_continue` e `claims_unverified`. Se `voc_forced_continue: true`, a copy foi escrita com VOC insuficiente (o membro escolheu prosseguir mesmo assim) — guarde esse contexto pro diagnóstico de underperformance (ETAPA 4 / 6B), onde ele muda a hipótese causal.
5. **Unidade de análise:** a estrutura padrão da Skill 10 é **1 campanha → 1 ad set → N ads**. Toda leitura comparativa desta skill (share de spend, freq, CPM, CPA) acontece **entre ADS (criativos) dentro do ad set único**. Leitura por ad set/campanha só se aplica DEPOIS que a Skill 12 criou múltiplas campanhas/ad sets (pós-escala) ou se o membro montou estrutura custom por fora.
6. **Puxe os SISTEMAS NOMEADOS da base — NÃO use query genérica.** Rode `search_knowledge` com a `best_query` exata de cada framework relevante pra ETAPA que está executando (cada ETAPA abaixo já lista os seus). O índice completo do domínio desta skill (meta-ads-strategy, ~26 frameworks com suas queries) está em **`.claude/lib/kb-index/`** (`frameworks.json` + `README.md`, mapa skill→domínio no README). Os sistemas de maior impacto pra leitura de performance, com a query a rodar:
   - **4Pi Analysis (Spend, Frequency, CPM, Cost per Result)** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) — o motor da ETAPA 2
   - **4Pi+2 Dashboard & Custom Metrics** (rode `4Pi+2 custom metrics dashboard GPT account centers Ads Manager`) — setup das colunas customizadas
   - **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`) — as signatures de freq TOF/MOF/BOF do Pi 2
   - **Why New Ads Steal From Old Ads / Creative Hamster Wheel** (rode `why new ads steal from old ads creative hamster wheel deprioritized`) — fadiga e canibalização
   - **Profitable Scaling Margin (PSM) — Golden Ratio of Growth** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — o `psm_real` gravado pra skill 12
   - **Performance Gate Scaling (PGS)** (rode `Performance Gate Scaling PGS automated rules total loss investment soft surfing`) — checagem de scale automático
   - **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`) — por que ads ruins geram gasto
   - **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) — leitura do Pi 1
   - **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`) — interpretação do `dataset_health.match_quality_score`

   Cada framework que existir na base, aplique. A leitura por 4Pi/PSM é o RACIOCÍNIO; a DECISÃO de matar criativo segue o PLAYBOOK no topo desta skill (1-2× breakeven CPA sem venda → kill; CPM = saúde da conta; benchmarks de funil separam criativo de página).

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md`, mapa skill→domínio no README). NUNCA use query genérica — sempre puxe o sistema nomeado pela `best_query`.

## Fluxo da Skill

### ETAPA 0.5 — TrendTrack MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use como camada de comparação contextual:

- **`mcp__trendtrack__scan_ad`** nos winners do membro (após identificar via 4Pi) → decomposição com lente de mercado: hook archetype, ângulo, reach estimado, scaling assessment. Compara com benchmarks da vertical pra confirmar se o winner é mediocre ou top-tier do mercado.
- **`mcp__trendtrack__daily_radar`** se concorrentes já foram trackados na skill 03 → reporta movimentos recentes (novos ads dos competitors, mudanças de posicionamento). Adiciona contexto pro `NEXT_BATCH_IDEAS.md` final.

Use 1-3 chamadas por análise. Não desperdiçar créditos em criativo perdedor.

Se TrendTrack NÃO estiver disponível, siga ETAPA 1 normalmente.

### ETAPA 0.6 — Foreplay MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__foreplay__` disponíveis (ad spy — 200M+ ads; mesmo padrão de detecção das skills 03/08). Se SIM, use como camada de benchmark dos winners: depois de identificar os winners do batch (4Pi + Decision Thresholds), compare hooks e formatos deles com os ads ESCALADOS do nicho (busca por marca/vertical) — análogo ao `scan_ad` do TrendTrack acima. O sinal alimenta duas coisas: (a) confirmar se o winner é top-tier do mercado ou apenas o melhor de um batch fraco, (b) apontar formatos/hooks ativos no nicho que o batch ainda não explorou (vai pro `NEXT_BATCH_IDEAS.md`). Limite: 1-2 chamadas por análise — benchmark de winner, nunca em criativo perdedor.

Se Foreplay NÃO estiver disponível (ou uma chamada falhar), fallback silencioso: siga com TrendTrack (se houver) ou só com os dados do próprio batch — nada trava, nada é mencionado ao membro. Setup opcional em `.claude/automations/setup-mcps.md` (3.8).

### ETAPA 1 — Obter Dados (cascade: oficial → Pipeboard → manual)

Aura tenta 3 caminhos em ordem. Cada falha cai pro próximo silenciosamente — o membro vê apenas a versão final com label indicando qual modo entregou os dados.

#### Caminho 1 — Meta MCP **oficial** (preferencial; em open beta desde 2026-04-29, rollout gradual sem GA — contas podem aparecer "disabled", e o cascade cobre exatamente isso)

1. Verificar se tools com prefixo `mcp__meta__ads_` estão na sessão (prefixo canônico do connector oficial — ver `.claude/lib/mcp-detect/README.md`):
   ```
   official_mcp_available = existe ≥ 1 tool com prefixo mcp__meta__ads_
   ```

2. Se sim, tentar listar contas:
   ```
   accounts = mcp__meta__ads_get_ad_accounts()
   ```
   - Sucesso E ad_account do membro NÃO marcado "disabled" → invocar a receita única `sync-campaign-from-meta.md` (o cascade interno dela resolve pelo caminho oficial)
   - Conta marcada "disabled" no rollout gradual da beta → logar `account_disabled_in_official_beta` em `mcp-errors.log` e cair pro Caminho 2
   - OAuth expirado → tentar uma única re-autorização inline; se membro recusa, cair pro Caminho 2

3. Pelo caminho oficial, a receita salva pull completo em `workspace/[produto]/11-ad-analysis/raw-pull-[timestamp].json` com `source: "meta_mcp_official"` + blocos extras (`dataset_health`, `market_context` com industry benchmarks, auction ranking, opportunity score, anomalies). **ZERO interação com o membro.** Vá pra ETAPA 2.

#### Caminho 2 — Meta MCP via Pipeboard (3rd party, fallback)

Acionado quando o Caminho 1 falha. Verificar se MCP legado `meta-ads` (binary local do Pipeboard) está disponível:

```
pipeboard_mcp_available = tools com prefixo mcp__meta-ads__ existem
```

Se sim, invocar a MESMA receita única `sync-campaign-from-meta.md`, passando `force_path: "pipeboard"` no input + `fallback_reason` preenchido conforme o motivo do Caminho 1 ter falhado (motivos canônicos: `account_disabled_in_official_beta` | `oauth_failed` | `official_unreachable` | `forced_by_member`). JSON resultado tem `source: "meta_mcp_pipeboard"` e o mesmo shape base (sem os blocos `dataset_health` e `market_context` exclusivos do oficial).

#### Caminho 3 — Manual (último recurso)

Quando ambos MCPs falham (não configurados, ambos token/OAuth expirados, ambos rate-limited):

1. Logar ambos os erros em `workspace/[produto]/11-ad-analysis/mcp-errors.log`
2. Pedir ao membro:

   > "MCP do Meta Ads não respondeu (motivo: oficial=[erro], pipeboard=[erro]). Cola os dados aqui — screenshot ou números. Preciso ver **por AD (criativo)**: Spend, Frequency, CPM, CPC, Cost per Purchase, ROAS, e (importante pro diagnóstico de funil) Adds to Cart e Checkouts Initiated além das Purchases. E quantos dias cada ad está rodando."

3. ESPERE a resposta. Parse manual. Marcar `source: "manual"` internamente (valor canônico — ver `.claude/lib/mcp-detect/README.md`).

#### Output final — declarar o modo usado

No final da análise, header do relatório indica qual modo foi usado:

- **Caminho 1 (oficial):** "Dados puxados via Meta MCP oficial em [timestamp]. Industry benchmarks incluídos."
- **Caminho 2 (Pipeboard):** "Dados via Pipeboard MCP em [timestamp] (oficial indisponível: [motivo])."
- **Caminho 3 (manual):** "Dados colados pelo membro em [timestamp]."

Esta é a diferença entre Skill 11 totalmente autônoma (caminho 1 ou 2) vs sob demanda (caminho 3).

#### Quando dados oficiais existem, integrá-los na 4Pi analysis

Se `raw-pull.market_context.industry_benchmark` está presente:
- **Pi 3 CPM judgment:** comparar membro vs vertical em vez de absoluto. Ex: "membro CPM $42 vs vertical p50 $38 → 10% acima da mediana, dentro do esperado". Sem isso, CPM $42 sozinho não diz nada.
- **CPM subindo (fadiga vs sazonalidade):** se `anomalies_detected` confirma anomalia, decisão é mais confiante.
- **Auction ranking `below_avg` em quality OU engagement OU conversion** → marcador independente de problema do creative que entra no 19-Point Diagnostic.
- **Opportunity Score — usar como higiene, NUNCA como comando.** O score (0-100) mede aderência às best practices da Meta, não performance. Use os itens de checklist que ele expõe (audience overlap, sinal de conversão, variedade de criativo) como sinal secundário que "reforça vs contradiz" o 4Pi. **NUNCA aplique recomendações em lote pra "subir o score"** — em particular, IGNORE recomendação de ligar CBO/Advantage+ campaign budget durante a fase de teste 1-1-N: o budget no ad set é decisão deliberada da Skill 10 (variável de controle do teste). Score alto = alinhamento com o playbook da Meta, não ROAS.

Se `dataset_health.match_quality_score < 6.0` (EMQ na escala 0-10 do Events Manager — gate canônico da 07c é EMQ ≥ 6.0) → marcar warning no relatório: "Match quality abaixo do gate, CPAs podem estar inflados por undercounting de conversões". Antes esse contexto só vinha do Events Manager manualmente.

> Pra interpretar e corrigir match quality baixa: **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`). Diz quais parâmetros de advanced matching (email, click ID) elevam o EMQ e quando um EMQ baixo está inflando o CPA observado — não confunda CPA inflado por undercounting com criativo ruim antes de checar isso.

### ETAPA 2 — 4Pi Analysis (Ordem EXATA)

**Frameworks a puxar ANTES de ler os Pi's (rode a `best_query` de cada):**
- **4Pi Analysis (Spend, Frequency, CPM, Cost per Result)** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) — o sistema completo da ordem dos 4 Pi's e o que cada um contextualiza no próximo.
- **4Pi+2 Dashboard & Custom Metrics** (rode `4Pi+2 custom metrics dashboard GPT account centers Ads Manager`) — quais colunas customizadas montar no Ads Manager pra ler os Pi's corretamente (freq diária, CPM, cost per result por ad set).
- **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — fundamenta o `psm_real` calculado abaixo (PSM substitui ROAS como métrica-mãe de scaling).

#### Decision Thresholds (bloco canônico — referenciado por TODOS os steps abaixo)

Defina estes valores UMA vez no topo da análise. Todos os steps (Pi 4, ETAPA 3, ETAPA 9, ETAPA 11) usam ESTES, sem redefinir.

**Unit economics (de `04-offer-builder/dados.json`):**
- `breakeven_cpa = offer.unit_economics.weighted_margin_per_order` (denominador de margem canônico)
- `target_cpa_2x = offer.unit_economics.target_cpa_primary_2x`
- `target_cpa_3x = offer.unit_economics.target_cpa_primary_3x`
- **`target` = `target_cpa_2x` em TODAS as classificações desta skill** (quando o texto diz "target", é este). `target_cpa_3x` é só o alvo esticado de referência pra leitura de scaling agressivo na ETAPA 9 — não entra em nenhuma decisão de kill.
- COGS canônico = somatório de `offer.cogs_breakdown` (NÃO existe campo `cogs_total`)
- **Fallback** se campos não existirem (oferta antiga): `breakeven_cpa = AOV / breakeven_roas` (mesmo fallback da Skill 10); se nem esses campos existirem, usar default conservador e marcar `data_gap`.
- **`fair_share` = spend total do ad set ÷ N ads ativos** (a fatia que cada criativo receberia numa distribuição uniforme). É a régua de sub-entrega — nunca use "% do spend total" fixo: com 10-12 criativos, 10% do total É o fair share, e um critério fixo condenaria até o ad perfeitamente distribuído.

> **Incremental Attribution (setting do Ads Manager, 2025+):** se o membro ligou esse setting em alguma campanha, o CPA reportado dela NÃO é comparável ao CPA clássico — o Meta passa a contar só conversões que julga ter causado (conversões reportadas caem, CPA observado sobe, e o setting trava as attribution settings). Nesse caso, re-baseline TODOS os thresholds desta análise antes de qualquer kill naquela campanha, e trate a leitura como ferramenta de alocação de budget, não de kill de criativo. No teste padrão da Skill 10, o baseline é 7d-click/1d-view — a régua de kill foi calibrada nele.

**PSM real (fórmula canônica — unificada com skill 12):**
```
psm_real = LTV / (CPA + COGS)
```
- `CPA` = `observed_cpa_avg_last_7d` (CPA médio real dos últimos 7 dias)
- `COGS` = somatório de `offer.cogs_breakdown`
- `LTV` = de `04-offer-builder/dados.json` (ou AOV se LTV ausente)
- Thresholds PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.
- **A skill 11 é a ÚNICA fonte que grava `manifest.psm_real`** (a partir de performance real). Também grava em `11-ad-analysis/dados.json`. Skill 12 LÊ `manifest.psm_real`; nunca recalcula.

**Gatilho de KILL operacional (PLAYBOOK — a decisão de matar criativo):**
- **KILL imediato:** criativo gastou **1-2× breakeven CPA SEM venda** → pausa. CPA manda, CTR não salva.
- **Exceção (segura):** criativo com **2+ initiate-checkouts** no comecinho → deixa rodar mais (Meta tem sinal pra otimizar), mesmo já no range de kill.
- **Funil quebrado antes de matar:** se houve checkouts mas as taxas de funil estão abaixo de ATC→compra 20-25% / checkout→compra 40-50% (com a amostra mínima da ETAPA 6B), o bloqueio é página/oferta, não o criativo → NÃO matar o criativo; rotear pra 06/07/04.
- **Conta antes de produto:** CPM muito acima do nicho → suspeitar da CONTA primeiro; testar o mesmo criativo em outra conta antes de matar o produto.

**Winner / Loser (definição única — vale pra ETAPA 3, 9, 11 e handoff pra skill 14):**
- **WINNER:** ad recebeu spend real (≥ 50% do `fair_share`), CPA ≤ target, e a campanha overall não piorou.
- **LOSER** (qualquer uma destas):
  1. Disparou o gatilho de KILL (gastou 1-2× breakeven CPA sem venda — na régua de target: spend ≥ 1.5× target CPA sem conversão; vale o que atingir primeiro), fora da exceção de checkouts;
  2. **Sub-entrega:** spend do ad **< 50% do `fair_share` após 72h**, COM a entrega geral do ad set saudável (se NADA gastou, o problema é review/policy/conta — não é loser individual);
  3. **CPA > 2× target sustentado após 7 dias** (abaixo do KPI mesmo depois da janela de iteração).
- **NEEDS OPTIMIZATION:** CPA entre target e 2× target após 7 dias — iterar, não pausar ainda.
- **EM APRENDIZADO:** ainda não atingiu 1× breakeven CPA de spend OU < 7 dias rodando — aguardar antes de decidir.

Aplique os 4 Pi's **NA ORDEM** (Spend → Frequency → CPM → Cost per Result). A ordem importa — cada Pi contextualiza o próximo.

#### Dados insuficientes — como proceder

- **Ad set rodou < 24h**: análise 4Pi é **inválida**; apenas diagnóstico qualitativo. Marque "PRELIMINAR" no output.
- **Volume de conversões baixo** (poucas purchases, CPA instável dia-a-dia): CPA é ruído; use Spend + Freq + CPM apenas. CPA column = "insufficient data". O gate clássico da learning phase **continua valendo em 2026**: ~50 eventos de conversão em 7 dias por ad set pra sair de learning — abaixo disso, o CPA balança e a leitura é preliminar. O que mudou (desde abril/2026) é outra coisa: edições antes consideradas "seguras" (ajuste pequeno de bid, tweak de criativo) passaram a **resetar o learning com mais facilidade** — mais um motivo pro "não mexe por 3 dias" da Skill 10.
- **Dados faltando Frequency ou CPM** (API error): tentar refetch; se persistir, documentar como `data_gap` e pular aquele Pi.

#### CPM subindo: fadiga OU sazonalidade?

Antes de declarar "fadiga" (que justifica creative refresh), checar:
- Calendário: Q2-Q4 geralmente vê CPM subindo (holiday prep, Black Friday, Xmas)
- Benchmark setor: olhe CPM médio do seu vertical na semana atual (Meta insights ou reports de terceiros)
- Delta relativo: se seu CPM subiu 15% mas vertical subiu 20%, você está na média — NÃO é fadiga
- Só declare fadiga se CPM subiu > 20% VS vertical e freq diária > 1.5

#### Winner picking — ROAS ou CPA?

Para decisões de "qual ad (criativo) é melhor":
- Use ROAS quando AOV varia entre ads (ex: um criativo puxa mais bundle/upsell)
- Use CPA quando AOV é ~estável
- **Desempate por lucro (quando os dados existem):** lucro por compra = `AOV − COGS − CPA` (comparável entre ads quando o AOV varia); ou lucro por clique = `(AOV × CVR) − CPC` (quando quer comparar eficiência de tráfego). Nunca misture as duas réguas na mesma comparação.

#### Pi 1: SPEND

> Fundamento: **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) + **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`). Explicam por que o algoritmo concentra ou força spend e por que NÃO se desliga o top spender mesmo quando parece ineficiente.

"Quanto cada AD (criativo) recebeu do budget do ad set único?"

Observação-chave: **Meta distribui spend pra onde ele ACREDITA que está funcionando**. Com N criativos no mesmo ad set, o `fair_share` de cada um é 1/N do spend. Se o ad A recebeu 3× o fair share e o ad B só 20% dele, o algoritmo tá "votando" que A é melhor (independente de CPA).

- **Ad com spend ≥ 2× o fair share** → Meta tá confiante nele (candidato a winner — confirmar no Pi 4)
- **Ad com spend < 50% do fair share após 72h** (com a entrega geral saudável) → Meta não tá confiante nele OU o ad não foi aprovado → entra no critério de sub-entrega do LOSER

Se NENHUM ad gastou em 24-48h (entrega geral travada): verificar Ads Manager > Delivery insights + Review status — pode ser policy/review/conta, NÃO criativo. Pós-escala (Skill 12 criou múltiplas campanhas/ad sets), a mesma leitura de share se aplica um nível acima: campanha/ad set com spend muito abaixo do esperado = algoritmo sem confiança nela.

#### Pi 2: FREQUENCY (Sinaliza Posição no Funil)

> Fundamento das signatures: **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`). É de lá que vêm as bandas de freq diária ↔ posição no funil (TOF/MOF/BOF) e a leitura de sprinters vs marathoners.

**Regra base: a frequency lida aqui deve ser a frequency DIÁRIA** (freq do dia, não acumulada da vida toda do ad set). Frequency lifetime cresce indefinidamente e não diz nada sobre fadiga atual. Sempre puxe/compare a freq diária. As bandas abaixo são para freq DIÁRIA.

Aplicar as signatures (freq diária, lida POR AD):

- **Freq ~1.05** → **prospecting / TOF** (Top of Funnel) — novas impressões, cold traffic, ~1 impressão por pessoa/dia
- **Freq 1.1-1.4** → **MOF** (Middle) — starting to warm up
- **Freq 1.5-1.9** → **retargeting / BOF** (Bottom) — mesmas pessoas vendo várias vezes ao dia

Se os ads da campanha de teste (que é 100% prospecting broad) estão com freq diária bem acima de ~1.05 (puxando pra 1.5-1.9, comportamento de retargeting), o Meta está re-martelando a mesma audiência em vez de abrir TOF novo — sinal de saturação da entrega. Recomendação: adicionar conceito TOF-friendly (hook problem, angle curiosity) no próximo batch.

**Freq ~1.05 estável NÃO é anomalia aqui:** na estrutura 1-1-N broad, ~1.05 sustentada é o estado normal e desejado de uma campanha 100% prospecting — não dispare alerta por isso. O alerta de "Meta não consegue re-engajar" só se aplica quando existe camada de retargeting esperada (que o fluxo padrão não monta). O check que continua valendo em qualquer cenário: **CPM baixo + CTR muito baixo = criativo não ressoa** com a audiência.

#### Pi 3: CPM (Contexto Combinado com Freq)

**CPM isolado diz pouco. CPM + Freq diz muito:**

- **CPM alto (acima da média do nicho) + Freq diária alta (>1.5)** → Meta tá mandando pra audience cara (prime-time, premium placements) porque POUCA audience nova está disponível. Sinal de BOF / possível fadiga.
- **CPM alto + Freq diária baixa (~1.05)** → audience premium/cara mas fresca. Pode ser normal em nicho competitivo (skincare, finance, luxury).
- **CPM baixo + Freq alta** → Meta tá procurando impressões baratas com audience repetida. Frequência tá alta mas CPM não subiu = Meta não tá pagando caro pra forçar. Pode ser fadiga mas também pode ser só stabilidade.
- **CPM subindo no tempo** (comparar com análises anteriores se houver) → **possível fadiga**. Combinar com CTR falling pra confirmar.

**CPM também é sinal de saúde da CONTA (lente do playbook):** o mesmo produto/criativo pode dar CPM $30 numa conta e $100 noutra — o CPM diz tanto sobre a conta quanto sobre o criativo. Se o CPM está muito acima do esperado do nicho de forma generalizada (TODOS os ads caros, não só um criativo), suspeite da CONTA antes do produto. Antes de declarar o produto morto por economia ruim, marque `health_signals.account_cpm_suspect = true` e recomende **testar o mesmo criativo em outra conta de anúncio** (resiliência legítima: ter conta reserva ajuda aqui). Só mata o PRODUTO se ele não validar em conta nenhuma.

#### Pi 4: COST PER RESULT (O Que Realmente Importa)

Compare CPA de cada AD (criativo) contra o **target CPA da oferta** (do `04-offer-builder/offer-builder.md`), usando as classificações do bloco **Decision Thresholds** definido no topo desta ETAPA:

- **CPA ≤ target** → WINNER (vai pro diagnóstico "scale")
- **CPA entre target e 2× target após 7 dias** → NEEDS OPTIMIZATION (iteração, não pausar ainda)
- **CPA > 2× target sustentado após 7 dias OU spend < 50% do fair share após 72h (entrega geral saudável)** → LOSER (pausar)

**Gatilho de KILL do playbook (decisão operacional por criativo, antes do horizonte de 7 dias):** pra cada criativo, compare o spend acumulado com o breakeven CPA:
- **Gastou 1-2× breakeven CPA SEM venda → KILL** (pausa o criativo). CPA é o que manda — **CTR alto sem venda não salva**. Marque `outcome = "loser"` com `reason = "kill_no_sale_at_breakeven"`.
- **Exceção:** se o criativo tem **2+ initiate-checkouts** no comecinho, NÃO mate ainda — o Meta tem sinal pra otimizar; deixa rodar mais um pouco. Classifique como NEEDS OPTIMIZATION.
- **Funil quebrado (cruzar com benchmarks ANTES de matar):** se o criativo gerou ATC/checkouts mas as taxas estão abaixo de **ATC→compra 20-25%** ou **checkout→compra 40-50%**, o bloqueio é página/checkout/oferta, NÃO o criativo. Ex: 3 checkouts e 0 venda → checkout→compra = 0%, muito abaixo dos 40-50% esperados → o ad fez o trabalho, a página falhou. **NÃO mate o criativo**; roteie pra 06/07 (página) ou 04 (oferta) e registre o gargalo de funil no diagnóstico.
- **Conta antes do produto:** se o CPM está fora do esperado do nicho de forma generalizada (ver Pi 3, `account_cpm_suspect`), trate como problema de CONTA — recomende re-testar em outra conta antes de matar o produto.

Contexto importante: **CPA de um ad isolado não é tudo**. "a campanha overall melhorou?". Se a campanha total está dentro do CPA target mesmo com 1-2 ads fora, a máquina tá OK. Otimiza os outliers, não destrua a campanha.

**Breakdown por placement (check rápido quando o CPA agregado está fora do target):** puxe insights com breakdown por placement (o MCP oficial expõe; no Ads Manager: Breakdown > Placement). Placement de CPM baixo mas conversão fraca — Threads (placement global desde jan/2026, ligado por default no Advantage+) e Audience Network são os suspeitos usuais — pode estar comendo spend sem vender. Só considere opt-out via manual placements como **exceção documentada depois desse dado**; nunca preventivamente (a tese de deixar o Meta distribuir continua certa).

#### PSM real (gravado nesta análise — usado pela skill 12)

Calcule `psm_real` pela fórmula canônica do bloco **Decision Thresholds**:
```
psm_real = LTV / (CPA + COGS)
```
- `CPA` = `observed_cpa_avg_last_7d`
- `COGS` = somatório de `offer.cogs_breakdown` (NÃO existe campo `cogs_total`)
- `LTV` = de `04-offer-builder/dados.json` (ou AOV se LTV ausente)

Este `psm_real` é gravado em `11-ad-analysis/dados.json` E em `manifest.psm_real` (ver ETAPA de update do manifest). Skill 12 lê de `manifest.psm_real`, nunca recalcula. Thresholds de ação PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.

### ETAPA 3 — Diagnóstico Por Ad (criativo)

Pra CADA ad do ad set único, classifique:

**WINNER:** recebeu spend real (≥ 50% do fair share), CPA ≤ target, campanha overall melhorou.
→ Ação: manter rodando; se a Automated Rule de PGS existe E está ativa (`pgs_enabled` da 10), ela escala dentro da margem — senão, a escala é decisão da ETAPA 9. Se quer escalar mais agressivo, considera promover criativo a Champion (Post ID) e adicionar ad set dedicado.

**IN FATIGUE:** CPM subindo + CTR caindo + Freq subindo ao longo dos dias (comparar com análises anteriores).
> Antes de classificar fadiga, puxe **Why New Ads Steal From Old Ads / Creative Hamster Wheel** (rode `why new ads steal from old ads creative hamster wheel deprioritized`) — explica quando o sinal de "fadiga" é na verdade um ad novo canibalizando o spend do antigo (deprioritization), e não fadiga real da audience. Muda a ação: nesse caso o fix é consolidar, não refresh.
> **Calibração 2026 (pós-Andromeda/GEM):** a vida útil típica de criativo encolheu pra **2-4 semanas** (estático fatiga mais rápido; o pico de performance costuma ser a 1ª semana). Planeje refresh nessa janela — não em ciclos de 6-8 semanas.
→ Ação: trocar os 1-2 criativos mais fatigados do ad set por conceitos novos (Skill 08) OU pedir batch novo completo. **Não pausar ainda** — pode ainda estar performando acima do breakeven mesmo com sinais de fadiga.

**LOSER** (def. canônica do bloco Decision Thresholds): disparou o **gatilho de KILL** (gastou 1-2× breakeven CPA SEM venda, fora da exceção de 2+ checkouts) OU **sub-entrega** (spend < 50% do fair share após 72h com entrega geral saudável) OU **CPA > 2× target sustentado após 7 dias**. Qualquer dessas = loser.
→ Ação: PAUSAR. Se produto já validado (outro criativo vende), mata rápido. Fazer diagnóstico profundo (Etapa 4) pra entender por que falhou.

**FUNIL QUEBRADO (não é o criativo):** o criativo trouxe ATC/checkouts mas as taxas estão abaixo dos benchmarks (ATC→compra < 20-25% ou checkout→compra < 40-50%).
→ Ação: **NÃO pausar o criativo** — o ad fez o trabalho, o gargalo é página/checkout/oferta. Rotear pra 06/07 (página) ou 04 (oferta). Registrar o gargalo de funil no `health_signals` e no NEXT_BATCH_IDEAS.

**CONTA SUSPEITA (não é o produto):** CPM generalizado muito acima do nicho (`account_cpm_suspect`).
→ Ação: re-testar o mesmo criativo/produto em OUTRA conta de anúncio antes de matar o produto. Só mata o produto se não validar em conta nenhuma.

**EM APRENDIZADO:** ainda não atingiu 1× breakeven CPA de spend OU < 7 dias rodando, spend baixo.
→ Ação: aguardar antes de decidir. Dê ao Meta tempo de estabilizar a entrega e o CPA antes de julgar — a learning phase clássica (~50 eventos de conversão/7 dias por ad set) continua valendo em 2026, e abaixo desse volume o CPA balança. Não mexer no ad set enquanto isso (edições resetam o learning com mais facilidade desde abril/2026).

**KILL de PRODUTO (cadência quarta→domingo — a decisão vive AQUI, não na 10):** o teste de produto lança quarta e tem teto de 7 dias (cadência montada pela Skill 10). Se até domingo NENHUM criativo vendeu, o default é **matar o produto** e rodar o próximo. Ordem de precedência OBRIGATÓRIA antes de decretar:
1. **Funil quebrado?** (ETAPA 6B) — se os ads trouxeram checkouts que a página desperdiçou, o problema é página/oferta; conserta antes de matar o produto.
2. **Conta suspeita?** (Pi 3, `account_cpm_suspect`) — CPM generalizado fora do nicho pede re-teste em OUTRA conta antes de matar o produto.
3. **Entrega travada?** — ads presos em review/policy não testaram nada; resolver e re-rodar a janela.
Se os 3 checks passam e não houve venda até domingo → mata o produto, documenta o learning e segue pro próximo.

### ETAPA 4 — Diagnóstico Profundo de LOSERS (19-Point Diagnostic)

### 19-Point Loser Diagnostic

**Camada 1: Targeting (4 pontos) — só se aplica a estruturas CUSTOM.** A estrutura padrão da 10 é broad/Advantage+ sem exclusões e sem lookalike — nela, pule direto pra Camada 2. Use esta camada só se o membro montou targeting manual por fora do fluxo.
1. Audience muito broad — CTR alto, CVR baixo
2. Audience muito narrow — CPM alto, volume baixo
3. Exclusões conflitantes (ex: excluir compradores mas campaign é de aquisição — conflito)
4. Lookalike source com baixa qualidade (seed < 500 de alta qualidade)

**Camada 2: Hook (4 pontos)**
5. Hook não promete ganho específico
6. Hook sem pattern interrupt visual (3 primeiros segundos)
7. Hook não casa com awareness stage dominante
8. Hook saturado (claim idêntico a 5+ concorrentes)

**Camada 3: Copy (4 pontos)**
9. Primary text > 125 chars (corta em mobile)
10. CTA vago ("saiba mais" vs "ativar desconto 30%")
11. Zero social proof específico
12. Benefício listado sem transformação (feature, não benefit)

**Camada 4: Offer (4 pontos)**
13. Preço quebra o budget do awareness stage
14. Garantia fraca ou ausente
15. Urgência artificial óbvia
16. Bundle não faz sentido para o público

**Camada 5: Técnico (3 pontos)**
17. EMQ < 6/10 (Event Match Quality do Events Manager — gate canônico da 07c é ≥ 6.0)
18. Landing page carrega > 3s (mobile)
19. Mismatch ad → landing (visual/copy)

Pra cada loser, identifique **a camada onde falhou** e a hipótese específica. Documente.

### ETAPA 5 — Diagnóstico de WINNERS (Extração de Learnings)

Pra cada WINNER, extraia learnings aplicando o framework:

- **O que funcionou?** (hook específico, ângulo, formato, CTA, LP)
- **Por que funcionou?** (hipótese causal — ex: "hook de curiosity pattern interrupt em audience Problem Aware onde concorrentes usam authority-first")
- **Como replicar?** (quais elementos isolar pra usar em próximos batches — ex: "o hook 'POV: você acorda com X' pode ser template pra outros conceitos")

Learnings vão alimentar Skill 08 (creatives) no próximo batch — escreva de forma utilizável.

### ETAPA 6 — Saúde do Funil (posição + conversão)

**6A — Posição de funil** (dos Pi 2 — frequency signatures):
> Pra recomendar qual posição reforçar, puxe **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`) — diz quais formatos/ângulos servem cada posição faltante (ex: TOF → hook problem/curiosity; BOF → offer/comparison). Isso alimenta o NEXT_BATCH_IDEAS com a posição + o tipo de conceito certo.
- Todos os ads em TOF? → normal na campanha de teste 1-1-N (100% prospecting por construção); só vira "funil raso" quando já existe volume de warm audience acumulado sem nada convertendo ela
- Todos em BOF? → falta trazer volume novo, tá escalando sobre a mesma audience
- Distribuído em TOF + MOF + BOF? → saudável (esperado só pós-escala, quando a 12 já criou camadas)

Recomendação baseada em desbalanço:
- Falta TOF → próximo batch inclui conceitos de awareness building (hook problem, curiosity, authority)
- Falta BOF → próximo batch inclui retargeting-style (offer-focused, urgency, comparison)

**6B — Conversão de funil (diagnóstico de funil quebrado — separa criativo de página/oferta):**

Calcule, com os dados do pull (ATC, initiate-checkout, purchases) por ad E agregado da campanha:
- **Add-to-cart → compra = `purchases / add_to_cart`.** Benchmark: **20-25%** (a cada 10 ATC, ~2 compras).
- **Checkout → compra = `purchases / initiate_checkout`.** Benchmark: **40-50%** (média ~40%).

**Amostra mínima antes de decretar funil quebrado:** ≥ **10 initiate-checkouts** OU ≥ **20 ATC** agregados na campanha. Abaixo disso, taxa de funil é ruído — com checkout→compra saudável de 40%, "3 checkouts e 0 venda" acontece por puro acaso em ~1 de cada 5 criativos bons (0,6³ = 21,6%). Sem a amostra, marque a leitura como **PRELIMINAR**, NÃO sete `funnel_broken` e NÃO roteie o membro pra retrabalhar página/oferta ainda.

Leitura (com amostra suficiente):
- **Dentro ou acima do benchmark** → o funil converte; se um criativo não vende, o problema é o criativo (entra na regra de KILL).
- **Abaixo do benchmark** → o bloqueio é PÁGINA / CHECKOUT / OFERTA, não o criativo. Ex: campanha com muitos checkouts e poucas vendas → checkout→compra abaixo de 40% → a página/checkout está vazando. **Não mate criativos por isso** — eles trouxeram intenção de compra que a página desperdiçou.
- Se os dados de ATC/checkout não vierem no pull (manual ou API limitada), marque `data_gap` e diga ao membro exatamente o que olhar no Shopify/Meta pra preencher (funnel do checkout: sessions → ATC → checkout → purchase).

Roteamento quando funil quebrado: checkout→compra baixo → `'page'`/`'copy'` (página vazando) ou checkout flow; ATC→compra baixo com checkout→compra ok → oferta/preço fraco no checkout → `'offer'`. Registre o gargalo em `health_signals` e no NEXT_BATCH_IDEAS pra não repetir o erro de matar criativo bom.

**Check de VOC insuficiente ANTES de culpar criativo/oferta:** se `06-copy-engine/dados.json.voc_forced_continue: true` (carregado no Contexto, item 4b) E CTR/CVR estão abaixo do esperado (CTR baixo generalizado entre os ads, ou CVR da página abaixo do benchmark), a hipótese primária muda: **a copy rodou com VOC insuficiente** — os hooks e a página falam a língua errada porque a matéria-prima de pesquisa era rasa. Diagnóstico: "copy rodou com VOC insuficiente — re-rodar skill 02 (market research) com mais fontes e re-gerar a copy antes de culpar criativo ou oferta". Registre em `health_signals` como `voc_insufficient_copy` e roteie pra 02 → 06, não pra 08. (Mesma lógica se `claims_unverified: true` e a página tem CVR baixo com tráfego bom: claims sem lastro derrubam confiança — rotear pra 04 Etapa 2.5.)

### ETAPA 7 — 12 Perguntas de Feedback (checklist desta skill)

Aplique as 12 perguntas aos dados (checklist próprio desta skill — no cenário padrão 1-1-N, a unidade é o AD dentro do ad set único):

1. Qual ad (criativo) teve maior ROAS e por quê?
2. Qual teve menor ROAS e por quê?
3. Qual elemento específico dentro dos winners tá puxando mais (hook, formato, ângulo)?
4. Houve variação significativa de performance por primary text?
5. Alguma headline se destacou?
6. Algum placement (Threads, Audience Network) está comendo spend com CPM baixo sem converter? (breakdown do Pi 4)
7. Frequency subiu mais rápido que esperado em algum ad? (sinal de saturação da entrega)
8. CPM variou muito entre ads? (aponta pra diferenças de resposta da audiência por criativo)
9. CTR variou muito? (indicador de hook strength)
10. Conversão CTR→Purchase variou? (indicador de message match)
11. Retention no site (se tiver) — quanto tempo ficam?
12. Qual a hipótese causal principal pro resultado?

Compile respostas num bloco objetivo.

### ETAPA 8 — Recomendações Acionáveis (Imediato / Curto Prazo / Médio Prazo)

**AÇÕES IMEDIATAS (hoje/24h):**
- Pausar losers identificados na Etapa 3 (especificar quais ADS, por nome/`concept_id`)
- Consertar problemas técnicos identificados no 19-point (se houver)
- **PGS — só se a Automated Rule existe:** se `pgs_enabled == true` no `10-ad-strategy/dados.json` (ou a receita full-deploy criou a rule), verificar se ela está ATIVA e disparou nos últimos dias (Ads Manager > Automated Rules > history). Se NENHUMA rule existe, PGS não está rodando — não há escala automática pra "verificar"; configurar é decisão da ETAPA 9.

**CURTO PRAZO (3-7 dias):**
- Se tem fadiga: trocar os 1-2 criativos mais fatigados do ad set por conceitos novos da 08
- Se falta diversidade de funil: gerar novo batch de conceitos (Skill 08) com foco na posição faltante
- Se o breakdown por placement (Pi 4) mostrou placement comendo spend sem converter: documentar e decidir a exceção de opt-out

**MÉDIO PRAZO (2-4 semanas):**
- Se winners estáveis: promover pra Champion (Post ID separado)
- Se CPA está melhor que target consistentemente: reavaliar se dá pra escalar mais (vertical + horizontal — delegar pra Skill 12)
- Se oferta parece ser o bloqueio: voltar pra Skill 04 e ajustar (bundle structure, guarantee, stack)
- Se página parece ser o bloqueio: voltar pra Skill 06/07 e iterar

### ETAPA 9 — Decisão de Scaling (Recomendação Clara)

> Fundamente a recomendação puxando os sistemas de scaling (rode as `best_query`): **Profitable Scaling Margin (PSM)** (`Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — usa o `psm_real` calculado na ETAPA 2 pra decidir agressivo/steady/breakeven/cortar; e **Performance Gate Scaling (PGS)** (`Performance Gate Scaling PGS automated rules total loss investment soft surfing`) — confirma se as automated rules estão ativas antes de prometer "escala automática". A montagem detalhada do plano de escala (vertical + horizontal) é delegada pra skill 12; aqui só a recomendação.

**Configuração REAL do PGS (quando o membro quiser a escala automática):** PGS só existe se a Automated Rule foi de fato criada — nenhuma promessa sem isso. Dois caminhos:
1. **Via MCP oficial** (se `mcp__meta__ads_*` na sessão): criar a rule com condições CPA trailing (Purchase) < `pgs_cpa_threshold`, spend > `pgs_spend_threshold`, frequency ≤ `pgs_freq_max` (do `10-ad-strategy/dados.json`), ação +5% de budget, schedule 3×/semana. **A rule nasce DESATIVADA** — o membro revisa e ativa no Ads Manager.
2. **Manual** (sem MCP): passo-a-passo pro membro em Ads Manager > Automated Rules > Create rule, com os mesmos valores preenchidos. Instruir a salvar a rule desligada e ativar só depois de revisar.
Depois de criada e ativada, atualizar `pgs_enabled: true` no `10-ad-strategy/dados.json`.

Baseado no diagnóstico completo, dê uma recomendação clara:

**SE CPA dentro do target E winning ads estáveis:**
- Com PGS ativo (`pgs_enabled == true`): "Continue rodando. O PGS escala automaticamente dentro da margem. Se quer escalar mais agressivo OU adicionar canais novos, diga **'scale'** pra eu montar o plano."
- Sem PGS configurado: "Continue rodando. Se quiser escala automática conservadora, configuro o PGS agora (Automated Rule que sobe +5% de budget só quando o CPA trailing segura — nasce desativada pra você revisar). Pra escala de verdade, diga **'scale'**."

**SE CPA ≤ 0.7× target E winning ad claro:**
"Oferta forte, ads matando. Diga **'scale'** pra montar plano de escala vertical + horizontal. Pode considerar scaling aggressive em paralelo ao PGS (se configurado)."

**SE CPA acima do target mas ainda abaixo de 2×:**
"Não escala. Foco em iteração. Diga **'creatives'** pra gerar novo batch baseado nos learnings desta análise."

**SE CPA > 2× target após 7+ dias:**
"Bloqueio não é só ad — pode ser oferta, página, ou audience. Vou sugerir investigação: [indicar onde está o bloqueio mais provável baseado no 19-point]. Depois de ajuste, re-roda análise em mais 7 dias."

**SE funil quebrado (ETAPA 6B abaixo do benchmark):**
"Os criativos estão trazendo gente que adiciona ao carrinho e inicia checkout, mas a conversão final está abaixo do esperado ([checkout→compra X% vs 40-50% ideal]). O gargalo é a página/checkout, não o ad. Antes de mexer em criativo: diga **'page'** ou **'copy'** pra eu revisar a página (ou **'offer'** se for preço/oferta no checkout)."

**SE conta suspeita (`account_cpm_suspect`):**
"O CPM está bem acima do esperado do nicho de forma generalizada — isso costuma ser a CONTA, não o produto. Antes de matar o produto, vale re-testar o mesmo criativo em outra conta de anúncio. Se quiser, monto a estrutura de teste de novo (diga **'ad strategy'**)."

### ETAPA 10 — Learnings Documentados (Pra Feedback Loop)

Na seção final do relatório, documente learnings que vão alimentar próximos batches:

**Hipóteses validadas** (o que ficou confirmado pelos dados):
**Hipóteses rejeitadas** (o que não confirmou):
**Hipóteses ainda em teste** (precisa mais dados):
**Ideias pra próximo batch:**

Isso é o "feedback loop motor de crescimento" — cada análise enriquece o próximo batch de criativos.

### ETAPA 11 — DNA Update (silent — feedback automático pro registry)

Pra cada criativo analisado nesta rodada:

1. Classificar outcome (alinhado ao bloco Decision Thresholds — o `outcome` aqui é o mesmo gravado em `winners[]`/`losers[]` de `11-ad-analysis/dados.json`):
   - `winner`: CPA ≤ target E recebeu spend real (≥ 50% do fair share) E campanha overall não piorou; sinal forte se spend > $300 E decile_rank 1-2
   - `loser`: disparou o gatilho de KILL (gastou 1-2× breakeven CPA sem venda, fora da exceção de 2+ checkouts) OU sub-entrega (spend < 50% do fair share após 72h com entrega geral saudável) OU CPA > 2× target sustentado após 7 dias
   - `neutral`: demais (inclui criativo em FUNIL QUEBRADO — não foi o criativo que falhou, não conta como loser dele)

2. Compor performance JSON:
   ```json
   {
     "cpa": X, "ctr": Y, "roas": Z, "spend": W,
     "thumbstop_3s": A, "hold_15s": B,
     "impressions": N, "clicks": M, "purchases": P,
     "days_active": D, "decile_rank": R,
     "outcome": "winner|loser|neutral"
   }
   ```

3. Salvar em `workspace/[produto]/creative-dna/perf-[creative-id].json`

4. Invocar silenciosamente:
   ```
   python3 .claude/lib/creative-dna/registry.py update workspace/[produto] [creative-id] workspace/[produto]/creative-dna/perf-[creative-id].json
   ```

5. Se total de criativos com performance ≥ 10 E (total atual % 5 == 0):
   ```
   python3 .claude/lib/creative-dna/registry.py dna workspace/[produto] --product [slug]
   ```
   Atualiza `workspace/[produto]/creative-dna/dna-profile.json` que será usado na próxima Skill 08.

Silent. Membro não vê. Apenas o efeito: próximo briefing começa a refletir padrões aprendidos.

### PII redaction (antes de salvar qualquer dump de Ads Manager)

Antes de persistir dados em `workspace/`:
- Substituir Account IDs por `ACC-[hash 8 chars]`
- Substituir Pixel IDs por `PX-[hash 8 chars]`
- Remover emails em UTM/audience names (regex `[\w.+-]+@[\w.-]+\.\w+` → `[EMAIL_REDACTED]`)
- Remover telefones em audience names (regex `\+?\d{10,15}` → `[PHONE_REDACTED]`)
- Nota: manter hash dos IDs consistente entre execuções para correlacionar análises

### Output adicional — NEXT_BATCH_IDEAS.md (fecha loop 11→08)

Além de `[YYYYMMDD]-analysis.md`, gerar OBRIGATORIAMENTE:
`workspace/[produto]/11-ad-analysis/NEXT_BATCH_IDEAS.md`

**Critério de parada pra evitar loop infinito 11↔08:**

Antes de gerar ideias novas:
1. Se `NEXT_BATCH_IDEAS.md` já existe:
   - Ler versão anterior + ler `08-creative-engine/dados.json` (criativos gerados desde última rodada)
   - Comparar: quantas ideias propostas na versão anterior **foram testadas** (viraram criativos em 08-creative-engine/dados.json com performance registrada nas análises desta skill)?
   - Se `testadas < 50%` das ideias propostas na última rodada → **Não gerar novas ideias.** Retornar versão anterior intacta + adicionar seção "Validation pending: {ideia1}, {ideia2} ainda não foram testadas — priorize antes de gerar novos angles."
   - Se `testadas >= 50%` → proceder com novas ideias (baseadas em learnings das testadas)
2. Se arquivo não existe: gerar do zero normalmente.

Conteúdo (quando gerar):
- **Ângulos a testar no próximo batch de creatives** (2-3 bullets específicos)
- **Ângulos a EVITAR** (identificados como saturados ou já losers)
- **VOC phrases não usadas ainda** que aparecem em learning de review mining
- **Formatos a priorizar** (UGC vs studio vs static vs video — baseado em performance)
- **Awareness stage para focar** (se campanha atual oversserve um stage)
- **Ideias carry-over** (propostas antes, ainda não testadas)

**Skill 08 DEVE ler este arquivo no pre-flight.** Isto fecha o loop 11→08 **com critério de parada.**

### Panorama para skill 12 (scale) e skill 14 (content-recycler) — handoff

Se ações próximas = 'scale', skill 12 lerá este JSON SEM precisar perguntar.
Se membro invoca `recycle winner`, skill 14 lerá esse JSON pra achar winner ID.

O arquivo de análise é `workspace/[produto]/11-ad-analysis/dados.json` (cópia do último análise — nome literal `dados.json` dentro da pasta `11-ad-analysis/`):

```json
{
  "analysis_id": "uuid",
  "analyzed_at": "ISO timestamp",
  "current_daily_spend": 0,
  "current_cpa_avg": 0,
  "current_roas_avg": 0,
  "active_winners_count": 0,
  "active_losers_count": 0,
  "winners": [
    { "creative_id": "c-01", "ad_set_id": "...", "cpa": 0, "roas": 0, "spend_total": 0, "days_active": 0, "outcome": "winner" }
  ],
  "champions": [
    { "creative_id": "c-01", "post_id": "...", "promoted_at": "ISO timestamp" }
  ],
  "losers": [
    { "creative_id": "c-03", "reason": "kill_no_sale_at_breakeven|below_kpi_7d|under_fair_share_72h|creative_policy", "days_active": 0, "outcome": "loser" }
  ],
  "health_signals": {
    "frequency_max": 0,
    "cpm_trend": "up|flat|down",
    "creative_age_days_oldest": 0,
    "creative_age_days_newest": 0,
    "account_cpm_suspect": false,
    "funnel_atc_to_purchase_rate": 0,
    "funnel_checkout_to_purchase_rate": 0,
    "funnel_broken": false
  },
  "psm_real": 0,
  "margin_per_order_weighted": 0,
  "recommended_action": "continue|scale|refresh_creatives|kill|fix_funnel|test_other_account"
}
```

**Importante:** `winners[]` contém a lista completa de criativos vencedores (não só a contagem), já filtrada aqui na skill 11 por `outcome == "winner"`. Skill 14 apenas LÊ esse array e ordena por spend_total/days_active (NÃO re-filtra nem recomputa nenhum threshold de target — a classificação winner é responsabilidade exclusiva da skill 11). `champions[]` lista criativos promovidos a Post ID dedicado (espelha `manifest.champions[]`); `psm_real` aqui é o mesmo valor gravado em `manifest.psm_real`.

### Atualização do manifest (OBRIGATÓRIO — single source of truth)

Após gerar `dados.json`, atualizar `manifest.json` com campos canônicos:

- `manifest.psm_real` ← `psm_real` calculado nesta análise pela fórmula canônica `LTV / (CPA + COGS)`. **A skill 11 é a ÚNICA fonte que grava `manifest.psm_real`** (skill 12 lê daqui, nunca recalcula).
- `manifest.winners[]` ← lista de creative_ids vencedores desta análise (espelha `dados.json.winners[]`; skill 14 lê `manifest.winners[]` / `dados.json.winners[]`)
- `manifest.champions[]` ← acrescentar creative_ids promovidos a Post ID dedicado (não sobrescrever os já existentes; merge sem duplicar)
- `manifest.last_analysis_date` ← timestamp desta análise
- `manifest.analysis_count` ← incrementar +1
- `manifest.last_cpa_avg` ← `current_cpa_avg`
- `manifest.last_roas_avg` ← `current_roas_avg`
- `manifest.last_recommended_action` ← `recommended_action` (inclui `fix_funnel` e `test_other_account` do playbook — sinaliza pra skill 12 que o bloqueio não é escala)
- `manifest.account_cpm_suspect` / `manifest.funnel_broken` ← espelham `dados.json.health_signals` (sinalizam que matar produto/criativo seria erro — é conta ou página)
- Se `manifest.skipped_preflight` foi marcado no pré-flight (estratégia faltante), manter a flag.

Por que atualizar manifest: skills 12 e 14 leem `manifest.psm_real`, `manifest.winners[]` e `manifest.champions[]` como fonte canônica. O `dados.json` é histórico por análise; manifest é o estado atual consolidado.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `[YYYYMMDD]-analysis.md` e `ad-analysis.md`). **Isentos** (arquivos operacionais de handoff — rule 6b do CLAUDE.md, lista completa em `.claude/lib/workspace-index/workspace-layout.md`): `NEXT_BATCH_IDEAS.md`, `raw-pull-*.json`, `mcp-errors.log`, `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/11-ad-analysis/` antes de salvar.

Outputs em `workspace/[produto]/11-ad-analysis/`:
- `[YYYYMMDD]-analysis.md` (contendo todas as etapas do diagnóstico, incluindo a regra de KILL do playbook e os benchmarks de funil — histórico cumulativo)
- `[YYYYMMDD]-analysis.html` (companion visual)
- `ad-analysis.md` + `ad-analysis.html` (cópia da última rodada como relatório humano principal — é o que o painel do produto abre; sempre reflete a análise mais recente)
- `NEXT_BATCH_IDEAS.md` (input pra skill 08 no próximo batch — fecha loop)
- `dados.json` (handoff pra skill 12 — schema acima)

A pasta `11-ad-analysis/` acumula histórico — análises anteriores servem de input pra comparar evolução nas análises seguintes.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json` (ver lista canônica completa de campos acima):
- Adicionar `11-ad-analysis` em `skills_completed` (primeira vez) ou incrementar `analysis_count`
- Registrar `last_analysis_date`, `psm_real` (calculado via `LTV / (CPA + COGS)`), `winners[]`, `champions[]` (merge), `recommended_action`
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html)

## Mensagem Final

Adapte baseado no diagnóstico (ver Etapa 9 — recomendação de scaling). Termine sempre com uma próxima-ação CLARA:

- Continua rodando + PGS → monitora, próxima análise em 3-7 dias
- Escala → diga `'scale'`
- Iteração de criativos → diga `'creatives'`
- Ajuste de oferta → diga `'offer'`
- Ajuste de página → diga `'copy'` ou `'page'`
- Bloqueio técnico → resolução específica + nova análise depois
