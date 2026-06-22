---
name: market-research
description: Engine profundo de pesquisa de mercado que produz o Unified Research Brief — o documento mais importante do sistema. Use quando o membro disser "market research", "pesquisa de mercado", "pesquisar mercado", ou quando a fase de product research estiver completa e o membro quiser aprofundar num produto específico. Este documento alimenta TODAS as fases seguintes (offer, copy, criativos, ad strategy). Se for raso, tudo depois será raso.
---

# Market Research Engine

## Quando Usar
Quando o membro tem produto definido e precisa entender profundamente o mercado, o público, e o cenário competitivo antes de criar oferta e copy. Esta é a fundação de toda a máquina — um product research superficial ou ausente é aceitável em alguns casos, mas market research superficial **garante** que copy, criativos, e ads sejam genéricos e ineficazes.

## Antes de Começar

1. Leia `workspace/profile.md` pra contexto do membro. Leia `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.
2. Se existir `workspace/[produto]/01-product-research/relatorio.md`, leia — tem dados preliminares úteis (dores, linguagem, concorrentes identificados, awareness/sophistication preliminar)
3. **Puxe os SISTEMAS NOMEADOS da base — NUNCA use query genérica.** Para cada ETAPA abaixo, rode `search_knowledge` com a `best_query` exata de cada framework relevante listado naquela etapa (deep=true). Não busque por "market research" ou "pesquisa de mercado" solto — busque pelo NOME do sistema (ex: `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware`). Aprofunde em cada método até entender o "por quê" de cada passo. Este documento é a FUNDAÇÃO de todo o sistema — se for raso, tudo que vier depois será raso.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, mapa skill→domínio no README). Esta skill cruza dois domínios: **market-research-voc** (43 sistemas) e **persuasion-psychology** (49 sistemas). Os frameworks de maior impacto estão embutidos nas ETAPAS abaixo com sua `best_query`; o restante do domínio fica disponível no índice. Quando uma etapa precisar de mais profundidade do que os frameworks listados, consulte o índice e puxe o sistema nomeado certo — nunca caia em query genérica.

## Fluxo da Skill

### ETAPA 0 — Pre-flight

1. Leia `workspace/profile.md`. Se ausente → aborte, mas ofereça rodar o setup inline: `"Não achei seu profile. Rode \`setup\` agora (eu conduzo) e volto pra cá."`
2. Leia `workspace/[produto]/manifest.json` (descubra `[produto]` a partir do manifest — único `manifest.json` com `setup_complete === true`). Se ausente → aborte, mas ofereça rodar o setup inline: `"Não achei o manifest. Rode \`setup\` agora (eu conduzo) e volto pra cá."`
3. Valide que `"01-product-research"` está em `manifest.skills_completed` E que `workspace/[produto]/01-product-research/relatorio.md` existe. Se faltar qualquer um → NÃO aborte seco; ofereça ≥2 caminhos: **(A)** rodar `product research` agora pra gerar o arquivo, OU **(B)** prosseguir com default genérico (sem dados preliminares de dores/linguagem/awareness) marcando `manifest.skipped_preflight += ["01-product-research"]` e avisando no output final que recomenda rodar `product research` e re-executar esta skill.
4. **Rejeitar slug placeholder:** se `product_slug` começa com `dev-placeholder-` → NÃO aborte seco; ofereça ≥2 caminhos: **(A)** rodar `product research` agora pra definir o `product_slug` real, OU **(B)** prosseguir com o produto que o membro descrever inline (sem validação prévia) marcando `manifest.skipped_preflight += ["product-validation"]` e avisando no output final.
5. Use `product_slug` do manifest como `[produto]` pra todos os paths daqui pra frente.

### ETAPA 1 — Confirmar Produto + Mercado Geográfico

Verifique `workspace/profile.md` se já tem `Link do produto principal`.

**SE o profile tem link do produto (ou veio da fase de product research):**
- Confirme: "Vou fazer o market research pro [produto]. Correto?" — espere só "sim" ou correção.

**SE NÃO tem link de produto:**
- Pergunte: "Me descreva o produto: o que é, o que faz, pra quem é, e o link se tiver."

Depois (em qualquer um dos casos acima), pergunte:
- "Qual o mercado geográfico principal? (US, UK, EU, global)"

Salve o mercado geográfico no documento final da pesquisa — toda a análise de awareness, sofisticação, VOC, etc. deve considerar esse mercado específico. Costumes de compra, objeções culturais, e linguagem variam enormemente entre mercados. Se o membro disser "global", analise o mercado anglo-saxão (US+UK+AU+CA) como default.

### ETAPA 2 — Product-Market Awareness Analysis (5 Níveis de Schwartz)

**Sistemas a puxar da base antes de estimar (rode cada `best_query`):**
- **Eugene Schwartz — 5 Stages of Awareness** (rode `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware`)
- **Awareness TAM Distribution (1/13.5/60/99% pyramid)** (rode `awareness levels percentage TAM distribution problem aware unaware easiest convert`) — calibra a distribuição numérica do TAM
- **Awareness Stage Headline Strategy (5 stages + 7 superiority tasks)** (rode `Schwartz awareness stage headline strategy seven tasks superiority approaches`) — alimenta as implicações de copy por nível
- **Deep Research AI Prompt (Awareness assessment)** (rode `deep research AI prompt market awareness TAM distribution Schwartz levels geography`) — estrutura a estimativa por geografia
- **Schwartz↔TTM↔Brunson Awareness Mapping Table** (rode `Schwartz TTM Brunson awareness mapping table copy approach by stage`) — cruza awareness com abordagem de copy/temperatura de tráfego

Pesquise (web search) sinais de cada nível de awareness:
- Volume de busca por termos do problema (Google Keyword Planner, trends)
- Volume de busca por termos da categoria de produto
- Ratio: busca por problema / busca por produto indica distribuição de awareness
- Social chatter: Reddit, TikTok, Twitter — as pessoas falam do problema, da solução, ou da marca específica?
- Artigos, blog posts, conteúdo de influencers no nicho

**Estime a distribuição do TAM por nível** (em porcentagem):
- X% Unaware (não sabe do problema)
- X% Problem Aware (sabe do problema, não sabe de soluções)
- X% Solution Aware (conhece soluções genéricas)
- X% Product Aware (conhece categoria de produto)
- X% Most Aware (conhece sua marca especificamente)

**Defaults por categoria** — se o membro não sabe estimar e a web search não trouxer sinais suficientes, pergunte em qual bucket o nicho se encaixa e aplique o default correspondente (marque `awareness_distribution_source = "default"` no JSON companion):

| Bucket | unaware | problem_aware | solution_aware | product_aware | most_aware |
|---|---|---|---|---|---|
| Nicho novo | 45 | 35 | 13 | 6 | 1 |
| Nicho maduro | 15 | 32 | 35 | 15 | 3 |
| Commodity saturado | 8 | 25 | 40 | 22 | 5 |

> **Nota Schwartz:** o grosso do mercado vive quase sempre em **problem_aware** ou **solution_aware** — é onde estão a maioria dos compradores que ainda não escolheram marca. `product_aware` é tipicamente 5-15% (já conhece a categoria) e `most_aware` é tipicamente só 1-5% (já conhece sua marca específica). Desconfie de qualquer distribuição que jogue 10%+ em `most_aware` num produto que ainda não tem brand reconhecida — isso quase nunca é real e infla a expectativa de quem chega pronto pra comprar.

Se o membro der um palpite, mas a pesquisa web sugerir algo diferente, use **hybrid**: média entre palpite e default (marque `awareness_distribution_source = "hybrid"`).

Defina onde está a **maioria** (50%+) do mercado. Este nível vai ditar TODA a estratégia de copy, página, e criativos.

**Implicações práticas a documentar:**
- Problem Aware → advertorial ou listicle obrigatório (educação antes do pitch). PDP direta NÃO converte.
- Solution Aware → landing page dedicada com educação sobre diferenciação + mecanismo único forte.
- Product Aware → PDP robusta com comparação, reviews, garantia, proof stacking.
- Most Aware → PDP enxuta com foco na oferta (preço, bundle, urgência).

### ETAPA 3 — Market Sophistication Analysis (5 Estágios)

**Sistemas a puxar da base antes de classificar o estágio (rode cada `best_query`):**
- **Eugene Schwartz — 5 Stages of Market Sophistication** (rode `market sophistication five stages Schwartz mechanism claim escalation jaded market`)
- **Three Strategic Responses for Sophisticated Markets (New Mechanism / New Information / New Identity)** (rode `New Mechanism New Information New Identity three strategic responses sophisticated markets`) — define a resposta estratégica certa pros estágios 3/4/5
- **Market Sophistication Headline Templates (by stage)** (rode `market sophistication headline templates by stage markets retrace insight cigarette cycle`) — ancora os claims comuns/saturados de cada estágio
- **Schwartz Deadly Sincerity & The Turn** (rode `Schwartz deadly sincerity damaging admission product flaw the turn transition believability`) — recurso pra estágio saturado onde claims diretos morreram

Analise o mercado através dos claims dos concorrentes identificados no product research:

- **Quantos produtos/soluções similares já existem?** (contagem de marcas ativas com ads escalados)
- **Quais claims já foram feitos?** Liste os 10-15 principais claims do mercado
- **Em qual estágio está?**:

| Estágio | Características | Resposta Estratégica |
|---|---|---|
| **1** | Virgin market. Produto novo, crowd não conhece a categoria | Claim direto simples: "X faz Y" |
| **2** | Claim direto com superlativo ainda funciona | "MAIS efetivo", "MAIS rápido", "MAIS barato que concorrentes" |
| **3** | Claims diretos saturados — precisa de **mecanismo único** | Nome proprietário de ingrediente/processo/tecnologia |
| **4** | Mecanismos saturados — precisa de **nova informação** | Descoberta recente, causa-raiz nova, expansão de mecanismo existente |
| **5** | Tudo saturado — precisa de **identificação** | Falar com quem a pessoa quer SER, não com o problema funcional |

Liste:
- **Claims saturados a EVITAR** (todo concorrente usa)
- **Claims comuns** (maioria usa, usar com twist próprio)
- **Claims raros** (poucos usam, oportunidade)
- **Claims ausentes** (ninguém usa, oportunidade forte)

Defina a resposta estratégica certa pro estágio identificado.

### ETAPA 4 — Perfil Psicográfico Profundo

**Sistemas a puxar da base antes de construir o perfil (rode cada `best_query`):**
- **Psychographic Research — Decision Drivers (RMBC R-stage questions)** (rode `psychographic research decision drivers struggles pain points beliefs RMBC research questions`) — estrutura as perguntas de pesquisa que extraem hopes/failures/beliefs
- **Eugene Schwartz — Mass Desire Theory (3-Stage Channeling)** (rode `mass desire Schwartz channeling process amplification effect cannot create desire`) + **Desire Power Ranking — Scope / Urgency / Staying Power** (rode `mass desire scope urgency staying power power ranking choose strongest`) — hierarquiza desejos por força, não por arbitrariedade
- **Surface Desire vs Core Desire** (rode `surface level desire vs core desire why behind the desire avatar building`) — alimenta "o desejo POR TRÁS do desejo"
- **Core Avatars & Sub-Avatars — The Core Five Categories** (rode `core avatar sub avatar core five categories desire experience emotion behavior demographic`) + **Desire-First Avatar (over Demographics)** (rode `desire first avatar over demographics avoid combining desires single desire core avatar`) — constrói o avatar a partir do desejo, não da demografia
- **Prejudices & Core Beliefs (Institutional / Age / Product biases)** (rode `market prejudices core beliefs institutional bias age bias product bias worldview`) — alimenta Prejudices & Biases + Core Beliefs
- **Corruption Angle — Paradise Lost** (rode `corruption angle paradise lost outside forces worsened pain point nostalgia indignation`) — alimenta External Forces Blamed (quem a pessoa culpa)
- **Jobs To Be Done — The Switch & Four Forces** (rode `Jobs to be Done switch push pull anxiety habit four forces Moesta Christensen`) — mapeia push/pull/anxiety/habit, base de Victories & Failures e Trigger Events
- **Existing Solutions Analysis (failed solutions mapping)** (rode `existing solutions analysis failed solutions why they didnt work solution landscape mapping`) — cada solução falha vira objeção potencial
- **Cashvertising — Life-Force 8 (LF8)** (rode `Cashvertising Life-Force 8 LF8 biologically hardwired desires Whitman`) — checa que o desejo principal ancora num drive biológico, não num want aprendido raso
- **Plutchik Emotion Wheel + Secondary-Emotion Frequency Tiers** (rode `Plutchik emotion wheel secondary emotions frequency tiers marketing utility`) — nomeia as dores emocionais com precisão (vergonha, frustração, invisibilidade)

Pesquise extensivamente em Reddit, Amazon reviews, TikTok comments, fóruns de nicho, Quora, Trustpilot, grupos do Facebook. Use as técnicas de review mining.

> **Coleta resiliente (rule `.claude/rules/resilient-fetch.md`):** descubra fontes com a tool **`WebSearch`** (nunca scrapear HTML de buscador — vira CAPTCHA). Busque páginas com **`WebFetch`**. Se barrar (403/429/Cloudflare/JS), use o **fetcher Playwright da Aura**: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode reddit|reviews|text --json` — **Reddit** sempre `--mode reddit` (via redlib, contorna o bloqueio de IP); **Amazon/Trustpilot/Loox** com `--mode reviews`. Se mesmo o fetcher cair em hard-CAPTCHA (ex: Walmart), use fonte redundante (Amazon cobre o mesmo produto) ou peça paste ao membro. **NUNCA inventar VOC** — fonte que caiu em todos os fallbacks vai no Data Quality Summary como bloqueada.

Construa o perfil em camadas:

**Demographics (superficial mas necessário):**
- Idade, gênero, renda, localização, estado civil, escolaridade, ocupação típica

**Psychographics (a parte que REALMENTE importa):**

- **Hopes & Dreams** — o estado futuro ideal ESPECÍFICO. NÃO genérico como "perder peso" — específico como "poder vestir o vestido que usei no casamento da minha prima sem medo de me olhar no espelho depois". A especificidade vem da linguagem real do consumidor.

- **Victories & Failures** — o que já tentaram, o que funcionou parcialmente, o que falhou completamente e POR QUÊ. Esta seção é ouro: cada coisa que falhou é uma objeção potencial, cada coisa que funcionou parcialmente é uma ponte pra posicionar seu mecanismo único.

- **External Forces Blamed** — quem/o que eles culpam. Genética, hormônios, indústria de beleza, médicos, sistema capitalista, envelhecimento, falta de tempo. Esta informação entra direto na "corruption angle" da copy (mecanismo que externaliza a culpa).

- **Prejudices & Biases** — contra quais tipos de produto ou abordagem são céticos. "Suplementos são scam", "cremes são placebo", "dietas não funcionam". Esses vieses precisam ser ENDEREÇADOS, não ignorados.

- **Core Beliefs** — sobre saúde, beleza, envelhecimento, investimento em si mesmo, relacionamentos. Moldam aceitação/rejeição de claims.

- **The Paradox** — a tensão entre ceticismo e esperança. Não acreditam que nada funciona MAS continuam procurando. Essa tensão é a energia por trás da decisão de compra.

**Pain Points hierarquizados:**
- **Dor principal** (a razão #1 que a pessoa acorda pensando)
- **Dores secundárias** (3-5 dores adjacentes)
- **Dores emocionais** (como se sentem POR CAUSA do problema — vergonha, frustração, invisibilidade, perda de confiança)
- **Dores sociais** (como afeta relacionamentos, vida social, auto-imagem em público)
- Frequência de menção (alta/média/baixa) pra priorizar

**Desires hierarquizados:**
- **Desejo principal** (o resultado específico que querem)
- **Desejos secundários**
- **O desejo POR TRÁS do desejo** — o que realmente querem no nível mais profundo (ex: "perder 10kg" → o que querem é "sentir-se desejada de novo" → o que querem MESMO é "voltar a ser quem eram antes do parto")
- Intensidade (alta/média/baixa)

**Objeções com prioridade:**
- **Preço** — "muito caro pra tentar sem saber se funciona"
- **Eficácia** — "já tentei X e não funcionou"
- **Segurança** — "vai machucar?", "efeito colateral?"
- **Esforço** — "é complicado de usar?", "vou desistir?"
- **Ceticismo** — "mais um scam"
- **Identidade** — "produto não é pra alguém como eu"

Pra cada objeção, sugira **como quebrar** puxando os sistemas de persuasão NOMEADOS da base (rode cada `best_query`), não fórmulas genéricas:
- **Cialdini's Six Weapons of Influence** (rode `Cialdini six weapons of influence reciprocity commitment social proof authority liking scarcity`) — escolhe a alavanca certa por objeção
- **The 'Yeah, Sure' Principle (Proof Matches Claim)** (rode `Bencivenga yeah sure principle proof match claim three reasons why IF THEN construction doctors headache`) — quebra objeção de eficácia com proof que casa com o claim
- **Inoculation Theory** (rode `inoculation theory McGuire weakened attack pre-emptive defense competitor argument resistance`) — antecipa e neutraliza a objeção antes dela surgir
- **Four-Step Fear Appeal** (rode `four-step fear appeal Pratkanis Aronson scare recommend prove effectiveness accessibility Listerine`) — pra objeção de segurança/inação
- **Schwartz Gradualization / Believability Bridge** (rode `Schwartz gradualization believability bridge belief gap intermediate beliefs Breakthrough Advertising`) — quebra ceticismo construindo crença em degraus
- **Blair Warren's One-Sentence Persuasion** (rode `Blair Warren one sentence persuasion encourage dreams justify failures allay fears confirm suspicions throw rocks enemies`) — quebra objeção de identidade ("não é pra alguém como eu")

**Trigger Events:**
O que faz a pessoa decidir comprar AGORA? Event específico, data, situação, ponto-de-dor agudo:
- Pré-evento (casamento, viagem, encontro de ex-colegas)
- Deadline (aniversário próximo, fim de ano)
- Pico de dor (acordou com dor de novo, viu uma foto, foi rejeitada)
- Social trigger (amiga comentou, viu no TikTok, recomendação médica)

### ETAPA 5 — Voice of Customer (Linguagem EXATA — Mínimo 35 Frases)

**Sistemas a puxar da base antes de minerar (rode cada `best_query`):**
- **Voice of Customer Research (Review Mining / Surveys / Interviews)** (rode `Voice of Customer review mining process extracting verbatim phrases from reviews`) — o processo de extração de frases exatas
- **4-Star Review Mining (avoid 1s and 5s)** (rode `four star reviews mining avoid 5 star 1 star fake reviews honest language`) — onde está a linguagem honesta (evitar 1s e 5s)
- **Google Review-Mining Shortcuts (site:amazon.com inurl product-reviews)** (rode `Amazon review mining google shortcut tired of wasn't until tried site operator`) — operadores de busca pra achar frases rápido
- **Consumer Insights Database (where + what + how to mine)** (rode `consumer insights database mine reviews reddit tiktok ad comments fears desires motivations`) — mapa de fontes (Reddit, TikTok, ad comments)
- **Says-vs-Does (Trust Behavior, Not Surveys)** (rode `says vs does trust purchasing behavior not surveys beer survey national enquirer right answer bias`) — filtra o que as pessoas DIZEM do que realmente FAZEM

Das pesquisas da etapa 4, extraia e organize SEPARADAMENTE. **NUNCA PARAFRASEAR** — capture exatamente como as pessoas falam. Isso vai pra copy e criativos literalmente. **VOC permanece SEMPRE no idioma original do consumidor (inglês US), nunca traduzir** — mesmo com `report_language: "pt-BR"`. É matéria-prima literal; o resto do relatório fica no idioma do membro, as frases não.

- **Frases exatas descrevendo o PROBLEMA** — mínimo 15 frases
- **Frases exatas descrevendo o DESEJO** — mínimo 10 frases
- **Frases exatas descrevendo FRUSTRAÇÕES com produtos existentes** — mínimo 10 frases
- **Palavras e expressões recorrentes** (aparecem 3+ vezes na base de pesquisa)

Essas frases são ouro. Hopkins escreveu em 1923: "a boa copy fala a linguagem do consumidor". Esse é o raw material.

**Fallback quando < 35 frases reais foram coletadas**: **NUNCA** gere frases artificiais/sintéticas/plausíveis. Em vez disso:

1. Documente o déficit explicitamente no output: `"VOC real: N frases únicas; mínimo 35 não atingido."`
2. Liste as fontes tentadas e as que bloquearam acesso.
3. **Classificar severidade do déficit pra alertar skills downstream:**
   - `voc_count >= 35` → OK, segue normal
   - `15 <= voc_count < 35` → `voc_adequacy: "medium"`, skill 06 emite warning mas procede
   - `voc_count < 15` → `voc_adequacy: "insufficient"`. Skill 06 DEVE bloquear no pré-flight — copy sem VOC real não é copy, é invenção. Salvar em `02-market-research/dados.json`: `"voc_adequacy": "insufficient", "skills_blocked": ["06-copy-engine"]`
4. Siga com as etapas restantes (awareness, sophistication, root cause) — essas não dependem de VOC quantity.

Esse déficit é rastreado em `voc_count` + `voc_adequacy` do manifest e do JSON companion (`02-market-research/dados.json`).

### ETAPA 6 — Root Cause Research (Metodologia Zakaria)

**Sistemas a puxar da base pra dar ângulo à causa-raiz (rode cada `best_query`):**
- **Corruption Angle — Paradise Lost** (rode `corruption angle paradise lost outside forces worsened pain point nostalgia indignation`) — molda a causa-raiz como "forças externas corromperam X", externalizando a culpa
- **Curiosity Angle — Rediscovered/Suppressed Solution** (rode `curiosity angle rediscovered suppressed solution historical forgotten wisdom narrative`) — enquadra a descoberta como conhecimento perdido/suprimido (combustível do advertorial)
- **Gap Theory of Curiosity** (rode `Loewenstein gap theory of curiosity knowledge gap open loop highlight what they don't know`) — abre o loop de "o que você não sabe sobre a causa real"
- **Schwartz Mechanization Stages (Mechanism Proof)** (rode `Schwartz mechanization stages name describe feature mechanism promise reason why headline`) — garante que a causa-raiz é nomeável e vira mecanismo provável

Pra cada dor central identificada, faça uma pesquisa de **causa-raiz** que será a fundação do mecanismo único da oferta:

- **Causa superficial** (o que a pessoa acha que é a causa) — ex: "estou comendo muito"
- **Causa intermediária** (o que a ciência ou especialistas apontam) — ex: "resistência à insulina"
- **Causa raiz proprietária** (um ângulo novo baseado em descoberta recente, research, ou combinação única) — ex: "desregulação do ritmo circadiano do eixo hormonal metabólico"

A causa raiz deve ser:
- Real (baseada em ciência, não inventada)
- Nova pro mercado (o público não conhece)
- Específica (pode ser nomeada)
- Externaliza a culpa (não "você comeu muito" mas "seu corpo tá te sabotando POR CAUSA DE X")

Esta causa raiz alimenta o **advertorial de 7 seções** (Seção 4 — Root Cause Explanation) e o **corruption angle** (quem/o que corrompeu a situação: indústria, genética, envelhecimento, hormônios). Documente 2-3 opções de causa raiz pra oferta escolher depois.

### ETAPA 7 — Competitive Landscape (Overview Rápido)

A análise competitiva completa vai na Skill 03. Aqui só um overview pra informar as decisões estratégicas deste documento:

- Quem são os 5-10 maiores concorrentes identificados (ativos em ads, com tração)?
- O que prometem (claim principal de cada)?
- Qual faixa de preço do mercado (min-max-mediana)?
- Qual posicionamento cada um usa (hero, expert, problem-solver, aspirational)?
- **Gaps óbvios** — o que nenhum concorrente está fazendo/prometendo/abordando?

**Soluções alternativas (categorias):** mapeie as categorias de solução que o público usa HOJE pra resolver a mesma dor — não só produtos concorrentes diretos, mas tudo que compete pela mesma decisão (ex: pra skincare anti-rugas: cremes de farmácia, o procedimento na clínica, DIY caseiro, "não fazer nada e aceitar"). Pra cada categoria documente o que o público acha que ela entrega e por que abandona/não escolhe (a fraqueza que sua oferta explora). Isso popula `alternative_solutions` no JSON companion e alimenta o posicionamento "por que nada que você já tentou funcionou".

Esta seção é breve. Skill 03 aprofunda.

### ETAPA 8 — Síntese Estratégica (Unified Research Brief Final)

Consolide tudo num documento **estruturado, navegável, acionável**:

**1. Target Market Overview**
- Demographics resumido
- Mercado geográfico
- Awareness level dominante + distribuição do TAM
- Sophistication stage + claims saturados

**2. Psychographic Profile Completo**
- Hopes, Dreams, Failures, Blamed Forces, Prejudices, Core Beliefs, The Paradox (da Etapa 4)

**3. Pain Points & Desires Hierarquizados**
- Top 5 dores em ordem de intensidade
- Top 5 desejos em ordem de intensidade
- **O desejo mais profundo** (the real want behind the want)

**4. Voice of Customer — Quotes Curadas**
- Top 10 frases mais poderosas que vão direto pra copy (problemas + desejos + frustrações misturadas)

**5. Objeções & Como Quebrar**
- Top 5 objeções priorizadas, cada uma com estratégia de quebra específica

**6. Trigger Events**
- Os 3-5 trigger events mais fortes que levam à compra imediata

**7. Root Cause Candidatas**
- 2-3 opções de causa raiz pro mecanismo único da oferta

**8. Competitive Landscape (Overview)**
- Tabela resumo + gaps identificados

**9. Strategic Implications — Recomendações Acionáveis:**

- **Tipo de página recomendada** (advertorial, landing page, PDP robusta, PDP enxuta) com justificativa baseada em awareness + sophistication
- **Tipo de lead** pra copy (Story Lead, Problem-Solution Lead, Secret Lead, Offer Lead) baseado em awareness
- **Tipo de mecanismo necessário** (direto, ingredient-based, process-based, combinação) baseado em sophistication stage
- **Ângulos de diferenciação mais promissores** (ranqueados) — ângulos que NENHUM concorrente está usando

### Validação Final

Antes de salvar, valide:
- [ ] Voice of Customer tem mínimo 35 frases EXATAS (não parafraseadas)
- [ ] Awareness distribution é numérica (não "a maioria é problem aware" — mas "45% problem aware, 30% solution aware")
- [ ] Sophistication stage tem claims saturados LISTADOS
- [ ] Cada objeção tem estratégia de quebra específica (não genérica)
- [ ] Recomendações finais são acionáveis (não "a copy deve ser emocional" — mas "lead com Story Lead sobre trigger event X, foco em desejo Y, mecanismo Z")

Se alguma validação falhar, aprofunde naquele ponto antes de salvar.

### Data Quality Summary (antes de salvar)

Inclua seção dedicada no `.md` e no `.json`:

```
## Data Quality Summary
- VOC coletado de: Amazon reviews (N), Reddit (N), TikTok comments (N), Trustpilot (N), fóruns (N) = Total N frases únicas
- Fontes tentadas e bloqueadas: [lista, ex: "Trustpilot (Cloudflare)", "Quora (login wall)"]
- VOC minimum atingido? [sim / não — se não, N frases a aquém do mínimo 35]
- Awareness distribution source: [user_estimate / default:<bucket> / hybrid / web_signals]
- Sophistication stage confidence: [high / medium / low] + racional em 1 frase
- Root cause candidatas baseadas em: [peer-reviewed research / specialist consensus / extrapolation]
```

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer-builder/relatorio.md` → `04-offer-builder/relatorio.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).


**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/02-market-research/`.

Salvar TRÊS artefatos:

1. **`workspace/[produto]/02-market-research/relatorio.md`** — fonte canônica para AI das próximas skills
2. **`workspace/[produto]/02-market-research/relatorio.html`** — visualização humana (template ou fallback inline)
3. **`workspace/[produto]/02-market-research/dados.json`** — JSON companion estruturado:

```json
{
  "awareness_distribution": { "unaware": 0, "problem_aware": 0, "solution_aware": 0, "product_aware": 0, "most_aware": 0 },
  "awareness_distribution_source": "default|user_estimate|hybrid|web_signals",
  "dominant_awareness": "problem_aware",
  "sophistication_stage": 3,
  "sophistication_confidence": "high|medium|low",
  "voc_phrases": { "problem": ["..."], "desire": ["..."], "frustration": ["..."] },
  "voc_count": 0,
  "avatar": {
    "demographics": {},
    "psychographics": {},
    "pain_hierarchy": [
      { "rank": 1, "item": "", "emotional_layer": "", "frequency": "high|med|low", "voc_quote": "" }
    ],
    "desire_hierarchy": [
      { "rank": 1, "item": "", "emotional_layer": "", "frequency": "high|med|low", "voc_quote": "" }
    ]
  },
  "trigger_events": [
    { "type": "pre_event|deadline|pain_peak|social", "description": "", "voc_quote": "" }
  ],
  "objections": [
    { "type": "price|efficacy|safety|effort|skepticism|identity", "quote": "", "break_strategy": "" }
  ],
  "alternative_solutions": [
    { "category": "", "perceived_benefit": "", "weakness_exploited": "" }
  ],
  "root_cause_candidates": [],
  "strategic_implications": { "page_type": "", "lead_type": "", "mechanism_type": "", "top_angles": [] }
}
```

> **VOC permanece SEMPRE no idioma original do consumidor (inglês US).** Todos os campos `voc_quote` e `voc_phrases` são matéria-prima literal — nunca traduzir, mesmo com `report_language: "pt-BR"`. Eles vão pra copy e criativos exatamente como o consumidor falou.

Este é o DOCUMENTO MAIS IMPORTANTE. Ele alimenta:
- Skill 03 (`03-competitor-analysis`) — usa gaps e claims identificados
- Skill 04 (`04-offer-builder`) — usa pain points, desires, root cause, mechanism hints
- Skill 06 (`06-copy-engine`) — usa VOC literal, lead type, awareness level, objeções
- Skill 07 (cadeia storefront `07a-page-design` → `07b-page-build`) — usa tudo da copy + proof stacking
- Skill 08 (`08-creative-engine`) — usa trigger events, ângulos, VOC, visual hooks
- Skill 10 (`10-ad-strategy`) — usa awareness pra targeting

**Atualize o `manifest.json`** (fonte única de verdade):

- `voc_count` ← número total de frases VOC únicas coletadas
- `awareness_distribution` ← objeto com os 5 níveis em inteiros 0-100
- `sophistication_stage` ← inteiro 1-5
- `skills_completed` ← adicione `"02-market-research"` (sem duplicar)
- `updated_at` ← timestamp atual ISO-8601 UTC

**Regenera o painel do produto:** `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` do manifest — atualiza o `ABRIR-AQUI.html`).

## Mensagem Final

"Unified Research Brief completo. Este documento é a fundação de tudo — copy, criativos, ads, e página vão puxar direto daqui.

Próximos passos:
- Diga **'competitor analysis'** (skill `03-competitor-analysis`) pra aprofundar no cenário competitivo (PDPs, ads, gaps)
- OU diga **'offer'** (skill `04-offer-builder`) se já quer montar a oferta com mecanismo único, stack, e unit economics

Recomendação: competitor analysis primeiro. A profundidade da análise competitiva afeta diretamente a força do posicionamento."
