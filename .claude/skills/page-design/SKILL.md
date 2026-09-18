---
name: page-design
description: Primeira skill da fase STOREFRONT. Planeja a página (page_type pelo awareness de Schwartz, menu de sections, hero_type, bloco strategy completo no page-plan.json, eyebrows criativos), mapeia os assets de imagem por section (inventário do membro, geração AI foto-real-primeiro só pra lifestyle, placeholder só explícito com plano registrado), extrai os brand signals (brand.md primeiro; cascade Refero → screenshot lido por visão → design-clone opcional → presets) e apresenta ao membro o menu de rotas de design (clone-and-adapt, Claude Design, AIDesigner MCP, frontend-design, AI site-builders), todas convergindo pra design/page.html, a página inteira com a copy real da copy-engine e as imagens nos slots, revisada por screenshot antes do checkpoint e aprovada pelo membro antes de qualquer Liquid existir. Gera design-signals.json e design-tokens.json. Use quando o membro disser "page", "página", "design da página", logo depois da copy pronta. Depois rode page-build pra compilar e deployar.
---

# Page Design · Passo 7 · apelido antigo: 07a <!-- gen:title -->

## Quando usar

Primeira das duas skills da fase STOREFRONT (`page-design` → `page-build`). Ela decide a estratégia da página, define os signals visuais e gera o design como HTML navegável que o membro aprova. O Liquid só nasce na `page-build`, por código, a partir do HTML aprovado aqui. Princípio: HTML primeiro, fonte única de verdade visual, aprovação humana antes de qualquer código. A skill não escolhe sozinha como o design nasce: apresenta o menu de rotas e o membro escolhe. Todas as rotas convergem pro mesmo `design/page.html`.

Material de apoio em `reference/`; abra só o arquivo da etapa atual. Abertura completa em `reference/contexto.md`.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova (só leia da numerada se a migração não puder rodar; escreva sempre na pasta sem número).

1. Idioma (regra 0): `report_language` de `workspace/profile.md` (default `pt-BR`) em todo output interno; a copy inserida no `design/page.html` fica sempre em inglês US.
2. Inputs sob `workspace/[produto]/`: `manifest.json` com `copy-engine` em `skills_completed`; `copy-engine/dados.json` e `copy-engine/copy-engine.md`; `offer-builder/dados.json` e `offer-builder/offer-builder.md`; `market-research/dados.json` e o `.md`; `competitor-analysis/competitor-analysis.md` (opcional); dir `page/` (`mkdir -p`). Relatório `.md` novo ausente: use o legado `relatorio.md`.
3. Input obrigatório faltando (ES1): oferecer (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight` e `risk_acknowledged`. Manifest ou profile totalmente ausentes: oferecer o `setup` inline.

## Contexto a carregar

Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar; sem `resumo`, leia inteiro.

1. `copy-engine/copy-engine.md` e `dados.json` (obrigatório: seções canônicas, `lead_type`, `specs[]`), `offer-builder` (preço, stack, garantia, mecanismo nomeado LITERAL), `market-research` (awareness, sophistication, ceticismo, VOC), `competitor-analysis` (gaps, claims saturados), `workspace/profile.md` (estilo de marca, stage) e `workspace/[produto]/brand.md` (paleta, tipografia e tom já respondidos).
2. Base pelo índice (domínio `page-landing-cro`): `python3 .claude/lib/kb-index/kb_lookup.py --skill page-design --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 14 buscas por etapa; as queries embutidas em `reference/` são o mínimo garantido; nunca query genérica nem busca repetida na sessão.

## Fluxo da skill

### ETAPA 0 · Detecção e leitura

Leia `reference/leitura-e-base.md`. 0.1: puxe os nove sistemas de fundação de página pela `best_query` de cada um até dominar conversão e estrutura. 0.2: detecte o produto (slug explícito; senão liste `workspace/`: um produto confirma, vários escolhem, nenhum manda rodar `setup` ou `product research`) e grave o slug em `PRODUTO`. 0.3: leia os inputs obrigatórios listados acima.

### ETAPA 1 · PLAN (estratégia e plano de sections)

A página não tem estrutura fixa; a `copy-engine` já tomou as decisões e esta etapa as respeita.

- **1.1 `page_type`** (`reference/page-type.md`): decidido pelo `dominant_awareness` da `market-research` e confirmado pelo `lead_type` top-level da `copy-engine` (story, big_idea e problem_agitation → `advertorial`; mechanism, secret e proclamation → `landing`; offer e direct → `pdp_robust` ou `pdp_lean`); heurística sintática só como desempate; `dominant_awareness_secondary` presente vira `hybrid: true` (na dúvida, o page_type do nível menos consciente). Advertorial exige dois passos obrigatórios: definir o `destination_ref` do soft CTA (segunda passada da cadeia gerando uma `pdp_lean`, PDP existente já trabalhada ou checkout direto) e montar o `sections_plan` pelo mapa canônico 1:1 das 7 seções da copy (hero, lead, background-story, root-cause, mechanism-reveal, product-buildup, reveal-close); seção canônica ausente no `copy-engine.md` = parar e mandar rodar a `copy-engine` de novo. Puxe os frameworks da decisão listados no arquivo. Confirme o `page_type` com o membro em uma frase.
- **1.2 a 1.5** (`reference/sections-e-hero.md`): escolha as sections pelo menu (core `hero`, `offer`, `faq`, `cta-final`; `mechanism` só com mecanismo único real; `specs` recomendado em toda pdp, com a copy de `dados.json.specs[]`), o `hero_type` entre os 5 canônicos (value-prop, dreamstate, problem, segment, campaign) validado por StoryBrand e Grunt Test, os block types por section, e mostre o plano ao membro (o que entra, o que fica de fora e por quê); só siga com a confirmação.
- **Eyebrows** (`reference/eyebrows.md`): nunca rótulo de framework na página; tag criativa de 2 a 5 palavras, em inglês, específica do produto, sem travessão; gravada em `sections_plan[].eyebrow`.
- **1.6 Assets de imagem** (`reference/assets-de-imagem.md`): inventário do que o membro tem (fornecedor, próprias, UGC, selos) salvo em `page/design/assets/`; mapa de mídia por section no campo `media` (o `hero_type` amarra o requisito do hero); geração AI só pra lifestyle, sempre ancorada na foto real do produto, nunca rótulo ou embalagem por prompt de texto; sem nenhuma foto real do produto é bloqueio de inventário. Gate: o HTML só é aprovado com imagem real no slot ou placeholder EXPLÍCITO com `acquisition_plan` registrado.

### ETAPA 2 · Brand signals (cascade unificada → `design-signals.json`)

Leia `reference/brand-signals.md`. Aqui sai só direção de cor, tipografia e densidade, nunca o layout. Leia `brand.md` primeiro e pergunte em uma mensagem só o que faltar. Cascade: Caminho 1, Refero MCP (`mcp__refero__`, 2 a 3 candidatos, o membro escolhe); Caminho 2, screenshot full-page lido por visão (fallback primário); Caminho 3, `tools/design-clone/aura_clone.py` só pra hex exato (ignore `defaults_fallback`); Caminho 4, descrição livre ou um dos 8 presets com tokens LITERAIS de `.claude/lib/design-presets/presets.json` (nunca ajustados em runtime). Com 2 a 4 paletas vivas, gere a página comparadora com tokens em trio R,G,B; dois temas pedem um snippet de paleta por tema, com a disciplina de push da rule `shopify-theme-safety.md`. Salve `design-signals.json` e mostre o resumo ao membro.

### ETAPA 3 · Escolha da fonte de design (o membro escolhe a rota)

- **3.1 e 3.2** (`reference/menu-de-rotas.md`): detecte em runtime as rotas viáveis (1 clone-and-adapt, sempre; 2 Claude Design, sempre; 3 AIDesigner só com `mcp__aidesigner__`; 4 frontend-design, fallback; 5 AI site-builders só se o membro usa um) e apresente a tabela no `report_language`, sugerindo a rota 1 como default sem impor. `mkdir -p workspace/[produto]/page/design`.
- **3.3 Rota 1** (`reference/rota-clone-and-adapt.md`): `aura_clone.py clone-and-adapt` na URL com a cascade de captura (downloader, single-file automático, screenshot por visão exceto com `challenge_detected`, extensão SingleFile manual com `--from-file`); reconcilie o esqueleto com o `sections_plan`; gere o `page.html` com a copy real, a oferta, os signals e as imagens da 1.6. Regra legal inegociável: só estrutura e layout; copy, imagens, logos, marca e claims do concorrente nunca. A variante de clone fiel seção a seção (4 passos, padrões em `.claude/lib/shopify-section-patterns/`) está no mesmo arquivo.
- **3.4 a 3.6c** (`reference/rotas-externas-e-normalizacao.md`): rota 2 (canvas do Claude Design, export HTML; DesignSync não serve pra página), rota 3 (AIDesigner alimentado com plano e copy; falha cai pra rota 1 ou 4), rota 4 (`frontend-design` uma vez, com signals, referência concreta e direção explícita; 2 a 3 variações da página inteira com abas), rota 5 (site-builder externo, `design_route: "site-builder"`). Rotas 2 e 5 passam pela normalização 3.6c: Tailwind vira CSS plano por estilos computados, JS de runtime removido, assets locais, validação self-contained com zero `<script>`.
- **3.7, self-review e checkpoint** (`reference/qualidade-e-checkpoint.md`): regras comuns a toda rota (markers `data-aura-section` por section, SVG inline sem emoji, travessão mínimo, WCAG AA, performance budget com hero sem lazy e HTML+CSS até cerca de 150 KB, imagens do mapa de mídia, CTAs como call-to-value, as 4 modalities servidas, receita por sessão como régua, congruência ad→page, tratamento editorial no advertorial); corrija inline o que a rota violou. Self-review visual obrigatório: screenshots 1440 e 390 lidos por visão, defeitos corrigidos antes de o membro ver; parede de texto aciona a dieta de copy da `copy-engine`. Checkpoint como draft navegável com pergunta granular; versões `page-v2.html`, log em `page/iterations-log.json`, 3 iterações sem progresso escalam; a aprovação consolida `design/page.html`.
- **Tokens** (`reference/design-tokens.md`): consolide `design-tokens.json` por código a partir do HTML aprovado (`variant_chosen`, cores, tipografia, spacing base 4 ou 8, radii, shadow, `components_by_section` cruzado com o `sections_plan`).

### ETAPA 4 · Persistir `page-plan.json`, relatórios e manifest

Leia `reference/page-plan-e-salvar.md`. `page-plan.json` com o bloco `strategy` completo (`mechanism_name` LITERAL da `offer-builder`, `hero_type`, `page_type` igual no topo e dentro de `strategy`, `hybrid`), `sections_plan[]` com `eyebrow`, `blocks` e o campo `media` obrigatório, `section_order`, `brand_discovery`, `design_route`, `design_route_ref`, `destination_ref` e as refs dos arquivos de design.

## SALVAR

Em `workspace/[produto]/page/`: `page-plan.json`, `design-signals.json`, `design-tokens.json`, `design/page.html` (página do consumidor: SVG, sem emoji, sem logo Aura), `design/assets/` e `design-system.md`, cujo `.html` sai de `python3 tools/render_report.py workspace/[produto]/page/design-system.md` (convenções em `.claude/templates/aura-html-components.md`). Depois `python3 tools/manifest.py <slug> complete page-design` (`page_type` e `signals_source` ficam só no `page-plan.json`) e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Texto integral, self-audit silencioso e referências cruzadas em `reference/mensagem-final-e-self-audit.md`. Framing de draft: design aprovado (rota escolhida, `design/page.html` como fonte única), plano em `page-plan.json`, tokens em `design-tokens.json`; próximo passo é a `page-build` ('build page' ou 'deploy'), que compila esse HTML exato em Liquid. Antes de declarar concluído, rode os 5 gates do self-audit com a checklist do arquivo (mecanismo literal, `page_type` coerente, `destination_ref` e mapa canônico no advertorial, `media` completo, self-review rodado, tokens de preset literais, markers em toda section, zero copy ou imagem do concorrente na rota 1).
