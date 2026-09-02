---
name: finance-engine
description: Engine financeira da marca — dona do modelo completo declarado no cânone `.claude/lib/unit-economics/README.md` §5 (4 alavancas, cohorts, ciclo de caixa). Roda em DOIS MODOS decididos pelos dados disponíveis, sem perguntar mais que o necessário. Modo A (Planejar, sem histórico): monthly model com custos fixos, margem de contribuição, ponto de cobertura do fixo, piso de CAC, caixa pra 90 dias e benchmarks DTC. Modo B (Medir, com meses fechados): as 4 alavancas (AOV, CAC, ad spend, % de recorrentes), cohorts com decay factor e LTV medido, payback de 90 dias, first-order profitability, taxa de aumento de CAC e teto de escala, ciclo de conversão de caixa (~105 dias de float) e banking sheet semanal. É a skill que CALCULA a espiral do ROAS (cânone §4) e publica o `breakeven_roas_with_fixed` que as skills 11 e 12 consultam antes de recomendar qualquer corte de spend. Nunca chama de lucro um número que não subtraiu custo fixo; nunca estima custo fixo, CAC real nem contagem de clientes novos — pede. Use quando o membro disser "finance", "finanças", "números", "projeção", "quanto vou faturar", "fluxo de caixa", "quanto preciso de capital", "meu negócio dá lucro", "quanto posso gastar em ads".
---

# Finance Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md` — domínio `finance-projections` — o tamanho é o que o frameworks.json disser). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> **Cânone que governa esta skill:** `.claude/lib/unit-economics/README.md`. Ele já declara a 15 como **dona do modelo completo** (§5). Esta skill **referencia** o cânone — não redefine margem de contribuição, first order vs repeat order, CAC vs CPA nem a espiral do ROAS. Onde o texto daqui divergir do cânone, **o cânone vence**, e a divergência é bug desta skill.

## Quando Usar

Quando a pergunta é sobre o **negócio inteiro como máquina financeira**, não sobre um pedido nem sobre um ad set. Gatilhos: "finance", "finanças", "números", "projeção", "quanto vou faturar", "fluxo de caixa", "quanto preciso de capital", "meu negócio dá lucro", "quanto posso gastar em ads", "quanto tempo meu caixa aguenta".

**Não é fase do pipeline — é skill de consulta, como a 09.** Dois momentos naturais:

- **Logo depois da 04 (Modo A):** "a oferta que acabei de montar fecha a conta do negócio?" A 04 responde por pedido; a 15 responde por mês, com o custo fixo dentro.
- **A qualquer momento depois do lançamento (Modo B):** com mês fechado na mão, medir de verdade — alavancas, cohorts, payback, caixa. Recorrente por natureza: o banking sheet é ritual semanal, a calibragem de cohort é mensal, a revisão de LTV é semestral.

**O que esta skill responde e nenhuma outra respondia:** qual é minha margem de contribuição, qual é meu piso de CAC, quanto tempo leva meu payback, quanto caixa preciso pra rodar 90 dias, e o que acontece se eu mexer numa alavanca.

**O que ela NÃO faz:** não desenha oferta (04), não decide budget de ad set nem estrutura de campanha (10/12), não classifica criativo (11). Ela entrega o **número** que essas skills consultam.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. Copy consumidor-final não existe nesta skill — ela não produz nada que vá pro consumidor.

### Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `workspace/[produto]/04-offer-builder/dados.json` existe — é a fonte do **stack de custos variáveis** (`cogs_breakdown`, 8 campos) e do AOV esperado
- [ ] **Modo B adicionalmente:** existe pelo menos **1 mês fechado** com ad spend do período E contagem de clientes novos do Shopify (`new customer = TRUE`). Sem os dois, o modo é A — não force B com dado pela metade

Se `04-offer-builder/dados.json` faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill 04 agora, **OU (B)** prosseguir pedindo direto ao membro o AOV e o stack de custos variáveis item a item, marcando `manifest.skipped_preflight += ["04-offer-builder/dados.json"]` e avisando no output que recomenda re-executar depois da 04.

### Contexto a carregar

1. `workspace/profile.md` — stage e budget declarado (define linguagem e apetite; ver `member-stage-awareness.md`)
2. `workspace/[produto]/manifest.json` — em especial **`manifest.fixed_costs_monthly`** (campo canônico já existente no schema; escrito pelo membro através da 04, 11, 12 ou desta skill). Se existir, **use e confirme**; não pergunte de novo o que já está gravado
3. `workspace/[produto]/04-offer-builder/dados.json` — leia:
   - **`cogs_breakdown`** (8 campos, todos em dinheiro POR PEDIDO): `product_delivered`, `shipping_to_customer`, `pick_pack`, `payment_processing`, `taxes_and_duties`, `subscription_app_fee`, `agency_fee_variable`, `refund_chargeback_provision`
   - **`unit_economics`**: `weighted_margin_per_order` (denominador de margem canônico de todo o framework), `contribution_margin_pct`, `breakeven_cpa`, `breakeven_roas`, `target_cpa_primary_2x/3x`, `cac_basis`, `repeat_order{}`, `aov_blended`
   - **`pricing.aov_expected`** e **`budget_viability.fixed_costs_monthly`** (pode estar `null` — é exatamente o buraco que esta skill fecha)
4. `workspace/[produto]/11-ad-analysis/dados.json` **(se existir)** — spend real, CPA real, ROAS real, AOV real, `psm_real`. É a matéria-prima do Modo B
5. `workspace/[produto]/12-scale-engine/dados.json` **(se existir)** — `cash_flow.cash_gap_projected` e `fixed_cost_gate` da última rodada de escala. A 12 estima caixa sozinha hoje; aqui o número é recalculado com o fixo dentro e devolvido pra ela
6. `workspace/[produto]/13-retention-engine/dados.json` **(se existir)** — take rate de assinatura e sinais de recompra, que alimentam a alavanca de % de recorrentes
7. Rodadas anteriores desta skill em `workspace/[produto]/15-finance-engine/` — comparar premissas com o realizado é metade do valor do Modo B
8. **Skills laterais (se existirem — leitura aditiva, nunca pré-requisito):**
   - `17-promo-engine/dados.json` → janela promocional fechada no período: o mês da janela entra em `monthly_notes[]` automaticamente ("promoção no site inteiro") e o cohort de nov/dez (ou da janela) é marcado pra **não calibrar o decay** sem a nota — cohort de promo tem LTV atípico e compará-lo com mês normal quebra o modelo
   - `18-team-engine/dados.json` → `payroll.monthly_total` (ou o delta de contratação planejada): entra nos custos fixos do monthly model — contratação nova SEM atualizar o fixo é exatamente o furo que o Modo A existe pra fechar
   - `20-marketplace-engine/dados.json` → `channels[].fees` e comissões (Amazon/TikTok Shop/afiliados): comissão é **custo variável por pedido daquele canal** — quando houver receita de marketplace no período, o stack de variáveis do canal é montado à parte (a margem blended esconde canal deficitário)

### As quatro regras que não se negociam

Vêm do cânone. Valem em todo output desta skill, nos dois modos.

1. **Nunca chame de "lucro" um número que não subtraiu custo fixo** (cânone §1). O rótulo correto é **margem de contribuição**. Quando o custo fixo for desconhecido, **diga isso explicitamente** em vez de omitir: "margem de contribuição de US$ X; sem os custos fixos informados não dá pra dizer se há lucro". Nenhum campo do `dados.json` desta skill chama-se "profit"; o único número que merece o nome é `monthly_model.operating_income`, e ele é `null` enquanto os fixos forem `null`.

2. **CAC ≠ CPA** (cânone §3). CAC = ad spend do período ÷ **clientes novos do Shopify** (`new customer = TRUE`) no mesmo período. CPA de plataforma conta conversão atribuída pelo Meta, cliente recorrente incluído. Onde a decisão for de aquisição, o modelo usa CAC. Misturar os dois torna o modelo falso — e todo o Modo B é construído em cima dele.

3. **A espiral do ROAS é conta desta skill** (cânone §4). A 15 é quem calcula e publica o número; a 11 e a 12 leem. Detalhe operacional na ETAPA 5.

4. **Três campos nunca se estima. Faltando, a skill pede:**

   | Campo | Por que nunca se chuta |
   |---|---|
   | **Custo fixo mensal** | É o que separa margem de contribuição de lucro. Chutar inverte a recomendação de spend. |
   | **CAC real** | Só existe com clientes novos do Shopify. Estimar CAC a partir do CPA do Meta é o erro que o cânone §3 nomeia. |
   | **Contagem de clientes novos** | É o denominador do CAC. Sem ela não há CAC, não há cohort e não há LTV. |

   Faltando qualquer um: o campo fica `null` no `dados.json`, entra em `pending_inputs[]`, o bloco que depende dele fica marcado como bloqueado, e o relatório diz **o que falta e o que destrava**. Nunca preencher com plausível.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. O domínio inteiro é `finance-projections` no `.claude/lib/kb-index/`. **Esta skill é a consumidora que faltava** dos quatro sistemas marcados como dormant no índice (`use_in_skill: "—"`) — a partir dela, eles são puxáveis.

**Mínimo a carregar nos DOIS modos:**

- **Contribution Margin + Variable Cost Stack** — `contribution margin stack de custos variáveis COGS fully loaded processing fees`
- **First Order vs Repeat Order Economics ("perder para ganhar")** — `first order vs repeat order economics perder no primeiro pedido janela payback`
- **The ROAS Death Spiral** — `espiral do ROAS cortar spend aumenta prejuízo custos fixos não encolhem`
- **DTC P&L Benchmarks + The Barometers** — `benchmarks financeiros DTC barometers CAC LTV COGS consertáveis AOV baixo mata`
- **Four Quarter Accounting (25/25/25/25)** — `Four Quarter Accounting 25% COGS overhead aquisição EBITDA Taylor Holiday`
- **Meta CAC Floor + regra de forecast 4:1** — `CAC floor Meta $15-25 em escala crescer 5% spend razão 4:1`
- **3-Scenario Pre-Scale Stress Test** — `stress test antes de escalar CAC +20% LTV −20% COGS +5% modelo sobrevive`
- **CAC vs CPA Discipline (Shopify new customer = TRUE)** — `CAC igual spend dividido por clientes novos Shopify não CPA de plataforma`
- **A Função Financeira em 3 Camadas** _(dormant até esta skill)_ — `função financeira em 3 camadas bookkeeping reporting strategy brand DTC`

**Adicionalmente no Modo B:**

- **4-Lever Projection Model** — `projection sheet 12 meses 4 alavancas AOV CAC ad spend returning customers`
- **Cohort LTV Model (12 meses, decay ~0,8)** — `cohort model LTV 12 meses decay 0.8 total margin acumulada Lifetimely`
- **90-Day Payback + First-Order Profitability Check** — `janela de payback 90 dias first-order profitability CAC máximo margem`
- **Scale-Ceiling Detection (plateau no operating income)** — `detecção de teto de escala operating income cai além de X de spend plateau`
- **Great Wall of Death — as 3 perguntas de cash conversion** — `great wall of death cohort fica positivo antes do boleto vencer cash-out date`
- **The Float Stack (Meta net 45 + Melio + Amex Plum ≈ 105 dias)** _(dormant até esta skill)_ — `stack de float Meta invoicing net 45 Melio Amex Plum net 60 105 dias`
- **Float Guardrails (erro de 5% no cohort vira +$157k em −$257k)** — `guardrails do float erro de 5% no cohort calibrar antes de alavancar`
- **Banking Sheet + Founder Burn Rate Rule** _(dormant até esta skill)_ — `banking sheet ritual semanal domingo todas as contas net cash flow`
- **Revenue Slice & Dice / Triple Profit Tracking** _(dormant até esta skill)_ — `triângulo de forecasts sales cash inventory safety stock lead time`
- **Offer-Change Break-Even Reset** — `nova oferta recalcular break-even ROAS e CPA-alvo antes de escalar promo`

Aprofunde. Um erro de 5% num cohort vira centenas de milhares de dólares de diferença de decisão — é o único lugar do framework onde a precisão do número importa mais que a velocidade da entrega.

## Fluxo da Skill

**ETAPAs 1-6 e 12-14 rodam nos dois modos. ETAPAs 7-11 são exclusivas do Modo B** e são puladas silenciosamente quando não há histórico — sem seção vazia no relatório, sem explicar o que não foi feito (rule `report-only-results.md`).

### ETAPA 1 — Detectar o modo e completar só o que falta

O modo é **decidido pelos dados**, não perguntado. Regra:

| Situação dos dados | Modo | Observação |
|---|---|---|
| Nenhum mês fechado com ad spend **e** clientes novos do Shopify | **A — Planejar** | Pré-lançamento ou primeiros dias. O modelo é projetivo. |
| 1 a 2 meses fechados | **B — Medir**, cohort **não calibrado** | Decay assumido; a coluna de cohort roda com aviso de que ainda não estabilizou. |
| 3 ou mais meses fechados | **B — Medir**, cohort **calibrado** | O decay estabiliza; o modelo passa a valer pra decisão de escala. |

Grave em `mode` e `mode_reason`. Se o membro pedir explicitamente o modo que os dados não sustentam, faça o que os dados sustentam e diga por quê em uma linha — nunca rode o Modo B com número inventado.

**Pré-popule TUDO dos artefatos antes de perguntar qualquer coisa.** Do `04-offer-builder/dados.json` saem AOV, o stack de custos variáveis inteiro e a margem por pedido. Do `manifest` sai `fixed_costs_monthly`, se já existir. Do `11-ad-analysis/dados.json` saem spend, CPA, ROAS e AOV reais.

Depois, peça **numa única mensagem** só o que não vive em nenhum arquivo:

**Sempre (os dois modos):**
- **Custo fixo mensal** — "tudo que você paga mesmo vendendo zero: time, apps, ferramentas, aluguel, contabilidade, agência de valor fixo." Se o membro não souber separar, peça o total e a lista; a decomposição é secundária, o total não é. Se `manifest.fixed_costs_monthly` já existir, só confirme: "seus custos fixos ainda são US$ X/mês?"
- **Caixa disponível hoje** — o número que responde "quanto tempo eu aguento".

**Só no Modo B:**
- **Clientes novos do Shopify no período** (Analytics → Reports → *New vs Returning customers*, com a dimensão de mês). É o denominador do CAC — sem ele não há Modo B.
- **Ad spend total do mesmo período** (todas as plataformas, não só Meta).
- **Curva de LTV por cohort**, se o membro tiver (Lifetimely é a fonte mais precisa; Triple Whale manual serve; Shopify puro dá pra reconstruir). Sem ela, a ETAPA 8 roda com decay assumido e o aviso correspondente.
- **Prazo real de repasse do processador** (`payout_lag_days`) e, se usar faturamento da Meta, o prazo da fatura.

Formato da pergunta, uma vez só: *"Já tenho [lista do que foi lido]. Me falta só: [campos ausentes]."* Não re-explique campo já preenchido.

### ETAPA 2 — Monthly Model (o resultado do mês decomposto linha a linha)

O modelo mensal é a espinha dos dois modos. Custos **fixos** declarados em dinheiro; custos **variáveis** como **% do AOV**.

**Teste pra classificar um custo:** *"se eu dobrar a receita, esse custo dobra?"* Taxa de processamento: sim (variável). Ad spend: sim, às vezes mais que dobra. Fee de agência cobrado como % do spend: sim. App de assinatura: sim. Folha: não (fixo). Software: depende — alguns cobram por pedido. Aluguel, contabilidade, ferramentas: fixo.

Monte a tabela nesta ordem — ela é a mesma sequência do cânone §1, e nenhuma linha pode ser pulada:

| Linha | Como calcular |
|---|---|
| Receita | AOV × pedidos do mês |
| (−) COGS fully loaded (o custo do produto **entregue**: produto + embalagem + frete até o cliente + tarifa) | `cogs_breakdown.product_delivered` + `shipping_to_customer` + `pick_pack` + `taxes_and_duties` |
| **= Lucro bruto** | receita − COGS |
| Margem bruta % | lucro bruto ÷ receita |
| (−) Processamento de pagamento | `cogs_breakdown.payment_processing` (~3%) |
| (−) App de assinatura | `cogs_breakdown.subscription_app_fee` (0,5-1%, zero quando não há assinatura) |
| (−) Fee de agência variável | `cogs_breakdown.agency_fee_variable` (só quando é % do spend; fee de valor fixo é custo FIXO) |
| (−) Provisão de reembolso/chargeback | `cogs_breakdown.refund_chargeback_provision` (nunca zero) |
| (−) Ad spend | o maior custo variável de todos |
| **= Margem de contribuição** | receita − todos os variáveis acima |
| Margem de contribuição % | margem de contribuição ÷ receita |
| (−) Custos fixos mensais | `manifest.fixed_costs_monthly` — **`null` se não informado** |
| **= Resultado operacional** | **o único número que pode ser chamado de lucro.** `null` enquanto os fixos forem `null` |

**Os dois números que quase ninguém calcula e que mudam a conversa:**

- **`gross_margin_needed_to_exist`** = o próprio custo fixo mensal, em dinheiro. É o **lucro bruto** que a operação precisa gerar todo mês **só pra pagar o fixo**, antes de gastar um centavo em anúncio.
- **`revenue_at_gross_margin_to_exist`** = custo fixo mensal ÷ margem bruta %. É a receita que produz esse lucro bruto.

Com US$ 38,5k de custo fixo e 70% de margem bruta: a operação precisa de **US$ 38,5k de lucro bruto por mês só pra existir**, o que exige cerca de **US$ 55k de receita** — e isso ainda é antes de considerar o custo dos anúncios. Coloque os dois em destaque no relatório; são eles que reenquadram a pergunta "quanto eu preciso vender?".

Se os fixos forem `null`: a tabela para na linha de margem de contribuição, as duas últimas linhas ficam explicitamente marcadas como não calculáveis, e o relatório diz o que destrava.

### ETAPA 3 — Margem de contribuição e o ponto de cobertura do fixo

A margem de contribuição é **a lucratividade de escalar**: se a receita dobra, ela aproximadamente dobra. O custo fixo não. Por isso a pergunta certa nunca é "meu ROAS está bom?", e sim **"minha margem de contribuição cobre meus fixos?"**.

Calcule e apresente três números:

- **`contribution_margin_monthly`** — em dinheiro e em %.
- **`fixed_cost_coverage_ratio`** = margem de contribuição ÷ custo fixo mensal. Abaixo de 1,0, a operação consome caixa todo mês, por mais bonito que esteja o ROAS.
- **`revenue_to_cover_fixed`** = custo fixo mensal ÷ margem de contribuição %. É a receita mensal em que a operação empata de verdade. A margem de contribuição já é líquida de ad spend, então essa receita pressupõe a mesma eficiência de mídia do mês que serviu de base — se o CAC piorar, o ponto de equilíbrio sobe junto.

**Separe first order de repeat order (cânone §2), sempre.** São economias diferentes: o primeiro pedido carrega o CAC inteiro e os fees atrelados a spend; a recompra não carrega nenhum dos dois. Modelar os dois juntos esconde a decisão. Use `unit_economics` (first order) e `unit_economics.repeat_order` do `04-offer-builder/dados.json` — a 04 já entrega separado. Um produto pode ser deficitário no primeiro pedido e excelente no segundo, e a decisão de spend depende de qual dos dois você está olhando.

Exemplo canônico da separação, pra calibrar a leitura: pedido de US$ 100 com COGS US$ 35, processamento US$ 3,30, app US$ 1, CAC US$ 40 e fee de agência US$ 2 → margem de contribuição do **1º pedido = US$ 18,70**. O **pedido de recompra**, sem CAC e sem fee de agência, dá **US$ 60,70**. Com o CAC subindo a US$ 70, o 1º pedido vira −US$ 12,80 — e uma única recompra em 90 dias devolve +US$ 47,90.

### ETAPA 4 — Piso de CAC e checagem do CPA-alvo

**Piso físico do CAC no Meta:** existe um chão dado por CPM e CTR. No melhor caso realista (CPM ~US$ 10-15, CTR ~3%), o CAC mínimo em escala fica em **US$ 15-25** (cânone §3). Abaixo disso, desconfie da atribuição antes de comemorar — quase sempre é CPA de plataforma disfarçado de CAC.

Três checagens, nesta ordem:

1. **`cac_max_first_order`** = `unit_economics.weighted_margin_per_order`. É o CAC em que o primeiro pedido empata. Acima dele, o primeiro pedido é deficitário — o que **pode** ser certo, mas só com LTV medido e janela de payback definida (ETAPA 9).
2. **CPA-alvo da 04 é alcançável?** Compare `target_cpa_primary_2x` e `target_cpa_primary_3x` contra o piso de US$ 15-25. Se o alvo estiver **abaixo do piso**, o problema não é mídia — é AOV. Diga isso sem rodeio: nenhuma otimização de criativo faz o Meta entregar cliente novo abaixo do chão de CPM.
3. **AOV sustenta tráfego pago?** Esta é a barômetro que **não conserta com trabalho**. CAC, LTV e COGS são consertáveis; AOV baixo demais não. Produto de AOV abaixo de ~US$ 30 raramente fecha conta em escala — a saída é AOV e LTV (bundle, assinatura, upsell), não "mídia melhor". Para assinatura: mínimo absoluto US$ 29,99, faixa realista US$ 39-49.

Ordem de ataque quando o modelo está no vermelho, do mais fácil pro mais difícil: **CAC → LTV → COGS → AOV**. COGS acima de **30% é teto de longo prazo** — acima disso, subir preço, renegociar volume ou trocar de fábrica. Volume destrava negociação: 4× de volume costuma comprar 2 pontos de COGS, e o plano de processamento melhora perto de 8 dígitos anuais.

### ETAPA 5 — A espiral do ROAS: o número que a 11 e a 12 consultam

**Esta ETAPA é a razão principal de a skill existir.** O cânone §4 define o erro; aqui ele vira número.

ROAS é adimensional e ignora custo fixo. Maximizá-lo isoladamente inverte a decisão certa. A conta que prova isso, e que esta skill reproduz com os números do membro:

> Base: ROAS-alvo 4×, spend US$ 250k → receita US$ 1M; COGS 30% → lucro bruto US$ 700k; margem de contribuição US$ 450k; fixos US$ 300k → **lucro US$ 150k**.
> ROAS cai pra 3× com o mesmo spend: margem de contribuição US$ 275k; fixos continuam US$ 300k → **prejuízo de US$ 25k**.
> Reação intuitiva — cortar spend pra US$ 150k e "voltar ao 4×": margem de contribuição US$ 270k → **prejuízo MAIOR, US$ 30k**. O ROAS subiu e o resultado piorou, porque os fixos não encolheram.
> Reação correta: **aumentar** spend pra US$ 350k aceitando ROAS ~2,65 → volta ao breakeven.

**As fórmulas (rode com os números do membro, não com os do exemplo):**

```
margin_rate = weighted_margin_per_order / aov_expected        (= 1 / breakeven_roas da skill 04)

breakeven_roas_with_fixed = (1 + fixed_costs_monthly / ad_spend_monthly) / margin_rate

spend_to_breakeven_with_fixed = fixed_costs_monthly / (margin_rate × roas_projected − 1)
    válido só quando  margin_rate × roas_projected > 1
```

Conferência com o exemplo do cânone (`margin_rate` = 0,70; fixos 300k): a 250k de spend, `breakeven_roas_with_fixed` = (1 + 300/250)/0,70 = **3,14** — por isso 3,0× dá prejuízo. A 350k, = (1 + 300/350)/0,70 = **2,65** — exatamente o número do material. **O breakeven com fixo CAI conforme o spend sobe.** É essa propriedade que torna o corte reflexo a decisão errada.

**A linha divisória, e é ela que decide:**

| Situação | O que cada dólar a mais de spend faz | Recomendação |
|---|---|---|
| ROAS **acima** do breakeven de variável (`1 / margin_rate`) | **Adiciona** margem de contribuição | Cortar spend **aumenta** o prejuízo. A saída costuma ser subir spend aceitando ROAS menor até `spend_to_breakeven_with_fixed`. |
| ROAS **abaixo** do breakeven de variável | **Destrói** margem de contribuição | Cortar é certo. Aqui a régua de descida do `ad-taxonomy` §5 (−20%) vale integralmente — mais volume só aprofunda o buraco. |

**Gate obrigatório de saída desta ETAPA:**

- **Fixos conhecidos** → calcule, publique `breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed` e `verdict`, e grave `cut_spend_recommendation_allowed` conforme a linha divisória acima.
- **Fixos desconhecidos** → `breakeven_roas_with_fixed: null`, `verdict: "blocked_pending_fixed_costs"`, `cut_spend_recommendation_allowed: false`. A recomendação **vira pergunta, não instrução**: "quanto você tem de custo fixo por mês?". Registre em `pending_inputs[]` e escreva isso no relatório.

Esses campos são o **contrato** com as skills 11 e 12 (ver "Contrato de leitura" no fim). **Quando este arquivo existe**, nenhuma das duas emite corte de spend por queda de ROAS sem ler daqui — o veredito calculado aqui vence a heurística local delas. Quando não existe, elas caem no comportamento anterior: sem os custos fixos na mesa, a recomendação de corte vira pergunta ao membro (cânone `unit-economics` §4). A 15 **não é pré-requisito** de nenhuma skill; ela substitui uma pergunta por um número.

### ETAPA 6 — Caixa: quanto o negócio precisa pra rodar 90 dias

Modelo lucrativo e caixa morto convivem. O modelo diz lucro no mês 3; o banco diz morte na semana 3. Troque a pergunta *"sou lucrativo eventualmente?"* por três: **quando o dinheiro sai da conta, quando entra, e o cohort fica positivo antes do boleto vencer?**

**Necessidade de caixa em 90 dias:**

```
caixa_necessario_90d =
      (ad_spend_diário × payout_lag_days × 1,3)      ← o buraco do descasamento (1,3 = margem de segurança)
    + (custo_fixo_mensal × 3)                         ← o fixo não espera venda entrar
    + desembolso_de_estoque_previsto_no_período       ← reposição, se houver
    − margem_de_contribuição_acumulada_projetada_90d  ← o que a operação devolve no período
```

**`payout_lag_days` é campo do membro, não default.** O lag nominal do Shopify Payments é 3-5 dias (Stripe ~2), mas processadora segura mais quando a conta é nova ou o volume dá spike — exatamente o que a escala provoca. Loja com menos de ~90 dias de processamento, ou no primeiro pico grande: use **7-14 dias** e confirme no dashboard do processador se há reserva rolante ativa. Escalar assumindo repasse em 3 dias com reserva de 30% ativa é o furo de caixa clássico da loja nova.

Publique **`runway_months`** = caixa disponível ÷ burn mensal. É o número que responde "quantos meses eu tenho pra fazer isso funcionar" — e o que transforma decisão de spend em decisão de prazo.

**Guard-rails, sempre no relatório:**
- Saber a **data exata da saída de caixa** (a data do boleto, não "mês 3").
- **Float não conserta oferta quebrada.** Prazo maior de pagamento adia o problema, não resolve.
- Nunca escalar dívida mais rápido que a capacidade de entrega — reembolso e chargeback destroem float.
- Não financiar caos operacional.

No Modo B esta ETAPA ganha o stack de float completo (ETAPA 10).

---

**As ETAPAs 7 a 11 rodam somente no Modo B.**

### ETAPA 7 — [Modo B] As 4 alavancas

Qualquer negócio de ecommerce é controlado por **4 alavancas: AOV, CAC (por cliente novo pago), Ad Spend e % de clientes recorrentes.** O valor do modelo não é prever o futuro — é responder "o que acontece se eu mexer nisto?" antes de mexer.

Monte a baseline com os números reais do mês fechado e simule **uma alavanca por vez**, mantendo as outras três congeladas. Para cada simulação, reporte o delta de **margem de contribuição** e de **resultado operacional** (o segundo só existe com os fixos informados).

| Alavanca | O que costuma mover na prática |
|---|---|
| **AOV** | Subir preço; bundle por volume; faixa de frete grátis; upsell pós-compra de um clique; anunciar a versão premium. Costuma ser a alavanca de maior impacto: no material de referência, AOV de US$ 35 → US$ 48 levou o mês de −US$ 53k pra +US$ 58k. |
| **CAC** | Criativo mais interessante (CTR sobe, CAC cai); landing page melhor; **oferta melhor** — mexe em CVR, CTR e AOV ao mesmo tempo. Cuidado com o piso da ETAPA 4: reduzir CAC costuma ser a meta menos realista das quatro. |
| **Ad Spend** | Com margem de contribuição positiva, **volume dilui o fixo**. Expandir países, plataformas novas. É a alavanca que a espiral do ROAS (ETAPA 5) governa. |
| **% recorrentes** | Email/SMS, programa de fidelidade, assinatura, unboxing melhor, indicação. Alimenta os cohorts da ETAPA 8. |

**Diagnóstico por eliminação quando o resultado está no vermelho:** (a) cortar custo fixo, (b) reduzir CAC — frequentemente irrealista, (c) escalar spend, (d) subir AOV. Ranqueie as quatro pelo delta calculado e nomeie **`highest_impact_lever`**. Não recomende as quatro ao mesmo tempo: mexer em tudo junto impede saber o que funcionou.

### ETAPA 8 — [Modo B] Cohorts com decay factor e LTV medido

Cohort = clientes adquiridos no mesmo mês, seguidos ao longo de 12 meses. É o que legitima gastar mais que o concorrente.

**Estrutura da tabela** (por cohort, mês a mês):

| Coluna | Definição |
|---|---|
| `ltv_pct` | Multiplicador sobre o mês 0. **Mês 0 = 100% por definição** (na prática 101-102%, porque uma fração recompra dentro dos 28 dias). Mês 1 = 60% significa que, pra cada US$ 100 do mês 0, o mês 1 acrescenta US$ 60. |
| `revenue` | `ltv_pct` × AOV × nº de clientes do cohort |
| `margin` | receita × margem de contribuição % − (CAC × clientes) — **o CAC entra só no mês 0** |
| `total_revenue` | acumulado |
| **`total_margin`** | acumulado. **É a coluna de decisão de escala** — mostra o mês em que o cohort cruza pra positivo. |

**Decay factor.** Com a série real em mãos (Lifetimely é a fonte mais precisa; Triple Whale manual serve), calcule o decaimento médio entre meses consecutivos e use-o pra estender a curva nos meses sem dado. A referência de mercado é **~0,8**: de 100 clientes adquiridos, ~15 voltam no mês 1, ~12 no mês 2, ~11 no mês 3. Grave `decay_source` como `calculated` (série real) ou `assumed` (referência) — nunca deixe ambíguo qual dos dois foi usado.

**Calibragem.** Ajuste a linha de retorno basal até o número de recorrentes do modelo bater com o real de cada mês fechado. Repita a cada mês fechado até ter **3 a 5 meses de dados reais**; depois o decay estabiliza. Uma vez calibrada, **não mexa** na curva de LTV — revise a cada ~6 meses com dados novos. Quanto mais tempo o modelo roda, mais preciso fica.

**Aviso de sensibilidade — obrigatório no relatório:** um erro de 5% no cohort inverte o resultado. No exemplo de referência, a diferença entre acertar e errar 5% é sair de +US$ 157k pra −US$ 257k. Enquanto o cohort não estiver calibrado com 3+ meses reais, **modele o payback no mês 2 em vez do 3** — 30 dias de folga tornam a conta quase impossível de perder.

**Marca nova, sem cohort nenhum:** não invente curva. Rode o Modo B só nos blocos que os dados sustentam, marque `cohorts.calibrated: false`, e diga no relatório que a decisão de escala baseada em LTV fica travada até 3 meses fechados.

**LTV ≠ retenção.** Retenção é gente ficando; LTV é dólares gerados. Modele dólares: retenção boa com ticket baixo perde de retenção mediana com AOV alto.

**Pico de churn no dia ~45** — a maior parte do cancelamento acontece num único momento, tipicamente quando o produto chegou, foi testado e a decisão foi tomada. É o ponto que a skill 13 ataca primeiro; esta skill entrega o número que prova onde ele está.

### ETAPA 9 — [Modo B] Payback, first-order profitability e teto de escala

**Checagem de first-order profitability:**

```
cac_max_first_order = margem de contribuição do 1º pedido (antes do CAC)
first_order_profitable = (cac_real < cac_max_first_order)
```

Exemplo de leitura: AOV US$ 74 com COGS 20% (US$ 14) → margem US$ 58 → CAC máximo US$ 58. CAC real de US$ 48-49 ⇒ **lucrativo no primeiro pedido** ⇒ a estratégia correta é **escalar spend até chegar perto do zero a zero no primeiro pedido**, porque o LTV paga o resto. Marca lucrativa no primeiro pedido que não escala está deixando dinheiro na mesa.

**Janela de payback.** A referência é **90 dias** (LTV de 3 meses). Quem tem capital e paciência otimiza pra 12 meses; quem está calibrando o cohort usa 60 dias por segurança. Publique `payback_window_days_measured` a partir da coluna `total_margin` da ETAPA 8: é o mês em que o acumulado cruza zero.

> **Perder no primeiro pedido é decisão, não acidente.** É racional perder ~US$ 20 de margem de contribuição no 1º pedido se em ~3 meses o cohort devolve US$ 30+. As duas condições: LTV **medido** (não estimado) e caixa que aguenta a janela. Sem as duas, o gate da 04 (margem por pedido) continua valendo integralmente — e para membro em `starter` ou `validating` ele continua valendo de qualquer forma.

**Taxa de aumento do CAC e teto de escala.** O CAC não sobe proporcionalmente ao spend, mas sobe. A referência de forecast é **4:1 — a cada 5% de aumento de spend, ~1% de aumento de CAC**. Com histórico suficiente, calcule a taxa real por US$ 1.000 de spend adicional a partir dos meses fechados e use-a no lugar da referência.

**Detecção do teto:** projete o resultado operacional em faixas crescentes de spend. O ponto em que ele **para de subir e começa a cair** é o `scale_ceiling_monthly_spend` — o plateau. Escrito de forma acionável: *"não passar de US$ X/mês de spend até o CAC melhorar"*. É o número que a skill 12 precisa antes de autorizar escala agressiva.

### ETAPA 10 — [Modo B] Ciclo de conversão de caixa (o stack de float)

Se o cliente te paga antes de você pagar as contas, dá pra escalar sem sangrar caixa. O stack, em camadas:

| Camada | O que é | Prazo |
|---|---|---|
| 1 — Faturamento da Meta | Cobrança mensal por fatura em vez de cobrança no cartão a cada gasto. Fatura mensal + prazo de graça ≈ **net 45** (modele com 44 por segurança) | ~45 dias |
| 2 — Serviço de pagamento de boletos | Pagar com cartão uma fatura que não aceita cartão (Melio, Bill.com, Plastiq). Custo ~2,5-2,9% | — |
| 3 — Cartão de prazo longo | Cartão de cobrança com **net 60** e ~1,5% de crédito de fatura de volta | +60 dias |
| **Total** | | **~105 dias de float** |

Custo líquido do stack: taxa de ~2,9% menos ~1,5% de volta ≈ **1,4% por 105 dias** — na prática, o crédito mais barato disponível pra uma operação de ecommerce. É o que permite ser negativo na aquisição e na primeira recompra e pagar a fatura com o dinheiro da terceira.

**Efeito prático no modelo:** com o stack ativo, o ad spend sai do cálculo de necessidade de caixa de 90 dias da ETAPA 6 — ele só deixa a conta no dia ~105. Recalcule `cash_needed_90d` com e sem o stack e mostre as duas linhas; a diferença entre elas costuma ser o que separa "não dá pra escalar" de "dá".

**Extensão ao fornecedor:** pagar a fábrica pelo mesmo caminho, ou negociar prazo direto, alinha o desembolso de COGS ao mesmo ciclo. Essa é a ponte com a operação de suprimento.

**Guard-rails (repetir no relatório, não resumir):** nunca escalar dívida mais rápido que a capacidade de entrega; rodar o stress test da ETAPA 12 **antes** de alavancar; saber a data exata de cada saída de caixa; não confiar em conta de pontos sem calcular; **float não conserta oferta quebrada**; não financiar caos operacional.

### ETAPA 11 — [Modo B] Banking sheet semanal e notas mensais

**Banking sheet** — o pulso do caixa real, e o único artefato desta skill que vira ritual.

- **Estrutura:** linhas = dias do mês. Colunas = entrada de caixa (repasse do processador, outras entradas) e, em negativo, despesa de negócio, folha, ad spend, investimento, retirada de sócio, despesa pessoal. Fecha com **fluxo líquido por dia, por semana e por mês**.
- **Ritual:** uma vez por semana (~45 min), abrir **todas** as contas e cartões e lançar transação por transação do período.
- **Regra:** transferência entre contas próprias **não conta** — só dinheiro novo entrando ou saindo de verdade (a taxa da transferência, sim).
- **Por que fazer você mesmo pelo menos no começo:** é assim que se pega cobrança estranha e assinatura esquecida que nenhum relatório agregado mostra.
- A skill salva o template em `banking-sheet.csv` com os cabeçalhos e as fórmulas de fechamento descritas, pronto pra abrir em planilha.

**Notas mensais obrigatórias.** Todo mês fora da curva ganha uma linha explicando **por quê**: ruptura de estoque, entrada de assinatura, promoção no site inteiro, conta de anúncio suspensa, sazonalidade, teste de oferta que mudou o CAC. Sem essas notas, o histórico vira ruído e a calibragem do cohort passa a corrigir o modelo pelo motivo errado. Grave em `monthly_notes[]` — mês, evento, efeito no número.

**Camada contábil.** O modelo desta skill é a camada de estratégia; ele assume que existe uma camada de escrituração (todas as transações categorizadas) e uma de relatórios (as três demonstrações). Se o membro não tem nem a primeira, diga isso como pendência com efeito prático — *"sem transações categorizadas, os números aqui valem como direção, não como fechamento"* — sem virar consultoria contábil.

---

**A partir daqui, os dois modos voltam a rodar juntos.**

### ETAPA 12 — Stress test padrão

Três cenários, sempre os mesmos, sempre rodados antes de qualquer recomendação de aumentar spend ou alavancar caixa:

| Cenário | Ajuste | O que ele testa |
|---|---|---|
| **CAC +20%** | multiplique o CAC real por 1,2 | leilão piorando, fadiga de criativo, CPM de temporada |
| **LTV −20%** | corte a curva de cohort em 20% | churn pior que o modelado, take rate de assinatura caindo |
| **COGS +5 pontos** | some 5 pontos percentuais ao COGS | tarifa, frete, câmbio, taxa de defeito |

Para cada um, reporte margem de contribuição, resultado operacional (quando os fixos existirem) e um veredito binário **`survives`**. No Modo B, acrescente dois cenários de caixa antes de alavancar float: **reembolso +2 pontos** e **repasse do processador atrasado 7-14 dias**.

Se **qualquer** cenário derrubar o resultado operacional abaixo de zero, a recomendação de escalar sai com esse alerta em destaque — ele não some do relatório.

### ETAPA 13 — Benchmarks e veredito

Compare os números do membro contra as faixas de referência do canal direto ao consumidor (DTC). O que importa é a **tendência ao longo dos meses**, não o valor absoluto de um mês isolado.

| Indicador | Referência | Leitura |
|---|---|---|
| Margem bruta | **~70%** no canal direto ao consumidor | beleza tende a mais, vestuário a menos |
| Margem de contribuição | **10-20%** pra marca sem investidor | marca com aporte pode operar negativa de propósito pra escalar |
| Custos fixos | **abaixo de 10%** da receita | acima disso, o fixo come a escala antes de ela acontecer |
| COGS | **até 30%** como teto de longo prazo | acima, subir preço ou renegociar |
| Resultado operacional | acima de zero | depende do estágio e de haver aporte |

**Four Quarter Accounting** — a repartição de referência de um resultado mensal saudável: **25% COGS / 25% custo fixo / 25% custo de aquisição / 25% resultado**. Mostre a repartição real do membro ao lado dela. Não é regra rígida; é o jeito mais rápido de ver qual quarto está estourado.

**Exceção legítima de COGS alto:** COGS de 50-67% funciona quando o AOV é alto e a **margem de contribuição absoluta** é grande. Produto de US$ 3.000 com US$ 2.000 de margem por venda tem economia melhor que produto de US$ 30 com 70% de margem. Julgue pela margem em dinheiro por pedido, não só pela porcentagem.

**Veredito.** Feche com uma leitura em linguagem direta: a operação cobre os fixos hoje, quanto falta pra cobrir, e **qual alavanca única** move mais o resultado. Uma alavanca, não quatro.

**Memo de decisão (formato WAFM).** Quando o modelo produzir uma decisão que custa dinheiro — subir spend aceitando ROAS menor, cortar um custo fixo, entrar no stack de float, mudar preço —, feche o relatório com um memo curto de quatro blocos: **Por quê** (a dor ou oportunidade agora, com o número específico), **O quê** (a definição precisa da decisão), **Como** (a mecânica, os recursos e o prazo) e **Agora/Depois** (a ação, o dono e a data). Especificidade impiedosa: "as vendas caíram" não serve; "a receita caiu de US$ 127k pra US$ 98k em 30 dias, −23%" serve. Uma página, no máximo duas.

### ETAPA 14 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Nenhum número rotulado "lucro" sem custo fixo subtraído — no `.md`, no `.html` e no `dados.json`.
2. `monthly_model.operating_income` é `null` sempre que `fixed_costs_monthly` for `null`.
3. `cac_basis` é `shopify_new_customer` em todo cálculo de aquisição; nenhum CPA de plataforma entrou como CAC.
4. `roas_spiral.cut_spend_recommendation_allowed` é `false` sempre que os fixos forem desconhecidos.
5. `breakeven_roas_with_fixed` é maior que `breakeven_roas_variable_only` sempre que houver custo fixo positivo (se não for, a conta está errada).
6. Nenhum dos três campos que não se estima foi preenchido por estimativa; todos os ausentes estão em `pending_inputs[]`.
7. First order e repeat order aparecem em blocos separados, nunca somados numa média.
8. No Modo B: `cohorts.decay_source` declara explicitamente `calculated` ou `assumed`.
9. No Modo B com `cohorts.calibrated: false`: o payback foi modelado com a folga de 30 dias e isso está dito.
10. Os três cenários de stress test rodaram e cada um tem `survives` preenchido.
11. `runway_months` existe sempre que houver caixa disponível informado.
12. O relatório contém só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa (rule `report-only-results.md`).

## Output Schema — `15-finance-engine/finance-engine.md` + `15-finance-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills 04, 10, 11, 12 e 13.

```json
{
  "finance_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "currency": "USD",
  "mode": "A_plan | B_measure",
  "mode_reason": "sem mês fechado com ad spend e clientes novos do Shopify",
  "closed_months_available": 0,
  "inputs": {
    "aov_first_order": 118.00,
    "aov_repeat_order": 97.00,
    "aov_blended": 108.00,
    "orders_monthly": 0,
    "cogs_breakdown_source": "04-offer-builder/dados.json",
    "variable_cost_stack": {
      "product_delivered": 18.00,
      "shipping_to_customer": 6.50,
      "pick_pack": 2.50,
      "payment_processing": 3.50,
      "taxes_and_duties": 1.50,
      "subscription_app_fee": 0.90,
      "agency_fee_variable": 0.00,
      "refund_chargeback_provision": 2.10
    },
    "fixed_costs_monthly": null,
    "fixed_costs_source": "member | manifest | 04-offer-builder | unknown",
    "fixed_costs_breakdown": {},
    "ad_spend_monthly": null,
    "new_customers_period": null,
    "period_days": 30,
    "cac_real": null,
    "cac_basis": "shopify_new_customer",
    "returning_customer_pct": null,
    "cash_available": null,
    "payout_lag_days": null,
    "payout_lag_source": "member | conservative_new_store_default"
  },
  "monthly_model": {
    "revenue": 0,
    "cogs_fully_loaded": 0,
    "gross_profit": 0,
    "gross_margin_pct": 0,
    "variable_costs_total": 0,
    "contribution_margin": 0,
    "contribution_margin_pct": 0,
    "fixed_costs_monthly": null,
    "operating_income": null,
    "operating_income_status": "not_computable_fixed_costs_missing | computed",
    "gross_margin_needed_to_exist": null,
    "revenue_at_gross_margin_to_exist": null,
    "revenue_to_cover_fixed": null,
    "fixed_cost_coverage_ratio": null
  },
  "first_vs_repeat": {
    "first_order": { "aov": 118.00, "variable_costs_total": 0, "contribution_margin": 0, "contribution_margin_pct": 0 },
    "repeat_order": { "aov": 97.00, "variable_costs_total": 0, "contribution_margin": 0, "contribution_margin_pct": 0 },
    "note": "o primeiro pedido carrega o CAC inteiro e os fees atrelados a spend; a recompra não carrega nenhum dos dois"
  },
  "cac": {
    "cac_real": null,
    "cac_floor_reference_usd": [15, 25],
    "cac_max_first_order": 72.00,
    "target_cpa_from_04": { "primary_2x": 36.00, "primary_3x": 24.00 },
    "target_reachable_vs_floor": "yes | no | unknown",
    "first_order_profitable": null,
    "aov_supports_paid_traffic": true,
    "barometer_order_of_attack": ["cac", "ltv", "cogs", "aov"]
  },
  "roas_spiral": {
    "margin_rate": 0.61,
    "breakeven_roas_variable_only": 1.64,
    "breakeven_roas_with_fixed": null,
    "current_roas": null,
    "current_ad_spend_monthly": null,
    "spend_to_breakeven_with_fixed": null,
    "roas_above_variable_breakeven": null,
    "cut_spend_recommendation_allowed": false,
    "verdict": "blocked_pending_fixed_costs | covers_fixed_costs | scale_up_accept_lower_roas | cut_spend_below_variable_breakeven",
    "explanation": "frase em report_language explicando a decisão com os números do membro"
  },
  "cash": {
    "days_covered_target": 90,
    "cash_needed_90d": null,
    "cash_needed_90d_with_float_stack": null,
    "cash_available": null,
    "runway_months": null,
    "float_stack": {
      "active": false,
      "invoicing_net_days": null,
      "bill_pay_fee_pct": null,
      "charge_card_net_days": null,
      "statement_credit_pct": null,
      "total_float_days": null,
      "net_cost_pct": null,
      "cash_out_date": null
    },
    "guardrails_acknowledged": [
      "cash_out_date_known",
      "float_does_not_fix_broken_offer",
      "debt_not_faster_than_fulfillment",
      "no_financing_operational_chaos"
    ],
    "verdict": "..."
  },
  "levers": {
    "baseline": { "aov": 0, "cac": null, "ad_spend_monthly": null, "returning_pct": null },
    "simulations": [
      { "lever": "aov | cac | ad_spend | returning_pct", "from": 0, "to": 0,
        "contribution_margin_delta": 0, "operating_income_delta": null, "rank": 1 }
    ],
    "highest_impact_lever": null
  },
  "cohorts": {
    "source": "lifetimely | triple_whale | shopify_manual | member_pasted | none",
    "aov_month_0": null,
    "ltv_pct_by_month": [],
    "decay_factor": null,
    "decay_source": "calculated | assumed",
    "months_of_actuals": 0,
    "calibrated": false,
    "revenue_by_month": [],
    "margin_by_month": [],
    "total_margin_by_month": [],
    "crossover_month": null,
    "churn_spike_day": null,
    "sensitivity_note": "erro de 5% no cohort pode inverter o sinal do resultado; enquanto não calibrado, payback é modelado no mês 2"
  },
  "payback": {
    "window_days_target": 90,
    "payback_window_days_measured": null,
    "modeled_with_safety_margin": true,
    "cac_increase_ratio_reference": "4:1",
    "cac_increase_per_1k_spend": null,
    "scale_ceiling_monthly_spend": null,
    "scale_ceiling_note": null
  },
  "banking_sheet": {
    "cadence": "weekly",
    "columns": ["date", "cash_in", "business_expense", "payroll", "ad_spend", "investment", "partner_draw", "personal_expense", "net_cash_flow"],
    "template_path": "15-finance-engine/banking-sheet.csv",
    "last_reconciled": null
  },
  "stress_test": [
    { "scenario": "cac_plus_20pct", "contribution_margin": 0, "operating_income": null, "survives": null },
    { "scenario": "ltv_minus_20pct", "contribution_margin": 0, "operating_income": null, "survives": null },
    { "scenario": "cogs_plus_5pts", "contribution_margin": 0, "operating_income": null, "survives": null }
  ],
  "benchmarks": {
    "gross_margin_pct": { "actual": 0, "reference": 70, "status": "ok | below | above | unknown" },
    "contribution_margin_pct": { "actual": 0, "reference": "10-20", "status": "..." },
    "fixed_costs_pct_of_revenue": { "actual": null, "reference": "<10", "status": "unknown" },
    "cogs_pct_of_revenue": { "actual": 0, "reference": "<=30", "status": "..." },
    "four_quarter_accounting": { "cogs_pct": 0, "fixed_costs_pct": null, "acquisition_pct": 0, "operating_result_pct": null }
  },
  "monthly_notes": [
    { "month": "2026-08", "event": "ruptura de estoque", "effect": "spend cortado 12 dias; CAC do mês não é comparável" }
  ],
  "decision_memo": {
    "why": null, "what": null, "how": null, "now_next": null
  },
  "pending_inputs": [],
  "handoff": {
    "for_skill_11": ["roas_spiral.breakeven_roas_with_fixed", "roas_spiral.cut_spend_recommendation_allowed", "roas_spiral.verdict", "roas_spiral.spend_to_breakeven_with_fixed"],
    "for_skill_12": ["cash.cash_needed_90d", "cash.float_stack.total_float_days", "cash.runway_months", "monthly_model.fixed_costs_monthly", "payback.scale_ceiling_monthly_spend", "roas_spiral.cut_spend_recommendation_allowed"],
    "for_skill_04": ["monthly_model.fixed_costs_monthly", "payback.payback_window_days_measured", "monthly_model.contribution_margin_pct", "cash.runway_months"],
    "for_skill_13": ["cohorts.ltv_pct_by_month", "cohorts.decay_factor", "cohorts.crossover_month", "cohorts.churn_spike_day"],
    "for_skill_10": ["cac.cac_floor_reference_usd", "cac.cac_max_first_order", "cac.target_reachable_vs_floor"]
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo são ILUSTRATIVOS e independentes entre si** — mostram o formato de cada campo, não compõem um caso econômico coerente. Não re-derive um campo a partir de outro usando os valores do exemplo; as fórmulas canônicas estão nas ETAPAs 2, 5, 6 e 9.

**Campos que a skill NUNCA preenche por estimativa:** `inputs.fixed_costs_monthly`, `inputs.cac_real` e `inputs.new_customers_period`. Faltando qualquer um, o campo fica `null`, entra em `pending_inputs[]`, e todo bloco derivado dele fica marcado como não calculável — nunca preenchido com plausível. `cohorts.ltv_pct_by_month` segue a mesma regra: sem série real, `decay_source: "assumed"` e `calibrated: false`, declarados.

**Nomenclatura (cânone §1):** nenhum campo deste schema chama-se "profit". `contribution_margin` é margem de contribuição; `operating_income` é o único que pode ser chamado de lucro, e é `null` enquanto `fixed_costs_monthly` for `null`.

**Se `15-finance-engine/dados.json` falhar as checagens da ETAPA 14, NÃO salvar o `.md`.**

## Contrato de leitura (quem lê o quê)

Esta skill é a **produtora** dos números abaixo. As consumidoras leem por estes caminhos exatos e não recalculam com fórmula própria.

| Skill | Campo que passa a ler | O que muda |
|---|---|---|
| **11** ad-analysis | `roas_spiral.breakeven_roas_with_fixed`, `roas_spiral.cut_spend_recommendation_allowed`, `roas_spiral.verdict`, `roas_spiral.spend_to_breakeven_with_fixed` | Hoje a 11 lê `04-offer-builder/dados.json.budget_viability.fixed_costs_monthly` e bloqueia o corte quando é `null`. Com a 15 rodada, a decisão deixa de ser bloqueio e vira número: sobe, segura ou corta, com o spend de breakeven calculado. |
| **12** scale-engine | `cash.cash_needed_90d`, `cash.float_stack.total_float_days`, `cash.runway_months`, `monthly_model.fixed_costs_monthly`, `payback.scale_ceiling_monthly_spend`, `roas_spiral.cut_spend_recommendation_allowed` | A ETAPA 6 da 12 estima o gap de caixa sozinha e a ETAPA 7 projeta 30/60/90 sem camada de custo fixo. Com estes campos, a projeção passa a ter resultado operacional, e o teto de escala vira número em vez de sensação. |
| **04** offer-builder | `monthly_model.fixed_costs_monthly`, `monthly_model.contribution_margin_pct`, `payback.payback_window_days_measured`, `cash.runway_months` | `budget_viability.result_after_fixed_monthly` deixa de ser `null`. E para membro em `scaling` com LTV **medido**, `payback_window_days_measured ≤ 90` é a alternativa ao gate de margem mínima por pedido — com `cash.runway_months` fechando a segunda perna da alternativa (o caixa aguenta a janela: `runway_months × 30 ≥ payback_window_days_measured`). |
| **13** retention-engine | `cohorts.ltv_pct_by_month`, `cohorts.decay_factor`, `cohorts.crossover_month`, `cohorts.churn_spike_day` | Os flows deixam de mirar LTV estimado e passam a mirar o mês real de cruzamento e o pico de churn medido. |
| **10** ad-strategy | `cac.cac_floor_reference_usd`, `cac.cac_max_first_order`, `cac.target_reachable_vs_floor` | O CPA-alvo da campanha passa por checagem contra o piso físico antes de virar setpoint. |

Quando o `15-finance-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — a leitura é aditiva, nunca pré-requisito.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `finance-engine.md` → `finance-engine.html`). **Isentos** (arquivos operacionais — rule 6b): `dados.json` e `banking-sheet.csv`. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, **logo SVG do Aura na topbar copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**, componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/15-finance-engine/` antes de salvar.

Outputs em `workspace/[produto]/15-finance-engine/`:

- **`finance-engine.md`** contendo, nesta ordem:
  1. Modelo mensal completo, com `gross_margin_needed_to_exist` em destaque (ETAPA 2)
  2. Margem de contribuição e ponto de cobertura do fixo, com first order e repeat order em blocos separados (ETAPA 3)
  3. Piso de CAC, CAC máximo do primeiro pedido e viabilidade do CPA-alvo (ETAPA 4)
  4. **A espiral do ROAS com os números do membro** — o breakeven com fixo, o spend de breakeven e o veredito (ETAPA 5)
  5. Necessidade de caixa em 90 dias, runway e guard-rails (ETAPA 6)
  6. **[Modo B]** As 4 alavancas simuladas e ranqueadas (ETAPA 7)
  7. **[Modo B]** Tabela de cohort com decay, coluna de margem acumulada e mês de cruzamento (ETAPA 8)
  8. **[Modo B]** Payback, first-order profitability e teto de escala (ETAPA 9)
  9. **[Modo B]** Stack de float e o efeito dele na necessidade de caixa (ETAPA 10)
  10. **[Modo B]** Banking sheet e notas mensais (ETAPA 11)
  11. Stress test (ETAPA 12)
  12. Benchmarks, Four Quarter Accounting e veredito, mais o memo de decisão quando houver decisão que custa dinheiro (ETAPA 13)
  13. Pendências: o que falta e o que destrava — sem narrar as tentativas

  No Modo A, os itens 6 a 10 simplesmente não aparecem. O doc segue `.claude/rules/report-only-results.md`: só o resultado, sem descrever o que não contém.

- **`banking-sheet.csv`** (só no Modo B) — cabeçalhos das colunas da ETAPA 11, uma linha por dia do mês corrente, coluna de fluxo líquido pronta.

- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:

- Adicionar `15-finance-engine` em `skills_completed`
- **Gravar `manifest.fixed_costs_monthly`** quando o membro informar. É o campo canônico compartilhado com as skills 04, 11 e 12 (descrito no `manifest-schema.json`). Se já existir e o membro der outro valor, o novo prevalece e a mudança é avisada em uma linha.
- Gravar `manifest.finance` = `{ mode, breakeven_roas_with_fixed, cut_spend_recommendation_allowed, cash_needed_90d, runway_months, payback_window_days_measured, scale_ceiling_monthly_spend, checked_at }` — o resumo que as outras skills leem sem abrir o `dados.json` inteiro
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `ABRIR-AQUI.html`, onde `<slug>` é o `product_slug`)

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`). O modelo melhora a cada mês fechado — diga isso.

**Modo A (planejar), com os fixos informados:**
"Modelo financeiro montado. Sua margem de contribuição é **[X]%** — é o que sobra depois de todos os custos variáveis. Com **US$ [F]/mês de custo fixo**, o negócio empata em **US$ [R] de receita mensal**, e precisa gerar **US$ [G] de lucro bruto por mês só pra existir**.
Seu CAC máximo no primeiro pedido é **US$ [C]**, e o piso físico do Meta fica entre US$ 15 e 25 — [o CPA-alvo da sua oferta cabe nessa faixa / o CPA-alvo está abaixo do piso, e isso é problema de AOV, não de mídia].
Pra rodar 90 dias você precisa de **US$ [K] em caixa**. Com o que você tem hoje, isso dá **[N] meses de fôlego**.
Revisa os números e me diz o que não bate. Quando tiver o primeiro mês fechado (ad spend + clientes novos do Shopify), diga **'finanças'** de novo — aí eu meço em vez de projetar: alavancas, cohorts, payback e ciclo de caixa."

**Modo A, sem os fixos:**
"Modelo montado até onde os dados deixam. Sua margem de contribuição é **US$ [X]/mês** — mas **sem os seus custos fixos eu não posso dizer se há lucro**, e não vou chamar de lucro um número que não subtraiu custo fixo.
Me passa o total que você paga por mês mesmo vendendo zero (time, apps, ferramentas, aluguel, contabilidade) e eu fecho: ponto de equilíbrio, resultado operacional, caixa pra 90 dias e o ROAS de breakeven real. É o número que também destrava as decisões de corte de spend nas análises de ads."

**Modo B (medir):**
"Números medidos, não projetados. CAC real de **US$ [C]** (clientes novos do Shopify, não CPA do Meta). Margem de contribuição de **[X]%**, [cobrindo / não cobrindo] os **US$ [F]** de custo fixo.
**A alavanca que mais move seu resultado é [alavanca]:** [de A pra B] muda o mês em **US$ [D]**.
Seu cohort cruza pra positivo no **mês [M]**, com payback de **[P] dias**. [Se não calibrado: 'Com [N] meses de dados, essa curva ainda não estabilizou — modelei o payback com 30 dias de folga. Repete comigo a cada mês fechado até 3 meses e ela trava.']
**Sobre ROAS:** seu breakeven com o custo fixo dentro é **[Y]×** ao nível de spend atual — e ele **cai** conforme o spend sobe. [Veredito: se o ROAS cair, a resposta [não] é cortar; o número que fecha a conta é subir spend até US$ [S]/mês aceitando ROAS ~[Z].]
Roda o banking sheet uma vez por semana e me volta no próximo mês fechado — a cada calibragem o modelo fica mais preciso."

**Se faltar input crítico (qualquer modo):**
"Faltam [N] número(s) que eu não posso estimar sem tornar o modelo falso: [listar]. Cada um destrava: [o que destrava]. Me passa e eu fecho a conta — chutar custo fixo ou CAC inverte a recomendação de spend, que é exatamente o erro que este modelo existe pra evitar."
