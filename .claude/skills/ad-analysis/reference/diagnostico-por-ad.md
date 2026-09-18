# Ad Analysis · Referência: Diagnóstico por ad (ETAPA 3)

> A gravação de `ad_class` por criativo com o gate de piso, a leitura por método de teste (Sniper vs Marksman), a ação de cada classe e estado (breakthrough, spend winner, KPI winner, fadiga, loser, funil quebrado, conta suspeita, em aprendizado) e o checkpoint de kill de produto na cadência quarta→domingo. Abra na ETAPA 3.

### ETAPA 3 — Diagnóstico Por Ad (criativo)

Pra CADA ad de CADA ad set, grave `ad_class` (as 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2, calculadas no bloco Decision Thresholds). Registre junto o `concept_id` do ad set a que ele pertence — é o que permite responder "qual CONCEITO funcionou", e não só "qual execução". Se o batch tem creator humano e a `creator-engine` rodou (Contexto 4h), agrupe a MESMA leitura também **por creator** (custom report "ad name contains" o nome do creator) — é esse agrupamento que devolve hit rate por creator pra `creator-engine` e pro creator report da `content-recycler`.

**Gate de piso (antes de classificar qualquer ad):** se `test_capacity.below_floor_directional_only: true` na `ad-strategy` (Contexto 4f; PLAYBOOK item 6), **não grave `ad_class` formal** — a análise inteira sai marcada como DIRECIONAL (`test_capacity_check.directional_only_analysis: true` no `dados.json`), sem kill e sem escala; a recomendação é subir budget até o piso ou reduzir conceitos, dita ao membro com todas as letras.

**Leitura por método de teste — o que a comparação entre os 3 ads do ad set responde (`testing_method` da `creative-engine`, Contexto 4e):**

| Método do conceito | A comparação dentro do ad set responde | Como nomear o vencedor |
|---|---|---|
| **`sniper`** (ou campo ausente — batch legado) | **"qual EXECUÇÃO venceu"** — os 3 ads são 3 execuções do MESMO ângulo (varia hook/abertura/visual de entrada) | pelo elemento de execução que variou (hook A vs B vs C) |
| **`marksman`** | **"qual ÂNGULO venceu"** — os 3 ads carregam 3 ângulos DISTINTOS sobre um hold universal (cânone §7: Marksman acontece DENTRO do ad set, não entre ad sets) | pela **frase de `angles[]`** do criativo vencedor (match por `creative_n`), carregando o `sub_avatar_id` daquele item |

Três consequências da leitura Marksman:
- **Loser dentro de pack Marksman ≠ ângulo morto.** Cada ângulo recebeu UMA execução só — o trade-off declarado do cânone §7: a falha pode ter sido a execução, não o ângulo. Antes de enterrar um ângulo, puxe **The Execution Problem** (rode `execution problem angle certo palavras erradas 3 strikes por angle 12 razoes de falha`): o mesmo ângulo ganha **3 tentativas (3 strikes)** contra as 12 razões de falha de execução antes de ser descartado. A diretiva de re-teste vai pro `NEXT_BATCH_IDEAS.md`.
- **Hold baixo nos 3 ads do pack = o `hold_universal` é o suspeito**, não qualquer ângulo individual (o hold é compartilhado por construção — se os 3 seguram mal, o problema é o corpo comum). E se o pack saiu com `hold_universal_validated: false` (não deveria — o gate da `creative-engine` bloqueia), a leitura de ângulo está contaminada ("meio Sniper, meio Marksman não ensina nada"): trate como teste inválido de método, não como veredito sobre os ângulos.
- **Vencedor de Marksman → a próxima entrada é Sniper.** Sequência oficial do cânone §7 (Marksman acha a direção → Sniper extrai o máximo do ângulo vencedor); a diretiva de iteração no `NEXT_BATCH_IDEAS.md` nasce já como `sniper` sobre o ângulo nomeado.

**`breakthrough`:** KPI do ad melhor que o KPI da campanha **E** puxa spend (`spend_share_7d` ≥ 30% em conta pequena; 5-10% em conta grande).
→ Ação: manter rodando. **Não há escala automática pra acionar** — Automated Rule de performance é recusada em CBO (cânone §6); a escala é decisão da ETAPA 9 e execução da Skill `scale-engine`, pelo Scaling Protocol manual do §5. É o **único** `ad_class` que entra em `breakthroughs[]` e libera skill `scale-engine` (escala) e skill `content-recycler` (reciclagem).

**`spend_winner`:** puxa spend (`spend_share_7d` ≥ 10%) mas com KPI abaixo do da campanha.
→ Ação: **iterar, não escalar**. Ele segura a conta onde está; escalar um spend winner é subir budget num criativo que já está diluindo o KPI médio. Vai pro `NEXT_BATCH_IDEAS.md` como iteração de uma variável (ETAPA 5).

**`kpi_winner`:** bate o KPI da campanha mas **não puxa spend** (`spend_share_7d` < 10%).
→ Ação: **tratado como loser para decisão** — não escala, não recicla, não vira learning replicável. O KPI bonito veio de amostra pequena e não provou nada. A hipótese mais comum é audiência pequena demais; o escape (forçar spend em ad set próprio pra tirar a dúvida) é recomendação pra skill `scale-engine`, e só depois de sustentar spend ele pode ser reclassificado. **Nunca** o coloque em `breakthroughs[]` "porque bateu o alvo".

**IN FATIGUE:** CPM subindo + CTR caindo + Freq subindo ao longo dos dias (comparar com análises anteriores).
> Antes de classificar fadiga, puxe **Why New Ads Steal From Old Ads / Creative Hamster Wheel** (rode `why new ads steal from old ads creative hamster wheel deprioritized`) — explica quando o sinal de "fadiga" é na verdade um ad novo canibalizando o spend do antigo (deprioritization), e não fadiga real da audience. Muda a ação: nesse caso o fix é consolidar, não refresh.
> **Calibração 2026 (pós-Andromeda/GEM):** a vida útil típica de criativo encolheu pra **2-4 semanas** (estático fatiga mais rápido; o pico de performance costuma ser a 1ª semana). Planeje refresh nessa janela — não em ciclos de 6-8 semanas.
→ Ação: trocar os 1-2 criativos mais fatigados do ad set por conceitos novos (Skill `creative-engine`) OU pedir batch novo completo. **Não pausar ainda** — pode ainda estar performando acima do breakeven mesmo com sinais de fadiga.

**`loser`** (def. canônica do bloco Decision Thresholds): `spend_share_7d` ≤ 2% em 7 dias ("não fez nada pela conta" — cânone §2; gastar sem bater KPI não é loser: puxando spend, é `spend_winner`, que itera). Some a isso as réguas de kill do cânone §3 — conta madura: ad set após 7 dias sem spend e sem KPI; conta nova: ad com ≥ 8× o target CPA sem purchase; ad novo overspendando: 24-48h de carência antes de decidir.
→ Ação: PAUSAR pela régua do contexto da conta (ad set em conta madura, ad em conta nova). Fazer diagnóstico profundo (Etapa 4) pra entender por que falhou.

**FUNIL QUEBRADO (não é o criativo):** o criativo trouxe ATC/checkouts mas as taxas estão abaixo dos benchmarks (ATC→compra < 20-25% ou checkout→compra < 40-50%).
→ Ação: **NÃO pausar o criativo** — o ad fez o trabalho, o gargalo é página/checkout/oferta. Rotear pra `copy-engine`/`page-design` (página) ou `offer-builder` (oferta). Registrar o gargalo de funil no `health_signals` e no NEXT_BATCH_IDEAS.

**CONTA SUSPEITA (não é o produto):** CPM generalizado muito acima do nicho (`account_cpm_suspect`).
→ Ação: re-testar o mesmo criativo/produto em OUTRA conta de anúncio antes de matar o produto. Só mata o produto se não validar em conta nenhuma.

**EM APRENDIZADO:** < 7 dias rodando (ou < 24-48h, no caso de ad novo que está overspendando), ou a campanha ainda sem `campaign_cpa` estável.
→ Ação: aguardar antes de classificar — não grave `ad_class` ainda. Dê ao Meta tempo de estabilizar a entrega e o CPA antes de julgar — a learning phase clássica (~50 eventos de conversão/7 dias por ad set) continua valendo em 2026, e abaixo desse volume o CPA balança. Não mexer no ad set enquanto isso (edições resetam o learning com mais facilidade desde abril/2026).

**CHECKPOINT de KILL de PRODUTO (cadência quarta→domingo — a leitura vive AQUI, não na `ad-strategy`):** o teste de produto lança quarta e tem teto de 7 dias por rodada (cadência montada pela Skill `ad-strategy`). **Domingo é CHECKPOINT de decisão informada, não sentença** — a data abre a leitura; quem decreta qualquer óbito é a leitura (esta skill + as réguas do cânone), nunca o calendário. Ordem de precedência OBRIGATÓRIA no checkpoint:
0. **Teste abaixo do piso?** (`below_floor_directional_only: true` — Contexto 4f) — resultado direcional NÃO decreta morte de produto: a janela não teve leitura válida. Recomende subir budget até o piso (ou reduzir conceitos) e re-rodar a janela antes de qualquer veredito.
1. **Funil quebrado?** (ETAPA 6B) — se os ads trouxeram checkouts que a página desperdiçou, o problema é página/oferta; conserta antes de matar o produto.
2. **Conta suspeita?** (Pi 3, `account_cpm_suspect`) — CPM generalizado fora do nicho pede re-teste em OUTRA conta antes de matar o produto.
3. **Entrega travada?** — ads presos em review/policy não testaram nada; resolver e re-rodar a janela.
Se os 4 checks passam e não houve venda até domingo → o default é **processar os learnings e iterar**, não matar o produto. Batch sem venda reprova, na maioria dos casos, a EXECUÇÃO testada, não o ângulo (Execution Problem, ETAPA 3): ângulo com strikes restantes itera em **Sniper** no próximo batch, com a diretiva gravada no `NEXT_BATCH_IDEAS.md`. O que morre já no checkpoint morre por régua, não por clemência: ad set que cruzou o cânone §3 (conta madura: 7 dias sem spend e sem KPI · conta nova: 8× target CPA sem purchase) é decretado normalmente.

**Matar o PRODUTO é decisão de outro nível:** só entra na mesa com **≥ 2 batches com learnings processados** (esta skill extraiu o que cada batch ensinou e o batch seguinte aplicou a correção) **OU quando as réguas do cânone §3 mandarem — nunca por calendário sozinho.** A intenção original do marco de domingo permanece inteira: impedir o membro de queimar caixa por semanas num produto morto. O que muda é o mecanismo — quem declara o óbito é a leitura (esta skill + cânone), não a data.
