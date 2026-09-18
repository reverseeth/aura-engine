# Tracking Setup · Referência: Contrato de leitura dos números (ETAPA 4B)

> Os quatro sistemas a puxar, o Blended ROAS como métrica de P&L, CAC versus CPA, o ponto cego da branded search e os handoffs pra ad-analysis, scale-engine e finance-engine. Abra na ETAPA 4B.

### ETAPA 4B — Leitura: o contrato de interpretação que este setup entrega

O relatório fixa COMO os números do stack escolhido serão lidos — é o que evita a briga "o Meta diz X, o Shopify diz Y" no dia 3 de tráfego.

**Puxe antes desta seção:**

- **Blended ROAS as the P&L Metric** (rode `blended ROAS Shopify dividido por spend total atribuição first click mente`)
- **CAC vs CPA Discipline (Shopify new customer = TRUE)** (rode `CAC igual spend dividido por clientes novos Shopify não CPA de plataforma`)
- **Regra de inflação do TA no Google** (rode `Triple Whale TA infla Google branded search comparar first click last click incremental`)
- **Google Search Stronghold + setup 80-20** (rode `Google Search Stronghold branded search proteger a marca converter copy do Facebook`)

1. **Blended ROAS é a métrica de P&L (o resultado do negócio):** receita do Shopify ÷ spend total de TODAS as plataformas. A atribuição da plataforma superatribui o próprio canal ("a atribuição de first click mente") — número de plataforma serve pra otimizar DENTRO dela, nunca pra responder "o negócio dá dinheiro?". É o nível 1 dos KPIs por maturidade da ETAPA 4, e a única leitura que o starter precisa no primeiro mês.
2. **CAC ≠ CPA:** CAC = spend do período ÷ **clientes NOVOS marcados no Shopify** (`new customer = TRUE`); o CPA que a plataforma reporta conta cliente recorrente e atribuição inflada. Cânone `.claude/lib/unit-economics/README.md` §3 — o relatório de tracking deixa as duas colunas nomeadas pra ninguém misturar depois.
3. **Branded search é o ponto cego da atribuição de terceiro:** o modelo TA do Triple Whale **infla o Google — sobretudo a busca pelo nome da marca**; antes de decidir qualquer coisa por esse número, comparar first click, last click e a leitura incremental. Vale dobrado se a Skill `ad-strategy` montar o **Google Search Stronghold** (o setup 80-20 que defende a branded search reaproveitando a copy que já converte no Facebook): a receita dessa campanha é em boa parte demanda que o Meta criou — leia-a como proteção de marca, não como canal incremental.

**Quem consome a decisão de atribuição desta skill (handoffs, 1 linha cada):**

- **Skill `ad-analysis`** usa a **hierarquia de decisão por atribuição** (blended decide o negócio, plataforma decide a otimização, terceiro levanta red flag) como régua de leitura sobre o `manifest.tracking.analytics_stack` gravado aqui.
- **Skill `scale-engine`** usa o **gate click-based** do Scaling Protocol (≥60% das purchases em 7-day click, `ad-taxonomy` §5) — o share de clique só é medível porque a ETAPA 3B fixou a janela baseline e preservou o Click ID; quando o gate falha, a `scale-engine` manda de volta pra cá re-medir.
- **Skill `finance-engine`** usa **Blended ROAS como métrica de P&L** (e CAC de clientes novos do Shopify) — os números do negócio inteiro saem da leitura blended fixada nesta seção, nunca do painel da plataforma.
