---
name: page-engine
description: Engine de geração de páginas Shopify a partir da copy. Usa orquestração de specialists (frontend-design + designer-* skills) pra gerar sections premium, theme-agnostic, 100% editáveis via {% schema %}, validadas com shopify-liquid. Use quando o membro disser "page", "página", "build page", "shopify page", "gerar página", ou após gerar copy e quiser ver no tema.
---

# Page Engine

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

1. **ZERO `custom_liquid` blocks**. Todo elemento visível é uma `setting` no `{% schema %}`. O custom_liquid é proibido — é onde os geradores ruins escondem HTML cru não-editável.
2. **Self-contained CSS**. Todo CSS vai dentro de `{% stylesheet %}` da própria section. Zero dependência de classes/variáveis do tema pai.
3. **Theme-agnostic**. Não use classes do tema pai (`.product-card`, `.btn-primary`, etc). Use namespacing próprio: `.page-[produto]-hero`, `.page-[produto]-feature`.
4. **Mobile-first**. Todo CSS começa pelo mobile e usa media queries pra escalar.
5. **Semantic HTML**. `<section>`, `<article>`, `<header>`, `<h1>-<h6>` na ordem correta, `<button>` pra ações, `<a>` pra navegação, `<picture>`/`<img>` com `alt`.
6. **WCAG 2.1 AA**. Contraste mínimo 4.5:1, focus states visíveis, ARIA quando necessário, alt em todas as imagens.
7. **Validação obrigatória**. Cada arquivo passa pelo skill `shopify-plugin:shopify-liquid` (validate.mjs) antes de ser salvo. Se falhar, corrige e revalida (3 retries).
8. **Zero JS frameworks externos**. Sem React, Vue, jQuery, libraries de animação. Use JavaScript vanilla quando absolutamente necessário, dentro de `{% javascript %}`.
9. **Imagens via `image_picker` setting**, nunca hardcoded ou via `asset_url`. O membro sobe a foto pelo theme editor.
10. **Fluid type e spacing**. Use `clamp(min, preferred, max)` pra tipografia e padding em sections importantes.

## Mapping de Schema (regras de tradução)

Quando converter HTML/CSS pra Liquid section, siga estas regras de tradução de elementos pra settings:

| Elemento HTML | Setting type | Notas |
|---|---|---|
| Texto curto (headline, label, button text) | `text` | |
| Texto longo (parágrafo, descrição) | `richtext` | |
| `<h1>`-`<h6>` | `text` (com select pra nível semântico se relevante) | |
| `<img>` ou `background-image` | `image_picker` | |
| `<a href>` | `url` | Pareie com setting `text` pro label |
| Cor de fundo, texto, accent | `color` | Use CSS custom property: `style="--bg: {{ section.settings.bg }}"` |
| Alinhamento (left/center/right) | `select` ou `text_alignment` | |
| Tamanho (small/medium/large) | `select` ou `range` | |
| Padding/spacing | `range` com `unit: "px"` | |
| Largura máxima | `range` ou `select` | |
| Toggle/visibilidade | `checkbox` | |
| Quantidade | `range` ou `number` | |
| Lista de itens (features, FAQs, steps, testimonials) | **blocks** com schema próprio | Cada item vira um block reorderável |

**Padrões repetíveis SEMPRE viram blocks**, nunca settings duplicadas. Exemplos: features, FAQs, testimonials, pricing tiers, comparison rows, ingredients, steps, badges.

## Fluxo da Skill

### ETAPA 1 — Leitura e Planejamento

1. Leia o `05-copy.md` integralmente. Identifique todas as sections presentes na copy. Tipicamente:
   - Hero
   - Benefícios / Problema
   - Mecanismo Único
   - Prova Social (testimonials, reviews, números)
   - Oferta / Stack
   - Garantia
   - FAQ
   - CTA Final
   - Opcionais: Comparação, Before/After, How it Works, Ingredientes

2. Para cada section identificada, extraia:
   - Nome (slug): `hero`, `benefits`, `mechanism`, `social-proof`, `offer`, `guarantee`, `faq`, `cta-final`
   - Conteúdo textual exato da copy
   - Decisão: section monolítica ou section + blocks repetíveis?
     - Hero, mechanism, guarantee, cta-final → monolíticas
     - Benefits, social-proof, faq, offer (stack items), before-after (pares) → section + blocks

3. Mostre o plano completo pro membro num formato compacto:
   ```
   PLANO DE SECTIONS PRA [produto]:
   1. hero (monolítica) — headline, subheading, CTA, imagem
   2. benefits (section + blocks) — N feature blocks
   3. mechanism (monolítica) — explicação do diferencial
   4. social-proof (section + blocks) — N testimonial blocks
   5. offer (section + blocks) — stack items como blocks
   6. guarantee (monolítica)
   7. faq (section + blocks) — N faq blocks
   8. cta-final (monolítica)
   ```
   
4. Pergunte: "Algum ajuste no plano antes de eu começar?" Aguarde confirmação ou ajustes.

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

### ETAPA 4.5 — Decisão de Arquitetura: Sections ou Blocks?

Antes de converter pra Liquid, decida como os elementos serão estruturados no tema. Duas opções:

**Opção A — Sections independentes (default, clássico)**
- Cada elemento (hero, benefits, mechanism, etc) vira uma section no template
- Ordem fixa no `templates/page.[produto].json`
- Bom pra temas antigos (Dawn, Impulse, Sense)
- Membro edita cada section no theme editor mas **não intercala com sections nativas facilmente**

**Opção B — Theme blocks + container section (RECOMENDADO pra Horizon e temas 2.0+)**
- Cada elemento vira um theme block em `/blocks/page-[produto]-[tipo].liquid`
- Uma container section `/sections/page-[produto]-main.liquid` aceita os blocks + `@theme` + `@app`
- Membro pode: (1) drag-and-drop pra reordenar, (2) duplicar blocks, (3) ocultar individualmente, (4) intercalar com blocks nativos do tema (text, image banner, etc.), (5) adicionar sections nativas antes/depois da container
- Testa e aprovado em Horizon

**Como escolher:**
1. Cheque o tema do membro: `ls [THEME_PATH]/blocks/ | head` — se houver muitos blocks (`_card.liquid`, `_accordion-row.liquid`, etc) é Horizon ou tema moderno → **use Opção B**.
2. Se só tem sections e poucos blocks → Opção A.
3. Na dúvida: Opção B. Horizon é o default do Shopify desde 2024 e funciona em 99% dos temas 2.0+.

Pergunte ao membro apenas se o caso for ambíguo. Caso contrário, decida e siga.

### ETAPA 5 — Convert Hero to Liquid Section

Após escolha do membro:

1. Pegue o HTML/CSS da variante escolhida.
2. **Aplique as regras de Schema Mapping** (ver tabela acima):
   - Cada texto → setting `text` ou `richtext`
   - Cada imagem → setting `image_picker`
   - Cada cor → setting `color` referenciada via CSS custom property
   - Cada link → setting `url`
   - Cada alinhamento/tamanho/spacing → settings configuráveis
3. Gere `{% schema %}` completo com:
   - `name`: "Page [Produto] - Hero"
   - `tag`: "section"
   - `class`: namespace específico
   - `settings`: lista completa de settings com defaults pré-populados da copy
   - `presets`: 1 preset com nome do produto
4. Gere `{% stylesheet %}` self-contained com:
   - CSS custom properties no topo (do design system)
   - Estilos da variante escolhida
   - Mobile-first com media queries
   - `@media (prefers-reduced-motion: reduce)` quando houver animações
5. Gere o markup HTML usando `{{ section.settings.* }}` pra todos os textos/imagens/links/cores.
6. **Valide com o skill `shopify-plugin:shopify-liquid`** (`validate.mjs --filename ... --filetype sections --code ...`).
7. Se a validação falhar:
   - Leia o erro
   - Identifique o problema
   - Corrija o código exato
   - Revalide
   - Máximo 3 retries
8. Se a validação passar, salve em `~/shopify-theme/sections/page-[produto]-hero.liquid` (Opção A) ou `~/shopify-theme/blocks/page-[produto]-hero.liquid` (Opção B).

**Ferramenta de conversão (tools/design-clone/liquid-converter.py):**

Se o membro preferir, pode rodar o converter automaticamente (faz tudo acima em um passo):

```bash
python3 tools/design-clone/liquid-converter.py \
  --html /tmp/fresh-[produto]/hero.html \
  --css /tmp/fresh-[produto]/hero.css \
  --type hero \
  --output ~/shopify-theme/[blocks|sections]/page-[produto]-hero.liquid \
  --blocks-dir ~/shopify-theme/blocks \
  --namespace page-[produto]-hero \
  --product-slug [produto] \
  --asset-type [section|block]
```

O converter faz automaticamente: extração de cores (cada hex vira color setting), labels semânticos BEM (`hero__title` → "Title"), inline_richtext pra texto misto com `<em>`/`<strong>`, image settings com aspect ratio + fit, headers de grupo, sanitização pra validação Shopify. Mesmo assim, sempre valide o output final com `shopify-plugin:shopify-liquid`.

### ETAPA 6 — Generate Remaining Sections

Para cada section restante do plano (etapa 1), repita o processo da etapa 5 mas SEM gerar 3 variantes (uma só, baseada no estilo definido):

Para cada section:

1. **Skill `frontend-design`**: gera HTML/CSS premium pra essa section usando a copy real e o design system.
2. **Specialists relevantes** (chame quando aplicável):
   - `designer-visual-hierarchy` — sempre
   - `designer-responsive-design` — sempre
   - `designer-component-spec` — pra sections com componentes complexos (FAQ accordion, tabs, accordion, carousel)
   - `designer-micro-interaction-spec` — pra hovers, focus states, transições
   - `designer-feedback-patterns` — pra estados de confirmação (botões pressionados, etc)
3. Identifique se a section tem **padrões repetíveis** → vire blocks:
   - Section `benefits` → block `feature` (icon + heading + text)
   - Section `social-proof` → block `testimonial` (quote + author + role + photo)
   - Section `faq` → block `faq_item` (question + answer)
   - Section `offer` → block `stack_item` (label + value + icon)
   - Section `mechanism` (se tiver passos) → block `step` (number + heading + text)
   - Section `before-after` → block `comparison_pair` (before + after images + label)
4. Para cada block identificado:
   - Crie arquivo separado em `~/shopify-theme/blocks/page-[produto]-[block-name].liquid`
   - Inclua `{% doc %}` header com params e exemplo
   - Schema completo com settings + preset
   - Stylesheet self-contained
5. Na section, use `{% content_for 'blocks' %}` pra renderizar os blocks.
6. Schema da section deve listar os tipos de blocks aceitos:
   ```json
   "blocks": [
     { "type": "page-[produto]-feature" }
   ],
   "presets": [
     {
       "name": "...",
       "blocks": [
         { "type": "page-[produto]-feature" },
         { "type": "page-[produto]-feature" },
         { "type": "page-[produto]-feature" }
       ]
     }
   ]
   ```
7. Valida com `shopify-plugin:shopify-liquid` (section + cada block separadamente).
8. Salva em `~/shopify-theme/sections/` e `~/shopify-theme/blocks/`.

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

### ETAPA 9 — Create Page Template

Crie `~/shopify-theme/templates/page.[produto].json`. A estrutura varia pela arquitetura escolhida na Etapa 4.5:

**Se Opção A (sections independentes):**

```json
{
  "sections": {
    "hero": {
      "type": "page-[produto]-hero",
      "settings": { "heading_1": "[da copy]", "paragraph_2": "[da copy]", "link_label_3": "[da copy]" }
    },
    "benefits": {
      "type": "page-[produto]-benefits",
      "settings": {}
    }
  },
  "order": ["hero", "benefits", "mechanism", "proof", "offer", "guarantee", "faq", "cta-final"]
}
```

**Se Opção B (theme blocks + container — recomendada pra Horizon):**

Crie primeiro a container section `~/shopify-theme/sections/page-[produto]-main.liquid`:

```liquid
<div class="page-[produto]-main">
  {% content_for 'blocks' %}
</div>

{% stylesheet %}
.page-[produto]-main { display: flex; flex-direction: column; }
.page-[produto]-main > * { display: block; width: 100%; }
{% endstylesheet %}

{% schema %}
{
  "name": "[Produto] page",
  "tag": "section",
  "settings": [],
  "blocks": [
    { "type": "page-[produto]-hero" },
    { "type": "page-[produto]-trust-bar" },
    { "type": "page-[produto]-benefits" },
    { "type": "page-[produto]-mechanism" },
    { "type": "page-[produto]-proof" },
    { "type": "page-[produto]-offer" },
    { "type": "page-[produto]-guarantee" },
    { "type": "page-[produto]-faq" },
    { "type": "page-[produto]-cta-final" },
    { "type": "@theme" },
    { "type": "@app" }
  ],
  "presets": [{
    "name": "[Produto] page (all blocks)",
    "blocks": [
      { "type": "page-[produto]-hero" },
      { "type": "page-[produto]-trust-bar" },
      { "type": "page-[produto]-benefits" },
      { "type": "page-[produto]-mechanism" },
      { "type": "page-[produto]-proof" },
      { "type": "page-[produto]-offer" },
      { "type": "page-[produto]-guarantee" },
      { "type": "page-[produto]-faq" },
      { "type": "page-[produto]-cta-final" }
    ]
  }]
}
{% endschema %}
```

Então o template JSON vira:

```json
{
  "sections": {
    "[produto]_main": {
      "type": "page-[produto]-main",
      "blocks": {
        "hero": { "type": "page-[produto]-hero", "settings": {} },
        "trust_bar": { "type": "page-[produto]-trust-bar", "settings": {} },
        "benefits": { "type": "page-[produto]-benefits", "settings": {} },
        "mechanism": { "type": "page-[produto]-mechanism", "settings": {} },
        "proof": { "type": "page-[produto]-proof", "settings": {} },
        "offer": { "type": "page-[produto]-offer", "settings": {} },
        "guarantee": { "type": "page-[produto]-guarantee", "settings": {} },
        "faq": { "type": "page-[produto]-faq", "settings": {} },
        "cta_final": { "type": "page-[produto]-cta-final", "settings": {} }
      },
      "block_order": ["hero", "trust_bar", "benefits", "mechanism", "proof", "offer", "guarantee", "faq", "cta_final"],
      "settings": {}
    }
  },
  "order": ["[produto]_main"]
}
```

**Pré-popule os settings com a copy real** só quando necessário. Os defaults já estão no schema de cada block/section — geralmente o JSON pode deixar `settings: {}` e herdar os defaults.

Valide o JSON contra o schema do Shopify (a skill `shopify-plugin:shopify-liquid` cobre isso indiretamente — se os arquivos individuais validam, o template deve funcionar).

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
   # Opção B (blocks):
   cp ~/shopify-theme-[produto]-out/blocks/page-[produto]-*.liquid ~/shopify-theme-[produto]/blocks/
   cp ~/shopify-theme-[produto]-out/sections/page-[produto]-main.liquid ~/shopify-theme-[produto]/sections/
   cp ~/shopify-theme-[produto]-out/templates/page.[produto].json ~/shopify-theme-[produto]/templates/

   # Opção A (sections):
   cp ~/shopify-theme-[produto]-out/sections/page-[produto]-*.liquid ~/shopify-theme-[produto]/sections/
   cp ~/shopify-theme-[produto]-out/templates/page.[produto].json ~/shopify-theme-[produto]/templates/
   ```

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

1. **Arquitetura usada** (Opção A sections / Opção B blocks) + justificativa.
2. **Lista de arquivos criados** (paths absolutos).
3. **Preview links** (theme editor + storefront com `?view=`).
4. **Como subir pra produção** (quando satisfeito):
   ```
   # Publica a cópia como tema live (substitui o atual):
   shopify theme publish --theme [NEW-ID] --store [LOJA].myshopify.com
   ```
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

### SALVAR

Salve um relatório completo em `/workspace/[produto]/06-page.md` contendo:

- Plano de sections gerado (etapa 1)
- Brand discovery answers (etapa 2) — incluindo se usou referência visual e qual
- Design system completo (etapa 3) — paleta, tipografia, spacing, breakpoints
- Variante de hero escolhida + por quê (etapa 4)
- Lista de arquivos criados (etapa 10)
- Settings expostos por section (etapa 10)
- Issues conhecidas (se houver)
- Histórico de iterações (etapa 11) — atualize a cada refinement

Ao final diga:

> "Page-engine completo. Próximo passo: rode `shopify theme dev` pra ver ao vivo, ou diga 'creatives' pra gerar briefings de criativos pra ads, ou 'scale' pra estratégia de escala."

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

## DO NOT

NUNCA, em hipótese alguma:

- Use blocks tipo `custom_liquid` (proibido — quebra a editabilidade)
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
