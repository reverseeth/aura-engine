# Setup MCPs — guia 15min

Setup único. Depois disso, Claude Code executa operações em Meta Ads + Shopify via linguagem natural.

## Stack atual (recomendada — julho/2026)

Aura usa **cascade resiliente** com 2 MCPs Meta em paralelo. Você instala os dois; Aura tenta o oficial primeiro e cai pro 3rd party automaticamente se o oficial não estiver disponível pra seu ad account (rollout gradual).

| MCP | Propósito | Status |
|---|---|---|
| **Meta MCP oficial** (`mcp.facebook.com/ads`) | Caminho preferencial — 29 tools, OAuth Business Suite, industry benchmarks, dataset quality | Open beta desde 2026-04-29, rollout gradual, ainda sem GA |
| **Pipeboard MCP** (`pipeboard-co/meta-ads-mcp`) | Fallback automático quando o oficial não responde ou está disabled | 3rd party, GA |
| **Shopify AI Toolkit** (plugin Claude Code) | Operações Shopify (produto, theme, store execute) + validação Liquid/GraphQL | Oficial, abril/2026 — **ver alerta de telemetria no passo 4** |

Opcionais que enriquecem skills específicas: `GROQ_API_KEY` (1.5 — transcrição de criativos na Skill 03), Refero (3.5), Klaviyo (3.6), **Higgsfield** (3.7 — render de vídeo in-session na Skill 08), **Foreplay** (3.8 — ad spy nas Skills 03/08/11), Shopify Dev + Stripe (4.5).

## 1. Instalar dependências (2min)

```bash
# Python (pro Pipeboard fallback + Playwright)
pip3 install meta-ads-mcp playwright
```

> O SDK do Model Context Protocol NÃO precisa ser instalado à parte — `meta-ads-mcp` já declara as próprias dependências.

O MCP oficial **não precisa de instalação local** — é remote, conecta via URL.

## 1.5. (Opcional) GROQ_API_KEY — transcrição de criativos (Skill 03 ETAPA 3C)

Não é MCP, mas mora aqui porque é setup de integração: a análise profunda de criativos escalados dos concorrentes (Skill 03 ETAPA 3C) transcreve os vídeos com um cascade de 3 degraus — **Groq API (`whisper-large-v3-turbo`) → Whisper local → transcript colado pelo membro**. O degrau 1 é o preferencial: rápido, ~$0.02-0.04 por hora de áudio, zero instalação.

```bash
# 1. Criar key grátis em https://console.groq.com/keys
# 2. Exportar no shell (adicionar ao ~/.zshrc ou ~/.bashrc pra persistir):
export GROQ_API_KEY=gsk_...
# 3. Testar:
test -n "$GROQ_API_KEY" && echo "ok"
```

Sem a key, nada trava — a Skill 03 cai pro Whisper local (se instalado) ou pede o transcript ao membro. Detalhes do cascade completo na própria Skill 03 (ETAPA 3C).

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

## 3. Conectar Pipeboard MCP (5min — fallback)

Mesmo que o oficial funcione hoje, instale o Pipeboard. Quando alguma conta do membro estiver "disabled" no rollout da Meta, Aura cai aqui sem interrupção.

### Gerar token Meta Marketing API
1. https://developers.facebook.com/apps → Create App (tipo "Business")
2. Adicionar produto "Marketing API"
3. Settings → Basic → copiar App ID + App Secret
4. Tools → Graph API Explorer → generate token com scopes:
   - `ads_management`
   - `ads_read`
   - `business_management`
   - `pages_read_engagement`
5. Exchange pra long-lived token (dura 60 dias — anote pra renovar):
   ```bash
   curl "https://graph.facebook.com/v23.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
   ```
   > A Meta aposenta versões da Graph API a cada ~2 anos. Se o curl retornar erro de versão, troque `v23.0` pela versão corrente listada em https://developers.facebook.com/docs/graph-api/changelog.

Guarde uma cópia do token em `~/.config/aura/meta-token` (modo 600) — é só backup seu pra renovação; o registro do MCP abaixo usa o valor literal.

### Pegar Ad Account ID
```bash
curl "https://graph.facebook.com/v23.0/me/adaccounts?access_token=TEU_TOKEN"
# resposta: "act_123456789" — esse é o ad_account_id
```

### Registrar como `meta-ads`

Registre via `claude mcp add`, colando o token e o ad account reais no comando (NÃO use `$(cat ...)` — valores de env de MCP são passados literalmente ao processo, sem shell pra expandir; o servidor receberia a string `$(cat ...)` como token e toda chamada falharia com "Invalid OAuth access token"):

```bash
claude mcp add meta-ads \
  --env META_ACCESS_TOKEN=<COLA_O_TOKEN_AQUI> \
  --env META_DEFAULT_AD_ACCOUNT=act_123456789 \
  -- meta-ads-mcp
```

Reinicie o Claude Code. **Renovação (a cada 60 dias):** gere o token novo (passo acima) e re-registre:

```bash
claude mcp remove meta-ads
claude mcp add meta-ads --env META_ACCESS_TOKEN=<TOKEN_NOVO> --env META_DEFAULT_AD_ACCOUNT=act_123456789 -- meta-ads-mcp
```

> **Importante — naming:** o connector oficial usa `meta` (vira tools `mcp__meta__*`). O Pipeboard usa `meta-ads` (vira tools `mcp__meta-ads__*`). Não troque os nomes — as receitas detectam por prefixo.

## 3.5. Conectar Refero MCP (opcional, 2min — design system curado)

Se o membro quer alimentar a skill 07a Brand Discovery com design systems curados de top sites (~200 sites premium tipo Cursor, Linear, Vercel), conecte o Refero MCP. Sem ele, Aura cai pro `tools/design-clone/` (Playwright) ou pergunta manual.

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

Se o membro usa Klaviyo e quer que a **Skill 13 (retention-engine)** crie os flows direto (welcome / abandoned-cart / post-purchase / win-back / replenishment) com contrato estável — em vez de só gerar HTML + setup-guide pra importar à mão — conecte o **MCP oficial da Klaviyo**.

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

Se retornar lista → conectado (tools `mcp__klaviyo__*` disponíveis). Sem ele, a Skill 13 cai pro caminho de **assets + setup-guide** (HTML pronto + guia manual), que continua sendo o fallback confiável. Os flows criados via MCP ficam SEMPRE em draft — o membro revisa e ativa no Klaviyo UI (a skill nunca ativa sozinha, pra não arriscar spam).

## 3.7. Conectar Higgsfield MCP (opcional, 2min — render de vídeo in-session)

Fecha o único passo manual do pipeline de criativos: sem ele, a **Skill 08** entrega prompts prontos pra você colar no Higgsfield; com ele, a skill gera o prompt E **renderiza o vídeo na própria sessão**, salvando o `.mp4` em `workspace/[produto]/08-creative-engine/renders/`.

É o MCP oficial hospedado da Higgsfield (lançado 2026-04-30): OAuth via browser, sem API key, usa os créditos do plano que você já tem. Expõe 30+ modelos (Kling 3.x, Veo 3.1, Sora 2, Seedance, MiniMax Hailuo), output sem watermark em plano pago.

### Claude Desktop
Settings → Connectors → "+ Add custom connector" → nome `higgsfield`, URL `https://mcp.higgsfield.ai/mcp` → OAuth quando pedir.

### Claude Code
```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
```

Reinicie. Tools com prefixo `mcp__higgsfield__` aparecem — a Skill 08 (ETAPA 0.7) detecta sozinha e **pergunta antes de gastar créditos** ("quer que eu renderize os N vídeos ou prefere só os prompts?"). Sem o MCP, nada muda: a skill entrega os prompts como sempre.

## 3.8. Conectar Foreplay MCP (opcional, 2min — ad spy)

Fonte de criativos escalados dos concorrentes (200M+ ads em Facebook/Instagram/TikTok/YouTube/LinkedIn, busca por marca e domain intelligence). Com ele conectado, a **Skill 03** puxa os criativos escalados sem pedir screenshots/uploads, e as **Skills 08/11** ganham sinal de hooks/formatos ativos no nicho. Requer conta Foreplay (usa o plano + créditos de API que você já tem).

### Claude Desktop
Settings → Connectors → "+ Add custom connector" → nome `foreplay`, URL `https://public.api.foreplay.co/mcp` → sign-in com a conta Foreplay.

### Claude Code
```bash
claude mcp add --transport http foreplay https://public.api.foreplay.co/mcp
```

Reinicie. Tools com prefixo `mcp__foreplay__` aparecem; as skills detectam sozinhas. Sem ele, as skills seguem o método tradicional (TrendTrack MCP se houver, Meta Ad Library público, uploads do membro) — silent fallback, nada trava.

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
> Se preferir não instalar o plugin, tudo continua funcionando: as skills 07b/07d usam o Shopify CLI puro (`shopify theme push`, etc.) como caminho default, e a validação de Liquid fica com o check interno do `liquid-converter.py`.

## 4.5. (Opcionais) Shopify Dev MCP + Stripe MCP

Dois MCPs opcionais que enriquecem skills específicas. Sem eles tudo funciona — são puro upside.

**Shopify Dev MCP** (`mcp__shopify_dev__*`) — docs + validação de Liquid/GraphQL. Reduz hallucination na **07b-page-build** (compile HTML→Liquid) ao validar schema/sintaxe contra a fonte oficial antes do push. É um servidor stdio local (não HTTP remoto). Se você já instalou o plugin AI Toolkit (passo 4), a validação já vem junto — este passo é só pra quem quer o Dev MCP sem o plugin:

```bash
claude mcp add shopify_dev -- npx -y @shopify/dev-mcp
```

**Stripe MCP** (`mcp__stripe__*`) — leitura de revenue real (AOV histórico) pra calcular PSM/pricing de verdade em vez de teórico. Útil na **04-offer** (pricing) e **07d-checkout-aov** (thresholds de free-shipping / bundle):

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
- [ ] Pipeboard token gerado e válido (fallback)
- [ ] Ad Account ID identificado
- [ ] Pipeboard registrado (`claude mcp list` mostra `meta-ads`)
- [ ] Shopify CLI autenticado
- [ ] Plugin Shopify AI Toolkit instalado **com `OPT_OUT_INSTRUMENTATION=true` exportado** (ou decisão consciente de ficar no CLI puro)
- [ ] Claude Code lista campanhas via cascade
- [ ] (Opcional) Klaviyo MCP conectado (`mcp__klaviyo__*`) — automação de retention flows na Skill 13
- [ ] (Opcional) Higgsfield MCP conectado (`mcp__higgsfield__*`) — render de vídeo in-session na Skill 08
- [ ] (Opcional) Foreplay MCP conectado (`mcp__foreplay__*`) — ad spy nas Skills 03/08/11
- [ ] (Opcional) Shopify Dev MCP (`mcp__shopify_dev__*`) + Stripe MCP (`mcp__stripe__*`)
- [ ] (Opcional) `GROQ_API_KEY` exportado — degrau 1 da transcrição de criativos na Skill 03 ETAPA 3C

Pronto. A partir daqui, membro invoca receitas por linguagem natural.

## Troubleshooting

**Oficial retorna 401/403 mas autenticou:**
→ Rollout gradual. Sua conta específica ainda não foi liberada. Aura cai pro Pipeboard automaticamente.

**Oficial mostra "account disabled":**
→ Mesmo motivo. Aguarde liberação ou use Pipeboard temporariamente.

**Pipeboard "Invalid OAuth access token":**
→ Duas causas comuns: (a) token expirou (long-lived dura 60 dias) — regenerar e re-registrar (passo 3); (b) o env foi registrado com `$(cat ...)` em vez do token literal — o valor não é expandido; re-registre colando o token real.

**Pipeboard "Missing permissions":**
→ Scopes insuficientes. Refazer token com os 4 scopes listados.

**"MCP server not found" pro oficial:**
→ Confirmar que `mcp.facebook.com/ads` foi adicionado corretamente (`claude mcp list` / Settings→Connectors). Reiniciar Claude.

**"MCP server not found" pro Pipeboard:**
→ Reiniciar Claude Code após o `claude mcp add`. Verificar `which meta-ads-mcp`.

**"Rate limit exceeded" no Pipeboard:**
→ Meta Marketing API tem limit 200 calls/hora/user + 100k/48h em dev. Esperar ou pedir aumento em https://developers.facebook.com/apps/.

**Oficial sem rate limit documentado:**
→ A beta não publicou tetos. A hipótese de trabalho das receitas é herança da Marketing API (~200 calls/hora/ad account) — trate como estimativa, não como fato. Se ver erro 429 explícito, abrir issue em developers.facebook.com.

## Custo

- **Meta MCP oficial:** $0 durante a open beta. Long-term pricing não-anunciado pela Meta até julho/2026.
- **Pipeboard:** $0 — Meta Marketing API é grátis pra uso regular de advertiser.
- **Shopify AI Toolkit:** $0 — grátis e open source (mas leia o alerta de telemetria no passo 4).
- **Higgsfield MCP:** $0 pelo MCP em si — o render consome créditos do plano Higgsfield que você já paga.
- **Foreplay MCP:** $0 pelo MCP — usa o plano + créditos de API da conta Foreplay existente.
- **Groq API (transcrição):** free tier generoso; pago sai ~$0.02-0.04 por hora de áudio transcrita.

## Por que manter os dois Meta MCPs

| Cenário | Oficial responde? | Pipeboard responde? | Aura usa |
|---|---|---|---|
| Conta liberada no rollout | ✅ | ✅ | Oficial (mais features) |
| Conta ainda disabled na beta | ❌ | ✅ | Pipeboard automático |
| Oficial passa por outage | ❌ | ✅ | Pipeboard automático |
| Token Pipeboard expirou | ✅ | ❌ | Oficial sozinho |
| Ambos caem | ❌ | ❌ | Pergunta ao membro |

Resultado: Skill 11 nunca trava por causa de MCP. Resiliência sem trabalho extra do membro.
