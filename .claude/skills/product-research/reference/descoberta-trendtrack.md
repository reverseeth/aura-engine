# Product Research · Referência: Motor de descoberta, TrendTrack por MCP ou manual (ETAPA 0.5)

> O filtro fixo da Aura (um conjunto só, imagem e vídeo juntos) com o porquê de cada filtro, o caminho A pelo MCP (créditos, ids dos nichos, mapeamento filtro a param, paginação, fallback) e o caminho B manual com a mensagem ao membro, os critérios de pré-seleção e a saída da etapa. Abra na ETAPA 0.5.

### ETAPA 0.5 — Motor de descoberta: TrendTrack (MCP ou manual)

A fonte de descoberta é o **TrendTrack — Explorer → Meta Ads**, com um conjunto fixo de filtros. O objetivo é achar marcas DTC que estão escalando agora nos nichos de beleza e saúde, pelos anúncios que já provaram que vendem.

**Filtro fixo da Aura:**

```
Monthly traffic: min 200k
Status: active
Days Running: min 14, max 60
Language: english
Niche: beauty & care + health & supplements
Ad rank: top 5%
Growth rank: rising
Active ads: min 200
Ad countries: US, Canada, Australia, UK
Sort by: ad rank
```

Por que esses filtros: `Days Running` entre 14 e 60 isola o anúncio que já sobreviveu duas semanas de teste e ainda é recente (a marca está escalando agora, não deixando um criativo velho no automático); `Ad rank top 5%` + `Growth rank rising` pega só o topo que ainda está subindo; `Active ads ≥ 200` na página garante marca que testa e escala em volume; `Monthly traffic ≥ 200k` garante loja com escala real; os quatro países de língua inglesa (os "Big 4") são os mercados que a Aura mira.

**Caminho A — MCP do TrendTrack (gasta créditos do membro):**

Verifique se há tools com prefixo `mcp__trendtrack__` na sessão. Se SIM:

1. **Rode a tool de créditos primeiro** (intenção *Account → créditos*, hoje `check_credits`) e diga ao membro em 1 linha quanto tem e quanto a pesquisa deve gastar (descoberta: 3-6 chamadas; ficha por marca: 2-3 chamadas × número de marcas pré-selecionadas). Se o saldo não cobre, rode a descoberta por MCP e faça a ficha por marca pelo caminho manual — ou tudo manual, o membro decide.
2. **Resolva os ids dos nichos** (intenção *lookup de filtros*, hoje `lookup_filter_ids` com `type: "categories"`, uma consulta por termo: `"beauty"`, `"personal care"`, `"health"`, `"supplement"`; pegue os ids que casam com beauty & care e health & supplements e passe todos juntos).
3. **Rode a pesquisa** (intenção *Discover → ads em lote*, hoje `search_ads`). Mapeamento dos filtros da UI pros params da tool (NÃO invente params — se um filtro não existir na versão da tool, aplique-o você mesmo na leitura dos resultados):

   | Filtro da UI | Param da tool (hoje) |
   |---|---|
   | Monthly traffic ≥ 200k | `min_traffic: 200000` |
   | Status: active | `status: "active"` |
   | Days Running 14 a 60 | `min_days_running: 14`, `max_days_running: 60` |
   | Language: english | `ad_languages: ["en"]` |
   | Niche | `category_ids: [<ids do passo 2>]` |
   | Ad rank: top 5% | `ad_rank_mode: "percentile"`, `max_ad_rank_value: 5` |
   | Growth rank: rising | `growth_rank: [{ "period": "last7d", "direction": "rising" }]` (se vier pouco resultado, `last30d`) |
   | Active ads ≥ 200 | `min_active_ads: 200` |
   | Ad countries: US, CA, AU, UK | `ad_countries: { "include": ["US", "CA", "AU", "GB"] }` |
   | Sort by ad rank | `sort_by: "adOrder"` (segunda passada, se precisar de volume: `sort_by: "longestRunning"`) |
   | (diversidade) | `max_ads_per_brand: 2`, `limit: 20`, `page: 1, 2, 3` |

   Passe `sort_by` SEMPRE — sem ele a tool aplica por default um filtro de alcance que só existe pra ads da União Europeia e devolve zero pra ads só-US. Se mesmo assim a resposta vier vazia ou magra, adicione `trend_signal: "relevance"`. **Regra de leitura:** o alcance publicado pela Meta só existe pra ads veiculados na UE — ad só-US aparece com alcance 0 sem significar gasto zero. Escala se lê por **dias no ar + duplicatas + ad rank + tráfego da loja**.
4. Pagine até juntar **15-25 marcas distintas** (uma marca com vários anúncios conta uma vez). Anote por ad: marca, domínio, link do ad (Ad Library / TrendTrack), URL de mídia (Media URL, senão Thumbnail URL), dias no ar, ad rank, duplicatas, tráfego mensal da loja, LP de destino.
5. Se uma chamada falhar (auth expirou, rate limit, créditos acabaram), caia pro caminho manual sem drama — diga ao membro exatamente o que fazer (abaixo) e continue de onde parou.

**Caminho B — manual (membro usa o TrendTrack no browser):**

Se não há MCP, ou os créditos acabaram, ou o membro prefere olhar com os próprios olhos:

> "Abre o TrendTrack → **Explorer → Meta Ads**. Aplica os filtros abaixo (o filtro fixo da Aura, imagem e vídeo juntos). Ordena por **ad rank**. Vai abrindo os ads e, pra cada marca que fizer sentido, me manda:
>
> 1. Nome da marca + site
> 2. Link do ad (o link do TrendTrack ou do Ad Library) — os 2-3 ads de melhor ad rank da marca
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
