# Aura Engine — Visão Geral Completa

Este documento explica tudo que existe no Aura Engine: o que cada peça faz, como elas conectam, e como uma sessão flui do início ao fim. Pensado pra quem está se reorientando depois de ter adicionado várias funções ao longo do tempo.

---

## 1. O que é o Aura Engine

Sistema completo pra construir e escalar marcas de ecommerce. Funciona dentro do Claude Code (CLI da Anthropic) como um conjunto de skills + libs + rules + hooks que se ativam por contexto. O membro descreve o que precisa, o Aura identifica em qual fase está e executa a skill apropriada.

**Princípio central:** cada fase produz artefatos versionados em `/workspace/[produto]/` que alimentam a próxima. Nada é jogado fora — copy bebe da pesquisa, criativos bebem da copy, ads bebem dos criativos, retenção bebe da venda.

**Filosofia de output:** todo arquivo `.md` salvo tem um `.html` companion no mesmo diretório. O `.md` é a fonte que a AI lê na fase seguinte; o `.html` é a versão que o membro abre no browser pra ler com calma.

---

## 2. Arquitetura geral

```
.claude/
├── CLAUDE.md              ← instruções fundamentais (idioma, copy rules, dual output)
├── OVERVIEW.md            ← este documento
├── skills/                ← 15 skills (00-14, sendo 07 dividida em 07a/07b/07c — 17 arquivos .md no total)
├── lib/                   ← bibliotecas reutilizáveis chamadas pelas skills
├── rules/                 ← diretrizes carregadas automaticamente por contexto
├── hooks/                 ← scripts que rodam em eventos do Claude Code
├── templates/             ← templates HTML, schemas JSON, snippets de logo
└── settings.json          ← configuração do Claude Code (hooks, permissions)

workspace/                 ← criado por skill 00, organizado por produto
└── [produto-slug]/
    ├── manifest.json      ← estado central do produto (single source of truth)
    ├── profile.md         ← contexto do membro (budget, tools, experiência)
    ├── 01-product-research.md
    ├── 02-market-research.md
    ├── 03-competitor-analysis.md
    ├── 03-creative-patterns.json
    ├── 04-offer.md / .json / 04-research-foundation.json
    ├── 05-bonus-delivery/
    ├── 06-copy.md / .json
    ├── 07-page/           ← cadeia 07a → 07b → 07c
    ├── 08-creatives.json + briefings .md por conceito
    ├── 09-consistency-audit.json / .md
    ├── 10-ad-strategy.md / .json
    ├── 11-analysis/       ← uma análise por execução + latest.json
    ├── 12-scale/
    ├── 13-retention/      ← fluxos por canal
    └── 14-recycled/[source-id]/   ← derivadas de 1 winner
```

---

## 3. As 15 skills (em detalhe)

Cada skill é um arquivo `.md` com frontmatter (nome + descrição) + corpo estruturado em ETAPAs. O Claude lê a skill, segue as etapas, e salva os artefatos prescritos.

### Skill 00 — Setup
**Arquivo:** `00-setup.md`
**Trigger:** "setup"
**O que faz:**
- Cria `/workspace/` com slug do produto
- Coleta dados do membro pra `profile.md` (budget diário, ESP, ferramentas, mercado)
- Inicializa `manifest.json` com schema mínimo
- Detecta se o membro já está em meio a outro produto e oferece continuação

**Output:** `/workspace/[slug]/manifest.json` + `/workspace/profile.md`.

### Skill 01 — Product Research
**Trigger:** "product research"
**O que faz:**
- Avalia produtos contra critérios de validação (mass desire, mass urgency, mass uniqueness)
- Aplica framework de Schwartz (sophistication stage 1-5)
- Recomenda go/no-go com base em sinais de mercado
- Se membro não tem produto definido, sugere produtos viáveis no nicho

**Output:** `01-product-research.md` + atualização do manifest com `product_vertical`.

### Skill 02 — Market Research
**Trigger:** "market research"
**O que faz:**
- Voice of Customer (VOC) mining em Reddit, fóruns, reviews, TikTok comments
- Identifica frases exatas (verbatim) usadas pelo público
- Mapeia awareness distribution (% unaware, problem aware, solution aware, product aware, most aware)
- Detecta drivers psicográficos (medos, desejos, identidade, sonhos)
- Lista objeções organizadas por intensidade

**Por que importa:** este é o documento mais consultado. Skills 04 (oferta), 05 (copy), 07 (criativos) leem dele pra fundamentar tudo.

**Output:** `02-market-research.md` + `02-market-research.json` com VOC array.

### Skill 03 — Competitor Analysis
**Trigger:** "competitor analysis"
**O que faz:**
- Identifica 5-10 concorrentes ativos via Meta Ad Library + Similarweb
- Análise de PDPs (estrutura, headlines, mecanismos, garantias, social proof)
- ETAPA 3C: análise profunda de criativos escalados via Whisper transcription
- Extrai padrões e gaps que podem virar ângulo

**Fallback chain pra páginas bloqueadas:** Wayback Machine → archive.today (Google Cache foi descontinuado em 2024 e foi removido).

**Output:** `03-competitor-analysis.md` + `03-creative-patterns.json`.

### Skill 04 — Offer Builder
**Trigger:** "offer"
**O que faz:**
- Constrói mecanismo único (UMP/UMS theory)
- ETAPA 2.5 obrigatória — Research Foundation: cada claim do mecanismo precisa de evidência rastreável
- Pricing triangulado (3 ancoras: COGS, valor entregue, dor evitada)
- Stack de bonuses com ancoragem de valor
- Garantia que ataca a objeção #1
- Unit economics (margin per unit, breakeven ROAS, target CPA pra 2x e 3x)
- 11 sanity checks antes de salvar

**Outputs críticos pro próximo skill:**
- `bonuses[]` array (lido por skill 05 bonus-delivery)
- `offer_stack` string (lido por skill 06 copy)
- `unit_economics.weighted_margin_per_order` + `target_cpa_primary_2x/3x` (lido por skill 11 ad-analysis)

**Output:** `04-offer.md` + `04-offer.json` + `04-research-foundation.json`.

### Skill 06 — Copy Engine
**Trigger:** "copy"
**O que faz:**
- Headlines (process de geração — adapta o "Process of 100" de Caples ao volume necessário)
- Lead types selecionados por awareness stage (Story, Problem-Solution, Secret, Offer, Proclamation, Direct)
- Hero section apropriado ao tipo de página
- Bullets, social proof, FAQ, urgency
- Email hooks (pra skill 13 reutilizar)
- 8 sweeps de revisão (clarity, VOC, specificity, flow, objection, CTA, originality, compliance)
- Compliance pre-flight inline (rule 8b do CLAUDE.md)

**Output:** `06-copy.md` + `06-copy.json` (lido pela skill 07 page chain).

### Skill 07 — Page Engine (cadeia 07a → 07b → 07c)

**Por que está dividida em 3:** o monolítico tinha 1055 linhas. Quebrar em 3 melhora performance e permite iteration loop em fase específica sem regenerar tudo.

#### 07a — Page Planning
**Trigger:** "page" (entry point) ou "page-planning" direto
- Pre-flight (skill 06 completa, manifest válido)
- Detecta tipo de página (advertorial vs landing vs hybrid)
- Brand discovery + opcional referência visual
- Design system orchestration: cor → typography → spacing → grid → tokens
**Output:** `07-page/07-design-system.md` + `07-plan.md` + `07-plan.json`

#### 07b — Page Sections
- Gera 3 variantes de hero (membro escolhe A/B/C)
- Converte pra padrão de blocks inline no schema Shopify
- Replica pras demais sections do plano
- UX writing pass + self-critique (Nielsen + WCAG 2.1 AA)
- Validação Liquid via `shopify-plugin:shopify-liquid` com retry logic
**Output:** arquivos `.liquid` em `<staging>/sections/` + `07-sections-report.md`

#### 07c — Page Deploy
- **Gate de skill 09** (consistency audit) no pre-flight: se BLOCK, aborta
- Cria `templates/page.[produto].json` com blocks pré-populados
- Validação OBRIGATÓRIA de blocks (não-vazios, types válidos)
- Deploy seguro: duplicate theme → pull → cp → push --nodelete
- Smoke test pós-push (curl no storefront, grep marker)
**Output:** preview URLs + `07-deploy-report.md` + `.json`

### Skill 08 — Creative Engine
**Trigger:** "creatives"
**O que faz:**
- ETAPA 1: detecta material disponível + creator archetype
- ETAPA 2: calcula quantidade de conceitos por stage do membro (3-4 starter, 6-8 validating, 10-15 scaling)
- ETAPA 3: gera ângulos das 3 verticais (problema, resultado, identidade)
- ETAPA 4.5: regras estruturais globais (VOC traceability, hook rotation, swap viability)
- ETAPA 5: briefings completos por conceito
- ETAPA 5.7: production-ready prompts (Higgsfield + GPT Image 2.0)
- ETAPA 6: LP congruency mapping (qual LP cada conceito direciona)
- ETAPA 7: hooks bank (10 alternativas pra iterações futuras)
- ETAPA 7.4: carrega DNA aprendido do registry (cross-product learning)
- ETAPA 7.5: compliance pre-flight (rule 8b)
- ETAPA 7.6: DNA registry extraction (silent — alimenta `lib/creative-dna/registry.py`)
- ETAPA 8: resumo de produção

**Output:** `08-creatives.json` + 1 briefing `.md` por conceito.

### Skill 10 — Ad Strategy
**Trigger:** "ad strategy"
**O que faz:**
- **Gate de skill 09** no pre-flight (BLOCK se drift crítico)
- Verificação de pré-requisitos (Pixel, CAPI, produto ativo, criativos prontos)
- Estrutura de campanha (One Campaign Method)
- Ad sets em estrutura 3-2-2 (3 conceitos × 2 hooks × 2 thumbnails)
- Naming convention padrão (campaign_name único por batch — gravado no manifest pra skill 11 cruzar)
- Decisão por timeline (dia 1/3/7/14)
- PGS (Performance Gate Scaling) automático

**Output:** `10-ad-strategy.md` + `.json` + manifest atualizado com `10_campaign_name`.

### Skill 11 — Ad Analysis
**Trigger:** "ad analysis"
**O que faz:**
- 4Pi analysis (Spend, Frequency, CPM, Cost per Result)
- LOSER detection dinâmico (lê `04-offer.json.unit_economics.weighted_margin_per_order` + `target_cpa_primary_2x/3x`)
- 19-Point Loser Diagnostic (4 camadas: targeting, hook, copy, oferta)
- Identifica WINNERs (CPA < target × 0.7, spend > $300, idade > 5 dias)
- Recomenda iteração ou scale

**Output:** `11-analysis/[timestamp].json` + `11-analysis/latest.json` (handoff pra skill 12 e skill 14).

### Skill 12 — Scale Engine
**Trigger:** "scale"
**O que faz:**
- Pre-flight (skills 10 + 11 completas)
- Vertical scaling (5% rule do PGS)
- Horizontal scaling (novos ad sets, novos placements, novos angles)
- Champion promotion (Post ID dedicated)
- Diversification (stage scaling tem requisitos diferentes — Tier 1/2/3+)

**Output:** `12-scale/[timestamp].md` + plano de execução.

### Skill 09 — Consistency Audit
**Trigger:** "consistency audit" ou "audit"
**O que faz:**
- Cross-phase drift detection: confere se mecanismo, awareness stage, VOC, oferta batem entre todos os artefatos (skills 02 → 03 → 04 → 06 → 07 → 08)
- Identifica VOC traceability (frases na copy/ads vêm da pesquisa)
- Verifica promise↔config (promessas de copy batem com config da loja Shopify)

**Output:** `09-consistency-audit.json` com `launch_recommendation: "BLOCK" | "CAUTION" | "GO"`.

**Como vira gate:** skills 07c, 10, 13 leem esse JSON no pre-flight. Se BLOCK, abortam.

### Skill 13 — Retention Engine
**Trigger:** "retention", "email flows", "klaviyo"
**O que faz:**
- **Gate de skill 09** no pre-flight
- Pre-flight: ESP identificado (Klaviyo / Omnisend / MailerLite), ≥50 compras
- Fluxos base: welcome series, abandoned cart, post-purchase, browse abandon, win-back, replenishment
- Adapta cada fluxo ao produto (lê `04-offer.md` pra reorder rate, guarantee, bonuses)
- Templates Klaviyo (HTML + flow JSON)

**Output:** `13-retention/[fluxo].md` + arquivos exportáveis.

### Skill 05 — Bonus Delivery
**Trigger:** "bonus delivery"
**O que faz:**
- Lê `04-offer.json.bonuses[]`
- Pra cada bonus, gera pipeline de entrega conforme `delivery_trigger` (post-purchase, on-signup, day-7, on-first-reorder)
- Templates por tipo: digital guide → PDF, community access → Circle invite, video series → Wistia hosted, etc.

**Output:** `05-bonus-delivery/[bonus-id]/` com assets + instruções de upload.

### Skill 14 — Content Recycler (anteriormente 17)
**Trigger:** "content recycler" ou "recycle [creative-id]" ou "recycle winner"
**O que faz:**
- Lê 1 criativo winner (input direto OU detecta automático via `11-analysis/latest.json.winners[]`)
- Extrai essência (big idea, hook, mechanism, avatar, voice) pra `essence.json`
- Gera 9 derivadas em formatos diferentes: advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad
- Compliance pre-flight em cada derivada (severity ≥ high dispara auto-rewrite)

**Output:** `/workspace/[produto]/14-recycled/[source-id]/` com 9 `.md` + 9 `.html` companion + `README.md/.html` + `essence.json` + `compliance-log.json`.

---

## 4. Sistema de libs

Bibliotecas reutilizáveis chamadas pelas skills. Ficam em `.claude/lib/`.

### compliance-preflight
**Função:** detecta palavras ad-flag (Botox, weight loss, cure, treat, anti-aging, before & after, guaranteed, etc.) que disparam disapproval automático no Meta/TikTok.
**Entry point:** `run.py --input <texto> --config red_flags.json --schema output-schema.json`
**Output:** JSON com `severity: critical | high | medium | low` + `rewrite_suggestion`.
**Usado por:** skills 06, 07b, 07c, 08, 14 (e por dentro do 10 implicitamente via gate de 09).

### content-recycler
**Função:** engine prompt-driven da skill 14.
**Arquivos:** `recycler.md` (prompt principal) + `formats.json` (specs dos 9 formatos).
**Como customizar:** adicionar formato novo = editar `formats.json` com `id`, `name`, `output_file`, `length_words`, `structure`, `tone`, `compliance_notes`. Próxima execução pega automaticamente.

### creative-dna
**Função:** registry de DNA aprendido entre produtos. Cada vez que skill 08 gera conceitos, extrai padrões (winning hook archetypes, structural patterns, voice signatures) e salva. Próxima execução em outro produto consulta o registry e adapta.
**Por que importa:** é o cross-product learning. Membros que rodam vários produtos têm vantagem cumulativa.
**Arquivos:** `registry.py` (CRUD), `archetypes.json` (catálogo).

### hook-taxonomy
**Função:** taxonomia de hooks usada pela skill 08 (categorização Problema/Resultado/Curiosidade/Prova social).
**Arquivos:** `archetypes.json` (catálogo). README cita `patterns.md` que ainda não existe — documentação pendente, não bloqueia uso.

### prompt-directors
**Função:** directors de prompt pra ferramentas externas de geração de imagem/vídeo.
**Arquivos:**
- `marketing-studio-director.md` — Higgsfield Marketing Studio (UGC, Tutorial, Unboxing, Hyper Motion, Product Review, TV Spot, Wild Card, Virtual Try On)
- (outros directors conforme necessário)
**Usado por:** skill 08 ETAPA 5.7.

### trendtrack-integration (opcional)
**Função:** integração read-only com TrendTrack MCP (`https://api.trendtrack.io/v1/mcp`). 11 tools cobrindo product discovery, competitor briefing, ad scanning, email pattern analysis e monitoramento.
**Arquivo:** `README.md` (mapping skill→tool, detection runtime, custo/créditos, fallback).
**Detecção:** runtime — skill verifica se há tools com prefixo `mcp__trendtrack__` na sessão. Se sim, usa como fonte primária. Se não, segue ETAPA tradicional (web fetch + Meta Ad Library + scraping).
**Usado por (opcional):** skills 01 (product research), 03 (competitor analysis), 08 (creatives), 11 (ad analysis), 13 (retention).
**Por que importa:** elimina cloaker fallbacks da skill 03, dá hooks reais pra Hooks Bank da skill 08, viabiliza loop de monitoramento contínuo via `daily_radar`. Aura funciona 100% sem ela — integração é puro upside.

### automations/ (Meta Ads + Shopify, cascade resiliente)
**Não é uma lib em `.claude/lib/`** — vive em `.claude/automations/` (setup-mcps.md + 6 receitas em `recipes/`). Mas funciona como integration layer: skills delegam aqui.

**Stack Meta Ads (cascade automático):**
1. **MCP oficial da Meta** — `mcp.facebook.com/ads` (open beta desde 2026-04-29). Tools com prefixo `mcp__meta__ads_*`. 29 tools: campaign create/manage, catalog (10 tools), insights, datasets (Pixel/CAPI quality), industry benchmarks, auction ranking, opportunity score, anomaly signal. OAuth via Business Suite — zero token manual.
2. **Pipeboard MCP** — `pipeboard-co/meta-ads-mcp` (3rd party). Tools com prefixo `mcp__meta-ads__*`. Long-lived token Meta Marketing API (60d). Fallback automático quando o oficial está disabled no rollout gradual da beta.
3. **Manual** — membro cola screenshot quando ambos MCPs falham.

**Receitas em `recipes/`:**
- `sync-campaign-from-meta-official.md` — pull completo via MCP oficial (preferencial); inclui dataset health + industry benchmarks
- `sync-campaign-from-meta.md` — fallback Pipeboard
- `pause-ad-set.md` — cascade oficial→Pipeboard pra pausar ad set (PGS guard)
- `upload-creative-to-meta.md` — continua via Pipeboard (oficial não aceita arquivo local)
- `deploy-shopify-product.md`, `rotate-winning-creative.md`, `full-deploy.md`

**Setup:** documentado em `.claude/automations/setup-mcps.md`. Instala ambos os Meta MCPs em paralelo pra ter resiliência.

---

## 5. Sistema de rules

Diretrizes em `.claude/rules/` carregadas automaticamente pelo Claude Code conforme contexto. Cada rule tem escopo específico.

| Rule | Quando aplica |
|------|--------------|
| `pre-launch-gates.md` | NON-NEGOTIABLE. Define dois gates: ad-flag compliance (skills 06, 07b, 07c, 08, 10) e Promise↔Config (skills 07c, 10) |
| `shopify-theme-safety.md` | Toda operação Shopify CLI. Pull antes de edit, --nodelete, marker verification, smoke test pós-push |
| `iteration-driven-refinement.md` | Skills que geram asset (copy, briefing, página). Primeira versão é draft, max 3 iterações antes de escalate |
| `member-stage-awareness.md` | Toda skill. Detecta starter/validating/scaling pelo manifest e adapta tom + recomendações |
| `emergency-escape-paths.md` | Toda skill. ES1-ES7 cobrem situações de skill travada, workspace corrompido, compliance bloqueando, Shopify push rejeitado, Klaviyo cookie expirado, rate limit, conflito de edição |
| `troubleshooting-patterns.md` | Quando skill não entrega. Árvore de diagnóstico estruturada antes de "desistir" |
| `post-task-self-audit.md` | Toda skill peso médio/alto. 6 gates antes de declarar "completo" — cross-artifact consistency, erros factuais, gaps, qualidade, alinhamento de rules |
| `reverse-order-insertion.md` | Quando AI insere múltiplos elementos em arquivo (page.json sections, Liquid blocks). Inserir em ordem reversa pra line numbers não shiftarem |

**Rules são diretrizes, não código enforced.** O Claude lê e aplica. A camada de enforcement real são os hooks.

---

## 6. Sistema de hooks

Scripts em `.claude/hooks/` registrados em `.claude/settings.json`. Rodam em eventos específicos do Claude Code.

### post-start.sh
**Quando:** abertura de sessão Claude Code (1× por dia, com lock).
**O que faz:** adiciona alias `aura` no shell rc do membro pra ele poder digitar `aura` em qualquer terminal e cair no diretório certo.

### Hooks globais (vindos de `~/.claude/settings.json`, projeto-agnóstico)
- `enforce-git-push-authority.sh` — só @devops pode push
- `sql-governance.py` — bloqueia SQL perigoso
- `enforce-delegation.cjs` — orchestrators não podem executar
- `enforce-architecture-first.cjs` — docs antes de código protegido
- `enforce-story-gate.cjs` — story obrigatória antes de código
- `synapse-wrapper.cjs` — context injection no prompt do usuário

Esses hooks vêm do framework SINAPSE global (`~/.claude/`). Aura Engine herda eles mas não depende deles.

---

## 7. Sistema de templates

Em `.claude/templates/`.

### aura-report-template.html
Template HTML self-contained (CSS inline, sem server) usado por toda skill que gera companion `.html`. Tem componentes: `section-label`, `callout`, `note`, `opportunity`, `danger`, `table-wrap`, `quote`, `pill`, `winner`, `kpi-grid`. Responsivo mobile.

### aura-logo-snippet.html
Bloco SVG da logo Aura (6 linhas). **Obrigatório no topo de TODO `.html` gerado**, copiado literalmente. Proibido substituir por texto. Existe pra branding consistency.

### manifest-schema.json
JSON Schema (draft-07) pro `manifest.json` de cada produto. Tem `additionalProperties: true` — skills podem gravar campos extras sem violar schema. Os campos obrigatórios são `product_slug`, `product_name`, `created_at`, `updated_at`, `skills_completed`.

---

## 8. Workspace structure

Cada produto vive em `/workspace/[slug]/`. Estrutura típica após cadeia completa:

```
/workspace/produto-x/
├── manifest.json              ← estado central, lido e atualizado por toda skill
├── 01-product-research.md / .html
├── 02-market-research.md / .html / .json
├── 03-competitor-analysis.md / .html
├── 03-creative-patterns.json
├── 04-offer.md / .html / .json
├── 04-research-foundation.json
├── 06-copy.md / .html / .json
├── 07-page/
│   ├── 07-design-system.md
│   ├── 07-plan.md / .json
│   ├── 07-sections-report.md
│   └── 07-deploy-report.md / .json
├── 08-creatives.json
├── 08-creatives/
│   ├── briefing-c01.md / .html
│   ├── prompt-c01-image.txt
│   └── ... (1 set por conceito)
├── 10-ad-strategy.md / .html / .json
├── 11-analysis/
│   ├── 2026-04-15.json
│   ├── 2026-04-22.json
│   └── latest.json
├── 12-scale/
├── 09-consistency-audit.md / .html / .json
├── 13-retention/
│   ├── welcome-series.md / .html
│   ├── abandoned-cart.md / .html
│   └── ... (1 por fluxo)
├── 05-bonus-delivery/
│   └── [bonus-id]/
└── 14-recycled/
    └── [source-id]/
        ├── README.md / .html
        ├── essence.json
        ├── compliance-log.json
        ├── advertorial.md / .html
        ├── email-sequence.md / .html
        └── ... (9 formatos)
```

`/workspace/profile.md` (no nível do workspace, fora do produto) tem dados do membro: budget, ESP, ferramentas, mercado, idioma de copy.

---

## 9. Convenções operacionais

### Idioma e estilo (rule 0 do CLAUDE.md)
- Relatórios internos: português claro, sem jargão acadêmico, termos de marketing em inglês quando naturais (VOC, hook, CTA, ROAS)
- Copy pro consumidor final: inglês US (mercado padrão Aura)

### Dual output (.md + .html) — rule 6b
- `.md` é a fonte que a AI lê na próxima fase
- `.html` é a versão humana (browser)
- HTML usa o template `aura-report-template.html` + logo SVG no topo

### Logo SVG obrigatória
- Bloco SVG copiado literalmente de `aura-logo-snippet.html`
- Proibido substituir por texto "AURA" / "Aura Engine" / qualquer variação textual
- Sem fallback: se não copiar, parar e avisar

### Ícones SVG, nunca emojis em UI consumidor — rule 7
- PDPs, landings, checkouts: SVGs inline (Lucide, Heroicons, Phosphor, custom)
- Specs: 16-18px em listas, 20-24px em features, stroke 1.5-2px
- EXCEÇÃO: relatórios internos `.md`/`.html` em /workspace/ podem usar emojis pra escaneamento

### Copy rules (rule 8)
- **8a** — minimizar travessão (—). Em headlines, zero. Em copy longa, ≤2.
- **8b** — ad-flag word substitutions automáticas pra Meta/TikTok policy (Botox → "the appointment", Filler → "injectables", etc.)

---

## 10. Memória persistente — creative-dna registry

Cross-product learning. A skill 08 (creatives) salva DNA toda vez que executa: hook archetypes que funcionaram, voice signatures, structural patterns. Próxima execução em outro produto consulta esse registry e adapta sem reinventar.

**Como ler/escrever:** via `lib/creative-dna/registry.py`. Skill 08 chama em silent steps (ETAPA 7.4 carrega, ETAPA 7.6 escreve).

**O que NÃO entra no registry:** dados específicos do produto (nomes, claims, preços). Só padrões abstratos.

---

## 11. Como rodar uma sessão completa do zero

Ordem canônica pra um produto novo:

```
1. setup                        → cria workspace, profile, manifest
2. product research             → valida produto, define vertical
3. market research              → VOC, awareness, drivers (mais consultado)
4. competitor analysis          → 5-10 concorrentes, padrões, gaps
5. offer                        → mecanismo, pricing, stack, garantia
6. bonus delivery (asset prep)  → PDFs/emails/Circle invites dos bonuses
7. copy                         → copy completa pra todas sections
8. page                         → 07a (planning) → 07b (sections) → 07c (deploy)
9. creatives                    → 6-15 conceitos com briefings
10. consistency audit            → cross-phase drift check (gate)
11. ad strategy                 → estrutura de campanha, naming, PGS
   --- LAUNCH ---
12. ad analysis (após 3-7 dias) → 4Pi, diagnóstico, decisões
13. scale (após winners)        → vertical + horizontal
14. retention (≥50 compras)     → fluxos Klaviyo
15. content recycler (após winner consolidado) → 9 derivadas do criativo top
```

Cada skill faz pre-flight da anterior. Se artefato faltar, oferece fallback (rule `emergency-escape-paths.md` — ES1).

**Iteration loop normal:** depois de cada launch, ad analysis + iteração de creatives ou copy é o ciclo. Skill 09 (consistency audit) reroda antes de cada relaunch crítico.

---

## 12. Mudanças recentes (registro)

> Os números abaixo refletem a numeração das skills **na época de cada mudança**. Renumerações posteriores não modificam histórico.

| Data | Mudança |
|------|---------|
| 2026-04-30 | Skill 06 deprecated removida (era só redirecionamento) |
| 2026-04-30 | Skill 17 renomeada pra 14 (numeração contígua) |
| 2026-04-30 | Drift 04↔09 corrigido (`weighted_margin_per_order`, `target_cpa_primary_2x/3x` adicionados ao output do 04) |
| 2026-04-30 | Drift 04↔05 corrigido (`offer_stack` adicionado ao output do 04) |
| 2026-04-30 | Drift 08↔09 corrigido (skill 08 grava `08_campaign_name` no manifest) |
| 2026-04-30 | ETAPA 6 missing em skill 07 corrigida (LP Congruency tem header) |
| 2026-04-30 | Skill 11 vira hard gate em 06c, 08, 12 (lê `launch_recommendation`, aborta em BLOCK) |
| 2026-04-30 | Google Cache removido do fallback chain do skill 03 (descontinuado set/2024) |
| 2026-04-30 | URL Higgsfield hardcoded substituída por URL genérica em `prompt-directors/marketing-studio-director.md` |
| 2026-04-30 | Libs órfãs deletadas: `shocking-stats`, `whisper-transcribe`, `section-patterns` |
| 2026-04-30 | Skill 14 (ex-17) ganha companion `.html` obrigatório (rule 6b) |
| 2026-04-30 | CLAUDE.md atualizado com skill 14 na lista oficial |
| 2026-05-03 | Self-audit silencioso obrigatório no fim de toda skill (rule + regra 9 em CLAUDE.md) |
| 2026-05-03 | **Renumeração completa pra alinhar números com ordem de execução**: bonus-delivery 13→05, copy 05→06, page 06→07, creative 07→08, consistency-audit 11→09, ad-strategy 08→10, ad-analysis 09→11, scale 10→12, retention 12→13. Content-recycler permanece 14. Numbers daqui pra frente refletem ordem cronológica do workflow. |
| 2026-04-30 | TrendTrack MCP integration adicionada como lib opcional (`lib/trendtrack-integration/`). Skills 01, 03, 08, 11, 13 ganharam ETAPA 0.5 / bloco TrendTrack que detecta `mcp__trendtrack__*` tools em runtime e usa como fonte primária. Fallback silencioso pro método tradicional quando ausente. CLAUDE.md ganhou regra 10 sobre integrações MCP opcionais. |
| 2026-05-11 | Meta MCP oficial (`mcp.facebook.com/ads`, open beta desde 2026-04-29) integrado em cascade. Nova receita `sync-campaign-from-meta-official.md` usa as 29 tools nativas (incluindo industry benchmarks, dataset quality, auction ranking, opportunity score, anomaly signal que não existem no Pipeboard). Skill 11 ETAPA 1 vira cascade: oficial → Pipeboard → manual. `pause-ad-set.md` ganha cascade interno. `setup-mcps.md` documenta os dois caminhos. CLAUDE.md regra 10 expandida pra mencionar Meta MCP. |
