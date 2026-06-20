---
name: consistency-audit
description: Auditoria cross-phase que valida consistência entre os artefatos gerados nas skills 01-08. Detecta drift (mecanismo muda entre offer e copy, VOC phrase não aparece em nenhum hook, claim sem research foundation, promessa sem config de loja, etc). Use quando o membro disser "audit", "consistência", "review", "verificar coerência" ou antes de launch oficial. Roda smoke checks em minutos, retorna report com severity-ranked issues e fix paths.
---

# Cross-Phase Consistency Audit

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (frameworks.json / README.md — mapa skill→domínio no README). Esta skill audita coerência cross-phase; quando precisar JULGAR qualidade de um claim, proof, ou alinhamento (não só comparar strings), puxe os SISTEMAS NOMEADOS da base via `search_knowledge` com a `best_query` de cada framework relevante pra ETAPA. NUNCA use query genérica.

## Quando Usar

Antes de launch oficial (ads go-live + page em produção), rodar esta skill pra pegar incoerências acumuladas ao longo das skills 01-08. Exemplos reais de drift:

- Mecanismo único nomeado "X" na skill 04 virou "X-alt" nas variações de hook da skill 08
- VOC phrase repetida 12x no market research NÃO aparece em nenhum hook do ad batch
- Claim "clinically proven" aparece no hero da página mas `04-research-foundation.json` não tem estudo correspondente
- Guarantee copy diz "90 days" mas `04-offer.json` diz 30 days
- Promo banner promete "free US shipping" mas Shopify shipping zones cobram $X em algumas regiões
- Ad primary text menciona bonus que foi removido na última iteração do offer stack

## Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe com `setup_complete: true`
- [ ] Pelo menos 3 skills completed em `skills_completed[]` (senão não há o que comparar)

**report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

**Input parcial (safeguard):** se `06-copy.{md,json}` E `08-creatives.json` estiverem AMBOS ausentes, não há copy nem ad pra cruzar — force `launch_recommendation: "CAUTION"` (nunca `GO`), registre cada artefato faltante em `artefacts_missing[]`, e marque os checks que dependem deles como `"skipped"` (nunca `"pass"`). Não aborte: rode os checks que forem possíveis com o que existe e avise no output final que recomenda re-executar após gerar copy/criativos.

## Fluxo da Skill

### ETAPA 1 — Load artefatos

Ler todos os artefatos disponíveis (só os que existem):

- `01-product-research.{md,json}`
- `02-market-research.{md,json}` → extract `voc_phrases[]`, `awareness_distribution`, `sophistication_stage`
- `03-competitor-analysis.{md,json}` → extract `claims_saturation[]`, `swipe_adapt[]`, `positioning_recommendation`
- `03-creative-patterns.json` (se existir) → extract `hook_archetypes[]`, `recurring_claims[]`
- `04-offer.{md,json}` → extract `mechanism.name`, `mechanism.version_short`, `guarantee`, `pricing`, `bonuses[]`
- `04-research-foundation.json` → extract `evidence_items[]`, claims supported, `confidence_score`, `mechanism_name` (top-level)
  - **Se AUSENTE:** automaticamente criar CRITICAL finding C2b "Research foundation não rodou — todos os claims de copy/ads saem sem lastro verificável." Oferecer 2 caminhos: **(A)** rodar Skill 04 Etapa 2.5 agora pra gerar o lastro, OU **(B)** prosseguir com o check flagado como critical marcando `manifest.skipped_preflight += ["04-research-foundation.json"]` e avisando no output final que recomenda re-executar. Não pule o check.
- `06-copy.{md,json}` → extract headlines, hero, mechanism mentions, claims, promises
- `07-page/07-plan.json` → extract `sections_plan[]`, `section_order`, `brand_discovery`
- `07-page/07-design-system.md` → extract paleta, tipografia (pra comparar com blueprint/tokens)
- `07-page/design-blueprint/design-tokens.json` (se Claude Design rodou) → tokens extraídos da variação aprovada
- `08-creatives/08-creatives.json` → extract hooks, primary_texts, headlines per concept
- `10-ad-strategy.json` **(if exists)** — no modo pré-launch ainda não existe (a 10 roda depois da 09); só lê se presente, nunca bloqueia por ausência.
- `11-analysis/latest.json` **(if exists)** → extract `psm_real`, `winners[]`, `recommended_action` — só existe na re-execução pós-iteração, nunca no pré-launch.

> **A 09 roda em dois momentos:** (1) **gate pré-launch** — antes de ads go-live e page em produção, com artefatos 01-08; nesse modo `10-ad-strategy.json` e `11-analysis/latest.json` não existem ainda e devem ser lidos só `if exists` (inversão de dependência: a 10 e a 11 dependem da 09 passar, não o contrário). (2) **re-validação pós-iteração** — depois de corrigir issues ou rodar batches, quando 10/11 já existem e entram no cruzamento.

### ETAPA 2 — Check battery (ordenada por severity)

#### CRITICAL (bloqueia launch)

**C1. Mecanismo name consistency**
- `04-offer.json.mechanism.name` deve aparecer LITERALMENTE em:
  - Pelo menos 1 headline de `06-copy.md`
  - Pelo menos 1 hook em `08-creatives.json`
- Se ausente em ambos → `severity: critical`, `fix: inject mechanism name in hero + at least 1 hook`

**C1b. Mechanism name normalizado (04 ↔ research-foundation)**
- `04-offer.json.mechanism.name` DEVE ser idêntico a `04-research-foundation.json.mechanism_name` (campo top-level).
- Divergência → `severity: critical`, `check_id: "mechanism-drift"`, `fix: alinhar o nome do mecanismo entre offer e research-foundation antes de propagar pra copy/ads`. (É a fonte da verdade do mecanismo; se essas duas já divergem, todo C1 abaixo herda o drift.)

**C2. Claim sem research foundation**
- Pra cada claim forte em `06-copy.md` (hero, mechanism section, proof blocks) e `08-creatives.json` (hooks + primary_texts):
  - Cross-check com `04-research-foundation.json.evidence_items[]`
  - Se o claim NÃO tem match → `severity: critical`, `fix: add evidence OR soften claim ("helps with" instead of "proven to")`
- **Não é só "tem match sim/não" — julgue se o PROOF SUSTENTA o CLAIM.** Puxe estes sistemas da base pra calibrar o veredito (rode a `best_query` de cada um):
  - **Bencivenga's 'Yeah, Sure' Principle** (rode `Bencivenga yeah sure principle proof must match claims promise outweighs proof doctors headache`) — proof tem que ser proporcional à ousadia do claim; claim grande com proof fraco dispara o reflexo "yeah, sure". É o gate central deste check.
  - **Hopkins' Specificity Principle (Reason-Why)** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`) — claim vago/genérico (sem número, sem mecanismo, sem reason-why) é fraco mesmo "com evidence". Flag claim que é platitude.
  - **Schwab's Ten Categories of Proof** (rode `Schwab ten categories of proof taxonomy five principles presenting proof testimonials`) — classifica o TIPO de proof disponível em `04-research-foundation`; se o claim exige proof tipo X mas só existe tipo Y, é gap real.
  - **Made to Stick — Audience-Testable Credibility + Sinatra Test** (rode `Made to Stick three wellsprings credibility external internal audience-testable Heath` e `Sinatra Test one example so impressive establishes credibility case study`) — se um único caso/demo carrega o claim sozinho, marca como forte; se nem isso existe, agrava o finding.

**C3. Guarantee copy divergente**
- `04-offer.json.guarantee.duration_days` vs texto em `06-copy.md` guarantee section vs `08-creatives.json` primary_texts
- Divergência (30 vs 60 vs 90 dias) → `severity: critical`

**C4. Promessa sem config**
- Trigger o Promise↔Config gate (`.claude/rules/pre-launch-gates.md`)
- Qualquer `fail` → `severity: critical`

**C5. Ad-flag compliance drift**
- Trigger Compliance Pre-flight em todo output consumidor-final
- `severity: critical` em qualquer peça → reportar

#### HIGH (recomendar fix antes de launch)

**H1. VOC coverage**
- `02-market-research.json.voc_phrases` é o objeto `{problem:[], desire:[], frustration:[]}` — achate os 3 pools numa lista única de frases.
- `coverage = (VOC phrases parafraseadas em hooks/headlines/primary_texts da skill 08) / voc_count`.
- Coverage < 30% → `severity: high` (copy não tá espelhando voz do cliente)
- **Não conte só presença — julgue se a frase exata do cliente foi PRESERVADA ou diluída pra jargão de marketer.** Calibre com:
  - **Collier's Mental Conversation / Enter the Conversation** (rode `Collier six essentials sales letter mental conversation enter conversation in customer's mind word pictures`) — a copy entra na conversa que JÁ acontece na cabeça do cliente? VOC parafraseada pra linguagem corporativa perde isso, mesmo "cobrindo" o tema.
  - **Cashvertising — PVAs + VAKOG Mental Movies** (rode `Cashvertising extreme specificity PVAs powerful visual adjectives VAKOG mental movies five senses`) — VOC forte é palpável/sensorial; se a copy abstraiu a dor concreta do cliente, flag mesmo com coverage alto.

**H2. Awareness alignment**
- Awareness dominante em `02-market-research.json` deve alinhar com tipo de lead escolhido em `06-copy.md`
- Unaware/Problem Aware → deveria ser Story/Secret Lead
- Product/Most Aware → deveria ser Offer/Direct Lead
- Mismatch → `severity: high`
- **Pra julgar SE o lead realmente serve o awareness level (não só "qual tipo é"), puxe:**
  - **Bencivenga's IF...THEN + I=B+C + Shake-Me-Awake Test** (rode `Bencivenga IF THEN construction I equals B plus C interest benefit curiosity shake me awake test`) — lead pra audiência menos aware precisa de mais Curiosity no I=B+C; lead direto pra audiência aware pode liderar com Benefit. Confira o balanço da abertura contra o awareness.
  - **Brunson's Epiphany Bridge + Three False Beliefs** (rode `Brunson big domino three false beliefs vehicle internal external epiphany bridge story expert secrets`) — pra Unaware/Problem Aware, o Story/Secret Lead tem que carregar a epiphany bridge e quebrar as crenças falsas; se a copy pula direto pro produto, o mismatch é mais grave que só "tipo de lead errado".

**H3. Sophistication vs mechanism match**
- Stage 3 → mercado cansou das promessas: exige um **mecanismo novo featured no headline** (o "como funciona" diferente vira o gancho principal).
- Stage 4 → mercado já viu o mecanismo: exige **elaborar o MESMO mecanismo** (mais forte, mais rápido, mais fácil), não trocar de mecanismo nem virar "information-based".
- Stage 5 → mercado cansou de mecanismos: exige **identification** (identidade/pertencimento, não o mecanismo).
- Check contra `04-offer.mechanism`: comparar SE/COMO um mecanismo está featured no headline (Stage 3) ou sendo elaborado (Stage 4), e se Stage 5 puxa identity. Mismatch → `severity: high`.
- **Pra julgar a FORÇA do headline contra o stage (não só "tem mecanismo sim/não"), puxe:**
  - **Schwartz's 38 Verbalization Techniques** (rode `Schwartz 38 verbalization techniques strengthen headline measure compare metaphorize paradox three functions`) — em Stage 3/4 o headline tem que intensificar o mecanismo (measure, compare, metaphorize); headline morno que só NOMEIA o mecanismo é fraco mesmo "alinhado".
  - **Reeves' USP + Vampire Claims** (rode `Reeves USP burning glass vampire claims mosaic structure single proposition unrelated claims`) — em mercado saturado, claims não-relacionados drenam a única proposição; flag headline/hook que dilui o mecanismo único com promessas paralelas.
  - **Caples' Three Classes of Headlines** (rode `Caples three classes headlines self-interest news curiosity six first-paragraph formulas shocker preview`) — Stage 3 (mecanismo novo) pede classe News/Curiosity; Stage 4 (elaborar) pede Self-Interest reforçado. Confira a classe do headline contra o stage.

**H4. Ad angles diversification**
- **Dim 1 — emotion:** `emotion_dominant` vive em `08-creatives.json.concepts[].hooks[].emotion_dominant` e (após o fix da 08) no nível do `concept`. O batch deve cobrir ≥ 2 emotions distintas dos Big 4 (fear, desire, pride/status, curiosity).
- **Dim 2 — angle:** `08-creatives.json.concepts[].angle` deve cobrir ≥ 3 angles distintos dos 8 possíveis (ou ≥ 3 verticais distintas se o schema usar `vertical`).
- Se concentrado em 1 emotion OU < 3 angles/verticais → `severity: high`, `fix: gerar concept complementar com emotion/angle ausente`.

#### MEDIUM (nice to fix)

**M1. Saturated claim usage**
- Claims marcados como `saturation: HIGH` em `03-competitor-analysis.json` aparecendo em hero ou hooks → `severity: medium`
- **Exceção que rebaixa o finding:** um claim saturado pode ser legítimo SE a copy o reapresenta com diferenciação. Puxe pra avaliar:
  - **Hopkins' Preemptive Claim (Schlitz Beer)** (rode `Hopkins preemptive claim Schlitz beer first to make common claims specific Road 3`) — se a copy é a PRIMEIRA a tornar o claim comum específico/concreto, ela "rouba" o claim saturado; nesse caso rebaixe pra pass/note, não medium.
  - **Inoculation Theory (McGuire)** (rode `Inoculation theory McGuire weakened attack vaccination strengthen attitudes competitor argument`) — se a copy antecipa o ceticismo ("você já ouviu isso de todo mundo, mas...") antes de fazer o claim saturado, é uso forte, não fraco.

**M2. Gap não explorado**
- `03-competitor-analysis.json.gaps[]` identifica gap forte, e nenhuma peça de copy/ad explora esse gap → `severity: medium`

**M3. Hook-swap misuse**
- Conceito marcado `hook_swap_viable: false` mas Hooks Bank tá sendo usado como swap source → `severity: medium`

**M4. Duration/word count mismatch**
- Script marcado pra 22s mas word count cabe em 15s (ou vice-versa) → `severity: medium`, `fix: ajustar duration ou cortar script`

### ETAPA 3 — Output (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/` antes de salvar.

Salvar TRÊS artefatos em `workspace/[produto]/`:

1. **`09-consistency-audit.md`** — fonte legível pela AI e pelo membro
2. **`09-consistency-audit.html`** — visualização humana usando `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained). Logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto. Usar componentes:
   - `.danger` pra critical issues
   - `.callout` pra high
   - `.note` pra medium
   - `.pill` pra status tags (BLOCK/CAUTION/GO)
   - `.kpi-grid` pra counters (critical/high/medium)
3. **`09-consistency-audit.json`** — machine-readable schema abaixo

Atualizar `workspace/[produto]/manifest.json` adicionando `"09-consistency-audit"` em `skills_completed`.

Schema do JSON:

```json
{
  "audit_id": "uuid",
  "audited_at": "ISO",
  "artefacts_loaded": ["01-product-research", "..."],
  "artefacts_missing": [],
  "checks_run": 15,
  "issues_critical": 2,
  "issues_high": 3,
  "issues_medium": 4,
  "launch_recommendation": "BLOCK|CAUTION|GO",
  "findings": [
    {
      "check_id": "C2",
      "severity": "critical",
      "status": "fail",
      "artifact": "06-copy.md hero section",
      "issue": "Claim 'visibly firmer skin in 14 days' não tem evidence em 04-research-foundation.json",
      "fix_suggested": "Adicionar study com N=X amostra OR reescrever como 'designed to help with firmness'",
      "auto_fixable": false
    }
  ]
}
```

> O array de problemas chama-se `findings[]` — é o nome que o gate de deploy lê. Cada finding tem `status` ∈ `pass|fail|skipped`; checks não-rodáveis por artefato ausente entram como `"skipped"`, nunca `"pass"`. `artefacts_missing[]` lista os inputs esperados que não existiam.

Markdown com o mesmo conteúdo em formato humano (componentes `.danger` pra critical, `.callout` pra high, `.note` pra medium).

### ETAPA 4 — Decisão

- `issues_critical > 0` → `launch_recommendation: "BLOCK"` → mensagem pro membro: "BLOQUEADO. [N] issues críticas. Fix antes de launch."
- `issues_high > 0 E critical == 0` → `CAUTION` → "CAUTION. Launch possível mas [N] issues high — fix recomendado."
- `artefacts_missing` inclui `06-copy` E `08-creatives` (input parcial) → força no mínimo `CAUTION`, nunca `GO`, mesmo sem critical/high — não dá pra atestar coerência de copy/ad que ainda não existe.
- Tudo limpo E nenhum artefato essencial faltando → "GO. Auditoria passou. Pode lançar."

## Mensagem Final

"Auditoria completa. Launch recommendation: [BLOCK/CAUTION/GO].

- Critical: [N]
- High: [N]
- Medium: [N]

Report salvo em `workspace/[produto]/09-consistency-audit.html`. Abre no browser pra revisar cada issue com fix sugerido.

Depois de corrigir, rode `consistency-audit` de novo pra re-validar."
