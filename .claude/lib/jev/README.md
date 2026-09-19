# Jev — a camada de decisão

> **ESTA CAMADA ESTÁ DESLIGADA. Nenhuma skill a chama, e nenhuma deve passar a chamar sem decisão explícita do membro.**
>
> Ela foi construída, medida duas vezes e documentada em setembro de 2026. Funciona, é segura com o corte de confiança, e **não muda nenhum resultado**: em 196 julgamentos medidos ela não pegou uma única coisa que o modelo de raciocínio tivesse deixado passar. O que ela compra é velocidade e custo dentro de etapas que o membro não vê, ao preço de cada membro precisar de conta na Vercel, chave, cartão e uma dependência de Node.
>
> A decisão de 19/09/2026 foi deixar pronta e desligada. As duas medições completas estão em `docs/historico/jev-2026-09/`.
>
> **O que faria a conta virar:** uma etapa nova com milhares de itens independentes, ou o modelo passar a ficar confiante também sobre presença (hoje só fica sobre ausência).

Camada opcional que tira do modelo de raciocínio as decisões que são **classificação, nota ou sim/não** sobre muitos itens, e deixa ele livre pro que só ele faz: entender, sintetizar e escrever.

## O que o Jev é, e o que ele não é

O Jev é um modelo que **não escreve**. Ele faz três coisas, e só:

| Primitivo | O que devolve | Quando usar |
|---|---|---|
| `choice` | uma opção de um conjunto **fechado** que você define, com a probabilidade de cada opção e a confiança | classificar em categoria que o framework já tem |
| `score` | um número **na escala que você define**: passe uma lista ordenada de critérios e a nota volta como posição nela, com a legenda | dar grau, força, saturação, prioridade |
| `boolean` | a probabilidade de um sim/não, de 0 a 1 | conferir item a item se uma condição vale |

Entrada é **só texto**. Nada de imagem, áudio ou vídeo. Quando a decisão depende de pixel, o Jev é cego: outro modelo transforma pixel em texto primeiro, e aí o Jev classifica o texto.

Várias perguntas cabem numa chamada só, avaliadas em paralelo e isoladas sobre o mesmo estado.

## A frase que engana

Dizem que o Jev "não alucina". Isso quer dizer **apenas** que a resposta sempre cabe no formato pedido: quatro opções entram, uma das quatro volta, sempre.

Não quer dizer que a opção está certa. **Uma nota perfeitamente válida pode estar perfeitamente errada**, e como não vem raciocínio junto, ninguém percebe olhando. Hoje quem põe o número é quem escreve o texto ao lado, então o disparate aparece. Terceirizando o número, ele para de aparecer. É por isso que existem as três regras duras abaixo.

## O que a medição na máquina já mostrou

Rodado em 19 de setembro de 2026, com chave real. Estes não são números de folheto:

**Sim/não não devolve confiança.** O campo de confiança volta vazio quando a pergunta é de sim/não; ele só aparece em escolha e em nota. **Para sim/não, o sinal é a própria probabilidade, e a certeza é a distância até 0,5.** Probabilidade 0,95 e probabilidade 0,05 são igualmente confiantes: uma diz sim com força, a outra diz não com força. Um corte que olhe só o lado de cima joga fora metade das respostas boas.

**A escala do sim/não é comprimida.** Casal perfeito não dá 0,95: numa página que literalmente diz "repairs the skin barrier in 14 days", perguntado sobre a dor correspondente, a resposta foi 0,74. É mais uma razão pra perguntar por nota com régua ordenada em vez de por sim/não.

**A resposta é estável.** A mesma pergunta repetida cinco vezes devolveu 0,47, 0,49, 0,49, 0,50 e 0,48. Variação de três centésimos. Isso é bom: dá pra comparar rodadas.

**Nota volta fracionária.** Uma régua de cinco critérios devolve algo como 3,29, que é a média ponderada da distribuição, mais a distribuição inteira por índice. Regra escrita sobre "nota 1 ou 2" tem de olhar a distribuição, não o arredondamento.

**É rápido.** De 450 a 800 milissegundos por chamada.

**O tier gratuito do gateway barra cedo.** Cinco chamadas passam, a sexta é recusada, e a recusa não melhora com pausa de quatro segundos entre elas. Lote grande no tier gratuito não termina: o cliente pausa, recua duas vezes e para o lote quando a cota acaba, devolvendo o que já respondeu e dizendo em que item parou. **Medição de cem casos precisa de crédito comprado, ou de rodar em pedaços ao longo do dia.**

**O estado precisa chegar limpo.** Texto cru de scraper é de 13% a 73% moldura: banner de cookie, carrinho, grade de produto, rodapé, letreiro repetido. Com a moldura junto, a confiança despenca a zero, porque metade do estado é ruído. Passe a página pelo `.claude/lib/web-fetch/reduzir.py` antes de montar o estado. Isso é degrau zero, e vale também pro modelo de raciocínio.

## A regra que mais muda o resultado: agrupar

**Uma chamada leva UM estado e MUITAS perguntas, e pergunta a mais custa quase nada.** Errar isso não degrada um pouco: degrada tudo.

Medido em 19 de setembro de 2026, a mesma matriz de 5 dores × 10 páginas, o mesmo material, as duas formas:

| | Chamadas | Tempo | Confiança mediana | Células acima de 0,85 |
|---|---|---|---|---|
| uma célula por chamada | 50 | 53 minutos no tier gratuito | 0,70 | 14 de 50 |
| **tudo numa chamada** | **1** | **1,15 segundo** | **0,90** | **30 de 50** |

A versão agrupada **dobrou a fatia utilizável** e resolveu a matriz inteira em pouco mais de um segundo, com 16.351 tokens de entrada. As 30 células de confiança alta ficaram todas dentro de um degrau do caminho de raciocínio: **30 de 30**.

Como montar, seguindo a documentação do modelo:

- **estado é objeto com campos nomeados**, não texto corrido. Array quando forem vários registros.
- **a pergunta cita o campo pelo caminho, entre crases**: ``Com que profundidade `paginas[3].texto` trata esta dor?``
- **o orçamento é de 32 mil tokens, compartilhado entre estado e perguntas.** Cabem 10 páginas reduzidas e 50 perguntas com folga.
- **agrupe em BLOCOS, não tudo de uma vez.** Um empate num item derruba a chamada inteira: 96 perguntas numa chamada falharam por causa de uma review que reclamava de entrega e de atendimento em pé de igualdade, e as 96 respostas se perderam. Em blocos de 24 passou. **Bloco que falha, quebre ao meio e tente de novo** — isso recupera tudo sem perder item.
- **só o contexto que aquelas perguntas precisam.** A documentação do modelo chama o excesso de "context rot", e a medição confirma: estado cru de scraper derruba a confiança a zero.

## A cascade, em quatro degraus

Mesmo padrão dos outros MCPs (`.claude/lib/mcp-detect/README.md`): existe, usa; não existe, desce um degrau em silêncio, sem avisar o membro e sem travar nada.

**Degrau zero, sempre primeiro.** O que é busca de texto ou conta roda antes e não depende de ninguém: filtro por nota de estrela, ordenação por tamanho, comparação de id, contagem de palavras, lista literal. É exato, é de graça e funciona sem internet. O Jev só entra no que sobra.

**Degrau um, confiança alta.** O valor é usado. A procedência fica no `dados.json` da fase, nunca no relatório que o membro lê, porque a regra de só resultado proíbe narrar como o documento foi feito.

**Degrau dois, confiança no meio.** O caso volta pro modelo de raciocínio decidir, com o texto na mão. **Isso é o valor da integração, não uma falha dela**: são poucos casos por rodada e costumam ser os mais valiosos.

**Degrau três, Jev indisponível.** Ele está em acesso antecipado, então **indisponível é o estado normal, não a exceção**. A etapa roda exatamente como roda hoje, em silêncio, sem uma linha pro membro e sem baixar nenhum mínimo de qualidade.

## As três regras duras

1. **O Jev nunca descarta sozinho.** Ele ordena e sinaliza. Quem elimina é a régua escrita na skill ou o modelo de raciocínio.
2. **Nenhum campo obrigatório de schema nasce por causa do Jev.** Campo de veredito obrigatório faz a skill quebrar toda vez que ele não responder.
3. **Chamada que falha no meio de um lote vira caso do meio**, nunca descarte por omissão. Item perdido por demora não pode virar item descartado.

## Os limites de corte

Medidos em 19 de setembro de 2026, sobre 50 células de matriz de lacunas rodadas pelos dois caminhos com o mesmo material. A confiança **prevê o acerto**, e a previsão é monotônica:

| Faixa de confiança | Erro médio na nota | Sim/não bate |
|---|---|---|
| 0,00 – 0,50 | 0,53 degrau | 7 de 10 |
| 0,50 – 0,70 | 0,41 degrau | 13 de 15 |
| 0,70 – 0,85 | 0,39 degrau | 11 de 11 |
| **0,85 – 1,00** | **0,18 degrau** | **14 de 14** |

Daí o corte:

- **confiança a partir de 0,85: a skill age sozinha.** Acerto de 14 em 14, nenhuma discordância de dois degraus, nenhuma lacuna real apagada.
- **abaixo de 0,85: o caso volta pro modelo de raciocínio.** São cerca de 70% das células, e é aí que mora o trabalho que importa.
- em escolha e nota a régua é a confiança; em sim/não, que não devolve confiança, é a distância da probabilidade até 0,5, contada dos dois lados. Fora da faixa de 0,1 a 0,9 o sim/não acertou 11 de 11, mas só 11 das 50 células chegaram lá — a nota com régua ordenada carrega mais informação, e é ela que deve ser perguntada.

## A coisa mais importante que a medição mostrou

**Ele fica confiante para dizer que NÃO está lá. Nunca para dizer que ESTÁ.**

Medido duas vezes, nas duas formulações: das 14 células de confiança alta da versão item a item, 14 eram de ausência; das 30 da versão agrupada, **30 eram de ausência e nenhuma de presença**. E a confiança alta se concentra na pergunta lexical: numa dor que se resolve por vocabulário, 9 das 10 células passaram de 0,85; nas dores de leitura fina, 1 de 10.

Isso redesenha o papel da camada. Ela **não classifica**: ela **elimina o óbvio ausente** e devolve o resto. Na versão agrupada, resolveu **30 das 50 células** com confiança alta, todas dentro de um degrau do caminho de raciocínio. O julgamento que decide oferta continua inteiro com o modelo de raciocínio.

Uma regra prática cai daí: **nunca pergunte ao Jev se algo está presente.** Pergunte se está ausente, e use só a resposta confiante.

## Chave: de cada membro, nunca compartilhada

O acesso é pelo AI Gateway da Vercel, modelo `typesafe-ai/jev`. Cada membro usa a **conta dele**, com a variável `AI_GATEWAY_API_KEY` na máquina dele, exatamente como já acontece com TrendTrack, Higgsfield e Notion.

**Chave compartilhada no repositório é proibida**, e não é regra nova: uma chave de acesso já vazou nesse repositório antes e foi removida. O guard de commit bloqueia segredo e o lint acusa. Quem não tem chave roda a Aura inteira, só sem esta camada.

## Como ligar, em dois comandos

Os dois rodam na máquina do membro, uma vez só:

```bash
cd tools && npm i
```

```bash
export AI_GATEWAY_API_KEY="a chave criada em vercel.com/dashboard, aba AI Gateway"
```

A segunda linha vale só pro terminal aberto. Pra valer sempre, ela entra no `~/.zshrc` (Mac) ou no `~/.bashrc` (Linux). Pra conferir que ficou de pé:

```bash
node tools/jev.mjs --check
```

Saída `0` com `"disponivel": true` é camada ligada. Saída `3` diz o que falta e **não é erro**: é o degrau três, e a Aura segue inteira sem ela.

## Medição 2: a triagem de reviews, e o número que decide

96 reviews negativas de 6 marcas, classificadas em quatro temas pelos dois caminhos. A etapa de maior volume do framework.

| | Chamadas | Tempo |
|---|---|---|
| Jev, em blocos de 24 | 4 | **3,01 segundos** |
| raciocínio, 6 agentes | 6 agentes | 159 segundos |

**A confiança separa o acerto do erro de forma limpa:** mediana de **0,93** nas concordâncias e de **0,54** nas discordâncias. Apenas 4 das 23 discordâncias ficaram acima de 0,85.

E o teste que importa, porque é o que decide negócio: sem corte, comparando saída crua contra saída crua, **uma marca de seis mudaria de veredito** — uma que devia ser eliminada por falta de eficácia passaria. As quatro reviews que causaram a virada tinham confiança de 0,43 · 0,36 · 0,61 · 0,22.

**Com o corte de 0,85 aplicado, os seis vereditos batem exatamente.** A camada resolve 54% das reviews e devolve o resto.

É a validação do desenho inteiro: o valor não está em confiar na resposta, está em confiar na confiança.

## O limite que nenhuma formulação mexeu

Em 196 julgamentos medidos, entre a matriz de lacunas e a triagem de reviews, **ele não pegou uma única coisa que o modelo de raciocínio tivesse deixado passar.** Concordância de 49 em 50 dentro de um degrau quer dizer que ele confirma, não que ele descobre.

O que a camada compra é **velocidade e custo**. Ela não compra pesquisa melhor. Quem esperar resposta mais fina vai se decepcionar; quem esperar a mesma resposta em um segundo, não.

## O que não passa pelo Jev

- **Copy do consumidor final não é filtrada por máquina.** Nada de caçar aviso, ressalva ou suavização. Em setembro de 2026 saíram da Aura o gate de compliance, as flags de não verificado e a lista de palavras proibidas sobre copy, de propósito (regra 8b do `CLAUDE.md`). Pôr um filtro de máquina no caminho da copy seria reverter essa decisão, não otimizar nada.
- **Dado financeiro não sai da máquina.** Extrato, faturamento e custo ficam onde estão. O gateway declara retenção zero e não treinar com o dado, e ainda assim o padrão aqui é não mandar.
- **Decisão que o membro precisa entender.** Onde o schema exige a evidência ao lado do rótulo, o Jev não serve: saber o rótulo não muda nada, saber a razão muda tudo.
- **O que um script já resolve.** Detecção de bloqueio de página, validação de enum e mapeamento de campo fixo já são exatos hoje, sem modelo nenhum.
