---
name: ad-analysis
description: Engine de análise de performance de Meta Ads. Lê a estrutura da Skill 10 (1 campanha com CBO → N ad sets, 1 ad set = 1 conceito) em DOIS níveis: por CONCEITO (o ad set — onde o CBO concentra gasto é o sinal) e por CRIATIVO (o ad dentro do ad set). Classifica cada criativo nas 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2 (loser · KPI winner · spend winner · breakthrough) — só o breakthrough (KPI do AD melhor que o KPI da CAMPANHA E puxando spend) libera escala e reciclagem; KPI winner é tratado como loser para decisão. Aplica as réguas de kill do cânone §3 (conta madura: ad set após 7 dias sem spend e sem KPI · conta nova: 8× target CPA sem purchase · ad novo overspendando: 24-48h), mede Hook rate e Hold rate (§4) pra dizer ONDE o criativo falhou, usa CPM como sinal de saúde da conta, diagnostica funil quebrado por benchmarks (ATC→compra, checkout→compra) e cruza com o espécime de copy da Skill 06, e lê tudo por 4Pi (Spend → Frequency → CPM → Cost per Result) + PSM como diagnóstico. Nenhuma recomendação de cortar spend por queda de ROAS sai sem passar por `.claude/lib/unit-economics/README.md` §4. Faz 19-point diagnostic de losers, extração de learnings de breakthroughs, checklist de 12 perguntas de feedback, e roda o checkpoint de kill (cadência quarta→domingo). NÃO configura escala nem kill por Automated Rule: condição de performance é recusada pelo Meta em campanha com CBO (cânone §6), então o ritmo de escala é o Scaling Protocol manual do §5, executado pela Skill 12 — o que esta skill confere são as duas automações de proteção (pico de gasto, URL errada). Lê os contratos dos produtores: da 08, `testing_method`+`angles[]` (num pack Marksman a leitura por criativo é "qual ÂNGULO venceu", não "qual execução"), `sub_avatar_id` (grava `winning_sub_avatar_id` — o sinal que volta pra pesquisa) e `valence`/`intensity` (diagnóstico de iteração que trocou de zona emocional sem perceber); da 10, `test_capacity.below_floor_directional_only` (teste nascido abaixo do piso = resultado DIRECIONAL: sem classificação formal, sem kill, sem escala). Lê `workspace/[produto]/ad-log.md` no início de TODA análise (cânone `.claude/lib/ad-log/README.md`) pra cruzar a janela de leitura com as mudanças executadas na conta, e grava no manifest `ad_classification[]` + `click_based_purchase_share`. Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "ver resultado", "diagnóstico", ou após rodar a campanha da Skill 10. Entrega decisões concretas — matar criativo, testar produto em outra conta, escalar, refresh, ou ajustar oferta/página.
---

# Ad Analysis Engine

## Quando Usar
Quando a campanha está rodando e o membro precisa diagnosticar o que está acontecendo e decidir próximos passos. Esta skill NÃO é "reportar dados" — é **diagnóstico + decisão**. Sai com ações concretas (hoje / 3-7 dias / 2-4 semanas).

## PLAYBOOK — A camada de execução (decisão de KILL real)

A base Aura tem a TEORIA da leitura (4Pi, PSM). Este playbook é a camada de EXECUÇÃO operacional — exatamente o que decidir olhando o Ads Manager. Quando o playbook e a leitura teórica conflitam numa decisão de matar/manter criativo, **o playbook manda na decisão**; o 4Pi/PSM continuam como o RACIOCÍNIO que explica o porquê. E quando o playbook diverge de um dos dois cânones do item 0 abaixo, **o cânone vence** — esta skill aplica, não redefine.

> Os números de referência vêm de `04-offer-builder/dados.json`: `breakeven_cpa` = `unit_economics.weighted_margin_per_order`, e `target` = `unit_economics.target_cpa_primary_2x` (é ele que entra na régua de 8× de conta nova). Toda regra abaixo é relativa a ESSES números, nunca a um valor fixo.

> Se existe `03-competitor-analysis/dados.json` com `monitoring_radar[]` (ETAPA 3E da Skill 03), releia a cada análise: cheque se algum `trigger_signal` disparou (concorrente escalando ângulo novo, entrante no formato, rede de afiliado acelerando) e, se sim, informe o membro com a `action_if_triggered` correspondente.

**0. Os dois cânones que governam esta skill (leia antes de classificar ou recomendar corte):**
- **`.claude/lib/ad-taxonomy/README.md`** — fonte única da classificação (§2, as 4 classes), das réguas de kill (§3) e das fórmulas de Hook/Hold (§4). Esta skill **mede e aplica**; não redefine nenhuma tabela localmente.
- **`.claude/lib/unit-economics/README.md`** — fonte única de margem, CPA/CAC e da **espiral do ROAS** (§4). Nenhuma recomendação de **cortar spend** por queda de ROAS sai desta skill sem passar por lá.

**1. Regra de KILL de criativo (as três réguas do cânone §3 — CPA manda, não CTR):**

A régua antiga ("gastou 1-2× o breakeven CPA sem venda → pausa") **saiu**: ela mata cedo por ruído. Com CPA saudável, a chance de **zero** vendas ao gastar exatamente 1× o CPA é ≈ 37% (≈ 14% em 2× CPA) — é o mesmo raciocínio de amostra mínima que a ETAPA 6B já aplica ao funil. Matar ali descarta criativo bom por acaso estatístico.

As réguas que valem, por contexto (cânone `.claude/lib/ad-taxonomy/README.md` §3):

| Situação | Régua |
|---|---|
| **Conta madura** (já tem breakthrough rodando) | kill no nível do **AD SET**, após **7 dias sem spend E sem KPI** — abre espaço, não persegue criativo individual |
| **Conta nova** (nenhum breakthrough ainda) | kill do ad que gastou **≥ 8× o target CPA sem nenhuma purchase** |
| **Ad novo overspendando** | **esperar 24-48h** antes de qualquer decisão — o Meta frequentemente corrige o pacing sozinho |

- **CTR alto sem venda não salva o criativo.** Scroll-stop ótimo e CTR alto não pagam a conta; a compra paga. Mas a decisão de matar é pelas réguas acima, não pelo CTR nem por 1-2× breakeven.
- **Nunca julgue por dia isolado.** A leitura é por **média** da janela, não pelo pior dia.
- **Exceção — 2+ checkouts no comecinho:** se o criativo já gerou 2+ initiate-checkouts (mesmo sem venda fechada), o Meta tem sinal pra otimizar. Deixa rodar mais antes de qualquer kill.
- **Produto já validado** (outro criativo já vende): a conta é madura → a régua é a do ad set, não a do ad individual. Criativo novo sem spend e sem KPI simplesmente não sobrevive à limpeza dos 7 dias.
- **Antes de qualquer kill:** cheque funil quebrado (item 3 abaixo) e conta suspeita (item 2). Ad que trouxe checkout que a página desperdiçou não é loser.

**2. CPM = sinal de saúde da CONTA (não do produto):**
- O MESMO produto/criativo pode dar **CPM $30 numa conta e $100 noutra.** CPM alto demais geralmente é a conta, não o produto.
- Antes de declarar um produto "morto" por CPM alto, **testar o mesmo produto/criativo em OUTRA conta de anúncio.** Só depois de não validar em conta nenhuma é que se mata o PRODUTO.
- Isso muda a ordem da decisão: CPM muito acima do esperado do nicho → primeiro suspeitar da conta (resiliência: ter conta reserva legítima ajuda aqui), não do criativo.

**3. Benchmarks de funil (diagnóstico de funil quebrado — separa criativo de página/oferta):**
- **Add-to-cart → compra = 20-25%** (a cada 10 ATC, ~2 compras fecham).
- **Checkout → compra = 40-50%** (média ~40%; iniciou checkout e finalizou).
- **Abaixo desses números = o bloqueio é funil/página/oferta, NÃO necessariamente o criativo.** Ex: criativo trouxe 3 checkouts e 0 venda → sinal de página/checkout, não do ad. Mas atenção à amostra: 0 venda em 3 checkouts acontece por puro acaso ~1 vez em 5 mesmo com funil saudável — só decrete "funil quebrado" com a amostra mínima da ETAPA 6B. Não mate o criativo por algo que é culpa da página.
- Esse cruzamento evita o erro caro de matar um criativo bom porque a página converte mal.

**4. Classificação = as 4 classes do cânone (o falso positivo que essa skill produzia):**
- A pergunta que separa um criativo que escala de uma ilusão **não** é "o CPA dele bateu o alvo?". É **"o KPI deste AD é melhor que o KPI da CAMPANHA — e ele puxa spend?"**. Só quando as duas coisas são verdadeiras existe **breakthrough**.
- **Ad que bate o KPI com pouco spend não é winner.** Ele não provou nada em escala; o KPI bonito veio de amostra pequena. Essa classe (`kpi_winner`) é **tratada como loser para efeito de decisão** — não escala (skill 12), não recicla (skill 14).
- Definições completas, destinos e benchmarks: `.claude/lib/ad-taxonomy/README.md` §2. Esta skill mede os números e aplica; não redefine as classes.

**5. Antes de recomendar CORTAR spend (a espiral do ROAS):**
- Queda de ROAS **não** autoriza, por si só, recomendar corte de spend. Cortar pode **aumentar** o prejuízo: os custos fixos não encolhem junto, então sobra menos receita para diluir a mesma base fixa.
- Rode `.claude/lib/unit-economics/README.md` §4 antes de escrever qualquer recomendação de redução. **Se os custos fixos mensais do membro não forem conhecidos, a recomendação vira pergunta** ("quanto você tem de custo fixo por mês?"), nunca instrução de cortar.
- **Se `15-finance-engine/dados.json` existir (Contexto, item 4d), o gate deixa de ser só bloqueio e vira número.** A 15 já rodou a conta com o custo fixo dentro e publicou o resultado; leia e aplique, sem recalcular:

  | `roas_spiral.verdict` da 15 | O que esta skill recomenda |
  |---|---|
  | `cut_spend_below_variable_breakeven` (`cut_spend_recommendation_allowed: true`) | **Cortar é certo** — cada dólar a mais destrói margem de contribuição. Vale a régua de descida do `ad-taxonomy` §5 (−20%, só com breakeven furado **por 24-48h persistentes** — um dia ruim isolado não dispara) |
  | `scale_up_accept_lower_roas` | **Cortar aumentaria o prejuízo.** A saída é **subir** spend aceitando ROAS menor, até o `spend_to_breakeven_with_fixed` que a 15 calculou |
  | `covers_fixed_costs` | **Segurar.** A operação cobre o fixo no nível de spend atual; não há corte a recomendar por queda de ROAS |
  | `blocked_pending_fixed_costs` | Fallback: volta a valer o bloqueio acima — a recomendação é a pergunta |

  Use `breakeven_roas_with_fixed` como a régua contra a qual o ROAS observado é comparado (o breakeven de variável sozinho não enxerga o fixo), e cite `spend_to_breakeven_with_fixed` como o número da ação quando o veredito for subir spend.
- **Sem o arquivo da 15, nada muda:** vale o comportamento de hoje (item 4c), com a recomendação virando pergunta enquanto os fixos forem desconhecidos.
- Isso vale pra ETAPA 8 (ações), ETAPA 9 (scaling) e pro `recommended_action` gravado no `dados.json`.

**6. Teste que nasceu abaixo do piso = resultado DIRECIONAL (gate do cânone §1):**
- Se `10-ad-strategy/dados.json → test_capacity.below_floor_directional_only` é `true`, o teste rodou abaixo do piso operacional de US$ 100-150/dia e o dado não sustenta decisão formal. Esta skill **diz isso ao membro com todas as letras**, trata TODA a leitura como direcional, **não classifica formalmente (sem `ad_class`), não autoriza kill (de criativo, ad set ou produto) nem escala** — a recomendação vira uma de duas: **subir o budget até o piso** OU **reduzir o nº de conceitos no ar** (o excedente entra na fila do próximo batch). `binding_constraint` diz qual restrição apertou o teste (Contexto, item 4f).
- **Fallback legado:** `test_capacity` ausente (estratégia gravada antes do campo existir) → siga o comportamento normal; se `test_budget_daily` existir e estiver abaixo de US$ 100/dia, aplique este item do mesmo jeito — é a mesma régua do cânone §1, verificada à mão.

## Antes de Começar

### Pré-flight
- [ ] `10-ad-strategy/dados.json` existe
- [ ] Dir `workspace/[produto]/11-ad-analysis/` existe (`mkdir -p`)
- [ ] Se houver análises anteriores, ler **as 2-3 mais recentes** + o `dados.json` consolidado (para delta/trend analysis). Ler todas só quando a análise pedir tendência longa (ex: sazonalidade de CPM).

> **report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma, seguindo o padrão de linguagem simples da regra 0 do `.claude/CLAUDE.md` (nenhuma sigla sem explicação imediata, zero frase de analista comprimida, números estatísticos em palavras). **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

> **Se `10-ad-strategy/dados.json` faltar:** não aborte seco. Ofereça (A) rodar a skill 10 agora pra gerar a estratégia, OU (B) prosseguir com targets genéricos (CPA provisório = `breakeven_cpa` do `04-offer-builder/dados.json` se existir, senão default conservador — **avisando que esse target provisório é 2× mais frouxo que o target normal `target_cpa_2x`**, então as classificações saem otimistas) marcando `manifest.skipped_preflight += ["10-ad-strategy/dados.json"]` e avisando no output final que recomenda re-executar. Se profile/manifest estiverem TOTALMENTE ausentes, ofereça rodar o setup (skill 00) inline.

### Contexto a carregar

1. Leia `workspace/profile.md` (budget — contexto pra decisões de scale)
2. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (target CPA, breakeven ROAS, margem — benchmarks pra avaliar performance; se não existir, leia o legado `relatorio.md`)
3. Leia `workspace/[produto]/10-ad-strategy/ad-strategy.md` (estrutura da campanha, conceitos testados, regras de decisão)
4. Leia `workspace/[produto]/11-ad-analysis/` — **SE EXISTIR**, leia as **2-3 análises mais recentes** + o `dados.json` consolidado (evolução, tendências, comparação com rodadas passadas). Todas só quando precisar de tendência longa.
4b. Leia `workspace/[produto]/06-copy-engine/dados.json` (se existir) — quatro campos, todos usados no diagnóstico de página da ETAPA 6B:
   - `voc_forced_continue` — se `true`, a copy foi escrita com VOC insuficiente (o membro escolheu prosseguir mesmo assim). Muda a hipótese causal do diagnóstico de underperformance (ETAPA 4 / 6B).
   - `claims_unverified` — se `true`, claims fortes saíram sem research foundation.
   - `specimen_primary` (+ `specimen_secondary`, `specimen_block_map`) — qual espécime estrutural a copy modelou. O catálogo está em `.claude/lib/swipe-models/specimens.json`; cada espécime traz `aplica_a` (page_type × awareness × sophistication × vertical) e `regra_diagnostica`. É o que permite perguntar, quando a página converte mal, se **a estrutura escolhida era a certa pro avatar**.
   - `markup_audit` — o resultado da auditoria de markup por camada (4 U's da headline, ideal prospect, big promise, first page test, 4 emoções, lead de 4 passos do Makepeace, defeitos encontrados, `verdict`). É o que permite perguntar **qual camada já tinha reprovado antes do launch**.
4c. Leia `workspace/[produto]/04-offer-builder/dados.json` → **`budget_viability.fixed_costs_monthly`** (os custos fixos mensais do membro; `null` quando ele nunca informou). Sem esse número, nenhuma recomendação de cortar spend pode ser emitida (PLAYBOOK item 5 + `.claude/lib/unit-economics/README.md` §4) — ela vira pergunta. Leia também `unit_economics.cac_basis` (deve ser `"shopify_new_customer"`) e o bloco `cogs_breakdown` inteiro — os dois entram no `psm_real`.
4d. Leia `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** → o bloco `roas_spiral`, quatro campos: `breakeven_roas_with_fixed`, `cut_spend_recommendation_allowed`, `verdict` e `spend_to_breakeven_with_fixed`. A skill 15 é a **produtora** desses números (ela roda a conta da espiral com o custo fixo do membro na mesa); esta skill **lê e aplica, nunca recalcula com fórmula própria**. Com eles, a decisão de spend do PLAYBOOK item 5 deixa de ser bloqueio e vira número: cortar, segurar ou **subir**. **Fallback (o arquivo não existe, ou o bloco veio com `verdict: "blocked_pending_fixed_costs"`):** o comportamento é exatamente o de hoje — vale o item 4c, e sem `fixed_costs_monthly` a recomendação de corte continua sendo **pergunta**, não instrução. A 15 nunca é pré-requisito desta skill.
4e. Leia `workspace/[produto]/08-creative-engine/dados.json → concepts[]` (se existir) — os campos de contrato que mudam a LEITURA desta análise:
   - **`testing_method`** (`marksman|sniper`) + **`angle`** + **`angles[]`** + **`hold_universal`**/**`hold_universal_validated`** — decidem O QUE a comparação entre os 3 ads de um ad set responde: num **Sniper**, "qual EXECUÇÃO venceu"; num **Marksman**, "qual ÂNGULO venceu" (bifurcação completa na ETAPA 3). `angles[]` traz os 3 ângulos em frase, um por criativo (`creative_n`), com o `sub_avatar_id` de cada um — é por essa frase que o vencedor de um Marksman é NOMEADO.
   - **`sub_avatar_id`** (por conceito; num Marksman, por item de `angles[]`) — permite registrar QUAL sub-avatar produziu o vencedor (`winning_sub_avatar_id`, ETAPA 5): o sinal que volta pra 02/08.
   - **`valence`/`intensity`** + `valence_open`/`valence_close` (por conceito e por hook) — a zona emocional declarada; é o que permite diagnosticar iteração que trocou de zona sem perceber (ETAPA 4, `iteration_zone_check`).
   **Fallback legado (batch anterior a esse schema — campos ausentes):** leia como sempre — comparação por execução (semântica sniper), sem zona declarada (`unknown`) e sem sub-avatar (`null`). Nada trava; os diagnósticos que dependem desses campos saem marcados como sem dado, nunca inventados.
4f. Leia `workspace/[produto]/10-ad-strategy/dados.json → test_capacity` — os dois campos que dizem SE a leitura nasceu apertada:
   - **`binding_constraint`** (`max_adsets|floor|adset_cap_5|batch_size|margin_warning|none`) — qual restrição limitou o teste (a que apertou primeiro). Quando ≠ `none`, cite no relatório: leitura de teste que nasceu apertado carrega esse contexto.
   - **`below_floor_directional_only`** — se `true`, aplica o PLAYBOOK item 6: resultado DIRECIONAL, dito ao membro com todas as letras — sem `ad_class` formal, sem kill, sem escala; recomendação = subir budget até o piso ou reduzir conceitos. Vale pra ETAPA 3 (classificação), ETAPA 9 (scaling) e pro `recommended_action`.
   **Fallback legado (`test_capacity` ausente):** o do PLAYBOOK item 6 — comportamento normal, com o check manual de `test_budget_daily` contra o piso de US$ 100/dia.
4g. **Ad log (cânone `.claude/lib/ad-log/README.md`) — SEMPRE, no início da análise.** Leia `workspace/[produto]/ad-log.md` (registro append-only de toda MUDANÇA executada na conta: budget, pausas, religadas, criações, LP trocada, automações) e cruze a janela de leitura desta análise com as mudanças do período — "a queda de quinta coincide com o quê?". Os dois achados que SÓ este log revela entram no diagnóstico (ETAPA 2 e ETAPA 7): **mudança sem o efeito esperado** (ex: budget subiu e o resultado não acompanhou) e **efeito sem mudança conhecida** (degrau de performance sem nenhuma linha no log — aí sim vale investigar fadiga/conta/mercado). Se o membro relatar durante a análise uma mudança manual que não está no log ("desliguei o ad X ontem"), registre a linha na hora com executor `membro` (criando o arquivo com o cabeçalho da tabela se não existir — regra do cânone). **Fallback legado (arquivo não existe e nenhuma mudança relatada):** siga sem ele — produto anterior ao cânone; não é `data_gap` bloqueante, mas o diagnóstico de coincidência temporal sai limitado e o relatório diz isso em uma linha.
4h. Leia `workspace/[produto]/16-creator-engine/dados.json → performance_by_creator` **(se existir — leitura aditiva, nunca pré-requisito):** com o bloco na mão + o sufixo de creator/editor no ad name (convenção 08/16 — o nome do ad carrega o nome do creator), a ETAPA 3 pode AGRUPAR a leitura também **por creator** ("ad name contains"), além de por conceito e por criativo: hit rate e soft metrics por creator alimentam a devolutiva da 16 e o creator report da 14. Sem o arquivo (ou sem sufixo no ad name), nada muda — a análise segue por conceito/criativo como sempre.
5. **Unidade de análise (dois níveis):** a estrutura padrão da Skill 10 é **1 campanha com CBO → N ad sets broad/Advantage+, 1 ad set = 1 conceito → 3 ads (criativos) cada**. A leitura acontece nos dois níveis: **entre AD SETS** (qual CONCEITO o CBO escolheu financiar — a distribuição de spend entre ad sets é o sinal de escala) e **entre ADS dentro de cada ad set** — e o que ESSA comparação responde depende do `testing_method` do conceito (item 4e): num Sniper, qual EXECUÇÃO do conceito puxou; num Marksman, qual ÂNGULO (bifurcação na ETAPA 3). O `concept_id` está no nome do ad set e do ad (naming convention da Skill 10) e o `utm_content=[concept-id]-[creative-n]` fecha o cruzamento com a loja. A classificação em `ad_class` continua sendo por AD; o nível de ad set responde "qual conceito funcionou". Leitura por CAMPANHA só se aplica depois que a Skill 12 criou campanhas ABO paralelas (pós-escala) ou se o membro montou estrutura custom por fora.
6. **Puxe os SISTEMAS NOMEADOS da base — NÃO use query genérica.** Rode `search_knowledge` com a `best_query` exata de cada framework relevante pra ETAPA que está executando (cada ETAPA abaixo já lista os seus). O índice completo do domínio desta skill (meta-ads-strategy — **o tamanho do domínio é o que o `frameworks.json` disser hoje, nunca um número decorado neste texto**) está em **`.claude/lib/kb-index/`** (`frameworks.json` + `README.md`, mapa skill→domínio no README). Os sistemas de maior impacto pra leitura de performance, com a query a rodar:
   - **4Pi Analysis (Spend, Frequency, CPM, Cost per Result)** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) — o motor da ETAPA 2
   - **4Pi+2 Dashboard & Custom Metrics** (rode `4Pi+2 custom metrics dashboard GPT account centers Ads Manager`) — setup das colunas customizadas
   - **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`) — as signatures de freq TOF/MOF/BOF do Pi 2
   - **Why New Ads Steal From Old Ads / Creative Hamster Wheel** (rode `why new ads steal from old ads creative hamster wheel deprioritized`) — fadiga e canibalização
   - **Profitable Scaling Margin (PSM) — Golden Ratio of Growth** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — o `psm_real` gravado pra skill 12
   - **Performance Gate Scaling (PGS)** existe na base, mas **NÃO se aplica a esta estrutura** — Automated Rule com condição de performance é recusada pelo Meta em campanha com CBO (cânone `.claude/lib/ad-taxonomy/README.md` §6). Não puxe esse sistema pra prometer escala automática; o ritmo de escala é o **Scaling Protocol** manual do §5, executado pela Skill 12
   - **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`) — por que ads ruins geram gasto
   - **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) — leitura do Pi 1
   - **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`) — interpretação do `dataset_health.match_quality_score`
   - **Taxonomia de Winners (Loser / KPI Winner / Spend Winner / Breakthrough)** (rode `breakthrough spend winner KPI winner losing ad classificação destino por categoria`) — o sistema nomeado por trás do cânone `ad-taxonomy` §2; carrega a lógica de por que KPI winner conta como loser na decisão
   - **Would It Hold at 3X Budget? (Mental Model)** (rode `would it hold at 3X budget mental model low spend high ROAS statistically insignificant`) — o teste mental que impede chamar de breakthrough um criativo com pouco spend e ROAS alto (é a mesma lógica que o cânone formaliza no `kpi_winner`)

   Cada framework que existir na base, aplique. A leitura por 4Pi/PSM é o RACIOCÍNIO; a CLASSIFICAÇÃO segue o cânone `.claude/lib/ad-taxonomy/README.md` §2 e a DECISÃO de matar segue as réguas do §3 (PLAYBOOK no topo desta skill: kill de ad set após 7 dias sem spend e sem KPI em conta madura; 8× target CPA sem purchase em conta nova; 24-48h de carência pra ad novo; CPM = saúde da conta; benchmarks de funil separam criativo de página).

7. **Contrato de cobertura da base (REGRA — `.claude/lib/kb-index/README.md`).** A puxada não é uma amostra, é cobertura do tópico:
   1. **Abra a seção inteira do domínio, sempre.** No início de cada ETAPA que consulta a base, abra `frameworks.json` e **enumere TODAS as entradas de `meta-ads-strategy` cujo `use_in_skill` inclui a 11** — e some as entradas de OUTROS domínios marcadas `11 (ad-analysis)` no `use_in_skill` (hoje existem em `scaling`, `creatives-hooks-formats`, `market-research-voc`, `competitor-positioning`, `copy-proof-persuasion-structure`, `page-landing-cro`, `persuasion-psychology`, `finance-projections` e `team-hiring-ops` — enumere pelo campo, não por esta lista). A contagem de cada domínio é a que o `frameworks.json` mostrar na hora.
   2. **Rode a `best_query` exata de cada entrada relevante à etapa, com `deep=true`.** As queries embutidas nas ETAPAs desta skill são o **núcleo mínimo garantido de cada etapa, nunca o teto**: entrada relevante que não está embutida É PARA SER PUXADA do mesmo jeito.
   3. **Critério de relevância é por ETAPA, não por preguiça:** a pergunta é "esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa. Só se descarta o que claramente pertence a outra etapa desta skill (e será puxado lá).
   4. **Não repita busca de framework já puxado na mesma sessão** — entradas duplicadas entre domínios apontam pro MESMO conteúdo; reuse o resultado.
   5. **Check de encerramento de etapa:** antes de fechar cada ETAPA, releia a lista enumerada do passo 1 e confirme que nenhuma entrada relevante ficou sem puxar. Se ficou, puxe agora — é este check que garante o padrão "sem deixar passar nada importante da base".

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md`, mapa skill→domínio no README). NUNCA use query genérica — sempre puxe o sistema nomeado pela `best_query`.

## Fluxo da Skill

### ETAPA 0.5 — TrendTrack MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use como camada de comparação contextual:

- **`mcp__trendtrack__scan_ad`** nos **breakthroughs** do membro (após classificar — nunca em `kpi_winner`, que não provou nada) → decomposição com lente de mercado: hook archetype, ângulo, reach estimado, scaling assessment. Compara com benchmarks da vertical pra confirmar se o breakthrough é mediocre ou top-tier do mercado.
- **`mcp__trendtrack__daily_radar`** se concorrentes já foram trackados na skill 03 → reporta movimentos recentes (novos ads dos competitors, mudanças de posicionamento). Adiciona contexto pro `NEXT_BATCH_IDEAS.md` final.

Use 1-3 chamadas por análise. Não desperdiçar créditos em criativo perdedor.

Se TrendTrack NÃO estiver disponível, siga ETAPA 1 normalmente.

### ETAPA 0.6 — Foreplay MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__foreplay__` disponíveis (ad spy — 200M+ ads; mesmo padrão de detecção das skills 03/08). Se SIM, use como camada de benchmark dos **breakthroughs**: depois de classificar o batch (4Pi + Decision Thresholds), compare hooks e formatos deles com os ads ESCALADOS do nicho (busca por marca/vertical) — análogo ao `scan_ad` do TrendTrack acima. O sinal alimenta duas coisas: (a) confirmar se o breakthrough é top-tier do mercado ou apenas o melhor de um batch fraco, (b) apontar formatos/hooks ativos no nicho que o batch ainda não explorou (vai pro `NEXT_BATCH_IDEAS.md`). Limite: 1-2 chamadas por análise — benchmark de breakthrough, nunca em `kpi_winner` nem em criativo perdedor.

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
- **Opportunity Score — usar como higiene, NUNCA como comando.** O score (0-100) mede aderência às best practices da Meta, não performance. Use os itens de checklist que ele expõe (audience overlap, sinal de conversão, variedade de criativo) como sinal secundário que "reforça vs contradiz" o 4Pi. **NUNCA aplique recomendações em lote pra "subir o score"** — em particular, IGNORE recomendação de mover o budget pros ad sets (desligar o CBO) ou de consolidar os conceitos num ad set só: o CBO no nível da campanha com **1 ad set por conceito** é decisão deliberada da Skill 10 (ETAPA 3.3), e é exatamente ele que produz o sinal de escala que esta skill lê. Score alto = alinhamento com o playbook da Meta, não ROAS.

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
- **COGS canônico = somatório de TODOS os campos de `offer.cogs_breakdown`** (NÃO existe campo `cogs_total`). Itere sobre as chaves do objeto — **nunca some uma lista fixa de campos**. O bloco tem hoje 8 itens (`product_delivered`, `shipping_to_customer`, `pick_pack`, `payment_processing`, `taxes_and_duties`, `subscription_app_fee`, `agency_fee_variable`, `refund_chargeback_provision`) e pode crescer; somar só os 5 antigos infla a margem e derruba o CPA/PSM pro lado otimista. **Todos os valores são dinheiro POR PEDIDO, nunca percentual** — se algum campo vier como percentual, é erro de gravação da 04: marque `data_gap` e não converta por conta própria. **Ad spend nunca está aqui** (ele é o CAC do PSM); somá-lo contaria o mesmo dinheiro duas vezes.
- **Fallback** se campos não existirem (oferta antiga): `breakeven_cpa = AOV / breakeven_roas` (mesmo fallback da Skill 10); se nem esses campos existirem, usar default conservador e marcar `data_gap`.
- **`fair_share` = spend total do ad set ÷ N ads ativos** (a fatia que cada criativo receberia numa distribuição uniforme). É a régua de **entrega** (Pi 1: o algoritmo está ou não votando neste ad) — nunca use "% do spend total" fixo: com 10-12 criativos, 10% do total É o fair share, e um critério fixo condenaria até o ad perfeitamente distribuído. **`fair_share` não classifica mais ninguém como winner** — a classificação usa `spend_share_7d` e a comparação com o KPI da campanha (bloco abaixo).

**KPI da CAMPANHA (métrica de referência — é o que separa breakthrough de ilusão):**
- `campaign_cpa` = spend da campanha ÷ purchases da campanha, na janela de 7 dias
- `campaign_roas` = revenue da campanha ÷ spend da campanha, na janela de 7 dias
- `account_spend_7d` = spend total da conta em 7 dias. Na estrutura da Skill 10 (uma campanha por produto, com N ad sets sob o mesmo CBO), `account_spend_7d` é o spend dessa campanha; quando a Skill 12 já criou campanhas ABO paralelas, use o total da conta.
- `spend_share_7d` do ad = `ad_spend_7d ÷ account_spend_7d`
- `ad_kpi_vs_campaign` = `ad_cpa <= campaign_cpa` (ou `ad_roas >= campaign_roas` quando o AOV varia entre ads — regra de desempate igual à do bloco "Winner picking")
- Se não há purchases suficientes na campanha pra calcular `campaign_cpa` com estabilidade (learning phase, < ~50 conversões em 7 dias), a comparação é **preliminar**: marque `data_gap` e não classifique ninguém como breakthrough ainda.

> **Incremental Attribution (setting do Ads Manager, 2025+):** se o membro ligou esse setting em alguma campanha, o CPA reportado dela NÃO é comparável ao CPA clássico — o Meta passa a contar só conversões que julga ter causado (conversões reportadas caem, CPA observado sobe, e o setting trava as attribution settings). Nesse caso, re-baseline TODOS os thresholds desta análise antes de qualquer kill naquela campanha, e trate a leitura como ferramenta de alocação de budget, não de kill de criativo. No teste padrão da Skill 10, o baseline é 7d-click/1d-view — a régua de kill foi calibrada nele.

**PSM real (fórmula canônica — mesma base do `psm_theoretical` da skill 04):**
```
psm_real = LTV / (CAC_real + COGS)
```
- **`CAC_real` = ad spend do período ÷ clientes NOVOS do período.** Os clientes novos vêm do **Shopify** (`new customer = TRUE`), **não** do gerenciador de ads. O denominador é CAC, não CPA de plataforma (`.claude/lib/unit-economics/README.md` §3).
- `COGS` = somatório de TODOS os campos de `offer.cogs_breakdown` (regra acima).
- `LTV` = de `04-offer-builder/dados.json` (ou AOV do primeiro pedido se LTV ausente — recompra estimada não entra).
- Thresholds PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.
- **A skill 11 é a ÚNICA fonte que grava `manifest.psm_real`** (a partir de performance real). Também grava em `11-ad-analysis/dados.json`. Skill 12 LÊ `manifest.psm_real`; nunca recalcula.

> **Por que o denominador mudou (e por que isso importa):** a skill 04 grava `psm_theoretical` com **CAC** (base Shopify, `unit_economics.cac_basis: "shopify_new_customer"`), e a skill 12 compara `psm_real` contra `psm_theoretical` com tolerância de 20% pra liberar escala. Enquanto esta skill usava o **CPA de plataforma** — que conta conversões atribuídas pelo Meta, incluindo cliente recorrente, e por isso é sempre MENOR que o CAC real numa loja com recompra — o `psm_real` saía **otimista** e podia liberar escala indevida. Os dois números só são comparáveis na mesma base.

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
- **Funil quebrado antes de matar:** se houve checkouts mas as taxas de funil estão abaixo de ATC→compra 20-25% / checkout→compra 40-50% (com a amostra mínima da ETAPA 6B), o bloqueio é página/oferta, não o criativo → NÃO matar o criativo; rotear pra 06/07/04.
- **Conta antes de produto:** CPM muito acima do nicho → suspeitar da CONTA primeiro; testar o mesmo criativo em outra conta antes de matar o produto.
- **Não existe régua "1-2× breakeven CPA sem venda".** A 1× CPA há ≈ 37% de chance de zero vendas por puro acaso (≈ 14% em 2×) — matar ali descarta criativo bom por ruído.

**Classificação — as 4 classes (cânone `.claude/lib/ad-taxonomy/README.md` §2; vale pra ETAPA 3, 5, 9, 11 e pro handoff das skills 12 e 14):**

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
| **`breakthrough`** | KPI do AD melhor que o KPI da CAMPANHA **e** puxa spend | **Escala (skill 12) + reciclagem (skill 14)** — o único que libera as duas |
| **`spend_winner`** | Puxa spend mas KPI abaixo do da campanha | Iterar (skill 08), **não escalar** |
| **`kpi_winner`** | Bate o KPI mas **não puxa spend** | **Tratar como loser para decisão** — não escala, não recicla, não vira learning replicável |
| **`loser`** | ≤ 2% do spend da conta em 7 dias ("não fez nada pela conta") | Graveyard / limpeza pela régua de kill do ad set |

> **O falso positivo que essa skill produzia:** a definição anterior (`CPA ≤ target` + `spend ≥ 50% do fair_share`) classificava como "winner" exatamente o que o cânone chama de **KPI winner** — ad que bate um alvo estático numa amostra pequena. Isso se propagava pra skill 12 (escala prematura) e pra skill 14 (reciclagem de criativo que nunca provou nada). O que separa breakthrough de ilusão é a comparação com **o KPI da própria campanha**, não com um alvo fixo, somada à prova de que o ad **puxa spend**.

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
- **Volume de conversões baixo** (poucas purchases, CPA instável dia-a-dia): CPA é ruído; use Spend + Freq + CPM apenas. CPA column = "insufficient data". O gate clássico da learning phase **continua valendo em 2026**: ~50 eventos de conversão em 7 dias por ad set pra sair de learning — abaixo disso, o CPA balança e a leitura é preliminar. O que mudou (desde abril/2026) é outra coisa: edições antes consideradas "seguras" (ajuste pequeno de bid, tweak de criativo) passaram a **resetar o learning com mais facilidade** — mais um motivo pro "não mexe por 3 dias" da Skill 10.
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

#### Pi 1: SPEND

> Fundamento: **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) + **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`). Explicam por que o algoritmo concentra ou força spend e por que NÃO se desliga o top spender mesmo quando parece ineficiente.

"Quanto cada CONCEITO (ad set) puxou do budget da campanha, e quanto cada AD (criativo) puxou dentro do ad set dele?"

Observação-chave: **Meta distribui spend pra onde ele ACREDITA que está funcionando** — e sob CBO isso acontece em dois níveis. Primeiro o CBO reparte entre os ad sets: **o ad set que concentra gasto é o conceito que o algoritmo escolheu**, e essa é a leitura mais informativa do batch. Depois, dentro de cada ad set, o Meta reparte entre os 3 ads do pack; ali o `fair_share` de cada criativo é 1/N do spend daquele ad set (com o pack 3-2-2, 1/3). Se o ad A recebeu 3× o fair share e o ad B só 20% dele, o algoritmo tá "votando" que A é melhor (independente de CPA).

- **Ad com spend ≥ 2× o fair share** → Meta tá confiante nele. É **candidato** a `breakthrough` ou a `spend_winner` — quem decide qual é a comparação com o KPI da campanha no Pi 4, não este Pi.
- **Ad com spend < 50% do fair share após 72h** (com a entrega geral saudável) → Meta não tá confiante nele OU o ad não foi aprovado. Sozinho isso **não** classifica ninguém: se o ad bate o KPI da campanha, ele é `kpi_winner` (loser para decisão, mas o diagnóstico é "audiência pequena demais", não "criativo ruim"); se não bate e o `spend_share_7d` fica em ≤ 2%, é `loser`.
- **Registre `spend_share_7d` de cada ad aqui** (spend do ad ÷ spend da conta na janela de 7 dias). É esse número, e não o `fair_share`, que entra na classificação do bloco Decision Thresholds.

Se NENHUM ad gastou em 24-48h (entrega geral travada): verificar Ads Manager > Delivery insights + Review status — pode ser policy/review/conta, NÃO criativo. Pós-escala (Skill 12 criou múltiplas campanhas/ad sets), a mesma leitura de share se aplica um nível acima: campanha/ad set com spend muito abaixo do esperado = algoritmo sem confiança nela.

#### Pi 2: FREQUENCY (Sinaliza Posição no Funil)

> Fundamento das signatures: **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`). É de lá que vêm as bandas de freq diária ↔ posição no funil (TOF/MOF/BOF) e a leitura de sprinters vs marathoners.

**Regra base: a frequency lida aqui deve ser a frequency DIÁRIA** (freq do dia, não acumulada da vida toda do ad set). Frequency lifetime cresce indefinidamente e não diz nada sobre fadiga atual. Sempre puxe/compare a freq diária. As bandas abaixo são para freq DIÁRIA.

Aplicar as signatures (freq diária, lida POR AD):

- **Freq ~1.05** → **prospecting / TOF** (Top of Funnel) — novas impressões, cold traffic, ~1 impressão por pessoa/dia
- **Freq 1.1-1.4** → **MOF** (Middle) — starting to warm up
- **Freq 1.5-1.9** → **retargeting / BOF** (Bottom) — mesmas pessoas vendo várias vezes ao dia

Se os ads da campanha de teste (que é 100% prospecting broad) estão com freq diária bem acima de ~1.05 (puxando pra 1.5-1.9, comportamento de retargeting), o Meta está re-martelando a mesma audiência em vez de abrir TOF novo — sinal de saturação da entrega. Recomendação: adicionar conceito TOF-friendly (hook problem, angle curiosity) no próximo batch.

**Freq ~1.05 estável NÃO é anomalia aqui:** na estrutura broad da Skill 10, ~1.05 sustentada é o estado normal e desejado de uma campanha 100% prospecting — não dispare alerta por isso. O alerta de "Meta não consegue re-engajar" só se aplica quando existe camada de retargeting esperada (que o fluxo padrão não monta). O check que continua valendo em qualquer cenário: **CPM baixo + CTR muito baixo = criativo não ressoa** com a audiência.

#### Pi 3: CPM (Contexto Combinado com Freq)

**CPM isolado diz pouco. CPM + Freq diz muito:**

- **CPM alto (acima da média do nicho) + Freq diária alta (>1.5)** → Meta tá mandando pra audience cara (prime-time, premium placements) porque POUCA audience nova está disponível. Sinal de BOF / possível fadiga.
- **CPM alto + Freq diária baixa (~1.05)** → audience premium/cara mas fresca. Pode ser normal em nicho competitivo (skincare, finance, luxury).
- **CPM baixo + Freq alta** → Meta tá procurando impressões baratas com audience repetida. Frequência tá alta mas CPM não subiu = Meta não tá pagando caro pra forçar. Pode ser fadiga mas também pode ser só stabilidade.
- **CPM subindo no tempo** (comparar com análises anteriores se houver) → **possível fadiga**. Combinar com CTR falling pra confirmar.

**CPM também é sinal de saúde da CONTA (lente do playbook):** o mesmo produto/criativo pode dar CPM $30 numa conta e $100 noutra — o CPM diz tanto sobre a conta quanto sobre o criativo. Se o CPM está muito acima do esperado do nicho de forma generalizada (TODOS os ads caros, não só um criativo), suspeite da CONTA antes do produto. Antes de declarar o produto morto por economia ruim, marque `health_signals.account_cpm_suspect = true` e recomende **testar o mesmo criativo em outra conta de anúncio** (resiliência legítima: ter conta reserva ajuda aqui). Só mata o PRODUTO se ele não validar em conta nenhuma.

#### Pi 4: COST PER RESULT (O Que Realmente Importa)

A comparação que classifica é **CPA do AD vs. `campaign_cpa`** (ou ROAS do ad vs. `campaign_roas`), cruzada com `spend_share_7d` — as 4 classes do bloco **Decision Thresholds** no topo desta ETAPA. O `target` CPA da oferta (do `04-offer-builder/offer-builder.md`) continua sendo lido, mas como piso de rentabilidade e como base da régua de kill de conta nova, **não** como definição de winner:

- **KPI do ad melhor que o da campanha + puxa spend** → **`breakthrough`** (o único que vai pro diagnóstico "scale")
- **Puxa spend + KPI abaixo do da campanha** → **`spend_winner`** (iterar, não escalar)
- **KPI melhor que o da campanha + `spend_share_7d` < 10%** → **`kpi_winner`** (loser para decisão; ver o escape abaixo antes de descartar)
- **`spend_share_7d` ≤ 2% em 7 dias** → **`loser`** (gastou sem bater KPI mas puxando spend? é `spend_winner` acima, nunca loser — cânone §2)

**Escape antes de descartar um `kpi_winner`:** o ad pode ser ótimo pra uma audiência pequena demais. Antes de tratá-lo como peso morto, dá pra **forçar spend** — ad set próprio começando no que ele já gastava — para tirar a dúvida em ambiente controlado. Isso é decisão de estrutura, então a recomendação sai daqui e a execução é da skill 12. O que **não** pode acontecer é ele entrar em `breakthroughs[]` sem ter provado que sustenta spend.

**Réguas de KILL (cânone §3, decisão operacional):**
- **Conta madura:** kill no nível do **ad set** após 7 dias sem spend e sem KPI. Marque `reason = "adset_7d_no_spend_no_kpi"`.
- **Conta nova:** ad que gastou **≥ 8× o `target` CPA sem purchase** → kill. Marque `ad_class = "loser"` com `reason = "kill_8x_target_cpa_no_purchase"`.
- **Ad novo overspendando:** **24-48h** de carência antes de qualquer decisão. Marque `reason = "awaiting_24_48h_grace"` e não classifique ainda.
- **Exceção:** se o criativo tem **2+ initiate-checkouts** no comecinho, NÃO mate ainda — o Meta tem sinal pra otimizar; deixa rodar mais um pouco. Classifique como NEEDS OPTIMIZATION.
- **CTR alto sem venda não salva** o criativo — mas também não o mata sozinho. A régua é a de cima.
- **Funil quebrado (cruzar com benchmarks ANTES de matar):** se o criativo gerou ATC/checkouts mas as taxas estão abaixo de **ATC→compra 20-25%** ou **checkout→compra 40-50%**, o bloqueio é página/checkout/oferta, NÃO o criativo. Ex: 3 checkouts e 0 venda → checkout→compra = 0%, muito abaixo dos 40-50% esperados → o ad fez o trabalho, a página falhou. **NÃO mate o criativo**; roteie pra 06/07 (página) ou 04 (oferta) e registre o gargalo de funil no diagnóstico.
- **Conta antes do produto:** se o CPM está fora do esperado do nicho de forma generalizada (ver Pi 3, `account_cpm_suspect`), trate como problema de CONTA — recomende re-testar em outra conta antes de matar o produto.

Contexto importante: **CPA de um ad isolado não é tudo**. "a campanha overall melhorou?". Se a campanha total está dentro do CPA target mesmo com 1-2 ads fora, a máquina tá OK. Otimiza os outliers, não destrua a campanha.

**Breakdown por placement (check rápido quando o CPA agregado está fora do target):** puxe insights com breakdown por placement (o MCP oficial expõe; no Ads Manager: Breakdown > Placement). Placement de CPM baixo mas conversão fraca — Threads (placement global desde jan/2026, ligado por default no Advantage+) e Audience Network são os suspeitos usuais — pode estar comendo spend sem vender. Só considere opt-out via manual placements como **exceção documentada depois desse dado**; nunca preventivamente (a tese de deixar o Meta distribuir continua certa).

#### Hook rate e Hold rate (ONDE o criativo falhou)

Os 4Pi dizem **que** um criativo falhou. Hook e Hold dizem **onde**. Sem os dois, "o criativo não funcionou" não é diagnóstico — é constatação, e não gera briefing pra 08.

**Fórmulas** (cânone `.claude/lib/ad-taxonomy/README.md` §4):
```
Hook rate = 3-second video plays ÷ impressões
Hold rate = ThruPlays ÷ impressões
```
(ThruPlay = ≥ 15s, ou o vídeo inteiro se durar menos que isso.)

**Como obter:** no Ads Manager, Columns → Customize Columns → Create Custom Metric, uma coluna pra cada fórmula. Pelo MCP, os componentes (`impressions`, `video_3_sec_watched_actions`, `video_thruplay_watched_actions`) vêm no pull — calcule direto, não peça ao membro. Se o criativo é estático, os dois campos ficam `null` e o diagnóstico de abertura passa a ser CTR + tempo de leitura, não hook rate.

**Benchmarks:** as faixas de Hook (ok/bom/muito bom/excepcional) e Hold estão na tabela do cânone §4. Leia de lá; não replique a tabela aqui nem invente número intermediário.

**Leitura diagnóstica (é isto que vira briefing pra 08):**

| Padrão | O que significa | Ação |
|---|---|---|
| **Hook baixo** | Problema de **abertura** — os 3 primeiros segundos não fisgam. O resto do vídeo nem foi visto, então não há informação sobre ele. | Reescrever o hook e retestar **o mesmo conceito** (iteração de uma variável só). Não descarte o conceito. |
| **Hook bom + Hold baixo** | A abertura fisgou, mas **a promessa não sustentou** — o vídeo entregou menos do que o hook prometeu, ou demorou pra entregar. | O hook está resolvido; o trabalho é o corpo do vídeo (ritmo, prova, mecanismo). |
| **Hook e Hold bons + CPA ruim** | O criativo prende atenção mas não converte — o problema está depois do vídeo. | Vá pra ETAPA 6B (funil/página) e pro 19-Point antes de culpar o criativo. |

**Ressalva obrigatória:** hook rate, hold rate, CTR e CPC são **métricas macias** — um ad com o dobro do CPC pode ter o mesmo ROAS, e ninguém paga boleto com hook rate. O uso correto é **diagnóstico de onde o criativo falhou**, **nunca** critério de kill nem de classificação. As classes continuam vindo do bloco Decision Thresholds; kill continua vindo das réguas do cânone §3.

Grave `hook_rate` e `hold_rate` por criativo no `dados.json` e no perf JSON do DNA (é o que preenche os campos `thumbstop_3s` / `hold_15s`, que até agora eram gravados vazios).

#### PSM real (gravado nesta análise — usado pela skill 12)

Calcule `psm_real` pela fórmula canônica do bloco **Decision Thresholds**:
```
psm_real = LTV / (CAC_real + COGS)
```
- `CAC_real` = ad spend do período ÷ **clientes NOVOS** do período (Shopify, `new customer = TRUE`) — nunca o CPA de plataforma. Se a base for proxy, grave `psm_real_basis: "platform_cpa_proxy"` e trate o número como otimista.
- `COGS` = somatório de TODOS os campos de `offer.cogs_breakdown` (8 hoje; itere as chaves, não uma lista fixa — NÃO existe campo `cogs_total`)
- `LTV` = de `04-offer-builder/dados.json` (ou AOV do primeiro pedido se LTV ausente)

Este `psm_real` é gravado em `11-ad-analysis/dados.json` E em `manifest.psm_real`, junto com `psm_real_basis` (ver ETAPA de update do manifest). Skill 12 lê de `manifest.psm_real`, nunca recalcula — e compara contra o `psm_theoretical` da skill 04, que usa a MESMA base (CAC). Thresholds de ação PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.

#### Share de compras em 7-day click (gravado nesta análise — gate de escala da 12)

Calcule, na janela de 7 dias e no nível da campanha:
```
click_based_purchase_share = purchases atribuídas em 7-day click ÷ purchases totais da janela
```
- **Como obter:** o breakdown de atribuição vem no pull do MCP (comparação de attribution settings); no Ads Manager: Columns → Compare attribution settings (7-day click vs 1-day view). No caminho manual, peça o número ao membro junto com os demais dados.
- **Grave em `dados.json` e em `manifest.click_based_purchase_share`.** É o número que a Skill 12 confere no gate click-based do cânone `.claude/lib/ad-taxonomy/README.md` §5 (escala só com ≥ 60% das purchases em 7-day click, OU com o ROAS calculado só das purchases click-based batendo o KPI sozinho). **NUNCA estimar** (regra do manifest-schema): se o breakdown não veio, NÃO grave o campo — o gate da 12 fica bloqueado até o número existir, e o relatório diz exatamente onde olhar pra destravar.
- **Se a share vier baixa** (view-through inflando o resultado — disparo de email e cliente recorrente são os suspeitos usuais), o teste nomeado da base pra tirar a prova é o **Teste de troca pra 7DC-only** (rode `campanha duplicada 7-day click only view-through inflado email blast returning customers`): duplicar a campanha rodando só com atribuição 7-day click e medir quanto do resultado era inflação. A recomendação sai daqui; a execução é decisão de estrutura (Skill 12, com a 07c na camada de atribuição).

### ETAPA 3 — Diagnóstico Por Ad (criativo)

Pra CADA ad de CADA ad set, grave `ad_class` (as 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2, calculadas no bloco Decision Thresholds). Registre junto o `concept_id` do ad set a que ele pertence — é o que permite responder "qual CONCEITO funcionou", e não só "qual execução". Se o batch tem creator humano e a 16 rodou (Contexto 4h), agrupe a MESMA leitura também **por creator** (custom report "ad name contains" o nome do creator) — é esse agrupamento que devolve hit rate por creator pra 16 e pro creator report da 14.

**Gate de piso (antes de classificar qualquer ad):** se `test_capacity.below_floor_directional_only: true` na 10 (Contexto 4f; PLAYBOOK item 6), **não grave `ad_class` formal** — a análise inteira sai marcada como DIRECIONAL (`test_capacity_check.directional_only_analysis: true` no `dados.json`), sem kill e sem escala; a recomendação é subir budget até o piso ou reduzir conceitos, dita ao membro com todas as letras.

**Leitura por método de teste — o que a comparação entre os 3 ads do ad set responde (`testing_method` da 08, Contexto 4e):**

| Método do conceito | A comparação dentro do ad set responde | Como nomear o vencedor |
|---|---|---|
| **`sniper`** (ou campo ausente — batch legado) | **"qual EXECUÇÃO venceu"** — os 3 ads são 3 execuções do MESMO ângulo (varia hook/abertura/visual de entrada) | pelo elemento de execução que variou (hook A vs B vs C) |
| **`marksman`** | **"qual ÂNGULO venceu"** — os 3 ads carregam 3 ângulos DISTINTOS sobre um hold universal (cânone §7: Marksman acontece DENTRO do ad set, não entre ad sets) | pela **frase de `angles[]`** do criativo vencedor (match por `creative_n`), carregando o `sub_avatar_id` daquele item |

Três consequências da leitura Marksman:
- **Loser dentro de pack Marksman ≠ ângulo morto.** Cada ângulo recebeu UMA execução só — o trade-off declarado do cânone §7: a falha pode ter sido a execução, não o ângulo. Antes de enterrar um ângulo, puxe **The Execution Problem** (rode `execution problem angle certo palavras erradas 3 strikes por angle 12 razoes de falha`): o mesmo ângulo ganha **3 tentativas (3 strikes)** contra as 12 razões de falha de execução antes de ser descartado. A diretiva de re-teste vai pro `NEXT_BATCH_IDEAS.md`.
- **Hold baixo nos 3 ads do pack = o `hold_universal` é o suspeito**, não qualquer ângulo individual (o hold é compartilhado por construção — se os 3 seguram mal, o problema é o corpo comum). E se o pack saiu com `hold_universal_validated: false` (não deveria — o gate da 08 bloqueia), a leitura de ângulo está contaminada ("meio Sniper, meio Marksman não ensina nada"): trate como teste inválido de método, não como veredito sobre os ângulos.
- **Vencedor de Marksman → a próxima entrada é Sniper.** Sequência oficial do cânone §7 (Marksman acha a direção → Sniper extrai o máximo do ângulo vencedor); a diretiva de iteração no `NEXT_BATCH_IDEAS.md` nasce já como `sniper` sobre o ângulo nomeado.

**`breakthrough`:** KPI do ad melhor que o KPI da campanha **E** puxa spend (`spend_share_7d` ≥ 30% em conta pequena; 5-10% em conta grande).
→ Ação: manter rodando. **Não há escala automática pra acionar** — Automated Rule de performance é recusada em CBO (cânone §6); a escala é decisão da ETAPA 9 e execução da Skill 12, pelo Scaling Protocol manual do §5. É o **único** `ad_class` que entra em `breakthroughs[]` e libera skill 12 (escala) e skill 14 (reciclagem).

**`spend_winner`:** puxa spend (`spend_share_7d` ≥ 10%) mas com KPI abaixo do da campanha.
→ Ação: **iterar, não escalar**. Ele segura a conta onde está; escalar um spend winner é subir budget num criativo que já está diluindo o KPI médio. Vai pro `NEXT_BATCH_IDEAS.md` como iteração de uma variável (ETAPA 5).

**`kpi_winner`:** bate o KPI da campanha mas **não puxa spend** (`spend_share_7d` < 10%).
→ Ação: **tratado como loser para decisão** — não escala, não recicla, não vira learning replicável. O KPI bonito veio de amostra pequena e não provou nada. A hipótese mais comum é audiência pequena demais; o escape (forçar spend em ad set próprio pra tirar a dúvida) é recomendação pra skill 12, e só depois de sustentar spend ele pode ser reclassificado. **Nunca** o coloque em `breakthroughs[]` "porque bateu o alvo".

**IN FATIGUE:** CPM subindo + CTR caindo + Freq subindo ao longo dos dias (comparar com análises anteriores).
> Antes de classificar fadiga, puxe **Why New Ads Steal From Old Ads / Creative Hamster Wheel** (rode `why new ads steal from old ads creative hamster wheel deprioritized`) — explica quando o sinal de "fadiga" é na verdade um ad novo canibalizando o spend do antigo (deprioritization), e não fadiga real da audience. Muda a ação: nesse caso o fix é consolidar, não refresh.
> **Calibração 2026 (pós-Andromeda/GEM):** a vida útil típica de criativo encolheu pra **2-4 semanas** (estático fatiga mais rápido; o pico de performance costuma ser a 1ª semana). Planeje refresh nessa janela — não em ciclos de 6-8 semanas.
→ Ação: trocar os 1-2 criativos mais fatigados do ad set por conceitos novos (Skill 08) OU pedir batch novo completo. **Não pausar ainda** — pode ainda estar performando acima do breakeven mesmo com sinais de fadiga.

**`loser`** (def. canônica do bloco Decision Thresholds): `spend_share_7d` ≤ 2% em 7 dias ("não fez nada pela conta" — cânone §2; gastar sem bater KPI não é loser: puxando spend, é `spend_winner`, que itera). Some a isso as réguas de kill do cânone §3 — conta madura: ad set após 7 dias sem spend e sem KPI; conta nova: ad com ≥ 8× o target CPA sem purchase; ad novo overspendando: 24-48h de carência antes de decidir.
→ Ação: PAUSAR pela régua do contexto da conta (ad set em conta madura, ad em conta nova). Fazer diagnóstico profundo (Etapa 4) pra entender por que falhou.

**FUNIL QUEBRADO (não é o criativo):** o criativo trouxe ATC/checkouts mas as taxas estão abaixo dos benchmarks (ATC→compra < 20-25% ou checkout→compra < 40-50%).
→ Ação: **NÃO pausar o criativo** — o ad fez o trabalho, o gargalo é página/checkout/oferta. Rotear pra 06/07 (página) ou 04 (oferta). Registrar o gargalo de funil no `health_signals` e no NEXT_BATCH_IDEAS.

**CONTA SUSPEITA (não é o produto):** CPM generalizado muito acima do nicho (`account_cpm_suspect`).
→ Ação: re-testar o mesmo criativo/produto em OUTRA conta de anúncio antes de matar o produto. Só mata o produto se não validar em conta nenhuma.

**EM APRENDIZADO:** < 7 dias rodando (ou < 24-48h, no caso de ad novo que está overspendando), ou a campanha ainda sem `campaign_cpa` estável.
→ Ação: aguardar antes de classificar — não grave `ad_class` ainda. Dê ao Meta tempo de estabilizar a entrega e o CPA antes de julgar — a learning phase clássica (~50 eventos de conversão/7 dias por ad set) continua valendo em 2026, e abaixo desse volume o CPA balança. Não mexer no ad set enquanto isso (edições resetam o learning com mais facilidade desde abril/2026).

**CHECKPOINT de KILL de PRODUTO (cadência quarta→domingo — a leitura vive AQUI, não na 10):** o teste de produto lança quarta e tem teto de 7 dias por rodada (cadência montada pela Skill 10). **Domingo é CHECKPOINT de decisão informada, não sentença** — a data abre a leitura; quem decreta qualquer óbito é a leitura (esta skill + as réguas do cânone), nunca o calendário. Ordem de precedência OBRIGATÓRIA no checkpoint:
0. **Teste abaixo do piso?** (`below_floor_directional_only: true` — Contexto 4f) — resultado direcional NÃO decreta morte de produto: a janela não teve leitura válida. Recomende subir budget até o piso (ou reduzir conceitos) e re-rodar a janela antes de qualquer veredito.
1. **Funil quebrado?** (ETAPA 6B) — se os ads trouxeram checkouts que a página desperdiçou, o problema é página/oferta; conserta antes de matar o produto.
2. **Conta suspeita?** (Pi 3, `account_cpm_suspect`) — CPM generalizado fora do nicho pede re-teste em OUTRA conta antes de matar o produto.
3. **Entrega travada?** — ads presos em review/policy não testaram nada; resolver e re-rodar a janela.
Se os 4 checks passam e não houve venda até domingo → o default é **processar os learnings e iterar**, não matar o produto. Batch sem venda reprova, na maioria dos casos, a EXECUÇÃO testada, não o ângulo (Execution Problem, ETAPA 3): ângulo com strikes restantes itera em **Sniper** no próximo batch, com a diretiva gravada no `NEXT_BATCH_IDEAS.md`. O que morre já no checkpoint morre por régua, não por clemência: ad set que cruzou o cânone §3 (conta madura: 7 dias sem spend e sem KPI · conta nova: 8× target CPA sem purchase) é decretado normalmente.

**Matar o PRODUTO é decisão de outro nível:** só entra na mesa com **≥ 2 batches com learnings processados** (esta skill extraiu o que cada batch ensinou e o batch seguinte aplicou a correção) **OU quando as réguas do cânone §3 mandarem — nunca por calendário sozinho.** A intenção original do marco de domingo permanece inteira: impedir o membro de queimar caixa por semanas num produto morto. O que muda é o mecanismo — quem declara o óbito é a leitura (esta skill + cânone), não a data.

### ETAPA 4 — Diagnóstico Profundo de LOSERS (19-Point Diagnostic)

Roda pra todo criativo com `ad_class` = `loser`. Roda **também** pra `kpi_winner` (que é loser para decisão) e pra `spend_winner` — nos dois casos a pergunta muda: no `kpi_winner`, por que ele não puxou spend (hipótese primária: audiência pequena demais); no `spend_winner`, por que o KPI ficou abaixo do da campanha apesar do volume.

### 19-Point Loser Diagnostic

**Camada 1: Targeting (4 pontos) — só se aplica a estruturas CUSTOM.** A estrutura padrão da 10 é broad/Advantage+ sem exclusões e sem lookalike — nela, pule direto pra Camada 2. Use esta camada só se o membro montou targeting manual por fora do fluxo.
1. Audience muito broad — CTR alto, CVR baixo
2. Audience muito narrow — CPM alto, volume baixo
3. Exclusões conflitantes (ex: excluir compradores mas campaign é de aquisição — conflito)
4. Lookalike source com baixa qualidade (seed < 500 de alta qualidade)

**Camada 2: Hook (4 pontos)** — entre nesta camada **com os números de Hook e Hold já medidos** (bloco da ETAPA 2). Hook baixo confirma que a falha é aqui; hook bom com hold baixo joga o diagnóstico pra Camada 3 (a promessa do hook não foi sustentada pelo corpo). Pra loser que **gastou sem vender**, a ordem do diagnóstico é sistema nomeado da base: **Diagnóstico de Spend Sem Venda** (rode `spend sem venda hook traz gente errada beliefs gradualization average watch time`) — primeiro cheque se o hook está trazendo a **pessoa errada** (spend e clique com zero intenção), só depois a camada de crenças/gradualization; o **average watch time** é o sinal que separa os dois casos.
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

### Diagnóstico de valência — iteração que trocou de zona (`iteration_zone_check`)

Roda pra **toda iteração que fracassou** (criativo cujo conceito nasceu de `NEXT_BATCH_IDEAS.md` ou é iteração declarada — `testing_method: "sniper"` de batch derivado). **Quem é o original:** leia `concepts[].iteration_of` da 08 (creative_id do original — a linhagem declarada); só quando o campo não existe (batch legado), paree original↔iteração pela prosa do briefing, como sempre. Compare, em `08-creative-engine/dados.json`, a zona emocional do ORIGINAL vs a da ITERAÇÃO — `valence` × `intensity` de abertura (do conceito e do hook) e o arco `valence_open` → `valence_close`:

- **Zona igual, elemento iterado diferente** → a variável testada explica o resultado; o diagnóstico segue nas camadas do 19-point.
- **Zona MUDOU** (ex: a iteração abre em negative/high onde o original abria em positive/low) → a iteração **trocou de zona emocional sem perceber** — o flop inexplicável que a 08 (ETAPA 4.5.E) documenta: trocou a palavra, trocou junto o sentimento, e o ad deixou de falar com o mesmo estado emocional. A causa provável do fracasso é a ZONA, não o elemento editado; a diretiva pro próximo batch é refazer a iteração **na zona original**, mudando só a variável pretendida.

Registre em `iteration_zone_check[]` no `dados.json` (um item por iteração analisada): referência do original e da iteração, as duas zonas, `zone_changed` e o veredito. **Fallback legado:** original ou iteração sem `valence`/`intensity` gravados (batch anterior ao schema da 08) → registre `"unknown"` no lado sem dado e **não conclua troca de zona** — o item sai com `verdict: "no_data"`.

### ETAPA 5 — Diagnóstico de BREAKTHROUGHS (Extração de Learnings)

Extraia learnings replicáveis **só dos `breakthrough`**. Um `kpi_winner` não gera learning confiável: o resultado bonito veio de amostra pequena, e transformar isso em hipótese pro próximo batch propaga o falso positivo pra dentro da skill 08. Um `spend_winner` gera um learning de outra natureza — o que fez o Meta apostar nele (útil pra hook e formato), somado à hipótese do que derrubou o KPI.

Pra cada breakthrough, extraia learnings aplicando o framework:

- **O que funcionou?** (hook específico, ângulo, formato, CTA, LP)
- **Por que funcionou?** (hipótese causal — ex: "hook de curiosity pattern interrupt em audience Problem Aware onde concorrentes usam authority-first")
- **QUAL variável explica?** — nomeie a hipótese usando o mapa "As Variáveis de um Ad" da Skill 08 (persona/micro-persona, avatar, formato, conceito/big idea, tema, ângulo, benefício vs consequência, senso estético, estrutura invisível). "O criativo ganhou" não é learning; "a MICRO-PERSONA da mãe insone ganhou do avatar genérico, com o mesmo conceito" é. Compare o breakthrough com os losers do MESMO batch: em quais variáveis eles diferem? A variável que separa breakthrough de loser é a candidata a causa.
- **Como replicar?** (quais elementos isolar pra usar em próximos batches — ex: "o hook 'POV: você acorda com X' pode ser template pra outros conceitos")
- **Como iterar o breakthrough:** a iteração de maior alavancagem mantém TUDO que ele provou e muda **UMA variável por vez** (ex: mesmo conceito/estrutura pra outra persona; mesmo criativo com outro avatar; mesma estrutura com o par benefício→consequência invertido). Duas variáveis mudadas ao mesmo tempo = aprendizado zero sobre o porquê. Registre a variável escolhida no NEXT_BATCH_IDEAS.md.
- **Onde ele ganhou dentro do vídeo:** compare o Hook e o Hold do breakthrough com os dos losers do mesmo batch. Se ele ganhou no hook, o ativo replicável é a abertura; se ganhou no hold, é a estrutura do corpo. Isso decide o que a 08 deve preservar na iteração.
- **QUAL sub-avatar produziu o vencedor (fecha o loop com a pesquisa):** leia o `sub_avatar_id` do conceito do breakthrough (num pack `marksman`, o do item de `angles[]` do criativo vencedor) e grave **`winning_sub_avatar_id`** no item correspondente de `breakthroughs[]` do `dados.json`. É o sinal que volta pra 02/08: a 02 é a produtora de `sub_avatars[]` e a 08 monta conceito por referência a esse `id` — saber qual RECORTE DE AVATAR venceu vale mais que saber qual arquivo de vídeo venceu. **Fallback legado:** conceito sem `sub_avatar_id` (batch anterior ao schema da 08) → grave `null` e nomeie a persona pelo texto do briefing da 08.
- **O learning é sobre o CLIENTE, não sobre a estrutura do ad.** Puxe **Winning Ad Extraction / Processing Learnings** (rode `winning ads extracting strategies process learnings AdSpy shares validated hook why it works`): pergunte "why does this matter?" repetidamente até o learning virar ESTRATÉGIA transferível sobre quem compra ("essa audiência responde a X porque Y"), não template de execução ("usar POV com fundo branco"). Template copiado sem o porquê morre na segunda aplicação; a estratégia viaja entre conceitos e formatos.
- **AI Ad Review do breakthrough (segunda opinião estruturada):** o sistema nomeado da base é o **AI Ad Review no Google AI Studio + checklist de 13 perguntas** (rode `Google AI Studio Gemini upload video por que este ad funciona tabela transposicao para minha marca`) — subir o vídeo vencedor e perguntar por que ele funciona, seguindo o checklist de 13 perguntas até a tabela de transposição do padrão. Confronta a hipótese causal desta ETAPA com uma leitura independente; o que divergir vira pergunta, não veredito. Alimenta o briefing da 08.

> **Learning é palpite fundamentado, não fato.** Uma hipótese só vira quase-fato quando é **reaplicada num criativo novo e gera outro breakthrough**. Grave as hipóteses da ETAPA 10 com esse status: uma hipótese "validada" sem reaplicação continua sendo hipótese.

**Re-research do ângulo vencedor (a perna do loop que volta pra 02):** breakthrough confirmado gera, além do `NEXT_BATCH_IDEAS.md`, uma recomendação EXPLÍCITA no relatório e na mensagem final: **"aprofunde a pesquisa DESTE ângulo antes do próximo swing grande"** — por que o cliente liga pra isso? (keep asking why: cada resposta ganha outro "por quê?" até chegar no desejo por trás do desejo). O handoff é nomeado: **Skill 02, mini-passada focada** no `winning_sub_avatar_id` e no ângulo vencedor — não uma re-execução completa da 02; só o recorte que venceu, minerando mais VOC daquele sub-avatar e aprofundando o porquê. O sistema da base pro aprofundamento vertical é o **Angle Research** (rode `angle research vertical cruzar fato de autoridade com produto claim defensavel` — cruzar fatos de autoridade com o produto até um claim defensável). O resultado alimenta **a próxima iteração Sniper** do breakthrough (cânone §7: é o Sniper que extrai o máximo do ângulo vencedor — e ele extrai mais com pesquisa nova na mão do que reciclando a VOC de antes do teste). **Fallback legado:** sem `sub_avatar_id`, o handoff nomeia o ângulo/persona pelo texto do briefing da 08.

Learnings vão alimentar Skill 08 (creatives) no próximo batch — escreva de forma utilizável.

### ETAPA 6 — Saúde do Funil (posição + conversão)

**6A — Posição de funil** (dos Pi 2 — frequency signatures):
> Pra recomendar qual posição reforçar, puxe **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`) — diz quais formatos/ângulos servem cada posição faltante (ex: TOF → hook problem/curiosity; BOF → offer/comparison). Isso alimenta o NEXT_BATCH_IDEAS com a posição + o tipo de conceito certo.
- Todos os ads em TOF? → normal na campanha de teste da Skill 10 (100% prospecting por construção); só vira "funil raso" quando já existe volume de warm audience acumulado sem nada convertendo ela
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

**6C — Quando a página converte mal: diagnóstico pelo espécime da copy**

Quando a leitura acima aponta a **página** como gargalo (checkout→compra ou ATC→compra abaixo do benchmark, com amostra suficiente), não devolva o membro pra 06/07 com "a página converte mal". Isso não é diagnóstico e produz reescrita às cegas. A skill 06 grava em `06-copy-engine/dados.json` exatamente o que permite localizar a falha (carregado no Contexto, item 4b). Rode as duas perguntas, nesta ordem:

**(a) O espécime escolhido era o certo pro avatar?**
- Leia `specimen_primary` (e `specimen_secondary`, se houver) e abra a entrada correspondente em `.claude/lib/swipe-models/specimens.json`.
- Compare o `aplica_a` do espécime (`page_type` × `awareness` × `sophistication` × `vertical`) com o avatar e o awareness reais do produto (`02-market-research/dados.json`) e com o `page_type` que de fato foi ao ar (`07-page`).
- Confira a `regra_diagnostica` do espécime: ela descreve a condição sob a qual aquela estrutura funciona. Se a condição não se sustenta no caso do membro, **a estrutura estava errada desde antes do tráfego** — nenhuma troca de criativo conserta isso.
- Grave o veredito em `page_diagnosis.specimen_fit`: `fit` · `mismatch_awareness` · `mismatch_page_type` · `mismatch_sophistication` · `mismatch_vertical` · `unknown` (quando `specimen_primary` não existir — página anterior à skill 06 atual).

**(b) Qual camada do markup audit já tinha reprovado antes do launch?**
- Leia `markup_audit`. Ele é o registro do que a auditoria de markup encontrou **antes** da página ir ao ar: os 4 U's da headline, ideal prospect, big promise, first page test, as 4 emoções, o lead de 4 passos, `defects_found` e o `verdict`.
- Se o `verdict` era `rewrite_lead`, ou se algum dos gates de headline estava em `false`, **a página subiu com um defeito conhecido** — e é ali que a investigação começa, não numa reescrita geral.
- Grave a camada que reprovou em `page_diagnosis.markup_audit_layer_failed` (ex: `four_us.unique`, `four_emotions.safe_predictable`, `makepeace_4.cred`) e liste os `defects_found` que continuam de pé.

**Roteamento com o diagnóstico na mão:**

| O que os dois checks mostram | Para onde volta |
|---|---|
| Espécime incompatível com o avatar/awareness | **06** — reselecionar o espécime (ETAPA 2.5) antes de reescrever qualquer bloco |
| Espécime certo, mas camada do markup audit reprovada | **06** — corrigir a camada nomeada (lead, headline, prova, oferta), não a página inteira |
| Espécime certo e audit limpo, checkout vazando | **07** (página/checkout) ou **04** (preço/oferta no checkout) |
| `specimen_primary` ausente (`unknown`) | Registre `data_gap` e trate como diagnóstico de página comum; a copy é anterior à camada de espécime |

Isso entra no `dados.json` (`page_diagnosis`) e no `NEXT_BATCH_IDEAS.md`. **Nunca mate criativo por falha localizada aqui** — o ad trouxe a intenção de compra que a estrutura da página desperdiçou.

**6D — Check de VOC insuficiente ANTES de culpar criativo/oferta:** se `06-copy-engine/dados.json.voc_forced_continue: true` (carregado no Contexto, item 4b) E CTR/CVR estão abaixo do esperado (CTR baixo generalizado entre os ads, ou CVR da página abaixo do benchmark), a hipótese primária muda: **a copy rodou com VOC insuficiente** — os hooks e a página falam a língua errada porque a matéria-prima de pesquisa era rasa. Diagnóstico: "copy rodou com VOC insuficiente — re-rodar skill 02 (market research) com mais fontes e re-gerar a copy antes de culpar criativo ou oferta". Registre em `health_signals` como `voc_insufficient_copy` e roteie pra 02 → 06, não pra 08. (Mesma lógica se `claims_unverified: true` e a página tem CVR baixo com tráfego bom: claims sem lastro derrubam confiança — rotear pra 04 Etapa 2.5.)

### ETAPA 7 — 12 Perguntas de Feedback (checklist desta skill)

Aplique as 12 perguntas aos dados (checklist próprio desta skill — no cenário padrão da Skill 10, a unidade é o AD dentro do ad set do seu conceito, com a leitura de qual CONCEITO o CBO financiou por cima):

1. Qual ad (criativo) teve maior ROAS e por quê? (em ad set `marksman`, responda também no nível do ângulo: qual dos 3 ângulos de `angles[]` venceu — ETAPA 3)
2. Qual teve menor ROAS e por quê?
3. Qual variável específica dentro dos **breakthroughs** tá puxando mais (persona, avatar, formato, ângulo, tema, benefício vs consequência, senso estético — o mapa da Skill 08)?
3b. Hook e Hold: onde os losers do batch perderam a audiência — na abertura (hook baixo) ou no corpo (hook bom, hold baixo)?
3c. Quantos conceitos foram testados e qual o `breakthrough_rate` do batch? Ele subiu ou caiu em relação ao batch anterior, e o volume de criativos subiu ou caiu junto?
3d. O ad log explica algum degrau da janela? Alguma **mudança logada ficou sem o efeito esperado**, ou algum **efeito apareceu sem mudança conhecida**? (Contexto 4g + bloco da ETAPA 2 — os dois achados entram na hipótese causal da pergunta 12)
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
- **Conferir as duas automações de proteção (cânone §6)** que a Skill 10 montou na ETAPA 6 dela — elas nascem DESATIVADAS e só protegem se o membro ligou. Leia o estado em `10-ad-strategy/dados.json → protections` e confirme no Ads Manager > Automated Rules: **(a)** pico de gasto (spend 5× em 24h → pausar) e **(b)** URL de destino ≠ domínio da loja → desligar o ad. Confira também o `daily maximum` de cada ad set de teste (~3× target CPA/dia). Alguma ausente ou desligada → é essa a ação de automação a recomendar. **Não existe rule de escala nem de kill por performance pra verificar** — o Meta recusa condição de performance em CBO; `pgs_enabled` é campo legado fixo em `false` e nunca autoriza prometer escala automática.

**CURTO PRAZO (3-7 dias):**
- Se tem fadiga: trocar os 1-2 criativos mais fatigados do ad set por conceitos novos da 08
- Se falta diversidade de funil: gerar novo batch de conceitos (Skill 08) com foco na posição faltante
- Se o breakdown por placement (Pi 4) mostrou placement comendo spend sem converter: documentar e decidir a exceção de opt-out

> **Antes de escrever qualquer ação que REDUZA spend** (pausar em bloco, baixar budget, "voltar pro ROAS de antes"): rode `.claude/lib/unit-economics/README.md` §4. ROAS é adimensional e ignora custo fixo — cortar spend por queda de ROAS pode **aumentar** o prejuízo, porque os fixos não encolhem junto e sobra menos receita pra diluí-los. **Se `15-finance-engine/dados.json` existir, a conta já está feita:** a ação sai do `roas_spiral.verdict` conforme a tabela do PLAYBOOK item 5 — cortar, segurar ou subir spend até `spend_to_breakeven_with_fixed`, com número, não com aviso. Sem o arquivo da 15, vale `budget_viability.fixed_costs_monthly`: faça a conta e recomende o que ela disser (às vezes é **subir** spend aceitando ROAS menor). **Sem os fixos em nenhuma das duas fontes, a ação não é "corte X%" — é a pergunta "quanto você tem de custo fixo por mês?"**. Isso não se aplica a pausar um `loser` individual pela régua de kill: ali o critério é o cânone §3, não o ROAS da conta.

**MÉDIO PRAZO (2-4 semanas):**
- Se há breakthrough estável (~7 dias): a promoção pra **ad set próprio em campanha ABO paralela** é decisão de estrutura da Skill 12 (o cânone `.claude/lib/ad-taxonomy/README.md` §5 aposentou o champions ad set em favor dessa rota, mantendo o ad original rodando no CBO). Aqui você só sinaliza que ele está pronto. `kpi_winner` **não** entra nessa fila.
- Se CPA está melhor que target consistentemente: reavaliar se dá pra escalar mais (vertical + horizontal — delegar pra Skill 12)
- Se oferta parece ser o bloqueio: voltar pra Skill 04 e ajustar (bundle structure, guarantee, stack)
- Se página parece ser o bloqueio: voltar pra Skill 06/07 e iterar

### ETAPA 9 — Decisão de Scaling (Recomendação Clara)

> Fundamente a recomendação puxando o sistema de scaling da base (rode a `best_query`): **Profitable Scaling Margin (PSM)** (`Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — usa o `psm_real` calculado na ETAPA 2 pra decidir agressivo/steady/breakeven/cortar. O ritmo de subida e descida é o **Scaling Protocol** do cânone `.claude/lib/ad-taxonomy/README.md` §5 (48-72h acima do target → **+20%**, depois a cada 24h; abaixo do breakeven **por 24-48h persistentes** → **−20%** — um dia ruim isolado não dispara), executado **à mão** pela Skill 12 — nunca por automação. A montagem detalhada do plano de escala (vertical + horizontal) é delegada pra skill 12; aqui só a recomendação.

**Escala automática não existe nesta estrutura (cânone §6).** Se o membro pedir "deixa uma regra escalando sozinha", a resposta é não — e o porquê tem duas camadas independentes:

1. **Tecnicamente o Meta recusa.** Automated Rule com condição de performance (CPA, ROAS, frequency) não roda em campanha que usa CBO; o erro retornado é literalmente *"performance-related conditions are not available for assets that use CBO"*. Não ofereça, não tente criar, não prometa.
2. **Mesmo onde rodasse, seria errado.** A métrica do Ads Manager engana — um ad a 1× ROAS na plataforma pode estar excelente no 1-day click de uma ferramenta de atribuição de terceiro. Automatizar kill ou escala por metadado do painel mata winner. **Kill e escala são leitura, não regra:** quem decide o kill é esta skill (réguas do §3) e quem executa a escala é a Skill 12 (Scaling Protocol do §5).

O que É automatizável já foi montado pela Skill 10 (ETAPA 6 dela) — confira o estado de cada item em `10-ad-strategy/dados.json → protections`:

- **`Ad set spending limit → daily maximum`** por ad set de teste (~3× target CPA/dia): é teto de gasto, não condição de performance, então funciona em CBO.
- **Automação obrigatória A — pico de gasto:** spend 5× em 24h → pausar.
- **Automação obrigatória B — URL errada:** destino ≠ domínio da loja → desligar o ad.

Alguma das duas rules ausente ou desativada → **essa** é a ação de automação a recomendar aqui, nunca uma rule de performance. O campo `pgs_enabled` do `10-ad-strategy/dados.json` é legado, fixo em `false`, e não deve ser lido como permissão pra prometer escala automática nem gravado como `true`.

> **Gate de piso (roda antes dos dois gates abaixo):** teste nascido abaixo do piso (`below_floor_directional_only: true` — PLAYBOOK item 6) não produz recomendação de escala NEM de kill: o resultado é direcional. A recomendação desta ETAPA vira "subir o budget até o piso de US$ 100-150/dia (cânone §1) ou reduzir o nº de conceitos no ar" — e o `recommended_action` gravado é `raise_budget_or_reduce_concepts`.
>
> **Gate único de escala:** só existe recomendação de escalar quando há **≥ 1 `breakthrough`**. `kpi_winner` e `spend_winner` **não** liberam escala — o primeiro não provou nada em spend, o segundo já está diluindo o KPI da campanha. A skill 12 confere isso de novo no pré-flight dela; não a mande pra lá sem breakthrough. A 12 também confere o **gate click-based** do cânone §5 lendo `manifest.click_based_purchase_share` gravado nesta análise (bloco da ETAPA 2) — sem o número, aquele gate fica bloqueado; nunca estime.

> **Gate de corte:** nenhuma recomendação desta ETAPA que reduza spend por queda de ROAS sai sem `.claude/lib/unit-economics/README.md` §4 aplicado com os custos fixos na mesa. **Fonte preferencial: `15-finance-engine/dados.json` → `roas_spiral`** (a 15 calcula e publica; esta skill lê pela tabela do PLAYBOOK item 5). Na ausência dela, `budget_viability.fixed_costs_monthly` do 04. Sem os fixos em nenhuma das duas, o output é a pergunta, não a instrução.
>
> **Quando o veredito da 15 é `scale_up_accept_lower_roas`,** a recomendação desta ETAPA é subir spend até `spend_to_breakeven_with_fixed` — e ela é **independente do gate de escala acima**: não é escala de breakthrough (que exige criativo provado), é diluição de custo fixo. Diga a diferença ao membro em uma frase pra ele não confundir as duas decisões.

Baseado no diagnóstico completo, dê uma recomendação clara:

**SE existe `breakthrough` e o CPA está dentro do target:**
"Continue rodando. Não tem regra escalando sozinha, e isso é de propósito: em campanha com CBO o Meta não aceita automação por condição de performance, e decidir por metadado do painel mata winner. A subida de budget é decisão de leitura, feita à mão. Diga **'scale'** que a Skill 12 aplica o Scaling Protocol (48-72h acima do target → +20%, depois a cada 24h) e monta a promoção do breakthrough pra ad set próprio em campanha ABO paralela."

**SE CPA ≤ 0.7× target E há `breakthrough` claro:**
"Oferta forte, ads matando. Diga **'scale'** pra montar plano de escala vertical + horizontal — com esse PSM a Skill 12 pode ir mais agressiva no Scaling Protocol, sempre à mão e com a regra de reset do cânone §5 aplicada (ao ajustar budget, o novo valor sai de ~50% do que foi REALMENTE gasto, nunca do budget nominal)."

**SE só existe `kpi_winner` (nenhum breakthrough):**
"Você tem criativo batendo o KPI, mas nenhum que puxe spend — e ad que bate KPI com pouco spend ainda não provou nada em escala. Isso não é hora de escalar. Dois caminhos: (a) forçar spend num ad set próprio pra esse criativo, pra tirar a dúvida se o limite é ele ou a audiência (diga **'scale'** que eu passo pra estrutura); (b) diga **'creatives'** pra gerar conceito novo. O que **não** funciona é subir budget da campanha esperando que ele apareça."

**SE só existe `spend_winner` (nenhum breakthrough):**
"Tem criativo puxando spend, mas com KPI abaixo do da própria campanha — ele segura a conta onde está, não escala. O trabalho é iteração: diga **'creatives'** pra rodar a variação de uma variável só, com os learnings desta análise."

**SE nenhum breakthrough e nenhum sinal (só losers):**
"Você ainda não tem um ad que escala. Isso é o normal estatístico, não fracasso: o hit rate esperado de super winner é de 1-3% dos criativos testados. O próximo passo é volume com intenção (skill 08), não budget."

**SE CPA acima do target mas ainda abaixo de 2×:**
"Não escala. Foco em iteração. Diga **'creatives'** pra gerar novo batch baseado nos learnings desta análise."

**SE CPA > 2× target após 7+ dias:**
"Bloqueio não é só ad — pode ser oferta, página, ou audience. Vou sugerir investigação: [indicar onde está o bloqueio mais provável baseado no 19-point]. Depois de ajuste, re-roda análise em mais 7 dias."

**SE funil quebrado (ETAPA 6B abaixo do benchmark):**
"Os criativos estão trazendo gente que adiciona ao carrinho e inicia checkout, mas a conversão final está abaixo do esperado ([checkout→compra X% vs 40-50% ideal]). O gargalo é a página/checkout, não o ad. [Acrescente aqui o resultado da ETAPA 6C, com o nome próprio da falha: espécime incompatível com o avatar (`page_diagnosis.specimen_fit`) ou camada do markup audit que já tinha reprovado antes do launch (`page_diagnosis.markup_audit_layer_failed`).] Antes de mexer em criativo: diga **'copy'** pra corrigir a camada específica (ou **'page'** / **'offer'** se o bloqueio for checkout ou preço)."

**SE conta suspeita (`account_cpm_suspect`):**
"O CPM está bem acima do esperado do nicho de forma generalizada — isso costuma ser a CONTA, não o produto. Antes de matar o produto, vale re-testar o mesmo criativo em outra conta de anúncio. Se quiser, monto a estrutura de teste de novo (diga **'ad strategy'**)."

### ETAPA 10 — Learnings Documentados (Pra Feedback Loop)

Na seção final do relatório, documente learnings que vão alimentar próximos batches:

**Hipóteses confirmadas por reaplicação** (a hipótese foi aplicada num criativo novo e ele virou `breakthrough` — só aqui ela deixa de ser palpite):
**Hipóteses levantadas nesta rodada** (vieram dos breakthroughs deste batch, ainda **não** reaplicadas — continuam sendo palpite fundamentado):
**Hipóteses rejeitadas** (foram reaplicadas e não confirmaram):
**Hipóteses ainda em teste** (precisa mais dados):
**Ideias pra próximo batch:**

Isso é o "feedback loop motor de crescimento" — cada análise enriquece o próximo batch de criativos.

### ETAPA 11 — DNA Update (silent — feedback automático pro registry)

Pra cada criativo analisado nesta rodada:

1. Gravar `ad_class` (as 4 classes do cânone §2 — o mesmo valor de `11-ad-analysis/dados.json` — mais `unclassified` quando ainda não há base pra classificar) **e** o `outcome` legado que o registry aceita.

   O banco do registry (`.claude/lib/creative-dna/schema.sql`) valida `outcome` contra um enum próprio e **não conhece** as 4 classes — gravar `breakthrough` ali quebra o insert. Por isso o perf JSON leva os dois campos, com este mapeamento fixo:

   | `ad_class` (canônico) | `outcome` (legado, pro registry) |
   |---|---|
   | `breakthrough` | `winner` |
   | `spend_winner` | `neutral` |
   | `kpi_winner` | `neutral` |
   | `loser` **com pelo menos 1 purchase no período** | `loser` |
   | `loser` **sem nenhuma purchase no período** | `zero_conversions` |
   | `unclassified` (ainda em aprendizado / sem `campaign_cpa` estável / análise DIRECIONAL do gate de piso — PLAYBOOK item 6) | `insufficient_data` |
   | criativo em FUNIL QUEBRADO (não foi ele que falhou) | `neutral` |

   `spend_winner` e `kpi_winner` vão pra `neutral` de propósito: nenhum dos dois é evidência de acerto, e marcá-los como `winner` envenenaria as correlações de feature que o `dna-profile.json` calcula — exatamente o falso positivo que esta correção elimina. Sinal forte de breakthrough: spend > $300 E decile_rank 1-2.

   O desdobramento do `loser` em dois destinos existe porque **`zero_conversions` é o negativo mais forte do enum legado** e o registry precisa dele: gastou e não converteu nenhuma vez é um sinal de aprendizado cross-product mais nítido que "converteu mal". O que separa as duas linhas é só a contagem de purchases do período analisado: zero ou não. **Nenhum corte de spend entra nesta gravação** — quanto o criativo precisa gastar antes de ser morto é a régua de kill do cânone §3, decisão separada, tomada antes e por outro motivo. Esta é a MESMA conversão que a receita `sync-campaign-from-meta.md` aplica no `to_legacy_outcome()` dela; os dois escritores do registry usam o mesmo vocabulário, senão o mesmo criativo entra no banco com rótulo diferente conforme quem gravou.

2. Compor performance JSON:
   ```json
   {
     "cpa": 38.5, "ctr": 1.4, "roas": 2.6, "spend": 412.0,
     "thumbstop_3s": 0.31, "hold_15s": 0.12,
     "impressions": 48210, "clicks": 675, "purchases": 11,
     "days_active": 7, "decile_rank": 2,
     "ad_class": "breakthrough|spend_winner|kpi_winner|loser|unclassified",
     "outcome": "winner|loser|neutral|zero_conversions|insufficient_data"
   }
   ```
   Os números do exemplo são ilustrativos — grave os medidos deste criativo. `thumbstop_3s` recebe o **hook rate** (3-second plays ÷ impressões) e `hold_15s` recebe o **hold rate** (ThruPlays ÷ impressões), medidos na ETAPA 2 — os dois nomes de campo são legados do registry, o conteúdo é o do cânone §4. Criativo estático: `null` nos dois. Nunca grave esses campos vazios: sem eles o `dna-profile.json` não consegue correlacionar abertura e retenção com resultado.

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
- **Variável a testar na iteração de cada breakthrough** (1 bullet por breakthrough: qual variável única muda mantendo o resto — ex: "c-03: mesma estrutura, testar a micro-persona X no lugar da Y"). `spend_winner` também ganha um bullet de iteração; `kpi_winner` não entra aqui.
- **Método da iteração (contrato com a 08):** vencedor de pack `marksman` entra como iteração **`sniper` sobre o ângulo vencedor** (nomeado pela frase de `angles[]` + `winning_sub_avatar_id`); ângulo que perdeu com UMA execução só entra como re-teste (os 3 strikes do Execution Problem — ETAPA 3) antes de ir pra lista de evitar. Iteração que trocou de zona emocional (`iteration_zone_check`, ETAPA 4) entra refeita **na zona original**, mudando só a variável pretendida.
- **Re-research do ângulo vencedor** (ETAPA 5): registre aqui que a mini-passada da 02 no sub-avatar/ângulo vencedor precede o próximo swing grande — o batch derivado do breakthrough espera essa pesquisa quando ela foi recomendada.
- **Onde os losers perderam a audiência** (hook vs hold, com os números medidos): hook baixo → o próximo batch reescreve a abertura do mesmo conceito; hook bom + hold baixo → mantém a abertura e refaz o corpo.
- **Governador de volume:** se o `breakthrough_rate` caiu quando o volume de criativos subiu, o próximo batch deve ser **menor e mais deliberado** — a diretiva pra 08 é intenção, não quantidade.
- **Ângulos a EVITAR** (identificados como saturados ou já losers)
- **VOC phrases não usadas ainda** que aparecem em learning de review mining
- **Formatos a priorizar** (UGC vs studio vs static vs video — baseado em performance)
- **Awareness stage para focar** (se campanha atual oversserve um stage)
- **Ideias carry-over** (propostas antes, ainda não testadas)

**Skill 08 DEVE ler este arquivo no pre-flight.** Isto fecha o loop 11→08 **com critério de parada.**

### Panorama para skill 12 (scale) e skill 14 (content-recycler) — handoff

Se ações próximas = 'scale', skill 12 lerá este JSON SEM precisar perguntar.
Se membro invoca `recycle winner`, skill 14 lerá esse JSON pra achar o criativo — e o que ela lê é **`breakthroughs[]`**, não mais um genérico "winners".

O arquivo de análise é `workspace/[produto]/11-ad-analysis/dados.json` (cópia do último análise — nome literal `dados.json` dentro da pasta `11-ad-analysis/`):

```json
{
  "analysis_id": "uuid",
  "analyzed_at": "ISO timestamp",
  "current_daily_spend": 0,
  "current_cpa_avg": 0,
  "current_roas_avg": 0,
  "campaign_kpi": {
    "campaign_cpa": 0,
    "campaign_roas": 0,
    "account_spend_7d": 0,
    "window_days": 7,
    "stable": true
  },
  "batch_rates": {
    "concepts_tested": 0,
    "hit_rate": 0,
    "breakthrough_rate": 0,
    "volume_up_rate_down": false
  },
  "test_capacity_check": {
    "source": "10-ad-strategy|none",
    "binding_constraint": "max_adsets|floor|adset_cap_5|batch_size|margin_warning|none|null",
    "below_floor_directional_only": false,
    "directional_only_analysis": false
  },
  "active_breakthroughs_count": 0,
  "active_losers_count": 0,
  "breakthroughs": [
    { "creative_id": "c-01", "ad_set_id": "...", "ad_class": "breakthrough", "cpa": 0, "roas": 0, "spend_total": 0, "spend_share_7d": 0, "ad_kpi_vs_campaign": true, "hook_rate": 0, "hold_rate": 0, "days_active": 0, "winning_sub_avatar_id": "sa-01|null" }
  ],
  "spend_winners": [
    { "creative_id": "c-02", "ad_class": "spend_winner", "cpa": 0, "roas": 0, "spend_total": 0, "spend_share_7d": 0, "ad_kpi_vs_campaign": false, "hook_rate": 0, "hold_rate": 0, "days_active": 0, "next_action": "iterate" }
  ],
  "kpi_winners": [
    { "creative_id": "c-04", "ad_class": "kpi_winner", "cpa": 0, "roas": 0, "spend_total": 0, "spend_share_7d": 0, "ad_kpi_vs_campaign": true, "hook_rate": 0, "hold_rate": 0, "days_active": 0, "treated_as": "loser_for_decision", "next_action": "force_spend_test|drop" }
  ],
  "losers": [
    { "creative_id": "c-03", "ad_class": "loser", "reason": "adset_7d_no_spend_no_kpi|kill_8x_target_cpa_no_purchase|spend_share_under_2pct_7d|creative_policy", "spend_share_7d": 0, "hook_rate": 0, "hold_rate": 0, "days_active": 0 }
  ],
  "winners": [],
  "champions": [
    { "creative_id": "c-01", "post_id": "...", "promoted_at": "ISO timestamp" }
  ],
  "health_signals": {
    "frequency_max": 0,
    "cpm_trend": "up|flat|down",
    "creative_age_days_oldest": 0,
    "creative_age_days_newest": 0,
    "account_cpm_suspect": false,
    "hook_rate_avg": 0,
    "hold_rate_avg": 0,
    "funnel_atc_to_purchase_rate": 0,
    "funnel_checkout_to_purchase_rate": 0,
    "funnel_broken": false
  },
  "page_diagnosis": {
    "specimen_primary": "agora-11-blocos|null",
    "specimen_fit": "fit|mismatch_awareness|mismatch_page_type|mismatch_sophistication|mismatch_vertical|unknown",
    "markup_audit_verdict": "pass|rewrite_lead|unknown",
    "markup_audit_layer_failed": null,
    "defects_still_open": []
  },
  "iteration_zone_check": [
    { "iteration_creative_id": "c-07", "original_ref": "c-03", "zone_original": "positive/low|unknown", "zone_iteration": "negative/high|unknown", "zone_changed": true, "verdict": "zone_shift_suspected|variable_isolated|no_data" }
  ],
  "roas_spiral_check": {
    "source": "15-finance-engine|04-offer-builder|none",
    "fixed_costs_monthly": null,
    "breakeven_roas_with_fixed": null,
    "spend_to_breakeven_with_fixed": null,
    "finance_verdict": "covers_fixed_costs|scale_up_accept_lower_roas|cut_spend_below_variable_breakeven|blocked_pending_fixed_costs|null",
    "spend_cut_considered": false,
    "spend_cut_recommended": false,
    "blocked_reason": "fixed_costs_unknown|null"
  },
  "click_based_purchase_share": null,
  "psm_real": 0,
  "psm_real_basis": "shopify_new_customer|platform_cpa_proxy",
  "cac_real": 0,
  "new_customers_period": 0,
  "margin_per_order_weighted": 0,
  "recommended_action": "continue|scale|iterate_creatives|refresh_creatives|kill|fix_funnel|fix_copy_specimen|test_other_account|ask_fixed_costs|raise_spend_accept_lower_roas|raise_budget_or_reduce_concepts"
}
```

**Importante:**
- **`ad_class` é o campo canônico de classificação** desta skill, com os quatro valores do cânone `.claude/lib/ad-taxonomy/README.md` §2: `breakthrough` · `spend_winner` · `kpi_winner` · `loser`. Todo criativo classificado carrega esse campo, e é por ele que as skills 12 e 14 devem decidir — nunca por "CPA ≤ target".
- **`breakthroughs[]` substitui `winners[]`** como gatilho de escala (skill 12) e de reciclagem (skill 14). Ele contém **apenas** `ad_class == "breakthrough"`.
- **`winners[]` fica como alias legado, e só pode conter exatamente o mesmo conteúdo de `breakthroughs[]`** — existe para que um leitor antigo não quebre e, principalmente, não receba um `kpi_winner` disfarçado de winner. Está deprecado: leitores novos usam `breakthroughs[]`. **Nunca** coloque `kpi_winner` ou `spend_winner` nesse array.
- Skill 14 apenas LÊ `breakthroughs[]` e ordena por `spend_total`/`days_active` (NÃO re-filtra nem recomputa threshold nenhum — a classificação é responsabilidade exclusiva da skill 11). Se `breakthroughs[]` vier vazio, a resposta honesta ao membro **não** é "aguardar mais dados": é "você ainda não tem um ad que escala — o próximo passo é a 08, não a 14".
- `psm_real` é o mesmo valor gravado em `manifest.psm_real`, e `psm_real_basis` diz em que base ele foi calculado (`shopify_new_customer` = comparável com o `psm_theoretical` da 04; `platform_cpa_proxy` = otimista, **não** comparável e não libera escala).
- **`roas_spiral_check` registra de ONDE veio a decisão de spend.** Com `15-finance-engine/dados.json` na mão, `source: "15-finance-engine"` e os quatro campos vêm copiados de lá (`breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed`, `finance_verdict`, mais `fixed_costs_monthly` de `monthly_model`) — esta skill não recalcula nenhum deles. Sem o arquivo, `source: "04-offer-builder"` (ou `"none"`), os três campos novos ficam `null` e o `blocked_reason` volta a operar como hoje. `recommended_action: "raise_spend_accept_lower_roas"` só pode ser gravado quando `finance_verdict == "scale_up_accept_lower_roas"` — nunca por leitura própria de ROAS.
- **`winning_sub_avatar_id`** (por item de `breakthroughs[]`) fecha o loop com a pesquisa: aponta o item de `sub_avatars[]` da 02 que produziu o vencedor (num Marksman, o do item de `angles[]` do criativo vencedor). `null` em batch legado sem o campo. É o alvo da mini-passada de re-research da ETAPA 5.
- **`test_capacity_check`** copia `binding_constraint` e `below_floor_directional_only` da 10; `directional_only_analysis: true` marca que ESTA análise inteira saiu direcional (gate de piso) — as skills 12 e 14 não devem tratar `breakthroughs[]` vazio dessa análise como veredito. `source: "none"` = estratégia legada sem `test_capacity`.
- **`iteration_zone_check[]`** registra o diagnóstico de valência da ETAPA 4 (iteração que trocou de zona emocional); `original_ref` vem de `concepts[].iteration_of` da 08 quando presente (linhagem declarada), com fallback = pareamento por prosa do briefing (batch legado); `verdict: "no_data"` quando o batch é anterior ao schema de `valence`/`intensity` da 08.
- **`click_based_purchase_share`** espelha o que vai pro manifest (bloco da ETAPA 2): fração das purchases da janela em 7-day click. `null` = breakdown indisponível — **nunca estimado**; o gate de escala da 12 fica bloqueado até existir.
- `champions[]` permanece por compatibilidade (Post ID dedicado). A rota vigente de promoção de breakthrough é o ABO paralelo da skill 12 (cânone §5).

### Atualização do manifest (OBRIGATÓRIO — single source of truth)

Após gerar `dados.json`, atualizar `manifest.json` com campos canônicos:

- `manifest.psm_real` ← `psm_real` calculado nesta análise pela fórmula canônica `LTV / (CAC_real + COGS)`, com CAC = ad spend ÷ clientes novos do Shopify. **A skill 11 é a ÚNICA fonte que grava `manifest.psm_real`** (skill 12 lê daqui, nunca recalcula).
- `manifest.psm_real_basis` ← `"shopify_new_customer"` ou `"platform_cpa_proxy"`. A skill 12 compara `psm_real` com `psm_theoretical` (tolerância de 20%) — **essa comparação só é válida quando a base é `shopify_new_customer`**; com proxy, o número está otimista e não pode liberar escala.
- `manifest.ad_classification[]` ← **TODOS os criativos classificados nesta análise**, no shape do `manifest-schema.json`: `{creative_id, class, spend_share_7d, ad_kpi, campaign_kpi, hook_rate, hold_rate}`. `class` = o `ad_class` canônico; `ad_kpi`/`campaign_kpi` = o par usado na comparação de classificação (CPA do ad vs CPA da campanha — ou ROAS vs ROAS quando a régua de desempate for ROAS, bloco Winner picking; grave os dois lados na MESMA métrica); `hook_rate`/`hold_rate` = os medidos na ETAPA 2 (`null` pra estático). **Substitui o array inteiro a cada análise** (é estado atual, não histórico — o histórico vive nos `dados.json` datados). É a fonte de verdade que o schema declara como substituta de `winners[]`: a 12 e a `member-stage-awareness` leem `class == "breakthrough"` daqui. Análise direcional (gate de piso): não grave — sem classificação formal não há o que espelhar.
- `manifest.click_based_purchase_share` ← fração das purchases da janela atribuídas em 7-day click (bloco da ETAPA 2). É o gate de escala da 12 (≥ 0.60, cânone §5). **NUNCA estimar** (regra do manifest-schema): sem o breakdown de atribuição, NÃO grave o campo — o gate fica bloqueado e o relatório diz onde buscar o número.
- `manifest.breakthroughs[]` ← lista de creative_ids com `ad_class == "breakthrough"` nesta análise (espelha `dados.json.breakthroughs[]`). **É este o campo que as skills 12 e 14 devem ler.**
- `manifest.winners[]` ← alias legado, com **exatamente** os mesmos ids de `manifest.breakthroughs[]` (nunca `kpi_winner` nem `spend_winner`). Existe só pra não quebrar leitor antigo; deprecado.
- `manifest.kpi_winners[]` / `manifest.spend_winners[]` ← creative_ids das outras duas classes, pra que a skill 12 saiba que existe sinal sem que ele seja confundido com liberação de escala.
- `manifest.champions[]` ← acrescentar creative_ids promovidos a Post ID dedicado (não sobrescrever os já existentes; merge sem duplicar)
- `manifest.last_analysis_date` ← timestamp desta análise
- `manifest.analysis_count` ← incrementar +1
- `manifest.last_cpa_avg` ← `current_cpa_avg`
- `manifest.last_roas_avg` ← `current_roas_avg`
- `manifest.last_recommended_action` ← `recommended_action` (inclui `fix_funnel` e `test_other_account` do playbook — sinaliza pra skill 12 que o bloqueio não é escala)
- `manifest.account_cpm_suspect` / `manifest.funnel_broken` ← espelham `dados.json.health_signals` (sinalizam que matar produto/criativo seria erro — é conta ou página)
- `manifest.breakthrough_rate` ← `batch_rates.breakthrough_rate` desta análise (a skill 12 usa como leitura de saúde do pipeline de criativo; benchmark de super winner: 1-3%)
- Se `manifest.skipped_preflight` foi marcado no pré-flight (estratégia faltante), manter a flag.

Por que atualizar manifest: skills 12 e 14 leem `manifest.psm_real` (+ `psm_real_basis`), `manifest.breakthroughs[]` e `manifest.champions[]` como fonte canônica. O `dados.json` é histórico por análise; manifest é o estado atual consolidado.

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
- Registrar `last_analysis_date`, `psm_real` + `psm_real_basis` (calculado via `LTV / (CAC_real + COGS)`), `breakthroughs[]` (+ o alias legado `winners[]` com o mesmo conteúdo), `kpi_winners[]`, `spend_winners[]`, `champions[]` (merge), `recommended_action`, **`ad_classification[]`** (shape do manifest-schema — substitui o array inteiro a cada análise) e **`click_based_purchase_share`** (quando medido; NUNCA estimado — sem o breakdown, não gravar)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html)

## Mensagem Final

Adapte baseado no diagnóstico (ver Etapa 9 — recomendação de scaling). Termine sempre com uma próxima-ação CLARA:

- Continua rodando (sem automação de escala — ela não existe em CBO) → monitora, próxima análise em 3-7 dias
- Teste abaixo do piso (`below_floor_directional_only` — PLAYBOOK item 6) → diga com todas as letras que o resultado é DIRECIONAL e que a próxima ação é subir o budget até o piso de US$ 100-150/dia OU reduzir conceitos no ar — nunca kill nem escala com esse dado
- Escala (**só com `breakthrough`**) → diga `'scale'`
- Breakthrough confirmado → junto da próxima ação, a recomendação de re-research (ETAPA 5): "aprofunde a pesquisa DESTE ângulo antes do próximo swing grande" — mini-passada da 02 no sub-avatar vencedor (`winning_sub_avatar_id`); o resultado alimenta a próxima iteração Sniper
- Iteração de criativos (`spend_winner`, `kpi_winner`, ou nenhum sinal) → diga `'creatives'`
- Ajuste de oferta → diga `'offer'`
- Ajuste de página → diga `'copy'` (camada de copy/espécime nomeada na ETAPA 6C) ou `'page'` (checkout/técnico)
- Custos fixos desconhecidos travando uma decisão de spend → pergunte o número antes de recomendar qualquer corte (e ofereça rodar **'finanças'** — a skill 15 fecha essa conta e devolve o breakeven com o fixo dentro)
- Espiral do ROAS com veredito de **subir** spend (`finance_verdict: "scale_up_accept_lower_roas"`) → diga o número: até quanto subir (`spend_to_breakeven_with_fixed`) e qual ROAS isso aceita
- Bloqueio técnico → resolução específica + nova análise depois

> Quando não há breakthrough, diga isso com todas as letras: "você ainda não tem um ad que escala". Não substitua por "aguardar mais dados" — o membro precisa saber que o próximo passo é criativo (08), não paciência.
