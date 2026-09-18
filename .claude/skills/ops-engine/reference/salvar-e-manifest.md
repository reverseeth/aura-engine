# Ops Engine · Referência: SALVAR e atualização do manifest

> A regra do dual output com os arquivos isentos, a ordem das seções do relatório, o caso da primeira rodada cedo e os campos do manifest. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `ops-engine.md` → `ops-engine.html`). **Isentos** (arquivos operacionais — rule 6b): `dados.json` e os memos em `memos/`. O `.md` é fonte pra AI; o `.html` nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`). No `.md`, cada risco aberto de dano alto entra como citação `**Risco:**` (vira o card vermelho).

**Garantir diretório:** `mkdir -p workspace/[produto]/ops-engine/` antes de salvar.

Outputs em `workspace/[produto]/ops-engine/`:

- **`ops-engine.md`** contendo, nesta ordem: a constraint do ano (ETAPA 1) · checklist de continuidade com status e riscos abertos ranqueados (ETAPA 2) · status e processo de proteção de marca (ETAPA 3) · negócio como ativo — teste de moat, lacunas de exit e hábito de memo (ETAPA 4) · veredito e data de revisão (ETAPA 5) · pendências (o que falta e o que destrava, sem narrar tentativas). Numa primeira rodada cedo (só ETAPA 2), o doc contém só o checklist, os riscos e as pendências.
- **`ops-engine.html`** — companion.
- **`dados.json`** — schema acima.
- **`memos/`** — criada quando o primeiro memo existir.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete ops-engine` marca a skill em `skills_completed`, e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:

- Adicionar `ops-engine` em `skills_completed`
- Gravar `manifest.ops` = `{ constraint_type, constraint_statement, backups_ready, backups_total, open_risks_high, exit_ready_gaps, checked_at }` — o resumo de leitura rápida
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenerar o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>`
