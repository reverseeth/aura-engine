# Team Engine · Referência: Sistemas nomeados da Porta 1, decidir

> A regra de consulta à base pelo índice e a lista dos sistemas da porta de decisão, com a query exata de cada um, incluindo as entradas vizinhas de gargalo e de papel do fundador. Abra nas ETAPAs 1 a 4.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. O domínio principal é `team-hiring-ops` no `.claude/lib/kb-index/`. **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill team-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

**PORTA 1 — Decidir (ETAPAs 1-4):**

- **Buyback Rate + 4 zonas de delegação** — `buyback rate taxa horaria delegar 4 zonas de delegacao tarefas de menor valor`
- **Want > Need Hiring Rule (bad hire = 15× o salário anual)** — `contratar por querer nao por precisar bad hire custa 15x o salario anual`
- **4 tipos de role + benchmarks de time-to-hire** — `quatro tipos de role benchmarks de time to hire por tipo de vaga`
- **Potential vs Skill Hiring** — `contratar por potencial versus por skill quando cada um faz sentido`
- **Top-Down vs Bottom-Up Org Building** — `construir organograma top down versus bottom up primeira contratacao`
- **Superhero → Facilitator** — `transicao de superheroi para facilitador founder para de executar`
- **Time Audit** — `time audit auditoria de tempo onde o time gasta as horas`
- **Key Man Risk + Headaches per Dollar** — `key man risk headaches per dollar dependencia de uma pessoa so`
- **As duas rotas para creative strategist** — `duas rotas para contratar creative strategist formar ou importar`
- **Constraint de 12 meses** _(vizinha, ops-scale-risk)_ — `constraint de 12 meses qual o unico gargalo que limita o ano inteiro`
- **O que quebra entre $500k e $3M/mês** _(vizinha, ops-scale-risk)_ — `o que quebra entre 500 mil e 3 milhoes por mes gargalos por faixa`
- **People-Vision-Cash + os 3 buckets do CEO** _(vizinha, ops-scale-risk)_ — `people vision cash tres buckets do CEO onde o founder gasta o tempo`
- **Founder Optimization + Big 5** _(vizinha, ops-scale-risk)_ — `founder optimization big 5 do fundador foco em poucas alavancas`
- **Modelo de escala por faixa de faturamento** _(vizinha, scaling — já lida pela `scale-engine`/`creative-engine`; reuse)_ — `revenue tier volume intent systems $50K $300K $3M foco por faixa de faturamento`
- **Estrutura de time criativo por faturamento** _(vizinha, scaling — já lida pela `creative-engine`; reuse)_ — `estrutura de time criativo por faturamento creative pods Leanne model um creator`
- **Modelo híbrido de time (fractional / freelancer / offshore direto + primeiras 3 contratações)** — `modelo hibrido de time fractional offshore contratacao direta primeiras 3 contratacoes brand DTC`
