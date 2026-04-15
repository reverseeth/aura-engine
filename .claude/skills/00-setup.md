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

Antes de qualquer pergunta, verifique se o ambiente técnico está OK. Dependências obrigatórias: **Node.js v20+** e **gum** (charmbracelet/gum — usado pra tornar o onboarding interativo com setas, checkboxes e inputs visuais).

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

**gum** — verifique e instale silenciosamente se não existir:

```bash
# Verificação
if ! command -v gum >/dev/null 2>&1; then
  # Instalação silenciosa por OS
  if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install gum >/dev/null 2>&1
  else
    sudo apt install -y gum >/dev/null 2>&1 || go install github.com/charmbracelet/gum@latest >/dev/null 2>&1
  fi
fi
```

Para cada dependência obrigatória:
- ✅ se instalada, com versão
- ❌ se não, com instrução exata

Também detecte ferramentas opcionais pra uso futuro, mostrando como "disponível" (não bloqueador):
- FFmpeg: `ffmpeg -version 2>/dev/null | head -1` — paths comuns: `/opt/homebrew/bin/ffmpeg`, `/usr/local/bin/ffmpeg`, `/usr/bin/ffmpeg`. Install: `brew install ffmpeg` (Mac) ou `apt install ffmpeg` (Linux).
- Whisper.cpp: verificar `~/whisper.cpp/main`, `/usr/local/bin/whisper-cli`, `/opt/homebrew/bin/whisper-cli`. Install: `brew install whisper-cpp` (Mac) ou `git clone https://github.com/ggerganov/whisper.cpp.git ~/whisper.cpp && cd ~/whisper.cpp && make`.

NÃO prossiga enquanto Node e gum não estiverem OK. As ferramentas opcionais podem ficar como aviso.

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

### ETAPA 3 — Onboarding do Membro (Interativo via gum)

O onboarding é 100% visual. O membro só digita quando é input de texto livre (budget, link). Pra situação e ferramentas, ele navega com setas e marca com espaço. Execute cada comando `gum` via Bash, UM DE CADA VEZ, e capture o stdout pra salvar depois no profile.

**Pergunta 1 — Situação atual (seta + enter, escolha única):**

```bash
SITUACAO=$(gum choose \
  --header "Qual sua situação agora?" \
  --cursor.foreground="#FF6B35" \
  "A) Não tenho produto — quero encontrar um" \
  "B) Tenho produto mas ainda não lancei" \
  "C) Já estou vendendo mas não escalo" \
  "D) Já escalo e quero otimizar")
```

**Pergunta 2 — Budget (input de texto):**

```bash
BUDGET=$(gum input \
  --header "Qual seu budget diário disponível pra ads? (em dólares)" \
  --placeholder "50" \
  --prompt "> $")
```

Classifique internamente pra uso futuro (não mostre ao membro):
- < $50/dia → starter
- $50-200/dia → standard
- $200-1000/dia → escala-inicial
- $1000+/dia → escala-avançada

**Pergunta 3 — Ferramentas (checkbox múltiplo, espaço pra marcar, enter pra confirmar):**

```bash
TOOLS=$(gum choose --no-limit \
  --header "Quais ferramentas você tem acesso? (espaço pra marcar, enter pra confirmar)" \
  --cursor.foreground="#FF6B35" \
  --selected.foreground="#22C55E" \
  "SpyBox" \
  "Shopify" \
  "ElevenLabs" \
  "Meta Ads Manager")
```

**Pergunta 4 — Link do produto (condicional):**

SE a variável `SITUACAO` NÃO começa com "A)", pergunte:

```bash
if [[ "$SITUACAO" != *"A)"* ]]; then
  LINK=$(gum input \
    --header "Me manda o link da sua loja e do produto principal" \
    --placeholder "https://sualoja.com" \
    --prompt "> ")
fi
```

**Pergunta 5 — Link da Shopify (condicional):**

SE "Shopify" aparece no output de TOOLS, pergunte:

```bash
if echo "$TOOLS" | grep -q "Shopify"; then
  SHOPIFY_LINK=$(gum input \
    --header "Qual o link da sua loja Shopify?" \
    --placeholder "https://sualoja.com" \
    --prompt "> ")
fi
```

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

### ETAPA 6 — Confirmação Visual + Roteamento Inteligente

Antes da mensagem de roteamento, mostre uma confirmação visual destacada usando gum:

```bash
gum style \
  --border normal \
  --padding "1 2" \
  --border-foreground "#22C55E" \
  "✓ Setup completo!"
```

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
`product research` · `market research` · `competitor analysis` · `offer` · `copy` · `creatives` · `ad strategy` · `ad analysis` · `scale` · `page`

Cada fase lê o que as anteriores produziram em /workspace/[produto]/ — você nunca precisa repetir informação."

## SALVAR

`/workspace/profile.md` (formato da Etapa 5).

Se o membro já tinha um profile anterior e está refazendo, faça backup em `/workspace/.profile-backup-[YYYYMMDD-HHMMSS].md` antes de sobrescrever.

## Mensagem Final

Já coberta na Etapa 6 — roteamento específico pela situação (A/B/C/D).
