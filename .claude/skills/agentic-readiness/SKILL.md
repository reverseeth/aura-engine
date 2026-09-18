---
name: agentic-readiness
description: Checklist de AEO (Answer Engine Optimization, a otimização pra ser encontrado e citado por agentes de compra com AI) e de prontidão agentic da loja. Garante que a PDP e a loja sejam descobríveis dentro de ChatGPT, Perplexity, Google AI Mode e Copilot, com o canal Agentic Storefronts habilitado no Shopify admin, o Knowledge Base app populado, dados estruturados completos na PDP (GTIN, ratings, FAQ, shipping e return), bloco de specs legível por agente, robots.txt liberando os robôs de AI, override opcional do llms.txt, registro no Perplexity Merchant Program e qualidade do feed do Google Merchant Center. Roda depois do deploy da página (page-build) e antes do consistency audit e do launch. Use quando o membro disser "agentic readiness", "aeo", "ai visibility", "otimizar pra ChatGPT/Perplexity", ou depois que a página estiver no ar.
---

# Agentic Readiness · Passo 14 · apelido antigo: 07e <!-- gen:title -->

## Quando usar

Depois que a loja está montada (cadeia `page-design` a `checkout-aov`) e, idealmente, com os criativos já prontos, antes do consistency audit e do launch. A página precisa estar no ar: esta skill audita o que o robô de AI encontra de verdade, não o que está planejado. Comprador que chega via assistente de AI converte mais que o tráfego orgânico comum, e o Shopify já liga a infraestrutura por default (Agentic Storefronts, `/llms.txt`, `/api/mcp`), então o robô vai passar na página de qualquer jeito; a pergunta é se ele acha o que precisa pra citar a loja. A copy Hopkins otimiza pra humano; agentes leem Schema.org, GTIN, políticas e specs verificáveis, e esta skill entrega essa segunda camada. Checklist barato, de execução única, que vale pra todo stage, inclusive starter; a adaptação por stage é só de expectativa (`reference/contexto.md`).

Esta skill não consulta a base de conhecimento (não existe domínio de AEO lá); não invente query. Fontes: docs oficiais (Shopify Agentic Storefronts, Perplexity Merchant Program, Google Merchant Center), verificação direta na loja viva por `curl` ou `WebFetch` e os artefatos das fases anteriores. Doc da web pela rule `resilient-fetch.md`.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe e parseia (senão, escape ES2).
2. `report_language` do profile (default `pt-BR`) em todo output interno e na conversa; conteúdo que vai pra loja (specs, FAQ, llms.txt) é sempre em inglês US.
3. `page-build` em `manifest.skills_completed` e `manifest.storefront.page_url` presente. Página fora do ar: escape ES1, (A) rodar `page-build` primeiro, recomendado, ou (B) gerar só o blueprint do checklist marcando `manifest.skipped_preflight += ["page-build"]` e deixando os itens de verificação live como `pending`. Nunca abortar seco.
4. Acesso ao Shopify admin da loja (canal de vendas, apps, robots.txt do tema).

## Contexto a carregar

1. `manifest.json` (`storefront.page_url`, `store_url`, `stage`, `product_vertical`).
2. `offer-builder/dados.json` (garantia, envio, pricing, bundle; GTIN se o membro informou).
3. `copy-engine/dados.json` (FAQ real da página).
4. `page/deploy-report.json` e `page/staging/geo/` (`product-schema.json`, `agent-facts.html`), a camada GEO que a `page-build` (ETAPA 4.5) já gerou; esta skill verifica e completa essa camada, não a recria.

## Fluxo da skill

### ETAPA 1 · Canal Agentic Storefronts + policies

Leia `reference/canal-e-knowledge-base.md`. O canal torna a loja descobrível dentro dos assistentes via Universal Commerce Protocol; vem auto-ativado pra merchants US elegíveis, e elegível exige policies completas. Guiar o membro no admin: confirmar o canal em Settings > Apps and sales channels; completar as 3 policies obrigatórias (shipping, return/refund, contact) com os mesmos prazos e condições da página e da oferta; registrar `enabled` / `pending_policies` / `not_eligible`. Confirmar o endpoint `/api/mcp` com `curl -sI` (qualquer status diferente de 404 conta como presente).

### ETAPA 2 · Knowledge Base app da Shopify

Mesmo arquivo. Instalar o app grátis e popular com dado real das fases anteriores (FAQ da `copy-engine`, políticas da ETAPA 1, garantia da `offer-builder`, 2 a 3 parágrafos de brand voice do `brand.md`), em inglês US, factual e específico. Status `populated` / `installed_empty` / `pending`.

### ETAPA 3 · Dados estruturados da PDP (auditoria do JSON-LD)

Leia `reference/dados-estruturados-e-specs.md`. `curl -s <page_url>`, extrair os blocos `application/ld+json` e validar o que o agente de compra consome: GTIN/EAN no nó Product (sem GTIN, documentar o gap e usar `mpn` ou `sku`, nunca inventar código), `aggregateRating` só com reviews reais (sem reviews, omitir o nó), FAQPage cobrindo as perguntas reais, `shippingDetails` e `MerchantReturnPolicy` batendo com a config real. Nó faltando ou divergente: a correção acontece na `page-build`, com a lista exata de gaps; esta skill não injeta Liquid por fora do pipeline. Status por item mais `gaps[]`.

### ETAPA 4 · Bloco de specs legível por agente

Mesmo arquivo. Conferir que o bloco agent-facts (`data-aura-section="product-facts"`) está no ar e cobre specs concretas: materiais ou ingredientes com quantidade, dimensões e quantidade por embalagem, certificações verificáveis, envio, devolução e garantia. Spec verificável vence copy sensorial nesta camada; o bloco nunca contradiz o JSON-LD nem a config real. Spec que falta e o membro tem vai pra `page-build` adicionar. Ícones SVG, nunca emoji; fatos diretos, sem aviso nem suavização.

### ETAPA 5 · robots.txt liberando os robôs de AI

Leia `reference/robots-e-llms.md`. `curl -s https://<store>/robots.txt` e confirmar que nenhum destes está bloqueado: `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`. Bloqueio vem de customização antiga em `templates/robots.txt.liquid`: pull antes de editar (`shopify-theme-safety.md`), remover só as regras desses 5 agents, push seguro e re-verificar com curl. Status `all_allowed` / `fixed` / `blocked_pending`.

### ETAPA 6 · llms.txt (override opcional)

Mesmo arquivo. Verificar que o `/llms.txt` nativo existe. O override por `templates/llms.txt.liquid` é opcional (1 parágrafo de marca, produto hero com o mecanismo nomeado da `offer-builder`, links pras políticas, fatos específicos, em inglês US); sem customização, registrar `native` e seguir.

### ETAPA 7 · Perplexity Merchant Program

Leia `reference/perplexity-e-merchant-center.md`. Registro grátis, sem taxa nem mínimo de receita, que exige a conta do merchant: passar o passo a passo ao membro e marcar `registered` / `pending` (pendente não bloqueia o launch).

### ETAPA 8 · Qualidade do feed do Google Merchant Center

Mesmo arquivo. Com o Merchant Center conectado, auditar o produto hero: título com 30 caracteres ou mais e descritivo pra query de agente, descrição com 500 caracteres ou mais, 3 imagens ou mais, GTIN preenchido (ou `identifier_exists: false` declarado), preço e disponibilidade iguais aos da PDP. Sem Merchant Center, recomendar a conexão e marcar `pending`.

### ETAPA 9 · Score de AI visibility + wrap-up

Leia `reference/score.md`. Score = itens `pass` sobre itens aplicáveis (`na` sai do denominador): 80% ou mais, pronta pra descoberta por agente; 50 a 79%, funcional com lacunas, com as 2 a 3 ações de maior impacto listadas; abaixo de 50%, invisível, com as ETAPAs 1, 3 e 5 resolvidas antes do launch. O score não bloqueia o launch (quem gateia é a `consistency-audit`), mas dado estruturado divergente da página (ETAPA 3) se resolve antes.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/agentic-readiness/`; `agentic-readiness.md` no `report_language` (score e leitura executiva, tabela do checklist, gaps de dados estruturados pra iteração da `page-build`, pendências do membro, o que esperar do canal), `agentic-readiness.html` por `python3 tools/render_report.py workspace/[produto]/agentic-readiness/agentic-readiness.md` com as convenções de `.claude/templates/aura-html-components.md`, e `dados.json` no schema do arquivo (checklist por item com status, `ai_visibility_score`, `pending_actions`). Manifest pelo script: `python3 tools/manifest.py <slug> complete agentic-readiness`, `set agentic` com `ready`, `channel_enabled`, `score` e `checked_at` (a `consistency-audit` lê como contexto e a `scale-engine` pra tratar o tráfego de referral de AI como fonte incremental), e `python3 .claude/lib/workspace-index/build_index.py <slug>`. O self-audit silencioso da skill (status `pass` só quando verificado na loja viva, nada inventado, score conferido, conteúdo público em inglês US sem suavização, outputs salvos) está no mesmo arquivo.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft: o score, o que já está de pé, o que depende do membro, o que volta pra `page-build`, a expectativa honesta do canal e o próximo passo, 'consistency audit'.
