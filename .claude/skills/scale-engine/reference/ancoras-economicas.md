# Scale Engine · Referência: Breakeven, gate de custo fixo e PSM real vs teórico

> As três âncoras que toda a matemática desta skill usa: o CPA de breakeven e o `max_cpa` (fonte canônica e precedência do manifest), o gate obrigatório de custo fixo antes de cortar spend (com a tabela de veredito da `finance-engine` e o rótulo margem de contribuição vs lucro) e a leitura do `manifest.psm_real` pela base gravada (`psm_real_basis`), com a comparação de 20% contra o teórico. Abra antes de qualquer recomendação.

### Breakeven é a âncora de tudo

Toda a matemática de escala desta skill ancora no **CPA de breakeven** e no **CPA máximo** (`max_cpa` = breakeven menos a margem de lucro desejada — é o setpoint do cost cap/bid cap, **distinto** dos `target_cpa_primary_2x/3x` da Skill `offer-builder`, que são alvos de múltiplo de ROAS; o `max_cpa` é dirigido pelo lucro que o membro quer por pedido). **Fonte canônica do breakeven CPA (a MESMA das Skills `ad-strategy` e `ad-analysis`):** `offer-builder/dados.json.unit_economics.weighted_margin_per_order`. Use esse campo direto, não re-derive. **Pós-07d:** se `manifest.target_cpa`/`manifest.breakeven_roas` existirem, eles carregam o recálculo mais recente (a `offer-builder` grava; a `checkout-aov` atualiza quando as alavancas de checkout aplicadas mudaram a economics) — prevalecem sobre os valores do `dados.json` do `offer-builder`, mesma precedência que a Skill `ad-strategy` aplica. A performance real vem do `ad-analysis/dados.json`. Não invente — leia. Se faltar, pegue na ETAPA 1.

### Custo fixo antes de cortar spend (gate obrigatório — cânone unit-economics §4)

Breakeven CPA, ROAS e PSM enxergam custo **variável**. Nenhum deles enxerga o **custo fixo** (time, apps, ferramentas, aluguel, retainer de creator). Por isso, **antes de emitir QUALQUER recomendação de cortar spend motivada por queda de ROAS**, aplique `.claude/lib/unit-economics/README.md` §4 — a espiral do ROAS:

> Cortar spend pra "recuperar o ROAS" costuma **aumentar** o prejuízo, porque o custo fixo não encolhe junto. Sobra menos receita pra diluir a mesma base fixa. A reação certa às vezes é o contrário: **aumentar** spend aceitando ROAS menor, porque mais volume dilui melhor o fixo.

Como a skill `scale-engine` opera esse gate:

- **Com `finance-engine/dados.json` (fonte preferencial):** a conta já foi rodada pela `finance-engine`, e o veredito dela **decide** — esta skill não decide localmente. Leia `roas_spiral.cut_spend_recommendation_allowed` e `roas_spiral.verdict` e grave `fixed_cost_gate` conforme o mapa:

  | `roas_spiral` da `finance-engine` | `fixed_cost_gate.roas_cut_recommendation` | O que a skill recomenda |
  |---|---|---|
  | `cut_spend_recommendation_allowed: true` (verdict `cut_spend_below_variable_breakeven`) | `cleared` | Corte autorizado — cada dólar a mais destrói margem de contribuição |
  | `verdict: "scale_up_accept_lower_roas"` | `blocked_by_roas_spiral` | **Não cortar.** A saída é subir spend até `roas_spiral.spend_to_breakeven_with_fixed`, aceitando ROAS menor |
  | `verdict: "covers_fixed_costs"` | `not_applicable` | Segurar — a operação cobre o fixo no nível de spend atual |
  | `verdict: "blocked_pending_fixed_costs"` | `blocked_pending_fixed_costs` | Fallback: vale o gate local abaixo |

- **Fixos conhecidos, sem a `finance-engine`** (o membro informou o custo fixo mensal direto aqui) → rode a conta com eles na mesa e recomende o que o resultado disser, mesmo quando o resultado for subir spend com ROAS menor.
- **Fixos desconhecidos** → a recomendação **vira pergunta, não instrução**: "quanto você tem de custo fixo por mês (time, apps, ferramentas, aluguel)?". Sem esse número, a skill **não manda cortar** por queda de ROAS. Registre `fixed_cost_gate.roas_cut_recommendation: "blocked_pending_fixed_costs"` no `dados.json` e diga isso no relatório — e ofereça rodar `'finanças'` (skill `finance-engine`), que fecha essa conta e devolve o número.
- **Isto não afasta a descida do cânone de escala:** CPA/ROAS **abaixo do breakeven por 24-48h persistentes** dispara o −20% do `ad-taxonomy` §5 do mesmo jeito (um dia ruim isolado não dispara) — ali cada pedido novo destrói margem de contribuição, e o fixo não muda essa conta. O gate governa o corte motivado por ROAS que caiu mas **ainda paga o variável**.
- **Rótulo obrigatório em todo output** (unit-economics §1): número que não subtraiu custo fixo é **margem de contribuição**, nunca "lucro". Se os fixos não foram informados, escreva isso em vez de omitir.

### PSM real (vs teórico) — LER, não recalcular

`psm_theoretical` vem do `offer-builder/dados.json` (baseado em AOV esperado).
`psm_real` é gravado SOMENTE pela skill `ad-analysis` a partir de performance real. A skill `scale-engine` **LÊ `manifest.psm_real` + `manifest.psm_real_basis`** — fonte canônica — e **NUNCA recalcula** com outra fórmula.

Fórmula canônica (referência, calculada pela `ad-analysis`): `PSM = LTV / (CAC_real + COGS)`, onde `CAC_real` = ad spend do período ÷ clientes NOVOS do período (Shopify) e COGS é o somatório de `offer-builder/dados.json.cogs_breakdown` (não existe campo `cogs_total`).

**A base do número decide se a comparação vale — `manifest.psm_real_basis`:**
- **`"shopify_new_customer"`** — o denominador é o CAC real (ad spend ÷ clientes NOVOS do Shopify). É a ÚNICA base em que a comparação `psm_real` vs `psm_theoretical` (tolerância de 20%, abaixo) é válida — o teórico da `offer-builder` usa CAC.
- **`"platform_cpa_proxy"`** — o CPA de plataforma entrou como proxy do CAC. O número está **declaradamente otimista** (CPA de plataforma mistura recompra e atribuição inflada no denominador) e **não libera escala**: a comparação de 20% não se aplica nessa base. A skill exibe o motivo ao membro e **pede o CAC real** (ad spend do período ÷ clientes novos no Shopify, `new customer = TRUE`) — com o número na mão, re-rodar a `ad-analysis`, que regrava `psm_real` na base certa.
- **Campo ausente** (análise antiga da `ad-analysis`, produto legado) → **tratar como `platform_cpa_proxy`**: mesma régua, mesmo pedido de CAC real.

**Frameworks pra interpretar PSM (rode antes de decidir):**
- **Profitable Scaling Margin (PSM) — golden ratio** (rode `Profitable Scaling Margin PSM golden ratio LTV CPA COGS formula`) — a fórmula canônica e por que ela manda
- **PSM Scaling Thresholds** (rode `PSM thresholds 1.3 aggressive 1.1 healthy breakeven zone scaling decision`) — `≥1.3` escala agressivo, `~1.1` saudável (escala medido), perto de breakeven = não escala
- **Scaling Mindset Farmer vs Hunter (Andromeda)** (rode `scaling mindset farmer vs hunter Andromeda think bigger clarity not volume`) — qual mentalidade aplicar ao número do PSM

Compare `manifest.psm_real` contra `psm_theoretical` — **somente com `psm_real_basis: "shopify_new_customer"`** (proxy ou campo ausente: não compara nem libera; ver bloco da base acima). Se `|psm_real − psm_theoretical| / psm_theoretical > 0.2` (desvio > 20%):
- **psm_real < psm_theoretical**: economia de oferta pior que esperada; **NÃO escale** (nem o passo do protocolo, nem surf), revisar offer primeiro
- **psm_real > psm_theoretical**: oferta performa melhor que o esperado; pode escalar mais agressivo dentro do protocolo (teto de custo mais alto quando houver, surf mais ousado)

Use os **PSM Scaling Thresholds** como teto de agressividade: mesmo com `psm_real > psm_theoretical`, se o `psm_real` absoluto está perto de 1.0 (breakeven zone), escala só medido — margem fina não aguenta surf 10×.

Se `manifest.psm_real` estiver ausente, rode a skill `ad-analysis` primeiro (quem o grava) — não estime aqui.
