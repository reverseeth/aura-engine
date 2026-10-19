# Offer Builder · Referência: Modelo de estoque e coleta do produto (ETAPAS 0 e 1)

> A pergunta do modelo de estoque (ETAPA 0, sempre a primeira) e o que ela muda na oferta; as 3 perguntas ao membro (o COGS item a item pelo stack do cânone §1, conforme o modelo de estoque; features; produto complementar), o que o `sourcing` já responde, as decisões automáticas com as flags de estimativa, o sanity check de margem de contribuição abaixo de US$ 20 e a exceção por payback medido. Abra na ETAPA 0.

### ETAPA 0 — Modelo de estoque (primeira pergunta, antes de tudo)

Nem todo membro quer comprar estoque de cara. A resposta muda o custo por unidade, o prazo de entrega, a garantia, os bundles e o caixa necessário, então ela vem antes de qualquer outra pergunta.

**Antes de perguntar, cheque** `sourcing/dados.json` (`logistics_route`, `three_pl`, agente contratado) e `workspace/profile.md`. Se um deles já responde, confirme em 1 linha ("Pelo sourcing, você vai com estoque em 3PL nos EUA. Mantenho?") e siga.

**A pergunta:**

> "Antes de montar a oferta: como você quer operar o estoque?
> **A) Comprar estoque.** Você compra um lote, ele fica num centro de distribuição (3PL) e sai de lá em 2 a 5 dias. Custo por unidade menor, mas exige caixa pro lote.
> **B) Sem estoque.** O fornecedor ou agente na China envia cada pedido direto pro cliente. Nenhum lote parado, custo por unidade maior e entrega em 7 a 15 dias.
> **C) Começar sem estoque e migrar.** Valida o produto no modelo B e compra lote quando as vendas provarem."

**O que cada resposta muda:**

| | A) Com estoque | B) Sem estoque | C) Sem estoque, depois estoque |
|---|---|---|---|
| `fulfillment_model` | `stock` | `no_stock` | `no_stock_then_stock` |
| Custo por unidade | Menor: preço de lote + frete de entrada + 3PL | Maior: o preço do agente já inclui produto, embalagem, separação e frete até o cliente | Oferta calculada no custo do modelo B; o custo do A entra como cenário de margem depois da migração |
| Prazo de entrega (`delivery_days_estimate`) | 2 a 5 dias | 7 a 15 dias | 7 a 15 dias no lançamento |
| Garantia (ETAPA 4) | Conta da compra | Conta da **entrega**, pra o prazo longo não comer a janela | Igual ao B |
| Bundles | Qualquer tamanho | Só os que o agente envia num pacote só (confirme com ele) | Igual ao B |
| Pedido mínimo e caixa | Pedido mínimo da fábrica × custo = caixa travado no lote | Sem lote; o caixa vai todo pra ads | Lote só depois da validação |
| Texto de envio na página | "Ships in 1-2 business days" | O prazo real, dito com confiança ("Arrives in 7-12 days, tracked") | Igual ao B |

Grave em `offer-builder/dados.json`: `fulfillment_model` e `delivery_days_estimate` (`{ "min": 7, "max": 15 }`). No modelo B ou C, se o membro ainda não tem agente, aponte os agentes parceiros da skill `sourcing` (ETAPA 6 dela) e siga com estimativa conservadora marcada `cogs_estimated: true`.

### ETAPA 1 — Coletar informações do produto (3 perguntas)

Antes de perguntar, extraia o máximo automaticamente da página do produto (dado salvo no profile pela Skill `setup` ou puxando via web fetch agora se o link estiver no profile). Features, ingredientes, claims, preço atual de mercado — tudo que conseguir.

**Antes das perguntas, cheque `workspace/[produto]/sourcing/dados.json` (Skill `sourcing`).** Se existir com `status: "closed"`, o COGS real já está lá (`landed_cost_per_unit`, `three_pl.pick_pack_per_order`, `logistics_route`) — use esses números direto, não pergunte custo ao membro e não marque `cogs_estimated`. Se existir com qualquer `status` diferente de `"closed"` (`quoting` ou `samples` — cotação/amostra ainda aberta), rode com estimativa conservadora + `cogs_estimated: true` e avise que os números refrescam quando a cotação fechar.

**Faça APENAS estas 3 perguntas, na ordem (pulando o que o sourcing já respondeu):**

**1. Custos (COGS breakdown — NÃO aceite agregado):**

O stack de custos variáveis é o do cânone §1 (`.claude/lib/unit-economics/README.md`) — **item a item, nunca agregado**. Pergunte separadamente:

1. Custo do produto **entregue** (fully loaded): produto na fábrica + embalagem + frete de entrada (inbound) + tarifa de importação, por unidade. Custo cru de matéria-prima subestima a linha inteira.
2. Frete médio por pedido até o cliente (informe região principal: Brasil interior? EUA West Coast?) — **incluindo a parcela de frete grátis que a loja absorve**
3. Pick & pack (fulfillment center): R$/$ por pedido

   **Sem estoque (`no_stock` ou `no_stock_then_stock`):** os itens 1 a 3 viram uma pergunta só: o preço que o agente cobra por pedido entregue (produto + embalagem + separação + frete até o cliente), mais o preço de cada unidade extra no mesmo pacote (é o que custa um bundle). Grave o produto em `product_delivered`, o frete em `shipping_to_customer` e `pick_pack: 0` quando o agente embute a separação; sem frete de entrada nem 3PL. No modelo C, peça também o preço de lote, se o membro já tiver, pro cenário depois da migração.
4. Processamento de pagamento: ~3% + taxa fixa (Stripe US: 2.9% + $0.30; Stripe BR: 3.99% + R$0.39; Shopify Payments fica na mesma faixa)
5. Taxas e impostos incidentes por pedido
6. **App de assinatura: 0,5–1% por transação** — só quando a oferta tem assinatura (Seal, Skio, Loop e similares). Parece pequeno e não é: 1% de US$ 1 milhão por mês é US$ 10 mil por mês, permanente. No breakdown, grave o valor por pedido (% × AOV).
7. **Fee de agência quando é cobrado como % do ad spend** — é custo variável, não despesa fixa: agência a 5% de um spend de US$ 1 milhão custa US$ 50 mil. No breakdown, grave o valor por pedido (% × custo de aquisição por pedido), usando o CAC de referência da categoria ou o CAC-alvo declarado pelo membro — uma passada só, sem recalcular em loop quando o teto de CAC mudar. Se a agência cobra valor fixo mensal, ela NÃO entra aqui — vai pros custos fixos da ETAPA 8.
8. **Provisão de reembolso e chargeback** — nunca zero. Entra **uma vez só**: ou como linha de custo aqui, ou como desconto no net AOV da ETAPA 6. Contar nos dois lugares subestima a margem duas vezes.

Os itens 6 e 7 são exatamente os que somem das planilhas: num pedido de US$ 100 com margem de contribuição de US$ 18,70, os dois juntos somam US$ 3 — **16% da margem**. Numa oferta com assinatura, onde o app de subscription é obrigatório, o erro é sistemático.

**Ad spend NÃO entra no `cogs_breakdown`.** Ele é o maior custo variável do cânone, mas nesta skill ele aparece como **CAC** no denominador do PSM (ETAPAs 5 e 7). Somar nos dois lugares conta o mesmo dinheiro duas vezes e derruba a margem artificialmente.

Documente cada um em `offer-builder/dados.json` → `cogs_breakdown`.

**2. Features/ingredientes (CONDICIONAL):**
- SE não conseguiu extrair da página automaticamente: "Liste as features ou ingredientes principais do produto."
- SE conseguiu extrair: NÃO pergunte; mostre o que extraiu e peça confirmação rápida ("tá certo? falta alguma coisa?").

**3. Produto complementar:**
"Tem algum produto complementar que poderia vender junto? (se não souber, diz 'não sei')"

Se a resposta for "não sei", NÃO trave: o Gate de Complementaridade da ETAPA 3 deriva candidatos do market research automaticamente.

**Decisões automáticas do sistema (NÃO PERGUNTE):**
- **Preço final**: definido pelo framework de pricing abaixo (Etapa 3), triangulando 3 ancoras (value / competitor / economics)
- **Pick & pack** (só com estoque): se o membro não souber, estime ~$2-3 por unidade E **marcar `"pick_pack_estimated": true` no JSON companion** (membro precisa validar)
- **Gateway fee**: se o membro não souber, estime ~3% do AOV + taxa fixa E **marcar `"gateway_fee_estimated": true`**
- **App de assinatura**: se a oferta tem assinatura e o membro não sabe a taxa do app, use o topo da faixa (1% do valor da transação) E **marcar `"sub_app_fee_estimated": true`**. Oferta sem assinatura = 0, não estimativa.
- **Fee de agência**: pergunte apenas se o membro paga agência **por percentual do ad spend** (se paga valor fixo ou não tem agência, o campo é 0 aqui). Não invente percentual.

**Sanity check obrigatório depois de calcular Unit Economics (Etapa 5):**

Se a **margem de contribuição por pedido** < $20 → PARAR e avisar membro:
> ⚠️  Margem de contribuição por unidade calculada: $X (receita menos custos variáveis — ainda não é lucro; os custos fixos do negócio não estão descontados aqui).
>     Isso é muito baixo pra ecommerce direct-response: o CAC aceitável fica abaixo de $10-15, e o piso físico de CAC em Meta hoje é US$ 15–25 (cânone §3). Ou seja, o número exigido não existe no leilão.
>
>     Causas prováveis:
>     - COGS subestimado (provável se vc não tinha todos os itens do breakdown — veja `pick_pack_estimated`, `gateway_fee_estimated`, `sub_app_fee_estimated`)
>     - Preço de venda abaixo do competitivo (vê o framework de pricing na Etapa 3)
>     - Produto com AOV inerentemente baixo (considera bundle pra aumentar AOV)
>
>     Opções:
>     1. Reveja COGS itemizado real (peça fatura pro fornecedor)
>     2. Aumenta preço via bundle 2-3 unidades ou upsell pós-compra
>     3. Abandona esse produto — margem não sobe via marketing
>
>     Prosseguir mesmo assim? (sim/não)

Se continuar, marca `"margin_warning": true` no manifest pra Skills `ad-strategy`/`scale-engine` alertarem escala agressiva.

> **Exceção única, e ela não é chute:** membro em `scaling` com janela de payback **medida** (`finance-engine/dados.json` → `payback.payback_window_days_measured ≤ 90`, com cohort calibrado) **e caixa medido que aguenta a janela** (`cash.runway_months` do mesmo arquivo) pode operar com margem de primeiro pedido abaixo de $20 de propósito, porque a recompra devolve dentro da janela. As condições completas estão no check 8 da ETAPA 9 — sem elas, o alerta acima vale integralmente.
