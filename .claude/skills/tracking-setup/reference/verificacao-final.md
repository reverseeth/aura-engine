# Tracking Setup · Referência: Verificação final e handoff (ETAPA 5)

> A checklist de sete itens que responde à creative-engine e à ad-strategy. Abra na ETAPA 5.

### ETAPA 5 — Verificação final + handoff

Antes de declarar pronto, confirmar a checklist (responde `creative-engine`/`ad-strategy`):

- [ ] Pixel conectado ao Dataset correto (bate com o ad account da `ad-strategy`)
- [ ] Data sharing do pixel em **"Always on"** (não "Optimized")
- [ ] 5 eventos do funil disparando (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)
- [ ] CAPI ON (Data sharing = Maximum) + Advanced Matching ON (dupla-coluna Browser + Server), sem fonte server-side duplicada (CAPI 1-clique)
- [ ] EMQ ≥ 6.0 no Purchase (ou `emq_warn` documentado; ou `pending_traffic` com Purchase validado por pedido-teste e `emq_pending: true` no manifest)
- [ ] Janela baseline `7d-click/1d-view` documentada, Incremental Attribution desligado, Click ID conferido no Purchase (ETAPA 3B)
- [ ] Analytics stack escolhido e instalado/confirmado + contrato de leitura fixado no relatório (Blended ROAS como P&L, CAC ≠ CPA — ETAPA 4B)
