# Offer Builder · Referência: Mecanismo único (ETAPA 2)

> Os sistemas nomeados da base pra ideação de mecanismo, as duas rotas da 2A (recombinação validada como default e criação original), as regras transversais, o filtro S.I.N., a avaliação rigorosa da 2B, a recomendação da 2C e a documentação da lógica de UMP e UMS sem escrever copy (2D). Abra na ETAPA 2.

### ETAPA 2 — MECANISMO ÚNICO (A Parte Mais Importante)

O mecanismo único é o que diferencia seu produto de TODO concorrente. Sem mecanismo forte, a copy vira commodity disputando no preço. Com mecanismo forte, você cria um espaço sem concorrência direta (blue ocean) dentro de qualquer nicho.

**Puxe estes SISTEMAS NOMEADOS da base antes de ideação (rode a `best_query` de cada — NUNCA query genérica):**
- **Unique Mechanism Theory (UMP/UMS — UMP é o mecanismo do problema, UMS é o mecanismo da solução)** (rode `unique mechanism UMP UMS theory two-part problem solution`) — o framework-mãe: mecanismo do problema + mecanismo da solução.
- **UMP/UMS Internal Structure** (rode `UMP UMS structure trigger surprising cause quiz specific delivery`) — anatomia interna do mecanismo (trigger → causa surpreendente → delivery específico).
- **S.I.N. Filter (Simple, Intuitive, New)** (rode `mechanism SIN filter simple intuitive new`) — o filtro aplicado em 2A/2B abaixo.
- **Os 3 tipos de mecanismos (New / Unspoken / Renamed)** (rode `tres tipos de mecanismo new unspoken renamed its toasted bone broth ordem de busca`) — os três tipos (novo, não dito e renomeado) com a ordem de busca entre eles: antes de fabricar mecanismo novo, cheque se o produto já tem um mecanismo não dito ("it's toasted") ou renomeável (bone broth).
- **Fabricação de Mecanismo — receita de 4 passos + pipeline de 9 passos** (rode `fabricar mecanismo composto real indisponivel vilao decompor em constituintes protocolo numerado`) — o caminho da commodity ao new mechanism: partir de um composto real e indisponível, definir o vilão, decompor em constituintes e virar protocolo numerado. Alimenta a Rota B (criação original) da 2A.
- **Proprietary Mechanism Naming (Gum Name)** (rode `proprietary mechanism gum name nickname ritual hack effect`) — como cunhar o nome proprietário (2-4 palavras).
- **The Big 3: New Mechanism / New Information / New Identity** (rode `new mechanism new information new identity big 3 sophisticated market`) — qual eixo usar conforme sophistication.
- **Market Sophistication (5 Stages)** (rode `market sophistication 5 stages Schwartz new mechanism identification`) — determina QUE tipo de mecanismo o mercado ainda aceita.
- **Reeves USP (3 Requirements + 3 Roads)** (rode `Reeves USP three requirements three roads preemptive claim`) — garante que o mecanismo vira proposição única defensável.
- **Hopkins Reason-Why Rule** (rode `Hopkins reason why rule every claim needs a reason`) — todo claim do mecanismo precisa de um porquê concreto.

Frameworks adjacentes de mecanismo (Big Domino, Three False Beliefs, Schwartz Mechanization, Big Idea, Sugarman Concept Selling, Hormozi MAGIC Naming) estão no índice `.claude/lib/kb-index/` — puxe conforme o vertical exigir.

**2A — Ideação (Gerar 5-7 Opções por DUAS rotas):**

Inputs (pras duas rotas):
- Features/ingredientes do produto
- Root cause research da Skill `market-research` (causa-raiz proprietária)
- `competitor-analysis/dados.json` → `validated_library` (mecanismos + ângulos com evidência de veiculação/escala) e `claims_saturation`
- `competitor-analysis/creative-patterns.json` (se existir) → `recurring_claims` com `market_validated: true`
- Awareness level do mercado (Schwartz) e sophistication stage (determina que tipo de mecanismo funciona)

**Rota A — Recombinação validada (DEFAULT).** Criar mecanismo do zero é mais caro e arriscado do que recombinar o que o mercado já validou com dinheiro alheio — a validação de mercado é o ativo. Gere a maioria dos candidatos por aqui:

- **A1 — Aprimorar mecanismo validado (mantendo o ângulo):** pegue um mecanismo da `validated_library` com evidência de escala e construa a versão 2: mais específica, mais crível, com um elemento novo (ingrediente, número, etapa do processo) — subindo **+1 no estágio de sofisticação** (Schwartz: quando o mercado já aceitou um mecanismo, a versão ampliada/melhorada dele é o que vence o controle). O nome proprietário é SEMPRE nosso — aprimorar ≠ clonar. `validation_source: "improved_validated"`.
- **A2 — Cruzar mecanismo validado × ângulo validado de OUTRA marca/vertical adjacente:** combinação única, porém pré-validada nas duas pontas (ex: mecanismo de gut health cruzado com ângulo de skincare via ligação intestino-pele). Use `validated_library.mechanisms` de um lado e `validated_library.angles` (ou ângulo escalado de vertical adjacente) do outro. `validation_source: "crossed_validated"`.

**Rota B — Criação original (complementar).** O fluxo clássico: features + root cause + gaps de mecanismo da `competitor-analysis`. Use quando a `validated_library` não tem NENHUM mecanismo com evidência real de escala (dias rodando, nº de criativos no mesmo ângulo — o critério é a qualidade da evidência, não a contagem: 2 mecanismos bem evidenciados sustentam a Rota A), ou quando o mercado está em **estágio 5** de sofisticação (pede identidade nova, não mecanismo recombinado). `validation_source: "original"`.

**Regras transversais (valem pras duas rotas):**
- EVITAR mecanismos/claims com saturação ALTA na matriz Claims Saturation da `competitor-analysis` (o público não acredita mais)
- PREEMPTAR claim comum sem dono (Preemptive Claim — claim que vários usam mas ninguém CRAVOU como seu). Fontes: `claims_saturation` dá os candidatos com `count > 0` (claim/count/total/saturation — o campo NÃO diz quem é dono); **quem já "possui" cada claim vem da narrativa do `competitor-analysis/competitor-analysis.md`** (a análise por concorrente mostra quem cravou o quê). Claim frequente no JSON + sem dono no relatório = candidato a preempção.
- Registrar em CADA candidato o `validation_source` (de onde veio a validação: qual mecanismo/ângulo, de qual concorrente, com que evidência)

Gere 5-7 opções de mecanismo único no total (mix das rotas — se a validated_library sustentar, 4-5 da Rota A + 1-2 da Rota B). Cada um com:

- **Nome proprietário** (2-4 palavras, memorável, proprietário-soando, pronunciável)
- **Explicação simples** (2-3 frases — como funciona na prática)
- **Base real do produto** (ingrediente, feature, processo, combinação — NÃO inventar ciência falsa)
- **Por que é diferente dos concorrentes** (qual claim rompe, qual gap preenche)
- **Em qual nível de awareness funciona melhor**
- **Match com sophistication stage** (ingredient-based pra Estágio 3, information-based pra Estágio 4, identification pra Estágio 5)
- **validation_source** (improved_validated / crossed_validated / original) + o que valida (qual mecanismo/ângulo de qual concorrente, com que evidência da validated_library)

**Aplicar o filtro S.I.N. (Simple / Intuitive / New):**
- **Simple** (fácil de entender de primeira, sem jargão — "Joint Drought Protocol" comunica na hora, não exige explicação técnica)
- **Intuitive** (faz sentido imediato pro avatar, a lógica "clica" sozinha — "Lipid Barrier Breach" sugere causa e solução sem precisar de aula)
- **New** (soa novo pro mercado, mesmo que a ciência subjacente seja antiga — reformulação criativa de algo conhecido)

Nomes pode vir de:
- Renomear ingredientes/componentes existentes pra novo propósito (ex: num suplemento: "Bioavailable Matrix" em vez de "complexo"; num wearable: "Adaptive Core Module" em vez de "sensor")
- Combinar 2-3 features em conceito unificado (ex: "Triple Action Stack", "Dual Channel System")
- Nomear um processo interno (ex: "48-Hour Activation Protocol", "7-Day Reset Method")
- Reposicionar uma feature secundária como central (ex: transformar feature "com antioxidantes" em "Free Radical Neutralization System"; feature "bateria de 72h" em "Perpetual Charge Architecture")

**2B — Avaliação Rigorosa:**

Pra CADA opção de mecanismo, score 1-10 em:

| Dimensão | O que avaliar |
|---|---|
| **Diferenciação** (1-10) | Quão diferente dos claims dos concorrentes? |
| **Credibilidade** (1-10) | A ciência/lógica por trás é defensável? Fake = 1, baseado em research real = 10 |
| **Memorabilidade** (1-10) | O nome "gruda"? É fácil de repetir? |
| **Expandibilidade** (1-10) | Dá pra expandir em 2-3 parágrafos pra copy sem soar repetitivo? |
| **Match com awareness** (1-10) | Funciona pro nível de awareness dominante do TAM? |

Score final = soma / 5.

**2C — Recomendação:**

Recomende o mecanismo com maior score total, com justificativa explícita por que esse vence os outros. Registre o `validation_source` do vencedor em `dados.json` → `mechanism.validation_source`.

**2D — Documentar a LÓGICA do Mecanismo (sem escrever copy):**

A oferta define a estratégia do mecanismo; a copy nasce na Skill `copy-engine`. **NUNCA escreva versões prontas de copy do mecanismo aqui (headline, parágrafo de PDP, expansão de advertorial)** — copy pré-escrita na oferta enviesa a Skill `copy-engine`, que deve reler todo o research e decidir os ângulos sozinha. Documente, no report_language:

- **UMP (o problema):** nome próprio + a lógica de por que as soluções atuais falham, com os números e estudos do banco de provas (ETAPA 2.5) quando houver.
- **UMS (a solução):** nome próprio + a lógica de por que a nossa entrega funciona, com os números e estudos do banco de provas quando houver.
- **Externalização de culpa:** de quem/do que é a culpa pela falha das soluções anteriores (nunca do avatar).

É essa lógica (nomes + causa + prova) que a Skill `copy-engine` expande em copy nas versões que ELA decidir (headline, parágrafo, expansão longa) conforme awareness e formato de página.
