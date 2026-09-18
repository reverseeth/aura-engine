# Checkout & AOV · Referência: Alavanca 2, cart bump e order bump

> A aceitação projetada, o Gate de Complementaridade, os bumps de margem quase pura com permalinks (query exata) e os três caminhos no Shopify. Abra ao especificar a Alavanca 2.

### Alavanca 2 — Cart bump / order bump

Checkbox de add-on no cart ou no order form ("Add [complemento] for just $X more"). O cliente já está em modo de compra (Brunson) — aceitação projetada **20-35%** em checkout Shopify real (o teto de 20-50% vem do **Free-Plus-Shipping & Order Form Bump**, query no item 3 de "Antes de Começar" — é bump de order form de funil dedicado; use o piso como conservador, igual à `offer-builder`). O bump deve ter passado no **Gate de Complementaridade** da `offer-builder` (uma das 4 categorias — nunca complemento aleatório), ser low-ticket ($9-19) e high-margin (custa $3, vende $17 = $14 de lucro quase puro — a matemática do **AOV Money Close + Offer Bump**, rode `AOV money close offer bump add more packages biggest package most popular checkout`).

**Bumps de margem quase pura + carrinho por URL:** além do add-on de produto, existe a família de bumps que não custa COGS — puxe **AOV Bumps "Selling Air" + Cart Permalinks** (rode `shipping protection 3 dólares, priority processing, montar carrinho pela URL sem app`): shipping protection por ~$3, priority processing, e a rota de montar o carrinho já preenchido por permalink na URL, sem app — o mesmo permalink serve o fallback de thank-you page da Alavanca 1 (link pra checkout pré-preenchido). Bump de "ar" também passa pelo Gate de Complementaridade no sentido do valor percebido: só entra se o membro consegue ENTREGAR o que o bump promete (proteção real, processamento real) — vender ar de mentira é refund e chargeback.

**Caminho real Shopify:**
1. **Cart bump** no template de cart do tema (`sections/main-cart.liquid` ou drawer) — bloco com checkbox que adiciona uma variante via AJAX (`/cart/add.js`). Editável como section/block (alinha com o padrão da `page-build`: tudo é setting; a copy do `offer-builder` entra como default). Este é o caminho do tema, dentro do escopo de `shopify-theme-safety` — funciona em qualquer plano.
2. **Order bump DENTRO do checkout** — via Checkout UI Extension no checkout point, mostrando o add-on antes do pagamento. **Shopify Plus only** (customização dos steps do checkout via extension exige Plus) + app container. Sem Plus, o bump vive no cart (caminho 1) — que é onde 80% do efeito acontece de qualquer jeito.
3. **App de bump** (mesmos apps da alavanca 1 normalmente cobrem cart + order bump) — no-code pra starter.

A copy do bump é 1 frase + 1 benefício (já especificada na Etapa 3 do `offer-builder`). Mantê-la curta e em inglês US.
