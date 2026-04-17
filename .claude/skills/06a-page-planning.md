---
name: page-planning
description: Planeja uma página Shopify a partir da copy — detecta tipo (advertorial / landing / hybrid), roda brand discovery, extrai signals de referência visual (opcional), orquestra specialists de design pra gerar o design system completo. Primeira skill da cadeia `page-planning → page-sections → page-deploy`. Use quando o membro disser "page", "página", "build page", "shopify page", "gerar página" logo após ter copy pronta.
---

# Page Planning — ETAPAS 0-3

Esta é a **primeira** das 3 skills da cadeia Page Engine modularizada. Ela:

1. Faz pre-flight (valida inputs)
2. Detecta tipo de página (advertorial vs landing vs hybrid)
3. Escolhe o plano de sections (menu adaptativo)
4. Roda brand discovery (6 perguntas em 1 mensagem)
5. Extrai signals de referência visual (se membro colar URL)
6. Orquestra 5 specialists pra gerar o design system completo

**Outputs gravados em `/workspace/[produto]/06-page/`:**
- `06-design-system.md` — paleta, tipografia, spacing, grid, tokens
- `06-plan.md` — plano de sections + justificativa
- `06-plan.json` — mesmo plano, machine-readable (consumido pela `page-sections`)

Depois desta skill, rode `page-sections` pra converter em Liquid.

## Pré-flight

Antes de qualquer outra coisa, valide:

- [ ] `/workspace/[produto]/manifest.json` existe e tem `05-copy-engine` em `skills_completed`
- [ ] `/workspace/[produto]/05-copy.json` existe e é parseável
- [ ] `/workspace/[produto]/04-offer.json` existe
- [ ] Dir de output: `/workspace/[produto]/06-page/` (criar com `mkdir -p` se não existir)

Se algum item faltar:
- Copy não gerada → "Não achei `05-copy.json`. Rode a skill `copy-engine` primeiro."
- Offer não gerada → "Não achei `04-offer.json`. Rode `offer-builder` primeiro."
- Manifest inexistente ou sem `05-copy-engine` → peça pra completar o fluxo anterior antes.

## Quando Usar

Quando o membro tem copy pronta (em `/workspace/[produto]/05-copy.md` / `05-copy.json`) e quer começar a gerar uma página Shopify completa que seja:
- Visualmente premium
- Theme-agnostic (funciona em Dawn, Horizon, Impulse, Sense, Prestige, qualquer Shopify 2.0+)
- 100% editável via theme editor (todo elemento é uma `setting`)
- Self-contained (zero dependência do CSS do tema pai)
- Validada antes de salvar

A página vem ANTES dos criativos no fluxo do Aura Engine — não faz sentido criar ads pra uma página que ainda não existe.

## ETAPA 0 — Detecção e Leitura

### 0.1 Pesquisa exploratória na base Aura

Consulte a base Aura extensivamente sobre: 15 fatores da estrutura de funil (framework que diagnostica PDPs e LPs), landing pages que convertem (Empathy/Trust/Offer, NESP framework), 10x page plan (framework completo), advertorials (propósito, listicles, 7-section blueprint), checkout optimization (frictionless, trust badges, bumps, savings display), profit optimization (pricing, bundles, AOV builders), hero sections (5 tipos e critérios de seleção), congruência ad→page (message match, visual match, promise match), 4 decision making modalities (Spontaneous/Competitive/Humanistic/Methodical — toda página deve servir os 4 simultaneamente), behavioral psychology (System 1 vs System 2, above-the-fold triggers), CTAs como call to VALUE, crossheads e estrutura visual, wireframing e validação de web copy, proof stacking (Hopkins specificity + social proof volume + authority markers), e qualquer framework adjacente que apareça. Aprofunde em cada sub-conceito até ter domínio completo de conversão + estrutura de página.

### 0.2 Detectar o produto

A skill precisa saber **qual produto** ela está construindo a página. Detecte assim:

1. **Se o membro mencionou o produto explicitamente** ("page para [nome-do-produto]", "build page for [slug]"), use o slug exato.
2. **Caso contrário, liste os produtos disponíveis** em `/workspace/` (cada subpasta é um produto):
   - Se tiver **apenas 1 produto** → use ele automaticamente, mas confirme: "Vou gerar a página pro produto X. Confirma?"
   - Se tiver **múltiplos produtos** → mostre lista numerada e peça pro membro escolher
   - Se não tiver **nenhum produto** → diga: "Não encontrei produtos no workspace. Rode primeiro a skill `setup` ou `product research` pra criar a estrutura, ou cole a copy diretamente aqui."
3. **Salve o slug do produto** numa variável `PRODUTO` que será usada em todos os paths daqui pra frente. Daqui em diante, sempre que ver `[produto]` na skill, substitua pelo slug detectado.

### 0.3 Detecção de tipo de página (advertorial vs landing vs hybrid)

Antes do plano de sections, decida o TIPO da página baseado na copy:

| Tipo | Sinal na copy | Estrutura típica |
|---|---|---|
| **advertorial** | copy começa com narrativa/story/article-style, headlines editoriais, "I used to..." / "Doctor reveals...", sem CTA explícito no topo | Listicles, 7-section blueprint (hook → problem → agitation → mechanism → proof → CTA soft → FAQ) |
| **landing** | copy focada em produto específico, headline de benefit + CTA logo no hero, estrutura NESP (Novelty/Exclusivity/Simplicity/Proof) | 10x plan, estrutura persuasiva com hero → proof → offer → guarantee → faq → cta-final |
| **hybrid** | copy começa com hook narrativo mas converge pra produto específico e tem offer stack | Advertorial na abertura + landing nos últimos 40% da página |

**Como detectar programaticamente:**
1. Leia o primeiro bloco de copy do `05-copy.json`.
2. Conte: headlines no estilo "How I [verb]..." / "The [adjective] [noun] that..." → advertorial
3. Se tem **offer stack explícito** (pricing tiers, bundles com preços) no topo → landing
4. Se tem narrativa MAS também pricing logo no topo → hybrid

Pergunte ao membro pra confirmar o tipo detectado antes de prosseguir.

### 0.4 Ler inputs obrigatórios

1. **OBRIGATÓRIO**: Leia `/workspace/[produto]/05-copy.md` e `/workspace/[produto]/05-copy.json`.
2. Leia `/workspace/[produto]/04-offer.md` / `04-offer.json` (preço, stack, garantia — vai pra section de oferta).
3. Leia `/workspace/[produto]/02-market-research.md` se existir (pra entender awareness level e voz do cliente).
4. Leia `/workspace/[produto]/03-competitor-analysis.md` se existir.
5. Leia `/workspace/profile.md` se existir.

## Princípios Inegociáveis (aplicam a TODA a cadeia)

Estes princípios NÃO são negociáveis. Se algum for violado, a section deve ser refeita.

1. **Proibido o block `custom_liquid` NATIVO do Shopify** (o que a plataforma adiciona por default em certos temas e esconde HTML cru não-editável). Elementos visuais sempre são settings ou blocks customizados. **Exceção:** você PODE oferecer um block type customizado chamado `custom_liquid` com setting `type: "liquid"` (documentado no Catálogo de Blocks em `page-sections`) — isso é escape hatch editável, não o antipattern Shopify nativo.
2. **Self-contained CSS**. Todo CSS vai dentro de `{% stylesheet %}` da própria section. Zero dependência de classes/variáveis do tema pai.
3. **Theme-agnostic**. Não use classes do tema pai (`.product-card`, `.btn-primary`, etc). Use namespacing próprio: `.page-[produto]-hero`, `.page-[produto]-feature`.
4. **Mobile-first**. Todo CSS começa pelo mobile e usa media queries pra escalar.
5. **Semantic HTML**. `<section>`, `<article>`, `<header>`, `<h1>-<h6>` na ordem correta, `<button>` pra ações, `<a>` pra navegação, `<picture>`/`<img>` com `alt`.
6. **WCAG 2.1 AA** (checklist detalhado na skill `page-sections`). Quality standard universal — não restringe design, garante que qualquer design gerado seja usável por todo usuário.
7. **Validação obrigatória**. Cada arquivo passa pelo skill `shopify-plugin:shopify-liquid` (validate.mjs) antes de ser salvo. Se falhar, corrige e revalida (3 retries).
8. **Zero JS frameworks externos**. Sem React, Vue, jQuery, libraries de animação. Use JavaScript vanilla quando absolutamente necessário, dentro de `{% javascript %}`.
9. **Imagens via `image_picker` setting**, nunca hardcoded ou via `asset_url`. O membro sobe a foto pelo theme editor.
10. **Fluid type e spacing**. Use `clamp(min, preferred, max)` pra tipografia e padding em sections importantes.
11. **Color settings são injetadas INLINE no root da section** (via `style="--c-primary: {{ section.settings.color_primary }};"`), nunca hardcoded em `:root` do stylesheet. Sem isso, a mudança no theme editor não aplica. Detalhe completo em `page-sections` (Padrão crítico — Color settings inline).
12. **Everything editable** — fonts, radius, shadows, sizes são settings no schema, não valores fixos no CSS. O membro não sabe CSS mas sabe quando quer mudar a fonte. Detalhe em `page-sections` (Padrão "Everything editable").
13. **Granularidade máxima de cores** — toda cor visível tem color setting próprio (média 15-30 por section). Checklist por tipo de section em `page-sections` (Auditoria de cores).

## ETAPA 1 — Leitura e Planejamento (adaptativo à estratégia)

**A página NÃO tem estrutura fixa.** Cada produto merece um plano de sections que reflita sua estratégia específica — awareness level do mercado (Schwartz), sophistication stage (Bond), nível de ceticismo, complexidade do produto, categoria, tipo de decisão (impulse vs considered), presença ou não de mecanismo único, etc. A skill 05 (copy) já definiu essas decisões — respeite-as.

**1. Leia `05-copy.md` + `02-market-research.md` + `03-competitor-analysis.md` + `04-offer.md`** pra entender:
- Awareness level do mercado (Unaware → Most Aware)
- Sophistication stage (1-5)
- Nível de ceticismo (baixo/médio/alto)
- Se tem mecanismo único ou não
- Tipo de produto (commodity, categoria nova, disrupter, incremental)
- Preço (baixo = impulse, alto = considered)

**2. Escolha as sections adequadas a partir do MENU abaixo**, baseando-se no que a estratégia pede. Não force o formato "9 sections padrão" em todo produto.

### Menu de sections possíveis

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
- Quais blocks atômicos do catálogo universal (eyebrow, heading, paragraph, etc — ver `page-sections`)
- Quais blocks type-specific (benefit_card, pricing_tier, review_card, faq_item, etc)
- **Quais settings de customização máxima** vão ser expostos no schema (planeje desde já pra não esquecer):
  - Todas as cores visíveis têm color setting próprio (15-30 settings por section — auditoria detalhada em `page-sections`)
  - Fonts (heading + body) como select preset + text custom family
  - Radius (sm/md/lg/pill), shadow intensity (none/subtle/medium/strong), font_size_base, scale_ratio como ranges
  - Ícones: preset enum + `icon_custom_svg` textarea (overrides preset) + opção `none`
  - Pricing tier CTAs: usar form `/cart/add` nativo, NÃO link — precisa settings `variant_id`, `quantity`, `after_add`, `cta_fallback_url`, + subscribe & save (se aplicável)
  - Countdown banner (se offer tem urgência real): deadline fixo + timezone + labels + colors
- **Regra:** a filosofia do Aura Engine é "everything editable". Membros não sabem CSS mas sabem quando querem mudar algo. Tudo que pode virar setting, vira — o cap é o limite de 250 settings/section do Shopify.

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

## ETAPA 2 — Brand Discovery (1 mensagem ao membro)

Pergunte (em UMA mensagem) só o que precisa pra começar:

1. **Estilo visual desejado** (escolha 1 ou descreva custom):
   - Minimalist editorial — off-white, sage/cream, generous whitespace, refined serif
   - Bold modern — dark backgrounds, large sans-serif, vibrant accent
   - Clinical premium — clean white, navy/gold, data-forward, technical
   - Wellness organic — warm tones, soft curves, hand-drawn touches
   - Custom — descreva
2. **Cores da marca** se houver (ou "escolhe pra mim baseado no estilo")
3. **Caminhos de assets** (logo, fotos do produto) se tiver — caso contrário usa placeholders
4. **Theme path** (default `~/shopify-theme`) — vai ser usado pela `page-deploy`
5. **Handle do produto pro template** (default = slug do nome do produto)
6. **Referência visual (opcional)** — "Tem algum site cujo visual você curte e quer usar como inspiração pra paleta e fontes? Passa o link (ou pula)." Se o membro passar um link, vai pra sub-etapa 2.1. Se não, pula direto pra Etapa 3.

### Validação das respostas de cor

Quando o membro responder, **valide cada cor fornecida** antes de aceitar:

1. **Regex de hex válido:** `^#([0-9A-Fa-f]{3,8})$` (aceita `#RGB`, `#RRGGBB`, `#RRGGBBAA`).
2. **Se o membro passar nome de cor** (ex: "sage green", "dusty rose"), converta via tabela fixa abaixo. Se a cor não estiver na tabela, pergunte: "Preciso do hex exato ou um dos nomes abaixo. Qual você quer?"

**Tabela fixa de nomes → hex (30 cores comuns):**

| Nome | Hex |
|---|---|
| sage green | `#9CAF88` |
| dusty rose | `#D4A5A5` |
| warm white / off-white | `#FDFAF4` |
| cream | `#F5EDE0` |
| navy | `#14213D` |
| ivory | `#FFFFF0` |
| charcoal | `#36454F` |
| taupe | `#B0A99F` |
| terracotta | `#C66B3D` |
| olive | `#6B7040` |
| burgundy | `#800020` |
| mustard | `#D4A017` |
| blush | `#F4C2C2` |
| forest green | `#228B22` |
| dusty blue | `#6B8CAE` |
| coral | `#FF7F50` |
| camel | `#C19A6B` |
| slate | `#708090` |
| mint | `#98D8B0` |
| lavender | `#B497BD` |
| rust | `#B7410E` |
| sand | `#C2B280` |
| pearl | `#EAE0C8` |
| plum | `#8E4585` |
| peach | `#FFCBA4` |
| sage | `#9CAF88` |
| moss | `#8A9A5B` |
| bone | `#E3DAC9` |
| onyx | `#353839` |
| gold | `#D4AF37` |

3. **Se o membro não passar cor alguma** ("escolhe pra mim"), pule a validação — o `designer-color-system` vai gerar do estilo.

### ETAPA 2.1 — Referência visual (quando o membro passa link)

**Importante:** isso NÃO é clone de design. É só extração de sinais de paleta/tipografia do site de referência pra ALIMENTAR o `designer-color-system` e o `designer-typography-scale` na Etapa 3. O design ainda é gerado do zero.

**Validação de tooling (antes de rodar):**

1. Cheque se o script existe:
   ```bash
   test -f tools/design-clone/downloader.py && echo "OK" || echo "MISSING"
   ```
   Se `MISSING`, **pule esta etapa graciosamente**: informe o membro que o sistema de extração visual não está disponível neste projeto e peça pra colar descrição manual da referência (ou simplesmente escolher um dos estilos pré-definidos).

2. Valide que Playwright + BeautifulSoup estão instalados:
   ```bash
   python3 -c "import playwright, bs4" 2>&1
   ```
   Se falhar: "Pra extrair signals da referência visual preciso de Playwright + BeautifulSoup. Rode no terminal real:
   ```
   pip install -r tools/design-clone/requirements.txt
   playwright install chromium
   ```
   Ou pula a referência e escolhe um dos estilos pré-definidos."

3. Baixe a página de referência:
   ```bash
   python3 tools/design-clone/downloader.py "URL" "/tmp/ref-[produto]"
   ```

4. Rode analyzer + pattern-extractor pra extrair signals:
   ```bash
   python3 tools/design-clone/analyzer.py "/tmp/ref-[produto]"
   python3 tools/design-clone/pattern-extractor.py "/tmp/ref-[produto]"
   ```

5. Leia `/tmp/ref-[produto]/patterns.json` → extraia apenas o `design_system` (typography + colors + shape + spacing). Ignore `sections[]` — não vamos copiar estrutura, só absorver signals visuais.

6. Mostre ao membro um resumo curto:
   > "Peguei a vibe da [url]:
   > - Fontes: **[heading_font]** (títulos) + **[body_font]** (corpo)
   > - Paleta: fundo **[background_primary]** · texto **[text_primary]** · accents **[accents]**
   > - Radius **[border_radius_px]px** · shadow **[shadow_style]** · density **[density]**
   > 
   > Vou usar isso como input pro design system. O layout e a estrutura ainda vêm da copy — só a paleta/tipografia é inspirada."

7. Siga pra Etapa 3. No `designer-color-system` e `designer-typography-scale`, passe os valores extraídos como **preferência inicial** (não impositivo — o specialist pode ajustar pra garantir contraste WCAG e hierarquia).

## ETAPA 3 — Generate Design System (orquestração)

Antes de gerar qualquer section, defina o sistema de design completo.

### Invocação dos specialists (sequencial)

Use **Skill tool** na ordem:

1. `/designer-color-system` com params: `brand_colors=[...]`, `usage_context=ecommerce`
   - Gere paleta de 5-7 cores (background, surface, foreground, primary, accent, muted, border) baseada no estilo + cores da marca + signals da referência (se houver da Etapa 2.1).
   - Saída: hex codes + role semântico.

2. `/designer-typography-scale` com params: `base_size=16`, `ratio=1.25`
   - Gere modular type scale (recomendado 1.25 ou 1.333) com 6 níveis (h1-h6) + body + small.
   - Use fluid type com `clamp()`.
   - Sugira heading font + body font (system fonts ou Google Fonts populares).
   - Se houver referência, priorize as fontes extraídas.

3. `/designer-spacing-system` com params: `base_unit=4`
   - Gere spacing tokens em base 4px ou 8px (xs, sm, md, lg, xl, 2xl, 3xl).

4. `/designer-layout-grid` com params: `max_width=1280`, `breakpoints=[640,960,1280]`
   - Defina container max-width (recomendado 1200-1440px), grid system, breakpoints (mobile 480, tablet 768, desktop 1024, wide 1440).

5. `/designer-design-token` com params: `output_format=css-variables`
   - Consolide tudo em um conjunto de CSS custom properties que serão injetadas via `:root` no `{% stylesheet %}` de cada section.

**Output agregado em `/workspace/[produto]/06-page/06-design-system.md`** como referência. Mostre ao membro um resumo compacto e peça aprovação rápida.

## Outputs (ao final da skill)

Salve em `/workspace/[produto]/06-page/`:

- **`06-design-system.md`** — design system completo (paleta, tipografia, spacing, grid, tokens)
- **`06-plan.md`** — plano de sections humanizado (justificativa de cada section incluída/excluída)
- **`06-plan.json`** — plano machine-readable consumido pela `page-sections`:
  ```json
  {
    "produto": "[slug]",
    "page_type": "advertorial|landing|hybrid",
    "sections_plan": [
      {"id": "hero", "blocks": ["eyebrow","heading","paragraph","button_row","stats_bar","tag"]},
      {"id": "benefits", "blocks": ["eyebrow","heading","benefit_card"]},
      ...
    ],
    "section_order": ["hero","benefits","mechanism","proof","offer","guarantee","faq","cta_final"],
    "brand_discovery": {
      "style": "minimalist-editorial",
      "brand_colors": ["#...","#..."],
      "logo_path": "...",
      "theme_path": "~/shopify-theme",
      "handle": "[slug]",
      "reference_url": "https://..."
    },
    "design_system_ref": "06-design-system.md",
    "generated_at": "2026-...Z"
  }
  ```

Atualize `/workspace/[produto]/manifest.json` adicionando `06a-page-planning` ao array `skills_completed`.

Ao final diga ao membro:

> "Plano de página + design system prontos. Próximo passo: rode `page-sections` pra converter em Liquid e gerar os arquivos `.liquid` das sections."

## Referências cruzadas

- **Próxima skill:** `page-sections` (consome `06-plan.json` + `06-design-system.md`)
- **Skill final da cadeia:** `page-deploy` (deploy no Shopify)
- **Catálogo completo de blocks** (universais + type-specific) está em `page-sections` — não repita aqui.
- **Ferramentas auxiliares de referência visual:** `tools/design-clone/downloader.py`, `analyzer.py`, `pattern-extractor.py`. Estes scripts compartilham `_css_utils.py` (util de rewrite de CSS namespace).
