# Real Browser Agent — Automations

Coleção de "receitas" que permitem ao Claude Code executar operações diretamente
no Shopify (criar produto, wire variants, push tema) e Meta Ads Manager (subir
criativo, pausar ad set, rotacionar winners) via MCPs oficiais.

## Stack grátis

| Componente | Fonte |
|---|---|
| Meta Marketing API MCP | https://github.com/pipeboard-co/meta-ads-mcp |
| Shopify AI Toolkit | https://github.com/Shopify/Shopify-AI-Toolkit (oficial, abril 2026) |
| Playwright (fallback) | `pip install playwright` |
| Claude Code | tua assinatura |

## Setup (15min, uma vez)

Segue `setup-mcps.md` passo a passo. Depois de configurado:
- Claude Code terá tools `meta_ads.*` e `shopify.*` disponíveis
- Membro usa linguagem natural pra disparar receitas
- Zero infra 24/7 necessária (executa quando invocado)

## Receitas disponíveis

Em `recipes/`:

- `upload-creative-to-meta.md` — sobe vídeo aprovado pro Meta Ads Manager com
  UTM + pixel wired, modo pausado (humano ativa)
- `pause-ad-set.md` — pausa ad set por CPA/freq threshold
- `deploy-shopify-product.md` — cria produto + 3 variants (Starter/Popular/BestValue)
  + wire Variant IDs no template da PDP
- `rotate-winning-creative.md` — detecta winner, sobe variações no Meta
- `create-shopify-page.md` — cria Page no Shopify Admin com template vinculado
- `bulk-update-metafields.md` — atualiza metafields em massa (proof, trust badges, etc)

## Como invocar

Membro diz linguagem natural (padrões — troque pelos valores reais do seu produto):

```
"Claude, sobe o criativo aprovado <creative_id> pro ad set <nome> em modo pausado."
"Claude, pausa o ad set <nome> — CPA tá acima do target."
"Claude, cria o produto no Shopify com 3 variants e wire no PDP."
"Claude, rotaciona o winner <creative_id> — sobe 3 variações."
```

Claude identifica a receita apropriada em `recipes/`, executa step-by-step usando
MCPs, e reporta de volta.

## Segurança

- **Zero autonomous write**: MCPs da Shopify exigem confirmação explícita pra
  operações destrutivas (deletar produto, dropar tabela)
- **Paused by default**: ads subidos sempre em status PAUSED, humano ativa
- **Audit log**: cada ação de automação é registrada em
  `/workspace/[produto]/automation-log.jsonl`
- **Dry-run mode**: toda receita suporta `--dry-run` antes de executar real

## Limitações

- Shopify MCP não cria Pages ainda (abril 2026) — fallback Playwright ou manual
- Meta Ad Library monitoring requer API access ou scraping Playwright
- Change de catalog grande (500+ products) pode bater rate limit — batch em
  grupos de 50
