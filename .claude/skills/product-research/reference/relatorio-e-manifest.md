# Product Research · Referência: SALVAR, o relatório da pesquisa e o manifest

> Os dois arquivos do relatório com a ordem do conteúdo (ficha primeiro, detalhe depois), a regra de só o resultado no doc e a atualização do manifest pelo script (slug novo, complete, campos preliminares, painel). Abra ao gravar o relatório.

### 2. Relatório da pesquisa (dual output — rule 6b)

1. **`product-research/product-research.md`** (a AI lê nas fases seguintes)
2. **`product-research/product-research.html`** (visualização humana, gerada com `python3 tools/render_report.py workspace/[produto]/product-research/product-research.md`)

Conteúdo (na ordem — ficha primeiro, detalhe depois):
1. **Resumo de 1 página**: a oportunidade #1 (marca-base → jogada), o mecanismo sugerido, por que funciona, o maior concorrente na mesma faixa, o score e os 3 riscos
2. Ranking completo (ETAPA 7) com timestamp e fórmula explícita
3. As jogadas de cada finalista com o "por que tem potencial" (ETAPA 6)
4. Pool de elementos validados, com contagem de marcas e saturação (ETAPA 4)
5. Análise estratégica dos finalistas (ETAPA 5)
6. Resultados de Trends e Trustpilot por marca, incluindo as eliminadas com o motivo (ETAPAS 2-3)
7. Plano preliminar da #1 (ETAPA 8)
8. Lista completa das marcas pré-selecionadas (link pro banco de marcas no Notion ou pro `banco-de-marcas.html`)

O doc segue `.claude/rules/report-only-results.md`: só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa. Dado que veio colado pelo membro entra como dado, sem marcação.

### 4. `manifest.json` (fonte única de verdade)

1. Se o `product_slug` do vencedor for diferente do slug temporário do setup: `mkdir -p workspace/[novo-slug]/`, mova o manifest e atualize `product_slug` e `product_name` com `python3 tools/manifest.py <novo-slug> set product_slug '"<novo-slug>"' product_name '"<nome>"'`.
2. Marque a skill pelo script (nunca editando o JSON à mão): `python3 tools/manifest.py <slug> complete product-research` (não duplica, faz backup e grava `updated_at`).
3. Os campos do item 4 entram com `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]`.
4. Grave (PRELIMINARES — a Skill `market-research` refina): `product_vertical`, `awareness_distribution` (`{unaware, problem, solution, product, most}`), `sophistication_stage` (1-5), e o bloco `product_research: { "source": "trendtrack_mcp|manual|mixed", "notion_url": "...|null", "winner_play_id": "play-01", "base_brands": ["..."] }`.
5. Preserve todos os campos do setup (`budget_tier`, `budget_daily`, etc.).
6. Regenere o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>`.
