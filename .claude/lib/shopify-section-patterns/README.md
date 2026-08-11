# Shopify Section Patterns

Padrões de section Liquid endurecidos em produção numa loja Shopify real (tema Impact, arquitetura Online Store 2.0 — o modelo atual de temas da Shopify, com sections configuráveis por JSON). Cada arquivo documenta um problema que só aparece no aparelho do cliente (nunca no preview com cache quente), a solução que sobreviveu ao uso real, o código de referência pronto pra adaptar e as armadilhas que fazem o padrão regredir. A regra de uso é uma só: **adaptar tokens, copy e seletores pro produto da vez — nunca colar cru.** Os textos dos exemplos são placeholders e as cores são neutras de propósito; o valor do padrão está na estrutura e nas decisões técnicas, não no visual do exemplo.

## Índice

| Padrão | Quando usar | Arquivo |
|---|---|---|
| Marquee infinito | Faixa de logos/press rolando em loop sem emenda visível | `marquee-infinito.md` |
| Sticky add-to-cart | Botão de compra fixo no rodapé da tela, que some sobre a oferta e o footer | `sticky-add-to-cart.md` |
| Gradiente de hero com easing | Degradê escuro sobre foto de hero sem degrau visível (banding) | `gradiente-hero-eased.md` |
| Badges sobre imagem | Selos de vidro editáveis flutuando sobre a foto do produto | `badges-sobre-imagem.md` |
| Drawer enriquecido | Personalizar o cart-drawer do tema (identidade, card de infos, cupom, add-to-cart sem reload) sem fork | `drawer-enriquecido.md` |
| Fonte universal | Fonte custom em 100% da página, incluindo o drawer do tema | `fonte-universal.md` |

## Sistema de tokens por snippet (pré-requisito de todos os padrões)

Todos os padrões assumem que a paleta da página vive num snippet base (renderizado no `theme.liquid` ou no topo do template) que declara cada cor como um **trio R,G,B sem o `rgb()` em volta**:

```css
:root {
  --sec-bg: 246, 245, 241;      /* areia clara */
  --sec-ink: 28, 28, 30;        /* grafite */
  --sec-accent: 40, 40, 46;
  --sec-line: 214, 214, 210;
  --sec-dark: 24, 24, 28;
}
```

O consumo é sempre `rgb(var(--x))` pra cor cheia e `rgba(var(--x), alpha)` pra cor com transparência:

```css
.card { background: rgb(var(--sec-bg)); border: 1px solid rgb(var(--sec-line)); }
.glow { box-shadow: 0 14px 38px rgba(var(--sec-accent), 0.42); }
```

O motivo do formato: um token em trio serve tanto pra cor sólida quanto pra qualquer nível de transparência dela — sombras, scrims, overlays e bordas suaves saem todos da mesma paleta, sem duplicar valores em versão "com alpha". Trocar a marca inteira é editar um bloco de `:root`.
