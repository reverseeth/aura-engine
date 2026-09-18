# Team Engine · Referência: As três portas, o gate de estágio e a resposta 'ainda não' (ETAPAs 1 e 1.5)

> A tabela que decide a porta pela pergunta do membro, o gate de estágio com a leitura por stage e a nomeação do gargalo, as referências por faixa de faturamento e a estrutura completa da resposta 'ainda não' com a exceção do editor por projeto. Abra na ETAPA 1.

A skill roda por **portas**, decididas pela pergunta do membro e pelos dados — não por interrogatório:

| Pergunta do membro | Porta | ETAPAs |
|---|---|---|
| "Devo contratar? Quem primeiro? Agência ou interno?" | **1 — Decidir** | 1-4 |
| "Preciso contratar um editor / como contrato [função]" | **2 — Contratar** | 1 + 5-8 |
| "Meu time não performa / como pago / como organizo" | **3 — Rodar** | 1 + 9-13 |

A ETAPA 1 roda SEMPRE (é o gate de estágio e a nomeação do gargalo). A ETAPA 14 (sanidade) roda sempre antes de salvar. Portas puladas não aparecem no relatório — sem seção vazia, sem explicar o que não foi feito (rule `report-only-results.md`).

### ETAPA 1 — O gate: estágio e gargalo (roda sempre)

Leia `manifest.stage` (inferência por sinais quando ausente, conforme `member-stage-awareness.md`) e responda internamente duas perguntas antes de qualquer recomendação:

**1. Este membro está no estágio em que contratar resolve?**

| Stage | Leitura | O que esta skill entrega |
|---|---|---|
| `starter` | Ainda validando oferta e primeiro criativo | **"Ainda não."** O gargalo é oferta/criativo/venda — não falta de gente. Entregar a resposta da ETAPA 1.5 e parar (a não ser que o membro queira ajuda pontual com um freelancer por projeto — aí a versão mínima da ETAPA 4 cobre). |
| `validating` | Vendas existem mas inconsistentes | Quase sempre **"ainda não"** também — com uma exceção real: **editor**. A referência da fonte é comportamental, não de vaidade: quando editar vídeo é a tarefa que mais come o tempo de quem deveria estar em oferta e ads, um editor freelancer/por projeto entra na mesa. O resto do funil desta skill continua fechado. |
| `scaling` | Breakthrough identificado, escala rodando | **Skill inteira liberada.** Aqui contratar remove gargalo de verdade — e adiar demais vira o gargalo. |

**2. Qual é o gargalo que uma contratação removeria?** Nomeie a restrição atual do negócio em uma frase, com dado: "o membro gasta X horas/semana em [tarefa]", "a máquina criativa produz N conceitos/mês e a capacidade de teste pede M", "o caixa fecha mas ninguém olha os números". A pergunta-guia da fonte: **qual é o único gargalo que limita os próximos 12 meses?** — as prioridades do ano se organizam em volta de removê-lo, não de atacar várias frentes ao mesmo tempo. Toda vaga recomendada daqui em diante referencia esse gargalo por escrito (`hiring_decision.constraint`).

**Referências por faixa (da fonte, pra calibrar a leitura — a régua canônica de stage continua sendo o manifest):**

- **US$ 0-100k/mês:** o foco é pesquisa profunda de avatar e apostas criativas maiores — não contratação. "99% dos produtos escalam até US$ 100k/mês" com UMA oferta lucrativa, UM anúncio vencedor e UM caminho de compra otimizado.
- **US$ 100-250k/mês:** matar perfeccionismo e testar oferta — time mínimo.
- **US$ 250-500k/mês:** a PRIMEIRA contratação estrutural que a fonte recomenda: **operações** (de cima pra baixo — antes de mais editores, atendimento ou gestores), junto com processos documentados e projeção de verdade.
- **US$ 500k-1M/mês:** KPIs por departamento (decisão por fatos, não sensação) e **automatizar antes de contratar**.
- **US$ 1-3M/mês:** recrutador dedicado + strategists **melhores que o próprio fundador** + AI pesada nos fluxos.
- **US$ 3M+/mês:** eliminar a dependência de pessoas únicas (key man risk) e atrair A-players de fora.

Grave `stage_check` no `dados.json`. Se a resposta é "ainda não", siga direto pra ETAPA 1.5; senão, siga pra porta que a pergunta do membro pede.

### ETAPA 1.5 — A resposta "ainda não" (starter/validating)

Não é recusa — é a entrega. Estrutura da resposta:

1. **O gargalo real, nomeado com o dado do workspace** ("suas últimas análises mostram X conceitos testados e nenhum breakthrough — o gargalo é criativo/oferta, não braço").
2. **Por que contratar agora seria a decisão errada:** contratação por necessidade é a origem do bad hire de ~15× o salário anual; e abaixo de ~US$ 1-2k/dia de gasto em ads, **o membro É o estrategista criativo** — delegar a estratégia criativa cedo demais corrói exatamente a habilidade que diferencia a marca ("nunca terceirize sua vantagem; primeiro saem as tarefas de baixo valor: atendimento, edição, design").
3. **O que fazer no lugar:** a skill que ataca o gargalo nomeado (`offer-builder` pra oferta, 08 pra criativo, 02 pra pesquisa...).
4. **O marco que reabre esta conversa:** "quando [sinal concreto — ex.: editar vídeo virar a maior fatia da sua semana com a máquina de ads validada], volta aqui que a gente monta a vaga."

Exceção pontual coberta: membro `validating` afogado em edição pode contratar **editor por projeto/freelancer** sem abrir o funil completo — bons editores custam **US$ 2,5-5k/mês** no mercado global (referência da fonte; há quem pague US$ 8k pelos melhores), e por projeto sai bem menos. Vale a regra da ETAPA 5 mesmo assim: sucesso definido antes (o que é um vídeo "pronto", quantos por semana, prazo de entrega).
