# Finance Engine · Referência: Monthly model, o resultado do mês decomposto linha a linha (ETAPA 2)

> O teste de classificação de custo, a tabela do modelo mensal na sequência do cânone, os dois números que reenquadram a pergunta (`gross_margin_needed_to_exist` e `revenue_at_gross_margin_to_exist`) e o comportamento com os fixos em `null`. Abra na ETAPA 2.

### ETAPA 2 — Monthly Model (o resultado do mês decomposto linha a linha)

O modelo mensal é a espinha dos dois modos. Custos **fixos** declarados em dinheiro; custos **variáveis** como **% do AOV**.

**Teste pra classificar um custo:** *"se eu dobrar a receita, esse custo dobra?"* Taxa de processamento: sim (variável). Ad spend: sim, às vezes mais que dobra. Fee de agência cobrado como % do spend: sim. App de assinatura: sim. Folha: não (fixo). Software: depende — alguns cobram por pedido. Aluguel, contabilidade, ferramentas: fixo.

Monte a tabela nesta ordem — ela é a mesma sequência do cânone §1, e nenhuma linha pode ser pulada:

| Linha | Como calcular |
|---|---|
| Receita | AOV × pedidos do mês |
| (−) COGS fully loaded (o custo do produto **entregue**: produto + embalagem + frete até o cliente + tarifa) | `cogs_breakdown.product_delivered` + `shipping_to_customer` + `pick_pack` + `taxes_and_duties` |
| **= Lucro bruto** | receita − COGS |
| Margem bruta % | lucro bruto ÷ receita |
| (−) Processamento de pagamento | `cogs_breakdown.payment_processing` (~3%) |
| (−) App de assinatura | `cogs_breakdown.subscription_app_fee` (0,5-1%, zero quando não há assinatura) |
| (−) Fee de agência variável | `cogs_breakdown.agency_fee_variable` (só quando é % do spend; fee de valor fixo é custo FIXO) |
| (−) Provisão de reembolso/chargeback | `cogs_breakdown.refund_chargeback_provision` (nunca zero) |
| (−) Ad spend | o maior custo variável de todos |
| **= Margem de contribuição** | receita − todos os variáveis acima |
| Margem de contribuição % | margem de contribuição ÷ receita |
| (−) Custos fixos mensais | `manifest.fixed_costs_monthly` — **`null` se não informado** |
| **= Resultado operacional** | **o único número que pode ser chamado de lucro.** `null` enquanto os fixos forem `null` |

**Os dois números que quase ninguém calcula e que mudam a conversa:**

- **`gross_margin_needed_to_exist`** = o próprio custo fixo mensal, em dinheiro. É o **lucro bruto** que a operação precisa gerar todo mês **só pra pagar o fixo**, antes de gastar um centavo em anúncio.
- **`revenue_at_gross_margin_to_exist`** = custo fixo mensal ÷ margem bruta %. É a receita que produz esse lucro bruto.

Com US$ 38,5k de custo fixo e 70% de margem bruta: a operação precisa de **US$ 38,5k de lucro bruto por mês só pra existir**, o que exige cerca de **US$ 55k de receita** — e isso ainda é antes de considerar o custo dos anúncios. Coloque os dois em destaque no relatório; são eles que reenquadram a pergunta "quanto eu preciso vender?".

Se os fixos forem `null`: a tabela para na linha de margem de contribuição, as duas últimas linhas ficam explicitamente marcadas como não calculáveis, e o relatório diz o que destrava.
