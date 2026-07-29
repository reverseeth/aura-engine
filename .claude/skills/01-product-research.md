---
name: product-research
description: Engine completo de pesquisa e validação de produto. Use quando o membro disser "product research", "pesquisa de produto", "encontrar produto", "qual produto vender", ou quando estiver na situação A do setup (não tem produto). Faz filtragem técnica, validação de Trends, trademark, Meta Ad Library, review mining, validação de eficácia, análise estratégica completa usando os frameworks, e entrega ranking com veredicto + plano preliminar + brand.md inicial pro produto #1.
---

# Product Research Engine

## Quando Usar
Quando o membro ainda não tem produto ou quer validar/encontrar um novo produto pra testar. Esta skill existe pra reduzir drasticamente o risco de escolher um produto ruim — sai com um veredicto fundamentado em frameworks em vez de "parece interessante".

## Antes de Começar

0. **Idioma do relatório (rule 0 — INVIOLÁVEL)**: leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language`.
1. Leia `workspace/profile.md` pra entender o contexto do membro (budget, ferramentas disponíveis, se tem SpyBox)

> **Índice completo dos frameworks desta skill: `.claude/lib/kb-index/` (mapa skill→domínio no README; catálogo machine-readable em `frameworks.json`).** Skill 01 puxa do domínio `product-research` (29 sistemas nomeados). Nas ETAPAS abaixo, onde a skill pede "puxe os SISTEMAS NOMEADOS", rode `search_knowledge` com a `best_query` EXATA de cada framework relevante — nunca query genérica tipo "product research" ou "market sophistication".

2. **Puxe os SISTEMAS NOMEADOS da base — não query genérica.** Antes da análise, rode `search_knowledge` com a `best_query` de cada framework que esta skill aplica abaixo (estão embutidos por NOME nas ETAPAS 2, 8 e 10). A lista completa do domínio `product-research` está em `.claude/lib/kb-index/` (`frameworks.json` / README). Puxe os SISTEMAS COMPLETOS (ex: os 5 estágios de sophistication de Schwartz com claims e respostas estratégicas, não "sophistication"), aprofunde em cada sub-conceito que aparecer, e aplique os thresholds/critérios LITERALMENTE nas etapas seguintes.
3. Internalize os frameworks ANTES de começar a análise. Não é pra "mencionar" — é pra APLICAR na escolha de cada produto.

## Fluxo da Skill

### ETAPA 0 — Pre-flight

Antes de qualquer outra coisa:

1. Leia `workspace/profile.md`. Se **não existir**, aborte com: `"Rode \`setup\` primeiro — profile.md ausente."` (profile/manifest totalmente ausentes mantêm abort: sem eles não há o que inferir; ofereça rodar o setup inline).
2. Localize `manifest.json`:
   - Procure um `manifest.json` em `workspace/*/manifest.json` cujo `setup_complete === true`.
   - Se existir, leia `product_slug` — este é o path canônico para qualquer salvamento (ver Etapa SALVAR).
   - **Se houver MAIS de um** manifest com `setup_complete === true` (membro roda 2+ produtos), NÃO escolha silenciosamente: liste os `product_name` e pergunte em 1 linha qual é o produto-alvo. Se o membro já nomeou o produto no trigger (ex: "product research do [produto]"), use esse sem perguntar.
   - Se **não existir**, aborte com: `"Rode \`setup\` primeiro — manifest.json ausente."` (ofereça rodar o setup inline).
3. Confirme que `00-setup` está em `skills_completed` do manifest. Caso contrário, re-rode o setup.
4. Use `product_slug` do manifest como `[produto]` padrão para todos os paths nesta skill até que o produto vencedor seja escolhido (ver Etapa SALVAR para substituição).

### ETAPA 0.5 — Motor de descoberta: o que é AUTOMÁTICO vs o que o MEMBRO COLA

Antes de qualquer coisa, fica CRISTALINO o que esta skill faz sozinha e o que depende de dado colado pelo membro. **Regra dura de honestidade: a AI NUNCA finge acessar ferramenta paga.** SpyBox, Kalodata e SimilarWeb são pagos e sem API que a AI consiga ler — sempre que precisar de um número dessas ferramentas, a AI diz EXATAMENTE o que olhar e onde, e trata o que voltar como input colado pelo membro (marcado como fonte manual no relatório).

Há **dois caminhos de descoberta**, e o que estiver disponível define o caminho:

**Caminho AUTO — TrendTrack MCP (runtime-discovery, sem nomes hard-coded):**

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis na sessão. Se SIM, este é o motor de descoberta automático (única fonte que dá revenue estimado de forma legítima e programática). **NÃO assuma nomes de tool fixos** (`find_winning_products`, `search_shops`, etc — a lista muda entre versões do MCP). Em vez disso:

1. **Descubra em runtime** quais tools `mcp__trendtrack__*` existem nesta sessão (inspecione os nomes disponíveis).
2. **Case por intenção, não por nome literal:**
   - Descoberta de winners (intenção "discover/find products/winning") → use pra puxar a leva inicial de candidatos.
   - Busca de lojas/concorrentes (intenção "search/find shops/similar") → fonte alternativa pra ETAPA 5 (sizing de concorrente) com revenue agregado.
   - Inspiração criativa (intenção "creative/inspiration/hooks/angles") → sinal extra pra ETAPA 8.
3. **Passe a intenção de filtro via params que a tool expõe** (não invente params): nicho do `profile.md`, país US, crescimento de tráfego alto, evitar marca grande já estabelecida (plano Shopify alto, se a tool filtrar isso), já rodando alguns dias, limite ~15 candidatos brutos. Se a tool não suportar um filtro, aplique-o depois nas ETAPAS 2-4 (são eliminatórios de qualquer jeito).
4. Se nenhuma tool de descoberta de produto existir entre as `mcp__trendtrack__*` (só tools de brief/monitor, por ex.), trate como **TrendTrack ausente pra esta etapa** e caia no caminho manual abaixo.

Custa créditos TrendTrack. Use 2-4 chamadas no máximo aqui — não saia explorando. Se uma chamada falhar (auth expirou, rate limit), caia pro caminho manual sem avisar o membro (silent fallback).

**Caminho MANUAL — membro cola do Kalodata/SpyBox (ETAPA 1):**

Se NÃO há `mcp__trendtrack__*` (ou nenhuma faz descoberta de produto), a leva inicial vem do membro colando dados do Kalodata/SpyBox — ver ETAPA 1. A AI não abre essas ferramentas; ela pede o dado e o recebe colado.

**Pós-descoberta (vale pros DOIS caminhos):** os ~15 candidatos (vindos do TrendTrack-auto OU colados pelo membro) ENTRAM na ETAPA 2. Os filtros eliminatórios da Aura são aplicados nas ETAPAS 2/3/4 já existentes:

- **AOV ≥ $60** → ELIMINATÓRIO (ETAPA 2) — precisa do supplier price do membro pra checar o 3× markup
- **3× markup** → ELIMINATÓRIO (ETAPA 2)
- **Peso/logística** → FLAG (não elimina) (ETAPA 2)
- **Google Trends 5 anos** → ELIMINATÓRIO se QUEDA consistente (ETAPA 3)
- **USPTO / trademark de marca grande** → ELIMINATÓRIO (ETAPA 4)

Antes da análise profunda (ETAPAS 5+), corte dos ~15 pros **top 8-10** por um `triage_score`:

```
triage_score = growth*0.35 + ad_traction*0.30 + price_fit_AOV60*0.20 + store_smallness*0.15
  (cada componente normalizado 0-1; ad_traction = densidade de ads ativos do nicho)

SEM dado de ads no momento do triage (caminho manual Kalodata/SpyBox — o membro cola
nome/preço/revenue, não densidade de ads), NÃO tente levantar Ad Library pros 15 candidatos
(é exatamente o custo que o triage evita). Re-normalize sem o componente:
  triage_score = growth*0.50 + price_fit_AOV60*0.30 + store_smallness*0.20
No caminho TrendTrack, use o sinal de ads que a própria tool de discovery já retornou.
```

**Regra:** o motor de descoberta (TrendTrack-auto OU Kalodata-colado) só ACELERA achar candidatos. Nunca pula os filtros eliminatórios — todo candidato passa pelas ETAPAS 2/3/4.

> **MAPA AUTO vs MANUAL (pipeline de 7 estágios desta skill) — leia antes de seguir:**
>
> | # | Estágio | Fonte | Como roda | Eliminatório? |
> |---|---------|-------|-----------|---------------|
> | 1 | **Descoberta** | TrendTrack `mcp__trendtrack__*` **OU** Kalodata/SpyBox | **AUTO** (TrendTrack, runtime-discovery) **OU** membro cola (Kalodata/SpyBox) | não (gera a leva) |
> | 2 | **AOV ≥ $60 + 3× markup** | dado do produto + **supplier price do membro** | semi-auto: AOV do dado; markup precisa o membro informar o supplier price (Alibaba/1688) | **SIM** |
> | 3 | **Peso / logística** | descrição do produto | AUTO leve (FLAG, não elimina) | não (flag) |
> | 4 | **Google Trends 5 anos** | Google Trends público | **AUTO** via WebFetch (fallback: fetcher Playwright → membro cola screenshot) | **SIM** se queda |
> | 5 | **Revenue / sizing do concorrente** | TrendTrack **OU** SimilarWeb/Kalodata | **AUTO** (TrendTrack) **OU** membro **COLA** (SimilarWeb é pago, sem API — revenue via SimilarWeb é SEMPRE colado) | não (calibra) |
> | 6 | **USPTO trademark** | uspto.gov público | **AUTO** via WebFetch (fallback: fetcher Playwright) | **SIM** se marca grande |
> | 7 | **Mecanismo único + avatar underserved** | frameworks da base Aura | **AUTO** (raciocínio sobre frameworks) | não (scoring) |
>
> Os estágios 2-7 mapeiam nas ETAPAS 2-8 abaixo. Onde diz "membro cola", a AI **pede o dado exato e espera** — nunca inventa o número nem finge ter aberto a ferramenta.

Se TrendTrack NÃO estiver disponível, pule a parte AUTO desta etapa e siga pra ETAPA 1 (caminho manual).

### ETAPA 1 — Receber Dados (Kalodata / SpyBox OU Fallback) — CAMINHO MANUAL

Esta etapa só roda quando a descoberta automática (TrendTrack) NÃO está disponível, OU pra complementar a leva auto com dados que só a ferramenta paga mostra. **A AI não abre o Kalodata/SpyBox — esses são pagos e sem API que a AI consiga ler.** Ela diz exatamente o que olhar e recebe o dado colado pelo membro, tratando-o como input manual.

Verifique em `workspace/profile.md` se o membro tem SpyBox disponível.

**SE tem SpyBox / Kalodata:**

Diga ao membro:

"Eu não consigo abrir o Kalodata/SpyBox por você (são pagos, sem acesso direto), então preciso que você abra e cole o resultado:
1. Aplique os filtros:
   - Period: Last 30 Days
   - Revenue: $30k - $400k
   - Revenue Growth Rate: >0%
   - Avg. Unit Price: >$15
   - Category: sem filtro (não marque nenhuma categoria)
2. Selecione entre 5 e 15 produtos que parecem promissores
3. Me mande: screenshots dos produtos OU copie e cole os dados (nome, preço, faturamento estimado, categoria, link)

> NOTA: unit price > $15 no Kalodata NÃO é o mesmo que AOV ≥ $60. Um produto de $25/unidade que vende em 3-pack atinge AOV $75 e PASSA na ETAPA 2. São dois filtros diferentes — não confundir o preço unitário da vitrine com o AOV viável depois de bundle/bump.

Tudo que você colar daqui eu marco como **fonte manual (colada por você)** no relatório, pra ficar claro de onde veio cada número. Se você também tiver dados do SimilarWeb sobre os concorrentes, cole também (a receita do SimilarWeb eu nunca consigo puxar sozinho — é sempre colada). Se não tiver, eu faço o que puder com fontes públicas."

**SE NÃO tem SpyBox/Kalodata (fallback):**

"Você não tem acesso ao SpyBox/Kalodata — sem problema. Me descreva o tipo de produto que te interessa:
- Categoria / nicho
- Faixa de preço-alvo
- Público que quer atingir

Eu pesquiso usando fontes públicas (Meta Ad Library, TikTok Shop Trending, Amazon Best Sellers, Reddit) e te volto com candidatos pra analisar."

ESPERE o membro responder antes de prosseguir. Se veio com fallback, faça as buscas iniciais automaticamente e apresente 8-12 candidatos identificados antes de seguir pras próximas etapas.

**Elicitação sem timeout automático**: Claude Code não tem timer interno dentro de uma skill. Espere a resposta do membro. Se o membro disser "não sei" ou "prossiga com dados públicos" ou se ele não souber responder de imediato, siga com fallback público (Meta Ad Library, TikTok Shop Trending, Amazon Best Sellers, Reddit via web search) e avise: `"Prosseguindo com dados públicos. Me passa SpyBox/Kalodata quando tiver e eu re-rankeio."` Não espere prazo — se membro respondeu com conteúdo vazio, é sinal de "sigo sem".

### ETAPA 2 — Filtragem Técnica (Thresholds Exatos)

Pra CADA produto enviado ou identificado, aplique os filtros técnicos nesta ordem. Cada FILTRO é eliminatório — descarta o produto se falha. Os critérios vêm dos frameworks sobre viabilidade e unit economics.

**Sistemas a puxar nesta etapa (rode a `best_query` exata, não query genérica):**
- **Technical Viability Criteria — economic gate** (rode `technical viability criteria AOV markup 3x Google Trends lightweight product filter`) — fonte literal dos thresholds AOV ≥ $60, markup 3×, peso/logística. Aplique os números exatos que vierem.
- **Halbert RFU Framework (Recency, Frequency, Unit of Sale)** (rode `Halbert RFU recency frequency unit of sale buyer evaluation`) — calibra se o unit-of-sale do produto sustenta AOV/repeat.

> **Markup 3× depende de dado do membro (supplier price).** O preço de venda você vê no dado de descoberta, mas o COGS real (custo do fornecedor + frete) a AI não tem como adivinhar. Antes de avaliar o filtro de markup, peça ao membro: *"Pra checar o markup 3×, me passa o preço de fornecedor (Alibaba/1688/AliExpress) de cada produto-candidato — ou um custo estimado se ainda não cotou. Sem isso eu uso uma estimativa de COGS conservadora (~30-40% do preço de venda) e marco o markup como ESTIMADO, não confirmado."* Se o membro não passar, rode com a estimativa conservadora e deixe a coluna Markup marcada como estimada (não dispare DESCARTA só com base em estimativa — vira FLAG até o membro confirmar o supplier price).

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

**Estágio AUTO.** Pra cada produto que passou na Etapa 2, consulte o Google Trends via WebFetch (dado público, a AI puxa sozinha):

- Termos principais do produto (nome genérico + categoria + problema que resolve)
- Janela: últimos 5 anos
- Comparar com termos relacionados e concorrentes quando relevante

> **Fallback em cascade (rule `.claude/rules/resilient-fetch.md`)** se o WebFetch do Trends falhar (bloqueio/anti-bot — trends.google.com é app só-JS, o WebFetch quase sempre falha): primeiro tente o fetcher Playwright da Aura: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text`. Só se o fetcher também falhar, peça ao membro pra abrir `trends.google.com`, setar a janela de 5 anos pro termo, e colar um screenshot da curva. Aí você lê a tendência pela imagem (visão nativa). Marque como fonte manual.

Classifique:
- **QUEDA CONSISTENTE** (tendência negativa há 12+ meses) → DESCARTA
- **FLAT** (estável, sem crescimento mas sem queda) → ACEITÁVEL
- **SUBINDO** (tendência positiva há 6+ meses) → BOM
- **SPIKE RECENTE** (subida vertical em 1-3 meses) → FLAG (pode ser fad temporário)

Mostre tendência por produto com o classificador aplicado.

### ETAPA 4 — USPTO Trademark + Brand Check

**Estágio AUTO.** Pra cada produto ainda na lista, consulte o USPTO via WebFetch (`tmsearch.uspto.gov`, base pública) + web search. Se o WebFetch barrar (o tmsearch é app JS pesado), use o fetcher Playwright: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (rule `.claude/rules/resilient-fetch.md`):

- Existe trademark ativo pro nome do produto, da marca mais conhecida vendendo ele, ou do mecanismo/fórmula?
- Classifique o owner:
  - **Marca grande com recursos legais** (ex: Unilever, P&G, Nestle, ou DTC de 9 dígitos) → DESCARTA (alto risco de C&D + ação legal)
  - **Marca pequena ou média** → PASSA (risco gerenciável com mecanismo próprio e copy original)
  - **Sem trademark ativo** → PASSA

Também busque no Google por `"nome do produto" site:bbb.org` e `"nome do produto" lawsuit OR complaint` — identifique se há histórico de problemas legais no nicho.

### ETAPA 5 — Meta Ad Library + Sizing do Concorrente (Agrupamento Por Aparições)

**Fontes desta etapa (auto vs manual):**

- **Ads ativos / criativos escalados** → AUTO: Meta Ad Library público (web search / fetch). Se TrendTrack estiver conectado, as tools `mcp__trendtrack__*` de busca de loja/concorrente (descobertas em runtime, ver ETAPA 0.5) dão isso refinado em 1-2 chamadas.
- **Revenue / sizing estimado do concorrente** → **AUTO se TrendTrack** (revenue agregado via tool); **MANUAL se não** — a AI **NÃO acessa o SimilarWeb** (pago, sem API que ela leia). Quando precisar do tamanho/tráfego de uma loja sem TrendTrack, ela pede o dado colado, com instrução exata:
  > *"Pra dimensionar o concorrente [loja X], abre o SimilarWeb (direto ou pelo painel do SpyBox) e me cola: visitas/mês (visits) + receita estimada da loja. Eu não consigo puxar esse número sozinho — a receita via SimilarWeb é sempre colada por você."*
  Trate o número como input manual e marque a fonte no relatório. NUNCA estime revenue do SimilarWeb sem o dado colado (não invente "deve faturar ~$200k").

Acesse o Meta Ad Library (web search / fetch quando possível) pra cada produto. A Ad Library é conteúdo só-JS — se o WebFetch voltar vazio ou barrado, use o fetcher Playwright: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (rule `.claude/rules/resilient-fetch.md`); só depois disso caia pra pedir screenshot ao membro.

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

Pra cada produto ainda na lista, pesquise (descoberta via `WebSearch`; aprofundamento via `WebFetch` — se barrado, fetcher Playwright: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode reviews|reddit|text`, conforme rule `.claude/rules/resilient-fetch.md`; só então fallback manual de paste/screenshot):

- **Amazon reviews** — pegue 4-star e 1-star reviews (as mais honestas). Foco: o que elogiam E o que reclamam. 4-star especialmente útil porque geralmente elogia MAS identifica um problema real que pode virar positioning. Se a página de reviews barrar o WebFetch, use `--mode reviews` (rola pra carregar os widgets lazy).
- **Reddit** — procure em subreddits relevantes (r/SkincareAddiction, r/HairLoss, r/BuyItForLife, etc). Use busca: `"nome do produto" OR "categoria" site:reddit.com`. Reddit bloqueia fetch direto por IP — pra abrir o thread inteiro, sempre `--mode reddit`.
- **TikTok comments** — nos próprios ads dos concorrentes identificados na Etapa 5. Comentários em viral posts (#nomedoproduto) também.
- **Fóruns** específicos do nicho (ex: realself.com pra beauty, forum.bodybuilding.com ou r/fitness / r/xxfitness pra fitness)
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

**Estágio AUTO (frameworks da base Aura).** Esta é a etapa onde os frameworks geram o insight final — mecanismo único possível e avatar underserved saem do raciocínio sobre os frameworks, sem depender de dado colado. Aplique TODOS em sequência pra cada produto remanescente.

**Puxe os SISTEMAS NOMEADOS desta etapa ANTES de raciocinar (rode a `best_query` de cada um, nunca query genérica — índice completo em `.claude/lib/kb-index/`):**
- **Schwartz Mass Desire Theory + 3-Stage Channeling** (rode `Schwartz mass desire theory channeling urgency staying power scope`) → sub-passo 1 (Magnitude).
- **Three Factors That Determine Product Difficulty** (rode `three factors determine difficulty desire magnitude market awareness sophistication`) → enquadra os sub-passos 1-3 (são os 3 fatores).
- **Cashvertising Life-Force 8 (LF8)** (rode `Cashvertising Life-Force 8 LF8 Whitman biological desires`) + **Six Mass Instincts** (rode `six mass instincts health sex status belonging control comfort technological problems`) → qual instinto biológico o desejo ataca (calibra Magnitude pra FORTE vs MÉDIO).
- **Hormozi Starving Crowd / Market Selection (4 Indicators)** (rode `Hormozi starving crowd market selection four indicators massive pain purchasing power`) → valida que o mercado tem dor massiva + poder de compra antes de pontuar.
- **Schwartz 5 Levels of Product-Market Awareness** (rode `Schwartz five stages of awareness Unaware Problem Solution Product Most aware`) + **AI Deep-Research Market Awareness Prompt** (rode `deep research prompt market awareness TAM percentage distribution final selection`) → sub-passo 2 (distribuição de awareness por % do TAM).
- **Schwartz 5 Stages of Market Sophistication** (rode `Schwartz market sophistication 5 stages mechanism claims`) → sub-passo 3 (estágio + resposta estratégica certa).
- **Two Forms of Differentiation (Mechanism vs Avatar Innovation)** (rode `two forms of differentiation mechanism innovation avatar innovation overlooked avatar`) → sub-passos 4 e 5 (UMP e avatar underserved são as duas formas).
- **Ries & Trout: Cherchez le Creneau (8 Holes in the Mind)** (rode `Ries Trout cherchez le creneau eight holes in the mind size price age`) → sub-passo 5 (achar a brecha de posicionamento/avatar livre).

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

**4. Possibilidade de Mecanismo Único** (mecanismo único do problema/da solução — UMP/UMS):

> Sistema-base deste sub-passo: **Two Forms of Differentiation — Mechanism Innovation** (já puxado no topo da ETAPA 8, rode `two forms of differentiation mechanism innovation avatar innovation overlooked avatar` se ainda não puxou). O mecanismo é a primeira das duas formas de diferenciar.

Aplique o filtro S.I.N. (Simple / Intuitive / New — o mesmo da Skill 04 e do kb-index):
- **Simple** — dá pra explicar em 1-2 frases que qualquer pessoa entende?
- **Intuitive** — faz sentido imediato ("ah, é ÓBVIO que isso funciona") sem exigir fé?
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

Inclua no topo do output desta etapa:

```
Ranking Generated at: YYYY-MM-DDTHH:MM:SSZ   (ISO-8601 UTC)
Formula:
  Total = (Magnitude × 2 + Sophistication × 2 + AwarenessFit + UMPotential + AvatarFit + OfferPotential + CreativePotential + TrendFit) / 10
  — Magnitude e Sophistication pesam 2× (filtros mais decisivos).
  — Todos os sub-scores são 1-10 inteiros ou com 1 casa.
  — Min aceitável pra TESTAR: ≥ 7.5. Min aceitável pra TALVEZ: 6.0-7.4. Abaixo de 6.0 → DESCARTA.
```

**Definição explícita de cada sub-score (use literalmente — elimina drift entre rodadas):**

- **Magnitude** (do desejo, ETAPA 8.1): FRACO = 2-3 · MÉDIO = 5-7 · FORTE = 8-10.
- **Sophistication** = FACILIDADE de diferenciação dado o estágio (sentido INVERTIDO do stage: quanto mais cedo o mercado, mais fácil diferenciar, maior o score). Stage 1-2 = 9-10 · Stage 3 = 6-7 · Stage 4 = 4-5 · Stage 5 = 2-3.
- **AwarenessFit** = quão bem o funil/copy viável bate com a distribuição de awareness dominante (ETAPA 8.2) e o budget do membro: distribuição majoritária em Most/Product Aware (PDP direta, conversão barata) = 8-10 · Solution Aware (landing com mecanismo) = 6-7 · Problem Aware (advertorial/listicle, conversão mais cara mas TAM maior) = 4-6 · majoritariamente Unaware = 2-3.
- **UMPotential** = score do filtro S.I.N. da ETAPA 8.4 — média dos 3 componentes **Simple / Intuitive / New** (simplicity/intuitiveness/novelty, como no `sin_score` da Skill 04) do mecanismo possível, 1-10 cada.
- **AvatarFit** = força do avatar underserved da ETAPA 8.5 (segmento ignorado claro e alcançável = alto; todos os concorrentes já falam com o mesmo público sem brecha = baixo).
- **OfferPotential** = potencial de stack/bundle/bump e AOV projetado da ETAPA 8.6.
- **CreativePotential** = ângulos não-usados + demonstrabilidade visual + viabilidade de UGC da ETAPA 8.7.
- **TrendFit** (bucket da ETAPA 3 → número): QUEDA = 2 · FLAT = 6 · SUBINDO = 9 · SPIKE = 5.

Crie um ranking dos produtos sobreviventes com score de 1-10 em cada dimensão:

| Produto | Magnitude | Awareness Fit | Sophistication | UM Potential | Avatar | Offer | Creative | Trend | **Total** |
|---|---|---|---|---|---|---|---|---|---|

Score final = média ponderada documentada acima. Apresente o cálculo numericamente pra pelo menos o Top 3.

> **Cross-check do ranking com o sistema de validação final** (rode `final validation Gemini GPT Perplexity Kimi rank products scale potential unique mechanism`): a base traz o protocolo **AI Final-Validation Ranking** que cruza scale potential × mecanismo único — use os critérios dele pra sanity-check do Top 3 antes de cravar o veredicto, garantindo que o produto #1 tem escala E diferenciação, não só um ou outro.

**Validação de mínimo (bloqueadora)**: se NENHUM produto atingiu score ≥ 6.0, **NÃO** declare "research completo". Em vez disso:

1. Liste por que cada candidato falhou (o filtro ou score dominante).
2. Sugira **3 novos candidatos** alinhados ao perfil do membro (budget, tools, interesse declarado) via web search em Meta Ad Library + TikTok Shop + Amazon Best Sellers. Pra escolher a nova leva, aplique **Hormozi Starving Crowd / Market Selection (4 Indicators)** (rode `Hormozi starving crowd market selection four indicators massive pain purchasing power`) e **Halbert Market-First Thinking** (rode `Halbert market-first thinking product-market inversion starving crowd`) — comece pelo mercado faminto, não pelo produto.
3. Retorne à Etapa 2 com essa nova leva. Repita até haver pelo menos 1 produto TESTAR ou o membro optar explicitamente por parar.

Pra CADA produto mostre:

**[Nome do Produto] — Score: X.X/10 — Veredicto: TESTAR / TALVEZ / DESCARTAR**

- **3 razões principais pra testar** (com fundamento em frameworks)
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

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/01-product-research/`.

Salve em DOIS arquivos dentro de `workspace/[produto]/` (onde `[produto]` = slug do PRODUTO VENCEDOR, não do produto original da pesquisa — assim as fases seguintes salvam no mesmo lugar):

1. **`01-product-research/product-research.md`** (a AI lê nas fases seguintes)
2. **`01-product-research/product-research.html`** (visualização humana — use `.claude/templates/aura-report-template.html` como base, self-contained com CSS inline + logo SVG do Aura (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto))

Conteúdo de ambos:
- Lista completa de todos os produtos analisados (mesmo os descartados, com razão)
- Tabela de filtragem técnica (Etapa 2)
- Resultados de Trends, Trademark, Meta Ad Library, Reviews (Etapas 3-6)
- Validação de eficácia (Etapa 7)
- Análise estratégica completa aplicando os 7 frameworks (Etapa 8)
- Ranking final com scores e veredictos (Etapa 9) — incluindo timestamp e fórmula explícita
- Plano preliminar pro produto #1 (Etapa 10)

**Atualize o `manifest.json`** (fonte única de verdade):

1. Se o `product_slug` do vencedor for diferente do slug temporário criado no setup:
   - `mkdir -p workspace/[novo-slug]/`
   - Mova (ou copie + remove) o manifest existente para o novo diretório
   - Atualize `product_slug` e `product_name` com os valores do vencedor
2. Adicione `"01-product-research"` ao array `skills_completed` (evite duplicatas)
3. Atualize `updated_at` com o timestamp atual (ISO-8601 UTC)
4. Grave (marcados como PRELIMINARES — a Skill 02 refina depois):
   - `product_vertical` — vertical/nicho do vencedor
   - `awareness_distribution` — distribuição estimada por nível de Schwartz da ETAPA 8.2 (objeto `{unaware, problem, solution, product, most}`)
   - `sophistication_stage` — estágio de sophistication da ETAPA 8.3 (1-5)
5. Preserve todos os campos preenchidos no setup (`budget_tier`, `product_url`, etc.)
6. Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` = `product_slug` do vencedor — atualiza o `ABRIR-AQUI.html`).

**Naming da marca — nome chiclete (antes de criar o brand.md):**

As marcas que mais vendem têm nome chiclete: criativo, que gruda na primeira vez que a pessoa ouve, e amarrado ao conceito central do produto (o problema, o momento, o mecanismo, a tribo). Frameworks da base pra fundamentar (puxar por nome): **Bencivenga's Benefit-Embedded Naming** (rode `Bencivenga benefit embedded naming product name headline miniature`), **Ries & Trout Naming as Positioning** (rode `positioning Ries Trout naming most powerful positioning tool`), **Gum Names** (rode `big idea gum names sticky nickname mechanism`).

- Gere 3-5 candidatos e recomende 1, com a lógica de cada um. O melhor candidato é o que gera VOCABULÁRIO próprio: rende verbo de campanha, status de cliente, apelido de mecanismo — um nome que só nomeia é fraco; um nome que cria linguagem carrega a marca inteira.
- **O que É gate**: colisão direta na MESMA categoria com marca ativa vendendo (confusão real de consumidor).
- **O que NÃO é gate no estágio de teste**: domínio exato ocupado (variação de domínio resolve); registro de marca ainda não feito (o custo de registro vem DEPOIS da validação com vendas, não antes); marca parecida em outra categoria que não fala do mesmo conceito. O check de trademark da ETAPA 4 informa o risco — não veta um nome genial pré-validação.
- O membro decide. Grave o nome escolhido (e o vocabulário que ele gera) no `brand.md`.

**Crie o `brand.md` do vencedor** (se ainda não existir `workspace/[produto]/brand.md` — membros de situação B/C/D já ganharam o deles no setup):

- Copie `.claude/templates/brand.md.template` pra `workspace/[produto]/brand.md`.
- Preencha o que a pesquisa já sabe: `{{ PRODUCT_SLUG }}` (slug do vencedor), posicionamento preliminar (1 frase, do ângulo de diferenciação da ETAPA 9/10), atributos de tom sugeridos pelo nicho/avatar, e "o que NUNCA dizer" (claims saturados da ETAPA 8.3).
- Paleta de cores, tipografia e logo ficam como `[preencher]` — o produto ainda não tem loja pra extrair identidade visual. A skill 07a (page design) lê este arquivo na brand discovery e só pergunta o que faltar.
- Avise o membro: `"Criei workspace/[produto]/brand.md com o posicionamento preliminar. Cores/fontes/logo ficam pra fase de page."`

Se o slug mudou, informe ao membro: `"Produto vencedor: [nome]. Movi os artefatos para workspace/[novo-slug]/."`

## Mensagem Final

Se houver produto TESTAR no ranking:

"Product research completo. [Nome do produto] venceu com score X.X/10.

Plano preliminar salvo em `workspace/[produto]/01-product-research/product-research.md`. Alinhamento com budget: [starter/standard/escala-inicial/escala-avançada] — viável.

Próximo passo: diga **'market research'** pra aprofundar a pesquisa e montar o Unified Research Brief. Se o produto é físico e você ainda não tem fornecedor, diga **'sourcing'** — a cotação roda em paralelo à pesquisa e fecha o custo real antes da oferta."

Se NENHUM produto passou (todos TALVEZ ou DESCARTAR):

"Nenhum produto dessa leva passou nos filtros críticos. Os principais bloqueios foram: [listar razões].

Antes de investir tempo nesses, vale buscar novos candidatos. Sugestões de filtros ajustados DERIVADOS do bloqueador mais comum nesta leva:
- Se bloqueio dominante foi **AOV** → buscar produtos com preço base ≥ $60 OU que suportam bundle 3-unit
- Se foi **Markup 3x+** → buscar fornecedores alternativos (1688, Alibaba Gold supplier) ou produtos com COGS < 30% do preço visto
- Se foi **Saturação/Claims saturados** → buscar nichos adjacentes (ex: se beauty skincare saturado, testar beauty devices ou supplements beauty)
- Se foi **Logística (peso, bateria)** → filtrar por peso < 500g e sem componentes eletrônicos

Volte ao Kalodata/SpyBox com esses filtros ou me descreva outro nicho que eu rodo a busca."
