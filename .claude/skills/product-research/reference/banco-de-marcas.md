# Product Research · Referência: SALVAR, o banco de marcas no Notion ou em HTML

> O diretório e o slug do vencedor, a página-mãe e o banco de dados do Notion com todas as propriedades, a página por marca com a ficha integral, a página de síntese, a URL no manifest, o fallback em HTML pelo `render_report.py` e o `banco-de-marcas.md` que as fases seguintes leem. Abra ao começar a salvar.

## SALVAR

**Antes de qualquer write**, garanta: `mkdir -p workspace/[produto]/product-research/`.

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

**Se NÃO há Notion** (escolha `html`): salve `product-research/banco-de-marcas.html` gerando-o com `python3 tools/render_report.py workspace/[produto]/product-research/banco-de-marcas.md` (o `.md` do parágrafo seguinte é a fonte; nunca escreva o HTML à mão). No `.md`: no topo, a tabela-resumo de todas as marcas (status, score, veredicto, visitas, AOV, cenário, veredito Trustpilot, jogada) e, depois, **uma seção `##` por marca** com exatamente a mesma ficha completa descrita no item 3 (links clicáveis dos ads, mídia, LP e Trustpilot). Texto integral, nunca truncar.

**Nos dois casos**, salve também `product-research/banco-de-marcas.md` — a mesma ficha por marca em markdown. É o arquivo que as Skills `market-research` e `competitor-analysis` leem (concorrentes já identificados, VOC de review, mecanismos e ângulos validados).
