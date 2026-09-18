# Team Engine · Referência: SALVAR e atualização do manifest

> A regra do dual output, as quatorze seções do relatório na ordem das portas rodadas e os campos do manifest, com o que a skill nunca escreve. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `team-engine.md` → `team-engine.html`). **Isento** (arquivo operacional): `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/team-engine/` antes de salvar.

Outputs em `workspace/[produto]/team-engine/`:

- **`team-engine.md`** contendo, na ordem das portas rodadas (portas puladas não aparecem):
  1. O veredito de estágio e o gargalo nomeado (ETAPA 1) — ou a resposta "ainda não" completa (ETAPA 1.5)
  2. **[Porta 1]** Taxa de recompra, as 4 zonas e a lista do que sai da mão do membro (ETAPA 2)
  3. **[Porta 1]** A sequência de contratação com tipo de vaga, faixa e prazo realista (ETAPA 3)
  4. **[Porta 1]** Interno vs fora, com o memo de decisão (ETAPA 4)
  5. **[Porta 2]** Scorecard + descrição da vaga prontos (ETAPA 5)
  6. **[Porta 2]** Anúncio pronto pra publicar + plano de sourcing (ETAPA 6, no `hiring_language`)
  7. **[Porta 2]** O funil com as etapas, o teste prático desenhado pro papel e o roteiro de oferta (ETAPA 7)
  8. **[Porta 2]** Métricas do funil e o veredito (ou a pendência) de "a folha cabe" (ETAPA 8)
  9. **[Porta 3]** Plano de onboarding de 8 semanas com QA regressivo e cadência (ETAPA 9)
  10. **[Porta 3]** KPIs por função com faixas + o painel semanal pronto pra copiar (ETAPA 10)
  11. **[Porta 3]** Org chart atual vs futuro, células e o ritmo semanal (ETAPA 11)
  12. **[Porta 3]** Ciclo de reviews, 9-box e o que fazer com cada casela (ETAPA 12)
  13. **[Porta 3]** Incentivos e promoções com a alavanca mais barata que resolve cada caso (ETAPA 13)
  14. Pendências: o que falta e o que destrava — sem narrar tentativas

- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete team-engine` marca a skill em `skills_completed` (e valida o `team-engine/dados.json` contra `.claude/templates/schemas/team-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:

- Adicionar `team-engine` em `skills_completed`
- Gravar `manifest.team` = `{ org_size, open_roles_count, hiring_recommended, constraint, payroll_monthly, key_man_risk_flag, checked_at }` — o resumo que as outras skills leem sem abrir o `dados.json` inteiro
- **NÃO** escrever `manifest.stage` (esta skill lê o stage, nunca o altera) e **NÃO** escrever `manifest.fixed_costs_monthly` (campo do membro via `offer-builder`/`ad-analysis`/`scale-engine`/`finance-engine` — esta skill só aponta)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `ABRIR-AQUI.html`, onde `<slug>` é o `product_slug`)
