# Creative Engine · Referência: Depois dos briefings (ETAPAs 6, 7, 7.5 e 7.6)

> LP congruency por conceito, o Hooks Bank com os sistemas de hook da base, a passada final de estilo e a extração silenciosa de DNA. Abra na ETAPA 6.

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

> As 4 categorias acima são **embalagens** (`concept_type`), não ângulos. Cada hook do bank ainda declara o **ângulo em frase** que ele abre — hook sem ângulo é hook sem razão de compra (gate da ETAPA 4.5.A.0.3).

Cada hook deve declarar:
- **Zona emocional**: `valence` (positive/negative) × `intensity` (low/high) — ETAPA 4.5.E. **Cobertura obrigatória do bank:** pelo menos 1 hook em cada uma das 4 zonas, e se há winners na `ad-analysis`, pelo menos 2 hooks na zona vencedora
- 4 Hook Emotions dominante (curiosity/urgency/fear/delight) — camada inferior, derivada da zona
- **Ângulo (frase)** que o hook abre, e o `sub_avatar_id` de origem quando houver
- VOC source (ref ao `market-research/dados.json`, conforme Etapa 4.5.F)
- Word count (≤ 10 palavras ideal pro primeiro beat do vídeo)
- Aspect ratio: 9:16 (sempre)

Cada hook = 1-2 frases, formato de vídeo hook ou image headline.

Esses hooks ficam na biblioteca pra iteração futura. **Além do `hooks-bank.md`, grave os 10 hooks no array top-level `hooks_bank[]` do `creative-engine/dados.json`** (mesma estrutura de `concepts[].hooks[]` + campo `category` — schema abaixo). É por esse array que a Skill `consistency-audit` audita a rastreabilidade VOC e o uso correto do bank (checks H1/M3) — hook só no `.md` fica invisível pro gate.

> O DNA aprendido (dna-profile.json) já foi carregado no "Contexto a carregar" (item 6) e enviesou a ideação desde a ETAPA 3 — não há step de DNA aqui.

### ETAPA 7.5 — Passada final de estilo

Antes de salvar: travessão (—) zero em headlines, ≤2 em copy longa (8a); nenhuma peça pública com aviso, disclaimer ou claim suavizado por iniciativa da skill (8b); todo arquivo em `renders/` passou pelo limpador de metadados e tem nome `asset-xxxx` (item I da ETAPA 4.5).

### ETAPA 7.6 — DNA Registry Extraction (silent)

Após os briefings e o hooks bank, pra cada criativo gerado:

1. Ler `.claude/lib/creative-dna/feature_schema.json` e `.claude/lib/creative-dna/extractor.md`
2. Rodar o extractor prompt com:
   - Briefing completo do criativo
   - Awareness level dominante do market research
   - Hook archetype declarado na ETAPA 4.5.E (id de `.claude/lib/hook-taxonomy/archetypes.json`) — a extração é schema-driven (a feature `hook_archetype` do `feature_schema.json` flui automaticamente), mas o PROMPT do `extractor.md` pede o archetype declarado explicitamente; é o que fecha o loop archetype→DNA prometido pelo hook-taxonomy
3. Parse JSON response (features estruturadas conforme schema)
4. Salvar em `workspace/[produto]/creative-dna/features-[creative-id].json`
5. Invocar (passar o caminho COMPLETO do features file — `registry.py add` abre o arquivo direto; passar só o nome quebra com FileNotFoundError e o DNA nunca popula):
   ```
   python3 .claude/lib/creative-dna/registry.py init workspace/[produto]  # se ainda não inicializado
   python3 .claude/lib/creative-dna/registry.py add workspace/[produto] [creative-id] workspace/[produto]/creative-dna/features-[creative-id].json --product [slug]
   ```

Silent pro membro. Se extração falhar (Claude retorna malformed JSON), logar erro em `workspace/[produto]/creative-dna/extraction-errors.log` mas não bloquear skill.
