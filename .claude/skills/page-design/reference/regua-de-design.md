# Page Design · Referência: A régua de design (ETAPAS 4 e 5)

> O padrão de design que a página tem que atingir nos dois modos de construção, em cinco blocos de itens: tipografia, ritmo e espaço, cor, movimento e os sinais de "feito por IA". Cada item diz como é conferido: medido por script, conferido no arquivo ou julgado pelo revisor sem contexto. Serve de direção ANTES de construir (ETAPA 4) e de placar DEPOIS, nas rodadas de QA da ETAPA 5. É também o único lugar da skill com a regra do travessão e o teto de rodadas.

## Como esta régua é usada

Dois momentos, o mesmo arquivo:

1. **Antes de construir** (ETAPA 4, nos dois modos): os números daqui são a direção. Escala, grade de espaço, uso da cor e movimento já nascem certos, em vez de virarem correção depois.
2. **Depois de gerar o `design/page.html`** (ETAPA 5): cada item é conferido pelo caminho que a etiqueta dele diz.

**As três etiquetas:**

- **`medido · <id>`**: o número sai do `.claude/lib/theme-verify/verify_page.py --json-out page/qa-metrics.json` (ou do `tools/page-qa/tokens.py`, quando o id diz). O item da régua lê o `status` daquele id; não se refaz a medida à mão.
- **`arquivo`**: conferido no `design/page.html` pelo comando do item ou pela leitura do CSS, com o valor encontrado como evidência. É o que nenhum script mede e nenhuma captura mostra (movimento, foco, ordem de blocos na folha de estilo).
- **`julgado`**: o revisor sem contexto (`reference/revisor.md`) dá a nota olhando as capturas de 1440 e 390, as 3 referências marcadas e o `direction.md`, e grava no `page/review.md`. Sem subagente na sessão, a skill pontua esses itens sozinha nas mesmas capturas.

**Rodadas e teto (regra única da skill):**

- Bloqueia só o que o `verify_page.py` marca como bloqueante em `fail` (a lista está em `.claude/lib/theme-verify/README.md`). Os itens desta régua não bloqueiam sozinhos: viram as correções da rodada seguinte, junto das 5 correções de maior impacto do `review.md`.
- Cada rodada corrige e mede a página INTEIRA de novo, porque a correção de um item costuma quebrar outro (subir o respiro entre seções mexe no ritmo, trocar o peso do título mexe na hierarquia).
- **Teto de 3 rodadas de correção.** Para antes da terceira quando não há item bloqueante em `fail` e nenhuma nota do revisor abaixo de 3. O que continuar em `fail` ou abaixo de 3 depois da terceira vai pro membro, em uma linha por item: o que está errado, o que você tentou e o que depende dele. Essas rodadas são silenciosas e acontecem ANTES de ele ver a página; não se confundem com as iterações COM o membro depois do preview.
- O placar não vira arquivo próprio: os números ficam no `qa-metrics.json`, as notas no `review.md`, e os itens `arquivo` aparecem só como correção feita ou, depois da terceira rodada, na linha dita ao membro.
- **Com duas versões da mesma página** (a segunda opinião da ETAPA 5, `reference/brief-codex.md`), o placar é este mesmo, com uma coluna por versão e os mesmos ids. A comparação não muda nenhum item nem inventa critério novo: quem decide é a contagem de reprovas, e o desempate está escrito lá.

Os comandos abaixo rodam de dentro de `workspace/[produto]/page/`.

## Bloco T — Tipografia

**T1 · Escala modular declarada.** `medido · font_sizes_distinct`. Os tamanhos de fonte saem de uma escala com razão única, 1.25 ou 1.333, declarada em custom properties `--text-*` no `:root`. Todo `font-size` da página é uma dessas variáveis, ou um `clamp()` cujos dois extremos são degraus da escala. No máximo 7 tamanhos distintos renderizados na página inteira, contados pelo `verify_page.py` nos elementos visíveis.

**T2 · Só as famílias declaradas.** `arquivo`. A página usa só as famílias que a marca ou a direção declararam (sub-etapa 2.1, `reference/tipografia.md`), nunca mais de duas, ignorando a pilha de fallback. Toda `font-family` aponta pra `--font-heading` ou `--font-body`.

```bash
grep -o 'font-family:[^;]*' design/page.html | sort -u
```

**T3 · Contraste de peso real entre título e corpo.** `julgado`. A diferença de `font-weight` entre os títulos e o corpo é de pelo menos 200 (corpo em 400 com título em 600 ou 700, por exemplo). Se a família tem um peso só, o contraste vem de dois degraus de escala no tamanho mais uma diferença clara de entrelinha, e isso fica escrito na evidência. Título e corpo no mesmo peso e a um degrau de distância reprovam: a hierarquia some na leitura de relance.

**T4 · Medida de linha entre 45 e 75 caracteres.** `medido · line_length`. Todo bloco de texto corrido tem `max-width` entre `45ch` e `75ch` (ou o equivalente em rem). O `verify_page.py` mede a linha renderizada em 1440, então texto atravessando a tela inteira reprova mesmo com o `max-width` declarado, porque em geral o contêiner está sobrescrevendo.

**T5 · Entrelinha proporcional ao tamanho.** `arquivo`. Quanto maior o texto, menor a entrelinha. Corpo entre 1.5 e 1.7; subtítulos entre 1.3 e 1.45; títulos grandes entre 1.05 e 1.25. `line-height: 1.5` num h1 reprova, e corpo abaixo de 1.4 também.

**T6 · Caixa alta só em rótulo curto.** `julgado`. Texto em maiúsculas aparece só em eyebrow, rótulo e microcopy de botão, com no máximo cinco palavras e com `letter-spacing` positivo (entre 0.04em e 0.12em). Parágrafo, headline ou item de lista em caixa alta reprovam.

## Bloco E — Ritmo e espaço

**E1 · Uma grade de espaçamento, base 4 ou 8, sem exceção.** `arquivo`. Todo `padding`, `margin` e `gap` é múltiplo da base, declarado como token no `:root` e usado pela variável. Valor solto fora da grade reprova, com duas exceções que não precisam de justificativa: borda de 1px e centralização por `auto`.

```bash
grep -oE '(padding|margin|gap)[^:]*:[^;]*' design/page.html | sort -u
```

**E2 · O respiro entre seções é maior que o respiro dentro delas.** `julgado`. O `padding-block` da section vale pelo menos duas vezes o maior `gap` interno dela. No print de 1440, a distância entre a última linha de uma seção e o título da seguinte é visivelmente maior que a distância entre esse título e o parágrafo dele. Se a página parece um texto corrido sem divisão, é este item que está reprovado. Referência de respiro no desktop: 5 a 8rem de `padding-block` no hero e na oferta, menos nas seções de apoio, e no celular a metade disso, porque a tela já é estreita e o mesmo valor come a página inteira.

**E3 · Proximidade dentro do bloco.** `julgado`. Cada elemento fica mais perto do que ele pertence do que do vizinho: rótulo colado no dado que descreve, legenda colada na imagem, título mais perto do próprio parágrafo do que do parágrafo anterior. Confere no print.

**E4 · Alinhamento óptico nos blocos com ícone.** `julgado`. O ícone alinha pelo centro óptico da primeira linha do texto, não pelo topo da caixa, e o texto de todos os itens da lista começa na mesma coluna (grade de duas colunas, largura fixa na coluna do ícone). Ícone flutuando acima ou abaixo da linha reprova. Confere no print, ampliando a lista.

**E5 · Margem lateral constante no celular.** `medido · equal_side_margins` e `horizontal_overflow`. O mesmo gutter do topo ao rodapé, entre 16px e 24px, e nada encostando na borda em 390. Zero rolagem horizontal: a largura de rolagem é igual à largura visível.

## Bloco C — Cor

**C1 · A paleta é a da marca ou da direção, por papel.** `medido · tokens.py` (cores soltas). Toda cor usada vem de uma variável `--color-<papel>` (`background`, `surface`, `foreground`, `primary`, `on-primary`, `accent`, `muted`, `border`). Cor solta no CSS, fora do `:root`, reprova; o `tools/page-qa/tokens.py` lista as que achar e recusa gerar os tokens com mais de 5. Cor inventada no meio da página é o caminho mais rápido pra página parecer de outro produto.

**C2 · Cor com significado.** `julgado`. O `primary` marca uma classe de coisa só, e a mais importante: a ação. Nenhum elemento não clicável usa a cor do botão principal. O `accent` marca o que a página quer que seja lido primeiro em cada seção (um número de prova, uma palavra da headline, um selo), no máximo um por seção. Cor forte espalhada em três papéis diferentes virou decoração e reprova.

**C3 · Zero gradiente decorativo.** `medido · gradients` (contagem, até 3) e `julgado` (função). Gradiente só entra com função: escurecer uma foto pra o texto ficar legível, ou separar duas seções que dividem o mesmo fundo. Gradiente de duas cores de marca no hero "porque preenche" reprova.

**C4 · Estado de foco visível.** `arquivo`. Todo elemento clicável tem `:focus-visible` com contorno de pelo menos 2px, afastado do elemento, e com contraste de pelo menos 3:1 contra o fundo ao lado. `outline: none` sem substituto reprova.

```bash
grep -nE 'focus-visible|outline:\s*none' design/page.html
```

**C5 · A cor não é o único sinal.** `julgado`. Nenhuma informação depende só da cor pra ser entendida (o item selecionado do seletor de pacote tem borda ou marca, além da cor; o preço riscado tem o risco, além do tom apagado).

## Bloco M — Movimento

O contrato do `page.html` é **zero JavaScript**. Todo movimento aqui é CSS, com as receitas de `reference/movimento-css.md`. O revisor vê capturas paradas, então os itens de movimento são todos `arquivo`.

**M1 · Movimento só na entrada da seção.** `arquivo`. Uma animação por seção, de opacidade 0 até 1 com deslocamento curto, entre 8px e 24px, sempre na mesma direção na página inteira. Nada mais se mexe sozinho.

**M2 · Duração entre 200ms e 600ms, com saída suave.** `arquivo`. A curva desacelera no fim (`ease-out` ou uma `cubic-bezier` equivalente). `linear` e `ease-in-out` longo reprovam numa entrada: fazem o elemento parecer que escorrega.

```bash
grep -oE 'animation[^;]*|transition[^;]*' design/page.html | sort -u
```

**M3 · Atraso escalonado entre irmãos.** `arquivo`. Cartões da mesma fileira entram em sequência, com 40ms a 120ms de diferença entre um e o seguinte, e no máximo cinco degraus. Sem teto, o sexto cartão espera meio segundo e a página parece travada.

**M4 · Rolagem sem script, e nunca às custas do conteúdo.** `arquivo`. Animação disparada pela rolagem usa `animation-timeline: view()` dentro de `@supports (animation-timeline: view())`, e o estado inicial (a opacidade zerada e o deslocamento) é declarado **só dentro** desse bloco. Em navegador sem suporte, a seção nasce visível e parada. Estado inicial fora do `@supports` reprova, porque é assim que a página inteira fica invisível pra quem não tem suporte.

**M5 · `prefers-reduced-motion: reduce` desliga tudo, e vem por último.** `arquivo`. Dentro dessa media query, as animações e transições vão a zero e o conteúdo fica no estado FINAL, visível. Nunca no inicial. E o bloco fica DEPOIS do `@supports` do M4 na folha de estilo: os dois têm a mesma especificidade, então o último vence. Invertido, quem pediu menos movimento recebe a seção com opacidade zero e nunca vê o conteúdo. Confere pela ordem em que os dois blocos aparecem no `<style>`.

**M6 · Zero animação em laço, com uma exceção.** `arquivo`. Nada pisca, pulsa, gira ou repete enquanto a pessoa lê: contador animado, seta saltitante e selo pulsando reprovam. A exceção é o marquee em CSS puro (faixa de logos, de selos ou de prova), no máximo um por página, com `transform` em `@keyframes`, imagens com `width` e `height` reservados (sem isso a emenda salta enquanto elas carregam) e parado sob `prefers-reduced-motion`. Marquee com JavaScript continua reprovando.

**M7 · Só `opacity` e `transform` são animados.** `arquivo`. Animar `height`, `top`, `margin` ou `width` reprova, porque recalcula o layout a cada quadro e engasga no celular.

**M8 · Transição entre telas, só no `page_type: quiz`.** `arquivo`. A troca de tela não é entrada de seção e tem régua própria, mais curta, porque a pessoa está esperando a resposta:

- A tela que entra faz opacidade de 0 a 1 com deslocamento de no máximo 12px, entre 150ms e 300ms, com a mesma curva de saída do M2. Nada mais se move na troca.
- **Zero salto de altura entre as perguntas.** As telas de pergunta dividem o mesmo `min-height`, e a diferença medida entre elas é zero nas duas larguras. Tela que encolhe e cresce a cada pergunta faz o dedo errar a alternativa.
- A barra de progresso aparece em toda tela de pergunta e nunca anda para trás.
- A leitura do resultado dura entre 1,2s e 2,5s, preenche uma vez e para (não é laço, então o M6 continua valendo), e `prefers-reduced-motion` a zera: o resultado aparece de uma vez, nunca invisível.

```bash
# a altura de cada tela, numa sessão do Playwright sobre o page.html
# (percorra as telas pelo endereço: #q1, #q2, ... e meça [data-aura-screen])
```

## Bloco S — Os sinais de "feito por IA" que reprovam

Cada um destes pesa sozinho na nota de "feito por IA" do revisor. São os padrões que fazem qualquer pessoa reconhecer a página como gerada, mesmo sem saber explicar por quê.

**S1 · Três cartões iguais, de novo e de novo.** `julgado`. No máximo duas seções da página usam a grade de três cartões iguais. A terceira que precisaria dela muda de forma: lista com número, linhas alternando imagem e texto, tabela de comparação, citação grande.

**S2 · Ícone genérico em todo item.** `julgado`. Ícone só entra quando informa. Se todos os itens da lista levam o mesmo desenho (o check repetido oito vezes), ele não informa nada e vira marcador: troque por marcador tipográfico simples, ou dê a cada item um ícone próprio e específico.

**S3 · Gradiente roxo e azul sem motivo.** `arquivo`. Converta o hex de cada parada do gradiente: nenhuma delas fica entre 230 e 290 graus de matiz, a não ser que a cor venha da paleta da marca ou da direção. É a assinatura visual mais reconhecível de página gerada.

**S4 · Travessão (regra única da skill).** `arquivo`. Zero travessão (em dash) em h1, h2, h3 e eyebrow, e no máximo dois na página inteira (rule 8a). Vale também pra Big Idea usada como eyebrow e pra todo texto que a skill escreve na página.

```bash
grep -oE '<h[1-3][^>]*>[^<]*—[^<]*</h[1-3]>' design/page.html   # tem que voltar vazio
```

**S5 · Foto de catálogo com sorriso corporativo.** `julgado`. Pessoa em fundo branco ou de escritório, olhando pra câmera, sorriso de banco de imagens. As fotos são as do mapa de mídia da ETAPA 1.6: inventário do membro, ou lifestyle gerado com a doutrina de imagem daquela etapa.

**S6 · Espaçamento uniforme do topo ao rodapé.** `julgado`, com as alturas por seção do `qa-metrics.json` como apoio. Reprova quando todas as seções cabem numa faixa estreita, com menos de 15% de diferença entre a mais alta e a mais baixa em 1440. A página precisa de seção curta e de seção longa: o hero e a oferta respiram, uma faixa de prova é baixa. Régua de espaço igual do começo ao fim é o que faz a página parecer um formulário.

**S7 · Tudo centralizado, nenhuma assimetria.** `julgado`. Menos da metade das seções é "texto centralizado numa coluna". Pelo menos uma seção quebra a simetria de propósito: imagem sangrando até a borda, divisão de dois terços com um terço, texto alinhado à esquerda com a imagem descolada da grade.

**S8 · Sombra em tudo.** `julgado`. A sombra do preset base marca uma classe de elemento só, normalmente o cartão que carrega a oferta. Sombra idêntica em toda caixa da página faz nada se destacar, que é o contrário do que ela existe pra fazer.

## O que esta régua não cobre

Os itens do `qa-metrics.json` que não têm par aqui (contraste, linhas da headline em 390, faixas vazias, peso da página, imagens quebradas, markers e o resto da lista do `.claude/lib/theme-verify/README.md`), que a ETAPA 5 lê direto do arquivo; fonte que de fato carrega (preview da ETAPA 6 e 6.9 da `page-build`); copy e prova (`copy-engine`); e as regras de acessibilidade que a `page-build` valida no compilado.
