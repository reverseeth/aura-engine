---
name: team-engine
description: Engine de time da marca — decide QUANDO contratar (pela restrição real do negócio, nunca por desespero), COMO contratar (scorecard antes da vaga, funil de 9 etapas, teste prático cronometrado, headhunting) e COMO rodar o time depois (onboarding de 8 semanas, KPIs por função com hit rate por editor, reviews com 9-box e PIP, incentivos tipo Gravy, org design em engines e pods, frameworks de decisão DAI/RAPID/AAR). Skill de consulta lateral pensada pro membro em estágio scaling; pra quem está em starter/validating a resposta certa costuma ser "ainda não — sua restrição hoje é X", e esta skill entrega exatamente essa resposta com o porquê. Lê o stage do manifest, aponta pra 15 (finance) quando a pergunta é "a folha cabe no caixa?" e separa funcionário de creator (creator é território da 16). Nunca recomenda vaga sem nomear o gargalo que ela remove; nunca estima salário do membro nem diz que a folha cabe sem os números na mesa. Use quando o membro disser "contratar", "time", "equipe", "editor", "hiring", "org", "quem contratar", "delegar", "quem eu contrato primeiro", "meu time não performa", "preciso de um editor".
---

# Team Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md` — domínio `team-hiring-ops`, 62 sistemas). Esta skill é a **consumidora que faltava** do maior bloco órfão da base: até ela existir, 54 dos 62 sistemas estavam marcados como dormant (`use_in_skill: "—"`) e só 8 tinham leitor (08/09/11/12). A partir dela, o domínio inteiro é puxável. Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> Além do domínio próprio, esta skill consome **6 entradas vizinhas** — 4 do domínio `ops-scale-risk` (a decisão por gargalo e o papel do fundador) e 2 do domínio `scaling` (o foco e o tamanho de time por faixa de faturamento, já lidas pela 08/12 — conteúdo compartilhado, reuse o resultado se já foi puxado na sessão).
>
> **Réguas compartilhadas que esta skill respeita:** `member-stage-awareness.md` (o stage do manifest decide a apresentação) e o cânone `.claude/lib/unit-economics/README.md` §1 via skill 15 — folha de pagamento é **custo fixo**, e custo fixo nunca se estima: quando a pergunta for "cabe no caixa?", o número vem da 15 ou do membro, nunca de chute desta skill.

## Quando Usar

Quando a pergunta é sobre **gente**: contratar, delegar, montar estrutura, medir, pagar, promover ou desligar. Gatilhos: "contratar", "time", "equipe", "editor", "hiring", "org", "quem contratar", "delegar", "preciso de um editor", "quero sair do operacional", "meu time não entrega", "quanto pagar", "como demitir".

**Não é fase do pipeline — é skill de consulta lateral, como a 15.** Três momentos naturais:

- **Quando o membro vira o gargalo:** faturamento subiu, o dia acabou e ele ainda edita vídeo, sobe ad e responde cliente. A pergunta real é "o que sai da minha mão primeiro?".
- **Quando existe vaga pra abrir:** "preciso de um editor / media buyer / strategist" — a skill monta o gabarito da vaga, o anúncio e o funil inteiro.
- **Quando o time já existe e não performa:** expectativa mal definida, KPI que ninguém acompanha, promoção e demissão no feeling. A skill instala o ciclo de gestão.

**Pra quem esta skill foi desenhada:** o membro em **`scaling`** — é nesse estágio que contratar resolve gargalo de verdade. Pra membro em `starter` ou `validating`, a resposta mais valiosa que esta skill entrega costuma ser **"ainda não"** com o motivo (ETAPA 1) — o material de referência é explícito: marca de ecommerce enxuta escala a US$ 1M+/mês com time mínimo, e a resposta raramente é "mais gente"; é "gente melhor" (muitas vezes: você, melhor).

**O que ela NÃO faz:** não recruta creator de conteúdo nem monta programa de afiliado — **creator não é funcionário**; contratação de creators, seeding, bounty com gente de fora da empresa e programa de embaixador são território da **skill 16 (creator-engine)**. Também não calcula o modelo financeiro — quando a conversa vira "quanto de folha o negócio aguenta", esta skill lê o que a 15 publicou e aponta pra ela, sem refazer a conta.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Exceção deliberada:** artefatos que o CANDIDATO vai ler (anúncio de vaga, mensagem de abordagem, roteiro do teste prático) saem no idioma do mercado onde o membro contrata — pra contratação remota global/EUA o padrão é inglês; se o membro contrata no Brasil, português. Pergunte uma vez e grave em `dados.json.hiring_language`.

### Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe — fonte do `stage`, `budget_daily` e `fixed_costs_monthly`
- [ ] `workspace/profile.md` existe — stage declarado e contexto do membro

Se o manifest faltar ou não parsear, não aborte seco (rule `emergency-escape-paths.md` ES2): ofereça **(A)** rodar a skill 00 (setup), **OU (B)** prosseguir perguntando direto ao membro faturamento mensal aproximado, gasto em ads e estágio, marcando `manifest.skipped_preflight += ["manifest.json"]` quando o manifest voltar a existir. Esta skill não tem pré-requisito de outra fase — time é conversa que pode acontecer a qualquer altura.

### Contexto a carregar

1. `workspace/[produto]/manifest.json` — **`stage`** (campo canônico, `member-stage-awareness.md`), `budget_daily`, `fixed_costs_monthly` (se existir), `manifest.finance` (resumo gravado pela 15, se existir)
2. `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** — `monthly_model.fixed_costs_monthly`, `monthly_model.operating_income`, `monthly_model.contribution_margin`, `cash.runway_months`. É a fonte da resposta "a folha cabe?" (ETAPA 8)
3. `workspace/[produto]/11-ad-analysis/dados.json` **(se existir)** — volume de criativos rodados e classificação; é o dado real por trás de "quantos conceitos/mês a máquina atual produz"
4. `workspace/[produto]/12-scale-engine/dados.json` **(se existir)** — fase de escala; escala agressiva com key man risk alto é risco que esta skill nomeia
5. Rodadas anteriores desta skill em `workspace/[produto]/18-team-engine/` — org, vagas e pipeline de candidatos são artefatos vivos: continue de onde parou, não recomece

### As cinco regras que não se negociam

1. **Contrata-se porque QUER, nunca porque PRECISA.** A regra nº 1 da fonte primária: contratação por desespero ("assinei cliente, preciso de editor pra ontem") é a origem do bad hire — e o custo real de um bad hire é **~15× o salário anual** do cargo (treinamento, onboarding, softwares, dano a clientes e marca, saída de outros membros e reinício do funil: um erro de US$ 100k/ano pode custar US$ 1,5M no acumulado). Se o processo apontou red flag e o membro está aliviado em vez de empolgado, a recomendação desta skill é NÃO contratar — mesmo com a vaga urgente.

2. **Nenhuma vaga sem gargalo nomeado.** Toda recomendação de contratação desta skill sai com a frase "esta vaga remove o gargalo X" preenchida com o gargalo real (ETAPA 1). Vaga que não remove gargalo é custo fixo novo sem retorno — e custo fixo é exatamente o que a 15 mostra que mata operação em escala.

3. **Sucesso definido ANTES da vaga aberta.** O motivo nº 1 de contratação falhar são expectativas que o CONTRATANTE falhou em definir. Nenhum anúncio vai ao ar sem o gabarito da vaga (scorecard) pronto: missão, funções nucleares e o par de indicadores-alvo (ETAPA 5). Sem isso, o editor que entrega 10 vídeos/semana "acha que está arrasando" enquanto o membro pensa em demiti-lo — desconexão criada pelo membro, não pelo contratado.

4. **Três números nunca se inventam.** (a) **Salário/custo do time do membro** — benchmark do material de referência é referência, o número real é do membro; (b) **caixa e custo fixo** — vêm da 15 ou do membro (cânone: nunca estimar); (c) **KPI real de uma pessoa** — vem de tracking (planilha, ferramenta de gestão, relatório de ads), nunca de impressão. Faltando qualquer um: campo `null`, entra em `pending_inputs[]`, e o bloco dependente fica marcado como não calculável.

5. **Creator ≠ funcionário.** Quem produz conteúdo de fora (creator, afiliado, embaixador) não entra no org chart, não ganha scorecard de funcionário e não passa pelo funil desta skill — o caminho é a **skill 16 (creator-engine)**. O que ESTA skill cobre é o time interno e contractors fixos: editor, media buyer, strategist, designer, operações, atendimento. A fronteira aparece na prática no bounty: prêmio por performance pago a **editor do time** é incentivo desta skill; bounty aberto pra **creators externos** é programa da 16.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. O domínio principal é `team-hiring-ops` no `.claude/lib/kb-index/` — **abra a seção inteira do domínio e enumere todas as entradas antes de filtrar por ETAPA** (contrato de cobertura do índice). As queries abaixo são o núcleo mínimo garantido de cada porta, nunca o teto. Não repita busca de sistema já puxado na mesma sessão; entradas duplicadas entre domínios apontam pro mesmo conteúdo.

**PORTA 1 — Decidir (ETAPAs 1-4):**

- **Buyback Rate + 4 zonas de delegação** — `buyback rate taxa horaria delegar 4 zonas de delegacao tarefas de menor valor`
- **Want > Need Hiring Rule (bad hire = 15× o salário anual)** — `contratar por querer nao por precisar bad hire custa 15x o salario anual`
- **4 tipos de role + benchmarks de time-to-hire** — `quatro tipos de role benchmarks de time to hire por tipo de vaga`
- **Potential vs Skill Hiring** — `contratar por potencial versus por skill quando cada um faz sentido`
- **Top-Down vs Bottom-Up Org Building** — `construir organograma top down versus bottom up primeira contratacao`
- **Superhero → Facilitator** — `transicao de superheroi para facilitador founder para de executar`
- **Time Audit** — `time audit auditoria de tempo onde o time gasta as horas`
- **Key Man Risk + Headaches per Dollar** — `key man risk headaches per dollar dependencia de uma pessoa so`
- **As duas rotas para creative strategist** — `duas rotas para contratar creative strategist formar ou importar`
- **Constraint de 12 meses** _(vizinha, ops-scale-risk)_ — `constraint de 12 meses qual o unico gargalo que limita o ano inteiro`
- **O que quebra entre $500k e $3M/mês** _(vizinha, ops-scale-risk)_ — `o que quebra entre 500 mil e 3 milhoes por mes gargalos por faixa`
- **People-Vision-Cash + os 3 buckets do CEO** _(vizinha, ops-scale-risk)_ — `people vision cash tres buckets do CEO onde o founder gasta o tempo`
- **Founder Optimization + Big 5** _(vizinha, ops-scale-risk)_ — `founder optimization big 5 do fundador foco em poucas alavancas`
- **Modelo de escala por faixa de faturamento** _(vizinha, scaling — já lida pela 12/08; reuse)_ — `revenue tier volume intent systems $50K $300K $3M foco por faixa de faturamento`
- **Estrutura de time criativo por faturamento** _(vizinha, scaling — já lida pela 08; reuse)_ — `estrutura de time criativo por faturamento creative pods Leanne model um creator`
- **Modelo híbrido de time (fractional / freelancer / offshore direto + primeiras 3 contratações)** — `modelo hibrido de time fractional offshore contratacao direta primeiras 3 contratacoes brand DTC`
- **Terceirização sem ser queimado (benchmark de rede + valor esperado)** — `[query provisória — indexar] terceirizar agencia benchmark referencias comparar fornecedores expected value de contratacao`

**PORTA 2 — Contratar (ETAPAs 5-8):**

- **Job Description v2.0** — `job description v2 estrutura moderna responsabilidades e resultados`
- **Job Scorecard (6 blocos)** — `job scorecard 6 blocos missao resultados competencias criterios de sucesso`
- **Role Alignment Call** — `role alignment call alinhar expectativa de funcao antes da oferta`
- **Inverse Thinking para métricas** — `inverse thinking para metricas o que faria a metrica piorar`
- **Talent Engine (pipeline de 9 etapas)** — `talent engine pipeline de contratacao 9 etapas sourcing ate onboarding`
- **Hire Slow but Fast** — `hire slow but fast processo rigoroso sem arrastar a decisao`
- **Sales-Letter Job Posting + faixa salarial alta** — `anuncio de vaga escrito como sales letter faixa salarial alta no topo`
- **Hire-All-Qualified Matrix** — `matriz contratar todos os qualificados quando o funil de talento aparece`
- **Hiring Engine Metrics (cost to hire)** — `metricas do motor de contratacao cost to hire tempo por etapa`
- **5-Stage Rejection Ladder** — `escada de rejeicao em 5 estagios filtrar candidatos por etapa`
- **Custom Loom Headhunting (~40% de response rate)** — `headhunting com Loom personalizado response rate 40 por cento abordagem fria`
- **Headhunted Candidate Funnel** — `funil de candidato headhunted diferente do candidato que se aplica`
- **Big-Agency Poaching Playbook** — `playbook para atrair talento de agencia grande argumentos de saida`
- **Technical Assessment cronometrado** — `technical assessment cronometrado teste pratico com tempo limite`
- **Surprise Weekend Assessment** — `surprise weekend assessment teste surpresa de fim de semana`
- **SME Interview Script** — `SME interview script entrevista conduzida por especialista da area`
- **Two-Offer Salary Negotiation** — `negociacao salarial com duas ofertas estrutura de escolha`
- **Reference Check de 6 perguntas** — `reference check seis perguntas para checar referencia de candidato`
- **Community Hiring** — `community hiring contratar de dentro da comunidade da marca`
- **Ad Bounties** — `ad bounties pagar editores por performance do criativo`
- **Creator Pipeline (hit rate 14% de creators vs 4% interno)** _(ponte com a 16; já lida pela 08/12)_ — `creator pipeline hit rate 14 por cento creators versus 4 por cento interno`

**PORTA 3 — Rodar (ETAPAs 9-13):**

- **JIT Bootcamp (I Do / We Do / You Do)** — `JIT bootcamp onboarding I do we do you do treinamento just in time`
- **Regressive QA (100% → 50% → 20% → 0%)** — `regressive QA revisar 100% depois 50% 20% ate 0% amostragem decrescente`
- **Cadência 5-3-1** — `cadencia 5-3-1 ritmo de check-in com novo contratado`
- **Getting-to-Know-You Form** — `getting to know you form formulario de integracao de novo membro`
- **Comprehension Checks de aplicação** — `comprehension checks de aplicacao confirmar entendimento no treinamento`
- **Goal → Strategy → KPI** — `goal strategy KPI cascata de objetivo para indicador`
- **Core Metrics Dashboard (target semanal = mensal ÷ 4.3)** — `core metrics dashboard target semanal igual mensal dividido por 4.3`
- **Hit Rate por editor** — `hit rate por editor rastrear taxa de acerto criativo por autor`
- **Creative Velocity Metrics** — `creative velocity metrics time to ship internal revisions error tracking`
- **Creative Production Pipeline (statuses + Super Winner)** — `pipeline de producao criativa statuses working filming learning done super winner`
- **Creative Pod Structure** — `creative pod estrutura de celula criativa por marca ou avatar`
- **4 Engines Org Chart** — `organograma de 4 engines estrutura por motor de negocio`
- **Weekly Call Schedule (learnings ANTES do planning)** — `agenda semanal de calls learnings antes do planning ordem das reunioes`
- **Playbooks ("SOPs on steroids", 7 blocos)** — `playbooks SOPs on steroids 7 blocos documentacao de processo`
- **Engine Projects** — `engine projects projetos que constroem o motor e nao entregam tarefa`
- **4 níveis de gestão** — `quatro niveis de gestao do micro ao estrategico`
- **DAI + 5W1H** — `DAI 5W1H delegacao com dono acao e prazo definidos`
- **RAPID + Decision Log** — `RAPID decision log quem recomenda concorda executa decide`
- **Autonomy × Alignment + Disagree & Commit** — `autonomia versus alinhamento disagree and commit`
- **After Action Review** — `after action review retrospectiva do que foi planejado versus o que aconteceu`
- **High Sync High Output + Promise Management** — `high sync high output promise management gestao de promessas do time`
- **"Go Figure It Out"** — `go figure it out cultura de resolver sem pedir resposta pronta`
- **Bi-Annual Review + Team Survey** — `review semestral mais pesquisa de time avaliacao de desempenho`
- **9-Box Grid + regra A/B** — `9-box grid performance potencial regra A B de talento`
- **PIP (Performance Improvement Plan)** — `performance improvement plan PIP plano de recuperacao de desempenho`
- **Os 2 gatilhos de demissão** — `dois gatilhos de demissao quando desligar sem hesitar`
- **Modelo Gravy** — `modelo Gravy remuneracao variavel acima do resultado base`
- **Escada de incentivos financeiros** — `escada de incentivos financeiros bonus comissao equity por nivel`
- **A-Playing Field + Big 3 da motivação** — `A-playing field big 3 da motivacao ambiente para A-player render`
- **Zone of Genius Role Redesign** — `zone of genius redesenhar a funcao em volta da forca da pessoa`
- **As 7 alavancas de promoção** — `sete alavancas de promocao o que destrava a proxima faixa`
- **Promotion Readiness Test** — `promotion readiness test candidato esta pronto para promover`

Antes de fechar cada ETAPA, releia a lista da porta correspondente e confirme: alguma entrada relevante ficou sem puxar? Se sim, puxe agora.

## Fluxo da Skill

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
3. **O que fazer no lugar:** a skill que ataca o gargalo nomeado (04 pra oferta, 08 pra criativo, 02 pra pesquisa...).
4. **O marco que reabre esta conversa:** "quando [sinal concreto — ex.: editar vídeo virar a maior fatia da sua semana com a máquina de ads validada], volta aqui que a gente monta a vaga."

Exceção pontual coberta: membro `validating` afogado em edição pode contratar **editor por projeto/freelancer** sem abrir o funil completo — bons editores custam **US$ 2,5-5k/mês** no mercado global (referência da fonte; há quem pague US$ 8k pelos melhores), e por projeto sai bem menos. Vale a regra da ETAPA 5 mesmo assim: sucesso definido antes (o que é um vídeo "pronto", quantos por semana, prazo de entrega).

---

**PORTA 1 — DECIDIR (ETAPAs 2-4). Pergunta do membro: "devo contratar? quem primeiro?"**

### ETAPA 2 — O tempo do fundador: taxa de recompra e as 4 zonas

Antes de decidir QUEM contratar, meça o que o tempo do membro vale — é o critério objetivo de delegação da fonte (framework popularizado pelo Dan Martell, operacionalizado no material de referência):

1. **Valor da hora** = renda anual ÷ 2.000 (horas úteis/ano). Ex.: US$ 500k/ano → US$ 250/h. Use o anual, não o mensal — protege contra meses fora da curva.
2. **Taxa de recompra (buyback rate)** = valor da hora ÷ 4. Ex.: US$ 250/h → US$ 62,50/h. O ÷4 existe porque contratar derruba o lucro no curto prazo — o retorno vem do tempo recomprado.
3. **Auditoria de tempo:** o membro lista TODA tarefa que faz durante 1-2 semanas (documento fixado, ou ferramenta de monitoramento de horas se já usar). Sem essa lista real, o resto da ETAPA fica em `pending_inputs[]` — não invente a agenda do membro.
4. **Classifique cada tarefa nas 4 zonas** (matriz gosto × receita): **Incompetência** (odeia + não gera receita → delega JÁ: emails, agenda, operacional miúdo), **Ressentimento** (odeia + gera receita → continua fazendo e caça um A-player pra assumir), **Luxo** (ama + não gera receita → vira tempo livre), **Gênio** (ama + gera receita → 80% do tempo do membro deveria estar aqui).
5. **Regra de decisão:** pra cada tarefa fora da zona de gênio, identifique quem faria (o "who") e o custo/hora de mercado. **Custo/hora do substituto < taxa de recompra → delega.** A inversão que convence: quem tem hora de US$ 250-1.000 e ainda sobe ads está pagando US$ 250-1.000/h por um trabalho de media buyer júnior.

Duas trilhas de leitura complementares da fonte, pra enquadrar a conversa: o trabalho de quem lidera se resume a **Pessoas, Visão e Caixa** (visão atrai gente boa, gente boa gera caixa, caixa compra gente melhor) — se o membro não está criando visão nem adquirindo pessoas, ele está fazendo o trabalho errado; e **delegar tarefa ≠ delegar atenção**: se a área delegada ainda ocupa a cabeça do membro (todo problema dela vira pergunta pra ele), a delegação resolveu metade. Líder de verdade é a pessoa em cuja área o membro **nem pensa**.

### ETAPA 3 — Quem primeiro: tipos de vaga, sequência e o tipo de contratação

**Os 4 tipos de vaga (com prazo realista de contratação, da fonte):**

| Tipo | O que é | Custo de referência | Tempo pra fechar |
|---|---|---|---|
| **Acessória** | Tarefas repetitivas: assistente virtual, atendimento, upload de ads, edição/design de entrada | US$ 1-3k/mês (global) | ~30 dias |
| **Sênior** | Trabalho criativo/avançado + alguma decisão: creative strategist, media buyer sênior | varia por função (ver abaixo) | ~35 dias |
| **Liderança** | Gerencia processo E pessoas (ex.: diretor criativo); precisa ter "ganhado o direito" (já executou a função) | acima de sênior | 60+ dias |
| **Sócio/parceiro** | Lidera líderes; vem com participação | — | quase sempre formado DENTRO, em anos |

A distinção que orienta tudo: **gestores delegam tarefas; líderes delegam decisões.** Se só o membro decide, ele tem gestores — e o gargalo continua sendo ele.

**A sequência que a fonte recomenda (de cima pra baixo, não de baixo pra cima):**

- **De baixo pra cima** (o padrão do fundador): todo mundo reporta a ele → caos, dependência, e o gestor contratado por cima depois não ganha a confiança do time. Correção: promover cedo alguém de dentro pra liderar.
- **De cima pra baixo (recomendado):** pra abrir uma célula nova, contrate primeiro o **sênior que sabe fazer tudo** que o time dele fará; os juniores nascem reportando a ele. Achar júnior é fácil; achar o líder é a parte difícil — o membro faz a parte difícil primeiro.
- **Sequência típica de marca em escala** (referência da fonte pro caminho US$ 100k → 1M/mês): **media buyer/growth primeiro** (tira o membro dos ads), **creative strategist/gestor de UGC segundo** (sem ele o media buyer fica sem munição), **retenção/email terceiro** (20-30% da receita se esconde ali). Depois: operações, atendimento, parcerias. E o lembrete que reequilibra tudo: o time mínimo que leva uma marca de US$ 200k a US$ 1M/mês é **2 editores + 1 copywriter + 1 media buyer** — a pergunta não é quantos, é quão bons.
- **A contratação que remove o membro do próprio processo de contratar:** um recrutador dedicado (ou gestor de operações com chapéu de recrutamento) — processa candidaturas, faz triagem e entrevistas iniciais; o membro só grava as abordagens de headhunting e dá o carimbo final.

**Potencial vs habilidade pronta:** contratar por **potencial** paga-se com tempo (base sólida sem a habilidade exata; exige treino e acompanhamento apertado — um strategist formado do zero leva ~3 meses até o primeiro anúncio vencedor; tende a ser mais leal). Contratar por **habilidade** paga-se com dinheiro (experiência específica de ecommerce; impacto em semanas). Time pequeno com bom sistema de treino → potencial funciona; estágio avançado → priorize habilidade. Sinal de habilidade real: a pessoa **ensina algo novo ao membro** já na entrevista.

**O caso especial do creative strategist** (a vaga mais escassa do mercado): rota A — buscar pronto em agência grande (custa US$ 15-20k/mês pra quem tem histórico de ecommerce; alternativa: base US$ 12k + variável de performance); rota B — contratar fome e treinar (copywriter com vontade vira strategist em ~1,5 mês de treino intensivo; US$ 8-10k/mês + incentivos). E o teto de sofisticação: a partir de ~US$ 1M/mês, a fonte manda contratar **experts melhores que o próprio fundador** no pilar que falta — contratar "gente faminta pra ensinar o que eu sei" produz mini-versões do fundador e no máximo dobra o resultado; quem destrava a próxima ordem de grandeza é quem domina o que o fundador NÃO domina (e o fundador precisa da humildade de deixar a pessoa trazer a mágica dela).

**A matemática que justifica pagar mais:** empresa de 7 dígitos é feita de pessoas com habilidade de 6 dígitos; a de 8-9 dígitos, de **times** de pessoas de 7-8. Pagar acima do mercado é o atalho nº 1 de recrutamento — caso real da fonte: vaga a US$ 6-8k/mês → 3-4 meses de busca, 1 candidato mediano, ~US$ 25k de custo de processo; a MESMA vaga repostada a US$ 9-12k/mês → 2 potenciais A-players em 30 dias (e um fechou por US$ 8k, dentro da faixa antiga). A faixa alta atrai quem não se candidataria, filtra os fracos por autosseleção e cria alavancagem de expectativa. Proteção: período de experiência de 90 dias.

### ETAPA 4 — Montar dentro ou comprar fora (interno vs agência vs modelo híbrido)

A decisão não é binária. O modelo que a fonte recomenda pra marca abaixo de dezenas de milhões/ano é **híbrido**:

| Camada | O que é | Custo de referência |
|---|---|---|
| **Núcleo fixo** (3-7 pessoas) | Fundador + operações + 1-2 executores em função crítica | salário cheio |
| **Executivo fracionado** (fractional: líder sênior por fração da semana) | Diretor de marketing/criativo/retenção "de aluguel" — 80% estratégia, 20% execução | US$ 5-10k/mês (~80% do valor de um executivo full-time por 20-30% do custo) |
| **Freelancers especializados** | Copywriter, editor, media buyer por projeto ou retainer baixo | por projeto |
| **Talento global direto** | Assistentes, atendimento, edição de entrada — contratados DIRETO (sem agência de staffing, que cobra 3-4× de markup: o mesmo profissional sai US$ 800-1.200/mês direto vs US$ 3-4k intermediado) | US$ 0,8-3k/mês |

**O que faz sentido terceirizar** (referência da fonte): canais que não são a força do membro (Google Ads, email/retenção quando a lista ainda é pequena, marketplace). **O que nunca se terceiriza:** a vantagem competitiva — se a força da marca é criativo/copy, isso fica dentro (ou no mínimo o membro segue afiado o bastante pra julgar trabalho bom vs ruim; a fonte estima que até ~US$ 1,5M/mês o fundador precisa estar ~80% dentro do jogo de copy e criativo). Marcas grandes fazem as duas coisas: time interno focado em iterações + agências criativas contratadas em paralelo trazendo apostas novas — e só as boas ficam.

**Protocolo pra contratar agência sem ser queimado** (a fonte é dura: "90%+ das agências não entregam e contam com você não cancelar"):

1. Comece pelo problema, não pela ferramenta: o que exatamente está sendo terceirizado?
2. Pergunte a quem já terceirizou com sucesso **qual é o benchmark esperado** (ex.: % da receita vinda de email) — e cobre a agência contra o benchmark na call. Gaguejou? Próxima.
3. Exija referências e histórico verificável.
4. Fale com **5-7 fornecedores** e compare os preços entre eles — quem não compara paga caro.
5. Aprenda o suficiente da área pra julgar qualidade (a barreira de entrada pro conhecimento hoje é zero).
6. Avalie contratação e serviço por **valor esperado**: um strategist de US$ 5k/mês custa US$ 60k/ano; se produz UM criativo vencedor que gasta US$ 100k+ no ano com margem, a conta fecha mesmo que "pareça" 11 meses de nada.

**Feche a porta 1 com um memo de decisão (formato: Por quê / O quê / Como / Agora-Depois),** de uma página: o gargalo nomeado com número, a vaga (ou a decisão de NÃO contratar / terceirizar), a mecânica (faixa salarial, tipo de contratação, prazo realista do funil pelo tipo de vaga) e a ação com dono e data. Especificidade impiedosa — "preciso de ajuda no criativo" não serve; "a máquina produz 18 conceitos/mês, a capacidade de teste pede 40, e a vaga de editor nº 2 fecha o gap" serve.

---

**PORTA 2 — CONTRATAR (ETAPAs 5-8). Pergunta do membro: "como contrato [função]?"**

### ETAPA 5 — O gabarito da vaga ANTES do anúncio (scorecard + descrição)

Nada vai ao ar antes disto. Dois artefatos, nesta ordem:

**1. Descrição da vaga em card (JD v2.0)** — três blocos:
- **Propósito em 1 frase amarrada a dinheiro** ("lançar ads com eficiência e comunicar dados que alimentam o criativo" — não "gerenciar campanhas").
- **4-6 funções nucleares específicas** (vago é proibido: "gerenciar produção" → "gerenciar o processo do brief à entrega dentro da ferramenta de gestão").
- **Par de indicadores-norte SEMPRE balanceado** — volume + qualidade juntos, porque um sem o outro degenera: gasto nos conceitos + ROAS nos conceitos (anúncio de US$ 10 com ROAS 20× não serve; queremos US$ 20k de gasto a 3×).

**2. Scorecard (o gabarito que define e MEDE sucesso)** — seis blocos: missão do cargo; sucesso definido com números E provado com exemplos reais (a visão que está na cabeça do membro precisa ser MOSTRADA — 99% das vezes a prova existe, só está presa lá); KPIs mensais com faixa verde/vermelha; 2-3 iniciativas por ciclo; responsabilidades e traços avaliados 1-5; valores da empresa traduzidos pro papel.

**Faixas de referência da fonte por função (calibre à estrutura do membro — os números pressupõem uma máquina criativa completa; estrutura menor, régua menor):**

| Função | KPIs com faixa |
|---|---|
| Creative strategist | Hit rate de ads ≥10% · conceitos entregues/mês (70 na estrutura de referência; ~50 em estrutura menor) · ideias ≥35 · taxa de revisão <25% · tempo até o ar ≤6 dias · % do gasto total |
| Editor | Hit rate POR EDITOR · lotes/conceitos · taxa de revisão · entrega no prazo · tempo de edição · % do gasto total · capacidade ~7 vídeos/semana |
| Media buyer | Tempo do brief ao lançamento (~4 dias; bom lança em 24h da aprovação) · nº e % de erros · dados reportados no ritmo |

Truque de rastreio que liga esta skill à 11: **sufixo com o nome do editor/strategist no naming dos ads** → a busca no gerenciador mostra o % do gasto que os ads DELE puxaram. Grave a convenção em `dados.json.naming_suffix_by_person` — a 11 usa isso pra atribuir hit rate por editor.

**Ferramenta de desenho de métrica:** pensamento inverso (via Charlie Munger) — "se essa pessoa fosse demitida em 60 dias, por quê?" → liste os comportamentos do fracasso e inverta-os em métricas.

**Pra função que JÁ existe no time:** antes de contratar o segundo do mesmo papel, rode uma **call de alinhamento de função** com o atual — a pessoa traz a lista de TUDO que faz (ela fala primeiro), compara com a lista do gestor, e o papel é redesenhado (parar/começar/continuar). Caso real da fonte: um media buyer gastava metade do dia num processo de re-upload que ninguém sabia que existia — a call liberou ~6h/dia.

### ETAPA 6 — Anúncio e sourcing: atrair, caçar e cultivar

**Anúncio (job posting):**

- **Canais como plataformas de anúncio** (todos funcionam; o que muda é a qualidade do SEU posting): Indeed (grátis, global — nº 1), LinkedIn (pago; US$ 6/dia bastam — US$ 24 já geraram ~140 candidaturas), indicações (versão paga: ~20% de um salário mensal ou US$ 1-2k por indicação contratada), grupos/comunidades da área, plataformas de talento global pra vagas acessórias (nessas, inverta o funil: teste prático ANTES da call).
- **Dois formatos:** direto (vagas simples) ou **carta de vendas** (vagas altas): a dor do candidato → "sabemos porque estivemos lá" → o sonho → provas da empresa → o que a pessoa vai ser DONA → requisitos → remuneração e benefícios → valores (pedindo pra citar o favorito na candidatura — teste embutido de leitura) → o processo seletivo listado etapa a etapa.
- **Faixa salarial publicada na metade ALTA do mercado** — é o filtro de qualidade nº 1 (ETAPA 3). Sem faixas absurdas de largas.
- **Qualificadores duros no texto** filtram volume genérico: "não se candidate se nunca geriu US$ 10-20k/dia".

**Headhunting (caçar quem não está procurando emprego) — a rota nº 1 da fonte pra vagas sênior/liderança, conduzida pelo próprio dono:**

- **Vídeo curto personalizado por alvo** (máx. 3 min, gravado pra AQUELA pessoa; ~40% de taxa de resposta reportada): abertura humana que tira a pressão → mostrar o que a empresa TEM (faturamento, meta, comunidade) → conectar com as dores do alvo ("em agência você apaga incêndio de 10 contas; aqui você vai FUNDO em uma marca") → mini organograma na tela posicionando a pessoa → fechamento leve. Até os "não" viram pipeline: gente responde 8 meses depois, quando o chefe irrita.
- **Funil DIFERENTE pra quem foi caçado:** sem triagem e sem vídeo de candidatura (a call inicial vira uma call de VENDA conduzida pelo dono), agendamento concierge, **teste prático SEMPRE pago** (a pessoa tem emprego e não pediu nada — a fonte cita US$ 200-250 pra vagas sênior), referências normalmente puladas.
- **Garimpo em agências grandes:** liste as maiores agências (200-500+ pessoas — treinamento bom por necessidade), busque perfis mid-level **sem promoção há 2-4 anos**, aborde vendendo oportunidade e teto ("aqui você é o nº 1"), nunca "quero que trabalhe pra mim". Arbitragem citada: pagar US$ 4k em alguém que, treinado, vale US$ 10-12k.

**Community hiring (o fim de jogo):** um líder A-player do time documenta o que faz, vira treinamento, vira comunidade paga do nicho de talento (editores, criadores de página) — e **as pessoas passam a PAGAR pra entrar no funil de contratação do membro**, já treinadas do jeito da casa. O acordo certo com o líder é por afiliação (ex.: ~30% sobre quem entra pelo link da empresa), nunca tomar corte do negócio dele — é o incentivo de empreendedorismo interno que retém A-players. Aviso da fonte: não resolve contratação imediata; é jogada de longo prazo.

**Bounties e creators — a fronteira com a 16:** prêmio por performance pago a **editores do time** (remunerar o editor com % atrelada ao desempenho do criativo que ele produziu) é incentivo interno — vive aqui e na ETAPA 13. Bounty aberto pra **creators externos**, pipeline de creators (o dado de referência: hit rate ~14% de creators vs ~4% do time interno) e programa de embaixador são canal da **skill 16 (creator-engine)** — quando a conversa virar "quero criativo de gente de fora", aponte pra lá (se a 16 ainda não existir no clone do membro, os frameworks de creator seguem acessíveis pela 08).

### ETAPA 7 — O funil: 9 etapas, teste cronometrado e a oferta

**O pipeline (cada etapa filtra uma dimensão; decisão binária em cada uma — avança ou sai, sem empurrar com a barriga):**

1. **Anúncio + sourcing** (ETAPA 6)
2. **Triagem de candidaturas** — delegável só a quem reconhece talento; menos candidaturas com alta intenção > volume genérico
3. **Vídeo de apresentação** (2-3 min do candidato): testa seguir instrução (não enviou = fora) e revela postura que currículo esconde
4. **Entrevista de cultura e traços** (20-30 min, com roteiro; os traços da descrição da vaga viram perguntas)
5. **Teste prático cronometrado** — a etapa inegociável (abaixo)
6. **Entrevista técnica com o especialista da área** (o futuro gestor conduz; pedir que o candidato **explique o papel de volta** — "descreva uma semana típica"; a pergunta que separa: *"como é um A-player nesse papel?"* — A-players falam de resultado e impacto; medianos listam tarefas)
7. **Entrevista final com o dono** — só pra vagas acima de ~US$ 5-6k/mês (abaixo disso, o time decide com orçamento dado); logística, salário e caráter; atraso >2 min sem aviso = eliminado
8. **Checagem de referência** — 6 perguntas por telefone, <5 min, com referência que o MEMBRO escolhe pelo histórico (nunca a "referência do pai"); a resposta que importa: *"você recontrataria?"*
9. **Oferta + contrato** — dispara o onboarding (ETAPA 9)

**O teste prático (assessment) — regra da casa:**

- Máximo **2 horas** de trabalho (mais que isso = teste mal desenhado), com TUDO que a pessoa precisa (materiais, exemplos, acessos temporários — pra teste com dados reais de conta de ads, acesso temporário de poucos dias + acordo de confidencialidade).
- **Vídeo curto obrigatório junto:** o candidato explica o que fez e por quê — avalia-se o RACIOCÍNIO, não só a peça.
- **O cronômetro é metade da nota:** registre envio e devolução. A régua da fonte: **85% de qualidade no mesmo dia vale mais que 90% numa semana** (caso real: dois candidatos igualmente bons, um entregou em 5 dias, outro em 3 horas — contratou-se o segundo).
- Não é pago — EXCETO vagas de liderança e todo candidato caçado.
- **Desempate entre finalistas:** mini-teste surpresa de 30-60 min enviado no fim de semana — quem devolve revela a fome. Inclua um detalhe-armadilha de atenção ("se não achar a imagem certa, descreva a que você usaria").
- Portfólio não prova nada (é fácil de forjar); o teste prova.

**Velocidade: processo rigoroso, calendário comprimido.** "Contrate devagar" vale pro critério, nunca pro relógio — talento bom fecha com o mercado em ~8 dias (dado citado via Hormozi). Candidatura ótima na segunda → call no mesmo dia → teste enviado em minutos → entrevista técnica no dia seguinte → final no outro → referência em paralelo → oferta no mesmo dia da final. Diga o ritmo ao candidato explicitamente ("se devolver amanhã, fechamos até sexta — topa?"). Pular etapa não é acelerar — é a origem do bad hire.

**Negociação e oferta:**

- **Técnica das duas ofertas** (a preferida da fonte, tira a negociação da call): "você vai receber DUAS ofertas — (1) perto do que pediu com variável menor, ou (2) base menor com pacote de performance melhor. Qual prefere?" Quem confia em si escolhe performance — e isso também é sinal.
- Oferta com narrativa ("de 520 candidaturas chegamos a UM — você") + vídeo curto explicando o contrato cláusula a cláusula.
- Contrato: período de experiência de **90 dias** ("na 1ª ou 2ª semana você já sabe se é killer"), avisos assimétricos, meio-a-meio no mês. Templates não são à prova de bala — revisão jurídica é do membro.
- **2+ finalistas A-players = sinal de funil saudável, não problema.** A matriz da fonte: os dois em meio período no mesmo papel (trial de ~30 dias); um integral + um meio período; os dois integrais (funções sempre escaláveis: editor, designer, copy); um no papel + outro em papel ADJACENTE real (com scorecard próprio); ou vaga sob medida (raro). "A-player você nunca deixa ir — se aparecer um, você CRIA espaço."
- **Rejeição em escada, personalização crescente** (automática no início do funil → pessoal e específica no fim, com oferta de feedback): reputação no mercado de talento + efeito bumerangue — rejeitado bom evolui e volta. Nunca sumir sem resposta.
- **Não pare de contratar depois de contratar:** anúncio ativo e entrevistas agendadas concluídas até o novo contratado sobreviver à experiência — o pipeline aquecido é o seguro. E-mail explícito aos finalistas fortes ("quero ficar próximo").

### ETAPA 8 — Métricas do funil e a pergunta "a folha cabe?"

**Métricas do motor de contratação (grave a cada vaga fechada):**

- **Tempo pra contratar** (referências da fonte: acessória ~30d, sênior ~34-35d, liderança ~60d; média real ~38d)
- **Custo de contratar** = (tempo pra contratar ÷ 30) × US$ 5.000 (custo mensal estimado do processo — ex.: 82 dias ≈ US$ 13k; é o número que justifica pagar faixa alta e fechar rápido)
- **Onde o funil perde candidatos** (qualificado/desqualificado/perdido por etapa)
- **Resultado de cada contratação** (ruim / mediana / ótima) + canal de origem — é o feedback loop do processo: a fonte reporta um ano com 54% de contratações ruins ANTES de levar o funil a sério, e 100% de retenção no ano seguinte.

**"A folha cabe no caixa?" — pointer pra 15, nunca conta própria:**

1. Some o custo mensal da vaga nova (salário + ferramentas + variável estimada no alvo) = `payroll_delta_monthly`.
2. Leia `15-finance-engine/dados.json` (ou `manifest.finance`): `monthly_model.operating_income`, `monthly_model.fixed_costs_monthly`, `cash.runway_months`. Folha é **custo fixo** — a leitura honesta é "a vaga sobe seu custo fixo de A pra B; pelo modelo da 15, o resultado operacional atual é C e o fôlego de caixa é D meses".
3. **Sem a 15 rodada (ou sem custo fixo informado):** a resposta vira pergunta, não instrução — "não dá pra dizer se cabe sem o modelo financeiro; roda 'finanças' que a 15 fecha isso em minutos". Registre em `pending_inputs[]`. Proibido dizer "cabe tranquilo" de sensação.
4. **Depois de contratar:** lembre o membro de atualizar o custo fixo na próxima rodada da 15 — o campo canônico `manifest.fixed_costs_monthly` é escrito pelo membro através da 04/11/12/15; esta skill não o escreve, aponta.

---

**PORTA 3 — RODAR (ETAPAs 9-13). Pergunta do membro: "como faço o time performar?"**

### ETAPA 9 — Onboarding: treinamento na hora certa, confiança por evidência

O objetivo declarado da fonte: "construir sistemas onde é impossível a pessoa falhar". O modelo "aqui está a ferramenta, se vira" falha sempre. Duas partes:

**1. Integração técnica (dia zero):** automação de contas/acessos, documento de boas-vindas que abre pelos **valores da empresa** e segue ferramenta a ferramenta, **formulário de conhecer a pessoa** (aniversário, hobbies, como gosta de receber feedback — direto ou com jeito —, reconhecimento público ou privado, tipo de aprendiz) — os dados alimentam a gestão o ano inteiro. Call técnica de ~30 min conferindo acessos (não precisa ser o membro). Velocidade importa: a pessoa começa assim que assina.

**2. Bootcamp de treinamento na hora certa (JIT — o treino chega quando a tarefa chega, não tudo de uma vez), máximo 8 semanas:**

- **Eu faço (semana 1):** o gestor executa ao vivo em 3 camadas — os passos, o como, e as RAZÕES de cada ponto-chave.
- **Nós fazemos (semanas 2-3):** o novato executa explicando passo e porquê; correção na hora.
- **Você faz (semana 4+):** trabalho real, começando por material de baixo risco (nunca no cliente/campanha mais crítica).
- **QA regressivo — supervisão que diminui por evidência, não por tempo de casa:** semana 2 = revisar **100%** de tudo antes de ir ao ar → semana 3 = **50%** → semana 4 = **20-25%** → semana 5+ = **0%**, com conferências aleatórias pra sempre. Grave o estágio de QA de cada pessoa em `dados.json.onboarding[]` — é o dado que a 09 (consistency-audit) usa como referência quando audita artefatos produzidos por gente nova.
- **Cadência 5-3-1 de reuniões:** semana 1 = 1:1 todo dia; semanas 2-3 = 3×/semana; semanas 4-8 = 1×/semana ("traga suas dúvidas acumuladas" + o gestor traz a lista do QA).
- **Cheques de compreensão por aplicação, nunca "entendeu?"** (gera "sim" preguiçoso): "como você explicaria isso pra outra pessoa do time?", "em que situação isso NÃO funcionaria?".
- **Diagnóstico em 2 semanas:** (a) voando desde o início; (b) KPIs fracos mas melhorando toda semana com esforço visível → mantém; (c) sem progresso → plano de recuperação e busca reaberta. Treinamento passando de 8 semanas só tem dois diagnósticos: pessoa menos experiente que o esperado (ok SE melhora semana a semana) ou contratação errada.
- Sênior não dispensa estrutura — dispensa micro-checklist, não cadência (huddles curtos na semana 1, chegando COM pauta).

### ETAPA 10 — KPIs por função e o painel semanal

**A cascata que evita indicador órfão:** **Goal → Estratégia → KPI.** O goal quase não muda (ex.: US$ 5M/mês); a estratégia é a aposta do momento ("dobrar o volume de anúncios vencedores"); os KPIs testam se a aposta está sendo executada. As **2 regras de ajuste**: bateu os KPIs mas não bateu o goal → a ESTRATÉGIA está errada; bateu o goal sem bater os KPIs → os KPIs estão superdimensionados, recalibre. Nunca mude o goal.

**O painel semanal (a implementação de gestão mais valiosa da fonte):**

- Colunas: departamento → métrica → **fonte do dado** (dado impreciso = decisão ruim) → **dono único** (quem preenche e responde; o membro não preenche KPI dos outros) → alvo → realizado por semana (segunda→domingo, verde/vermelho automático).
- **Alvo semanal = alvo mensal ÷ 4,3** (não ÷4).
- Indicadores **antecedentes** acima dos de resultado: ROAS do mês é consequência; nº de anúncios vencedores novos por semana é o que o prevê.
- Call semanal curta com os líderes: vitórias → destaques → alvos por área → prioridades. **Todo KPI perdido exige do dono: motivo + experimento** (o que faremos diferente) — que vira a prioridade dele. Registre motivo também quando SUPERA muito (pra sistematizar o acerto).
- KPIs viram conversa de dados, não de sentimento: "você leva 7,7 dias pra entregar brief; precisa ser 3" encerra a discussão que "você é lento" jamais encerraria.

**Granularidade desce só quando o agregado piora:** nível 1 = total de vencedores → nível 2 = por tipo (imagem vs vídeo) → nível 3 = **por editor**. O scorecard de editor real da fonte: hit rate por editor (ex. real de um mês: 5,26% / 3,7% / **14,28%**), conceitos, taxa de revisão, entrega no prazo, tempo de edição, % do gasto total (via sufixo no naming — ETAPA 5). Gestão de capacidade empírica: editor com ~30 conceitos/mês e hit rate 3,7% → reduza volume e veja se a taxa sobe; editor com 18 vídeos e 14% → aumente volume e veja se escala. Hit rate sozinho engana: cruze com % do gasto e com a qualidade do brief antes de culpar o editor. Painel **compartilhado de propósito** — editores verem o hit rate uns dos outros cria competição saudável.

**Velocidade criativa (o KPI de máquina, não de pessoa):** tempo até o ar (~5,5-6 dias na referência; meta ≤7), revisões internas (**5 revisões = problema, convoque call**; "melhor um ad 100% pronto do que seis ads 50-75% prontos"), rastreio de erros pós-lançamento — **taxa de erro alta = processo pouco claro ou time sobrecarregado; o remédio é melhorar o processo, não punir.** Capacidade de referência: ~7 vídeos/semana por editor (ads complexos 3-4h, normais 1-2h). Resolve também o "media buyer não tem KPI": tempo até lançar (~4 dias; bom lança em 24h da aprovação), nº e % de erros.

### ETAPA 11 — Org design, playbooks e como as decisões fluem

**A estrutura em motores (engines):** a empresa mapeada em 4 motores, cada um com um líder — **Campanha** (media buying), **Criativo** (o maior: diretor criativo + copy + strategist + editores + designer; um diretor criativo gerencia até ~10 pessoas), **Conversão** (página/loja) e **Conteúdo** (UGC; nas versões novas, fundido ao Criativo). **Ordem de construção: Campanha primeiro** (tira o membro do media buying), Criativo segundo (líder criativo + quem escreve brief + editor já vão longe), Conversão, Conteúdo por último. Referência de custo da máquina completa: ~US$ 50-60k/mês produz 500+ ads/mês e 15-30 landing pages/mês pra um pequeno portfólio de marcas — útil pra dimensionar o próprio apetite, não pra copiar.

- **Org chart em DUAS versões** (ferramenta visual qualquer): **atual** — com a cara do membro em cada assento que ele de fato ocupa (torna o gargalo visível) — e **futuro** (6-12 meses): contratar vira "preencher blocos vazios".
- **Máximo 4 subordinados diretos por pessoa (6 é o teto absoluto).** Camadas existem pra ninguém gerenciar gente demais.
- **Células (pods):** produção criativa organizada em células dedicadas por marca ou por avatar — **nunca por estilo de criativo**. Célula inicial: 1 strategist → 1 editor + 1 designer; evolui promovendo o strategist a sênior com copywriters abaixo. Um sênior gerencia cada função quando ela passa de ~2 pessoas. Rotacione gente entre produtos pra evitar desgaste.
- **Todo líder sabe executar o que o time dele faz** (diretor criativo edita e escreve brief) — é o que permite detectar corpo mole e treinar.
- **Herói → facilitador:** enquanto o membro conserta tudo, o time aprende que "o fundador resolve", nada é documentado e A-players não ficam. Protocolo anti-herói ao se pegar salvando o dia: de quem é esse trabalho? por que EU estou fazendo? → documente, transforme em processo e devolva ao dono. Se depois de treinar, documentar e facilitar a pessoa ainda não performa — aí sim é problema de pessoa.
- **Risco de pessoa única (key man risk):** se o melhor gestor sair amanhã, o que quebra? A causa estrutural: promover o melhor executor a gestor sem experiência de gestão — e todo mundo finge que sabe. O antídoto é sistema + donos claros (abaixo), nunca heroísmo. Vale pro próprio membro: quanto mais ele segura, mais ELE é o risco.
- **Ritmo semanal:** check-in de dados na segunda → dia livre de execução → **call de aprendizados no meio da semana ANTES da call de planejamento** (o plano da semana parte do que foi aprendido) → planejamento → fechamento leve. Calls internas de até 60 min. Metas de ciclo: briefs prontos até segunda; sem trabalho no fim de semana.

**Playbooks ("SOPs turbinados" — SOP = procedimento operacional escrito):** documentação de processo em 7 blocos — objetivo da tarefa; por que ela existe; visão geral + passo a passo com telas; conhecimento tribal (os truques de quem é bom naquilo); **como é RUIM**; **como é EXCELENTE** (com exemplos reais); KPIs da tarefa — com estimativa de tempo por passo. Priorize os maiores gargalos, 1-2 playbooks por dia; processo mudou → playbook atualizado. A síntese da fonte sobre pra QUEM se escreve: **sistemas para high performers, SOP para o repetitivo e o onboarding** — não "à prova de burro" pra gente sênior. E o motivo extra na era da AI: playbook é o contexto que separa quem usa AI bem ("todos têm as mesmas ferramentas; o que separa é o contexto").

**Projetos de motor:** separe os projetos que CONSTROEM a máquina dos que entregam a tarefa do dia — um quadro por área, cada aprendizado vira card com dono + hipótese + resultado; deu certo → atualiza o playbook.

**Como as decisões fluem (os frameworks de decisão):**

- **Os 4 níveis de gestão, em ordem obrigatória:** **Clareza** (qualquer pessoa sabe responder "o que é vencer?" pro negócio e pra função dela) → **Responsabilização** (conversa por placar, não por sentimento — "own the score, not the effort") → **Esforço coordenado** (o time só trabalha no que move o placar) → **Melhoria contínua** (retrospectivas). Não adianta cobrar (nível 2) sem clareza (nível 1).
- **5W1H como brief mínimo:** toda tarefa/processo responde quem, o quê, onde, quando, por quê, como. Teste os furos perguntando ao time "quem é o dono disso? por que existe?".
- **DAI — um único dono por decisão** (Directly Accountable Individual: a pessoa que vive e morre por ela), com **limites** (o que controla e o que não) e **cenários de escalada** escritos. Contrato emocional neutro: "se der certo, o crédito é seu; se der errado, você conduz a retrospectiva e apresenta os aprendizados". Se o membro reclama que "o time não pensa como dono", cheque primeiro se existe dono claro — geralmente não existe.
- **RAPID + registro de decisões** (framework da Bain): quem Recomenda, de quem se ouve Input, quem precisa concordar (Agree), quem Decide, quem executa (Perform) — cada decisão relevante vira UMA linha numa planilha (o registro combate o esquecimento institucional e permite retrospectiva sobre decisões, não só projetos).
- **Autonomia × Alinhamento:** o alvo é alto alinhamento + alta autonomia ("precisamos resolver X; descubra como e volte"). Alto alinhamento com baixa autonomia é ditadura — key man risk institucionalizado.
- **Discordar e se comprometer** (via Amazon), pras decisões sem volta: quem discorda é OBRIGADO a falar ANTES; decidido, compromete-se totalmente — inclusive o dono, quando o DAI decidir diferente dele.
- **Retrospectiva pós-ação (AAR):** ao fim de projeto/campanha, hierarquia suspensa: o que deveria ter acontecido vs o que aconteceu → o que foi bem/mal e por quê → lista curta de próximos passos. Facilitador neutro quando possível. Matéria-prima inclui **perder um A-player**.
- **"Vá descobrir" (anti-gestor-Wikipédia):** antes de escalar um problema, a pessoa traz o problema real formulado como lacuna (o que acontece vs o que deveria), 2+ opções, e a recomendação dela com o porquê.
- **Gestão de promessas:** coluna "quem está esperando" em toda tarefa — mata o "eu ia te responder aquilo". Fechar loops > abrir loops.

### ETAPA 12 — Reviews, 9-box, plano de recuperação e desligamento

Premissa que muda o tom: **90% da baixa performance é expectativa mal definida** (e o membro é co-responsável); só 10% é contratação errada mesmo.

- **Cadência:** contratado novo → review mensal nos 2 primeiros meses; demais → trimestral; painel semanal rodando por fora. Estrutura da call (em cima do scorecard): KPIs → iniciativas → responsabilidades com **preenchimento duplo** (a pessoa se avalia, o gestor avalia, a conversa fecha a diferença — com dados) → plano de ação (sem ele, "a call foi toda pro nada"; os itens viram as iniciativas do próximo ciclo). Pergunta de pulso no agendamento: auto-classificação em **motivação × habilidade** — habilidade se treina; motivação baixa é o alerta.
- **Review semestral:** pesquisa com o time (recomendaria a empresa como lugar de trabalho, satisfação, começar/parar/continuar — as respostas viram iniciativas do semestre) + **grade 9-box** (desempenho × potencial, 9 caselas: do risco imediato ao destaque que precisa de liderança já). Cada gestor avalia o próprio time; o membro só avalia os diretos. Regra dura da fonte: **não mantenha ninguém por "potencial"** — só por desempenho; e pros melhores, **antecipe a conversa de carreira antes que o mercado o faça**.
- **Regra A/B:** liste todos como A, B, C ou D. A-players lideram sozinhos; B-players sustentam; desenvolva B → A; **quem não é A nem B sai** — tolerar C/D derruba os outros ("com C no time, os B gravitam pra baixo").
- **Plano de recuperação (PIP — plano formal com prazo e passos):** valores violados + prazo (padrão 30 dias) + "eis o que estamos observando" com DADOS (nunca "sinto que você não trabalha"; sempre "70 conceitos e zero vencedores", "taxa de revisão 60% vs 10% do colega") + **responsabilidade própria assumida por escrito** ("nosso treinamento falhou nisso; eis o que estamos mudando") + passos mensuráveis + assinatura com espaço pra discordar. Taxa de recuperação reportada pela fonte: **~90%**. Quem escreve leva ~1h — "se não está disposto a gastar 1h escrevendo, você já decidiu demitir". Muitas vezes a conversa dura ANTES do plano resolve em uma semana. Com funcionário formal (EUA/Canadá), demitir sem plano prévio pode dar problema jurídico — revisão legal é do membro.
- **Auditoria de tempo ("estudo de tempo", nunca "vigilância"):** anunciada com o framing certo ("é otimização, não monitoramento; eu mesmo vou fazer"), 2-4 semanas, ferramenta de monitoramento de horas. O que se busca: onde vão as horas, baselines pra contratação, quem tem folga e quem está sobrecarregado. Referências: ~7h úteis/dia esperadas, ~95% de utilização é saudável. Os arquétipos que aparecem: o saudável, o sobrecarregado (redistribuir antes do burnout), o subutilizado (se bate KPI → conversa de expansão; se não → conversa dura) — e o próprio dono (caso real: 38h/semana em reuniões e chat; saiu de várias). Atenção legal: gravar tela de equipamento que a empresa não forneceu pode ser ilegal em algumas jurisdições — informe-se e comunique.
- **Os 2 gatilhos de desligamento:** (1) **não bate KPI** — melhoria tentada → plano de recuperação → sem virada, desligamento; (2) **desligou por dentro** (checked out: atrasos, sumiço, sem responsividade) — conversa direta + estudo de tempo. **Os dois juntos = desligamento imediato.** Exceção óbvia: violação grave de ética/valores → direto. Saída elegante sempre (intros, recomendação) — e a auto-crítica da fonte: erra-se mais por demorar demais do que por demitir cedo.

### ETAPA 13 — Incentivos e promoções (as alavancas de retenção)

**Regra de ouro de qualquer incentivo: simples, claro, alcançável** — se o time não entende como ganhar, não motiva.

- **Modelo Gravy (participação no EXCEDENTE):** defina o alvo mensal na projeção (lucro, receita ou gasto — pra alvo de lucro, o número vem da 15, não desta skill); o que passar do alvo é o "molho": **30-50% do excedente vira o pool de bônus** (padrão 40%; nunca acima de 50% — a empresa precisa reter lucro), dividido por percentuais individuais **privados** e deliberadamente ponderados por quem dirigiu a performance do mês. O racional: o bônus sai de dinheiro que "não deveria existir" — indolor pro caixa e diretamente causado pelo time. Cuidado com sazonalidade: não torre o pool em janeiro pra sofrer em julho.
- **Bônus de KPI:** 5-15% do salário mensal por bater os alvos com consistência — deixando claro que **bater KPI é a expectativa básica do salário**; bônus grande é pra quem vai além.
- **% de performance competitiva:** só os top 3-5 ads do mês pagam — força strategists/editores a competir. Teste e meça: hit rate subiu, mantém; caiu, remove. (Com editor interno = incentivo desta skill; com creator externo = programa da 16.)
- **Funções que não geram receita** (operações, dev, recrutamento): aumentos a cada ~6 meses + bônus pontual + título; variante vista na fonte: salário do líder de operações escalonado por faixa de receita da empresa.
- **A escada de carreira:** trilha de senioridade (vendida já na contratação: "entra júnior; te vejo sênior em 1-2 anos"), trilha de gestão (mini-empresa embaixo da pessoa — com o alerta: **seu melhor editor não é necessariamente seu melhor gestor de editores**; quem prefere ser especialista promove-se por escopo e pagamento, não por gestão), e sociedade/participação **só pra pouquíssimos** (nunca distribuir participação levianamente).
- **As 7 alavancas de promoção, da mais barata pra mais cara:** (1) **título (custa US$ 0** — título é identidade; sempre acoplado a UMA responsabilidade real nova); (2) aumento de 5-10% pra excelência na mesma função (quanto menor o salário, maior o % viável); (3) checar o mercado antes de aumento grande (promover de dentro normalmente paga abaixo do mercado e ainda dá salto pra pessoa); (4) **experimente antes de comprar** — responsabilidades ANTES do título/salário; provou, formaliza; (5) subir o variável em vez do fixo quando o caixa aperta; (6) **nunca promover pra reter** nem porque pediram — promova porque mereceram (contra-oferta de pânico é anti-padrão; quem chega EXIGINDO promoção sem provas é red flag — "os que realmente merecem nunca pedem"); (7) conhecer os números antes de qualquer aumento (P&L e caixa — de novo: 15).
- **Sinais de que alguém está pronto pra subir:** KPIs superados por meses; treinou/gerenciou outros sem ser pedido; resolveu problemas que o membro nem sabia que existiam; criou sistemas; os colegas vão naturalmente até a pessoa pedir conselho. Gestores reportam pra cima quem está voando — aumento proativo com transparência de caixa vale mais que reativo.
- **Os 3 motores da motivação (via Daniel Pink):** autonomia (donos de RESULTADO, não de lista de tarefas), maestria (metas pessoais/profissionais/financeiras de cada um mapeadas + investimento em desenvolvimento — "treinar é caro? NÃO treinar é caro"; "e se eu treinar e saírem? e se eu não treinar e FICAREM?"), propósito (ninguém trabalha pra encher o bolso do dono — propósito com "p minúsculo" basta). Reconhecimento custa US$ 0 e retém tanto quanto dinheiro: público (canal de vitórias) ou privado (mensagem direta inesperada), conforme o que a pessoa declarou no formulário de entrada.
- **O campo de A-player:** se a marca não atrai A-players, o problema é o campo, não o mercado — visão crível (gap alcançável entre onde está e onde diz que vai, com prova), motivação intrínseca (A-player cercado de medianos carrega o time e se esgota) e ownership radical. E redesenhe cargos em volta da força de cada um (mapear o que a pessoa ama, o que gera receita e o que ela odeia — e mover o cargo na direção do primeiro par): é o maior truque de retenção que existe.

---

### ETAPA 14 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Toda vaga recomendada tem `hiring_decision.constraint` preenchido com o gargalo real e o dado que o sustenta — nenhuma vaga "porque sim".
2. `stage_check` gravado; pra membro `starter`/`validating` sem exceção aplicável, o output é a resposta "ainda não" da ETAPA 1.5 — o funil completo não rodou por inércia.
3. Nenhuma vaga em `open_roles[]` com anúncio publicado sem `scorecard` preenchido (missão + funções + par de indicadores com faixa).
4. Todo par de indicadores-norte é balanceado (volume + qualidade juntos); nenhum KPI de volume solto.
5. `payroll.fits_cash` só tem veredito quando os números da 15 (ou do membro) existem; sem eles, `null` + entrada em `pending_inputs[]` + a recomendação virou pergunta.
6. Nenhum salário, KPI real ou dado de agenda do membro foi inventado — benchmarks da fonte estão marcados como referência (`source: "reference"`), números do membro como `member`.
7. Nenhum creator/afiliado/embaixador entrou em `org` ou `open_roles[]` — fronteira com a 16 respeitada.
8. Nenhuma recomendação de desligamento sem os 2 gatilhos avaliados com dados — e com plano de recuperação antes, exceto violação grave de ética.
9. Recomendação de promoção cita a prova concreta (trigger objetivo), nunca "merece" solto.
10. `naming_suffix_by_person` gravado quando existe editor/strategist produzindo criativo — é o handoff que liga hit rate a pessoa na 11.
11. O relatório contém só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa (rule `report-only-results.md`), e 100% legível de primeira por quem não é do setor (regra 0).
12. Portas não rodadas não deixaram seção vazia nem explicação no relatório.

## Output Schema — `18-team-engine/team-engine.md` + `18-team-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills 08, 09, 11, 12, 15 e 16.

```json
{
  "team_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "currency": "USD",
  "doors_run": ["decide", "hire", "run"],
  "hiring_language": "en",
  "stage_check": {
    "stage": "starter | validating | scaling",
    "recommended": false,
    "not_yet_reason": "gargalo atual é oferta/criativo, não braço",
    "reopen_signal": "sinal concreto que reabre a conversa",
    "exception_applied": "none | project_editor"
  },
  "founder_time": {
    "annual_income": null,
    "hourly_rate": null,
    "buyback_rate": null,
    "audit_source": "member_list | tracking_tool | none",
    "tasks": [
      { "task": "", "hours_week": 0, "zone": "incompetence | resentment | luxury | genius",
        "who": "", "market_cost_hour": null, "delegate": null }
    ]
  },
  "hiring_decision": {
    "constraint": "o gargalo nomeado, com o dado que o sustenta",
    "verdict": "hire | not_yet | outsource | upgrade_existing",
    "build_vs_buy": {
      "choice": "in_house | agency | fractional | freelancer | offshore_direct | hybrid",
      "edge_kept_in_house": "o que NUNCA sai de dentro",
      "agency_protocol_done": null
    },
    "sequence": [
      { "order": 1, "role": "", "role_type": "accessory | senior | leadership | partner",
        "hire_for": "skill | potential", "expected_time_to_hire_days": 35, "rationale": "" }
    ],
    "decision_memo": { "why": null, "what": null, "how": null, "now_next": null }
  },
  "org": {
    "current": [ { "seat": "", "person": "", "is_founder_seat": false, "reports_to": "" } ],
    "future_6_12m": [ { "seat": "", "person": null, "reports_to": "" } ],
    "engines": [ { "engine": "campaign | creative | conversion | content", "lead": null, "built": false } ],
    "pods": [ { "pod": "", "segmented_by": "product | avatar", "members": [] } ],
    "max_direct_reports_ok": null,
    "key_man_risk": [ { "person": "", "what_breaks": "", "patch": "" } ],
    "weekly_rhythm_installed": false
  },
  "open_roles": [
    {
      "role": "", "role_type": "accessory | senior | leadership",
      "scorecard": {
        "purpose_one_line": "",
        "core_functions": [],
        "north_star_pair": { "volume": "", "quality": "" },
        "kpi_bands": [ { "kpi": "", "green": "", "red": "", "source": "reference | member" } ]
      },
      "salary_band": { "low": null, "high": null, "source": "reference | member", "posted_top_half": null },
      "posting": { "status": "draft | live | paused", "format": "simple | sales_letter", "channels": [] },
      "sourcing": { "headhunting_active": false, "targets": [], "community_hiring": false }
    }
  ],
  "candidate_pipeline": [
    {
      "candidate": "", "role": "", "source_channel": "", "headhunted": false,
      "stage": "applied | screening_video | culture_interview | assessment | sme_interview | final_interview | reference_check | offer | hired | rejected",
      "assessment": { "sent_at": null, "returned_at": null, "hours_to_return": null, "paid": false, "wow": null },
      "verdict_notes": ""
    }
  ],
  "funnel_metrics": {
    "time_to_hire_days": null,
    "cost_to_hire": null,
    "loss_by_stage": {},
    "outcome_log": [ { "hire": "", "outcome": "bad | average | great", "source_channel": "" } ]
  },
  "onboarding": [
    { "person": "", "week": 1, "phase": "i_do | we_do | you_do",
      "qa_review_pct": 100, "meeting_cadence": "daily | 3x_week | weekly",
      "two_week_diagnosis": "crushing | grinding_up | no_progress | pending" }
  ],
  "team_kpis": {
    "goal": "", "strategy_bet": "",
    "dashboard": { "installed": false, "weekly_target_divisor": 4.3, "weekly_call_day": null },
    "by_person": [
      { "person": "", "role": "", "kpis": [ { "kpi": "", "target": null, "actual": null, "source": "" } ],
        "hit_rate_pct": null, "spend_share_pct": null }
    ],
    "naming_suffix_by_person": {}
  },
  "reviews": {
    "cadence": { "new_hires": "monthly", "team": "quarterly", "survey_nine_box": "jan_jul" },
    "nine_box": [ { "person": "", "box": "", "ab_class": "A | B | C | D", "action": "" } ],
    "pips": [ { "person": "", "opened_at": null, "duration_days": 30, "data_evidence": [], "status": "open | recovered | exit" } ],
    "time_audit": { "last_run": null, "findings": [] }
  },
  "incentives": {
    "gravy": { "active": false, "monthly_target": null, "target_source": "15-finance-engine | member | null", "pool_pct": 40, "split_private": true },
    "kpi_bonus_pct_of_salary": null,
    "career_ladders": [ { "person": "", "track": "ic | management | partner", "next_step": "" } ],
    "promotions": [ { "person": "", "lever": "title | pay_bump | market_check | try_before_buy | variable_up", "proof": "" } ]
  },
  "payroll": {
    "current_monthly_total": null,
    "payroll_delta_monthly": null,
    "fits_cash": null,
    "finance_source": "15-finance-engine/dados.json | manifest.finance | member | missing",
    "note": "folha é custo fixo; veredito só com os números da 15 ou do membro"
  },
  "pending_inputs": [],
  "handoff": {
    "for_skill_08": ["org.pods", "team_kpis.by_person", "open_roles (editor/strategist em contratação)"],
    "for_skill_09": ["onboarding[].qa_review_pct"],
    "for_skill_11": ["team_kpis.naming_suffix_by_person", "team_kpis.by_person[].hit_rate_pct"],
    "for_skill_12": ["org.key_man_risk", "payroll.current_monthly_total", "stage_check", "hiring_decision.constraint"],
    "for_skill_15": ["payroll.payroll_delta_monthly"],
    "for_skill_16": ["fronteira: creators/afiliados/embaixadores não vivem neste arquivo"]
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo são ILUSTRATIVOS** — mostram o formato de cada campo, não um caso real. Benchmarks do material de referência entram sempre com `source: "reference"`; números do membro, com `source: "member"`. Os três dados que nunca se inventam (regra 4): salário/custo real do time, caixa/custo fixo, KPI real de pessoa.

## Contrato de leitura (quem lê o quê)

Esta skill é a **produtora** dos campos abaixo. A leitura é **aditiva, nunca pré-requisito**: quando `18-team-engine/dados.json` não existir, cada consumidora mantém o comportamento atual.

| Skill | Campo que passa a poder ler | O que muda |
|---|---|---|
| **08** creative-engine | `org.pods`, `team_kpis.by_person`, vagas de editor/strategist abertas | O batch passa a saber a capacidade real da máquina (nº de editores × ~7 vídeos/semana) e quem produz o quê — em vez de assumir capacidade infinita. |
| **09** consistency-audit | `onboarding[].qa_review_pct` | Artefato produzido por pessoa em QA regressivo 100%/50% ganha revisão proporcional — a amostragem decrescente vira dado, não intuição. |
| **11** ad-analysis | `team_kpis.naming_suffix_by_person`, `hit_rate_pct` por pessoa | A análise desce ao nível 3 de granularidade (hit rate por editor) usando o sufixo de naming — atribuição de criativo a autor sem planilha manual. |
| **12** scale-engine | `org.key_man_risk`, `payroll.current_monthly_total`, `hiring_decision.constraint` | Antes de autorizar escala agressiva, a 12 enxerga se a operação depende de uma pessoa só e qual gargalo de gente a escala vai estourar. |
| **15** finance-engine | `payroll.payroll_delta_monthly` | A projeção de custo fixo da próxima rodada da 15 já entra com a folha nova na mesa — o membro confirma o número, a 15 recalcula o ponto de cobertura. |
| **16** creator-engine | fronteira declarada no handoff | Creators, afiliados e embaixadores nunca aparecem como funcionários aqui; bounty interno (editor) vive aqui, bounty externo vive lá. |

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `team-engine.md` → `team-engine.html`). **Isento** (arquivo operacional): `dados.json`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, **logo SVG do Aura na topbar copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**, componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/18-team-engine/` antes de salvar.

Outputs em `workspace/[produto]/18-team-engine/`:

- **`team-engine.md`** contendo, na ordem das portas rodadas (portas puladas não aparecem):
  1. O veredito de estágio e o gargalo nomeado (ETAPA 1) — ou a resposta "ainda não" completa (ETAPA 1.5)
  2. **[Porta 1]** Taxa de recompra, as 4 zonas e a lista do que sai da mão do membro (ETAPA 2)
  3. **[Porta 1]** A sequência de contratação com tipo de vaga, faixa e prazo realista (ETAPA 3)
  4. **[Porta 1]** Interno vs fora, com o memo de decisão (ETAPA 4)
  5. **[Porta 2]** Scorecard + descrição da vaga prontos (ETAPA 5)
  6. **[Porta 2]** Anúncio pronto pra publicar + plano de sourcing (ETAPA 6, no `hiring_language`)
  7. **[Porta 2]** O funil com as etapas, o teste prático desenhado pro papel e o roteiro de oferta (ETAPA 7)
  8. **[Porta 2]** Métricas do funil e o veredito (ou a pendência) de "a folha cabe" (ETAPA 8)
  9. **[Porta 3]** Plano de onboarding de 8 semanas com QA regressivo e cadência (ETAPA 9)
  10. **[Porta 3]** KPIs por função com faixas + o painel semanal pronto pra copiar (ETAPA 10)
  11. **[Porta 3]** Org chart atual vs futuro, células e o ritmo semanal (ETAPA 11)
  12. **[Porta 3]** Ciclo de reviews, 9-box e o que fazer com cada casela (ETAPA 12)
  13. **[Porta 3]** Incentivos e promoções com a alavanca mais barata que resolve cada caso (ETAPA 13)
  14. Pendências: o que falta e o que destrava — sem narrar tentativas

- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:

- Adicionar `18-team-engine` em `skills_completed`
- Gravar `manifest.team` = `{ org_size, open_roles_count, hiring_recommended, constraint, payroll_monthly, key_man_risk_flag, checked_at }` — o resumo que as outras skills leem sem abrir o `dados.json` inteiro
- **NÃO** escrever `manifest.stage` (esta skill lê o stage, nunca o altera) e **NÃO** escrever `manifest.fixed_costs_monthly` (campo do membro via 04/11/12/15 — esta skill só aponta)
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `ABRIR-AQUI.html`, onde `<slug>` é o `product_slug`)

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`). Time é o artefato mais vivo do workspace — org, vagas e pipeline mudam toda semana; diga ao membro que esta skill continua de onde parou a cada rodada.

**Porta 1 (decidir), com recomendação de contratar:**
"Decisão montada. Seu gargalo hoje é **[gargalo, com o número]** — e a vaga que o remove é **[função]** ([tipo], faixa de US$ [X-Y], prazo realista de ~[N] dias de funil). Sua taxa de recompra é **US$ [B]/h**: tudo que custa menos que isso por hora pra delegar está te custando dinheiro na sua mão. [Se 15 existe: 'Com a folha nova, seu custo fixo vai de US$ [A] pra US$ [B]/mês — confirma na próxima rodada de finanças.' / Se não: 'Antes de assinar oferta, roda **finanças** — sem o modelo da 15 eu não digo se a folha cabe, e chutar isso é o erro mais caro da lista.']
Revisa o memo e me diz: monto a vaga? (Aí eu abro o gabarito, o anúncio e o funil inteiro.)"

**Porta 1, resposta "ainda não" (starter/validating):**
"Olhei seu estágio e vou te dar a resposta honesta: **ainda não é hora de contratar.** Seu gargalo é **[gargalo, com o dado]** — e contratar agora seria pagar salário pra não resolver o problema (contratação errada custa ~15× o salário anual da vaga). O caminho que ataca esse gargalo é **[skill]**.
O sinal que reabre esta conversa: **[marco concreto]**. Quando chegar lá, volta aqui que eu monto a vaga certa em uma sessão. [Se exceção de editor se aplica: 'Uma exceção cabe já: um editor por projeto tira a edição da sua semana sem abrir vaga fixa — quer que eu defina o escopo e o teste prático?']"

**Porta 2 (contratar):**
"Vaga de **[função]** montada: gabarito com o par de indicadores **[volume] + [qualidade]**, anúncio em formato [carta de vendas/direto] com a faixa na metade alta (**US$ [X-Y]** — é o filtro nº 1 de qualidade), e o funil de 9 etapas com o teste prático de até 2h desenhado pro papel.
Regra de ritmo: com candidato excelente, o calendário comprime — teste no mesmo dia, oferta na mesma semana. Etapa pulada não é velocidade, é a origem do bad hire.
Publica o anúncio e me traz cada candidatura — eu trio, pontuo o teste contra o gabarito e te devolvo o ranking. E não fecha oferta sem a checagem de caixa: [status da checagem da 15]."

**Porta 3 (rodar):**
"Sistema de gestão montado pro seu time de **[N] pessoas**: KPIs por função com faixa verde/vermelha (alvo semanal = mensal ÷ 4,3), painel com dono único por número e a regra de ouro — **KPI perdido exige motivo + experimento**, nunca bronca. [Se tem editor: 'Seus editores agora têm hit rate individual — o sufixo no naming dos ads liga cada criativo ao autor, e a análise de ads (11) passa a ler isso sozinha.']
O ciclo: review mensal pros novos, trimestral pro time, 9-box duas vezes por ano — e a regra A/B sem exceção: quem não é A nem B derruba os outros.
Roda a primeira semana do painel e me volta com os números — a primeira calibragem de faixa é sempre a maior."

**Se faltar input crítico (qualquer porta):**
"Faltam [N] dado(s) que eu não posso inventar sem tornar a recomendação falsa: [listar — ex.: sua lista real de tarefas da semana, o salário que você paga hoje, o custo fixo da 15]. Cada um destrava: [o que destrava]. Me passa e eu fecho — decisão de gente com número chutado é como escalar ads com CAC inventado: a direção parece certa até a conta chegar."
