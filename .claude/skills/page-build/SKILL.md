---
name: page-build
description: Segunda skill da fase STOREFRONT. Compila o design/page.html aprovado na page-design em sections Liquid por código (liquid-converter.py em batch ou Modo C por section, nunca por reasoning), popula o template JSON com a copy real, renomeia blocks e restaura SVGs grandes, valida cada section com shopify-plugin shopify-liquid (3 retries) e o template contra os schemas, bloqueia imagem vazia e placeholder residual, gera o JSON-LD Schema.org e o bloco de agent-readable facts, roda o gate de performance budget, faz o deploy seguro no Shopify (shopify-theme-safety integral, web fonts provisionadas, marker data-aura-build, smoke test), conduz a publicação com aprovação do membro (grava manifest.storefront) e fecha com o fidelity check por visão contra o design aprovado. Use quando o membro disser "build page", "deploy", "subir página", depois de aprovar o design na page-design.
---

# Page Build · Passo 8 · apelido antigo: 07b <!-- gen:title -->

## Quando usar

Segunda e última skill da fase STOREFRONT (`page-design` → `page-build`). O `design/page.html` aprovado é a fonte única de verdade visual; esta skill o compila em Liquid por CÓDIGO, não por reasoning, popula o template com a copy real, passa os gates e deploya no Shopify. O Claude entra só pra splitar o HTML, renomear blocks depois do compile, reimplementar interações removidas pelo conversor e validar. Toda decisão de conteúdo e design nasceu na `page-design`; esta skill não re-decide página.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

1. `report_language` de `workspace/profile.md` (default `pt-BR`): `page-report.md` e conversa nesse idioma, com a linguagem simples da regra 0; copy pública sempre em inglês US
2. `consistency-audit/dados.json`, se existir: `BLOCK` não trava o deploy (a página existir não gasta dinheiro), mas avise os itens críticos; `CAUTION` pede confirmação; `GO` ou ausente segue
3. Sob `workspace/[produto]/page/`: `design/page.html` (sem ele, PARE e mande pra `page-design`; não existe "gera Liquid direto"), `design-tokens.json` parseável, `page-plan.json` com `strategy`, `sections_plan` (com `media`, o mapa de mídia) e `section_order`, manifest com `page-design` em `skills_completed`, plugin `shopify-plugin:shopify-liquid` disponível
4. Dirs de staging `page/staging/{html,sections,templates,geo}/` e as variáveis de path de `reference/contexto.md` (`PRODUTO`, `PAGE_DIR`, `DESIGN_HTML`, `STAGING_DIR`, `THEME_DIR`, `TOOLS_DIR`, `STORE`)

Íntegra do pré-flight, dos outputs e dos paths em `reference/contexto.md`.

## Contexto a carregar

Toda decisão de conteúdo vem da `page-design`. Nos pontos de implementação manual onde esta skill decide sozinha (selling plan, buy box, desconto Shopify, countdown), rode `python3 .claude/lib/kb-index/kb_lookup.py --skill page-build --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa (as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto); nunca query genérica nem busca repetida. As rules `shopify-theme-safety.md` e `reverse-order-insertion.md` valem inteiras no deploy e nos ajustes do template JSON. Leia `reference/padroes-do-conversor.md` antes de afirmar qualquer capacidade do conversor: os nove padrões que ele aplica por código e o que ele NÃO faz (ícones em 3 camadas, countdown, selling plan com os números da `offer-builder`, custom_css por block).

## Fluxo da skill

### ETAPA 1 · SPLIT (HTML aprovado → fragmentos por section)

Leia `reference/split-e-compile.md`. Um fragmento por `<section data-aura-section="X">` em `staging/html/<X>.html` (ids iguais a `sections_plan[].id`) e o CSS em `staging/html/page.css`, tirando de fora o bloco `<style data-aura-fonts>` (carregamento de fonte pelo caminho do arquivo de design, que não existe na loja; a família dele é provisionada no 6.4b). Sem marcadores, splite pelo `section_order` ou peça o HTML re-emitido; nunca chute fronteira de section. `page_type: quiz` no plano: o funil inteiro é UMA section (`reference/quiz-sections.md`), que governa o split, os blocks por tela, o CSS estático que faz o funil andar, o formulário de compra de cada resultado e o que muda no check de IDs, no GATE 1 e no smoke test.

### ETAPA 2 · COMPILE+POPULATE (liquid-converter.py, uma invocação)

Mesmo arquivo. `tools/design-clone/liquid-converter.py` é o conversor canônico: caminho preferido `--batch` com `batch-manifest.json` e `--emit-template-json`; Modo C por section só no iteration loop. Nunca rode duas vezes sobre o mesmo output. Depois do compile: rename semântico dos block types pelo `reference/catalogo-de-blocks.md`, tocando os 4 lugares em sincronia; `pricing_tier` expõe `variant_id` e `qty`; interações removidas viram `<details>` ou CSS; restauração obrigatória dos SVGs grandes (grep de `icon-placeholder` até zero).

### ETAPA 3 · VALIDATE (3 retries)

Leia `reference/validate.md`. Cada `.liquid` no `shopify-plugin:shopify-liquid`: validate, auto-fix e revalidate, leitura manual pela tabela de `reference/limitacoes-e-debug.md`; ainda falhou, PARE e reporte. Plugin ausente, instale antes de seguir.

### ETAPA 4 · Validação do template JSON populado

Mesmo arquivo. Section block-based precisa de `blocks{}` e `block_order[]` explícitos (senão renderiza zero blocks); monolítica tem `blocks: {}` legítimo. Rode o snippet de validação cruzada contra os schemas dos `.liquid` antes de todo push; advertorial e listicle exigem `destination_ref`. Check bloqueante: nenhuma section com `media.status: "placeholder"` ou imagem exigida vazia, e zero placeholder `{{MAIÚSCULA}}` residual (grep do arquivo); não existe path "deploya assim mesmo".

### ETAPA 4.5 · GEO / Schema (agent-readability)

Leia `reference/geo-schema.md`. Monte `staging/geo/product-schema.json` (Product, Offer, AggregateRating só com reviews reais, BreadcrumbList, FAQPage com as perguntas idênticas às da página) a partir de `offer-builder/dados.json`, `copy-engine/dados.json` e reviews; sem dado, sem nó. Valide com o script (Product e BreadcrumbList obrigatórios), injete como bloco `custom_liquid` e gere `staging/geo/agent-facts.html` em frases declarativas verificáveis, em inglês US, batendo 1:1 com o Schema e a config da loja. Honestidade: o ganho hoje é discovery e citação, não venda dentro do chat.

### ETAPA 5 · GATE 1, performance budget (blocking, antes do deploy)

Leia `reference/gate-de-launch.md`. Passada de estilo (zero travessão em headline, zero emoji, nenhum aviso inserido). Preços renderizados iguais à arquitetura da `offer-builder` (`subscription_architecture`, `onetime_premium_pct`, `main_sku_price`, tiers de `aov_levers.bundles[]`). GATE 1: imagens por `image_url | image_tag` com `width`, hero sem lazy, zero `<script>` de runtime, CSS filtrado por section; pós-push, HTML até ~200 KB e página total até ~1,5 MB; estouro grosseiro bloqueia o publish. Registre em `deploy-report.json.gates.performance`.

### ETAPA 6 · DEPLOY (shopify-theme-safety integral)

Leia `reference/deploy.md` e siga os doze passos com os comandos do arquivo: 6.1 CLI e detecção da loja (logue `shopify version`); 6.1b produto e oferta de pé na loja por `reference/produto-e-oferta.md` (produto criado ou conferido, cada formato de oferta pelo caminho nativo, IDs de variante em todas as superfícies de compra do template, gravados em `manifest.storefront`, e o check bloqueante de IDs antes do push); 6.2 duplicate do tema live; 6.3 pull com `--nodelete`; 6.4 instalar sections e template mais o marker `data-aura-build` no elemento raiz do hero; 6.4b provisionar web fonts pelo `provision` de cada família em `type.families[]` (Google Fonts por `<link>`, arquivo local do membro como asset do tema com o `@font-face` do `local_fonts.py --mode asset`), só com os pesos usados, e confirmar no HTML servido; 6.5 push com `--nodelete` (`--allow-live` só no tema live) lendo `errors` do `--json`; 6.6 criar a página no admin com o handle exato; 6.7 marker verification (nunca pull depois de push não verificado); 6.8 smoke test; 6.9 preview links e aprovação; 6.10 PUBLISH só com aprovação explícita, backup do live, atribuição do template e `manifest.storefront` gravado; 6.11 fidelity check por visão (screenshots da página no ar e do design aprovado, desktop e mobile), corrigindo divergência real antes de encerrar.

### ETAPA 7 · Reports e iteration loop

Leia `reference/reports-e-iteracao.md`. `page-report.md` (gerando o `.html` por `python3 tools/render_report.py`) e `deploy-report.json` no schema do arquivo; `python3 tools/manifest.py <slug> complete page-build` e `set store_url` se ausente; `python3 .claude/lib/workspace-index/build_index.py <slug>`. Iteration loop: só markup ou CSS de section recompila a section e sobe com `--only`; mudança estrutural nunca regenera o template no ar (pull `--only`, `tools/theme-template-merge.py`, push); re-compile apaga renames e restaurações (reaplique); preço, rating, política ou FAQ mudou, regenere o Schema; sempre pull antes de re-push, sempre revalide. Máximo 3 iterações sem progresso, depois escalate. Antes de declarar concluído, rode o self-audit expandido do fim do arquivo.

## SALVAR

Em `workspace/[produto]/page/`: `staging/html/*.html` e `page.css`, `staging/sections/page-[produto]-*.liquid`, `staging/templates/page.[produto].json`, `staging/geo/product-schema.json` e `agent-facts.html`, `page-report.md` mais `page-report.html`, `deploy-report.json`; o conversor não gera `blocks/*.liquid`. Referência técnica em `reference/limitacoes-e-debug.md`, `reference/acessibilidade-e-do-not.md` e `reference/specialists-e-referencias.md`.

## Mensagem final

Íntegra em `reference/reports-e-iteracao.md`. Publicou: página no ar na `page_url`. Não publicou: página no preview, e sem publicar a campanha da `ad-strategy` não tem URL de destino. Próximo passo: `'tracking'`, depois `'checkout'`, bônus Fase A, retention Fase A e só então `'creatives'`.
