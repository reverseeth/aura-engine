# Offer Builder · Referência: AOV projetado e PSM projetado (ETAPAs 6 e 7)

> Os sistemas de AOV e upsell, as taxas de aceitação realistas, a fórmula do AOV projetado com o mix baseline, os benchmarks de categoria, o guardrail de canibalização de bundle (ETAPA 6) e o PSM projetado com a explicação de LTV vs PSM e as saídas quando o PSM fica abaixo de 1,1 (ETAPA 7). Abra nas ETAPAs 6 e 7.

### ETAPA 6 — AOV Projetado (com Bump e Upsell Acceptance)

**Puxe estes SISTEMAS NOMEADOS de AOV/upsell antes de projetar (rode a `best_query` de cada):**
- **Profit Optimization 4 Categories + AOV Builders** (rode `profit optimization four categories AOV builders bundles free shipping threshold volume discount GWP profit per visitor`) — o menu de alavancas de AOV (bundle, threshold de frete grátis, volume discount, GWP).
- **Free-Plus-Shipping & Order Form Bump** (rode `Brunson free plus shipping buyer 10x order form bump 20 to 50 percent`) — taxas de aceitação realistas do bump (20-50%) que calibram a estimativa abaixo.
- **Three OTO Structures** (rode `Brunson three OTO structures next thing do it faster need help upsell`) — estrutura o upsell pós-compra (próxima coisa / fazer mais rápido / preciso de ajuda).
- **AOV Money Close + Offer Bump + Add-More-Packages** (rode `AOV money close offer bump add more packages biggest package most popular checkout`) — qual pacote destacar e como apresentar o "add more" no checkout.

Estime taxas de aceitação realistas (ajustar depois com dados reais):
- **Bump acceptance**: 20-35% (conservador: 20%) — o teto de 20-50% é de order-form bump de funil dedicado; checkout Shopify real fica mais perto do piso
- **Upsell acceptance (post-purchase)**: média da plataforma 3-8%; oferta bem casada (Gate de Complementaridade + more-of-same) 8-14% (conservador: 8%)
- Referência de lift 2026: página post-purchase bem construída adiciona 12-22% no valor do pedido; as 3 superfícies juntas (cart + checkout + post-purchase) ≈ +22% de AOV

Calcule AOV projetado:

AOV = (% compra solo × preço solo)
    + (% compra 3-pack × preço 3-pack)
    + (% compra 6-pack × preço 6-pack)
    + (bump acceptance × preço bump)
    + (upsell acceptance × preço upsell)

Baseline mix (ajustar com data depois):
- 50% solo, 35% 3-pack, 15% 6-pack (mix típico com Popular destacado no 3-pack)

**Sanity de categoria (benchmarks 2026 — o AOV projetado deve cair numa faixa crível):**
- Beauty/personal care: AOV $55-137 (média global $74; impulso single-SKU $30-55, bundle de rotina $75-95, skincare premium com assinatura $100-137)
- Supplements: $45-65 transacional; bundle 90 dias $90-120 (billing trimestral triplica o AOV efetivo e derruba o payback do CAC de ~3 pedidos pra 1)
- Shopify DTC geral: $85-95 (top 20% acima de $120); CAC de referência nas duas categorias ≈ $61; margem bruta 60-70%; recompra 37.7% em supplements vs 25-30% em beauty

Se o AOV projetado ficar muito fora da faixa da categoria sem justificativa clara (posicionamento premium, bundle robusto), reveja o mix antes de prosseguir.

**Guardrail de canibalização de bundle (net AOV, não AOV bruto):**
- Desconto de 15% num bundle que sobe o AOV em 30% derruba a margem de contribuição em **6-7 pontos percentuais**, A MENOS que **mais de 20% dos pedidos do bundle sejam incrementais** (gente que não teria comprado o solo full-price). Sem histórico, assuma o cenário conservador (incrementalidade baixa) e avalie o bundle pela **margem de contribuição líquida**, nunca pelo AOV do painel.
- Net AOV: desconte devoluções — com 15% de returns, AOV $120 no painel é ~$102 real. Use o net nas projeções de PSM da ETAPA 7. Se a provisão de reembolso/chargeback já entrou como linha de custo no `cogs_breakdown` (item 8 da ETAPA 1), **não desconte de novo aqui** — a provisão conta uma vez só.

### ETAPA 7 — PSM Projetado (Profitable Scaling Margin)

Reavalie o PSM com o **AOV projetado da ETAPA 6** (pós bump/upsell) como LTV-proxy, pela MESMA fórmula da ETAPA 5 (a mesma que a skill `ad-analysis` usa pro `psm_real`):

**Fórmula:** PSM = LTV / (CAC + COGS) — agora LTV = AOV projetado do primeiro pedido (ETAPA 6, ajustado pra net AOV se houver estimativa de devoluções), **CAC = teto de CAC 2× da ETAPA 5** (ou um CAC esperado de benchmark, se o membro tiver — custo por cliente NOVO, medido no Shopify com `new customer = TRUE`, nunca o CPA que o gerenciador de ads reporta; cânone §3), COGS = somatório de todos os itens do `cogs_breakdown` (igual à ETAPA 5 e à Skill `ad-analysis`). Se houver dado de recompra medido, use LTV com reorder ao longo de 30-60-90 dias — aí o LTV deixa de ser proxy do primeiro pedido, o PSM sobe e justifica um teto de CAC mais alto. Sem dado medido, o LTV permanece o do primeiro pedido: **recompra estimada não entra no PSM** (cânone §2 — a economia da recompra é outra tabela, não um multiplicador otimista nesta).

- **PSM < 1.0**: cada cliente perde dinheiro em escala — oferta NÃO viável
- **PSM 1.0–1.1**: breakeven, cresce devagar com risco
- **PSM 1.1–1.3**: escala estável, +5% por ciclo
- **PSM > 1.3**: escala agressiva viável

**No relatório (.md/.html), explique LTV e PSM como conceitos separados, em linguagem simples** — o membro confunde os dois. LTV é um valor em dinheiro (quanto um cliente rende ao longo do tempo; sem histórico, o proxy é o AOV projetado do primeiro pedido). PSM é uma razão: LTV dividido pelo custo de trazer e entregar o cliente (CAC + COGS) — acima de 1,0 o cliente rende mais do que custa; acima de 1,3 dá pra escalar forte. Mostre os dois números lado a lado (o LTV que alimenta o cálculo e o PSM resultante), nos cenários sem recompra e com recompra.

**No mesmo trecho do relatório, diga em uma frase por que o custo de aquisição usado aqui é o CAC e não o CPA do gerenciador**: o gerenciador conta como conversão a compra de quem já era cliente, então o custo por cliente NOVO (Shopify, `new customer = TRUE`) é sempre maior que o CPA reportado. É esse número maior que a oferta precisa aguentar.

Se PSM projetado < 1.1 — oferta **não sustenta escala lucrativa** com economics atuais. Sugira em ordem:
1. **Aumentar AOV** (primeira opção, sem arriscar volume):
   - Bundle (ex: 3-pack desconto 15%)
   - Upsell no checkout (complemento de $20-40 com margem alta)
   - Assinatura **sem desconto**: o preço de assinatura fica no preço-base e o one-time sobe ~15% (regra da ETAPA 3). Aumenta o LTV sem entregar margem em cada recompra
2. **Reduzir COGS** (fornecedor alternativo, negociar volume, frete agregado)
3. **Aumentar preço** (só se posicionamento competitivo permitir; re-validar pricing anchors)
4. **Pivotar oferta** — mudar mecanismo ou público-alvo
NUNCA "reduzir o teto de CAC magicamente"; o custo de aquisição é output de eficácia no leilão, não input — e abaixo de US$ 15–25 ele não existe (piso de CAC, ETAPA 5).
