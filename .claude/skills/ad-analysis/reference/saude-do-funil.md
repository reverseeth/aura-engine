# Ad Analysis · Referência: Saúde do funil (ETAPA 6)

> 6A posição de funil pelas signatures de frequency, 6B conversão de funil com benchmarks e amostra mínima, 6C diagnóstico da página pelo espécime da copy e pelo markup audit, com a tabela de roteamento, e 6D o check de VOC insuficiente. Abra na ETAPA 6.

### ETAPA 6 — Saúde do Funil (posição + conversão)

**6A — Posição de funil** (dos Pi 2 — frequency signatures):
> Pra recomendar qual posição reforçar, puxe **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`) — diz quais formatos/ângulos servem cada posição faltante (ex: TOF → hook problem/curiosity; BOF → offer/comparison). Isso alimenta o NEXT_BATCH_IDEAS com a posição + o tipo de conceito certo.
- Todos os ads em TOF? → normal na campanha de teste da Skill `ad-strategy` (100% prospecting por construção); só vira "funil raso" quando já existe volume de warm audience acumulado sem nada convertendo ela
- Todos em BOF? → falta trazer volume novo, tá escalando sobre a mesma audience
- Distribuído em TOF + MOF + BOF? → saudável (esperado só pós-escala, quando a `scale-engine` já criou camadas)

Recomendação baseada em desbalanço:
- Falta TOF → próximo batch inclui conceitos de awareness building (hook problem, curiosity, authority)
- Falta BOF → próximo batch inclui retargeting-style (offer-focused, urgency, comparison)

**6B — Conversão de funil (diagnóstico de funil quebrado — separa criativo de página/oferta):**

Calcule, com os dados do pull (ATC, initiate-checkout, purchases) por ad E agregado da campanha:
- **Add-to-cart → compra = `purchases / add_to_cart`.** Benchmark: **20-25%** (a cada 10 ATC, ~2 compras).
- **Checkout → compra = `purchases / initiate_checkout`.** Benchmark: **40-50%** (média ~40%).

**Amostra mínima antes de decretar funil quebrado:** ≥ **10 initiate-checkouts** OU ≥ **20 ATC** agregados na campanha. Abaixo disso, taxa de funil é ruído — com checkout→compra saudável de 40%, "3 checkouts e 0 venda" acontece por puro acaso em ~1 de cada 5 criativos bons (0,6³ = 21,6%). Sem a amostra, marque a leitura como **PRELIMINAR**, NÃO sete `funnel_broken` e NÃO roteie o membro pra retrabalhar página/oferta ainda.

Leitura (com amostra suficiente):
- **Dentro ou acima do benchmark** → o funil converte; se um criativo não vende, o problema é o criativo (entra na regra de KILL).
- **Abaixo do benchmark** → o bloqueio é PÁGINA / CHECKOUT / OFERTA, não o criativo. Ex: campanha com muitos checkouts e poucas vendas → checkout→compra abaixo de 40% → a página/checkout está vazando. **Não mate criativos por isso** — eles trouxeram intenção de compra que a página desperdiçou.
- Se os dados de ATC/checkout não vierem no pull (manual ou API limitada), marque `data_gap` e diga ao membro exatamente o que olhar no Shopify/Meta pra preencher (funnel do checkout: sessions → ATC → checkout → purchase).

Roteamento quando funil quebrado: checkout→compra baixo → `'page'`/`'copy'` (página vazando) ou checkout flow; ATC→compra baixo com checkout→compra ok → oferta/preço fraco no checkout → `'offer'`. Registre o gargalo em `health_signals` e no NEXT_BATCH_IDEAS pra não repetir o erro de matar criativo bom.

**6C — Quando a página converte mal: diagnóstico pelo espécime da copy**

Quando a leitura acima aponta a **página** como gargalo (checkout→compra ou ATC→compra abaixo do benchmark, com amostra suficiente), não devolva o membro pra `copy-engine`/`page-design` com "a página converte mal". Isso não é diagnóstico e produz reescrita às cegas. A skill `copy-engine` grava em `copy-engine/dados.json` exatamente o que permite localizar a falha (carregado no Contexto, item 4b). Rode as duas perguntas, nesta ordem:

**(a) O espécime escolhido era o certo pro avatar?**
- Leia `specimen_primary` (e `specimen_secondary`, se houver) e abra a entrada correspondente em `.claude/lib/swipe-models/specimens.json`.
- Compare o `aplica_a` do espécime (`page_type` × `awareness` × `sophistication` × `vertical`) com o avatar e o awareness reais do produto (`market-research/dados.json`) e com o `page_type` que de fato foi ao ar (`page`). Traduza antes de comparar, pela correspondência fixa do `.claude/lib/swipe-models/README.md`: `listicle` conta como `advertorial`, `pdp_robust` e `pdp_lean` contam como `pdp`, e um `quiz` no ar nunca é `mismatch_page_type` (não existe espécime de quiz).
- Confira a `regra_diagnostica` do espécime: ela descreve a condição sob a qual aquela estrutura funciona. Se a condição não se sustenta no caso do membro, **a estrutura estava errada desde antes do tráfego** — nenhuma troca de criativo conserta isso.
- Grave o veredito em `page_diagnosis.specimen_fit`: `fit` · `mismatch_awareness` · `mismatch_page_type` · `mismatch_sophistication` · `mismatch_vertical` · `unknown` (quando `specimen_primary` não existir — página anterior à skill `copy-engine` atual).

**(b) Qual camada do markup audit já tinha reprovado antes do launch?**
- Leia `markup_audit`. Ele é o registro do que a auditoria de markup encontrou **antes** da página ir ao ar: os 4 U's da headline, ideal prospect, big promise, first page test, as 4 emoções, o lead de 4 passos, `defects_found` e o `verdict`.
- Se o `verdict` era `rewrite_lead`, ou se algum dos gates de headline estava em `false`, **a página subiu com um defeito conhecido** — e é ali que a investigação começa, não numa reescrita geral.
- Grave a camada que reprovou em `page_diagnosis.markup_audit_layer_failed` (ex: `four_us.unique`, `four_emotions.safe_predictable`, `makepeace_4.cred`) e liste os `defects_found` que continuam de pé.

**Roteamento com o diagnóstico na mão:**

| O que os dois checks mostram | Para onde volta |
|---|---|
| Espécime incompatível com o avatar/awareness | **06** — reselecionar o espécime (ETAPA 2.5) antes de reescrever qualquer bloco |
| Espécime certo, mas camada do markup audit reprovada | **06** — corrigir a camada nomeada (lead, headline, prova, oferta), não a página inteira |
| Espécime certo e audit limpo, checkout vazando | **`page-build`/`checkout-aov`** (página/checkout) ou **`offer-builder`** (preço/oferta no checkout) |
| `specimen_primary` ausente (`unknown`) | Registre `data_gap` e trate como diagnóstico de página comum; a copy é anterior à camada de espécime |

Isso entra no `dados.json` (`page_diagnosis`) e no `NEXT_BATCH_IDEAS.md`. **Nunca mate criativo por falha localizada aqui** — o ad trouxe a intenção de compra que a estrutura da página desperdiçou.

**6D — Check de VOC insuficiente ANTES de culpar criativo/oferta:** se `copy-engine/dados.json.voc_forced_continue: true` (carregado no Contexto, item 4b) E CTR/CVR estão abaixo do esperado (CTR baixo generalizado entre os ads, ou CVR da página abaixo do benchmark), a hipótese primária muda: **a copy rodou com VOC insuficiente** — os hooks e a página falam a língua errada porque a matéria-prima de pesquisa era rasa. Diagnóstico: "copy rodou com VOC insuficiente — re-rodar skill `market-research` com mais fontes e re-gerar a copy antes de culpar criativo ou oferta". Registre em `health_signals` como `voc_insufficient_copy` e roteie pra `market-research` → `copy-engine`, não pra `creative-engine`.
