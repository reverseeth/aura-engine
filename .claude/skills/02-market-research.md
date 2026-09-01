---
name: market-research
description: Engine profundo de pesquisa de mercado que produz o Unified Research Brief — o documento mais importante do sistema. Use quando o membro disser "market research", "pesquisa de mercado", "pesquisar mercado", quando a fase de product research estiver completa, ou quando o membro JÁ TEM produto definido (situações B/C/D do setup — product research não é pré-requisito pra quem já tem produto). Este documento alimenta TODAS as fases seguintes (offer, copy, criativos, ad strategy). Se for raso, tudo depois será raso.
---

# Market Research Engine

## Quando Usar
Quando o membro tem produto definido e precisa entender profundamente o mercado, o público, e o cenário competitivo antes de criar oferta e copy. Esta é a fundação de toda a máquina — um product research superficial ou ausente é aceitável em alguns casos, mas market research superficial **garante** que copy, criativos, e ads sejam genéricos e ineficazes.

## Antes de Começar

1. Leia `workspace/profile.md` pra contexto do membro. Leia `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma, seguindo o padrão de linguagem simples da regra 0 do `.claude/CLAUDE.md` (nenhuma sigla sem explicação imediata, zero frase de analista comprimida, números estatísticos em palavras, citação VOC em inglês com "tradução livre:" ao lado quando o relatório é pt-BR). **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.
2. Se existir `workspace/[produto]/01-product-research/product-research.md`, leia — tem dados preliminares úteis (dores, linguagem, concorrentes identificados, awareness/sophistication preliminar)
3. **Puxe os SISTEMAS NOMEADOS da base — NUNCA use query genérica.** Para cada ETAPA abaixo, rode `search_knowledge` com a `best_query` exata de cada framework relevante listado naquela etapa (deep=true). Não busque por "market research" ou "pesquisa de mercado" solto — busque pelo NOME do sistema (ex: `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware`). Aprofunde em cada método até entender o "por quê" de cada passo. Este documento é a FUNDAÇÃO de todo o sistema — se for raso, tudo que vier depois será raso.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, mapa skill→domínio no README). Esta skill cruza dois domínios: **market-research-voc** e **persuasion-psychology**. O tamanho de cada domínio é o que estiver no próprio `frameworks.json` — a fonte da verdade é sempre o índice, nunca um número decorado no texto desta skill.
>
> **Contrato de cobertura (regra do kb-index, revisada 2026-09):** a consulta à base é **cobertura do tópico**, não amostra.
> 1. No início de cada ETAPA que consulta a base, abra o `frameworks.json` e **enumere TODAS as entradas dos dois domínios cujo `use_in_skill` inclui a 02**. As queries embutidas nas ETAPAS abaixo são o núcleo mínimo garantido daquela etapa, nunca o teto — entrada relevante pra fase que não está embutida É PARA SER PUXADA do mesmo jeito.
> 2. Rode a `best_query` EXATA de cada entrada relevante à fase, com `deep=true` — é a query curada que traz o sistema completo, nunca query genérica.
> 3. O critério de relevância é por FASE: "esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa. Só descarte o que claramente pertence a outra etapa (e será puxado lá).
> 4. Não repita busca de framework já puxado na mesma sessão — entradas duplicadas entre os dois domínios apontam pro MESMO conteúdo (reuse o resultado).
> 5. Antes de fechar cada ETAPA, releia a lista enumerada do passo 1 e confirme: nenhuma entrada relevante ficou sem puxar. Se ficou, puxe agora.

## Fluxo da Skill

### ETAPA 0 — Pre-flight

1. Leia `workspace/profile.md`. Se ausente → aborte, mas ofereça rodar o setup inline: `"Não achei seu profile. Rode \`setup\` agora (eu conduzo) e volto pra cá."`
2. Leia `workspace/[produto]/manifest.json` (descubra `[produto]` a partir do manifest com `setup_complete === true`). **Se houver MAIS de um** manifest com `setup_complete === true` (membro roda 2+ produtos), NÃO escolha silenciosamente: liste os `product_name` e pergunte em 1 linha qual é o produto-alvo (se o membro já nomeou o produto no trigger, use esse sem perguntar). Se ausente → aborte, mas ofereça rodar o setup inline: `"Não achei o manifest. Rode \`setup\` agora (eu conduzo) e volto pra cá."`
3. Cheque se `"01-product-research"` está em `manifest.skills_completed` (e se `workspace/[produto]/01-product-research/product-research.md` existe). Se estiver → leia os dados preliminares. Se faltar, **ramifique pelo que o membro é**:
   - **Membro que JÁ TEM produto** (`manifest.product_url` preenchido, OU situação B/C/D no profile): skill 01 ausente é o caminho NORMAL — ela existe pra ACHAR produto, não faz sentido pra quem já tem. Siga direto, sem `skipped_preflight`, sem warning e sem recomendar "rodar product research depois". Só não haverá dados preliminares de dores/linguagem/concorrentes (esta skill coleta tudo do zero mesmo).
   - **Membro SEM produto definido** (situação A e/ou sem `product_url`): aí sim a 01 faz falta. NÃO aborte seco; ofereça ≥2 caminhos: **(A)** rodar `product research` agora pra escolher/validar o produto, OU **(B)** prosseguir com o produto que o membro descrever inline marcando `manifest.skipped_preflight += ["01-product-research"]` e avisando no output final que recomenda rodar `product research`.
4. **Rejeitar slug placeholder:** se `product_slug` começa com `dev-placeholder-` → NÃO aborte seco; ofereça ≥2 caminhos: **(A)** rodar `product research` agora pra definir o `product_slug` real, OU **(B)** prosseguir com o produto que o membro descrever inline (sem validação prévia) marcando `manifest.skipped_preflight += ["product-validation"]` e avisando no output final.
5. Use `product_slug` do manifest como `[produto]` pra todos os paths daqui pra frente.

### ETAPA 1 — Confirmar Produto + Mercado Geográfico

Verifique `workspace/profile.md` se já tem `Link do produto principal`.

**SE o profile tem link do produto (ou veio da fase de product research):**
- Confirme: "Vou fazer o market research pro [produto]. Correto?" — espere só "sim" ou correção.

**SE NÃO tem link de produto:**
- Pergunte: "Me descreva o produto: o que é, o que faz, pra quem é, e o link se tiver."

Depois (em qualquer um dos casos acima), confirme o mercado geográfico. Leia `manifest.market` primeiro (o setup grava `"US"` como default) e proponha como default em vez de perguntar do zero:
- "Mercado geográfico principal: **[manifest.market]** — confirma, ou é outro? (US, UK, EU, global)"

Salve o mercado geográfico no documento final da pesquisa E de volta em `manifest.market` (ver seção "Atualize o manifest.json") — toda a análise de awareness, sofisticação, VOC, etc. deve considerar esse mercado específico. Costumes de compra, objeções culturais, e linguagem variam enormemente entre mercados. Se o membro disser "global", analise o mercado anglo-saxão (US+UK+AU+CA) como default.

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
| Nicho maduro | 15 | 30 | 38 | 14 | 3 |
| Commodity saturado | 8 | 25 | 40 | 22 | 5 |

> **Racional do 30/38 no nicho maduro:** os dois níveis do meio ficam a 8pp de distância de propósito — assim o DEFAULT nunca cai sozinho na regra de empate (±5pp) descrita abaixo. Híbrido tem que nascer de sinal REAL da pesquisa (palpite do membro + web signals apertados), nunca do default.

> **Nota Schwartz:** o grosso do mercado vive quase sempre em **problem_aware** ou **solution_aware** — é onde estão a maioria dos compradores que ainda não escolheram marca. `product_aware` é tipicamente 5-15% (já conhece a categoria) e `most_aware` é tipicamente só 1-5% (já conhece sua marca específica). Desconfie de qualquer distribuição que jogue 10%+ em `most_aware` num produto que ainda não tem brand reconhecida — isso quase nunca é real e infla a expectativa de quem chega pronto pra comprar.

Se o membro der um palpite, mas a pesquisa web sugerir algo diferente, use **hybrid**: média entre palpite e default (marque `awareness_distribution_source = "hybrid"`).

Defina o nível **DOMINANTE** — o de maior percentual na distribuição (com os defaults acima, nenhum nível chega a 50%, e tudo bem: dominante = o maior). Se dois níveis adjacentes empatarem (±5 pontos percentuais), trate como híbrido e documente os dois: grave em `dominant_awareness` o nível de **MAIOR intenção de compra** dos dois (o mais avançado no espectro Schwartz — ex: empate problem/solution → `solution_aware`) e o outro em `dominant_awareness_secondary` (campo opcional do dados.json — só existe no empate). As skills 06 e 07a leem esse campo secundário pra tratar a página/lead como híbrido. Este nível vai ditar TODA a estratégia de copy, página, e criativos.

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
- **Buzzword Tally (medição de saturação de mensagem)** (rode `contagem de buzzwords tally +1 cada repeticao medir mensagem saturada fatigada`) — a classificação saturado/comum/raro/ausente abaixo não é palpite, é contagem: +1 a cada repetição do mesmo claim/buzzword nos ads e PDPs coletados. O claim mais contado é a mensagem mais fatigada do mercado. Essa mesma contagem alimenta o `saturated_in_market` do vocabulário na ETAPA 5

Analise o mercado através dos claims dos concorrentes identificados no product research.

**Fallback quando a Skill 01 não rodou (caminho NORMAL pra quem já tem produto — ver ETAPA 0):** não existe lista prévia de claims. Colete AGORA: use a tool `WebSearch` pra identificar os 5-10 concorrentes ativos do nicho (buscas por categoria de produto, marcas citadas na VOC, "best [categoria]" em listicles) e a **Meta Ad Library pública** (`https://www.facebook.com/ads/library/`) pra extrair os claims dos ads ATIVOS de cada um — via `WebFetch`, e se barrar (JS/rate-limit), o fetcher Playwright: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (rule `resilient-fetch.md`). 10-15 claims reais bastam pra classificar o estágio. Essa coleta NÃO é retrabalho: a ETAPA 7 (Competitive Landscape) reaproveita os MESMOS concorrentes e claims — colete uma vez, use duas.

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
- **12-Source Research Methodology (em ordem)** (rode `metodologia de 12 fontes em ordem self onboarding ate customer calls por ultimo`) — a ordem da varredura de fontes desta etapa e da ETAPA 5: começa pelo self-onboarding (o que o membro já sabe — o `profile.md` cumpre esse papel) e deixa as ligações pra clientes por último. Percorra as fontes NESSA ordem em vez de pular direto pra favorita
- **Psychographic Research — Decision Drivers (research-stage questions da metodologia interna de copy)** (rode `psychographic research decision drivers struggles pain points beliefs research questions`) — estrutura as perguntas de pesquisa que extraem hopes/failures/beliefs
- **Avatar Deep Dive Template (14 seções + Visual Cues + Trigger Moments)** (rode `avatar deep dive 14 secoes pain points day to day struggles victories failures beliefs`) — o template que estrutura as camadas do perfil abaixo (pain points, struggles do dia a dia, victories, failures, beliefs, entre outras), mais os blocos de Visual Cues (o que a pessoa VÊ no cotidiano — vira direção visual pra 08) e Trigger Moments (alimenta os Trigger Events desta etapa)
- **Eugene Schwartz — Mass Desire Theory (3-Stage Channeling)** (rode `mass desire Schwartz channeling process amplification effect cannot create desire`) + **Desire Power Ranking — Scope / Urgency / Staying Power** (rode `mass desire scope urgency staying power power ranking choose strongest`) — hierarquiza desejos por força, não por arbitrariedade
- **Surface Desire vs Core Desire** (rode `surface level desire vs core desire why behind the desire avatar building`) — alimenta "o desejo POR TRÁS do desejo"
- **Desire Chain de 4 níveis (Surface → Emotional → Identity → Core)** (rode `desire chain i want so i can so i can core desire quatro niveis`) — a ferramenta pra descer do desejo de superfície ao core desire: encadeie "I want… so I can… so I can…" até o quarto nível (superfície → emocional → identidade → core). É como o "desejo POR TRÁS do desejo" é encontrado na prática, nível a nível, em vez de num salto de intuição
- **Core Avatars & Sub-Avatars — The Core Five Categories** (rode `core avatar sub avatar core five categories desire experience emotion behavior demographic`) + **Desire-First Avatar (over Demographics)** (rode `desire first avatar over demographics avoid combining desires single desire core avatar`) — constrói o avatar a partir do desejo, não da demografia
- **Prejudices & Core Beliefs (Institutional / Age / Product biases)** (rode `market prejudices core beliefs institutional bias age bias product bias worldview`) — alimenta Prejudices & Biases + Core Beliefs
- **Corruption Angle — Paradise Lost** (rode `corruption angle paradise lost outside forces worsened pain point nostalgia indignation`) — alimenta External Forces Blamed (quem a pessoa culpa)
- **Jobs To Be Done — The Switch & Four Forces** (rode `Jobs to be Done switch push pull anxiety habit four forces Moesta Christensen`) — mapeia push/pull/anxiety/habit, base de Victories & Failures e Trigger Events
- **Existing Solutions Analysis (failed solutions mapping)** (rode `existing solutions analysis failed solutions why they didnt work solution landscape mapping`) — cada solução falha vira objeção potencial
- **Answer The Public + AnswerSocrates (pesquisa de perguntas)** (rode `answer the public answersocrates aba amazon perguntas objecao advertorial`) — a rota Google da varredura por plataforma: as perguntas reais que o público digita (inclusive a aba de perguntas da Amazon nessas ferramentas) viram as objeções desta etapa e pautas de advertorial pra causa-raiz da ETAPA 6
- **Cashvertising — Life-Force 8 (LF8)** (rode `Cashvertising Life-Force 8 LF8 biologically hardwired desires Whitman`) — checa que o desejo principal ancora num drive biológico, não num want aprendido raso
- **Plutchik Emotion Wheel + Secondary-Emotion Frequency Tiers** (rode `Plutchik emotion wheel secondary emotions frequency tiers marketing utility`) — nomeia as dores emocionais com precisão (vergonha, frustração, invisibilidade)

Pesquise extensivamente em Reddit, Amazon reviews, TikTok comments, fóruns de nicho, Quora, Trustpilot, grupos do Facebook. Use as técnicas de review mining.

> **Coleta resiliente (rule `.claude/rules/resilient-fetch.md`):** descubra fontes com a tool **`WebSearch`** (nunca scrapear HTML de buscador — vira CAPTCHA). Busque páginas com **`WebFetch`**. Se barrar (403/429/Cloudflare/JS), use o **fetcher Playwright da Aura**: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode reddit|reviews|text --json` — **Reddit** sempre `--mode reddit` (via redlib, contorna o bloqueio de IP); **Amazon/Trustpilot/Loox** com `--mode reviews`. Se mesmo o fetcher cair em hard-CAPTCHA (ex: Walmart), use fonte redundante (Amazon cobre o mesmo produto) ou peça paste ao membro. **NUNCA inventar VOC** — fonte que caiu em todos os fallbacks vai no Data Quality Summary como bloqueada.

**A ordem de construção do avatar — as Core Five Categories.** O avatar não nasce da demografia, nasce do desejo. As cinco categorias que agrupam pessoas, em ordem de importância: **1) Desires · 2) Experiences · 3) Emotions · 4) Behaviors & Habits · 5) Demographics**. Comece pelo topo e deixe **demografia por último** — é o inverso do que a maioria faz, e é por isso que a maioria produz avatar que ninguém usa depois ("Susan, 47 anos, corporativa, 2 filhos" não é acionável).

Duas dessas categorias costumam ficar de fora da pesquisa tradicional, e são justamente as que mais rendem ângulo:

- **Experiences** — o que a pessoa viveu, em dois tipos. *Situacional* (uma circunstância ou um evento: "acabou de ter bebê", "o quarto fica claro cedo demais", "se divorciou há dois anos") e *de produto* (tentou uma solução e teve um resultado: "tentou magnésio e continuou acordando cansada"). Experiência de produto SEMPRE tem um desfecho — funcionou, não funcionou, ainda está testando. Registre a experiência limpa, sem a emoção grudada nela: "mora em apartamento barulhento" é experiência; "ODEIA morar em apartamento barulhento" é experiência mais emoção, e cada metade vai pra sua categoria. Cuidado com experiência de múltiplo benefício: "magnésio não funcionou" — não funcionou pra quê? Pode ter falhado pro sono e funcionado pra enxaqueca. Pesquise o contexto real antes de atacar o mecanismo, senão você desalinha com quem teve sucesso em outro uso.
- **Behaviors & Habits** — o que a pessoa FAZ de forma repetida (pesquisa tudo antes de comprar, só compra em promoção, faz meal prep todo domingo, dorme com fita nasal, evita academia lotada). Feito uma vez é experiência; repetido é comportamento — e quanto mais frequente o comportamento, mais ele está ligado à identidade da pessoa e mais fácil ela se reconhecer no anúncio. Comportamento nasce das outras categorias (uma experiência ruim gera um hábito novo, um desejo muda a rotina) e é o material mais subexplorado do mercado.

Construa o perfil em camadas:

**Psychographics (a parte que REALMENTE importa):**

- **Hopes & Dreams** — o estado futuro ideal ESPECÍFICO. NÃO genérico como "perder peso" — específico como "poder vestir o vestido que usei no casamento da minha prima sem medo de me olhar no espelho depois". A especificidade vem da linguagem real do consumidor.

- **Victories & Failures** — o que já tentaram, o que funcionou parcialmente, o que falhou completamente e POR QUÊ. Esta seção é ouro: cada coisa que falhou é uma objeção potencial, cada coisa que funcionou parcialmente é uma ponte pra posicionar seu mecanismo único.

- **External Forces Blamed** — quem/o que eles culpam. Genética, hormônios, indústria de beleza, médicos, sistema capitalista, envelhecimento, falta de tempo. Esta informação entra direto na "corruption angle" da copy (mecanismo que externaliza a culpa).

- **Prejudices & Biases** — contra quais tipos de produto ou abordagem são céticos. "Suplementos são scam", "cremes são placebo", "dietas não funcionam". Esses vieses precisam ser ENDEREÇADOS, não ignorados.

- **Core Beliefs** — sobre saúde, beleza, envelhecimento, investimento em si mesmo, relacionamentos. Moldam aceitação/rejeição de claims. **Crença não é bloco de construção de avatar — é resultado.** Uma crença é o que sobra quando experiência, emoção e comportamento se amarram. Toda vez que achar uma crença na pesquisa ("acho que não consigo emagrecer", "genética está contra mim"), desempacote com três perguntas: (a) o que aconteceu pra ela acreditar nisso? → vira **experience**; (b) como essa crença faz ela se sentir? → vira **emotion**; (c) o que ela faz ou deixa de fazer por causa disso? → vira **behavior**. Uma frase vaga vira três ou quatro ângulos acionáveis. Crença rende hook excelente ("Se você acha que nunca mais vai dormir a noite inteira…") — use na mensagem, nunca como base do avatar.

- **The Paradox** — a tensão entre ceticismo e esperança. Não acreditam que nada funciona MAS continuam procurando. Essa tensão é a energia por trás da decisão de compra.

**Demographics (por último, e só o que refina de verdade):**
- Idade (em faixas, nunca em precisão — "40+" pode importar, "44 anos" não importa), gênero, renda, localização, estado civil, escolaridade, ocupação típica
- Na maioria dos casos a demografia já vem implícita nas outras camadas ("acabou de dar à luz" implica mulher) e não precisa ser declarada. Declare quando o produto **funciona melhor** para aquela demografia — skincare formulado para pele rica em melanina, meia de compressão para quem passa 14 horas em pé. Fora disso, declarar demografia só corta mercado à toa: uma mulher de 22 e um homem de 54 podem ter o mesmo desejo, a mesma experiência, a mesma emoção e o mesmo comportamento, e declarar idade ou gênero elimina metade dos compradores com a dor idêntica.

**Pain Points hierarquizados:**
- **Dor principal** (a razão #1 que a pessoa acorda pensando)
- **Dores secundárias** (3-5 dores adjacentes)
- **Dores emocionais** (como se sentem POR CAUSA do problema — vergonha, frustração, invisibilidade, perda de confiança)
- **Dores sociais** (como afeta relacionamentos, vida social, auto-imagem em público)
- Frequência de menção (alta/média/baixa) pra priorizar

**Desires hierarquizados:**
- **Desejo principal** — o resultado imediato e específico que querem, em nível de superfície, escrito na frase "I want X" / "I need Y"
- **Desejos secundários**
- **O desejo POR TRÁS do desejo** — o instinto que sustenta o desejo de superfície: saúde, status, sexo, pertencimento, controle ou conforto. Ele orienta o tom e a mensagem, mas **não é** a unidade de construção do avatar (esse papel é do desejo de superfície, ETAPA 4.5). Ex: "perder 10kg" → o que querem é "sentir-se desejada de novo" → o instinto por trás é status/sexo.
- **Ranqueie os desejos por scope (alcance — quantas pessoas compartilham), urgency (urgência — com que desespero e em quanto tempo precisam) e staying power (poder de permanência — o desejo se renova ou morre quando resolvido).** O desejo vencedor desse ranking vira o core avatar da ETAPA 4.5, e é lá que os três valores ficam gravados.
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

### ETAPA 4.5 — Core Avatar e Sub-Avatares (a camada que vira ângulo)

**Sistemas a puxar da base antes de montar (rode cada `best_query`):**
- **Core Avatars & Sub-Avatars — The Core Five Categories** (rode `core avatar sub avatar core five categories desire experience emotion behavior demographic`)
- **Desire-First Avatar (over Demographics)** (rode `desire first avatar over demographics avoid combining desires single desire core avatar`)
- **Surface Desire vs Core Desire** (rode `surface level desire vs core desire why behind the desire avatar building`)
- **Desire Power Ranking — Scope / Urgency / Staying Power** (rode `mass desire scope urgency staying power power ranking choose strongest`)

O perfil da ETAPA 4, sozinho, descreve um mercado — não diz PRA QUEM cada peça fala. Esta etapa converte aquele perfil em avatares nomeados e acionáveis. É o único lugar do sistema onde `core_avatar` e `sub_avatars[]` nascem: a Skill 08 lê os sub-avatares como a variável mestre de cada conceito de criativo, e a Skill 06 usa o mesmo recorte pra decidir a quem a copy se dirige. Sem esta etapa, as duas ficam sem a informação e voltam a escrever pra "mulheres 45+", que é o mesmo que escrever pra ninguém.

**1. Escolha o core avatar — UMA categoria só.**

Core avatar é o ponto de partida, construído com **uma única** das Core Five. Para praticamente todo produto essa categoria é **desire**, e o desejo usado é o de **superfície**, não o instinto:

- **Desejo de superfície** é o resultado imediato e específico que a pessoa quer: "I want to sleep through the night", "I want smoother and less dry skin", "quero que meu cachorro pare de puxar a guia".
- **Desejo central** é o instinto por trás (saúde, status, sexo, pertencimento, controle, conforto). Orienta tom e mensagem, mas é amplo demais pra construir avatar. Mirar o instinto direto só se justifica pra marca grande com skill de marketing muito alto.
- **Checador de desejo:** cabe na frase "I want X" ou "I need Y"? Se não cabe, não é desejo — é outra categoria disfarçada.
- Reclamação vira desejo espelhado: "por que demora tanto pra escovar os dentes?" → "quero escovar os dentes mais rápido".

Ordene os candidatos por **scope**, **urgency** e **staying power** (o ranking da ETAPA 4). Quanto menor a operação, mais pro lado específico da escala ela precisa operar.

**2. A escala do específico ao amplo — específico sem alienar.**

Avatares vivem num espectro. De um lado, específico a ponto de excluir todo mundo ("dentista de 34 anos em Tampa que dirige Tesla vermelho e toma oat milk latte"): quase ninguém se encaixa e não há escala. Do outro, amplo a ponto de não dizer nada ("mães", "quem quer ser saudável"): é o território das marcas gigantes, não o do membro. **Quanto mais amplo o avatar, melhores precisam ser produto, oferta, marca E skill de marketing**, porque a disputa é de frente com os gigantes. Quanto mais específico sem alienar, mais a especificidade compra confiança e compensa produto, oferta e marca menores.

Quantidade de core avatars por tamanho de operação: **um único core avatar até $100k/mês** (todo o trabalho é aprofundar sub-avatares a partir dele); **2-3 acima de $500k/mês**; **3-10 entre $1M e $10M/mês**. Trocar de core avatar cedo demais rouba foco do que está funcionando.

**3. Construa os sub-avatares — duas categorias ou mais.**

Sub-avatar é o core avatar refinado com pelo menos mais uma categoria: desejo + experiência, desejo + emoção, desejo + comportamento, desejo + demografia, ou combinações de três ("quer que a família toda durma melhor" + "o bebê acorda às 5h por causa da luz da manhã" + "se sente exausto"). Regras inegociáveis:

- **Todo sub-avatar precisa de pelo menos um desejo** — desejo é o que faz comprar.
- **Nunca combine mais de um desejo** no mesmo avatar. Um desejo pode levar a outro, mas o avatar mira um só.
- Quanto mais categorias empilhadas, mais específico o avatar fica. Em mercado sofisticado, os recortes óbvios já foram atacados: empilhe mais categorias.
- Demografia entra **por último** e só quando refina de verdade.

Pesquise **uma categoria por vez**, com a mesma coleta resiliente da ETAPA 4 e buscas simples: emoção (`"lack of sleep is making me feel reddit"`), experiência de produto (`"blackout room sleep reddit"`), demografia (`"night shift workers sleep reddit"`, `"at what age does sleep start getting worse"`). Uma única thread boa costuma render vários sub-avatares. Vale também o caso sem dor ativa (a pessoa 70+ que dorme bem tomando vinho): ela não é avatar de compra, mas vira informação pra um ângulo ("durma melhor sem precisar se intoxicar").

**4. Cada sub-avatar carrega o ângulo que ele gera.**

Sub-avatar existe pra produzir ângulo — essa é a razão de tudo. Método em três passos: (1) olhe o **desejo** (o que a pessoa quer); (2) olhe a **experiência ou o comportamento** (o que ela já tentou ou já faz pra conseguir); (3) nomeie a **lacuna** entre os dois. A lacuna é o ângulo.

Exemplo: desejo "restorative sleep" + comportamento "dorme com fita nasal pra forçar respiração nasal" → ela faz isso e ainda não dorme direito → ângulo **"better than nose strips"**.

**Ângulo é a razão principal que você dá pra alguém comprar**, voltado ao cliente e escrito em frase completa. Se a frase não entrega ao cliente uma razão de compra, ainda não é ângulo — é conceito ou formato. "Comparação", "before & after" e "us vs them" são conceitos: comparação de quê? O "quê" é o ângulo. Trava contra excesso de zelo: **um ângulo por sub-avatar**. Se sobrar ângulo, ele indica um sub-avatar novo — não vira lista solta.

**5. Anote os labels — como o mercado se chama.**

Labels são os apelidos que o próprio mercado usa pra se descrever: "light sleeper", "night shifter", "graveyard shift", "sleep tech user". Colete sempre que aparecerem, em comentários, threads e nos anúncios ativos dos concorrentes na Meta Ad Library (é lá que o concorrente já testou esse jeito de falar com dinheiro real). Servem pra duas coisas: entram literalmente na copy, porque usar as palavras que o mercado usa pra se nomear gera identificação imediata, e viram termo de busca pra achar mais gente igual na rodada seguinte de pesquisa. Grave em **`labels[]`** no `dados.json`.

**Saída obrigatória desta etapa:** `core_avatar` + `sub_avatars[]` + `labels[]` no `dados.json` (schema abaixo). Sub-avatar não tem certo e errado — é hipótese que gera ângulo pra teste. Se o ângulo não performar, na esmagadora maioria das vezes o problema é execução, não o avatar.

### ETAPA 5 — Voice of Customer (Linguagem EXATA — Mínimo 35 Frases)

**Sistemas a puxar da base antes de minerar (rode cada `best_query`):**
- **Voice of Customer Research (Review Mining / Surveys / Interviews)** (rode `Voice of Customer review mining process extracting verbatim phrases from reviews`) — o processo de extração de frases exatas
- **4-Star Review Mining (avoid 1s and 5s)** (rode `four star reviews mining avoid 5 star 1 star fake reviews honest language`) — onde está a linguagem honesta (evitar 1s e 5s)
- **Google Review-Mining Shortcuts (site:amazon.com inurl product-reviews)** (rode `Amazon review mining google shortcut tired of wasn't until tried site operator`) — operadores de busca pra achar frases rápido
- **Consumer Insights Database (where + what + how to mine)** (rode `consumer insights database mine reviews reddit tiktok ad comments fears desires motivations`) — mapa de fontes (Reddit, TikTok, ad comments)
- **Says-vs-Does (Trust Behavior, Not Surveys)** (rode `says vs does trust purchasing behavior not surveys beer survey national enquirer right answer bias`) — filtra o que as pessoas DIZEM do que realmente FAZEM
- **Review Density Filter (Organize For Best Reviews)** (rode `filtrar reviews por tamanho LEN body ordenar Z A manter 200 300 mais longas`) — antes de ler review por review numa base grande: filtre pelo tamanho do texto (o comprimento do campo body), ordene do maior pro menor e fique com as 200-300 mais longas — são as densas em linguagem aproveitável; review de uma linha quase nunca rende frase de copy
- **Amazon Mining com Shulex + mapa de níveis de preço** (rode `shulex chatgpt for amazon top pros cons purchase motivation usage scenarios QA`) — a rota Amazon da varredura por plataforma: extrai das listagens os top pros e cons, a motivação de compra, os cenários de uso e o Q&A, cruzando os achados com um mapa de níveis de preço do mercado

Das pesquisas da etapa 4, extraia e organize SEPARADAMENTE. **NUNCA PARAFRASEAR** — capture exatamente como as pessoas falam. Isso vai pra copy e criativos literalmente. **VOC permanece SEMPRE no idioma original do consumidor (inglês US), nunca traduzir** — mesmo com `report_language: "pt-BR"`. É matéria-prima literal; o resto do relatório fica no idioma do membro, as frases não.

- **Frases exatas descrevendo o PROBLEMA** — mínimo 15 frases
- **Frases exatas descrevendo o DESEJO** — mínimo 10 frases
- **Frases exatas descrevendo FRUSTRAÇÕES com produtos existentes** — mínimo 10 frases
- **Palavras e expressões recorrentes** (aparecem 3+ vezes na base de pesquisa) — com a contagem gravada, não só a lista

Essas frases são ouro. Hopkins escreveu em 1923: "a boa copy fala a linguagem do consumidor". Esse é o raw material.

**Fontes de primeira mão — quando o membro JÁ tem lista ou clientes (cheque o `profile.md`/manifest antes de assumir que não tem):**

Review de concorrente é a linguagem do cliente DOS OUTROS. Se o membro já vende, a fonte mais rica é o cliente dele — e a base tem dois sistemas prontos pra isso:

- **Giveaway Survey System (Viral Sweep + Klaviyo + Custom GPT)** (rode `giveaway survey system viral sweep bonus entries klaviyo entry rate benchmark`) — VOC em massa disfarçado de sorteio: as bonus entries (entradas extras que o participante ganha por responder) compram respostas escritas dos próprios clientes. Regra de qualificação do sistema: lista de compradores abaixo de 2.000-3.000 pessoas → NÃO rodar (a amostra não paga o esforço); acima disso, é a fonte de primeira mão mais barata que existe — o prêmio se paga e o produto real do sorteio é o dado.
- **Warm Calls — Customer Phone Call Research** (rode `warm call cliente script como voce chegou ate nossa marca pausa nao fale mais nada`) — ligação pro cliente com o script "como você chegou até a nossa marca?" seguida da instrução mais difícil: **pausa — não fale mais nada** e deixe o cliente preencher o silêncio. Poucas ligações rendem frases inteiras, com contexto e emoção, que nenhum review entrega. As frases entram na base de VOC com `source` próprio.

Membro pré-launch, sem lista e sem clientes: pule este bloco sem warning — as fontes públicas da ETAPA 4 cobrem a rodada, e este bloco entra na re-rodada da skill quando a marca tiver compradores.

**O teste do Ctrl+F — o vocabulário real do mercado (obrigatório):**

A proibição de parafrasear vira uma checagem verificável aqui. Depois de coletar as frases, conte quantas vezes cada termo relevante aparece na base de pesquisa e, principalmente, **rode a busca inversa**: pegue os termos que a marca, a indústria e os concorrentes usam e procure cada um dentro da base. Termo que aparece zero vez está proibido na copy.

O caso que ancora a regra vem de uma marca de colágeno. O cliente escreveu "I was tired of my skin looking dry no matter my skincare routine" — o desejo dele é "I want smoother and less dry skin". Ninguém escreveu "hydrated"; o Ctrl+F confirmou zero ocorrências. Um anúncio que diz "hydrated" está falando a língua da indústria, não a do mercado, e não ressoa.

Grave em **`market_vocabulary`** no `dados.json`:
- **`words_used[]`** — o termo real, a contagem de ocorrências na base e a categoria (problema / desejo / frustração)
- **`words_absent[]`** — o termo que a marca ou a indústria usa, quem o usa, a confirmação de zero (ou quase zero) ocorrências na base, e o substituto que o mercado usa no lugar dele

A contagem tem um segundo uso. Termo muito repetido **na base de pesquisa** é vocabulário real e deve ser usado; termo muito repetido **nos claims dos concorrentes** (os 10-15 coletados na ETAPA 3, contados pelo Buzzword Tally de lá) é mensagem fatigada e serve como prova no corpo do texto, nunca como headline. Marque esses com `saturated_in_market: true` — foi assim que um claim aparentemente ótimo ("fast hair drying without heat damage") morreu no feed: sete concorrentes diziam exatamente a mesma coisa. **As Skills 06 e 08 consultam `market_vocabulary` ANTES de escrever qualquer linha.**

**Curadoria top 20 (obrigatória):** das frases coletadas, monte o ranking das **20 mais fortes** — critério primário: frequência de menção na base de pesquisa; desempate: força emocional/especificidade. Cada entrada leva `id`, `rank`, `count` (quantas vezes a frase ou variação próxima apareceu) e `category` (problem/desire/frustration). Grave o ranking em **`voc_top20`** no `dados.json` (schema abaixo). **A Skill 06 lê exatamente esse campo** pro checklist de VOC da copy — sem ele, a 06 tem que re-curar do zero e a informação de frequência se perde. Se coletou menos de 20 frases, grave as que tem (o `voc_adequacy` já sinaliza o déficit).

**IDs estáveis de VOC (contrato com as Skills 06/08/14):** cada frase VOC ganha um `id` sequencial no formato `voc-001`, `voc-002`… O id identifica a **FRASE**, não a posição no ranking. Regras de cunhagem:

- **Primeira execução:** cunhe os ids na ordem do rank do `voc_top20` (`voc-001` pro rank 1, `voc-002` pro rank 2…). Frases citadas em `voc_evidence[]` (core_avatar e sub_avatars da ETAPA 4.5) usam o MESMO namespace: quote que já está no top20 repete o id dela; quote que não está cunha o próximo número livre.
- **Re-execução (a skill roda de novo com aprendizado dos testes):** antes de gravar, leia o `dados.json` anterior. Frase que já tem id **MANTÉM o id pra sempre**, mesmo que o rank, o count ou a category mudem. Frase nova recebe o próximo número livre da sequência (append). Frase que saiu do top20 não libera o número dela — id nunca é renumerado nem reaproveitado.
- **Por quê:** a copy (06), os hooks dos criativos (08 — o `voc_source.ref_id` de cada hook/headline aponta pra cá) e o content recycler (14 — herda `voc_refs[]` via 08) rastreiam cada linha até a frase de origem por esse id. Id que muda entre execuções quebra a rastreabilidade de tudo que já foi produzido.

**Fallback quando < 35 frases reais foram coletadas**: **NUNCA** gere frases artificiais/sintéticas/plausíveis. Em vez disso:

1. Documente o déficit explicitamente no output: `"VOC real: N frases únicas; mínimo 35 não atingido."`
2. Liste as fontes tentadas e as que bloquearam acesso.
3. **Classificar severidade do déficit pra alertar skills downstream** (`voc_adequacy` e `skills_blocked` são gravados SEMPRE no `dados.json`, inclusive no caminho feliz — a skill 06 lê esses campos):
   - `voc_count >= 35` → `voc_adequacy: "ok"`, `skills_blocked: []`, segue normal
   - `15 <= voc_count < 35` → `voc_adequacy: "medium"`, `skills_blocked: []`, skill 06 emite warning mas procede
   - `voc_count < 15` → `voc_adequacy: "insufficient"`. Skill 06 DEVE bloquear no pré-flight — copy sem VOC real não é copy, é invenção. Salvar em `02-market-research/dados.json`: `"voc_adequacy": "insufficient", "skills_blocked": ["06-copy-engine"]`
4. Siga com as etapas restantes (awareness, sophistication, root cause) — essas não dependem de VOC quantity.

Esse déficit é rastreado em `voc_count` + `voc_adequacy` do manifest e do JSON companion (`02-market-research/dados.json`).

### ETAPA 6 — Root Cause Research (metodologia da masterclass interna)

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

**Sistemas a puxar da base antes de consolidar (rode cada `best_query`):**
- **Unified Research Document (Processo Completo)** (rode `unified research document process demographics psychographics promises objections language`) — o processo de consolidação que este brief implementa: demographics, psychographics, linguagem a usar/evitar, promessas, objeções e soluções existentes num documento único que alimenta todas as fases seguintes com contexto consistente
- **Psychological Audit — protocolo de 7 passos** (rode `psychological audit row codes 12 categorias merge prompt insights agrupados`) — o protocolo que transforma o dado bruto das ETAPAS 4-5 em insight agrupado ANTES de escrever o brief: um código por linha de dado (row code), distribuição de tudo em 12 categorias e um prompt de merge que devolve os insights agrupados. Rode ele sobre a base coletada; a síntese abaixo nasce dos grupos, não da releitura solta das anotações
- **Ultimate Message Map (UMM)** (rode `ultimate message map tabs tag manager all known jobs all known motivators persona`) — o "tag manager da mensagem": todos os jobs conhecidos e todos os motivadores conhecidos cruzados com a persona. Use como checagem final da síntese — mensagem (dor, desejo, objeção, ângulo) que não está amarrada a um dono no brief é mensagem que a copy e os criativos nunca vão achar

Consolide tudo num documento **estruturado, navegável, acionável**:

**1. Target Market Overview**
- Demographics resumido
- Mercado geográfico
- Awareness level dominante + distribuição do TAM
- Sophistication stage + claims saturados

**2. Arquitetura de Avatar + Perfil Psicográfico**
- **Core avatar** — a categoria escolhida, o desejo de superfície na frase "I want X", o instinto por trás, e o ranking de alcance/urgência/permanência que o elegeu (da Etapa 4.5)
- **Sub-avatares** — tabela com uma linha por sub-avatar: nome, categorias combinadas, e o **ângulo** que ele gera em frase completa (é o que a Skill 08 transforma em conceito de criativo)
- **Labels** — os apelidos que o próprio mercado usa pra se descrever
- Hopes, Dreams, Failures, Blamed Forces, Prejudices, Core Beliefs, The Paradox (da Etapa 4)

**3. Pain Points & Desires Hierarquizados**
- Top 5 dores em ordem de intensidade
- Top 5 desejos em ordem de intensidade
- **O desejo mais profundo** (the real want behind the want)

**4. Voice of Customer — Quotes Curadas**
- Top 10 frases mais poderosas que vão direto pra copy (as 10 primeiras do ranking `voc_top20` — problemas + desejos + frustrações misturadas, com a contagem de menções de cada uma)
- **Vocabulário do mercado** — as palavras que o mercado usa de fato (com a contagem) e, ao lado, as palavras da marca ou da indústria que não aparecem na pesquisa e por isso estão proibidas na copy

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
- **Ângulos de diferenciação mais promissores** (ranqueados) — os ângulos de `sub_avatars[]` que NENHUM concorrente está usando, cada um nomeando o sub-avatar de onde saiu

### Regra de Parada — quando encerrar a pesquisa

A skill tem mínimo (35 frases de VOC) e precisa também de um teto, porque pesquisa é o lugar mais confortável do mundo pra procrastinar. O teto é o sistema **Regra dos 5–10 Ad Ideas** da base (rode `quando parar a research 5 a 10 boas ad ideas va testar blocos de uma hora` antes de decidir a parada): o teto é de resultado, não de relógio — **quando a pesquisa já produziu de 5 a 10 boas ideias de anúncio (os golden nuggets da rodada), pare e vá testar.**

- Na primeira passada, cubra todas as fontes (Amazon, Reddit, YouTube, comentários de TikTok) em blocos de aproximadamente uma hora, até o filão esgotar — o sinal de esgotamento é a thread parar de trazer coisa nova e os sub-avatares novos virarem variação dos que já existem.
- Acumular 100 ideias sem validação não é profundidade, é adiamento. Quem devolve a direção da próxima rodada é o teste: o ângulo que puxa spend diz qual sub-avatar tem mercado de verdade, e é dali que a pesquisa seguinte parte.
- Registre de onde veio cada ideia. Cada frase em `voc_evidence` leva o `id` estável (namespace `voc-NNN` da ETAPA 5) e o campo `source`, e cada label também leva `source`. Quando um anúncio vencer na Skill 11, essa marcação diz qual fonte de pesquisa produziu o vencedor — e é pra ela que a próxima rodada volta primeiro.
- Pesquisa não termina, ela pausa. A Skill 02 pode ser re-rodada a qualquer momento com o aprendizado dos testes na mão. Não tente esgotar o mercado antes de o primeiro anúncio existir.

### Validação Final

Antes de salvar, valide:
- [ ] Voice of Customer tem mínimo 35 frases EXATAS (não parafraseadas)
- [ ] `voc_top20` gravado no dados.json com id + rank + count + category (a Skill 06 lê esse campo direto)
- [ ] IDs de VOC estáveis: todo item de `voc_top20` e de `voc_evidence[]` tem `id` no formato `voc-NNN`, mesmo namespace; em re-execução, nenhum id de frase existente mudou (só append de frases novas)
- [ ] `core_avatar` gravado com UMA categoria dominante e o desejo em nível de superfície (cabe na frase "I want X")
- [ ] Cada item de `sub_avatars[]` combina 2+ das Core Five, tem pelo menos um desejo, traz demografia por último (só se refina) e carrega **um** `angle` em frase completa — a Skill 08 lê exatamente esse campo como persona/micro-persona de cada conceito
- [ ] `labels[]` gravado com os apelidos que o próprio mercado usa
- [ ] `market_vocabulary` gravado com contagem em `words_used[]` e os termos proibidos em `words_absent[]`
- [ ] A pesquisa produziu de 5 a 10 boas ideias de anúncio (regra de parada) — abaixo disso, aprofunde; acima, pare e vá testar
- [ ] Awareness distribution é numérica (não "a maioria é problem aware" — mas "45% problem aware, 30% solution aware")
- [ ] Sophistication stage tem claims saturados LISTADOS
- [ ] Cada objeção tem estratégia de quebra específica (não genérica)
- [ ] Recomendações finais são acionáveis (não "a copy deve ser emocional" — mas "lead com Story Lead sobre trigger event X, foco em desejo Y, mecanismo Z")

Se alguma validação falhar, aprofunde naquele ponto antes de salvar.

### Data Quality Summary (antes de salvar)

Inclua seção dedicada no `.md` e no `.json`:

```
## Data Quality Summary
- VOC coletado de: Amazon reviews (N), Reddit (N), TikTok comments (N), Trustpilot (N), fóruns (N), survey/giveaway (N), ligações pra clientes (N) = Total N frases únicas
- Fontes tentadas e bloqueadas: [lista, ex: "Trustpilot (Cloudflare)", "Quora (login wall)"]
- VOC minimum atingido? [sim / não — se não, N frases a aquém do mínimo 35]
- Awareness distribution source: [user_estimate / default:<bucket> / hybrid / web_signals]
- Sophistication stage confidence: [high / medium / low] + racional em 1 frase
- Root cause candidatas baseadas em: [peer-reviewed research / specialist consensus / extrapolation]
- Avatar: 1 core avatar + N sub-avatares (cada um com ângulo declarado) · N labels coletados
- Vocabulário: N termos reais com contagem · N termos da marca/indústria confirmados como ausentes na base
- Ideias de anúncio geradas até a parada: N (regra de parada: 5-10)
```

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer-builder/offer-builder.md` → `04-offer-builder/offer-builder.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).


**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/02-market-research/`.

Salvar TRÊS artefatos:

1. **`workspace/[produto]/02-market-research/market-research.md`** — fonte canônica para AI das próximas skills
2. **`workspace/[produto]/02-market-research/market-research.html`** — visualização humana (template ou fallback inline)
3. **`workspace/[produto]/02-market-research/dados.json`** — JSON companion estruturado:

```json
{
  "awareness_distribution": { "unaware": 0, "problem_aware": 0, "solution_aware": 0, "product_aware": 0, "most_aware": 0 },
  "awareness_distribution_source": "default|user_estimate|hybrid|web_signals",
  "dominant_awareness": "problem_aware",
  "dominant_awareness_secondary": "solution_aware",
  "_comment_dominant_awareness_secondary": "campo OPCIONAL — só existe quando dois níveis adjacentes empataram (±5pp). dominant_awareness leva o de MAIOR intenção de compra; este campo guarda o outro. Ausente = sem empate (downstream trata como nível único)",
  "sophistication_stage": 3,
  "sophistication_confidence": "high|medium|low",
  "voc_phrases": { "problem": ["..."], "desire": ["..."], "frustration": ["..."] },
  "voc_top20": [
    { "id": "voc-001", "rank": 1, "phrase": "frase exata em inglês US", "count": 8, "category": "problem|desire|frustration" }
  ],
  "_comment_voc_top20": "as 20 frases mais fortes ranqueadas por frequência de menção (curadoria da ETAPA 5) — a Skill 06 lê ESTE campo pro voc_checklist da copy",
  "_comment_voc_ids": "contrato de rastreabilidade: `id` é a identidade ESTÁVEL da frase (`voc-001`, `voc-002`…), cunhada na ordem do rank da PRIMEIRA execução — namespace único pro produto inteiro, compartilhado entre voc_top20 e todo voc_evidence[] (a mesma frase leva o MESMO id onde aparecer; quote de voc_evidence fora do top20 cunha o próximo número livre). Em re-execução: frase existente MANTÉM o id (mesmo mudando rank/count), frase nova entra em append com o próximo número, id nunca é renumerado nem reaproveitado. CONSUMIDORES: Skill 06 (voc_refs da copy), Skill 08 (voc_source.ref_id de cada hook/primary/headline) e Skill 14/recycler (voc_refs herdadas via 08) rastreiam cada linha produzida até a frase de origem por ESTE id — id instável quebra a rastreabilidade retroativa de tudo que já foi gerado",
  "voc_count": 0,
  "voc_adequacy": "ok|medium|insufficient",
  "skills_blocked": [],
  "data_quality": {
    "voc_sources": { "amazon": 0, "reddit": 0, "tiktok": 0, "trustpilot": 0, "forums": 0 },
    "sources_blocked": [],
    "voc_minimum_met": true,
    "root_cause_basis": "peer_reviewed|specialist_consensus|extrapolation"
  },
  "core_avatar": {
    "category": "desire",
    "surface_desire": "I want to sleep through the night without waking at 3am",
    "core_desire_behind": "health|status|sex|belonging|control|comfort",
    "scope": "high|med|low",
    "urgency": "high|med|low",
    "staying_power": "high|med|low",
    "labels": ["light sleeper"],
    "voc_evidence": [
      { "id": "voc-001", "quote": "frase exata em inglês US", "source": "reddit|amazon|tiktok|youtube|trustpilot|forum|ad_library|survey|warm_call" }
    ]
  },
  "_comment_core_avatar": "o avatar central da ETAPA 4.5, construído com UMA categoria só (`category` = uma das Core Five: desire|experience|emotion|behavior|demographic — desire em praticamente todo caso). `surface_desire` é a unidade de construção e cabe na frase 'I want X'; `core_desire_behind` é o instinto por trás e orienta TOM, não construção. CONSUMIDORES: Skill 06 (define a quem a página e a copy se dirigem) e Skill 08 (base da persona de cada conceito)",
  "sub_avatars": [
    {
      "id": "sa-01",
      "name": "the magnesium tried-it",
      "categories_used": ["desire", "experience"],
      "desire": "I want to sleep through the night",
      "experience": "tried magnesium, still woke up tired",
      "emotion": "",
      "behavior": "",
      "demographic": "",
      "labels": [],
      "angle": "Why magnesium only fixed half of your sleep problem",
      "voc_evidence": [
        { "id": "voc-001", "quote": "frase exata em inglês US", "source": "reddit|amazon|tiktok|youtube|trustpilot|forum|ad_library|survey|warm_call" }
      ]
    }
  ],
  "_comment_sub_avatars": "cada sub-avatar combina 2+ das Core Five e SEMPRE tem `desire` preenchido. A ordem dos campos é a ordem de importância do material (desire → experience → emotion → behavior → demographic): demografia vem POR ÚLTIMO e só quando refina de verdade; categoria não usada fica string vazia. `angle` é obrigatório e ÚNICO por sub-avatar — é a razão de compra em frase completa, voltada ao cliente (se não dá razão de compra, é conceito, não ângulo). CONSUMIDORES: Skill 08 lê ESTE campo como Persona/Micro-persona (a variável mestre de cada conceito) e `angle` como ângulo de entrada; Skill 06 usa o mesmo recorte pra escolher o foco da copy",
  "labels": [
    { "label": "night shifter", "refers_to": "quem trabalha turno da noite e dorme de dia", "source": "reddit|amazon|tiktok|youtube|forum|ad_library", "voc_quote": "" }
  ],
  "_comment_labels": "os apelidos que o próprio mercado usa pra se descrever (ETAPA 4.5) — esta é a lista completa, com origem e frase de apoio; os campos `labels` dentro de `core_avatar` e de `sub_avatars[]` são só os termos (strings) que apontam pra ela. CONSUMIDORES: Skill 06 (entram literalmente na copy — usar a palavra com que o mercado se nomeia gera identificação) e Skill 08 (call-out do primeiro beat do criativo). Também servem de termo de busca pra achar mais gente igual numa próxima rodada de pesquisa",
  "market_vocabulary": {
    "words_used": [
      { "term": "smoother", "count": 0, "category": "problem|desire|frustration", "saturated_in_market": false }
    ],
    "words_absent": [
      { "term": "hydrated", "used_by": "brand|industry|competitor", "occurrences_in_research": 0, "market_says_instead": "smoother / less dry" }
    ]
  },
  "_comment_market_vocabulary": "teste do Ctrl+F da ETAPA 5. `words_used` = vocabulário REAL observado, com a contagem de ocorrências; `saturated_in_market: true` quando o termo também domina os claims dos concorrentes da ETAPA 3 (mensagem fatigada — serve de prova no corpo do texto, nunca de headline). `words_absent` = termos da marca/indústria com zero (ou quase zero) ocorrência na base — PROIBIDOS na copy, com o substituto real ao lado. CONSUMIDORES: Skills 06 e 08 consultam ANTES de escrever qualquer linha",
  "avatar": {
    "psychographics": {},
    "pain_hierarchy": [
      { "rank": 1, "item": "", "emotional_layer": "", "frequency": "high|med|low", "voc_quote": "" }
    ],
    "desire_hierarchy": [
      { "rank": 1, "item": "", "emotional_layer": "", "frequency": "high|med|low", "voc_quote": "" }
    ],
    "demographics": {}
  },
  "_comment_avatar": "camada descritiva do mercado (ETAPA 4) — demografia fica por último porque é a que menos gera motivação de compra. A camada ACIONÁVEL, que as Skills 06 e 08 leem pra decidir pra quem cada peça fala, é `core_avatar` + `sub_avatars[]`, não este objeto",
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
- Skill 06 (`06-copy-engine`) — usa VOC literal, lead type, awareness level, objeções, `core_avatar` (a quem a copy se dirige), `labels` (os apelidos do mercado que entram na copy) e `market_vocabulary` (as palavras permitidas e as proibidas)
- Skill 07 (cadeia storefront `07a-page-design` → `07b-page-build`) — usa tudo da copy + proof stacking
- Skill 08 (`08-creative-engine`) — usa trigger events, VOC, visual hooks, `market_vocabulary`, e **`sub_avatars[]` como persona/micro-persona de cada conceito, com `sub_avatars[].angle` como o ângulo de entrada** (é o contrato que substitui a leitura genérica de "sub-avatares da Skill 02")
- Skill 10 (`10-ad-strategy`) — usa awareness pra targeting

**Atualize o `manifest.json`** (fonte única de verdade):

- `market` ← mercado geográfico confirmado na ETAPA 1 (`US` / `UK` / `EU` / `global`) — sem isso o manifest fica pra sempre com o default `"US"` do setup, divergindo do relatório
- `voc_count` ← número total de frases VOC únicas coletadas
- `voc_adequacy` ← `"ok" | "medium" | "insufficient"` (mesmo valor do dados.json)
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
