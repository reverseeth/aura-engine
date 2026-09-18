# Page Build · Referência: o funil de quiz virando section Liquid (ETAPAs 1, 2 e 5)

> Por que o funil inteiro é uma section só, o modelo de blocks com uma tela por block, os settings de cada tipo de tela, as três armadilhas do Shopify que mordem exatamente aqui, o CSS estático que faz o funil andar, o formulário de compra por tela de resultado e o que muda no GATE 1, no check de IDs, no smoke test e no loop de iteração. Abra quando o `page_type` do `page-plan.json` for `quiz`.

Nada aqui re-decide o funil. As telas, as perguntas, as ramificações e os perfis nasceram na `page-design` (`.claude/skills/page-design/reference/quiz-funnel.md`) e chegam prontos no bloco `quiz` do `page-plan.json`. Esta referência é como aquilo vira Liquid editável e vai ao ar.

## O split: uma section, um funil

O `design/page.html` aprovado traz o funil inteiro dentro de um `<section data-aura-section="quiz">`, com uma `<div data-aura-screen="[id]">` por tela. **O split da ETAPA 1 não muda:** um fragmento por `data-aura-section`, então o funil sai inteiro em `staging/html/quiz.html`. Nunca splite por tela.

O motivo é mecânico. O CSS que faz o funil andar tem regras cujo alvo é uma tela e cujo sujeito é o contêiner do funil (a regra 3 do mecanismo, que tira a abertura de cena). O conversor filtra e reescopa o CSS por section (padrão 7): telas em sections diferentes recebem folhas diferentes, e essas regras deixam de existir. Uma tela por section quebra o funil no primeiro clique.

Sections depois do funil (garantia, FAQ, rodapé de marca) continuam sections normais no `section_order`, compiladas como sempre.

## COMPILE: uma tela por block

Rode o conversor sobre o fragmento único, como qualquer outra section (`--type quiz`, batch ou Modo C). Depois do compile, no rename semântico da ETAPA 2, o `{% case block.type %}` da section passa a ter três tipos, um por tipo de tela do plano:

| Block type | Uma por | Settings |
|---|---|---|
| `quiz_intro` | funil | `key` (text) · `heading` (inline_richtext) · `body` (richtext) · `cta_label` (text) · `cta_to` (text) · `image` (image_picker) |
| `quiz_question` | tela de pergunta | `key` · `question` (inline_richtext) · `step` (number) · `steps_total` (number) · `back_to` (text) · por alternativa (até 4): `answer_N_label` (text) e `answer_N_to` (text) |
| `quiz_result` | perfil | `key` · `profile_name` · `read_line` (inline_richtext) · `mechanism` (text) · `offer_strap` (inline_richtext) · `proof` (richtext) · `guarantee` (richtext) · `cta_label` · **`variant_id`** (text, vazio) · **`qty`** (number) · `image` (image_picker) |

`max_blocks` no schema igual ao número de telas do plano mais duas, para o membro conseguir acrescentar uma pergunta sem recompilar.

`variant_id` e `qty` no `quiz_result` são o mesmo contrato do `pricing_tier` (`reference/split-e-compile.md`): é por `qty` que a 6.1b casa a tela com a variante criada na loja.

**A ordem dos blocks não é a ordem do funil.** Quem manda é o `cta_to`, o `answer_N_to` e o `back_to`, que carregam a `key` da tela de destino. Isso é proposital: no editor de tema o membro arrasta blocks à vontade sem quebrar o caminho. Escreva isso no `info` do setting `key`, senão a primeira reordenação vira um chamado de suporte.

### As três armadilhas do Shopify que mordem aqui

1. **Destino de tela nunca é setting `url`.** A limitação 2 de `reference/limitacoes-e-debug.md` é exatamente este caso: setting `url` não aceita `#ancora` como default. Por isso `cta_to`, `answer_N_to` e `back_to` são `text` com a `key` da tela, e o markup monta o endereço:
   ```liquid
   <a class="quiz-answer" href="#quiz-{{ block.settings.answer_1_to }}">{{ block.settings.answer_1_label }}</a>
   ```
2. **Default de `richtext` sem `<p>` derruba o arquivo inteiro em silêncio** (limitação 16). `body`, `proof` e `guarantee` são `richtext`: no schema e no template JSON, todo default vai como `"<p>...</p>"`.
3. **`image_picker` não aceita default** (limitação 18). Tela sem imagem trata a ausência no Liquid (`{% if block.settings.image %}`), nunca com default no schema.

### O markup de cada tela

```liquid
<div class="quiz-screen" id="quiz-{{ block.settings.key }}"
     data-aura-screen="{{ block.settings.key }}" {% if block.type == 'quiz_intro' %}data-first{% endif %} {{ block.shopify_attributes }}>
```

- O `id` vai sempre prefixado com `quiz-`: o funil divide o documento com o tema, e `#hero` ou `#faq` soltos colidem com âncora de tema.
- `data-first` sai do TIPO do block, nunca da posição dele: o membro pode arrastar os blocks no editor, e `forloop.first` marcaria a tela errada. É o atributo que a regra 1 do CSS usa, e ele pertence à tela de abertura.
- `{{ block.shopify_attributes }}` em toda tela, senão o editor de tema não seleciona o block.
- A imagem da abertura renderiza **sem** `loading: 'lazy'` (é o candidato a LCP); toda imagem das outras telas renderiza **com**, porque o documento carrega o funil inteiro de uma vez.
- Heading da abertura em `<h1>`, das demais telas em `<h2>`: um `<h1>` por página continua valendo.

## O CSS do funil

O CSS que faz o funil andar é **estático**: nenhum valor dele vem de setting. Por isso ele vai inteiro no `{% stylesheet %}` da section, que não processa Liquid e nem precisa. Ele chega pronto do `design/page.html` aprovado, e o conversor só o reescopa. Confira, depois do compile, que as quatro peças sobreviveram e nesta ordem:

1. `.quiz-screen:not([data-first]){display:none}`
2. `.quiz-screen:target{display:block}`
3. `.quiz:has(.quiz-screen:target) .quiz-screen[data-first]{display:none}`
4. a camada de leitura do resultado (`.quiz-read` com `animation ... forwards`, `.quiz-body` com `backwards`) e, **depois** dela, o bloco `prefers-reduced-motion` que zera atraso e duração.

A regra 3 é a única com `:has()`, e o navegador que não a entende descarta só ela: o visitante vê a abertura mais a tela atual, nunca uma página em branco. Reordenar essas regras quebra o funil sem erro de validação nenhum, então elas não se "organizam" na passada de estilo.

Cores, tipografia, espaçamento e a paleta continuam saindo dos settings como em qualquer section (padrão 2 do conversor). O que é estrutural (`display`, `position`, os `@keyframes`) não vira setting: setting de estrutura é botão para o membro quebrar o funil sem saber.

## O formulário de compra da tela de resultado

Cada `quiz_result` carrega o próprio formulário nativo. Um formulário por tela, nunca um formulário só com vários botões:

```liquid
<form action="{{ routes.cart_add_url }}" method="post" enctype="multipart/form-data">
  <input type="hidden" name="id" value="{{ block.settings.variant_id }}">
  <input type="hidden" name="quantity" value="1">
  <input type="hidden" name="properties[_Quiz]" value="{{ block.settings.profile_name }}">
  <button type="submit" class="quiz-cta">{{ block.settings.cta_label }}</button>
</form>
```

- O carrinho sai preenchido com o item que o resultado recomendou, sem JavaScript: é POST nativo do Shopify, o mesmo caminho do padrão 5 do conversor, e o POST leva `id`, `quantity` e a propriedade juntos. Link `/cart/add?id=` no lugar do formulário é o erro que faz o Meta Pixel não registrar o AddToCart (tabela de debug em `reference/limitacoes-e-debug.md`).
- A propriedade começa com `_`, então ela fica fora da vista do cliente no carrinho e no checkout e ainda assim aparece no pedido: é o perfil do quiz chegando ao admin e ao ESP, de graça.
- **O `variant_id` nasce vazio** e é preenchido na 6.1b, casando pelo `qty` do block, como toda superfície de compra.
- Página que mostra assinatura leva também o campo do plano de venda ao lado do `id`, igual à buy box (`reference/produto-e-oferta.md`).

## O que muda nos gates

**6.1b, check bloqueante de IDs.** O bloco `commerce.buy_surfaces[]` do plano traz uma entrada por tela de resultado, com o campo `screen`. Nenhuma régua nova: os seis itens da 6.1b valem como estão, e o item 6 (toda quantidade da página tem variante) passa a cobrir as telas de resultado porque elas estão na lista. Tela de resultado fora do `buy_surfaces` é o furo clássico aqui, e ele aparece como botão sem ID no ar.

**ETAPA 4, check de placeholder.** O gate de imagem lê o `media` de `sections_plan[]` **e** o `media` de cada tela em `quiz.screens[]`. Placeholder vivo numa tela de resultado bloqueia o deploy igual a placeholder numa section.

**GATE 1, performance.** O funil inteiro vive no mesmo documento, então o peso é a soma de todas as telas. Dois checks a mais na lista:
- toda imagem que não é a da abertura renderiza com `loading: 'lazy'`;
- o HTML servido continua dentro do alvo de ~200 KB com todas as telas dentro. Estourou: reduza a `width:` do `image_url` das telas de resultado, que é onde mora a imagem grande.
O check de zero `<script>` de runtime vale igual, e num quiz ele é mais do que estilo: o funil foi desenhado para não precisar de JavaScript, e um `<script>` aqui significa que alguém reimplementou o que o CSS já fazia.

**6.8, smoke test.** Andar o funil na URL do preview, e não só carregar a página: abertura visível sozinha, uma tela por clique, o endereço mudando a cada resposta, o botão voltar do navegador andando uma tela, a leitura do resultado saindo depois do tempo do plano, o link direto para a tela de resultado abrindo nela, e o botão de compra devolvendo o carrinho com a variante certa. Um caminho por perfil, do começo ao fim.

**6.11, fidelity check.** O screenshot é por tela, nas duas larguras, comparado com a mesma tela do `design/page.html` aprovado. Compare também a altura entre as telas de pergunta: se ela variou no ar e não variava no design, o `min-height` se perdeu na compilação.

## Loop de iteração

Recompilar a section do quiz apaga, de uma vez, os renames dos três block types, os `variant_id` das telas de resultado e as `key` de destino preenchidas no template. Depois de qualquer recompilação: reaplique o rename, refaça o passo de ligar os IDs (6.1b.4) e confira as quatro peças do CSS antes do push. Mudança só de texto de uma tela é edição de setting no template JSON, e não pede recompilação nenhuma.
