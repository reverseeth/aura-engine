# Page Design · Referência: Gerar as imagens que faltam, in-session (sub-etapa 1.6.3)

> A rota de geração de imagem pelo MCP da Higgsfield: quando ela existe, o que se gera e o que nunca se gera, a confirmação antes de gastar crédito, como o prompt nasce, a régua que lê cada imagem por visão antes de ela entrar na página, as 3 tentativas por slot e o caminho do arquivo até o slot. Abra no passo 3 da sub-etapa 1.6, depois do mapa de mídia fechado.

## Quando esta rota existe

Detecção por prefixo de tool na sessão, como manda o canon `.claude/lib/mcp-detect/README.md`: há ao menos uma tool `mcp__higgsfield__` disponível?

- **Não há.** Esta rota não existe nesta sessão. O passo 3 da 1.6 segue como está escrito em `assets-de-imagem.md`: o prompt de cada imagem que falta é salvo para o membro gerar onde ele quiser, ou o slot vira placeholder explícito com `acquisition_plan`. Nada desta página aparece na conversa, e não se menciona o MCP ausente.
- **Há.** Rode esta rota **depois** que o mapa de mídia da 1.6 estiver fechado. Ela preenche os slots que o mapa declarou; ela nunca cria slot, nunca acrescenta seção e nunca gera imagem que a página não pediu.

**As tools se descobrem em runtime.** Leia a descrição de cada tool do prefixo antes da primeira chamada: nome de tool, nome de modelo e parâmetro mudam de uma versão para a outra; o prefixo não. O que o MCP oferece hoje: geração de imagem a partir de texto, de uma imagem de referência ou dos dois juntos, personagem consistente entre gerações, e o histórico das gerações da conta. **A geração é assíncrona:** a chamada volta antes da imagem ficar pronta, então consulte o status até o arquivo existir. Slot só é dado como pronto com o arquivo na mão — nunca por ter chamado a geração.

## O que se gera e o que não se gera

| `media.kind` do slot | Gera aqui? |
|---|---|
| `lifestyle` | Sim. É o caso principal: a cena de contexto ou de resultado, com ou sem pessoa em quadro. |
| `review_faces` | Sim, pelas regras de pessoa da lib (abaixo), com a distribuição de idade e gênero saindo dos avatares da `market-research`. |
| `packshot` | Não. Rótulo, embalagem, frasco e qualquer texto de embalagem vêm de foto real, do fornecedor ou do membro. Sem nenhuma foto real do produto, isso é bloqueio de inventário: peça a foto, é pré-requisito de qualquer rota. |
| `before_after_pair` | Não. O par antes e depois é prova, e prova gerada é prova inventada. Par real, ou a seção sai do plano. |
| `diagram` | Não por geração de imagem. Diagrama de mecanismo é SVG desenhado na página, que fica nítido em qualquer tela e o membro consegue corrigir depois. |

## Confirme antes de gastar crédito

O crédito é do plano do membro. Antes da primeira chamada, uma mensagem só, com número:

> "Higgsfield conectado. Faltam imagens em [N] slots: [id da section] ([o que a cena precisa mostrar]), [id da section] (...). Gero agora? Cada slot tem até 3 tentativas se a imagem sair com defeito, então o teto é [N × 3] gerações. Se preferir, salvo os prompts e você gera aí."

Ele recusou: salve os prompts e trate os slots como o `assets-de-imagem.md` manda. Se alguma tool do MCP informar o saldo de crédito, mostre o saldo junto do número de gerações; se não informar, não estime saldo.

## Como o prompt nasce

**O cânone do prompt com pessoa em quadro é `.claude/lib/prompt-directors/real-people-imagery.md`**, e ele vale inteiro aqui: pessoa crível em vez de modelo, públicos distribuídos pela pesquisa, embalagem real como referência anexada, specs de câmera e de luz, cenário imperfeito e proporção declarada. Sem pessoa em quadro, o bloco de câmera, luz e cenário continua valendo do mesmo jeito: é ele que separa fotografia de render.

Três coisas são desta etapa e se somam ao que está lá:

1. **A âncora do produto é uma só, e é a mesma em todas as gerações.** Escolha uma foto real do produto no inventário da 1.6 e use aquele arquivo como referência em toda imagem do site que mostra o produto. É o que faz o frasco ser o mesmo frasco no hero, na seção de mecanismo e na foto de uso. Trocar a referência no meio do caminho entrega três produtos diferentes na mesma página. No prompt, junto da referência: `label and packaging exactly as in the reference image, do not redesign`.
2. **A proporção sai do slot, não do gerador.** O hero de desktop é horizontal (3:2 ou 16:9), a foto de seção vertical é 4:5, o retrato de review é 1:1 ou 4:5. Declare a proporção no prompt e gere já na proporção certa: recortar depois corta justamente a margem que o enquadramento precisava.
3. **Nenhum texto legível dentro da imagem.** Nem headline, nem selo, nem rótulo inventado. O texto da página é HTML, onde ele é nítido, traduzível e editável. Texto desenhado pelo gerador derrete e reprova (bloco de reprova, abaixo).

**Quando dois slots mostram a mesma pessoa** (a cena do hero e a continuação dela numa seção de uso, por exemplo), fixe o personagem pelo recurso de consistência do MCP e reaproveite entre as gerações. Sem isso, o rosto muda de uma foto para a outra e a página se denuncia sozinha.

## A régua: cada imagem é lida por visão antes de entrar na página

Abra cada imagem gerada e **leia por visão**, item a item, com a evidência escrita ao lado (o que você viu e onde). Item sem evidência conta como reprovado, porque não foi conferido — a mesma regra do placar da `reference/regua-de-design.md`.

**Produto.** O rótulo, a cor e o formato da embalagem são os da foto de referência, sem redesenho. Frasco não virou pote, pote não virou sachê. Nenhuma palavra nova apareceu na embalagem.

**Pessoa: tem que parecer fotografia, não computação gráfica.**

- Pele com textura e imperfeição: poro visível, fio de cabelo fora do lugar, assimetria natural do rosto. Pele lisa e uniforme reprova.
- Uma fonte de luz, com a sombra caindo de acordo com ela.
- Profundidade de campo de lente real: o que está longe do plano de foco desfoca de verdade, e desfoca progressivamente.
- Enquadramento de fotógrafo: o assunto fora do centro exato, margem que respira de um lado, algo cortado pela borda. Composição perfeitamente simétrica e centralizada é assinatura de renderizador.
- Zero brilho plástico na pele, no cabelo e no produto.

**Reprova automática. Cada um destes reprova a imagem sozinho:**

- Mão com dedo a mais, dedo a menos ou dedo dobrado para onde não dobra.
- Texto ilegível em qualquer lugar do quadro: letra derretida, palavra sem sentido, logo borrado.
- Reflexo impossível: sombra sem fonte que a explique, reflexo que não corresponde ao que está na cena, espelho mostrando o que não existe no quadro.
- Fundo que derrete: linha reta que se dobra sozinha, objeto que funde no outro, moldura que continua do lado errado.
- Duas fontes de luz brigando: duas sombras do mesmo objeto em direções diferentes.
- Olhar vidrado: pupila morta, olhos apontando para lados diferentes, íris derretida.

**A régua da página e esta régua são o mesmo padrão em dois momentos.** O item S5 de `reference/regua-de-design.md` reprova a foto de catálogo com sorriso corporativo olhando no print da página inteira; esta régua reprova o arquivo antes dele entrar na página. Imagem que passa aqui e reprova no S5 volta para cá com o defeito nomeado — não se conserta no CSS.

## Três tentativas por slot, e o que acontece na terceira

1. Reprovou: **corrija o prompt pelo defeito que você nomeou** e gere de novo. Repetir o mesmo prompt devolve o mesmo defeito.
2. Reprovou de novo: mude a direção da cena, não só o adjetivo. Outro ângulo, outro momento da ação, outro enquadramento, mão fora do quadro quando o defeito é de mão.
3. Reprovou na terceira: **pare.** O slot vira `status: "placeholder"` com `acquisition_plan` específico no `page-plan.json`, e vai ao membro em uma linha: qual slot, o que reprovou nas três e as duas saídas (a foto real dele, ou outra rodada com uma direção de cena que ele descreve). A `page-build` bloqueia o deploy enquanto o placeholder existir, que é o comportamento certo.

Nunca coloque na página a menos ruim das três. Imagem com defeito custa mais caro que slot vazio: o slot vazio o membro vê e resolve, o defeito o cliente vê e desconfia.

## Do arquivo gerado até o slot (nesta ordem)

1. **Baixe para `workspace/[produto]/page/design/assets/`**, com nome por uso (`hero-lifestyle.jpg`, `mechanism-closeup.jpg`). Nunca deixe o `src` da página apontando para a URL do gerador: ela expira, e a página seria aprovada com uma imagem que vai sumir.
2. **Reduza para a largura do slot.** O gerador entrega até 4K, e a página aprovada carrega no browser do membro antes de existir CDN nenhuma. Alvo pelo maior lado: hero 1600px, imagem de seção 1200px, retrato de review 600px. No Mac, com o que já está instalado:
   ```bash
   IMG=workspace/[produto]/page/design/assets/hero-lifestyle.jpg
   sips -g pixelWidth -g pixelHeight "$IMG"     # confira ANTES
   sips -Z 1600 "$IMG"                          # só quando o maior lado passa de 1600
   ```
   O `-Z` também AMPLIA: rodar sobre imagem menor que o alvo degrada a imagem. Por isso o `-g` vem antes. Sem `sips` na máquina, siga com o arquivo como veio e registre o peso no gate de performance da 3.7.
   **Não converta para WebP aqui.** O `sips` do macOS não escreve WebP e o ffmpeg padrão do Homebrew vem sem o encoder, então a conversão viraria uma dependência a instalar por nada: quem serve WebP e AVIF na loja é o CDN da Shopify, pelo `image_url` com `width:` que a `page-build` já usa.
3. **Limpe os metadados, por último** (regra 12). O gerador grava a própria assinatura no arquivo, e qualquer redimensionamento ou conversão volta a gravar tag de encoder — por isso o limpador é o último passo, nunca o primeiro:
   ```bash
   bash tools/strip-metadata.sh workspace/[produto]/page/design/assets/ --sem-renomear
   bash tools/strip-metadata.sh workspace/[produto]/page/design/assets/ --verificar   # exit 0 = limpo
   ```
   (da raiz do repositório, como todo comando de `tools/`)
   O `--sem-renomear` é obrigatório aqui: sem ele o arquivo vira `asset-xxxx.jpg` e todo `src` da página e todo `media.asset` do plano apontam para um arquivo que mudou de nome. O nome `asset-xxxx` é a exigência de quem sobe criativo para plataforma de ads; aqui o arquivo entra na loja, e o nome por uso é o que o membro reconhece no editor de tema.
4. **Registre no `page-plan.json`:** `media.source: "ai_lifestyle"` (é o valor do enum para imagem gerada, inclusive quando o `kind` é `review_faces`), `media.status: "ready"` e `media.asset` com o caminho final em `design/assets/`.

**Nada na imagem, na página ou no texto diz como a imagem foi feita.** Sem marca d'água, sem rótulo de origem, sem legenda explicando a geração, sem asterisco (rule 8b).

## Quando a chamada falha no meio

Erro de autenticação, crédito acabado ou tool fora do ar não abortam a 1.6 (`emergency-escape-paths`). Degraus, em ordem: outra tentativa; os prompts salvos para o membro gerar onde ele já tem conta; o slot como placeholder explícito com `acquisition_plan`. Diga em uma linha o que aconteceu e qual degrau você pegou. Nunca peça credencial, cookie nem chave ao membro.

## Fora do escopo desta etapa

Vídeo e criativo de anúncio são da `creative-engine`, que tem a própria rota de render in-session pelo mesmo MCP. Aqui se produz imagem para a página da loja, e só.
