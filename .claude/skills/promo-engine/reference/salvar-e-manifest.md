# Promo Engine · Referência: SALVAR e atualização do manifest

> A regra do dual output, a ordem das onze seções do relatório, o que some quando o gate bloqueia e os campos do manifest, com o que a skill nunca escreve. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `promo-engine.md` → `promo-engine.html`). **Isento** (arquivo operacional — rule 6b): `dados.json`. O `.md` é fonte pra AI; o `.html` nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/promo-engine/` antes de salvar.

Outputs em `workspace/[produto]/promo-engine/`:

- **`promo-engine.md`** contendo, nesta ordem:
  1. A janela: evento, datas, fases e o porquê do início cedo (ETAPA 1)
  2. Preparação: momentum, decisão VIP com a calculadora, estoque, pointer de backups, site (ETAPA 2)
  3. A oferta: core, stack com a matemática conferida, linguagem, bônus do pico e cauda degradada (ETAPA 3)
  4. **Os números recalculados da janela** — margem promocional, breakeven ROAS/CPA promo, target, piso de margem (ETAPA 4)
  5. Estrutura de campanha e budget inicial, com o status PAUSED e o que o membro ativa (ETAPA 5)
  6. Brief de criativo entregue à `creative-engine` (ETAPA 6)
  7. Calendário de email/SMS entregue à `retention-engine` (ETAPA 7)
  8. Plano de escala da janela: cadência de surf, curva do fim de semana, resets (ETAPA 8)
  9. Aterrissagem: rule de fim, cauda, volta pro evergreen (ETAPA 9)
  10. Pós-promo: leitura, cohort flagado, cofre sazonal e notas pro ano que vem (ETAPA 10)
  11. Pendências: o que falta e o que destrava — sem narrar tentativas

  Rodada bloqueada no gate: os itens 5 a 9 simplesmente não aparecem (rule `report-only-results.md` — sem seção vazia, sem descrever ausência).

- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete promo-engine` marca a skill em `skills_completed` (e valida o `promo-engine/dados.json` contra `.claude/templates/schemas/promo-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:

- Adicionar `promo-engine` em `skills_completed` (id canônico desta skill, padrão `NN-nome` do schema)
- Gravar **`manifest.promo`** = `{ event_name, window_start, window_end, breakeven_roas_promo, target_cpa_promo, active, checked_at }` — o resumo que a `ad-analysis` e a `scale-engine` leem sem abrir o `dados.json` inteiro; `active: true` na abertura, `false` na aterrissagem
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- **NÃO** sobrescrever `manifest.target_cpa`/`manifest.breakeven_roas` (são os números do EVERGREEN; os da janela vivem em `manifest.promo` e morrem com ela)
- Regenerar o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>`
