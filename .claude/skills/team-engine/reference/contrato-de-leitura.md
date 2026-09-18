# Team Engine · Referência: Contrato de leitura, quem lê o quê

> Quem já lê hoje, o que está disponível para leitura aditiva em cada skill vizinha e a fronteira com a creator-engine. Abra ao fechar o `dados.json`.

## Contrato de leitura (quem lê o quê)

Esta skill é a **produtora** dos campos abaixo. A leitura é **aditiva, nunca pré-requisito**: quando `team-engine/dados.json` não existir, cada consumidora mantém o comportamento atual.

**Quem já lê hoje:**

| Skill | Campo que já lê | O que muda |
|---|---|---|
| **15** finance-engine | `payroll.payroll_delta_monthly` | A projeção de custo fixo da próxima rodada da `finance-engine` entra com a folha nova na mesa — o membro confirma o número, a `finance-engine` recalcula o ponto de cobertura. |

**Disponível para (leitura aditiva)** — dados publicados que as skills podem puxar quando fizer sentido, sem que já leiam hoje:

| Skill | Campo disponível | O que permite |
|---|---|---|
| **08** creative-engine | `org.pods`, `team_kpis.by_person`, vagas de editor/strategist abertas | Conhecer a capacidade real da máquina (nº de editores × ~7 vídeos/semana) e quem produz o quê — em vez de assumir capacidade infinita. |
| **09** consistency-audit | `onboarding[].qa_review_pct` | Dar a artefato produzido por pessoa em QA regressivo 100%/50% revisão proporcional — a amostragem decrescente vira dado disponível, não intuição. |
| **11** ad-analysis | `team_kpis.naming_suffix_by_person`, `hit_rate_pct` por pessoa | Descer ao nível 3 de granularidade (hit rate por editor) usando o sufixo de naming — atribuição de criativo a autor sem planilha manual. |
| **12** scale-engine | `org.key_man_risk`, `payroll.current_monthly_total`, `hiring_decision.constraint` | Checar, antes de escala agressiva, se a operação depende de uma pessoa só e qual gargalo de gente a escala vai estourar. |

**Fronteira com a `creator-engine` (não é leitura):** creators, afiliados e embaixadores nunca aparecem como funcionários neste arquivo; bounty interno (editor contratado) vive aqui — bounty externo é operado pela `creator-engine` (roster, tier `bounty` e convenção de nome de lá); daqui vai só a mecânica de recrutamento via comunidade.
