# Finance Engine · Referência: Cohorts com decay factor e LTV medido, só no Modo B (ETAPA 8)

> A estrutura da tabela de cohort, o decay factor calculado ou assumido, a calibragem, o aviso de sensibilidade obrigatório, a marca sem cohort, LTV versus retenção e o pico de churn. Abra na ETAPA 8.

### ETAPA 8 — [Modo B] Cohorts com decay factor e LTV medido

Cohort = clientes adquiridos no mesmo mês, seguidos ao longo de 12 meses. É o que legitima gastar mais que o concorrente.

**Estrutura da tabela** (por cohort, mês a mês):

| Coluna | Definição |
|---|---|
| `ltv_pct` | Multiplicador sobre o mês 0. **Mês 0 = 100% por definição** (na prática 101-102%, porque uma fração recompra dentro dos 28 dias). Mês 1 = 60% significa que, pra cada US$ 100 do mês 0, o mês 1 acrescenta US$ 60. |
| `revenue` | `ltv_pct` × AOV × nº de clientes do cohort |
| `margin` | receita × margem de contribuição % − (CAC × clientes) — **o CAC entra só no mês 0** |
| `total_revenue` | acumulado |
| **`total_margin`** | acumulado. **É a coluna de decisão de escala** — mostra o mês em que o cohort cruza pra positivo. |

**Decay factor.** Com a série real em mãos (Lifetimely é a fonte mais precisa; Triple Whale manual serve), calcule o decaimento médio entre meses consecutivos e use-o pra estender a curva nos meses sem dado. A referência de mercado é **~0,8**: de 100 clientes adquiridos, ~15 voltam no mês 1, ~12 no mês 2, ~11 no mês 3. Grave `decay_source` como `calculated` (série real) ou `assumed` (referência) — nunca deixe ambíguo qual dos dois foi usado.

**Calibragem.** Ajuste a linha de retorno basal até o número de recorrentes do modelo bater com o real de cada mês fechado. Repita a cada mês fechado até ter **3 a 5 meses de dados reais**; depois o decay estabiliza. Uma vez calibrada, **não mexa** na curva de LTV — revise a cada ~6 meses com dados novos. Quanto mais tempo o modelo roda, mais preciso fica.

**Aviso de sensibilidade — obrigatório no relatório:** um erro de 5% no cohort inverte o resultado. No exemplo de referência, a diferença entre acertar e errar 5% é sair de +US$ 157k pra −US$ 257k. Enquanto o cohort não estiver calibrado com 3+ meses reais, **modele o payback no mês 2 em vez do 3** — 30 dias de folga tornam a conta quase impossível de perder.

**Marca nova, sem cohort nenhum:** não invente curva. Rode o Modo B só nos blocos que os dados sustentam, marque `cohorts.calibrated: false`, e diga no relatório que a decisão de escala baseada em LTV fica travada até 3 meses fechados.

**LTV ≠ retenção.** Retenção é gente ficando; LTV é dólares gerados. Modele dólares: retenção boa com ticket baixo perde de retenção mediana com AOV alto.

**Pico de churn no dia ~45** — a maior parte do cancelamento acontece num único momento, tipicamente quando o produto chegou, foi testado e a decisão foi tomada. É o ponto que a skill `retention-engine` ataca primeiro; esta skill entrega o número que prova onde ele está.
