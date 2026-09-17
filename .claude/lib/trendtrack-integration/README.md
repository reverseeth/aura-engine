# TrendTrack Integration (opcional)

Integração com TrendTrack MCP. Read-only, OAuth 2.1, ~24h refresh. É o **motor de descoberta da Skill 01** e substitui scraping manual + Meta Ad Library público em várias outras skills quando o membro tem assinatura TrendTrack.

## Quando usar

Membro tem TrendTrack pago E conectou via MCP. Detecção automática: se tools com prefixo `mcp__trendtrack__` existirem na sessão, usar; senão, fallback pro método da skill (na 01, o membro aplica os mesmos filtros no browser do TrendTrack e cola o resultado; nas demais, Meta Ad Library público + scraping).

**Default = não-integrado.** Aura Engine funciona sem TrendTrack MCP. Integração é upside, não dependência.

## Como o membro conecta

Tutorial completo em `docs/aura-setup-pt.html` (passo opcional na seção Aura Engine). Fluxo:

1. Claude Desktop ou Code → Settings → Connectors → Add custom connector
2. URL: `https://api.trendtrack.io/v1/mcp`
3. OAuth → login TrendTrack → aprovar os scopes read-only
4. As tools aparecem automaticamente (30+ hoje)

## Créditos

O MCP gasta créditos do plano do membro por chamada. Regra em toda skill que usa TrendTrack: **rodar a tool de créditos primeiro** (intenção *Account → créditos*, hoje `check_credits`), dizer ao membro em 1 linha quanto tem e quanto a skill deve gastar, e cair pro caminho manual (membro usa o TrendTrack no browser) quando o saldo não cobre ou acaba no meio. Estimativas de uso por skill:

- **01 product research**: descoberta 4-8 chamadas (2 pesquisas × 2-3 páginas + lookup de nicho) + ficha por marca 2-3 chamadas × 15-25 marcas.
- **03 competitor analysis**: 1-2 chamadas por concorrente (brief + ads em lote).
- **08 / 11 / 13**: 1-3 chamadas por rodada.

## Runtime-discovery: NÃO assuma nomes de tool fixos

> **Regra central desta integração.** A lista de tools `mcp__trendtrack__*` **muda entre versões do MCP** — nomes podem ser renomeados, somados ou removidos. Por isso **nenhuma skill assume nomes de tool hard-coded**. Em vez disso, cada skill:
>
> 1. **Descobre em runtime** quais tools `mcp__trendtrack__*` realmente existem na sessão.
> 2. **Casa por INTENÇÃO/categoria, não por nome literal.**
> 3. **Passa filtros só via params que a tool expõe** (não inventa params). Se a tool não suporta um filtro, a skill aplica esse filtro depois, na leitura dos resultados.
> 4. Se **nenhuma** tool casa com a intenção necessária, trata como TrendTrack ausente pra aquela etapa e cai no fallback.

A tabela abaixo lista as tools que o TrendTrack expõe HOJE (referência, não contrato).

## Tools disponíveis hoje (referência — pode mudar)

| Tool (hoje) | Intenção / categoria (estável) | O que faz |
|------|-----------|-----------|
| `search_ads` | **Discover → ads em lote (filtros da UI)** | Busca Meta ads com os mesmos filtros do Explorer → Meta Ads: status, media type, days running, data de criação, idioma, ad rank (percentil), growth rank, tamanho da copy, países, nicho (`category_ids`), tráfego da loja, Trustpilot, ordenações (`longestRunning`, `mostDuplicates`, `adOrder`, `reachDelta*`). Motor da descoberta da 01 e da ETAPA 3F da 03 |
| `lookup_filter_ids` | **Lookup → ids de filtro / landing pages** | Resolve ids de nicho/categoria, apps, pixels, temas; com `type: "landing_pages"` + `scope_domain`, devolve as URLs de destino de uma marca com contagem de ads ativos (= LP mais escalada) |
| `search_shops` | **Discover → lojas** | Busca no universo de lojas indexado; `match_mode: "exact"` + domínio devolve visitas/mês, nota e nº de reviews no Trustpilot, data de criação, apps/tema |
| `search_advertisers` | **Discover → anunciantes** | Anunciantes por marca/domínio/copy com ads ativos, reach e lançamentos |
| `lookup` | **Lookup → entidade** | Resolve marca/domínio/página em ids roteáveis (shop, advertiser, brandtracker) |
| `scan_ad` | **Brief → decompor 1 ad** | Decompõe 1 Meta ad (ou uma collation de `search_ads`): hook, enquadramento, estrutura, LP, alcance, tempo no ar, veredito de escala |
| `find_winning_products` | **Discover → produtos winning** | Top products por nicho + keywords com sinais de tração |
| `find_similar_shops` | **Discover → lojas similares** | Lojas comparáveis por similaridade |
| `creative_inspiration_pack` | **Discover → inspiração criativa** | Hooks, landing pages, ângulos, media benchmarks por vertical |
| `brief_competitor` | **Brief → concorrente completo** | Análise competitiva completa (ads + email patterns + opportunities) |
| `get_brandtracker_scaling_ads` | **Brief → ads escalando (marca trackada)** | Ads de marca trackada com movimento de Ad Rank (7d/14d/30d) |
| `analyze_tracked_brand` | **Brief → marca trackada** | Deep-dive de marca trackada |
| `analyze_shop_emails` / `search_emails` / `get_email_html` | **Brief → emails da loja** | Padrões de envio, subject lines, HTML dos emails |
| `search_google_ads_library` / `search_tiktok_library` | **Discover → outros canais** | Ads no Google e no TikTok |
| `daily_radar` | **Monitor → mudanças** | Mudanças nas marcas trackadas |
| `list_tracked_brands` / `add_to_brandtracker` / … | **Monitor → lista** | Gestão das marcas monitoradas e favoritos |
| `check_credits` / `usage_get` | **Account → créditos** | Saldo, uso, limites |

> Ao codificar uma skill, refira-se à **coluna de intenção**, não ao nome literal. Descubra o nome real em runtime.

**Regra de leitura de escala (vale pra todas as skills):** o alcance (reach) publicado pela Meta só existe pra ads veiculados na União Europeia — ad só-US/Canadá aparece com alcance 0 sem significar gasto zero. Escala se lê por **dias no ar + duplicatas + ad rank + tráfego da loja**. Em `search_ads`, passe `sort_by` sempre (sem ele a tool injeta um filtro de alcance mínimo que zera resultados só-US); se vier vazio, `trend_signal: "relevance"`.

## Mapping skill → tool (por INTENÇÃO, não nome literal)

| Skill | Intenção de tool usada | O que melhora |
|-------|--------------|---------------|
| **01 product research** | *Discover → ads em lote* (as duas pesquisas fixas: native ads em imagem e em vídeo), *Lookup → ids de filtro / landing pages*, *Discover → lojas* (tráfego + Trustpilot), *Brief → decompor 1 ad* | TrendTrack é o motor de DESCOBERTA. O MCP roda os dois conjuntos de filtros do Explorer → Meta Ads e monta a ficha de cada marca (LP mais escalada, ads mais escalados, tráfego, Trustpilot). Sem MCP ou sem créditos, o membro aplica os mesmos filtros no browser e cola — a skill explica passo a passo |
| **03 competitor analysis** | *Brief → concorrente completo*, *Brief → decompor 1 ad*, *Discover → lojas*, *Discover → lojas similares*, *Discover → ads em lote* | ETAPA 1 (identificar concorrentes) + ETAPA 2 (PDPs) + ETAPA 3 (ads) viram 1-2 chamadas por concorrente. A ETAPA 3F (ads escalados com link da Ad Library) usa *Discover → ads em lote*: busca por domínio, 3 ordenações (duplicatas · alcance · tempo no ar), dedup por collation |
| **08 creative engine** | *Discover → inspiração criativa*, *Brief → decompor 1 ad* | ETAPA 3 (ângulos das 3 verticais) + Hooks Bank ganham dataset real de hooks vencedores no nicho |
| **11 ad-analysis** | *Brief → decompor 1 ad*, *Monitor → mudanças* | Decompor breakthroughs do membro com lente do mercado; monitoramento contínuo |
| **13 retention** | *Brief → emails da loja* | Email flows ganham referência de padrões reais de cadência/subject/content da concorrência |

## Detecção em runtime (padrão)

Cada skill que se beneficia tem bloco assim no início:

```
### Se TrendTrack MCP estiver conectado (opcional)

1. Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis na sessão.
2. NÃO assuma nomes fixos. Descubra em runtime quais existem e case por INTENÇÃO.
3. Rode a tool de créditos primeiro e diga ao membro quanto a skill vai gastar.
4. Passe filtros só via params que a tool realmente expõe.
5. Se NÃO existir tool que case com a intenção, siga o caminho manual da skill.
```

> **Regra dura de honestidade.** A AI só lê programaticamente o que tem MCP. Ferramenta paga sem MCP na sessão (SpyBox, Kalodata, SimilarWeb, ou o próprio TrendTrack quando o MCP não está conectado) a AI **nunca finge acessar**: diz exatamente o que olhar e onde, e trata o resultado como dado colado pelo membro. O dado colado entra no relatório como dado — sem rótulo de "manual" no texto (a procedência vai no `dados.json.source`).

## Falhas e fallback

Se uma chamada TrendTrack falhar (auth expirou, rate limit, créditos zerados, server down), a skill cai pro caminho manual daquela etapa sem interromper — dizendo ao membro o que fazer no browser e continuando de onde parou.

## Privacidade

OAuth read-only. Aura Engine NÃO armazena tokens — eles ficam no Claude Desktop/Code do membro (via MCP framework). Aura só consome via tool calls em runtime.
