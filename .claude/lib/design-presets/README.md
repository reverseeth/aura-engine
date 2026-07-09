# Design Presets (fonte única dos 8 presets da 07a)

Tokens **completos e fixos** dos 8 presets de design que a skill **07a-page-design** oferece no **Caminho 4 dos brand signals** (Manual / presets — último recurso da cascade, quando não há Refero, nem print, nem URL de referência).

**Por que este arquivo existe:** antes, cada run da 07a "inventava" os tokens do preset escolhido na hora — dois membros escolhendo "Warm Lifestyle" recebiam paletas diferentes, e o mesmo membro re-rodando a skill via drift visual sem ter pedido. Preset é promessa de consistência: mesmo nome, mesmos tokens, sempre. A fonte única é `presets.json`; a skill **lê o arquivo, nunca gera de cabeça**.

## Os 8 presets

| Key | Nome | Em uma frase |
|---|---|---|
| `modern-clean` | Modern Clean | DTC neutro e confiável, azul firme de CTA — o default seguro |
| `bold-editorial` | Bold Editorial | Capa de revista em alto contraste, display pesado, vermelho-tijolo |
| `premium-minimal` | Premium Minimal | Luxo silencioso quase monocromático, CTA preto, serif clássica |
| `warm-lifestyle` | Warm Lifestyle | Wellness acolhedor: linho, terracota, sálvia, cantos generosos |
| `tech-sharp` | Tech Sharp | Dark mode técnico, azul elétrico, grotesk geométrica |
| `atelier-document` | Atelier Document | Documento editorial em papel, oxblood, low-pressure, ensaio |
| `apothecary-calm` | Apothecary Calm | Botânico-clínico: verde de farmácia antiga + dourado de herbário |
| `luxe-magazine` | Luxe Magazine | Editorial de moda/luxo: preto, branco, dourado, serif de alta-costura |

## Shape de cada preset

Cada entrada espelha (e é superset de) o shape do `design-signals.json` que a 07a grava:

```json
{
  "name": "Warm Lifestyle",
  "vibe": "descrição em 1-2 frases do clima visual",
  "use_when": "quando recomendar este preset",
  "heading_font": "'Fraunces', Georgia, serif",
  "body_font": "'Nunito Sans', -apple-system, sans-serif",
  "google_fonts": [{ "family": "Fraunces", "weights": [400, 600] }],
  "palette": { "background": "#...", "surface": "#...", "foreground": "#...", "primary": "#...", "on_primary": "#...", "accent": "#...", "muted": "#...", "border": "#..." },
  "radius": { "base_px": 16, "pill_px": 1000 },
  "shadow": "none | subtle | medium | strong",
  "density": "airy | medium | compact"
}
```

- **`palette` é role-tagged** — mesmas roles do `design-signals.json`/`design-tokens.json` (a 07b mapeia direto pra CSS vars + settings). `on_primary` é a cor do texto sobre o `primary` (botões).
- **`google_fonts`** lista família + pesos usados — é o que a **07b (passo de web fonts)** usa pra montar o `<link>` do Google Fonts (só os pesos listados; cada peso extra é KB no LCP).
- Todas as fontes são **Google Fonts** de propósito: o provisionamento na 07b é padronizado e sem arquivo de fonte pra licenciar.

## Como a 07a consome

1. Membro escolhe o preset no Caminho 4 (ETAPA 2 da 07a).
2. A skill lê `.claude/lib/design-presets/presets.json`, pega a entrada da key escolhida.
3. Mapeia LITERALMENTE pro `design-signals.json` do produto: `source: "manual"`, `source_detail: "preset [Nome]"`, e os campos `heading_font`/`body_font`/`palette`/`radius`/`shadow`/`density` copiados do preset (sem ajuste criativo — ajuste só se o membro pedir explicitamente, e aí registre como customização, não como preset puro).

## Regras

- **NUNCA inventar/ajustar tokens de preset em runtime.** Se o resultado do preset não agrada, o caminho é o membro pedir customização (vira `source_detail: "preset X (customizado)"`) ou trocar de caminho na cascade — não é "melhorar" o preset silenciosamente.
- **Editar este arquivo é mudança de FRAMEWORK** (afeta todos os membros): mantenha coerência com o nome do preset, contraste WCAG AA entre `foreground`/`background` e `on_primary`/`primary`, e fontes disponíveis no Google Fonts.
- Novos presets: adicionar entrada aqui + atualizar a lista nomeada na 07a (Caminho 4).
