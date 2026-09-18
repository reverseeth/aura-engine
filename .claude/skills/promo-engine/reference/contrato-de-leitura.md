# Promo Engine · Referência: Contrato de leitura, quem lê o quê

> As duas tabelas de quem já lê hoje e do que está disponível para leitura aditiva, com a regra de que a ausência do arquivo nunca bloqueia ninguém. Abra ao fechar o `dados.json`.

## Contrato de leitura (quem lê o quê)

**Quem já lê hoje:**

| Skill | Campo que já lê | O que muda |
|---|---|---|
| **12** scale-engine | `manifest.promo.active` (+ o resumo `manifest.promo`) | A exceção (a) do §5 só vale com janela registrada e ativa; na aterrissagem (`active: false`) a leitura do evergreen reinicia limpa |
| **15** finance | `result.promo_cohort_flagged_for_15` + números da janela | O mês da promo ganha nota obrigatória e o cohort não calibra decay sem ela |

**Disponível para (leitura aditiva)** — dados publicados que as skills podem puxar quando fizer sentido, sem que já leiam hoje:

| Skill | Campo disponível | O que permite |
|---|---|---|
| **08** creatives | `creative_brief_08` | O batch de sale nasce do brief (banner sobre o winner + statics de oferta), não de ideação evergreen |
| **11** ad-analysis | `window`, `scaling_window.midnight_resets`, `result.curve_by_day` | A janela demarcada separa efeito de promo de fadiga (o `ad-log.md` a `ad-analysis` já lê sempre, por cânone); winner de janela passa pelo filtro Lucky vs Durable antes de virar control |
| **12** scale-engine | `window`, `promo_economics.breakeven_roas_promo`, `landing.evergreen_budget_restored_to`, `seasonal_vault` | A volta pro evergreen usa o budget pré-janela do ad-log; o cofre alimenta revival |
| **13** retention | `email_sms_calendar_13`, `offer`, `window.phases` | Os sends sazonais nascem do calendário desta skill quando o membro roda 'retention'; flows se adaptam à promo sem desligar |
| **14** content-recycler | `seasonal_vault` | Winners sazonais entram na reciclagem com timing de religar |

Quando `promo-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — leitura aditiva, nunca pré-requisito.
