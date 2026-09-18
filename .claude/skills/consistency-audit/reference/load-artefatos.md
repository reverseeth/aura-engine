# Consistency Audit · Referência: Load dos artefatos, o que extrair de cada fase (ETAPA 1)

> A lista completa dos artefatos a ler, com os campos extraídos de cada um, os fallbacks legados, o que é lido só se existir e a nota dos dois momentos em que a auditoria roda. Abra na ETAPA 1.

### ETAPA 1 — Load artefatos

Ler todos os artefatos disponíveis (só os que existem):

- `product-research/product-research.md` (+ json se existir)
- `market-research/market-research.md` (se não existir, leia o legado `relatorio.md` — mesmo fallback vale pras outras fases) + `market-research/dados.json` → extract `voc_phrases[]`, `awareness_distribution`, `sophistication_stage`
- `competitor-analysis/competitor-analysis.md` + `competitor-analysis/dados.json` → extract `claims_saturation[]`, `swipe_adapt[]`, `positioning_recommendation`
- `competitor-analysis/creative-patterns.json` (se existir) → extract `hook_archetypes[]`, `recurring_claims[]`
- `offer-builder/offer-builder.md` + `offer-builder/dados.json` → extract `mechanism.name`, `mechanism.ump.name`, `mechanism.ums.name`, `guarantee`, `pricing`, `bonuses[]` (schemas legados podem ter `mechanism.version_short` no lugar de `ump`/`ums` — aceitar ambos)
- `offer-builder/research-foundation.json` (se existir) → extract `proof_items[]`, `best_numbers[]`, `mechanism_name` (top-level) — contexto pro C2 (prova apresentada perto do claim). Ausente → C1b e a parte de números do C2 ficam `skipped`, sem finding.
- `bonus-delivery/bonus-delivery.md` **(if exists)** + assets em `bonus-delivery/bonuses/[bonus-id]/` → extract status da Fase A por bônus (asset gerado? GWP/delivery configurado? "pronto pro launch"?) — alimenta o H5. Se há bônus visível na PDP e a `bonus-delivery` nunca rodou, o próprio H5 flaga (não bloqueia a carga).
- `copy-engine/copy-engine.md` + `copy-engine/dados.json` → extract headlines, hero, mechanism mentions, claims, promises + os campos top-level `lead_type` (enum: `story|big_idea|problem_agitation|mechanism|secret|proclamation|offer|direct` — alimenta o H2) e o flag de pré-flight `voc_forced_continue` (contexto pro H1: se `true`, a copy nasceu com VOC insuficiente — coverage baixo no H1 ganha essa causa provável no finding, com fix "re-rodar skill `market-research` e re-gerar a copy")
- `page/page-plan.json` → extract `strategy.mechanism_name`, `page_type`, `sections_plan[]`, `section_order`, `brand_discovery` (alimenta C1c e M5)
- `page/design-system.md` → extract paleta, tipografia (alimenta M6 — comparação com os tokens)
- `page/design-tokens.json` (gerado por `page-design`, qualquer rota) → tokens extraídos da variação aprovada (alimenta M6)
- `checkout-aov/dados.json` **(if exists)** → extract bump/upsell/free-shipping threshold aplicados (contexto pro C3 e pro H5: a garantia e o bônus que o checkout mostra são os mesmos da oferta e da página)
- `creative-engine/dados.json` → extract hooks, primary_texts, headlines per concept + `hooks_bank[]` top-level
- `retention-engine/[fluxo]/email-N.html` + `flow-metadata.json` **(if exists — a Fase A da `retention-engine` roda pré-launch na ordem canônica: abandoned cart + post-purchase)** → alimenta o M7 (placeholders tipo `{{BONUS_LINK}}` ainda não preenchidos) e dá contexto ao gate (flows de recuperação prontos antes do go-live)
- `ad-strategy/dados.json` **(if exists)** — no modo pré-launch ainda não existe (a `ad-strategy` roda depois da `consistency-audit`); só lê se presente, nunca bloqueia por ausência.
- `ad-analysis/dados.json` **(if exists)** → extract `psm_real`, `winners[]`, `recommended_action` — só existe na re-execução pós-iteração, nunca no pré-launch.
- `manifest.json.agentic` **(if exists)** → `{ready, channel_enabled, score, checked_at}` escrito pela `agentic-readiness` — **contexto INFORMATIVO no gate de launch, NUNCA bloqueante** (agentic readiness é canal incremental, não pré-requisito de ads). Se presente com `ready: false` ou itens `blocked_pending` em `agentic-readiness/dados.json`, mencione no output como nota informativa: esses itens apontam pra dado estruturado (JSON-LD/agent-facts) que diverge da página — se o C3 (garantia) ou o H5 (bônus) acharam drift nessas superfícies, o dado da `agentic-readiness` ajuda a localizar. Ausente → silêncio (a `agentic-readiness` pode não ter rodado; não é finding).

> **A `consistency-audit` roda em dois momentos:** (1) **gate pré-launch** — antes de ads go-live e page em produção, com os artefatos da `product-research` até a `creative-engine`; nesse modo `ad-strategy/dados.json` e `ad-analysis/dados.json` não existem ainda e devem ser lidos só `if exists` (inversão de dependência: a `ad-strategy` e a `ad-analysis` dependem da `consistency-audit` passar, não o contrário). (2) **re-validação pós-iteração** — depois de corrigir issues ou rodar batches, quando `ad-strategy`/`ad-analysis` já existem e entram no cruzamento.
