# Sourcing · Referência: Contrato com a offer-builder, o COGS real (ETAPA 13)

> A regra de escrita do `cogs_breakdown` (só as linhas do sourcing, preservando as demais), a tabela campo a campo, o cuidado com a contagem dupla do imposto no DDP e o fluxo de atualização com ou sem a `offer-builder` já rodada. Abra na ETAPA 13.

### ETAPA 13 — Contrato com a Skill `offer-builder` (COGS real)

Ao fechar a cotação, grave os números e atualize a oferta. **A `offer-builder` mantém o COGS num bloco de 8 linhas, todas em dinheiro por pedido, nunca em percentual** — o cânone é `.claude/lib/unit-economics/README.md` e a definição do bloco está na Skill `offer-builder`.

**Regra de escrita (crítica): a `sourcing` atualiza APENAS as linhas que o sourcing fecha e PRESERVA as demais com o valor que já está lá.** Nunca reescreva o `cogs_breakdown` inteiro, nunca zere um campo que esta skill não conhece.

| Campo do `cogs_breakdown` da `offer-builder` | Quem preenche | De onde vem aqui |
|---|---|---|
| `product_delivered` | **`sourcing`** | `landed_cost_per_unit` — produto na fábrica + embalagem + frete de entrada + imposto de importação, por unidade |
| `shipping_to_customer` | **`sourcing`** | `three_pl.shipping_to_customer_per_order` (inclui a parcela de frete grátis que a loja absorve) |
| `pick_pack` | **`sourcing`** | `three_pl.pick_pack_per_order` |
| `taxes_and_duties` | **`sourcing`** | Tributos por pedido que ainda NÃO estejam dentro do custo desembarcado |
| `refund_chargeback_provision` | **`sourcing` informa o piso** | `quality.defect_provision_per_order` (ETAPA 10.1) — a `offer-builder` decide o valor final, porque essa linha entra UMA vez só (ou aqui, ou como desconto no AOV líquido) |
| `payment_processing` | `offer-builder` | Não é domínio do sourcing — preservar |
| `subscription_app_fee` | `offer-builder` | Não é domínio do sourcing — preservar |
| `agency_fee_variable` | `offer-builder` | Não é domínio do sourcing — preservar |

**Cuidado com contagem dupla do imposto de importação:** no regime DDP, o imposto já está DENTRO do preço cotado e portanto dentro de `product_delivered`. Nesse caso `taxes_and_duties` cobre apenas tributos por pedido que ainda não entraram (imposto sobre a venda, taxas locais) — **jamais o imposto de importação de novo**. Registre `landed_cost_includes_duty: true` para deixar isso explícito pra Skill `offer-builder` e pra Skill `ad-analysis`.

Fluxo de atualização:
- Se `offer-builder/dados.json` já existe com `cogs_estimated: true` → atualize as linhas da tabela acima com os custos reais, recalcule unit economics/AOV/PSM e regrave (a Skill `offer-builder` define as fórmulas; os inputs vêm daqui). Remova `cogs_estimated` só quando as 4 linhas de domínio do sourcing estiverem fechadas.
- Se a Skill `offer-builder` ainda não rodou → ela lê `sourcing/dados.json` no pré-flight e nasce com COGS real (sem estimativa).
- O **preço-alvo declarado à fábrica** (ETAPA 4, bloco 4) e o COGS da `offer-builder` são o mesmo número visto dos dois lados: se a cotação voltar acima do alvo, é a oferta que precisa mudar (preço, bundle, AOV), não a planilha.
