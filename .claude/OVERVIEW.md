---
documento: Visão geral
versão: setembro 2026
data: 2026-09-17
público: Interno (framework)
eyebrow: Aura Engine / visão geral
tipo: Visão geral
---

# Aura Engine — Visão Geral Completa

Tudo que existe no ecossistema Aura: o que cada peça faz, como se conectam, e como uma sessão flui do início ao fim.

**Versão:** setembro 2026
**Skills:** 26, identificadas pelo id (o slug sem número; o número antigo continua só como apelido de roteamento): 19 skills na sequência canônica (21 passos, porque `bonus-delivery` e `retention-engine` rodam em duas fases), mais a `sourcing` (paralela, opcional) e seis engines laterais. A sub-cadeia storefront é `page-design`/`page-build`/`tracking-setup`/`checkout-aov`, seguida da `agentic-readiness`
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

- **Claude Code:** automático. O repo traz um `.mcp.json` que registra o servidor `aura`; na primeira abertura do Claude Code na pasta, o membro só aprova o aviso de novo servidor. Não há variável de ambiente nem credencial pra configurar.
- **Claude Desktop:** Settings → Connectors (em versões antigas, Integrations) → Add custom connector → Nome *Aura* → URL `https://aura-mcp-production.up.railway.app/mcp` → Add (uma vez por dispositivo, permanente até o membro remover)

Instruções completas com screenshots ficam em `docs/aura-setup-pt.html`.

### O que tem dentro

A base agrega a literatura fundacional de direct-response e ecommerce mais metodologia original. Quando uma skill precisa fundamentar uma decisão, consulta com frases de intent específica. Exemplos por domínio:

| Domínio | Queries representativas |
|---|---|
| Pesquisa de produto | domínio `product-research` do kb-index pela `best_query` (Schwartz, Hormozi, Halbert, Ries & Trout, Brunson); descoberta, Trends, Trustpilot e recombinação são método da própria skill, não da base |
| Pesquisa de mercado | `unified research document process`, `psychographic research drivers`, `voice of customer review mining`, `Schwartz five stages of awareness unaware problem aware solution aware product aware most aware` |
| Análise de concorrente | `competitor research extracting claims`, `market sophistication saturation` |
| Construção de oferta | `unique mechanism UMP UMS theory`, `offer stack pricing guarantee`, `Hormozi value equation dream outcome perceived likelihood time delay effort sacrifice` |
| Copywriting | `headlines formulas process 100 lines`, `Schwartz lead desire identification belief dimension awareness lead selection`, `hero sections types selection`, `PDP structure reviews above fold how it works section ecommerce product detail page`, `CTA psychology call to action` |
| Produção de criativo | `ad angles concepts variations`, `ad formats roadmap creative`, `hooks video ads`, `funnel creative playbook` |
| Meta Ads | `scientific method meta ads control variable`, `one campaign method AndroMeta`, `4Pi analysis spend frequency CPM`, `budget scaling methods 5% rule`, `automations obrigatórias spend 5x em 24h pausar URL diferente do site desligar` (automação é só proteção — regra com condição de performance é impossível em campanha com CBO, o Meta recusa; cânone ad-taxonomy §6) |
| Escala | `scaling strategy vertical horizontal`, `creative diversity scaling mechanism`, `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo` |
| Retenção | `email lifecycle welcome abandoned cart post-purchase winback`, `30-60-90 day LTV email SMS flow second purchase window replenishment` |
| Reciclagem de conteúdo | Nenhuma das duas trilhas da skill `content-recycler` vem da base: a Trilha 1 (amplificação) sai do cânone `.claude/lib/ad-taxonomy/README.md` (§2 classes, §5 escala, §7 Sniper) e a estrutura "1 criativo → 9 formatos" da Trilha 2 sai da lib `.claude/lib/content-recycler/` (formats.json). Na base a skill `content-recycler` puxa só frameworks de copy nomeados, ex: `Caples four U's hierarchy unique useful urgent ultra-specific headlines`, `gap theory of curiosity hooks counterintuitive open loop slippery slope` |

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
│   ├── OVERVIEW.md / .html ← este documento (o .html é gerado do .md pelo gen_docs.py)
│   ├── skills/            ← 26 skills, todas no formato nativo: `<id>/SKILL.md` (o roteiro) + `<id>/reference/*.md` (o material de apoio que cada etapa manda abrir); sub-cadeia storefront `page-design`/`page-build`/`tracking-setup`/`checkout-aov` + `agentic-readiness`
│   ├── lib/               ← libs reutilizáveis chamadas pelas skills
│   ├── rules/             ← diretrizes auto-carregadas por contexto
│   ├── hooks/             ← scripts que rodam em eventos do Claude Code
│   ├── templates/         ← templates HTML, manifest-schema, schemas/ (um por dados.json de fase), snippet do logo SVG
│   └── settings.json      ← config do Claude Code (hooks, permissions)
│
└── workspace/             ← criado pela skill `setup`, organizado por produto
    ├── profile.md         ← contexto do membro (budget, ESP, tools, mercado, idioma)
    ├── ABRIR-AQUI.html    ← painel global, um card por produto (build_index.py --global)
    └── [product-slug]/
        ├── manifest.json  ← single source of truth do estado do produto (só muda pelo tools/manifest.py)
        └── <skill-id>/    ← artefatos de cada fase, em pasta com o id da skill
```

A Base de Conhecimento Aura **não** está nesta árvore — é um servidor MCP remoto conectado separadamente. Engine e Base de Conhecimento são independentes.

---

## 4. As skills (em detalhe)

Cada skill é um arquivo `.md` com frontmatter (nome + descrição) e corpo estruturado em ETAPAs numeradas. Skills estão listadas abaixo na ordem em que rodam (o id de cada skill é o slug; o número antigo é só apelido), com três exceções: a `agentic-readiness` aparece depois da `creative-engine` porque é ali que ela roda, a `finance-engine` aparece logo depois da `offer-builder` porque é ali que ela é consultada pela primeira vez, e as engines laterais (`creator-engine`, `promo-engine`, `team-engine`, `ops-engine` e `marketplace-engine`) aparecem juntas no fim, depois da `content-recycler`, porque não são etapas da sequência. A ordem canônica exata de uma sessão está no §13. A fase de página virou a fase **storefront** (`page-design`→`page-build`→`tracking-setup`→`checkout-aov`), a bonus delivery e a retention (`retention-engine`) rodam em duas fases (Fase A pré-launch, Fase B pós-launch), a agentic readiness (`agentic-readiness`) roda depois dos criativos, antes do gate de launch (`consistency-audit`), e a finance engine não é etapa da sequência — é consulta lateral, acionada quando o membro precisa de uma decisão financeira. As engines 16 (creators), 17 (promo), 18 (time), 19 (ops) e 20 (marketplace) são laterais como a `finance-engine`, cada uma com sua posição natural (detalhe no §13).

### Setup · Passo 1 · apelido antigo: 00 <!-- gen:skill-header:setup -->
**Trigger:** `"setup"`
Configuração da primeira vez. Pergunta o idioma preferido pra relatórios internos (`pt-BR` ou `en`), cria `/workspace/` com o slug do produto, coleta contexto do membro (budget, ESP, tools, mercado) em `profile.md`, inicializa `manifest.json`.
**Output:** `manifest.json` + `profile.md`

### Product Research · Passo 2 · apelido antigo: 01 <!-- gen:skill-header:product-research -->
**Trigger:** `"product research"`
Pesquisa por **recombinação de elementos validados**. Descobre as marcas DTC que já escalam no nicho (default health & supplements) no **TrendTrack — Explorer → Meta Ads**, com dois conjuntos fixos de filtros (native ads em imagem com copy ≥ 1500 caracteres, e em vídeo; ativos há ≥ 10 dias, criados nos últimos 30, ad rank top 10%, growth rising, US, tráfego ≥ 300k/mês), pré-seleciona DTCs com AOV ≥ $60 contando bundle/upsell e monta a **ficha de cada marca** (LP mais escalada, ads mais escalados com links, visitas/mês, oferta e AOV, mecanismo do problema e da solução, ângulo, avatar, formato de criativo). **Duas checagens só:** Google Trends (problema + ingrediente, 5 anos, US — queda de 12+ meses elimina; problema subindo + ingrediente estável é o melhor cenário; ingrediente em pico recente pede troca de mecanismo; subida vertical em 1-3 meses é hype) e Trustpilot 1-2 estrelas (reclamação de cobrança/entrega passa; maioria sobre eficácia elimina — produto que não funciona vira refund em massa no mês 2-3). Decompõe cada finalista em elementos (mecanismos, ângulo, formato, posicionamento, criativo, oferta) com evidência de escala, monta o pool cruzado (aberto vs saturado) e as **jogadas de recombinação** — 4 padrões: mesmo mecanismo com outro ângulo/formato/posicionamento; problema de A + solução de B; trocar o mecanismo mantendo o ângulo; aprimorar um mecanismo validado. Nunca clonar, nunca criar do zero. Rankeia pelos 8 eixos de score (Magnitude, Sophistication, Awareness, UM, Avatar, Offer, Creative, Trend) e entrega o plano preliminar da #1.
**MCP ou manual:** com `mcp__trendtrack__*` a skill roda as pesquisas e as fichas sozinha (checa créditos antes); sem MCP ou sem créditos, explica os mesmos filtros pro membro aplicar no browser e colar.
**Banco de marcas:** no **Notion** (página-mãe + banco de dados com uma página por marca + página de ranking) se o MCP estiver conectado; senão `banco-de-marcas.html` na pasta do produto. O `.md` é salvo sempre (`market-research`/`competitor-analysis` leem).
**Output:** `product-research/product-research.md` + `.html` + `dados.json` + `banco-de-marcas.md` (+ `.html` sem Notion) + `brand.md` do vencedor

### Sourcing · Paralela, opcional · apelido antigo: 01b <!-- gen:skill-header:sourcing -->
**Trigger:** `"sourcing"` / `"fornecedor"`
Fornecedor, cotação e logística do produto físico. Explica a operação em linguagem simples (MOQ, OEM/ODM, DDP, 3PL, FBA), analisa anúncios/fornecedores (começar vs escalar), monta a mensagem de cotação em inglês (7 blocos), oferece os agentes de sourcing parceiros da Aura (contato WhatsApp), compara cotações e entrega o custo real pro COGS da Skill `offer-builder`. Roda em paralelo à `market-research` e à `competitor-analysis`.
**Output:** `sourcing/sourcing.md` + `sourcing.html` + `dados.json`

### Market Research · Passo 3 · apelido antigo: 02 <!-- gen:skill-header:market-research -->
**Trigger:** `"market research"`
Coleta de Voice of Customer em Reddit, fóruns, reviews, comentários do TikTok. Identifica frases exatas dos clientes, mapeia awareness distribution, drivers psicográficos, objeções ranqueadas.
**Por que importa:** o documento mais consultado do sistema.
**Output:** `market-research/market-research.md` + `market-research.html` + `dados.json`

### Competitor Analysis · Passo 4 · apelido antigo: 03 <!-- gen:skill-header:competitor-analysis -->
**Trigger:** `"competitor analysis"`
Identifica 5-10 concorrentes ativos via Meta Ad Library + Similarweb. Analisa PDPs. ETAPA 3C: análise profunda de criativos escalados com transcrição (Groq API ou Whisper local).
**Fallback chain pra páginas bloqueadas:** Wayback Machine → archive.today.
**Enrichment opcional:** quando MCP TrendTrack conectado, ETAPA 0.5 condensa ETAPAs 1-3 em `brief_competitor` + `search_shops` + `find_similar_shops` + `scan_ad`.
**Output:** `competitor-analysis/competitor-analysis.md` + `competitor-analysis.html` + `dados.json` + `creative-patterns.json` + `creatives-inbox/` (uploads do membro + transcripts Whisper)

### Offer Builder · Passo 5 · apelido antigo: 04 <!-- gen:skill-header:offer-builder -->
**Trigger:** `"offer"`
Constrói mecanismo único (UMP/UMS — a razão pela qual o produto resolve o problema, e por que a alternativa do mercado falha). ETAPA 2.5 obrigatória — Research Foundation. Pricing triangulado, bonus stack, garantia, unit economics, 12 sanity checks (4 deles bloqueiam o save).
**Economia unitária pelo cânone `.claude/lib/unit-economics/README.md`:** stack de custos variáveis item a item (nunca agregado), margem de contribuição rotulada corretamente (nunca "Lucro" sobre um número que não subtraiu os fixos), CAC ≠ CPA e o piso de CAC (US$ 15-25) como gate.
**Outputs críticos pras skills downstream:**
- `bonuses[]` array → lido pela skill `bonus-delivery`
- `offer_stack` string → lido pela skill `copy-engine`
- `unit_economics.weighted_margin_per_order` (breakeven CPA) + `target_cpa_primary_2x/3x` (target CPA — o divisor da capacidade de teste) → lidos pelas skills `ad-strategy`, `ad-analysis` e `scale-engine`
- `budget_viability.fixed_costs_monthly` → lido pela `ad-analysis` antes de qualquer recomendação de cortar spend

**Output:** `offer-builder/offer-builder.md` + `offer-builder.html` + `dados.json` + `research-foundation.json`

### Finance Engine · Lateral · apelido antigo: 15 <!-- gen:skill-header:finance-engine -->
**Trigger:** `"finance"` / `"finanças"` / `"projeção"` / `"cohort"` / `"fluxo de caixa"` / `"quanto posso gastar em ads"` / `"payback"` / `"runway"`
Dona do modelo financeiro completo declarado no cânone `.claude/lib/unit-economics/README.md` §5 (4 alavancas, cohorts, ciclo de caixa). **Não é fase do pipeline** — roda quando o membro precisa de uma decisão financeira, tipicamente logo depois da `offer-builder` e depois a cada mês fechado. Recorrente por natureza: banking sheet semanal, calibragem de cohort mensal, revisão de LTV semestral.
**Dois modos, decididos pelos dados — sem pergunta extra:**
- **Modo A — Planejar** (nenhum mês fechado com ad spend *e* clientes novos do Shopify): monthly model linha a linha com o custo fixo dentro, margem de contribuição e ponto de cobertura do fixo, `gross_margin_needed_to_exist` (o lucro bruto que a operação precisa gerar todo mês só pra existir), piso de CAC, necessidade de caixa pra 90 dias, runway e benchmarks DTC.
- **Modo B — Medir** (≥1 mês fechado): as 4 alavancas (AOV, CAC, ad spend, % de recorrentes) simuladas uma por vez e ranqueadas, cohorts de 12 meses com decay factor e LTV medido, payback de 90 dias e first-order profitability, taxa de aumento do CAC e teto de escala, ciclo de conversão de caixa (o stack de float ≈ 105 dias) e banking sheet semanal. Com 1-2 meses fechados o cohort roda **não calibrado** (payback modelado com 30 dias de folga); com 3+ ele estabiliza.

**A ETAPA 5 é a razão principal de a skill existir:** ela transforma a espiral do ROAS (cânone §4) em número e publica `roas_spiral.breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed` e `cut_spend_recommendation_allowed`. Com os fixos desconhecidos, `cut_spend_recommendation_allowed` é `false` e a recomendação vira pergunta, não instrução.
**As regras que não se negociam:** nunca chamar de "lucro" um número que não subtraiu custo fixo (`operating_income` é `null` enquanto os fixos forem `null`); CAC vem do Shopify (`new customer = TRUE`), nunca do CPA de plataforma; e **três campos nunca se estima** — custo fixo mensal, CAC real e contagem de clientes novos. Faltando qualquer um, o campo fica `null`, entra em `pending_inputs[]` e o bloco derivado dele fica marcado como não calculável.
**Contrato de leitura (aditivo — sem o arquivo, cada skill mantém o comportamento atual):** a **`ad-analysis`** lê o breakeven com fixo e a permissão de corte; a **`scale-engine`** lê caixa, float, runway, fixos e teto de escala; a **`offer-builder`** fecha `budget_viability.result_after_fixed_monthly`; a **`retention-engine`** mira o mês real de cruzamento do cohort e o pico de churn; a **`ad-strategy`** checa o CPA-alvo contra o piso físico de CAC.
**Output:** `finance-engine/finance-engine.md` + `finance-engine.html` + `dados.json` + `banking-sheet.csv` (só no Modo B) + `manifest.fixed_costs_monthly` e bloco `manifest.finance`

### Bonus Delivery · Passo 11 (Fase A) · Passo 20 (Fase B) · apelido antigo: 05 <!-- gen:skill-header:bonus-delivery -->
**Trigger:** `"bonus delivery"` / `"bônus"`
Geração do asset de bônus de ecom + delivery. A DEFINIÇÃO do bônus continua na skill `offer-builder`; a `bonus-delivery` gera o ASSET (PDF/e-book/checklist) e rastreia access rate. Tipos primários de ecom: gift-with-purchase (GWP, threshold de cart subtotal vindo do AOV, take-rate como KPI), free e-book/guide toward dream outcome, free complementary SKU, free gift wrapping (Q4). A entrega do email integra com a skill `retention-engine` (via `delivery_trigger`); a config de GWP integra com a checkout-aov (é config de loja). **Fase A (pré-launch, logo após a `checkout-aov`, antes da retenção Fase A — só se a oferta tem bônus):** gerar assets + configurar GWP/entrega — todo bônus prometido na PDP precisa existir antes do primeiro ad (a `consistency-audit` verifica no gate). **Fase B (pós-launch, junto da Fase B da `retention-engine`):** tracking de take-rate/access rate.
**Output:** `bonus-delivery/bonus-delivery.md` + `bonus-delivery.html` + `dados.json` (log de entrega) + `bonuses/[bonus-id]/`

### Copy Engine · Passo 6 · apelido antigo: 06 <!-- gen:skill-header:copy-engine -->
**Trigger:** `"copy"`
Headlines ("Process of 100" de Caples). Lead types por awareness stage. Hero sections, bullets, social proof, FAQ, urgency, email hooks.
**ETAPA 2.5 obrigatória — Swipe Modeling:** antes de escrever, a skill escolhe **1 espécime primário** (opcionalmente 1 secundário) no catálogo `.claude/lib/swipe-models/specimens.json` cruzando `page_type` × awareness × sophistication × vertical, puxa a anatomia da peça na base pela `best_query` do espécime, e monta o `specimen_block_map` — a sequência de blocos que a copy vai seguir. Regra inegociável: modela-se **estrutura e mecânica, nunca conteúdo** (copiar frase, claim ou nome de mecanismo é plágio).
**Revisão:** 7 sweeps Aura (1-7) + **sweep 8** (força: claim hedged vira claim direto com a prova ao lado — nenhum sweep suaviza ou insere aviso) + **sweep 9** (markup audit — auditoria estrutural em 5 camadas a partir do nó `auditoria` do mesmo JSON: estrutura + 4 U's, 4 emoções, lead de 4 passos, psicologia, oferta/preço, com o loop `Objection → Claim → Proof → Benefit` rastreado parágrafo a parágrafo e a folha de 12 defeitos. Headline que reprova em 3 dos 4 U's e falha em ideal prospect ou big promise = reescrever o lead antes de auditar o corpo).
**Output:** `copy-engine/copy-engine.md` + `copy-engine.html` + `dados.json`

### Storefront · Passos 7 a 10 · Page Design → Page Build → Tracking Setup → Checkout & AOV · apelidos antigos: 07a → 07b → 07c → 07d <!-- gen:skill-header:page-design,page-build,tracking-setup,checkout-aov -->
**Trigger:** `"page"` / `"tracking"` / `"checkout"`
A fase storefront monta a loja inteira: página, deploy, tracking e AOV. Arquitetura **HTML-first determinística** — o design nasce in-session, vira a fonte única de verdade visual, e a conversão pra Liquid é por código, não por reasoning. Mata o drift entre o que o membro aprova e o que vai pro ar.
- **`page-design` — Page Design:** PLAN adaptativo de sections (page_type por três sinais: awareness_level de Schwartz, lead_type da copy e o formato de landing dos concorrentes escalados) + brand signals (tipografia abrindo com duas famílias sugeridas, cor pela cascade, os dois provados na mesma comparadora) + design HTML-first por uma de três rotas que o membro escolhe (do zero no canvas do Claude Design, clone de uma página salva com o SingleFile, ou quebra-cabeça de seções a partir de várias referências), todas gerando a página inteira como HTML+CSS self-contained com a copy real já inserida e todas passando pela mesma régua de design (tipografia, ritmo e espaço, cor, movimento e os sinais de "feito por IA"), pontuada item a item no self-review visual e bloqueante. No checkpoint, a skill oferece uma vez a segunda opinião no Codex (opcional): um briefing autossuficiente que o membro cola lá, e as duas versões pontuadas no mesmo placar, coluna a coluna, com recomendação e motivo. O membro aprova esse HTML ANTES de qualquer Liquid existir. **Output:** `page-plan.json` (com bloco `strategy`), `design-system.md/html`, `design/page.html` (aprovado), `design-tokens.json`, `design-signals.json`
- **`page-build` — Page Build:** compile determinístico HTML→Liquid via `liquid-converter.py` (conversor canônico), populate `templates/page.[produto].json` com blocks/block_order/settings preenchidos com a copy real, gate de performance budget, deploy seguro (duplicate → pull --nodelete → cp → push --allow-live --nodelete) + marker verification + smoke test
- **`tracking-setup` — Tracking Setup:** Meta Pixel + Conversions API (CAPI), valida EMQ ≥ 6/10 (Event Match Quality, escala 0-10 do Events Manager), escolhe o analytics stack por stage (Meta App / Wetracked / Triple Whale / Aimerce). Destrava os pré-flights de tracking das skills `creative-engine` e `ad-strategy`. **Output:** `tracking-setup/tracking-setup.md/.html` + `dados.json` + estado no manifest (bloco `tracking`: `tracking_ready`, `analytics_stack`)
- **`checkout-aov` — Checkout AOV:** post-purchase upsell (one-click), cart bump, bundle/quantity-break, free-shipping threshold, checkout trust. Consome os bumps/upsells já definidos no `offer-builder/dados.json`. Caminho real Shopify: Functions (cart transform / discount), post-purchase extension (Checkout UI) ou apps equivalentes. **Output:** `checkout-aov/checkout-aov.md/.html` + `dados.json` + `manifest.aov_baseline` (quando a config foi aplicada na loja)

### Creative Engine · Passo 13 · apelido antigo: 08 <!-- gen:skill-header:creative-engine -->
**Trigger:** `"creatives"`
Pipeline completo de briefing. Começa perguntando a **rota de produção** (A: gerar com IA · B: modelar concorrente e montar clipes · C: mix) e gera conceitos a partir das 3 verticais de pesquisa (competitiva, consumidor, interna). Cada conceito sai como um **pack 3-2-2** (3 criativos + 2 primary texts + 2 headlines) e ocupa 1 ad set próprio na estrutura da `ad-strategy`.
**O tamanho do batch vem da capacidade de teste, não do stage do membro** — `max_assets = budget diário ÷ target CPA` (cânone `.claude/lib/ad-taxonomy/README.md` §1, lido de `ad-strategy/dados.json.test_capacity` quando existe). Cada conceito declara o método de teste do §7 (Marksman = 3 ângulos distintos dentro do pack; Sniper = 1 ângulo em 3 execuções; toda iteração é Sniper), o **ângulo como frase de razão de compra** (a embalagem fica separada no `concept_type`) e a zona emocional em Valence × Intensity.
ETAPAs: detecção de material, ideação nas 3 verticais, regras estruturais, briefings com script segundo a segundo, entregáveis ramificados (prompts de IA por clipe na rota A / EDL de montagem na rota B), LP congruency mapping, hooks bank, DNA registry load/extract, passada de estilo + limpeza de metadados (todo criativo passa pelo Limpador de Metadados antes do upload — regra 12; renders do Higgsfield MCP saem limpos e renomeados `asset-xxxx`).
**Enrichment opcional:** quando MCP TrendTrack conectado, Hooks Bank ganha archetypes vencedores reais; quando o MCP da Higgsfield está conectado, a skill pode renderizar os vídeos in-session (sempre confirmando antes de gastar créditos).
**Output:** `creative-engine/creative-engine.md` + `creative-engine.html` + `dados.json` + 1 briefing por conceito (`concept-NN.md/html`) + `prompts/` (rota A) ou `concept-NN-edl.md` (rota B) + `hooks-bank.md`

### Agentic Readiness · Passo 14 · apelido antigo: 07e <!-- gen:skill-header:agentic-readiness -->
**Trigger:** `"agentic readiness"` / `"aeo"` / `"ai visibility"`
Checklist de descoberta por agentes de compra com AI (ChatGPT, Perplexity, Google AI Mode, Copilot). Roda depois do deploy (`page-build`) — na prática, depois dos criativos — e antes do gate de launch (`consistency-audit`). Verifica na loja VIVA: canal Agentic Storefronts + 3 policies, Knowledge Base app populado, dados estruturados da PDP (GTIN, ratings, FAQ/shipping/return — audita o que a camada GEO da `page-build` injetou), bloco de specs legível por agente, robots.txt liberando OAI-SearchBot/ChatGPT-User/PerplexityBot/ClaudeBot/Google-Extended, `/llms.txt` (nativo ou override), registro no Perplexity Merchant Program e qualidade do feed do Merchant Center. Fecha com score de AI visibility. **Não consulta a base Aura** (não há domínio de AEO lá — fontes são docs oficiais + verificação direta). Checklist barato de 1×, vale pra todo stage.
**Output:** `agentic-readiness/agentic-readiness.md` + `agentic-readiness.html` + `dados.json` + bloco `agentic` no manifest (lido pela `consistency-audit` como contexto e pela `scale-engine` como fonte incremental de tráfego)

### Consistency Audit · Passo 15 · apelido antigo: 09 <!-- gen:skill-header:consistency-audit -->
**Trigger:** `"consistency audit"` / `"audit"`
Cross-phase drift detection: mecanismo, awareness stage, VOC, oferta concordam entre todos os artefatos (skills `market-research` → `competitor-analysis` → `offer-builder` → `copy-engine` → `page-design`/`page-build` → `creative-engine`). Cobertura de VOC, garantia/bônus/urgência iguais entre oferta, página, checkout e ads. Roda ANTES do launch, conferindo a página já no ar + criativos + oferta.
**Vira gate de launch:** em `BLOCK`, a `ad-strategy` aborta (só prossegue com pedido explícito do membro); a `retention-engine` bloqueia por default mas oferece prosseguir com `skipped_preflight` reconhecido (filosofia never-stuck). A página existir (`page-build`) não gasta dinheiro; os ads (`ad-strategy`) sim — por isso o gate fica antes da `ad-strategy`, não do deploy da página.
**Output:** `consistency-audit/consistency-audit.md` + `consistency-audit.html` + `dados.json` com `launch_recommendation`

### Ad Strategy · Passo 16 · apelido antigo: 10 <!-- gen:skill-header:ad-strategy -->
**Trigger:** `"ad strategy"`
Pre-flight pra Pixel/CAPI/produto live/criativos prontos. One Campaign Method na forma vigente: **1 campanha com CBO → N ad sets broad/Advantage+ (1 ad set = 1 conceito) → 3 criativos + 2 primary texts + 2 headlines cada**, criada em PAUSED via Meta MCP (o membro revisa e ativa).
**Quantos ad sets sobem é conta, não preferência** (cânone `.claude/lib/ad-taxonomy/README.md` §1): `max_assets = budget diário ÷ target CPA` e `max_adsets = budget diário ÷ (3 × target CPA)`, com piso operacional de US$ 100-150/dia, teto de ~3× target CPA por ad set e máximo de 5 ad sets de teste abaixo de US$ 1k/dia. O batch da `creative-engine` pode trazer mais conceitos do que o budget consegue ler — o excedente vai pra fila do batch seguinte, nunca dilui o teste.
Método de teste Marksman ou Sniper (§7 — Marksman acontece DENTRO de um ad set, com 3 ângulos no mesmo pack, não entre ad sets). Naming convention, UTM schema, warmup de conta nova, cadência quarta→domingo, 3 dias sem mexer.
**Proteções (§6):** Automated Rule com condição de performance é recusada pelo Meta em campanha com CBO — não existe PGS aqui. O que entra: `ad set spending limit → daily maximum` (~3× target CPA) criado junto do ad set, mais as **duas automações de proteção obrigatórias** — (a) spend 5× em 24h → pausar; (b) URL de destino ≠ domínio da loja → desligar — que **nascem desativadas** pro membro ativar. Kill e escala continuam sendo leitura das skills `ad-analysis` e `scale-engine`, nunca regra automática.
Confirma o analytics stack gravado pela `tracking-setup` em `manifest.tracking` (a escolha da stack é da `tracking-setup`, não desta).
**GATE skill `consistency-audit`** roda no pre-flight.
**Output:** `ad-strategy/ad-strategy.md` + `ad-strategy.html` + `dados.json` (com `test_capacity` inteiro e auditável, `ad_sets[]` e `protections`) + manifest `10_campaign_name` / `10_campaign_id` / `10_ad_set_ids` (um por conceito — a `ad-analysis` puxa insights por ID)

### Ad Analysis · Passo 17 · apelido antigo: 11 <!-- gen:skill-header:ad-analysis -->
**Trigger:** `"ad analysis"`
Lê a estrutura da `ad-strategy` em DOIS níveis: por **conceito** (o ad set — onde o CBO concentra gasto é o sinal) e por **criativo** (o ad). 4Pi (Spend, Frequency, CPM, Cost per Result). 19-Point Loser Diagnostic.
**Classifica cada criativo nas 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2** — `loser` · `kpi_winner` · `spend_winner` · `breakthrough`. Só `breakthrough` (KPI do AD melhor que o KPI da CAMPANHA **e** puxando spend) libera escala e reciclagem; `kpi_winner` bate o KPI sem puxar spend e é tratado como **loser para decisão**. Réguas de kill do §3 (conta madura: ad set após 7 dias sem spend e sem KPI; conta nova: 8× target CPA sem purchase; ad novo overspendando: 24-48h de carência) e Hook rate / Hold rate do §4 pra dizer ONDE o criativo falhou.
**Gate de unit economics:** nenhuma recomendação de cortar spend por queda de ROAS sai sem aplicar `.claude/lib/unit-economics/README.md` §4 com os custos fixos na mesa — sem eles, a saída é a pergunta ("quanto você tem de custo fixo por mês?"), não a instrução de corte.
**Enrichment opcional:** quando MCP TrendTrack conectado, `scan_ad` faz benchmark dos breakthroughs e `daily_radar` monitora concorrentes.
**Output:** `ad-analysis/ad-analysis.md` + `ad-analysis.html` + `dados.json` (última análise) + `[YYYYMMDD]-analysis.md/html` (histórico)

### Scale Engine · Passo 18 · apelido antigo: 12 <!-- gen:skill-header:scale-engine -->
**Trigger:** `"scale"`
Escala vertical governada pelo **Scaling Protocol** do cânone `.claude/lib/ad-taxonomy/README.md` §5 — a espinha única de toda subida e descida: dois gates cumulativos pra subir (48-72h acima do target **e** ≥60% das purchases em 7-day click), passo de **+20%** repetível a cada 24h enquanto os gates seguram, **−20%** abaixo do breakeven, e a **regra de reset da meia-noite** (o budget do dia seguinte é ~50% do que foi REALMENTE gasto, nunca do nominal — sem isso o Meta faz pacing pro nominal inteiro e a escala vira queima de caixa).
As 3 escolas de gestores de tráfego (A cost-cap duplication + surf, B bid cap, C budget-doubling) são **variantes de intensidade dentro do protocolo**, recomendadas por member-stage — nenhuma dispensa os gates.
Escala só abre com **breakthrough** (§2): `kpi_winner` não conta. A promoção é o **ABO paralelo** — cada breakthrough ganha 1 ad set próprio em campanha ABO a ~10% do budget diário da campanha principal, mantendo o ad original rodando no CBO; o **champions ad set foi aposentado** em favor dessa rota (`champions[]` permanece só como campo de compatibilidade).
Horizontal scaling por diversidade de criativo (+ referral de agentes de AI como fonte incremental quando a `agentic-readiness` marcou a loja como pronta). Graduação pra Advantage+ Sales acima de US$ 1k/dia sustentado. Cash flow e projeções 30/60/90. PSM como diagnóstico (lê `manifest.psm_real`, não recomputa). Antes de qualquer corte de spend por queda de ROAS, aplica `.claude/lib/unit-economics/README.md` §4. Fecha ciclo de volta pra `creative-engine` quando o gargalo é criativo.
**Output:** `scale-engine/scale-engine.md` + `scale-engine.html` + `dados.json` + `scale-directives.md`

### Retention Engine · Passo 12 (Fase A) · Passo 19 (Fase B) · apelido antigo: 13 <!-- gen:skill-header:retention-engine -->
**Trigger:** `"retention"` / `"email flows"` / `"klaviyo"`
ESP identificado. Fluxos base: welcome series, abandoned cart, post-purchase, win-back, replenishment. **Fase A (pré-launch, depois da `checkout-aov`/`bonus-delivery` e antes dos criativos):** flows de recuperação — abandoned cart + post-purchase. É infraestrutura de cash flow do launch, não campanha de email: operador de elite nunca liga tráfego pago sem abandoned cart flow (a receita mais barata que existe, custa zero no free tier do ESP). **Fase B (pós-launch, ≥50 compras):** win-back, replenishment e segmentação. Campanhas/newsletters continuam sempre pós-launch.
**GATE skill `consistency-audit`** no pre-flight da Fase B (a Fase A roda antes de a `consistency-audit` existir).
**Setup pipeline:** Klaviyo MCP oficial (`mcp__klaviyo__`) cria os flows direto, SEMPRE em draft → fallback assets HTML + setup-guide (único caminho pra Omnisend/MailerLite/Shopify Email). Ver §12.4.
**Enrichment opcional:** `analyze_shop_emails` (TrendTrack) calibra timing dos fluxos.
**Output:** `retention-engine/retention-engine.md` + `retention-engine.html` + `dados.json` + `[fluxo]/`

### Content Recycler · Passo 21 · apelido antigo: 14 <!-- gen:skill-header:content-recycler -->
**Trigger:** `"content recycler"` / `"recycle [id]"` / `"recycle breakthrough"`
**O gatilho é `breakthrough`, não "winner" genérico.** Lê a classificação que a skill `ad-analysis` gravou (`breakthroughs[]`, espelhado em `manifest.breakthroughs[]`) e nunca a recomputa. `kpi_winner` **não entra** — o cânone `.claude/lib/ad-taxonomy/README.md` §2 o trata como loser para decisão (bateu o KPI com pouco spend, não provou nada em escala). `spend_winner` entra pela porta estreita: só o Movimento 1 (iteração), porque o cânone manda iterar, não escalar.
Extrai a essência e — acima dela — o **framework que viaja** (`framework_template` + `psychological_mechanism`): o padrão por trás do script, não o script.
**Trilha 1 — Amplificação (default, roda primeiro):** 6 movimentos pra extrair mais spend lucrativo do que já provou escalar — (1) iterar pelos 4 elementos (ângulo, mecanismo, autoridade, avatar), (2) portar o ângulo pra outros formatos, (3) LP/prelander dedicada, (4) portar pra Axon/AppLovin e TikTok (9:16 + end card, régua de US$ 250-1.000/dia por 60-90 dias), (5) duplicar em ad set ABO próprio a ~10% do budget da campanha principal, (6) devolver como creator report. A skill **especifica**; quem executa é a `creative-engine` (criativo), a `page-design`/`copy-engine` (página e copy) e a `scale-engine` (escala).
**Trilha 2 — Derivadas de formato (sob pedido):** as 9 peças de canal próprio (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad), agora enquadradas como jogada de **marca e LTV**, não de performance — quem escala a conta é a Trilha 1. Engine e specs dos formatos vivem na lib `.claude/lib/content-recycler/` (`recycler.md` + `formats.json`).
**Output:** `content-recycler/content-recycler.md` + `content-recycler.html` (índice) + `[source-id]/` com `essence.json`, `amplification-plan.md/.html`, `creator-report.md/.html` e — se a Trilha 2 rodou — 9 `.md` + 9 `.html`

### Creator Engine · Lateral · apelido antigo: 16 <!-- gen:skill-header:creator-engine -->
**Trigger:** `"creators"` / `"ugc"` / `"seeding"` / `"whitelisting"` / `"ambassador"`
A operação completa de conteúdo humano — content é o arquivo bruto, creative é o content editado, e sem abundância de conteúdo não há volume de teste. **Fase A — Content Engine (paralela à `creative-engine`, pode começar antes do launch):** product seeding (enviar produto de graça em troca de conteúdo, em plataforma tipo Insense ou por outreach manual), casting com diversidade de creator amarrada aos sub-avatares da `market-research`, framework de brief (nunca script fechado), B-roll de referência, follow-up e coleta, corte de cada vídeo em 3 hooks e o pipeline TikTok Shop como fábrica de volume. O objetivo da Fase A é encontrar **um brand ambassador**, não um winning ad de primeira (isso é bônus). **Fase B — Performance Program (SÓ depois de breakthrough confirmado pela `ad-analysis`):** o creator vencedor sobe de degrau — contrato recorrente, escada de embaixador com comissão em degraus, whitelisting (rodar ads do perfil do creator — só de quem já tem breakthrough com a marca, e só com os ads DELE), partnership ads, raw content campaign, creator farming e recrutamento pago de afiliados.
**Fronteiras:** a `creative-engine` continua dona do QUE dizer (conceitos, roteiros, produção IA); esta skill é dona de QUEM grava e da relação com quem grava. Não cria campanha nem mexe em budget (`ad-strategy`/`scale-engine`), não classifica criativo (`ad-analysis`), não recicla breakthrough (`content-recycler`). Material voltado ao creator (brief, mensagem, contrato, report) sai sempre em inglês US; números de remuneração nunca se inventam.
**Output:** `creator-engine/creator-engine.md` + `creator-engine.html` + `dados.json` + `briefs/` + `outreach/messages.md` + `contracts/` + `roster.csv` + bloco `creator` no manifest

### Promo Engine · Lateral · apelido antigo: 17 <!-- gen:skill-header:promo-engine -->
**Trigger:** `"black friday"` / `"bfcm"` / `"promo"` / `"sale"` / `"q4"` / `"flash sale"`
Dona da janela promocional de ponta a ponta (Q4/BFCM, datas sazonais, flash sales) — dispara por época ou pedido, uma rodada por janela. Calendário da janela (começar cedo é a tese central), preparação (momentum do evergreen, decisão de lead-gen VIP pelo critério de returning customers, estoque via `sourcing`, backups via `ops-engine`), oferta da promo (hierarquia de ofertas BFCM, store credit, stacking e linguagem) e o **gate inegociável**: recalcular o breakeven ROAS e o CPA-alvo com a margem promocional ANTES de ligar qualquer campanha — sem os números recalculados, a skill PARA (é o erro nº 1 da temporada: oferta melhor com o mesmo ROAS-alvo de antes = mais receita, menos lucro).
**Execução:** Promo Campaign (Broad/WARM60/HOT90) em paralelo ao evergreen intocado, criativos "best ad + banner" via handoff pra `creative-engine`, calendário de email/SMS que a `retention-engine` transforma em assets (flow nunca desliga durante campanha — se adapta), surf scaling e reset da meia-noite pelo cânone ad-taxonomy §5 (promo com data-fim é a exceção (a) do protocolo: entra direto no budget planejado), tudo logado no ad-log. **Aterrissagem:** regra de fim por horário, volta pro evergreen, leitura pós-promo com a `ad-analysis` e a `finance-engine`, cofre sazonal de winners pro revival no ano seguinte. Os números da janela vivem em `manifest.promo` e morrem com ela — nunca sobrescrevem o `target_cpa`/`breakeven_roas` do evergreen.
**Output:** `promo-engine/promo-engine.md` + `promo-engine.html` + `dados.json` + bloco `promo` no manifest

### Team Engine · Lateral · apelido antigo: 18 <!-- gen:skill-header:team-engine -->
**Trigger:** `"contratar"` / `"time"` / `"equipe"` / `"hiring"` / `"quem contratar"`
Decide QUANDO contratar (pela restrição real do negócio, nunca por desespero — contrata-se porque QUER, nunca porque PRECISA; bad hire custa ~15× o salário anual da vaga), COMO contratar (scorecard antes da vaga, funil de 9 etapas, teste prático cronometrado, headhunting) e COMO rodar o time depois (onboarding de 8 semanas, KPIs por função com hit rate por editor, reviews com 9-box e PIP, incentivos, org design em engines e pods, frameworks de decisão DAI/RAPID/AAR). Desenhada pro membro em estágio scaling — pra starter/validating a resposta mais valiosa costuma ser **"ainda não — sua restrição hoje é X"**, entregue com o porquê e o sinal que reabre a conversa.
**Réguas:** nenhuma vaga sem gargalo nomeado; sucesso definido ANTES da vaga aberta (scorecard); salário, caixa e KPI real de pessoa nunca se inventam — quando a pergunta é "a folha cabe no caixa?", o número vem da `finance-engine` ou do membro. Creator ≠ funcionário: creator, afiliado e embaixador são território da `creator-engine`. Consumidora do maior bloco órfão da base (o domínio `team-hiring-ops` inteiro do kb-index).
**Output:** `team-engine/team-engine.md` + `team-engine.html` + `dados.json` + bloco `team` no manifest

### Ops Engine · Lateral · apelido antigo: 19 <!-- gen:skill-header:ops-engine -->
**Trigger:** `"backup de conta"` / `"risco"` / `"constraint"` / `"operação"` / `"continuidade"` / `"exit"`
A skill que pergunta **"o que mata esse negócio nos próximos 12 meses?"** e arma a resposta antes. Três frentes: **(1) Constraint dos próximos 12 meses** — o ÚNICO gargalo que limita o ano (estoque, caixa, plataforma ou pessoa-chave) e as prioridades organizadas em torno de removê-lo; **(2) Continuidade** — checklist de backups com status confirmado pelo membro, nunca deduzido: conta e Business Manager reserva com campanhas pré-montadas desligadas, processadora de pagamento redundante, banco e domínio reserva, pre-order pronto pra ligar como válvula de estoque e caixa, risco de pessoa-chave medido em "dores de cabeça por dólar"; **(3) Negócio como ativo** — memos de decisão (WAFM: sem memo, não há reunião de decisão), teste de moat de produto e operação exit-ready (o que um comprador auditaria). A parte de backups vale DESDE O COMEÇO — logo depois da `setup` e antes do primeiro ad, porque conta nova é a mais frágil da vida do negócio; o resto revisita por trimestre e antes de decisões grandes (escala agressiva, Q4).
**Fronteiras:** não monta a estrutura anti-ban (`setup`), não calcula caixa/runway/float (`finance-engine`), não escolhe fornecedor nem define recompra (`sourcing`), não mexe em campanha (`ad-strategy`/`ad-analysis`/`scale-engine`) — audita o status e aponta.
**Output:** `ops-engine/ops-engine.md` + `ops-engine.html` + `dados.json` + `memos/` + bloco `ops` no manifest

### Marketplace Engine · Lateral · apelido antigo: 20 <!-- gen:skill-header:marketplace-engine -->
**Trigger:** `"amazon"` / `"tiktok shop"` / `"marketplace"` / `"afiliados"` / `"expandir canal"`
Expansão de CANAL DE VENDA além do site próprio — decide quando (e se) a marca abre Amazon, TikTok Shop e programa de afiliados, e acompanha cada canal aberto. Roda um **GATE antes de qualquer tática**: Meta + site provados primeiro (breakthrough na `ad-analysis`, conta fechando na `finance-engine`) e sinal de demanda transbordando (busca de marca subindo, cliente procurando a marca na Amazon, revendedor aparecendo na listagem) — porque canal novo não conserta oferta quebrada. Sem prova, a skill roda mesmo assim, mas o veredito só pode sair `not_yet` ou `blocked_pending_proof` — a resposta honesta "ainda não, e falta X" é output válido.
**Os canais:** Amazon como captura da demanda que o ad já criou (SEO da listagem, defesa de marca, lances baixos, preço riscado, custom link, TACOS); TikTok Shop como canal de venda operado por afiliados (comissão orgânica vs de ads, samples, GMV — o conteúdo em si é da `creator-engine`); afiliados via tráfego pago (funil "apply to be brand ambassador", comissão decrescente por faixa) e clientes virando afiliados automaticamente. **Fronteiras:** recrutar/gerenciar creators é da `creator-engine`; portar campanha paga pra AppLovin/Axon/TikTok Ads é da `content-recycler` (Movimento 4); a conta financeira por canal (margem com comissão e fee dentro) é da `finance-engine`. Fees reais, busca de marca e GMV nunca se estimam — o membro cola o que vê no painel.
**Output:** `marketplace-engine/marketplace-engine.md` + `marketplace-engine.html` + `dados.json` + bloco `marketplace` no manifest

---

## 5. Sistema de libs

Libs reutilizáveis em `.claude/lib/`.

| Lib | Função | Usada por |
|---|---|---|
| **ad-taxonomy** | **Cânone de classificação e capacidade de teste.** Capacidade (`assets = budget diário ÷ target CPA`, piso US$ 100-150/dia, teto ~3× target CPA por ad set, máx. 5 ad sets abaixo de US$ 1k/dia) + estrutura CBO com 1 ad set = 1 conceito; as 4 classes de resultado (loser · KPI winner · spend winner · breakthrough); réguas de kill; Hook/Hold rate; Scaling Protocol + ABO paralelo (champions ad set aposentado); o que pode e não pode ser automatizado (condição de performance é recusada em CBO; 2 automações de proteção obrigatórias); métodos Marksman/Sniper/Shotgun e a distinção ângulo ≠ conceito. Nenhuma skill redefine isso localmente. | `creative-engine`, `ad-strategy`, `ad-analysis`, `scale-engine`, `content-recycler`, `promo-engine` + rules `member-stage-awareness`/`troubleshooting-patterns` + receitas de automação |
| **unit-economics** | **Cânone de margem, CAC e decisão de spend.** Stack completo de custos variáveis e a regra de nomenclatura (nunca chamar de "Lucro" o que não subtraiu custos fixos); first order vs repeat order; CAC ≠ CPA (CAC vem do Shopify, `new customer = TRUE`); a **espiral do ROAS** — cortar spend por queda de ROAS pode aumentar o prejuízo, então nenhuma recomendação de corte sai sem os custos fixos na mesa. O §5 declara a **skill `finance-engine`** como dona do modelo completo (4 alavancas, cohorts, ciclo de caixa). | `offer-builder`, `ad-analysis`, `scale-engine`, `finance-engine` |
| **ad-log** | **Cânone do registro de mudanças na conta.** `workspace/[produto]/ad-log.md`, **append-only**, uma linha por mudança executada (entidade, mudança com valores antes → depois, executor, motivo curto) — separa o que foi FEITO do que foi lido (as análises datadas da `ad-analysis` registram leituras). Escrito no momento da execução; mudança executada e não logada é bug de processo. | Escrevem: `ad-strategy`, `scale-engine`, `promo-engine` + receitas de automação. Leem: `ad-analysis` (SEMPRE, no início da análise) e `scale-engine` (antes de escalar — o gate de 24h entre degraus é verificado ali) |
| **auto-update** | Protocolo completo do update do framework que o agente segue quando o hook `post-start.sh` avisa que algo bloqueou o update (mudanças locais, branch errada, fetch falhou, histórico divergiu) ou quando o membro pede "aura, resolve o update". O CLAUDE.md traz só o resumo de cinco linhas. | Agente da sessão (auto-update); hook `post-start.sh` |
| **swipe-models** | **Camada de modelagem por espécime.** `specimens.json` cataloga 12 espécimes estruturais de swipe files reais, cada um com seletor (`page_type` × awareness × sophistication × vertical), `best_query`, `regra_diagnostica`, `blocos_chave` e `base_empirica`. A skill `copy-engine` escolhe 1 primário (+1 secundário opcional) na ETAPA 2.5 e modela a ESTRUTURA — nunca o conteúdo. O nó `auditoria` vira o sweep 9 (markup audit: 4 U's, 4 emoções, lead de 4 passos, loop Objection→Claim→Proof→Benefit, folha de 12 defeitos). | `copy-engine` (dono), `offer-builder` e `ad-analysis` (diagnóstico) |
| **content-recycler** | Engine prompt-driven da **Trilha 2** da skill `content-recycler` (as 9 derivadas de formato). Arquivos: `recycler.md` + `formats.json`. A Trilha 1 (amplificação) não vem daqui — vem do cânone `ad-taxonomy`. | `content-recycler` |
| **creative-dna** | Cross-product DNA registry. Skill `creative-engine` salva padrões abstratos; próxima execução em outro produto carrega e adapta. | `creative-engine` |
| **design-presets** | **Paleta e tipografia da página: gerador de paletas, os 8 presets que servem de base e as 2 famílias sugeridas.** O `palette_engine.py` devolve exatamente 3 candidatas pro produto (nome curto, motivo em uma frase, relação de matiz declarada, paleta role-tagged e os trios R,G,B da comparadora), garantindo antes de imprimir saturação viva, harmonia que bate com a distância real de matiz, contraste WCAG AA e as 3 distintas entre si; paleta que não passa é corrigida ou o script sai com erro. Cada candidata herda de um preset de `presets.json` o perfil de claridade, a tipografia e a forma, e troca só o matiz — e a mesma entrada devolve sempre a mesma saída. Caminho 4 (último) da cascade de brand signals; os presets não são mais um menu. O bloco `suggested_typefaces` de `presets.json` registra as 2 famílias que a skill sugere antes de qualquer outra (uma do Google Fonts, uma que o membro baixa da fundição), e o `local_fonts.py` cuida do arquivo baixado: lê o peso real de cada um pelo metadado, escolhe o formato e emite o `@font-face` marcado com `data-aura-fonts` em três modos (arquivos ao lado do HTML de design, asset do tema, ou a fonte embutida em base64 pra quando o arquivo precisa abrir longe da pasta). Testes em `tools/tests/test_palette_engine.py` e `tools/tests/test_local_fonts.py`. | `page-design`, `page-build` |
| **hook-taxonomy** | Taxonomia de hooks (Problema / Resultado / Curiosidade / Prova Social). | `creative-engine` |
| **kb-index** | Índice permanente das 1.309 entradas de frameworks nomeados da base, em 19 domínios (alguns sistemas aparecem em mais de um domínio quando servem a skills diferentes), com a `best_query` exata de cada um e o campo `skills` (ids do registro, derivados do texto de `use_in_skill` pelo `normalize_index.py`). As skills consultam o índice pelo `kb_lookup.py --skill <id>` (lista por domínio com a `best_query` de cada entrada e o total no fim) e puxam os sistemas por nome, nunca por query genérica; o `check_embedded_queries.py` confere que as queries embutidas nas skills continuam no índice. | Todas as skills que consultam a base |
| **mcp-detect** | Fonte única de verdade dos prefixos de tool MCP detectáveis (`mcp__trendtrack__`, `mcp__meta__ads_*`, `mcp__meta-ads__`, `mcp__refero__`, `mcp__klaviyo__`, `mcp__shopify_dev__`, `mcp__stripe__`, `mcp__claude_ai_Notion__`/`mcp__notion__`) + convenção de log `source`. | `product-research`, `tracking-setup`, `ad-strategy`, `ad-analysis`, `retention-engine` + receitas de automação |
| **prompt-directors** | Directors de prompt pra ferramentas externas (Higgsfield Marketing Studio). | `creative-engine` (ETAPA 5.7) |
| **shopify-section-patterns** | 6 padrões de section Liquid endurecidos em produção (marquee infinito por JS em pixels, sticky add-to-cart com IntersectionObserver, gradiente de hero com easing, badges sobre imagem, drawer enriquecido via `::part`, fonte universal incluindo drawer) + o sistema de tokens de paleta em trios R,G,B. Formato: problema → solução → código de referência → armadilhas. | `page-design` (clone fiel), `page-build` |
| **theme-verify** | Gate de verificação da página no ar via Playwright: `verify_page.py` (overflow/seções/console, desktop+mobile), `font_census.py` (censo de fonte computada — declarar não é carregar), `motion_check.py` (continuidade de animação com `--throttle` 3G + cache frio, o cenário que revela bug de mobile real). Mesmo venv da web-fetch. | `page-build` (6.8/6.11) |
| **web-fetch** | Fetcher Playwright de navegador real (`fetch.py --mode text\|reddit\|reviews`) pro cascade resiliente da rule `resilient-fetch` (WebSearch → WebFetch → fetcher). Reddit via redlib, reviews com scroll de widgets lazy. | `setup`, `market-research`, `competitor-analysis` + qualquer skill que minera web (rule `resilient-fetch`) |
| **workspace-index** | `build_index.py` regenera o painel `ABRIR-AQUI.html` do produto; `workspace-layout.md` define a estrutura canônica do workspace. | Todas as skills (no SALVAR) |
| **trendtrack-integration** (opcional) | Integração read-only com MCP TrendTrack (30+ tools; `search_ads` com os filtros do Explorer é o motor de descoberta da `product-research`). Detecção runtime: tools com prefixo `mcp__trendtrack__`; checa créditos antes de gastar. Sem MCP, a `product-research` explica a pesquisa manual no browser. | `product-research`, `competitor-analysis`, `creative-engine`, `ad-analysis`, `retention-engine` |
| **refero-integration** (opcional) | Integração com Refero Design MCP (`fidgetcoding-refero-mcp`). Catálogo curado de ~200 design systems premium (Cursor, Linear, Vercel, Notion, Stripe). 6 tools (`refero_search`, `refero_get`, `refero_similar`, `refero_list`, `refero_design_md`, `refero_refresh`). Fonte de brand signals (não decisão visual) que alimentam a rota de design escolhida. Cascade na `page-design` ETAPA 2 (Brand Signals): Refero → screenshot→visão → `tools/design-clone/` → manual. | `page-design` (ETAPA 2) |
| **automations/ (Meta + Shopify)** | Vive em `.claude/automations/`. Cascade resiliente pra Meta Ads: **(1)** MCP oficial da Meta `mcp.facebook.com/ads` (open beta desde 2026-04-29, tools `mcp__meta__ads_*`, 29 tools); **(2)** MCP Pipeboard 3rd-party (tools `mcp__meta-ads__*`) como fallback automático; **(3)** paste manual. Receitas: `sync-campaign-from-meta.md` (única, com cascade interna oficial → Pipeboard → manual), `pause-ad-set.md`, `upload-creative-to-meta.md`, `creative-loop.md` (loop semi-autônomo: performance → DNA dos winners → variações novas → aprovação humana → upload), `full-deploy.md`, `deploy-shopify-product.md`, `create-fixed-bundles.md` (bundles fixos via Admin GraphQL `productBundleCreate`), `rotate-winning-creative.md` | `ad-strategy`, `ad-analysis` |

**Por que cascade no Meta:** o MCP oficial está em rollout gradual — algumas ad accounts aparecem "disabled" mesmo depois do setup correto. Manter Pipeboard como fallback elimina dependência da Meta liberar acesso.

---

## 6. Sistema de rules

Diretrizes em `.claude/rules/` auto-carregadas pelo Claude Code conforme contexto.

| Rule | Quando aplica |
|---|---|
| `shopify-theme-safety` | Toda operação Shopify CLI. Pull antes de edit, `--nodelete`, marker verification. |
| `iteration-driven-refinement` | Skills que geram asset. Primeira versão é draft, máximo 3 iterações. |
| `member-stage-awareness` | Toda skill. Detecta starter / validating / scaling e adapta tom. |
| `emergency-escape-paths` | ES1-ES7 cobrem pre-flights travados, workspace corrompido, etc. |
| `troubleshooting-patterns` | Quando skill não entrega. Árvore de diagnóstico estruturada. |
| `post-task-self-audit` | Toda skill peso médio/alto. 5 gates silenciosos antes de declarar "completo". Fixes inline silenciosos. |
| `report-only-results` | **NON-NEGOTIABLE.** Todo relatório salvo em `workspace/` (.md e .html). O doc contém só o resultado final — zero narração de processo/correções, zero descrição de ausências, zero referência à conversa, zero auto-referência da AI. Meta-informação vive no chat e no `dados.json`. |
| `report-language` | **NON-NEGOTIABLE.** Idioma e estilo de todo relatório interno e da conversa com o membro (`report_language` do profile; copy consumidor-final sempre em inglês; português simples e natural, sem sigla sem explicação) mais as sete regras de escrita. É a fonte única: a regra 0 do CLAUDE.md vive aqui por inteiro. Carrega em skills, templates e `workspace/`. |
| `resilient-fetch` | **NON-NEGOTIABLE.** Toda skill que busca dados na web. Cascade WebSearch → WebFetch → fetcher Playwright (`lib/web-fetch`); nunca inventar VOC/claim quando a fonte bloqueia. |
| `reverse-order-insertion` | Multi-insert safety: em arrays posicionais (`order[]`, `block_order`), inserir em ordem reversa; em edits por anchor de texto, planejar anchors únicos e disjuntos. |

**Rules são diretrizes, não código enforced.** O Claude lê e aplica. A camada real de enforcement são os hooks.

---

## 7. Sistema de hooks

Scripts em `.claude/hooks/` registrados em `.claude/settings.json`.

### post-start.sh
**Quando:** abertura de sessão Claude Code.
**O que faz toda sessão:** instala o guard `.git/hooks/pre-commit` que bloqueia mecanicamente qualquer commit com arquivos de `workspace/` (camada 2 da separação framework vs workspace — CLAUDE.md rule 11), deixa os atalhos do Limpador de Metadados executáveis e roda `python3 tools/migrate.py --all`, que aplica a cada produto as migrações de layout pendentes (silencioso quando não há nada pendente; uma linha por produto migrado).
**O que faz 1× por dia:** adiciona o alias `aura` no shell rc do membro, faz o auto-update do framework e avisa onde está o Limpador.

### post-skill.sh
**Quando:** evento `Stop` do Claude Code (o assistente terminou uma resposta).
**O que faz:** acha o produto do workspace tocado nos últimos 30 minutos (mtime do `manifest.json` ou de qualquer `<fase>/dados.json`), roda `python3 tools/aura-status.py <slug> --brief` e mostra até 10 linhas com prefixo `[aura-status]` (skills marcadas, relatórios, pontos a conferir). Silêncio quando nada mudou; cada mudança é reportada uma vez (guarda o mtime já reportado em `~/.cache/aura/`). Como texto puro no stdout de um hook `Stop` não aparece pro membro, a saída vai no campo `systemMessage` do JSON de hook. Nunca bloqueia a resposta.

---

## 8. Sistema de templates

Em `.claude/templates/`.

### aura-report-template.html
Base de todo `.html` de relatório. O `tools/render_report.py` lê o `.md` e monta o `.html` a partir daqui (o `<style>` completo, a topbar com a logo, o hero, a meta-bar, o sumário gerado dos `##`, o rodapé e o script de interação). Nenhuma skill copia o template à mão. Componentes: `section-label`, `callout`, `note`, `opportunity`, `danger`, `table-wrap`, `quote`, `pill`, `winner`, `kpi-grid`.

### aura-html-components.md
As convenções de Markdown que o `render_report.py` transforma em componentes (citação com `**Nota:**`, `**Atenção:**`, `**Oportunidade:**`, `**Risco:**` ou `**Vencedor:**`; tabela `KPI | Valor`; citação de cliente com `Tradução livre:` e `Fonte:`) e o frontmatter que alimenta a meta-bar.

### aura-logo-snippet.html
Path canônico da logo Aura. A topbar do template carrega o mesmo SVG e o render confere os dois; a logo entra em todo `.html` por esse caminho, nunca por texto.

### manifest-schema.json
JSON Schema (draft-07) pro `manifest.json`. `additionalProperties: true` — skills podem gravar campos extras. Obrigatórios: `product_slug`, `product_name`, `created_at`, `updated_at`, `skills_completed`. Quem grava o manifest é o `tools/manifest.py` (`get` / `set` / `complete` / `validate`): backup em `.manifest-backup-*`, `updated_at` automático e validação contra este schema antes de gravar (falha nova bloqueia a escrita; falha que já existia é avisada).

### schemas/<id>.dados.schema.json
Um JSON Schema (draft-07) por skill que grava um `dados.json` lido por outra skill: `market-research`, `competitor-analysis`, `offer-builder`, `copy-engine`, `creative-engine`, `ad-strategy`, `ad-analysis`, `scale-engine`, `finance-engine`, `creator-engine`, `promo-engine`, `team-engine` e `marketplace-engine`. Os campos vêm da seção de schema de cada skill; `required` só nos campos que outra skill lê; `additionalProperties: true`. O `manifest.py complete <id>` valida o `dados.json` da fase antes de marcar a skill, e o `aura-status.py` acusa arquivo que falha. Validador mínimo em `tools/schema_validate.py` (só biblioteca padrão).

---

## 9. Estrutura do workspace

Cada produto vive em `/workspace/[slug]/`.

Cada fase mora numa subpasta própria `<stem>/`, onde o stem é o id da skill, sem número. Dentro: `<stem>.html` (o que o membro abre), `<stem>.md` (o que a AI lê na fase seguinte), `dados.json` (dados estruturados) — o relatório humano leva o nome da pasta (ex.: `market-research/market-research.html`). Produto criado antes da reforma de 2026-09 tinha pastas numeradas (o apelido antigo da skill na frente do nome, guardado em `legacy_folder` no registro); o `tools/migrate.py`, chamado pelo hook de início de sessão, renomeia essas pastas e grava `framework_version` no manifest. Arquivos secundários mantêm nome descritivo dentro da pasta. Estrutura canônica completa (incl. compat com nomes legados) em `.claude/lib/workspace-index/workspace-layout.md`.

```
/workspace/produto-x/
├── ABRIR-AQUI.html                    ← PAINEL: porta de entrada do membro (gerado por build_index.py)
├── manifest.json                      ← estado central
├── brand.md  ·  brand/logo.svg        ← identidade (infra)
├── creative-dna/                      ← infra compartilhada (`creative-engine` + `ad-analysis`)
├── product-research/   → product-research.md / .html + dados.json + banco-de-marcas.md (+ .html sem Notion)
├── sourcing/              → sourcing.md / .html + dados.json   (`sourcing`, opcional — fornecedor, cotação, logística)
├── market-research/    → market-research.md / .html + dados.json
├── competitor-analysis/ → competitor-analysis.md / .html + dados.json + creative-patterns.json + creatives-inbox/
├── offer-builder/      → offer-builder.md / .html + dados.json + research-foundation.json
├── bonus-delivery/     → bonus-delivery.md / .html + dados.json + bonuses/[bonus-id]/   (2 fases: A pré-launch, B pós-launch)
├── copy-engine/        → copy-engine.md / .html + dados.json
├── page/               ← storefront (`page-design` design + `page-build` build)
│   ├── design-system.md / .html · page-plan.json (bloco strategy)
│   ├── design/page.html               ← HTML aprovado (fonte única visual)
│   ├── design-tokens.json · design-signals.json · iterations-log.json
│   ├── page-report.html                   ← página final (relatório humano da fase)
│   └── deploy-report.json · staging/
├── tracking-setup/    → tracking-setup.md / .html + dados.json
├── checkout-aov/      → checkout-aov.md / .html + dados.json
├── agentic-readiness/ → agentic-readiness.md / .html + dados.json   (pós-deploy, pré-launch)
├── creative-engine/    → creative-engine.md / .html + dados.json + concept-NN.md/html + hooks-bank + prompts/
├── consistency-audit/  → consistency-audit.md / .html + dados.json
├── ad-strategy/        → ad-strategy.md / .html + dados.json
├── ad-analysis/        → ad-analysis.md / .html + dados.json + [YYYYMMDD]-analysis.md/html
├── scale-engine/       → scale-engine.md / .html + dados.json + scale-directives.md
├── retention-engine/   → retention-engine.md / .html + dados.json + [fluxo]/   (2 fases: A pré-launch, B pós-launch)
├── content-recycler/   → content-recycler.md / .html (índice) + [source-id]/   (só depois de um breakthrough)
├── finance-engine/     → finance-engine.md / .html + dados.json + banking-sheet.csv   (consulta lateral; o .csv só no Modo B)
├── creator-engine/     → creator-engine.md / .html + dados.json + briefs/ + outreach/ + contracts/ + roster.csv   (lateral, 2 fases: A seeding/conteúdo, B performance)
├── promo-engine/       → promo-engine.md / .html + dados.json   (lateral/sazonal — uma rodada por janela)
├── team-engine/        → team-engine.md / .html + dados.json   (lateral — org, vagas, pipeline de candidatos)
├── ops-engine/         → ops-engine.md / .html + dados.json + memos/   (lateral — backups valem desde o começo)
├── marketplace-engine/ → marketplace-engine.md / .html + dados.json   (lateral — canais de venda além do site)
└── ad-log.md              ← registro append-only de toda mudança executada na conta (cânone ad-log; escrito por `ad-strategy`/`scale-engine`/`promo-engine`/receitas)
```

`/workspace/profile.md` (fora de qualquer produto) guarda dados do membro: budget, ESP, tools, mercado, idioma. Escrito pela skill `setup`, lido por todas. O **`ABRIR-AQUI.html`** de cada produto é a porta de entrada: lista cada fase, o que já foi feito e o próximo passo — toda skill o regenera ao terminar. O **`workspace/ABRIR-AQUI.html`** (painel global, `build_index.py --global`) tem um card por produto com progresso, próximo passo e pontos a conferir.

**Estado verificável.** `python3 tools/aura-status.py <slug>` (ou `--all`, `--json`, `--brief`) cruza o manifest, os arquivos da pasta e o layout canônico (a lista `writes` de cada skill no registro): fase com relatório presente ou ausente, skill marcada sem artefato e artefato sem marca (ES3), arquivo fora do layout, `dados.json` que falha no schema da fase e manifest que falha no `manifest-schema.json`. Em lista separada, avisos informativos que não contam como issue: hoje, `dados.json` sem o bloco `resumo` que o schema da fase prevê, porque a fase seguinte vai ler o arquivo inteiro. O painel lê o estado daí, e o hook `post-skill.sh` mostra o mesmo status ao fim da resposta que mexeu no produto. O manifest só muda pelo `python3 tools/manifest.py <slug> set|complete` (backup + validação), nunca à mão.

---

## 10. Convenções operacionais

### Idioma e estilo (CLAUDE.md rule 0)
- **Relatórios internos:** no idioma escolhido durante setup (`pt-BR` ou `en`).
- **Regra inteira** (termos permitidos e proibidos, português natural, sete regras de escrita): `.claude/rules/report-language.md`. O CLAUDE.md traz só o resumo.
- **Copy pro consumidor final:** sempre em inglês (mercado US padrão), independente do idioma de relatório interno.

### Uso da Base de Conhecimento (CLAUDE.md rules 1-3)
- Skills consultam `search_knowledge` silenciosamente.
- Nomes de cursos/programas internos nunca citados. Livros e autores (Schwartz, Cialdini, Hopkins, Hormozi, etc.) podem ser referenciados diretamente.

### Dual output (.md + .html) — CLAUDE.md rule 6b
- `.md` é a fonte que a AI lê na fase seguinte
- `.html` é a versão humana (browser)
- o `.html` é gerado do `.md` por `python3 tools/render_report.py <md>` (template, logo, sumário); nunca é escrito à mão

### Logo SVG obrigatório
- entra na topbar de todo `.html` pelo render, a partir do template (mesmo path de `aura-logo-snippet.html`)
- Proibido substituir por texto. Sem fallback.

### Ícones SVG, nunca emojis em UI consumidor — rule 7
- PDPs, landings, checkouts: SVGs inline (Lucide, Heroicons, Phosphor, custom)
- Exceção: relatórios internos em `/workspace/` podem usar emojis pra velocidade de escaneamento

### Copy rules — rule 8
- **8a** — minimizar em-dashes (—). Zero em headlines, ≤2 em copy longa.
- **8b** — copy agressiva, direta e sem aviso: nenhuma skill insere disclaimer, "não verificado" ou suavização de claim por conta própria; nenhuma checagem de policy ou lista de palavras roda sobre copy ou pesquisa. O membro decide o tom final.

### Self-audit silencioso obrigatório — rule 9
Antes de declarar qualquer skill "completa", 5 gates mentais rodam silenciosamente. Fixes inline sem mencionar. Surface só quando precisa decisão do membro.

### Integrações MCP opcionais — rule 10
A Aura detecta MCPs externos e enriquece skills automaticamente. **Meta MCP** (cascade oficial → Pipeboard → manual), **TrendTrack**, **Refero** e **Klaviyo** são os casos principais. Prefixos canônicos em `.claude/lib/mcp-detect/README.md`.

---

## 11. Memória persistente — registry creative-dna

Cross-product learning. A skill `creative-engine` (creatives) salva DNA toda vez que executa: hook archetypes que funcionaram, voice signatures, padrões estruturais. Próxima execução em outro produto carrega esse registry e adapta sem reinventar.

**Read/write:** via `lib/creative-dna/registry.py`. Skill `creative-engine` chama em silent steps (o "Contexto a carregar" — item 6 — carrega o dna-profile.json e enviesa a ideação desde a ETAPA 3; a ETAPA 7.6 escreve).

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
| Product Catalog (`ad-strategy`) | `ads_catalog_create`, `ads_catalog_get_*` | Integração de catálogo Shopify, monitoramento de feed |
| Accounts / Pages / Assets (3) | `ads_get_ad_accounts`, `ads_get_ad_entities`, `ads_get_pages_for_business` | Descoberta de hierarquia |
| Dataset / Pixel / CAPI Quality (4) | `ads_get_dataset_details`, `ads_get_dataset_quality`, `ads_get_dataset_stats`, `ads_get_errors` | **Exclusivo do oficial** — match quality, deduplication, errors |
| Insights / Benchmarks (7) | `ads_insights_advertiser_context`, `ads_insights_anomaly_signal`, `ads_insights_auction_ranking_benchmarks`, `ads_insights_industry_benchmark`, `ads_insights_performance_trend`, `ads_get_opportunity_score`, `ads_get_help_article` | **Exclusivo do oficial** — benchmarks por vertical, auction ranking, anomalias |

**Onde a Aura usa:**

| Skill / Receita | Tools | O que melhora |
|---|---|---|
| 11 ad analysis (ETAPA 1) | Cascade via `sync-campaign-from-meta.md` (receita única: oficial → Pipeboard → manual) | Auto-pull + market context (industry benchmark, auction ranking, opportunity score, anomalies). Compara membro vs vertical p50. |
| 10 ad strategy (pre-flight) | `ads_get_dataset_quality` | Gate de EMQ ≥ 6/10 (Event Match Quality) antes do launch |
| `pause-ad-set.md` | `ads_update_entity` (cascade) | Executa a pausa que o membro decidiu — o gatilho é humano (leitura das réguas de kill do cânone §3 pela Skill `ad-analysis`), nunca uma regra de performance |
| `upload-creative-to-meta.md` | Continua via Pipeboard/Playwright | MCP oficial não aceita arquivos locais |

**Por que o cascade importa:** o MCP oficial está em rollout gradual. Pipeboard como fallback automático significa que a Skill `ad-analysis` nunca trava.

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
| 01 product research | `search_ads` (filtros do Explorer), `lookup_filter_ids` (nicho + landing pages), `search_shops` (tráfego + Trustpilot), `scan_ad`, `check_credits` | Motor de descoberta: as duas pesquisas fixas + a ficha de cada marca saem do MCP |
| 03 competitor analysis | `brief_competitor`, `scan_ad`, `search_shops`, `find_similar_shops` | ETAPAs 1-3 se juntam em 1-2 tool calls |
| 08 creatives | `creative_inspiration_pack`, `scan_ad` | Hooks Bank com archetypes reais |
| 11 ad analysis | `scan_ad`, `daily_radar` | Benchmark de winners + loop de monitoramento |
| 13 retention | `analyze_shop_emails` | Timing dos fluxos calibrado contra concorrência |

**Padrão de detecção:** tools com prefixo `mcp__trendtrack__` → fonte primária. Ausente → fallback silencioso.

**Custos:** sistema de créditos. Quando skill planeja >5 chamadas, roda `check_credits` primeiro.

**Privacidade:** OAuth read-only. Aura não armazena tokens.

### 12.3 — Refero MCP (design system curado)

Refero é um catálogo curado de ~200 design systems de sites premium (Cursor, Linear, Vercel, Notion, Stripe, etc.). O MCP é pacote npm local (`fidgetcoding-refero-mcp`). A Aura usa na skill page-design ETAPA 2 (Brand Signals) pra extrair signals coerentes de cor/typography/spacing — esses signals alimentam a rota de design escolhida na ETAPA 3, que gera o HTML da página (a fonte única de verdade visual). O Refero é fonte de signals, não decisão visual.

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

**Cascade de brand signals na skill page-design ETAPA 2** (a de cor, sub-etapa 2.2; a tipografia é decidida antes, na 2.1, e vence a família que qualquer caminho trouxer)**:** Refero → screenshot→visão (membro tira print full-page da loja de referência e o Claude lê a imagem com visão nativa — imune a Cloudflare/JS/markup bagunçado; fallback primário de inspiração) → `tools/design-clone/` (Playwright, caminho 3 opcional pra hex exato) → gerador de 3 paletas candidatas (`palette_engine.py`, com os 8 presets como base), provadas na comparadora.

**O design é HTML-first, por uma das três rotas da ETAPA 3** (do zero no canvas do Claude Design, clone com o SingleFile, quebra-cabeça de seções), e o resultado é a página inteira como HTML+CSS self-contained com a copy real. Refero entra antes, só como input de signals pra rota escolhida.

### 12.4 — Klaviyo MCP oficial (criação de flows de retenção)

O Klaviyo publicou um MCP oficial (25 tools, 2026) que a skill `retention-engine` usa como caminho preferencial pra criar os flows de lifecycle direto na conta do membro — com contrato de API estável, sem scraping e sem cookie de sessão (o caminho de session-cookie foi REMOVIDO por risco de segurança).

**Padrão de detecção:** tools com prefixo `mcp__klaviyo__` na sessão → Caminho 1 (criação direta via MCP). Ausente ou falha (auth/rate-limit) → fallback silencioso pro Caminho 2: assets HTML + `setup-guide.md` que o membro importa no UI do ESP (único caminho pra Omnisend/MailerLite/Shopify Email, que não têm MCP).

**Regra inviolável:** flows criados via MCP nascem SEMPRE em draft/manual — a skill nunca ativa automaticamente (risco de spam se um email tiver bug). O membro revisa no Klaviyo UI e ativa. `source` logado no `retention-engine/dados.json`: `klaviyo_mcp` ou `klaviyo_assets_guide`.

---

## 13. Como rodar uma sessão completa do zero

Ordem canônica pra um produto novo:

<!-- gen:overview-order:start -->
1. **setup**: cria workspace, profile, manifest
   - *lateral:* **Ops Engine**: consulta lateral; a parte de backups (conta e Business Manager reserva, processadora redundante) vale desde o começo, porque conta nova é a mais frágil
2. **product research**: acha as marcas que escalam no nicho (TrendTrack), valida (Trends + Trustpilot), monta as jogadas de recombinação e salva o banco de marcas (Notion ou HTML)
   - *paralela, opcional:* **Sourcing**: fornecedor, cotação e logística; roda em paralelo aos passos 3-4 e fecha o custo real antes da oferta
3. **market research**: VOC, awareness, drivers
4. **competitor analysis**: 5-10 concorrentes, padrões, gaps
5. **offer**: mecanismo, pricing, stack, garantia, unit economics
   - *lateral:* **Finance Engine**: consulta lateral; a primeira consulta natural é logo depois da oferta (a oferta fecha a conta do negócio inteiro, com o custo fixo dentro? Modo A) e depois a cada mês fechado (Modo B)
6. **copy**: copy completa pra cada section
7. **page**: design HTML-first da página, com a copy real inserida; o membro aprova o HTML antes de qualquer Liquid existir
8. **build page**: compile determinístico HTML→Liquid + deploy seguro no Shopify
9. **tracking**: Meta Pixel + CAPI (EMQ ≥ 6/10) + analytics stack por stage
10. **checkout**: post-purchase upsell, cart bump, bundle, free-shipping threshold, checkout trust
11. **bonus delivery, Fase A**: assets + config de GWP/entrega, só se a oferta tem bônus (todo bônus da PDP existe antes do primeiro ad)
12. **retention, Fase A**: flows de recuperação (abandoned cart + post-purchase); infraestrutura de cash flow do launch, custa zero no free tier
13. **creatives**: conceitos com briefings, em pack 3-2-2; o número sai da capacidade de teste, não do stage
   - *lateral:* **Creator Engine**: consulta lateral em duas fases; a Fase A (seeding + conteúdo humano) roda junto dos criativos e antes do launch, e a Fase B (contrato recorrente, whitelisting, partnership ads) só depois de um breakthrough confirmado pela análise de ads
14. **agentic readiness**: checklist de descoberta por agentes de AI na loja viva
15. **consistency audit**: cross-phase drift check (gate de launch)
16. **ad strategy**: capacidade de teste, estrutura (1 campanha com CBO → N ad sets, 1 = 1 conceito), naming, UTM, proteções

**LAUNCH**

17. **ad analysis**: 4Pi, classificação nas 4 classes, diagnóstico e decisões, depois de 3-7 dias de veiculação
18. **scale**: Scaling Protocol vertical + horizontal, depois que aparece um breakthrough
   - *lateral:* **Promo Engine**: consulta lateral e sazonal; uma rodada por janela, sempre com o gate de números (breakeven ROAS e CPA recalculados com a margem promocional)
   - *lateral:* **Team Engine**: consulta lateral de estágio scaling; pra starter/validating a resposta honesta costuma ser "ainda não", com o gargalo nomeado
19. **retention, Fase B**: win-back, replenishment e segmentação, a partir de 50 compras
20. **bonus delivery, Fase B**: tracking de take-rate
21. **content recycler**: Trilha 1 amplificação e, sob pedido, Trilha 2 (9 derivadas); só com breakthrough
   - *lateral:* **Marketplace Engine**: consulta lateral de estágio scaling; canal secundário só depois de breakthrough na análise de ads e conta fechando na finance engine
<!-- gen:overview-order:end -->

**Fora desta sequência — a finance engine como consulta lateral.** Ela não ocupa um passo: roda quando o membro precisa de uma decisão financeira. Dois momentos naturais — logo depois do passo 5 (**offer**), pra checar se a oferta fecha a conta do negócio inteiro com o custo fixo dentro (Modo A), e a cada mês fechado depois do LAUNCH, pra medir alavancas, cohorts, payback e caixa (Modo B). As skills **`offer-builder`** (oferta), **10** (ad strategy), **11** (ad analysis), **12** (escala) e **13** (retenção) leem o output dela quando ele existe — sem o arquivo, cada uma mantém o comportamento atual.

**As outras cinco laterais (`creator-engine`, `promo-engine`, `team-engine`, `ops-engine` e `marketplace-engine`) seguem o mesmo princípio — nenhuma ocupa um passo, e cada uma tem sua posição natural:**

- **Creator engine** — DUAS fases com posições diferentes. A **Fase A** (seeding + conteúdo humano) pode rodar em paralelo desde cedo: junto do passo 10 (**creatives**) e antes do LAUNCH, a partir do momento em que existe produto com preço definido (a plataforma de seeding prefere a loja no ar; o outreach manual anda antes). Começar cedo importa — do contrato de um creator externo até o conteúdo virar ad passam ~26 dias na média. A **Fase B** (contrato recorrente, whitelisting, partnership ads) só abre depois de um breakthrough confirmado pela **`ad-analysis`**.
- **Promo engine** — sazonal: dispara por época ou pedido (setembro-outubro pra montar o Q4; as outras datas pelo calendário sazonal de desejos), uma rodada por janela. Sempre com o gate de números: breakeven ROAS e CPA recalculados com a margem promocional antes de ligar qualquer campanha. O evergreen segue intocado em paralelo.
- **Team engine** e **marketplace engine** — consultas de estágio scaling: time quando o membro vira o gargalo (ou a vaga/gestão aparecem), canal secundário só depois de breakthrough na `ad-analysis` e conta fechando na `finance-engine`. Pra starter/validating, a resposta honesta das duas costuma ser "ainda não", com o motivo e o sinal que reabre a conversa.
- **Ops engine** — a parte de backups (checklist de continuidade) vale desde o começo, logo depois do passo 1 (**setup**) e antes do primeiro ad: conta nova é a mais frágil da vida do negócio, e a redundância é mais barata de armar cedo. O resto (constraint do ano, negócio como ativo) revisita por trimestre e antes de decisões grandes — escala agressiva e Q4.

Cada skill faz pre-flight da anterior. Se algum artefato falta, oferece fallback (rule `emergency-escape-paths` — ES1).

**Iteration loop normal:** depois de cada launch, ad analysis + iteração de creative ou copy é o ciclo. Skill `consistency-audit` reroda antes de qualquer relaunch crítico.

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
| 2026-09-17 | **Skill 01 reescrita — pesquisa por recombinação de elementos validados; compliance e gates de evidência removidos do framework.** A 01 passa a descobrir marcas no TrendTrack (Explorer → Meta Ads, dois conjuntos fixos de filtros: native ads em imagem e em vídeo; MCP com checagem de créditos ou manual no browser), montar a ficha de cada marca (LP mais escalada, ads mais escalados, tráfego, oferta, mecanismos), validar só com Google Trends (problema + ingrediente) e Trustpilot 1-2 estrelas, decompor em elementos validados e montar jogadas de recombinação (4 padrões; nunca clonar, nunca criar do zero). Banco de marcas no Notion (MCP novo, prefixo `mcp__claude_ai_Notion__`/`mcp__notion__`) ou em HTML. Saem do framework: a lib `compliance-preflight`, o GATE 1 de ad-flag, o sweep 8 de compliance da 06, a ETAPA 7.5 da 08, o C5 da 09, a rule 8b de palavras proibidas (vira "copy agressiva e sem aviso"), os filtros técnicos de markup/peso/bateria/sazonalidade, o check de USPTO, o gimmick check, os Data Quality/Source Audit nos relatórios e as flags `claims_unverified`/`compliance_override`. A Research Foundation da 04 vira **banco de provas** (munição de specificity, sem grau de evidência, sem suavizar claim, sem bloquear). A rule `pre-launch-gates` (Promise↔Config) e o label "AI Info" da Meta saem por completo — nenhum limitador entre copy e launch. Entra a **regra 12 + `tools/limpador-de-metadados/`**: todo criativo passa pelo Limpador de Metadados antes de subir (programa de arrastar e soltar com 2 cliques na pasta da Aura, Mac e Windows, ou `bash tools/strip-metadata.sh`) — remove EXIF/XMP/IPTC/C2PA/`hf-job-id`/tags de encoder sem perder qualidade (imagem reescrita byte a byte, vídeo por stream copy) e renomeia pra `asset-xxxx`; o hook de início deixa os atalhos prontos e avisa se falta o ffmpeg. |
| 2026-09-17 | **Reforma mecânica, Fase 1: acesso à base sem credencial.** A URL do servidor MCP da base perde o parâmetro de chave e a variável de ambiente associada em todos os lugares (`.mcp.json`, README, skill de setup, guia de instalação, OVERVIEW). A base passa a ser acessível por quem tiver a URL; o membro só aprova o servidor `aura` na primeira abertura do Claude Code. O guard de pre-commit ganha dois padrões novos pra impedir que a credencial antiga volte por acidente. Dois exemplos de skill (01 e 02) que reproduziam um produto real trocam de vertical pra pele. |
| 2026-09-17 | **Reforma mecânica, Fase 2: registro único das skills e documentação gerada.** Nasce o `.claude/skills.json`, fonte única da identidade, da ordem, dos gatilhos e das pastas de cada skill (id por slug, sem número; o número antigo vira apelido em `legacy_ids` e continua roteando; `position` define o "Passo N", com `two-phase`, `parallel` e `side` como faixas fora da sequência simples). O `tools/gen_docs.py` passa a gerar, a partir dele, a tabela de skills do README, a lista de gatilhos e a linha ORDEM LÓGICA do CLAUDE.md, a lista `PHASES` do painel, o enum de `skills_completed` do manifest-schema (ids novos, com os antigos aceitos até a migração do workspace), os cabeçalhos do §4 e a ordem canônica do §13 deste documento e a linha de título de cada skill; `gen_docs.py --check` acusa trecho gerado editado à mão. O Gate 5 da rule de self-audit troca a checklist de cinco lugares pela regra "skill nova = uma entrada no skills.json + gen_docs". |
| 2026-09-17 | **Reforma mecânica, Fase 3: consulta ao índice por script.** As skills deixam de abrir o `frameworks.json` (720 KB, cerca de 200 mil tokens) para enumerar entradas: cada uma roda `kb_lookup.py --skill <id> [--domain ...]` e trabalha com a lista impressa, com teto de 6, 10 ou 14 buscas por etapa conforme o peso da skill; as `best_query` embutidas nas skills continuam byte a byte (737 ocorrências, conferidas pelo `check_embedded_queries.py`). O índice ganha o campo `skills` por entrada (ids do registro, derivados do texto de `use_in_skill` pelo `normalize_index.py`), sem alterar nenhum outro campo. |
| 2026-09-17 | **Reforma mecânica, Fase 4: lint do framework e correção das pontas soltas.** Nasce o `tools/aura-check.py`, que confere a consistência mecânica do framework em oito regras (`paths`, `queries`, `skill-ids`, `counts`, `removed-terms`, `sections`, `secrets`, `gen`) e imprime cada falha como `ARQUIVO:LINHA  REGRA  mensagem`; o pre-commit guard passa a rodá-lo (`secrets`, `paths`, `skill-ids`) sempre que há arquivo de `.claude/` ou `tools/` no staging. Com o lint limpo, entraram as correções da leitura linha a linha: contratos entre skills alinhados (nomes de campo que a 15 lê na 18 e na 20, leitoras nomeadas na 09 e na 19, SALVAR da 03 completo, fechamento da 07d na ordem canônica, seção e chave `specs` na 06, régua única de custo desembarcado × preço no cânone unit-economics §6), réguas contraditórias resolvidas dentro da mesma skill (margem abaixo de US$ 20 na 04 vira aviso com `margin_warning`, exceção do tempo no ar escrita na 03, filtro S.I.N. movido pra ETAPA 6 da 01, warmup da 10 começando no domingo, Escola C da 12 na cadência do protocolo, cinco cenários de stress na 15, 9 sweeps na 06, gate único renumerado na 07b), o ES3 da rule de escape preenchido, os últimos resíduos de linguagem de policy apagados e a documentação das libs (swipe-models, creative-dna, design system dos relatórios) alinhada aos arquivos reais. |
| 2026-09-17 | **Reforma mecânica, Fase 5a: skills identificadas por nome.** Os 26 arquivos de skill passam a se chamar `<id>.md` (sem número); o número antigo sobrevive só como apelido em `legacy_ids`. Nasce o `tools/migrate_ids.py`, que trocou as referências numéricas do framework pelos ids (`08-creative-engine` → `creative-engine`, `07-page/` → `page/`, `skill 08` → skill `creative-engine`, `(04)` → (`offer-builder`), `a 11` → a `ad-analysis`) e lista o que sobrou para revisão manual; a revisão fechou o resto à mão. Ficam numéricos por natureza: `legacy_ids`/`legacy_folder` do registro, `use_in_skill` do índice, o catálogo do `kb-index/`, este changelog, o `OVERVIEW.html` (gerado na Fase 6), o `build_index.py` e as pastas do workspace (migrados na Fase 5b) e os campos `10_*` do manifest (nomes gravados em manifests reais, agora exceção explícita do lint). |
| 2026-09-17 | **Reforma mecânica, Fase 5b: pastas do workspace por nome e migração automática.** Cada fase do produto passa a morar em `workspace/<slug>/<id>/` (`market-research/`, `page/`), sem número. Nasce o `tools/migrate.py` (executor de migrações de layout, com `--all`, `--product`, `--dry-run` e `--list`) e a migração `tools/migrations/001_slug_folders.py`, que renomeia as pastas numeradas pelo par `legacy_folder` → `folder` do registro, traduz `skills_completed` para os ids, faz backup do manifest, grava `framework_version` (campo novo do manifest-schema) e registra cada passo em `.migrations.log`; pasta de destino já existente é pulada e avisada, nunca mesclada. O hook `post-start.sh` roda a migração toda sessão (silenciosa quando não há nada pendente). O `build_index.py` lê as pastas novas e cai na numerada por um ciclo (mapa `LEGACY_FOLDERS`, gerado junto com a `PHASES`); o pré-flight de todas as skills que leem o produto ganhou a mesma frase de fallback. Os sete produtos do workspace local foram migrados nesta fase. |
| 2026-09-17 | **Reforma mecânica, Fase 5c: apelidos só no registro e no índice; regra estrita no lint.** O número antigo de cada skill passa a existir em três lugares apenas: `legacy_ids`/`legacy_folder` do `.claude/skills.json` (roteamento quando o membro diz um número), `use_in_skill` do `frameworks.json` (texto original do catálogo, traduzido pelo `normalize_index.py` para o campo `skills`) e o changelog deste §14. A regra `skill-ids` do `tools/aura-check.py` fica estrita: em qualquer outro texto do framework, número como identificador de skill é falha (pasta ou arquivo `NN-slug`, `skill NN`, `skill-NN`, `(NN)` depois do nome, apelido com letra solto, preposição + número fora de contexto numérico, faixa entre apelidos), usando o filtro de contexto numérico do `tools/migrate_ids.py`, que passou a ser importado pelo lint. O enum de `skills_completed` do `manifest-schema.json` sai só com os ids (os manifests antigos são traduzidos pela migração 001). O `migrate_ids.py` deixa de pular toda linha com a palavra "apelido" (só "apelido antigo", que é o rótulo das docs geradas) e passa a cobrir `.template`; com isso saíram as últimas referências numéricas escondidas (`labels[]` "da Skill 02" na copy-engine e na creative-engine, "Skill 06" na market-research, a lista de skills do `brand.md.template`). O CLAUDE.md gerado continua mostrando "apelido antigo: NN" por um ciclo, com a linha de roteamento pelo `legacy_ids`. |
| 2026-09-17 | **Reforma mecânica, Fase 6: o HTML dos relatórios deixa de ser escrito à mão.** Nasce o `tools/render_report.py`: lê o `.md` de um relatório e monta o `.html` sobre o `aura-report-template.html` (o `<style>` completo, a topbar com a logo SVG canônica, o hero, a meta-bar, o sumário gerado dos `##`, as bandas escuras alternadas, o rodapé e o script de interação), com um conversor de Markdown mínimo (títulos, parágrafos, listas aninhadas, tabelas, negrito, itálico, código, links, citações) e convenções que viram componentes: citação com `**Nota:**`, `**Atenção:**`, `**Oportunidade:**`, `**Risco:**` ou `**Vencedor:**` vira o card correspondente, citação comum vira citação de cliente (com `Tradução livre:` e `Fonte:`), tabela `KPI \| Valor` vira os números grandes. A meta-bar lê um frontmatter simples (`produto`, `mercado`, `data`, `alimenta`) ou, sem ele, o manifest do produto, a data de hoje e os consumidores da skill no registro; o chrome sai em `pt-BR` ou `en` conforme o `report_language`. A regra 6b do CLAUDE.md, as seções SALVAR das 26 skills, a lib do content-recycler e a rule de self-audit passam a mandar `python3 tools/render_report.py <md>` em vez de copiar `<style>`, topbar e logo; o bloco da logo obrigatória vira uma linha; o `aura-html-components.md` foi reescrito como a lista das convenções de Markdown; o template ganhou o CSS de prosa (bloco de código, listas, régua, imagem, link, meta-bar com menos de quatro itens). O `.claude/OVERVIEW.html` passa a ser gerado deste `.md` pelo `gen_docs.py` (alvo `overview-html`, coberto pelo `--check`) e nunca mais é editado à mão; o `.md` ganhou um frontmatter com os dados da meta-bar. |
| 2026-09-17 | **Reforma mecânica, Fase 7: CLAUDE.md enxuto, regra de idioma como rule e duplicatas removidas.** O `.claude/CLAUDE.md` cai de cerca de 63 KB para menos de 15 KB: fica a identidade, as treze regras em forma curta (cada uma apontando para o arquivo com o detalhe), os gatilhos e a ordem gerados (a linha de gatilho perde o resumo longo por skill; a descrição completa vive no frontmatter de cada skill e no §4 deste documento), os quatro cânones em uma linha cada, a coleta resiliente em três linhas e o auto-update em cinco. A regra 0 inteira passa a viver na rule nova `.claude/rules/report-language.md` (carregada em skills, templates e `workspace/`), junto com as sete regras de escrita simples do manual do membro; o protocolo completo de auto-update vai, sem alteração, para `.claude/lib/auto-update/README.md`. Saem do CLAUDE.md a seção de queries úteis por área (as queries vivem nas skills e no índice) e a prosa das laterais (que já estava no §13). Este documento perde a subseção de hooks globais do §7. O README do `kb-index` fica só com as seções de atualização, uso do índice, mapa skill → domínios e ex-órfãos (o catálogo por domínio sai do `kb_lookup.py`, nunca de um README). |
| 2026-09-18 | **Reforma mecânica, Fase 8: estado verificável.** Nascem os schemas por fase em `.claude/templates/schemas/<id>.dados.schema.json` (13 skills que gravam `dados.json` lido por outra; campos da seção de schema de cada skill, `required` só no que outra skill lê), o `tools/manifest.py` (`get`, `set`, `complete`, `validate`: única forma de escrever o manifest, com backup, `updated_at` e validação contra o `manifest-schema.json`; `complete` valida o `dados.json` da fase antes de marcar), o `tools/aura-status.py` (relatório presente ou ausente por fase, marca sem artefato e artefato sem marca, arquivo fora do layout canônico, `dados.json` fora do schema, manifest inválido; `--all`, `--json`, `--brief`) e o validador `tools/schema_validate.py`. O `build_index.py` passa a ler o estado do `aura-status` e ganha `--global` (painel `workspace/ABRIR-AQUI.html` com um card por produto). O hook `Stop` `post-skill.sh` mostra até 10 linhas `[aura-status]` do produto tocado nos últimos 30 minutos, uma vez por mudança. O ES3 da rule de escape paths passa a apontar `aura-status` e `manifest.py complete`; as seções de manifest das 26 skills chamam o script em vez de editar o JSON. A regra 5 do CLAUDE.md cita os dois scripts. O `AGENTS.md` local foi apagado (decisão do membro) e a linha do §3 saiu. |
| 2026-09-18 | **Reforma mecânica, Fase 9a: a `creative-engine` no formato nativo de skills do Claude Code (piloto).** A skill passa a viver em `.claude/skills/creative-engine/SKILL.md` (frontmatter `name` e `description`, roteiro de 12 KB: quando usar, pré-flight, contexto a carregar, uma seção curta por ETAPA dizendo o que fazer, ler e escrever, SALVAR e mensagem final) com o material de apoio em `reference/<tema>.md` (15 arquivos: contexto, MCPs opcionais, rota de produção, capacidade de teste, variáveis de um ad, ideação e seleção, regras estruturais, zona emocional, briefing, entregável de produção, pós-briefing, resumo de produção, checklist final, dados.json e mensagem final), que cada etapa manda abrir na hora. Nenhuma etapa, régua ou query mudou: o texto integral da skill foi movido, sem alteração, para os arquivos de apoio. O registro aponta `file` para o `SKILL.md`; o `aura-check.py` lê os arquivos de apoio (caminhos `reference/` relativos à pasta da skill, queries, contagens e referências a ETAPA resolvidas contra o `SKILL.md`) e o `check_embedded_queries.py` os conta. As outras 25 skills migram nas fases 9b a 9d. |
| 2026-09-18 | **Reforma mecânica, Fase 9b: lote 1 do formato nativo (`ad-analysis`, `scale-engine`, `offer-builder` e `page-build`).** As quatro skills passam a viver em `.claude/skills/<id>/SKILL.md` (frontmatter `name` e `description`, roteiro abaixo de 12 KB) com o material de apoio em `reference/<tema>.md` (16, 12, 13 e 12 arquivos), pelo mesmo método do piloto: o texto integral de cada skill foi fatiado por faixa de linha, sem alteração de etapa, régua ou query, e todo cabeçalho de ETAPA continua no `SKILL.md`. Um commit por skill. As duas rules com `paths` apontando para `page-build.md` (`reverse-order-insertion.md` e `shopify-theme-safety.md`) passam a apontar para `page-build/SKILL.md`. O conversor `migrate_ids.py` e o lint passam a compartilhar a lista de nomes legados de relatório (`LEGACY_REPORT_NAMES`), fechando o falso positivo em `tools/aura-status.py`. |
| 2026-09-18 | **Reforma mecânica, Fase 9c: lote 2 do formato nativo (`page-design`, `copy-engine`, `ad-strategy` e `market-research`).** As quatro skills passam a viver em `.claude/skills/<id>/SKILL.md` (frontmatter `name` e `description`, roteiro abaixo de 12 KB) com o material de apoio em `reference/<tema>.md` (14, 15, 13 e 16 arquivos), pelo mesmo método do lote 1: o texto integral de cada skill foi fatiado por faixa de linha, sem alteração de etapa, régua ou query, e todo cabeçalho de ETAPA continua no `SKILL.md`. Um commit por skill. Na `copy-engine`, a linha de exemplo da Trust Bar volta a citar um número de reviews (a conversão mecânica da Fase 5a a tinha transformado num id de skill). Nenhuma rule tinha `paths` apontando para essas quatro skills. Nove skills estão no formato nativo; as dezessete restantes migram na Fase 9d. |
| 2026-09-18 | **Reforma mecânica, fechamento da Fase 9c: número em contexto numérico nunca é apelido de skill.** O conversor `tools/migrate_ids.py` e a regra `skill-ids` do `tools/aura-check.py` só tratam um número como candidato a id de skill quando ele aparece isolado como palavra ("a 08", "skill 12"); dígito colado, vírgula ou ponto seguidos de dígito, `%`, moeda, unidade colada e data AAAA-MM-DD ficam de fora (`12,000 reviews`, `18,7%`, `$12`, `20% do budget`, `2026-09-01`). Testes em `tools/tests/test_migrate_ids.py`. Os dois literais que a conversão mecânica da Fase 5a tinha estragado voltaram ao original: `(12,000 reviews)` na Trust Bar de exemplo da `copy-engine` e `(18,7%)` no exemplo de margem da `offer-builder`; a varredura completa contra a `main` não achou outro. |
| 2026-09-18 | **Reforma mecânica, Fase 9d, lote 3a do formato nativo (`setup`, `product-research`, `sourcing` e `competitor-analysis`).** As quatro skills passam a viver em `.claude/skills/<id>/SKILL.md` (frontmatter `name` e `description`, roteiro abaixo de 12 KB) com o material de apoio em `reference/<tema>.md` (10, 15, 16 e 15 arquivos), pelo mesmo método dos lotes anteriores: o texto integral de cada skill foi fatiado por faixa de linha, sem alteração de etapa, régua ou query, e todo cabeçalho de ETAPA continua no `SKILL.md`. Um commit pras quatro. Treze skills estão no formato nativo; as treze restantes migram nos próximos lotes da Fase 9d. |
| 2026-09-18 | **Reforma mecânica, Fase 9d, lote 3b do formato nativo (`finance-engine`, `tracking-setup`, `checkout-aov` e `bonus-delivery`).** As quatro skills passam a viver em `.claude/skills/<id>/SKILL.md` (frontmatter `name` e `description`, roteiro abaixo de 12 KB) com o material de apoio em `reference/<tema>.md` (17, 10, 11 e 8 arquivos), pelo mesmo método: texto integral fatiado por faixa de linha, sem alteração de etapa, régua ou query, todo cabeçalho de ETAPA no `SKILL.md`. A rule `shopify-theme-safety` passa a apontar `paths` para `tracking-setup/SKILL.md` e `checkout-aov/SKILL.md`. Um commit pras quatro. Dezessete skills estão no formato nativo; as nove restantes migram nos próximos lotes da Fase 9d. |
| 2026-09-18 | **Reforma mecânica, Fase 9d, lote 3c do formato nativo (`retention-engine`, `creator-engine`, `agentic-readiness` e `consistency-audit`).** As quatro skills passam a viver em `.claude/skills/<id>/SKILL.md` (frontmatter `name` e `description`, roteiro abaixo de 12 KB) com o material de apoio em `reference/<tema>.md` (12, 17, 8 e 7 arquivos), pelo mesmo método: texto integral fatiado por faixa de linha, sem alteração de etapa, régua ou query, e o material de apoio byte a byte igual ao original. Na `retention-engine`, cujo texto original não tinha cabeçalho de ETAPA, o roteiro ganhou a numeração `ETAPA 0` a `ETAPA 6` sobre as seções que já existiam; nas outras três, todo cabeçalho de ETAPA continua no `SKILL.md`. Nenhuma rule tinha `paths` apontando para essas quatro skills. Um commit pras quatro. Vinte e uma skills estão no formato nativo; as cinco restantes migram nos próximos lotes da Fase 9d. |
| 2026-09-18 | **Reforma mecânica, Fase 9d, lote 3d do formato nativo (`promo-engine`, `team-engine`, `content-recycler` e `marketplace-engine`).** As quatro skills passam a viver em `.claude/skills/<id>/SKILL.md` (frontmatter `name` e `description`, roteiro abaixo de 12 KB) com o material de apoio em `reference/<tema>.md` (17, 23, 9 e 12 arquivos), pelo mesmo método: texto integral fatiado por faixa de linha, sem alteração de etapa, régua ou query, e todo cabeçalho de ETAPA no `SKILL.md`. As rules `shopify-theme-safety` e `reverse-order-insertion` passam a apontar `paths` para `content-recycler/SKILL.md`. Some também a redundância que a conversão da Fase 5a deixou em nove lugares, onde o número virou slug ao lado do nome já escrito por extenso ("skill `page-design` (page-design)"), no `manifest-schema.json`, na `team-engine` e na `checkout-aov`. Um commit pras quatro. Vinte e cinco skills estão no formato nativo; falta a `ops-engine`, que fecha a fase junto com as rules e as docs. |
| 2026-09-18 | **Reforma mecânica, Fase 9d, lote 3e: a `ops-engine` no formato nativo e as rules apontando para o novo caminho. Fecha a fase.** A `ops-engine` passa a viver em `.claude/skills/ops-engine/SKILL.md` com dez arquivos de apoio, e com ela as vinte e seis skills estão no formato nativo: nenhum `.claude/skills/<id>.md` restou. As cinco rules que valiam para todas as skills (`report-language`, `emergency-escape-paths`, `iteration-driven-refinement`, `member-stage-awareness` e `troubleshooting-patterns`) trocam `paths: .claude/skills/` por `.claude/skills/**/SKILL.md`; as duas que valem só para algumas (`shopify-theme-safety` e `reverse-order-insertion`) já listam skill por skill, agora pelo caminho novo. O `report-only-results` e o `resilient-fetch` seguem sem frontmatter, porque valem em toda sessão e não só dentro de uma skill. Método da fase, igual do começo ao fim: o texto de cada skill foi fatiado por faixa de linha para os arquivos de apoio, byte a byte, e o `SKILL.md` virou o roteiro curto que diz o que fazer, o que abrir e o que salvar em cada etapa. |
| 2026-09-18 | **Reforma mecânica, Fase 9e: o bloco `resumo` no `dados.json` de cada fase que alimenta a seguinte.** O `dados.json` da `market-research`, da `competitor-analysis`, da `offer-builder`, da `copy-engine` e da `creative-engine` passa a abrir por um objeto `resumo`, com no máximo doze campos curtos: o que a fase seguinte precisa saber de primeira, sem carregar o arquivo inteiro. Ele não guarda dado novo, espelha campos que já existem mais abaixo, é preenchido por último e, onde divergir, o campo de origem vence. As sete consumidoras (`offer-builder`, `copy-engine`, `page-design`, `creative-engine`, `consistency-audit`, `ad-strategy` e `ad-analysis`) ganharam a regra no 'Contexto a carregar': ler o `resumo` primeiro e abrir o arquivo inteiro só na etapa que precisa do detalhe; na `consistency-audit`, todo check que compara valor literal continua abrindo o campo de origem. Os cinco schemas de fase descrevem o bloco como **opcional**, então `dados.json` gravado antes desta convenção continua validando. |
| 2026-09-18 | **Reforma mecânica, fechamento da Fase 9: o teto do `SKILL.md` virou regra do lint.** O `tools/aura-check.py` ganha a nona regra, `skill-size`: todo `SKILL.md` apontado pelo registro cabe em 12 KB (12.288 bytes). O teto existia desde a Fase 9a como critério do plano e era conferido à mão; agora falha sozinho e diz quanto o arquivo tem, com o remédio junto, que é mover o excedente para `reference/<tema>.md`. As vinte e seis skills passam, e a maior é a `promo-engine`, com 12.095 bytes. |
| 2026-09-18 | **Orçamento de buscas: piso obrigatório e teto só para o adicional.** A instrução de consulta à base dizia "no máximo N buscas por etapa" e, na frase seguinte, que as queries já embutidas na etapa eram o mínimo garantido; quando a etapa trazia mais queries que o teto, as duas se contradiziam. A redação passa a separar os papéis em todas as skills que consultam a base, no item 3 do README do kb-index e na regra 3 do CLAUDE.md: as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Junto, a `consistency-audit` saiu das skills leves e passou a ter teto 14: as três baterias de checks trazem 32 queries embutidas (12, 12 e 8), 33 no total, contra o teto antigo de 6. |
| 2026-09-18 | **Regra `member-data` no lint: dado de produto do membro não entra no framework.** O `tools/aura-check.py` ganha a décima regra, que confere que nenhum arquivo rastreado contém nome de produto, loja ou marca do workspace. A lista de termos é montada em tempo de execução a partir dos `manifest.json` de `workspace/` (`product_slug`, nome da pasta, `product_name` inteiro e a parte antes do primeiro parêntese) mais os domínios `*.myshopify.com` que aparecerem neles e o handle de cada um; termo curto demais, igual a um id ou pasta do registro, ou de uma palavra só e genérica (`GENERIC_TERMS`) fica de fora, para a regra não acusar vocabulário comum. A falha nunca imprime o termo: só arquivo, linha e o aviso. Sem `workspace/` na máquina a lista fica vazia e a regra passa. O CHECK 4 do pre-commit guard passa a rodar essa regra com qualquer arquivo no staging, não só com arquivo de `.claude/` ou `tools/`. Junto: o `.claude/templates/aura-html-components.md` trocou os dois exemplos que usavam um produto real (o `produto` do frontmatter e a citação de cliente com fonte) por exemplo genérico de outra vertical. |
| 2026-09-18 | **O re-clone do auto-update passa a preservar tudo que é local-only.** O caso 5 do protocolo de `.claude/lib/auto-update/README.md` (histórico divergiu, precisa de clone novo) tirava do clone só o `workspace/` e depois apagava a pasta inteira, o que destruía o `docs/historico/`, que também é local-only e não existe no GitHub. A sequência passa a renomear o clone antigo (`mv ~/aura-engine ~/aura-engine-antigo`) em vez de apagar, restaura o `workspace/` e o `docs/historico/` a partir dele e só então declara concluído; enquanto a pasta antiga existir, nada se perdeu, e `git status --ignored` dentro dela lista o que mais era local-only. A regra inviolável trocou "nunca `rm -rf` com o workspace dentro" por "nunca apague a pasta do clone". Mesma correção na seção Updates do `README.md` e na linha de auto-update do `CLAUDE.md`. |
| 2026-09-18 | **Reforma mecânica: o `aura-status` avisa quando um `dados.json` não tem o bloco `resumo`.** O `tools/aura-status.py` passa a imprimir, por produto e por fase, uma lista de avisos separada das issues: `dados.json` de uma fase cujo schema prevê o bloco `resumo` e que não tem o bloco no arquivo, com a frase "sem bloco resumo: a fase seguinte vai ler o arquivo inteiro". É informativo, não conta como issue, não muda o exit code e não aparece no painel do workspace. A detecção sai do próprio schema da fase (`properties.resumo`), então vale sozinha para qualquer schema que ganhe o bloco depois. Arquivo que não parseia continua sendo issue de schema e não vira aviso. No `--json` os avisos vivem na chave `notes`; no `--brief` entram depois das issues, no espaço que sobra das dez linhas. |
| 2026-09-18 | **Reforma mecânica, Fase 9d: barra, faixa e palavra de quantidade entram no filtro de contexto numérico.** Uma segunda varredura da conversão da Fase 5a, comparando cada arquivo com a versão anterior àquele commit, achou três números que viraram id de skill fora de contexto de skill: a data do Singles' Day na `promo-engine`, as doze perguntas numeradas da `ad-analysis` e as dez alternativas do Hooks Bank da `creative-engine`. Os três literais voltaram. Para a regra não repetir o erro, o filtro do `tools/migrate_ids.py` (usado pelo lint) passa a tratar como número, nunca como apelido: barra com dígito ou mês dos dois lados (`11/11`, `26/12`, `10/nov`), faixa escrita em português (`de 5 a 10`, `ETAPAs 8 a 14`) e palavra de quantidade depois do número (`10 alternativas`, `12 numeradas`). Seis casos novos entraram nos testes de `tools/tests/test_migrate_ids.py`, e o relatório de menções numéricas caiu de trinta e duas para onze linhas, todas números reais. |
| 2026-09-18 | **O formato que o concorrente escalado usa entra na escolha do tipo de página, e o enum ganha `quiz` e `listicle`.** A `competitor-analysis` passa a classificar, na ETAPA 3E, o formato de cada página de destino dos ads escalados em oito valores (`advertorial`, `listicle`, `landing`, `pdp_robust`, `pdp_lean`, `quiz`, `vsl`, `home`), com o link, quantos ads caem nela e o elemento da página que decidiu a classificação, em `landing_formats[]`; o `resumo` ganha `dominant_landing_format`, que é o formato com a maior soma de ads e fica `null` com menos de três landings classificadas. O `page_type` da `page-design` deixa de sair de dois sinais e passa a sair de três, nesta ordem de peso: consciência dominante, tipo de abertura da copy e formato dominante do concorrente. Os três viram famílias antes de serem comparados (pré-lander editorial, página de venda dedicada, página de produto, quiz): mesma família e mesma variante, a skill decide e segue; variante diferente dentro da família, adota a do concorrente e informa em uma linha; famílias diferentes, mostra a divergência com o número de ads e o membro decide. O `page-plan.json` grava os três sinais e o que fechou a decisão em `strategy.page_type_signals`, e a `consistency-audit` lê esse bloco antes de acusar drift de tipo de página. `quiz` e `listicle` entram no enum de `page_type` do `manifest-schema.json` e do `page-plan.json`: o listicle é pré-lander como o advertorial (mesmo `destination_ref` obrigatório e mesmo mapa canônico das sete seções da copy, com os itens numerados como tratamento), e o quiz, que só chega pelo sinal do concorrente, sempre passa pela decisão do membro. |
| 2026-09-18 | **A paleta da página deixa de ser um menu de 8 presets e passa a ser gerada, com motivo, em 3 candidatas.** O Caminho 4 dos brand signals da `page-design` (ETAPA 2) trocou a lista de presets pelo gerador `.claude/lib/design-presets/palette_engine.py`: entram a vertical do produto, o avatar central da `market-research`, o ceticismo do mercado e as cores da marca quando existem; saem exatamente 3 paletas candidatas, cada uma com nome curto, o motivo em uma frase (o que aquela família de cor comunica naquele mercado, pra aquele avatar), a relação de matiz declarada (análoga, complementar dividida ou tríade) e os 8 roles completos. O script valida a si mesmo antes de imprimir e nenhuma paleta sai com aviso: saturação acima do piso em `primary` e `accent` (cor viva, nunca cinza), a distância real de matiz batendo com a harmonia declarada, contraste WCAG AA no texto e no texto secundário contra o fundo e contra a superfície dos cartões, e no texto do botão contra o botão, mais 3:1 na cor de apoio, e as 3 candidatas a 25 graus ou mais uma da outra; o que não fecha é corrigido na claridade ou o script sai com erro. Os 8 presets de `presets.json` continuam sendo a base (cada candidata herda deles o perfil de claridade dos neutros, a tipografia, o radius, a sombra e a densidade, literais, e troca só o matiz), e a mesma entrada devolve sempre as mesmas 3 paletas, então re-rodar a skill não troca a cor debaixo do membro. A comparadora na página real vira obrigatória nesse caminho, com os blocos de token em trio R,G,B saindo prontos do `--format css`. Testes em `tools/tests/test_palette_engine.py`. |
| 2026-09-18 | **A tipografia da página passa a abrir com duas famílias sugeridas, e arquivo de fonte do membro vira caminho de primeira classe.** A ETAPA 2 da `page-design` ganhou três sub-etapas explícitas: 2.1 tipografia, 2.2 cor e 2.3 a comparadora. A 2.1 mostra duas famílias e só duas, lidas do bloco `suggested_typefaces` de `.claude/lib/design-presets/presets.json`: ABC Oracle, da fundição Dinamo, que o membro baixa no site dela e guarda em `workspace/fontes/`, e Geist, que carrega por link do Google Fonts e não pede passo nenhum. A Aura não baixa, não hospeda e não copia fonte de um membro pra outro, e nada sobre licença entra no que o membro lê. O arquivo baixado passa pelo `.claude/lib/design-presets/local_fonts.py`, novo: ele lê o peso real de cada arquivo no metadado (`usWeightClass`, direto do `.otf`, `.ttf` ou `.woff`; o `.woff2` empresta do irmão de mesmo nome e, sem irmão, vale o apelido do nome, com o relatório dizendo que foi assim), prefere `.woff2` quando existe, copia pra `page/design/assets/fonts/` só os pesos que a página usa e emite o `@font-face` num bloco marcado `data-aura-fonts`, em três modos: apontando pros arquivos ao lado do HTML de design (o padrão, mesmo tratamento das imagens), com `asset_url` pro `<head>` do `theme.liquid`, ou com a fonte embutida em base64 pra quando o HTML precisa viajar sem a pasta. A comparadora deixou de ser só de cor: passa a ter um seletor por eixo, e o membro escolhe paleta e fonte vendo a página real. A tipografia decidida na 2.1 vence a que vier do Refero, do print ou do preset base. Na `page-build`, o passo 6.4b lê o `type.families[]` do `design-tokens.json` e provisiona por `provision` (Google Fonts por `<link>`, arquivo local como asset do tema), o split remove o bloco antes de compilar (o caminho que ele carrega não existe na loja) e o GATE 1 conta o peso da fonte local, avisando com número quando ela estoura o orçamento. O pre-commit guard passou a recusar `.woff`, `.woff2`, `.otf` e `.ttf` no staging: o framework não versiona binário de fonte. Testes em `tools/tests/test_local_fonts.py`, com arquivos SFNT sintéticos montados byte a byte. |
| 2026-09-18 | **O menu de rotas de design da `page-design` passa de cinco rotas para três.** A ETAPA 3 agora abre com três caminhos, todos convergindo pro mesmo `design/page.html` e passando pela mesma régua de qualidade, que é bloqueante nas três. A rota 1, o novo padrão, desenha a página do zero no canvas do Claude Design, que hoje roda dentro do Claude Code pela tool `Artifact` (quickstart com `intent: "design"` devolve o tipo de design da conta, o create traz as instruções dele, e toda atualização vai pro mesmo endereço); o arquivo local continua sendo o entregável e a fonte, e canvas que não abre não aborta a rota. A rota 2 é o clone de uma página inteira que o membro salva com a extensão SingleFile no browser dele, com o esqueleto reconciliado com o plano de seções e a página preparada para virar seções editáveis no editor da Shopify, o que faz dela a única rota com pré-requisito de loja conectada pela CLI. A rota 3 monta uma página só a partir de várias referências, arquivos e prints misturados, extraindo estrutura de cada uma (nunca o texto) e unificando tudo numa escala tipográfica, numa grade de espaçamento e na paleta da ETAPA 2, com um teste de vizinhança que reprova quando dá para ver onde uma referência termina e a outra começa. Sai do framework a rota que dependia do **AIDesigner**, o MCP pago de geração de design (prefixo de tool `mcp__aidesigner__`), apagado também do canon de detecção de MCP, da regra 10 do `CLAUDE.md` e dos enums; o nome fica escrito aqui, e só aqui, para quem precisar procurar depois; saem do menu, junto, os construtores de site externos e o `frontend-design` como rota separada, cujo papel de gerar do zero passou a ser a rota 1. O enum de `design_route` do `page-plan.json` passa a ser `claude-design`, `singlefile-clone` e `section-puzzle`. |
| 2026-09-18 | **A régua de design da página passa a existir como arquivo, com itens que se conferem, e o self-review a pontua.** A sub-etapa 3.7 da `page-design` deixa de ser uma lista de boas intenções e ganha `.claude/skills/page-design/reference/regua-de-design.md`, válida nas três rotas e bloqueante: cinco blocos com teste objetivo em cada item. Tipografia (escala modular de razão única declarada no `:root`, no máximo duas famílias, diferença de peso de pelo menos 200 entre título e corpo, medida de linha entre 45 e 75 caracteres, entrelinha que encolhe conforme o texto cresce, caixa alta só em rótulo curto). Ritmo e espaço (uma grade base 4 ou 8 sem exceção, respiro entre seções valendo pelo menos duas vezes o respiro interno, proximidade dentro do bloco, alinhamento óptico do ícone pela primeira linha do texto, gutter constante no celular sem rolagem lateral). Cor (toda cor vem de um role da ETAPA 2, a cor do botão principal não aparece em nada que não seja clicável, gradiente só com função declarada, foco visível com contorno de 2px e contraste, nada dependendo só da cor). Movimento sem JavaScript (entrada por seção de 8 a 24px, duração de 200 a 600 ms com saída suave, atraso de 40 a 120 ms entre irmãos com teto de cinco degraus, rolagem por `animation-timeline: view()` dentro de `@supports` com o estado inicial só ali dentro, `prefers-reduced-motion` deixando o conteúdo no estado final, zero laço, e só `opacity` e `transform` animados). E os oito sinais de "feito por IA" que reprovam sozinhos: a grade de três cartões iguais em mais de duas seções, o mesmo ícone repetido em todo item, gradiente entre 230 e 290 graus fora da paleta, travessão em h1, h2 ou h3, foto de catálogo com sorriso corporativo, alturas de seção variando menos de 15% do topo ao rodapé, mais da metade das seções em texto centralizado numa coluna, e a mesma sombra em toda caixa. O self-review visual da 3.7 passa a preencher um placar, uma linha por item, com veredicto e evidência (o valor lido no CSS ou o que apareceu no print e em qual seção); item sem evidência conta como reprovado, e a correção refaz o placar inteiro. O teto é de 3 rodadas silenciosas: o que sobreviver à terceira vai pro membro no checkpoint, em uma linha por item, e não se confunde com as 3 iterações com ele. A régua também é briefing: a rota 1 lê antes da primeira linha de HTML, a rota 2 usa os números para limpar o layout herdado e a rota 3 tira deles a unificação. |
| 2026-09-18 | **A página ganha uma segunda opinião opcional, gerada por outro modelo e julgada pela mesma régua.** A `page-design` ganhou a sub-etapa 3.8 (`reference/brief-codex.md`), oferecida uma vez no checkpoint da 3.7, depois de a página desta skill já ter passado na régua: a Aura monta um briefing autossuficiente e salva em `page/design/brief-codex.md`, o membro cola no Codex, o agente de programação da OpenAI, e volta com outra versão da mesma página em `page/design/page-codex.html`. O briefing carrega tudo em valor literal, porque o Codex não enxerga o workspace: a página em cinco linhas (tipo, avatar, consciência, promessa e o mecanismo nomeado), o plano de seções com id, eyebrow, papel e blocos, a copy real seção por seção em inglês, os oito roles da paleta com o hex e onde cada um entra, as famílias tipográficas com os pesos e como carregam, uma linha por imagem do mapa de mídia, a régua de design inteira copiada e a lista fechada do que não fazer, que inclui a instrução explícita de não acrescentar aviso, disclaimer, asterisco, rodapé que enfraquece o claim de cima nem versão suavizada de claim. A etapa diz ao membro exatamente o que anexar em cada caminho (Codex com a pasta `page/design/` aberta, onde nada precisa ser anexado, ou Codex no browser, com as imagens e as fontes) e por que o `design/page.html` desta skill nunca é anexado: segunda opinião que começa vendo a primeira vira cópia dela. Quando o HTML volta, ele passa pela normalização da 3.6, pela limpeza silenciosa de qualquer aviso que o outro modelo tenha acrescentado, pela conferência de que a copy é literalmente a da `copy-engine` e pelo self-review visual completo; então as duas versões entram no mesmo placar da régua, com os mesmos ids e uma coluna cada, e a Aura recomenda uma em até três linhas, com desempate declarado (menos reprovas, depois o hero que passa no Grunt Test em 390, depois a fidelidade ao `section_order`). A escolha final é do membro, a versão escolhida vira `design/page.html` pelo mesmo portão de qualquer outra, o `design_route` não muda porque isto não é rota, e a rodada fica registrada no `iterations-log.json`. |
