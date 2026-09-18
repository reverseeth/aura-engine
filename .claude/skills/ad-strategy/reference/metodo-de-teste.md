# Ad Strategy · Referência: Método de teste, Marksman ou Sniper lido por conceito (sub-etapa 3.2)

> Por que o método se lê e não se decide, a regra por conceito com batch misto, o fallback para batch legado, a tabela Marksman, Sniper e Shotgun, a correção de que Marksman acontece dentro de um ad set e a distinção ângulo e conceito. Abra na sub-etapa 3.2.

#### 3.2 — Método de teste: Marksman ou Sniper (cânone §7 — lido POR CONCEITO da `creative-engine`)

**O método não se decide aqui — se LÊ.** A Skill `creative-engine` grava `concepts[].testing_method` (`marksman|sniper`) e constrói cada pack NAQUELE método: pack Marksman já vem com 3 ângulos distintos sob hold universal validado, pack Sniper já vem com 1 ângulo em 3 execuções. Re-decidir o método na `ad-strategy` não muda o que os criativos são — só desalinha o registro e quebra a leitura da `ad-analysis` (que pergunta "qual ângulo venceu?" num pack Marksman e "qual execução venceu?" num Sniper). Portanto:

- **Batch com `testing_method` por conceito (padrão da `creative-engine` desde 2026-09):** RESPEITAR o campo, conceito a conceito. Um batch pode ser misto (ex: 2 conceitos `marksman` + 1 `sniper`) — cada ad set carrega o método do SEU conceito, gravado em `ad_sets[].testing_method` no dados.json. O `test_method` batch-level vira resumo: o método único quando todos coincidem, `mixed` quando variam.
- **Fallback (batch legado da `creative-engine` sem o campo):** gravar `ad_sets[].testing_method: "sniper"` em todos os ad sets do batch, com a nota "(legado: sem `angles[]` do batch, a leitura é por execução)" e `data_gap` marcado no dados.json. NÃO aplicar aqui a regra prática "imagens → Marksman" do cânone: ela é regra de ESCOLHA pra teste novo (a `creative-engine` constrói o pack Marksman com 3 ângulos declarados), não de classificação retroativa — rotular de Marksman um pack legado afirmaria uma variação de ângulo que ninguém construiu, e a `ad-analysis` perguntaria "qual ângulo venceu?" a um pack sem `angles[]`. A `ad-analysis` trata batch legado exatamente assim: sem os campos da `creative-engine`, a comparação é por execução (semântica sniper).

| Método | Quando | Como vira estrutura aqui |
|---|---|---|
| **Marksman** | primeiro teste, ou quando a performance platôa | **3 ângulos diferentes DENTRO de um pack 3-2-2 = 1 ad set.** As 3 execuções do mesmo conceito carregam ângulos distintos |
| **Sniper** | a direção já existe (ângulo com tração) — e **toda iteração** depois da leitura da Skill `ad-analysis` | **1 ângulo, 3 execuções** = 1 ad set com o pack 3-2-2 |
| **Shotgun** | só no pipeline de conteúdo de creators (product seeding) | volume sem estratégia individual; não é estratégia criativa deliberada |

> **Correção importante (2026-09-01): Marksman acontece DENTRO de um ad set, não entre ad sets.** O material é literal — *"Marksman (rajada de 3 tiros — testa 3 angles diferentes num único 3:2:2)"*, com o caso real do conceito "superlatives" (variação 1 "world's first stainless steel", 2 "world's easiest to clean", 3 "world's first doctor-designed"). O conceito é a **embalagem** e continua sendo um só ad set; o que varia entre as 3 execuções é o **ângulo**. Espalhar 3 ângulos em 3 ad sets não é Marksman — e a leitura do resultado fica pior, porque o CBO passa a repartir budget entre ad sets antes de você conseguir comparar os ângulos entre si.

**Consequência para o mapeamento:** o método NÃO muda quantos ad sets existem — isso é decidido só pela capacidade da 3.1 (`max_adsets`). O que o método muda é **o que varia dentro de cada pack**. Um batch com 3 conceitos vira 3 ad sets independente de ser Marksman ou Sniper; a diferença é se as 3 execuções de cada pack testam 3 ângulos (Marksman) ou 3 execuções do mesmo ângulo (Sniper).

**Ângulo ≠ conceito** (cânone §7). Ângulo é a **razão de compra em frase** ("para de virar de um lado pro outro a noite toda"). Conceito é a **embalagem** (comparação, depoimento, autoridade). Ao ler o batch da `creative-engine`, confira conceito a conceito: se dois conceitos são a mesma embalagem da mesma razão de compra, eles respondem uma pergunta só — o mais forte entra e o outro volta pro batch seguinte.
