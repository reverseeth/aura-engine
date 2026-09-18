# Copy Engine · Referência: As duas únicas perguntas ao membro (ETAPA 1)

> A pergunta do tipo de página com a decisão pelo awareness quando o membro não sabe, a pergunta da página atual com a cascade de leitura (WebFetch, fetcher resiliente, paste) e a regra de nenhuma outra pergunta. Abra na ETAPA 1.

### ETAPA 1 — Perguntas ao Membro (APENAS 2)

Faça APENAS estas duas perguntas:

**1. Tipo de página:**
"Que tipo de página vamos escrever?
- PDP (Shopify)
- Landing Page dedicada
- Advertorial
- Não sei (o sistema recomenda baseado no awareness level)"

Se o membro disser "não sei", use o awareness level dominante do market research pra decidir:
- **Unaware / Problem Aware** → Advertorial (educação antes do pitch)
- **Solution Aware** → Landing Page dedicada
- **Product Aware / Most Aware** → PDP

**2. Página atual:**
"Tem página atual que quer melhorar? Se sim, me manda o link."

- SE mandar o link: leia/extraia a página (`WebFetch`; se barrado — 403/Cloudflare/password page da loja —, use o fetcher resiliente: `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text`, conforme `resilient-fetch.md`; último caso, o membro cola o texto da página) e use como baseline — identifique o que manter (o que funciona) e o que reescrever (o que tá fraco).
- SE não tiver: partimos do zero.

**NENHUMA outra pergunta ao membro.** Todas as decisões estratégicas abaixo são tomadas automaticamente pelo sistema.
