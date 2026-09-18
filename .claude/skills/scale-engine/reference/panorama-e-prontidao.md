# Scale Engine · Referência: Panorama atual, estágio de escala e prontidão (ETAPAs 1, 2 e 3)

> O que pré-popular dos artefatos e o que perguntar numa mensagem só (ETAPA 1), a tabela de sub-fases de spend e onde ela vive (ETAPA 2) e a tabela completa de pré-requisitos com o critério e a ação quando falha, mais os frameworks de prontidão e o teste de troca pra 7DC-only (ETAPA 3). Abra nas ETAPAs 1 a 3.

### ETAPA 1 — Receber Panorama Atual

Primeiro, pré-popule dos artefatos: `ad-analysis/dados.json` (spend diário, CPA médio, ROAS médio, a classificação por criativo nas 4 classes do cânone §2 — ou `winners[]` a reclassificar — + `champions[]` com Post ID, se houver) + `offer-builder/dados.json` (breakeven CPA/ROAS) + `manifest.psm_real`. **AOV real:** leia do `finance-engine/dados.json` (modelo mensal) quando existir; senão, pergunte ao membro — a `ad-analysis` não grava AOV. **CPM atual da conta:** pergunte ao membro (Ads Manager) — a `ad-analysis` grava só a tendência (`health_signals.cpm_trend`), não o valor. Só pergunte ao membro o que NÃO está nos artefatos.

Campos **necessários pra esta skill decidir** que os artefatos nem sempre cobrem — peça junto com o resto, numa mensagem só, apenas os que faltarem:

- **Custo fixo mensal** (time, apps, ferramentas, aluguel) — sem ele, o gate de corte por ROAS fica bloqueado (ver "Custo fixo antes de cortar spend"). **Não pergunte se já está gravado:** `finance-engine/dados.json.monthly_model.fixed_costs_monthly` e `manifest.fixed_costs_monthly` são a mesma verdade — existindo qualquer um dos dois, só confirme ("seus custos fixos ainda são US$ X/mês?").
- **Share de purchases em 7-day click** — é o gate click-based do Scaling Protocol. **Não pergunte se já está gravado:** a `ad-analysis` grava `manifest.click_based_purchase_share` a cada análise — existindo, use direto (confirmando só se a última análise não for recente). Sem o campo (análise antiga da `ad-analysis`, produto legado), pergunte como hoje (Ads Manager → janela de atribuição). O mesmo recorte serve à segunda porta do gate: o ROAS calculado só com purchases click-based.
- **Fuso horário do ad account** — define quando é a "meia-noite" da regra de reset.
- **Caixa disponível hoje** — entra no check de float da ETAPA 6. Se a `finance-engine` rodou, `cash.cash_needed_90d` e `cash.runway_months` já respondem isso e a pergunta vira confirmação.

Se algo faltar (ex: cash disponível pra surf, que não vive em nenhum JSON), peça em UMA única mensagem só os campos faltantes:

"Confirmando o panorama: [valores lidos do ad-analysis/dados.json + breakeven do `offer-builder`]. Me falta só [campo(s) ausente(s)]."

Se `ad-analysis/dados.json` não existir, aí sim peça tudo: "Me dá o panorama atual: quanto gasta por dia, CPA médio, CPM médio, ROAS, AOV, e — por ad — **quanto cada um gastou** e **qual o CPA/ROAS dele comparado ao da campanha** (é isso que separa um breakthrough de um ad que só bate o KPI numa amostra pequena). E o breakeven CPA do produto." Não re-explique campos já preenchidos.

### ETAPA 2 — Classificar Estágio de Escala

Stage canônico vem do `manifest.stage` (`starter` | `validating` | `scaling`) — detecção pela rule `member-stage-awareness.md`. O stage dita **qual escola de escala recomendar como default** e a agressividade. A sub-fase de spend abaixo é DIAGNÓSTICO (informa intensidade), nunca substitui o stage canônico.

| Spend diário | Sub-fase de escala | Leitura |
|---|---|---|
| < $100/dia | Teste | Ainda achando breakthrough. Escala = mais criativo, não mais budget. |
| $100-500/dia | Tração | Breakthrough frágil. Passo do protocolo (+20%) com mão leve, sem surf. |
| $500-1K/dia | Escala Inicial | Breakthrough estável. Passo do protocolo a cada 24h enquanto os dois gates seguram. |
| $1K-5K/dia | Escala Agressiva | Passo do protocolo + surf possível, atenção diária e reset da meia-noite obrigatório. |
| $5K+/dia | Otimização | Unit economics, múltiplas contas, omnichannel. |

A sub-fase vive em `scale_phase` no `scale-engine/dados.json` — **NUNCA** em `manifest.stage`.

### ETAPA 3 — Análise de Prontidão (Pré-Requisitos)

Antes de aumentar spend, validar se o sistema aguenta. Falhar em qualquer um = identificar gargalo e resolver ANTES de escalar.

**Frameworks de prontidão (rode antes de aprovar escala):**
- **Three Reasons Scale Breaks** (rode `three reasons scale breaks unit economics funnel imbalance cash constraints can we spend more tomorrow`) — escala quebra por 3 motivos: unit economics fraco, funnel desbalanceado, cash constraint. Cada pré-requisito abaixo mapeia num desses.
- **Would It Hold at 3X Budget? (Mental Model)** (rode `would it hold at 3X budget mental model low spend high ROAS statistically insignificant`) — criativo com pouco spend e ROAS alto pode ser ruído estatístico. É o mesmo raciocínio que o cânone §2 formaliza no `KPI winner`: aplique este teste mental antes de chamar qualquer coisa de breakthrough.
- **Scaling Click-Based Data Gate** (rode `scaling click-based data gate 60% purchases view-through attribution 7-day click 1-day view`) — se a maioria das conversões é view-through (não click-based), o sinal de escala é frágil. O gate tem **duas portas** (`ad-taxonomy` §5 — qualquer uma libera): **≥ 60% das purchases em 7-day click**, OU **o ROAS calculado só com purchases click-based já bate o KPI sozinho**. As duas vermelhas, não sobe.
- **Teste de troca pra 7DC-only** (rode `campanha duplicada 7-day click only view-through inflado email blast returning customers`) — o diagnóstico quando o gate reprova: trocar a atribuição pra 7-day click only numa campanha **DUPLICADA** (nunca na de controle) e comparar. Se o "desempenho" some sem a view-through, o sinal estava inflado (email blast, returning customers contados como conversão do ad) — conserta atribuição na `tracking-setup` antes de falar em escala.

| Pré-requisito | Critério | Se falhar |
|---|---|---|
| **Breakthrough provado** | ≥ 1 criativo classificado como `breakthrough` pelo cânone `ad-taxonomy` §2 (KPI do ad melhor que o KPI da campanha **e** puxa spend), estável por 3+ dias | **Volta pra `creative-engine`** (mais criativo). `KPI winner` e `spend winner` **não** substituem: o primeiro não provou nada em escala, o segundo pede iteração |
| **Gate click-based (duas portas)** | ≥ 60% das purchases em 7-day click **OU** ROAS só de purchases click-based batendo o KPI sozinho (`ad-taxonomy` §5 — qualquer porta libera). Share lido de `manifest.click_based_purchase_share` (a `ad-analysis` grava); sem o campo, o número que o membro trouxe na ETAPA 1 | Nas duas portas vermelhas, não escala com sinal view-through. Rodar o teste de troca 7DC-only (framework acima), revisar tracking na `tracking-setup` e re-medir antes de subir budget |
| **PSM real ≥ teórico, em base válida** | `manifest.psm_real` não está > 20% abaixo do `psm_theoretical` **e** `manifest.psm_real_basis` é `"shopify_new_customer"` (campo ausente = proxy) | Abaixo do teórico → ajustar oferta (AOV, garantia, stack) ANTES de escalar. Base `platform_cpa_proxy` ou ausente → número declaradamente otimista, **não libera escala**: pedir o CAC real (ad spend ÷ clientes NOVOS do Shopify) e re-rodar a `ad-analysis` |
| **Margem por pedido saudável** | `manifest.margin_warning` ≠ `true` (a Skill `offer-builder` grava `true` quando a margem ponderada fica < $20/pedido) | Segurar a escala VERTICAL e alertar o membro: com margem apertada, cada dólar de CPA acima do alvo come uma fatia grande do lucro — revisar oferta/pricing na `offer-builder` antes de subir budget |
| **CPA estável ou melhorando** | Trend dos últimos 3-7 dias estável ou descendo | Diagnóstico de fadiga (skill `ad-analysis`) antes de escalar |
| **CPM saudável na conta** | CPM dentro da faixa normal pro nicho/conta | CPM muito alto = problema de CONTA, não de produto. Testar o breakthrough em outra conta (skill `ad-analysis`) antes de escalar |
| **Creative pipeline ativo** | Batch novo a cada 1-2 semanas no ritmo de escala | Recomendar Skill `creative-engine` — escala consome volume de criativo |
| **Pixel/CAPI health** | EMQ ≥ 6.0 (escala 0-10 do Events Manager), sem events perdidos | Fix técnico (skill `tracking-setup`) antes de escalar |
| **Cash flow pra COGS + spend** | Membro tem $ pra cobrir o gap entre spend (cobrado diário) e payout (Shopify 3-5 dias) | Ajustar pace de escala ao cash disponível (ver ETAPA 6) |
| **Volume do fornecedor confirmado** | `sourcing/dados.json` → `calendar.volume_confirmation_30_60_90` preenchido (a `sourcing` ETAPA 12 grava — existindo, use e NÃO re-pergunte) ou confirmação escrita equivalente informada pelo membro | Sem confirmação de volume, escalar contra ruptura de estoque é **risco declarado**: avisar e pedir a confirmação por escrito ao fornecedor (ou rodar a `sourcing` ETAPA 12, que fecha exatamente isso). Sourcing nunca rodou → pergunta de hoje, ao membro. Ponto de recompra operacional na ETAPA 6 |

Pra cada pré-requisito que falha, documente o bloqueio e recomende ação específica. **Breakthrough provado é eliminatório** — sem ele, a skill não monta plano de escala, manda de volta pra `creative-engine`. O membro que chega com um `KPI winner` bonito ouve isso explicitamente: o ad bate o KPI numa amostra pequena e não puxa spend, então não há o que escalar ainda.
