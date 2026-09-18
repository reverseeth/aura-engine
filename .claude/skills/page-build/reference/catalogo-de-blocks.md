# Page Build · Referência: Referência técnica, catálogo de block types

> O vocabulário de conteúdo pro rename semântico: os blocks universais com os settings-chave, os type-specific por section, a regra dos 4 headers e por que blocks são inline no schema. Abra no rename da ETAPA 2.

## Catálogo de Block Types

Este catálogo é o **vocabulário de conteúdo** pro rename semântico (ETAPA 2) — NÃO é a lista de settings que o conversor emite (ele deriva os settings do markup real de cada item; os "Settings-chave" abaixo são referência do que costuma existir, e `custom_css` é adição manual opcional, nunca automática). Realização concreta: conteúdo de instância ÚNICA (1 eyebrow, 1 heading, 1 CTA num hero) vira **section setting** (grupo Content, editável); conteúdo REPETÍVEL (vários cards/tiers/reviews/faq items) vira **block** (`{% case block.type %}`, arrastável/reordenável). O `{% case %}` gerado contém só o(s) type(s) do padrão repetido detectado — os "universais" NÃO são gerados como block types; aparecem como settings quando o conteúdo é único.

**Universais (conteúdo estrutural — settings quando único; vocabulário de nomeação quando o padrão repetido cai numa dessas categorias):**

| Block | Uso | Settings-chave |
|---|---|---|
| `eyebrow` | Label acima de headings | text · size · weight · transform · tracking · color · space b/a · **custom_css** |
| `heading` | Título (h1/h2/h3) com `<em>` | text (inline_richtext) · size · font · weight · color · line_height · letter_spacing · max_width · **custom_css** |
| `paragraph` | Texto longo | text (richtext) · size · color · line_height · max_width · **custom_css** |
| `badge` | Pill/chip com dot | text · show_dot · dot_color · variant · bg · text_color · radius · **custom_css** |
| `button_row` | Até 3 botões inline | alignment · gap · radius · por botão (show/label/url/variant/bg/text/price) · **custom_css** |
| `stats_bar` | Até 5 stats em grid | columns · gap · show_divider · por stat (show/label/value inline_richtext) · **custom_css** |
| `trust_row` | Até 6 trust items | alignment · gap · show_divider · por item (icon/label) · **custom_css** |
| `tag` | Floating tag sobre imagem | eyebrow · title · position (tl/tr/bl/br) · rotation · theme · bg · text · radius · **custom_css** |
| `divider` | Linha separadora | style · color · thickness · width% · **custom_css** |
| `icon` | Ícone isolado | icon · size · color · **custom_css** |
| `spacer` | Espaço vertical | height · **custom_css** |
| `custom_liquid` | Escape hatch (`type: "liquid"`) | code · **custom_css** |
| `custom_html` | HTML estático (`type: "html"`) | html · **custom_css** |

**Type-specific (além dos universais):**
- Benefits → `benefit_card` (num/icon + title + body + accent)
- Proof / social-proof → `review_card` (stars + quote + author + avatar + featured)
- Offer → `pricing_tier` (name + price + strap + features richtext + CTA form `/cart/add` + **`qty` + `variant_id`** — contrato da recipe deploy-shopify-product + badge + popular + image) · `countdown_banner` (limit 1; implementação manual — o conversor não gera) · selling plan/Subscribe & Save (implementação manual COM os números da `offer-builder` — contrato `offer-builder`→`page-build` na lista "O que o conversor NÃO faz")
- Guarantee → `promise_item` (title + body + accent + icon)
- FAQ → `faq_item` (question + answer richtext + open_by_default) — usar `<details><summary>` nativo
- Mechanism → `mechanism_card` / `ingredient_card` / `process_step` / `science_card` (nomeie conforme o mecanismo real)
- Before-after → `comparison_pair` (before_image + after_image + label)
- Ingredients → `ingredient` (name + role + dosage + image)
- How-it-works → `step` (number + title + description + image)
- Quiz (`page_type: quiz`, uma section pro funil inteiro) → `quiz_intro` (1) · `quiz_question` (1 por pergunta, com até 4 pares `answer_N_label`/`answer_N_to`) · `quiz_result` (1 por perfil, com **`qty` + `variant_id`**, mesmo contrato do `pricing_tier`). Destino de tela é setting `text` com a `key` da tela de destino, NUNCA setting `url` (limitação 2). Detalhe em `reference/quiz-sections.md`

**Regra dos 4 headers (organização manual opcional):** Content (o quê) · Style (como) · Spacing (onde) · Advanced (custom_css com `id="pu-{{ block.id }}"` + `<style>` scoped). O conversor NÃO emite isso automaticamente — é padrão de organização pro Claude aplicar à mão quando um block precisa de controle fino.

**Blocks inline no schema, NUNCA theme blocks em `/blocks/*.liquid`** com `{% content_for 'block' type: block.type %}` — o validator do Shopify bloqueia vars dinâmicas ("The 'id' argument should be a string"). O conversor gera inline (nenhum `blocks/*.liquid` é escrito; `--blocks-dir` é deprecado e ignorado).
