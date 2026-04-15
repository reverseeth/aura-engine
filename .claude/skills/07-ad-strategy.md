---
name: ad-strategy
description: Engine de estratégia e estrutura de campanha no Meta Ads. Use quando o membro disser "ad strategy", "estratégia de ads", "montar campanha", "estrutura de campanha", ou quando os criativos estiverem prontos e o membro quiser lançar no Meta.
---

# Ad Strategy Engine

## Quando Usar
Quando os criativos estão prontos e o membro precisa da estrutura de campanha pra lançar no Meta.

## Antes de Começar
1. Leia /workspace/profile.md (orçamento diário é CRUCIAL)
2. Leia /workspace/[produto]/04-offer.md (unit economics, CPA target, breakeven ROAS)
3. Leia /workspace/[produto]/06-creatives/ (quantos conceitos, quais formatos)
4. Consulte a base Aura (deep=true):
   - "scientific method meta ads control variable testing"
   - "one campaign method AndroMeta one architecture CBO"
   - "3-2-2 flexible ads format rules setup"
   - "andromeda system what changed meta why"
   - "budget scaling methods 5% aggressive business led"
   - "performance gate scaling PGS automated rules"
   - "4Pi analysis spend frequency CPM cost per result"
   - "ROAS targets scaling vertical horizontal"
   - "ad account pixel dataset setup CAPI"
   - "minimum daily spend why bad ads generate spend"
   - "naming convention campaigns ad sets"
   - "hero offer best customer second scale"

## Fluxo da Skill

### ETAPA 1 — Verificar Pré-Requisitos

Pergunte em UMA única mensagem:

"Antes de montar a campanha, confirma: Pixel + CAPI funcionando? Produto ativo na loja? Criativos prontos? Me diz 'sim' ou o que ainda falta."

Se o membro responder "sim" (ou equivalente) → vai direto pra ETAPA 2.

Se o membro disser o que falta, aponte como resolver:
- Pixel/CAPI não funcionando → instrua como verificar no Events Manager do Meta e como instalar CAPI via Shopify/Gateway
- Produto não ativo → pede link do Shopify ativo
- Criativos não prontos → redireciona pra skill 06 (creatives)

Não prossiga pra ETAPA 2 enquanto os 3 itens não estiverem ok.

### ETAPA 2 — Estrutura de Campanha

Consulte a base Aura: "one campaign method AndroMeta architecture" e "scientific method control variable"

Monte a estrutura baseada no One Campaign Method:

**Uma campanha CBO.** Objetivo: Purchase (ou Lead se aplicável). Advantage+ placements. Broad targeting (18-65+, sem exclusões de audiência).

**Ad Sets:**

1. **Champions Ad Set** (se o membro já tem ads que vendem):
   - Post IDs dos melhores ads existentes
   - Esse é o control — representa "isso é o que bom se parece"
   - Se o membro está começando DO ZERO: não tem champions. Pule pro ad set 2.

2. **Creative Batch #1** (variable):
   - Um 3-2-2 flexible ad por conceito
   - Cada conceito = 1 ad set
   - Se tem 3 conceitos da skill 06 → 3 ad sets de batch

3. **Page Test Ad Set** (opcional — se tiver mais de uma LP):
   - Mesmos criativos do batch, mas com URL diferente
   - Permite testar qual jornada converte melhor

**Cálculo de ad sets máximos:**
Budget diário / CPA target = máximo de ad sets
Exemplo: $100/dia com CPA target de $25 = 4 ad sets máximo

Se o membro tem mais conceitos que ad sets possíveis, priorize os mais fortes e guarde os outros pro batch #2.

### ETAPA 3 — Configuração Detalhada

Forneça instruções STEP-BY-STEP de como configurar no Meta Ads Manager:

**Nível de Campanha:**
- Nome: [Naming convention — consulte a base Aura: "naming convention campaigns"]
- Objetivo: Purchase
- Campaign Budget Optimization: ON
- Budget diário: $[do profile.md]
- Advantage Campaign Budget: ON

**Nível de Ad Set (pra cada ad set):**
- Nome: [formato de naming — ex: "CBO_US_All_18-65_ConceptName_Batch01"]
- Conversão: Purchase
- Pixel: [confirmar qual]
- Placements: Advantage+
- Targeting: broad (18-65+, localização, sem interests nem lookalikes)
- Sem exclusões de audiência (engajamento positivo de audiências conhecidas ajuda CPMs)
- Daily minimum: NÃO definir (a menos que o membro insista — consulte a base Aura sobre min/max)
- Daily maximum: NÃO definir

**Nível de Ad (pra cada 3-2-2):**
- Formato: Flexible Ad
- 3 criativos (upload)
- 2 primary texts (colar da skill 06)
- 2 headlines (colar da skill 06)
- URL de destino (PDP ou LP conforme briefing)
- CTA button: Shop Now (ou o mais adequado)
- NÃO testar descriptions

### ETAPA 4 — Regras de Decisão

Consulte a base Aura: "when turn off 3-2-2" e "when leave running" e "how long test creatives"

Monte a tabela de decisão:

**Pós-lançamento — Timeline de decisão:**

| Dia | Ação |
|-----|------|
| Dia 1-3 | NÃO TOQUE EM NADA. Deixe rodar. |
| Dia 3 | Check rápido: algum ad set recebeu spend? Se nenhum spend → problema de criativo, não de estrutura |
| Dia 7 | Primeira análise real. Ad set com spend e CPA acima de 2x target → considere pausar. Ad set sem spend → pause. Ad set com spend e CPA dentro do target → mantenha. |
| Dia 14 | Se ad set ainda não perform → pause definitivamente. |

**Critérios de winner:**
- Ad set ganhou spend naturalmente (Meta direcionou budget pra ele)
- CPA dentro do target OU campanha inteira melhorou com ele ativo
- A pergunta certa NÃO é "esse ad tem bom CPA?" — é "a campanha inteira ficou melhor?"

**Critérios de loser:**
- Não recebeu spend em 7 dias
- Recebeu spend mas CPA consistentemente acima de 2x target após 7 dias
- A campanha piorou quando ele foi adicionado

### ETAPA 5 — PGS (Performance Gate Scaling)

Consulte a base Aura: "performance gate scaling PGS automated rules 5% compounding"

Configure regra automatizada de scaling:

"Crie uma regra automatizada no Meta Ads Manager:
- Nome: PGS - [Produto]
- Condição: Se CPA dos últimos 7 dias < $[CPA target]
- Ação: Aumentar budget em 5%
- Frequência: 3x por semana (Segunda, Quarta, Sexta)
- Aplicar a: campanha

Isso = budget dobra a cada ~30 dias de forma previsível e composta.

NÃO escale manualmente a menos que tenha motivo específico (winning ad novo que explodiu). Se performance piorar, a regra simplesmente para de disparar — o budget para de subir sozinho."

### ETAPA 6 — Próximos Batches

Explique ao membro:

"Essa estrutura está pronta. Nos próximos dias:
1. Monitore usando 'ad analysis' (skill 08) a cada 3-7 dias
2. Quando um ad set for winner → promova os post IDs pro champions ad set
3. Quando um ad set for loser → pause e prepare o próximo batch
4. O próximo batch de criativos segue o mesmo processo: diga 'creatives' pra gerar novos briefings baseados nos learnings"

### SALVAR

Salve em: /workspace/[produto]/07-ad-strategy.md

Inclua: estrutura completa, naming, configurações, regras de decisão, PGS setup.

Ao final diga: "Campanha estruturada. Monte no Meta Ads Manager seguindo as instruções acima. Depois de 3-7 dias rodando, diga 'ad analysis' pra eu analisar a performance."
