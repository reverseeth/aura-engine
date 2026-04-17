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

### PADRÃO 1 — Color settings devem ser injetadas INLINE no section root (CRÍTICO)

**Problema observado em produção:** gerações anteriores declaravam CSS vars dentro do `{% stylesheet %}` como valores ESTÁTICOS:

```liquid
{% stylesheet %}
  :root {
    --color-primary: #002DD1;  /* ❌ hardcoded, ignora setting */
    --color-bg: #FAFAFA;       /* ❌ hardcoded */
  }
  .section-X__cta { background: var(--color-primary); }
{% endstylesheet %}
```

Isso faz o schema setting `color_primary` aparecer no theme editor MAS a mudança NÃO aplica na página — o CSS continua usando o hex hardcoded. Membro muda a cor, salva, abre preview, cor não muda. Bug silencioso.

**Fix obrigatório:** injetar TODOS os color settings via `style=""` inline no root `<section>`:

```liquid
<section class="section-X section-X-{{ section.id }}"
  style="
    --c-primary: {{ section.settings.color_primary | default: '#002DD1' }};
    --c-bg: {{ section.settings.color_bg | default: '#FAFAFA' }};
    --c-fg: {{ section.settings.color_fg | default: '#231F20' }};
    /* repita pra TODAS as color settings da section */
  "
  aria-labelledby="...">
```

E no stylesheet use `var(--c-primary)` — **SEM** declarar `:root { --c-primary: ... }` estático:

```liquid
{% stylesheet %}
  /* ✅ certo — sem :root redeclaring vars */
  .section-X__cta {
    background: var(--c-primary);
    color: var(--c-bg);
  }
  .section-X__heading { color: var(--c-fg); }
{% endstylesheet %}
```

**Regra:** toda `color` setting exposta no schema TEM que ter um `{{ section.settings.color_X }}` correspondente injetado no style inline do root da section. Mesmo princípio pra `--font-*`, `--radius-*`, `--shadow-*`, `--size-*` quando esses também vierem de settings (ver Padrão 5 — "Everything editable").

**Checklist no self-critique (ETAPA 8):** grep por `:root {` no stylesheet — se aparecer com CSS vars redeclaradas, é bug. Única exceção válida: `:root` definindo constantes que NÃO são settings (ex: `--font-system: -apple-system, sans-serif`).

### ⚠️ PADRÃO 1.5 — CRÍTICO: SEMPRE aplicar `| escape` em valores dentro do `style=""`

**Bug observado em produção (altíssimo impacto):** quando o Liquid renderiza um valor com aspas duplas internas no `style="..."` do `<section>`, o browser interpreta a primeira `"` interna como FECHAMENTO do atributo. TODAS as CSS vars declaradas DEPOIS desse ponto ficam órfãs (undefined).

**Exemplo real que quebrou tudo:**

```liquid
<section style="
  --font-heading: {{ heading_family }};    {# valor: "Playfair Display", Georgia, serif #}
  --radius-md: 12px;
  --shadow-md: 0 4px 12px rgba(...);
">
```

Renderiza:
```html
<section style="--font-heading: "Playfair Display", Georgia, serif; --radius-md: 12px;">
                                 ↑ browser fecha o attribute aqui
```

Resultado: `--radius-md`, `--shadow-md`, e todas as vars restantes NÃO são aplicadas. Página renderiza com bordas retas, shadows ausentes, fontes fallback, etc — tudo silencioso, nenhum erro no console.

**Fix obrigatório:** aplicar `| escape` em TODA interpolação `{{ ... }}` dentro do atributo `style=""`:

```liquid
<section style="
  --font-heading: {{ heading_family | escape }};
  --font-body: {{ body_family | escape }};
  --color-primary: {{ section.settings.color_primary | default: '#002DD1' | escape }};
  --radius-md: {{ section.settings.radius_md | default: 12 }}px;
  --shadow-md: {{ shadow_md | escape }};
">
```

O filtro `| escape` converte `"` → `&quot;`, que o browser decodifica corretamente ao aplicar o CSS.

**Aplique universalmente** em todas interpolações do `style=""`, mesmo que o valor seja numérico (não quebra). É mais seguro blanket-apply do que caso a caso.

**Checklist no self-critique (ETAPA 8):** grep por `style="` no markup e confirmar que cada `{{ ... }}` dentro do atributo tem `| escape`. Se algum não tem, é bug crítico em espera.

### PADRÃO 1.6 — Box-shadows de elevação devem usar `var(--shadow-*)`, NÃO hardcoded

**Bug observado:** gerações declararam `--shadow-sm/md/lg` no style inline mas os stylesheets mantiveram `box-shadow: 0 4px 12px rgba(35,31,32,0.06)` HARDCODED. Resultado: mudar `shadow_intensity` no theme editor não faz nada nas regras com shadow hardcoded.

**Fix:** após criar `--shadow-sm/md/lg`, fazer grep `box-shadow:` em TODOS os stylesheets e migrar:

- Elevação de card/popular tier/guarantee box → `var(--shadow-md)` ou `var(--shadow-lg)`
- Hover elevation → `var(--shadow-md)`
- Inset shadows, focus rings (`0 0 0 3px rgba(accent, 0.3)`) → PODE manter hardcoded (indicator visual, não muda com shadow_intensity)

**Auto-check:** após migration, rodar:

```bash
grep -nE "box-shadow:.*rgba" sections/page-*.liquid | grep -v "var(--shadow" | grep -v "0 0 0 3px"
```

Se retornar qualquer rule de elevação (não-focus-ring) ainda hardcoded, migrar.

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
- Offer → `pricing_tier` (name + price + strap + features richtext + CTA + badge + popular checkbox + image) — ver [Padrão 4](#padrão-4--offer-ctas--padrão-formactioncartadd-nativo) pro CTA funcional
- Guarantee → `promise_item` (title + body + accent color + icon)
- FAQ → `faq_item` (question + answer richtext + open_by_default checkbox)
- Mechanism → `mechanism_card` (tag + value + status + list items — nomeie conforme o mecanismo real do produto, ex: `ingredient_card`, `process_step`, `science_card`)

**Offer section — blocks type-specific adicionais (ver [Padrão 6](#padrão-6--countdown-banner--subscribe--save-como-blocks-especializados)):**

- `countdown_banner` (limit: 1) — urgência legítima com deadline fixo (sale real, drop, launch). Markup com `data-end=""` + vanilla JS `setInterval` no `{% javascript %}`. **⚠️ Compliance Meta/TikTok:** USAR APENAS deadlines fixos reais ou integrados com Shopify sale end (`compare_at_price`). Evitar rolling per-user (cookie 24h fake scarcity) — Meta detecta e desaprova ads. Evitar reset evergreen.
- `pricing_tier` com Subscribe & Save — apps compatíveis: Loop, Recharge, Skio, Seal, Shopify Subscriptions native (grátis). Todos registram selling plan no Shopify; front-end usa mesmo pattern `<input name="selling_plan">` hidden/radio.

**Regra dos 4 headers em TODO bloco** (organização):
1. `Content` — os campos de texto/imagem/url (o QUE mostra)
2. `Style` — cores, tamanhos, variantes, fontes (o COMO mostra)
3. `Spacing` — space_before, space_after (o ONDE fica)
4. `Advanced` — custom_css textarea (o ÚLTIMO recurso pra edição não-coberta)

### PADRÃO 2 — Flexibilidade máxima em ícones (3 camadas obrigatórias)

**Problema observado em produção:** membros em pre-launch raramente têm os ícones "certos" que batem com o preset enum do block. Opções: (a) usar ícone errado, (b) pedir pro membro abrir código e trocar SVG (viola "everything editable"), (c) pular ícone. Nenhuma é boa.

**Fix — todo block com icon deve oferecer 3 níveis de customização:**

**Camada 1 — Preset enum (fast path):**
```json
{ "type": "select", "id": "icon",
  "options": [
    { "value": "none", "label": "No icon" },
    { "value": "shield-check", "label": "Shield (check)" },
    { "value": "package", "label": "Package" },
    { "value": "leaf", "label": "Leaf" },
    { "value": "sparkle", "label": "Sparkle" },
    { "value": "check-circle", "label": "Check circle" },
    { "value": "heart", "label": "Heart" },
    { "value": "star", "label": "Star" }
  ],
  "default": "shield-check"
}
```

**Camada 2 — Custom SVG override (power user):**
```json
{ "type": "textarea", "id": "icon_custom_svg",
  "label": "Custom SVG (overrides icon above)",
  "info": "Paste SVG code. Use viewBox='0 0 24 24' for consistent sizing. stroke='currentColor' to inherit color settings."
}
```

**Camada 3 — Opção `none` (opt-out):** setting `icon` sempre inclui `{ "value": "none", "label": "No icon" }` como **primeira option**. Permite layouts sem ícone (ex: authority block minimalista).

**Markup condicional canônico (ordem de precedência):**

```liquid
{%- if block.settings.icon_custom_svg != blank -%}
  <span class="X__icon-wrap" aria-hidden="true">{{ block.settings.icon_custom_svg }}</span>
{%- elsif block.settings.icon != 'none' -%}
  <span class="X__icon-wrap" aria-hidden="true">
    {%- case block.settings.icon -%}
      {%- when 'shield-check' -%}
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 2l8 3v7c0 5-4 9-8 10-4-1-8-5-8-10V5l8-3z"/>
          <path d="M9 12l2 2 4-4"/>
        </svg>
      {%- when 'package' -%}
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">...</svg>
      {%- when 'leaf' -%}
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">...</svg>
      {# etc pra cada preset do enum #}
    {%- endcase -%}
  </span>
{%- endif -%}
```

**Settings de cor/tamanho do ícone** (sempre expostos junto):
- `icon_color` (color) — usa `currentColor` via `color: {{ block.settings.icon_color }}` no wrapper
- `icon_size` (range 12-48px, step 2, default 20)
- `icon_bg` (color opcional) + `icon_bg_radius` + `icon_padding` se o ícone tiver container circular/rounded

**Racional:** membros em pre-launch podem não ter os ícones "certos" do preset. Custom SVG permite usar brand icons específicos. `None` permite layouts sem ícone. Preset cobre 80% dos casos. Combinação das 3 camadas = flexibilidade total sem pedir ao membro pra editar código.

### Customização máxima — checklist por block

Antes de salvar a section, verifique que CADA bloco tem:
- [ ] TODA cor visível editável (bg, text, border, shadow, dot, underline, ícone interno)
- [ ] TODO tamanho editável (font-size, padding x/y, radius, thickness, gap)
- [ ] Tipografia editável (size, weight, letter-spacing, line-height, transform)
- [ ] Spacing top/bottom por range
- [ ] `custom_css` textarea na aba Advanced
- [ ] Root element tem `id="pu-{{ block.id }}"` pra o CSS ser scoped
- [ ] `<style>#pu-{{ block.id }} { {{ block.settings.custom_css }} }</style>` injetado após o markup

### PADRÃO 5 — "Everything editable" (fonts, radius, shadows, sizes como settings)

Membros experientes querem controle fino. Toda section deve expor como settings:

**Typography group** (agrupe com `{ "type": "header", "content": "Typography" }` no schema):

```json
{ "type": "select", "id": "heading_font_preset",
  "options": [
    { "value": "fraunces", "label": "Fraunces (serif modern)" },
    { "value": "playfair", "label": "Playfair Display (serif classic)" },
    { "value": "dm_serif", "label": "DM Serif Display" },
    { "value": "inter", "label": "Inter (sans)" },
    { "value": "manrope", "label": "Manrope (sans geometric)" },
    { "value": "work_sans", "label": "Work Sans" },
    { "value": "custom", "label": "Custom (set family below)" }
  ],
  "default": "fraunces"
},
{ "type": "text", "id": "heading_font_custom_family",
  "label": "Custom heading font-family",
  "info": "Only used when preset = Custom. Full CSS stack, e.g. 'Playfair Display', Georgia, serif"
}
```

Pra body: mesmo padrão (`body_font_preset` + `body_font_custom_family`).

Mapeie preset pra font-family stack no preamble da section (antes do markup). **USE ASPAS SIMPLES** dentro do valor (ou aspas duplas com cuidado — se duplas, OBRIGATÓRIO aplicar `| escape` ao injetar no style inline, ver Padrão 1.5):

```liquid
{% liquid
  case section.settings.heading_font_preset
    when 'fraunces' ; assign heading_family = "'Fraunces', Georgia, serif"
    when 'playfair' ; assign heading_family = "'Playfair Display', Georgia, serif"
    when 'dm_serif' ; assign heading_family = "'DM Serif Display', Georgia, serif"
    when 'inter' ; assign heading_family = "'Inter', -apple-system, sans-serif"
    when 'manrope' ; assign heading_family = "'Manrope', -apple-system, sans-serif"
    when 'work_sans' ; assign heading_family = "'Work Sans', -apple-system, sans-serif"
    when 'custom' ; assign heading_family = section.settings.heading_font_custom_family
    else ; assign heading_family = "Georgia, serif"
  endcase
%}
```

E injete no style inline do root **SEMPRE COM `| escape`** (obrigatório pra evitar quebra de HTML por aspas internas — ver [Padrão 1.5](#-padrão-15--crítico-sempre-aplicar-escape-em-valores-dentro-do-style)):

```liquid
style="
  --font-heading: {{ heading_family | escape }};
  --font-body: {{ body_family | escape }};
  /* demais vars */
"
```

**Google Fonts loader:** adicione `<link>` no TOPO de cada section (fora do `{% stylesheet %}`) — browser cacheia, deduplica automaticamente entre sections:

```liquid
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..700&family=Inter:wght@400..700&display=swap" rel="stylesheet">
```

**Shape & Sizing group:**

```json
{ "type": "header", "content": "Shape & Sizing" },
{ "type": "range", "id": "radius_sm", "min": 0, "max": 24, "step": 2, "unit": "px", "default": 6 },
{ "type": "range", "id": "radius_md", "min": 0, "max": 32, "step": 2, "unit": "px", "default": 12 },
{ "type": "range", "id": "radius_lg", "min": 0, "max": 48, "step": 2, "unit": "px", "default": 20 },
{ "type": "range", "id": "radius_pill", "min": 0, "max": 1000, "step": 10, "unit": "px", "default": 1000,
  "info": "Use 1000 for fully rounded pills. Step is 10 (Shopify limits to 101 steps — see Limitação #9)" },
{ "type": "select", "id": "shadow_intensity",
  "options": [
    { "value": "none", "label": "None" },
    { "value": "subtle", "label": "Subtle" },
    { "value": "medium", "label": "Medium" },
    { "value": "strong", "label": "Strong" }
  ],
  "default": "subtle"
},
{ "type": "range", "id": "font_size_base", "min": 13, "max": 20, "step": 1, "unit": "px", "default": 16 },
{ "type": "range", "id": "scale_ratio", "min": 115, "max": 150, "step": 5, "default": 125,
  "info": "Typography scale ratio × 100. 125 = 1.25 (Major Third). 133 = Perfect Fourth." }
```

Mapeie `shadow_intensity` pra triple shadows via `case`:

```liquid
{% liquid
  case section.settings.shadow_intensity
    when 'none'
      assign shadow_sm = 'none'
      assign shadow_md = 'none'
      assign shadow_lg = 'none'
    when 'subtle'
      assign shadow_sm = '0 1px 2px rgba(0,0,0,0.04)'
      assign shadow_md = '0 4px 12px rgba(0,0,0,0.06)'
      assign shadow_lg = '0 12px 32px rgba(0,0,0,0.08)'
    when 'medium'
      assign shadow_sm = '0 2px 4px rgba(0,0,0,0.08)'
      assign shadow_md = '0 8px 20px rgba(0,0,0,0.10)'
      assign shadow_lg = '0 20px 48px rgba(0,0,0,0.14)'
    when 'strong'
      assign shadow_sm = '0 4px 8px rgba(0,0,0,0.12)'
      assign shadow_md = '0 12px 28px rgba(0,0,0,0.16)'
      assign shadow_lg = '0 28px 64px rgba(0,0,0,0.22)'
  endcase
%}
```

E injete no style inline **com `| escape`** (ver Padrão 1.5): `--shadow-sm: {{ shadow_sm | escape }}; --shadow-md: {{ shadow_md | escape }}; --shadow-lg: {{ shadow_lg | escape }};`.

**Pro scale_ratio**, divida por 100 no uso: `font-size: calc(var(--font-size-base) * pow({{ section.settings.scale_ratio | divided_by: 100.0 }}, 3))` ou pré-calcule os tamanhos no preamble.

#### ⚠️ Gotcha CRÍTICO — Ao criar setting, MIGRAR TODAS as hardcoded usages no stylesheet

**Bug observado em produção:** agent declarou `--shadow-sm/md/lg` corretamente, injetou inline, expôs como setting. MAS esqueceu de migrar rules existentes no stylesheet que tinham `box-shadow: 0 4px 12px rgba(35,31,32,0.06)` HARDCODED. Resultado: setting aparece no editor, membro muda `shadow_intensity` de "subtle" pra "strong", nada muda visualmente — porque as rules ignoram o CSS var.

**Mesmo bug acontece com radius, font-size, font-family.**

**Protocolo obrigatório ao expor token como setting:**

1. Criar setting no schema
2. Declarar CSS var correspondente no style inline do section root (com `| escape`)
3. **Grep o stylesheet** procurando valores hardcoded do tipo antigo:
   - `grep -n "box-shadow:" | grep -v "var(--shadow"`
   - `grep -nE "border-radius:\s*[0-9]+"`
   - `grep -nE "font-size:\s*[0-9.]+(rem|px)" | grep -v "var(--"`
   - `grep -n "font-family:" | grep -v "var(--font-"`
4. Migrar cada match pra `var(--X)`. EXCEÇÕES permitidas:
   - Focus rings (`0 0 0 3px rgba(accent, 0.3)`) — indicator de foco, não deve mudar com shadow_intensity
   - Mono fonts em contexto específico (ex: molecular info em ingredient cards) — mantém `"SF Mono", monospace`
   - Clamp() em headline fluids — ok manter
5. Re-push e testar no theme editor: mudar setting, confirmar que aplica visual.

**Sem esse passo 3-4, a feature é schema-only (aparece no editor mas não funciona).**

#### ⚠️ Gotcha crítico — text settings com default blank

Shopify REJEITA `{ "type": "text", ..., "default": "" }` com erro `"default can't be blank"`. Pra text settings opcionais (ex: `heading_font_custom_family`), **OMITIR** o key `default` inteiro:

```json
// ❌ Rejected — "default can't be blank"
{ "type": "text", "id": "custom_family", "default": "" }

// ✅ Correct
{ "type": "text", "id": "custom_family" }
```

**Racional:** "everything editable" é filosofia Aura. Membros NÃO sabem CSS, mas SABEM quando querem mudar a fonte, o arredondamento dos cards, ou a sombra. Expor como setting elimina necessidade de editar código.

### PADRÃO 3 — Auditoria de cores por section (evita "cor não editável")

**Problema observado em produção:** gerações iniciais expõem só 4-5 color settings básicos (bg, fg, primary, border). Membros reclamam: "não consigo mudar a cor do savings badge", "a borda do card popular tá fixa", "o strikethrough do preço tá azul e eu quero cinza", etc. Resultado: retrabalho manual em cada pedido de cor nova.

**Fix:** antes de fechar cada section, auditar TODAS as cores visíveis no output e garantir que cada uma tem um color setting próprio no schema. Checklist mínimo por tipo de section:

| Section type | Color settings obrigatórios (mínimo) |
|---|---|
| **Hero** | `color_eyebrow`, `color_heading`, `color_subhead`, `color_cta_bg`, `color_cta_text`, `color_cta_secondary_bg`, `color_cta_secondary_text`, `color_trust_badge_bg`, `color_trust_badge_text`, `color_trust_badge_icon`, `color_bg_top`, `color_bg_bottom`, `color_accent` |
| **Offer / Pricing** | `color_tier_bg`, `color_tier_border`, `color_tier_popular_border`, `color_tier_popular_bg`, `color_tier_name`, `color_price`, `color_price_original` (strikethrough), `color_savings_bg`, `color_savings_text`, `color_popular_badge_bg`, `color_popular_badge_text`, `color_cta_primary_bg`, `color_cta_primary_text`, `color_cta_outline_border`, `color_cta_outline_text`, `color_value_stack_bg`, `color_value_stack_border`, `color_value_stack_item`, `color_value_stack_total` |
| **Social proof** | `color_stat_number`, `color_stat_label`, `color_testimonial_quote`, `color_testimonial_name`, `color_testimonial_meta`, `color_authority_bg`, `color_authority_text`, `color_authority_icon`, `color_avatar_bg`, `color_star_filled`, `color_star_empty` |
| **Comparison table** | `color_table_header_bg`, `color_table_header_text`, `color_row_alt_bg`, `color_border`, `color_highlighted_col_bg`, `color_highlighted_col_border`, `color_sticky_col_bg`, `color_sticky_col_text`, `color_checkmark`, `color_x_mark`, `color_caption` |
| **FAQ** | `color_question_text`, `color_question_bg`, `color_answer_text`, `color_answer_bg`, `color_accordion_border`, `color_accordion_icon`, `color_accordion_icon_hover`, `color_accordion_hover_bg` |
| **Benefits** | `color_card_bg`, `color_card_border`, `color_icon_bg`, `color_icon_fg`, `color_card_title`, `color_card_body`, `color_card_accent` |
| **Mechanism** | `color_tag_bg`, `color_tag_text`, `color_value_text`, `color_status_ok`, `color_status_warn`, `color_list_icon`, `color_list_text`, `color_divider` |
| **Guarantee** | `color_seal_bg`, `color_seal_border`, `color_seal_icon`, `color_seal_title`, `color_seal_body`, `color_accent` |

**Regra:** qualquer elemento que o membro POSSA querer destacar ou harmonizar separadamente → color setting próprio. Média esperada: **15-30 color settings por section**. Não economize aqui.

**Checklist no self-critique (ETAPA 8):** abra a section renderizada, aponte pra CADA cor visível na tela, e confirme que existe setting correspondente no schema. Se não existe, adicione antes de fechar.

## PADRÃO 4 — Offer CTAs: padrão `<form action="/cart/add">` nativo

**Problema observado em produção:** gerações iniciais faziam o CTA do `pricing_tier` como `<a href="...">` exigindo membro colar URL manual tipo `/cart/add?id=X`. Falhas em cascata:
- Não funciona sem JS adicional (GET request vs POST — Shopify add-to-cart espera POST)
- Não dispara Shopify Web Pixel `cart_updated` event
- Meta Pixel perde o `AddToCart` event
- Meta Conversions API, TikTok, Google Analytics, tudo fica cego

**Fix canônico — form nativo com fallback:**

```liquid
{%- if block.settings.variant_id != blank -%}
  <form action="/cart/add" method="post" enctype="multipart/form-data" class="X__form">
    <input type="hidden" name="id" value="{{ block.settings.variant_id }}">
    <input type="hidden" name="quantity" value="{{ block.settings.quantity | default: 1 }}">

    {%- if block.settings.after_add == 'checkout' -%}
      <input type="hidden" name="return_to" value="/checkout">
    {%- elsif block.settings.after_add == 'cart' -%}
      <input type="hidden" name="return_to" value="/cart">
    {%- endif -%}

    {# Subscribe & Save radio buttons (quando aplicável) #}
    {%- if block.settings.subscribe_enabled and block.settings.subscribe_selling_plan_id != blank -%}
      <fieldset class="X__purchase-options">
        <legend class="visually-hidden">Purchase options</legend>
        <label class="X__option">
          <input type="radio" name="selling_plan" value="" checked>
          <span>One-time purchase</span>
        </label>
        <label class="X__option X__option--subscribe">
          <input type="radio" name="selling_plan" value="{{ block.settings.subscribe_selling_plan_id }}">
          <span>
            {{ block.settings.subscribe_frequency_label | default: 'Subscribe & save' }}
            {%- if block.settings.subscribe_badge_text != blank -%}
              <em class="X__save-badge">{{ block.settings.subscribe_badge_text }}</em>
            {%- endif -%}
          </span>
        </label>
      </fieldset>
    {%- endif -%}

    <button type="submit" class="X__cta">{{ block.settings.cta_text }}</button>
  </form>
{%- elsif block.settings.cta_fallback_url != blank -%}
  <a href="{{ block.settings.cta_fallback_url }}" class="X__cta">{{ block.settings.cta_text }}</a>
{%- else -%}
  <button type="button" class="X__cta" disabled>{{ block.settings.cta_text | default: 'Coming soon' }}</button>
{%- endif -%}
```

**Settings obrigatórios no `pricing_tier`:**

| Setting | Type | Notas |
|---|---|---|
| `variant_id` | text | Shopify product variant ID (`shopify.com/admin/products/X/variants/Y` — Y é o ID) |
| `quantity` | range 1-10 step 1 | Default 1 |
| `after_add` | select (checkout / cart / stay) | `checkout` = skip cart, vai direto. `cart` = vai pro carrinho. `stay` = fica na página (drawer abre) |
| `cta_fallback_url` | text | Fallback quando `variant_id` vazio (ex: "Coming soon" linka pra waitlist) |
| `cta_text` | text | Ex: "Add to cart", "Start My Glow", "Buy the Kit" |

**Settings Subscribe & Save (quando aplicável):**

| Setting | Type | Notas |
|---|---|---|
| `subscribe_enabled` | checkbox | Default false |
| `subscribe_selling_plan_id` | text | Selling plan ID gerado pelo app (Loop/Recharge/Skio/Shopify Subscriptions) |
| `subscribe_frequency_label` | text | Ex: "Delivered every 3 months" |
| `subscribe_discount_display` | text | Ex: "15% OFF" |
| `subscribe_badge_text` | text | Ex: "SAVE 15%" |
| `color_subscribe_badge_bg`, `color_subscribe_badge_text`, `color_subscribe_radio_selected`, `color_subscribe_option_bg_selected` | color | Ver [Padrão 3](#padrão-3--auditoria-de-cores-por-section-evita-cor-não-editável) |

**Racional:** forms POST nativos disparam `cart_updated` via Shopify Web Pixel Manager, que propaga automaticamente pro Meta Pixel (se canal Meta instalado), Google Analytics GA4, TikTok, etc. Zero JS custom, zero configuração extra. Tudo o que o membro precisa fazer no theme editor é colar o variant_id — o resto é automático.

## PADRÃO 6 — Countdown banner & Subscribe & Save como blocks especializados

**Countdown banner (offer section, limit: 1):**

Urgência LEGÍTIMA com deadline fixo é conversão honesta. Rolling per-user (fake scarcity) é manipulação que o Meta detecta e pune.

**Settings do block `countdown_banner`:**

| Setting | Type | Notas |
|---|---|---|
| `label_before` | text | Ex: "Offer ends in" |
| `label_expired` | text | Ex: "Offer ended" |
| `end_date` | text | Formato YYYY-MM-DD |
| `end_time` | text | Formato HH:MM (24h) |
| `timezone` | select | US/Eastern, US/Central, US/Mountain, US/Pacific, UTC |
| `show_labels` | checkbox | Mostra "Days / Hours / Min / Sec" abaixo dos dígitos |
| `color_bg`, `color_text`, `color_digits_bg`, `color_digits_text`, `color_labels`, `color_expired_text` | color | |
| `digit_size` | range 24-72px | |
| `padding_y` | range 12-48px | |
| `custom_css` | textarea | |

**Markup canônico:**

```liquid
<div id="pu-{{ block.id }}"
     class="X__countdown"
     data-end="{{ block.settings.end_date }}T{{ block.settings.end_time }}"
     data-tz="{{ block.settings.timezone }}"
     data-expired="false">
  <span class="X__countdown-label">{{ block.settings.label_before }}</span>
  <div class="X__countdown-digits">
    <span><strong data-days>--</strong>{% if block.settings.show_labels %}<em>Days</em>{% endif %}</span>
    <span><strong data-hours>--</strong>{% if block.settings.show_labels %}<em>Hours</em>{% endif %}</span>
    <span><strong data-mins>--</strong>{% if block.settings.show_labels %}<em>Min</em>{% endif %}</span>
    <span><strong data-secs>--</strong>{% if block.settings.show_labels %}<em>Sec</em>{% endif %}</span>
  </div>
  <span class="X__countdown-expired" hidden>{{ block.settings.label_expired }}</span>
</div>
```

**JS no `{% javascript %}`:**

```javascript
document.querySelectorAll('.X__countdown').forEach(function(el){
  var end = new Date(el.dataset.end).getTime();
  function tick(){
    var now = Date.now();
    var diff = end - now;
    if (diff <= 0) {
      el.setAttribute('data-expired', 'true');
      el.querySelector('.X__countdown-digits').hidden = true;
      el.querySelector('.X__countdown-expired').hidden = false;
      return;
    }
    var d = Math.floor(diff / 86400000);
    var h = Math.floor((diff % 86400000) / 3600000);
    var m = Math.floor((diff % 3600000) / 60000);
    var s = Math.floor((diff % 60000) / 1000);
    el.querySelector('[data-days]').textContent = String(d).padStart(2,'0');
    el.querySelector('[data-hours]').textContent = String(h).padStart(2,'0');
    el.querySelector('[data-mins]').textContent = String(m).padStart(2,'0');
    el.querySelector('[data-secs]').textContent = String(s).padStart(2,'0');
  }
  tick();
  setInterval(tick, 1000);
});
```

**Expired state** via CSS: `.X__countdown[data-expired="true"] { ... }` — swap color, apaga digits, mostra label.

**⚠️ Compliance Meta/TikTok:**
- **USAR:** deadlines fixos reais (sale end date, launch, drop, cohort close) OU integrado com Shopify sale via `compare_at_price` (countdown desaparece quando sale acaba automaticamente).
- **EVITAR:** rolling per-user (cookie-based 24h fake scarcity). Meta detecta porque cada usuário vê timer diferente pra mesma oferta → flag de "misleading urgency" → ad disapproval + shadow ban.
- **EVITAR:** reset evergreen (countdown chega a 0, recarrega pra 24h). Mesma razão.

**Subscribe & Save:** ver [Padrão 4](#padrão-4--offer-ctas-padrão-formactioncartadd-nativo) pro pattern de front-end. Apps compatíveis:

| App | Preço | Selling plan ID | Notas |
|---|---|---|---|
| Shopify Subscriptions (native) | Grátis | Admin → Products → Selling plans | Recomendado pra primeira loja |
| Loop Subscriptions | Paid | Loop dashboard → Plans | Popular em DTC escalado |
| Recharge | Paid | Recharge dashboard | Mais antigo, maior ecosystem |
| Skio | Paid | Skio dashboard | UI moderna, focus em retention |
| Seal Subscriptions | Paid | Seal dashboard | |

Todos registram `selling_plan_id` no Shopify. Front-end usa mesmo pattern `<input type="radio" name="selling_plan" value="ID">`. O app cuida do resto (cobrança recorrente, cancelamento, skip).

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
