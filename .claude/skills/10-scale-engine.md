---
name: scale-engine
description: Engine de planejamento de escala vertical (PGS + aggressive quando apropriado) e horizontal (canais complementares — Google Search, TikTok, Amazon), com análise de prontidão (PSM > 1.2, winning ads estáveis, pipeline criativo), projeções realistas 30/60/90, cenário pessimista, e checklist operacional semanal. Use quando o membro disser "scale", "escalar", "plano de escala", "crescer", "maximizar", ou quando os ads estão estáveis e quer aumentar spend. A skill aplica "More Better New" (Hormozi) — maximizar o que funciona antes de abrir canal novo.
---

# Scale Engine

## Quando Usar
Quando o membro tem campanha rodando com performance dentro/abaixo do target, quer aumentar spend de forma sistemática, e precisa saber se tá pronto pra escalar OU quais bloqueios resolver primeiro. Esta skill é também quando o membro quer abrir canais novos (horizontal scale).

## Antes de Começar

### Pré-flight
- [ ] `08-ad-strategy.json` + `09-analysis-latest.json` existem (`/workspace/[produto]/09-analysis/latest.json`)
- [ ] Manifest tem `09-ad-analysis` em `skills_completed`
- [ ] `psm_real` foi calculado em ≥ 1 análise recente (senão, rodar 09 primeiro)

### Contexto a carregar

1. Leia `/workspace/profile.md` (budget atual — define ponto de partida)
2. Leia `/workspace/[produto]/04-offer.md` (PSM projetado — validar se a oferta sustenta escala)
3. Leia `/workspace/[produto]/08-ad-strategy.md` (estrutura atual, PGS configurado?)
4. Leia TODAS as análises em `/workspace/[produto]/09-analysis/` em ordem cronológica (pra ver trajetória real de performance e winning ads estáveis) + `latest.json` (handoff da skill 09)
5. Leia scale plans anteriores em `/workspace/[produto]/10-scale/` (se existir — comparar premissas com realidade)
6. Consulte a base Aura extensivamente sobre: mentalidade de escala (farmer vs hunter mindset, Andromeda pensar maior), budget scaling methods (5% rule, aggressive 50% trade, business-led operator), Profitable Scaling Margin (PSM — golden ratio of growth), Performance Gate Scaling (PGS completo), creative diversity como mecanismo de escala, hero offer e best customer (segundo Scale), funnel creative playbook (Olympic Rings — cobertura de posições de funil ao escalar), revenue-tier scaling model (o que otimizar em cada tier — starter / $100-500 / $500-1K / $1K-5K / $5K+), winning ad rate, More Better New (Hormozi $100M Leads — maximize → expand → diversify), ROAS Targets (vertical vs horizontal), Mentalidade de Escala (Andromeda Pensar Maior), Lead Gen Outreach (Core Four framework), canais complementares (Google Search como complemento ao FB, TikTok Shop, Amazon), e cash flow implications de escala. Aprofunde em cada framework — escala errada queima budget mais rápido que ad ruim.

### Cálculo de PSM real (vs teórico)

`psm_theoretical` vem do `04-offer.json` (baseado em AOV esperado).
`psm_real` calculado de performance ao vivo:

```python
psm_real = margin_per_unit_real / cpa_observed_avg
# Onde:
# margin_per_unit_real = AOV_real_ultimos_30d − cogs_total (do 04-offer.json)
# cpa_observed_avg = sum(spend_30d) / sum(conversions_30d)
```

Se `|psm_real − psm_theoretical| / psm_theoretical > 0.2` (desvio > 20%):
- **psm_real < psm_theoretical**: economia de oferta pior que esperada; PAUSE escalada, revisar offer
- **psm_real > psm_theoretical**: oferta performa melhor; pode escalar agressivamente

Atualizar `manifest.json` → `psm_real` após cada cálculo.

## Fluxo da Skill

### ETAPA 1 — Receber Panorama Atual

Peça ao membro em UMA única mensagem:

"Me dá o panorama atual: quanto gasta por dia, CPA médio, ROAS médio, AOV, e quantos winning ads tem rodando."

Se faltar algum número, peça só o que faltou — não re-explique.

### ETAPA 2 — Classificar Estágio de Escala

Aplicar o **revenue-tier model**:

| Spend diário | Estágio | Foco Principal | Estratégia Dominante |
|---|---|---|---|
| < $100/dia | **Fase de Teste** | Encontrar winning ads | Creative velocity, hit rate |
| $100-500/dia | **Tração** | Estabilizar e começar a escalar | PGS + refresh criativo semanal |
| $500-1K/dia | **Escala Inicial** | Escalar com controle | PGS + aggressive selectivo + creative pipeline forte |
| $1K-5K/dia | **Escala Agressiva** | Maximizar spend mantendo eficiência | PGS + aggressive + horizontal canais |
| $5K+/dia | **Otimização** | Unit economics + diversificação | CRO da página, LTV, omnichannel |

Classifique o membro. O estágio dita o que é "escalar" pra ele.

### ETAPA 3 — Análise de Prontidão (Pré-Requisitos)

Antes de aumentar spend, validar se o sistema aguenta. Falhar em qualquer um = identificar gargalo e resolver ANTES de escalar.

| Pré-requisito | Critério | Se falhar |
|---|---|---|
| **PSM > 1.2** | Da `04-offer.md` + performance real | Ajustar oferta (AOV, garantia, stack) ou pausar escala |
| **Winning ads estáveis** | Min 2-3 ads performando ≤ target por 14+ dias | Focar em hit rate (mais criativos, não mais spend) |
| **CPA estável ou melhorando** | Trend dos últimos 14 dias estável ou descendo | Diagnóstico de fadiga antes de escalar |
| **Creative pipeline ativo** | Min 1 batch novo a cada 2-4 semanas | Recomendar Skill 07 regular |
| **Pixel/CAPI health** | Match quality ≥ 80%, sem events perdidos | Fix técnico antes de escalar |
| **Cash flow pra COGS** | Membro tem $ pra produzir inventory em escala | Ajustar pace de escala ao cash flow disponível |

Pra cada pré-requisito que falha, documente o bloqueio e recomende ação específica.

### ETAPA 4 — Plano de Escala Vertical (Mesmo Canal, Mais Budget)

**PGS (Performance Gate Scaling) — Base de Tudo:**

Da Skill 08, o PGS deve estar ativo: 5% aumento 3×/semana quando CPA 7-day trailing está abaixo do target.

**Matemática**: 5% × 3 × 4 semanas = ~60% aumento mensal = duplica em ~30-40 dias sem desestabilizar.

- Se PGS já tá ativo e performando → não toque, deixa rodar. Simplesmente observe.
- Se PGS não tá ativo → configure conforme Skill 08 Etapa 8.

**Quando Escalar Aggressive (acima do PGS):**

só escalar aggressive (+25-50% de uma vez) com razão concreta:

- **Winning ad novo provado** (Post ID acumulou 1K+ impressions com CPA ≤ 0.5× target) → duplicate ad set com budget 2× pra forçar spend nele
- **Oferta nova que está outperforming** (novo bundle, novo pricing, nova garantia) → scale rápido pra capturar momento
- **LP nova que converte melhor** (test de 3-2-2-2 mostrou preferência) → mover ad sets pra essa URL
- **Evento sazonal iminente** (BFCM, Memorial Day, Mother's Day) → escala preparatória 3-4 semanas antes

Se não tem razão concreta, **não escale aggressive**. PGS é o seguro.

**Business-Led Operator Mode (pra escala > $1K/dia):**

Tier $1K+ pode considerar mode business-led: budget set baseado em **demand do negócio** (capacidade de fulfillment, cash flow, goal de revenue) em vez de PGS linear.

Exemplo: se o membro quer hit $5K/dia até fim do mês e o fulfillment aguenta, pode jogar budget agressivo direto. Mas isso exige:
- CFO-mindset (prevê cash gap entre spend e Shopify payout)
- Oferta MUITO robusta (PSM > 1.5 pra compensar flutuações)
- Creative pipeline pronto (diversidade pra não queimar audience)

### Business-Led Mode — Safeguards OBRIGATÓRIOS

Antes de autorizar budget set por "biz demand" (não por data):

**Cash flow check**:
- [ ] Float de cash disponível ≥ 1.5× daily_budget_target × payout_lag_days
  (Shopify: 3-5 dias; Stripe 2 dias)
- [ ] Cobertura de COGS pipeline: fornecedor pode entregar N units em 30/60/90 dias? Obter confirmação escrita.
- [ ] Pipeline de cartão de crédito / capital: se Meta bloquear cobrança, tem backup payment method?

**Cálculo de bridge financing**:
```
cash_gap_projected = (daily_budget × 30 × burn_multiplier) − (daily_revenue_projected × 30 × (1 − payout_lag/30))
onde burn_multiplier = 1.3 (margem de segurança)
```

Se `cash_gap_projected > 50% cash_disponivel`, **NÃO autorize** mode business-led. Voltar a mode data-led.

**Não autorizar escalada > 2× budget atual em < 7 dias** — independente de sinal.

### ETAPA 5 — Plano de Escala Horizontal (Canais Novos)

(More Better New da Hormozi): **maximize → expand → diversify**. Não abra canal novo antes de maximizar o atual.

**Critério pra abrir canal novo:**
- Meta ads escalando bem (>$1K/dia sustentável)
- Criatividade replicável (UGC style pode ser repurposed pra TikTok/IG/Shorts)
- Cash flow pra cobrir 30-60 dias de aprendizado no novo canal

**Sequência recomendada (pra ecom DTC padrão):**

1. **Meta (Facebook + Instagram)** — base. Tudo escala a partir daqui.
2. **TikTok Ads** — segundo canal natural se o produto funciona pra audience mais jovem / estética / viral potential. Creative strategy é diferente (nativo, UGC puro, trend-based). Pode acontecer em paralelo com Meta quando a marca ganha tração.
3. **Google Search (Brand + Intent)** — capturar quem já ouviu falar da marca (brand search) + intent keywords ("best [categoria]", "[problema] solution"). Muito barato e converts bem quando brand awareness existe. Roda em paralelo assim que spend Meta chegar ~$500+/dia.
4. **Amazon** (se produto permite) — canal de discovery + retargeting natural. Muda a tese do negócio (vendas não passam pelo seu Shopify). Abrir só quando o canal Shopify está forte ($3K+/dia estável).
5. **YouTube Ads** — requer criativos próprios pra format longo, good pra TOF high-volume em nichos específicos. Tier mais avançado.
6. **Email/SMS** — não é "aquisição" mas LTV. Sempre ativo em paralelo desde o primeiro cliente.

**Core Four** (Hormozi): warm outreach + cold outreach + content + ads. Em DTC o foco é ads, mas content (TikTok orgânico, UGC creators em retainer) é o que escala sustentably a longo prazo.

### Expansion para TikTok — NÃO reutilizar creatives Meta diretamente

TikTok exige native creative style:
- Vertical 9:16 obrigatório
- 3 primeiros segundos sem logo óbvio (parece orgânico)
- Legenda estilo "POV" / "story-time" / hook casual
- Trends musicais relevantes (não stock music)
- Duração sweet spot: 15-30s (vs Meta 6-15s)

**Bridge**: antes de rodar creatives em TikTok, invocar SKILL 07 novamente com flag `platform=tiktok` — skill deve re-orientar hooks + primary texts para linguagem TikTok-native. NÃO copy-paste Meta → TikTok.

### Google ads em 2026

Performance Max canibaliza Search em ecommerce (Google prioriza automation).
- **Abertura a Google**: começar com Performance Max com shopping feed
- **Search puro**: apenas para brand defense (campaigns com exato nome da marca/produto), budget pequeno
- Não replicar estratégia Meta em Search literal

### ETAPA 6 — Creative Diversity Como Motor de Escala

### Creative diversity — regra calibrada (contextual)

Antiga: "2× budget → 2× creative".

Nova (contextual, baseada em tier):
- **< $500/dia**: manter 3-5 criativos ativos (não precisa proliferar)
- **$500-$2000/dia**: 2× budget = 1.5× creative (diminishing returns)
- **> $2000/dia**: 2× budget = 2× creative (audience expansion + hedge)
- Se `frequency_max < 1.3` e CPM estável → pode manter creative count atual mesmo escalando

Regra é heurística, não lei.

Por quê: mesmo criativo rodando em $100/dia satura audience em ~30 dias. Em $500/dia satura em ~7-10 dias. Em $2K/dia satura em 3-5 dias.

**Diversificar em 3 dimensões:**

1. **Formato**: vídeo UGC + demonstração + imagem estática + carrossel + motion graphics
2. **Ângulo**: alternar entre as 3 verticais (competitiva / consumidor / interna) e entre TOF/MOF/BOF
3. **Duração/Estilo**: short-form (15s) + medium (22-30s) + long-form (45-60s pra storytelling)

**Pipeline recomendado por estágio:**

| Estágio | Novos conceitos/batch | Frequência | Creators em retainer |
|---|---|---|---|
| Teste ($<100/dia) | 3-5 | Mensal | 0 |
| Tração ($100-500) | 5-8 | A cada 3-4 semanas | 1 |
| Escala Inicial ($500-1K) | 8-12 | Quinzenal | 2-3 |
| Escala Agressiva ($1K-5K) | 12-20 | Semanal | 3-5 |
| Otimização ($5K+) | 20+ | Semanal | 5+ ou agência |

### ETAPA 7 — Projeção Realista 30/60/90

Construa cenário base + pessimista.

**Base (premissas: PGS ativo, pipeline ativo, CPA estável):**

| Mês | Spend/dia alvo | Revenue/dia (AOV × vendas) | Margem mensal estimada |
|---|---|---|---|
| Mês 1 | $[atual × 1.5-2] | $[calculado] | $[margem × 30] |
| Mês 2 | $[atual × 2-3] | $[calc] | $[margem] |
| Mês 3 | $[atual × 3-4] | $[calc] | $[margem] |

Use o PSM e AOV da `04-offer.md` pra calcular numbers realistas.

**Pessimista (CPA sobe 20%):**

Ação: pausar PGS, estabilizar com refresh criativo + possível ajuste de oferta, retomar PGS quando CPA voltar a estar dentro do target (geralmente 7-14 dias depois).

Impacto: escala atrasada ~1 mês, mas sem queimar cash flow.

### Template de projeção 30/60/90 — incluir cash flow

Modelo:

| Dia | Daily Budget | Daily Revenue | Payable (ads) | Receivable (payout +3d) | Cash Float Needed |
|-----|--------------|---------------|---------------|-------------------------|-------------------|
| 1   | $200         | $500          | -$200         | $0                      | $200              |
| 3   | $300         | $750          | -$300         | +$500                   | $300-500          |
| ... | ...          | ...           | ...           | ...                     | ...               |

Alertar se `cash_float_needed_peak > cash_disponivel * 0.7`.

### CPM escalation risk (competitivo)

Se você escala 2× em 30 dias em um vertical hot, concorrentes também escalam.
Monitorar CPM delta: se CPM subiu > 25% em 14d E sua CVR se manteve, pode ser "race to bottom".

Ação: cap escala a 1.5× por mês; diversificar com canal novo (TikTok/Google) em vez de dobrar Meta.

### ETAPA 8 — Checklist Operacional Semanal

Operação de escala sustentável exige **ritmo constante**. Documente o membro:

| Dia | Ação | Skill |
|---|---|---|
| **Segunda** | 4Pi quick check (5-10 min) | - |
| **Terça** | PGS dispara automaticamente (10 AM) | Auto |
| **Quarta** | Revisar learnings da semana anterior + preparar ideias de novo batch | - |
| **Quinta** | PGS dispara automaticamente | Auto |
| **Sexta** | **Análise semanal completa** (4Pi full + diagnóstico) | Skill 09 |
| **Sábado** | PGS dispara automaticamente | Auto |
| **Domingo** | **Preparar próximo batch** de criativos (rotacionar conceitos, produção) | Skill 07 |

**Monthly review** (1× ao mês, primeiro dia útil):
- Revisar PSM real vs projetado
- Revisar winning ad rate (% de conceitos testados que viraram winners)
- Avaliar prontidão pra próximo tier (escala inicial → agressiva → otimização)
- Decidir se é hora de abrir canal horizontal novo (Etapa 5)
- Re-rodar Skill 10 se mudanças estruturais (novo canal, novo produto, nova oferta)

### ETAPA 9 — Sinais de Alerta (Quando Parar/Ajustar)

Mesmo com PGS, pode ter que parar. Sinais:

- **CPA 7-day sobe acima do target** → PGS vai parar de disparar (sua regra já tem essa condicional). Refresh criativo antes de qualquer escala manual.
- **Frequency em todos os ad sets > 1.5** → audience saturada, precisa diversificar (novo batch)
- **CPM subindo 30%+ em 14 dias** → saturation OU competição aumentou OU ad fatigue. Investigação na Skill 09.
- **Cash flow gap** → spend > cash in (especialmente com payout 3-5 dias do Shopify e ads cobrando diário). Ajustar pace.
- **Fulfillment bottleneck** → estoque acabando, 3PL atrasando. Não escale acima da capacidade operacional.

### Quando 10 recomenda voltar para 07 (ciclo explícito)

Se algum destes sinais → invoke skill 07 para novo batch:
- Top 3 creatives têm > 14 dias de idade
- Frequency max > 1.4 com CTR caindo > 20% vs baseline
- Escala cruzou 2× budget (precisa creative diversity)
- TikTok/canal novo habilitado (precisa creative nativo)

Skill 07 lerá `NEXT_BATCH_IDEAS.md` atualizado (de 09) + `10-scale-directives.md` (novo, abaixo).

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p /workspace/[produto]/10-scale/` antes de salvar.

Outputs em `/workspace/[produto]/10-scale/`:

- `10-scale-plan.md` contendo:
  1. Classificação de estágio (Etapa 2)
  2. Análise de prontidão com bloqueios identificados (Etapa 3)
  3. Plano vertical — PGS config + critérios de aggressive (Etapa 4)
  4. Plano horizontal — sequência e critérios de abertura (Etapa 5)
  5. Creative diversity plan (Etapa 6)
  6. Projeção 30/60/90 base + pessimista + cash flow template (Etapa 7)
  7. Checklist operacional semanal (Etapa 8)
  8. Sinais de alerta (Etapa 9)

- `10-scale-directives.md` (fecha ciclo 10→07):
  - Budget atual + budget alvo (30d)
  - Canais ativos + canais a ativar
  - PSM real atual
  - Sinais que trigger volta para 07 (creative refresh)
  - Bloqueios de cash flow (se houver)

- `10-scale.json` (JSON companion):

```json
{
  "plan_id": "uuid",
  "product_slug": "...",
  "stage": "traction|initial_scale|aggressive|optimization",
  "current_daily_spend": 0,
  "target_daily_spend_30d": 0,
  "psm_real": 0,
  "psm_theoretical": 0,
  "readiness_blockers": [],
  "vertical_plan": {
    "pgs_active": true,
    "aggressive_triggers": []
  },
  "horizontal_plan": {
    "active_channels": ["meta"],
    "next_channels": []
  },
  "cash_flow": {
    "cash_gap_projected": 0,
    "safe_to_escalate": true
  },
  "triggers_back_to_07": []
}
```

### Atualizar manifest

Após salvar, atualizar `/workspace/[produto]/manifest.json`:
- Adicionar `10-scale-engine` em `skills_completed`
- Registrar `plan_id`, `psm_real`, `stage`, `active_channels`

## Mensagem Final

Adapte baseado na análise de prontidão:

**Se PRONTO pra escalar:**
"Plano de escala pronto. PGS ativo cuida da vertical. Próximos canais recomendados: [lista da Etapa 5]. Roda o checklist semanal e me volta daqui a 30 dias ou quando precisar re-rodar análise — diga **'ad analysis'** com os dados atualizados."

**Se NÃO PRONTO (algum bloqueio):**
"Identifiquei [N] bloqueio(s) que precisam resolver antes de escalar: [listar]. Ação recomendada por bloqueio:
- [Bloqueio 1] → [ação + skill]
- ...
Uma vez resolvidos, diga **'scale'** de novo que eu atualizo o plano."
