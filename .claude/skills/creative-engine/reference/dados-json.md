# Creative Engine · Referência: SALVAR: outputs, schema do dados.json e manifest

> A lista completa de outputs por rota, o contrato com a `consistency-audit`, a tabela de mudanças de schema e quem consome cada campo, o JSON de referência do `dados.json` e a atualização do manifest. Abra ao salvar.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `creative-engine.md`, `concept-NN.md`, `hooks-bank.md`, `production-summary.md`). **Isentos** (arquivos operacionais de handoff — rule 6b do CLAUDE.md, lista completa em `.claude/lib/workspace-index/workspace-layout.md`): `concept-NN-edl.md`, `prompts/*`, `renders/*`, `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).

**Garantir diretório:** `mkdir -p workspace/[produto]/creative-engine/` antes de salvar.

Outputs em `workspace/[produto]/creative-engine/` (nomenclatura normalizada):

- `creative-engine.md` (estratégia macro — rota de produção escolhida, quantos conceitos, ângulos escolhidos, racional agregado)
- `concept-01.md`, `concept-02.md`, `concept-03.md` (briefs individuais — Etapa 5 completa, um arquivo por conceito)
- `hooks-bank.md` (Etapa 7 — 10 hooks alternativos)
- `production-summary.md` (Etapa 8 — resumo operacional)
- `dados.json` (manifest do batch — ver schema abaixo)
- **Rota A / conceitos `ai`:** `prompts/prompt-c01-video.txt`, `prompts/prompt-c01-image.txt`, ... (Etapa 5.7 Ramo A — prompts production-ready, um arquivo por conceito × formato; pasta `c0X-slug/` com shots quando Higgsfield multi-shot) + `prompts/prompts-index.json` (index — director/modelo/preset/formato) + `renders/asset-xxxx.mp4` (nome final, depois do Limpador de Metadados) quando o Higgsfield MCP rendeu in-session (ETAPA 0.7)
- **Rota B / conceitos `edl`:** `concept-01-edl.md`, ... (Etapa 5.7 Ramo B — roteiro de montagem por conceito, com tabela timecode + bloco de usage rights)
- **Rota C (Mix):** os dois tipos acima, conforme a rota de cada conceito

### JSON companion — `creative-engine/dados.json`

> **Contrato com a Skill `consistency-audit` (gate H4):** `emotion_dominant` (4 Hook Emotions: curiosity/urgency/fear/delight) e `archetype` ficam no NÍVEL do concept (não só dentro de `hooks[]`). Como os 3 criativos de um 3-2-2 compartilham conceito/awareness/intent, a emoção dominante do conceito = a emoção do hook principal. `awareness_level` é travado por conceito (Hard Rule A.0.2). O array `hooks_bank[]` (ETAPA 7) também é contrato com a `consistency-audit` (checks H1/M3).
>
> **Mudanças de schema desta versão e quem consome cada campo (declaração obrigatória — nenhum consumidor pode ser surpreendido):**
>
> | Campo | Antes | Agora | Quem lê / o que quebra |
> |---|---|---|---|
> | `concepts[].angle` | enum de 8 valores (`problem\|result\|curiosity\|social\|authority\|comparison\|controversy\|identification`) | **string em frase** (razão de compra), obrigatória, vinda de `sub_avatars[].angle` da Skill `market-research` | **Skill `consistency-audit`, gate H4 Dim 2** — hoje conta "≥3 angles distintos dos 8 possíveis". Com string livre, a contagem de distintos continua funcionando (frases distintas), mas o texto do gate que cita "os 8 possíveis" fica desatualizado e deve passar a contar `concept_type` OU frases distintas. **Skill `ad-analysis`** ao devolver `NEXT_BATCH_IDEAS.md` deve escrever ângulo em frase |
> | `concepts[].concept_type` | não existia | **enum de 8** (o enum antigo de `angle`, renomeado) — a embalagem do cânone §7 | **Skill `consistency-audit`, gate H4 Dim 2** (é o campo com cardinalidade fixa, o alvo natural do check de diversidade); `creative-dna` (`angle_vertical` continua lendo `vertical`, não muda) |
> | `concepts[].testing_method` + `angles[]` + `hold_universal*` | não existiam | `marksman\|sniper` + os 3 ângulos quando Marksman + o hold universal e sua validação | **Skill `ad-analysis`** (a leitura de um pack Marksman é "qual ângulo venceu", não "qual execução venceu"); **Skill `ad-strategy`** lê `testing_method` pra mapear o batch em ad sets (ETAPA 3.2 dela) |
> | `concepts[].valence` + `intensity` + `valence_open/close` | não existiam | zona emocional e arco | **Skill `ad-analysis`** (diagnóstico de iteração que trocou de zona); `creative-dna` (feature nova, opcional — o registry ignora campo desconhecido) |
> | `concepts[].emotion_dominant` | enum de 4, campo primário | **enum de 4, campo DERIVADO** de `valence`×`intensity` (mapa na ETAPA 4.5.E) | **Skill `consistency-audit`, gate H4 Dim 1** e `creative-dna` continuam funcionando sem alteração — é por isso que o campo permanece |
> | `concepts[].sub_avatar_id` | não existia | `id` do item de `sub_avatars[]` da Skill `market-research` | **Skill `ad-analysis`** (fecha o loop "qual sub-avatar produziu o vencedor"); **Skill `market-research`** é a produtora |
> | `concepts[].mold_id` + `mold_source` | não existiam | o `mold_id` do molde de `competitor-analysis/ad-molds.json` que deu a ESTRUTURA do conceito, mais o concorrente e o sinal de escala que o justificaram; `null` nos dois quando o conceito não usou molde | **Skill `ad-analysis`** (ETAPA 5: com um breakthrough na mão, o molde entra como variável candidata da vitória, junto com a contagem de conceitos do batch que usaram o mesmo molde). Nenhuma outra skill lê |
> | `concepts[].production_prompts.video.rendered_files[]` | existia só o escalar `rendered_file` (um caminho por CONCEITO) | **lista com 1 item por EXECUÇÃO** (`creative_n` 1..3 + `file`), porque as 3 execuções do pack 3-2-2 viram 3 ads distintos dentro do ad set do conceito (Skill `ad-strategy`, ETAPA 3.3) e cada uma precisa do seu binário | **Skill `ad-strategy`** e a receita `.claude/automations/recipes/upload-creative-to-meta.md` (sobem um binário por ad); **`.claude/automations/recipes/full-deploy.md`**, que hoje lê o escalar `rendered_file` e contorna pedindo os caminhos ao membro — passa a poder ler a lista |
>
> Nenhum campo foi removido. `angle` mudou de tipo (enum → string) — é a única mudança que exige ajuste de texto na Skill `consistency-audit`. **`rendered_file` (escalar) permanece como alias legado**, apontando pro arquivo da execução 1, só pra que a `full-deploy.md` não quebre antes de ser atualizada; leitores novos usam `rendered_files[]`.

## O `resumo`, o bloco que a próxima fase lê primeiro

O `dados.json` abre com um objeto `resumo`: até doze campos curtos com o que a fase seguinte precisa saber de primeira, sem abrir o arquivo inteiro. Ele não guarda dado novo, é espelho do que já está mais abaixo: cada campo copia o valor literal do campo de origem, e onde diverge, o campo de origem vence. Preencha por último, depois que o resto do arquivo estiver fechado.

```json
{
  "resumo": {
    "batch_id": "uuid",
    "concepts_count": 0,
    "total_assets": 0,
    "concept_lines": ["c-01 · tipo de conceito · ângulo em meia linha · emoção dominante"],
    "testing_method_by_concept": { "c-01": "sniper | marksman" },
    "production_route": "a rota de produção do batch",
    "platform_primary": "meta | tiktok | outra",
    "aspect_ratio_primary": "9:16",
    "hooks_bank_count": 0,
    "naming_convention": "o padrão de nome do ad que a ad-analysis lê"
  },
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
      "testing_method": "marksman|sniper",
      "_comment_testing_method": "cânone `.claude/lib/ad-taxonomy/README.md` §7. Default: primeiro teste em IMAGEM = marksman; primeiro teste em VÍDEO = sniper; conceito que É iteração = sniper (regra POR CONCEITO — direção nova no mesmo batch pode ser marksman). Define o que os 3 criativos variam entre si (ETAPA 4.5.A.0)",
      "iteration_of": null,
      "_comment_iteration_of": "OPCIONAL (string|null): creative_id do criativo ORIGINAL quando este conceito é iteração dele (nasceu de NEXT_BATCH_IDEAS.md ou de diretiva da `ad-analysis`/`scale-engine`); null pra conceito novo. Preencher no pré-flight, quando a iteração nasce. É a linhagem que a Skill `ad-analysis` usa como `original_ref` no `iteration_zone_check` — sem o campo, ela pareia por prosa do briefing",
      "angle": "frase completa que dá a razão de compra, ex: 'you're still waking up tired even after the magnesium'",
      "_comment_angle": "STRING EM FRASE, obrigatória — NUNCA um enum. Fonte: `sub_avatars[].angle` de `market-research/dados.json`, ou frase nova das Verticais 1/3 no mesmo formato. Uma palavra solta, um rótulo de formato ou um valor de `concept_type` aqui = reprovado (gate ETAPA 4.5.A.0.3). Em marksman este campo carrega o ângulo do criativo #1 e os 3 vivem em `angles[]`",
      "angles": [
        { "creative_n": 1, "angle": "frase", "sub_avatar_id": "sa-01" },
        { "creative_n": 2, "angle": "frase distinta", "sub_avatar_id": "sa-02" },
        { "creative_n": 3, "angle": "frase distinta", "sub_avatar_id": "sa-03" }
      ],
      "_comment_angles": "obrigatório quando testing_method=marksman (3 ângulos DISTINTOS, um por criativo); null quando sniper (os 3 criativos compartilham o `angle` do conceito)",
      "concept_type": "problem|result|curiosity|social|authority|comparison|controversy|identification",
      "_comment_concept_type": "a EMBALAGEM (cânone §7): a estratégia do teste, o que VOCÊ quer aprender. É o enum que antes ocupava o campo `angle` por engano. Conceito é sobre você; ângulo é sobre o cliente",
      "sub_avatar_id": "sa-01",
      "mold_id": "mold-slug|null",
      "mold_source": { "competitor": "nome da marca dona do anúncio", "scale_signal": "rank_do_anuncio|longest_running|aparicoes_repetidas|metrica_direta_de_spend" },
      "_comment_mold": "OPCIONAL (string|null + object|null): o molde do vídeo escalado que deu a estrutura deste conceito (ETAPA 5, `reference/molde-e-injecao.md`). `mold_id` copia o id do molde escolhido em `competitor-analysis/ad-molds.json`; `mold_source` copia `competitor` e `scale_signal` do item correspondente de `ad_molds.molds[]` no `competitor-analysis/dados.json`, com os mesmos nomes de campo. Os dois saem `null` juntos quando o conceito não usou molde (arquivo ausente, conceito de imagem/carrossel, ou nenhum molde encaixou no ângulo) — ausência se escreve `null`, nunca omitindo o campo. Quem lê é a Skill `ad-analysis` na ETAPA 5: num breakthrough, o molde entra como variável candidata da vitória, com a contagem de conceitos do batch que usaram o MESMO `mold_id` como denominador",
      "persona": "leitura humana do sub-avatar em 1 frase (as categorias combinadas), ex: 'quer dormir a noite inteira; já tentou magnésio e continuou acordando cansada'",
      "_comment_persona": "derivado de `sub_avatars[]` de `market-research/dados.json` pelo `sub_avatar_id` — a variável mestre do conceito. NÃO inventar micro-persona aqui; se o batch precisa do avatar amplo, a fonte é `core_avatar.surface_desire`",
      "labels_used": ["light sleepers"],
      "_comment_labels_used": "apelidos de `labels[]` da Skill `market-research` usados no call-out do primeiro beat",
      "hold_universal": "descrição do hold que sustenta os 3 ângulos (ancorado em core_avatar.surface_desire)|null",
      "hold_universal_validated": true,
      "_comment_hold_universal": "só em marksman: o hold precisa sustentar os 3 hooks, validado um a um. `false` bloqueia o conceito até reescrever o hold ou virar sniper. Em sniper ambos são null e o hold é específico/profundo por definição",
      "avatar_who": "quem grava/aparece no ad (ex: mulher 50s aparência real; sem pessoa = null)",
      "theme": "assunto que a copy ataca, em poucas palavras",
      "benefit_or_consequence": "benefit|consequence",
      "aesthetic_ref": "referência de senso estético em 1 linha (caseiro|polido + ritmo de cortes)",
      "vertical": "competitive|consumer|internal",
      "awareness_level": "unaware|problem_aware|solution_aware|product_aware|most_aware",
      "valence": "positive|negative",
      "intensity": "low|high",
      "valence_open": "negative/high",
      "valence_close": "positive/low",
      "valence_arc_owner": "ad|landing_page",
      "_comment_valence": "zona emocional de ABERTURA em `valence`+`intensity` (ETAPA 4.5.E); `valence_open`→`valence_close` é o arco obrigatório, que fecha SEMPRE em valência alta. `valence_arc_owner: landing_page` é a única exceção (image ad de curiosidade cujo arco sobe na página)",
      "emotion_dominant": "curiosity|urgency|fear|delight",
      "_comment_emotion_dominant": "campo DERIVADO de valence×intensity (mapa na ETAPA 4.5.E). Mantido porque o gate H4 Dim 1 da Skill `consistency-audit` e o registry `creative-dna` leem este nome. Quando a derivação for ambígua (curiosity/delight), a zona declarada prevalece",
      "archetype": "ai_ugc|licensed_montage|motion_graphics|founder_led|demo|creator_human",
      "funnel_position": "TOF|MOF|BOF",
      "hook_swap_viable": true,
      "format": "video_ugc|video_demo|static_image|carousel|motion_graphic",
      "duration_target_seconds": 22,
      "edl_file": "concept-01-edl.md|null",
      "_comment_edl_file": "preenchido só pra conceitos production_route=edl; null na rota ai (o entregável vira production_prompts)",
      "video_generation_mode": "split_takes|continuous|single_take|null",
      "word_count_spoken": 55,
      "word_count_within_limit": true,
      "hooks": [
        {
          "creative_n": 1,
          "text": "texto do hook",
          "angle": "a frase de razão de compra que este hook abre",
          "valence": "negative",
          "intensity": "high",
          "emotion_dominant": "curiosity",
          "call_out_label": "light sleepers|null",
          "voc_source": { "ref_id": "voc-001", "original_phrase": "...", "confidence": "direct_quote" }
        }
      ],
      "primary_texts": [
        { "text": "...", "variant": "A|B", "structure": "descrição da estrutura desta variante", "valence": "positive|negative", "intensity": "low|high", "voc_source": { "ref_id": "voc-001", "original_phrase": "...", "confidence": "direct_quote" } }
      ],
      "_comment_primary_texts": "`variant` substitui o antigo `angle: A|B` — as duas versões NÃO mudam o ângulo do conceito (ângulo é variável do criativo). O que varia é estrutura, entrada e zona emocional",
      "headlines": [
        { "text": "...", "frame": "benefit|urgency|offer|question", "voc_source": { "ref_id": "voc-001", "original_phrase": "...", "confidence": "direct_quote" } }
      ],
      "production_prompts": {
        "_comment": "preenchido só pra conceitos production_route=ai; pra route=edl, production_prompts=null e o entregável é edl_file",
        "video": {
          "_comment": "director continuous-script = modelo de geração contínua (Veo/Sora/Kling); rendered_files[] preenchido só quando o Higgsfield MCP rendeu in-session (ETAPA 0.7) — um item por EXECUÇÃO do pack 3-2-2, sempre os 3, com file:null pro que ainda não rendeu",
          "file": "prompts/prompt-c01-video.txt",
          "director": "marketing-studio-director|continuous-script",
          "model": "higgsfield|veo_3.1|sora_2|kling",
          "preset": "UGC|Tutorial|Unboxing|Hyper Motion|Product Review|TV Spot|Wild Card|UGC Virtual Try On|Pro Virtual Try On",
          "tool_url": "https://higgsfield.ai/marketing-studio",
          "rendered_files": [
            { "creative_n": 1, "file": "renders/asset-k3p9.mp4|null", "metadata_clean": true },
            { "creative_n": 2, "file": "renders/asset-7wq2.mp4|null", "metadata_clean": true },
            { "creative_n": 3, "file": "renders/asset-m1xd.mp4|null", "metadata_clean": true }
          ],
          "rendered_file": "renders/asset-k3p9.mp4|null"
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
      "_comment_category": "é a EMBALAGEM do hook (equivalente ao concept_type), não o ângulo",
      "angle": "a frase de razão de compra que este hook abre",
      "sub_avatar_id": "sa-01|null",
      "valence": "positive|negative",
      "intensity": "low|high",
      "emotion_dominant": "curiosity|urgency|fear|delight",
      "voc_source": { "ref_id": "voc-001", "original_phrase": "...", "confidence": "direct_quote|paraphrase|inferred_pattern" },
      "word_count": 8
    }
  ],
  "_comment_hooks_bank": "cobertura obrigatória: ≥1 hook em cada uma das 4 zonas de valence×intensity; ≥2 na zona vencedora quando a Skill `ad-analysis` já apontou uma",
  "total_assets": 3,
  "format": "3-2-2",
  "next_batch_ideas_applied": ["ref-01", "ref-02"],
  "vocabulary_summary": {
    "em_dash_in_headlines": 0,
    "absent_terms_used": 0,
    "saturated_terms_in_headlines": 0,
    "_comment_vocabulary": "gate de `market_vocabulary` da Skill `market-research`: `absent_terms_used` = ocorrências de `words_absent[]` em qualquer peça (tem que ser 0); `saturated_terms_in_headlines` = termos com `saturated_in_market: true` usados em headline/hook em vez de prova no corpo (tem que ser 0)"
  }
}
```

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete creative-engine` marca a skill em `skills_completed` (e valida o `creative-engine/dados.json` contra `.claude/templates/schemas/creative-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:
- Adicionar `creative-engine` em `skills_completed`
- Registrar `last_batch_id`, `batch_count`, e `next_batch_ideas_applied` (refs lidas de `ad-analysis/NEXT_BATCH_IDEAS.md`, se houver)
- Registrar `production_route` (`ai|edl|mix`) e, se rota envolve IA, `ai_video_model` (pra a próxima execução já assumir a rota/modelo do membro sem reperguntar — só confirmar)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html)
