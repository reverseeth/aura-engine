# Design Clone — Aura Engine

Pipeline de 3 etapas pra clonar o design de uma página de concorrente e converter em Shopify Liquid sections editáveis. Usado pela skill `06-page-engine` no Modo B.

## Pré-requisitos

```bash
pip install -r requirements.txt
playwright install chromium
```

## Pipeline

### 1. `downloader.py` — Baixa a página renderizada

```bash
python3 downloader.py <URL> <output_dir>
```

Renderiza com Playwright (JS executado), faz scroll automático pra trigger lazy loading, aguarda network idle, captura HTML final, CSS computado, fontes, imagens, e screenshot. Salva tudo em `<output_dir>`.

### 2. `analyzer.py` — Identifica seções semanticamente

```bash
python3 analyzer.py <output_dir>
```

Lê `page.html` + `styles.css` e identifica as seções (hero, features, testimonials, faq, pricing, etc) usando heurísticas de tags semânticas, classes comuns de ecommerce, padrões de conteúdo (H1+imagem+CTA = hero; cards repetidos = features), e padrões de layout. Salva `sections.json` com HTML + metadados de cada seção.

### 3. `liquid-converter.py` — Converte seção em Liquid

```bash
python3 liquid-converter.py \
  --sections-json <output_dir>/sections.json \
  --section-index <N> \
  --output ~/shopify-theme/sections/page-<produto>-<tipo>.liquid \
  --blocks-dir ~/shopify-theme/blocks \
  --namespace page-<produto> \
  --product-slug <produto>
```

Converte uma seção em `.liquid` editável:
- Textos fixos viram `{{ section.settings.* }}`
- Imagens viram `image_picker` settings
- Links viram pares de `text` + `url` settings
- Padrões repetíveis (cards, testimonials, FAQ items) viram `blocks` separados
- Classes do concorrente são substituídas por namespace próprio
- Scripts, tracking, pixels, analytics são removidos
- `{% schema %}` completo gerado com defaults pré-populados

**IMPORTANTE:** sempre valide o arquivo gerado com a skill `shopify-plugin:shopify-liquid` antes de instalar no tema. Este script gera o Liquid mas edge cases podem precisar ajuste manual.

## Princípios

- **Zero tracking:** scripts, analytics, pixels do concorrente nunca entram no output
- **Theme-agnostic:** classes e IDs sempre namespaced (`page-<produto>-*`)
- **100% editável:** todo texto/imagem/cor vira setting no theme editor
- **Validação obrigatória:** output do converter passa por validação Shopify Liquid antes de instalar
