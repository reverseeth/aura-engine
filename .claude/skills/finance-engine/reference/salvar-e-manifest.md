# Finance Engine · Referência: SALVAR e atualização do manifest

> A regra do dual output com os isentos, os outputs na ordem dos treze blocos do relatório, o `banking-sheet.csv`, e a atualização do manifest pelo script com os campos gravados. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `finance-engine.md` → `finance-engine.html`). **Isentos** (arquivos operacionais — rule 6b): `dados.json` e `banking-sheet.csv`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/finance-engine/` antes de salvar.

Outputs em `workspace/[produto]/finance-engine/`:

- **`finance-engine.md`** contendo, nesta ordem:
  1. Modelo mensal completo, com `gross_margin_needed_to_exist` em destaque (ETAPA 2)
  2. Margem de contribuição e ponto de cobertura do fixo, com first order e repeat order em blocos separados (ETAPA 3)
  3. Piso de CAC, CAC máximo do primeiro pedido e viabilidade do CPA-alvo (ETAPA 4)
  4. **A espiral do ROAS com os números do membro** — o breakeven com fixo, o spend de breakeven e o veredito (ETAPA 5)
  5. Necessidade de caixa em 90 dias, runway e guard-rails (ETAPA 6)
  6. **[Modo B]** As 4 alavancas simuladas e ranqueadas (ETAPA 7)
  7. **[Modo B]** Tabela de cohort com decay, coluna de margem acumulada e mês de cruzamento (ETAPA 8)
  8. **[Modo B]** Payback, first-order profitability e teto de escala (ETAPA 9)
  9. **[Modo B]** Stack de float e o efeito dele na necessidade de caixa (ETAPA 10)
  10. **[Modo B]** Banking sheet e notas mensais (ETAPA 11)
  11. Stress test (ETAPA 12)
  12. Benchmarks, Four Quarter Accounting e veredito, mais o memo de decisão quando houver decisão que custa dinheiro (ETAPA 13)
  13. Pendências: o que falta e o que destrava — sem narrar as tentativas

  No Modo A, os itens 6 a 10 simplesmente não aparecem. O doc segue `.claude/rules/report-only-results.md`: só o resultado, sem descrever o que não contém.

- **`banking-sheet.csv`** (só no Modo B) — cabeçalhos das colunas da ETAPA 11, uma linha por dia do mês corrente, coluna de fluxo líquido pronta.

- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete finance-engine` marca a skill em `skills_completed` (e valida o `finance-engine/dados.json` contra `.claude/templates/schemas/finance-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:

- Adicionar `finance-engine` em `skills_completed`
- **Gravar `manifest.fixed_costs_monthly`** quando o membro informar. É o campo canônico compartilhado com as skills `offer-builder`, `ad-analysis` e `scale-engine` (descrito no `manifest-schema.json`). Se já existir e o membro der outro valor, o novo prevalece e a mudança é avisada em uma linha.
- Gravar `manifest.finance` = `{ mode, breakeven_roas_with_fixed, cut_spend_recommendation_allowed, cash_needed_90d, runway_months, payback_window_days_measured, scale_ceiling_monthly_spend, checked_at }` — o resumo que as outras skills leem sem abrir o `dados.json` inteiro
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `ABRIR-AQUI.html`, onde `<slug>` é o `product_slug`)
