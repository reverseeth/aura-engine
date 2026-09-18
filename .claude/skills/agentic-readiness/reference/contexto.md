# Agentic Readiness · Referência: Quando usar, fontes da skill, pré-flight e contexto a carregar

> O texto integral de quando usar (posição na cadeia, por que vale o tempo, adaptação por stage), das fontes da skill (docs oficiais, loja viva e artefatos anteriores, sem base de conhecimento), do pré-flight com o escape da página fora do ar e do contexto a carregar. Abra antes da ETAPA 1.

## Quando Usar

Depois que a loja está montada (cadeia `page-design`→`checkout-aov`) e — idealmente — os criativos já saíram (`creative-engine`), antes do consistency audit e do launch. A página precisa estar NO AR: esta skill audita o que o robô de AI encontra de verdade, não o que está planejado.

**Por que vale o tempo:** comprador que chega via assistente de AI converte mais que o tráfego orgânico comum, e a fatia de shoppers US que usa AI pra decidir compra só cresce. O Shopify já liga a infraestrutura por default (Agentic Storefronts auto-ativado pra merchants US elegíveis, `/llms.txt` e endpoint `/api/mcp` gerados nativamente em toda loja) — o robô de AI **vai** passar na sua página de qualquer jeito. A pergunta é se ele acha o que precisa pra te citar. A copy Hopkins-style que a Aura escreve otimiza pra humano; agentes leem Schema.org, GTIN, políticas e specs verificáveis. São camadas complementares: esta skill entrega a segunda.

**Member stage (rule `member-stage-awareness.md`):** este é um checklist barato, de execução única, sem custo de tool — vale pra TODO stage, inclusive starter. Não pule pra "quando escalar": grande parte das lojas tem título/dados ruins pra query de agente, então arrumar agora é vantagem que compõe. A única adaptação por stage é de expectativa (starter: canal novo sem autoridade rankeia devagar — configure e esqueça; scaling: monitore tráfego de referral de AI como fonte incremental na Skill `scale-engine`).

## Fontes desta skill (IMPORTANTE — sem base Aura)

Esta skill **NÃO consulta a base de conhecimento Aura** (`search_knowledge`): não existe domínio de AEO/agentic commerce lá — o assunto é recente demais. **Não invente query pra base nesta skill.** As fontes são: (1) docs oficiais (Shopify Agentic Storefronts/`shopify.dev/docs/agents`, Perplexity Merchant Program, Google Merchant Center), (2) verificação direta na loja viva (`curl`/`WebFetch` na PDP, `/robots.txt`, `/llms.txt`), e (3) os artefatos que as fases anteriores já geraram (JSON-LD e agent-facts da `page-build`, oferta da `offer-builder`, FAQ da `copy-engine`). Se precisar de doc atualizada da web, siga a rule `resilient-fetch.md`.

## Pré-flight (OBRIGATÓRIO)

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

- [ ] `workspace/[produto]/manifest.json` existe e é parseável (senão → escape ES2: rebuild ou restore de `.manifest-backup-*.json`)
- [ ] **Idioma:** ler `report_language` de `workspace/profile.md` (default `pt-BR`; também em `manifest.report_language`). Todo output interno e conversa usam esse idioma. Conteúdo que vai pra loja (specs, FAQ, llms.txt) é **sempre em inglês US** — é superfície pública que o robô lê (rule 0 do CLAUDE.md).
- [ ] `page-build` em `manifest.skills_completed` E `manifest.storefront.page_url` presente (página publicada). Sem página no ar não há o que auditar.
- [ ] Acesso ao Shopify admin da loja (canal de vendas, apps, robots.txt do tema).

**Se a página NÃO está no ar (escape ES1):** ofereça **(A)** rodar `build page` (`page-build`) primeiro — recomendado —, OU **(B)** gerar só o BLUEPRINT do checklist (tudo que não depende da loja viva: plano de specs, texto do llms.txt, instruções de registro) marcando `manifest.skipped_preflight += ["page-build"]` e deixando os itens de verificação live como `pending`. Nunca abortar seco.

### Contexto a carregar

1. `manifest.json` → `storefront.page_url`, `store_url`, `stage`, `product_vertical`.
2. `offer-builder/dados.json` → garantia, envio, pricing, bundle (viram fatos verificáveis); GTIN/código de barras se o membro informou.
3. `copy-engine/dados.json` → FAQ real da página (alimenta FAQ schema e Knowledge Base app).
4. `page/deploy-report.json` + `page/staging/geo/` (`product-schema.json`, `agent-facts.html`) → o que a camada GEO da `page-build` (ETAPA 4.5) já gerou. Esta skill **verifica e completa** essa camada, não a recria.
