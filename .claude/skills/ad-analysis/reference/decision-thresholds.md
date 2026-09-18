# Ad Analysis · Referência: 4Pi, frameworks e Decision Thresholds (ETAPA 2, primeira parte)

> Os sistemas a puxar antes dos Pi's e o bloco canônico que todas as etapas seguintes usam: unit economics da `offer-builder`, KPI da campanha, fórmula do PSM real e como obter o CAC real, réguas de kill, as 4 classes com a fórmula de classificação, benchmarks e taxas do batch, estados intermediários, dados insuficientes, CPM subindo, montanha-russa e winner picking. Abra ao começar a ETAPA 2.

### ETAPA 2 — 4Pi Analysis (Ordem EXATA)

**Frameworks a puxar ANTES de ler os Pi's (rode a `best_query` de cada):**
- **4Pi Analysis (Spend, Frequency, CPM, Cost per Result)** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) — o sistema completo da ordem dos 4 Pi's e o que cada um contextualiza no próximo.
- **4Pi+2 Dashboard & Custom Metrics** (rode `4Pi+2 custom metrics dashboard GPT account centers Ads Manager`) — quais colunas customizadas montar no Ads Manager pra ler os Pi's corretamente (freq diária, CPM, cost per result por ad set).
- **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — fundamenta o `psm_real` calculado abaixo (PSM substitui ROAS como métrica-mãe de scaling).

#### Decision Thresholds (bloco canônico — referenciado por TODOS os steps abaixo)

Defina estes valores UMA vez no topo da análise. Todos os steps (Pi 4, ETAPA 3, ETAPA 9, ETAPA 11) usam ESTES, sem redefinir.

**Unit economics (de `offer-builder/dados.json`):**
- `breakeven_cpa = offer.unit_economics.weighted_margin_per_order` (denominador de margem canônico)
- `target_cpa_2x = offer.unit_economics.target_cpa_primary_2x`
- `target_cpa_3x = offer.unit_economics.target_cpa_primary_3x`
- **`target` = `target_cpa_2x` em TODAS as classificações desta skill** (quando o texto diz "target", é este). `target_cpa_3x` é só o alvo esticado de referência pra leitura de scaling agressivo na ETAPA 9 — não entra em nenhuma decisão de kill.
- **COGS canônico = somatório de TODOS os campos de `offer.cogs_breakdown`** (NÃO existe campo `cogs_total`). Itere sobre as chaves do objeto — **nunca some uma lista fixa de campos**. O bloco tem hoje 8 itens (`product_delivered`, `shipping_to_customer`, `pick_pack`, `payment_processing`, `taxes_and_duties`, `subscription_app_fee`, `agency_fee_variable`, `refund_chargeback_provision`) e pode crescer; somar só os 5 antigos infla a margem e derruba o CPA/PSM pro lado otimista. **Todos os valores são dinheiro POR PEDIDO, nunca percentual** — se algum campo vier como percentual, é erro de gravação da `offer-builder`: marque `data_gap` e não converta por conta própria. **Ad spend nunca está aqui** (ele é o CAC do PSM); somá-lo contaria o mesmo dinheiro duas vezes.
- **Fallback** se campos não existirem (oferta antiga): `breakeven_cpa = AOV / breakeven_roas` (mesmo fallback da Skill `ad-strategy`); se nem esses campos existirem, usar default conservador e marcar `data_gap`.
- **`fair_share` = spend total do ad set ÷ N ads ativos** (a fatia que cada criativo receberia numa distribuição uniforme). É a régua de **entrega** (Pi 1: o algoritmo está ou não votando neste ad) — nunca use "% do spend total" fixo: com 10-12 criativos, 10% do total É o fair share, e um critério fixo condenaria até o ad perfeitamente distribuído. **`fair_share` não classifica mais ninguém como winner** — a classificação usa `spend_share_7d` e a comparação com o KPI da campanha (bloco abaixo).

**KPI da CAMPANHA (métrica de referência — é o que separa breakthrough de ilusão):**
- `campaign_cpa` = spend da campanha ÷ purchases da campanha, na janela de 7 dias
- `campaign_roas` = revenue da campanha ÷ spend da campanha, na janela de 7 dias
- `account_spend_7d` = spend total da conta em 7 dias. Na estrutura da Skill `ad-strategy` (uma campanha por produto, com N ad sets sob o mesmo CBO), `account_spend_7d` é o spend dessa campanha; quando a Skill `scale-engine` já criou campanhas ABO paralelas, use o total da conta.
- `spend_share_7d` do ad = `ad_spend_7d ÷ account_spend_7d`
- `ad_kpi_vs_campaign` = `ad_cpa <= campaign_cpa` (ou `ad_roas >= campaign_roas` quando o AOV varia entre ads — regra de desempate igual à do bloco "Winner picking")
- Se não há purchases suficientes na campanha pra calcular `campaign_cpa` com estabilidade (learning phase, < ~50 conversões em 7 dias), a comparação é **preliminar**: marque `data_gap` e não classifique ninguém como breakthrough ainda.

> **Incremental Attribution (setting do Ads Manager, 2025+):** se o membro ligou esse setting em alguma campanha, o CPA reportado dela NÃO é comparável ao CPA clássico — o Meta passa a contar só conversões que julga ter causado (conversões reportadas caem, CPA observado sobe, e o setting trava as attribution settings). Nesse caso, re-baseline TODOS os thresholds desta análise antes de qualquer kill naquela campanha, e trate a leitura como ferramenta de alocação de budget, não de kill de criativo. No teste padrão da Skill `ad-strategy`, o baseline é 7d-click/1d-view — a régua de kill foi calibrada nele.

**PSM real (fórmula canônica — mesma base do `psm_theoretical` da skill `offer-builder`):**
```
psm_real = LTV / (CAC_real + COGS)
```
- **`CAC_real` = ad spend do período ÷ clientes NOVOS do período.** Os clientes novos vêm do **Shopify** (`new customer = TRUE`), **não** do gerenciador de ads. O denominador é CAC, não CPA de plataforma (`.claude/lib/unit-economics/README.md` §3).
- `COGS` = somatório de TODOS os campos de `offer.cogs_breakdown` (regra acima).
- `LTV` = de `offer-builder/dados.json` (ou AOV do primeiro pedido se LTV ausente — recompra estimada não entra).
- Thresholds PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.
- **A skill `ad-analysis` é a ÚNICA fonte que grava `manifest.psm_real`** (a partir de performance real). Também grava em `ad-analysis/dados.json`. Skill `scale-engine` LÊ `manifest.psm_real`; nunca recalcula.

> **Por que o denominador mudou (e por que isso importa):** a skill `offer-builder` grava `psm_theoretical` com **CAC** (base Shopify, `unit_economics.cac_basis: "shopify_new_customer"`), e a skill `scale-engine` compara `psm_real` contra `psm_theoretical` com tolerância de 20% pra liberar escala. Enquanto esta skill usava o **CPA de plataforma** — que conta conversões atribuídas pelo Meta, incluindo cliente recorrente, e por isso é sempre MENOR que o CAC real numa loja com recompra — o `psm_real` saía **otimista** e podia liberar escala indevida. Os dois números só são comparáveis na mesma base.

**Como obter `CAC_real` (em ordem, sem inventar):**
1. **Shopify** — ad spend do período ÷ pedidos marcados como `new customer = TRUE` no mesmo período. É a base canônica.
2. **Se o membro não tem o número de clientes novos à mão:** pergunte diretamente ("no Shopify, quantos pedidos do período foram de **cliente novo**?"). Uma pergunta, sem rodeio.
3. **Se ele não conseguir informar:** grave `psm_real` mesmo assim usando o CPA de plataforma como proxy, mas marque **`psm_real_basis: "platform_cpa_proxy"`** no `dados.json` e no manifest, e diga no relatório que o número está **otimista** e que a comparação com `psm_theoretical` (que usa CAC) não é válida nessa base. Quando a base é proxy, o PSM **não** libera escala sozinho.
4. Quando a base é Shopify, grave `psm_real_basis: "shopify_new_customer"`.

> **Sanidade (cânone §3):** o piso realista de CAC em escala é US$ 15–25. Se o `CAC_real` medido vier abaixo disso, desconfie da atribuição (ou de estar medindo CPA disfarçado de CAC) antes de comemorar.

> `observed_cpa_avg_last_7d` (CPA médio de plataforma dos últimos 7 dias) continua sendo lido e gravado — ele é a régua de kill de conta nova, a leitura do Pi 4 e o `current_cpa_avg` do `dados.json`. O que ele **não** é mais: o denominador do PSM.

**Réguas de KILL (cânone `.claude/lib/ad-taxonomy/README.md` §3 — a decisão de matar):**
- **Conta madura** (existe ≥ 1 breakthrough rodando): kill no nível do **AD SET**, após **7 dias sem spend E sem KPI**.
- **Conta nova** (nenhum breakthrough ainda): kill do ad que gastou **≥ 8× o `target` CPA sem nenhuma purchase**.
- **Ad novo overspendando:** **24-48h de carência** antes de qualquer decisão — o Meta costuma corrigir o pacing sozinho.
- **Qualquer conta:** julgue por **média** da janela, nunca por dia isolado.
- **Exceção (segura):** criativo com **2+ initiate-checkouts** no comecinho → deixa rodar mais (Meta tem sinal pra otimizar), mesmo se já cruzou uma régua.
- **Funil quebrado antes de matar:** se houve checkouts mas as taxas de funil estão abaixo de ATC→compra 20-25% / checkout→compra 40-50% (com a amostra mínima da ETAPA 6B), o bloqueio é página/oferta, não o criativo → NÃO matar o criativo; rotear pra `copy-engine`, `page-design` ou `offer-builder`.
- **Conta antes de produto:** CPM muito acima do nicho → suspeitar da CONTA primeiro; testar o mesmo criativo em outra conta antes de matar o produto.
- **Não existe régua "1-2× breakeven CPA sem venda".** A 1× CPA há ≈ 37% de chance de zero vendas por puro acaso (≈ 14% em 2×) — matar ali descarta criativo bom por ruído.

**Classificação — as 4 classes (cânone `.claude/lib/ad-taxonomy/README.md` §2; vale pra ETAPA 3, 5, 9, 11 e pro handoff das skills `scale-engine` e `content-recycler`):**

O campo canônico gravado por criativo é **`ad_class`**, com quatro valores possíveis. Calcule assim:

```
ad_kpi_vs_campaign = ad_cpa <= campaign_cpa   (ou ad_roas >= campaign_roas)
spend_share_7d     = ad_spend_7d / account_spend_7d

breakthrough  = ad_kpi_vs_campaign AND puxa spend
                (conta pequena, < ~$3k/dia: spend_share_7d >= 0.30
                 conta grande, > ~$500k/mês: spend_share_7d >= 0.05-0.10)
spend_winner  = spend_share_7d >= 0.10 AND NOT ad_kpi_vs_campaign
kpi_winner    = ad_kpi_vs_campaign AND spend_share_7d < 0.10
loser         = spend_share_7d <= 0.02 em 7 dias
```

> **Gastar sem bater KPI não faz loser.** O cânone §2 é explícito: ad que puxa spend sem bater o KPI é **`spend_winner`** — o destino é iteração (autópsia do que o algoritmo gostou), nunca a lixeira. A única régua de gasto-sem-venda que MATA é o **8× de conta nova** (§3). Faixa intermediária (spend share entre 2% e 10%, sem KPI) não é classe: cai nos estados intermediários abaixo (NEEDS OPTIMIZATION / EM APRENDIZADO) até a leitura fechar.

| `ad_class` | O que é | Destino |
|---|---|---|
| **`breakthrough`** | KPI do AD melhor que o KPI da CAMPANHA **e** puxa spend | **Escala (skill `scale-engine`) + reciclagem (skill `content-recycler`)** — o único que libera as duas |
| **`spend_winner`** | Puxa spend mas KPI abaixo do da campanha | Iterar (skill `creative-engine`), **não escalar** |
| **`kpi_winner`** | Bate o KPI mas **não puxa spend** | **Tratar como loser para decisão** — não escala, não recicla, não vira learning replicável |
| **`loser`** | ≤ 2% do spend da conta em 7 dias ("não fez nada pela conta") | Graveyard / limpeza pela régua de kill do ad set |

> **O falso positivo que essa skill produzia:** a definição anterior (`CPA ≤ target` + `spend ≥ 50% do fair_share`) classificava como "winner" exatamente o que o cânone chama de **KPI winner** — ad que bate um alvo estático numa amostra pequena. Isso se propagava pra skill `scale-engine` (escala prematura) e pra skill `content-recycler` (reciclagem de criativo que nunca provou nada). O que separa breakthrough de ilusão é a comparação com **o KPI da própria campanha**, não com um alvo fixo, somada à prova de que o ad **puxa spend**.

**Benchmarks do cânone §2** (use pra calibrar expectativa, nunca como meta artificial):
- **≤ 2% do spend da conta em 7 dias = loser.**
- **Super winner absorve 30-40% do spend** da conta.
- **Hit rate esperado de super winner: 1-3%** dos criativos testados. Um batch sem breakthrough não é anomalia — é o normal estatístico.

**Taxas do batch (grave no `dados.json`; sem elas o membro não sabe se o problema é volume ou intenção):**
- `hit_rate` = criativos que bateram o KPI da campanha ÷ conceitos testados no batch
- `breakthrough_rate` = criativos `breakthrough` ÷ conceitos testados no batch
- Se o `breakthrough_rate` **caiu** quando o volume de criativos subiu, o problema é intenção, não volume: o próximo batch deve ser menor e mais deliberado (a diretiva vai pro `NEXT_BATCH_IDEAS.md`).

**Estados intermediários (não são classes — são "ainda não dá pra classificar"):**
- **NEEDS OPTIMIZATION:** `spend_winner`, ou ad com KPI entre o da campanha e 2× o `target` após 7 dias — iterar, não pausar.
- **EM APRENDIZADO:** < 7 dias rodando, ou a campanha ainda sem `campaign_cpa` estável (learning phase) — aguardar antes de classificar. Nunca grave `breakthrough` nesse estado.

Aplique os 4 Pi's **NA ORDEM** (Spend → Frequency → CPM → Cost per Result). A ordem importa — cada Pi contextualiza o próximo.

#### Dados insuficientes — como proceder

- **Ad set rodou < 24h**: análise 4Pi é **inválida**; apenas diagnóstico qualitativo. Marque "PRELIMINAR" no output.
- **Volume de conversões baixo** (poucas purchases, CPA instável dia-a-dia): CPA é ruído; use Spend + Freq + CPM apenas. CPA column = "insufficient data". O gate clássico da learning phase **continua valendo em 2026**: ~50 eventos de conversão em 7 dias por ad set pra sair de learning — abaixo disso, o CPA balança e a leitura é preliminar. O que mudou (desde abril/2026) é outra coisa: edições antes consideradas "seguras" (ajuste pequeno de bid, tweak de criativo) passaram a **resetar o learning com mais facilidade** — mais um motivo pro "não mexe por 3 dias" da Skill `ad-strategy`.
- **Dados faltando Frequency ou CPM** (API error): tentar refetch; se persistir, documentar como `data_gap` e pular aquele Pi.

#### CPM subindo: fadiga OU sazonalidade?

Antes de declarar "fadiga" (que justifica creative refresh), checar:
- Calendário: Q2-Q4 geralmente vê CPM subindo (holiday prep, Black Friday, Xmas)
- Benchmark setor: olhe CPM médio do seu vertical na semana atual (Meta insights ou reports de terceiros)
- Delta relativo: se seu CPM subiu 15% mas vertical subiu 20%, você está na média — NÃO é fadiga
- Só declare fadiga se CPM subiu > 20% VS vertical e freq diária > 1.5

#### Dia ótimo → dia péssimo: montanha-russa OU mudança na conta?

Oscilação diária forte não é, por si, sinal de criativo morto — os dois checks abaixo rodam ANTES de qualquer hipótese de fadiga ou kill:

- **Cruze com o ad log primeiro (Contexto, item 4g):** todo degrau da janela (queda de quinta, pico de sábado) é confrontado com as mudanças registradas em `workspace/[produto]/ad-log.md`. Mudança logada que explica o degrau encerra o mistério (high spender pausado semanas atrás, reset de budget, LP trocada, promo que começou). Os dois achados de diagnóstico: **mudança sem o efeito esperado** e **efeito sem mudança conhecida** — registre-os na hipótese causal da ETAPA 7. **Fallback:** sem `ad-log.md` (produto anterior ao cânone), pergunte ao membro se algo mudou na conta na janela antes de atribuir o degrau a fadiga — e logue o que ele relatar com executor `membro`.
- **Diagnóstico da montanha-russa** (rode `roller coaster performance dias ótimos e péssimos we don't sell to robots Meta devs`) — separa os 3 fatores fora do controle (incluindo mudanças feitas pelos devs do Meta e o fato de que não se vende para robôs) do único fator controlável. Dias ótimos e péssimos alternados com média da janela saudável = comportamento normal do leilão, não defeito do criativo; a régua de decisão continua sendo a **média**, nunca o pior dia.

#### Winner picking — ROAS ou CPA?

Para decisões de "qual ad (criativo) é melhor":
- Use ROAS quando AOV varia entre ads (ex: um criativo puxa mais bundle/upsell)
- Use CPA quando AOV é ~estável
- **Desempate por lucro (quando os dados existem):** lucro por compra = `AOV − COGS − CPA` (comparável entre ads quando o AOV varia); ou lucro por clique = `(AOV × CVR) − CPC` (quando quer comparar eficiência de tráfego). Nunca misture as duas réguas na mesma comparação.
