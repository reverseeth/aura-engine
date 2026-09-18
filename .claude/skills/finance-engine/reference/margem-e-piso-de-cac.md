# Finance Engine · Referência: Margem de contribuição, ponto de cobertura do fixo e piso de CAC (ETAPAs 3 e 4)

> Os três números de cobertura do fixo, a separação obrigatória de first order e repeat order com o exemplo canônico, o piso físico do CAC no Meta, as três checagens do CPA-alvo e a ordem de ataque quando o modelo está no vermelho. Abra na ETAPA 3.

### ETAPA 3 — Margem de contribuição e o ponto de cobertura do fixo

A margem de contribuição é **a lucratividade de escalar**: se a receita dobra, ela aproximadamente dobra. O custo fixo não. Por isso a pergunta certa nunca é "meu ROAS está bom?", e sim **"minha margem de contribuição cobre meus fixos?"**.

Calcule e apresente três números:

- **`contribution_margin_monthly`** — em dinheiro e em %.
- **`fixed_cost_coverage_ratio`** = margem de contribuição ÷ custo fixo mensal. Abaixo de 1,0, a operação consome caixa todo mês, por mais bonito que esteja o ROAS.
- **`revenue_to_cover_fixed`** = custo fixo mensal ÷ margem de contribuição %. É a receita mensal em que a operação empata de verdade. A margem de contribuição já é líquida de ad spend, então essa receita pressupõe a mesma eficiência de mídia do mês que serviu de base — se o CAC piorar, o ponto de equilíbrio sobe junto.

**Separe first order de repeat order (cânone §2), sempre.** São economias diferentes: o primeiro pedido carrega o CAC inteiro e os fees atrelados a spend; a recompra não carrega nenhum dos dois. Modelar os dois juntos esconde a decisão. Use `unit_economics` (first order) e `unit_economics.repeat_order` do `offer-builder/dados.json` — a `offer-builder` já entrega separado. Um produto pode ser deficitário no primeiro pedido e excelente no segundo, e a decisão de spend depende de qual dos dois você está olhando.

Exemplo canônico da separação, pra calibrar a leitura: pedido de US$ 100 com COGS US$ 35, processamento US$ 3,30, app US$ 1, CAC US$ 40 e fee de agência US$ 2 → margem de contribuição do **1º pedido = US$ 18,70**. O **pedido de recompra**, sem CAC e sem fee de agência, dá **US$ 60,70**. Com o CAC subindo a US$ 70, o 1º pedido vira −US$ 12,80 — e uma única recompra em 90 dias devolve +US$ 47,90.

### ETAPA 4 — Piso de CAC e checagem do CPA-alvo

**Piso físico do CAC no Meta:** existe um chão dado por CPM e CTR. No melhor caso realista (CPM ~US$ 10-15, CTR ~3%), o CAC mínimo em escala fica em **US$ 15-25** (cânone §3). Abaixo disso, desconfie da atribuição antes de comemorar — quase sempre é CPA de plataforma disfarçado de CAC.

Três checagens, nesta ordem:

1. **`cac_max_first_order`** = `unit_economics.weighted_margin_per_order`. É o CAC em que o primeiro pedido empata. Acima dele, o primeiro pedido é deficitário — o que **pode** ser certo, mas só com LTV medido e janela de payback definida (ETAPA 9).
2. **CPA-alvo da `offer-builder` é alcançável?** Compare `target_cpa_primary_2x` e `target_cpa_primary_3x` contra o piso de US$ 15-25. Se o alvo estiver **abaixo do piso**, o problema não é mídia — é AOV. Diga isso sem rodeio: nenhuma otimização de criativo faz o Meta entregar cliente novo abaixo do chão de CPM.
3. **AOV sustenta tráfego pago?** Esta é a barômetro que **não conserta com trabalho**. CAC, LTV e COGS são consertáveis; AOV baixo demais não. Produto de AOV abaixo de ~US$ 30 raramente fecha conta em escala — a saída é AOV e LTV (bundle, assinatura, upsell), não "mídia melhor". Para assinatura: mínimo absoluto US$ 29,99, faixa realista US$ 39-49.

Ordem de ataque quando o modelo está no vermelho, do mais fácil pro mais difícil: **CAC → LTV → COGS → AOV**. COGS acima de **30% é teto de longo prazo** — acima disso, subir preço, renegociar volume ou trocar de fábrica. Volume destrava negociação: 4× de volume costuma comprar 2 pontos de COGS, e o plano de processamento melhora perto de 8 dígitos anuais.
