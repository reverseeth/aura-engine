---
name: page-engine
description: Engine de geração de páginas Shopify a partir da copy. Usa orquestração de specialists (frontend-design + designer-* skills) pra gerar sections premium, theme-agnostic, 100% editáveis via {% schema %}, validadas com shopify-liquid. Use quando o membro disser "page", "página", "build page", "shopify page", "gerar página", ou após gerar copy e quiser ver no tema.
---

# Page Engine

## Fluxo em uma tela (overview)

| # | Etapa | Output | Tempo típico |
|---|---|---|---|
| 0 | Pesquisa na base Aura + detectar produto + ler inputs + detectar tema | Variáveis `PRODUTO`, `THEME_PATH` | 2-3min |
| 1 | Plano de sections ADAPTATIVO à estratégia (não fixo) + eyebrows criativos | Lista de sections escolhidas do menu | 3-5min |
| 2 | Brand discovery em 1 mensagem (6 perguntas) + referência visual opcional | Estilo, cores, assets, theme path, handle | 1min (pergunta) |
| 2.1 | Se ref visual passada: `downloader.py` → `pattern-extractor.py` | `design_system` da ref (só paleta + fontes) | 2min |
| 3 | Orquestra 5 skills `designer-*` (color-system, typography, spacing, grid, tokens) | `/workspace/[produto]/06-design-system.md` | 3-5min |
| 4 | `frontend-design` gera 3 variantes de hero em paralelo + ASCII preview → membro escolhe | HTML/CSS de 1 hero | 3-5min |
| 5 | Converte hero pro padrão de **blocks inline no schema** + validação Liquid | `sections/page-[produto]-hero.liquid` | 2-3min |
| 6 | Mesmo padrão da 5 pras demais sections do plano | 1 `.liquid` por section | 3-5min cada |
| 7 | UX writing pass (`designer-ux-writing`) | Microcopy refinado em defaults | 2min |
| 8 | Self-critique com 4 skills (critique + Nielsen + WCAG + QA) — **não pule** | Issues resolvidos | 5min |
| 9 | Template JSON `templates/page.[produto].json` com blocks **pré-populados com copy real** | Template pronto | 2-3min |
| 10 | `shopify theme duplicate` → `pull` → `cp` → `push --nodelete` | Tema unpublished "[Produto] Preview (Aura)" | 2min |
| 10.5 | Report ao membro (links de preview + arquivos + settings + issues) | Mensagem final | 1min |
| 11 | Iteration loop — ajustes sem regenerar do zero | Ajustes aplicados | variável |

**Princípios gerais aplicados em todas as etapas:**
- ✅ Cada section é pasta no sidebar da Shopify com blocks atômicos inline dentro (nunca theme blocks em `/blocks/`)
- ✅ Pagina vem 100% pré-montada via `templates/page.[produto].json` (não só preset)
- ✅ Toda cor, tamanho, tipografia, spacing editável; cada bloco tem `custom_css` textarea escape hatch
- ✅ Safe install: sempre duplicar tema live, nunca tocar direto o ao vivo
- ✅ Validação obrigatória via `shopify-plugin:shopify-liquid` antes de todo save

## Quando Usar

Quando o membro tem copy pronta (idealmente em `/workspace/[produto]/05-copy.md` do copy-engine) e quer gerar uma página Shopify completa que seja:
- Visualmente premium
- Theme-agnostic (funciona em Dawn, Horizon, Impulse, Sense, Prestige, qualquer Shopify 2.0+)
- 100% editável via theme editor (todo elemento é uma `setting`)
- Self-contained (zero dependência do CSS do tema pai)
- Validada antes de salvar

A página vem ANTES dos criativos no fluxo do Aura Engine — não faz sentido criar ads pra uma página que ainda não existe.

## Antes de Começar

### 0. Pesquisa exploratória na base Aura

Consulte a base Aura extensivamente sobre: 15 fatores da estrutura de funil (framework que diagnostica PDPs e LPs), landing pages que convertem (Empathy/Trust/Offer, NESP framework), 10x page plan (framework completo), advertorials (propósito, listicles, 7-section blueprint), checkout optimization (frictionless, trust badges, bumps, savings display), profit optimization (pricing, bundles, AOV builders), hero sections (5 tipos e critérios de seleção), congruência ad→page (message match, visual match, promise match), 4 decision making modalities (Spontaneous/Competitive/Humanistic/Methodical — toda página deve servir os 4 simultaneamente), behavioral psychology (System 1 vs System 2, above-the-fold triggers), CTAs como call to VALUE, crossheads e estrutura visual, wireframing e validação de web copy, proof stacking (Hopkins specificity + social proof volume + authority markers), e qualquer framework adjacente que apareça. Aprofunde em cada sub-conceito até ter domínio completo de conversão + estrutura de página.

### 1. Detectar o produto

A skill precisa saber **qual produto** ela está construindo a página. Detecte assim:

1. **Se o membro mencionou o produto explicitamente** ("page para [nome-do-produto]", "build page for [slug]"), use o slug exato.
2. **Caso contrário, liste os produtos disponíveis** em `/workspace/` (cada subpasta é um produto):
   - Se tiver **apenas 1 produto** → use ele automaticamente, mas confirme: "Vou gerar a página pro produto X. Confirma?"
   - Se tiver **múltiplos produtos** → mostre lista numerada e peça pro membro escolher
   - Se não tiver **nenhum produto** → diga: "Não encontrei produtos no workspace. Rode primeiro a skill `setup` ou `product research` pra criar a estrutura, ou cole a copy diretamente aqui."
3. **Salve o slug do produto** numa variável `PRODUTO` que será usada em todos os paths daqui pra frente. Daqui em diante, sempre que ver `[produto]` na skill, substitua pelo slug detectado.

### 2. Ler inputs obrigatórios

1. **OBRIGATÓRIO**: Leia `/workspace/[produto]/05-copy.md`.
   - Se não existir, pergunte: "Não achei a copy desse produto. Quer rodar a skill `copy` primeiro pra gerar (recomendado), ou colar a copy direto no chat agora?"
2. Leia `/workspace/[produto]/04-offer.md` se existir (preço, stack, garantia — vai pra section de oferta).
3. Leia `/workspace/[produto]/02-market-research.md` se existir (pra entender awareness level e voz do cliente).
4. Leia `/workspace/profile.md` se existir.

### 3. Detectar o tema Shopify local

A skill precisa saber **onde o tema Shopify do membro está baixado**. Detecte assim:

1. **Cheque os locais padrão na ordem**:
   - `~/shopify-theme/` (default recomendado)
   - `~/shopify-theme/<nome-da-loja>/`
   - Diretório atual se ele tiver `sections/`, `templates/`, `config/`
   - Variável de ambiente `$SHOPIFY_THEME_PATH` se existir
2. **Verifique se a estrutura é válida** (precisa ter `sections/`, `blocks/`, `templates/`, `config/`).
3. **Se não encontrar**, peça ao membro o path:
   > "Não achei seu tema Shopify baixado. Onde ele está? Se ainda não baixou, rode em terminal real (não no `!`):
   > 
   > ```
   > mkdir -p ~/shopify-theme && cd ~/shopify-theme
   > shopify theme pull --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
   > ```
   > 
   > Depois me passa o caminho ou roda `page` de novo."
4. **Salve o path numa variável `THEME_PATH`** usada daqui pra frente.

## Princípios Inegociáveis

Estes princípios NÃO são negociáveis. Se algum for violado, a section deve ser refeita.

1. **Proibido o block `custom_liquid` NATIVO do Shopify** (o que a plataforma adiciona por default em certos temas e esconde HTML cru não-editável). Elementos visuais sempre são settings ou blocks customizados. **Exceção:** você PODE oferecer um block type customizado chamado `custom_liquid` com setting `type: "liquid"` (documentado no Catálogo de Blocks) — isso é escape hatch editável, não o antipattern Shopify nativo.
2. **Self-contained CSS**. Todo CSS vai dentro de `{% stylesheet %}` da própria section. Zero dependência de classes/variáveis do tema pai.
3. **Theme-agnostic**. Não use classes do tema pai (`.product-card`, `.btn-primary`, etc). Use namespacing próprio: `.page-[produto]-hero`, `.page-[produto]-feature`.
4. **Mobile-first**. Todo CSS começa pelo mobile e usa media queries pra escalar.
5. **Semantic HTML**. `<section>`, `<article>`, `<header>`, `<h1>-<h6>` na ordem correta, `<button>` pra ações, `<a>` pra navegação, `<picture>`/`<img>` com `alt`.
6. **WCAG 2.1 AA** (checklist detalhado na seção "Acessibilidade" abaixo). Quality standard universal — não restringe design, garante que qualquer design gerado seja usável por todo usuário.
7. **Validação obrigatória**. Cada arquivo passa pelo skill `shopify-plugin:shopify-liquid` (validate.mjs) antes de ser salvo. Se falhar, corrige e revalida (3 retries).
8. **Zero JS frameworks externos**. Sem React, Vue, jQuery, libraries de animação. Use JavaScript vanilla quando absolutamente necessário, dentro de `{% javascript %}`.
9. **Imagens via `image_picker` setting**, nunca hardcoded ou via `asset_url`. O membro sobe a foto pelo theme editor.
10. **Fluid type e spacing**. Use `clamp(min, preferred, max)` pra tipografia e padding em sections importantes.

## Mapping de Schema (regras de tradução)

Quando converter HTML/CSS pra Liquid section, siga estas regras de tradução de elementos pra settings:

| Elemento HTML / caso | Setting type | Notas |
|---|---|---|
| Texto curto sem formatação (label, button text, eyebrow) | `text` | |
| Texto com `<em>`, `<strong>`, `<br>` inline (headlines com emphasis) | `inline_richtext` | Preserva inline tags no browser |
| Parágrafo ou bloco de texto longo | `richtext` | Wrapea em `<p>` automaticamente — não envolva em `<p>` no markup |
| `<img>` ou `background-image` | `image_picker` | Use com filtro `image_tag` pra adicionar width/height automaticamente |
| `<a href>` + texto | `text` (label) + `url` (destino) | URL só aceita absolutos (http(s)/paths); anchor `#` inválido |
| Cor de fundo, texto, accent, border, shadow — TODAS | `color` | Nunca hardcode hex no CSS; exponha como var `var(--c-*)` e setting |
| Alinhamento (left/center/right) | `select` | Ou `text_alignment` se só left/center/right |
| Tamanho (small/medium/large) com presets de CSS | `select` com classes modificadoras | |
| Padding, margin, gap, radius, thickness, font-size | `range` com `unit: "px"` | `(max-min)/step ≤ 100`; default alinhado ao step |
| Largura máxima em chars | `range` sem `unit` | |
| Toggle on/off | `checkbox` | |
| Quantidade discreta (1-10) | `range` com step 1 | |
| Código Liquid/HTML customizável (escape hatch) | `liquid` ou `html` | `liquid` pré-renderiza, `html` é estático (XSS-safe) |
| Custom CSS por bloco/section | `textarea` | Renderizado em `<style>` scoped via `id="pu-{{ block.id }}"` |
| Lista de itens (FAQs, reviews, tiers, features) | **blocks inline** no schema da section | Padrões repetíveis viram blocks — reorderáveis no theme editor |

**Regras de ouro:**
1. Padrões repetíveis SEMPRE viram blocks inline, nunca settings duplicadas.
2. Toda section tem setting `textarea custom_css` no grupo Advanced — escape hatch pra CSS livre.
3. Todo block também tem `custom_css` próprio + `id="pu-{{ block.id }}"` no root pra scoping.

### Aspect ratios de imagem — traduza pro membro

Quando o setting `image_ratio` for exposto, use `info` ou opções com nomes humanos. A tabela abaixo é o mapping:

| Valor técnico | Nome amigável | Uso típico |
|---|---|---|
| `adapt` | Adaptive (ajusta à imagem) | Default — ratio natural da foto carregada |
| `1 / 1` | Quadrado (1:1) | Product shot, Instagram post |
| `4 / 5` | Portrait vertical (4:5) | Hero moderno, Instagram portrait |
| `3 / 4` | Portrait clássico (3:4) | Foto de pessoa, fashion editorial |
| `16 / 9` | Landscape widescreen (16:9) | Video embed, banner horizontal |
| `3 / 2` | Landscape fotografia (3:2) | Lifestyle, outdoor, reportagem |

Sempre default `adapt` — é o que evita o bug "imagem quadrada em container vertical com espaço branco" (ver Limitação #5).

## Fluxo da Skill

### ETAPA 1 — Leitura e Planejamento (adaptativo à estratégia)

**A página NÃO tem estrutura fixa.** Cada produto merece um plano de sections que reflita sua estratégia específica — awareness level do mercado (Schwartz), sophistication stage (Bond), nível de ceticismo, complexidade do produto, categoria, tipo de decisão (impulse vs considered), presença ou não de mecanismo único, etc. A skill 05 (copy) já definiu essas decisões — respeite-as.

**1. Leia `05-copy.md` + `02-market-research.md` + `03-competitor-analysis.md` + `04-offer.md`** pra entender:
- Awareness level do mercado (Unaware → Most Aware)
- Sophistication stage (1-5)
- Nível de ceticismo (baixo/médio/alto)
- Se tem mecanismo único ou não
- Tipo de produto (commodity, categoria nova, disrupter, incremental)
- Preço (baixo = impulse, alto = considered)

**2. Escolha as sections adequadas a partir do MENU abaixo**, baseando-se no que a estratégia pede. Não force o formato "9 sections padrão" em todo produto.

#### Menu de sections possíveis

**Core (geralmente presente em 90% das PDPs):**
- `hero` — headline + sub + CTA + mídia principal
- `offer` — stack de preços/bundles com CTAs
- `faq` — objeções antecipadas
- `cta-final` — última chance de converter

**Estrutura (escolha baseado na estratégia):**
- `trust-bar` — quando tem 3+ selos de autoridade (media, certificação, rating)
- `benefits` — sempre que a copy tem bullets VOC-loaded (quase sempre). Em produtos Stage 4-5 de sophistication, usar MAIS peso aqui
- `mechanism` — **SÓ se o produto tem mecanismo único** (ingrediente patenteado, processo proprietário, inovação tecnológica). Se for commodity, PULE. Mecanismo forçado em produto sem inovação parece falso
- `social-proof` — essencial em produtos com alto ceticismo (skincare, saúde, wellness). Pular em impulse buys baratos
- `guarantee` — proporcional ao risco percebido. Produto caro/duradouro = seção grande. Impulse = uma linha no footer
- `comparison-table` — quando o produto é disrupter numa categoria madura (vs. concorrentes conhecidos)
- `before-after` — cosmético / estético / transformação visual
- `how-it-works` — produtos complexos com 3+ passos de uso
- `ingredients` — skincare / supplements / food
- `founder-story` — marcas DTC com narrativa de origem forte
- `video-demo` — produto que precisa ver em ação
- `sustainability` — marcas com claim ambiental relevante
- `gift-guide` — produtos sazonais / presenteáveis
- `app-embed` — reviews apps (Okendo, Judge.me), subscription widgets

**3. Monte o plano específico pra ESSE produto.** Exemplos de planos diferentes:

> Produto A — Suplemento nootropic premium ($89, Stage 4, alto ceticismo, tem ingrediente patenteado):
> hero → trust-bar → mechanism → benefits → ingredients → social-proof → founder-story → offer → guarantee → faq → cta-final

> Produto B — Camiseta básica ($25, Stage 2, baixo ceticismo, sem mecanismo único):
> hero → benefits → sustainability → offer → social-proof → faq → cta-final

> Produto C — App de meditação (assinatura $12/mo, Stage 3):
> hero → how-it-works → benefits → video-demo → social-proof → offer → guarantee → faq → cta-final

**4. Pra cada section do plano, decida:**
- Monolítica (só settings, sem blocks) ou com blocks?
- Quais blocks atômicos do catálogo universal (eyebrow, heading, paragraph, etc)
- Quais blocks type-specific (benefit_card, pricing_tier, review_card, faq_item, etc)

**5. Mostre o plano ao membro** antes de começar. Exemplo:

> "Pro seu produto [X], o plano é:
> 1. hero — headline + CTA + badges + stats + floating tags sobre imagem
> 2. trust-bar — 4 selos de mídia
> 3. mechanism — pq tem ingrediente patenteado XXX, essa section é MUITO importante
> 4. ...
>
> Seções que eu NÃO vou incluir: before-after (seu produto é ingestível, não visual), how-it-works (uso simples: 1 cápsula/dia), comparison-table (não tem concorrente direto).
>
> Algum ajuste antes?"

**6.** Aguarde confirmação ou ajustes. Só depois siga pra Etapa 2.

### REGRA CRÍTICA — Eyebrows criativos, não rótulos de framework

**Os nomes "Mechanism", "Offer Stack", "Guarantee Block", "Social Proof", "FAQ Estratégica" são LABELS INTERNOS do framework de copy.** São os "nomes de pasta" usados no `05-copy.md` pra você saber onde cada coisa vai. **Nunca** apareçam literal na página do cliente — soa como template genérico.

**No eyebrow da section (quando tiver), use uma tag CRIATIVA, específica do produto.** Referencie o mecanismo real, o benefício central, ou um ângulo da marca. Exemplos:

| Framework name (interno) | Eyebrow RUIM (literal) | Eyebrow BOM (criativo, produto-específico) |
|---|---|---|
| Mechanism | "The Mechanism" / "Mecanismo" | "The Science", "How It Works", "Why [Produto] Works", "Inside the Formula", "The [Ingrediente]® Difference" |
| Offer / Stack | "Offer Stack" / "Oferta" | "Choose Your [Kit/Routine/Bundle]", "Your Starter Set", "Pick Your Glow", "Build Your Stack", "Start Here" |
| Guarantee | "Guarantee Block" / "Garantia" | "The Promise", "Our Word", "Zero Risk", "Glow or Get Back", "60 Days, No Excuses" |
| Benefits | "Benefits" / "Benefícios" | "Why [Produto]", "Five Things Change", "What You Get", "The Difference" |
| Social Proof | "Social Proof" / "Prova" | "Real Results", "What [Persona] Say", "500+ [Persona] Stories", "Why They Switched" |
| FAQ | "FAQ Estratégica" / "Perguntas Frequentes" | "You Asked", "Before You Buy", "The Real Questions", "Stuff We Hear Most" |
| Trust Bar | "Trust Bar" | (normalmente sem eyebrow, os selos falam sozinhos) |
| CTA Final | "CTA Final" | "One Last Thing", "Ready?", "Your Glow Starts Here" |

**Regras pra escrever eyebrows:**
1. **2-5 palavras.** Curto, punchy.
2. **Específico do produto.** "The pH Difference" é melhor que "The Science".
3. **Em inglês** (copy pro cliente US — seguindo rule 0 do CLAUDE.md).
4. **Sem rotular o framework.** Nunca "Offer" / "Mechanism" / "FAQ" literal.
5. **Pode pular o eyebrow.** Seções como trust-bar, hero e cta-final podem não precisar de eyebrow.
6. **Se o copy tem um Big Idea, USE.** Ex: se o Big Idea é "pH changes everything", o eyebrow do mechanism pode ser "It's Not the Fragrance — It's the pH".

### ETAPA 2 — Brand Discovery (1 mensagem ao membro)

Pergunte (em UMA mensagem) só o que precisa pra começar:

1. **Estilo visual desejado** (escolha 1 ou descreva custom):
   - Minimalist editorial — off-white, sage/cream, generous whitespace, refined serif
   - Bold modern — dark backgrounds, large sans-serif, vibrant accent
   - Clinical premium — clean white, navy/gold, data-forward, technical
   - Wellness organic — warm tones, soft curves, hand-drawn touches
   - Custom — descreva
2. **Cores da marca** se houver (ou "escolhe pra mim baseado no estilo")
3. **Caminhos de assets** (logo, fotos do produto) se tiver — caso contrário usa placeholders
4. **Theme path** (default `~/shopify-theme`)
5. **Handle do produto pro template** (default = slug do nome do produto)
6. **Referência visual (opcional)** — "Tem algum site cujo visual você curte e quer usar como inspiração pra paleta e fontes? Passa o link (ou pula)." Se o membro passar um link, vai pra sub-etapa 2.1. Se não, pula direto pra Etapa 3.

#### ETAPA 2.1 — Referência visual (quando o membro passa link)

**Importante:** isso NÃO é clone de design. É só extração de sinais de paleta/tipografia do site de referência pra ALIMENTAR o `designer-color-system` e o `designer-typography-scale` na Etapa 3. O design ainda é gerado do zero.

1. Valide que Playwright + BeautifulSoup estão instalados:
   ```bash
   python3 -c "import playwright, bs4" 2>&1
   ```
   Se falhar: "Pra extrair signals da referência visual preciso de Playwright + BeautifulSoup. Rode no terminal real:
   ```
   pip install -r tools/design-clone/requirements.txt
   playwright install chromium
   ```
   Ou pula a referência e escolhe um dos estilos pré-definidos."

2. Baixe a página de referência:
   ```bash
   python3 tools/design-clone/downloader.py "URL" "/tmp/ref-[produto]"
   ```

3. Rode analyzer + pattern-extractor pra extrair signals:
   ```bash
   python3 tools/design-clone/analyzer.py "/tmp/ref-[produto]"
   python3 tools/design-clone/pattern-extractor.py "/tmp/ref-[produto]"
   ```

4. Leia `/tmp/ref-[produto]/patterns.json` → extraia apenas o `design_system` (typography + colors + shape + spacing). Ignore `sections[]` — não vamos copiar estrutura, só absorver signals visuais.

5. Mostre ao membro um resumo curto:
   > "Peguei a vibe da [url]:
   > - Fontes: **[heading_font]** (títulos) + **[body_font]** (corpo)
   > - Paleta: fundo **[background_primary]** · texto **[text_primary]** · accents **[accents]**
   > - Radius **[border_radius_px]px** · shadow **[shadow_style]** · density **[density]**
   > 
   > Vou usar isso como input pro design system. O layout e a estrutura ainda vêm da copy — só a paleta/tipografia é inspirada."

6. Siga pra Etapa 3. No `designer-color-system` e `designer-typography-scale`, passe os valores extraídos como **preferência inicial** (não impositivo — o specialist pode ajustar pra garantir contraste WCAG e hierarquia).

### ETAPA 3 — Generate Design System (orquestração)

Antes de gerar qualquer section, defina o sistema de design completo. Invoque os specialists nessa ordem:

1. **Skill `designer-color-system`**: gere paleta de 5-7 cores (background, surface, foreground, primary, accent, muted, border) baseada no estilo + cores da marca + signals da referência (se houver da Etapa 2.1). Saída: hex codes + role semântico.

2. **Skill `designer-typography-scale`**: gere modular type scale (recomendado 1.25 ou 1.333) com 6 níveis (h1-h6) + body + small. Use fluid type com `clamp()`. Sugira heading font + body font (system fonts ou Google Fonts populares). Se houver referência, priorize as fontes extraídas.

3. **Skill `designer-spacing-system`**: gere spacing tokens em base 4px ou 8px (xs, sm, md, lg, xl, 2xl, 3xl).

4. **Skill `designer-layout-grid`**: defina container max-width (recomendado 1200-1440px), grid system, breakpoints (mobile 480, tablet 768, desktop 1024, wide 1440).

5. **Skill `designer-design-token`**: consolide tudo em um conjunto de CSS custom properties que serão injetadas via `:root` no `{% stylesheet %}` de cada section.

6. Salve o design system gerado em `/workspace/[produto]/06-design-system.md` como referência. Mostre ao membro um resumo compacto e peça aprovação rápida.

### ETAPA 4 — Generate Hero Section (3 variantes em paralelo)

A hero é a section mais importante. Gere 3 direções distintas e deixe o membro escolher.

Para cada variante:

1. **Skill `frontend-design`**: gere HTML + CSS (vanilla, não Tailwind) seguindo o design system da etapa 3, usando a copy real do `05-copy.md`. Inclua:
   - Pre-headline / eyebrow tag (se a copy tiver)
   - Headline principal
   - Subheading
   - CTA primário
   - CTA secundário ou trust indicator (rating, "as seen in", etc) se a copy tiver
   - Imagem do produto (placeholder via image_picker)
   - Layout pode variar entre as 3 variantes:
     - **Variante A — Editorial minimalista**: assimétrico, texto à esquerda, imagem à direita, muito whitespace, tipografia grande
     - **Variante B — Centered bold**: tudo centralizado, headline gigante (clamp até 6rem), CTA em destaque, imagem como background sutil
     - **Variante C — Split full-bleed**: 50/50 split, imagem ocupa metade da viewport, texto na outra metade, full-bleed mobile

2. **Skill `designer-visual-hierarchy`**: valida hierarquia da variante.
3. **Skill `designer-responsive-design`**: garante mobile-first com breakpoints corretos.

4. Para cada variante gerada, prepare um preview ASCII/descrição visual da estrutura:
   ```
   VARIANTE A — Editorial Minimalista
   ┌─────────────────────────────────────────┐
   │  EYEBROW TAG                            │
   │                                         │
   │  Large Headline           [Product Img] │
   │  Subheading             [              ]│
   │                         [              ]│
   │  [PRIMARY CTA]  →ver mais [           ]│
   └─────────────────────────────────────────┘
   ```

5. Mostre as 3 variantes ao membro. Pergunte: "Qual variante? A/B/C ou misturar elementos de duas?"

### ETAPA 4.5 — Arquitetura das Sections (padrão validado)

**Use sempre este padrão — cada section é uma "pasta" no sidebar da Shopify com blocks atômicos dentro.** Validado em campo (Horizon, Shopify push zero erros, ~700 settings totais entre 9 sections).

**Princípio central:** a section é um CONTAINER com layout + cores, e cada elemento visual (eyebrow, heading, paragraph, button-row, stats-bar, tag, trust-row, etc) é um **bloco inline** definido dentro do `{% schema %}` da própria section (não theme blocks em arquivos separados).

**Vantagens desse modelo:**
1. Section aparece organizada como pasta no sidebar ("Hero — [nome do produto]") com todos os blocks dentro
2. Membro arrasta blocks pra reordenar, duplica, remove individualmente
3. Membro adiciona blocks novos (Custom Liquid, Custom HTML, Divider, Spacer) sem tocar código
4. Tudo editável: cor de cada micro-elemento, tamanho, espaçamento, font weight, letter spacing
5. Validação passa no `shopify-plugin:shopify-liquid` (não precisa forloop grouping complexo)

**Como funciona:**
- Section file (`sections/page-[produto]-[tipo].liquid`) tem:
  - Markup com `{% for block in section.blocks %}{% case block.type %}...{% endcase %}{% endfor %}`
  - Stylesheet self-contained com CSS vars (`var(--c-accent)`, `var(--c-heading)`)
  - Schema inline com TODOS os blocks definidos
- Template JSON (`templates/page.[produto].json`) tem:
  - Section + seus blocks **pré-populados com copy real**
  - `block_order` na ordem correta
  - Section settings pré-configurados

**Resultado:** membro abre `/pages/[produto]` → **página já montada, bonita, editável**. Não precisa arrastar nada.

**Não use theme blocks em arquivos separados** (`/blocks/*.liquid`) pra esta skill — testamos e o validator do Shopify bloqueia referências dinâmicas via `{% content_for 'block' type: block.type %}`. Blocks inline no schema da section é o padrão que passa.

### ETAPA 5 — Convert Hero to Liquid Section (padrão de blocks inline)

Pegue o HTML+CSS da variante escolhida (Etapa 4) e transforme numa section com blocks inline. A estrutura canônica é:

```liquid
<section class="pu-hero pu-hero-{{ section.id }}" style="--c-bg-top: {{ section.settings.color_bg_top }}; --c-bg-bottom: {{ section.settings.color_bg_bottom }}; --c-accent: {{ section.settings.color_accent }}; /* repita pra cada token do design system */">
  <div class="pu-hero__wrap pu-hero__wrap--{{ section.settings.layout }}">
    <div class="pu-hero__content">
      {%- for block in section.blocks -%}
        {%- case block.type -%}

          {%- when 'eyebrow' -%}
            <p id="pu-{{ block.id }}" class="pu-hero__eyebrow" style="{% if block.settings.color != blank %}color: {{ block.settings.color }};{% endif %} margin: {{ block.settings.space_before }}px 0 {{ block.settings.space_after }}px;" {{ block.shopify_attributes }}>
              {{ block.settings.text }}
            </p>
            {%- if block.settings.custom_css != blank -%}<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>{%- endif -%}

          {%- when 'heading' -%}
            <h2 id="pu-{{ block.id }}" class="pu-hero__heading pu-hero__heading--size-{{ block.settings.size }}" style="{% if block.settings.color != blank %}color: {{ block.settings.color }};{% endif %} line-height: {{ block.settings.line_height | times: 0.1 }}; margin: {{ block.settings.space_before }}px 0 {{ block.settings.space_after }}px;" {{ block.shopify_attributes }}>{{ block.settings.text }}</h2>
            {%- if block.settings.custom_css != blank -%}<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>{%- endif -%}

          {# ... outros blocks: paragraph, badge, button_row, stats_bar, trust_row, divider, icon, spacer, custom_liquid, custom_html #}
          {# IMPORTANTE: NÃO adicione case pra 'tag' aqui — blocks tipo tag são renderizados separadamente dentro de figure_wrap (abaixo) pra ficar sobre a imagem. Adicionar case aqui causa double-render. #}

        {%- endcase -%}
      {%- endfor -%}
    </div>

    {%- if section.settings.show_figure -%}
      <div class="pu-hero__figure_wrap">
        <figure class="pu-hero__figure" data-adapt="{% if section.settings.image_ratio == 'adapt' %}true{% else %}false{% endif %}" style="{% if section.settings.image_ratio != 'adapt' %}aspect-ratio: {{ section.settings.image_ratio }};{% endif %}">
          {%- if section.settings.image -%}
            {{ section.settings.image | image_url: width: 1600 | image_tag: loading: 'eager', widths: '400, 800, 1200, 1600', sizes: '(min-width: 900px) 50vw, 100vw' }}
          {%- endif -%}
        </figure>
        {# Tags (floating) ficam FORA do figure pra overflow não cortá-los #}
        {%- for block in section.blocks -%}
          {%- if block.type == 'tag' -%}
            <span id="pu-{{ block.id }}" class="pu-hero__tag pu-hero__tag--{{ block.settings.position }}" {{ block.shopify_attributes }}>
              {%- if block.settings.eyebrow != blank -%}<em>{{ block.settings.eyebrow }}</em>{%- endif -%}
              <strong>{{ block.settings.title }}</strong>
            </span>
            {%- if block.settings.custom_css != blank -%}<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>{%- endif -%}
          {%- endif -%}
        {%- endfor -%}
      </div>
    {%- endif -%}
  </div>
</section>

{%- if section.settings.custom_css != blank -%}
<style>.pu-hero-{{ section.id }} { {{ section.settings.custom_css }} }</style>
{%- endif -%}

{% stylesheet %}
  /* section-scoped styles usando CSS vars do :root da section */
  /* todos hardcoded hex viram var(--c-*) pra edição */
{% endstylesheet %}

{% schema %}
{
  "name": "[Produto] — Hero",
  "tag": "section",
  "class": "page-[produto]-hero-section",
  "settings": [
    { "type": "header", "content": "Layout" },
    { "type": "select", "id": "layout", "options": [...] },
    { "type": "range", "id": "container_max", "min": 800, "max": 1600, "step": 20, "unit": "px", "default": 1280 },
    { "type": "range", "id": "padding_y", "min": 24, "max": 200, "step": 4, "unit": "px", "default": 112 },
    { "type": "header", "content": "Image" },
    { "type": "image_picker", "id": "image" },
    { "type": "select", "id": "image_ratio", "options": [{"value": "adapt", "label": "Adaptive"}, ...] },
    { "type": "select", "id": "image_fit", "options": [{"value": "cover", "label": "Cover"}, {"value": "contain", "label": "Contain"}] },
    { "type": "header", "content": "Colors" },
    { "type": "color", "id": "color_bg_top", "default": "..." },
    { "type": "color", "id": "color_accent", "default": "..." },
    /* etc — cada token do design system vira uma color setting */
    { "type": "header", "content": "Advanced" },
    { "type": "textarea", "id": "custom_css", "label": "Section custom CSS" }
  ],
  "blocks": [
    { "type": "eyebrow", "name": "Eyebrow", "settings": [...] },
    { "type": "heading", "name": "Heading", "settings": [...] },
    { "type": "paragraph", "name": "Paragraph", "settings": [...] },
    { "type": "button_row", "name": "CTA row", "settings": [...] },
    { "type": "stats_bar", "name": "Stats bar", "settings": [...] },
    { "type": "tag", "name": "Floating tag", "settings": [...] },
    { "type": "divider", "name": "Divider", "settings": [...] },
    { "type": "spacer", "name": "Spacer", "settings": [...] },
    { "type": "custom_liquid", "name": "Custom Liquid", "settings": [...] },
    { "type": "custom_html", "name": "Custom HTML", "settings": [...] }
  ],
  "presets": [ { "name": "[Produto] — Hero", "blocks": [ /* todos os blocks com settings pré-populados */ ] } ]
}
{% endschema %}
```

**Regras inegociáveis pra CADA block no schema:**

1. **Agrupe settings por `header`**: Content / Style / Spacing / Advanced
2. **Exponha toda cor visível como `color` setting**: bg, text, border, shadow, hover — tudo editável
3. **Exponha todo tamanho como `range`**: font-size, padding, gap, radius, thickness
4. **Toda tipografia customizável**: size select, weight select, letter-spacing select, font-family select
5. **Toda seção tem `space_before` e `space_after` ranges** pra margens top/bottom
6. **SEMPRE termine com `header: Advanced` + `textarea: custom_css`** — escape hatch pra CSS livre
7. **Todo bloco emite `id="pu-{{ block.id }}"`** e fecha com `{% if block.settings.custom_css != blank %}<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>{% endif %}` pra scoping

**Blocks obrigatórios em TODA section** (universais): `custom_liquid`, `custom_html`, `divider`, `spacer` — escape hatches que o membro sempre vai querer ter disponíveis.

**Ferramenta de ajuda:** `tools/design-clone/liquid-converter.py` gera section boilerplate (cores auto-extraídas, labels semânticos, image controls). Útil como DRAFT — depois você adapta pro padrão de blocks inline descrito aqui. Nunca use o output do converter diretamente na Aura Engine — sempre refatore pro padrão acima.

**Validação obrigatória:**
```bash
node .../shopify-liquid/scripts/validate.mjs --filename page-[produto]-hero.liquid --filetype sections --code "$(cat file)" --model ... --client-name claude-code --artifact-id [produto]-hero --revision 1
```
Se falhar, leia o erro, ajuste, revalide (3 retries max).

**Salve em:** `~/shopify-theme/sections/page-[produto]-[tipo].liquid`

### Catálogo de Block Types Universais

Toda section da página deve expor este conjunto de blocks (adapte os type-specific conforme a natureza da section — uma FAQ section usa `faq_item` em vez de `stat`, etc). Esses são os universais que SEMPRE estão disponíveis:

| Block type | Uso | Settings obrigatórios |
|---|---|---|
| `eyebrow` | Label pequeno em cima de headings | text · size · weight · transform · tracking · color · dash before/after · dash color · space before/after · **custom_css** |
| `heading` | Título (h1/h2/h3) com `<em>` italic permitido | text (inline_richtext) · size (display1/display2/h1/h2/h3) · font (serif/sans) · weight · color · italic color · line_height · letter_spacing · max_width · space before/after · **custom_css** |
| `paragraph` | Parágrafo de texto | text (richtext) · size · color · line_height · max_width · space before/after · **custom_css** |
| `badge` | Pill/chip com dot opcional | text · show_dot · dot_color · dot_size · dot_pulse · variant · bg · text_color · border_color · font_size · padding x/y · radius · space before/after · **custom_css** |
| `button_row` | Container de até 3 botões inline | alignment · gap · show_arrow · radius · padding x/y · font_size · arrow_color · price_bg · price_text · por botão: show · label · url · variant · bg · text · price · space before/after · **custom_css** |
| `stats_bar` | Container de até 5 stats em grid | columns · gap · alignment · show_divider · divider_color · divider_thickness · divider_spacing · label_color · value_color · unit_color · por stat: show · label · value (inline_richtext com `<span>` pra unit) · space before/after · **custom_css** |
| `trust_row` | Até 6 trust items (icon + label) inline | alignment · gap x/y · show_divider · divider_color · icon_color global · label_color · por item: show · icon · label · space before/after · **custom_css** |
| `tag` | Floating tag posicionado sobre imagem | eyebrow · title · position (tl/tr/bl/br) · rotation · theme (light/dark/accent) · bg · text · border · radius · padding · shadow_color · shadow_y · shadow_blur · **custom_css** |
| `divider` | Linha separadora | style (solid/dashed/dotted/gradient) · color · thickness · width % · space before/after · **custom_css** |
| `icon` | Ícone/emoji isolado | icon · size · color · space before/after · **custom_css** |
| `spacer` | Espaço vertical custom | height · **custom_css** |
| `custom_liquid` | **Escape hatch.** Código Liquid/HTML arbitrário | code (`type: "liquid"`) · space before/after · **custom_css** |
| `custom_html` | Código HTML estático | html (`type: "html"`) · space before/after · **custom_css** |

**Blocks type-specific por section** (adicione ALÉM dos universais):
- Benefits → `benefit_card` (num/icon + title + body + accent color)
- Proof → `review_card` (quote + author + avatar + meta + featured checkbox)
- Offer → `pricing_tier` (name + price + strap + features richtext + CTA + badge + popular checkbox + image)
- Guarantee → `promise_item` (title + body + accent color + icon)
- FAQ → `faq_item` (question + answer richtext + open_by_default checkbox)
- Mechanism → `mechanism_card` (tag + value + status + list items — nomeie conforme o mecanismo real do produto, ex: `ingredient_card`, `process_step`, `science_card`)

**Regra dos 4 headers em TODO bloco** (organização):
1. `Content` — os campos de texto/imagem/url (o QUE mostra)
2. `Style` — cores, tamanhos, variantes, fontes (o COMO mostra)
3. `Spacing` — space_before, space_after (o ONDE fica)
4. `Advanced` — custom_css textarea (o ÚLTIMO recurso pra edição não-coberta)

### Customização máxima — checklist por block

Antes de salvar a section, verifique que CADA bloco tem:
- [ ] TODA cor visível editável (bg, text, border, shadow, dot, underline, ícone interno)
- [ ] TODO tamanho editável (font-size, padding x/y, radius, thickness, gap)
- [ ] Tipografia editável (size, weight, letter-spacing, line-height, transform)
- [ ] Spacing top/bottom por range
- [ ] `custom_css` textarea na aba Advanced
- [ ] Root element tem `id="pu-{{ block.id }}"` pra o CSS ser scoped
- [ ] `<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>` injetado após o markup

### ETAPA 6 — Generate Remaining Sections

Para cada section do plano (etapa 1) além do hero, aplique o MESMO padrão da Etapa 5: **uma section file com blocks inline no schema** (nunca theme blocks em `/blocks/*.liquid`).

Loop por section:

1. **Skill `frontend-design`**: gera HTML + CSS vanilla seguindo o design system da etapa 3 + copy real da section (vem do `05-copy.md`).

2. **Specialists relevantes** (chame quando aplicável):
   - `designer-visual-hierarchy` — sempre
   - `designer-responsive-design` — sempre
   - `designer-component-spec` — pra sections com componentes complexos (FAQ accordion, tabs, carousel)
   - `designer-micro-interaction-spec` — pra hovers, focus states, transições
   - `designer-feedback-patterns` — pra estados de confirmação

3. Identifique os **blocks universais** (do Catálogo) que a section precisa: `eyebrow`, `heading`, `paragraph`, `button_row`, `divider`, `spacer`, `custom_liquid`, `custom_html` — normalmente todos.

4. Identifique os **blocks type-specific** pra essa section:
   - `benefits` → bloco `benefit_card` (num/icon + title + body)
   - `social-proof` / `proof` → bloco `review_card` (stars + quote + author + avatar + featured)
   - `faq` → bloco `faq_item` (question + answer richtext + open_by_default)
   - `offer` → bloco `pricing_tier` (name + price + features richtext + CTA + badge + popular + image)
   - `mechanism` → bloco `mechanism_card` ou `feature_compare` (tag + value + status + list — nomeie o type conforme o mecanismo real: `ingredient_card` pra skincare, `process_step` pra how-it-works, `science_card` pra claim técnico)
   - `before-after` → bloco `comparison_pair` (before_image + after_image + label)
   - `guarantee` → bloco `promise_item` (title + body + accent + icon)
   - `ingredients` → bloco `ingredient` (name + role + dosage + image)
   - `how-it-works` → bloco `step` (number + title + description + image)

5. Converta pro padrão de **blocks inline no schema da section** (igual Etapa 5):
   - `{% for block in section.blocks %}{% case block.type %}...{% endcase %}{% endfor %}` no markup
   - TODOS os blocks (universais + type-specific) definidos dentro do array `blocks` do `{% schema %}` da section
   - Cada block com `id="pu-{{ block.id }}"` e `custom_css` na aba Advanced
   - Section com `textarea custom_css` global

6. Valide com `shopify-plugin:shopify-liquid` (só a section — blocks inline vão junto).

7. Salve em `~/shopify-theme/sections/page-[produto]-[tipo].liquid`.

**Não crie arquivos em `~/shopify-theme/blocks/`** pra esta skill. Theme blocks em arquivos separados falham no validator quando renderizados com `{% content_for 'block' type: block.type id: block.id %}` (ver Limitação #12).

### ETAPA 7 — UX Writing Pass

Após gerar todas as sections:

1. **Skill `designer-ux-writing`**: revise toda a microcopy gerada nas settings de:
   - CTAs (deve refletir valor, não ação genérica — "Buy Now" é ruim, "Start Your 30-Day Transformation" é bom)
   - Empty states de placeholders nas settings
   - Alt texts default das imagens
   - Aria labels
   - FAQ wording
2. Aplique as melhorias diretamente nos defaults dos schemas das sections.

### ETAPA 8 — Self-Critique Pass (orquestração de qualidade)

Esta é a etapa que move qualidade de 8/10 pra 9/10. Não pule.

1. **Skill `designer-design-critique`**: critique o conjunto completo de sections geradas. Foque em:
   - Hierarquia visual entre sections
   - Consistência de espaçamento
   - Ritmo da página (a página guia o leitor naturalmente?)
   - Originalidade (foge do padrão genérico de IA?)
2. **Skill `designer-heuristic-evaluation`**: aplica heurísticas de Nielsen.
3. **Skill `designer-accessibility-audit`**: WCAG 2.1 AA full audit em todas as sections.
4. **Skill `designer-design-qa-checklist`**: QA final.

5. Compile todas as issues encontradas. Pra cada issue:
   - Identifique a section/block afetado
   - Identifique o fix exato
   - Aplique no código
   - Revalide com `shopify-plugin:shopify-liquid`

6. Se alguma issue não for corrigível sem mudança estrutural significativa, liste pro membro como "issues conhecidas" no relatório final.

### ETAPA 9 — Create Page Template (blocks pré-populados com a copy)

**REGRA DE OURO:** Quando o membro abre `/pages/[produto]` no theme editor, a página tem que estar **100% montada** com todos os blocks no lugar certo + todos os settings preenchidos com a copy real. Não é pra ele arrastar nada. Ele só edita/deleta/adiciona se quiser.

Pra isso, o `templates/page.[produto].json` **precisa listar TODOS os blocks** dentro de cada section, com settings inline. **Section sem `blocks: {...}` preenchido NÃO funciona** — se a entry tiver só `settings: {}` (sem a key `blocks`), ou `blocks: {}` vazio, a página renderiza zero blocks. Apesar dos defaults estarem no schema, o Shopify só popula blocks do preset quando o membro adiciona a section manualmente via "Add section". Pra páginas pré-montadas via template JSON, os blocks precisam estar **explícitos no próprio JSON** com `blocks: {...}` + `block_order: [...]`.

**Padrão correto do template JSON:**

```json
{
  "sections": {
    "hero": {
      "type": "page-[produto]-hero",
      "blocks": {
        "badge": {
          "type": "badge",
          "settings": {
            "text": "[eyebrow da copy]",
            "show_dot": true,
            "dot_color": "[cor do design system]",
            "variant": "solid",
            "font_size": 13,
            "padding_x": 14,
            "padding_y": 7,
            "radius": 99,
            "space_after": 20,
            "custom_css": ""
          }
        },
        "heading": {
          "type": "heading",
          "settings": {
            "text": "[hero headline da copy, com <em>palavra</em> pra emphasis]",
            "size": "display2",
            "font": "serif",
            "weight": "500",
            "line_height": 10,
            "letter_spacing": "-0.03em",
            "space_after": 24
          }
        },
        "paragraph": {
          "type": "paragraph",
          "settings": {
            "text": "<p>[sub-headline da copy]</p>",
            "size": "lg",
            "line_height": 15,
            "max_width": 48,
            "space_after": 24
          }
        },
        "cta_row": {
          "type": "button_row",
          "settings": {
            "alignment": "flex-start",
            "gap": 12,
            "radius": 4,
            "btn_1_show": true,
            "btn_1_label": "[CTA principal]",
            "btn_1_variant": "primary",
            "btn_1_price": "[preço se aplicável]",
            "btn_2_show": true,
            "btn_2_label": "[CTA secundário]",
            "btn_2_variant": "ghost",
            "btn_3_show": false
          }
        },
        "stats": {
          "type": "stats_bar",
          "settings": {
            "columns": 3,
            "show_divider": true,
            "stat_1_show": true,
            "stat_1_label": "[label 1]",
            "stat_1_value": "[value 1 com <span>unit</span>]",
            "stat_2_show": true,
            "stat_2_label": "[label 2]",
            "stat_2_value": "[value 2]",
            "stat_3_show": true,
            "stat_3_label": "[label 3]",
            "stat_3_value": "[value 3]"
          }
        },
        "tag_1": {
          "type": "tag",
          "settings": {"eyebrow": "[tag 1 eyebrow]", "title": "[tag 1 title]", "position": "tl", "rotation": -3, "theme": "light"}
        },
        "tag_2": {
          "type": "tag",
          "settings": {"eyebrow": "[tag 2 eyebrow]", "title": "[tag 2 title]", "position": "br", "rotation": 3, "theme": "dark"}
        }
      },
      "block_order": ["badge", "heading", "paragraph", "cta_row", "stats", "tag_1", "tag_2"],
      "settings": {
        "layout": "split-lr",
        "container_max": 1280,
        "padding_y": 112,
        "column_gap": 56,
        "image_ratio": "adapt",
        "image_fit": "cover",
        "color_bg_top": "[design system bg]",
        "color_bg_bottom": "[design system bg2]",
        "color_text": "[design system text]",
        "color_heading": "[design system heading]",
        "color_accent": "[design system accent]",
        "color_on_accent": "[design system on-accent]"
      }
    }
  },
  "order": ["hero", "benefits", "mechanism", "proof", "offer", "guarantee", "faq", "cta_final"]
}
```

**Pseudocódigo acima — só o hero expandido.** Replique a estrutura pras outras sections do plano (benefits, mechanism, etc), cada uma com `blocks: {...}` + `block_order: [...]` + `settings: {...}` completos. JSON real não aceita `/* comentários */` nem `...` — todo bloco fica listado explicitamente.

**Checklist final do template JSON:**
- [ ] TODA section tem `blocks: {...}` pré-populado (não `{}`)
- [ ] TODO block tem `settings: {...}` com os valores da copy real (não vazios)
- [ ] Cada section tem `block_order: [...]` com a ordem correta
- [ ] Section `settings` têm as cores do design system aplicadas
- [ ] `order: [...]` lista todas as sections na sequência persuasiva (hero → proof → offer → cta)
- [ ] Copy REAL populada: hero headline, sub-headline, CTAs, stats, benefits VOC, testimonials, tiers, FAQ questions+answers, CTA final — tudo do `05-copy.md`

**Quando salvar:** `~/shopify-theme/templates/page.[produto].json`. O Shopify CLI faz upload via `shopify theme push` (Etapa 10).

### ETAPA 10 — Install no tema do membro (safe preview)

**Regra:** nunca modifique o tema live do membro. Sempre trabalhe numa duplicata unpublished. A Shopify CLI faz isso em 4 comandos.

1. **Detectar store + tema ao vivo:**
   ```bash
   shopify theme list --json --store [LOJA].myshopify.com
   shopify theme info --json
   ```
   Identifique o theme com `"role": "live"` e anote o ID.

2. **Duplicar o tema live (cria cópia unpublished):**
   ```bash
   shopify theme duplicate --theme [LIVE-THEME-ID] --name "[Produto] Preview (Aura)" \
     --store [LOJA].myshopify.com --force --json
   ```
   Output inclui o ID novo. Chame de `[NEW-ID]`.

3. **Pullar a cópia pra pasta local:**
   ```bash
   shopify theme pull --theme [NEW-ID] --store [LOJA].myshopify.com \
     --path ~/shopify-theme-[produto] --force
   ```

4. **Instalar os arquivos gerados:**
   ```bash
   # Copia section files + template JSON pro tema duplicado
   cp <dir-staging>/sections/page-[produto]-*.liquid ~/shopify-theme-[produto]/sections/
   cp <dir-staging>/templates/page.[produto].json ~/shopify-theme-[produto]/templates/
   ```
   Onde `<dir-staging>` é onde a skill gerou os arquivos (ex: `/tmp/aura-page-[produto]/` ou diretamente no `~/shopify-theme-[produto]/` se você gerou lá). **Não tem diretório `blocks/`** — todos os blocks são inline no schema da section.

5. **Push pra cópia unpublished:**
   ```bash
   shopify theme push --theme [NEW-ID] --store [LOJA].myshopify.com \
     --path ~/shopify-theme-[produto] --nodelete --json
   ```
   O `--nodelete` preserva tudo que já existe no tema copiado. Se aparecer `"warning": "..."` no JSON com campo `"errors"`, resolva os erros (veja "Limitações Shopify" abaixo) e re-push.

6. **Dar o preview link ao membro:**

   Theme editor direto no template:
   ```
   https://[LOJA].myshopify.com/admin/themes/[NEW-ID]/editor?template=page.[produto]
   ```

   Preview da storefront (precisa a página "[produto]" existir no Admin → Pages):
   ```
   https://[LOJA].myshopify.com/pages/[produto]?preview_theme_id=[NEW-ID]
   ```

   **IMPORTANTE:** o dropdown "Theme template" no admin Pages SÓ lista templates do tema LIVE. Como `page.[produto]` só existe na cópia unpublished, não aparece lá. Workaround: usar `?view=[produto]` na URL do storefront pra forçar o template alternate, OU o theme editor direto (funciona sempre).

### ETAPA 10.5 — Report ao membro

Mostre ao membro:

1. **Sections geradas** + justificativa do plano específico (por que incluiu/excluiu cada section baseado na estratégia da copy).
2. **Lista de arquivos criados** (paths absolutos).
3. **Preview links** (theme editor + storefront com `?view=`).
4. **Como subir pra produção** (quando satisfeito):

   > ⚠️ **Aviso**: `shopify theme publish` substitui o tema live atual. Antes, duplique o live como backup:
   > ```
   > # 1. Backup do live atual (recomendado antes de publicar a cópia Aura):
   > shopify theme duplicate --theme [LIVE-THEME-ID] --name "Pre-Aura Backup $(date +%Y%m%d)" --store [LOJA].myshopify.com --force
   > 
   > # 2. Depois publica a cópia Aura como live:
   > shopify theme publish --theme [NEW-ID] --store [LOJA].myshopify.com
   > ```
   > Se der ruim: abre admin → Online Store → Themes → encontra "Pre-Aura Backup [data]" → Publish.
5. **Settings expostos** por block/section (resumo compacto).
6. **Issues conhecidas** da etapa 8.

### ETAPA 11 — Iteration Loop

Termine perguntando: 

> "Página gerada e validada. Quer ajustar algo? Pode pedir coisas como: 'hero muito apertado, mais ar', 'cores mais escuras', 'features em 2 colunas em vez de 3', 'adicionar countdown na oferta'. Vou refinar sem regenerar tudo do zero."

Para ajustes futuros:
- Mudanças de spacing/layout → edite o `{% stylesheet %}` da section afetada
- Mudanças estruturais → adicione/remova settings + blocks
- Mudanças de copy → atualize os defaults no schema E os pré-populados no template JSON
- **Sempre** revalide com `shopify-plugin:shopify-liquid` após qualquer mudança

### SALVAR (dual output obrigatório — rule 6b do CLAUDE.md)

Salve um relatório completo em **DOIS arquivos** dentro de `/workspace/[produto]/`:

1. **`06-page.md`** (fonte — a AI lê nas fases seguintes)
2. **`06-page.html`** (visualização humana — o membro abre no browser)

Conteúdo de ambos:

- Plano de sections gerado (etapa 1) + justificativa por que incluiu/excluiu cada section
- Brand discovery answers (etapa 2) — incluindo se usou referência visual e qual
- Design system completo (etapa 3) — paleta, tipografia, spacing, breakpoints
- Variante de hero escolhida + por quê (etapa 4)
- Lista de arquivos criados (etapa 10) com paths absolutos
- Settings expostos por section (resumo compacto — etapa 10.5)
- Preview links (theme editor + storefront)
- Issues conhecidas (se houver, da etapa 8)
- Histórico de iterações (etapa 11) — atualize a cada refinement

**Como gerar o `.html`:** use o design system de `.claude/templates/aura-report-template.html` — copie o CSS completo + estrutura de componentes (section-label, callout, note, opportunity, pill, table-wrap, quote, kpi-grid). Self-contained (CSS inline, sem server). Inclua o logo SVG do Aura no topo. Responsivo mobile (overflow-wrap, word-break em code/callout).

Ao final diga:

> "Page-engine completo. Próximo passo: rode `shopify theme dev` pra ver ao vivo, ou diga 'creatives' pra gerar briefings de criativos pra ads, ou 'scale' pra estratégia de escala."

## Debug — Quando `shopify theme push` falha

Quando o push retorna JSON com campo `"errors"`, leia a mensagem do erro e aja conforme a tabela:

| Mensagem de erro (trecho) | Causa provável | Solução | Limitação |
|---|---|---|---|
| `Missing width and height attributes on img tag` | `<img>` sem dimensões — falha CLS | Use `{{ image \| image_url: width: X \| image_tag: loading: 'lazy' }}` no markup | #1 |
| `default must be a string or datasource access path` | `url` setting com `#anchor` ou relative path como default | Deixe o default vazio ou use URL absoluto `http(s)://` ou `/path/` | #2 |
| `invalid inline richtext: Attribute 'X' is not permitted` | `inline_richtext` com `class`/`aria`/`data` nas tags inline | Strip esses attributes antes de setar no default — só `<em>`, `<strong>`, `<br>`, `<span>`, `<a>`, `<u>`, `<p>` sem attrs | #3 |
| `Range settings must have at most 101 steps` | `(max - min) / step > 100` | Aumente o `step` ou reduza o range | #9 |
| `step invalid. Range settings must have at most 101 steps` | Mesmo do anterior | Mesmo | #9 |
| `default must be a step in the range` | Default não é múltiplo válido (ex: `min: 6, step: 2, default: 15`) | Ajuste o default pra `min + N*step` | #10 |
| `Opening tag does not have a matching closing tag` | Theme-check de HTML balance num conditional Liquid | Evite quebrar tags HTML em `{% if %}` — use atributos/classes condicionais ou container blocks | #12 |
| `The 'id' argument should be a string` | Uso de theme blocks em `/blocks/` com `{% content_for 'block' type: block.type %}` dinâmico | Refatore pra blocks inline no schema da section com `{% case block.type %}` | #12 |
| `Section type 'X' does not refer to an existing section file` | Template JSON referencia section que não foi installada ainda OU falhou install | Push a section antes, ou verifique ordem dos arquivos no `cp` | — |
| `Theme block 'blocks/X.liquid' does not exist` | Mesma causa — theme blocks referenciados mas arquivos não existem | Igual acima | — |
| `ERR_MODULE_NOT_FOUND @shopify/theme-check-common` (na validação local) | Plugin aponta pra registry privado `npm.shopify.io` | `cd <plugin-dir> && rm package-lock.json && npm install --registry=https://registry.npmjs.org/` | #8 |
| Page template não aparece no dropdown "Theme template" do admin Pages | Admin só lista templates do tema LIVE; seu template tá na cópia unpublished | Use theme editor direto: `/admin/themes/<NEW-ID>/editor?template=page.<produto>` | #6 |
| `shopify theme duplicate` trava esperando confirmação | Contexto não-interativo | Adicione flag `--force` | #7 |

**Fluxo:** sempre leia o JSON do push (`--json`), filtre `"errors"`, resolva erro por erro consultando a tabela. Se a mensagem não bater com nenhuma linha, consulte a seção de limitações completa abaixo.

## Limitações Shopify conhecidas (descobertas em campo)

Estas regras vêm do validator oficial `shopify-plugin:shopify-liquid` + push pra tema real. O converter aplica automaticamente, mas se você editar à mão, respeite:

1. **`<img>` precisa `width` e `height`** — senão falha validação. Use o filtro `image_tag` do Shopify (auto-adiciona): `{{ image | image_url: width: 1600 | image_tag: loading: 'lazy' }}`.

2. **`url` setting não aceita `#anchor` como default** — só URLs absolutos (`http(s)://...`) ou paths (`/products/...`). Se o HTML de origem tem `href="#shop"`, deixe o default **vazio**; o membro preenche no theme editor.

3. **`inline_richtext` não aceita attributes em tags** — só tags simples: `<em>`, `<strong>`, `<br>`, `<span>`, `<a>`, `<u>`, `<p>`. Strip `class`, `aria-*`, `data-*` do HTML antes de colocar no default.

4. **`richtext` wraps em `<p>` automaticamente** — se seu markup é `<p>{{ setting }}</p>`, vai dar `<p><p>...</p></p>`. Use `<div>` ou `inline_richtext`.

5. **Aspect-ratio conflicts**: nunca deixe um ancestral do `<img>` com `aspect-ratio` fixa + deixe `image_wrap` com `aspect-ratio: auto` esperando ser adapt — o pai ganha. Use `data-adapt="true"` attr + CSS com seletor `[data-adapt='true']` como o converter v3 faz.

6. **Dropdown "Theme template" do admin Pages só lista templates do tema LIVE** — templates que existem só em tema unpublished não aparecem. Workaround pra preview: abrir o theme editor direto no template (`.../editor?template=page.[produto]`) ou usar `?view=[produto]` na URL do storefront.

7. **`shopify theme duplicate` precisa de `--force`** em contextos não-interativos. Sem isso trava esperando confirmação.

8. **Package-lock do plugin `shopify-plugin:shopify-liquid`** aponta pro registry privado `npm.shopify.io` que requer auth. Se `node scripts/validate.mjs` falhar com `ERR_MODULE_NOT_FOUND`, rode no dir do plugin: `rm package-lock.json && npm install --registry=https://registry.npmjs.org/`.

9. **Range settings: max 101 steps.** `{"min": 0, "max": 999, "step": 1}` falha push. Use `step: 10` ou reduza `max`. Fórmula: `(max - min) / step ≤ 100`.

10. **Range default deve alinhar ao step.** Se `min: 6, step: 2`, defaults válidos são 6, 8, 10, 12... — 15 é inválido. Sempre cheque: `(default - min) % step == 0`.

11. **Preset de section ≠ blocks em template JSON.** O `presets` do schema da section só popula blocks quando o membro ADICIONA a section manualmente via "Add section" no theme editor. Pra páginas pré-montadas via `templates/page.[produto].json`, os blocks precisam estar **dentro do template JSON** com `blocks: {...}` explícito + `block_order: [...]`. Section entry sem a key `blocks` (ou com `blocks: {}` vazio) renderiza ZERO blocks — esse é o erro mais comum. Não confundir: `settings: {}` vazio está OK (defaults do schema assumem), o que quebra é a ausência dos `blocks`.

12. **Blocks inline no schema da section** (via `{% case block.type %}`) passa validação. **Theme blocks em arquivos separados** (`/blocks/*.liquid` + `{% content_for 'block' type: block.type id: block.id %}`) FALHA com "The 'id' argument should be a string" — o linter não aceita vars dinâmicas. Sempre use inline.

13. **`inline_richtext` renderiza HTML no browser mas o preview editor pode mostrar raw**. Se o membro editar um stat value como `4.8<span>/5</span>`, o editor do theme mostra o `<span>` literal. Solução: `info` no setting explicando (`"info": "Use <span> for the unit"`). Em runtime renderiza correto.

14. **Custom Liquid em block: use `type: "liquid"` no schema.** Shopify pré-renderiza o código em tempo de theme push. `type: "html"` aceita HTML estático (seguro contra XSS).

15. **Admin API: criar página via CLI não existe.** `shopify page create` não é um comando. O membro precisa criar a página em Admin → Pages → Add page manualmente. A skill entrega theme editor URL direto (`?template=page.[produto]`) que rola sem precisar da página existir antes.

## DO NOT

NUNCA, em hipótese alguma:

- Use o block NATIVO do Shopify chamado `custom_liquid` (o que a plataforma adiciona nos temas e esconde HTML cru). Nosso block `custom_liquid` customizado (setting `type: "liquid"`) é permitido porque é editável.
- Hardcode texto/imagens/cores no markup (sempre via settings)
- Use classes do tema pai (`.product-card`, `.btn`, `.button`, etc) — sempre namespace próprio
- Use `asset_url` ou caminhos hardcoded de imagens (sempre `image_picker`)
- Use `!important` em CSS
- Use IDs em selectores CSS (use classes)
- Importe libraries externas de JS ou CSS
- Use jQuery, React, Vue, ou qualquer framework JS
- Salve um arquivo sem antes validar com `shopify-plugin:shopify-liquid`
- Pule a self-critique pass (etapa 8) — é onde mora a maior parte do ganho de qualidade
- Ignore o mobile — sempre teste mentalmente em 375px primeiro
- Use Tailwind ou utility frameworks no output final (vanilla CSS dentro de `{% stylesheet %}`)
- Crie sections que "funcionam só no Horizon" — sempre theme-agnostic
- Copiar HTML/CSS do site de referência direto pro tema do membro. Referência visual (Etapa 2.1) alimenta apenas os specialists de design — o código é sempre gerado do zero via `frontend-design`.

## Princípios de Qualidade Visual (ground rules pro frontend-design)

Quando invocar o skill `frontend-design` ou gerar CSS diretamente, sempre:

- **Type scale modular**: 1.25 (Major Third) ou 1.333 (Perfect Fourth)
- **Fluid type**: `font-size: clamp(min, preferred-vw, max)` em headings
- **Spacing generoso**: padding-block 5-8rem em sections importantes (hero, oferta), 3-4rem em sections de transição
- **Hierarchy clara**: h1 muito maior que h2, h2 maior que h3 (pelo menos 1.25x cada nível)
- **Microinterações sutis**: hover transitions de 200-300ms ease-out, jamais bouncy
- **Container max-width**: 1200-1440px com padding lateral generoso
- **Container queries** quando aplicável (não só viewport queries)
- **CSS Grid pra layouts 2D**, Flexbox pra unidimensionais
- **Custom properties pra TUDO** que pode ser editável (cores, fontes, spacing, raios, sombras)
- **Sombras sutis** se houver — `box-shadow` com opacity baixa, jamais "card-with-thick-shadow" padrão
- **Border radius consistente** — define um valor base no design system (ex: 8px) e múltiplos (4px, 8px, 16px, 24px, 9999px pra pills)
- **Focus states visíveis** — `outline: 2px solid var(--accent); outline-offset: 2px;` em foco-visible
- **Reduced motion respect**: `@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }`

## Acessibilidade — checklist obrigatório (quality standard, não template)

Toda section gerada precisa passar neste checklist. São regras **universais** que **não restringem design** — valem pra qualquer paleta, tipografia, layout, e vibe visual. São o equivalente a "validar Liquid": garante que o código funciona pra todos os usuários.

A skill `designer-accessibility-audit` (Etapa 8) aplica um audit WCAG 2.1 AA completo — mas desde o momento da geração (Etapas 5 e 6) respeite estas regras pra evitar retrabalho:

### Conteúdo semântico
- [ ] `<h1>` usado 1× por página (normalmente no hero); h2/h3 nas demais
- [ ] Heading order sem pular níveis (h1 → h2 → h3, nunca h1 → h3)
- [ ] `<section>`, `<article>`, `<header>`, `<footer>`, `<nav>`, `<main>`, `<aside>` onde aplicável
- [ ] `<button>` pra ações (abrir modal, submit, toggle), `<a href>` pra navegação
- [ ] FAQ usa `<details><summary>` nativo (teclado-acessível sem JS)

### Texto alternativo e labels
- [ ] Todo `<img>` tem `alt` descritivo (ou `alt=""` se for puramente decorativo)
- [ ] Todo `<button>` com ícone sem texto tem `aria-label`
- [ ] Todo ícone decorativo tem `aria-hidden="true"`
- [ ] Links têm texto descritivo (nunca "clique aqui", "saiba mais" genérico — use "Read the full derm breakdown", "See all 500 reviews")
- [ ] `<label>` associado a `<input>` via `for`/`id` em qualquer form

### Contraste e cor
- [ ] Contraste texto normal ≥ **4.5:1** (WCAG AA body text)
- [ ] Contraste texto grande (≥18pt ou 14pt bold) ≥ **3:1**
- [ ] Contraste elementos de UI (bordas de input, focus rings) ≥ **3:1**
- [ ] **Cor nunca é o único indicador** de estado (ex: erro não é só vermelho — tem ícone ou texto "Erro:")
- [ ] Liquid tem filtro nativo `color_contrast`: `{{ '#D85C4A' | color_contrast: '#FDFAF4' }}` retorna o ratio — use no designer-accessibility-audit pra validar

### Foco e navegação por teclado
- [ ] `:focus-visible` definido em **todo elemento interativo** com outline visível — ex: `outline: 2px solid var(--c-accent); outline-offset: 3px; border-radius: 4px;`
- [ ] Tab order segue ordem visual (DOM order = reading order)
- [ ] Nenhum elemento interativo escondido atrás de hover-only (tudo acessível via teclado)
- [ ] Modais/drawers prendem foco dentro deles (`aria-modal="true"` + focus trap)

### Movimento e animação
- [ ] `@media (prefers-reduced-motion: reduce)` no final do stylesheet desligando **todas** `transition` e `animation`
- [ ] Auto-play de carrosséis/videos tem botão de pause
- [ ] Nenhuma animação que pisca mais de 3× por segundo (risco de foto-sensibilidade)

### Responsividade
- [ ] Layout funciona em 320px de largura (menor mobile típico)
- [ ] Texto NUNCA fixa em `px` pequenos — use `clamp()` com mínimo ≥ 14px no body
- [ ] Touch targets interativos ≥ **44×44px** em mobile (botões, links tappáveis)
- [ ] Texto permanece legível até `zoom 200%` sem quebrar layout

### Checklist final de validação
1. Abra DevTools → Lighthouse → Accessibility. Score alvo ≥ **95/100**
2. Rode com teclado only (desligue mouse): consegue navegar tudo? acessar todos CTAs?
3. Teste com VoiceOver (Mac: ⌘+F5) ou NVDA (Windows): headings lidos na ordem? labels fazem sentido?
4. Filter cores com `prefers-color-scheme: dark` (se suportar) e `prefers-contrast: high`

## Como invocar specialists

Esta skill **orquestra outras skills**. Sempre use o **Skill tool** pra invocá-las, não tente rodar scripts diretamente. Os nomes exatos são:

| Specialist | Skill name (use no Skill tool) |
|---|---|
| Geração de código frontend | `frontend-design` |
| Sistema de cor | `designer-color-system` |
| Tipografia | `designer-typography-scale` |
| Spacing | `designer-spacing-system` |
| Layout grid | `designer-layout-grid` |
| Design tokens | `designer-design-token` |
| Hierarquia visual | `designer-visual-hierarchy` |
| Responsivo | `designer-responsive-design` |
| Spec de componente | `designer-component-spec` |
| Microinterações | `designer-micro-interaction-spec` |
| Feedback patterns | `designer-feedback-patterns` |
| UX writing | `designer-ux-writing` |
| Critique | `designer-design-critique` |
| Heurísticas | `designer-heuristic-evaluation` |
| Acessibilidade | `designer-accessibility-audit` |
| QA checklist | `designer-design-qa-checklist` |
| **Validação Liquid** | `shopify-plugin:shopify-liquid` |

A validação Liquid é o único specialist crítico do pipeline. Ela é parte do plugin **Shopify AI Toolkit** (instalável via `/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`). Se o membro não tiver o plugin instalado, instrua a instalar antes de prosseguir.

## Ferramentas auxiliares (apenas pra referência visual — Etapa 2.1)

Se o membro passou um site de referência na Etapa 2, essa é a cadeia de scripts Python em `tools/design-clone/`:

| Script | Uso |
|---|---|
| `downloader.py` | Renderiza a página de referência com Playwright e salva HTML/CSS/fontes/imagens em pasta temporária |
| `analyzer.py` | Identifica sections (ignorado no fluxo atual) |
| `pattern-extractor.py` | Extrai `design_system` abstrato (cores, fontes, radius, shadow, density) — **ÚNICO output usado** |

Os outros scripts (`liquid-converter.py`, `preview.py`) existem pra cenários avançados de clone literal, mas **não são usados no fluxo principal da skill**. A skill usa apenas o `design_system` como input adicional pros specialists `designer-color-system` e `designer-typography-scale`.

## Comandos úteis (referência pro membro)

> Estes comandos rodam no terminal **real** do membro (não dentro do `!` do Claude Code, que é não-interativo).

Baixar o tema Shopify (uma vez):
```bash
mkdir -p ~/shopify-theme && cd ~/shopify-theme
shopify theme pull --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
```

Preview ao vivo (durante edição):
```bash
cd ~/shopify-theme
shopify theme dev --store SUA-LOJA.myshopify.com
```

Push pro tema (quando satisfeito):
```bash
cd ~/shopify-theme
shopify theme push --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
```

Substitua `SUA-LOJA.myshopify.com` e `ID-DO-TEMA` pelos valores reais do membro. Pra descobrir o ID:
```bash
shopify theme list --store SUA-LOJA.myshopify.com
```
