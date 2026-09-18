# Ops Engine · Referência: Sanidade e veredito (ETAPA 5)

> Os oito itens que bloqueiam o salvamento do relatório e o formato do veredito final. Abra na ETAPA 5.

### ETAPA 5 — Sanidade e veredito

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. **Uma** constraint declarada — não uma lista de quatro.
2. Nenhum item do checklist marcado `ready` sem confirmação explícita do membro nesta conversa (ou em rodada anterior gravada no dados.json).
3. Nenhum status deduzido ou inventado; todo item sem resposta está `pending` e em `pending_inputs[]`.
4. Nenhum número de caixa calculado aqui — onde caixa aparece, é leitura da `finance-engine` ou ponteiro pra ela.
5. Nenhuma decisão de fornecedor/estoque tomada aqui — onde estoque aparece, é ponteiro pra `sourcing`.
6. Nenhuma instrução de MONTAR estrutura (BM, registro de marca) — montagem é da `setup`; aqui é status, processo e uso.
7. O relatório contém só o resultado (rule `report-only-results.md`) — sem narração de processo, sem descrição do que não foi feito.
8. `dados.json` validado e manifest atualizado.

O veredito final é curto e em linguagem direta: a constraint do ano em uma frase, os 3 riscos abertos mais graves com a mitigação de cada um, e a próxima data de revisão.
