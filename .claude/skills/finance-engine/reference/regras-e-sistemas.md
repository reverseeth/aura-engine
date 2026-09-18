# Finance Engine · Referência: As quatro regras que não se negociam e os sistemas nomeados a puxar

> As quatro regras do cânone (margem de contribuição versus lucro, CAC versus CPA, a espiral do ROAS como conta desta skill, os três campos que nunca se estimam) e a lista dos sistemas nomeados com a query exata de cada um, o mínimo dos dois modos e o adicional do Modo B. Abra antes de qualquer cálculo.

### As quatro regras que não se negociam

Vêm do cânone. Valem em todo output desta skill, nos dois modos.

1. **Nunca chame de "lucro" um número que não subtraiu custo fixo** (cânone §1). O rótulo correto é **margem de contribuição**. Quando o custo fixo for desconhecido, **diga isso explicitamente** em vez de omitir: "margem de contribuição de US$ X; sem os custos fixos informados não dá pra dizer se há lucro". Nenhum campo do `dados.json` desta skill chama-se "profit"; o único número que merece o nome é `monthly_model.operating_income`, e ele é `null` enquanto os fixos forem `null`.

2. **CAC ≠ CPA** (cânone §3). CAC = ad spend do período ÷ **clientes novos do Shopify** (`new customer = TRUE`) no mesmo período. CPA de plataforma conta conversão atribuída pelo Meta, cliente recorrente incluído. Onde a decisão for de aquisição, o modelo usa CAC. Misturar os dois torna o modelo falso — e todo o Modo B é construído em cima dele.

3. **A espiral do ROAS é conta desta skill** (cânone §4). A `finance-engine` é quem calcula e publica o número; a `ad-analysis` e a `scale-engine` leem. Detalhe operacional na ETAPA 5.

4. **Três campos nunca se estima. Faltando, a skill pede:**

   | Campo | Por que nunca se chuta |
   |---|---|
   | **Custo fixo mensal** | É o que separa margem de contribuição de lucro. Chutar inverte a recomendação de spend. |
   | **CAC real** | Só existe com clientes novos do Shopify. Estimar CAC a partir do CPA do Meta é o erro que o cânone §3 nomeia. |
   | **Contagem de clientes novos** | É o denominador do CAC. Sem ela não há CAC, não há cohort e não há LTV. |

   Faltando qualquer um: o campo fica `null` no `dados.json`, entra em `pending_inputs[]`, o bloco que depende dele fica marcado como bloqueado, e o relatório diz **o que falta e o que destrava**. Nunca preencher com plausível.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. O domínio inteiro é `finance-projections` no `.claude/lib/kb-index/`. **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill finance-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão. **Esta skill é a consumidora que faltava** dos quatro sistemas marcados como dormant no índice (`use_in_skill: "—"`) — a partir dela, eles são puxáveis.

**Mínimo a carregar nos DOIS modos:**

- **Contribution Margin + Variable Cost Stack** — `contribution margin stack de custos variáveis COGS fully loaded processing fees`
- **First Order vs Repeat Order Economics ("perder para ganhar")** — `first order vs repeat order economics perder no primeiro pedido janela payback`
- **The ROAS Death Spiral** — `espiral do ROAS cortar spend aumenta prejuízo custos fixos não encolhem`
- **DTC P&L Benchmarks + The Barometers** — `benchmarks financeiros DTC barometers CAC LTV COGS consertáveis AOV baixo mata`
- **Four Quarter Accounting (25/25/25/25)** — `Four Quarter Accounting 25% COGS overhead aquisição EBITDA Taylor Holiday`
- **Meta CAC Floor + regra de forecast 4:1** — `CAC floor Meta $15-25 em escala crescer 5% spend razão 4:1`
- **3-Scenario Pre-Scale Stress Test** — `stress test antes de escalar CAC +20% LTV −20% COGS +5% modelo sobrevive`
- **CAC vs CPA Discipline (Shopify new customer = TRUE)** — `CAC igual spend dividido por clientes novos Shopify não CPA de plataforma`
- **A Função Financeira em 3 Camadas** _(dormant até esta skill)_ — `função financeira em 3 camadas bookkeeping reporting strategy brand DTC`

**Adicionalmente no Modo B:**

- **4-Lever Projection Model** — `projection sheet 12 meses 4 alavancas AOV CAC ad spend returning customers`
- **Cohort LTV Model (12 meses, decay ~0,8)** — `cohort model LTV 12 meses decay 0.8 total margin acumulada Lifetimely`
- **90-Day Payback + First-Order Profitability Check** — `janela de payback 90 dias first-order profitability CAC máximo margem`
- **Scale-Ceiling Detection (plateau no operating income)** — `detecção de teto de escala operating income cai além de X de spend plateau`
- **Great Wall of Death — as 3 perguntas de cash conversion** — `great wall of death cohort fica positivo antes do boleto vencer cash-out date`
- **The Float Stack (Meta net 45 + Melio + Amex Plum ≈ 105 dias)** _(dormant até esta skill)_ — `stack de float Meta invoicing net 45 Melio Amex Plum net 60 105 dias`
- **Float Guardrails (erro de 5% no cohort vira +$157k em −$257k)** — `guardrails do float erro de 5% no cohort calibrar antes de alavancar`
- **Banking Sheet + Founder Burn Rate Rule** _(dormant até esta skill)_ — `banking sheet ritual semanal domingo todas as contas net cash flow`
- **Revenue Slice & Dice / Triple Profit Tracking** _(dormant até esta skill)_ — `triângulo de forecasts sales cash inventory safety stock lead time`
- **Offer-Change Break-Even Reset** — `nova oferta recalcular break-even ROAS e CPA-alvo antes de escalar promo`

Aprofunde. Um erro de 5% num cohort vira centenas de milhares de dólares de diferença de decisão — é o único lugar do framework onde a precisão do número importa mais que a velocidade da entrega.
