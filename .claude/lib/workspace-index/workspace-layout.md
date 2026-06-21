# Workspace Layout — estrutura canônica de cada produto

> Fonte única de verdade da organização de `workspace/<slug>/`. Toda skill escreve e lê
> seguindo EXATAMENTE este mapa. O painel `ABRIR-AQUI.html` (gerado por `build_index.py`)
> depende dele: cada fase tem sua subpasta `0X-<stem>/` e o relatório humano é sempre
> `relatorio.html`.

## Princípio

Cada fase do pipeline mora numa **subpasta própria** cujo nome é **o stem da skill** (`08-creative-engine`, `11-ad-analysis`, etc.). Dentro de cada subpasta:

| Arquivo | Papel |
|---------|-------|
| `relatorio.html` | **O que o membro abre.** Report humano (design v5). É o link "Abrir" no painel. |
| `relatorio.md` | O que a IA lê nas fases seguintes (narrativa). |
| `dados.json` | Dados estruturados primários da fase (quando a fase tem JSON). |
| *(descritivos)* | Arquivos secundários mantêm nome descritivo dentro da pasta (ex: `research-foundation.json`, `compliance-log.json`, `concept-01.md`). |

Arquivos de **infra/fundação** ficam na raiz do produto (não são fase): `manifest.json`, `brand.md`, `brand/logo.svg`, `promise-check.json`, `compliance-warnings.json`, `creative-dna/` (compartilhado 08+11), `ABRIR-AQUI.html`, backups. O `profile.md`/`profile.html` do membro são **globais** em `workspace/` (não por produto).

## Mapa por fase (sufixo relativo a `workspace/<slug>/`)

```
manifest.json                          ← infra (inalterado)
brand.md  ·  brand/logo.svg            ← infra (inalterado)
promise-check.json                     ← infra compartilhada (07b + 10)
compliance-warnings.json               ← infra compartilhada (07b + 10)
creative-dna/                          ← infra compartilhada (08 escreve features-*, 11 escreve perf-*/dna-profile)
ABRIR-AQUI.html                        ← painel, gerado por build_index.py

01-product-research/
  relatorio.md   relatorio.html         (01 não tem dados.json)
02-market-research/
  relatorio.md   relatorio.html   dados.json
03-competitor-analysis/
  relatorio.md   relatorio.html   dados.json
  creative-patterns.json                (era 03-creative-patterns.json)
  creatives-inbox/transcripts/[id].json (era 03-creatives-inbox/)
04-offer-builder/
  relatorio.md   relatorio.html   dados.json
  research-foundation.json              (era 04-research-foundation.json)
05-bonus-delivery/
  relatorio.md   relatorio.html   dados.json   (dados.json = era 05-bonus-delivery-log.json)
  bonuses/[bonus-id]/[bonus-id].pdf
06-copy-engine/
  relatorio.md   relatorio.html   dados.json
  compliance-log.json                   (era 06-compliance-log.json)
07-page/                                ← storefront (07a design + 07b build); pasta já era foldered
  07-plan.json   07-design-system.md   07-design-system.html
  design/page.html   design-tokens.json   design-signals.json
  iterations-log.json                   (movido pra cá; era na raiz do produto)
  07-page.md   07-page.html             (relatório humano da página = 07-page.html)
  07-deploy-report.json
  staging/...   theme-clone/...
07c-tracking-setup/                     ← movido pra FORA de 07-page/
  relatorio.md   relatorio.html   dados.json   (dados.json = era 07c-tracking.json)
07d-checkout-aov/
  relatorio.md   relatorio.html   dados.json
08-creative-engine/                     ← pasta renomeada de 08-creatives/
  relatorio.md   relatorio.html   dados.json   (relatorio = era 08-creative-strategy; dados = era 08-creatives.json)
  concept-NN.md/.html   concept-NN-edl.md   hooks-bank.md/.html   production-summary.md/.html
  compliance-log.json                   (era 08-compliance-log.json, estava na raiz)
  prompts/...
09-consistency-audit/
  relatorio.md   relatorio.html   dados.json
10-ad-strategy/
  relatorio.md   relatorio.html   dados.json
11-ad-analysis/                         ← pasta renomeada de 11-analysis/
  relatorio.md   relatorio.html   dados.json   (relatorio/relatorio.html = a análise mais recente; dados.json = era latest.json)
  [YYYYMMDD]-analysis.md/.html          (arquivo histórico de cada rodada)
  NEXT_BATCH_IDEAS.md   raw-pull-[ts].json   mcp-errors.log
12-scale-engine/                        ← pasta renomeada de 12-scale/
  relatorio.md   relatorio.html   dados.json   (relatorio = era 12-scale-plan; dados = era 12-scale.json)
  scale-directives.md                   (era 12-scale-directives.md)
13-retention-engine/                    ← consolida flat 13-retention.* + pasta 13-retention/
  relatorio.md   relatorio.html   dados.json   (dados.json = era 13-retention-log.json)
  [fluxo]/email-N.html   [fluxo]/flow-metadata.json   [fluxo]/setup-guide.md
14-content-recycler/                    ← pasta renomeada de 14-recycled/
  relatorio.md   relatorio.html         (índice das fontes recicladas — p/ o painel)
  [source-id]/README.md/.html   [source-id]/essence.json   [source-id]/compliance-log.json
```

## Regra de geração do painel

Toda skill, **depois** de salvar seus outputs e atualizar o `manifest.json`, roda:

```bash
python3 .claude/lib/workspace-index/build_index.py <slug>
```

Isso regenera `workspace/<slug>/ABRIR-AQUI.html` refletindo o que já foi feito + próximo passo. `<slug>` = `product_slug` do manifest.

## Produtos legados

Produtos criados antes desta reorganização (ex: numeração antiga `05-copy/`, `06-page/`, `07-creatives/`) **não** são migrados automaticamente — a numeração das skills mudou no overhaul. Se o membro quiser migrar um produto legado, é um passo manual à parte (não rode skills novas esperando achar os outputs no layout novo até migrar).
