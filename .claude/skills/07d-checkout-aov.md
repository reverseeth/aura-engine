---
name: checkout-aov
description: Engine de AOV — implementa post-purchase upsell (one-click), cart/order bump, bundle e quantity-break, free-shipping threshold, e checkout trust (badges/garantia/reviews no checkout). Consome os bumps/upsells/bonuses já definidos no 04-offer.json e os configura na loja Shopify pelo caminho real (Functions cart-transform/discount, post-purchase Checkout UI extension, ou apps equivalentes). Use quando o membro disser "checkout", "upsell", "aov", "bump", "bundle", "order bump", "free shipping", ou após o tracking estar instalado e antes de gerar criativos. Esta é a maior alavanca de lucro por visitante que existe fora dos ads.
---

# Checkout & AOV Engine

A oferta (Skill 04) DEFINIU os bumps, upsells e bundles. Esta skill os IMPLEMENTA na loja. Aumentar o lucro por visitante aqui é o que destrava spend mais agressivo nos ads: cada $1 extra de margem por pedido é $1 a mais que você pode pagar de CPA. É a alavanca mais barata do funil porque não custa tráfego novo — só monetiza melhor o tráfego que já chega.

### Pré-flight (OBRIGATÓRIO)

Valide antes de prosseguir:

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] **Idioma (report_language).** Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (`07d-checkout-aov.md`/`.html`, `07d-checkout-aov.json` descritivo, perguntas e mensagens ao membro) usa esse idioma. **A copy que aparece no checkout/cart pro consumidor (texto do bump, headline do upsell, trust badges, barra de free-shipping) permanece SEMPRE em inglês US**, independente do report_language — é consumidor-final do mercado US e o Meta scraper lê.
- [ ] `04-offer.json` existe → extrair `bonuses[]`, `pricing` (`main_sku_price`, `aov_expected`), `unit_economics` (`weighted_margin_per_order`, `margin_per_unit`), `guarantee`, e a string `offer_stack`. O 04 já descreve **bundles** (Solo/3-pack/6-pack com savings), **checkout bump** (complemento $9-19) e **upsell pós-compra** (alto ticket $47-97+) na Etapa 3 — esta skill lê essas decisões, não as reinventa.
- [ ] `manifest.store_url` (handle .myshopify.com ou domínio custom). Se ausente, a página ainda não foi deployada — ver escape-path abaixo.
- [ ] Detectar **member-stage** (`manifest.stage` ou inferir por `member-stage-awareness.md`) — define a profundidade da implementação (starter = 1-2 alavancas no-code; scaling = stack completo).

Se faltar `04-offer.json` (a fonte dos bumps/upsells/bundles), em vez de abortar seco ofereça ≥2 caminhos (escape-path ES1):
- **(A)** Rodar a skill 04 (offer) agora pra definir bumps/upsells/bundles com base na unit economics real, OU
- **(B)** Prosseguir com defaults conservadores (bump $15 complementar, upsell single de alto ticket, free-shipping threshold ≈ 1.4× AOV) marcando `manifest.skipped_preflight += ["04-offer.json"]` e avisando no output final que recomenda re-executar quando a oferta real existir.

Se `manifest.store_url` estiver ausente (página não deployada): a config de checkout precisa de uma loja viva pra apontar variantes e thresholds. Ofereça **(A)** rodar a 07b (page-build/deploy) primeiro, OU **(B)** gerar o blueprint completo (esta skill produz todos os specs) e deixar marcado como `pending_store: true` no output pra aplicar assim que a loja existir — sem inventar IDs de variante.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes (membro nunca rodou setup), pare — mas ofereça rodar o setup (Skill 00) inline.

## Quando Usar

Na fase **storefront**, depois da página estar no ar (07b) e do tracking instalado (07c), antes dos criativos (08). A ordem importa: a página precisa existir pra ter variantes/produtos referenciáveis; o pixel/CAPI precisa estar ativo pra que os eventos de bump/upsell sejam medidos corretamente (purchase value com upsell tem que bater no Events Manager, senão o ROAS reportado fica subestimado). Os criativos vêm depois porque o AOV configurado aqui muda o CPA que você pode pagar — e o briefing de ad usa esse número.

## Antes de Começar

1. Leia `workspace/profile.md` — `report_language`, budget, stage, e tools disponíveis (algumas alavancas dependem de app pago).
2. Leia `workspace/[produto]/04-offer.md` + `04-offer.json` — bundles, bump, upsell, stack de valor, garantia, e unit economics. Os números de aceitação projetados (bump 20-35%, upsell 5-15%) e o AOV projetado da Etapa 6 do 04 são o baseline; aqui você os transforma em config real.
3. Consulte a base Aura sobre pricing psychology e checkout optimization: **decoy effect** e **extremeness aversion** pra estruturar os tiers de bundle (3 opções, o do meio é o alvo, o premium ancora, o budget faz o meio parecer esperto), **charm pricing** (terminação em 9, left-digit effect — exceto se o posicionamento for premium/round), **zero price effect** (FREE é qualitativamente diferente de "quase grátis" — o threshold de free-shipping tem que entregar frete REALMENTE zero), **mental accounting** (segregar ganhos: listar bônus e savings separados; integrar perdas: um pagamento só), **order form bump** (Brunson — checkbox no checkout converte 20-50% porque o cliente já está em modo de compra), as 3 estruturas de OTO (Next Thing / Do It Faster / Need Help?), e checkout friction reduction (tirar o olho do campo de cupom, CTA em primeira pessoa, atenção gerenciada pro botão).

Não consulte o membro sobre decisões estratégicas (qual tier ancora, qual % de savings) — isso já saiu da Skill 04 e da base. Pergunte só o que é input externo que você não tem (IDs de variante, app instalado, fulfillment de in-box gift).

## As 5 alavancas de AOV (e o caminho real no Shopify pra cada)

O Shopify mudou o checkout: customizações de checkout exigem **Checkout UI Extensions** (Checkout Extensibility, obrigatório desde a depreciação do `checkout.liquid`) e **Shopify Functions** pra lógica de desconto/bundle. Não existe "editar o checkout.liquid à mão" pra a maioria das lojas hoje. Abaixo o caminho real por alavanca — sem pseudo-API.

### Alavanca 1 — Post-purchase upsell (one-click)

O mais lucrativo e o de maior margem incremental: o cliente já pagou, o cartão já passou, aceitar é 1 clique sem re-digitar nada. Aceitação típica 5-15%; um upsell que vai de 20% pra 40% de take pode somar $15-25 ao bottom line por pedido.

**Caminho real Shopify (em ordem de robustez):**
1. **Post-purchase Checkout UI Extension** (`purchase.thank-you` / post-purchase extension point) — extensão nativa que aparece ENTRE o pagamento e a thank-you page, com one-click add sem novo checkout. É o caminho canônico pós-`checkout.liquid`. Requer app (custom ou via Shopify CLI `shopify app generate extension --type post_purchase`) e que o produto/plano da loja suporte post-purchase (Shopify Plus ou plano que habilite a API). Documente que o membro precisa de um app container pra hospedar a extensão.
2. **App de post-purchase upsell** (ex: AfterSell, ReConvert, Zipify OCU, Selleasy) — caminho no-code/low-code. Pra **starter/validating** é o recomendado: instala da App Store, configura o OTO no painel do app apontando pro `upsell` do 04-offer, sem código. Documente o app concreto que o stack do membro permite (ler `profile.md`).
3. **Thank-you page upsell (fallback sem one-click)** — se nem extension nem app: bloco de oferta na thank-you page (Settings → Checkout → Order status page additional scripts ou bloco no tema) com link pra um checkout pré-preenchido. Perde o "um clique" (cliente re-paga), aceitação cai. Só como último recurso.

**Estrutura do OTO** (da base — escolher a que casa com o produto): **Next Thing** (complemento lógico ao que comprou), **Do It Faster** (acelera o resultado), **Need Help?** (done-for-you/serviço). Copy: 2-3 frases + benefício principal + a oferta com âncora ("normally $X, today $Y"). Aplicar charm pricing no preço do upsell.

### Alavanca 2 — Cart bump / order bump

Checkbox de add-on no cart ou no order form ("Add [complemento] for just $X more"). Converte 20-50% porque o cliente já está em modo de compra (Brunson). O bump deve ser complemento natural do SKU principal, low-ticket ($9-19), e high-margin (custa $3, vende $17 = $14 de lucro quase puro).

**Caminho real Shopify:**
1. **Cart bump** no template de cart do tema (`sections/main-cart.liquid` ou drawer) — bloco com checkbox que adiciona uma variante via AJAX (`/cart/add.js`). Editável como section/block (alinha com o padrão da 07b: tudo é setting; a copy do 04 entra como default). Este é o caminho do tema, dentro do escopo de `shopify-theme-safety`.
2. **Order bump no checkout** — via Checkout UI Extension no checkout point, mostrando o add-on antes do pagamento. Requer app container (igual à alavanca 1).
3. **App de bump** (mesmos apps da alavanca 1 normalmente cobrem cart + order bump) — no-code pra starter.

A copy do bump é 1 frase + 1 benefício (já especificada na Etapa 3 do 04). Mantê-la curta e em inglês US.

### Alavanca 3 — Bundle / quantity-break

O 04 já definiu a tabela (Solo / 3-pack "Popular" / 6-pack "Best Value") com savings. Aqui você a renderiza com pricing psychology aplicada:

- **3 tiers sempre** (extremeness aversion — Simonson/Tversky): o do meio (3-pack) é o alvo, marcado **Popular**; o 6-pack é o âncora premium que faz o 3-pack parecer razoável; o Solo é o budget que faz o 3-pack parecer esperto. Se a oferta tiver só 2 tiers, sugira adicionar um terceiro — o tier que ninguém compra pode ser o elemento mais lucrativo da arquitetura (decoy).
- **Decoy quando aplicável** — se o objetivo é empurrar o 3-pack, garantir que ele domine claramente o vizinho em $/unidade e savings (o "Economist effect": o tier que ninguém escolhe move 84% pro combo).
- **Charm pricing** nos preços de bundle (terminação em 9) — exceto se o posicionamento for premium (aí round numbers). Mostrar sempre o "was" (3× solo riscado) ao lado do preço do bundle: transaction utility = a alegria da pechincha vem do gap entre a âncora e o preço real.
- **Savings segregado** ("You save $Z (28%)") — mental accounting: ganho listado à parte é um ganho a mais.

**Caminho real Shopify:**
1. **Quantity-break / volume discount via Shopify Function** (discount function "buy X get Y% off" / tiered) — preço por unidade cai automaticamente conforme a quantidade. Função aplicada via app de discount (ou custom function `shopify app generate extension --type product_discounts`).
2. **Variantes de bundle** (3-pack e 6-pack como variantes ou produtos separados com seu próprio SKU/preço) renderizadas no bloco de pricing-tier da PDP (o block type `pricing_tier` da 07b). Caminho mais simples, no-code, e o que casa diretamente com a página já buildada.
3. **App de bundle** (ex: Fast Bundle, Bundler, Shopify Bundles app nativo) — gera o bundle product + desconto sem código.

Recomendar o caminho 2 (variantes na PDP) pra starter/validating — zero app, zero função, e o pricing block do tema já existe. Function/app só quando o membro quer quantity-break dinâmico ou mix-and-match.

### Alavanca 4 — Free-shipping threshold

Empurra o cliente a adicionar mais um item pra cruzar a linha. Funciona por **zero price effect** (frete REALMENTE $0, não "quase") + **mental accounting** (o "free shipping over $X" é um ganho dentro do frame). Threshold típico ≈ 1.3-1.5× do AOV atual (perto o bastante pra ser alcançável, alto o bastante pra forçar o item extra). Puxar `aov_expected` do 04 pra calcular.

**Caminho real Shopify:**
1. **Shipping rate condicional** — Settings → Shipping and delivery → criar rate "Free" com condição "Order price ≥ $X" na zona do target market. Esta é a fonte da verdade que o **Gate Promise↔Config (pre-launch-gates)** valida: se a copy promete "Free shipping over $75" mas a zona não tem essa rate configurada, é `fail` e bloqueia.
2. **Barra de progresso de free-shipping** no cart/drawer — bloco do tema ("You're $12 away from free shipping") que atualiza via JS conforme o subtotal. Editável como block (copy default do 04, em inglês US). Caminho do tema, dentro de `shopify-theme-safety`.
3. **App de progress bar** (ex: Hextom Free Shipping Bar) — no-code se o membro preferir.

### Alavanca 5 — Checkout trust (badges / garantia / reviews)

Reduz a ansiedade no momento mais nervoso do funil (digitar o cartão). Pós-`checkout.liquid`, o checkout só aceita customização via **Checkout UI Extensions** — não dá pra colar HTML solto. Onde colocar:

1. **Checkout UI Extension** nos blocks do checkout (ex: dynamic checkout, ou os checkout branding settings) — trust badges (secure payment, money-back), a garantia do 04 (ex: "90-day money-back"), e 1-2 reviews curtos. Requer app container.
2. **Checkout branding** (Settings → Checkout → customize / brand) — logo, cores, e os trust elements suportados nativamente sem extension. Caminho no-code pro que o branding API expõe.
3. **Trust row na PDP/cart** (caminho do tema) — como o checkout em si é restrito, a maior parte da prova de confiança vive na PDP e no cart (trust badges com **ícones SVG, nunca emoji** — regra 7 do CLAUDE.md: cadeado, caminhão, escudo de garantia, estrelas de review em SVG inline 16-18px). É onde o membro tem controle total e onde 80% do efeito acontece antes do checkout.

A garantia exibida tem que bater com a `guarantee` do 04 E com a policy page da loja (Gate Promise↔Config: "90-day money-back" na trust row exige policy declarando 90 dias). Os números de review ("Rated 4.8 by 2,300 customers") exigem que o review app (Judge.me/Loox/Yotpo) tenha esses números reais — senão é `fail` no gate.

## Fluxo da Skill

### ETAPA 1 — Carregar a oferta e mapear o que já existe

Leia o `04-offer.json` e monte a tabela do que a oferta JÁ definiu vs. o que falta implementar:

| Alavanca | Definido no 04? | Valor/spec do 04 | Caminho Shopify escolhido | Status |
|---|---|---|---|---|
| Post-purchase upsell | `upsell` (sim/não) | nome, preço, take projetado | extension / app / thank-you | a configurar |
| Cart/order bump | `bump` (sim/não) | complemento, preço, copy | tema / extension / app | a configurar |
| Bundles | `bundles[]` (sim/não) | Solo/3/6, savings, Popular | variantes PDP / function / app | a configurar |
| Free-shipping threshold | derivado de AOV | threshold = 1.3-1.5× AOV | shipping rate + bar | a configurar |
| Checkout trust | `guarantee` + reviews | tipo de garantia, # reviews | checkout extension / branding / PDP | a configurar |

Se uma alavanca não foi definida no 04 (ex: oferta sem upsell), não a force — registre como `not_in_offer` e siga. Não inventar um upsell que a unit economics não sustenta.

### ETAPA 2 — Pergunta ao membro (APENAS o que é input externo)

Não pergunte estratégia. Pergunte só o que você não consegue inferir:

1. **Apps já instalados?** "Você já tem algum app de upsell/bump instalado (AfterSell, ReConvert, Zipify, Selleasy, etc)? Se sim, qual? Se não, posso fazer pelo caminho nativo (tema + Functions) ou recomendar um app." — define caminho no-code vs. código.
2. **Plano da loja** (só se for tentar post-purchase extension): "Sua loja é Shopify Plus ou plano que habilita post-purchase?" — post-purchase one-click depende disso; se não, cai pro app ou thank-you fallback.
3. **In-box gift?** (só se algum bonus do 04 for físico/in-box): "O brinde físico vai junto na caixa? Aí é coordenação com fulfillment, não config de loja." — separa o que é config do que é operação.

Para **starter**, default no-code: app único que cobre bump + upsell + bar, ou caminho do tema pros bundles. Não recomendar app pago se o membro tem budget apertado e o caminho nativo resolve.

### ETAPA 3 — Especificar cada alavanca (blueprint implementável)

Para cada alavanca ativa, produza um spec concreto e aplicável (não prosa genérica):

- **Pricing exato** com charm pricing aplicado e a âncora ("was $X / now $Y").
- **Copy real** (inglês US, ad-safe pela regra 8b, sem travessão em headlines pela 8a) — bump (1 frase + benefício), upsell (2-3 frases + benefício + oferta), bundle labels (Popular/Best Value), free-shipping bar ("You're $X away from free shipping"), trust row (garantia + badges).
- **Caminho técnico** escolhido (tema / Function / extension / app) com os passos reais.
- **Onde aplicar** (qual arquivo do tema, qual setting do admin, qual painel do app).
- **Aceitação projetada** (do 04 ou benchmark da base) e impacto no AOV.

### ETAPA 4 — Recalcular o AOV e a economics com as alavancas ativas

Atualize o AOV projetado considerando as alavancas implementadas (bump take × preço bump + upsell take × preço upsell + shift de mix por bundle/threshold). Mostre o delta:

- AOV antes (do 04): $X
- AOV depois (com checkout stack): $Y
- Delta de margem por pedido: +$Z (puxa de `weighted_margin_per_order`)
- **Novo target CPA viável**: como `weighted_margin_per_order` sobe, o CPA que você pode pagar pra 2×/3× ROAS também sobe — registrar pra a Skill 10 (ad-strategy) usar o número atualizado.

> **Não sobrescreva** `weighted_margin_per_order` no `04-offer.json` (é a fonte da unit economics). Grave o AOV/margem PROJETADOS-PÓS-CHECKOUT em `07d-checkout-aov.json` e atualize `manifest.aov_baseline` se a config foi de fato aplicada na loja (não só planejada). A Skill 11 reconcilia com o AOV real medido depois.

### ETAPA 5 — Aplicar na loja (se store_url existe) ou entregar blueprint

**Se a loja existe e o membro aprovou o blueprint** (checkpoint de iteration-driven-refinement — "Aprova a direção ou ajusto pricing/copy?"):

- **Caminhos do tema** (cart bump, free-shipping bar, trust row na PDP): seguir `shopify-theme-safety` INTEGRAL — `shopify theme pull --live --nodelete` antes de editar, marker de verificação, `shopify theme push --live --allow-live --nodelete`, smoke test (Regra 7), e o iteration loop dá `pull` antes de re-push pra não sobrescrever settings do theme editor.
- **Caminhos de admin** (shipping rate, checkout branding, discount function via app): documentar os passos exatos do painel (não dá pra automatizar tudo via CLI) — ex: "Settings → Shipping → Add rate → condition Order price ≥ $75 → price $0.00".
- **Caminhos de app**: passos no painel do app, apontando os IDs de variante reais (pedir ao membro ou ler via Admin API se conectada).

**GATES (blocking — pre-launch-gates):**
- **GATE 1 — Ad-flag compliance** sobre TODA copy de checkout/cart injetada (bump, upsell, bar, trust) ANTES de aplicar. `critical`/`high` bloqueia; aplicar rewrite e re-checar.
- **GATE 2 — Promise↔Config**: o free-shipping threshold da copy tem que existir como shipping rate real; a garantia exibida tem que bater com a policy page; os números de review têm que existir no review app. `fail` ≥ 1 → não aplicar, reportar o `fix`.

**Se a loja NÃO existe** (`pending_store: true`): entregar o blueprint completo, marcar cada alavanca como `pending` no JSON, e avisar no output final que aplica assim que a 07b deployar a loja. Sem inventar IDs de variante nem aplicar nada.

### ETAPA 6 — Member-stage (profundidade da implementação)

- **Starter** (0-30 dias, budget apertado): 1-2 alavancas de maior alavancagem e menor esforço — geralmente **bundle na PDP** (zero app, já tem o pricing block) + **free-shipping bar** (tema). Pular post-purchase extension (depende de plano/app). Explicar o porquê de cada escolha (educação embutida).
- **Validating** (30-90 dias): adicionar **cart/order bump** + **um app de upsell** no-code (AfterSell/ReConvert). Trust row na PDP. Começar a medir take rates reais.
- **Scaling** ($5k+/mês): stack completo — post-purchase one-click via extension/app, quantity-break via Function, checkout trust via extension, bundle dinâmico. A margem extra justifica o custo de app premium e o trabalho de extension.

Não recomende post-purchase extension custom pra starter com $500/mês; não deixe um scaling com $20k/mês só com bundle na PDP (desperdiça a alavanca de upsell one-click).

## SALVAR (dual output — rule 6b do CLAUDE.md)

Salvar em `workspace/[produto]/`:

**`07d-checkout-aov.md`** (humano) contendo:
1. Mapa das 5 alavancas: definida no 04? caminho Shopify? status (aplicada/pending/not_in_offer)
2. Spec de cada alavanca ativa (pricing com charm, copy real, caminho técnico, onde aplicar, aceitação projetada)
3. AOV/margem antes vs. depois + novo target CPA viável pra a Skill 10
4. Resultado dos gates (compliance + promise↔config)
5. Passos de aplicação (tema / admin / app) e o que ficou pending

**`07d-checkout-aov.html`** (companion humano) — usar `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained). **Logo SVG no topo do `<body>`, copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA texto.** Componentes aura (kpi-grid pro AOV antes/depois, table-wrap pro mapa de alavancas, callout/note/danger pros gates). Ícones SVG, nunca emoji, em qualquer preview de checkout/cart consumidor-final (regra 7).

**`07d-checkout-aov.json`** (estruturado, pras skills 10/11):

```json
{
  "product_slug": "<do manifest>",
  "store_url": "<do manifest ou null>",
  "applied_to_store": false,
  "pending_store": false,
  "levers": {
    "post_purchase_upsell": { "active": true, "path": "app|extension|thankyou", "app": "AfterSell|null", "price": 49, "anchor_was": 79, "take_projected": 0.10, "oto_structure": "next_thing|do_it_faster|need_help", "status": "applied|pending|not_in_offer" },
    "cart_bump": { "active": true, "path": "theme|extension|app", "price": 17, "take_projected": 0.25, "status": "applied" },
    "bundles": { "active": true, "path": "pdp_variants|function|app", "tiers": [{ "qty": 1, "price": 49 }, { "qty": 3, "price": 119, "label": "Popular" }, { "qty": 6, "price": 199, "label": "Best Value" }], "psychology": ["extremeness_aversion", "decoy", "charm_pricing"], "status": "applied" },
    "free_shipping_threshold": { "active": true, "threshold": 75, "path": "shipping_rate+bar", "status": "applied" },
    "checkout_trust": { "active": true, "path": "pdp_trust_row|checkout_extension|branding", "guarantee": "90-day money-back", "review_count": 2300, "status": "applied" }
  },
  "aov_projection": {
    "aov_before": 118.00,
    "aov_after": 142.00,
    "weighted_margin_before": 72.00,
    "weighted_margin_after": 88.00,
    "new_target_cpa_2x": 44.00,
    "new_target_cpa_3x": 29.33
  },
  "gates": {
    "compliance": "pass|warn|block",
    "promise_config": { "pass": 3, "warn": 0, "fail": 0 }
  }
}
```

Atualizar `manifest.json`: adicionar `07d-checkout-aov` em `skills_completed`; se aplicado de fato na loja, atualizar `aov_baseline` com o `aov_after`. Não sobrescrever `04-offer.json`.

## Mensagem Final

Primeira versão como **draft**, não "pronto" (iteration-driven-refinement):

"Primeira versão do stack de checkout/AOV pronta. Implementei [N] alavancas: [lista curta — ex: bundle 3-tier na PDP, cart bump $17, free-shipping bar em $75, trust row].

AOV projetado subiu de **$X pra $Y** (+$Z de margem por pedido). Isso significa que o CPA que você pode pagar pra 2× ROAS subiu de $A pra $B — a Skill 10 vai usar esse número novo no briefing de ad.

Revisa o pricing e a copy e me diz o que ajustar: o threshold de free-shipping tá no ponto certo? O preço do upsell faz sentido? Itero até ficar redondo.

Próximo passo: diga **'creatives'** pra gerar os anúncios (já com o AOV/CPA atualizado) — ou **'tracking'** se o pixel/CAPI ainda não tiver sido configurado."
