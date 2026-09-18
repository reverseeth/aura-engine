# Design Presets (gerador de paletas + os 8 presets que servem de base)

A lib do **Caminho 4 dos brand signals** da skill **page-design** (ETAPA 2), o caminho que roda quando não há Refero, nem print, nem URL de referência. Dois arquivos:

| Arquivo | O que é |
|---|---|
| `palette_engine.py` | O gerador. Devolve **exatamente 3 paletas candidatas** pro produto, cada uma com nome curto, motivo em uma frase e a relação de matiz declarada. |
| `presets.json` | Os **8 presets completos e fixos**. Cada candidata nasce de um deles: herda o perfil de claridade e saturação dos neutros, a tipografia, o radius, a sombra e a densidade, e troca só o matiz. |

**Por que a lib existe:** antes, cada run da `page-design` "inventava" os tokens do preset escolhido na hora, e dois membros escolhendo "Warm Lifestyle" recebiam paletas diferentes. O `presets.json` resolveu isso congelando os tokens. Sobrou o outro problema: um menu de 8 opções fixas deixa a página com a paleta do preset mais próximo, nunca com a paleta daquele produto, e escolher por amostra de cor solta é escolher às cegas. O gerador resolve os dois de uma vez: a cor nasce da vertical, do avatar e do ceticismo daquele mercado, sai em 3 opções com motivo, e a mesma entrada devolve sempre a mesma saída.

## O gerador

```bash
python3 .claude/lib/design-presets/palette_engine.py --vertical supplements
python3 .claude/lib/design-presets/palette_engine.py --vertical beauty --skepticism alto \
    --avatar "mulheres de 45 a 65 anos que já tentaram de tudo"
python3 .claude/lib/design-presets/palette_engine.py --vertical home --seed "#C66B3D,#9CAF88"
python3 .claude/lib/design-presets/palette_engine.py --vertical other --format css
```

| Flag | Para quê |
|---|---|
| `--vertical` | Obrigatória. Mesmo eixo do seletor de espécimes do `swipe-models`: `supplements`, `health`, `beauty`, `home`, `relationship`, `other`. Decide os matizes que carregam significado naquele mercado. |
| `--avatar` | A linha do avatar central da `market-research`. Entra no motivo de cada paleta e no hash que define a rodada. |
| `--skepticism` | `baixo`, `médio` (default) ou `alto`, o ceticismo da `market-research`. Ceticismo alto puxa a saturação pra baixo e o tom pra sóbrio. |
| `--seed` | Hex da marca ou da referência do membro. O mais saturado vira o matiz da primeira candidata (um neutro quase sem cor é ignorado); as outras duas se afastam dele. |
| `--signals` | Um `design-signals.json` já gravado: as cores dele entram como semente. |
| `--lang` | `pt-BR` (default) ou `en`. Muda nome, motivo e rótulos, seguindo o `report_language` do membro. |
| `--theme` | `auto` (default, o tema do preset base), `light` ou `dark`. |
| `--format` | `md` (default, pro membro), `json` (pra gravar) ou `css` (os blocos de token em trio R,G,B da página comparadora). |
| `--out` | Salva no caminho em vez de imprimir. |

Saída de cada candidata: `name`, `why`, `harmony` (+ `harmony_label` em linguagem simples), `base_preset`, `palette` role-tagged com os 8 roles, `tokens_rgb` (trios da comparadora), `contrast` (as quatro razões medidas) e `non_color_tokens` (`heading_font`, `body_font`, `google_fonts`, `radius`, `shadow`, `density` **literais do preset base** — é o que a `page-build` usa pra provisionar a fonte).

## Os quatro testes que nenhuma paleta escapa

O script valida a si mesmo antes de imprimir. Reprovou, ele corrige a claridade e revalida; não convergiu, **sai com erro em vez de entregar paleta com aviso**.

1. **Saturação viva.** `primary` e `accent` acima de 0.35 em HSL: cor que carrega significado, nunca cinza disfarçado.
2. **Harmonia calculada, não sorteada.** Cada paleta declara a relação de matiz entre `primary` e `accent` (análoga, complementar dividida ou tríade) e a distância real precisa bater com a faixa daquela relação.
3. **Contraste WCAG AA.** 4.5:1 no texto e no texto secundário contra o fundo E contra a superfície dos cartões (é onde o texto secundário vive de verdade), e no texto do botão contra o botão; 3:1 na cor de apoio sobre o fundo (elemento gráfico). A cor de apoio também tem teto de contraste: acima dele ela deixa de ser cor e vira uma segunda tinta.
4. **As 3 distintas entre si.** Matiz de `primary` a 25 graus ou mais uma da outra, medido no hex final.

Testes automatizados em `tools/tests/test_palette_engine.py` (`python3 -m unittest discover -s tools/tests`): cobrem a geração em toda vertical e cada violação isolada que precisa reprovar.

## Os 8 presets (a base)

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

Shape de cada entrada (superset do `design-signals.json` que a `page-design` grava):

```json
{
  "name": "Warm Lifestyle",
  "vibe": "descrição em 1-2 frases do clima visual",
  "use_when": "quando esse caráter serve",
  "heading_font": "'Fraunces', Georgia, serif",
  "body_font": "'Nunito Sans', -apple-system, sans-serif",
  "google_fonts": [{ "family": "Fraunces", "weights": [400, 600] }],
  "palette": { "background": "#...", "surface": "#...", "foreground": "#...", "primary": "#...", "on_primary": "#...", "accent": "#...", "muted": "#...", "border": "#..." },
  "radius": { "base_px": 16, "pill_px": 1000 },
  "shadow": "none | subtle | medium | strong",
  "density": "airy | medium | compact"
}
```

- **`palette` é role-tagged** — mesmas roles do `design-signals.json`/`design-tokens.json` (a `page-build` mapeia direto pra CSS vars + settings). `on_primary` é a cor do texto sobre o `primary` (botões).
- **`google_fonts`** lista família + pesos usados — é o que a **`page-build` (passo de web fonts)** usa pra montar o `<link>` do Google Fonts (só os pesos listados; cada peso extra é KB no LCP).
- Todas as fontes são **Google Fonts** de propósito: o provisionamento na `page-build` é padronizado e sem arquivo de fonte pra licenciar.

## Como a `page-design` consome

1. Caminho 4 da ETAPA 2: a skill roda o gerador com a vertical, o avatar e o ceticismo lidos das fases anteriores.
2. Monta a página comparadora com as 3 candidatas aplicadas às seções reais do produto (os blocos de token saem do `--format css`) e mostra nome e motivo ao lado de cada aba.
3. Com a escolha do membro, grava no `design-signals.json`: `source: "manual"`, `source_detail: "paleta gerada [Nome] · harmonia [harmony] · base [base_preset]"`, a `palette` inteira e os campos de `non_color_tokens` **literais**. O preset base fica no `source_detail` porque é por ele que a `page-build` encontra os pesos de fonte em `presets.json`.

## Regras

- **Os 8 presets não são mais um menu.** Não ofereça a lista ao membro, não copie cor de `presets.json` à mão: a cor vem do gerador, e do preset vem só o que não é cor.
- **NUNCA inventar ou ajustar tokens em runtime.** Se o resultado não agrada, o caminho é rodar o gerador com outra semente (ou o membro pedir customização, registrada como `"paleta gerada [Nome] (customizado)"`), não "melhorar" hex na mão.
- **Editar `presets.json` é mudança de FRAMEWORK** (afeta todos os membros e o gerador inteiro): mantenha o contraste WCAG AA entre `foreground`/`background` e `on_primary`/`primary`, e fontes disponíveis no Google Fonts.
- **Mexer nos pisos do gerador** (saturação, contraste, distância de matiz) é mexer no padrão visual de toda página da Aura: rode os testes e trate a mudança como decisão de framework.
