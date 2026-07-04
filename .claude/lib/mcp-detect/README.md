# MCP Detection — lista canônica de prefixos + convenção de "source"

Fonte única de verdade pros prefixos de tool MCP que o Aura Engine detecta em runtime e pra como cada skill/receita loga qual caminho foi usado. Toda skill e receita que detecta MCP referencia ESTE arquivo em vez de re-explicar o padrão em prosa.

## Princípio

MCP é sempre **opcional + cascade resiliente**. Cada integração tenta o caminho preferencial, cai pro fallback automático em caso de falha, e termina em fallback manual (membro cola dado / faz no UI). O membro NUNCA trava por causa de MCP ausente — só perde o enrichment.

A detecção é sempre por **prefixo de tool disponível na sessão**. Se não há tool com o prefixo, a integração não existe pra aquela run — segue o método tradicional sem avisar.

## Prefixos canônicos

| Integração | Prefixo de tool | Papel | Cascade |
|---|---|---|---|
| **TrendTrack** | `mcp__trendtrack__` | Enrichment de research (product/competitor/creative/retention) | TrendTrack → método tradicional (web fetch + Meta Ad Library + scraping) |
| **Meta Ads oficial** | `mcp__meta__ads_*` | Caminho preferencial pra ads (campaign mgmt, insights, datasets, benchmarks) | Oficial → Pipeboard → manual |
| **Meta Ads Pipeboard** | `mcp__meta-ads__` | Fallback 3rd party quando o oficial está disabled/indisponível | (é o 2º degrau do cascade Meta) |
| **Refero** | `mcp__refero__` | Design system curado (~200 sites premium) pra brand signals da 07a | Refero → screenshot→visão → design-clone → manual |
| **AIDesigner** | `mcp__aidesigner__` | Rota 3 do menu de rotas de design da 07a (geração de página via MCP) | AIDesigner → demais rotas do menu da 07a (clone-and-adapt / Claude Design handoff / frontend-design) |
| **Higgsfield** | `mcp__higgsfield__` | Render de vídeo AI in-session na 08 (30+ modelos: Kling 3.x, Veo 3.1, Sora 2; OAuth via browser, créditos do plano do membro) | Higgsfield MCP → prompts salvos pro membro gerar manualmente |
| **Foreplay** | `mcp__foreplay__` | Ad spy (200M+ ads; criativos escalados dos concorrentes) nas skills 03/08/11 | Foreplay → TrendTrack (se houver) → Meta Ad Library público / uploads do membro |
| **Shopify AI Toolkit** | `mcp__shopify__` | Operações de produto/tema (usado por `deploy-shopify-product.md` e `full-deploy.md`) | Shopify MCP → Playwright → manual |
| **Klaviyo oficial** | `mcp__klaviyo__` | Criação de flows de retenção (welcome/abandoned-cart/post-purchase) | Klaviyo MCP → HTML+setup-guide |
| **Shopify Dev** | `mcp__shopify_dev__` | Docs/validação Liquid+GraphQL (reduz hallucination na 07b) | Opcional — enrichment, sem fallback dedicado |
| **Stripe** | `mcp__stripe__` | AOV/PSM real (revenue histórico pra pricing) | Stripe → membro informa AOV manual |

> **Nota de naming Meta:** o connector oficial registra como `meta` (tools `mcp__meta__ads_*`); o Pipeboard registra como `meta-ads` (tools `mcp__meta-ads__*`). Não existe `mcp__meta-official__*` — esse alias nunca foi real. Detecte exatamente por esses dois prefixos.

## Detecção em runtime (snippet padrão)

```
<integração>_available = existe ao menos 1 tool com prefixo `mcp__<prefixo>__` na sessão

if <integração>_available:
    usar como fonte primária (caminho 1)
else:
    seguir o próximo degrau do cascade (fallback automático), sem avisar o membro
```

Para o cascade Meta (2 degraus de MCP + manual):

```
if tools `mcp__meta__ads_*` disponíveis E ad account não está "disabled":
    caminho 1 — oficial
elif tools `mcp__meta-ads__*` disponíveis:
    caminho 2 — Pipeboard
else:
    caminho 3 — fallback manual (membro cola screenshot/dados)
```

## Convenção de logging de "source"

Toda skill/receita que produz output a partir de MCP grava qual caminho foi usado, pra debug e pra que skills downstream saibam a procedência do dado. Valores canônicos do campo `source`:

| `source` | Significa |
|---|---|
| `trendtrack` | Dado veio do TrendTrack MCP |
| `meta_mcp_official` | Meta MCP oficial |
| `meta_mcp_pipeboard` | Pipeboard MCP (fallback) — incluir `fallback_reason` |
| `foreplay` | Dado veio do Foreplay MCP (ad spy) |
| `shopify_mcp` | Shopify AI Toolkit MCP (operações de produto/tema) |
| `admin_api_client_credentials` | Admin GraphQL direto via token de app do Dev Dashboard (grant `client_credentials`) — caminho SEM MCP, usado quando o Shopify MCP está ausente (ex: `create-fixed-bundles.md` Caminho 2) |
| `refero` | Refero MCP |
| `aidesigner` | AIDesigner MCP (rota 3 de design da 07a — valor de `design_route` no `page-plan.json`) |
| `screenshot_vision` | Print lido por visão nativa (fallback de signals da 07a) |
| `design_clone` | `tools/design-clone/` Playwright (caminho de extração de hex exato) |
| `klaviyo_mcp` | Klaviyo MCP oficial |
| `klaviyo_assets_guide` | Fallback HTML + setup-guide |
| `manual` | Membro forneceu o dado à mão |

Onde gravar:

- **Receitas de automação** (`recipes/*.md`): campo `source` no log JSON + entrada no `workspace/[produto]/automation-log.jsonl`.
- **Skills**: quando relevante pra downstream, no JSON de output da fase (ex: `design-signals.json` → `"source": "refero"`).
- **Fallback de Meta**: sempre acompanhar `source: "meta_mcp_pipeboard"` de `fallback_reason` (`account_disabled_in_official_beta` | `oauth_failed` | `official_unreachable` | `forced_by_member`) e logar o motivo em `mcp-errors.log`.

## Onde está documentado cada cascade

| Integração | Detalhe completo |
|---|---|
| TrendTrack | `.claude/lib/trendtrack-integration/README.md` |
| Refero | `.claude/lib/refero-integration/README.md` |
| AIDesigner | skill `07a-page-design.md` (rota 3 do menu de rotas de design) |
| Higgsfield | skill `08-creative-engine.md` (detecção + confirmação de créditos antes de renderizar) + setup em `.claude/automations/setup-mcps.md` (3.7) |
| Foreplay | skills `03-competitor-analysis.md` / `08-creative-engine.md` / `11-ad-analysis.md` + setup em `.claude/automations/setup-mcps.md` (3.8) |
| Meta (oficial/Pipeboard) | receita única `sync-campaign-from-meta.md` (cascade interno oficial → Pipeboard → manual), `pause-ad-set.md`, `upload-creative-to-meta.md` + setup em `.claude/automations/setup-mcps.md` |
| Shopify AI Toolkit | receitas `deploy-shopify-product.md` / `full-deploy.md` + setup em `.claude/automations/setup-mcps.md` (passo 4) |
| Klaviyo | skill `13-retention-engine.md` + setup em `.claude/automations/setup-mcps.md` |
| Shopify Dev / Stripe | `.claude/automations/setup-mcps.md` (opcionais) |
