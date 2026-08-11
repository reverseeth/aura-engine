# Badges sobre imagem (selos de vidro editáveis na foto do produto)

## O problema

Selos flutuando sobre a foto do produto ("Hypoallergenic", "Free shipping") precisam de três coisas que a implementação ingênua erra. Contraste: pill clara sobre foto clara (ou escura sobre escura) desaparece — o selo precisa de um fundo próprio que funcione sobre QUALQUER foto que o membro escolher no editor. Clique: uma camada absoluta cobrindo o topo da imagem rouba os eventos de ponteiro de tudo que está embaixo. E edição: selos hard-codados no markup obrigam deploy a cada mudança de texto — num fluxo em que quem edita é o membro, no editor do tema.

Tem ainda o problema do vidro no mobile: `backdrop-filter: blur()` tem jank conhecido no Safari iOS (repaint travado durante scroll, flicker em camadas sobrepostas). O efeito de vidro que fica bonito no desktop precisa de um fallback sólido no breakpoint mobile.

## A solução

- **Camada de ancoragem + gradiente de base**: um contêiner absoluto no topo da imagem (`top: 0; left: 0; right: 0`) com um degradê escuro que desmancha pra baixo — é ele que garante o contraste das pills sobre qualquer foto. `pointer-events: none` na camada inteira: os selos são decorativos, o clique atravessa.
- **Pills de vidro**: fundo `rgba(var(--sec-dark), 0.55)` + `backdrop-filter: blur(8px)` + borda branca translúcida. No `≤860px`, o `backdrop-filter` sai e o fundo escurece pra sólido fosco (`rgba(var(--sec-dark), 0.82)`) — mesmo efeito visual, sem o jank do Safari iOS.
- **Cada badge = um par de settings**: `text` (o rótulo) + `html` (o ícone como SVG inline). Ícone é sempre SVG, nunca emoji — o SVG herda `currentColor`, escala limpo e não muda de aparência entre sistemas operacionais.
- **1 a 3 badges**, cada um só renderiza se o texto não está vazio (`!= blank`): o membro liga e desliga selos apagando o campo, sem mexer em código.
- **`z-index: 2`** na camada — acima da imagem, abaixo de qualquer conteúdo interativo da section.

## Código de referência

```liquid
<style>
  .sec-media { position: relative; }
  .sec-media__badges {
    position: absolute;
    top: 0; left: 0; right: 0;
    z-index: 2;
    padding: 14px 14px 34px;
    background: linear-gradient(180deg, rgba(var(--sec-dark), 0.5), rgba(var(--sec-dark), 0));
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    pointer-events: none;
    border-radius: 20px 20px 0 0; /* acompanha o raio do frame da imagem */
  }
  .sec-media__badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 13px;
    border-radius: 999px;
    border: 1px solid rgba(255, 255, 255, 0.28);
    background: rgba(var(--sec-dark), 0.55);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: rgb(255, 255, 255);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
    white-space: nowrap;
  }
  .sec-media__badge svg { flex: none; }
  @media (max-width: 860px) {
    /* Safari iOS: backdrop-filter causa jank no scroll — fundo sólido fosco no lugar */
    .sec-media__badge {
      backdrop-filter: none;
      -webkit-backdrop-filter: none;
      background: rgba(var(--sec-dark), 0.82);
    }
  }
  @media (max-width: 749px) {
    .sec-media__badge { font-size: 11px; padding: 6px 11px; }
  }
</style>

<div class="sec-media">
  {%- if section.settings.badge_a != blank or section.settings.badge_b != blank or section.settings.badge_c != blank -%}
  <div class="sec-media__badges" aria-hidden="true">
    {%- if section.settings.badge_a != blank -%}
    <span class="sec-media__badge">{{ section.settings.icon_a }}<span>{{ section.settings.badge_a | escape }}</span></span>
    {%- endif -%}
    {%- if section.settings.badge_b != blank -%}
    <span class="sec-media__badge">{{ section.settings.icon_b }}<span>{{ section.settings.badge_b | escape }}</span></span>
    {%- endif -%}
    {%- if section.settings.badge_c != blank -%}
    <span class="sec-media__badge">{{ section.settings.icon_c }}<span>{{ section.settings.badge_c | escape }}</span></span>
    {%- endif -%}
  </div>
  {%- endif -%}
  {{ section.settings.image | image_url: width: 1430 | image_tag: loading: 'lazy', class: 'sec-media__img', alt: '' }}
</div>
```

Settings de schema (o par texto + ícone, repetido por badge):

```json
{ "type": "header", "content": "Selos sobre a imagem" },
{ "type": "text", "id": "badge_a", "label": "Selo 1 (vazio = não mostra)", "default": "[claim curto]" },
{
  "type": "html",
  "id": "icon_a",
  "label": "Ícone 1 (SVG inline)",
  "default": "<svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.75\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M12 2.8l7.2 2.9v5.2c0 4.9-3.1 8.3-7.2 10.3-4.1-2-7.2-5.4-7.2-10.3V5.7Z\"></path><path d=\"M8.8 11.9l2.2 2.3 4.2-4.6\"></path></svg>"
}
```

## Armadilhas

- **Camada de badges sem `pointer-events: none`.** Sintoma: o terço superior da imagem para de responder — zoom da foto, link no frame, qualquer clique morre na camada invisível.
- **Pill sem fundo próprio, contando com a foto.** Sintoma: o selo funciona com a foto de teste e desaparece quando o membro troca a imagem no editor. O gradiente de base + o fundo da pill garantem contraste sobre qualquer foto.
- **`backdrop-filter` sem fallback mobile.** Sintoma: no iPhone, as pills piscam ou o scroll engasga sobre a imagem. O breakpoint `≤860px` troca o vidro por sólido fosco — visualmente quase idêntico, sem o custo de render.
- **Emoji como ícone.** Sintoma: o selo muda de cara entre iOS/Android/desktop, não herda a cor do texto e escala serrilhado. SVG inline com `stroke="currentColor"` resolve os três.
- **Setting `text` pro ícone em vez de `html`.** Sintoma: o SVG aparece escapado como texto (`<svg...`) dentro da pill. Ícone entra por setting `html`; só o RÓTULO passa por `| escape`.
- **Badges hard-codados no markup.** Sintoma: toda mudança de claim vira tarefa de código. O padrão `!= blank` renderiza só o que o membro preencheu — o editor do tema é o lugar da edição.
