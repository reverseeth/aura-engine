# Scale Engine · Referência: Projeção realista 30/60/90 (ETAPA 7)

> As tabelas do cenário base e pessimista, a camada de custo fixo e o teto de escala quando a `finance-engine` rodou, e o template de cash flow com o payout lag real do membro. Abra na ETAPA 7.

### ETAPA 7 — Projeção Realista 30/60/90 (base + pessimista + cash flow)

Construa dois cenários usando breakeven, AOV e PSM reais.

**Base (premissas: escola escolhida rodando, pipeline de criativo ativo, CPA estável):**

| Mês | Spend/dia alvo | Receita/dia (AOV × vendas) | Margem mensal estimada |
|---|---|---|---|
| Mês 1 | $[atual × 1.5-2] | $[calculado] | $[margem × 30] |
| Mês 2 | $[atual × 2-3] | $[calc] | $[margem] |
| Mês 3 | $[atual × 3-4] | $[calc] | $[margem] |

Use o AOV real da ETAPA 1 (do `finance-engine/dados.json` quando existir; senão o que o membro informou — a `ad-analysis` não grava AOV) e o breakeven do `offer-builder/dados.json`. Não infle: na Escola A o crescimento é em saltos (surf), na C é dobra a cada 3 dias até o teto — modele o caminho realista da escola escolhida.

> **Camada de custo fixo na projeção (quando `finance-engine/dados.json` existir).** A tabela acima projeta **margem de contribuição**, não lucro (unit-economics §1). Com `monthly_model.fixed_costs_monthly` na mão, acrescente **uma coluna**: `Resultado operacional mensal = margem de contribuição do mês − custo fixo mensal` — o único número da projeção que pode ser chamado de lucro. Some duas linhas de leitura ao redor da tabela: o **teto de escala** (`payback.scale_ceiling_monthly_spend`) marcando até onde a curva de spend pode ir, e o **runway** (`cash.runway_months`) dizendo quantos meses o caixa banca esse caminho. O custo fixo é o MESMO valor nos três meses — ele não cresce porque o budget cresceu, e é exatamente por isso que mais volume melhora o resultado mesmo com eficiência um pouco pior (cânone §4).
>
> **Sem o arquivo da `finance-engine`, nada muda:** a projeção fica como hoje, com a coluna de margem mensal, e o relatório diz a frase inteira — *"margem de contribuição de US$ X/mês; sem os custos fixos informados não dá pra dizer se há lucro"* — em vez de deslizar pra chamar a margem de "lucro".

**Pessimista (CPA sobe 20%):**

Ação: parar de subir budget, segurar no último nível lucrativo, refresh de criativo (`creative-engine`) + possível ajuste de oferta (`offer-builder`), retomar escala quando o CPA voltar ao alvo (geralmente 7-14 dias).

Impacto: escala atrasa ~1 mês, mas sem queimar cash flow.

**Template de cash flow (incluir sempre):**

| Dia | Daily Budget | Daily Revenue | Payable (ads) | Receivable (payout +3d) | Cash Float Needed |
|-----|--------------|---------------|---------------|-------------------------|-------------------|
| 1   | $200         | $500          | -$200         | $0                      | $200              |
| 4   | $300         | $750          | -$300         | +$500 (payout do Dia 1) | $300-500          |
| ...  | ...          | ...           | ...           | ...                     | ...               |

(Com payout +3d, a receita do Dia 1 só vira caixa no Dia 4 — os dias 1-3 são cobertos 100% pelo float. Esse é exatamente o descasamento que a tabela existe pra mostrar. Use o payout_lag REAL do membro: loja nova com hold/rolling reserve → montar a tabela com 7-14 dias, não +3d — ver o cenário na ETAPA 6.)

Alerte se `cash_float_needed_peak > cash_disponivel × 0.7`.
