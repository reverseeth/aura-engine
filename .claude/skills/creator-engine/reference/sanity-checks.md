# Creator Engine · Referência: Checagens de sanidade (ETAPA 15)

> Os doze itens que bloqueiam o salvamento do relatório. Abra na ETAPA 15.

### ETAPA 15 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Nenhum material de creator (brief, mensagem, contrato, report) em português — tudo inglês US.
2. Fase B só rodou com `breakthrough` confirmado no manifest; nenhuma etapa 8-14 aparece no relatório de uma rodada Fase A.
3. Nenhum creator marcado pra whitelisting sem breakthrough próprio; nenhum ad de um creator agendado pra página de outro (exceção única: o acesso de partnership de 30 dias da ETAPA 13, que não é whitelisting).
4. `report_visibility` é `spend_only` pra todo creator de retainer simples e `full` só pra performance.
5. Todo contrato gerado carrega o aviso de referência jurídica.
6. Nenhum valor de remuneração fora dos defaults da fonte sem ter vindo do membro; nenhum tier inventado.
7. Todo creator `hired` tem endereço confirmado e produto escolhido POR ELE registrado.
8. Todo brief tem ≤ 9 concepts e a curadoria por creator registrada (`curated: true` com a lista do que ficou).
9. A convenção de nome com o creator está definida e gravada em `handoff.for_skill_10` antes de qualquer conteúdo ir pra ad.
10. Nenhum conteúdo de terceiro (rip/borrowed) marcado como `dct_ready` — só referência de estrutura.
11. A matriz sub-avatar × creator aparece no relatório com as lacunas visíveis (célula vazia = casting que falta).
12. O relatório contém só o resultado — sem narração de processo, sem descrição de ausências (rule `report-only-results.md`).
