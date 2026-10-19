# Tracking Setup · Referência: Verificação final e handoff (ETAPA 5)

> A checklist de sete itens que responde à creative-engine e à ad-strategy. Abra na ETAPA 5.

### ETAPA 5 — Verificação final + handoff

Antes de declarar pronto, confirmar a checklist (responde `creative-engine`/`ad-strategy`):

- [ ] Pixel conectado ao Dataset correto (bate com o ad account da `ad-strategy`)
- [ ] Wetracked como fonte única: data sharing do app Facebook & Instagram desligado, nenhum outro app de pixel ou CAPI, nenhum snippet no tema
- [ ] 5 eventos do funil disparando (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)
- [ ] CAPI do Wetracked ON + Advanced Matching (dupla-coluna Browser + Server), com o Wetracked como fonte server-side única (sem CAPI de 1 clique, sem Sonar ou container do Aimerce mandando pra Meta)
- [ ] EMQ ≥ 6.0 no Purchase (ou `emq_warn` documentado; ou `pending_traffic` com Purchase validado por pedido-teste e `emq_pending: true` no manifest)
- [ ] Janela baseline `7d-click/1d-view` documentada, Incremental Attribution desligado, Click ID conferido no Purchase (ETAPA 3B)
- [ ] Wetracked instalado e confirmado (mais a camada de atribuição, se `scaling` com Triple Whale ou Aimerce) + contrato de leitura fixado no relatório (Blended ROAS como P&L, CAC ≠ CPA — ETAPA 4B)
