---
name: ops-engine
description: Engine de continuidade e risco estrutural da operação, a skill que pergunta o que mata esse negócio nos próximos doze meses e arma a resposta antes. Três frentes, curtas e acionáveis. A primeira é a restrição do ano, identificar o único gargalo que limita os próximos doze meses (estoque, caixa, plataforma ou pessoa-chave) e organizar as prioridades em torno de removê-lo. A segunda é continuidade, um checklist de backups com status confirmado pelo membro, com conta e Business Manager reserva com campanhas pré-montadas e desligadas, processadora de pagamento redundante, banco e domínio reserva, pré-venda pronta pra ligar como válvula de estoque e caixa, e o risco de pessoa-chave medido em dores de cabeça por dólar. A terceira é o negócio como ativo, com memos de decisão, o teste de vantagem defensável do produto e a operação pronta pra auditoria de compra. É consulta lateral, não fase do pipeline, e a parte de backups vale desde o começo, porque conta nova é a mais frágil. Não monta a estrutura anti-ban, que é da setup, não calcula caixa, que é da finance-engine, e não escolhe fornecedor, que é da sourcing. Use quando o membro disser "ops", "backup de conta", "risco", "processadora", "constraint", "gargalo", "operação", "continuidade", "plano B", "conta caiu", "e se a conta for banida", "memo", "exit", "moat".
---

# Ops Engine · Lateral · apelido antigo: 19 <!-- gen:title -->

## Quando usar

Quando a pergunta é sobre a sobrevivência e a estrutura da operação, não sobre um pedido, um ad ou o modelo financeiro. Não é fase do pipeline, é consulta lateral como a `finance-engine`, com três momentos naturais: cedo, logo depois do setup e antes do primeiro ad, rodando só a ETAPA 2, porque conta nova é a mais frágil da vida do negócio e a redundância nunca é tão barata; recorrente, com revisão dos riscos por trimestre e a restrição do ano declarada uma vez por ano; e antes de decisões grandes, como escalar agressivo ou entrar no quarto trimestre, os dois momentos em que a operação quebra por trás enquanto todo mundo olha pros anúncios.

Responde qual é o gargalo que decide o ano, o que acontece amanhã se a conta, a processadora ou o fornecedor caírem, quanto do negócio depende de uma única pessoa e o que um comprador encontraria se auditasse a operação hoje. Não monta Business Manager nem registra marca (montagem é da `setup`, aqui é status e processo), não calcula caixa nem fôlego (`finance-engine`), não escolhe fornecedor nem ponto de recompra (`sourcing`), não mexe em campanha e não cobre contratação (`team-engine`) nem canal novo (`marketplace-engine`). Esses assuntos são apontados pra dona certa, nunca resolvidos aqui.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe. Sem ele, escape ES1: ofereça rodar a `setup` inline ou prosseguir em modo consulta, sem gravar nada.
2. Nenhum outro arquivo é obrigatório. A skill roda com o que houver, e quanto mais fases anteriores existirem, mais preciso fica o diagnóstico.
3. `report_language` do profile (default `pt-BR`) em tudo: todo output desta skill é interno, e não existe copy pro consumidor final aqui.

## Contexto a carregar

1. `profile.md` e `manifest.json` (o stage decide a profundidade: pra quem está começando, a ETAPA 2 é o centro e as ETAPAs 1 e 4 saem curtas; pra quem valida ou escala, as quatro rodam inteiras).
2. `finance-engine/dados.json` (o retrato de caixa que a ETAPA 1 usa; ponteiro, nunca cálculo, porque nenhum número de caixa nasce aqui), `sourcing/dados.json` (o retrato de estoque, também como ponteiro), `ad-analysis/dados.json` e `scale-engine/dados.json` (gasto real e fase de escala dimensionam o custo de um dia parado) e as rodadas anteriores em `ops-engine/`, porque o valor da revisão está em comparar com a rodada passada.
3. A regra de honestidade, em `reference/contexto.md`: status de backup é confirmação do membro, nunca dedução. Cada item é perguntado; item sem resposta fica `pending` e entra em `pending_inputs[]`. Checklist de continuidade falso é pior que nenhum, porque o membro acha que está protegido.
4. Base pelo índice (domínio `ops-scale-risk`, mais três entradas reaproveitadas de outros domínios): `python3 .claude/lib/kb-index/kb_lookup.py --skill ops-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 6 buscas adicionais por etapa (as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto); a lista completa, com as queries exatas, está em `reference/sistemas.md`; nunca query genérica nem busca repetida.

## Fluxo da skill

### ETAPA 1 · A constraint dos próximos doze meses

Leia `reference/constraint.md`. A pergunta que organiza o ano é qual é o único gargalo que, se não for removido, limita o crescimento nos próximos doze meses. Uma restrição, não uma lista: organizar o ano em torno de remover uma coisa é o que separa prioridade de vontade. Diagnostique entre os quatro tipos da tabela (estoque, caixa, plataforma e conta, pessoa-chave), cada um com o sinal que o denuncia e o que significa agir doze meses antes. O mapa do que quebra por faixa de faturamento entra como mapa do que vem, não como tarefa de agora. Saída: uma frase declarada pelo membro, a ação que remove e a data de revisão, gravadas em `constraint_12m`. Se o membro listar três, ajude a escolher uma perguntando qual delas, removida, deixa as outras duas mais fáceis.

### ETAPA 2 · Continuidade, o checklist de backups e o risco de pessoa-chave

Leia `reference/continuidade.md`. O princípio é planejar pro pior cenário e não pro melhor, e a redundância é barata perto do que evita. Monte o checklist com o membro, item a item, com status confirmado: conta e Business Manager reserva com campanhas pré-montadas e desligadas, três admins reais em cada Business Manager, página fora dele, processadora reserva testada com uma transação, banco reserva, domínio reserva, fornecedor reserva, pré-venda pronta pra ligar e atendimento dimensionado pra pico. Para quem está começando, os seis primeiros valem agora. Depois, o risco de pessoa-chave pelas três perguntas do arquivo, com a métrica de dores de cabeça por dólar, incluindo os equivalentes de marketing (um ou dois ads puxando todo o gasto, uma landing page campeã, um canal único), que aqui só se nomeiam. Saída: checklist com status mais a lista de riscos abertos, cada um com probabilidade, dano, mitigação e dono, ordenada por probabilidade vezes dano.

### ETAPA 3 · Proteção jurídica em operação

Leia `reference/protecao-juridica.md`. A divisão não muda: registrar a marca e entrar no programa de proteção de marca do Meta é montagem, e isso é da `setup`. Aqui cuida-se do que vem depois, como processo contínuo: status do registro por território (Estados Unidos primeiro, União Europeia e China assim que houver tração), o programa ativo e efetivamente usado para derrubar quem copia, a resposta a derrubada falsa enquanto o registro não sai, e a queixa direta contra concorrente que usa o nome da marca. Saída: o bloco `legal` com o status por território, o programa ativo ou não e o registro de cada ação de defesa.

### ETAPA 4 · Negócio como ativo

Leia `reference/negocio-como-ativo.md`. Três hábitos que custam disciplina e não dinheiro. Memos de decisão de uma a duas páginas antes de toda decisão que custa dinheiro relevante, nos quatro blocos do arquivo, com especificidade impiedosa e a regra de que sem memo não há reunião de decisão; memo também mata ideia, e matar ideia no papel é o descarte mais barato que existe. O teste de vantagem defensável, uma vez por rodada: se o marketing for desligado amanhã, a receita cresce ou encolhe? A resposta não gera tarefa aqui, gera a leitura honesta de onde o negócio está entre campanha e ativo, e alimenta a restrição do ano quando é ruim. E a operação pronta pra auditoria de compra, pelos cinco pontos do arquivo. Saída: o bloco `business_asset`.

### ETAPA 5 · Sanidade e veredito

Leia `reference/sanidade-e-veredito.md`: os oito itens, de uma única restrição declarada a nenhum status deduzido. Falha em qualquer um bloqueia o salvamento do `.md`. O veredito final é curto e direto: a restrição do ano em uma frase, os três riscos abertos mais graves com a mitigação de cada um, e a próxima data de revisão.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/ops-engine/`; `ops-engine.md` na ordem do arquivo, com cada risco de dano alto entrando como citação `**Risco:**`, `ops-engine.html` por `python3 tools/render_report.py workspace/[produto]/ops-engine/ops-engine.md`, `dados.json` no schema de `reference/dados-json.md` e a pasta `memos/`, criada quando o primeiro memo existir. Numa primeira rodada cedo, o doc traz só o checklist, os riscos e as pendências. Isentos de `.html`: o `dados.json` e os memos. Manifest pelo script: `python3 tools/manifest.py <slug> complete ops-engine` e `set ops` com o resumo (tipo e frase da restrição, backups prontos sobre o total, riscos altos abertos, lacunas de venda e a data), nunca `manifest.stage`, mais `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft, lembrando que o checklist e a restrição melhoram a cada revisão: uma versão pra rodada cedo, só com a continuidade, e outra pra rodada completa, com a restrição do ano, os riscos mais sérios e a próxima data de revisão.
