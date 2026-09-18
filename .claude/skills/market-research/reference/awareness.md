# Market Research · Referência: Product-Market Awareness, os 5 níveis de Schwartz (ETAPA 2)

> Os sistemas a puxar, os sinais a pesquisar na web, a estimativa da distribuição do TAM, a tabela de defaults por bucket com o racional do 30/38, a nota Schwartz sobre a massa do mercado, o modo híbrido, a regra do nível dominante e do empate (`dominant_awareness_secondary`) e as implicações práticas por nível. Abra na ETAPA 2.

### ETAPA 2 — Product-Market Awareness Analysis (5 Níveis de Schwartz)

**Sistemas a puxar da base antes de estimar (rode cada `best_query`):**
- **Eugene Schwartz — 5 Stages of Awareness** (rode `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware`)
- **Awareness TAM Distribution (1/13.5/60/99% pyramid)** (rode `awareness levels percentage TAM distribution problem aware unaware easiest convert`) — calibra a distribuição numérica do TAM
- **Awareness Stage Headline Strategy (5 stages + 7 superiority tasks)** (rode `Schwartz awareness stage headline strategy seven tasks superiority approaches`) — alimenta as implicações de copy por nível
- **Deep Research AI Prompt (Awareness assessment)** (rode `deep research AI prompt market awareness TAM distribution Schwartz levels geography`) — estrutura a estimativa por geografia
- **Schwartz↔TTM↔Brunson Awareness Mapping Table** (rode `Schwartz TTM Brunson awareness mapping table copy approach by stage`) — cruza awareness com abordagem de copy/temperatura de tráfego

Pesquise (web search) sinais de cada nível de awareness:
- Volume de busca por termos do problema (Google Keyword Planner, trends)
- Volume de busca por termos da categoria de produto
- Ratio: busca por problema / busca por produto indica distribuição de awareness
- Social chatter: Reddit, TikTok, Twitter — as pessoas falam do problema, da solução, ou da marca específica?
- Artigos, blog posts, conteúdo de influencers no nicho

**Estime a distribuição do TAM por nível** (em porcentagem):
- X% Unaware (não sabe do problema)
- X% Problem Aware (sabe do problema, não sabe de soluções)
- X% Solution Aware (conhece soluções genéricas)
- X% Product Aware (conhece categoria de produto)
- X% Most Aware (conhece sua marca especificamente)

**Defaults por categoria** — se o membro não sabe estimar e a web search não trouxer sinais suficientes, pergunte em qual bucket o nicho se encaixa e aplique o default correspondente (marque `awareness_distribution_source = "default"` no JSON companion):

| Bucket | unaware | problem_aware | solution_aware | product_aware | most_aware |
|---|---|---|---|---|---|
| Nicho novo | 45 | 35 | 13 | 6 | 1 |
| Nicho maduro | 15 | 30 | 38 | 14 | 3 |
| Commodity saturado | 8 | 25 | 40 | 22 | 5 |

> **Racional do 30/38 no nicho maduro:** os dois níveis do meio ficam a 8pp de distância de propósito — assim o DEFAULT nunca cai sozinho na regra de empate (±5pp) descrita abaixo. Híbrido tem que nascer de sinal REAL da pesquisa (palpite do membro + web signals apertados), nunca do default.

> **Nota Schwartz:** o grosso do mercado vive quase sempre em **problem_aware** ou **solution_aware** — é onde estão a maioria dos compradores que ainda não escolheram marca. `product_aware` é tipicamente 5-15% (já conhece a categoria) e `most_aware` é tipicamente só 1-5% (já conhece sua marca específica). Desconfie de qualquer distribuição que jogue 10%+ em `most_aware` num produto que ainda não tem brand reconhecida — isso quase nunca é real e infla a expectativa de quem chega pronto pra comprar.

Se o membro der um palpite, mas a pesquisa web sugerir algo diferente, use **hybrid**: média entre palpite e default (marque `awareness_distribution_source = "hybrid"`).

Defina o nível **DOMINANTE** — o de maior percentual na distribuição (com os defaults acima, nenhum nível chega a 50%, e tudo bem: dominante = o maior). Se dois níveis adjacentes empatarem (±5 pontos percentuais), trate como híbrido e documente os dois: grave em `dominant_awareness` o nível de **MAIOR intenção de compra** dos dois (o mais avançado no espectro Schwartz — ex: empate problem/solution → `solution_aware`) e o outro em `dominant_awareness_secondary` (campo opcional do dados.json — só existe no empate). As skills `copy-engine` e `page-design` leem esse campo secundário pra tratar a página/lead como híbrido. Este nível vai ditar TODA a estratégia de copy, página, e criativos.

**Implicações práticas a documentar:**
- Problem Aware → advertorial ou listicle obrigatório (educação antes do pitch). PDP direta NÃO converte.
- Solution Aware → landing page dedicada com educação sobre diferenciação + mecanismo único forte.
- Product Aware → PDP robusta com comparação, reviews, garantia, proof stacking.
- Most Aware → PDP enxuta com foco na oferta (preço, bundle, urgência).
