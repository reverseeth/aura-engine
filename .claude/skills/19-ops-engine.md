---
name: ops-engine
description: Engine de continuidade e risco estrutural da operação — a skill que pergunta "o que mata esse negócio nos próximos 12 meses?" e arma a resposta antes. Três frentes, curtas e acionáveis. (1) Constraint dos próximos 12 meses — identificar o ÚNICO gargalo que limita o ano (estoque, caixa, plataforma ou pessoa-chave) e organizar as prioridades em torno de removê-lo. (2) Continuidade — checklist de backups com status confirmado pelo membro: conta e Business Manager reserva com campanhas pré-montadas desligadas, processadora de pagamento redundante, banco e domínio reserva, pre-order pronto pra ligar como válvula de estoque e caixa, risco de pessoa-chave medido em "dores de cabeça por dólar". (3) Negócio como ativo — memos de decisão (WAFM), o teste de moat de produto e a operação exit-ready (o que um comprador auditaria). É consulta lateral, não fase do pipeline — e a parte de backups vale DESDE O COMEÇO, porque conta nova é a mais frágil. Não monta a estrutura anti-ban (isso é a skill 00), não calcula caixa (15) e não escolhe fornecedor (01b) — audita o status e aponta. Use quando o membro disser "backup de conta", "risco", "processor", "processadora", "constraint", "gargalo", "operação", "continuidade", "plano B", "conta caiu", "e se a conta for banida", "memo", "exit", "vender a empresa", "moat".
---

# Ops Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md` — domínio `ops-scale-risk`, 14 entradas). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica. **Esta skill é a consumidora que faltava** de 5 sistemas do domínio marcados como dormant no índice (`use_in_skill: "—"`) — a partir dela, eles são puxáveis. As 2 entradas do domínio que já transferem pra outras skills (expectativa de winning ad → 08/12; mini-memo de criativo → 08) continuam lá e NÃO são desta skill. O restante do domínio segue dormant de propósito (ver "O que esta skill NÃO faz").

## Quando Usar

Quando a pergunta é sobre a **sobrevivência e a estrutura da operação**, não sobre um pedido, um ad ou o modelo financeiro. Gatilhos: "backup de conta", "risco", "processor", "processadora", "constraint", "gargalo", "operação", "continuidade", "plano B", "e se a conta cair", "memo", "exit", "moat", "quero vender a empresa um dia".

**Não é fase do pipeline — é skill de consulta lateral, como a 15.** Três momentos naturais:

- **Cedo, logo depois do setup (00) e antes do primeiro ad:** só a ETAPA 2 (continuidade). **Conta nova é a mais frágil da vida do negócio** — sem histórico de gasto, sem Business Manager verificado, com a processadora ainda desconfiando do volume. É exatamente quando um banimento ou uma retenção de repasse dói mais, e quando a redundância é mais barata de armar. A skill 00 monta a estrutura; esta skill confirma que ela continua viva.
- **Recorrente:** revisão dos riscos abertos por trimestre; declaração da constraint 1 vez por ano (ou quando o negócio muda de patamar).
- **Antes de decisões grandes:** antes de escalar agressivo (12) e antes do Q4 — os dois momentos em que a operação quebra por trás enquanto todo mundo olha pros anúncios.

**O que esta skill responde e nenhuma outra respondia:** qual é o gargalo que decide o meu ano, o que acontece amanhã se a conta/a processadora/o fornecedor caírem, quanto do negócio depende de uma única pessoa, e o que um comprador encontraria se auditasse a operação hoje.

**O que ela NÃO faz:** não monta Business Manager nem registra marca (a montagem é da 00 — aqui é status e processo); não calcula caixa, runway nem float (15); não escolhe fornecedor nem define ponto de recompra de estoque (01b); não mexe em campanha (10/11/12); não cobre contratação e gestão de time (domínio `team-hiring-ops` do índice, sem skill consumidora hoje) nem canais novos como Amazon e TikTok Shop (domínio `affiliate-creator-channels`, idem) — quando esses assuntos aparecerem aqui, são apontados como fronteira, não resolvidos.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output desta skill é interno — relatório, checklist e memos usam esse idioma. Não existe copy consumidor-final aqui.

### Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe. Se não existir, ofereça rodar o `setup` inline (rule `emergency-escape-paths.md` ES1) ou prosseguir em modo consulta, sem gravar nada.
- [ ] Nenhum outro arquivo é obrigatório. Esta skill roda com o que houver — quanto mais fases anteriores existirem, mais preciso fica o diagnóstico.

### Contexto a carregar

1. `workspace/profile.md` + `manifest.json` — **stage** e `budget_daily` (ver `member-stage-awareness.md`). O stage decide a profundidade: pra `starter`, a ETAPA 2 é o centro e as ETAPAs 1 e 4 são curtas (a constraint vira uma pergunta, o bloco de ativo vira leitura de direção); pra `validating`/`scaling`, as quatro ETAPAs rodam inteiras.
2. `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** — `cash.runway_months`, `cash.cash_needed_90d`, `monthly_model.fixed_costs_monthly`. É o retrato de caixa que a ETAPA 1 usa pra avaliar a constraint de caixa. **Ponteiro, não cálculo:** nenhum número de caixa nasce aqui; se o membro quiser o modelo, o caminho é dizer "finanças".
3. `workspace/[produto]/sourcing/dados.json` **(se existir)** — `calendar.reorder_point_days`, `calendar.volume_confirmation_30_60_90`, fornecedor escolhido. É o retrato de estoque da constraint de estoque. **Ponteiro:** decisão de fornecedor e recompra é da 01b.
4. `workspace/[produto]/11-ad-analysis/dados.json` e `12-scale-engine/dados.json` **(se existirem)** — spend real e fase de escala, pra dimensionar o risco de plataforma (quanto maior o gasto diário, maior o custo de um dia parado).
5. Rodadas anteriores desta skill em `workspace/[produto]/19-ops-engine/` — o valor da revisão recorrente é comparar o checklist e os riscos com a rodada anterior.

### Regra de honestidade (não se negocia)

**Status de backup é confirmação do membro, nunca dedução.** A skill não tem como ver se existe Business Manager reserva, se a processadora backup está configurada ou se o registro de marca saiu. Cada item do checklist é perguntado; item sem resposta fica `pending` e entra em `pending_inputs[]`. Marcar "pronto" sem confirmação explícita torna o checklist falso — e um checklist de continuidade falso é pior que nenhum, porque o membro acha que está protegido.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. Os 5 primeiros são do domínio `ops-scale-risk`; os 3 seguintes vivem em outros domínios do índice e são reaproveitados aqui (mesmo conteúdo, recorte desta skill); os 3 últimos ainda não têm entrada no índice.

**Domínio `ops-scale-risk`:**

- **Constraint de 12 meses (o gargalo que decide o ano)** — `constraint de 12 meses qual o unico gargalo que limita o ano inteiro`
- **O que quebra entre $500k e $3M/mês** — `o que quebra entre 500 mil e 3 milhoes por mes gargalos por faixa`
- **Headaches per Dollar + key man risk** — `headaches per dollar key man risk custo escondido de cada linha de receita`
- **Registro de marca EUA-UE-China + Brand Rights Protection** — `registrar marca nos EUA Uniao Europeia e China brand rights protection defesa de marca`
- **Exits e due diligence (o que o comprador audita)** — `exit due diligence o que o comprador audita antes de comprar a marca`

**De outros domínios (recorte desta skill):**

- **Estrutura de Assets Anti-Ban (2–3 BMs + regra dos 3 admins)** — `três business managers pixel BM holding ad account BM 3 admins perfis reais` (a 00 usa pra MONTAR; aqui é o gabarito pra AUDITAR o status)
- **Trademark + Facebook Brand Rights Protection** — `trademark registrado brand rights protection fake DMCA derrubou 300 ads` (a 00 usa pro registro; aqui é o processo contínuo de defesa)
- **Product Moat > Marketing Moat (o teste de desligar o marketing)** — `se você desligar o marketing amanhã sua receita cresce ou encolhe, Snow versus Hismile, IM8 construiu antes de lançar` (a 01/04 usam na escolha de produto e oferta; aqui é a leitura de ativo)

**Sem entrada no índice ainda:**

- **Preparação operacional pro pior cenário (backups de conta, processadora, banco)** — `preparacao operacional worst case backup de BM processadora banco reserva nao financiar o caos`
- **Pre-order como válvula de estoque e caixa** — `pre-order honesto expectativa clara valvula de estoque e caixa melhor que encalhar`
- **Memos de negócio (WAFM / "no memo, no meeting")** — `no memo no meeting WAFM why what how now next memo de 1 a 2 paginas antes da reuniao`

## Fluxo da Skill

### ETAPA 1 — A constraint dos próximos 12 meses

A pergunta que organiza o ano: **"qual é o ÚNICO gargalo que, se eu não remover, limita o crescimento nos próximos 12 meses?"** Uma constraint, não uma lista — organizar o ano em torno de remover UMA coisa é o que separa prioridade de vontade. O padrão de quem escala é o arrependimento invertido: quase todo operador grande consegue nomear o gargalo que gostaria de ter resolvido um ano antes.

Diagnostique com o membro entre os quatro tipos (a maioria dos negócios de ecommerce cai num deles):

| Tipo | Sinal de que é ela | Agir 12 meses antes significa |
|---|---|---|
| **Estoque** | Venda limitada pelo que há no armazém; ruptura em campanha; prazo de produção maior que o ciclo de venda | Negociar prazo de pagamento e pré-produção com o fornecedor ANTES de multiplicar o volume (a cada pedido, reduzir a entrada e esticar o prazo) e **deixar o pre-order pronto antes de precisar**. Caso real da fonte: marca foi de $10k pra $100k/dia em menos de um mês, estourou o estoque, e o pânico de "não perder venda" virou onda de chargebacks que derrubou o Business Manager. O detalhe operacional (ponto de recompra, fornecedor) é da 01b — aqui só se declara a constraint e a ação. |
| **Caixa** | O modelo diz "dá pra escalar" e o banco diz que não; runway curto; cada rodada de estoque consome o fôlego | Rodar a skill 15 (se ainda não rodou) e tratar o número dela — runway, caixa pra 90 dias — como a régua da constraint. Nenhuma conta de caixa nasce aqui. |
| **Plataforma / conta** | Operação inteira dentro de 1 Business Manager, 1 processadora, 1 canal; um banimento = receita zero | A ETAPA 2 inteira. É a constraint mais barata de remover e a mais cara de ignorar. |
| **Pessoa-chave** | O negócio para se UMA pessoa (inclusive o membro) parar uma semana | Documentar o processo (transformar o que só existe na cabeça em SOP — processo escrito passo a passo), treinar uma segunda pessoa, e medir "dores de cabeça por dólar" (ETAPA 2). |

**O mapa do que quebra por faixa de faturamento** (puxe o sistema — apresente como mapa do que VEM, não como tarefa de agora): na subida, primeiro quebram os fundamentos de pesquisa e oferta; depois a organização (processos, previsão de demanda, registro de marca por país); na faixa de $500k–1M/mês quebram os dados (números confiáveis, ancorados no demonstrativo de resultado, e cada métrica do funil com dono e linha de base — quando algo sai da base, achar a causa ANTES de concluir "precisamos de mais ads"); acima disso, o gargalo vira produto, pessoa-chave e comunidade. Pra membro `starter`/`validating`, o valor do mapa é saber o que NÃO é a constraint dele ainda.

**Saída da ETAPA:** uma frase declarada pelo membro — tipo, enunciado específico ("a constraint do ano é X porque Y"), a ação que remove, e a data de revisão. Grave em `constraint_12m`. Se o membro listar três, ajude a escolher UMA pela pergunta: "removida qual delas, as outras duas ficam mais fáceis?"

### ETAPA 2 — Continuidade: o checklist de backups e o risco de pessoa-chave

O princípio da fonte primária (P1): planejar pro PIOR cenário, não pro melhor — conta banida, processadora segurando repasse, fábrica sem capacidade, atendimento afogado. Redundância é barata perto do que ela evita, e **"você não pode financiar o caos"**: dívida e float não consertam operação quebrada (a régua de caixa disso é da 15).

Monte o checklist COM o membro, item a item, cada um com status confirmado (`ready` / `in_progress` / `missing` / `not_applicable`):

| # | Item | O que "pronto" significa |
|---|---|---|
| 1 | **Business Manager + conta de anúncio reserva** | Estrutura da 00 viva (pixel isolado num BM próprio, conta de anúncio em outro) E uma conta reserva aquecida com **campanhas pré-montadas e desligadas** — se a conta principal cair no meio da escala, liga-se a reserva no mesmo dia, sem recomeçar do zero. |
| 2 | **3 admins reais em cada BM** | Os mesmos 3 perfis reais (o membro + família/amigos de confiança) em todos os BMs. Nunca perfil comprado. Um admin banido não pode significar perder o acesso a tudo. |
| 3 | **Página fora do BM** | Página criada no perfil pessoal, não dentro do BM (sobrevive a banimento de BM). |
| 4 | **Processadora de pagamento reserva** | Uma segunda processadora (ex.: Stripe ou Airwallex no básico) já configurada e testada com uma transação — não "sei que existe". E o membro sabe o que a processadora principal olha pra segurar repasse (redes sociais da marca, termos de serviço, taxa de chargeback): retenção de repasse acontece MESMO com chargeback baixo, e o risco real de recorrência mal sinalizada não é o reembolso, é perder a processadora. |
| 5 | **Banco reserva** | Segunda conta bancária aberta (ex.: um segundo banco digital) — bloqueio de conta bancária não pode parar folha e fornecedor. |
| 6 | **Domínio reserva** | Um segundo domínio registrado e apontável em horas. Caso real da fonte: uma restrição de política derrubou TODAS as campanhas de um domínio, inclusive de produtos sem relação com a infração — domínio/subdomínio separado isola esse risco. |
| 7 | **Fornecedor reserva** | Identificado e com contato feito (pra suplemento/skincare, um nos EUA além da China). A escolha e a negociação são da 01b — aqui só o status. |
| 8 | **Pre-order pronto pra ligar** | Widget/configuração de pre-order testada na loja + texto de expectativa de prazo escrito. É a válvula dupla: segura a venda quando o estoque acaba (sem pânico → sem chargeback → sem derrubar a conta) e adianta caixa (o dinheiro entra antes de produzir). Com expectativa clara, a conversão quase não cai — caso real da fonte: um novembro de $2,4M vendido em pre-order, mais que o ano anterior inteiro. **Melhor subestimar o estoque e ir pra pre-order do que encalhar.** |
| 9 | **Atendimento dimensionado pra pico** | O atendimento aguenta 3–10x o volume de tickets de um pico (Q4, escala, viral)? Se não: treinar, ou contratar temporário antes do pico. |

Pra membro `starter`, os itens 1–6 são os que valem AGORA (custam quase nada e protegem o que ele tem); 7–9 entram quando houver estoque próprio e volume.

**Risco de pessoa-chave e "dores de cabeça por dólar".** Três perguntas, respondidas com honestidade:

1. Se você adoecer uma semana, a marca degringola?
2. Se a pessoa mais treinada do time sair amanhã, o que quebra?
3. Linha de receita por linha de receita: quantas dores de cabeça por dólar ganho ela gera?

A métrica "dores de cabeça por dólar" existe porque receita cresce junto com problema — o jogo é crescer o dinheiro sem crescer o caos, e linha de receita que fatura bem mas consome o fundador é constraint disfarçada. Quanto mais o membro segura tudo, mais ELE é a pessoa-chave em risco. E o risco tem equivalentes de marketing que entram no mesmo diagnóstico: **1–2 ads puxando todo o gasto, 1 landing page campeã, 1 canal único** — concentração é fragilidade estrutural onde quer que apareça (a resposta de criativo/funil é das skills 08/10/14; aqui só se nomeia o risco). Regra prática pra fechar: todo problema recorrente ganha um conserto definitivo (patch), não um apagão de incêndio repetido.

**Saída da ETAPA:** checklist com status + lista de riscos abertos, cada um com probabilidade (baixa/média/alta), dano se acontecer (baixo/médio/alto), mitigação e dono. Ordene por probabilidade × dano.

### ETAPA 3 — Proteção jurídica em operação (processo, não setup)

**A divisão é explícita e não muda:** o SETUP é da skill 00 (ETAPA 5C) — registrar a marca e entrar no Brand Rights Protection do Meta (o programa que vincula o registro à marca) acontecem na montagem da operação. Esta ETAPA cuida do que vem DEPOIS: manter e usar essa proteção como processo contínuo.

O processo, revisado a cada rodada:

1. **Status do registro por território.** EUA primeiro; **União Europeia e China assim que houver tração** — custa poucas centenas de dólares e o custo de adiar é real (caso da fonte: marca registrada por terceiros na primeira semana do lançamento; recuperar depois é caro ou impossível). Grave o status dos três territórios.
2. **Brand Rights Protection ativo e USADO.** Com o programa ativo, o efeito é duplo: derrubadas falsas contra os seus ads ficam muito mais difíceis, e VOCÊ passa a derrubar quem copia seus criativos e usa sua marca — o Meta bane por você. Rip de criativo e clone de loja deixam de ser "faz parte" e viram fila de denúncia.
3. **Resposta a derrubada falsa.** Caso real da fonte: uma queixa falsa de direitos autorais (DMCA — o mecanismo legal de derrubar conteúdo por copyright) tirou do ar 300 ads de uma vez, incluindo os vencedores, numa conta de $200k/dia. Enquanto o registro e o programa não saem, a única defesa é o item 1 do checklist da ETAPA 2 (conta reserva pronta). Não existe proteção completa sem o programa.
4. **Competidor usando o nome da sua marca** em ads ou funil → queixa DMCA direta, o membro mesmo, sem advogado.

**Saída da ETAPA:** bloco `legal` no dados.json — status por território, programa ativo ou não, e o registro de cada ação de defesa (data, alvo, resultado).

### ETAPA 4 — Negócio como ativo

Três hábitos que transformam uma operação que fatura numa empresa que vale — e que custam disciplina, não dinheiro.

**1. Memos de decisão (formato WAFM).** Toda decisão que custa dinheiro relevante — trocar de fornecedor, entrar num canal, contratar, mudar preço, montar time — vira um memo de 1 a 2 páginas ANTES de ser tomada. Quatro blocos: **Por quê** (a dor ou oportunidade agora, com número: "a receita caiu de US$ 127k pra US$ 98k em 30 dias, −23%" serve; "as vendas caíram" não serve), **O quê** (a definição precisa da decisão), **Como** (mecânica, recursos, prazo, obstáculos) e **Agora/Depois** (ações com dono e data). Regras: sem memo, não há reunião de decisão; especificidade impiedosa; escrever expõe a ideia rasa — **memo também mata ideia, e matar ideia no papel é o descarte mais barato que existe**. O hábito conversa com o que já existe no framework: a 15 fecha decisões financeiras com memo de decisão e a 08 usa mini-memo de criativo; aqui o formato vira rotina pra QUALQUER decisão de operação. Memos escritos com a Aura são salvos em `workspace/[produto]/19-ops-engine/memos/AAAA-MM-DD-<assunto>.md`.

**2. O teste de moat (vantagem defensável) do produto.** A pergunta, feita uma vez por rodada: **"se você desligar o marketing amanhã, sua receita cresce ou encolhe?"** Marca de verdade cresce mesmo sem tráfego pago (indicação, recompra, comunidade); operação que zera sem ads é uma campanha bem-sucedida, não um ativo. Habilidade de marketing está virando commodity (AI, saturação de ângulo acelerando) — o que sobrevive é o que não se copia em um dia: produto e fórmula próprios, categoria criada ou redefinida, comunidade real, indicação espontânea como motor. Produto que qualquer um pode dropshippar é fila de espera pra concorrência. A resposta do teste não gera tarefa aqui (a escolha de produto é da 01, a oferta é da 04) — ela gera a leitura honesta de onde o negócio está no espectro "campanha → ativo" e alimenta a constraint do ano quando a resposta for ruim.

**3. Operação exit-ready (pronta pra auditoria de compra).** Manter o negócio vendável é disciplina que paga mesmo sem intenção de vender — tudo que um comprador audita numa due diligence (a auditoria antes de comprar a empresa) é sinal de saúde AGORA:

- **Números confiáveis, ancorados no demonstrativo de resultado** — transações categorizadas, sem "acho que a margem é X" (a camada contábil é a da 15; aqui é o status).
- **Receita que sobrevive sem o fundador** — sem pessoa-chave insubstituível (ETAPA 2), processos documentados.
- **Valor de cliente comprovado** — base de recompra/assinatura real; comprador sofisticado paga mais por LTV comprovado + risco baixo ("desligo os ads e o negócio ainda lucra?").
- **Stack limpo** — quanto mais a operação vive dentro do padrão (Shopify, apps conhecidos), mais fácil a auditoria; ferramenta exótica de checkout pode converter mais E sujar o pacote na venda — é trade-off consciente, não regra.
- **Papel em dia** — registro de marca, contratos com fornecedor, autorização de uso de imagem de creators.

**Saída da ETAPA:** bloco `business_asset` — resposta do teste de moat em uma frase, lacunas de exit-readiness (o que um comprador apontaria hoje) e se o hábito de memo está de pé.

### ETAPA 5 — Sanidade e veredito

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. **Uma** constraint declarada — não uma lista de quatro.
2. Nenhum item do checklist marcado `ready` sem confirmação explícita do membro nesta conversa (ou em rodada anterior gravada no dados.json).
3. Nenhum status deduzido ou inventado; todo item sem resposta está `pending` e em `pending_inputs[]`.
4. Nenhum número de caixa calculado aqui — onde caixa aparece, é leitura da 15 ou ponteiro pra ela.
5. Nenhuma decisão de fornecedor/estoque tomada aqui — onde estoque aparece, é ponteiro pra 01b.
6. Nenhuma instrução de MONTAR estrutura (BM, registro de marca) — montagem é da 00; aqui é status, processo e uso.
7. O relatório contém só o resultado (rule `report-only-results.md`) — sem narração de processo, sem descrição do que não foi feito.
8. `dados.json` validado e manifest atualizado.

O veredito final é curto e em linguagem direta: a constraint do ano em uma frase, os 3 riscos abertos mais graves com a mitigação de cada um, e a próxima data de revisão.

## Output Schema — `19-ops-engine/ops-engine.md` + `19-ops-engine/dados.json`

O markdown é humano; o JSON é o registro que as rodadas futuras desta skill comparam.

```json
{
  "ops_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "stage_at_run": "starter | validating | scaling",
  "constraint_12m": {
    "type": "estoque | caixa | plataforma | pessoa_chave | outro",
    "statement": "frase declarada pelo membro",
    "why_now": "o sinal que aponta pra ela",
    "action_before": "a ação que remove, com prazo",
    "declared_at": "2026-09-01",
    "review_date": "2027-09-01"
  },
  "backups_checklist": [
    { "item": "bm_conta_reserva", "status": "ready | in_progress | missing | not_applicable | pending", "note": "" },
    { "item": "tres_admins_reais", "status": "pending", "note": "" },
    { "item": "pagina_fora_do_bm", "status": "pending", "note": "" },
    { "item": "processadora_reserva", "status": "pending", "note": "" },
    { "item": "banco_reserva", "status": "pending", "note": "" },
    { "item": "dominio_reserva", "status": "pending", "note": "" },
    { "item": "fornecedor_reserva", "status": "pending", "note": "ver sourcing/dados.json" },
    { "item": "preorder_pronto", "status": "pending", "note": "" },
    { "item": "cs_dimensionado_pico", "status": "pending", "note": "" }
  ],
  "key_man": {
    "founder_one_week_out": "degringola | segura | nao_sei",
    "single_person_dependencies": [],
    "marketing_concentration": { "top_ad_spend_share": null, "single_landing_page": null, "single_channel": null },
    "headaches_per_dollar_worst_line": null
  },
  "legal": {
    "trademark_us": "registered | filed | missing | pending",
    "trademark_eu": "pending",
    "trademark_cn": "pending",
    "brp_active": null,
    "enforcement_log": [
      { "date": "", "action": "takedown_violador | resposta_dmca_falso | dmca_contra_competidor", "target": "", "result": "" }
    ]
  },
  "business_asset": {
    "moat_test_answer": "cresce | encolhe | nao_sei",
    "moat_note": "1 frase",
    "memo_habit_active": null,
    "memos_written": [],
    "exit_ready_gaps": []
  },
  "open_risks": [
    { "risk": "", "likelihood": "baixa | media | alta", "impact": "baixo | medio | alto", "mitigation": "", "owner": "membro | aura | terceiro", "opened_at": "", "closed_at": null }
  ],
  "pending_inputs": [],
  "previous_run_diff": { "items_resolved": [], "items_new": [] },
  "handoff": { "note": "nenhuma skill consome este arquivo hoje; a leitura é das rodadas futuras desta skill e do membro" }
}
```

**Campos que a skill NUNCA preenche por dedução:** todos os `status` do checklist, `legal.*` e `key_man.founder_one_week_out`. Sem resposta do membro → `pending` + `pending_inputs[]`.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `ops-engine.md` → `ops-engine.html`). **Isentos** (arquivos operacionais — rule 6b): `dados.json` e os memos em `memos/`. Use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, **logo SVG na topbar copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**, componentes aura; o card `danger` é o lugar natural dos riscos abertos de dano alto).

**Garantir diretório:** `mkdir -p workspace/[produto]/19-ops-engine/` antes de salvar.

Outputs em `workspace/[produto]/19-ops-engine/`:

- **`ops-engine.md`** contendo, nesta ordem: a constraint do ano (ETAPA 1) · checklist de continuidade com status e riscos abertos ranqueados (ETAPA 2) · status e processo de proteção de marca (ETAPA 3) · negócio como ativo — teste de moat, lacunas de exit e hábito de memo (ETAPA 4) · veredito e data de revisão (ETAPA 5) · pendências (o que falta e o que destrava, sem narrar tentativas). Numa primeira rodada cedo (só ETAPA 2), o doc contém só o checklist, os riscos e as pendências.
- **`ops-engine.html`** — companion.
- **`dados.json`** — schema acima.
- **`memos/`** — criada quando o primeiro memo existir.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:

- Adicionar `19-ops-engine` em `skills_completed`
- Gravar `manifest.ops` = `{ constraint_type, constraint_statement, backups_ready, backups_total, open_risks_high, exit_ready_gaps, checked_at }` — o resumo de leitura rápida
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenerar o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>`

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`). O checklist e a constraint melhoram a cada revisão — diga isso.

**Rodada cedo (só continuidade):**
"Checklist de continuidade montado: **[N] de [M] itens prontos**. Os que faltam, em ordem do que protege mais por menos esforço: [top 3 com 1 linha cada]. Conta nova é o momento mais frágil da operação — é agora que essa redundância custa pouco e vale muito. Me confirma os status que ficaram pendentes e eu fecho o quadro. Quando o negócio estiver rodando, roda **'operação'** de novo que a gente declara a constraint do ano e olha o resto."

**Rodada completa:**
"Diagnóstico de operação fechado. **A constraint do seu ano é [tipo]: [frase]** — e a ação que remove é [ação], até [prazo]. No checklist de continuidade, **[N] de [M] prontos**; os riscos abertos mais sérios são [top 3, cada um com a mitigação em meia linha]. [Se moat_test = encolhe: 'No teste de desligar o marketing, hoje a receita encolhe — o caminho pra virar ativo passa por [lacuna principal], e isso alimenta a constraint que você declarou.'] Revisa comigo o que não bate. Marquei a próxima revisão pra [data] — riscos por trimestre, constraint uma vez por ano."
