---
name: bonus-delivery
description: Pipeline de bônus de ecommerce DTC, em duas fases. Lê os bonuses[] que a offer-builder definiu (nunca inventa bônus), gera o asset entregável quando é digital (e-book, guide ou checklist em PDF com o design da marca, rumo ao dream outcome), configura o gift-with-purchase, o SKU complementar grátis e o gift wrapping na loja (app ou Shopify Function, nunca draft order, coordenado com a checkout-aov), garante o acesso do comprador do dia 1 pela thank-you page e produz o payload do email de entrega que a retention-engine executa. Fase A antes do go-live de ads (todo bônus prometido na PDP precisa existir no dia 1); Fase B pós-launch, com campanha ativa e pedidos, puxa take-rate e access rate agregados por bônus e alimenta a iteração da oferta. Use quando o membro disser "bonus delivery", "bônus", "como entregar o bônus", "configurar GWP", ou depois da oferta definir o stack de valor com bonuses[].
---

# Bonus Delivery · Passo 11 (Fase A) · Passo 20 (Fase B) · apelido antigo: 05 <!-- gen:title -->

## Quando usar

A definição do bônus (qual, valor ancorado, por que entra no stack) é da `offer-builder`; esta skill lê o que foi definido e executa o trabalho operacional que a oferta não faz: gerar o asset digital, configurar GWP na loja, produzir o email de entrega pra `retention-engine` e rastrear access rate e take-rate. Duas fases resolvem o paradoxo de launch: Fase A (logo depois da `checkout-aov`, antes do primeiro ad) deixa todo bônus visível na PDP existindo no dia 1, o que a `consistency-audit` confere no H5; Fase B (pós-launch, junto da Fase B da `retention-engine`, em D+30) puxa os agregados e alimenta a iteração da oferta. Íntegra em `reference/contexto.md`.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/profile.md` e `workspace/[produto]/manifest.json`; `stage` influencia o tipo (starter prioriza e-book e GWP de baixo COGS; scaling sustenta SKU físico).
2. Detecte a fase: Fase B só com a dupla condição (`ad-strategy` em `skills_completed` e campanha de fato ativa ou pedidos no período, porque a `ad-strategy` cria em PAUSED) mais assets e config de todos os bônus existindo; qualquer outra combinação é Fase A.
3. `offer-builder/dados.json` com `bonuses[]` preenchido, cada um com `type` e `condition`; `condition` ausente é inferida (no `offer_stack` da PDP é `unconditional`; GWP com threshold é `cart_threshold`) e gravada de volta na oferta. Ausente ou corrompido, escape ES1: (A) re-rodar a `offer-builder` ou (B) bônus genérico marcando `skipped_preflight`. `bonuses[]` vazio e membro querendo bônus: volte pra `offer-builder`.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`) em toda doc interna e conversa; o asset entregável ao consumidor (PDF, email) é sempre em inglês.
2. `market-research/dados.json` (VOC e desejo) e `offer-builder/dados.json` (mecanismo, `guarantee`, `bonuses[]`) pra ancorar o asset no dream outcome.
3. Base pelo índice (domínio `brand-building-bonus-aov`): `python3 .claude/lib/kb-index/kb_lookup.py --skill bonus-delivery --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa; as queries embutidas nos arquivos de `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida.
4. Os tipos de bônus e o princípio do stack de 2 (`reference/tipos-e-stack-de-dois.md`): os 4 tipos primários que movem AOV num DTC (gift-with-purchase, e-book ou guide rumo ao dream outcome, SKU complementar grátis, gift wrapping em Q4); com mais de um bônus, o primeiro presupõe sucesso no produto (razor-blade, fit natural) e o segundo é o hit hedônico; "free" precisa aparecer visualmente na PDP. Puxe os três sistemas do arquivo antes de modelar o stack.

## Fluxo da skill

### ETAPA 1 · Parse dos bonuses definidos na `offer-builder`

Leia `reference/parse-dos-bonuses.md`. Leia `bonuses[]` no enum canônico (`id`, `name`, `description`, `value_anchored`, `type`, `format_hint`, `condition`, `delivery_trigger`); `type` fora do enum se corrige na `offer-builder`, nunca com mapeamento local. Pra cada bônus, identifique o playbook da ETAPA 2.

### ETAPA 2 · Playbook por tipo

Leia `reference/playbooks-por-tipo.md`. Gift-with-purchase: puxe os três sistemas de calibragem; a `condition` define a mecânica antes de qualquer threshold (`unconditional` é auto-add em toda compra, `cart_threshold` é threshold de 10% a 20% acima do AOV, `tier_specific` é gatilho por variante do tier); sourcing low-COGS com valor percebido alto; implementação por app de GWP ou Shopify Function coordenada com a `checkout-aov`, nunca draft order; "free" visível na PDP com ícone SVG; KPI take-rate. E-book, guide, workbook ou checklist: puxe a Value Equation e o razor-blade; conteúdo real e específico do avatar rumo ao dream outcome, em inglês, PDF com o design da marca do membro em `bonus-delivery/bonuses/[bonus-id]/`, entregue pela thank-you page (a rede de segurança do dia 1) e pelo email post-purchase, hospedado em Shopify Files, S3 ou R2; KPI access rate. SKU complementar grátis: fit confirmado, gatilho por produto no cart ou in-box documentado pro fulfillment; KPI take-rate e attach. Gift wrapping: opção grátis no cart ou checkout, instrução ao fulfillment, personalização por persona quando houver split; KPI attach rate. Discount code: bônus de reorder, com expiração, dimensionado pelos Kennedy Price Minimizers.

### ETAPA 2b · Tipos de subscription e membership (caso de borda)

Mesmo arquivo. `community_access`, `video_series`, `consultation_call` e `trial_extension` só fazem sentido em negócio de assinatura ou membership; bônus de produto físico modelado num deles vai pro membro como decisão de oferta a ajustar na `offer-builder`.

### ETAPA 3 · Email de entrega (integra com a `retention-engine`)

Leia `reference/email-de-entrega.md`. A `retention-engine` é o único executor de email; esta skill produz conteúdo mais trigger como payload. Mapa `delivery_trigger` para o email que entrega (`post_purchase` no Email 1 do post-purchase, `day_7_post_purchase` no Email 3, `on_first_reorder` no replenishment, `on_signup` no welcome; win-back nunca). GWP físico e gift wrapping não precisam de email. O payload nasce na Fase A e a Fase A da `retention-engine` monta o flow em seguida; a thank-you page garante o acesso do dia 1. Template base em inglês no arquivo (subject curto, 1 CTA, reply-to monitorado, unsubscribe).

### ETAPA 4 · Tracking de access rate e take-rate (Fase B)

Leia `reference/tracking.md`. Não existe log por compra; a métrica nasce agregada no re-run (D+30 e a cada ciclo): Shopify Analytics ou Admin API pro take-rate (pedidos elegíveis versus pedidos com o brinde ou o tier), Klaviyo via `retention-engine` pro access rate (abertura e clique do email de entrega). Snapshot por bônus e período em `bonus-delivery/dados.json`, sempre em append. Alarme abaixo de 30%: o bônus não agrega valor percebido, sinal de iteração na `offer-builder`; GWP saudável passa de 50%. Pra ler o take-rate como sinal econômico, puxe o Funnel Economics Profit Map e o PSM.

### ETAPA 5 · Integrações, valor ancorado e regras de rigor

Leia `reference/integracoes-valor-e-rigor.md`: a tabela de integrações (Shopify coordenado com a `checkout-aov`, `retention-engine` como executor de email, hosting do PDF, fulfillment pro in-box), o valor ancorado no varejo do item e o Kennedy Level-2 (quem pede reembolso fica com o bônus, coordenado com a `guarantee` da oferta e a copy da página), os anti-patterns (PDF genérico, bônus de info-product em produto físico, draft order, bônus sem trigger, asset depois do launch, threshold em bônus incondicional, log por compra, código sem expiração, in-box sem fulfillment, threshold abaixo do AOV, sobrescrever o `dados.json`) e as quatro regras de rigor.

## SALVAR

Leia `reference/salvar-e-mensagem-final.md`. `mkdir -p workspace/[produto]/bonus-delivery/bonuses/`; assets por bônus em `bonuses/[bonus-id]/` (design da marca, consumidor em inglês); `bonus-delivery.md` no `report_language` com uma seção por bônus (type, condition, canal, trigger, threshold, path do asset, KPI, status da Fase A); `bonus-delivery.html` por `python3 tools/render_report.py workspace/[produto]/bonus-delivery/bonus-delivery.md`; `dados.json` como array de snapshots em append. Manifest pelo script: `python3 tools/manifest.py <slug> complete bonus-delivery` e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/salvar-e-mensagem-final.md`, como draft: os bônus da oferta com tipo, condição e canal, o GWP configurado conforme a condição, os assets em `bonuses/` com o link na thank-you page, o payload do email pronto pra `retention-engine`, o pedido de teste de compra, e os próximos passos ('retention' Fase A agora; 'bonus delivery' de novo depois de cerca de 30 dias com ads ativos, pra Fase B).
