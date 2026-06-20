---
name: ad-analysis
description: Engine de análise de performance de Meta Ads. Aplica a REGRA DE KILL operacional (criativo gasta 1-2× o breakeven CPA sem venda → mata; CPA manda, não CTR), usa CPM como sinal de saúde da conta, diagnostica funil quebrado por benchmarks (ATC→compra, checkout→compra), e lê tudo por 4Pi (Spend → Frequency → CPM → Cost per Result) + PSM como diagnóstico. Faz 19-point diagnostic de losers, extração de learnings de winners, framework de 12 perguntas (feedback loops), e recomendações imediato/curto/médio prazo. Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "ver resultado", "diagnóstico", ou após rodar a campanha da Skill 10. Entrega decisões concretas — matar criativo, testar produto em outra conta, escalar, refresh, ou ajustar oferta/página.
---

# Ad Analysis Engine

## Quando Usar
Quando a campanha está rodando e o membro precisa diagnosticar o que está acontecendo e decidir próximos passos. Esta skill NÃO é "reportar dados" — é **diagnóstico + decisão**. Sai com ações concretas (hoje / 3-7 dias / 2-4 semanas).

## PLAYBOOK — A camada de execução (decisão de KILL real)

A base Aura tem a TEORIA da leitura (4Pi, PSM). Este playbook é a camada de EXECUÇÃO operacional — exatamente o que decidir olhando o Ads Manager. Quando o playbook e a leitura teórica conflitam numa decisão de matar/manter criativo, **o playbook manda na decisão**; o 4Pi/PSM continuam como o RACIOCÍNIO que explica o porquê.

> Os números de breakeven CPA vêm de `04-offer.json` (`unit_economics.weighted_margin_per_order`). Toda regra abaixo é relativa a ESSE breakeven, não a um valor fixo.

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
- **Abaixo desses números = o bloqueio é funil/página/oferta, NÃO necessariamente o criativo.** Ex: criativo trouxe 3 checkouts e 0 venda → está abaixo da média ideal; o problema mais provável está na página/checkout, não no ad. Não mate o criativo por algo que é culpa da página.
- Esse cruzamento evita o erro caro de matar um criativo bom porque a página converte mal.

## Antes de Começar

### Pré-flight
- [ ] `10-ad-strategy.json` existe
- [ ] Dir `workspace/[produto]/11-analysis/` existe (`mkdir -p`)
- [ ] Se houver análises anteriores, ler AS 2 MAIS RECENTES (para delta/trend analysis)

> **report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

> **Se `10-ad-strategy.json` faltar:** não aborte seco. Ofereça (A) rodar a skill 10 agora pra gerar a estratégia, OU (B) prosseguir com targets genéricos (CPA = `breakeven_cpa` do `04-offer.json` se existir, senão default conservador) marcando `manifest.skipped_preflight += ["10-ad-strategy.json"]` e avisando no output final que recomenda re-executar. Se profile/manifest estiverem TOTALMENTE ausentes, ofereça rodar o setup (skill 00) inline.

### Contexto a carregar

1. Leia `workspace/profile.md` (budget — contexto pra decisões de scale)
2. Leia `workspace/[produto]/04-offer.md` (target CPA, breakeven ROAS, margem — benchmarks pra avaliar performance)
3. Leia `workspace/[produto]/10-ad-strategy.md` (estrutura da campanha, conceitos testados, regras de decisão)
4. Leia `workspace/[produto]/11-analysis/` — **SE EXISTIR**, leia análises anteriores em ordem cronológica (pra ver evolução, identificar tendências, comparar com análises passadas)
5. **Puxe os SISTEMAS NOMEADOS da base — NÃO use query genérica.** Rode `search_knowledge` com a `best_query` exata de cada framework relevante pra ETAPA que está executando (cada ETAPA abaixo já lista os seus). O índice completo do domínio desta skill (meta-ads-strategy, ~26 frameworks com suas queries) está em **`.claude/lib/kb-index/`** (`frameworks.json` + `README.md`, mapa skill→domínio no README). Os sistemas de maior impacto pra leitura de performance, com a query a rodar:
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

Use 1-3 chamadas por análise. Não desperdiçar créditos em ad set perdedor.

Se TrendTrack NÃO estiver disponível, siga ETAPA 1 normalmente.

### ETAPA 1 — Obter Dados (cascade: oficial → Pipeboard → manual)

Aura tenta 3 caminhos em ordem. Cada falha cai pro próximo silenciosamente — o membro vê apenas a versão final com label indicando qual modo entregou os dados.

#### Caminho 1 — Meta MCP **oficial** (preferencial desde 2026-04-29)

1. Verificar se tools com prefixo `mcp__meta__ads_` estão na sessão (prefixo canônico do connector oficial — ver `.claude/lib/mcp-detect/README.md`):
   ```
   official_mcp_available = qualquer tool começando com mcp__meta__ads_get_ad_accounts existe
   ```

2. Se sim, tentar listar contas:
   ```
   accounts = mcp__meta__ads_get_ad_accounts()
   ```
   - Sucesso E ad_account do membro NÃO marcado "disabled" → invocar receita `sync-campaign-from-meta-official.md`
   - Conta marcada "disabled" no rollout gradual da beta → logar `account_disabled_in_official_beta` em `mcp-errors.log` e cair pro Caminho 2
   - OAuth expirado → tentar uma única re-autorização inline; se membro recusa, cair pro Caminho 2

3. Receita oficial salva pull completo em `workspace/[produto]/11-analysis/raw-pull-[timestamp].json` com `source: "meta_mcp_official"` + blocos extras (`dataset_health`, `market_context` com industry benchmarks, auction ranking, opportunity score, anomalies). **ZERO interação com o membro.** Vá pra ETAPA 2.

#### Caminho 2 — Meta MCP via Pipeboard (3rd party, fallback)

Acionado quando o Caminho 1 falha. Verificar se MCP legado `meta-ads` (binary local do Pipeboard) está disponível:

```
pipeboard_mcp_available = tools com prefixo mcp__meta-ads__ existem
```

Se sim, invocar receita legacy `sync-campaign-from-meta.md` com `fallback_reason` preenchido conforme o motivo do Caminho 1 ter falhado. JSON resultado tem `source: "meta_mcp_pipeboard"` e o mesmo shape base (sem os blocos `dataset_health` e `market_context` exclusivos do oficial).

#### Caminho 3 — Manual (último recurso)

Quando ambos MCPs falham (não configurados, ambos token/OAuth expirados, ambos rate-limited):

1. Logar ambos os erros em `workspace/[produto]/11-analysis/mcp-errors.log`
2. Pedir ao membro:

   > "MCP do Meta Ads não respondeu (motivo: oficial=[erro], pipeboard=[erro]). Cola os dados aqui — screenshot ou números. Preciso ver por ad set: Spend, Frequency, CPM, CPC, Cost per Purchase, ROAS, e (importante pro diagnóstico de funil) Adds to Cart e Checkouts Initiated além das Purchases. E quantos dias cada ad set está rodando."

3. ESPERE a resposta. Parse manual. Marcar `source: "manual_paste"` internamente.

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

Se `dataset_health.match_quality_score < 7` → marcar warning no relatório: "Match quality ruim, CPAs podem estar inflados por undercounting de conversões". Antes esse contexto só vinha do Events Manager manualmente.

> Pra interpretar e corrigir match quality baixa: **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`). Diz quais parâmetros de advanced matching (email, click ID) elevam o EMQ e quando um EMQ baixo está inflando o CPA observado — não confunda CPA inflado por undercounting com criativo ruim antes de checar isso.

### ETAPA 2 — 4Pi Analysis (Ordem EXATA)

**Frameworks a puxar ANTES de ler os Pi's (rode a `best_query` de cada):**
- **4Pi Analysis (Spend, Frequency, CPM, Cost per Result)** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) — o sistema completo da ordem dos 4 Pi's e o que cada um contextualiza no próximo.
- **4Pi+2 Dashboard & Custom Metrics** (rode `4Pi+2 custom metrics dashboard GPT account centers Ads Manager`) — quais colunas customizadas montar no Ads Manager pra ler os Pi's corretamente (freq diária, CPM, cost per result por ad set).
- **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — fundamenta o `psm_real` calculado abaixo (PSM substitui ROAS como métrica-mãe de scaling).

#### Decision Thresholds (bloco canônico — referenciado por TODOS os steps abaixo)

Defina estes valores UMA vez no topo da análise. Todos os steps (Pi 4, ETAPA 3, ETAPA 9, ETAPA 11) usam ESTES, sem redefinir.

**Unit economics (de `04-offer.json`):**
- `breakeven_cpa = offer.unit_economics.weighted_margin_per_order` (denominador de margem canônico)
- `target_cpa_2x = offer.unit_economics.target_cpa_primary_2x`
- `target_cpa_3x = offer.unit_economics.target_cpa_primary_3x`
- COGS canônico = somatório de `offer.cogs_breakdown` (NÃO existe campo `cogs_total`)
- **Fallback** se campos não existirem (oferta antiga): `breakeven_cpa = offer.unit_economics.weighted_margin_per_order`; se nem esse existir, usar default conservador e marcar `data_gap`.

**PSM real (fórmula canônica — unificada com skill 12):**
```
psm_real = LTV / (CPA + COGS)
```
- `CPA` = `observed_cpa_avg_last_7d` (CPA médio real dos últimos 7 dias)
- `COGS` = somatório de `offer.cogs_breakdown`
- `LTV` = de `04-offer.json` (ou AOV se LTV ausente)
- Thresholds PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.
- **A skill 11 é a ÚNICA fonte que grava `manifest.psm_real`** (a partir de performance real). Também grava em `latest.json`. Skill 12 LÊ `manifest.psm_real`; nunca recalcula.

**Gatilho de KILL operacional (PLAYBOOK — a decisão de matar criativo):**
- **KILL imediato:** criativo gastou **1-2× breakeven CPA SEM venda** → pausa. CPA manda, CTR não salva.
- **Exceção (segura):** criativo com **2+ initiate-checkouts** no comecinho → deixa rodar mais (Meta tem sinal pra otimizar), mesmo já no range de kill.
- **Funil quebrado antes de matar:** se houve checkouts mas as taxas de funil estão abaixo de ATC→compra 20-25% / checkout→compra 40-50%, o bloqueio é página/oferta, não o criativo → NÃO matar o criativo; rotear pra 06/07/04.
- **Conta antes de produto:** CPM muito acima do nicho → suspeitar da CONTA primeiro; testar o mesmo criativo em outra conta antes de matar o produto.

**Winner / Loser (definição única — vale pra ETAPA 3, 9, 11 e handoff pra skill 14):**
- **WINNER:** ad recebeu spend, CPA ≤ target, e a campanha overall não piorou.
- **LOSER:** disparou o gatilho de KILL (1-2× breakeven CPA sem venda, fora da exceção de checkouts) OU ad desligado após 7 dias com **< 10% do spend total** OU **abaixo do KPI** (CPA acima do target após 7 dias). Qualquer dessas condições = loser.
- **NEEDS OPTIMIZATION:** CPA entre target e 2× target após 7 dias — iterar, não pausar ainda.
- **EM APRENDIZADO:** ainda não atingiu 1× breakeven CPA de spend OU < 7 dias rodando — aguardar antes de decidir.

Aplique os 4 Pi's **NA ORDEM** (Spend → Frequency → CPM → Cost per Result). A ordem importa — cada Pi contextualiza o próximo.

#### Dados insuficientes — como proceder

- **Ad set rodou < 24h**: análise 4Pi é **inválida**; apenas diagnóstico qualitativo. Marque "PRELIMINAR" no output.
- **Volume de conversões baixo** (poucas purchases, CPA instável dia-a-dia): CPA é ruído; use Spend + Freq + CPM apenas. CPA column = "insufficient data". Avalie estabilidade do CPA pela variação entre dias, não por um número fixo de conversões — o Meta 2026 não usa mais o gate de 50 conversões da learning phase clássica.
- **Dados faltando Frequency ou CPM** (API error): tentar refetch; se persistir, documentar como `data_gap` e pular aquele Pi.

#### CPM subindo: fadiga OU sazonalidade?

Antes de declarar "fadiga" (que justifica creative refresh), checar:
- Calendário: Q2-Q4 geralmente vê CPM subindo (holiday prep, Black Friday, Xmas)
- Benchmark setor: olhe CPM médio do seu vertical na semana atual (Meta insights ou reports de terceiros)
- Delta relativo: se seu CPM subiu 15% mas vertical subiu 20%, você está na média — NÃO é fadiga
- Só declare fadiga se CPM subiu > 20% VS vertical e freq diária > 1.5

#### Winner picking — ROAS ou CPA?

Para decisões de "qual ad set é melhor":
- Use ROAS quando AOV varia entre ad sets (ex: um ad set traz upsells mais)
- Use CPA quando AOV é ~estável
- **Regra**: Profit per ad spend = (AOV × CVR − CPA) — use isto se disponível

#### Pi 1: SPEND

> Fundamento: **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) + **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`). Explicam por que o algoritmo concentra ou força spend e por que NÃO se desliga o top spender mesmo quando parece ineficiente.

"Quanto cada ad set recebeu de budget?"

Observação-chave: **Meta distribui spend pra onde ele ACREDITA que está funcionando**. Se o ad set A recebeu 40% do spend total e o B só 10%, o algoritmo tá "votando" que A é melhor (independente de CPA).

- **Ad set que recebeu muito spend** (share > 25% do total) → Meta tá confiante nele
- **Ad set com spend < 10% do seu share esperado** → Meta não tá confiante OU ad não foi aprovado OU audience muito pequena

Se um ad set "não gastou" em 3+ dias: verificar Ads Manager > Delivery insights + Review status. Pode ter sido pausado por policy.

#### Pi 2: FREQUENCY (Sinaliza Posição no Funil)

> Fundamento das signatures: **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`). É de lá que vêm as bandas de freq diária ↔ posição no funil (TOF/MOF/BOF) e a leitura de sprinters vs marathoners.

**Regra base: a frequency lida aqui deve ser a frequency DIÁRIA** (freq do dia, não acumulada da vida toda do ad set). Frequency lifetime cresce indefinidamente e não diz nada sobre fadiga atual. Sempre puxe/compare a freq diária. As bandas abaixo são para freq DIÁRIA.

Aplicar as signatures (freq diária):

- **Freq ~1.05** → **prospecting / TOF** (Top of Funnel) — novas impressões, cold traffic, ~1 impressão por pessoa/dia
- **Freq 1.1-1.4** → **MOF** (Middle) — starting to warm up
- **Freq 1.5-1.9** → **retargeting / BOF** (Bottom) — mesmas pessoas vendo várias vezes ao dia

Se a campanha tem TODOS os ad sets prospecting com freq diária bem acima de ~1.05 (puxando pra 1.5-1.9 como retargeting), falta **diversidade no funil** — você tá esgotando a audience sem abrir pra TOF novo. Recomendação: adicionar conceito TOF-friendly (hook problem, angle curiosity).

Se TODOS estão com freq diária ~1.05 e a campanha tá há 14+ dias, algo tá preventing Meta de re-engajar — geralmente CPM baixo + CTR muito baixo = audience não resonando.

#### Pi 3: CPM (Contexto Combinado com Freq)

**CPM isolado diz pouco. CPM + Freq diz muito:**

- **CPM alto (acima da média do nicho) + Freq diária alta (>1.5)** → Meta tá mandando pra audience cara (prime-time, premium placements) porque POUCA audience nova está disponível. Sinal de BOF / possível fadiga.
- **CPM alto + Freq diária baixa (~1.05)** → audience premium/cara mas fresca. Pode ser normal em nicho competitivo (skincare, finance, luxury).
- **CPM baixo + Freq alta** → Meta tá procurando impressões baratas com audience repetida. Frequência tá alta mas CPM não subiu = Meta não tá pagando caro pra forçar. Pode ser fadiga mas também pode ser só stabilidade.
- **CPM subindo no tempo** (comparar com análises anteriores se houver) → **possível fadiga**. Combinar com CTR falling pra confirmar.

**CPM também é sinal de saúde da CONTA (lente do playbook):** o mesmo produto/criativo pode dar CPM $30 numa conta e $100 noutra — o CPM diz tanto sobre a conta quanto sobre o criativo. Se o CPM está muito acima do esperado do nicho de forma generalizada (todos os ad sets caros, não só um criativo), suspeite da CONTA antes do produto. Antes de declarar o produto morto por economia ruim, marque `health_signals.account_cpm_suspect = true` e recomende **testar o mesmo criativo em outra conta de anúncio** (resiliência legítima: ter conta reserva ajuda aqui). Só mata o PRODUTO se ele não validar em conta nenhuma.

#### Pi 4: COST PER RESULT (O Que Realmente Importa)

Compare CPA de cada ad set contra o **target CPA da oferta** (do `04-offer.md`), usando as classificações do bloco **Decision Thresholds** definido no topo desta ETAPA:

- **CPA ≤ target** → WINNER (vai pro diagnóstico "scale")
- **CPA entre target e 2× target após 7 dias** → NEEDS OPTIMIZATION (iteração, não pausar ainda)
- **CPA acima do target (abaixo do KPI) após 7 dias OU < 10% do spend total após 7 dias** → LOSER (pausar)

**Gatilho de KILL do playbook (decisão operacional por criativo, antes do horizonte de 7 dias):** pra cada criativo, compare o spend acumulado com o breakeven CPA:
- **Gastou 1-2× breakeven CPA SEM venda → KILL** (pausa o criativo). CPA é o que manda — **CTR alto sem venda não salva**. Marque `outcome = "loser"` com `reason = "kill_no_sale_at_breakeven"`.
- **Exceção:** se o criativo tem **2+ initiate-checkouts** no comecinho, NÃO mate ainda — o Meta tem sinal pra otimizar; deixa rodar mais um pouco. Classifique como NEEDS OPTIMIZATION.
- **Funil quebrado (cruzar com benchmarks ANTES de matar):** se o criativo gerou ATC/checkouts mas as taxas estão abaixo de **ATC→compra 20-25%** ou **checkout→compra 40-50%**, o bloqueio é página/checkout/oferta, NÃO o criativo. Ex: 3 checkouts e 0 venda → checkout→compra = 0%, muito abaixo dos 40-50% esperados → o ad fez o trabalho, a página falhou. **NÃO mate o criativo**; roteie pra 06/07 (página) ou 04 (oferta) e registre o gargalo de funil no diagnóstico.
- **Conta antes do produto:** se o CPM está fora do esperado do nicho de forma generalizada (ver Pi 3, `account_cpm_suspect`), trate como problema de CONTA — recomende re-testar em outra conta antes de matar o produto.

Contexto importante: **CPA de um ad set isolado não é tudo**. "a campanha overall melhorou?". Se campanha total está dentro de CPA target mesmo com 1-2 ad sets fora, a maquina tá OK. Otimiza os outliers, não destrua campanha.

#### PSM real (gravado nesta análise — usado pela skill 12)

Calcule `psm_real` pela fórmula canônica do bloco **Decision Thresholds**:
```
psm_real = LTV / (CPA + COGS)
```
- `CPA` = `observed_cpa_avg_last_7d`
- `COGS` = somatório de `offer.cogs_breakdown` (NÃO existe campo `cogs_total`)
- `LTV` = de `04-offer.json` (ou AOV se LTV ausente)

Este `psm_real` é gravado em `latest.json` E em `manifest.psm_real` (ver ETAPA de update do manifest). Skill 12 lê de `manifest.psm_real`, nunca recalcula. Thresholds de ação PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.

### ETAPA 3 — Diagnóstico Por Ad Set

Pra CADA ad set, classifique:

**WINNER:** recebeu spend, CPA ≤ target, campanha overall melhorou.
→ Ação: escala automática via PGS. Se quer escalar mais agressivo, considera promover criativo a Champion (Post ID) e adicionar ad set dedicado.

**IN FATIGUE:** CPM subindo + CTR caindo + Freq subindo ao longo dos dias (comparar com análises anteriores).
> Antes de classificar fadiga, puxe **Why New Ads Steal From Old Ads / Creative Hamster Wheel** (rode `why new ads steal from old ads creative hamster wheel deprioritized`) — explica quando o sinal de "fadiga" é na verdade um ad novo canibalizando o spend do antigo (deprioritization), e não fadiga real da audience. Muda a ação: nesse caso o fix é consolidar, não refresh.
→ Ação: refresh criativo (trocar 1-2 dos 3 criativos do 3-2-2) OU adicionar novo batch de conceitos (Skill 08). **Não pausar ainda** — pode ainda estar performando acima do breakeven mesmo com sinais de fadiga.

**LOSER** (def. canônica do bloco Decision Thresholds): disparou o **gatilho de KILL** (gastou 1-2× breakeven CPA SEM venda, fora da exceção de 2+ checkouts) OU ad desligado após 7 dias com **< 10% do spend total** OU **abaixo do KPI** (CPA acima do target após 7 dias). Qualquer dessas = loser.
→ Ação: PAUSAR. Se produto já validado (outro criativo vende), mata rápido. Fazer diagnóstico profundo (Etapa 4) pra entender por que falhou.

**FUNIL QUEBRADO (não é o criativo):** o criativo trouxe ATC/checkouts mas as taxas estão abaixo dos benchmarks (ATC→compra < 20-25% ou checkout→compra < 40-50%).
→ Ação: **NÃO pausar o criativo** — o ad fez o trabalho, o gargalo é página/checkout/oferta. Rotear pra 06/07 (página) ou 04 (oferta). Registrar o gargalo de funil no `health_signals` e no NEXT_BATCH_IDEAS.

**CONTA SUSPEITA (não é o produto):** CPM generalizado muito acima do nicho (`account_cpm_suspect`).
→ Ação: re-testar o mesmo criativo/produto em OUTRA conta de anúncio antes de matar o produto. Só mata o produto se não validar em conta nenhuma.

**EM APRENDIZADO:** ainda não atingiu 1× breakeven CPA de spend OU < 7 dias rodando, spend baixo.
→ Ação: aguardar antes de decidir. Dê ao Meta tempo de estabilizar a entrega e o CPA antes de julgar (sem gate fixo de N conversões — Meta 2026 não usa mais o threshold clássico de 50 conversões da learning phase).

### ETAPA 4 — Diagnóstico Profundo de LOSERS (19-Point Diagnostic)

### 19-Point Loser Diagnostic

**Camada 1: Targeting (4 pontos)**
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
17. Pixel Match Quality < 80%
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
- Todos os ad sets em TOF? → funil raso, falta converter warm audience
- Todos em BOF? → falta trazer volume novo, tá escalando sobre a mesma audience
- Distribuído em TOF + MOF + BOF? → saudável

Recomendação baseada em desbalanço:
- Falta TOF → próximo batch inclui conceitos de awareness building (hook problem, curiosity, authority)
- Falta BOF → próximo batch inclui retargeting-style (offer-focused, urgency, comparison)

**6B — Conversão de funil (diagnóstico de funil quebrado — separa criativo de página/oferta):**

Calcule, com os dados do pull (ATC, initiate-checkout, purchases) por ad set E agregado da campanha:
- **Add-to-cart → compra = `purchases / add_to_cart`.** Benchmark: **20-25%** (a cada 10 ATC, ~2 compras).
- **Checkout → compra = `purchases / initiate_checkout`.** Benchmark: **40-50%** (média ~40%).

Leitura:
- **Dentro ou acima do benchmark** → o funil converte; se um criativo não vende, o problema é o criativo (entra na regra de KILL).
- **Abaixo do benchmark** → o bloqueio é PÁGINA / CHECKOUT / OFERTA, não o criativo. Ex: campanha com muitos checkouts e poucas vendas → checkout→compra abaixo de 40% → a página/checkout está vazando. **Não mate criativos por isso** — eles trouxeram intenção de compra que a página desperdiçou.
- Se os dados de ATC/checkout não vierem no pull (manual ou API limitada), marque `data_gap` e diga ao membro exatamente o que olhar no Shopify/Meta pra preencher (funnel do checkout: sessions → ATC → checkout → purchase).

Roteamento quando funil quebrado: checkout→compra baixo → `'page'`/`'copy'` (página vazando) ou checkout flow; ATC→compra baixo com checkout→compra ok → oferta/preço fraco no checkout → `'offer'`. Registre o gargalo em `health_signals` e no NEXT_BATCH_IDEAS pra não repetir o erro de matar criativo bom.

### ETAPA 7 — Framework de 12 Perguntas (Feedback Loops)

Aplique os princípios de "Framework de 12 Perguntas pra Feedback Loops". Aplique as perguntas aos dados:

1. Qual ad set teve maior ROAS e por quê?
2. Qual teve menor ROAS e por quê?
3. Qual criativo específico dentro dos winners tá puxando mais?
4. Houve variação significativa de performance por primary text?
5. Alguma headline se destacou?
6. Qual URL (se 3-2-2-2) converte melhor?
7. Frequency subiu mais rápido que esperado em algum ad set? (sinal de audience pequena)
8. CPM variou muito entre ad sets? (aponta pra diferenças de audience ou bidding)
9. CTR variou muito? (indicador de hook strength)
10. Conversão CTR→Purchase variou? (indicador de message match)
11. Retention no site (se tiver) — quanto tempo ficam?
12. Qual a hipótese causal principal pro resultado?

Compile respostas num bloco objetivo.

### ETAPA 8 — Recomendações Acionáveis (Imediato / Curto Prazo / Médio Prazo)

**AÇÕES IMEDIATAS (hoje/24h):**
- Pausar losers identificados na Etapa 3 (especificar quais ad sets)
- Consertar problemas técnicos identificados no 19-point (se houver)
- Verificar se PGS está ativo e disparou nos últimos dias (Automated Rules history)

**CURTO PRAZO (3-7 dias):**
- Se tem fadiga: refresh de criativos nos ad sets afetados (trocar 1-2 dos 3 no 3-2-2)
- Se falta diversidade de funil: gerar novo batch de conceitos (Skill 08) com foco na posição faltante
- Ajuste de URLs se 3-2-2-2 mostrou preferência clara de LP

**MÉDIO PRAZO (2-4 semanas):**
- Se winners estáveis: promover pra Champion (Post ID separado)
- Se CPA está melhor que target consistentemente: reavaliar se dá pra escalar mais (vertical + horizontal — delegar pra Skill 12)
- Se oferta parece ser o bloqueio: voltar pra Skill 04 e ajustar (bundle structure, guarantee, stack)
- Se página parece ser o bloqueio: voltar pra Skill 06/07 e iterar

### ETAPA 9 — Decisão de Scaling (Recomendação Clara)

> Fundamente a recomendação puxando os sistemas de scaling (rode as `best_query`): **Profitable Scaling Margin (PSM)** (`Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — usa o `psm_real` calculado na ETAPA 2 pra decidir agressivo/steady/breakeven/cortar; e **Performance Gate Scaling (PGS)** (`Performance Gate Scaling PGS automated rules total loss investment soft surfing`) — confirma se as automated rules estão ativas antes de prometer "escala automática". A montagem detalhada do plano de escala (vertical + horizontal) é delegada pra skill 12; aqui só a recomendação.

Baseado no diagnóstico completo, dê uma recomendação clara:

**SE CPA dentro do target E winning ads estáveis:**
"Continue rodando. PGS vai escalar automaticamente. Se quer escalar mais agressivo OU adicionar canais novos, diga **'scale'** pra eu montar o plano."

**SE CPA ≤ 0.7× target E winning ad claro:**
"Oferta forte, ads matando. Diga **'scale'** pra montar plano de escala vertical + horizontal. Pode considerar scaling aggressive em paralelo ao PGS."

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

1. Classificar outcome (alinhado ao bloco Decision Thresholds — o `outcome` aqui é o mesmo gravado em `winners[]`/`losers[]` de `latest.json`):
   - `winner`: CPA ≤ target E recebeu spend (≥ 10% do share) E campanha overall não piorou; sinal forte se spend > $300 E decile_rank 1-2
   - `loser`: disparou o gatilho de KILL (gastou 1-2× breakeven CPA sem venda, fora da exceção de 2+ checkouts) OU desligado após 7 dias com < 10% do spend total OU CPA acima do target após 7 dias
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
`workspace/[produto]/11-analysis/NEXT_BATCH_IDEAS.md`

**Critério de parada pra evitar loop infinito 09↔07:**

Antes de gerar ideias novas:
1. Se `NEXT_BATCH_IDEAS.md` já existe:
   - Ler versão anterior + ler `08-creatives.json` (criativos gerados desde última rodada)
   - Comparar: quantas ideias propostas na versão anterior **foram testadas** (viraram criativos em 08-creatives.json com performance em 09)?
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

O arquivo de análise é `workspace/[produto]/11-analysis/latest.json` (cópia do último análise — nome literal `latest.json` dentro da pasta `11-analysis/`, NÃO `11-analysis-latest.json`):

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
    { "creative_id": "c-03", "reason": "kill_no_sale_at_breakeven|below_kpi_7d|under_10pct_spend_7d|creative_policy", "days_active": 0, "outcome": "loser" }
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

Após gerar `latest.json`, atualizar `manifest.json` com campos canônicos:

- `manifest.psm_real` ← `psm_real` calculado nesta análise pela fórmula canônica `LTV / (CPA + COGS)`. **A skill 11 é a ÚNICA fonte que grava `manifest.psm_real`** (skill 12 lê daqui, nunca recalcula).
- `manifest.winners[]` ← lista de creative_ids vencedores desta análise (espelha `latest.json.winners[]`; skill 14 lê `manifest.winners[]` / `latest.json.winners[]`)
- `manifest.champions[]` ← acrescentar creative_ids promovidos a Post ID dedicado (não sobrescrever os já existentes; merge sem duplicar)
- `manifest.last_analysis_date` ← timestamp desta análise
- `manifest.analysis_count` ← incrementar +1
- `manifest.last_cpa_avg` ← `current_cpa_avg`
- `manifest.last_roas_avg` ← `current_roas_avg`
- `manifest.last_recommended_action` ← `recommended_action` (inclui `fix_funnel` e `test_other_account` do playbook — sinaliza pra skill 12 que o bloqueio não é escala)
- `manifest.account_cpm_suspect` / `manifest.funnel_broken` ← espelham `latest.json.health_signals` (sinalizam que matar produto/criativo seria erro — é conta ou página)
- Se `manifest.skipped_preflight` foi marcado no pré-flight (estratégia faltante), manter a flag.

Por que atualizar manifest: skills 12 e 14 leem `manifest.psm_real`, `manifest.winners[]` e `manifest.champions[]` como fonte canônica. Latest.json é histórico por análise; manifest é o estado atual consolidado.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/11-analysis/` antes de salvar.

Outputs em `workspace/[produto]/11-analysis/`:
- `[YYYYMMDD]-analysis.md` (contendo todas as etapas do diagnóstico, incluindo a regra de KILL do playbook e os benchmarks de funil — histórico cumulativo)
- `[YYYYMMDD]-analysis.html` (companion visual)
- `NEXT_BATCH_IDEAS.md` (input pra skill 08 no próximo batch — fecha loop)
- `latest.json` (handoff pra skill 12 — schema acima)

A pasta `11-analysis/` acumula histórico — análises anteriores servem de input pra comparar evolução nas análises seguintes.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json` (ver lista canônica completa de campos acima):
- Adicionar `11-ad-analysis` em `skills_completed` (primeira vez) ou incrementar `analysis_count`
- Registrar `last_analysis_date`, `psm_real` (calculado via `LTV / (CPA + COGS)`), `winners[]`, `champions[]` (merge), `recommended_action`

## Mensagem Final

Adapte baseado no diagnóstico (ver Etapa 9 — recomendação de scaling). Termine sempre com uma próxima-ação CLARA:

- Continua rodando + PGS → monitora, próxima análise em 3-7 dias
- Escala → diga `'scale'`
- Iteração de criativos → diga `'creatives'`
- Ajuste de oferta → diga `'offer'`
- Ajuste de página → diga `'copy'` ou `'page'`
- Bloqueio técnico → resolução específica + nova análise depois
