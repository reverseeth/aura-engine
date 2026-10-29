# Page Design · Referência: Movimento em CSS (ETAPAS 3 e 4)

> Como estudar o movimento de uma referência (Awwwards) e traduzir para CSS puro: entrada no scroll com `animation-timeline: view()` dentro de `@supports`, `@starting-style`, sticky, marquee sem JavaScript e `prefers-reduced-motion`. O que não cabe em CSS fica de fora e vai listado no `review.md`. Abra quando a direção ou a referência pedir movimento.

A página não tem `<script>` (vira Liquid na `page-build`), então todo movimento é CSS. Movimento é opcional: uma página parada e bem composta vence uma página que se mexe sem motivo. Cada animação tem um papel (guiar o olho, mostrar o produto, dar ritmo à prova), e a página funciona inteira sem ela.

## 1. Estudar a referência (quando houver)

Com o Awwwards na sessão e uma referência marcada que se mexe:

- `mcp__awwwards__get_motion_dna` na URL: a pilha de animação, quantos pins e scrubs, o vocabulário de easing e as durações.
- `mcp__awwwards__analyze_scroll_map` com `compact: true`: o que anima, em que propriedade, com que gatilho.

Com a skill `awwwards-motion-study` instalada, siga o roteiro dela para o inventário. Escreva o inventário em 3 a 6 linhas no `direction.md` (seção da direção ou do blueprint da seção): o elemento, o que faz, a receita CSS deste arquivo que o traduz, ou "fora: precisa de JS".

## 2. Receitas

### Entrada no scroll (o conteúdo nasce visível)

```css
.reveal { opacity: 1; transform: none; }
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .reveal {
      animation: reveal linear both;
      animation-timeline: view();
      animation-range: entry 0% entry 40%;
    }
    @keyframes reveal { from { opacity: 0; transform: translateY(24px); } }
  }
}
```

O QA da ETAPA 5 fotografa com movimento reduzido, então a receita precisa ficar inteira dentro do `prefers-reduced-motion: no-preference`; fora dele, a captura sai com faixas em branco. O estado padrão é visível: navegador sem `view()` (o Firefox hoje) mostra a página parada e inteira. Nunca esconda conteúdo fora do `@supports`. Anime só `opacity` e `transform`.

### Elemento que aparece (`@starting-style`)

```css
details[open] .answer {
  opacity: 1; transform: none;
  transition: opacity .3s ease, transform .3s ease;
  @starting-style { opacity: 0; transform: translateY(-6px); }
}
```

Bom para FAQ em `<details>`, troca de kit por `:has(input:checked)` e o painel da "live thing".

### Sticky

`position: sticky; top: 0` numa coluna (imagem que fica enquanto o texto rola, a "split stage") ou no resumo da oferta. Em 390 o sticky vira bloco normal ou um topo de 50 a 60svh que solta depois da primeira seção; nunca prenda mais de um elemento ao mesmo tempo na tela pequena.

### Marquee sem JavaScript

Faixa de logos ou de prova em loop, só CSS:

```css
.marquee { overflow: hidden; }
.marquee__belt { display: flex; width: max-content; }
.marquee__group { display: flex; gap: var(--space-6); padding-inline-end: var(--space-6); flex-shrink: 0; }
@media (prefers-reduced-motion: no-preference) {
  .marquee__belt { animation: marquee 40s linear infinite; }
  .marquee:hover .marquee__belt { animation-play-state: paused; }
  @keyframes marquee { to { transform: translateX(-50%); } }
}
```

Duas cópias idênticas do grupo (a segunda com `aria-hidden="true"`), o espaço entre itens dentro de cada grupo (o `padding-inline-end` fecha a emenda) e toda imagem com `width` e `height` no HTML, sem `loading="lazy"`, para a largura não mudar no meio do loop. A versão com JavaScript de `.claude/lib/shopify-section-patterns/marquee-infinito.md` é do tema, não desta página: aqui vale a receita acima.

### Hover e foco

Transições de 150 a 250ms em cor, sombra e `transform` de botões e cards, sempre com o mesmo estado em `:focus-visible`.

## 3. `prefers-reduced-motion`

Todo `animation` fica dentro de `@media (prefers-reduced-motion: no-preference)`, como nas receitas. Com redução pedida, a página fica parada e completa.

## 4. O que fica de fora

Scroll com scrub de timeline complexa, WebGL, cursor customizado, pin com troca de cena, contadores que sobem e qualquer coisa que dependa de medir o DOM. Não tente imitar com hack: liste no `review.md` ("movimento da referência que não entrou: X, precisa de JS") para o membro saber o que ficou na mesa.
