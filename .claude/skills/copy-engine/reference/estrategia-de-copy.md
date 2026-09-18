# Copy Engine · Referência: Estratégia de copy, o sistema decide (ETAPA 2)

> Os sistemas de seleção de estratégia com a `best_query` de cada um, a tabela lead por awareness e os sistemas que constroem cada lead, a nota de proveniência (Caples, Schwartz, Masterson), os hero patterns de ecom cruzados com os 5 tipos canônicos, o ângulo principal a partir do gap da `competitor-analysis` e do sub-avatar, o tom de voz, o framework de organização por tipo de página, as 4 Decision Making Modalities com os princípios de influência, o modelo do brief e o contrato do `lead_type`. Abra na ETAPA 2.

### ETAPA 2 — Estratégia de Copy (SISTEMA DECIDE)

Antes de decidir, puxe os SISTEMAS de seleção de estratégia (rode cada `best_query`):
- **Schwartz's Five Stages of Awareness** (rode `Schwartz five stages of awareness headline approach per stage Breakthrough Advertising`) — define a abordagem por awareness dominante
- **Schwartz's Three Lead Dimensions (Desire, Identification, Belief)** (rode `Schwartz lead desire identification belief dimension awareness lead selection`) — define QUAL lead casa com o avatar
- **Schwartz's Five Stages of Market Sophistication** (rode `Schwartz market sophistication five stages new mechanism virgin market skepticism Breakthrough Advertising`) — define se lidera com promessa, mecanismo, ou identificação conforme o estágio de saturação da Skill `competitor-analysis`
- **Big Idea (Paradoxical Question, Gum Name, Conspiracy Story)** (rode `Big Idea paradoxical question gum name conspiracy story marketing thesis`) — transforma o gap mais forte da Skill `competitor-analysis` no ângulo dominante
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
- Escolha o gap mais forte identificado na Skill `competitor-analysis` (angle que NENHUM concorrente está usando)
- Esse vira o **Big Idea** da página — o ângulo dominante que unifica headline, subheadline, e hook
- Cruze com `sub_avatars[]` da `market-research`: escolha o sub-avatar cujo `angle` casa com esse gap — **é com ELE que o lead fala** (Rule of One: one reader). Registre a escolha no brief abaixo

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

**Persistir a decisão de lead (contrato com a `page-design`):** o tipo de lead escolhido nesta etapa DEVE ser gravado no campo **top-level `lead_type`** do `copy-engine/dados.json` (ver Output Schema). A `page-design` lê esse campo pra confirmar o `page_type` da página — sem ele, a fase STOREFRONT decide no escuro.
