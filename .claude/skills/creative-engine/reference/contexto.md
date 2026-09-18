# Creative Engine · Referência: Quando usar, pré-flight e contexto a carregar

> Versão completa do que o `SKILL.md` resume no topo: quando a skill roda, o pré-flight item a item, a árvore de decisão de quando rodar (primeira vez, pedido da `ad-analysis`, refresh por fadiga, diversificação), o contrato de sub-avatar com a `market-research` e os sistemas da base que valem pra skill inteira. Abra no início da execução.

## Quando Usar
Quando o membro tem copy pronta (Skill `copy-engine`) e precisa dos briefings de criativos pra rodar no Meta. Cada briefing é completo: tudo que precisa pra filmar, gerar com IA, ou montar (UGC humano, UGC com IA, stock, imagem, ou montagem de clipes), editar, e subir no Ads Manager.

**Mira de volume (alinhamento com a Skill `ad-strategy`):** a estrutura de teste atual é **1 campanha com CBO → N ad sets (broad/Advantage+), sendo 1 ad set = 1 conceito → 3 criativos + 2 primary texts + 2 headlines cada**. O budget vive na campanha, e onde o CBO concentra gasto é o sinal que a Skill `ad-analysis` lê — em dois níveis: por conceito (o ad set) e por criativo (o ad). O "3-2-2" é exatamente o conteúdo de um ad set: **1 conceito = 1 ad set = 1 pack 3-2-2**. Quantos conceitos cabem no batch não vem do stage do membro — vem da **capacidade de teste** do cânone `.claude/lib/ad-taxonomy/README.md` §1 (ETAPA 2).

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.
- [ ] `manifest.json` existe com copy-engine em skills_completed
- [ ] `offer-builder/dados.json` (`target_cpa_primary_2x`, `mechanism`) existe (o `target_cpa` simples vive no `manifest.json`, não no dados.json do `offer-builder`)
- [ ] `market-research/dados.json` existe com `awareness_distribution`, `voc_phrases`, **`sub_avatars[]`**, `core_avatar`, `labels[]` e `market_vocabulary` (contrato de sub-avatar da ETAPA 3 — detalhe no "Contexto a carregar", item 2b)
- [ ] **Pixel/CAPI validados**: ler `manifest.tracking.tracking_ready` (gravado pela `tracking-setup`). Se `true`, seguir. Se `false`/ausente, pedir screenshot do Events Manager mostrando **EMQ ≥ 6/10** (Event Match Quality, escala 0-10) — se membro não pode fornecer, AVISAR que criativos serão desperdiçados e sugerir rodar a `tracking-setup` primeiro
- [ ] Se existe `workspace/[produto]/competitor-analysis/creative-patterns.json` (output do `creative_deep_analysis` da Skill `competitor-analysis`), LER pra extrair `hook_archetypes`, `recurring_claims` (cada claim traz `market_validated` + `also_saturated_pdp` + `usage` — semântica na ETAPA 3) e `format_distribution` dos concorrentes — alimenta a ideação na ETAPA 3
- [ ] **Limpador de Metadados pronto (regra 12):** `node -v` responde (já vem com o Claude Code) e `ffmpeg -version` responde — sem ffmpeg, imagens limpam mas vídeo não. Se faltar, ofereça instalar agora (`brew install ffmpeg` no Mac · `winget install Gyan.FFmpeg` no Windows) e siga; o membro abre o programa com 2 cliques em `Limpador de Metadados.command`/`.cmd` na pasta da Aura quando os criativos finais estiverem prontos
- [ ] Se existe `workspace/[produto]/competitor-analysis/dados.json` com `validated_library` (mecanismos + ângulos validados com evidência de veiculação/escala), `top_creatives` e `ad_formats` (formatos dissecados dos criativos escalados — ETAPA 3D da Skill `competitor-analysis`: estrutura, duração, padrão de iteração), LER também — ângulos com validação de mercado entram na Vertical 1 da ideação com prioridade, e o batch usa formatos JÁ validados por escala (`ad_formats`), nunca só ângulos
- [ ] Se existe `workspace/[produto]/ad-analysis/NEXT_BATCH_IDEAS.md` (output do loop `ad-analysis`→`creative-engine` fechado), LER e usar como input para priorizar ângulos no novo batch — e todo conceito que ITERA um criativo já rodado nasce com **`iteration_of`** preenchido (creative_id do original, schema do dados.json): é essa linhagem que a `ad-analysis` lê no `iteration_zone_check`

**Arquivo de pré-flight faltante (escape path, rule ES1):** se `offer-builder/dados.json` ou `market-research/dados.json` não existir, NÃO aborte seco. Ofereça: **(A)** rodar a skill faltante agora (`offer-builder` ou `market-research`), OU **(B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar a Skill `creative-engine` quando o arquivo real existir. `competitor-analysis/creative-patterns.json` ausente é não-bloqueante (a ETAPA 3 segue só com VOC + competitor analysis + base).

### Quando rodar essa skill (decision tree)
- **Primeira vez** (nunca rodou para este produto): sim, proceed
- **Após skill `ad-analysis` recomendar 'creatives'**: sim, proceed — LER `ad-analysis/NEXT_BATCH_IDEAS.md` primeiro
- **Refresh por fadiga**: só execute se o último ciclo da `ad-analysis` sustenta a leitura — pelos campos que o handoff dela REALMENTE grava (`ad-analysis/dados.json.health_signals`):
  - `frequency_max > 1.4` E `cpm_trend == "up"` (re-martelando a mesma audiência com custo subindo), OU
  - `cpm_trend == "up"` com `frequency_max < 1.3` (saturação de audiência: custo sobe sem re-impacto), OU
  - top-performing criativo tem > 14 dias de idade (`creative_age_days_oldest`)
  A queda de CTR não vive no handoff da `ad-analysis` — antes de rodar refresh pelos dois primeiros sinais, confirme com o membro em 1 pergunta: "o CTR desses ads caiu na última semana no Ads Manager?"
- **Diversificação** (skill `scale-engine` pediu mais diversity): use ratio "2× budget → 2× creative" só em escala >$1k/dia; abaixo disso, use 1.5× — em qualquer caso limitado pela capacidade de teste da ETAPA 2

### Contexto a carregar

1. Leia `workspace/profile.md` (budget → entra na conta de capacidade da ETAPA 2, junto com o target CPA; ferramentas → informa tipo de material viável). Se `workspace/[produto]/ad-strategy/dados.json` já existe, leia `test_capacity` de lá — é a capacidade já calculada pela Skill `ad-strategy` (ETAPA 2, item 1). Leia também `report_language` (regra 0 do CLAUDE.md; default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo: strategy, briefings, hooks bank, production summary) e toda conversa com o membro usam esse idioma, no padrão de escrita da regra 0. **Copy consumidor-final (hooks, scripts, primary texts, headlines, voiceover, text overlays) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.
2. Leia `workspace/[produto]/market-research/market-research.md` (VOC literal, trigger events, objeções, dores/desejos hierarquizados, root cause — TUDO vai pra script; se o `.md` novo não existir, leia o legado `relatorio.md` — mesmo fallback vale pras outras fases)

2b. **CONTRATO DE SUB-AVATAR — leia `workspace/[produto]/market-research/dados.json` (não o `.md`).** É daqui que sai a variável mestre de cada conceito. A Skill `market-research` (ETAPA 4.5) é o único lugar do sistema onde esses campos nascem; a Skill `creative-engine` lê, nunca reinventa:

   | Campo em `market-research/dados.json` | O que a Skill `creative-engine` faz com ele |
   |---|---|
   | **`sub_avatars[]`** — cada item traz `id` (ex: `sa-01`), `name`, `categories_used`, as cinco Core Five na ordem `desire` → `experience` → `emotion` → `behavior` → `demographic` (categoria não usada = string vazia), mais `labels` e `voc_evidence[]` | **Um item = a Persona/Micro-persona de UM conceito.** O conceito referencia o sub-avatar pelo `id` (`sub_avatar_id: "sa-01"` no `dados.json`), nunca por descrição solta reescrita à mão |
   | **`sub_avatars[].angle`** | **O ângulo de entrada do conceito** — já vem em frase completa e é ÚNICO por sub-avatar. Vai direto pro campo `angle` (gate na ETAPA 4.5.A.0.3) |
   | **`core_avatar`** (`surface_desire` = "I want X"; `core_desire_behind` = o instinto por trás) | Usado quando o conceito precisa do avatar AMPLO em vez do recorte fino: hold universal de Marksman (ancorado no `surface_desire`), primary text de static, hook broad sem call-out. `core_desire_behind` orienta TOM, não construção |
   | **`labels[]`** (apelidos que o próprio mercado usa: "light sleepers", "night shifters") | **Call-out do primeiro beat** do criativo — a palavra com que o mercado se nomeia, usada literal |
   | **`market_vocabulary.words_used[]`** com `saturated_in_market: true` | Mensagem **fatigada** (domina os claims dos concorrentes): serve de prova no corpo do texto, **nunca em headline/hook** |
   | **`market_vocabulary.words_absent[]`** | Termos da marca/indústria com zero ocorrência na pesquisa: **PROIBIDOS** em qualquer peça. Use o `market_says_instead` no lugar |

   Consulte `market_vocabulary` **ANTES de escrever qualquer linha** (regra da Skill `market-research`, compartilhada com a `copy-engine`). Se `sub_avatars[]` não existir (produto pesquisado antes deste contrato), trate como pré-flight faltante: ofereça re-rodar a ETAPA 4.5 da Skill `market-research` ou seguir com persona derivada do `avatar` descritivo, marcando `manifest.skipped_preflight += ["02.sub_avatars"]`.
3. Leia `workspace/[produto]/competitor-analysis/competitor-analysis.md` (top criativos transcritos dos concorrentes, gaps de formato/ângulo, swipe file, claims saturados). Se existir `workspace/[produto]/competitor-analysis/creative-patterns.json` (flag `creative_deep_analysis` da Skill `competitor-analysis`), leia também — `hook_archetypes`, `recurring_claims` e `format_distribution` entram na ideação da ETAPA 3. Se o `competitor-analysis/dados.json` tiver `validated_library` e `top_creatives`, leia também (lastro de validação pros ângulos da Vertical 1)
4. Leia `workspace/[produto]/offer-builder/offer-builder.md` (mecanismo único com 3 versões, stack, garantia)
5. Leia `workspace/[produto]/copy-engine/copy-engine.md` (big idea, headlines top 5, CTAs, linguagem usada na LP)
6. **DNA aprendido (loop `ad-analysis`→`creative-engine` — silent):** se `workspace/[produto]/creative-dna/dna-profile.json` existe E `total_creatives >= 10`, extraia as top 5 features com maior delta winners vs losers e use como viés soft na ideação de ângulos (ETAPA 3) e nos briefings (ETAPA 5): priorizar essas features, reservando ~20% do batch pra novelty (o DNA calibra, não engessa). Se não existe ou `total < 10`, siga sem viés. Silent — o membro não vê esse step.
7. Consultas à base de conhecimento — **NUNCA use query genérica.** Puxe os SISTEMAS NOMEADOS da base: rode `search_knowledge` com a `best_query` exata de cada framework relevante à ETAPA em que está. O índice completo dos frameworks desta skill (creatives-hooks-formats + persuasion-psychology) está em `.claude/lib/kb-index/` (mapa skill→domínio no README).

   **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill creative-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 14 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

   Algumas entradas de OUTROS domínios (meta-ads-strategy, scaling) também marcam a `creative-engine` em `use_in_skill`: as que mudam decisão DESTA skill já estão embutidas com query exata no ponto de uso (auditoria de maturidade e share de teste na ETAPA 2; feedback loop de creator na ETAPA 8); o motor de campanha/diagnóstico/escala em volta delas pertence às Skills `ad-strategy`/`ad-analysis`/`scale-engine` e chega aqui via handoff (`NEXT_BATCH_IDEAS.md`, `creative-patterns.json`), não via busca desta skill.

   Tópicos-chave com resumo inline + referência:

   **Hook-Bridge-Hold-CTA** (estrutura de vídeo ad):
   - Hook (0-3s) captura atenção com pattern interrupt + zona emocional de abertura (Valence × Intensity) e hook emotion dominante dentro dela
   - Bridge (3-8s) transiciona da promessa pro corpo estabelecendo credibilidade
   - Hold (8-18s) desenvolve mecanismo/proof/benefit usando o slippery slide (escorregador de leitura: cada frase compele a próxima)
   - CTA (18-22s) call-to-value (não action) + guarantee badge visual
   - [REF: rode a best_query `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`]

   **Valence × Intensity** (camada emocional primária — ETAPA 4.5.E): dois eixos (a emoção é positiva ou negativa × quão forte ela é) que formam 4 zonas, mais o arco emocional obrigatório do ad. É o enum `valence` + `intensity` do dados.json.

   **4 Hook Emotions** (camada inferior, dentro da zona escolhida — 1 dominante por hook; é o enum `emotion_dominant` do dados.json, mantido como campo derivado):
   - Curiosity (pattern interrupt, mistério), Urgency (tempo/escassez real), Fear (dor amplificada), Delight (desejo/transformação)
   - Não confundir com **The Big 4 Emotions** de headline (NEW/ONLY, EASY/ANYBODY, SAFE/PREDICTABLE, BIG/FAST) — esse é framework nomeado da base, usado na ETAPA 5 pra headlines.

   **Slippery Slope** (Sugarman, estrutura de copy):
   - Primeira frase existe só pra fazer ler a segunda; segunda pra fazer ler a terceira; cada linha é um gancho pro próximo
   - Aplicação em vídeo: cada beat de 2-3s tem pattern interrupt visual ou verbal
   - [REF: rode a best_query `slippery slope principle open loops pattern interrupt end with intrigue video script`]

   Sistemas adicionais a puxar por NOME (rode a `best_query` exata, nunca query genérica):
   - **3-2-2 Flexible Ad — Format + 5 Hard Rules** (rode `3-2-2 flexible ad hard rules same format awareness intent one question 12 combinations`)
   - **Ad Definitions — Concept / Angle / Variation / Format** (rode `ad definitions concept angle variation format 3-2-2 testing structure`)
   - **Métodos de teste (Marksman / Sniper / Shotgun) e a distinção ângulo ≠ conceito:** a fonte de verdade NÃO é a base nem esta skill — é o cânone `.claude/lib/ad-taxonomy/README.md` **§7**. A skill referencia; não redefine. O mesmo cânone governa capacidade de teste (§1), as 4 classes de resultado (§2) e Hook/Hold (§4), que a Skill `ad-analysis` usa pra devolver diagnóstico a esta skill.
   - **Funnel Creative Playbook — Olympic Rings Model** (rode `Funnel Creative Playbook Olympic Rings model prospecting closing rings`)
   - **Complete Ad Format Taxonomy (6 video + image formats)** (rode `ad formats taxonomy voiceover b-roll subtitles slideshow UGC studio animation`)
   - **Formats vs Styles (distinção da fonte primária 2026)** (rode `format e entrega neutra style tem vies embutido us vs them nao e formato nem angle`) — completa a taxonomia: **formato é a entrega neutra; estilo carrega viés embutido** ("us vs them" não é formato nem ângulo — é estilo). Declarar os dois separados no briefing evita concluir que "o formato venceu" quando o que mudou foi o estilo.
   - **9-Part Creative Brief Template** (rode `creative brief template 9 parts concept angle testing method format sizes safe zones`)
   - **Show Don't Tell / 'When you're telling, you aren't selling'** (rode `show don't tell behavioral change when telling aren't selling spoken language video`)

   A contagem por domínio NÃO vive aqui: a lista completa e o total saem do `kb_lookup.py`, como manda a instrução de consulta à base no item 7 de "Contexto a carregar".
