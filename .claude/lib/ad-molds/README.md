# Ad Molds — o molde do vídeo escalado, slot a slot

Camada que faz a skill `creative-engine` **escrever o roteiro em cima do esqueleto de um vídeo que já escala**, em vez de montar a estrutura do zero a cada briefing. É o equivalente em vídeo do que o `.claude/lib/swipe-models/` faz com página.

## O problema que resolve

A skill `competitor-analysis` já transcreve os criativos escalados dos concorrentes com marcação de tempo por palavra, e já separa cada um em hook, bridge, hold e CTA.

O que ela produz com isso é estatística. O `creative-patterns.json` guarda quantos por cento dos criativos abrem com rosto em close, que afirmações se repetem, que durações concentram os escalados. Isso responde "o mercado costuma abrir assim". Não responde "este vídeo, que roda há noventa dias, faz isto, nesta ordem, nestes segundos".

Hook (a abertura que para o dedo), bridge (a ponte que leva da abertura ao problema), hold (o corpo, onde o mecanismo e a prova aparecem) e CTA (o fechamento com a oferta) são quatro baldes grossos. Dentro deles, um vídeo de trinta segundos faz de oito a quatorze trabalhos diferentes com a cabeça de quem assiste. O molde é o mapa desses trabalhos.

## A regra inegociável

**Modelar ESTRUTURA e MECÂNICA. Nunca conteúdo.**

Copiar frase, afirmação, número ou nome de mecanismo do concorrente é plágio. O que se extrai é a arquitetura: em que ordem os blocos vêm, que trabalho cada um faz na cabeça de quem assiste, e quanto tempo cada um ocupa.

Por isso nenhum arquivo de molde guarda o texto falado pelo concorrente. A fala continua no transcript, que já existe. O molde guarda a função.

## O que é um slot

Slot é uma unidade funcional: um trecho do vídeo com uma função psicológica própria. Não é parágrafo, não é frase.

Uma frase isolada é um slot quando faz um trabalho distinto do que a frase anterior fez. Duas frases que fazem o mesmo trabalho são um slot só. Um vídeo de trinta segundos costuma ter de oito a quatorze slots.

## Os três eixos

Um molde de página tem um eixo: a ordem dos blocos de texto. Um molde de vídeo tem três, e é isso que separa os dois.

**Fala.** O que é dito no slot, registrado como função psicológica (`function`) e como tipo de frase (`sentence_type`). "Aqui o mecanismo é batizado" é função. "Aqui ele diz o nome tal" é conteúdo, e conteúdo não entra.

**Tempo.** Entrada e saída em segundos (`t_in`, `t_out`), vindas da transcrição cronometrada. O ritmo do molde é o ritmo em segundos, não a contagem de palavras: um slot de dois segundos e meio continua sendo de dois segundos e meio quando o argumento muda de mercado.

**Imagem.** O que a tela faz durante o slot (`visual_function`), sempre como função. "Rosto em close" e "demonstração do produto" são funções. "A moça de blusa azul na cozinha dela" é a cena do concorrente, e cena do concorrente não entra.

## A injeção

Injeção é o momento em que os argumentos do membro entram no esqueleto. Ela tem três listas, e as três valem ao mesmo tempo.

### O que não pode mudar

| Item | Por quê |
|---|---|
| A função psicológica de cada slot | É o trabalho que aquele segundo do vídeo faz; trocar a função é trocar o molde |
| A posição na sequência | A ordem é o que segura a atenção de um slot ao seguinte |
| A contagem de slots | Molde de onze slots vira roteiro de onze slots |
| O tipo de frase | Pergunta retórica que vira afirmação muda a relação com quem assiste |
| A duração aproximada de cada slot | O ritmo é o ativo; ele veio medido, não estimado |

### O que tem de mudar

Os argumentos, as provas, o nicho, o vocabulário e as referências culturais. Tudo isso é conteúdo, e conteúdo é do membro.

A especificidade numérica é preservada **como especificidade**, com o número trocado pelo número real do membro. Se o slot do molde carrega um número exato, o slot injetado carrega um número exato. Se o membro não tem número para aquele slot, o slot vira pendência nomeada na nota técnica, nunca um número inventado.

### O que reprova a injeção

Cada item abaixo é erro, não estilo:

1. Trocar palavra por sinônimo e chamar isso de adaptação.
2. Reordenar slots.
3. Acrescentar ou remover slot.
4. Suavizar a copy.
5. Inventar fato, mecanismo ou prova que não esteja na pesquisa do membro.
6. Escrever num slot mais palavras do que cabem na duração dele.

O item 6 é o que só existe em vídeo. Num molde de página, texto a mais alonga a página. Num molde de vídeo, texto a mais atropela o slot seguinte e destrói o ritmo que fez o vídeo escalar.

## De onde vêm os argumentos

**O molde vem do concorrente. O conteúdo vem da Aura.** Por slot, a origem é sempre um destes:

| Origem | O que ela dá |
|---|---|
| `market-research` | Dores, desejos, vocabulário do mercado, sub-avatares |
| `competitor-analysis` | Buracos do mercado e a biblioteca de mecanismos e ângulos com evidência de escala |
| `offer-builder` | Mecanismo nomeado, promessa, garantia, stack de valor |
| Banco de provas | Estudo, número, depoimento, demonstração |

Slot sem argumento equivalente na pesquisa **vira pendência nomeada**, com o nome do que faltou. Nunca vira texto plausível escrito na hora.

## O orçamento de palavras

Cada slot carrega um `words_budget`: quantas palavras couberam ali no vídeo original, contadas na transcrição cronometrada. É um número, não um texto, então ele não carrega conteúdo do concorrente.

- **Teto:** o slot injetado fica em até 115% do orçamento. Acima disso, reprova pelo item 6.
- **Piso:** abaixo de 85% do orçamento, o slot deixa um buraco no ritmo. Não reprova, mas entra na nota técnica.
- **Slot sem fala:** orçamento zero e tipo de frase `sem_fala`. O trabalho ali é todo da imagem.
- **Referência de leitura:** fala de anúncio em inglês corre perto de duas palavras e meia a três por segundo. Um slot de quatro segundos com orçamento de trinta palavras não é um slot normal, é sinal de erro na marcação de tempo.

## Os arquivos

| Arquivo | O que guarda |
|---|---|
| `.claude/lib/ad-molds/molds.json` | O cânone: schema do molde, os três vocabulários controlados e as regras de injeção em forma legível por máquina |
| `.claude/lib/ad-molds/README.md` | Este arquivo, a versão humana das mesmas regras |
| `workspace/[produto]/competitor-analysis/ad-molds.json` | Os moldes extraídos de verdade, um por vídeo, no schema do cânone |

Os moldes extraídos são pesquisa do membro: nomeiam concorrente, anúncio e nicho. Por isso vivem no workspace do produto e nunca no framework, como manda a regra 11 do `CLAUDE.md`.

## O vocabulário

As três listas fechadas vivem no `molds.json`, cada valor com a descrição do trabalho que ele nomeia.

- **`function`** — a função psicológica do slot. Vinte e um valores, agrupados pelas quatro seções da anatomia de vídeo que a Aura já usa (hook, bridge, hold e CTA), com o ciclo objeção, afirmação, prova e benefício aberto em slots próprios dentro do hold.
- **`sentence_type`** — o tipo de frase. Seis valores.
- **`visual_function`** — o que a tela faz. Dez valores, mais `null` para quando a mídia não abriu.

Valor fora da lista significa slot mal classificado. Antes de inventar um valor novo, confira se o trabalho daquele slot não é um dos que já existem com outro nome.

## Manutenção

O vocabulário cresce quando um molde real não couber nele, nunca por antecipação. Valor novo entra no `molds.json` com descrição no mesmo formato dos existentes, e o número citado na seção acima é atualizado junto.

A classificação de hook aqui não substitui o `.claude/lib/hook-taxonomy/archetypes.json`: aquele catálogo diz **que tipo de hook** é, e o molde diz **quanto tempo o hook ocupa e o que vem depois dele**. Os dois se usam juntos.
