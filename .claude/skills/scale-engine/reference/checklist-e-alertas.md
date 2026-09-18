# Scale Engine · Referência: Checklist operacional semanal, sinais de alerta e a volta pra creative-engine (ETAPAs 9 e 10)

> A tabela do ritmo semanal e o monthly review (ETAPA 9), a régua única de frequency, os frameworks de recuo, o gate de corte por ROAS e cada sinal de alerta com a ação (ETAPA 10), e os gatilhos que mandam de volta pra `creative-engine`. Abra nas ETAPAs 9 e 10.

### ETAPA 9 — Checklist Operacional Semanal

Escala sustentável é ritmo. Adapte ao stage e à escola escolhida — os dias abaixo executam o Scaling Protocol da ETAPA 3.5, não uma régua paralela:

| Dia | Ação |
|---|---|
| **Todo dia, à meia-noite do fuso do ad account** | **Reset de budget: ~50% do gasto REAL do dia** em toda campanha que teve budget alterado. Nunca deixar o nominal de pé (ETAPA 3.5). Cada reset aplicado = linha no `ad-log.md` (executor `skill-scale-engine`, motivo "reset da meia-noite"). |
| **Manhã (diário, só Escola A)** | Surf check: alguma campanha com CPA muito abaixo do alvo? Empurra budget e observa 2-3h. Recolhe se quebrar. |
| **Segunda** | 4Pi quick check (Spend → Frequency → CPM → CPR), 5-10 min + checar os dois gates do protocolo (48-72h acima do target? click-based verde — ≥ 60% em 7-day click OU ROAS click-based batendo o KPI?) |
| **Terça** | Avaliar se sobe nível: gates verdes → **+20%** (ou o passo da escola escolhida) / adicionar ad set novo (Escola B) — conferindo no `ad-log.md` que o degrau anterior tem ≥24h, e logando o novo. Gates vermelhos → passo zero e ação fora do ad account (ETAPA 3.5, passo 7) |
| **Quarta** | Revisar learnings + preparar ideias de batch novo |
| **Quinta** | Continuar alimentando criativo (Escola B) / surf se Escola A |
| **Sexta** | **Análise semanal completa** (skill `ad-analysis` — 4Pi full + diagnóstico de fadiga) |
| **Domingo** | **Preparar próximo batch** de criativos (skill `creative-engine`) |

**Monthly review** (1× ao mês, primeiro dia útil):
- PSM real vs projetado (re-ler `manifest.psm_real` + `psm_real_basis` — base proxy segue não liberando escala)
- **Calendário de desejos — revival sazonal:** algum winner que morreu por sazonalidade tem a época dele chegando? Ad sazonal aposentado volta a performar no MESMO período do ano seguinte, e religar custa zero criativo novo (rode `religar seasonal winners ads que morreram voltam no mesmo período calendário de desejos`). Religada executada → linha no `ad-log.md` ("religado", motivo "revival sazonal")
- Custo fixo mensal mudou? (contratação, app novo, retainer) — o gate de corte por ROAS depende desse número estar atual
- Winning ad rate (% de conceitos testados que viraram **breakthrough**, não só que bateram KPI)
- A intensidade atual ainda serve? (graduou de stage? subir de C pra B, ou de B pra A? passou de $1K/dia sustentado → hora de avaliar a graduação pra ASC, ETAPA 4?)
- Algum CPM de conta subiu a ponto de pedir conta nova legítima?
- Membro ligou **Incremental Attribution** em alguma campanha? Os CPAs dela não são comparáveis aos clássicos — re-baseline antes de qualquer decisão de kill/escala (ver nota na Skill `ad-analysis`). Em multi-canal com suspeita de over-attribution do Meta, pode servir como teste de eficiência real — nunca como régua default.
- Re-rodar Skill `scale-engine` se mudança estrutural (novo produto, nova oferta, novo teto)

### ETAPA 10 — Sinais de Alerta (Quando Parar/Recuar)

**Régua única de frequency desta skill (freq DIÁRIA, mesma base da Skill `ad-analysis` — as três leituras abaixo usam ESTA régua, não invente outra):**
- **< 1.3** → folga: pode segurar a contagem de criativos mesmo escalando (ETAPA 8).
- **> 1.4 sustentada + CTR caindo > 20% vs baseline** → fadiga: refresh de criativo — volta pra `creative-engine` (é o trigger canônico do `dados.json`).
- **> 1.5 sustentada em prospecting** → audiência saturada: batch novo ANTES de mais budget.

**Frameworks de recuo e diagnóstico de saturação (rode quando algum sinal disparar):**
- **Scale-Down Rules (PGS reverse)** (rode `scale-down rules decrease budget 20% 7-day CPA exceeds target safety net`) — quando o CPA de 7 dias estoura, corta 20% e segura (não desliga). É a regra dura por trás de "derruba o surf" / "volta pro último nível bom".
- **Spend Redistribution Framework (Don't Kill the Top Spender)** (rode `spend redistribution framework do not turn off top spender ROAS drops higher budget`) — quando o ROAS cai ao subir budget, redistribui em vez de matar o top spender (matar reseta aprendizado).
- **Frequency as Prospecting-vs-Retargeting Proxy** (rode `frequency prospecting vs retargeting proxy low 1.0 high 2.5 broad CBO scaling signal`) — lê frequency como sinal de saturação: baixa (~1.0) = ainda prospectando (pode subir), alta (~2.5) = virou retargeting disfarçado (audiência saturada, pede batch novo).

> **Gate obrigatório antes de recomendar CORTE de spend por queda de ROAS** (unit-economics §4, detalhado em "Custo fixo antes de cortar spend"): ROAS que caiu mas ainda paga o custo variável **não** autoriza corte automático. Com o custo fixo parado, cortar receita pode **aumentar** o prejuízo — e a resposta certa às vezes é subir spend aceitando ROAS menor, porque volume dilui melhor o fixo. Se o membro não informou os fixos, a skill devolve **pergunta** ("quanto é seu custo fixo mensal?"), não instrução de corte. Abaixo do **breakeven por 24-48h persistentes**, a descida de −20% do `ad-taxonomy` §5 continua valendo normalmente (um dia ruim isolado não desce) — lá o problema não é diluição, é margem de contribuição negativa por pedido.

- **CPA dos últimos 3 dias acima do breakeven** → para de subir budget (passo zero no protocolo), refresh criativo antes de qualquer escala. Na Escola A, derruba o surf. E 3 dias já cruzaram a janela de 24-48h persistentes do §5 — a descida de −20% se aplica; confira no `ad-log.md` se ela já foi executada.
- **Frequency > 1.5 sustentada em prospecting** (nas campanhas/ad sets ativos — régua única acima) → audiência saturada, precisa batch novo (`creative-engine`).
- **CPM subindo 30%+ em 14 dias** → saturação, competição, ou conta cansada. Diagnóstico na skill `ad-analysis`; se for conta, abrir conta nova legítima (ETAPA 4.5).
- **Budget novo não gasta / trava entrega** → diagnóstico ETAPA 4.5 (conta vs produto), não conclua "teto" cedo demais. Se o teto for real, a ação é **fora do ad account** (ETAPA 3.5, passo 7), não outro ajuste de bidding.
- **Gates do protocolo vermelhos há mais de uma semana** (nunca completa 48-72h acima do target, ou gate click-based vermelho nas duas portas — <60% em 7-day click E ROAS click-based abaixo do KPI) → o gargalo não é budget. Batch novo (`creative-engine`) + conferência de funil, e re-medir atribuição na `tracking-setup` (o teste de troca 7DC-only da ETAPA 3 é o diagnóstico). Antes de culpar o leilão, confira também um "new reason to be scaling" perdido: se a demanda mudou (sazonalidade, oferta nova), a leitura do protocolo reinicia (ETAPA 3.5).
- **Cash flow gap** → spend correndo na frente do payout. Ajustar pace (ETAPA 6).
- **Fulfillment bottleneck** → estoque/3PL não acompanha. Nunca escale acima da capacidade operacional — venda que não entrega vira chargeback e ban. Com o sourcing na mão, `calendar.reorder_point_days` diz quando segurar: perto do ponto de recompra, pedido de reposição colocado e escala agressiva em pausa até o estoque chegar (ETAPA 6).

### Quando a `scale-engine` recomenda voltar para a `creative-engine` (ciclo explícito)

Se algum destes → invoque skill `creative-engine` pra novo batch:
- Top 3 criativos com > 14 dias de idade
- Frequency max > 1.4 sustentada com CTR caindo > 20% vs baseline (régua única da ETAPA 10)
- Escala cruzou 2× budget (precisa creative diversity pra sustentar)
- Conta nova aberta (ETAPA 4.5) precisa de criativo pra alimentar
- **Escala estagnou** — budget não sobe mais sem quebrar o CPA, ou os gates do protocolo não fecham (ETAPA 3.5, passo 7). É o gatilho mais frequente: quando a escala trava, a alavanca está fora do ad account, e criativo novo é a primeira dela.
- **Só existe `KPI winner` / `spend winner`, nenhum breakthrough** — não há o que escalar; o pedido pra `creative-engine` é conceito novo, não variação do mesmo.

Skill `creative-engine` lerá `ad-analysis/NEXT_BATCH_IDEAS.md` (de 11) + `scale-engine/scale-directives.md` (gerado abaixo).
