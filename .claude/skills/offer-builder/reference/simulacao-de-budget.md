# Offer Builder · Referência: Simulação de budget em 2 níveis (ETAPA 8)

> A pergunta dos custos fixos (e quando não perguntar), a conferência contra a margem medida pela `finance-engine`, a tabela dos dois níveis, a regra de rótulo margem de contribuição vs lucro, as três ressalvas e o bloco `budget_viability`. Abra na ETAPA 8.

### ETAPA 8 — Simulação de Budget (2 níveis)

Simule a operação em DOIS níveis: o budget diário declarado do membro (do profile) E o dobro dele. O membro decide budget olhando cenários lado a lado, não um número isolado. Pra cada nível, com o CAC de referência (mediano da categoria, ou o CAC-alvo se o membro declarou um — custo por cliente NOVO, não CPA de plataforma; ver cânone §3):

**Antes de montar a tabela, pergunte uma coisa ao membro:** *"Quanto você tem de custo fixo por mês no negócio? (aluguel, salários, ferramentas, agência de valor fixo, contabilidade — tudo que você paga mesmo vendendo zero.)"* Se ele não souber ou não quiser informar, siga com a tabela mesmo assim e trate a ausência conforme a regra abaixo. Grave em `budget_viability.fixed_costs_monthly` (`null` quando não informado — nunca zero por omissão; zero só quando o membro declarar zero).

**Não pergunte o que já está gravado.** Se `finance-engine/dados.json.monthly_model.fixed_costs_monthly` existir (ou `manifest.fixed_costs_monthly` — é o mesmo campo canônico, compartilhado entre as skills `offer-builder`, `ad-analysis`, `scale-engine` e `finance-engine`), pré-popule dali e só confirme: *"seus custos fixos ainda são US$ X/mês?"*. Grave a origem em `budget_viability.fixed_costs_source`. Com o número na mesa, **as duas últimas linhas da tabela têm número** e `result_after_fixed_monthly` deixa de ser `null` nos dois cenários.

**Conferência contra o medido (só quando a `finance-engine` rodou):** compare a margem de contribuição % que esta simulação projeta com `monthly_model.contribution_margin_pct` da `finance-engine`, que é a margem **medida** do negócio. Divergência grande é sinal de que uma das duas premissas está errada — quase sempre um custo variável que ficou fora do `cogs_breakdown`, ou um mix de bundle que na prática não aconteceu. Registre o número medido em `budget_viability.contribution_margin_pct_measured` e, se divergir, diga qual das duas o relatório está usando e por quê. **Sem a `finance-engine`, a linha simplesmente não existe** e a projeção segue como hoje.

| Métrica | Budget declarado | 2× o budget |
|---|---|---|
| Clientes novos por dia (budget ÷ CAC) | ... | ... |
| Margem de contribuição por dia (clientes × margem de contribuição por pedido) | ... | ... |
| Investimento no mês (budget × 30) | ... | ... |
| Clientes novos no mês | ... | ... |
| **Margem de contribuição no mês** | ... | ... |
| Custos fixos no mês | ... | ... |
| **Resultado após custos fixos — é este o número que pode ser chamado de lucro** | ... | ... |

Os custos fixos são o MESMO valor nos dois níveis: eles não crescem porque o budget cresceu. É por isso que o nível 2× costuma melhorar o resultado mesmo com eficiência um pouco pior — mais volume dilui a mesma base fixa (cânone §4).

**Regra de rótulo (cânone §1 — inegociável):** margem de contribuição é receita menos custos variáveis. **Lucro é margem de contribuição menos custos fixos.** A palavra "lucro" só pode aparecer na última linha da tabela, e só quando os custos fixos foram informados. Isso vale na tabela, no texto do relatório, no `dados.json` e em qualquer mensagem ao membro.

**Quando os custos fixos NÃO forem conhecidos:** as duas últimas linhas ficam explicitamente sem número (não zere, não omita a linha, não deslize pra chamar a margem de "lucro"). O relatório diz a frase inteira, na cara: *"Margem de contribuição de US$ X por mês; sem os custos fixos informados não dá para dizer se há lucro."* Grave `result_after_fixed_monthly: null` no cenário correspondente.

**Três ressalvas obrigatórias junto da tabela** (senão a simulação engana): (1) o número simulado conta só a primeira compra — recompra soma por cima, com a economia melhor da tabela 5B; (2) **margem de contribuição não é lucro** — quando os fixos não estão na conta, o que a tabela mostra é o dinheiro que sobra ANTES de pagar a estrutura do negócio; (3) o CAC tende a subir conforme o investimento cresce, então o nível 2× é estimativa de mesma eficiência, não promessa.

Registre em `dados.json` → `budget_viability`: `cac_ref`, `fixed_costs_monthly` e `scenarios[]` (um objeto por nível: `daily_budget`, `new_customers_per_day`, `contribution_margin_per_day`, `monthly_spend`, `new_customers_per_month`, `contribution_margin_per_month`, `result_after_fixed_monthly`) + `caveats` + `verdict`. **Não existe campo com a palavra `profit` neste bloco** — o único número que mereceria o nome é `result_after_fixed_monthly`, e ele é `null` sempre que os fixos não foram informados.

Se `scale-engine/dados.json` já existir com projeções 30/60/90 e cash flow, cruze: em qual patamar de receita mensal essa oferta coloca o membro em 30, 60 e 90 dias? Na primeira rodada da oferta esse arquivo ainda não existe; pule a conferência sem registrar pendência.
