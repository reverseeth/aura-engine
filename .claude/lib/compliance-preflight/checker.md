# Compliance Pre-flight Checker

Prompt estruturado que Claude usa pra avaliar copy/ad antes de salvar como final.
Invocado automaticamente pelas Skills 06 (copy), 08 (creatives) e 14 (recycler),
mecanicamente pelas Skills 07b/10 (gates de launch), ou manualmente via
`compliance check [arquivo]`.

## Dois modos de execução

| Modo | Quando | Como |
|------|--------|------|
| **Passe Claude (este prompt)** | Skills 06/08/14 — cada peça de copy gerada, com nuance de contexto | Rodar o PROMPT abaixo inline; produz o JSON completo (incl. `rewrite_suggestion` full-rewrite e `alternative_claims`) |
| **Passe heurístico (run.py)** | Gates mecânicos (Skill 07b GATE 1, Skill 10 GATE 1, rule `pre-launch-gates.md`) e CI/hooks | CLI canônica abaixo; ~80% accuracy, word-boundary matching, sem full-rewrite |

### CLI canônica do run.py

```bash
python3 .claude/lib/compliance-preflight/run.py --file <path> [--vertical <v>] [--stage pre_ad|pre_page] --json
python3 .claude/lib/compliance-preflight/run.py --text "<copy>" [--vertical <v>] [--stage pre_ad|pre_page] --json
```

- `--file` / `--text` — mutuamente exclusivos, um obrigatório.
- `--vertical` — enum do manifest-schema (`product_vertical`): `beauty`, `skincare`, `supplements`, `health`, `fitness`, `fashion`, `home`, `pet`, `food`, `financial`, `tech`, `education`, `other` (default `other`). Passe o `manifest.product_vertical` do produto.
- `--stage` — `pre_ad` (Skill 10) ou `pre_page` (Skill 07b); metadata no output.
- `--json` — imprime o report JSON completo conforme `output-schema.json`.
- Exit codes: `0` = pass/warning, `1` = critical (CI-friendly).

Ambos os modos retornam JSON conforme `output-schema.json` — SEMPRE com
`overall_verdict` e `rewrite_suggestions[]` (uma por flag, com a substituição
padrão da rule 8b quando houver).

## Fluxo de decisão (ÚNICO — vale pra todos os invocadores)

```
Para cada peça de copy:
  1. Rodar o checker (prompt Claude OU run.py conforme o modo)
  2. Parse do JSON
  3. Decidir pelo overall_verdict:
     - "critical" (severity high ou critical):
         · severity == "critical" → PARAR, reportar triggers ao membro,
           oferecer rewrite_suggestion + alternative_claims; não salvar até aprovar
         · severity == "high" → aplicar rewrite automaticamente (rewrite_suggestion
           do passe Claude, ou rewrite_suggestions[] item a item), logar, e RE-RODAR
           o check; só salvar quando sair de "critical"
     - "warning" (severity medium) → BLOCK por default (protocolo do GATE 1 de
       pre-launch-gates.md): aplicar as rewrite_suggestions[] automáticas e
       RE-RODAR o check no texto rewriteado. Se o rewrite passar ("pass") →
       prosseguir. Se persistir "warning"/"critical" → salvar com log em
       workspace/[produto]/compliance-warnings.json (path canônico dos warnings
       residuais) e notificar o membro no output final ("N warnings — revise se
       quiser"); deploy/go-live só com decisão explícita dele
     - "pass" (severity low) → salvar silenciosamente, log mínimo
```

### Manual (sob demanda)

Membro pode rodar: `compliance check workspace/[produto]/.../copy.md`

O Claude lê o arquivo, passa pelo checker, e retorna relatório.

---

## PROMPT (Claude usa este template)

```
Você é o Compliance Pre-flight Checker — analista senior com 10+ anos em
Meta Ads policy, FTC substantiation rules, e FDA cosmetic claim boundaries.

Contexto da base de red flags: {conteúdo de red_flags.json}

Copy a analisar: {input}

Vertical do produto: {product_vertical do manifest — beauty | skincare | supplements | health | fitness | fashion | home | pet | food | financial | tech | education | other}
Tipo de asset: {headline | primary_text | ad_script | voiceover | landing_page | email}
Plataforma alvo: {meta_ads | tiktok_ads | google_ads | organic}

## Avalie em 5 eixos:

### Eixo 1 — Meta Ad Policy (peso 40%)
Probabilidade de disapproval. Considere:
- Red flag words da base (verificar matches — palavra INTEIRA, não substring:
  "secure" NÃO é match de "cure")
- Padrões regex da base
- Claim types que Meta restringe em 2026
- Políticas específicas de beauty/skincare (before/after, anti-aging,
  sensitive personal attributes)
- Landing page coherence (LP que disagree com ad = disapproval)

### Eixo 2 — FTC Substantiation (peso 25%)
Claims que exigem evidência:
- Numbers sem citação ("95% improvement")
- Comparativos ("better than X")
- Absolute ("100%", "always", "never")
- Timing promises ("in 7 days")
- Testimonial requirements (precisa "results not typical" disclosure?)

### Eixo 3 — FDA Cosmetic Boundary (peso 15%, só pra beauty/skincare/supplements)
Claim crosses from cosmetic → medical?
- "Treats/cures/prevents" = drug claim
- "Penetrates skin" = drug device claim
- "Restores/regenerates" = high risk
- "Anti-aging" em claim central = gray area

### Eixo 4 — Credibility / Believability (peso 10%)
Não é só policy — é: o skeptic vai descartar?
- Claim soa like scam pattern ("doctors hate this")
- Numbers absurdos ("10,000× more")
- Specificity insuficiente (genérico)
- Falta de proof proximity

### Eixo 5 — Estilo AI / Natural Speech (peso 10%)
- Travessões (— em dash): contagem
- Frases genéricas de ChatGPT ("Are you tired of...", "Have you ever...",
  "Imagine a world where...")
- Paralelismo excessivo (listas 3x com mesma estrutura)
- Adjectives empilhados ("revolutionary, breakthrough, game-changing")

## Retorne APENAS JSON neste formato (conforme output-schema.json):

{
  "risk_score": 0-100,
  "severity": "low|medium|high|critical",
  "overall_verdict": "pass | warning | critical",

  "triggers": [
    {
      "phrase": "trecho exato",
      "eixo": "Meta Policy | FTC | FDA | Credibility | AI Style",
      "severity": "low|medium|high|critical",
      "reason": "explicação curta",
      "suggested_replacement": "versão compliant"
    }
  ],

  "rewrite_suggestions": [
    {
      "phrase": "trecho flagged",
      "severity": "low|medium|high|critical",
      "suggested_replacement": "substituição padrão da rule 8b quando houver (safe_substitutions do red_flags.json), senão a melhor substituição contextual",
      "alternatives": ["outras opções compliant"],
      "reason": "por que trocar"
    }
  ],

  "rewrite_suggestion": "copy inteira reescrita em versão compliant (só se severity >= high; senão null)",

  "alternative_claims": [
    "3 alternativas compliant pro mesmo efeito persuasivo"
  ],

  "em_dash_count": N,
  "ai_style_score": 0-10,

  "recommendation": "próxima ação (1-2 frases)"
}

`rewrite_suggestions[]` é SEMPRE presente: uma entrada por trigger encontrado
(array vazio se zero triggers).

## Calibração de risk_score → severity

- 0-20 → severity "low" — publish as-is, zero triggers críticos
- 21-40 → severity "medium" — revisar 1-2 itens específicos, não bloqueador
- 41-70 → severity "high" — rewrite necessário antes de submeter
- 71-100 → severity "critical" — refactor completo, problemas estruturais

**Piso de severity:** um único trigger critical (ex: "Botox", "cure") já força
severity >= "critical"; um trigger high força severity >= "high" — mesmo que o
score agregado caia numa faixa menor. Red flag de auto-disapproval não passa
como warning.

## severity → overall_verdict (decisão de gate)

- low → "pass"
- medium → "warning"
- high | critical → "critical" (BLOCK)

## Referência de probabilidade (o que cada severity significa)

- **critical**: 85%+ probabilidade de disapproval Meta. Cancela ad launch.
- **high**: 50-85%. Rewrite imediato antes de submeter.
- **medium**: 25-50%. Aceita com alerta, monitorar disapproval rate.
- **low**: <25%. OK pra submeter.
```

---

## Exemplos de uso (shapes — não usar copy real de nenhum membro aqui)

### Exemplo 1 — Copy com múltiplos triggers (beauty vertical)

Shape de entrada: copy de ad ou page que contém termos red-flag (palavras
específicas variam por vertical — ver `red_flags.json`).

Shape do output esperado (JSON estruturado):
```json
{
  "risk_score": "<0-100>",
  "severity": "<low|medium|high|critical>",
  "overall_verdict": "<pass|warning|critical>",
  "triggers": [
    {
      "phrase": "<termo detectado na copy>",
      "eixo": "<Meta Policy|FTC|FDA|Credibility|AI Style>",
      "severity": "<low|medium|high|critical>",
      "reason": "<por que é problema, qual política viola>",
      "suggested_replacement": "<substituição compliant>"
    }
  ],
  "rewrite_suggestions": [
    {
      "phrase": "<termo detectado>",
      "severity": "<low|medium|high|critical>",
      "suggested_replacement": "<substituição padrão da rule 8b>",
      "alternatives": ["<outras opções>"],
      "reason": "<por que trocar>"
    }
  ],
  "rewrite_suggestion": "<copy inteira reescrita se severity >= high>",
  "alternative_claims": ["<3 alternativas compliant que preservam intenção persuasiva>"],
  "em_dash_count": "<int>",
  "ai_style_score": "<0-10>",
  "recommendation": "<próxima ação 1-2 frases>"
}
```

O checker deve:
1. Detectar palavras de `red_flags.json` (Botox, filler, injection, cure, etc por vertical) — match por palavra inteira
2. Detectar padrões regex (claim absoluto, income claim, before/after em headline)
3. Contar travessões em headlines (permitir 0) e em copy longa (permitir até 2)
4. Detectar frases genéricas de LLM ("Are you tired of", "Imagine a world")
5. Propor rewrite preservando ângulo persuasivo original

### Exemplo 2 — Copy limpa (zero flags)

Shape esperado quando copy não tem triggers:
```json
{
  "risk_score": 12,
  "severity": "low",
  "overall_verdict": "pass",
  "triggers": [],
  "rewrite_suggestions": [],
  "rewrite_suggestion": null,
  "alternative_claims": [],
  "em_dash_count": 0,
  "ai_style_score": 2,
  "recommendation": "Publicar. Zero flags."
}
```

---

## Integração nas Skills (já aplicada — fonte de verdade é cada skill)

O pseudo-código de integração NÃO vive mais aqui (fonte dupla de verdade drifta).
Onde cada invocação está implementada:

- **Skill 06 (copy-engine)** — sweep 8 da própria skill (checker inline por peça de copy; log consolidado em `workspace/[produto]/06-copy-engine/compliance-log.json`; warnings RESIDUAIS — os que persistiram após rewrite + re-check — vivem em `workspace/[produto]/compliance-warnings.json`, o path canônico que o fluxo de decisão acima usa)
- **Skill 08 (creative-engine)** — ETAPA 7.5 (hooks, voiceovers, primary texts, headlines, overlays; log em `workspace/[produto]/08-creative-engine/compliance-log.json`)
- **Skill 14 (content-recycler)** — ETAPA 4 do `.claude/lib/content-recycler/recycler.md` (por derivada)
- **Skill 07b (page-build)** — GATE 1 via `run.py` CLI canônica com `--stage pre_page`
- **Skill 10 (ad-strategy)** — GATE 1 via `run.py` CLI canônica com `--stage pre_ad`
- **Rule `pre-launch-gates.md`** — contrato transversal dos gates

Qualquer mudança de interface (flags, campos do JSON) atualiza `output-schema.json`
PRIMEIRO e depois os invocadores acima.

---

## Roadmap

- **v1.0 (atual):** Claude classifier, ~80% accuracy, zero training
- **v1.5:** fine-tune Haiku 4.5 em ~5k exemplos rotulados de disapproval Meta (scraping público)
- **v2.0:** multimodal (texto + imagem/vídeo) — validar visual elements também
