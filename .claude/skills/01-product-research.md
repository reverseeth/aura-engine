---
name: product-research
description: Engine de pesquisa de produto por recombinação de elementos validados. Use quando o membro disser "product research", "pesquisa de produto", "encontrar produto", "qual produto vender", ou quando estiver na situação A do setup (não tem produto). Descobre marcas DTC que já escalam no nicho de health & supplements via TrendTrack (MCP ou manual, com dois conjuntos de filtros fixos — native ads em imagem e em vídeo), monta a ficha completa de cada marca (LP mais escalada, ads mais escalados, tráfego, oferta, mecanismos, ângulo), valida com Google Trends (problema + ingrediente, 5 anos, US) e com as reviews de 1-2 estrelas do Trustpilot, decompõe cada marca em elementos validados, monta jogadas de recombinação (nunca clonar, nunca criar do zero), rankeia pelos eixos de score e salva o banco de marcas no Notion (ou em HTML na pasta da Aura).
---

# Product Research Engine

## Quando Usar

Quando o membro ainda não tem produto ou quer encontrar o próximo. A skill existe pra responder uma pergunta só: **qual combinação de elementos que o mercado já provou (mecanismo, ângulo, formato do produto, posicionamento, oferta) eu consigo montar de um jeito que nenhum concorrente escalado está usando — sem clonar ninguém e sem inventar nada do zero?**

A tese que governa a skill inteira:

- **Clonar** uma marca escalada coloca o membro num leilão com quem já tem histórico de pixel, prova social e caixa. Sem diferencial, ele paga o CPM mais caro pra entregar a mesma mensagem.
- **Criar do zero** (mecanismo novo, formato novo, ângulo nunca testado) custa o teste inteiro — e a maior parte dos testes do zero morre.
- **Recombinar** elementos validados por marcas diferentes é o meio do caminho: cada peça já provou que vende, e a combinação é nova. O máximo de invenção permitido é **aprimorar** um mecanismo que já escala.

## Antes de Começar

0. **Idioma do relatório (rule 0 — INVIOLÁVEL)**: leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo, páginas do Notion) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (hooks, headlines, ads, páginas) e VOC literal (frases de review) permanecem SEMPRE em inglês US**, independente do `report_language`.
1. Leia `workspace/profile.md` — budget diário, ferramentas conectadas (TrendTrack, Notion), nicho de interesse se o membro já declarou.

> **Índice completo dos frameworks desta skill: `.claude/lib/kb-index/` (mapa skill→domínio no README; catálogo machine-readable em `frameworks.json`).** A skill 01 puxa do domínio `product-research`. Nas ETAPAS 5, 7 e no naming, onde a skill pede "puxe os SISTEMAS NOMEADOS", rode `search_knowledge` com a `best_query` EXATA de cada framework — nunca query genérica tipo "product research" ou "market sophistication".
>
> **Contrato de cobertura (regra 2026-09 do kb-index):** a puxada é COBERTURA do tópico, não amostra. No início de cada ETAPA que consulta a base, abra o domínio `product-research` inteiro no `frameworks.json` e enumere TODAS as entradas cujo `use_in_skill` inclui esta skill. As queries embutidas nas ETAPAs são o núcleo mínimo garantido, **nunca o teto**: entrada relevante pra fase que não está embutida é pra puxar do mesmo jeito. Não repita framework já puxado na mesma sessão.

2. **Puxe os SISTEMAS COMPLETOS**, não resumos (ex: os 5 estágios de sophistication de Schwartz com claims e respostas estratégicas, não "sophistication"). Internalize ANTES de analisar — os frameworks são pra APLICAR na decomposição e no ranking de cada marca, não pra citar.

## Fluxo da Skill

### ETAPA 0 — Pre-flight

1. Leia `workspace/profile.md`. Se **não existir**, aborte com: `"Rode \`setup\` primeiro — profile.md ausente."` (ofereça rodar o setup inline).
2. Localize `manifest.json`:
   - Procure um `manifest.json` em `workspace/*/manifest.json` cujo `setup_complete === true`.
   - Se existir, leia `product_slug` — é o path canônico pra qualquer salvamento até o produto vencedor ser escolhido (ver SALVAR).
   - **Se houver MAIS de um** manifest com `setup_complete === true`, NÃO escolha silenciosamente: liste os `product_name` e pergunte em 1 linha qual é o alvo. Se o membro já nomeou o produto no trigger, use esse.
   - Se **não existir**, aborte com: `"Rode \`setup\` primeiro — manifest.json ausente."` (ofereça rodar o setup inline).
3. Confirme que `00-setup` está em `skills_completed`. Caso contrário, re-rode o setup.
4. **Nicho.** Default desta skill é **health & supplements** (é o nicho dos filtros fixos da ETAPA 0.5). Se o membro quer outro nicho, ele diz e você troca só o filtro de nicho — o resto do método é idêntico.
5. **Onde salvar o banco de marcas.** Verifique se há tools de Notion na sessão (prefixo `mcp__claude_ai_Notion__` ou `mcp__notion__` — qualquer prefixo com `notion`). Se NÃO houver, pergunte UMA vez, em 1 linha:

   > "Quer que eu salve o banco de marcas no Notion (uma página por marca, com links dos ads, LP, tráfego, reviews e a jogada recomendada)? Se sim, conecta o Notion MCP agora — no claude.ai / Claude Desktop: Settings → Connectors → Notion → conectar; no Claude Code: `claude mcp add --transport http notion https://mcp.notion.com/mcp` e autorize no browser. Se preferir, eu salvo tudo em HTML na pasta do produto."

   Grave a escolha (`notion` ou `html`) e siga. A pesquisa não espera o Notion — ela roda igual; só o destino muda (ver SALVAR).

### ETAPA 0.5 — Motor de descoberta: TrendTrack (MCP ou manual)

A fonte de descoberta é o **TrendTrack — Explorer → Meta Ads**, com dois conjuntos de filtros fixos. O objetivo é achar **native ads** (anúncio que parece conteúdo, com copy longa) de marcas DTC que já escalam no nicho — imagem e vídeo separadamente, porque os dois formatos revelam marcas diferentes.

**Pesquisa 1 — native ads em IMAGEM:**

```
Status: active
Media type: image
Days Running: min 10
Ad creation date: last 30 days
Language: english
Ad rank: top 10%
Growth rank: rising
Description Length: min 1500
Ad countries: only US
Niche: health & supplement
Monthly traffic: min 300k
Sort by: longest running (ou ad rank)
```

**Pesquisa 2 — native ads em VÍDEO:**

```
Status: active
Media type: video
Days Running: min 10
Ad creation date: last 30 days
Language: english
Ad rank: top 10%
Growth rank: rising
Ad countries: only US
Niche: health & supplement
Monthly traffic: min 300k
Sort by: longest running (ou ad rank)
```

Por que esses filtros: `Days Running ≥ 10` + `Ad creation date: last 30 days` isola ad **novo que já sobreviveu** (a marca está escalando agora, não um criativo velho rodando no automático); `Ad rank top 10%` + `Growth rank rising` pega o que está subindo; `Description Length ≥ 1500` (só na imagem) força native ad de copy longa, que é o formato que converte tráfego frio em supplements; `Monthly traffic ≥ 300k` garante marca com escala real, não teste de iniciante.

**Caminho A — MCP do TrendTrack (gasta créditos do membro):**

Verifique se há tools com prefixo `mcp__trendtrack__` na sessão. Se SIM:

1. **Rode a tool de créditos primeiro** (intenção *Account → créditos*, hoje `check_credits`) e diga ao membro em 1 linha quanto tem e quanto a pesquisa deve gastar (descoberta: 4-8 chamadas; ficha por marca: 2-3 chamadas × número de marcas pré-selecionadas). Se o saldo não cobre, rode a descoberta por MCP e faça a ficha por marca pelo caminho manual — ou tudo manual, o membro decide.
2. **Resolva o id do nicho** (intenção *lookup de filtros*, hoje `lookup_filter_ids` com `type: "categories"`, `query: "supplement"` — e também `"health"`; pegue os ids que casam com health & supplement).
3. **Rode as duas pesquisas** (intenção *Discover → ads em lote*, hoje `search_ads`). Mapeamento dos filtros da UI pros params da tool (NÃO invente params — se um filtro não existir na versão da tool, aplique-o você mesmo na leitura dos resultados):

   | Filtro da UI | Param da tool (hoje) |
   |---|---|
   | Status: active | `status: "active"` |
   | Media type | `media_type: "image"` / `"video"` |
   | Days Running ≥ 10 | `min_days_running: 10` |
   | Ad creation date: last 30 days | `created_after: "<hoje − 30 dias, YYYY-MM-DD>"` |
   | Language: english | `ad_languages: ["en"]` |
   | Ad rank: top 10% | `ad_rank_mode: "percentile"`, `max_ad_rank_value: 10` |
   | Growth rank: rising | `growth_rank: [{ "period": "last7d", "direction": "rising" }]` (se vier pouco resultado, `last30d`) |
   | Description Length ≥ 1500 (só imagem) | `min_description_length: 1500` |
   | Ad countries: only US | `ad_countries: { "include": ["US"] }` |
   | Niche | `category_ids: [<ids do passo 2>]` |
   | Monthly traffic ≥ 300k | `min_traffic: 300000` |
   | Sort by longest running / ad rank | `sort_by: "longestRunning"` / `sort_by: "adOrder"` |
   | (diversidade) | `max_ads_per_brand: 2`, `limit: 20`, `page: 1, 2, 3` |

   Passe `sort_by` SEMPRE — sem ele a tool aplica por default um filtro de alcance que só existe pra ads da União Europeia e devolve zero pra ads só-US. Se mesmo assim a resposta vier vazia ou magra, adicione `trend_signal: "relevance"`. **Regra de leitura:** o alcance publicado pela Meta só existe pra ads veiculados na UE — ad só-US aparece com alcance 0 sem significar gasto zero. Escala se lê por **dias no ar + duplicatas + ad rank + tráfego da loja**.
4. Pagine até juntar **15-25 marcas distintas** entre as duas pesquisas (uma marca pode aparecer nas duas — conta uma vez). Anote por ad: marca, domínio, link do ad (Ad Library / TrendTrack), URL de mídia (Media URL, senão Thumbnail URL), dias no ar, ad rank, duplicatas, tráfego mensal da loja, LP de destino.
5. Se uma chamada falhar (auth expirou, rate limit, créditos acabaram), caia pro caminho manual sem drama — diga ao membro exatamente o que fazer (abaixo) e continue de onde parou.

**Caminho B — manual (membro usa o TrendTrack no browser):**

Se não há MCP, ou os créditos acabaram, ou o membro prefere olhar com os próprios olhos:

> "Abre o TrendTrack → **Explorer → Meta Ads**. Aplica os filtros abaixo (dois passes: um com Media type = image + Description Length min 1500, outro com Media type = video sem esse filtro de tamanho). Ordena por **longest running** (ou ad rank). Vai abrindo os ads e, pra cada marca que fizer sentido, me manda:
>
> 1. Nome da marca + site
> 2. Link do ad (o link do TrendTrack ou do Ad Library) — os 2-3 ads mais antigos no ar da marca
> 3. Dias no ar de cada ad
> 4. Link da landing page do ad (o destino do botão)
> 5. Tráfego mensal da loja (aparece no card da marca)
> 6. Link do Trustpilot da marca (aparece na página da marca no TrendTrack)
>
> Pode mandar screenshot também, eu leio. Mira em 15-25 marcas. Marca que só vende na Amazon, marketplace ou gigante (Nestlé, Bayer, Unilever) não entra — quero DTC com loja própria."

Onde diz "membro cola", a AI **pede o dado exato e espera** — nunca finge ter aberto o TrendTrack nem inventa número.

**Critérios de pré-seleção (valem pros dois caminhos):**

- **DTC com loja própria** (Shopify ou equivalente) — não Amazon-only, não marketplace, não gigante de consumo.
- **AOV ≥ $60 contando a oferta inteira** — abra a LP/PDP e some o que a marca faz pra subir o ticket: preço base, bundle (3-pack/6-pack), assinatura, bump no carrinho, upsell pós-compra. Marca com produto de $29 que vende em 3-pack a $79 com upsell **passa**; marca de $39 unitário sem bundle nem upsell **não passa**.
- **O produto faz sentido** pro membro — ele conhece o nicho, consegue sourcing (fórmula pronta / white label na 01b), e o problema é real e recorrente (consumível = recompra).

Saída desta etapa: **lista de 15-25 marcas pré-selecionadas**, cada uma com domínio + ads + LP + tráfego + Trustpilot. Todas seguem pra ETAPA 1.

### ETAPA 1 — Ficha por marca (coleta profunda)

Pra CADA marca pré-selecionada, monte a ficha completa. É a matéria-prima de tudo que vem depois — quanto mais detalhada, melhor a recombinação.

**Com MCP (2-3 chamadas por marca):**

- **Ads mais escalados da marca:** `search_ads` com `query: "<domínio>"`, `search_in: "domain"`, `status: "active"`, `sort_by: "longestRunning"` (e uma segunda passada com `sort_by: "mostDuplicates"`). Pegue os **top 3-5** — link, mídia, dias no ar, duplicatas, formato, hook (primeiras linhas da copy / primeiros 3s), ângulo, LP de destino.
- **LP mais escalada:** `lookup_filter_ids` com `type: "landing_pages"`, `scope_domain: "<domínio>"`, `status: "active"` — devolve as URLs de destino com a contagem de ads ativos apontando pra cada uma. A LP com mais ads ativos é a **LP mais escalada**.
- **Loja:** `search_shops` com `query: "<domínio>"`, `match_mode: "exact"` — visitas mensais, nota e nº de reviews no Trustpilot, data de criação da loja, apps/tema (opcional).
- **Decomposição de 1 ad (opcional, quando o hook não está claro):** `scan_ad` com o `collation_id` do ad — hook, enquadramento da copy, estrutura, LP, veredito de escala.

**Manual:** o membro abre a página da marca no TrendTrack e cola os mesmos itens (ads mais antigos no ar, aba de landing pages, tráfego, Trustpilot).

**Leitura da LP (vale pros dois caminhos):** abra a LP mais escalada com `WebFetch`; se barrar (Cloudflare/JS), `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (rule `.claude/rules/resilient-fetch.md`); último degrau: o membro cola um print. Extraia:

- **Tipo de página** (advertorial / listicle / PDP / landing dedicada / quiz)
- **Headline e promessa central**
- **Mecanismo do problema** (o "por que as outras soluções falham" — a causa raiz que a marca nomeia)
- **Mecanismo da solução** (o "por que o nosso funciona" — ingrediente/ativo, processo, forma, dose, nome proprietário se houver)
- **Ângulo principal** (a razão de compra que a copy usa: problema, custo da alternativa, identidade, comparação, medo, curiosidade, autoridade)
- **Avatar** (com quem a página fala — idade, gênero, momento de vida, sub-grupo)
- **Formato do produto** (cápsula, gummy, pó, sachê, líquido, shot, patch…)
- **Estrutura de oferta**: preço base, bundles e preço por tier, assinatura (% off), bump, upsell pós-compra, garantia, frete, bônus — e o **AOV estimado** que sai disso
- **Prova** usada (reviews, número de clientes, estudos citados, autoridade, antes/depois)

**Ficha por marca (campos obrigatórios):**

| Campo | Conteúdo |
|---|---|
| Marca / site | nome + domínio |
| Visitas/mês | número do TrendTrack |
| Nicho / sub-nicho | ex: gut health → bloating |
| Produto + formato | ex: pó de fibra em sachê |
| Preço base / AOV estimado | $ / $ (com a conta: base × bundle + upsell) |
| LP mais escalada | link + tipo de página |
| Ads mais escalados | 3-5 links (+ mídia), com dias no ar, duplicatas, formato, hook, ângulo |
| Formato de criativo dominante | imagem native / vídeo UGC / vídeo talking head / demo |
| Mecanismo do problema | nome + lógica em 1-2 frases |
| Mecanismo da solução | nome + ingrediente/ativo + lógica em 1-2 frases |
| Ângulo principal | 1 frase de razão de compra |
| Avatar | quem, em 1 linha |
| Trustpilot | link + nota + nº de reviews (o veredito vem na ETAPA 3) |
| Fonte | `trendtrack_mcp` ou `manual` |

Vá salvando as fichas conforme fecha cada uma (Notion ou `banco-de-marcas.md` — ver SALVAR). Não deixe pra salvar tudo no fim: se a sessão cair, o trabalho fica.

### ETAPA 2 — Checagem 1: Google Trends (5 anos, US)

Pra cada marca, rode **duas** consultas no Google Trends: **o problema** que o produto resolve (ex: "bloating", "joint pain", "hair thinning") e **o ingrediente ou mecanismo** da solução (ex: "berberine", "collagen peptides", "psyllium husk"). Janela: **últimos 5 anos**, país: **US**.

Como rodar: `python3 .claude/lib/web-fetch/fetch.py "<termo>" --mode trends` (defaults já são US / 5 anos; devolve a série + classificação). NUNCA tente renderizar o site do Trends com `--mode text` — ele recusa navegador automatizado. Se o fetcher falhar, peça ao membro pra abrir `trends.google.com`, setar 5 anos / US e colar um print da curva de cada termo — você lê a tendência pela imagem.

**Regra de eliminação:** queda constante por 12 meses ou mais, dentro da janela de 5 anos → **elimina** (vale pro problema e pro ingrediente).

**Leitura dos dois termos juntos:**

- **Problema vivo define se o nicho vale a pena.** Problema em queda de 12+ meses = nicho encolhendo, elimina mesmo com ingrediente bom.
- **Ingrediente define se você chegou na hora.**
- **Problema subindo + ingrediente estável** = **melhor cenário** (demanda crescendo, mecanismo maduro e sem hype).
- **Ingrediente ou mecanismo subindo há 6+ meses** = ótimo cenário — a onda ainda está no começo.
- **Problema subindo + ingrediente em pico recente** = tarde. A marca pegou a onda cedo; o membro chegaria no pico. Aqui a jogada é **trocar o mecanismo** (ETAPA 6, padrão 3): manter o ângulo/problema e usar um ingrediente validado por outra marca que não esteja no pico.
- **Subida vertical em 1-3 meses** = **hype**. Na maior parte das vezes cai tão rápido quanto subiu. Não elimina sozinho, mas rebaixa o score e exige mecanismo alternativo.

Classifique cada termo em **QUEDA / ESTÁVEL / SUBINDO / PICO RECENTE / HYPE** e grave o **cenário** da marca (combinação dos dois) na ficha. Marca eliminada aqui sai da análise com o motivo registrado.

### ETAPA 3 — Checagem 2: Trustpilot, reviews de 1 e 2 estrelas

O TrendTrack traz o link do Trustpilot da marca. Entre nele e puxe as reviews negativas: `https://www.trustpilot.com/review/<domínio>?stars=1&stars=2&languages=all&sort=recency`. Cascade: `WebFetch` → se barrar, `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode reviews` (rola pra carregar os widgets) → se ainda barrar, o membro abre e cola as 20-30 reviews mais recentes de 1-2 estrelas.

Leia **no mínimo 20-30 reviews negativas** por marca e classifique cada uma em um tema:

- **Cobrança / assinatura** (cobrado sem querer, cancelamento difícil, refund lento)
- **Entrega / logística** (atraso, não chegou, embalagem)
- **Atendimento** (ninguém responde)
- **Eficácia** ("não funcionou", "não senti nada", "zero diferença", "waste of money")

**Regras de veredito:**

- Reviews reclamando de **cobrança e entrega** → dá pra resolver com fornecedor, operador logístico e checkout melhores. **Passa.** (E vira ângulo: "sem assinatura escondida", "cancela em 1 clique" são posicionamentos abertos.)
- Nota **abaixo de 4** mas as reclamações **não são sobre eficácia** → tudo bem. **Passa.**
- A **maioria** das reviews negativas fala de **eficácia** → **elimina.**
- Nota **abaixo de 4** com **muita gente dizendo que o produto não funciona** → **elimina.**

O porquê: produto que não funciona gera refund em massa no mês 2 e 3, quando o efeito prometido não aparece. A marca pode até estar escalando agora — ela está escalando em cima de churn, e o membro herdaria o mesmo churn ao usar o mesmo produto.

Grave na ficha: nota, nº de reviews, mix de temas (% por tema), veredito (**OK / cobrança-entrega / eficácia → eliminar**) e **5-10 frases literais** em inglês (com "tradução livre:" ao lado nos relatórios em pt-BR). As frases de eficácia dos concorrentes são matéria-prima de ângulo pra 02/06 ("I tried X for 3 months and nothing" é o hook de quem chega com mecanismo diferente).

**Marcas sem Trustpilot:** procure a mesma leitura em reviews da Amazon (se a marca vende lá), Reddit (`--mode reddit`) e comentários dos próprios ads. Sem NENHUMA fonte de review negativa, a marca segue com o veredito em aberto e o score de eficácia neutro.

Ao fim das ETAPAS 2 e 3, sobram os **finalistas** (alvo: 8-12 marcas). Marca eliminada permanece no banco com status `eliminada` + motivo — é informação de mercado, não lixo.

### ETAPA 4 — Decomposição em elementos validados

Aqui a skill deixa de olhar marca por marca e passa a olhar **peças**. Pra cada finalista, quebre a marca em elementos e registre, ao lado de cada um, a **evidência de validação** (dias no ar do ad mais antigo, ad rank, duplicatas, tráfego da loja, nº de ads ativos no mesmo ângulo):

| Elemento | O que é | Exemplo |
|---|---|---|
| **Mecanismo do problema** | a causa raiz que a marca nomeia pra explicar por que as soluções comuns falham | "your gut lining is leaky, that's why probiotics never worked" |
| **Mecanismo da solução** | o ingrediente/processo/forma que resolve a causa raiz, com nome | "butyrate-first formula", "8-hour release" |
| **Ângulo** | a razão de compra que o ad usa | custo anual da alternativa; "I tried everything"; identidade ("for women over 45") |
| **Formato do produto** | a forma física | gummy, pó em sachê, shot, cápsula, patch |
| **Posicionamento / avatar** | com quem a marca fala e como se enquadra | "a marca do despertar das 3h", "gut health pra quem usa GLP-1" |
| **Formato de criativo** | o tipo de peça que mais escala | native image de copy longa; UGC talking head; demo |
| **Estrutura de oferta** | como a marca sobe o ticket | 3-pack + assinatura + upsell de sono |

Depois, consolide o **pool cruzado de elementos validados** (todas as marcas juntas), agrupando elementos iguais/quase iguais e contando **em quantas marcas escaladas cada um aparece**:

- Elemento presente em **1-2 marcas** escaladas = **validado e ainda aberto** (a melhor matéria-prima).
- Elemento presente em **3+ marcas** no mesmo ângulo = **validado e saturado** naquele ângulo — só entra numa jogada se vier com outro ângulo, outro formato ou aprimorado (ETAPA 6).
- Elemento que nenhuma marca escalada usa = **não validado** — não entra em jogada nenhuma (é criação do zero).

Esse pool é a `validated_elements[]` do `dados.json` e a semente da `validated_library` que a Skill 03 constrói em profundidade.

### ETAPA 5 — Análise Estratégica (frameworks da base)

**Puxe os SISTEMAS NOMEADOS desta etapa ANTES de raciocinar (rode a `best_query` de cada um — índice completo em `.claude/lib/kb-index/`):**
- **Schwartz Mass Desire Theory + 3-Stage Channeling** (rode `Schwartz mass desire theory channeling urgency staying power scope`) → sub-passo 1 (Magnitude).
- **Three Factors That Determine Product Difficulty** (rode `three factors determine difficulty desire magnitude market awareness sophistication`) → enquadra os sub-passos 1-3.
- **Cashvertising Life-Force 8 (LF8)** (rode `Cashvertising Life-Force 8 LF8 Whitman biological desires`) + **Six Mass Instincts** (rode `six mass instincts health sex status belonging control comfort technological problems`) → qual instinto biológico o desejo ataca (calibra Magnitude).
- **Hormozi Starving Crowd / Market Selection (4 Indicators)** (rode `Hormozi starving crowd market selection four indicators massive pain purchasing power`) → dor massiva + poder de compra.
- **Halbert Market-First Thinking / Product-Market Inversion** (rode `Halbert market-first thinking product-market inversion starving crowd`) + **Halbert RFU** (rode `Halbert RFU recency frequency unit of sale buyer evaluation`) → o mercado compra com frequência? o unit-of-sale sustenta AOV/recompra?
- **Schwartz 5 Levels of Product-Market Awareness** (rode `Schwartz five stages of awareness Unaware Problem Solution Product Most aware`) + **AI Deep-Research Market Awareness Prompt** (rode `deep research prompt market awareness TAM percentage distribution final selection`) → sub-passo 2.
- **Schwartz 5 Stages of Market Sophistication** (rode `Schwartz market sophistication 5 stages mechanism claims`) → sub-passo 3.
- **Two Forms of Differentiation (Mechanism vs Avatar Innovation)** (rode `two forms of differentiation mechanism innovation avatar innovation overlooked avatar`) → sub-passos 4 e 5.
- **Ries & Trout: Cherchez le Creneau (8 Holes in the Mind)** (rode `Ries Trout cherchez le creneau eight holes in the mind size price age`) + **Positioning Strategies** (rode `positioning strategies being first against the leader repositioning by attribute by user`) → sub-passo 5.
- **Brunson Market Depth Model** (rode `Brunson Expert Secrets market depth core market submarket niche three levels`) → define em que nível (core / submercado / nicho) a jogada entra.
- **Market Cyclicality** (rode `market cyclical 2-3 years markets retrace swipe file recycle past`) + **3 tipos de tendência** (rode `tendencia de conteudo consumo marketing criterio decisivo entrada nicho`) → cruza com a leitura do Trends (ETAPA 2).
- **Auditoria de Produto / 8-Figure Blueprint** (rode `auditoria de produto fraquezas forcas unico so contam forcas que o mercado valoriza`) → só contam forças que o mercado de fato valoriza.
- **Avatar Selection Matrix** (rode `avatar selection matrix desire magnitude competition level quick kill framework`) → sub-passo 5.

Aplique em sequência pra cada finalista:

**1. Magnitude do Desejo** — FRACO (organizar mesa) / MÉDIO (dormir melhor, mais energia) / FORTE (perder peso, dor crônica, envelhecimento, dinheiro, atração). Supplements quase sempre caem em MÉDIO-FORTE; documente qual instinto do LF8 o problema ataca.

**2. Market Awareness** — estime a distribuição do TAM pelos 5 níveis de Schwartz. A distribuição dita o funil: maioria Problem Aware → advertorial/listicle; Solution Aware → landing com mecanismo; Product Aware → PDP robusta; Most Aware → PDP enxuta. O tipo de LP mais escalada de cada marca (ETAPA 1) é a pista mais forte de onde o mercado está.

**3. Market Sophistication** — pelos claims que os finalistas usam: estágio 1-2 (claim direto ainda funciona), 3 (precisa de mecanismo nomeado), 4 (mecanismo saturou, precisa de informação nova/mecanismo expandido), 5 (identificação). Liste os claims e mecanismos **saturados** (os do pool com 3+ marcas) — são os que a jogada precisa evitar ou superar.

**4. Possibilidade de mecanismo por recombinação** — o filtro S.I.N. (Simple / Intuitive / New) sobre cada mecanismo candidato que sai da ETAPA 6: dá pra explicar em 1-2 frases? faz sentido imediato sem exigir fé? soa novo pro mercado (mesmo que a ciência seja antiga)? Mecanismo que nasce de elemento validado fica no topo da faixa que o S.I.N. der; mecanismo que só existiria por criação original **não entra** nesta skill.

**5. Avatar underserved** — todos os finalistas falam com o mesmo público? Existe segmento ignorado (45+, homens, quem usa GLP-1, atletas amadores, mães no pós-parto…)? O buraco de avatar é uma das duas formas de diferenciar — e é a mais barata, porque não muda o produto.

**6. Potencial de oferta** — dá pra montar stack (bundle + bump + upsell) que chegue em AOV ≥ $60 com folga? Tem produto complementar óbvio? O formato permite premium?

**7. Potencial criativo** — os ângulos abertos (do pool) rendem hooks? O produto/mecanismo é demonstrável em vídeo? UGC é viável?

### ETAPA 6 — Jogadas de recombinação (o que fazer diferente)

É a etapa que responde a pergunta do membro. Pra cada finalista (ou pra cada oportunidade que o pool revelar), monte **2-3 jogadas** usando os padrões abaixo. Toda jogada nomeia **cada elemento usado, de qual marca veio e com que evidência de escala** — jogada sem lastro de validação em alguma ponta não é jogada, é aposta.

**Os 4 padrões de recombinação:**

1. **Mesmo mecanismo validado (não saturado) + outro ângulo, formato de produto ou posicionamento.** Ex: a marca A escala "8-hour release magnesium" em cápsula pra insônia com ângulo de "wake up at 3am"; a jogada é o mesmo mecanismo em **pó pra mulheres 45+ na perimenopausa**, com ângulo de "hot flashes at night". O mecanismo já provou; o avatar e o formato são novos.
2. **Mecanismo do problema da marca A + mecanismo da solução da marca B (mesmo nicho).** Ex: A explica o problema como "gut lining damage" (e vende probiótico comum); B vende "butyrate" (com explicação fraca do problema). A jogada casa a explicação forte de A com o ativo validado de B — ninguém no mercado conta essa história inteira.
3. **Trocar o mecanismo mantendo o ângulo.** Ex: o ângulo "I tried every sleep supplement and nothing worked" escala pra marca A com melatonina (ingrediente em pico/saturado); a jogada mantém o ângulo e usa **um mecanismo validado por outra marca** (ex: glycine + apigenin, que a marca C escala com ângulo diferente). É a jogada certa quando o Trends mostra ingrediente em pico recente.
4. **Aprimorar um mecanismo validado** (o máximo de invenção permitido). Pegue um mecanismo que já escala e leve pro próximo nível de sophistication: mais específico (dose, forma, timing), mais crível (um elemento novo de explicação), mais completo (o passo que a marca original não explica). Mantém o ângulo que o mercado já compra. Ex: "magnesium glycinate" → "3-form magnesium timed for the 3 sleep phases".

**Regras duras:**

- **Nunca clonar**: mesma combinação de mecanismo + ângulo + formato + posicionamento de uma marca escalada = leilão contra quem já tem histórico. Se a jogada não muda pelo menos DUAS peças (ou aprimora o mecanismo de forma visível), não é jogada.
- **Nunca criar do zero**: mecanismo, formato ou ângulo que nenhuma marca escalada validou não entra. O máximo é o padrão 4.
- **Saturação respeitada**: elemento com 3+ marcas no mesmo ângulo só entra com ângulo/formato diferente ou aprimorado.
- **O Trends manda no ingrediente**: ingrediente em pico recente ou hype só entra via padrão 3 (troca) ou 4 (aprimoramento com timing/forma diferente).
- **A oferta faz parte da jogada**: toda jogada declara a estrutura de oferta (bundle/assinatura/upsell) que sustenta AOV ≥ $60 — e de qual marca essa estrutura foi validada.

Pra cada jogada, escreva em texto corrido (report_language) **por que ela tem potencial**: qual elemento carrega a validação, o que é novo, por que o mercado deve comprar a combinação, e o que a diferencia de cada finalista que usa peças parecidas. É esse texto que o membro lê pra decidir.

### ETAPA 7 — Ranking Final (eixos de score)

Inclua no topo do output desta etapa:

```
Ranking Generated at: YYYY-MM-DDTHH:MM:SSZ   (ISO-8601 UTC)
Formula:
  Total = (Magnitude × 2 + Sophistication × 2 + AwarenessFit + UMPotential + AvatarFit + OfferPotential + CreativePotential + TrendFit) / 10
  — Magnitude e Sophistication pesam 2× (filtros mais decisivos).
  — Todos os sub-scores são 1-10 inteiros ou com 1 casa.
  — Min aceitável pra TESTAR: ≥ 7.5. Min aceitável pra TALVEZ: 6.0-7.4. Abaixo de 6.0 → DESCARTA.
```

O objeto rankeado é a **oportunidade**: a marca finalista **com a sua melhor jogada** (ETAPA 6). Uma marca pode aparecer duas vezes se duas jogadas dela forem realmente distintas.

**Definição de cada sub-score (use literalmente):**

- **Magnitude** (ETAPA 5.1): FRACO = 2-3 · MÉDIO = 5-7 · FORTE = 8-10.
- **Sophistication** = FACILIDADE de diferenciação dado o estágio (sentido INVERTIDO): Stage 1-2 = 9-10 · Stage 3 = 6-7 · Stage 4 = 4-5 · Stage 5 = 2-3.
- **AwarenessFit** = quão bem o funil viável bate com a distribuição dominante (ETAPA 5.2) e o budget do membro: Most/Product Aware (PDP direta) = 8-10 · Solution Aware (landing com mecanismo) = 6-7 · Problem Aware (advertorial, TAM maior, conversão mais cara) = 4-6 · Unaware = 2-3.
- **UMPotential** = média S.I.N. (Simple / Intuitive / New, 1-10 cada) do mecanismo da jogada, **ajustado pelo padrão de recombinação**: padrão 1 ou 2 (duas pontas validadas) fica no topo da faixa; padrão 3 (troca) no meio; padrão 4 (aprimoramento) no topo se o aprimoramento for específico e demonstrável, senão no meio.
- **AvatarFit** = força do avatar underserved (ETAPA 5.5): segmento ignorado claro e alcançável = alto; todos já falam com o mesmo público sem brecha = baixo.
- **OfferPotential** = stack/bundle/bump e AOV projetado (ETAPA 5.6).
- **CreativePotential** = ângulos abertos + demonstrabilidade + viabilidade de UGC (ETAPA 5.7).
- **TrendFit** (cenário da ETAPA 2 → número): problema SUBINDO + ingrediente ESTÁVEL ou SUBINDO 6+ meses = 9-10 · ESTÁVEL + ESTÁVEL = 6 · problema SUBINDO + ingrediente em PICO RECENTE = 5 (a jogada precisa ser padrão 3 ou 4) · HYPE (subida vertical 1-3 meses) = 4 · QUEDA de 12+ meses em qualquer termo = a marca já foi eliminada antes do ranking.

Tabela do ranking:

| # | Marca (oportunidade) | Jogada recomendada | Magnitude | Awareness | Sophist. | UM | Avatar | Offer | Creative | Trend | **Total** | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Apresente o cálculo numericamente pra pelo menos o Top 3.

> **Cross-check do Top 3 com o sistema de validação final** (rode `final validation Gemini GPT Perplexity Kimi rank products scale potential unique mechanism`): o **AI Final-Validation Ranking** cruza potencial de escala × mecanismo único — use os critérios dele pra confirmar que a #1 tem escala E diferenciação, não só um dos dois.

> **Segundo cross-check — template de go/no-go** (rode `avaliar produto magnitude de desejo awareness 1 a 5 competition 1 a 5 go no go`): o **Product Evaluation Framework (Desire × Awareness × Sophistication)** em notas de 1 a 5. Rode pro Top 3; se o go/no-go divergir do veredicto, re-examine o score antes de cravar.

**Validação de mínimo (bloqueadora):** se NENHUMA oportunidade atingiu ≥ 6.0, **NÃO** declare "research completo". Liste por que cada uma falhou (o filtro ou score dominante), volte ao TrendTrack com o filtro de nicho ajustado (sub-nicho vizinho, ou o mesmo nicho com `Growth rank` em `last30d`) e repita a partir da ETAPA 0.5 até haver pelo menos 1 TESTAR — ou o membro optar por parar.

Pra CADA oportunidade do ranking:

**[Marca → Jogada] — Score: X.X/10 — Veredicto: TESTAR / TALVEZ / DESCARTAR**

- **O que fazer diferente** (a jogada em 2-4 frases, com os elementos e as marcas de origem)
- **Por que tem potencial** (o texto corrido da ETAPA 6)
- **3 riscos principais** (com o que fazer sobre cada um)
- **Nível de dificuldade**: FÁCIL / MÉDIO / DIFÍCIL (sophistication stage + budget do membro)

Veredicto: **TESTAR** ≥ 7.5 e sem eliminação em Trends/Trustpilot · **TALVEZ** 6.0-7.4 · **DESCARTAR** < 6.0.

### ETAPA 8 — Plano Preliminar pra Oportunidade #1

Pra oportunidade com maior score, entregue um plano inicial (detalhado depois nas skills 02-04):

**Mecanismo sugerido (da jogada):**
- Nome proprietário (2-4 palavras, memorável)
- Explicação em 2-3 frases (como funciona, por que diferente)
- Ingrediente/forma/processo base — e **de qual marca cada peça foi validada**

**Avatar principal sugerido:**
- Quem é (demografia rápida)
- Dor central (frase literal do Trustpilot/reviews, em inglês)
- Desejo central (frase literal)
- Trigger event típico (o que faz comprar AGORA)

**Estrutura de oferta preliminar** (validada pela estrutura das marcas do pool):
- Produto base: $X
- Bundle: 2-pack / 3-pack com savings
- Assinatura: sim/não e %
- Bump / upsell sugeridos
- Garantia (tipo + duração)
- AOV projetado

**3 hooks de criativo (ângulos abertos no pool — em inglês US):**
- Hook 1: [texto + tipo de criativo]
- Hook 2: [texto + tipo]
- Hook 3: [texto + tipo]

**Sourcing:** se a jogada usa fórmula validada por outra marca, o caminho mais curto costuma ser fórmula pronta / white label — a Skill 01b fecha o custo real.

## SALVAR

**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/01-product-research/`.

`[produto]` = slug da **oportunidade vencedora** (não o placeholder do setup) — assim as fases seguintes salvam no mesmo lugar.

### 1. Banco de marcas — Notion (caminho preferido) ou HTML

**Se há Notion MCP** (escolha `notion` na ETAPA 0):

1. Crie uma página-mãe privada: `Aura — Product Research — [nicho] — [YYYY-MM-DD]` (tool de criar página; sem parent nomeado, cria como página privada do membro — diga isso a ele e ofereça mover).
2. Dentro dela, crie o **banco de dados de marcas** (tool de criar database, parent = a página-mãe) com estas propriedades:

   ```
   CREATE TABLE (
     "Marca" TITLE,
     "Site" URL,
     "Status" SELECT('Pré-selecionada':gray, 'Finalista':green, 'Eliminada':red),
     "Ranking" NUMBER,
     "Score" NUMBER,
     "Veredicto" SELECT('TESTAR':green, 'TALVEZ':yellow, 'DESCARTAR':red),
     "Nicho" RICH_TEXT,
     "Produto" RICH_TEXT,
     "Formato do produto" RICH_TEXT,
     "Preço base" NUMBER FORMAT 'dollar',
     "AOV estimado" NUMBER FORMAT 'dollar',
     "Visitas/mês" NUMBER,
     "LP mais escalada" URL,
     "Tipo de LP" SELECT('Advertorial':blue, 'Listicle':blue, 'PDP':gray, 'Landing dedicada':purple, 'Quiz':orange),
     "Ads mais escalados" RICH_TEXT,
     "Dias no ar (ad mais antigo)" NUMBER,
     "Formato de criativo" SELECT('Imagem native':blue, 'Vídeo UGC':purple, 'Vídeo talking head':purple, 'Demo':gray, 'Misto':gray),
     "Mecanismo do problema" RICH_TEXT,
     "Mecanismo da solução" RICH_TEXT,
     "Ingrediente / ativo" RICH_TEXT,
     "Ângulo principal" RICH_TEXT,
     "Avatar" RICH_TEXT,
     "Trustpilot" URL,
     "Trustpilot nota" NUMBER,
     "Trustpilot reviews" NUMBER,
     "Trustpilot veredito" SELECT('OK':green, 'Cobrança/entrega':yellow, 'Eficácia — eliminar':red, 'Sem fonte':gray),
     "Trends problema" SELECT('Subindo':green, 'Estável':gray, 'Pico recente':yellow, 'Hype':orange, 'Queda':red),
     "Trends ingrediente" SELECT('Subindo':green, 'Estável':gray, 'Pico recente':yellow, 'Hype':orange, 'Queda':red),
     "Cenário" RICH_TEXT,
     "O que fazer diferente" RICH_TEXT,
     "Fonte" SELECT('TrendTrack MCP':blue, 'Manual':gray),
     "Pesquisado em" DATE
   )
   ```

3. **Uma página por marca** no banco (tool de criar páginas, parent = data source do banco). Propriedades preenchidas + **conteúdo da página** com a ficha completa: tabela dos ads mais escalados (link do ad, link da mídia, dias no ar, duplicatas, formato, hook, ângulo), leitura da LP (headline, promessa, mecanismos, prova, estrutura de oferta com a conta do AOV), leitura do Trends (os dois termos + cenário), Trustpilot (mix de temas + 5-10 frases literais com tradução livre), decomposição em elementos (ETAPA 4) e as jogadas da marca (ETAPA 6, com o texto de "por que tem potencial"). Texto integral — nunca truncar.
4. **Uma página de síntese** dentro da página-mãe: `Ranking e recomendação` — a tabela do ranking (ETAPA 7), o pool de elementos validados (ETAPA 4), as jogadas rankeadas com o "por que" e o plano preliminar da #1 (ETAPA 8).
5. Grave a URL da página-mãe em `manifest.product_research.notion_url` e cite na mensagem final.

Vá criando as páginas de marca **conforme fecha cada ficha** (ETAPA 1), e atualize Status/Score/Veredicto no fim. Se uma chamada do Notion falhar (auth, rate limit), salve o restante em HTML (abaixo) e avise em 1 linha.

**Se NÃO há Notion** (escolha `html`): salve `01-product-research/banco-de-marcas.html` — um HTML self-contained no design system `.claude/templates/aura-report-template.html` (copiar `<style>` + topbar com a logo SVG, NUNCA texto no lugar da logo), com **um card/seção por marca** contendo exatamente a mesma ficha completa descrita no item 3 (links clicáveis dos ads, mídia, LP e Trustpilot) e, no topo, a tabela-resumo de todas as marcas (status, score, veredicto, visitas, AOV, cenário, veredito Trustpilot, jogada). Texto integral, nunca truncar.

**Nos dois casos**, salve também `01-product-research/banco-de-marcas.md` — a mesma ficha por marca em markdown. É o arquivo que as Skills 02 e 03 leem (concorrentes já identificados, VOC de review, mecanismos e ângulos validados).

### 2. Relatório da pesquisa (dual output — rule 6b)

1. **`01-product-research/product-research.md`** (a AI lê nas fases seguintes)
2. **`01-product-research/product-research.html`** (visualização humana — `.claude/templates/aura-report-template.html`, self-contained, logo SVG copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html`)

Conteúdo (na ordem — ficha primeiro, detalhe depois):
1. **Resumo de 1 página**: a oportunidade #1 (marca-base → jogada), o mecanismo sugerido, por que funciona, o maior concorrente na mesma faixa, o score e os 3 riscos
2. Ranking completo (ETAPA 7) com timestamp e fórmula explícita
3. As jogadas de cada finalista com o "por que tem potencial" (ETAPA 6)
4. Pool de elementos validados, com contagem de marcas e saturação (ETAPA 4)
5. Análise estratégica dos finalistas (ETAPA 5)
6. Resultados de Trends e Trustpilot por marca, incluindo as eliminadas com o motivo (ETAPAS 2-3)
7. Plano preliminar da #1 (ETAPA 8)
8. Lista completa das marcas pré-selecionadas (link pro banco de marcas no Notion ou pro `banco-de-marcas.html`)

O doc segue `.claude/rules/report-only-results.md`: só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa. Dado que veio colado pelo membro entra como dado, sem marcação.

### 3. `01-product-research/dados.json` (AI-only, lido por 02/03/04)

```json
{
  "generated_at": "ISO-8601 UTC",
  "niche": "health & supplements",
  "source": "trendtrack_mcp | manual | mixed",
  "notion_url": "https://... | null",
  "filters_used": { "image": { }, "video": { } },
  "brands": [
    {
      "brand": "...", "domain": "...", "monthly_visits": 0, "niche": "...", "product": "...", "format": "...",
      "price_base": 0, "aov_estimated": 0, "offer_structure": { "bundles": [], "subscription_pct": 0, "bump": "...", "upsell": "...", "guarantee": "..." },
      "lp_url": "...", "lp_type": "advertorial|listicle|pdp|landing|quiz",
      "top_ads": [ { "url": "...", "media_url": "...", "days_running": 0, "ad_rank": 0, "duplicates": 0, "format": "image|video", "hook": "...", "angle": "..." } ],
      "creative_format": "...", "problem_mechanism": "...", "solution_mechanism": "...", "ingredient": "...", "angle": "...", "avatar": "...",
      "trustpilot": { "url": "...", "rating": 0, "reviews": 0, "complaint_mix": { "billing": 0, "delivery": 0, "support": 0, "efficacy": 0 }, "verdict": "ok|billing_delivery|efficacy_eliminate|no_source", "quotes": ["..."] },
      "trends": { "problem_term": "...", "problem_class": "rising|flat|recent_peak|hype|decline", "ingredient_term": "...", "ingredient_class": "...", "scenario": "..." },
      "status": "pre_selected|finalist|eliminated", "elimination_reason": "... | null"
    }
  ],
  "validated_elements": [
    { "type": "problem_mechanism|solution_mechanism|angle|product_format|positioning|creative_format|offer_structure", "name": "...", "brands": ["..."], "evidence": "...", "saturation": "open|saturated" }
  ],
  "plays": [
    { "id": "play-01", "base_brand": "...", "pattern": 1, "description": "...", "elements": [ { "type": "...", "name": "...", "from_brand": "...", "evidence": "..." } ], "why_it_wins": "...", "offer_structure": "..." }
  ],
  "ranking": [ { "rank": 1, "brand": "...", "play_id": "play-01", "scores": { "magnitude": 0, "sophistication": 0, "awareness_fit": 0, "um_potential": 0, "avatar_fit": 0, "offer_potential": 0, "creative_potential": 0, "trend_fit": 0 }, "total": 0, "verdict": "TESTAR|TALVEZ|DESCARTAR" } ],
  "winner": { "brand": "...", "play_id": "...", "mechanism_name": "...", "avatar": "...", "offer": { }, "hooks": ["..."] }
}
```

### 4. `manifest.json` (fonte única de verdade)

1. Se o `product_slug` do vencedor for diferente do slug temporário do setup: `mkdir -p workspace/[novo-slug]/`, mova o manifest, atualize `product_slug` e `product_name`.
2. Adicione `"01-product-research"` a `skills_completed` (sem duplicar).
3. Atualize `updated_at` (ISO-8601 UTC).
4. Grave (PRELIMINARES — a Skill 02 refina): `product_vertical`, `awareness_distribution` (`{unaware, problem, solution, product, most}`), `sophistication_stage` (1-5), e o bloco `product_research: { "source": "trendtrack_mcp|manual|mixed", "notion_url": "...|null", "winner_play_id": "play-01", "base_brands": ["..."] }`.
5. Preserve todos os campos do setup (`budget_tier`, `budget_daily`, etc.).
6. Regenere o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>`.

### 5. Naming da marca — nome chiclete (antes do brand.md)

As marcas que mais vendem têm nome chiclete: gruda na primeira vez que a pessoa ouve e está amarrado ao conceito central (o problema, o momento, o mecanismo, a tribo). Frameworks (puxar pela `best_query` do kb-index): **Ries & Trout Naming as Positioning** (rode `Ries Trout name is the position own a word mind works by ear line extension`); **Hopkins Naming Strategy Hierarchy** (rode `Hopkins naming hierarchy coined personal names substitution warning frivolous`); **Proprietary Mechanism Naming (Gum Name)** (rode `proprietary mechanism gum name nickname ritual hack effect`); **Big Idea** (rode `Big Idea paradoxical question gum name conspiracy story`).

- Gere 3-5 candidatos e recomende 1, com a lógica de cada um. O melhor é o que gera VOCABULÁRIO próprio (verbo de campanha, status de cliente, apelido de mecanismo).
- Os nomes são **sugestão** — o membro decide. Domínio ocupado se resolve com variação; registro de marca vem depois da validação com vendas, não antes.
- Grave o nome escolhido (e o vocabulário que ele gera) no `brand.md`.

### 6. `brand.md` do vencedor

Se ainda não existir `workspace/[produto]/brand.md`: copie `.claude/templates/brand.md.template`, preencha `{{ PRODUCT_SLUG }}`, posicionamento preliminar (1 frase, da jogada vencedora), atributos de tom sugeridos pelo avatar, e "o que NUNCA dizer" (claims e mecanismos saturados do pool). Paleta, tipografia e logo ficam como `[preencher]` — a 07a lê e só pergunta o que faltar.

Se o slug mudou, informe: `"Oportunidade vencedora: [marca-base → jogada]. Movi os artefatos para workspace/[novo-slug]/."`

## Mensagem Final

Se houver TESTAR no ranking:

"Product research completo. A oportunidade #1 é **[jogada]** (base: [marca], score X.X/10) — [1 frase do que fazer diferente].

Banco de marcas: [link do Notion | `workspace/[produto]/01-product-research/banco-de-marcas.html`] — [N] marcas pré-selecionadas, [M] finalistas, [K] eliminadas (Trends/Trustpilot). Relatório em `workspace/[produto]/01-product-research/product-research.md`.

Próximo passo: diga **'market research'** pra aprofundar no avatar e montar o Unified Research Brief. Se a jogada usa fórmula que outra marca já valida, diga **'sourcing'** — a 01b fecha o custo real (fórmula pronta / white label) em paralelo à pesquisa."

Se NENHUMA oportunidade passou:

"Nenhuma oportunidade dessa leva passou. Os bloqueios foram: [Trends em queda / eficácia no Trustpilot / mercado em estágio 5 sem avatar aberto / AOV sem sustentação].

Vale rodar outra leva: [sub-nicho vizinho sugerido a partir do pool] ou o mesmo nicho com a janela de `Growth rank` em 30 dias. Me diz o nicho e eu rodo de novo — ou aplica os filtros no TrendTrack e me cola as marcas."
