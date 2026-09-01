---
name: member-stage-awareness
description: Ajusta comportamento das skills conforme o estágio do membro (iniciante vs validando vs escalando). Respostas e recomendações mudam radicalmente entre esses estágios.
paths:
  - .claude/skills/
---

# Member Stage Awareness

Aura Engine atende membros em 3 estágios bem diferentes. Mesma skill precisa adaptar tom, profundidade e recomendação conforme onde o membro está.

## Os 3 estágios

### Stage 1 — Iniciante (0-30 dias)

**Perfil**: nunca rodou ads pagos, não tem dados próprios, tá montando primeira oferta. Orçamento limitado ($300-1000/mês total em ads + tools).

**Sinais no manifest**:
- `stage: "starter"` ou ausente
- `skills_completed.length < 5`
- `budget_daily < 50`
- Sem dados de revenue no profile

**Como skill deve se comportar**:
- **Quantos conceitos sobem é conta, não preferência.** O número vem da capacidade de teste do cânone `.claude/lib/ad-taxonomy/README.md` §1 (aplicada na Skill 10 ETAPA 3.1), nunca do stage. Com budget de starter a capacidade costuma dar 1 conceito, e é comum o budget nem alcançar o piso operacional. O que o stage muda é a **apresentação**: pra starter abaixo do piso, o caminho recomendado é adiar e juntar caixa, dito sem rodeio — rodar mesmo assim dá resultado direcional, que não autoriza kill nem escala
- Explicar o "porquê" de cada decisão (educação embutida)
- Priorizar tools grátis/low-cost (Meta App, free tier Klaviyo, stock + AI UGC)
- **Escala: passo pequeno e sem improviso.** O Scaling Protocol do cânone §5 vale igual pra todo stage (gates, +20% de subida, −20% abaixo do breakeven). O que muda aqui é a tolerância a risco DENTRO dele: o starter não precisa tomar todo passo que o protocolo libera — sobe um degrau, deixa a leitura fechar, e só então considera o próximo. Sem surf, sem duplicação de campanha. A Skill 12 recomenda a Escola C (budget-doubling) como intensidade default nesse stage
- Linguagem: didática, sem jargão sem explicar primeira vez

### Stage 2 — Validando (30-90 dias)

**Perfil**: rodou 1-3 batches de ads, tem alguma venda mas inconsistente. Cerca de $1-5k/mês em ads. Ainda ajustando oferta.

**Sinais no manifest**:
- `stage: "validating"`
- `skills_completed.length 5-10`
- `batch_count 1-3`
- `target_cpa` existe + `breakeven_roas` calculado
- Tem `last_batch_id`, mas `manifest.ad_classification[]` ainda sem `breakthrough` estável (no máximo `kpi_winner`/`spend_winner` — cânone §2)

**Como skill deve se comportar**:
- **Conceitos no ar continuam saindo da capacidade** (cânone §1). Nessa faixa de budget a restrição que costuma morder é a própria capacidade: o batch da Skill 08 quase sempre traz mais conceitos do que o budget consegue ler, e o excedente entra na fila do batch seguinte em vez de diluir o teste
- Foco em iteração: "o que aprendemos no último batch?"
- Introduzir tools intermediárias (Wetracked, creator humano 1-2)
- Skill 11 (ad-analysis) como núcleo do workflow
- **Escala: passo do protocolo em sequência, ainda sem surf.** Com os dois gates verdes (48-72h acima do target e ≥60% das compras em 7-day click), pode encadear os +20% a cada 24h enquanto seguram — é a diferença prática pro starter. Escola C com o passo do protocolo é o default da Skill 12; Escola B (bid cap) entra só se o membro quiser mais controle, e sempre com a ressalva declarada de que bid caps têm problemas conhecidos
- Linguagem: técnica mas com context

### Stage 3 — Escalando ($5k+/mês em ads)

**Perfil**: tem breakthrough(s) identificado(s), ROAS consistente, escalando vertical+horizontal. $5-50k+/mês em ads.

**Sinais no manifest**:
- `stage: "scaling"`
- `skills_completed.length > 10`
- `batch_count 4+`
- Ao menos um criativo com `class: "breakthrough"` em `manifest.ad_classification[]` — KPI do ad melhor que o da CAMPANHA **e** puxando spend (cânone §2, gravado pela Skill 11, que também espelha a lista em `manifest.breakthroughs[]`). `champions[]` (Post IDs) e `winners[]` são campos legados e **não** servem como sinal de stage: nenhum dos dois distingue breakthrough de `kpi_winner`
- `12-scale-engine/dados.json.scale_phase` em `initial_scale` ou além, com as projeções 30/60/90 da Skill 12 sustentando o caixa (spend diário sustentado sem furo de cash flow)

**Como skill deve se comportar**:
- **Capacidade deixa de ser o gargalo; o batch passa a ser.** Aqui o budget costuma comportar o teto de 5 ad sets de teste do cânone §1 (abaixo de US$ 1k/dia), e a restrição que morde vira o tamanho do batch da Skill 08. O volume de criativo novo por rodada acompanha a sub-fase de escala (Skill 12 ETAPA 8), não o stage sozinho
- Foco em diversificação (horizontal scale, new angles, new placements)
- Tools premium (Triple Whale, Aimerce, creator humano scale)
- Skill 12 (scale-engine) como núcleo
- **Escala: maior apetite dentro do mesmo protocolo.** Os gates não afrouxam — o que muda é que surf e duplicação com tetos decrescentes entram na mesa (Escola A, default da Skill 12 nesse stage), a atenção vira diária, e o reset da meia-noite passa a ser rotina obrigatória todo dia que o budget for mexido. Acima de US$ 1k/dia sustentado, avaliar a graduação pra Advantage+ Sales com a estrutura de teste virando sandbox de criativo
- Linguagem: executive, concisa, assume expertise

## Detecção automática

Toda skill ANTES de executar:

1. Ler `manifest.json` — o sinal `budget_daily` é o campo numérico CANÔNICO de budget ($/dia), gravado pela skill 00 (setup) a partir do budget declarado pelo membro (`budget_tier` é derivado dele; ver manifest-schema.json). Manifest legado sem `budget_daily`: inferir de `budget_tier` (`starter` ≈ <$50/dia) ou da linha "Budget diário" do `profile.md`.
2. Ler `profile.md` (budget + revenue disclosed)
3. Calcular stage via:
   - Se `stage` field explícito → usar
   - Senão, inferir:
     - `skills_completed < 5` AND `budget_daily < 50` → starter
     - `batch_count 1-3` AND `target_cpa set` → validating
     - `batch_count >= 4` AND ao menos um `class: "breakthrough"` em `manifest.ad_classification[]` → scaling (fonte canônica da classificação, gravada pela Skill 11; a lista espelhada `manifest.breakthroughs[]` serve igual. **Nunca** inferir scaling de `champions[]` ou `winners[]`: são legados e podem conter `kpi_winner`, que não escala)
     - Se NENHUMA condição casa (perfil híbrido, ex: começou com budget alto) → default `starter` (comportamento mais conservador — coerente com o princípio de default seguro do emergency-escape-paths)

4. Aplicar comportamento do stage pelo resto da execução

## Regras que NÃO mudam entre stages

Alguns elementos são inegociáveis em qualquer stage:

- Research foundation (Skill 04 Etapa 2.5)
- VOC traceability (Skill 08 Etapa 4.5.F)
- Compliance pre-flight
- Promise↔Config gate
- Shopify theme safety
- Logo SVG obrigatória
- Aspect ratio 9:16
- **A capacidade de teste** do cânone `.claude/lib/ad-taxonomy/README.md` §1 — piso operacional, teto por ad set e teto de ad sets de teste valem igual em qualquer stage
- **Os dois gates de subida do Scaling Protocol** (§5) e a descida de −20% abaixo do breakeven
- **A regra de reset da meia-noite** (§5): o budget do dia seguinte é ~50% do que foi REALMENTE gasto, nunca do nominal
- **Só `breakthrough` libera escala** (§2) — `kpi_winner` e `spend_winner` não, em nenhum stage

Esses não relaxam pro iniciante nem aceleram pro escalador — são baseline.

## Anti-patterns (FORBIDDEN)

- Recomendar creator humano pago pra starter com $500/mês
- Recomendar só AI UGC pra scaling com $20k/mês (desperdiça margem pra custo marginal de creator humano)
- Usar tom técnico sem explicar pra starter
- Explicar tudo passo-a-passo pra scaling experiente (vira ruído)
- Ignorar stage e aplicar sempre mesmo playbook
- **Definir o número de conceitos do teste pelo stage** em vez da capacidade do cânone §1 — a conta manda, o stage só decide como o resultado é apresentado
- **Prometer escala ou kill automáticos por regra de performance** em qualquer stage: o Meta recusa condição de performance em campanha com CBO (cânone §6). A escala é manual, pelo Scaling Protocol da Skill 12
- **Afrouxar um gate do protocolo "porque o membro é experiente"** ou apertá-lo "porque é iniciante" — os gates são fixos; o que varia é o apetite dentro deles

## Update de stage

Stage pode mudar durante uso. Skill 12 (scale-engine) revisita stage a cada execução. Se membro graduou de validating → scaling, atualizar `manifest.json.stage` e avisar:

> "Você graduou de 'validating' pra 'scaling'. A partir de agora as skills operam com mais apetite — batches maiores, tools premium como opção, e surf e duplicação de campanha na mesa. A régua de subida continua a mesma: 48-72h acima do target e pelo menos 60% das compras em 7-day click antes de cada +20%. E toda vez que você mexer no budget, à meia-noite ele volta pra ~metade do que você REALMENTE gastou, nunca pro número que ficou na tela."
