# Creative Engine · Referência: Ideação nas 3 verticais e seleção dos conceitos (ETAPAs 3 e 4)

> Os sistemas de ideação da base (com a `best_query` exata de cada um), o uso dos sinais da `competitor-analysis`, as três verticais em detalhe e os critérios de seleção e o formato de apresentação ao membro. Abra na ETAPA 3.

### ETAPA 3 — Gerar Ângulos (3 Verticais da Vault)

**Puxe os SISTEMAS NOMEADOS de ideação de ângulo da base (rode a `best_query` exata de cada um — NUNCA query genérica):**

- **Ad Angles Framework — extract actionable angles from sub-avatars** (rode `Ad Angles how to create actionable angles from sub avatars desire behavior gap 3 hooks`) — é o motor das 3 verticais: desire → behavior gap → 3 hooks por sub-avatar.
- **Hormozi What-Who-When Angle Multiplication Matrix** (rode `Hormozi what who when angle multiplication matrix 8 value elements status perspectives timeline`) — multiplica cada ângulo por status/perspectiva/timeline pra explodir o leque sem repetir.
- **Hormozi Callout System — 4 Verbal + 3 Nonverbal Callouts** (rode `Hormozi four verbal callout types labels yes-questions if-then ridiculous results` e `Hormozi three nonverbal callout types contrast likeness scene visual`) — como o ângulo "chama" o avatar certo no primeiro beat.
- **Brunson's Five Curiosity Hooks** (rode `Brunson five curiosity hooks controversial bold prediction conspiracy reframe angles`) — usar quando os ângulos óbvios já estão saturados pelos concorrentes (reframe).
- **New Opportunity vs Improvement Offer (in creative)** (rode `new opportunity vs improvement offer opportunity switch stack new way better way`) — decide se o ângulo posiciona como nova oportunidade (switch) ou melhoria.
- **Categorization = Death / Own a New Category** (rode `categorization death own a new category new hope never compare Ozempic Theragun`) — evita ângulo que ancora o produto na categoria do concorrente.
- **Storytelling as the Hardest-to-Replicate Angle (founder story)** (rode `storytelling hardest to replicate angle founder story defensible creative`) — ângulo defensável pra Vertical 3 (interna).

Índice completo dos sistemas de ideação em `.claude/lib/kb-index/`.

Se `competitor-analysis/creative-patterns.json` foi lido no pré-flight, use os sinais dos concorrentes pra calibrar a ideação: `hook_archetypes` (arquétipos de hook já testados no nicho — não reinventar, mas variar), `recurring_claims` (ler os DOIS sinais de cada claim: `usage: "anchor_headline"` = claim validado em ads E não saturado nas PDPs — pode ANCORAR criativos nele, é o que está convertendo no mercado; `usage: "proof_only"` = claim que também está saturado nas PDPs (`also_saturated_pdp: true`) — usar SÓ como prova/base do argumento no body, nunca como headline, porque headline saturada morre no feed) e `format_distribution` (formatos dominantes — se todos usam vídeo demo, considerar um formato sub-explorado). Se o `competitor-analysis/dados.json` trouxe `validated_library` (mecanismos + ângulos com evidência de veiculação/escala) e `top_creatives`, priorize na Vertical 1 os ângulos com validação real de mercado — combinação de ângulo validado + execução nova bate ângulo inventado do zero.

**Fonte opcional de inspiração — TikTok Creative Center (grátis):** o Top Ads Dashboard (`https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en`) lista os ads de melhor performance por região/indústria/objetivo, com métricas de engajamento e tempo de veiculação — o que o PRÓPRIO TikTok diz que performa no nicho. Não busca por marca (não é spy tool); serve pra calibrar padrões de hook/formato vencedores antes de gerar ângulos. A página é renderizada por JavaScript: use `python3 .claude/lib/web-fetch/fetch.py "<url>" --mode text` (cascade da rule resilient-fetch). Índice denso só em US/UK/AU/DE/FR; categorias vazias por política são normais. Opcional — pular não bloqueia a ideação.

Gere ângulos em 3 verticais. **Formato obrigatório de saída em qualquer vertical:** cada ângulo é uma **frase completa que dá uma razão de compra** (gate da ETAPA 4.5.A.0.3) — nunca uma palavra, um rótulo de formato ou um valor do enum `concept_type`. E antes de escrever qualquer frase, passe o vocabulário pelo filtro da Skill `market-research`: termo em `market_vocabulary.words_absent[]` é proibido; termo com `saturated_in_market: true` só entra como prova no corpo, nunca no ângulo nem na headline.

**Vertical 1 — Competitiva:**
O que os concorrentes NÃO estão dizendo que você pode dizer (gaps do competitor analysis + `recurring_claims`/`format_distribution` de `competitor-analysis/creative-patterns.json` se disponível).
- "Ninguém está endereçando a dor [X] — nosso ad atacará direto"
- "Todo mundo usa angle de resultado — nós vamos de angle de causa raiz"
- "Concorrentes fazem autoridade de doctor — nós vamos peer-to-peer UGC"
- "`recurring_claims` com `usage: proof_only` mostra que todos batem em [claim Z] — vamos pelo gap [W] na headline, mantendo [claim Z] como prova no body"

Gere 3-5 ângulos desta vertical.

**Vertical 2 — Consumidor (o gerador é `sub_avatars[]`, não a VOC solta):**

**Comece pelos ângulos que já existem.** Cada item de `market-research/dados.json → sub_avatars[]` traz **um** `angle` pronto, em frase, gerado pela Skill `market-research` a partir daquele recorte. Esses entram na lista **primeiro e literalmente** — não reescreva o que a pesquisa já formulou. Registre a origem (`sub_avatar_id`) junto de cada um.

Para ampliar além do que já veio, use o método de 3 passos sobre o mesmo objeto:

1. Olhe o **`desire`** do sub-avatar (o que ele quer).
2. Olhe o **`behavior`** (ou `experience`) — o que ele **já faz** para tentar conseguir aquilo.
3. Identifique o **gap**: ele faz X e ainda não tem o resultado. **O gap é o ângulo.**

Exemplo: `desire` = "restorative sleep" + `behavior` = "dorme com nose strips" → ângulo **"better than nose strips"** (escrito em frase: "you're still waking up tired even with the strips on"). Um ângulo por sub-avatar; se sobrarem variações do mesmo recorte, faça o merge em um só.

Complementos desta vertical (todos ainda em frase de razão de compra):
- Trigger event como cenário do ad (ex: antes do casamento)
- Objeção quebrada (ex: "já tentei X — aqui está por que este funciona onde aquele parou")
- **`labels[]`** da Skill `market-research` (os apelidos que o mercado usa para si) alimentam o **call-out do primeiro beat**, não o ângulo em si: o label chama quem é, o ângulo diz por que comprar.

Gere 3-5 ângulos.

**Vertical 3 — Interna (Oferta/Mecanismo):**
O que é único do seu produto/oferta:
- "Mecanismo único [nome] — apresentado como revelação/descoberta"
- "Garantia agressiva como angle ('90-day guarantee — you pay nothing if it doesn't work')"
- "Stack de valor como angle ('Tudo isso por $X')"
- "Combinação rara de ingredientes como ângulo técnico"

Gere 3-5 ângulos.

### ETAPA 4 — Selecionar os Top N + Apresentar Pro Membro (Pergunta 2)

Das 9-15 opções de ângulo, selecione os **N conceitos mais fortes** (N vem da Etapa 2). Critérios de seleção:
- Cobrir posições diferentes do funil (TOF + MOF + BOF — não todos no mesmo awareness)
- Cobrir ângulos das 3 verticais (não concentrar em uma só)
- Priorizar ângulos DE GAPS (ninguém faz) sobre ângulos de posição já ocupada
- **Diversidade nas variáveis grandes:** o batch precisa variar entre conceitos as variáveis que ensinam algo (persona, big idea, formato, ângulo — mapa "As Variáveis de um Ad" acima). N conceitos com a mesma persona e o mesmo formato respondem 1 pergunta, não N.
- **Contabilidade de ângulos por método (ETAPA 4.5.A.0.1):** um conceito `sniper` consome **1** ângulo (3 execuções dele); um conceito `marksman` consome **3** ângulos (um por criativo, sob hold universal). Confira que a lista da ETAPA 3 tem ângulos suficientes para os N conceitos escolhidos antes de apresentar.
- **Zona emocional (ETAPA 4.5.E):** se há histórico na `ad-analysis`, pelo menos um conceito do batch abre na zona que já venceu.

Apresente ao membro em formato compacto:

"Esses são os [N] conceitos que recomendo testar:

1. **[Conceito]** — método: **[Marksman / Sniper]** · [se Sniper: o ângulo em frase completa · se Marksman: os 3 ângulos em frase, um por criativo] (persona: [`sub_avatars[].name` + id, ex: "the magnesium tried-it" (sa-01)], vertical: [competitiva/consumidor/interna], posição: [TOF/MOF/BOF], zona emocional de abertura: [1 acolhimento / 2 entusiasmo / 3 incômodo / 4 alerta])
2. ...

Quer ajustar algum antes de eu gerar os briefings completos?"

- Se o membro disser "tá bom" / "segue" / "manda" → vai pra Etapa 5
- Se pedir ajuste → aplique e confirme antes de gerar briefings
