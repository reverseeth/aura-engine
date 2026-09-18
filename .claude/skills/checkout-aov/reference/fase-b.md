# Checkout & AOV · Referência: Fase B, o teste de backend em ciclos pós-launch

> Quando re-rodar, a regra de uma variável por ciclo, a leitura pela ad-analysis com o revenue do OTO reconciliado e o que a Fase B não é. Abra na Fase B.

### Fase B — teste de backend (cadência recorrente, pós-launch)

A primeira rodada desta skill arma o stack ANTES do tráfego. Com pedidos reais rodando, o backend não fica parado: ele **re-testa em ciclos** — e re-testar backend é mais barato que testar criativo, porque usa o tráfego que já foi pago.

- **Quando re-rodar:** quando a Skill `ad-analysis` já tem leitura de funil com amostra mínima (a régua da ETAPA 6B dela) — take rate lido com meia dúzia de pedidos é ruído, não sinal.
- **Uma variável por ciclo** (mesmo método científico dos ads): trocar o produto do OTO (re-rodando o Gate de Complementaridade), preço/âncora do upsell, o downsell (fórmula do Haddad — Alavanca 1), ordem/labels dos tiers, valor do threshold. A ORDEM dos testes segue a ordem de ROI dos testes de checkout (**Mecânica visual de pricing table**, já puxada na Alavanca 3 — não re-puxe).
- **A leitura é da Skill `ad-analysis` (handoff):** take rates reais vs projetados por alavanca, com o revenue do OTO reconciliado no Shopify — o Purchase do pixel não vê o valor do one-click ("Quando Usar"). Cada ciclo atualiza os `take_projected` do `dados.json` com os medidos e re-roda a reconciliação da ETAPA 4 (as regras de `scope_diff` continuam mandando em `manifest.target_cpa`/`breakeven_roas`).
- **O que a Fase B NÃO é:** escala de ads (Skill `scale-engine`) nem campanha de email (Skill `retention-engine` Fase B). É o backend — upsell/downsell/bundle/threshold — re-testado em ciclos enquanto os ads rodam.
