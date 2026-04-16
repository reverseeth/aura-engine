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

### ETAPA 1 — Verificação de Dependências

Antes de qualquer pergunta, verifique se o ambiente técnico está OK. Dependência obrigatória: **Node.js v20+**.

**Node.js** — detecte de forma inteligente:

```bash
# Node via direct
node --version 2>/dev/null

# Node via nvm
[ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh" && nvm current 2>/dev/null

# Node via brew
/opt/homebrew/bin/node --version 2>/dev/null
/usr/local/bin/node --version 2>/dev/null
```

Se não encontrar:
- Mac via nvm: `nvm install 20 && nvm use 20`
- Mac via brew: `brew install node`

Para a dependência obrigatória:
- ✅ se instalada, com versão
- ❌ se não, com instrução exata

Também detecte ferramentas opcionais pra uso futuro, mostrando como "disponível" (não bloqueador):
- FFmpeg: `ffmpeg -version 2>/dev/null | head -1` — paths comuns: `/opt/homebrew/bin/ffmpeg`, `/usr/local/bin/ffmpeg`, `/usr/bin/ffmpeg`. Install: `brew install ffmpeg` (Mac) ou `apt install ffmpeg` (Linux).
- Whisper.cpp: verificar `~/whisper.cpp/main`, `/usr/local/bin/whisper-cli`, `/opt/homebrew/bin/whisper-cli`. Install: `brew install whisper-cpp` (Mac) ou `git clone https://github.com/ggerganov/whisper.cpp.git ~/whisper.cpp && cd ~/whisper.cpp && make`.
- Python 3: `python3 --version` — necessário pra pipeline de design-clone (skill 06 modo B). Mac já vem com Python 3.
- Playwright + BeautifulSoup (opcional — só pra design-clone no modo B da skill 06): `python3 -c "import playwright, bs4" 2>&1`. Install: `pip install -r tools/design-clone/requirements.txt && playwright install chromium`. Se o membro não for usar design-clone, pode deixar pra instalar depois.

NÃO prossiga enquanto o Node não estiver OK. As ferramentas opcionais podem ficar como aviso — se o membro indicar que vai usar a skill 06 em modo de clone de design, sinalize que Playwright + BeautifulSoup precisam ser instalados antes.

### ETAPA 2 — Verificação do MCP Aura

O sistema depende do MCP `aura` pra acessar a base de conhecimento. Teste com uma query real e relevante, não "test connection". Rode:

```
search_knowledge("market sophistication stages")
```

Verifique que a resposta retorna conteúdo real (não vazio, não erro). Se funcionar, mostre ✅ "Aura conectada (XX notas disponíveis)". Se não:

"Rode no terminal, FORA do Claude Code:

```
claude mcp add aura --transport http https://aura-mcp-production.up.railway.app/mcp
```

Depois reinicie o Claude Code e digite 'setup' novamente."

NÃO prossiga sem o MCP funcionando.

### ETAPA 2.5 — Confirmação do Atalho `aura`

O alias `aura` (`cd ~/aura-engine && claude`) é criado automaticamente pelo hook AUTO-UPDATE do CLAUDE.md em toda sessão — membros novos e antigos recebem sem precisar refazer setup. Aqui, apenas confirme visualmente ao membro que já pode usar:

> "Atalho criado. Da próxima vez, basta abrir o Terminal e digitar: **aura**"

Se o shell do membro não for zsh nem bash (ex: fish, nushell), o hook pula silenciosamente — nesse caso não mostre a mensagem acima.

### ETAPA 3 — Onboarding do Membro (Perguntas por Texto)

O onboarding é feito por perguntas de texto simples. Apresente as 4 perguntas numa única mensagem bem formatada e peça pro membro responder numa mensagem só, no formato que preferir. Isso reduz fricção e funciona em qualquer ambiente (inclusive dentro do Claude Code, que não tem TTY interativo).

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
> **3. Ferramentas que você tem acesso** (marca as que se aplicam): SpyBox · Shopify · ElevenLabs · Meta Ads Manager
>
> **4. Link da sua loja e do produto principal** (se A, pula)
>  → Se tem Shopify, link da loja Shopify também.

Depois que o membro responder, parseie a resposta e extraia:
- `SITUACAO` → A, B, C ou D
- `BUDGET` → número em dólares
- `TOOLS` → lista das ferramentas mencionadas (SpyBox, Shopify, ElevenLabs, Meta Ads Manager)
- `LINK` → URL do produto principal (se SITUACAO ≠ A)
- `SHOPIFY_LINK` → URL da loja Shopify (se TOOLS contém Shopify)

Se o membro esquecer alguma resposta essencial, pergunte APENAS o que faltou — não re-apresente tudo.

Classifique o budget internamente pra uso futuro (não mostre ao membro):
- < $50/dia → starter
- $50-200/dia → standard
- $200-1000/dia → escala-inicial
- $1000+/dia → escala-avançada

Capture TODAS as respostas (`SITUACAO`, `BUDGET`, `TOOLS`, `LINK`, `SHOPIFY_LINK`) pra usar na Etapa 4 (auto-extração) e Etapa 5 (salvar profile).

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

Se a página estiver bloqueada (Cloudflare, login wall), documente "não acessível" sem falhar. O importante é capturar o que consegue.

Salve tudo no profile pra servir de referência em TODAS as skills seguintes — nunca mais perguntamos essas informações ao membro.

### ETAPA 5 — Salvar Profile

Use os valores capturados das variáveis `SITUACAO`, `BUDGET`, `TOOLS`, `LINK` e `SHOPIFY_LINK` da Etapa 3 mais os dados extraídos na Etapa 4. Salve em `/workspace/profile.md`:

```markdown
# Perfil do Membro

## Situação
Situação: [A / B / C / D — por extenso]
Classificação de budget: [starter / standard / escala-inicial / escala-avançada]
Budget diário: $[X]
Data do setup: [YYYY-MM-DD]

## Ferramentas
- SpyBox: [sim/não]
- Shopify: [sim + link / não]
- ElevenLabs: [sim/não]
- Meta Ads Manager: [sim + conta ativa / não]

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

Próximo passo: **'scale'**. Monto um plano baseado nos seus números — PGS pra escala vertical sistemática, análise de PSM pra garantir margem de crescimento, roadmap de canais horizontais (Google Search, TikTok, Amazon) quando fizer sentido, e ritmo de criativos/offers alinhado ao revenue tier que você tá operando."

Depois da mensagem específica, adicione SEMPRE:

"Você pode dizer o nome de qualquer fase a qualquer momento:
`product research` · `market research` · `competitor analysis` · `offer` · `copy` · `page` · `creatives` · `ad strategy` · `ad analysis` · `scale`

Cada fase lê o que as anteriores produziram em /workspace/[produto]/ — você nunca precisa repetir informação."

## SALVAR (dual output — rule 6b do CLAUDE.md)

Salve em DOIS arquivos:
1. **`/workspace/profile.md`** (formato da Etapa 5 — a AI lê nas fases seguintes)
2. **`/workspace/profile.html`** (visualização humana — use `.claude/templates/aura-report-template.html` como base, self-contained com CSS inline + logo SVG do Aura)

Se o membro já tinha um profile anterior e está refazendo, faça backup em `/workspace/.profile-backup-[YYYYMMDD-HHMMSS].md` antes de sobrescrever.

## Mensagem Final

Já coberta na Etapa 6 — roteamento específico pela situação (A/B/C/D).
