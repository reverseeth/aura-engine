---
name: checkout-aov
description: Engine de AOV na fase storefront, depois do tracking e antes dos criativos. Implementa na loja Shopify as 5 alavancas que a offer-builder já definiu e aprovou no Gate de Complementaridade (post-purchase upsell one-click, cart bump, bundle e quantity-break com pricing psychology, free-shipping threshold e checkout trust) pelo caminho real por plano e estágio (variantes na PDP, bundle nativo via productBundleCreate, Functions por app público, matriz de apps ReConvert, AfterSell e Zipify OCU com config spec, porque nenhum app tem API de configuração), obedece as superfícies de assinatura do contrato da oferta, reconcilia o AOV sem contagem dupla (o aov_expected da oferta já inclui bump e upsell) e só atualiza target_cpa e breakeven_roas no manifest quando o escopo muda; a Fase B re-testa o backend em ciclos com o tráfego já pago. Use quando o membro disser "checkout", "upsell", "aov", "bump", "bundle", "order bump", "free shipping", ou depois do tracking instalado e antes de gerar criativos. É a maior alavanca de lucro por visitante fora dos ads.
---

# Checkout & AOV · Passo 10 · apelido antigo: 07d <!-- gen:title -->

## Quando usar

Na fase storefront, depois da página no ar (`page-build`) e do tracking instalado (`tracking-setup`), antes dos criativos (`creative-engine`): a página precisa existir pra ter variantes referenciáveis, o pixel precisa medir bump e bundle no Purchase, e o AOV configurado aqui muda o CPA que o briefing de ad usa. A oferta definiu bumps, upsells e bundles; esta skill os implementa. Cada dólar extra de margem por pedido é um dólar a mais de CPA que dá pra pagar, sem tráfego novo. Limitação conhecida: o Purchase da integração nativa dispara antes do aceite do upsell one-click, então o valor do OTO não entra no pixel (a `ad-analysis` reconcilia com o Shopify).

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` e `profile.md`; ausentes, oferecer rodar o `setup` inline.
2. `offer-builder/dados.json` (`bonuses[]`, `pricing`, `unit_economics`, `guarantee`, `offer_stack`, `aov_levers` e o contrato de assinatura `subscription_architecture` com `onetime_premium_pct`); faltando, escape ES1: (A) rodar a `offer-builder` ou (B) defaults conservadores marcando `skipped_preflight`.
3. `manifest.store_url` e `manifest.storefront` (`theme_id` e `page_url`, gravados pela `page-build`): esta skill opera no mesmo tema da página; loja ausente, (A) rodar a `page-build` ou (B) entregar o blueprint com `pending_store: true`, sem inventar IDs de variante; tema não publicado, avisar que a publicação precisa acontecer antes do launch.
4. Stage do membro (`manifest.stage` ou a rule `member-stage-awareness`): define a profundidade (starter com 1 a 2 alavancas no-code; scaling com o stack completo).

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`) em todo output interno; a copy do checkout e do cart (bump, upsell, trust, barra de frete) fica sempre em inglês US.
2. `offer-builder/offer-builder.md` (legado `relatorio.md`) e o `dados.json`: bundles, bump, upsell, stack, garantia e unit economics; os números de aceitação projetados e o AOV projetado são a fonte única, aqui viram config real sem re-somar.
3. Base pelo índice (domínios `page-landing-cro`, `brand-building-bonus-aov`, `offer-pricing-guarantee`): `python3 .claude/lib/kb-index/kb_lookup.py --skill checkout-aov --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa; os cinco sistemas de `reference/contexto.md` e os embutidos em cada alavanca são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida. Não consulte o membro sobre estratégia (tier âncora, % de savings), só sobre input externo.

## As 5 alavancas e o caminho real no Shopify

O checkout hoje exige Checkout UI Extensions e Shopify Functions; não existe editar o `checkout.liquid`. Leia o arquivo de cada alavanca antes de especificá-la.

- **Alavanca 1, post-purchase upsell one-click** (`reference/alavanca-post-purchase-upsell.md`): aceitação de 3% a 8% na média e de 8% a 14% em oferta bem casada; funciona em qualquer plano via app, mas não aparece em wallet (desconte do take), 1 app por loja, 3 ofertas por checkout. Caminhos: app (config spec pro painel), extension custom só pra scaling com dev, thank-you page como último recurso (nunca "additional scripts", desligado). Estrutura do OTO pelos sistemas do arquivo (Next Thing, Do It Faster, Need Help; os 5 tipos de upsell pela contribuição em AOV; a escada de upsell e downsell); more-of-same primeiro pra comprador novo. Superfícies de assinatura obedecem o contrato: `subscription_first` nunca desconta a assinatura (o prêmio do one-time é o diferencial; adoçante é produto grátis), `onetime_plus_sub_no_reorder` não empurra assinatura no checkout, `no_subscription` não tem superfície; campos ausentes é fallback legado anotado.
- **Alavanca 2, cart e order bump** (`reference/alavanca-cart-bump.md`): checkbox de complemento aprovado no Gate, low-ticket e high-margin, aceitação projetada de 20% a 35%; bumps de margem quase pura (shipping protection, priority processing) só se o membro entrega o que prometem; caminhos: bloco no cart do tema (qualquer plano), extension in-checkout (Plus), app.
- **Alavanca 3, bundle e quantity-break** (`reference/alavanca-bundle.md`): 3 tiers sempre, o do meio como alvo, decoy, charm pricing, "was" riscado e savings segregado; caminhos: variantes na PDP (block `pricing_tier` da `page-build`, default pra starter e validating), bundle nativo por `productBundleCreate` (recipe `.claude/automations/recipes/create-fixed-bundles.md`, o único caminho 100% automatizável), Function via app público (CLI custom só em Plus), app de bundle. Gate anti-Shopify-Scripts em app já instalado; guardrail de margem líquida, nunca AOV bruto.
- **Alavancas 4 e 5, free-shipping threshold e checkout trust** (`reference/alavanca-free-shipping-e-trust.md`): threshold de 1,3 a 1,5 vezes o AOV com frete realmente zero, shipping rate condicional mais barra de progresso no tema; trust por extension (Plus), checkout branding ou trust row na PDP e no cart com ícones SVG, garantia da oferta e números do review app.

## Fluxo da skill

### ETAPA 1 · Carregar a oferta e mapear o que já existe

Leia `reference/mapear-e-perguntar.md`. Detalhes de bump, upsell e bundles vêm de `aov_levers` (fallback: a Etapa 3 do relatório da oferta; sem relatório, reconstrua com o membro); alavanca `null` vira `not_in_offer`, nunca forçada. Monte a tabela das 5 alavancas (definida?, spec e fonte, caminho Shopify, status). Gate de Complementaridade nas 4 categorias (more-of-same, consumption chaining, aceleração de resultado, problema adjacente); componente trocado pelo membro re-roda o gate e grava `complementarity_category`.

### ETAPA 2 · Perguntar ao membro só o que é input externo

Mesmo arquivo. Apps instalados (dispara o gate anti-Scripts), gateway de pagamento (loja wallet-heavy desconta o take do OTO; Plus só se o caminho exigir) e brinde físico in-box (operação, não config). Starter: app único no-code ou caminho do tema.

### ETAPA 3 · Especificar cada alavanca (blueprint implementável)

Leia `reference/blueprint-e-reconciliacao.md`. Por alavanca ativa: pricing exato com charm e âncora, copy real em inglês US (direta e sem aviso, sem travessão em headline), caminho técnico com os passos, onde aplicar, aceitação projetada e impacto no AOV.

### ETAPA 4 · Reconciliar o AOV sem contagem dupla

Mesmo arquivo. `pricing.aov_expected` já inclui bump e upsell: realize a projeção, não a some de novo. Três números: AOV sem alavancas, AOV projetado (a fonte única; caso normal com delta zero) e ajuste só por diferença de escopo (alavanca fora do plano da oferta ou projetada e não implementada), com os mesmos benchmarks. Só nesse caso o target CPA (margem ponderada ÷ 2 ou ÷ 3, múltiplo do ROAS de breakeven) e `manifest.target_cpa` e `breakeven_roas` mudam, e só quando aplicado de fato; nunca sobrescreva `weighted_margin_per_order` da oferta.

### ETAPA 5 · Aplicar na loja ou entregar o blueprint

Leia `reference/aplicar-e-stage.md`. Com loja e blueprint aprovado (checkpoint de iteração): caminhos do tema no `theme_id` do `manifest.storefront` com `shopify-theme-safety` integral (pull, marker `data-aura-build`, push com `--path` e `--nodelete`, verificação e smoke test); caminhos de admin com os passos exatos; bundles fixos pela recipe nativa; apps com config spec e IDs de variante reais. Sem loja, blueprint completo com cada alavanca `pending`.

### ETAPA 6 · Profundidade por stage

Mesmo arquivo. Starter: bundle na PDP e free-shipping bar (ReConvert se quiser); validating: cart bump, um app de upsell, trust row, medir take rates; scaling: stack completo. Nunca extension custom pra starter nem só bundle pra scaling.

### ETAPA 6b · Matriz de apps de upsell por estágio

Mesmo arquivo: ReConvert (starter e validating, comissão sobre a receita de upsell), AfterSell (validating e scaling, flat), Zipify OCU (funil multi-step), Rebuy (enterprise, teto e nunca default). Nenhum tem API de configuração; o config spec é desta skill.

### Fase B · Teste de backend (cadência recorrente, pós-launch)

Leia `reference/fase-b.md`. Quando a `ad-analysis` já tem leitura de funil com amostra mínima, re-teste uma variável por ciclo (produto do OTO com o gate re-rodado, preço e âncora, downsell, tiers, threshold) na ordem de ROI dos testes de checkout; a leitura é da `ad-analysis`, com o revenue do OTO reconciliado no Shopify; cada ciclo atualiza os `take_projected` e re-roda a ETAPA 4. Não é escala de ads nem campanha de email.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `checkout-aov/checkout-aov.md` (mapa das 5 alavancas com categoria do gate, spec de cada ativa, reconciliação com o target CPA explicado, check anti-Scripts, passos de aplicação e o que ficou pending), `checkout-aov.html` por `python3 tools/render_report.py workspace/[produto]/checkout-aov/checkout-aov.md` (SVG, nunca emoji, em preview consumidor-final) e `dados.json` no schema do arquivo (`levers` com status e `complementarity_category`, `levers.bundles.tiers` lido pelas recipes, `aov_reconciliation` com `scope_diff`). Manifest pelo script: `python3 tools/manifest.py <slug> complete checkout-aov`; se aplicado na loja, `set aov_baseline`; só com `scope_diff` não vazio, `set target_cpa` e `breakeven_roas`; e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`: primeira versão como draft, com as alavancas implementadas, o AOV sem e com o stack, o ajuste de CPA só se o escopo mudou, o convite pra revisar pricing e copy, e os próximos passos ('bonus delivery' se há bônus, 'retention', depois 'creatives'; 'tracking' antes de tudo se faltou; 'checkout' de novo pra Fase B). Antes de declarar pronto, o self-audit silencioso dos itens do arquivo.
