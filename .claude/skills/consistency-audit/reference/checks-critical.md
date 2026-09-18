# Consistency Audit · Referência: Check battery, bloco CRITICAL (ETAPA 2, checks C1 a C4)

> Os checks que bloqueiam o launch: nome do mecanismo (C1, C1b, C1c), claim forte sem prova ao lado (C2, com os sistemas da base e as queries exatas que calibram o veredito), garantia divergente (C3) e urgência e escassez (C4). Abra na ETAPA 2.

### ETAPA 2 — Check battery (ordenada por severity)

#### CRITICAL (bloqueia launch)

**C1. Mecanismo name consistency**
- `offer-builder/dados.json.mechanism.name` deve aparecer LITERALMENTE em:
  - Pelo menos 1 headline de `copy-engine/copy-engine.md`, E
  - Pelo menos 1 conceito de `creative-engine/dados.json` — vale no hook, no Bridge/Hold do script ou em primary text. Não exija o nome literal no hook de 3s: a doutrina de hook da `creative-engine` é abrir loop (gap theory), não explicar; o mecanismo pode entrar no corpo do ad.
- Ausente em AMBOS os lados (copy E ads) → `severity: critical`, `fix: inject mechanism name in hero + no corpo de pelo menos 1 conceito`
- Presente em só UM dos lados → `severity: high` (drift parcial: o consumidor vê o mecanismo numa fase da jornada e não na outra)

**C1b. Mechanism name normalizado (`offer-builder` ↔ research-foundation)** — só se `research-foundation.json` existir
- `offer-builder/dados.json.mechanism.name` DEVE ser idêntico a `offer-builder/research-foundation.json.mechanism_name` (campo top-level).
- Divergência → `severity: critical`, `check_id: "mechanism-drift"`, `fix: alinhar o nome do mecanismo entre offer e research-foundation antes de propagar pra copy/ads`. (É a fonte da verdade do mecanismo; se essas duas já divergem, todo C1 abaixo herda o drift.)

**C1c. Mechanism name na página (`offer-builder` ↔ 07-plan)**
- `page/page-plan.json.strategy.mechanism_name` DEVE ser idêntico a `offer-builder/dados.json.mechanism.name` — a `page-design` grava esse campo LITERAL exatamente pra este check (ver nota no schema da `page-design`).
- Divergência → `severity: critical` (a página é o artefato de maior visibilidade pro consumidor; mecanismo com nome diferente na página vs ads quebra o message match do funil inteiro), `fix: corrigir o strategy block do page-plan.json e re-gerar a section afetada`.
- `page/page-plan.json` ausente (página ainda não planejada) → check `"skipped"`.

**C2. Claim forte sem prova apresentada ao lado**
- Pra cada claim forte em `copy-engine/copy-engine.md` (hero, mechanism section, proof blocks) e `creative-engine/dados.json` (hooks + primary_texts):
  - Confira se existe PROVA apresentada perto dele — número, estudo do banco de provas (`research-foundation.json.proof_items[]`), depoimento de performance, demo, comparação. Prova pode estar na mesma seção ou na imediatamente seguinte.
  - Claim forte sem prova por perto → `severity: high`; se é a promessa do HERO e não existe prova em lugar nenhum da página → `severity: critical`. `fix: trazer a prova pra perto do claim (número do banco de provas, depoimento com resultado, demo) — nunca suavizar o claim`. O claim fica; o que muda é a prova chegar junto.
- **Julgue a APRESENTAÇÃO da prova, não a força do claim.** Puxe estes sistemas da base pra calibrar o veredito (rode a `best_query` de cada um):
  - **Bencivenga's 'Yeah, Sure' Principle** (rode `Bencivenga yeah sure principle proof must match claims promise outweighs proof doctors headache`) — proof tem que ser proporcional à ousadia do claim; claim grande com proof fraco dispara o reflexo "yeah, sure". É o gate central deste check.
  - **Hopkins' Specificity Principle (Reason-Why)** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`) — claim vago/genérico (sem número, sem mecanismo, sem reason-why) é fraco mesmo "com evidence". Flag claim que é platitude.
  - **Schwab's Ten Categories of Proof** (rode `Schwab ten categories of proof taxonomy five principles presenting proof testimonials`) — classifica o TIPO de proof que a peça usa; se o claim pede proof tipo X (resultado) e a peça só traz tipo Y (autoridade), o fix é trazer o tipo certo pra perto.
  - **Made to Stick — Audience-Testable Credibility + Sinatra Test** (rode `Made to Stick three wellsprings credibility external internal audience-testable Heath` e `Sinatra Test one example so impressive establishes credibility case study`) — se um único caso/demo carrega o claim sozinho, marca como forte; se nem isso existe, agrava o finding.
  - **Puffery (hipérbole)** (rode `puffery hiperbole evitar sustentar claim biggest no-brainer OMG that was easy`) — separa hipérbole reconhecível ("best decision ever"), que não pede prova ao lado, de promessa concreta, que pede; evita finding falso em cima de puffery legítima.
  - **Auditoria de prova — vocabulário de Kyle Milligan + o "Imagery Hack"** (rode `auditoria de prova numere as provas 3 to 6 examples mais fraca no meio fracao vence porcentagem`) — julga a APRESENTAÇÃO do proof que existe: provas numeradas, 3 a 6 exemplos, a mais fraca no meio, fração vencendo porcentagem. Evidence presente mas mal apresentada é finding de fix barato (medium, não critical).
  - **Auditoria de especificidade** (rode `auditoria de especificidade claims especificos 21 a 53% mais criveis timeline do processo`) — régua medida pro julgamento do Hopkins acima: claim específico é 21 a 53% mais crível; claim sem número, timeline ou detalhe de processo perde essa margem mesmo "com evidence".
  - **Os 4 Erros de Conversão que o Critique caça (Kyle Milligan)** (rode `selling from your heels, pinte a imagem antes de oferecer o dinheiro de volta, mostre o resultado não o processo`) — lente de erro de conversão sobre os mesmos claims: vender na defensiva (claim hedged — "may help", "designed to support" — é finding aqui, com fix "afirmar direto"), mostrar o processo em vez do resultado, e oferecer o dinheiro de volta antes de pintar a imagem — este último alimenta também o C3.
  - **Greek Sweep (Ethos / Logos / Pathos)** (rode `greek sweep ethos logos pathos passada de edicao prova e emocao long copy`) — mapeia onde a peça concentra prova vs emoção; trecho todo pathos carregando claim forte sem nenhum logos por perto é exatamente onde este check mais acha gap.
  - **Empty vs Performance Testimonial (Settle) + os 3 formatos de elite** (rode `empty vs performance testimonial criterio de descarte retrato demografico asset nomeado`) — quando o "evidence" do claim é depoimento/review: depoimento vazio ("love it!") não sustenta claim de performance; aplicar o critério de descarte antes de aceitar o match.

**C3. Guarantee copy divergente**
- `offer-builder/dados.json.guarantee.duration_days` vs texto em `copy-engine/copy-engine.md` guarantee section vs `creative-engine/dados.json` primary_texts
- Divergência (30 vs 60 vs 90 dias) → `severity: critical`
- **Não é só duração — julgue também a POSIÇÃO da garantia.** O sistema **Os 4 Erros de Conversão** (mesma puxada do C2 — não repita a busca) marca como erro oferecer o dinheiro de volta ANTES de pintar a imagem do resultado: garantia aparecendo antes do value build na página/copy → `severity: medium` no mesmo `check_id` (a divergência de duração continua `critical`).

**C4. Urgência e escassez coerentes entre ad, página e checkout**
- Puxe **Urgency / Scarcity / FOMO como três alavancas distintas** (rode `urgency scarcity FOMO tres alavancas distintas hot sauce seeds of regret why 500`) — a mesma alavanca de urgência/escassez tem que aparecer com o MESMO número, prazo e "Why?" no ad, na página e no checkout. Ad diz "48h", página diz "this week", checkout não mostra nada → `severity: high`, `fix: alinhar a alavanca nas três superfícies`.
