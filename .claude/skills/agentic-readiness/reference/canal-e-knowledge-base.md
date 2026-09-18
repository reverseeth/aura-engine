# Agentic Readiness · Referência: Canal Agentic Storefronts, policies e Knowledge Base app (ETAPAs 1 e 2)

> O passo a passo no admin pro canal e as 3 policies obrigatórias, a checagem do endpoint `/api/mcp`, e a instalação e o preenchimento do Knowledge Base app com dado real das fases anteriores. Abra na ETAPA 1.

### ETAPA 1 — Canal Agentic Storefronts + policies

O canal é o que torna a loja descobrível dentro dos assistentes (ChatGPT, Copilot, Gemini) via Universal Commerce Protocol. Desde mar/2026 vem auto-ativado pra merchants US elegíveis — mas "elegível" exige policies completas.

Guiar o membro no admin:
1. **Shopify admin > Settings > Apps and sales channels** → confirmar o canal **Agentic Storefronts** (ou "Agentic") instalado/ativo. Se a loja é US e ele não aparece, checar elegibilidade nos requisitos do canal (plano, região, policies).
2. **Completar as 3 policies obrigatórias** que o canal exige — o próprio admin marca o que falta (tipicamente: shipping policy, return/refund policy e contact/customer service). Sem elas o canal não expõe a loja. Escreva as policies com os mesmos prazos e condições que a página e a oferta (`offer-builder`) usam.
3. Registrar o status: `enabled` / `pending_policies` / `not_eligible`.

> A loja também expõe nativamente o endpoint `/api/mcp` (Storefront MCP) — não precisa configurar nada, mas confirme com `curl -sI https://<store>/api/mcp` que responde (qualquer status ≠ 404 conta como presente).

### ETAPA 2 — Knowledge Base app da Shopify

O Knowledge Base app é a camada de contexto que os agentes consultam pra responder perguntas sobre a loja (políticas, FAQs, voz de marca). Instalar e popular:

1. Instalar o app **Knowledge Base** da Shopify (App Store, grátis).
2. Popular com dado REAL das fases anteriores — nunca inventar: FAQ da PDP (de `copy-engine/dados.json`), políticas de envio/devolução (as mesmas da ETAPA 1), garantia (da `offer-builder`), e 2-3 parágrafos de brand voice (de `brand.md`, se existir).
3. Conteúdo em inglês US, factual e específico.

Status: `populated` / `installed_empty` / `pending`.
