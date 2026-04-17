# Compliance Pre-flight

Classifier que prevê probabilidade de disapproval do Meta Ads / TikTok Ads
antes de submeter copy/ad. Abordagem A — Claude-based, zero infra externa.

## Como funciona

1. Qualquer copy/ad/page text é passado pelo `checker.md` prompt
2. Claude avalia contra 5 eixos: Meta Policy, FTC substantiation, FDA cosmetic boundary, red-flag words, claim credibility
3. Retorna risk score 0-100 + triggers específicos + rewrite sugerido

## Onde é invocado

**Skill 05 (copy-engine)** — antes de finalizar cada peça de copy (headlines,
primary texts, advertorial, PDP sections)

**Skill 07 (creative-engine)** — antes de finalizar cada briefing (scripts,
voiceover, text overlays)

**Skill 11+ qualquer** — invocável on-demand via `compliance check [arquivo]`

## Output

JSON estruturado com:
- `risk_score` 0-100
- `severity` low/medium/high
- `triggers[]` — phrase + why + policy violated
- `rewrite_suggestion`
- `alternative_claims[]` — 3 variações compliant

## Integração com Skills

Cada skill que gera copy ao consumidor final DEVE:

1. Gerar copy normalmente
2. Antes de salvar final, rodar Compliance Pre-flight
3. Se `risk_score >= 30`, aplicar rewrite ou apresentar ao membro
4. Se `risk_score < 30`, salvar

Silent quando baixo risco. Só "fala" quando detecta problema.

## Custo

Zero. Só tokens Claude da assinatura normal.

## Limitações

- ~80% accuracy vs Meta reviewer real
- Não captura política regional (EU, AU, LATAM variam)
- Não detecta visual elements (só texto)
- Abordagem B (classifier treinado em Meta Ad Library data) dá +10% accuracy
  mas requer setup Modal + training — roadmap futuro
