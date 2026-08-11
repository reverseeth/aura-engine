# Fonte universal (fonte custom em 100% da página, incluindo o drawer)

## O problema

Declarar a fonte custom nas sections da landing não basta: o tema renderiza componentes próprios (cart-drawer, popups, banners de aviso, campos de formulário) com as fontes DELE, resolvidas por CSS vars internas. O resultado é uma página quebrada em duas tipografias — a landing na fonte da marca e o drawer/checkout-path na fonte do tema — exatamente na transição mais sensível do funil.

O segundo modo de falha é silencioso: `@font-face` declarado apontando pra um arquivo que NÃO está nos assets do tema não gera erro nenhum — o browser tenta baixar, falha, e cai pro fallback da pilha (`sans-serif`) sem avisar. A página "funciona", só que na fonte errada, e ninguém percebe até olhar lado a lado.

## A solução

Quatro camadas, todas necessárias:

- **`@font-face` servido do próprio tema**: o arquivo da fonte sobe pra `assets/` e a URL vem de `{{ 'brand-sans.otf' | asset_url }}` — sem host externo, sem CORS, cache do CDN da Shopify.
- **Regra universal com `!important`**: `body, body *, button, input, select, textarea { font-family: ... !important }`. Os controles de formulário entram explícitos porque não herdam `font-family` do body por padrão.
- **As CSS vars do tema**: o Impact resolve a própria tipografia por `--heading-font-family` e `--text-font-family` — repontar as duas garante que qualquer componente do tema que monte a pilha pela var já nasça na fonte certa. Outros temas têm vars equivalentes (inspecionar o `:root` do tema pra achar os nomes).
- **O drawer explicitamente**: `cart-drawer, cart-drawer *:not(svg):not(path)` — a exclusão de `svg`/`path` evita warnings e efeitos colaterais de `font-family` em nós de vetor.

E uma verificação obrigatória, porque **declarar não é carregar**: um censo de fonte computada — percorrer os elementos visíveis da página renderizada e contar qual `font-family` o browser DE FATO resolveu pra cada um. A lib `.claude/lib/theme-verify/` já traz esse censo pronto (`font_census.py "<url>" --font "Nome da Fonte"`, com `--open-selector` pra verificar o drawer aberto); o snippet abaixo é a versão manual pra rodar no console do browser. Se o arquivo não subiu pros assets, o censo mostra o fallback dominando; o CSS, olhado sozinho, parece perfeito.

## Código de referência

CSS (no snippet base da página, renderizado no `theme.liquid`):

```liquid
<style>
  @font-face {
    font-family: 'Brand Sans';
    src: url('{{ 'brand-sans.otf' | asset_url }}') format('opentype');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
  }
  :root {
    /* o tema Impact resolve as próprias fontes por estas vars */
    --heading-font-family: "Brand Sans", sans-serif;
    --text-font-family: "Brand Sans", sans-serif;
  }
  /* absolutamente todo texto da página (sections, drawer, popup, banners) */
  body, body *, button, input, select, textarea {
    font-family: "Brand Sans", -apple-system, sans-serif !important;
  }
  cart-drawer, cart-drawer *:not(svg):not(path) {
    font-family: "Brand Sans", sans-serif !important;
  }
</style>
```

Censo de fonte computada (rodar via Playwright ou no console do browser sobre a página publicada):

```js
/* conta a font-family computada de cada elemento visível com texto */
const censo = {};
document.querySelectorAll('body *').forEach((el) => {
  if (!el.textContent.trim() || !el.offsetParent) return;
  const fam = getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim();
  censo[fam] = (censo[fam] || 0) + 1;
});
console.table(censo);
/* esperado: "Brand Sans" com ~100% dos nós; qualquer outra família com
   contagem alta = ou o arquivo não está nos assets, ou um componente
   escapou das quatro camadas de regra */
```

O upload do arquivo pros assets sai pelo Shopify CLI:

```bash
shopify theme push --only assets/brand-sans.otf
```

## Armadilhas

- **Confiar no CSS sem rodar o censo.** Sintoma: nenhum — e esse é o problema. Fonte que falha em carregar degrada em silêncio pro fallback; a página abre, "funciona", e está na fonte errada. O censo de fonte computada é a única prova de que a fonte carregou e venceu em todos os nós.
- **Declarar o `@font-face` sem subir o arquivo pros assets.** Sintoma: censo mostra o fallback (`-apple-system`, `sans-serif`) dominando; a aba Network mostra 404 no `.otf`. O push do asset faz parte do deploy do padrão, não é passo opcional.
- **Só a regra `body *`, sem as vars do tema.** Sintoma: componentes do tema que montam a pilha de fonte via `var(--heading-font-family)` em contextos que a regra universal não alcança (shadow DOM, estilos injetados depois) ficam na fonte do tema. As duas camadas se cobrem mutuamente.
- **Esquecer `button, input, select, textarea` explícitos.** Sintoma: os campos de formulário (cupom, quantidade, newsletter) ficam na fonte do sistema — controles de formulário não herdam `font-family` por padrão.
- **Aplicar `font-family` em `svg`/`path` dentro do drawer.** Sintoma: nenhum efeito visual útil e, em alguns temas, warnings de estilo em nós de vetor. O `:not(svg):not(path)` existe por isso.
- **Fonte de host externo (CDN de fontes).** Sintoma: flash de fallback mais longo, dependência de terceiro no caminho crítico e potencial bloqueio por consent-tools. `asset_url` mantém tudo no CDN da Shopify.
- **`font-display` ausente.** Sintoma: texto invisível durante o carregamento da fonte em conexão lenta. `font-display: swap` mostra o fallback primeiro e troca quando a fonte chega.
