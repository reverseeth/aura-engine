# Sourcing · Referência: Calendário, Ano Novo Chinês e prevenção de ruptura de estoque (ETAPA 12)

> Os seis sistemas a puxar, a hierarquia dos problemas, a cronologia real do feriado, o que fazer na ordem, a armadilha do quarto trimestre pesado e a confirmação de volume em 30, 60 e 90 dias que a `scale-engine` exige. Abra na ETAPA 12.

### ETAPA 12 — Calendário: Ano Novo Chinês e prevenção de ruptura de estoque

**Puxe antes desta etapa:**
- **Chinese New Year Playbook** (rode `Chinese New Year playbook cronologia shutdown pedidos até dezembro embarques 8-10 fev`)
- **Hybrid Shipping + Inventory Roll-Forward** (rode `hybrid shipping air freight só para o buffer de 10 dias inventory roll-forward CNY`)
- **Integrated Q1+Q2 Planning** (rode `planejamento Q1 Q2 armadilha Q4-heavy front-load SKUs janelas de negociação janeiro março`)
- **Post-CNY Re-Audit** (rode `pós-CNY re-auditar fábrica trocou sub-vendors quality manager corrective action plan`)
- **Gift-Giving & CNY Ritual Calendar** (rode `gift giving fornecedor pagar saldos antes do Chinese New Year annual party VIP customer`)
- **Supply Chain Threat Hierarchy** (rode `hierarquia de problemas supply chain stockout desligar ads defect rate inventário`)

**12.1 — A hierarquia dos problemas (define a prioridade de tudo):**

1. **Ruptura de estoque é o pior.** Pedido sem produto derruba a operação: o prazo explode e o caminho passa a ser **desligar os anúncios** — e reotimizar a campanha do zero depois é caríssimo. O antídoto é planejamento de compra que cruza a venda atual + o estoque do dia + os prazos, pra prever a data em que o estoque acaba e a data em que a recompra precisa ser feita.
2. **Taxa de defeito vem em segundo** (ETAPA 10).
3. **Estoque encalhado em terceiro** — e defeito vira encalhe. Prazo de pagamento negociado (ETAPA 8) é o que evita capital preso.

**12.2 — O Ano Novo Chinês, com a cronologia real.** É a maior migração humana do mundo: o feriado oficial cai em fevereiro, mas o país para bem antes e demora muito a voltar.

| Momento | O que acontece |
|---|---|
| Até o fim de dezembro | Prazo real pra colocar o pedido que precisa sair antes do feriado |
| Meados de janeiro | **Os fornecedores de matéria-prima fecham ANTES das montadoras** (aço e algodão param por volta do dia 15) |
| Semanas antes do feriado | Os trabalhadores começam a ir embora; as cidades industriais esvaziam |
| Cerca de 8 a 10 de fevereiro | Últimos embarques saem |
| Semana final | Nada acontece; os 3PLs chineses fecham por cerca de uma semana |
| Fim de fevereiro / início de março | Volta oficial, com cerca de metade da capacidade |
| **Meados de março** | **Capacidade normal** — parte dos trabalhadores não volta (muitos trocam de emprego no reinício do ano) e a fábrica precisa recontratar e retreinar |

**O que fazer, na ordem:**
- **Pergunte a cada fornecedor** (a resposta muda de fábrica pra fábrica; não existe resposta única): "qual o prazo da matéria-prima antes e depois do feriado, e quanto eu preciso comprar ou depositar AGORA pra operar liso na volta?" e "qual o calendário de parada de vocês?". **Documente por fábrica.**
- **Emita os pedidos de compra antes do feriado.** Se o gatilho de compra de material da fábrica é o seu pedido formal, previsão sem pedido não compra matéria-prima nenhuma.
- **Embarque parcial**: se a ordem não sai inteira, negocie sair em partes; identifique o item que está travando tudo (costuma ser a embalagem) e pressione ou incentive aquele fornecedor específico.
- **Logística com antecedência**: reserve contêiner com semanas de antecedência (já houve produção heroica concluída e navio só duas semanas depois). Perto do feriado, sobretaxas dobram ou triplicam, e contêiner "rola" pra semana seguinte por congestionamento.
- **Embarque híbrido pra cobrir o período sem produção**: calcule estoque atual + em trânsito + em produção contra a velocidade de venda, e projete quantos dias de suprimento você tem durante o período. Use frete aéreo APENAS pro buffer da semana a 10 dias em que o 3PL chinês está fechado, e marítimo pro resto. Decida pela economia do produto: produto pesado com frete aéreo caro pode não fechar. **Vender no empate pra NÃO desligar os anúncios costuma valer a pena** — o custo de reotimizar a campanha é maior.
- **Use a parada a favor**: o primeiro trimestre é a época oficial de desenvolvimento de produto. Feche o depósito do molde ANTES do feriado e pré-encomende o aço (a compra do aço come os primeiros 7 a 10 dias dos cerca de 30 do molde), pra o molde ser cortado assim que voltarem. Os engenheiros ficam ociosos nesse período e o design avança mais rápido que em qualquer outra época do ano.
- **Pague todo saldo pendente antes do feriado** — é a época de bônus da equipe da fábrica, e isso pesa muito na prioridade que você recebe antes e depois. Presença nas festas anuais (ou um presente do seu país, que vale mais que coisa cara) compra prioridade real.
- **Microgerencie**: se existe uma hora pra perguntar todo dia se está no prazo, é essa.
- **Depois da volta, re-audite**: pergunte se trocaram fornecedor de componente, gerente de qualidade ou pessoal de linha, e peça inspeção. Muita coisa muda de mãos no reinício do ano.

**12.3 — A armadilha do quarto trimestre pesado.** Vendeu muito no fim do ano, relaxou no primeiro trimestre, teve ruptura de estoque, passou o primeiro e o segundo trimestres correndo atrás e chegou no terceiro sem ter preparado o quarto. É um ciclo vicioso, e ele começa exatamente aqui. Mesmo produzindo fora da China (Vietnã, Malásia), componentes e engenheiros frequentemente vêm de lá — o feriado te afeta igual.

**12.4 — Confirmação de volume (o que a Skill `scale-engine` vai cobrar).** Antes de fechar esta skill, obtenha do fornecedor escolhido, **por escrito**, se ele consegue entregar o volume projetado em 30, 60 e 90 dias, e o ponto de recompra (a partir de quantos dias de estoque restante o pedido precisa ser colocado, considerando o prazo dele). Grave em `calendar.volume_confirmation_30_60_90` e `calendar.reorder_point_days`. A Skill `scale-engine` exige essa confirmação no pré-flight de escala, e sem ela a escala roda no escuro: **perto do ponto de recompra, faça o pedido, acompanhe o rastreio e NÃO escale os anúncios agressivamente** — vai bater na ruptura.
