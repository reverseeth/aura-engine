# Jev — a camada de decisão

Camada opcional que tira do modelo de raciocínio as decisões que são **classificação, nota ou sim/não** sobre muitos itens, e deixa ele livre pro que só ele faz: entender, sintetizar e escrever.

## O que o Jev é, e o que ele não é

O Jev é um modelo que **não escreve**. Ele faz três coisas, e só:

| Primitivo | O que devolve | Quando usar |
|---|---|---|
| `choice` | uma opção de um conjunto **fechado** que você define, com a probabilidade de cada opção e a confiança | classificar em categoria que o framework já tem |
| `score` | um número **na escala que você define**: passe uma lista ordenada de critérios e a nota volta como posição nela, com a legenda | dar grau, força, saturação, prioridade |
| `noul` | a probabilidade de um sim/não, de 0 a 1 | conferir item a item se uma condição vale |

Entrada é **só texto**. Nada de imagem, áudio ou vídeo. Quando a decisão depende de pixel, o Jev é cego: outro modelo transforma pixel em texto primeiro, e aí o Jev classifica o texto.

Várias perguntas cabem numa chamada só, avaliadas em paralelo e isoladas sobre o mesmo estado.

## A frase que engana

Dizem que o Jev "não alucina". Isso quer dizer **apenas** que a resposta sempre cabe no formato pedido: quatro opções entram, uma das quatro volta, sempre.

Não quer dizer que a opção está certa. **Uma nota perfeitamente válida pode estar perfeitamente errada**, e como não vem raciocínio junto, ninguém percebe olhando. Hoje quem põe o número é quem escreve o texto ao lado, então o disparate aparece. Terceirizando o número, ele para de aparecer. É por isso que existem as três regras duras abaixo.

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

Ficam em `perguntas.json`, por aplicação, porque a régua certa depende do custo do erro. O padrão, enquanto não houver medição:

- acima de **0,90** a skill age sozinha
- entre **0,65 e 0,90** o caso volta pro modelo de raciocínio
- abaixo de **0,65** o caso sobe pro membro, quando a decisão é de negócio

**Nenhum desses números vale antes da medição em espelho.** Rode a aplicação pelos dois caminhos com o mesmo material, confira na mão os casos de confiança alta, e veja se a taxa de acerto bate com a probabilidade que ele deu. Sem isso, qualquer corte é palpite com cara de medida.

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

## O que não passa pelo Jev

- **Copy do consumidor final não é filtrada por máquina.** Nada de caçar aviso, ressalva ou suavização. Em setembro de 2026 saíram da Aura o gate de compliance, as flags de não verificado e a lista de palavras proibidas sobre copy, de propósito (regra 8b do `CLAUDE.md`). Pôr um filtro de máquina no caminho da copy seria reverter essa decisão, não otimizar nada.
- **Dado financeiro não sai da máquina.** Extrato, faturamento e custo ficam onde estão. O gateway declara retenção zero e não treinar com o dado, e ainda assim o padrão aqui é não mandar.
- **Decisão que o membro precisa entender.** Onde o schema exige a evidência ao lado do rótulo, o Jev não serve: saber o rótulo não muda nada, saber a razão muda tudo.
- **O que um script já resolve.** Detecção de bloqueio de página, validação de enum e mapeamento de campo fixo já são exatos hoje, sem modelo nenhum.
