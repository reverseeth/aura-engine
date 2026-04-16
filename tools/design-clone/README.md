# Design Clone — Aura Engine

Pipeline híbrido que extrai padrões estruturais e design signals de uma página de concorrente e gera sections Shopify Liquid editáveis com design fresh. Usado pela skill `06-page-engine` no Modo B.

**Abordagem híbrida (não clone literal):** baixa → analisa sections → extrai design system (cores, fontes, spacing, radius, shadows) + patterns estruturais (layout, slots de conteúdo). Esses artefatos alimentam a skill `frontend-design`, que gera HTML/CSS fresh. O converter então transforma esse HTML fresh em Liquid. O código do concorrente nunca entra no tema do membro — só a "vibe" visual.

## Pré-requisitos

```bash
pip install -r requirements.txt
playwright install chromium
```

## Pipeline

### 1. `downloader.py` — Baixa a página renderizada

```bash
python3 downloader.py <URL> <output_dir>
```

Renderiza com Playwright (JS executado), faz scroll automático pra trigger lazy loading, aguarda network idle, captura HTML final, CSS computado (`computed-styles.json` com rect/bbox de cada elemento), fontes, imagens, e screenshot. Salva tudo em `<output_dir>`.

### 2. `analyzer.py` — Identifica sections semanticamente

```bash
python3 analyzer.py <output_dir>
```

Lê `page.html` + `styles.css` e identifica sections (hero, features, testimonials, faq, pricing, cta, etc) usando heurísticas de tags semânticas, classes comuns de ecommerce, padrões de conteúdo (H1+imagem+CTA = hero; cards repetidos = features), e padrões de layout. Salva `sections.json` com HTML + metadados + imagens + padrões de repetição de cada section.

### 3. `pattern-extractor.py` — Extrai patterns + design system

```bash
python3 pattern-extractor.py <output_dir>
```

Lê `sections.json` + `computed-styles.json` e produz `patterns.json` abstrato, theme-agnostic, SEM HTML/CSS do concorrente:

- **`design_system`** — signals agregados:
  - `typography.heading_font` / `body_font` (fonte mais usada em H1-H3 e body)
  - `colors.background_primary` / `text_primary` / `accents[]` (top 3 cores vivas ponderadas por área)
  - `shape.border_radius_px` / `shadow_style` (none/subtle/medium/large)
  - `spacing.density` (tight/medium/generous) / `avg_padding_px`
- **`sections[]`** — um pattern abstrato por section:
  - `type` (hero/features/testimonials/faq/pricing/cta)
  - `layout` (split-lr / centered-bold / grid-3col / grid-4col / carousel / accordion-stacked / tiers-3col / full-bleed-centered)
  - `slots` (heading, subhead, cta_label, image, features[], testimonials[], faq_items[] com length_hint e count)
  - `visual_hints`, `description`

Este arquivo é o input pra skill `frontend-design` gerar HTML fresh.

### 4. `frontend-design` (skill, não script) — Gera HTML fresh

Pra cada section em `patterns.json`, a skill 06 invoca `frontend-design` passando o pattern + design_system + conteúdo real do `05-copy.md`. Output: HTML + CSS vanilla moderno, limpo, theme-agnostic, inspirado no visual mas sem o bloat do código original.

### 5. `liquid-converter.py` — Converte HTML fresh em Liquid

```bash
python3 liquid-converter.py \
  --html <fresh_html_path> \
  --css <fresh_css_path> \
  --output ~/shopify-theme/sections/page-<produto>-<tipo>.liquid \
  --blocks-dir ~/shopify-theme/blocks \
  --namespace page-<produto>-<tipo> \
  --product-slug <produto>
```

Converte o HTML fresh em `.liquid` editável:
- Textos fixos viram `{{ section.settings.heading_1 }}`, `{{ section.settings.paragraph_2 }}`, etc (nomes semânticos, dedup por tipo+default)
- Imagens viram `image_picker` settings
- Links viram pares de `text` + `url` settings
- Padrões repetíveis viram `blocks` separados
- Classes namespaced (`.page-<produto>-<tipo>__*`)
- Scripts, tracking, pixels, web components Shopify do concorrente são removidos (mas como o HTML de entrada é fresh, isso raramente é necessário)
- `{% schema %}` completo com defaults pré-populados

**IMPORTANTE:** sempre valide o arquivo gerado com a skill `shopify-plugin:shopify-liquid` antes de instalar no tema.

### 6. `preview.py` — Visualiza o .liquid como HTML standalone

```bash
python3 preview.py \
  --section <path.liquid> \
  --blocks-dir <path> \
  --images-dir <output_dir>/images \
  --images-json <output_dir>/images.json \
  --output /tmp/preview.html
```

Renderiza o `.liquid` como HTML standalone pra visualização no browser. Expande settings com defaults do schema, expande `{% content_for 'blocks' %}` com N instâncias, injeta imagens locais. Útil pra debug antes de subir pro tema.

## Princípios

- **Zero código do concorrente no output:** só design signals agregados e patterns abstratos
- **Design fresh, não cópia:** `frontend-design` gera HTML novo inspirado na vibe
- **Theme-agnostic:** classes e IDs sempre namespaced (`page-<produto>-<tipo>-*`)
- **100% editável:** todo texto/imagem/cor vira setting no theme editor
- **Validação obrigatória:** output do converter passa por `shopify-plugin:shopify-liquid` antes de instalar
