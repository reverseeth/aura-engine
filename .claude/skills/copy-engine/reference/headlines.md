# Copy Engine · Referência: Headlines, o processo de 100 linhas condensado (ETAPA 3)

> Os sistemas de headline com a `best_query` de cada um, a geração de 20 a 30 variações por tipo com VOC literal, labels como call-out e o gate de vocabulário já na geração (3A), a categorização e o top 5 justificado (3B) e as 3 hipóteses diferentes para teste A/B (3C). Abra na ETAPA 3.

### ETAPA 3 — Headlines (Processo de 100 Linhas, versão condensada)

> O processo canônico gera 100 linhas; aqui rodamos a versão condensada (20-30 variações) que preserva as fases do framework (gerar em volume sem julgar → categorizar → top 5 → 3 hipóteses A/B) sem estourar contexto. As primeiras variações "ruins" continuam fazendo parte do método — elas destravam as boas.

Puxe os SISTEMAS de headline da base antes de gerar (rode cada `best_query` — não query genérica tipo "headlines"):
- **100-Headline Exercise (Process)** (rode `100 headlines exercise process first 20 suck VOC immersion prereqs`) — o processo que governa esta ETAPA inteira
- **Caples' 35 Proven Headline Formulas + Three Classes** (rode `Caples headline formulas three classes self-interest news curiosity techniques`)
- **Caples' Six First-Paragraph Formulas** (rode `Caples six first-paragraph formulas interrupting idea shocker news preview quotation story`)
- **Schwartz's 38 Verbalization Techniques** (rode `Schwartz 38 verbalization techniques Breakthrough Advertising strengthening claim`) — pra fortalecer cada claim na headline
- **Bencivenga's I = B + C Formula** + **Shake-Me-Awake-at-3AM Test** (rode `Bencivenga I=B+C formula interest benefit curiosity headline evaluation` e `Bencivenga shake me awake at 3am test headline strength`) — pra avaliar força de cada variação
- **Four U's (Unique, Useful, Urgent, Ultra-specific)** (rode `Four U's unique useful urgent ultra-specific hook headline hierarchy`) — grade rápido das top variações
- **Hormozi's Seven Headline Components** (rode `Hormozi seven headline components callout value timeframe proof mechanism obstacle urgency $100M Leads`) — pra ofertas/Product-Most Aware
- **Hopkins: Headlines as Audience Selectors + Specificity** (rode `Hopkins headlines audience selectors preemptive claim specificity Scientific Advertising`) — specificity converte 2-3x sobre generalidade
- **Sticky Hook — 3 must-haves** (rode `sticky hook emotion curiosity gap high stakes targeted vs broad ad`) — emoção + curiosity gap + stakes altos: o critério mínimo que toda headline/hook precisa cumprir
- **Promise vs Open Loop** (rode `make a promise vs open a loop juxtaposition fear do the opposite Harry Dry`) — a decisão binária de cada variação: PROMETER ou ABRIR LOOP (e as 3 formas de abrir o loop)
- **Labels + Word Swapping** (rode `labels callout de identidade word swapping linguagem do cliente urban dictionary`) — `labels[]` da `market-research` como call-out de identidade; troque a palavra da marca/indústria pela palavra que o cliente usa
- **Headline Sweep (8-Part Laddering Edit)** (rode `headline sweep eight parts captures attention avoids confusion matches message button SEO`) — pra refinar as top 5 na sub-etapa 3B

Aplique os princípios do processo de 100 linhas (Caples, expandido) e as fórmulas clássicas acima.

**3A — Geração (20-30 variações):**

Gere 20-30 variações de headline aplicando as fórmulas. Cobrir diferentes tipos:

- **Benefício direto**: "Get [outcome] without [pain]"
- **Curiosidade**: "The [adjective] secret [audience] don't know about [topic]"
- **Problema**: "If you [problem], you're not alone — but there's a reason"
- **Resultado com especificidade**: "[Specific number] [specific outcome] in [specific time]"
- **Mecanismo único**: "Introducing the [mechanism name] — [what it does]"
- **Contrarian/controversy**: "Why [common belief] is actually making [problem] worse"
- **Question hook**: "What if [familiar problem] wasn't your fault?"
- **Testimonial hook**: "[Specific person] lost [specific number] in [time] — here's how"
- **Authority**: "[Expert title] reveals the [claim]"
- **Fear of loss**: "The [thing you're missing] that [outcome]"

Use linguagem EXATA do VOC do market research sempre que possível. Hopkins: "specificity in headlines converts 2-3x over generality". Pro call-out (componente #1 do Hormozi), use os `labels[]` da `market-research` — o apelido com que o mercado se nomeia é o call-out mais forte que existe. E consulte `market_vocabulary` JÁ NA GERAÇÃO: termo com `saturated_in_market: true` não entra em headline (mensagem fatigada — só como prova no corpo); termo de `words_absent[]` não entra em lugar nenhum (use o `market_says_instead`).

**3B — Categorização + Top 5:**

Categorize as 20-30 por tipo. Selecione **top 5** com justificativa explícita por que cada uma funciona pro awareness level + ângulo + tom + Big Idea.

**3C — 3 pra Teste A/B:**

Das top 5, escolha 3 que representam HIPÓTESES DIFERENTES (não variações cosméticas):
- Headline 1: hipótese de ângulo dominante
- Headline 2: hipótese alternativa (ângulo secundário)
- Headline 3: hipótese de formato diferente (ex: pergunta vs afirmação)

Justifique cada escolha.
