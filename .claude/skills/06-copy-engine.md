---
name: copy-engine
description: Engine de escrita de copy completo baseado em market research, competitor analysis, e oferta. Escreve PDPs, landing pages, advertoriais, ou long-form sales pages aplicando headlines (processo de 100 linhas, fórmulas), leads tipados por awareness, hero patterns de ecom, 10x page plan, frameworks de persuasão (Cialdini, Sugarman, Hopkins), proof stacking, CTAs (call to value), 7 sweeps de revisão, e linguagem EXATA do customer. Modela a estrutura contra ESPÉCIMES reais de swipe file (peças que já converteram) antes de escrever, e audita o resultado com o método de markup (4 U's, 4 emoções, loop Objection-Claim-Proof-Benefit). Use quando o membro disser "copy", "escrever copy", "copy da página", "copy do ad", "PDP copy", "landing page copy", ou após a skill de oferta. O sistema DECIDE a estratégia de copy automaticamente — não consulta o membro sobre decisões estratégicas.
---

# Copy Engine

### Pré-flight (OBRIGATÓRIO)
- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `product_slug` do manifest NÃO começa com `dev-placeholder-` (senão, pare: "rode product research primeiro")
- [ ] `02-market-research/dados.json` existe → extrair `awareness_distribution`, `sophistication_stage`, `voc_top20` (se presente), `voc_phrases`, `voc_count`, `voc_adequacy`
  - `voc_top20` é o ranking curado da Skill 02 (20 frases com `rank` + `count` + `category`) — é a fonte primária do `voc_checklist` (Input Extraction). `voc_phrases` é o objeto `{problem:[], desire:[], frustration:[]}` — se precisar usar (fallback legado), **achate os 3 pools** num único array antes (não assuma array plano). `voc_count` = total de frases únicas somando os 3 pools.
- [ ] **VOC adequacy check:** se `voc_adequacy == "insufficient"` OU `voc_count < 15` → PARE com mensagem:
  > ⚠️  VOC atual: {N} frases únicas. Mínimo pra copy direta: 15.
  >     Copy sem VOC real é invenção — vai soar genérica e não converter.
  >     Opções:
  >     1. Rode skill 02 (market-research) de novo com mais fontes (Reddit, Amazon reviews, TikTok comments)
  >     2. Me cola manualmente 10-15 frases de clientes reais (reviews, DMs, comentários)
  >     3. Prossiga mesmo assim reconhecendo limitação (copy ficará abstrata)

  Se membro escolher 3, marca `"voc_forced_continue": true` no output pra Skill 11 diagnosticar depois.
- [ ] `03-competitor-analysis/competitor-analysis.md` existe (ou o legado `relatorio.md` — mesmo fallback vale pras outras fases)
- [ ] `04-offer-builder/dados.json` existe → extrair `mechanism` (objeto `{name, ...}` — usar `mechanism.name`, NÃO tratar como string), `pricing`, `guarantee`, `bonuses[]` (cada bonus tem `condition` — dirige a copy de GWP/stack, ver ETAPA 4)
- [ ] `04-offer-builder/research-foundation.json` existe → extrair `evidence_items[]`, `confidence_score`, `gaps_and_risks`
  - Se ausente: WARN "Research foundation não rodou (Skill 04 Etapa 2.5). Claims na copy vão sair sem lastro verificável. Opções: (1) voltar pra skill 04 e rodar Etapa 2.5; (2) prosseguir marcando `claims_unverified: true` no output — skill 09 (consistency-audit) vai bloquear launch depois."
  - Se existe mas `confidence_score == "low"`: WARN "Evidence weak — claims fortes (clinically proven, X% melhoria) vão ser suavizados automaticamente pra 'helps with', 'designed to support'. Skill 09 vai re-validar antes de launch."
- [ ] Extrair `product_vertical` do manifest (default "other" se ausente) — usado pelo Compliance Pre-flight (Sweep 8)
- [ ] Ler `manifest.copy_language` (se presente; default `"en"`) — confirma o idioma da copy consumidor-final. Não confundir com `report_language` (idioma dos relatórios internos): a copy pública segue `copy_language`, que hoje é sempre inglês US pro mercado US

Se faltar qualquer arquivo de fase anterior (02/03/04), em vez de abortar seco ofereça ≥2 caminhos:
> **(A)** Rodar a skill faltante agora (02/03/04), OU **(B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar com o arquivo real. VOC com opção 3 e research-foundation com acknowledgment já seguem esse padrão acima. Exceção: se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes, não há o que inferir — ofereça rodar o setup (skill 00) inline.

## Quando Usar
Quando o membro tem market research, competitor analysis e oferta prontos, e precisa escrever a copy da página que vai converter o tráfego pago. Copy aqui é escrita com base em decisões ESTRATÉGICAS derivadas dos documentos anteriores, não em opiniões ou intuições.

## Antes de Começar

1. Leia `workspace/profile.md` — em especial `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno desta skill (strategy brief, sweeps documentados, `.md`/`.html` descritivos) e toda conversa com o membro usam esse idioma, seguindo o padrão de linguagem simples da regra 0 do `.claude/CLAUDE.md` (nenhuma sigla sem explicação imediata, zero frase de analista comprimida, números estatísticos em palavras). **A copy consumidor-final (headlines, leads, hero, bullets, CTAs, advertorial, email hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language` — copy pública nunca traduz.
2. Leia `workspace/[produto]/02-market-research/market-research.md` (psychographics, awareness/sophistication, VOC literal, objeções, root cause)
3. Leia `workspace/[produto]/03-competitor-analysis/competitor-analysis.md` (claims saturados a evitar, gaps, posicionamento recomendado, swipe file)
4. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (mecanismo único com 3 versões, bundles, garantia, unit economics)
5. **Puxe os SISTEMAS NOMEADOS da base — não query genérica.** Esta skill é o coração do sistema. NUNCA dispare uma busca tipo "copy framework" ou "headlines" — sempre o nome do sistema + sua query curada. **Contrato de cobertura (regra do kb-index):** no início de cada ETAPA que consulta a base, abra `.claude/lib/kb-index/frameworks.json` e enumere TODAS as entradas dos 3 domínios desta skill (copy-headlines-leads, copy-proof-persuasion-structure, persuasion-psychology) cujo `use_in_skill` inclui a 06; rode a `best_query` exata, com `deep=true`, de TODAS as relevantes àquela etapa. As queries embutidas nas ETAPAs 2-6 abaixo (no ponto onde cada framework é usado) são o **núcleo mínimo garantido de cada etapa, nunca o teto** — entrada relevante que não está embutida é pra ser puxada do mesmo jeito. Critério de relevância: "esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa; só descarte o que claramente pertence a outra etapa (será puxado lá). Framework já puxado na sessão não se busca de novo (entradas duplicadas entre domínios apontam pro MESMO conteúdo — reuse o resultado). **Antes de fechar cada ETAPA, releia a lista enumerada e confirme: alguma entrada relevante ficou sem puxar? Se sim, puxe agora.** A fonte da verdade do tamanho de cada domínio é sempre o próprio `frameworks.json`, nunca contagem citada em texto de skill (mapa skill→domínio no `README.md` da lib).

## Fluxo da Skill

### Input Extraction (automático)
Antes de gerar copy, carregue:
1. `dominant_awareness` = ler DIRETO o campo `dominant_awareness` de `02-market-research/dados.json` (a Skill 02 já grava esse campo decidido, com nuance de fonte). Só recompute a partir de `awareness_distribution` (stage com maior %) como FALLBACK se o campo faltar (produto legado) — recomputar quando o campo existe abre porta pra drift em distribuições apertadas. Se `dominant_awareness_secondary` presente (empate ±5pp na 02), trate como híbrido: escolha um lead que sirva os DOIS níveis (ex: empate problem/solution → lead de mecanismo com abertura de problema), não só o primário
2. `sophistication` = `sophistication_stage` (1-5)
3. `voc_checklist` = ler DIRETO o campo `voc_top20` de `02-market-research/dados.json` (a Skill 02 já grava as 20 frases curadas com rank + contagem de menções — use na ordem do rank, a frequência real vale mais que re-curadoria). FALLBACK (produto legado sem `voc_top20`): achate os 3 pools de `voc_phrases` — `{problem, desire, frustration}` — num único array e selecione as 20 mais repetidas antes do substring matching. VOC permanece SEMPRE no inglês original do consumidor.
4. `mechanism` = objeto do `04-offer-builder/dados.json` (use `mechanism.name` pro nome; não tratar como string)
5. `guarantee` + `offer_stack` = do `04-offer-builder/dados.json`
6. `core_avatar` + `sub_avatars[]` = ler DIRETO de `02-market-research/dados.json` — a camada ACIONÁVEL de avatar da 02 (não confundir com o objeto descritivo `avatar`). `core_avatar` define a quem a PÁGINA inteira se dirige: `surface_desire` é a promessa no nível "I want X", `core_desire_behind` orienta o TOM. **O lead fala com UM sub-avatar — o da estratégia escolhida na ETAPA 2** (o de `angle` mais próximo do ângulo principal), nunca com "todos ao mesmo tempo".
7. `labels[]` = os apelidos com que o próprio mercado se nomeia — **matéria-prima de call-out** (headline, kicker/eyebrow, bullets). Usar o label literal gera identificação imediata.
8. `market_vocabulary` = as palavras permitidas e proibidas da 02: `words_used[]` (com flag `saturated_in_market`) e `words_absent[]` (com o substituto `market_says_instead`). Consulte ANTES de escrever qualquer linha — alimenta o gate de vocabulário do sweep 2.

FALLBACK (produto legado sem os campos 6-8 — a 02 rodou antes de eles existirem): derive o foco do objeto `avatar` (psychographics + pain/desire hierarchy) e do `voc_top20`, escreva sem o gate de vocabulário (o sweep 2 checa só o checklist VOC) e recomende na Mensagem Final re-rodar a 02 pra ganhar a camada acionável de avatar.

Use ESTAS variáveis ao gerar — sem placeholders hardcoded.

### ETAPA 1 — Perguntas ao Membro (APENAS 2)

Faça APENAS estas duas perguntas:

**1. Tipo de página:**
"Que tipo de página vamos escrever?
- PDP (Shopify)
- Landing Page dedicada
- Advertorial
- Não sei (o sistema recomenda baseado no awareness level)"

Se o membro disser "não sei", use o awareness level dominante do market research pra decidir:
- **Unaware / Problem Aware** → Advertorial (educação antes do pitch)
- **Solution Aware** → Landing Page dedicada
- **Product Aware / Most Aware** → PDP

**2. Página atual:**
"Tem página atual que quer melhorar? Se sim, me manda o link."

- SE mandar o link: leia/extraia a página (`WebFetch`; se barrado — 403/Cloudflare/password page da loja —, use o fetcher resiliente: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text`, conforme `resilient-fetch.md`; último caso, o membro cola o texto da página) e use como baseline — identifique o que manter (o que funciona) e o que reescrever (o que tá fraco).
- SE não tiver: partimos do zero.

**NENHUMA outra pergunta ao membro.** Todas as decisões estratégicas abaixo são tomadas automaticamente pelo sistema.

### ETAPA 2 — Estratégia de Copy (SISTEMA DECIDE)

Antes de decidir, puxe os SISTEMAS de seleção de estratégia (rode cada `best_query`):
- **Schwartz's Five Stages of Awareness** (rode `Schwartz five stages of awareness headline approach per stage Breakthrough Advertising`) — define a abordagem por awareness dominante
- **Schwartz's Three Lead Dimensions (Desire, Identification, Belief)** (rode `Schwartz lead desire identification belief dimension awareness lead selection`) — define QUAL lead casa com o avatar
- **Schwartz's Five Stages of Market Sophistication** (rode `Schwartz market sophistication five stages new mechanism virgin market skepticism Breakthrough Advertising`) — define se lidera com promessa, mecanismo, ou identificação conforme o estágio de saturação da Skill 03
- **Big Idea (Paradoxical Question, Gum Name, Conspiracy Story)** (rode `Big Idea paradoxical question gum name conspiracy story marketing thesis`) — transforma o gap mais forte da Skill 03 no ângulo dominante
- **Hero Sections (5 Types + 3 Questions)** (rode `hero sections five types selection three questions five seconds awareness`) — value-prop / problem / dreamstate / segment / campaign-level
- **As três escolas de porta-voz** (rode `tres escolas de porta-voz autoridade primeiro credibilidade de baixo autoridade quebrada`) — decide QUEM fala a peça (autoridade primeiro / credibilidade de baixo / autoridade quebrada) antes de escolher o hero pattern e, no advertorial, a Background Story
- **Rule of One (One Reader, One Idea, One Offer)** (rode `Rule of One one reader one idea one offer one promise copy`) — força foco da página inteira; o "one reader" aqui é o sub-avatar escolhido pro lead

O sistema apresenta as decisões como FATO (não pedido de aprovação) e segue pra escrita. Todas vêm do market research + competitor analysis + oferta:

**Tipo de Lead por Awareness:**

| Awareness dominante | Lead recomendado |
|---|---|
| Unaware | Story Lead ou Big Idea Lead (identificação antes do pitch) |
| Problem Aware | Problem-Agitation Lead ou Story Lead |
| Solution Aware | Mechanism Lead / Secret Lead ou Proclamation Lead |
| Product Aware | Offer Lead ou Direct Lead |
| Most Aware | Direct Lead (apela pra oferta/urgência direto) |

Pra CONSTRUIR o lead escolhido, puxe o sistema certo (rode a `best_query`):
- **Story Lead / Background-Emotional-Discovery Stories** (rode `storytelling copy background emotional discovery story spine once upon a time hero journey`) — Unaware / Problem Aware
- **Kennedy's PAS (Problem-Agitation-Solution) + Fortune Telling** (rode `Kennedy PAS problem agitation solution fortune telling winners losers formula`) — Problem Aware
- **Unique Mechanism Theory (UMP + UMS)** (rode `unique mechanism UMP UMS problem solution knowledge gap direct response`) — Solution Aware (Mechanism/Secret Lead)
- **Sugarman's Seeds of Curiosity / Slippery Slide** (rode `Sugarman seeds of curiosity slippery slide open loop paragraph end`) — pra qualquer lead que precisa puxar pra próxima frase
- **Schwartz's 'The Turn'** (rode `Schwartz the turn product introduction inevitable transition after lead story`) — a transição do lead pro pitch
- **As 6 Formas de Bridge + Bridge Hook** (rode `6 formas de bridge introduce mechanism escalate problem reposition timeline`) — as seis maneiras de sair do hook e chegar na oferta sem quebrar a leitura (par operacional do The Turn)
- **Unaware Ads — Buyer's Pyramid + 4 openers** (rode `unaware ads buyers pyramid 4 openers hidden fear hidden desire did you know debate`) — quando o awareness dominante é Unaware (hidden fear / hidden desire / did you know / debate)
- **Identity Lead — 5 beats + 3 variantes** (rode `identity lead manifesto de persona recusa ritual confissao de ex-membro prova de lifestyle`) — o lead-manifesto de persona pra Sophistication 4-5 (a regra diagnóstica da ETAPA 2.5 veta usá-lo fora desse estágio)

Nota de proveniência (não é Schwartz): os 5 tipos de lead acima cruzam três tradições. As fórmulas de primeiro parágrafo vêm de **Caples** (as 6 fórmulas clássicas). A escolha de QUAL lead usar vem da dimensão **Schwartz** de awareness + desire/identification/belief. **Secret Lead** e **Proclamation Lead** são da tradição **Masterson**, não de Schwartz. Mapeamento canônico: Unaware → story/identification · Problem Aware → problem-agitation · Solution Aware → mechanism/secret · Product/Most Aware → direct/offer.

**Hero Patterns (ecom)** — estes são padrões práticos de execução, não os "5 tipos" canônicos da base:
- **Authority hero** (expert, doctor, scientist apresentando): indicado pra Solution Aware + high-trust products
- **UGC/Testimonial hero**: indicado pra Problem Aware + baixa confiança inicial
- **Product-hero** (produto em destaque): Product Aware + Most Aware
- **Problem-agitate hero**: Problem Aware com dor forte e frequente
- **Demo/before-after hero**: quando transformação visual é forte e rápida

(Cruzando com os 5 tipos canônicos de hero da base — value-prop / problem / dreamstate / segment / campaign-level: Authority e Product-hero servem o value-prop hero; Problem-agitate é o problem hero; Demo/before-after empurra pro dreamstate; UGC/Testimonial costuma ancorar segment ou campaign-level.)

Decisão aplica: awareness + tipo de produto + presença de visual transformation + tipo de ceticismo do avatar.

**Ângulo Principal** (do competitor analysis):
- Escolha o gap mais forte identificado na Skill 03 (angle que NENHUM concorrente está usando)
- Esse vira o **Big Idea** da página — o ângulo dominante que unifica headline, subheadline, e hook
- Cruze com `sub_avatars[]` da 02: escolha o sub-avatar cujo `angle` casa com esse gap — **é com ELE que o lead fala** (Rule of One: one reader). Registre a escolha no brief abaixo

**Tom de Voz** (do market research):
Definido pelo perfil psicográfico (e pelo `core_desire_behind` do `core_avatar` — o instinto por trás do desejo orienta o registro emocional):
- Sofisticado/educado (público com renda alta, escolaridade, sofisticação do mercado)
- Casual/conversacional (público mainstream, Gen Z/millennial)
- Técnico/autoridade (público que valoriza credenciais — saúde, finanças)
- Emocional/empático (público vulnerável — dor crônica, luto, autoimagem)
- Urgente/direto (público que decide na hora, já acostumado a ads)

**Framework de Organização:**
- **PDP** → estrutura: Hero → Trust Bar → Benefícios → Mecanismo → Prova Social → Oferta/Stack → Garantia → FAQ → CTA final
- **Landing Page** → 10x Page Plan ou PAS on Steroids
- **Advertorial** → 7-section blueprint (estilo da masterclass interna): Headline → Lead → Background Story → Root Cause → Unique Mechanism → Product Build-Up → Product Reveal + Close (7 seções; Reveal e Close são UMA seção combinada — ver ETAPA 5)
- **Long-form Sales Page** → 15-point themeplate ou 8-block VSL structure

**Como servir as 4 Decision Making Modalities**:

Puxe os princípios de influência que sustentam as 4 modalidades (rode cada `best_query`):
- **Cialdini's Six Weapons of Influence** (rode `Cialdini six weapons of influence reciprocity commitment social proof authority liking scarcity`) — reciprocity/social proof/authority/scarcity distribuídos pelas 4 modalidades
- **The Unity Principle (7th Weapon)** (rode `Cialdini Unity principle seventh weapon being together acting together asking advice merger mindset`) — pro Humanistic (comunidade/identidade)
- **Schwartz Gradualization / Believability Bridge** (rode `Schwartz gradualization believability bridge belief gap intermediate beliefs Breakthrough Advertising`) — pro Methodical (yes-momentum, prova encadeada)

Toda página precisa SIMULTANEAMENTE servir os 4 tipos de decisor (senão perde conversão de 25-75% dos visitantes):

- **Spontaneous** (decide rápido, emocional) → hero visual forte + promessa clara + CTA óbvio acima do fold
- **Competitive** (quer dominar, odeia perder vantagem) → comparação, "best in class", escassez, urgência
- **Humanistic** (empático, social) → testimonials, UGC, story do fundador, comunidade
- **Methodical** (analítico, quer provas) → ingredient breakdown, estudos, FAQ detalhada, specs, reviews com detalhes técnicos

Apresente a estratégia (6-8 linhas no máximo) como um BRIEF antes de escrever:

> Baseado no market research (awareness: {{dominant_awareness}}, Sophistication: Estágio {{sophistication_stage}}) e gaps do competitor analysis ([gap X]), vou escrever [tipo de página] com [tipo de lead], hero [tipo], ângulo [ângulo], tom [tom], usando o framework [X]. O lead fala com o sub-avatar [nome do sub-avatar escolhido] (angle: [angle dele]). Mecanismo único: {{mechanism.name}}. VOC phrases prioritárias: [3 frases-chave do voc_checklist]. Objeções principais a quebrar: [3].

(Os placeholders `{{...}}` indicam valores vindos do Input Extraction — NÃO usar números fixos como "45%" ou "Estágio 4".)

Não peça aprovação — segue direto pra escrita. O membro pode ajustar depois se quiser, mas o default é o sistema executar a decisão fundamentada.

**Persistir a decisão de lead (contrato com a 07a):** o tipo de lead escolhido nesta etapa DEVE ser gravado no campo **top-level `lead_type`** do `06-copy-engine/dados.json` (ver Output Schema). A 07a lê esse campo pra confirmar o `page_type` da página — sem ele, a fase STOREFRONT decide no escuro.

### ETAPA 2.5 — Seleção de Espécime (Swipe Modeling) — OBRIGATÓRIA

> Frameworks dizem O QUE fazer. Espécime mostra COMO uma peça que já converteu foi montada, bloco a bloco. Copywriter de verdade não escreve só com framework na mesa — ele escolhe a peça provada mais próxima e modela a estrutura. Esta etapa faz isso explicitamente, antes de escrever qualquer linha.

**2.5A — Selecionar o espécime primário.**

Leia `.claude/lib/swipe-models/specimens.json`. Cruze o seletor de cada espécime (`aplica_a`: `page_type` × `dominant_awareness` × `sophistication_stage` × `product_vertical`) com as decisões que a ETAPA 2 já tomou. Precedência: `page_type` restringe primeiro; depois awareness; `sophistication` desempata (4-5 empurra pra espécimes de identidade/mecanismo); vertical só refina.

Leia a `regra_diagnostica` do candidato antes de fechar — ela existe pra vetar escolha errada (ex.: Identity Lead só serve estágio 4-5; discovery story exige evento dramático real ou defensável, senão use problem-agitation em vez de fabricar história).

Escolha **1 espécime primário**. Opcionalmente **1 secundário**, só quando houver um bloco específico que o primário não resolve bem (ex.: primário = advertorial de 7 seções, secundário = escada de prova em 3 degraus do chassi de VSL).

**2.5B — Puxar a anatomia.**

Rode `search_knowledge` com a `best_query` do espécime escolhido (e do secundário, se houver). Rode também a régua medida da base: **Anatomia da Promo — 11 blocos, presença medida em 179 promos** (rode `11 blocos promo Agora kicker saudacao qualificada mecanismo batizado presenca medida`) — a frequência real de cada bloco (kicker, saudação qualificada, big idea narrativa, mecanismo batizado) calibra o modelo estrutural contra o que as peças que converteram de fato fazem. Extraia:
- a **sequência de blocos** da peça, em ordem
- **que trabalho cada bloco faz** (não o texto dele)
- a **regra diagnóstica** que a nota documenta

Se a query não retornar a anatomia, escolha o próximo espécime aplicável e registre o fato — escrever sem modelo é o comportamento antigo, e é o que esta etapa existe pra evitar.

**2.5C — Montar o modelo estrutural.**

Antes de escrever, produza a tabela de blocos que a copy vai seguir:

| # | Bloco (do espécime) | Trabalho que faz | O que entra aqui (do research do membro) |
|---|---|---|---|

Preencha a última coluna com o material real das skills 02/03/04 — VOC, mecanismo, prova, objeções, oferta. **É essa tabela que vira a copy nas ETAPAs 3-5**, não o espécime.

Declare também os **4-6 pilares** da peça (leia `arquitetura_de_extensao` no mesmo JSON). Copy longa que funciona não é muito conteúdo — é um número pequeno de ideias reapresentadas, onde o que muda a cada volta é a **prova**, nunca a ideia. Cada bloco de corpo deve marcar qual pilar reforça e com que prova nova. Isso alimenta a dieta do sweep 4.5: pilar que volta **sem** prova nova é gordura; pilar que volta **com** prova nova é a arquitetura funcionando.

**2.5D — Aplicar o scaffold universal de lead.**

Independente do espécime escolhido, o lead precisa cumprir os 4 passos do Makepeace (rode `grab eyeballs expand headline establish credibility bribe esqueleto de abertura`): grab eyeballs (ideal prospect + big promise + curiosidade) → expand headline → establish cred → bribe. É a segunda camada sobre o espécime primário; lead que não cumpre os 4 passos não está pronto.

> **REGRA INEGOCIÁVEL — modelar estrutura, nunca conteúdo.** Não copie frase, claim, número ou nome de mecanismo do espécime. Além de plágio, boa parte do arquivo de health é anterior à política atual do Meta e carrega disease claims que reprovam no gate de compliance (sweep 8). O que se extrai é arquitetura: ordem dos blocos, trabalho de cada um, e por que funciona.

Registre no `dados.json`: `specimen_primary` (id), `specimen_secondary` (id ou null), e `specimen_block_map` (a tabela 2.5C). A skill 11 (ad-analysis) usa isso pra diagnosticar depois se a estrutura escolhida foi a certa pro avatar.

### ETAPA 3 — Headlines (Processo de 100 Linhas, versão condensada)

> O processo canônico gera 100 linhas; aqui rodamos a versão condensada (20-30 variações) que preserva as fases do framework (gerar em volume sem julgar → categorizar → top 5 → 3 hipóteses A/B) sem estourar contexto. As primeiras variações "ruins" continuam fazendo parte do método — elas destravam as boas.

Puxe os SISTEMAS de headline da base antes de gerar (rode cada `best_query` — não query genérica tipo "headlines"):
- **100-Headline Exercise (Process)** (rode `100 headlines exercise process first 20 suck VOC immersion prereqs`) — o processo que governa esta ETAPA inteira
- **Caples' 35 Proven Headline Formulas + Three Classes** (rode `Caples headline formulas three classes self-interest news curiosity techniques`)
- **Caples' Six First-Paragraph Formulas** (rode `Caples six first-paragraph formulas interrupting idea shocker news preview quotation story`)
- **Schwartz's 38 Verbalization Techniques** (rode `Schwartz 38 verbalization techniques Breakthrough Advertising strengthening claim`) — pra fortalecer cada claim na headline
- **Bencivenga's I = B + C Formula** + **Shake-Me-Awake-at-3AM Test** (rode `Bencivenga I=B+C formula interest benefit curiosity headline evaluation` e `Bencivenga shake me awake at 3am test headline strength`) — pra avaliar força de cada variação
- **Four U's (Unique, Useful, Urgent, Ultra-specific)** (rode `Four U's unique useful urgent ultra-specific hook headline hierarchy`) — grade rápido das top variações
- **Hormozi's Seven Headline Components** (rode `Hormozi seven headline components callout value timeframe proof mechanism obstacle urgency $100M Leads`) — pra ofertas/Product-Most Aware
- **Hopkins: Headlines as Audience Selectors + Specificity** (rode `Hopkins headlines audience selectors preemptive claim specificity Scientific Advertising`) — specificity converte 2-3x sobre generalidade
- **Sticky Hook — 3 must-haves** (rode `sticky hook emotion curiosity gap high stakes targeted vs broad ad`) — emoção + curiosity gap + stakes altos: o critério mínimo que toda headline/hook precisa cumprir
- **Promise vs Open Loop** (rode `make a promise vs open a loop juxtaposition fear do the opposite Harry Dry`) — a decisão binária de cada variação: PROMETER ou ABRIR LOOP (e as 3 formas de abrir o loop)
- **Labels + Word Swapping** (rode `labels callout de identidade word swapping linguagem do cliente urban dictionary`) — `labels[]` da 02 como call-out de identidade; troque a palavra da marca/indústria pela palavra que o cliente usa
- **Headline Sweep (8-Part Laddering Edit)** (rode `headline sweep eight parts captures attention avoids confusion matches message button SEO`) — pra refinar as top 5 na sub-etapa 3B

Aplique os princípios do processo de 100 linhas (Caples, expandido) e as fórmulas clássicas acima.

**3A — Geração (20-30 variações):**

Gere 20-30 variações de headline aplicando as fórmulas. Cobrir diferentes tipos:

- **Benefício direto**: "Get [outcome] without [pain]"
- **Curiosidade**: "The [adjective] secret [audience] don't know about [topic]"
- **Problema**: "If you [problem], you're not alone — but there's a reason"
- **Resultado com especificidade**: "[Specific number] [specific outcome] in [specific time]"
- **Mecanismo único**: "Introducing the [mechanism name] — [what it does]"
- **Contrarian/controversy**: "Why [common belief] is actually making [problem] worse"
- **Question hook**: "What if [familiar problem] wasn't your fault?"
- **Testimonial hook**: "[Specific person] lost [specific number] in [time] — here's how"
- **Authority**: "[Expert title] reveals the [claim]"
- **Fear of loss**: "The [thing you're missing] that [outcome]"

Use linguagem EXATA do VOC do market research sempre que possível. Hopkins: "specificity in headlines converts 2-3x over generality". Pro call-out (componente #1 do Hormozi), use os `labels[]` da 02 — o apelido com que o mercado se nomeia é o call-out mais forte que existe. E consulte `market_vocabulary` JÁ NA GERAÇÃO: termo com `saturated_in_market: true` não entra em headline (mensagem fatigada — só como prova no corpo); termo de `words_absent[]` não entra em lugar nenhum (use o `market_says_instead`).

**3B — Categorização + Top 5:**

Categorize as 20-30 por tipo. Selecione **top 5** com justificativa explícita por que cada uma funciona pro awareness level + ângulo + tom + Big Idea.

**3C — 3 pra Teste A/B:**

Das top 5, escolha 3 que representam HIPÓTESES DIFERENTES (não variações cosméticas):
- Headline 1: hipótese de ângulo dominante
- Headline 2: hipótese alternativa (ângulo secundário)
- Headline 3: hipótese de formato diferente (ex: pergunta vs afirmação)

Justifique cada escolha.

### ETAPA 4 — Página Completa (Seção por Seção)

Escreva a página inteira, seção por seção, na ordem definida pelo framework escolhido. Para cada seção, aplique frameworks específicos.

Antes do corpo, puxe a ordem macro do pitch: **Pitch Sem Rejeição (Payoff → Belief → Recomendação)** (rode `pitch sem rejeicao entregue o payoff estabeleca belief recomendacao em vez de venda`) — entregue primeiro o payoff que o lead prometeu, estabeleça a crença necessária, e só então RECOMENDE o produto em vez de vendê-lo (vale pra PDP/LP e igualmente pro advertorial da ETAPA 5).

#### Hero Section

- **Headline**: a #1 das top 5 (pode ajustar um pouco pra fit com hero)
- **Sub-headline**: 1-2 linhas que expandem a promessa, introduzem o mecanismo único
- **CTA principal**: texto do botão (call to VALUE, não call to action — ex: "Get My [Outcome]" em vez de "Buy Now")
- **Instrução visual**: que imagem/vídeo colocar (hero type já decidido — authority/UGC/product/problem/demo)

#### Trust Bar (opcional)

Se o produto tem credenciais (mídia coverage, certificações, reviews count), coloca logo abaixo do hero:
"Featured in Forbes · 4.8★ (12,000 reviews) · Dermatologist-tested"

#### Benefits / Problem Block

Frameworks pra esta seção (rode cada `best_query`):
- **Fascinations / Bullets as Teasers (Mega List)** (rode `fascinations bullets teasers not tell-alls mega list curiosity loop checkmarks six versus nine`) — cada bullet abre loop, não entrega tudo
- **Cashvertising Life-Force 8 (LF8)** (rode `Cashvertising Life-Force 8 LF8 eight biological desires survival social approval superiority Whitman`) — ancora o emocional ("por trás do por trás") no desejo biológico certo
- **Blair Warren's One-Sentence Persuasion** (rode `Blair Warren one sentence persuasion encourage dreams justify failures allay fears confirm suspicions throw rocks enemies`) — pra externalizar culpa no problem block

Use a linguagem EXATA do VOC. Não parafraseie. Cada bullet:
- Começa com a frase/palavra do consumidor (do market research)
- Expande com o benefício funcional
- Termina com o emocional (o "por trás do por trás" do desejo)

3-5 bullets de benefício. Se é Problem Aware/Unaware, começa com dor; se é Solution/Product Aware, começa com resultado.

#### Unique Mechanism Expandido

Frameworks pra esta seção (rode cada `best_query`):
- **Unique Mechanism Theory (UMP + UMS)** (rode `unique mechanism UMP UMS problem solution knowledge gap direct response`) — separa o mecanismo do PROBLEMA (por que falhou) do mecanismo da SOLUÇÃO (por que o seu funciona)
- **Schwartz Mechanization Stages (Mechanism Proof)** (rode `Schwartz mechanization stages name describe feature mechanism promise reason why headline`) — quanto explicar o mecanismo conforme sophistication
- **Made to Stick — Three Wellsprings of Credibility + Sinatra Test** (rode `Made to Stick three wellsprings credibility external internal audience-testable Heath`) — torna o mecanismo crível sem só afirmar

Use a **versão 1 parágrafo** do mecanismo da oferta (ou a 2-3 parágrafos se for LP dedicada ou advertorial). Adaptado ao awareness level:
- Problem Aware → explica a root cause ANTES do mecanismo (educação)
- Solution Aware → compara com soluções genéricas e posiciona o mecanismo como a evolução
- Product Aware → foca na especificidade do mecanismo (ingredientes, dosagem, processo)

Inclua:
- Nome do mecanismo (do 04-offer-builder/offer-builder.md)
- Como funciona (biology/mechanism of action se aplicável)
- Por que é diferente
- Referência a evidência (estudo, ingredient research, patents se aplicável)

#### Prova Social (Proof Stacking)

Aplicar os frameworks de proof — puxe cada um por nome (rode a `best_query`):
- **Hopkins' Specificity Principle (Reason-Why)** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`)
- **Schwab's Ten Categories of Proof + Five Presentation Principles** (rode `Schwab ten categories of proof taxonomy five principles presenting proof testimonials`) — o menu completo de tipos de prova
- **Sugarman's Satisfaction Conviction** (rode `Sugarman satisfaction conviction objection raising resolution before order form doubt friction`) — levanta e resolve dúvida antes do botão
- **The Sinatra Test + Human-Scale Principle** (rode `Sinatra Test one example so impressive establishes credibility case study` e `Made to Stick human-scale principle statistics as relationships Disneyland 99.9 percent`) — 1 prova devastadora + estatística traduzida pra relação humana
- **Prova em Escada (3 degraus)** (rode `prova em escada funcionou em mim no cetico mais proximo espalhou numero quebrado`) — a ordem de montagem do stack: funcionou em mim → funcionou no cético mais próximo → espalhou-se, fechando com número quebrado
- **Length-Implies-Strength Heuristic** (rode `length implies strength heuristic volume persuasion cue 101 testimonials 22 reasons`) — volume de prova vira sinal de força

- **Social proof volume**: número de clientes, reviews, anos no mercado
- **Specific testimonials**: 3-5 testimonials com NOMES COMPLETOS, FOTOS, e RESULTADOS ESPECÍFICOS (com datas e números quando possível)

  Se o membro não tem testimonials reais ainda (lançamento novo):
  - Use `{{TESTIMONIAL_PLACEHOLDER_1}}` no copy e liste no final:
    "### Testimonials needed: [frase_motora, resultado_especifico, perfil_demografico] × 3"
  - NÃO gere testimonials fictícios com nomes aleatórios.
  - Proof stack fica com placeholder até membro coletar via email / WhatsApp com clientes existentes.
- **Authority proof**: menções em mídia, certificações, endorsement de experts
- **Before/After** (se visual e o produto permite): imagens com legendas
- **Science/ingredient research**: evidência técnica se apropriado

Organize em formato visual navegável (tiles, carrossel, grid).

#### Oferta / Stack Com Ancoragem

Do `04-offer-builder/offer-builder.md`:
- Produto com nome
- Bundles (Solo / Popular 3-pack / Best Value 6-pack) com savings visíveis
- Bump (produto complementar baixo ticket)
- Stack de valor: "Você recebe [X + Y + Z] no valor de $[total ancorado]. Hoje: $[preço]"
- Savings visíveis ("Você economiza $[diff] hoje")

**Bônus/GWP respeitam `bonuses[].condition` do `04-offer-builder/dados.json`** (extraído no pré-flight) — a copy do stack DEVE refletir a condição configurada:
- `cart_threshold` → a copy diz a condição explícita ("FREE [bonus] on orders over $X") — NUNCA prometa incondicional um brinde que só destrava por subtotal
- `unconditional` → sem condição na copy (todo comprador recebe)
- `tier_specific` → o brinde aparece SÓ no tier que o destrava (3-pack/6-pack), não no stack geral

Mismatch entre a promessa da página e a `condition` real é promessa quebrada no checkout — o GATE 2 (promise↔config) bloqueia por isso.

Aplique **pricing psychology** — puxe os sistemas por nome (rode cada `best_query`):
- **Anchoring & Adjustment + Contrast Principle** (rode `anchoring adjustment Tversky Kahneman SSN auction real estate listing reference price Poundstone`) — o valor ancorado do stack
- **Decoy Effect (Asymmetric Dominance)** (rode `decoy effect asymmetric dominance Economist Ariely pricing tiers print-only combo`) — o 3-pack Popular como decoy
- **Extremeness Aversion + Three-Tier Pricing** (rode `extremeness aversion three tier pricing middle option beer experiment Simonson Tversky`) — por que a opção do meio ganha
- **Charm Pricing (9-Endings) & Transaction Utility** (rode `charm pricing nine endings left digit transaction utility was price deal Poundstone Thaler`) — framing de "savings" e was-price
- **Os 4 tipos de Reason-Why** (rode `quatro tipos de reason-why preco existencia generosidade mecanismo razao operacional`) — razão OPERACIONAL pra preço/escassez, razão MORAL pra generosidade/garantia; trocar uma pela outra inverte o efeito (também governa a razão real da seção Urgency/Scarcity abaixo)

#### Garantia

Do `04-offer-builder/offer-builder.md`, a copy de garantia (2-3 frases, tom confiante, detalhes claros).

Posicione com destaque visual (box, shield icon, destaque colorido).

#### FAQ

Frameworks pra quebrar objeção (rode cada `best_query`):
- **Inoculation Theory (McGuire)** (rode `Inoculation theory McGuire weakened attack vaccination strengthen attitudes competitor argument`) — antecipa e neutraliza a objeção antes que ela cresça
- **Kennedy's Damaging Admission** (rode `Kennedy damaging admission list every reason not to respond admit flaws too good to be true`) — admitir a falha desarma o ceticismo
- **The 'Yeah, Sure' Principle (Proof Matches Claim)** (rode `Bencivenga yeah sure principle proof match claim three reasons why IF THEN construction doctors headache`) — cada resposta de FAQ precisa de prova proporcional ao claim
- **Matriz de objeções (3 tipos × 4 estratégias)** (rode `3 tipos de objecao 4 estrategias facts reversals because reassigning matriz eficacia`) — pra cada objeção da 02, classifique o TIPO e escolha a estratégia (facts / reversals / because / reassigning) que a matriz indica como mais eficaz pra ele

Cada FAQ quebra uma objeção REAL do market research. Pegue as **Top 5 objeções priorizadas** da Skill 02 e escreva a resposta que quebra cada uma. Nada de FAQ genérica ("qual o prazo de envio" — isso vai em lugar específico, não é FAQ estratégica).

FAQ estratégica típica:
- "Vai funcionar pra mim se eu já tentei X?" (quebra "já tentei e não deu certo")
- "É seguro pra [condição específica do avatar]?" (quebra medo)
- "E se não funcionar?" (reforça garantia)
- "Por que é diferente do [concorrente comum]?" (quebra comparação)
- "Quando começo a ver resultado?" (quebra time delay)

#### CTA Final

Frameworks pro close (rode cada `best_query`):
- **Pain-to-Hope CTA Transition + CTA Style Matrix** (rode `pain to hope CTA transition style matrix emotional trigger solution-aware avoidance call to value`) — call to VALUE casado com o awareness
- **Closing: Propellants vs Repellants + Temporal Discounting** (rode `propellants repellants temporal discounting close carrot caveman cost of inaction immediate`) — remove repellants, ativa custo da inação
- **Future Pacing** (rode `future pacing copywriting commitment consistency imagine your life with the product better self`) — projeta o membro no resultado antes do clique

Call to VALUE, não call to action. Reforça o outcome + remove fricção:
- "Claim My [Outcome]" (não "Buy Now")
- "Start My [Transformation]"
- "Get [Specific Result] Today"

Repita CTA em 3-5 pontos da página (após hero, após mecanismo, após social proof, após oferta, no final).

#### Urgency/Scarcity

Curta e com razão REAL — urgência inventada (countdown falso, "only 3 left" de mentira) destrói confiança e viola policy. Ancore num elemento verdadeiro da oferta da 04: bônus que expira de verdade, preço de lançamento com data definida, lote/estoque real limitado, GWP por threshold enquanto durar. Escreva 2-4 frases prontas pra usar junto da oferta e no close (esta é a seção canônica `## Urgency/Scarcity` do relatório e o campo `urgency` do dados.json). Se a oferta da 04 NÃO tem nenhum elemento de urgência real, registre isso no relatório e entregue a página sem urgência fabricada — o custo da inação (Temporal Discounting, já puxado no CTA Final) cobre o empurrão. NÃO invente escassez.

#### Seções Adicionais (se fizer sentido)

- **Comparação com concorrentes** (se Product Aware): tabela "Nosso produto vs [concorrente A] vs [concorrente B]" com dimensões claras (ingrediente, preço, guarantee, mechanism)
- **How it works** (se mechanism exige explicação): 3-step visual (Step 1 → Step 2 → Step 3) com ícones e copy curta
- **Before/After grid** (se visual): 3-4 comparisons
- **Ingredient/feature spotlight** (se ingredient-based mechanism): cada ingrediente com benefit e research
- **Specs objetivas (legíveis por agente de compra AI)** — recomendado em TODA PDP: um bloco curto de especificações concretas e verificáveis (materiais/ingredientes com dosagem exata, dimensões/peso, quantidade por unidade, certificações reais, país de fabricação, modo de uso em passos numerados). Agentes de compra AI (ChatGPT/Perplexity shopping e afins) decidem lendo specs e dados estruturados, não copy sensorial — uma página sem specs objetivas fica invisível pra esse tráfego crescente. Escreva como fatos secos (Hopkins: especificidade sem adjetivos); a skill 07e (agentic-readiness) audita esse bloco depois.

### ETAPA 5 — Se for ADVERTORIAL (Alternativa à Etapa 4)

Frameworks pra advertorial (rode cada `best_query`):
- **Halbert's Editorial Look / Invisible Selling (5x Readership)** (rode `Halbert editorial look invisible selling 5x readership does not appear to sell advertorial`) — o tom editorial não-vendedor que governa a peça inteira
- **Storytelling in Copy (Background / Emotional / Discovery Stories + Story Spine)** (rode `storytelling copy background emotional discovery story spine once upon a time hero journey`) — pra a Background Story (seção 3)
- **Sugarman's Slippery Slide + Seeds of Curiosity** (rode `Sugarman slippery slide every element read the next sentence frictionless`) — mantém o leitor descendo parágrafo a parágrafo
- **Schwartz's 'The Turn'** (rode `Schwartz the turn product introduction inevitable transition after lead story`) — a transição do Root Cause pro Mechanism Reveal (seção 4→5)
- **Cashvertising — 12 Ways to Lure Readers Into Copy** (rode `Cashvertising 12 ways lure readers into copy question authority skepticism story bandwagon short first sentence`) — pro Lead (seção 2)

Se o tipo de página definido é Advertorial, siga a **estrutura de 7 seções** (blueprint da masterclass interna):

1. **Irresistible Headline** (estilo editorial, não-vendedor: "The Weird 30-Second Ritual That's Changing How Women Over 40 Handle [Problem]")
2. **Lead** que pulls readers in (primeiras 100-200 palavras — responde as 4 perguntas mentais do leitor: por que ler agora? por que isso importa? por que isso é diferente? por que vai funcionar pra mim?)
3. **Background Story** (storytelling pessoal ou de terceiro — builds empathy + credibility — aplica a Discovery Story)
4. **Root Cause Explanation** — use a causa raiz do market research (Etapa 6 da Skill 02). Explique o problema de forma clara, externaliza a culpa (genética, hormônios, indústria — NÃO o leitor)
5. **Unique Mechanism Reveal** — apresente o mecanismo único como a descoberta, a revelação (use a versão de 2-3 parágrafos do 04-offer-builder/offer-builder.md)
6. **Product Build-Up** — traz o produto no contexto do mecanismo. Primeiros parágrafos são sobre o MÉTODO/PRODUTO antes da oferta
7. **Product Reveal + Close** — oferta, stack, garantia, urgência, CTA. Manipulation close (scarcity real, bonus que expiram, urgency com razão). O trecho de urgência do close também é extraído pra seção canônica `## Urgency/Scarcity` do relatório (e pro campo `urgency` do dados.json), com a mesma regra da ETAPA 4: razão REAL, nunca escassez inventada

Tom editorial (não vendedor). Use parágrafos curtos (2-4 linhas). Inclua imagens/quotes entre parágrafos.

No arquivo final (`copy-engine.md`), estas 7 seções entram com os nomes canônicos H2 do Output Schema (`## Advertorial Headline` → `## Reveal + Close`) — ver a seção "Output Schema" abaixo. É por esses nomes exatos que a 07a mapeia o advertorial pro design da página.

### ETAPA 6 — Auto-Revisão (7 sweeps Aura + gate de compliance)

Antes de entregar, faça os **7 sweeps Aura** abaixo (1–7) — são os sweeps de revisão DESTA skill, não os "7 sweeps" clássicos de copywriting. O **Compliance Pre-flight (sweep 8)** roda em seguida como gate de bloqueio separado, fora da contagem dos 7.

Pra calibrar o que cada sweep procura, puxe os sistemas de edição (rode cada `best_query`):
- **Seven Sweeps (Editing Ladder)** (rode `Seven Sweeps editing ladder clarity voice tone so what prove it specificity heightened emotion zero risk`) — o ladder canônico que inspira estes sweeps
- **Hopkins' Specificity Principle** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`) — pro Specificity sweep (#3)
- **Mona Lisa Frame (show, don't tell)** (rode `Mona Lisa Frame show dont tell placa embaixo do quadro half the words double the examples`) — também pro Specificity sweep (#3): mostrar em vez de afirmar — metade das palavras, o dobro dos exemplos
- **Sugarman's Slippery Slide** (rode `Sugarman slippery slide every element read the next sentence frictionless`) — pro Flow sweep (#4)
- **5 Alavancas de Stakes** (rode `5 alavancas de stakes bigger witnesses urgent permanent cost more revisao`) — passada de revisão que eleva o que está em jogo (maior / testemunhas / urgente / permanente / custo); aplicar onde a peça está morna
- **Checklist do Copywriter (13 checagens)** (rode `checklist de revisao do copywriter 13 checagens sanity check onde posso dramatizar`) — o sanity check final da peça inteira, rodado DEPOIS dos sweeps 1-7 (inclui o "onde ainda dá pra dramatizar?")
- **Reeves' USP + Vampire Claims** (rode `Reeves USP burning glass vampire claims mosaic structure single proposition unrelated claims`) — pro Originality sweep (#7), pra não cair em claim saturado/genérico:

1. **Clarity sweep**: cada frase é clara em primeira leitura? Jargão sem explicação?
2. **Customer voice sweep (VOC compliance)**: checklist dinâmico — passe o `voc_checklist` como lista. Para cada frase VOC:
   - [ ] Aparece LITERAL no copy? (marca se sim)
   - [ ] Aparece parafraseada? (marca se só aproximação)
   - [ ] Ausente? (marca como gap)

   Taxa mínima: >= 60% das top-20 VOC phrases presentes literais ou parafraseadas. Se < 60%, regerar seções fracas.

   **Gate de vocabulário (contrato com `market_vocabulary` da 02) — roda no mesmo sweep:**
   - Ctrl+F em CADA termo de `market_vocabulary.words_absent[]`: qualquer ocorrência na copy é **PROIBIDA** — a pesquisa provou que o mercado não fala assim. Substitua pelo `market_says_instead` do próprio campo e re-cheque.
   - CADA termo com `saturated_in_market: true` NÃO pode aparecer em headline (nas variações da ETAPA 3 nem em crosshead que faz papel de headline) — mensagem fatigada serve só como prova no corpo. Se apareceu, reescreva a headline.
   - `labels[]` são matéria-prima de call-out: se a 02 coletou labels e NENHUM aparece na peça (call-out, kicker, bullets), corrija ou justifique no relatório do sweep.
   - FALLBACK legado: sem `market_vocabulary` no dados.json da 02, o gate roda só com o checklist VOC acima — e a Mensagem Final recomenda re-rodar a 02.
3. **Specificity sweep**: Hopkins — cada claim genérico foi substituído por específico? ("many customers" → "12,847 customers"; "fast results" → "visible improvement in 14 days")
4. **Flow sweep**: slippery slide de Sugarman — cada frase compele a próxima? Onde há quebra de fluxo?
   - **Em-dash check (rule 8a, ACIONÁVEL):** conte os travessões (—) por peça. Se `em_dash_count > 0` em QUALQUER headline OU `> 2` em copy longa → **REESCREVER** os trechos afetados substituindo o travessão por ponto, vírgula, parênteses, duas frases curtas, ou dois-pontos, e **re-checar** a contagem depois. Não basta medir: o sweep só passa quando headlines têm zero travessão e a copy longa tem ≤2.
4.5. **Dieta de copy (extensão sob controle)**: conte as palavras da página inteira e por seção. A força da copy vem da PROVA, não do volume — o Length-Implies-Strength continua valendo pra prova, specificity e VOC (isso NUNCA se corta). O que a dieta corta é o resto: a mesma ideia dita duas vezes em seções diferentes, adjetivo que não muda a decisão de compra, parágrafo de transição que não move a leitura, benefício reafirmado pela terceira vez sem prova nova. Processo:
   - Se a página passou do teto da categoria (PDP/landing: ~1.800 palavras é sinal de alerta; advertorial aguenta mais) OU o membro pediu "menos texto": monte a proposta de corte — percentual alvo (ex: reduzir ~25-30%) + cortes estruturais (seções que dizem a mesma coisa e podem fundir) — e mostre AO MEMBRO antes de aplicar, com o word count atual e o projetado. Extensão é decisão estratégica; dieta nunca é silenciosa.
   - Ao aplicar, teste frase a frase: cortar esta frase leva junto alguma prova, VOC literal ou claim único? Se sim, a frase fica (ou a prova migra pra outra seção antes do corte).
   - **Teste do pilar (da ETAPA 2.5C):** antes de cortar um bloco por "já foi dito", cheque qual pilar ele reforça e com que prova. Repetição de pilar **com prova nova** não é redundância — é a arquitetura de copy longa (ver `arquitetura_de_extensao` em `.claude/lib/swipe-models/specimens.json`). Só corte quando o pilar voltar sem trazer prova ou ângulo que as voltas anteriores não trouxeram.
   - Depois do corte, re-rode os sweeps 2 (a taxa de VOC continua ≥ 60%?) e 4 (o fluxo continua deslizando sem os conectivos removidos?).
5. **Objection sweep**: cada objeção do market research foi quebrada em algum lugar? Onde está omitida?
6. **CTA sweep**: CTAs são call to VALUE? Aparecem em frequência certa (não muito, não pouco)?
7. **Originality sweep**: comparar com os claims saturados do competitor analysis — onde estou usando um claim saturado? substitua por ângulo original.
8. **Compliance Pre-flight sweep** (OBRIGATÓRIO antes de salvar o arquivo final):

   Claude deve rodar este prompt INLINE (não invocar arquivo externo) pra cada peça de copy gerada — headlines, primary texts, advertorial sections, CTAs, crossheads:

   ```
   Você é Compliance Pre-flight Checker. Analise a copy abaixo contra Meta Ad Policy, FTC substantiation, FDA cosmetic boundary (se vertical = beauty/skincare/supplements), e AI style red flags.

   Vertical: {product_vertical do manifest — default "other"}
   Asset type: {headline | primary_text | advertorial_section | cta | crosshead}
   Plataforma: Meta Ads (padrão)

   Red flags de referência (categoria do vertical): {leia `.claude/lib/compliance-preflight/red_flags.json`, filtre pelo vertical}

   Copy a analisar:
   \"{copy_text}\"

   Retorne JSON conforme o shape definido em `.claude/lib/compliance-preflight/output-schema.json` (essa é a fonte da verdade do formato — siga os campos e enums dela). `rewrite_suggestions[]` é SEMPRE presente (uma entrada por flag não-informational); `rewrite_suggestion` (reescrita COMPLETA da peça) deve ser preenchido SOMENTE quando `severity >= high`; caso contrário, `null`.
   {
     "risk_score": 0,
     "severity": "low|medium|high|critical",
     "overall_verdict": "pass|warning|critical",
     "triggers": [{"phrase": "...", "severity": "...", "reason": "...", "eixo": "...", "suggested_replacement": "..."}],
     "rewrite_suggestions": [{"phrase": "...", "severity": "...", "suggested_replacement": "...", "reason": "..."}],
     "rewrite_suggestion": null,
     "em_dash_count": 0,
     "ai_style_score": 0,
     "recommendation": "..."
   }
   ```

   Ação pelo `overall_verdict` — mesma tabela do GATE 1 de `pre-launch-gates.md` (a rule é a fonte da verdade do protocolo; mapeamento severity→verdict: low → `pass`, medium → `warning`, high/critical → `critical`):
   - `critical` → **BLOCK**: se algum trigger tem `severity: "critical"`, PARAR direto — apresentar os triggers ao membro com as `rewrite_suggestions[]` e pedir revisão manual (rota ES3 se launch urgente). Se o verdict veio só de triggers `high`, aplicar o `rewrite_suggestion` (reescrita completa) e **RE-RODAR este check no texto reescrito**; se ainda `critical`, PARAR e apresentar ao membro — a peça não entra no relatório final sem passar.
   - `warning` → aplicar as `rewrite_suggestions[]` automáticas e re-rodar o check. Se virar `pass`, prosseguir. Se persistir `warning`, salvar a peça MAS logar em `workspace/[produto]/compliance-warnings.json` (path canônico do gate) e citar os warnings na Mensagem Final ("N warnings de compliance — revise se quiser").
   - `pass` → salvar silenciosamente (sem output).

   Além do log de warnings acima, mantenha o log consolidado de TODOS os checks (qualquer verdict) em `workspace/[produto]/06-copy-engine/compliance-log.json`. Se diretório não existir, `mkdir -p` antes de escrever.

9. **Markup audit sweep (método Kyle Milligan)** — auditoria estrutural da peça, rodada DEPOIS dos sweeps 1-7 e do gate de compliance:

   Leia o nó `auditoria` de `.claude/lib/swipe-models/specimens.json` (e, se precisar do detalhe, rode `auditoria markup promo codigo de cores lexico de blocos objection claim proof benefit`). Audite a copy gerada em 5 camadas:

   **Gate de entrada (roda primeiro, é bloqueante):**
   - Teste dos **4 U's** na headline escolhida: Urgent / Useful / Unique / Ultra-Specific — marque passa/reprova em cada um.
   - **Ideal Prospect** e **Big Promise** presentes no lead?
   - Distinção obrigatória: **fato do mundo não é promessa.** "X causa Y" é fato — o leitor não tem o que fazer com ele. Promessa é uma transação: o que ele ganha, em troca do quê. Se o lead abre com fato, ele reprova em Big Promise mesmo que a afirmação seja verdadeira e interessante.
   - **Regra de veredito:** se reprova em 3 dos 4 U's **e** falha em Ideal Prospect ou Big Promise → **não audite o corpo. Reescreva o lead e volte à ETAPA 3.** Auditar corpo de peça que morreu na abertura é desperdício.
   - **Teste da primeira página:** o lead inteiro precisa poder ser rotulado nos três frames (4 U's + 4 emoções + os 4 passos do Makepeace) **dentro da primeira tela/página**. Se algum frame só se resolve depois, o lead está diluído.

   **Camadas de auditoria (documente bloco a bloco)** — as 4 grades na ordem fixa vêm da base: rode `quatro grades auditoria 4 U's lead Makepeace checklist desejabilidade Beats body copy formula`:
   - **Estrutura** — a sequência de blocos bate com o `specimen_block_map` da ETAPA 2.5? Onde divergiu, foi decisão ou descuido?
   - **4 emoções** — New/Only · Safe/Predictable · Easy/Anybody · Big/Fast: marque onde cada uma é ativada. Emoção sem nenhuma ocorrência na peça é buraco.
   - **Lead de 4 passos** — grab eyeballs / expand HL / establish cred / bribe, em ordem. Nota: `cred` **não precisa vir primeiro** — no espécime control auditado, o porta-voz só se apresenta a 40% da peça, e passa; o que não pode é faltar.
   - **Psicologia** — secret knowledge, sense of power, future pacing, WIIFM. O WIIFM tem que estar respondido **antes** da primeira prova, não depois.
   - **Oferta/preço** — a escada `extreme anchor → step down → price anchor → true price` está montada? A adesão é escrita como pertencimento ou como transação? ("subscribe"/"assine" é transação; "faça parte" é pertencimento.)

   **Loop de body copy** — rastreie `Objection → Claim → Proof (3x) → Benefit` parágrafo a parágrafo. O ciclo roda dezenas de vezes numa peça longa, não uma vez por seção. Onde houver Claim sem Proof adjacente, marque.

   **Folha de defeitos** — varra os 12 defeitos catalogados no JSON (o método de rotulagem por camadas + as 12 críticas recorrentes: rode `auditoria com caneta camadas de rotulagem too vague too big too early move to end`). Os que mais aparecem em copy gerada por AI: *too vague*, *lazy copy / obligatory* (bloco escrito por obrigação), *old proof* (prova reciclada), *reads like editorial* (falta WIIFM), *vende a categoria e não o ativo* (prova pertence ao ingrediente/estudo, não ao seu produto), e **prova em ordem decrescente** (número grande antes do pequeno faz o segundo encolher — "too big too early").

   **Output do sweep:** tabela de arco (bloco → camada auditada → veredito → correção aplicada). As correções são aplicadas na hora; o que não puder ser corrigido sem novo research entra na Mensagem Final como recomendação.

Para cada sweep, documente o que mudou (as edits são o output do sweep).

### ETAPA 7 — Variações pra Teste A/B

Gere:
- **3 headlines** diferentes (já feito na Etapa 3C — compile aqui)
- **2 hero sections** com abordagens diferentes (authority vs problem-agitate, por exemplo)
- **2 CTAs diferentes** (call to value variations)
- **3-5 email follow-up hooks** — subject lines/hooks de abertura derivados das top 5 headlines + Big Idea + objeções principais. São o material de partida pros flows da Skill 13 (welcome, abandoned cart, post-purchase) — em inglês US, como toda copy consumidor-final. Vão na seção canônica `## Email Follow-up Hooks` do relatório e no campo `email_hooks` do dados.json.

Documente a hipótese por trás de cada variação. As variações de hero e CTA vão pro dados.json em `hero.variants[]` e `cta_variants[]` (com `hypothesis` preenchida) — presas só na prosa do relatório, a 07a/07b e um A/B test futuro não conseguem consumi-las.

## Output Schema — Seções Canônicas (`06-copy-engine/copy-engine.md`)

O markdown DEVE ter as seções NOMEADAS ASSIM (case-sensitive, H2). Cada seção contém texto pronto pra colar, SEM comentários de instrução no output final.

**PDP / Landing Page (ETAPA 4):**

```
## Hero
### Headlines (ranked)
### Subheadline
### CTA Primary
### CTA Secondary

## Mechanism
## Benefits
## Social Proof
## Offer Stack
## Guarantee
## FAQ
## Urgency/Scarcity
## Email Follow-up Hooks
```

**ADVERTORIAL (ETAPA 5):** o corpo da página usa estas seções canônicas no LUGAR do bloco `## Hero`→`## FAQ` acima — EXATAMENTE estes nomes, case-sensitive (a 07a localiza o advertorial por eles):

```
## Advertorial Headline
## Lead
## Background Story
## Root Cause
## Mechanism Reveal
## Product Build-Up
## Reveal + Close

## Urgency/Scarcity
## Email Follow-up Hooks
```

As 7 seções mapeiam 1:1 pro blueprint da ETAPA 5 (Irresistible Headline → `## Advertorial Headline`; Root Cause Explanation → `## Root Cause`; Unique Mechanism Reveal → `## Mechanism Reveal`; Product Reveal + Close → `## Reveal + Close`). `## Urgency/Scarcity` e `## Email Follow-up Hooks` continuam obrigatórias no fim do relatório em qualquer tipo de página — a urgência do advertorial vive dentro de `## Reveal + Close` E é extraída pra seção canônica, como a ETAPA 5 já define.

## JSON Companion Obrigatório — `06-copy-engine/dados.json`

Schema:
```json
{
  "copy_id": "uuid-v4",
  "product_slug": "...",
  "offer_id": "ref ao 04-offer-builder/dados.json",
  "lead_type": "story | big_idea | problem_agitation | mechanism | secret | proclamation | offer | direct",
  "hero": {
    "headlines": [
      {"id": "h-01", "text": "...", "type": "benefit|curiosity|authority|contrarian|big_idea", "score": 9.2, "reasoning": "..."}
    ],
    "top_5_ranked": ["h-01", "h-07", "h-12", "h-03", "h-18"],
    "ab_test_picks": ["h-01", "h-07", "h-12"],
    "subheadline": "...",
    "cta_primary": "...",
    "cta_secondary": "...",
    "variants": [{"id": "hero-A", "approach": "authority | problem_agitate | ...", "subheadline": "...", "hypothesis": "..."}]
  },
  "cta_variants": [{"id": "cta-A", "text": "...", "hypothesis": "..."}],
  "mechanism_copy": "...",
  "benefits": [{"title": "...", "body": "...", "voc_refs": ["..."]}],
  "social_proof": {"testimonials": [...], "proof_stack": [...]},
  "offer_stack": "...",
  "guarantee_copy": "...",
  "faq": [{"q": "...", "a": "..."}],
  "urgency": "...",
  "email_hooks": ["..."],
  "voc_compliance": { "total_checked": 20, "literal_hits": 14, "paraphrased": 5, "missing": 1 },
  "voc_forced_continue": false,
  "claims_unverified": false,
  "decision_modalities_covered": ["spontaneous", "competitive", "humanistic", "methodical"],
  "specimen_primary": "agora-11-blocos",
  "specimen_secondary": null,
  "specimen_block_map": [
    {"n": 1, "bloco": "saudacao qualificada", "trabalho": "pre-qualifica o leitor pelo estado emocional", "conteudo_origem": "voc_top20 #3 + persona da 02"}
  ],
  "markup_audit": {
    "four_us": {"urgent": true, "useful": true, "unique": false, "ultra_specific": true},
    "ideal_prospect": true,
    "big_promise": true,
    "first_page_test": true,
    "four_emotions": {"new_only": true, "safe_predictable": false, "easy_anybody": true, "big_fast": true},
    "makepeace_4": {"grab_eyeballs": true, "expand_hl": true, "cred": true, "bribe": true},
    "defects_found": ["too vague (secao Benefits, corrigido)"],
    "verdict": "pass | rewrite_lead"
  }
}
```

> `specimen_primary`/`specimen_block_map` vêm da ETAPA 2.5 e `markup_audit` do sweep 9. A skill 11 (ad-analysis) usa os dois pra diagnosticar: quando uma página converte mal, a primeira pergunta é se o espécime escolhido era o certo pro avatar, e a segunda é qual camada do audit já tinha reprovado antes do launch.

`lead_type` é o campo **top-level** decidido na ETAPA 2 — contrato com a 07a (que o lê pra confirmar `page_type`). `voc_forced_continue` e `claims_unverified` são os flags do pré-flight (só `true` quando o membro escolheu prosseguir com VOC insuficiente / sem research foundation).

**A 07a (pré-flight/PLAN) e a 07b (populate/GEO) leem diretamente este JSON** — se inválido, a fase STOREFRONT não prossegue.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de salvar, garanta o diretório:** `mkdir -p workspace/[produto]/06-copy-engine/`.

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `06-copy-engine/copy-engine.md` → `06-copy-engine/copy-engine.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

Atualizar `manifest.json`: adicionar `06-copy-engine` em `skills_completed`, atualizar `updated_at`. Em seguida, regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug`; atualiza ABRIR-AQUI.html).

`workspace/[produto]/06-copy-engine/copy-engine.md` contendo (seções canônicas acima):
1. Strategy brief (Etapa 2 — tipo de página, lead, hero, ângulo, tom, framework, modalities mapping)
2. 20-30 headlines geradas + top 5 + 3 pra teste A/B
3. Página completa seção por seção (Etapa 4 ou 5)
4. Revisão após 7 sweeps (mudanças documentadas, incluindo VOC compliance %)
5. Variações pra teste (Etapa 7)

Também salvar `workspace/[produto]/06-copy-engine/dados.json` no schema acima.

## Mensagem Final

"Copy completa pro [tipo de página]. Big Idea: [big idea]. Mecanismo aplicado: [nome]. VOC integrado, objeções quebradas, 3 variações de headline pra teste. [Se houver warnings residuais de compliance: N warnings — revise se quiser.]

Próximo passo: diga **'page'** pro design da página (skill 07a — você escolhe a rota de design e aprova o HTML navegável, com essa copy dentro, ANTES de qualquer código existir); depois **'build page'** pra compilar e subir no Shopify (07b), **'tracking'** (07c) e **'checkout'** (07d). Com a loja pronta, armamos a infraestrutura de launch — **'bônus'** (05 Fase A, se a oferta tem bônus) e **'retention'** (13 Fase A: flows de recuperação, abandoned cart + post-purchase) — e só então os criativos. Não adianta criar ads pra uma página que ainda não existe."
