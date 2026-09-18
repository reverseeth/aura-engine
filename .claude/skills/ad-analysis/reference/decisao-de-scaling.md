# Ad Analysis · Referência: Decisão de scaling (ETAPA 9)

> Por que escala automática não existe em CBO, o que é automatizável, os três gates (piso, escala, corte) e o texto da recomendação em cada cenário: breakthrough dentro do target, CPA muito abaixo, só KPI winner, só spend winner, só losers, CPA acima do target, funil quebrado, conta suspeita. Abra na ETAPA 9.

### ETAPA 9 — Decisão de Scaling (Recomendação Clara)

> Fundamente a recomendação puxando o sistema de scaling da base (rode a `best_query`): **Profitable Scaling Margin (PSM)** (`Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — usa o `psm_real` calculado na ETAPA 2 pra decidir agressivo/steady/breakeven/cortar. O ritmo de subida e descida é o **Scaling Protocol** do cânone `.claude/lib/ad-taxonomy/README.md` §5 (48-72h acima do target → **+20%**, depois a cada 24h; abaixo do breakeven **por 24-48h persistentes** → **−20%** — um dia ruim isolado não dispara), executado **à mão** pela Skill `scale-engine` — nunca por automação. A montagem detalhada do plano de escala (vertical + horizontal) é delegada pra skill `scale-engine`; aqui só a recomendação.

**Escala automática não existe nesta estrutura (cânone §6).** Se o membro pedir "deixa uma regra escalando sozinha", a resposta é não — e o porquê tem duas camadas independentes:

1. **Tecnicamente o Meta recusa.** Automated Rule com condição de performance (CPA, ROAS, frequency) não roda em campanha que usa CBO; o erro retornado é literalmente *"performance-related conditions are not available for assets that use CBO"*. Não ofereça, não tente criar, não prometa.
2. **Mesmo onde rodasse, seria errado.** A métrica do Ads Manager engana — um ad a 1× ROAS na plataforma pode estar excelente no 1-day click de uma ferramenta de atribuição de terceiro. Automatizar kill ou escala por metadado do painel mata winner. **Kill e escala são leitura, não regra:** quem decide o kill é esta skill (réguas do §3) e quem executa a escala é a Skill `scale-engine` (Scaling Protocol do §5).

O que É automatizável já foi montado pela Skill `ad-strategy` (ETAPA 6 dela) — confira o estado de cada item em `ad-strategy/dados.json → protections`:

- **`Ad set spending limit → daily maximum`** por ad set de teste (~3× target CPA/dia): é teto de gasto, não condição de performance, então funciona em CBO.
- **Automação obrigatória A — pico de gasto:** spend 5× em 24h → pausar.
- **Automação obrigatória B — URL errada:** destino ≠ domínio da loja → desligar o ad.

Alguma das duas rules ausente ou desativada → **essa** é a ação de automação a recomendar aqui, nunca uma rule de performance. O campo `pgs_enabled` do `ad-strategy/dados.json` é legado, fixo em `false`, e não deve ser lido como permissão pra prometer escala automática nem gravado como `true`.

> **Gate de piso (roda antes dos dois gates abaixo):** teste nascido abaixo do piso (`below_floor_directional_only: true` — PLAYBOOK item 6) não produz recomendação de escala NEM de kill: o resultado é direcional. A recomendação desta ETAPA vira "subir o budget até o piso de US$ 100-150/dia (cânone §1) ou reduzir o nº de conceitos no ar" — e o `recommended_action` gravado é `raise_budget_or_reduce_concepts`.
>
> **Gate único de escala:** só existe recomendação de escalar quando há **≥ 1 `breakthrough`**. `kpi_winner` e `spend_winner` **não** liberam escala — o primeiro não provou nada em spend, o segundo já está diluindo o KPI da campanha. A skill `scale-engine` confere isso de novo no pré-flight dela; não a mande pra lá sem breakthrough. A `scale-engine` também confere o **gate click-based** do cânone §5 lendo `manifest.click_based_purchase_share` gravado nesta análise (bloco da ETAPA 2) — sem o número, aquele gate fica bloqueado; nunca estime.

> **Gate de corte:** nenhuma recomendação desta ETAPA que reduza spend por queda de ROAS sai sem `.claude/lib/unit-economics/README.md` §4 aplicado com os custos fixos na mesa. **Fonte preferencial: `finance-engine/dados.json` → `roas_spiral`** (a `finance-engine` calcula e publica; esta skill lê pela tabela do PLAYBOOK item 5). Na ausência dela, `budget_viability.fixed_costs_monthly` do `offer-builder`. Sem os fixos em nenhuma das duas, o output é a pergunta, não a instrução.
>
> **Quando o veredito da `finance-engine` é `scale_up_accept_lower_roas`,** a recomendação desta ETAPA é subir spend até `spend_to_breakeven_with_fixed` — e ela é **independente do gate de escala acima**: não é escala de breakthrough (que exige criativo provado), é diluição de custo fixo. Diga a diferença ao membro em uma frase pra ele não confundir as duas decisões.

Baseado no diagnóstico completo, dê uma recomendação clara:

**SE existe `breakthrough` e o CPA está dentro do target:**
"Continue rodando. Não tem regra escalando sozinha, e isso é de propósito: em campanha com CBO o Meta não aceita automação por condição de performance, e decidir por metadado do painel mata winner. A subida de budget é decisão de leitura, feita à mão. Diga **'scale'** que a Skill `scale-engine` aplica o Scaling Protocol (48-72h acima do target → +20%, depois a cada 24h) e monta a promoção do breakthrough pra ad set próprio em campanha ABO paralela."

**SE CPA ≤ 0.7× target E há `breakthrough` claro:**
"Oferta forte, ads matando. Diga **'scale'** pra montar plano de escala vertical + horizontal — com esse PSM a Skill `scale-engine` pode ir mais agressiva no Scaling Protocol, sempre à mão e com a regra de reset do cânone §5 aplicada (ao ajustar budget, o novo valor sai de ~50% do que foi REALMENTE gasto, nunca do budget nominal)."

**SE só existe `kpi_winner` (nenhum breakthrough):**
"Você tem criativo batendo o KPI, mas nenhum que puxe spend — e ad que bate KPI com pouco spend ainda não provou nada em escala. Isso não é hora de escalar. Dois caminhos: (a) forçar spend num ad set próprio pra esse criativo, pra tirar a dúvida se o limite é ele ou a audiência (diga **'scale'** que eu passo pra estrutura); (b) diga **'creatives'** pra gerar conceito novo. O que **não** funciona é subir budget da campanha esperando que ele apareça."

**SE só existe `spend_winner` (nenhum breakthrough):**
"Tem criativo puxando spend, mas com KPI abaixo do da própria campanha — ele segura a conta onde está, não escala. O trabalho é iteração: diga **'creatives'** pra rodar a variação de uma variável só, com os learnings desta análise."

**SE nenhum breakthrough e nenhum sinal (só losers):**
"Você ainda não tem um ad que escala. Isso é o normal estatístico, não fracasso: o hit rate esperado de super winner é de 1-3% dos criativos testados. O próximo passo é volume com intenção (skill `creative-engine`), não budget."

**SE CPA acima do target mas ainda abaixo de 2×:**
"Não escala. Foco em iteração. Diga **'creatives'** pra gerar novo batch baseado nos learnings desta análise."

**SE CPA > 2× target após 7+ dias:**
"Bloqueio não é só ad — pode ser oferta, página, ou audience. Vou sugerir investigação: [indicar onde está o bloqueio mais provável baseado no 19-point]. Depois de ajuste, re-roda análise em mais 7 dias."

**SE funil quebrado (ETAPA 6B abaixo do benchmark):**
"Os criativos estão trazendo gente que adiciona ao carrinho e inicia checkout, mas a conversão final está abaixo do esperado ([checkout→compra X% vs 40-50% ideal]). O gargalo é a página/checkout, não o ad. [Acrescente aqui o resultado da ETAPA 6C, com o nome próprio da falha: espécime incompatível com o avatar (`page_diagnosis.specimen_fit`) ou camada do markup audit que já tinha reprovado antes do launch (`page_diagnosis.markup_audit_layer_failed`).] Antes de mexer em criativo: diga **'copy'** pra corrigir a camada específica (ou **'page'** / **'offer'** se o bloqueio for checkout ou preço)."

**SE conta suspeita (`account_cpm_suspect`):**
"O CPM está bem acima do esperado do nicho de forma generalizada — isso costuma ser a CONTA, não o produto. Antes de matar o produto, vale re-testar o mesmo criativo em outra conta de anúncio. Se quiser, monto a estrutura de teste de novo (diga **'ad strategy'**)."
