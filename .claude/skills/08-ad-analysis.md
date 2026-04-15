---
name: ad-analysis
description: Engine de análise de performance de ads. Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "como estão meus ads", "analisar campanha", ou quando a campanha estiver rodando e o membro quiser entender a performance.
---

# Ad Analysis Engine

## Quando Usar
Quando a campanha está rodando e o membro quer análise de performance.

## Antes de Começar
1. Leia /workspace/profile.md
2. Leia /workspace/[produto]/04-offer.md (CPA target, breakeven ROAS)
3. Leia /workspace/[produto]/07-ad-strategy.md (estrutura, regras de decisão)
4. Leia análises anteriores em /workspace/[produto]/08-analysis/ (se existirem — pra comparar evolução)
5. Consulte a base Aura (deep=true):
   - "4Pi analysis spend frequency CPM cost per result diagnostic"
   - "4Pi dashboard setup custom metrics"
   - "creative fatigue signals CPM rising CTR falling"
   - "aplicacao learnings novos ads"
   - "winning ad rate hit rate"
   - "when turn off 3-2-2 when leave running"
   - "budget scaling methods when to scale"
   - "ad formats funnel position video image"

## Fluxo da Skill

### ETAPA 1 — Receber Dados

Diga ao membro (uma única mensagem):

"Cola os dados do Ads Manager aqui — screenshot ou números. Preciso ver por ad set: Spend, Frequency, CPM, CPC, Cost per Purchase, ROAS. E quantos dias cada ad set está rodando."

ESPERE a resposta antes de prosseguir. Se o membro enviar dados incompletos, peça só o que faltou — não re-explique a pergunta.

### ETAPA 2 — 4Pi Analysis

Consulte a base Aura: "4Pi analysis spend frequency CPM cost per result" (deep=true)

Analise na ordem EXATA do 4Pi:

**1. SPEND — O que a máquina quer investir:**
- Qual ad set está recebendo mais spend? Isso é o que Meta acredita que funciona.
- Algum ad set NÃO está recebendo spend? Isso é feedback: Meta não acredita nesse criativo.
- Se um novo ad set entrou e roubou spend de um existente → o novo pode estar ganhando

**2. FREQUENCY — Pra quem está mostrando (posição no funil):**
- Frequency diária < 1.10 = prospecting (topo de funil)
- Frequency diária moderada = mid funnel
- Frequency diária alta = retargeting (fundo de funil)
- Todos os ads com frequency similar? = falta diversidade de funil

**3. CPM — Qualidade da experiência:**
- CPM alto + frequency alta = fundo de funil (audiência quente, competição alta)
- CPM baixo + frequency baixa = topo de funil (audiência ampla, barata)
- CPM subindo com o tempo no mesmo ad = possível fadiga criativa

**4. COST PER RESULT — Eficiência:**
- Dentro do CPA target → saudável
- Acima do target mas abaixo de 2x → monitorar
- Acima de 2x o target → problema

### ETAPA 3 — Diagnóstico

Com base no 4Pi, identifique:

**Criativos winners:**
- Recebem spend naturalmente
- CPA dentro ou abaixo do target
- Métricas estáveis ou melhorando
- AÇÃO: manter, considerar promover pra champions

**Criativos em fadiga:**
- CPM subindo, CTR caindo, Frequency subindo
- Spend pode ainda estar alto (inércia) mas CPA degradando
- AÇÃO: preparar substituição, não cortar imediatamente

**Criativos losers:**
- Pouco ou nenhum spend após 7 dias
- OU: receberam spend mas CPA consistentemente acima de 2x target
- AÇÃO: pausar

**Problemas de funil:**
- Todos os ads na mesma posição de funil → falta diversidade
- AÇÃO: adicionar formato diferente (se tudo é vídeo → testar imagem, ou vice-versa)

### ETAPA 4 — Recomendações de Ação

Entregue recomendações específicas e acionáveis:

"Baseado na análise:

**Ações imediatas (faça hoje):**
- [ex: Pause o ad set Batch #2 — 0 spend em 8 dias, criativo não ressoou]
- [ex: Mantenha Batch #1 — CPA de $22 vs target de $25, spend crescente]

**Ações de curto prazo (próximos 3-7 dias):**
- [ex: Promova o criativo #1.2 pro champions com post ID]
- [ex: Prepare novo batch testando ângulo de resultado — gaps do competitor analysis sugerem oportunidade]

**Ações de médio prazo (próximas 2-4 semanas):**
- [ex: O account está bottom-heavy — todos os ads em frequency 1.5+. Adicione vídeo UGC pra ampliar topo de funil]

**Sobre scaling:**
- Se CPA dentro do target → a regra PGS está escalando automaticamente, não toque
- Se CPA abaixo do target E tem winning ad claro → pode escalar mais agressivamente (consulte a base Aura: "when to scale aggressively reasons")
- Se CPA acima do target → NÃO escale, foque em novos criativos"

### ETAPA 5 — Learnings pra Próximo Batch

Consulte a base Aura: "aplicacao learnings novos ads"

Documente o que aprendemos:
- Qual conceito funcionou? Por quê?
- Qual formato performou melhor? (vídeo vs imagem)
- Qual hook teve melhor CTR?
- Qual primary text teve melhor conversão?
- Qual ângulo ressoou mais?

"Esses learnings vão alimentar o próximo batch de criativos. Quando quiser criar novos criativos, diga 'creatives' e eu vou usar esses insights."

### SALVAR

Salve em: /workspace/[produto]/08-analysis/[data]-analysis.md

Ao final diga: "Análise completa. Execute as ações recomendadas. Volte em 3-7 dias pra nova análise, ou diga 'creatives' pra gerar o próximo batch baseado nos learnings, ou 'scale' se quiser montar um plano de escala."
