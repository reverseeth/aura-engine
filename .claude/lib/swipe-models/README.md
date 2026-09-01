# Swipe Models — modelagem por espécime

Camada que faz a skill 06 (copy engine) **modelar contra uma peça real que já converteu** antes de escrever, em vez de escrever só a partir de frameworks teóricos.

## O problema que resolve

O `kb-index` entrega **frameworks** — o que fazer (Caples, Schwartz, Cialdini, Hopkins). Isso é necessário e não muda. Mas nenhum copywriter de verdade escreve só com framework na mesa: ele escolhe a peça provada mais próxima do caso dele e **modela a estrutura** — a sequência de blocos, onde entra prova, onde entra credencial, onde o mecanismo é batizado, como a ponte pro preço é feita.

Até 2026-09-01 a skill 06 não tinha essa etapa. Ela decidia estratégia (ETAPA 2) e ia direto pra headline (ETAPA 3), sem nunca olhar como uma peça vencedora do mesmo tipo foi montada.

## Como funciona

`specimens.json` cataloga **12 espécimes estruturais** extraídos de swipe files reais (1.338 peças mineradas: Chris Haddad, arquivo Agora/Empiricus, Schwartz, Halbert, Lampropoulos, Makepeace, Clemens, Georgi, Milligan), cada um com:

- **`aplica_a`** — o seletor: `page_type` × `awareness` × `sophistication` × `vertical`
- **`best_query`** — a query exata pra puxar a anatomia completa da base
- **`regra_diagnostica`** — quando esse espécime é a escolha certa, e quando não é
- **`blocos_chave`** — a sequência que a copy deve seguir
- **`base_empirica`** — de quantas peças aquele padrão foi medido (honestidade sobre a força da evidência)

A skill 06 seleciona **1 espécime primário** e, opcionalmente, **1 secundário** pra emprestar um bloco específico (ex.: primário = advertorial de 7 seções da masterclass interna, secundário = escada de prova do chassi Haddad).

## A regra inegociável

**Modelar ESTRUTURA e MECÂNICA. Nunca conteúdo.**

Copiar frase, claim, número ou nome de mecanismo de um espécime é plágio e — no vertical de suplementos, onde boa parte do arquivo é pré-política atual do Meta — é também risco de compliance. Os espécimes de health carregam disease claims que hoje reprovam no gate. O que se extrai é a arquitetura: em que ordem os blocos vêm, que trabalho cada um faz, e por que funciona.

## A auditoria (sweep 9 da ETAPA 6)

O nó `auditoria` do JSON transforma o método de markup do Kyle Milligan numa rubrica de QA reproduzível — as 5 camadas (estrutura+4 U's, 4 emoções, lead de 4 passos, psicologia, oferta/preço), o loop `Objection → Claim → Proof (3x) → Benefit` rastreado parágrafo a parágrafo, e a folha de 12 defeitos recorrentes com o nome que o próprio auditor usa.

A regra de veredito é dura de propósito: **se a headline reprova em 3 dos 4 U's e falha em ideal prospect ou big promise, não vale auditar o corpo — reescreve o lead antes.** No arquivo original, o auditor abandona a anotação na página 4 de 21 quando isso acontece; o abandono é o veredito.

## Manutenção

Quando novos swipe files forem minerados e virarem notas na base, acrescente o espécime aqui com o mesmo shape. O campo `nota_kb` precisa bater com o título exato da nota (as 12 entradas atuais foram verificadas contra a base em 2026-09-01) — `best_query` que não resolve significa espécime sem anatomia, e a skill escreve sem modelo.
