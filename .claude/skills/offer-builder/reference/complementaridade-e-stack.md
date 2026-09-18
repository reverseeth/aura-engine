# Offer Builder · Referência: Gate de Complementaridade, bump, upsell, stack de valor e bônus (ETAPA 3, segunda parte)

> A hierarquia de 4 categorias que todo componente de AOV atravessa, a derivação de candidatos quando o membro não sabe, checkout bump e upsell pós-compra com as taxas de aceitação, o bloco `aov_levers`, os sistemas de stack e bônus, a regra do `Not: "___"` e o registro de `bonuses[]` com o enum canônico. Abra depois da primeira parte da ETAPA 3.

**Gate de Complementaridade (OBRIGATÓRIO pra TODO componente de AOV — bump, upsell, bundle-mate, GWP):**

Nenhum componente entra na oferta por ser "um produto que dá pra vender junto". Todo candidato passa pela hierarquia abaixo — avalie na ordem; a categoria mais alta em que ele se encaixa define a prioridade:

1. **More-of-same** — mais unidades do PRÓPRIO produto (bundle, supply maior). Default e maior aceitação: pra comprador NOVO de tráfego frio, o que mais converte no pós-compra não é complemento, é o mesmo produto com desconto exclusivo do momento (operadores de supplements documentaram publicamente AOV saindo de $70-80 pra $100-130 só com isso). Inclui o "big swing": supply de 3-6 meses a 3-5× o valor do pedido — aceita menos, mas ganha em lucro por visitante.
2. **Consumption chaining** — item consumido JUNTO, no mesmo ritual de uso do produto principal (o cleanser antes do sérum, o shaker do pré-treino).
3. **Aceleração de resultado** — item que encurta o tempo até o resultado do desejo central (menos Time Delay = Value Equation melhor).
4. **Problema adjacente** — o PRÓXIMO problema que o avatar enfrenta DEPOIS de alcançar o resultado (o passo seguinte da jornada).

**REPROVADO:** componente que não se encaixa em NENHUMA das 4 = complemento aleatório — fica fora da oferta.

**Se o membro respondeu "não sei" na pergunta 3 da ETAPA 1:** NÃO pule e NÃO aceite qualquer coisa. DERIVE 3-5 candidatos das 4 categorias cruzando o market research: ritual de uso + desejo central + jornada do avatar (`market-research/market-research.md` + `dados.json`) e o que o avatar já compra/tenta pra resolver o problema (`alternative_solutions` da `market-research` e da `competitor-analysis`). Apresente cada candidato com a categoria em que se encaixa.

**Branch "sem complemento viável":** se nenhum candidato externo passa no gate, a categoria 1 (more-of-same) SEMPRE existe — bundle e big swing não dependem de segundo produto. Zere as linhas de bump/upsell externo na tabela de unit economics (ETAPA 5) em vez de forçar componente aleatório.

**Segmentação novo vs recorrente:** a hierarquia acima vale pro funil FRIO (comprador novo). Cliente recorrente inverte: produto complementar não-testado converte 20-35% melhor pra quem já confia na marca — essa é alavanca das Skills `checkout-aov` (superfícies de checkout pra recorrente) e 13 (retention), não do funil de aquisição.

**Checkout Bump:**
- Componente aprovado no Gate (tipicamente categoria 2-4) de baixo preço ($9-19) ou add-on (frete expresso, versão com mais, etc)
- Taxa de aceitação: 20-35% quando bem posicionado (conservador: 20%). O teto de 20-50% vem do order-form bump de funil dedicado; em checkout Shopify real o range observado fica mais perto do piso — recalibre com o take rate real após 2 semanas
- Copy curta do bump (1 frase + 1 benefício)

**Upsell Pós-Compra:**
- Prioridade 1 (tráfego frio): **more-of-same** — o próprio produto com desconto exclusivo do momento pós-compra, ou o big swing (supply 3-6 meses)
- Prioridade 2: componente aprovado no Gate de maior ticket ($47-97+) que amplia o resultado
- Apresentado na thank-you page após a compra (a `checkout-aov` implementa a superfície)
- Taxa de aceitação: média da plataforma 3-8%; oferta bem casada (Gate + more-of-same) chega a 8-14% (conservador: 8%)
- Copy do upsell (2-3 frases + principal benefício + oferta)

**OBRIGATÓRIO — Registrar bump, upsell e tiers de bundle no bloco top-level `aov_levers` do `offer-builder/dados.json`** (estrutura exata no Output Schema no fim desta skill). A Skill `checkout-aov` lê DESSE bloco na ETAPA 1 dela — não da prosa acima (a prosa é a versão humana). Alavanca que a oferta não tem = `null` (nunca inventar).

**Stack de Valor Com Ancoragem:**

**Puxe estes SISTEMAS NOMEADOS de stack/bônus antes de montar (rode a `best_query` de cada):**
- **Bonus Stacking (Value Stack / Stack Slide)** (rode `value stack stack slide bonus stacking standalone value exceeds price`) — soma cumulativa que faz o preço parecer pequeno.
- **Razor-Blade vs Handle (Bonus Fit Principle)** (rode `razor blade vs handle bonus fit natural complement to product`) — cada bônus deve aumentar o consumo/resultado do produto principal.
- **Bonus Types Taxonomy** (rode `bonus types presuppose success enables success graduation gift access partner complementary`) — escolhe o `type` certo (não default pra PDF), alimenta o campo `bonuses[]` do JSON.
- **P.S. que Acrescenta — Fast-Reply Gift** (rode `P.S. acrescenta bonus novo fast-reply gift nao recapitula oferta 154 de 179`) — padrão medido em 154 de 179 peças: o P.S. ACRESCENTA um bônus novo (o fast-reply gift, prêmio por agir agora) em vez de recapitular a oferta. A decisão de oferta é aqui: se o stack tiver um bônus com essa vocação, marque-o — a Skill `copy-engine` escreve o P.S.; a oferta define qual bônus ele entrega.

**Nomeação dos entregáveis — a regra do `Not: "___"` (OBRIGATÓRIA antes de escrever o stack):**

A palavra genérica da categoria é **proibida em toda a pilha de entregáveis**. Se o stack lista "e-book", "vídeo", "newsletter", "acesso ao grupo", ele está descrevendo **formato** em vez de nomear **ativo** — e formato não tem valor percebido. Ninguém paga por "um PDF"; paga pelo ativo que aquele PDF é.

Como executar, item por item (produto principal, bônus e entregáveis inclusos):

1. Escreva a palavra genérica que você ia usar, marcada como proibida: `Not: "e-book"`.
2. Nomeie o ativo pelo trabalho que ele faz na vida do comprador, não pelo arquivo que ele é.
3. Só entra no stack o nome do passo 2.

Exemplos reais desse método aplicado numa peça vencedora: email virou **"Mission Order"**, vídeo virou **"Debriefing"**, site virou **"Digital Headquarters"**, carteira virou **"Victory Scorecard"**. Na peça auditada a anotação `Not: "___"` aparece 9 vezes só na seção de oferta — a disciplina é item a item, não uma passada geral no fim.

Detalhe completo do método em `.claude/lib/swipe-models/specimens.json` → nó `auditoria`, camada `rosa-nomeacao`. **E puxe o sistema completo da base:** rode `not X renomear termo generico por proprietario newsletter research service charter member` (deep=true) — é a entrada `Not: X` do índice, com o percurso da oferta inteira trocando cada termo-commodity por nome proprietário (newsletter → research service, assinante → charter member).

Dois limites que evitam erro na aplicação:
- **O nome nomeia, não promete o que o ativo não entrega.** Nome proprietário não é licença pra inflar: o entregável continua sendo o que é, e o `value_anchored` continua preso à regra de valor legalmente sustentável (o bônus tem que ser realmente vendível por aquele valor).
- **O nome é copy pública (inglês US); o formato técnico continua nos campos de máquina.** `bonuses[].name` e a string `offer_stack` recebem o nome proprietário; `type` e `format_hint` continuam com o enum técnico (`free_ebook`, `pdf`, `community_access`) — é isso que a Skill `bonus-delivery` usa pra montar a entrega. Não há contradição entre os dois campos: o comprador lê o ativo, o pipeline lê o formato.

Liste tudo que vem no pacote com valor ancorado (todos os nomes já passados pela regra acima):
- Produto principal: valor $X
- Bonus 1 (o ativo nomeado — `Not: "guia digital"`): $Y
- Bonus 2 (o ativo nomeado — `Not: "acesso ao grupo"`): $Z
- Bonus 3 (o ativo nomeado — `Not: "consultoria inicial"`): $W
- **Valor total**: $X+Y+Z+W
- **Preço hoje**: $(preço real)
- **Economia percebida**: $(diferença)

Cada bonus é REAL (entregável), não inflado artificialmente. O stack cria percepção de valor desproporcional ao preço. Bônus físicos (`gift_with_purchase` / `free_complementary_sku`) também passam no **Gate de Complementaridade** acima; os digitais seguem o Razor-Blade (o mesmo gate aplicado a conteúdo: o bônus aumenta o consumo/resultado do produto principal, senão descarta).

**OBRIGATÓRIO — Registrar bonuses no campo top-level `bonuses[]` do `offer-builder/dados.json`.** Skill `bonus-delivery` lê desse campo pra montar o pipeline de entrega. Pra cada bonus do stack, gerar entry (enum idêntico ao do Output Schema no fim desta skill — é o enum canônico):

```json
{
  "id": "bonus-01",
  "name": "o ativo nomeado — texto igual ao da stack, nunca a palavra de formato (regra do Not: \"___\")",
  "description": "1-2 frases do que é e por que vale",
  "value_anchored": 49,
  "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
  "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
  "condition": "unconditional | cart_threshold | tier_specific",
  "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
}
```

**`condition` é OBRIGATÓRIO e a Skill `bonus-delivery` configura a entrega exatamente por ele:** bônus mostrado no offer_stack da PDP a TODO comprador = `unconditional` (auto-add em toda compra — threshold aqui quebraria a promessa da página); GWP destravado por subtotal do carrinho = `cart_threshold` (e a copy da página DEVE dizer a condição: "FREE over $X"); brinde de tier específico (3-pack/6-pack) = `tier_specific`. Mismatch entre condition e o que a página promete é promessa quebrada na cara do comprador.

**Tipos NÃO default pra "PDF":** escolher o type que realmente bate com o avatar. Se membro disser "bonus é PDF só porque é fácil", questionar: "Esse avatar REALMENTE quer PDF? Pra [avatar profile], [alternative type] costuma ter access rate maior." Documentar essa decisão.
