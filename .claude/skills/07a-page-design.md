---
name: page-design
description: Primeira skill da fase STOREFRONT. Planeja a página (page_type por awareness, menu de sections, hero_type, strategy block completo no page-plan.json), mapeia os ASSETS DE IMAGEM por section (inventário do que o membro tem + rota AI foto-real-primeiro pra lifestyle; placeholder só EXPLÍCITO com plano registrado), roda brand signals (lê brand.md primeiro e só pergunta o que faltar; cascade Refero → screenshot→visão → design-clone opcional → manual/presets de .claude/lib/design-presets/, todos convergindo pra design-signals.json) e apresenta ao MEMBRO um MENU DE ROTAS DE DESIGN (clone-and-adapt, Claude Design handoff, AIDesigner MCP opcional, frontend-design fallback, AI site-builders externos se o membro usa) pra ele escolher — todas convergindo pra design/page.html, a PÁGINA INTEIRA aprovada com a copy real de 06 inserida, os signals aplicados e as imagens reais nos slots. Antes do checkpoint roda SELF-REVIEW VISUAL obrigatório (screenshot desktop+mobile lido por visão, auto-correção). O membro aprova esse HTML ANTES de qualquer Liquid existir — ele é a FONTE ÚNICA DE VERDADE visual. Gera design-tokens.json. Use quando o membro disser "page", "página", "design da página", logo após ter copy pronta. Depois rode 07b-page-build pra compilar e deployar.
---

# 07a — Page Design (PLAN + BRAND SIGNALS + MENU DE ROTAS DE DESIGN)

Primeira das duas skills da fase **STOREFRONT** (07a → 07b). Esta skill decide a estratégia da página, define os signals visuais e gera o design como **HTML navegável aprovado pelo membro**. O Liquid só nasce na 07b, deterministicamente, a partir do HTML que você aprovar aqui.

Princípio reitor: **HTML-first → fonte única de verdade visual → aprovação humana ANTES do código.** Nada de "gerar Liquid e torcer pra renderizar igual". O membro vê a página real, navegável, com a copy dele dentro, e só depois ela vira Shopify.

Decisão de design: a 07a NÃO escolhe sozinha COMO o design nasce. Ela **apresenta ao membro um menu de rotas** (clone-and-adapt, Claude Design handoff, AIDesigner MCP, frontend-design fallback, AI site-builders externos quando o membro já usa um) e ele escolhe. Causa raiz de página genérica/"horrível" = gerar do zero sem referência concreta. Por isso clone-and-adapt (partir de um layout de concorrente que já converte) é o padrão recomendado, e gerar do zero (frontend-design) é o fallback. Todas as rotas convergem pro MESMO `design/page.html`.

> **Índice completo dos frameworks desta skill (domínio page-landing-cro):** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, mapa skill→domínio no README). Sempre que esta skill mandar "consulte a base", isso significa: **puxe os SISTEMAS NOMEADOS da base — rode `search_knowledge` com a `best_query` de cada framework relevante PRA AQUELA ETAPA, com `deep=true`.** NUNCA use query genérica. Os frameworks de maior impacto já vêm embutidos nas ETAPAs abaixo com sua query exata; o resto do domínio (33 frameworks) está no índice.

**O que esta skill faz:**

1. Pré-flight + PLAN — detecta produto, lê copy/offer/research, escolhe `page_type` pelo awareness, monta o plano de sections, escolhe `hero_type`, persiste o bloco `strategy` completo em `page-plan.json` + eyebrows criativos.
2. ASSETS DE IMAGEM — inventário do que o membro tem (fotos de fornecedor/próprias/UGC), mapa de necessidade de mídia POR SECTION (o `hero_type` amarra o requisito do hero), rota de geração AI pra lifestyle (doutrina foto-real-primeiro da skill 08 — NUNCA gerar rótulo/embalagem por texto). Tudo registrado em `sections_plan[].media`.
3. BRAND SIGNALS — lê `workspace/[produto]/brand.md` PRIMEIRO (só pergunta o que faltar), depois cascade (Refero MCP → screenshot→visão → design-clone opcional pra hex exato → manual/presets de `.claude/lib/design-presets/presets.json`), tudo convergindo pro mesmo `design-signals.json`.
4. MENU DE ROTAS DE DESIGN — apresenta as rotas viáveis (detectadas em runtime), o membro escolhe; a rota gera a PÁGINA INTEIRA em `design/page.html` com a copy real inserida, os signals aplicados e as imagens reais nos slots. SELF-REVIEW VISUAL obrigatório (Playwright + visão) antes do checkpoint; member aprova. Gera `design-tokens.json`.
5. Dual output dos relatórios (.md + .html, logo SVG) + framing de draft + atualiza manifest.

**Outputs gravados em `workspace/[produto]/07-page/`:**
- `page-plan.json` — plano machine-readable + bloco `strategy` completo + mapa de mídia por section (consumido pela 07b e pela skill 09)
- `design-system.md` + `design-system.html` — design system humanizado
- `design/page.html` — **a página inteira aprovada (FONTE ÚNICA DE VERDADE visual)**
- `design/assets/` — imagens reais da página (inventário/geração da ETAPA 1.6)
- `design-tokens.json` — tokens consolidados da variação escolhida (consumido pela 07b)
- `design-signals.json` — signals de marca (heading_font, body_font, palette role-tagged, radius, shadow, density)

Depois desta skill, rode **07b-page-build** pra compilar o HTML aprovado em Liquid + deployar.

---

## Pré-flight

1. Leia `workspace/profile.md` — em especial `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno desta skill (`page-plan.json` reasoning, `design-system.md`/`.html`, conversa com o membro) usa esse idioma. **A copy consumidor-final (headlines, eyebrows, hero, bullets, CTAs) inserida no `design/page.html` permanece SEMPRE em inglês US**, independente do `report_language` — copy pública nunca traduz.
2. Valide os inputs (todos sob `workspace/[produto]/`):
   - [ ] `manifest.json` existe e tem `06-copy-engine` em `skills_completed`
   - [ ] `06-copy-engine/dados.json` + `06-copy-engine/copy-engine.md` existem e parseiam (se o `.md` novo não existir, use o legado `relatorio.md` — mesmo fallback vale pras outras fases)
   - [ ] `04-offer-builder/dados.json` + `04-offer-builder/offer-builder.md` existem (preço, stack, garantia, mecanismo nomeado)
   - [ ] `02-market-research/dados.json`/`market-research.md` existe (awareness, sophistication, ceticismo, VOC) — usado pra detectar `page_type`
   - [ ] `03-competitor-analysis/competitor-analysis.md` existe (opcional, mas alimenta gaps/diferenciação)
   - [ ] Dir de output: `workspace/[produto]/07-page/` (criar com `mkdir -p` se não existir)

**Se algum input obrigatório faltar** (regra `emergency-escape-paths` ES1) — não aborte seco. Ofereça:
- **(A)** Rodar a skill faltante agora (06/04/02), OU
- **(B)** Prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` + `risk_acknowledged: true` e avisando no output final que recomenda re-executar com o arquivo real.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes, ofereça rodar o setup (skill 00) inline.

---

## ETAPA 0 — Detecção e leitura

### 0.1 Pesquisa exploratória na base Aura

Puxe os SISTEMAS NOMEADOS da base (não query genérica) — rode `search_knowledge(deep=true)` com a `best_query` de cada framework de fundação de página. Os de maior impacto pra dominar conversão + estrutura ANTES de planejar:

- **15 Factors of Funnel Structure** (rode `15 factors of funnel structure diagnostic social proof time for results`) — diagnóstico de PDP/LP.
- **Empathy-Trust-Offer (3 Pillars of Landing Pages)** (rode `landing pages that convert empathy trust offer three pillars`).
- **NESP Framework (New, Easy, Safe, Big Promise)** (rode `NESP framework new easy safe big promise offer landing page`).
- **10x Page Plan** (rode `10x page plan framework web pages sections hero proof bar switch close`).
- **4 Decision Making Modalities** (rode `4 decision making modalities spontaneous competitive humanistic methodical web copy`) — toda página serve Spontaneous + Competitive + Humanistic + Methodical ao mesmo tempo.
- **Hero Sections (5 Types + Selection)** (rode `hero sections 5 types value prop dreamstate problem segment campaign selection`) — usado de novo na 1.3.
- **Congruence Principle (Ad-to-Page Message Match / Scent)** (rode `congruence principle message match ad to landing page scent Kennedy consistency rule`).
- **Specificity → Landing Page Conversion** (rode `specificity landing page conversion Hopkins Caples PVA VAKOG mental movies`) — Hopkins/Caples proof stacking + mental movies.
- **CTAs / Calls to Value** (rode `CTAs buttons friction anxiety calls to value lizard brain first person mirror headline`).

Aprofunde até ter domínio de conversão + estrutura de página. Schwartz awareness e Bond sophistication entram na 1.1; advertorial e checkout/AOV têm seus frameworks próprios nas ETAPAs onde são usados (1.1 / referência cruzada à 07d). Domínio completo (33 frameworks) em `.claude/lib/kb-index/`.

### 0.2 Detectar o produto

1. Se o membro mencionou o produto explicitamente, use o slug exato.
2. Senão, liste as subpastas de `workspace/`:
   - 1 produto → use ele, confirmando: "Vou gerar o design da página pro produto X. Confirma?"
   - múltiplos → lista numerada, membro escolhe
   - nenhum → "Não encontrei produtos no workspace. Rode `setup` ou `product research` primeiro, ou cole a copy aqui."
3. Salve o slug em `PRODUTO`. Daqui pra frente, todo `[produto]` = esse slug.

### 0.3 Ler inputs obrigatórios

Leia, sob `workspace/[produto]/`: `06-copy-engine/copy-engine.md` + `06-copy-engine/dados.json` (OBRIGATÓRIO), `04-offer-builder/offer-builder.md`/`dados.json` (preço, stack, garantia, **mecanismo nomeado LITERAL**), `02-market-research/market-research.md`/`dados.json` (awareness, sophistication, ceticismo, VOC), `03-competitor-analysis/competitor-analysis.md` (gaps, claims saturados a evitar). Leia `workspace/profile.md` (estilo de marca, stage).

---

## ETAPA 1 — PLAN (estratégia + plano de sections)

A página NÃO tem estrutura fixa. Cada produto merece um plano que reflita sua estratégia. A skill 06 já tomou essas decisões — respeite-as.

### 1.1 Detectar `page_type` — PRIMARIAMENTE pelo awareness (Schwartz)

O `page_type` é decidido pelo **awareness level** lido de `02-market-research/dados.json` (campo `dominant_awareness`) e confirmado pelo campo **top-level `lead_type`** de `06-copy-engine/dados.json` (a 06 grava esse campo na ETAPA 2 dela — é o contrato machine-readable entre as duas skills). Confirmação: lead `story`/`big_idea`/`problem_agitation` casa com `advertorial`; `mechanism`/`secret`/`proclamation` casa com `landing`; `offer`/`direct` casa com `pdp_robust`/`pdp_lean`. Se `lead_type` estiver ausente (dados.json de produto legado), siga só pelo awareness e anote a lacuna. Heurística sintática é só **tie-break**. Se `dominant_awareness_secondary` presente no dados.json da 02 (empate ±5pp), trate a página como híbrida: grave `hybrid: true` no bloco strategy do `page-plan.json` e escolha o page_type que serve os dois níveis (na dúvida, o do nível de menor awareness — página que educa converte os dois; página que assume conhecimento perde o menos consciente).

| Awareness (Schwartz) | page_type | Lógica | Estrutura típica |
|---|---|---|---|
| **Problem-Aware** (ou Unaware aquecido pra problem) | `advertorial` | Mercado sente a dor mas não conhece a solução — precisa de narrativa editorial que educa antes de vender | hook → problem → agitation → mechanism → proof → soft CTA → FAQ (7-section blueprint, listicle) |
| **Solution-Aware** | `landing` | Conhece o tipo de solução, não a sua marca — precisa de persuasão NESP focada em diferenciação | hero benefit + CTA → proof → mechanism → offer → guarantee → faq → cta-final |
| **Product-Aware** | `pdp_robust` | Conhece seu produto, compara — precisa de PDP completa que vence objeções e ancora valor | hero → benefits → mechanism → social-proof → comparison → offer → guarantee → faq → cta-final |
| **Most-Aware** | `pdp_lean` | Só precisa do empurrão final (preço/oferta/urgência) | hero curto → offer → proof condensada → guarantee → cta-final |

**Tie-break sintático** (só se awareness ambíguo entre dois níveis): copy abre com narrativa "I used to..." / "Doctor reveals..." e sem CTA no topo → puxa pra `advertorial`; copy abre com pricing tiers/bundles explícitos no topo → puxa pra `landing`/`pdp`. Hybrid (narrativa abrindo + offer stack convergindo nos últimos 40%) é válido — marque `page_type` como o dominante e anote `hybrid: true` no strategy.

**Se `page_type = advertorial` — defina o DESTINO do soft CTA (obrigatório):** advertorial é pré-lander, não fecha a venda sozinho; o soft CTA precisa apontar pra uma página que fecha. Pergunte ao membro e registre a escolha em `page-plan.json.destination_ref`:
- **(a) Rodar a cadeia 07a→07b uma SEGUNDA vez** pra gerar a página de fechamento (`pdp_lean` com a oferta da 04) — recomendado quando não existe PDP trabalhada;
- **(b) PDP existente da loja** — só se a copy/oferta dela já foram trabalhadas (apontar pra PDP default do tema quebra a congruência exigida na 3.7);
- **(c) Checkout direto** com a oferta da 04 (produto simples, membro quer funil curto).

A 07b usa `destination_ref` pra linkar o soft CTA. Sem destino definido, o advertorial vai ao ar mandando tráfego pago pra uma página sem copy nem oferta — NÃO pule esta decisão.

**Se `page_type = advertorial` — mapa canônico copy→sections (estrutura Zakaria):** a skill 06 grava a copy do advertorial com 7 seções canônicas de heading fixo. O `sections_plan` de um advertorial NÃO usa o menu genérico da 1.2 cru — a espinha é este mapa 1:1 (não improvise ids; a 07b splita por eles):

| Seção canônica da copy (06) | `sections_plan[].id` | Papel na página |
|---|---|---|
| `## Advertorial Headline` | `hero` | headline editorial + dek — **sem CTA no topo** (é editorial, não landing) |
| `## Lead` | `lead` | abertura da história (relato em primeira pessoa / cena que fisga) |
| `## Background Story` | `background-story` | contexto do protagonista, a luta antes da descoberta |
| `## Root Cause` | `root-cause` | a causa raiz do problema que ninguém contou pro leitor |
| `## Mechanism Reveal` | `mechanism-reveal` | a virada: o mecanismo que ataca a causa raiz |
| `## Product Build-Up` | `product-buildup` | do mecanismo ao produto — prova, credibilidade, especificidade |
| `## Reveal + Close` | `reveal-close` | revelação do produto + **soft CTA apontando pro `destination_ref`** |

Sections opcionais podem entrar DEPOIS da espinha (ex: `social-proof` se a copy tem depoimentos, `faq` se há objeções mapeadas) — nunca no meio da narrativa, que quebra o ritmo editorial. Se alguma das 7 seções não existir no `copy-engine.md` do produto, PARE e avise o membro: o advertorial da 06 está incompleto — rode a 06 de novo antes de desenhar a página (não invente a seção faltante).

**Frameworks que sustentam essa decisão** (puxe os nomeados, não query genérica):
- **Schwartz awareness levels** (rode `product market awareness Schwartz levels`) + **Bond sophistication stages** (rode `market sophistication stages`) — confirme que o awareness lido de `02` casa com o lead type de `06`.
- Se `page_type = advertorial`: **Advertorial / Editorial-Look Principle** (rode `advertorial editorial look principle 5x readership Halbert Kennedy native ad`) + **Listicle Advertorials (2 Types)** (rode `listicle advertorial product-focused education-focused types awareness bridge`) pra escolher product-focused vs education-focused, e **PCPO body copy** (rode `PCPO problem cure proof offer body copy framework web page`) pra estruturar o corpo editorial (Problem → Cure → Proof → Offer).
- Se `page_type = landing`: **NESP** (já puxado na 0.1) dirige a diferenciação Solution-Aware.
- Se `page_type = pdp_robust/pdp_lean`: **AOV Builders** (rode `checkout optimization AOV order bump upsell gift with purchase bundle threshold money close`) informam a ancoragem de oferta — note que a execução de bump/upsell vive na 07d, aqui só dimensiona a section de oferta.

Confirme o `page_type` detectado com o membro antes de prosseguir (1 frase + a lógica).

### 1.2 Escolher as sections a partir do MENU

Não force "9 sections padrão". Escolha o que a estratégia pede.

**Core (90% das páginas):** `hero` · `offer` · `faq` · `cta-final`

**Estrutura (escolha pela estratégia):**
- `trust-bar` — quando tem 3+ selos de autoridade (media, certificação, rating)
- `benefits` — sempre que a copy tem bullets VOC-loaded (quase sempre); peso maior em Stage 4-5 de sophistication
- `mechanism` — **SÓ se o produto tem mecanismo único** (ingrediente patenteado, processo proprietário, inovação). Commodity → PULE (mecanismo forçado parece falso)
- `social-proof` — essencial em alto ceticismo (skincare, saúde, wellness); pular em impulse barato
- `guarantee` — proporcional ao risco percebido (caro/duradouro = section grande; impulse = uma linha)
- `comparison-table` — quando o produto é disrupter numa categoria madura
- `before-after` — cosmético / estético / transformação visual
- `how-it-works` — produtos com 3+ passos de uso
- `ingredients` — skincare / supplements / food
- `specs` — bloco de especificações objetivas (materiais/ingredientes com dosagem, dimensões/peso, quantidade por unidade, certificações, modo de uso). Recomendado em TODA pdp: agentes de compra AI (ChatGPT/Perplexity shopping) decidem lendo specs e dados estruturados, não copy sensorial — sem esse bloco a página fica invisível pra esse tráfego. A copy vem da seção de specs da 06 (fatos verificáveis, sem adjetivos); a skill 07e (agentic-readiness) audita depois, junto da camada GEO/Schema.org que a 07b injeta
- `founder-story` — DTC com narrativa de origem forte
- `video-demo` — produto que precisa ver em ação
- `sustainability` — claim ambiental relevante
- `gift-guide` — sazonais / presenteáveis
- `app-embed` — reviews apps (Okendo, Judge.me), subscription widgets

**Exemplos de planos diferentes:**
> Nootropic premium ($89, Stage 4, alto ceticismo, ingrediente patenteado, Product-Aware): hero → trust-bar → mechanism → benefits → ingredients → social-proof → founder-story → offer → guarantee → faq → cta-final
> Camiseta básica ($25, Stage 2, baixo ceticismo, sem mecanismo, Most-Aware): hero → benefits → offer → social-proof → faq → cta-final

### 1.3 Escolher o `hero_type` dos 5 canônicos

Puxe o framework nomeado: **Hero Sections (5 Types + Selection)** (rode `hero sections 5 types value prop dreamstate problem segment campaign selection`) pra ter os 5 tipos canônicos (value-prop, dreamstate, problem, segment, campaign) e os critérios de seleção. Cruze com **StoryBrand 5 Website Essentials** (rode `StoryBrand five website essentials above the fold offer CTA images of success`) e valide a clareza do topo com o **Grunt Test** (rode `StoryBrand grunt test 5 second clarity hero section three questions`) — o herói tem que passar nos 3 segundos. Escolha 1 hero baseado no `page_type`, awareness, e na natureza do produto (transformação visual vs commodity vs categoria nova). Registre o `hero_type` no strategy block — a 07b e o `frontend-design` usam isso pra dar a direção do hero. Pra advertorial, o "hero" tende a ser editorial (headline + dek + abertura de história); pra landing/pdp, benefit-forward com CTA e proof acima da dobra.

### 1.4 Decidir blocks por section

Pra cada section do plano, decida: monolítica (só settings) ou com blocks; quais blocks universais (eyebrow, heading, paragraph, button_row, etc — ver Catálogo na 07b) e quais type-specific (benefit_card, pricing_tier, review_card, faq_item...). Isso vira `sections_plan[].blocks` no `page-plan.json`. Não precisa detalhar settings aqui (a 07b deriva do HTML) — basta listar os block types que cada section vai ter.

### 1.5 Mostrar o plano ao membro

> "Pro seu produto [X] (awareness [Y] → page_type [Z]), o plano é:
> 1. hero ([hero_type]) — headline + CTA + proof acima da dobra
> 2. mechanism — porque tem [mecanismo real], section importante
> ...
> Seções que NÃO vou incluir: before-after (produto ingestível, não visual), comparison-table (sem concorrente direto).
> Algum ajuste antes de eu desenhar?"

Aguarde confirmação ou ajuste. Só então siga.

### REGRA CRÍTICA — Eyebrows criativos, não rótulos de framework

"Mechanism", "Offer Stack", "Guarantee", "Social Proof", "FAQ" são LABELS INTERNOS do framework de copy (nomes de pasta). **Nunca** aparecem literal na página — soa template genérico. No eyebrow de cada section (quando tiver), use uma tag CRIATIVA e específica do produto.

| Framework (interno) | Eyebrow RUIM (literal) | Eyebrow BOM (criativo, produto-específico) |
|---|---|---|
| Mechanism | "The Mechanism" | "The Science", "Why [Produto] Works", "Inside the Formula", "The [Ingrediente]® Difference" |
| Offer / Stack | "Offer Stack" | "Choose Your Kit", "Build Your Stack", "Pick Your Glow", "Start Here" |
| Guarantee | "Guarantee" | "The Promise", "Zero Risk", "Glow or Get Back", "60 Days, No Excuses" |
| Benefits | "Benefits" | "Why [Produto]", "Five Things Change", "The Difference" |
| Social Proof | "Social Proof" | "Real Results", "Why They Switched", "500+ Stories" |
| FAQ | "FAQ" | "You Asked", "Before You Buy", "The Real Questions" |
| CTA Final | "CTA Final" | "One Last Thing", "Ready?", "Your Glow Starts Here" |

Regras pra eyebrows: 2-5 palavras, específico do produto ("The pH Difference" > "The Science"), **em inglês** (copy pública), nunca rotule o framework, pode pular (trust-bar/hero/cta-final podem não precisar). Se o copy tem um Big Idea, USE ("It's Not the Fragrance. It's the pH." — sem travessão: rule 8a vale pra eyebrow também). Esses eyebrows vão pro `page-plan.json` (`sections_plan[].eyebrow`) e são inseridos no HTML na ETAPA 3.

### 1.6 — Assets de imagem (inventário + mapa de mídia por section)

Página de conversão sem imagem real é wireframe, não página. Causa recorrente de "design aprovado bonito, página no ar feia": o HTML foi aprovado com caixas cinza/stock genérico e ninguém planejou de onde as imagens REAIS viriam. Esta sub-etapa fecha esse furo ANTES do design nascer.

**1. Inventário do que o membro TEM.** Pergunte em uma mensagem só: fotos do fornecedor (AliExpress/Alibaba — packshots, rótulo, embalagem)? Fotos próprias do produto? UGC/lifestyle (cliente usando, contexto real)? Logos/selos (certificações, mídia)? Peça os arquivos/paths e salve os utilizáveis em `workspace/[produto]/07-page/design/assets/` (nomeie por uso: `hero-lifestyle.jpg`, `packshot-front.png`).

**2. Mapa de necessidade POR SECTION.** Pra cada section do `sections_plan`, decida o que ela precisa de mídia — e registre no campo `media` (schema na 4.1). O `hero_type` amarra o requisito do hero:

| `hero_type` | Imagem que o hero exige |
|---|---|
| value-prop | packshot limpo do produto (fundo neutro) ou produto em contexto |
| dreamstate | lifestyle do RESULTADO (pessoa no estado desejado, produto presente) |
| problem | cena da dor/frustração (sem o produto como herói) |
| segment | pessoa reconhecível do avatar usando/segurando o produto |
| campaign | key visual da campanha (produto + elemento da Big Idea) |

Demais sections: `before-after` exige pares reais; `social-proof` pede rostos/fotos de review quando existirem; `mechanism`/`ingredients` aceitam diagrama/close do ingrediente; `benefits`/`faq`/`guarantee` normalmente vivem de ícone SVG (`media.required: false`).

**3. Rota de geração AI (só pra LIFESTYLE, com a doutrina foto-real-primeiro da skill 08).** Quando falta imagem lifestyle/contexto, gere por AI — mas SEMPRE ancorado na foto REAL do produto (composição image-to-image com o packshot real como referência). **NUNCA gere rótulo/embalagem por prompt de texto puro** — o modelo alucina texto e embalagem, e página com rótulo inventado destrói confiança (e é a mesma regra da 08 pra vídeo). Packshot não se gera do zero: vem do fornecedor ou de foto própria; se o membro não tem NENHUMA foto real do produto, isso é bloqueio de inventário (peça a foto — é pré-requisito de qualquer rota).

**4. Gate de aprovação (vale pro checkpoint da ETAPA 3).** O `design/page.html` só é apresentado/aprovado com as imagens REAIS nos slots — OU com placeholder **EXPLÍCITO** (bloco visivelmente marcado, ex: caixa cinza com o texto "PLACEHOLDER: hero lifestyle") + plano de obtenção registrado em `sections_plan[].media.acquisition_plan` no `page-plan.json`. Placeholder implícito é PROIBIDO: stock aleatório que parece final, `{{IMAGE}}` invisível, imagem do concorrente esquecida no slot. A 07b bloqueia o deploy de qualquer section com imagem vazia/placeholder — resolver aqui é mais barato.

---

## ETAPA 2 — BRAND SIGNALS (cascade unificada → `design-signals.json`)

Isto NÃO é a fonte do layout. É só extração de signals (paleta, tipografia, vibe) que vão alimentar QUALQUER rota de design escolhida na ETAPA 3 (clone-and-adapt aplica esses signals sobre o esqueleto de layout do concorrente; frontend-design e AIDesigner geram com eles; no handoff do canvas eles dirigem o membro). O layout em si vem da rota escolhida na ETAPA 3 — aqui só sai a direção de cor/tipografia/densidade.

Os 4 caminhos convergem TODOS pro MESMO arquivo `workspace/[produto]/07-page/design-signals.json`:

```json
{
  "source": "refero | screenshot_vision | design_clone | manual",
  "source_detail": "Linear (via Refero) | print da loja X | hex extraído de competitor.com | preset Atelier Document",
  "heading_font": "'Fraunces', Georgia, serif",
  "body_font": "'Inter', -apple-system, sans-serif",
  "palette": {
    "background": "#FDFAF4",
    "surface": "#F5EDE0",
    "foreground": "#231F20",
    "primary": "#D85C4A",
    "accent": "#9CAF88",
    "muted": "#B0A99F",
    "border": "#E3DAC9"
  },
  "radius": { "base_px": 12, "pill_px": 1000 },
  "shadow": "subtle | medium | strong",
  "density": "airy | medium | compact"
}
```

Antes de começar, **leia `workspace/[produto]/brand.md` PRIMEIRO** — as skills 00 (ETAPA 5A) e 01 (etapa SALVAR) criam esse arquivo e prometem ao membro literalmente que "a 07a lê esse arquivo na brand discovery e só pergunta o que faltar". O que já estiver preenchido lá (posicionamento, arquétipo/tom, paleta com hex reais, tipografia, do/don'ts) entra DIRETO como brand discovery — não pergunte de novo o que o arquivo já responde (hex reais do brand.md alimentam a paleta dos signals sem cascade). Depois, pergunte em UMA mensagem SÓ o que estiver ausente ou marcado `[preencher]` (estilo visual desejado: minimalist editorial / bold modern / clinical premium / wellness organic / custom; cores da marca se houver, ou "escolhe pra mim"; tem site de referência cujo visual ele curte?). Se `brand.md` não existir, faça a brand discovery mínima completa nessa mesma mensagem única. Use as respostas pra dirigir a cascade.

### Caminho 1 — Refero MCP (preferencial, catálogo curado)

Detecta tools com prefixo `mcp__refero__` na sessão. Se disponíveis, vibe search no catálogo de ~200 design systems premium (Cursor, Linear, Vercel, Notion, Stripe, etc.).

1. Construa a query a partir da brand discovery (ex: "editorial magazine ultralight italic premium" / "modern SaaS clean tech minimal"). Se o membro nomeou um site específico, pule direto pro `refero_get`.
2. `mcp__refero__refero_search(query=<query>, limit=5)` — ou `mcp__refero__refero_get(hostname="<site>.com")` quando nomeou um site.
3. Apresente 2-3 candidatos (nome + 1 frase do `northStar`). Membro escolhe (ou pede mais 3 com search refinada).
4. `chosen = mcp__refero__refero_get(uuid=<id>)` → extrair `chosen.designSystem` (typography + colors role-tagged + spacing + radius). Mapeie pro shape de `design-signals.json`.

Se Refero retorna zero resultados úteis OU o membro não gostou de nenhum, caia pro Caminho 2.

### Caminho 2 — SCREENSHOT → VISÃO (fallback PRIMÁRIO)

Substitui o scraping de computed-styles do design-clone como fallback principal. Imune a Cloudflare, JS pesado, markup bagunçado — exatamente o que faz o scraping travar.

1. Peça ao membro um **print full-page** da loja de referência (qualquer concorrente, mesmo nichado fora do catálogo Refero). OU, se o membro deu uma URL e prefere automatizar, a Aura captura **1 screenshot** via `webapp-testing`/Playwright — SÓ o screenshot, sem extrair DOM:
   ```
   # via skill webapp-testing — navegar à URL, full-page screenshot, salvar em /tmp/ref-[produto].png
   ```
2. **Leia a imagem com visão nativa** (Read tool no PNG, ou o screenshot capturado). Extraia da imagem:
   - Paleta dominante (background, foreground, primary/accent, surfaces) — nomeie em hex aproximado
   - Tipografia (serif vs sans no heading; peso; vibe — editorial / técnica / geométrica)
   - Radius (cantos retos vs arredondados vs pill), profundidade de shadow, densidade (airy vs compact)
3. Preencha `design-signals.json` com `source: "screenshot_vision"`.

> Hex extraído de imagem é aproximado — está OK. São signals de direção, não pixel-exato. O `frontend-design` ajusta pra garantir contraste WCAG e hierarquia.

### Caminho 3 (opcional) — design-clone para hex exato

Só pra quem QUER hex exato de um concorrente nichado e tem o venv do design-clone instalado (skill 00). Não é o fallback primário (screenshot→visão é). Se o membro pedir, use o caminho canônico — o wrapper orquestra downloader → analyzer → pattern-extractor e a cascade de captura sozinho (não chame os scripts soltos):

```bash
python3 tools/design-clone/aura_clone.py "URL" --output=/tmp/ref-[produto] --skip-images
```

Leia o bloco `design_system` de `/tmp/ref-[produto]/patterns.json` e **cheque o campo `design_system_source`**: se `"extracted"`, mapeie pro shape do `design-signals.json` com `source: "design_clone"`; se `"defaults_fallback"` (o site não rendeu CSS computado real), **IGNORE o bloco e caia pro próximo caminho** — nada de paleta inventada. Se o modo signals abortar com "engine não extrai computed-styles" (a captura veio do single-file-cli, que não gera computed-styles), ou se Playwright não estiver instalado, pule graciosamente pro Caminho 2 (screenshot→visão) ou pro Caminho 4.

### Caminho 4 — Manual / 8 presets (último recurso)

Quando Refero não tem match E o membro não tem print/URL:
- Peça descrição livre da vibe ("editorial sério, low-pressure, italic em keywords"), OU
- Ofereça os 8 presets (Modern Clean, Bold Editorial, Premium Minimal, Warm Lifestyle, Tech Sharp, Atelier Document, Apothecary Calm, Luxe Magazine) — membro escolhe um, e os tokens saem **LITERAIS de `.claude/lib/design-presets/presets.json`** (paleta role-tagged, heading/body font, radius, shadow, density — completos e fixos por preset; o `vibe`/`use_when` de cada entrada ajuda a recomendar). Leia o arquivo e copie os campos pro `design-signals.json` com `source: "manual"`, `source_detail: "preset [Nome]"`. **NUNCA invente/ajuste tokens de preset em runtime** — preset é promessa de consistência (mesmo nome = mesmos tokens em qualquer run). Se o membro pedir ajuste, aplique e registre como `"preset [Nome] (customizado)"`.

Se o membro passou nomes de cor por extenso (ex: "sage green"), valide via regex de hex `^#([0-9A-Fa-f]{3,8})$` ou converta por nome (sage green `#9CAF88`, dusty rose `#D4A5A5`, off-white `#FDFAF4`, navy `#14213D`, terracotta `#C66B3D`, olive `#6B7040`, etc). Se a cor não for reconhecível, peça o hex.

### Prova de paletas na página real (quando há 2-4 candidatas)

Paleta não se escolhe por swatch (a amostra de cor isolada). Quando a cascade deixou mais de uma candidata viva, ou o membro pediu comparação, gere uma página comparadora self-contained: a MESMA página (ou as 2-3 seções mais representativas: hero, oferta e uma seção escura) renderizada em CADA paleta candidata, com navegação por abas ou âncoras, pro membro decidir VENDO a cor aplicada no contexto real.

A implementação usa o sistema de tokens por snippet: todo valor de cor entra como trio R,G,B (ex: `--tk-bg: 240,240,238` pra um fundo areia, `--tk-ink: 34,34,36` pra um grafite) e é consumido como `rgb(var(--tk-bg))` ou `rgba(var(--tk-bg), .5)`. Trocar a paleta inteira significa trocar 1 bloco de tokens, e o formato em trio dá transparência (alpha) sem duplicar a paleta. A paleta vencedora vira o `design-signals.json`/`design-tokens.json` normalmente.

**Dois temas, duas paletas:** quando o membro mantém 2 ou mais temas com paletas diferentes (teste A/B de identidade visual), o snippet de tokens é POR-TEMA — as sections são as mesmas, muda só o snippet de paleta de cada tema. A disciplina de push por-tema está na rule `shopify-theme-safety.md`: nunca pushar snippet de paleta em lote genérico (um push amplo leva a paleta de um tema pro outro sem ninguém perceber), conferir o tema alvo antes de cada push, e `--allow-live` exige atenção redobrada porque o tema publicado é a loja no ar.

### Output da ETAPA 2

Salve `design-signals.json` e mostre ao membro um resumo curto:
> "Peguei a vibe [da Linear via Refero / do print da loja X via visão / do estilo Atelier Document]:
> - Fontes: **[heading_font]** (títulos) + **[body_font]** (corpo)
> - Paleta: fundo **[background]** · texto **[foreground]** · accent **[primary]**
> - Radius **[radius]px** · shadow **[shadow]** · density **[density]**
> Vou usar isso como direção visual. O layout e a estrutura vêm da sua copy — só a paleta/tipografia é inspirada."

---

## ETAPA 3 — ESCOLHA DA FONTE DE DESIGN (o membro escolhe a rota)

Aqui o design nasce. A causa raiz de página "horrível" é gerar do zero sem referência concreta: sai genérico. Por isso a 07a NÃO escolhe a rota por você. Ela **apresenta as opções e o MEMBRO escolhe.** Todas as rotas convergem pro MESMO arquivo: `workspace/[produto]/07-page/design/page.html` — a **FONTE ÚNICA DE VERDADE visual**, aprovada pelo membro antes de qualquer Liquid existir. O resto da skill (tokens, plan, 07b) segue idêntico, independente da rota escolhida.

### 3.1 Detectar rotas viáveis (runtime)

Antes de apresentar o menu, detecte o que está disponível NESTA sessão e só ofereça as rotas viáveis:

| Rota | Disponível quando |
|---|---|
| **1. Clone-and-adapt** | `tools/design-clone/` existe no repo (sempre presente no framework). O membro precisa ter uma URL de concorrente cuja página ele ache boa (ou um .html da página salvo com a extensão SingleFile — ver degrau 4 da cascade na §3.3). |
| **2. Claude Design (handoff)** | Sempre ofertável — depende só do membro ter acesso ao canvas do `claude.ai/design` (Claude Pro/Max). Não há tool a detectar; é um handoff manual de arquivo. |
| **3. AIDesigner MCP** | Há tools com prefixo `mcp__aidesigner__` na sessão. Se ausente, NÃO liste como rota ativa — mencione em 1 linha "rota paga opcional, conecte o MCP se quiser" e siga. |
| **4. frontend-design (fallback)** | Sempre disponível (skill nativa). É a rota de menor qualidade — só quando o membro não tem referência nem quer desenhar. |
| **5. AI site-builders (v0 / Lovable / Manus)** | Rota EXTERNA — só entra no menu se o membro mencionar que usa algum deles (não ofereça espontaneamente). O membro descreve a página num desses geradores, eles criam o HTML. Ponto de atenção: trazem **runtime próprio** (stack/hospedagem deles), não Liquid nativo do Shopify — então serve como landing externa OU o membro exporta o HTML e a 07b reintegra ao tema. |

> Refero (`mcp__refero__`), se presente, já foi usado na ETAPA 2 pra brand signals — NÃO é uma rota de design de página aqui, é fonte de signals que alimenta qualquer rota.

### 3.2 Apresentar o menu ao membro (no `report_language`)

Mostre esta tabela (traduzida pro idioma do membro, listando só as rotas viáveis da 3.1):

| Rota | Como funciona | Qualidade de design | Custo | Automação | Quando usar |
|---|---|---|---|---|---|
| **1. Clone-and-adapt** *(padrão recomendado p/ velocidade)* | Você indica 1 PDP/landing de concorrente que acha bonita. A Aura captura só a **estrutura/layout** dela e adapta com a SUA copy (06), oferta (04) e imagens. Herda hierarquia e fluxo de conversão já validados no mercado. | Alta — parte de um layout que já converte | Zero | Alta | Você viu uma página de concorrente que funciona e quer velocidade sem reinventar layout |
| **2. Claude Design (handoff)** | Você desenha/itera a página no canvas visual do `claude.ai/design`, exporta como HTML standalone, e cola o arquivo aqui. A Aura consome esse HTML como `page.html`. | Alta — controle visual fino, aprovação no canvas | Incluso no Claude Pro/Max (consome mais token, mesmo limite) | Média (design semi-manual no canvas — isso é feature: você aprova visualmente antes do Liquid) | Você quer controle visual total e gosta de iterar num canvas |
| **3. AIDesigner MCP** *(se conectado)* | Roda dentro do Claude Code injetando padrões de design premium; cospe HTML/CSS limpo direto como `page.html`. | Alta | ~$20/mês (MCP pago) | Alta | Você já tem o MCP e quer design premium automatizado sem sair do Claude Code |
| **4. frontend-design** *(fallback)* | Gera a página via skill nativa, **com direção forte** (brand-signals da ETAPA 2 + referência concreta + estilo nomeado). | A mais baixa do menu — única gerada do zero, sem referência | Zero | Total | Você NÃO tem página de referência nem quer desenhar no canvas. É o fallback. |
| **5. AI site-builders (v0 / Lovable / Manus)** *(rota externa — só aparece se você usa um deles)* | Você descreve a página num desses geradores, ele cria o HTML, e você cola aqui como `page.html`. Eles trazem **runtime próprio** (não é Liquid nativo do Shopify) — então serve como landing externa OU a 07b exporta/reintegra ao tema. Consumida igual à rota 2 (você traz o HTML; a Aura injeta os markers `data-aura-section` e segue pra 3.7). | Alta — geradores modernos | Free tier / pago conforme uso | Média (gera no app deles; você traz o HTML) | Você já usa v0/Lovable/Manus e prefere desenhar lá fora, ciente de que o runtime é deles |

Pergunte direto, sem decidir por ele:
> "Qual rota você prefere pro design da página? A **1 (clone-and-adapt)** é a mais rápida e costuma sair melhor, porque parte de um layout de concorrente que já converte — você só me indica uma página que acha boa. Mas escolhe a que fizer sentido pra você."

Auto-sugira a rota 1 como **default** (não imposição) por velocidade e qualidade, mas respeite a escolha do membro. Se o membro estiver em stage starter (member-stage-awareness) e sem referência em mente, explique a rota 4 sem empurrar custo.

Depois da escolha, vá pra sub-etapa correspondente (rota 1 → 3.3 · rota 2 → 3.4 · rota 3 → 3.5 · rota 4 → 3.6 · rota 5 → 3.6b). **Toda rota termina gerando `design/page.html` + indo pra 3.7 (regras de qualidade comuns) + checkpoint de aprovação.** Crie o dir com `mkdir -p workspace/[produto]/07-page/design`.

> **Ajustes rápidos no admin (Sidekick) — pós-launch:** depois que a página estiver no ar (pós-07b), o membro pode usar o **Sidekick** (a IA dentro do admin do Shopify) pra microajustes pontuais — trocar uma imagem, ajustar um texto, mexer numa cor — sem voltar pro Claude Code. Não substitui a 07a/07b (que constroem a página inteira com a copy real e fazem o deploy versionado e seguro): é só pro retoque rápido depois. Mencione isso ao membro só se for útil no contexto, não como rota de design.

> **Prontidão pra IA de busca (GEO):** independente da rota escolhida aqui, a 07b adiciona a camada GEO/Schema.org (`product-schema.json` + `agent-facts.html`) pra a página ser entendida e citada quando alguém pesquisa o produto no ChatGPT, Claude ou Perplexity (search/shopping). A rota desta etapa é só decisão **visual** — a prontidão pra IA de busca é garantida no build (07b), não depende da rota.

---

### 3.3 Rota 1 — Clone-and-adapt

O membro indica 1 URL de concorrente. A Aura captura a **ESTRUTURA** dessa página (ordem de sections, hierarquia, layout) e a usa como **ponto de partida**, trocando TODO o conteúdo pelo do membro.

> **REGRA LEGAL E ÉTICA (inegociável):** capturar estrutura/layout e trocar 100% do conteúdo (copy, imagens, marca, paleta) é defensável. Copiar 1:1 não é. **NÃO** reaproveite copy, imagens, logos, nome de marca ou claims do concorrente — só o esqueleto de layout como direção. A copy vem SEMPRE de `06-copy-engine/dados.json`, a oferta de `04-offer-builder/dados.json`, a paleta/tipografia dos `design-signals` da ETAPA 2.

1. Peça a URL: *"Me passa a URL da página de concorrente que você acha boa. Vou pegar só o esqueleto de layout dela (não a copy nem as imagens) e montar a SUA versão por cima."*
2. Capture a estrutura via o subcomando `clone-and-adapt` do `aura_clone.py` (orquestra downloader → analyzer → skeleton-builder numa chamada):
   ```bash
   python3 tools/design-clone/aura_clone.py clone-and-adapt "URL" --output=/tmp/clone-[produto] --product=[produto]
   ```
   Ele emite `skeleton.html` (sections só com estrutura/placeholder, ordem+tipo+layout do concorrente, ZERO copy/imagem/marca) + `skeleton.json`. Esse esqueleto é o que você preenche com a copy de `06` e a oferta de `04`. (Os scripts `downloader.py`/`analyzer.py` rodam por baixo — não os chame soltos; o `analyzer.py` sozinho não gera o skeleton.) Exit codes do wrapper: `0` sucesso · `1` input inválido · `2` pipeline incompleto (ver manifest/stderr).

   **Cascade de captura (degraus 1-2 são AUTOMÁTICOS dentro do wrapper; 3-4 são a degradação):**

   - **Degrau 1 — `downloader.py` (Playwright stealth):** roda primeiro, é o único que extrai DOM com fidelidade máxima.
   - **Degrau 2 — `snapshot.py` (single-file-cli), automático:** se o DOM falhar, o `--engine=auto` (default) já cai sozinho pro motor SingleFile — não precisa invocar nada. Requer Node >= 20; se ausente, o wrapper pula esse degrau e segue a degradação.
   - **Degrau 3 — screenshot→visão (ES1-style):** se nenhuma engine pegou DOM, o wrapper grava `raw/fallback-screenshot.png` e marca `"mode": "screenshot_fallback"` + `"skeleton": null` no manifest. Leia o PNG por visão nativa (Read) pra derivar a estrutura. **EXCEÇÃO — challenge detectado:** se `raw/fallback.json` marcar `challenge_detected: true`, o screenshot é o interstitial do Cloudflare ("Just a moment…"/Turnstile) — NÃO leia por visão (derivaria estrutura de uma tela de bloqueio); vá DIRETO pro degrau 4.
   - **Degrau 4 — MANUAL via extensão SingleFile (vence Cloudflare/login, 1 clique):** peça ao membro, com instrução mastigada:
     > "Instala a extensão **SingleFile** no Chrome (https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle), abre a página do concorrente normalmente no SEU Chrome (logado, sem tela de bloqueio), clica no ícone da extensão — ela salva a página inteira num único arquivo .html em Downloads. Me manda o caminho do arquivo (ou arrasta ele pro chat)."

     Ingira o arquivo com o mesmo pipeline (não precisa de browser nem de Node):
     ```bash
     python3 tools/design-clone/aura_clone.py clone-and-adapt --from-file=<arquivo.html> --output=/tmp/clone-[produto]
     ```
     O browser real do membro é imune a anti-bot — esse degrau resolve o que os automáticos não conseguem. O .html salvo é material de trabalho (referência de concorrente): vive em `/tmp`/workspace, JAMAIS é commitado (rule 11).
3. **Reconcilie com o plano da ETAPA 1.** O esqueleto do concorrente é referência de layout, mas a verdade estratégica é o seu `sections_plan` (que veio do awareness/sophistication do SEU produto). Onde o concorrente tem sections que o seu plano não pede (ex: gift-guide irrelevante), descarte. Onde o seu plano pede sections que o concorrente não tem (ex: `mechanism` porque você tem mecanismo único real), adicione. O layout do concorrente informa hierarquia e ritmo; o conteúdo e a seleção de sections são seus.
4. **Gere `design/page.html`** aplicando: a estrutura reconciliada, a copy REAL de `06`, a oferta de `04`, os `design-signals` da ETAPA 2 (paleta/tipografia/radius/density) e as **imagens do mapa de mídia da 1.6** (`design/assets/` — jamais as imagens do concorrente). Uma única variação fiel ao layout-base é suficiente aqui (o membro já escolheu a referência); ofereça iterar se quiser ajustar densidade/paleta.

**Variante — clone fiel seção a seção (página inteira como sections editáveis):** quando o membro tem o snapshot completo da página de referência (o arquivo .html salvo com a extensão SingleFile — degrau 4 da cascade) e quer a ESTRUTURA INTEIRA reproduzida como sections OS 2.0 (o formato de tema do Shopify em que cada section é editável no theme editor), não só o esqueleto, o trabalho segue 4 passos:

1. **Serializar o DOM por seção**, com estilos computados em desktop E mobile + screenshot de cada seção. O par geometria+imagem é o contrato de fidelidade: os estilos computados dão as medidas exatas, o screenshot mostra como a seção deve ficar — a conversão só está certa quando os dois batem.
2. **Converter seção a seção** — trabalho paralelizável (1 agente por seção). Cada seção vira uma section Liquid com schema completo: todo texto vira setting, toda imagem vira `image_picker`, listas repetíveis viram blocks, e o preset carrega valores de exemplo genéricos ("Your headline here", "[garantia]"). As classes CSS de cada section levam o prefixo `sec` (de section), ex: `.sec-hero-title`, pra o estilo de uma section nunca vazar pra outra.
3. **Montar o template** a partir dos presets das sections e popular com o conteúdo real.
4. **Verificar end-to-end:** renderização desktop+mobile comparada com os screenshots do passo 1, e comércio real funcionando (variantes, add-to-cart, cupom).

A MESMA regra legal e ética acima vale integralmente nesta variante: estrutura/layout sim; copy, imagens, marca e paleta do concorrente NUNCA — o clone nasce com o conteúdo do PRÓPRIO membro injetado (copy de `06`, oferta de `04`, imagens da 1.6, paleta dos signals da ETAPA 2). Os padrões de seção endurecidos (marquee/faixa rolante, sticky add-to-cart, gradiente, badges, drawer, fonte universal) vivem em `.claude/lib/shopify-section-patterns/` — consulte antes de reinventar qualquer um deles.

### 3.4 Rota 2 — Claude Design (handoff)

O membro desenha a página no canvas visual e entrega o HTML pronto.

1. Instrua exatamente:
   > "Abre o `claude.ai/design`, desenha/itera a página lá no canvas. Quando estiver boa, exporta com **'Export as standalone HTML'** (ou 'Download .zip' / 'Handoff to Claude Code'). Depois cola o HTML aqui, ou me dá o caminho do arquivo/zip que você baixou."
2. Pra dirigir o trabalho dele no canvas, forneça antes: o `section_order` + `sections_plan` da ETAPA 1, os eyebrows criativos, a copy de `06` por section, e os `design-signals` da ETAPA 2 — pra ele não desenhar no escuro.
3. Quando o membro colar/apontar o arquivo, leia-o (Read no path, ou descompacte o .zip), rode a **normalização da §3.6c** (Tailwind→CSS plano, remoção de JS de runtime, validação self-contained), confira que a copy real está dentro (não placeholder do canvas), e salve como `design/page.html`.
   > **NOTA:** o `/design-sync` / DesignSync é só pra design-**SYSTEM** (componentes isolados), NÃO pra puxar página inteira. O caminho de página é sempre o export HTML / handoff manual descrito aqui.

### 3.5 Rota 3 — AIDesigner MCP (se `mcp__aidesigner__` presente)

Só ofereça se as tools `mcp__aidesigner__*` existirem na sessão.

1. Construa o input do MCP a partir do `sections_plan` + copy de `06` + `design-signals` da ETAPA 2 (não desenhe do zero — alimente o MCP com a estrutura e o conteúdo reais).
2. Invoque a(s) tool(s) `mcp__aidesigner__*` disponíveis (descubra em runtime quais existem; não assuma nomes hard-coded) pra gerar a página premium.
3. Salve o HTML/CSS limpo retornado como `design/page.html`.
4. Se o MCP falhar ou retornar vazio, ofereça cair pra rota 1 (clone-and-adapt) ou rota 4 (fallback) — não aborte (emergency-escape-paths).

### 3.6 Rota 4 — frontend-design (fallback, qualidade menor)

Use quando o membro não tem referência (sem URL de concorrente, sem canvas). Deixe explícito que é o fallback e a qualidade é a mais baixa do menu (única rota gerada do zero, sem referência).

**Invoque a skill `frontend-design` UMA vez** pra gerar a **PÁGINA INTEIRA** como HTML+CSS self-contained (vanilla, não Tailwind) — mas **NUNCA de tela em branco.** Sempre com direção forte:

- **(a)** os `design-signals` da ETAPA 2 (paleta role-tagged, heading/body fonts, radius, shadow, density).
- **(b)** uma **referência concreta**: peça ao membro um screenshot de inspiração (qualquer página cujo visual ele curta) e leia-o com visão nativa (Read no PNG) pra extrair direção. Se ele não tiver nenhum, use um dos 8 presets da ETAPA 2 como âncora visual nomeada.
- **(c)** **direção de design explícita**: estilo nomeado (ex: "minimalist editorial"), do/don't, e um anti-genérico (o que NÃO fazer pra não sair "cara de template AI").

Demais inputs idênticos às outras rotas: a copy REAL de `06` já inserida (nada de lorem ipsum), as imagens do mapa de mídia da 1.6 (`design/assets/`), a estrutura do `sections_plan` + `section_order` da ETAPA 1, `page_type` e `hero_type` respeitados. Gere **2-3 variações da PÁGINA INTEIRA** (não 4 só do hero) — tratamentos visuais diferentes do mesmo layout/sections (tipografia editorial vs utilitária, paleta warm vs cool, densidade alta vs respiro, hierarquia de proof diferente) num único HTML navegável com tabs/anchors pra alternar A / B / C. Salve em `design/page.html`.

### 3.6b Rota 5 — AI site-builders (externa; consumo igual à rota 2)

Só quando o membro mencionou que usa v0/Lovable/Manus. O design acontece no app externo; o lado da Aura é fornecer o material e consumir o HTML:

1. Forneça ao membro o mesmo pacote da rota 2: `section_order` + `sections_plan` da ETAPA 1, eyebrows criativos, copy de `06` por section, e os `design-signals` da ETAPA 2 — pra ele não descrever a página no escuro.
2. Quando ele trouxer o HTML exportado, leia o arquivo e rode a **normalização da §3.6c** (obrigatória aqui — v0/Lovable/Manus exportam Tailwind + JS de framework): utilities inlined em CSS plano, JS de runtime removido, self-contained validado. Confira que a copy real de `06` está dentro (não placeholder do gerador), injete os markers `data-aura-section` e salve como `design/page.html`.
3. Lembre o membro do runtime: se o destino for o tema Shopify, a 07b compila esse HTML em Liquid normalmente; se ele preferir hospedar no runtime do gerador (landing externa), o deploy sai do fluxo 07b e o tracking (07c) precisa ser configurado lá.
4. Registre `design_route: "site-builder"` no `page-plan.json` e siga pra 3.7.

### 3.6c Normalização de HTML externo (rotas 2 e 5 — procedimento real, não "normalize" vago)

HTML de canvas/site-builders vem com Tailwind (classes utilitárias + CDN/build) e JS de framework (React/Vue hydration). O `design/page.html` precisa ser **HTML+CSS plano e self-contained** — é o contrato que o SPLIT/COMPILE da 07b assume. Procedimento:

1. **Tailwind/utilities → CSS plano via render computado.** Renderize o HTML original no Playwright (`file://` ou server local, com o CSS do Tailwind ainda ativo). Pra cada elemento estrutural (sections, headings, parágrafos, botões, cards, grids), leia os **computed styles** (`getComputedStyle`) e materialize as propriedades relevantes (display/grid/flex, spacing, tipografia, cor, radius, shadow, breakpoints via re-render em 390px e 1440px) em **classes semânticas próprias** (`.hero`, `.hero-title`, `.tier-card`...) num `<style>` único no `<head>`. Troque as classes utilitárias pelas semânticas no markup e remova o `<script src="...tailwind...">`/`<link>` do framework CSS. (Página pequena com poucas utilities? Traduzir manualmente as classes usadas é aceitável — mesmo resultado.)
2. **JS de runtime → fora.** Remova bundles/hydration de framework (`<script>` de React/Next/Vue, chunks). O HTML final é estático; interações (accordion/tabs/FAQ) são reimplementadas com `<details><summary>`/CSS puro — mesma regra que a 07b aplica no compile.
3. **Assets → locais ou estáveis.** Baixe as imagens referenciadas pra `design/assets/` e reescreva os `src` (self-contained de verdade), ou mantenha URL absoluta só se for CDN estável do próprio membro. Nunca deixe `src` apontando pro sandbox temporário do gerador (expira e a página aprova com imagem que vai sumir).
4. **Validação de self-contained (obrigatória):** abra o HTML normalizado no Playwright com requests externos bloqueados (exceto Google Fonts) e confirme por screenshot que renderiza igual ao original nos dois breakpoints; console sem erros; `grep -c '<script'` no arquivo = 0 (zero JS de runtime).
5. Injete os markers `data-aura-section` e siga pra 3.7.

---

### 3.7 Regras de qualidade COMUNS (toda rota)

Independente da rota, `design/page.html` precisa passar nas mesmas ground rules antes do checkpoint:

- **Marcação de sections:** cada section marcada com `<section data-aura-section="hero">`, `data-aura-section="benefits">`, etc (um por section do plano, usando os mesmos ids de `sections_plan[].id`) — isso permite o SPLIT determinístico na 07b sem ambiguidade. Se a rota não gerou esses markers (ex: HTML do canvas na rota 2), você os injeta antes de salvar.
- **Ícones SVG inline** (Lucide/Heroicons/Phosphor), NUNCA emojis na UI da página (rule 7).
- **Copy ad-safe:** minimizar travessão (rule 8a, zero em headlines); zero ad-flag words na copy pública (rule 8b — Botox/Filler/Injection/Cure/Medical-grade/Anti-aging/etc reformulados).
- **Tipografia/layout:** type scale modular (1.25 ou 1.333); fluid type `clamp()` em headings; spacing generoso (padding-block 5-8rem em hero/oferta); WCAG AA contraste; focus-visible; `prefers-reduced-motion`; touch targets ≥44px; responsivo real, mobile-first.
- **Performance (budget de página):** imagens comprimidas (WebP/AVIF quando possível) e `loading="lazy"` abaixo da dobra; a imagem do hero SEM lazy (é o LCP) e COM `width`/`height` explícitos (zero layout shift); ZERO JavaScript de runtime (interação = `<details>`/CSS). Proxy simples: HTML+CSS ≤ ~150KB, página total com imagens ≤ ~1.5MB — o alvo real é LCP mobile < 2.5s. A 07b re-valida isso como gate (GATE 3) antes do deploy; estourar aqui = retrabalho lá.
- **Imagens do mapa de mídia (ETAPA 1.6):** toda section com `media.required` tem a imagem REAL no slot, ou placeholder EXPLÍCITO (visivelmente marcado) com `acquisition_plan` registrado no `page-plan.json`. Nunca stock aleatório fingindo ser final, nunca `src` de sandbox de gerador, nunca imagem/foto do concorrente (rota 1).
- **CTAs como call-to-VALUE** ("Start My 30-Day Glow", não "Buy Now"). Fundamente em **CTAs / Calls to Value** (rode `CTAs buttons friction anxiety calls to value lizard brain first person mirror headline`) e decida direto vs stepping-stone com **Direct vs Transitional CTA** (rode `direct vs transitional CTA Miller buy now download guide stepping stone`).
- **Serve as 4 modalities ao mesmo tempo** — antes do checkpoint, confira que o `page.html` atende **4 Decision Making Modalities** (rode `4 decision making modalities spontaneous competitive humanistic methodical web copy`): Spontaneous (CTA rápido acima da dobra), Competitive (comparison/diferenciação), Humanistic (prova social, rostos, histórias), Methodical (specs, garantia, FAQ). Falta de uma = furo de conversão.
- **Congruência ad→page:** o topo da página tem que ecoar a promessa do ad que traz o tráfego — valide com **Congruence Principle** (rode `congruence principle message match ad to landing page scent Kennedy consistency rule`).
- **Tratamento por page_type:** advertorial → editorial (dek, drop caps, ritmo de leitura); landing/pdp → benefit-forward com proof acima da dobra. Em advertorial, aplique os **Ogilvy 14 Readability Devices** (rode `Ogilvy 14 readability devices drop caps captions subheads reverse type`) e a **Double Readership Path** (rode `Kennedy double readership path skimmers analytical readers subheads PS`) pra servir skimmers e leitores analíticos.

Se a rota entregou HTML que viola alguma dessas (comum no handoff do canvas e em clone-and-adapt), **corrija inline** antes de salvar — não devolva ao membro pra ele consertar.

### Self-review visual (OBRIGATÓRIO antes do checkpoint — o membro nunca vê defeito óbvio)

Ler o HTML como texto NÃO é ver a página. Antes de apresentar QUALQUER draft ao membro, você olha a página renderizada com os próprios olhos:

1. **Renderize** `design/page.html` no Playwright via `file://` (skill `webapp-testing`) e capture screenshot **full-page** em DUAS larguras: desktop (1440px) e mobile (390px).
2. **LEIA os dois screenshots por visão** e caçe defeitos: hierarquia frouxa (headline que não domina a dobra), contraste insuficiente na prática (texto sobre imagem/surface), spacing quebrado (sections coladas ou buracos gigantes), imagem estourada/distorcida/com overflow, texto cortado ou colidindo em mobile, CTA invisível, placeholder implícito parecendo final, tipografia que caiu pra fallback (serif genérica onde devia ter a heading font).
3. **Auto-corrija inline** o que encontrar (post-task-self-audit: silent fix) e re-screenshote. Repita até os dois screenshots passarem.
4. Só então apresente o draft ao membro no checkpoint abaixo. Nas rotas com iteração (todas), repita este self-review a cada versão nova (`page-v2.html`...) antes de devolver ao membro.

### Checkpoint de aprovação (iteration-driven-refinement)

Apresente como **draft navegável**, não como "pronto". Adapte a pergunta à rota:
> "Página montada (rota [escolhida]). Abre `design/page.html` no browser e me diz o que ajustar. Pergunta granular: o tom tá certo (mais editorial ou mais direto)? O hero puxa atenção? A hierarquia de proof convence? [Se rota 4: qual das variações A/B/C, ou um mix tipo 'A no hero, C na proof'?] Itero até você dizer 'tá bom'."

**Este HTML é a FONTE ÚNICA DE VERDADE visual.** O membro aprova AQUI, antes de qualquer Liquid existir. Não avance pra 07b sem aprovação. E não declare aprovado com slot de imagem pendente: cada section com `media.required` tem a imagem REAL, ou o placeholder EXPLÍCITO da ETAPA 1.6 com `acquisition_plan` registrado no `page-plan.json` (avise o membro que a 07b bloqueia o deploy enquanto o placeholder existir).

- Cada iteração salva versão nova (`design/page-v2.html`, `-v3`), não sobrescreve. Log em `workspace/[produto]/07-page/iterations-log.json`.
- Max 3 iterações sem progresso → escalate. Na rota 4, peça referência descritiva em vez de draft-reativo; nas rotas 1/2/3/5, ofereça trocar de rota (ex: "clone-and-adapt não está saindo bom — quer desenhar no canvas (rota 2) ou me dar outra referência?"; na rota 5, iterar exige voltar ao gerador externo — se o loop ficar caro, ofereça migrar pra rota 1 ou 2).
- Quando o membro aprova, consolide como `design/page.html` (versão canônica). Na rota 4, isso significa promover a variação escolhida (ou o mix) ao arquivo final; nas demais rotas, é o HTML aprovado da própria rota. Diga: "Salvando como `design/page.html` — fonte única de verdade. A 07b vai compilar exatamente isso em Liquid."

### Gerar `design-tokens.json` (programaticamente)

Do `design/page.html` aprovado, consolide os tokens **programaticamente** (não "extraídos do HTML por reasoning"). A 07b consome isto pra mapear cada token → CSS var + setting. `variant_chosen` registra a variação na rota 4 (A/B/C ou mix); nas rotas 1/2/3/5, use o nome da rota (ex: `"clone-and-adapt"`, `"claude-design"`, `"aidesigner"`, `"site-builder"`):

```json
{
  "produto": "[slug]",
  "variant_chosen": "A",
  "colors": {
    "background": "#FDFAF4", "surface": "#F5EDE0", "foreground": "#231F20",
    "primary": "#D85C4A", "on_primary": "#FFFFFF", "accent": "#9CAF88",
    "muted": "#B0A99F", "border": "#E3DAC9"
  },
  "type": {
    "heading_font": "'Fraunces', Georgia, serif",
    "body_font": "'Inter', -apple-system, sans-serif",
    "scale_ratio": 1.25,
    "h1": "clamp(2.5rem, 5vw, 4rem)",
    "h2": "clamp(1.75rem, 3vw, 2.5rem)",
    "body": "1.0625rem"
  },
  "spacing": { "base": 8, "scale": [4, 8, 12, 16, 24, 32, 48, 64, 96] },
  "radii": { "sm": 6, "md": 12, "lg": 20, "pill": 1000 },
  "shadow": { "intensity": "subtle", "color": "#231F20" },
  "components_by_section": {
    "hero": ["eyebrow", "heading", "paragraph", "button_row", "stats_bar", "tag"],
    "offer": ["eyebrow", "heading", "pricing_tier", "countdown_banner"]
  },
  "generated_at": "2026-...Z"
}
```

`spacing.base` é 4 ou 8 (base-4/8). `components_by_section` lista, por section, os block types que a 07b vai criar — cruza com `sections_plan` do `page-plan.json`.

---

## ETAPA 4 — Persistir `page-plan.json` + relatórios + manifest

### 4.1 `page-plan.json` (com bloco `strategy` COMPLETO)

```json
{
  "produto": "[slug]",
  "page_type": "advertorial | landing | pdp_robust | pdp_lean",
  "strategy": {
    "awareness_level": "Problem-Aware | Solution-Aware | Product-Aware | Most-Aware",
    "sophistication_stage": 4,
    "skepticism": "baixo | médio | alto",
    "product_type": "commodity | nova categoria | disrupter | incremental",
    "has_unique_mechanism": true,
    "mechanism_name": "[LITERAL do 04-offer-builder/dados.json — nome exato do mecanismo nomeado]",
    "hero_type": "[1 dos 5 canônicos da base]",
    "decision_modalities_served": ["spontaneous", "competitive", "humanistic", "methodical"],
    "page_type": "advertorial | landing | pdp_robust | pdp_lean",
    "hybrid": false
  },
  "sections_plan": [
    {"id": "hero", "eyebrow": "[eyebrow criativo ou null]", "blocks": ["eyebrow","heading","paragraph","button_row","stats_bar","tag"],
     "media": {"required": true, "kind": "lifestyle", "source": "ai_lifestyle", "status": "ready", "asset": "design/assets/hero-lifestyle.jpg", "acquisition_plan": null}},
    {"id": "mechanism", "eyebrow": "The pH Difference", "blocks": ["eyebrow","heading","paragraph","mechanism_card"],
     "media": {"required": false, "kind": "icon_svg", "source": "none", "status": "ready", "asset": null, "acquisition_plan": null}}
  ],
  "section_order": ["hero","mechanism","benefits","social-proof","offer","guarantee","faq","cta-final"],
  "brand_discovery": {
    "style": "minimalist-editorial",
    "brand_colors": ["#...","#..."],
    "signals_source": "refero | screenshot_vision | design_clone | manual",
    "reference": "Linear | print loja X | hex de competitor.com | preset Atelier Document"
  },
  "design_route": "clone-and-adapt | claude-design | aidesigner | frontend-design | site-builder",
  "design_route_ref": "URL do concorrente (clone-and-adapt) | path do export (claude-design/site-builder) | null",
  "destination_ref": "SÓ quando page_type=advertorial: destino do soft CTA — handle/URL da pdp_lean gerada numa 2ª passada da cadeia, PDP existente trabalhada, ou checkout direto. null nos demais page_types",
  "design_signals_ref": "design-signals.json",
  "design_tokens_ref": "design-tokens.json",
  "design_html_ref": "design/page.html",
  "design_system_ref": "design-system.md",
  "generated_at": "2026-...Z"
}
```

> `mechanism_name` é o nome **LITERAL** de `04-offer-builder/dados.json` — não invente, não parafraseie. A skill 09 (consistency audit) compara esse campo cross-fase; drift aqui falha o gate.
> `page_type` aparece tanto no top-level quanto dentro de `strategy` (downstream lê de ambos) — mantenha idênticos.
> **Campo `media` (ETAPA 1.6) é obrigatório em toda entry de `sections_plan`**: `required` (bool), `kind` (`lifestyle | packshot | before_after_pair | review_faces | diagram | icon_svg | none`), `source` (`member_photo | supplier_photo | ugc | ai_lifestyle | none`), `status` (`ready | placeholder`), `asset` (path em `design/assets/` ou null), `acquisition_plan` (null quando `ready`; **obrigatório e específico** quando `placeholder` — ex: "foto lifestyle com modelo, membro fotografa até sexta"). A 07b bloqueia deploy enquanto houver `status: "placeholder"`.

### 4.2 Relatórios (dual output — rule 6b)

Salve `design-system.md` (paleta role-tagged, tipografia, spacing, radii, shadow, density, components por section — humanizado, no `report_language`) + o `.html` companion. O `.html` usa `.claude/templates/aura-report-template.html` (CSS inline, self-contained) e **abre com o bloco SVG da logo copiado LITERAL de `.claude/templates/aura-logo-snippet.html`** (rule 6b — NUNCA texto). Use componentes Aura (section-label, callout, note, kpi-grid, table-wrap). Responsivo mobile.

> Nota: `design/page.html` é a página do CONSUMIDOR (ícones SVG, sem emoji, sem logo Aura). Os relatórios internos (`design-system.html`) são documentos Aura (logo SVG Aura no topo, emojis OK). Não confunda os dois.

### 4.3 Manifest

Atualize `workspace/[produto]/manifest.json` adicionando `07a-page-design` ao array `skills_completed`. Registre `page_type` e `signals_source` no manifest se útil pra downstream.

- Regenera o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `workspace/[produto]/ABRIR-AQUI.html`).

---

## Mensagem final (framing de draft)

> "Design da página pronto e aprovado por você (rota [escolhida], salvo em `design/page.html` — fonte única de verdade). Plano + strategy em `page-plan.json`, tokens em `design-tokens.json`.
> Próximo passo: rode **07b-page-build** (ou diga 'build page' / 'deploy'). Ela vai compilar esse HTML exato em sections Liquid editáveis, popular o template e subir no Shopify. Como o Liquid é gerado deterministicamente do HTML que você aprovou, o que você vê no theme editor vai ser pixel-idêntico ao que aprovou aqui."

---

## Self-audit silencioso (rule post-task-self-audit)

Antes de declarar concluído, rode os 5 gates internos e corrija inline (sem mencionar): `mechanism_name` em `page-plan.json` bate LITERAL com `04-offer-builder/dados.json`; `page_type` é coerente com o awareness de `02` e com o `lead_type` de `06`; se `page_type=advertorial`, `destination_ref` está definido (não null) E o `sections_plan` segue o mapa canônico Zakaria da 1.1 (as 7 seções da copy de 06 mapeadas 1:1, nada inventado); eyebrows são criativos (não rótulos de framework); a copy inserida em `design/page.html` veio de `06` (não inventada); **todo `sections_plan[]` tem o campo `media` preenchido (ETAPA 1.6) — nenhum placeholder implícito, todo `status: "placeholder"` tem `acquisition_plan` específico, e nenhum lifestyle gerado por AI nasceu de prompt de texto puro com rótulo/embalagem em quadro**; **o self-review visual rodou (screenshots desktop 1440 + mobile 390 lidos por visão) e os defeitos achados foram corrigidos ANTES do checkpoint**; se o Caminho 4 foi usado, os tokens vieram LITERAIS de `.claude/lib/design-presets/presets.json` (não inventados); `design-tokens.json` e `design-signals.json` existem e parseiam; `section_order` e `sections_plan` consistentes entre si; `design_route` registrado no plan; nas rotas 2/5, a normalização da 3.6c rodou de verdade (zero `<script>` no `page.html`, CSS plano, assets locais/estáveis); markers `data-aura-section` presentes em todas as sections (qualquer rota, inclusive handoff do canvas e clone-and-adapt); regras de qualidade comuns da 3.7 passaram (SVG, ad-safe, contraste, performance budget); logo SVG presente nos `.html` internos. **Se a rota foi clone-and-adapt: confirme que NENHUMA copy, imagem, logo, claim ou nome de marca do concorrente vazou pra `design/page.html` — só o esqueleto de layout.** Surface só o que exige decisão do membro (ex: conflito de nome de mecanismo entre 02 e 04, ou rota escolhida que ficou inviável a meio caminho).

## Referências cruzadas

- **Próxima skill:** `07b-page-build` (compila `design/page.html` em Liquid + deploya)
- **Conversor canônico (usado pela 07b):** `tools/design-clone/liquid-converter.py` (Modo C)
- **Presets de design (Caminho 4):** `.claude/lib/design-presets/presets.json` (tokens completos e fixos dos 8 presets + README)
- **Doutrina de imagem AI (ETAPA 1.6):** skill `08-creative-engine` ETAPA 1.0 (foto-real-primeiro — produto/rótulo nunca nasce de prompt de texto)
- **Skill que audita o output:** `09-consistency-audit` (lê `page-plan.json` strategy + `design-tokens.json`)
