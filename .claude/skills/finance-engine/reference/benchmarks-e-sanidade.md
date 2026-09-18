# Finance Engine · Referência: Benchmarks, veredito, memo de decisão e checagens de sanidade (ETAPAs 13 e 14)

> As faixas de referência DTC, o Four Quarter Accounting, a exceção de COGS alto, o veredito com uma alavanca única, o memo de decisão em quatro blocos e as doze checagens de sanidade que bloqueiam o salvamento. Abra na ETAPA 13.

### ETAPA 13 — Benchmarks e veredito

Compare os números do membro contra as faixas de referência do canal direto ao consumidor (DTC). O que importa é a **tendência ao longo dos meses**, não o valor absoluto de um mês isolado.

| Indicador | Referência | Leitura |
|---|---|---|
| Margem bruta | **~70%** no canal direto ao consumidor | beleza tende a mais, vestuário a menos |
| Margem de contribuição | **10-20%** pra marca sem investidor | marca com aporte pode operar negativa de propósito pra escalar |
| Custos fixos | **abaixo de 10%** da receita | acima disso, o fixo come a escala antes de ela acontecer |
| COGS | **até 30%** como teto de longo prazo | acima, subir preço ou renegociar |
| Resultado operacional | acima de zero | depende do estágio e de haver aporte |

**Four Quarter Accounting** — a repartição de referência de um resultado mensal saudável: **25% COGS / 25% custo fixo / 25% custo de aquisição / 25% resultado**. Mostre a repartição real do membro ao lado dela. Não é regra rígida; é o jeito mais rápido de ver qual quarto está estourado.

**Exceção legítima de COGS alto:** COGS de 50-67% funciona quando o AOV é alto e a **margem de contribuição absoluta** é grande. Produto de US$ 3.000 com US$ 2.000 de margem por venda tem economia melhor que produto de US$ 30 com 70% de margem. Julgue pela margem em dinheiro por pedido, não só pela porcentagem.

**Veredito.** Feche com uma leitura em linguagem direta: a operação cobre os fixos hoje, quanto falta pra cobrir, e **qual alavanca única** move mais o resultado. Uma alavanca, não quatro.

**Memo de decisão (formato WAFM).** Quando o modelo produzir uma decisão que custa dinheiro — subir spend aceitando ROAS menor, cortar um custo fixo, entrar no stack de float, mudar preço —, feche o relatório com um memo curto de quatro blocos: **Por quê** (a dor ou oportunidade agora, com o número específico), **O quê** (a definição precisa da decisão), **Como** (a mecânica, os recursos e o prazo) e **Agora/Depois** (a ação, o dono e a data). Especificidade impiedosa: "as vendas caíram" não serve; "a receita caiu de US$ 127k pra US$ 98k em 30 dias, −23%" serve. Uma página, no máximo duas.

### ETAPA 14 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Nenhum número rotulado "lucro" sem custo fixo subtraído — no `.md`, no `.html` e no `dados.json`.
2. `monthly_model.operating_income` é `null` sempre que `fixed_costs_monthly` for `null`.
3. `cac_basis` é `shopify_new_customer` em todo cálculo de aquisição; nenhum CPA de plataforma entrou como CAC.
4. `roas_spiral.cut_spend_recommendation_allowed` é `false` sempre que os fixos forem desconhecidos.
5. `breakeven_roas_with_fixed` é maior que `breakeven_roas_variable_only` sempre que houver custo fixo positivo (se não for, a conta está errada).
6. Nenhum dos três campos que não se estima foi preenchido por estimativa; todos os ausentes estão em `pending_inputs[]`.
7. First order e repeat order aparecem em blocos separados, nunca somados numa média.
8. No Modo B: `cohorts.decay_source` declara explicitamente `calculated` ou `assumed`.
9. No Modo B com `cohorts.calibrated: false`: o payback foi modelado com a folga de 30 dias e isso está dito.
10. Os três cenários de stress test rodaram (cinco no Modo B, com os dois de caixa) e cada um tem `survives` preenchido.
11. `runway_months` existe sempre que houver caixa disponível informado.
12. O relatório contém só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa (rule `report-only-results.md`).
