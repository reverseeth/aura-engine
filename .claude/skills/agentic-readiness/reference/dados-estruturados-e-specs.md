# Agentic Readiness · Referência: Auditoria do JSON-LD no ar e o bloco de specs legível por agente (ETAPAs 3 e 4)

> O checklist do que o agente de compra consome no JSON-LD (GTIN, rating real, FAQPage, envio e devolução), a regra de que a correção acontece na page-build, e as specs concretas que o bloco agent-facts precisa cobrir. Abra na ETAPA 3.

### ETAPA 3 — Dados estruturados da PDP (auditoria do JSON-LD)

A `page-build` (ETAPA 4.5) já gerou e injetou o JSON-LD (Product + Offer + AggregateRating + BreadcrumbList + FAQPage). Aqui a auditoria é do que está **no ar**:

1. `curl -s <page_url>` → extrair os blocos `<script type="application/ld+json">` e validar presença/conteúdo.
2. Checklist do que agente de compra consome:
   - **GTIN/EAN** (o código de barras global do produto) no nó Product — é o campo que mais pesa pra matching de catálogo. Se o produto não tem GTIN (white-label novo), documentar o gap e usar `mpn`/`sku` no lugar; não inventar código.
   - **aggregateRating** com contagem real de reviews (se ainda não há reviews, OMITIR o nó — rating inventado é dado estruturado fraudulento).
   - **FAQPage schema** cobrindo as perguntas reais da PDP.
   - **shippingDetails** e **MerchantReturnPolicy** batendo com a config real da loja.
3. Se algum nó falta ou diverge → **a correção acontece na `page-build`** (é lá que o JSON-LD nasce, valida e injeta como bloco `custom_liquid`). Diga ao membro pra rodar a iteração da `page-build` com a lista exata de gaps; esta skill não injeta Liquid por fora do pipeline.

Status por item + lista `gaps[]`.

### ETAPA 4 — Bloco de specs legível por agente

Além do JSON-LD (máquina), o agente cita com mais confiança página que tem **fatos em prosa limpa**. A `page-build` já gera o bloco agent-facts (`data-aura-section="product-facts"`); aqui confira que ele está no ar e que cobre **specs concretas**:

- Materiais/ingredientes com quantidade ("500mg magnesium glycinate per capsule", "100% GOTS certified cotton, 200 GSM")
- Dimensões/peso/quantidade por embalagem
- Certificações verificáveis (GOTS, NSF, cGMP, third-party tested)
- Envio (prazo, origem), devolução (janela, quem paga), garantia (dias, condição)

Regra de ouro: **spec verificável > copy sensorial** pra esta camada. "47-day supply, 90-day money-back" rankeia pra query de agente; "transforms your mornings" não. O bloco NUNCA contradiz o JSON-LD nem a config real — é a mesma verdade em outro formato. Faltou spec que o membro tem? Coletar e mandar pra `page-build` adicionar. Ícones SVG, nunca emoji (rule 7); fatos diretos, sem aviso nem suavização (rule 8b).
