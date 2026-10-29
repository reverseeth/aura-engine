# Page Design · Referência: Modo direção (ETAPA 4)

> Construir o `page.html` a partir do `direction.md` e da marca, com toda cor e tamanho em variáveis CSS no `:root`; o canvas do Claude Design pela tool `Artifact` como superfície de trabalho; as regras do taste-skill no perfil Aura (sem JavaScript); o contrato do `page.html` e o caminho quando o canvas não abre. Abra na ETAPA 4 quando o membro escolhe o modo direção.

## O que precisa estar na mão antes da primeira linha

- **(a) `page/direction.md`** (ETAPA 3): tipografia, paleta, hero, blueprint por seção e o proibido. É a direção desta página; não misture com o layout que você faria de qualquer jeito.
- **(b) A marca** (ETAPA 2): os 8 papéis e as famílias, com o bloco `data-aura-fonts` no `<head>` quando a família é de arquivo local (`reference/tipografia.md`).
- **(c) O plano** (ETAPA 1): `section_order`, `sections_plan` com blocks e `media`, `page_type` e `hero_type`. A estrutura já foi decidida pelo awareness e pela copy.
- **(d) A copy REAL da `copy-engine`**, seção por seção. Zero lorem ipsum, zero frase inventada pra caber no layout.
- **(e) As imagens do mapa de mídia da 1.6** (`design/assets/`).
- **(f) A régua** (`reference/regua-de-design.md`): leia antes de desenhar. Ela volta medida e julgada na ETAPA 5; chegar lá dentro dos números evita refazer.
- **(g) Movimento**, quando a direção pede: `reference/movimento-css.md`.

## Tokens no `:root` (contrato com o `tokens.py`)

Toda cor, família, tamanho de texto, espaço, raio e sombra da página vive numa variável do `:root`, com estes nomes, e o resto do CSS só consome `var(...)`:

```css
:root {
  --color-background: #...; --color-surface: #...; --color-foreground: #...;
  --color-primary: #...; --color-on-primary: #...; --color-accent: #...;
  --color-muted: #...; --color-border: #...;
  --font-heading: "...", serif; --font-body: "...", sans-serif;
  --text-xs: ...; --text-sm: ...; --text-base: ...; --text-lg: ...; --text-xl: ...; --text-display: ...;
  --space-1: ...; --space-2: ...; /* grade base 4 ou 8 */
  --radius-base: ...; --shadow-base: ...;
}
```

O `tools/page-qa/tokens.py` lê exatamente isso na ETAPA 6 e falha com mais de 5 cores hex soltas fora das variáveis. Cor com transparência: `color-mix(in srgb, var(--color-foreground) 60%, transparent)`, não hex novo.

## As regras do taste-skill no perfil Aura

Com o plugin taste-skill, a skill `design-taste-frontend` e a folha da direção valem como guia de composição, tipografia e imagem, com estas exceções, porque a página vira Liquid e não pode ter JavaScript:

- **Sem `stage.js` e sem o gate `html.js`:** nada de script de palco, de revelação ou de checagem em runtime.
- **A "live thing"** (a coisa que o visitante faz na página) só com `:has()`, `<details>`/`<summary>` ou `<input type="radio">` + `label`: seletor de kit que troca a imagem, comparativo que abre, quiz de uma pergunta.
- **O `MOTION_MIN` não se aplica.** Movimento é opcional e sempre CSS (`reference/movimento-css.md`).
- **Imagem:** a ordem do mapa de mídia da 1.6 vence a da folha. Nada de picsum; desenho SVG do produto só quando o membro não tem foto e a 1.6 registrou o `acquisition_plan`.
- Conflito entre a folha e o plano: o plano vence em estrutura e conteúdo; a folha vence em geometria, ritmo e tipo.

## Abrir o canvas do Claude Design

O canvas roda dentro do Claude Code, pela tool `Artifact`. Três passos, nesta ordem:

1. **Quickstart** (uma vez por página): `Artifact` com `action: "quickstart"`, `intent: "design"` e `design_systems: false` (a marca já está fechada; design system de terceiro não entra). Use o `type_url` que voltar; nunca guarde uma URL fixa nem reaproveite a de outra sessão.
2. **Criar**: publique com aquele `type_url`, um `title` curto (marca + tipo de página), sem arquivos e com `auto_open: "after_first_write"`. Siga as instruções que o create devolver: elas dizem como preencher o canvas.
3. **Preencher** com a página inteira, na ordem do `section_order`, sempre no MESMO `url`.

Avise em uma linha, antes do primeiro publish, que a página abre como Artifact privado na conta claude.ai do membro e que o arquivo local é a fonte.

## O contrato do `page.html` (vale acima do canvas)

O entregável é `workspace/[produto]/page/design/page.html`, e é ele que a `page-build` compila. **O `page.html` publicado é sempre o do repo, normalizado**: o canvas é superfície de trabalho, não fonte.

- HTML + CSS plano e self-contained, num `<style>` único no `<head>`. Sem Tailwind, sem framework, sem CDN de CSS.
- **Zero `<script>`.**
- `<section data-aura-section="[id do sections_plan]">` em todas as seções, com os ids do plano.
- Imagens por caminho relativo pra `design/assets/`, nunca `src` de sandbox.

Escreva o arquivo local e publique esse mesmo conteúdo no canvas. Se o membro editar no canvas, releia o Artifact (`action: "read"`), passe a versão nova pela normalização (`reference/normalizacao-html-externo.md`) e só então grave no arquivo local.

## Iterar

Comentários no Artifact chegam pelo `ArtifactComments`; os do chat chegam direto. Ajuste o arquivo local, republique no mesmo `url`. Cada rodada salva versão nova (`page-v2.html`...) e entra no `iterations-log.json`.

## Quando o canvas não abre

Quickstart ou publish falhou (conta sem Artifacts, erro de rede): não aborte. O arquivo local existe e é a fonte; a ETAPA 5 tira as capturas e a ETAPA 6 mostra o preview. Diga em uma linha que o canvas não abriu e que isso não muda o resultado.

## Registro

`page-plan.json`: `build_mode: "direction"`, `design_route: "direction"` e, em `design_route_ref`, a URL do Artifact (ou `null`).
