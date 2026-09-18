# Product Research · Referência: Motor de descoberta, TrendTrack por MCP ou manual (ETAPA 0.5)

> Os dois conjuntos de filtros fixos (native ads em imagem e em vídeo) com o porquê de cada filtro, o caminho A pelo MCP (créditos, id do nicho, mapeamento filtro a param, paginação, fallback) e o caminho B manual com a mensagem ao membro, os critérios de pré-seleção e a saída da etapa. Abra na ETAPA 0.5.

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
- **O produto faz sentido** pro membro — ele conhece o nicho, consegue sourcing (fórmula pronta / white label na `sourcing`), e o problema é real e recorrente (consumível = recompra).

Saída desta etapa: **lista de 15-25 marcas pré-selecionadas**, cada uma com domínio + ads + LP + tráfego + Trustpilot. Todas seguem pra ETAPA 1.
