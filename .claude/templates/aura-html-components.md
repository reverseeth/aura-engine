# Aura HTML Components — v5 "Premium / Liquid Glass"

Referência dos componentes do design system Aura. Usado por TODA skill que gera `.html` dual output de relatório (regra 6b do CLAUDE.md — arquivos operacionais de handoff como `dados.json`/`scale-directives.md` são isentos).

A fonte única de verdade é **`aura-report-template.html`** (v5). Esta doc é o mapa: lista cada classe e quando usar. **Não reinvente CSS** — copie o `<head>` + `<style>` + `<script>` do template e adapte só o conteúdo.

> Estética v5: moderno, light, premium (Apple / Human Academy / academypass.ai). Sans geométrica (Satoshi → Inter). Fundo com **glow ambiente** sutil. Cards em **liquid glass** (frosted, `backdrop-blur`). Stats gigantes com divisores. **Animações**: reveal no scroll, count-up nos números, hover-lift nos cards. Tudo com progressive enhancement (visível sem JS).

---

## Como montar um report (3 cópias literais + 1 logo)

Todo `.html` de report é montado copiando **literalmente** do template, nesta ordem:

1. **O `<head>` inteiro** — inclui os `<link>` das fontes (Satoshi via Fontshare + Inter via Google), a meta CSP, e o `<style>` completo do design system. Não edite o CSS.
2. **A logo** no topo do `<body>` — bloco SVG de `.claude/templates/aura-logo-snippet.html`, com a classe `logo-wrap reveal`. NUNCA texto (regra 6b).
3. **O conteúdo** — dentro de `<div class="container">`, usando as classes abaixo. Adapte só o conteúdo.
4. **O `<script>` no fim do `<body>`** — copiado literal. Liga as animações (reveal + count-up). Sem ele, tudo aparece estático (progressive enhancement), mas com ele o report ganha vida.

Estrutura final: `<head>` (fontes+CSP+style) → `<body>` → `.container` → logo → header → seções → `.footer` → `<script>`.

---

## Convenções de animação (v5 — não esquecer)

São o que separa um report v5 de um report "morto". Três regras:

1. **Classe `reveal`** — adicione em CADA bloco de primeiro nível que deve entrar animado: logo, `h1.page-title`, `p.page-subtitle`, `.meta-bar`, `.toc`, cada `.section-label`, cada `.subsection`, `.kpi-grid`, `.table-wrap`, `.quote`, `.note`, `.callout`, `.opportunity`, `.danger`, `.winner`, `.faq`, `.check-row`, etc. O `<script>` observa esses elementos e revela no scroll.
2. **`data-count` nos números gigantes** — todo `.big-num` recebe `data-count="58"` + opcional `data-suffix="%"` / `data-prefix="$"`, e o texto visível como fallback. Ex: `<div class="big-num" data-count="58" data-suffix="%">58%</div>`. O count-up anima de 0 ao valor quando entra na viewport. Sem JS, mostra o fallback.
3. **Progressive enhancement** — o `<script>` adiciona `class="js"` no `<html>`; o CSS só esconde `.reveal` quando `.js` está presente. Logo: sem JS, nada fica invisível. `prefers-reduced-motion` desliga tudo automaticamente.

---

## Tokens (já no `:root` do template — referência)

- Cores: `--bg:#EFF1F5` (fundo cool light), `--surface:#FFFFFF`, `--ink:#14161D` (texto forte), `--ink-2:#3A3E4A`, `--muted:#565B68`, `--faint:#9499A5`, `--line:#E5E7EE`.
- Accent: `--accent:#2D5BFF` (indigo), `--accent-2:#7C5CFF` (violeta — o tom dos glows/halos; no CSS os glows usam esse tom em rgba literal).
- Semânticas: `--green:#0E9F6E`, `--red:#E5484D`, `--amber:#B7791F` (+ variantes `-soft`).
- Glass: `--glass:rgba(255,255,255,.62)`, `--glass-line:rgba(255,255,255,.75)`.
- Tipografia: `--display:'Satoshi'` (títulos/números), `--sans:'Inter'` (corpo), `--mono` (código/VOC).
- Raio/sombra: `--r:22px`, `--r-sm:16px`, `--shadow`, `--shadow-sm`, `--shadow-lift` (hover).

---

## Componentes

### Estrutura & header

- `.container` — wrapper max-width 840px, centralizado. Tudo vai dentro.
- `.page-title` — H1 gigante (clamp 40-62px, Satoshi). O título do report.
- `.page-subtitle` — deck abaixo do título (19px, muted, max 60ch).
- `.meta-bar` — barra de metadados em **grid glass** (auto-fit minmax 160px). Cada `<div><strong>Label</strong> valor</div>`; o `strong` vira overline uppercase. Use pra Produto · Mercado · Data · Alimenta (report em `en`: Product · Market · Date · Feeds).
- `.toc` / `.toc-title` — sumário com `<ol>` numerado (decimal-leading-zero), hover desliza.
- `.section` — bloco de seção (margin-bottom grande). Use `id` pra ancorar do TOC.
- `.section-label` — label da seção com `<span class="num">01</span>Título` + régua que esvai.
- `.subsection` / `.subsection-title` — subdivisão (Satoshi 27px).
- `hr` — divisor sutil entre grandes blocos.

### Texto

- `p`, `p strong`, `ul`/`ol`/`li`, `code` (inline mono, `overflow-wrap:anywhere` pra não quebrar mobile).

### Call-outs (cards glass com overline-label + glow leve)

Em todos, o **primeiro `<strong>` vira o rótulo** (uppercase, display:block). Ex: `<div class="callout"><strong>Recomendação</strong> texto...</div>`.

- `.note` — nota auxiliar neutra.
- `.callout` — destaque informativo/recomendação (glow indigo).
- `.opportunity` — gap/oportunidade (glow verde).
- `.danger` — alerta crítico, erro a evitar (glow vermelho).

### Winner (conceito vencedor — dark glass + halo violeta)

```html
<div class="winner reveal">
  <div class="winner-label">Winner</div>
  <div class="winner-name">Nome do mecanismo</div>
  <p>Por que vence.</p>
</div>
```

### KPIs / stats gigantes (painel glass com divisores)

```html
<div class="kpi-grid reveal">
  <div class="kpi-card"><div class="big-num" data-count="58" data-suffix="%">58%</div><div class="big-num-label">label da métrica</div></div>
  <div class="kpi-card"><div class="big-num" data-count="34" data-suffix="%">34%</div><div class="big-num-label">label</div></div>
</div>
```
`.big-num` e `.big-num-label` se auto-ordenam (número em cima, label embaixo) via `order` — independe da ordem no HTML.

### Prova & citação

- `.quote` + `.quote-source` — VOC / frase exata do cliente em card glass mono. `.quote-source` é a fonte (Reddit, review, etc).
- `.voc-words` (wrapper) com `<span>` por palavra — nuvem de termos exatos do mercado.
- `.script-block` — bloco de script/roteiro (mono, pre-wrap).

### Pills / badges (liquid glass) & scores

- `.pill` + variante: `.pill-win`/`.pill-rare`/`.pill-ok` (verde), `.pill-saturated`/`.pill-bof`/`.pill-pending` (vermelho), `.pill-common`/`.pill-mof` (âmbar), `.pill-absent`/`.pill-tof` (indigo).
- `.score` + `.score-high`/`.score-mid`/`.score-low` — nota inline.

### Tabelas

- `.table-wrap` (overflow-x mobile) envolvendo `table`/`th`/`td`. Use `.pill` na célula de status.

### Cards de domínio

- `.brand-card`, `.concept-card` — cards de marca/conceito (radius `--r`, hover-lift).
- `.tier-card` (+ `.popular` pra destacar plano) — card de pricing/tier.
- `.timeline-day` (+ `.timeline-day-label` — badge do dia) + `.timeline`/`.timeline-row`/`.timeline-time`/`.timeline-label`/`.timeline-content` — cronograma.
- `.primary-text-box` + `.pt-label` — bloco de Primary Text de ad.
- `.faq` + `.faq-q`/`.faq-a` — perguntas/objeções.
- `.hook-row` + `.hook-label`/`.hook-text`/`.hook-use` — hooks de criativo.
- `.headline-card` (+ `.top`) + `.hl-num`/`.hl-justify` — headlines com justificativa.
- `.ascii-map` — diagrama ASCII (mono, scroll-x).
- `.check-row` + `.check-icon` — sanity checks / itens validados.

### Advertorial

- `.advertorial` (card glass grande) + `.adv-kicker`, `.adv-headline`, `.adv-deck`, `.adv-byline`, `.adv-section-label`, `.advertorial p`, `.adv-cta` (botão escuro).

### Logo & footer

- `.logo-wrap` (`reveal`) — SVG da logo, height 28px. SEMPRE SVG, NUNCA texto.
- `.footer` — rodapé. Texto: **`Aura © [ano corrente da geração do report]`** (ex: `Aura © 2026` num report gerado em 2026), nada mais.

---

## Regras de uso

1. **Logo no topo do `<body>`** — bloco SVG de `aura-logo-snippet.html`, literal, com `reveal`. Proibido texto.
2. **`<head>` + `<style>` + `<script>` copiados literais** do template — self-contained, fontes via `<link>`, sem editar CSS.
3. **`reveal` nos blocos de topo + `data-count` nos `.big-num`** — senão o report fica estático.
4. **Emojis ✅ ⚠️ ❌ OK em report interno** (exceção regra 7) — NUNCA em página pro consumidor final.
5. **Mobile** — `overflow-wrap:anywhere` em `code`, `.quote` e nos callouts (`.note`/`.callout`/`.opportunity`/`.danger`) — o CSS do template já aplica; o `@media (max-width:640px)` já trata `.kpi-grid`, `.winner`, `.timeline` etc.
6. **Footer = `Aura © [ano corrente]`** — o ano da geração do report (o mesmo da meta-bar Data), nada mais.
7. **Idioma do chrome segue o `report_language`** — pra membro `en`: `<html lang="en">`, toc-title "Contents", meta-bar "Product/Market/Date/Feeds". Pra `pt-BR` (default), mantenha o chrome do template como está.

## Extensão

Pra adicionar componente novo: (1) adiciona o CSS em `aura-report-template.html` dentro do `<style>`; (2) documenta aqui (classe + propósito); (3) NÃO crie componente one-off sem adicionar ao template — fragmenta o design system.

---

## Esqueleto mínimo (v5)

```html
<!DOCTYPE html>
<html lang="pt-BR"> <!-- report_language "en" → lang="en" + chrome em inglês (regra 7 acima) -->
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Título] — Aura Engine</title>
  <!-- COPIAR LITERAL de aura-report-template.html: <link> das fontes + meta CSP + <style> inteiro -->
</head>
<body>
  <div class="container">

    <!-- LOGO — copiar literal de aura-logo-snippet.html -->
    <div class="logo-wrap reveal" role="img" aria-label="Aura Engine">
      <svg viewBox="0 0 1789.33 925.59" ...><title>Aura Engine</title><path d="..." fill="#14161D"/></svg>
    </div>

    <h1 class="page-title reveal">[Título]</h1>
    <p class="page-subtitle reveal">[Deck]</p>
    <div class="meta-bar reveal">
      <div><strong>Produto</strong> [nome]</div>
      <div><strong>Mercado</strong> [mercado]</div>
      <div><strong>Data</strong> [data]</div>
      <div><strong>Alimenta</strong> [próxima fase]</div>
    </div>

    <div class="section" id="s1">
      <div class="section-label reveal"><span class="num">01</span>[Seção]</div>
      <p>Conteúdo...</p>
      <div class="callout reveal"><strong>Recomendação</strong> insight-chave.</div>
    </div>

    <p class="footer">Aura © [ano corrente]</p>
  </div>

  <!-- ANIMAÇÃO — copiar literal o <script> de aura-report-template.html -->
  <script>/* reveal + count-up */</script>
</body>
</html>
```
