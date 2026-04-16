# Design Clone — Aura Engine (ferramenta auxiliar)

**Status:** ferramenta auxiliar, não pipeline principal. A skill 06 (page-engine) gera páginas Shopify do zero a partir da copy — não clona design de concorrente. Estes scripts existem pra um único caso: **extrair sinais de paleta/tipografia de um site de referência** quando o membro passa um link na Etapa 2.1 (Brand Discovery) da skill 06. Os signals alimentam os specialists `designer-color-system` e `designer-typography-scale`. Nenhum código do concorrente vai pro tema.

## Pré-requisitos

```bash
pip install -r requirements.txt
playwright install chromium
```

## Uso no fluxo da skill 06 (único cenário suportado)

Quando o membro passa um site de referência visual na Etapa 2.1:

```bash
# 1. Baixa a página renderizada
python3 downloader.py "URL" /tmp/ref-<produto>

# 2. Identifica sections (input do extractor)
python3 analyzer.py /tmp/ref-<produto>

# 3. Extrai design_system abstrato (o único output usado)
python3 pattern-extractor.py /tmp/ref-<produto>
```

A skill 06 lê apenas o bloco `design_system` de `/tmp/ref-<produto>/patterns.json`:

```json
{
  "design_system": {
    "typography": { "heading_font": "...", "body_font": "..." },
    "colors": { "background_primary": "#...", "text_primary": "#...", "accents": [...] },
    "shape": { "border_radius_px": 8, "shadow_style": "subtle" },
    "spacing": { "density": "medium", "avg_padding_px": 24 }
  }
}
```

Esse bloco vira input pros specialists de design na Etapa 3. O resto do `patterns.json` (sections detectadas) é ignorado — a estrutura da página vem sempre da copy do membro, não do concorrente.

## Scripts

| Script | Papel no fluxo atual |
|---|---|
| `downloader.py` | Renderiza página com Playwright, salva HTML/CSS/fontes/imagens + `computed-styles.json` |
| `analyzer.py` | Detecta sections semanticamente — necessário pro pattern-extractor, output ignorado pela skill |
| `pattern-extractor.py` | **Core.** Produz `design_system` abstrato (cores, fontes, radius, shadow, density) |
| `liquid-converter.py` | Legacy. Converte HTML (scraped ou fresh) em Liquid section. NÃO é usado pela skill 06 — ela gera Liquid direto via `frontend-design` + schema mapping próprio |
| `preview.py` | Legacy. Renderiza `.liquid` como HTML standalone pra debug |

Os scripts legacy (`liquid-converter.py`, `preview.py`) continuam funcionais pra quem quiser cenários avançados de clone literal fora do fluxo padrão, mas **não são acionados pela skill 06**.

## Princípios

- **Zero código do concorrente no output final.** A skill 06 só extrai signals agregados (paleta + fontes + tokens); o HTML/CSS da página Shopify é gerado fresh via `frontend-design`.
- **Theme-agnostic.** Sections geradas pela skill 06 têm namespacing próprio (`page-<produto>-<tipo>`), zero dependência do tema pai.
- **Validação obrigatória.** Toda section .liquid gerada passa pela skill `shopify-plugin:shopify-liquid` antes de instalar no tema.
