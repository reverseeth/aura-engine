---
name: scale-engine
description: Plano de escala vertical no Meta Ads governado pelo Scaling Protocol do cânone ad-taxonomy (48 a 72h acima do target → +20%, depois a cada 24h; −20% só após 24 a 48h persistentes abaixo do breakeven; gate click-based de duas portas; as duas exceções, promo com data-fim e new reason to be scaling; reset da meia-noite sobre o gasto real), com as 3 escolas de intensidade (cost-cap duplication + surf, bid cap campanha monstro, budget-doubling) recomendadas por stage, promoção do breakthrough pra ABO paralelo, execução opcional em PAUSED via Meta MCP, gate de custo fixo antes de qualquer corte por ROAS, PSM lido do manifest (nunca recalculado), cash flow e projeção 30/60/90, toda mudança de budget no ad-log e a volta pra creative-engine quando falta criativo. Só breakthrough libera escala. Use quando o membro disser "scale", "escalar", "plano de escala", "crescer", "maximizar", ou quando os ads estão estáveis e quer aumentar spend de forma sistemática.
---

# Scale Engine · Passo 18 · apelido antigo: 12 <!-- gen:title -->

## Quando usar

Quando o membro tem breakthrough provado (KPI do ad melhor que o da campanha e puxando spend, medido pela `ad-analysis`) e quer subir spend de forma sistemática sem queimar conta. Esta é a camada de execução: qual régua seguir, que estrutura montar, quanto duplicar, quando surfar, quando recuar. Sem breakthrough não é hora de escalar: é hora de mais criativo (`creative-engine`) e melhor oferta (`offer-builder`); KPI winner não libera escala, e a ETAPA 3 manda de volta sem culpa.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova.

- [ ] `ad-strategy/dados.json` e `ad-analysis/dados.json` existem; manifest com `ad-analysis` em `skills_completed`
- [ ] `manifest.psm_real` gravado por análise recente, junto com `manifest.psm_real_basis`
- [ ] Ao menos um `breakthrough` nas 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2; `winners[]` legado é reclassificado pela régua do §2 antes de liberar; Post ID (`champions[]`) é opcional

Arquivo faltando (ES1): (A) rodar a skill faltante agora ou (B) seguir com default genérico marcando `manifest.skipped_preflight`. Íntegra em `reference/contexto.md`.

## Contexto a carregar

Leia nesta ordem (detalhe em `reference/contexto.md`):

1. `workspace/profile.md` (budget, stage, `report_language`); `offer-builder/offer-builder.md` (fallback `relatorio.md`) e `offer-builder/dados.json` (breakeven, `cogs_breakdown`, PSM projetado) mais `manifest.margin_warning`
2. `ad-strategy/ad-strategy.md`; TODAS as análises de `ad-analysis/` em ordem cronológica e o `dados.json`; planos anteriores em `scale-engine/`
3. Os dois cânones, obrigatórios: `.claude/lib/ad-taxonomy/README.md` (§2 classes; §5 Scaling Protocol, ABO paralelo, gate click-based, reset da meia-noite) e `.claude/lib/unit-economics/README.md` (§1 margem de contribuição não é lucro; §4 espiral do ROAS); onde a skill divergir, o cânone vence
4. Se existirem: `manifest.agentic`, `finance-engine/dados.json` (seis campos, cada um com o ponto de uso e o fallback na tabela do arquivo; esta skill lê e nunca recalcula), `workspace/[produto]/ad-log.md` (a última mudança de budget e há quanto tempo; o gate de 24h se confere no log), `sourcing/dados.json` (`calendar.volume_confirmation_30_60_90`, `calendar.reorder_point_days`) e `manifest.promo.active` (janela com data-fim é da `promo-engine`)
5. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill scale-engine --domain <domínio desta etapa>` (domínios `scaling` e `finance-projections`); `best_query` exata com `deep=true`, no máximo 10 buscas por etapa; as queries embutidas em `reference/` são o mínimo garantido; nunca query genérica nem busca repetida

Antes de qualquer recomendação, leia `reference/ancoras-economicas.md`: o breakeven CPA vem de `unit_economics.weighted_margin_per_order` (o manifest prevalece quando `target_cpa` e `breakeven_roas` existem lá); nenhum corte de spend por queda de ROAS sem os custos fixos na mesa (com a `finance-engine`, o `roas_spiral.verdict` decide pela tabela; sem os fixos, a recomendação vira pergunta); número sem o fixo descontado é margem de contribuição, nunca lucro; `manifest.psm_real` se LÊ, e a comparação de 20% com `psm_theoretical` só vale na base `shopify_new_customer`.

Idioma: output interno e conversa no `report_language`; copy e VOC literal sempre em inglês US.

## Fluxo da skill

### ETAPA 1 · Receber o panorama atual

Leia `reference/panorama-e-prontidao.md`. Pré-popule dos artefatos e pergunte numa mensagem só o que falta: AOV real (da `finance-engine` ou do membro), CPM atual, custo fixo mensal (não pergunte o que já está gravado), share de purchases em 7-day click (`manifest.click_based_purchase_share`), fuso do ad account e caixa disponível.

### ETAPA 2 · Classificar o estágio de escala

Mesmo arquivo. Stage canônico é `manifest.stage`; a sub-fase por spend diário (teste, tração, escala inicial, agressiva, otimização) é diagnóstico e vive em `scale_phase` do `dados.json`, nunca em `manifest.stage`.

### ETAPA 3 · Análise de prontidão

Mesmo arquivo. Rode os frameworks de prontidão (lista no arquivo) e a tabela de pré-requisitos: breakthrough provado (eliminatório), gate click-based de duas portas, PSM real em base válida, margem por pedido, CPA estável, CPM saudável, pipeline de criativo, EMQ ≥ 6.0, cash flow e volume do fornecedor. Cada falha vira bloqueio documentado com ação e skill.

### ETAPA 3.5 · Scaling Protocol (a espinha única)

Leia `reference/scaling-protocol.md`. Subida só com os dois gates (48 a 72h acima do target e click-based verde), passo de +20% a cada 24h conferidas no `ad-log.md`; as duas exceções do cânone (promo com data-fim, new reason to be scaling); teto medido `payback.scale_ceiling_monthly_spend` quando existe; descida de −20% só após 24 a 48h persistentes abaixo do breakeven, e corte por ROAS que ainda paga o variável passa pelo gate de custo fixo; estagnou, a ação é fora do ad account (criativo, funil, oferta, learnings, Chunk Up). Reset da meia-noite em toda subida: o dia seguinte começa em ~50% do gasto REAL, no fuso do ad account, gravado em `midnight_reset`. Toda mudança de budget entra no `ad-log.md` no ato.

### ETAPA 4 · As 3 escolas de escala

Leia `reference/escolas-de-escala.md`. Bidding em escala: highest volume é o default da campanha principal; cost cap é ferramenta de zombie campaign ou da duplicação da Escola A; bid cap só com a ressalva declarada. Apresente as três (A cost-cap duplication + surf, B bid cap campanha monstro, C budget-doubling) na tabela do arquivo, marque o default do stage (starter C; validating C ou B; scaling A) e deixe o membro escolher; grave `scaling_school` e `bidding`. Acima de US$ 1k/dia sustentado, avalie a graduação pra Advantage+ Sales; value optimization só com spread de AOV acima de ~30%.

### ETAPA 4.4 · Promoção do breakthrough pra ABO

Leia `reference/abo-conta-nova-mcp.md`. Campanha ABO paralela reusada, 1 ad set por breakthrough com ~10% do budget da principal, o ad original segue no CBO, o degrau normal governa dali em diante, linha no ad-log no ato; registre em `abo_promotions[]`.

### ETAPA 4.5 · Quando o budget trava a entrega

Mesmo arquivo. Conta ou produto: CPM muito acima do nicho é conta cansada, e a saída legítima é conta nova no próprio Business Manager. Limite ético inviolável: nada de farmar conta, BM de terceiro, cloaking ou réplica.

### ETAPA 4.6 · Execução opcional via Meta MCP

Mesmo arquivo. Mesma cascade da `ad-strategy` (oficial → Pipeboard → manual); tudo nasce PAUSED e o membro ativa; só as duas automações de proteção do cânone §6, criadas desativadas; o reset da meia-noite nunca vira automação; IDs em `mcp_execution` e cada ação no ad-log.

### ETAPA 5 · Credibilidade da loja

Leia `reference/credibilidade-e-cash-flow.md`. Página social viva, reviews reais, highlights de confiança e gestão diária de comentários; prova social comprada, não.

### ETAPA 6 · Cash flow

Mesmo arquivo. Payout lag conservador de 7 a 14 dias em loja nova (rolling reserve), frameworks de teto de risco, o check obrigatório antes de escalar mais de 2× em menos de 7 dias (float ≥ 1,5 × budget × lag, fornecedor, ponto de recompra, cartão reserva) e o gap projetado; com a `finance-engine`, use `cash.cash_needed_90d`, `total_float_days` e `runway_months`. Gap acima de 50% do caixa bloqueia escala agressiva.

### ETAPA 7 · Projeção realista 30/60/90

Leia `reference/projecao-30-60-90.md`. Cenário base e pessimista com AOV e breakeven reais, a coluna de resultado operacional e o teto de escala quando os fixos existem, e o template de cash flow com o payout lag real. Alerte se o pico de float passar de 70% do caixa.

### ETAPA 8 · Creative diversity como combustível

Leia `reference/creative-diversity.md`. Frameworks, tabela de conceitos por sub-fase calibrada pelo stage, expansão de canal com criativo validado via `'recycle'` na `content-recycler` e o canal incremental de agentes de AI.

### ETAPA 9 · Checklist operacional semanal

Leia `reference/checklist-e-alertas.md`. Reset à meia-noite todo dia, surf só na Escola A, 4Pi na segunda, degrau na terça (com o ad-log), análise semanal na sexta, batch no domingo, e o monthly review.

### ETAPA 10 · Sinais de alerta

Mesmo arquivo. Régua única de frequency diária (abaixo de 1,3 é folga; acima de 1,4 com CTR caindo 20% pede refresh; acima de 1,5 em prospecting pede batch novo), CPA acima do breakeven por 3 dias, CPM subindo 30% em duas semanas, budget que não gasta, gates vermelhos por mais de uma semana, cash gap e fulfillment. Os gatilhos de volta pra `creative-engine` estão no mesmo arquivo; ela lê `NEXT_BATCH_IDEAS.md` e `scale-directives.md`.

## SALVAR

Todo relatório `.md` ganha `.html` por `python3 tools/render_report.py <md>` (isentos: `scale-directives.md`, `dados.json`, `ad-log.md`). Em `workspace/[produto]/scale-engine/`: `scale-engine.md` (seções listadas em `reference/salvar-e-dados-json.md`), `scale-directives.md` e `dados.json` no schema do mesmo arquivo (schema em `.claude/templates/schemas/`); as linhas do `ad-log.md` já foram gravadas no ato de cada mudança. Depois `python3 tools/manifest.py <slug> complete scale-engine` e `set` com `plan_id`, `psm_real`, `scaling_school`, `fixed_costs_monthly` (quando informado) e `stage` no vocabulário canônico; então `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`. Draft, não decreto. Pronto: a régua do protocolo, a escola recomendada com o setup concreto, a promoção pra ABO se houver breakthrough novo e o número do reset da meia-noite de hoje; volte com `'ad analysis'`. Não pronto: os bloqueios com ação e skill por bloqueio; resolve e diz `'scale'` de novo.
