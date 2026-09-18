# Page Build · Referência: o produto e a oferta de pé na loja (6.1b)

> Quando o produto nasce ou é conferido na loja, como cada formato de oferta sobe pelo caminho nativo do Shopify, como os botões de compra da página passam a apontar para o ID certo, o check bloqueante de IDs antes do push e o registro `store_config` do que mudou. Abra logo depois da 6.1, assim que a loja estiver detectada.

A página aprovada mostra preço, pacote, assinatura e brinde. Nada disso existe na loja antes desta sub-etapa. É ela que transforma um botão bonito em botão que vende: sem produto, sem variante e sem ID real, o formulário de compra da página devolve erro e o visitante vai embora.

**Onde entra:** depois da 6.1 (loja detectada) e antes da 6.2 (duplicate do tema). Os IDs precisam entrar no template que está em `staging/` antes do 6.4 instalar esse template no tema clonado.

**Como a Aura chega na loja:** a mesma cascade das recipes, na ordem delas. Primeiro o MCP da Shopify, quando o membro tem; depois a Admin API por GraphQL com token de app do Dev Dashboard; por último o caminho manual, em que a Aura entrega os valores exatos e o membro cola no admin. A cascade completa, com os pré-requisitos de cada degrau, está em `.claude/automations/recipes/deploy-shopify-product.md` e em `.claude/lib/mcp-detect/README.md`. Nenhum degrau é pulado e nenhum ID é inventado: quando o caminho automático não existe, o membro responde os IDs e eles entram do mesmo jeito.

## 6.1b.1 · O que a página promete

Três leituras, nesta ordem. Elas definem tudo o que precisa existir; nada aqui é escolha nova da `page-build`.

1. **`page-plan.json`, bloco `commerce`** (escrito pela `page-design`): as superfícies de compra da página, quais quantidades cada uma oferece, se a página mostra assinatura e o que ela anuncia de graça. É a lista do que o visitante vai ver e clicar.
2. **`offer-builder/dados.json`**: `pricing.main_sku_price`, `aov_levers.bundles[]` (as quantidades, os preços e os rótulos dos pacotes), `subscription_architecture` com `onetime_premium_pct`, `bonuses[]` e `guarantee`. É a fonte dos números. A `page-build` nunca recalcula preço.
3. **`checkout-aov/dados.json`, se existir** (segunda rodada, com a `checkout-aov` já rodada): `levers.bundles.tiers` manda sobre os pacotes, porque é a versão já aplicada na loja. Na primeira rodada esse arquivo não existe e a fonte é o item 2.

Plano legado sem o bloco `commerce`: reconstrua a lista lendo os blocks `pricing_tier` do template em `staging/templates/` (cada um traz `qty`) e siga; anote no `store_config` que o plano veio sem o bloco.

## 6.1b.2 · O produto na loja

**Se o produto não existe, crie.** O caminho automatizado é a recipe `.claude/automations/recipes/deploy-shopify-product.md`, que cria produto, variantes e imagens de uma vez. Uma variante por quantidade que a página oferece: a de quantidade 1 é o produto solo, as outras são os pacotes.

| Campo | De onde vem | Regra |
|---|---|---|
| Título | `manifest.product_name` | O mesmo nome que a página usa, letra por letra |
| Descrição | `copy-engine/copy-engine.md`, seção da PDP | Copy real em inglês, nunca resumo escrito na hora |
| Handle | `manifest.product_slug` | É o que entra na URL do produto |
| Imagens | `page/design/assets/` | As mesmas da página, já limpas de metadados |
| Preço de cada variante | `aov_levers.bundles[].price` | Exato, com o final de preço que a oferta definiu |
| Preço comparativo | preço solo × quantidade | O valor riscado do pacote; na variante solo fica vazio |
| SKU | `manifest.shopify_product_ops.sku_base` mais a quantidade | Pergunte uma vez ao membro e grave no manifest |
| Estoque | resposta do membro, dividida pelo mix esperado | Com controle de estoque ligado |
| Peso | peso da unidade × quantidade | Alimenta o cálculo de frete |

**Se o produto já existe, confira e complete.** Não sobrescreva o que o membro construiu: compare campo a campo com a tabela acima e só escreva no que está vazio ou divergente. Divergência de preço entre a loja e a oferta é decisão dele, e vai numa linha ao final da etapa, com os dois números. Quantidade que a página oferece e que não tem variante correspondente é criada.

**Duas armadilhas que derrubam a venda em silêncio:**

- **Produto ativo não é produto à venda.** Além do status ativo, o produto precisa estar publicado no canal Online Store. Produto ativo e não publicado responde à consulta por ID, some da loja e o botão volta erro. Confira a publicação, não só o status.
- **Variante existe e não vende.** Variante sem estoque e com controle ligado fica indisponível. Ou o estoque entra, ou a política de estoque da variante passa a permitir venda sem saldo. A escolha é do membro, porque muda a operação dele.

Produto e variantes nascem em rascunho, como toda automação da casa, e o membro publica. A publicação acontece antes do 6.10, porque página publicada com produto em rascunho é página que não vende.

## 6.1b.3 · A oferta, formato por formato

A oferta da `offer-builder` sobe pelo caminho nativo da Shopify sempre que ele existe. App é o segundo degrau, usado só onde o nativo não chega, e sempre com a configuração escrita passo a passo para o membro colar no painel.

| Formato da oferta | De onde vem | Caminho nativo | Quem executa |
|---|---|---|---|
| Pacote com desconto por volume | `aov_levers.bundles[]` | Variantes do próprio produto (default) ou produto-bundle pela recipe `.claude/automations/recipes/create-fixed-bundles.md` | `page-build`, aqui |
| Assinatura | `subscription_architecture` | App primeiro-parte Shopify Subscriptions, que cria o plano de venda; a variante recebe o plano | `page-build`, aqui |
| Desconto automático | preço promocional que a variante não carrega | Desconto automático com início e fim marcados no admin | `page-build`, aqui |
| Cupom | bônus do tipo código de desconto | Código de desconto com data de validade | `page-build`, aqui |
| Brinde por compra | `bonuses[]` do tipo brinde | Desconto automático do tipo compre e leve, que dá o brinde sozinho | `bonus-delivery`, Fase A |
| Item complementar grátis | `bonuses[]` do tipo item complementar | O mesmo compre e leve, com o produto do gatilho no lugar do valor | `bonus-delivery`, Fase A |
| Frete grátis acima de um valor | `aov_levers` | Tarifa de frete condicional nas configurações de envio | `checkout-aov`, Alavanca 4 |
| Bump no carrinho e upsell pós-compra | `aov_levers.bump` e `aov_levers.upsell` | Não há nativo; é app ou tema | `checkout-aov`, Alavancas 1 e 2 |

Os quatro primeiros são desta sub-etapa porque o que a página mostra depende deles. Os quatro últimos são de quem vem depois, e aqui só entram no `store_config` como pendência com dono e fase, para ninguém achar que a loja está completa.

**Pacote por volume.** Dois caminhos, e a escolha é pelo tamanho do catálogo. Variante do mesmo produto é o default: um produto, uma variante por quantidade, os IDs entram direto nos blocos de preço da página. Produto-bundle é para quando o pacote precisa aparecer sozinho no catálogo ou puxar estoque de mais de um produto, e aí o caminho é a recipe de bundles, que devolve os IDs prontos para o passo 6.1b.4. Desconto por quantidade calculado no carrinho, sem variante própria, exige função de carrinho publicada por um app: não prometa esse comportamento pelo caminho nativo.

**Assinatura.** O plano de venda não se cria sozinho pela API: quem segura o contrato de assinatura é um app. O caminho nativo e sem mensalidade é o app Shopify Subscriptions, que é da própria Shopify e instala pelo admin. Passos: instalar o app, criar o plano com a frequência de entrega da oferta, ligar o plano à variante e anotar o ID do plano. **Esse ID é obrigatório na página**: o formulário de compra precisa enviar o campo do plano de venda junto do ID da variante, senão o pedido entra como compra avulsa e o cliente nunca é cobrado de novo. O preço segue o contrato da oferta: a assinatura é o preço-base e o avulso é o preço-base acrescido do prêmio de `onetime_premium_pct`, nunca o contrário. Oferta com `subscription_architecture` igual a `no_subscription` pula o formato inteiro.

**Desconto automático.** Serve quando o preço que a página anuncia não é o preço gravado na variante, o caso típico de oferta de lançamento por tempo determinado. Ele aplica sozinho e aparece no carrinho, sem o cliente digitar nada. Crie com início e fim marcados e com a trava de aplicar uma vez por pedido. Desconto sem data de fim vira preço permanente e come a margem que a `offer-builder` calculou. Quando a janela é sazonal, quem manda no calendário é a `promo-engine`; aqui o desconto é o da oferta de sempre.

**Cupom.** Mesmo mecanismo, com código digitado. Só existe quando a oferta pediu um código, seja porque a página o mostra, seja porque ele é um bônus de recompra. Sempre com validade. O código nasce aqui e quem entrega ao cliente é a `retention-engine` ou a `bonus-delivery`, conforme o bônus.

**Brinde por compra e item complementar grátis.** O caminho nativo é o desconto automático do tipo compre e leve, que cobre as três condições que a oferta usa: brinde para todo comprador (o gatilho é uma unidade do produto principal), brinde acima de um valor de carrinho (o gatilho é o valor) e brinde só num pacote (o gatilho é a variante daquele pacote). App de brinde e função de carrinho ficam para o que o compre e leve não faz, como escolher entre vários brindes. Quem executa é a `bonus-delivery` na Fase A, coordenada com a `checkout-aov`; nunca por pedido de rascunho. Bônus prometido na página e ainda não configurado entra no `store_config` como pendência com o nome do bônus.

## 6.1b.4 · Ligar a oferta à página

O template em `staging/templates/page.[produto].json` sai da ETAPA 2 com um bloco de preço por quantidade, cada um com o campo do ID de variante vazio. Preencher esses campos é o que liga a página à loja.

1. **Backup antes de escrever**, no padrão da recipe: uma cópia do template com a hora no nome. A pasta do membro não tem histórico, então o backup é a única volta atrás.
2. **Case pelo campo de quantidade**, nunca pela ordem dos blocos: cada bloco de preço diz qual quantidade representa, e é essa quantidade que encontra a variante certa. Ordem de bloco muda no editor do tema; quantidade não.
3. **Cada superfície de compra, não só a tabela de preço.** O botão do topo, o botão fixo no rodapé e o botão do fim da página também mandam um ID. Todos passam pela mesma regra, e a lista deles é o `commerce.buy_surfaces` do plano.
4. **Assinatura**, quando a página mostra: o formulário leva também o ID do plano de venda ao lado do ID da variante.
5. **Grave os IDs no manifest**, pelo script, nunca editando o arquivo à mão:

```bash
python3 tools/manifest.py <slug> set \
  storefront.product_id '"gid://shopify/Product/..."' \
  storefront.product_handle '"<handle>"' \
  storefront.product_status '"draft"' \
  storefront.variant_ids '{"1": "gid://shopify/ProductVariant/...", "3": "gid://shopify/ProductVariant/..."}' \
  storefront.selling_plan_id '"gid://shopify/SellingPlan/..."'
```

É daqui que a `checkout-aov` lê os IDs para configurar bump, upsell e bundle sem perguntar de novo, e é daqui que a `bonus-delivery` tira o gatilho do brinde.

> **No loop de iteração, recompilar uma section apaga os IDs dela.** O conversor regenera o bloco do zero. Depois de qualquer recompilação da section de preço, refaça o passo 2 deste bloco antes do push, junto do rename e da restauração de ícones que a ETAPA 7 já manda refazer.

## 6.1b.5 · Check bloqueante de IDs (antes do push)

Roda com tudo já ligado e antes do 6.5. Nenhum push acontece com um item reprovado, e não existe caminho de "sobe assim mesmo": página no ar com botão quebrado gasta o dinheiro do anúncio e não devolve pedido.

1. **Nenhum ID de exemplo.** Varra o template e as sections atrás de campo de ID vazio ou com valor de demonstração (o número redondo do exemplo, o texto do modelo). Zero ocorrências.
2. **Todo ID existe na loja.** Consulte cada ID coletado e confirme que a loja responde com aquele objeto.
3. **Todo ID está à venda.** A variante está disponível para venda e o produto dela está publicado no canal Online Store. Variante que existe e não vende reprova igual a variante que não existe.
4. **Preço igual ao anunciado.** O preço da variante bate com o preço que a página mostra para aquela quantidade. Se o que fecha a conta é um desconto automático, ele existe, está dentro da janela e leva ao mesmo número.
5. **Assinatura completa.** Se a página mostra assinatura, o plano de venda existe, está ligado à variante e o formulário leva o campo do plano.
6. **Toda quantidade da página tem variante.** Cada quantidade declarada em `commerce.buy_surfaces` aparece nos IDs gravados no manifest.

Reprovou: corrija na origem, aqui mesmo, e rode de novo. O que depende de decisão do membro, como divergência de preço entre a loja e a oferta, vai a ele em uma linha com os dois números, e a etapa espera a resposta.

## 6.1b.6 · O registro do que mudou na loja

Tudo o que esta sub-etapa mexeu na loja entra no bloco `store_config` do `deploy-report.json`, com três listas que não se misturam: o que foi criado agora, o que já existia e foi conferido, e o que o membro precisa abrir no admin. O schema está em `reference/reports-e-iteracao.md`, e a versão que o membro lê é a seção "Configuração da loja" do `page-report.md`.

A terceira lista é a que mais importa, e ela é curta e acionável: cada item diz o que abrir, o que fazer lá e o que destrava. Publicar o produto, revisar o texto da descrição no admin, confirmar o estoque inicial e ligar o desconto automático na data combinada são os itens que aparecem quase sempre.

Pendência de outra fase entra com o dono escrito: o brinde é da `bonus-delivery` na Fase A, o frete grátis e o bump são da `checkout-aov`. Assim o membro lê uma única lista do estado da loja, em vez de descobrir buraco no dia do lançamento.
