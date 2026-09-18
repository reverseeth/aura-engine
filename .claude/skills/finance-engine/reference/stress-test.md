# Finance Engine · Referência: Stress test padrão (ETAPA 12)

> A nota de que os dois modos voltam a rodar juntos, os três cenários fixos com o que cada um testa, os dois cenários de caixa do Modo B e a regra do alerta em destaque. Abra na ETAPA 12.

**A partir daqui, os dois modos voltam a rodar juntos.**

### ETAPA 12 — Stress test padrão

Três cenários, sempre os mesmos, sempre rodados antes de qualquer recomendação de aumentar spend ou alavancar caixa:

| Cenário | Ajuste | O que ele testa |
|---|---|---|
| **CAC +20%** | multiplique o CAC real por 1,2 | leilão piorando, fadiga de criativo, CPM de temporada |
| **LTV −20%** | corte a curva de cohort em 20% | churn pior que o modelado, take rate de assinatura caindo |
| **COGS +5 pontos** | some 5 pontos percentuais ao COGS | tarifa, frete, câmbio, taxa de defeito |

Para cada um, reporte margem de contribuição, resultado operacional (quando os fixos existirem) e um veredito binário **`survives`**. No Modo B, acrescente dois cenários de caixa antes de alavancar float: **reembolso +2 pontos** e **repasse do processador atrasado 7-14 dias** (entram no mesmo `stress_test[]`, como `refund_plus_2pts` e `processor_payout_delay_7_14d`).

Se **qualquer** cenário derrubar o resultado operacional abaixo de zero, a recomendação de escalar sai com esse alerta em destaque — ele não some do relatório.
