# Compliance Pre-flight

Classifier que prevê probabilidade de disapproval do Meta Ads / TikTok Ads
antes de submeter copy/ad. Dois passes: Claude-based (`checker.md`, nuance
completa) e heurístico standalone (`run.py`, word-boundary matching, CI-friendly).

## Como funciona

1. Qualquer copy/ad/page text é passado pelo checker (prompt `checker.md` ou `run.py`)
2. Avaliação contra 5 eixos: Meta Policy, FTC substantiation, FDA cosmetic boundary, red-flag words, claim credibility
3. Retorna JSON conforme `output-schema.json`: risk score 0-100 + `overall_verdict` + triggers + `rewrite_suggestions[]`

## CLI canônica (run.py)

```bash
python3 .claude/lib/compliance-preflight/run.py --file <path> [--vertical <v>] [--stage pre_ad|pre_page] --json
python3 .claude/lib/compliance-preflight/run.py --text "<copy>" [--vertical <v>] [--stage pre_ad|pre_page] --json
```

- `--vertical` usa o enum do manifest-schema (`product_vertical`); default `other`
- Matching por palavra inteira, case-insensitive ("secure" NÃO dispara "cure")
- Exit codes: `0` = pass/warning, `1` = critical

## Onde é invocado

**Skill 06 (copy-engine)** — sweep 8, antes de finalizar cada peça de copy (headlines,
primary texts, advertorial, PDP sections)

**Skill 08 (creative-engine)** — ETAPA 7.5, antes de finalizar cada briefing (scripts,
voiceover, text overlays)

**Skill 14 (content-recycler)** — cada derivada gerada

**Skill 07b (page-build) / Skill 10 (ad-strategy)** — GATE 1 mecânico via `run.py`
(`--stage pre_page` / `--stage pre_ad`), contrato na rule `pre-launch-gates.md`

**Qualquer skill on-demand** — invocável via `compliance check [arquivo]` em qualquer fase

## Output

JSON estruturado (contrato: `output-schema.json`) com:
- `risk_score` 0-100
- `severity` low/medium/high/critical
- `overall_verdict` **pass | warning | critical** — a decisão de gate
- `triggers[]` — phrase + why + policy violated (`informational: true` = só contexto, não pontua)
- `rewrite_suggestions[]` — SEMPRE presente; uma por flag, com a substituição padrão da rule 8b quando houver
- `rewrite_suggestion` — reescrita completa (só passe Claude, severity >= high)
- `alternative_claims[]` — 3 variações compliant (só passe Claude)

## Régua de decisão (ÚNICA — pelo overall_verdict)

| overall_verdict | Severity | Ação |
|-----------------|----------|------|
| `pass` | low | Salvar silenciosamente |
| `warning` | medium | Manter copy, logar warning + alertar membro |
| `critical` | high | Aplicar rewrite automático, logar, re-rodar até passar |
| `critical` | critical | PARAR, reportar ao membro, não salvar até aprovar |

Silent quando baixo risco. Só "fala" quando detecta problema.

## Custo

Zero. Só tokens Claude da assinatura normal (run.py nem usa tokens).

## Limitações

- ~80% accuracy vs Meta reviewer real
- Não captura política regional (EU, AU, LATAM variam)
- Não detecta visual elements (só texto)
- Abordagem B (classifier treinado em Meta Ad Library data) dá +10% accuracy
  mas requer setup Modal + training — roadmap futuro
