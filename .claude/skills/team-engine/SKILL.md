---
name: team-engine
description: Engine de time da marca, decide quando contratar (pela restrição real do negócio, nunca por desespero), como contratar (gabarito antes da vaga, funil de nove etapas, teste prático cronometrado, headhunting) e como rodar o time depois (onboarding de oito semanas, indicadores por função com taxa de acerto por editor, reviews com grade de nove caselas e plano de recuperação, incentivos por participação no excedente, organograma em motores e células, frameworks de decisão com dono único). Skill de consulta lateral pensada pro membro em estágio de escala; pra quem está começando ou validando, a resposta certa costuma ser "ainda não, sua restrição hoje é outra", e esta skill entrega exatamente essa resposta com o porquê. Lê o stage do manifest, aponta pra finance-engine quando a pergunta é se a folha cabe no caixa e separa funcionário de creator, que é território da creator-engine. Nunca recomenda vaga sem nomear o gargalo que ela remove e nunca estima salário nem diz que a folha cabe sem os números na mesa. Use quando o membro disser "contratar", "time", "equipe", "editor", "hiring", "org", "quem contratar", "delegar", "quem eu contrato primeiro", "meu time não performa", "preciso de um editor".
---

# Team Engine · Lateral · apelido antigo: 18 <!-- gen:title -->

## Quando usar

Quando a pergunta é sobre gente: contratar, delegar, montar estrutura, medir, pagar, promover ou desligar. Não é fase do pipeline, é consulta lateral como a `finance-engine`, com três momentos naturais: o membro virou o gargalo, existe vaga pra abrir, ou o time já existe e não performa. Foi desenhada pro membro em escala; pra quem está começando ou validando, a entrega mais valiosa costuma ser a resposta "ainda não" com o motivo. Não recruta creator nem monta programa de afiliado, que é da `creator-engine`, e não refaz o modelo financeiro, que é da `finance-engine`.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe (fonte de `stage`, `budget_daily` e `fixed_costs_monthly`) e `workspace/profile.md` existe. Faltando ou quebrado, escape ES1 ou ES2: (A) rodar a `setup`, ou (B) perguntar direto ao membro faturamento, gasto em ads e estágio, marcando `manifest.skipped_preflight`. Esta skill não tem pré-requisito de fase.
2. `report_language` do profile (default `pt-BR`) em todo output interno e na conversa. Exceção deliberada: o que o candidato lê sai no idioma do mercado onde o membro contrata. Pergunte uma vez e grave em `dados.json.hiring_language`.
3. Leia, se existirem, `finance-engine/dados.json` (a fonte da resposta sobre a folha), `ad-analysis/dados.json` (o volume real de criativo por trás da capacidade), `scale-engine/dados.json` e as rodadas anteriores em `team-engine/`, que continuam de onde pararam.

## Contexto a carregar

1. As cinco regras que não se negociam, em `reference/regras-inegociaveis.md`: contrata-se porque quer e nunca porque precisa; nenhuma vaga sem gargalo nomeado; sucesso definido antes da vaga aberta; três números nunca se inventam (salário real, caixa e custo fixo, indicador real de uma pessoa); creator não é funcionário.
2. Réguas compartilhadas: `member-stage-awareness.md` decide a apresentação, e o cânone `.claude/lib/unit-economics/README.md` §1, pela `finance-engine`, lembra que folha é custo fixo e custo fixo nunca se estima.
3. Base pelo índice (domínio principal `team-hiring-ops`, mais entradas vizinhas de `ops-scale-risk` e `scaling`): `python3 .claude/lib/kb-index/kb_lookup.py --skill team-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa (as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto); as listas por porta, com as queries exatas, estão em `reference/sistemas-porta-1.md`, `reference/sistemas-porta-2.md` e `reference/sistemas-porta-3.md`; antes de fechar cada etapa, releia a lista da porta e confirme que nada relevante ficou sem puxar; nunca query genérica nem busca repetida.

## Fluxo da skill

A skill roda por portas, decididas pela pergunta do membro e pelos dados, nunca por interrogatório. A tabela das portas está em `reference/portas-e-gate.md`: decidir (ETAPAs 1 a 4), contratar (ETAPA 1 mais 5 a 8) e rodar (ETAPA 1 mais 9 a 13). A ETAPA 1 roda sempre e a ETAPA 14 fecha sempre. Porta pulada não aparece no relatório, sem seção vazia e sem explicar o que não foi feito.

### ETAPA 1 · O gate, estágio e gargalo (roda sempre)

Leia `reference/portas-e-gate.md`. Duas perguntas antes de qualquer recomendação. Primeira: este membro está no estágio em que contratar resolve? A tabela por stage dá a leitura, e a única exceção fora de escala é o editor por projeto pra quem está validando e afogado em edição. Segunda: qual é o gargalo que uma contratação removeria? Nomeie a restrição em uma frase com dado, guiado pela pergunta de qual é o único gargalo que limita os próximos doze meses. Toda vaga referencia esse gargalo em `hiring_decision.constraint`. Grave `stage_check`.

### ETAPA 1.5 · A resposta "ainda não"

Mesmo arquivo. Não é recusa, é a entrega, em quatro partes: o gargalo real nomeado com o dado do workspace, por que contratar agora seria a decisão errada, o que fazer no lugar (a skill que ataca o gargalo) e o marco concreto que reabre a conversa.

### ETAPA 2 · [Porta 1] O tempo do fundador

Leia `reference/tempo-do-fundador.md`. Valor da hora, taxa de recompra, auditoria de tempo real (sem a lista do membro o resto fica em `pending_inputs[]`, nunca se inventa a agenda dele), classificação das tarefas nas quatro zonas e a regra de decisão: custo por hora do substituto abaixo da taxa de recompra manda delegar.

### ETAPA 3 · [Porta 1] Quem primeiro

Leia `reference/quem-primeiro.md`. Os quatro tipos de vaga com custo e prazo realista, a sequência de cima pra baixo, potencial contra habilidade pronta, o caso especial do creative strategist e a matemática que justifica publicar faixa acima do mercado.

### ETAPA 4 · [Porta 1] Montar dentro ou comprar fora

Leia `reference/dentro-ou-fora.md`. O modelo híbrido com as quatro camadas e os custos de referência, o que se terceiriza e o que nunca sai de dentro (a vantagem competitiva), o protocolo de seis passos pra contratar agência sem se queimar, e o fechamento da porta com um memo de decisão de uma página, com especificidade impiedosa.

### ETAPA 5 · [Porta 2] O gabarito da vaga antes do anúncio

Leia `reference/gabarito-da-vaga.md`. Nada vai ao ar antes disto: a descrição em card, com propósito amarrado a dinheiro, funções nucleares específicas e o par de indicadores sempre balanceado, e o gabarito em seis blocos que define e mede sucesso. Grave a convenção de sufixo por pessoa no naming dos ads em `dados.json.naming_suffix_by_person`, o handoff que permite à `ad-analysis` medir taxa de acerto por editor. Para função que já existe, rode antes a call de alinhamento com quem ocupa o papel.

### ETAPA 6 · [Porta 2] Anúncio e sourcing

Leia `reference/anuncio-e-sourcing.md`. Canais tratados como plataforma de anúncio, os dois formatos de texto, a faixa na metade alta como filtro número um e os qualificadores duros. Headhunting com vídeo curto personalizado é a rota principal pras vagas sênior, e quem é caçado passa por um funil diferente, com teste pago. Bounty pago a editor do time vive aqui; bounty externo é da `creator-engine`.

### ETAPA 7 · [Porta 2] O funil, o teste cronometrado e a oferta

Leia `reference/funil-e-oferta.md`. Nove etapas com decisão binária em cada uma. O teste prático é a etapa inegociável: no máximo duas horas, com tudo que a pessoa precisa, vídeo curto explicando o raciocínio, e o cronômetro valendo metade da nota. Critério rigoroso com calendário comprimido, porque talento bom fecha com o mercado em poucos dias. Oferta pela técnica das duas ofertas e rejeição em escada.

### ETAPA 8 · [Porta 2] Métricas do funil e a folha

Leia `reference/metricas-e-folha.md`. Grave tempo e custo de contratar, onde o funil perde candidato e o resultado de cada contratação por canal. A pergunta sobre a folha caber no caixa sai dos números da `finance-engine` ou do membro: some o custo mensal da vaga, leia resultado operacional, custo fixo e fôlego de caixa, e dê a leitura honesta. Sem o modelo, a resposta vira pergunta e entra em `pending_inputs[]`; dizer que cabe de sensação é proibido.

### ETAPA 9 · [Porta 3] Onboarding

Leia `reference/onboarding.md`. Integração técnica no dia zero, com o formulário de conhecer a pessoa alimentando a gestão o ano inteiro, e bootcamp de no máximo oito semanas em três fases, com QA regressivo que diminui por evidência e não por tempo de casa, cadência de reuniões decrescente, cheques de compreensão por aplicação e diagnóstico em duas semanas.

### ETAPA 10 · [Porta 3] Indicadores por função e o painel semanal

Leia `reference/kpis-e-painel.md`. A cascata de objetivo, estratégia e indicador, com as duas regras de ajuste e a proibição de mudar o objetivo. O painel semanal com fonte do dado, dono único, alvo semanal e indicadores antecedentes acima dos de resultado; indicador perdido exige motivo mais experimento do dono. A granularidade desce até o editor só quando o agregado piora.

### ETAPA 11 · [Porta 3] Organograma, playbooks e decisões

Leia `reference/org-e-decisoes.md`. A estrutura em quatro motores com a ordem de construção, organograma atual e futuro, teto de subordinados diretos, células por marca ou avatar, a transição de herói pra facilitador, o risco de pessoa única, os playbooks em sete blocos e os frameworks de decisão.

### ETAPA 12 · [Porta 3] Reviews, grade de nove caselas e desligamento

Leia `reference/reviews-e-desligamento.md`. A maior parte da baixa performance é expectativa mal definida, e o membro é corresponsável. Cadência de reviews em cima do gabarito com preenchimento duplo, review semestral com pesquisa de time e grade de desempenho por potencial, o plano de recuperação com dados e responsabilidade própria assumida, e os dois gatilhos de desligamento.

### ETAPA 13 · [Porta 3] Incentivos e promoções

Leia `reference/incentivos-e-promocoes.md`. Todo incentivo é simples, claro e alcançável. Participação no excedente com o alvo vindo da `finance-engine`, bônus por indicador deixando claro que bater o alvo é a expectativa do salário, percentual competitivo só pros melhores ads do mês, a escada de carreira, as sete alavancas de promoção e os três motores da motivação.

### ETAPA 14 · Checagens de sanidade

Leia `reference/sanity-checks.md`: os doze itens, do gargalo nomeado em toda vaga ao relatório sem seção vazia das portas não rodadas. Falha em qualquer um bloqueia o salvamento do `.md`.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/team-engine/`; `team-engine.md` nas quatorze seções do arquivo, na ordem das portas rodadas, `team-engine.html` por `python3 tools/render_report.py workspace/[produto]/team-engine/team-engine.md`, e `dados.json` no schema de `reference/dados-json.md` (quem lê o quê em `reference/contrato-de-leitura.md`). Manifest pelo script: `python3 tools/manifest.py <slug> complete team-engine` e `set team` com o resumo (tamanho do time, vagas abertas, se contratar é recomendado, o gargalo, folha mensal, risco de pessoa única e a data), nunca `manifest.stage` nem `manifest.fixed_costs_monthly`, mais `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft, lembrando que time é o artefato mais vivo do workspace e que a skill continua de onde parou: uma mensagem por porta, mais a da resposta "ainda não" e a de quando falta input crítico.
