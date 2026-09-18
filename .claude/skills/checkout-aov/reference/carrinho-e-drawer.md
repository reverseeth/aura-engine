# Checkout & AOV · Referência: o carrinho e a gaveta lateral

> A última superfície antes do checkout, personalizada por completo: identidade da página, barra de progresso do frete grátis, item sugerido, prova social curta, garantia visível e edição de quantidade sem recarregar. Abra na ETAPA 5, junto dos caminhos de tema.

O carrinho é o único ponto do funil depois da página em que o membro tem controle total do que aparece. Depois dele começa o checkout, que a Shopify fecha. E ele é o momento mais nervoso da compra: a pessoa já escolheu e está decidindo se conclui. Carrinho que nasce com a cara padrão do tema, em outra tipografia e sem nenhum reforço, desmonta em cinco segundos a página que levou semanas para ficar de pé.

Esta referência é a dona da superfície do carrinho. As Alavancas 1, 2, 4 e 5 continuam decidindo **o quê** entra (qual complemento, qual valor de frete grátis, qual garantia); aqui se define **como** aquilo aparece e funciona no carrinho e na gaveta lateral.

## De onde vem cada peça

Nada aqui é escrito na hora. Cada elemento tem uma fonte, e divergência entre carrinho e página é drift que a `consistency-audit` pega.

| Peça do carrinho | Fonte |
|---|---|
| Cores e tipografia | `page/design-tokens.json` (a mesma paleta e as mesmas famílias da página) |
| Valor do frete grátis | `levers.free_shipping_threshold.threshold`, da Alavanca 4 |
| Item sugerido | `levers.cart_bump`, da Alavanca 2, com o ID de variante real de `manifest.storefront.variant_ids` |
| Garantia | `guarantee` do `offer-builder/dados.json`, com o mesmo prazo da página de política |
| Números de review | O app de review da loja (Judge.me, Loox, Yotpo), nunca número escrito de cabeça |
| Copy de tudo acima | Inglês US, direta e sem aviso, sem travessão em headline |

## As seis peças

**1. Identidade.** O carrinho usa a paleta e a tipografia da página, e a gaveta lateral também. A armadilha conhecida está em `.claude/lib/shopify-section-patterns/fonte-universal.md`: declarar a fonte nas sections da página não alcança os componentes do tema, e o funil termina em duas tipografias diferentes justo na transição mais sensível. A correção é a regra de fonte universal daquele arquivo, que inclui a gaveta e os campos de formulário por nome.

**2. Barra de progresso do frete grátis.** Mostra quanto falta para o frete zerar, com o número exato ("You're $12 away from free shipping") e uma barra que anda conforme o subtotal muda. Quando o valor já foi cruzado, a barra vira confirmação, não some. O valor anunciado é o mesmo da tarifa de frete condicional configurada na Alavanca 4; barra e tarifa nunca podem divergir, senão o cliente vê a promessa e o checkout cobra frete.

**3. Item sugerido.** Um complemento só, o que passou no Gate de Complementaridade da ETAPA 1, com imagem pequena, nome, preço e um botão de adicionar que não tira a pessoa do carrinho. Dois ou mais itens sugeridos transformam o carrinho em vitrine e adiam a decisão. O ID de variante vem do manifest; sem ID real, o item não entra.

**4. Prova social curta.** Uma linha, com o número de reviews e a nota do app de review. Ela ocupa o lugar da dúvida de última hora, e é curta porque o carrinho não é lugar de ler depoimento.

**5. Garantia visível.** O texto da garantia da oferta, com ícone SVG, acima do botão de fechar o pedido. É a peça que mais reduz o abandono no momento de digitar o cartão e a que mais costuma ficar de fora.

**6. Edição de quantidade sem recarregar.** Aumentar, diminuir e remover atualizam o total ali mesmo. **Confira antes de implementar:** a maioria dos temas atuais já faz isso na gaveta lateral. Só entre no código quando o teste mostrar recarga de página inteira ao mudar a quantidade.

## Como implementar sem forkar o tema

O padrão endurecido em produção está em `.claude/lib/shopify-section-patterns/drawer-enriquecido.md`, com o código de referência pronto para adaptar. Ele resolve os três problemas que fazem qualquer tentativa ingênua falhar:

- **O tema redesenha o interior da gaveta a cada mudança de carrinho**, então qualquer coisa injetada some na atualização seguinte. A função de injeção é idempotente e está pendurada em três gatilhos redundantes (os eventos de carrinho do tema, um observador de mudanças no próprio elemento da gaveta, e o clique no ícone do carrinho com uma escada de esperas).
- **O visual se aplica de fora**, por seletores do próprio componente, a partir do snippet de tokens da página. Nenhum arquivo do tema é modificado, então o próximo update do tema não vira trabalho de merge.
- **O adicionar ao carrinho é interceptado com volta garantida**: adiciona por requisição, busca o estado novo, dispara os eventos do tema e abre a gaveta; se a requisição falhar, o envio nativo do formulário assume. Interceptar sem essa volta é a pior falha possível numa loja, porque o clique em comprar simplesmente não faz nada.

Aquele arquivo foi endurecido no tema Impact. Em outro tema mudam os nomes dos seletores e dos eventos; a mecânica e as armadilhas são as mesmas. Descubra os nomes no tema clonado antes de adaptar, nunca por suposição.

Toda edição segue a rule `.claude/rules/shopify-theme-safety.md` por inteiro, no tema de `manifest.storefront.theme_id`: pull antes de editar, marker no elemento raiz do que foi tocado, push com `--path` e `--nodelete`, verificação do marker e smoke test.

**Nunca use pedido de rascunho para simular a oferta no carrinho.** Ele não dispara no fluxo normal de compra, não passa pelo checkout que o cliente usa, não conta no pixel e some no autoatendimento. Oferta que só existe em pedido de rascunho é oferta que o cliente nunca vai ver.

## Verificação antes de fechar

Num carrinho de verdade, no celular e no computador, com o tema em preview:

1. A gaveta abre na paleta e na tipografia da página, sem nenhum texto na fonte padrão do tema.
2. A barra de frete grátis mostra o valor que falta, anda ao mudar a quantidade e confirma quando o valor é cruzado.
3. O item sugerido adiciona sem sair do carrinho, e o total muda.
4. Aumentar, diminuir e remover atualizam o total sem recarregar a página.
5. A garantia e a linha de prova social aparecem acima do botão de fechar o pedido.
6. O botão de fechar o pedido leva ao checkout com os itens certos.

Item reprovado volta para o passo dele. Só com os seis verdes o carrinho entra no relatório como aplicado.

## O que entra no registro de configuração

Tudo o que esta skill mudou na loja entra no bloco `store_config` do `checkout-aov/dados.json`, com as mesmas três listas da `page-build`: o que foi criado agora, o que já existia e foi conferido, e o que o membro precisa abrir no admin. O schema está em `reference/salvar-e-manifest.md`, e a versão que o membro lê é a seção "Configuração da loja" do `checkout-aov.md`.

Aqui os itens típicos da terceira lista são a tarifa de frete grátis criada nas configurações de envio, a configuração colada no painel de cada app de upsell e a publicação do tema quando o carrinho foi editado num tema em preview.
