# Real Browser Agent — Automations

Coleção de "receitas" que permitem ao Claude Code executar operações diretamente
no Shopify (criar produto, wire variants, push tema) e Meta Ads Manager (subir
criativo, pausar ad set, rotacionar winners, puxar insights) via MCPs.

## Stack atual (julho/2026)

Receitas Meta usam **cascade resiliente** — tenta o MCP oficial primeiro, cai pro 3rd party automaticamente.

| Componente | URL/Fonte | Status |
|---|---|---|
| **Meta MCP oficial** (preferencial) | `https://mcp.facebook.com/ads` | Open beta desde 2026-04-29, rollout gradual sem GA, 29 tools |
| Pipeboard Meta MCP (fallback) | https://github.com/pipeboard-co/meta-ads-mcp | 3rd party, GA, dispara quando oficial está disabled no ad account |
| Shopify AI Toolkit (plugin Claude Code) | https://github.com/Shopify/shopify-ai-toolkit | Oficial, abril 2026 — **exportar `OPT_OUT_INSTRUMENTATION=true`** (ver alerta de telemetria no `setup-mcps.md` passo 4) |
| Higgsfield MCP (opcional) | `https://mcp.higgsfield.ai/mcp` | Oficial, render de vídeo in-session (Skill 08 + creative-loop) |
| Playwright (fallback final) | `pip install playwright` | Pra operações que MCPs não cobrem |
| Claude Code | tua assinatura | — |

Setup ambos os Meta MCPs em `setup-mcps.md` — Aura escolhe sozinha qual usar em cada chamada.

## Setup (15min, uma vez)

Segue `setup-mcps.md` passo a passo. Depois de configurado:
- Claude Code terá tools com prefixos `mcp__meta__ads_*` (oficial), `mcp__meta-ads__*` (Pipeboard) e `mcp__shopify__*` (AI Toolkit) disponíveis — lista canônica de prefixos em `.claude/lib/mcp-detect/README.md`
- Membro usa linguagem natural pra disparar receitas
- Zero infra 24/7 necessária (executa quando invocado)

## Receitas disponíveis

Em `recipes/`:

- `sync-campaign-from-meta.md` — puxa estado completo da campanha com **cascade interno** (MCP oficial → Pipeboard → manual). No caminho oficial inclui industry benchmarks, dataset quality, auction ranking e anomaly signal; no Pipeboard, mesmo shape sem esses blocos.
- `upload-creative-to-meta.md` — sobe vídeo aprovado pro Meta Ads Manager com UTM + pixel wired, modo pausado (humano ativa). Roda via Pipeboard ou Playwright porque o MCP oficial não aceita arquivo local.
- `pause-ad-set.md` — pausa ad set por CPA/freq threshold (emergência). Cascade oficial → Pipeboard.
- `deploy-shopify-product.md` — cria produto + variants pelos tiers de bundle da 07d (Solo/3-pack/6-pack) + wire Variant IDs no template da PDP
- `create-fixed-bundles.md` — cria os bundles FIXOS da oferta (tiers `qty > 1` do 04/07d) via Admin GraphQL `productBundleCreate` — bundle nasce como produto nativo, sem app de terceiro, qualquer plano. Cascade: Shopify MCP → Admin API `client_credentials` (token de app do Dev Dashboard) → app nativo Shopify Bundles manual. Invocada pela 07d Alavanca 3 caminho 2; roda DEPOIS de `deploy-shopify-product.md` (o produto principal precisa existir).
- `rotate-winning-creative.md` — detecta winner, gera variações via Skill 08 preservando DNA, sobe paused
- `creative-loop.md` — **loop semi-autônomo** ad → performance → variação com 2 gates humanos e guardrails (spend cap, piso de ROAS, incrementos < 20%, nunca publish autônomo). Ritual de ~15min pós-teste.
- `full-deploy.md` — orquestra full launch (Shopify product + campanha 1-1-N no Meta, tudo paused)

## Como invocar

Membro diz linguagem natural (padrões — troque pelos valores reais do seu produto):

```
"Claude, sobe o criativo aprovado <creative_id> pro ad set <nome> em modo pausado."
"Claude, pausa o ad set <nome> — CPA tá acima do target."
"Claude, cria o produto no Shopify com os tiers de bundle e wire no PDP."
"Claude, cria os bundles no Shopify."
"Claude, rotaciona o winner <creative_id> — sobe 3 variações."
"Claude, roda o loop criativo."
```

Claude identifica a receita apropriada em `recipes/`, executa step-by-step usando
MCPs, e reporta de volta.

## Segurança

- **Zero autonomous write**: operações destrutivas ou públicas (deletar produto,
  publicar tema live, ativar campanha) exigem confirmação explícita do membro
- **Paused by default**: ads subidos sempre em status PAUSED, humano ativa;
  Automated Rules nascem DESATIVADAS
- **Audit log**: cada ação de automação é registrada em
  `/workspace/[produto]/automation-log.jsonl`
- **Dry-run**: `full-deploy.md` e `upload-creative-to-meta.md` suportam `--dry-run`
  (simula sem criar nada real). As demais receitas ou são read-only (sync) ou têm
  gates humanos embutidos (creative-loop, pause, rotate).

## Limitações

- Shopify MCP não cria Pages ainda (julho 2026) — fallback Playwright ou manual
- Meta Ad Library monitoring requer API access ou scraping Playwright
- Change de catalog grande (500+ products) pode bater rate limit — batch em
  grupos de 50
