# Page Design · Referência: Leitura (ETAPA 0)

> A regra de consulta à base pelo índice, a pesquisa exploratória com os nove sistemas de fundação de página e a `best_query` de cada um, mais as três buscas de design visual (0.1), a detecção do produto no workspace (0.2) e a lista dos inputs obrigatórios a ler (0.3). Abra na ETAPA 0.

## ETAPA 0 — Leitura

### Como esta skill consulta a base

Sempre que esta skill mandar "consulte a base", isso significa: puxe os SISTEMAS NOMEADOS da base, rodando `search_knowledge` com a `best_query` de cada framework relevante PRA AQUELA ETAPA, com `deep=true`. Nunca use query genérica. O índice completo do domínio `page-landing-cro` está em `.claude/lib/kb-index/` (mapa skill→domínio no README).

Rode `python3 .claude/lib/kb-index/kb_lookup.py --skill page-design --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 14 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

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

**Três buscas de design visual.** A lista acima só traz conversão. Some estas três, também com `search_knowledge(deep=true)`, pra que a direção da ETAPA 3 e a construção da ETAPA 4 partam de hierarquia, escala e narrativa, e não só de persuasão. Os termos vêm de três skills de conhecimento do dembrandt (`visual-emphasis-and-hierarchy`, `modular-scale-typography` e `layout-paradigms-and-consistency`); não são `best_query` do índice, então rodam como estão e contam como piso:

- **Hierarquia visual** (rode `visual hierarchy emphasis size colour weight position primary action`) — o que a página manda ler primeiro em cada seção.
- **Escala tipográfica** (rode `modular type scale ratio font sizes relate typography tokens`) — a escala de razão única que a régua mede.
- **Narrativa de landing** (rode `landing page narrative layout paradigm sections consistency structure`) — a ordem das seções como história, que a 1.2 usa fora do advertorial e do listicle.

Aprofunde até ter domínio de conversão + estrutura de página. Awareness e sophistication (os dois são Schwartz — Breakthrough Advertising) entram na 1.1; advertorial e checkout/AOV têm seus frameworks próprios nas ETAPAs onde são usados (1.1 / referência cruzada à `checkout-aov`). A lista completa do domínio sai do `kb_lookup.py` (regra no topo deste arquivo).

### 0.2 Detectar o produto

1. Se o membro mencionou o produto explicitamente, use o slug exato.
2. Senão, liste as subpastas de `workspace/`:
   - 1 produto → use ele, confirmando: "Vou gerar o design da página pro produto X. Confirma?"
   - múltiplos → lista numerada, membro escolhe
   - nenhum → "Não encontrei produtos no workspace. Rode `setup` ou `product research` primeiro, ou cole a copy aqui."
3. Salve o slug em `PRODUTO`. Daqui pra frente, todo `[produto]` = esse slug.

### 0.3 Ler inputs obrigatórios

Leia, sob `workspace/[produto]/`: `copy-engine/copy-engine.md` + `copy-engine/dados.json` (OBRIGATÓRIO), `offer-builder/offer-builder.md`/`dados.json` (preço, stack, garantia, **mecanismo nomeado LITERAL**), `market-research/market-research.md`/`dados.json` (awareness, sophistication, ceticismo, VOC), `competitor-analysis/competitor-analysis.md` (gaps, claims saturados a evitar). Leia `workspace/profile.md` (estilo de marca, stage).

**Marcadores de copy por preencher.** Procure na copy os marcadores em maiúsculas entre colchetes (`[X]`, `[X.X]`, `[AUTHOR NAME]`, `[END DATE]`; "[ CHECK AVAILABILITY ]", com espaço, é estilo de botão e não conta). Achou: liste ao membro, em uma linha cada, e peça os valores. Sem eles a página segue com o marcador no lugar, mas o QA (`copy_placeholders`, bloqueante e nunca liberável) segura a aprovação e a `page-build` até cada um virar um dado real. Nunca invente o número, o nome ou a data.
