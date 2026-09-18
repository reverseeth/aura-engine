# Page Design · Referência: Detecção e leitura (ETAPA 0)

> A pesquisa exploratória na base com os nove sistemas de fundação de página e a `best_query` de cada um (0.1), a detecção do produto no workspace (0.2) e a lista dos inputs obrigatórios a ler (0.3). Abra na ETAPA 0.

## ETAPA 0 — Detecção e leitura

### 0.1 Pesquisa exploratória na base Aura

Puxe os SISTEMAS NOMEADOS da base (não query genérica) — rode `search_knowledge(deep=true)` com a `best_query` de cada framework de fundação de página. Os de maior impacto pra dominar conversão + estrutura ANTES de planejar:

- **15 Factors of Funnel Structure** (rode `15 factors of funnel structure diagnostic social proof time for results`) — diagnóstico de PDP/LP.
- **Empathy-Trust-Offer (3 Pillars of Landing Pages)** (rode `landing pages that convert empathy trust offer three pillars`).
- **NESP Framework (New, Easy, Safe, Big Promise)** (rode `NESP framework new easy safe big promise offer landing page`).
- **10x Page Plan** (rode `10x page plan framework web pages sections hero proof bar switch close`).
- **4 Decision Making Modalities** (rode `4 decision making modalities spontaneous competitive humanistic methodical web copy`) — toda página serve Spontaneous + Competitive + Humanistic + Methodical ao mesmo tempo.
- **Hero Sections (5 Types + Selection)** (rode `hero sections 5 types value prop dreamstate problem segment campaign selection`) — usado de novo na 1.3.
- **Congruence Principle (Ad-to-Page Message Match / Scent)** (rode `congruence principle message match ad to landing page scent Kennedy consistency rule`).
- **Specificity → Landing Page Conversion** (rode `specificity landing page conversion Hopkins Caples PVA VAKOG mental movies`) — Hopkins/Caples proof stacking + mental movies.
- **CTAs / Calls to Value** (rode `CTAs buttons friction anxiety calls to value lizard brain first person mirror headline`).

Aprofunde até ter domínio de conversão + estrutura de página. Awareness e sophistication (os dois são Schwartz — Breakthrough Advertising) entram na 1.1; advertorial e checkout/AOV têm seus frameworks próprios nas ETAPAs onde são usados (1.1 / referência cruzada à `checkout-aov`). A lista completa do domínio sai do `kb_lookup.py` (instrução no topo desta skill).

### 0.2 Detectar o produto

1. Se o membro mencionou o produto explicitamente, use o slug exato.
2. Senão, liste as subpastas de `workspace/`:
   - 1 produto → use ele, confirmando: "Vou gerar o design da página pro produto X. Confirma?"
   - múltiplos → lista numerada, membro escolhe
   - nenhum → "Não encontrei produtos no workspace. Rode `setup` ou `product research` primeiro, ou cole a copy aqui."
3. Salve o slug em `PRODUTO`. Daqui pra frente, todo `[produto]` = esse slug.

### 0.3 Ler inputs obrigatórios

Leia, sob `workspace/[produto]/`: `copy-engine/copy-engine.md` + `copy-engine/dados.json` (OBRIGATÓRIO), `offer-builder/offer-builder.md`/`dados.json` (preço, stack, garantia, **mecanismo nomeado LITERAL**), `market-research/market-research.md`/`dados.json` (awareness, sophistication, ceticismo, VOC), `competitor-analysis/competitor-analysis.md` (gaps, claims saturados a evitar). Leia `workspace/profile.md` (estilo de marca, stage).
