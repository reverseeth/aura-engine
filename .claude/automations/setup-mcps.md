# Setup MCPs — guia 15min

Setup único. Depois disso, Claude Code executa operações em Meta Ads + Shopify via linguagem natural.

## Stack atual (recomendada — maio/2026)

Aura usa **cascade resiliente** com 2 MCPs Meta em paralelo. Você instala os dois; Aura tenta o oficial primeiro e cai pro 3rd party automaticamente se o oficial não estiver disponível pra seu ad account (rollout gradual).

| MCP | Propósito | Status |
|---|---|---|
| **Meta MCP oficial** (`mcp.facebook.com/ads`) | Caminho preferencial — 29 tools, OAuth Business Suite, industry benchmarks, dataset quality | Open beta desde 2026-04-29, rollout gradual |
| **Pipeboard MCP** (`pipeboard-co/meta-ads-mcp`) | Fallback automático quando o oficial não responde ou está disabled | 3rd party, GA |
| **Shopify AI Toolkit** | Operações Shopify (produto, theme, page) | Oficial, GA |

## 1. Instalar dependências (2min)

```bash
# Python (pro Pipeboard fallback + Playwright)
pip3 install modelcontextprotocol meta-ads-mcp playwright

# Node.js (pro Shopify AI Toolkit)
npm install -g @shopify/cli @shopify/ai-toolkit
```

O MCP oficial **não precisa de instalação local** — é remote, conecta via URL.

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
   curl "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
   ```

Salva o token em `~/.config/aura/meta-token` (modo 600).

### Pegar Ad Account ID
```bash
curl "https://graph.facebook.com/v19.0/me/adaccounts?access_token=TEU_TOKEN"
# resposta: "act_123456789" — esse é o ad_account_id
```

### Registrar como `meta-ads`

Edit `~/.claude/mcp.json` (cria se não existe):

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "meta-ads-mcp",
      "args": [],
      "env": {
        "META_ACCESS_TOKEN": "$(cat ~/.config/aura/meta-token)",
        "META_DEFAULT_AD_ACCOUNT": "act_123456789"
      }
    }
  }
}
```

> **Importante — naming:** o connector oficial usa `meta` (vira tools `mcp__meta__*`). O Pipeboard usa `meta-ads` (vira tools `mcp__meta-ads__*`). Não troque os nomes — as receitas detectam por prefixo.

## 4. Conectar Shopify (3min)

Você provavelmente já tem Shopify CLI autenticado. Verificar:
```bash
shopify app dev --help
```

Se não, `shopify auth login`. Depois adicionar ao `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "meta": { /* já configurado acima */ },
    "meta-ads": { /* já configurado acima */ },
    "shopify": {
      "command": "npx",
      "args": ["-y", "@shopify/ai-toolkit", "serve"],
      "env": {
        "SHOPIFY_STORE": "<sua-loja>.myshopify.com"
      }
    }
  }
}
```

## 5. Verificar conexões (2min)

Reiniciar Claude Code. Rodar:
```
Claude, lista minhas campanhas ativas no Meta Ads.
```

Aura tenta:
1. Tools `mcp__meta__ads_get_ad_accounts` (oficial) — se sucesso, usa
2. Senão, tools `mcp__meta-ads__*` (Pipeboard) — se sucesso, usa
3. Senão, pergunta ao membro pra colar dados

Output do membro vê apenas a lista de campanhas + label "via Meta MCP oficial" ou "via Pipeboard MCP (oficial indisponível)".

## 6. (Opcional) Playwright headless pra fallback

Pra operações que MCPs não cobrem (criar Shopify Page, upload de creative com arquivo local):

```bash
pip install playwright
playwright install chromium
```

Receitas que usam Playwright vão usar os cookies do teu login Shopify (guardados em `~/.config/shopify-cli`).

## Checklist de sucesso

- [ ] Meta MCP oficial conectado (Settings → Connectors → `meta`)
- [ ] OAuth Business Suite autorizado
- [ ] Pelo menos 1 ad account aparece em `ads_get_ad_accounts`
- [ ] Pipeboard token gerado e válido (fallback)
- [ ] Ad Account ID identificado
- [ ] Shopify CLI autenticado
- [ ] MCPs registrados em `~/.claude/mcp.json` (`meta`, `meta-ads`, `shopify`)
- [ ] Claude Code lista campanhas via cascade

Pronto. A partir daqui, membro invoca receitas por linguagem natural.

## Troubleshooting

**Oficial retorna 401/403 mas autenticou:**
→ Rollout gradual. Sua conta específica ainda não foi liberada. Aura cai pro Pipeboard automaticamente.

**Oficial mostra "account disabled":**
→ Mesmo motivo. Aguarde liberação ou use Pipeboard temporariamente.

**Pipeboard "Invalid OAuth access token":**
→ Token expirou (long-lived dura 60 dias). Regenerar token (passo 3).

**Pipeboard "Missing permissions":**
→ Scopes insuficientes. Refazer token com os 4 scopes listados.

**"MCP server not found" pro oficial:**
→ Confirmar que `mcp.facebook.com/ads` foi adicionado corretamente nas Settings/Connectors. Reiniciar Claude.

**"MCP server not found" pro Pipeboard:**
→ Reiniciar Claude Code após editar mcp.json. Verificar `which meta-ads-mcp`.

**"Rate limit exceeded" no Pipeboard:**
→ Meta Marketing API tem limit 200 calls/hora/user + 100k/48h em dev. Esperar ou pedir aumento em https://developers.facebook.com/apps/.

**Oficial sem rate limit documentado:**
→ Beta não publicou tetos. Se ver erro 429 explícito, abrir issue em developers.facebook.com.

## Custo

- **Meta MCP oficial:** $0 durante a open beta. Long-term pricing não-anunciado pela Meta até maio/2026.
- **Pipeboard:** $0 — Meta Marketing API é grátis pra uso regular de advertiser.
- **Shopify AI Toolkit:** $0 — grátis e open source.

## Por que manter os dois Meta MCPs

| Cenário | Oficial responde? | Pipeboard responde? | Aura usa |
|---|---|---|---|
| Conta liberada no rollout | ✅ | ✅ | Oficial (mais features) |
| Conta ainda disabled na beta | ❌ | ✅ | Pipeboard automático |
| Oficial passa por outage | ❌ | ✅ | Pipeboard automático |
| Token Pipeboard expirou | ✅ | ❌ | Oficial sozinho |
| Ambos caem | ❌ | ❌ | Pergunta ao membro |

Resultado: Skill 11 nunca trava por causa de MCP. Resiliência sem trabalho extra do membro.
