# Hook Taxonomy

Catálogo de archetypes de hook pra ad creatives. Usado pela Skill 08 (creative-engine) pra gerar variações com cobertura de emotions e formatos diferentes, e pela Skill 03 (competitor-analysis) pra classificar criativos escalados dos concorrentes.

## Estrutura

- `archetypes.json` — definição estruturada de cada archetype (id, name, emotion dominante, signals de identificação, estrutura-tipo, format_fit)
- `README.md` — este arquivo, descrição humana dos padrões

O `format_fit` de cada archetype usa o enum canônico de `format` do `.claude/lib/creative-dna/feature_schema.json` — mesmo vocabulário do registry, então dá pra cruzar "archetype X performa em formato Y" com o creative DNA.

## Archetypes (Big 4 emotions as anchors)

Cada hook tem UMA emoção dominante. Archetypes são cortes mais finos dentro das 4 emotions.

### Curiosity-dominant

| Archetype | Signal | Estrutura-tipo |
|-----------|--------|-----------------|
| `pattern_interrupt` | Cena visual inesperada + pergunta | "Why is [X] doing [Y]?" / visual surpreendente |
| `secret_reveal` | "The one thing nobody tells you" | "[Authority] never told you about [topic]" |
| `contrarian` | Desafia consenso | "Everyone says [X]. They're wrong." |
| `listicle_open` | "3 things I wish I knew" | Número + promessa de lista rápida |
| `question_hook` | Pergunta incompleta que força completar | "Ever wondered why [observation]?" |

### Urgency-dominant

| Archetype | Signal | Estrutura-tipo |
|-----------|--------|-----------------|
| `tempo_escasso` | Janela explícita de tempo | "Only [N] hours left" |
| `ultima_chance` | Stock/oportunidade acabando | "Last [N] in stock" |
| `trend_expiring` | Momento cultural fugaz | "Before [event/season] ends" |
| `missed_opportunity` | Consequência de não agir | "If you don't do this now, [outcome]" |

### Fear-dominant

| Archetype | Signal | Estrutura-tipo |
|-----------|--------|-----------------|
| `pain_amplification` | Dor atual explícita + visual | "Still dealing with [pain]?" |
| `warning` | Alerta sobre algo que o avatar faz errado | "Stop doing [X] before [consequence]" |
| `comparative_loss` | Outros tendo resultado, você não | "Everyone else [has outcome] — why not you?" |
| `regret_future` | Future pacing negativo | "In 10 years, you'll wish you had..." |

### Delight-dominant

| Archetype | Signal | Estrutura-tipo |
|-----------|--------|-----------------|
| `transformation` | Before-after implícito | "[Person] had [problem], now [outcome]" |
| `aspiration` | Future self positivo | "Imagine waking up and [outcome]" |
| `discovery` | Descoberta que resolve | "I found the [thing] that actually [benefit]" |
| `peer_validation` | Social proof de semelhante | "[N] people like you already [outcome]" |

## Regras de uso

1. **Cada hook declara 1 archetype + 1 emotion** (não múltiplos). Se o hook encaixa em 2, escolher o dominante.
2. **Archetype NÃO substitui VOC traceability** — todo hook ainda precisa linkar a VOC phrase no `02-market-research/dados.json` (ou marcar `voc_source: null, requires_manual_review: true`).
3. **Cobertura por batch**: um batch de N conceitos deve cobrir ≥ 2 emotions diferentes e ≥ 3 archetypes distintos (diversidade de cobertura = escala).
4. **Archetype ≠ formato**: um `pain_amplification` pode ser UGC humano, AI UGC, motion graphic, ou static. Formato é decisão separada.

## Exemplos genéricos (template — NUNCA copiar literal)

> "Why is every [professional demographic] reaching for [product category] this season?" — `pattern_interrupt` / curiosity

> "Last [N] at this price — [promo] ends Sunday." — `tempo_escasso` / urgency

> "Still using [old solution] that [problem]?" — `pain_amplification` / fear

> "I spent [time] trying [alternatives]. Then I found this." — `discovery` / delight

Esses são ilustrativos. Sempre gerar o hook específico pro produto/avatar/VOC do membro.

## Integração com Skills

- **Skill 03 Etapa 3C** (scaled creative deep analysis): classifica criativos escalados dos concorrentes usando esse taxonomy. Preenche `hook_archetypes[]` em `03-competitor-analysis/creative-patterns.json`.
- **Skill 08 Etapa 4.5.E + Etapa 7**: cada hook gerado declara archetype + emotion. Hooks Bank final tem cobertura balanceada. Na ETAPA 7.6, o archetype declarado entra no registry via a feature `hook_archetype` do creative DNA (`feature_schema.json`).
- **Skill 11** (ad-analysis): ao marcar winners/losers, a performance conecta-se ao `hook_archetype` já registrado — o padrão por archetype emerge no `dna-profile.json` ao longo do tempo.
