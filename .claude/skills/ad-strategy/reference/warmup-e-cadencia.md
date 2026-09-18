# Ad Strategy · Referência: Warmup de conta nova e cadência de teste (ETAPAs 4 e 5)

> O warmup de 3 dias com o Day 4 caindo na quarta e a nota ética (ETAPA 4); os 3 dias sem mexer e as variáveis invisíveis, a cadência quarta a domingo, o checkpoint de decisão informada com as três coisas na mesa, a régua de kill de produto e a janela de decisão com o handoff para a `ad-analysis` (ETAPA 5). Abra nas ETAPAs 4 e 5.

### ETAPA 4 — Warmup de Conta Nova (se aplicável)

Conta de anúncio recém-criada precisa "esquentar" antes da campanha real — o Facebook precisa cobrar o cartão algumas vezes e ver atividade legítima antes de confiar gasto de conversão.

- **3 dias** de uma campanha simples de **engajamento (~$50/dia — ou o budget diário do membro, o que for MENOR)** ANTES da campanha de teste real.
- Objetivo só esquentar a conta — não é teste de criativo.
- **Day 4**: sobe a campanha de teste real (ETAPA 3). Comece o warmup no **domingo**, pra que o Day 4 caia na **quarta-feira**, o dia de lançamento da ETAPA 5.

**Quando pular:** se a conta já tem histórico de gasto e Purchases, não precisa de warmup — vai direto pra ETAPA 3. Detectar pelo histórico da conta (ou perguntar ao membro: "essa conta já rodou ads com venda antes?").

> **Nota ética (não grey-hat):** warmup aqui é **higiene legítima de conta nova** — qualquer anunciante sério faz. Esta skill **não** ensina account farming, compra de Business Manager, perfis-laranja, contingência pra driblar ban, nem produtos réplica. Essas táticas derrubam a conta da marca real e brigam com a tese de brand-building do Aura. Ter conta reserva é resiliência legítima; **farmar/driblar ban não é** — e a skill não encoda isso.

### ETAPA 5 — Cadência de Teste e Janela de Decisão

**Não mexer por 3 dias.** Depois de ativar, **deixar 3 dias rodando sem otimizar** (leilão e demanda variam dia a dia; mexer cedo destrói o sinal). Nada de pausar criativo, mudar budget ou trocar audiência nesse período.

> **Por que 3 dias (as variáveis invisíveis):** além da variação de leilão, todo ad é consumido sob condições que ninguém controla nem seta — o prospect vê na carona do carro ou no sofá, com som ou no mudo, depois de um ad bom ou ruim, num dia calmo ou caótico (mapa "As Variáveis de um Ad" da Skill `creative-engine`). Com poucas impressões, o resultado mede o CONTEXTO dos espectadores, não o criativo. Essas variáveis só se diluem em volume — a janela de 3 dias existe pra isso.

**Cadência de teste de PRODUTO (preview — quem decreta qualquer kill é a Skill `ad-analysis`):**
- **Lançar quarta-feira**, deixar até **domingo** (segunda/terça/quarta são dias mais fracos pra teste novo; quarta→domingo pega os dias fortes).
- **7 dias é o teto por rodada de teste** — a régua de 7 dias do cânone §3 vale por **ad set** (7 dias sem spend e sem KPI = kill do ad set), não como sentença do produto.
- **Domingo é CHECKPOINT de decisão informada, não data de execução.** No checkpoint, rodar a leitura da Skill `ad-analysis` e decidir com três coisas na mesa: **(1)** as réguas de kill do cânone §3 (conta madura: ad set 7 dias sem spend e sem KPI · conta nova: 8× target CPA sem purchase · ad novo overspendando: 24-48h); **(2)** os checks de precedência da `ad-analysis` (funil quebrado? conta suspeita? entrega travada?) — matar produto por culpa da página ou da conta é o erro caro que esses checks evitam; **(3)** o **Execution Problem**, a leitura que a `ad-analysis` aplica (rode `execution problem angle certo palavras erradas 3 strikes por angle 12 razoes de falha`): batch sem venda reprova, na maioria dos casos, a EXECUÇÃO testada — não o ângulo. Um ângulo ganha **3 tentativas (3 strikes)** antes de ser descartado, e execução ruim não mata ângulo — muito menos produto.
- **Matar o PRODUTO é decisão de outro nível:** entra na mesa só depois de **≥ 2 batches com learnings processados** (a `ad-analysis` extraiu o que cada batch ensinou e o batch seguinte aplicou a correção) OU quando as réguas do cânone §3 mandarem — **nunca por calendário sozinho**. A intenção original do marco de domingo permanece inteira: ele existe pra impedir o membro de queimar caixa por semanas num produto morto. O que muda é o mecanismo — quem declara o óbito é a leitura (`ad-analysis` + cânone), não a data. Sem venda até domingo, o caminho default é processar os learnings e iterar (Sniper nos ângulos que ainda têm strikes), com a `ad-analysis` dizendo se algum ad set ou ângulo morre já.
- Quem testa volume: ~**3 produtos/semana**.

**Janela de decisão (handoff pra Skill `ad-analysis`):**
- **Dia 1-3**: deixar rodar. Verificar só que os ads saíram do review e que a CAMPANHA está entregando (spend acontecendo). Sob CBO, **ad set sem gasto não é necessariamente erro** — pode ser o CBO escolhendo outro conceito, e isso já é informação. O que exige checar warnings (rejeição de audiência/criativo, ad em review há mais de 24h) é a campanha inteira sem gasto em 24-48h, ou um ad set inteiro travado com os ads ainda "In review". Em nenhum dos casos se otimiza nesse período.
- **A partir do Dia 3**: primeira leitura real. Rodar a Skill `ad-analysis` (`'ad analysis'`) — é ela que aplica os critérios de kill/scale por conceito (o ad set) e por criativo (o ad), com CPA mandando, não CTR, os benchmarks de funil, e a leitura de CPM como saúde da conta. **Esta skill não decide kill** — ela monta e cria; a `ad-analysis` lê e decide. A leitura por criativo apoia-se nos SISTEMAS NOMEADOS **4Pi Analysis** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) e **Lucky Wins vs Durable Wins** (rode `lucky wins vs durable wins spend concentration promote to control`) — onde o Facebook concentra gasto é o sinal de escala, mas distinguir win de sorte de win durável evita escalar ruído.

> A escala (cost-cap + surf, bid cap, budget-doubling) é assunto da **Skill `scale-engine`**, acionada só depois de um criativo validar como breakthrough (cânone §2). Não escalar manualmente durante o teste. A régua de subida e descida é o **Scaling Protocol** do cânone `.claude/lib/ad-taxonomy/README.md` §5, que a Skill `scale-engine` executa; os SISTEMAS NOMEADOS de leitura que a acompanham — **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) e **ROAS Target = Break-Even ROAS + 1 / Scaling Protocol** (rode `ROAS target break-even plus one scaling protocol 48 72 hours 20 percent`) — vivem na Skill `scale-engine` e no índice `.claude/lib/kb-index/`, não aqui. **Escala por Automated Rule de performance não entra nessa lista**: em campanha com CBO o Meta não aceita condição de performance em rule (ETAPA 6).
