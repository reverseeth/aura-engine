# Ad Analysis · Referência: Playbook, a camada de execução (decisão de kill real)

> Os seis itens que mandam em toda decisão de matar, manter ou cortar: os dois cânones, as três réguas de kill, CPM como saúde da conta, benchmarks de funil, as 4 classes, a espiral do ROAS (com a tabela de veredito da `finance-engine`) e o teste abaixo do piso como resultado direcional. Abra antes de classificar ou recomendar corte.

## PLAYBOOK — A camada de execução (decisão de KILL real)

A base Aura tem a TEORIA da leitura (4Pi, PSM). Este playbook é a camada de EXECUÇÃO operacional — exatamente o que decidir olhando o Ads Manager. Quando o playbook e a leitura teórica conflitam numa decisão de matar/manter criativo, **o playbook manda na decisão**; o 4Pi/PSM continuam como o RACIOCÍNIO que explica o porquê. E quando o playbook diverge de um dos dois cânones do item 0 abaixo, **o cânone vence** — esta skill aplica, não redefine.

> Os números de referência vêm de `offer-builder/dados.json`: `breakeven_cpa` = `unit_economics.weighted_margin_per_order`, e `target` = `unit_economics.target_cpa_primary_2x` (é ele que entra na régua de 8× de conta nova). Toda regra abaixo é relativa a ESSES números, nunca a um valor fixo.

> Se existe `competitor-analysis/dados.json` com `monitoring_radar[]` (ETAPA 3E da Skill `competitor-analysis`), releia a cada análise: cheque se algum `trigger_signal` disparou (concorrente escalando ângulo novo, entrante no formato, rede de afiliado acelerando) e, se sim, informe o membro com a `action_if_triggered` correspondente.

**0. Os dois cânones que governam esta skill (leia antes de classificar ou recomendar corte):**
- **`.claude/lib/ad-taxonomy/README.md`** — fonte única da classificação (§2, as 4 classes), das réguas de kill (§3) e das fórmulas de Hook/Hold (§4). Esta skill **mede e aplica**; não redefine nenhuma tabela localmente.
- **`.claude/lib/unit-economics/README.md`** — fonte única de margem, CPA/CAC e da **espiral do ROAS** (§4). Nenhuma recomendação de **cortar spend** por queda de ROAS sai desta skill sem passar por lá.

**1. Regra de KILL de criativo (as três réguas do cânone §3 — CPA manda, não CTR):**

A régua antiga ("gastou 1-2× o breakeven CPA sem venda → pausa") **saiu**: ela mata cedo por ruído. Com CPA saudável, a chance de **zero** vendas ao gastar exatamente 1× o CPA é ≈ 37% (≈ 14% em 2× CPA) — é o mesmo raciocínio de amostra mínima que a ETAPA 6B já aplica ao funil. Matar ali descarta criativo bom por acaso estatístico.

As réguas que valem, por contexto (cânone `.claude/lib/ad-taxonomy/README.md` §3):

| Situação | Régua |
|---|---|
| **Conta madura** (já tem breakthrough rodando) | kill no nível do **AD SET**, após **7 dias sem spend E sem KPI** — abre espaço, não persegue criativo individual |
| **Conta nova** (nenhum breakthrough ainda) | kill do ad que gastou **≥ 8× o target CPA sem nenhuma purchase** |
| **Ad novo overspendando** | **esperar 24-48h** antes de qualquer decisão — o Meta frequentemente corrige o pacing sozinho |

- **CTR alto sem venda não salva o criativo.** Scroll-stop ótimo e CTR alto não pagam a conta; a compra paga. Mas a decisão de matar é pelas réguas acima, não pelo CTR nem por 1-2× breakeven.
- **Nunca julgue por dia isolado.** A leitura é por **média** da janela, não pelo pior dia.
- **Exceção — 2+ checkouts no comecinho:** se o criativo já gerou 2+ initiate-checkouts (mesmo sem venda fechada), o Meta tem sinal pra otimizar. Deixa rodar mais antes de qualquer kill.
- **Produto já validado** (outro criativo já vende): a conta é madura → a régua é a do ad set, não a do ad individual. Criativo novo sem spend e sem KPI simplesmente não sobrevive à limpeza dos 7 dias.
- **Antes de qualquer kill:** cheque funil quebrado (item 3 abaixo) e conta suspeita (item 2). Ad que trouxe checkout que a página desperdiçou não é loser.

**2. CPM = sinal de saúde da CONTA (não do produto):**
- O MESMO produto/criativo pode dar **CPM $30 numa conta e $100 noutra.** CPM alto demais geralmente é a conta, não o produto.
- Antes de declarar um produto "morto" por CPM alto, **testar o mesmo produto/criativo em OUTRA conta de anúncio.** Só depois de não validar em conta nenhuma é que se mata o PRODUTO.
- Isso muda a ordem da decisão: CPM muito acima do esperado do nicho → primeiro suspeitar da conta (resiliência: ter conta reserva legítima ajuda aqui), não do criativo.

**3. Benchmarks de funil (diagnóstico de funil quebrado — separa criativo de página/oferta):**
- **Add-to-cart → compra = 20-25%** (a cada 10 ATC, ~2 compras fecham).
- **Checkout → compra = 40-50%** (média ~40%; iniciou checkout e finalizou).
- **Abaixo desses números = o bloqueio é funil/página/oferta, NÃO necessariamente o criativo.** Ex: criativo trouxe 3 checkouts e 0 venda → sinal de página/checkout, não do ad. Mas atenção à amostra: 0 venda em 3 checkouts acontece por puro acaso ~1 vez em 5 mesmo com funil saudável — só decrete "funil quebrado" com a amostra mínima da ETAPA 6B. Não mate o criativo por algo que é culpa da página.
- Esse cruzamento evita o erro caro de matar um criativo bom porque a página converte mal.

**4. Classificação = as 4 classes do cânone (o falso positivo que essa skill produzia):**
- A pergunta que separa um criativo que escala de uma ilusão **não** é "o CPA dele bateu o alvo?". É **"o KPI deste AD é melhor que o KPI da CAMPANHA — e ele puxa spend?"**. Só quando as duas coisas são verdadeiras existe **breakthrough**.
- **Ad que bate o KPI com pouco spend não é winner.** Ele não provou nada em escala; o KPI bonito veio de amostra pequena. Essa classe (`kpi_winner`) é **tratada como loser para efeito de decisão** — não escala (skill `scale-engine`), não recicla (skill `content-recycler`).
- Definições completas, destinos e benchmarks: `.claude/lib/ad-taxonomy/README.md` §2. Esta skill mede os números e aplica; não redefine as classes.

**5. Antes de recomendar CORTAR spend (a espiral do ROAS):**
- Queda de ROAS **não** autoriza, por si só, recomendar corte de spend. Cortar pode **aumentar** o prejuízo: os custos fixos não encolhem junto, então sobra menos receita para diluir a mesma base fixa.
- Rode `.claude/lib/unit-economics/README.md` §4 antes de escrever qualquer recomendação de redução. **Se os custos fixos mensais do membro não forem conhecidos, a recomendação vira pergunta** ("quanto você tem de custo fixo por mês?"), nunca instrução de cortar.
- **Se `finance-engine/dados.json` existir (Contexto, item 4d), o gate deixa de ser só bloqueio e vira número.** A `finance-engine` já rodou a conta com o custo fixo dentro e publicou o resultado; leia e aplique, sem recalcular:

  | `roas_spiral.verdict` da `finance-engine` | O que esta skill recomenda |
  |---|---|
  | `cut_spend_below_variable_breakeven` (`cut_spend_recommendation_allowed: true`) | **Cortar é certo** — cada dólar a mais destrói margem de contribuição. Vale a régua de descida do `ad-taxonomy` §5 (−20%, só com breakeven furado **por 24-48h persistentes** — um dia ruim isolado não dispara) |
  | `scale_up_accept_lower_roas` | **Cortar aumentaria o prejuízo.** A saída é **subir** spend aceitando ROAS menor, até o `spend_to_breakeven_with_fixed` que a `finance-engine` calculou |
  | `covers_fixed_costs` | **Segurar.** A operação cobre o fixo no nível de spend atual; não há corte a recomendar por queda de ROAS |
  | `blocked_pending_fixed_costs` | Fallback: volta a valer o bloqueio acima — a recomendação é a pergunta |

  Use `breakeven_roas_with_fixed` como a régua contra a qual o ROAS observado é comparado (o breakeven de variável sozinho não enxerga o fixo), e cite `spend_to_breakeven_with_fixed` como o número da ação quando o veredito for subir spend.
- **Sem o arquivo da `finance-engine`, nada muda:** vale o comportamento de hoje (item 4c), com a recomendação virando pergunta enquanto os fixos forem desconhecidos.
- Isso vale pra ETAPA 8 (ações), ETAPA 9 (scaling) e pro `recommended_action` gravado no `dados.json`.

**6. Teste que nasceu abaixo do piso = resultado DIRECIONAL (gate do cânone §1):**
- Se `ad-strategy/dados.json → test_capacity.below_floor_directional_only` é `true`, o teste rodou abaixo do piso operacional de US$ 100-150/dia e o dado não sustenta decisão formal. Esta skill **diz isso ao membro com todas as letras**, trata TODA a leitura como direcional, **não classifica formalmente (sem `ad_class`), não autoriza kill (de criativo, ad set ou produto) nem escala** — a recomendação vira uma de duas: **subir o budget até o piso** OU **reduzir o nº de conceitos no ar** (o excedente entra na fila do próximo batch). `binding_constraint` diz qual restrição apertou o teste (Contexto, item 4f).
- **Fallback legado:** `test_capacity` ausente (estratégia gravada antes do campo existir) → siga o comportamento normal; se `test_budget_daily` existir e estiver abaixo de US$ 100/dia, aplique este item do mesmo jeito — é a mesma régua do cânone §1, verificada à mão.
