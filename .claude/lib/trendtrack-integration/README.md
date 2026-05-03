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

## Tools disponíveis (11)

| Tool | Categoria | O que faz |
|------|-----------|-----------|
| `find_winning_products` | Discover | Top-performing products por niche, com métricas de growth real |
| `search_shops` | Discover | Free-text search no universo de Shopify stores indexado (1M+ lojas) |
| `find_similar_shops` | Discover | Lojas comparáveis ranqueadas por similaridade |
| `creative_inspiration_pack` | Discover | Hooks, landing pages, ângulos, media benchmarks por vertical |
| `brief_competitor` | Brief | Análise competitiva completa (ads + email patterns + opportunities) |
| `scan_ad` | Brief | Decompõe 1 Meta ad: hook, ângulo, reach, scaling assessment |
| `analyze_tracked_brand` | Brief | Deep-dive de marca trackada (ads, hooks, LPs, format splits) |
| `analyze_shop_emails` | Brief | Padrões de envio + subject lines + content categories de emails |
| `daily_radar` | Monitor | Mudanças nas marcas trackadas (novos ads, launches, partnerships) |
| `list_tracked_brands` | Monitor | Lista das marcas monitoradas |
| `check_credits` | Account | Saldo, uso, limites |

## Mapping skill → tool

Cada skill tem ETAPA conditional que detecta TrendTrack e usa a tool apropriada. Se ausente, segue método tradicional (web fetch + Meta Ad Library + scraping).

| Skill | Tools usadas | O que melhora |
|-------|--------------|---------------|
| **01 product research** | `find_winning_products`, `search_shops` | Valida ideia contra winners reais com revenue data, em vez de só frameworks (Schwartz, mass desire) + Google Trends |
| **03 competitor analysis** | `brief_competitor`, `scan_ad`, `search_shops`, `find_similar_shops` | ETAPA 1 (identificar concorrentes) + ETAPA 2 (PDPs) + ETAPA 3 (ads no Meta Ad Library) viram 1-2 chamadas de tool com dados refinados, em vez de scraping + cloaker fallbacks |
| **08 creative engine** | `creative_inspiration_pack`, `scan_ad` | ETAPA 3 (ângulos das 3 verticais) + Hooks Bank ganham dataset real de hooks vencedores no nicho |
| **11 ad-analysis** | `scan_ad`, `daily_radar` | Decompor winners do membro com lente do mercado (comparar com benchmarks); `daily_radar` viabiliza loop de monitoramento contínuo |
| **13 retention** | `analyze_shop_emails` | Email flows ganham referência de padrões reais de cadência/subject/content da concorrência (em vez de só `02-market-research` + `04-offer`) |

## Detecção em runtime (padrão)

Cada skill que se beneficia tem bloco assim no início:

```
### Se TrendTrack MCP estiver conectado (opcional, melhora qualidade)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se sim:
- USE como fonte primária (dados mais frescos, mais escaláveis)
- Custa créditos TrendTrack do membro — não desperdiçar (1 chamada por necessidade real, não por exploração)

Se NÃO, segue ETAPA tradicional abaixo (web fetch + Meta Ad Library + scraping).
```

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
