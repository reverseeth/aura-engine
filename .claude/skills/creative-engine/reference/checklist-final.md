# Creative Engine · Referência: Checklist final antes de entregar o batch (ETAPA 9)

> A consolidação de todos os gates da skill, em quatro blocos. Abra na ETAPA 9 e percorra a lista inteira.

### ETAPA 9 — Checklist final antes de entregar o batch (consolidação de TODOS os gates)

A skill tem ~10 gates espalhados pelas ETAPAs. Antes de declarar o batch entregue, percorra esta lista COMPLETA — é a consolidação verificável de tudo (mesmo padrão da Validação Final da `offer-builder` e dos sweeps da `copy-engine`). Item falhou → volte à ETAPA indicada e corrija ANTES de entregar (silent fix first, rule `post-task-self-audit`). O membro só vê o batch com a lista inteira passando.

**Estrutura e volume:**
- [ ] N de conceitos respeita a capacidade de teste da ETAPA 2 — `test_capacity.max_adsets` da `ad-strategy` quando existe, senão `max_adsets = floor(budget ÷ (3 × target CPA))` do cânone §1 —, com o teto de 5 ad sets abaixo de US$ 1k/dia; cada conceito entregue = 1 ad set = 3 criativos
- [ ] `testing_method` declarado por conceito e coerente com a matriz do cânone §7 (ETAPA 4.5.A.0.1): primeiro teste em imagem = `marksman`; primeiro teste em vídeo = `sniper`; **toda iteração = `sniper`**. Desvio do default está justificado no briefing
- [ ] Cada conceito respeita as hard rules do 3-2-2 (ETAPA 4.5.A.0.2): MESMO formato, MESMO awareness, MESMO intent nos 3 criativos — em qualquer método. Ângulo: `sniper` = o mesmo nos 3, variando só hook/abertura/visual; `marksman` = 3 ângulos distintos sob hold universal
- [ ] Conceito `marksman` tem `hold_universal` declarado e `hold_universal_validated: true` (o hold sustenta os 3 hooks, checado um a um). Conceito `sniper` tem hold específico e profundo, não genérico — hold que serviria pra qualquer hook reprova
- [ ] `awareness_level` travado por conceito e validado contra `awareness_distribution` da `market-research` (warning emitido se peso <10%)
- [ ] Todo criativo em 9:16 (1080×1920) como versão primária (ETAPA 4.5.A); crop 1:1/4:5 documentado quando aplicável
- [ ] Plataforma primária calibrada (ETAPA 4.5.B); se roda em Meta E TikTok, briefing tem as 2 versões de script

**Copy e script:**
- [ ] Word count do spoken script dentro do range 2.8-3.0 palavras/s pra duração alvo (ETAPA 4.5.C); `word_count_within_limit: true` em todos
- [ ] Siglas, números técnicos e compostos químicos SÓ em text overlay, nunca na fala (ETAPA 4.5.D)
- [ ] **Ângulo em frase (gate ETAPA 4.5.A.0.3):** todo conceito tem `angle` preenchido como frase completa de razão de compra, passando no teste de classificação. Zero enum, zero palavra solta, zero rótulo de formato no campo `angle`. `concept_type` preenchido separadamente com a embalagem
- [ ] **Contrato de sub-avatar:** todo conceito tem `sub_avatar_id` apontando pra um item real de `sub_avatars[]` da `market-research`, e o `angle` veio de `sub_avatars[].angle` (ou é frase nova no mesmo formato, das Verticais 1/3). Nenhuma micro-persona escrita à mão sem lastro na `market-research`
- [ ] **Vocabulário do mercado:** zero termos de `market_vocabulary.words_absent[]` em qualquer peça; zero termos com `saturated_in_market: true` em headline/hook (só como prova no corpo). `absent_terms_used` e `saturated_terms_in_headlines` = 0 no `vocabulary_summary`
- [ ] **Zona emocional e arco (ETAPA 4.5.E):** todo conceito e todo hook com `valence` + `intensity` declarados; `valence_open` → `valence_close` gravado e **fechando em valência alta** (única exceção aceita: `valence_arc_owner: "landing_page"` para image ad de curiosidade). Conceito que abre e fecha na mesma zona baixa não sai
- [ ] Hooks Bank cobre as 4 zonas (≥1 hook em cada) e, se a `ad-analysis` já apontou zona vencedora, ≥2 hooks nela
- [ ] Todo hook (dos conceitos E do Hooks Bank) com `emotion_dominant` (1 das 4 Hook Emotions, derivado da zona) + hook archetype declarados (ETAPA 4.5.E)
- [ ] Hook/primary text/headline que nasceu de frase real tem `voc_source` apontando pra `market-research` (ETAPA 4.5.F); os demais com `voc_source: null`
- [ ] `hook_swap_viable` declarado por conceito (ETAPA 4.5.G)
- [ ] Primary texts meaningfully different (estrutura+ângulo+hook, não cosmético); headlines com frames distintos (ETAPA 5)

**Estilo e upload:**
- [ ] Passada de estilo (ETAPA 7.5): zero travessão em headlines (≤2 em copy longa); nenhuma peça pública com aviso, disclaimer ou claim suavizado por iniciativa da skill
- [ ] Renders in-session (se houve) passaram pelo limpador de metadados e estão como `asset-xxxx` com `metadata_clean: true`; o resumo de produção lista a limpeza como último passo antes do upload (ETAPA 4.5.I / regra 12)

**Entregáveis e handoff:**
- [ ] Entregável de produção por conceito conforme a rota (ETAPA 5.7): Rota A = prompts em `prompts/` + `prompts-index.json` (+ `renders/` se MCP rendeu); Rota B = `concept-XX-edl.md` com tabela timecode + bloco de usage rights; Mix = cada conceito no seu ramo
- [ ] LP congruency documentada por conceito (ETAPA 6): destino + message/visual/promise match
- [ ] Hooks Bank com 10 hooks categorizados no `.md` E no array top-level `hooks_bank[]` do dados.json (ETAPA 7 — contrato com os checks H1/M3 da Skill `consistency-audit`)
- [ ] `dados.json` completo no schema: `emotion_dominant`/`archetype`/`awareness_level` no NÍVEL do concept (contrato com o gate H4 da `consistency-audit`), mais os campos novos `testing_method`, `angle` (frase), `concept_type`, `sub_avatar_id`, `valence`/`intensity`/`valence_open`/`valence_close`, `angles[]`+`hold_universal*` nos conceitos `marksman`, e `iteration_of` preenchido em todo conceito que é iteração (null nos novos); `vocabulary_summary` preenchido, `production_route`/`ai_video_model` gravados
- [ ] DNA extraction rodada por criativo (ETAPA 7.6) ou erro logado em `extraction-errors.log` (não bloqueia)
- [ ] Instrução de UTM usa o schema canônico da Skill `ad-strategy` (`utm_content=[concept-id]-[creative-n]` + macros `{{ad.id}}`/`{{adset.id}}`) — nenhum formato próprio inventado
- [ ] Dual output: todo relatório `.md` com `.html` companion gerado pelo `tools/render_report.py` (isenções: `concept-NN-edl.md`, `prompts/*`, `renders/*`, `dados.json`); `manifest.json` atualizado + `build_index.py` rodado
