---
name: scale-engine
description: Engine de escala vertical de Meta Ads governada pelo Scaling Protocol (48-72h acima do target → +20%, depois a cada 24h; −20% só após 24-48h persistentes abaixo do breakeven; gate click-based de duas portas; as duas exceções — promo com data-fim e "new reason to be scaling"; reset de budget da meia-noite sobre o gasto REAL) do cânone `.claude/lib/ad-taxonomy/README.md`, com 3 escolas reais de gestores de tráfego (A cost-cap duplication + surf, B bid cap "campanha monstro", C budget-doubling) rebaixadas a variantes de intensidade dentro do protocolo, recomendadas por member-stage, com execução opcional das estruturas em PAUSED via Meta Ads MCP (membro revisa e ativa) e graduação pra Advantage+ Sales em spend alto. Libera escala só com breakthrough (KPI winner não conta), aplica o cânone de unit-economics antes de qualquer corte de spend por queda de ROAS, mantém PSM (lê manifest.psm_real + psm_real_basis, não recomputa) como diagnóstico, projeções 30/60/90 com cash flow, registra toda mudança de budget no ad-log do produto (e verifica lá o gate de 24h entre degraus), e fecha ciclo de volta pra 08 quando precisa de criativo novo. Use quando o membro disser "scale", "escalar", "plano de escala", "crescer", "maximizar", ou quando os ads estão estáveis e quer aumentar spend de forma sistemática.
---

# Scale Engine

## Quando Usar
Quando o membro tem **breakthrough(s)** provados (criativo cujo KPI é melhor que o KPI da campanha **e** que puxa spend — classificação canônica em `.claude/lib/ad-taxonomy/README.md` §2, medida pela skill 11) e quer aumentar spend de forma sistemática sem queimar conta. Esta skill é a **camada de execução operacional** de escala: qual régua de subida e descida seguir (o Scaling Protocol da ETAPA 3.5), qual estrutura montar no Ads Manager, quanto duplicar, quando surfar, quando recuar. PSM e 4Pi continuam como leitura de diagnóstico (a skill 11 calcula), mas o "exatamente o que fazer" vive aqui.

> **Pré-condição honesta:** escala não conserta ad ruim nem oferta fraca. Se não tem breakthrough, isto não é hora de escalar — é hora de mais criativo (skill 08) e melhor oferta (skill 04). Criativo que bate o KPI mas não puxa spend (`KPI winner`) **não** conta como liberação de escala. A skill detecta isso na ETAPA 3 e te manda de volta sem culpa.

## Antes de Começar

### report_language (regra 0 do CLAUDE.md — INVIOLÁVEL)

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma, com o estilo de escrita da regra 0 do `.claude/CLAUDE.md` na íntegra (linguagem simples, sigla sempre explicada na primeira vez, português natural sem jargão cru). **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

### Pré-flight
- [ ] `10-ad-strategy/dados.json` + `11-ad-analysis/dados.json` existem (`workspace/[produto]/11-ad-analysis/dados.json`)
- [ ] Manifest tem `11-ad-analysis` em `skills_completed`
- [ ] `manifest.psm_real` foi gravado por ≥ 1 análise recente (senão, rodar 11 — quem calcula `psm_real`). Leia junto `manifest.psm_real_basis` — a base decide se a comparação com o teórico vale (ver "PSM real (vs teórico)")
- [ ] Existe ≥ 1 **breakthrough** entre os criativos analisados pela 11. A classificação canônica é a das **4 classes** de `.claude/lib/ad-taxonomy/README.md` §2 (loser · KPI winner · spend winner · breakthrough) — a skill 12 **não redefine** essas classes, só as lê:
  - **`breakthrough`** = KPI do AD melhor que o KPI da CAMPANHA **e** puxa spend → **é o único que libera escala**.
  - **`KPI winner`** (bate o KPI mas **não** puxa spend) → **NÃO libera escala.** O KPI bonito veio de amostra pequena; o cânone manda tratá-lo como loser para decisão.
  - **`spend winner`** (puxa spend com KPI abaixo do da campanha) → itera, não escala.
  - Se `11-ad-analysis/dados.json` já traz a classe por criativo, use-a direto. Se traz só `winners[]` (formato anterior), aplique a régua do cânone §2 sobre os mesmos números **antes** de liberar escala — "CPA ≤ target" sozinho não distingue breakthrough de KPI winner. Para carregar o sistema nomeado, rode `breakthrough spend winner KPI winner losing ad classificação destino por categoria`.
  - Post ID dedicado (`champions[]`) segue **opcional** pra escalar. Sem breakthrough, escala é prematura.

Se algum arquivo de pré-flight faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill faltante agora (11 pra `11-ad-analysis/dados.json`/`psm_real`, 10 pra ad-strategy), **OU (B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar.

### Contexto a carregar

1. Leia `workspace/profile.md` (budget atual + stage — define ponto de partida e agressividade)
2. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (se não existir, leia o legado `relatorio.md`) + `04-offer-builder/dados.json` (breakeven CPA/ROAS, `cogs_breakdown`, PSM projetado — define o teto de cost cap / bid cap). Leia também `manifest.margin_warning`: se `true`, a Skill 04 flagou margem ponderada < $20/pedido — tratar como pré-requisito de prontidão na ETAPA 3 (margem apertada amplia o dano de qualquer CPA acima do alvo na escala)
3. Leia `workspace/[produto]/10-ad-strategy/ad-strategy.md` (estrutura de campanha atual: estamos na estrutura de teste da 10 — 1 campanha CBO → N ad sets, 1 por conceito → 3 ads? cost cap já roda?)
4. Leia TODAS as análises em `workspace/[produto]/11-ad-analysis/` em ordem cronológica (trajetória real de performance, classificação por criativo, CPM por conta) + `dados.json` (handoff da skill 11)
5. Leia scale plans anteriores em `workspace/[produto]/12-scale-engine/` (se existir — comparar premissas com realidade)
5b. Leia `manifest.agentic` **(if exists)** — `{ready, channel_enabled, score, checked_at}` escrito pela Skill 07e. Se `ready: true`, a loja está descobrível por agentes de compra com AI (ChatGPT, Perplexity, Google AI Mode) — trate esse referral como **fonte incremental de tráfego no scale horizontal** (ver ETAPA 8). Ausente ou `ready: false` → ignorar silenciosamente (canal não existe ainda; se o membro está escalando forte, vale sugerir rodar a 07e como quick win).
5c. **Leia os dois cânones antes de qualquer recomendação** (leitura obrigatória, não opcional — a skill referencia, nunca redefine):
   - `.claude/lib/ad-taxonomy/README.md` — **§2** (as 4 classes que definem o gatilho de escala) e **§5** (Scaling Protocol, ABO paralelo, gate click-based e a regra de reset da meia-noite). É a fonte de verdade de QUANDO e QUANTO subir/descer.
   - `.claude/lib/unit-economics/README.md` — **§1** (margem de contribuição ≠ lucro) e **§4** (a espiral do ROAS). É o gate obrigatório antes de qualquer recomendação de cortar spend.

   Onde a skill e o cânone divergirem, **o cânone vence** — e a divergência é bug da skill, a reportar.

5d. Leia `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** — a skill 15 é a dona do modelo financeiro completo (cânone §5) e publica os números que esta skill hoje estima sozinha. Seis campos, cada um com o ponto exato onde entra:

   | Campo da 15 | Onde esta skill usa | Fallback quando a 15 não rodou |
   |---|---|---|
   | `cash.cash_needed_90d` | ETAPA 6 — substitui o `cash_gap_projected` estimado localmente | Fórmula local da ETAPA 6 |
   | `cash.float_stack.total_float_days` | ETAPA 6 — o float real do membro no lugar do `payout_lag_days` isolado | `payout_lag_days` (3-5 nominais; 7-14 pra loja nova) |
   | `cash.runway_months` | ETAPA 6 e ETAPA 7 — quantos meses o caixa aguenta o plano | Não existe hoje; segue sem a linha |
   | `monthly_model.fixed_costs_monthly` | ETAPA 1 (não perguntar o que já está gravado), gate de corte e ETAPA 7 (camada de fixo na projeção) | Pergunta ao membro, como hoje |
   | `payback.scale_ceiling_monthly_spend` | ETAPA 3.5 — teto dos passos de +20% | Não existe hoje; o teto é descoberto empiricamente (a escola quebra e recua) |
   | `roas_spiral.cut_spend_recommendation_allowed` (+ `roas_spiral.verdict`) | Gate de corte por ROAS — decide o `fixed_cost_gate.roas_cut_recommendation` | Gate local: fixos conhecidos → conta; desconhecidos → pergunta |

   **Leitura aditiva:** esta skill **lê e aplica, nunca recalcula** os campos acima; e sem o arquivo da 15, cada ponto de uso cai no fallback da coluna 3 — o comportamento de hoje, inteiro. A 15 nunca é pré-requisito da 12.

5e. Leia `workspace/[produto]/ad-log.md` **(se existir)** — o registro cronológico de toda mudança executada na conta (cânone `.claude/lib/ad-log/README.md`). É DAQUI que sai a última mudança de budget e há quanto tempo ela aconteceu — **o gate de 24h entre degraus é verificado no log, não de memória** (ETAPA 3.5); e mudança recente ainda sem leitura fechada é motivo pra segurar o passo. Sem o arquivo (conta nunca operada pelas skills), o histórico vem do membro — e o log nasce na primeira mudança que esta skill instruir/executar.

5f. Leia `workspace/[produto]/sourcing/dados.json` **(se existir)** — a 01b (ETAPA 12) grava `calendar.volume_confirmation_30_60_90` (confirmação escrita do fornecedor pro volume de 30/60/90 dias) e `calendar.reorder_point_days` (ponto de recompra em dias de estoque restante). Existindo, esses campos respondem o check de fornecedor da ETAPA 3 e da ETAPA 6 — **não re-pergunte ao membro**. Sourcing nunca rodou → o check segue com a pergunta de hoje.

6. **Puxe os SISTEMAS NOMEADOS da base — NUNCA query genérica — e cubra o domínio, não uma amostra** (contrato de cobertura do `.claude/lib/kb-index/README.md`):
   - **Enumere o domínio inteiro no início de cada ETAPA que consulta a base:** abra `.claude/lib/kb-index/frameworks.json` e liste TODAS as entradas dos domínios desta skill — `scaling` e `finance-projections` (mapa skill→domínio no README do índice) — cujo `use_in_skill` inclui a 12; entradas de outros domínios marcadas pra 12 (ex: `ops-scale-risk`, `affiliate-creator-channels`) contam igual. **O tamanho do domínio é o que o `frameworks.json` disser** — contagem citada em texto de skill nunca é fonte de verdade.
   - **As queries embutidas nas ETAPAS abaixo são o núcleo mínimo garantido daquela etapa, nunca o teto:** entrada relevante pra fase que não está embutida É PARA SER PUXADA do mesmo jeito. Critério de relevância é por FASE: "esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa.
   - **Rode a `best_query` exata de cada entrada relevante, com `deep=true`.** Não repita framework já puxado na mesma sessão (entradas duplicadas entre domínios apontam pro mesmo conteúdo — reuse o resultado).
   - **Antes de fechar cada ETAPA,** releia a lista enumerada e confirme: alguma entrada relevante ficou sem puxar? Se sim, puxe agora.

   Mínimo a carregar antes de montar qualquer plano:
   - **Scaling Protocol & Decision Tree (fonte primária 2026)** (rode `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`) — **a espinha única** de quando subir, segurar e descer (ETAPA 3.5). Carregue este primeiro.
   - **Reset da meia-noite** (rode `reset da meia-noite metade do spend real nunca budget nominal explode a conta`) — a regra de risco financeiro que acompanha TODA subida de budget (ETAPA 3.5)
   - **Taxonomia de Winners (Loser / KPI Winner / Spend Winner / Breakthrough)** (rode `breakthrough spend winner KPI winner losing ad classificação destino por categoria`) — define o gatilho de escala do pré-flight e da ETAPA 3
   - **Performance Gate Scaling (PGS) + The Three PGS Principles** (rode `Performance Gate Scaling PGS 3 principles trailing CPA automated rules` e `The three PGS principles never scale past margin trailing multi-day KPI campaign-based`) — nunca escalar além da margem; opera **dentro** do Scaling Protocol, não em paralelo a ele
   - **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM golden ratio LTV CPA COGS formula`) + **PSM Scaling Thresholds** (rode `PSM thresholds 1.3 aggressive 1.1 healthy breakeven zone scaling decision`) — leitura de diagnóstico (a 11 calcula)
   - **Three Budget Scaling Methods** (rode `Three budget scaling methods farmer 5% aggressive 50% business-led MRR`) — farmer 5% vs aggressive 50% vs business-led
   - **Three Reasons Scale Breaks** (rode `three reasons scale breaks unit economics funnel imbalance cash constraints can we spend more tomorrow`) — unit economics, funnel imbalance, cash
   - **Creative Diversity as a Scaling Mechanism** (rode `creative diversity as a scaling mechanism funnel balance video image 4Pi same position`) — combustível da escala

   Aprofunde — escala errada queima budget mais rápido que ad ruim.

### Breakeven é a âncora de tudo

Toda a matemática de escala desta skill ancora no **CPA de breakeven** e no **CPA máximo** (`max_cpa` = breakeven menos a margem de lucro desejada — é o setpoint do cost cap/bid cap, **distinto** dos `target_cpa_primary_2x/3x` da Skill 04, que são alvos de múltiplo de ROAS; o `max_cpa` é dirigido pelo lucro que o membro quer por pedido). **Fonte canônica do breakeven CPA (a MESMA das Skills 10 e 11):** `04-offer-builder/dados.json.unit_economics.weighted_margin_per_order`. Use esse campo direto, não re-derive. **Pós-07d:** se `manifest.target_cpa`/`manifest.breakeven_roas` existirem, eles carregam o recálculo mais recente (a 04 grava; a 07d atualiza quando as alavancas de checkout aplicadas mudaram a economics) — prevalecem sobre os valores do `dados.json` do 04, mesma precedência que a Skill 10 aplica. A performance real vem do `11-ad-analysis/dados.json`. Não invente — leia. Se faltar, pegue na ETAPA 1.

### Custo fixo antes de cortar spend (gate obrigatório — cânone unit-economics §4)

Breakeven CPA, ROAS e PSM enxergam custo **variável**. Nenhum deles enxerga o **custo fixo** (time, apps, ferramentas, aluguel, retainer de creator). Por isso, **antes de emitir QUALQUER recomendação de cortar spend motivada por queda de ROAS**, aplique `.claude/lib/unit-economics/README.md` §4 — a espiral do ROAS:

> Cortar spend pra "recuperar o ROAS" costuma **aumentar** o prejuízo, porque o custo fixo não encolhe junto. Sobra menos receita pra diluir a mesma base fixa. A reação certa às vezes é o contrário: **aumentar** spend aceitando ROAS menor, porque mais volume dilui melhor o fixo.

Como a skill 12 opera esse gate:

- **Com `15-finance-engine/dados.json` (fonte preferencial):** a conta já foi rodada pela 15, e o veredito dela **decide** — esta skill não decide localmente. Leia `roas_spiral.cut_spend_recommendation_allowed` e `roas_spiral.verdict` e grave `fixed_cost_gate` conforme o mapa:

  | `roas_spiral` da 15 | `fixed_cost_gate.roas_cut_recommendation` | O que a skill recomenda |
  |---|---|---|
  | `cut_spend_recommendation_allowed: true` (verdict `cut_spend_below_variable_breakeven`) | `cleared` | Corte autorizado — cada dólar a mais destrói margem de contribuição |
  | `verdict: "scale_up_accept_lower_roas"` | `blocked_by_roas_spiral` | **Não cortar.** A saída é subir spend até `roas_spiral.spend_to_breakeven_with_fixed`, aceitando ROAS menor |
  | `verdict: "covers_fixed_costs"` | `not_applicable` | Segurar — a operação cobre o fixo no nível de spend atual |
  | `verdict: "blocked_pending_fixed_costs"` | `blocked_pending_fixed_costs` | Fallback: vale o gate local abaixo |

- **Fixos conhecidos, sem a 15** (o membro informou o custo fixo mensal direto aqui) → rode a conta com eles na mesa e recomende o que o resultado disser, mesmo quando o resultado for subir spend com ROAS menor.
- **Fixos desconhecidos** → a recomendação **vira pergunta, não instrução**: "quanto você tem de custo fixo por mês (time, apps, ferramentas, aluguel)?". Sem esse número, a skill **não manda cortar** por queda de ROAS. Registre `fixed_cost_gate.roas_cut_recommendation: "blocked_pending_fixed_costs"` no `dados.json` e diga isso no relatório — e ofereça rodar `'finanças'` (skill 15), que fecha essa conta e devolve o número.
- **Isto não afasta a descida do cânone de escala:** CPA/ROAS **abaixo do breakeven por 24-48h persistentes** dispara o −20% do `ad-taxonomy` §5 do mesmo jeito (um dia ruim isolado não dispara) — ali cada pedido novo destrói margem de contribuição, e o fixo não muda essa conta. O gate governa o corte motivado por ROAS que caiu mas **ainda paga o variável**.
- **Rótulo obrigatório em todo output** (unit-economics §1): número que não subtraiu custo fixo é **margem de contribuição**, nunca "lucro". Se os fixos não foram informados, escreva isso em vez de omitir.

### PSM real (vs teórico) — LER, não recalcular

`psm_theoretical` vem do `04-offer-builder/dados.json` (baseado em AOV esperado).
`psm_real` é gravado SOMENTE pela skill 11 (ad-analysis) a partir de performance real. A skill 12 **LÊ `manifest.psm_real` + `manifest.psm_real_basis`** — fonte canônica — e **NUNCA recalcula** com outra fórmula.

Fórmula canônica (referência, calculada pela 11): `PSM = LTV / (CAC_real + COGS)`, onde `CAC_real` = ad spend do período ÷ clientes NOVOS do período (Shopify) e COGS é o somatório de `04-offer-builder/dados.json.cogs_breakdown` (não existe campo `cogs_total`).

**A base do número decide se a comparação vale — `manifest.psm_real_basis`:**
- **`"shopify_new_customer"`** — o denominador é o CAC real (ad spend ÷ clientes NOVOS do Shopify). É a ÚNICA base em que a comparação `psm_real` vs `psm_theoretical` (tolerância de 20%, abaixo) é válida — o teórico da 04 usa CAC.
- **`"platform_cpa_proxy"`** — o CPA de plataforma entrou como proxy do CAC. O número está **declaradamente otimista** (CPA de plataforma mistura recompra e atribuição inflada no denominador) e **não libera escala**: a comparação de 20% não se aplica nessa base. A skill exibe o motivo ao membro e **pede o CAC real** (ad spend do período ÷ clientes novos no Shopify, `new customer = TRUE`) — com o número na mão, re-rodar a 11, que regrava `psm_real` na base certa.
- **Campo ausente** (análise antiga da 11, produto legado) → **tratar como `platform_cpa_proxy`**: mesma régua, mesmo pedido de CAC real.

**Frameworks pra interpretar PSM (rode antes de decidir):**
- **Profitable Scaling Margin (PSM) — golden ratio** (rode `Profitable Scaling Margin PSM golden ratio LTV CPA COGS formula`) — a fórmula canônica e por que ela manda
- **PSM Scaling Thresholds** (rode `PSM thresholds 1.3 aggressive 1.1 healthy breakeven zone scaling decision`) — `≥1.3` escala agressivo, `~1.1` saudável (escala medido), perto de breakeven = não escala
- **Scaling Mindset Farmer vs Hunter (Andromeda)** (rode `scaling mindset farmer vs hunter Andromeda think bigger clarity not volume`) — qual mentalidade aplicar ao número do PSM

Compare `manifest.psm_real` contra `psm_theoretical` — **somente com `psm_real_basis: "shopify_new_customer"`** (proxy ou campo ausente: não compara nem libera; ver bloco da base acima). Se `|psm_real − psm_theoretical| / psm_theoretical > 0.2` (desvio > 20%):
- **psm_real < psm_theoretical**: economia de oferta pior que esperada; **NÃO escale** (nem o passo do protocolo, nem surf), revisar offer primeiro
- **psm_real > psm_theoretical**: oferta performa melhor que o esperado; pode escalar mais agressivo dentro do protocolo (teto de custo mais alto quando houver, surf mais ousado)

Use os **PSM Scaling Thresholds** como teto de agressividade: mesmo com `psm_real > psm_theoretical`, se o `psm_real` absoluto está perto de 1.0 (breakeven zone), escala só medido — margem fina não aguenta surf 10×.

Se `manifest.psm_real` estiver ausente, rode a skill 11 primeiro (quem o grava) — não estime aqui.

## Fluxo da Skill

### ETAPA 1 — Receber Panorama Atual

Primeiro, pré-popule dos artefatos: `11-ad-analysis/dados.json` (spend diário, CPA médio, CPM por conta, ROAS médio, AOV real, a classificação por criativo nas 4 classes do cânone §2 — ou `winners[]` a reclassificar — + `champions[]` com Post ID, se houver) + `04-offer-builder/dados.json` (breakeven CPA/ROAS) + `manifest.psm_real`. Só pergunte ao membro o que NÃO está nos artefatos.

Campos **necessários pra esta skill decidir** que os artefatos nem sempre cobrem — peça junto com o resto, numa mensagem só, apenas os que faltarem:

- **Custo fixo mensal** (time, apps, ferramentas, aluguel) — sem ele, o gate de corte por ROAS fica bloqueado (ver "Custo fixo antes de cortar spend"). **Não pergunte se já está gravado:** `15-finance-engine/dados.json.monthly_model.fixed_costs_monthly` e `manifest.fixed_costs_monthly` são a mesma verdade — existindo qualquer um dos dois, só confirme ("seus custos fixos ainda são US$ X/mês?").
- **Share de purchases em 7-day click** — é o gate click-based do Scaling Protocol. **Não pergunte se já está gravado:** a 11 grava `manifest.click_based_purchase_share` a cada análise — existindo, use direto (confirmando só se a última análise não for recente). Sem o campo (análise antiga da 11, produto legado), pergunte como hoje (Ads Manager → janela de atribuição). O mesmo recorte serve à segunda porta do gate: o ROAS calculado só com purchases click-based.
- **Fuso horário do ad account** — define quando é a "meia-noite" da regra de reset.
- **Caixa disponível hoje** — entra no check de float da ETAPA 6. Se a 15 rodou, `cash.cash_needed_90d` e `cash.runway_months` já respondem isso e a pergunta vira confirmação.

Se algo faltar (ex: cash disponível pra surf, que não vive em nenhum JSON), peça em UMA única mensagem só os campos faltantes:

"Confirmando o panorama: [valores lidos do 11-ad-analysis/dados.json + breakeven do 04]. Me falta só [campo(s) ausente(s)]."

Se `11-ad-analysis/dados.json` não existir, aí sim peça tudo: "Me dá o panorama atual: quanto gasta por dia, CPA médio, CPM médio, ROAS, AOV, e — por ad — **quanto cada um gastou** e **qual o CPA/ROAS dele comparado ao da campanha** (é isso que separa um breakthrough de um ad que só bate o KPI numa amostra pequena). E o breakeven CPA do produto." Não re-explique campos já preenchidos.

### ETAPA 2 — Classificar Estágio de Escala

Stage canônico vem do `manifest.stage` (`starter` | `validating` | `scaling`) — detecção pela rule `member-stage-awareness.md`. O stage dita **qual escola de escala recomendar como default** e a agressividade. A sub-fase de spend abaixo é DIAGNÓSTICO (informa intensidade), nunca substitui o stage canônico.

| Spend diário | Sub-fase de escala | Leitura |
|---|---|---|
| < $100/dia | Teste | Ainda achando breakthrough. Escala = mais criativo, não mais budget. |
| $100-500/dia | Tração | Breakthrough frágil. Passo do protocolo (+20%) com mão leve, sem surf. |
| $500-1K/dia | Escala Inicial | Breakthrough estável. Passo do protocolo a cada 24h enquanto os dois gates seguram. |
| $1K-5K/dia | Escala Agressiva | Passo do protocolo + surf possível, atenção diária e reset da meia-noite obrigatório. |
| $5K+/dia | Otimização | Unit economics, múltiplas contas, omnichannel. |

A sub-fase vive em `scale_phase` no `12-scale-engine/dados.json` — **NUNCA** em `manifest.stage`.

### ETAPA 3 — Análise de Prontidão (Pré-Requisitos)

Antes de aumentar spend, validar se o sistema aguenta. Falhar em qualquer um = identificar gargalo e resolver ANTES de escalar.

**Frameworks de prontidão (rode antes de aprovar escala):**
- **Three Reasons Scale Breaks** (rode `three reasons scale breaks unit economics funnel imbalance cash constraints can we spend more tomorrow`) — escala quebra por 3 motivos: unit economics fraco, funnel desbalanceado, cash constraint. Cada pré-requisito abaixo mapeia num desses.
- **Would It Hold at 3X Budget? (Mental Model)** (rode `would it hold at 3X budget mental model low spend high ROAS statistically insignificant`) — criativo com pouco spend e ROAS alto pode ser ruído estatístico. É o mesmo raciocínio que o cânone §2 formaliza no `KPI winner`: aplique este teste mental antes de chamar qualquer coisa de breakthrough.
- **Scaling Click-Based Data Gate** (rode `scaling click-based data gate 60% purchases view-through attribution 7-day click 1-day view`) — se a maioria das conversões é view-through (não click-based), o sinal de escala é frágil. O gate tem **duas portas** (`ad-taxonomy` §5 — qualquer uma libera): **≥ 60% das purchases em 7-day click**, OU **o ROAS calculado só com purchases click-based já bate o KPI sozinho**. As duas vermelhas, não sobe.
- **Teste de troca pra 7DC-only** (rode `campanha duplicada 7-day click only view-through inflado email blast returning customers`) — o diagnóstico quando o gate reprova: trocar a atribuição pra 7-day click only numa campanha **DUPLICADA** (nunca na de controle) e comparar. Se o "desempenho" some sem a view-through, o sinal estava inflado (email blast, returning customers contados como conversão do ad) — conserta atribuição na 07c antes de falar em escala.

| Pré-requisito | Critério | Se falhar |
|---|---|---|
| **Breakthrough provado** | ≥ 1 criativo classificado como `breakthrough` pelo cânone `ad-taxonomy` §2 (KPI do ad melhor que o KPI da campanha **e** puxa spend), estável por 3+ dias | **Volta pra 08** (mais criativo). `KPI winner` e `spend winner` **não** substituem: o primeiro não provou nada em escala, o segundo pede iteração |
| **Gate click-based (duas portas)** | ≥ 60% das purchases em 7-day click **OU** ROAS só de purchases click-based batendo o KPI sozinho (`ad-taxonomy` §5 — qualquer porta libera). Share lido de `manifest.click_based_purchase_share` (a 11 grava); sem o campo, o número que o membro trouxe na ETAPA 1 | Nas duas portas vermelhas, não escala com sinal view-through. Rodar o teste de troca 7DC-only (framework acima), revisar tracking na 07c e re-medir antes de subir budget |
| **PSM real ≥ teórico, em base válida** | `manifest.psm_real` não está > 20% abaixo do `psm_theoretical` **e** `manifest.psm_real_basis` é `"shopify_new_customer"` (campo ausente = proxy) | Abaixo do teórico → ajustar oferta (AOV, garantia, stack) ANTES de escalar. Base `platform_cpa_proxy` ou ausente → número declaradamente otimista, **não libera escala**: pedir o CAC real (ad spend ÷ clientes NOVOS do Shopify) e re-rodar a 11 |
| **Margem por pedido saudável** | `manifest.margin_warning` ≠ `true` (a Skill 04 grava `true` quando a margem ponderada fica < $20/pedido) | Segurar a escala VERTICAL e alertar o membro: com margem apertada, cada dólar de CPA acima do alvo come uma fatia grande do lucro — revisar oferta/pricing na 04 antes de subir budget |
| **CPA estável ou melhorando** | Trend dos últimos 3-7 dias estável ou descendo | Diagnóstico de fadiga (skill 11) antes de escalar |
| **CPM saudável na conta** | CPM dentro da faixa normal pro nicho/conta | CPM muito alto = problema de CONTA, não de produto. Testar o breakthrough em outra conta (skill 11) antes de escalar |
| **Creative pipeline ativo** | Batch novo a cada 1-2 semanas no ritmo de escala | Recomendar Skill 08 — escala consome volume de criativo |
| **Pixel/CAPI health** | EMQ ≥ 6.0 (escala 0-10 do Events Manager), sem events perdidos | Fix técnico (skill 07c) antes de escalar |
| **Cash flow pra COGS + spend** | Membro tem $ pra cobrir o gap entre spend (cobrado diário) e payout (Shopify 3-5 dias) | Ajustar pace de escala ao cash disponível (ver ETAPA 6) |
| **Volume do fornecedor confirmado** | `sourcing/dados.json` → `calendar.volume_confirmation_30_60_90` preenchido (a 01b ETAPA 12 grava — existindo, use e NÃO re-pergunte) ou confirmação escrita equivalente informada pelo membro | Sem confirmação de volume, escalar contra ruptura de estoque é **risco declarado**: avisar e pedir a confirmação por escrito ao fornecedor (ou rodar a 01b ETAPA 12, que fecha exatamente isso). Sourcing nunca rodou → pergunta de hoje, ao membro. Ponto de recompra operacional na ETAPA 6 |

Pra cada pré-requisito que falha, documente o bloqueio e recomende ação específica. **Breakthrough provado é eliminatório** — sem ele, a skill não monta plano de escala, manda de volta pra 08. O membro que chega com um `KPI winner` bonito ouve isso explicitamente: o ad bate o KPI numa amostra pequena e não puxa spend, então não há o que escalar ainda.

### ETAPA 3.5 — Scaling Protocol (a espinha única de toda subida e descida)

Antes de escolher escola, fixe a régua. **Toda mudança de budget desta skill obedece ao Scaling Protocol do cânone `.claude/lib/ad-taxonomy/README.md` §5.** As escolas da ETAPA 4 são variantes de **intensidade** dentro dele — mudam o quanto e com que mão o membro empurra, nunca os gates. Onde uma escola sugerir ritmo que conflita com o protocolo, **o protocolo vence**.

Sistemas a carregar antes de montar o plano: `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`, `reset da meia-noite metade do spend real nunca budget nominal explode a conta` e `the fix is outside the ad account pesquisa avatares mecanismos ofertas novas plateau`.

> ⚠️ **REGRA DE RESET DA MEIA-NOITE (crítica — risco financeiro real)**
>
> **Ao ajustar o budget à meia-noite, o novo valor é ~50% do que a campanha REALMENTE GASTOU no dia — nunca 50% do budget nominal que ficou setado na tela.** (cânone `ad-taxonomy` §5.)
>
> Um budget setado em $1.600 que gastou $300 vira **~$150** no dia seguinte, não $1.600. Sem isso, o Meta faz *pacing* pra gastar o nominal inteiro no dia seguinte: o membro dorme com um teste de $300 e acorda com $1.600 queimados sem ninguém olhando.
>
> **Vale para TODA escola e TODO salto de budget desta skill** — o surf da A, a alimentação da B, o doubling da C. Sempre que a skill instruir uma subida, ela instrui **junto** o valor de reset do dia seguinte. Grave em `dados.json.midnight_reset`.
>
> A meia-noite que conta é a do **fuso do AD ACCOUNT**, não a do membro — confirme o fuso na ETAPA 1 antes de dar horário.
>
> Exceção única: dia excepcional em que o gasto real bateu o KPI com folga → pode manter o gasto real como budget do dia seguinte, em vez da metade. Nunca acima do gasto real.

**Ad log — verificar antes, registrar no ato (cânone `.claude/lib/ad-log/README.md`):**

- **Antes de qualquer degrau, leia `workspace/[produto]/ad-log.md`:** qual foi a última mudança de budget e há quanto tempo — **o gate de 24h entre degraus é verificado ali, não de memória.** Mudança recente cujo efeito ainda não foi lido é motivo pra segurar o passo mesmo com gates verdes.
- **Toda mudança de budget que esta skill instrui ou executa** — degrau de ±20%, reset da meia-noite, surf e o recuo do surf, duplicação em ABO, graduação pra ASC — **é registrada no MESMO momento da execução** (nunca "depois"), uma linha por mudança no formato do cânone: `| YYYY-MM-DD HH:MM | entidade | mudança | executor | motivo curto |`, com valores antes → depois ("budget $200→$240") e executor `skill-12` (ou `membro`, quando ele relata mudança manual). Arquivo inexistente → criar com o cabeçalho da tabela na primeira escrita. **Mudança executada e não logada é bug de processo.**

**Subida (os dois gates são cumulativos — falhou um, o passo é zero):**

1. **Gate de consistência:** a campanha precisa estar **48-72h acima do target** antes do primeiro aumento. Um dia bom não abre escala.
2. **Gate click-based (duas portas — qualquer uma libera, cânone §5):** só sobe se **≥ 60% das purchases aparecem em 7-day click** OU se **o ROAS calculado só com purchases click-based já bate o KPI sozinho**. Sinal majoritariamente view-through que não passa em nenhuma das duas não sustenta escala. (Share: `manifest.click_based_purchase_share`, gravado pela 11; sem o campo, o número da ETAPA 1.)
3. **Passo: +20%.** Passado o primeiro aumento, pode repetir **a cada 24h** enquanto os dois gates seguirem verdadeiros — e as 24h desde o degrau anterior se conferem no `ad-log.md`, não de memória.
4. Sem os 48-72h, ou com o gate click-based vermelho nas duas portas, não existe atalho por entusiasmo: **o passo é zero** e a ação vai pro item 7 — salvo as **duas exceções do cânone** logo abaixo.

**As DUAS exceções do protocolo (cânone §5 — são da fonte e valem sobre os degraus; nenhuma outra existe):**

- **(a) Promo com data-fim** (BFCM, lançamento, liquidação com prazo): entra **direto no budget planejado da promo** — não sobe em degraus de +20%, porque a janela termina antes de os degraus chegarem lá. O que protege a promo é o **surf + reset da meia-noite** (presença ativa no dia; à meia-noite, ~50% do gasto REAL), não o protocolo. Terminada a promo, o budget volta ao trilho dos degraus.
- **(b) "New reason to be scaling"** — oferta nova, breakthrough novo, sazonalidade que mudou a demanda: **reinicia a leitura do protocolo.** O histórico anterior de degraus não trava o passo novo — os 48-72h acima do target contam a partir do motivo novo, não do degrau velho.

Exceção usada → registre em `dados.json.scaling_protocol.active_exception` e no `ad-log.md` (motivo curto = a exceção, ex: "promo início" / "new reason: oferta nova").

> **Teto de escala medido (quando `15-finance-engine/dados.json` existir):** a 15 projeta o resultado operacional em faixas crescentes de spend e publica `payback.scale_ceiling_monthly_spend` — o ponto em que o resultado **para de subir e começa a cair**. Enquanto os passos de +20% acumulados estiverem abaixo desse teto, o protocolo roda normal; ao chegar perto dele, o passo é zero **mesmo com os dois gates verdes**, e a ação vai pro item 7 (fora do ad account). Escreva o teto de forma acionável no relatório: *"não passar de US$ X/mês de spend até o CAC melhorar"*. **Sem o arquivo da 15, nada muda:** o teto continua sendo descoberto empiricamente — a escola sobe até quebrar o CPA e recua pro último nível bom.

**Descida:**

5. **Abaixo do breakeven por 24-48h persistentes → −20%** (cânone §5 — **um dia ruim isolado não dispara descida**; a leitura é da janela, não do susto do dia). Cortar, não desligar: matar o top spender reseta o aprendizado (Spend Redistribution Framework, ETAPA 10).
6. **Antes de qualquer corte motivado por queda de ROAS que ainda paga o variável**, roda o gate de custo fixo (ver "Custo fixo antes de cortar spend", unit-economics §4). Fixos desconhecidos → a saída é pergunta, não instrução de corte.

**Quando estagna (o passo que impede o membro de girar botão à toa):**

7. Se o budget não sobe mais sem quebrar o CPA, **a ação certa está FORA do ad account**. Nessa ordem:
   - **Batch novo de criativo** (skill 08) — é o gargalo na maioria esmagadora dos platôs;
   - **Funil inteiro conferido por bug** — código de carrinho removido, produto fora de estoque, checkout quebrado, pixel caído. Checar **diariamente** depois de qualquer queda brusca, antes de culpar o leilão;
   - **Oferta re-testada** (skill 04) e **página re-trabalhada** (07a/07b);
   - **Learnings processados** — o que os breakthroughs atuais têm em comum e o que ainda não foi testado;
   - **Sub-avatar esgotado → Chunk Up** (rode `plateau chunk up desejo central amplo calendario de desejos nichar acha broad escala`) — quando o platô é de mercado (o ângulo nichado do sub-avatar já foi "snipado" e não rende mais), a saída é **subir UM nível de abstração**: falar ao desejo central mais amplo por trás do sub-avatar e deixar o broad achar o público. Nichar de novo só quando o patamar novo platôar por sua vez. O briefing do nível novo vai pra 08 via `scale-directives.md`.

   Mexer em bidding, budget e estrutura quando o gargalo é criativo ou oferta só troca a forma do prejuízo. Registre a estagnação em `dados.json.scaling_protocol` e roteie explicitamente (ver "Quando 12 recomenda voltar para 08").

### ETAPA 4 — As 3 Escolas de Escala (variantes de intensidade dentro do protocolo)

As três escolas abaixo são **variantes de intensidade do Scaling Protocol da ETAPA 3.5**, não caminhos alternativos de mesmo nível: mudam o apetite e a mão de obra, mas nenhuma delas dispensa os gates (48-72h acima do target, gate click-based de duas portas, −20% só após 24-48h persistentes abaixo do breakeven, reset da meia-noite). Não há uma "certa" — há a certa pro **stage** e pro **apetite de risco** do membro. **Apresente as três ao membro** (tabela curta, no report_language), marque a recomendada pro stage dele, e deixe ele escolher.

> **Bidding em escala — correção factual (a "regra de ouro" anterior desta skill estava errada):** escala **não** exige cost cap nem bid cap, e Max Conversion **não** é só pra teste. A campanha principal que escala alto roda **maximize number of conversions (highest volume), bid strategy padrão** — é com esse lance que uma campanha chega a **$40 mil/dia**. O que muda de teste pra escala é o volume de sinal e a régua de decisão, não o tipo de lance.
> - **Highest volume** → default da campanha principal, em teste **e** em escala.
> - **Cost per result goal (cost cap)** → ferramenta da **zombie/graveyard campaign** (extrair ROI de ads reprovados/mortos com teto de custo), não da campanha que escala. Se o membro quiser montar essa camada, rode `zombie graveyard campaign cost per result goal ads reprovados milk the creative`.
> - **Bid cap** → opção com **ressalva declarada: bid caps têm issues.** Só com folga de margem, nunca como default. A Escola B usa bid cap por desenho — apresente-a com essa ressalva na mesa.
>
> As escolas A e B seguem disponíveis porque a mecânica de duplicação e de campanha única alimentada é real e útil. O que sai é a afirmação de que escala **obriga** um teto de lance.

**Sistemas nomeados que sustentam o ritmo das três escolas (rode os relevantes à escola escolhida):**
- **Performance Gate Scaling (PGS) + The Three PGS Principles** (rode `Performance Gate Scaling PGS 3 principles trailing CPA automated rules` e `The three PGS principles never scale past margin trailing multi-day KPI campaign-based`) — nunca escala além da margem, usa trailing multi-day KPI (não 1 dia), decisão por campanha. Opera **dentro** do Scaling Protocol (ETAPA 3.5): onde os dois discordarem de ritmo, o protocolo manda.
- **Three Budget Scaling Methods** (rode `Three budget scaling methods farmer 5% aggressive 50% business-led MRR`) — farmer (+5%/dia, conservador), aggressive (+50%, troca volatilidade por velocidade), business-led (escala atrelada a MRR/cash). Mapeia direto: C≈farmer, A≈aggressive.
- **Scaling Protocol & Decision Tree (fonte primária 2026)** (rode `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`) — 48-72h acima do target antes de subir, depois escala a cada 24h enquanto segura. Árvore de decisão de quando subir vs segurar vs recuar.
- **Sliding Scale Rules (PGS Advanced)** (rode `sliding scale rules PGS different CPA targets spend levels 60 55 52 50`) — fundamenta os **caps decrescentes da Escola A** ($50/$45/$40/$35): cada nível de spend tem um CPA target diferente.
- **Soft Surfing (PGS Advanced)** (rode `soft surfing additional daily 5% increase CPA far below target accelerate growth`) — versão controlada do "surf de manhã" da Escola A: +5% extra quando o CPA está MUITO abaixo do target. Use isto pra calibrar o surf antes do 10× agressivo.
- **Scale-Down Rules (PGS reverse)** (rode `scale-down rules decrease budget 20% 7-day CPA exceeds target safety net`) — quando o CPA de 7 dias estoura o target, corta budget 20%. É a rede de segurança das três escolas (espelha o "recolhe quando quebra" da Escola A e o "volta pro último nível bom" da Escola C). **Hierarquia:** o gatilho duro do cânone §5 é **abaixo do breakeven por 24-48h persistentes → −20%** (um dia ruim isolado não desce); corte motivado por ROAS que ainda paga o variável passa antes pelo gate de custo fixo (ETAPA 3.5, item 6).
- **Spend Redistribution Framework (Don't Kill the Top Spender)** (rode `spend redistribution framework do not turn off top spender ROAS drops higher budget`) — quando o ROAS cai ao subir budget, NÃO desliga o top spender (matar quebra o aprendizado). Crítico pra Escola B (nunca desativa criativo) e pra surf que quebrou.
- **Levels of Scaling (Zero-to-50K to 100K/day)** (rode `levels of scaling zero to 50k 100k per day one campaign CBO raw content ASC whitelisting segmented`) — estrutura de campanha por nível de spend (one-campaign → CBO → ASC → whitelisting → segmented). Mapeia a `scale_phase` da ETAPA 2 num blueprint de estrutura real.

#### Escola A — Cost-Cap Duplication + Surf de Manhã (mais agressiva, mais upside)

> Variante de **intensidade alta** do protocolo. Usa cost cap fora da zombie campaign: legítimo como mecânica de duplicação com tetos decrescentes, desde que o membro saiba que a campanha principal de maior escala roda **highest volume** (bloco de bidding acima) — o cap aqui é escolha de controle, não requisito de escala.

A mecânica:

1. **Isola o breakthrough numa campanha 1-1-1** — 1 campanha, 1 ad set, 1 criativo. Limpo, sem ruído. Se 2 criativos chegaram a breakthrough, uma estrutura 1-1-1 pra cada.
2. **Bidding = Cost Cap** (custo por resultado), setado **~10% abaixo do CPA de breakeven**. Ex: breakeven $55 → cost cap inicial **~$50** (deixa ~9% de lucro por pedido nesse teto: `lucro/pedido = breakeven − cap = $5` ≈ 9% da margem de $55). O cost cap é o teto: o Facebook só gasta enquanto consegue resultado abaixo dele. **São os caps decrescentes do passo 3 que vão exigindo mais lucro por pedido** — quanto mais baixo o cap, maior a margem por venda (ex: cap ~$38 ≈ 30% de lucro/pedido).
3. **Duplica o 1-1-1 várias vezes com caps DECRESCENTES** — $50, $45, $40, $35… de $5 em $5. Cada duplicata com o mesmo budget de teste (ex: $160/dia). A lógica: cada cap mais baixo pega a eficiência num ponto diferente do leilão; o Facebook acha gasto onde dá pra entregar dentro daquele teto. Quanto mais baixo o cap, mais difícil gastar, mas mais barato o resultado.
4. **Surf de manhã (a parte agressiva).** Ao acordar, olhe as campanhas. Uma com CPA **muito** abaixo do alvo (ex: 2 vendas, gastou $30, CPA $15 num produto de breakeven $55) está pedindo budget. **Joga o budget 10×** ($160 → $1.600), observa 2-3h.
   - Continua vendendo dentro do alvo → **sobe mais** ($3k, $30k — não gasta tudo, gasta o que conseguir vendendo).
   - Gastou ~$150 a mais SEM venda nova, ou o CPA passou do breakeven → **derruba o budget de volta IMEDIATAMENTE**. Não espera prejuízo grande. Ao baixar, a campanha frequentemente volta a vender no nível anterior.
   - Sem regra fixa de %. Vai pelo que a campanha entrega naquele momento. É monitoramento ativo, não set-and-forget.
   - **À meia-noite, aplique a REGRA DE RESET (ETAPA 3.5): o budget do dia seguinte é ~50% do que a campanha REALMENTE gastou, nunca o nominal que ficou na tela.** Surfou até $30k mas gastou $4k → o dia seguinte começa em ~$2k. Deixar o nominal de pé é o erro que transforma um dia bom numa conta queimada enquanto o membro dorme. Toda instrução de surf desta skill sai com o número do reset junto.

   > Surf é "navegar a onda": quando o leilão tá te dando resultado barato, você empurra o máximo de budget enquanto a onda segura, e recolhe na hora que ela quebra. Exige presença (olhar a cada 2-3h num dia de surf). Por isso é escola de **scaling**, não de starter.

**Quando usar:** stage `scaling`, breakthrough muito estável, membro com tempo pra monitorar de manhã e estômago pra volatilidade. Maior upside, maior atenção — e reset da meia-noite todo santo dia.

#### Escola B — Bid Cap "Campanha Monstro" (mais controlada, mão menos pesada)

> Variante de **intensidade média** do protocolo, construída sobre bid cap — e bid cap carrega a **ressalva declarada do bloco de bidding: bid caps têm issues.** Apresente a escola com essa ressalva explícita: ela troca upside por controle, e o controle vem de um mecanismo de lance reconhecidamente problemático. Se o membro quer só volume estável sem esse risco, a campanha em **highest volume** rodando o protocolo entrega o mesmo crescimento sem o teto de lance.

A mecânica:

1. **1 conta de anúncio = 1 campanha de Bid Cap.** (Roda 1 dia de Max Conversion antes, só pra a conta pegar mini-dados de cliente e ajudar o bid cap a achar gasto.)
2. **Setup:** `bid cap = seu CPA máximo`; `budget = 100× o CPA máximo`. Ex: CPA máximo $30 → bid cap $30, budget diário $3.000. **Não gasta tudo** — o budget alto é só espaço; o bid cap é o teto real de custo por resultado.
3. **Alimenta a MESMA campanha continuamente** com mais ad sets de criativo (≈5 criativos por ad set). A cada 1-2 dias, adiciona um ad set novo com criativos novos. Pode chegar a 20 ad sets / 200 criativos numa única campanha "monstro".
4. **NÃO desativa criativos.** Deixa o Facebook varrer todos atrás de CPA abaixo do bid cap. O algoritmo concentra gasto onde acha resultado e ignora o resto (criativo ruim simplesmente não gasta — você não precisa matar manualmente).

**Risco e safeguard:** adicionar ad set novo numa campanha que está ótima pode **travar a entrega** (resetar o aprendizado). Se a campanha tá voando, **prefira abrir OUTRA conta/campanha** em vez de arriscar mexer na boa. Baixar o bid cap de $2 em $2 pra apertar o CPA é possível, mas arriscado (também pode travar) — faça só com folga. Isso ficou AINDA mais verdadeiro desde abril/2026: edições antes consideradas "seguras" (ajuste pequeno de bid, tweak de criativo) passaram a resetar o learning com mais facilidade — duplicar/abrir conta nova em vez de editar campanha boa é a jogada default da era.

**Quando usar:** stage `validating` ou `scaling` que quer crescimento estável com pouca mão. Menos volatilidade que a Escola A, menos upside explosivo.

#### Escola C — Budget-Doubling a cada 3 Dias (mais simples)

A mecânica:

1. Roda a campanha (highest volume é o default — cost/bid cap só se o membro quiser teto, com as ressalvas do bloco de bidding).
2. **Dobra o budget a cada 3 dias** enquanto o ROI/CPA segura: $100 → $200 → $400 → $800…
3. Quando quebra num nível (CPA estoura o target / ROI fica negativo), **volta pro último nível bom** e segura ali. Esse é o seu teto atual ("achei meu teto").
4. Pra subir de novo depois: melhora o que está fora do Ads Manager (criativo novo da 08, oferta melhor da 04) e tenta dobrar de novo a partir do teto.

> Os 3 dias importam: dão dado suficiente pro Facebook estabilizar antes de cada salto e evitam reagir a um pico de 1 dia. É a versão "sem ficar no teclado" de escala — não exige surf nem gestão de N campanhas.

**Quando usar:** stage `starter` (e `validating` no começo). É a mais fácil de operar, a mais perdoável, e ensina o membro a achar o teto sem queimar conta.

#### Tabela de escolha (apresentar ao membro)

| Escola | Como funciona em 1 frase | Mão de obra | Volatilidade | Default pra stage |
|---|---|---|---|---|
| **C — Budget-doubling 3d** | Dobra a cada 3 dias até quebrar, volta pro último nível bom | Baixíssima | Baixa | **starter** |
| **B — Bid cap monstro** | 1 campanha, budget 100× CPA, bid cap = CPA máx, alimenta com ad sets, nunca desativa | Baixa-média | Média | **validating** que quer controle — com a ressalva "bid caps têm issues" |
| **A — Cost-cap + surf** | Isola o breakthrough num 1-1-1, duplica com caps decrescentes, surfa de manhã e reseta à meia-noite sobre o gasto real | Alta (olhar 2-3×/dia) | Alta | **scaling** |

Recomendação por stage (default, não trava): **starter → C**; **validating → C com passo do protocolo, ou B se quiser controle** (com a ressalva de bid cap); **scaling → A** (mais upside, mais atenção). Em qualquer stage, a campanha principal em **highest volume** rodando o protocolo puro é alternativa legítima — nenhuma escola é obrigatória pra escalar.

Pergunte ao membro qual escola quer rodar. Se ele não tiver opinião, vá com o default do stage e explique por quê. Registre a escola escolhida no `12-scale-engine/dados.json` (`scaling_school`) — junto com o bidding efetivo em `dados.json.bidding`, porque a escola é a intensidade, o bidding é uma escolha separada.

**Graduação pra ASC — Advantage+ Sales (nível $1K+/dia sustentado):** as três escolas seguem sendo o playbook até aí. Acima disso, o desenho operacional 2026 em ecom é **ASC como campanha principal + a estrutura de teste da Skill 10 (1 campanha CBO → N ad sets, 1 por conceito → 3 ads) virando sandbox de teste de criativo** (breakthroughs promovidos pra ASC). Requisitos práticos: volume de conversão alto e 6-10 criativos vivos. Dois detalhes que mudam o setup: (1) configurar o **existing-customer budget cap** (reintroduzido em março/2026) pra manter o ASC prospectando em vez de virar retargeting disfarçado; (2) dentro do ASC não existe bid cap — o controle de custo é o **cost-per-result goal**. Números de lift divulgados (4.5x ROAS etc.) vêm de fontes pró-automação — trate como direcionais, valide com o SEU CPA.

**Variante condicional — value optimization (só se o AOV varia de verdade):** se o spread de AOV entre pedidos passa de ~30% (bundle/subscription/upsell forte pós-07d), otimizar por CPA uniforme sub-otimiza — paga o mesmo por pedido de $40 e de $120. Nesse caso, teste **ROAS goal + value rules** numa campanha DUPLICADA (nunca na campanha de controle), com 14+ dias de teste antes de julgar. Pra produto único de preço estável (a maioria dos membros), ignore esta variante: otimizar por CPA — no lance padrão (highest volume) ou com teto, conforme a escola — segue superior em simplicidade e controle.

### ETAPA 4.5 — Quando o budget trava a entrega → abrir nova conta

Padrão que aparece em todas as escolas: às vezes você sobe o budget e a entrega **não acompanha** — a campanha não gasta o novo budget, ou trava o aprendizado e o CPA dispara. Antes de concluir "atingi meu teto", diagnostique:

1. **É a conta ou o produto?** CPM muito acima do normal pro nicho é sinal de **conta cansada**, não de produto morto. O mesmo criativo pode dar CPM $30 numa conta e $100 noutra (a skill 11 mede isso).
2. **Se for a conta** → a jogada legítima é **abrir uma conta de anúncio nova** e rodar o mesmo breakthrough lá. Ter contas de anúncio organizadas (1 por produto, mais contas de reserva pra resiliência) é organização e contingência legítimas — embaralhar 2 produtos numa conta confunde o aprendizado, então separar é boa prática.
3. **Na Escola B**, lembre: se a campanha boa não aguenta mais um ad set sem travar, **abra outra conta/campanha** em vez de arriscar a que está performando.

> **Limite ético (inviolável):** esta skill encode SÓ a mecânica legítima de organização de conta e campanha. **NÃO** ensina nem recomenda comprar BM/contas de terceiros, "farmar" contas, contingenciar perfil-dono-vs-anunciante pra driblar ban, produto réplica ou cloaking. Essas táticas derrubam a conta da marca real e brigam com a tese brand-building do Aura. Abrir uma conta de anúncio nova e legítima dentro do seu próprio Business Manager é resiliência; farmar conta pra driblar política não é — e não tem suporte aqui.

### ETAPA 4.6 — Execução opcional via Meta MCP (criar em PAUSED)

A escala não precisa ser só instrução manual — o membro é não-técnico, e as operações das escolas são numerosas e repetitivas. Se ele topar, criar a estrutura da escola escolhida via a MESMA cascade da Skill 10 ETAPA 6 (oficial `mcp__meta__ads_*` → Pipeboard `mcp__meta-ads__*` → manual — detecção por prefixo, ver `.claude/lib/mcp-detect/README.md`):

- **Escola A:** as campanhas 1-1-1 do breakthrough, duplicadas com os caps decrescentes calculados ($50/$45/$40/$35…), todas em `status: PAUSED`. O surf em si continua manual — é monitoramento ativo por definição.
- **Escola B:** a campanha bid cap (bid = CPA máximo, budget 100×) em PAUSED; os ad sets novos de alimentação também nascem PAUSED a cada adição.
- **Escola C:** sem estrutura nova pra criar — só o plano de doubling (mudança de budget é sempre aprovada pelo membro, nunca automática).
- **Automated Rules opcionais** (scale-down −20% quando a performance fica abaixo do breakeven **por 24-48h persistentes** — a janela do protocolo da ETAPA 3.5, nunca o susto de 1 dia; PGS): criar **DESATIVADAS** — nenhuma rule executa ação automática até o membro revisar e ativar no Ads Manager.
- **A regra de reset da meia-noite NÃO vira automação.** Ela depende do gasto REAL do dia, que só se conhece no fim do dia — a skill entrega o número calculado e o membro aplica. Nenhuma automated rule pode setar budget nominal sozinha.

**Regras invioláveis (as mesmas da 10):** tudo nasce PAUSED/desativado; o membro revisa e ativa; a skill NUNCA ativa nada sozinha. Gravar os IDs criados em `12-scale-engine/dados.json.mcp_execution` — e **registrar cada ação executada via MCP no `workspace/[produto]/ad-log.md` na MESMA execução** (cânone ad-log: campanhas/ad sets criados em PAUSED, automated rules criadas desativadas — executor `skill-12`). Sem MCP conectado → entregar o passo-a-passo manual formatado campo a campo (como sempre). Se a criação falhar (rate limit/auth), aplicar `.claude/rules/emergency-escape-paths.md` ES6.

### ETAPA 5 — Credibilidade da Loja (lever de conversão antes de escalar)

Escalar budget joga tráfego mais frio na loja. Se a loja não parece confiável, a conversão cai e a escala morre. Antes de empurrar volume, confirme (nota rápida, não bloqueio):

- Página de Facebook + Instagram com seguidores reais e posts (não vazio).
- Reviews/avaliações reais (~100, em inglês) na PDP — prova social.
- Highlights/destaques de confiança: brand story / About, feedback, selos legítimos.
- **Gestão de comentários é o mais importante.** Comentário negativo num post de ad fica visível pra todo mundo que vê o anúncio e derruba conversão direto. Responder ou deletar comentários ruins é manutenção diária de escala.

> **Honestidade:** foco em prova social **real**. Comprar seguidor/comentário falso em volume pode atrapalhar (parece fake, arrisca a conta) — não recomendado. Se a credibilidade da loja está fraca, isso é gargalo de conversão a resolver na 07a/07b/07d antes de gastar mais em ads.

### ETAPA 6 — Cash Flow (o gargalo invisível de escala)

Ads cobram **diário**; o payout do Shopify chega em **3-5 dias** (Stripe ~2 dias). Quando você escala, esse descasamento vira um buraco de caixa que cresce com o budget. Escalar sem cobrir o gap é a forma mais comum de quebrar uma marca que estava lucrando.

**Payout hold / rolling reserve (cenário obrigatório pra loja nova):** os 3-5 dias são o lag NOMINAL — processadores seguram mais quando a conta é nova ou o volume dá spike (exatamente o que a escala provoca). Shopify Payments/Stripe podem aplicar **rolling reserve** (reter uma % de cada payout por semanas) ou **hold temporário** de dias a semanas enquanto revisam o risco da conta. Pra loja com **menos de ~90 dias de processamento** (ou no primeiro spike grande de volume), use `payout_lag_days` conservador de **7-14 dias** no check de float abaixo — não os 3-5 nominais — e confirme no dashboard do processador se há reserve ativa antes de autorizar qualquer escala agressiva. Escalar assumindo payout de 3 dias com uma reserve de 30% ativa é o furo de caixa clássico da loja nova.

**Frameworks de cash flow e teto de risco (rode antes de autorizar escala agressiva):**
- **Total Loss Investment Concept** (rode `total loss investment concept aggression ceiling zero additional revenue acceptable loss`) — define o teto de agressividade: quanto você aceita perder se o gasto extra trouxer zero receita nova. É o limite duro do surf da Escola A e do doubling rápido da Escola C.
- **Fractional Banking** (rode `fractional banking borrow against future revenue rolling repeat purchase cash flow scale negative CPA`) — como financiar escala emprestando contra receita futura/repeat purchase quando o cash gira mais devagar que o spend. Pré-condição: LTV/repeat real provado (não chute).
- **Going Negative on CPA (LTV-Funded Acquisition)** (rode `going negative on CPA LTV rebills Agora upfront capital dominate market acquire more customers`) — só pra `scaling` com LTV/rebill comprovado e capital de giro: aceitar CPA acima do breakeven na primeira compra porque o LTV banca. **Nunca** ofereça isto a starter/validating sem dado de repeat real.
- **Great Wall of Death — as 3 perguntas de cash conversion** (rode `great wall of death cohort fica positivo antes do boleto vencer cash-out date`) — o teste de caixa da escala: a coorte fica positiva **antes** da data em que a conta vence (o cash-out date)? Se a resposta é não, a escala está financiando prejuízo com prazo. Quem fecha essa conta com os números do membro é a **skill 15** (`'finanças'`) — o `cash.cash_needed_90d` e o `cash.runway_months` dela já carregam essa leitura; sem a 15, use as 3 perguntas como check qualitativo antes de autorizar escala agressiva.

**Check obrigatório antes de qualquer escala > 2× em < 7 dias:**

- [ ] Float de cash disponível ≥ `1.5 × daily_budget_target × payout_lag_days`
- [ ] Fornecedor consegue entregar o volume de unidades projetado em 30/60/90 dias? **Leia primeiro `sourcing/dados.json` → `calendar.volume_confirmation_30_60_90`** (a 01b ETAPA 12 grava a confirmação escrita — existindo, use e não re-pergunte). Sourcing rodou mas o campo está vazio → avisar que escalar sem confirmação de volume é **risco declarado de ruptura de estoque** e pedir a confirmação ao fornecedor (ou rodar a 01b ETAPA 12). Sourcing nunca rodou → pergunta de hoje (confirmação escrita)
- [ ] Estoque longe do ponto de recompra: com `calendar.reorder_point_days` na mão, **perto desse ponto o pedido de reposição é colocado, o rastreio acompanhado e a escala agressiva SEGURA** até o estoque novo chegar — subir budget contra a ruptura só antecipa o dia sem estoque
- [ ] Backup payment method se o Meta bloquear o cartão principal?

**Cálculo de gap projetado:**
```
cash_gap_projected = (daily_budget × 30 × burn_multiplier) − (daily_revenue_projected × 30 × (1 − payout_lag/30))
onde burn_multiplier = 1.3 (margem de segurança)
```

> **Quando `15-finance-engine/dados.json` existir, o número de caixa vem de lá — esta skill não estima.** A 15 monta a necessidade de caixa com o custo fixo dentro, o desembolso de estoque e a margem de contribuição acumulada do período (ETAPA 6 dela), coisas que a fórmula acima não enxerga. Leia e use:
> - **`cash.cash_needed_90d`** no lugar do `cash_gap_projected` estimado aqui. É a necessidade de caixa de 90 dias já com o fixo somado.
> - **`cash.float_stack.total_float_days`** no lugar do `payout_lag_days` isolado no check de float acima: com o stack de float ativo, o ad spend só deixa a conta lá na frente, e a diferença entre as duas linhas (`cash_needed_90d` vs `cash_needed_90d_with_float_stack`) costuma ser o que separa "não dá pra escalar" de "dá".
> - **`cash.runway_months`** como a leitura de prazo: quantos meses o caixa aguenta o plano de escala que está sendo montado.
>
> **Sem o arquivo da 15, nada muda:** a fórmula local acima continua valendo integralmente, com o `payout_lag_days` conservador de loja nova. Registre em `cash_flow.source` qual das duas fontes produziu o número.

Se `cash_gap_projected` (ou o `cash.cash_needed_90d` da 15, quando existir) **> 50% do cash disponível**, **NÃO autorize** escala agressiva (surf 10×, doubling rápido). Volte pra ritmo conservador (Escola C devagar, ou o passo de +20% do protocolo sem surf) até o caixa girar.

**Regra dura:** nunca escala > 2× o budget atual em < 7 dias se o cash não cobre o gap — independente de quão bom o sinal está. O surf da Escola A respeita isso: surfa com o que tem, recua na hora.

### ETAPA 7 — Projeção Realista 30/60/90 (base + pessimista + cash flow)

Construa dois cenários usando breakeven, AOV e PSM reais.

**Base (premissas: escola escolhida rodando, pipeline de criativo ativo, CPA estável):**

| Mês | Spend/dia alvo | Receita/dia (AOV × vendas) | Margem mensal estimada |
|---|---|---|---|
| Mês 1 | $[atual × 1.5-2] | $[calculado] | $[margem × 30] |
| Mês 2 | $[atual × 2-3] | $[calc] | $[margem] |
| Mês 3 | $[atual × 3-4] | $[calc] | $[margem] |

Use AOV real do `11-ad-analysis/dados.json` e breakeven do `04-offer-builder/dados.json`. Não infle: na Escola A o crescimento é em saltos (surf), na C é dobra a cada 3 dias até o teto — modele o caminho realista da escola escolhida.

> **Camada de custo fixo na projeção (quando `15-finance-engine/dados.json` existir).** A tabela acima projeta **margem de contribuição**, não lucro (unit-economics §1). Com `monthly_model.fixed_costs_monthly` na mão, acrescente **uma coluna**: `Resultado operacional mensal = margem de contribuição do mês − custo fixo mensal` — o único número da projeção que pode ser chamado de lucro. Some duas linhas de leitura ao redor da tabela: o **teto de escala** (`payback.scale_ceiling_monthly_spend`) marcando até onde a curva de spend pode ir, e o **runway** (`cash.runway_months`) dizendo quantos meses o caixa banca esse caminho. O custo fixo é o MESMO valor nos três meses — ele não cresce porque o budget cresceu, e é exatamente por isso que mais volume melhora o resultado mesmo com eficiência um pouco pior (cânone §4).
>
> **Sem o arquivo da 15, nada muda:** a projeção fica como hoje, com a coluna de margem mensal, e o relatório diz a frase inteira — *"margem de contribuição de US$ X/mês; sem os custos fixos informados não dá pra dizer se há lucro"* — em vez de deslizar pra chamar a margem de "lucro".

**Pessimista (CPA sobe 20%):**

Ação: parar de subir budget, segurar no último nível lucrativo, refresh de criativo (08) + possível ajuste de oferta (04), retomar escala quando o CPA voltar ao alvo (geralmente 7-14 dias).

Impacto: escala atrasa ~1 mês, mas sem queimar cash flow.

**Template de cash flow (incluir sempre):**

| Dia | Daily Budget | Daily Revenue | Payable (ads) | Receivable (payout +3d) | Cash Float Needed |
|-----|--------------|---------------|---------------|-------------------------|-------------------|
| 1   | $200         | $500          | -$200         | $0                      | $200              |
| 4   | $300         | $750          | -$300         | +$500 (payout do Dia 1) | $300-500          |
| ...  | ...          | ...           | ...           | ...                     | ...               |

(Com payout +3d, a receita do Dia 1 só vira caixa no Dia 4 — os dias 1-3 são cobertos 100% pelo float. Esse é exatamente o descasamento que a tabela existe pra mostrar. Use o payout_lag REAL do membro: loja nova com hold/rolling reserve → montar a tabela com 7-14 dias, não +3d — ver o cenário na ETAPA 6.)

Alerte se `cash_float_needed_peak > cash_disponivel × 0.7`.

### ETAPA 8 — Creative Diversity Como Combustível da Escala

Escalar consome criativo. O mesmo criativo satura a audiência: a $100/dia satura em ~30 dias; a $500/dia em ~7-10 dias; a $2K/dia em 3-5 dias. As três escolas dependem de pipeline de criativo:

**Frameworks que governam o criativo como alavanca de escala (rode os relevantes):**
- **Creative Diversity as a Scaling Mechanism** (rode `creative diversity as a scaling mechanism funnel balance video image 4Pi same position`) — diversidade de criativo (video/image, ângulos) equilibra o funnel e destrava mais spend na MESMA posição do 4Pi. É o motor de horizontal scale dentro da vertical.
- **More Better New Scaling Framework (Hormozi)** (rode `More Better New scaling framework Hormozi sequence maximize before new method`) — sequência: maximize o que existe (More), melhore (Better), só então adicione método novo (New). Aplique antes de abrir frente de criativo nova — esgote o winner atual primeiro.
- **Reeves' Principle of Dispersion** (rode `Reeves principle of dispersion reach over frequency Reality in Advertising new audiences`) — em escala, reach sobre frequency: criativo novo abre audiência nova em vez de martelar a mesma. Fundamenta por que frequency alta pede batch novo, não mais budget.
- **Minimum Daily Spend & Creative Hamster Wheel** (rode `minimum daily spend creative hamster wheel new ads steal bottom of funnel never turn off main campaign`) — ads novos roubam bottom-of-funnel da campanha principal; nunca desligue a campanha principal pra "fazer espaço". Calibra a cadência de batch sem canibalizar.

- A Escola B é **literalmente alimentada** por ad sets novos de criativo continuamente.
- A Escola A precisa de breakthroughs de backup pra quando o atual cansar no surf.
- A Escola C destrava níveis novos com criativo melhor.

**Quantidade de criativo por sub-fase de escala (heurística, não lei):**

| Sub-fase | Novos conceitos/batch | Frequência | Creators em retainer |
|---|---|---|---|
| Teste (<$100/dia) | 3-5 | Mensal | 0 |
| Tração ($100-500) | 5-8 | A cada 2-3 semanas | 0-1 |
| Escala Inicial ($500-1K) | 8-12 | Quinzenal | 1-2 |
| Escala Agressiva ($1K-5K) | 12-20 | Semanal | 2-4 |
| Otimização ($5K+) | 20+ | Semanal | 4+ ou agência |

Calibre pelo stage (`member-stage-awareness.md`): starter recebe a ponta baixa, scaling a ponta alta. Se `frequency_max < 1.3` e CPM estável (banda de folga da régua única — ver ETAPA 10), pode segurar a contagem atual mesmo escalando.

**Expansão de canal com criativo validado (horizontal, só com breakthrough vivo):** quando a vertical no Meta encosta no teto e o breakthrough segue performando, o movimento horizontal é replicar o criativo **já validado** em outro leilão — prioridade pós-Meta: **AppLovin/Axon ≈ TikTok**, empatados (rode `replicar criativo validado AppLovin Axon Snapchat YouTube end cards 9:16`). A execução NÃO vive nesta skill: é o **Movimento 4 da Trilha 1 da skill 14 (content-recycler)** — re-export 9:16, brief do end card do Axon e a régua de canal novo (US$ 250-1.000/dia por 60-90 dias antes de julgar; desistir em 1-2 semanas não descobre nada). Handoff: diga **`'recycle [id do breakthrough]'`** e a 14 monta o pacote de adaptação. Canal novo aberto = linha nova no `ad-log.md` quando o budget dele nascer.

**Canal incremental — tráfego de agentes de AI (se `manifest.agentic.ready: true`):** além da diversificação de criativo, o scale horizontal ganha uma fonte que não depende de leilão do Meta: referral de agentes de compra com AI (ChatGPT, Perplexity, Google AI Mode). Se a Skill 07e marcou a loja como pronta (`agentic.ready: true`, score no bloco), trate esse canal como **fonte incremental** no plano: (1) confira no analytics se já existe referral desses domínios (chatgpt.com, perplexity.ai) e registre a linha de base; (2) inclua o canal nas projeções 30/60/90 como upside conservador (não como premissa de caixa — o volume ainda é pequeno e não-comprável); (3) se `agentic.score < 80`, mencione que re-rodar a 07e fecha gaps que aumentam a chance de citação. Nunca desvie budget de ads pra "otimizar AEO" — é canal orgânico incremental, não substituto do paid.

### ETAPA 9 — Checklist Operacional Semanal

Escala sustentável é ritmo. Adapte ao stage e à escola escolhida — os dias abaixo executam o Scaling Protocol da ETAPA 3.5, não uma régua paralela:

| Dia | Ação |
|---|---|
| **Todo dia, à meia-noite do fuso do ad account** | **Reset de budget: ~50% do gasto REAL do dia** em toda campanha que teve budget alterado. Nunca deixar o nominal de pé (ETAPA 3.5). Cada reset aplicado = linha no `ad-log.md` (executor `skill-12`, motivo "reset da meia-noite"). |
| **Manhã (diário, só Escola A)** | Surf check: alguma campanha com CPA muito abaixo do alvo? Empurra budget e observa 2-3h. Recolhe se quebrar. |
| **Segunda** | 4Pi quick check (Spend → Frequency → CPM → CPR), 5-10 min + checar os dois gates do protocolo (48-72h acima do target? click-based verde — ≥ 60% em 7-day click OU ROAS click-based batendo o KPI?) |
| **Terça** | Avaliar se sobe nível: gates verdes → **+20%** (ou o passo da escola escolhida) / adicionar ad set novo (Escola B) — conferindo no `ad-log.md` que o degrau anterior tem ≥24h, e logando o novo. Gates vermelhos → passo zero e ação fora do ad account (ETAPA 3.5, passo 7) |
| **Quarta** | Revisar learnings + preparar ideias de batch novo |
| **Quinta** | Continuar alimentando criativo (Escola B) / surf se Escola A |
| **Sexta** | **Análise semanal completa** (skill 11 — 4Pi full + diagnóstico de fadiga) |
| **Domingo** | **Preparar próximo batch** de criativos (skill 08) |

**Monthly review** (1× ao mês, primeiro dia útil):
- PSM real vs projetado (re-ler `manifest.psm_real` + `psm_real_basis` — base proxy segue não liberando escala)
- **Calendário de desejos — revival sazonal:** algum winner que morreu por sazonalidade tem a época dele chegando? Ad sazonal aposentado volta a performar no MESMO período do ano seguinte, e religar custa zero criativo novo (rode `religar seasonal winners ads que morreram voltam no mesmo período calendário de desejos`). Religada executada → linha no `ad-log.md` ("religado", motivo "revival sazonal")
- Custo fixo mensal mudou? (contratação, app novo, retainer) — o gate de corte por ROAS depende desse número estar atual
- Winning ad rate (% de conceitos testados que viraram **breakthrough**, não só que bateram KPI)
- A intensidade atual ainda serve? (graduou de stage? subir de C pra B, ou de B pra A? passou de $1K/dia sustentado → hora de avaliar a graduação pra ASC, ETAPA 4?)
- Algum CPM de conta subiu a ponto de pedir conta nova legítima?
- Membro ligou **Incremental Attribution** em alguma campanha? Os CPAs dela não são comparáveis aos clássicos — re-baseline antes de qualquer decisão de kill/escala (ver nota na Skill 11). Em multi-canal com suspeita de over-attribution do Meta, pode servir como teste de eficiência real — nunca como régua default.
- Re-rodar Skill 12 se mudança estrutural (novo produto, nova oferta, novo teto)

### ETAPA 10 — Sinais de Alerta (Quando Parar/Recuar)

**Régua única de frequency desta skill (freq DIÁRIA, mesma base da Skill 11 — as três leituras abaixo usam ESTA régua, não invente outra):**
- **< 1.3** → folga: pode segurar a contagem de criativos mesmo escalando (ETAPA 8).
- **> 1.4 sustentada + CTR caindo > 20% vs baseline** → fadiga: refresh de criativo — volta pra 08 (é o trigger canônico do `dados.json`).
- **> 1.5 sustentada em prospecting** → audiência saturada: batch novo ANTES de mais budget.

**Frameworks de recuo e diagnóstico de saturação (rode quando algum sinal disparar):**
- **Scale-Down Rules (PGS reverse)** (rode `scale-down rules decrease budget 20% 7-day CPA exceeds target safety net`) — quando o CPA de 7 dias estoura, corta 20% e segura (não desliga). É a regra dura por trás de "derruba o surf" / "volta pro último nível bom".
- **Spend Redistribution Framework (Don't Kill the Top Spender)** (rode `spend redistribution framework do not turn off top spender ROAS drops higher budget`) — quando o ROAS cai ao subir budget, redistribui em vez de matar o top spender (matar reseta aprendizado).
- **Frequency as Prospecting-vs-Retargeting Proxy** (rode `frequency prospecting vs retargeting proxy low 1.0 high 2.5 broad CBO scaling signal`) — lê frequency como sinal de saturação: baixa (~1.0) = ainda prospectando (pode subir), alta (~2.5) = virou retargeting disfarçado (audiência saturada, pede batch novo).

> **Gate obrigatório antes de recomendar CORTE de spend por queda de ROAS** (unit-economics §4, detalhado em "Custo fixo antes de cortar spend"): ROAS que caiu mas ainda paga o custo variável **não** autoriza corte automático. Com o custo fixo parado, cortar receita pode **aumentar** o prejuízo — e a resposta certa às vezes é subir spend aceitando ROAS menor, porque volume dilui melhor o fixo. Se o membro não informou os fixos, a skill devolve **pergunta** ("quanto é seu custo fixo mensal?"), não instrução de corte. Abaixo do **breakeven por 24-48h persistentes**, a descida de −20% do `ad-taxonomy` §5 continua valendo normalmente (um dia ruim isolado não desce) — lá o problema não é diluição, é margem de contribuição negativa por pedido.

- **CPA dos últimos 3 dias acima do breakeven** → para de subir budget (passo zero no protocolo), refresh criativo antes de qualquer escala. Na Escola A, derruba o surf. E 3 dias já cruzaram a janela de 24-48h persistentes do §5 — a descida de −20% se aplica; confira no `ad-log.md` se ela já foi executada.
- **Frequency > 1.5 sustentada em prospecting** (nas campanhas/ad sets ativos — régua única acima) → audiência saturada, precisa batch novo (08).
- **CPM subindo 30%+ em 14 dias** → saturação, competição, ou conta cansada. Diagnóstico na skill 11; se for conta, abrir conta nova legítima (ETAPA 4.5).
- **Budget novo não gasta / trava entrega** → diagnóstico ETAPA 4.5 (conta vs produto), não conclua "teto" cedo demais. Se o teto for real, a ação é **fora do ad account** (ETAPA 3.5, passo 7), não outro ajuste de bidding.
- **Gates do protocolo vermelhos há mais de uma semana** (nunca completa 48-72h acima do target, ou gate click-based vermelho nas duas portas — <60% em 7-day click E ROAS click-based abaixo do KPI) → o gargalo não é budget. Batch novo (08) + conferência de funil, e re-medir atribuição na 07c (o teste de troca 7DC-only da ETAPA 3 é o diagnóstico). Antes de culpar o leilão, confira também um "new reason to be scaling" perdido: se a demanda mudou (sazonalidade, oferta nova), a leitura do protocolo reinicia (ETAPA 3.5).
- **Cash flow gap** → spend correndo na frente do payout. Ajustar pace (ETAPA 6).
- **Fulfillment bottleneck** → estoque/3PL não acompanha. Nunca escale acima da capacidade operacional — venda que não entrega vira chargeback e ban. Com o sourcing na mão, `calendar.reorder_point_days` diz quando segurar: perto do ponto de recompra, pedido de reposição colocado e escala agressiva em pausa até o estoque chegar (ETAPA 6).

### Quando 12 recomenda voltar para 08 (ciclo explícito)

Se algum destes → invoque skill 08 pra novo batch:
- Top 3 criativos com > 14 dias de idade
- Frequency max > 1.4 sustentada com CTR caindo > 20% vs baseline (régua única da ETAPA 10)
- Escala cruzou 2× budget (precisa creative diversity pra sustentar)
- Conta nova aberta (ETAPA 4.5) precisa de criativo pra alimentar
- **Escala estagnou** — budget não sobe mais sem quebrar o CPA, ou os gates do protocolo não fecham (ETAPA 3.5, passo 7). É o gatilho mais frequente: quando a escala trava, a alavanca está fora do ad account, e criativo novo é a primeira dela.
- **Só existe `KPI winner` / `spend winner`, nenhum breakthrough** — não há o que escalar; o pedido pra 08 é conceito novo, não variação do mesmo.

Skill 08 lerá `11-ad-analysis/NEXT_BATCH_IDEAS.md` (de 11) + `12-scale-engine/scale-directives.md` (gerado abaixo).

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `scale-engine.md` → `scale-engine.html`). **Isentos** (arquivos operacionais de handoff — rule 6b do CLAUDE.md, lista completa em `.claude/lib/workspace-index/workspace-layout.md`): `scale-directives.md`, `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, **logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**, componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/12-scale-engine/` antes de salvar.

Outputs em `workspace/[produto]/12-scale-engine/`:

- `scale-engine.md` contendo:
  1. Classificação de estágio + sub-fase de escala (Etapa 2)
  2. Análise de prontidão com bloqueios identificados, incluindo a classe do(s) criativo(s) que liberou (ou não) a escala (Etapa 3)
  2b. **Scaling Protocol aplicado ao caso do membro** (Etapa 3.5): status dos dois gates (consistência 48-72h + as duas portas do click-based), a última mudança de budget do `ad-log.md` e há quanto tempo, exceção ativa do cânone se houver (promo com data-fim / "new reason to be scaling"), qual o próximo passo de budget e quando, a régua de descida (−20% só após 24-48h persistentes abaixo do breakeven), e — em destaque — **a regra de reset da meia-noite com o número calculado** pro budget vigente
  3. **Escola de escala escolhida** (variante de intensidade) + bidding efetivo + setup operacional concreto (cost cap value / bid cap + budget / cadência de doubling) (Etapa 4)
  4. Política de conta nova quando entrega trava (Etapa 4.5) + status da execução via MCP, se usada: o que foi criado em PAUSED e os IDs (Etapa 4.6)
  5. Credibilidade da loja — gaps a resolver (Etapa 5)
  6. Cash flow check + gap projetado — com a necessidade de caixa, o float e o runway da 15 quando ela existir (Etapa 6)
  7. Projeção 30/60/90 base + pessimista + template cash flow, com a coluna de resultado operacional e o teto de escala quando os fixos estiverem na mesa (Etapa 7)
  8. Creative diversity plan (Etapa 8)
  9. Checklist operacional semanal (Etapa 9)
  10. Sinais de alerta (Etapa 10)

- `scale-directives.md` (fecha ciclo 12→08):
  - Budget atual + budget alvo (30d)
  - Escola de escala em uso + ritmo de criativo que ela exige
  - **Breakthrough(s) em escala** — o que a 08 precisa produzir pra sustentá-los; e, se só há `KPI winner`/`spend winner`, dizer isso explicitamente (o pedido vira conceito novo, não variação)
  - PSM real atual
  - Sinais que trigam volta pra 08 (creative refresh) + se a escala está estagnada (a ação fora do ad account que cabe à 08)
  - Bloqueios de cash flow (se houver)

- **`workspace/[produto]/ad-log.md`** (append-only, cânone `.claude/lib/ad-log/README.md` — arquivo operacional, isento de dual output): as linhas desta execução já foram gravadas **no momento de cada mudança** (degraus, resets da meia-noite, ABO, graduação ASC, ações via MCP — ETAPAS 3.5/4.6/9), nunca em lote no fim. Antes de fechar, conferir que nenhuma mudança instruída/executada ficou sem linha.

- `dados.json` (JSON companion):

```json
{
  "plan_id": "uuid",
  "product_slug": "...",
  "stage": "starter|validating|scaling",
  "scale_phase": "testing|traction|initial_scale|aggressive|optimization",
  "scaling_school": "A_cost_cap_surf|B_bid_cap|C_budget_doubling",
  "current_daily_spend": 0,
  "target_daily_spend_30d": 0,
  "breakeven_cpa": 0,
  "max_cpa": 0,
  "psm_real": 0,
  "psm_real_basis": "shopify_new_customer|platform_cpa_proxy",
  "psm_theoretical": 0,
  "readiness_blockers": [],
  "scale_trigger": {
    "class": "breakthrough|spend_winner|kpi_winner|loser|none",
    "breakthrough_ids": [],
    "source": "11-ad-analysis/dados.json",
    "reclassified_from_legacy_winners": false,
    "scale_unlocked": false
  },
  "scaling_protocol": {
    "hours_above_target": 0,
    "consistency_gate_passed": false,
    "click_based_purchase_share": 0,
    "click_based_share_source": "manifest|member|none",
    "click_based_roas_beats_kpi": false,
    "click_gate_passed": false,
    "hours_below_breakeven": 0,
    "active_exception": "none|promo_end_date|new_reason_to_be_scaling",
    "step_up_pct": 20,
    "step_down_pct": 20,
    "next_step_allowed_at": null,
    "last_budget_change_from_ad_log": null,
    "stagnated": false,
    "scale_ceiling_monthly_spend": null,
    "scale_ceiling_source": "15-finance-engine|empirical|unknown",
    "outside_ad_account_actions": []
  },
  "midnight_reset": {
    "rule": "next_day_budget = ~50% of REAL spend, never of nominal budget",
    "ad_account_timezone": null,
    "last_real_spend": 0,
    "next_day_budget": 0
  },
  "bidding": {
    "main_campaign": "highest_volume",
    "cost_cap_scope": "zombie_graveyard_only",
    "bid_cap_used": false,
    "bid_cap_caveat_acknowledged": false
  },
  "fixed_cost_gate": {
    "source": "15-finance-engine|member|manifest|none",
    "monthly_fixed_costs_known": false,
    "monthly_fixed_costs": null,
    "finance_verdict": "covers_fixed_costs|scale_up_accept_lower_roas|cut_spend_below_variable_breakeven|blocked_pending_fixed_costs|null",
    "spend_to_breakeven_with_fixed": null,
    "roas_cut_recommendation": "blocked_pending_fixed_costs|blocked_by_roas_spiral|cleared|not_applicable"
  },
  "vertical_plan": {
    "cost_cap_value": null,
    "cost_cap_duplication_steps": [],
    "bid_cap_value": null,
    "bid_cap_budget": null,
    "doubling_cadence_days": null,
    "surf_enabled": false
  },
  "new_account_policy": {
    "trigger": "delivery_throttled_or_account_cpm_too_high",
    "legitimate_only": true
  },
  "mcp_execution": {
    "path": "official|pipeboard|manual",
    "created_paused_campaign_ids": [],
    "automated_rules_created_disabled": []
  },
  "cash_flow": {
    "source": "15-finance-engine|local_estimate",
    "cash_gap_projected": 0,
    "cash_needed_90d": null,
    "total_float_days": null,
    "runway_months": null,
    "safe_to_escalate": true
  },
  "supply_confirmation": {
    "source": "sourcing-01b|member|none",
    "volume_confirmation_30_60_90": null,
    "reorder_point_days": null
  },
  "triggers_back_to_08": [
    "top_3_creatives_older_than_14_days",
    "frequency_max_over_1.4_with_ctr_drop_over_20pct",
    "scaled_past_2x_budget",
    "new_account_opened_needs_creative_fuel",
    "scale_stagnated_fix_is_outside_ad_account",
    "no_breakthrough_only_kpi_or_spend_winners"
  ]
}
```

**Campos que a skill NUNCA preenche por estimativa:** `scale_trigger.class` (vem da classificação do cânone §2 sobre dados reais da 11), `scaling_protocol.click_based_purchase_share` (vem de `manifest.click_based_purchase_share` gravado pela 11 — ou do membro via Ads Manager, quando o manifest não tem), `psm_real_basis` (cópia de `manifest.psm_real_basis`; ausente = tratar como `platform_cpa_proxy`), `supply_confirmation` (vem do `sourcing/dados.json` da 01b ou do membro) e `fixed_cost_gate.monthly_fixed_costs` (vem do membro ou da 15). Faltando qualquer um, o campo fica nulo, o gate correspondente fica bloqueado, e o relatório diz o que falta pra destravar.

**Campos que só existem quando a 15 rodou:** `fixed_cost_gate.finance_verdict` / `.spend_to_breakeven_with_fixed`, `scaling_protocol.scale_ceiling_monthly_spend`, `cash_flow.cash_needed_90d` / `.total_float_days` / `.runway_months`. São **cópias** do `15-finance-engine/dados.json` — esta skill não os recalcula com fórmula própria. Sem o arquivo da 15, ficam `null`, os campos `source` registram a origem local, e cada ponto de uso cai no fallback descrito no Contexto (item 5d).

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `12-scale-engine` em `skills_completed`
- Registrar `plan_id`, `psm_real`, `scaling_school`
- Registrar `manifest.fixed_costs_monthly` quando o membro informar (a 11 e a 15 usam o mesmo número; se já existir e o membro deu outro, o valor novo prevalece e a mudança é avisada)
- Gravar `manifest.stage` com o vocabulário canônico (`starter` | `validating` | `scaling`). Se a sub-fase de escala importar, ela vive em `scale_phase` no `12-scale-engine/dados.json` — **NUNCA** em `stage`.
- Se o membro graduou de stage durante esta análise (ex: `validating` → `scaling`), atualizar `manifest.stage` e avisar (ver `member-stage-awareness.md`).
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html, onde `<slug>` é o product_slug).

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`). Apresente a escola recomendada como ponto de partida e convide ajuste.

**Se PRONTO pra escalar:**
"Plano de escala pronto (draft). A régua é a mesma pra qualquer caminho: sobe **+20%** só depois de **48-72h acima do target** e com o gate click-based verde (**≥60% das compras em 7-day click**, ou o ROAS contado só com compras de clique batendo o KPI sozinho), depois a cada 24h — cada mudança fica registrada no ad-log do produto, e é lá que eu confiro as 24h desde o último degrau. Descida: só depois de **24-48h seguidas abaixo do breakeven**, aí **−20%** (um dia ruim isolado não derruba nada). Duas exceções, e só essas: promo com data-fim entra direto no budget da promo (protegida pelo surf + reset da meia-noite), e um motivo NOVO pra escalar (oferta nova, breakthrough novo, sazonalidade) reinicia a contagem. Recomendei a **Escola [X]** pro seu stage como intensidade: [setup concreto — bidding, cost cap $Y / bid cap $Z budget $W / dobra a cada 3 dias].
**O ponto que mais custa dinheiro:** toda vez que você subir budget, à meia-noite (fuso do seu ad account) o budget do dia seguinte volta pra **~metade do que você REALMENTE gastou**, nunca pro número que ficou na tela. Hoje isso dá **~$[valor]**. Se deixar o nominal de pé, o Meta gasta ele inteiro no dia seguinte enquanto você dorme.
Quer rodar essa escola ou prefere outra? Roda o checklist semanal e me volta daqui a 30 dias ou quando precisar re-analisar — diga **'ad analysis'** com os dados atualizados."

**Se NÃO PRONTO (algum bloqueio):**
"Antes de escalar, [N] bloqueio(s) a resolver: [listar]. Ação por bloqueio:
- [Bloqueio 1] → [ação + skill]
- ...
Sem breakthrough (criativo que bate o KPI da campanha **e** puxa spend) ou com PSM abaixo do esperado, escalar só queima budget mais rápido. Criativo que bate o KPI mas não puxa spend ainda não provou nada em escala. Resolve isso e diz **'scale'** de novo que eu monto o plano."
