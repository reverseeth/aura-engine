# Aura Engine — Visão Geral Completa

Tudo que existe no ecossistema Aura: o que cada peça faz, como se conectam, e como uma sessão flui do início ao fim.

**Versão:** maio 2026
**Skills:** 15 (numeradas 00-14, com sub-cadeia 07a/07b/07c)
**Plataforma:** Claude Code (CLI da Anthropic)
**Raiz de output:** `/workspace/[product-slug]/`

---

## 1. O que é a Aura

A Aura é um sistema de duas partes pra construir e escalar marcas de ecommerce dentro do **Claude Code**, a CLI da Anthropic:

- **Base de Conhecimento Aura** — um servidor MCP remoto (ferramenta `search_knowledge`) que guarda os frameworks especialistas em que o raciocínio da Aura é construído (Schwartz, Hopkins, Hormozi, Cialdini, Sugarman, Ogilvy, Caples, mais metodologia original sobre construção de oferta, Meta Ads científico e produção de criativos). Conectada uma vez via Settings do Claude; consultada silenciosamente dentro de toda skill que precisa fundamentar uma decisão.
- **Aura Engine** — um projeto (clonado em `~/aura-engine`) contendo 15 skills, libs de suporte, rules, hooks e templates. Skills se ativam por contexto: o membro descreve o que precisa, a Aura identifica em qual fase está, e a skill apropriada roda.

**Princípio central:** cada fase produz artefatos versionados em `/workspace/[product-slug]/` que alimentam a próxima. Nada é jogado fora — copy bebe da pesquisa, criativos bebem da copy, ads bebem dos criativos, retenção bebe da venda.

**Filosofia de output:** todo arquivo `.md` que a Aura escreve tem um `.html` companion no mesmo diretório. O `.md` é a fonte que a AI lê na fase seguinte; o `.html` é a versão que o membro abre no browser pra ler com calma.

---

## 2. A Base de Conhecimento Aura (search_knowledge)

A Base de Conhecimento é a camada de expertise profunda que sustenta o raciocínio da Aura. Vive como um servidor MCP remoto, indexado e consultável por uma única chamada de tool.

### Como o membro conecta

Conexão acontece uma vez por dispositivo, e fica permanente até o membro remover.

- **Claude Desktop:** Settings → Integrations → Add Custom Integration → Nome *Aura* → URL `https://aura-mcp-production.up.railway.app/mcp` → Add
- **Claude Code (terminal):** `claude mcp add --transport http aura https://aura-mcp-production.up.railway.app/mcp`

Instruções completas com screenshots ficam em `Aura.html` (português) e `Aura-en.html` (inglês).

### O que tem dentro

A base agrega a literatura fundacional de direct-response e ecommerce mais metodologia original. Quando uma skill precisa fundamentar uma decisão, consulta com frases de intent específica. Exemplos por domínio:

| Domínio | Queries representativas |
|---|---|
| Pesquisa de produto | `product research criteria validation`, `market desires mass desire`, `market sophistication stages` |
| Pesquisa de mercado | `unified research document process`, `psychographic research drivers`, `voice of customer review mining`, `product market awareness Schwartz levels` |
| Análise de concorrente | `competitor research extracting claims`, `market sophistication saturation` |
| Construção de oferta | `unique mechanism UMP UMS theory`, `offer stack pricing guarantee`, `Hormozi grand slam offer value equation` |
| Copywriting | `headlines formulas process 100 lines`, `leads types Schwartz awareness`, `hero sections types selection`, `PDP product page copy`, `CTA psychology call to action` |
| Produção de criativo | `ad angles concepts variations`, `3-2-2 flexible ads format`, `hooks video ads`, `funnel creative playbook` |
| Meta Ads | `scientific method meta ads control variable`, `one campaign method AndroMeta`, `4Pi analysis spend frequency CPM`, `budget scaling methods 5% rule`, `performance gate scaling PGS` |
| Escala | `scaling strategy vertical horizontal`, `creative diversity scaling mechanism` |
| Retenção | `email lifecycle welcome abandoned cart post-purchase winback`, `Klaviyo flow trigger replenishment` |
| Reciclagem de conteúdo | `1 winner 9 derivatives formats advertorial email TikTok blog Pinterest` |

Toda busca roda com `deep=true` pra resultados completos. Múltiplas buscas por tópico são normais.

### Como se comporta dentro das skills

- **Sempre consultada, nunca nomeada.** Skills consultam a base sempre que precisam fundamentar uma recomendação, mas nunca avisam ao membro que estão buscando, nunca citam a fonte e nunca namedropam o material de curso por trás.
- **Autores e livros são citáveis.** Schwartz, Cialdini, Hopkins, Hormozi, Sugarman, Ogilvy, Caples etc. podem ser referenciados diretamente quando relevante — são conhecimento público.
- **Fontes internas não.** Nomes específicos de cursos, vaults, programas internos nunca aparecem pro membro.

**Por que importa:** a Base de Conhecimento é o que faz o output da Aura ser específico em vez de genérico. Sem ela, o sistema cairia no mesmo conselho superficial de marketing que um LLM sozinho produz.

---

## 3. Arquitetura geral

```
~/aura-engine/             ← clonado de github.com/reverseeth/aura-engine
├── .claude/
│   ├── CLAUDE.md          ← instruções fundamentais (idioma, copy rules, dual output, MCP)
│   ├── OVERVIEW.md / .html ← companion interno deste documento
│   ├── skills/            ← 17 arquivos .md (skills 00-14, com 07a/07b/07c)
│   ├── lib/               ← libs reutilizáveis chamadas pelas skills
│   ├── rules/             ← diretrizes auto-carregadas por contexto
│   ├── hooks/             ← scripts que rodam em eventos do Claude Code
│   ├── templates/         ← templates HTML, schemas JSON, snippet do logo SVG
│   └── settings.json      ← config do Claude Code (hooks, permissions)
│
├── AGENTS.md              ← mirror local do CLAUDE.md (gitignored, específico do membro)
└── workspace/             ← criado pela skill 00, organizado por produto
    ├── profile.md         ← contexto do membro (budget, ESP, tools, mercado, idioma)
    └── [product-slug]/
        ├── manifest.json  ← single source of truth do estado do produto
        └── 01..14         ← artefatos versionados produzidos por cada skill
```

A Base de Conhecimento Aura **não** está nesta árvore — é um servidor MCP remoto conectado separadamente. Engine e Base de Conhecimento são independentes.

---

## 4. As 15 skills (em detalhe)

Cada skill é um arquivo `.md` com frontmatter (nome + descrição) e corpo estruturado em ETAPAs numeradas. Skills estão listadas abaixo na ordem em que o membro roda em uma sessão normal.

### Skill 00 — Setup
**Trigger:** `"setup"`
Configuração da primeira vez. Pergunta o idioma preferido pra relatórios internos (`pt-BR` ou `en`), cria `/workspace/` com o slug do produto, coleta contexto do membro (budget, ESP, tools, mercado) em `profile.md`, inicializa `manifest.json`.
**Output:** `manifest.json` + `profile.md`

### Skill 01 — Product Research
**Trigger:** `"product research"`
Valida produtos contra critérios (mass desire, mass urgency, mass uniqueness), aplica framework de sophistication de Schwartz (stages 1-5), recomenda go/no-go.
**Enrichment opcional:** quando MCP TrendTrack conectado, ETAPA 0.5 usa `find_winning_products` + `search_shops` + `creative_inspiration_pack`.
**Output:** `01-product-research.md/html`

### Skill 02 — Market Research
**Trigger:** `"market research"`
VOC mining em Reddit, fóruns, reviews, TikTok comments. Identifica frases exatas (verbatim), mapeia awareness distribution, drivers psicográficos, objeções ranqueadas.
**Por que importa:** o documento mais consultado do sistema.
**Output:** `02-market-research.md/html/json`

### Skill 03 — Competitor Analysis
**Trigger:** `"competitor analysis"`
Identifica 5-10 concorrentes ativos via Meta Ad Library + Similarweb. Analisa PDPs. ETAPA 3C: análise profunda de criativos escalados via Whisper transcription.
**Fallback chain pra páginas bloqueadas:** Wayback Machine → archive.today.
**Enrichment opcional:** quando MCP TrendTrack conectado, ETAPA 0.5 colapsa ETAPAs 1-3 em `brief_competitor` + `search_shops` + `find_similar_shops` + `scan_ad`.
**Output:** `03-competitor-analysis.md/html` + `03-creative-patterns.json`

### Skill 04 — Offer Builder
**Trigger:** `"offer"`
Constrói mecanismo único (UMP/UMS theory). ETAPA 2.5 obrigatória — Research Foundation. Pricing triangulado, bonus stack, garantia, unit economics, 11 sanity checks.
**Outputs críticos pras skills downstream:**
- `bonuses[]` array → lido pela skill 05
- `offer_stack` string → lido pela skill 06
- `unit_economics.weighted_margin_per_order` + `target_cpa_primary_2x/3x` → lidos pela skill 11

**Output:** `04-offer.md/html/json` + `04-research-foundation.json`

### Skill 05 — Bonus Delivery
**Trigger:** `"bonus delivery"`
Asset prep pros bonuses definidos na skill 04. Pra cada bonus, gera pipeline de entrega conforme `delivery_trigger`.
**Output:** `05-bonus-delivery/[bonus-id]/`

### Skill 06 — Copy Engine
**Trigger:** `"copy"`
Headlines ("Process of 100" de Caples). Lead types por awareness stage. Hero sections, bullets, social proof, FAQ, urgency, email hooks. 8 sweeps de revisão.
**Output:** `06-copy.md/html/json`

### Skill 07 — Page Engine (cadeia 07a → 07b → 07c)
**Trigger:** `"page"`
Dividida em três pra performance e iteration loop.
- **07a — Planning:** detecta tipo de página, brand discovery, design system orchestration, blueprint visual via Google Stitch (opt-in)
- **07b — Sections:** 3 hero variants → inline-blocks Shopify → demais sections → UX writing pass + Liquid validation
- **07c — Deploy:** **GATE skill 09**, cria `templates/page.[produto].json`, deploy seguro (duplicate → pull → cp → push --nodelete), smoke test

**Page registry:** quando múltiplas páginas existem pra um produto, `07-page/page-registry.md` centraliza URL, frame, opening line, message-match ad→page.

### Skill 08 — Creative Engine
**Trigger:** `"creatives"`
Pipeline completo. Por conceito: 3 format variants (Real Cuts / Hyper Motion / AI UGC). ETAPAs: detecção de material, quantidade por stage, ângulos das 3 verticais, regras estruturais, briefings, prompts production-ready (Higgsfield), LP congruency mapping, hooks bank, DNA registry load/extract, compliance pre-flight.
**Enrichment opcional:** quando MCP TrendTrack conectado, Hooks Bank ganha archetypes vencedores reais.
**Output:** `08-creatives.json` + 1 briefing por conceito

### Skill 09 — Consistency Audit
**Trigger:** `"consistency audit"` / `"audit"`
Cross-phase drift detection: mecanismo, awareness stage, VOC, oferta concordam entre todos os artefatos (skills 02 → 03 → 04 → 06 → 07 → 08). VOC traceability + promise↔config.
**Vira gate:** skills 07c, 10, 13 abortam em `BLOCK`.
**Output:** `09-consistency-audit.md/html/json` com `launch_recommendation`

### Skill 10 — Ad Strategy
**Trigger:** `"ad strategy"`
Pre-flight pra Pixel/CAPI/produto live/criativos prontos. One Campaign Method, 3-2-2 ad sets, naming convention, decisão por timeline, PGS automático. Inclui árvore de analytics (Meta App / Wetracked / Triple Whale / Aimerce).
**GATE skill 09** roda no pre-flight.
**Output:** `10-ad-strategy.md/html/json` + manifest `10_campaign_name`

### Skill 11 — Ad Analysis
**Trigger:** `"ad analysis"`
4Pi (Spend, Frequency, CPM, Cost per Result). LOSER detection dinâmico (lê unit_economics da skill 04). 19-Point Loser Diagnostic. Identifica WINNERs.
**Enrichment opcional:** quando MCP TrendTrack conectado, `scan_ad` faz benchmark dos winners e `daily_radar` monitora concorrentes.
**Output:** `11-analysis/[timestamp].json` + `latest.json`

### Skill 12 — Scale Engine
**Trigger:** `"scale"`
Vertical scaling (PGS 5% rule). Horizontal scaling. Champion promotion. Diversification por stage.
**Output:** `12-scale/[timestamp].md`

### Skill 13 — Retention Engine
**Trigger:** `"retention"` / `"email flows"` / `"klaviyo"`
ESP identificado, ≥50 compras. Fluxos base: welcome series, abandoned cart, post-purchase, win-back, replenishment.
**GATE skill 09** no pre-flight.
**Enrichment opcional:** `analyze_shop_emails` calibra timing dos fluxos.
**Output:** `13-retention/[fluxo]/`

### Skill 14 — Content Recycler
**Trigger:** `"content recycler"` / `"recycle [id]"` / `"recycle winner"`
Lê 1 criativo winner (auto-detect via `11-analysis/latest.json.winners[]`). Extrai essência. Gera 9 derivadas: advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad.
**Output:** `14-recycled/[source-id]/` com 9 `.md` + 9 `.html`

---

## 5. Sistema de libs

Libs reutilizáveis em `.claude/lib/`.

| Lib | Função | Usada por |
|---|---|---|
| **compliance-preflight** | Detecta palavras ad-flag que disparam disapproval no Meta/TikTok. Output: JSON com `severity` + `rewrite_suggestion`. | 06, 07b, 07c, 08, 14 |
| **content-recycler** | Engine prompt-driven pra skill 14. Arquivos: `recycler.md` + `formats.json`. | 14 |
| **creative-dna** | Cross-product DNA registry. Skill 08 salva padrões abstratos; próxima execução em outro produto carrega e adapta. | 08 |
| **hook-taxonomy** | Taxonomia de hooks (Problema / Resultado / Curiosidade / Prova Social). | 08 |
| **prompt-directors** | Directors de prompt pra ferramentas externas (Higgsfield Marketing Studio). | 08 (ETAPA 5.7) |
| **trendtrack-integration** (opcional) | Integração read-only com MCP TrendTrack. 11 tools. Detecção runtime: tools com prefixo `mcp__trendtrack__`. Aura funciona 100% sem ela. | 01, 03, 08, 11, 13 |
| **automations/ (Meta + Shopify)** | Vive em `.claude/automations/`. Cascade resiliente pra Meta Ads: **(1)** MCP oficial da Meta `mcp.facebook.com/ads` (open beta desde 2026-04-29, tools `mcp__meta__ads_*`, 29 tools); **(2)** MCP Pipeboard 3rd-party (tools `mcp__meta-ads__*`) como fallback automático; **(3)** paste manual. Receitas: `sync-campaign-from-meta-official.md`, `sync-campaign-from-meta.md`, `pause-ad-set.md`, `upload-creative-to-meta.md`, etc. | 10, 11 |

**Por que cascade no Meta:** o MCP oficial está em rollout gradual — algumas ad accounts aparecem "disabled" mesmo depois do setup correto. Manter Pipeboard como fallback elimina dependência da Meta liberar acesso.

---

## 6. Sistema de rules

Diretrizes em `.claude/rules/` auto-carregadas pelo Claude Code conforme contexto.

| Rule | Quando aplica |
|---|---|
| `pre-launch-gates` | **NON-NEGOTIABLE.** Dois gates: ad-flag compliance e Promise↔Config. |
| `shopify-theme-safety` | Toda operação Shopify CLI. Pull antes de edit, `--nodelete`, marker verification. |
| `iteration-driven-refinement` | Skills que geram asset. Primeira versão é draft, máximo 3 iterações. |
| `member-stage-awareness` | Toda skill. Detecta starter / validating / scaling e adapta tom. |
| `emergency-escape-paths` | ES1-ES7 cobrem pre-flights travados, workspace corrompido, etc. |
| `troubleshooting-patterns` | Quando skill não entrega. Árvore de diagnóstico estruturada. |
| `post-task-self-audit` | Toda skill peso médio/alto. 5 gates silenciosos antes de declarar "completo". Fixes inline silenciosos. |
| `reverse-order-insertion` | Inserir múltiplos elementos em arquivo em ordem reversa pra line numbers não shiftarem. |

**Rules são diretrizes, não código enforced.** O Claude lê e aplica. A camada real de enforcement são os hooks.

---

## 7. Sistema de hooks

Scripts em `.claude/hooks/` registrados em `.claude/settings.json`.

### post-start.sh
**Quando:** abertura de sessão Claude Code (1× por dia).
**O que faz:** adiciona o alias `aura` no shell rc do membro.

### Hooks globais (vindos de ~/.claude/settings.json)
- `enforce-git-push-authority.sh` — só @devops pode push
- `sql-governance.py` — bloqueia SQL perigoso
- `enforce-delegation.cjs` — orchestrators não podem executar
- `enforce-architecture-first.cjs` — docs antes de código protegido
- `enforce-story-gate.cjs` — story obrigatória antes de código
- `synapse-wrapper.cjs` — context injection no prompt

Esses hooks vêm do framework SINAPSE global. Aura herda eles, mas não depende.

---

## 8. Sistema de templates

Em `.claude/templates/`.

### aura-report-template.html
Template HTML self-contained (CSS inline) usado por toda skill que gera companion `.html`. Componentes: `section-label`, `callout`, `note`, `opportunity`, `danger`, `table-wrap`, `quote`, `pill`, `winner`, `kpi-grid`.

### aura-logo-snippet.html
Bloco SVG do logo Aura (6 linhas). **Obrigatório no topo de TODO `.html` gerado**, copiado literalmente. Proibido substituir por texto.

### manifest-schema.json
JSON Schema (draft-07) pro `manifest.json`. `additionalProperties: true` — skills podem gravar campos extras. Obrigatórios: `product_slug`, `product_name`, `created_at`, `updated_at`, `skills_completed`.

---

## 9. Estrutura do workspace

Cada produto vive em `/workspace/[slug]/`.

```
/workspace/produto-x/
├── manifest.json                      ← estado central
├── 01-product-research.md / .html
├── 02-market-research.md / .html / .json
├── 03-competitor-analysis.md / .html
├── 03-creative-patterns.json
├── 04-offer.md / .html / .json
├── 04-research-foundation.json
├── 05-bonus-delivery/
├── 06-copy.md / .html / .json
├── 07-page/
│   ├── 07-design-system.md
│   ├── 07-plan.md / .json
│   ├── 07-sections-report.md
│   ├── 07-deploy-report.md / .json
│   └── page-registry.md / .html       ← multi-page slug index
├── 08-creatives.json
├── 08-creatives/
│   └── briefing-c01.md / .html + prompt files
├── 09-consistency-audit.md / .html / .json
├── 10-ad-strategy.md / .html / .json
├── 11-analysis/
├── 12-scale/
├── 13-retention/
│   ├── welcome-series/
│   ├── abandoned-cart/
│   └── ...
└── 14-recycled/
    └── [source-id]/
```

`/workspace/profile.md` (fora de qualquer produto) guarda dados do membro: budget, ESP, tools, mercado, idioma. Escrito pela skill 00, lido por todas.

---

## 10. Convenções operacionais

### Idioma e estilo (CLAUDE.md rule 0)
- **Relatórios internos:** no idioma escolhido durante setup (`pt-BR` ou `en`).
- **Copy pro consumidor final:** sempre em inglês (mercado US padrão), independente do idioma de relatório interno.

### Uso da Base de Conhecimento (CLAUDE.md rules 1-3)
- Skills consultam `search_knowledge` silenciosamente.
- Nomes de cursos/programas internos nunca citados. Livros e autores (Schwartz, Cialdini, Hopkins, Hormozi, etc.) podem ser referenciados diretamente.

### Dual output (.md + .html) — CLAUDE.md rule 6b
- `.md` é a fonte que a AI lê na fase seguinte
- `.html` é a versão humana (browser)
- HTML usa `aura-report-template.html` + logo SVG no topo

### Logo SVG obrigatório
- Bloco SVG copiado literalmente de `aura-logo-snippet.html`
- Proibido substituir por texto. Sem fallback.

### Ícones SVG, nunca emojis em UI consumidor — rule 7
- PDPs, landings, checkouts: SVGs inline (Lucide, Heroicons, Phosphor, custom)
- Exceção: relatórios internos em `/workspace/` podem usar emojis pra velocidade de escaneamento

### Copy rules — rule 8
- **8a** — minimizar em-dashes (—). Zero em headlines, ≤2 em copy longa.
- **8b** — substituições automáticas de palavras ad-flag pra política Meta/TikTok.

### Self-audit silencioso obrigatório — rule 9
Antes de declarar qualquer skill "completa", 5 gates mentais rodam silenciosamente. Fixes inline sem mencionar. Surface só quando precisa decisão do membro.

### Integrações MCP opcionais — rule 10
A Aura detecta MCPs externos e enriquece skills automaticamente. **Meta MCP** (cascade oficial → Pipeboard → manual) e **TrendTrack MCP** são os casos principais.

---

## 11. Memória persistente — registry creative-dna

Cross-product learning. A skill 08 (creatives) salva DNA toda vez que executa: hook archetypes que funcionaram, voice signatures, padrões estruturais. Próxima execução em outro produto carrega esse registry e adapta sem reinventar.

**Read/write:** via `lib/creative-dna/registry.py`. Skill 08 chama em silent steps (ETAPA 7.4 carrega, ETAPA 7.6 escreve).

**O que NÃO entra no registry:** dados específicos do produto (nomes, claims, preços). Só padrões abstratos.

---

## 12. Integrações MCP opcionais — Meta + TrendTrack

A Aura é desenhada em volta de um padrão cascade resiliente pra MCPs externos. Cada skill enriquecida detecta tools MCP disponíveis em runtime e usa como fonte primária; ausência dispara fallback silencioso. O membro nunca vê estado quebrado.

### 12.1 — Meta Ads MCP (cascade: oficial → Pipeboard → manual)

A Meta lançou o **MCP oficial de Ads** em 2026-04-29 em `mcp.facebook.com/ads` com 29 tools. A Aura usa como caminho preferencial com fallback automático pro Pipeboard 3rd-party (o oficial está em rollout gradual — algumas contas aparecem "disabled").

**Como o membro conecta:**

Passo 1 — Meta MCP oficial (preferencial):
- **Claude Desktop:** Settings → Connectors → Add custom connector → Nome `meta` → URL `https://mcp.facebook.com/ads` → OAuth via Business Suite
- **Claude Code:** `claude mcp add --transport http meta https://mcp.facebook.com/ads`

Passo 2 — Pipeboard fallback (recomendado em paralelo): token long-lived do Marketing API (60d) + registrar como `meta-ads`. Setup completo em `.claude/automations/setup-mcps.md`.

**As 29 tools oficiais (5 categorias):**

| Categoria | Tools | Propósito |
|---|---|---|
| Campaign Create/Manage (5) | `ads_create_campaign`, `ads_create_ad_set`, `ads_create_ad`, `ads_update_entity`, `ads_activate_entity` | Lifecycle completo via linguagem natural |
| Product Catalog (10) | `ads_catalog_create`, `ads_catalog_get_*` | Integração de catálogo Shopify, monitoramento de feed |
| Accounts / Pages / Assets (3) | `ads_get_ad_accounts`, `ads_get_ad_entities`, `ads_get_pages_for_business` | Descoberta de hierarquia |
| Dataset / Pixel / CAPI Quality (4) | `ads_get_dataset_details`, `ads_get_dataset_quality`, `ads_get_dataset_stats`, `ads_get_errors` | **Exclusivo do oficial** — match quality, deduplication, errors |
| Insights / Benchmarks (7) | `ads_insights_advertiser_context`, `ads_insights_anomaly_signal`, `ads_insights_auction_ranking_benchmarks`, `ads_insights_industry_benchmark`, `ads_insights_performance_trend`, `ads_get_opportunity_score`, `ads_get_help_article` | **Exclusivo do oficial** — benchmarks por vertical, auction ranking, anomalias |

**Onde a Aura usa:**

| Skill / Receita | Tools | O que melhora |
|---|---|---|
| 11 ad analysis (ETAPA 1) | Cascade via `sync-campaign-from-meta-official.md` | Auto-pull + market context (industry benchmark, auction ranking, opportunity score, anomalies). Compara membro vs vertical p50. |
| 10 ad strategy (pre-flight) | `ads_get_dataset_quality` | Gate de Match Quality ≥80% antes do launch |
| `pause-ad-set.md` | `ads_update_entity` (cascade) | PGS guard sem interação manual |
| `upload-creative-to-meta.md` | Continua via Pipeboard/Playwright | MCP oficial não aceita arquivos locais |

**Por que o cascade importa:** o MCP oficial está em rollout gradual. Pipeboard como fallback automático significa que a Skill 11 nunca trava.

**Custo / rate limits:** MCP oficial é grátis durante a open beta; pricing futuro não anunciado. Sem rate limits documentados. Pipeboard usa Marketing API direto (200/hora + 100k/48h). Ambos $0 hoje.

### 12.2 — TrendTrack MCP (enrichment de research)

TrendTrack é uma ferramenta paga 3rd-party que indexa 1M+ shops Shopify. O servidor MCP expõe 11 tools read-only.

**Como o membro conecta (opcional):**
- **Claude Desktop:** Settings → Connectors → Add custom connector → URL `https://api.trendtrack.io/v1/mcp` → OAuth login
- **Claude Code:** `claude mcp add --transport http trendtrack https://api.trendtrack.io/v1/mcp`

**As 11 tools:**

| Tool | Categoria | Propósito |
|---|---|---|
| `find_winning_products` | Discover | Top products num nicho com revenue tracked |
| `search_shops` | Discover | Busca free-text no universo Shopify indexado |
| `find_similar_shops` | Discover | Shops comparáveis por similaridade |
| `creative_inspiration_pack` | Discover | Hooks, landing pages, ângulos, media benchmarks |
| `brief_competitor` | Brief | Análise competitiva completa |
| `scan_ad` | Brief | Decompõe 1 Meta ad |
| `analyze_tracked_brand` | Brief | Deep dive em marca trackada |
| `analyze_shop_emails` | Brief | Padrões de email |
| `daily_radar` | Monitor | Movimentos das marcas trackadas |
| `list_tracked_brands` | Monitor | Lista de marcas |
| `check_credits` | Account | Saldo, uso, limites |

**Mapping skill ↔ tool:**

| Skill | Tools | O que melhora |
|---|---|---|
| 01 product research | `find_winning_products`, `search_shops` | Valida contra winners reais |
| 03 competitor analysis | `brief_competitor`, `scan_ad`, `search_shops`, `find_similar_shops` | ETAPAs 1-3 colapsam em 1-2 tool calls |
| 08 creatives | `creative_inspiration_pack`, `scan_ad` | Hooks Bank com archetypes reais |
| 11 ad analysis | `scan_ad`, `daily_radar` | Benchmark de winners + loop de monitoramento |
| 13 retention | `analyze_shop_emails` | Timing dos fluxos calibrado contra concorrência |

**Padrão de detecção:** tools com prefixo `mcp__trendtrack__` → fonte primária. Ausente → fallback silencioso.

**Custos:** sistema de créditos. Quando skill planeja >5 chamadas, roda `check_credits` primeiro.

**Privacidade:** OAuth read-only. Aura não armazena tokens.

---

## 13. Como rodar uma sessão completa do zero

Ordem canônica pra um produto novo:

1. **setup** — cria workspace, profile, manifest
2. **product research** — valida o produto, define vertical
3. **market research** — VOC, awareness, drivers
4. **competitor analysis** — 5-10 concorrentes, padrões, gaps
5. **offer** — mecanismo, pricing, stack, garantia, unit economics
6. **bonus delivery** — asset prep dos bonuses
7. **copy** — copy completa pra cada section
8. **page** — 07a (planning) → 07b (sections) → 07c (deploy)
9. **creatives** — 6-15 conceitos com briefings
10. **consistency audit** — cross-phase drift check (gate)
11. **ad strategy** — estrutura de campanha, naming, PGS
12. **— LAUNCH —**
13. **ad analysis** (depois de 3-7 dias) — 4Pi, diagnóstico, decisões
14. **scale** (depois que winners emergem) — vertical + horizontal
15. **retention** (≥50 compras) — fluxos Klaviyo
16. **content recycler** (depois de winner consolidado) — 9 derivadas

Cada skill faz pre-flight da anterior. Se algum artefato falta, oferece fallback (rule `emergency-escape-paths` — ES1).

**Iteration loop normal:** depois de cada launch, ad analysis + iteração de creative ou copy é o ciclo. Skill 09 reroda antes de qualquer relaunch crítico.

---

## 14. Mudanças recentes

Os números das skills refletem a numeração da época de cada mudança.

| Data | Mudança |
|------|---------|
| 2026-04-30 | Skill 06 deprecated removida (era só um redirect) |
| 2026-04-30 | Skill 17 renomeada pra 14 (numeração contígua) |
| 2026-04-30 | Drift 04↔09 corrigido (`weighted_margin_per_order`, `target_cpa_primary_2x/3x` adicionados ao output da 04) |
| 2026-04-30 | Drift 04↔05 corrigido (`offer_stack` adicionado ao output da 04) |
| 2026-04-30 | Drift 08↔09 corrigido (skill 08 grava `08_campaign_name` no manifest) |
| 2026-04-30 | Skill 11 vira hard gate em 06c, 08, 12 (lê `launch_recommendation`, aborta em BLOCK) |
| 2026-04-30 | Google Cache removido do fallback chain da 03 (descontinuado set/2024) |
| 2026-04-30 | URL hardcoded do Higgsfield substituída por URL genérica |
| 2026-04-30 | Libs órfãs deletadas: `shocking-stats`, `whisper-transcribe`, `section-patterns` |
| 2026-04-30 | Skill 14 ganha companion `.html` obrigatório (rule 6b) |
| 2026-04-30 | CLAUDE.md atualizado com skill 14 na lista oficial |
| 2026-04-30 | **Integração MCP TrendTrack** adicionada como lib opcional. Skills 01, 03, 08, 11, 13 ganham ETAPAs condicionais. Fallback silencioso. CLAUDE.md ganha rule 10. |
| 2026-05-11 | **Integração do MCP oficial da Meta** (`mcp.facebook.com/ads`, open beta desde 2026-04-29). Nova receita `sync-campaign-from-meta-official.md` usa as 29 tools nativas. Skill 11 ETAPA 1 vira cascade: oficial → Pipeboard → manual. `pause-ad-set.md` ganha cascade interno. CLAUDE.md rule 10 expandida. |
| 2026-05-03 | Self-audit silencioso obrigatório no fim de toda skill (rule + CLAUDE.md rule 9) |
| 2026-05-03 | **Renumeração completa das skills** pra match com ordem de execução: bonus-delivery 13→05, copy 05→06, page 06→07, creatives 07→08, consistency-audit 11→09, ad-strategy 08→10, ad-analysis 09→11, scale 10→12, retention 12→13. Content-recycler permanece 14. |
| 2026-05-04 | Skill 00 setup pergunta idioma de relatório (`pt-BR` ou `en`) como primeira pergunta; salvo em `profile.md` como `report_language`. |
| 2026-05-04 | Page registry pattern introduzido: `07-page/page-registry.md` centraliza URL, frame e dados de message-match ad↔page pra múltiplos criativos referenciarem páginas por slug. |
