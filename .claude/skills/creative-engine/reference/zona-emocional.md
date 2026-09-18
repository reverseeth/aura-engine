# Creative Engine · Referência: Zona emocional: Valence × Intensity e as 4 Hook Emotions (ETAPA 4.5, bloco E)

> As 4 zonas de valência × intensidade, o processo de 4 passos, o arco emocional obrigatório, a régua da zona 4, as 4 Hook Emotions como camada derivada e o hook archetype. Abra na ETAPA 4.5 e sempre que uma etapa citar zona emocional.

**E. Valence × Intensity — a zona emocional do criativo (camada primária) + as 4 Hook Emotions (camada inferior)**

A variável escondida do criativo não é o que você diz, é **como o leitor se sente ao ler**. O framework tem dois eixos: **valência** (a emoção é positiva ou negativa) × **intensidade** (quão forte ela é). Cruzando os dois saem 4 zonas, e todo conceito (e todo hook) declara em qual entra.

| Zona | Valência | Intensidade | Como soa | Para quem funciona |
|---|---|---|---|---|
| **1 — Acolhimento** | positiva | baixa | suporte, calma, "vai ficar tudo bem" | avatares emocionalmente derrotados (já tentaram tudo e nada funcionou) |
| **2 — Entusiasmo** | positiva | alta | alegria, thrill, identidade, pertencimento | avatares apaixonados por uma causa/comunidade/identidade |
| **3 — Incômodo** | negativa | baixa | irritação, chateação cotidiana, o pequeno atrito diário | avatar que convive com o problema sem tratá-lo como urgente |
| **4 — Alerta** | negativa | alta | medo, perigo, risco de dano | é onde muitos anunciantes fazem muito dinheiro — e onde o guardrail ético abaixo é obrigatório |

**O mesmo conteúdo em zonas opostas:** *"watch out for these ingredients when buying shampoo"* (zona negativa) vs *"the best ingredients for healthier hair"* (zona positiva). Mesma informação, sentimento diferente, performance diferente.

**A zona certa é função do estado emocional do avatar, não do produto.** Por isso a persona vem do `sub_avatars[]` da Skill `market-research` ANTES da escolha de zona (contrato no "Contexto a carregar", item 2b) — é a pesquisa que diz se aquele avatar está derrotado (zona 1) ou irritado (zona 3).

**Processo de 4 passos (é como o framework vira decisão de batch):**

1. **Identificar a zona dos winners atuais.** Se existe `ad-analysis/dados.json` com resultado, classifique os hooks vencedores nas 4 zonas (comece pelos hooks; depois headlines de LP/advertorial). Sem histórico, pule para o passo 2 com a zona derivada do estado emocional do sub-avatar.
2. **Criar mais ads na zona vencedora** — regra operacional: **pelo menos 1 das 3 variações de cada conceito** fica na zona que já venceu. Isso não fere as hard rules: a zona é propriedade do **hook**, e hook/abertura é exatamente o que as 3 execuções podem variar (em `sniper`) ou já variam (em `marksman`). O campo `valence`/`intensity` no nível do conceito registra a zona de abertura **dominante**; cada hook carrega a sua.
3. **Testar o mesmo ângulo em outras zonas** — algumas zonas dão mais escala que outras para o mesmo ângulo. Quando um ângulo vence, cabe um conceito dedicado de "teste de valência e intensidade": os 3 criativos do pack cobrem os **3 quadrantes que o ângulo ainda não ocupou**, 1 por quadrante (o quadrante vencedor já tem o criativo original), mantendo a régua de 3 criativos por ad set da skill `ad-strategy`.
4. **Reviver winners antigos** reescrevendo-os na zona que funciona hoje (entra como ideia de batch, não como criativo novo do zero).

**O valor diagnóstico (é por isso que o framework entra):** ele explica os flops inexplicáveis. Muitas "iterações melhores" que fracassaram na verdade **mudaram de zona emocional sem que ninguém percebesse** — trocaram a palavra, trocaram junto o sentimento, e o ad deixou de falar com o mesmo estado emocional. Declarar `valence` e `intensity` isola essa variável e transforma "não sei por que essa iteração morreu" em resposta.

**ARCO EMOCIONAL — OBRIGATÓRIO (o ad NÃO fica na mesma zona do começo ao fim)**

Em direct response o ad **abre em valência baixa e fecha em valência alta**. A regra em uma frase: **ninguém compra com medo.**

- **Hook** — o caso comum abre em valência baixa (zona 4 alerta, ou zona 3 incômodo), porque a emoção negativa é o que abre atenção. Abertura em zona 1 (acolhimento, para avatar derrotado) ou zona 2 (identidade) é legítima quando a pesquisa aponta esse estado emocional — o que é inegociável é o **fecho**, não a abertura.
- **Bridge / início do Hold** — segura na zona de abertura, aprofunda o custo do problema.
- **Hold → CTA** — resolve para segurança e confiança. A emoção positiva é o que fecha a venda. **Este passo é obrigatório em todo conceito.**
- **Sem saltos bruscos:** pânico → "let's go" não cola. Pânico → reasseguramento cola. A ponte entre as duas zonas é o trabalho de copy.
- **Única exceção:** image ad de curiosidade que manda para advertorial/listicle — aí quem faz a subida de valência é a página, não o ad. Nesse caso declare `valence_arc_owner: "landing_page"`.

Declare o arco no `dados.json` (`valence_open` → `valence_close`) e na linha "Estrutura Invisível / emocional" do briefing. **Conceito que abre e fecha na mesma zona baixa está incompleto** — volte e escreva a resolução antes de entregar.

**Régua da zona 4 (craft, não freio):**

- **Intensidade com lastro escala mais.** O medo mais forte é o que o avatar já sente: tire a consequência das frases literais de review e do banco de provas da `offer-builder` (números, estudos) — história real de cliente é a fonte de intensidade que mais converte.
- **A linha:** se o medo faz a pessoa **parar** de ler/assistir, você cruzou. O objetivo é fazer checar se está tudo bem, não paralisar.

**As 4 Hook Emotions (camada inferior — continua obrigatória por hook):**

Dentro da zona escolhida, todo criativo e todo hook do Hooks Bank ainda declara qual das 4 domina:

- **Curiosity** — pattern interrupt, mistério, pergunta incompleta, "o que poucos sabem"
- **Urgency** — tempo escasso, janela limitada, risco de perder
- **Fear** — dor amplificada, consequência negativa, "se você não fizer X"
- **Delight** — desejo/transformação, imagem de futuro melhor, prazer antecipado

NÃO permitir hook sem emoção dominante atribuída. Se o hook não encaixa em nenhuma das 4, ele é fraco — reescrever.

**Como as duas camadas se encaixam (mapa de derivação — `emotion_dominant` vira campo DERIVADO de `valence` × `intensity`):**

| `emotion_dominant` | `valence` | `intensity` | Observação |
|---|---|---|---|
| `fear` | `negative` | `high` | zona 4 |
| `urgency` | `negative` | `high` | é contexto (tempo), não emoção — a zona vem do conteúdo |
| `delight` | `positive` | `high` ou `low` | zona 2 quando é thrill/identidade; zona 1 quando é acolhimento |
| `curiosity` | herda a zona do conteúdo | herda | curiosidade é **técnica** (open loop), não emoção — pode operar em qualquer quadrante |

Preencha os três campos (`valence`, `intensity`, `emotion_dominant`). Quando a derivação for ambígua (curiosity, delight), a zona declarada em `valence`/`intensity` prevalece — `emotion_dominant` existe para não quebrar o gate H4 da Skill `consistency-audit` e o registry `creative-dna`.

Junto da emoção, declarar também o **hook archetype** (id de `.claude/lib/hook-taxonomy/archetypes.json` — 17 arquétipos organizados pelas 4 emoções, ex: `pattern_interrupt`, `secret_reveal`, `transformation`). O archetype declarado aqui entra no contexto da extração de DNA (ETAPA 7.6) — é o que permite ao dna-profile revelar QUAL arquétipo de hook ganha no seu nicho quando a Skill `ad-analysis` marca winners.
