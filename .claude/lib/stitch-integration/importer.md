# Stitch HTML Importer — spec pra Skill 06b

Como a Skill 06b (page-sections) processa HTML standalone exportado do Stitch
e converte pra Liquid sections preservando a estética visual.

## Detecção automática

No início da Skill 06b, verificar se existe blueprint:

```python
blueprint_dir = f"/workspace/{produto}/06-page/stitch-blueprint/"
blueprint_html = f"{blueprint_dir}/index.html"

if exists(blueprint_html):
    mode = "blueprint_guided"   # usar HTML como visual reference
else:
    mode = "direct_generation"  # gerar do zero (fluxo padrão atual)
```

## Pipeline quando `mode == blueprint_guided`

### Passo 1 — Parse do HTML

**Nenhuma dep externa.** Claude lê o `index.html` como string (via Read tool) e extrai os tokens abaixo via regex + LLM reasoning. NÃO use BeautifulSoup ou Playwright — skill 06b roda dentro do Claude Code, sem runtime Python adicional.

Claude deve extrair:

```json
{
  "visual_tokens": {
    "colors": {
      "primary_text": "#1A1A1A",        // extract do body color
      "background": "#FAFAFA",           // extract do body bg
      "accent_primary": "#002DD1",       // extract de CTAs, links
      "accent_secondary": "#...",        // se existir segunda accent
      "neutrals": ["#F5F5F5", "#E8E8E8", "#AAAAAA"],
      "semantic": {"danger": "#B03A3A", "success": "#4A9A2E"}
    },
    "typography": {
      "heading_family": "Fraunces, serif",
      "body_family": "Inter, sans-serif",
      "heading_sizes": [48, 36, 28, 22, 18],   // H1-H5
      "body_size": 16,
      "scale_ratio": 1.333,
      "line_height_body": 1.7
    },
    "spacing": {
      "base_unit": 8,
      "section_padding_y": [64, 80, 96],      // observed across sections
      "container_max_width": 1200
    },
    "radii": {
      "sm": 6, "md": 12, "lg": 20, "pill": 9999
    },
    "shadows": {
      "sm": "0 2px 4px rgba(0,0,0,0.04)",
      "md": "0 4px 12px rgba(0,0,0,0.06)",
      "lg": "0 8px 24px rgba(0,0,0,0.1)"
    }
  },
  "layout_intent": {
    "sections_detected": [
      {"id": "hero", "type": "product-hero", "height_vh": 80, "columns": 2},
      {"id": "trust_bar", "type": "trust-indicators", "columns": 4},
      {"id": "mechanism", "type": "3-step-visual", "columns": 3},
      {"id": "benefits", "type": "grid-cards", "columns": 2, "rows": 2},
      ...
    ],
    "scroll_rhythm": "dense → breathing → dense",
    "mobile_breakpoint_detected": 768,
    "content_alignment": "center-dominant"
  },
  "component_patterns": {
    "card_style": "bordered-rounded",
    "cta_style": "filled-rounded-pill",
    "icon_style": "svg-stroke-1.5",
    "badge_style": "pill-small-caps"
  }
}
```

Salvar em `/workspace/{produto}/06-page/stitch-extracted-tokens.json`.

### Passo 2 — Pipeline de geração Liquid com bias visual

Pra cada section identificada:

1. **Usar o token extraction como constraints** no prompt de geração do Liquid:
   ```
   Gere section Liquid "page-[slug]-hero" que implementa este layout visual:
   {stitch_section_html_snippet}

   Preservar:
   - Cores: {extracted_colors}
   - Tipografia: {extracted_typography}
   - Spacing: {extracted_spacing}
   - Hierarquia visual observada

   Traduzir pra Shopify Liquid 2.0:
   - Settings customizáveis (colors, radius, fonts) seguindo Padrão 1 (inline CSS vars)
   - Blocks quando há repetição (ex: benefits com 4 cards)
   - Form /cart/add se for pricing tier (Padrão 4)
   - SVG icons (Padrão 2)

   Output: arquivo .liquid completo com schema
   ```

2. **Validation step** após geração (heurístico — sem renderização real):
   - Claude compara lista de CSS vars geradas no Liquid vs tokens extraídos do HTML
   - Claude confere se layout Liquid preserva hierarquia (ordem de blocks) do HTML
   - Se >3 tokens divergem ou ordem muda, regerar com prompt mais específico (max 3 retries)
   - Se ≤3 divergem, aprovar com log em `stitch-conversion-notes.md`

### Passo 3 — Consolidar design tokens no brand-discovery

Sobrescrever `06-brand-discovery.json` com tokens extraídos do Stitch:
```json
{
  "brand_discovered": {
    "source": "stitch_blueprint",
    "visual_tokens": { ...(extracted tokens from above) },
    "generated_at": "timestamp",
    "blueprint_path": "/workspace/[produto]/06-page/stitch-blueprint/index.html"
  }
}
```

Isso garante que:
- Skill 06b aplica mesmos tokens em todas as sections (consistency)
- Iterações futuras preservam o design aprovado visualmente pelo membro

### Passo 4 — Flagar divergências críticas

Algumas coisas do Stitch não mapeiam 1-para-1 pro Liquid:

| Pattern Stitch | Comportamento |
|---|---|
| Imagens hardcoded (`<img src="assets/hero.jpg">`) | Converter pra `image_picker` setting, membro uploada via theme editor |
| SVG inline customizado | Manter como `icon_custom_svg` textarea setting (Padrão 2) |
| Hover states / animações | Mapear pra Liquid + CSS hover quando trivial; flagar pro membro se complexo |
| Custom JS / Web Components | Converter pra vanilla JS dentro de `{% javascript %}` quando possível; senão alertar |
| External CDN fonts | Adicionar `<link>` Google Fonts no topo da section |

Flagar no output: `/workspace/[produto]/06-page/conversion-notes.md` listando:
- O que converteu 100%
- O que simplificou (com justificativa)
- O que não converteu (exigiu decisão do membro)

## Custo computacional

- Parse HTML: 1 Claude call (~2-3k tokens)
- Extract tokens: 1 Claude call (~5k tokens)
- Gerar Liquid por section: N calls (mesmo que modo direct, só com mais constraints)

Total adicional vs modo direct: ~10-15k tokens a mais. Desprezível.

## Fallback — se Stitch HTML for incompatível

Se o HTML exportado do Stitch for muito bagunçado (inline styles caóticos, estrutura
confusa), skill 06b pode cair pra `mode == direct_generation` automaticamente e
logar:

```
⚠️ Stitch blueprint detectado mas estrutura incompatível.
   Usando apenas extraction de tokens visuais (cores/fonts/spacing)
   e gerando sections do zero com esses constraints.
```

Isso garante que **zero rodadas falham por blueprint ruim.**
