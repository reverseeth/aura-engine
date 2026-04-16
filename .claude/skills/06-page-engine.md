---
name: page-engine
description: Engine de construção de páginas Shopify em dois modos — Modo A aplica a copy da skill 05 no tema atual gerando sections premium theme-agnostic, Modo B clona o design de um concorrente usando Playwright + BeautifulSoup e converte em Liquid sections editáveis. Use quando o membro disser "page", "página", "shopify page", "build page", "clonar design", "clone page", ou após a copy estar pronta. A skill pergunta qual modo usar e orquestra toda a execução.
---

# Page Engine

## Quando Usar

Quando o membro tem copy pronta (skill 05) e precisa publicar a página na loja Shopify. A skill opera em DOIS MODOS distintos e o membro escolhe qual usar:

- **Modo A — Aplicar copy no tema atual:** gera sections Liquid premium a partir da copy (fluxo clássico)
- **Modo B — Clonar design de concorrente:** baixa o HTML/CSS renderizado de uma página que o membro gostou, identifica as seções visualmente (hero, features, testimonials, FAQ), converte em Liquid sections editáveis substituindo os textos/imagens do concorrente por variáveis, e aplica a copy da skill 05 nessas variáveis

A página vem ANTES dos criativos no fluxo do Aura Engine — não faz sentido criar ads pra uma página que ainda não existe.

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

> "Quer aplicar a copy no seu tema atual (Modo A) ou clonar o design de um concorrente que você gostou (Modo B)?
> 
> - Modo A — eu gero sections Liquid do zero baseadas na copy e no estilo que você escolher
> - Modo B — você me manda um ou mais links de concorrentes, eu baixo o design renderizado, identifico as seções, e converto em Liquid sections editáveis com sua copy aplicada"

Conforme a resposta, vá para a seção apropriada abaixo. **Se for Modo B**, também pergunte logo em seguida: "Manda os links dos concorrentes que você quer clonar. Pode ser 1 ou vários."

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

# MODO B — Clonar Design de Concorrente

### Etapa B1 — Coletar Links

Já capturado na seleção de modo. Salve a lista de URLs na variável `COMPETITOR_URLS`.

### Etapa B2 — Validar Dependências

Verifique se Playwright + BeautifulSoup estão instalados:

```bash
python3 -c "import playwright, bs4" 2>&1
```

Se falhar: "Faltam dependências pra clonar design. Rode no terminal:
```
pip install playwright beautifulsoup4
playwright install chromium
```
Depois rode `page` de novo."

### Etapa B3 — Download da Página Renderizada

Pra cada URL em `COMPETITOR_URLS`, chame o módulo downloader:

```bash
python3 tools/design-clone/downloader.py "URL" "/tmp/clone-[produto]-[N]"
```

O downloader (documentado em `tools/design-clone/downloader.py`):
- Usa Playwright pra renderizar JS (sem isso, muitos sites ficam vazios)
- Faz scroll automático pra trigger lazy loading (tem imagens/seções que só carregam quando entram no viewport)
- Aguarda network idle
- Captura HTML final, CSS computado de cada elemento, fontes usadas, URLs de imagens
- Salva tudo em pasta temporária:
  - `page.html` — HTML renderizado
  - `styles.css` — CSS consolidado
  - `images/` — imagens baixadas
  - `fonts.json` — fontes detectadas
  - `viewport-screenshot.png` — screenshot pra referência visual

### Etapa B4 — Análise de Seções

Chame o analyzer:

```bash
python3 tools/design-clone/analyzer.py "/tmp/clone-[produto]-[N]"
```

O analyzer (documentado em `tools/design-clone/analyzer.py`):
- Lê `page.html` + `styles.css`
- Identifica seções semanticamente usando:
  - Tags semânticas (`<section>`, `<header>`, `<footer>`)
  - Classes comuns de ecommerce (`hero`, `features`, `benefits`, `testimonials`, `faq`, `pricing`, `footer`)
  - Heurísticas baseadas em conteúdo (H1+imagem+CTA = hero; lista de cards iguais = features)
  - Padrões de layout (full-bleed com background = hero; grid de 3-4 colunas = features)
- Pra cada seção detectada, extrai:
  - HTML da seção
  - CSS que aplica (computed styles dos elementos dentro)
  - Imagens referenciadas
  - Tipo semântico (hero/features/testimonials/faq/etc)
- Retorna `sections.json` com lista de seções identificadas + metadados

### Etapa B5 — Membro Seleciona Seções

Apresente ao membro:

> "Identifiquei [N] seções na página do concorrente:
> 1. [Tipo semântico] — [descrição curta: 'Hero com imagem à direita, headline grande, 2 CTAs']
> 2. ...
> 
> Quais você quer clonar? (pode dizer 'todas', 'só 1, 3 e 5', ou descrever)"

Salve a seleção em `SELECTED_SECTIONS`.

### Etapa B6 — Conversão pra Liquid

Pra cada seção em `SELECTED_SECTIONS`, chame o converter:

```bash
python3 tools/design-clone/liquid-converter.py \
  --section "[caminho do JSON da seção]" \
  --output "~/shopify-theme/sections/page-[produto]-[tipo].liquid" \
  --namespace "page-[produto]" \
  --product-slug "[produto]"
```

O converter (documentado em `tools/design-clone/liquid-converter.py`):
- Recebe HTML+CSS de uma seção
- Converte pra Liquid:
  - Textos fixos → `{{ section.settings.heading }}`, `{{ section.settings.subheading }}`, etc
  - Imagens do concorrente → `{{ section.settings.image | image_url }}` (placeholder até o membro subir)
  - Cores hardcoded → CSS custom properties referenciadas via settings `color`
  - Links → `{{ section.settings.cta_url }}`
- Gera `{% schema %}` completo com settings + presets pré-populados com a copy do `05-copy.md`
- Namespace classes (remove qualquer classe do tema pai, aplica `.page-[produto]-*`)
- Remove JS inline e libraries externas (React, Vue, jQuery se houver)
- Remove tracking scripts, analytics, pixels do concorrente
- Para padrões repetíveis (cards, testimonials, FAQ items) gera `blocks/page-[produto]-[nome].liquid` separado
- Valida o arquivo final com skill `shopify-plugin:shopify-liquid` (3 retries)
- Salva `.liquid` pronto pra instalar

### Etapa B7 — Install no Tema

1. Confirme com membro: "Vou instalar [N] sections + [M] blocks no teu tema em `THEME_PATH`. Ok?"
2. Copie os arquivos `.liquid` gerados pra `~/shopify-theme/sections/` e `~/shopify-theme/blocks/`
3. Cria `~/shopify-theme/templates/page.[produto].json` com as sections clonadas na ordem do concorrente + settings pré-populados com copy
4. Se o membro tiver múltiplos concorrentes, mescle: por default, mantém ordem do primeiro concorrente; seções dos outros são adicionadas ao final ou substituem equivalentes se o membro escolher "usar hero do concorrente A + features do B"

### Etapa B8 — Apply Copy

Pra cada setting que tem texto, cole o texto correspondente do `05-copy.md`:
- Hero headline → `{{ section.settings.heading }}` recebe o hero headline da copy
- Benefits bullets → cada block `feature` recebe um benefit
- FAQ → cada block `faq_item` recebe uma pergunta/resposta
- etc

Se o concorrente tiver mais seções que a copy, as extras ficam com placeholder ("Add your text here"). Se a copy tiver mais seções que o concorrente, as extras precisam ser geradas via Modo A (avise o membro).

### Etapa B9 — UX Writing + Critique

Mesmo fluxo do Modo A (Etapa A7 + A8): ux-writing pass, design-critique, heuristic-evaluation, accessibility-audit, QA checklist.

### Etapa B10 — Report

Mostre:
- Sections clonadas + paths
- Blocks gerados + paths
- Template JSON criado
- Mapeamento copy → settings (qual texto da copy foi pra qual setting)
- Seções que ficaram com placeholder (precisam copy adicional ou skip)
- Issues conhecidas
- Como visualizar, editar, e subir

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
- No Modo B: manter tracking scripts, analytics, ou pixels do concorrente
- No Modo B: manter classes do tema do concorrente (aplicar namespacing próprio sempre)
- No Modo B: copiar código de frameworks (React/Vue/jQuery) — converter pra vanilla ou pular o elemento

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
