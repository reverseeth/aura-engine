# Copy Engine · Referência: Página completa, prova social e oferta com ancoragem (ETAPA 4, segunda parte)

> O proof stacking com os frameworks de prova, a regra dos testimonials reais (placeholder listado, nunca depoimento fictício), a oferta e o stack a partir da `offer-builder`, a copy de bônus e GWP governada por `bonuses[].condition` e a pricing psychology com os sistemas de ancoragem. Abra na ETAPA 4.

#### Prova Social (Proof Stacking)

Aplicar os frameworks de proof — puxe cada um por nome (rode a `best_query`):
- **Hopkins' Specificity Principle (Reason-Why)** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`)
- **Schwab's Ten Categories of Proof + Five Presentation Principles** (rode `Schwab ten categories of proof taxonomy five principles presenting proof testimonials`) — o menu completo de tipos de prova
- **Sugarman's Satisfaction Conviction** (rode `Sugarman satisfaction conviction objection raising resolution before order form doubt friction`) — levanta e resolve dúvida antes do botão
- **The Sinatra Test + Human-Scale Principle** (rode `Sinatra Test one example so impressive establishes credibility case study` e `Made to Stick human-scale principle statistics as relationships Disneyland 99.9 percent`) — 1 prova devastadora + estatística traduzida pra relação humana
- **Prova em Escada (3 degraus)** (rode `prova em escada funcionou em mim no cetico mais proximo espalhou numero quebrado`) — a ordem de montagem do stack: funcionou em mim → funcionou no cético mais próximo → espalhou-se, fechando com número quebrado
- **Length-Implies-Strength Heuristic** (rode `length implies strength heuristic volume persuasion cue 101 testimonials 22 reasons`) — volume de prova vira sinal de força

- **Social proof volume**: número de clientes, reviews, anos no mercado
- **Specific testimonials**: 3-5 testimonials com NOMES COMPLETOS, FOTOS, e RESULTADOS ESPECÍFICOS (com datas e números quando possível)

  Se o membro não tem testimonials reais ainda (lançamento novo):
  - Use `{{TESTIMONIAL_PLACEHOLDER_1}}` no copy e liste no final:
    "### Testimonials needed: [frase_motora, resultado_especifico, perfil_demografico] × 3"
  - NÃO gere testimonials fictícios com nomes aleatórios.
  - Proof stack fica com placeholder até membro coletar via email / WhatsApp com clientes existentes.
- **Authority proof**: menções em mídia, certificações, endorsement de experts
- **Before/After** (se visual e o produto permite): imagens com legendas
- **Science/ingredient research**: evidência técnica se apropriado

Organize em formato visual navegável (tiles, carrossel, grid).

#### Oferta / Stack Com Ancoragem

Do `offer-builder/offer-builder.md`:
- Produto com nome
- Bundles (Solo / Popular 3-pack / Best Value 6-pack) com savings visíveis
- Bump (produto complementar baixo ticket)
- Stack de valor: "Você recebe [X + Y + Z] no valor de $[total ancorado]. Hoje: $[preço]"
- Savings visíveis ("Você economiza $[diff] hoje")

**Bônus/GWP respeitam `bonuses[].condition` do `offer-builder/dados.json`** (extraído no pré-flight) — a copy do stack DEVE refletir a condição configurada:
- `cart_threshold` → a copy diz a condição explícita ("FREE [bonus] on orders over $X") — NUNCA prometa incondicional um brinde que só destrava por subtotal
- `unconditional` → sem condição na copy (todo comprador recebe)
- `tier_specific` → o brinde aparece SÓ no tier que o destrava (3-pack/6-pack), não no stack geral

A `condition` que a copy descreve é exatamente a que a Skill `bonus-delivery` configura na loja — escreva a copy a partir do campo, não de memória.

Aplique **pricing psychology** — puxe os sistemas por nome (rode cada `best_query`):
- **Anchoring & Adjustment + Contrast Principle** (rode `anchoring adjustment Tversky Kahneman SSN auction real estate listing reference price Poundstone`) — o valor ancorado do stack
- **Decoy Effect (Asymmetric Dominance)** (rode `decoy effect asymmetric dominance Economist Ariely pricing tiers print-only combo`) — o 3-pack Popular como decoy
- **Extremeness Aversion + Three-Tier Pricing** (rode `extremeness aversion three tier pricing middle option beer experiment Simonson Tversky`) — por que a opção do meio ganha
- **Charm Pricing (9-Endings) & Transaction Utility** (rode `charm pricing nine endings left digit transaction utility was price deal Poundstone Thaler`) — framing de "savings" e was-price
- **Os 4 tipos de Reason-Why** (rode `quatro tipos de reason-why preco existencia generosidade mecanismo razao operacional`) — razão OPERACIONAL pra preço/escassez, razão MORAL pra generosidade/garantia; trocar uma pela outra inverte o efeito (também governa a razão real da seção Urgency/Scarcity abaixo)
