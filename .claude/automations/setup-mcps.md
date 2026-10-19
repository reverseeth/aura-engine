# Setup MCPs — guia 15min

Setup único. Depois disso, Claude Code executa operações em Meta Ads + Shopify via linguagem natural.

## Stack atual (recomendada — julho/2026)

Aura usa **cascade resiliente** com 2 MCPs Meta em paralelo. Você instala os dois; Aura tenta o oficial primeiro e cai pro 3rd party automaticamente se o oficial não estiver disponível pra seu ad account (rollout gradual).

| MCP | Propósito | Status |
|---|---|---|
| **Meta MCP oficial** (`mcp.facebook.com/ads`) | Caminho preferencial — 29 tools, OAuth Business Suite, industry benchmarks, dataset quality | Open beta desde 2026-04-29, rollout gradual, ainda sem GA |
| **Marketing API com System User** (via `pipeboard-co/meta-ads-mcp`) | Fallback automático quando o oficial não responde ou está disabled. Token de usuário de sistema, que não expira | API oficial da Meta, GA |
| **Shopify AI Toolkit** (plugin Claude Code) | Operações Shopify (produto, theme, store execute) + validação Liquid/GraphQL | Oficial, abril/2026 — **ver alerta de telemetria no passo 4** |

Opcionais que enriquecem skills específicas: `GROQ_API_KEY` (1.5 — transcrição de criativos na Skill `competitor-analysis`), Refero (3.5), Klaviyo (3.6), **Higgsfield** (3.7 — vídeo in-session na Skill `creative-engine` e imagem da página na Skill `page-design`), **Foreplay** (3.8 — ad spy nas Skills `competitor-analysis`/`creative-engine`/`ad-analysis`), **postagem no Instagram** (3.10 — API oficial pelo System User, ou Blotato e Metricool, na Skill `social-engine`), Shopify Dev + Stripe (4.5).

## 1. Instalar dependências (2min)

```bash
# Python (pro Pipeboard fallback + Playwright)
pip3 install meta-ads-mcp playwright
```

> O SDK do Model Context Protocol NÃO precisa ser instalado à parte — `meta-ads-mcp` já declara as próprias dependências.

O MCP oficial **não precisa de instalação local** — é remote, conecta via URL.

## 1.4. FFmpeg (recomendado, 1min — Limpador de Metadados pra vídeo)

O Limpador de Metadados (2 cliques em `Limpador de Metadados` na pasta da Aura, ou `bash tools/strip-metadata.sh`) limpa imagens só com o Node. Pra vídeo e áudio ele usa o ffmpeg (stream copy, sem re-encodar):

```bash
brew install ffmpeg            # Mac
winget install Gyan.FFmpeg     # Windows (depois feche e abra o terminal)
```

## 1.5. (Opcional) GROQ_API_KEY — transcrição de criativos (Skill `competitor-analysis` ETAPA 3C)

Não é MCP, mas mora aqui porque é setup de integração: a análise profunda de criativos escalados dos concorrentes (Skill `competitor-analysis` ETAPA 3C) transcreve os vídeos com um cascade de 3 degraus — **Groq API (`whisper-large-v3-turbo`) → Whisper local → transcript colado pelo membro**. O degrau 1 é o preferencial: rápido, ~$0.02-0.04 por hora de áudio, zero instalação.

```bash
# 1. Criar key grátis em https://console.groq.com/keys
# 2. Exportar no shell (adicionar ao ~/.zshrc ou ~/.bashrc pra persistir):
export GROQ_API_KEY=gsk_...
# 3. Testar:
test -n "$GROQ_API_KEY" && echo "ok"
```

Sem a key, nada trava — a Skill `competitor-analysis` cai pro Whisper local (se instalado) ou pede o transcript ao membro. Detalhes do cascade completo na própria Skill `competitor-analysis` (ETAPA 3C).

## 2. Conectar Meta MCP oficial (3min — caminho preferencial)

### Claude Desktop
1. Settings → Connectors → "+ Add custom connector"
2. Nome: `meta`
3. URL: `https://mcp.facebook.com/ads`
4. OAuth login via Business Suite quando pedir
5. Aprove permissões granulares por ad account / Page
6. Feche e reabra o Claude Desktop

### Claude Code (terminal)
```bash
claude mcp add --transport http meta https://mcp.facebook.com/ads
```
Reinicie o Claude Code. Na primeira chamada de tool, vai pedir OAuth no browser.

### Testar
```
Claude, lista minhas Meta ad accounts.
```

Se retornar lista → conectado. Se erro `account_disabled_in_official_beta` em alguma conta → essa conta ainda não foi liberada no rollout gradual. Não é problema: o fallback Pipeboard cobre.

## 3. Conectar a Marketing API oficial com System User (10min, caminho que não expira)

A Marketing API é a API oficial da Meta pra anúncios. O acesso é por um **System User** (usuário de sistema) do Business Manager: um usuário técnico, sem login de pessoa, com um token que não expira e que só enxerga os ativos que você entregar pra ele. É esse token que roda o MCP `meta-ads` (Pipeboard). Mesmo que o oficial do passo 2 funcione hoje, faça este passo: quando alguma conta estiver "disabled" no rollout do oficial, a Aura cai aqui sem interrupção.

### A. Conta de anúncios aquecida

Use uma conta de anúncios que já tenha histórico de gasto e de pagamento. Conta recém-criada operada por API desde o primeiro dia tem mais chance de revisão e bloqueio.

### B. Criar o System User no Business Manager

1. https://business.facebook.com/settings → **Usuários → Usuários do sistema → Adicionar**.
2. Nome `aura`, função **Admin** (a função Funcionário não gera token com permissão de gestão de anúncios em todos os casos).

### C. Criar o app no Meta for Developers

1. https://developers.facebook.com/apps → **Criar app**, tipo **Business** (Empresa), vinculado ao seu Business Manager.
2. No painel do app, adicione o produto **Marketing API**.
3. Pra postar no Instagram pela API (Skill `social-engine`, passo 3.10), adicione também o produto **Instagram** (API com login do Facebook).

O app começa no nível de acesso de desenvolvimento da Marketing API, com limite baixo de chamadas. Quando a operação crescer, peça o **Ads Management Standard Access** na Revisão do app; até lá, o limite de desenvolvimento dá conta de uma ou duas contas.

### D. Entregar os ativos ao System User

Em **Usuários do sistema → aura → Atribuir ativos**, entregue só o que a operação usa, com a permissão mínima:

| Ativo | Permissão |
|---|---|
| Conta de anúncios | Gerenciar campanhas |
| Página do Facebook da marca | Criar conteúdo + Anúncios |
| Pixel / conjunto de dados | Usar |
| Conta do Instagram (se for publicar) | Conteúdo |
| O app criado no 3.3 | Desenvolver app |

### E. Gerar o token

1. **Usuários do sistema → aura → Gerar novo token**, escolha o app do passo C.
2. Validade: **Nunca expira**.
3. Permissões: `ads_management`, `ads_read`, `business_management`, `pages_read_engagement`, `pages_show_list`. Pra publicar no Instagram, some `instagram_basic` e `instagram_content_publish`.
4. Copie o token **uma vez** e cole direto no comando do passo F.

O token é segredo. Nunca cole no chat com o Claude, nunca salve dentro da pasta da Aura, nunca mande em print. Ele vive só no registro do MCP (que fica fora do repositório) ou num gerenciador de senhas seu.

### F. Registrar como `meta-ads`

Rode no **seu terminal**, fora do Claude (não use o `!` dentro da sessão: o comando apareceria na conversa), colando o token e o ID da conta reais. Não use `$(cat ...)`: valores de env de MCP são passados literalmente, sem shell pra expandir, e toda chamada falharia com "Invalid OAuth access token".

```bash
claude mcp add meta-ads \
  --env META_ACCESS_TOKEN=<COLA_O_TOKEN_AQUI> \
  --env META_DEFAULT_AD_ACCOUNT=act_123456789 \
  -- meta-ads-mcp
```

O ID da conta (`act_` + número) está no Gerenciador de Anúncios, no seletor de contas. Reinicie o Claude Code e teste: "Claude, lista minhas Meta ad accounts." Se o token vazar ou um membro do time sair, gere um novo no passo E (o antigo é revogado) e re-registre com `claude mcp remove meta-ads` seguido do mesmo `claude mcp add`.

> **Importante — naming:** o connector oficial usa `meta` (vira tools `mcp__meta__*`). O Pipeboard usa `meta-ads` (vira tools `mcp__meta-ads__*`). Não troque os nomes — as receitas detectam por prefixo.

### G. Como a Aura opera a conta

Regra de toda receita e skill que escreve na conta (`.claude/automations/README.md`, Segurança): uma operação por vez, na ordem das dependências (campanha → conjunto → criativo → anúncio), conferindo o resultado de cada uma antes da próxima; tudo nasce pausado; limite de chamadas respeitado com espera e nova tentativa só em leitura; erro de escrita para a sequência e volta pro membro, nunca é repetido às cegas.

## 3.5. Conectar Refero MCP (opcional, 2min — design system curado)

Se o membro quer alimentar a skill `page-design` Brand Discovery com design systems curados de top sites (~200 sites premium tipo Cursor, Linear, Vercel), conecte o Refero MCP. Sem ele, Aura cai pro `tools/design-clone/` (Playwright) ou pergunta manual.

```bash
claude mcp add refero -- npx -y fidgetcoding-refero-mcp
```

Opcional (qualidade de busca):

```bash
# Pra semantic search via embeddings (default cai pra BM25 keyword)
export OPENAI_API_KEY="sk-..."

# Pra Refero escrever DESIGN.md direto no workspace
export REFERO_MCP_VAULT_DIR="$HOME/aura-engine/workspace"
```

Reinicie o Claude Code. Tools com prefixo `mcp__refero__` aparecem. Sem auth obrigatória — o `mcp_token` que aparece na URL do `styles.refero.design` é só do front-end web, não do MCP.

**Testar:**
```
Claude, vibe search no refero pra "editorial premium magazine"
```

Detalhes completos em `.claude/lib/refero-integration/README.md`.

## 3.6. Conectar Klaviyo MCP (opcional, 3min — automação de retention flows)

Se o membro usa Klaviyo e quer que a **Skill `retention-engine`** crie os flows direto (welcome / abandoned-cart / post-purchase / win-back / replenishment) com contrato estável — em vez de só gerar HTML + setup-guide pra importar à mão — conecte o **MCP oficial da Klaviyo**.

### Claude Desktop (servidor remoto, OAuth)
1. Settings → Connectors → "+ Add custom connector"
2. Nome: `klaviyo`
3. URL do servidor remoto oficial (em https://developers.klaviyo.com/en/docs/klaviyo_mcp_server) + OAuth quando pedir
4. Aprove permissões de flows + profiles + events

### Claude Code (servidor local via uv)
Gere uma Private API Key no Klaviyo (Settings → API Keys) e registre:

```bash
claude mcp add klaviyo \
  --env PRIVATE_API_KEY=pk_... \
  --env READ_ONLY=false \
  -- uvx klaviyo-mcp-server@latest
```

(Requer `uv` instalado: `pip3 install uv`.) Reinicie. 

### Testar
```
Claude, lista meus flows no Klaviyo.
```

Se retornar lista → conectado (tools `mcp__klaviyo__*` disponíveis). Sem ele, a Skill `retention-engine` cai pro caminho de **assets + setup-guide** (HTML pronto + guia manual), que continua sendo o fallback confiável. Os flows criados via MCP ficam SEMPRE em draft — o membro revisa e ativa no Klaviyo UI (a skill nunca ativa sozinha, pra não arriscar spam).

## 3.7. Conectar Higgsfield MCP (opcional, 2min — vídeo e imagem gerados na própria sessão)

Fecha o único passo manual do pipeline de criativos: sem ele, a **Skill `creative-engine`** entrega prompts prontos pra você colar no Higgsfield; com ele, a skill gera o prompt E **renderiza o vídeo na própria sessão**, salvando o `.mp4` em `workspace/[produto]/creative-engine/renders/`. O mesmo MCP também gera **as imagens que faltam na página**: a **Skill `page-design`** (sub-etapa 1.6.3) preenche os slots do mapa de mídia que você não tem foto, lê cada imagem gerada e só usa a que passa na régua de imagem dela.

É o MCP oficial hospedado da Higgsfield (lançado 2026-04-30): OAuth via browser, sem API key, usa os créditos do plano que você já tem. Expõe 30+ modelos (Kling 3.x, Veo 3.1, Sora 2, Seedance, MiniMax Hailuo), output sem watermark em plano pago.

### Claude Desktop
Settings → Connectors → "+ Add custom connector" → nome `higgsfield`, URL `https://mcp.higgsfield.ai/mcp` → OAuth quando pedir.

### Claude Code
```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
```

Reinicie. Tools com prefixo `mcp__higgsfield__` aparecem — a Skill `creative-engine` (ETAPA 0.7) e a Skill `page-design` (1.6.3) detectam sozinhas e **perguntam antes de gastar créditos** ("quer que eu renderize os N vídeos ou prefere só os prompts?"; "faltam imagens em N slots, gero agora?"). Sem o MCP, nada muda: uma entrega os prompts como sempre, a outra segue com as suas fotos.

## 3.8. Conectar Foreplay MCP (opcional, 2min — ad spy)

Fonte de criativos escalados dos concorrentes (200M+ ads em Facebook/Instagram/TikTok/YouTube/LinkedIn, busca por marca e domain intelligence). Com ele conectado, a **Skill `competitor-analysis`** puxa os criativos escalados sem pedir screenshots/uploads, e as **Skills `creative-engine`/`ad-analysis`** ganham sinal de hooks/formatos ativos no nicho. Requer conta Foreplay (usa o plano + créditos de API que você já tem).

### Claude Desktop
Settings → Connectors → "+ Add custom connector" → nome `foreplay`, URL `https://public.api.foreplay.co/mcp` → sign-in com a conta Foreplay.

### Claude Code
```bash
claude mcp add --transport http foreplay https://public.api.foreplay.co/mcp
```

Reinicie. Tools com prefixo `mcp__foreplay__` aparecem; as skills detectam sozinhas. Sem ele, as skills seguem o método tradicional (TrendTrack MCP se houver, Meta Ad Library público, uploads do membro) — silent fallback, nada trava.

## 3.9. Conectar Notion MCP (opcional, 2min — banco de marcas da pesquisa de produto)

A **Skill `product-research`** salva o banco de marcas (uma página por marca com LP mais escalada, ads mais escalados, tráfego, oferta, mecanismos, Trustpilot, Trends e a jogada recomendada, mais uma página de ranking) direto no seu Notion. Sem ele, a skill salva o mesmo banco em HTML na pasta do produto.

### Claude Desktop / claude.ai
Settings → Connectors → **Notion** (connector oficial) → conectar e autorizar o workspace. As tools aparecem com prefixo `mcp__claude_ai_Notion__` (o Claude Code logado na mesma conta enxerga as mesmas tools).

### Claude Code (registro local)
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```
Reinicie e autorize no browser. Tools com prefixo `mcp__notion__` aparecem; a Skill `product-research` detecta qualquer prefixo com `notion` sozinha.

## 3.10. Postagem automática no Instagram (opcional, 5min — Skill `social-engine`)

O Higgsfield gera as imagens, mas não posta no Instagram. O padrão da Aura é a **API oficial do Instagram**, pelo mesmo System User do passo 3: grátis, sem intermediário e sem mensalidade. A conta do Instagram precisa ser **Business ou Creator** e estar ligada à página do Facebook da marca.

### API oficial do Instagram (padrão)

1. No app do passo 3 (C), adicione o produto **Instagram** (API com login do Facebook).
2. Em **Usuários do sistema → aura → Atribuir ativos**, entregue a conta do Instagram da marca com permissão de conteúdo.
3. Gere o token de novo (passo 3, E) somando `instagram_basic` e `instagram_content_publish` às permissões. Re-registre o `meta-ads` com o token novo (passo 3, F).
4. **Guarde o token como segredo da rotina:** em https://claude.ai/code, edite o ambiente na nuvem que a rotina usa → **Network secrets → Add secret** → tipo **Bearer**, site permitido `graph.facebook.com`, cabeçalho `Authorization` com prefixo `Bearer` e o token como valor. O proxy da Anthropic põe o token na requisição depois que ela sai da máquina da rotina: nem a rotina nem o Claude veem o valor. Disponível nos planos Pro, Max, Team e Enterprise.
5. Pra testar no seu computador, deixe o token numa variável de ambiente, digitando no seu terminal (fora do Claude): `export META_ACCESS_TOKEN=<token>` no `~/.zshrc`.

Limite da Meta: 50 posts por conta a cada 24 horas. A API publica na hora em que a rotina roda, então os 9 saem juntos e o grid aparece montado no perfil.

### Alternativa: Blotato ou Metricool

Pra quem quer os 9 posts espaçados ao longo do dia sem depender da rotina: o agendamento fica do lado deles.

| Publicador | Por que | Custo |
|---|---|---|
| **Blotato** | Posta feed, carrossel, Reels e Stories, aceita arquivo ou URL e agenda do lado dele. Preço fixo, sem limite por volume | A partir de US$ 29 por mês, com até 20 contas. A conexão com o Claude não entra no teste grátis |
| **Metricool** | Connector no diretório do Claude, agenda no melhor horário do público e traz as métricas do perfil | Plano pago pra 9 posts por dia, porque o grátis limita a vinte agendados |

- **Blotato:** conta em https://www.blotato.com com o Instagram conectado; no Claude, Settings → Connectors → Add custom connector → `https://mcp.blotato.com/mcp`; no Claude Code, `claude mcp add --transport http blotato https://mcp.blotato.com/mcp`.
- **Metricool:** no Claude, Settings → Connectors → procure **Metricool** no diretório e faça login.

Sem nenhum caminho ligado, a rotina deixa as 9 imagens e as legendas prontas numa pasta pra agendar em lote no Meta Business Suite.

## 4. Conectar Shopify (3min — plugin oficial AI Toolkit)

O caminho oficial é o **plugin Shopify AI Toolkit pro Claude Code** (não existe pacote npm `@shopify/ai-toolkit` — o toolkit é distribuído como plugin):

```bash
claude plugin install shopify-ai-toolkit@claude-plugins-official
```

Reinicie o Claude Code. O plugin traz busca de docs/schemas, **validação de Liquid/GraphQL contra os schemas oficiais**, e operações de loja via Shopify CLI (`shopify store auth` / `shopify store execute`). Autentique a loja:

```bash
shopify auth login
```

> **⚠️ ALERTA DE TELEMETRIA — leia ANTES de usar o plugin.** A cada invocação, o toolkit envia um evento de uso pra `shopify.dev` contendo: o código validado, o texto da busca E **a sua última mensagem literal (truncada em 2000 chars)**. No contexto Aura isso importa de verdade: a sua mensagem pode conter estratégia de marca, pricing, oferta — conteúdo do workspace que é confidencial por regra inviolável (regra 11 do CLAUDE.md). **Desative a telemetria antes de usar:**
>
> ```bash
> export OPT_OUT_INSTRUMENTATION=true   # adicione ao ~/.zshrc pra valer em toda sessão
> ```
>
> Se preferir não instalar o plugin, tudo continua funcionando: as skills `page-build`/`checkout-aov` usam o Shopify CLI puro (`shopify theme push`, etc.) como caminho default, e a validação de Liquid fica com o check interno do `liquid-converter.py`.

## 4.5. (Opcionais) Shopify Dev MCP + Stripe MCP

Dois MCPs opcionais que enriquecem skills específicas. Sem eles tudo funciona — são puro upside.

**Shopify Dev MCP** (`mcp__shopify_dev__*`) — docs + validação de Liquid/GraphQL. Reduz hallucination na **page-build** (compile HTML→Liquid) ao validar schema/sintaxe contra a fonte oficial antes do push. É um servidor stdio local (não HTTP remoto). Se você já instalou o plugin AI Toolkit (passo 4), a validação já vem junto — este passo é só pra quem quer o Dev MCP sem o plugin:

```bash
claude mcp add shopify_dev -- npx -y @shopify/dev-mcp
```

**Stripe MCP** (`mcp__stripe__*`) — leitura de revenue real (AOV histórico) pra calcular PSM/pricing de verdade em vez de teórico. Útil na **offer-builder** (pricing) e **checkout-aov** (thresholds de free-shipping / bundle):

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
```

Detecção por prefixo conforme `.claude/lib/mcp-detect/README.md`. Se ausentes, as skills usam defaults (validação interna do `liquid-converter.py`; AOV informado manualmente pelo membro).

## 5. Verificar conexões (2min)

Reiniciar Claude Code. Conferir os servers registrados:

```bash
claude mcp list
```

Depois rodar:
```
Claude, lista minhas campanhas ativas no Meta Ads.
```

Aura tenta:
1. Tools `mcp__meta__ads_get_ad_accounts` (oficial) — se sucesso, usa
2. Senão, tools `mcp__meta-ads__*` (Pipeboard) — se sucesso, usa
3. Senão, pergunta ao membro pra colar dados

Output do membro vê apenas a lista de campanhas + label "via Meta MCP oficial" ou "via Pipeboard MCP (oficial indisponível)".

## 6. (Opcional) Playwright headless pra fallback

Pra operações que MCPs não cobrem (criar Shopify Page, upload de creative com arquivo local quando o Pipeboard falha):

```bash
pip3 install playwright
playwright install chromium
```

**Como o login funciona (Shopify E Meta):** o Shopify CLI guarda token de sessão da CLI — isso NÃO são cookies de browser, e o Playwright não consegue reaproveitar. O fluxo real, nas receitas que caem em Playwright:

1. Na primeira run, a Aura abre um browser **visível** (headed) e pede: "loga na sua conta [Shopify Admin | Meta Business] nessa janela".
2. Após o login, a Aura salva o estado da sessão em `~/.config/aura/playwright-state-shopify.json` (ou `playwright-state-meta.json`) — local-only, fora de qualquer git, modo 600.
3. Runs seguintes reutilizam esse `storage_state` sem pedir login de novo. Quando a sessão expirar, repete o passo 1.

Vale pros dois lados: Admin da Shopify (criar Pages — `deploy-shopify-product.md` caminho 2) e Ads Manager da Meta (fallback de upload de criativo — `upload-creative-to-meta.md`).

## Checklist de sucesso

- [ ] Meta MCP oficial conectado (`claude mcp list` mostra `meta`)
- [ ] OAuth Business Suite autorizado
- [ ] Pelo menos 1 ad account aparece em `ads_get_ad_accounts`
- [ ] System User criado, com conta de anúncios, página e pixel atribuídos, e token sem validade gerado (passo 3)
- [ ] Ad Account ID identificado
- [ ] Pipeboard registrado (`claude mcp list` mostra `meta-ads`)
- [ ] Shopify CLI autenticado
- [ ] Plugin Shopify AI Toolkit instalado **com `OPT_OUT_INSTRUMENTATION=true` exportado** (ou decisão consciente de ficar no CLI puro)
- [ ] Claude Code lista campanhas via cascade
- [ ] (Opcional) Klaviyo MCP conectado (`mcp__klaviyo__*`) — automação de retention flows na Skill `retention-engine`
- [ ] (Opcional) Higgsfield MCP conectado (`mcp__higgsfield__*`) — vídeo in-session na Skill `creative-engine` e imagem da página na Skill `page-design`
- [ ] (Opcional) Foreplay MCP conectado (`mcp__foreplay__*`) — ad spy nas Skills `competitor-analysis`/`creative-engine`/`ad-analysis`
- [ ] (Opcional) Postagem no Instagram: produto Instagram no app, `instagram_content_publish` no token e o token como segredo de rede do ambiente da rotina (ou Blotato/Metricool) — Skill `social-engine`
- [ ] (Opcional) Notion MCP conectado (`mcp__claude_ai_Notion__*` ou `mcp__notion__*`) — banco de marcas da Skill `product-research`
- [ ] (Recomendado) TrendTrack MCP conectado (`mcp__trendtrack__*`) — motor de descoberta da Skill `product-research` (gasta créditos do plano; sem ele, a pesquisa roda manual no browser). Quem ainda não assina: https://app.trendtrack.io/invite/tt-d0b18d189489 dá 20% de desconto nos 3 primeiros meses
- [ ] (Opcional) Shopify Dev MCP (`mcp__shopify_dev__*`) + Stripe MCP (`mcp__stripe__*`)
- [ ] (Opcional) `GROQ_API_KEY` exportado — degrau 1 da transcrição de criativos na Skill `competitor-analysis` ETAPA 3C

Pronto. A partir daqui, membro invoca receitas por linguagem natural.

## Troubleshooting

**Oficial retorna 401/403 mas autenticou:**
→ Rollout gradual. Sua conta específica ainda não foi liberada. Aura cai pro Pipeboard automaticamente.

**Oficial mostra "account disabled":**
→ Mesmo motivo. Aguarde liberação ou use Pipeboard temporariamente.

**Pipeboard "Invalid OAuth access token":**
→ Duas causas comuns: (a) token revogado (alguém gerou um novo no System User ou tirou o ativo dele) — gerar de novo e re-registrar (passo 3, E e F); (b) o env foi registrado com `$(cat ...)` em vez do token literal — o valor não é expandido; re-registre colando o token real.

**Pipeboard "Missing permissions":**
→ Permissão ou ativo faltando. Confira se a conta de anúncios, a página e o pixel estão atribuídos ao System User (passo 3, D) e gere o token de novo com as permissões do passo 3, E.

**"MCP server not found" pro oficial:**
→ Confirmar que `mcp.facebook.com/ads` foi adicionado corretamente (`claude mcp list` / Settings→Connectors). Reiniciar Claude.

**"MCP server not found" pro Pipeboard:**
→ Reiniciar Claude Code após o `claude mcp add`. Verificar `which meta-ads-mcp`.

**"Rate limit exceeded" no Pipeboard:**
→ O app está no nível de desenvolvimento da Marketing API, que tem limite baixo. Esperar a janela zerar (a receita espera sozinha em leitura) ou pedir o Ads Management Standard Access na Revisão do app em https://developers.facebook.com/apps/.

**Oficial sem rate limit documentado:**
→ A beta não publicou tetos. A hipótese de trabalho das receitas é herança da Marketing API (~200 calls/hora/ad account) — trate como estimativa, não como fato. Se ver erro 429 explícito, abrir issue em developers.facebook.com.

## Custo

- **Meta MCP oficial:** $0 durante a open beta. Long-term pricing não-anunciado pela Meta até julho/2026.
- **Pipeboard:** $0 — Meta Marketing API é grátis pra uso regular de advertiser.
- **Shopify AI Toolkit:** $0 — grátis e open source (mas leia o alerta de telemetria no passo 4).
- **Higgsfield MCP:** $0 pelo MCP em si — o vídeo e a imagem consomem créditos do plano Higgsfield que você já paga.
- **Foreplay MCP:** $0 pelo MCP — usa o plano + créditos de API da conta Foreplay existente.
- **Groq API (transcrição):** free tier generoso; pago sai ~$0.02-0.04 por hora de áudio transcrita.

## Por que manter os dois Meta MCPs

| Cenário | Oficial responde? | Pipeboard responde? | Aura usa |
|---|---|---|---|
| Conta liberada no rollout | ✅ | ✅ | Oficial (mais features) |
| Conta ainda disabled na beta | ❌ | ✅ | Pipeboard automático |
| Oficial passa por outage | ❌ | ✅ | Pipeboard automático |
| Token do System User revogado | ✅ | ❌ | Oficial sozinho |
| Ambos caem | ❌ | ❌ | Pergunta ao membro |

Resultado: Skill `ad-analysis` nunca trava por causa de MCP. Resiliência sem trabalho extra do membro.
