---
name: agentic-readiness
description: Checklist de AEO (Answer Engine Optimization — otimização pra ser encontrado e citado por agentes de compra com AI) e de prontidão agentic da loja. Garante que a PDP e a loja sejam descobríveis dentro de ChatGPT, Perplexity, Google AI Mode e Copilot — canal Agentic Storefronts habilitado no Shopify admin, Knowledge Base app populado, dados estruturados completos na PDP (GTIN, ratings, FAQ/shipping/return), bloco de specs legível por agente, robots.txt liberando os robôs de AI, override opcional do llms.txt, registro no Perplexity Merchant Program e qualidade do feed do Google Merchant Center. Roda DEPOIS do deploy da página (07b) e ANTES do consistency audit (09)/launch. Use quando o membro disser "agentic readiness", "aeo", "ai visibility", "otimizar pra ChatGPT/Perplexity", ou depois que a página estiver no ar.
---

# Agentic Readiness — AEO / AI Visibility

## Quando Usar

Depois que a loja está montada (cadeia 07a→07d) e — idealmente — os criativos já saíram (08), antes do consistency audit (09) e do launch. A página precisa estar NO AR: esta skill audita o que o robô de AI encontra de verdade, não o que está planejado.

**Por que vale o tempo:** comprador que chega via assistente de AI converte mais que o tráfego orgânico comum, e a fatia de shoppers US que usa AI pra decidir compra só cresce. O Shopify já liga a infraestrutura por default (Agentic Storefronts auto-ativado pra merchants US elegíveis, `/llms.txt` e endpoint `/api/mcp` gerados nativamente em toda loja) — o robô de AI **vai** passar na sua página de qualquer jeito. A pergunta é se ele acha o que precisa pra te citar. A copy Hopkins-style que a Aura escreve otimiza pra humano; agentes leem Schema.org, GTIN, políticas e specs verificáveis. São camadas complementares: esta skill entrega a segunda.

**Member stage (rule `member-stage-awareness.md`):** este é um checklist barato, de execução única, sem custo de tool — vale pra TODO stage, inclusive starter. Não pule pra "quando escalar": grande parte das lojas tem título/dados ruins pra query de agente, então arrumar agora é vantagem que compõe. A única adaptação por stage é de expectativa (starter: canal novo sem autoridade rankeia devagar — configure e esqueça; scaling: monitore tráfego de referral de AI como fonte incremental na Skill 12).

## Fontes desta skill (IMPORTANTE — sem base Aura)

Esta skill **NÃO consulta a base de conhecimento Aura** (`search_knowledge`): não existe domínio de AEO/agentic commerce lá — o assunto é recente demais. **Não invente query pra base nesta skill.** As fontes são: (1) docs oficiais (Shopify Agentic Storefronts/`shopify.dev/docs/agents`, Perplexity Merchant Program, Google Merchant Center), (2) verificação direta na loja viva (`curl`/`WebFetch` na PDP, `/robots.txt`, `/llms.txt`), e (3) os artefatos que as fases anteriores já geraram (JSON-LD e agent-facts da 07b, oferta da 04, FAQ da 06). Se precisar de doc atualizada da web, siga a rule `resilient-fetch.md`.

## Pré-flight (OBRIGATÓRIO)

- [ ] `workspace/[produto]/manifest.json` existe e é parseável (senão → escape ES2: rebuild ou restore de `.manifest-backup-*.json`)
- [ ] **Idioma:** ler `report_language` de `workspace/profile.md` (default `pt-BR`; também em `manifest.report_language`). Todo output interno e conversa usam esse idioma. Conteúdo que vai pra loja (specs, FAQ, llms.txt) é **sempre em inglês US** — é superfície pública que o robô lê (rules 0 e 8b do CLAUDE.md).
- [ ] `07b-page-build` em `manifest.skills_completed` E `manifest.storefront.page_url` presente (página publicada). Sem página no ar não há o que auditar.
- [ ] Acesso ao Shopify admin da loja (canal de vendas, apps, robots.txt do tema).

**Se a página NÃO está no ar (escape ES1):** ofereça **(A)** rodar `build page` (07b) primeiro — recomendado —, OU **(B)** gerar só o BLUEPRINT do checklist (tudo que não depende da loja viva: plano de specs, texto do llms.txt, instruções de registro) marcando `manifest.skipped_preflight += ["07b-page-build"]` e deixando os itens de verificação live como `pending`. Nunca abortar seco.

### Contexto a carregar

1. `manifest.json` → `storefront.page_url`, `store_url`, `stage`, `product_vertical`.
2. `04-offer-builder/dados.json` → garantia, envio, pricing, bundle (viram fatos verificáveis); GTIN/código de barras se o membro informou.
3. `06-copy-engine/dados.json` → FAQ real da página (alimenta FAQ schema e Knowledge Base app).
4. `07-page/deploy-report.json` + `07-page/staging/geo/` (`product-schema.json`, `agent-facts.html`) → o que a camada GEO da 07b (ETAPA 4.5) já gerou. Esta skill **verifica e completa** essa camada, não a recria.

## Fluxo da Skill

### ETAPA 1 — Canal Agentic Storefronts + policies

O canal é o que torna a loja descobrível dentro dos assistentes (ChatGPT, Copilot, Gemini) via Universal Commerce Protocol. Desde mar/2026 vem auto-ativado pra merchants US elegíveis — mas "elegível" exige policies completas.

Guiar o membro no admin:
1. **Shopify admin > Settings > Apps and sales channels** → confirmar o canal **Agentic Storefronts** (ou "Agentic") instalado/ativo. Se a loja é US e ele não aparece, checar elegibilidade nos requisitos do canal (plano, região, policies).
2. **Completar as 3 policies obrigatórias** que o canal exige — o próprio admin marca o que falta (tipicamente: shipping policy, return/refund policy e contact/customer service). Sem elas o canal não expõe a loja. As policies têm que bater com o que a página promete (a 09 confere promise↔config depois).
3. Registrar o status: `enabled` / `pending_policies` / `not_eligible`.

> A loja também expõe nativamente o endpoint `/api/mcp` (Storefront MCP) — não precisa configurar nada, mas confirme com `curl -sI https://<store>/api/mcp` que responde (qualquer status ≠ 404 conta como presente).

### ETAPA 2 — Knowledge Base app da Shopify

O Knowledge Base app é a camada de contexto que os agentes consultam pra responder perguntas sobre a loja (políticas, FAQs, voz de marca). Instalar e popular:

1. Instalar o app **Knowledge Base** da Shopify (App Store, grátis).
2. Popular com dado REAL das fases anteriores — nunca inventar: FAQ da PDP (de `06-copy-engine/dados.json`), políticas de envio/devolução (as mesmas da ETAPA 1), garantia (da 04), e 2-3 parágrafos de brand voice (de `brand.md`, se existir).
3. Conteúdo em inglês US, factual, sem palavra ad-flag (rule 8b — o robô da Meta também lê).

Status: `populated` / `installed_empty` / `pending`.

### ETAPA 3 — Dados estruturados da PDP (auditoria do JSON-LD)

A 07b (ETAPA 4.5) já gerou e injetou o JSON-LD (Product + Offer + AggregateRating + BreadcrumbList). Aqui a auditoria é do que está **no ar**:

1. `curl -s <page_url>` → extrair os blocos `<script type="application/ld+json">` e validar presença/conteúdo.
2. Checklist do que agente de compra consome:
   - **GTIN/EAN** (o código de barras global do produto) no nó Product — é o campo que mais pesa pra matching de catálogo. Se o produto não tem GTIN (white-label novo), documentar o gap e usar `mpn`/`sku` no lugar; não inventar código.
   - **aggregateRating** com contagem real de reviews (se ainda não há reviews, OMITIR o nó — rating inventado é dado estruturado fraudulento).
   - **FAQPage schema** cobrindo as perguntas reais da PDP.
   - **shippingDetails** e **MerchantReturnPolicy** batendo com a config real da loja.
3. Se algum nó falta ou diverge → **a correção acontece na 07b** (é lá que o JSON-LD nasce, valida e injeta como bloco `custom_liquid`). Diga ao membro pra rodar a iteração da 07b com a lista exata de gaps; esta skill não injeta Liquid por fora do pipeline.

Status por item + lista `gaps[]`.

### ETAPA 4 — Bloco de specs legível por agente

Além do JSON-LD (máquina), o agente cita com mais confiança página que tem **fatos em prosa limpa**. A 07b já gera o bloco agent-facts (`data-aura-section="product-facts"`); aqui confira que ele está no ar e que cobre **specs concretas**:

- Materiais/ingredientes com quantidade ("500mg magnesium glycinate per capsule", "100% GOTS certified cotton, 200 GSM")
- Dimensões/peso/quantidade por embalagem
- Certificações verificáveis (GOTS, NSF, cGMP, third-party tested)
- Envio (prazo, origem), devolução (janela, quem paga), garantia (dias, condição)

Regra de ouro: **spec verificável > copy sensorial** pra esta camada. "47-day supply, 90-day money-back" rankeia pra query de agente; "transforms your mornings" não. O bloco NUNCA contradiz o JSON-LD nem a config real — é a mesma verdade em outro formato. Faltou spec que o membro tem? Coletar e mandar pra 07b adicionar. Ícones SVG, nunca emoji (rule 7); zero palavra ad-flag (rule 8b).

### ETAPA 5 — robots.txt liberando os robôs de AI

Verificar `curl -s https://<store>/robots.txt` e confirmar que NENHUM destes user-agents está bloqueado:

`OAI-SearchBot` · `ChatGPT-User` · `PerplexityBot` · `ClaudeBot` · `Google-Extended`

O robots.txt default do Shopify não os bloqueia — o risco é customização antiga em `templates/robots.txt.liquid` (comum em temas que copiaram "bloqueie os bots de AI" de 2023). Se houver bloqueio:
1. `shopify theme pull` antes de editar (rule `shopify-theme-safety.md` — pull-before-edit, `--nodelete`).
2. Remover/ajustar só as regras que bloqueiam esses 5 agents (não mexer no resto do arquivo).
3. Push seguro + re-verificar com curl.

Status: `all_allowed` / `fixed` / `blocked_pending`.

### ETAPA 6 — llms.txt (override opcional)

O Shopify gera `/llms.txt` nativo em toda loja (desde mai/2026). Verificar com `curl -s https://<store>/llms.txt` que existe. O override via `templates/llms.txt.liquid` é **opcional** — vale quando o membro quer controlar a descrição da marca e destacar o mecanismo/claims com as palavras certas:

- Conteúdo: 1 parágrafo de marca + produto hero com mecanismo nomeado (da 04) + links pras políticas + fatos verificáveis. Inglês US, claims sustentados pela research foundation, zero ad-flag.
- Se o membro não quiser customizar, o nativo basta — registrar `native` e seguir.

### ETAPA 7 — Perplexity Merchant Program

Registro grátis, taxa zero, sem mínimo de receita, com caminho simplificado pra lojas Shopify — coloca o catálogo dentro do shopping do Perplexity. Não dá pra automatizar (exige a conta do merchant):

1. Passar ao membro o passo a passo: perplexity.ai → Merchant Program → conectar a loja Shopify.
2. Marcar `registered` / `pending` (pendente NÃO bloqueia o launch — é upside, não gate).

### ETAPA 8 — Qualidade do feed do Google Merchant Center

O feed (o catálogo de produtos que o Google lê) alimenta o Google AI Mode e o shopping dos assistentes. Se o membro tem Merchant Center conectado (app Google & YouTube), auditar o produto hero:

- **Título ≥ 30 caracteres** e descritivo pra query de agente — "Magnesium Glycinate Sleep Support, 120 Capsules" acha comprador; título só com nome de marca não (é o erro da maioria das lojas).
- **Descrição ≥ 500 caracteres** com specs e uso.
- **≥ 3 imagens** do produto.
- **GTIN preenchido** no feed (ou `identifier_exists: false` declarado quando não há).
- Preço/disponibilidade do feed = PDP (mismatch derruba o listing).

Sem Merchant Center conectado: recomendar a conexão (grátis) e marcar `pending` — de novo, upside, não gate.

### ETAPA 9 — Score de AI visibility + wrap-up

Consolidar o checklist num score simples: **itens `pass` / itens aplicáveis** (itens `na` — ex: GTIN inexistente documentado — saem do denominador). Classificar:

| Score | Leitura |
|---|---|
| ≥ 80% | Pronta pra descoberta por agente. Pendências são upside incremental. |
| 50-79% | Funcional com lacunas — listar as 2-3 ações de maior impacto (quase sempre: dados estruturados + canal). |
| < 50% | Invisível pra agente de compra. Resolver ETAPAs 1, 3 e 5 antes do launch. |

O score NÃO bloqueia o launch (quem gateia é a 09) — mas os itens `blocked_pending` de dado estruturado divergente (ETAPA 3) devem ser resolvidos antes, porque a 09 confere promise↔config nas mesmas superfícies.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/07e-agentic-readiness/` antes de salvar.

**`07e-agentic-readiness/agentic-readiness.md`** (humano, no `report_language`) contendo:
1. Score de AI visibility + leitura executiva
2. Tabela do checklist (item → status → o que foi feito/o que falta → quem resolve)
3. Gaps de dados estruturados com a lista exata pra iteração da 07b
4. Pendências que dependem do membro (registro Perplexity, Merchant Center, policies)
5. O que esperar do canal (honesto: descoberta e citação por AI search, não venda mágica no chat — canal novo sem autoridade rankeia devagar)

**`07e-agentic-readiness/agentic-readiness.html`** — companion humano: usar `.claude/templates/aura-report-template.html` (CSS inline, self-contained), abrindo o `<body>` com o bloco SVG da logo copiado LITERALMENTE de `.claude/templates/aura-logo-snippet.html` (NUNCA texto). Componentes aura: `kpi-grid` pro score, `table-wrap` pro checklist, `callout`/`danger` pros gaps, `note` pras pendências. Emojis ✅⚠️❌ OK aqui (relatório interno).

**`07e-agentic-readiness/dados.json`** (estruturado):

```json
{
  "product_slug": "<do manifest>",
  "generated_at": "ISO-8601",
  "report_language": "pt-BR",
  "page_url": "<manifest.storefront.page_url>",
  "checklist": {
    "agentic_channel": { "status": "pass|pending|blocked_pending|na", "policies_complete": true, "notes": "" },
    "storefront_mcp_endpoint": { "status": "pass|pending", "notes": "" },
    "knowledge_base_app": { "status": "pass|pending", "notes": "" },
    "structured_data": { "status": "pass|blocked_pending", "jsonld_types_live": ["Product", "Offer"], "gtin_present": false, "gaps": [] },
    "agent_facts_block": { "status": "pass|pending", "specs_covered": ["materials", "shipping", "guarantee"] },
    "robots_txt": { "status": "all_allowed|fixed|blocked_pending", "bots_checked": ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Google-Extended"] },
    "llms_txt": { "status": "native|overridden|pending" },
    "perplexity_merchant": { "status": "registered|pending" },
    "merchant_center_feed": { "status": "pass|pending|na", "title_ok": true, "description_ok": true, "images_ok": true, "gtin_in_feed": false }
  },
  "ai_visibility_score": 0,
  "pending_actions": []
}
```

### Atualizar manifest

- `skills_completed += ["07e-agentic-readiness"]`, `updated_at`
- Bloco **`agentic`**: `{ "ready": <score ≥ 80 e sem blocked_pending>, "channel_enabled": <bool>, "score": <0-100>, "checked_at": "ISO-8601" }` — a Skill 09 lê como contexto informativo (não gate) e a Skill 12 lê pra tratar tráfego de referral de AI como fonte incremental de scale.
- Regenerar o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html).

## Mensagem Final

(idioma = `report_language`; primeira versão como draft — rule `iteration-driven-refinement`)

> "Checklist de agentic readiness rodado: sua loja está **[score]%** pronta pra ser encontrada por agentes de compra com AI (ChatGPT, Perplexity, Google AI Mode).
>
> O que já está de pé: [2-3 itens pass]. O que depende de você: [pendências — ex: completar as policies do canal, registrar no Perplexity Merchant Program]. O que volta pra 07b: [gaps de dados estruturados, se houver].
>
> Expectativa honesta: isso é descoberta e citação por AI search — canal de aquisição incremental de custo zero, não substituto dos ads. Loja nova rankeia devagar; o valor é compor desde o dia 1.
>
> Revisa o relatório e me diz o que ajustar. Próximo passo: diga **'consistency audit'** pra rodar o gate de launch (Skill 09)."

---

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) todo status `pass` foi VERIFICADO na loja viva (curl/print), não assumido — item não verificado é `pending`, nunca `pass`; (2) nenhum dado inventado (GTIN, rating, review count — se não existe, o gap está documentado, não preenchido); (3) score bate com a aritmética do checklist (pass/aplicáveis); (4) conteúdo público gerado (specs, llms.txt, Knowledge Base) está em inglês US, sem ad-flag word e consistente com 04/06/config real; (5) `agentic-readiness.md` + `.html` (logo SVG) + `dados.json` salvos, manifest atualizado (`skills_completed`, bloco `agentic`, `updated_at`), painel regenerado. Issue dentro do escopo → fix inline. Divergência entre policy da loja e promessa da página (precisa decisão do membro) → surface curto.
