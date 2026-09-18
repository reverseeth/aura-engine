# Bonus Delivery · Referência: Playbook por tipo de bônus e os tipos de subscription (ETAPAs 2 e 2b)

> O playbook completo de cada tipo primário (gift-with-purchase com os sistemas de calibragem e a mecânica por `condition`, e-book e guide rumo ao dream outcome, SKU complementar grátis, gift wrapping, discount code) e o bloco curto dos tipos de subscription e membership como caso de borda. Abra na ETAPA 2.

### ETAPA 2 — Playbook por tipo (primários)

#### `gift_with_purchase` (GWP) — brinde físico low-COGS acima de threshold

A alavanca de AOV mais direta. Add um item de baixo COGS quando o cart subtotal cruza um threshold.

**Puxe os SISTEMAS NOMEADOS pra calibrar o GWP** (rode a `best_query`):
- **Profit Optimization 4 Categories + AOV Builders (Bundles, Free-Shipping Threshold, Volume Discounts, GWP, Pack Sizes)** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — define onde o GWP encaixa no mapa de AOV e a métrica profit/visitor.
- **AOV Money Close + Offer Bump + Add-More-Packages** (rode `AOV money close offer bump add more packages biggest package most popular checkout`) — posiciona o threshold do GWP junto do tier "most popular".
- **3x+ Markup Rule + $60 AOV Floor (Margin Validation for Paid-Traffic Brands)** (rode `3x markup rule 60 dollar AOV floor COGS shipping margin paid traffic CPM fixed`) — sanity check de margem: o brinde low-COGS não pode furar o piso.

**0. Ler `condition` do bonus (da `offer-builder`) — define a mecânica ANTES de qualquer threshold:**
   - `unconditional` → o brinde foi prometido na PDP a TODO comprador: **auto-add em toda compra** (app/Function SEM threshold). Colocar threshold aqui quebra a promessa da página.
   - `cart_threshold` → seguir os passos 1-2 abaixo (threshold ancorado no AOV). A copy da página DEVE refletir a condição ("FREE over $X") — coordenar com `copy-engine`/`page-design`.
   - `tier_specific` → o brinde destrava num tier específico (3-pack/6-pack): gatilho por produto/variant do tier, não por subtotal.

**1. Definir o threshold (cart subtotal — só pra `condition: cart_threshold`):** ancorar no AOV. Ler `offer-builder/dados.json` (price, offer_stack) e o AOV histórico se existir (manifest ou Stripe). Regra prática: threshold ~10-20% **acima** do AOV atual, pra empurrar o cliente a adicionar 1 item a mais sem ser inalcançável. Se não houver AOV histórico, usar o preço do tier principal × 1.1 como proxy e marcar como teórico.

**2. Sourcing low-COGS:** o brinde precisa ter percepção de valor alta e custo real baixo (sample size do próprio catálogo, item complementar barato, kit emocional). O `value_anchored` na PDP ancora no preço de varejo do item ou de itens comparáveis no mercado.

**3. Implementação Shopify (caminho real — NÃO draft order):**
   - **Caminho A — App de gift-with-purchase** (BOLD, Gift Box, Free Gifts BOGO, etc): config no admin do app "free product when cart ≥ $threshold". Mais rápido pra starter, sem código.
   - **Caminho B — Shopify Functions** (cart transform / discount function): regra "add free variant / 100% off quando cart subtotal ≥ threshold". Mais robusto e sem mensalidade de app, mas exige a function publicada na loja. Coordenar com **checkout-aov** (é config de checkout/store, mora lá).
   - **NUNCA** usar draft order pra GWP — não escala, quebra com self-checkout, e não dispara no fluxo normal de compra.

**4. Congruência "free" na PDP:** garantir que o brinde **apareça** visualmente (imagem do gift, badge "FREE GIFT over $X"). Coordenar com a página (`page-design`/`page-build`) — ícone SVG, nunca emoji (rule 7).

**5. KPI = take-rate.** A métrica é quantos % dos pedidos destravam o brinde (escolhem o tier ou cruzam o threshold). Benchmark da base: a escolha do tier full-size (o tamanho cheio, que destrava o brinde) subiu de **30% pra 52%** dos pedidos ao adicionar o GWP; AOV +12%, lucro por visitante +20%. Registrar take-rate no snapshot (ETAPA 4) assim que houver dado.

#### `free_ebook` / `digital_guide` / `workbook` / `checklist` — asset digital rumo ao dream outcome

O e-book/guide que ajuda o cliente a **alcançar o resultado** que o produto promete (não um PDF genérico). Razor-blade fit: o asset faz o cliente ter mais sucesso com o produto → mais retenção e reorder.

**Puxe os SISTEMAS NOMEADOS pra ancorar o asset no dream outcome** (rode a `best_query`):
- **Hormozi Value Equation (Dream Outcome × Perceived Likelihood / Time Delay × Effort & Sacrifice)** (rode `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice`) — o e-book deve mover ≥1 das 4 variáveis (tipicamente reduzir Time Delay e Effort pra chegar no resultado).
- **Razor-Blade vs Handle (Bonus Fit Principle)** (rode `razor blade vs handle bonus fit natural complement to product`) — o asset só vale se faz o cliente extrair mais do produto principal, não como "PDF qualquer".

**1. Gerar o conteúdo** alinhado ao dream outcome (ler `market-research/dados.json` pra VOC e desire, `offer-builder/dados.json` pro mecanismo). O e-book é REAL e específico do avatar, não "10 daily tips". Exemplo bom: skincare 45-65 → "The 14-Day Glow Protocol: exactly when to apply, what to pair, what to avoid".

**2. Produzir o PDF:** Markdown → HTML → PDF (weasyprint ou headless Chrome). Design da **marca do membro** (cores/fonte da brand, não do Aura). Conteúdo **em inglês** (consumidor US). Salvar em `workspace/[produto]/bonus-delivery/bonuses/[bonus-id]/[bonus-id].pdf`.

**3. Entrega:** link na thank-you page / order status (config da Fase A — é o que garante o acesso do comprador do dia 1, antes do flow de email existir) + link no email post-purchase (ver ETAPA 3, executado pela `retention-engine`). Asset hospedado em Shopify Files API, S3 ou R2.

**4. KPI = access rate** (% que abre/baixa). Logar na ETAPA 4.

#### `free_complementary_sku` — produto complementar grátis

Um SKU do catálogo que **vai bem com o principal** dado grátis (não um threshold genérico). Funciona como GWP atrelado a um produto específico ("compre o sérum, ganhe o cleanser travel-size").

**1. Confirmar o fit:** o complementary precisa potencializar o resultado do principal (razor-blade). Se for só "outro produto qualquer", questionar o membro.
**2. Implementação:** mesma mecânica do GWP (app ou Function, NÃO draft order), mas o gatilho é o **produto** no cart, não o subtotal. Coordenar com `checkout-aov`.
**3. In-box vs auto-add:** se o complementary já é estoque físico, pode ser **in-box gift** — documentar pro fulfillment incluir em toda caixa do SKU principal. Se for via cart, app/Function.
**4. KPI = take-rate + attach impact** (sobe o reorder do complementary depois?).

#### `gift_wrapping` — embrulho de presente grátis (Q4)

Bônus sazonal de alto valor percebido e COGS quase zero. Brilha em Q4/gifting season e converte o avatar "comprando pra outra pessoa".

**1. Implementação:** opção de gift-wrap grátis no cart/checkout (cart attribute, line-item property, ou app de gift options). Coordenar com `checkout-aov` (checkout) — é config de loja.
**2. Fulfillment:** documentar pro fulfillment center: "embrulhar pedidos com a flag gift_wrap". In-box, não digital.
**3. Personalização por persona** (da base — exemplo Original Grain): quem chega de ad de gifting vê a opção de gift-wrap + card em destaque; quem chega de self-purchase, não. Coordenar com a página se houver split de persona.
**4. KPI = attach rate do gift-wrap.**

#### `discount_code` — código de desconto complementar (suporte, não primário)

Code na Shopify Admin pra produto complementar, com expiração (30-60 dias pós-purchase). Único por customer (tag `uniqueCode`) ou compartilhado. Delivery: email + thank-you page com botão copy-to-clipboard. É bônus de **reorder/backend**, não de aquisição.

Como é alavanca de LTV/backend, **puxe o SISTEMA NOMEADO** antes de dimensionar o desconto (rode a `best_query`): **Kennedy Price Minimizers (5 Strategies) + Damaging Admission** (rode `Kennedy price minimizers five strategies compare apples oranges damaging admission`) — pra enquadrar o code como minimizador de preço percebido no reorder, não como erosão de margem.

### ETAPA 2b — Tipos de subscription/membership only (caso de borda)

Estes tipos só fazem sentido pra negócios de **subscription/membership**, não DTC físico padrão. Se o membro vende produto físico one-time, **não recomendar** — geralmente é o domínio errado (info-product) herdado. Playbook curto:

- **`community_access`** — Circle (single-use invite, mais seguro) / Discord / Skool. Link no email post-purchase. Só se a marca opera comunidade ativa.
- **`video_series`** — Wistia/Vimeo com password, gated page Shopify. Só se há conteúdo em vídeo de valor.
- **`consultation_call`** — Calendly/Cal.com com quota diária. **Escala mal**: se vender >50 unidades/dia, desligar ou cobrar fee simbólico.
- **`trial_extension`** — extender via Shopify Subscription app (se subscription) ou license key UUID com expiração.

Se algum bonus da `offer-builder` caiu num desses por engano (era pra ser ecom), surface pro membro: "Esse bônus tá modelado como [tipo de subscription], mas seu produto é físico one-time. Quer trocar pra [gift_with_purchase / free_ebook]? Isso é decisão de oferta, ajusto na `offer-builder`."
