# Checkout & AOV · Referência: Alavancas 4 e 5, free-shipping threshold e checkout trust

> O threshold pelo zero price effect com o sistema a puxar e os caminhos (shipping rate, barra de progresso, app), e o checkout trust por extension, branding ou trust row na PDP e no cart com ícones SVG. Abra ao especificar as Alavancas 4 e 5.

### Alavanca 4 — Free-shipping threshold

Empurra o cliente a adicionar mais um item pra cruzar a linha. Funciona por **zero price effect** (frete REALMENTE $0, não "quase") + **mental accounting** (o "free shipping over $X" é um ganho dentro do frame) — os dois já puxados na **Pricing Psychology Suite** do item 3. Threshold típico ≈ 1.3-1.5× do AOV atual (perto o bastante pra ser alcançável, alto o bastante pra forçar o item extra). Puxar `aov_expected` do `offer-builder` pra calcular. Fundamento com números de operação: **Profit Optimization 4 Categories + AOV Builders** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — threshold, volume discount e GWP julgados por lucro-por-visitante, nunca por AOV bruto.

**Caminho real Shopify:**
1. **Shipping rate condicional** — Settings → Shipping and delivery → criar rate "Free" com condição "Order price ≥ $X" na zona do target market — o mesmo $X que a barra e a copy anunciam.
2. **Barra de progresso de free-shipping** no cart/drawer — bloco do tema ("You're $12 away from free shipping") que atualiza via JS conforme o subtotal. Editável como block (copy default do `offer-builder`, em inglês US). O valor anunciado é o MESMO da rate do item 1 (divergência = promessa na barra e frete cobrado no checkout). Como ela entra no carrinho e na gaveta, junto das outras peças da superfície, está em `reference/carrinho-e-drawer.md`.
3. **App de progress bar** (ex: Hextom Free Shipping Bar) — no-code se o membro preferir.

### Alavanca 5 — Checkout trust (badges / garantia / reviews)

Reduz a ansiedade no momento mais nervoso do funil (digitar o cartão). Pós-`checkout.liquid`, o checkout só aceita customização via **Checkout UI Extensions** — não dá pra colar HTML solto. Onde colocar:

1. **Checkout UI Extension** nos blocks do checkout — trust badges (secure payment, money-back), a garantia do `offer-builder` (ex: "90-day money-back"), e 1-2 reviews curtos. **Shopify Plus only** (customização in-checkout via extension exige Plus) + app container. Sem Plus, pule direto pros caminhos 2-3.
2. **Checkout branding** (Settings → Checkout → customize / brand) — logo, cores, e os trust elements suportados nativamente sem extension. Caminho no-code pro que o branding API expõe.
3. **Trust row na PDP/cart** (caminho do tema; no cart e na gaveta, pela superfície única de `reference/carrinho-e-drawer.md`) — como o checkout em si é restrito, a maior parte da prova de confiança vive na PDP e no cart (trust badges com **ícones SVG, nunca emoji** — regra 7 do CLAUDE.md: cadeado, caminhão, escudo de garantia, estrelas de review em SVG inline 16-18px). É onde o membro tem controle total e onde 80% do efeito acontece antes do checkout.

A garantia exibida vem da `guarantee` do `offer-builder` (e a policy page da loja diz os mesmos dias). Os números de review ("Rated 4.8 by 2,300 customers") vêm do review app (Judge.me/Loox/Yotpo).
