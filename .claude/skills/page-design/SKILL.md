---
name: page-design
description: Primeira skill da fase STOREFRONT. Planeja a página (page_type por três sinais, sections_plan com o mapa de mídia, hero_type, bloco strategy e commerce no page-plan.json), fecha a marca pelo brand-tokens.json (dembrandt numa URL da própria marca, gerador de 3 paletas com comparadora, ou manual), monta o board de referências premiadas no Awwwards com as 3 que o membro marca, sorteia 3 direções de arte pelo taste-skill e grava a escolhida em direction.md, e constrói a página num de dois modos que o membro escolhe (direção, no canvas do Claude Design; ou referência, seguindo a geometria de uma página que ele admira, seção por seção, com geodiff e checagem legal). QA medido pelo verify_page.py (qa-metrics.json), revisor sem contexto (review.md), preview de layout na Vercel, aprovação do membro e tokens por script (design-tokens.json, drift contra a marca). Grava design/page.html com a copy real da copy-engine, a fonte única que a page-build compila. Use quando o membro disser "page", "página", "design da página", logo depois da copy pronta. Depois rode page-build pra compilar e deployar.
---

# Page Design · Passo 7 · apelido antigo: 07a <!-- gen:title -->

## Quando usar

Primeira das duas skills da fase STOREFRONT (`page-design` → `page-build`), logo depois da copy pronta. Ela decide a estratégia da página, fecha a marca, escolhe referências e direção com o membro e gera o design como HTML aprovado por ele; o Liquid só nasce na `page-build`, por código, a partir desse HTML. Princípio: HTML primeiro, fonte única de verdade visual, aprovação humana antes de qualquer código.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova (escreva sempre na pasta sem número).

1. Idioma (regra 0): `report_language` de `workspace/profile.md` (default `pt-BR`) em todo output interno; a copy inserida no `design/page.html` fica sempre em inglês US.
2. Inputs sob `workspace/[produto]/`: `manifest.json` com `copy-engine` em `skills_completed`; `copy-engine/dados.json` e `copy-engine.md`; `offer-builder/dados.json` e `.md`; `market-research/dados.json` e `.md`; `competitor-analysis/` (opcional); dir `page/` (`mkdir -p`). Relatório `.md` novo ausente: use o legado `relatorio.md`.
3. Input obrigatório faltando (ES1): oferecer (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight` e `risk_acknowledged`. Manifest ou profile ausentes: oferecer o `setup` inline.
4. Ferramentas de terceiros: confira na sessão o MCP `mcp__awwwards__`, o MCP do dembrandt (`mcp__plugin_dembrandt_dembrandt__`), o plugin taste-skill e as skills `awwwards-inspiration`, `awwwards-motion-study` e `deploy-to-vercel`. Para cada ausente, diga em uma linha qual etapa roda na reserva (a reserva de cada uma está no arquivo da etapa). Nada disso bloqueia.
5. Com tools `mcp__higgsfield__` na sessão, a 1.6 gera imagem in-session (`reference/imagens-higgsfield.md`), confirmada com o membro antes de gastar crédito.

## Contexto a carregar

Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar.

1. `copy-engine` (seções canônicas, `lead_type`, `specs[]`), `offer-builder` (preço, stack, garantia, mecanismo nomeado LITERAL), `market-research` (awareness, sophistication, ceticismo, VOC), `competitor-analysis` (gaps, claims saturados, `dominant_landing_format`), `workspace/profile.md`, `workspace/[produto]/brand.md` e `workspace/[produto]/brand/brand-tokens.json`.
2. Base pelo índice (domínio `page-landing-cro`), com a regra de busca em `reference/leitura-e-base.md`.

## Fluxo da skill

### ETAPA 0 · Leitura

`reference/leitura-e-base.md`: os sistemas de fundação de página e de design visual pela `best_query` de cada um; detecte o produto (slug explícito; senão liste `workspace/`: um confirma, vários escolhem, nenhum manda rodar `setup`) e leia os inputs.

### ETAPA 1 · Plano

A `copy-engine` já tomou as decisões de conteúdo e esta etapa as respeita.

- **1.1 `page_type`** (`reference/page-type.md`): pelos três sinais, na ordem de peso do arquivo; divergência de família sempre passa pelo membro. Advertorial e listicle têm o mapa fixo das seções da copy e o botão único `#offer`.
- **1.2 a 1.5** (`reference/sections-e-hero.md`): seções a partir da narrativa do produto, `hero_type` e blocks; eyebrow opcional (`reference/eyebrows.md`). Mostre o plano e só siga com a confirmação.
- **1.6 Assets de imagem** (`reference/assets-de-imagem.md`): mapa de mídia por seção no campo `media`; imagem real no slot ou placeholder EXPLÍCITO com `acquisition_plan`.
- **1.7 Quiz** (`reference/quiz-funnel.md`): só com `page_type: quiz`, no lugar da 1.2.

### ETAPA 2 · Marca

`reference/brand-signals.md`: `brand-tokens.json` do setup quando não está vazio; senão dembrandt numa URL da própria marca, o gerador de 3 paletas com a comparadora na página real, ou o membro informa. Sai a paleta de 8 papéis e as famílias; tipografia e fonte local em `reference/tipografia.md`. A página só escreve na marca quando ela está vazia.

### ETAPA 3 · Referências e direção

`reference/referencias-e-direcao.md`: board no Awwwards (WebSearch de reserva), o membro marca as 3 que mais quer seguir e cada uma ganha imagem para o revisor; o taste-skill sorteia 3 direções, o membro escolhe 1, e ela vira `page/direction.md` no formato fixo. Sem a aprovação da direção, a ETAPA 4 não começa.

### ETAPA 4 · Construção (o membro escolhe o modo)

Pergunte em uma linha; a skill nunca escolhe por ele. `mkdir -p workspace/[produto]/page/design`.

- **Modo direção** (`reference/modo-direcao.md`): a página desenhada a partir do `direction.md` e da marca, no canvas do Claude Design pela tool `Artifact`, com os tokens no `:root`.
- **Modo referência** (`reference/modo-referencia.md`): o membro passa 1 URL (página inteira) ou uma por seção; captura em faixas, construção seção por seção travada pelo `geodiff.py`, unificação e `legal_check.py`. Da referência sai só geometria. Robots ou bloqueio impedindo a captura: ofereça o modo direção.
- Nos dois: movimento só em CSS (`reference/movimento-css.md`); HTML que a skill ingere em vez de escrever passa pela normalização (`reference/normalizacao-html-externo.md`); régua de design em `reference/regua-de-design.md`.

### ETAPA 5 · QA

`reference/qualidade-e-checkpoint.md`: `verify_page.py` grava `page/qa-metrics.json` e as capturas; o revisor sem contexto (`reference/revisor.md`) grava `page/review.md`; rodadas de correção até o teto da régua. Bloqueante que sobrou vai ao membro, que só pode liberar `horizontal_overflow`, `broken_images` e `html_css_kb` (`qa_overrides`). Segunda opinião no Codex opcional (`reference/brief-codex.md`).

### ETAPA 6 · Preview, aprovação, tokens e salvar

Mesmo arquivo: preview de layout na Vercel sem conta (link público, só com o sim do membro), aprovação pelas capturas com as fontes reais e pelo link no celular, `tokens.py` para o `design-tokens.json` e o drift contra a marca. Depois `reference/page-plan-e-salvar.md`: `page-plan.json` com `schema_version: 2`, `strategy` completo (`mechanism_name` LITERAL, `page_type` igual no topo e em `strategy`), `sections_plan[]` com `media`, `section_order`, `commerce`, `reference_board`, `build_mode` e as refs (`direction_ref`, `reference_capture_ref`, `qa_metrics_ref`, `review_ref`, `preview_url`).

## SALVAR

Em `workspace/[produto]/page/`: `page-plan.json`, `direction.md`, `design-tokens.json`, `qa-metrics.json`, `review.md`, `design/page.html` (SVG, sem emoji, sem logo Aura), `design/assets/`, `design-system.md` e o `.html` por `python3 tools/render_report.py workspace/[produto]/page/design-system.md`; no modo referência, `reference-capture/`. `brand/brand-tokens.json` só quando estava vazio. Valide o plano com `python3 tools/schema_validate.py .claude/templates/schemas/page-design.page-plan.schema.json workspace/[produto]/page/page-plan.json`. Depois `python3 tools/manifest.py <slug> complete page-design` (não marque se o `tokens.py` falhou) e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

`reference/mensagem-final-e-self-audit.md`: framing de draft aprovado (modo, `design/page.html` como fonte única, link de preview), o drift da página contra a marca, avisos do QA e do revisor, e o próximo passo: `page-build` ('build page' ou 'deploy'), que compila esse HTML exato em Liquid e faz a aprovação final de tipografia no tema. Antes de declarar concluído, rode a checklist do self-audit do arquivo.
