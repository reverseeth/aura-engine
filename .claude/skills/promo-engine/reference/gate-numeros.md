# Promo Engine · Referência: O gate do recálculo do breakeven com a margem promocional (ETAPA 4)

> O exemplo canônico da receita que sobe e do lucro que cai, o bloco de fórmulas com os números do membro, as réguas de piso de margem, a métrica da janela e a saída binária do gate. Abra na ETAPA 4.

### ETAPA 4 — GATE: recálculo do breakeven com a margem promocional

**Esta ETAPA é a razão de a skill existir como dona da janela.** Rode **Offer-Change Break-Even Reset** (`nova oferta recalcular break-even ROAS e CPA-alvo antes de escalar promo`) e, se a `finance-engine` existir, releia `roas_spiral` e `handoff.for_skill_12`.

O exemplo canônico da fonte, pra calibrar a leitura antes da conta: base com ROAS-alvo 2,0×, breakeven 1,43×, 70% de margem bruta — US$ 100k de spend → US$ 200k de receita → ~US$ 40k de lucro. Entra 30% off → a margem cai pra ~55% e o breakeven vira ~1,82×. Quem mantém o alvo de 2,0× e sobe o spend pra US$ 150k termina com US$ 15k. **"Você fez US$ 100k a mais de receita e US$ 25k a menos de lucro."**

**A conta, com os números do membro (mesma família de fórmulas da `offer-builder`/`finance-engine` — nada novo):**

```
desconto_efetivo         = desconto total por pedido, em dinheiro, com o stack inteiro dentro
                           (recalculado a partir do compare-at; store credit entra pelo CUSTO REAL:
                            a margem do valor de face, ajustada pela quebra esperada — não o valor de face)

aov_promo                = aov_esperado − desconto_efetivo

margem_promo_por_pedido  = recomputar o stack da `offer-builder` sobre o preço promocional:
                           custos em % do preço (processamento, provisão de reembolso, fee variável)
                           encolhem junto; custos em dinheiro (produto entregue, frete, pick/pack) NÃO —
                           é por isso que a margem % cai mais do que o desconto sugere

margin_rate_promo        = margem_promo_por_pedido ÷ aov_promo
breakeven_roas_promo     = 1 ÷ margin_rate_promo          (= aov_promo ÷ margem_promo_por_pedido)
breakeven_cpa_promo      = margem_promo_por_pedido
target_cpa_promo         = breakeven_cpa_promo − lucro desejado por pedido na janela
```

Com `finance-engine/dados.json` na mão, reaplique a fórmula da ETAPA 5 da `finance-engine` com o `margin_rate_promo` pra publicar `breakeven_roas_with_fixed_promo` — mesma fórmula, margem nova; esta skill não a redefine. Sem a `finance-engine`, os números da janela são **margem de contribuição**, e o relatório diz isso com todas as letras (unit-economics §1) — nunca "lucro".

**Réguas de margem da fonte:** piso absoluto ~**55%** de margem bruta na oferta promocional; tente ficar **acima de 60%**. AOV baixo (< US$ 60) exige margem % mais alta; AOV alto tolera % menor. Furou o piso → volte pra ETAPA 3 e redesenhe a oferta (store credit e Buy X Gift X existem exatamente pra dar generosidade percebida sem furar margem).

**Métrica da janela:** o que manda é o **blended ROAS** — receita do Shopify ÷ spend total (rode `blended ROAS Shopify dividido por spend total atribuição first click mente` e `blended decide o negócio plataforma decide a otimização third-party red flag incrementalidade`). Marca com orgânico forte (ex.: metade da receita) **não escala por blended** — olha dado click-based/incremental; no surf, olhe também 1-day click (compradores de agora). *"Screenshot de US$ 500k/mês não paga boleto: olhe o P&L, não o dashboard."* Melhor um dia menor com margem do que um dia recorde sem lucro.

**Saída do gate (binária):**
- **Números completos** → grave `promo_economics` com `status: "computed"` e siga pra ETAPA 5.
- **Falta qualquer número** (margem, AOV, desconto definido) → `status: "blocked_pending_inputs"`, `pending_inputs[]` preenchido, **as ETAPAs 5-8 não rodam** — nenhuma campanha criada, nenhum brief pra `creative-engine`, nenhum calendário pra `retention-engine`. A skill para e pede o que falta, em uma mensagem. Nunca preencher com plausível.
