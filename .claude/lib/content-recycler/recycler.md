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
# (sistema identifica automaticamente o top CPA dos últimos 7 dias)
```

## Fluxo da skill

### ETAPA 1 — Identificação do winner

1. Se `[creative-id]` fornecido: ler `/workspace/[produto]/07-creatives/07-concept-XX.md` correspondente
2. Se `winner`: consultar `/workspace/[produto]/09-analysis/latest.json` (se existir) e pegar o criativo com menor CPA e spend > $300
3. Se nenhum dos dois disponível: perguntar ao membro qual criativo reciclar

### ETAPA 2 — Extração de essência

Ler o criativo fonte e destilar em shape estruturado (valores são extraídos do briefing do membro, não pré-definidos):

```json
{
  "source_id": "<creative-id>",
  "big_idea": "<one-sentence thesis extraído do briefing>",
  "hook_essence": "<primeira frase/hook do criativo>",
  "mechanism": "<descrição do UMP/UMS em 5-12 palavras>",
  "key_numbers": ["<Hopkins specificity numbers usados no criativo>"],
  "avatar": "<descrição resumida do avatar target>",
  "brand_voice": "<tom dominante derivado do briefing>",
  "proof_points": ["<proof points mais repetidos no briefing>"],
  "offer_core": "<garantia + pricing principal resumido>",
  "cta_essence": "<call to value final do criativo>",
  "forbidden_words": ["<red-flag words do CLAUDE.md + blocklist do membro>"]
}
```

Salvar em `/workspace/[produto]/17-recycled/[source-id]/essence.json` pra referência de todos os formatos.

### ETAPA 3 — Consultar base Aura sobre cada formato

Antes de gerar cada derivada, consultar Aura knowledge base:
- `mcp__aura__search_knowledge("advertorial blueprint Zakaria 7 sections")`
- `mcp__aura__search_knowledge("email sequence welcome flow ecommerce")`
- `mcp__aura__search_knowledge("TikTok organic content creator voice")`
- `mcp__aura__search_knowledge("blog SEO E-E-A-T featured snippet")`
- `mcp__aura__search_knowledge("Pinterest carousel ecommerce conversion")`
- `mcp__aura__search_knowledge("YouTube pre-roll non-skippable 15s")`
- `mcp__aura__search_knowledge("SMS welcome message ecommerce copy")`
- `mcp__aura__search_knowledge("package insert onboarding DTC brand")`
- `mcp__aura__search_knowledge("podcast host-read ad copy")`

### ETAPA 4 — Gerar cada derivada

Loop através de cada format em `formats.json`:

Pra cada formato:
1. Carregar format spec de `formats.json`
2. Construir prompt usando essence.json + format spec + knowledge base context
3. Gerar derivada respeitando `length_words`, `structure`, `tone`
4. Rodar Compliance Pre-flight (`.claude/lib/compliance-preflight/checker.md`)
5. Se severity >= high: auto-rewrite e log
6. Salvar em `/workspace/[produto]/17-recycled/[source-id]/[output_file]`

### ETAPA 5 — Gerar índice + relatório

Criar `/workspace/[produto]/17-recycled/[source-id]/README.md`:

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

### ETAPA 6 — Compliance log consolidado

Salvar log consolidado em `/workspace/[produto]/17-recycled/[source-id]/compliance-log.json`:

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
/workspace/[produto]/17-recycled/
└── <creative-id>/
    ├── README.md                     ← índice + instruções
    ├── essence.json                  ← essência extraída (pra reuso)
    ├── compliance-log.json           ← log consolidado
    ├── advertorial-1500w.md
    ├── email-sequence.md
    ├── organic-tiktok-20s.md
    ├── blog-seo-post.md
    ├── pinterest-carousel-8.md
    ├── youtube-preroll-15s.md
    ├── sms-welcome.md
    ├── package-insert.md
    └── podcast-ad-30s.md
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
