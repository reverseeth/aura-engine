# Content Recycler — prompt structured

Skill auxiliar invocável. Pega 1 winner e gera 9 derivadas.

## Como invocar

Membro digita uma das duas formas:

```
recycle [creative-id]
# ex: recycle <creative-id>
```

ou

```
recycle winner
# (sistema lê dados.winners[] já marcado pela skill 11 e ordena por spend_total)
```

## Fluxo da skill

### ETAPA 1 — Identificação do winner

1. Se `[creative-id]` fornecido (formato `c-NN`, que mapeia pra `concept-NN.md`):
   - PRIMEIRO abrir `workspace/[produto]/08-creative-engine/dados.json` (fonte estruturada), achar `concepts[]` cujo `id == creative-id`, e extrair dali os campos estruturados (hook, mechanism, avatar, voc_source, proof, cta).
   - Usar `workspace/[produto]/08-creative-engine/concept-NN.md` como brief complementar (texto longo, nuance de tom).
2. Se `winner`: ler `workspace/[produto]/11-ad-analysis/dados.json` e usar `dados.winners[]` — array JÁ filtrado pela skill 11 (`outcome == "winner"`). NÃO recomputar critério; ordenar por `spend_total` desc (tiebreak `days_active` desc) e pegar o topo. Se precisar de target pra exibir, ler explícito de `manifest.target_cpa`.
3. Se nenhum dos dois disponível: perguntar ao membro qual criativo reciclar

### ETAPA 2 — Extração de essência (rastreável, não inventada)

Antes de destilar, abrir as fontes pra herdar dados reais (nunca reparafrasear o que já é canônico):

- `workspace/[produto]/04-offer-builder/relatorio.md` (ou `04-offer-builder/dados.json`) → copiar o `mechanism_name` **LITERAL** pra `mechanism_name_canonical`. NÃO reparafraseie o nome do mecanismo.
- `workspace/[produto]/08-creative-engine/dados.json` → herdar `voc_source.ref_id` de cada hook do conceito fonte pra popular `voc_refs[]`.
- `workspace/[produto]/02-market-research/relatorio.md` (ou `02-market-research/dados.json`) → VOC real (frases exatas do consumidor, em inglês US literal) referenciadas por `voc_refs[]`.

Destilar em shape estruturado (valores extraídos das fontes acima, não pré-definidos):

```json
{
  "source_id": "<creative-id>",
  "big_idea": "<one-sentence thesis extraído do briefing>",
  "hook_essence": "<primeira frase/hook do criativo>",
  "mechanism": "<descrição do UMP/UMS em 5-12 palavras>",
  "mechanism_name_canonical": "<nome LITERAL do mecanismo, copiado de 04-offer-builder>",
  "voc_refs": ["<ref_id de cada VOC herdada de 08-creative-engine/dados.json / 02-market-research>"],
  "key_numbers": ["<Hopkins specificity numbers usados no criativo>"],
  "avatar": "<descrição resumida do avatar target>",
  "brand_voice": "<tom dominante derivado do briefing>",
  "proof_points": ["<proof points mais repetidos no briefing>"],
  "offer_core": "<garantia + pricing principal resumido>",
  "cta_essence": "<call to value final do criativo>",
  "forbidden_words": ["<red-flag words do CLAUDE.md + blocklist do membro>"]
}
```

**Sanity check (drift)**: se o `mechanism_name_canonical` extraído divergir do `mechanism_name` em `04-offer-builder`, PARE e surface ao membro (não auto-resolva) — é drift entre fases que precisa decisão dele.

Salvar em `workspace/[produto]/14-content-recycler/[source-id]/essence.json` pra referência de todos os formatos. O `essence.json` descritivo segue o `report_language` do membro; `voc_refs`/VOC literal permanecem em inglês US.

### ETAPA 3 — Consultar base Aura sobre cada formato (SISTEMAS NOMEADOS, não query genérica)

Antes de gerar cada derivada, puxar os SISTEMAS NOMEADOS do domínio **creatives-hooks-formats** rodando `search_knowledge` com a `best_query` de cada framework (`deep=true`). NUNCA use query genérica de canal. Índice completo do domínio em `.claude/lib/kb-index/` (`frameworks.json` + `README.md`). Curadoria de maior impacto por formato:

- **Advertorial / Blog SEO** →
  - `search_knowledge("Caples four U's hierarchy unique useful urgent ultra-specific headlines", deep=true)`
  - `search_knowledge("Hopkins specificity rule 1-2 second rule vague vs specific claims", deep=true)`
  - `search_knowledge("objection claim proof benefit cycle hold section one cycle", deep=true)`
- **Organic TikTok / YouTube pre-roll** →
  - `search_knowledge("gap theory of curiosity hooks counterintuitive open loop slippery slope", deep=true)`
  - `search_knowledge("video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds", deep=true)`
  - `search_knowledge("strategic pacing rapid cuts hook bridge solution CTA video editing rhythm", deep=true)`
- **Pinterest carousel / package insert (estáticos)** →
  - `search_knowledge("static image archetypes funnel position plain reminder direct response complexity rule", deep=true)`
  - `search_knowledge("13 winning static ad templates avatar callout nutella meme breakdown why it works", deep=true)`
- **Email sequence / SMS / Podcast ad** →
  - `search_knowledge("Big 4 Emotions NEW ONLY EASY ANYBODY SAFE PREDICTABLE BIG FAST", deep=true)`
  - `search_knowledge("Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles", deep=true)`
- **Transversal a TODAS as 9 (continuidade de mensagem)** →
  - `search_knowledge("congruency multiplier ad landing page offer visual message emotional continuity", deep=true)`

Demais sistemas do domínio (Hormozi Callout System, What-Who-When Matrix, SUCCESs, New Opportunity vs Improvement, Reeves USP-Demonstrate-USP, etc.) ficam disponíveis em `.claude/lib/kb-index/` pra puxar sob demanda quando o formato pedir.

### ETAPA 4 — Gerar cada derivada

Loop através de cada format em `formats.json`:

Pra cada formato:
1. Carregar format spec de `formats.json`
2. Construir prompt usando essence.json + format spec + knowledge base context
3. Gerar derivada respeitando `length_words`, `structure`, `tone`
4. Rodar Compliance Pre-flight (`.claude/lib/compliance-preflight/checker.md`)
5. Se severity >= high: auto-rewrite e log
6. Salvar em `workspace/[produto]/14-content-recycler/[source-id]/[output_file]`

### ETAPA 5 — Gerar índice + relatório

Criar `workspace/[produto]/14-content-recycler/[source-id]/README.md` (relatório interno → segue `report_language` do membro; as 9 derivadas em si permanecem em inglês US):

```markdown
# Content Recycler Output — [source-id]

Gerado em [timestamp] a partir de [source file].

## Essence extraída
- Big idea: [...]
- Mechanism: [...]
- Avatar: [...]

## 9 formatos gerados

| Formato | Arquivo | Palavras | Compliance |
|---|---|---|---|
| Advertorial 1500w | advertorial-1500w.md | 1540 | ✅ low |
| Email sequence | email-sequence.md | 1080 | ✅ low |
| Organic TikTok 20s | organic-tiktok-20s.md | 78 | ⚠️ medium (1 trigger) |
| Blog SEO post | blog-seo-post.md | 1820 | ✅ low |
| Pinterest carousel | pinterest-carousel-8.md | 290 | ✅ low |
| YouTube pre-roll 15s | youtube-preroll-15s.md | 48 | ✅ low |
| SMS welcome | sms-welcome.md | 24 | ✅ low |
| Package insert | package-insert.md | 165 | ✅ low |
| Podcast host-read 30s | podcast-ad-30s.md | 88 | ✅ low |

## Como usar

Cada formato foi derivado da mesma essência do winner [source-id]. Os prompts foram calibrados pra cada canal respeitar: comprimento, estrutura, tom, e restrições de compliance.

**Próximos passos sugeridos:**
- Advertorial: publicar em blog ou landing page secundária
- Email sequence: importar no Klaviyo/Attentive, ligar como flow de welcome
- Organic TikTok: postar em conta orgânica, sem pixel
- Blog SEO: publicar em /blog, registrar no Search Console, submit sitemap
- Pinterest: criar board temático, pin um slide por semana
- YouTube pre-roll: subir como campaign separada (não mesma audience do Meta)
- SMS: wire no Postscript/Attentive como trigger de opt-in
- Package insert: mandar pro fornecedor imprimir
- Podcast: outreach pra shows relevantes do nicho

## Gerar outros formatos

Caso queira adicionar formato novo (ex: LinkedIn, Substack, Twitter thread), edit `.claude/lib/content-recycler/formats.json` adicionando novo entry com especificação.
```

### ETAPA 5.5 — Companions .html (dual output — rule 6b)

Pra CADA `.md` salvo nesta pasta (README.md + as 9 derivadas) gerar o `.html` companion correspondente no mesmo diretório (`README.html`, `advertorial-1500w.html`, ... `podcast-ad-30s.html`). São 9 `.html` de derivada + `README.html`.

- Copiar o CSS completo de `.claude/templates/aura-report-template.html` (inline, self-contained, sem server; manter responsividade mobile).
- Abrir o `<body>` com o bloco SVG da logo copiado **LITERALMENTE** de `.claude/templates/aura-logo-snippet.html` (6 linhas, sem alterações). PROIBIDO substituir por texto "AURA"/"Aura Engine". Sem fallback textual.
- O HTML do README segue o `report_language` do membro; o HTML das 9 derivadas reflete o conteúdo consumidor-final em inglês US.

### ETAPA 6 — Compliance log consolidado

Salvar log consolidado em `workspace/[produto]/14-content-recycler/[source-id]/compliance-log.json`:

```json
{
  "source_creative": "<creative-id>",
  "recycled_at": "2026-04-17T...",
  "formats_generated": 9,
  "compliance_summary": {
    "all_low": true,
    "total_triggers": 1,
    "critical": 0,
    "high": 0,
    "medium": 1,
    "low": 0
  },
  "by_format": {
    "advertorial_1500w": {"severity": "low", "triggers": []},
    "organic_tiktok_20s": {"severity": "medium", "triggers": [{"phrase": "...", "reason": "..."}]},
    ...
  }
}
```

## Estrutura final de arquivos

```
workspace/[produto]/14-content-recycler/
└── <creative-id>/
    ├── README.md                     ← índice + instruções
    ├── README.html                   ← companion humano (rule 6b)
    ├── essence.json                  ← essência extraída (pra reuso)
    ├── compliance-log.json           ← log consolidado
    ├── advertorial-1500w.md          (+ .html)
    ├── email-sequence.md             (+ .html)
    ├── organic-tiktok-20s.md         (+ .html)
    ├── blog-seo-post.md              (+ .html)
    ├── pinterest-carousel-8.md       (+ .html)
    ├── youtube-preroll-15s.md        (+ .html)
    ├── sms-welcome.md                (+ .html)
    ├── package-insert.md             (+ .html)
    └── podcast-ad-30s.md             (+ .html)
```

## Custo estimado

- ~10-12 chamadas Claude (extração essência + 9 derivadas + compliance em cada)
- Tokens totais: ~40-60k
- Custo: ~$0.10-0.30 em tokens (Sonnet) ou incluso na assinatura Claude Code

## Tempo

- Geração paralela: 3-5 minutos
- Geração sequencial: 8-12 minutos

## Observações

- **Não reinventar wheel**: se já tem email flow no Klaviyo com performance, recyler gera variação alternativa pra A/B, não substitui
- **Idioma do destino**: derivadas seguem mesma language do criativo fonte (US market default = English)
- **Brand voice lock**: essence.json inclui `brand_voice` — todas derivadas respeitam
- **Forbidden words**: herdadas do CLAUDE.md (rules 8b) + qualquer blocklist específica do membro
