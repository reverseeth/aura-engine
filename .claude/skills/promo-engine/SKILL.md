---
name: promo-engine
description: Engine de janela promocional, dona da promoção de ponta a ponta (Q4 e BFCM, datas sazonais e sales datadas). Orquestra o calendário da janela com as datas e prazos da fonte (começar cedo é a tese central), a preparação (momentum do evergreen, decisão de lead-gen VIP pelo critério de clientes que voltam, estoque pela sourcing, backups pela ops-engine), a oferta da promo (hierarquia de ofertas, store credit, stacking e linguagem), o gate inegociável de recálculo do breakeven ROAS e do CPA com a margem promocional antes de ligar qualquer campanha (sem números recalculados, a skill para), a execução (campanha de promo Broad, WARM60 e HOT90 em paralelo ao evergreen, criativos de melhor ad com banner via brief pra creative-engine, calendário de email e SMS que a retention-engine transforma em assets, surf scaling e reset da meia-noite pelo cânone de ad-taxonomy, tudo logado no ad-log) e a aterrissagem (regra de fim por horário, volta pro evergreen, leitura pós-promo com a ad-analysis e a finance-engine, revival sazonal de winners pelo Desire Calendar). Lateral e sazonal, não é etapa da sequência. Use quando o membro disser "black friday", "bfcm", "promo", "promoção", "sale", "q4", "cyber monday", "desconto sazonal", "mother's day", "valentine's", "flash sale".
---

# Promo Engine · Lateral · apelido antigo: 17 <!-- gen:title -->

## Quando usar

Quando existe (ou vai existir) uma janela promocional com data de fim: Black Friday e Cyber Monday, o Q4 inteiro, datas sazonais ou uma flash sale. Não é fase do pipeline, é skill lateral como a `finance-engine`: dispara por pedido, e a época é o motivo natural de chamar. Pode rodar mais de uma vez por ano, uma rodada por janela. É dona do calendário da janela, da mecânica da oferta promocional, do gate de números recalculados, da estrutura de campanha de promo, do plano de escala dentro da janela e da aterrissagem de volta pro evergreen. A tabela da divisão com as vizinhas está em `reference/contexto.md`: criativo é da `creative-engine`, email e SMS da `retention-engine`, evergreen e escala fora da janela da `ad-strategy` e da `scale-engine`, estoque da `sourcing`, backups da `ops-engine`.

Cânones que governam a skill, citados e nunca redefinidos: `.claude/lib/ad-taxonomy/README.md` §5 (Scaling Protocol e as duas exceções, promo com data-fim entrando direto no budget planejado e o novo motivo de escalar) e `.claude/lib/unit-economics/README.md` §1 e §4. Todo registro de mudança na conta segue `.claude/lib/ad-log/README.md`.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe.
2. `offer-builder/dados.json` existe, fonte do stack de custos, da margem ponderada por pedido e do AOV esperado. Faltando, escape ES1: (A) rodar a `offer-builder` agora, ou (B) pedir ao membro o AOV e o custo por pedido item a item, marcando `manifest.skipped_preflight`. O gate aceita número vindo do membro; o que ele não aceita é número estimado.
3. Loja no ar (`manifest.storefront.page_url` ou confirmação do membro). Sem loja, o caminho é o pipeline normal, não esta skill.
4. Histórico de ads não é pré-requisito, mas muda a rota de criativo (com winner provado, melhor ad com banner; sem nenhum, statics de foto com oferta). Loja nova na semana da Black Friday é não, e a recomendação honesta é essa.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`) em todo output interno e na conversa; copy pro consumidor final fica sempre em inglês US, inclusive o nome da sale e o texto de banner.
2. `profile.md` (stage muda o apetite, nunca os gates) e `manifest.json` (`target_cpa` e `breakeven_roas` mais recentes prevalecem sobre a oferta, mais `budget_daily`, `stage`, `ad_classification[]`, `fixed_costs_monthly`, `esp` e `storefront.page_url`).
3. `offer-builder/dados.json` (o stack de custos, o que encolhe com o desconto e o que não encolhe), `finance-engine/dados.json`, `sourcing/dados.json`, `ad-analysis/dados.json` mais o `ad-log.md`, `scale-engine/dados.json`, `ad-strategy/dados.json`, `retention-engine/dados.json` e as rodadas anteriores em `promo-engine/`, em especial o `seasonal_vault[]`.
4. Base pelo índice (a skill cruza vários domínios e não tem domínio próprio): `python3 .claude/lib/kb-index/kb_lookup.py --skill promo-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa (as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto); o núcleo mínimo, com as queries exatas, está em `reference/gate-e-sistemas.md`; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 1 · A janela, qual data, quando começar, como se chama

Leia `reference/janela-e-calendario.md`. Pergunte numa mensagem só qual evento, o estoque disponível e quanto do budget o membro topa dedicar à janela; o resto sai dos artefatos. Comece a sale cedo: o consumidor compra do primeiro que abrir, e abrir antes captura quem já ia comprar, testa oferta e site antes do pico e gera momentum. Use as âncoras de calendário do arquivo, a regionalização por mercado, o nome que as pessoas procuram e o ângulo do mês. Grave `window` no `dados.json` e `manifest.promo`.

### ETAPA 2 · Preparação, o que precisa estar de pé antes da janela

Leia `reference/preparacao.md`. Momentum do evergreen e contraste de oferta (promoção só existe em contraste com a oferta normal); lead-gen VIP com o default de não fazer, liberado só pelos critérios do arquivo e sempre pela calculadora; estoque com a confirmação de volume por escrito da `sourcing`; backups e pior cenário pela `ops-engine`, registrando o status em `prep.ops_backups` sem virar dono do assunto; site pronto antes, com desconto automático agendado, economia visível em cada etapa e QA no celular, porque o pico é pra escalar e nunca pra otimizar site.

### ETAPA 3 · A oferta da promo

Leia `reference/oferta.md`. Percentual e valor em dinheiro são as duas melhores, disparado, e a escolha é pelo número que parece maior. Add-ons entram como camada, nunca como core; store credit e Buy X Gift X dão generosidade percebida sem furar margem. Stacking recalculado a partir do compare-at, compare-at nunca inflado, razão declarada pra sale. Progressão: a melhor oferta a janela inteira, bônus por cima no fim de semana do pico, oferta degradada de propósito na cauda. Grave `offer` no `dados.json`.

### ETAPA 4 · GATE, recálculo do breakeven com a margem promocional

Leia `reference/gate-numeros.md`. É a razão de a skill existir como dona da janela: lançar oferta melhor e continuar escalando no mesmo alvo de antes é o erro número um da temporada, mais receita e menos lucro. Recalcule com os números do membro o desconto efetivo, o AOV promocional, a margem por pedido (custos em percentual encolhem junto, custos em dinheiro não), o breakeven ROAS e o CPA da janela. Com a `finance-engine` na mesa, reaplique a fórmula dela com a margem nova; sem ela, o número é margem de contribuição e o relatório diz isso com todas as letras. Piso de margem e métrica da janela no arquivo. Saída binária: `computed` segue; qualquer número faltando vira `blocked_pending_inputs`, e as ETAPAs 5 a 8 não rodam.

### ETAPA 5 · Estrutura de campanha da janela

Leia `reference/estrutura-de-campanha.md`. Uma campanha CBO com três ad sets (Broad, WARM60 e HOT90), a única ocasião de retargeting do sistema, com o evergreen rodando em paralelo e os criativos de sale dentro da campanha de promo. Budget pela exceção do cânone (entra direto no valor planejado, sem degraus; o que protege é o surf mais o reset). Execução opcional por MCP na mesma cascade das outras skills, sempre em `PAUSED` e com a regra de fim desativada; o membro revisa e ativa. IDs no `dados.json` e linha no `ad-log.md` na mesma execução.

### ETAPA 6 · Criativos da janela, o brief pra creative-engine

Leia `reference/criativos-da-janela.md`. A doutrina é anticlimática e comprovada: o melhor ad existente com banner de oferta por cima, e foto simples do produto com a oferta. Statics superam vídeo no pico, porque o público está em modo most aware. O brief entregue em `creative_brief_08` vai na ordem de prioridade do arquivo. Escreva Black Friday Cyber Monday já nos criativos da sexta, e não desligue os ads da sexta no domingo.

### ETAPA 7 · Email e SMS da janela

Leia `reference/email-sms.md`. Esta skill é dona do calendário, das janelas de envio, das fases e da orientação de segmento; a `retention-engine` produz os assets e opera o ESP, e o flow nunca desliga durante campanha, se adapta. Grave `email_sms_calendar_13` com as fases, os segmentos e o criativo por fase seguindo awareness, confirmando os cutoffs de envio com a operação antes de prometer.

### ETAPA 8 · Escalar dentro da janela

Leia `reference/escalar-na-janela.md`, com o cânone §5 aberto ao lado. Surf scaling com a cadência por spend, a régua por período contra o KPI da ETAPA 4, a planilha por período no fuso da conta de anúncio e a ordem de decisão que começa pelo blended. Reset da meia-noite toda noite da janela, sem exceção, com o valor saindo junto de toda instrução de subida e gravado em `scaling_window.midnight_resets[]`. A curva do fim de semana e o nightcap da Cyber Monday estão no arquivo. Split test desligado no pico, caixa conferido antes, e toda mudança executada vira linha no `ad-log.md` no momento da execução.

### ETAPA 9 · Aterrissagem, fim da janela e volta pro evergreen

Leia `reference/aterrissagem.md`. Fim por horário, com a regra criada desativada pro membro ativar antes do fim, e o desconto automático morrendo junto. Depois: dip esperado com budgets descendo, cauda com a oferta degradada, campanha desligada na data-fim com o evergreen seguindo, budget realocado pelo número que o ad-log guardou e leitura reiniciando limpa, porque sazonalidade é motivo novo. Grave `landing` e `manifest.promo.active: false`.

### ETAPA 10 · Leitura pós-promo e o cofre sazonal

Leia `reference/pos-promo-e-cofre.md`. A análise datada é da `ad-analysis`, com a janela demarcada e o ad-log completo, sob duas lentes obrigatórias (CPM de temporada e winner de sorte contra winner durável, que não vira control automático). O cohort da janela vai pra `finance-engine` com nota, porque cliente de presente tem comportamento atípico. Grave em `result` o que funcionou, porque o dado da marca vence o da fonte, e alimente o `seasonal_vault[]`, que a `scale-engine` e a `content-recycler` leem.

### ETAPA 11 · Checagens de sanidade

Leia `reference/sanity-checks.md`: os doze itens, do gate computado antes de qualquer campanha ao dual output gerado. Falha em qualquer um bloqueia o salvamento do `.md`.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/promo-engine/`; `promo-engine.md` nas onze seções do arquivo, `promo-engine.html` por `python3 tools/render_report.py workspace/[produto]/promo-engine/promo-engine.md`, e `dados.json` no schema de `reference/dados-json.md` (quem lê o quê em `reference/contrato-de-leitura.md`). Rodada bloqueada no gate: os itens de campanha a aterrissagem simplesmente não aparecem. Manifest pelo script: `python3 tools/manifest.py <slug> complete promo-engine` e `set promo` com o bloco da janela, nunca `manifest.stage` e nunca por cima do `target_cpa` e do `breakeven_roas` do evergreen, mais `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft e adaptada ao stage: a da rodada completa (janela, oferta, o breakeven novo, campanha em pausa, briefs entregues, a chamada diária durante a janela), a da rodada bloqueada no gate (o que falta e o que destrava) e a de quem chega em cima da hora (a ordem de prioridade do que ainda dá tempo).
