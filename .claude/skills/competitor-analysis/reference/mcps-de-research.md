# Competitor Analysis · Referência: MCPs de research opcionais, TrendTrack e Foreplay (ETAPA 0.5)

> As tools do TrendTrack que substituem etapas manuais, a regra de 1 brief por concorrente, o Foreplay como fonte de criativos escalados e o fallback silencioso. Abra na ETAPA 0.5.

### ETAPA 0.5 — MCPs de research (opcionais, se conectados)

**TrendTrack MCP:** verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use TrendTrack como fonte primária pra ETAPAs 1-3 e fallback de Cloudflare/cloaker fica desnecessário:

- **`mcp__trendtrack__search_shops`** com niche/keyword → substitui Etapa 1 manual de identificação de concorrentes (browse 1M+ Shopify stores indexados, com sinais de receita/crescimento).
- **`mcp__trendtrack__find_similar_shops`** após identificar 1 concorrente forte → encontra adjacentes ranqueados por similaridade.
- **`mcp__trendtrack__brief_competitor`** com domínio → substitui ETAPA 2 (PDP analysis) + ETAPA 3 (ads no Meta Ad Library) numa chamada só, retornando deep-dive com ads, email patterns, opportunities. Fim das corridas com cloaker/archive.today.
- **`mcp__trendtrack__scan_ad`** com URL/ID de ad → substitui análise manual de hook/ângulo na ETAPA 3, e dá assessment de scaling (volume + reach).

Pra cada concorrente, prefira 1 chamada `brief_competitor` em vez de 4-5 chamadas web fetch. Custa créditos — não desperdiçar em concorrente irrelevante. Limite: 5-10 concorrentes principais.

Se uma chamada falhar → silent fallback pra ETAPA tradicional, sem avisar membro.

**Foreplay MCP (ad spy):** verifique se há tools com prefixo `mcp__foreplay__`. Se SIM, use-as como fonte primária de criativos escalados dos concorrentes nas ETAPAs 3/3C (boards, top ads por marca, dados de veiculação) — elimina a dependência de screenshots/uploads do membro na 3C. Mesma regra do TrendTrack: chamada falhou → silent fallback pro método tradicional, sem avisar o membro.

Se nenhum MCP estiver disponível, pule esta etapa e siga ETAPAs 1-3 normalmente.
