# Page Design · Referência: Tokens de design, do rascunho ao design-tokens.json

> O rascunho de tokens que a ETAPA 2 deixa pronto no `:root` (o contrato de variáveis CSS), e o `design-tokens.json` que o `tools/page-qa/tokens.py` gera na ETAPA 6, a partir do `page.html` aprovado: comando, campos, `source`, `preset_base` e a política do arquivo de marca. Abra no fim da ETAPA 2 e de novo na ETAPA 6, depois da aprovação do membro.

### Na ETAPA 2: o rascunho no `:root`

A marca fechada na ETAPA 2 (o `brand-tokens.json`, ou a candidata escolhida na comparadora) vira um bloco `:root` que abre o `<style>` do `design/page.html` e da comparadora. Os nomes são fixos, porque é por eles que o `tokens.py`, o `verify_page.py` e a `page-build` leem a página:

```css
:root {
  --color-background: #FDFAF4; --color-surface: #F5EDE0; --color-foreground: #231F20;
  --color-primary: #D85C4A; --color-on-primary: #FFFFFF; --color-accent: #9CAF88;
  --color-muted: #B0A99F; --color-border: #E3DAC9;
  --font-heading: '<família>', -apple-system, sans-serif;
  --font-body: '<família>', -apple-system, sans-serif;
  --text-0: 1.0625rem; --text-1: 1.333rem; --text-2: clamp(1.75rem, 3vw, 2.5rem);
  --space-1: 4px; --space-2: 8px; --space-4: 16px; --space-8: 32px;
  --radius-sm: 6px; --radius-md: 12px;
  --shadow-card: 0 8px 24px rgb(35 31 32 / .08);
}
```

- **Os 8 papéis de cor são obrigatórios** (`background`, `surface`, `foreground`, `primary`, `on-primary`, `accent`, `muted`, `border`). Sem um deles, o `tokens.py` recusa gerar os tokens.
- `--text-*`, `--space-*`, `--radius-*` e `--shadow-*` podem ter os degraus que a direção pedir; o resto do CSS usa só essas variáveis (régua, itens T1, E1 e C1).
- A direção da ETAPA 3 e a construção da ETAPA 4 ajustam escala, espaço, raio e sombra. As cores e as famílias só mudam quando a marca está vazia.

### Na ETAPA 6: `tokens.py` gera o `design-tokens.json`

Ninguém consolida tokens à mão nem "lendo o HTML". Antes do script, grave no `design-tokens.json` só os dois campos que ele não deduz do HTML, e ele preserva os dois:

- `variant_chosen`: o modo de construção (`"direction"` ou `"reference"`), com a letra da variação quando a rodada ofereceu mais de uma (ex: `"direction-B"`), ou a versão do Codex quando a segunda opinião venceu;
- `components_by_section`: por section, os block types que a `page-build` vai criar (cruza com `sections_plan` do `page-plan.json`).

Depois rode, da raiz do repositório:

```bash
python3 tools/page-qa/tokens.py workspace/[produto]/page/design/page.html \
  --out workspace/[produto]/page/design-tokens.json \
  --source <dembrandt|brand_tokens|palette_engine|manual> [--preset-base <id do preset>] \
  [--brand-out workspace/[produto]/brand/brand-tokens.json]
```

- **`--source`** diz de onde veio a marca da página: `brand_tokens` (o `brand-tokens.json` do setup), `dembrandt` (extraída na ETAPA 2 numa URL da própria marca), `palette_engine` (candidata da comparadora) ou `manual` (cores que o membro informou).
- **`--preset-base`** só com `palette_engine`: o id do preset da candidata escolhida, que vai pro campo `preset_base` (sem a flag, o campo não aparece).
- **`--brand-out`** só quando o `brand-tokens.json` está vazio (`source: "none"`): grava a marca a partir da página aprovada. Com a marca já preenchida, o script recusa (exit 4) e a marca não muda.
- **Exit 1**: mais de 5 cores soltas fora das variáveis. Troque cada uma pela variável do papel.

O arquivo que sai:

```json
{
  "produto": "[slug]",
  "variant_chosen": "direction",
  "components_by_section": {
    "hero": ["heading", "paragraph", "button_row", "stats_bar"],
    "offer": ["heading", "pricing_tier", "countdown_banner"]
  },
  "colors": {
    "background": "#fdfaf4", "surface": "#f5ede0", "foreground": "#231f20",
    "primary": "#d85c4a", "on_primary": "#ffffff", "accent": "#9caf88",
    "muted": "#b0a99f", "border": "#e3dac9"
  },
  "type": {
    "heading_font": "'<família>', -apple-system, sans-serif",
    "body_font": "'<família>', -apple-system, sans-serif",
    "families": [{ "name": "<família>", "role": "both", "provision": "google_fonts", "weights": [400, 600], "files_dir": null }],
    "scale": { "0": "1.0625rem", "1": "1.333rem", "2": "clamp(1.75rem, 3vw, 2.5rem)" }
  },
  "spacing": { "scale": { "1": "4px", "2": "8px", "4": "16px", "8": "32px" } },
  "radii": { "sm": "6px", "md": "12px" },
  "shadow": { "card": "0 8px 24px rgb(35 31 32 / .08)" },
  "source": "brand_tokens",
  "generated_at": "2026-...Z"
}
```

`type.families[]` é o que a `page-build` abre no passo de web fonts: `provision` (`local_files`, `google_fonts` ou `system`) diz por qual caminho cada família carrega, `weights` sai dos `@font-face` do bloco `data-aura-fonts` e, em `local_files`, `files_dir` aponta pra cópia guardada dentro da pasta do produto (`reference/tipografia.md`, 2.1.3). Sem esse bloco, a `page-build` não tem como saber que a tipografia aprovada vem de arquivo e a página sobe com a fonte de fallback.

**Drift contra a marca.** Com a marca já preenchida, rode `python3 tools/page-qa/tokens.py --diff workspace/[produto]/brand/brand-tokens.json workspace/[produto]/page/design-tokens.json` e leve o `drift` e as chaves que mudaram pra mensagem final. A marca não muda por causa disso: pra mudar a marca, o membro refaz a extração do setup ou edita o arquivo.

**Se o `tokens.py` falhar depois da aprovação:** a página continua aprovada, a marca não é tocada, o manifest não marca a etapa como concluída, e a mensagem final diz o erro e o comando pra rodar de novo.

Página antiga (sem `schema_version`) pode ter `design-tokens.json` no formato anterior, com `variant_chosen` no nome da rota antiga e o bloco `typography` no `design-signals.json`; a `page-build` continua lendo os dois nesse caso.
