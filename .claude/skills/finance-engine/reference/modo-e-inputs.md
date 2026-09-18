# Finance Engine · Referência: Detectar o modo e completar só o que falta (ETAPA 1)

> Quais ETAPAs rodam em cada modo, a regra de decisão do modo pelos dados, a pré-população a partir dos artefatos e a mensagem única com os inputs que não vivem em arquivo. Abra na ETAPA 1.

**ETAPAs 1-6 e 12-14 rodam nos dois modos. ETAPAs 7-11 são exclusivas do Modo B** e são puladas silenciosamente quando não há histórico — sem seção vazia no relatório, sem explicar o que não foi feito (rule `report-only-results.md`).

### ETAPA 1 — Detectar o modo e completar só o que falta

O modo é **decidido pelos dados**, não perguntado. Regra:

| Situação dos dados | Modo | Observação |
|---|---|---|
| Nenhum mês fechado com ad spend **e** clientes novos do Shopify | **A — Planejar** | Pré-lançamento ou primeiros dias. O modelo é projetivo. |
| 1 a 2 meses fechados | **B — Medir**, cohort **não calibrado** | Decay assumido; a coluna de cohort roda com aviso de que ainda não estabilizou. |
| 3 ou mais meses fechados | **B — Medir**, cohort **calibrado** | O decay estabiliza; o modelo passa a valer pra decisão de escala. |

Grave em `mode` e `mode_reason`. Se o membro pedir explicitamente o modo que os dados não sustentam, faça o que os dados sustentam e diga por quê em uma linha — nunca rode o Modo B com número inventado.

**Pré-popule TUDO dos artefatos antes de perguntar qualquer coisa.** Do `offer-builder/dados.json` saem AOV, o stack de custos variáveis inteiro e a margem por pedido. Do `manifest` sai `fixed_costs_monthly`, se já existir. Do `ad-analysis/dados.json` saem spend, CPA, ROAS e AOV reais.

Depois, peça **numa única mensagem** só o que não vive em nenhum arquivo:

**Sempre (os dois modos):**
- **Custo fixo mensal** — "tudo que você paga mesmo vendendo zero: time, apps, ferramentas, aluguel, contabilidade, agência de valor fixo." Se o membro não souber separar, peça o total e a lista; a decomposição é secundária, o total não é. Se `manifest.fixed_costs_monthly` já existir, só confirme: "seus custos fixos ainda são US$ X/mês?"
- **Caixa disponível hoje** — o número que responde "quanto tempo eu aguento".

**Só no Modo B:**
- **Clientes novos do Shopify no período** (Analytics → Reports → *New vs Returning customers*, com a dimensão de mês). É o denominador do CAC — sem ele não há Modo B.
- **Ad spend total do mesmo período** (todas as plataformas, não só Meta).
- **Curva de LTV por cohort**, se o membro tiver (Lifetimely é a fonte mais precisa; Triple Whale manual serve; Shopify puro dá pra reconstruir). Sem ela, a ETAPA 8 roda com decay assumido e o aviso correspondente.
- **Prazo real de repasse do processador** (`payout_lag_days`) e, se usar faturamento da Meta, o prazo da fatura.

Formato da pergunta, uma vez só: *"Já tenho [lista do que foi lido]. Me falta só: [campos ausentes]."* Não re-explique campo já preenchido.
