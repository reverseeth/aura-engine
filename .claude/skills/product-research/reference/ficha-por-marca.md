# Product Research · Referência: Ficha por marca, a coleta profunda (ETAPA 1)

> As chamadas por marca com MCP (ads mais escalados, LP mais escalada, loja, decomposição de um ad), o caminho manual, a leitura da LP pela cascade resiliente com os nove itens a extrair e a tabela dos campos obrigatórios da ficha. Abra na ETAPA 1.

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
