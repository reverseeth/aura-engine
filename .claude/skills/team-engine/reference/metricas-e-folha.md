# Team Engine · Referência: Métricas do funil e a pergunta sobre a folha caber no caixa (ETAPA 8)

> As quatro métricas do motor de contratação com as referências de tempo e custo, e o protocolo de quatro passos da pergunta sobre a folha, que aponta pra finance-engine e nunca responde de sensação. Abra na ETAPA 8.

### ETAPA 8 — Métricas do funil e a pergunta "a folha cabe?"

**Métricas do motor de contratação (grave a cada vaga fechada):**

- **Tempo pra contratar** (referências da fonte: acessória ~30d, sênior ~34-35d, liderança ~60d; média real ~38d)
- **Custo de contratar** = (tempo pra contratar ÷ 30) × US$ 5.000 (custo mensal estimado do processo — ex.: 82 dias ≈ US$ 13k; é o número que justifica pagar faixa alta e fechar rápido)
- **Onde o funil perde candidatos** (qualificado/desqualificado/perdido por etapa)
- **Resultado de cada contratação** (ruim / mediana / ótima) + canal de origem — é o feedback loop do processo: a fonte reporta um ano com 54% de contratações ruins ANTES de levar o funil a sério, e 100% de retenção no ano seguinte.

**"A folha cabe no caixa?" — pointer pra `finance-engine`, nunca conta própria:**

1. Some o custo mensal da vaga nova (salário + ferramentas + variável estimada no alvo) = `payroll_delta_monthly`.
2. Leia `finance-engine/dados.json` (ou `manifest.finance`): `monthly_model.operating_income`, `monthly_model.fixed_costs_monthly`, `cash.runway_months`. Folha é **custo fixo** — a leitura honesta é "a vaga sobe seu custo fixo de A pra B; pelo modelo da `finance-engine`, o resultado operacional atual é C e o fôlego de caixa é D meses".
3. **Sem a `finance-engine` rodada (ou sem custo fixo informado):** a resposta vira pergunta, não instrução — "não dá pra dizer se cabe sem o modelo financeiro; roda 'finanças' que a `finance-engine` fecha isso em minutos". Registre em `pending_inputs[]`. Proibido dizer "cabe tranquilo" de sensação.
4. **Depois de contratar:** lembre o membro de atualizar o custo fixo na próxima rodada da `finance-engine` — o campo canônico `manifest.fixed_costs_monthly` é escrito pelo membro através da `offer-builder`/`ad-analysis`/`scale-engine`/`finance-engine`; esta skill não o escreve, aponta.
