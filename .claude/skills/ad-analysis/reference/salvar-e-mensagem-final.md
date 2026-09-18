# Ad Analysis · Referência: SALVAR e mensagem final

> O texto integral da seção SALVAR (dual output, outputs da pasta, atualização do manifest) e da mensagem final por cenário. Abra ao fechar a análise.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `[YYYYMMDD]-analysis.md` e `ad-analysis.md`). **Isentos** (arquivos operacionais de handoff — rule 6b do CLAUDE.md, lista completa em `.claude/lib/workspace-index/workspace-layout.md`): `NEXT_BATCH_IDEAS.md`, `raw-pull-*.json`, `mcp-errors.log`, `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/ad-analysis/` antes de salvar.

Outputs em `workspace/[produto]/ad-analysis/`:
- `[YYYYMMDD]-analysis.md` (contendo todas as etapas do diagnóstico, incluindo a regra de KILL do playbook e os benchmarks de funil — histórico cumulativo)
- `[YYYYMMDD]-analysis.html` (companion visual)
- `ad-analysis.md` + `ad-analysis.html` (cópia da última rodada como relatório humano principal — é o que o painel do produto abre; sempre reflete a análise mais recente)
- `NEXT_BATCH_IDEAS.md` (input pra skill `creative-engine` no próximo batch — fecha loop)
- `dados.json` (handoff pra skill `scale-engine` — schema acima)

A pasta `ad-analysis/` acumula histórico — análises anteriores servem de input pra comparar evolução nas análises seguintes.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete ad-analysis` marca a skill em `skills_completed` (e valida o `ad-analysis/dados.json` contra `.claude/templates/schemas/ad-analysis.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo (ver lista canônica completa de campos acima):
- Adicionar `ad-analysis` em `skills_completed` (primeira vez) ou incrementar `analysis_count`
- Registrar `last_analysis_date`, `psm_real` + `psm_real_basis` (calculado via `LTV / (CAC_real + COGS)`), `breakthroughs[]` (+ o alias legado `winners[]` com o mesmo conteúdo), `kpi_winners[]`, `spend_winners[]`, `champions[]` (merge), `recommended_action`, **`ad_classification[]`** (shape do manifest-schema — substitui o array inteiro a cada análise) e **`click_based_purchase_share`** (quando medido; NUNCA estimado — sem o breakdown, não gravar)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html)

## Mensagem Final

Adapte baseado no diagnóstico (ver Etapa 9 — recomendação de scaling). Termine sempre com uma próxima-ação CLARA:

- Continua rodando (sem automação de escala — ela não existe em CBO) → monitora, próxima análise em 3-7 dias
- Teste abaixo do piso (`below_floor_directional_only` — PLAYBOOK item 6) → diga com todas as letras que o resultado é DIRECIONAL e que a próxima ação é subir o budget até o piso de US$ 100-150/dia OU reduzir conceitos no ar — nunca kill nem escala com esse dado
- Escala (**só com `breakthrough`**) → diga `'scale'`
- Breakthrough confirmado → junto da próxima ação, a recomendação de re-research (ETAPA 5): "aprofunde a pesquisa DESTE ângulo antes do próximo swing grande" — mini-passada da `market-research` no sub-avatar vencedor (`winning_sub_avatar_id`); o resultado alimenta a próxima iteração Sniper
- Iteração de criativos (`spend_winner`, `kpi_winner`, ou nenhum sinal) → diga `'creatives'`
- Ajuste de oferta → diga `'offer'`
- Ajuste de página → diga `'copy'` (camada de copy/espécime nomeada na ETAPA 6C) ou `'page'` (checkout/técnico)
- Custos fixos desconhecidos travando uma decisão de spend → pergunte o número antes de recomendar qualquer corte (e ofereça rodar **'finanças'** — a skill `finance-engine` fecha essa conta e devolve o breakeven com o fixo dentro)
- Espiral do ROAS com veredito de **subir** spend (`finance_verdict: "scale_up_accept_lower_roas"`) → diga o número: até quanto subir (`spend_to_breakeven_with_fixed`) e qual ROAS isso aceita
- Bloqueio técnico → resolução específica + nova análise depois

> Quando não há breakthrough, diga isso com todas as letras: "você ainda não tem um ad que escala". Não substitua por "aguardar mais dados" — o membro precisa saber que o próximo passo é criativo (`creative-engine`), não paciência.
