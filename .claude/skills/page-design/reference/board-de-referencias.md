# Page Design · Referência: Board de referências (ETAPA 1.8)

> A pesquisa visual obrigatória antes de qualquer cor, fonte ou HTML: Pinterest como fonte principal, as páginas escaladas dos concorrentes e o Refero como complemento, o board de 8 a 15 referências com o que se tira de cada uma, a direção visual em três linhas aprovada pelo membro e onde tudo fica salvo. Abra depois do plano de sections (1.1 a 1.7) e antes da ETAPA 2.

## Por que vem antes de tudo

Página desenhada sem referência sai na média do que o modelo já viu, e a média é exatamente a cara de template. O designer sênior não abre o canvas em branco: ele junta referências, decide o que roubar de cada uma e só então desenha. A ETAPA 2 (cor e tipografia) e a ETAPA 3 (a rota de design) partem da direção que sai daqui.

## 1. Reaproveite o que já existe

- **Board da marca no Instagram:** se existir `workspace/<slug>/social-engine/` com board de referências ou direção visual, ele é o ponto de partida. Loja e Instagram precisam parecer a mesma marca: mesma paleta, mesma família de tipografia, mesmo tratamento de foto. O board da página só complementa com referências de layout de página, que o board de Instagram não cobre.
- **Board do membro:** pergunte em uma linha se ele tem um board no Pinterest ou páginas que curte. Link colado entra primeiro no board.
- **`brand.md`:** paleta e tipografia já respondidas continuam valendo; o board decide o resto (grid, ritmo, foto, componentes).

## 2. Colete no Pinterest (fonte principal)

1. **Descoberta pela tool `WebSearch`**, nunca scrapeando o buscador. Rode de 4 a 6 queries combinando nicho e estilo:
   - `site:pinterest.com <nicho> landing page design`
   - `site:pinterest.com <nicho> website design` (ex.: `supplement website design`, `skincare website design`)
   - `site:pinterest.com <estilo> web design` (o estilo vem do `brand.md` ou do `profile.md`: `editorial minimal`, `clinical clean`, `warm organic`, `bold DTC`)
   - `site:pinterest.com <nicho> packaging photography` (tratamento de foto)
   - `site:pinterest.com advertorial story page design` quando `page_type` é `advertorial` ou `listicle`
2. **Abra os pins e boards** pelo fetcher da Aura: `python3 .claude/lib/web-fetch/fetch.py "<url do pin ou board>" --mode text --json`. O pin quase sempre aponta pro site original: siga o link e olhe a página real, porque é ela que vira referência, não a miniatura.
3. **Screenshot das melhores** com o Playwright (mesmo método do self-review da 3.7, 1440px) salvo em `page/design/references/ref-NN.png`, pra ler por visão e pra o membro ver.

## 3. Complete com o que o dinheiro já valida

- **Páginas escaladas dos concorrentes:** as landings de `competitor-analysis/dados.json` (`landing_formats[]`) e, com o TrendTrack conectado, as LPs dos ads de maior ad rank do nicho. Delas sai estrutura e hierarquia, nunca copy, imagem, logo ou marca.
- **Refero** (`mcp__refero__`), se conectado: 2 a 3 páginas por componente que o board ainda não cobre (hero, bloco de oferta, prova social).

## 4. Monte o board (8 a 15 referências)

Uma linha por referência, nesta tabela, que entra no `design-system.md` como seção "Board de referências":

| # | Referência (link) | Fonte | O que se tira dela |
|---|---|---|---|
| 1 | https://... | Pinterest | Tipografia: serifa display enorme no hero com sans pequena em caixa alta no eyebrow |
| 2 | https://... | concorrente escalado | Grid: oferta em duas colunas, imagem do kit sangrando à esquerda |

Cada linha nomeia pelo menos um destes eixos, com o detalhe concreto: **tipografia** (família, contraste de tamanho, caixa), **grid** (colunas, assimetria, largura de leitura), **paleta** (cores dominantes e de acento), **tratamento de foto** (luz, fundo, enquadramento, textura), **componentes** (hero, cards, tabela de comparação, depoimento, CTA, divisores). Referência sem eixo concreto sai do board. Cobertura mínima: os cinco eixos aparecem pelo menos duas vezes cada no board inteiro.

## 5. Direção visual e aprovação

Feche o board em uma direção de três linhas, escrita pro membro:

1. **Sensação:** o que a página tem que transmitir em uma frase (ex.: "laboratório limpo com calor humano").
2. **Assinatura:** as duas ou três escolhas que fazem a página ser reconhecível (ex.: "serifa display gigante, foto de produto em luz dura com sombra longa, divisores finos sublinhados").
3. **Proibido:** o que esta página nunca faz (ex.: "nada de gradiente, nada de cartão com sombra, nada de foto de banco de imagens").

Mostre o board e a direção ao membro e pergunte em uma linha se a direção está certa. **Sem aprovação da direção, a ETAPA 2 não começa.** Ajuste e mostre de novo até ele aprovar.

## 6. Onde fica salvo

- `page/design/references/`: os screenshots `ref-NN.png`.
- `page-plan.json` → bloco `reference_board`: `{ "references": [{ "url": "...", "source": "pinterest | competitor | refero | member", "takeaways": ["tipografia: ...", "grid: ..."], "screenshot": "design/references/ref-01.png" }], "direction": { "feel": "...", "signature": ["..."], "forbidden": ["..."] }, "social_board_reused": true }`.
- `design-system.md`: a seção "Board de referências" com a tabela e a direção.

A régua de qualidade da 3.7 confere a página contra esta direção: cada item de "Assinatura" aparece no `page.html`, nenhum item de "Proibido" aparece.
