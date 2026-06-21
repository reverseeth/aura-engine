---
name: scale-engine
description: Engine de escala vertical de Meta Ads em cima de 3 escolas reais de gestores de tráfego escalando ecom US/EU — (A) cost-cap duplication + surf de manhã, (B) bid cap "campanha monstro", (C) budget-doubling a cada 3 dias — recomendadas por member-stage. Mantém PSM (lê manifest.psm_real, não recomputa) como diagnóstico, projeções 30/60/90 com cash flow, e fecha ciclo de volta pra 08 quando precisa de criativo novo. Use quando o membro disser "scale", "escalar", "plano de escala", "crescer", "maximizar", ou quando os ads estão estáveis e quer aumentar spend de forma sistemática.
---

# Scale Engine

## Quando Usar
Quando o membro tem winner(s) provados (criativo que vende com CPA dentro/abaixo do breakeven, validado pela skill 11) e quer aumentar spend de forma sistemática sem queimar conta. Esta skill é a **camada de execução operacional** de escala: qual estrutura de campanha montar no Ads Manager, com qual bidding, quanto duplicar, quando surfar, quando recuar. PSM e 4Pi continuam como leitura de diagnóstico (a skill 11 calcula), mas o "exatamente o que fazer" vive aqui.

> **Pré-condição honesta:** escala não conserta ad ruim nem oferta fraca. Se não tem winner provado, isto não é hora de escalar — é hora de mais criativo (skill 08) e melhor oferta (skill 04). A skill detecta isso na ETAPA 3 e te manda de volta sem culpa.

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

### Pré-flight
- [ ] `10-ad-strategy/dados.json` + `11-ad-analysis/dados.json` existem (`workspace/[produto]/11-ad-analysis/dados.json`)
- [ ] Manifest tem `11-ad-analysis` em `skills_completed`
- [ ] `manifest.psm_real` foi gravado por ≥ 1 análise recente (senão, rodar 11 — quem calcula `psm_real`)
- [ ] Existe ≥ 1 winner identificado no `11-ad-analysis/dados.json` (Post ID com CPA ≤ breakeven estável) — sem isso, escala é prematura

Se algum arquivo de pré-flight faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill faltante agora (11 pra `11-ad-analysis/dados.json`/`psm_real`, 10 pra ad-strategy), **OU (B)** prosseguir com default genérico marcando `manifest.skipped_preflight += ["arquivo"]` e avisando no output final que recomenda re-executar.

### Contexto a carregar

1. Leia `workspace/profile.md` (budget atual + stage — define ponto de partida e agressividade)
2. Leia `workspace/[produto]/04-offer-builder/relatorio.md` + `04-offer-builder/dados.json` (breakeven CPA/ROAS, `cogs_breakdown`, PSM projetado — define o teto de cost cap / bid cap)
3. Leia `workspace/[produto]/10-ad-strategy/relatorio.md` (estrutura de campanha atual: estamos em 1-1-N de teste? cost cap já roda?)
4. Leia TODAS as análises em `workspace/[produto]/11-ad-analysis/` em ordem cronológica (trajetória real de performance, winners estáveis, CPM por conta) + `dados.json` (handoff da skill 11)
5. Leia scale plans anteriores em `workspace/[produto]/12-scale-engine/` (se existir — comparar premissas com realidade)
6. **Puxe os SISTEMAS NOMEADOS da base — NUNCA query genérica.** Rode `search_knowledge` (deep=true) com a `best_query` exata de cada framework relevante pra ETAPA que está rodando. O índice completo do domínio de escala desta skill está em `.claude/lib/kb-index/` (`frameworks.json` / `README.md` — mapa skill→domínio). Os sistemas de maior impacto pra escala estão embutidos nas ETAPAS abaixo; o resto (28 frameworks de scaling) fica disponível no índice. Mínimo a carregar antes de montar qualquer plano:
   - **Performance Gate Scaling (PGS) + The Three PGS Principles** (rode `Performance Gate Scaling PGS 3 principles trailing CPA automated rules` e `The three PGS principles never scale past margin trailing multi-day KPI campaign-based`) — espinha dorsal de quando subir/segurar
   - **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM golden ratio LTV CPA COGS formula`) + **PSM Scaling Thresholds** (rode `PSM thresholds 1.3 aggressive 1.1 healthy breakeven zone scaling decision`) — leitura de diagnóstico (a 11 calcula)
   - **Three Budget Scaling Methods** (rode `Three budget scaling methods farmer 5% aggressive 50% business-led MRR`) — farmer 5% vs aggressive 50% vs business-led
   - **Three Reasons Scale Breaks** (rode `three reasons scale breaks unit economics funnel imbalance cash constraints can we spend more tomorrow`) — unit economics, funnel imbalance, cash
   - **Creative Diversity as a Scaling Mechanism** (rode `creative diversity as a scaling mechanism funnel balance video image 4Pi same position`) — combustível da escala

   Aprofunde — escala errada queima budget mais rápido que ad ruim.

### Breakeven é a âncora de tudo

Toda a matemática de escala desta skill ancora no **CPA de breakeven** e no **CPA máximo** (`max_cpa` = breakeven menos a margem de lucro desejada — é o setpoint do cost cap/bid cap, **distinto** dos `target_cpa_primary_2x/3x` da Skill 04, que são alvos de múltiplo de ROAS; o `max_cpa` é dirigido pelo lucro que o membro quer por pedido). **Fonte canônica do breakeven CPA (a MESMA das Skills 10 e 11):** `04-offer-builder/dados.json.unit_economics.weighted_margin_per_order`. Use esse campo direto, não re-derive. A performance real vem do `11-ad-analysis/dados.json`. Não invente — leia. Se faltar, pegue na ETAPA 1.

### PSM real (vs teórico) — LER, não recalcular

`psm_theoretical` vem do `04-offer-builder/dados.json` (baseado em AOV esperado).
`psm_real` é gravado SOMENTE pela skill 11 (ad-analysis) a partir de performance real. A skill 12 **LÊ `manifest.psm_real`** — fonte canônica — e **NUNCA recalcula** com outra fórmula.

Fórmula canônica (referência, calculada pela 11): `PSM = LTV / (CPA + COGS)`, onde COGS é o somatório de `04-offer-builder/dados.json.cogs_breakdown` (não existe campo `cogs_total`).

**Frameworks pra interpretar PSM (rode antes de decidir):**
- **Profitable Scaling Margin (PSM) — golden ratio** (rode `Profitable Scaling Margin PSM golden ratio LTV CPA COGS formula`) — a fórmula canônica e por que ela manda
- **PSM Scaling Thresholds** (rode `PSM thresholds 1.3 aggressive 1.1 healthy breakeven zone scaling decision`) — `≥1.3` escala agressivo, `~1.1` saudável (escala medido), perto de breakeven = não escala
- **Scaling Mindset Farmer vs Hunter (Andromeda)** (rode `scaling mindset farmer vs hunter Andromeda think bigger clarity not volume`) — qual mentalidade aplicar ao número do PSM

Compare `manifest.psm_real` contra `psm_theoretical`. Se `|psm_real − psm_theoretical| / psm_theoretical > 0.2` (desvio > 20%):
- **psm_real < psm_theoretical**: economia de oferta pior que esperada; **NÃO escale** (nem cost cap, nem surf), revisar offer primeiro
- **psm_real > psm_theoretical**: oferta performa melhor que o esperado; pode escalar mais agressivo (cost cap mais alto, surf mais ousado)

Use os **PSM Scaling Thresholds** como teto de agressividade: mesmo com `psm_real > psm_theoretical`, se o `psm_real` absoluto está perto de 1.0 (breakeven zone), escala só medido — margem fina não aguenta surf 10×.

Se `manifest.psm_real` estiver ausente, rode a skill 11 primeiro (quem o grava) — não estime aqui.

## Fluxo da Skill

### ETAPA 1 — Receber Panorama Atual

Primeiro, pré-popule dos artefatos: `11-ad-analysis/dados.json` (spend diário, CPA médio, CPM por conta, ROAS médio, AOV real, winners estáveis com Post ID) + `04-offer-builder/dados.json` (breakeven CPA/ROAS) + `manifest.psm_real`. Só pergunte ao membro o que NÃO está nos artefatos.

Se algo faltar (ex: cash disponível pra surf, que não vive em nenhum JSON), peça em UMA única mensagem só os campos faltantes:

"Confirmando o panorama: [valores lidos do 11-ad-analysis/dados.json + breakeven do 04]. Me falta só [campo(s) ausente(s)]."

Se `11-ad-analysis/dados.json` não existir, aí sim peça tudo: "Me dá o panorama atual: quanto gasta por dia, CPA médio, CPM médio, ROAS, AOV, e quais ads são winners (gastam e vendem dentro do breakeven). E o breakeven CPA do produto." Não re-explique campos já preenchidos.

### ETAPA 2 — Classificar Estágio de Escala

Stage canônico vem do `manifest.stage` (`starter` | `validating` | `scaling`) — detecção pela rule `member-stage-awareness.md`. O stage dita **qual escola de escala recomendar como default** e a agressividade. A sub-fase de spend abaixo é DIAGNÓSTICO (informa intensidade), nunca substitui o stage canônico.

| Spend diário | Sub-fase de escala | Leitura |
|---|---|---|
| < $100/dia | Teste | Ainda achando winner. Escala = mais criativo, não mais budget. |
| $100-500/dia | Tração | Tem winner mas frágil. Escola C ou bid cap, devagar. |
| $500-1K/dia | Escala Inicial | Winner estável. Bid cap ou cost cap. |
| $1K-5K/dia | Escala Agressiva | Cost cap + surf, atenção diária. |
| $5K+/dia | Otimização | Unit economics, múltiplas contas, omnichannel. |

A sub-fase vive em `scale_phase` no `12-scale-engine/dados.json` — **NUNCA** em `manifest.stage`.

### ETAPA 3 — Análise de Prontidão (Pré-Requisitos)

Antes de aumentar spend, validar se o sistema aguenta. Falhar em qualquer um = identificar gargalo e resolver ANTES de escalar.

**Frameworks de prontidão (rode antes de aprovar escala):**
- **Three Reasons Scale Breaks** (rode `three reasons scale breaks unit economics funnel imbalance cash constraints can we spend more tomorrow`) — escala quebra por 3 motivos: unit economics fraco, funnel desbalanceado, cash constraint. Cada pré-requisito abaixo mapeia num desses.
- **Would It Hold at 3X Budget? (Mental Model)** (rode `would it hold at 3X budget mental model low spend high ROAS statistically insignificant`) — winner com pouco spend e ROAS alto pode ser ruído estatístico. Aplique este teste mental antes de chamar algo de "winner provado".
- **Scaling Click-Based Data Gate** (rode `scaling click-based data gate 60% purchases view-through attribution 7-day click 1-day view`) — se a maioria das conversões é view-through (não click-based), o sinal de escala é frágil. Cheque a janela de atribuição antes de subir.

| Pré-requisito | Critério | Se falhar |
|---|---|---|
| **Winner provado** | ≥ 1 criativo com CPA ≤ breakeven, estável por 3+ dias (ideal 2-3 winners) | **Volta pra 08** (mais criativo) — escala sem winner é prematura |
| **PSM real ≥ teórico** | `manifest.psm_real` não está > 20% abaixo do `psm_theoretical` | Ajustar oferta (AOV, garantia, stack) ANTES de escalar |
| **CPA estável ou melhorando** | Trend dos últimos 3-7 dias estável ou descendo | Diagnóstico de fadiga (skill 11) antes de escalar |
| **CPM saudável na conta** | CPM dentro da faixa normal pro nicho/conta | CPM muito alto = problema de CONTA, não de produto. Testar winner em outra conta (skill 11) antes de escalar |
| **Creative pipeline ativo** | Batch novo a cada 1-2 semanas no ritmo de escala | Recomendar Skill 08 — escala consome volume de criativo |
| **Pixel/CAPI health** | Match quality ≥ 80%, sem events perdidos | Fix técnico (skill 07c) antes de escalar |
| **Cash flow pra COGS + spend** | Membro tem $ pra cobrir o gap entre spend (cobrado diário) e payout (Shopify 3-5 dias) | Ajustar pace de escala ao cash disponível (ver ETAPA 6) |

Pra cada pré-requisito que falha, documente o bloqueio e recomende ação específica. **Winner provado é eliminatório** — sem ele, a skill não monta plano de escala, manda de volta pra 08.

### ETAPA 4 — As 3 Escolas de Escala (apresentar, recomendar por stage)

Existem três escolas de escala vertical, todas reais e usadas por gestores de tráfego escalando ecom. Não há uma "certa" — há a certa pro **stage** e pro **apetite de risco** do membro. **Apresente as três ao membro** (tabela curta, no report_language), marque a recomendada pro stage dele, e deixe ele escolher.

> **Regra de ouro das três:** em escala, o bidding é cost cap ou bid cap — **Max Conversion (highest volume) é só pra TESTAR criativo** (estrutura 1-1-N da skill 10). Quando o criativo já provou, você passa pra uma das escolas abaixo pra forçar volume com teto de custo.

**Sistemas nomeados que sustentam o ritmo das três escolas (rode os relevantes à escola escolhida):**
- **Performance Gate Scaling (PGS) + The Three PGS Principles** (rode `Performance Gate Scaling PGS 3 principles trailing CPA automated rules` e `The three PGS principles never scale past margin trailing multi-day KPI campaign-based`) — nunca escala além da margem, usa trailing multi-day KPI (não 1 dia), decisão por campanha. É a régua de QUANDO subir em qualquer escola.
- **Three Budget Scaling Methods** (rode `Three budget scaling methods farmer 5% aggressive 50% business-led MRR`) — farmer (+5%/dia, conservador), aggressive (+50%, troca volatilidade por velocidade), business-led (escala atrelada a MRR/cash). Mapeia direto: C≈farmer, A≈aggressive.
- **EAM Scaling Protocol & Decision Tree** (rode `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`) — 48-72h acima do target antes de subir, depois escala a cada 24h enquanto segura. Árvore de decisão de quando subir vs segurar vs recuar.
- **Sliding Scale Rules (PGS Advanced)** (rode `sliding scale rules PGS different CPA targets spend levels 60 55 52 50`) — fundamenta os **caps decrescentes da Escola A** ($50/$45/$40/$35): cada nível de spend tem um CPA target diferente.
- **Soft Surfing (PGS Advanced)** (rode `soft surfing additional daily 5% increase CPA far below target accelerate growth`) — versão controlada do "surf de manhã" da Escola A: +5% extra quando o CPA está MUITO abaixo do target. Use isto pra calibrar o surf antes do 10× agressivo.
- **Scale-Down Rules (PGS reverse)** (rode `scale-down rules decrease budget 20% 7-day CPA exceeds target safety net`) — quando o CPA de 7 dias estoura o target, corta budget 20%. É a rede de segurança das três escolas (espelha o "recolhe quando quebra" da Escola A e o "volta pro último nível bom" da Escola C).
- **Spend Redistribution Framework (Don't Kill the Top Spender)** (rode `spend redistribution framework do not turn off top spender ROAS drops higher budget`) — quando o ROAS cai ao subir budget, NÃO desliga o top spender (matar quebra o aprendizado). Crítico pra Escola B (nunca desativa criativo) e pra surf que quebrou.
- **Levels of Scaling (Zero-to-50K to 100K/day)** (rode `levels of scaling zero to 50k 100k per day one campaign CBO raw content ASC whitelisting segmented`) — estrutura de campanha por nível de spend (one-campaign → CBO → ASC → whitelisting → segmented). Mapeia a `scale_phase` da ETAPA 2 num blueprint de estrutura real.

#### Escola A — Cost-Cap Duplication + Surf de Manhã (mais agressiva, mais upside)

A mecânica:

1. **Isola o winner numa campanha 1-1-1** — 1 campanha, 1 ad set, 1 criativo vencedor. Limpo, sem ruído. Se 2 criativos validaram, uma estrutura 1-1-1 pra cada.
2. **Bidding = Cost Cap** (custo por resultado), setado **~10% abaixo do CPA de breakeven**. Ex: breakeven $55 → cost cap inicial **~$50** (deixa ~9% de lucro por pedido nesse teto: `lucro/pedido = breakeven − cap = $5` ≈ 9% da margem de $55). O cost cap é o teto: o Facebook só gasta enquanto consegue resultado abaixo dele. **São os caps decrescentes do passo 3 que vão exigindo mais lucro por pedido** — quanto mais baixo o cap, maior a margem por venda (ex: cap ~$38 ≈ 30% de lucro/pedido).
3. **Duplica o 1-1-1 várias vezes com caps DECRESCENTES** — $50, $45, $40, $35… de $5 em $5. Cada duplicata com o mesmo budget de teste (ex: $160/dia). A lógica: cada cap mais baixo pega a eficiência num ponto diferente do leilão; o Facebook acha gasto onde dá pra entregar dentro daquele teto. Quanto mais baixo o cap, mais difícil gastar, mas mais barato o resultado.
4. **Surf de manhã (a parte agressiva).** Ao acordar, olhe as campanhas. Uma com CPA **muito** abaixo do alvo (ex: 2 vendas, gastou $30, CPA $15 num produto de breakeven $55) está pedindo budget. **Joga o budget 10×** ($160 → $1.600), observa 2-3h.
   - Continua vendendo dentro do alvo → **sobe mais** ($3k, $30k — não gasta tudo, gasta o que conseguir vendendo).
   - Gastou ~$150 a mais SEM venda nova, ou o CPA passou do breakeven → **derruba o budget de volta IMEDIATAMENTE**. Não espera prejuízo grande. Ao baixar, a campanha frequentemente volta a vender no nível anterior.
   - Sem regra fixa de %. Vai pelo que a campanha entrega naquele momento. É monitoramento ativo, não set-and-forget.

   > Surf é "navegar a onda": quando o leilão tá te dando resultado barato, você empurra o máximo de budget enquanto a onda segura, e recolhe na hora que ela quebra. Exige presença (olhar a cada 2-3h num dia de surf). Por isso é escola de **scaling**, não de starter.

**Quando usar:** stage `scaling`, winner muito estável, membro com tempo pra monitorar de manhã e estômago pra volatilidade. Maior upside, maior atenção.

#### Escola B — Bid Cap "Campanha Monstro" (mais controlada, mão menos pesada)

A mecânica:

1. **1 conta de anúncio = 1 campanha de Bid Cap.** (Roda 1 dia de Max Conversion antes, só pra a conta pegar mini-dados de cliente e ajudar o bid cap a achar gasto.)
2. **Setup:** `bid cap = seu CPA máximo`; `budget = 100× o CPA máximo`. Ex: CPA máximo $30 → bid cap $30, budget diário $3.000. **Não gasta tudo** — o budget alto é só espaço; o bid cap é o teto real de custo por resultado.
3. **Alimenta a MESMA campanha continuamente** com mais ad sets de criativo (≈5 criativos por ad set). A cada 1-2 dias, adiciona um ad set novo com criativos novos. Pode chegar a 20 ad sets / 200 criativos numa única campanha "monstro".
4. **NÃO desativa criativos.** Deixa o Facebook varrer todos atrás de CPA abaixo do bid cap. O algoritmo concentra gasto onde acha resultado e ignora o resto (criativo ruim simplesmente não gasta — você não precisa matar manualmente).

**Risco e safeguard:** adicionar ad set novo numa campanha que está ótima pode **travar a entrega** (resetar o aprendizado). Se a campanha tá voando, **prefira abrir OUTRA conta/campanha** em vez de arriscar mexer na boa. Baixar o bid cap de $2 em $2 pra apertar o CPA é possível, mas arriscado (também pode travar) — faça só com folga.

**Quando usar:** stage `validating` ou `scaling` que quer crescimento estável com pouca mão. Menos volatilidade que a Escola A, menos upside explosivo.

#### Escola C — Budget-Doubling a cada 3 Dias (mais simples)

A mecânica:

1. Roda a campanha (pode ser Max Conversion no começo, ou cost/bid cap).
2. **Dobra o budget a cada 3 dias** enquanto o ROI/CPA segura: $100 → $200 → $400 → $800…
3. Quando quebra num nível (CPA estoura o target / ROI fica negativo), **volta pro último nível bom** e segura ali. Esse é o seu teto atual ("achei meu teto").
4. Pra subir de novo depois: melhora o que está fora do Ads Manager (criativo novo da 08, oferta melhor da 04) e tenta dobrar de novo a partir do teto.

> Os 3 dias importam: dão dado suficiente pro Facebook estabilizar antes de cada salto e evitam reagir a um pico de 1 dia. É a versão "sem ficar no teclado" de escala — não exige surf nem gestão de N campanhas.

**Quando usar:** stage `starter` (e `validating` no começo). É a mais fácil de operar, a mais perdoável, e ensina o membro a achar o teto sem queimar conta.

#### Tabela de escolha (apresentar ao membro)

| Escola | Como funciona em 1 frase | Mão de obra | Volatilidade | Default pra stage |
|---|---|---|---|---|
| **C — Budget-doubling 3d** | Dobra a cada 3 dias até quebrar, volta pro último nível bom | Baixíssima | Baixa | **starter** |
| **B — Bid cap monstro** | 1 campanha, budget 100× CPA, bid cap = CPA máx, alimenta com ad sets, nunca desativa | Baixa-média | Média | **validating** (e starter que quer controle) |
| **A — Cost-cap + surf** | Isola winner 1-1-1, duplica com caps decrescentes, surfa de manhã | Alta (olhar 2-3×/dia) | Alta | **scaling** |

Recomendação por stage (default, não trava): **starter → C** (ou bid cap se quiser controle); **validating → bid cap ou cost-cap**; **scaling → cost-cap + surf** (mais upside, mais atenção).

Pergunte ao membro qual escola quer rodar. Se ele não tiver opinião, vá com o default do stage e explique por quê. Registre a escola escolhida no `12-scale-engine/dados.json` (`scaling_school`).

### ETAPA 4.5 — Quando o budget trava a entrega → abrir nova conta

Padrão que aparece em todas as escolas: às vezes você sobe o budget e a entrega **não acompanha** — a campanha não gasta o novo budget, ou trava o aprendizado e o CPA dispara. Antes de concluir "atingi meu teto", diagnostique:

1. **É a conta ou o produto?** CPM muito acima do normal pro nicho é sinal de **conta cansada**, não de produto morto. O mesmo winner pode dar CPM $30 numa conta e $100 noutra (a skill 11 mede isso).
2. **Se for a conta** → a jogada legítima é **abrir uma conta de anúncio nova** e rodar o mesmo winner lá. Ter contas de anúncio organizadas (1 por produto, mais contas de reserva pra resiliência) é organização e contingência legítimas — embaralhar 2 produtos numa conta confunde o aprendizado, então separar é boa prática.
3. **Na Escola B**, lembre: se a campanha boa não aguenta mais um ad set sem travar, **abra outra conta/campanha** em vez de arriscar a que está performando.

> **Limite ético (inviolável):** esta skill encode SÓ a mecânica legítima de organização de conta e campanha. **NÃO** ensina nem recomenda comprar BM/contas de terceiros, "farmar" contas, contingenciar perfil-dono-vs-anunciante pra driblar ban, produto réplica ou cloaking. Essas táticas derrubam a conta da marca real e brigam com a tese brand-building do Aura. Abrir uma conta de anúncio nova e legítima dentro do seu próprio Business Manager é resiliência; farmar conta pra driblar política não é — e não tem suporte aqui.

### ETAPA 5 — Credibilidade da Loja (lever de conversão antes de escalar)

Escalar budget joga tráfego mais frio na loja. Se a loja não parece confiável, a conversão cai e a escala morre. Antes de empurrar volume, confirme (nota rápida, não bloqueio):

- Página de Facebook + Instagram com seguidores reais e posts (não vazio).
- Reviews/avaliações reais (~100, em inglês) na PDP — prova social.
- Highlights/destaques de confiança: brand story / About, feedback, selos legítimos.
- **Gestão de comentários é o mais importante.** Comentário negativo num post de ad fica visível pra todo mundo que vê o anúncio e derruba conversão direto. Responder ou deletar comentários ruins é manutenção diária de escala.

> **Honestidade:** foco em prova social **real**. Comprar seguidor/comentário falso em volume pode atrapalhar (parece fake, arrisca a conta) — não recomendado. Se a credibilidade da loja está fraca, isso é gargalo de conversão a resolver na 07a/07b/07d antes de gastar mais em ads.

### ETAPA 6 — Cash Flow (o gargalo invisível de escala)

Ads cobram **diário**; o payout do Shopify chega em **3-5 dias** (Stripe ~2 dias). Quando você escala, esse descasamento vira um buraco de caixa que cresce com o budget. Escalar sem cobrir o gap é a forma mais comum de quebrar uma marca que estava lucrando.

**Frameworks de cash flow e teto de risco (rode antes de autorizar escala agressiva):**
- **Total Loss Investment Concept** (rode `total loss investment concept aggression ceiling zero additional revenue acceptable loss`) — define o teto de agressividade: quanto você aceita perder se o gasto extra trouxer zero receita nova. É o limite duro do surf da Escola A e do doubling rápido da Escola C.
- **Fractional Banking** (rode `fractional banking borrow against future revenue rolling repeat purchase cash flow scale negative CPA`) — como financiar escala emprestando contra receita futura/repeat purchase quando o cash gira mais devagar que o spend. Pré-condição: LTV/repeat real provado (não chute).
- **Going Negative on CPA (LTV-Funded Acquisition)** (rode `going negative on CPA LTV rebills Agora upfront capital dominate market acquire more customers`) — só pra `scaling` com LTV/rebill comprovado e capital de giro: aceitar CPA acima do breakeven na primeira compra porque o LTV banca. **Nunca** ofereça isto a starter/validating sem dado de repeat real.

**Check obrigatório antes de qualquer escala > 2× em < 7 dias:**

- [ ] Float de cash disponível ≥ `1.5 × daily_budget_target × payout_lag_days`
- [ ] Fornecedor consegue entregar o volume de unidades projetado em 30/60/90 dias? (confirmação escrita)
- [ ] Backup payment method se o Meta bloquear o cartão principal?

**Cálculo de gap projetado:**
```
cash_gap_projected = (daily_budget × 30 × burn_multiplier) − (daily_revenue_projected × 30 × (1 − payout_lag/30))
onde burn_multiplier = 1.3 (margem de segurança)
```

Se `cash_gap_projected > 50% do cash disponível`, **NÃO autorize** escala agressiva (surf 10×, doubling rápido). Volte pra ritmo conservador (Escola C devagar ou cost cap sem surf) até o caixa girar.

**Regra dura:** nunca escala > 2× o budget atual em < 7 dias se o cash não cobre o gap — independente de quão bom o sinal está. O surf da Escola A respeita isso: surfa com o que tem, recua na hora.

### ETAPA 7 — Projeção Realista 30/60/90 (base + pessimista + cash flow)

Construa dois cenários usando breakeven, AOV e PSM reais.

**Base (premissas: escola escolhida rodando, pipeline de criativo ativo, CPA estável):**

| Mês | Spend/dia alvo | Receita/dia (AOV × vendas) | Margem mensal estimada |
|---|---|---|---|
| Mês 1 | $[atual × 1.5-2] | $[calculado] | $[margem × 30] |
| Mês 2 | $[atual × 2-3] | $[calc] | $[margem] |
| Mês 3 | $[atual × 3-4] | $[calc] | $[margem] |

Use AOV real do `11-ad-analysis/dados.json` e breakeven do `04-offer-builder/dados.json`. Não infle: na Escola A o crescimento é em saltos (surf), na C é dobra a cada 3 dias até o teto — modele o caminho realista da escola escolhida.

**Pessimista (CPA sobe 20%):**

Ação: parar de subir budget, segurar no último nível lucrativo, refresh de criativo (08) + possível ajuste de oferta (04), retomar escala quando o CPA voltar ao alvo (geralmente 7-14 dias).

Impacto: escala atrasa ~1 mês, mas sem queimar cash flow.

**Template de cash flow (incluir sempre):**

| Dia | Daily Budget | Daily Revenue | Payable (ads) | Receivable (payout +3d) | Cash Float Needed |
|-----|--------------|---------------|---------------|-------------------------|-------------------|
| 1   | $200         | $500          | -$200         | $0                      | $200              |
| 3   | $300         | $750          | -$300         | +$500                   | $300-500          |
| ...  | ...          | ...           | ...           | ...                     | ...               |

Alerte se `cash_float_needed_peak > cash_disponivel × 0.7`.

### ETAPA 8 — Creative Diversity Como Combustível da Escala

Escalar consome criativo. Mesmo winner satura a audiência: a $100/dia satura em ~30 dias; a $500/dia em ~7-10 dias; a $2K/dia em 3-5 dias. As três escolas dependem de pipeline de criativo:

**Frameworks que governam o criativo como alavanca de escala (rode os relevantes):**
- **Creative Diversity as a Scaling Mechanism** (rode `creative diversity as a scaling mechanism funnel balance video image 4Pi same position`) — diversidade de criativo (video/image, ângulos) equilibra o funnel e destrava mais spend na MESMA posição do 4Pi. É o motor de horizontal scale dentro da vertical.
- **More Better New Scaling Framework (Hormozi)** (rode `More Better New scaling framework Hormozi sequence maximize before new method`) — sequência: maximize o que existe (More), melhore (Better), só então adicione método novo (New). Aplique antes de abrir frente de criativo nova — esgote o winner atual primeiro.
- **Reeves' Principle of Dispersion** (rode `Reeves principle of dispersion reach over frequency Reality in Advertising new audiences`) — em escala, reach sobre frequency: criativo novo abre audiência nova em vez de martelar a mesma. Fundamenta por que frequency alta pede batch novo, não mais budget.
- **Minimum Daily Spend & Creative Hamster Wheel** (rode `minimum daily spend creative hamster wheel new ads steal bottom of funnel never turn off main campaign`) — ads novos roubam bottom-of-funnel da campanha principal; nunca desligue a campanha principal pra "fazer espaço". Calibra a cadência de batch sem canibalizar.

- A Escola B é **literalmente alimentada** por ad sets novos de criativo continuamente.
- A Escola A precisa de winners de backup pra quando o atual cansar no surf.
- A Escola C destrava níveis novos com criativo melhor.

**Quantidade de criativo por sub-fase de escala (heurística, não lei):**

| Sub-fase | Novos conceitos/batch | Frequência | Creators em retainer |
|---|---|---|---|
| Teste (<$100/dia) | 3-5 | Mensal | 0 |
| Tração ($100-500) | 5-8 | A cada 2-3 semanas | 0-1 |
| Escala Inicial ($500-1K) | 8-12 | Quinzenal | 1-2 |
| Escala Agressiva ($1K-5K) | 12-20 | Semanal | 2-4 |
| Otimização ($5K+) | 20+ | Semanal | 4+ ou agência |

Calibre pelo stage (`member-stage-awareness.md`): starter recebe a ponta baixa, scaling a ponta alta. Se `frequency_max < 1.3` e CPM estável, pode segurar a contagem atual mesmo escalando.

### ETAPA 9 — Checklist Operacional Semanal

Escala sustentável é ritmo. Adapte ao stage e à escola escolhida:

| Dia | Ação |
|---|---|
| **Manhã (diário, só Escola A)** | Surf check: alguma campanha com CPA muito abaixo do alvo? Empurra budget e observa 2-3h. Recolhe se quebrar. |
| **Segunda** | 4Pi quick check (Spend → Frequency → CPM → CPR), 5-10 min |
| **Terça** | Avaliar se sobe nível (Escola C: passou 3 dias bom? dobra) / adicionar ad set novo (Escola B) |
| **Quarta** | Revisar learnings + preparar ideias de batch novo |
| **Quinta** | Continuar alimentando criativo (Escola B) / surf se Escola A |
| **Sexta** | **Análise semanal completa** (skill 11 — 4Pi full + diagnóstico de fadiga) |
| **Domingo** | **Preparar próximo batch** de criativos (skill 08) |

**Monthly review** (1× ao mês, primeiro dia útil):
- PSM real vs projetado (re-ler `manifest.psm_real`)
- Winning ad rate (% de conceitos testados que viraram winners)
- A escola atual ainda serve? (graduou de stage? trocar de C pra bid cap, ou bid cap pra cost-cap+surf?)
- Algum CPM de conta subiu a ponto de pedir conta nova legítima?
- Re-rodar Skill 12 se mudança estrutural (novo produto, nova oferta, novo teto)

### ETAPA 10 — Sinais de Alerta (Quando Parar/Recuar)

**Frameworks de recuo e diagnóstico de saturação (rode quando algum sinal disparar):**
- **Scale-Down Rules (PGS reverse)** (rode `scale-down rules decrease budget 20% 7-day CPA exceeds target safety net`) — quando o CPA de 7 dias estoura, corta 20% e segura (não desliga). É a regra dura por trás de "derruba o surf" / "volta pro último nível bom".
- **Spend Redistribution Framework (Don't Kill the Top Spender)** (rode `spend redistribution framework do not turn off top spender ROAS drops higher budget`) — quando o ROAS cai ao subir budget, redistribui em vez de matar o top spender (matar reseta aprendizado).
- **Frequency as Prospecting-vs-Retargeting Proxy** (rode `frequency prospecting vs retargeting proxy low 1.0 high 2.5 broad CBO scaling signal`) — lê frequency como sinal de saturação: baixa (~1.0) = ainda prospectando (pode subir), alta (~2.5) = virou retargeting disfarçado (audiência saturada, pede batch novo).

- **CPA dos últimos 3 dias acima do breakeven** → para de subir budget, refresh criativo antes de qualquer escala. Na Escola A, derruba o surf.
- **Frequency em todos os ad sets > 1.5** → audiência saturada, precisa batch novo (08).
- **CPM subindo 30%+ em 14 dias** → saturação, competição, ou conta cansada. Diagnóstico na skill 11; se for conta, abrir conta nova legítima (ETAPA 4.5).
- **Budget novo não gasta / trava entrega** → diagnóstico ETAPA 4.5 (conta vs produto), não conclua "teto" cedo demais.
- **Cash flow gap** → spend correndo na frente do payout. Ajustar pace (ETAPA 6).
- **Fulfillment bottleneck** → estoque/3PL não acompanha. Nunca escale acima da capacidade operacional — venda que não entrega vira chargeback e ban.

### Quando 12 recomenda voltar para 08 (ciclo explícito)

Se algum destes → invoque skill 08 pra novo batch:
- Top 3 criativos com > 14 dias de idade
- Frequency max > 1.4 com CTR caindo > 20% vs baseline
- Escala cruzou 2× budget (precisa creative diversity pra sustentar)
- Conta nova aberta (ETAPA 4.5) precisa de criativo pra alimentar

Skill 08 lerá `11-ad-analysis/NEXT_BATCH_IDEAS.md` (de 11) + `12-scale-engine/scale-directives.md` (gerado abaixo).

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome. O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, **logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**, componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/12-scale-engine/` antes de salvar.

Outputs em `workspace/[produto]/12-scale-engine/`:

- `relatorio.md` contendo:
  1. Classificação de estágio + sub-fase de escala (Etapa 2)
  2. Análise de prontidão com bloqueios identificados (Etapa 3)
  3. **Escola de escala escolhida** + setup operacional concreto (cost cap value / bid cap + budget / cadência de doubling) (Etapa 4)
  4. Política de conta nova quando entrega trava (Etapa 4.5)
  5. Credibilidade da loja — gaps a resolver (Etapa 5)
  6. Cash flow check + gap projetado (Etapa 6)
  7. Projeção 30/60/90 base + pessimista + template cash flow (Etapa 7)
  8. Creative diversity plan (Etapa 8)
  9. Checklist operacional semanal (Etapa 9)
  10. Sinais de alerta (Etapa 10)

- `scale-directives.md` (fecha ciclo 12→08):
  - Budget atual + budget alvo (30d)
  - Escola de escala em uso + ritmo de criativo que ela exige
  - PSM real atual
  - Sinais que trigam volta pra 08 (creative refresh)
  - Bloqueios de cash flow (se houver)

- `dados.json` (JSON companion):

```json
{
  "plan_id": "uuid",
  "product_slug": "...",
  "stage": "starter|validating|scaling",
  "scale_phase": "testing|traction|initial_scale|aggressive|optimization",
  "scaling_school": "A_cost_cap_surf|B_bid_cap|C_budget_doubling",
  "current_daily_spend": 0,
  "target_daily_spend_30d": 0,
  "breakeven_cpa": 0,
  "max_cpa": 0,
  "psm_real": 0,
  "psm_theoretical": 0,
  "readiness_blockers": [],
  "vertical_plan": {
    "cost_cap_value": null,
    "cost_cap_duplication_steps": [],
    "bid_cap_value": null,
    "bid_cap_budget": null,
    "doubling_cadence_days": null,
    "surf_enabled": false
  },
  "new_account_policy": {
    "trigger": "delivery_throttled_or_account_cpm_too_high",
    "legitimate_only": true
  },
  "cash_flow": {
    "cash_gap_projected": 0,
    "safe_to_escalate": true
  },
  "triggers_back_to_08": [
    "top_3_creatives_older_than_14_days",
    "frequency_max_over_1.4_with_ctr_drop_over_20pct",
    "scaled_past_2x_budget",
    "new_account_opened_needs_creative_fuel"
  ]
}
```

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `12-scale-engine` em `skills_completed`
- Registrar `plan_id`, `psm_real`, `scaling_school`
- Gravar `manifest.stage` com o vocabulário canônico (`starter` | `validating` | `scaling`). Se a sub-fase de escala importar, ela vive em `scale_phase` no `12-scale-engine/dados.json` — **NUNCA** em `stage`.
- Se o membro graduou de stage durante esta análise (ex: `validating` → `scaling`), atualizar `manifest.stage` e avisar (ver `member-stage-awareness.md`).
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html, onde `<slug>` é o product_slug).

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`). Apresente a escola recomendada como ponto de partida e convide ajuste.

**Se PRONTO pra escalar:**
"Plano de escala pronto (draft). Recomendei a **Escola [X]** pro seu stage: [setup concreto — cost cap $Y / bid cap $Z budget $W / dobra a cada 3 dias]. Quer rodar essa ou prefere outra das três? Roda o checklist semanal e me volta daqui a 30 dias ou quando precisar re-analisar — diga **'ad analysis'** com os dados atualizados."

**Se NÃO PRONTO (algum bloqueio):**
"Antes de escalar, [N] bloqueio(s) a resolver: [listar]. Ação por bloqueio:
- [Bloqueio 1] → [ação + skill]
- ...
Sem winner provado / com PSM abaixo do esperado, escalar só queima budget mais rápido. Resolve isso e diz **'scale'** de novo que eu monto o plano."
