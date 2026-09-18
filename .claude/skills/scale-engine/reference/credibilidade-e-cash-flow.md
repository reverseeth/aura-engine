# Scale Engine · Referência: Credibilidade da loja e cash flow (ETAPAs 5 e 6)

> A checagem de credibilidade antes de empurrar volume (ETAPA 5) e o gargalo de caixa da escala: payout hold e rolling reserve de loja nova, os frameworks de teto de risco, o check obrigatório antes de escalar mais de 2× em menos de 7 dias, a fórmula do gap projetado e os campos da `finance-engine` que a substituem (ETAPA 6). Abra nas ETAPAs 5 e 6.

### ETAPA 5 — Credibilidade da Loja (lever de conversão antes de escalar)

Escalar budget joga tráfego mais frio na loja. Se a loja não parece confiável, a conversão cai e a escala morre. Antes de empurrar volume, confirme (nota rápida, não bloqueio):

- Página de Facebook + Instagram com seguidores reais e posts (não vazio).
- Reviews/avaliações reais (~100, em inglês) na PDP — prova social.
- Highlights/destaques de confiança: brand story / About, feedback, selos legítimos.
- **Gestão de comentários é o mais importante.** Comentário negativo num post de ad fica visível pra todo mundo que vê o anúncio e derruba conversão direto. Responder ou deletar comentários ruins é manutenção diária de escala.

> **Honestidade:** foco em prova social **real**. Comprar seguidor/comentário falso em volume pode atrapalhar (parece fake, arrisca a conta) — não recomendado. Se a credibilidade da loja está fraca, isso é gargalo de conversão a resolver na `page-design`/`page-build`/`checkout-aov` antes de gastar mais em ads.

### ETAPA 6 — Cash Flow (o gargalo invisível de escala)

Ads cobram **diário**; o payout do Shopify chega em **3-5 dias** (Stripe ~2 dias). Quando você escala, esse descasamento vira um buraco de caixa que cresce com o budget. Escalar sem cobrir o gap é a forma mais comum de quebrar uma marca que estava lucrando.

**Payout hold / rolling reserve (cenário obrigatório pra loja nova):** os 3-5 dias são o lag NOMINAL — processadores seguram mais quando a conta é nova ou o volume dá spike (exatamente o que a escala provoca). Shopify Payments/Stripe podem aplicar **rolling reserve** (reter uma % de cada payout por semanas) ou **hold temporário** de dias a semanas enquanto revisam o risco da conta. Pra loja com **menos de ~90 dias de processamento** (ou no primeiro spike grande de volume), use `payout_lag_days` conservador de **7-14 dias** no check de float abaixo — não os 3-5 nominais — e confirme no dashboard do processador se há reserve ativa antes de autorizar qualquer escala agressiva. Escalar assumindo payout de 3 dias com uma reserve de 30% ativa é o furo de caixa clássico da loja nova.

**Frameworks de cash flow e teto de risco (rode antes de autorizar escala agressiva):**
- **Total Loss Investment Concept** (rode `total loss investment concept aggression ceiling zero additional revenue acceptable loss`) — define o teto de agressividade: quanto você aceita perder se o gasto extra trouxer zero receita nova. É o limite duro do surf da Escola A e do doubling rápido da Escola C.
- **Fractional Banking** (rode `fractional banking borrow against future revenue rolling repeat purchase cash flow scale negative CPA`) — como financiar escala emprestando contra receita futura/repeat purchase quando o cash gira mais devagar que o spend. Pré-condição: LTV/repeat real provado (não chute).
- **Going Negative on CPA (LTV-Funded Acquisition)** (rode `going negative on CPA LTV rebills Agora upfront capital dominate market acquire more customers`) — só pra `scaling` com LTV/rebill comprovado e capital de giro: aceitar CPA acima do breakeven na primeira compra porque o LTV banca. **Nunca** ofereça isto a starter/validating sem dado de repeat real.
- **Great Wall of Death — as 3 perguntas de cash conversion** (rode `great wall of death cohort fica positivo antes do boleto vencer cash-out date`) — o teste de caixa da escala: a coorte fica positiva **antes** da data em que a conta vence (o cash-out date)? Se a resposta é não, a escala está financiando prejuízo com prazo. Quem fecha essa conta com os números do membro é a **skill `finance-engine`** (`'finanças'`) — o `cash.cash_needed_90d` e o `cash.runway_months` dela já carregam essa leitura; sem a `finance-engine`, use as 3 perguntas como check qualitativo antes de autorizar escala agressiva.

**Check obrigatório antes de qualquer escala > 2× em < 7 dias:**

- [ ] Float de cash disponível ≥ `1.5 × daily_budget_target × payout_lag_days`
- [ ] Fornecedor consegue entregar o volume de unidades projetado em 30/60/90 dias? **Leia primeiro `sourcing/dados.json` → `calendar.volume_confirmation_30_60_90`** (a `sourcing` ETAPA 12 grava a confirmação escrita — existindo, use e não re-pergunte). Sourcing rodou mas o campo está vazio → avisar que escalar sem confirmação de volume é **risco declarado de ruptura de estoque** e pedir a confirmação ao fornecedor (ou rodar a `sourcing` ETAPA 12). Sourcing nunca rodou → pergunta de hoje (confirmação escrita)
- [ ] Estoque longe do ponto de recompra: com `calendar.reorder_point_days` na mão, **perto desse ponto o pedido de reposição é colocado, o rastreio acompanhado e a escala agressiva SEGURA** até o estoque novo chegar — subir budget contra a ruptura só antecipa o dia sem estoque
- [ ] Backup payment method se o Meta bloquear o cartão principal?

**Cálculo de gap projetado:**
```
cash_gap_projected = (daily_budget × 30 × burn_multiplier) − (daily_revenue_projected × 30 × (1 − payout_lag/30))
onde burn_multiplier = 1.3 (margem de segurança)
```

> **Quando `finance-engine/dados.json` existir, o número de caixa vem de lá — esta skill não estima.** A `finance-engine` monta a necessidade de caixa com o custo fixo dentro, o desembolso de estoque e a margem de contribuição acumulada do período (ETAPA 6 dela), coisas que a fórmula acima não enxerga. Leia e use:
> - **`cash.cash_needed_90d`** no lugar do `cash_gap_projected` estimado aqui. É a necessidade de caixa de 90 dias já com o fixo somado.
> - **`cash.float_stack.total_float_days`** no lugar do `payout_lag_days` isolado no check de float acima: com o stack de float ativo, o ad spend só deixa a conta lá na frente, e a diferença entre as duas linhas (`cash_needed_90d` vs `cash_needed_90d_with_float_stack`) costuma ser o que separa "não dá pra escalar" de "dá".
> - **`cash.runway_months`** como a leitura de prazo: quantos meses o caixa aguenta o plano de escala que está sendo montado.
>
> **Sem o arquivo da `finance-engine`, nada muda:** a fórmula local acima continua valendo integralmente, com o `payout_lag_days` conservador de loja nova. Registre em `cash_flow.source` qual das duas fontes produziu o número.

Se `cash_gap_projected` (ou o `cash.cash_needed_90d` da `finance-engine`, quando existir) **> 50% do cash disponível**, **NÃO autorize** escala agressiva (surf 10×, doubling rápido). Volte pra ritmo conservador (Escola C devagar, ou o passo de +20% do protocolo sem surf) até o caixa girar.

**Regra dura:** nunca escala > 2× o budget atual em < 7 dias se o cash não cobre o gap — independente de quão bom o sinal está. O surf da Escola A respeita isso: surfa com o que tem, recua na hora.
