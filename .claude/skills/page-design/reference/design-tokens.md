# Page Design · Referência: Gerar o design-tokens.json por código

> O schema completo do `design-tokens.json` consolidado do HTML aprovado (cores, tipografia, spacing, radii, shadow, `components_by_section`, `variant_chosen`). Abra depois da aprovação do membro.

### Gerar `design-tokens.json` (programaticamente)

Do `design/page.html` aprovado, consolide os tokens **programaticamente** (não "extraídos do HTML por reasoning"). A `page-build` consome isto pra mapear cada token → CSS var + setting. `variant_chosen` registra o nome da rota (`"claude-design"`, `"singlefile-clone"`, `"section-puzzle"`); quando a rodada ofereceu mais de uma variação, registre a escolhida (ex: `"claude-design-B"`):

```json
{
  "produto": "[slug]",
  "variant_chosen": "A",
  "colors": {
    "background": "#FDFAF4", "surface": "#F5EDE0", "foreground": "#231F20",
    "primary": "#D85C4A", "on_primary": "#FFFFFF", "accent": "#9CAF88",
    "muted": "#B0A99F", "border": "#E3DAC9"
  },
  "type": {
    "heading_font": "'Geist', -apple-system, sans-serif",
    "body_font": "'Geist', -apple-system, sans-serif",
    "families": [
      { "name": "Geist", "role": "both", "provision": "google_fonts", "weights": [400, 500, 600, 700] }
    ],
    "scale_ratio": 1.25,
    "h1": "clamp(2.5rem, 5vw, 4rem)",
    "h2": "clamp(1.75rem, 3vw, 2.5rem)",
    "body": "1.0625rem"
  },
  "spacing": { "base": 8, "scale": [4, 8, 12, 16, 24, 32, 48, 64, 96] },
  "radii": { "sm": 6, "md": 12, "lg": 20, "pill": 1000 },
  "shadow": { "intensity": "subtle", "color": "#231F20" },
  "components_by_section": {
    "hero": ["eyebrow", "heading", "paragraph", "button_row", "stats_bar", "tag"],
    "offer": ["eyebrow", "heading", "pricing_tier", "countdown_banner"]
  },
  "generated_at": "2026-...Z"
}
```

`spacing.base` é 4 ou 8 (base-4/8). `components_by_section` lista, por section, os block types que a `page-build` vai criar — cruza com `sections_plan` do `page-plan.json`.

`type.families[]` é o espelho do bloco `typography` do `design-signals.json` (sub-etapa 2.1) e é o que a `page-build` abre no passo de web fonts: `provision` (`google_fonts`, `local_files` ou `system`) diz por qual caminho cada família é carregada, `weights` lista só os pesos que a página usa e, em `local_files`, `files_dir` aponta pra cópia guardada dentro da pasta do produto. Sem esse bloco, a `page-build` não tem como saber que a tipografia aprovada vem de arquivo e a página sobe com a fonte de fallback.
