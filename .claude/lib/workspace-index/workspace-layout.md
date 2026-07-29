# Workspace Layout — estrutura canônica de cada produto

> Fonte única de verdade da organização de `workspace/<slug>/`. Toda skill escreve e lê
> seguindo EXATAMENTE este mapa. O painel `ABRIR-AQUI.html` (gerado por `build_index.py`)
> depende dele: cada fase tem sua subpasta `0X-<stem>/` e o relatório humano é
> `<stem>.html` (o stem = nome da pasta sem o prefixo numérico — única exceção: fase 07,
> cujo relatório humano é `07-page/page-report.html`, escrito pela 07b pós-deploy).

## Princípio

Cada fase do pipeline mora numa **subpasta própria** cujo nome é **o stem da skill** (`08-creative-engine`, `11-ad-analysis`, etc.). Dentro de cada subpasta:

| Arquivo | Papel |
|---------|-------|
| `<stem>.html` (ex: `market-research.html`) | **O que o membro abre.** Report humano (design v5). É o link "Abrir" no painel. |
| `<stem>.md` (ex: `market-research.md`) | O que a IA lê nas fases seguintes (narrativa). |
| `dados.json` | Dados estruturados primários da fase (quando a fase tem JSON). |
| *(descritivos)* | Arquivos secundários mantêm nome descritivo dentro da pasta (ex: `research-foundation.json`, `compliance-log.json`, `concept-01.md`). |

**Por que `dados.json` NÃO ganha nome por fase:** é um arquivo AI-only (o membro nunca abre), e o nome imutável permite que qualquer skill downstream leia `[fase]/dados.json` sem manter mapa de nomes por fase. O nome descritivo existe pra ajudar o MEMBRO a se orientar em .html/.md — pra dado estruturado que só a IA consome, uniformidade > descritividade.

**Compat legado:** produtos criados antes da renomeação usam `relatorio.md`/`relatorio.html`. O `build_index.py` tenta `<stem>.html` primeiro e cai pra `relatorio.html`; skills que leem outputs das fases mais consumidas (02/03/04/06) leem `<stem>.md` e, se não existir, `relatorio.md` (legado). Nenhuma migração automática.

Arquivos de **infra/fundação** ficam na raiz do produto (não são fase): `manifest.json`, `brand.md`, `brand/logo.svg`, `promise-check.json`, `compliance-warnings.json`, `creative-dna/` (compartilhado 08+11), `ABRIR-AQUI.html`, backups. O `profile.md`/`profile.html` do membro são **globais** em `workspace/` (não por produto).

**Artefatos de runtime de rules** (criados sob demanda pelas rules, também na raiz do produto): `troubleshooting-log.md` (troubleshooting-patterns), `escape-paths-log.json` e `.snapshots/[timestamp]/` (emergency-escape-paths), `compliance-warnings.json` (pre-launch-gates — já listado na infra acima), `.manifest-backup-*.json` (skill 00 / ES2); e **per-fase**, `[fase]/iterations-log.json` (iteration-driven-refinement — não existe log global de iterações na raiz).

## Mapa por fase (sufixo relativo a `workspace/<slug>/`)

```
manifest.json                          ← infra (inalterado)
brand.md  ·  brand/logo.svg            ← infra (inalterado)
promise-check.json                     ← infra compartilhada (07b + 10)
compliance-warnings.json               ← infra compartilhada (07b + 10)
creative-dna/                          ← infra compartilhada (08 escreve features-*, 11 escreve perf-*/dna-profile)
ABRIR-AQUI.html                        ← painel, gerado por build_index.py

01-product-research/
  product-research.md   product-research.html         (01 não tem dados.json)
sourcing/
  sourcing.md   sourcing.html   dados.json            (01b, opcional — fornecedor, cotação, logística)
02-market-research/
  market-research.md   market-research.html   dados.json
03-competitor-analysis/
  competitor-analysis.md   competitor-analysis.html   dados.json
  creative-patterns.json
  creatives-inbox/transcripts/[id].json
04-offer-builder/
  offer-builder.md   offer-builder.html   dados.json
  research-foundation.json
05-bonus-delivery/
  bonus-delivery.md   bonus-delivery.html   dados.json
  bonuses/[bonus-id]/[bonus-id].pdf
06-copy-engine/
  copy-engine.md   copy-engine.html   dados.json
  compliance-log.json
07-page/                                ← storefront (07a design + 07b build)
  page-plan.json   design-system.md   design-system.html
  design/page.html                      (só page.html fica dentro de design/)
  design-tokens.json   design-signals.json   (na raiz do 07-page/, NÃO em design/)
  iterations-log.json
  page-report.md   page-report.html     (relatório humano da página — escrito pela 07b PÓS-deploy)
  deploy-report.json
  staging/...   theme-clone/...
07c-tracking-setup/
  tracking-setup.md   tracking-setup.html   dados.json
07d-checkout-aov/
  checkout-aov.md   checkout-aov.html   dados.json
07e-agentic-readiness/
  agentic-readiness.md   agentic-readiness.html   dados.json
08-creative-engine/
  creative-engine.md   creative-engine.html   dados.json
  concept-NN.md/.html   concept-NN-edl.md   hooks-bank.md/.html   production-summary.md/.html
  compliance-log.json
  prompts/...
09-consistency-audit/
  consistency-audit.md   consistency-audit.html   dados.json
10-ad-strategy/
  ad-strategy.md   ad-strategy.html   dados.json
11-ad-analysis/
  ad-analysis.md   ad-analysis.html   dados.json   (a análise mais recente)
  [YYYYMMDD]-analysis.md/.html          (arquivo histórico de cada rodada)
  NEXT_BATCH_IDEAS.md   raw-pull-[ts].json   mcp-errors.log
12-scale-engine/
  scale-engine.md   scale-engine.html   dados.json
  scale-directives.md
13-retention-engine/
  retention-engine.md   retention-engine.html   dados.json
  [fluxo]/email-N.html   [fluxo]/flow-metadata.json   [fluxo]/setup-guide.md
14-content-recycler/
  content-recycler.md   content-recycler.html         (índice das fontes recicladas — p/ o painel)
  [source-id]/README.md/.html   [source-id]/essence.json   [source-id]/compliance-log.json
```

## Dual output (.md + .html) — escopo e isenções

A regra 6b do CLAUDE.md vale pra **relatório voltado ao membro**: todo `.md` de relatório
gera um `.html` companion (design v5). São **ISENTOS** (arquivos operacionais de handoff
entre skills, que o membro não abre no browser):

- `dados.json` (e qualquer `.json` — dado estruturado é AI-only)
- `scale-directives.md` (12 → 11: diretrizes operacionais)
- `NEXT_BATCH_IDEAS.md` (11 → 08: fila de ideias)
- `concept-NN-edl.md` (08 → editor: roteiro de montagem)
- `setup-guide.md` (13: passo-a-passo de ESP pro fluxo)

Na dúvida: se o arquivo é lido pela PRÓXIMA skill (não pelo membro), não precisa de .html.

## Regra de geração do painel

Toda skill, **depois** de salvar seus outputs e atualizar o `manifest.json`, roda:

```bash
python3 .claude/lib/workspace-index/build_index.py <slug>
```

Isso regenera `workspace/<slug>/ABRIR-AQUI.html` refletindo o que já foi feito + próximo passo. `<slug>` = `product_slug` do manifest.

## Produtos legados

Dois níveis de legado, nenhum migrado automaticamente:

1. **Nomes de relatório antigos** (`relatorio.md`/`relatorio.html`, `07-page.html`, `07-plan.json`, `07-design-system.*`, `07-deploy-report.json`): o `build_index.py` e as skills tratam via fallback de leitura (esquema novo primeiro, legado depois). Escrita nova usa SEMPRE o esquema novo.
2. **Numeração antiga de pastas** (ex: `05-copy/`, `06-page/`, `07-creatives/`, de antes do overhaul de numeração): sem fallback — se o membro quiser migrar um produto desses, é um passo manual à parte (não rode skills novas esperando achar os outputs no layout novo até migrar).
