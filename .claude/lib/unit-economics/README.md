# Unit Economics — cânone único

Fonte de verdade para margem, CAC, ROAS e decisão de spend. Skills 04, 11, 12 e 15 leem **daqui**; nenhuma redefine esses conceitos localmente.

Origem: fonte primária high-ticket 2026 (P1) + módulo de finanças da fonte primária (fontes prioritárias da base). Queries: `contribution margin stack custos variaveis first order repeat order`, `espiral do ROAS custos fixos cortar spend piora`, `projections 4 levers AOV CAC ad spend returning customers cohorts`.

## 1. Margem de contribuição ≠ lucro

**CM = receita − custos variáveis.** Lucro = CM − custos fixos. São coisas diferentes e chamar uma de outra é o erro mais caro do sistema.

O stack de custos variáveis, completo:

| Componente | Observação |
|---|---|
| COGS fully loaded | produto + embalagem + inbound freight + tarifa |
| Fulfillment / shipping | inclui a parcela de frete grátis absorvida |
| Processamento de pagamento | ~3% |
| Apps de assinatura | 0,5–1% quando há subscription |
| Fee de agência | quando é % do ad spend, é variável — entra aqui |
| Ad spend | o maior deles |
| Reembolso/chargeback esperado | provisão, não zero — *adição da engine: no material, refund aparece como guardrail/stress test ("+2%"), não como linha do stack; mantida aqui por prudência, contada UMA vez só (regra anti-dupla-contagem da skill 04)* |

> **Regra de nomenclatura (obrigatória em todo output):** nunca escreva "Lucro" sobre um número que não subtraiu custos fixos. O rótulo correto é **"Margem de contribuição"**. Se o membro não informou os fixos, diga isso explicitamente em vez de omitir — "CM de US$ X; sem os custos fixos informados não dá para dizer se há lucro".

## 2. First order vs repeat order

Economia diferente: o primeiro pedido carrega o CAC inteiro, o repeat não. Modelar os dois juntos esconde o que decide o negócio. Um produto pode ser deficitário no primeiro pedido e excelente no segundo — e a decisão de spend depende de qual dos dois você está olhando.

## 3. CAC ≠ CPA

- **CPA de plataforma** (Meta) conta conversões atribuídas pela plataforma, incluindo cliente recorrente.
- **CAC** = ad spend ÷ **clientes novos** (Shopify, `new customer = TRUE`).

Misturar os dois torna o modelo fake. Onde a decisão for de aquisição, use CAC do Shopify. Pisos de referência: **CAC mínimo US$ 15–25** em escala (a fonte deriva de CPM US$ 10–15 e CTR ~3%). *A glosa "abaixo disso, desconfie da atribuição antes de comemorar" é inferência nossa, coerente com a doutrina da fonte de que plataformas mentem com atribuição — não citação.*

## 4. A espiral do ROAS (o erro estrutural)

ROAS é adimensional e ignora custo fixo. Maximizá-lo isoladamente inverte a decisão certa:

> Operação a 4× ROAS com lucro. O ROAS cai para 3×. A reação intuitiva — cortar spend para "voltar ao 4×" — **aumenta o prejuízo**, porque os custos fixos não encolhem junto: menos receita para diluir a mesma base fixa. A reação correta costuma ser **aumentar** spend aceitando ROAS menor (no exemplo do material, 2,65× é o ponto de breakeven), porque mais volume dilui melhor o fixo.

**Regra operacional:** nenhuma recomendação de cortar spend por queda de ROAS pode ser emitida sem antes rodar a conta com os custos fixos na mesa. Se os fixos não forem conhecidos, a recomendação vira pergunta ("quanto você tem de custo fixo mensal?"), não instrução.

Benchmarks DTC de referência: margem bruta ~70%, CM 10–20%, fixos <10% da receita.

## 5. Como as skills usam

| Skill | Uso |
|---|---|
| 04 offer-builder | monta o stack de custos variáveis completo; rotula CM corretamente; aplica piso de CAC como gate |
| 11 ad-analysis | antes de recomendar corte por ROAS, aplica a seção 4 |
| 12 scale-engine | decisão de escala considera diluição de fixo, não só ROAS |
| 15 finance-engine | dono do modelo completo (4 alavancas, cohorts, ciclo de caixa) |
| 17 promo-engine | recalcula o breakeven com a margem promocional antes de ligar campanha de promo (gate da janela) |
