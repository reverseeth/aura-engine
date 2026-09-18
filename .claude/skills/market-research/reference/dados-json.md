# Market Research · Referência: JSON companion, o schema do dados.json

> O schema completo do `market-research/dados.json` com os comentários de contrato (`voc_top20`, ids estáveis, `core_avatar`, `sub_avatars[]`, `labels[]`, `market_vocabulary`, `avatar`, objeções, soluções alternativas, causas raiz e implicações estratégicas) e a nota do VOC em inglês. Abra ao gravar o `dados.json`.

## O `resumo`, o bloco que a próxima fase lê primeiro

O `dados.json` abre com um objeto `resumo`: até doze campos curtos com o que a fase seguinte precisa saber de primeira, sem abrir o arquivo inteiro. Ele não guarda dado novo, é espelho do que já está mais abaixo: cada campo copia o valor literal do campo de origem, e onde diverge, o campo de origem vence. Preencha por último, depois que o resto do arquivo estiver fechado.

```json
{
  "resumo": {
    "dominant_awareness": "problem_aware",
    "sophistication_stage": 3,
    "core_avatar_line": "quem é, em uma frase, com a dor principal",
    "core_problem": "o problema central em uma frase",
    "core_desire": "o desejo central em uma frase",
    "top_objection": "a objeção que mais aparece",
    "voc_top5": ["frase literal do cliente, em inglês", "…"],
    "sub_avatar_ids": ["sa-1: ângulo em meia linha", "…"],
    "market_labels": ["como o mercado chama a categoria"],
    "alternative_solutions_top3": ["o que a pessoa faz hoje no lugar"],
    "voc_adequacy": "ok | insuficiente",
    "blocked_skills": []
  },
  "awareness_distribution": { "unaware": 0, "problem_aware": 0, "solution_aware": 0, "product_aware": 0, "most_aware": 0 },
  "awareness_distribution_source": "default|user_estimate|hybrid|web_signals",
  "dominant_awareness": "problem_aware",
  "dominant_awareness_secondary": "solution_aware",
  "_comment_dominant_awareness_secondary": "campo OPCIONAL — só existe quando dois níveis adjacentes empataram (±5pp). dominant_awareness leva o de MAIOR intenção de compra; este campo guarda o outro. Ausente = sem empate (downstream trata como nível único)",
  "sophistication_stage": 3,
  "sophistication_confidence": "high|medium|low",
  "voc_phrases": { "problem": ["..."], "desire": ["..."], "frustration": ["..."] },
  "voc_top20": [
    { "id": "voc-001", "rank": 1, "phrase": "frase exata em inglês US", "count": 8, "category": "problem|desire|frustration" }
  ],
  "_comment_voc_top20": "as 20 frases mais fortes ranqueadas por frequência de menção (curadoria da ETAPA 5) — a Skill `copy-engine` lê ESTE campo pro voc_checklist da copy",
  "_comment_voc_ids": "contrato de rastreabilidade: `id` é a identidade ESTÁVEL da frase (`voc-001`, `voc-002`…), cunhada na ordem do rank da PRIMEIRA execução — namespace único pro produto inteiro, compartilhado entre voc_top20 e todo voc_evidence[] (a mesma frase leva o MESMO id onde aparecer; quote de voc_evidence fora do top20 cunha o próximo número livre). Em re-execução: frase existente MANTÉM o id (mesmo mudando rank/count), frase nova entra em append com o próximo número, id nunca é renumerado nem reaproveitado. CONSUMIDORES: Skill `copy-engine` (voc_refs da copy), Skill `creative-engine` (voc_source.ref_id de cada hook/primary/headline) e Skill `content-recycler`/recycler (voc_refs herdadas via `creative-engine`) rastreiam cada linha produzida até a frase de origem por ESTE id — id instável quebra a rastreabilidade retroativa de tudo que já foi gerado",
  "voc_count": 0,
  "voc_adequacy": "ok|medium|insufficient",
  "skills_blocked": [],
  "sources": {
    "voc_sources": { "amazon": 0, "reddit": 0, "tiktok": 0, "trustpilot": 0, "forums": 0, "survey": 0, "warm_call": 0, "product_research_brand_bank": 0 },
    "awareness_distribution_source": "user_estimate|default|hybrid|web_signals",
    "blocked_sources": [{"source": "", "reason": "http_403|captcha|login_wall|timeout"}]
  },
  "core_avatar": {
    "category": "desire",
    "surface_desire": "I want my skin to stop feeling tight and itchy after every shower",
    "core_desire_behind": "health|status|sex|belonging|control|comfort",
    "scope": "high|med|low",
    "urgency": "high|med|low",
    "staying_power": "high|med|low",
    "labels": ["dry skin"],
    "voc_evidence": [
      { "id": "voc-001", "quote": "frase exata em inglês US", "source": "reddit|amazon|tiktok|youtube|trustpilot|forum|ad_library|survey|warm_call" }
    ]
  },
  "_comment_core_avatar": "o avatar central da ETAPA 4.5, construído com UMA categoria só (`category` = uma das Core Five: desire|experience|emotion|behavior|demographic — desire em praticamente todo caso). `surface_desire` é a unidade de construção e cabe na frase 'I want X'; `core_desire_behind` é o instinto por trás e orienta TOM, não construção. CONSUMIDORES: Skill `copy-engine` (define a quem a página e a copy se dirigem) e Skill `creative-engine` (base da persona de cada conceito)",
  "sub_avatars": [
    {
      "id": "sa-01",
      "name": "the magnesium tried-it",
      "categories_used": ["desire", "experience"],
      "desire": "I want to sleep through the night",
      "experience": "tried magnesium, still woke up tired",
      "emotion": "",
      "behavior": "",
      "demographic": "",
      "labels": [],
      "angle": "Why magnesium only fixed half of your sleep problem",
      "voc_evidence": [
        { "id": "voc-001", "quote": "frase exata em inglês US", "source": "reddit|amazon|tiktok|youtube|trustpilot|forum|ad_library|survey|warm_call" }
      ]
    }
  ],
  "_comment_sub_avatars": "cada sub-avatar combina 2+ das Core Five e SEMPRE tem `desire` preenchido. A ordem dos campos é a ordem de importância do material (desire → experience → emotion → behavior → demographic): demografia vem POR ÚLTIMO e só quando refina de verdade; categoria não usada fica string vazia. `angle` é obrigatório e ÚNICO por sub-avatar — é a razão de compra em frase completa, voltada ao cliente (se não dá razão de compra, é conceito, não ângulo). CONSUMIDORES: Skill `creative-engine` lê ESTE campo como Persona/Micro-persona (a variável mestre de cada conceito) e `angle` como ângulo de entrada; Skill `copy-engine` usa o mesmo recorte pra escolher o foco da copy",
  "labels": [
    { "label": "night shifter", "refers_to": "quem trabalha turno da noite e dorme de dia", "source": "reddit|amazon|tiktok|youtube|forum|ad_library", "voc_quote": "" }
  ],
  "_comment_labels": "os apelidos que o próprio mercado usa pra se descrever (ETAPA 4.5) — esta é a lista completa, com origem e frase de apoio; os campos `labels` dentro de `core_avatar` e de `sub_avatars[]` são só os termos (strings) que apontam pra ela. CONSUMIDORES: Skill `copy-engine` (entram literalmente na copy — usar a palavra com que o mercado se nomeia gera identificação) e Skill `creative-engine` (call-out do primeiro beat do criativo). Também servem de termo de busca pra achar mais gente igual numa próxima rodada de pesquisa",
  "market_vocabulary": {
    "words_used": [
      { "term": "smoother", "count": 0, "category": "problem|desire|frustration", "saturated_in_market": false }
    ],
    "words_absent": [
      { "term": "hydrated", "used_by": "brand|industry|competitor", "occurrences_in_research": 0, "market_says_instead": "smoother / less dry" }
    ]
  },
  "_comment_market_vocabulary": "teste do Ctrl+F da ETAPA 5. `words_used` = vocabulário REAL observado, com a contagem de ocorrências; `saturated_in_market: true` quando o termo também domina os claims dos concorrentes da ETAPA 3 (mensagem fatigada — serve de prova no corpo do texto, nunca de headline). `words_absent` = termos da marca/indústria com zero (ou quase zero) ocorrência na base — PROIBIDOS na copy, com o substituto real ao lado. CONSUMIDORES: Skills `copy-engine` e `creative-engine` consultam ANTES de escrever qualquer linha",
  "avatar": {
    "psychographics": {},
    "pain_hierarchy": [
      { "rank": 1, "item": "", "emotional_layer": "", "frequency": "high|med|low", "voc_quote": "" }
    ],
    "desire_hierarchy": [
      { "rank": 1, "item": "", "emotional_layer": "", "frequency": "high|med|low", "voc_quote": "" }
    ],
    "demographics": {}
  },
  "_comment_avatar": "camada descritiva do mercado (ETAPA 4) — demografia fica por último porque é a que menos gera motivação de compra. A camada ACIONÁVEL, que as Skills `copy-engine` e `creative-engine` leem pra decidir pra quem cada peça fala, é `core_avatar` + `sub_avatars[]`, não este objeto",
  "trigger_events": [
    { "type": "pre_event|deadline|pain_peak|social", "description": "", "voc_quote": "" }
  ],
  "objections": [
    { "type": "price|efficacy|safety|effort|skepticism|identity", "quote": "", "break_strategy": "" }
  ],
  "alternative_solutions": [
    { "category": "", "perceived_benefit": "", "weakness_exploited": "" }
  ],
  "root_cause_candidates": [],
  "strategic_implications": { "page_type": "", "lead_type": "", "mechanism_type": "", "top_angles": [] }
}
```

> **VOC permanece SEMPRE no idioma original do consumidor (inglês US).** Todos os campos `voc_quote` e `voc_phrases` são matéria-prima literal — nunca traduzir, mesmo com `report_language: "pt-BR"`. Eles vão pra copy e criativos exatamente como o consumidor falou.
