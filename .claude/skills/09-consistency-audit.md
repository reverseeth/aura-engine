---
name: consistency-audit
description: Auditoria cross-phase que valida consistência entre os artefatos gerados nas skills 01-08, incluindo a página (07a — page-plan.json/design-tokens), o checkout (07d) e os artefatos pré-launch da 05 (Fase A — assets de bônus) e da 13 (Fase A — flows de recuperação). Detecta drift (mecanismo muda entre offer, copy e página, VOC phrase não aparece em nenhum hook, claim sem research foundation, promessa sem config de loja, bonus removido da oferta mas ainda anunciado, placeholder não-resolvido em copy deployada, etc). Use quando o membro disser "audit", "consistência", "review", "verificar coerência" ou antes de launch oficial. Roda smoke checks em minutos, retorna report com severity-ranked issues e fix paths.
---

# Cross-Phase Consistency Audit

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (frameworks.json / README.md — mapa skill→domínio no README). Esta skill audita coerência cross-phase; quando precisar JULGAR qualidade de um claim, proof, ou alinhamento (não só comparar strings), puxe os SISTEMAS NOMEADOS da base via `search_knowledge` com a `best_query` de cada framework relevante pra ETAPA. NUNCA use query genérica.

## Quando Usar

Antes de launch oficial (ads go-live + page em produção), rodar esta skill pra pegar incoerências acumuladas ao longo das skills 01-08 — incluindo os artefatos pré-launch da 05 (Fase A) e da 13 (Fase A), que na ordem canônica já existem neste ponto. Exemplos reais de drift:

- Mecanismo único nomeado "X" na skill 04 virou "X-alt" nas variações de hook da skill 08
- VOC phrase repetida 12x no market research NÃO aparece em nenhum hook do ad batch
- Claim "clinically proven" aparece no hero da página mas `04-offer-builder/research-foundation.json` não tem estudo correspondente
- Guarantee copy diz "90 days" mas `04-offer-builder/dados.json` diz 30 days
- Promo banner promete "free US shipping" mas Shopify shipping zones cobram $X em algumas regiões
- Ad primary text menciona bonus que foi removido na última iteração do offer stack

## Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe com `setup_complete: true`
- [ ] Pelo menos 3 skills completed em `skills_completed[]` (senão não há o que comparar)

**report_language:** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

**Input parcial (safeguard):** se `06-copy-engine/{copy-engine.md,dados.json}` E `08-creative-engine/dados.json` estiverem AMBOS ausentes, não há copy nem ad pra cruzar — force `launch_recommendation: "CAUTION"` (nunca `GO`), registre cada artefato faltante em `artefacts_missing[]`, e marque os checks que dependem deles como `"skipped"` (nunca `"pass"`). Não aborte: rode os checks que forem possíveis com o que existe e avise no output final que recomenda re-executar após gerar copy/criativos.

## Fluxo da Skill

### ETAPA 1 — Load artefatos

Ler todos os artefatos disponíveis (só os que existem):

- `01-product-research/product-research.md` (+ json se existir)
- `02-market-research/market-research.md` (se não existir, leia o legado `relatorio.md` — mesmo fallback vale pras outras fases) + `02-market-research/dados.json` → extract `voc_phrases[]`, `awareness_distribution`, `sophistication_stage`
- `03-competitor-analysis/competitor-analysis.md` + `03-competitor-analysis/dados.json` → extract `claims_saturation[]`, `swipe_adapt[]`, `positioning_recommendation`
- `03-competitor-analysis/creative-patterns.json` (se existir) → extract `hook_archetypes[]`, `recurring_claims[]`
- `04-offer-builder/offer-builder.md` + `04-offer-builder/dados.json` → extract `mechanism.name`, `mechanism.version_short`, `guarantee`, `pricing`, `bonuses[]`
- `04-offer-builder/research-foundation.json` → extract `evidence_items[]`, claims supported, `confidence_score`, `mechanism_name` (top-level)
  - **Se AUSENTE:** automaticamente criar CRITICAL finding C2b "Research foundation não rodou — todos os claims de copy/ads saem sem lastro verificável." Oferecer 2 caminhos: **(A)** rodar Skill 04 Etapa 2.5 agora pra gerar o lastro, OU **(B)** prosseguir com o check flagado como critical marcando `manifest.skipped_preflight += ["04-offer-builder/research-foundation.json"]` e avisando no output final que recomenda re-executar. Não pule o check.
  - **Sinal explícito adicional:** `06-copy-engine/dados.json.claims_unverified: true` dispara o MESMO finding C2b, mesmo que o `research-foundation.json` exista agora — significa que a copy foi escrita ANTES do lastro existir (membro escolheu prosseguir no pré-flight da 06). Nesse caso o fix é re-validar os claims da copy contra o research-foundation atual (não basta o arquivo existir; a copy nasceu sem ele). Mais robusto que só detectar ausência do arquivo, porque cobre o cenário do membro gerar o research-foundation DEPOIS da copy.
- `05-bonus-delivery/bonus-delivery.md` **(if exists)** + assets em `05-bonus-delivery/bonuses/[bonus-id]/` → extract status da Fase A por bônus (asset gerado? GWP/delivery configurado? "pronto pro launch"?) — alimenta o H5. Se há bônus visível na PDP e a 05 nunca rodou, o próprio H5 flaga (não bloqueia a carga).
- `06-copy-engine/copy-engine.md` + `06-copy-engine/dados.json` → extract headlines, hero, mechanism mentions, claims, promises + os campos top-level `lead_type` (enum: `story|big_idea|problem_agitation|mechanism|secret|proclamation|offer|direct` — alimenta o H2) e os flags de pré-flight `claims_unverified` (alimenta o C2b) e `voc_forced_continue` (contexto pro H1: se `true`, a copy nasceu com VOC insuficiente — coverage baixo no H1 ganha essa causa provável no finding, com fix "re-rodar skill 02 e re-gerar a copy")
- `07-page/page-plan.json` → extract `strategy.mechanism_name`, `page_type`, `sections_plan[]`, `section_order`, `brand_discovery` (alimenta C1c e M5)
- `07-page/design-system.md` → extract paleta, tipografia (alimenta M6 — comparação com os tokens)
- `07-page/design-tokens.json` (gerado por 07a, qualquer rota) → tokens extraídos da variação aprovada (alimenta M6)
- `07d-checkout-aov/dados.json` **(if exists)** → extract config aplicada de bump/upsell/free-shipping threshold (alimenta o C4: promessa de checkout vs config real)
- `08-creative-engine/dados.json` → extract hooks, primary_texts, headlines per concept + `hooks_bank[]` top-level
- `13-retention-engine/[fluxo]/email-N.html` + `flow-metadata.json` **(if exists — a Fase A da 13 roda pré-launch na ordem canônica: abandoned cart + post-purchase)** → alimenta o M7 (placeholders tipo `{{BONUS_LINK}}` ainda não preenchidos) e dá contexto ao gate (flows de recuperação prontos antes do go-live)
- `10-ad-strategy/dados.json` **(if exists)** — no modo pré-launch ainda não existe (a 10 roda depois da 09); só lê se presente, nunca bloqueia por ausência.
- `11-ad-analysis/dados.json` **(if exists)** → extract `psm_real`, `winners[]`, `recommended_action` — só existe na re-execução pós-iteração, nunca no pré-launch.
- `manifest.json.agentic` **(if exists)** → `{ready, channel_enabled, score, checked_at}` escrito pela 07e — **contexto INFORMATIVO no gate de launch, NUNCA bloqueante** (agentic readiness é canal incremental, não pré-requisito de ads). Se presente com `ready: false` ou itens `blocked_pending` em `07e-agentic-readiness/dados.json`, mencione no output como nota informativa: esses itens apontam pras mesmas superfícies que o C4 (promise↔config) já confere (JSON-LD/agent-facts vs config real da loja) — se o C4 achou drift nessas superfícies, o dado da 07e ajuda a localizar. Ausente → silêncio (a 07e pode não ter rodado; não é finding).

> **A 09 roda em dois momentos:** (1) **gate pré-launch** — antes de ads go-live e page em produção, com artefatos 01-08; nesse modo `10-ad-strategy/dados.json` e `11-ad-analysis/dados.json` não existem ainda e devem ser lidos só `if exists` (inversão de dependência: a 10 e a 11 dependem da 09 passar, não o contrário). (2) **re-validação pós-iteração** — depois de corrigir issues ou rodar batches, quando 10/11 já existem e entram no cruzamento.

### ETAPA 2 — Check battery (ordenada por severity)

#### CRITICAL (bloqueia launch)

**C1. Mecanismo name consistency**
- `04-offer-builder/dados.json.mechanism.name` deve aparecer LITERALMENTE em:
  - Pelo menos 1 headline de `06-copy-engine/copy-engine.md`, E
  - Pelo menos 1 conceito de `08-creative-engine/dados.json` — vale no hook, no Bridge/Hold do script ou em primary text. Não exija o nome literal no hook de 3s: a doutrina de hook da 08 é abrir loop (gap theory), não explicar; o mecanismo pode entrar no corpo do ad.
- Ausente em AMBOS os lados (copy E ads) → `severity: critical`, `fix: inject mechanism name in hero + no corpo de pelo menos 1 conceito`
- Presente em só UM dos lados → `severity: high` (drift parcial: o consumidor vê o mecanismo numa fase da jornada e não na outra)

**C1b. Mechanism name normalizado (04 ↔ research-foundation)**
- `04-offer-builder/dados.json.mechanism.name` DEVE ser idêntico a `04-offer-builder/research-foundation.json.mechanism_name` (campo top-level).
- Divergência → `severity: critical`, `check_id: "mechanism-drift"`, `fix: alinhar o nome do mecanismo entre offer e research-foundation antes de propagar pra copy/ads`. (É a fonte da verdade do mecanismo; se essas duas já divergem, todo C1 abaixo herda o drift.)

**C1c. Mechanism name na página (04 ↔ 07-plan)**
- `07-page/page-plan.json.strategy.mechanism_name` DEVE ser idêntico a `04-offer-builder/dados.json.mechanism.name` — a 07a grava esse campo LITERAL exatamente pra este check (ver nota no schema da 07a).
- Divergência → `severity: critical` (a página é o artefato de maior visibilidade pro consumidor; mecanismo com nome diferente na página vs ads quebra o message match do funil inteiro), `fix: corrigir o strategy block do page-plan.json e re-gerar a section afetada`.
- `07-page/page-plan.json` ausente (página ainda não planejada) → check `"skipped"`.

**C2. Claim sem research foundation**
- Pra cada claim forte em `06-copy-engine/copy-engine.md` (hero, mechanism section, proof blocks) e `08-creative-engine/dados.json` (hooks + primary_texts):
  - Cross-check com `04-offer-builder/research-foundation.json.evidence_items[]`
  - Se o claim NÃO tem match → `severity: critical`, `fix: add evidence OR soften claim ("helps with" instead of "proven to")`
- **Não é só "tem match sim/não" — julgue se o PROOF SUSTENTA o CLAIM.** Puxe estes sistemas da base pra calibrar o veredito (rode a `best_query` de cada um):
  - **Bencivenga's 'Yeah, Sure' Principle** (rode `Bencivenga yeah sure principle proof must match claims promise outweighs proof doctors headache`) — proof tem que ser proporcional à ousadia do claim; claim grande com proof fraco dispara o reflexo "yeah, sure". É o gate central deste check.
  - **Hopkins' Specificity Principle (Reason-Why)** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`) — claim vago/genérico (sem número, sem mecanismo, sem reason-why) é fraco mesmo "com evidence". Flag claim que é platitude.
  - **Schwab's Ten Categories of Proof** (rode `Schwab ten categories of proof taxonomy five principles presenting proof testimonials`) — classifica o TIPO de proof disponível em `04-offer-builder/research-foundation.json`; se o claim exige proof tipo X mas só existe tipo Y, é gap real.
  - **Made to Stick — Audience-Testable Credibility + Sinatra Test** (rode `Made to Stick three wellsprings credibility external internal audience-testable Heath` e `Sinatra Test one example so impressive establishes credibility case study`) — se um único caso/demo carrega o claim sozinho, marca como forte; se nem isso existe, agrava o finding.

**C3. Guarantee copy divergente**
- `04-offer-builder/dados.json.guarantee.duration_days` vs texto em `06-copy-engine/copy-engine.md` guarantee section vs `08-creative-engine/dados.json` primary_texts
- Divergência (30 vs 60 vs 90 dias) → `severity: critical`

**C4. Promessa sem config**
- Trigger o Promise↔Config gate (`.claude/rules/pre-launch-gates.md`)
- Inclui o checkout (se `07d-checkout-aov/dados.json` existe): threshold de free-shipping prometido na barra/copy vs threshold configurado; desconto prometido no bump/upsell vs desconto realmente aplicado na config — promessa não-cumprida no checkout é onde nasce chargeback
- Qualquer `fail` → `severity: critical`

**C5. Ad-flag compliance drift**
- Trigger Compliance Pre-flight em todo output consumidor-final
- `severity: critical` em qualquer peça → reportar

#### HIGH (recomendar fix antes de launch)

**H1. VOC coverage**
- `02-market-research/dados.json.voc_phrases` é o objeto `{problem:[], desire:[], frustration:[]}` — achate os 3 pools numa lista única de frases.
- **Denominador = subconjunto prioritário, NUNCA o pool inteiro.** Monte o subconjunto das **20 frases mais repetidas** (é o mesmo `voc_checklist` que a Skill 06 usa — se a 06 já rodou, reuse a lista dela). Dividir pelo `voc_count` total penalizaria matematicamente quem coletou mais VOC: com 80+ frases coletadas e um batch starter de 2-3 conceitos, 30% do pool inteiro é fisicamente impossível de cobrir.
- `coverage = frases do subconjunto prioritário parafraseadas em hooks/headlines/primary_texts da skill 08 (incluindo o hooks_bank[] top-level) / 20`.
- Coverage < 30% → `severity: high` (copy não tá espelhando voz do cliente)
- **Não conte só presença — julgue se a frase exata do cliente foi PRESERVADA ou diluída pra jargão de marketer.** Calibre com:
  - **Collier's Mental Conversation / Enter the Conversation** (rode `Collier six essentials sales letter mental conversation enter conversation in customer's mind word pictures`) — a copy entra na conversa que JÁ acontece na cabeça do cliente? VOC parafraseada pra linguagem corporativa perde isso, mesmo "cobrindo" o tema.
  - **Cashvertising — PVAs + VAKOG Mental Movies** (rode `Cashvertising extreme specificity PVAs powerful visual adjectives VAKOG mental movies five senses`) — VOC forte é palpável/sensorial; se a copy abstraiu a dor concreta do cliente, flag mesmo com coverage alto.

**H2. Awareness alignment**
- Awareness dominante em `02-market-research/dados.json` deve alinhar com o tipo de lead escolhido pela 06 — leia o campo **top-level `lead_type` de `06-copy-engine/dados.json`** (enum: `story|big_idea|problem_agitation|mechanism|secret|proclamation|offer|direct`, gravado na ETAPA 2 da 06). Só caia pra inferir da prosa de `copy-engine.md` se o campo não existir (dados.json legado, gerado antes do contrato).
- Unaware/Problem Aware → deveria ser `story`/`secret`
- Product/Most Aware → deveria ser `offer`/`direct`
- Mismatch → `severity: high`
- **Pra julgar SE o lead realmente serve o awareness level (não só "qual tipo é"), puxe:**
  - **Bencivenga's IF...THEN + I=B+C + Shake-Me-Awake Test** (rode `Bencivenga IF THEN construction I equals B plus C interest benefit curiosity shake me awake test`) — lead pra audiência menos aware precisa de mais Curiosity no I=B+C; lead direto pra audiência aware pode liderar com Benefit. Confira o balanço da abertura contra o awareness.
  - **Brunson's Epiphany Bridge + Three False Beliefs** (rode `Brunson big domino three false beliefs vehicle internal external epiphany bridge story expert secrets`) — pra Unaware/Problem Aware, o Story/Secret Lead tem que carregar a epiphany bridge e quebrar as crenças falsas; se a copy pula direto pro produto, o mismatch é mais grave que só "tipo de lead errado".

**H3. Sophistication vs mechanism match**
- Stage 3 → mercado cansou das promessas: exige um **mecanismo novo featured no headline** (o "como funciona" diferente vira o gancho principal).
- Stage 4 → mercado já viu o mecanismo: exige **elaborar o MESMO mecanismo** (mais forte, mais rápido, mais fácil), não trocar de mecanismo nem virar "information-based".
- Stage 5 → mercado cansou de mecanismos: exige **identification** (identidade/pertencimento, não o mecanismo).
- Check contra `04-offer-builder/dados.json.mechanism`: comparar SE/COMO um mecanismo está featured no headline (Stage 3) ou sendo elaborado (Stage 4), e se Stage 5 puxa identity. Mismatch → `severity: high`.
- **Pra julgar a FORÇA do headline contra o stage (não só "tem mecanismo sim/não"), puxe:**
  - **Schwartz's 38 Verbalization Techniques** (rode `Schwartz 38 verbalization techniques strengthen headline measure compare metaphorize paradox three functions`) — em Stage 3/4 o headline tem que intensificar o mecanismo (measure, compare, metaphorize); headline morno que só NOMEIA o mecanismo é fraco mesmo "alinhado".
  - **Reeves' USP + Vampire Claims** (rode `Reeves USP burning glass vampire claims mosaic structure single proposition unrelated claims`) — em mercado saturado, claims não-relacionados drenam a única proposição; flag headline/hook que dilui o mecanismo único com promessas paralelas.
  - **Caples' Three Classes of Headlines** (rode `Caples three classes headlines self-interest news curiosity six first-paragraph formulas shocker preview`) — Stage 3 (mecanismo novo) pede classe News/Curiosity; Stage 4 (elaborar) pede Self-Interest reforçado. Confira a classe do headline contra o stage.

**H4. Ad angles diversification**
- **Dim 1 — emotion:** `emotion_dominant` vive em `08-creative-engine/dados.json.concepts[].emotion_dominant` (nível do concept; também dentro de `concepts[].hooks[]`). O batch deve cobrir ≥ 2 emotions distintas das 4 Hook Emotions que a 08 grava: **curiosity, urgency, fear, delight** (é o enum literal do campo — não usar nenhuma outra lista).
- **Dim 2 — angle:** `08-creative-engine/dados.json.concepts[].angle` deve cobrir ≥ 3 angles distintos dos 8 possíveis (ou ≥ 3 verticais distintas se o schema usar `vertical`).
- Se concentrado em 1 emotion OU < 3 angles/verticais → `severity: high`, `fix: gerar concept complementar com emotion/angle ausente`.

**H5. Bonus drift (promessa fantasma)**
- Toda menção a bonus em hooks/primary_texts/headlines de `08-creative-engine/dados.json` e no hero/offer stack de `06-copy-engine/copy-engine.md` deve ter entry correspondente em `04-offer-builder/dados.json.bonuses[]` (o campo que a Skill 05 consome).
- Bonus mencionado na copy/ad e AUSENTE do `bonuses[]` atual → `severity: high` (promessa fantasma: bonus removido do stack ainda sendo anunciado — exatamente o drift do exemplo em "Quando Usar"), `fix: remover a menção OU devolver o bonus ao stack (decisão do membro)`.
- Bonus presente em `bonuses[]` e nunca mencionado em copy/ad → não é finding (nem toda oferta anuncia todos os bônus em toda peça).
- **Fase A da Skill 05 completa (gate de launch):** todo bônus visível na PDP (`condition: unconditional` ou `cart_threshold`) precisa ter a Fase A da 05 concluída ANTES do go-live — asset existente em `05-bonus-delivery/bonuses/[bonus-id]/` (PDF/config GWP conforme `type`) E status "pronto pro launch" no `05-bonus-delivery/bonus-delivery.md`. Bônus prometido na página sem asset/config → `severity: high`, `fix: rodar a Fase A da Skill 05 antes do primeiro ad`. Skill 05 nunca rodou e há bônus na PDP → mesmo finding.
- **Condition ↔ copy da página:** a `condition` de cada `bonuses[]` deve bater com a copy — `cart_threshold` exige a condição explícita na página ("FREE over $X", com o X do threshold configurado); `unconditional` exige promessa SEM condição (e auto-add sem threshold na config). Página prometendo incondicionalmente um GWP que na config só destrava acima de threshold (ou vice-versa) → `severity: high`, `fix: alinhar copy OU config (decisão do membro — ver Skill 05 ETAPA 2)`.

#### MEDIUM (nice to fix)

**M1. Saturated claim usage**
- Claims marcados como `saturation: HIGH` em `03-competitor-analysis/dados.json` aparecendo em hero ou hooks → `severity: medium`
- **Exceção que rebaixa o finding:** um claim saturado pode ser legítimo SE a copy o reapresenta com diferenciação. Puxe pra avaliar:
  - **Hopkins' Preemptive Claim (Schlitz Beer)** (rode `Hopkins preemptive claim Schlitz beer first to make common claims specific Road 3`) — se a copy é a PRIMEIRA a tornar o claim comum específico/concreto, ela "rouba" o claim saturado; nesse caso rebaixe pra pass/note, não medium.
  - **Inoculation Theory (McGuire)** (rode `Inoculation theory McGuire weakened attack vaccination strengthen attitudes competitor argument`) — se a copy antecipa o ceticismo ("você já ouviu isso de todo mundo, mas...") antes de fazer o claim saturado, é uso forte, não fraco.

**M2. Gap não explorado**
- `03-competitor-analysis/dados.json.gaps` é o objeto `{audience, messaging, format, offer, mechanism}` — achate as 5 dimensões numa lista única antes de cruzar (mesma situação do `voc_phrases` no H1; iterar como array direto falha).
- Gap forte identificado e nenhuma peça de copy/ad explora → `severity: medium`

**M3. Hook-swap misuse**
- Conceito marcado `hook_swap_viable: false` mas o Hooks Bank (`08-creative-engine/dados.json.hooks_bank[]`) tá sendo usado como swap source nesse conceito → `severity: medium`

**M4. Duration/word count mismatch**
- Script marcado pra 22s mas word count cabe em 15s (ou vice-versa) → `severity: medium`, `fix: ajustar duration ou cortar script`

**M5. Page type vs awareness**
- `07-page/page-plan.json.page_type` deve ser coerente com o awareness dominante de `02-market-research/dados.json` (Unaware/Problem Aware → advertorial; Solution Aware → landing; Product/Most Aware → pdp_robust/pdp_lean — mesma tabela da 07a ETAPA 1.1).
- Mismatch → `severity: medium` (a 07a confirma isso com o membro na criação; aqui é rede de segurança contra drift pós-iteração). `page-plan.json` ausente → `"skipped"`.

**M6. Design tokens vs design system**
- Paleta e tipografia de `07-page/design-tokens.json` (variação aprovada) devem bater com o documentado em `07-page/design-system.md`.
- Divergência (hex do accent diferente, font-family trocada) → `severity: medium`, `fix: regenerar o design system a partir dos tokens da variação aprovada (07a)`. Artefatos ausentes → `"skipped"`.

**M7. Placeholders não-resolvidos em template/copy deployada**
- Varrer os artefatos consumidor-final que já existem — `06-copy-engine/copy-engine.md` (copy final), `07-page/design/page.html` (design aprovado com a copy real inserida), o template JSON/sections populados pela 07b, e os emails da 13 Fase A (`13-retention-engine/[fluxo]/email-N.html`) — procurando tokens de placeholder que deveriam ter sido substituídos por conteúdo real: `{{ALGO_EM_CAPS}}` (ex: `{{BONUS_LINK}}`, `{{MECHANISM_NAME}}`), stand-ins entre colchetes (`[HEADLINE]`, `[PLACEHOLDER]`, `[TBD]`), números de mentira (`XX%`, `$XX`) e "lorem ipsum".
- **Exceções (não são finding):** tags Liquid legítimas de objeto (`{{ product.title }}`, `{{ shop.* }}`, `{% ... %}`) e merge tags de ESP (`{{ first_name }}` do Klaviyo) — o alvo são stand-ins de CONTEÚDO em caixa alta ou colchetes, não a sintaxe do template.
- Placeholder achado → `severity: medium` (caso clássico: `{{BONUS_LINK}}` num email ainda em draft aguardando o asset da 05 — fix: "colar o link do asset da 05 antes de ativar o flow"). **Escalar pra `severity: high` se o placeholder está numa superfície JÁ PUBLICADA** (PDP/landing no ar) — consumidor vendo `{{...}}` na página quebra a confiança na hora.

### ETAPA 3 — Output (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/09-consistency-audit/` antes de salvar.

Salvar TRÊS artefatos em `workspace/[produto]/09-consistency-audit/`:

1. **`09-consistency-audit/consistency-audit.md`** — fonte legível pela AI e pelo membro
2. **`09-consistency-audit/consistency-audit.html`** — visualização humana usando `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained). Logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto. Usar componentes:
   - `.danger` pra critical issues
   - `.callout` pra high
   - `.note` pra medium
   - `.pill` pra status tags (BLOCK/CAUTION/GO)
   - `.kpi-grid` pra counters (critical/high/medium)
3. **`09-consistency-audit/dados.json`** — machine-readable schema abaixo

Atualizar o manifest e regenerar o painel:

- Atualizar `workspace/[produto]/manifest.json` adicionando `"09-consistency-audit"` em `skills_completed`.
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html, onde `<slug>` é o `product_slug`).

Schema do JSON:

```json
{
  "audit_id": "uuid",
  "audited_at": "ISO",
  "artefacts_loaded": ["01-product-research", "..."],
  "artefacts_missing": [],
  "checks_run": 20,
  "issues_critical": 2,
  "issues_high": 3,
  "issues_medium": 4,
  "launch_recommendation": "BLOCK|CAUTION|GO",
  "findings": [
    {
      "check_id": "C2",
      "severity": "critical",
      "status": "fail",
      "artifact": "06-copy-engine/copy-engine.md hero section",
      "issue": "Claim 'visibly firmer skin in 14 days' não tem evidence em 04-offer-builder/research-foundation.json",
      "fix_suggested": "Adicionar study com N=X amostra OR reescrever como 'designed to help with firmness'",
      "auto_fixable": false
    }
  ]
}
```

> O array de problemas chama-se `findings[]` — é o nome que o gate de deploy lê. Cada finding tem `status` ∈ `pass|fail|skipped`; checks não-rodáveis por artefato ausente entram como `"skipped"`, nunca `"pass"`. `artefacts_missing[]` lista os inputs esperados que não existiam.

Markdown com o mesmo conteúdo em formato humano (componentes `.danger` pra critical, `.callout` pra high, `.note` pra medium).

### ETAPA 4 — Decisão

- `issues_critical > 0` → `launch_recommendation: "BLOCK"` (mostrar ao membro como **BLOQUEAR**) → mensagem pro membro: "BLOQUEADO. [N] issues críticas. Corrige antes de lançar."
- `issues_high > 0 E critical == 0` → `CAUTION` (mostrar ao membro como **CUIDADO**) → "CUIDADO. Dá pra lançar, mas [N] issues high — fix recomendado."
- `artefacts_missing` inclui `06-copy-engine` E `08-creative-engine` (input parcial) → força no mínimo `CAUTION`, nunca `GO`, mesmo sem critical/high — não dá pra atestar coerência de copy/ad que ainda não existe.
- Tudo limpo E nenhum artefato essencial faltando → `GO` (mostrar ao membro como **PODE LANÇAR**) → "PODE LANÇAR. Auditoria passou. Próximo passo: diga **'ad strategy'** pra montar a campanha."

## Mensagem Final

"Auditoria completa. Recomendação de lançamento: [BLOQUEAR/CUIDADO/PODE LANÇAR].

- Critical: [N]
- High: [N]
- Medium: [N]

Report salvo em `workspace/[produto]/09-consistency-audit/consistency-audit.html`. Abre no browser pra revisar cada issue com fix sugerido.

[Se BLOQUEAR/CUIDADO:] Depois de corrigir, rode `consistency-audit` de novo pra re-validar.
[Se PODE LANÇAR:] **GO → próximo passo: diga 'ad strategy'** (Skill 10) pra montar a campanha de teste."
