# Page Design · Referência: O que a skill faz, outputs e pré-flight

> O texto integral da abertura (princípio HTML-first, o menu de rotas como decisão do membro, a consulta à base pelo índice, o que a skill faz passo a passo e os outputs em `page/`) e do pré-flight (idioma, inputs obrigatórios sob `workspace/[produto]/`, escape ES1 e setup inline). Abra antes da ETAPA 0.

Primeira das duas skills da fase **STOREFRONT** (`page-design` → `page-build`). Esta skill decide a estratégia da página, define os signals visuais e gera o design como **HTML navegável aprovado pelo membro**. O Liquid só nasce na `page-build`, deterministicamente, a partir do HTML que você aprovar aqui.

Princípio reitor: **HTML-first → fonte única de verdade visual → aprovação humana ANTES do código.** Nada de "gerar Liquid e torcer pra renderizar igual". O membro vê a página real, navegável, com a copy dele dentro, e só depois ela vira Shopify.

Decisão de design: a `page-design` NÃO escolhe sozinha COMO o design nasce. Ela **apresenta ao membro um menu de rotas** (clone-and-adapt, Claude Design handoff, AIDesigner MCP, frontend-design fallback, AI site-builders externos quando o membro já usa um) e ele escolhe. Causa raiz de página genérica/"horrível" = gerar do zero sem referência concreta. Por isso clone-and-adapt (partir de um layout de concorrente que já converte) é o padrão recomendado, e gerar do zero (frontend-design) é o fallback. Todas as rotas convergem pro MESMO `design/page.html`.

> **Índice completo dos frameworks desta skill (domínio page-landing-cro):** `.claude/lib/kb-index/` (mapa skill→domínio no README). Sempre que esta skill mandar "consulte a base", isso significa: **puxe os SISTEMAS NOMEADOS da base — rode `search_knowledge` com a `best_query` de cada framework relevante PRA AQUELA ETAPA, com `deep=true`.** NUNCA use query genérica.
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill page-design --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 14 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.

**O que esta skill faz:**

1. Pré-flight + PLAN — detecta produto, lê copy/offer/research, escolhe `page_type` pelo awareness, monta o plano de sections, escolhe `hero_type`, persiste o bloco `strategy` completo em `page-plan.json` + eyebrows criativos.
2. ASSETS DE IMAGEM — inventário do que o membro tem (fotos de fornecedor/próprias/UGC), mapa de necessidade de mídia POR SECTION (o `hero_type` amarra o requisito do hero), rota de geração AI pra lifestyle (doutrina foto-real-primeiro da skill `creative-engine` — NUNCA gerar rótulo/embalagem por texto). Tudo registrado em `sections_plan[].media`.
3. BRAND SIGNALS — lê `workspace/[produto]/brand.md` PRIMEIRO (só pergunta o que faltar), depois cascade (Refero MCP → screenshot→visão → design-clone opcional pra hex exato → manual/presets de `.claude/lib/design-presets/presets.json`), tudo convergindo pro mesmo `design-signals.json`.
4. MENU DE ROTAS DE DESIGN — apresenta as rotas viáveis (detectadas em runtime), o membro escolhe; a rota gera a PÁGINA INTEIRA em `design/page.html` com a copy real inserida, os signals aplicados e as imagens reais nos slots. SELF-REVIEW VISUAL obrigatório (Playwright + visão) antes do checkpoint; member aprova. Gera `design-tokens.json`.
5. Dual output dos relatórios (.md + .html gerado pelo `render_report.py`) + framing de draft + atualiza manifest.

**Outputs gravados em `workspace/[produto]/page/`:**
- `page-plan.json` — plano machine-readable + bloco `strategy` completo + mapa de mídia por section (consumido pela `page-build` e pela skill `consistency-audit`)
- `design-system.md` + `design-system.html` — design system humanizado
- `design/page.html` — **a página inteira aprovada (FONTE ÚNICA DE VERDADE visual)**
- `design/assets/` — imagens reais da página (inventário/geração da ETAPA 1.6)
- `design-tokens.json` — tokens consolidados da variação escolhida (consumido pela `page-build`)
- `design-signals.json` — signals de marca (heading_font, body_font, palette role-tagged, radius, shadow, density)

Depois desta skill, rode **page-build** pra compilar o HTML aprovado em Liquid + deployar.

## Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

1. **Idioma (report_language — regra 0 do CLAUDE.md, INVIOLÁVEL):** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno desta skill (`page-plan.json` reasoning, `design-system.md`/`.html`, conversa com o membro) usa esse idioma, com o rigor de linguagem simples da regra 0. **A copy consumidor-final (headlines, eyebrows, hero, bullets, CTAs) inserida no `design/page.html` permanece SEMPRE em inglês US**, independente do `report_language` — copy pública nunca traduz.
2. Valide os inputs (todos sob `workspace/[produto]/`):
   - [ ] `manifest.json` existe e tem `copy-engine` em `skills_completed`
   - [ ] `copy-engine/dados.json` + `copy-engine/copy-engine.md` existem e parseiam (se o `.md` novo não existir, use o legado `relatorio.md` — mesmo fallback vale pras outras fases)
   - [ ] `offer-builder/dados.json` + `offer-builder/offer-builder.md` existem (preço, stack, garantia, mecanismo nomeado)
   - [ ] `market-research/dados.json`/`market-research.md` existe (awareness, sophistication, ceticismo, VOC) — usado pra detectar `page_type`
   - [ ] `competitor-analysis/competitor-analysis.md` existe (opcional, mas alimenta gaps/diferenciação)
   - [ ] Dir de output: `workspace/[produto]/page/` (criar com `mkdir -p` se não existir)

**Se algum input obrigatório faltar** (regra `emergency-escape-paths` ES1) — não aborte seco. Ofereça:
- **(A)** Rodar a skill faltante agora (`copy-engine`/`offer-builder`/`market-research`), OU
- **(B)** Prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` + `risk_acknowledged: true` e avisando no output final que recomenda re-executar com o arquivo real.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes, ofereça rodar o setup (skill `setup`) inline.
