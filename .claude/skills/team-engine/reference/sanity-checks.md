# Team Engine · Referência: Checagens de sanidade (ETAPA 14)

> Os doze itens que bloqueiam o salvamento do relatório. Abra na ETAPA 14.

### ETAPA 14 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Toda vaga recomendada tem `hiring_decision.constraint` preenchido com o gargalo real e o dado que o sustenta — nenhuma vaga "porque sim".
2. `stage_check` gravado; pra membro `starter`/`validating` sem exceção aplicável, o output é a resposta "ainda não" da ETAPA 1.5 — o funil completo não rodou por inércia.
3. Nenhuma vaga em `open_roles[]` com anúncio publicado sem `scorecard` preenchido (missão + funções + par de indicadores com faixa).
4. Todo par de indicadores-norte é balanceado (volume + qualidade juntos); nenhum KPI de volume solto.
5. `payroll.fits_cash` só tem veredito quando os números da `finance-engine` (ou do membro) existem; sem eles, `null` + entrada em `pending_inputs[]` + a recomendação virou pergunta.
6. Nenhum salário, KPI real ou dado de agenda do membro foi inventado — benchmarks da fonte estão marcados como referência (`source: "reference"`), números do membro como `member`.
7. Nenhum creator/afiliado/embaixador entrou em `org` ou `open_roles[]` — fronteira com a `creator-engine` respeitada.
8. Nenhuma recomendação de desligamento sem os 2 gatilhos avaliados com dados — e com plano de recuperação antes, exceto violação grave de ética.
9. Recomendação de promoção cita a prova concreta (trigger objetivo), nunca "merece" solto.
10. `naming_suffix_by_person` gravado quando existe editor/strategist produzindo criativo — é o handoff que liga hit rate a pessoa na `ad-analysis`.
11. O relatório contém só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa (rule `report-only-results.md`), e 100% legível de primeira por quem não é do setor (regra 0).
12. Portas não rodadas não deixaram seção vazia nem explicação no relatório.
