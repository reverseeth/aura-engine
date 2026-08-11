---
name: ad-strategy
description: Engine de configuração e CRIAÇÃO da estrutura de teste no Meta Ads Manager — estrutura enxuta 1 campanha → 1 ad set (Advantage+ / broad, Max Conversion) → 5-12 criativos, budget = 2× o CPA de breakeven/dia, 3 dias rodando sem mexer, 1 conta por produto, warmup de conta nova, cadência de teste quarta→domingo. Cria campanha/ad set/criativos em PAUSED via Meta Ads MCP (membro revisa e ativa), com gates pre-launch e leitura de credibilidade da loja antes do go-live. Use quando o membro disser "ad strategy", "estratégia de ads", "montar campanha", "setup Meta Ads", "configurar campanha", ou após os briefings de criativos estarem prontos.
---

# Ad Strategy Engine

## Quando Usar
Quando o membro tem criativos prontos (da Skill 08) + página pronta na loja (cadeia 07a/07b) + tracking validado (07c) + oferta ativa (Skill 04), e precisa configurar **e criar** a estrutura de teste no Meta Ads Manager. Essa skill não é "estratégia conceitual" — é a **camada de execução**: monta a campanha exata e a cria em PAUSED via MCP pro membro revisar e ativar.

A teoria de diagnóstico (PSM, 4Pi, ROAS targets) continua viva como **leitura** — a Skill 11 (ad-analysis) lê por ali. O que esta skill entrega é o "exatamente o que fazer no Ads Manager" pra validar criativo.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` + `README.md`, com o mapa skill→domínio). Sempre que esta skill mandar "consultar a base", puxe os **SISTEMAS NOMEADOS** abaixo — rode `search_knowledge` com a `best_query` exata de cada framework relevante pra ETAPA. **NUNCA use query genérica** ("ads strategy", "como configurar campanha"). Os domínios desta skill são `meta-ads-strategy` (estrutura/budget/escala) e `persuasion-psychology` (credibilidade/gestão de comentários).

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)
- [ ] `workspace/[produto]/08-creative-engine/dados.json` existe (5-12 criativos prontos — eles vão TODOS pro mesmo ad set; o handoff é `concepts[].id`/criativo)
- [ ] `workspace/[produto]/04-offer-builder/dados.json` existe (`target_cpa` / `breakeven_cpa`, `breakeven_roas`, `weighted_margin_per_order` — base do budget de teste). **Se `manifest.target_cpa`/`manifest.breakeven_roas` existirem, eles PREVALECEM sobre os valores do 04**: a 04 os grava no manifest, e a 07d os ATUALIZA quando o escopo real das alavancas de checkout mudou a economics (`07d-checkout-aov/dados.json.aov_reconciliation.scope_diff` não-vazio + aplicado na loja) — o manifest carrega o recálculo mais recente; o dados.json do 04 é a projeção original
- [ ] `workspace/[produto]/profile.md` existe (budget diário, stage, conta do Meta Ads ativa)
- [ ] **`manifest.margin_warning` lido**: se `true` (a Skill 04 flagou margem ponderada < $20/pedido), capar o budget inicial de teste no piso da faixa (nunca acima de 2× breakeven CPA, preferir mais perto de 1×) e AVISAR o membro que a margem apertada reduz o espaço de erro do CPA — subir budget só depois de revisar a margem na 04
- [ ] **`report_language`** lido (default `pt-BR`) — ver "Contexto a carregar"
- [ ] Tracking validado via Skill 07c: `manifest.tracking.tracking_ready == true` (Pixel + CAPI, EMQ ≥ 6.0 na escala 0-10 do Events Manager). **`emq_pending: true` é aceito** (loja pré-launch sem tráfego: o EMQ só calcula com eventos reais — a 07c validou instalação + Purchase por pedido-teste): prosseguir, avisando o membro que **a Skill 11 re-lê o EMQ no dia 3 de tráfego** e EMQ < 6.0 pós-tráfego = ação corretiva na 07c antes de qualquer decisão de kill/escala. Se `tracking_ready != true`, redirecionar pra `'tracking'` antes — sem evento de Purchase confiável, Max Conversion não otimiza.
- [ ] `manifest.storefront.page_url` preenchido (a página publicada pela 07b — é a URL de destino da campanha). Se vazio, redirecionar pra `'build page'` (07b) antes.

Se algum arquivo crítico sumiu/corrompeu, aplicar `.claude/rules/emergency-escape-paths.md` (ES1/ES2): oferecer **(A)** re-rodar a skill que gera o arquivo, ou **(B)** proceder com default e marcar `manifest.skipped_preflight`. Nunca abortar sem ≥ 2 caminhos.

### Contexto a carregar

1. Leia `workspace/profile.md`. **Leia `report_language`** (default `pt-BR` se ausente; também em `manifest.report_language`): TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final (ads, headlines, páginas, emails, hooks) e VOC literal permanecem SEMPRE em inglês US**, independente do `report_language`.
2. Leia `workspace/[produto]/04-offer-builder/offer-builder.md` (se não existir, leia o legado `relatorio.md`) + `04-offer-builder/dados.json` — daqui sai o **breakeven CPA**, o número que governa o budget de teste e os critérios de kill da Skill 11. **Ordem de precedência de `target_cpa`/`breakeven_roas`:** primeiro `manifest.target_cpa`/`manifest.breakeven_roas` (se presentes — a 04 grava, e a 07d atualiza quando o escopo de alavancas de checkout aplicado mudou a economics); só na ausência deles, os valores de `04-offer-builder/dados.json`. **Fonte canônica do breakeven CPA (a MESMA que a Skill 11 e a 12 usam):** `breakeven_cpa = 04-offer-builder/dados.json.unit_economics.weighted_margin_per_order`. Use esse campo direto — não re-derive. Só se ele faltar, caia pro fallback `breakeven_cpa = AOV / breakeven_roas`.
3. Leia a **URL de destino** de `manifest.storefront.page_url` (gravada pela 07b no deploy — a PDP/landing publicada). Essa é a fonte canônica da URL da campanha; NUNCA tirar a URL do relatório da 06 (copy não é deploy — a página pode ter mudado de handle na publicação).
4. Leia `workspace/[produto]/08-creative-engine/dados.json` (os 5-12 criativos que entram no único ad set de teste).
5. Detecte o **stage** do membro (`.claude/rules/member-stage-awareness.md`): starter / validating / scaling. Define tom, agressividade e número de criativos recomendado.
6. Puxe os **SISTEMAS NOMEADOS** da base como camada de LEITURA/diagnóstico (não de execução de estrutura) — rode `search_knowledge` com a `best_query` de cada um, nunca query genérica. O que sustenta esta skill como leitura:
   - **Scientific Method for Meta Ads (Control vs Variable)** (rode `scientific method meta ads control variable environmental impact`) — por que 1 ad set único é a estrutura limpa de teste.
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

### ETAPA 3 — Estrutura de Teste (o playbook)

A estrutura de teste do Aura é **enxuta de propósito**. O aprendizado acontece no **ad set**, não na campanha: um único ad set otimiza muito mais rápido que vários competindo por budget. E o **criativo faz o targeting** — por isso a audiência é broad/Advantage+, sem detailed targeting.

**Ancorar a estrutura nos SISTEMAS NOMEADOS (rode a `best_query` de cada um — nunca query genérica):**
- **One Campaign Method (AndroMeta One Architecture)** (rode `One Campaign Method AndroMeta One CBO control variable ad set structure`) — a arquitetura 1 campanha → 1 ad set que esta etapa monta.
- **Andromeda System (5 Core Principles)** + **Before vs After Andromeda Mental Model Shift** (rode `Andromeda 5 principles one campaign method scaling Meta Ads` e `Andromeda before after mental model creative defines targeting`) — o princípio "o criativo define o targeting", base da audiência broad.
- **Why Bad Ads Get Spend (CBO vs ABO)** (rode `why bad ads get spend CBO vs ABO force spend organic algorithm cost caps`) — por que budget no ad set (não CBO) é a escolha certa pra teste.
- **Minimum Daily Spend & Spend Redistribution** (rode `minimum daily spend spend redistribution do not turn off top spender`) — base do budget = 2× breakeven CPA (dar fôlego pro algoritmo distribuir).

```
1 CAMPANHA  →  1 AD SET (Advantage+ / broad)  →  5-12 CRIATIVOS
```

**Campanha:**
- **Campaign Name**: `[Produto]_[YYYYMMDD]_Test` (ex: `CollagenSerum_20260620_Test`)
- **Objective / Goal**: **Sales** (o objetivo de Max Conversion / otimização por Purchase; em interfaces antigas aparecia como "Conversions")
- **Special Ad Categories**: nenhum (a menos que saúde/finanças/emprego/habitação — aí marcar)
- **Budget**: deixar no **nível do ad set** (Advantage+ Campaign Budget OFF nesta estrutura de teste — budget único de ad set é o que queremos)
- **Campanha por produto**: **1 conta de anúncio por produto**. NÃO misturar 2 produtos na mesma conta — embaralha o aprendizado do algoritmo. Exceção: produtos muito similares (ex: variações do mesmo item) podem dividir conta.

**Ad set (o único):**
- **Ad Set Name**: `[Produto]_MainTest_[YYYYMMDD]` (ex: `CollagenSerum_MainTest_20260620`)
- **Conversion event / Optimization**: **Purchase** (Max Conversion). Se a conta ainda não tem volume de Purchase pra otimizar, NÃO descer pra ViewContent às cegas — isso traz tráfego que não compra; preferir o warmup da ETAPA 4 pra a conta esquentar antes.
- **Budget de teste = 2× o CPA de breakeven/dia.** Ex: breakeven CPA $80 → começar **$160/dia**. Esse é o número que dá ao Facebook fôlego pra distribuir entre os criativos e achar onde gasta com retorno. (Budget muito abaixo de 2× breakeven CPA = cada criativo recebe migalha, learning nunca fecha, decisão impossível.)
- **Se 2× breakeven estoura o budget do membro** (starter com budget diário menor que o número): não finja que dá. Dois caminhos honestos, apresentar os dois: **(a)** adiar o teste até ter caixa pro número certo (leitura limpa, sem desperdício), ou **(b)** mínimo viável = **1× breakeven CPA/dia com 3-4 criativos** — o teste demora mais e a leitura sai mais ruidosa (avisar isso explicitamente ao membro). Abaixo de 1× breakeven/dia, **não rodar**: é queimar caixa sem conseguir decidir nada.
- **Audience**:
  - **Location**: mercado principal do market research (US/UK/EU/global).
  - **Age**: **18-65+** (broad — deixar o Meta otimizar).
  - **Gender**: **All** (a menos que o produto seja genuinamente gênero-específico com dado claro).
  - **Detailed targeting**: **Advantage+ / broad** (automático). **NÃO** adicionar interests manuais — o criativo é o targeting. Advantage+ vem batendo manual targeting na grande maioria dos casos. (Pra entender o trade-off Advantage+ broad vs true broad sem training wheels, puxe **True Broad vs Advantage+ Broad** — rode `True Broad vs Advantage Plus broad targeting training wheels`.)
  - **Languages**: idioma do mercado.
  - **Excluded**: nenhum (a menos que retargeting de aquisição precise excluir clientes existentes).
- **Placements**: **Advantage+ Placements** (automático) — Meta distribui entre Feed/Stories/Reels/etc. Não usar manual placements.
- **Schedule**: "Run continuously starting today".
- **Attribution**: 7-day click, 1-day view (padrão 2026). Em EU, restrições de consent podem limitar o view-through — se necessário, ficar só com 7d-click (confirmar com o membro). Não existe janela de 28 dias no Meta desde 2021 — não procure. E **não ligar o setting de Incremental Attribution na campanha de teste**: a régua de kill da Skill 11 foi calibrada no baseline 7d-click/1d-view (ver nota na 11).

**Criativos (5-12 no mesmo ad set):**
- Carregar **todos os criativos da Skill 08 como ads separados dentro deste único ad set**. Sweet spot **~5-8**; teto **12**. Abaixo de 5, pouco material pro Facebook escolher; acima de 12, dilui demais o budget de teste.
- **Diversidade GENUÍNA entre os criativos:** no sistema de entrega pós-Andromeda/GEM, criativos muito similares são tratados como praticamente a mesma entidade — subir 8 variações do mesmo visual conta como ~1 criativo pro algoritmo (e pro teste). Diversidade genuína = os conceitos diferem nas **variáveis GRANDES do ad** (persona, conceito/big idea, formato, ângulo — o mapa "As Variáveis de um Ad" da Skill 08), não em detalhes de execução como cor de fundo ou ordem de cena. O gate de diversidade da Skill 08 já força isso — não dilua na hora de subir.
- O Facebook distribui o budget entre os criativos. **Onde ele começa a concentrar gasto é onde tem escala** — esse é o sinal que a Skill 11 vai ler.
- **Ad Name** (cada um): `[concept_id]_[YYYYMMDD]` (ex: `RootCauseAngle_20260620`) — preserva o handoff 08→10→11.
- **CTA Button**: "Shop Now" (PDP direta) ou "Learn More" (advertorial/landing).
- **URL**: `manifest.storefront.page_url` (a página publicada pela 07b — fonte canônica).
- **UTM (schema obrigatório — este bloco é a FONTE ÚNICA do framework; a Skill 08 aponta pra cá):**
  ```
  utm_source=facebook
  utm_medium=paid_social
  utm_campaign=[product-slug]_[YYYYMMDD]_test
  utm_content=[concept-id]-[creative-n]   (por CRIATIVO, não por conceito)
  utm_term={{adset.id}}   (dinâmico via macro do Meta — nunca placeholder estático)
  utm_id={{ad.id}}        (dinâmico via macro do Meta)
  ```
  **Por que `utm_content` é por criativo:** um conceito tem até 3 execuções (pack 3-2-2 da 08) — `utm_content` só por `[concept-id]` fundiria as 3 no analytics e mataria a leitura por criativo em qualquer ferramenta que não expõe o `{{ad.id}}` (GA4, dashboard do ESP, relatório da loja). O sufixo `-[creative-n]` (ex: `rootcause-2`) dá granularidade por criativo legível por humano; o `{{ad.id}}` do `utm_id` segue como identificador único de máquina (é ele que a 11 usa pra casar com o Ads Manager). **Normalização no upload:** se o link veio da 08 só com `[concept-id]` no `utm_content`, acrescentar o sufixo `-[creative-n]` (1..3, na ordem das execuções do pack) ao subir cada ad — nunca subir 2+ criativos com o mesmo `utm_content`.

> **Por que 1 ad set e não vários?** Cada ad set que você adiciona compete pelo aprendizado e fragmenta o sinal. Um ad set único, broad, com vários criativos, fecha o learning phase mais rápido e te diz em dias quais criativos têm tração. A diversificação de ad sets/campanhas é assunto de **escala** (Skill 12), não de teste.

Número de criativos por stage (alinhado com a tabela de conceitos da Skill 08 ETAPA 2 — cada conceito = 1 pack 3-2-2 = 3 criativos):
- **starter** (< $50/dia) → 6-9 criativos (2-3 conceitos) — orçamento limitado, não dilui.
- **validating** ($50-500/dia) → 9-12 criativos (3-4 conceitos) — enche o ad set sem estourar o teto.
- **scaling** ($500+/dia) → até 12 criativos por ad set; batches maiores (6-10 conceitos) transbordam pra ad sets adicionais (nota abaixo).

**Nota de overflow (batch > 12 criativos):** se o batch da 08 vier com mais de 12 criativos (ex: 5-6 conceitos × 3 execuções = 15-18), NÃO subir tudo no mesmo ad set — acima de 12 o budget de teste dilui e o learning não fecha. **Dividir em 2+ ad sets**, cada um com 5-12 criativos E budget de teste próprio (o mesmo 2× breakeven por ad set), espelhando a regra da 08 ("N×3 > 12 → distribuir em 2+ ad sets/contas"). Distribuir conceitos genuinamente diversos entre os ad sets (não agrupar variações do mesmo conceito em ad sets diferentes). Se o budget não sustenta 2 ad sets de teste, priorizar os 12 criativos mais diversos e guardar o resto pro batch seguinte — é a única exceção legítima à regra "1 ad set" desta estrutura, e ela existe por diluição, não por "testar mais".

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

**Cadência de teste de PRODUTO (preview — quem decreta o kill é a Skill 11):**
- **Lançar quarta-feira**, deixar até **domingo** (segunda/terça/quarta são dias mais fracos pra teste novo; quarta→domingo pega os dias fortes).
- **7 dias é o teto** por teste de produto.
- Se até domingo nenhum criativo vendeu, o default é **matar o produto** — mas a decisão é da **Skill 11**, que antes roda os checks de precedência (funil quebrado? conta suspeita? entrega travada?). Matar produto por culpa da página ou da conta é o erro caro que esses checks evitam.
- Quem testa volume: ~**3 produtos/semana**.

**Janela de decisão (handoff pra Skill 11):**
- **Dia 1-3**: deixar rodar. Verificar só que os ads saíram do review e estão entregando (spend acontecendo). Ad set sem gasto nenhum em 24-48h → checar warnings (rejeição de audiência/criativo) no Ads Manager, não otimizar.
- **A partir do Dia 3**: primeira leitura real. Rodar a Skill 11 (`'ad analysis'`) — é ela que aplica os critérios de kill/scale por criativo (CPA manda, não CTR), os benchmarks de funil, e a leitura de CPM como saúde da conta. **Esta skill não decide kill** — ela monta e cria; a 11 lê e decide. A leitura por criativo apoia-se nos SISTEMAS NOMEADOS **4Pi Analysis** (rode `4Pi analysis spend frequency CPM cost per result funnel position`) e **Lucky Wins vs Durable Wins** (rode `lucky wins vs durable wins spend concentration promote to control`) — onde o Facebook concentra gasto é o sinal de escala, mas distinguir win de sorte de win durável evita escalar ruído.

> A escala (cost-cap + surf, bid cap, budget-doubling) é assunto da **Skill 12 (scale)**, acionada só depois de um criativo validar. Não escalar manualmente durante o teste. Os SISTEMAS NOMEADOS que governam essa decisão de escala — **Profitable Scaling Margin (PSM)** (rode `Profitable Scaling Margin PSM LTV CPA COGS replaces ROAS`), **ROAS Target = Break-Even ROAS + 1 / Scaling Protocol** (rode `ROAS target break-even plus one scaling protocol 48 72 hours 20 percent`) e **Performance Gate Scaling (PGS)** (rode `Performance Gate Scaling PGS automated rules total loss investment soft surfing`) — vivem na Skill 12 e no índice `.claude/lib/kb-index/`, não aqui.

### ETAPA 6 — Criação em PAUSED via Meta Ads MCP

Em vez de só entregar "cole isso no Ads Manager", esta skill **cria** a campanha + ad set + ads em **PAUSED** via MCP, pro membro revisar e ativar com 1 clique. Os gates da ETAPA 1 já passaram antes deste ponto.

**Cascade de MCP** (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md` e regra 10 do CLAUDE.md):

1. **Caminho 1 — MCP oficial da Meta (`mcp__meta__ads_*`):** criar a campanha (objective Sales) e o ad set (audience broad/Advantage+, placements automáticos, budget = o budget de teste efetivo da ETAPA 3, optimization Purchase, attribution 7d/1d) em `status: PAUSED`. O oficial é remoto e lida bem com criação de estrutura por parâmetros. (Status: o connector oficial segue em **open beta desde 2026-04-29**, com rollout gradual e sem GA — contas podem aparecer "disabled" mesmo com setup correto; é exatamente o buraco que o Caminho 2 cobre.)
2. **Caminho 2 — Pipeboard (`mcp__meta-ads__*`):** fallback automático quando o oficial está indisponível/"disabled" no rollout. **O upload do binário dos criativos (.mp4) força Pipeboard ou Playwright** mesmo quando o oficial está conectado (o oficial é remote-hosted e não lê arquivo local) — ver receita `.claude/automations/recipes/upload-creative-to-meta.md`.
3. **Caminho 3 — manual:** se nenhum MCP está conectado, entregar o passo-a-passo exato pra o membro montar no Ads Manager (a estrutura das ETAPAS 3-5, formatada pra colar campo a campo).

**Passo opcional — Automated Rule de PGS (só com aprovação explícita do membro):** oferecer criar, junto da estrutura, a Automated Rule de Performance Gate Scaling — condições: CPA trailing (Purchase) abaixo de `pgs_cpa_threshold`, spend acima de `pgs_spend_threshold`, frequency ≤ `pgs_freq_max`; ação: +5% de budget; schedule 3×/semana. **A rule nasce DESATIVADA** (nenhuma ação automática roda até o membro revisar e ativar no Ads Manager, junto com a campanha). Gravar a escolha em `pgs_enabled` no dados.json. Se o membro recusar ou nenhum caminho MCP suportar a criação, `pgs_enabled: false` — e a Skill 11 então NÃO promete escala automática (ela orienta configurar quando fizer sentido).

**Regras invioláveis da criação:**
- **Tudo nasce em `status: PAUSED`** (inclusive Automated Rules — nascem desativadas). O membro revisa e ativa. A skill NUNCA ativa nada sozinha.
- Os **gates da ETAPA 1** (compliance + promise↔config + disclosure "AI Info") rodam ANTES de criar — não há criação sem gate verde (ou override explícito do membro).
- Reutilizar as receitas existentes onde aplicável: `upload-creative-to-meta.md` (subir os criativos + criar o creative object) e o setup de MCP em `.claude/automations/setup-mcps.md`.
- Após criar, **guardar os IDs retornados** (campaign_id, ad_set_id, ad_ids) no JSON e no manifest — a Skill 11 lê esses IDs pra puxar insights.

**Mensagem ao membro após criar em PAUSED:**
> "Criei a campanha `[nome]` em **PAUSED** na sua conta — 1 ad set broad/Advantage+, [N] criativos, budget $[budget de teste efetivo]/dia ([multiplicador]× o breakeven CPA de $[breakeven]), otimizando pra Purchase. Revisa no Ads Manager (audiência, budget, criativos) e **ativa quando estiver OK**. Não ativei nada por você. [Se houver concepts com `ai_disclosure_required: true`:] Os ads [lista] têm humano gerado por AI — confirma que o label 'AI Info' está marcado neles antes de ativar (GATE 3)."

Se a criação via MCP falhar (rate limit, auth), aplicar `.claude/rules/emergency-escape-paths.md` ES6: backoff, depois oferecer **(A)** retomar em 1h, ou **(B)** cair pro Caminho 3 manual com a estrutura formatada.

### ETAPA 7 — Erros Comuns a Evitar

1. **NÃO criar múltiplos ad sets pra "testar mais"** — fragmenta o aprendizado. 1 ad set, vários criativos. Diversificação é escala (Skill 12), não teste.
2. **NÃO usar detailed targeting / interests** — o criativo faz o targeting. Adicionar interest só encolhe o pool e limita o algoritmo.
3. **NÃO mexer antes de 3 dias** — cada mudança (budget, audiência, pausar criativo) reseta o sinal. Deixar rodar.
4. **NÃO usar daily minimums** ("garantir $X de spend") — força o Meta a gastar em impressão ruim pra bater meta. Deixar a otimização fluir.
5. **NÃO misturar 2 produtos numa conta** — embaralha o aprendizado. 1 conta por produto.
6. **NÃO subir budget muito acima de 2× breakeven CPA "pra acelerar"** — não acelera o teste, só queima caixa. 2× breakeven CPA é o número (pra baixo, só a regra de mínimo viável da ETAPA 3 — nunca menos que 1× breakeven).
7. **NÃO escalar manualmente durante o teste** — escala é depois do winner (Skill 12).
8. **NÃO ler CTR como verdade** — CPA é o que manda; isso a Skill 11 detalha. Aqui só não tome decisão de kill na base de CTR.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/10-ad-strategy/` antes de salvar.

`workspace/[produto]/10-ad-strategy/ad-strategy.md` (no `report_language`) contendo:
1. Estrutura de teste completa: 1 campanha → 1 ad set → N criativos (ETAPA 3)
2. Budget de teste EFETIVO com o multiplicador aplicado — default 2× breakeven CPA; 1× no mínimo viável da ETAPA 3; perto de 1× quando `margin_warning` capou — sempre o número REAL calculado pra este produto, nunca "2×" carimbado
3. Warmup de conta (se aplicável) e cadência quarta→domingo / 7 dias (ETAPAS 4-5)
4. Naming convention aplicada (Campaign / Ad Set / Ad)
5. UTM schema preenchido
6. Janela de decisão e handoff pra Skill 11 (ETAPA 5)
7. Checklist de credibilidade da loja com os gaps encontrados (ETAPA 2)
8. Status da criação via MCP (criado em PAUSED / fallback manual) + IDs retornados
9. Checklist de erros a evitar (ETAPA 7)

**Dual output:** gerar `10-ad-strategy/ad-strategy.html` companion (mesmo diretório) usando `.claude/templates/aura-report-template.html` como base — CSS inline, self-contained, **logo SVG do Aura no topo copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` (NUNCA texto)**, componentes aura (callout, note, danger, winner, kpi-grid, table-wrap). O `.md` é fonte pra AI; o `.html` é visualização humana.

### JSON companion — `10-ad-strategy/dados.json`

```json
{
  "strategy_id": "uuid",
  "product_slug": "...",
  "creative_batch_ref": "08-creative-engine/dados.json batch_id (concepts[].id é o handoff 08→10→11)",
  "breakeven_cpa": 80,
  "budget_multiplier": 2.0,
  "test_budget_daily": 160,
  "structure": "1_campaign_1_adset_broad",
  "campaign": {
    "name": "...",
    "objective": "Sales",
    "optimization": "purchase_max_conversion",
    "budget_level": "ad_set",
    "daily_budget": 160,
    "attribution": "7d_click_1d_view",
    "placements": "advantage_plus",
    "targeting": "advantage_plus_broad",
    "one_account_per_product": true
  },
  "ad_set": {
    "name": "...",
    "creative_count": 7,
    "creative_concept_ids": []
  },
  "account_warmup": { "required": false, "days": 3, "engagement_budget_daily": 50 },
  "cadence": { "launch_day": "wednesday", "kill_by": "sunday", "max_days": 7 },
  "pgs_enabled": false,
  "pgs_cpa_threshold": 40,
  "pgs_spend_threshold": 80,
  "pgs_freq_max": 1.5,
  "store_credibility": { "instagram": "ok", "reviews_count": 0, "comment_management": "flagged", "gaps": [] },
  "mcp_creation": { "path": "official|pipeboard|manual", "status": "created_paused|fallback_manual", "campaign_id": "", "ad_set_id": "", "ad_ids": [] },
  "utm_schema": {}
}
```

> **Campos `pgs_*`:** defaults derivados da oferta — `pgs_cpa_threshold` = target CPA (o alvo de 2× ROAS da 04), `pgs_spend_threshold` = breakeven CPA, `pgs_freq_max` = 1.5. São os campos que a receita `full-deploy.md` (Stage 4 — a rule nasce DESATIVADA, alinhada à ETAPA 6 desta skill) e a Skill 11 leem; `pgs_enabled` só vira `true` se a Automated Rule foi criada E o membro ativou.
>
> **Campo `budget_multiplier`:** o multiplicador REALMENTE aplicado sobre o breakeven CPA (`test_budget_daily = breakeven_cpa × budget_multiplier`). Default 2.0; 1.0 no mínimo viável da ETAPA 3; entre 1.0 e 2.0 quando `margin_warning` capou o budget. Os valores do exemplo (80/2.0/160) são ilustrativos — grave sempre os números reais do produto.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `10-ad-strategy` em `skills_completed`
- Registrar `strategy_id`, `creative_batch_ref`, `test_budget_daily`, `breakeven_cpa`
- **Gravar `10_campaign_name`** com o nome da campanha gerado (naming convention). A Skill 11 lê via `read_manifest("10_campaign_name")` pra cruzar com dados do Meta.
- Se criou via MCP, gravar `10_campaign_id` / `10_ad_set_id` (a Skill 11 puxa insights por ID, mais robusto que por nome).
- Registrar `pgs_enabled` (se a Automated Rule de PGS foi criada e ativada pelo membro) — a Skill 11 lê esse campo antes de falar em "escala automática".
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza ABRIR-AQUI.html).

## Mensagem Final

Apresentar como **draft pronto pra revisão** (`.claude/rules/iteration-driven-refinement.md`), não como "pronto, pode escalar":

"Estrutura de teste montada: campanha `[nome]`, **1 ad set broad/Advantage+** com **[N] criativos**, otimizando pra Purchase, budget **$[budget de teste efetivo]/dia** ([multiplicador]× o seu breakeven CPA de $[breakeven]) ([se MCP] já criada em **PAUSED** na sua conta — revisa e ativa).

Plano de teste: [se conta nova: 3 dias de warmup de engajamento primeiro, depois] lançar **quarta**, deixar até **domingo**, **3 dias sem mexer**. Se até domingo não vendeu, a gente mata e roda o próximo.

Quando ativar e passarem **3 dias**, diga **'ad analysis'** e me manda os dados (ou eu puxo via MCP) — aí a 11 lê CPA por criativo, CPM da conta e os benchmarks de funil pra decidir o que mantém, o que mata e o que está pronto pra escalar.

Antes de ativar: confere a credibilidade da loja (reviews, comentários dos posts) — [resumo dos gaps da ETAPA 2, se houver]. Quer que eu ajuste algo na estrutura — budget, número de criativos, mercado?"
