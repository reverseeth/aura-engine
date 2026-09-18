# Page Build · Referência: Referência técnica, checklist WCAG 2.1 AA e DO NOT

> As regras universais de acessibilidade a validar no output compilado e a lista do que nunca fazer nesta skill. Abra antes do push.

## Acessibilidade — checklist WCAG 2.1 AA (quality standard universal)

Regras universais que NÃO restringem design — garantem que qualquer página seja usável por todos. O `frontend-design` (`page-design`) já respeita; valide no output compilado:

- **Semântica:** `<h1>` 1×/página (hero); heading order sem pular níveis; `<section>/<article>/<header>/<main>` onde aplicável; `<button>` pra ações, `<a href>` pra navegação; FAQ com `<details><summary>` nativo.
- **Alt/labels:** todo `<img>` com `alt` descritivo (ou `alt=""` decorativo); `<button>` só-ícone com `aria-label`; ícone decorativo `aria-hidden="true"`; links com texto descritivo (nunca "clique aqui"); `<label for>` em forms.
- **Contraste:** texto normal ≥ 4.5:1; texto grande ≥ 3:1; UI/focus rings ≥ 3:1; cor nunca é o único indicador de estado. Liquid `color_contrast` filter valida.
- **Foco/teclado:** `:focus-visible` com outline visível em todo interativo; tab order = ordem visual; nada escondido atrás de hover-only; modais com focus trap.
- **Movimento:** `@media (prefers-reduced-motion: reduce)` desligando transitions/animations; auto-play com pause; nada piscando >3×/s.
- **Responsividade:** funciona em 320px; texto nunca em px pequeno (clamp, mínimo ≥14px body); touch targets ≥ 44×44px; legível a 200% zoom.

Validação: Lighthouse Accessibility ≥ 95; navegação só-teclado; VoiceOver/NVDA (headings + labels fazem sentido).

## DO NOT

- Usar o block NATIVO `custom_liquid` do Shopify (HTML cru não-editável). O nosso `custom_liquid` customizado (`type: "liquid"`) é OK porque é editável.
- Hardcode texto/imagens/cores no markup (sempre settings).
- Usar classes do tema pai (`.product-card`, `.btn`) — sempre namespace próprio (`page-[produto]-X`).
- Usar `asset_url`/caminhos hardcoded de imagem (sempre `image_picker`).
- `!important` em CSS; IDs em selectors (use classes).
- Importar libraries JS/CSS externas; jQuery/React/Vue/Tailwind no output final (vanilla CSS em `{% stylesheet %}`).
- Salvar um `.liquid` sem validar com `shopify-plugin:shopify-liquid`.
- Pushar no live sem backup + `--allow-live` + `--nodelete`.
- Pushar snippet/asset de paleta em lote genérico quando há mais de um tema ativo com paletas diferentes — arquivo de identidade é POR-TEMA (rule `shopify-theme-safety`, disciplina multi-tema).
- Pull depois de push não-verificado (marker ausente) — sobrescreve trabalho local.
- Criar sections que "só funcionam no Horizon" — sempre theme-agnostic, self-contained.
- Gerar Liquid por reasoning manual em vez de rodar o `liquid-converter.py` — a conversão é determinística por design.
