# Creative Engine · Referência: Capacidade de teste e tamanho do batch (ETAPA 2)

> A conta de quantos conceitos o budget consegue ler, os casos de contorno, a reconciliação com a rule de stage, a conversa de volume com membro em escala e o texto que se mostra ao membro. Abra na ETAPA 2.

### ETAPA 2 — Quantos Conceitos Entram no Batch (capacidade de teste, não stage)

**Estrutura de teste atual (Skill `ad-strategy`, ETAPA 3.3):** **1 campanha com CBO → N ad sets (broad/Advantage+), sendo 1 ad set = 1 conceito = 3 criativos + 2 primary texts + 2 headlines**. Logo **1 conceito = 1 ad set**, e o número de conceitos do batch é o número de ad sets que o budget consegue LER.

**Quem decide o número é a capacidade de teste, não o stage do membro** (cânone `.claude/lib/ad-taxonomy/README.md` §1). A Skill `ad-strategy` resolve essa conta na ETAPA 3.1 dela e a grava em `ad-strategy/dados.json → test_capacity`. Ordem de leitura:

1. **Se `workspace/[produto]/ad-strategy/dados.json` existe** (já houve campanha antes): leia `test_capacity.max_adsets` — é ele o teto de conceitos deste batch. Não recalcule por fora. Só recalcule pelo item 2 se `manifest.budget_daily` ou `manifest.target_cpa` mudaram desde aquela gravação.
2. **Se não existe** (primeiro batch do produto — a `ad-strategy` roda depois desta skill): aplique a MESMA fórmula do cânone §1, com os mesmos insumos que a `ad-strategy` usa:
   ```
   max_assets = floor(budget_diário ÷ target_cpa)          → criativos com chance justa
   max_adsets = floor(budget_diário ÷ (3 × target_cpa))    → CONCEITOS simultâneos
   ```
   `budget_diário` = `manifest.budget_daily` (fallback: linha "Budget diário" do `profile.md`); `target_cpa` = `manifest.target_cpa` (fallback: `offer-builder/dados.json.unit_economics.target_cpa_primary_2x`). Exemplo do cânone: **US$ 160/dia com target CPA de US$ 80 = 2 assets** — não 5, não 12.
3. **Teto de ad sets de teste: 5**, enquanto o budget diário estiver abaixo de US$ 1k/dia (cânone §1). **N de conceitos = o MENOR entre `max_adsets` e esse teto de 5.**

**Casos de contorno (mesma doutrina da ETAPA 3.1 da Skill `ad-strategy` — nenhum se resolve diluindo):**

- **`max_assets < 3`** — o budget não paga um pack 3-2-2 inteiro. Gere **1 conceito** e avise que ele roda em fila: sobe um, e quando o próximo entra sai o mais velho que não pegou tração.
- **Budget abaixo do piso operacional de US$ 100-150/dia** — não finja que dá teste. Gere **1 conceito** e diga ao membro, sem rodeio, que o resultado é **direcional** e não autoriza decisão de kill nem de escala (a Skill `ad-analysis` lê com essa ressalva).
- **Capacidade maior que a ideação** (`max_adsets` maior que o número de ângulos fortes que a ETAPA 3 produziu) — não invente conceito pra preencher slot. Entregue os que se sustentam e diga quantos slots ficaram abertos.

**Referência de volume por conceito:** cada conceito = 1 pack 3-2-2 = 1 ad set = 3 criativos. Então N conceitos = N ad sets = N×3 criativos no teste inteiro.

> **Por que não empilhar conceitos além da capacidade:** ad set que recebe menos que ~3× target CPA por dia (o teto por ad set do cânone §1 — é o que dá mais ou menos 1× CPA/dia a cada um dos 3 criativos) não acumula dado suficiente pra decisão de kill (Skill `ad-analysis`): o teste devolve ruído com cara de resultado. O excedente vai pro batch seguinte, na fila, e nunca comprimido em ad set compartilhado (Skill `ad-strategy`, ETAPA 7, erro 2). Budget maior é o que compra mais conceitos.

> **Reconciliação com a rule `member-stage-awareness`:** a rule **não define contagem de conceitos** — ela aponta pra mesma capacidade calculada acima (cânone §1, resolvida na Skill `ad-strategy` ETAPA 3.1). Nenhum número de conceito sai do stage. O que o stage governa é o TOM e a apresentação do resultado: pra **starter** abaixo do piso operacional, o caminho recomendado é acumular caixa antes de testar, dito sem rodeio, e o que rodar é direcional (não autoriza kill nem escala); pra **validating**, a restrição que costuma morder é a própria capacidade — o excedente do batch entra na fila do batch seguinte em vez de diluir o teste; pra **scaling**, a capacidade deixa de ser o gargalo (o teto de 5 ad sets abaixo de US$ 1k/dia costuma caber) e quem morde passa a ser o tamanho da ideação.

**Conversa de volume com membro `scaling` (dois sistemas da base — rodar os dois juntos, ANTES de fechar o tamanho do batch):**

- **Creative Strategy em 9 Dimensões (self-audit red/yellow/green)** — rode a `best_query` exata `9 dimensoes self-audit business brand creative sales channel funnel production testing measurement`. Auditoria de maturidade da estratégia criativa: pontue com o membro as nove dimensões (negócio, marca, criativo, vendas, canal, funil, produção, testes e mensuração) em vermelho/amarelo/verde. Dimensão vermelha em produção/testes/mensuração muda o plano do batch antes de qualquer conceito nascer (ex: mensuração vermelha = batch menor até a `tracking-setup` sustentar a leitura; produção vermelha = o gargalo não é ideação, é pipeline de execução). Pra starter/validating, pule a auditoria — a capacidade já é o gargalo e o audit vira ruído.
- **Testing Engine Calculator (share de spend em teste)** — rode a `best_query` exata `quanto do spend vai para teste 20% saudavel 50% dificuldade 100% falhando budget dividido pelo CPA`. Com a conta em escala, a pergunta muda de "quantos conceitos cabem" pra "que fatia do spend TOTAL da conta está em teste": **~20% é saudável; ~50% indica dificuldade** (a conta depende demais de achar winner novo); **100% é conta falhando** (tudo em teste, nada consolidado). Use esse share na conversa de volume pra calibrar quanto do budget vai pro batch novo vs pros breakthroughs já rodando — a capacidade por ad set continua saindo do cânone §1, este sistema só diz quanto da conta o teste inteiro pode ocupar.

**Champions (conceitos já validados):** breakthrough validado não disputa slot de teste — a Skill `scale-engine` o promove a **ad set próprio em campanha ABO paralela** (cânone §5), mantendo o ad original rodando no CBO. Os slots calculados acima são todos de conceito NOVO.

Mostre ao membro (sem pedir confirmação):

"Com CPA alvo de $[target_cpa] e budget de $[X]/dia, esse budget consegue LER **[N] conceitos** (~[N×3] criativos) — é esse o tamanho do batch. Cada conceito é um pack 3-2-2 (3 criativos + 2 primary texts + 2 headlines) e vira **um ad set próprio** dentro da campanha com CBO, que é o que permite ler qual conceito funcionou. O que os 3 criativos de cada pack variam entre si depende do método de teste do conceito (ETAPA 4.5.A.0): **Marksman** = 3 ângulos distintos pra achar direção; **Sniper** = 1 ângulo em 3 execuções. [Se alguma restrição mordeu — piso, teto de 5 ad sets, ideação menor que a capacidade: diga qual em uma frase. Se sobrou ângulo: os conceitos excedentes ficam pro próximo batch.]"
