# Aura Engine — Visão Geral Completa

Tudo que existe no ecossistema Aura: o que cada peça faz, como se conectam, e como uma sessão flui do início ao fim.

**Versão:** setembro 2026
**Skills:** 26 (numeradas 00-20, incluindo a 01b opcional e o slot 07 expandido em 07a/07b/07c/07d — sub-cadeia storefront — + 07e agentic readiness)
**Plataforma:** Claude Code (CLI da Anthropic)
**Raiz de output:** `workspace/[product-slug]/`

---

## 1. O que é a Aura

A Aura é um sistema de duas partes pra construir e escalar marcas de ecommerce dentro do **Claude Code**, a CLI da Anthropic:

- **Base de Conhecimento Aura** — um servidor MCP remoto (ferramenta `search_knowledge`) que guarda os frameworks especialistas em que o raciocínio da Aura é construído (Schwartz, Hopkins, Hormozi, Cialdini, Sugarman, Ogilvy, Caples, mais metodologia original sobre construção de oferta, Meta Ads científico e produção de criativos). Conectada uma vez via Settings do Claude; consultada silenciosamente dentro de toda skill que precisa fundamentar uma decisão.
- **Aura Engine** — um projeto (clonado em `~/aura-engine`) contendo 26 skills, libs de suporte, rules, hooks e templates. Skills se ativam por contexto: o membro descreve o que precisa, a Aura identifica em qual fase está, e a skill apropriada roda.

**Princípio central:** cada fase produz artefatos versionados em `/workspace/[product-slug]/` que alimentam a próxima. Nada é jogado fora — a copy se apoia na pesquisa, os criativos se apoiam na copy, os ads se apoiam nos criativos, a retenção se apoia na venda.

**Filosofia de output:** todo arquivo `.md` que a Aura escreve tem um `.html` companion no mesmo diretório. O `.md` é a fonte que a AI lê na fase seguinte; o `.html` é a versão que o membro abre no browser pra ler com calma.

---

## 2. A Base de Conhecimento Aura (search_knowledge)

A Base de Conhecimento é a camada de expertise profunda que sustenta o raciocínio da Aura. Vive como um servidor MCP remoto, indexado e consultável por uma única chamada de tool.

### Como o membro conecta

- **Claude Code:** automático — o repo traz um `.mcp.json` que registra o servidor `aura`; na primeira abertura do Claude Code na pasta, o membro só aprova o aviso de novo servidor. A chave de acesso (obrigatória — está no guia `docs/aura-setup-pt.html`) entra via variável de ambiente `AURA_KEY` no `~/.zshrc`, antes de abrir o Claude Code.
- **Claude Desktop:** Settings → Integrations → Add Custom Integration → Nome *Aura* → URL `https://aura-mcp-production.up.railway.app/mcp?key=CHAVE` (chave no guia de setup) → Add (uma vez por dispositivo, permanente até o membro remover)

Instruções completas com screenshots ficam em `docs/aura-setup-pt.html`.

### O que tem dentro

A base agrega a literatura fundacional de direct-response e ecommerce mais metodologia original. Quando uma skill precisa fundamentar uma decisão, consulta com frases de intent específica. Exemplos por domínio:

| Domínio | Queries representativas |
|---|---|
| Pesquisa de produto | `product research criteria validation`, `market desires mass desire`, `market sophistication stages` |
| Pesquisa de mercado | `unified research document process`, `psychographic research drivers`, `voice of customer review mining`, `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware` |
| Análise de concorrente | `competitor research extracting claims`, `market sophistication saturation` |
| Construção de oferta | `unique mechanism UMP UMS theory`, `offer stack pricing guarantee`, `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice` |
| Copywriting | `headlines formulas process 100 lines`, `Schwartz lead desire identification belief dimension awareness lead selection`, `hero sections types selection`, `PDP structure reviews above fold how it works section ecommerce product detail page`, `CTA psychology call to action` |
| Produção de criativo | `ad angles concepts variations`, `ad formats roadmap creative`, `hooks video ads`, `funnel creative playbook` |
| Meta Ads | `scientific method meta ads control variable`, `one campaign method AndroMeta`, `4Pi analysis spend frequency CPM`, `budget scaling methods 5% rule`, `automations obrigatórias spend 5x em 24h pausar URL diferente do site desligar` (automação é só proteção — regra com condição de performance é impossível em campanha com CBO, o Meta recusa; cânone ad-taxonomy §6) |
| Escala | `scaling strategy vertical horizontal`, `creative diversity scaling mechanism`, `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo` |
| Retenção | `email lifecycle welcome abandoned cart post-purchase winback`, `30-60-90 day LTV email SMS flow second purchase window replenishment` |
| Reciclagem de conteúdo | Nenhuma das duas trilhas da skill 14 vem da base: a Trilha 1 (amplificação) sai do cânone `.claude/lib/ad-taxonomy/README.md` (§2 classes, §5 escala, §7 Sniper) e a estrutura "1 criativo → 9 formatos" da Trilha 2 sai da lib `.claude/lib/content-recycler/` (formats.json). Na base a skill 14 puxa só frameworks de copy nomeados, ex: `Caples four U's hierarchy unique useful urgent ultra-specific headlines`, `gap theory of curiosity hooks counterintuitive open loop slippery slope` |

Toda busca roda com `deep=true` pra resultados completos. Múltiplas buscas por tópico são normais.

### Como se comporta dentro das skills

- **Sempre consultada, nunca nomeada.** Skills consultam a base sempre que precisam fundamentar uma recomendação, mas nunca avisam ao membro que estão buscando, nunca citam a fonte e nunca citam o material de curso por trás.
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
│   ├── skills/            ← skills 00-20, com sub-cadeia storefront 07a/07b/07c/07d + 07e (agentic readiness)
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
        └── 01..20         ← artefatos versionados produzidos por cada skill
```

A Base de Conhecimento Aura **não** está nesta árvore — é um servidor MCP remoto conectado separadamente. Engine e Base de Conhecimento são independentes.

---

## 4. As skills (em detalhe)

Cada skill é um arquivo `.md` com frontmatter (nome + descrição) e corpo estruturado em ETAPAs numeradas. Skills estão listadas abaixo em ordem numérica (o número é o ID fixo de cada skill), com três exceções: a 07e aparece depois da 08 porque é ali que ela roda, a 15 aparece logo depois da 04 porque é ali que ela é consultada pela primeira vez, e as engines laterais 16-20 aparecem juntas no fim, depois da 14, porque não são etapas da sequência. A ordem canônica exata de uma sessão está no §13. A fase de página virou a fase **storefront** (07a→07b→07c→07d), a bonus delivery (05) e a retention (13) rodam em duas fases (Fase A pré-launch, Fase B pós-launch), a agentic readiness (07e) roda depois dos criativos, antes do gate de launch (09), e a finance engine (15) não é etapa da sequência — é consulta lateral, acionada quando o membro precisa de uma decisão financeira. As engines 16 (creators), 17 (promo), 18 (time), 19 (ops) e 20 (marketplace) são laterais como a 15, cada uma com sua posição natural (detalhe no §13).

### Skill 00 — Setup
**Trigger:** `"setup"`
Configuração da primeira vez. Pergunta o idioma preferido pra relatórios internos (`pt-BR` ou `en`), cria `/workspace/` com o slug do produto, coleta contexto do membro (budget, ESP, tools, mercado) em `profile.md`, inicializa `manifest.json`.
**Output:** `manifest.json` + `profile.md`

### Skill 01 — Product Research
**Trigger:** `"product research"`
Valida produtos contra critérios (mass desire, mass urgency, mass uniqueness), aplica framework de sophistication de Schwartz (stages 1-5), recomenda go/no-go.
**Enrichment opcional:** quando MCP TrendTrack conectado, ETAPA 0.5 usa `find_winning_products` + `search_shops` + `creative_inspiration_pack`.
**Output:** `01-product-research/product-research.md` + `product-research.html`

### Skill 01b — Sourcing (opcional)
**Trigger:** `"sourcing"` / `"fornecedor"`
Fornecedor, cotação e logística do produto físico. Explica a operação em linguagem simples (MOQ, OEM/ODM, DDP, 3PL, FBA), analisa anúncios/fornecedores (começar vs escalar), monta a mensagem de cotação em inglês (7 blocos), oferece os agentes de sourcing parceiros da Aura (contato WhatsApp), compara cotações e entrega o custo real pro COGS da Skill 04. Roda em paralelo às fases 02-03.
**Output:** `sourcing/sourcing.md` + `sourcing.html` + `dados.json`

### Skill 02 — Market Research
**Trigger:** `"market research"`
Coleta de Voice of Customer em Reddit, fóruns, reviews, comentários do TikTok. Identifica frases exatas dos clientes, mapeia awareness distribution, drivers psicográficos, objeções ranqueadas.
**Por que importa:** o documento mais consultado do sistema.
**Output:** `02-market-research/market-research.md` + `market-research.html` + `dados.json`

### Skill 03 — Competitor Analysis
**Trigger:** `"competitor analysis"`
Identifica 5-10 concorrentes ativos via Meta Ad Library + Similarweb. Analisa PDPs. ETAPA 3C: análise profunda de criativos escalados com transcrição (Groq API ou Whisper local).
**Fallback chain pra páginas bloqueadas:** Wayback Machine → archive.today.
**Enrichment opcional:** quando MCP TrendTrack conectado, ETAPA 0.5 condensa ETAPAs 1-3 em `brief_competitor` + `search_shops` + `find_similar_shops` + `scan_ad`.
**Output:** `03-competitor-analysis/competitor-analysis.md` + `competitor-analysis.html` + `dados.json` + `creative-patterns.json` + `creatives-inbox/` (uploads do membro + transcripts Whisper)

### Skill 04 — Offer Builder
**Trigger:** `"offer"`
Constrói mecanismo único (UMP/UMS — a razão pela qual o produto resolve o problema, e por que a alternativa do mercado falha). ETAPA 2.5 obrigatória — Research Foundation. Pricing triangulado, bonus stack, garantia, unit economics, 12 sanity checks (4 deles bloqueiam o save).
**Economia unitária pelo cânone `.claude/lib/unit-economics/README.md`:** stack de custos variáveis item a item (nunca agregado), margem de contribuição rotulada corretamente (nunca "Lucro" sobre um número que não subtraiu os fixos), CAC ≠ CPA e o piso de CAC (US$ 15-25) como gate.
**Outputs críticos pras skills downstream:**
- `bonuses[]` array → lido pela skill 05
- `offer_stack` string → lido pela skill 06
- `unit_economics.weighted_margin_per_order` (breakeven CPA) + `target_cpa_primary_2x/3x` (target CPA — o divisor da capacidade de teste) → lidos pelas skills 10, 11 e 12
- `budget_viability.fixed_costs_monthly` → lido pela 11 antes de qualquer recomendação de cortar spend

**Output:** `04-offer-builder/offer-builder.md` + `offer-builder.html` + `dados.json` + `research-foundation.json`

### Skill 15 — Finance Engine (consulta lateral, não é etapa da sequência)
**Trigger:** `"finance"` / `"finanças"` / `"projeção"` / `"cohort"` / `"fluxo de caixa"` / `"quanto posso gastar em ads"` / `"payback"` / `"runway"`
Dona do modelo financeiro completo declarado no cânone `.claude/lib/unit-economics/README.md` §5 (4 alavancas, cohorts, ciclo de caixa). **Não é fase do pipeline** — roda quando o membro precisa de uma decisão financeira, tipicamente logo depois da 04 e depois a cada mês fechado. Recorrente por natureza: banking sheet semanal, calibragem de cohort mensal, revisão de LTV semestral.
**Dois modos, decididos pelos dados — sem pergunta extra:**
- **Modo A — Planejar** (nenhum mês fechado com ad spend *e* clientes novos do Shopify): monthly model linha a linha com o custo fixo dentro, margem de contribuição e ponto de cobertura do fixo, `gross_margin_needed_to_exist` (o lucro bruto que a operação precisa gerar todo mês só pra existir), piso de CAC, necessidade de caixa pra 90 dias, runway e benchmarks DTC.
- **Modo B — Medir** (≥1 mês fechado): as 4 alavancas (AOV, CAC, ad spend, % de recorrentes) simuladas uma por vez e ranqueadas, cohorts de 12 meses com decay factor e LTV medido, payback de 90 dias e first-order profitability, taxa de aumento do CAC e teto de escala, ciclo de conversão de caixa (o stack de float ≈ 105 dias) e banking sheet semanal. Com 1-2 meses fechados o cohort roda **não calibrado** (payback modelado com 30 dias de folga); com 3+ ele estabiliza.

**A ETAPA 5 é a razão principal de a skill existir:** ela transforma a espiral do ROAS (cânone §4) em número e publica `roas_spiral.breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed` e `cut_spend_recommendation_allowed`. Com os fixos desconhecidos, `cut_spend_recommendation_allowed` é `false` e a recomendação vira pergunta, não instrução.
**As regras que não se negociam:** nunca chamar de "lucro" um número que não subtraiu custo fixo (`operating_income` é `null` enquanto os fixos forem `null`); CAC vem do Shopify (`new customer = TRUE`), nunca do CPA de plataforma; e **três campos nunca se estima** — custo fixo mensal, CAC real e contagem de clientes novos. Faltando qualquer um, o campo fica `null`, entra em `pending_inputs[]` e o bloco derivado dele fica marcado como não calculável.
**Contrato de leitura (aditivo — sem o arquivo, cada skill mantém o comportamento atual):** a **11** lê o breakeven com fixo e a permissão de corte; a **12** lê caixa, float, runway, fixos e teto de escala; a **04** fecha `budget_viability.result_after_fixed_monthly`; a **13** mira o mês real de cruzamento do cohort e o pico de churn; a **10** checa o CPA-alvo contra o piso físico de CAC.
**Output:** `15-finance-engine/finance-engine.md` + `finance-engine.html` + `dados.json` + `banking-sheet.csv` (só no Modo B) + `manifest.fixed_costs_monthly` e bloco `manifest.finance`

### Skill 05 — Bonus Delivery (DUAS fases: A pré-launch, B pós-launch)
**Trigger:** `"bonus delivery"` / `"bônus"`
Geração do asset de bônus de ecom + delivery. A DEFINIÇÃO do bônus continua na skill 04; a 05 gera o ASSET (PDF/e-book/checklist) e rastreia access rate. Tipos primários de ecom: gift-with-purchase (GWP, threshold de cart subtotal vindo do AOV, take-rate como KPI), free e-book/guide toward dream outcome, free complementary SKU, free gift wrapping (Q4). A entrega do email integra com a skill 13 (via `delivery_trigger`); a config de GWP integra com a 07d-checkout-aov (é config de loja). **Fase A (pré-launch, logo após a 07d, antes da retenção Fase A — só se a oferta tem bônus):** gerar assets + configurar GWP/entrega — todo bônus prometido na PDP precisa existir antes do primeiro ad (a 09 verifica no gate). **Fase B (pós-launch, junto da Fase B da 13):** tracking de take-rate/access rate.
**Output:** `05-bonus-delivery/bonus-delivery.md` + `bonus-delivery.html` + `dados.json` (log de entrega) + `bonuses/[bonus-id]/`

### Skill 06 — Copy Engine
**Trigger:** `"copy"`
Headlines ("Process of 100" de Caples). Lead types por awareness stage. Hero sections, bullets, social proof, FAQ, urgency, email hooks.
**ETAPA 2.5 obrigatória — Swipe Modeling:** antes de escrever, a skill escolhe **1 espécime primário** (opcionalmente 1 secundário) no catálogo `.claude/lib/swipe-models/specimens.json` cruzando `page_type` × awareness × sophistication × vertical, puxa a anatomia da peça na base pela `best_query` do espécime, e monta o `specimen_block_map` — a sequência de blocos que a copy vai seguir. Regra inegociável: modela-se **estrutura e mecânica, nunca conteúdo** (copiar frase, claim ou nome de mecanismo é plágio e, no vertical de suplementos, risco de compliance).
**Revisão:** 7 sweeps Aura (1-7) + **sweep 8** (Compliance Pre-flight, gate de bloqueio, fora da contagem dos 7) + **sweep 9** (markup audit — auditoria estrutural em 5 camadas a partir do nó `auditoria` do mesmo JSON: estrutura + 4 U's, 4 emoções, lead de 4 passos, psicologia, oferta/preço, com o loop `Objection → Claim → Proof → Benefit` rastreado parágrafo a parágrafo e a folha de 12 defeitos. Headline que reprova em 3 dos 4 U's e falha em ideal prospect ou big promise = reescrever o lead antes de auditar o corpo).
**Output:** `06-copy-engine/copy-engine.md` + `copy-engine.html` + `dados.json` + `compliance-log.json`

### Skill 07 — Storefront (cadeia 07a → 07b → 07c → 07d)
**Trigger:** `"page"` / `"tracking"` / `"checkout"`
A fase storefront monta a loja inteira: página, deploy, tracking e AOV. Arquitetura **HTML-first determinística** — o design nasce in-session, vira a fonte única de verdade visual, e a conversão pra Liquid é por código, não por reasoning. Mata o drift entre o que o membro aprova e o que vai pro ar.
- **07a — Page Design:** PLAN adaptativo de sections (page_type detectado primariamente pelo awareness_level de Schwartz) + brand signals + design HTML-first via a skill nativa `frontend-design` (gera a página inteira como HTML+CSS self-contained com a copy real já inserida). O membro aprova esse HTML ANTES de qualquer Liquid existir. **Output:** `page-plan.json` (com bloco `strategy`), `design-system.md/html`, `design/page.html` (aprovado), `design-tokens.json`, `design-signals.json`
- **07b — Page Build:** compile determinístico HTML→Liquid via `liquid-converter.py` (conversor canônico), populate `templates/page.[produto].json` com blocks/block_order/settings preenchidos com a copy real, GATEs de compliance + promise↔config, deploy seguro (duplicate → pull --nodelete → cp → push --allow-live --nodelete) + marker verification + smoke test
- **07c — Tracking Setup:** Meta Pixel + Conversions API (CAPI), valida EMQ ≥ 6/10 (Event Match Quality, escala 0-10 do Events Manager), escolhe o analytics stack por stage (Meta App / Wetracked / Triple Whale / Aimerce). Destrava os pré-flights de tracking das skills 08 e 10. **Output:** `07c-tracking-setup/tracking-setup.md/.html` + `dados.json` + estado no manifest (bloco `tracking`: `tracking_ready`, `analytics_stack`)
- **07d — Checkout AOV:** post-purchase upsell (one-click), cart bump, bundle/quantity-break, free-shipping threshold, checkout trust. Consome os bumps/upsells já definidos no `04-offer-builder/dados.json`. Caminho real Shopify: Functions (cart transform / discount), post-purchase extension (Checkout UI) ou apps equivalentes. **Output:** `07d-checkout-aov/checkout-aov.md/.html` + `dados.json` + `manifest.aov_baseline` (quando a config foi aplicada na loja)

### Skill 08 — Creative Engine
**Trigger:** `"creatives"`
Pipeline completo de briefing. Começa perguntando a **rota de produção** (A: gerar com IA · B: modelar concorrente e montar clipes · C: mix) e gera conceitos a partir das 3 verticais de pesquisa (competitiva, consumidor, interna). Cada conceito sai como um **pack 3-2-2** (3 criativos + 2 primary texts + 2 headlines) e ocupa 1 ad set próprio na estrutura da 10.
**O tamanho do batch vem da capacidade de teste, não do stage do membro** — `max_assets = budget diário ÷ target CPA` (cânone `.claude/lib/ad-taxonomy/README.md` §1, lido de `10-ad-strategy/dados.json.test_capacity` quando existe). Cada conceito declara o método de teste do §7 (Marksman = 3 ângulos distintos dentro do pack; Sniper = 1 ângulo em 3 execuções; toda iteração é Sniper), o **ângulo como frase de razão de compra** (a embalagem fica separada no `concept_type`) e a zona emocional em Valence × Intensity.
ETAPAs: detecção de material, ideação nas 3 verticais, regras estruturais, briefings com script segundo a segundo, entregáveis ramificados (prompts de IA por clipe na rota A / EDL de montagem na rota B), LP congruency mapping, hooks bank, DNA registry load/extract, compliance pre-flight + gate de disclosure "AI Info" (humano fotorrealista gerado por AI exige o label da Meta no upload).
**Enrichment opcional:** quando MCP TrendTrack conectado, Hooks Bank ganha archetypes vencedores reais; quando o MCP da Higgsfield está conectado, a skill pode renderizar os vídeos in-session (sempre confirmando antes de gastar créditos).
**Output:** `08-creative-engine/creative-engine.md` + `creative-engine.html` + `dados.json` + 1 briefing por conceito (`concept-NN.md/html`) + `prompts/` (rota A) ou `concept-NN-edl.md` (rota B) + `hooks-bank.md`

### Skill 07e — Agentic Readiness (AEO / AI visibility)
**Trigger:** `"agentic readiness"` / `"aeo"` / `"ai visibility"`
Checklist de descoberta por agentes de compra com AI (ChatGPT, Perplexity, Google AI Mode, Copilot). Roda depois do deploy (07b) — na prática, depois dos criativos — e antes do gate de launch (09). Verifica na loja VIVA: canal Agentic Storefronts + 3 policies, Knowledge Base app populado, dados estruturados da PDP (GTIN, ratings, FAQ/shipping/return — audita o que a camada GEO da 07b injetou), bloco de specs legível por agente, robots.txt liberando OAI-SearchBot/ChatGPT-User/PerplexityBot/ClaudeBot/Google-Extended, `/llms.txt` (nativo ou override), registro no Perplexity Merchant Program e qualidade do feed do Merchant Center. Fecha com score de AI visibility. **Não consulta a base Aura** (não há domínio de AEO lá — fontes são docs oficiais + verificação direta). Checklist barato de 1×, vale pra todo stage.
**Output:** `07e-agentic-readiness/agentic-readiness.md` + `agentic-readiness.html` + `dados.json` + bloco `agentic` no manifest (lido pela 09 como contexto e pela 12 como fonte incremental de tráfego)

### Skill 09 — Consistency Audit
**Trigger:** `"consistency audit"` / `"audit"`
Cross-phase drift detection: mecanismo, awareness stage, VOC, oferta concordam entre todos os artefatos (skills 02 → 03 → 04 → 06 → 07 → 08). VOC traceability + promise↔config. Roda ANTES do launch, conferindo a página já no ar + criativos + oferta.
**Vira gate de launch:** em `BLOCK`, a 10 aborta (override só via `compliance_override` no manifest); a 13 bloqueia por default mas oferece prosseguir com `skipped_preflight` reconhecido (filosofia never-stuck). A página existir (07b) não gasta dinheiro; os ads (10) sim — por isso o gate fica antes da 10, não do deploy da página.
**Output:** `09-consistency-audit/consistency-audit.md` + `consistency-audit.html` + `dados.json` com `launch_recommendation`

### Skill 10 — Ad Strategy
**Trigger:** `"ad strategy"`
Pre-flight pra Pixel/CAPI/produto live/criativos prontos. One Campaign Method na forma vigente: **1 campanha com CBO → N ad sets broad/Advantage+ (1 ad set = 1 conceito) → 3 criativos + 2 primary texts + 2 headlines cada**, criada em PAUSED via Meta MCP (o membro revisa e ativa).
**Quantos ad sets sobem é conta, não preferência** (cânone `.claude/lib/ad-taxonomy/README.md` §1): `max_assets = budget diário ÷ target CPA` e `max_adsets = budget diário ÷ (3 × target CPA)`, com piso operacional de US$ 100-150/dia, teto de ~3× target CPA por ad set e máximo de 5 ad sets de teste abaixo de US$ 1k/dia. O batch da 08 pode trazer mais conceitos do que o budget consegue ler — o excedente vai pra fila do batch seguinte, nunca dilui o teste.
Método de teste Marksman ou Sniper (§7 — Marksman acontece DENTRO de um ad set, com 3 ângulos no mesmo pack, não entre ad sets). Naming convention, UTM schema, warmup de conta nova, cadência quarta→domingo, 3 dias sem mexer.
**Proteções (§6):** Automated Rule com condição de performance é recusada pelo Meta em campanha com CBO — não existe PGS aqui. O que entra: `ad set spending limit → daily maximum` (~3× target CPA) criado junto do ad set, mais as **duas automações de proteção obrigatórias** — (a) spend 5× em 24h → pausar; (b) URL de destino ≠ domínio da loja → desligar — que **nascem desativadas** pro membro ativar. Kill e escala continuam sendo leitura das skills 11 e 12, nunca regra automática.
Confirma o analytics stack gravado pela 07c em `manifest.tracking` (a escolha da stack é da 07c, não desta).
**GATE skill 09** roda no pre-flight.
**Output:** `10-ad-strategy/ad-strategy.md` + `ad-strategy.html` + `dados.json` (com `test_capacity` inteiro e auditável, `ad_sets[]` e `protections`) + manifest `10_campaign_name` / `10_campaign_id` / `10_ad_set_ids` (um por conceito — a 11 puxa insights por ID)

### Skill 11 — Ad Analysis
**Trigger:** `"ad analysis"`
Lê a estrutura da 10 em DOIS níveis: por **conceito** (o ad set — onde o CBO concentra gasto é o sinal) e por **criativo** (o ad). 4Pi (Spend, Frequency, CPM, Cost per Result). 19-Point Loser Diagnostic.
**Classifica cada criativo nas 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2** — `loser` · `kpi_winner` · `spend_winner` · `breakthrough`. Só `breakthrough` (KPI do AD melhor que o KPI da CAMPANHA **e** puxando spend) libera escala e reciclagem; `kpi_winner` bate o KPI sem puxar spend e é tratado como **loser para decisão**. Réguas de kill do §3 (conta madura: ad set após 7 dias sem spend e sem KPI; conta nova: 8× target CPA sem purchase; ad novo overspendando: 24-48h de carência) e Hook rate / Hold rate do §4 pra dizer ONDE o criativo falhou.
**Gate de unit economics:** nenhuma recomendação de cortar spend por queda de ROAS sai sem aplicar `.claude/lib/unit-economics/README.md` §4 com os custos fixos na mesa — sem eles, a saída é a pergunta ("quanto você tem de custo fixo por mês?"), não a instrução de corte.
**Enrichment opcional:** quando MCP TrendTrack conectado, `scan_ad` faz benchmark dos breakthroughs e `daily_radar` monitora concorrentes.
**Output:** `11-ad-analysis/ad-analysis.md` + `ad-analysis.html` + `dados.json` (última análise) + `[YYYYMMDD]-analysis.md/html` (histórico)

### Skill 12 — Scale Engine
**Trigger:** `"scale"`
Escala vertical governada pelo **Scaling Protocol** do cânone `.claude/lib/ad-taxonomy/README.md` §5 — a espinha única de toda subida e descida: dois gates cumulativos pra subir (48-72h acima do target **e** ≥60% das purchases em 7-day click), passo de **+20%** repetível a cada 24h enquanto os gates seguram, **−20%** abaixo do breakeven, e a **regra de reset da meia-noite** (o budget do dia seguinte é ~50% do que foi REALMENTE gasto, nunca do nominal — sem isso o Meta faz pacing pro nominal inteiro e a escala vira queima de caixa).
As 3 escolas de gestores de tráfego (A cost-cap duplication + surf, B bid cap, C budget-doubling) são **variantes de intensidade dentro do protocolo**, recomendadas por member-stage — nenhuma dispensa os gates.
Escala só abre com **breakthrough** (§2): `kpi_winner` não conta. A promoção é o **ABO paralelo** — cada breakthrough ganha 1 ad set próprio em campanha ABO a ~10% do budget diário da campanha principal, mantendo o ad original rodando no CBO; o **champions ad set foi aposentado** em favor dessa rota (`champions[]` permanece só como campo de compatibilidade).
Horizontal scaling por diversidade de criativo (+ referral de agentes de AI como fonte incremental quando a 07e marcou a loja como pronta). Graduação pra Advantage+ Sales acima de US$ 1k/dia sustentado. Cash flow e projeções 30/60/90. PSM como diagnóstico (lê `manifest.psm_real`, não recomputa). Antes de qualquer corte de spend por queda de ROAS, aplica `.claude/lib/unit-economics/README.md` §4. Fecha ciclo de volta pra 08 quando o gargalo é criativo.
**Output:** `12-scale-engine/scale-engine.md` + `scale-engine.html` + `dados.json` + `scale-directives.md`

### Skill 13 — Retention Engine (DUAS fases: A pré-launch, B pós-launch)
**Trigger:** `"retention"` / `"email flows"` / `"klaviyo"`
ESP identificado. Fluxos base: welcome series, abandoned cart, post-purchase, win-back, replenishment. **Fase A (pré-launch, depois da 07d/05 e antes dos criativos):** flows de recuperação — abandoned cart + post-purchase. É infraestrutura de cash flow do launch, não campanha de email: operador de elite nunca liga tráfego pago sem abandoned cart flow (a receita mais barata que existe, custa zero no free tier do ESP). **Fase B (pós-launch, ≥50 compras):** win-back, replenishment e segmentação. Campanhas/newsletters continuam sempre pós-launch.
**GATE skill 09** no pre-flight da Fase B (a Fase A roda antes de a 09 existir).
**Setup pipeline:** Klaviyo MCP oficial (`mcp__klaviyo__`) cria os flows direto, SEMPRE em draft → fallback assets HTML + setup-guide (único caminho pra Omnisend/MailerLite/Shopify Email). Ver §12.4.
**Enrichment opcional:** `analyze_shop_emails` (TrendTrack) calibra timing dos fluxos.
**Output:** `13-retention-engine/retention-engine.md` + `retention-engine.html` + `dados.json` + `[fluxo]/`

### Skill 14 — Content Recycler
**Trigger:** `"content recycler"` / `"recycle [id]"` / `"recycle breakthrough"`
**O gatilho é `breakthrough`, não "winner" genérico.** Lê a classificação que a skill 11 gravou (`breakthroughs[]`, espelhado em `manifest.breakthroughs[]`) e nunca a recomputa. `kpi_winner` **não entra** — o cânone `.claude/lib/ad-taxonomy/README.md` §2 o trata como loser para decisão (bateu o KPI com pouco spend, não provou nada em escala). `spend_winner` entra pela porta estreita: só o Movimento 1 (iteração), porque o cânone manda iterar, não escalar.
Extrai a essência e — acima dela — o **framework que viaja** (`framework_template` + `psychological_mechanism`): o padrão por trás do script, não o script.
**Trilha 1 — Amplificação (default, roda primeiro):** 6 movimentos pra extrair mais spend lucrativo do que já provou escalar — (1) iterar pelos 4 elementos (ângulo, mecanismo, autoridade, avatar), (2) portar o ângulo pra outros formatos, (3) LP/prelander dedicada, (4) portar pra Axon/AppLovin e TikTok (9:16 + end card, régua de US$ 250-1.000/dia por 60-90 dias), (5) duplicar em ad set ABO próprio a ~10% do budget da campanha principal, (6) devolver como creator report. A skill **especifica**; quem executa é a 08 (criativo), a 07a/06 (página e copy) e a 12 (escala).
**Trilha 2 — Derivadas de formato (sob pedido):** as 9 peças de canal próprio (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad), agora enquadradas como jogada de **marca e LTV**, não de performance — quem escala a conta é a Trilha 1. Engine e specs dos formatos vivem na lib `.claude/lib/content-recycler/` (`recycler.md` + `formats.json`).
**Output:** `14-content-recycler/content-recycler.md` + `content-recycler.html` (índice) + `[source-id]/` com `essence.json`, `amplification-plan.md/.html`, `creator-report.md/.html` e — se a Trilha 2 rodou — 9 `.md` + 9 `.html` + `compliance-log.json`

### Skill 16 — Creator Engine (consulta lateral, DUAS fases)
**Trigger:** `"creators"` / `"ugc"` / `"seeding"` / `"whitelisting"` / `"ambassador"`
A operação completa de conteúdo humano — content é o arquivo bruto, creative é o content editado, e sem abundância de conteúdo não há volume de teste. **Fase A — Content Engine (paralela à 08, pode começar antes do launch):** product seeding (enviar produto de graça em troca de conteúdo, em plataforma tipo Insense ou por outreach manual), casting com diversidade de creator amarrada aos sub-avatares da 02, framework de brief (nunca script fechado), B-roll de referência, follow-up e coleta, corte de cada vídeo em 3 hooks e o pipeline TikTok Shop como fábrica de volume. O objetivo da Fase A é encontrar **um brand ambassador**, não um winning ad de primeira (isso é bônus). **Fase B — Performance Program (SÓ depois de breakthrough confirmado pela 11):** o creator vencedor sobe de degrau — contrato recorrente, escada de embaixador com comissão em degraus, whitelisting (rodar ads do perfil do creator — só de quem já tem breakthrough com a marca, e só com os ads DELE), partnership ads, raw content campaign, creator farming e recrutamento pago de afiliados.
**Fronteiras:** a 08 continua dona do QUE dizer (conceitos, roteiros, produção IA); esta skill é dona de QUEM grava e da relação com quem grava. Não cria campanha nem mexe em budget (10/12), não classifica criativo (11), não recicla breakthrough (14). Material voltado ao creator (brief, mensagem, contrato, report) sai sempre em inglês US; números de remuneração nunca se inventam.
**Output:** `16-creator-engine/creator-engine.md` + `creator-engine.html` + `dados.json` + `briefs/` + `outreach/messages.md` + `contracts/` + `roster.csv` + bloco `creator` no manifest

### Skill 17 — Promo Engine (consulta lateral, sazonal)
**Trigger:** `"black friday"` / `"bfcm"` / `"promo"` / `"sale"` / `"q4"` / `"flash sale"`
Dona da janela promocional de ponta a ponta (Q4/BFCM, datas sazonais, flash sales) — dispara por época ou pedido, uma rodada por janela. Calendário da janela (começar cedo é a tese central), preparação (momentum do evergreen, decisão de lead-gen VIP pelo critério de returning customers, estoque via 01b, backups via 19), oferta da promo (hierarquia de ofertas BFCM, store credit, stacking e linguagem) e o **gate inegociável**: recalcular o breakeven ROAS e o CPA-alvo com a margem promocional ANTES de ligar qualquer campanha — sem os números recalculados, a skill PARA (é o erro nº 1 da temporada: oferta melhor com o mesmo ROAS-alvo de antes = mais receita, menos lucro).
**Execução:** Promo Campaign (Broad/WARM60/HOT90) em paralelo ao evergreen intocado, criativos "best ad + banner" via handoff pra 08, calendário de email/SMS que a 13 transforma em assets (flow nunca desliga durante campanha — se adapta), surf scaling e reset da meia-noite pelo cânone ad-taxonomy §5 (promo com data-fim é a exceção (a) do protocolo: entra direto no budget planejado), tudo logado no ad-log. **Aterrissagem:** regra de fim por horário, volta pro evergreen, leitura pós-promo com a 11 e a 15, cofre sazonal de winners pro revival no ano seguinte. Os números da janela vivem em `manifest.promo` e morrem com ela — nunca sobrescrevem o `target_cpa`/`breakeven_roas` do evergreen.
**Output:** `17-promo-engine/promo-engine.md` + `promo-engine.html` + `dados.json` + bloco `promo` no manifest

### Skill 18 — Team Engine (consulta lateral)
**Trigger:** `"contratar"` / `"time"` / `"equipe"` / `"hiring"` / `"quem contratar"`
Decide QUANDO contratar (pela restrição real do negócio, nunca por desespero — contrata-se porque QUER, nunca porque PRECISA; bad hire custa ~15× o salário anual da vaga), COMO contratar (scorecard antes da vaga, funil de 9 etapas, teste prático cronometrado, headhunting) e COMO rodar o time depois (onboarding de 8 semanas, KPIs por função com hit rate por editor, reviews com 9-box e PIP, incentivos, org design em engines e pods, frameworks de decisão DAI/RAPID/AAR). Desenhada pro membro em estágio scaling — pra starter/validating a resposta mais valiosa costuma ser **"ainda não — sua restrição hoje é X"**, entregue com o porquê e o sinal que reabre a conversa.
**Réguas:** nenhuma vaga sem gargalo nomeado; sucesso definido ANTES da vaga aberta (scorecard); salário, caixa e KPI real de pessoa nunca se inventam — quando a pergunta é "a folha cabe no caixa?", o número vem da 15 ou do membro. Creator ≠ funcionário: creator, afiliado e embaixador são território da 16. Consumidora do maior bloco órfão da base (o domínio `team-hiring-ops` inteiro do kb-index).
**Output:** `18-team-engine/team-engine.md` + `team-engine.html` + `dados.json` + bloco `team` no manifest

### Skill 19 — Ops Engine (consulta lateral — backups valem desde cedo)
**Trigger:** `"backup de conta"` / `"risco"` / `"constraint"` / `"operação"` / `"continuidade"` / `"exit"`
A skill que pergunta **"o que mata esse negócio nos próximos 12 meses?"** e arma a resposta antes. Três frentes: **(1) Constraint dos próximos 12 meses** — o ÚNICO gargalo que limita o ano (estoque, caixa, plataforma ou pessoa-chave) e as prioridades organizadas em torno de removê-lo; **(2) Continuidade** — checklist de backups com status confirmado pelo membro, nunca deduzido: conta e Business Manager reserva com campanhas pré-montadas desligadas, processadora de pagamento redundante, banco e domínio reserva, pre-order pronto pra ligar como válvula de estoque e caixa, risco de pessoa-chave medido em "dores de cabeça por dólar"; **(3) Negócio como ativo** — memos de decisão (WAFM: sem memo, não há reunião de decisão), teste de moat de produto e operação exit-ready (o que um comprador auditaria). A parte de backups vale DESDE O COMEÇO — logo depois da 00 e antes do primeiro ad, porque conta nova é a mais frágil da vida do negócio; o resto revisita por trimestre e antes de decisões grandes (escala agressiva, Q4).
**Fronteiras:** não monta a estrutura anti-ban (00), não calcula caixa/runway/float (15), não escolhe fornecedor nem define recompra (01b), não mexe em campanha (10/11/12) — audita o status e aponta.
**Output:** `19-ops-engine/ops-engine.md` + `ops-engine.html` + `dados.json` + `memos/` + bloco `ops` no manifest

### Skill 20 — Marketplace Engine (consulta lateral, estágio scaling)
**Trigger:** `"amazon"` / `"tiktok shop"` / `"marketplace"` / `"afiliados"` / `"expandir canal"`
Expansão de CANAL DE VENDA além do site próprio — decide quando (e se) a marca abre Amazon, TikTok Shop e programa de afiliados, e acompanha cada canal aberto. Roda um **GATE antes de qualquer tática**: Meta + site provados primeiro (breakthrough na 11, conta fechando na 15) e sinal de demanda transbordando (busca de marca subindo, cliente procurando a marca na Amazon, revendedor aparecendo na listagem) — porque canal novo não conserta oferta quebrada. Sem prova, a skill roda mesmo assim, mas o veredito só pode sair `not_yet` ou `blocked_pending_proof` — a resposta honesta "ainda não, e falta X" é output válido.
**Os canais:** Amazon como captura da demanda que o ad já criou (SEO da listagem, defesa de marca, lances baixos, preço riscado, custom link, TACOS); TikTok Shop como canal de venda operado por afiliados (comissão orgânica vs de ads, samples, GMV — o conteúdo em si é da 16); afiliados via tráfego pago (funil "apply to be brand ambassador", comissão decrescente por faixa) e clientes virando afiliados automaticamente. **Fronteiras:** recrutar/gerenciar creators é da 16; portar campanha paga pra AppLovin/Axon/TikTok Ads é da 14 (Movimento 4); a conta financeira por canal (margem com comissão e fee dentro) é da 15. Fees reais, busca de marca e GMV nunca se estimam — o membro cola o que vê no painel.
**Output:** `20-marketplace-engine/marketplace-engine.md` + `marketplace-engine.html` + `dados.json` + bloco `marketplace` no manifest

---

## 5. Sistema de libs

Libs reutilizáveis em `.claude/lib/`.

| Lib | Função | Usada por |
|---|---|---|
| **ad-taxonomy** | **Cânone de classificação e capacidade de teste.** Capacidade (`assets = budget diário ÷ target CPA`, piso US$ 100-150/dia, teto ~3× target CPA por ad set, máx. 5 ad sets abaixo de US$ 1k/dia) + estrutura CBO com 1 ad set = 1 conceito; as 4 classes de resultado (loser · KPI winner · spend winner · breakthrough); réguas de kill; Hook/Hold rate; Scaling Protocol + ABO paralelo (champions ad set aposentado); o que pode e não pode ser automatizado (condição de performance é recusada em CBO; 2 automações de proteção obrigatórias); métodos Marksman/Sniper/Shotgun e a distinção ângulo ≠ conceito. Nenhuma skill redefine isso localmente. | 08, 10, 11, 12, 14, 17 + rules `member-stage-awareness`/`troubleshooting-patterns` + receitas de automação |
| **unit-economics** | **Cânone de margem, CAC e decisão de spend.** Stack completo de custos variáveis e a regra de nomenclatura (nunca chamar de "Lucro" o que não subtraiu custos fixos); first order vs repeat order; CAC ≠ CPA (CAC vem do Shopify, `new customer = TRUE`); a **espiral do ROAS** — cortar spend por queda de ROAS pode aumentar o prejuízo, então nenhuma recomendação de corte sai sem os custos fixos na mesa. O §5 declara a **skill 15** como dona do modelo completo (4 alavancas, cohorts, ciclo de caixa). | 04, 11, 12, 15 |
| **ad-log** | **Cânone do registro de mudanças na conta.** `workspace/[produto]/ad-log.md`, **append-only**, uma linha por mudança executada (entidade, mudança com valores antes → depois, executor, motivo curto) — separa o que foi FEITO do que foi lido (as análises datadas da 11 registram leituras). Escrito no momento da execução; mudança executada e não logada é bug de processo. | Escrevem: 10, 12, 14, 17 + receitas de automação. Leem: 11 (SEMPRE, no início da análise) e 12 (antes de escalar — o gate de 24h entre degraus é verificado ali) |
| **swipe-models** | **Camada de modelagem por espécime.** `specimens.json` cataloga 12 espécimes estruturais de swipe files reais, cada um com seletor (`page_type` × awareness × sophistication × vertical), `best_query`, `regra_diagnostica`, `blocos_chave` e `base_empirica`. A skill 06 escolhe 1 primário (+1 secundário opcional) na ETAPA 2.5 e modela a ESTRUTURA — nunca o conteúdo. O nó `auditoria` vira o sweep 9 (markup audit: 4 U's, 4 emoções, lead de 4 passos, loop Objection→Claim→Proof→Benefit, folha de 12 defeitos). | 06 (dono), 04 e 11 (diagnóstico) |
| **compliance-preflight** | Detecta palavras ad-flag que disparam disapproval no Meta/TikTok. Output: JSON com `severity` + `rewrite_suggestion`. | 06, 07b, 08, 14 |
| **content-recycler** | Engine prompt-driven da **Trilha 2** da skill 14 (as 9 derivadas de formato). Arquivos: `recycler.md` + `formats.json`. A Trilha 1 (amplificação) não vem daqui — vem do cânone `ad-taxonomy`. | 14 |
| **creative-dna** | Cross-product DNA registry. Skill 08 salva padrões abstratos; próxima execução em outro produto carrega e adapta. | 08 |
| **design-presets** | Fonte única dos 8 presets de design da 07a (`presets.json` com os tokens completos e fixos). Existe pra que o mesmo preset devolva sempre os mesmos tokens — a skill lê o arquivo, nunca gera de cabeça. Caminho 4 (último) da cascade de brand signals. | 07a, 07b |
| **hook-taxonomy** | Taxonomia de hooks (Problema / Resultado / Curiosidade / Prova Social). | 08 |
| **kb-index** | Índice permanente das 1.309 entradas de frameworks nomeados da base, em 19 domínios (alguns sistemas aparecem em mais de um domínio quando servem a skills diferentes; `frameworks.json` + `README.md`), com a `best_query` exata de cada um. Skills puxam sistemas por nome via esse índice, nunca por query genérica — a fonte da verdade do tamanho de cada domínio é o próprio `frameworks.json`. | Todas as skills que consultam a base |
| **mcp-detect** | Fonte única de verdade dos prefixos de tool MCP detectáveis (`mcp__trendtrack__`, `mcp__meta__ads_*`, `mcp__meta-ads__`, `mcp__refero__`, `mcp__klaviyo__`, `mcp__shopify_dev__`, `mcp__stripe__`) + convenção de log `source`. | 07c, 10, 11, 13 + receitas de automação |
| **prompt-directors** | Directors de prompt pra ferramentas externas (Higgsfield Marketing Studio). | 08 (ETAPA 5.7) |
| **shopify-section-patterns** | 6 padrões de section Liquid endurecidos em produção (marquee infinito por JS em pixels, sticky add-to-cart com IntersectionObserver, gradiente de hero com easing, badges sobre imagem, drawer enriquecido via `::part`, fonte universal incluindo drawer) + o sistema de tokens de paleta em trios R,G,B. Formato: problema → solução → código de referência → armadilhas. | 07a (clone fiel), 07b |
| **theme-verify** | Gate de verificação da página no ar via Playwright: `verify_page.py` (overflow/seções/console, desktop+mobile), `font_census.py` (censo de fonte computada — declarar não é carregar), `motion_check.py` (continuidade de animação com `--throttle` 3G + cache frio, o cenário que revela bug de mobile real). Mesmo venv da web-fetch. | 07b (6.8/6.11) |
| **web-fetch** | Fetcher Playwright de navegador real (`fetch.py --mode text\|reddit\|reviews`) pro cascade resiliente da rule `resilient-fetch` (WebSearch → WebFetch → fetcher). Reddit via redlib, reviews com scroll de widgets lazy. | 00 (setup), 02, 03 + qualquer skill que minera web (rule `resilient-fetch`) |
| **workspace-index** | `build_index.py` regenera o painel `ABRIR-AQUI.html` do produto; `workspace-layout.md` define a estrutura canônica do workspace. | Todas as skills (no SALVAR) |
| **trendtrack-integration** (opcional) | Integração read-only com MCP TrendTrack. 11 tools. Detecção runtime: tools com prefixo `mcp__trendtrack__`. Aura funciona 100% sem ela. | 01, 03, 08, 11, 13 |
| **refero-integration** (opcional) | Integração com Refero Design MCP (`fidgetcoding-refero-mcp`). Catálogo curado de ~200 design systems premium (Cursor, Linear, Vercel, Notion, Stripe). 6 tools (`refero_search`, `refero_get`, `refero_similar`, `refero_list`, `refero_design_md`, `refero_refresh`). Fonte de brand signals (não decisão visual) que alimentam o `frontend-design`. Cascade na 07a ETAPA 2 (Brand Signals): Refero → screenshot→visão → `tools/design-clone/` → manual. | 07a (ETAPA 2) |
| **automations/ (Meta + Shopify)** | Vive em `.claude/automations/`. Cascade resiliente pra Meta Ads: **(1)** MCP oficial da Meta `mcp.facebook.com/ads` (open beta desde 2026-04-29, tools `mcp__meta__ads_*`, 29 tools); **(2)** MCP Pipeboard 3rd-party (tools `mcp__meta-ads__*`) como fallback automático; **(3)** paste manual. Receitas: `sync-campaign-from-meta.md` (única, com cascade interna oficial → Pipeboard → manual), `pause-ad-set.md`, `upload-creative-to-meta.md`, `creative-loop.md` (loop semi-autônomo: performance → DNA dos winners → variações novas → aprovação humana → upload), `full-deploy.md`, `deploy-shopify-product.md`, `create-fixed-bundles.md` (bundles fixos via Admin GraphQL `productBundleCreate`), `rotate-winning-creative.md` | 10, 11 |

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
| `report-only-results` | **NON-NEGOTIABLE.** Todo relatório salvo em `workspace/` (.md e .html). O doc contém só o resultado final — zero narração de processo/correções, zero descrição de ausências, zero referência à conversa, zero auto-referência da AI. Meta-informação vive no chat e no `dados.json`. |
| `resilient-fetch` | **NON-NEGOTIABLE.** Toda skill que busca dados na web. Cascade WebSearch → WebFetch → fetcher Playwright (`lib/web-fetch`); nunca inventar VOC/claim quando a fonte bloqueia. |
| `reverse-order-insertion` | Multi-insert safety: em arrays posicionais (`order[]`, `block_order`), inserir em ordem reversa; em edits por anchor de texto, planejar anchors únicos e disjuntos. |

**Rules são diretrizes, não código enforced.** O Claude lê e aplica. A camada real de enforcement são os hooks.

---

## 7. Sistema de hooks

Scripts em `.claude/hooks/` registrados em `.claude/settings.json`.

### post-start.sh
**Quando:** abertura de sessão Claude Code (1× por dia).
**O que faz:** adiciona o alias `aura` no shell rc do membro e instala o guard `.git/hooks/pre-commit` que bloqueia mecanicamente qualquer commit com arquivos de `workspace/` (camada 2 da separação framework vs workspace — CLAUDE.md rule 11e).

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

Cada fase mora numa subpasta própria `0X-<stem>/`. Dentro: `<stem>.html` (o que o membro abre), `<stem>.md` (o que a AI lê na fase seguinte), `dados.json` (dados estruturados) — o relatório humano leva o nome da pasta sem o prefixo numérico (ex.: `02-market-research/market-research.html`). Arquivos secundários mantêm nome descritivo dentro da pasta. Estrutura canônica completa (incl. compat com nomes legados) em `.claude/lib/workspace-index/workspace-layout.md`.

```
/workspace/produto-x/
├── ABRIR-AQUI.html                    ← PAINEL: porta de entrada do membro (gerado por build_index.py)
├── manifest.json                      ← estado central
├── brand.md  ·  brand/logo.svg        ← identidade (infra)
├── promise-check.json · compliance-warnings.json   ← infra compartilhada
├── creative-dna/                      ← infra compartilhada (08 + 11)
├── 01-product-research/   → product-research.md / .html
├── sourcing/              → sourcing.md / .html + dados.json   (01b, opcional — fornecedor, cotação, logística)
├── 02-market-research/    → market-research.md / .html + dados.json
├── 03-competitor-analysis/ → competitor-analysis.md / .html + dados.json + creative-patterns.json + creatives-inbox/
├── 04-offer-builder/      → offer-builder.md / .html + dados.json + research-foundation.json
├── 05-bonus-delivery/     → bonus-delivery.md / .html + dados.json + bonuses/[bonus-id]/   (2 fases: A pré-launch, B pós-launch)
├── 06-copy-engine/        → copy-engine.md / .html + dados.json + compliance-log.json
├── 07-page/               ← storefront (07a design + 07b build)
│   ├── design-system.md / .html · page-plan.json (bloco strategy)
│   ├── design/page.html               ← HTML aprovado (fonte única visual)
│   ├── design-tokens.json · design-signals.json · iterations-log.json
│   ├── page-report.html                   ← página final (relatório humano da fase)
│   └── deploy-report.json · staging/
├── 07c-tracking-setup/    → tracking-setup.md / .html + dados.json
├── 07d-checkout-aov/      → checkout-aov.md / .html + dados.json
├── 07e-agentic-readiness/ → agentic-readiness.md / .html + dados.json   (pós-deploy, pré-launch)
├── 08-creative-engine/    → creative-engine.md / .html + dados.json + concept-NN.md/html + hooks-bank + prompts/
├── 09-consistency-audit/  → consistency-audit.md / .html + dados.json
├── 10-ad-strategy/        → ad-strategy.md / .html + dados.json
├── 11-ad-analysis/        → ad-analysis.md / .html + dados.json + [YYYYMMDD]-analysis.md/html
├── 12-scale-engine/       → scale-engine.md / .html + dados.json + scale-directives.md
├── 13-retention-engine/   → retention-engine.md / .html + dados.json + [fluxo]/   (2 fases: A pré-launch, B pós-launch)
├── 14-content-recycler/   → content-recycler.md / .html (índice) + [source-id]/   (só depois de um breakthrough)
├── 15-finance-engine/     → finance-engine.md / .html + dados.json + banking-sheet.csv   (consulta lateral; o .csv só no Modo B)
├── 16-creator-engine/     → creator-engine.md / .html + dados.json + briefs/ + outreach/ + contracts/ + roster.csv   (lateral, 2 fases: A seeding/conteúdo, B performance)
├── 17-promo-engine/       → promo-engine.md / .html + dados.json   (lateral/sazonal — uma rodada por janela)
├── 18-team-engine/        → team-engine.md / .html + dados.json   (lateral — org, vagas, pipeline de candidatos)
├── 19-ops-engine/         → ops-engine.md / .html + dados.json + memos/   (lateral — backups valem desde o começo)
├── 20-marketplace-engine/ → marketplace-engine.md / .html + dados.json   (lateral — canais de venda além do site)
└── ad-log.md              ← registro append-only de toda mudança executada na conta (cânone ad-log; escrito por 10/12/14/17/receitas)
```

`/workspace/profile.md` (fora de qualquer produto) guarda dados do membro: budget, ESP, tools, mercado, idioma. Escrito pela skill 00, lido por todas. O **`ABRIR-AQUI.html`** de cada produto é a porta de entrada: lista cada fase, o que já foi feito e o próximo passo — toda skill o regenera ao terminar.

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
A Aura detecta MCPs externos e enriquece skills automaticamente. **Meta MCP** (cascade oficial → Pipeboard → manual), **TrendTrack**, **Refero** e **Klaviyo** são os casos principais. Prefixos canônicos em `.claude/lib/mcp-detect/README.md`.

---

## 11. Memória persistente — registry creative-dna

Cross-product learning. A skill 08 (creatives) salva DNA toda vez que executa: hook archetypes que funcionaram, voice signatures, padrões estruturais. Próxima execução em outro produto carrega esse registry e adapta sem reinventar.

**Read/write:** via `lib/creative-dna/registry.py`. Skill 08 chama em silent steps (o "Contexto a carregar" — item 6 — carrega o dna-profile.json e enviesa a ideação desde a ETAPA 3; a ETAPA 7.6 escreve).

**O que NÃO entra no registry:** dados específicos do produto (nomes, claims, preços). Só padrões abstratos.

---

## 12. Integrações MCP opcionais — Meta + TrendTrack + Refero + Klaviyo

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
| 11 ad analysis (ETAPA 1) | Cascade via `sync-campaign-from-meta.md` (receita única: oficial → Pipeboard → manual) | Auto-pull + market context (industry benchmark, auction ranking, opportunity score, anomalies). Compara membro vs vertical p50. |
| 10 ad strategy (pre-flight) | `ads_get_dataset_quality` | Gate de EMQ ≥ 6/10 (Event Match Quality) antes do launch |
| `pause-ad-set.md` | `ads_update_entity` (cascade) | Executa a pausa que o membro decidiu — o gatilho é humano (leitura das réguas de kill do cânone §3 pela Skill 11), nunca uma regra de performance |
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
| `find_winning_products` | Discover | Top products num nicho com receita rastreada |
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
| 03 competitor analysis | `brief_competitor`, `scan_ad`, `search_shops`, `find_similar_shops` | ETAPAs 1-3 se juntam em 1-2 tool calls |
| 08 creatives | `creative_inspiration_pack`, `scan_ad` | Hooks Bank com archetypes reais |
| 11 ad analysis | `scan_ad`, `daily_radar` | Benchmark de winners + loop de monitoramento |
| 13 retention | `analyze_shop_emails` | Timing dos fluxos calibrado contra concorrência |

**Padrão de detecção:** tools com prefixo `mcp__trendtrack__` → fonte primária. Ausente → fallback silencioso.

**Custos:** sistema de créditos. Quando skill planeja >5 chamadas, roda `check_credits` primeiro.

**Privacidade:** OAuth read-only. Aura não armazena tokens.

### 12.3 — Refero MCP (design system curado)

Refero é um catálogo curado de ~200 design systems de sites premium (Cursor, Linear, Vercel, Notion, Stripe, etc.). O MCP é pacote npm local (`fidgetcoding-refero-mcp`). A Aura usa na skill 07a-page-design ETAPA 2 (Brand Signals) pra extrair signals coerentes de cor/typography/spacing — esses signals alimentam o `frontend-design`, que gera o HTML da página (a fonte única de verdade visual). O Refero é fonte de signals, não decisão visual.

**Como o membro conecta (opcional):**
- **Claude Code:** `claude mcp add refero -- npx -y fidgetcoding-refero-mcp`

Sem auth obrigatória. Não confundir com o `mcp_token` da URL do `styles.refero.design` (esse é do front-end web).

Opcionais: `OPENAI_API_KEY` (semantic search) e `REFERO_MCP_VAULT_DIR` (escrever `DESIGN.md` no workspace).

**As 6 tools:**

| Tool | Categoria | Propósito |
|---|---|---|
| `refero_search` | Discover | Vibe search natural |
| `refero_get` | Inspect | designSystem completo de 1 site |
| `refero_similar` | Inspect | Similar styles ranking |
| `refero_list` | Browse | Catálogo com filtros |
| `refero_design_md` | Generate | Renderiza style como `DESIGN.md` |
| `refero_refresh` | Maintenance | Bypass cache 24h |

**Cascade de brand signals na skill 07a-page-design ETAPA 2:** Refero → screenshot→visão (membro tira print full-page da loja de referência e o Claude lê a imagem com visão nativa — imune a Cloudflare/JS/markup bagunçado; fallback primário de inspiração) → `tools/design-clone/` (Playwright, caminho 3 opcional pra hex exato) → manual / 8 presets.

**O Claude Design SAIU do caminho crítico.** O design é HTML-first via a skill nativa `frontend-design` (gera a página inteira como HTML+CSS self-contained com a copy real). Refero entra antes, só como input de signals pro `frontend-design`.

### 12.4 — Klaviyo MCP oficial (criação de flows de retenção)

O Klaviyo publicou um MCP oficial (25 tools, 2026) que a skill 13 (retention-engine) usa como caminho preferencial pra criar os flows de lifecycle direto na conta do membro — com contrato de API estável, sem scraping e sem cookie de sessão (o caminho de session-cookie foi REMOVIDO por risco de segurança).

**Padrão de detecção:** tools com prefixo `mcp__klaviyo__` na sessão → Caminho 1 (criação direta via MCP). Ausente ou falha (auth/rate-limit) → fallback silencioso pro Caminho 2: assets HTML + `setup-guide.md` que o membro importa no UI do ESP (único caminho pra Omnisend/MailerLite/Shopify Email, que não têm MCP).

**Regra inviolável:** flows criados via MCP nascem SEMPRE em draft/manual — a skill nunca ativa automaticamente (risco de spam se um email tiver bug). O membro revisa no Klaviyo UI e ativa. `source` logado no `13-retention-engine/dados.json`: `klaviyo_mcp` ou `klaviyo_assets_guide`.

---

## 13. Como rodar uma sessão completa do zero

Ordem canônica pra um produto novo:

1. **setup** — cria workspace, profile, manifest
2. **product research** — valida o produto, define vertical
   - **sourcing** (01b, opcional) — fornecedor, cotação e logística; roda em paralelo aos passos 3-4 e fecha o custo real antes da oferta
3. **market research** — VOC, awareness, drivers
4. **competitor analysis** — 5-10 concorrentes, padrões, gaps
5. **offer** — mecanismo, pricing, stack, garantia, unit economics
6. **copy** — copy completa pra cada section
7. **storefront** — 07a (page design HTML-first) → 07b (build + deploy) → 07c (tracking setup) → 07d (checkout AOV)
8. **bonus delivery — Fase A** (05, se a oferta tem bônus) — assets + config de GWP/entrega (todo bônus da PDP existe antes do primeiro ad)
9. **retention — Fase A** (13) — flows de recuperação: abandoned cart + post-purchase (infraestrutura de cash flow do launch, custa zero no free tier)
10. **creatives** — conceitos com briefings, em pack 3-2-2; o número sai da capacidade de teste, não do stage
11. **agentic readiness** (07e) — checklist de descoberta por agentes de AI na loja viva
12. **consistency audit** — cross-phase drift check (gate de launch)
13. **ad strategy** — capacidade de teste, estrutura (1 campanha com CBO → N ad sets, 1 = 1 conceito), naming, UTM, proteções
14. **— LAUNCH —**
15. **ad analysis** (depois de 3-7 dias) — 4Pi, classificação nas 4 classes, diagnóstico, decisões
16. **scale** (depois que aparece um breakthrough) — Scaling Protocol vertical + horizontal
17. **retention — Fase B** (≥50 compras) — win-back, replenishment, segmentação + **bonus delivery — Fase B** (tracking de take-rate)
18. **content recycler** (só com breakthrough) — Trilha 1 amplificação; Trilha 2 (9 derivadas) sob pedido

**Fora desta sequência — a finance engine (15) como consulta lateral.** Ela não ocupa um passo: roda quando o membro precisa de uma decisão financeira. Dois momentos naturais — logo depois do passo 5 (**offer**), pra checar se a oferta fecha a conta do negócio inteiro com o custo fixo dentro (Modo A), e a cada mês fechado depois do LAUNCH, pra medir alavancas, cohorts, payback e caixa (Modo B). As skills **04** (oferta), **10** (ad strategy), **11** (ad analysis), **12** (escala) e **13** (retenção) leem o output dela quando ele existe — sem o arquivo, cada uma mantém o comportamento atual.

**As outras cinco laterais (16-20) seguem o mesmo princípio — nenhuma ocupa um passo, e cada uma tem sua posição natural:**

- **Creator engine (16)** — DUAS fases com posições diferentes. A **Fase A** (seeding + conteúdo humano) pode rodar em paralelo desde cedo: junto do passo 10 (**creatives**) e antes do LAUNCH, a partir do momento em que existe produto com preço definido (a plataforma de seeding prefere a loja no ar; o outreach manual anda antes). Começar cedo importa — do contrato de um creator externo até o conteúdo virar ad passam ~26 dias na média. A **Fase B** (contrato recorrente, whitelisting, partnership ads) só abre depois de um breakthrough confirmado pela **11**.
- **Promo engine (17)** — sazonal: dispara por época ou pedido (setembro-outubro pra montar o Q4; as outras datas pelo calendário sazonal de desejos), uma rodada por janela. Sempre com o gate de números: breakeven ROAS e CPA recalculados com a margem promocional antes de ligar qualquer campanha. O evergreen segue intocado em paralelo.
- **Team engine (18)** e **marketplace engine (20)** — consultas de estágio scaling: time quando o membro vira o gargalo (ou a vaga/gestão aparecem), canal secundário só depois de breakthrough na 11 e conta fechando na 15. Pra starter/validating, a resposta honesta das duas costuma ser "ainda não", com o motivo e o sinal que reabre a conversa.
- **Ops engine (19)** — a parte de backups (checklist de continuidade) vale desde o começo, logo depois do passo 1 (**setup**) e antes do primeiro ad: conta nova é a mais frágil da vida do negócio, e a redundância é mais barata de armar cedo. O resto (constraint do ano, negócio como ativo) revisita por trimestre e antes de decisões grandes — escala agressiva e Q4.

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
| 2026-05-03 | Self-audit silencioso obrigatório no fim de toda skill (rule + CLAUDE.md rule 9) |
| 2026-05-03 | **Renumeração completa das skills** pra match com ordem de execução: bonus-delivery 13→05, copy 05→06, page 06→07, creatives 07→08, consistency-audit 11→09, ad-strategy 08→10, ad-analysis 09→11, scale 10→12, retention 12→13. Content-recycler permanece 14. |
| 2026-05-04 | Skill 00 setup pergunta idioma de relatório (`pt-BR` ou `en`) como primeira pergunta; salvo em `profile.md` como `report_language`. |
| 2026-05-11 | **Integração do MCP oficial da Meta** (`mcp.facebook.com/ads`, open beta desde 2026-04-29). Nova receita `sync-campaign-from-meta-official.md` usa as 29 tools nativas. Skill 11 ETAPA 1 vira cascade: oficial → Pipeboard → manual. `pause-ad-set.md` ganha cascade interno. CLAUDE.md rule 10 expandida. |
| 2026-05-11 | **Integração Refero MCP** (`fidgetcoding-refero-mcp`). Catálogo curado de ~200 design systems premium. Skill 07a ETAPA 2.1 Brand Discovery vira cascade: Refero → `tools/design-clone/` → manual. Complementar ao Claude Design (ETAPA 0.5 continua gerando 4 variações visuais). CLAUDE.md rule 10 expandida. Nova lib `refero-integration/`. |
| 2026-06-20 | **Redesign storefront (Onda 2).** Fase de página vira a cadeia storefront **07a-page-design → 07b-page-build → 07c-tracking-setup → 07d-checkout-aov**. 07a/07b são HTML-first determinístico: design nasce in-session via `frontend-design` (fonte única visual aprovada antes do Liquid), conversão HTML→Liquid por código via `liquid-converter.py`. Claude Design sai do caminho crítico; Refero vira fonte de signals e screenshot→visão vira o fallback primário de inspiração. **07c-tracking-setup** (Pixel + CAPI + analytics stack) e **07d-checkout-aov** (upsell/bump/bundle/checkout trust) são skills novas. **Bonus delivery (05)** redesenhada pra bônus de ecom (GWP, e-book, free SKU, gift wrapping) e movida pra pós-launch junto da 13. Gate de consistência (09) trava o launch (skill 10), não o deploy da página. CLAUDE.md/AGENTS.md rule 10c atualizada. |
| 2026-06-20 | **Skill 13 sem cookie.** Caminho de session-cookie/internal-API do Klaviyo DELETADO (risco de segurança: cookie dava acesso full à conta). Cascade da 13 vira: **Klaviyo MCP oficial** (`mcp__klaviyo__`, flows sempre em draft) → assets HTML + setup-guide. Papéis pós-compra consolidados: 05 produz asset de bônus, 13 é o executor único de email, 14 gera só variação de nutrição derivada de winner. |
| 2026-06-22 | **Coleta resiliente da web.** Nova lib `web-fetch` (fetcher Playwright headless + stealth: `--mode text\|reddit\|reviews`, Reddit via redlib) + rule `resilient-fetch` (NON-NEGOTIABLE): cascade WebSearch → WebFetch → fetcher; bloqueio é tratado, nunca preenchido com texto inventado. Resolve os bloqueios de fetch (403/Cloudflare/CAPTCHA soft) nas skills de research. |
| 2026-07-03 | **Skill 07e — Agentic Readiness (AEO).** Skill nova (19ª): checklist pós-deploy/pré-launch de descoberta por agentes de compra com AI — canal Agentic Storefronts + policies, Knowledge Base app, dados estruturados da PDP (audita a camada GEO da 07b), specs legíveis por agente, robots.txt (OAI-SearchBot/ChatGPT-User/PerplexityBot/ClaudeBot/Google-Extended), llms.txt, Perplexity Merchant Program, feed do Merchant Center, score de AI visibility. Não usa a base Aura (fontes: docs oficiais + verificação na loja viva). Bonus delivery (05) formalizada em DUAS fases (Fase A pré-launch: assets + GWP; Fase B pós-launch: tracking). Recipes novas registradas: `creative-loop.md` e `create-fixed-bundles.md`; `sync-campaign-from-meta.md` vira receita única com cascade interna. |
| 2026-07-09 | **Retention (13) em DUAS fases.** Fase A pré-launch (flows de recuperação: abandoned cart + post-purchase) entra na ordem canônica entre a 05 Fase A e os criativos — infraestrutura de cash flow do launch, não campanha de email (win-back/replenishment e campanhas continuam pós-launch na Fase B, ≥50 compras). Painel `ABRIR-AQUI.html` ganha tag "2 fases" nos cards da 05/13, próximo-passo condicional (07d concluída → cobra 05 Fase A se a oferta tem bônus, depois 13 Fase A) e linha fixa explicando que os cards seguem a ordem de execução (o número é o ID fixo da skill). |
| 2026-07-29 | **Skill 01b — Sourcing (opcional).** Fornecedor, cotação e logística: a operação explicada em linguagem simples (MOQ, OEM/ODM, DDP, 3PL, FBA, dropship — tabela de trade-offs), análise de fornecedores (começar vs escalar), mensagem de cotação em inglês (7 blocos), agentes de sourcing parceiros da Aura (WhatsApp), comparação de cotações e contrato com a 04 (ETAPA 1 lê `sourcing/dados.json` fechado e usa COGS real em vez de estimar). Painel ganha tag "Opcional" (nunca vira sugestão de próximo passo). Docs de onboarding aura-explained (pt/en) e aura-setup-en removidos — `docs/aura-setup-pt.html` é o único guia. |
| 2026-08-11 | **Storefront endurecido em produção.** Libs novas `shopify-section-patterns` (6 padrões de section com problema/solução/código/armadilhas + sistema de tokens de paleta por snippet) e `theme-verify` (gate Playwright: overflow/seções, censo de fonte computada, continuidade de animação com rede lenta emulada). 07a ganha a variante clone fiel seção a seção (snapshot SingleFile → sections OS 2.0 editáveis) + prova de paletas na página real; 07b ganha 3 limitações Shopify novas (richtext default sem `<p>` = rejeição silenciosa do arquivo; assign-first em argumento nomeado; `image_picker` sem default) e o iteration loop alinhado à Regra 6b. Rule `shopify-theme-safety`: Regra 6b (nunca regenerar template JSON por cima do ar + `tools/theme-template-merge.py`) e 6c (arquivo de identidade é por-tema em lojas com 2+ paletas). |
| 2026-09-01 | **Cânone de ads reescrito (ad-taxonomy + unit-economics).** Duas libs novas viram fonte única e as skills 08/10/11/12/14 passam a ler delas em vez de redefinir régua local. **Estrutura de campanha:** 1 campanha com CBO → **N ad sets, 1 ad set = 1 conceito** (3 criativos + 2 primary texts + 2 headlines), com o número de ad sets vindo da **capacidade de teste** (`assets = budget diário ÷ target CPA`, piso US$ 100-150/dia, teto ~3× target CPA por ad set, máx. 5 ad sets abaixo de US$ 1k/dia) — substitui o "1 ad set → 5-12 criativos". **Classificação:** 4 classes (loser · KPI winner · spend winner · breakthrough); só `breakthrough` libera escala e reciclagem, `kpi_winner` é tratado como loser para decisão. **PGS saiu:** Automated Rule com condição de performance é recusada pelo Meta em CBO — o substituto é `ad set spending limit → daily maximum` + as duas automações de proteção obrigatórias (spend 5× em 24h; URL ≠ domínio), que nascem desativadas. O ritmo de escala é o **Scaling Protocol** manual (+20% após 48-72h acima do target, depois a cada 24h; −20% abaixo do breakeven; gate click-based ≥60%; reset da meia-noite sobre o gasto REAL), e o champions ad set foi aposentado em favor do **ABO paralelo** (~10% do budget da campanha principal). **Unit economics:** nenhuma recomendação de cortar spend por queda de ROAS sai sem os custos fixos na mesa (a espiral do ROAS). |
| 2026-09-01 | **Skill 14 em duas trilhas + gatilho `breakthrough`.** O gatilho deixa de ser "winner" genérico: só criativo classificado como `breakthrough` pela 11 entra (`kpi_winner` nunca; `spend_winner` só no Movimento 1). **Trilha 1 — Amplificação** vira o default e roda primeiro (6 movimentos: iterar pelos 4 elementos, portar o ângulo, LP/prelander dedicada, portar pra Axon/AppLovin e TikTok, duplicar em ABO próprio, creator report), com handoff explícito pra 08/07a/12. As **9 derivadas de formato viram Trilha 2**, sob pedido, reenquadradas como jogada de marca e LTV. Novo output: `essence.json` com `framework_template` + `psychological_mechanism`, `amplification-plan.md/.html` e `creator-report.md/.html`. |
| 2026-09-01 | **Skill 06 ganha modelagem por espécime (`swipe-models`).** Lib nova com `specimens.json` (12 espécimes estruturais de swipe files reais, seletor `page_type` × awareness × sophistication × vertical). **ETAPA 2.5 obrigatória:** escolher 1 espécime primário (+1 secundário opcional), puxar a anatomia pela `best_query` e montar o `specimen_block_map` antes de escrever — modelando estrutura e mecânica, nunca conteúdo. **Sweep 9 (markup audit)** fecha a revisão em 5 camadas a partir do nó `auditoria` do mesmo JSON; `specimen_primary`/`specimen_block_map`/`markup_audit` entram no `dados.json` e a 11 os usa pra diagnosticar página que converte mal. |
| 2026-09-01 | **Índice de frameworks expandido (append incremental).** O `kb-index` sai de **541 para 1.309 entradas** e de **14 para 19 domínios** (em duas ondas na mesma data: o append incremental e, na criação das skills 16-20, o retag geral + 19 entradas novas), com `name` e `best_query` das entradas antigas preservados byte a byte (centenas dessas queries estão copiadas literalmente dentro das skills — reescrevê-las quebraria as buscas em silêncio). Os 5 domínios novos incluem `supply-chain-sourcing` (consumido pela 01b) e `finance-projections` (consumido pela 15). Três domínios entraram **órfãos**, indexados sem skill consumidora (`team-hiring-ops`, `ops-scale-risk`, `affiliate-creator-channels`) — todos ganharam consumidora na 2ª onda (skills 18/19/20 + 16). |
| 2026-09-01 | **Skill 15 — Finance Engine (21ª skill).** Dona do modelo financeiro completo declarado no cânone `unit-economics` §5, e consumidora do domínio `finance-projections` do kb-index (22 sistemas, incluindo os 4 que estavam dormentes: Float Stack, Função Financeira em 3 Camadas, Triângulo de Forecasts e Banking Sheet). **Não é etapa da sequência — é consulta lateral**, acionada quando o membro precisa de decisão financeira. **Dois modos decididos pelos dados:** A (planejar, sem mês fechado — monthly model com custo fixo dentro, margem de contribuição, piso de CAC, caixa pra 90 dias, benchmarks DTC) e B (medir, com ≥1 mês fechado — 4 alavancas, cohorts com decay e LTV medido, payback de 90 dias, teto de escala, ciclo de caixa ≈105 dias de float, banking sheet semanal). A ETAPA 5 fecha o buraco que a arquitetura tinha: a decisão de spend passa a ter camada de custo fixo, com `roas_spiral.breakeven_roas_with_fixed` e `cut_spend_recommendation_allowed` publicados pra 11 e 12 lerem antes de recomendar qualquer corte. Leitura aditiva nas skills 04/10/11/12/13 — sem o `dados.json` da 15, cada uma mantém o comportamento atual. |
| 2026-09-01 | **Skills 16-20 — as cinco engines laterais (o framework fecha em 26 skills).** **16-creator-engine** (a operação de conteúdo humano em DUAS fases: seeding, casting amarrado aos sub-avatares da 02, framework de brief e pipeline TikTok Shop rodando em paralelo à 08 desde cedo; whitelisting, escada de embaixador e partnership ads SÓ depois de breakthrough confirmado pela 11 — a 08 segue dona do QUE dizer, a 16 vira dona de QUEM grava). **17-promo-engine** (a janela promocional de ponta a ponta — Q4/BFCM, sazonais, flash sales — com o gate inegociável de recalcular breakeven ROAS/CPA com a margem promocional antes de ligar campanha; Promo Campaign Broad/WARM60/HOT90 em paralelo ao evergreen intocado, surf + reset da meia-noite pelo cânone §5, aterrissagem com rule de fim por horário). **18-team-engine** (quando/como contratar e como rodar o time — consumidora do maior bloco órfão da base, o domínio `team-hiring-ops` inteiro). **19-ops-engine** (constraint dos 12 meses, checklist de backups com status confirmado pelo membro — que vale desde o começo, porque conta nova é a mais frágil — e negócio como ativo). **20-marketplace-engine** (gate de expansão de canal + Amazon, TikTok Shop e afiliados como canais secundários). Junto com elas: **cânone novo `ad-log`** (registro append-only de toda mudança executada na conta — escrito por 10/12/14/17 e receitas no momento da execução, lido pela 11 sempre e pela 12 antes de escalar), o **contrato de cobertura do índice** em todas as skills consumidoras (enumerar TODAS as entradas do domínio com `use_in_skill` da skill e puxar cada uma pela `best_query` com deep=true — a puxada deixa de ser amostra e vira cobertura), os **contratos entre skills fechados** (cada engine nova declara em tabela a divisão explícita com as vizinhas — quem é dona de quê, o que entrega e o que nunca faz) e o **kb-index em 1.309 entradas / 19 domínios**, com os três domínios órfãos ganhando consumidora (restam 5 entradas dormant, todas em `ops-scale-risk`). |
