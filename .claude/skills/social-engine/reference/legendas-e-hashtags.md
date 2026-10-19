# Social Engine · Referência: Primeiro lote, legendas e hashtags (ETAPA 3)

> O sim de custo, a geração do lote pela fórmula, a conferência por visão, a estrutura da legenda, o banco de hashtags e a aprovação do grid montado. Abra na ETAPA 3.

## 1. Custo antes de gerar

Mostre ao membro: créditos por imagem, créditos do lote de 9 e o custo de 30 dias de rotina. Gere só depois do sim. Esse sim vira o `daily_credit_cap` da rotina: ela nunca gasta acima dele num dia.

## 2. Gere e confira

1. Gere as 9 pela fórmula do grid (hoje `execute_preset` pros templates do banco, ou `generate_image_batch` pros prompts próprios), proporção 4:5 (1080 × 1350), com o produto do Ads Studio como referência. Espere os jobs (hoje `jobs_wait`) e baixe os arquivos pra `social-engine/<data>/`.
2. Confira cada imagem por visão:
   - o produto está fiel (rótulo, cor, formato da embalagem);
   - o texto na imagem está escrito certo, sem letra deformada;
   - mãos, rostos e proporções estão normais;
   - nada bate com o "Proibido" da direção.
   Imagem que falha é refeita, até duas vezes. Na terceira, troque o template daquela posição.
3. Monte uma prévia do grid 3x3 (as 9 lado a lado, na ordem em que vão aparecer no perfil) e salve como `social-engine/<data>/grid-preview.png`.

## 3. A legenda de cada post

Copy pro consumidor final: inglês US (ou a língua do público), na força máxima que a pesquisa sustenta, sem aviso nem suavização (regra 8b). Estrutura:

1. **Primeira linha é o hook:** é a única que aparece antes do "mais". Use frase de VOC real de `market-research/dados.json` ou um hook aprovado da `creative-engine`. Nunca comece com o nome da marca.
2. **Corpo de duas a cinco linhas curtas:** uma ideia só, ligada ao papel da posição (dor, mecanismo pelo nome literal da `offer-builder`, prova, oferta).
3. **CTA:** "link in bio", "comment X and we'll DM you the link" ou "save this for later", alternando entre os posts do lote.
4. **Hashtags:** 15 a 25 por post, separadas do corpo por uma linha em branco.

Travessão no máximo um por legenda (regra 8a). Emoji só se a direção do feed permitir, e nunca mais que dois.

## 4. O banco de hashtags

Monte uma vez, por WebSearch e pelos perfis dos concorrentes, e grave em `dados.json` → `hashtag_bank`:

- **Volume alto (milhões de posts):** 3 a 5 por post, pra alcance.
- **Nicho (dezenas a centenas de milhares):** 8 a 12 por post, onde o post consegue aparecer no topo.
- **Específicas do problema e do ingrediente:** 4 a 6 por post.
- **Marca:** 1 ou 2 próprias, sempre.

Cada post sorteia do banco por papel, sem repetir o mesmo conjunto dois dias seguidos.

## 5. Aprovação

Mostre a prévia do grid e as 9 legendas. Pergunte por dimensão (rule `iteration-driven-refinement.md`): a cara do feed está certa, as legendas estão no tom, a oferta está forte o bastante. Ajuste até o membro aprovar. O lote aprovado é o padrão que a rotina copia, e as legendas dele entram no `rotina-prompt.md` como exemplo.
