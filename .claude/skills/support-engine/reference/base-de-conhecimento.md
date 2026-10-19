# Support Engine · Referência: Base de conhecimento do Obie (ETAPA 2)

> Os documentos da base, de onde sai cada um no workspace, o prazo de envio pelo modelo de estoque, a política de reembolso pela garantia e o guia de tom. Abra na ETAPA 2.

## Regra de origem

Todo fato da base sai do workspace: preço, garantia, prazo, bônus e mecanismo vêm literais da `offer-builder` e da `copy-engine`. A base nunca promete o que a oferta não promete, e nunca contradiz a página: o cliente que leu uma coisa na página e ouve outra no suporte pede reembolso. Fato que não está no workspace (endereço de devolução, nome da transportadora) é perguntado ao membro e, sem resposta, entra em `pending_inputs[]`.

## Os documentos (um arquivo por tema, em inglês)

Salvos em `support-engine/base-de-conhecimento/`, prontos pra subir:

1. **`product.md`:** o que é, o que tem dentro, como usar, quando aparece o resultado, quem não deve usar. O mecanismo pelo nome literal, explicado em linguagem de cliente.
2. **`shipping.md`:** prazo de processamento e de entrega por região, transportadora, como rastrear. O prazo depende do modelo de estoque da oferta (`offer-builder/dados.json` → `fulfillment_model` e `delivery_days_estimate`): com estoque num armazém nos Estados Unidos, de 2 a 5 dias úteis; sem estoque, com o fornecedor enviando cada pedido de fora, de 7 a 15 dias, e a resposta já diz isso de cara, com o rastreio. Quando a oferta gravou `delivery_days_estimate`, é ele que vale, literal.
3. **`guarantee-and-refunds.md`:** a garantia literal da oferta, o passo a passo do reembolso, se precisa devolver o produto, em quanto tempo o dinheiro volta.
4. **`returns-and-exchanges.md`:** troca de produto, produto com defeito, produto errado, endereço de devolução.
5. **`orders.md`:** troca de endereço antes do envio, cancelamento antes do envio, pedido duplicado, cobrança não reconhecida.
6. **`subscription.md`** (só se a oferta tem assinatura): pular uma entrega, trocar a frequência, cancelar.
7. **`bonuses.md`** (só se a oferta tem bônus): o que é cada bônus, a condição pra ganhar e como acessar.
8. **`faq.md`:** as perguntas do FAQ da página e as objeções reais do avatar de `market-research/dados.json`, cada uma com a resposta que a página já dá.

## O guia de tom

`support-engine/base-de-conhecimento/tone.md`: o tom de voz do `brand.md` adaptado pra suporte. Frases curtas, primeiro nome do cliente, resolve antes de explicar, nada de "we apologize for any inconvenience". Três exemplos de resposta boa e três de resposta ruim, todos sobre o produto real.

## Onde fica salvo

Os arquivos em `support-engine/base-de-conhecimento/` e, no `dados.json`, `knowledge_base`: `{ "docs": ["product.md", "..."], "uploaded": false, "shipping_window_days": [2, 5] }`. `uploaded` vira `true` quando o membro confirma que colou a base na Brandwise.
