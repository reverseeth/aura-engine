---
name: creative-engine
description: Engine de criação de briefings de criativos para Meta Ads. Começa perguntando a ROTA de produção (gerar com IA / modelar concorrente e montar clipes / mix), gera conceitos baseados nas 3 verticais de pesquisa (competitiva, consumidor, interna), produz briefings completos com scripts de vídeo segundo-a-segundo, hooks exatos, image ad specs, primary texts meaningfully different, headlines, LP congruency, e entregáveis ramificados (prompts de IA por clipe OU EDL/roteiro de montagem). Vídeo AI segue hierarquia I2V-first (foto real do produto → image-to-video; avatar fixo + lip-sync pra talking head; text-to-video só B-roll) e, se o Higgsfield MCP estiver conectado, renderiza os vídeos in-session. Humano fotorrealista gerado por AI exige o label "AI Info" da Meta no upload. Mira VOLUME de criativo por semana (a estrutura de teste de 1 ad set com vários criativos da Skill 10 consome volume). Use quando o membro disser "creatives", "criativos", "briefings", "ads", "criar anúncios", ou quando a copy estiver pronta. A mensagem final orienta geração de IA, edição em ferramentas externas (CapCut, Submagic, Captions) e voiceover no ElevenLabs.
---

# Creative Engine

## Quando Usar
Quando o membro tem copy pronta (Skill 06) e precisa dos briefings de criativos pra rodar no Meta. Cada briefing é completo: tudo que precisa pra filmar, gerar com IA, ou montar (UGC humano, UGC com IA, stock, imagem, ou montagem de clipes), editar, e subir no Ads Manager.

**Mira de volume (alinhamento com a Skill 10):** a estrutura de teste atual é **1 campanha → 1 ad set (Advantage+/broad) → N criativos** (5-12). O aprendizado acontece no ad set, e o Facebook distribui o budget entre os criativos. Isso CONSOME volume: o "3-2-2" não é mais "1 ad set por conceito" — é a forma de **organizar o pack de criativos DENTRO do único ad set** (3 execuções do mesmo conceito + 2 primary texts + 2 headlines por conceito). Quanto mais conceitos por semana, mais o ad set tem pra otimizar. O nº de conceitos por batch escala com budget/stage (ETAPA 2).

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)
- [ ] `manifest.json` existe com 06-copy-engine em skills_completed
- [ ] `04-offer-builder/dados.json` (`target_cpa_primary_2x`, `mechanism`) existe (o `target_cpa` simples vive no `manifest.json`, não no dados.json do 04)
- [ ] `02-market-research/dados.json` (awareness_distribution, voc_phrases) existe
- [ ] **Pixel/CAPI validados**: ler `manifest.tracking.tracking_ready` (gravado pela 07c). Se `true`, seguir. Se `false`/ausente, pedir screenshot do Events Manager mostrando **EMQ ≥ 6/10** (Event Match Quality, escala 0-10) — se membro não pode fornecer, AVISAR que criativos serão desperdiçados e sugerir rodar a 07c (tracking-setup) primeiro
- [ ] Se existe `workspace/[produto]/03-competitor-analysis/creative-patterns.json` (output do `creative_deep_analysis` da Skill 03), LER pra extrair `hook_archetypes`, `recurring_claims` (cada claim traz `market_validated` + `also_saturated_pdp` + `usage` — semântica na ETAPA 3) e `format_distribution` dos concorrentes — alimenta a ideação na ETAPA 3
- [ ] Se existe `workspace/[produto]/03-competitor-analysis/dados.json` com `validated_library` (mecanismos + ângulos validados com evidência de veiculação/escala), `top_creatives` e `ad_formats` (formatos dissecados dos criativos escalados — ETAPA 3D da Skill 03: estrutura, duração, padrão de iteração), LER também — ângulos com validação de mercado entram na Vertical 1 da ideação com prioridade, e o batch usa formatos JÁ validados por escala (`ad_formats`), nunca só ângulos
- [ ] Se existe `workspace/[produto]/11-ad-analysis/NEXT_BATCH_IDEAS.md` (output do loop 11→08 fechado), LER e usar como input para priorizar ângulos no novo batch

**Arquivo de pré-flight faltante (escape path, rule ES1):** se `04-offer-builder/dados.json` ou `02-market-research/dados.json` não existir, NÃO aborte seco. Ofereça: **(A)** rodar a skill faltante agora (04 ou 02), OU **(B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar a Skill 08 quando o arquivo real existir. `03-competitor-analysis/creative-patterns.json` ausente é não-bloqueante (a ETAPA 3 segue só com VOC + competitor analysis + base).

### Quando rodar essa skill (decision tree)
- **Primeira vez** (nunca rodou para este produto): sim, proceed
- **Após skill 11 recomendar 'creatives'**: sim, proceed — LER `11-ad-analysis/NEXT_BATCH_IDEAS.md` primeiro
- **Refresh por fadiga**: só execute se `11-ad-analysis` reportou no último ciclo:
  - `frequency > 1.4` E `ctr_drop_pct > 20` em 7 dias, OU
  - CPM subiu > 30% em 7 dias com freq < 1.3 (saturation de audience), OU
  - top-performing criativo tem > 14 dias de idade
- **Diversificação** (skill 12 pediu mais diversity): use ratio "2× budget → 2× creative" só em escala >$1k/dia; abaixo disso, use 1.5×

### Contexto a carregar

1. Leia `workspace/profile.md` (budget → informa quantos conceitos testar; ferramentas → informa tipo de material viável). Leia também `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo: strategy, briefings, hooks bank, production summary) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (hooks, scripts, primary texts, headlines, voiceover, text overlays) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.
2. Leia `workspace/[produto]/02-market-research/market-research.md` (VOC literal, trigger events, objeções, dores/desejos hierarquizados, root cause — TUDO vai pra script; se o `.md` novo não existir, leia o legado `relatorio.md` — mesmo fallback vale pras outras fases)
3. Leia `workspace/[produto]/03-competitor-analysis/competitor-analysis.md` (top criativos transcritos dos concorrentes, gaps de formato/ângulo, swipe file, claims saturados). Se existir `workspace/[produto]/03-competitor-analysis/creative-patterns.json` (flag `creative_deep_analysis` da Skill 03), leia também — `hook_archetypes`, `recurring_claims` e `format_distribution` entram na ideação da ETAPA 3. Se o `03-competitor-analysis/dados.json` tiver `validated_library` e `top_creatives`, leia também (lastro de validação pros ângulos da Vertical 1)
4. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (mecanismo único com 3 versões, stack, garantia)
5. Leia `workspace/[produto]/06-copy-engine/copy-engine.md` (big idea, headlines top 5, CTAs, linguagem usada na LP)
6. **DNA aprendido (loop 11→08 — silent):** se `workspace/[produto]/creative-dna/dna-profile.json` existe E `total_creatives >= 10`, extraia as top 5 features com maior delta winners vs losers e use como viés soft na ideação de ângulos (ETAPA 3) e nos briefings (ETAPA 5): priorizar essas features, reservando ~20% do batch pra novelty (o DNA calibra, não engessa). Se não existe ou `total < 10`, siga sem viés. Silent — o membro não vê esse step.
7. Consultas à base de conhecimento — **NUNCA use query genérica.** Puxe os SISTEMAS NOMEADOS da base: rode `search_knowledge` com a `best_query` exata de cada framework relevante à ETAPA em que está. O índice completo dos frameworks desta skill (creatives-hooks-formats + persuasion-psychology) está em `.claude/lib/kb-index/` (`frameworks.json` / `README.md` — mapa skill→domínio no README). Os frameworks de maior impacto já estão embutidos nas ETAPAs 3, 5, 5.7 e 7 abaixo; o resto fica disponível no índice. Tópicos-chave com resumo inline + referência:

   **Hook-Bridge-Hold-CTA** (estrutura de vídeo ad):
   - Hook (0-3s) captura atenção com pattern interrupt + hook emotion dominante (ver 4 Hook Emotions abaixo)
   - Bridge (3-8s) transiciona da promessa pro corpo estabelecendo credibilidade
   - Hold (8-18s) desenvolve mecanismo/proof/benefit usando o slippery slide (escorregador de leitura: cada frase compele a próxima)
   - CTA (18-22s) call-to-value (não action) + guarantee badge visual
   - [REF: rode a best_query `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`]

   **4 Hook Emotions** (taxonomia interna da skill — escolher 1 dominante por hook; é o enum `emotion_dominant` do dados.json):
   - Curiosity (pattern interrupt, mistério), Urgency (tempo/escassez real), Fear (dor amplificada), Delight (desejo/transformação)
   - Não confundir com **The Big 4 Emotions** de headline (NEW/ONLY, EASY/ANYBODY, SAFE/PREDICTABLE, BIG/FAST) — esse é framework nomeado da base, usado na ETAPA 5 pra headlines.

   **Slippery Slope** (Sugarman, estrutura de copy):
   - Primeira frase existe só pra fazer ler a segunda; segunda pra fazer ler a terceira; cada linha é um gancho pro próximo
   - Aplicação em vídeo: cada beat de 2-3s tem pattern interrupt visual ou verbal
   - [REF: rode a best_query `slippery slope principle open loops pattern interrupt end with intrigue video script`]

   Sistemas adicionais a puxar por NOME (rode a `best_query` exata, nunca query genérica):
   - **3-2-2 Flexible Ad — Format + 5 Hard Rules** (rode `3-2-2 flexible ad hard rules same format awareness intent one question 12 combinations`)
   - **Ad Definitions — Concept / Angle / Variation / Format** (rode `ad definitions concept angle variation format 3-2-2 testing structure`)
   - **Funnel Creative Playbook — Olympic Rings Model** (rode `Funnel Creative Playbook Olympic Rings model prospecting closing rings`)
   - **Complete Ad Format Taxonomy (6 video + image formats)** (rode `ad formats taxonomy voiceover b-roll subtitles slideshow UGC studio animation`)
   - **9-Part Creative Brief Template** (rode `creative brief template 9 parts concept angle testing method format sizes safe zones`)
   - **Show Don't Tell / 'When you're telling, you aren't selling'** (rode `show don't tell behavioral change when telling aren't selling spoken language video`)

   O índice completo do domínio (43 frameworks de creatives-hooks-formats + 49 de persuasion-psychology) está em `.claude/lib/kb-index/`.

## Fluxo da Skill

### ETAPA 0.5 — TrendTrack MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__trendtrack__` disponíveis. Se SIM, use ANTES de gerar ângulos na ETAPA 3:

- **`mcp__trendtrack__creative_inspiration_pack`** com vertical do produto → retorna hooks, landing pages, ângulos e media benchmarks já validados no nicho. Use como sinal extra na ideação das 3 verticais (junto com VOC + competitor analysis + base Aura).
- **`mcp__trendtrack__scan_ad`** em ads escalados detectados pela skill 03 → decomposição precisa de hook + ângulo + scaling assessment, alimenta Hooks Bank (ETAPA 7) com archetypes reais.

Não substitui a ideação criativa nem força copy-paste de hooks alheios — é input adicional pra evitar reinventar formatos que sabemos que funcionam ou repetir claims já saturados. Limite: 1-2 chamadas por batch.

Se TrendTrack NÃO estiver disponível, siga ETAPAs 1-8 normalmente.

### ETAPA 0.6 — Foreplay MCP (opcional, se conectado)

Verifique se há tools com prefixo `mcp__foreplay__` disponíveis (ad spy — 200M+ ads em Facebook/Instagram/TikTok/YouTube/LinkedIn, busca por marca e domain intelligence; o watchlist Spyder já entrega transcrição de hooks). Se SIM, use como fonte ADICIONAL de sinal na ideação da ETAPA 3: hooks e formatos ativos dos concorrentes do nicho, ângulos que estão escalando. Mesmo papel do TrendTrack — input de calibração, nunca copy-paste de hook alheio. Limite: 1-2 chamadas por batch. Se NÃO estiver disponível, siga normalmente (setup opcional documentado em `.claude/automations/setup-mcps.md`).

### ETAPA 0.7 — Higgsfield MCP (opcional, se conectado — muda o ENTREGÁVEL da Rota A)

Verifique se há tools com prefixo `mcp__higgsfield__` disponíveis (MCP oficial da Higgsfield — 30+ modelos incluindo Kling 3.x, Veo 3.1 e Sora 2; OAuth via browser, créditos do plano do membro, sem API key). Se SIM, a ETAPA 5.7 (Ramo A) pode, além de salvar os prompts, **renderizar os vídeos in-session**: a skill gera o prompt, chama a tool de geração e salva o asset pronto no workspace — e roda `bash tools/strip-metadata.sh <pasta-dos-assets>` logo depois (todo asset gerado por IA sobe limpo de metadados de proveniência — EXIF/XMP/C2PA, IDs de job do gerador; o script preserva os pixels e o perfil de cor, e NÃO substitui o label "AI Info" da Meta). Confirme com o membro antes de gastar créditos ("Higgsfield conectado — quer que eu já renderize os [N] vídeos ou prefere só os prompts?"). Se NÃO estiver disponível, entregue os prompts como sempre — nada muda no fluxo atual.

### ETAPA 1.0 — Rota de Produção (Pergunta 0 — ANTES de tudo)

Antes de calcular conceitos, gerar ângulos ou briefings, defina **COMO os criativos vão existir no mundo**. Essa escolha muda o entregável final (prompts de IA vs roteiro de montagem) e como o briefing é escrito. É a primeira pergunta da skill.

Antes de perguntar, calcule o **default recomendado** por stage + nicho (member-stage-awareness + profile), e apresente já com a recomendação marcada — sem travar a escolha do membro:

| Stage / contexto | Default recomendado | Razão |
|---|---|---|
| Starter (budget < $50/dia, primeiro batch) | **Rota A (IA)** | Custo marginal por variação quase zero, sem creator, gera volume rápido pra alimentar o ad set |
| Validating | **Mix (Rota C)** | IA pra volume + 1-2 montagens modeladas em concorrentes que já escalam no nicho |
| Scaling | **Mix (Rota C)** | Diversidade de produção é lever de scale (Skill 12); IA + UGC licenciado + montagens |
| Nicho de alta confiança visual (skincare/beauty 45+, supplement, onde UGC humano real converte muito mais que avatar de IA) | **Rota B ou Mix** | Avatar de IA derruba credibilidade nesses nichos; modelar o que já vende e montar com UGC real rende mais |

Pergunte ao membro (no `report_language`):

"Como você quer produzir esses criativos? Tem 3 rotas:

- **(A) Gerar com IA** — você roda os clipes no Higgsfield Marketing Studio (ou outro modelo) a partir de prompts prontos. Rápido, barato por variação, sem precisar de creator. Entrego **prompts prontos por clipe**. *(custo de referência: Higgsfield Ultra ~$129/mês; gera volume ilimitado de variações)*
- **(B) Modelar concorrente / montar clipes** — você (ou um editor) monta o ad juntando footage real: UGC licenciado (Billo, Insense), stock, ou material próprio, seguindo um **roteiro de montagem (EDL)** que eu entrego — tabela com timecode, tipo de clipe, fonte sugerida, text overlay, legenda exata e transição. Um criativo escalado de concorrente serve SÓ como referência de *timing/estrutura*, nunca pra reusar o clipe dele.
- **(C) Mix** — alguns conceitos com IA, outros com montagem. Diversidade de produção ajuda na escala.

Minha recomendação pro seu caso: **Rota [X]** — [razão de 1 frase]. Quer seguir com ela ou prefere outra?"

Salve a escolha em `manifest.json → production_route: "ai" | "edl" | "mix"` e no `08-creative-engine/dados.json → production_route`. Para **Mix**, na ETAPA 4 (seleção de conceitos) marque por conceito qual rota cada um segue (`concept.production_route`).

**Se Rota A (ou conceito A no Mix) — hierarquia de rotas de geração (doutrina de vídeo AI, ordem de preferência):**

1. **Image-to-video (I2V) a partir de foto REAL do produto** — default pra QUALQUER cena com produto/rótulo em quadro (Kling 3.x é o modelo de referência). O primeiro frame nasce ancorado na foto real, então embalagem, rótulo e texto do produto NÃO alucinam. Peça a foto do produto ao membro antes de compor os prompts.
2. **Avatar fixo + lip-sync** — rota talking head (UGC/testimonial). Consistência da pessoa entre takes só existe com avatar fixo; o script vem do briefing e o lip-sync anima a fala.
3. **Text-to-video (T2V — Sora 2 / Veo 3.1)** — SÓ pra storyboard e B-roll atmosférico (lifestyle, textura, cenário) SEM produto/rótulo em quadro. T2V alucina texto e embalagem; nunca é o asset principal de direct response.

Um mesmo conceito pode combinar as 3 rotas (ex: hook I2V com produto + B-roll T2V + take de avatar lip-sync) — o roteamento por tipo de cena corta custo vs gerar tudo no modelo premium.

**Opção externa pra talking-head (menção, não integração):** se o membro quer volume de vídeo testimonial-style sem gravar gente real e sem montar avatar, o **Arcads** (arcads.ai) transforma script em vídeo UGC com ator AI em minutos (~$2.20/vídeo a partir de $110/mês; alternativa: Creatify, workflow URL-do-produto → ad). A skill escreve o script (o forte da Aura) e o membro renderiza lá. É redundante com a rota avatar + lip-sync pra quem já paga Higgsfield — só recomende se o membro já assina ou pediu explicitamente essa classe de ferramenta.

**Pergunta 1.5: qual modelo de geração?**

A escolha do modelo define **duração e estrutura de geração** (ETAPA 5.7, Ramo A). Pergunte (ou leia de `profile.md → ai_video_model` se já registrado):

"Qual gerador de vídeo de IA você vai usar?
- **Higgsfield Marketing Studio** (clipes curtos, ~15s max por geração) — default, presets de marketing prontos
- **Veo 3.1** (até 60s contínuo)
- **Sora 2** (até 25s contínuo)
- **Kling 3.x** (clipes longos contínuos; modelo de referência pra image-to-video de product shots)
- Outro / não sei → assumo Higgsfield"

Guarde em `08-creative-engine/dados.json → ai_video_model`. O impacto:

| Modelo | Limite por geração | Estrutura de geração | Regra "autocontido por clipe" |
|---|---|---|---|
| **Higgsfield Marketing Studio** | ~15s | **Split em takes** ≤15s (hook num take, body no seguinte) | **APLICA** — cada take é renderizado do zero, sem memória dos outros |
| **Veo 3.1** | ~60s | **Geração contínua única** (o ad inteiro num prompt) | NÃO aplica — é um roteiro contínuo, mais coeso e mais barato |
| **Sora 2** | ~25s | **Geração contínua única** se o ad cabe em ~25s; senão split | NÃO aplica abaixo do limite |
| **Kling 3.x** | longo | **Geração contínua única** | NÃO aplica |

A regra de **"clipe autocontido sem memória cross-shot"** (herdada do `marketing-studio-director.md`) vale **só pra modelos de clipe CURTO** (Higgsfield, e Sora/qualquer modelo quando o ad estoura o limite). Pra modelos longos, gerar o ad inteiro numa **geração contínua** — mais coeso, mais barato, sem split. O split fixo ≤15s da versão antiga era limite do Higgsfield, **não** uma regra universal.

**Se Rota B (ou conceito B no Mix):**

Não há modelo de IA a escolher. O entregável vira um **EDL/roteiro de montagem** por conceito (ETAPA 5.7, Ramo B). Avise o membro que a fonte das imagens precisa ser **licenciada** (UGC de Billo/Insense, stock pago, ou material próprio) — clipe de TikTok/Reels de terceiro NÃO é livre pra reusar. Esse aviso reaparece formalizado no bloco de **usage rights** do EDL.

### ETAPA 1 — Material Disponível + Creator Archetype (Pergunta 1)

Pergunte:

"Que tipo de material você tem pra montar os ads?
- Clips do TikTok/Reels de outros criadores (servem como referência de estrutura/timing, não como footage — ver bloco de Usage Rights)
- Vídeos do fornecedor/fabricante
- UGC gerado por AI (Higgsfield, Arcads, HeyGen, etc)
- Fotos de produto
- Creator humano contratado (pago pra gravar)
- Self-recorded (você mesmo grava)
- Mix de tudo acima"

**Creator Archetype Auto-Selection (realista):**

A maioria dos membros NÃO vai pagar creator humano ($150-500 por vídeo) e NÃO vai querer gravar a si mesmo (barreira alta). Selecione archetype default com base na resposta + budget do profile:

| Resposta do membro | Budget < $500/mês | Budget $500-2k/mês | Budget > $2k/mês |
|--------------------|-------------------|--------------------|-------------------|
| "não tenho nada" / "só fotos" | **AI UGC + stock + motion graphics** (default) | AI UGC + founder-led opcional | AI UGC + 1-2 creators humanos |
| "tenho clips do TikTok" | Montagem licenciada + AI UGC | Montagem licenciada + AI UGC | Montagem licenciada + creator humano |
| "tenho vídeo do fornecedor" | Demonstração + motion graphics | Demo + AI UGC complementar | Demo + creator humano |
| "posso gravar eu mesmo" | Founder-led + AI UGC | Founder-led + AI UGC | Founder-led + creator humano |
| "tenho creator contratado" | Raro — mas priorize o creator | Creator humano primary | Creator humano primary |

**Default geral (se membro estiver em dúvida):** AI UGC + stock + motion graphics. Esse mix é acessível, escalável, e cobre 80% dos cenários.

**Coerência com a rota de produção (ETAPA 1.0):** se o membro escolheu **Rota A (IA)**, o archetype default é `ai_ugc`/`motion_graphics` (gerável por prompt). Se escolheu **Rota B (montagem)**, o archetype tende a `demo`/`creator_human`/`licensed_montage` (footage real montado) — a pergunta de material acima já vira input do EDL. Na **Rota C (Mix)**, cada conceito carrega seu próprio archetype conforme a rota daquele conceito.

> **"Montagem licenciada" (`licensed_montage`):** clipes de TikTok/Reels que o membro coletou servem SÓ como referência de timing/estrutura — o clipe de terceiro NUNCA entra na montagem final (violação de copyright + risco de strike/ban na conta de ads; ver bloco de Usage Rights no Ramo B). A montagem real usa stock pago, UGC licenciado (Billo/Insense) ou material próprio, modelando a ESTRUTURA do que já escala.

Use o archetype pra influenciar FORMATO e SCRIPT dos conceitos:
- **AI UGC** (Higgsfield/Arcads): avatar-driven, ajuste de fala natural obrigatório pra não soar robotizado, duração 15-22s ideal
- **Montagem licenciada** (estilo modelado em criadores): cortes rápidos, UGC-style hooks de pattern interrupt, nenhuma voz off — estrutura modelada, footage 100% licenciado
- **Motion graphics**: carregado de claims, com muito texto na tela, ideal pra listicle hooks e mechanism explainers
- **Founder-led**: talking head caseiro, tom pessoal, storytelling, duração 25-45s
- **Demonstração**: close-up do produto em uso, b-roll intercalado, mínimo de talking, foco em proof visual
- **Creator humano**: UGC tradicional com spokesperson, maior range de duração e complexidade de script

### ETAPA 2 — Calcular Quantidade de Conceitos (mira de volume)

**Estrutura de teste atual (Skill 10):** **1 campanha → 1 ad set (Advantage+/broad) → N criativos** (sweet spot ~5-8, max 12). Não é mais "1 conceito = 1 ad set". Todos os conceitos do batch entram como criativos do MESMO ad set, e o Facebook distribui o budget entre eles. Logo o nº de conceitos não vem de "quantos ad sets cabem" — vem de quantos criativos o ad set comporta sem diluir o aprendizado, ajustado por budget/stage.

**Referência de volume por conceito:** cada conceito = 1 pack 3-2-2 (3 execuções do mesmo conceito + 2 primary texts + 2 headlines). Os 3 criativos do conceito contam como 3 dos N criativos do ad set. Então **2-4 conceitos** já preenchem o sweet spot de 5-12 criativos do ad set.

| Budget diário / stage | Conceitos novos por batch | Por quê |
|---|---|---|
| < $50/dia (starter) | **2-3 conceitos** | 6-9 criativos no ad set; não estourar o sweet spot com pouco budget pra aprender |
| $50-150/dia | **3-4 conceitos** | ~9-12 criativos; enche o ad set sem diluir |
| $150-500/dia (validating) | **4-6 conceitos** (batches mais frequentes) | Pode rodar 1 ad set perto do teto + começar segundo ad set / segunda conta |
| $500+/dia (scaling) | **6-10 conceitos por batch, batches semanais** | Volume é lever de scale; alimenta múltiplos ad sets / contas com criativo fresco toda semana |

> **Por que não despejar 20 criativos num ad set:** acima de ~12 o budget se espalha fino demais e nenhum criativo junta dados suficientes pra decisão de kill (Skill 11). Quando há volume além do teto do ad set, abrir um segundo ad set / segunda conta (regra da Skill 12), não inflar um só.

> **Reconciliação com a rule `member-stage-awareness`:** a rule cita contagens de conceitos por stage (3-4 / 6-8 / 10-15) que vêm da estrutura antiga de 1 ad set por conceito. Com a estrutura atual (1 ad set → N criativos, cada conceito = 3 criativos), **a TABELA ACIMA é a fonte canônica de contagem** — em qualquer divergência, vale esta tabela. O espírito da rule (conservador pra starter, agressivo pra scaling) permanece; só os números absolutos mudaram.

**Champions (conceitos já validados):** se há winners rodando, eles ocupam slots do ad set de teste OU foram isolados em campanha própria de escala (Skill 12). Conceitos novos preenchem os slots restantes até o teto.

Mostre ao membro (sem pedir confirmação) — a mensagem depende de N×3 vs o teto de ~12 do ad set:

- **Se N×3 ≤ 12:** "Com seu budget de $[X]/dia (stage [Y]), vou gerar **[N] conceitos novos** pra este batch. Cada conceito é um pack 3-2-2 (3 execuções do mesmo ângulo + 2 primary texts + 2 headlines), e todos entram como criativos do mesmo ad set Advantage+ pra o Facebook otimizar. Isso dá ~[N×3] criativos no ad set."
- **Se N×3 > 12:** "Com seu budget de $[X]/dia (stage [Y]), vou gerar **[N] conceitos novos** (~[N×3] criativos). Como o teto saudável é ~12 criativos por ad set, o batch será distribuído em 2+ ad sets/contas (regra da Skill 12), com ~5-12 criativos em cada."

### ETAPA 3 — Gerar Ângulos (3 Verticais da Vault)

**Puxe os SISTEMAS NOMEADOS de ideação de ângulo da base (rode a `best_query` exata de cada um — NUNCA query genérica):**

- **Ad Angles Framework — extract actionable angles from sub-avatars** (rode `Ad Angles how to create actionable angles from sub avatars desire behavior gap 3 hooks`) — é o motor das 3 verticais: desire → behavior gap → 3 hooks por sub-avatar.
- **Hormozi What-Who-When Angle Multiplication Matrix** (rode `Hormozi what who when angle multiplication matrix 8 value elements status perspectives timeline`) — multiplica cada ângulo por status/perspectiva/timeline pra explodir o leque sem repetir.
- **Hormozi Callout System — 4 Verbal + 3 Nonverbal Callouts** (rode `Hormozi four verbal callout types labels yes-questions if-then ridiculous results` e `Hormozi three nonverbal callout types contrast likeness scene visual`) — como o ângulo "chama" o avatar certo no primeiro beat.
- **Brunson's Five Curiosity Hooks** (rode `Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles`) — usar quando os ângulos óbvios já estão saturados pelos concorrentes (reframe).
- **New Opportunity vs Improvement Offer (in creative)** (rode `new opportunity vs improvement offer opportunity switch stack new way better way`) — decide se o ângulo posiciona como nova oportunidade (switch) ou melhoria.
- **Categorization = Death / Own a New Category** (rode `categorization death own a new category new hope never compare Ozempic Theragun`) — evita ângulo que ancora o produto na categoria do concorrente.
- **Storytelling as the Hardest-to-Replicate Angle (founder story)** (rode `storytelling hardest to replicate angle founder story defensible creative`) — ângulo defensável pra Vertical 3 (interna).

Índice completo dos sistemas de ideação em `.claude/lib/kb-index/`.

Se `03-competitor-analysis/creative-patterns.json` foi lido no pré-flight, use os sinais dos concorrentes pra calibrar a ideação: `hook_archetypes` (arquétipos de hook já testados no nicho — não reinventar, mas variar), `recurring_claims` (ler os DOIS sinais de cada claim: `usage: "anchor_headline"` = claim validado em ads E não saturado nas PDPs — pode ANCORAR criativos nele, é o que está convertendo no mercado; `usage: "proof_only"` = claim que também está saturado nas PDPs (`also_saturated_pdp: true`) — usar SÓ como prova/base do argumento no body, nunca como headline, porque headline saturada morre no feed) e `format_distribution` (formatos dominantes — se todos usam vídeo demo, considerar um formato sub-explorado). Se o `03-competitor-analysis/dados.json` trouxe `validated_library` (mecanismos + ângulos com evidência de veiculação/escala) e `top_creatives`, priorize na Vertical 1 os ângulos com validação real de mercado — combinação de ângulo validado + execução nova bate ângulo inventado do zero.

**Fonte opcional de inspiração — TikTok Creative Center (grátis):** o Top Ads Dashboard (`https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en`) lista os ads de melhor performance por região/indústria/objetivo, com métricas de engajamento e tempo de veiculação — o que o PRÓPRIO TikTok diz que performa no nicho. Não busca por marca (não é spy tool); serve pra calibrar padrões de hook/formato vencedores antes de gerar ângulos. A página é renderizada por JavaScript: use `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (cascade da rule resilient-fetch). Índice denso só em US/UK/AU/DE/FR; categorias vazias por política são normais. Opcional — pular não bloqueia a ideação.

Gere ângulos em 3 verticais:

**Vertical 1 — Competitiva:**
O que os concorrentes NÃO estão dizendo que você pode dizer (gaps do competitor analysis + `recurring_claims`/`format_distribution` de `03-competitor-analysis/creative-patterns.json` se disponível).
- "Ninguém está endereçando a dor [X] — nosso ad atacará direto"
- "Todo mundo usa angle de resultado — nós vamos de angle de causa raiz"
- "Concorrentes fazem autoridade de doctor — nós vamos peer-to-peer UGC"
- "`recurring_claims` com `usage: proof_only` mostra que todos batem em [claim Z] — vamos pelo gap [W] na headline, mantendo [claim Z] como prova no body"

Gere 3-5 ângulos desta vertical.

**Vertical 2 — Consumidor:**
Dos dados do market research (VOC, trigger events, objeções):
- "Hook baseado na frase exata do cliente que aparece 8x na coleta de reviews"
- "Trigger event [Y] (ex: antes de casamento) como cenário do ad"
- "Ângulo de objeção quebrada [Z] (ex: 'já tentei X, mas aqui está por que este é diferente')"

Gere 3-5 ângulos.

**Vertical 3 — Interna (Oferta/Mecanismo):**
O que é único do seu produto/oferta:
- "Mecanismo único [nome] — apresentado como revelação/descoberta"
- "Garantia agressiva como angle ('90-day guarantee — you pay nothing if it doesn't work')"
- "Stack de valor como angle ('Tudo isso por $X')"
- "Combinação rara de ingredientes como ângulo técnico"

Gere 3-5 ângulos.

### ETAPA 4 — Selecionar os Top N + Apresentar Pro Membro (Pergunta 2)

Das 9-15 opções de ângulo, selecione os **N conceitos mais fortes** (N vem da Etapa 2). Critérios de seleção:
- Cobrir posições diferentes do funil (TOF + MOF + BOF — não todos no mesmo awareness)
- Cobrir ângulos das 3 verticais (não concentrar em uma só)
- Priorizar ângulos DE GAPS (ninguém faz) sobre ângulos de posição já ocupada

Apresente ao membro em formato compacto:

"Esses são os [N] conceitos que recomendo testar:

1. [Conceito] — [ângulo em 1 frase] (vertical: [competitiva/consumidor/interna], posição: [TOF/MOF/BOF])
2. ...

Quer ajustar algum antes de eu gerar os briefings completos?"

- Se o membro disser "tá bom" / "segue" / "manda" → vai pra Etapa 5
- Se pedir ajuste → aplique e confirme antes de gerar briefings

### ETAPA 4.5 — Regras estruturais globais (aplicadas a TODO briefing)

Antes de gerar briefings individuais, estas regras se aplicam a qualquer conceito, independente de vertical/formato:

**A.0. 3-2-2 — Hard Rules (GATE — ler antes de gerar qualquer briefing)**

Um 3-2-2 = 3 criativos + 2 primary texts + 2 headlines = 1 post ID = **1 conceito**. Cada 3-2-2 responde **UMA pergunta**. Os 3 criativos NÃO são 3 ideias diferentes — são **3 EXECUÇÕES do MESMO conceito**, variando SÓ hook/abertura/visual de entrada. As 4 regras abaixo são inegociáveis:

> **Onde o 3-2-2 vive na campanha:** com a estrutura atual (Skill 10: 1 campanha → 1 ad set Advantage+ → N criativos), o 3-2-2 deixou de ser "1 ad set por conceito". Ele é a forma de **organizar o pack de criativos de cada conceito DENTRO do único ad set** — os 3 criativos de cada conceito entram como 3 dos N criativos do ad set. A regra continua valendo como disciplina de variável controlada (testar abertura, não embolar formato/ângulo/awareness), só que a separação por ad set virou separação por conceito dentro do mesmo ad set.

1. **MESMO conceito** — os 3 criativos testam o mesmo ângulo/big idea. Não são 3 ângulos distintos num só 3-2-2.
2. **MESMO formato** — 3 vídeos OU 3 imagens, **nunca misturar**. Variação de formato (vídeo↔imagem) vira um **3-2-2 SEPARADO**, não criativo #2 dentro do mesmo.
3. **MESMO awareness level** — os 3 travados no mesmo nível de Schwartz (ver "Awareness lock" logo abaixo). Awareness diferente = conceito diferente.
4. **MESMO intent** — mesma pergunta de teste, mesma posição de funil. O que varia entre #1/#2/#3 é só o **hook/abertura/visual inicial** (e, se vídeo, o primeiro beat). Body, mecanismo, prova e CTA permanecem coerentes.

**Variação que NÃO é permitida dentro de um 3-2-2:** formato diferente (#1 vídeo, #2 imagem), ângulo diferente (#1 causa-raiz, #2 resultado), awareness diferente (#1 TOF, #3 BOF). Qualquer uma dessas exige um 3-2-2 novo (= novo conceito, novo ad set). Se você quer testar formato/ângulo/awareness diferente, conte como conceito separado na ETAPA 2.

**Awareness lock:** trave o awareness_level do conceito e aplique aos 3 criativos. Valide cada conceito contra `awareness_distribution` de `02-market-research/dados.json` — se o nível escolhido tem peso <10% na distribuição do mercado, emita warning ("awareness X representa só Y% do mercado; confirma a aposta?") antes de prosseguir.

**A. Aspect ratio — sempre 9:16**

Todo criativo (vídeo ou imagem) é produzido em **9:16 (1080×1920)**. Meta/Instagram/TikTok rodam Reels/Stories nessa razão, e versões 1:1/4:5 derivam do 9:16 via crop central ou re-framing manual (documentar esse crop no briefing quando aplicável). Nunca produza 4:5 ou 1:1 como versão primária — vai perder placements de Reels/Stories/TikTok.

**B. Plataforma primária — TikTok vs Meta difference**

Pergunte ao membro (se não estiver no profile): "Esse batch vai rodar primariamente em Meta (FB/IG) ou TikTok?" Use a resposta pra calibrar o briefing:

| Aspecto | Meta (FB/IG Reels) | TikTok |
|---------|---------------------|--------|
| Hook timing | 0-3s com pattern interrupt forte | 0-2s — TikTok penaliza mais rápido |
| Tom | Mais polido aceitável | Mais cru/UGC-native convert melhor |
| Duration ideal | 15-22s TOF, até 45s MOF | 12-20s cap — scroll é mais rápido |
| Text overlay | Importante pra hook retention | Essencial — muitos assistem sem som |
| CTA | Explícito + badge visual | Soft CTA ("link na bio" não funciona em ad — usar CTA button nativo) |
| Música/trending sound | Menos crítico | Trending sound aumenta reach orgânico — aproveitar |
| Format | 1 criativo = 1 ad dentro do ad set (breakdown nativo por ad) | 1 criativo = 1 ad set |

Se o batch roda em **ambas** as plataformas, o briefing tem 2 versões do script: Meta-optimized e TikTok-optimized. Não assuma portabilidade 1:1.

**C. Word count validation por duration (spoken script)**

Cadência de fala natural pra ad é **2.8 a 3.0 palavras por segundo** (mesma referência canônica do `marketing-studio-director.md`: ~43 palavras ≈ 15s). Use esse range pra validar se o script cabe na duração alvo. O director é a fonte única — se houver divergência, vale a do director.

| Duration alvo | Word count ideal (fala) | Word count teto absoluto |
|---------------|-------------------------|--------------------------|
| 10s | 28-30 palavras | 33 |
| 15s | 42-45 palavras | 48 |
| 22s | 62-66 palavras | 72 |
| 30s | 84-90 palavras | 98 |
| 45s | 126-135 palavras | 145 |

**Regra:** ao gerar script de voiceover/fala, ANTES de salvar, conte as palavras e confirme que cabe no range. Se estourar, corte — não deixe o editor precisar acelerar a fala pra caber (soa robótico e destrói retention).

Text overlay não conta nesse cálculo — overlay roda em paralelo à fala.

**Limite de duração por geração — depende do modelo (só relevante pra Rota A/IA):** o split em takes ≤15s **não é universal** — é o limite do **Higgsfield**. O comportamento depende do `ai_video_model` escolhido na ETAPA 1.0 (Pergunta 1.5):

- **Modelo de clipe curto (Higgsfield ~15s; Sora/outro quando o ad estoura o limite):** cada geração é 1 clipe renderizado do zero, **sem memória dos clipes anteriores**. Se o script falado passa do limite, NÃO acelere a fala nem corte — **divida em takes** ≤limite: hook num take, body (mecanismo/prova/CTA) começando no take seguinte (hook e body nunca no mesmo take), cada take 100% autocontido. Lógica completa em `marketing-studio-director.md` (MULTI-SHOT SPLITTING). Entregável = 1 pasta por conceito, 1 arquivo por take.
- **Modelo de geração contínua (Veo 3.1 ~60s; Sora 2 ~25s quando cabe; Kling longo):** gera o ad inteiro numa **geração única contínua** — sem split, mais coeso. A regra "autocontido por clipe sem memória cross-shot" **NÃO se aplica** (é um roteiro contínuo). Entregável = 1 arquivo único por conceito.

A validação de word count por duração (tabela acima) vale em qualquer caso — o que muda é se o script vira 1 clipe contínuo ou vários takes. Detalhe operacional na ETAPA 5.7 (Ramo A). Na Rota B (montagem), não há "geração" — a duração é controlada na edição via o EDL.

**D. Spoken vs Overlay — disciplina de jargão técnico**

Siglas, números complexos, nomes científicos, compostos químicos, unidades de medida e claims regulatórios são **sempre text overlay**, **nunca** na fala. Regras:

- Siglas (qualquer acrônimo de 2+ letras maiúsculas) → overlay
- Números com decimais, percentuais, ou unidades técnicas → overlay (`"48.5% improvement"`, `"2,500 IU"`)
- Nomes de ingrediente/composto químico complexos → overlay
- Estudos citados com N amostral, duração, peer-review status → overlay ou gráfico
- Regulatory references (FDA status, clinical trial phase) → overlay ou disclaimer

**Motivo:** a fala precisa fluir emocionalmente. Siglas/números faladas quebram ritmo, desligam avatares 35+, soam clinicamente desinteressante. No overlay, o mesmo dado ganha peso de evidência visual sem matar cadência.

**Regra de ouro:** se a frase contém ≥2 elementos técnicos, quebrar — a parte emocional vai na fala, os dados duros vão no overlay lado-a-lado.

**E. 4 Hook Emotions — obrigatório marcar dominante no hook**

Todo criativo (e todo hook na Hooks Bank) DEVE declarar explicitamente qual das 4 Hook Emotions domina:

- **Curiosity** — pattern interrupt, mistério, pergunta incompleta, "o que poucos sabem"
- **Urgency** — tempo escasso, janela limitada, risco de perder
- **Fear** — dor amplificada, consequência negativa, "se você não fizer X"
- **Delight** — desejo/transformação, imagem de futuro melhor, prazer antecipado

NÃO permitir hook sem emoção dominante atribuída. Se o hook não encaixa em nenhuma das 4, ele é fraco — reescrever.

Junto da emoção, declarar também o **hook archetype** (id de `.claude/lib/hook-taxonomy/archetypes.json` — 17 arquétipos organizados pelas 4 emoções, ex: `pattern_interrupt`, `secret_reveal`, `transformation`). O archetype declarado aqui entra no contexto da extração de DNA (ETAPA 7.6) — é o que permite ao dna-profile revelar QUAL arquétipo de hook ganha no seu nicho quando a Skill 11 marca winners.

**F. VOC traceability — cada claim/hook linka a VOC phrase**

Cada hook, cada primary text, cada headline precisa ser rastreável a uma fonte no `02-market-research/dados.json` (VOC phrases, trigger events, objeções, dores hierarquizadas). Documentar no output JSON:

```json
{
  "asset_id": "c-01-h-03",
  "text": "texto do hook",
  "voc_source": {
    "ref_id": "voc-phrase-0042",
    "original_phrase": "frase exata do review/post/comment",
    "source_type": "amazon_review|reddit_thread|tiktok_comment|g2_review|...",
    "confidence": "direct_quote|paraphrase|inferred_pattern"
  },
  "emotion_dominant": "curiosity|urgency|fear|delight"
}
```

Claim sem VOC rastreável **OU** sem evidência no `04-offer-builder/research-foundation.json` da Skill 04 = marcar `"voc_source": null, "requires_manual_review": true` e listar no output final pra o membro validar. Proibido inventar frase de avatar sem lastro.

**G. Hook-swap — OPCIONAL, não sempre**

O padrão "1 body × N hook variants" (manter corpo do vídeo e só trocar hook) funciona BEM quando:
- Conceito ganhou e quer testar variações de abertura sem refazer produção
- Body é genérico (product demo, lifestyle footage, motion graphics reutilizável)
- Budget não comporta refilmagem/re-render

Hook-swap NÃO funciona quando:
- Conceito depende de storytelling coeso (founder-led, UGC narrativo)
- Ângulo do hook é tão específico que o body precisa acompanhar (ex: hook de causa-raiz exige body educacional)
- Plataforma detecta "same-body creative" como duplicata (TikTok especificamente)

**Regra:** na Etapa 5, declare explicitamente `hook_swap_viable: true|false` por conceito. Se `false`, Etapa 7 (Hooks Bank) gera hooks pra FUTUROS conceitos novos (não pra swap no atual).

**H. Compliance pré-geração (gate leve antes da Etapa 7.5)**

Além do compliance pass final da Etapa 7.5, aplicar **soft check** durante geração:

- Zero travessão (—) em headlines (regra 8a do CLAUDE.md)
- Zero palavras ad-flag (Botox/Filler/Injection/Cure/Treat/Anti-aging literal) em qualquer peça de copy pra consumidor (regra 8b)
- Substituições automáticas do CLAUDE.md já aplicadas na primeira geração (não deixar pro compliance checker consertar depois)

Esse soft check evita 80% do retrabalho pós-compliance.

**I. Disclosure "AI Info" da Meta — humano fotorrealista gerado por AI**

Se o criativo contém HUMANO fotorrealista gerado ou alterado por AI (avatar de IA, lip-sync, ator sintético — qualquer conceito de Rota A com pessoa em quadro), o ad DEVE receber o label **"AI Info"** da Meta no upload (Ads Manager → nível do ad → marcação de conteúdo gerado por AI). Disclosure correto NÃO sofre penalidade de entrega; conteúdo detectado SEM disclosure sofre distribuição reduzida ou remoção. Regras:

- Marcar `ai_disclosure_required: true` no concept correspondente do `dados.json`
- Listar no resumo de produção (ETAPA 8) quais conceitos exigem o label
- Motion graphics, product shots sem pessoa e footage real de creator humano NÃO exigem o label

### ETAPA 5 — Gerar Briefings Completos (Um Por Conceito)

Para CADA conceito aprovado, gere o briefing completo aplicando os frameworks. **Antes de escrever hook/script/headline, puxe os SISTEMAS NOMEADOS da base — rode a `best_query` exata de cada um, NUNCA query genérica. Índice completo em `.claude/lib/kb-index/`.**

**Para o HOOK (0-3s) — sistemas de maior impacto:**
- **Hook Writing Framework — 3 Functions of a Hook** (rode `hook framework 3 functions ad video stop scroll create curiosity`) — stop scroll, criar curiosidade, set up o ângulo.
- **Gap Theory of Curiosity** (rode `gap theory of curiosity hooks counterintuitive open loop slippery slope`) — abrir loop que o avatar precisa fechar (nunca explicar no hook).
- **Hook Patterns — This-is-X / Timeline+Outcome / Percentage+Promise / Identity Match** (rode `hook patterns this is X timeline percentage identity match POV`) — bancos de padrão prontos pra variar #1/#2/#3.
- **Hopkins' Specificity Rule / 1-2 Second Rule** (rode `Hopkins specificity rule 1-2 second rule vague vs specific claims`) — "47% em 14 dias" > "resultados rápidos".
- **Hook-Specificity-for-Video Rule** (rode `hook specificity rule video specific sub-avatar hooks generic universal hold POV`) — hook específico por sub-avatar, hold universal.

**Para BRIDGE → HOLD → CTA (estrutura do corpo):**
- **4-Section Video Ad Structure (Hook / Bridge / Hold / CTA)** (rode `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`) — timing canônico das 4 seções.
- **Objection → Claim → Proof → Benefit cycle (the Hold)** (rode `objection claim proof benefit cycle hold section one cycle`) — o ciclo que estrutura cada beat do Hold.
- **Slippery Slope Principle** (rode `slippery slope principle open loops pattern interrupt end with intrigue video script`) — cada frase compele a próxima (Sugarman).
- **Schwartz Five Stages of Awareness** (rode `Schwartz five stages of awareness unaware problem solution product most aware headline approach`) — calibra a abordagem do script ao awareness travado do conceito (Hard Rule A.0).

**Para HEADLINES (abaixo do criativo):**
- **Caples' Four U's Hierarchy** (rode `Caples four U's hierarchy unique useful urgent ultra-specific headlines`) — Unique / Useful / Urgent / Ultra-Specific.
- **The Big 4 Emotions (NEW/ONLY, EASY/ANYBODY, SAFE/PREDICTABLE, BIG/FAST)** (rode `Big 4 Emotions NEW ONLY EASY ANYBODY SAFE PREDICTABLE BIG FAST`) — framework de EMOÇÃO DE HEADLINE da base. Não confundir com as 4 Hook Emotions do gate E (curiosity/urgency/fear/delight), que marcam o hook.

**Para PRIMARY TEXTS / proof / fechamento — puxar conforme o ângulo do conceito:**
- **Cialdini's Six Weapons of Influence** (rode `Cialdini six weapons of influence reciprocity commitment social proof authority liking scarcity`).
- **Blair Warren's One-Sentence Persuasion** (rode `Blair Warren one sentence persuasion encourage dreams justify failures allay fears confirm suspicions throw rocks enemies`).
- **Future Pacing** (rode `future pacing copywriting commitment consistency imagine your life with the product better self`).

**Formato do briefing:**

---

# BRIEFING DE CONCEITO #[N]

**Conceito:** [nome/descrição curta do conceito]
**Ângulo:** [razão de compra que estamos comunicando]
**Vertical:** [competitiva / consumidor / interna]
**Awareness Level:** [Unaware / Problem Aware / Solution Aware / Product Aware / Most Aware]
**Posição no Funil:** [TOF / MOF / BOF]
**Formato Principal:** [UGC vídeo / demo vídeo / static / carrossel / motion graphics]
**Big Idea:** [a ideia unificadora em 1 frase]

---

## 3 CRIATIVOS (3 Execuções do Mesmo Conceito)

**Hard Rule (ETAPA 4.5.A.0):** os 3 criativos são o MESMO conceito, MESMO formato (3 vídeos OU 3 imagens), MESMO awareness, MESMO intent. Varia SÓ hook/abertura/visual inicial. Body, mecanismo, prova e CTA permanecem coerentes entre os 3. Formato/ângulo/awareness diferente = 3-2-2 separado (outro conceito).

### Criativo #1

**Tipo:** [vídeo UGC / vídeo demonstração / imagem estática / carrossel / motion graphics]

**SE VÍDEO (script segundo-a-segundo):**

Duração alvo: [15s / 22s / 30s — baseada em posição de funil; TOF mais curto, BOF pode ser mais longo]

Estrutura: Hook → Bridge → Hold → CTA (framework)

- **[00:00-00:03] HOOK** (aplica 4 Hook Emotions: curiosity, urgency, fear, delight — escolher 1 dominante)
  - **Texto/fala EXATA**: "[texto literal — 1-2 frases]"
  - **Visual**: [descrição do que aparece na tela]
  - **Text overlay** (se houver): "[texto]"
  - **Tipo de hook**: [problem / result / curiosity / controversy / social proof / authority]
  - **Força do hook em parar o scroll (thumbstop) esperada**: (estimativa 1-10 baseada em força do hook)

- **[00:03-00:08] BRIDGE** (transição do hook pro corpo)
  - **Texto/fala**: "[texto]"
  - **Visual**: [descrição]
  - **Função**: [estabelecer credibilidade / apresentar problema / mostrar o pattern interrupt]

- **[00:08-00:18] HOLD** (desenvolvimento — mecanismo, proof, benefit)
  - **Texto/fala**: "[texto]"
  - **Visual**: [descrição]
  - **Aplicação do slippery slide**: cada frase deve compelir a próxima (Sugarman)
  - **Proof element presente**: [testimonial / número específico / demo / authority]

- **[00:18-00:22] CTA**
  - **Texto/fala**: "[texto — call to value, não call to action: 'Get my [outcome]' > 'Shop now']"
  - **Visual**: [CTA text overlay + produto em tela + badge de garantia]

**Música/SFX:** [tipo de música ou "sem música" — background que não distrai]
**Precisa de voiceover ElevenLabs?** [sim/não — UGC é geralmente não; demo/motion graphics é sim]
**Se sim, script de voiceover separado:**
```
[script completo e humanizado da locução — contrações, pausas naturais, frases curtas, pra não soar robotizado]
```

**SE IMAGEM** (puxe os sistemas nomeados de static — rode a `best_query` exata, índice em `.claude/lib/kb-index/`):
- **Static/Image Archetypes by Funnel Position** (rode `static image archetypes funnel position plain reminder direct response complexity rule`) — escolhe o archetype certo pra posição de funil do conceito.
- **13+ Winning Static Ad Templates (named breakdowns)** (rode `13 winning static ad templates avatar callout nutella meme breakdown why it works`) — templates nomeados (avatar callout, meme, etc).
- **Show Don't Tell / 'ugly ads convert'** (rode `show don't tell behavioral change when telling aren't selling spoken language video`) — quando o "ugly ad" cru bate o product shot polido.

**Se a imagem tem PESSOA fotorrealista** (review de PDP, "closer look", UGC estático, pessoa aplicando/segurando o produto): as regras de `.claude/lib/prompt-directors/real-people-imagery.md` são OBRIGATÓRIAS no prompt — pessoa crível (nunca modelo), públicos distribuídos por pesquisa (nunca lote homogêneo), zero pele exposta, embalagem real por referência anexada, specs de câmera/luz, contexto imperfeito, ratio pelo destino — mais o pós-processo (strip de metadados + disclosure "AI Info" + review do lote).

- **Descrição visual principal**: [o que aparece — produto + contexto + modelo se houver]
- **Texto overlay principal** (hook): "[texto grande]"
- **Textos secundários**: "[subheadline ou benefits]"
- **CTA visual**: "[texto do botão/badge visual]"
- **Estilo**: [clean product shot / lifestyle / ugly ad / meme-style — "ugly ads convert" principle]
- **Elementos de proof**: [rating stars / review count / featured-in badges / guarantee shield]

### Criativo #2 — [Variação: hook/abertura diferente]

[MESMO formato, MESMO awareness, MESMO ângulo do #1. Varia só o hook e o visual de entrada (primeiro beat se vídeo). Se #1 é vídeo UGC, #2 também é vídeo UGC — nunca troca pra imagem ou demo. Body, mecanismo, prova e CTA seguem coerentes com #1.]

### Criativo #3 — [Variação: hook/visual inicial diferente]

[MESMO conceito, MESMO formato, MESMO awareness. Terceira execução variando só a abertura/visual de entrada. Se quiser testar formato ou ângulo diferente, isso é um 3-2-2 SEPARADO, não o criativo #3.]

---

## 2 PRIMARY TEXTS (Meaningfully Different)

**IMPORTANTE**: Não são variações cosméticas. Cada primary text usa ESTRUTURA, ÂNGULO, e HOOK diferentes.

### Primary Text 1 — [Angle A]

[Copy completa — 100-300 palavras]

Estrutura:
- Hook (primeira linha acima do "See more")
- Corpo (dor/solução/mecanismo/proof/oferta)
- CTA linha final

### Primary Text 2 — [Angle B — diferente de A]

[Copy completa — estrutura diferente]

---

## 2 HEADLINES (Abaixo do Vídeo/Imagem)

Duas headlines que representam hipóteses diferentes. Cada uma é um frame de valor real.

- **Headline 1**: "[texto — max 40 chars ideal]" — frame: [benefício / urgência / offer / pergunta]
- **Headline 2**: "[texto]" — frame: [frame diferente]

---

## URL DE DESTINO

**Destino**: [PDP / Landing Page / Advertorial]

**Justificativa de congruência**:
- Message match: [como o ad conecta com o headline da LP]
- Visual match: [tom visual bate entre ad e LP?]
- Promise match: [a promessa do ad é mantida/expandida na LP, não trocada]

Se o conceito é TOF (cold traffic, awareness low), a LP precisa de mais educação → recomendar advertorial ou LP dedicada. Se é BOF/retargeting (warm), PDP direto funciona.

---

## RACIONAL ESTRATÉGICO

- **Por que esse conceito**: [1-2 frases justificando a aposta com base em market research/competitor analysis]
- **O que esperamos aprender**: [a pergunta que esse teste responde — ex: "o angle de causa raiz (hormônios) converte melhor que angle direto de resultado?"]
- **Success criteria**: [ex: CPA dentro do target em 3-7 dias; thumbstop > 5; CTR > 1.5%]

---

### ETAPA 5.7 — Entregável de produção (ramifica pela rota da ETAPA 1.0)

Após gerar os briefings (Etapa 5), pra CADA conceito gere o entregável de produção. Não é etapa opcional — é parte do entregável final. **A forma do entregável depende da rota escolhida na ETAPA 1.0:**

- **Rota A (IA)** → **Ramo A**: prompts production-ready por clipe (fluxo atual: marketing-studio-director / gpt-image-2-director).
- **Rota B (montagem)** → **Ramo B**: EDL / roteiro de montagem (`concept-XX-edl.md`).
- **Rota C (Mix)** → **Ramo C**: para cada conceito, rodar o ramo correspondente ao `concept.production_route` (alguns A, outros B).

Decida por conceito olhando `concept.production_route` (no Mix) ou a `production_route` global do batch.

---

#### Ramo A — Prompts production-ready de IA (Higgsfield/Veo/Sora/Kling + GPT Image 2.0)

Pra CADA conceito de rota A, gerar prompts prontos pra colar nas ferramentas de geração externas.

**Duração e estrutura de geração — depende do modelo (ETAPA 1.0, Pergunta 1.5):**

Antes de compor o prompt de vídeo, leia `08-creative-engine/dados.json → ai_video_model` e aplique:

- **Modelo de clipe curto (Higgsfield; Sora/outro quando o ad estoura o limite):** validar a duração falada por word count (ETAPA 4.5.C). Se o script passa do limite do modelo (~15s Higgsfield), **dividir em takes autocontidos** — hook num take, body (mecanismo/prova/CTA) começando no take seguinte (hook e body NUNCA no mesmo take), cada take 100% autocontido (sem referência a outro clipe). Lógica completa em `marketing-studio-director.md` (MULTI-SHOT SPLITTING). Entregável = 1 pasta por conceito, 1 arquivo por take.
- **Modelo de geração contínua (Veo 3.1 ~60s; Sora 2 ~25s quando cabe; Kling longo):** gerar o ad inteiro numa **única geração contínua** — um roteiro só, coeso, sem split. A regra "autocontido sem memória cross-shot" **NÃO se aplica** aqui (é roteiro contínuo). Entregável = 1 arquivo único por conceito (`prompt-c01-video.txt`), com o roteiro contínuo (hook → bridge → hold → CTA encadeados) + link/instrução de generation do modelo. O `marketing-studio-director.md` é canônico só pra Higgsfield; pra modelo longo, adaptar a saída pra um roteiro contínuo (mesma copy do briefing, sem dividir em shots).

**Roteamento por tipo de cena (doutrina da ETAPA 1.0):** cena com produto/rótulo em quadro = **I2V a partir da foto real** (anexar a foto como `<<<image_1>>>`); talking head = **avatar fixo + lip-sync**; B-roll atmosférico sem produto = T2V. NUNCA gerar produto/rótulo via T2V puro — alucina embalagem e texto.

**Diretores disponíveis** (em `.claude/lib/prompt-directors/`):

| Director | Ferramenta alvo | Quando invocar |
|---|---|---|
| `marketing-studio-director.md` | Higgsfield Marketing Studio (vídeo) | Conceito com componente de vídeo (qualquer formato: UGC, demo, motion graphic, hyper motion, TV spot, etc) |
| `gpt-image-2-director.md` | GPT Image 2.0 (imagem) | Conceito com componente de imagem estática (PDP-style hero, layout denso com texto, infografia, mockup, ou single-frame cinematográfico) |

**Processo por conceito:**

1. Identificar quais formatos o conceito tem (vídeo? imagem? ambos? — vem da Etapa 5 do briefing)
2. Para cada formato presente, carregar o director correspondente:
   - Vídeo → ler `.claude/lib/prompt-directors/marketing-studio-director.md`
   - Imagem → ler `.claude/lib/prompt-directors/gpt-image-2-director.md`; se a imagem tem pessoa fotorrealista, aplicar POR CIMA as regras obrigatórias de `.claude/lib/prompt-directors/real-people-imagery.md` (pessoa crível, lote distribuído por pesquisa, zero pele exposta, embalagem por referência, câmera/luz, contexto imperfeito)
3. Compor input pro director extraindo do briefing:
   - **Pra Higgsfield (vídeo)**: hook completo + bridge + hold + CTA + visual descriptions de cada beat + duração + creator archetype + plataforma primária + product/avatar attached (se houver)
   - **Pra GPT Image 2.0 (imagem)**: descrição visual principal + texto overlay + estilo + proof elements + estrutura de layout (se denso) ou cena cinematográfica (se single-frame)
4. Rodar o director conforme as regras do SKILL.md dele:
   - Marketing Studio: identifica preset (UGC/Tutorial/Unboxing/Hyper Motion/Product Review/TV Spot/Wild Card/UGC Virtual Try On/Pro Virtual Try On), aplica preset-specific rules, retorna 1 parágrafo + link Higgsfield
   - GPT Image 2.0: roteia entre Format A (JSON estruturado pra layout denso), Format B (prosa cinematográfica pra single image), ou Format C (meta-prompt pra theme-only) — retorna code block do prompt
5. Salvar em `workspace/[produto]/08-creative-engine/prompts/`:
   - **Geração contínua (Veo/Sora dentro do limite/Kling) OU vídeo curto que cabe num take só:** 1 arquivo `prompt-c01-video.txt` — roteiro único (contínuo pros modelos longos; take único pros curtos)
   - **Vídeo curto que estoura o limite do modelo (Higgsfield >15s, multi-shot):** 1 PASTA por conceito (`c01-[slug]/`) com 1 arquivo por take (`shot-1.txt`, `shot-2.txt`, …). Shot 1 = hook; body começa no shot 2 (hook e body NUNCA no mesmo take, cada take autocontido). Cada arquivo de take tem: cabeçalho (conceito, hook, nº do shot, duração estimada, preset), o parágrafo pra colar na ferramenta, o link de generation, e ABAIXO as notas pro membro (produto SIM/NÃO, consistência avatar/cenário, pronúncia) — notas nunca dentro do parágrafo colado.
   - **Imagem:** `prompt-c01-image.txt` (se conceito tem componente de imagem)
   - Quando split, também salvar `_LEIA-PRIMEIRO.txt` na raiz de `prompts/` explicando ordem dos takes, durações e como juntar no editor com 1 voiceover por cima. (Geração contínua não precisa de `_LEIA-PRIMEIRO` — é um clipe só.)

**Inputs herdados (CRÍTICO — não duplicar trabalho):**

- A copy exata (hook, headline, subhead, dialogue) vem do briefing — director NÃO inventa copy nova, só formata
- Product fidelity: se o membro tem foto do produto, o prompt do director menciona explicitamente "<<<image_1>>> = product"
- Avatar fidelity: se há foto de avatar/creator, mesma referência `<<<image_n>>>`
- Aspect ratio 9:16 já é regra global (Etapa 4.5.A) — director NÃO especifica aspect, ferramenta seleciona

**Hard rule — directors são opacos:**

Os SKILL.md dos directors são canônicos. Não modificar conteúdo deles dentro da Skill 08. Se a saída precisar de ajuste, ajustar o INPUT (extrato do briefing) que vai pro director, não o director. Se houver bug recorrente em algum director, atualizar `.claude/lib/prompt-directors/[director].md` em commit separado.

**Render in-session (se Higgsfield MCP conectado — ETAPA 0.7):**

Se há tools `mcp__higgsfield__*` na sessão E o membro aprovou o render, após salvar cada prompt:

1. Chamar a tool de geração correspondente à rota da cena (I2V com a foto real do produto pra cenas com produto; lip-sync pra takes de avatar; T2V só pra B-roll)
2. Salvar o vídeo resultante em `workspace/[produto]/08-creative-engine/renders/c0X-shot-N.mp4` (ou `c0X.mp4` pra geração contínua)
3. Registrar o path em `production_prompts.video.rendered_file` no `dados.json`

Falha de render (créditos esgotados, timeout, tool error) NÃO bloqueia a skill — o prompt salvo continua sendo o entregável e o membro gera manualmente (escape-path: sempre ≥2 caminhos). Sem o MCP, o fluxo é o atual (prompts pra colar).

**Output secundário — `prompts-index.json`:**

Em `workspace/[produto]/08-creative-engine/prompts/prompts-index.json`:

```json
{
  "generated_at": "ISO",
  "concepts": [
    {
      "concept_id": "c-01",
      "video_prompt_file": "prompt-c01-video.txt",
      "video_prompt_folder": "c01-slug/|null",
      "_comment_video_prompt_folder": "preenchida só quando multi-shot (Higgsfield estourando o limite); senão null",
      "video_shots": [
        { "file": "shot-1.txt", "phase": "hook", "duration_sec": 4, "product_ref": false },
        { "file": "shot-2.txt", "phase": "body", "duration_sec": 14, "product_ref": true }
      ],
      "video_director": "marketing-studio-director",
      "video_preset": "UGC|Tutorial|...",
      "image_prompt_file": "prompt-c01-image.txt",
      "image_director": "gpt-image-2-director",
      "image_format": "json|prose|meta"
    }
  ]
}
```

---

#### Ramo B — EDL / roteiro de montagem (`concept-XX-edl.md`)

Pra CADA conceito de rota B (montagem de clipes), gerar um **EDL (Edit Decision List)** — o roteiro que o editor segue pra montar o ad juntando footage real. NÃO é prompt de IA. É um plano de montagem timecode a timecode.

**Insumo:** o briefing completo do conceito (Etapa 5) — hook, bridge, hold, CTA, durações, copy exata, text overlays. A copy NÃO muda; o EDL só decide com qual footage cada beat é coberto.

**Estrutura do arquivo `workspace/[produto]/08-creative-engine/concept-XX-edl.md`:**

```
# EDL — Conceito #[N]: [nome]

**Ângulo:** [...]  ·  **Awareness:** [...]  ·  **Funil:** [TOF/MOF/BOF]
**Duração total alvo:** [Xs]  ·  **Aspect ratio:** 9:16 (1080×1920)
**Voiceover:** [sim/não — se sim, script vem do briefing, gerado no ElevenLabs por cima da montagem]

## Roteiro de montagem

| Timecode | Tipo de clipe | Fonte sugerida | Text overlay | Legenda (caption) | Transição |
|----------|---------------|----------------|--------------|-------------------|-----------|
| 00:00–00:03 | Hook / pattern interrupt | UGC licenciado (Billo/Insense) OU stock — pessoa reagindo | "[overlay literal]" | "[caption literal]" | hard cut |
| 00:03–00:08 | Bridge / problema | UGC ou b-roll do produto | "[overlay]" | "[caption]" | jump cut |
| 00:08–00:18 | Hold / mecanismo+prova | demo do produto + close-up | "[overlay com número/dado]" | "[caption]" | match cut |
| 00:18–00:22 | CTA | produto em tela + badge garantia | "[CTA overlay]" | "[caption]" | — |

> Para split em ≥3 execuções (3-2-2): repetir a tabela variando SÓ a linha do hook (00:00–00:03) — execuções #2 e #3 trocam só o clipe e o overlay de abertura, o resto da montagem é idêntico (mesma disciplina da ETAPA 4.5.A.0).

## Referência de timing (modelar concorrente)

[Se o membro indicou um criativo escalado de concorrente como referência: descrever a ESTRUTURA/ritmo dele — "hook nos primeiros 2s, corta a cada 1.5s, prova no segundo 9, CTA no 18" — como guia de montagem. NUNCA instruir a baixar/reusar o clipe do concorrente. É referência de timing, não asset.]

## ⚠️ Usage rights (OBRIGATÓRIO — ler antes de montar)

Todo footage usado na montagem precisa ser **licenciado pra uso comercial em ads**:

- ✅ **UGC licenciado** (Billo, Insense, Trend.io, ou creator contratado com cessão de direitos por escrito pra paid ads)
- ✅ **Stock pago** com licença comercial (Artgrid, Storyblocks, Envato — confirmar que cobre paid social)
- ✅ **Material próprio** (você filmou / é dono)
- ❌ **Clipe de TikTok/Reels de terceiro** — NÃO é livre. Baixar e reusar footage de outro criador sem licença é violação de copyright e expõe a conta de ads a strike/ban. Um criativo de concorrente serve SÓ como referência de timing/estrutura (coluna acima), nunca como asset na montagem final.
- ❌ Música/trending sound de catálogo não-licenciado em ad pago (em orgânico TikTok ok; em ad pago precisa de áudio licenciado).

Se o membro não tem footage licenciado pra um beat, o EDL marca esse beat como `[FALTA FOOTAGE — opções: contratar UGC Billo/Insense (~$X) | stock pago | filmar próprio]` em vez de sugerir reuso.
```

**Salvar:** `concept-XX-edl.md` por conceito de rota B, em `workspace/[produto]/08-creative-engine/`. Não gera arquivo em `prompts/` (não há prompt de IA pra esse conceito). Registrar no `08-creative-engine/dados.json` (`concept.edl_file`).

---

#### Ramo C — Mix (ambos)

Para cada conceito, rodar o ramo do seu `concept.production_route`: conceitos `ai` seguem o Ramo A (prompts em `prompts/`), conceitos `edl` seguem o Ramo B (`concept-XX-edl.md`). Um mesmo batch pode ter os dois tipos de entregável lado a lado. O `08-creative-engine/dados.json` registra a rota de cada conceito e o arquivo correspondente.

### ETAPA 6 — LP Congruency (Mapeamento Conceito → Landing Page)

Pra cada conceito, documente explicitamente qual LP da fase de copy ele deve direcionar:

| Conceito | Awareness | LP recomendada | Por quê |
|---|---|---|---|
| 1 | Problem Aware | Advertorial | Hook de dor → educação do mecanismo → produto |
| 2 | Solution Aware | Landing Page dedicada | Compara + mecanismo |
| 3 | Product Aware | PDP | Direto pra oferta |

Se o membro só tem uma LP, recomende adaptações (sessões-chave a adicionar na PDP existente pra servir TOF).

### ETAPA 7 — Hooks Bank (10 Alternativas)

Pra uso em iterações futuras, gere **10 hooks alternativos** categorizados. **Só aplique swap se o conceito tiver `hook_swap_viable: true` na Etapa 4.5.G** — senão, esses hooks servem como semente pra conceitos NOVOS, não pra trocar no conceito atual.

**Puxe os SISTEMAS NOMEADOS de hook da base pra variar de verdade (rode a `best_query` exata — NUNCA query genérica; índice em `.claude/lib/kb-index/`):**
- **Two Hook Frameworks: 'This is X' vs 'This is Quirky'** (rode `two hook frameworks this is X biggest thing happening quirky counter-intuitive 5 words`) — cobre os hooks de Resultado e de Curiosidade.
- **Hook Patterns — This-is-X / Timeline+Outcome / Percentage+Promise / Identity Match** (rode `hook patterns this is X timeline percentage identity match POV`) — banco de padrões pros 10 hooks.
- **Brunson's Five Curiosity Hooks** (rode `Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles`) — alimenta os 2 hooks de Curiosidade.
- **Hormozi Callout System — Verbal Callouts** (rode `Hormozi four verbal callout types labels yes-questions if-then ridiculous results`) — hooks de Problema que "chamam" o avatar.
- **Social Proof Scaling System (volume tiers)** (rode `social proof scaling system volume tiers white label percentage testimonial`) — alimenta os 2 hooks de Prova social.

- **Problema** (3 hooks): frases de abertura que lideram com a dor
- **Resultado** (3 hooks): frases que lideram com o outcome desejado
- **Curiosidade** (2 hooks): que despertam mistério ou pattern interrupt
- **Prova social** (2 hooks): que lideram com testimonial ou número

Cada hook deve declarar:
- 4 Hook Emotions dominante (curiosity/urgency/fear/delight)
- VOC source (ref ao `02-market-research/dados.json`, conforme Etapa 4.5.F)
- Word count (≤ 10 palavras ideal pro primeiro beat do vídeo)
- Aspect ratio: 9:16 (sempre)

Cada hook = 1-2 frases, formato de vídeo hook ou image headline.

Esses hooks ficam na biblioteca pra iteração futura. **Além do `hooks-bank.md`, grave os 10 hooks no array top-level `hooks_bank[]` do `08-creative-engine/dados.json`** (mesma estrutura de `concepts[].hooks[]` + campo `category` — schema abaixo). É por esse array que a Skill 09 audita a rastreabilidade VOC e o uso correto do bank (checks H1/M3) — hook só no `.md` fica invisível pro gate.

> O DNA aprendido (dna-profile.json) já foi carregado no "Contexto a carregar" (item 6) e enviesou a ideação desde a ETAPA 3 — não há step de DNA aqui.

### ETAPA 7.5 — Compliance Pre-flight (OBRIGATÓRIO antes de salvar)

Antes de finalizar os briefings e hooks bank, rodar compliance check em TODA peça de copy que vai pro consumidor final.

**Invocação:**
1. Ler `.claude/lib/compliance-preflight/checker.md` (prompt completo) e `.claude/lib/compliance-preflight/red_flags.json` (base de regras)
2. Para CADA item abaixo, rodar o checker:
   - Hook (primeiros 3s do script de cada criativo)
   - Voiceover script completo (se houver)
   - Primary text de cada ad (2 versões por conceito)
   - Headlines (2 por conceito)
   - Text overlays (todos os beats)
   - Hooks Bank (10 alternativos)
3. Parse da resposta JSON — decisão pelo **`overall_verdict`** (protocolo canônico do GATE 1 de `pre-launch-gates.md`, mesma tabela da Skill 06; mapeamento severity→verdict: low → `pass`, medium → `warning`, high/critical → `critical`):
   - `critical` → **BLOCK**: se algum trigger tem `severity: "critical"`, PARAR e apresentar os triggers ao membro com as `rewrite_suggestions[]`, pedindo revisão manual (rota ES3 se launch urgente). Se o verdict veio só de triggers `high`, aplicar o `rewrite_suggestion` (reescrita completa da peça) e **RE-RODAR o check no texto reescrito**; se persistir `critical`, PARAR e apresentar ao membro — a peça não entra no batch sem passar.
   - `warning` → aplicar as `rewrite_suggestions[]` automáticas e **RE-RODAR o check** (NUNCA "manter original"). Se virar `pass`, prosseguir. Se persistir `warning`, salvar a peça MAS logar em `workspace/[produto]/compliance-warnings.json` (path canônico do gate) e citar os warnings na Mensagem Final ("N warnings de compliance — revise se quiser").
   - `pass` → salvar silenciosamente.

   Além do log de warnings acima, manter o log consolidado de TODOS os checks (qualquer verdict) em `workspace/[produto]/08-creative-engine/compliance-log.json`.
4. Sanity pass final: zero termos ad-flag (Botox, filler, injection, cure, treat) em qualquer peça pública. Travessão (—) zero em headlines, ≤2 em copy longa. Todo conceito com humano fotorrealista gerado por AI está marcado `ai_disclosure_required: true` (gate I da ETAPA 4.5).

Output log em `workspace/[produto]/08-creative-engine/compliance-log.json`:
```json
{
  "checked_at": "ISO timestamp",
  "total_pieces": 45,
  "flags_critical": 0,
  "flags_high": 2,
  "flags_medium": 3,
  "pieces_rewritten": 2,
  "triggers_by_eixo": {"Meta Policy": 3, "FTC": 2, "AI Style": 1},
  "details": [...]
}
```

### ETAPA 7.6 — DNA Registry Extraction (silent)

Após compliance pass, pra cada criativo gerado:

1. Ler `.claude/lib/creative-dna/feature_schema.json` e `.claude/lib/creative-dna/extractor.md`
2. Rodar o extractor prompt com:
   - Briefing completo do criativo
   - Awareness level dominante do market research
   - Compliance risk score do Pre-flight
   - Hook archetype declarado na ETAPA 4.5.E (id de `.claude/lib/hook-taxonomy/archetypes.json`) — a extração é schema-driven (a feature `hook_archetype` do `feature_schema.json` flui automaticamente), mas o PROMPT do `extractor.md` pede o archetype declarado explicitamente; é o que fecha o loop archetype→DNA prometido pelo hook-taxonomy
3. Parse JSON response (features estruturadas conforme schema)
4. Salvar em `workspace/[produto]/creative-dna/features-[creative-id].json`
5. Invocar (passar o caminho COMPLETO do features file — `registry.py add` abre o arquivo direto; passar só o nome quebra com FileNotFoundError e o DNA nunca popula):
   ```
   python3 .claude/lib/creative-dna/registry.py init workspace/[produto]  # se ainda não inicializado
   python3 .claude/lib/creative-dna/registry.py add workspace/[produto] [creative-id] workspace/[produto]/creative-dna/features-[creative-id].json --product [slug]
   ```

Silent pro membro. Se extração falhar (Claude retorna malformed JSON), logar erro em `workspace/[produto]/creative-dna/extraction-errors.log` mas não bloquear skill.

### ETAPA 8 — Resumo de Produção

Crie um resumo operacional pro membro executar. As linhas variam conforme a rota (ETAPA 1.0):

**Linhas comuns a qualquer rota:**

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Primary texts prontos | [N × 2] | Copy pra colar no Ads Manager |
| Headlines prontas | [N × 2] | Copy pra colar |
| Voiceovers a gerar | [Z] | ElevenLabs com scripts fornecidos (voz recomendada: [voz]) |

**Se Rota A (ou conceitos `ai` no Mix):**

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Vídeos a gerar com IA ([modelo escolhido]) | [Y] | Prompts prontos em `prompts/prompt-c0X-video.txt` (modelo longo = roteiro contínuo único) ou pasta `c0X-slug/` (Higgsfield multi-shot). Link/instrução de generation no fim do prompt. Se o Higgsfield MCP rendeu in-session (ETAPA 0.7), os vídeos prontos já estão em `renders/` |
| Imagens a gerar com GPT Image 2.0 | [W] | Prompts em `prompts/prompt-c0X-image.txt` — colar direto no GPT Image 2.0 |
| Conceitos que exigem label "AI Info" no upload | [lista de concept-ids] | Ads Manager → nível do ad → marcação de conteúdo gerado por AI (gate I da ETAPA 4.5 — humano fotorrealista AI) |

**Se Rota B (ou conceitos `edl` no Mix):**

| Item | Quantidade | Onde editar/gerar |
|---|---|---|
| Ads a montar (EDL) | [V] | Roteiro de montagem em `concept-0X-edl.md` — seguir a tabela timecode no CapCut/editor, usando SÓ footage licenciado (ver bloco de usage rights) |
| Footage a licenciar (se faltando) | [U beats] | Billo/Insense (UGC), stock pago, ou material próprio — marcado `[FALTA FOOTAGE]` no EDL |

**Tempo estimado de produção:** [Rota A IA: 1-2 dias / Rota B montagem com footage em mãos: 1 dia, com UGC a contratar: 3-7 dias / Mix: combinar]

### Isolar winners no ad set único (estrutura 1-ad-set-N-criativos)

Na estrutura da Skill 10 (1 campanha → 1 ad set Advantage+ → N criativos), cada criativo entra como um **ad individual** no ad set, então o Ads Manager dá breakdown por criativo nativamente (CPA/spend por ad). Para reforçar a leitura e cruzar com Shopify:
- UTMs seguem o **schema canônico da Skill 10** (fonte única — NÃO inventar formato próprio aqui): `utm_content=[concept-id]-[creative-n]` identifica o CRIATIVO (ex: `rootcause-2` — as 3 execuções do pack 3-2-2 nunca dividem o mesmo `utm_content`), e as macros dinâmicas `utm_id={{ad.id}}` + `utm_term={{adset.id}}` dão os identificadores de máquina no breakdown
- Pós-compra, cruzar com Shopify analytics por UTM (o que o Ads Manager mede como purchase nem sempre bate 1:1 com a venda real)
- O Flexible Ads Format do Meta (combinar variações dentro de UM ad) foi **descontinuado em março/2026** — não existe mais como opção no Ads Manager. O parente vivo mais próximo é o toggle **"Flexible media"** do Advantage+ creative (deixa o Meta remixar as mídias entre placements) — sofre da MESMA limitação de breakdown opaco; manter desligado durante teste pra não perder a leitura por criativo. A estrutura é sempre **1 criativo = 1 ad dentro do ad set**, com breakdown nativo por criativo.

### ETAPA 9 — Checklist final antes de entregar o batch (consolidação de TODOS os gates)

A skill tem ~10 gates espalhados pelas ETAPAs. Antes de declarar o batch entregue, percorra esta lista COMPLETA — é a consolidação verificável de tudo (mesmo padrão da Validação Final da 04 e dos sweeps da 06). Item falhou → volte à ETAPA indicada e corrija ANTES de entregar (silent fix first, rule `post-task-self-audit`). O membro só vê o batch com a lista inteira passando.

**Estrutura e volume:**
- [ ] N de conceitos segue a tabela da ETAPA 2 (canônica) pro budget/stage do membro; N×3 ≤ 12 por ad set (ou split em 2+ ad sets anunciado)
- [ ] Cada conceito respeita as 4 hard rules do 3-2-2 (ETAPA 4.5.A.0): MESMO conceito, MESMO formato, MESMO awareness, MESMO intent — os 3 criativos variam SÓ hook/abertura/visual inicial
- [ ] `awareness_level` travado por conceito e validado contra `awareness_distribution` da 02 (warning emitido se peso <10%)
- [ ] Todo criativo em 9:16 (1080×1920) como versão primária (ETAPA 4.5.A); crop 1:1/4:5 documentado quando aplicável
- [ ] Plataforma primária calibrada (ETAPA 4.5.B); se roda em Meta E TikTok, briefing tem as 2 versões de script

**Copy e script:**
- [ ] Word count do spoken script dentro do range 2.8-3.0 palavras/s pra duração alvo (ETAPA 4.5.C); `word_count_within_limit: true` em todos
- [ ] Siglas, números técnicos, compostos químicos e claims regulatórios SÓ em text overlay, nunca na fala (ETAPA 4.5.D)
- [ ] Todo hook (dos conceitos E do Hooks Bank) com `emotion_dominant` (1 das 4 Hook Emotions) + hook archetype declarados (ETAPA 4.5.E)
- [ ] Todo hook/primary text/headline com `voc_source` rastreável à 02 OU marcado `requires_manual_review: true` e listado pro membro (ETAPA 4.5.F) — zero frase de avatar inventada
- [ ] `hook_swap_viable` declarado por conceito (ETAPA 4.5.G)
- [ ] Primary texts meaningfully different (estrutura+ângulo+hook, não cosmético); headlines com frames distintos (ETAPA 5)

**Compliance:**
- [ ] Soft check da geração passou (ETAPA 4.5.H): zero travessão em headlines (≤2 em copy longa), zero ad-flag words em peça pública
- [ ] Compliance Pre-flight (ETAPA 7.5) rodado em TODA peça consumidor-final; decisão pelo `overall_verdict` (critical bloqueado/reescrito+re-rodado, warning reescrito+re-rodado); `compliance-log.json` salvo e warnings residuais em `compliance-warnings.json`
- [ ] Todo conceito com humano fotorrealista de AI marcado `ai_disclosure_required: true` e listado no resumo de produção (ETAPA 4.5.I)

**Entregáveis e handoff:**
- [ ] Entregável de produção por conceito conforme a rota (ETAPA 5.7): Rota A = prompts em `prompts/` + `prompts-index.json` (+ `renders/` se MCP rendeu); Rota B = `concept-XX-edl.md` com tabela timecode + bloco de usage rights; Mix = cada conceito no seu ramo
- [ ] LP congruency documentada por conceito (ETAPA 6): destino + message/visual/promise match
- [ ] Hooks Bank com 10 hooks categorizados no `.md` E no array top-level `hooks_bank[]` do dados.json (ETAPA 7 — contrato com os checks H1/M3 da Skill 09)
- [ ] `dados.json` completo no schema: `emotion_dominant`/`archetype`/`awareness_level` no NÍVEL do concept (contrato com o gate H4 da 09), `compliance_summary` preenchido, `production_route`/`ai_video_model` gravados
- [ ] DNA extraction rodada por criativo (ETAPA 7.6) ou erro logado em `extraction-errors.log` (não bloqueia)
- [ ] Instrução de UTM usa o schema canônico da Skill 10 (`utm_content=[concept-id]-[creative-n]` + macros `{{ad.id}}`/`{{adset.id}}`) — nenhum formato próprio inventado
- [ ] Dual output: todo relatório `.md` com `.html` companion + logo SVG literal (isenções: `concept-NN-edl.md`, `prompts/*`, `renders/*`, `dados.json`); `manifest.json` atualizado + `build_index.py` rodado

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `creative-engine.md`, `concept-NN.md`, `hooks-bank.md`, `production-summary.md`). **Isentos** (arquivos operacionais de handoff — rule 6b do CLAUDE.md, lista completa em `.claude/lib/workspace-index/workspace-layout.md`): `concept-NN-edl.md`, `prompts/*`, `renders/*`, `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/08-creative-engine/` antes de salvar.

Outputs em `workspace/[produto]/08-creative-engine/` (nomenclatura normalizada):

- `creative-engine.md` (estratégia macro — rota de produção escolhida, quantos conceitos, ângulos escolhidos, racional agregado)
- `concept-01.md`, `concept-02.md`, `concept-03.md` (briefs individuais — Etapa 5 completa, um arquivo por conceito)
- `hooks-bank.md` (Etapa 7 — 10 hooks alternativos)
- `production-summary.md` (Etapa 8 — resumo operacional)
- `dados.json` (manifest do batch — ver schema abaixo)
- **Rota A / conceitos `ai`:** `prompts/prompt-c01-video.txt`, `prompts/prompt-c01-image.txt`, ... (Etapa 5.7 Ramo A — prompts production-ready, um arquivo por conceito × formato; pasta `c0X-slug/` com shots quando Higgsfield multi-shot) + `prompts/prompts-index.json` (index — director/modelo/preset/formato) + `renders/c0X*.mp4` quando o Higgsfield MCP rendeu in-session (ETAPA 0.7)
- **Rota B / conceitos `edl`:** `concept-01-edl.md`, ... (Etapa 5.7 Ramo B — roteiro de montagem por conceito, com tabela timecode + bloco de usage rights)
- **Rota C (Mix):** os dois tipos acima, conforme a rota de cada conceito

### JSON companion — `08-creative-engine/dados.json`

> **Contrato com a Skill 09 (gate H4):** `emotion_dominant` (4 Hook Emotions: curiosity/urgency/fear/delight) e `archetype` ficam no NÍVEL do concept (não só dentro de `hooks[]`). Como os 3 criativos de um 3-2-2 compartilham conceito/awareness/intent, a emoção dominante do conceito = a emoção do hook principal. `awareness_level` é travado por conceito (Hard Rule A.0). O array `hooks_bank[]` (ETAPA 7) também é contrato com a 09 (checks H1/M3).

```json
{
  "batch_id": "uuid",
  "product_slug": "...",
  "production_route": "ai|edl|mix",
  "ai_video_model": "higgsfield|veo_3.1|sora_2|kling|other",
  "creator_archetype_default": "ai_ugc|licensed_montage|motion_graphics|founder_led|demo|creator_human",
  "platform_primary": "meta|tiktok|both",
  "aspect_ratio_primary": "9:16",
  "concepts": [
    {
      "id": "c-01",
      "name": "...",
      "production_route": "ai|edl",
      "angle": "problem|result|curiosity|social|authority|comparison|controversy|identification",
      "vertical": "competitive|consumer|internal",
      "awareness_level": "unaware|problem_aware|solution_aware|product_aware|most_aware",
      "emotion_dominant": "curiosity|urgency|fear|delight",
      "archetype": "ai_ugc|licensed_montage|motion_graphics|founder_led|demo|creator_human",
      "funnel_position": "TOF|MOF|BOF",
      "hook_swap_viable": true,
      "format": "video_ugc|video_demo|static_image|carousel|motion_graphic",
      "ai_disclosure_required": false,
      "duration_target_seconds": 22,
      "edl_file": "concept-01-edl.md|null",
      "_comment_edl_file": "preenchido só pra conceitos production_route=edl; null na rota ai (o entregável vira production_prompts)",
      "video_generation_mode": "split_takes|continuous|single_take|null",
      "word_count_spoken": 55,
      "word_count_within_limit": true,
      "hooks": [
        {
          "text": "texto do hook",
          "emotion_dominant": "curiosity",
          "voc_source": { "ref_id": "voc-phrase-0042", "original_phrase": "...", "confidence": "direct_quote" }
        }
      ],
      "primary_texts": [
        { "text": "...", "angle": "A|B", "voc_source": {...}, "compliance_clean": true }
      ],
      "headlines": [
        { "text": "...", "frame": "benefit|urgency|offer|question", "voc_source": {...}, "compliance_clean": true }
      ],
      "production_prompts": {
        "_comment": "preenchido só pra conceitos production_route=ai; pra route=edl, production_prompts=null e o entregável é edl_file",
        "video": {
          "_comment": "director continuous-script = modelo de geração contínua (Veo/Sora/Kling); rendered_file preenchido só quando o Higgsfield MCP rendeu in-session (ETAPA 0.7), senão null",
          "file": "prompts/prompt-c01-video.txt",
          "director": "marketing-studio-director|continuous-script",
          "model": "higgsfield|veo_3.1|sora_2|kling",
          "preset": "UGC|Tutorial|Unboxing|Hyper Motion|Product Review|TV Spot|Wild Card|UGC Virtual Try On|Pro Virtual Try On",
          "tool_url": "https://higgsfield.ai/marketing-studio",
          "rendered_file": "renders/c01.mp4|null"
        },
        "image": {
          "file": "prompts/prompt-c01-image.txt",
          "director": "gpt-image-2-director",
          "format": "json|prose|meta",
          "tool": "GPT Image 2.0"
        }
      }
    }
  ],
  "hooks_bank": [
    {
      "text": "texto do hook alternativo",
      "category": "problema|resultado|curiosidade|prova_social",
      "emotion_dominant": "curiosity|urgency|fear|delight",
      "voc_source": { "ref_id": "voc-phrase-0042", "original_phrase": "...", "confidence": "direct_quote|paraphrase|inferred_pattern" },
      "word_count": 8
    }
  ],
  "total_assets": 3,
  "format": "3-2-2",
  "next_batch_ideas_applied": ["ref-01", "ref-02"],
  "compliance_summary": {
    "ad_flag_words_found": 0,
    "em_dash_in_headlines": 0,
    "unresolved_claims_without_voc": 0,
    "unresolved_claims_without_research_foundation": 0
  }
}
```

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `08-creative-engine` em `skills_completed`
- Registrar `last_batch_id`, `batch_count`, e `next_batch_ideas_applied` (refs lidas de `11-ad-analysis/NEXT_BATCH_IDEAS.md`, se houver)
- Registrar `production_route` (`ai|edl|mix`) e, se rota envolve IA, `ai_video_model` (pra a próxima execução já assumir a rota/modelo do membro sem reperguntar — só confirmar)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html)

## Mensagem Final

A mensagem se adapta à rota escolhida (ETAPA 1.0). Apresente como **draft** convidando iteração (rule iteration-driven-refinement), não como "pronto pra lançar". Se a ETAPA 7.5 deixou warnings residuais de compliance, cite na mensagem ("N warnings de compliance — revise se quiser").

**Se Rota A (IA):**

"Primeira versão dos briefings pronta. Como gerar:

- **Vídeos**: abra `workspace/[produto]/08-creative-engine/prompts/prompt-c0X-video.txt` — cole no [modelo escolhido] (link/instrução de generation no fim do prompt). Modelo longo (Veo/Sora/Kling) = 1 roteiro contínuo por conceito; Higgsfield = pode ter pasta `c0X-slug/` com 1 take por arquivo (gere na ordem e junte sob 1 voiceover). [Se o Higgsfield MCP rendeu in-session: "Os vídeos já estão renderizados em `renders/` — revise antes de editar."]
- **Imagens**: abra `prompts/prompt-c0X-image.txt` — cole no GPT Image 2.0 (formato já ajustado ao tipo)
- **Voiceovers** (se conceito tem): gere no ElevenLabs com os scripts marcados nos briefings
- **Edição**: junte vídeo + voiceover + text overlays no CapCut/Submagic/Captions
- **Label "AI Info"**: os conceitos [lista] têm humano fotorrealista gerado por AI — no upload, marque o conteúdo como gerado por AI no Ads Manager (com o label correto não há penalidade; sem ele, o Meta reduz a entrega ou remove o ad)

Revisa e me diz o que ajustar (tom, ângulo, hook) antes de você gerar tudo. Quando os criativos estiverem prontos: diga **'agentic readiness'** (07e) e depois **'consistency audit'** (09 — o GATE de launch); com o audit verde, **'ad strategy'** monta a campanha no Meta."

**Se Rota B (montagem/EDL):**

"Primeira versão dos roteiros de montagem pronta. Como montar:

- **EDL por conceito**: abra `workspace/[produto]/08-creative-engine/concept-0X-edl.md` — a tabela timecode diz, beat a beat, que clipe entra, o text overlay e a legenda exata. Monte no CapCut/editor seguindo a tabela
- **Footage**: use SÓ material licenciado (leia o bloco de usage rights em cada EDL). Onde falta footage, o EDL marca `[FALTA FOOTAGE]` com as opções (Billo/Insense, stock pago, próprio)
- **Voiceovers** (se conceito tem): gere no ElevenLabs e coloque por cima da montagem

Revisa os EDLs e me diz se o ritmo/estrutura tão certos antes de você montar. Quando os criativos estiverem prontos: diga **'agentic readiness'** (07e) e depois **'consistency audit'** (09 — o GATE de launch); com o audit verde, **'ad strategy'** monta a campanha no Meta."

**Se Rota C (Mix):** combine as duas mensagens — liste os conceitos `ai` apontando pros prompts e os conceitos `edl` apontando pros arquivos de montagem."
