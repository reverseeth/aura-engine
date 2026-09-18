# Creative Engine · Referência: Briefing completo por conceito (ETAPA 5)

> Os sistemas da base a puxar antes de escrever (script, hook, bridge, hold, CTA, headlines, primary texts, statics) e o formato completo do briefing, do cabeçalho com as 9 variáveis ao racional estratégico. Abra na ETAPA 5.

### ETAPA 5 — Gerar Briefings Completos (Um Por Conceito)

Para CADA conceito aprovado, gere o briefing completo aplicando os frameworks. **Antes de escrever hook/script/headline, puxe os SISTEMAS NOMEADOS da base — rode a `best_query` exata de cada um, NUNCA query genérica. Índice completo em `.claude/lib/kb-index/`.**

**Para o SCRIPT completo (rodar antes de escrever o roteiro segundo-a-segundo):**
- **Optimized Video Ad Script Prompt V1 (master prompt de roteiro)** (rode `master prompt situation setup Big 4 emotions B-roll AI voiceover slippery slope cadence`) — o master prompt completo de scriptwriting: situation setup, as Big 4 emotions, B-roll, voiceover de AI e cadência em slippery slope. Ele exige 4 documentos de contexto — aqui são os artefatos das fases `market-research`/`competitor-analysis`/`offer-builder`/`copy-engine` já carregados no "Contexto a carregar" — e uma restrição de awareness: o awareness lock do conceito (Hard Rule A.0.2) é exatamente essa restrição.
- **Scriptwriting: Draft → Reinforce → Refine → Visuals → Reflect** (rode `draft reinforce refine visuals reflect escrever hook para cada estagio de awareness heaven and hell`) — o roteiro em 5 passagens, com um hook por estágio de awareness e o contraste heaven/hell calibrando o corpo.

**Para o HOOK (0-3s) — sistemas de maior impacto:**
- **Hook Writing Framework — 3 Functions of a Hook** (rode `hook framework 3 functions ad video stop scroll create curiosity`) — stop scroll, criar curiosidade, set up o ângulo.
- **Gap Theory of Curiosity** (rode `gap theory of curiosity hooks counterintuitive open loop slippery slope`) — abrir loop que o avatar precisa fechar (nunca explicar no hook).
- **Hook Patterns — This-is-X / Timeline+Outcome / Percentage+Promise / Identity Match** (rode `hook patterns this is X timeline percentage identity match POV`) — bancos de padrão prontos pra variar #1/#2/#3.
- **Hopkins' Specificity Rule / 1-2 Second Rule** (rode `Hopkins specificity rule 1-2 second rule vague vs specific claims`) — "47% em 14 dias" > "resultados rápidos".
- **Hook-Specificity-for-Video Rule** (rode `hook specificity rule video specific sub-avatar hooks generic universal hold POV`) — hook específico por sub-avatar, hold universal.
- **Tipos de hook clip × estágio de awareness + enhancers** (rode `tipos de hook clip clickbait ideal outcome weird clip problema produto pareamento por estagio`) — o catálogo de clipes de abertura (clickbait, ideal outcome, clipe estranho, problema, produto) pareado com o estágio de awareness travado do conceito, mais os enhancers — decide O QUE aparece no primeiro beat, não só o que é dito.

**Para BRIDGE → HOLD → CTA (estrutura do corpo):**
- **4-Section Video Ad Structure (Hook / Bridge / Hold / CTA)** (rode `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`) — timing canônico das 4 seções.
- **Objection → Claim → Proof → Benefit cycle (the Hold)** (rode `objection claim proof benefit cycle hold section one cycle`) — o ciclo que estrutura cada beat do Hold.
- **Slippery Slope Principle** (rode `slippery slope principle open loops pattern interrupt end with intrigue video script`) — cada frase compele a próxima (Sugarman).
- **Schwartz Five Stages of Awareness** (rode `Schwartz five stages of awareness unaware problem solution product most aware headline approach`) — calibra a abordagem do script ao awareness travado do conceito (Hard Rule A.0).

**Para HEADLINES (abaixo do criativo):**
- **Caples' Four U's Hierarchy** (rode `Caples four U's hierarchy unique useful urgent ultra-specific headlines`) — Unique / Useful / Urgent / Ultra-Specific.
- **The Big 4 Emotions (NEW/ONLY, EASY/ANYBODY, SAFE/PREDICTABLE, BIG/FAST)** (rode `Big 4 Emotions NEW ONLY EASY ANYBODY SAFE PREDICTABLE BIG FAST`) — framework de EMOÇÃO DE HEADLINE da base. Não confundir com as 4 Hook Emotions do gate E (curiosity/urgency/fear/delight), que marcam o hook.

**Para PRIMARY TEXTS / proof / fechamento — puxar conforme o ângulo do conceito:**
- **Cialdini's Six Weapons of Influence** (rode `Cialdini six weapons of influence reciprocity commitment social proof authority liking scarcity`).
- **Blair Warren's One-Sentence Persuasion** (rode `Blair Warren one sentence persuasion encourage dreams justify failures allay fears confirm suspicions throw rocks enemies`).
- **Future Pacing** (rode `future pacing copywriting commitment consistency imagine your life with the product better self`).

**Formato do briefing:**

---

# BRIEFING DE CONCEITO #[N]

**Conceito / Big Idea:** [nome do conceito + a ideia unificadora em 1 frase]
**Embalagem (`concept_type`):** [problem / result / curiosity / social / authority / comparison / controversy / identification — a estratégia do teste, o que VOCÊ quer aprender]
**Método de teste:** [**Marksman** (3 ângulos, achar direção) / **Sniper** (1 ângulo, 3 execuções)] — [1 frase de justificativa pela matriz da ETAPA 4.5.A.0.1]
**Persona / Micro-persona:** [`sub_avatars[].name` + `id` da Skill `market-research`, ex: "the magnesium tried-it" (sa-01)] — [as categorias que ela combina, em 1 frase legível: "quer dormir a noite inteira; já tentou magnésio e continuou acordando cansada"]
**Ângulo:** [**frase completa que dá a razão de compra**, vinda de `sub_avatars[].angle`. Ex: "you're still waking up tired even after the magnesium". Se Marksman, listar os **3** ângulos, um por criativo]
**Labels de call-out:** [os apelidos do mercado (`labels[]` da Skill `market-research`) usados no primeiro beat, ex: "light sleepers"]
**Avatar:** [quem grava/aparece/fala no ad — e por que ESSA pessoa é crível pra ESSA persona. Ex: "mulher 50s, aparência real (não modelo), tom de amiga que passou por isso"]
**Tema:** [o assunto que a copy ataca. Ex: "o custo anual acumulado das alternativas"]
**Zona emocional (Valence × Intensity):** [zona de abertura: 1 acolhimento / 2 entusiasmo / 3 incômodo / 4 alerta] → **Arco:** [`valence_open` → `valence_close`, ex: "negative/high → positive/low"] — fecha sempre em valência alta (exceção declarada: image ad de curiosidade cujo arco sobe na LP)
**Benefício ou Consequência:** [qual dos dois o ad vende, declarado. Ex: "consequência — mais um ano de noites cortadas se nada mudar"]
**Vertical:** [competitiva / consumidor / interna]
**Awareness Level:** [Unaware / Problem Aware / Solution Aware / Product Aware / Most Aware]
**Posição no Funil:** [TOF / MOF / BOF]
**Formato Principal:** [UGC vídeo / demo vídeo / static / carrossel / motion graphics]
**Senso Estético:** [referência de design/edição: caseiro vs polido, fontes, ritmo de cortes (a cada quantos segundos algo muda), paleta]
**Molde** (só quando o conceito usa molde de `competitor-analysis/ad-molds.json`): [`mold_id` + concorrente + o sinal de escala do `evidence` + a frase do encaixe entre a função do molde e o ângulo deste conceito — `reference/molde-e-injecao.md`]
**Estrutura Invisível:** [1 linha por dimensão — psicológica (sequência de objeções que derruba), emocional (o arco de valência: em que zona abre, o que segura na bridge, em que zona fecha), visual (onde estão os pattern interrupts), comunicativa (o que é falado vs overlay)]

---

## 3 CRIATIVOS (o que varia depende do método)

**Hard Rules (ETAPA 4.5.A.0.2):** os 3 criativos são o MESMO conceito, MESMO formato (3 vídeos OU 3 imagens), MESMO awareness, MESMO intent — nos dois métodos. O ângulo é a única regra que muda:

- **Se `sniper`:** MESMO ângulo nos 3. Varia só hook/abertura/visual inicial. Hold **específico e profundo**, colado nesse ângulo (mostra comportamento/experiência/emoção do sub-avatar). Body, mecanismo, prova e CTA idênticos entre os 3.
- **Se `marksman`:** **3 ângulos distintos**, um por criativo, sobre um **hold universal** ancorado no `core_avatar.surface_desire`. Fórmula: hooks mais específicos + hold mais genérico. Declare aqui o hold universal e a validação contra os 3 hooks (`hold_universal_validated`) — hold que não sustenta algum dos 3 ângulos reprova o conceito.

Formato/awareness/intent diferente = 3-2-2 separado (outro conceito), em qualquer método.

### Criativo #1

**Tipo:** [vídeo UGC / vídeo demonstração / imagem estática / carrossel / motion graphics]

**SE VÍDEO (script segundo-a-segundo):**

**Conceito com molde:** os beats abaixo são os slots do molde, com o tempo, a função, o tipo de frase e o orçamento de palavras de cada um, e a duração alvo é o `duration_s` dele. A tabela de mapeamento e a nota técnica das pendências estão em `reference/molde-e-injecao.md`. Sem molde, valem as quatro seções e a duração escolhida por posição de funil, como abaixo.

Duração alvo: [15s / 22s / 30s — baseada em posição de funil; TOF mais curto, BOF pode ser mais longo]

Estrutura: Hook → Bridge → Hold → CTA (framework)

- **[00:00-00:03] HOOK**
  - **Texto/fala EXATA**: "[texto literal — 1-2 frases]"
  - **Visual**: [descrição do que aparece na tela]
  - **Text overlay** (se houver): "[texto]"
  - **Ângulo que este hook abre**: "[a frase de razão de compra — no Sniper é o mesmo dos 3; no Marksman é o ângulo específico deste criativo]"
  - **Zona emocional**: [valence positive|negative × intensity low|high] + **4 Hook Emotions dominante**: [curiosity / urgency / fear / delight]
  - **Call-out** (se houver): [label do mercado usado no primeiro beat]
  - **Força do hook em parar o scroll (thumbstop) esperada**: (estimativa 1-10 baseada em força do hook)

- **[00:03-00:08] BRIDGE** (transição do hook pro corpo)
  - **Texto/fala**: "[texto]"
  - **Visual**: [descrição]
  - **Função**: [estabelecer credibilidade / apresentar problema / mostrar o pattern interrupt]

- **[00:08-00:18] HOLD** (desenvolvimento — mecanismo, proof, benefit)
  - **Texto/fala**: "[texto]"
  - **Visual**: [descrição]
  - **Aplicação do slippery slide**: cada frase deve compelir a próxima (Sugarman)
  - **Proof element presente**: [testimonial / número específico / demo / authority]

- **[00:18-00:22] CTA**
  - **Texto/fala**: "[texto — call to value, não call to action: 'Get my [outcome]' > 'Shop now']"
  - **Visual**: [CTA text overlay + produto em tela + badge de garantia]
  - **Fechamento do arco emocional**: [a zona em que o ad TERMINA — tem que ser valência alta (segurança/confiança). Se o hook abriu em alerta, aqui está o reasseguramento que fecha; salto brusco de pânico pra euforia não cola]

**Música/SFX:** [tipo de música ou "sem música" — background que não distrai]
**Precisa de voiceover ElevenLabs?** [sim/não — UGC é geralmente não; demo/motion graphics é sim]
**Se sim, script de voiceover separado:**
```
[script completo e humanizado da locução — contrações, pausas naturais, frases curtas, pra não soar robotizado]
```

**SE IMAGEM** (puxe os sistemas nomeados de static — rode a `best_query` exata, índice em `.claude/lib/kb-index/`):
- **Static/Image Archetypes by Funnel Position** (rode `static image archetypes funnel position plain reminder direct response complexity rule`) — escolhe o archetype certo pra posição de funil do conceito.
- **13+ Winning Static Ad Templates (named breakdowns)** (rode `13 winning static ad templates avatar callout nutella meme breakdown why it works`) — templates nomeados (avatar callout, meme, etc).
- **Show Don't Tell / 'ugly ads convert'** (rode `show don't tell behavioral change when telling aren't selling spoken language video`) — quando o "ugly ad" cru bate o product shot polido.

**Se a imagem tem PESSOA fotorrealista** (review de PDP, "closer look", UGC estático, pessoa aplicando/segurando o produto): as regras de `.claude/lib/prompt-directors/real-people-imagery.md` são OBRIGATÓRIAS no prompt — pessoa crível (nunca modelo), públicos distribuídos por pesquisa (nunca lote homogêneo), zero pele exposta, embalagem real por referência anexada, specs de câmera/luz, contexto imperfeito, ratio pelo destino — mais o pós-processo (limpeza de metadados + review do lote).

- **Descrição visual principal**: [o que aparece — produto + contexto + modelo se houver]
- **Texto overlay principal** (hook): "[texto grande]"
- **Textos secundários**: "[subheadline ou benefits]"
- **CTA visual**: "[texto do botão/badge visual]"
- **Estilo**: [clean product shot / lifestyle / ugly ad / meme-style — "ugly ads convert" principle]
- **Elementos de proof**: [rating stars / review count / featured-in badges / guarantee shield]

### Criativo #2

**Se `sniper` — [Variação: hook/abertura diferente]:** MESMO formato, MESMO awareness, MESMO ângulo do #1. Varia só o hook e o visual de entrada (primeiro beat se vídeo). Se #1 é vídeo UGC, #2 também é vídeo UGC — nunca troca pra imagem ou demo. Body, mecanismo, prova e CTA seguem coerentes com #1.

**Se `marksman` — [Ângulo #2]:** MESMO formato, MESMO awareness, MESMO intent, e o **mesmo hold universal** do #1. O que muda é o **ângulo**: hook e abertura abrem uma razão de compra diferente sobre o mesmo hold. Declare o ângulo em frase e confirme que o hold universal o sustenta.

### Criativo #3

**Se `sniper` — [Variação: hook/visual inicial diferente]:** MESMO conceito, MESMO formato, MESMO awareness. Terceira execução variando só a abertura/visual de entrada.

**Se `marksman` — [Ângulo #3]:** terceiro ângulo distinto sobre o mesmo hold universal, mesmo formato e mesmo awareness.

Em qualquer método, testar **formato**, **awareness** ou **intent** diferente é um 3-2-2 SEPARADO, nunca o criativo #3.

---

## 2 PRIMARY TEXTS (Meaningfully Different)

**IMPORTANTE**: Não são variações cosméticas. Cada primary text usa ESTRUTURA, ENTRADA e ZONA EMOCIONAL diferentes. O **ângulo do conceito não muda aqui** (ele é variável do criativo, não do texto): em `sniper` os dois textos servem o mesmo ângulo por caminhos diferentes; em `marksman` os dois textos precisam funcionar sob o hold universal, servindo qualquer um dos 3 ângulos. Para static de sub-avatar, o primary text puxa mais para o `core_avatar.surface_desire` (mais geral) — o recorte fino já está na imagem.

### Primary Text 1 — [Variante A: estrutura + zona emocional]

[Copy completa — 100-300 palavras]

Estrutura:
- Hook (primeira linha acima do "See more")
- Corpo (dor/solução/mecanismo/proof/oferta)
- CTA linha final

### Primary Text 2 — [Variante B: estrutura e zona diferentes de A]

[Copy completa — estrutura diferente. Se A abriu em valência baixa, B pode abrir em valência alta com a mesma informação — é a variação mais barata de zona que existe]

---

## 2 HEADLINES (Abaixo do Vídeo/Imagem)

Duas headlines que representam hipóteses diferentes. Cada uma é um frame de valor real.

- **Headline 1**: "[texto — max 40 chars ideal]" — frame: [benefício / urgência / offer / pergunta]
- **Headline 2**: "[texto]" — frame: [frame diferente]

---

## URL DE DESTINO

**Destino**: [PDP / Landing Page / Advertorial]

**Justificativa de congruência**:
- Message match: [como o ad conecta com o headline da LP]
- Visual match: [tom visual bate entre ad e LP?]
- Promise match: [a promessa do ad é mantida/expandida na LP, não trocada]

Se o conceito é TOF (cold traffic, awareness low), a LP precisa de mais educação → recomendar advertorial ou LP dedicada. Se é BOF/retargeting (warm), PDP direto funciona.

---

## RACIONAL ESTRATÉGICO

- **Por que esse conceito**: [1-2 frases justificando a aposta com base em market research/competitor analysis]
- **O que esperamos aprender**: [a pergunta que esse teste responde, escrita conforme o método — **Marksman**: "qual dos 3 ângulos o mercado favorece?" · **Sniper**: "esta execução extrai mais do ângulo [X] do que a anterior?"]
- **Success criteria**: [ex: CPA dentro do target em 3-7 dias; thumbstop > 5; CTR > 1.5%. Leitura de resultado e classificação (loser / KPI winner / spend winner / breakthrough) e as réguas de Hook/Hold são do cânone `.claude/lib/ad-taxonomy/README.md` §2 e §4, aplicadas pela Skill `ad-analysis` — esta skill não redefine]

---
