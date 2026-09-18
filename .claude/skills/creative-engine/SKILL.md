---
name: creative-engine
description: Briefings de criativos para Meta Ads. Rota de produção (IA, montagem de clipes licenciados ou mix), número de conceitos pela capacidade de teste do cânone ad-taxonomy (nunca pelo stage), ângulos nas 3 verticais a partir dos sub-avatares da market-research e, por conceito, um pack 3-2-2 (3 criativos + 2 primary texts + 2 headlines, 1 ad set na campanha da ad-strategy) com método Marksman ou Sniper, ângulo em frase, zona emocional com arco, script segundo a segundo, prompts de IA ou EDL, LP congruency, hooks bank e resumo de produção. Todo criativo passa pelo Limpador de Metadados antes de subir. Use quando o membro disser "creatives", "criativos", "briefings", "ads", "criar anúncios", ou quando a copy estiver pronta.
---

# Creative Engine · Passo 13 · apelido antigo: 08 <!-- gen:title -->

## Quando usar

Quando a copy está pronta (`copy-engine` em `skills_completed`) e o membro precisa dos briefings de criativos pra rodar no Meta. Cada briefing traz tudo pra filmar, gerar com IA ou montar, editar e subir. Estrutura de teste: 1 campanha com CBO, 1 ad set = 1 conceito = 1 pack 3-2-2; quantos conceitos cabem vem da capacidade de teste (ETAPA 2), nunca do stage.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

- [ ] `manifest.json` com `copy-engine` em `skills_completed`
- [ ] `offer-builder/dados.json` (`target_cpa_primary_2x`, `mechanism`)
- [ ] `market-research/dados.json` com `awareness_distribution`, `voc_phrases`, `sub_avatars[]`, `core_avatar`, `labels[]` e `market_vocabulary`
- [ ] `manifest.tracking.tracking_ready` = `true`; senão, screenshot do Events Manager com EMQ ≥ 6/10, ou avise do desperdício e sugira a `tracking-setup`
- [ ] Se existirem: `competitor-analysis/creative-patterns.json`, `competitor-analysis/dados.json` (`validated_library`, `top_creatives`, `ad_formats`) e `ad-analysis/NEXT_BATCH_IDEAS.md` (iteração nasce com `iteration_of`)
- [ ] Limpador de Metadados pronto: `node -v` e `ffmpeg -version` respondem; sem ffmpeg, ofereça instalar e siga

Arquivo faltante (ES1): rodar a skill faltante agora OU seguir com default genérico marcando `manifest.skipped_preflight`. Quando rodar (primeira vez, pedido da `ad-analysis`, refresh por fadiga, diversificação): `reference/contexto.md`.

## Contexto a carregar

Leia nesta ordem e depois abra `reference/contexto.md` (contrato de sub-avatar e sistemas da base). Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar do detalhe; arquivo antigo sem `resumo` se lê inteiro, como antes.

1. `workspace/profile.md` (budget, ferramentas, `report_language`) e `ad-strategy/dados.json.test_capacity`, se existir
2. `market-research/market-research.md` (VOC, triggers, objeções; fallback legado `relatorio.md`)
3. `market-research/dados.json`, o contrato de sub-avatar: `sub_avatars[]` é a persona de cada conceito (por `id`) e `sub_avatars[].angle` o ângulo; `core_avatar` o avatar amplo; `labels[]` o call-out; `market_vocabulary` filtra toda palavra
4. `competitor-analysis/competitor-analysis.md` (mais `creative-patterns.json` e `dados.json`, se existirem)
5. `offer-builder/offer-builder.md` e `copy-engine/copy-engine.md`
6. DNA aprendido, silent: `creative-dna/dna-profile.json` com `total_creatives >= 10` vira viés soft na ideação, com ~20% do batch pra novelty
7. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill creative-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 14 buscas adicionais por etapa; as queries embutidas em `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida

Idioma: output interno e conversa no `report_language`; copy pro consumidor e VOC literal sempre em inglês US.

## Fluxo da skill

### ETAPA 0.5 · ETAPA 0.6 · ETAPA 0.7 · MCPs opcionais

Com tools `mcp__trendtrack__`, `mcp__foreplay__` ou `mcp__higgsfield__`, leia `reference/mcps-opcionais.md`: TrendTrack e Foreplay são sinal extra antes da ETAPA 3 (1 a 2 chamadas, sem copiar hook alheio); Higgsfield deixa a ETAPA 5.7 renderizar in-session, confirmando antes de gastar créditos. Sem MCP, nada muda.

### ETAPA 1.0 · Rota de produção (Pergunta 0)

Leia `reference/rota-de-producao.md`. Calcule o default por stage e nicho e pergunte: (A) gerar com IA, prompts por clipe; (B) modelar concorrente e montar clipes licenciados, EDL; (C) mix. Grave `production_route` no manifest e no `dados.json`. Rota A: hierarquia I2V-first do arquivo e a pergunta do modelo de geração, gravando `ai_video_model`, que decide entre takes autocontidos e geração contínua. Rota B: todo footage precisa ser licenciado.

### ETAPA 1 · Material disponível e creator archetype (Pergunta 1)

Mesmo arquivo. Pergunte que material o membro tem e escolha o archetype pela matriz resposta × budget, coerente com a rota; ele define formato, duração e script. Varie o talento entre conceitos e declare o eixo no campo Avatar do briefing. Recrutar ou gerir creators é da `creator-engine`.

### ETAPA 2 · Quantos conceitos entram no batch (capacidade, não stage)

Leia `reference/capacidade-de-teste.md`. 1 conceito = 1 ad set = 1 pack 3-2-2. Com `ad-strategy/dados.json.test_capacity`, `max_adsets` é o teto; senão, `max_adsets = floor(budget_diário ÷ (3 × target_cpa))` do cânone `.claude/lib/ad-taxonomy/README.md` §1, com o teto de ad sets do arquivo. Budget abaixo do piso: 1 conceito, resultado direcional. Capacidade maior que a ideação: não invente conceito. Membro `scaling`: rode antes os dois sistemas da base do arquivo. Mostre a conta sem pedir confirmação.

### As variáveis de um ad

Antes das ETAPAs 3, 4.5 e 5, leia `reference/variaveis-de-um-ad.md`: 9 variáveis controláveis e as invisíveis. Persona é a variável mestre e vem de `sub_avatars[]`. Num 3-2-2 quase tudo fica congelado; entre conceitos, varie as variáveis grandes; iteração muda UMA por vez.

### ETAPA 3 · Gerar ângulos (3 verticais)

Leia `reference/ideacao-e-selecao.md` e puxe os sistemas de ideação pela `best_query` (lista no arquivo). Calibre com `creative-patterns.json` e `validated_library`. Todo ângulo é frase completa de razão de compra, filtrada por `market_vocabulary`. Vertical 1 competitiva (gaps); Vertical 2 consumidor (comece pelos `sub_avatars[].angle` literais, amplie por desire → behavior → gap); Vertical 3 interna (mecanismo, garantia, stack). 3 a 5 ângulos por vertical.

### ETAPA 4 · Selecionar os top N e apresentar (Pergunta 2)

Mesmo arquivo. Escolha N conceitos cobrindo funil, verticais, gaps e diversidade nas variáveis grandes; `sniper` consome 1 ângulo, `marksman` consome 3; com histórico na `ad-analysis`, ao menos um conceito abre na zona que já venceu. Apresente em formato compacto (texto no arquivo) e pergunte se ajusta antes dos briefings.

### ETAPA 4.5 · Regras estruturais globais (todo briefing)

Leia `reference/regras-estruturais.md` (método de teste e as 4 hard rules do 3-2-2; ângulo é frase, conceito é embalagem; awareness lock; 9:16; Meta × TikTok; word count por duração e limite por modelo; jargão só em overlay; origem da VOC; hook-swap; estilo; limpeza de metadados) e `reference/zona-emocional.md` (4 zonas de Valence × Intensity, arco que abre em valência baixa e fecha em alta, 4 Hook Emotions derivadas, hook archetype). Grave por conceito `testing_method`, `angle`, `concept_type`, `valence`, `intensity`, `valence_open`, `valence_close`, `emotion_dominant`, `hook_swap_viable`, `mold_id` e `mold_source`.

### ETAPA 5 · Briefings completos (um por conceito)

Com `competitor-analysis/ad-molds.json` (`ad_molds.status` `completed`), leia antes `reference/molde-e-injecao.md`: 1 molde por conceito, tabela slot a slot e nota técnica; sem o arquivo, nada muda. Leia `reference/briefing.md`. Puxe os sistemas de script, hook, hold, headline e primary text pela `best_query` exata (lista no arquivo; statics e pessoa fotorrealista têm sistemas próprios). Escreva no formato do arquivo: cabeçalho com as 9 variáveis, 3 criativos (script Hook → Bridge → Hold → CTA segundo a segundo, ou spec de imagem), 2 primary texts meaningfully different, 2 headlines, URL de destino com a congruência justificada e racional estratégico. Salve `concept-NN.md`.

### ETAPA 5.7 · Entregável de produção (ramifica pela rota)

Leia `reference/entregavel-de-producao.md`. Ramo A: prompts por clipe pelos directors de `.claude/lib/prompt-directors/` (vídeo, imagem, pessoa real), roteamento por tipo de cena, takes ou geração contínua conforme `ai_video_model`, salvos em `prompts/` com `prompts-index.json`; com o Higgsfield MCP aprovado, renderiza em `renders/` e roda `bash tools/strip-metadata.sh` antes de registrar em `rendered_files[]`. Ramo B: `concept-NN-edl.md` com tabela timecode e usage rights (só footage licenciado). Ramo C: cada conceito no seu ramo.

### ETAPA 6 · LP congruency

Leia `reference/pos-briefing.md`. Tabela conceito → awareness → LP recomendada, com o porquê; com uma LP só, recomende adaptações. A `ad-strategy` lê a tabela pra definir o destino de cada ad set.

### ETAPA 7 · Hooks Bank

Mesmo arquivo. 10 hooks (3 problema, 3 resultado, 2 curiosidade, 2 prova social) com os sistemas de hook pela `best_query` exata. Cada hook declara zona, emoção dominante, ângulo em frase, `sub_avatar_id`, `voc_source` e word count; cobertura das 4 zonas. Grave em `hooks-bank.md` E em `hooks_bank[]` do `dados.json` (contrato com a `consistency-audit`).

### ETAPA 7.5 · Passada final de estilo

Zero travessão em headlines, no máximo 2 em copy longa; nenhuma peça com aviso ou claim suavizado; todo arquivo em `renders/` como `asset-xxxx`.

### ETAPA 7.6 · Extração de DNA (silent)

Mesmo arquivo. Por criativo: `feature_schema.json` e `extractor.md` de `.claude/lib/creative-dna/`, salvar `creative-dna/features-[creative-id].json` e rodar `registry.py add` com o caminho completo. Falha loga em `extraction-errors.log` e não bloqueia.

### ETAPA 8 · Resumo de produção

Leia `reference/resumo-de-producao.md`. Tabelas por rota (o que gerar, quantidade, onde), a tabela "como ler este batch" (método e pergunta por conceito), o loop de feedback de creator quando há creator humano, a limpeza de metadados como último passo e o tempo estimado. UTMs no schema da `ad-strategy` (`utm_content=[concept-id]-[creative-n]`); 1 criativo = 1 ad no ad set do conceito.

### ETAPA 9 · Checklist final antes de entregar

Leia `reference/checklist-final.md` e percorra a lista inteira (estrutura e volume, copy e script, estilo e upload, entregáveis e handoff). Item falhou: volte à etapa indicada e corrija antes de entregar, em silêncio.

## SALVAR

Todo relatório `.md` ganha `.html` por `python3 tools/render_report.py <md>` (isentos: `concept-NN-edl.md`, `prompts/*`, `renders/*` e o `dados.json`). Em `workspace/[produto]/creative-engine/`: `creative-engine.md` (estratégia macro), `concept-NN.md`, `hooks-bank.md`, `production-summary.md`, `dados.json` no schema de `reference/dados-json.md`, mais `prompts/` e `renders/` (Rota A) ou `concept-NN-edl.md` (Rota B). Depois `python3 tools/manifest.py <slug> complete creative-engine` e `set` com `last_batch_id`, `batch_count`, `next_batch_ideas_applied` e `production_route` (mais `ai_video_model`, se houver IA); então `python3 .claude/lib/workspace-index/build_index.py <slug>`. O `dados.json` abre pelo objeto `resumo`, o bloco curto que a fase seguinte lê de primeira (formato em `reference/dados-json.md`).

## Mensagem final

Texto integral em `reference/mensagem-final.md`. Apresente como draft e convide a iteração. Rota A: onde estão os prompts, imagens no GPT Image 2.0, voiceovers no ElevenLabs, edição no CapCut/Submagic/Captions, limpeza de metadados como último passo. Rota B: EDL por conceito, só footage licenciado. Mix: combine. Próximos passos: `agentic-readiness`, depois `consistency-audit` (gate de launch) e `ad-strategy`.
