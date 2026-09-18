---
name: product-research
description: Engine de pesquisa de produto por recombinação de elementos validados. Descobre marcas DTC que já escalam no nicho de health & supplements pelo TrendTrack (MCP ou manual, com dois conjuntos de filtros fixos, native ads em imagem e em vídeo), monta a ficha completa de cada marca (LP e ads mais escalados, tráfego, oferta, mecanismos, ângulo, avatar), valida com o Google Trends (problema e ingrediente, 5 anos, US) e com as reviews de 1 e 2 estrelas do Trustpilot, decompõe cada finalista em elementos validados, monta jogadas de recombinação pelos 4 padrões (nunca clonar, nunca criar do zero), rankeia pelos eixos de score com veredicto TESTAR, TALVEZ ou DESCARTAR, entrega o plano preliminar da oportunidade número 1 e salva o banco de marcas no Notion ou em HTML na pasta do produto. Use quando o membro disser "product research", "pesquisa de produto", "encontrar produto", "qual produto vender", ou quando estiver na situação A do setup (não tem produto).
---

# Product Research · Passo 2 · apelido antigo: 01 <!-- gen:title -->

## Quando usar

Quando o membro ainda não tem produto ou quer encontrar o próximo. A skill responde uma pergunta só: qual combinação de elementos que o mercado já provou (mecanismo, ângulo, formato do produto, posicionamento, oferta) dá pra montar de um jeito que nenhum concorrente escalado usa, sem clonar ninguém e sem inventar do zero. Recombinar é o meio do caminho entre clonar e criar do zero; o máximo de invenção permitido é aprimorar um mecanismo que já escala (tese em `reference/contexto.md`).

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/profile.md`; ausente, oferecer rodar o `setup` inline.
2. `manifest.json` com `setup_complete === true`; mais de um produto = perguntar qual em 1 linha; ausente, `setup` inline. O `product_slug` é o path de salvamento até o vencedor ser escolhido.
3. `setup` em `skills_completed`; senão, re-rode o setup.
4. Nicho: default health & supplements (o dos filtros fixos da ETAPA 0.5); outro nicho troca só o filtro de nicho.
5. Destino do banco de marcas: com tools de Notion na sessão (qualquer prefixo com `notion`), Notion; sem elas, pergunte uma vez, em 1 linha, se conecta o Notion MCP ou prefere HTML na pasta do produto; grave `notion` ou `html` e siga (a pesquisa não espera o Notion).

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`); todo output interno, inclusive páginas do Notion, nesse idioma; copy consumidor-final (hooks, headlines) e VOC literal sempre em inglês US.
2. `workspace/profile.md`: budget diário, ferramentas conectadas (TrendTrack, Notion) e nicho de interesse, se declarado.
3. Base pelo índice (domínio `product-research`): `python3 .claude/lib/kb-index/kb_lookup.py --skill product-research --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa; as queries embutidas nos arquivos de `reference/` (ETAPAS 5 e 7 e o naming) são piso obrigatório, rodam sempre e não contam no teto; sistemas completos, não resumos; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 0 · Pré-flight

É a checklist acima; o texto integral está em `reference/contexto.md`.

### ETAPA 0.5 · Motor de descoberta, TrendTrack (MCP ou manual)

Leia `reference/descoberta-trendtrack.md`. Fonte: TrendTrack, Explorer, Meta Ads, com os dois conjuntos de filtros fixos do arquivo (native ads em imagem, com copy longa, e em vídeo). Caminho A, MCP (gasta créditos): cheque os créditos e diga quanto a pesquisa gasta, resolva o id do nicho, rode as duas pesquisas com o mapeamento filtro a param da tabela (`sort_by` sempre, senão volta vazio pra ads só US; alcance zero não é gasto zero), pagine até 15 a 25 marcas distintas anotando por ad os campos do arquivo; chamada que falhar cai pro manual. Caminho B, manual: o membro aplica os filtros no browser e cola, por marca, os itens da mensagem do arquivo (nunca fingir que abriu o TrendTrack). Pré-seleção nos dois caminhos: DTC com loja própria, AOV de 60 dólares ou mais contando a oferta inteira, produto que faz sentido pro membro. Saída: 15 a 25 marcas pré-selecionadas.

### ETAPA 1 · Ficha por marca (coleta profunda)

Leia `reference/ficha-por-marca.md`. Com MCP, 2 a 3 chamadas por marca: ads mais escalados por domínio (top 3 a 5), LP mais escalada (a URL com mais ads ativos), dados da loja e, quando o hook não está claro, a decomposição de 1 ad. Manual: o membro cola os mesmos itens. Leitura da LP pela cascade resiliente (`WebFetch`, depois o fetcher em `--mode text`, depois print do membro): os nove itens do arquivo (tipo de página, promessa, os dois mecanismos, ângulo, avatar, formato, oferta com o AOV estimado, prova). Preencha os campos obrigatórios da tabela e salve cada ficha assim que fechar (Notion ou `banco-de-marcas.md`). Dispare o lote do Trends em segundo plano já aqui.

### ETAPA 2 · Checagem 1, Google Trends (5 anos, US)

Leia `reference/trends.md`. Dois termos por marca, o problema e o ingrediente ou mecanismo, em lote pelo `trends_batch.py` em segundo plano (o lote contorna o bloqueio do endpoint); termo avulso pelo fetcher em `--mode trends`; nunca renderizar o site do Trends; termo que ficar bloqueado vai pro membro por print. Regra de eliminação: queda constante por 12 meses ou mais, no problema ou no ingrediente. Leitura conjunta: problema subindo com ingrediente estável é o melhor cenário; ingrediente subindo há 6 meses ou mais é ótimo; problema subindo com ingrediente em pico recente é tarde (trocar o mecanismo, padrão 3 da ETAPA 6); subida vertical em 1 a 3 meses é hype (rebaixa o score). Classifique cada termo (QUEDA, ESTÁVEL, SUBINDO, PICO RECENTE, HYPE) e grave o cenário na ficha.

### ETAPA 3 · Checagem 2, Trustpilot (reviews de 1 e 2 estrelas)

Leia `reference/trustpilot.md`. URL filtrada em 1 e 2 estrelas por recência, pela cascade (`WebFetch`, fetcher em `--mode reviews`, paste do membro); no mínimo 20 a 30 reviews negativas por marca, classificadas em cobrança e assinatura, entrega, atendimento e eficácia. Veredito: cobrança e entrega passam (e viram ângulo); nota abaixo de 4 sem eficácia passa; maioria falando de eficácia elimina; nota abaixo de 4 com muita gente dizendo que não funciona elimina (a marca escala em cima de churn). Grave na ficha os campos do arquivo, com 5 a 10 frases literais em inglês (tradução livre ao lado em pt-BR). Sem Trustpilot: Amazon, Reddit e comentários dos ads; sem fonte, veredito em aberto. Ao fim das ETAPAS 2 e 3 sobram os finalistas (alvo: 8 a 12 marcas); eliminada fica no banco com status e motivo.

### ETAPA 4 · Decomposição em elementos validados

Leia `reference/elementos-validados.md`. Quebre cada finalista nos sete elementos da tabela, com a evidência de validação ao lado, e consolide o pool cruzado contando em quantas marcas escaladas cada elemento aparece: em 1 ou 2 marcas é validado e aberto; em 3 ou mais no mesmo ângulo é validado e saturado (só entra com outro ângulo, formato ou aprimorado); em nenhuma é não validado e não entra. O pool é `validated_elements[]` do `dados.json` e a semente da `validated_library` da `competitor-analysis`.

### ETAPA 5 · Análise estratégica (frameworks da base)

Leia `reference/analise-estrategica.md` e puxe os sistemas nomeados pela query exata antes de raciocinar. Aplique em sequência a cada finalista os sete sub-passos: magnitude do desejo (com o instinto do LF8), awareness (distribuição do TAM pelos 5 níveis; a LP mais escalada é a pista mais forte), sofisticação (claims e mecanismos saturados do pool), possibilidade de mecanismo por recombinação (nota fechada na ETAPA 7 pelo S.I.N.), avatar underserved, potencial de oferta (AOV de 60 dólares ou mais com folga) e potencial criativo.

### ETAPA 6 · Jogadas de recombinação (o que fazer diferente)

Leia `reference/jogadas-de-recombinacao.md`. Pra cada finalista ou oportunidade do pool, 2 a 3 jogadas pelos 4 padrões: mecanismo validado e não saturado com outro ângulo, formato ou posicionamento; mecanismo do problema de A com mecanismo da solução de B; trocar o mecanismo mantendo o ângulo (quando o Trends mostra pico recente); aprimorar um mecanismo validado. Regras duras: nunca clonar (a jogada muda pelo menos duas peças ou aprimora de forma visível), nunca criar do zero, saturação respeitada, o Trends manda no ingrediente, a oferta faz parte da jogada com a marca que a validou. Filtro S.I.N. (Simple, Intuitive, New) em cada mecanismo candidato. Cada jogada nomeia cada elemento, de qual marca veio e com que evidência, e ganha o texto de "por que tem potencial".

### ETAPA 7 · Ranking final (eixos de score)

Leia `reference/ranking.md`. Topo do output com o timestamp ISO-8601 UTC e a fórmula do arquivo (oito sub-scores de 1 a 10; Magnitude e Sophistication pesam o dobro). O objeto rankeado é a oportunidade (marca com a sua melhor jogada). Use as definições literais de cada sub-score do arquivo. Tabela do ranking, cálculo numérico pro Top 3, os dois cross-checks pela query exata e a validação de mínimo: sem oportunidade em 6.0 ou mais, não declare research completo; ajuste o filtro de nicho e repita da ETAPA 0.5. Por oportunidade: o que fazer diferente, por que tem potencial, 3 riscos com o que fazer, dificuldade. Veredicto: TESTAR em 7.5 ou mais sem eliminação, TALVEZ entre 6.0 e 7.4, DESCARTAR abaixo de 6.0.

### ETAPA 8 · Plano preliminar pra oportunidade número 1

Leia `reference/plano-preliminar.md`. Mecanismo sugerido (nome proprietário, explicação, ingrediente ou forma com a marca que validou cada peça), avatar principal (quem, dor e desejo em frase literal em inglês, trigger event), estrutura de oferta preliminar validada pelo pool, 3 hooks em inglês US nos ângulos abertos e o ponteiro de sourcing (fórmula pronta ou white label pela `sourcing`).

## SALVAR

`mkdir -p workspace/[produto]/product-research/`, com `[produto]` = slug da oportunidade vencedora. Seis entregas, na ordem. (1) Banco de marcas, `reference/banco-de-marcas.md`: no Notion, página-mãe, banco de dados com as propriedades do arquivo, uma página por marca com a ficha integral (nunca truncar) e a página de síntese, URL no manifest; sem Notion, `banco-de-marcas.md` mais o `.html` por `python3 tools/render_report.py`; nos dois casos o `banco-de-marcas.md` existe, porque a `market-research` e a `competitor-analysis` o leem. (2) `product-research.md` e `.html` pelo mesmo script, na ordem de `reference/relatorio-e-manifest.md` (ficha de 1 página da oportunidade número 1 primeiro, detalhe depois); só o resultado no doc. (3) `dados.json` no schema de `reference/dados-json.md`. (4) Manifest pelo script (mesmo arquivo): slug novo por `python3 tools/manifest.py <novo-slug> set`, depois `complete product-research`, os preliminares e o bloco `product_research` por `set`, e `python3 .claude/lib/workspace-index/build_index.py <slug>`. (5) Naming da marca, `reference/naming-e-brand.md`: 3 a 5 candidatos de nome chiclete pelos quatro frameworks (query exata), 1 recomendado, sempre como sugestão. (6) `brand.md` do vencedor a partir de `.claude/templates/brand.md.template`, com posicionamento preliminar, tom e "o que nunca dizer"; visual como `[preencher]`. Se o slug mudou, informe que os artefatos foram movidos.

## Mensagem final

Íntegra em `reference/mensagem-final.md`. Com TESTAR: a oportunidade número 1 com score e a frase do que fazer diferente, o banco de marcas com as contagens, o relatório, e os próximos passos 'market research' e, se a jogada usa fórmula validada, 'sourcing' em paralelo. Sem oportunidade aprovada: os bloqueios e a sugestão de outra leva.
