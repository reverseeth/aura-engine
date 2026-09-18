# Ad Strategy · Referência: Capacidade de teste (sub-etapa 3.1)

> A régua canônica de `max_assets` e `max_adsets`, as quatro restrições que valem juntas, a ordem de cálculo com a checagem do target contra o piso físico de CAC (item 1b, tabela por veredito), os casos de contorno e a regra de que o stage não define o número. Abra na sub-etapa 3.1.

#### 3.1 — Capacidade de teste (resolver ANTES de escolher quantos criativos sobem)

Régua canônica (`.claude/lib/ad-taxonomy/README.md` §1):

```
max_assets  = floor(budget_diário ÷ target_cpa)          → criativos simultâneos com chance justa
max_adsets  = floor(budget_diário ÷ (3 × target_cpa))    → conceitos simultâneos (1 ad set = 1 conceito = 3 criativos)
```

O exemplo do cânone: **US$ 160/dia com target CPA de US$ 80 = 2 assets.** Não 5, não 12. Criativo que recebe menos de ~1× target CPA por dia não acumula dado suficiente pra ser lido — o teste devolve ruído com cara de resultado, e a Skill `ad-analysis` classifica ruído.

**As quatro restrições valem JUNTAS (cânone §1, todas obrigatórias):**

| Restrição | Número | Por quê |
|---|---|---|
| Piso operacional | **US$ 100-150/dia** | Abaixo disso não há teste, há palpite — o Meta nem acha compra suficiente pra otimizar |
| Teto por ad set | **~3× target CPA/dia** | É exatamente o que um conceito de 3 criativos precisa pra dar ~1× CPA/dia a cada um. Acima disso o ad set não lê melhor, só gasta mais |
| Teto de ad sets de teste | **5**, enquanto o budget diário está abaixo de US$ 1k/dia | Mais que isso espalha o CBO fino demais e nenhum conceito fecha leitura |
| Teto do batch | `ad sets ≤ conceitos disponíveis no `creative-engine`` | Não existe ad set de teste sem conceito pra colocar dentro |

**Ordem de cálculo (aplicar nesta sequência e gravar cada número no dados.json):**

1. `target_cpa` — `manifest.target_cpa`; na ausência, `offer-builder/dados.json.unit_economics.target_cpa_primary_2x`.
1b. **Validar o `target_cpa` contra o piso físico de CAC ANTES de usá-lo como divisor** (só quando `finance-engine/dados.json` existir — Contexto, item 2b). O leilão tem um chão dado por CPM e CTR: no melhor caso realista o CAC mínimo em escala fica na faixa `cac.cac_floor_reference_usd` (US$ 15-25, cânone §3). Um alvo abaixo desse chão não é um alvo apertado, é um alvo que não existe — e ele **infla a capacidade de teste**: quanto menor o divisor, mais criativos a fórmula do passo 3 autoriza, e o teste sobe com mais conceitos do que o budget consegue de fato ler.

   | `cac.target_reachable_vs_floor` | O que fazer |
   |---|---|
   | `yes` | Seguir. O alvo cabe acima do chão; a capacidade calculada é real |
   | `no` | **Não silenciar e não ajustar o alvo por conta própria.** Calcule a capacidade também com o piso da `finance-engine` (`cac_floor_reference_usd`, ponta alta) no lugar do target e mostre os dois números ao membro: é a diferença entre quantos conceitos ele *acha* que consegue testar e quantos o leilão deixa. Diga a causa sem rodeio — alvo abaixo do piso é problema de **AOV**, não de mídia, e a saída é a `offer-builder` (subir AOV/preço ou sustentar com LTV medido), nunca "criativo melhor". Rode o teste pela capacidade conservadora e registre `cac_floor_check.binding: true` |
   | `unknown` / campo ausente | Fallback: seguir com o target como hoje (o check 12 da Skill `offer-builder` já barrou teto de CAC abaixo de US$ 25 na montagem da oferta) |

   Leia também `cac.cac_max_first_order` — é o CAC em que o **primeiro pedido empata**. Ele não entra na fórmula de capacidade (o divisor continua sendo o `target_cpa`), mas é o número que contextualiza o teto de gasto por ad set no relatório: acima dele, cada compra nova do teste é deficitária no primeiro pedido, o que pode ser decisão consciente (LTV medido) ou acidente.
2. `budget_diário` — `manifest.budget_daily` (fallback: linha "Budget diário" do `profile.md`).
3. `max_assets = floor(budget_diário ÷ target_cpa)` e `max_adsets = floor(budget_diário ÷ (3 × target_cpa))`.
4. `adsets_planejados = min(max_adsets, nº de conceitos do batch 08, 5 se budget_diário < 1000)`. Se `max_adsets` der **0**, o resultado não é "não rodar" — é o primeiro caso de contorno abaixo (1 conceito por vez).
5. `test_budget_daily = min(budget_diário, adsets_planejados × 3 × target_cpa)`, respeitando o piso operacional. Se o próprio `budget_diário` do membro já está abaixo do piso, o piso não pode ser "aplicado" gastando dinheiro que ele não tem — cai no segundo caso de contorno.
6. `assets_planejados = adsets_planejados × 3`.

**Casos de contorno (todos precisam de resposta explícita, nenhum se resolve diluindo):**

- **`max_assets < 3`** — o budget não paga um pack 3-2-2 inteiro. Não dilua: rode **1 conceito por vez**, em fila — sobe o conceito do dia e, quando o próximo entra, sai o mais velho que não pegou tração. Um conceito lido de verdade vale mais que três conceitos ilegíveis.
- **Budget abaixo do piso de US$ 100/dia** — não finja que dá. Dois caminhos honestos, apresentar os dois: **(a)** adiar o teste até o caixa alcançar o piso (leitura limpa, sem desperdício), ou **(b)** rodar com **1 conceito só**, sabendo que o resultado é **direcional e não autoriza decisão de kill nem de escala** — a Skill `ad-analysis` lê com essa ressalva. Nunca apresente (b) como "teste".
- **Capacidade maior que o batch** (`max_adsets` > conceitos disponíveis) — o excedente NÃO vira budget a mais nos mesmos ad sets: isso estoura o teto de ~3× target CPA por ad set e não compra leitura nenhuma. Ou volta pra Skill `creative-engine` por mais conceitos, ou o budget excedente fica fora do teste.
- **`manifest.margin_warning: true`** — ficar no piso operacional e cortar conceitos, nunca esticar budget. Margem apertada não muda a fórmula; muda quanto erro o membro aguenta.
- **CPA-alvo abaixo do piso físico de CAC** (`cac.target_reachable_vs_floor: "no"`, item 1b) — a capacidade calculada com esse alvo é fictícia, e rodar por ela sobe mais conceito do que o budget lê. Use a capacidade conservadora do item 1b e mande a correção pra `offer-builder` (AOV/preço), não pra mídia.

**O stage não define o número** (`.claude/rules/member-stage-awareness.md`) — a capacidade define. O stage define como os caminhos são apresentados: pra **starter** abaixo do piso, o caminho recomendado é adiar e acumular caixa (dito sem rodeio); pra **validating**, a restrição que costuma morder é a capacidade; pra **scaling**, a restrição que costuma morder é o tamanho do batch da `creative-engine` e o teto de 5 ad sets abaixo de US$ 1k/dia.
