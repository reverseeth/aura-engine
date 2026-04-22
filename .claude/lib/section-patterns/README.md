# Section Patterns

Biblioteca de padrões reutilizáveis pra sections Liquid/HTML em PDPs, landing pages e advertoriais. Usada pela Skill 06 (page-engine) e skills derivadas (06a/06b/06c) pra gerar código consistente.

## Estrutura

- `patterns.json` — definição estruturada de cada pattern (id, nome, quando usar, blocks/settings típicos, responsive behavior)
- Este README — descrição humana

## Por que isso existe

Toda PDP/LP ecommerce usa ~15 patterns recorrentes. Em vez de gerar do zero a cada skill run, carregamos esses patterns como reference structures. A AI adapta o conteúdo (copy/imagens/cores), mas a estrutura Liquid é consistente — menos bugs, mais facilidade de edição no theme editor.

## Patterns (catálogo base)

### 1. Hero (5 variantes)

- `hero-authority` — expert/doctor endorsement, foto de autoridade + claim forte
- `hero-ugc` — frame de customer real + quote + rating
- `hero-product` — produto centralizado, claim emocional, clean aesthetic
- `hero-problem-agitate` — dor visual + escalation + bridge pro produto
- `hero-lifestyle` — cenário aspiracional + produto incidental

Cada variante com blocks: eyebrow, headline, subheadline, hero_image/video, primary_cta, trust_row.

### 2. Mechanism explainer

Como o mecanismo único funciona. Estrutura: causa-raiz (1 parágrafo) → como o produto endereça (3 passos visuais com ícone SVG + texto curto) → diferenciador vs alternativas (comparison table).

### 3. Proof stack

Camadas de prova empilhadas: badges de mídia/certificação (row superior), rating score + review count, before-after gallery (carousel), expert endorsement (foto + quote + credencial), ingredient spotlight com evidence (linka `04-research-foundation.json`).

### 4. Comparison table

Seu produto vs concorrente-tipo vs alternativa genérica. Mobile: vira cards empilhados (não scroll horizontal). 5-7 linhas de comparação MAX, cada uma um benefício rastreável.

### 5. FAQ

10-15 perguntas cobrindo: objeções do market research, product usage, shipping/returns, guarantee specifics, who-this-is-for. Accordion pattern com schema FAQ (structured data SEO).

### 6. Offer block / value stack

Produto + bonuses empilhados com valor ancorado vs preço real. Seção visual impacta conversão 10-30% quando bem feita.

### 7. Guarantee callout

Destaque visual da garantia (escudo/badge SVG) + copy curta + prazo + condições.

### 8. Bundle selector

Radio buttons ou tabs pra escolher 1x / 3x / 6x. Mostra preço-por-unidade + savings. Pre-select do "Popular" (3-pack tipicamente).

### 9. Trust row

Linha de 3-5 badges (Free US shipping / Money-back / Secure checkout / Rating X) com ícone SVG + label curta. 16-18px de height, stroke 1.5-2px, opacity 0.7-0.8.

### 10. Final CTA

Reforço de oferta + stack resumido + preço riscado (se tiver ancora) + CTA primário grande + guarantee reminder + trust row final.

### 11. Advertorial-specific: Story hero

Parágrafo longo com first-person storytelling, imagem lateral ou topo, sem CTA direto (CTA vem no final da página).

### 12. Research / evidence section

Citações diretas de `04-research-foundation.json` com fonte linkada. Usa `.quote` component, com `cite` meta-link.

### 13. Video embed

Wistia/YouTube responsive embed. Se video é demo, colocar próximo ao offer block. Se é founder-story, colocar como hero.

### 14. Sticky ATC bar (mobile)

Barra fixa bottom em mobile com nome do produto + preço + CTA. Aparece após scroll > hero.

### 15. Eyebrow / promo banner (time-bound)

Banner topo com promo + countdown opcional. Schema time-bound (start/end date, render conditional). Ver `time-bound-promo.md` pra pattern dedicado.

## Regras comuns aplicadas a TODOS os patterns

1. **Schema-driven**: toda section Liquid expõe settings/blocks no schema pra o membro editar no theme editor sem mexer código.
2. **Conditional rendering**: `{% if section.settings.enabled %}` wrapping pra o membro poder ligar/desligar cada block.
3. **`data-*` preservation**: ao editar section existente, preservar todos os atributos `data-*` usados por apps (Klaviyo, Judge.me, Loox, Shop Pay) — deletar um `data-*` quebra a integração.
4. **Table → cards responsive**: `<table>` só funciona bem em desktop; em mobile (< 768px) virar cards empilhados via CSS grid.
5. **Ícones SVG inline, nunca emoji**: regra 7 do CLAUDE.md.
6. **Color via CSS vars inline**: `style="background: {{ section.settings.bg_color }}"` pra o membro editar cores sem tocar CSS.
7. **Forms com `/cart/add`**: todo ATC usa `<form action="/cart/add" method="post">` com `id` escondido. Nunca JS custom pra add-to-cart (quebra Shop Pay, dynamic checkout buttons).

## Integração com Skill 06

- `06a-page-planning.md`: consulta patterns pra decidir estrutura da página baseado em awareness/sophistication + tipo de página (PDP/LP/Advertorial).
- `06b-page-sections.md`: cada section Liquid é gerada a partir do pattern correspondente, adaptando conteúdo ao brand snapshot + blueprint do Claude Design.
- `06c-page-deploy.md`: valida que sections finais respeitam patterns antes de push (smoke test de estrutura).
