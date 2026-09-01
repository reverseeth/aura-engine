---
name: checkout-aov
description: Engine de AOV — implementa post-purchase upsell (one-click), cart bump, bundle e quantity-break, free-shipping threshold, e checkout trust. Consome os bumps/upsells/bundles já definidos na Skill 04 (todos aprovados no Gate de Complementaridade) e os configura na loja Shopify pelo caminho real por plano e estágio (variantes na PDP, bundle nativo via productBundleCreate, Functions via app público, matriz de apps ReConvert→AfterSell→Zipify OCU com config spec — nenhum app tem API de config). Use quando o membro disser "checkout", "upsell", "aov", "bump", "bundle", "order bump", "free shipping", ou após o tracking estar instalado e antes de gerar criativos. Esta é a maior alavanca de lucro por visitante que existe fora dos ads.
---

# Checkout & AOV Engine

A oferta (Skill 04) DEFINIU os bumps, upsells e bundles. Esta skill os IMPLEMENTA na loja. Aumentar o lucro por visitante aqui é o que destrava spend mais agressivo nos ads: cada $1 extra de margem por pedido é $1 a mais que você pode pagar de CPA. É a alavanca mais barata do funil porque não custa tráfego novo — só monetiza melhor o tráfego que já chega.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`; o mapa skill→domínio está no README). Os domínios desta skill são `page-landing-cro` (as famílias Checkout/Cart Friction Reduction, AOV Builders e Profit Optimization), `brand-building-bonus-aov` e `offer-pricing-guarantee`. Sempre que uma etapa mandar "consulte a base", rode `search_knowledge` com a `best_query` NOMEADA de cada framework relevante (`deep=true`) — **NUNCA query genérica**. As queries de maior impacto estão embutidas byte-exatas no item 3 de "Antes de Começar" e no ponto de uso de cada alavanca abaixo.
>
> **Contrato de cobertura (kb-index, revisado 2026-09):** no início de cada etapa que consulta a base, abra `frameworks.json` e **enumere TODAS as entradas dos domínios acima cujo `use_in_skill` inclui a 07d** — as queries embutidas nesta skill são o núcleo mínimo garantido, **nunca o teto**: entrada relevante à etapa que não está embutida é pra ser puxada do mesmo jeito. Critério de relevância por FASE: "esta entrada informa a decisão desta etapa?" — "talvez" = puxa. Não repita busca de framework já puxado na sessão (entradas duplicadas entre domínios apontam pro MESMO conteúdo — reuse o resultado). Antes de fechar a etapa, releia a lista enumerada e confirme que nada relevante ficou sem puxar. O tamanho real de cada domínio é o que está no `frameworks.json` — nunca número decorado em texto de skill.

### Pré-flight (OBRIGATÓRIO)

Valide antes de prosseguir:

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] **Idioma (report_language — regra 0 do CLAUDE.md, INVIOLÁVEL).** Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`), e escreva com o rigor de linguagem simples da regra 0. TODO output interno (`07d-checkout-aov/checkout-aov.md`/`.html`, `07d-checkout-aov/dados.json` descritivo, perguntas e mensagens ao membro) usa esse idioma. **A copy que aparece no checkout/cart pro consumidor (texto do bump, headline do upsell, trust badges, barra de free-shipping) permanece SEMPRE em inglês US**, independente do report_language — é consumidor-final do mercado US e o Meta scraper lê.
- [ ] `04-offer-builder/dados.json` existe → extrair `bonuses[]`, `pricing` (`main_sku_price`, `aov_expected`), `unit_economics` (`weighted_margin_per_order`, `margin_per_unit`), `guarantee`, a string `offer_stack`, **e o contrato de assinatura: `subscription_architecture` + `onetime_premium_pct`** (governam toda superfície de checkout/upsell que toque assinatura — ver o bloco "Superfícies de assinatura" na Alavanca 1; ausentes em dados.json legado → trate como sem contrato: comportamento atual, nenhuma superfície de assinatura nova, lacuna anotada no output). O 04 já descreve **bundles** (Solo/3-pack/6-pack com savings), **checkout bump** (complemento $9-19) e **upsell pós-compra** (alto ticket $47-97+) na Etapa 3 — esta skill lê essas decisões, não as reinventa.
- [ ] `manifest.store_url` (handle .myshopify.com ou domínio custom). Se ausente, a página ainda não foi deployada — ver escape-path abaixo.
- [ ] `manifest.storefront` (bloco gravado pela 07b na publicação: `theme_id` + `page_url`). **É nesse `theme_id` que esta skill opera** — cart bump/bar/trust row têm que viver no MESMO tema da página. Se `manifest.storefront` não existe (página só em preview, tema não publicado), avise: "A página ainda não foi publicada (07b passo 6.10). Posso gerar o blueprint e aplicar as alavancas no tema de preview, mas antes do launch a publicação precisa acontecer."
- [ ] Detectar **member-stage** (`manifest.stage` ou inferir por `member-stage-awareness.md`) — define a profundidade da implementação (starter = 1-2 alavancas no-code; scaling = stack completo).

Se faltar `04-offer-builder/dados.json` (a fonte dos bumps/upsells/bundles), em vez de abortar seco ofereça ≥2 caminhos (escape-path ES1):
- **(A)** Rodar a skill 04 (offer) agora pra definir bumps/upsells/bundles com base na unit economics real, OU
- **(B)** Prosseguir com defaults conservadores (bump $15 que caia numa das 4 categorias do Gate de Complementaridade, upsell more-of-same com desconto exclusivo pós-compra, free-shipping threshold ≈ 1.4× AOV) marcando `manifest.skipped_preflight += ["04-offer-builder/dados.json"]` e avisando no output final que recomenda re-executar quando a oferta real existir.

Se `manifest.store_url` estiver ausente (página não deployada): a config de checkout precisa de uma loja viva pra apontar variantes e thresholds. Ofereça **(A)** rodar a 07b (page-build/deploy) primeiro, OU **(B)** gerar o blueprint completo (esta skill produz todos os specs) e deixar marcado como `pending_store: true` no output pra aplicar assim que a loja existir — sem inventar IDs de variante.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes (membro nunca rodou setup), pare — mas ofereça rodar o setup (Skill 00) inline.

## Quando Usar

Na fase **storefront**, depois da página estar no ar (07b) e do tracking instalado (07c), antes dos criativos (08). A ordem importa: a página precisa existir pra ter variantes/produtos referenciáveis, e o pixel/CAPI precisa estar ativo pra que bump e bundle entrem no Purchase medido. **Limitação conhecida do post-purchase:** o evento Purchase da integração nativa dispara no fim do checkout, ANTES do aceite do upsell one-click — o valor do OTO aparece no Shopify mas normalmente NÃO entra no Purchase do Events Manager (o ROAS reportado fica um pouco subestimado; a Skill 11 reconcilia com o revenue real do Shopify). Os criativos vêm depois porque o AOV configurado aqui muda o CPA que você pode pagar — e o briefing de ad usa esse número.

## Antes de Começar

1. Leia `workspace/profile.md` — `report_language`, budget, stage, e tools disponíveis (algumas alavancas dependem de app pago).
2. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (se não existir, leia o legado `relatorio.md`) + `04-offer-builder/dados.json` — bundles, bump, upsell, stack de valor, garantia, e unit economics. Os números de aceitação projetados (bump 20-35%; upsell post-purchase 3-8% média da plataforma, 8-14% em oferta bem casada) e o AOV projetado da Etapa 6 do 04 são a fonte única; aqui você os transforma em config real (sem re-somar — ver ETAPA 4).
3. Puxe os SISTEMAS NOMEADOS da base (rode a `best_query` de cada um, `deep=true` — nunca query genérica):
   - **Pricing Psychology Suite** (rode `pricing psychology anchoring decoy extremeness aversion zero price effect charm pricing mental accounting endowment`) — o kit inteiro num sistema só: **decoy effect** e **extremeness aversion** pra estruturar os tiers de bundle (3 opções, o do meio é o alvo, o premium ancora, o budget faz o meio parecer esperto), **charm pricing** (terminação em 9, left-digit effect — exceto se o posicionamento for premium/round), **zero price effect** (FREE é qualitativamente diferente de "quase grátis" — o threshold de free-shipping tem que entregar frete REALMENTE zero) e **mental accounting** (segregar ganhos: listar bônus e savings separados; integrar perdas: um pagamento só).
   - **Profit Optimization (Profit Per Visitor + 5 Levers)** (rode `profit optimization profit per visitor pricing levers AOV revenue vanity profit sanity`) — a métrica-mãe desta skill: lucro por visitante = lucro por pedido × conversão; "revenue is vanity, profit is sanity".
   - **Free-Plus-Shipping & Order Form Bump** (rode `Brunson free plus shipping buyer 10x order form bump 20 to 50 percent`) — checkbox no order form converte 20-50% porque o cliente já está em modo de compra.
   - **Three OTO Structures** (rode `Brunson three OTO structures next thing do it faster need help upsell`) — as 3 estruturas de OTO (Next Thing / Do It Faster / Need Help?).
   - **Checkout / Cart Friction Reduction** (rode `checkout cart optimization coupon field abandonment first person button glowing box`) — tirar o olho do campo de cupom, CTA em primeira pessoa, atenção gerenciada pro botão.

Não consulte o membro sobre decisões estratégicas (qual tier ancora, qual % de savings) — isso já saiu da Skill 04 e da base. Pergunte só o que é input externo que você não tem (IDs de variante, app instalado, fulfillment de in-box gift).

## As 5 alavancas de AOV (e o caminho real no Shopify pra cada)

O Shopify mudou o checkout: customizações de checkout exigem **Checkout UI Extensions** (Checkout Extensibility, obrigatório desde a depreciação do `checkout.liquid`) e **Shopify Functions** pra lógica de desconto/bundle. Não existe "editar o checkout.liquid à mão" pra a maioria das lojas hoje. Abaixo o caminho real por alavanca — sem pseudo-API.

### Alavanca 1 — Post-purchase upsell (one-click)

O mais lucrativo e o de maior margem incremental: o cliente já pagou, o cartão já passou, aceitar é 1 clique sem re-digitar nada. Benchmarks 2026: aceitação média da plataforma **3-8%**; oferta bem casada (Gate de Complementaridade + more-of-same) chega a **8-14%**; página post-purchase bem construída adiciona **12-22%** no valor do pedido.

**Requisito real (NÃO é plano Shopify):** post-purchase one-click funciona em **qualquer plano** via app da App Store (ReConvert/AfterSell/Zipify pedem o acesso pra loja live automaticamente). As limitações verdadeiras: (a) o OTO só aparece pra pagamento com **cartão/Shopify Payments** — wallets (Apple Pay, Google Pay, Shop Pay em alguns fluxos, Klarna, PayPal) NÃO exibem a oferta, e em mobile US boa parte dos checkouts é wallet, então **desconte isso do take rate projetado**; (b) 1 app de post-purchase por loja; (c) máximo 3 ofertas aceitas por checkout; (d) pedido mínimo $0.50 no cartão.

**Caminho real Shopify (em ordem de recomendação):**
1. **App de post-purchase upsell** (matriz por estágio na ETAPA 6b) — caminho no-code recomendado pra qualquer stage: instala da App Store, configura o OTO no painel do app apontando pro `upsell` do 04-offer. **Nenhum desses apps tem API pública de configuração** — o setup é painel manual, então esta skill gera o *config spec* (produto, preço, copy, downsell) pro membro colar.
2. **Post-purchase Checkout UI Extension custom** (`shopify app generate extension --type post_purchase`) — extensão nativa que aparece ENTRE o pagamento e a thank-you page. Funciona em todos os planos (com request de acesso pra loja live), mas exige um app container próprio pra hospedar — só faz sentido pra scaling com dev à disposição; não recomende pra starter/validating.
3. **Thank-you page upsell (fallback sem one-click)** — bloco de oferta na **Thank you / Order status page via checkout editor** (Checkout Extensibility — apps de thank-you page cobrem isso em qualquer plano) com link pra checkout pré-preenchido. Perde o "um clique" (cliente re-paga), aceitação cai. Só como último recurso. **NUNCA recomende "Order status page additional scripts"** — esse recurso foi desligado (sunset pra todos os planos em 26/ago/2026); qualquer setup nele morre junto.

**Estrutura do OTO** (da base — escolher a que casa com o produto): **Next Thing** (complemento lógico ao que comprou), **Do It Faster** (acelera o resultado), **Need Help?** (done-for-you/serviço) — as 3 estruturas vêm do **Three OTO Structures** (query no item 3 de "Antes de Começar"). Pra escolher QUAL upsell por tipo de produto e montar a página do OTO, puxe os SISTEMAS NOMEADOS:
- **Os 5 Tipos de Upsell por Tipo de Produto + a Regra de Ouro** (rode `done-for-you more of the same acelerador novo problema proximidade, qual upsell por produto`) — os 5 formatos mapeados por tipo de produto, e a regra de escolher pela **contribuição em AOV**, não pela taxa de conversão.
- **Arquitetura Completa de Upsell/Downsell (Haddad, 9 movimentos)** (rode `reverter o dano que a doença já causou, speed angle via FAQ, fórmula de downsell reconhecer desmontar cortar`) — a escada encadeada de upsell→downsell (a anatomia da oferta pós-compra: ângulo, velocidade via FAQ, e a fórmula de downsell que reconhece, desmonta e corta a objeção quando o OTO principal é recusado).

Copy: 2-3 frases + benefício principal + a oferta com âncora ("normally $X, today $Y"). Aplicar charm pricing no preço do upsell.

**Hierarquia de complementaridade (comprador NOVO de tráfego frio — a 04 ETAPA 3 já ordenou assim):** a oferta nº 1 é **more-of-same** (mais do próprio produto com desconto exclusivo do momento pós-compra), a nº 2 é o **big swing** (supply 3-6 meses), e SÓ DEPOIS produto complementar. Cliente RECORRENTE inverte: complementar converte 20-35% melhor pra quem já conhece o produto — se a loja já tem base de clientes, segmente o OTO por novo vs. recorrente quando o app permitir (é a segmentação pós-compra que **Os 5 Tipos de Upsell** acima fundamenta: o upsell certo muda com quem está comprando, e a régua continua sendo contribuição de AOV).

**Superfícies de assinatura (contrato 04→07d — vale pra OTO, thank-you page, cart e qualquer superfície desta skill):** leia `04-offer-builder/dados.json` → `subscription_architecture` + `onetime_premium_pct` + `pricing.main_sku_price` e obedeça a arquitetura:

- `subscription_first` → a PDP (07b) já vende a assinatura no preço-base com o one-time `main_sku_price × (1 + onetime_premium_pct/100)`. Toda superfície de checkout que toque assinatura usa o MESMO framing invertido: **um upsell/OTO que ofereça a assinatura NUNCA oferece desconto sobre ela** — o desconto de assinatura foi abolido pela 04 (`sub_discount_pct` = 0; o número vivo é `onetime_premium_pct`). O diferencial percebido vem do prêmio do one-time ("you pay more by NOT subscribing"), e o adoçante permitido é produto/bônus grátis, nunca % off recorrente. Puxe os SISTEMAS NOMEADOS: **Estrutura da Oferta de Assinatura** (rode `você paga mais por NÃO assinar, one-click upsell na thank you page, produto grátis melhor que desconto`) e **Subscription Economics Playbook** (rode `playbook de subscription take rate one-click upsell pós-compra supply de 1 mês`) — o motor de lucro pós-compra: take rate, one-click na thank-you page, produto dimensionado pra 1 mês de supply.
- `onetime_plus_sub_no_reorder` → o checkout NÃO empurra assinatura: a conversão pra assinatura acontece no REORDER (Email 2 do replenishment da 13) e no pós-compra planejado lá. O OTO desta skill fica no produto (more-of-same/big swing) — não crie uma superfície de assinatura no checkout que atropele o timing que a oferta escolheu.
- `no_subscription` → nenhuma superfície de assinatura. Ponto.
- **Cuidado com a palavra na superfície:** framing de subscription mal apresentado destrói CPA — **Offer Rebuild + o custo da palavra "subscription"** (rode `mesmos ads mesma conta só mudou a oferta, subscription destrói CPA 100x`). Se a superfície precisa da assinatura, venda o benefício (supply contínuo, preço travado, "cancel anytime"), não a palavra.
- **Fallback legado:** `subscription_architecture`/`onetime_premium_pct` ausentes (dados.json anterior ao contrato) → comportamento atual (nenhuma superfície de assinatura nova), lacuna anotada no output.
- **Check de consistência (a 09 herda):** se qualquer superfície configurada aqui exibir desconto de assinatura, ou preço de assinatura ≠ preço-base, ou one-time ≠ base × (1+premium), registre item `warn` em `gates.promise_config` do `07d-checkout-aov/dados.json` (com o par esperado-vs-configurado) — a Skill 09 herda pelo C4 (checkout promise↔config) e cobra no gate de launch.

### Alavanca 2 — Cart bump / order bump

Checkbox de add-on no cart ou no order form ("Add [complemento] for just $X more"). O cliente já está em modo de compra (Brunson) — aceitação projetada **20-35%** em checkout Shopify real (o teto de 20-50% vem do **Free-Plus-Shipping & Order Form Bump**, query no item 3 de "Antes de Começar" — é bump de order form de funil dedicado; use o piso como conservador, igual à 04). O bump deve ter passado no **Gate de Complementaridade** da 04 (uma das 4 categorias — nunca complemento aleatório), ser low-ticket ($9-19) e high-margin (custa $3, vende $17 = $14 de lucro quase puro — a matemática do **AOV Money Close + Offer Bump**, rode `AOV money close offer bump add more packages biggest package most popular checkout`).

**Bumps de margem quase pura + carrinho por URL:** além do add-on de produto, existe a família de bumps que não custa COGS — puxe **AOV Bumps "Selling Air" + Cart Permalinks** (rode `shipping protection 3 dólares, priority processing, montar carrinho pela URL sem app`): shipping protection por ~$3, priority processing, e a rota de montar o carrinho já preenchido por permalink na URL, sem app — o mesmo permalink serve o fallback de thank-you page da Alavanca 1 (link pra checkout pré-preenchido). Bump de "ar" também passa pelo Gate de Complementaridade no sentido do valor percebido: só entra se o membro consegue ENTREGAR o que o bump promete (proteção real, processamento real) — vender ar de mentira é refund e chargeback.

**Caminho real Shopify:**
1. **Cart bump** no template de cart do tema (`sections/main-cart.liquid` ou drawer) — bloco com checkbox que adiciona uma variante via AJAX (`/cart/add.js`). Editável como section/block (alinha com o padrão da 07b: tudo é setting; a copy do 04 entra como default). Este é o caminho do tema, dentro do escopo de `shopify-theme-safety` — funciona em qualquer plano.
2. **Order bump DENTRO do checkout** — via Checkout UI Extension no checkout point, mostrando o add-on antes do pagamento. **Shopify Plus only** (customização dos steps do checkout via extension exige Plus) + app container. Sem Plus, o bump vive no cart (caminho 1) — que é onde 80% do efeito acontece de qualquer jeito.
3. **App de bump** (mesmos apps da alavanca 1 normalmente cobrem cart + order bump) — no-code pra starter.

A copy do bump é 1 frase + 1 benefício (já especificada na Etapa 3 do 04). Mantê-la curta e em inglês US.

### Alavanca 3 — Bundle / quantity-break

O 04 já definiu a tabela (Solo / 3-pack "Popular" / 6-pack "Best Value") com savings. Aqui você a renderiza com pricing psychology aplicada:

- **3 tiers sempre** (extremeness aversion — Simonson/Tversky): o do meio (3-pack) é o alvo, marcado **Popular**; o 6-pack é o âncora premium que faz o 3-pack parecer razoável; o Solo é o budget que faz o 3-pack parecer esperto. Se a oferta tiver só 2 tiers, sugira adicionar um terceiro — o tier que ninguém compra pode ser o elemento mais lucrativo da arquitetura (decoy).
- **Decoy quando aplicável** — se o objetivo é empurrar o 3-pack, garantir que ele domine claramente o vizinho em $/unidade e savings (o "Economist effect": o tier que ninguém escolhe move 84% pro combo).
- **Charm pricing** nos preços de bundle (terminação em 9) — exceto se o posicionamento for premium (aí round numbers). Mostrar sempre o "was" (3× solo riscado) ao lado do preço do bundle: transaction utility = a alegria da pechincha vem do gap entre a âncora e o preço real.
- **Savings segregado** ("You save $Z (28%)") — mental accounting: ganho listado à parte é um ganho a mais.

(A psicologia dos 4 bullets acima vem da **Pricing Psychology Suite** — query no item 3 de "Antes de Começar", não re-puxe.) Puxe os SISTEMAS NOMEADOS específicos da renderização:
- **AOV Builders (Bundles, GWP, Thresholds, Order Bump, Upsell)** (rode `checkout optimization AOV order bump upsell gift with purchase bundle threshold money close`) — o cardápio completo de construtores de AOV e o money close do fechamento.
- **Mecânica visual de pricing table + prioridades de A/B do checkout** (rode `preço baixo grande preço alto pequeno, remover cifrão em produto caro, ordem de ROI dos testes de checkout`) — a anatomia visual da buy box: preço baixo em fonte grande, preço de âncora pequeno, remover o cifrão em produto caro, e a ordem de ROI dos testes de checkout (reaparece na Fase B).
- **3 Tipos de Desconto Shopify + funil de sale congruente** (rode `automatic discount aparece no carrinho, only apply discount once per order, economia visível em cada etapa`) — automatic discount aparece no carrinho (código digitado não), "only apply once per order" na config, e a economia visível em CADA etapa do funil.

**Caminho real Shopify:**
1. **Variantes de bundle** (3-pack e 6-pack como variantes ou produtos separados com seu próprio SKU/preço) renderizadas no bloco de pricing-tier da PDP (o block type `pricing_tier` da 07b, com settings `qty` + `variant_id`). Caminho mais simples, no-code, e o que casa diretamente com a página já buildada.
2. **Bundle fixo nativo via Admin GraphQL `productBundleCreate`** — o ÚNICO pedaço do stack de AOV 100% automatizável via API/CLI: cria o bundle como produto de verdade (componentes + inventário calculado deles), em qualquer plano, sem app de terceiro. Automação pronta na recipe `.claude/automations/recipes/create-fixed-bundles.md` (cria os tiers do 04 e devolve os variant IDs pro wire da PDP). Recomendado quando há Admin API/MCP conectado.
3. **Quantity-break / volume discount via Shopify Function** (discount "buy X get Y% off" / tiered) — preço por unidade cai conforme a quantidade. **Nuance de plano:** custom function via CLI (`shopify app generate extension --type product_discounts`) só roda em **Shopify Plus** (custom app com Function é Plus-only); pra não-Plus, o caminho é **app público da App Store com Functions embutidas** ou o app nativo **Shopify Bundles**. NUNCA sugira a rota CLI custom pra starter/validating.
4. **App de bundle** (ex: Shopify Bundles nativo, Fast Bundle, Bundler) — gera o bundle product + desconto sem código.

Recomendar o caminho 1 (variantes na PDP) pra starter/validating — zero app, zero função, e o pricing block do tema já existe; o caminho 2 quando houver Admin API/MCP (mesmo resultado, automatizado). Function/app só quando o membro quer quantity-break dinâmico ou mix-and-match.

**Gate anti-Shopify-Scripts (OBRIGATÓRIO ao validar app já instalado):** Shopify Scripts (Ruby) morreram em 30/jun/2026 (edição congelada desde abr/2026). Se o membro já tem app de desconto/bundle/shipping instalado, confirme que ele NÃO roda sobre Scripts — app legado baseado em Script = desconto que desaparece no checkout sem aviso. Como checar: página do app na App Store menciona "Shopify Functions"/"Checkout Extensibility"? App atualizado depois de 2024? Em dúvida, teste um pedido: o desconto aparece no checkout? Se o app é Script-based, migre pro equivalente com Functions ANTES de configurar qualquer alavanca sobre ele.

**Guardrail de margem (net AOV, não AOV bruto):** desconto de 15% num bundle que sobe o AOV em 30% derruba a margem de contribuição 6-7 pontos percentuais, A MENOS que >20% dos pedidos do bundle sejam incrementais de verdade (gente que não compraria o solo full-price). A 04 ETAPA 5/6 já roda esse check — se você mudar preço/savings de tier aqui, re-valide contra a `weighted_margin_per_order` antes de aplicar (bundle se avalia por margem de contribuição líquida, nunca por AOV bruto).

### Alavanca 4 — Free-shipping threshold

Empurra o cliente a adicionar mais um item pra cruzar a linha. Funciona por **zero price effect** (frete REALMENTE $0, não "quase") + **mental accounting** (o "free shipping over $X" é um ganho dentro do frame) — os dois já puxados na **Pricing Psychology Suite** do item 3. Threshold típico ≈ 1.3-1.5× do AOV atual (perto o bastante pra ser alcançável, alto o bastante pra forçar o item extra). Puxar `aov_expected` do 04 pra calcular. Fundamento com números de operação: **Profit Optimization 4 Categories + AOV Builders** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — threshold, volume discount e GWP julgados por lucro-por-visitante, nunca por AOV bruto.

**Caminho real Shopify:**
1. **Shipping rate condicional** — Settings → Shipping and delivery → criar rate "Free" com condição "Order price ≥ $X" na zona do target market. Esta é a fonte da verdade que o **Gate Promise↔Config (pre-launch-gates)** valida: se a copy promete "Free shipping over $75" mas a zona não tem essa rate configurada, é `fail` e bloqueia.
2. **Barra de progresso de free-shipping** no cart/drawer — bloco do tema ("You're $12 away from free shipping") que atualiza via JS conforme o subtotal. Editável como block (copy default do 04, em inglês US). Caminho do tema, dentro de `shopify-theme-safety`.
3. **App de progress bar** (ex: Hextom Free Shipping Bar) — no-code se o membro preferir.

### Alavanca 5 — Checkout trust (badges / garantia / reviews)

Reduz a ansiedade no momento mais nervoso do funil (digitar o cartão). Pós-`checkout.liquid`, o checkout só aceita customização via **Checkout UI Extensions** — não dá pra colar HTML solto. Onde colocar:

1. **Checkout UI Extension** nos blocks do checkout — trust badges (secure payment, money-back), a garantia do 04 (ex: "90-day money-back"), e 1-2 reviews curtos. **Shopify Plus only** (customização in-checkout via extension exige Plus) + app container. Sem Plus, pule direto pros caminhos 2-3.
2. **Checkout branding** (Settings → Checkout → customize / brand) — logo, cores, e os trust elements suportados nativamente sem extension. Caminho no-code pro que o branding API expõe.
3. **Trust row na PDP/cart** (caminho do tema) — como o checkout em si é restrito, a maior parte da prova de confiança vive na PDP e no cart (trust badges com **ícones SVG, nunca emoji** — regra 7 do CLAUDE.md: cadeado, caminhão, escudo de garantia, estrelas de review em SVG inline 16-18px). É onde o membro tem controle total e onde 80% do efeito acontece antes do checkout.

A garantia exibida tem que bater com a `guarantee` do 04 E com a policy page da loja (Gate Promise↔Config: "90-day money-back" na trust row exige policy declarando 90 dias). Os números de review ("Rated 4.8 by 2,300 customers") exigem que o review app (Judge.me/Loox/Yotpo) tenha esses números reais — senão é `fail` no gate.

## Fluxo da Skill

### ETAPA 1 — Carregar a oferta e mapear o que já existe

**Onde cada spec vive no 04 (fontes reais, não campos imaginários):** o `04-offer-builder/dados.json` traz os campos estruturados `pricing` (`main_sku_price`, `aov_expected`), `unit_economics`, `guarantee`, `offer_stack` (string), `bonuses[]` e — **fonte primária dos detalhes de alavanca** — o bloco **`aov_levers`**: `bump` (name, price, copy, take_projected), `upsell` (name, price, anchor_was, oto_structure, take_projected) e `bundles[]` (`{qty, price, label, savings_pct}`). Leia os detalhes de bump/upsell/bundle DESSE bloco. **Fallback legado** (dados.json gerado antes do contrato, sem `aov_levers`): os mesmos detalhes vivem na **Etapa 3 do `04-offer-builder/offer-builder.md`** (prosa estruturada) — leia de lá; se nem o relatório existir, reconstrua com o membro em vez de inventar. Alavanca `null` no bloco (ex: `"upsell": null`) = a oferta não tem essa alavanca → registre `not_in_offer`, não force. Monte a tabela do que a oferta JÁ definiu vs. o que falta implementar:

| Alavanca | Definido no 04? | Valor/spec (fonte) | Caminho Shopify escolhido | Status |
|---|---|---|---|---|
| Post-purchase upsell | `aov_levers.upsell` (fallback: Etapa 3 do offer-builder.md) | nome, preço, take projetado | app / extension / thank-you | a configurar |
| Cart/order bump | `aov_levers.bump` (fallback: Etapa 3 do offer-builder.md) | complemento, preço, copy | tema / extension / app | a configurar |
| Bundles | `aov_levers.bundles[]` + `pricing` (fallback: Etapa 3 do offer-builder.md) | Solo/3/6, savings, Popular | variantes PDP / native_bundle / function / app | a configurar |
| Free-shipping threshold | derivado de `pricing.aov_expected` | threshold = 1.3-1.5× AOV | shipping rate + bar | a configurar |
| Checkout trust | `guarantee` + reviews | tipo de garantia, # reviews | checkout extension / branding / PDP | a configurar |

Se uma alavanca não foi definida no 04 (ex: oferta sem upsell), não a force — registre como `not_in_offer` e siga. Não inventar um upsell que a unit economics não sustenta.

**Gate de Complementaridade (C14 — aplicado às superfícies de checkout):** todo componente de AOV que passar por aqui (bump, upsell, bundle-mate, GWP) já deve ter passado no Gate da 04 ETAPA 3 — as 4 categorias, nesta ordem de prioridade: **(1) more-of-same** (mais unidades do próprio produto), **(2) consumption chaining** (item consumido JUNTO no mesmo ritual de uso), **(3) aceleração de resultado** (encurta o time-to-result do desejo central), **(4) problema adjacente** (o próximo problema depois do resultado). Se o membro trocar o produto de um bump/upsell NESTA skill (ex: "usa o sérum X no lugar"), re-rode o gate: em qual das 4 categorias o novo componente cai? Nenhuma → reprove e derive candidatos do market research (ritual de uso, desejo central, jornada), como a 04 faz. Registre a categoria no `dados.json` (`complementarity_category`).

### ETAPA 2 — Pergunta ao membro (APENAS o que é input externo)

Não pergunte estratégia. Pergunte só o que você não consegue inferir:

1. **Apps já instalados?** "Você já tem algum app de upsell/bump/bundle/desconto instalado? Se sim, qual?" — define caminho no-code vs. nativo, E dispara o gate anti-Shopify-Scripts da Alavanca 3 (app legado = desconto que some no checkout).
2. **Gateway de pagamento**: "Qual gateway você usa — Shopify Payments/cartão, ou o checkout é majoritariamente wallet (Apple Pay/Shop Pay/PayPal)?" — post-purchase one-click funciona em qualquer plano, mas o OTO NÃO aparece pra pagamento via wallet; se a loja é wallet-heavy, desconte o take projetado e reforce cart bump/bundle (que não dependem do método de pagamento). Pergunte também se a loja é Plus SÓ se algum caminho escolhido exigir (order bump in-checkout, trust blocks no checkout, custom Function via CLI).
3. **In-box gift?** (só se algum bonus do 04 for físico/in-box): "O brinde físico vai junto na caixa? Aí é coordenação com fulfillment, não config de loja." — separa o que é config do que é operação.

Para **starter**, default no-code: app único que cobre bump + upsell + bar, ou caminho do tema pros bundles. Não recomendar app pago se o membro tem budget apertado e o caminho nativo resolve.

### ETAPA 3 — Especificar cada alavanca (blueprint implementável)

Para cada alavanca ativa, produza um spec concreto e aplicável (não prosa genérica):

- **Pricing exato** com charm pricing aplicado e a âncora ("was $X / now $Y").
- **Copy real** (inglês US, ad-safe pela regra 8b, sem travessão em headlines pela 8a) — bump (1 frase + benefício), upsell (2-3 frases + benefício + oferta), bundle labels (Popular/Best Value), free-shipping bar ("You're $X away from free shipping"), trust row (garantia + badges).
- **Caminho técnico** escolhido (tema / Function / extension / app) com os passos reais.
- **Onde aplicar** (qual arquivo do tema, qual setting do admin, qual painel do app).
- **Aceitação projetada** (do 04 ou benchmark da base) e impacto no AOV.

### ETAPA 4 — Reconciliar o AOV e a economics (fonte única, SEM contagem dupla)

**Regra de ouro: o `pricing.aov_expected` do 04 JÁ INCLUI bump e upsell** (a Etapa 6 do 04 soma `bump acceptance × preço` + `upsell acceptance × preço` no AOV projetado, e a `weighted_margin_per_order` é ponderada por esse AOV). O papel desta skill é **REALIZAR** essa projeção na loja, não somá-la de novo — re-adicionar as alavancas sobre `aov_expected` infla o "novo target CPA" que a Skill 10 usaria em decisão de spend real.

Monte a reconciliação em 3 números:

- **AOV sem alavancas** (baseline de referência): recompute do 04 — o mix solo/bundle SEM os termos de bump/upsell (ou `main_sku_price` se a oferta é single-tier). Serve pra mostrar ao membro quanto o stack de checkout vale.
- **AOV projetado** (a fonte única): o próprio `pricing.aov_expected` do 04 **quando as alavancas implementadas aqui são as mesmas que o 04 projetou** — o caso normal; o delta desta skill é ≈ 0 por definição, e `manifest.target_cpa`/`breakeven_roas` do 04 continuam válidos.
- **Ajuste SÓ por diferença de escopo**: se esta skill implementa alavanca que o 04 NÃO projetou (ex: free-shipping threshold mudou o mix, ou um bump novo passou no Gate), ou DEIXA DE implementar alavanca projetada (ex: upsell ficou `not_in_offer`), recalcule o AOV/margem com os mesmos benchmarks do 04 (bump 20-35%, upsell 3-8%/8-14%) e documente item a item o que entrou/saiu do cálculo.

Se (e somente se) o ajuste de escopo mudou a economics: registre o novo `target CPA` viável (= nova margem ponderada / 2 ou / 3 — é o múltiplo do ROAS de BREAKEVEN, não ROAS literal) e atualize `manifest.target_cpa` + `manifest.breakeven_roas` quando a config for de fato aplicada — a Skill 10 lê do manifest.

> **Não sobrescreva** `weighted_margin_per_order` no `04-offer-builder/dados.json` (é a fonte da unit economics). Grave a reconciliação em `07d-checkout-aov/dados.json` e atualize `manifest.aov_baseline` se a config foi de fato aplicada na loja (não só planejada). A Skill 11 reconcilia com o AOV real medido depois (lembrando que o valor do OTO post-purchase não entra no Purchase do pixel — ver "Quando Usar").

### ETAPA 5 — Aplicar na loja (se store_url existe) ou entregar blueprint

**Se a loja existe e o membro aprovou o blueprint** (checkpoint de iteration-driven-refinement — "Aprova a direção ou ajusto pricing/copy?"):

- **Caminhos do tema** (cart bump, free-shipping bar, trust row na PDP): operar no tema onde a página vive — `THEME_ID = manifest.storefront.theme_id` (gravado pela 07b na publicação; se é o live, os comandos levam `--allow-live`). Seguir `shopify-theme-safety` INTEGRAL, sempre com `--path` explícito (Regra 8 proíbe push sem `--path`):
  ```bash
  shopify theme pull --theme "$THEME_ID" --store "$STORE" --path workspace/[produto]/07-page/theme-clone --nodelete
  # editar → marker data-aura-build no root da section editada (Regra 4 — atributo de dados, NUNCA comentário Liquid)
  shopify theme push --theme "$THEME_ID" --store "$STORE" --path workspace/[produto]/07-page/theme-clone --nodelete [--allow-live se THEME_ID é o live]
  # verificação: curl -s <página> | grep data-aura-build  → depois smoke test (Regra 7)
  ```
  O iteration loop dá `pull` antes de re-push pra não sobrescrever settings do theme editor.
- **Caminhos de admin** (shipping rate, checkout branding, discount function via app): documentar os passos exatos do painel (não dá pra automatizar tudo via CLI) — ex: "Settings → Shipping → Add rate → condition Order price ≥ $75 → price $0.00".
- **Caminho nativo automatizável** (bundles fixos): recipe `.claude/automations/recipes/create-fixed-bundles.md` (Admin GraphQL `productBundleCreate` — cria os tiers e devolve variant IDs pro wire da PDP).
- **Caminhos de app**: NENHUM app de upsell tem API pública de configuração — gere o **config spec** (produto, preço, copy, downsell, IDs de variante reais) pro membro colar no painel do app. IDs de variante: pedir ao membro ou ler via Admin API/MCP se conectada.

**GATES (blocking — pre-launch-gates):**
- **GATE 1 — Ad-flag compliance** sobre TODA copy de checkout/cart injetada (bump, upsell, bar, trust) ANTES de aplicar, via CLI canônica: `python3 .claude/lib/compliance-preflight/run.py --text "<copy>" --vertical <manifest.product_vertical> --stage pre_page --json`. Decisão pelo `overall_verdict`: `critical` bloqueia; `warning` bloqueia por default — aplicar as `rewrite_suggestions[]` e re-checar.
- **GATE 2 — Promise↔Config**: o free-shipping threshold da copy tem que existir como shipping rate real; a garantia exibida tem que bater com a policy page; os números de review têm que existir no review app. `fail` ≥ 1 → não aplicar, reportar o `fix`.

**Se a loja NÃO existe** (`pending_store: true`): entregar o blueprint completo, marcar cada alavanca como `pending` no JSON, e avisar no output final que aplica assim que a 07b deployar a loja. Sem inventar IDs de variante nem aplicar nada.

### ETAPA 6 — Member-stage (profundidade da implementação)

- **Starter** (0-30 dias, budget apertado): 1-2 alavancas de maior alavancagem e menor esforço — geralmente **bundle na PDP** (zero app, já tem o pricing block) + **free-shipping bar** (tema). Post-purchase via ReConvert se o membro quiser (custo quase zero — ver matriz), nunca extension custom. Explicar o porquê de cada escolha (educação embutida).
- **Validating** (30-90 dias): adicionar **cart bump** + **um app de upsell** no-code (matriz abaixo). Trust row na PDP. Começar a medir take rates reais.
- **Scaling** ($5k+/mês): stack completo — post-purchase one-click via app (ou extension custom se houver dev), quantity-break via Function (app público; CLI custom só em Plus), checkout trust via extension (Plus), bundle nativo automatizado. A margem extra justifica o custo de app premium.

Não recomende post-purchase extension custom pra starter com $500/mês; não deixe um scaling com $20k/mês só com bundle na PDP (desperdiça a alavanca de upsell one-click).

### ETAPA 6b — Matriz de apps de upsell por estágio (curadoria 2026)

Não existe app vencedor universal — existe vencedor por superfície e estágio. Critério de decisão por preço/volume:

| Stage | App default | Preço | Por quê |
|---|---|---|---|
| **Starter / validating** | **ReConvert** | $4.99/mês + 0.75% de comissão sobre a receita de upsell | Custo alinhado ao resultado (quase zero risco); lift comprovado ~15%; cobre post-purchase + thank-you |
| **Validating / scaling** | **AfterSell** | $34.99/mês até 500 pedidos | Quando o volume faz a comissão do ReConvert passar o flat fee; A/B nativo com milhares de variações |
| **Scaling com funil multi-step** | **Zipify OCU** | flat acima de 5k pedidos | Único com lógica de funil post-purchase de múltiplos passos; aceitação 8-14% auditada em oferta bem casada |
| **Enterprise (~$1M+/mês, catálogo grande)** | **Rebuy** | $99 a $1.000+/mês por volume | Recomendação por AI só compensa com catálogo profundo; pro membro típico Aura (1-3 SKUs hero), a OFERTA da 04 decide o upsell melhor que algoritmo cego — documentar como teto, nunca default |

**Regra transversal:** nenhum desses apps expõe API pública de configuração — o setup é painel manual. Esta skill gera o **config spec** completo (produto, preço com âncora, copy, downsell, ordem das ofertas) pro membro colar no painel; a automação de verdade fica no caminho nativo (bundles via `productBundleCreate`, shipping rate via admin).

### Fase B — teste de backend (cadência recorrente, pós-launch)

A primeira rodada desta skill arma o stack ANTES do tráfego. Com pedidos reais rodando, o backend não fica parado: ele **re-testa em ciclos** — e re-testar backend é mais barato que testar criativo, porque usa o tráfego que já foi pago.

- **Quando re-rodar:** quando a Skill 11 já tem leitura de funil com amostra mínima (a régua da ETAPA 6B dela) — take rate lido com meia dúzia de pedidos é ruído, não sinal.
- **Uma variável por ciclo** (mesmo método científico dos ads): trocar o produto do OTO (re-rodando o Gate de Complementaridade), preço/âncora do upsell, o downsell (fórmula do Haddad — Alavanca 1), ordem/labels dos tiers, valor do threshold. A ORDEM dos testes segue a ordem de ROI dos testes de checkout (**Mecânica visual de pricing table**, já puxada na Alavanca 3 — não re-puxe).
- **A leitura é da Skill 11 (handoff):** take rates reais vs projetados por alavanca, com o revenue do OTO reconciliado no Shopify — o Purchase do pixel não vê o valor do one-click ("Quando Usar"). Cada ciclo atualiza os `take_projected` do `dados.json` com os medidos e re-roda a reconciliação da ETAPA 4 (as regras de `scope_diff` continuam mandando em `manifest.target_cpa`/`breakeven_roas`).
- **O que a Fase B NÃO é:** escala de ads (Skill 12) nem campanha de email (Skill 13 Fase B). É o backend — upsell/downsell/bundle/threshold — re-testado em ciclos enquanto os ads rodam.

## SALVAR (dual output — rule 6b do CLAUDE.md)

Salvar em `workspace/[produto]/`:

**`07d-checkout-aov/checkout-aov.md`** (humano) contendo:
1. Mapa das 5 alavancas: definida no 04? caminho Shopify? status (aplicada/pending/not_in_offer) + categoria do Gate de Complementaridade
2. Spec de cada alavanca ativa (pricing com charm, copy real, caminho técnico, onde aplicar/config spec do app, aceitação projetada)
3. Reconciliação de AOV (sem alavancas → projeção do 04 → ajustes de escopo, se houver) + o target CPA que vale pra Skill 10 (explicitando: "2×" = 2× o ROAS de breakeven, metade da margem vira lucro)
4. Resultado dos gates (compliance + promise↔config + anti-Scripts se houve app instalado)
5. Passos de aplicação (tema / admin / app / recipe nativa) e o que ficou pending

**`07d-checkout-aov/checkout-aov.html`** (companion humano) — usar `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained). **Logo SVG no topo do `<body>`, copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA texto.** Componentes aura (kpi-grid pro AOV antes/depois, table-wrap pro mapa de alavancas, callout/note/danger pros gates). Ícones SVG, nunca emoji, em qualquer preview de checkout/cart consumidor-final (regra 7).

**`07d-checkout-aov/dados.json`** (estruturado; o contrato com a Skill 10 passa pelo MANIFEST — `aov_baseline`/`target_cpa` — e as recipes de automação leem `levers.bundles.tiers` daqui):

```json
{
  "product_slug": "<do manifest>",
  "store_url": "<do manifest ou null>",
  "theme_id": "<manifest.storefront.theme_id ou null>",
  "applied_to_store": false,
  "pending_store": false,
  "levers": {
    "post_purchase_upsell": { "active": true, "path": "app|extension|thankyou", "app": "reconvert|aftersell|zipify_ocu|rebuy|null", "complementarity_category": "more_of_same|consumption_chaining|result_acceleration|adjacent_problem", "price": 49, "anchor_was": 79, "take_projected": 0.08, "oto_structure": "more_of_same|next_thing|do_it_faster|need_help", "status": "applied|pending|not_in_offer" },
    "cart_bump": { "active": true, "path": "theme|extension|app", "complementarity_category": "consumption_chaining", "price": 17, "take_projected": 0.20, "status": "applied" },
    "bundles": { "active": true, "path": "pdp_variants|native_bundle|function|app", "tiers": [{ "qty": 1, "price": 49 }, { "qty": 3, "price": 119, "label": "Popular" }, { "qty": 6, "price": 199, "label": "Best Value" }], "psychology": ["extremeness_aversion", "decoy", "charm_pricing"], "status": "applied" },
    "free_shipping_threshold": { "active": true, "threshold": 75, "path": "shipping_rate+bar", "status": "applied" },
    "checkout_trust": { "active": true, "path": "pdp_trust_row|checkout_extension|branding", "guarantee": "90-day money-back", "review_count": 2300, "status": "applied" }
  },
  "aov_reconciliation": {
    "aov_no_levers": 97.00,
    "aov_projected_04": 118.00,
    "scope_diff": [],
    "aov_final": 118.00,
    "weighted_margin_final": 72.00,
    "target_cpa_2x_breakeven_multiple": 36.00,
    "target_cpa_3x_breakeven_multiple": 24.00,
    "manifest_updated": false
  },
  "gates": {
    "compliance": "pass|warn|block",
    "promise_config": { "pass": 3, "warn": 0, "fail": 0, "items": [] }
  }
}
```

Notas do schema:
- `gates.promise_config.items[]` detalha os `warn`/`fail` — inclusive o check de consistência de assinatura (superfície com desconto de assinatura, ou preço divergente de `subscription_architecture`/`onetime_premium_pct` da 04, entra como `warn` com o par esperado-vs-configurado; a Skill 09 herda pelo C4).
- `aov_reconciliation` substitui a antiga "projeção nova": no caso normal (alavancas = as que o 04 projetou), `aov_final == aov_projected_04` e `scope_diff` fica vazio — o delta é ≈ 0 por definição (ETAPA 4) e `manifest_updated: false`. Só quando `scope_diff` lista alavancas que entraram/saíram fora do plano do 04 é que `aov_final`/`weighted_margin_final` divergem e o manifest é atualizado.
- Os campos `target_cpa_*_breakeven_multiple` seguem a convenção do 04/11: margem final ÷ N — múltiplo do ROAS de BREAKEVEN, não ROAS literal.
- `levers.bundles.tiers` (`{qty, price, label}`) é o contrato lido pelas recipes `deploy-shopify-product.md` e `create-fixed-bundles.md`.

Atualizar `manifest.json`: adicionar `07d-checkout-aov` em `skills_completed`; se aplicado de fato na loja, atualizar `aov_baseline` com o `aov_final` e — SÓ se `scope_diff` não-vazio — `target_cpa` + `breakeven_roas` (a Skill 10 lê do manifest). Não sobrescrever `04-offer-builder/dados.json`.

Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html), onde `<slug>` é o `product_slug`.

## Mensagem Final

Primeira versão como **draft**, não "pronto" (iteration-driven-refinement):

"Primeira versão do stack de checkout/AOV pronta. Implementei [N] alavancas: [lista curta — ex: bundle 3-tier na PDP, cart bump $17, free-shipping bar em $75, trust row].

Sem as alavancas, o pedido médio ficaria em **$X**; com o stack aplicado, a projeção da oferta é **$Y** de AOV — este stack é o que faz esse número acontecer de verdade. [SE `scope_diff` não-vazio: 'Como implementamos [alavanca] além do planejado, o CPA máximo que você pode pagar subiu de $A pra $B — atualizei o número que a campanha vai usar. Esse teto é calculado pra 2× o ROAS de breakeven, ou seja, metade da margem de cada pedido vira lucro.']

Revisa o pricing e a copy e me diz o que ajustar: o threshold de free-shipping tá no ponto certo? O preço do upsell faz sentido? Itero até ficar redondo.

Próximo passo: diga **'creatives'** pra gerar os anúncios (já com o AOV/CPA correto) — ou **'tracking'** se o pixel/CAPI ainda não tiver sido configurado. E quando os pedidos estiverem rodando e a análise de ads já tiver leitura de funil, me chama de novo com **'checkout'**: a Fase B re-testa o backend em ciclos (upsell, downsell, bundle, threshold) usando o tráfego que você já pagou."

---

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) NENHUMA alavanca foi re-somada sobre `aov_expected` (contagem dupla — a reconciliação da ETAPA 4 bate: caso normal `aov_final == aov_projected_04` e `scope_diff` vazio); (2) todo bump/upsell/bundle-mate/GWP tem `complementarity_category` de uma das 4 categorias (componente sem categoria = reprovado, não aplicado); (3) copy de checkout/cart em inglês US, ad-safe (GATE 1 via CLI canônica), promessas batendo com config (GATE 2 — threshold como shipping rate real, garantia = policy page, reviews reais); (3b) superfícies de assinatura obedecem `subscription_architecture` + `onetime_premium_pct` da 04 (nenhum desconto de assinatura em upsell/OTO — o framing é o prêmio do one-time; arquitetura 2 = checkout sem push de assinatura; campos ausentes = fallback legado anotado; divergência = `warn` em `gates.promise_config.items[]`, nunca silenciada); (4) caminho recomendado respeita o plano da loja (nada de extension in-checkout ou Function custom pra não-Plus) e nenhum app instalado roda sobre Shopify Scripts; (5) operações de tema usaram `--path` + o `theme_id` do `manifest.storefront` + marker `data-aura-build`; (6) `dados.json` + `checkout-aov.md` + `checkout-aov.html` (logo SVG) salvos e manifest atualizado (`skills_completed`, `aov_baseline` se aplicado, `target_cpa`/`breakeven_roas` SÓ se `scope_diff` não-vazio). Issue dentro do escopo → fix inline. Decisão do membro (ex: trocar produto do bump, aceitar take menor por loja wallet-heavy) → surface curto.
