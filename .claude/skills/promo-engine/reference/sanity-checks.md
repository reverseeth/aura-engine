# Promo Engine · Referência: Checagens de sanidade (ETAPA 11)

> Os doze itens que bloqueiam o salvamento do relatório. Abra na ETAPA 11.

### ETAPA 11 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. `promo_economics.status` é `computed` antes de qualquer item em `campaigns[]`, brief pra `creative-engine` ou calendário pra `retention-engine` — ou é `blocked_pending_inputs` com `pending_inputs[]` preenchido e as ETAPAs 5-8 ausentes do relatório (sem seção vazia narrando a ausência — rule `report-only-results.md`).
2. `breakeven_roas_promo` > `breakeven_roas` evergreen sempre que `desconto_efetivo > 0` (se não for, a conta está errada).
3. Nenhum número sem custo fixo subtraído foi rotulado "lucro" — sem a `finance-engine`, o rótulo é margem de contribuição, dito com todas as letras (§1).
4. Toda instrução de subida de budget da janela saiu com o valor de reset da meia-noite junto, e os resets estão em `scaling_window.midnight_resets[]`.
5. Nenhuma régua do Scaling Protocol foi redefinida — exceções e reset citam `.claude/lib/ad-taxonomy/README.md` §5.
6. `window.end` > `window.start`; a rule de desligamento aponta exatamente pra `window.end`; o automatic discount tem início e fim agendados.
7. Divisão respeitada: zero asset de email/SMS gerado aqui (`retention-engine`) e zero asset de criativo gerado aqui (`creative-engine`) — só brief e calendário.
8. Copy consumidor-final em inglês US; texto de banner/oferta confere com a matemática do desconto efetivo (stacking recalculado do compare-at); compare-at price não inflado; "up to" só com desconto não-uniforme; regras 8a/8b aplicadas.
9. Toda mudança executada na conta durante a rodada tem linha correspondente no `ad-log.md`, gravada no momento da execução.
10. Estruturas criadas via MCP nasceram PAUSED e rules nasceram desativadas; nada foi ativado pela skill.
11. Queries à base usam `best_query` byte-exata do índice; conteúdo ainda sem entrada usa o marcador `[query provisória — indexar]` — nunca query genérica inventada.
12. O relatório contém só o resultado (rule `report-only-results.md`) e o dual output foi gerado (.md + .html; `dados.json` isento).
