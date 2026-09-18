# Page Design · Referência: A régua de design (sub-etapa 3.7)

> O padrão de design que a página tem que atingir nas três rotas, em cinco blocos de itens com teste objetivo: tipografia, ritmo e espaço, cor, movimento e os sinais de "feito por IA" que reprovam. Serve de direção ANTES de desenhar e de placar DEPOIS, dentro do self-review visual da 3.7. É bloqueante: página com item reprovado não vai ao membro.

## Como esta régua é usada

Dois momentos, o mesmo arquivo:

1. **Antes de desenhar** (rota 1, e o passo de unificação das rotas 2 e 3): os números daqui são a direção. Escala, grade de espaço, uso da cor e movimento já nascem certos, em vez de virarem correção depois.
2. **Depois de gerar o `design/page.html`**: o self-review visual da 3.7 preenche o placar, item a item, lendo o arquivo e os dois screenshots.

**Como pontuar:**

- Cada item tem um teste com resposta objetiva. Ou o arquivo tem o valor, ou não tem. Ou o screenshot mostra, ou não mostra. Nada de "ficou bom".
- O placar é uma linha por item: o id do item, o veredicto (passa ou reprova) e a evidência, que é o valor lido no CSS ou o que apareceu no print, com a seção onde apareceu. Item sem evidência conta como reprovado, porque não foi conferido.
- **Item de arquivo** confere no `design/page.html`, pelos comandos de cada bloco. **Item de print** confere nos screenshots de 1440 e de 390 que o self-review já capturou.
- Qualquer reprova bloqueia o checkpoint. Corrija inline e refaça o placar INTEIRO, porque a correção de um item costuma quebrar outro (subir o respiro entre seções mexe no ritmo, trocar o peso do título mexe na hierarquia).
- **Teto de 3 rodadas de correção.** O que continuar reprovado na terceira vai pro membro no checkpoint, em uma linha por item: o que está errado, o que você tentou e o que depende dele. Essas rodadas são silenciosas e acontecem ANTES de ele ver a página; não se confundem com as 3 iterações COM o membro que a 3.7 governa depois.
- O placar não vira arquivo. Ele existe pra decidir se a página passa, e o que sobrevive à terceira rodada é dito ao membro em uma linha.
- **Com duas versões da mesma página** (a segunda opinião da sub-etapa 3.8, `reference/brief-codex.md`), o placar é este mesmo, com uma coluna por versão e os mesmos ids. A comparação não muda nenhum item nem inventa critério novo: quem decide é a contagem de reprovas, e o desempate está escrito lá.

Os comandos abaixo rodam de dentro de `workspace/[produto]/page/`.

## Bloco T — Tipografia

**T1 · Escala modular declarada.** Os tamanhos de fonte saem de uma escala com razão única, 1.25 ou 1.333, declarada em custom properties no `:root` (`--step-1`, `--step0`, `--step1`...). Todo `font-size` da página é uma dessas variáveis, ou um `clamp()` cujos dois extremos são degraus da escala. No máximo 7 tamanhos distintos na página inteira.

```bash
grep -o 'font-size:[^;]*' design/page.html | sort -u        # cada valor é um degrau da escala
```

**T2 · No máximo duas famílias.** A regra é da sub-etapa 2.1 e aqui só se confere que a página obedece: no máximo dois valores distintos de `font-family` (ignorando a pilha de fallback), e eles são os da ETAPA 2. Uma família só é o normal, com a hierarquia vindo do peso.

```bash
grep -o 'font-family:[^;]*' design/page.html | sort -u
```

**T3 · Contraste de peso real entre título e corpo.** A diferença de `font-weight` entre os títulos e o corpo é de pelo menos 200 (corpo em 400 com título em 600 ou 700, por exemplo). Se a família tem um peso só, o contraste vem de dois degraus de escala no tamanho mais uma diferença clara de entrelinha, e isso fica escrito na evidência. Título e corpo no mesmo peso e a um degrau de distância reprovam: a hierarquia some na leitura de relance.

**T4 · Medida de linha entre 45 e 75 caracteres.** Todo bloco de texto corrido tem `max-width` entre `45ch` e `75ch` (ou o equivalente em rem). Confira também no print de 1440: conte os caracteres de uma linha cheia do parágrafo mais largo. Texto atravessando a tela inteira reprova, mesmo com o `max-width` declarado, porque em geral o contêiner está sobrescrevendo.

**T5 · Entrelinha proporcional ao tamanho.** Quanto maior o texto, menor a entrelinha. Corpo entre 1.5 e 1.7; subtítulos entre 1.3 e 1.45; títulos grandes entre 1.05 e 1.25. `line-height: 1.5` num h1 reprova, e corpo abaixo de 1.4 também.

**T6 · Caixa alta só em rótulo curto.** Texto em maiúsculas aparece só em eyebrow, rótulo e microcopy de botão, com no máximo cinco palavras e com `letter-spacing` positivo (entre 0.04em e 0.12em). Parágrafo, headline ou item de lista em caixa alta reprovam.

## Bloco E — Ritmo e espaço

**E1 · Uma grade de espaçamento, base 4 ou 8, sem exceção.** Todo `padding`, `margin` e `gap` é múltiplo da base, declarado como token no `:root` e usado pela variável. Valor solto fora da grade reprova, com duas exceções que não precisam de justificativa: borda de 1px e centralização por `auto`.

```bash
grep -oE '(padding|margin|gap)[^:]*:[^;]*' design/page.html | sort -u
```

**E2 · O respiro entre seções é maior que o respiro dentro delas.** O `padding-block` da section vale pelo menos duas vezes o maior `gap` interno dela. No print de 1440, a distância entre a última linha de uma seção e o título da seguinte é visivelmente maior que a distância entre esse título e o parágrafo dele. Se a página parece um texto corrido sem divisão, é este item que está reprovado. Referência de respiro no desktop: 5 a 8rem de `padding-block` no hero e na oferta, menos nas seções de apoio, e no celular a metade disso, porque a tela já é estreita e o mesmo valor come a página inteira.

**E3 · Proximidade dentro do bloco.** Cada elemento fica mais perto do que ele pertence do que do vizinho: rótulo colado no dado que descreve, legenda colada na imagem, título mais perto do próprio parágrafo do que do parágrafo anterior. Confere no print.

**E4 · Alinhamento óptico nos blocos com ícone.** O ícone alinha pelo centro óptico da primeira linha do texto, não pelo topo da caixa, e o texto de todos os itens da lista começa na mesma coluna (grade de duas colunas, largura fixa na coluna do ícone). Ícone flutuando acima ou abaixo da linha reprova. Confere no print, ampliando a lista.

**E5 · Margem lateral constante no celular.** O mesmo gutter do topo ao rodapé, entre 16px e 24px, e nada encostando na borda em 390. Zero rolagem horizontal: a largura de rolagem é igual à largura visível.

## Bloco C — Cor

**C1 · A paleta é a da ETAPA 2, por role.** Toda cor usada vem de uma variável de role (`background`, `surface`, `foreground`, `primary`, `on_primary`, `accent`, `muted`, `border`). Hex solto no CSS, fora do bloco onde os roles são declarados, reprova. Cor inventada no meio da página é o caminho mais rápido pra página parecer de outro produto.

```bash
grep -nE '#[0-9a-fA-F]{3,8}' design/page.html   # hex só na linha onde os roles são declarados
```

**C2 · Cor com significado.** O `primary` marca uma classe de coisa só, e a mais importante: a ação. Nenhum elemento não clicável usa a cor do botão principal. O `accent` marca o que a página quer que seja lido primeiro em cada seção (um número de prova, uma palavra da headline, um selo), no máximo um por seção. Cor forte espalhada em três papéis diferentes virou decoração e reprova.

**C3 · Zero gradiente decorativo.** Gradiente só entra com função declarada na evidência: escurecer uma foto pra o texto ficar legível, ou separar duas seções que dividem o mesmo fundo. Gradiente de duas cores de marca no hero "porque preenche" reprova.

```bash
grep -c 'gradient(' design/page.html                        # cada ocorrência tem função declarada
```

**C4 · Estado de foco visível.** Todo elemento clicável tem `:focus-visible` com contorno de pelo menos 2px, afastado do elemento, e com contraste de pelo menos 3:1 contra o fundo ao lado. `outline: none` sem substituto reprova.

**C5 · A cor não é o único sinal.** Nenhuma informação depende só da cor pra ser entendida (o item selecionado do seletor de pacote tem borda ou marca, além da cor; o preço riscado tem o risco, além do tom apagado).

## Bloco M — Movimento

O contrato do `page.html` é **zero JavaScript**. Todo movimento aqui é CSS.

**M1 · Movimento só na entrada da seção.** Uma animação por seção, de opacidade 0 até 1 com deslocamento curto, entre 8px e 24px, sempre na mesma direção na página inteira. Nada mais se mexe sozinho.

**M2 · Duração entre 200ms e 600ms, com saída suave.** A curva desacelera no fim (`ease-out` ou uma `cubic-bezier` equivalente). `linear` e `ease-in-out` longo reprovam numa entrada: fazem o elemento parecer que escorrega.

```bash
grep -oE 'animation[^;]*|transition[^;]*' design/page.html | sort -u
```

**M3 · Atraso escalonado entre irmãos.** Cartões da mesma fileira entram em sequência, com 40ms a 120ms de diferença entre um e o seguinte, e no máximo cinco degraus. Sem teto, o sexto cartão espera meio segundo e a página parece travada.

**M4 · Rolagem sem script, e nunca às custas do conteúdo.** Animação disparada pela rolagem usa `animation-timeline: view()` dentro de `@supports (animation-timeline: view())`, e o estado inicial (a opacidade zerada e o deslocamento) é declarado **só dentro** desse bloco. Em navegador sem suporte, a seção nasce visível e parada. Estado inicial fora do `@supports` reprova, porque é assim que a página inteira fica invisível pra quem não tem suporte.

**M5 · `prefers-reduced-motion: reduce` desliga tudo, e vem por último.** Dentro dessa media query, as animações e transições vão a zero e o conteúdo fica no estado FINAL, visível. Nunca no inicial. E o bloco fica DEPOIS do `@supports` do M4 na folha de estilo: os dois têm a mesma especificidade, então o último vence. Invertido, quem pediu menos movimento recebe a seção com opacidade zero e nunca vê o conteúdo. Confere pela ordem em que os dois blocos aparecem no `<style>`.

**M6 · Zero animação em laço.** Nada pisca, pulsa, gira ou repete enquanto a pessoa lê. Marquee, contador animado e seta saltitante reprovam.

**M7 · Só `opacity` e `transform` são animados.** Animar `height`, `top`, `margin` ou `width` reprova, porque recalcula o layout a cada quadro e engasga no celular.

## Bloco S — Os sinais de "feito por IA" que reprovam

Cada um destes reprova sozinho. São os padrões que fazem qualquer pessoa reconhecer a página como gerada, mesmo sem saber explicar por quê.

**S1 · Três cartões iguais, de novo e de novo.** No máximo duas seções da página usam a grade de três cartões iguais. A terceira que precisaria dela muda de forma: lista com número, linhas alternando imagem e texto, tabela de comparação, citação grande.

**S2 · Ícone genérico em todo item.** Ícone só entra quando informa. Se todos os itens da lista levam o mesmo desenho (o check repetido oito vezes), ele não informa nada e vira marcador: troque por marcador tipográfico simples, ou dê a cada item um ícone próprio e específico.

**S3 · Gradiente roxo e azul sem motivo.** Converta o hex de cada parada do gradiente: nenhuma delas fica entre 230 e 290 graus de matiz, a não ser que a cor venha da paleta da ETAPA 2. É a assinatura visual mais reconhecível de página gerada.

**S4 · Travessão em headline.** Zero travessão (em dash) em h1, h2 e h3, e no máximo dois na página inteira (rule 8a).

```bash
grep -oE '<h[1-3][^>]*>[^<]*—[^<]*</h[1-3]>' design/page.html   # tem que voltar vazio
```

**S5 · Foto de catálogo com sorriso corporativo.** Pessoa em fundo branco ou de escritório, olhando pra câmera, sorriso de banco de imagens. As fotos são as do mapa de mídia da ETAPA 1.6: inventário do membro, ou lifestyle gerado com a doutrina de imagem daquela etapa.

**S6 · Espaçamento uniforme do topo ao rodapé.** Meça a altura de cada seção em 1440, na mesma sessão do Playwright que tirou o screenshot (cada uma está marcada com `data-aura-section`). Reprova quando todas cabem numa faixa estreita, com menos de 15% de diferença entre a mais alta e a mais baixa. A página precisa de seção curta e de seção longa: o hero e a oferta respiram, uma faixa de prova é baixa. Régua de espaço igual do começo ao fim é o que faz a página parecer um formulário.

**S7 · Tudo centralizado, nenhuma assimetria.** Menos da metade das seções é "texto centralizado numa coluna". Pelo menos uma seção quebra a simetria de propósito: imagem sangrando até a borda, divisão de dois terços com um terço, texto alinhado à esquerda com a imagem descolada da grade.

**S8 · Sombra em tudo.** A sombra do preset base marca uma classe de elemento só, normalmente o cartão que carrega a oferta. Sombra idêntica em toda caixa da página faz nada se destacar, que é o contrário do que ela existe pra fazer.

## O que esta régua não cobre

Contraste de texto (já garantido pelo gerador de paletas da ETAPA 2 e conferido na checklist da 3.7), fonte que de fato carrega (item próprio da 3.7), copy e prova (`copy-engine`), o orçamento de peso da página, que é da 3.7 e volta no GATE 1 da `page-build`, e as regras de acessibilidade que a `page-build` valida no compilado.
