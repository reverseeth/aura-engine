# Finance Engine · Referência: O stack de float e o banking sheet semanal, só no Modo B (ETAPAs 10 e 11)

> As camadas do stack de float com o custo líquido, o efeito no modelo de caixa, a extensão ao fornecedor, os guard-rails, a estrutura e o ritual do banking sheet, as notas mensais e a camada contábil. Abra na ETAPA 10.

### ETAPA 10 — [Modo B] Ciclo de conversão de caixa (o stack de float)

Se o cliente te paga antes de você pagar as contas, dá pra escalar sem sangrar caixa. O stack, em camadas:

| Camada | O que é | Prazo |
|---|---|---|
| 1 — Faturamento da Meta | Cobrança mensal por fatura em vez de cobrança no cartão a cada gasto. Fatura mensal + prazo de graça ≈ **net 45** (modele com 44 por segurança) | ~45 dias |
| 2 — Serviço de pagamento de boletos | Pagar com cartão uma fatura que não aceita cartão (Melio, Bill.com, Plastiq). Custo ~2,5-2,9% | — |
| 3 — Cartão de prazo longo | Cartão de cobrança com **net 60** e ~1,5% de crédito de fatura de volta | +60 dias |
| **Total** | | **~105 dias de float** |

Custo líquido do stack: taxa de ~2,9% menos ~1,5% de volta ≈ **1,4% por 105 dias** — na prática, o crédito mais barato disponível pra uma operação de ecommerce. É o que permite ser negativo na aquisição e na primeira recompra e pagar a fatura com o dinheiro da terceira.

**Efeito prático no modelo:** com o stack ativo, o ad spend sai do cálculo de necessidade de caixa de 90 dias da ETAPA 6 — ele só deixa a conta no dia ~105. Recalcule `cash_needed_90d` com e sem o stack e mostre as duas linhas; a diferença entre elas costuma ser o que separa "não dá pra escalar" de "dá".

**Extensão ao fornecedor:** pagar a fábrica pelo mesmo caminho, ou negociar prazo direto, alinha o desembolso de COGS ao mesmo ciclo. Essa é a ponte com a operação de suprimento.

**Guard-rails (repetir no relatório, não resumir):** nunca escalar dívida mais rápido que a capacidade de entrega; rodar o stress test da ETAPA 12 **antes** de alavancar; saber a data exata de cada saída de caixa; não confiar em conta de pontos sem calcular; **float não conserta oferta quebrada**; não financiar caos operacional.

### ETAPA 11 — [Modo B] Banking sheet semanal e notas mensais

**Banking sheet** — o pulso do caixa real, e o único artefato desta skill que vira ritual.

- **Estrutura:** linhas = dias do mês. Colunas = entrada de caixa (repasse do processador, outras entradas) e, em negativo, despesa de negócio, folha, ad spend, investimento, retirada de sócio, despesa pessoal. Fecha com **fluxo líquido por dia, por semana e por mês**.
- **Ritual:** uma vez por semana (~45 min), abrir **todas** as contas e cartões e lançar transação por transação do período.
- **Regra:** transferência entre contas próprias **não conta** — só dinheiro novo entrando ou saindo de verdade (a taxa da transferência, sim).
- **Por que fazer você mesmo pelo menos no começo:** é assim que se pega cobrança estranha e assinatura esquecida que nenhum relatório agregado mostra.
- A skill salva o template em `banking-sheet.csv` com os cabeçalhos e as fórmulas de fechamento descritas, pronto pra abrir em planilha.

**Notas mensais obrigatórias.** Todo mês fora da curva ganha uma linha explicando **por quê**: ruptura de estoque, entrada de assinatura, promoção no site inteiro, conta de anúncio suspensa, sazonalidade, teste de oferta que mudou o CAC. Sem essas notas, o histórico vira ruído e a calibragem do cohort passa a corrigir o modelo pelo motivo errado. Grave em `monthly_notes[]` — mês, evento, efeito no número.

**Camada contábil.** O modelo desta skill é a camada de estratégia; ele assume que existe uma camada de escrituração (todas as transações categorizadas) e uma de relatórios (as três demonstrações). Se o membro não tem nem a primeira, diga isso como pendência com efeito prático — *"sem transações categorizadas, os números aqui valem como direção, não como fechamento"* — sem virar consultoria contábil.
