# Offer Builder · Referência: SALVAR e mensagem final

> A estrutura do `offer-builder.md` (ficha da oferta primeiro, números numa tabela só, detalhes curtos depois), o dual output e a mensagem final. Abra ao fechar a oferta.

## SALVAR (dual output, regra 6b do CLAUDE.md)

O `.md` é a fonte pras fases seguintes; o `.html` é o que o membro abre, gerado com `python3 tools/render_report.py offer-builder/offer-builder.md` (nunca escrito à mão; componentes em `.claude/templates/aura-html-components.md`). Salve também `offer-builder/research-foundation.json` (ETAPA 2.5) e o `dados.json` (schema em `reference/dados-json.md`).

## O doc: claro, curto, na ordem em que o membro lê

O `offer-builder.md` é a oferta, não o caminho até ela. O detalhe técnico pesado (fórmulas, breakdown item a item, cenários) vive no `dados.json`; o doc mostra o resultado em frases curtas, com todo termo explicado na primeira vez (regra 0). Nenhuma seção repete outra. Segue `.claude/rules/report-only-results.md`.

**1. Ficha da oferta (uma tela)**

Um bloco só, que responde sem rolar a página:
- **O que o cliente recebe:** o produto e cada item do stack pelo nome (regra do `Not: "___"`)
- **Preço de cada opção:** Solo, Popular e Best Value, com o preço por unidade ao lado; assinatura, se existir, em uma linha
- **Brindes e bônus:** nome e condição de cada um
- **Garantia:** a frase como o cliente lê
- **Envio:** modelo de estoque (com estoque, sem estoque ou sem estoque com migração) e prazo de entrega
- **Por que é irrecusável:** as 3 frases do teste "burro de dizer não" (ETAPA 4.5), em inglês, com tradução livre ao lado
- **Contra o concorrente principal:** a tabela lado a lado da ETAPA 4.5

**2. Os números (uma tabela)**

| Número | Valor | O que significa |
|---|---|---|
| Ticket médio esperado (AOV) | | o que cada pedido rende em média, com bump e upsell |
| Margem por pedido | | o que sobra depois de todos os custos variáveis; ainda não é lucro |
| Custo por cliente alvo (CPA alvo) | | o máximo pra pagar por cliente novo e dobrar o dinheiro |
| ROAS de equilíbrio | | quanto cada dólar de anúncio precisa voltar pra empatar |
| Viabilidade no seu budget | | viável, apertado ou inviável, em uma frase |

Se os custos fixos não foram informados, uma frase embaixo da tabela: sem eles, a conta mostra margem, não lucro.

**3. Mecanismo único**

Nome, a lógica do problema (por que o que o cliente já tentou falhou) e a da solução (por que a nossa funciona), em 3 a 5 frases, sem versões de copy.

**4. Provas**

Os 3 a 5 números mais fortes do banco de provas, cada um com a fonte em uma linha. A lista completa fica no `research-foundation.json`.

**5. Como a oferta foi montada**

Uma frase por peça: por que esse preço (as 3 âncoras), por que esses bundles, por que esse bump e esse upsell (a categoria do Gate de Complementaridade), por que essa garantia.

**6. Economia completa**

A tabela do primeiro pedido (5A) e, em consumível ou assinatura, a da recompra (5B). A palavra lucro não aparece nesta seção.

**7. Simulação de budget**

Os dois níveis numa tabela, com margem de contribuição e resultado depois dos custos fixos em linhas separadas.

**8. O que está validado**

As checagens da ETAPA 9 e o teste da ETAPA 4.5 como afirmações curtas, cada uma com a evidência em uma frase.

## Mensagem final

"Primeira versão da oferta pronta. Mecanismo: **[nome]**. Modelo de estoque: [com estoque / sem estoque / sem estoque com migração], entrega em [prazo]. Contra o [concorrente principal], a gente vence em [eixos] e só a gente tem [diferencial].

Margem por pedido: [valor], o que sobra depois dos custos variáveis. CPA alvo: [valor]. Viável pro seu budget: [sim / com ajustes]. [SE os custos fixos não foram informados: "Sem os seus custos fixos mensais, não dá pra dizer se há lucro; me passa esse número e eu fecho a simulação."]

Revisa a ficha: o nome do mecanismo gruda? Os preços e o stack fazem sentido pro seu cliente? A garantia ataca o medo certo? Me diz o que não fecha e eu ajusto.

Quando fechar, diga **'copy'** pra escrever a página com essa oferta."
