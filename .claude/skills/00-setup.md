---
name: setup
description: Onboarding inteligente do membro. Roda na primeira vez que o membro abre o Aura Engine. Verifica dependências do sistema, testa o MCP da Aura, coleta 4 inputs essenciais, extrai dados da loja automaticamente se houver link, e roteia o membro pra fase certa baseado na situação dele. Use quando o membro disser "setup", "onboarding", "configurar", ou quando for o primeiro uso do sistema.
---

# Setup — Onboarding Inicial

Esta skill roda quando o membro digita "setup" ou quando é a primeira vez usando o Aura Engine. O objetivo é: (1) garantir que o ambiente técnico está funcional, (2) entender a situação do membro com o mínimo de fricção, (3) extrair automaticamente tudo que já dá pra extrair (ex: dados da loja se o membro tem link), e (4) rotear pro próximo passo certo.

## Quando Usar

- Primeira vez que o membro abre o Claude Code na pasta do Aura Engine
- Membro digitou "setup", "onboarding", ou "configurar"
- Membro quer refazer o onboarding (ex: mudou de produto, de stack, ou de situação)

## Antes de Começar

Consulte a base Aura extensivamente sobre fundamentos operacionais, o estado atual do marketing DTC, e como cada fase do sistema alimenta a próxima. Aprofunde em tudo que encontrar sobre entry points de membros em estágios diferentes (sem produto, com produto, vendendo, escalando) e o que cada estágio precisa priorizar. Essa base vai informar o roteamento no final.

## Fluxo da Skill

### ETAPA 0 — Boas-vindas (só na primeira vez)

Se for a primeira vez do membro (não existe `workspace/profile.md`), abra com uma saudação curta de UMA linha, bilíngue (o idioma ainda não foi escolhido), só pra dar contexto antes dos checks técnicos:

> Bem-vindo ao Aura Engine. Vou configurar tudo pra você — leva uns 2 minutos. / Welcome to Aura Engine. I'll set everything up for you — takes about 2 minutes.

Se já existe profile (membro refazendo setup), pule a saudação e vá direto pro Pré-flight.

### Pré-flight

Antes de prosseguir, valide:

- [ ] `workspace/` existe e é gravável: `mkdir -p workspace && touch workspace/.aura-probe && rm workspace/.aura-probe` — se falhar (permissão), pare e dê a instrução de correção (sem permissão de escrita não há onde salvar nada).
- [ ] Template HTML disponível em `.claude/templates/aura-report-template.html` — se ausente, NÃO pare: a Etapa 5 gera HTML mínimo inline com aviso.

O MCP `aura` é testado UMA vez, na ETAPA 2 (com query real) — não duplique o teste aqui.

> **report_language (rule 0 — INVIOLÁVEL):** esta skill é onde o `report_language` é DEFINIDO (ETAPA 2.6). A partir do momento em que o membro escolhe, TODA conversa e TODO output interno (.md/.html/.json descritivo) usam esse idioma; antes disso, default é `pt-BR`. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language. A escolha é gravada em `workspace/profile.md` E espelhada em `manifest.report_language`.

### ETAPA 1 — Verificação de Dependências

Antes de qualquer pergunta, verifique se o ambiente técnico está OK. Dependência obrigatória: **Node.js v20+**.

**Node.js** — detecte de forma inteligente:

```bash
# Node via direct
node --version 2>/dev/null

# Node via nvm
NVM_DIR="${NVM_DIR:-$HOME/.nvm}"; [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && nvm current 2>/dev/null || true

# Node via brew
/opt/homebrew/bin/node --version 2>/dev/null
/usr/local/bin/node --version 2>/dev/null
```

**Valide o NÚMERO da major version, não só presença.** Parseie a saída (ex: `v20.11.0` → major `20`):

```bash
NODE_MAJOR=$(node --version 2>/dev/null | sed -E 's/^v([0-9]+).*/\1/')
[ -n "$NODE_MAJOR" ] && [ "$NODE_MAJOR" -ge 20 ] && echo "OK ($NODE_MAJOR)" || echo "FAIL"
```

Se Node estiver ausente OU a major < 20, trate como FALHA (não prossiga) e mostre a instrução de upgrade:
- Mac via nvm: `nvm install 20 && nvm use 20`
- Mac via brew: `brew install node` (ou `brew upgrade node` se já instalado em versão antiga)
- Windows: `winget install OpenJS.NodeJS.LTS` (ou nvm-windows: `nvm install 20 && nvm use 20`)

Para a dependência obrigatória:
- ✅ se instalada com major ≥ 20, mostrando a versão
- ❌ se ausente OU major < 20, com a instrução exata de upgrade acima

Também detecte ferramentas opcionais pra uso futuro, mostrando como "disponível" (não bloqueador):
- FFmpeg: `ffmpeg -version 2>/dev/null | head -1` — paths comuns: `/opt/homebrew/bin/ffmpeg`, `/usr/local/bin/ffmpeg`, `/usr/bin/ffmpeg`. Install: `brew install ffmpeg` (Mac) ou `apt install ffmpeg` (Linux).
- Whisper.cpp: verificar `~/whisper.cpp/main`, `/usr/local/bin/whisper-cli`, `/opt/homebrew/bin/whisper-cli`. Install: `brew install whisper-cpp` (Mac) ou `git clone https://github.com/ggerganov/whisper.cpp.git ~/whisper.cpp && cd ~/whisper.cpp && make`.
- **Groq API key (opcional — transcrição rápida):** cheque `[ -n "${GROQ_API_KEY:-}" ] && echo "disponível"`. Se o membro tiver uma key da Groq no ambiente, a skill 03 (competitor analysis, ETAPA 3C) transcreve os vídeos dos concorrentes via API (`whisper-large-v3-turbo`) — muito mais rápido que o Whisper local. A cascade de transcrição é: Groq API (se key) → Whisper local → pedir o transcript ao membro. Sem a key, nada quebra.
- Python 3: `python3 --version` — necessário pra pipeline de design-clone (skill 07a — rotas clone-and-adapt e brand signals). Mac já vem com Python 3.
- **single-file-cli (opcional — snapshot de página, via npm):** usado por `tools/design-clone/snapshot.py` (rota clone-and-adapt da skill 07a) pra capturar uma página de referência inteira num único arquivo HTML. Não precisa instalar globalmente — roda on-demand via npx. Teste rápido: `npx -y -p single-file-cli single-file --help >/dev/null 2>&1 && echo "disponível"`. Se npm/npx estiver ausente ou o download falhar, nada quebra: a 07a degrada graciosamente pros próximos degraus da cascade de captura (screenshot → arquivo salvo manualmente pela extensão SingleFile do Chrome).
- **Playwright + Chromium (RECOMENDADO — coleta resiliente de pesquisa):** o fetcher `.claude/lib/web-fetch/fetch.py` usa um navegador real pra contornar bloqueios (Cloudflare/403/429/Reddit) nas skills 02 (VOC), 03 (PDPs/ads) e no design-clone da 07a. Como o python moderno é externally-managed (PEP 668), instale num venv:
  ```bash
  python3 -m venv .claude/lib/web-fetch/.venv
  .claude/lib/web-fetch/.venv/bin/pip install -r .claude/lib/web-fetch/requirements.txt
  .claude/lib/web-fetch/.venv/bin/playwright install chromium
  ```
  Se já existir `tools/design-clone/.venv` com Playwright, o fetcher reusa automaticamente — pode pular. Teste: `python3 .claude/lib/web-fetch/fetch.py https://example.com --json`. Sem isso, as skills 02/03 funcionam só com WebSearch/WebFetch (cobertura menor quando sites bloqueiam).
- **Venv do design-clone (RECOMENDADO — rotas clone-and-adapt e brand signals da 07a):** os scripts de `tools/design-clone/` (downloader, analyzer, pattern-extractor, liquid-converter) precisam de Playwright/bs4 num venv PRÓPRIO (mesma razão PEP 668). Crie logo após o venv do fetcher:
  ```bash
  python3 -m venv tools/design-clone/.venv
  tools/design-clone/.venv/bin/pip install -r tools/design-clone/requirements.txt
  tools/design-clone/.venv/bin/playwright install chromium
  ```
  O download do Chromium é compartilhado entre venvs (cache do Playwright em `~/Library/Caches/ms-playwright`) — se o passo anterior já baixou, este comando só registra e não baixa de novo. Todos os entry-points do design-clone fazem bootstrap re-exec automático (mesmo padrão do fetch.py): com o venv existindo, `python3 tools/design-clone/aura_clone.py ...` direto funciona. Se a criação falhar (sem rede, pip bloqueado), NÃO bloqueie o setup: avise que as rotas clone-and-adapt/brand-signals da 07a vão degradar pros degraus seguintes da cascade (single-file-cli → screenshot→visão → extensão SingleFile manual) e siga.

NÃO prossiga enquanto o Node não estiver OK. As opcionais ficam como aviso — mas instalar o Playwright cedo melhora MUITO a qualidade de market research/competitor analysis (sem ele, Reddit/Trustpilot/Amazon/Cloudflare bloqueiam). Detalhes em `.claude/rules/resilient-fetch.md`.

### ETAPA 2 — Verificação do MCP Aura

O sistema depende do MCP `aura` pra acessar a base de conhecimento. Teste com uma query real e relevante, não "test connection". Rode:

```
search_knowledge("market sophistication stages")
```

Verifique que a resposta retorna conteúdo real (não vazio, não erro). Se funcionar, mostre ✅ "Aura conectada e respondendo." (sem inventar números — a tool não retorna contagem de conteúdo). Se não:

"Rode no terminal, FORA do Claude Code (troque `SUA_CHAVE` pela chave de acesso que veio com o seu acesso Aura; se você não recebeu chave, use a URL sem o `?key=`):

```
claude mcp add aura --transport http "https://aura-mcp-production.up.railway.app/mcp?key=SUA_CHAVE"
```

Depois reinicie o Claude Code e digite 'setup' novamente."

NÃO prossiga sem o MCP funcionando.

### ETAPA 2.5 — Confirmação do Atalho `aura`

O alias `aura` (`cd ~/aura-engine && claude`) é criado automaticamente pelo hook AUTO-UPDATE do CLAUDE.md em toda sessão — membros novos e antigos recebem sem precisar refazer setup. Aqui, apenas confirme visualmente ao membro que já pode usar:

> "Atalho criado. Da próxima vez, basta abrir o Terminal e digitar: **aura**"

O hook cobre zsh, bash e fish (cada um recebe o alias no arquivo de config certo). Só oculte a mensagem acima se o shell do membro não for nenhum desses (ex: nushell) — nesse caso o hook pula silenciosamente.

### ETAPA 2.6 — Idioma dos Relatórios (PERGUNTA 1, ANTES DE QUALQUER OUTRA)

**ANTES de qualquer outra pergunta, pergunte o idioma.** Os relatórios internos (market research, competitor analysis, offer briefs, copy docs, ad strategy, audits, etc.) precisam ser gerados num idioma que o membro entenda — sem isso ele não consegue usar nada do que a Aura produz.

Pergunte exatamente assim, em português E em inglês na mesma mensagem (membro escolhe sem precisar entender uma das línguas):

> **Antes de tudo / Before we start:**
>
> Em qual idioma você quer os relatórios internos (market research, briefings, análises)?
> Which language do you want for internal reports (market research, briefings, analyses)?
>
> **1.** Português (padrão Brasil)
> **2.** English (international members)
>
> Responda só `1` ou `2` / Reply just `1` or `2`.

Capture a resposta em `REPORT_LANGUAGE`:
- `1` → `"pt-BR"`
- `2` → `"en"`

**A partir desse ponto, TODA conversa com o membro acontece no idioma escolhido.** Se ele escolheu inglês, faça as 4 perguntas da ETAPA 3 traduzidas, gere o `profile.md` em inglês, e a partir dali todas as skills futuras vão respeitar essa escolha lendo `profile.md.report_language`.

**Importante:** copy pro consumidor final (ads, landing pages, PDPs do mercado US) **continua sempre em inglês** independente dessa escolha. Essa escolha vale só pra documentação INTERNA do membro (relatórios, análises, briefings que ele lê pra entender o trabalho). A regra 0 do CLAUDE.md detalha.

### ETAPA 2.7 — Como a Aura funciona (só na primeira vez, no idioma escolhido)

Logo depois da escolha de idioma e ANTES das 4 perguntas, dê ao membro um resumo curto de como o sistema funciona — só na primeira vez (sem `workspace/profile.md`). Use o `REPORT_LANGUAGE` escolhido. Mantenha leve e claro, sem jargão.

**Se `pt-BR`:**

> Antes das perguntas, 30 segundos sobre como isso funciona:
>
> O Aura Engine é o seu time de marca e marketing num lugar só. Ele constrói sua operação **em fases**, e cada fase usa o que a anterior descobriu — você nunca repete informação:
>
> 1. **Pesquisa** (produto → mercado → concorrência): o que vender, pra quem, e o que os concorrentes deixam na mesa.
> 2. **Estratégia** (oferta → copy): a oferta irresistível e o texto que vende.
> 3. **Loja** (página → tracking → checkout → bônus → flows de recuperação): tudo numa página que converte, com medição certa, os bônus prometidos já prontos, e os emails de carrinho abandonado e pós-compra armados antes do primeiro anúncio.
> 4. **Tráfego** (criativos → visibilidade pra agentes de AI → auditoria → ads → análise → escala): os anúncios, a loja visível pros assistentes de compra com AI (ChatGPT, Perplexity), a checagem de coerência, subir e escalar.
> 5. **Pós-venda** (retenção completa → medição dos bônus → reciclagem): win-back e reposição por email/SMS, medição dos brindes, e 1 anúncio vencedor virando vários.
>
> Você dispara qualquer fase só falando o nome dela. Eu sempre te digo qual é o próximo passo. E cada produto ganha um painel — o **ABRIR-AQUI.html** — que mostra o que já está pronto e o que abrir.

**Se `en`:** mesma estrutura, traduzida naturalmente (Research → Strategy → Store (page → tracking → checkout → bonuses → recovery flows) → Traffic (creatives → AI-agent visibility → audit → ads → analysis → scale) → Post-purchase; "every product gets a dashboard — **ABRIR-AQUI.html** — showing what's done and what to open").

Se NÃO for primeira vez (membro refazendo setup), pule esta etapa.

### ETAPA 3 — Onboarding do Membro (Perguntas por Texto)

O onboarding é feito por perguntas de texto simples. Apresente as 4 perguntas numa única mensagem bem formatada e peça pro membro responder numa mensagem só, no formato que preferir. Isso reduz fricção e funciona em qualquer ambiente (inclusive dentro do Claude Code, que não tem TTY interativo).

**Use o idioma escolhido na ETAPA 2.6.** Se `REPORT_LANGUAGE = "en"`, traduz as 4 perguntas pra inglês.

Formato da mensagem a enviar:

> Preciso de 4 respostas rápidas pra salvar seu profile:
>
> **1. Situação atual:**
> - A) Não tenho produto — quero encontrar um
> - B) Tenho produto mas ainda não lancei
> - C) Já estou vendendo mas não escalo
> - D) Já escalo e quero otimizar
>
> **2. Budget diário pra ads** (em dólares — ex: `100`)
>
> **3. Ferramentas que você tem acesso** (marca as que se aplicam): TrendTrack · SpyBox · Higgsfield
>
> **3b. Plataforma de email (ESP)** que você usa — escolha uma:
> - A) Klaviyo
> - B) Omnisend / MailerLite / Shopify Email
> - C) Nenhum ainda
>
> **4. Link da sua loja e do produto principal** (se A, pula)
>  → Se tem Shopify, link da loja Shopify também.

Depois que o membro responder, parseie a resposta e extraia:
- `SITUACAO` → A, B, C ou D
- `BUDGET` → número em dólares
- `TOOLS` → lista das ferramentas mencionadas (TrendTrack, SpyBox, Higgsfield)
- `ESP` → plataforma de email escolhida na 3b: `klaviyo` (A), `omnisend` / `mailerlite` / `shopify_email` conforme o que o membro citar (B), ou `none` (C) — tokens EXATOS do enum do manifest-schema (`shopify_email` com underscore, nunca hífen)
- `LINK` → URL do produto principal (se SITUACAO ≠ A)
- `SHOPIFY_LINK` → URL da loja Shopify (se o membro informar a loja na pergunta 4)

Se o membro esquecer alguma resposta essencial, pergunte APENAS o que faltou — não re-apresente tudo.

Classifique o budget internamente pra uso futuro (não mostre ao membro). Intervalos fechados, sem sobreposição:
- < $50/dia → starter
- $50-199/dia → standard
- $200-999/dia → escala-inicial
- ≥ $1000/dia → escala-avançada

Capture TODAS as respostas (`SITUACAO`, `BUDGET`, `TOOLS`, `ESP`, `LINK`, `SHOPIFY_LINK`) pra usar na Etapa 4 (auto-extração) e Etapa 5 (salvar profile).

### ETAPA 4 — Auto-Extração de Dados da Loja

SE o membro forneceu link do produto, faça **web fetch da página** automaticamente antes de salvar o profile. Extraia:

- Nome do produto
- Preço (incluindo bundles se visíveis)
- Descrição principal
- Principais features/ingredientes
- Hero headline e sub-headline
- Se tem guarantee (tipo + duração)
- Tipo de hero section (vídeo, imagem, gif)
- Presença de mecanismo único (sim/não + nome se tiver)
- Link de checkout
- **Cores dominantes** — extraia os hex principais (background, texto, accent/CTA) do CSS ou do computed style da página (`:root` custom properties, classes de botão/header). Capture 3-5 hex.
- **Font-families** — extraia as `font-family` declaradas (heading e body) do CSS/`@font-face` ou computed style.

**Cascade de coleta (rule `.claude/rules/resilient-fetch.md`):** tente `WebFetch` primeiro. Se barrar (Cloudflare, 403, login wall) OU se precisar do CSS cru (o WebFetch devolve markdown, sem `<style>`/classes — inviável pra extrair cores/fontes), use o fetcher Playwright instalado na ETAPA 1: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode html` (devolve o HTML renderizado com CSS). Só depois desses dois degraus documente "não acessível" sem falhar. O importante é capturar o que consegue. Cores/fontes que não der pra extrair ficam como `[preencher]` na ETAPA 5A.

Salve tudo no profile pra servir de referência em TODAS as skills seguintes — nunca mais perguntamos essas informações ao membro.

### ETAPA 5 — Salvar Profile

**Antes de qualquer escrita**, garanta que o diretório de destino exista:

```bash
mkdir -p workspace/
mkdir -p workspace/[produto]/   # onde [produto] = slug gerado a partir do nome do produto (ver Etapa 5B)
```

Use os valores capturados das variáveis `SITUACAO`, `BUDGET`, `TOOLS`, `ESP`, `LINK` e `SHOPIFY_LINK` da Etapa 3 mais os dados extraídos na Etapa 4. Salve em `workspace/profile.md`:

```markdown
# Perfil do Membro

## Idioma dos relatórios
report_language: [pt-BR | en]

## Situação
Situação: [A / B / C / D — por extenso]
Classificação de budget: [starter / standard / escala-inicial / escala-avançada]
Budget diário: $[X]
Data do setup: [YYYY-MM-DD]

## Ferramentas
- TrendTrack: [sim/não]
- SpyBox: [sim/não]
- Higgsfield: [sim/não]
- Shopify: [sim + link / não — vem da pergunta 4]
- ESP (plataforma de email): [klaviyo / omnisend / mailerlite / shopify_email / none]

## Produto (se aplicável)
Link da loja: [url ou "N/A"]
Link do produto principal: [url ou "N/A"]

### Dados extraídos automaticamente da página (se link foi acessível):
- Nome do produto: [...]
- Preço base: [...]
- Bundles detectados: [...]
- Descrição: [...]
- Features/ingredientes principais: [...]
- Hero headline atual: "[...]"
- Sub-headline: "[...]"
- Guarantee atual: [tipo + duração ou "nenhum"]
- Mecanismo único atual: [nome ou "não identificado"]
- Link de checkout: [url]
```

### ETAPA 5A — Inicializar `brand.md` do produto (opcional, mas recomendado)

Se SITUACAO ≠ A (membro já tem produto), copie `.claude/templates/brand.md.template` pra `workspace/[produto]/brand.md` e preencha os fields que conseguiu extrair automaticamente na ETAPA 4 (dados da página):

- `{{ PRODUCT_SLUG }}` → slug do produto
- Paleta de cores: preencha com os hex dominantes (background, texto, accent/CTA) extraídos na ETAPA 4
- Fontes: preencha com as font-families (heading e body) extraídas na ETAPA 4
- Logo path: `workspace/[produto]/brand/logo.svg` (criar diretório; membro upa depois)

Fields que NÃO conseguiu extrair (página bloqueada, hex/fontes não detectados) ficam como placeholders `[preencher]`. Avise ao membro:

> "Criei `workspace/[produto]/brand.md` com o que consegui extrair da sua loja. Abre e completa o que ficou como `[preencher]` antes de rodar `page` — isso é single-source-of-truth pra identidade visual e editorial."

Se SITUACAO = A (sem produto ainda), pule essa etapa. A Skill 01 cria o `brand.md` do produto vencedor na etapa SALVAR dela (com os fields visuais como `[preencher]`, já que ainda não existe loja pra extrair). A skill 07a (page design) lê esse arquivo na brand discovery e só pergunta o que faltar.

> **Escape (ES1):** se `.claude/templates/brand.md.template` estiver ausente, não aborte — ofereça **(A)** gerar um `brand.md` mínimo inline com os fields auto-extraídos e o resto como `[preencher]`, OU **(B)** pular a criação do brand.md agora marcando `manifest.skipped_preflight += ["brand.md.template"]` e avisando que recomenda re-executar antes de `page`.

### ETAPA 5B — Criar Manifest (fonte única de verdade)

Paralelamente ao `profile.md`, crie o arquivo `workspace/[produto]/manifest.json`. Este é o **ÚNICO** local que todas as skills seguintes leem/atualizam para descobrir paths, progresso, e métricas. Substitui qualquer inferência manual de caminho.

- `product_slug` — gere via slugify do nome do produto detectado na Etapa 4 (lowercase, ASCII, hyphens; regex `^[a-z0-9-]+$`). Se não houver produto (Situação A), use `dev-placeholder-[YYYYMMDD]` e a skill 01 substituirá depois.
- `product_name` — nome humano do produto (ou "TBD — product research pending" para Situação A).
- `product_url` — URL informada pelo membro, se houver.
- `store_url` — URL da loja Shopify (de `SHOPIFY_LINK`), se o membro deu o link.
- `created_at` / `updated_at` — timestamps ISO-8601 UTC (mesmo valor inicial).
- `setup_complete: true`.
- `budget_daily` — o valor NUMÉRICO de `BUDGET` em dólares/dia (ex: `80`). É o campo canônico de budget que as skills leem (member-stage-awareness usa `budget_daily < 50` como sinal de stage; a 07c usa na decision tree do analytics stack) — grave sempre.
- `budget_tier` — mapeie de `BUDGET` (starter / standard / escala-inicial / escala-avancada). Campo ECONÔMICO derivado de `budget_daily`, separado de `stage`.
- `stage` — mapeie da `SITUACAO`: A/B → `starter`, C → `validating`, D → `scaling`.
- `market` — default `"US"`.
- `copy_language` — default `"en"` (copy consumidor-final é sempre inglês US).
- `report_language` — valor capturado em `REPORT_LANGUAGE` na ETAPA 2.6 (`pt-BR` ou `en`), espelhando o `profile.md`.
- `esp` — valor de `ESP` (`klaviyo` / `omnisend` / `mailerlite` / `shopify_email` / `none` — enum exato do manifest-schema).
- `product_vertical` — infira do nome/descrição auto-extraídos na ETAPA 4, usando EXCLUSIVAMENTE o enum do manifest-schema.json: `beauty` / `skincare` / `supplements` / `health` / `fitness` / `fashion` / `home` / `pet` / `food` / `financial` / `tech` / `education` / `other`. Se ambíguo, pergunte em 1 linha; default `"other"`.
- `skills_completed: ["00-setup"]`.

**Se SITUACAO = C ou D (já vende):** faça 2 perguntas opcionais rápidas (1 mensagem só) e grave o que vier:
- AOV médio aproximado → `aov_baseline` (número em dólares).
- Margem ou COGS aproximada por pedido → `cogs_estimate` (número em dólares).
Se o membro não souber/responder, deixe vazio. Para SITUACAO A/B deixe ambos vazios — a skill 04 (offer) preenche depois.

Schema completo em `.claude/templates/manifest-schema.json`. Valide contra o schema antes de salvar (estrutural; ignore propriedades opcionais ainda não preenchidas).

Exemplo:

```json
{
  "product_slug": "collagen-glow",
  "product_name": "Collagen Glow",
  "product_url": "https://example.com",
  "store_url": "https://example.myshopify.com",
  "created_at": "2026-04-16T13:00:00Z",
  "updated_at": "2026-04-16T13:00:00Z",
  "setup_complete": true,
  "budget_daily": 80,
  "budget_tier": "standard",
  "stage": "validating",
  "market": "US",
  "copy_language": "en",
  "report_language": "pt-BR",
  "esp": "klaviyo",
  "product_vertical": "skincare",
  "aov_baseline": 72,
  "cogs_estimate": 14,
  "skills_completed": ["00-setup"]
}
```

### ETAPA 6 — Confirmação + Roteamento Inteligente

Comece com uma confirmação clara: `✓ Setup completo!`

Depois apresente a mensagem de próximo passo baseada na situação do membro (A/B/C/D). Essa lógica vem do princípio operacional: cada fase alimenta a próxima, mas o ponto de entrada depende do que já existe.

**Situação A — Não tem produto:**

"Setup completo. Seu perfil está salvo.

Começa pela fase de descoberta: diga **'product research'** pra encontrar um produto pra validar.

O sistema vai te guiar na filtragem (Kalodata/SpyBox, ou fontes públicas se não tiver), análise estratégica (market desires, sophistication, awareness), e ranking dos candidatos. Só depois disso partimos pra oferta e copy."

**Situação B — Tem produto, não lançou:**

"Setup completo. Perfil salvo — já extraí o que pude da sua página do [nome do produto].

Próximo passo: **'market research'**. Vou montar o Unified Research Brief do seu produto — a fundação de tudo que vem depois. Psicografia profunda do público, awareness/sophistication do mercado, voz do cliente, objeções, gaps de concorrentes. Esse documento alimenta copy, criativos, e estratégia de ads."

**Situação C — Vendendo mas não escala:**

"Setup completo. O problema aqui geralmente não é o produto — é diagnóstico.

Começa por **'ad analysis'**. Cole os dados do Ads Manager que eu rodo 4Pi completo (Spend → Frequency → CPM → Cost per Result) e digo exatamente o que tá emperrando: criativo em fadiga, oferta fraca, página incongruente, posição de funil desbalanceada, ou problema de tracking. Depois do diagnóstico a gente decide se o próximo passo é 'creatives', 'copy', 'offer', ou 'scale'."

**Situação D — Escala, quer otimizar:**

"Setup completo. Modo otimização.

Próximo passo: **'scale'**. Monto um plano baseado nos seus números — PGS pra escala vertical sistemática, análise de PSM pra garantir margem de crescimento, roadmap de canais horizontais (Google Search, TikTok, Amazon) quando fizer sentido, e ritmo de criativos/offers alinhado à faixa de faturamento que você tá operando."

Depois da mensagem específica, adicione SEMPRE:

"Você pode dizer o nome de qualquer fase a qualquer momento (a lista abaixo segue a ordem em que elas rodam):
`product research` · `market research` · `competitor analysis` · `offer` · `copy` · `page` · `build page` (ou `deploy`) · `tracking` (ou `pixel` / `capi`) · `checkout` (ou `upsell` / `aov`) · `bonus delivery` (ou `bônus`) · `retention` (ou `email flows` / `klaviyo`) · `creatives` · `agentic readiness` (ou `ai visibility`) · `consistency audit` (ou `audit`) · `ad strategy` · `ad analysis` · `scale` · `content recycler` (ou `recycle`)

Cada fase lê o que as anteriores produziram em workspace/[produto]/ — você nunca precisa repetir informação.

Seu ponto de partida é sempre o painel: abre **workspace/[produto]/ABRIR-AQUI.html** no navegador pra ver tudo que já foi feito, abrir qualquer relatório, e saber o próximo passo."

(Se `REPORT_LANGUAGE = "en"`, traduza essa adição também — inclusive a frase do painel: "Your home base is the dashboard: open **workspace/[product]/ABRIR-AQUI.html** to see everything done, open any report, and know the next step.")

## SALVAR (dual output — rule 6b do CLAUDE.md)

Garanta `mkdir -p workspace/` e `mkdir -p workspace/[produto]/` antes de qualquer write.

Salve em QUATRO arquivos:
1. **`workspace/profile.md`** (formato da Etapa 5 — a AI lê nas fases seguintes)
2. **`workspace/profile.html`** (visualização humana — use `.claude/templates/aura-report-template.html` como base, self-contained com CSS inline + logo SVG do Aura (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto))
3. **`workspace/[produto]/manifest.json`** (Etapa 5B — fonte única de verdade para todas as próximas skills)
4. **`workspace/[produto]/brand.md`** (Etapa 5A — apenas se SITUACAO ≠ A; copiado de `.claude/templates/brand.md.template` com fields auto-extraídos preenchidos)

**Validação do template HTML**: antes de escrever `profile.html`, confirme que `.claude/templates/aura-report-template.html` existe (`test -f`). Se NÃO existir, gere um HTML mínimo inline com CSS básico e a logo SVG copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` (arquivo independente do template — pode existir mesmo com o template ausente) + o CSS mínimo da logo (`.logo-wrap { margin-bottom: 30px; } .logo-wrap svg { height: 28px; width: auto; }`), e um aviso no topo: `<!-- WARNING: template .claude/templates/aura-report-template.html missing; fallback HTML in use -->`. Só se o snippet da logo TAMBÉM estiver ausente, PARE e peça ajuda ao membro (regra 6b do CLAUDE.md — nunca cabeçalho textual no lugar da logo). Template ausente sozinho nunca aborta o setup.

Se o membro já tinha um profile anterior e está refazendo, faça backup em `workspace/.profile-backup-[YYYYMMDD-HHMMSS].md` e do manifest em `workspace/[produto]/.manifest-backup-[YYYYMMDD-HHMMSS].json` antes de sobrescrever.

**5. Gerar o painel do produto.** Depois de salvar o manifest, rode via Bash pra criar a porta de entrada do membro:

```bash
python3 .claude/lib/workspace-index/build_index.py [product_slug]
```

Isso gera `workspace/[produto]/ABRIR-AQUI.html` — o painel que lista cada fase, o que já foi feito e o próximo passo. Toda skill seguinte regenera esse painel ao terminar, então ele está sempre atualizado. Estrutura canônica das pastas do produto em `.claude/lib/workspace-index/workspace-layout.md`.

## Mensagem Final

Já coberta na Etapa 6 — roteamento específico pela situação (A/B/C/D).

Adicione ao final da confirmação:

> O `manifest.json` em `workspace/[produto]/manifest.json` é a **fonte única de verdade**. Todas as próximas skills leem e atualizam este arquivo automaticamente. **NUNCA edite manualmente** — isso corrompe a coordenação entre skills.
