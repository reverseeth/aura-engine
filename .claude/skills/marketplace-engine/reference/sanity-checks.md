# Marketplace Engine · Referência: Checagens de sanidade (ETAPA 6)

> Os oito itens que bloqueiam o salvamento do relatório. Abra na ETAPA 6.

### ETAPA 6 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Nenhum canal com `verdict: "go"` sem `gate.verdict: "expand"` na mesma rodada.
2. O anti-sinal foi checado: nenhuma recomendação de canal novo motivada por fuga de CAC/criativo/oferta ruim no Meta.
3. Amazon com `go` e marca sem registro → a pendência de proteção (`setup`/`ops-engine`) está marcada e aparece no relatório antes de qualquer tática de listagem.
4. Toda comissão e fee de canal com `go` está registrada em `fees_and_commissions` e no handoff pra `finance-engine` — e nenhuma frase do relatório chama de "lucro do canal" um número que não passou pela `finance-engine`.
5. Nenhuma métrica de canal foi estimada; ausentes estão em `pending_inputs[]`.
6. Nada de plano de creator/conteúdo aqui (recrutamento, roteiro, volume de posts) — só requisitos de canal; conteúdo aponta pra `creator-engine`.
7. TROAS/retorno de anúncio interno da Amazon não foi comparado com ROAS do Meta em nenhuma tabela.
8. O relatório contém só o resultado (rule `report-only-results.md`) — sem narração de processo, sem descrição de ausências.
