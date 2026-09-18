# Bonus Delivery · Referência: Integrações, valor ancorado com Kennedy Level-2, anti-patterns e regras de rigor (ETAPA 5)

> A tabela de integrações, o sistema a puxar pra valor ancorado e garantia, o Kennedy Level-2, a lista de anti-patterns e as quatro regras de rigor. Abra na ETAPA 5.

### ETAPA 5 — Integrações

| Integração | Pra quê | Caminho |
|---|---|---|
| **Shopify** (app GWP / Functions / Admin API) | Configurar GWP, complementary, gift-wrap, discount code | Coordenar config de checkout com **checkout-aov** |
| **Skill `retention-engine`** | Disparar email de entrega | A `retention-engine` é o executor; a `bonus-delivery` fornece conteúdo + trigger |
| **File hosting** (Shopify Files API / S3 / R2) | Hospedar PDF do e-book/guide | Gerar link público |
| **Fulfillment center** | In-box gift (complementary físico, gift-wrap) | Documentar instrução pro membro repassar |

## Valor ancorado e Kennedy Level-2

**Puxe o SISTEMA NOMEADO antes de fechar valor ancorado e garantia** (rode a `best_query`):
- **Kennedy Five-Level Guarantee Hierarchy (incl. Refund + Keep the Premium, Deliberate Redundancy, Guarantee the Letter)** (rode `Kennedy five level guarantee hierarchy refund keep the premium guarantee the letter itself`) — base do Level-2 (item 2).

1. **Valor ancorado:** o `value_anchored` do bônus ancora no preço de varejo do item ou no preço de itens comparáveis no mercado — a âncora mais alta que o comprador aceita como plausível.
2. **Kennedy Level-2 (keep-the-premium-on-refund):** atar o bônus à garantia — "se pedir reembolso, **fica com o bônus de qualquer forma**". Sinaliza confiança suprema e reduz fricção de compra. Coordenar com a `guarantee` do `offer-builder/dados.json` (se a garantia já é Level-2, a copy da página deve refletir; ver `copy-engine`/`page-design`). Surface pro membro se quiser ativar isso e ainda não está na oferta.

## Anti-patterns (FORBIDDEN)

- **Default "free PDF bonus"** sem justificar o fit com o dream outcome (e-book genérico tem access rate baixíssima).
- **Modelar bônus de info-product** (community/video/call) pra produto físico one-time — domínio errado.
- **GWP via draft order** — caminho errado; usar app ou Shopify Function.
- Bônus sem `delivery_trigger` (fica em limbo, nunca entregue).
- **Prometer bônus na PDP e deixar asset/config pra depois do launch** — a Fase A existe exatamente pra isso; comprador do dia 1 recebe o que a página prometeu.
- **Colocar threshold num bônus `condition: unconditional`** (quebra a promessa da página) — e vice-versa: auto-add num GWP que a página anuncia como "FREE over $X".
- Modelar log por compra (customer_id/delivered_at) — não há quem alimente; tracking é snapshot agregado (ETAPA 4).
- Discount code sem expiração (vira promo eterna).
- In-box gift (complementary/gift-wrap) sem coordenar com fulfillment (não vai na caixa).
- GWP threshold abaixo do AOV (queima margem sem empurrar AOV pra cima).
- Sobrescrever o `bonus-delivery/dados.json` em vez de dar append (perde o histórico de snapshots).

## Regras de rigor

1. **Bônus real e específico** — cada entrega é tangível e útil pro avatar. Recusar gerar bônus genérico sem justificar relevância.
2. **Bônus prometido existe antes do launch** — bônus prometido no stack da Skill `offer-builder` (visível na PDP) precisa ter asset + delivery/GWP setup completos **ANTES do go-live de ads** (Fase A). A Skill `consistency-audit` confere isso no H5.
3. **Access/take-rate tracking** — sempre que possível, medir. Bônus nunca acessado/escolhido = sinal de oferta fraca, itera na `offer-builder`.
4. **Fallback graceful** — se a API de hosting/Function falha, gerar PDF como último recurso E avisar o membro pra setup manual depois (ES6).
