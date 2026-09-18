# Page Design · Referência: Rota 3, quebra-cabeça de seções (sub-etapa 3.5)

> O inventário das fontes, a extração de estrutura de arquivo `.html` e de print lido por visão, o mapa fonte→section conferido contra o plano, o passo de unificação que impede a página de parecer colagem e o teste de vizinhança. Abra na sub-etapa 3.5.

### 3.5 Rota 3 — Quebra-cabeça de seções

O membro manda várias referências: arquivos `.html` de páginas diferentes, prints de seções que achou no Pinterest, Figma ou Dribbble, ou os dois misturados. A Aura extrai a estrutura de cada uma e monta **uma página só**, unificada. Cada seção vira uma section editável no editor da Shopify, como na rota 2.

> **A MESMA regra legal e ética da rota 2 vale integralmente:** de cada fonte sai estrutura e layout, nunca copy, imagem, logo, marca ou claim. O conteúdo é 100% do membro (copy da `copy-engine`, oferta da `offer-builder`, imagens do mapa de mídia da 1.6, paleta e tipografia da ETAPA 2).

#### 1. Inventário das fontes

Peça o material e numere o que chegou, uma linha por fonte: o que é (arquivo `.html` ou print), de onde veio e **qual seção o membro quer dali**. Se ele não disser qual seção quer de qual fonte, proponha o mapa você mesmo e confirme em uma mensagem só. Sem esse mapa, a montagem vira colagem de tudo que apareceu.

#### 2. Extrair estrutura de cada fonte

- **Arquivo `.html`:** mesma serialização da rota 2 — a seção alvo com estilos computados em desktop e mobile, e o screenshot dela. Só a seção pedida; o resto do arquivo é descartado.
- **Print (PNG/JPG):** leia por visão (Read na imagem) e descreva em **estrutura**, nunca em conteúdo: grade e número de colunas, proporção e recorte da imagem, hierarquia tipográfica RELATIVA (quantas vezes o título é maior que o corpo), ritmo de espaço (respiro entre blocos comparado ao respiro interno), posição e peso do CTA, alinhamento (centrado, à esquerda, assimétrico). O texto que aparece no print nunca é copiado: a copy da seção é a da `copy-engine`.

Fonte que chegou ilegível (print cortado, resolução baixa demais pra ler hierarquia): diga em uma linha e peça outro, ou desenhe aquela seção pelo caminho da rota 1. Não invente a estrutura que não deu pra ver.

#### 3. Conferir contra o plano da ETAPA 1

O `sections_plan` manda, não o material que chegou:

- Fonte que cobre uma seção que o plano não pede: descarte e diga por que em uma linha.
- Seção do plano que nenhuma fonte cobre: desenhe pelo caminho da rota 1 (o pacote de direção da 3.3), no ritmo e na hierarquia das vizinhas já montadas. É o normal — quase nunca as referências cobrem a página inteira.
- Duas fontes disputando a mesma seção: escolha a que serve ao `page_type` e ao `hero_type` e diga qual entrou.

#### 4. Unificar (o passo que decide se parece colagem)

As fontes contribuem com **estrutura e ritmo**; os tokens são da página, nunca de cada referência. Antes de montar, fixe e aplique em todas as seções:

- **Uma escala tipográfica só** (modular, 1.25 ou 1.333) e no máximo duas famílias, as da ETAPA 2. A hierarquia relativa lida em cada fonte é traduzida PRA essa escala, nunca colada em pixels.
- **Uma grade de espaçamento só** (base 4 ou 8), com o respiro entre seções maior que o respiro dentro delas — o mesmo valor do topo ao rodapé.
- **A paleta da ETAPA 2 por role** em toda seção. Cor herdada de referência não entra.
- **Um radius e uma sombra** (os do preset base) e uma largura de contêiner única.
- **Um tratamento de botão só**: mesmo formato, mesmo peso, mesma cor de texto em toda a página, com o CTA de cada seção mudando só a palavra.
- **Proporção de imagem consistente** por família de seção (todas as fotos de prova social no mesmo recorte, todas as de produto no mesmo).

#### 5. Normalizar e marcar

O que veio de arquivo `.html` passa pela **normalização da 3.6** (utilities viram CSS plano, JS de runtime sai, assets locais, self-contained com zero `<script>`). Injete os markers `<section data-aura-section="[id do sections_plan]">` em todas as seções e salve como `design/page.html`.

#### 6. Teste de vizinhança (anti-colagem, bloqueante)

No self-review da 3.7, além da régua normal: no screenshot de 1440, olhe **cada par de seções vizinhas** e compare a assinatura visual — peso e tamanho do título, tratamento do botão, espaçamento antes e depois, largura do contêiner, tratamento de imagem. Se dá pra dizer onde uma referência termina e a outra começa, a unificação do passo 4 não fechou: volte nela e refaça. A página tem que parecer desenhada por uma pessoa só.

Registre no `page-plan.json`: `design_route: "section-puzzle"` e, em `design_route_ref`, o mapa fonte→section (qual fonte virou qual seção).
