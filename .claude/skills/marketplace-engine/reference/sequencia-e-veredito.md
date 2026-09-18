# Marketplace Engine · Referência: Sequência, plano por canal e veredito (ETAPA 5)

> A regra de um canal novo por vez com a ordem default, o que registrar por canal com a régua de cada um, e o encaminhamento do que está fora do escopo. Abra na ETAPA 5.

### ETAPA 5 — Sequência, plano por canal e veredito

**Um canal novo por vez.** Abrir dois ao mesmo tempo divide atenção e mata os dois. A ordem default quando mais de um canal passou no gate:

1. **Amazon primeiro** quando a busca de marca já cresce — é captura de demanda existente, o retorno mais rápido e a defesa mais urgente (revendedor não espera).
2. **TikTok Shop** quando a categoria é forte no social e a operação suporta o fluxo de creators (com a `creator-engine` rodando) — é geração de demanda + acervo, retorno mais composto e mais lento.
3. **Programa de afiliados** como camada sobre canal já rodando (site ou TikTok Shop) — em marca de identidade, pode subir na fila.

Para cada canal com `go`: registrar o plano de entrada resumido (requisitos, fees/comissões, dono, primeira meta), e para cada canal já aberto: atualizar status e métricas com a régua DO CANAL (TACOS/LTV-CAC na Amazon; GMV/comissão efetiva/afiliados ativos no TikTok Shop; % do GMV e retorno no programa de afiliados). Métrica que o membro não passou fica `null` e entra em `pending_inputs[]` — nunca preenchida com plausível.

**Fora do escopo — dito no relatório quando o membro pedir:** levar a CAMPANHA paga pra AppLovin/Axon ou TikTok Ads é expansão de canal de **mídia**, não de venda — é a skill **`content-recycler`, Movimento 4** (régua de US$ 250-1.000/dia por 60-90 dias pra crackear canal de mídia). Se o pedido do membro é esse, encaminhe sem rodar esta skill inteira.
