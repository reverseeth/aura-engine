# Sticky add-to-cart (botão fixo que some sobre a oferta e o footer)

## O problema

Um botão de compra fixo no rodapé da tela aumenta conversão em landing longa, mas cria três bugs clássicos. Um: se ele fica visível SOBRE a própria seção de oferta (ou sobre o footer), vira ruído — dois CTAs competindo na mesma tela e um botão flutuando sobre links de rodapé. Dois: o script que arma o observador costuma rodar dentro da section do header, que é parseada ANTES da seção de oferta existir no DOM — o `querySelector` volta `null`, o observador nunca arma, e o botão ou nunca aparece ou nunca some. Três: no mobile, o glow (sombras em camadas) do botão é cortado pelas bordas do viewport, porque a sombra se estende além da caixa e o botão está colado nas margens.

Um detalhe de UX na mesma seção: CTAs que ancoram na oferta com `href="#oferta"` levam o TOPO da seção pro topo da tela — e as opções de compra (o que o cliente precisa ver) ficam abaixo da dobra.

## A solução

- **Chip de preço por unidade dentro do botão** (`$X/dia`, `$X/unidade`): o botão fixo carrega a âncora de valor junto com o CTA.
- **`IntersectionObserver` com um `Map` de alvos**: o botão se esconde se QUALQUER alvo (seção de oferta OU footer) está intersectando. O `Map` guarda o estado de cada alvo; a cada callback, o botão fica oculto se algum valor do `Map` é `true`. Um observador só com um alvo não cobre o footer; dois observadores separados brigam entre si.
- **Armar o observador só em `DOMContentLoaded`** (ou imediatamente, se `readyState` já passou de `loading`): garante que a oferta e o footer já existem no DOM quando o `querySelector` roda.
- **Esconder com classe + transição**, não com `display: none` seco: `opacity` + `translateY` dão a saída suave. O atributo `hidden` inicial evita flash antes do observador armar — o script o remove quando está pronto.
- **Mobile: encolher as sombras e afastar o botão das bordas** (`left`/`right`/`bottom` maiores que no desktop). O halo precisa de espaço pra "respirar" dentro do viewport; sem o offset, é cortado seco nas laterais.
- **CTAs ancoram nas OPÇÕES da oferta com `scrollIntoView({ block: 'center' })`**: um listener global de clique intercepta âncoras pra oferta e centraliza o bloco de opções na tela, em vez de deixar o topo da seção esconder as opções abaixo da dobra.

## Código de referência

```liquid
<style>
  .sec-sticky {
    position: fixed;
    left: 16px;
    right: 16px;
    bottom: 16px;
    z-index: 70;
    display: flex;
    justify-content: center;
    pointer-events: none;
    opacity: 1;
    transform: none;
    transition: opacity 0.35s ease, transform 0.35s ease;
  }
  .sec-sticky.is-hidden, .sec-sticky[hidden] {
    opacity: 0;
    transform: translateY(14px);
    pointer-events: none;
    display: flex;
  }
  .sec-sticky__btn {
    pointer-events: auto;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    min-height: 58px;
    padding: 17px 34px;
    border-radius: 999px;
    background: rgb(var(--sec-accent));
    color: rgb(255, 255, 255);
    text-decoration: none;
    font-size: 16px;
    font-weight: 600;
    white-space: nowrap;
    box-shadow:
      0 16px 42px rgba(var(--sec-accent), 0.45),
      0 4px 14px rgba(var(--sec-accent), 0.32),
      0 2px 10px rgba(0, 0, 0, 0.18),
      inset 0 1px 0 rgba(255, 255, 255, 0.24);
    transition: transform 0.25s ease, background 0.25s ease;
  }
  .sec-sticky__btn:hover { background: rgb(var(--sec-accent-deep)); transform: translateY(-2px); }
  .sec-sticky__price {
    padding: 5px 11px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.18);
    font-size: 13.5px;
    font-weight: 600;
    line-height: 1;
  }
  @media (max-width: 749px) {
    /* glow mais compacto e botão mais afastado das bordas: a sombra respira sem sair do viewport */
    .sec-sticky { left: 20px; right: 20px; bottom: 22px; }
    .sec-sticky__btn {
      width: 100%;
      box-shadow:
        0 8px 18px rgba(var(--sec-accent), 0.40),
        0 3px 8px rgba(var(--sec-accent), 0.30),
        0 1px 6px rgba(0, 0, 0, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 0.24);
    }
  }
</style>

{%- if section.settings.sticky_cta -%}
<div class="sec-sticky" data-sec-sticky hidden>
  <a class="sec-sticky__btn" href="#sec-offer-options">
    {{ section.settings.sticky_label | escape }}
    <span class="sec-sticky__price">{{ section.settings.sticky_price | escape }}</span>
  </a>
</div>
{%- endif -%}

<script>
  (function () {
    /* CTAs #sec-offer levam as OPÇÕES da oferta pro centro da tela */
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href$="#sec-offer"], a[href$="#sec-offer-options"]');
      if (!a) return;
      var alvo = document.getElementById('sec-offer-options') || document.getElementById('sec-offer');
      if (!alvo) return;
      e.preventDefault();
      alvo.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });

    /* CTA fixo: visível na página toda, some enquanto oferta ou footer estão na tela.
       Arma só depois do parse completo (a oferta vem depois do header no DOM). */
    function armarSticky() {
      var sticky = document.querySelector('[data-sec-sticky]');
      if (!sticky || !('IntersectionObserver' in window)) return;
      var alvos = ['[data-section="sec-offer"]', '[data-section="sec-footer"]']
        .map(function (sel) { return document.querySelector(sel); })
        .filter(Boolean);
      if (!alvos.length) return;
      var visiveis = new Map();
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (en) { visiveis.set(en.target, en.isIntersecting); });
        var algum = false;
        visiveis.forEach(function (v) { if (v) algum = true; });
        sticky.classList.toggle('is-hidden', algum);
      }, { threshold: 0.04 });
      alvos.forEach(function (a) { io.observe(a); });
      sticky.removeAttribute('hidden');
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', armarSticky);
    else armarSticky();
  })();
</script>
```

Settings de schema correspondentes:

```json
{ "type": "checkbox", "id": "sticky_cta", "label": "Mostrar o botão fixo", "default": true },
{ "type": "text", "id": "sticky_label", "label": "Texto do botão", "default": "Shop now" },
{ "type": "text", "id": "sticky_price", "label": "Preço por unidade no chip", "default": "$0.00/day" }
```

## Armadilhas

- **Armar o observador no parse da section.** Sintoma: o botão nunca aparece (o `hidden` inicial nunca é removido) ou nunca some sobre a oferta — o `querySelector` rodou antes da seção de oferta existir e voltou `null` em silêncio. O script TEM que esperar `DOMContentLoaded`.
- **Observar só a oferta.** Sintoma: o botão flutua sobre o footer, cobrindo links de política e pagamento. O `Map` de alvos existe pra tratar oferta E footer com um observador só.
- **Dois observadores separados (um por alvo) escrevendo na mesma classe.** Sintoma: o botão pisca — o callback de um alvo desfaz o que o outro acabou de fazer. Um observador, um `Map`, uma decisão.
- **Sombra grande colada na borda no mobile.** Sintoma: o glow aparece "cortado a régua" nas laterais e embaixo. Sombra estendida precisa de offset das bordas do viewport (e de uma versão mais compacta no breakpoint mobile).
- **Âncora no topo da seção de oferta.** Sintoma: o clique no CTA rola a página e o cliente vê o título da oferta, mas as opções de compra ficam abaixo da dobra. Ancorar no bloco de OPÇÕES com `block: 'center'`.
- **Esconder com `display: none` direto.** Sintoma: o botão some e reaparece em corte seco, sem transição — e `display` não anima. A classe `.is-hidden` mantém `display: flex` e anima `opacity`/`transform`.
