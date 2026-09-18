# Finance Engine · Referência: Payback, first-order profitability e teto de escala, só no Modo B (ETAPA 9)

> A checagem de first-order profitability com o exemplo, a janela de payback, a regra de perder no primeiro pedido como decisão, a taxa de aumento do CAC e a detecção do teto de escala. Abra na ETAPA 9.

### ETAPA 9 — [Modo B] Payback, first-order profitability e teto de escala

**Checagem de first-order profitability:**

```
cac_max_first_order = margem de contribuição do 1º pedido (antes do CAC)
first_order_profitable = (cac_real < cac_max_first_order)
```

Exemplo de leitura: AOV US$ 74 com COGS 20% (US$ 14) → margem US$ 58 → CAC máximo US$ 58. CAC real de US$ 48-49 ⇒ **lucrativo no primeiro pedido** ⇒ a estratégia correta é **escalar spend até chegar perto do zero a zero no primeiro pedido**, porque o LTV paga o resto. Marca lucrativa no primeiro pedido que não escala está deixando dinheiro na mesa.

**Janela de payback.** A referência é **90 dias** (LTV de 3 meses). Quem tem capital e paciência otimiza pra 12 meses; quem está calibrando o cohort usa 60 dias por segurança. Publique `payback_window_days_measured` a partir da coluna `total_margin` da ETAPA 8: é o mês em que o acumulado cruza zero.

> **Perder no primeiro pedido é decisão, não acidente.** É racional perder ~US$ 20 de margem de contribuição no 1º pedido se em ~3 meses o cohort devolve US$ 30+. As duas condições: LTV **medido** (não estimado) e caixa que aguenta a janela. Sem as duas, o gate da `offer-builder` (margem por pedido) continua valendo integralmente — e para membro em `starter` ou `validating` ele continua valendo de qualquer forma.

**Taxa de aumento do CAC e teto de escala.** O CAC não sobe proporcionalmente ao spend, mas sobe. A referência de forecast é **4:1 — a cada 5% de aumento de spend, ~1% de aumento de CAC**. Com histórico suficiente, calcule a taxa real por US$ 1.000 de spend adicional a partir dos meses fechados e use-a no lugar da referência.

**Detecção do teto:** projete o resultado operacional em faixas crescentes de spend. O ponto em que ele **para de subir e começa a cair** é o `scale_ceiling_monthly_spend` — o plateau. Escrito de forma acionável: *"não passar de US$ X/mês de spend até o CAC melhorar"*. É o número que a skill `scale-engine` precisa antes de autorizar escala agressiva.
