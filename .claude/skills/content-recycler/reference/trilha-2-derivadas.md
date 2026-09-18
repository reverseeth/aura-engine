# Content Recycler · Referência: Trilha 2, as nove derivadas de canal próprio

> O enquadramento honesto das derivadas como jogada de marca e LTV, o fluxo a partir da etapa 3 da lib e a curadoria de sistemas por formato, com as queries exatas, mais a geração, a passada de estilo e o índice. Abra quando o membro pedir a Trilha 2.

## Trilha 2 — Derivadas de formato (9 canais, sob pedido)

As 9 derivadas continuam inteiras e continuam valendo — mas com o enquadramento honesto: são jogada de **marca, canal próprio e LTV**. Elas não escalam a conta; quem escala é a Trilha 1. Rode quando o membro pedir explicitamente (ou quando ele aceitar a oferta no fecho da Trilha 1). Um criativo `spend_winner` não entra aqui.

Siga o fluxo do `.claude/lib/content-recycler/recycler.md` a partir da ETAPA 3 — a essência já foi extraída na ETAPA 1 acima:

3. **Consultar base Aura por formato** — para CADA uma das 9 derivadas, puxe os SISTEMAS NOMEADOS do domínio (não query genérica; `deep=true`). Curadoria de maior impacto por formato:
   - **Advertorial / Blog SEO** → **Caples' Four U's Hierarchy** (rode `Caples four U's hierarchy unique useful urgent ultra-specific headlines`) + **Hopkins' Specificity Rule** (rode `Hopkins specificity rule 1-2 second rule vague vs specific claims`) + **Objection → Claim → Proof → Benefit cycle (the Hold)** (rode `objection claim proof benefit cycle hold section one cycle`) — headlines específicas e ciclos de prova pra long-form.
   - **Organic TikTok / YouTube pre-roll** → **Gap Theory of Curiosity** (rode `gap theory of curiosity hooks counterintuitive open loop slippery slope`) + **Slippery Slope Principle** (rode `slippery slope principle open loops pattern interrupt end with intrigue video script`) + **4-Section Video Ad Structure (Hook / Bridge / Hold / CTA)** (rode `video ad script 4 section structure hook bridge hold CTA timing 30-45 seconds`) + **Strategic Pacing** (rode `strategic pacing rapid cuts hook bridge solution CTA video editing rhythm`) — reembala o breakthrough em estrutura de vídeo orgânico com ritmo de corte por seção.
   - **Pinterest carousel / package insert (estáticos)** → **Static/Image Archetypes by Funnel Position** (rode `static image archetypes funnel position plain reminder direct response complexity rule`) + **13+ Winning Static Ad Templates** (rode `13 winning static ad templates avatar callout nutella meme breakdown why it works`) — escolhe arquétipo estático certo pra cada slide.
   - **Email sequence / SMS / Podcast ad** → **The Big 4 Emotions** (rode `Big 4 Emotions NEW ONLY EASY ANYBODY SAFE PREDICTABLE BIG FAST`) + **Brunson's Five Curiosity Hooks** (rode `Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles`) — reframes de curiosidade pra subject lines / aberturas de SMS / leitura de podcast quando o ângulo do breakthrough já saturou no feed.
   - **Transversal a TODAS as 9** → **Congruency — The Multiplier** (rode `congruency multiplier ad landing page offer visual message emotional continuity`) — cada derivada mantém continuidade de mensagem/promessa com o criativo fonte e com `offer-builder/dados.json` (sem deriva de mecanismo). O `psychological_mechanism` do `essence.json` é o teste: se a derivada não aciona o mesmo mecanismo, ela virou outro conceito.
   - Demais frameworks do domínio (Hormozi Callout System, What-Who-When Matrix, SUCCESs, New Opportunity vs Improvement, etc.) ficam disponíveis em `.claude/lib/kb-index/` pra puxar sob demanda quando o formato pedir.

4. **Gerar 9 derivadas** em paralelo (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad)
5. **Passada de estilo em cada** — travessão zero em headlines/subject lines, ≤2 no corpo (rule 8a); nenhuma derivada com aviso, disclaimer ou claim suavizado por conta própria (rule 8b)
6. **Gerar README.md** consolidado
