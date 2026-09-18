# Page Build · Referência: Referência técnica, padrões aplicados pelo conversor

> O que o `liquid-converter.py` aplica por código (os nove padrões) e o que ele NÃO faz, incluindo a implementação manual do selling plan com os números da `offer-builder`. Abra no rename semântico da ETAPA 2 e sempre que for afirmar capacidade do conversor.


Os ativos abaixo vinham da skill antiga `page-sections`. Aqui são **referência** que o conversor + a validação usam — não é geração manual de Liquid. O fluxo principal é determinístico (COMPILE via `liquid-converter.py`); esta seção explica o QUE o conversor produz e como debugar.

## Padrões aplicados pelo conversor (por código, determinísticos)

O que o `liquid-converter.py` (v3) REALMENTE aplica — valide o output contra esta lista, e NÃO afirme capacidade fora dela:

1. **Texto → settings (everything-editable)** — toda tag FOLHA com texto direto vira setting (inclui `<div class="price">$49</div>`, eyebrows em div). Texto misto com inline tags (`<em>/<strong>/<br>`) vira `inline_richtext` (tags preservadas, attrs removidos); `<p>` longo (>80 chars) vira `richtext`. Dedup: texto idêntico reutiliza o MESMO setting (2 CTAs "Buy Now" = 1 `cta_label`).
2. **Cores (CRÍTICO)** — toda cor extraída vira `color` setting E é injetada INLINE no root da section via `style="--c-x: {{ section.settings.color_x | escape }}; ..."` (NUNCA só em `:root` do stylesheet, senão o theme editor não aplica). `| escape` em TODA interpolação dentro de `style=""` — sem isso, aspas internas (`"Playfair Display", serif`) fecham o atributo e órfãm as vars seguintes. O merge respeita `style=""` existente no root.
3. **Tokens de design → settings** — `box-shadow`/`border-radius`/`font-size`/`font-family` viram `var(--x)` + setting, com migração automática de usages hardcoded no CSS (migrados ANTES das cores — shadow com hex vira 1 setting de shadow, não setting morto).
4. **Imagens → `image_picker`** + selects de aspect-ratio e fit, com `image_url | image_tag` responsivo.
5. **CTA de compra → form `/cart/add` nativo** (detecção por classe/texto/href) com settings `variant_id`/`quantity`/`after_add` e fallback URL (degrada pra `<a>` quando variant vazio). Form POST dispara `cart_updated` no Shopify Web Pixel → propaga AddToCart pra Meta Pixel/CAPI/GA4/TikTok. `<a href="/cart/add?id=X">` (GET) quebra essa cascade — pixel cego.
6. **Blocks inline com copy real por instância** — padrão repetido (cards/tiers/reviews/faq) vira block LOCAL no schema da section (`{% for block in section.blocks %}{% case block.type %}`), TODOS os itens convertidos com os defaults DAQUELE item (FAQ de 5 = 5 instâncias distintas). Irmãos fora do padrão (ex: cta-row no fim do grid) são preservados no markup.
7. **CSS por section** — `:root/html/body` rescopados pro namespace; o `page.css` é FILTRADO pras regras que a section usa (sem N cópias do CSS no tema).
8. **Schema names ≤ 25 chars** (section e blocks) — automático, com validação interna (`validate_shopify_schema`: types válidos, ids únicos, labels).
9. **`<script>` removidos COM warning** listando cada um — reimplementar a interação de forma nativa (`<details>` pra FAQ) em vez de perder silenciosamente. `<svg>` grandes viram placeholder.

**O que o conversor NÃO faz (passo manual do Claude quando a página precisar — nunca afirmar como automático):**

- **Ícones em 3 camadas** (preset enum + `icon_custom_svg` + `none`) — SVG >500 chars vira placeholder, SVG pequeno fica inline. Se o design pede ícones editáveis, o Claude adiciona os settings à mão.
- **`countdown_banner`** — não gerado. Se a oferta pede countdown, implementação manual respeitando a regra: deadline FIXO real (sale end/launch/drop), NUNCA rolling per-user nem reset evergreen (Meta detecta fake scarcity → disapproval).
- **Subscribe & Save / selling plan — não gerado pelo conversor; implementação manual COM os números da `offer-builder` (contrato `offer-builder`→`page-build`).** Antes de montar qualquer opção de assinatura na PDP, leia `offer-builder/dados.json` → `subscription_architecture` + `onetime_premium_pct` + `pricing.main_sku_price` e renderize DE ACORDO:
  - `subscription_first` → a PDP tem selling plan com DUAS opções e os preços derivados da oferta: **assinatura = `main_sku_price` (o preço-base)**; **one-time = `main_sku_price × (1 + onetime_premium_pct/100)`** (~15% acima no default da `offer-builder` — arredondamento segue a convenção de charm pricing que a `offer-builder` já validou contra a âncora de concorrente; na dúvida de arredondamento, o preço final é o do `offer-builder.md`, não um recálculo seu). O framing é o prêmio invertido ("you pay more by NOT subscribing") — **NUNCA escreva "Subscribe & Save X%"**: o desconto de assinatura foi abolido pela `offer-builder` (`sub_discount_pct` sai sempre `0`; o número vivo é `onetime_premium_pct`). O markup continua manual: `<input type="radio" name="selling_plan" value="ID">` do app de subscription, com o ID real do selling plan.
  - `onetime_plus_sub_no_reorder` → a PDP vende SÓ one-time a `main_sku_price`, **sem selling plan** — a assinatura entra no reorder (flow de replenishment da `retention-engine`) e no pós-compra (`checkout-aov`). Não adicione widget de Subscribe & Save "porque o app está instalado".
  - `no_subscription` → sem selling plan (nada a fazer).
  - **Fallback legado:** `subscription_architecture`/`onetime_premium_pct` ausentes do dados.json (oferta gerada antes do contrato) → comportamento atual (implementação manual guiada pelo membro), anotando a lacuna no `page-report.md`.
- **"Regra dos 4 headers" e `custom_css` por block** (`#pu-{{ block.id }}`) — não gerados; adicionar manualmente só se o membro precisar de override fino por block.
- **Texto solto misturado com sub-árvores** (`<div>Texto <div>...</div></div>`) fica hardcoded — reestruture o HTML no design se precisar editável.
- **Cores em `style=""` inline do HTML de origem** não são tokenizadas (só no CSS).
- **Validação semântica de Liquid** — o schema JSON é validado por código, mas rodar `shopify-plugin:shopify-liquid` em cada arquivo continua obrigatório (ETAPA 3).
