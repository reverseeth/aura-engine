# Bonus Delivery · Referência: Tracking de access rate e take-rate, a Fase B (ETAPA 4)

> A regra de que não existe log por compra, as fontes agregadas no re-run, o schema do snapshot em append, os KPIs por tipo, o threshold de alarme e os dois sistemas a puxar pra ler o take-rate como sinal econômico. Abra na ETAPA 4.

### ETAPA 4 — Tracking (access rate / take-rate) — Fase B

**Não existe log por compra.** O Claude não roda a cada pedido e esta skill não configura webhook — modelar delivery por compra geraria um arquivo que nasce vazio e nunca é alimentado. A métrica nasce AGREGADA, puxada das fontes reais no re-run da skill.

**No re-run (D+30 e a cada ciclo depois):**

1. **Shopify Analytics / Admin API** → take-rate: pedidos elegíveis no período vs pedidos que destravaram o brinde/tier (GWP, complementary, gift-wrap, tier do bundle).
2. **Klaviyo (via Skill `retention-engine`)** → access rate: open/click do email de entrega (e-book, discount code, community).
3. Gravar um **snapshot agregado por bônus** em `workspace/[produto]/bonus-delivery/dados.json` — array em **APPEND** (um item por bônus por período; o histórico mostra a evolução):

```json
[
  {
    "bonus_id": "bonus-01",
    "type": "gift_with_purchase",
    "delivery_channel": "shopify_function",
    "condition": "cart_threshold",
    "threshold": 65,
    "value_anchored": 49,
    "period": "2026-06-01..2026-06-30",
    "orders_eligible": 420,
    "orders_with_bonus": 219,
    "take_rate": 0.52,
    "access_rate": null,
    "source": "shopify_analytics | klaviyo | manual",
    "snapshot_at": "2026-07-01T14:00:00Z"
  }
]
```

KPIs por tipo:
- GWP / complementary SKU / gift-wrapping → **take-rate** (% dos pedidos elegíveis que destravam o brinde).
- E-book / digital / community → **access rate** (% que abre/baixa/aceita).

**Threshold de alarme:** access/take-rate < **30%** → o bônus não está agregando valor percebido. Surface pro membro como sinal de iteração na oferta (volta pra `offer-builder`), não como falha desta skill. Benchmark de GWP saudável: take-rate sobe pra ~50%+.

**Pra ler take-rate como sinal econômico (não só vaidade), puxe os SISTEMAS NOMEADOS** (rode a `best_query`):
- **Funnel Economics Profit Map (CRO + COGS + AOV + LTV levers)** (rode `funnel economics increase AOV lower COGS increase LTV CRO profit map supplement peptide example`) — onde o GWP/asset move o lucro (AOV via take-rate, LTV via reorder).
- **Profitable Scaling Margin (PSM = LTV / (CPA + COGS))** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS golden ratio`) — se o GWP sobe AOV mas o COGS do brinde derruba PSM, o bônus está caro demais; itera na `offer-builder`.
