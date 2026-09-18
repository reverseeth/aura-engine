---
name: page-design
description: Primeira skill da fase STOREFRONT. Planeja a página (page_type por três sinais, menu de sections, hero_type, bloco strategy no page-plan.json, eyebrows criativos), mapeia os assets de imagem por section (inventário do membro, geração AI só pra lifestyle, placeholder explícito com plano registrado), extrai os brand signals (brand.md primeiro; cascade Refero → screenshot lido por visão → design-clone opcional → gerador de 3 paletas) e apresenta ao membro o menu de três rotas de design (do zero com o Claude Design, clone de uma página inteira com o SingleFile, quebra-cabeça de seções), todas convergindo pra design/page.html, com a copy real da copy-engine e as imagens nos slots, aprovada pelo membro antes de qualquer Liquid existir. Gera design-signals.json e design-tokens.json. Use quando o membro disser "page", "página", "design da página", logo depois da copy pronta. Depois rode page-build pra compilar e deployar.
---

# Page Design · Passo 7 · apelido antigo: 07a <!-- gen:title -->

## Quando usar

Primeira das duas skills da fase STOREFRONT (`page-design` → `page-build`). Ela decide a estratégia da página, define os signals visuais e gera o design como HTML que o membro aprova; o Liquid só nasce na `page-build`, por código, a partir desse HTML. Princípio: HTML primeiro, fonte única de verdade visual, aprovação humana antes de qualquer código. A skill não escolhe sozinha como o design nasce: apresenta as três rotas e o membro escolhe, e todas convergem pro mesmo `design/page.html`.

Material de apoio em `reference/`; abra só o arquivo da etapa atual. Abertura completa em `reference/contexto.md`.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova (só leia da numerada se a migração não puder rodar; escreva sempre na pasta sem número).

1. Idioma (regra 0): `report_language` de `workspace/profile.md` (default `pt-BR`) em todo output interno; a copy inserida no `design/page.html` fica sempre em inglês US.
2. Inputs sob `workspace/[produto]/`: `manifest.json` com `copy-engine` em `skills_completed`; `copy-engine/dados.json` e `copy-engine/copy-engine.md`; `offer-builder/dados.json` e `offer-builder/offer-builder.md`; `market-research/dados.json` e o `.md`; `competitor-analysis/competitor-analysis.md` (opcional); dir `page/` (`mkdir -p`). Relatório `.md` novo ausente: use o legado `relatorio.md`.
3. Rota 2 do menu de design (clone com o SingleFile) exige a loja Shopify conectada (`shopify theme list` responde); sem isso o membro loga a CLI, como na `page-build`, ou escolhe outra rota.
4. Input obrigatório faltando (ES1): oferecer (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight` e `risk_acknowledged`. Manifest ou profile totalmente ausentes: oferecer o `setup` inline.

## Contexto a carregar

Em todo `dados.json` de fase anterior, leia primeiro o objeto `resumo` e abra o arquivo inteiro só na etapa que precisar; sem `resumo`, leia inteiro.

1. `copy-engine/copy-engine.md` e `dados.json` (obrigatório: seções canônicas, `lead_type`, `specs[]`), `offer-builder` (preço, stack, garantia, mecanismo nomeado LITERAL), `market-research` (awareness, sophistication, ceticismo, VOC), `competitor-analysis` (gaps, claims saturados, `dominant_landing_format`), `workspace/profile.md` (estilo de marca, stage) e `workspace/[produto]/brand.md` (paleta, tipografia e tom já respondidos).
2. Base pelo índice (domínio `page-landing-cro`): `python3 .claude/lib/kb-index/kb_lookup.py --skill page-design --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 14 buscas adicionais por etapa; as queries embutidas em `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida na sessão.

## Fluxo da skill

### ETAPA 0 · Detecção e leitura

Leia `reference/leitura-e-base.md`. 0.1: puxe os nove sistemas de fundação de página pela `best_query` de cada um até dominar conversão e estrutura. 0.2: detecte o produto (slug explícito; senão liste `workspace/`: um produto confirma, vários escolhem, nenhum manda rodar `setup` ou `product research`) e grave o slug em `PRODUTO`. 0.3: leia os inputs obrigatórios listados acima.

### ETAPA 1 · PLAN (estratégia e plano de sections)

A página não tem estrutura fixa; a `copy-engine` já tomou as decisões e esta etapa as respeita.

- **1.1 `page_type`** (`reference/page-type.md`): três sinais, em ordem de peso: `dominant_awareness` da `market-research`, `lead_type` top-level da `copy-engine` (o mapa de lead pra formato está no arquivo) e `dominant_landing_format` da `competitor-analysis`. Três na mesma família, decida e siga; variante diferente dentro dela, adote a do concorrente e informe em uma linha; famílias diferentes, mostre a divergência com o número de ads e o membro decide (nunca troque o `page_type` só pelo sinal do concorrente sem mostrar); sem o sinal, decida pelos dois primeiros. `dominant_awareness_secondary` presente vira `hybrid: true` (na dúvida, o page_type do nível menos consciente). Advertorial e listicle exigem dois passos obrigatórios: o `destination_ref` do soft CTA (as três opções de destino estão no arquivo) e o `sections_plan` pelo mapa canônico 1:1 das 7 seções da copy; seção canônica ausente no `copy-engine.md` = parar e mandar rodar a `copy-engine` de novo. Puxe os frameworks da decisão listados no arquivo. Confirme o `page_type` com o membro em uma frase e grave `strategy.page_type_signals`.
- **1.2 a 1.5** (`reference/sections-e-hero.md`): escolha as sections pelo menu (core `hero`, `offer`, `faq`, `cta-final`; `mechanism` só com mecanismo único real; `specs` recomendado em toda pdp, com a copy de `dados.json.specs[]`), o `hero_type` entre os 5 canônicos (value-prop, dreamstate, problem, segment, campaign) validado por StoryBrand e Grunt Test, os block types por section, e mostre o plano ao membro (o que entra, o que fica de fora e por quê); só siga com a confirmação.
- **Eyebrows** (`reference/eyebrows.md`): nunca rótulo de framework na página; tag criativa de 2 a 5 palavras, em inglês, específica do produto, sem travessão; gravada em `sections_plan[].eyebrow`.
- **1.6 Assets de imagem** (`reference/assets-de-imagem.md`): inventário do que o membro tem (fornecedor, próprias, UGC, selos) salvo em `page/design/assets/`; mapa de mídia por section no campo `media` (o `hero_type` amarra o requisito do hero); geração AI só pra lifestyle, sempre ancorada na foto real do produto, nunca rótulo ou embalagem por prompt de texto; sem nenhuma foto real do produto é bloqueio de inventário. Gate: o HTML só é aprovado com imagem real no slot ou placeholder EXPLÍCITO com `acquisition_plan` registrado.

### ETAPA 2 · Brand signals (cascade unificada → `design-signals.json`)

Leia `reference/brand-signals.md`. Aqui sai só direção de cor, tipografia e densidade, nunca o layout. Leia `brand.md` primeiro e pergunte em uma mensagem só o que faltar. Cascade: Caminho 1, Refero MCP (`mcp__refero__`, 2 a 3 candidatos, o membro escolhe); Caminho 2, screenshot full-page lido por visão (fallback primário); Caminho 3, `tools/design-clone/aura_clone.py` só pra hex exato (ignore `defaults_fallback`); Caminho 4, o gerador `.claude/lib/design-presets/palette_engine.py` (3 candidatas com motivo, harmonia declarada e AA garantido; os 8 presets são a base dele, nunca um menu). Comparadora obrigatória com as 3, nos trios R,G,B do `--format css`; dois temas pedem um snippet de paleta por tema, com a disciplina de push da rule `shopify-theme-safety.md`. Salve `design-signals.json` e mostre o resumo ao membro.

### ETAPA 3 · Escolha da fonte de design (o membro escolhe a rota)

- **3.1 e 3.2** (`reference/menu-de-rotas.md`): detecte as três rotas viáveis (1 Claude Design, com a tool `Artifact` na sessão; 2 clone com o SingleFile, com página de referência e loja conectada; 3 quebra-cabeça, com duas ou mais referências) e apresente a tabela no `report_language`, com a rota 1 como default. `mkdir -p workspace/[produto]/page/design`.
- **3.3 Rota 1, do zero com o Claude Design** (`reference/rota-claude-design.md`): nunca de tela em branco (signals da ETAPA 2, plano de sections, copy real, imagens da 1.6, referência visual e direção escrita). O canvas abre pela tool `Artifact`: quickstart com `intent: "design"`, create com o `type_url` que voltou e atualização no mesmo `url`. Entregável e fonte é o `design/page.html` local; canvas que não abre não aborta.
- **3.4 Rota 2, clone com o SingleFile** (`reference/rota-singlefile-clone.md`): o membro salva a página de referência com a extensão e diz o caminho; ingestão por `aura_clone.py clone-and-adapt --from-file`; reconcilie o esqueleto com o `sections_plan`; gere o `page.html` com a copy, a oferta, os signals e as imagens; prepare as sections editáveis no editor da Shopify. Regra legal inegociável, aqui e na 3.5: só estrutura e layout, nunca copy, imagem, logo, marca ou claim da referência.
- **3.5 Rota 3, quebra-cabeça de seções** (`reference/rota-section-puzzle.md`): mapa fonte→section; estrutura extraída de cada fonte (arquivo por estilos computados, print por visão), nunca o texto; conferência contra o `sections_plan`; unificação por token único e teste de vizinhança anti-colagem.
- **3.6 Normalização** (`reference/normalizacao-html-externo.md`): todo HTML ingerido vira CSS plano por estilos computados, sem JS de runtime, assets locais, self-contained com zero `<script>` e markers injetados.
- **3.7, self-review e checkpoint** (`reference/qualidade-e-checkpoint.md`): a régua comum às três rotas (markers, SVG sem emoji, travessão mínimo, WCAG AA, performance budget, mapa de mídia, call-to-value, 4 modalities, congruência ad→page, tratamento por page_type) é bloqueante; corrija inline o que a rota violou. Self-review visual obrigatório: screenshots 1440 e 390 lidos por visão, defeitos corrigidos antes de o membro ver. Checkpoint como draft navegável com pergunta granular; versões `page-v2.html`, log em `page/iterations-log.json`, 3 iterações sem progresso escalam; a aprovação consolida `design/page.html`.
- **Tokens** (`reference/design-tokens.md`): consolide `design-tokens.json` por código do HTML aprovado (`variant_chosen`, cores, tipografia, spacing base 4 ou 8, radii, shadow, `components_by_section` cruzado com o `sections_plan`).

### ETAPA 4 · Persistir `page-plan.json`, relatórios e manifest

Leia `reference/page-plan-e-salvar.md`. `page-plan.json` com o bloco `strategy` completo (`mechanism_name` LITERAL da `offer-builder`, `hero_type`, `page_type` igual no topo e dentro de `strategy`, `hybrid`), `sections_plan[]` com `eyebrow`, `blocks` e o campo `media` obrigatório, `section_order`, `brand_discovery`, `design_route`, `design_route_ref`, `destination_ref` e as refs dos arquivos de design.

## SALVAR

Em `workspace/[produto]/page/`: `page-plan.json`, `design-signals.json`, `design-tokens.json`, `design/page.html` (página do consumidor: SVG, sem emoji, sem logo Aura), `design/assets/` e `design-system.md`, cujo `.html` sai de `python3 tools/render_report.py workspace/[produto]/page/design-system.md` (convenções em `.claude/templates/aura-html-components.md`). Depois `python3 tools/manifest.py <slug> complete page-design` (`page_type` e `signals_source` ficam só no `page-plan.json`) e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Texto integral, self-audit silencioso e referências cruzadas em `reference/mensagem-final-e-self-audit.md`. Framing de draft: design aprovado (rota escolhida, `design/page.html` como fonte única), plano e tokens salvos; próximo passo é a `page-build` ('build page' ou 'deploy'), que compila esse HTML exato em Liquid. Antes de declarar concluído, rode os 5 gates do self-audit com a checklist do arquivo (mecanismo literal, `page_type` coerente, `media` completo, self-review rodado, markers em toda section, zero copy ou imagem da referência nas rotas 2 e 3).
