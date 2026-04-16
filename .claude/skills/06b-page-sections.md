---
name: page-sections
description: Converte o plano + design system de `page-planning` em arquivos Liquid (sections Shopify). Gera hero (3 variantes → membro escolhe), converte pro padrão de blocks inline no schema, replica pras demais sections, roda UX writing + self-critique (Nielsen + WCAG + QA). Segunda skill da cadeia Page Engine. Invoque depois de `page-planning`.
---

# Page Sections — ETAPAS 4-8

Esta é a **segunda** das 3 skills da cadeia Page Engine modularizada. Ela:

1. Valida que `page-planning` rodou (pre-flight)
2. Gera 3 variantes de hero → membro escolhe → converte pro padrão de blocks inline
3. Explica o **padrão arquitetural** (blocks inline no schema)
4. Replica o padrão pras demais sections do plano
5. Passa UX writing em toda a microcopy
6. Roda self-critique (design critique + heurísticas Nielsen + WCAG + QA checklist)

**Outputs gravados em:**
- `<staging>/sections/page-[produto]-[tipo].liquid` — 1 arquivo Liquid por section
- `/workspace/[produto]/06-page/06-sections-report.md` — relatório das sections geradas

Depois desta skill, rode `page-deploy` pra criar o template JSON e deployar no Shopify.

## Pré-flight

Valide que a skill anterior (`page-planning`) rodou:

- [ ] `/workspace/[produto]/06-page/06-plan.json` existe e é parseável
- [ ] `/workspace/[produto]/06-page/06-design-system.md` existe
- [ ] `/workspace/[produto]/manifest.json` tem `06a-page-planning` em `skills_completed`
- [ ] Dir de staging: `/workspace/[produto]/06-page/staging/sections/` (criar com `mkdir -p` se não existir)
- [ ] Plugin `shopify-plugin:shopify-liquid` disponível (tente invocá-lo em modo dry — se falhar, avise membro e peça `/plugin install shopify-plugin@shopify-plugin`)

Se `06-plan.json` não existir: "Rode `page-planning` primeiro — preciso do plano de sections + design system antes de gerar Liquid."

## Arquitetura — Por que blocks inline no schema

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
- Template JSON (criado pela `page-deploy`) tem section + blocks pré-populados com copy real

**Não use theme blocks em arquivos separados** (`/blocks/*.liquid`) pra esta skill — testamos e o validator do Shopify bloqueia referências dinâmicas via `{% content_for 'block' type: block.type %}`. Blocks inline no schema da section é o padrão que passa.

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

Sempre default `adapt` — é o que evita o bug "imagem quadrada em container vertical com espaço branco" (ver Limitação #5 na seção `Limitações Shopify`).

## ETAPA 4 — Generate Hero Section (3 variantes em paralelo)

A hero é a section mais importante. Gere 3 direções distintas e deixe o membro escolher.

Para cada variante:

1. **Skill `frontend-design`**: gere HTML + CSS (vanilla, não Tailwind) seguindo o design system da `page-planning`, usando a copy real do `05-copy.md`. Inclua:
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

5. Mostre as 3 variantes ao membro. Pergunte: **"Qual variante? A, B, ou C — ou misturar elementos de duas?"**

### Mapeamento ASCII → Liquid (explícito)

Quando o membro responder, use **essa tabela** pra pegar o código certo (evita ambiguidade):

| Letra escolhida | Variante | Liquid gerado |
|---|---|---|
| `A` | Editorial Minimalista | Usa o HTML/CSS gerado na variante A (layout `split-lr`, imagem direita, whitespace generoso) |
| `B` | Centered Bold | Usa o HTML/CSS da variante B (layout `centered`, headline gigante com clamp, CTA em destaque) |
| `C` | Split Full-Bleed | Usa o HTML/CSS da variante C (layout `split-full`, 50/50, imagem full-bleed mobile) |
| `A+B`, `B+C`, etc. | Híbrido | Rode o merge manual — pegue markup de uma, CSS de outra; revalide com `designer-visual-hierarchy` antes de prosseguir |

Armazene `variant_chosen` no report final.

## ETAPA 4.5 — Arquitetura das Sections (blocks universais)

**Antes de converter pra Liquid**, garanta que o template Liquid da hero (ETAPA 5) cobre TODOS os block types universais que possam aparecer no template JSON (ETAPA 9 da `page-deploy`):

**Block types universais (devem ter `{% when 'X' %}` no case):**
- `eyebrow`
- `heading`
- `paragraph`
- `badge`
- `button_row`
- `stats_bar`
- `trust_row`
- `tag` (renderizado separadamente fora do main loop — ver nota no markup canônico)
- `divider`
- `spacer`
- `custom_liquid`
- `custom_html`

**Regra de validação cruzada (OBRIGATÓRIA):**
> Se o template JSON criado pela `page-deploy` (ETAPA 9) usar algum block type que NÃO aparece como `{% when 'X' %}` no Liquid desta section, **ABORTE o fluxo e volte aqui pra adicionar o case no Liquid antes de prosseguir.**

Essa validação cruzada é feita pela `page-deploy` — mas você aqui já deve garantir que o Liquid cobre todos os universais + os type-specific da section (listados abaixo).

## ETAPA 5 — Convert Hero to Liquid Section (padrão de blocks inline)

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

          {# ... outros blocks: paragraph, badge, button_row, stats_bar, trust_row, divider, spacer, custom_liquid, custom_html #}
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

**Ferramenta de ajuda:** `tools/design-clone/liquid-converter.py` gera section boilerplate (cores auto-extraídas, labels semânticos, image controls). Útil como DRAFT — depois você adapta pro padrão de blocks inline descrito aqui. Nunca use o output do converter diretamente na Aura Engine — sempre refatore pro padrão acima. O converter (e o preview.py) compartilham `tools/design-clone/_css_utils.py` (módulo `rewrite_css_for_namespace`) pra rewrite de CSS namespace.

### Validação obrigatória — retry logic explícita

A validação roda via `shopify-plugin:shopify-liquid` com retry deterministic:

**Protocolo (3 tentativas max):**

1. **Tentativa 1 — validate:**
   - Invoque `shopify-plugin:shopify-liquid` em modo `validate`.
   - Se OK → siga pra próxima section.
   - Se erro → vá pro passo 2.

2. **Tentativa 2 — auto-fix + revalidate:**
   - Invoque `shopify-plugin:shopify-liquid` em modo `fix` (auto-fix do plugin).
   - Revalide (modo `validate`).
   - Se OK → siga pra próxima section.
   - Se erro → vá pro passo 3.

3. **Tentativa 3 — leitura manual do erro + ajuste direcionado:**
   - Leia a mensagem de erro, consulte a tabela "Debug — Quando validação falha" abaixo.
   - Aplique o fix sugerido.
   - Revalide.
   - Se OK → siga. Se erro → **ABORTE e reporte ao membro** com:
     - Arquivo afetado
     - Mensagem de erro exata
     - Tentativas já feitas
     - Sugestão de ação manual

**Comando manual (alternativa se o plugin não estiver disponível):**
```bash
node .../shopify-liquid/scripts/validate.mjs --filename page-[produto]-hero.liquid --filetype sections --code "$(cat file)" --model ... --client-name claude-code --artifact-id [produto]-hero --revision 1
```

**Salve em:** `<staging>/sections/page-[produto]-[tipo].liquid`

## Catálogo de Block Types Universais

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

## ETAPA 6 — Generate Remaining Sections

Para cada section do plano (`06-plan.json`) além do hero, aplique o MESMO padrão da Etapa 5: **uma section file com blocks inline no schema** (nunca theme blocks em `/blocks/*.liquid`).

Loop por section:

1. **Skill `frontend-design`**: gera HTML + CSS vanilla seguindo o design system + copy real da section (vem do `05-copy.md`).

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

6. Valide com `shopify-plugin:shopify-liquid` usando o protocolo de retry da Etapa 5.

7. Salve em `<staging>/sections/page-[produto]-[tipo].liquid`.

**Não crie arquivos em `<staging>/blocks/`** pra esta skill. Theme blocks em arquivos separados falham no validator quando renderizados com `{% content_for 'block' type: block.type id: block.id %}` (ver Limitação #12).

## ETAPA 7 — UX Writing Pass

Após gerar todas as sections:

1. **Skill `designer-ux-writing`**: revise toda a microcopy gerada nas settings de:
   - CTAs (deve refletir valor, não ação genérica — "Buy Now" é ruim, "Start Your 30-Day Transformation" é bom)
   - Empty states de placeholders nas settings
   - Alt texts default das imagens
   - Aria labels
   - FAQ wording
2. Aplique as melhorias diretamente nos defaults dos schemas das sections.

## ETAPA 8 — Self-Critique Pass (orquestração de qualidade)

Esta é a etapa que move qualidade de 8/10 pra 9/10. Não pule.

1. **Skill `designer-design-critique`**: critique o conjunto completo de sections geradas. Foque em:
   - Hierarquia visual entre sections
   - Consistência de espaçamento
   - Ritmo da página (a página guia o leitor naturalmente?)
   - Originalidade (foge do padrão genérico de IA?)
2. **Skill `designer-heuristic-evaluation`**: aplica heurísticas de Nielsen.
3. **Skill `designer-accessibility-audit`**: WCAG 2.1 AA full audit em todas as sections (checklist abaixo).
4. **Skill `designer-design-qa-checklist`**: QA final.

5. Compile todas as issues encontradas. Pra cada issue:
   - Identifique a section/block afetado
   - Identifique o fix exato
   - Aplique no código
   - Revalide com `shopify-plugin:shopify-liquid`

6. Se alguma issue não for corrigível sem mudança estrutural significativa, liste pro membro como "issues conhecidas" no relatório final.

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
- Copiar HTML/CSS do site de referência direto pro tema do membro. Referência visual (Etapa 2.1 da `page-planning`) alimenta apenas os specialists de design — o código é sempre gerado do zero via `frontend-design`.

## Debug — Quando validação falha

Quando `shopify-plugin:shopify-liquid` retorna erro, leia a mensagem e aja conforme:

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

## Limitações Shopify conhecidas (referência completa)

Estas regras vêm do validator oficial `shopify-plugin:shopify-liquid` + push pra tema real:

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

11. **Preset de section ≠ blocks em template JSON.** O `presets` do schema da section só popula blocks quando o membro ADICIONA a section manualmente via "Add section" no theme editor. Pra páginas pré-montadas via `templates/page.[produto].json`, os blocks precisam estar **dentro do template JSON** com `blocks: {...}` explícito + `block_order: [...]`. Section entry sem a key `blocks` (ou com `blocks: {}` vazio) renderiza ZERO blocks — esse é o erro mais comum. **A validação desse caso é feita na `page-deploy` ETAPA 9.**

12. **Blocks inline no schema da section** (via `{% case block.type %}`) passa validação. **Theme blocks em arquivos separados** (`/blocks/*.liquid` + `{% content_for 'block' type: block.type id: block.id %}`) FALHA com "The 'id' argument should be a string" — o linter não aceita vars dinâmicas. Sempre use inline.

13. **`inline_richtext` renderiza HTML no browser mas o preview editor pode mostrar raw**. Se o membro editar um stat value como `4.8<span>/5</span>`, o editor do theme mostra o `<span>` literal. Solução: `info` no setting explicando (`"info": "Use <span> for the unit"`). Em runtime renderiza correto.

14. **Custom Liquid em block: use `type: "liquid"` no schema.** Shopify pré-renderiza o código em tempo de theme push. `type: "html"` aceita HTML estático (seguro contra XSS).

15. **Admin API: criar página via CLI não existe.** `shopify page create` não é um comando. O membro precisa criar a página em Admin → Pages → Add page manualmente. A skill entrega theme editor URL direto (`?template=page.[produto]`) que rola sem precisar da página existir antes.

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

## Ferramentas auxiliares (apenas pra referência visual — Etapa 2.1 da `page-planning`)

Se o membro passou um site de referência na `page-planning` Etapa 2, essa é a cadeia de scripts Python em `tools/design-clone/`:

| Script | Uso |
|---|---|
| `downloader.py` | Renderiza a página de referência com Playwright e salva HTML/CSS/fontes/imagens em pasta temporária |
| `analyzer.py` | Identifica sections (ignorado no fluxo atual) |
| `pattern-extractor.py` | Extrai `design_system` abstrato (cores, fontes, radius, shadow, density) — **ÚNICO output usado** |
| `liquid-converter.py` | Gera boilerplate de section (só DRAFT — sempre adaptar pro padrão de blocks inline) |
| `preview.py` | Preview local de section convertida |
| `_css_utils.py` | **Módulo compartilhado** — `rewrite_css_for_namespace()` usado por `liquid-converter.py` e `preview.py` pra namespacing de CSS (single source of truth, evita drift) |

Os scripts `liquid-converter.py` e `preview.py` **não são usados no fluxo principal da skill**. A skill usa apenas o `design_system` como input adicional pros specialists `designer-color-system` e `designer-typography-scale` na `page-planning`.

## Outputs (ao final da skill)

Salve:

- **`<staging>/sections/page-[produto]-[tipo].liquid`** — 1 arquivo por section (hero + demais do plano)
- **`/workspace/[produto]/06-page/06-sections-report.md`** — relatório das sections geradas:
  - Variante de hero escolhida + por quê
  - Lista de arquivos `.liquid` gerados (paths absolutos)
  - Blocks universais + type-specific por section
  - Issues encontradas no self-critique + resoluções
  - Issues conhecidas (se houver)
  - Próximo passo: "Rode `page-deploy` pra criar o template JSON e fazer deploy."

Atualize `/workspace/[produto]/manifest.json` adicionando `06b-page-sections` ao array `skills_completed`.

## Referências cruzadas

- **Skill anterior:** `page-planning` (gera o plano + design system que esta skill consome)
- **Próxima skill:** `page-deploy` (ETAPAS 9-11: template JSON + deploy Shopify + iteration loop)
