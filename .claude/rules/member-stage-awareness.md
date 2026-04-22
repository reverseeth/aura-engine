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
- Recomendações conservadoras (3-4 conceitos max, não 8-10)
- Explicar o "porquê" de cada decisão (educação embutida)
- Priorizar tools grátis/low-cost (Meta App, free tier Klaviyo, stock + AI UGC)
- Evitar scale agressivo (PGS 3%/week, não 5%)
- Linguagem: didática, sem jargão sem explicar primeira vez

### Stage 2 — Validando (30-90 dias)

**Perfil**: rodou 1-3 batches de ads, tem alguma venda mas inconsistente. Cerca de $1-5k/mês em ads. Ainda ajustando oferta.

**Sinais no manifest**:
- `stage: "validating"`
- `skills_completed.length 5-10`
- `batch_count 1-3`
- `target_cpa` existe + `breakeven_roas` calculado
- Tem `last_batch_id` mas não winner consistente

**Como skill deve se comportar**:
- Recomendações balanceadas (6-8 conceitos por batch)
- Foco em iteração: "o que aprendemos no último batch?"
- Introduzir tools intermediárias (Wetracked, creator humano 1-2)
- Skill 09 (ad-analysis) como núcleo do workflow
- PGS padrão (5%/3×week)
- Linguagem: técnica mas com context

### Stage 3 — Escalando ($5k+/mês em ads)

**Perfil**: tem winners identificados, ROAS consistente, escalando vertical+horizontal. $5-50k+/mês em ads.

**Sinais no manifest**:
- `stage: "scaling"`
- `skills_completed.length > 10`
- `batch_count 4+`
- Champions ativos (multiple winner Post IDs)
- Revenue tier 3+ atingido (Skill 10)

**Como skill deve se comportar**:
- Recomendações agressivas (10-15 conceitos, batches semanais)
- Foco em diversificação (horizontal scale, new angles, new placements)
- Tools premium (Triple Whale, Aimerce, creator humano scale)
- Skill 10 (scale-engine) como núcleo
- PGS mais agressivo ou custom automation
- Linguagem: executive, concisa, assume expertise

## Detecção automática

Toda skill ANTES de executar:

1. Ler `manifest.json`
2. Ler `profile.md` (budget + revenue disclosed)
3. Calcular stage via:
   - Se `stage` field explícito → usar
   - Senão, inferir:
     - `skills_completed < 5` AND `budget_daily < 50` → starter
     - `batch_count 1-3` AND `target_cpa set` → validating
     - `batch_count >= 4` AND `champions.length > 0` → scaling

4. Aplicar comportamento do stage pelo resto da execução

## Regras que NÃO mudam entre stages

Alguns elementos são inegociáveis em qualquer stage:

- Research foundation (Skill 04 Etapa 2.5)
- VOC traceability (Skill 07 Etapa 4.5.F)
- Compliance pre-flight
- Promise↔Config gate
- Shopify theme safety
- Logo SVG obrigatória
- Aspect ratio 9:16

Esses não relaxam pro iniciante nem aceleram pro escalador — são baseline.

## Anti-patterns (FORBIDDEN)

- Recomendar creator humano pago pra starter com $500/mês
- Recomendar só AI UGC pra scaling com $20k/mês (desperdiça margem pra custo marginal de creator humano)
- Usar tom técnico sem explicar pra starter
- Explicar tudo passo-a-passo pra scaling experiente (vira ruído)
- Ignorar stage e aplicar sempre mesmo playbook

## Update de stage

Stage pode mudar durante uso. Skill 10 (scale-engine) revisita stage a cada execução. Se membro graduou de validating → scaling, atualizar `manifest.json.stage` e avisar:

> "Você graduou de 'validating' pra 'scaling'. A partir de agora as skills vão operar mais agressivas — batches maiores, tools premium como opção, PGS automático mais ambicioso."
