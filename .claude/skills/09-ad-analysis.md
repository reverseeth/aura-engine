---
name: ad-analysis
description: Engine de análise de performance de Meta Ads usando 4Pi Analysis (Spend → Frequency → CPM → Cost per Result), 19-point diagnostic pra losers, extração de learnings de winners, framework de 12 perguntas (feedback loops), e recomendações acionáveis imediato/curto/médio prazo. Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "ver resultado", "diagnóstico", ou após 3-7+ dias rodando a campanha da Skill 07. Entrega decisões concretas — escalar, pausar, refresh de criativos, ou ajustar oferta/página.
---

# Ad Analysis Engine

## Quando Usar
Quando a campanha está rodando há 3+ dias e o membro precisa diagnosticar o que está acontecendo e decidir próximos passos. Esta skill NÃO é "reportar dados" — é **diagnóstico + decisão**. Sai com ações concretas (hoje / 3-7 dias / 2-4 semanas).

## Antes de Começar

1. Leia `/workspace/profile.md` (budget — contexto pra decisões de scale)
2. Leia `/workspace/[produto]/04-offer.md` (target CPA, breakeven ROAS, margem — benchmarks pra avaliar performance)
3. Leia `/workspace/[produto]/07-ad-strategy.md` (estrutura da campanha, conceitos testados, regras de decisão)
4. Leia `/workspace/[produto]/08-analysis/` — **SE EXISTIR**, leia análises anteriores em ordem cronológica (pra ver evolução, identificar tendências, comparar com análises passadas)
5. Consulte a base Aura extensivamente sobre 4Pi Analysis (Spend/Frequency/CPM/Cost per Result completo), 4Pi Dashboard Setup (custom metrics), creative fatigue (sinais e tratamento), revisão de Ads Perdedores (diagnostic 19 pontos), revisão de Ads Vencedores e extração de ideias, Framework de 12 Perguntas pra Feedback Loops, Aplicação de Learnings pra Novos Ads, Complete a Feedback Loop, Feedback Loops como Motor de Crescimento, ROAS Targets e Scaling, Minimum Daily Spend (por que ads ruins geram gasto), PGS, winning ad rate, funnel creative playbook (positions e signatures TOF/MOF/BOF). Cada framework que existir, aplique.

## Fluxo da Skill

### ETAPA 1 — Receber Dados

Diga ao membro (uma única mensagem):

"Cola os dados do Ads Manager aqui — screenshot ou números. Preciso ver por ad set: Spend, Frequency, CPM, CPC, Cost per Purchase, ROAS. E quantos dias cada ad set está rodando."

ESPERE a resposta. Se enviar dados incompletos, peça só o que faltou — não re-explique a pergunta.

Parse os dados em uma tabela estruturada internamente:

| Ad Set | Days Running | Spend | Freq | CPM | CPC | CTR | CPA | ROAS |
|---|---|---|---|---|---|---|---|---|

Se o membro mandar screenshot, extraia os números via análise visual.

### ETAPA 2 — 4Pi Analysis (Ordem EXATA)

Aplique os 4 Pi's da vault **NA ORDEM** (Spend → Frequency → CPM → Cost per Result). A ordem importa — cada Pi contextualiza o próximo.

#### Pi 1: SPEND

"Quanto cada ad set recebeu de budget?"

Observação-chave (da vault): **Meta distribui spend pra onde ele ACREDITA que está funcionando**. Se o ad set A recebeu 40% do spend total e o B só 10%, o algoritmo tá "votando" que A é melhor (independente de CPA).

- **Ad set que recebeu muito spend** (share > 25% do total) → Meta tá confiante nele
- **Ad set com spend < 10% do seu share esperado** → Meta não tá confiante OU ad não foi aprovado OU audience muito pequena

Se um ad set "não gastou" em 3+ dias: verificar Ads Manager > Delivery insights + Review status. Pode ter sido pausado por policy.

#### Pi 2: FREQUENCY (Sinaliza Posição no Funil)

Aplicar as signatures da vault:

- **Freq < 1.1** → **TOF** (Top of Funnel) — novas impressões, cold traffic
- **Freq 1.15-1.3** → **MOF** (Middle) — starting to warm up
- **Freq > 1.3** → **BOF** (Bottom) — retargeting-like, mesmas pessoas vendo várias vezes

Se a campanha tem TODOS os ad sets com freq > 1.3, falta **diversidade no funil** — você tá esgotando a audience retardtada sem abrir pra TOF novo. Recomendação: adicionar conceito TOF-friendly (hook problem, angle curiosity).

Se TODOS estão com freq < 1.1 e a campanha tá há 14+ dias, algo tá preventing Meta de re-engajar — geralmente CPM baixo + CTR muito baixo = audience não resonando.

#### Pi 3: CPM (Contexto Combinado com Freq)

**CPM isolado diz pouco. CPM + Freq diz muito:**

- **CPM alto (acima da média do nicho) + Freq alta (>1.3)** → Meta tá mandando pra audience cara (prime-time, premium placements) porque POUCA audience nova está disponível. Sinal de BOF / possível fadiga.
- **CPM alto + Freq baixa (<1.1)** → audience premium/cara mas fresca. Pode ser normal em nicho competitivo (skincare, finance, luxury).
- **CPM baixo + Freq alta** → Meta tá procurando impressões baratas com audience repetida. Frequência tá alta mas CPM não subiu = Meta não tá pagando caro pra forçar. Pode ser fadiga mas também pode ser só stabilidade.
- **CPM subindo no tempo** (comparar com análises anteriores se houver) → **possível fadiga**. Combinar com CTR falling pra confirmar.

#### Pi 4: COST PER RESULT (O Que Realmente Importa)

Compare CPA de cada ad set contra o **target CPA da oferta** (do `04-offer.md`):

- **CPA ≤ target** → WINNER (vai pro diagnóstico "scale")
- **CPA ≤ 2× target mas > target** → NEEDS OPTIMIZATION (iteração, não pausar ainda)
- **CPA > 2× target após 7 dias** → LOSER (pausar)

Contexto importante: **CPA de um ad set isolado não é tudo**. A vault é clara: "a campanha overall melhorou?". Se campanha total está dentro de CPA target mesmo com 1-2 ad sets fora, a maquina tá OK. Otimiza os outliers, não destrua campanha.

### ETAPA 3 — Diagnóstico Por Ad Set

Pra CADA ad set, classifique:

**WINNER:** recebeu spend, CPA ≤ target, campanha overall melhorou.
→ Ação: escala automática via PGS. Se quer escalar mais agressivo, considera promover criativo a Champion (Post ID) e adicionar ad set dedicado.

**IN FATIGUE:** CPM subindo + CTR caindo + Freq subindo ao longo dos dias (comparar com análises anteriores).
→ Ação: refresh criativo (trocar 1-2 dos 3 criativos do 3-2-2) OU adicionar novo batch de conceitos (Skill 07). **Não pausar ainda** — pode ainda estar performando acima do breakeven mesmo com sinais de fadiga.

**LOSER:** sem spend em 7 dias OU CPA > 2× target após 7 dias.
→ Ação: PAUSAR. Fazer diagnóstico profundo (Etapa 4) pra entender por que falhou.

**EM APRENDIZADO:** < 7 dias rodando, spend baixo.
→ Ação: aguardar mais 3-4 dias antes de decidir. Learning phase do Meta precisa mínimo 50 conversions.

### ETAPA 4 — Diagnóstico Profundo de LOSERS (19-Point Diagnostic)

Consulte a base Aura sobre "revisão de ads perdedores 19 pontos". Aplique o checklist diagnóstico pra cada LOSER:

**Camada 1: Targeting/Audience**
1. Audience estava certa pro awareness level? (se é TOF, broad é certo; se é warm, Advantage+ broad ainda ok mas specific retargeting pode performar melhor)
2. Mercado geográfico alinhado com o que o produto atende?
3. Idade/gênero apropriados?

**Camada 2: Hook/Criativo**
4. O hook do criativo grabbed attention nos primeiros 3s? (thumbstop baixo → hook fraco)
5. O criativo comunica valor CLARO na primeira exposição (sem áudio)?
6. O formato escolhido casa com a audience (UGC pra mainstream, demo pra technical)?
7. A duração é apropriada (TOF curto 15-22s, BOF pode ser mais longo)?

**Camada 3: Copy/Messaging**
8. Primary text tem hook forte na primeira linha (antes do "See more")?
9. Headline é clara e ressoa com audience?
10. Congruência ad → LP (message match, visual match, promise match)?
11. Claim usado não é saturado (do competitor analysis)?

**Camada 4: Oferta/LP**
12. LP carrega rápido? (mobile speed score)
13. Above-the-fold da LP comunica a promessa do ad em 3 segundos?
14. Oferta tem stack de valor forte ou parece overpriced?
15. Garantia visível?

**Camada 5: Técnico**
16. Pixel + CAPI funcionando? (verifica no Events Manager)
17. Eventos disparando corretamente (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)?
18. UTMs capturando corretamente (pra atribuir no Shopify)?
19. Gateway/checkout não tem erro técnico (test purchase)?

Pra cada loser, identifique **a camada onde falhou** e a hipótese específica. Documente.

### ETAPA 5 — Diagnóstico de WINNERS (Extração de Learnings)

Pra cada WINNER, extraia learnings aplicando o framework da vault:

- **O que funcionou?** (hook específico, ângulo, formato, CTA, LP)
- **Por que funcionou?** (hipótese causal — ex: "hook de curiosity pattern interrupt em audience Problem Aware onde concorrentes usam authority-first")
- **Como replicar?** (quais elementos isolar pra usar em próximos batches — ex: "o hook 'POV: você acorda com X' pode ser template pra outros conceitos")

Learnings vão alimentar Skill 07 (creatives) no próximo batch — escreva de forma utilizável.

### ETAPA 6 — Balanço de Funil

Veja distribuição por posição de funil (dos Pi 2 — frequency signatures):
- Todos os ad sets em TOF? → funil raso, falta converter warm audience
- Todos em BOF? → falta trazer volume novo, tá escalando sobre a mesma audience
- Distribuído em TOF + MOF + BOF? → saudável

Recomendação baseada em desbalanço:
- Falta TOF → próximo batch inclui conceitos de awareness building (hook problem, curiosity, authority)
- Falta BOF → próximo batch inclui retargeting-style (offer-focused, urgency, comparison)

### ETAPA 7 — Framework de 12 Perguntas (Feedback Loops)

Consulte a vault sobre "Framework de 12 Perguntas pra Feedback Loops". Aplique as perguntas aos dados:

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
- Se falta diversidade de funil: gerar novo batch de conceitos (Skill 07) com foco na posição faltante
- Ajuste de URLs se 3-2-2-2 mostrou preferência clara de LP

**MÉDIO PRAZO (2-4 semanas):**
- Se winners estáveis: promover pra Champion (Post ID separado)
- Se CPA está melhor que target consistentemente: reavaliar se dá pra escalar mais (vertical + horizontal — delegar pra Skill 10)
- Se oferta parece ser o bloqueio: voltar pra Skill 04 e ajustar (bundle structure, guarantee, stack)
- Se página parece ser o bloqueio: voltar pra Skill 05/06 e iterar

### ETAPA 9 — Decisão de Scaling (Recomendação Clara)

Baseado no diagnóstico completo, dê uma recomendação clara:

**SE CPA dentro do target E winning ads estáveis:**
"Continue rodando. PGS vai escalar automaticamente. Se quer escalar mais agressivo OU adicionar canais novos, diga **'scale'** pra eu montar o plano."

**SE CPA ≤ 0.7× target E winning ad claro:**
"Oferta forte, ads matando. Diga **'scale'** pra montar plano de escala vertical + horizontal. Pode considerar scaling aggressive em paralelo ao PGS."

**SE CPA acima do target mas ainda abaixo de 2×:**
"Não escala. Foco em iteração. Diga **'creatives'** pra gerar novo batch baseado nos learnings desta análise."

**SE CPA > 2× target após 7+ dias:**
"Bloqueio não é só ad — pode ser oferta, página, ou audience. Vou sugerir investigação: [indicar onde está o bloqueio mais provável baseado no 19-point]. Depois de ajuste, re-roda análise em mais 7 dias."

### ETAPA 10 — Learnings Documentados (Pra Feedback Loop)

Na seção final do relatório, documente learnings que vão alimentar próximos batches:

**Hipóteses validadas** (o que ficou confirmado pelos dados):
**Hipóteses rejeitadas** (o que não confirmou):
**Hipóteses ainda em teste** (precisa mais dados):
**Ideias pra próximo batch:**

Isso é o "feedback loop motor de crescimento" da vault — cada análise enriquece o próximo batch de criativos.

## SALVAR

`/workspace/[produto]/08-analysis/[YYYYMMDD]-analysis.md` contendo todas as 10 etapas. A pasta `08-analysis/` acumula histórico — análises anteriores servem de input pra comparar evolução nas análises seguintes.

## Mensagem Final

Adapte baseado no diagnóstico (ver Etapa 9 — recomendação de scaling). Termine sempre com uma próxima-ação CLARA:

- Continua rodando + PGS → monitora, próxima análise em 3-7 dias
- Escala → diga `'scale'`
- Iteração de criativos → diga `'creatives'`
- Ajuste de oferta → diga `'offer'`
- Ajuste de página → diga `'copy'` ou `'page'`
- Bloqueio técnico → resolução específica + nova análise depois
