---
name: consistency-audit
description: Auditoria cross-phase que valida consistência entre os artefatos gerados nas skills 01-08. Detecta drift (mecanismo muda entre offer e copy, VOC phrase não aparece em nenhum hook, claim sem research foundation, promessa sem config de loja, etc). Use quando o membro disser "audit", "consistência", "review", "verificar coerência" ou antes de launch oficial. Roda smoke checks em minutos, retorna report com severity-ranked issues e fix paths.
---

# Cross-Phase Consistency Audit

## Quando Usar

Antes de launch oficial (ads go-live + page em produção), rodar esta skill pra pegar incoerências acumuladas ao longo das skills 01-08. Exemplos reais de drift:

- Mecanismo único nomeado "X" na skill 04 virou "X-alt" nas variações de hook da skill 07
- VOC phrase repetida 12x no market research NÃO aparece em nenhum hook do ad batch
- Claim "clinically proven" aparece no hero da página mas `04-research-foundation.json` não tem estudo correspondente
- Guarantee copy diz "90 days" mas `04-offer.json` diz 30 days
- Promo banner promete "free US shipping" mas Shopify shipping zones cobram $X em algumas regiões
- Ad primary text menciona bonus que foi removido na última iteração do offer stack

## Pré-flight

- [ ] `/workspace/[produto]/manifest.json` existe com `setup_complete: true`
- [ ] Pelo menos 3 skills completed em `skills_completed[]` (senão não há o que comparar)

## Fluxo da Skill

### ETAPA 1 — Load artefatos

Ler todos os artefatos disponíveis (só os que existem):

- `01-product-research.{md,json}`
- `02-market-research.{md,json}` → extract `voc_phrases[]`, `awareness_distribution`, `sophistication_stage`
- `03-competitor-analysis.{md,json}` → extract `claims_saturation[]`, `swipe_adapt[]`, `positioning_recommendation`
- `03-creative-patterns.json` (se existir) → extract `hook_archetypes[]`, `recurring_claims[]`
- `04-offer.{md,json}` → extract `mechanism.name`, `mechanism.version_short`, `guarantee`, `pricing`
- `04-research-foundation.json` → extract `evidence_items[]`, claims supported
- `05-copy.{md,json}` → extract headlines, hero, mechanism mentions, claims, promises
- `06-plan.json`, `06-brand-snapshot.md`, `06-design-tokens.json` (se existir)
- `07-creatives/07-creatives.json` → extract hooks, primary_texts, headlines per concept
- `08-ad-strategy.json`

### ETAPA 2 — Check battery (ordenada por severity)

#### CRITICAL (bloqueia launch)

**C1. Mecanismo name consistency**
- `04-offer.json.mechanism.name` deve aparecer LITERALMENTE em:
  - Pelo menos 1 headline de `05-copy.md`
  - Pelo menos 1 hook em `07-creatives.json`
- Se ausente em ambos → `severity: critical`, `fix: inject mechanism name in hero + at least 1 hook`

**C2. Claim sem research foundation**
- Pra cada claim forte em `05-copy.md` (hero, mechanism section, proof blocks) e `07-creatives.json` (hooks + primary_texts):
  - Cross-check com `04-research-foundation.json.evidence_items[]`
  - Se o claim NÃO tem match → `severity: critical`, `fix: add evidence OR soften claim ("helps with" instead of "proven to")`

**C3. Guarantee copy divergente**
- `04-offer.json.guarantee.duration_days` vs texto em `05-copy.md` guarantee section vs `07-creatives.json` primary_texts
- Divergência (30 vs 60 vs 90 dias) → `severity: critical`

**C4. Promessa sem config**
- Trigger o Promise↔Config gate (`.claude/rules/pre-launch-gates.md`)
- Qualquer `fail` → `severity: critical`

**C5. Ad-flag compliance drift**
- Trigger Compliance Pre-flight em todo output consumidor-final
- `severity: critical` em qualquer peça → reportar

#### HIGH (recomendar fix antes de launch)

**H1. VOC coverage**
- Top 20 VOC phrases mais repetidas em `02-market-research.json` → quantas aparecem (mesmo paraphrased) em hooks/headlines/primary_texts da skill 07?
- Coverage < 30% → `severity: high` (copy não tá espelhando voz do cliente)

**H2. Awareness alignment**
- Awareness dominante em `02-market-research.json` deve alinhar com tipo de lead escolhido em `05-copy.md`
- Unaware/Problem Aware → deveria ser Story/Secret Lead
- Product/Most Aware → deveria ser Offer/Direct Lead
- Mismatch → `severity: high`

**H3. Sophistication vs mechanism match**
- Stage 3 sophistication exige mechanism ingredient-based
- Stage 4 exige information/data-based
- Stage 5 exige identification-based
- Mismatch com `04-offer.mechanism` → `severity: high`

**H4. Ad angles diversification**
- `07-creatives.json.concepts[]` deve cobrir ≥ 2 emotions diferentes e ≥ 3 archetypes distintos
- Se concentrado em 1 emotion ou 1 archetype → `severity: high`, `fix: gerar concept complementar`

#### MEDIUM (nice to fix)

**M1. Saturated claim usage**
- Claims marcados como `saturation: HIGH` em `03-competitor-analysis.json` aparecendo em hero ou hooks → `severity: medium`

**M2. Gap não explorado**
- `03-competitor-analysis.json.gaps[]` identifica gap forte, e nenhuma peça de copy/ad explora esse gap → `severity: medium`

**M3. Hook-swap misuse**
- Conceito marcado `hook_swap_viable: false` mas Hooks Bank tá sendo usado como swap source → `severity: medium`

**M4. Duration/word count mismatch**
- Script marcado pra 22s mas word count cabe em 15s (ou vice-versa) → `severity: medium`, `fix: ajustar duration ou cortar script`

### ETAPA 3 — Output

Gerar `/workspace/[produto]/11-consistency-audit.{md,html,json}`:

```json
{
  "audit_id": "uuid",
  "audited_at": "ISO",
  "artefacts_loaded": ["01-product-research", "..."],
  "checks_run": 15,
  "issues_critical": 2,
  "issues_high": 3,
  "issues_medium": 4,
  "launch_recommendation": "BLOCK|CAUTION|GO",
  "issues": [
    {
      "check_id": "C2",
      "severity": "critical",
      "artifact": "05-copy.md hero section",
      "issue": "Claim 'visibly firmer skin in 14 days' não tem evidence em 04-research-foundation.json",
      "fix_suggested": "Adicionar study com N=X amostra OR reescrever como 'designed to help with firmness'",
      "auto_fixable": false
    }
  ]
}
```

Markdown com o mesmo conteúdo em formato humano (componentes `.danger` pra critical, `.callout` pra high, `.note` pra medium).

### ETAPA 4 — Decisão

- `issues_critical > 0` → mensagem pro membro: "BLOQUEADO. [N] issues críticas. Fix antes de launch."
- `issues_high > 0 E critical == 0` → "CAUTION. Launch possível mas [N] issues high — fix recomendado."
- Tudo limpo → "GO. Auditoria passou. Pode lançar."

## Mensagem Final

"Auditoria completa. Launch recommendation: [BLOCK/CAUTION/GO].

- Critical: [N]
- High: [N]
- Medium: [N]

Report salvo em `/workspace/[produto]/11-consistency-audit.html`. Abre no browser pra revisar cada issue com fix sugerido.

Depois de corrigir, rode `consistency-audit` de novo pra re-validar."
