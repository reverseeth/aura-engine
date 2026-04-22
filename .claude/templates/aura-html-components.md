# Aura HTML Components

Referência dos componentes reutilizáveis do design system Aura. Usado por TODA skill que gera `.html` dual output (regra 6b do CLAUDE.md).

O template base (`aura-report-template.html`) inclui CSS pra todos esses componentes. Adapta o conteúdo — não reinventa o CSS.

## Componentes disponíveis

### Estrutura

- `.section` — container de seção com padding vertical padrão
- `.container` — wrapper max-width 900px, centralizado
- `.section-label` — badge pequeno uppercase indicando tipo de seção ("MARKET RESEARCH", "OFFER", etc)
- `.divider` — linha horizontal sutil separadora

### Headings & hierarquia

- `h1` — título principal do report (30-36px)
- `h2` — seção (24-28px)
- `h3` — subseção (18-20px)
- `h4` — bloco interno (16-18px)
- `.eyebrow` — texto pequeno uppercase acima de heading pra contexto

### Call-outs (blocos de destaque)

- `.callout` — bloco informativo geral (bg suave, border-left accent)
- `.note` — nota auxiliar (italic, opacity 0.8)
- `.opportunity` — destaque de oportunidade (accent verde)
- `.danger` — alerta crítico (accent vermelho)
- `.winner` — destaque de conceito vencedor (accent gold)

### Prova & citação

- `.quote` — blockquote com estilo editorial (italic, border-left grosso)
- `.quote cite` — fonte da citação (bottom, small, opacity 0.7)
- `.pill` — tag/badge inline (small, rounded)
- `.kpi-grid` — grid responsivo de métricas (auto-fit minmax 200px)
- `.kpi-grid .kpi` — card individual dentro do grid (valor grande + label pequena)

### Tabelas

- `.table-wrap` — wrapper com overflow-x pra mobile
- `table` — base com bordas sutis, zebra stripes
- `th` — bold, uppercase, border-bottom mais pesado
- `td` — padding generoso, border-bottom sutil

### Código & dados

- `pre` — bloco de código com scroll horizontal
- `code` — inline code com bg sutil
- `.json-block` — JSON formatado com syntax highlighting suave (gray tones)

### Media

- `img.inline-img` — imagem inline responsiva com border-radius
- `.img-caption` — caption abaixo de imagem (small, italic)
- `.video-wrap` — wrapper 16:9 responsive pra embeds

### Navigation

- `.toc` — table of contents (top of long reports)
- `.back-to-top` — link "back to top" fixed bottom-right

### Logo

- `.logo-wrap` — wrapper com margin-bottom: 12px
- `.logo-wrap svg` — height 40px, width auto (regra obrigatória CLAUDE.md — logo SEMPRE SVG, NUNCA texto)

## Regras de uso

1. **Logo no topo do `<body>`** — SEMPRE o bloco SVG de `.claude/templates/aura-logo-snippet.html`, copiado literal. Proibido substituir por texto.
2. **CSS inline no `<style>`** — self-contained, sem server/externos
3. **Emojis ✅ ⚠️ ❌ OK em relatórios internos** (regra 7 CLAUDE.md exceção pra `/workspace/` reports) — NUNCA em páginas pro consumidor final
4. **Responsividade mobile obrigatória** — `overflow-wrap: anywhere` em code/callout pra não quebrar layout
5. **Contraste WCAG AA** — text primary sobre bg >= 4.5:1 em todo componente

## Extensão

Pra adicionar novo componente ao design system:

1. Adicionar o CSS em `aura-report-template.html` (dentro do `<style>`)
2. Documentar aqui com classe + propósito + exemplo mínimo HTML
3. Atualizar esta lista

**NÃO** criar componentes one-off sem adicionar ao template base — fragmenta design system e quebra consistência.

## Exemplo mínimo (esqueleto de report)

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Título do Report]</title>
  <style>
    /* copiar LITERAL de aura-report-template.html */
  </style>
</head>
<body>
  <!-- LOGO OBRIGATÓRIA — copiar literal de aura-logo-snippet.html -->
  <div class="logo-wrap">
    <svg viewBox="0 0 1789.33 925.59" ...>
      <path d="..." fill="#1A1A1A"/>
      ...
    </svg>
  </div>

  <div class="container">
    <span class="section-label">[Label]</span>
    <h1>[Título do report]</h1>

    <section class="section">
      <h2>Seção 1</h2>
      <p>Conteúdo...</p>

      <div class="callout">
        Bloco destacado com insight-chave.
      </div>
    </section>

    <!-- etc -->
  </div>
</body>
</html>
```
