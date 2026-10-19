# Copy Engine · Referência: Advertorial no formato story curto (ETAPA 5)

> O formato default de advertorial e listicle da Aura (story curto em conversa pergunta e resposta, uma página por problema e por sub-avatar), o espécime de mercado que o sustenta, o encaixe dele nas 7 seções canônicas que a `page-design` lê, os frameworks com a `best_query` de cada um e as regras de escrita. Abra na ETAPA 5 quando a página é advertorial ou listicle.

### ETAPA 5 — Se for ADVERTORIAL (alternativa à ETAPA 4)

**Formato default: story curto, não matéria gigante.** O advertorial da Aura é uma conversa curta com o leitor: uma pergunta, uma resposta, a próxima pergunta. Uma página resolve **um problema só**, pra **um sub-avatar só** (o `angle` da ETAPA 2). Quer falar com outro sub-avatar ou outra dor, escreva outra página: cada ângulo dos criativos ganha a sua. Listicle gigante, cheio de texto, só entra quando as páginas escaladas do 2.5.0 forem de fato listicles longos e com mais ads do que as stories.

**Espécime de mercado (as páginas story da Ryze Superfoods, escaladas no Meta):**
- https://shop.ryzesuperfoods.com/p/mom-71-victor-story
- https://shop.ryzesuperfoods.com/p/energy-crashes-gabriel-story
- https://shop.ryzesuperfoods.com/p/wiping-poop-gabriel-story

A anatomia comum das três:

1. Link "Skip to Special Offer" no topo, que pula pra oferta.
2. Hero: headline em pergunta, com uma palavra em itálico ("Why is one wipe *never* enough?"), duas frases embaixo e a linha de rating ("4.8 stars · 217,799 reviews").
3. A conversa anda em pares: uma pergunta na voz do leitor ("Then what's going on?", "So what helps my gut?", "What would I notice?") seguida de um subtítulo afirmativo e curto ("Ten Wipes In. Still Not Done.").
4. Blocos de 1 a 4 frases, em segunda pessoa, com uma cena concreta do dia do leitor (a parada no meio da estrada, o sofá às duas da tarde).
5. A causa entra em uma frase só, culpando algo fora do leitor.
6. O produto aparece só no meio, como **troca de hábito** ("Trade The Can For Mushroom Coffee", "Switch What You Drink Every Morning"), seguido da lista de ingredientes com ícone e benefício de três palavras.
7. Linha do tempo de Semana 1 a Semana 4, cada semana com uma frase em negrito e uma de corpo; a última semana é o payoff emocional.
8. Cinco depoimentos curtos (uma a três frases), com nome e inicial do sobrenome e "Verified buyer", todos do mesmo sub-avatar da página.
9. Oferta: "40% Off Bundles + Gifts Worth $40", brindes, frete grátis, garantia de 30 dias com a frase de risco zero ("Send the empty bag back") e **um** botão ("Claim Deal").
10. Um personagem ilustrado ou animado como narrador e rosto da página (Victor, 71; Gabriel), que dá identidade ao sub-avatar.

Modele a **estrutura**, nunca o conteúdo, e nunca o recuo deles: as páginas da Ryze suavizam o claim ("Some notice", "Many notice", asterisco em cada semana, rodapé de aviso). A Aura escreve a mesma estrutura com o claim direto e sem asterisco nem rodapé de aviso (regra 8b): "Week 2: The 2 p.m. crash is gone."

**Encaixe nas 7 seções canônicas.** A `page-design` lê o advertorial pelos 7 nomes H2 de `reference/output-schema.md`, então o story ocupa as mesmas seções, cada uma abrindo pela pergunta de transição na voz do leitor:

| Seção canônica | O que entra no story |
|---|---|
| `## Advertorial Headline` | Linha "Skip to Special Offer"; headline em pergunta com uma palavra em itálico, feita com VOC literal do sub-avatar; duas frases (dor + "não é culpa sua"); linha de rating com o número real de reviews (sem reviews ainda, `{{RATING_LINE}}`) |
| `## Lead` | Primeiro par pergunta e resposta: a pergunta que o leitor já se fez ("So what actually worked?") e a resposta curta que mostra que nada do que ele tentou funcionou (as `alternative_solutions` da `competitor-analysis`) |
| `## Background Story` | A cena: 1 a 3 blocos curtos em segunda pessoa (ou na voz do narrador ilustrado), com o momento exato em que a dor aparece no dia, tirados das frases da `market-research` |
| `## Root Cause` | "Then what's going on?" e a causa raiz da `market-research` em uma ou duas frases, com a culpa externalizada |
| `## Mechanism Reveal` | "So what helps [o problema]?" e a troca de hábito com o nome do mecanismo da `offer-builder`, em uma frase de subtítulo e um bloco curto |
| `## Product Build-Up` | Lista de ingredientes ou componentes com ícone e benefício curto; "What would I notice?" e a linha do tempo de 4 semanas; "What do other people say?" e os cinco depoimentos reais do mesmo sub-avatar (sem depoimento real, `{{TESTIMONIAL_PLACEHOLDER_N}}` e a lista do que coletar) |
| `## Reveal + Close` | "Alright, show me the deal", a oferta da `offer-builder` (bundle, desconto, brindes, frete, garantia com a frase de risco zero) e um CTA como call to value ("Claim Deal", "Get My Bundle"). A urgência, só com razão real, é extraída também pra `## Urgency/Scarcity` e pro campo `urgency` do `dados.json` |

O listicle usa o mesmo encaixe: `background-story`, `root-cause`, `mechanism-reveal` e `product-buildup` viram itens numerados no tratamento da `page-design`; a copy é a mesma.

**Narrador.** O personagem da página é um retrato do sub-avatar montado com as frases reais da `market-research` (idade, rotina, a dor dita com as palavras do mercado), apresentado como personagem ilustrado, do jeito que as páginas escaladas fazem. Ele guia a cena; depoimento é outra coisa e é sempre de cliente real.

**Regras de escrita do story:**
- Bloco de 1 a 4 frases. Nenhum parágrafo maior que isso.
- Toda seção abre com a pergunta de transição; o leitor sente que ele está conduzindo.
- Subtítulos em Title Case, curtos, afirmativos, com contraste ("Wired At Five. Quitting At Two.").
- O produto não aparece antes da `## Mechanism Reveal`.
- Um único CTA de compra, no fim, mais o link "Skip to Special Offer" no topo.
- Página inteira entre 400 e 700 palavras. Mais que isso, corte pela dieta do sweep 4.5.

Frameworks que sustentam o formato (rode cada `best_query`):
- **Halbert's Editorial Look / Invisible Selling (5x Readership)** (rode `Halbert editorial look invisible selling 5x readership does not appear to sell advertorial`): a página lê como conversa, não como anúncio
- **Storytelling in Copy (Background / Emotional / Discovery Stories + Story Spine)** (rode `storytelling copy background emotional discovery story spine once upon a time hero journey`): a cena da `## Background Story`
- **Sugarman's Slippery Slide + Seeds of Curiosity** (rode `Sugarman slippery slide every element read the next sentence frictionless`): as perguntas de transição são as sementes de curiosidade que puxam o próximo bloco
- **Schwartz's 'The Turn'** (rode `Schwartz the turn product introduction inevitable transition after lead story`): a passagem da `## Root Cause` pra troca de hábito
- **Cashvertising — 12 Ways to Lure Readers Into Copy** (rode `Cashvertising 12 ways lure readers into copy question authority skepticism story bandwagon short first sentence`): a headline em pergunta e a primeira frase curta

No arquivo final (`copy-engine.md`), as 7 seções entram com os nomes canônicos H2 de `reference/output-schema.md`, exatamente como estão escritos lá.
