# Setup MCPs — guia 15min

Setup único. Depois disso, Claude Code executa operações em Meta Ads + Shopify
via linguagem natural.

## 1. Instalar dependências (2min)

```bash
# Python (pro Meta MCP)
pip3 install modelcontextprotocol meta-ads-mcp playwright

# Node.js (pro Shopify AI Toolkit)
npm install -g @shopify/cli @shopify/ai-toolkit
```

## 2. Credenciais — Meta Marketing API (5min)

### Gerar token
1. Ir em https://developers.facebook.com/apps → Create App (tipo "Business")
2. Adicionar produto "Marketing API"
3. Settings → Basic → copiar App ID + App Secret
4. Tools → Graph API Explorer → generate token com scopes:
   - `ads_management`
   - `ads_read`
   - `business_management`
   - `pages_read_engagement`
5. Exchange pra long-lived token:
   ```bash
   curl "https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=SHORT_LIVED_TOKEN"
   ```

Salva o token em `~/.config/aura/meta-token` (modo 600).

### Pegar Ad Account ID
```bash
curl "https://graph.facebook.com/v19.0/me/adaccounts?access_token=TEU_TOKEN"
# resposta: "act_123456789" — esse é o ad_account_id
```

## 3. Credenciais — Shopify (3min)

Tu já tem Shopify CLI autenticado (vi no profile.md). Verificar:
```bash
shopify app dev --help
```

Se não tiver, `shopify auth login`.

## 4. Registrar MCPs no Claude Code (3min)

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
    },
    "shopify": {
      "command": "npx",
      "args": ["-y", "@shopify/ai-toolkit", "serve"],
      "env": {
        "SHOPIFY_STORE": "<store>.myshopify.com"
      }
    }
  }
}
```

## 5. Verificar conexão (2min)

Reiniciar Claude Code. Rodar:
```
Claude, lista minhas campanhas ativas no Meta Ads.
```

Se retornar lista, MCPs estão conectados. Se erro, checar:
- Token válido (pode ter expirado — long-lived dura 60 dias)
- Ad account ID correto
- Scopes suficientes

## 6. (Opcional) Playwright headless pra fallback (2min)

Pra operações que MCPs não cobrem (criar Shopify Page, por exemplo):

```bash
pip install playwright
playwright install chromium
```

Receitas que usam Playwright vão usar os cookies do teu login Shopify
(guardados em `~/.config/shopify-cli`).

## Checklist de sucesso

- [ ] Meta token gerado e válido
- [ ] Ad Account ID identificado
- [ ] Shopify CLI autenticado
- [ ] MCPs registrados em `~/.claude/mcp.json`
- [ ] Claude Code lista campanhas via `meta_ads.*`
- [ ] Claude Code lista produtos via `shopify.*`

Pronto. A partir daqui, membro invoca receitas por linguagem natural.

## Troubleshooting

**"Invalid OAuth access token"**
→ Token expirou. Regenerar long-lived token (step 2).

**"Missing permissions"**
→ Scopes insuficientes. Refazer token com todos os scopes listados.

**"MCP server not found"**
→ Reiniciar Claude Code após editar mcp.json. Verificar path do binary.

**"Rate limit exceeded"**
→ Meta Marketing API tem limit 200 calls/hora/user + 100k/48h em dev. Esperar
ou pedir aumento em https://developers.facebook.com/apps/.

## Custo

$0/mês. Meta Marketing API é grátis pra uso regular de advertiser.
Shopify AI Toolkit é grátis e open source.
