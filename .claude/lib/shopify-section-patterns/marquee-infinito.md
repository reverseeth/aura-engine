# Marquee infinito (faixa de logos sem emenda visível)

## O problema

A receita clássica de marquee — uma esteira `width: max-content` com N cópias do conteúdo e um `@keyframes` animando `translateX(-1/N * 100%)` — quebra no aparelho real de dois jeitos. Primeiro: as cópias nunca têm exatamente a mesma largura, porque o browser arredonda cada item pra subpixel de forma independente; a diferença de fração de pixel entre as cópias vira um salto visível na emenda a cada volta do loop. Segundo, e pior: se as imagens da faixa carregam com `loading="lazy"` (ou sem `width`/`height` intrínsecos), elas entram DEPOIS que a animação começou — a esteira muda de largura no meio do loop, o percentual do `translateX` passa a apontar pra outro lugar, e a faixa dá um tranco na frente do cliente.

Teste em headless com cache quente NÃO pega nenhum dos dois: as imagens vêm do cache antes do primeiro frame e a largura nunca muda durante a medição. O bug só existe em rede real, primeira visita, aparelho de verdade.

## A solução

- **N cópias idênticas do trilho** (4 funciona bem) dentro de uma esteira única; só a primeira cópia é "real" — as demais levam `aria-hidden="true"`.
- **Imagens `eager` com `width`/`height` intrínsecos** no `image_tag`: a esteira nasce com a largura final, sem reflow durante a animação.
- **Animação por JS em PIXELS**, não em percentual: `requestAnimationFrame` mede o tempo real entre frames e move `x -= largura / (veloc * 1000) * dt`; o loop fecha por módulo (`if (x <= -largura) x += largura`). Como a posição é em pixels medidos, subpixel e reflow deixam de importar.
- **Re-medição da largura** do trilho em `resize` E no `load` de cada imagem que ainda não completou — se algo mudar a largura, o loop se ajusta no frame seguinte, sem salto.
- **CSS keyframes mantido só como fallback sem JS**: quando o script roda, ele adiciona a classe `.is-js` que desliga a animação CSS (`animation: none`).
- **`prefers-reduced-motion` respeitado** nos dois caminhos (CSS e JS).
- **Pausa em hover** via flag no loop JS (e `animation-play-state: paused` no fallback CSS).

## Código de referência

```liquid
<style>
  .sec-press {
    background: rgb(var(--sec-bg));
    color: rgb(var(--sec-soft));
    padding-block: 22px;
    border-top: 1px solid rgb(var(--sec-line));
    border-bottom: 1px solid rgb(var(--sec-line));
    overflow: hidden;
  }
  .sec-press .sec-press__marquee {
    display: flex;
    width: 100%;
    overflow: hidden;
  }
  .sec-press .sec-press__belt {
    display: flex;
    flex: 0 0 auto;
    width: max-content;
    /* fallback sem JS; com JS, o script anima em pixels medidos */
    animation: sec-press-scroll var(--sec-press-speed, 16s) linear infinite;
    will-change: transform;
  }
  .sec-press .sec-press__belt.is-js { animation: none; }
  .sec-press .sec-press__track {
    display: flex;
    align-items: center;
    flex: 0 0 auto;
    width: max-content;
  }
  .sec-press .sec-press__marquee:hover .sec-press__belt {
    animation-play-state: paused;
  }
  /* 28px de cada lado = 56px entre itens, inclusive na emenda entre cópias */
  .sec-press .sec-press__item {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 0 28px;
  }
  .sec-press .sec-press__item img {
    display: block;
    width: auto;
    max-width: 180px;
    height: auto;
    max-height: 30px;
    object-fit: contain;
  }
  .sec-press .sec-press__label {
    white-space: nowrap;
    text-transform: uppercase;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.18em;
  }
  @keyframes sec-press-scroll {
    from { transform: translateX(0); }
    to { transform: translateX(-25%); } /* 1 de 4 cópias: o quadro final é idêntico ao inicial */
  }
  @media (max-width: 749px) {
    .sec-press .sec-press__item { padding: 0 20px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .sec-press .sec-press__belt { animation: none; }
  }
</style>

<section class="sec-press" data-section="sec-press" style="--sec-press-speed: {{ section.settings.speed | default: 16 }}s;">
  {%- if section.blocks.size > 0 -%}
    <div class="sec-press__marquee">
      <div class="sec-press__belt">
      {%- for copy in (1..4) -%}
        <div class="sec-press__track"{% if forloop.index > 1 %} aria-hidden="true"{% endif %}>
          {%- for block in section.blocks -%}
            <div class="sec-press__item"{% if copy == 1 %} {{ block.shopify_attributes }}{% endif %}>
              {%- if block.settings.logo != blank -%}
                {%- comment -%} eager + dimensões intrínsecas: a esteira nasce com a largura final {%- endcomment -%}
                {{ block.settings.logo | image_url: width: 400 | image_tag: loading: 'eager', width: block.settings.logo.width, height: block.settings.logo.height, alt: block.settings.label }}
              {%- else -%}
                <span class="sec-press__label">{{ block.settings.label }}</span>
              {%- endif -%}
            </div>
          {%- endfor -%}
        </div>
      {%- endfor -%}
      </div>
    </div>
  {%- endif -%}
</section>

<script>
  /* Marquee em pixels: mede a largura real de UMA cópia e fecha o loop por módulo.
     Re-mede em resize e quando cada imagem carrega — a emenda nunca salta. */
  (function () {
    var sec = document.querySelector('.sec-press');
    var marquee = sec && sec.querySelector('.sec-press__marquee');
    var belt = sec && sec.querySelector('.sec-press__belt');
    var primeira = belt && belt.querySelector('.sec-press__track');
    if (!sec || !marquee || !belt || !primeira) return;
    if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    belt.classList.add('is-js');
    var veloc = parseFloat(getComputedStyle(sec).getPropertyValue('--sec-press-speed')) || 16; /* s por cópia */
    var x = 0, largura = 0, anterior = null, pausado = false;
    function medir() { largura = primeira.getBoundingClientRect().width; }
    medir();
    addEventListener('resize', medir);
    belt.querySelectorAll('img').forEach(function (img) {
      if (!img.complete) img.addEventListener('load', medir);
    });
    marquee.addEventListener('mouseenter', function () { pausado = true; });
    marquee.addEventListener('mouseleave', function () { pausado = false; });
    function quadro(t) {
      if (anterior !== null && !pausado && largura > 0) {
        x -= (largura / (veloc * 1000)) * (t - anterior);
        if (x <= -largura) x += largura;
        belt.style.transform = 'translate3d(' + x.toFixed(2) + 'px, 0, 0)';
      }
      anterior = t;
      requestAnimationFrame(quadro);
    }
    requestAnimationFrame(quadro);
  })();
</script>

{% schema %}
{
  "name": "Press Marquee",
  "max_blocks": 12,
  "settings": [
    {
      "type": "range",
      "id": "speed",
      "label": "Velocidade do marquee",
      "min": 10,
      "max": 60,
      "step": 1,
      "unit": "s",
      "default": 16
    }
  ],
  "blocks": [
    {
      "type": "logo",
      "name": "Logo",
      "settings": [
        { "type": "image_picker", "id": "logo", "label": "Logo (imagem)" },
        { "type": "text", "id": "label", "label": "Texto (aparece quando nao ha imagem)", "default": "PRESS" }
      ]
    }
  ],
  "presets": [
    {
      "name": "Press Marquee",
      "blocks": [
        { "type": "logo", "settings": { "label": "AS SEEN IN" } },
        { "type": "logo", "settings": { "label": "[OUTLET ONE]" } },
        { "type": "logo", "settings": { "label": "[OUTLET TWO]" } },
        { "type": "logo", "settings": { "label": "[OUTLET THREE]" } }
      ]
    }
  ]
}
{% endschema %}
```

## Armadilhas

- **Animar só com CSS em percentual sobre `max-content`.** Sintoma: a faixa roda lisa no preview e dá um tranco na emenda no celular do cliente — o salto acontece exatamente quando uma imagem termina de carregar ou quando as cópias divergem por subpixel.
- **Deixar as imagens em `loading="lazy"` ou sem `width`/`height`.** Sintoma: a esteira "encolhe e estica" nos primeiros segundos; com animação percentual, cada carga é um pulo.
- **Medir a largura uma vez só, no parse.** Sintoma: depois de girar o celular (ou redimensionar a janela), a emenda passa a saltar — a largura guardada não é mais a real. A medição precisa reagir a `resize` e ao `load` de cada imagem.
- **Confiar no teste headless.** Cache quente entrega as imagens antes do primeiro frame; o cenário que quebra (rede real, primeira visita) nunca acontece na máquina de teste. Validar com cache desabilitado e throttling de rede.
- **Esquecer o fallback sem JS.** Se o script falhar (bloqueador, erro em outro script da página), a faixa fica parada. O `@keyframes` continua no CSS como plano B; a classe `.is-js` só o desliga quando o loop em pixels de fato assumiu.
- **Ignorar `prefers-reduced-motion`.** O loop JS precisa checar a media query e sair antes de animar — não basta a regra CSS, porque o script sobrepõe o `transform` inline.
