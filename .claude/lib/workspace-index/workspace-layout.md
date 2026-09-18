# Workspace Layout — estrutura canônica de cada produto

> Fonte única de verdade da organização de `workspace/<slug>/`. Toda skill escreve e lê
> seguindo EXATAMENTE este mapa. O painel `ABRIR-AQUI.html` (gerado por `build_index.py`)
> depende dele: cada fase tem sua subpasta `<stem>/` (o stem é o id da skill, sem número) e o
> relatório humano é `<stem>.html` — única exceção: a fase de página, cujo relatório humano é
> `page/page-report.html`, escrito pela `page-build` pós-deploy.

## Princípio

Cada fase do pipeline mora numa **subpasta própria** cujo nome é **o stem da skill** (`creative-engine`, `ad-analysis`, etc.). Dentro de cada subpasta:

| Arquivo | Papel |
|---------|-------|
| `<stem>.html` (ex: `market-research.html`) | **O que o membro abre.** Report humano (design v5). É o link "Abrir" no painel. |
| `<stem>.md` (ex: `market-research.md`) | O que a IA lê nas fases seguintes (narrativa). |
| `dados.json` | Dados estruturados primários da fase (quando a fase tem JSON). |
| *(descritivos)* | Arquivos secundários mantêm nome descritivo dentro da pasta (ex: `research-foundation.json`, `banco-de-marcas.md`, `concept-01.md`). |

**Por que `dados.json` NÃO ganha nome por fase:** é um arquivo AI-only (o membro nunca abre), e o nome imutável permite que qualquer skill downstream leia `[fase]/dados.json` sem manter mapa de nomes por fase. O nome descritivo existe pra ajudar o MEMBRO a se orientar em .html/.md — pra dado estruturado que só a IA consome, uniformidade > descritividade.

**Compat legado (nomes de relatório):** produtos criados antes da renomeação usam `relatorio.md`/`relatorio.html`. O `build_index.py` tenta `<stem>.html` primeiro e cai pra `relatorio.html`; skills que leem outputs das fases mais consumidas (`market-research`/`competitor-analysis`/`offer-builder`/`copy-engine`) leem `<stem>.md` e, se não existir, `relatorio.md` (legado). Esse nível não tem migração automática.

**Compat legado (pastas numeradas):** produtos criados antes da reforma de 2026-09 guardam cada fase numa pasta com prefixo numérico (o `legacy_folder` de cada skill no `.claude/skills.json`). O `tools/migrate.py` (migração `001_slug_folders`) renomeia essas pastas para o nome novo e traduz `skills_completed` para os ids; o hook de início de sessão roda `python3 tools/migrate.py --all` toda sessão, então em condição normal nenhuma skill encontra pasta numerada. Enquanto um produto não estiver migrado, o `build_index.py` e as skills leem da pasta numerada como fallback (por um ciclo, como o `relatorio.md`); a escrita é sempre na pasta nova. O manifest ganha `framework_version` (versão do layout; ausente = 1) e a pasta do produto ganha `.migrations.log`.

Arquivos de **infra/fundação** ficam na raiz do produto (não são fase): `manifest.json`, `brand.md`, `brand/logo.svg`, `creative-dna/` (compartilhado entre `creative-engine` e `ad-analysis`), `ABRIR-AQUI.html`, backups. O `profile.md`/`profile.html` do membro são **globais** em `workspace/` (não por produto), e o mesmo vale para `fontes/`: a pasta onde o membro guarda os arquivos de fonte que baixou da fundição, que a `page-design` lê na sub-etapa 2.1 e serve a qualquer produto. Ela é local-only como todo o resto do `workspace/`, e o pre-commit guard recusa arquivo de fonte no staging.

**Artefatos de runtime de rules** (criados sob demanda pelas rules, também na raiz do produto): `troubleshooting-log.md` (troubleshooting-patterns), `escape-paths-log.json` e `.snapshots/[timestamp]/` (emergency-escape-paths), `.manifest-backup-*.json` (skill `setup` / ES2); e **per-fase**, `[fase]/iterations-log.json` (iteration-driven-refinement — não existe log global de iterações na raiz).

## Mapa por fase (sufixo relativo a `workspace/<slug>/`)

```
manifest.json                          ← infra (inalterado)
brand.md  ·  brand/logo.svg            ← infra (inalterado)
creative-dna/                          ← infra compartilhada (`creative-engine` escreve features-*, 11 escreve perf-*/dna-profile)
ABRIR-AQUI.html                        ← painel, gerado por build_index.py

product-research/
  product-research.md   product-research.html   dados.json
  banco-de-marcas.md   banco-de-marcas.html    (banco de marcas — o .html só existe quando o membro não usa o Notion; o .md existe sempre)
sourcing/
  sourcing.md   sourcing.html   dados.json            (`sourcing`, opcional — fornecedor, cotação, logística)
market-research/
  market-research.md   market-research.html   dados.json
competitor-analysis/
  competitor-analysis.md   competitor-analysis.html   dados.json
  creative-patterns.json
  creatives-inbox/transcripts/[id].json
  ads-escalados.md   ads-escalados.html   ads-escalados-dados.json   (só quando a ETAPA 3F rodou)
offer-builder/
  offer-builder.md   offer-builder.html   dados.json
  research-foundation.json
bonus-delivery/
  bonus-delivery.md   bonus-delivery.html   dados.json
  bonuses/[bonus-id]/[bonus-id].pdf
copy-engine/
  copy-engine.md   copy-engine.html   dados.json
page/                                ← storefront (`page-design` design + `page-build` build)
  page-plan.json   design-system.md   design-system.html
  design/page.html                      (a página aprovada, a fonte única de verdade visual)
  design/assets/fonts/                  (cópia dos arquivos da fonte local usados na página, quando há)
  design/brief-codex.md                 (segunda opinião, sub-etapa 3.8: o briefing que o membro cola no Codex)
  design/page-codex.html                (segunda opinião: a versão que voltou de lá, quando o membro roda)
  design-tokens.json   design-signals.json   (na raiz do page/, NÃO em design/)
  iterations-log.json
  page-report.md   page-report.html     (relatório humano da página — escrito pela `page-build` PÓS-deploy)
  deploy-report.json
  staging/...   theme-clone/...
tracking-setup/
  tracking-setup.md   tracking-setup.html   dados.json
checkout-aov/
  checkout-aov.md   checkout-aov.html   dados.json
agentic-readiness/
  agentic-readiness.md   agentic-readiness.html   dados.json
creative-engine/
  creative-engine.md   creative-engine.html   dados.json
  concept-NN.md/.html   concept-NN-edl.md   hooks-bank.md/.html   production-summary.md/.html
  prompts/...   renders/asset-xxxx.mp4   (renders só quando o Higgsfield MCP rendeu in-session, já limpos)
consistency-audit/
  consistency-audit.md   consistency-audit.html   dados.json
ad-strategy/
  ad-strategy.md   ad-strategy.html   dados.json
ad-analysis/
  ad-analysis.md   ad-analysis.html   dados.json   (a análise mais recente)
  [YYYYMMDD]-analysis.md/.html          (arquivo histórico de cada rodada)
  NEXT_BATCH_IDEAS.md   raw-pull-[ts].json   mcp-errors.log
scale-engine/
  scale-engine.md   scale-engine.html   dados.json
  scale-directives.md
retention-engine/
  retention-engine.md   retention-engine.html   dados.json
  [fluxo]/email-N.html   [fluxo]/flow-metadata.json   [fluxo]/setup-guide.md
content-recycler/
  content-recycler.md   content-recycler.html         (índice das fontes recicladas — p/ o painel)
  [source-id]/README.md/.html   [source-id]/essence.json
finance-engine/
  finance-engine.md   finance-engine.html   dados.json   (consulta lateral)
  banking-sheet.csv                          (só no Modo B — medir)
creator-engine/
  creator-engine.md   creator-engine.html   dados.json   (lateral, 2 fases: A seeding/conteúdo, B performance)
  briefs/framework-[creator-slug].md   outreach/messages.md
  contracts/ambassador-agreement-[variant].md   roster.csv
promo-engine/
  promo-engine.md   promo-engine.html   dados.json   (lateral/sazonal — uma rodada por janela)
team-engine/
  team-engine.md   team-engine.html   dados.json    (lateral — org, vagas, pipeline de candidatos)
ops-engine/
  ops-engine.md   ops-engine.html   dados.json      (lateral — backups valem desde o começo)
  memos/AAAA-MM-DD-<assunto>.md                     (criada quando o primeiro memo existir)
marketplace-engine/
  marketplace-engine.md   marketplace-engine.html   dados.json   (lateral — canais além do site)
```

**Ad log (infra na raiz do produto, cânone `.claude/lib/ad-log/README.md`):** `ad-log.md` — registro append-only de toda mudança executada na conta de ads, escrito por `ad-strategy`, `scale-engine`, `promo-engine` e pelas receitas (a `content-recycler` planeja e não executa: quem executa loga). Isento de dual output (arquivo operacional de handoff, como `dados.json`).

## Dual output (.md + .html) — escopo e isenções

A regra 6b do CLAUDE.md vale pra **relatório voltado ao membro**: todo `.md` de relatório
gera um `.html` companion (design v5). São **ISENTOS** (arquivos operacionais de handoff
entre skills, que o membro não abre no browser):

- `dados.json` (e qualquer `.json` — dado estruturado é AI-only)
- `scale-directives.md` (`scale-engine` → `ad-analysis`: diretrizes operacionais)
- `NEXT_BATCH_IDEAS.md` (`ad-analysis` → `creative-engine`: fila de ideias)
- `concept-NN-edl.md` (`creative-engine` → editor: roteiro de montagem)
- `setup-guide.md` (`retention-engine`: passo-a-passo de ESP pro fluxo)
- `ad-log.md` (raiz do produto — registro append-only de mudanças na conta; cânone `ad-log`)
- `banking-sheet.csv` (`finance-engine`: planilha operacional do Modo B)
- `briefs/`, `outreach/messages.md`, `contracts/` e `roster.csv` (`creator-engine`: material operacional voltado ao creator, sempre em inglês US — não usa o design system Aura)
- `memos/AAAA-MM-DD-<assunto>.md` (`ops-engine`: memos de decisão WAFM)
- `design/brief-codex.md` (`page-design`: briefing pra colar num agente externo, não relatório que se abre no browser)

Na dúvida: se o arquivo é lido pela PRÓXIMA skill (não pelo membro), não precisa de .html.

## Regra de geração do painel

Toda skill, **depois** de salvar seus outputs e atualizar o `manifest.json` (sempre pelo `python3 tools/manifest.py <slug> set|complete`, que faz backup, valida contra o `manifest-schema.json` e grava `updated_at`; nunca editando o JSON à mão), roda:

```bash
python3 .claude/lib/workspace-index/build_index.py <slug>
```

Isso regenera `workspace/<slug>/ABRIR-AQUI.html` refletindo o que já foi feito + próximo passo. `<slug>` = `product_slug` do manifest. O painel lê o estado do produto do `tools/aura-status.py` (relatório de cada fase, skills marcadas, pontos a conferir), então painel e status nunca discordam.

**Painel global** (`workspace/ABRIR-AQUI.html`, fora de qualquer produto): um card por produto com progresso, próximo passo e o número de pontos a conferir, gerado por `python3 .claude/lib/workspace-index/build_index.py --global`.

## Estado verificável

`python3 tools/aura-status.py <slug>` (ou `--all`, `--json`, `--brief`) cruza o manifest, os arquivos da pasta e este layout: fase com relatório presente ou ausente; skill marcada em `skills_completed` sem artefato e artefato sem marca (ES3 da rule de escape paths); arquivo ou pasta fora do layout canônico (o canônico é a lista `writes` de cada skill no `.claude/skills.json`, mais a infraestrutura descrita acima); `dados.json` que falha no schema da fase (`.claude/templates/schemas/<id>.dados.schema.json`, um por skill que grava `dados.json` lido por outra). Separado das issues, imprime avisos informativos, que não são falha e não mudam o exit code: hoje, `dados.json` de fase cujo schema prevê o bloco `resumo` e que não tem o bloco no arquivo, porque a fase seguinte vai ler o arquivo inteiro em vez do resumo. O hook `Stop` (`.claude/hooks/post-skill.sh`) roda o mesmo status sozinho para o produto tocado nos últimos 30 minutos e mostra até 10 linhas com prefixo `[aura-status]`, uma vez por mudança.

## Produtos legados

Três níveis de legado:

1. **Nomes de relatório antigos** (`relatorio.md`/`relatorio.html`, `07-page.html`, `07-plan.json`, `07-design-system.*`, `07-deploy-report.json`): o `build_index.py` e as skills tratam via fallback de leitura (esquema novo primeiro, legado depois). Escrita nova usa SEMPRE o esquema novo. Sem migração automática.
2. **Pastas de fase numeradas do esquema anterior** (`01-product-research/`, `02-market-research/`, `07-page/`, `08-creative-engine/` etc., o `legacy_folder` de cada skill no registro): migradas automaticamente pelo `tools/migrate.py` (migração `001_slug_folders`), que o hook de início de sessão roda toda sessão. A migração renomeia a pasta, traduz `skills_completed` (`06-copy-engine` → `copy-engine`), faz backup do manifest (`.manifest-backup-*.json`) e registra cada passo em `.migrations.log`. Se a pasta nova já existir ao lado da numerada, ela NÃO mescla: avisa, registra no log e pula (resolver à mão, juntando o conteúdo na pasta nova e apagando a numerada). Nenhum outro arquivo do produto é tocado: referências a caminhos numerados dentro de `dados.json`, `deploy-report.json` ou notas ficam como estão (são texto, não caminho lido por script). Enquanto a migração não rodar, o `build_index.py` e as skills leem da pasta numerada como fallback, por um ciclo.
3. **Numeração antiga de pastas de antes do overhaul** (ex: `05-copy/`, `06-page/`, `07-creatives/`): sem fallback e sem migração automática (o nome não bate com nenhum `legacy_folder` do registro). Se o membro quiser migrar um produto desses, é um passo manual à parte (não rode skills novas esperando achar os outputs no layout novo até migrar).
