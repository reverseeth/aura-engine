# Creator Engine · Referência: Contrato de leitura, quem lê o quê

> Quem já lê hoje (ad-analysis) e os campos disponíveis pra creative-engine, ad-strategy, scale-engine e content-recycler, com a regra da leitura aditiva. Abra ao fechar o `dados.json`.

## Contrato de leitura (quem lê o quê)

**Quem já lê hoje:**

| Skill | Campo que já lê | O que muda |
|---|---|---|
| **11** ad-analysis | `performance_by_creator[].ad_naming_pattern` (o nome do creator no nome do ad) | A análise agrupa por creator e devolve quem venceu (fecha o loop da ETAPA 8) |

**Disponível para (leitura aditiva)** — dados publicados que as skills podem puxar quando fizer sentido, sem que já leiam hoje:

| Skill | Campo disponível | O que permite |
|---|---|---|
| **08** creative-engine | `content[].dct_ready`, `roster[].tier`, `briefs[]` | A rota B (montagem) ganha footage licenciado real do roster; o archetype `creator_human` deixa de ser "raro" quando há creator contratado; o batch não duplica concept que já está com creator |
| **10** ad-strategy | `handoff.for_skill_10` (naming, acessos, conteúdo cru) | Ads de creator sobem com o nome do creator no nome do ad; whitelisting/partnership viram opções de identidade na montagem; raw content campaign tem inventário |
| **12** scale-engine | `roster` por tier, `channels.tiktok_shop` | A coluna "Creators em retainer" da tabela de sub-fases ganha fonte real; o nível de escala consulta se há conteúdo/acessos pra abrir raw content (L2) e whitelisting (L3) |
| **14** content-recycler | `roster[]`, `report_visibility` | O creator-report do Movimento 6 sabe pra quem ir e com quais números visíveis |

Quando `creator-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — a leitura é aditiva, nunca pré-requisito.
