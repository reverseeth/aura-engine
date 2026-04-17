# Compliance Pre-flight Checker

Prompt estruturado que Claude usa pra avaliar copy/ad antes de salvar como final.
Invocado automaticamente pelas Skills 05 e 07, ou manualmente via
`compliance check [arquivo]`.

## Como invocar

### Automático (dentro de Skills 05/07)

Qualquer peça de copy gerada (headline, primary text, script, hook, overlay)
passa por este checker antes de ser salva no arquivo final. Padrão de chamada:

```
Para cada peça de copy gerada:
  1. Ler .claude/lib/compliance-preflight/red_flags.json
  2. Rodar PROMPT abaixo com a copy como input
  3. Parse JSON response
  4. Se risk_score >= 30:
     - Se severity == "critical": PARAR, reportar ao membro, pedir revisão
     - Se severity == "high": aplicar rewrite automático + notificar
     - Se severity == "medium": logar como warning + perguntar membro
  5. Se risk_score < 30: salvar silenciosamente
```

### Manual (sob demanda)

Membro pode rodar: `compliance check /path/to/copy.md`

O Claude lê o arquivo, passa pelo checker, e retorna relatório.

---

## PROMPT (Claude usa este template)

```
Você é o Compliance Pre-flight Checker — analista senior com 10+ anos em
Meta Ads policy, FTC substantiation rules, e FDA cosmetic claim boundaries.

Contexto da base de red flags: {conteúdo de red_flags.json}

Copy a analisar: {input}

Vertical do produto: {skincare | beauty | supplements | financial | other}
Tipo de asset: {headline | primary_text | ad_script | voiceover | landing_page | email}
Plataforma alvo: {meta_ads | tiktok_ads | google_ads | organic}

## Avalie em 5 eixos:

### Eixo 1 — Meta Ad Policy (peso 40%)
Probabilidade de disapproval. Considere:
- Red flag words da base (verificar matches)
- Padrões regex da base
- Claim types que Meta restringe em 2026
- Políticas específicas de beauty/skincare (before/after, anti-aging,
  sensitive personal attributes)
- Landing page coherence (LP que disagree com ad = dispaproval)

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

## Retorne APENAS JSON neste formato:

{
  "risk_score": 0-100,
  "severity": "low|medium|high|critical",
  "overall_verdict": "APPROVE | APPROVE_WITH_EDIT | REVISE | REJECT",

  "triggers": [
    {
      "phrase": "trecho exato",
      "eixo": "Meta Policy | FTC | FDA | Credibility | AI Style",
      "severity": "low|medium|high|critical",
      "reason": "explicação curta",
      "suggested_replacement": "versão compliant"
    }
  ],

  "rewrite_suggestion": "copy inteira reescrita em versão compliant (só se severity >= high)",

  "alternative_claims": [
    "3 alternativas compliant pro mesmo efeito persuasivo"
  ],

  "em_dash_count": N,
  "ai_style_score": 0-10,

  "recommendation": "próxima ação (1-2 frases)"
}

## Calibração de risk_score

- 0-20: LOW — publish as-is, zero triggers críticos
- 21-40: MEDIUM — revisar 1-2 itens específicos, não bloqueador
- 41-70: HIGH — rewrite necessário antes de submeter
- 71-100: CRITICAL — refactor completo, problemas estruturais

## Calibração de severity

- **critical**: 85% probabilidade de disapproval Meta. Cancela ad launch.
- **high**: 50-85%. Sugere rewrite imediato.
- **medium**: 25-50%. Aceita com ressalva, monitor disapproval rate.
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
  "overall_verdict": "<APPROVE|APPROVE_WITH_EDIT|REVISE|REJECT>",
  "triggers": [
    {
      "phrase": "<termo detectado na copy>",
      "eixo": "<Meta Policy|FTC|FDA|Credibility|AI Style>",
      "severity": "<low|medium|high|critical>",
      "reason": "<por que é problema, qual política viola>",
      "suggested_replacement": "<substituição compliant>"
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
1. Detectar palavras de `red_flags.json` (Botox, filler, injection, cure, etc por vertical)
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
  "overall_verdict": "APPROVE",
  "triggers": [],
  "rewrite_suggestion": null,
  "alternative_claims": [],
  "em_dash_count": 0,
  "ai_style_score": 2,
  "recommendation": "Publicar. Zero flags."
}
```

---

## Integração nas Skills

### Skill 05 (copy-engine) — patch a adicionar

Após cada geração de copy (headline, primary text, section, advertorial), antes
de salvar no arquivo final, adicionar step:

```
### Compliance Pre-flight (automático)

Antes de finalizar esta peça de copy:
1. Ler /.claude/lib/compliance-preflight/red_flags.json
2. Rodar checker.md prompt com copy gerada
3. Parse JSON response

Se `overall_verdict` == "REJECT" ou severity == "critical":
  - Parar, mostrar ao membro: "Compliance check detectou issues críticos: [triggers]"
  - Oferecer `rewrite_suggestion` + `alternative_claims`
  - Não salvar até aprovar

Se `overall_verdict` == "REVISE" ou severity == "high":
  - Aplicar `rewrite_suggestion` automaticamente
  - Logar em /workspace/[produto]/05-compliance-log.json

Se `overall_verdict` == "APPROVE_WITH_EDIT" ou severity == "medium":
  - Mostrar alerta: "Compliance check sugere ajustes — ver log"
  - Salvar copy original
  - Logar

Se `overall_verdict` == "APPROVE":
  - Salvar silenciosamente
  - Log mínimo
```

### Skill 07 (creative-engine) — patch a adicionar

Mesma lógica em cada:
- Hook (primeiros 3s do script)
- Voiceover completo
- Primary text do ad
- Headlines
- Text overlays

Logs consolidados em `/workspace/[produto]/07-compliance-log.json`.

---

## Roadmap

- **v1.0 (atual):** Claude classifier, ~80% accuracy, zero training
- **v1.5:** fine-tune Haiku 4.5 em ~5k exemplos rotulados de disapproval Meta (scraping público)
- **v2.0:** multimodal (texto + imagem/vídeo) — validar visual elements também
