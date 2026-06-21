# TrendTrack Integration (opcional)

Integração com TrendTrack MCP. Read-only, OAuth 2.1, ~24h refresh. Substitui scraping manual + Meta Ad Library público em várias skills quando o membro tem assinatura TrendTrack.

## Quando usar

Membro tem TrendTrack pago E conectou via MCP. Detecção automática: se tools com prefixo `mcp__trendtrack__` existirem na sessão, usar; senão, fallback pro método existente da skill.

**Default = não-integrado.** Aura Engine funciona 100% sem TrendTrack (continua usando Meta Ad Library público + scraping). Integração é puro upside, não dependência.

## Como o membro conecta

Tutorial completo em `Aura.html`/`Aura-en.html` (passo opcional na seção Aura Engine). Fluxo:

1. Claude Desktop ou Code → Settings → Connectors → Add custom connector
2. URL: `https://api.trendtrack.io/v1/mcp`
3. OAuth → login TrendTrack → aprovar 4 scopes read-only
4. 11 tools aparecem automaticamente

## Runtime-discovery: NÃO assuma nomes de tool fixos

> **Regra central desta integração.** A lista de tools `mcp__trendtrack__*` **muda entre versões do MCP** — nomes podem ser renomeados, somados ou removidos. Por isso **nenhuma skill assume nomes de tool hard-coded** (`find_winning_products`, `search_shops`, etc). Em vez disso, cada skill:
>
> 1. **Descobre em runtime** quais tools `mcp__trendtrack__*` realmente existem na sessão (inspeciona os nomes disponíveis).
> 2. **Casa por INTENÇÃO/categoria, não por nome literal.** Pra cada necessidade da skill, procura uma tool cuja função bate com a intenção (descobrir produto, buscar loja, decompor ad, etc).
> 3. **Passa filtros só via params que a tool expõe** (não inventa params). Se a tool não suporta um filtro, a skill aplica esse filtro depois, no próprio fluxo.
> 4. Se **nenhuma** tool casa com a intenção necessária, trata como TrendTrack ausente pra aquela etapa e cai no fallback tradicional.

A tabela abaixo lista as tools que o TrendTrack expõe HOJE (referência, não contrato). Use os **nomes da categoria/intenção** pra casar — não os nomes literais como se fossem garantidos.

## Tools disponíveis hoje (referência — pode mudar)

| Tool (hoje) | Intenção / categoria (estável) | O que faz |
|------|-----------|-----------|
| `find_winning_products` | **Discover → produtos winning** | Top-performing products por niche, com métricas de growth real |
| `search_shops` | **Discover → lojas (free-text)** | Free-text search no universo de Shopify stores indexado (1M+ lojas) |
| `find_similar_shops` | **Discover → lojas similares** | Lojas comparáveis ranqueadas por similaridade |
| `creative_inspiration_pack` | **Discover → inspiração criativa** | Hooks, landing pages, ângulos, media benchmarks por vertical |
| `brief_competitor` | **Brief → concorrente completo** | Análise competitiva completa (ads + email patterns + opportunities) |
| `scan_ad` | **Brief → decompor 1 ad** | Decompõe 1 Meta ad: hook, ângulo, reach, scaling assessment |
| `analyze_tracked_brand` | **Brief → marca trackada** | Deep-dive de marca trackada (ads, hooks, LPs, format splits) |
| `analyze_shop_emails` | **Brief → emails da loja** | Padrões de envio + subject lines + content categories de emails |
| `daily_radar` | **Monitor → mudanças** | Mudanças nas marcas trackadas (novos ads, launches, partnerships) |
| `list_tracked_brands` | **Monitor → lista** | Lista das marcas monitoradas |
| `check_credits` | **Account → créditos** | Saldo, uso, limites |

> Ao codificar uma skill, refira-se à **coluna de intenção** ("preciso de uma tool de *Discover → produtos winning*"), não ao nome literal da coluna 1. Descubra o nome real em runtime.

## Mapping skill → tool (por INTENÇÃO, não nome literal)

Cada skill tem ETAPA conditional que detecta TrendTrack em runtime e casa a tool por **intenção** (não nome literal). Se ausente, segue método tradicional (web fetch + Meta Ad Library + scraping; ou membro cola dado de ferramenta paga).

| Skill | Intenção de tool usada | O que melhora |
|-------|--------------|---------------|
| **01 product research** | *Discover → produtos winning*, *Discover → lojas* | TrendTrack é o motor de DESCOBERTA automático (revenue estimado de forma legítima/programática). Substitui a leva manual do Kalodata. **SpyBox/Kalodata/SimilarWeb continuam validação manual** — a AI nunca finge acessar essas ferramentas pagas; pede o dado colado. SimilarWeb revenue é SEMPRE colado (sem API). |
| **03 competitor analysis** | *Brief → concorrente completo*, *Brief → decompor 1 ad*, *Discover → lojas*, *Discover → lojas similares* | ETAPA 1 (identificar concorrentes) + ETAPA 2 (PDPs) + ETAPA 3 (ads no Meta Ad Library) viram 1-2 chamadas de tool com dados refinados, em vez de scraping + cloaker fallbacks |
| **08 creative engine** | *Discover → inspiração criativa*, *Brief → decompor 1 ad* | ETAPA 3 (ângulos das 3 verticais) + Hooks Bank ganham dataset real de hooks vencedores no nicho |
| **11 ad-analysis** | *Brief → decompor 1 ad*, *Monitor → mudanças* | Decompor winners do membro com lente do mercado (comparar com benchmarks); a tool de monitor viabiliza loop de monitoramento contínuo |
| **13 retention** | *Brief → emails da loja* | Email flows ganham referência de padrões reais de cadência/subject/content da concorrência (em vez de só `02-market-research` + `04-offer`) |

## Detecção em runtime (padrão)

Cada skill que se beneficia tem bloco assim no início:

```
### Se TrendTrack MCP estiver conectado (opcional, melhora qualidade)

1. Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis na sessão.
2. NÃO assuma nomes fixos. Descubra em runtime quais existem e case por INTENÇÃO
   (ex: "preciso de uma tool de Discover → produtos winning"), não por nome literal.
3. Passe filtros só via params que a tool realmente expõe.
4. Se sim, USE como fonte primária (dados mais frescos, mais escaláveis).
   - Custa créditos TrendTrack do membro — não desperdiçar (1 chamada por necessidade
     real, não por exploração).
5. Se NÃO existir tool que case com a intenção, segue ETAPA tradicional abaixo
   (web fetch + Meta Ad Library + scraping; ou membro cola dado de ferramenta paga).
```

> **Limite ético da automação (regra dura).** TrendTrack é a ÚNICA fonte que a AI lê programaticamente. SpyBox, Kalodata e SimilarWeb são pagos e sem API que a AI consiga ler — a AI **nunca finge acessar** essas ferramentas. Quando precisa de um número delas (ex: revenue/visitas do SimilarWeb), ela diz exatamente o que olhar e onde, e trata o resultado como input colado pelo membro, marcando a fonte como manual.

## Custos / créditos

TrendTrack tem sistema de créditos por chamada. Antes de uma chamada cara (ex: `brief_competitor` com deep-dive), skill PODE invocar `check_credits` se o membro estiver no plano starter, pra não estourar limite. Pra membros em plano alto, skip esse check.

Heurística simples: se planning de uma skill envolve > 5 chamadas a TrendTrack tools, rode `check_credits` primeiro e mostre projeção de uso ao membro.

## Falhas e fallback

Se uma chamada TrendTrack falhar (auth expirou, rate limit, server down), skill loga o erro silenciosamente e cai pro fallback tradicional sem interromper. Membro vê output igual; só não tem o enrichment de dados reais.

## Privacidade

OAuth read-only. Aura Engine NÃO armazena tokens — eles ficam no Claude Desktop/Code do membro (via MCP framework). Aura só consome via tool calls em runtime.

## Roadmap (não implementado, idéias futuras)

- `daily_radar` poderia rodar em loop scheduled pra disparar skill 11 (ad-analysis) automaticamente quando concorrente faz movimento relevante
- `creative_inspiration_pack` results poderiam ser cacheados em `lib/creative-dna/registry.py` pra cross-product learning
- `analyze_shop_emails` poderia gerar starter templates pra skill 13 (retention) automaticamente
