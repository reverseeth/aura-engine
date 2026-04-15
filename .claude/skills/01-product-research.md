---
name: product-research
description: Engine completo de pesquisa e validação de produto. Use quando o membro disser "product research", "pesquisa de produto", "encontrar produto", "qual produto vender", ou quando estiver na situação A do setup (não tem produto). Faz filtragem técnica, validação de Trends, trademark, Meta Ad Library, review mining, validação de eficácia, análise estratégica completa usando os frameworks da vault, e entrega ranking com veredicto + plano preliminar pro produto #1.
---

# Product Research Engine

## Quando Usar
Quando o membro ainda não tem produto ou quer validar/encontrar um novo produto pra testar. Esta skill existe pra reduzir drasticamente o risco de escolher um produto ruim — sai com um veredicto fundamentado em frameworks da vault em vez de "parece interessante".

## Antes de Começar

1. Leia `/workspace/profile.md` pra entender o contexto do membro (budget, ferramentas disponíveis, se tem SpyBox)
2. Consulte a base Aura extensivamente sobre product research, critérios de validação, market desires (magnitude, durabilidade, urgência), market sophistication (5 estágios), market awareness (5 níveis de Schwartz), unique mechanisms (UMP/UMS, S.I.N. filter), avatar core/sub, offer potential, e potencial criativo. Aprofunde em cada framework que encontrar até ter domínio completo — cada sub-conceito que aparecer nos resultados de busca, explore. A vault tem frameworks específicos com thresholds, critérios, e exemplos que devem ser aplicados literalmente nas etapas seguintes.
3. Internalize os frameworks ANTES de começar a análise. Não é pra "mencionar" — é pra APLICAR na escolha de cada produto.

## Fluxo da Skill

### ETAPA 1 — Receber Dados (Kalodata / SpyBox OU Fallback)

Verifique em `/workspace/profile.md` se o membro tem SpyBox disponível.

**SE tem SpyBox / Kalodata:**

Diga ao membro:

"Preciso que você abra o Kalodata (ou SpyBox) e faça o seguinte:
1. Aplique os filtros:
   - Period: Last 30 Days
   - Revenue: $100k - $500k
   - Revenue Growth Rate: >0%
   - Avg. Unit Price: >$60
   - Category: sem filtro (não marque nenhuma categoria)
2. Selecione entre 5 e 15 produtos que parecem promissores
3. Me mande: screenshots dos produtos OU copie e cole os dados (nome, preço, faturamento estimado, categoria, link)

Se você também tiver dados do Similar Web sobre os concorrentes, cole também. Se não tiver, eu faço o que puder com outras fontes."

**SE NÃO tem SpyBox/Kalodata (fallback):**

"Você não tem acesso ao SpyBox/Kalodata — sem problema. Me descreva o tipo de produto que te interessa:
- Categoria / nicho
- Faixa de preço-alvo
- Público que quer atingir

Eu pesquiso usando fontes públicas (Meta Ad Library, TikTok Shop Trending, Amazon Best Sellers, Reddit) e te volto com candidatos pra analisar."

ESPERE o membro responder antes de prosseguir. Se veio com fallback, faça as buscas iniciais automaticamente e apresente 8-12 candidatos identificados antes de seguir pras próximas etapas.

### ETAPA 2 — Filtragem Técnica (Thresholds Exatos)

Pra CADA produto enviado ou identificado, aplique os filtros técnicos nesta ordem. Cada FILTRO é eliminatório — descarta o produto se falha. Os critérios vêm dos frameworks da vault sobre viabilidade e unit economics.

| Filtro | Critério | Ação se falha |
|---|---|---|
| **AOV viável** | Preço base + potencial de bundle/bump permite AOV ≥ $60 | DESCARTA |
| **Markup 3x+** | Preço de venda ≥ 3× (COGS + frete estimado) | DESCARTA |
| **Peso/logística** | Produto não é volumoso/pesado (facilita fulfillment internacional) | FLAG de risco (não descarta) |
| **Bateria/eletrônico** | Produto tem bateria, é eletrônico, ou tem defect rate potencial | FLAG (questão legal + retorno) |
| **Sazonalidade** | Produto só vende em época específica (ex: natal, verão) | FLAG (operação de curto prazo) |
| **Compliance** | Produto faz claim médico direto (fármaco, tratamento) | FLAG ou descarta dependendo da agressividade do claim |

Mostre uma **tabela comparativa** com cada produto e o resultado de cada filtro:

| Produto | AOV | Markup | Peso | Bateria | Sazonal | Compliance | Status |
|---|---|---|---|---|---|---|---|

Produtos descartados saem da análise. Produtos com flags continuam mas com o risco documentado pra ser reavaliado depois.

### ETAPA 3 — Google Trends (Janela 5 Anos)

Pra cada produto que passou na Etapa 2, pesquise no Google Trends (use web search):

- Termos principais do produto (nome genérico + categoria + problema que resolve)
- Janela: últimos 5 anos
- Comparar com termos relacionados e concorrentes quando relevante

Classifique:
- **QUEDA CONSISTENTE** (tendência negativa há 12+ meses) → DESCARTA
- **FLAT** (estável, sem crescimento mas sem queda) → ACEITÁVEL
- **SUBINDO** (tendência positiva há 6+ meses) → BOM
- **SPIKE RECENTE** (subida vertical em 1-3 meses) → FLAG (pode ser fad temporário)

Mostre tendência por produto com o classificador aplicado.

### ETAPA 4 — USPTO Trademark + Brand Check

Pra cada produto ainda na lista, pesquise (web search):

- Existe trademark ativo pro nome do produto, da marca mais conhecida vendendo ele, ou do mecanismo/fórmula?
- Classifique o owner:
  - **Marca grande com recursos legais** (ex: Unilever, P&G, Nestle, ou DTC de 9 dígitos) → DESCARTA (alto risco de C&D + ação legal)
  - **Marca pequena ou média** → PASSA (risco gerenciável com mecanismo próprio e copy original)
  - **Sem trademark ativo** → PASSA

Também busque no Google por `"nome do produto" site:bbb.org` e `"nome do produto" lawsuit OR complaint` — identifique se há histórico de problemas legais no nicho.

### ETAPA 5 — Meta Ad Library (CRÍTICO: Agrupamento Por Aparições)

Acesse o Meta Ad Library (web search / fetch quando possível) pra cada produto.

**Regras críticas de análise:**

1. **NÃO use "tempo de veiculação" como métrica de escala.** Muitos criativos rodam há meses sem spend.
2. **Agrupe criativos idênticos ou quase idênticos** (mesmo vídeo com variação de overlay, mesma copy com 1-2 palavras diferentes) e conte o número de APARIÇÕES.
3. **Mais aparições = mais ad sets ativos usando esse criativo = mais escalado**. Esta é a métrica que importa.

Para cada concorrente que vende o produto:
- Total de ads ativos no momento
- Agrupamento dos criativos por semelhança
- **Top 5-10 criativos por número de aparições**

Pra cada um dos top 5 criativos mais escalados, documente:
- Tipo (UGC falando, demonstração, antes/depois, depoimento, imagem estática, carrossel)
- **Hook exato dos primeiros 3 segundos** (texto E fala, transcrição literal)
- Descrição visual do hook (o que aparece na tela)
- Ângulo (qual razão de compra — problema, resultado, curiosidade, autoridade, comparação, social proof, controvérsia)
- Primary text do ad (copia literal)
- CTA (botão + copy)
- Landing page destino (PDP, landing page dedicada, advertorial)
- Aparições aproximadas (proxy de escala)

Se for vídeo, transcreva pelo menos o hook + 2-3 frases do corpo do script.

**Sinal de validação forte:** se múltiplos concorrentes (3+) têm 20+ ads ativos cada no mesmo produto, é porque tem tração real. Se todo mundo tem ≤5 ads, ou não há tração, ou o nicho está morto, ou é muito novo.

### ETAPA 6 — Review Mining (Voice of Customer Preliminar)

Pra cada produto ainda na lista, pesquise (web search):

- **Amazon reviews** — pegue 4-star e 1-star reviews (as mais honestas). Foco: o que elogiam E o que reclamam. 4-star especialmente útil porque geralmente elogia MAS identifica um problema real que pode virar positioning.
- **Reddit** — procure em subreddits relevantes (r/SkincareAddiction, r/HairLoss, r/BuyItForLife, etc). Use busca: `"nome do produto" OR "categoria" site:reddit.com`.
- **TikTok comments** — nos próprios ads dos concorrentes identificados na Etapa 5. Comentários em viral posts (#nomedoproduto) também.
- **Fóruns** específicos do nicho (ex: realself.com pra beauty, baltimoresportsfitness pra fitness)
- **"Tired of" + "tried everything" shortcuts**: buscar essas frases + categoria revela a exata frustração da pessoa pronta pra comprar

Extraia e organize:
- **DORES** — o que reclamam sobre produtos similares (com frequência de menção)
- **DESEJOS** — o que querem que o produto faça (com intensidade)
- **OBJEÇÕES** — o que impede de comprar (medo, preço, ceticismo, experiência ruim anterior)
- **LINGUAGEM EXATA** — frases literais dos consumidores. Mínimo 10-15 frases que vão direto pra copy e criativos depois. NÃO parafrasear.
- **GAPS** — reclamações recorrentes que NENHUM concorrente está resolvendo

### ETAPA 7 — Validação de Eficácia (Gimmick Check)

Pra cada produto, pesquise (web search):

- O produto realmente funciona como promete?
- Tem estudos clínicos, evidências publicadas, ou consensus científico?
- Consulte PubMed, Google Scholar, ou reviews de especialistas
- Veja o sentimento nos reviews 1-star: "não funcionou" aparece muito?

Classifique:
- **FUNCIONA COMPROVADAMENTE** (estudos + reviews consistentes) → VERDE
- **FUNCIONA PARCIALMENTE** (funciona pra alguns, não pra outros, ou com condições) → AMARELO — precisa gerenciar expectativas
- **GIMMICK** (zero evidência, reviews inconsistentes, promessa fantasiosa) → DESCARTA

Não venda placebo, não venda fraude. Mesmo que tenha demanda, o long-term é insustentável.

### ETAPA 8 — Análise Estratégica Completa

Esta é a etapa onde os frameworks da vault geram o insight final. Aplique TODOS em sequência pra cada produto remanescente:

**1. Magnitude do Desejo** (Schwartz / Breakthrough Advertising):
- **FRACO**: desejos superficiais (organizar mesa, gerenciar cabos) → preço baixo, volume alto, persuasão muito pesada pra justificar ads pagos. Geralmente inviável.
- **MÉDIO**: qualidade de vida (melhor sono, mais energia, reduzir estresse) → viável com preço médio e storytelling forte.
- **FORTE**: desejos universais (perder peso, atrair sexo oposto, eliminar dor crônica, reverter envelhecimento, fazer dinheiro) → ticket alto viável, persuasão mínima, crowd pronta pra comprar.

O produto precisa atacar um desejo MÉDIO ou FORTE pra ser viável com budget de ads. Se é FRACO, descarta (ou marca como inviável com o budget atual).

**2. Market Awareness — 5 Níveis de Schwartz**:

Estime a distribuição do TAM (Total Addressable Market) por nível:
- Unaware (não sabe que tem o problema)
- Problem Aware (sabe do problema, não sabe de soluções)
- Solution Aware (conhece soluções genéricas, não a sua)
- Product Aware (conhece seu tipo de produto, comparando)
- Most Aware (conhece sua marca especificamente)

A distribuição dita o tipo de funil e copy necessários:
- MAIORIA em Problem Aware → advertorial ou listicle (educação antes do pitch)
- MAIORIA em Solution Aware → landing page com comparação e mecanismo
- MAIORIA em Product Aware → PDP robusta com reviews, garantia, comparação
- MAIORIA em Most Aware → PDP enxuta direto à oferta

Se o mercado é majoritariamente Unaware/Problem Aware, a conversão é MAIS CARA mas o TAM é MAIOR. Documenta.

**3. Market Sophistication — 5 Estágios**:

Analise os claims que os concorrentes já usam (da Etapa 5):
- **Estágio 1** (virgin market): "eu tenho X" funciona. Raramente existe hoje.
- **Estágio 2**: claim direto com superlativo ("MAIS eficaz", "MAIS barato"). Ainda funciona em nichos novos.
- **Estágio 3**: claims diretos ficaram saturados — precisa de **mecanismo único** (ingrediente, processo, tecnologia com nome próprio).
- **Estágio 4**: mecanismos ficaram saturados — precisa de **nova informação** ou mecanismo expandido (causa raiz nova, descoberta recente).
- **Estágio 5**: tudo saturado — precisa de **identificação** (falar com quem a pessoa quer SE TORNAR, não com o problema).

Liste os claims saturados que devem ser EVITADOS. Defina a resposta estratégica certa pro estágio (mecanismo novo? informação nova? identificação?).

**4. Possibilidade de Mecanismo Único** (UMP/UMS):

Aplique o filtro S.I.N. da vault:
- **Specific** — pode ser nomeado especificamente?
- **Intriguing** — desperta curiosidade?
- **New** — soa novo pro mercado (mesmo que a ciência subjacente seja antiga)?

Consigo criar um mecanismo proprietário baseado em algo REAL do produto (ingrediente, feature, processo, combinação única)? Dê 1-2 exemplos preliminares (detalhe completo na Skill 04).

**5. Oportunidade de Avatar Underserved**:

Dos concorrentes analisados, todos falam com o mesmo público? Existe segmento ignorado (ex: todos falam com mulheres 25-35, ninguém fala com 45+; todos focam em iniciantes, ninguém foca em avançados; todos falam com o problema funcional, ninguém fala com a identidade por trás)?

**6. Potencial de Oferta**:
- Dá pra criar stack de valor convincente (bundle com savings claros)?
- Tem produto complementar pra bump/upsell?
- AOV potencial projetado?
- Consigo justificar preço premium com o mecanismo único?

**7. Potencial Criativo**:
- Tem storytelling possível (fundador, jornada, transformação)?
- Tem ângulos que os concorrentes NÃO usam (identificados nos gaps da Etapa 6)?
- Tem visual demonstrável (before/after, demo, ingredient drop)?
- UGC viável com custo razoável?

### ETAPA 9 — Ranking Final

Crie um ranking dos produtos sobreviventes com score de 1-10 em cada dimensão:

| Produto | Magnitude | Awareness Fit | Sophistication | UM Potential | Avatar | Offer | Creative | **Total** |
|---|---|---|---|---|---|---|---|---|

Score final = média ponderada (Magnitude e Sophistication pesam 2x — são os filtros mais decisivos).

Pra CADA produto mostre:

**[Nome do Produto] — Score: X.X/10 — Veredicto: TESTAR / TALVEZ / DESCARTAR**

- **3 razões principais pra testar** (com fundamento em frameworks da vault)
- **3 riscos principais** (com mitigação sugerida)
- **Ângulo de diferenciação sugerido** (1 frase)
- **Nível de dificuldade**: FÁCIL / MÉDIO / DIFÍCIL (considerando sophistication stage + budget do membro)

Veredito:
- **TESTAR**: score ≥ 7.5, zero DESCARTA em nenhum filtro, alinha com budget do membro
- **TALVEZ**: score 6.0-7.4, tem flags mas viável com ajustes
- **DESCARTAR**: score < 6.0 OU falhou em filtro crítico

### ETAPA 10 — Plano Preliminar pro Produto #1

Pro produto com maior score, entregue um plano inicial (detalhado depois nas skills 02-04):

**Mecanismo Único Sugerido:**
- Nome proprietário (2-4 palavras, memorável)
- Explicação de 2-3 frases (como funciona, por que diferente)
- Ingrediente/feature/processo base (a coisa REAL do produto)

**Avatar Principal Sugerido:**
- Quem é (demografia rápida)
- Dor central (frase exata tirada do review mining)
- Desejo central (frase exata)
- Trigger event típico (o que faz comprar AGORA)

**Estrutura de Oferta Preliminar:**
- Produto base: $X
- Bundle sugerido: 2-pack ou 3-pack com savings
- Bump sugerido: produto complementar de $Y
- Guarantee sugerido (tipo + duração)
- AOV projetado

**3 Hooks de Criativo (ângulos que os concorrentes NÃO usam):**
- Hook 1: [texto + tipo de criativo sugerido]
- Hook 2: [texto + tipo]
- Hook 3: [texto + tipo]

**Próximo passo recomendado:**
"Diga 'market research' pra aprofundar na pesquisa do [produto] e montar o Unified Research Brief que vai alimentar copy, oferta, e criativos."

## SALVAR

`/workspace/[nome-do-produto-vencedor]/01-product-research.md` contendo:
- Lista completa de todos os produtos analisados (mesmo os descartados, com razão)
- Tabela de filtragem técnica (Etapa 2)
- Resultados de Trends, Trademark, Meta Ad Library, Reviews (Etapas 3-6)
- Validação de eficácia (Etapa 7)
- Análise estratégica completa aplicando os 7 frameworks (Etapa 8)
- Ranking final com scores e veredictos (Etapa 9)
- Plano preliminar pro produto #1 (Etapa 10)

O nome da pasta usa o PRODUTO VENCEDOR (não o produto original da pesquisa), pra que todas as fases seguintes salvem no mesmo lugar.

## Mensagem Final

Se houver produto TESTAR no ranking:

"Product research completo. [Nome do produto] venceu com score X.X/10.

Plano preliminar salvo em `/workspace/[produto]/01-product-research.md`. Alinhamento com budget: [starter/standard/escala-inicial] — viável.

Próximo passo: diga **'market research'** pra aprofundar a pesquisa e montar o Unified Research Brief."

Se NENHUM produto passou (todos TALVEZ ou DESCARTAR):

"Nenhum produto dessa leva passou nos filtros críticos. Os principais bloqueios foram: [listar razões].

Antes de investir tempo nesses, vale buscar novos candidatos. Volte ao Kalodata/SpyBox com filtros ajustados (ex: [sugestão]), ou me descreva outro nicho que eu rodo a busca."
