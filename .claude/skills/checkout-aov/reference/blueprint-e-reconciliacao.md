# Checkout & AOV · Referência: Blueprint implementável e reconciliação do AOV sem contagem dupla (ETAPAs 3 e 4)

> O spec concreto de cada alavanca e a regra de ouro da reconciliação (o `aov_expected` já inclui bump e upsell), os três números, o ajuste só por diferença de escopo e a atualização condicional do target CPA no manifest. Abra na ETAPA 3.

### ETAPA 3 — Especificar cada alavanca (blueprint implementável)

Para cada alavanca ativa, produza um spec concreto e aplicável (não prosa genérica):

- **Pricing exato** com charm pricing aplicado e a âncora ("was $X / now $Y").
- **Copy real** (inglês US, direta e sem aviso pela regra 8b, sem travessão em headlines pela 8a) — bump (1 frase + benefício), upsell (2-3 frases + benefício + oferta), bundle labels (Popular/Best Value), free-shipping bar ("You're $X away from free shipping"), trust row (garantia + badges).
- **Caminho técnico** escolhido (tema / Function / extension / app) com os passos reais.
- **Onde aplicar** (qual arquivo do tema, qual setting do admin, qual painel do app).
- **Aceitação projetada** (do `offer-builder` ou benchmark da base) e impacto no AOV.

### ETAPA 4 — Reconciliar o AOV e a economics (fonte única, SEM contagem dupla)

**Regra de ouro: o `pricing.aov_expected` do `offer-builder` JÁ INCLUI bump e upsell** (a Etapa 6 do `offer-builder` soma `bump acceptance × preço` + `upsell acceptance × preço` no AOV projetado, e a `weighted_margin_per_order` é ponderada por esse AOV). O papel desta skill é **REALIZAR** essa projeção na loja, não somá-la de novo — re-adicionar as alavancas sobre `aov_expected` infla o "novo target CPA" que a Skill `ad-strategy` usaria em decisão de spend real.

Monte a reconciliação em 3 números:

- **AOV sem alavancas** (baseline de referência): recompute do `offer-builder` — o mix solo/bundle SEM os termos de bump/upsell (ou `main_sku_price` se a oferta é single-tier). Serve pra mostrar ao membro quanto o stack de checkout vale.
- **AOV projetado** (a fonte única): o próprio `pricing.aov_expected` do `offer-builder` **quando as alavancas implementadas aqui são as mesmas que o `offer-builder` projetou** — o caso normal; o delta desta skill é ≈ 0 por definição, e `manifest.target_cpa`/`breakeven_roas` do `offer-builder` continuam válidos.
- **Ajuste SÓ por diferença de escopo**: se esta skill implementa alavanca que o `offer-builder` NÃO projetou (ex: free-shipping threshold mudou o mix, ou um bump novo passou no Gate), ou DEIXA DE implementar alavanca projetada (ex: upsell ficou `not_in_offer`), recalcule o AOV/margem com os mesmos benchmarks do `offer-builder` (bump 20-35%, upsell 3-8%/8-14%) e documente item a item o que entrou/saiu do cálculo.

Se (e somente se) o ajuste de escopo mudou a economics: registre o novo `target CPA` viável (= nova margem ponderada / 2 ou / 3 — é o múltiplo do ROAS de BREAKEVEN, não ROAS literal) e atualize `manifest.target_cpa` + `manifest.breakeven_roas` quando a config for de fato aplicada — a Skill `ad-strategy` lê do manifest.

> **Não sobrescreva** `weighted_margin_per_order` no `offer-builder/dados.json` (é a fonte da unit economics). Grave a reconciliação em `checkout-aov/dados.json` e atualize `manifest.aov_baseline` se a config foi de fato aplicada na loja (não só planejada). A Skill `ad-analysis` reconcilia com o AOV real medido depois (lembrando que o valor do OTO post-purchase não entra no Purchase do pixel — ver "Quando Usar").
