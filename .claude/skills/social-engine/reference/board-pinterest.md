# Social Engine · Referência: Board de branding no Pinterest (ETAPA 1)

> De onde vêm as referências do feed (board do membro, board da página, Pinterest), como montar o board de 9 a 15 referências com o eixo de cada uma, a direção de feed em três linhas e onde fica salvo. Abra na ETAPA 1.

## Por que vem antes de qualquer imagem

Feed gerado sem referência sai com a cara média de IA: cada post bonito sozinho e o grid inteiro sem identidade. O perfil que passa confiança tem três coisas repetidas em todo post: a mesma paleta, o mesmo tratamento de foto e o mesmo jeito de colocar texto na imagem. O board decide essas três coisas uma vez, e a rotina diária só obedece.

## 1. Reaproveite o que já existe

- **Board do membro:** pergunte em uma linha se ele tem um board no Pinterest ou perfis de Instagram que admira. Link colado entra primeiro, aberto pelo fetcher.
- **Board da página:** se existir `page/page-plan.json` com o bloco `reference_board`, a `direction` (sensação, assinatura, proibido) dele é o ponto de partida. O feed herda paleta, família de tipografia e tratamento de foto da loja, e o board daqui só complementa com o que é próprio de feed (composição quadrada e vertical, texto sobre imagem, ritmo do grid).
- **`brand.md`:** paleta, tipografia e imagery guidelines respondidas valem acima do board.

## 2. Colete no Pinterest

1. **Descoberta pela tool `WebSearch`**, nunca scrapeando o buscador. De 4 a 6 queries:
   - `site:pinterest.com <nicho> instagram feed aesthetic` (ex.: `supplement instagram feed aesthetic`)
   - `site:pinterest.com <nicho> brand instagram grid`
   - `site:pinterest.com <estilo> instagram feed` (o estilo vem do `brand.md` ou da direção da página: `clean clinical`, `warm editorial`, `bold DTC`)
   - `site:pinterest.com <nicho> product photography flat lay`
   - `site:pinterest.com instagram carousel design <nicho>`
2. **Abra pins e boards** pelo fetcher da Aura: `python3 .claude/lib/web-fetch/fetch.py "<url do pin ou board>" --mode text --json`. Quando o pin aponta pro perfil da marca, abra o perfil e olhe o grid real: é ele que vira referência.
3. **Complete com o que o dinheiro valida:** os perfis de Instagram das marcas de `competitor-analysis/dados.json` e, com o TrendTrack conectado, das marcas de maior ad rank do nicho. Delas sai composição e ritmo, nunca imagem, logo ou texto.
4. **Salve as imagens de referência** em `social-engine/board/ref-NN.png` pra ler por visão e pra o membro ver.

## 3. Monte o board (9 a 15 referências)

| # | Referência (link) | Fonte | O que se tira dela |
|---|---|---|---|
| 1 | https://... | Pinterest | Paleta: creme quente com um único acento verde-oliva |
| 2 | https://... | perfil de concorrente | Ritmo: a cada três posts, um é close de textura sem texto |

Cada linha nomeia pelo menos um eixo com o detalhe concreto: **paleta** (cor dominante e de acento), **tratamento de foto** (luz, fundo, textura, enquadramento), **composição** (produto centralizado, sangrando, flat lay, mão segurando), **texto sobre imagem** (família, tamanho, posição, quanto texto), **ritmo do grid** (como os tipos de post se alternam). Referência sem eixo concreto sai do board.

## 4. Direção de feed e aprovação

Feche em três linhas pro membro:

1. **Sensação:** o que o perfil transmite em uma frase.
2. **Assinatura:** as duas ou três escolhas que fazem o post ser reconhecível no meio do feed de quem segue.
3. **Proibido:** o que esse perfil nunca posta (ex.: foto de banco de imagens, fundo branco chapado, mais de oito palavras na imagem).

Mostre o board e a direção e pergunte em uma linha se a direção está certa. Sem aprovação, a ETAPA 2 não começa.

## 5. Onde fica salvo

- `social-engine/board/`: as imagens `ref-NN.png`.
- `social-engine/dados.json` → `brand_board`: `{ "references": [{ "url": "...", "source": "pinterest | competitor | member | page_board", "takeaways": ["paleta: ..."], "image": "board/ref-01.png" }], "direction": { "feel": "...", "signature": ["..."], "forbidden": ["..."] }, "page_board_reused": true }`. A `page-design` lê este bloco quando roda depois.
- `social-engine.md`: a seção "Board e direção do feed" com a tabela e as três linhas.
