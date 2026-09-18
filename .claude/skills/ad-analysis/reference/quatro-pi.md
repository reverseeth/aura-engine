# Ad Analysis · Referência: Os 4 Pi's, Hook e Hold, PSM real e share em 7-day click (ETAPA 2, segunda parte)

> A leitura de Spend, Frequency, CPM e Cost per Result na ordem exata, os padrões de Hook rate e Hold rate que viram briefing, o cálculo do `psm_real` gravado pra `scale-engine` e o `click_based_purchase_share` do gate de escala. Abra depois do bloco Decision Thresholds.

#### Pi 1: SPEND

> Fundamento: **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) + **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`). Explicam por que o algoritmo concentra ou força spend e por que NÃO se desliga o top spender mesmo quando parece ineficiente.

"Quanto cada CONCEITO (ad set) puxou do budget da campanha, e quanto cada AD (criativo) puxou dentro do ad set dele?"

Observação-chave: **Meta distribui spend pra onde ele ACREDITA que está funcionando** — e sob CBO isso acontece em dois níveis. Primeiro o CBO reparte entre os ad sets: **o ad set que concentra gasto é o conceito que o algoritmo escolheu**, e essa é a leitura mais informativa do batch. Depois, dentro de cada ad set, o Meta reparte entre os 3 ads do pack; ali o `fair_share` de cada criativo é 1/N do spend daquele ad set (com o pack 3-2-2, 1/3). Se o ad A recebeu 3× o fair share e o ad B só 20% dele, o algoritmo tá "votando" que A é melhor (independente de CPA).

- **Ad com spend ≥ 2× o fair share** → Meta tá confiante nele. É **candidato** a `breakthrough` ou a `spend_winner` — quem decide qual é a comparação com o KPI da campanha no Pi 4, não este Pi.
- **Ad com spend < 50% do fair share após 72h** (com a entrega geral saudável) → Meta não tá confiante nele OU o ad não foi aprovado. Sozinho isso **não** classifica ninguém: se o ad bate o KPI da campanha, ele é `kpi_winner` (loser para decisão, mas o diagnóstico é "audiência pequena demais", não "criativo ruim"); se não bate e o `spend_share_7d` fica em ≤ 2%, é `loser`.
- **Registre `spend_share_7d` de cada ad aqui** (spend do ad ÷ spend da conta na janela de 7 dias). É esse número, e não o `fair_share`, que entra na classificação do bloco Decision Thresholds.

Se NENHUM ad gastou em 24-48h (entrega geral travada): verificar Ads Manager > Delivery insights + Review status — pode ser policy/review/conta, NÃO criativo. Pós-escala (Skill `scale-engine` criou múltiplas campanhas/ad sets), a mesma leitura de share se aplica um nível acima: campanha/ad set com spend muito abaixo do esperado = algoritmo sem confiança nela.

#### Pi 2: FREQUENCY (Sinaliza Posição no Funil)

> Fundamento das signatures: **Creative Diversity by Funnel Position (4Pi Signatures)** (rode `creative diversity funnel position 4Pi signature UGC VSL sprinters marathoners`). É de lá que vêm as bandas de freq diária ↔ posição no funil (TOF/MOF/BOF) e a leitura de sprinters vs marathoners.

**Regra base: a frequency lida aqui deve ser a frequency DIÁRIA** (freq do dia, não acumulada da vida toda do ad set). Frequency lifetime cresce indefinidamente e não diz nada sobre fadiga atual. Sempre puxe/compare a freq diária. As bandas abaixo são para freq DIÁRIA.

Aplicar as signatures (freq diária, lida POR AD):

- **Freq ~1.05** → **prospecting / TOF** (Top of Funnel) — novas impressões, cold traffic, ~1 impressão por pessoa/dia
- **Freq 1.1-1.4** → **MOF** (Middle) — starting to warm up
- **Freq 1.5-1.9** → **retargeting / BOF** (Bottom) — mesmas pessoas vendo várias vezes ao dia

Se os ads da campanha de teste (que é 100% prospecting broad) estão com freq diária bem acima de ~1.05 (puxando pra 1.5-1.9, comportamento de retargeting), o Meta está re-martelando a mesma audiência em vez de abrir TOF novo — sinal de saturação da entrega. Recomendação: adicionar conceito TOF-friendly (hook problem, angle curiosity) no próximo batch.

**Freq ~1.05 estável NÃO é anomalia aqui:** na estrutura broad da Skill `ad-strategy`, ~1.05 sustentada é o estado normal e desejado de uma campanha 100% prospecting — não dispare alerta por isso. O alerta de "Meta não consegue re-engajar" só se aplica quando existe camada de retargeting esperada (que o fluxo padrão não monta). O check que continua valendo em qualquer cenário: **CPM baixo + CTR muito baixo = criativo não ressoa** com a audiência.

#### Pi 3: CPM (Contexto Combinado com Freq)

**CPM isolado diz pouco. CPM + Freq diz muito:**

- **CPM alto (acima da média do nicho) + Freq diária alta (>1.5)** → Meta tá mandando pra audience cara (prime-time, premium placements) porque POUCA audience nova está disponível. Sinal de BOF / possível fadiga.
- **CPM alto + Freq diária baixa (~1.05)** → audience premium/cara mas fresca. Pode ser normal em nicho competitivo (skincare, finance, luxury).
- **CPM baixo + Freq alta** → Meta tá procurando impressões baratas com audience repetida. Frequência tá alta mas CPM não subiu = Meta não tá pagando caro pra forçar. Pode ser fadiga mas também pode ser só stabilidade.
- **CPM subindo no tempo** (comparar com análises anteriores se houver) → **possível fadiga**. Combinar com CTR falling pra confirmar.

**CPM também é sinal de saúde da CONTA (lente do playbook):** o mesmo produto/criativo pode dar CPM $30 numa conta e $100 noutra — o CPM diz tanto sobre a conta quanto sobre o criativo. Se o CPM está muito acima do esperado do nicho de forma generalizada (TODOS os ads caros, não só um criativo), suspeite da CONTA antes do produto. Antes de declarar o produto morto por economia ruim, marque `health_signals.account_cpm_suspect = true` e recomende **testar o mesmo criativo em outra conta de anúncio** (resiliência legítima: ter conta reserva ajuda aqui). Só mata o PRODUTO se ele não validar em conta nenhuma.

#### Pi 4: COST PER RESULT (O Que Realmente Importa)

A comparação que classifica é **CPA do AD vs. `campaign_cpa`** (ou ROAS do ad vs. `campaign_roas`), cruzada com `spend_share_7d` — as 4 classes do bloco **Decision Thresholds** no topo desta ETAPA. O `target` CPA da oferta (do `offer-builder/offer-builder.md`) continua sendo lido, mas como piso de rentabilidade e como base da régua de kill de conta nova, **não** como definição de winner:

- **KPI do ad melhor que o da campanha + puxa spend** → **`breakthrough`** (o único que vai pro diagnóstico "scale")
- **Puxa spend + KPI abaixo do da campanha** → **`spend_winner`** (iterar, não escalar)
- **KPI melhor que o da campanha + `spend_share_7d` < 10%** → **`kpi_winner`** (loser para decisão; ver o escape abaixo antes de descartar)
- **`spend_share_7d` ≤ 2% em 7 dias** → **`loser`** (gastou sem bater KPI mas puxando spend? é `spend_winner` acima, nunca loser — cânone §2)

**Escape antes de descartar um `kpi_winner`:** o ad pode ser ótimo pra uma audiência pequena demais. Antes de tratá-lo como peso morto, dá pra **forçar spend** — ad set próprio começando no que ele já gastava — para tirar a dúvida em ambiente controlado. Isso é decisão de estrutura, então a recomendação sai daqui e a execução é da skill `scale-engine`. O que **não** pode acontecer é ele entrar em `breakthroughs[]` sem ter provado que sustenta spend.

**Réguas de KILL (cânone §3, decisão operacional):**
- **Conta madura:** kill no nível do **ad set** após 7 dias sem spend e sem KPI. Marque `reason = "adset_7d_no_spend_no_kpi"`.
- **Conta nova:** ad que gastou **≥ 8× o `target` CPA sem purchase** → kill. Marque `ad_class = "loser"` com `reason = "kill_8x_target_cpa_no_purchase"`.
- **Ad novo overspendando:** **24-48h** de carência antes de qualquer decisão. Marque `reason = "awaiting_24_48h_grace"` e não classifique ainda.
- **Exceção:** se o criativo tem **2+ initiate-checkouts** no comecinho, NÃO mate ainda — o Meta tem sinal pra otimizar; deixa rodar mais um pouco. Classifique como NEEDS OPTIMIZATION.
- **CTR alto sem venda não salva** o criativo — mas também não o mata sozinho. A régua é a de cima.
- **Funil quebrado (cruzar com benchmarks ANTES de matar):** se o criativo gerou ATC/checkouts mas as taxas estão abaixo de **ATC→compra 20-25%** ou **checkout→compra 40-50%**, o bloqueio é página/checkout/oferta, NÃO o criativo. Ex: 3 checkouts e 0 venda → checkout→compra = 0%, muito abaixo dos 40-50% esperados → o ad fez o trabalho, a página falhou. **NÃO mate o criativo**; roteie pra `copy-engine`/`page-design` (página) ou `offer-builder` (oferta) e registre o gargalo de funil no diagnóstico.
- **Conta antes do produto:** se o CPM está fora do esperado do nicho de forma generalizada (ver Pi 3, `account_cpm_suspect`), trate como problema de CONTA — recomende re-testar em outra conta antes de matar o produto.

Contexto importante: **CPA de um ad isolado não é tudo**. "a campanha overall melhorou?". Se a campanha total está dentro do CPA target mesmo com 1-2 ads fora, a máquina tá OK. Otimiza os outliers, não destrua a campanha.

**Breakdown por placement (check rápido quando o CPA agregado está fora do target):** puxe insights com breakdown por placement (o MCP oficial expõe; no Ads Manager: Breakdown > Placement). Placement de CPM baixo mas conversão fraca — Threads (placement global desde jan/2026, ligado por default no Advantage+) e Audience Network são os suspeitos usuais — pode estar comendo spend sem vender. Só considere opt-out via manual placements como **exceção documentada depois desse dado**; nunca preventivamente (a tese de deixar o Meta distribuir continua certa).

#### Hook rate e Hold rate (ONDE o criativo falhou)

Os 4Pi dizem **que** um criativo falhou. Hook e Hold dizem **onde**. Sem os dois, "o criativo não funcionou" não é diagnóstico — é constatação, e não gera briefing pra `creative-engine`.

**Fórmulas** (cânone `.claude/lib/ad-taxonomy/README.md` §4):
```
Hook rate = 3-second video plays ÷ impressões
Hold rate = ThruPlays ÷ impressões
```
(ThruPlay = ≥ 15s, ou o vídeo inteiro se durar menos que isso.)

**Como obter:** no Ads Manager, Columns → Customize Columns → Create Custom Metric, uma coluna pra cada fórmula. Pelo MCP, os componentes (`impressions`, `video_3_sec_watched_actions`, `video_thruplay_watched_actions`) vêm no pull — calcule direto, não peça ao membro. Se o criativo é estático, os dois campos ficam `null` e o diagnóstico de abertura passa a ser CTR + tempo de leitura, não hook rate.

**Benchmarks:** as faixas de Hook (ok/bom/muito bom/excepcional) e Hold estão na tabela do cânone §4. Leia de lá; não replique a tabela aqui nem invente número intermediário.

**Leitura diagnóstica (é isto que vira briefing pra `creative-engine`):**

| Padrão | O que significa | Ação |
|---|---|---|
| **Hook baixo** | Problema de **abertura** — os 3 primeiros segundos não fisgam. O resto do vídeo nem foi visto, então não há informação sobre ele. | Reescrever o hook e retestar **o mesmo conceito** (iteração de uma variável só). Não descarte o conceito. |
| **Hook bom + Hold baixo** | A abertura fisgou, mas **a promessa não sustentou** — o vídeo entregou menos do que o hook prometeu, ou demorou pra entregar. | O hook está resolvido; o trabalho é o corpo do vídeo (ritmo, prova, mecanismo). |
| **Hook e Hold bons + CPA ruim** | O criativo prende atenção mas não converte — o problema está depois do vídeo. | Vá pra ETAPA 6B (funil/página) e pro 19-Point antes de culpar o criativo. |

**Ressalva obrigatória:** hook rate, hold rate, CTR e CPC são **métricas macias** — um ad com o dobro do CPC pode ter o mesmo ROAS, e ninguém paga boleto com hook rate. O uso correto é **diagnóstico de onde o criativo falhou**, **nunca** critério de kill nem de classificação. As classes continuam vindo do bloco Decision Thresholds; kill continua vindo das réguas do cânone §3.

Grave `hook_rate` e `hold_rate` por criativo no `dados.json` e no perf JSON do DNA (é o que preenche os campos `thumbstop_3s` / `hold_15s`, que até agora eram gravados vazios).

#### PSM real (gravado nesta análise — usado pela skill `scale-engine`)

Calcule `psm_real` pela fórmula canônica do bloco **Decision Thresholds**:
```
psm_real = LTV / (CAC_real + COGS)
```
- `CAC_real` = ad spend do período ÷ **clientes NOVOS** do período (Shopify, `new customer = TRUE`) — nunca o CPA de plataforma. Se a base for proxy, grave `psm_real_basis: "platform_cpa_proxy"` e trate o número como otimista.
- `COGS` = somatório de TODOS os campos de `offer.cogs_breakdown` (8 hoje; itere as chaves, não uma lista fixa — NÃO existe campo `cogs_total`)
- `LTV` = de `offer-builder/dados.json` (ou AOV do primeiro pedido se LTV ausente)

Este `psm_real` é gravado em `ad-analysis/dados.json` E em `manifest.psm_real`, junto com `psm_real_basis` (ver ETAPA de update do manifest). Skill `scale-engine` lê de `manifest.psm_real`, nunca recalcula — e compara contra o `psm_theoretical` da skill `offer-builder`, que usa a MESMA base (CAC). Thresholds de ação PSM: >1.3 agressivo · 1.1–1.3 steady (+5%) · 1.0–1.1 breakeven · <1.0 unprofitable.

#### Share de compras em 7-day click (gravado nesta análise — gate de escala da `scale-engine`)

Calcule, na janela de 7 dias e no nível da campanha:
```
click_based_purchase_share = purchases atribuídas em 7-day click ÷ purchases totais da janela
```
- **Como obter:** o breakdown de atribuição vem no pull do MCP (comparação de attribution settings); no Ads Manager: Columns → Compare attribution settings (7-day click vs 1-day view). No caminho manual, peça o número ao membro junto com os demais dados.
- **Grave em `dados.json` e em `manifest.click_based_purchase_share`.** É o número que a Skill `scale-engine` confere no gate click-based do cânone `.claude/lib/ad-taxonomy/README.md` §5 (escala só com ≥ 60% das purchases em 7-day click, OU com o ROAS calculado só das purchases click-based batendo o KPI sozinho). **NUNCA estimar** (regra do manifest-schema): se o breakdown não veio, NÃO grave o campo — o gate da `scale-engine` fica bloqueado até o número existir, e o relatório diz exatamente onde olhar pra destravar.
- **Se a share vier baixa** (view-through inflando o resultado — disparo de email e cliente recorrente são os suspeitos usuais), o teste nomeado da base pra tirar a prova é o **Teste de troca pra 7DC-only** (rode `campanha duplicada 7-day click only view-through inflado email blast returning customers`): duplicar a campanha rodando só com atribuição 7-day click e medir quanto do resultado era inflação. A recomendação sai daqui; a execução é decisão de estrutura (Skill `scale-engine`, com a `tracking-setup` na camada de atribuição).
