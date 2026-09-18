# Marketplace Engine · Referência: Contrato de leitura, quem lê o quê

> Quem já lê hoje e o que está disponível para leitura aditiva nas skills vizinhas, com a regra de que a ausência do arquivo nunca bloqueia ninguém. Abra ao fechar o `dados.json`.

## Contrato de leitura (quem lê o quê)

**Quem já lê hoje:**

| Skill | Campo que já lê | O que muda |
|---|---|---|
| **15** finance-engine | `channels[].fees_and_commissions`, comissões | A margem por canal (fee/comissão como custo variável) entra no modelo — cada canal age como um mini negócio com a própria conta. |
| **16** creator-engine | `channels[tiktok_shop].commission_organic_pct`, `samples_policy`, meta de GMV | O pipeline TikTok Shop da `creator-engine` opera com os números de canal definidos aqui, sem redecidir o canal. |

**Disponível para (leitura aditiva)** — dados publicados que as skills podem puxar quando fizer sentido, sem que já leiam hoje:

| Skill | Campo disponível | O que permite |
|---|---|---|
| **12** scale-engine | `gate.verdict`, `channels[].status` | Canal `live` pode entrar nas projeções como fonte incremental (mesmo padrão do `manifest.agentic`), nunca como premissa de caixa. |
| **13** retention-engine | compradores de marketplace (lista anual da Amazon, clientes de TikTok Shop) | A lista alimenta a base de email própria — o trabalho de email é o normal da `retention-engine`. |

Quando `marketplace-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — a leitura é aditiva, nunca pré-requisito.
