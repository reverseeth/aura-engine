# Marketplace Engine · Referência: SALVAR e atualização do manifest

> A regra do dual output, a ordem das seções do relatório e os campos do manifest, com o que a skill nunca escreve. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `marketplace-engine.md` → `marketplace-engine.html`). **Isento:** `dados.json`. O `.md` é fonte pra AI; o `.html` nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/marketplace-engine/` antes de salvar.

- **`marketplace-engine.md`** contendo, nesta ordem: (1) o veredito do gate com o sinal decisivo; (2) um bloco por canal avaliado — go/no-go, requisitos de entrada, fees/comissões e primeira meta (canal `not_evaluated` simplesmente não aparece); (3) sequência recomendada; (4) status e métricas dos canais abertos (rodadas de atualização); (5) pendências — o que falta e o que destrava, sem narrar tentativas.
- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete marketplace-engine` marca a skill em `skills_completed` (e valida o `marketplace-engine/dados.json` contra `.claude/templates/schemas/marketplace-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:

- Adicionar `marketplace-engine` em `skills_completed` (id canônico desta skill)
- Gravar `manifest.marketplace` = `{ gate_verdict, channels_live: [], amazon_status, tiktok_shop_status, affiliate_program_status, checked_at }` — o resumo que as outras skills leem sem abrir o `dados.json` inteiro
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenerar o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>`
