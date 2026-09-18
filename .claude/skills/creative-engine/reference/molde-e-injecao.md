# Creative Engine · Referência: O molde do vídeo escalado e a injeção dos argumentos (ETAPA 5)

> Quando existe molde, como escolher um por conceito, a tabela de mapeamento slot a slot, o script que sai dela, a nota técnica das pendências, as três variações e a checagem antes de entregar. Abra no começo da ETAPA 5, antes de escrever o primeiro roteiro, junto com `reference/briefing.md`. O cânone do molde é `.claude/lib/ad-molds/README.md`.

### ETAPA 5 — Escrever o roteiro em cima de um esqueleto que já escala

A `competitor-analysis` pode ter extraído o molde de um vídeo que roda e paga a própria conta: a peça inteira cortada em slots, cada slot com o trabalho que faz na cabeça de quem assiste, o segundo em que entra e sai, o que a tela faz ali e quantas palavras couberam dentro. Com o molde em mão, o roteiro do briefing não nasce de uma estrutura montada do zero. Ele nasce em cima de um esqueleto que o mercado já premiou.

A regra que manda em tudo aqui é a do cânone: **o molde vem do concorrente, o conteúdo vem da Aura.** Estrutura e mecânica se modelam. Frase, afirmação, número e nome de mecanismo, não — copiar isso é plágio, e reprova o briefing.

#### 1. Quando existe molde

Leia o `competitor-analysis/dados.json`. O bloco `ad_molds` com `status` igual a `completed` e `molds_count` maior que zero significa que o arquivo `competitor-analysis/ad-molds.json` existe e tem molde dentro. Abra o arquivo e carregue junto os três vocabulários fechados de `.claude/lib/ad-molds/molds.json`, que são o que dá sentido a cada campo.

Sem o bloco, com `status` igual a `skipped` ou `no_timed_transcript`, ou com o arquivo ausente: a ETAPA 5 segue exatamente como hoje, com a estrutura de quatro seções de `reference/briefing.md`. Nada muda no briefing e nada se avisa ao membro.

O molde só serve a conceito de vídeo, porque o eixo dele é o tempo. Conceito de imagem, carrossel ou motion graphics sem fala segue sem molde, no mesmo batch, sem ressalva nenhuma.

#### 2. Seleção — um molde por conceito

Um conceito usa **um** molde. Dois moldes no mesmo conceito viram uma mistura de duas estruturas, que é exatamente o que o molde existe para evitar.

O encaixe se lê pela sequência de `function` do molde contra o trabalho que o conceito precisa fazer:

| O que o molde faz | O conceito que ele serve |
|---|---|
| Abre em `chamada_do_problema` e gasta tempo em `intensificacao_da_dor` | Problem Aware, abrindo em zona de incômodo ou de alerta |
| `nome_do_mecanismo` e `explicacao_do_mecanismo` ocupando a parte do meio | Solution Aware, ângulo da vertical interna |
| `prova` e `prova_social` dominando o hold | Conceito de prova social ou de autoridade |
| Abre em `quebra_de_padrao` ou `abertura_de_loop` | Curiosidade, topo de funil |
| `oferta` e `reversao_de_risco` longos no fim | Product Aware ou Most Aware, fundo de funil |

Molde e conceito que não se encaixam: o conceito sai sem molde, e os outros do batch seguem com o seu. Forçar um esqueleto de fundo de funil num conceito de topo entrega o ritmo certo fazendo o trabalho errado.

Com mais conceitos do que moldes, o mesmo molde pode servir a dois. Três roteiros com o mesmo ritmo só se sustentam quando os ângulos são mesmo distintos; havendo molde sobrando, use moldes diferentes.

Declare no briefing, em uma linha: o `mold_id`, o concorrente, o sinal de escala do `evidence` e a frase do encaixe.

#### 3. O pack 3-2-2 em cima de um molde só

O molde é do conceito, então os três criativos compartilham a mesma linha de slots. O que varia entre eles continua sendo só o que as hard rules mandam variar (ETAPA 4.5):

- **`sniper`:** as palavras mudam nos slots da seção `hook`. Do primeiro slot de bridge em diante, o texto dos três é o mesmo.
- **`marksman`:** mudam os slots de hook e os slots em que o ângulo aparece. O hold universal ocupa os mesmos slots, com o mesmo texto, nos três.

Em nenhum dos dois casos muda a contagem de slots, a ordem, a função ou a duração. Criativo com estrutura diferente é outro conceito, não a execução número dois.

#### 4. A tabela de mapeamento

Antes de escrever a primeira frase, monte a tabela. Uma linha por slot, na ordem do molde. A coluna do argumento diz **o que entra ali**, em uma linha; o texto final vem no passo seguinte.

| Slot | Função | Tempo | Imagem | Palavras | Argumento do membro | Origem |
|---|---|---|---|---|---|---|
| 1 | `chamada_de_avatar` | 0,0–1,8s | `rosto_em_close` | 5 | as mulheres que já tentaram magnésio e continuam acordando de madrugada | `market-research/dados.json` → `sub_avatars[sa-01].labels` |
| 2 | `chamada_do_problema` | 1,8–4,2s | `cena_do_problema` | 7 | acordar cansada mesmo depois de oito horas na cama | `market-research/dados.json` → `voc_top20[voc-003]` |
| 7 | `prova` | 14,0–18,5s | `prova_na_tela` | 13 | o número que sustenta a afirmação do slot 6 | `offer-builder/research-foundation.json` → `best_numbers` |

Ordem de preenchimento, para os slots de dono único caírem primeiro:

1. `nome_do_mecanismo`, `explicacao_do_mecanismo`, `oferta`, `reversao_de_risco` e `urgencia` → `offer-builder/dados.json` (`mechanism`, `pricing`, `offer_stack`, `guarantee`).
2. `prova` e `prova_social` → o banco de provas em `offer-builder/research-foundation.json` (`best_numbers`) e depoimentos reais.
3. `chamada_*`, `intensificacao_da_dor`, `causa_do_problema` e `beneficio_dimensionalizado` → `market-research/dados.json` (VOC, dores, desejos, sub-avatares).
4. `descredito_da_alternativa` e `diferenciacao` → `competitor-analysis/dados.json` (`gaps`, `alternative_solutions`, `validated_library`).
5. `objecao_antecipada` e `afirmacao_central` → `objections` da `market-research`, respondidas com o mecanismo da oferta.
6. `virada_pessoal` → a história do avatar declarado no cabeçalho do conceito.

A coluna Origem nomeia arquivo e campo, sempre. Slot cuja origem não dá para nomear é slot sem argumento: a célula fica vazia e ele vai para a nota técnica do item 6. **Nunca preencha com texto plausível escrito na hora** — é o item 5 do que reprova a injeção.

#### 5. Do slot ao script

O script sai da tabela, no formato segundo a segundo que a ETAPA 5 já usa (`reference/briefing.md`). O que muda é a régua dos beats: eles são os slots do molde, não os quatro blocos genéricos.

- Cada slot vira um beat com o tempo do molde: `[00:04-00:07] CAUSA DO PROBLEMA`. As quatro seções (HOOK, BRIDGE, HOLD, CTA) continuam agrupando os beats, porque cada valor de `function` já declara a seção a que pertence.
- **A duração alvo do criativo é o `duration_s` do molde.** O ritmo é o ativo que o molde entrega, e escolher outra duração descarta justamente o que se foi buscar ali.
- **O `words_budget` do slot é a régua mais apertada, e vence.** A tabela de palavras por duração da ETAPA 4.5.C continua valendo para o total falado. Dentro do slot, vale o orçamento dele: teto de 115%, e abaixo de 85% o slot entra na nota técnica.
- **O `sentence_type` é obrigação, não sugestão.** Pergunta retórica no molde sai pergunta retórica no roteiro; constatação pessoal sai em primeira pessoa.
- **Slot `sem_fala` não ganha fala.** O beat carrega só o visual e o texto na tela.
- **A imagem sai da `visual_function`**, escrita como a cena da marca do membro que faz aquele trabalho. `demonstracao_do_produto` vira o produto do membro sendo usado. A cena do concorrente não entra, e o molde não a guardou de propósito. Com `visual_function` em `null` (a mídia não abriu), o visual do beat é escolha da skill, como em qualquer briefing sem molde.
- **Rota A (IA):** quando o script estoura o limite do modelo e precisa de takes (ETAPA 5.7), o corte cai **na fronteira entre slots**, nunca no meio de um. A regra de hook e body em takes separados continua valendo.
- **Rota B (montagem):** cada slot é uma linha da tabela de timecode do EDL, com os segundos do molde.

#### 6. A nota técnica

Fecha o `concept-NN.md`, como seção **Pendências do molde**, e só existe quando há pendência. É relatório interno: nada dela entra na copy, em nenhuma forma (regra 8 do `CLAUDE.md`).

Uma linha por slot pendente, com três informações: o slot e a função, o que faltou, e o efeito de destravar.

> Slot 7 (`prova`): falta um número medido do produto para sustentar a afirmação do slot 6. Com o resultado em mãos, o slot passa de afirmação a evidência, que é o trabalho que ele faz no molde.

Entram na nota:

- Slot sem argumento equivalente na pesquisa.
- Slot de especificidade numérica sem número real do membro.
- Slot escrito abaixo de 85% do `words_budget`, que deixa buraco no ritmo.

Não entram: slot resolvido, o que foi tentado antes, nem o caminho até a versão final.

#### 7. As três variações

Conspiração, emocional e autoridade só saem quando o membro pede. As três mantêm a estrutura do molde inteira: mesma contagem, mesma ordem, mesma função, mesmo tipo de frase e mesma duração por slot. O que muda é a intensidade e o ângulo dentro de cada slot.

Elas não aumentam o batch. Se o membro quiser rodá-las, entram como as três execuções de um conceito `sniper` — mesmo ângulo, mesma estrutura, três temperaturas — e a capacidade de teste da ETAPA 2 continua sendo o teto.

#### Checagem antes de entregar o conceito

- A contagem de slots do roteiro é igual à do molde.
- A ordem é a do molde: nenhum slot reordenado, acrescentado ou removido.
- Cada slot mantém a `function` e o `sentence_type` do molde.
- Nenhum slot passa de 115% do `words_budget`, e os abaixo de 85% estão na nota técnica.
- Slot `sem_fala` continua sem fala.
- A duração alvo do criativo é o `duration_s` do molde.
- Toda palavra passou pelo filtro do `market_vocabulary`: zero termo de `words_absent[]`, nenhum termo saturado em hook ou headline.
- Nenhuma frase, afirmação, número ou nome de mecanismo do concorrente aparece na saída. A checagem é direta: abra o transcript em `competitor-analysis/creatives-inbox/transcripts/` e confirme que nenhuma linha do roteiro é aquele texto com as palavras trocadas.
- Todo slot preenchido tem origem nomeada na tabela, e todo slot vazio está na nota técnica.
