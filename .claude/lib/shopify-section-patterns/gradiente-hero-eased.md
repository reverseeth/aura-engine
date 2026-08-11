# Gradiente de hero com easing (degradê escuro sem banding)

## O problema

Um degradê escuro descendo do topo da foto do hero (pra dar contraste a header, headline ou selos) escrito como gradiente linear de 2 stops — `linear-gradient(180deg, rgba(0,0,0,.8), transparent)` — produz banding: a transição da opacidade é uma reta, o olho percebe o degrau onde o escuro "termina", e o resultado lê como uma sombra suja ou um retângulo semitransparente colado na foto, não como luz. Em telas com pouca profundidade de cor o degrau vira faixas visíveis.

O segundo problema é operacional: força e altura do degradê são decisões de arte que dependem da foto que o membro escolher no editor — hard-codar os valores no CSS obriga a editar código a cada troca de imagem.

## A solução

- **Curva suavizada de ~10 stops** que imita uma curva de easing: os alphas caem em `0.95 / 0.85 / 0.70 / 0.52 / 0.34 / 0.19 / 0.08 / 0.02` nas posições `12 / 24 / 36 / 48 / 60 / 72 / 84 / 93%`, fechando em zero no `100%`. A queda começa lenta, acelera no meio e desmancha devagar no fim — o preto se mistura na foto sem degrau perceptível.
- **Força e altura viram range settings do schema**, injetados como CSS vars inline no elemento da section: `--sec-grad` (0 a 1) multiplica cada alpha via `calc()`, e `--sec-grad-h` controla o `height` do `::before`. O membro ajusta os dois no editor do tema, olhando a foto real.
- **Checkbox liga/desliga** o degradê inteiro (a classe modificadora só entra no markup se o setting está ativo).
- **O degradê vive num `::before` da section** com `pointer-events: none` e `z-index` entre a foto (0) e o conteúdo (2) — nunca rouba clique nem cobre texto.

## Código de referência

```liquid
<section
  class="sec-hero{% if section.settings.top_gradient %} sec-hero--topgrad{% endif %}"
  data-section="sec-hero"
  style="--sec-grad: {{ section.settings.top_gradient_strength | default: 100 | divided_by: 100.0 }}; --sec-grad-h: {{ section.settings.top_gradient_height | default: 50 }}%;"
>
  <style>
    .sec-hero {
      position: relative;
      min-height: 700px;
      overflow: hidden;
      background: rgb(var(--sec-dark));
      color: rgb(255, 255, 255);
    }
    .sec-hero .sec-hero-media { position: absolute; inset: 0; z-index: 0; }
    .sec-hero .sec-hero-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: 50% 50%;
      display: block;
    }
    /* degradê escuro descendo do topo da foto (ligável no editor) */
    .sec-hero.sec-hero--topgrad::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: var(--sec-grad-h, 50%);
      z-index: 1;
      /* curva de easing: o escuro desmancha na imagem sem degrau visível */
      background: linear-gradient(
        180deg,
        rgba(0, 0, 0, var(--sec-grad, 1)) 0%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.95)) 12%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.85)) 24%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.70)) 36%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.52)) 48%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.34)) 60%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.19)) 72%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.08)) 84%,
        rgba(0, 0, 0, calc(var(--sec-grad, 1) * 0.02)) 93%,
        rgba(0, 0, 0, 0) 100%
      );
      pointer-events: none;
    }
    .sec-hero .sec-hero-inner { position: relative; z-index: 2; }
  </style>

  <div class="sec-hero-media" aria-hidden="true">
    {%- if section.settings.bg_image -%}
      {{ section.settings.bg_image
        | image_url: width: 2400
        | image_tag:
          loading: 'eager',
          fetchpriority: 'high',
          sizes: '100vw',
          widths: '750, 1100, 1440, 1920, 2400',
          alt: '' }}
    {%- endif -%}
  </div>

  <div class="sec-hero-inner">
    <h2>{{ section.settings.headline | escape }}</h2>
  </div>
</section>

{% schema %}
{
  "name": "Hero",
  "settings": [
    { "type": "image_picker", "id": "bg_image", "label": "Foto de fundo (full-bleed)" },
    { "type": "checkbox", "id": "top_gradient", "label": "Degradê escuro no topo da foto", "default": true },
    {
      "type": "range",
      "id": "top_gradient_strength",
      "min": 40, "max": 100, "step": 5, "unit": "%",
      "label": "Força do degradê",
      "default": 100
    },
    {
      "type": "range",
      "id": "top_gradient_height",
      "min": 20, "max": 100, "step": 5, "unit": "%",
      "label": "Alcance do degradê (altura da foto)",
      "default": 50
    },
    { "type": "text", "id": "headline", "label": "Headline", "default": "Your headline here" }
  ],
  "presets": [{ "name": "Hero" }]
}
{% endschema %}
```

## Armadilhas

- **Gradiente linear de 2 stops.** Sintoma: uma linha visível onde o escuro "acaba", e a área escura lê como sombra suja sobre a foto em vez de se misturar nela. É o motivo de existir a curva de ~10 stops.
- **Degradê curto e forte.** Sintoma: mesmo com easing, um degradê de 15-20% de altura com alpha 1 no topo parece um tarja preta. Força e altura andam juntas — degradê forte pede alcance maior pra desmanchar; por isso os dois são settings.
- **Hard-codar força/altura no CSS.** Sintoma: a cada troca de foto no editor, o degradê fica forte demais ou fraco demais e a correção exige deploy. As CSS vars inline vindas do schema deixam o ajuste no editor, onde a foto está.
- **Multiplicar o alpha fora do `calc()`** (pré-calcular no Liquid). Funciona, mas quebra o live preview do editor: o range setting muda o estilo inline e o `calc()` recalcula na hora; valor pré-calculado exige re-render da section.
- **Esquecer `pointer-events: none` no `::before`.** Sintoma: a metade de cima do hero deixa de responder a clique (CTA, header sobreposto) — o pseudo-elemento está na frente capturando os eventos.
- **Colocar o degradê acima do conteúdo no `z-index`.** Sintoma: headline e CTA escurecem junto com a foto. A ordem é foto (0) → degradê (1) → conteúdo (2).
