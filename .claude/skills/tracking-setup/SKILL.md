---
name: tracking-setup
description: Instalação e validação de tracking pré-launch. Instala o tracking sempre pelo Wetracked, em todos os stages: o app da Shopify que dispara o Meta Pixel no navegador e manda a Conversions API pelo servidor a partir do backend da loja, com Advanced Matching e dedup por event_id, como fonte única (data sharing do app Facebook & Instagram desligado, nenhum outro app de pixel, CAPI ou snippet no tema), valida o Event Match Quality de 6.0 ou mais na escala 0 a 10 do Events Manager (com o caminho pending_traffic pra loja pré-launch sem volume, destravado por pedido-teste validando o Purchase), fixa a janela de atribuição baseline de 7 dias pós-clique e 1 dia pós-visualização com o Click ID preservado, soma em scaling a camada opcional de atribuição (Triple Whale ou Aimerce, só leitura, nunca segunda fonte de eventos) e as camadas complementares de survey pós-compra e comportamento on-site, fixa o contrato de leitura (Blended ROAS como P&L, CAC diferente de CPA) e grava o bloco manifest.tracking que destrava os pré-flights da creative-engine e da ad-strategy. Roda depois do deploy da página e antes dos criativos. Use quando o membro disser "tracking", "pixel", "capi", "analytics setup", "configurar tracking", ou depois de a página estar no ar.
---

# Tracking Setup · Passo 9 · apelido antigo: 07c <!-- gen:title -->

## Quando usar

Quando a página já está no ar (`page-build`) e o membro precisa garantir que cada visita e compra seja medida antes de gastar com ads. A `creative-engine` e a `ad-strategy` exigem no pré-flight `manifest.tracking.tracking_ready == true`; esta skill constrói, valida e grava esse contrato. É operacional (passo a passo no Shopify e no Events Manager), não conceitual.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe e parseia; se não parseia, escape ES2: (A) rebuild ou (B) restore do backup mais recente.
2. `page-build` em `skills_completed`; senão, (A) rodar `build page` agora ou (B) seguir só com pixel e CAPI marcando `skipped_preflight` e avisando que a validação dos eventos de funil fica incompleta.
3. Budget legível (`manifest.budget_daily`; em manifest legado, `budget_tier` ou o profile); acesso ao Shopify admin e a uma conta Meta Business com Pixel ou Dataset.
4. A `consistency-audit` gateia o launch, não o tracking: com `launch_recommendation == "BLOCK"`, só registre no fim que o launch está bloqueado e siga instalando.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`), com a régua de linguagem simples (EMQ, CAPI, MMM e NCPA explicadas na primeira vez); esta skill não gera copy consumidor-final.
2. `manifest.stage` e `budget_daily`: a fonte de eventos é o Wetracked em todo stage; o stage e o budget só decidem se cabe a camada opcional de atribuição em scaling (detecção automática pela rule `member-stage-awareness`).
3. Base pelo índice (21 entradas em 6 domínios): `python3 .claude/lib/kb-index/kb_lookup.py --skill tracking-setup --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa; as queries embutidas nos arquivos de `reference/` são piso obrigatório, rodam sempre e não contam no teto; carregue já o sistema-espinha CAPI & Pixel Data / Event Match Quality (query em `reference/contexto.md`). Três entradas do índice ficam com a `retention-engine` (arquitetura de flow, hot-time anchor, métricas de SMS).
4. Cascade de MCP pra ler o EMQ: MCP oficial da Meta (`mcp__meta__ads_*`), Pipeboard (`mcp__meta-ads__*`), manual (print do Events Manager); logue o caminho em `source`. Sem MCP, o manual é o normal, não degradação.

## Fluxo da skill

### ETAPA 1 · Pixel pelo Wetracked

Leia `reference/pixel.md`. Dataset certo no Business Manager e no ad account da `ad-strategy`; app Facebook & Instagram da Shopify com o data sharing desligado (fica só pro catálogo); nenhuma outra fonte de pixel (custom pixel da Meta em Customer events, app de pixel ou CAPI, snippet no `theme.liquid`, CAPI de 1 clique); Wetracked instalado pela Shopify App Store e conectado ao mesmo Pixel ID. Confirme no Test Events os 5 eventos do funil (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase), cada um uma vez só.

### ETAPA 2 · Conversions API (CAPI) pelo Wetracked

Leia `reference/capi.md`. Conversions API ativa no Wetracked pro Dataset da ETAPA 1, com Advanced Matching por dado first-party do pedido (email, telefone, nome e endereço hasheados); no Events Manager cada evento aparece como Browser + Server, com o Wetracked como fonte server-side única. Puxe os dois sistemas do arquivo (engaged lead como evento customizado de conversão; os três tipos de tráfego, com o email capturado on-site como tráfego que você possui). Dedup por `event_id` igual no navegador e no servidor; Purchase em dobro = sobrou outra fonte ligada, volte à ETAPA 1.

### ETAPA 3 · Validar o Event Match Quality (EMQ de 6.0 ou mais, gate técnico)

Leia `reference/emq.md`. O EMQ é escore de 0 a 10 por evento, nunca porcentagem; leia pelo MCP ou pelo print do membro (dupla coluna Browser e Server e o escore do Purchase). Decisão: 8.0 ou mais é PASS; de 6.0 a 7.9 é PASS com `emq_warn` e recomendação de Advanced Matching completo; sem dados por falta de tráfego (loja pré-launch com Pixel e CAPI corretos e os 5 eventos confirmados) é PASS condicional `pending_traffic`, com `emq.score: null`, `tracking_ready: true` e `emq_pending: true`, obrigatoriamente validado por pedido-teste real (Bogus Gateway em preview ou pedido de 1 dólar com refund) chegando com a dupla coluna; abaixo de 6.0 com volume é BLOCK, com o diagnóstico do arquivo (servidor do Wetracked desligado, dado do cliente não passando, sem volume, fonte duplicada) e o escape ES1 (re-medir ou seguir com `tracking_ready: false` e o risco aceito). A `ad-analysis` re-lê o EMQ no dia 3 de tráfego.

### ETAPA 3B · Janela de atribuição e preservação do Click ID

Leia `reference/atribuicao-e-click-id.md` e puxe os três sistemas. Baseline de janela 7 dias pós-clique e 1 dia pós-visualização, documentada, com Incremental Attribution desligado no launch; o teste 7DC-only é diagnóstico agendado da `scale-engine` num slot de teste não-criativo, nunca default; Click ID preservado de ponta a ponta (jornada sem trocar de domínio raiz, parâmetro presente no Purchase mais recente ou no pedido-teste, captura server-side como parte do valor de stack pago), porque recuperá-lo restaura até 40% mais conversões atribuídas.

### ETAPA 4 · Analytics stack (Wetracked em todo stage)

Leia `reference/analytics-stack.md` e puxe os três sistemas (stack em 3 camadas, hierarquia de decisão, três níveis de KPI). A fonte de eventos é sempre o Wetracked; em `scaling` cabe uma camada opcional de leitura de atribuição: Triple Whale (a partir de mil dólares por dia) ou Aimerce (acima de 3 mil por dia), com o envio de eventos pra Meta delas desligado; nunca Elevar, Stape, Littledata, Segment, GTM custom ou CDP como fonte. O blended decide o negócio, a plataforma decide a otimização, o terceiro levanta red flag. Pergunte o que o membro já tem; outro app como fonte de eventos migra pro Wetracked; Triple Whale com o mapa de modelos puxado, nunca decisão no nível do anúncio; Aimerce com a ressalva por escrito de que identity resolution é ilegal na Europa. Camadas complementares em qualquer stage: survey pós-compra "how did you first hear about us" (a camada imune a cookie) e a camada on-site (4 métricas de página e os 3 relatórios do Hotjar). Grave em `manifest.tracking.analytics_stack`.

### ETAPA 4B · Contrato de leitura

Leia `reference/contrato-de-leitura.md` e puxe os quatro sistemas. Blended ROAS (receita do Shopify ÷ spend total de todas as plataformas) é a métrica de P&L; CAC = spend ÷ clientes novos do Shopify, nunca o CPA da plataforma (cânone `.claude/lib/unit-economics/README.md` §3); branded search é o ponto cego da atribuição de terceiro (o TA do Triple Whale infla o Google; o Google Search Stronghold é proteção de marca, não canal incremental). Handoffs: a `ad-analysis` lê pela hierarquia de decisão, a `scale-engine` pelo gate click-based e a `finance-engine` pelo Blended ROAS.

### ETAPA 5 · Verificação final e handoff

Leia `reference/verificacao-final.md`: a checklist de sete itens (Dataset certo, Wetracked como fonte única com o data sharing do app Facebook & Instagram desligado, 5 eventos, CAPI do Wetracked com Advanced Matching e sem fonte duplicada, EMQ ou `pending_traffic` com pedido-teste, janela baseline com Click ID, stack e contrato de leitura no relatório).

## SALVAR

Leia `reference/salvar-dados-e-manifest.md`. `mkdir -p workspace/[produto]/tracking-setup/`; `tracking-setup.md` nos oito blocos do arquivo (pixel, CAPI, EMQ com o caminho de verificação, atribuição, stack com razão e camadas complementares, contrato de leitura, checklist, próximos passos), `tracking-setup.html` por `python3 tools/render_report.py workspace/[produto]/tracking-setup/tracking-setup.md` e `dados.json` no schema do arquivo (`pixel`, `capi`, `attribution`, `emq` com `score` numérico ou `null`, `analytics_stack`, `tracking_ready`). Manifest pelo script: `python3 tools/manifest.py <slug> complete tracking-setup` e `set tracking` com o bloco aninhado (`pixel_installed`, `capi_active`, `emq_score`, `emq_pending`, `analytics_stack`, `tracking_ready`; nunca campos flat), `tracking_id`, e `python3 .claude/lib/workspace-index/build_index.py <slug>`. `tracking_ready: false` gravado por risco aceito faz a `creative-engine` e a `ad-strategy` herdarem o aviso.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, no `report_language`: pixel e CAPI prontos pelo Wetracked, EMQ (ou o estado `pending_traffic` explicado), janela e Click ID fixados, camada de atribuição (quando houver), o combinado de leitura (Blended ROAS decide se dá lucro) e o próximo passo 'checkout', seguido de 'bonus delivery', 'retention' e 'creatives'. Antes de declarar pronto, o self-audit silencioso dos sete itens do arquivo.
