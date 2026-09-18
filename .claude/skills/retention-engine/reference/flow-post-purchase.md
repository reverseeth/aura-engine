# Retention Engine · Referência: Flow 3, Post-Purchase Welcome (Fase A)

> Os quatro sistemas a puxar, os 4 emails com o timing e o beat do pico de churn com a leitura da curva medida da finance-engine ou o fallback de mercado. Abra ao escrever o post-purchase.

### 3. Post-Purchase Welcome (comprou pela primeira vez) — FASE A (pré-launch)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Kennedy's Post-Purchase Reassurance Letter** — pós-compra como profit center: matar buyer's remorse no Email 1 (rode `Kennedy post-purchase reassurance letter buyer remorse profit center order confirmation`)
- **Collier's Re-Sell After Shipment (Acknowledgment Letter)** — revender o que já foi comprado, reduzir returns, construir antecipação até a entrega (rode `Collier re-sell after shipment acknowledgment letter reduce returns build anticipation testimonial`)
- **Zero-Party Data Moat** — usar o Email 2/3 pra coletar dado de preferência (post-purchase survey/quiz) que alimenta personalização futura (rode `zero-party data moat post-purchase survey onboarding quiz preference center unreplicable personalization`)
- **30-60-90 Day LTV Email+SMS Flow Hacks** — janela da segunda compra; estruturar os emails 3-4 pra cair dentro dela (rode `30-60-90 day LTV email SMS flow hacks second purchase window zero-party data force multiplier`)

- Email 1 (30min pós-purchase): obrigado + unboxing tips + delivery ETA
- Email 2 (dia da entrega estimada): "chegou?" + how-to-use tutorial
- Email 3 (dia 7-10): request review (com incentivo)
- Email 4 (dia 21-30): cross-sell ou replenishment trigger (se consumível)

**O beat do pico de churn (a batida que decide a segunda compra).** A maior parte do abandono acontece num único momento, tipicamente quando o produto chegou, foi testado e a decisão foi tomada — a referência de mercado é **por volta do dia 45**, e é justamente onde o post-purchase acima acaba (dia 21-30) e o win-back ainda não começou (60+ dias). O Email 4 é o que cobre essa lacuna, e o timing dele não é palpite quando existe número:

- **Com `finance-engine/dados.json` (cohorts medidos):** posicione o Email 4 alguns dias **antes** de `cohorts.churn_spike_day` — chegar depois do pico é falar com quem já decidiu sair. O conteúdo do email é ditado pela leitura da curva: se `cohorts.ltv_pct_by_month` mostra queda forte já no mês 1, o email ataca uso e resultado (o cliente não chegou a experimentar o benefício); se a queda vem depois, ataca reposição e continuidade. Use `cohorts.crossover_month` como a régua de quanto vale investir aqui: é o mês em que o cohort cruza pra positivo, ou seja, até lá o cliente ainda não pagou o próprio CAC.
- **Sem o arquivo da `finance-engine` (ou com `cohorts.calibrated: false`):** mantenha o dia 21-30 do Email 4 e trate o dia ~45 como referência de mercado, não como medida do negócio — dizendo isso ao membro em uma frase, e não escrevendo o benchmark no doc como se fosse número dele.
