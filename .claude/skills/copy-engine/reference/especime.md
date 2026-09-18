# Copy Engine · Referência: Seleção de espécime, swipe modeling (ETAPA 2.5)

> A seleção do espécime primário em `.claude/lib/swipe-models/specimens.json` com a precedência do seletor e a `regra_diagnostica` (2.5A), a anatomia puxada da base com a régua dos 11 blocos (2.5B), a tabela de blocos e os 4 a 6 pilares da peça (2.5C), o scaffold universal de lead do Makepeace (2.5D), a regra de modelar estrutura e nunca conteúdo e os campos gravados no `dados.json`. Abra na ETAPA 2.5.

### ETAPA 2.5 — Seleção de Espécime (Swipe Modeling) — OBRIGATÓRIA

> Frameworks dizem O QUE fazer. Espécime mostra COMO uma peça que já converteu foi montada, bloco a bloco. Copywriter de verdade não escreve só com framework na mesa — ele escolhe a peça provada mais próxima e modela a estrutura. Esta etapa faz isso explicitamente, antes de escrever qualquer linha.

**2.5A — Selecionar o espécime primário.**

Leia `.claude/lib/swipe-models/specimens.json`. Cruze o seletor de cada espécime (`aplica_a`: `page_type` × `dominant_awareness` × `sophistication_stage` × `product_vertical`) com as decisões que a ETAPA 2 já tomou. Precedência: `page_type` restringe primeiro; depois awareness; `sophistication` desempata (4-5 empurra pra espécimes de identidade/mecanismo); vertical só refina. O eixo `page_type` do catálogo tem quatro valores e a `page-design` trabalha com seis: a correspondência fixa (`listicle` como `advertorial`, `pdp_robust` e `pdp_lean` como `pdp`, `quiz` sem espécime) está no `.claude/lib/swipe-models/README.md`.

Leia a `regra_diagnostica` do candidato antes de fechar — ela existe pra vetar escolha errada (ex.: Identity Lead só serve estágio 4-5; discovery story exige evento dramático real ou defensável, senão use problem-agitation em vez de fabricar história).

Escolha **1 espécime primário**. Opcionalmente **1 secundário**, só quando houver um bloco específico que o primário não resolve bem (ex.: primário = advertorial de 7 seções, secundário = escada de prova em 3 degraus do chassi de VSL).

**2.5B — Puxar a anatomia.**

Rode `search_knowledge` com a `best_query` do espécime escolhido (e do secundário, se houver). Rode também a régua medida da base: **Anatomia da Promo — 11 blocos, presença medida em 179 promos** (rode `11 blocos promo Agora kicker saudacao qualificada mecanismo batizado presenca medida`) — a frequência real de cada bloco (kicker, saudação qualificada, big idea narrativa, mecanismo batizado) calibra o modelo estrutural contra o que as peças que converteram de fato fazem. Extraia:
- a **sequência de blocos** da peça, em ordem
- **que trabalho cada bloco faz** (não o texto dele)
- a **regra diagnóstica** que a nota documenta

Se a query não retornar a anatomia, escolha o próximo espécime aplicável e registre o fato — escrever sem modelo é o comportamento antigo, e é o que esta etapa existe pra evitar.

**2.5C — Montar o modelo estrutural.**

Antes de escrever, produza a tabela de blocos que a copy vai seguir:

| # | Bloco (do espécime) | Trabalho que faz | O que entra aqui (do research do membro) |
|---|---|---|---|

Preencha a última coluna com o material real das skills `market-research`/`competitor-analysis`/`offer-builder` — VOC, mecanismo, prova, objeções, oferta. **É essa tabela que vira a copy nas ETAPAs 3-5**, não o espécime.

Declare também os **4-6 pilares** da peça (leia `arquitetura_de_extensao` no mesmo JSON). Copy longa que funciona não é muito conteúdo — é um número pequeno de ideias reapresentadas, onde o que muda a cada volta é a **prova**, nunca a ideia. Cada bloco de corpo deve marcar qual pilar reforça e com que prova nova. Isso alimenta a dieta do sweep 4.5: pilar que volta **sem** prova nova é gordura; pilar que volta **com** prova nova é a arquitetura funcionando.

**2.5D — Aplicar o scaffold universal de lead.**

Independente do espécime escolhido, o lead precisa cumprir os 4 passos do Makepeace (rode `grab eyeballs expand headline establish credibility bribe esqueleto de abertura`): grab eyeballs (ideal prospect + big promise + curiosidade) → expand headline → establish cred → bribe. É a segunda camada sobre o espécime primário; lead que não cumpre os 4 passos não está pronto.

> **REGRA INEGOCIÁVEL — modelar estrutura, nunca conteúdo.** Não copie frase, claim, número ou nome de mecanismo do espécime — é plágio. O que se extrai é arquitetura: ordem dos blocos, trabalho de cada um, e por que funciona.

Registre no `dados.json`: `specimen_primary` (id), `specimen_secondary` (id ou null), e `specimen_block_map` (a tabela 2.5C). A skill `ad-analysis` usa isso pra diagnosticar depois se a estrutura escolhida foi a certa pro avatar.
