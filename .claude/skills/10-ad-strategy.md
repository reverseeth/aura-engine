---
name: ad-strategy
description: Engine de configuração e CRIAÇÃO da estrutura de teste no Meta Ads Manager — 1 campanha com CBO (Advantage+ / broad, Max Conversion) → 1 ad set por conceito (3 criativos + 2 primary texts + 2 headlines), cada ad set com o `testing_method` do conceito (lido de `concepts[].testing_method` da 08) e o destino de página do mapeamento de congruência da 08 ETAPA 6 (fallback: URL canônica do manifest), com o nº de conceitos governado pela capacidade de teste do cânone `.claude/lib/ad-taxonomy/README.md` §1 (criativos = budget diário ÷ target CPA, piso de US$ 100-150/dia, teto de ~3× target CPA por ad set, máximo 5 ad sets abaixo de US$ 1k/dia), 3 dias sem mexer, 1 conta por produto, warmup de conta nova, cadência quarta→domingo (domingo = checkpoint de decisão informada via Skill 11, nunca kill por calendário sozinho). Cria tudo em PAUSED via Meta Ads MCP (membro revisa e ativa), com gates pre-launch, leitura de credibilidade da loja e as proteções que funcionam em CBO (ad set daily maximum + as duas automações do cânone §6). Use quando o membro disser "ad strategy", "estratégia de ads", "montar campanha", "setup Meta Ads", "configurar campanha", ou após os briefings de criativos estarem prontos.
---

# Ad Strategy Engine

## Quando Usar
Quando o membro tem criativos prontos (da Skill 08) + página pronta na loja (cadeia 07a/07b) + tracking validado (07c) + oferta ativa (Skill 04), e precisa configurar **e criar** a estrutura de teste no Meta Ads Manager. Essa skill não é "estratégia conceitual" — é a **camada de execução**: monta a campanha exata e a cria em PAUSED via MCP pro membro revisar e ativar.

A teoria de diagnóstico (PSM, 4Pi, ROAS targets) continua viva como **leitura** — a Skill 11 (ad-analysis) lê por ali. O que esta skill entrega é o "exatamente o que fazer no Ads Manager" pra validar criativo.

> **Cânone desta skill:** `.claude/lib/ad-taxonomy/README.md` — **§1** (capacidade de teste, piso/tetos de budget e a estrutura CBO + 1 ad set por conceito), **§6** (o que pode e o que não pode ser automatizado) e **§7** (métodos de teste Marksman/Sniper e a distinção ângulo ≠ conceito). Esta skill **não redefine** essas réguas — ela as aplica ao produto do membro. Onde o texto abaixo divergir do cânone, o cânone vence.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, com o mapa skill→domínio). Os domínios desta skill são `meta-ads-strategy` (estrutura/budget/escala) e `persuasion-psychology` (credibilidade/gestão de comentários).
>
> **Contrato de cobertura (README do kb-index, revisado 2026-09):** no início de cada ETAPA que consulta a base, abra o `frameworks.json` e **enumere TODAS as entradas desses domínios cujo `use_in_skill` inclua a 10** — as queries embutidas no texto desta skill são o **núcleo mínimo garantido de cada etapa, nunca o teto**: entrada relevante pra fase que não está embutida aqui É PARA SER PUXADA do mesmo jeito. Rode a `best_query` exata de cada entrada relevante com `deep=true`; **NUNCA use query genérica** ("ads strategy", "como configurar campanha"). O critério de relevância é por FASE ("esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa); não repita busca de framework já puxado na mesma sessão; e antes de fechar cada ETAPA, releia a lista enumerada e confirme que nenhuma entrada relevante ficou sem puxar. **Contagem de entradas por domínio não vive no texto de skill: a fonte da verdade do tamanho de cada domínio é sempre o próprio `frameworks.json`.**

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)
- [ ] `workspace/[produto]/08-creative-engine/dados.json` existe (os conceitos prontos — **cada conceito vira 1 ad set**, com seu pack 3-2-2; o handoff é `concepts[].id` + `concepts[].testing_method`, que a ETAPA 3.2 respeita conceito a conceito). Quantos conceitos ENTRAM no teste é decidido pela capacidade da ETAPA 3.1, não pelo tamanho do batch
- [ ] `workspace/[produto]/04-offer-builder/dados.json` existe (`unit_economics.target_cpa_primary_2x` — o **target CPA**, que é o divisor da fórmula de capacidade; `unit_economics.weighted_margin_per_order` — o breakeven CPA; `breakeven_roas`). **Se `manifest.target_cpa`/`manifest.breakeven_roas` existirem, eles PREVALECEM sobre os valores do 04**: a 04 os grava no manifest, e a 07d os ATUALIZA quando o escopo real das alavancas de checkout mudou a economics (`07d-checkout-aov/dados.json.aov_reconciliation.scope_diff` não-vazio + aplicado na loja) — o manifest carrega o recálculo mais recente; o dados.json do 04 é a projeção original
- [ ] `workspace/[produto]/profile.md` existe (budget diário, stage, conta do Meta Ads ativa) — o budget diário numérico canônico é `manifest.budget_daily`, o segundo termo da fórmula de capacidade
- [ ] **`manifest.margin_warning` lido**: se `true` (a Skill 04 flagou margem ponderada < $20/pedido), manter o teste no **piso operacional** da ETAPA 3.1 (US$ 100-150/dia) e reduzir o número de conceitos em vez de esticar budget, AVISANDO o membro que a margem apertada reduz o espaço de erro do CPA — subir budget só depois de revisar a margem na 04
- [ ] **`report_language`** lido (default `pt-BR`) — ver "Contexto a carregar"
- [ ] Tracking validado via Skill 07c: `manifest.tracking.tracking_ready == true` (Pixel + CAPI, EMQ ≥ 6.0 na escala 0-10 do Events Manager). **`emq_pending: true` é aceito** (loja pré-launch sem tráfego: o EMQ só calcula com eventos reais — a 07c validou instalação + Purchase por pedido-teste): prosseguir, avisando o membro que **a Skill 11 re-lê o EMQ no dia 3 de tráfego** e EMQ < 6.0 pós-tráfego = ação corretiva na 07c antes de qualquer decisão de kill/escala. Se `tracking_ready != true`, redirecionar pra `'tracking'` antes — sem evento de Purchase confiável, Max Conversion não otimiza.
- [ ] `manifest.storefront.page_url` preenchido (a página publicada pela 07b — a URL CANÔNICA de destino da campanha e o fallback do destino por conceito da ETAPA 3.3). Se vazio, redirecionar pra `'build page'` (07b) antes.

Se algum arquivo crítico sumiu/corrompeu, aplicar `.claude/rules/emergency-escape-paths.md` (ES1/ES2): oferecer **(A)** re-rodar a skill que gera o arquivo, ou **(B)** proceder com default e marcar `manifest.skipped_preflight`. Nunca abortar sem ≥ 2 caminhos.

### Contexto a carregar

1. Leia `workspace/profile.md`. **Leia `report_language`** (default `pt-BR` se ausente; também em `manifest.report_language`): TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language`.
2. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (se não existir, leia o legado `relatorio.md`) + `04-offer-builder/dados.json` — daqui saem os **dois** números que governam esta skill: o **target CPA** (divisor da capacidade de teste) e o **breakeven CPA** (piso de margem, base dos critérios de kill da Skill 11). **Ordem de precedência de `target_cpa`/`breakeven_roas`:** primeiro `manifest.target_cpa`/`manifest.breakeven_roas` (se presentes — a 04 grava, e a 07d atualiza quando o escopo de alavancas de checkout aplicado mudou a economics); só na ausência deles, os valores de `04-offer-builder/dados.json`. **Fontes canônicas (as MESMAS que a Skill 11 e a 12 usam):** `target_cpa = unit_economics.target_cpa_primary_2x` e `breakeven_cpa = unit_economics.weighted_margin_per_order`. Use os campos diretos — não re-derive. Só se faltarem, caia pros fallbacks `breakeven_cpa = AOV / breakeven_roas` e `target_cpa = breakeven_cpa / 2`, marcando `data_gap` no dados.json. **O target lido aqui vira setpoint da campanha — antes disso ele passa pela checagem contra o piso físico de CAC da ETAPA 3.1 (item 1b).**
2b. Leia `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** → bloco `cac`, três campos: `cac_floor_reference_usd`, `cac_max_first_order` e `target_reachable_vs_floor`. A skill 15 é quem confronta o CPA-alvo da oferta contra o chão físico do leilão (cânone `.claude/lib/unit-economics/README.md` §3) e publica o veredito; esta skill **lê e aplica na ETAPA 3.1, nunca recalcula**. **Fallback (arquivo ausente, ou `target_reachable_vs_floor: "unknown"`):** vale o comportamento de hoje — o target entra direto na fórmula de capacidade, apoiado no check 12 da Skill 04, que já barra teto de CAC abaixo de US$ 25 na hora de montar a oferta. A 15 nunca é pré-requisito desta skill.
3. Leia o cânone `.claude/lib/ad-taxonomy/README.md` — **§1** (capacidade de teste + estrutura), **§6** (automações) e **§7** (métodos de teste). É a fonte de verdade de quantos criativos o budget consegue ler e de como a campanha é montada; a ETAPA 3 só aplica essas réguas.
4. Leia a **URL de destino** de `manifest.storefront.page_url` (gravada pela 07b no deploy — a PDP/landing publicada). Essa é a fonte canônica da URL da campanha e o **fallback do destino por conceito**: o destino de cada ad set vem do mapeamento de congruência da **ETAPA 6 da 08** (ETAPA 3.3 abaixo) e cai nessa URL canônica quando o mapeamento não existe ou a página mapeada não está publicada. NUNCA tirar URL do relatório da 06 (copy não é deploy — a página pode ter mudado de handle na publicação).
5. Leia `workspace/[produto]/08-creative-engine/dados.json` (os conceitos do batch — cada um com seu pack 3-2-2 e seu `testing_method`; cada conceito é candidato a 1 ad set de teste) e o **mapeamento de congruência da ETAPA 6 da 08** no relatório dela (`creative-engine.md`, fallback legado `relatorio.md` — a tabela conceito→LP e a linha "Destino" de cada briefing), que alimenta o destino por conceito da ETAPA 3.3.
6. Detecte o **stage** do membro (`.claude/rules/member-stage-awareness.md`): starter / validating / scaling. Define tom e agressividade da recomendação. **O número de criativos NÃO vem do stage — vem da capacidade de teste (ETAPA 3.1).**
7. Puxe os **SISTEMAS NOMEADOS** da base como camada de LEITURA/diagnóstico (não de execução de estrutura) — rode `search_knowledge` com a `best_query` de cada um, nunca query genérica. O que sustenta esta skill como leitura:
   - **Scientific Method for Meta Ads (Control vs Variable)** (rode `scientific method meta ads control variable environmental impact`) — por que cada ad set carrega UM conceito só: o conceito é a variável, tudo o mais fica congelado.
   - **4Pi Analysis (Spend, Frequency, CPM, Cost per Result)** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) — a leitura que a Skill 11 aplica nos dados.
   - **Profitable Scaling Margin (PSM) — Golden Ratio of Growth** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) — o número de saúde que governa quando escalar (Skill 12).
   - **True Broad vs Advantage+ Broad** (rode `True Broad vs Advantage Plus broad targeting training wheels`) — por que a audiência é broad e o criativo faz o targeting.

   A EXECUÇÃO operacional (estrutura de campanha abaixo) é o playbook desta skill; os outros frameworks de `meta-ads-strategy` (escala, redistribuição de spend, lucky vs durable wins) estão no índice `.claude/lib/kb-index/` e entram via Skill 11/12.

### Analytics stack — quem decide
A escolha da stack de atribuição (Meta App / Wetracked / Triple Whale / Aimerce) é da **Skill 07c (tracking-setup)**, não desta. Aqui só **confirmamos** que existe stack validada antes de criar campanha: ler o bloco `manifest.tracking` gravado pela 07c. Se `manifest.tracking.tracking_ready != true` OU `manifest.tracking.analytics_stack` estiver vazio → redirecionar pra `'tracking'` (07c) e parar. Sem atribuição confiável, a Skill 11 lê dado ruim e mata criativo bom.

### Compatibilidade
Testada em Meta Ads Manager **2026 Q2** e Meta Marketing API **v21.0+**. Se o membro usa interface legada (Business Suite antigo) ou API anterior, adaptar passos visuais manualmente.

## Fluxo da Skill

### ETAPA 1 — Gates de Pré-Launch (BLOQUEANTES)

**Gate de consistência (Skill 09)** — ler `workspace/[produto]/09-consistency-audit/dados.json`:
- `launch_recommendation == "BLOCK"` → **ABORTAR**. Drift entre criativos/copy/oferta vira disapproval ou mismatch ad↔landing. Mostrar findings críticos e pedir `consistency audit` após corrigir. Override só com `compliance_override` no manifest.
- `CAUTION` → mostrar warnings, pedir OK explícito antes de prosseguir.
- `GO` → seguir.
- **Arquivo ausente → rodar a Skill 09 INLINE agora, por default.** A auditoria é barata (minutos, sem custo externo) e é o gate canônico de launch — não faz sentido criar campanha sem ela. Avisar o membro ("antes de montar a campanha, vou rodar a auditoria de consistência — leva uns minutos e evita ad reprovado por drift"), rodar a 09, e aplicar o resultado nas regras acima. Pular a auditoria só com recusa EXPLÍCITA do membro — nesse caso marcar `manifest.skipped_preflight += ["09-consistency-audit"]` e avisar no output final que a campanha nasce sem o gate de consistência (drift entre oferta/copy/ads vira disapproval ou mismatch ad↔landing).

**Pre-launch gates (NON-NEGOTIABLE — `.claude/rules/pre-launch-gates.md`)** — ANTES de criar qualquer campanha/ad set/criativo (PAUSED ou não), rodar os dois gates:

- **GATE 1 — Ad-flag Compliance**: salvar a copy de cada ad (primary text + headline + descrição + URL de destino) num arquivo temporário e rodar a CLI canônica: `python3 .claude/lib/compliance-preflight/run.py --file <arquivo> --vertical <manifest.product_vertical> --stage pre_ad --json` (pra trecho curto, `--text "<string>"` no lugar de `--file`). Ler `overall_verdict` do JSON de saída: `critical` → **BLOCK**: aplicar as `rewrite_suggestions[]` e re-rodar; se não passar, parar e pedir revisão. `warning` → **BLOCK por default** (protocolo do GATE 1): aplicar as `rewrite_suggestions[]` e re-rodar o check; se virar `pass`, seguir; se persistir, logar em `workspace/[produto]/compliance-warnings.json` e notificar o membro no output final — go-live só com decisão explícita dele. `pass` → seguir. Bypass só via `manifest.compliance_override` com risco reconhecido (`.claude/rules/emergency-escape-paths.md` ES3 — exige o membro digitar "EU ACEITO O RISCO").
- **GATE 2 — Promise ↔ Config**: validar cada promessa da copy/ad (free shipping, money-back, discount code, "limited time", reviews) contra a config real da loja Shopify. Output em `workspace/[produto]/promise-check.json`. `fail` ≥ 1 → **BLOCK** com `fix` (ajustar copy OU ajustar config); `warn` → apresentar pra decisão; tudo `pass` → prosseguir. Zero bypass automático.
- **GATE 3 — Disclosure "AI Info" (Meta)**: ler `08-creative-engine/dados.json.concepts[]` — todo concept com `ai_disclosure_required: true` (humano fotorrealista gerado por AI, gate I da ETAPA 4.5 da 08) precisa do label **"AI Info"** marcado no nível do ad (a receita `upload-creative-to-meta.md` marca/verifica no upload). A campanha NÃO vai ao ar sem o membro confirmar o label desses ads no Ads Manager — com o label correto não há penalidade de entrega; sem ele, distribuição reduzida ou remoção (`.claude/rules/pre-launch-gates.md`).

### ETAPA 2 — Leitura de Credibilidade da Loja (lever de conversão, pré-launch)

Antes de gastar em tráfego, a loja precisa **parecer confiável** — isso afeta conversão direto, e tráfego pago em loja sem prova social queima budget. Esta etapa é um **checklist de leitura**, não bloqueante por default (vira WARN), mas o membro precisa ver o gap antes de ativar.

**Fundamente a leitura de credibilidade nos SISTEMAS NOMEADOS (rode a `best_query` de cada um — nunca query genérica):**
- **Cialdini's Six Weapons of Influence** (rode `Cialdini six weapons of influence reciprocity commitment social proof authority liking scarcity`) — social proof e authority são as alavancas que a PDP/página de FB precisam exibir antes do tráfego chegar.
- **Bandwagon Effect (3 Group Types)** (rode `bandwagon effect aspirational associative dissociative groups social pressure conformity`) — por que ~100 reviews em inglês move conversão (massa visível = "todo mundo compra").
- **Inoculation Theory** (rode `inoculation theory McGuire weakened attack pre-emptive defense competitor argument resistance`) — base pra responder objeção nos comentários do ad antes que o ceticismo contamine o leitor seguinte.
- **Length-Implies-Strength Heuristic** (rode `length implies strength heuristic volume of content persuasion cue numbered reasons testimonials`) — volume de review/UGC sinaliza força mesmo antes de ser lido.

Verificar (e reportar o que falta):

- **Instagram + página do Facebook ativos**, com seguidores reais e posts recentes (a página do FB é o que aparece como anunciante no ad).
- **Reviews na PDP** — alvo ~100 avaliações em inglês (do mercado US). Menos que isso, conversão sofre. (A cadeia 07 já injeta reviews; aqui só confirmamos volume.)
- **Sinais de confiança visíveis**: brand story / About, destaques (TrustPilot se tiver), garantia clara, política de envio/retorno legível.
- **Flows de recuperação ativos (13 Fase A)**: abandoned cart + post-purchase configurados no ESP e ATIVADOS antes do go-live — é a receita mais barata do launch (recupera parte dos ~70% de carrinhos abandonados a custo zero, free tier do ESP). Se `manifest.retention.phase_a_done != true`, recomendar rodar `'retention'` (13 Fase A) antes de ativar a campanha — WARN, não bloqueia.
- **Gestão de comentários — o ponto mais importante**: comentário ruim num post de ad fica **visível pra todo mundo** e derruba conversão. O membro precisa de uma rotina pra **deletar/ocultar spam e responder objeção** nos comentários dos ads. Recomendar verificar comentários nos primeiros dias e responder rápido.

**Zero reviews → primeiras reviews (playbook legítimo, por stage):** loja nova não fica esperando review "acontecer" — constrói as primeiras com processo:

1. **Seeding de produto (starter/validating):** enviar 20-30 unidades pra micro-influencers e membros de comunidades do nicho em troca de **review honesta** (com disclosure de produto recebido). Custo = COGS de 20-30 unidades; retorno = as primeiras dezenas de reviews reais + UGC aproveitável nos criativos.
2. **Review request retroativo via app:** se a loja já teve QUALQUER venda (orgânica, amigos, marketplace), o app de reviews (Judge.me/Loox/Yotpo) dispara request pra compras passadas — recupera reviews que já existiam como clientes.
3. **Incentivo no pós-compra (13 Fase A):** o Email 3 do flow post-purchase (dia 7-10) pede a review com incentivo — cada venda do launch alimenta o contador automaticamente.
4. **Brinde por foto/review (coordenar com a 05):** GWP ou desconto na próxima compra em troca de foto + review honesta — foto real de cliente vale mais que texto.

**Guardrail explícito (PROIBIDO, sem exceção):** comprar reviews; importar reviews de OUTRO produto (ex: import de AliExpress de um listing diferente); ou condicionar o incentivo a review POSITIVA — incentivo é por review **honesta**, qualquer nota (condicionar a nota viola FTC e a policy das próprias review apps, e derruba a loja quando descoberto).

**Honestidade (não grey-hat):** NÃO recomendar comprar seguidor/comentário/review fake em volume. Além de risco pra conta e pra marca, prova social falsa não sustenta a venda — o foco é prova social **real** (reviews de clientes, UGC, depoimentos). Se a loja está fraca em prova social, isso é um sinal de que talvez seja cedo pra escalar budget — melhor começar menor e acumular review real (o playbook acima acelera exatamente isso).

Stage: pra **starter** sem prova social ainda, deixar explícito que rodar com budget pequeno enquanto acumula review é o caminho. Pra **scaling**, isso já está resolvido — só confirmação rápida.

### ETAPA 3 — Capacidade de Teste e Estrutura (o playbook)

A estrutura de teste do Aura é **enxuta de propósito**. Uma campanha só, com o budget no nível dela (CBO), e cada conceito num ad set próprio: assim o algoritmo redistribui entre os conceitos sozinho, e **onde ele concentra gasto é o sinal** que a Skill 11 vai ler. E o **criativo faz o targeting** — por isso a audiência é broad/Advantage+, sem detailed targeting.

Antes de qualquer coisa: **quantos criativos este budget consegue LER?** Essa pergunta vem primeiro que "quantos criativos eu tenho" — é a ETAPA 3.1, e ela governa todo o resto.

**Ancorar a estrutura nos SISTEMAS NOMEADOS (rode a `best_query` de cada um — nunca query genérica):**
- **Full Media Buying 2026 — estrutura consolidada da fonte primária (5 camadas)** (rode `estrutura full media buying 2026 cinco camadas main CBO ABO zombie raw content promo`) — o mapa vigente da conta inteira. A campanha que esta skill monta É a camada 1: a **CBO principal de aquisição** (broad, ads manuais 3:2:2, mínimo US$ 100/dia). As outras 4 camadas — ABO de teste/escala pra winners provados, Zombie em cost cap, Raw Content CBO a partir de US$ 3-10k/dia, Promo CBO com data — entram via Skills 12/14, nunca nascem aqui.
- **Coliseu / Spend-as-Verdict (sem campanha de teste separada)** (rode `testar direto no coliseu ad sem spend é ad ruim falsos winners forced spend`) — a filosofia por trás do "onde o gasto se concentra é o sinal": o ad novo prova valor DENTRO da CBO escalável, disputando contra os melhores ads existentes, com leitura binária — **ad sem spend é ad ruim**, e forçar spend em ad "resgatado" fabrica falso winner (500 ads testados e 60-70 resgates por spend forçado produziram zero winner sustentado, enquanto a CBO rodava 3-4×).
- **Promo Campaign (Broad / WARM60 / HOT90)** (rode `promo campaign CBO três ad sets broad WARM60 HOT90 retargeting só em sale`) — estrutura usada em janelas promocionais com data de fim (a exceção (a) do Scaling Protocol, cânone §5): 1 CBO com 3 ad sets — Broad, WARM60 e HOT90 — rodando em paralelo ao evergreen. NÃO é a campanha de teste desta skill e não substitui a estrutura abaixo; o playbook completo de promo é da skill **17-promo-engine** (em criação) — aqui fica só o registro de que a estrutura existe e de onde ela entra.
- **One Campaign Method (AndroMeta One Architecture)** (rode `One Campaign Method AndroMeta One CBO control variable ad set structure`) — a arquitetura de campanha única com CBO que esta etapa monta (registrada no índice como visão alternativa nomeada; o mapa consolidado vigente é o Full Media Buying 2026 acima).
- **Andromeda System (5 Core Principles)** + **Before vs After Andromeda Mental Model Shift** (rode `Andromeda 5 principles one campaign method scaling Meta Ads` e `Andromeda before after mental model creative defines targeting`) — o princípio "o criativo define o targeting", base da audiência broad.
- **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) — o risco real do CBO (um ad ruim forçando spend) e por isso as proteções da ETAPA 6 (daily maximum) existem.
- **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`) — por que cada criativo precisa de mais ou menos 1× target CPA por dia pra ser legível, e por que não se desliga o que mais gasta no meio da leitura.

#### 3.1 — Capacidade de teste (resolver ANTES de escolher quantos criativos sobem)

Régua canônica (`.claude/lib/ad-taxonomy/README.md` §1):

```
max_assets  = floor(budget_diário ÷ target_cpa)          → criativos simultâneos com chance justa
max_adsets  = floor(budget_diário ÷ (3 × target_cpa))    → conceitos simultâneos (1 ad set = 1 conceito = 3 criativos)
```

O exemplo do cânone: **US$ 160/dia com target CPA de US$ 80 = 2 assets.** Não 5, não 12. Criativo que recebe menos de ~1× target CPA por dia não acumula dado suficiente pra ser lido — o teste devolve ruído com cara de resultado, e a Skill 11 classifica ruído.

**As quatro restrições valem JUNTAS (cânone §1, todas obrigatórias):**

| Restrição | Número | Por quê |
|---|---|---|
| Piso operacional | **US$ 100-150/dia** | Abaixo disso não há teste, há palpite — o Meta nem acha compra suficiente pra otimizar |
| Teto por ad set | **~3× target CPA/dia** | É exatamente o que um conceito de 3 criativos precisa pra dar ~1× CPA/dia a cada um. Acima disso o ad set não lê melhor, só gasta mais |
| Teto de ad sets de teste | **5**, enquanto o budget diário está abaixo de US$ 1k/dia | Mais que isso espalha o CBO fino demais e nenhum conceito fecha leitura |
| Teto do batch | `ad sets ≤ conceitos disponíveis no 08` | Não existe ad set de teste sem conceito pra colocar dentro |

**Ordem de cálculo (aplicar nesta sequência e gravar cada número no dados.json):**

1. `target_cpa` — `manifest.target_cpa`; na ausência, `04-offer-builder/dados.json.unit_economics.target_cpa_primary_2x`.
1b. **Validar o `target_cpa` contra o piso físico de CAC ANTES de usá-lo como divisor** (só quando `15-finance-engine/dados.json` existir — Contexto, item 2b). O leilão tem um chão dado por CPM e CTR: no melhor caso realista o CAC mínimo em escala fica na faixa `cac.cac_floor_reference_usd` (US$ 15-25, cânone §3). Um alvo abaixo desse chão não é um alvo apertado, é um alvo que não existe — e ele **infla a capacidade de teste**: quanto menor o divisor, mais criativos a fórmula do passo 3 autoriza, e o teste sobe com mais conceitos do que o budget consegue de fato ler.

   | `cac.target_reachable_vs_floor` | O que fazer |
   |---|---|
   | `yes` | Seguir. O alvo cabe acima do chão; a capacidade calculada é real |
   | `no` | **Não silenciar e não ajustar o alvo por conta própria.** Calcule a capacidade também com o piso da 15 (`cac_floor_reference_usd`, ponta alta) no lugar do target e mostre os dois números ao membro: é a diferença entre quantos conceitos ele *acha* que consegue testar e quantos o leilão deixa. Diga a causa sem rodeio — alvo abaixo do piso é problema de **AOV**, não de mídia, e a saída é a 04 (subir AOV/preço ou sustentar com LTV medido), nunca "criativo melhor". Rode o teste pela capacidade conservadora e registre `cac_floor_check.binding: true` |
   | `unknown` / campo ausente | Fallback: seguir com o target como hoje (o check 12 da Skill 04 já barrou teto de CAC abaixo de US$ 25 na montagem da oferta) |

   Leia também `cac.cac_max_first_order` — é o CAC em que o **primeiro pedido empata**. Ele não entra na fórmula de capacidade (o divisor continua sendo o `target_cpa`), mas é o número que contextualiza o teto de gasto por ad set no relatório: acima dele, cada compra nova do teste é deficitária no primeiro pedido, o que pode ser decisão consciente (LTV medido) ou acidente.
2. `budget_diário` — `manifest.budget_daily` (fallback: linha "Budget diário" do `profile.md`).
3. `max_assets = floor(budget_diário ÷ target_cpa)` e `max_adsets = floor(budget_diário ÷ (3 × target_cpa))`.
4. `adsets_planejados = min(max_adsets, nº de conceitos do batch 08, 5 se budget_diário < 1000)`. Se `max_adsets` der **0**, o resultado não é "não rodar" — é o primeiro caso de contorno abaixo (1 conceito por vez).
5. `test_budget_daily = min(budget_diário, adsets_planejados × 3 × target_cpa)`, respeitando o piso operacional. Se o próprio `budget_diário` do membro já está abaixo do piso, o piso não pode ser "aplicado" gastando dinheiro que ele não tem — cai no segundo caso de contorno.
6. `assets_planejados = adsets_planejados × 3`.

**Casos de contorno (todos precisam de resposta explícita, nenhum se resolve diluindo):**

- **`max_assets < 3`** — o budget não paga um pack 3-2-2 inteiro. Não dilua: rode **1 conceito por vez**, em fila — sobe o conceito do dia e, quando o próximo entra, sai o mais velho que não pegou tração. Um conceito lido de verdade vale mais que três conceitos ilegíveis.
- **Budget abaixo do piso de US$ 100/dia** — não finja que dá. Dois caminhos honestos, apresentar os dois: **(a)** adiar o teste até o caixa alcançar o piso (leitura limpa, sem desperdício), ou **(b)** rodar com **1 conceito só**, sabendo que o resultado é **direcional e não autoriza decisão de kill nem de escala** — a Skill 11 lê com essa ressalva. Nunca apresente (b) como "teste".
- **Capacidade maior que o batch** (`max_adsets` > conceitos disponíveis) — o excedente NÃO vira budget a mais nos mesmos ad sets: isso estoura o teto de ~3× target CPA por ad set e não compra leitura nenhuma. Ou volta pra Skill 08 por mais conceitos, ou o budget excedente fica fora do teste.
- **`manifest.margin_warning: true`** — ficar no piso operacional e cortar conceitos, nunca esticar budget. Margem apertada não muda a fórmula; muda quanto erro o membro aguenta.
- **CPA-alvo abaixo do piso físico de CAC** (`cac.target_reachable_vs_floor: "no"`, item 1b) — a capacidade calculada com esse alvo é fictícia, e rodar por ela sobe mais conceito do que o budget lê. Use a capacidade conservadora do item 1b e mande a correção pra 04 (AOV/preço), não pra mídia.

**O stage não define o número** (`.claude/rules/member-stage-awareness.md`) — a capacidade define. O stage define como os caminhos são apresentados: pra **starter** abaixo do piso, o caminho recomendado é adiar e acumular caixa (dito sem rodeio); pra **validating**, a restrição que costuma morder é a capacidade; pra **scaling**, a restrição que costuma morder é o tamanho do batch da 08 e o teto de 5 ad sets abaixo de US$ 1k/dia.

#### 3.2 — Método de teste: Marksman ou Sniper (cânone §7 — lido POR CONCEITO da 08)

**O método não se decide aqui — se LÊ.** A Skill 08 grava `concepts[].testing_method` (`marksman|sniper`) e constrói cada pack NAQUELE método: pack Marksman já vem com 3 ângulos distintos sob hold universal validado, pack Sniper já vem com 1 ângulo em 3 execuções. Re-decidir o método na 10 não muda o que os criativos são — só desalinha o registro e quebra a leitura da 11 (que pergunta "qual ângulo venceu?" num pack Marksman e "qual execução venceu?" num Sniper). Portanto:

- **Batch com `testing_method` por conceito (padrão da 08 desde 2026-09):** RESPEITAR o campo, conceito a conceito. Um batch pode ser misto (ex: 2 conceitos `marksman` + 1 `sniper`) — cada ad set carrega o método do SEU conceito, gravado em `ad_sets[].testing_method` no dados.json. O `test_method` batch-level vira resumo: o método único quando todos coincidem, `mixed` quando variam.
- **Fallback (batch legado da 08 sem o campo):** classificar aqui pela regra prática do cânone — **imagens → Marksman; vídeos → Sniper; toda iteração → Sniper** — e gravar por ad set do mesmo jeito, marcando `data_gap` no dados.json (a classificação foi inferida nesta skill, não construída na 08).

| Método | Quando | Como vira estrutura aqui |
|---|---|---|
| **Marksman** | primeiro teste, ou quando a performance platôa | **3 ângulos diferentes DENTRO de um pack 3-2-2 = 1 ad set.** As 3 execuções do mesmo conceito carregam ângulos distintos |
| **Sniper** | a direção já existe (ângulo com tração) — e **toda iteração** depois da leitura da Skill 11 | **1 ângulo, 3 execuções** = 1 ad set com o pack 3-2-2 |
| **Shotgun** | só no pipeline de conteúdo de creators (product seeding) | volume sem estratégia individual; não é estratégia criativa deliberada |

> **Correção importante (2026-09-01): Marksman acontece DENTRO de um ad set, não entre ad sets.** O material é literal — *"Marksman (rajada de 3 tiros — testa 3 angles diferentes num único 3:2:2)"*, com o caso real do conceito "superlatives" (variação 1 "world's first stainless steel", 2 "world's easiest to clean", 3 "world's first doctor-designed"). O conceito é a **embalagem** e continua sendo um só ad set; o que varia entre as 3 execuções é o **ângulo**. Espalhar 3 ângulos em 3 ad sets não é Marksman — e a leitura do resultado fica pior, porque o CBO passa a repartir budget entre ad sets antes de você conseguir comparar os ângulos entre si.

**Consequência para o mapeamento:** o método NÃO muda quantos ad sets existem — isso é decidido só pela capacidade da 3.1 (`max_adsets`). O que o método muda é **o que varia dentro de cada pack**. Um batch com 3 conceitos vira 3 ad sets independente de ser Marksman ou Sniper; a diferença é se as 3 execuções de cada pack testam 3 ângulos (Marksman) ou 3 execuções do mesmo ângulo (Sniper).

**Ângulo ≠ conceito** (cânone §7). Ângulo é a **razão de compra em frase** ("para de virar de um lado pro outro a noite toda"). Conceito é a **embalagem** (comparação, depoimento, autoridade). Ao ler o batch da 08, confira conceito a conceito: se dois conceitos são a mesma embalagem da mesma razão de compra, eles respondem uma pergunta só — o mais forte entra e o outro volta pro batch seguinte.

#### 3.3 — A estrutura

```
1 CAMPANHA (CBO)  →  N AD SETS (1 = 1 conceito, broad/Advantage+)  →  3 CRIATIVOS + 2 PRIMARY TEXTS + 2 HEADLINES cada
```

**Campanha:**
- **Campaign Name**: `[Produto]_[YYYYMMDD]_Test` (ex: `CollagenSerum_20260620_Test`)
- **Objective / Goal**: **Sales** (o objetivo de Max Conversion / otimização por Purchase; em interfaces antigas aparecia como "Conversions")
- **Special Ad Categories**: nenhum (a menos que saúde/finanças/emprego/habitação — aí marcar)
- **Budget**: **CBO no nível da CAMPANHA** (Advantage+ Campaign Budget **LIGADO**), `daily_budget = test_budget_daily` calculado na ETAPA 3.1. É o CBO que redistribui entre os conceitos — e onde ele concentra gasto é o sinal de escala que a Skill 11 lê. Nenhum ad set de teste carrega budget próprio.
- **Campanha por produto**: **1 conta de anúncio por produto**. NÃO misturar 2 produtos na mesma conta — embaralha o aprendizado do algoritmo. Exceção: produtos muito similares (ex: variações do mesmo item) podem dividir conta.

**Ad sets (um por conceito — `adsets_planejados` da ETAPA 3.1):**
- **Ad Set Name**: `[Produto]_[concept_id]_[YYYYMMDD]` (ex: `CollagenSerum_RootCauseAngle_20260620`) — o `concept_id` no nome preserva o handoff 08→10→11 no nível do ad set, que é onde a leitura por conceito acontece.
- **Conversion event / Optimization**: **Purchase** (Max Conversion) em todos. Se a conta ainda não tem volume de Purchase pra otimizar, NÃO descer pra ViewContent às cegas — isso traz tráfego que não compra; preferir o warmup da ETAPA 4 pra a conta esquentar antes.
- **Budget**: **nenhum no ad set** — o budget vive na campanha (CBO). O único controle de budget no nível do ad set é o **daily maximum** de proteção da ETAPA 6, que é **teto** (proteção contra queima), nunca piso (daily minimum continua proibido — ETAPA 7).
- **Conteúdo**: exatamente **1 conceito por ad set** = o pack 3-2-2 da Skill 08 (3 criativos + 2 primary texts + 2 headlines). Não misturar conceitos dentro de um ad set: misturado, o CBO ainda distribui, mas a leitura de qual conceito funcionou morre.
- **Audience** (idêntica em todos os ad sets — a variável do teste é o conceito, não a audiência):
  - **Location**: mercado principal do market research (US/UK/EU/global).
  - **Age**: **18-65+** (broad — deixar o Meta otimizar).
  - **Gender**: **All** (a menos que o produto seja genuinamente gênero-específico com dado claro).
  - **Detailed targeting**: **Advantage+ / broad** (automático). **NÃO** adicionar interests manuais — o criativo é o targeting. Advantage+ vem batendo manual targeting na grande maioria dos casos. (Pra entender o trade-off Advantage+ broad vs true broad sem training wheels, puxe **True Broad vs Advantage+ Broad** — rode `True Broad vs Advantage Plus broad targeting training wheels`.)
  - **Languages**: idioma do mercado.
  - **Excluded**: nenhum (a menos que retargeting de aquisição precise excluir clientes existentes).
- **Placements**: **Advantage+ Placements** (automático) — Meta distribui entre Feed/Stories/Reels/etc. Não usar manual placements.
- **Schedule**: "Run continuously starting today".
- **Attribution**: 7-day click, 1-day view (padrão 2026). Em EU, restrições de consent podem limitar o view-through — se necessário, ficar só com 7d-click (confirmar com o membro). Não existe janela de 28 dias no Meta desde 2021 — não procure. E **não ligar o setting de Incremental Attribution na campanha de teste**: a régua de kill da Skill 11 foi calibrada no baseline 7d-click/1d-view (ver nota na 11).

**Criativos (3 por ad set — o pack 3-2-2 do conceito):**
- Carregar os **3 criativos do conceito como 3 ads dentro do ad set daquele conceito**, com os 2 primary texts e as 2 headlines do pack. Nunca subir criativo de um conceito no ad set de outro.
- **Diversidade GENUÍNA entre os conceitos (ou seja, entre os ad sets):** no sistema de entrega pós-Andromeda/GEM, criativos muito similares são tratados como praticamente a mesma entidade — 3 ad sets com variações do mesmo visual contam como ~1 conceito pro algoritmo (e pro teste). Diversidade genuína = os conceitos diferem nas **variáveis GRANDES do ad** (persona, conceito/big idea, formato, ângulo — o mapa "As Variáveis de um Ad" da Skill 08), não em detalhes de execução como cor de fundo ou ordem de cena. Dentro de um ad set é o contrário: os 3 criativos são 3 EXECUÇÕES do mesmo conceito, variando só a abertura. O gate de diversidade da Skill 08 já força isso — não dilua na hora de subir.
- O CBO distribui o budget entre os ad sets, e o Meta distribui entre os criativos de cada um. **Onde o gasto se concentra é onde tem escala** — esse é o sinal que a Skill 11 vai ler, agora legível em dois níveis (conceito e criativo).
- **Ad Name** (cada um): `[concept_id]_[creative-n]_[YYYYMMDD]` (ex: `RootCauseAngle_2_20260620`) — o `concept_id` preserva o handoff 08→10→11 e o índice da execução (1..3, na mesma ordem do pack) mantém os 3 ads do conceito distinguíveis no relatório, em paridade com o `utm_content`.
- **CTA Button**: "Shop Now" (PDP direta) ou "Learn More" (advertorial/landing).
- **URL**: o **destino do CONCEITO** — `ad_sets[].landing_url`, lido do mapeamento de congruência da **ETAPA 6 da 08** (a tabela conceito→LP do relatório da 08 + a linha "Destino" de cada briefing: advertorial pra conceito TOF/problem-aware, landing dedicada pra solution-aware, PDP pra product-aware). **Fallback = `manifest.storefront.page_url`** (a página publicada pela 07b — a URL canônica): vale quando a 08 não mapeou destino, quando o batch é legado, ou quando a página do tipo mapeado ainda não existe publicada — nesse último caso registrar o gap de congruência no relatório (a página recomendada se constrói na cadeia 07a/07b), nunca inventar URL. Todo `landing_url` precisa ser página PUBLICADA; os 3 ads de um ad set apontam pro mesmo destino (exceção: eixo de página abaixo).
- **UTM (schema obrigatório — este bloco é a FONTE ÚNICA do framework; a Skill 08 aponta pra cá):**
  ```
  utm_source=facebook
  utm_medium=paid_social
  utm_campaign=[product-slug]_[YYYYMMDD]_test
  utm_content=[concept-id]-[creative-n]   (por CRIATIVO, não por conceito)
  utm_term={{adset.id}}   (dinâmico via macro do Meta — nunca placeholder estático; com 1 ad set por conceito, ele passa a identificar o CONCEITO)
  utm_id={{ad.id}}        (dinâmico via macro do Meta)
  ```
  **Por que `utm_content` é por criativo:** um conceito tem até 3 execuções (pack 3-2-2 da 08) — `utm_content` só por `[concept-id]` fundiria as 3 no analytics e mataria a leitura por criativo em qualquer ferramenta que não expõe o `{{ad.id}}` (GA4, dashboard do ESP, relatório da loja). O sufixo `-[creative-n]` (ex: `rootcause-2`) dá granularidade por criativo legível por humano; o `{{ad.id}}` do `utm_id` segue como identificador único de máquina (é ele que a 11 usa pra casar com o Ads Manager). **Normalização no upload:** se o link veio da 08 só com `[concept-id]` no `utm_content`, acrescentar o sufixo `-[creative-n]` (1..3, na ordem das execuções do pack) ao subir cada ad — nunca subir 2+ criativos com o mesmo `utm_content`.

> **Por que N ad sets sob UMA campanha com CBO — e não N campanhas, nem tudo num ad set só?** Campanhas separadas competem pelo aprendizado e fragmentam o sinal: uma campanha só, broad, fecha o learning phase mais rápido. Já jogar todos os conceitos dentro de um único ad set faz o oposto do que parece: o Meta ainda distribui, mas a leitura por conceito desaparece e cada criativo recebe uma fração de CPA longe do 1× que o cânone exige. Um ad set por conceito com o budget no CBO resolve os dois lados — a campanha aprende junta, e o gasto que cada conceito puxa é a medida de qual conceito tem escala. A diversificação em campanhas ABO separadas é assunto de **escala** (Skill 12, cânone §5), não de teste.

**Eixo de página (3:2:2:2 — opção condicionada por budget):** existe um quarto eixo de teste além do criativo — a página de destino. O **3-2-2-2 Method** (rode `3-2-2-2 landing page testing link clicks vs landing page views clickbait`) adiciona 2 landing pages ao pack (3 criativos × 2 primary texts × 2 headlines × 2 páginas = 24 combinações) e deixa o Meta achar a melhor congruência ad↔página. **Gate do próprio material: budget ≥ US$ 2k/dia.** Abaixo disso a variável extra dilui a leitura de criativo que o teste existe pra comprar — cada ad set roda com **UMA URL só** (a do conceito, acima). Com o gate batido E 2 páginas de fato publicadas pro mesmo conceito:
- o ad set pode carregar as 2 LPs (`ad_sets[].landing_url` + `ad_sets[].landing_url_b`), mantendo o mesmo pack 3-2-2 — a página é a ÚNICA variável extra;
- a leitura da página é **por KPI, nunca por spend** (CPA/conversão por destino) — o mesmo princípio do **Page # Test** (rode `ad set Page # winners duplicados nova landing page julgar por KPI não por spend`), que é a rota certa pra testar LP nova DEPOIS do teste, com winners provados; e o ratio Link Clicks → Landing Page Views segue como detector de clickbait (LP views ≥ ~70% dos link clicks);
- a dupla de páginas sai do mapeamento da 08 ETAPA 6 + do que existe publicado — nunca duplicar a mesma página com URL diferente só pra "ligar o eixo".

**Nota de overflow (batch maior que a capacidade):** se o batch da 08 vier com mais conceitos do que `adsets_planejados` (ETAPA 3.1), NÃO suba tudo — o CBO espalha fino, nenhum conceito recebe ~3× target CPA/dia e o teste não fecha leitura. **Priorize os conceitos com ângulos genuinamente distintos** (ETAPA 3.2) e guarde o resto pro batch seguinte, que entra na fila. Nunca comprima 2 conceitos num ad set pra "caber mais": isso devolve exatamente a estrutura ilegível que a régua de capacidade existe pra evitar. Se o membro quiser mesmo testar tudo, o caminho honesto é budget maior (o que muda a capacidade), não mais ad sets no mesmo budget.

### ETAPA 4 — Warmup de Conta Nova (se aplicável)

Conta de anúncio recém-criada precisa "esquentar" antes da campanha real — o Facebook precisa cobrar o cartão algumas vezes e ver atividade legítima antes de confiar gasto de conversão.

- **3 dias** de uma campanha simples de **engajamento (~$50/dia — ou o budget diário do membro, o que for MENOR)** ANTES da campanha de teste real.
- Objetivo só esquentar a conta — não é teste de criativo.
- **Day 4**: sobe a campanha de teste real (ETAPA 3).

**Quando pular:** se a conta já tem histórico de gasto e Purchases, não precisa de warmup — vai direto pra ETAPA 3. Detectar pelo histórico da conta (ou perguntar ao membro: "essa conta já rodou ads com venda antes?").

> **Nota ética (não grey-hat):** warmup aqui é **higiene legítima de conta nova** — qualquer anunciante sério faz. Esta skill **não** ensina account farming, compra de Business Manager, perfis-laranja, contingência pra driblar ban, nem produtos réplica. Essas táticas derrubam a conta da marca real e brigam com a tese de brand-building do Aura. Ter conta reserva é resiliência legítima; **farmar/driblar ban não é** — e a skill não encoda isso.

### ETAPA 5 — Cadência de Teste e Janela de Decisão

**Não mexer por 3 dias.** Depois de ativar, **deixar 3 dias rodando sem otimizar** (leilão e demanda variam dia a dia; mexer cedo destrói o sinal). Nada de pausar criativo, mudar budget ou trocar audiência nesse período.

> **Por que 3 dias (as variáveis invisíveis):** além da variação de leilão, todo ad é consumido sob condições que ninguém controla nem seta — o prospect vê na carona do carro ou no sofá, com som ou no mudo, depois de um ad bom ou ruim, num dia calmo ou caótico (mapa "As Variáveis de um Ad" da Skill 08). Com poucas impressões, o resultado mede o CONTEXTO dos espectadores, não o criativo. Essas variáveis só se diluem em volume — a janela de 3 dias existe pra isso.

**Cadência de teste de PRODUTO (preview — quem decreta qualquer kill é a Skill 11):**
- **Lançar quarta-feira**, deixar até **domingo** (segunda/terça/quarta são dias mais fracos pra teste novo; quarta→domingo pega os dias fortes).
- **7 dias é o teto por rodada de teste** — a régua de 7 dias do cânone §3 vale por **ad set** (7 dias sem spend e sem KPI = kill do ad set), não como sentença do produto.
- **Domingo é CHECKPOINT de decisão informada, não data de execução.** No checkpoint, rodar a leitura da Skill 11 e decidir com três coisas na mesa: **(1)** as réguas de kill do cânone §3 (conta madura: ad set 7 dias sem spend e sem KPI · conta nova: 8× target CPA sem purchase · ad novo overspendando: 24-48h); **(2)** os checks de precedência da 11 (funil quebrado? conta suspeita? entrega travada?) — matar produto por culpa da página ou da conta é o erro caro que esses checks evitam; **(3)** o **Execution Problem**, a leitura que a 11 aplica (rode `execution problem angle certo palavras erradas 3 strikes por angle 12 razoes de falha`): batch sem venda reprova, na maioria dos casos, a EXECUÇÃO testada — não o ângulo. Um ângulo ganha **3 tentativas (3 strikes)** antes de ser descartado, e execução ruim não mata ângulo — muito menos produto.
- **Matar o PRODUTO é decisão de outro nível:** entra na mesa só depois de **≥ 2 batches com learnings processados** (a 11 extraiu o que cada batch ensinou e o batch seguinte aplicou a correção) OU quando as réguas do cânone §3 mandarem — **nunca por calendário sozinho**. A intenção original do marco de domingo permanece inteira: ele existe pra impedir o membro de queimar caixa por semanas num produto morto. O que muda é o mecanismo — quem declara o óbito é a leitura (11 + cânone), não a data. Sem venda até domingo, o caminho default é processar os learnings e iterar (Sniper nos ângulos que ainda têm strikes), com a 11 dizendo se algum ad set ou ângulo morre já.
- Quem testa volume: ~**3 produtos/semana**.

**Janela de decisão (handoff pra Skill 11):**
- **Dia 1-3**: deixar rodar. Verificar só que os ads saíram do review e que a CAMPANHA está entregando (spend acontecendo). Sob CBO, **ad set sem gasto não é necessariamente erro** — pode ser o CBO escolhendo outro conceito, e isso já é informação. O que exige checar warnings (rejeição de audiência/criativo, ad em review há mais de 24h) é a campanha inteira sem gasto em 24-48h, ou um ad set inteiro travado com os ads ainda "In review". Em nenhum dos casos se otimiza nesse período.
- **A partir do Dia 3**: primeira leitura real. Rodar a Skill 11 (`'ad analysis'`) — é ela que aplica os critérios de kill/scale por conceito (o ad set) e por criativo (o ad), com CPA mandando, não CTR, os benchmarks de funil, e a leitura de CPM como saúde da conta. **Esta skill não decide kill** — ela monta e cria; a 11 lê e decide. A leitura por criativo apoia-se nos SISTEMAS NOMEADOS **4Pi Analysis** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) e **Lucky Wins vs Durable Wins** (rode `lucky wins vs durable wins spend concentration promote to control`) — onde o Facebook concentra gasto é o sinal de escala, mas distinguir win de sorte de win durável evita escalar ruído.

> A escala (cost-cap + surf, bid cap, budget-doubling) é assunto da **Skill 12 (scale)**, acionada só depois de um criativo validar como breakthrough (cânone §2). Não escalar manualmente durante o teste. A régua de subida e descida é o **Scaling Protocol** do cânone `.claude/lib/ad-taxonomy/README.md` §5, que a Skill 12 executa; os SISTEMAS NOMEADOS de leitura que a acompanham — **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`) e **ROAS Target = Break-Even ROAS + 1 / Scaling Protocol** (rode `ROAS target break-even plus one scaling protocol 48 72 hours 20 percent`) — vivem na Skill 12 e no índice `.claude/lib/kb-index/`, não aqui. **Escala por Automated Rule de performance não entra nessa lista**: em campanha com CBO o Meta não aceita condição de performance em rule (ETAPA 6).

### ETAPA 6 — Criação em PAUSED via Meta Ads MCP

Em vez de só entregar "cole isso no Ads Manager", esta skill **cria** a campanha + os ad sets + os ads em **PAUSED** via MCP, pro membro revisar e ativar com 1 clique. Os gates da ETAPA 1 já passaram antes deste ponto.

**Cascade de MCP** (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md` e regra 10 do CLAUDE.md):

1. **Caminho 1 — MCP oficial da Meta (`mcp__meta__ads_*`):** criar a campanha (objective Sales, **CBO ligado com `daily_budget = test_budget_daily`** da ETAPA 3.1) e **um ad set por conceito** (`adsets_planejados`: audience broad/Advantage+, placements automáticos, **sem budget próprio**, com `daily_maximum` de spending limit, optimization Purchase, attribution 7d/1d) em `status: PAUSED`. O oficial é remoto e lida bem com criação de estrutura por parâmetros. (Status: o connector oficial segue em **open beta desde 2026-04-29**, com rollout gradual e sem GA — contas podem aparecer "disabled" mesmo com setup correto; é exatamente o buraco que o Caminho 2 cobre.)
2. **Caminho 2 — Pipeboard (`mcp__meta-ads__*`):** fallback automático quando o oficial está indisponível/"disabled" no rollout. **O upload do binário dos criativos (.mp4) força Pipeboard ou Playwright** mesmo quando o oficial está conectado (o oficial é remote-hosted e não lê arquivo local) — ver receita `.claude/automations/recipes/upload-creative-to-meta.md`.
3. **Caminho 3 — manual:** se nenhum MCP está conectado, entregar o passo-a-passo exato pra o membro montar no Ads Manager (a estrutura das ETAPAS 3-5, formatada pra colar campo a campo).

#### Proteções — o que É automatizável em CBO (cânone §6)

**Performance Gate Scaling (PGS) não existe nesta estrutura.** Automated Rule com condição de performance (CPA, ROAS, frequency) é **recusada pelo Meta** em campanha que usa CBO — o erro retornado é literalmente *"performance-related conditions are not available for assets that use CBO"*. Não ofereça, não tente criar, não prometa ao membro. O que entra no lugar:

1. **`Ad set spending limit → daily maximum` em cada ad set de teste (o substituto do PGS).** É teto de gasto diário no nível do ad set, não é condição de performance, então funciona em CBO. Valor: o mesmo **~3× target CPA/dia** que é o teto por ad set do cânone §1 — é o que o conceito precisa pra ser lido, e nada além disso precisa ser gasto enquanto ele não provou. Serve pra que "subir batch de madrugada" não vire conta de milhares no dia seguinte, e pra que um ad ruim que o CBO resolveu empurrar não coma o teste inteiro. Depois que o conceito prova tração, afrouxar/remover o teto é decisão do membro na Skill 12 — dentro do teste, ele fica.
2. **Automação obrigatória A — pico de gasto:** se o spend subir **5× em 24h**, pausar os ads/ad sets que subiram. Protege contra conta comprometida e contra um zero a mais digitado no budget.
3. **Automação obrigatória B — URL errada:** se a URL de destino do ad **≠ o domínio da loja** (`manifest.storefront.page_url`), desligar o ad. Protege contra ad rodando pra página errada, removida ou de terceiro.

> **Kill automatizado por performance NÃO se faz — nem aqui, nem na 11, nem na 12.** Duas razões independentes: (a) tecnicamente o Meta não aceita a condição em CBO; (b) mesmo onde aceitasse, a métrica do Ads Manager engana — um ad a 1× ROAS na plataforma pode estar excelente no 1-day click de uma ferramenta de atribuição de terceiro, e desligar por metadado mata winner. **Kill é leitura, não regra:** quem decide é a Skill 11, com as réguas do cânone §3.

As duas automações obrigatórias e o daily maximum são oferecidos junto da estrutura e **nascem DESATIVADOS** (as rules) / são criados junto do ad set (o daily maximum). Gravar em `protections` no dados.json o que foi efetivamente criado. Se nenhum caminho MCP suportar a criação das rules, entregar o passo-a-passo pro membro criar em Ads Manager > Automated Rules e marcar `created: false` — a proteção não é opcional por doutrina, só por limite de ferramenta.

**Regras invioláveis da criação:**
- **Tudo nasce em `status: PAUSED`** (inclusive Automated Rules — nascem desativadas). O membro revisa e ativa. A skill NUNCA ativa nada sozinha.
- Os **gates da ETAPA 1** (compliance + promise↔config + disclosure "AI Info") rodam ANTES de criar — não há criação sem gate verde (ou override explícito do membro).
- Reutilizar as receitas existentes onde aplicável: `upload-creative-to-meta.md` (subir os criativos + criar o creative object) e o setup de MCP em `.claude/automations/setup-mcps.md`.
- Após criar, **guardar os IDs retornados** (campaign_id, **ad_set_ids por conceito**, ad_ids) no JSON e no manifest — a Skill 11 lê esses IDs pra puxar insights nos dois níveis (conceito e criativo).
- **Toda criação vira linha no ad-log, na MESMA execução** (cânone `.claude/lib/ad-log/README.md`): campanha, cada ad set, cada ad e cada automação de proteção — **mesmo nascendo em PAUSED/desativada** — são registrados em `workspace/[produto]/ad-log.md`, uma linha por criação no formato do cânone (`| YYYY-MM-DD HH:MM | entidade | criado em PAUSED | skill-10 | motivo curto |`, entidades `campaign:[nome]` · `adset:[concept_id]` · `ad:[creative_id]` · `automation:[nome]`; se o arquivo não existir, criar com o cabeçalho da tabela; append-only). Mudança executada e não logada é bug de processo — é este log que a 11 cruza com a janela de leitura e a 12 consulta antes de escalar. No Caminho 3 (manual), logar quando o membro confirmar o que criou, com executor `membro`.

**Mensagem ao membro após criar em PAUSED:**
> "Criei a campanha `[nome]` em **PAUSED** na sua conta — budget de **$[test_budget_daily]/dia no nível da campanha** (CBO), dividido entre **[N] ad sets, um por conceito** ([lista dos conceitos]), cada um com 3 criativos broad/Advantage+, otimizando pra Purchase. [Se os destinos por conceito diferem:] Cada conceito aponta pra página do nível de consciência dele — [lista conceito→página]. Esse é o número de conceitos que o seu budget consegue LER: $[budget]/dia ÷ CPA alvo de $[target_cpa] dá [max_assets] criativos com chance justa. Revisa no Ads Manager (audiência, budget, criativos, URLs de destino) e **ativa quando estiver OK**. Não ativei nada por você. [Se as proteções foram criadas:] Deixei também o teto de gasto diário por ad set e as duas regras de proteção (pico de gasto e URL errada) — desativadas, ative junto. [Se houver concepts com `ai_disclosure_required: true`:] Os ads [lista] têm humano gerado por AI — confirma que o label 'AI Info' está marcado neles antes de ativar (GATE 3)."

Se a criação via MCP falhar (rate limit, auth), aplicar `.claude/rules/emergency-escape-paths.md` ES6: backoff, depois oferecer **(A)** retomar em 1h, ou **(B)** cair pro Caminho 3 manual com a estrutura formatada.

### ETAPA 7 — Erros Comuns a Evitar

1. **NÃO subir mais conceitos do que a capacidade comporta** — `max_adsets = floor(budget ÷ (3 × target CPA))` e teto de 5 ad sets abaixo de US$ 1k/dia (cânone §1). Ad set que recebe menos que ~3× target CPA/dia devolve ruído, e ruído lido vira decisão errada.
2. **NÃO misturar conceitos dentro de um ad set** — 1 ad set = 1 conceito = 1 pack 3-2-2. Misturado, o gasto ainda acontece, mas a pergunta "qual conceito funcionou" fica sem resposta.
3. **NÃO usar detailed targeting / interests** — o criativo faz o targeting. Adicionar interest só encolhe o pool e limita o algoritmo.
4. **NÃO mexer antes de 3 dias** — cada mudança (budget, audiência, pausar criativo) reseta o sinal. Deixar rodar.
5. **NÃO usar daily MINIMUM** ("garantir $X de spend" por ad set) — força o Meta a gastar em impressão ruim pra bater meta. **Atenção pra não confundir:** o daily **maximum** da ETAPA 6 é obrigatório (é teto de proteção); o daily **minimum** continua proibido (é piso forçado). São coisas opostas.
6. **NÃO criar Automated Rule de performance** (kill ou escala por CPA/ROAS/frequency) — o Meta recusa em CBO, e mesmo onde aceitasse, decidir por metadado do Ads Manager mata winner (cânone §6). As únicas automações são as três da ETAPA 6.
7. **NÃO misturar 2 produtos numa conta** — embaralha o aprendizado. 1 conta por produto.
8. **NÃO inflar o budget "pra acelerar"** — acima do teto por ad set o dinheiro extra não compra leitura, só queima caixa. Budget maior serve pra rodar MAIS conceitos (mais ad sets), não pra empurrar os mesmos.
9. **NÃO escalar manualmente durante o teste** — escala é depois do breakthrough (Skill 12, cânone §5).
10. **NÃO ler CTR como verdade** — CPA é o que manda; isso a Skill 11 detalha. Aqui só não tome decisão de kill na base de CTR.
11. **NÃO re-decidir na 10 o método que a 08 já gravou** — `concepts[].testing_method` manda: o pack foi CONSTRUÍDO naquele método (3 ângulos ou 3 execuções), e reclassificar aqui só desalinha a leitura da 11. A regra própria da 3.2 é fallback pra batch legado sem o campo.
12. **NÃO matar produto por calendário** — domingo é checkpoint de leitura (ETAPA 5): réguas do cânone §3 + checks de precedência da 11 + Execution Problem (falhou o ângulo ou a execução?), e kill de PRODUTO só com ≥ 2 batches de learnings processados ou régua do cânone mandando. Data sozinha não decide nada.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/10-ad-strategy/` antes de salvar.

`workspace/[produto]/10-ad-strategy/ad-strategy.md` (no `report_language`) contendo:
1. Estrutura de teste completa: 1 campanha com CBO → N ad sets (1 por conceito) → 3 criativos + 2 primary texts + 2 headlines cada (ETAPA 3.3)
2. A conta de capacidade explicada com os números REAIS deste produto (ETAPA 3.1): target CPA, budget diário, `max_assets`, `max_adsets`, quantos conceitos entraram, quantos ficaram pro batch seguinte, e o `test_budget_daily` resultante. Se alguma restrição mordeu (piso de budget, teto de 5 ad sets, tamanho do batch, `margin_warning`), dizer qual e o efeito prático. Se o CPA-alvo ficou **abaixo do piso físico de CAC** (item 1b), mostrar as duas capacidades lado a lado — a do alvo e a do piso — e dizer que a correção é de AOV, na 04
3. Método de teste POR AD SET — lido de `concepts[].testing_method` da 08 (ou o fallback da 3.2 pra batch legado, com `data_gap`) — com o resumo do batch e o que cada pack varia por dentro (ETAPA 3.2)
4. Warmup de conta (se aplicável), cadência quarta→domingo e o **checkpoint de decisão de domingo** — réguas do cânone §3, checks de precedência, Execution Problem, e a régua de ≥ 2 batches com learnings antes de qualquer kill de produto (ETAPAS 4-5)
5. Naming convention aplicada (Campaign / Ad Set / Ad)
6. UTM schema preenchido
7. Destino por ad set (mapeamento de congruência da 08 ETAPA 6, fallback = URL canônica do manifest), gaps de congruência se houver, e o eixo de página 3:2:2:2 quando o gate de US$ 2k/dia liberou (ETAPA 3.3)
8. Janela de decisão e handoff pra Skill 11 (ETAPA 5)
9. Checklist de credibilidade da loja com os gaps encontrados (ETAPA 2)
10. Status da criação via MCP (criado em PAUSED / fallback manual) + IDs retornados + criações registradas no `ad-log.md`
11. Proteções configuradas: daily maximum por ad set + as duas automações obrigatórias, com o status de cada uma (ETAPA 6)
12. Checklist de erros a evitar (ETAPA 7)

**Dual output:** gerar `10-ad-strategy/ad-strategy.html` companion (mesmo diretório) usando `.claude/templates/aura-report-template.html` como base — CSS inline, self-contained, **logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` (NUNCA texto)**, componentes aura (callout, note, danger, winner, kpi-grid, table-wrap). O `.md` é fonte pra AI; o `.html` é visualização humana.

### JSON companion — `10-ad-strategy/dados.json`

```json
{
  "strategy_id": "uuid",
  "product_slug": "...",
  "creative_batch_ref": "08-creative-engine/dados.json batch_id (concepts[].id é o handoff 08→10→11)",
  "target_cpa": 40,
  "breakeven_cpa": 80,
  "member_daily_budget": 240,
  "test_capacity": {
    "max_assets": 6,
    "max_adsets": 2,
    "adsets_planned": 2,
    "assets_planned": 6,
    "concepts_available": 4,
    "concepts_deferred": 2,
    "binding_constraint": "max_adsets|floor|adset_cap_5|batch_size|margin_warning|none",
    "floor_applied": false,
    "below_floor_directional_only": false
  },
  "cac_floor_check": {
    "source": "15-finance-engine|none",
    "cac_floor_reference_usd": null,
    "cac_max_first_order": null,
    "target_reachable_vs_floor": "yes|no|unknown",
    "binding": false,
    "max_assets_at_floor": null
  },
  "test_budget_daily": 240,
  "test_method": "marksman|sniper|mixed",
  "structure": "1_campaign_cbo_1_adset_per_concept",
  "campaign": {
    "name": "...",
    "objective": "Sales",
    "optimization": "purchase_max_conversion",
    "budget_level": "campaign_cbo",
    "daily_budget": 240,
    "attribution": "7d_click_1d_view",
    "placements": "advantage_plus",
    "targeting": "advantage_plus_broad",
    "one_account_per_product": true
  },
  "ad_sets": [
    {
      "name": "...",
      "concept_id": "...",
      "angle": "a razão de compra em uma frase",
      "testing_method": "marksman|sniper",
      "landing_url": "https://...",
      "landing_url_source": "08_etapa6|manifest_fallback",
      "landing_url_b": null,
      "creative_count": 3,
      "primary_texts": 2,
      "headlines": 2,
      "daily_max_spending_limit": 120,
      "ad_set_id": "",
      "ad_ids": []
    }
  ],
  "page_axis": { "enabled_322_2": false, "budget_gate_daily_usd": 2000 },
  "account_warmup": { "required": false, "days": 3, "engagement_budget_daily": 50 },
  "cadence": { "launch_day": "wednesday", "decision_checkpoint": "sunday", "max_days": 7 },
  "protections": {
    "adset_daily_maximum": { "enabled": true, "value_per_adset": 120, "basis": "3x_target_cpa" },
    "spend_spike_rule": { "created": false, "active": false, "condition": "spend_5x_24h", "action": "pause" },
    "url_mismatch_rule": { "created": false, "active": false, "condition": "destination_url_not_store_domain", "action": "pause_ad" },
    "automated_performance_kill": false,
    "automated_performance_scaling": false
  },
  "pgs_enabled": false,
  "store_credibility": { "instagram": "ok", "reviews_count": 0, "comment_management": "flagged", "gaps": [] },
  "mcp_creation": { "path": "official|pipeboard|manual", "status": "created_paused|fallback_manual", "campaign_id": "", "ad_set_ids": [], "ad_ids": [] },
  "utm_schema": {}
}
```

> **Todos os números do exemplo são ilustrativos** — grave sempre os números reais deste produto, calculados na ordem da ETAPA 3.1. `target_cpa` é o divisor da capacidade (`unit_economics.target_cpa_primary_2x` ou `manifest.target_cpa`); `breakeven_cpa` (`weighted_margin_per_order`) continua gravado porque a Skill 11 e a 12 leem por ele.
>
> **`test_capacity`:** a conta inteira, auditável. `binding_constraint` diz QUAL restrição limitou o teste (a que apertou primeiro) — é o campo que a Skill 11 lê pra saber se a leitura nasceu apertada. `below_floor_directional_only: true` marca o caminho (b) da ETAPA 3.1 (budget abaixo do piso de US$ 100/dia): nesse estado o resultado é direcional e **não autoriza kill nem escala** — a 11 precisa dizer isso ao membro em vez de classificar.
>
> **`cac_floor_check`** é o registro da checagem do item 1b da ETAPA 3.1 e existe **só quando `15-finance-engine/dados.json` está presente** — sem ele, `source: "none"`, `target_reachable_vs_floor: "unknown"` e a capacidade é calculada pelo target como sempre foi. Os três primeiros campos são **cópias** do bloco `cac` da 15; esta skill não recalcula piso nem CAC máximo. `max_assets_at_floor` guarda a capacidade recalculada com o piso no lugar do target (a conta conservadora que o membro vê ao lado da otimista quando o veredito é `no`). **Cuidado com o vocabulário:** o `floor` de `binding_constraint`/`floor_applied` é o **piso de BUDGET** (US$ 100-150/dia); o piso deste bloco é o **piso de CAC** do leilão. São coisas diferentes e não se misturam.
>
> **`ad_sets[]` é uma LISTA** (antes era o objeto único `ad_set`): 1 entrada por conceito, com o `ad_set_id` retornado pelo MCP dentro da própria entrada. `daily_max_spending_limit` é o teto de proteção da ETAPA 6 (~3× `target_cpa`), não um budget de ad set — o budget vive em `campaign.daily_budget` com `budget_level: "campaign_cbo"`.
>
> **`ad_sets[].testing_method` é o campo operativo de método** (contrato 08→10, ETAPA 3.2): copiado de `concepts[].testing_method` da 08; em batch legado sem o campo, inferido pela regra prática da 3.2 com `data_gap` marcado. O `test_method` batch-level é só RESUMO — o método único quando todos os ad sets coincidem, `mixed` quando variam. A Skill 11 lê o por-ad-set pra saber que pergunta cada pack responde ("qual ângulo venceu?" em Marksman, "qual execução venceu?" em Sniper).
>
> **`ad_sets[].landing_url` (+ `landing_url_source`, `landing_url_b`):** o destino do conceito (ETAPA 3.3) — `08_etapa6` quando veio do mapeamento de congruência da 08, `manifest_fallback` quando caiu na URL canônica `manifest.storefront.page_url`. `landing_url_b` fica `null` a menos que o eixo de página esteja ativo (`page_axis.enabled_322_2: true`, que exige budget ≥ US$ 2k/dia E 2 páginas publicadas pro conceito) — aí carrega a segunda LP do ad set, lida por KPI da página, nunca por spend.
>
> **`cadence.decision_checkpoint`** substitui o antigo `kill_by`: domingo é checkpoint de leitura (ETAPA 5), não data de execução. Kill de ad set é régua do cânone §3, decretada pela Skill 11; kill de PRODUTO exige ≥ 2 batches com learnings processados OU régua do cânone — nunca calendário sozinho.
>
> **`protections`:** substitui os antigos campos `pgs_*`. `automated_performance_kill`/`automated_performance_scaling` ficam `false` SEMPRE — não são configuráveis, são o registro explícito de que essa automação não existe nesta estrutura (cânone §6). **`pgs_enabled` permanece no schema apenas como campo de compatibilidade, fixo em `false`**, porque a receita `full-deploy.md` e a Skill 11 ainda o leem pra decidir se prometem escala automática; com `false`, as duas degradam pro comportamento certo (não prometem). Nunca gravar `true`.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `10-ad-strategy` em `skills_completed`
- Registrar `strategy_id`, `creative_batch_ref`, `test_budget_daily`, `target_cpa`, `breakeven_cpa`
- **Gravar `10_campaign_name`** com o nome da campanha gerado (naming convention). A Skill 11 lê via `read_manifest("10_campaign_name")` pra cruzar com dados do Meta.
- Se criou via MCP, gravar `10_campaign_id` e **`10_ad_set_ids`** (lista — um ID por conceito; a Skill 11 puxa insights por ID, mais robusto que por nome). Gravar também `10_ad_set_id` com o ID do PRIMEIRO ad set, só por compatibilidade com as receitas que ainda esperam o campo único.
- Registrar `pgs_enabled: false` (fixo — Automated Rule de performance não existe em CBO, ETAPA 6). A Skill 11 lê esse campo antes de falar em "escala automática"; com `false`, ela não promete.
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza ABRIR-AQUI.html).

## Mensagem Final

Apresentar como **draft pronto pra revisão** (`.claude/rules/iteration-driven-refinement.md`), não como "pronto, pode escalar":

"Estrutura de teste montada: campanha `[nome]` com o budget de **$[test_budget_daily]/dia no nível da campanha**, dividido entre **[N] ad sets broad/Advantage+ — um por conceito** ([lista]), cada um com 3 criativos, 2 textos e 2 headlines, otimizando pra Purchase[, e cada conceito apontando pra página do nível de consciência dele, se os destinos diferem] ([se MCP] já criada em **PAUSED** na sua conta — revisa e ativa).

Por que [N] conceitos e não mais: com CPA alvo de **$[target_cpa]** e **$[budget]/dia**, esse budget consegue LER [max_assets] criativos ([N] conceitos). Cada criativo precisa de mais ou menos 1 CPA por dia pra acumular dado suficiente — abaixo disso o número que aparece no painel é ruído, e decisão em cima de ruído custa caro. [Se sobrou conceito: Os outros [X] conceitos ficam pro próximo batch.] [Se alguma restrição mordeu: explicar qual em uma frase.]

Plano de teste: [se conta nova: 3 dias de warmup de engajamento primeiro, depois] lançar **quarta**, deixar até **domingo**, **3 dias sem mexer**. Domingo é o nosso **checkpoint de decisão**: eu rodo a leitura da 11 e a gente decide com dado na mesa — ad set que passou 7 dias sem gasto e sem resultado morre pela régua; ângulo que ainda tem tentativa sobrando itera no batch seguinte (antes de descartar qualquer ângulo, eu confiro se a falha foi dele ou da execução — o mesmo ângulo tem direito a 3 tentativas). Matar o PRODUTO só entra na conversa depois de pelo menos 2 batches com os aprendizados aplicados, ou antes disso se as réguas mandarem — nunca só porque o calendário virou. O checkpoint continua servindo pro mesmo propósito de sempre: impedir que você queime caixa em produto morto. Quem declara o óbito passa a ser a leitura, e ela é honesta nos dois sentidos.

Quando ativar e passarem **3 dias**, diga **'ad analysis'** e me manda os dados (ou eu puxo via MCP) — aí a 11 lê CPA por conceito e por criativo, CPM da conta e os benchmarks de funil pra decidir o que mantém, o que mata e o que está pronto pra escalar. Kill e escala são leitura dela: eu não deixo nenhuma regra automática decidindo isso por você.

Antes de ativar: confere a credibilidade da loja (reviews, comentários dos posts) — [resumo dos gaps da ETAPA 2, se houver]. Quer que eu ajuste algo na estrutura — budget, número de criativos, mercado?"
