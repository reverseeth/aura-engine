# Offer Builder · Referência: Produto principal, pricing, bundles e arquitetura de assinatura (ETAPA 3, primeira parte)

> Os sistemas nomeados de pricing e value, o framework de triangulação de 3 âncoras com a régua objetiva de divergência, a estrutura clássica de bundles, os sistemas de assinatura, a tabela das três arquiteturas de assinatura e a regra do desconto invertido (prêmio no one-time). Abra ao começar a ETAPA 3.

### ETAPA 3 — Estrutura de Oferta

Monte a arquitetura econômica completa:

**Produto Principal:**
- **Nome do produto** (se ainda não tem, sugira — pode incluir mecanismo no nome: ex: "[Brand] — [Mechanism Name] [Category]", adaptar ao vertical)
- **Preço base**: ver framework de pricing abaixo (triangulação de 3 ancoras)
- **Core deliverable**: o produto em si (1 unidade / X ml / Y cápsulas)

**Puxe estes SISTEMAS NOMEADOS de pricing/value antes de ancorar (rode a `best_query` de cada):**
- **Offer Rebuild (0.47x → 3.6x ROAS só mudando a oferta)** (rode `mesmos ads mesma conta só mudou a oferta, subscription destrói CPA 100x`) — o caso que prova que a oferta é a alavanca desta etapa inteira: mesmos ads, mesma conta, e o ROAS saiu de 0,47x pra 3,6x só com a troca da oferta. A mesma puxada traz o efeito da palavra "subscription" usado no bloco de assinatura abaixo.
- **Hormozi Value Equation** (rode `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice`) — sustenta a ancora value-anchored abaixo.
- **Anchoring & Adjustment** (rode `pricing anchoring adjustment set high anchor was price SSN auction Ariely`) — como ancorar o preço alto antes do real.
- **Decoy Effect (Asymmetric Dominance)** (rode `decoy effect asymmetric dominance Economist subscription Williams-Sonoma bread machine`) — desenha o bundle de 3 tiers.
- **Extremeness Aversion** (rode `extremeness aversion three tiers middle option beer experiment`) — por que o 3-pack "Popular" no meio vende mais.
- **Charm Pricing (Endings in 9)** (rode `charm pricing nine ending left-digit effect 24 percent catalog`) — terminação de preço.
- **3x+ Markup Rule + $60 AOV Floor** (rode `3x markup rule 60 dollar AOV floor COGS shipping margin paid traffic CPM fixed`) — piso de margem pra tráfego pago (cruza com o sanity de margem da ETAPA 1).
- **Hormozi Virtuous Cycle of Price** (rode `Hormozi virtuous cycle of price premium pricing better clients`) — quando subir o preço melhora o negócio.

Pricing psychology adjacente (Coherent Arbitrariness, Zero Price Effect, Mental Accounting, Endowment, Transaction Utility, Kennedy Five Price Minimizers) está no índice — puxe se o framing do preço exigir.

**Framework de pricing (escolher UMA ancora, validar com as outras 2):**
- **Value-anchored**: Preço = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)  [Hormozi Value Equation]
- **Competitor-anchored**: Mediana dos top 3 concorrentes × modificador (1.1-1.3 se diferenciação alta; 0.8-0.95 se entrada competitiva)
- **Economics-anchored**: COGS × 4 a 6 (ecommerce direct-response padrão para viabilizar paid acquisition; régua única no cânone `.claude/lib/unit-economics/README.md` §6, junto do teto de 30% de custo desembarcado que a `sourcing` checa ao cotar)

**Régua objetiva de divergência das âncoras:** `divergência = (âncora_máx − âncora_mín) / âncora_mediana`. Se **> 0.40**, revisitar a oferta antes de prosseguir. Exemplo: âncoras $49 / $62 / $97 → (97 − 49) / 62 = **0.77** → divergem demais, revisar (provavelmente o value-anchored está inflado ou o economics-anchored expõe COGS alto). Divergência ≤ 0.40 = as três contam a mesma história; escolha a âncora primária e siga.

**Bundles (estrutura clássica):**

| Bundle | Quantidade | Preço | Preço por unidade | Savings vs solo |
|---|---|---|---|---|
| Solo | 1x | $X | $X | — |
| Popular | 3x | $Y | $Y/3 | ~$Z ou ~Z% |
| Best Value | 6x | $W | $W/6 | ~$A ou ~A% |

Regra prática (pode ajustar):
- 3-pack: ~25-35% savings vs 3× solo
- 6-pack: ~40-50% savings vs 6× solo

Marcar **Popular** no 3-pack (visualmente destacado — driver de AOV). Best Value no 6-pack (pra clientes que compram em volume alto (whales)).

**Arquitetura de assinatura (decisão OBRIGATÓRIA pra produto consumível):**

**Puxe estes SISTEMAS NOMEADOS de assinatura antes de decidir (rode a `best_query` de cada):**
- **Estrutura da Oferta de Assinatura (não dê desconto — suba o preço do one-time)** (rode `você paga mais por NÃO assinar, one-click upsell na thank you page, produto grátis melhor que desconto`) — o sistema completo por trás da regra do desconto invertido abaixo: prêmio no one-time, produto grátis no lugar de desconto, one-click upsell na thank-you page.
- **Arquitetura Hume: soft offer envolvendo continuidade dura** (rode `entrada grátis envolvendo assinatura recorrente, micro-compromisso de $5, cancel anytime como feature`) — a intro offer: entrada grátis ou micro-compromisso de $5 embrulhando a assinatura recorrente, com o cancel anytime vendido como feature. Candidata quando o avatar é cético de assinatura mas a janela de consumo pede recorrência.
- **Try Before You Buy (o efeito da palavra "subscription")** — o efeito em si já veio na puxada do Offer Rebuild acima (a palavra "subscription" na página destrói o CPA — não repita a busca). Pro enquadramento substituto, rode `try before you buy enquadramento de assinatura sem a palavra subscription` — a assinatura é apresentada como "experimente antes de comprar", nunca pela palavra "subscription"; isso vale pro nome do selling plan que a `page-build` implementa e pra copy que a `copy-engine` escreve.

Se o produto é consumível (acaba e precisa recomprar: supplement, skincare, café, etc), decida AQUI a arquitetura de assinatura — ela muda o LTV, o PSM e o que a `page-build` (selling plan na PDP), a `checkout-aov` (superfícies de checkout) e a `retention-engine` (flow de replenishment) implementam. Três arquiteturas possíveis:

| Arquitetura | O que é | Quando escolher | Impacto no LTV/PSM |
|---|---|---|---|
| `subscription_first` | Subscribe & Save como opção destacada na PDP, com o preço de assinatura no preço-base e o **one-time ~15% mais caro**; one-time como alternativa | Janela de consumo curta (≤ 45 dias), categoria acostumada com assinatura (supplements, café), preço one-time majorado que ainda cabe na âncora de concorrente | LTV 2-4× o do one-time; PSM sobe porque o LTV real substitui o proxy de AOV nas ETAPAs 5/7; churn de assinatura vira a métrica a vigiar |
| `onetime_plus_sub_no_reorder` | PDP vende one-time; a assinatura é oferecida no momento do REORDER (flow de replenishment da `retention-engine`) e no pós-compra | Produto novo sem prova de consumo, avatar cético de assinatura, ou preço de entrada alto que a assinatura assustaria | LTV cresce mais devagar, mas sem custo de conversão na 1ª compra; a `retention-engine` carrega a conversão pra assinatura no timing certo |
| `no_subscription` | Sem selling plan; volume via bundle 3/6-pack | Produto não-consumível, consumível com janela > 90 dias, ou operação sem app de subscription | LTV depende de reorder manual; o 6-pack "Best Value" faz o papel do supply longo |

Critérios de decisão: janela de consumo (≤ 45 dias favorece `subscription_first`), familiaridade do avatar com assinatura na categoria (market research), preço (o prêmio de ~15% no one-time precisa caber na âncora de concorrente desta ETAPA), e stage (starter sem app de subscription instalado → começar `onetime_plus_sub_no_reorder` e migrar quando o consumo estiver provado). Produto não-consumível → `no_subscription` sem cerimônia.

**Regra de precificação da assinatura — o desconto é INVERTIDO (obrigatória em qualquer arquitetura com assinatura):**

**Não dê desconto ao assinante. Suba o preço do one-time em ~15%.** O assinante paga o preço-base; quem NÃO assina é que paga mais. O enquadramento na página é esse: você paga mais por não assinar.

Por que a inversão importa em vez de ser detalhe de framing: desconto de assinatura entrega margem em TODA recompra — exatamente onde a economia já é a melhor da operação, porque a recompra não carrega CAC nem fee de agência atrelado a spend (cânone §2). O prêmio no one-time produz o mesmo diferencial percebido sem tirar margem de nenhum pedido, e ainda melhora a margem de contribuição de quem compra avulso. Registrar como `onetime_premium_pct` (o quanto o one-time fica ACIMA do preço de assinatura), nunca como desconto.

O prêmio no one-time é uma mudança de preço real: revalide as 3 âncoras da triangulação desta ETAPA com o preço majorado antes de cravar. Se o one-time majorado estoura a âncora de concorrente, o caminho é reduzir o prêmio, não voltar pro desconto de assinatura.

**Registrar em `offer-builder/dados.json` → `subscription_architecture`** (campo top-level, enum acima) + `onetime_premium_pct` se houver assinatura — a `page-build` lê pra decidir se a PDP tem selling plan (Subscribe & Save) e com qual dos dois preços em cada opção, a `checkout-aov` pra superfícies de checkout, e a `retention-engine` pro flow de replenishment (na arquitetura 2, o Email 2 do replenishment é ONDE a assinatura é oferecida — o framing lá também é prêmio no one-time, não desconto). Se escolheu `subscription_first`, refaça o PSM da ETAPA 7 com o LTV de assinatura (não só o AOV projetado) — é exatamente o cenário em que o LTV real diverge do proxy.
