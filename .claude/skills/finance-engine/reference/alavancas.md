# Finance Engine · Referência: As 4 alavancas, só no Modo B (ETAPA 7)

> A nota de que as ETAPAs 7 a 11 são do Modo B, a simulação de uma alavanca por vez, a tabela do que move cada alavanca na prática e o diagnóstico por eliminação. Abra na ETAPA 7.

**As ETAPAs 7 a 11 rodam somente no Modo B.**

### ETAPA 7 — [Modo B] As 4 alavancas

Qualquer negócio de ecommerce é controlado por **4 alavancas: AOV, CAC (por cliente novo pago), Ad Spend e % de clientes recorrentes.** O valor do modelo não é prever o futuro — é responder "o que acontece se eu mexer nisto?" antes de mexer.

Monte a baseline com os números reais do mês fechado e simule **uma alavanca por vez**, mantendo as outras três congeladas. Para cada simulação, reporte o delta de **margem de contribuição** e de **resultado operacional** (o segundo só existe com os fixos informados).

| Alavanca | O que costuma mover na prática |
|---|---|
| **AOV** | Subir preço; bundle por volume; faixa de frete grátis; upsell pós-compra de um clique; anunciar a versão premium. Costuma ser a alavanca de maior impacto: no material de referência, AOV de US$ 35 → US$ 48 levou o mês de −US$ 53k pra +US$ 58k. |
| **CAC** | Criativo mais interessante (CTR sobe, CAC cai); landing page melhor; **oferta melhor** — mexe em CVR, CTR e AOV ao mesmo tempo. Cuidado com o piso da ETAPA 4: reduzir CAC costuma ser a meta menos realista das quatro. |
| **Ad Spend** | Com margem de contribuição positiva, **volume dilui o fixo**. Expandir países, plataformas novas. É a alavanca que a espiral do ROAS (ETAPA 5) governa. |
| **% recorrentes** | Email/SMS, programa de fidelidade, assinatura, unboxing melhor, indicação. Alimenta os cohorts da ETAPA 8. |

**Diagnóstico por eliminação quando o resultado está no vermelho:** (a) cortar custo fixo, (b) reduzir CAC — frequentemente irrealista, (c) escalar spend, (d) subir AOV. Ranqueie as quatro pelo delta calculado e nomeie **`highest_impact_lever`**. Não recomende as quatro ao mesmo tempo: mexer em tudo junto impede saber o que funcionou.
