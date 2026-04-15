---
name: setup
description: Onboarding do novo membro. Roda na primeira vez que o membro abre o Aura Engine. Configura o perfil e verifica dependências.
---

# Setup — Onboarding Inicial

Esta skill roda quando o membro digita "setup" ou quando é a primeira vez usando o Aura Engine.

## Verificação de Dependências

Antes de qualquer coisa, verifique se as seguintes ferramentas estão instaladas no sistema:

1. **Node.js v20+**: rode `node --version`. Se não tiver, instrua: `nvm install 20 && nvm use 20`

Para cada item, mostre:
- ✅ se está instalado (com versão)
- ❌ se não está, com instrução exata de como instalar

NÃO prossiga com o onboarding até que todas as dependências estejam resolvidas.

## Verificação do MCP Aura

Verifique se o MCP da Aura está conectado tentando fazer uma busca: search_knowledge com query "test connection". Se funcionar, mostre ✅. Se não, instrua o membro:

"Rode no terminal: claude mcp add aura --transport http https://aura-mcp-production.up.railway.app/mcp"

## Onboarding do Membro

Depois que tudo estiver funcionando, faça as seguintes perguntas UMA POR VEZ (espere a resposta antes de perguntar a próxima):

### 1. Situação atual

"Qual sua situação agora?"
- A) Não tenho produto — quero encontrar um
- B) Tenho produto mas ainda não lancei
- C) Já estou vendendo mas não escalo
- D) Já escalo e quero otimizar

### 2. Budget

"Qual seu budget diário disponível pra ads? (em dólares)"

### 3. Ferramentas

"Quais dessas ferramentas você tem acesso?"
- SpyBox
- Shopify (loja ativa? se sim, manda o link)
- ElevenLabs
- Meta Ads Manager (conta ativa?)

### 4. Produto (condicional)

SE respondeu B, C ou D na pergunta 1: "Me manda o link da sua loja e do produto principal."
SE respondeu A: pule esta pergunta.

## Salvar Perfil

Salve todas as respostas em `/workspace/profile.md` no formato:

```
Perfil do Membro
Situação: [A / B / C / D — por extenso]
Budget diário: [valor em USD]
Ferramentas:
  - SpyBox: [sim/não]
  - Shopify: [sim + link / não]
  - ElevenLabs: [sim/não]
  - Meta Ads Manager: [sim/não]
Link da loja: [url ou "N/A"]
Link do produto principal: [url ou "N/A"]
Data do setup: [data atual]
```

## Mensagem Final — Roteamento por Situação

Depois de salvar o perfil, mostre a mensagem de roteamento APROPRIADA pra situação respondida:

- **Situação A** (não tem produto): "Setup completo. Diga 'product research' pra encontrar um produto."
- **Situação B** (tem produto, não lançou): "Setup completo. Diga 'market research' pra começar a pesquisa do seu produto."
- **Situação C** (vende, não escala): "Setup completo. Diga 'ad analysis' pra eu diagnosticar seus ads atuais."
- **Situação D** (escala, quer otimizar): "Setup completo. Diga 'scale' pra montar seu plano de escala."

Depois da mensagem de roteamento, sempre adicione:
"Você pode dizer o nome de qualquer fase a qualquer momento. Eu vou te guiar."
