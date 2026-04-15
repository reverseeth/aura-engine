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

## Antes de Começar

### 0. Pesquisa exploratória na base Aura

Consulte a base Aura extensivamente sobre: 15 fatores da estrutura de funil (framework que diagnostica PDPs e LPs), landing pages que convertem (Empathy/Trust/Offer, NESP framework), 10x page plan (Copy School framework completo), advertorials (propósito, listicles, 7-section blueprint), checkout optimization (frictionless, trust badges, bumps, savings display), profit optimization (pricing, bundles, AOV builders), hero sections (5 tipos e critérios de seleção), congruência ad→page (message match, visual match, promise match), 4 decision making modalities (Spontaneous/Competitive/Humanistic/Methodical — toda página deve servir os 4 simultaneamente), behavioral psychology (System 1 vs System 2, above-the-fold triggers), CTAs como call to VALUE, crossheads e estrutura visual, wireframing e validação de web copy, proof stacking (Hopkins specificity + social proof volume + authority markers), e qualquer framework adjacente que apareça. Aprofunde em cada sub-conceito até ter domínio completo de conversão + estrutura de página.

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

### ETAPA 3 — Generate Design System (orquestração)

Antes de gerar qualquer section, defina o sistema de design completo. Invoque os specialists nessa ordem:

1. **Skill `designer-color-system`**: gere paleta de 5-7 cores (background, surface, foreground, primary, accent, muted, border) baseada no estilo + cores da marca. Saída: hex codes + role semântico.

2. **Skill `designer-typography-scale`**: gere modular type scale (recomendado 1.25 ou 1.333) com 6 níveis (h1-h6) + body + small. Use fluid type com `clamp()`. Sugira heading font + body font (system fonts ou Google Fonts populares).

3. **Skill `designer-spacing-system`**: gere spacing tokens em base 4px ou 8px (xs, sm, md, lg, xl, 2xl, 3xl).

4. **Skill `designer-layout-grid`**: defina container max-width (recomendado 1200-1440px), grid system, breakpoints (mobile 480, tablet 768, desktop 1024, wide 1440).

5. **Skill `designer-design-token`**: consolide tudo em um conjunto de CSS custom properties que serão injetadas via `:root` no `{% stylesheet %}` de cada section.

6. Salve o design system gerado em `/workspace/[produto]/10-design-system.md` como referência. Mostre ao membro um resumo compacto e peça aprovação rápida.

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
8. Se a validação passar, salve em `~/shopify-theme/sections/page-[produto]-hero.liquid`.

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

1. Crie `~/shopify-theme/templates/page.[produto].json` que junta todas as sections na ordem certa.

2. Estrutura do JSON:
   ```json
   {
     "sections": {
       "hero": {
         "type": "page-[produto]-hero",
         "settings": {
           "heading": "[da copy]",
           "subheading": "[da copy]",
           "cta_label": "[da copy]"
         }
       },
       "benefits": {
         "type": "page-[produto]-benefits",
         "blocks": {
           "feature-1": {
             "type": "page-[produto]-feature",
             "settings": { "title": "[copy]", "description": "[copy]" }
           },
           "feature-2": { ... }
         },
         "block_order": ["feature-1", "feature-2", ...],
         "settings": {}
       },
       ...
     },
     "order": ["hero", "benefits", "mechanism", "social-proof", "offer", "guarantee", "faq", "cta-final"]
   }
   ```

3. **Pré-popule TODOS os settings com a copy real** do 05-copy.md. O membro NÃO deve ter que digitar nada — só ajustar visualmente no theme editor.

4. Valide o JSON contra o schema do Shopify (a skill `shopify-plugin:shopify-liquid` cobre isso indiretamente — se as sections individuais validam, o template deve funcionar).

5. Salva.

### ETAPA 10 — Report

Mostre ao membro:

1. **Lista de arquivos criados** (paths absolutos):
   ```
   Sections:
   - ~/shopify-theme/sections/page-[produto]-hero.liquid
   - ~/shopify-theme/sections/page-[produto]-benefits.liquid
   ...
   
   Blocks:
   - ~/shopify-theme/blocks/page-[produto]-feature.liquid
   - ~/shopify-theme/blocks/page-[produto]-faq-item.liquid
   ...
   
   Template:
   - ~/shopify-theme/templates/page.[produto].json
   ```

2. **Como visualizar localmente** (rodar em terminal interativo, fora do `!`):
   ```
   cd ~/shopify-theme
   shopify theme dev --store [domain].myshopify.com
   ```
   Acesse: `http://127.0.0.1:9292/pages/[produto]`
   
   Nota: o membro precisa criar a página em Admin → Online Store → Pages → Add page, e selecionar o template `page.[produto]` na sidebar.

3. **Como editar pelo theme editor**:
   - Admin → Online Store → Themes → Customize
   - Pages → [produto]
   - Cada section/block tem todas as settings expostas

4. **Como subir as mudanças** (rodar em terminal real):
   ```
   shopify theme push --store [domain].myshopify.com --theme [theme-id]
   ```

5. **Settings expostos por section** (resumo compacto):
   ```
   hero — 12 settings (heading, subheading, eyebrow, cta_label, cta_link, image, ...)
   benefits — 4 settings + N feature blocks
   ...
   ```

6. **Issues conhecidas** (se houver da etapa 8).

### ETAPA 11 — Iteration Loop

Termine perguntando: 

> "Página gerada e validada. Quer ajustar algo? Pode pedir coisas como: 'hero muito apertado, mais ar', 'cores mais escuras', 'features em 2 colunas em vez de 3', 'adicionar countdown na oferta'. Vou refinar sem regenerar tudo do zero."

Para ajustes futuros:
- Mudanças de spacing/layout → edite o `{% stylesheet %}` da section afetada
- Mudanças estruturais → adicione/remova settings + blocks
- Mudanças de copy → atualize os defaults no schema E os pré-populados no template JSON
- **Sempre** revalide com `shopify-plugin:shopify-liquid` após qualquer mudança

### SALVAR

Salve um relatório completo em `/workspace/[produto]/10-page.md` contendo:

- Plano de sections gerado (etapa 1)
- Brand discovery answers (etapa 2)
- Design system completo (etapa 3) — paleta, tipografia, spacing, breakpoints
- Variante de hero escolhida + por quê (etapa 4)
- Lista de arquivos criados (etapa 10)
- Settings expostos por section (etapa 10)
- Issues conhecidas (se houver)
- Histórico de iterações (etapa 11) — atualize a cada refinement

Ao final diga:

> "Page-engine completo. Próximo passo: rode `shopify theme dev` pra ver ao vivo, ou diga 'creatives' pra gerar briefings de criativos pra ads, ou 'scale' pra estratégia de escala."

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
