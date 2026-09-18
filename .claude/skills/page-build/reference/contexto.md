# Page Build · Referência: O que a skill faz, pré-flight e paths normalizados

> O texto integral da abertura (princípio da conversão determinística, o que a skill faz passo a passo, os outputs em `page/`), do pré-flight (idioma, gate da `consistency-audit`, inputs exigidos, dirs de staging) e das variáveis de path usadas em todos os comandos. Abra antes da ETAPA 1.

Segunda e última skill da fase **STOREFRONT** (`page-design` → `page-build`). A `page-design` produziu o `design/page.html` aprovado — a FONTE ÚNICA DE VERDADE visual. Esta skill **compila esse HTML em Liquid por CÓDIGO, não por reasoning**, popula o template com a copy real, passa os gates de launch e deploya no Shopify.

Princípio: **conversão determinística mata as traduções lossy e o drift.** O Liquid é gerado mecanicamente do HTML aprovado via `tools/design-clone/liquid-converter.py` (Modo C por section, ou `--batch` pra página inteira). O Claude entra só pra (a) splitar o HTML por section, (b) renomear blocks semanticamente DEPOIS do compile, (c) reimplementar interações que o conversor removeu (`<script>` sai com warning — usar `<details>` nativo etc.), (d) validar. O que o conversor aplica por código e o que ele NÃO faz está na seção **Padrões aplicados pelo conversor** — não afirme capacidade que não existe.

> **Consulta à base pelo índice:** toda decisão de CONTEÚDO/design nasce na `page-design` — esta skill não re-decide página. Nos pontos de implementação MANUAL onde ela decide sozinha (selling plan/Subscribe & Save, buy box/pricing table, desconto Shopify, countdown — a lista "O que o conversor NÃO faz"), rode `python3 .claude/lib/kb-index/kb_lookup.py --skill page-build --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão. NUNCA query genérica.

**O que esta skill faz:**

1. Pré-flight — exige `design/page.html` aprovado + `design-tokens.json` + `page-plan.json`.
2. SPLIT — separa o HTML aprovado em fragmentos por section (via marcadores `data-aura-section`) + o CSS.
3. COMPILE+POPULATE — roda `liquid-converter.py` numa invocação só (preferir `--batch`; ou Modo C por section com `--emit-template-json`). O template `page.[produto].json` sai populado com blocks/block_order/settings e a copy real.
4. RENAME semântico — o Claude renomeia os block types genéricos pros type-specific (editando `.liquid` E template JSON juntos), SÓ DEPOIS do compile (nunca re-rode o conversor por cima de renames) — mais a RESTAURAÇÃO dos SVGs grandes que o conversor substituiu por placeholder (inventário + reinjeção do original).
5. VALIDATE — cada `.liquid` passa por `shopify-plugin:shopify-liquid` (3 retries) + snippet de validação cruzada do template JSON + **check bloqueante de imagens/placeholders** (nenhuma section com imagem vazia/placeholder do mapa de mídia da `page-design`; zero `{{PLACEHOLDER}}` residual).
6. GEO / Schema (ETAPA 4.5, agent-readability) — gera o JSON-LD Schema.org (Product + Offer + AggregateRating + BreadcrumbList + FAQPage das perguntas reais da section faq) de `offer-builder/dados.json` + `copy-engine/dados.json` + reviews, valida, e injeta no template como bloco `custom_liquid` + um bloco "agent-readable facts" (specs, envio/retorno, disponibilidade, garantia) em texto limpo separado da copy persuasiva.
7. GATE (ETAPA 5, blocking) — GATE 1 performance budget, ANTES do deploy (a página aprovada tem que ser rápida no 4G).
8. DEPLOY — shopify-theme-safety integral (duplicate → pull --nodelete → **provisionamento de web fonts** → push --nodelete + marker `data-aura-build` + criação da página + smoke test).
9. PUBLISH — com aprovação explícita do membro: backup do live → `shopify theme publish` → grava `manifest.storefront` (theme_id, page_url, published_at) que a `checkout-aov` e a `ad-strategy` leem → **fidelity check por visão** (screenshot da página no ar vs `design/page.html` aprovado; divergiu = corrige antes de encerrar).
9. Dual output (.md + .html gerado pelo `render_report.py`) + iteration loop.

**Outputs em `workspace/[produto]/page/`:** `staging/html/*.html` + `staging/html/page.css` (fragmentos do SPLIT), `staging/sections/page-[produto]-*.liquid`, `staging/templates/page.[produto].json`, `staging/geo/product-schema.json` (JSON-LD), `staging/geo/agent-facts.html`, `page-report.md` + `page-report.html`, `deploy-report.json`. (O conversor NÃO gera `blocks/*.liquid` — blocks são inline no schema da section.)

## Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

1. **Idioma (report_language — regra 0 do CLAUDE.md, INVIOLÁVEL):** leia `report_language` de `workspace/profile.md` (default `pt-BR`; também em `manifest.report_language`). Relatórios internos (`page-report.md`/`.html`) e conversa nesse idioma, com o rigor de linguagem simples da regra 0. Copy consumidor-final permanece SEMPRE em inglês US.
2. **Gate de consistência (skill `consistency-audit`)** — leia `workspace/[produto]/consistency-audit/dados.json` se existir:
   - `launch_recommendation == "BLOCK"` → o deploy da página NÃO está bloqueado por si só (a página existir não gasta dinheiro), mas avise o membro dos items críticos e recomende rodar `consistency audit` de novo. O gate 09 é pré-requisito do **LAUNCH** (gateia a skill `ad-strategy`), não do deploy da página.
   - `"CAUTION"` → mostre warnings, peça confirmação.
   - `"GO"` ou ausente → siga (recomende rodar a `consistency-audit` antes do launch).
3. Valide os inputs (sob `workspace/[produto]/page/`):
   - [ ] `design/page.html` existe (HTML aprovado da `page-design` — **sem ele, PARE e direcione pra `page-design`**; não existe modo "gera Liquid direto")
   - [ ] `design-tokens.json` existe e parseia
   - [ ] `page-plan.json` existe com bloco `strategy` + `sections_plan` + `section_order` (plans novos trazem `sections_plan[].media` — o mapa de mídia que o check bloqueante da ETAPA 4 usa; plan legado sem `media` é tolerado, o check degrada pro mínimo)
   - [ ] `manifest.json` tem `page-design` em `skills_completed`
   - [ ] Plugin `shopify-plugin:shopify-liquid` disponível (se falhar, instrua `/plugin install shopify-plugin@shopify-plugin`)
4. Dirs de staging: `workspace/[produto]/page/staging/{html,sections,templates,geo}/` (criar com `mkdir -p`).

Se `design/page.html` faltar → "Não achei o design aprovado. Rode `page-design` primeiro — preciso do `design/page.html` que você aprova antes de gerar Liquid."

## Paths normalizados (defina no topo)

```bash
PRODUTO="[slug]"
PAGE_DIR="workspace/${PRODUTO}/page"
DESIGN_HTML="${PAGE_DIR}/design/page.html"
STAGING_DIR="${PAGE_DIR}/staging"
THEME_DIR="${PAGE_DIR}/theme-clone"
TOOLS_DIR="tools/design-clone"
STORE=""  # preenchido na detecção da loja (ETAPA 6.1)
```
