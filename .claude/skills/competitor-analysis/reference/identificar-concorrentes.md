# Competitor Analysis · Referência: Identificar concorrentes e pedir screenshots de ads (ETAPAs 1 e 1B)

> A base da product-research, a pergunta ao membro, a busca automática, a ampliação pra produtos adjacentes, a validação de URLs por HEAD com a cascade antes de descartar, o registro de `competitors_discarded[]` e o pedido opcional de screenshots do Adsparo. Abra na ETAPA 1.

### ETAPA 1 — Identificar Concorrentes

Se o product research já identificou concorrentes, use essa lista como base (5-10 marcas). Se não, pergunte:

"Você já sabe quem são seus concorrentes? Se sim, me manda os links das lojas deles. Se não sabe, diga 'não sei' — o sistema encontra sozinho."

**SE o membro mandar links:** use como base e complemente se for menos de 5.

**SE o membro disser que não sabe:** pesquise automaticamente (web search):
- `"[produto]" brand site:.com`
- `"[produto]" shop`
- Meta Ad Library busca: categoria + palavras-chave
- TikTok Shop Best Sellers na categoria
- Amazon Best Sellers na categoria
- Similarweb pra identificar lojas com tráfego no nicho

Identifique **5-10 concorrentes** ATIVOS (têm ads rodando agora + loja funcional). Se encontrar menos de 5, amplie a busca pra produtos ADJACENTES que resolvem o mesmo problema (ex: se o produto é colágeno em pó, inclua serums anti-aging, tratamentos capilares com collagen boost, e clínicas de estética — são alternativas que o avatar considera).

**Validação de URLs (obrigatória)**: para cada URL de concorrente identificada, faça um HTTP HEAD request com timeout de **5 segundos**. Classifique:

- **Acessível (2xx / 3xx)** → inclua na análise principal
- **QUALQUER 4xx / 5xx / timeout** → **NÃO descarte ainda.** Rode a cascade completa da ETAPA 2 (fetcher Playwright → Wayback → archive.today) antes de classificar. Muitos servidores bloqueiam HEAD mas servem GET, e bot-protections comuns (Akamai, PerimeterX, Shopify bot check) devolvem 403 **sem** header `cf-*` — descartar concorrente real no primeiro 403 viola a rule `.claude/rules/resilient-fetch.md`.
- **Só DNS error descarta direto** (domínio morto).

Concorrente que falhou em TODA a cascade vai pra `dados.json.competitors_discarded[]` com: URL, motivo, fallbacks tentados e hora do check (`checked_at`). O relatório lista só os concorrentes analisados (rule `report-only-results`).

### ETAPA 1B — Ads Screenshots dos Concorrentes

Verifique no `workspace/profile.md` se o membro tem Adsparo.

**SE TEM:**
"Cola screenshots dos ads mais escalados dos concorrentes — se tiver acesso ao Adsparo. Se não tiver esses screenshots em mãos agora, tudo bem: sigo com o Meta Ad Library público."

**SE NÃO TEM:** pule a pergunta, use Meta Ad Library público direto na Etapa 3.
