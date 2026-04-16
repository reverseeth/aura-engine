---
name: page-engine
description: Engine de construção de páginas Shopify em dois modos — Modo A aplica a copy da skill 05 no tema atual gerando sections premium theme-agnostic, Modo B (híbrido) baixa um concorrente, extrai padrões estruturais + design signals (cores, fontes, layout, spacing) e gera um design NOVO inspirado no visual — sem copiar código — com sections Liquid editáveis. Use quando o membro disser "page", "página", "shopify page", "build page", "clonar design", "clone page", ou após a copy estar pronta. A skill pergunta qual modo usar e orquestra toda a execução.
---

# Page Engine

## Quando Usar

Quando o membro tem copy pronta (skill 05) e precisa publicar a página na loja Shopify. A skill opera em DOIS MODOS distintos e o membro escolhe qual usar:

- **Modo A — Aplicar copy no tema atual:** gera sections Liquid premium a partir da copy (fluxo clássico, do zero baseado no estilo que o membro escolher)
- **Modo B — Clone híbrido (estrutura + design fresh):** baixa o HTML/CSS renderizado de um concorrente que o membro gostou, extrai APENAS os padrões estruturais (tipos de section, layout, slots de conteúdo) e os sinais de design (cores dominantes, famílias tipográficas, border radius, shadows, densidade de spacing) — e então GERA UM DESIGN NOVO inspirado naquele visual. Não copia o código do concorrente. Cada section é limpa, moderna, theme-agnostic, e totalmente editável via theme editor.

A página vem ANTES dos criativos no fluxo do Aura Engine — não faz sentido criar ads pra uma página que ainda não existe.

**Por que Modo B é híbrido e não clone literal:** clone literal do HTML do concorrente herda todos os problemas do código deles — web components específicos do tema Dawn/Horizon que não funcionam em outros temas, fontes de CDN que quebram fora do contexto original, JS custom que depende de libraries específicas, classes que colidem com o tema do membro. O resultado é sempre algo "quebrado" visualmente. A abordagem híbrida resolve isso: extrai *o que funciona* (estrutura semântica + design system) e gera *fresh* a partir disso, preservando a vibe visual sem herdar o bloat.

## Antes de Começar

### 0. Pesquisa exploratória na base Aura

Consulte a base Aura extensivamente sobre: 15 fatores da estrutura de funil (framework que diagnostica PDPs e LPs), landing pages que convertem (Empathy/Trust/Offer, NESP framework), 10x page plan (Copy School framework completo), advertorials (propósito, listicles, 7-section blueprint), checkout optimization (frictionless, trust badges, bumps, savings display), profit optimization (pricing, bundles, AOV builders), hero sections (5 tipos e critérios de seleção), congruência ad→page (message match, visual match, promise match), 4 decision making modalities (Spontaneous/Competitive/Humanistic/Methodical — toda página deve servir os 4 simultaneamente), behavioral psychology (System 1 vs System 2, above-the-fold triggers), CTAs como call to VALUE, crossheads e estrutura visual, wireframing e validação de web copy, proof stacking (Hopkins specificity + social proof volume + authority markers), e qualquer framework adjacente que apareça. Aprofunde em cada sub-conceito até ter domínio completo de conversão + estrutura de página. Esses frameworks também guiam QUAIS elementos manter/adaptar no Modo B quando converte HTML de concorrente pra Liquid.

### 1. Detectar o produto

A skill precisa saber qual produto está sendo trabalhado. Detecte assim:

1. Se o membro mencionou o produto explicitamente ("page para [nome-do-produto]"), use o slug exato.
2. Caso contrário, liste os produtos disponíveis em `/workspace/` (cada subpasta é um produto):
   - Se tiver apenas 1 produto → use ele automaticamente, mas confirme: "Vou gerar a página pro produto X. Confirma?"
   - Se tiver múltiplos produtos → mostre lista numerada e peça pro membro escolher
   - Se não tiver nenhum produto → diga: "Não encontrei produtos no workspace. Rode primeiro `setup` ou `product research` pra criar a estrutura."
3. Salve o slug do produto numa variável PRODUTO que será usada em todos os paths daqui pra frente.

### 2. Ler inputs obrigatórios

1. OBRIGATÓRIO: leia `/workspace/[produto]/05-copy.md`.
   - Se não existir, pergunte: "Não achei a copy desse produto. Quer rodar `copy` primeiro (recomendado), ou colar a copy direto no chat agora?"
2. Leia `/workspace/[produto]/04-offer.md` se existir (preço, stack, guarantee — vai pra section de oferta)
3. Leia `/workspace/[produto]/02-market-research.md` se existir (awareness level, voice of customer)
4. Leia `/workspace/profile.md` se existir

### 3. Detectar o tema Shopify local

1. Cheque os locais padrão na ordem:
   - `~/shopify-theme/`
   - `~/shopify-theme/<nome-da-loja>/`
   - Diretório atual se tiver `sections/`, `templates/`, `config/`
   - Variável de ambiente `$SHOPIFY_THEME_PATH` se existir
2. Verifique se a estrutura é válida (precisa ter `sections/`, `blocks/`, `templates/`, `config/`).
3. Se não encontrar, peça ao membro:
   > "Não achei seu tema Shopify baixado. Onde ele está? Se ainda não baixou, rode num terminal real (não no `!`):
   > 
   > ```
   > mkdir -p ~/shopify-theme && cd ~/shopify-theme
   > shopify theme pull --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
   > ```
   > 
   > Depois me passa o caminho ou roda `page` de novo."
4. Salve o path numa variável THEME_PATH.

## Seleção de Modo

Pergunte ao membro numa mensagem só:

> "Quer aplicar a copy no seu tema atual (Modo A) ou usar um concorrente como inspiração visual (Modo B)?
>
> - **Modo A** — eu gero sections Liquid do zero, baseadas na sua copy e num estilo visual que você escolhe (minimalist, bold, clinical, wellness, ou custom)
> - **Modo B — Clone híbrido** — você me manda um link de concorrente que gostou do visual, eu analiso a estrutura (quais sections ele usa, o layout de cada uma) e o design system (cores, fontes, spacing, radius, shadows), e gero sections novas inspiradas naquele visual, com sua copy aplicada. Não é cópia do código — é design fresh com a vibe que você curtiu."

Conforme a resposta, vá para a seção apropriada abaixo. **Se for Modo B**, também pergunte logo em seguida: "Manda o link do concorrente. Pode ser 1 ou vários."

## Princípios Inegociáveis (aplicam a AMBOS os modos)

1. ZERO `custom_liquid` blocks. Todo elemento visível é uma `setting` no `{% schema %}`.
2. Self-contained CSS. Todo CSS vai dentro de `{% stylesheet %}` da própria section.
3. Theme-agnostic. Não use classes do tema pai. Use namespacing próprio: `.page-[produto]-hero`, `.page-[produto]-feature`.
4. Mobile-first.
5. Semantic HTML.
6. WCAG 2.1 AA. Contraste mínimo 4.5:1, focus states visíveis, ARIA quando necessário.
7. Validação obrigatória via skill `shopify-plugin:shopify-liquid` (validate.mjs). Se falhar, corrija (3 retries máximo).
8. Zero JS frameworks externos.
9. Imagens via `image_picker` setting.
10. Fluid type e spacing via `clamp()`.

## Mapping de Schema (regras de tradução — aplicam a AMBOS os modos)

| Elemento HTML | Setting type | Notas |
|---|---|---|
| Texto curto (headline, label, button text) | `text` | |
| Texto longo (parágrafo, descrição) | `richtext` | |
| `<h1>`-`<h6>` | `text` | |
| `<img>` ou `background-image` | `image_picker` | |
| `<a href>` | `url` | Pareie com setting `text` pro label |
| Cor | `color` | Use CSS custom property |
| Alinhamento | `select` ou `text_alignment` | |
| Tamanho | `select` ou `range` | |
| Padding/spacing | `range` com `unit: "px"` | |
| Toggle/visibilidade | `checkbox` | |
| Lista de itens (features, FAQs, steps, testimonials) | **blocks** | Cada item vira um block reorderável |

Padrões repetíveis SEMPRE viram blocks, nunca settings duplicadas.

---

# MODO A — Aplicar Copy no Tema Atual

### Etapa A1 — Leitura e Planejamento

1. Leia `05-copy.md` integralmente. Identifique todas as sections presentes. Tipicamente:
   - Hero · Benefícios/Problema · Unique Mechanism · Prova Social · Oferta/Stack · Guarantee · FAQ · CTA Final · Opcionais (Comparação, Before/After, How it Works, Ingredientes)

2. Pra cada section identificada, extraia:
   - Nome (slug): `hero`, `benefits`, `mechanism`, `social-proof`, `offer`, `guarantee`, `faq`, `cta-final`
   - Conteúdo textual exato da copy
   - Decisão: section monolítica ou section + blocks repetíveis?

3. Mostre o plano compacto ao membro:
   ```
   PLANO DE SECTIONS PRA [produto]:
   1. hero (monolítica) — headline, subheading, CTA, imagem
   2. benefits (section + blocks) — N feature blocks
   3. mechanism (monolítica)
   4. social-proof (section + blocks)
   5. offer (section + blocks)
   6. guarantee (monolítica)
   7. faq (section + blocks)
   8. cta-final (monolítica)
   ```
   
4. Pergunte: "Algum ajuste no plano antes de começar?"

### Etapa A2 — Brand Discovery (uma mensagem)

Pergunte numa única mensagem:

1. **Estilo visual desejado** (escolha 1 ou descreva custom):
   - Minimalist editorial — off-white, sage/cream, whitespace, refined serif
   - Bold modern — dark backgrounds, large sans-serif, vibrant accent
   - Clinical premium — clean white, navy/gold, data-forward, technical
   - Wellness organic — warm tones, soft curves, hand-drawn touches
   - Custom
2. **Cores da marca** se houver (ou "escolhe pra mim")
3. **Caminhos de assets** (logo, fotos do produto) se tiver
4. **Theme path** (default `~/shopify-theme`)
5. **Handle do produto pro template** (default = slug do produto)

### Etapa A3 — Generate Design System

Invoque specialists:
1. Skill `designer-color-system` — paleta 5-7 cores
2. Skill `designer-typography-scale` — modular scale 1.25 ou 1.333
3. Skill `designer-spacing-system` — base 4px ou 8px
4. Skill `designer-layout-grid` — container max 1200-1440px
5. Skill `designer-design-token` — consolida tudo em CSS custom properties

Salve em `/workspace/[produto]/06-design-system.md`.

### Etapa A4 — Generate Hero (3 variantes em paralelo)

Pra cada variante (A = Editorial minimalista, B = Centered bold, C = Split full-bleed):
1. Skill `frontend-design` — HTML+CSS vanilla
2. Skill `designer-visual-hierarchy` — valida
3. Skill `designer-responsive-design` — mobile-first

Mostre as 3 ao membro e pergunte qual escolher.

### Etapa A5 — Convert Hero to Liquid Section

1. Pegue o HTML/CSS da variante escolhida
2. Aplique Schema Mapping
3. Gere `{% schema %}` com settings + presets
4. Gere `{% stylesheet %}` self-contained
5. Valide com skill `shopify-plugin:shopify-liquid` (3 retries)
6. Salve em `~/shopify-theme/sections/page-[produto]-hero.liquid`

### Etapa A6 — Generate Remaining Sections

Pra cada section restante:
1. Skill `frontend-design` — gera HTML/CSS
2. Specialists relevantes (component-spec, micro-interaction-spec, feedback-patterns)
3. Identifique padrões repetíveis → blocks
4. Pra cada block: arquivo separado em `~/shopify-theme/blocks/`
5. Valide com skill `shopify-plugin:shopify-liquid`
6. Salve

### Etapa A7 — UX Writing Pass

Skill `designer-ux-writing` revisa microcopy (CTAs, placeholders, alt texts, aria labels, FAQ wording).

### Etapa A8 — Self-Critique Pass

1. Skill `designer-design-critique` — critique o conjunto
2. Skill `designer-heuristic-evaluation` — Nielsen
3. Skill `designer-accessibility-audit` — WCAG 2.1 AA
4. Skill `designer-design-qa-checklist` — QA final

Aplique os fixes e revalide.

### Etapa A9 — Create Page Template

Crie `~/shopify-theme/templates/page.[produto].json` juntando todas as sections na ordem correta. Pré-popule todos os settings com a copy real do `05-copy.md` — membro não digita nada.

### Etapa A10 — Report

Mostre lista de arquivos criados (paths absolutos), como visualizar localmente (`shopify theme dev`), como editar pelo theme editor, como subir (`shopify theme push`), settings expostos por section, e issues conhecidas (se houver).

---

# MODO B — Clone Híbrido (estrutura + design fresh)

**Fluxo resumido:** baixa o concorrente → extrai APENAS padrões estruturais + sinais de design → gera HTML fresh por section via `frontend-design` → converte pra Liquid. A copy é sempre sua (do `05-copy.md`). O design herdado é a "vibe" (cores, fontes, layout, density) — não o código.

### Etapa B1 — Coletar Links

Já capturado na seleção de modo. Salve a lista de URLs na variável `COMPETITOR_URLS`.

### Etapa B2 — Validar Dependências

Verifique se Playwright + BeautifulSoup estão instalados:

```bash
python3 -c "import playwright, bs4" 2>&1
```

Se falhar: "Faltam dependências pra clonar design. Rode no terminal:
```
pip install -r tools/design-clone/requirements.txt
playwright install chromium
```
Depois rode `page` de novo."

### Etapa B3 — Download da Página Renderizada

Pra cada URL em `COMPETITOR_URLS`, chame o módulo downloader:

```bash
python3 tools/design-clone/downloader.py "URL" "/tmp/clone-[produto]-[N]"
```

O downloader:
- Usa Playwright pra renderizar JS (sem isso muitos sites ficam vazios)
- Faz scroll automático pra triggerizar lazy loading
- Aguarda network idle
- Captura HTML final, `computed-styles.json` (CSS computado de cada elemento com rect/bbox), fontes, imagens
- Salva em pasta temporária:
  - `page.html` · `styles.css` · `computed-styles.json` · `images/` · `fonts.json` · `viewport-screenshot.png`

Esses artefatos ficam como **referência** e alimentam os próximos passos. Nada desse HTML/CSS vai pra o tema do membro — é só matéria-prima pra extração.

### Etapa B4 — Análise Semântica de Sections

```bash
python3 tools/design-clone/analyzer.py "/tmp/clone-[produto]-[N]"
```

O analyzer detecta as sections da página (hero, features, testimonials, faq, pricing, cta, footer, etc) usando tags semânticas, classes de ecommerce conhecidas, heurísticas de conteúdo (H1+imagem+CTA = hero; grid de 3-4 cards iguais = features) e padrões de layout. Output: `sections.json` com index, tipo semântico, confidence, padrão de repetição, imagens referenciadas, descrição curta.

### Etapa B5 — Extração de Patterns + Design System

Aqui está o coração do Modo B híbrido. Chame o pattern-extractor:

```bash
python3 tools/design-clone/pattern-extractor.py "/tmp/clone-[produto]-[N]"
```

O pattern-extractor (`tools/design-clone/pattern-extractor.py`) lê `sections.json` + `computed-styles.json` e produz `patterns.json` com duas partes:

**1. `design_system`** — signals agregados da página inteira:
- `typography.heading_font` · `typography.body_font` (a fonte mais usada em H1-H3 e a de body)
- `colors.background_primary` · `colors.text_primary` · `colors.accents[]` (top 3 cores vivas ponderadas por área)
- `shape.border_radius_px` · `shape.shadow_style` (none/subtle/medium/large)
- `spacing.density` (tight / medium / generous) · `spacing.avg_padding_px`

**2. `sections[]`** — um pattern por section, com:
- `type` (hero/features/testimonials/faq/pricing/cta)
- `layout` (split-lr / centered-bold / grid-3col / grid-4col / carousel / accordion-stacked / tiers-3col / full-bleed-centered)
- `slots` (o que a section espera como conteúdo: `heading`, `subhead`, `cta_label`, `image`, `features[]`, `testimonials[]`, `faq_items[]`, `pricing_tiers[]` — com `length_hint` e `count`)
- `visual_hints` (imagens, itens repetíveis)
- `description`

**NENHUM** HTML ou CSS do concorrente é carregado adiante. `patterns.json` é theme-agnostic e totalmente abstrato — só descreve *o que tem* e *que cara tem*, não *como tá codado*.

### Etapa B6 — Membro Seleciona Sections

Apresente ao membro de forma compacta, usando o `patterns.json`:

> "Analisei a página. Peguei a vibe visual:
> - Fontes: **[heading_font]** (títulos) + **[body_font]** (corpo)
> - Cores: fundo **[background_primary]** · texto **[text_primary]** · destaques **[accents]**
> - Shape: radius **[border_radius_px]px** · shadow **[shadow_style]**
> - Density: **[density]** (padding médio **[avg_padding_px]px**)
> 
> E identifiquei essas sections:
> 1. **[type]** — layout `[layout]` — [description]
> 2. ...
> 
> Quais você quer usar na sua página? Pode dizer 'todas', '1, 3 e 5', ou descrever."

Salve em `SELECTED_SECTIONS`.

### Etapa B7 — Gerar HTML Fresh por Section (via `frontend-design`)

Pra CADA section em `SELECTED_SECTIONS`, invoque a skill `frontend-design` passando:

1. **Pattern da section** (type, layout, slots) — do `patterns.json`
2. **Design system** (typography, colors, shape, spacing) — do `patterns.json`
3. **Conteúdo real** — trecho correspondente do `05-copy.md` (hero headline, benefit bullets, FAQ items, etc, mapeado ao `type`)
4. **Princípios de Qualidade Visual** desta skill (type scale, fluid clamp, hierarquia, focus states, reduced-motion)
5. **Namespace obrigatório** — `.page-[produto]-[type]`

**Prompt pattern pro frontend-design** (use um por section):

> "Gere HTML + CSS vanilla pra uma section `[type]` com layout `[layout]`. Use este design system (não invente cores nem fontes): bg `[background_primary]`, text `[text_primary]`, accents `[accents]`, heading `[heading_font]`, body `[body_font]`, radius `[border_radius_px]px`, shadow `[shadow_style]`, density `[density]`. Conteúdo: `[trecho da copy]`. Slots a renderizar: `[slots]`. Namespace: `.page-[produto]-[type]`. Mobile-first, fluid type com clamp, sem JS frameworks, self-contained CSS, semantic HTML. Siga os Princípios de Qualidade Visual da skill page-engine."

Isso faz o `frontend-design` produzir código **limpo, moderno, theme-agnostic** que reflete a vibe do concorrente sem herdar o bloat. O membro escolheu inspiração visual; você entregou design fresh.

Se a section tem padrão repetível (`repeating_count > 0`), gere 1 instância do item — o converter vai transformar em block reorderável.

Salve cada HTML/CSS gerado temporariamente em `/tmp/fresh-[produto]/[type].html` e `/tmp/fresh-[produto]/[type].css`.

### Etapa B8 — Converter HTML Fresh pra Liquid

Pra cada section fresh gerada, chame o converter no HTML *limpo que você acabou de gerar* (não o do concorrente):

```bash
python3 tools/design-clone/liquid-converter.py \
  --html "/tmp/fresh-[produto]/[type].html" \
  --css "/tmp/fresh-[produto]/[type].css" \
  --output "[THEME_PATH]/sections/page-[produto]-[type].liquid" \
  --blocks-dir "[THEME_PATH]/blocks/" \
  --namespace "page-[produto]-[type]" \
  --product-slug "[produto]"
```

O converter:
- Mapeia textos → `{{ section.settings.heading_1 }}`, `{{ section.settings.paragraph_2 }}`, etc (nomes semânticos, dedup por tipo+default)
- Imagens → `{{ section.settings.image_N | image_url }}` com `image_picker` setting
- Cores hardcoded → CSS custom properties ligadas a settings `color`
- Links → `{{ section.settings.link_url_N }}` + `link_label_N`
- Padrões repetíveis → `blocks/page-[produto]-[type]-[nome].liquid`
- Gera `{% schema %}` completo com settings + presets pré-populados
- Valida com skill `shopify-plugin:shopify-liquid` (3 retries)

Como o HTML de entrada já é limpo (sem web components Shopify, sem data-attrs de tema, sem scripts de analytics), o output é compacto e editável.

### Etapa B9 — Install + Apply Copy + Template

1. Confirme: "Vou instalar [N] sections + [M] blocks no tema em `[THEME_PATH]`. Ok?"
2. Arquivos já foram escritos em `sections/` e `blocks/` pelo converter.
3. Crie `[THEME_PATH]/templates/page.[produto].json` combinando as sections na ordem escolhida (default = ordem do concorrente; ajustável) e pré-populando TODOS os settings com os textos exatos do `05-copy.md`. O membro não digita nada.
4. Se o membro tem múltiplos concorrentes, ofereça escolha por section ("hero do A + features do B").

### Etapa B10 — UX Writing + Critique + Report

1. Mesmo fluxo do Modo A (A7 + A8): `designer-ux-writing` → `designer-design-critique` → `designer-heuristic-evaluation` → `designer-accessibility-audit` → `designer-design-qa-checklist`.
2. Report final mostra:
   - Modo B híbrido, URLs analisadas, design system extraído
   - Sections geradas (types + layouts + paths)
   - Blocks gerados (paths)
   - Template JSON criado
   - Mapeamento copy → settings
   - Como visualizar (`shopify theme dev`), editar (theme editor), e subir (`shopify theme push`)
   - Issues conhecidas

---

## Etapa Final (comum aos dois modos) — Iteration Loop

Termine:

> "Página gerada e validada. Quer ajustar? Pode pedir 'hero muito apertado, mais ar', 'cores mais escuras', 'features em 2 colunas', 'adicionar countdown'. Vou refinar sem regenerar tudo."

Pra ajustes:
- Spacing/layout → edite `{% stylesheet %}`
- Estruturais → adicione/remova settings + blocks
- Copy → atualize defaults no schema + pré-populados no template JSON
- Sempre revalide com skill `shopify-plugin:shopify-liquid`

## SALVAR

Salve um relatório completo em `/workspace/[produto]/06-page.md` contendo:

- Modo escolhido (A ou B)
- Se Modo B: URLs clonadas + seções selecionadas
- Plano de sections
- Brand discovery answers (se Modo A)
- Design system (se Modo A) ou mapping copy→setting (se Modo B)
- Lista de arquivos criados
- Settings expostos por section
- Issues conhecidas
- Histórico de iterações

## Mensagem Final

> "Page-engine completo. Rode `shopify theme dev` pra ver ao vivo. Próximo passo: diga **'creatives'** pra gerar os briefings de ads que vão levar tráfego pra essa página."

## DO NOT

- Blocks tipo `custom_liquid`
- Hardcode texto/imagens/cores no markup
- Classes do tema pai
- `asset_url` ou paths hardcoded de imagens
- `!important` em CSS
- IDs em selectores CSS
- Libraries externas de JS/CSS
- Pular validação com skill `shopify-plugin:shopify-liquid`
- No Modo B: **copiar HTML/CSS direto do concorrente pro tema do membro** — Modo B é híbrido: extrai patterns + design signals, gera fresh, converte. Nunca joga o código cru dele em Liquid.
- No Modo B: manter tracking scripts, analytics, pixels, web components Shopify do concorrente
- No Modo B: manter classes do tema do concorrente — namespace sempre como `.page-[produto]-[type]`
- No Modo B: usar fontes de CDN específicas do concorrente que podem quebrar fora do contexto — usar a família detectada via sistema (`system-ui`, Google Fonts padrão, ou a font-family nominal)

## Princípios de Qualidade Visual (ground rules pro frontend-design)

- Type scale modular 1.25 ou 1.333
- Fluid type com `clamp()` em headings
- Spacing generoso (5-8rem padding-block em sections importantes)
- Hierarchy clara (h1 muito maior que h2)
- Microinterações sutis (transitions 200-300ms ease-out)
- Container max 1200-1440px
- CSS Grid pra layouts 2D, Flexbox pra 1D
- Custom properties pra tudo editável
- Sombras sutis
- Border radius consistente
- Focus states visíveis
- `@media (prefers-reduced-motion: reduce)` pra animações

## Como invocar specialists

| Specialist | Skill name (use no Skill tool) |
|---|---|
| Frontend code | `frontend-design` |
| Color system | `designer-color-system` |
| Typography | `designer-typography-scale` |
| Spacing | `designer-spacing-system` |
| Layout grid | `designer-layout-grid` |
| Design tokens | `designer-design-token` |
| Visual hierarchy | `designer-visual-hierarchy` |
| Responsive | `designer-responsive-design` |
| Component spec | `designer-component-spec` |
| Microinterações | `designer-micro-interaction-spec` |
| Feedback patterns | `designer-feedback-patterns` |
| UX writing | `designer-ux-writing` |
| Critique | `designer-design-critique` |
| Heurísticas | `designer-heuristic-evaluation` |
| Acessibilidade | `designer-accessibility-audit` |
| QA checklist | `designer-design-qa-checklist` |
| **Validação Liquid** | `shopify-plugin:shopify-liquid` |

Se o plugin Shopify AI Toolkit não estiver instalado: `/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`.

## Comandos úteis (referência pro membro)

> Rodam no terminal real (não no `!` do Claude Code).

Baixar tema Shopify (uma vez):
```bash
mkdir -p ~/shopify-theme && cd ~/shopify-theme
shopify theme pull --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
```

Preview ao vivo:
```bash
cd ~/shopify-theme
shopify theme dev --store SUA-LOJA.myshopify.com
```

Push pro tema:
```bash
cd ~/shopify-theme
shopify theme push --store SUA-LOJA.myshopify.com --theme ID-DO-TEMA
```

Listar temas:
```bash
shopify theme list --store SUA-LOJA.myshopify.com
```
