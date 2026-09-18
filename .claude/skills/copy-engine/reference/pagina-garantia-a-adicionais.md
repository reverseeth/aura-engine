# Copy Engine · Referência: Página completa, garantia, FAQ, CTA final, urgência e seções adicionais (ETAPA 4, terceira parte)

> A garantia, a FAQ estratégica que quebra as top 5 objeções com os frameworks de objeção, o CTA final como call to value repetido pela página, a urgência com razão real (nunca escassez inventada) e as seções adicionais, inclusive o bloco de specs objetivas para agentes de compra AI. Abra na ETAPA 4.

#### Garantia

Do `offer-builder/offer-builder.md`, a copy de garantia (2-3 frases, tom confiante, detalhes claros).

Posicione com destaque visual (box, shield icon, destaque colorido).

#### FAQ

Frameworks pra quebrar objeção (rode cada `best_query`):
- **Inoculation Theory (McGuire)** (rode `Inoculation theory McGuire weakened attack vaccination strengthen attitudes competitor argument`) — antecipa e neutraliza a objeção antes que ela cresça
- **Kennedy's Damaging Admission** (rode `Kennedy damaging admission list every reason not to respond admit flaws too good to be true`) — admitir a falha desarma o ceticismo
- **The 'Yeah, Sure' Principle (Proof Matches Claim)** (rode `Bencivenga yeah sure principle proof match claim three reasons why IF THEN construction doctors headache`) — cada resposta de FAQ precisa de prova proporcional ao claim
- **Matriz de objeções (3 tipos × 4 estratégias)** (rode `3 tipos de objecao 4 estrategias facts reversals because reassigning matriz eficacia`) — pra cada objeção da `market-research`, classifique o TIPO e escolha a estratégia (facts / reversals / because / reassigning) que a matriz indica como mais eficaz pra ele

Cada FAQ quebra uma objeção REAL do market research. Pegue as **Top 5 objeções priorizadas** da Skill `market-research` e escreva a resposta que quebra cada uma. Nada de FAQ genérica ("qual o prazo de envio" — isso vai em lugar específico, não é FAQ estratégica).

FAQ estratégica típica:
- "Vai funcionar pra mim se eu já tentei X?" (quebra "já tentei e não deu certo")
- "É seguro pra [condição específica do avatar]?" (quebra medo)
- "E se não funcionar?" (reforça garantia)
- "Por que é diferente do [concorrente comum]?" (quebra comparação)
- "Quando começo a ver resultado?" (quebra time delay)

#### CTA Final

Frameworks pro close (rode cada `best_query`):
- **Pain-to-Hope CTA Transition + CTA Style Matrix** (rode `pain to hope CTA transition style matrix emotional trigger solution-aware avoidance call to value`) — call to VALUE casado com o awareness
- **Closing: Propellants vs Repellants + Temporal Discounting** (rode `propellants repellants temporal discounting close carrot caveman cost of inaction immediate`) — remove repellants, ativa custo da inação
- **Future Pacing** (rode `future pacing copywriting commitment consistency imagine your life with the product better self`) — projeta o membro no resultado antes do clique

Call to VALUE, não call to action. Reforça o outcome + remove fricção:
- "Claim My [Outcome]" (não "Buy Now")
- "Start My [Transformation]"
- "Get [Specific Result] Today"

Repita CTA em 3-5 pontos da página (após hero, após mecanismo, após social proof, após oferta, no final).

#### Urgency/Scarcity

Curta e com razão REAL — urgência inventada (countdown falso, "only 3 left" de mentira) destrói confiança. Ancore num elemento verdadeiro da oferta da `offer-builder`: bônus que expira de verdade, preço de lançamento com data definida, lote/estoque real limitado, GWP por threshold enquanto durar. Escreva 2-4 frases prontas pra usar junto da oferta e no close (esta é a seção canônica `## Urgency/Scarcity` do relatório e o campo `urgency` do dados.json). Se a oferta da `offer-builder` NÃO tem nenhum elemento de urgência real, registre isso no relatório e entregue a página sem urgência fabricada — o custo da inação (Temporal Discounting, já puxado no CTA Final) cobre o empurrão. NÃO invente escassez.

#### Seções Adicionais (se fizer sentido)

- **Comparação com concorrentes** (se Product Aware): tabela "Nosso produto vs [concorrente A] vs [concorrente B]" com dimensões claras (ingrediente, preço, guarantee, mechanism)
- **How it works** (se mechanism exige explicação): 3-step visual (Step 1 → Step 2 → Step 3) com ícones e copy curta
- **Before/After grid** (se visual): 3-4 comparisons
- **Ingredient/feature spotlight** (se ingredient-based mechanism): cada ingrediente com benefit e research
- **Specs objetivas (legíveis por agente de compra AI)** — recomendado em TODA PDP: um bloco curto de especificações concretas e verificáveis (materiais/ingredientes com dosagem exata, dimensões/peso, quantidade por unidade, certificações reais, país de fabricação, modo de uso em passos numerados). Agentes de compra AI (ChatGPT/Perplexity shopping e afins) decidem lendo specs e dados estruturados, não copy sensorial — uma página sem specs objetivas fica invisível pra esse tráfego crescente. Escreva como fatos secos (Hopkins: especificidade sem adjetivos); a skill `agentic-readiness` audita esse bloco depois. Sai na seção `## Specs` do `copy-engine.md` e no array `specs[]` do `dados.json` (rótulo + valor por linha); a `page-design` monta a section `specs` da página a partir dele.
