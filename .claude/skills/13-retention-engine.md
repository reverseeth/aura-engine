---
name: retention-engine
description: Setup automático de fluxos de retenção/lifecycle email via ESP (Klaviyo primário; Omnisend/MailerLite/Shopify Email via assets + setup-guide), em DUAS fases. Fase A (PRÉ-LAUNCH, depois da 07d/05 e antes dos criativos) = flows de RECUPERAÇÃO disparados por evento — abandoned cart + post-purchase welcome — infraestrutura de cash flow que se arma ANTES de ligar tráfego pago (receita mais barata que existe, custa zero no free tier), SEM segmentação; NÃO é email marketing. Fase B (PÓS-LAUNCH, ≥50 compras) = win-back, replenishment, cadência/segmentação + ops básicas (chargeback, refund da garantia, CS). Cria os flows via Klaviyo MCP oficial quando disponível, com fallback pra assets HTML + setup-guide que o membro importa. Use quando o membro disser "retention", "email flows", "automation", "lifecycle", "Klaviyo" — a fase certa é detectada no pré-flight.
---

# Retention Engine

## Quando Usar — DUAS fases

Esta skill roda em dois momentos diferentes do pipeline, com escopos diferentes. O framing importa: **a Fase A é infraestrutura de cash flow, não email marketing** — campanhas/newsletters de email continuam sempre pós-launch.

**Fase A — Flows de recuperação (PRÉ-LAUNCH, na ordem canônica: depois da 07d/05 Fase A, antes dos criativos da 08):** operador de elite nunca liga tráfego pago sem o abandoned cart flow armado — é a receita mais barata que existe (recupera parte dos ~70% de carrinhos abandonados) e custa zero (free tier do ESP). A Fase A monta APENAS os flows disparados por evento que recuperam dinheiro do tráfego do launch:
- **Abandoned Cart** (fluxo 2) — o coração da fase
- **Post-Purchase Welcome** (fluxo 3) — mata buyer's remorse, reduz refund, pede a primeira review
- **Welcome Series Email 1** SÓ SE a página promete welcome offer / há bonus com `delivery_trigger: on_signup` (promessa da página precisa existir no dia 1 — mesmo princípio da Fase A da 05)

**SEM segmentação na Fase A** — não há base pra segmentar (zero ou quase zero compradores), e não precisa: são flows por evento, funcionam com o primeiro visitante.

**Fase B — Retenção completa (PÓS-LAUNCH, ≥ 50 compras no ESP):** com dados mínimos existe o que segmentar. Entram: Welcome Series completo (emails 2-4), Win-Back, Replenishment, cadência/coordenação de lista, e as ops pós-launch (chargeback, refund da garantia, CS básico — seção própria). Antes de 50 compras, segmentação é noise — por isso ela espera.

## Base de conhecimento (contrato de cobertura — NUNCA query genérica)

Esta skill puxa SISTEMAS NOMEADOS de email lifecycle e psicologia de persuasão da base — não query genérica tipo "email flows" ou "abandoned cart". E a puxada é **cobertura do tópico, não amostra** (contrato completo: `.claude/lib/kb-index/README.md`):

1. **Abra a seção inteira dos domínios, sempre.** No início de cada fase/fluxo que consulta a base, abra `.claude/lib/kb-index/frameworks.json` e enumere TODAS as entradas dos domínios `retention-email` e `persuasion-psychology` cujo `use_in_skill` inclui a 13 — não só as embutidas no texto. As queries embutidas nos fluxos abaixo são o **núcleo mínimo garantido de cada etapa, nunca o teto**: entrada relevante à fase que não está embutida É PARA SER PUXADA do mesmo jeito. (Duas entradas de OUTROS domínios também pertencem a esta skill e já estão embutidas no ponto de uso: **Desire Calendar** em `market-research-voc` e **Subscription Economics Playbook** em `finance-projections`.)
2. **Rode a `best_query` exata de cada entrada relevante, com `deep=true`**, puxando o sistema completo (a curva de decaimento de abandoned cart com os 5 motivos de abandono, não "dicas de cart recovery").
3. **Relevância é por FASE, não por preguiça:** a pergunta é "esta entrada informa a decisão desta etapa?" — se a resposta for "talvez", puxa. Só se descarta o que claramente pertence a outra fase da skill (e será puxado lá).
4. **Não repita busca de framework já puxado na mesma sessão** — entradas duplicadas entre domínios apontam pro MESMO conteúdo; reuse o resultado.
5. **Encerramento de etapa:** antes de fechar cada fase, releia a lista enumerada do passo 1 e confirme que nenhuma entrada relevante ficou sem puxar.

A contagem de entradas por domínio **vem sempre do próprio `frameworks.json`** (fonte da verdade) — nunca de número fixo escrito no texto desta skill.

## Pré-flight

**Idioma (report_language).** Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Todo output interno (`13-retention-engine/retention-engine.md`/`.html`, `flow-metadata.json` descritivo, mensagens e perguntas ao membro) usa esse idioma. **A copy dos emails em si (subject, preview, body, CTA) permanece SEMPRE em inglês US**, independente do report_language — é consumidor-final do mercado US.

### Detecção de FASE (primeiro passo)

Ler `manifest.retention` (se existir) + `manifest.skills_completed`:

- **Fase A** se: `manifest.retention.phase_a_done != true` E o storefront existe (`07b-page-build` em `skills_completed` — sem loja no ar, não há evento de cart/purchase pra disparar flow). É o caminho normal pré-launch: `10-ad-strategy` AINDA NÃO rodou, e está tudo bem — a Fase A vem ANTES dela na ordem canônica.
- **Fase B** se: `manifest.retention.phase_a_done == true` E a campanha está ativa E há **≥ 50 compras** no ESP/Shopify (perguntar ao membro se não houver dado). Se o membro pedir "retention" com < 50 compras e Fase A já feita, explicar que win-back/segmentação prematuros viram noise e oferecer: revisar/otimizar os flows da Fase A com os dados que já existem, ou esperar o volume.
- Membro pediu explicitamente um flow específico → respeitar, mas avisar se está fora da fase (ex: win-back com 10 compras).

### Gate de consistência (Skill 09) — phase-aware
Ler `workspace/[produto]/09-consistency-audit/dados.json` **se existir**:
- **Na Fase A, arquivo ausente é o NORMAL** — a 13 Fase A roda ANTES da 09 na ordem canônica (a 09 audita inclusive os emails da Fase A, via check M7). Prosseguir sem cerimônia.
- Se existir com `launch_recommendation == "BLOCK"` → os fluxos de email vão herdar o drift detectado (mecanismo divergente, VOC sem rastreio, oferta diferente da página) e propagar inconsistência pra base de subscribers. Oferecer ≥2 caminhos: **(A)** rodar a skill 09 agora pra corrigir o drift, OU **(B)** prosseguir mesmo assim marcando `manifest.skipped_preflight += ["09-consistency-audit"]` e avisando no output final que recomenda re-executar após corrigir.
- Se `CAUTION` → exibir warnings e pedir OK do membro antes de gerar fluxos.
- Se `GO` → prosseguir.

### Checagens por fase

- [ ] **Fase A:** `07b-page-build` em `skills_completed` (loja no ar). **Fase B:** `10-ad-strategy` em `skills_completed` + campanha ativa + ≥ 50 compras (detecção acima).
- [ ] **ESP identificado (as duas fases).** Ler `manifest.esp` (e `profile.md` → `esp: "klaviyo" | "omnisend" | "mailerlite" | "shopify_email" | "none"` — enum exato do manifest-schema, `shopify_email` com underscore). Se o campo estiver **ausente** (membro nunca rodou setup completo), PERGUNTAR inline ao membro qual ESP ele usa e gravar a resposta em `manifest.esp`. Se `esp: "shopify_email"`, **não abortar** — seguir direto pro Caminho 2 (assets + setup-guide adaptado ao editor do Shopify Email); ver a nota de limitações na seção do Caminho 2. Se `esp: "none"` (membro não tem ESP), **não abortar** — recomendar Klaviyo (free tier até 250 contatos + Shopify integration nativa — o custo zero é parte do argumento da Fase A), e se o membro topar, gravar `manifest.esp = "klaviyo"` e seguir; se ele preferir decidir depois, gerar os fluxos no fallback HTML + setup-guide (seção abaixo) pra ele importar quando escolher.
- [ ] `04-offer-builder/offer-builder.md` (ou o legado `relatorio.md` — mesmo fallback vale pras outras fases) + `04-offer-builder/dados.json` carregados (pra saber a janela de reorder, guarantee period, e os `bonuses[]` com seus `delivery_trigger`)
- [ ] `02-market-research/market-research.md` carregado (objeções = hooks de win-back; dores = hooks de abandoned cart)
- [ ] `06-copy-engine/dados.json` carregado **(if exists)** → campo `email_hooks[]` (3-5 hooks de follow-up que a 06 gera na ETAPA 7, derivados das top-5 headlines + Big Idea + objeções — inglês US; também na seção canônica `## Email Follow-up Hooks` de `copy-engine.md`). É o seed dos subject lines/aberturas dos flows — ver nota em "Fluxos base". Ausente (copy legada, gerada antes do contrato) → derivar os hooks das headlines de `copy-engine.md` direto.
- [ ] `15-finance-engine/dados.json` carregado **(if exists)** → bloco `cohorts`, quatro campos: `ltv_pct_by_month`, `decay_factor`, `crossover_month` e `churn_spike_day`. É a curva de LTV **medida** do negócio (a 15 a calcula a partir dos cohorts reais do membro), e ela troca o benchmark por número em três lugares: o beat de churn do post-purchase (fluxo 3), a janela de reorder do replenishment (fluxo 5) e o gatilho do win-back (fluxo 4). **Fallback:** arquivo ausente, ou `cohorts.calibrated: false` / `decay_source: "assumed"` — os fluxos rodam pelos benchmarks e pela janela declarada pelo membro, exatamente como hoje. A 15 nunca é pré-requisito desta skill.

## TrendTrack MCP (opcional, se conectado)

Se há tools com prefixo `mcp__trendtrack__` disponíveis:

- **`mcp__trendtrack__analyze_shop_emails`** com domínio de 1-3 concorrentes do `03-competitor-analysis/competitor-analysis.md` → retorna padrões reais de cadência, subject lines e content categories da concorrência. Use como referência (não copy-paste) pra calibrar timing dos fluxos abaixo (welcome series, abandoned cart, post-purchase) com benchmark de mercado.

Se TrendTrack NÃO estiver disponível, segue templates abaixo direto, baseados em VOC + offer.

## Divisão de papéis pós-compra (05 / 13 / 14) — fonte única de verdade

Três skills tocam o pós-compra. Pra não duplicar nem sobrescrever, cada artefato tem UM dono:

| Artefato | Quem PRODUZ | Quem ENTREGA | Nota |
|---|---|---|---|
| Asset do bônus (PDF/e-book, config GWP, link) | **Skill 05** | — | A 05 gera o asset e define o `delivery_trigger`. Não monta email. |
| **Email de entrega de bônus** | **Skill 13** (este) | **Skill 13** | A 13 é o ÚNICO executor de email. A 05 fornece conteúdo + trigger; a 13 monta o flow e injeta o `{{BONUS_LINK}}`. Nunca duplicar lógica de email na 05. |
| Flows de lifecycle (welcome, abandoned-cart, post-purchase, win-back, replenishment) | **Skill 13** | **Skill 13** | Fonte única dos flows de retenção. |
| Email-sequence derivada do winner (recycler) | **Skill 14** | Membro (importa manual) | É **variação A/B de nutrição** derivada do criativo winner, NÃO um flow de lifecycle. Não colide nem sobrescreve o welcome/post-purchase da 13 — entra como flow separado/teste paralelo. Ver nota na Skill 14. |

Regra prática: se é email que dispara por evento de ciclo de vida (signup, cart, compra, inatividade, reorder) → é flow da 13. Se é peça de nutrição reaproveitada de um winner pra testar contra o que já roda → é a 14, e o membro decide onde plugar sem desligar os flows da 13.

## Conexão com bonuses da oferta (Skill 04)

Antes de gerar os fluxos, ler `04-offer-builder/dados.json.bonuses[]` e casar o `delivery_trigger` de cada bonus com o email do fluxo que entrega:

| `delivery_trigger` | Fluxo / email que entrega o bonus |
|--------------------|-----------------------------------|
| `on_signup` | Welcome Series — Email 1 (boas-vindas) |
| `post_purchase` | Post-Purchase Welcome — Email 1 (obrigado) |
| `day_7_post_purchase` | Post-Purchase Welcome — Email 3 (~dia 7) |
| `on_first_reorder` | Replenishment — Email 2/3 (no reorder) |

Incluir o asset/link do bonus (PDF, Circle invite, código de acesso — produzidos na Skill 05) no corpo do email correspondente. Se a Skill 05 ainda não gerou o asset, deixar placeholder `{{BONUS_LINK}}` no HTML e avisar no output final que o link precisa ser colado antes de ativar.

## Fluxos base (templates — adaptam ao produto)

**Mapa fluxo → fase:**

| Fluxo | Fase | Por quê |
|---|---|---|
| 2. Abandoned Cart | **A (pré-launch)** | Recupera dinheiro do primeiro dia de tráfego — a razão de existir da Fase A |
| 3. Post-Purchase Welcome | **A (pré-launch)** | Comprador do dia 1 recebe reassurance + entrega de bônus + review request |
| 1. Welcome Series | **A só o Email 1, SE há welcome offer/bonus `on_signup`** (promessa da página existe no dia 1); série completa (emails 2-4) = **B** | Sem oferta prometida no opt-in, nurturing é assunto pós-launch |
| 4. Win-Back | **B (≥ 50 compras)** | Precisa de base com inativos — não existe pré-launch |
| 5. Replenishment | **B (≥ 50 compras)** | Precisa da janela de consumo real validada |

**Frameworks de governança que valem pra TODOS os fluxos** (puxe uma vez, aplique em todos):
- **The Rule of 1** — cada email tem UM objetivo, UM job por elemento, UM leitor; escrever o CTA primeiro (rode `Rule of 1 email one goal one job per element one reader write CTA first`)
- **3-to-1 Value-to-Sales Rule** — equilíbrio de cadência entre emails de valor e de venda, pra não queimar a lista (rode `3 to 1 rule value emails sales email balance newsletter cadence`)
- **Email/SMS Coordination Rule (echo, don't collide)** — se o membro também roda SMS, escalonar (email primeiro, SMS follow-up pra não-openers), nunca colidir (rode `email SMS coordination echo not collide send email first SMS follow up non-openers staggered cadence`)
- **Drayton Bird's Email = Direct Mail Principle** — tratar cada email como carta de uma pessoa real, subject = headline, copy longa quando o argumento exige (rode `Drayton Bird email direct mail principle long copy real person subject line headline`)

**Seed de subject lines — `06-copy-engine/dados.json.email_hooks[]`:** os 3-5 hooks que a 06 gerou são o ponto de partida dos subject lines e das primeiras linhas dos flows de maior volume (welcome, abandoned cart, post-purchase) — eles já carregam a Big Idea, o mecanismo nomeado e as objeções reais do mercado, então usar eles garante message match entre o que o subscriber viu no ad/página e o que chega no inbox. Adapte cada hook ao contexto do flow (o mesmo hook vira curiosity no welcome e urgency no abandoned cart), não copie 1:1 nos 5 flows. Hooks são consumidor-final: **sempre inglês US**, ad-safe (rule 8b).


### 1. Welcome Series (novo subscriber, sem compra ainda) — Fase A só o Email 1 (condicional); série completa na Fase B

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **5-Step Welcome Sequence Process** — welcome = lead-nurturing, não "bem-vindo" genérico (rode `welcome sequence lead nurturing 5 step process VOC research plan automate not a template`)
- **DotCom Secrets' Soap Opera Sequence** — 5-email bonding (set the stage → high drama → epiphany → hidden benefits → urgency) pra estruturar o arco da série (rode `DotCom Secrets soap opera sequence 5 email set the stage high drama epiphany hidden benefits urgency`)
- **Expert Secrets' Email Epiphany Funnels** — quebrar as 3 false beliefs (vehicle / internal / external) ao longo dos emails 2-3 (rode `Expert Secrets email epiphany funnels vehicle internal external false belief epiphany bridge`)
- **From-Name as Inbox Filter** — definir o From name como pessoa real, não brand genérica, pra deliverability (rode `From name inbox filter mobile Gmail gatekeeper real person test from line deliverability`)
- **Restock / Testimonial / Anniversary Coupon Welcome Beats** — batidas de ecommerce pra calibrar o conteúdo de cada email (rode `ecommerce welcome series restock coupon testimonial week 5 anniversary coupon weekly post-purchase beats`)

- Email 1 (imediato): boas-vindas + reforço do motivo do opt-in + code do welcome offer (se houver)
- Email 2 (dia 2): educação sobre o mecanismo único (do `04-offer-builder/offer-builder.md`) + soft CTA
- Email 3 (dia 4): social proof stack + trust reinforcement
- Email 4 (dia 7): urgency layer + hard CTA. **Branch obrigatório:** se existe welcome code, a urgência é a expiração real do code (cross-check com o Promise↔Config gate — regra de rigor 4). Se NÃO existe welcome offer, NUNCA inventar deadline — usar urgência legítima alternativa: estoque real, prova social acumulada ("2.400 já compraram"), ou recap do mecanismo + custo de adiar o resultado.

### 2. Abandoned Cart (viewed product, added to cart, didn't checkout) — FASE A (pré-launch)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Abandoned-Cart Decay Curve + Two Sequence Styles** — quando disparar (curva de decaimento, Baymard 69.8%) e escolher entre estilo Discount-focused vs Emotion-focused conforme margem (rode `abandoned cart decay curve Baymard 69.8% discount-focused emotion-focused sequence escalating discount day 0 6 hours`)
- **5 Reasons People Abandon (objection map)** — mapear o motivo real de abandono pra Email 2 (preço / urgência / experiência negativa / info incompleta / ceticismo), cruzando com objeções do `02-market-research/market-research.md` (rode `five reasons people abandon cart price urgency negative experience incomplete information skepticism objection map`)
- **Kennedy's 4-Step Follow-Up Campaign** — Re-state / Second Notice / Final Notice / Change Offer pra estruturar a escalada dos 4 emails (rode `Kennedy 4-step follow-up campaign re-state second notice final notice change offer No BS Direct Marketing`)
- **Inoculation Theory** — pré-armar a objeção #1 antes que o cliente a verbalize (rode `inoculation theory McGuire weakened attack pre-emptive defense competitor argument resistance`)

- Email 1 (1h após abandon): "Esqueceu de algo?" + produto no cart + 1 benefício-chave
- Email 2 (24h): objeção quebrada (escolher objeção #1 do market research) + testimonial
- Email 3 (72h): urgência (stock/time) + discount code se margem permite
- Email 4 (7d, opcional): "last call" + reforço de garantia

### 3. Post-Purchase Welcome (comprou pela primeira vez) — FASE A (pré-launch)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Kennedy's Post-Purchase Reassurance Letter** — pós-compra como profit center: matar buyer's remorse no Email 1 (rode `Kennedy post-purchase reassurance letter buyer remorse profit center order confirmation`)
- **Collier's Re-Sell After Shipment (Acknowledgment Letter)** — revender o que já foi comprado, reduzir returns, construir antecipação até a entrega (rode `Collier re-sell after shipment acknowledgment letter reduce returns build anticipation testimonial`)
- **Zero-Party Data Moat** — usar o Email 2/3 pra coletar dado de preferência (post-purchase survey/quiz) que alimenta personalização futura (rode `zero-party data moat post-purchase survey onboarding quiz preference center unreplicable personalization`)
- **30-60-90 Day LTV Email+SMS Flow Hacks** — janela da segunda compra; estruturar os emails 3-4 pra cair dentro dela (rode `30-60-90 day LTV email SMS flow hacks second purchase window zero-party data force multiplier`)

- Email 1 (30min pós-purchase): obrigado + unboxing tips + delivery ETA
- Email 2 (dia da entrega estimada): "chegou?" + how-to-use tutorial
- Email 3 (dia 7-10): request review (com incentivo)
- Email 4 (dia 21-30): cross-sell ou replenishment trigger (se consumível)

**O beat do pico de churn (a batida que decide a segunda compra).** A maior parte do abandono acontece num único momento, tipicamente quando o produto chegou, foi testado e a decisão foi tomada — a referência de mercado é **por volta do dia 45**, e é justamente onde o post-purchase acima acaba (dia 21-30) e o win-back ainda não começou (60+ dias). O Email 4 é o que cobre essa lacuna, e o timing dele não é palpite quando existe número:

- **Com `15-finance-engine/dados.json` (cohorts medidos):** posicione o Email 4 alguns dias **antes** de `cohorts.churn_spike_day` — chegar depois do pico é falar com quem já decidiu sair. O conteúdo do email é ditado pela leitura da curva: se `cohorts.ltv_pct_by_month` mostra queda forte já no mês 1, o email ataca uso e resultado (o cliente não chegou a experimentar o benefício); se a queda vem depois, ataca reposição e continuidade. Use `cohorts.crossover_month` como a régua de quanto vale investir aqui: é o mês em que o cohort cruza pra positivo, ou seja, até lá o cliente ainda não pagou o próprio CAC.
- **Sem o arquivo da 15 (ou com `cohorts.calibrated: false`):** mantenha o dia 21-30 do Email 4 e trate o dia ~45 como referência de mercado, não como medida do negócio — dizendo isso ao membro em uma frase, e não escrevendo o benchmark no doc como se fosse número dele.

### 4. Win-Back (60+ dias sem purchase, subscriber ativo) — FASE B (pós-launch, ≥ 50 compras)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Hormozi's 9-Word Email** — reativação curta ("are you still interested in [resultado]?") como abertura mais barata e de maior reply (rode `Hormozi 9-word email are you still interested reactivation dormant leads $100M Leads`)
- **Kennedy's Collection Agency Model** — escalada de urgência em intervalos com mudança de formato a cada email (rode `Kennedy collection agency model multi-step mailing format change urgency intervals`)
- **Collier's Ruffle-Smooth-Ruffle** — alternar tom emocional (tensão → alívio → tensão) pra furar a habituação de quem ignora (rode `Collier ruffle smooth ruffle alternating emotional tone collection series habituation`)
- **Fórmula de Reorder + Winback com desconto progressivo** — a escada dos 3 emails: abrir pelo frame de progresso do cliente (está progredindo → vai progredir mais → vai perder o progresso) e só escalar o desconto quando o frame não converter; o mesmo sistema traz a fórmula de reorder ("7 dias antes de acabar o estoque") que alimenta o timing do Email 1 do Fluxo 5 — puxou aqui, reuse lá (rode `você está progredindo vai progredir mais continue vai perder o progresso, 7 dias antes de acabar o estoque`)
- **Engagement Suppression / Sunset & Double-Opt-In Re-engagement** — definir o ponto de corte: quem não reativar vai pra sunset/suppression pra proteger deliverability (rode `engagement suppression sunset re-engagement double opt-in unsubscribe non-engaged deliverability 30 day`)

- Email 1: "sentimos sua falta" + novidade do produto
- Email 2 (7 dias depois): oferta especial com código de win-back
- Email 3 (14 dias depois): final call + feedback survey pra entender porque churn

**Gatilho com número medido (se `15-finance-engine/dados.json` existir):** os "60+ dias sem purchase" são um default de mercado. Com a curva medida na mão, o disparo certo é logo depois de `cohorts.churn_spike_day` (quem passou do pico sem recomprar é inativo de fato, não alguém ainda dentro da janela normal de consumo) — e o tamanho do incentivo do Email 2 se calibra por `cohorts.crossover_month`: cliente que ainda não cruzou pra positivo não comporta desconto agressivo, porque o cohort dele nem pagou o CAC. **Sem o arquivo, mantenha os 60+ dias**, como hoje.

### 5. Replenishment (consumíveis — trigger baseado na janela de reorder) — FASE B (pós-launch)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Day Zero Triggered-Email Method** — replenishment é behavior-triggered mini-funnel (dispara pelo timing real de consumo), não drip por tempo fixo (rode `Day Zero behavior-triggered email mini-funnel outperforms time-based drip cap day 4`)
- **Fibonacci Drip-Cadence Sequence** — espaçamento dos nudges antes/depois do produto acabar (day 0/1/2/3/5/8) (rode `Fibonacci sequence drip campaign email cadence day 0 1 2 3 5 8 spacing Copyhackers`)
- **Door-Closing Aversion** — enquadrar a janela de reorder como opção que expira (subscription/2-pack antes de acabar o estoque dele) (rode `door-closing aversion loss of options Shin Ariely expires midnight only 3 spots disappearing bonus`)
- **Subscription Economics Playbook (8 passos)** — a economia da assinatura que o Email 2 oferece: take rate, one-click upsell pós-compra e produto dimensionado pra supply de 1 mês; ler junto do bloco "Arquitetura de assinatura" abaixo antes de escrever o Email 2 (rode `playbook de subscription take rate one-click upsell pós-compra supply de 1 mês`)

A janela de reorder não vem pronta do `04-offer-builder/dados.json` (ele não produz um `reorder_rate` legível por máquina). Defina a fonte assim, antes de configurar o fluxo:

1. PERGUNTAR ao membro: "Em quantos dias um cliente típico **acaba** uma unidade do produto?" (ex: um sérum de 30ml dura ~30 dias).
2. Calcular o timing dos emails a partir disso: Email 1 dispara ~5-7 dias **antes** do produto acabar (ex: produto dura 30 dias → Email 1 no dia 23-25 pós-compra), Email 2 perto do fim, Email 3 logo após o fim estimado.
3. Cruzar com benchmark: a 2ª compra ideal cai **antes de 65 dias** pós-primeira-compra. Se a duração informada empurrar o reorder pra além disso, antecipar o nudge (oferecer subscription/2-pack) pra não perder a janela.
4. **Cruzar com a curva medida, quando existir** (`15-finance-engine/dados.json` → `cohorts`): `ltv_pct_by_month` mostra em qual mês a recompra de fato acontece nesse negócio, e `decay_factor` diz o quanto ela decai de um mês pro seguinte. Se a janela declarada pelo membro no passo 1 não bate com o mês em que a curva medida acusa recompra, **a curva medida vence** — ela é o comportamento real, a estimativa dele é memória. Se a recompra medida vier depois de `cohorts.crossover_month`, o Email 2 é o momento de empurrar assinatura/2-pack com mais força: sem isso o cohort demora demais pra pagar o CAC. **Sem o arquivo da 15 (ou com `cohorts.calibrated: false`), os passos 1-3 decidem sozinhos**, como hoje.

- Email 1 (~5-7 dias antes do acabar): "seu [produto] tá acabando — reorder aqui"
- Email 2 (perto do fim): subscription option pelo preço-base (o one-time é que custa mais)
- Email 3 (pós-acabar): "hora de reabastecer"

**Arquitetura de assinatura (ler `04-offer-builder/dados.json.subscription_architecture`):**
- `onetime_plus_sub_no_reorder` → o **Email 2 deste fluxo é O momento canônico** de oferecer a assinatura (a PDP vendeu one-time de propósito; a conversão pra assinatura foi delegada pra cá).
  > **Framing corrigido (2026-09-01):** a 04 não dá mais desconto ao assinante — ela cobra um **prêmio de ~15% no one-time**. Leia `onetime_premium_pct` (o campo antigo `sub_discount_pct` existe só por compatibilidade e é **sempre 0**; usá-lo faria o email prometer "0% de desconto"). O framing correto é *"você paga mais por NÃO assinar"*: a assinatura é o preço-base, o avulso é que carrega o prêmio. Razão econômica: o desconto entregaria margem exatamente na recompra, que é onde ela é melhor.
- `subscription_first` → o fluxo mira só quem comprou one-time (assinante já tem reorder automático — mandar replenishment pra assinante é ruído); filtrar por não-assinante no trigger.
- `no_subscription` (ou campo ausente) → Email 2 oferece o 2-pack/bundle no lugar da assinatura.

## Sazonal (Fase B) — handoff

Dois donos, ninguém órfão: a 13 executa os **FLOWS** (sempre-ligados, disparados por evento) e a adaptação sazonal deles; as **CAMPANHAS** sazonais (Q4, Black Friday/Cyber Monday, promos datadas — sends agendados pra lista) são orquestradas pela skill **17-promo-engine**, que chama a 13 pra gerar os assets de email de cada send. Na prática: pedido de "campanha de email" / "Black Friday" / "promo" → a 17 é a dona do calendário, da mecânica da promo e dos segmentos; a 13 entrega os emails e mantém os flows coerentes com a promo no ar (flow NUNCA desliga durante campanha — se adapta). A copy dos emails sazonais permanece **inglês US** (regra de rigor 2); o handoff e o relatório seguem o `report_language`.

**Timing — quando religar/adaptar mensagens por época:**
- **Desire Calendar** — decide QUANDO adaptar a mensagem dos flows por época: como os 6 desejos flutuam mês a mês, Fresh Start Effect (janeiro e setembro) e Early Shopping Migration (antecipar a mensagem em 4-6 semanas) (rode `calendario sazonal de desejos health sex status belonging control comfort por mes`)

**Sistemas dos assets sazonais (puxar quando a 17 chamar — ou quando o membro pedir a campanha direto):**
- **Playbook Q4 de Email & SMS** — targeting pyramid (engaged 30 / engaged 90 / dormant 120), email tolera volume e SMS é cirúrgico, quiet hours (rode `email tolera volume SMS é cirúrgico, engaged 30 engaged 90 dormant 120, quiet hours texas`)
- **Campanha de 4 Dias e os 6 templates** — a estrutura de promo curta, incluindo o dia de slump e o template da inveja (rode `campanha sazonal de 4 dias com 6 templates, dia de slump, template da inveja`)
- **Sequências promocionais formulaicas (Holiday 3 / Black Friday 6 / Flash Sale 24h 3)** — os esqueletos por tipo de sale: razão pra sale, stock-up recommendation, sale de 24h "não planejada" (rode `razão para a sale, stock up recommendation, sale de 24 horas não planejada`)

**O lado dos FLOWS durante a campanha (trabalho da 13, sem esperar a 17):**
- **Seasonal Abandoned-Cart SMS Update Checklist** — atualizar o abandoned cart durante a janela da promo: detalhes da oferta, hora exata de fechamento, urgência/escassez reais e sem "rain check" (rode `seasonal abandoned cart SMS update checklist offer details campaign close time urgency scarcity no rain check`)

## OPS pós-launch (Fase B — seção compacta, junto dos flows de retenção)

Retenção não é só email: com pedidos rodando, três rotinas operacionais protegem a conta de pagamento e a margem. Entregar como checklist curto no relatório da Fase B (não é skill separada — é higiene):

**1. Chargeback (alvo: taxa < 1% dos pedidos):**
- **Responder TODA disputa com evidência** — tracking com entrega confirmada, screenshot da PDP com a promessa exata, log do email de confirmação, histórico de contato. Disputa não-respondida é derrota automática.
- **Refund proativo > disputa perdida:** cliente irritado ameaçando chargeback → reembolsar ANTES da disputa abrir. Chargeback custa a taxa + o produto + o strike na conta; refund custa só o pedido. Acima de ~1% de taxa, o processador aplica reserve/hold — exatamente o cenário que trava a escala (ver Skill 12, ETAPA 6).
- Sinais que previnem: descriptor de cartão reconhecível (nome da marca, não LLC genérica), email de confirmação imediato, tracking enviado assim que existe.

**2. Refund da garantia (macro de processo — a promessa da 04 sendo honrada):**
- A garantia definida na 04 e prometida na página é operação, não copy: definir o passo-a-passo UMA vez (macro) — pedido chega → conferir elegibilidade (janela/condição da garantia) → reembolsar sem fricção → registrar o motivo.
- Refund da garantia SEM interrogatório: garantia "sem perguntas" que na prática exige 5 emails vira chargeback + review negativa. O motivo registrado alimenta a iteração da oferta na 04 (padrão de motivo = sinal de produto/promessa desalinhados).
- Se a garantia é Level-2 (keep-the-premium, da 05/04): o cliente fica com o bônus — a macro lembra de NÃO pedir devolução dele.

**3. CS básico (o mínimo que segura a nota):**
- Caixa de suporte monitorada (o reply-to dos flows aponta pra ela) com resposta em < 24h úteis — atraso de resposta é o maior gerador de disputa "item not received".
- 5 macros prontas: onde está meu pedido (tracking + prazo), quero reembolso (macro da garantia acima), produto chegou danificado (reenvio direto, foto opcional), como usar (link do how-to do post-purchase), cancelar assinatura (se houver — sem fricção, com oferta de pausa).
- Comentários dos ads NÃO são CS — são gestão de comentários (rotina da Skill 10 ETAPA 2), mas reclamação real que aparece lá entra no funil de CS.

## Setup Pipeline — Klaviyo

Cascade resiliente (detecção de prefixo conforme `.claude/lib/mcp-detect/README.md`), **dois caminhos só**: **Klaviyo MCP oficial → HTML + setup-guide**. Não há caminho de session-cookie/internal-API — foi removido por risco de segurança (cookie dava acesso full à conta) e fragilidade (endpoints sem contrato público). Automação confiável = MCP oficial; sem MCP, fallback é assets + guia que o membro importa.

### Caminho 1 (PREFERENCIAL) — Klaviyo MCP oficial

Detecte se há tools com prefixo `mcp__klaviyo__` na sessão (Klaviyo MCP oficial, 25 tools, 2026):

```
klaviyo_mcp_available = existe ao menos 1 tool com prefixo `mcp__klaviyo__` na sessão
```

Se **disponível**, CRIE os flows direto via MCP (com contrato estável, sem scraping):

1. Gerar o HTML de cada email adaptando ao produto (usa `06-copy-engine/copy-engine.md` pra copy + `02-market-research/market-research.md` pra VOC + `04-offer-builder/offer-builder.md` pra mecanismo), mesma geração do caminho de assets.
2. Criar cada flow **da FASE ativa** (Fase A: abandoned cart + post-purchase welcome, + Welcome Email 1 se condicional; Fase B: welcome series completo, win-back, replenishment) via as tools `mcp__klaviyo__*` de flow creation/configuration: trigger, filtros, ações (email/delay/branch), subject + preview + conteúdo HTML.
3. **Flows criados SEMPRE em draft/manual** — nunca ativar automaticamente (regra "NUNCA ativar automaticamente" abaixo vale igual aqui: risco de spam se um email tiver bug). Membro revisa no Klaviyo UI e ativa.
4. Logar `source: "klaviyo_mcp"` no `13-retention-engine/dados.json` e no `automation-log.jsonl`.
5. Salvar os assets (HTML + flow-metadata.json) em paralelo, pra o membro ter material mesmo que queira ajustar fora do MCP.

Se uma chamada MCP falhar (auth, rate limit, tool indisponível), cair silenciosamente pro **Caminho 2** sem insistir — o membro vê os fluxos prontos pra importar do mesmo jeito.

### Caminho 2 (FALLBACK confiável) — assets + setup-guide

Gerar os assets prontos + setup-guide e o membro importa no Klaviyo UI. Veja a seção "Caminho 2 detalhado — assets + setup-guide" abaixo. Default quando não há Klaviyo MCP. Logar `source: "klaviyo_assets_guide"`. Vale também pra Omnisend/MailerLite/Shopify Email/outros ESPs (que não têm MCP).

### NUNCA ativar automaticamente (vale pros dois caminhos)

Ativar flow via skill — por MCP ou de qualquer outra forma — = risco de spam se algum email tiver bug. Skill SEMPRE deixa em draft/manual. Membro revisa no UI do ESP antes de ativar.

## Caminho 2 detalhado — assets + setup-guide (todos os ESPs)

Este é o caminho confiável e o fallback da skill quando não há MCP — vale pra Klaviyo e pra Omnisend/MailerLite/Shopify Email/outros. Skill gera:

1. `workspace/[produto]/13-retention-engine/[fluxo]/email-1.html`, `email-2.html`, etc (HTML pronto)
2. `workspace/[produto]/13-retention-engine/[fluxo]/setup-guide.md` com step-by-step manual no dashboard do ESP (trigger, delays, subject/preview de cada email, onde colar o HTML)

Membro faz o setup manual seguindo o guia, skill entrega os materiais prontos.

**Nota específica pra `esp: "shopify_email"`:** o Shopify Email (com Shopify automations/Flow) cobre bem welcome, abandoned cart e post-purchase, mas os flows com branch/segmentação avançada (win-back por janela de inatividade, replenishment com timing por consumo) são limitados. O setup-guide adapta: usa as automations nativas onde existem, e converte os flows que o Shopify Email não suporta em campanhas agendadas manualmente (com o timing calculado no guia). Avisar no output final: quando o membro passar de ~$5k/mês em receita de email, migrar pra Klaviyo destrava os 5 flows completos + segmentação — recomendar a migração sem forçar.

## Compliance & deliverability

Pra cada email gerado:

- **Subject line**: < 50 chars ideal; sem ALL CAPS; sem emoji excessivo
- **Preview text**: 40-70 chars
- **Unsubscribe link**: obrigatório no footer (CAN-SPAM + GDPR)
- **From name**: "[Brand Name]" — não email genérico tipo "noreply@"
- **Reply-to**: endereço monitorado (replies de cliente vão pra algum lugar)
- **Spam trigger words check (checklist inline — a lib `compliance-preflight` cobre ad-flags de Meta/TikTok, não spam de email; não usar aqui):** revisar subject + body contra: "FREE!!!" e variações all-caps, "ACT NOW", "LIMITED TIME!!!", "GUARANTEED", "RISK-FREE", "100% free", excesso de `!` e `$`, subject inteiro em caixa alta, mais de 1 emoji no subject. Esses padrões derrubam inbox rate (caem em Promotions/Spam) — reescrever antes de salvar

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/13-retention-engine/` antes de salvar.

Salvar:

1. **`workspace/[produto]/13-retention-engine/[fluxo]/email-N.html`** — HTML pronto de cada email do fluxo (consumidor final; responsive table-based email HTML, NÃO o design-system Aura)
2. **`workspace/[produto]/13-retention-engine/[fluxo]/flow-metadata.json`** — metadata de cada email (subject, preview, trigger, delay)
3. **`workspace/[produto]/13-retention-engine/retention-engine.md`** — relatório operacional do setup pra AI ler em skills futuras (resumo dos fluxos criados, triggers, status)
4. **`workspace/[produto]/13-retention-engine/retention-engine.html`** — visualização humana (AI report) usando `.claude/templates/aura-report-template.html` como base. Logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html`). Componentes: `.section-label` por fluxo, `.pill` pra status (DRAFT/ACTIVE), `.callout` pra avisos de compliance.
5. **`workspace/[produto]/13-retention-engine/dados.json`** — log de flows criados + timestamps + status + delivery results + `phase` (`"A" | "B"`) por flow

**Distinção importante:** os emails em si (item 1) são HTML de email marketing (table-based, inline styles pra ESP compatibility) — NÃO usam o design-system Aura, NÃO têm logo Aura. Já os relatórios internos (itens 3-4) seguem a rule 6b do CLAUDE.md normalmente.

Atualizar o `manifest.json`:
- `skills_completed` ← adicionar `"13-retention-engine"` (na primeira fase concluída; sem duplicar).
- **Bloco `retention` (contrato de fase — é o que a Skill 10 lê no checklist de credibilidade e o que a detecção de fase desta skill usa):**

```json
"retention": {
  "phase_a_done": true,
  "phase_a_flows": ["abandoned_cart", "post_purchase"],
  "phase_b_done": false
}
```

(`phase_a_flows` inclui `"welcome_email_1"` quando o condicional se aplicou; a Fase B atualiza `phase_b_done: true` e adiciona os flows dela.)

- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html), onde `<slug>` é o `product_slug`.

## Regras de rigor

1. **NUNCA ativar flow sem revisão humana** — risco de spam em escala
2. **Dois idiomas, dois papéis.** A copy dos emails (subject, preview, body, CTA) é consumidor-final do mercado US e fica SEMPRE em **inglês**, independente do `report_language`. Já o relatório interno (`13-retention-engine/retention-engine.md`/`.html`), o setup-guide e a conversa com o membro seguem o `report_language` do `profile.md` (default `pt-BR`). Nunca misturar: nunca email em português, nunca relatório interno forçado em inglês quando o membro escolheu pt-BR.
3. **Replenishment requer a janela de reorder definida** — perguntar ao membro em quantos dias o produto acaba (ver Fluxo 5). Se o produto é one-time (não consumível), pular Fluxo 5.
4. **Welcome offer code precisa existir** — cross-check com Promise↔Config gate antes de enviar
5. **Rate limit**: ao criar flows via Klaviyo MCP oficial, respeitar o rate limit da API pública (spacing entre chamadas; ao receber 429, backoff conforme ES6). No fallback (assets + guide) não há chamada de API, então não se aplica.

## Mensagem Final

**Fase A:**

"Flows de recuperação prontos no [ESP] em DRAFT — abandoned cart ([N] emails) + post-purchase ([N] emails)[+ welcome Email 1, se aplicou]. Isso é a infraestrutura de cash flow do launch: recupera parte dos carrinhos abandonados desde o primeiro dia de tráfego, a custo zero. Próximos passos:

1. Abre o dashboard do [ESP]
2. Revisa cada email (subject + preview + body)
3. **Ativa os flows ANTES de ligar a campanha** — flow em draft não recupera nada

Próximo passo na ordem de launch: diga **'creatives'** (Skill 08). Win-back, replenishment e segmentação ficam pra Fase B — quando você tiver ~50 compras, me chama com 'retention' de novo."

**Fase B:**

"Fluxo [X] configurado no [ESP] em DRAFT. [N] emails gerados. [+ checklist de OPS pós-launch no relatório: chargeback, refund da garantia, macros de CS.] Próximos passos:

1. Abre o dashboard do [ESP]
2. Revisa cada email (subject + preview + body)
3. Ativa o flow quando estiver OK

Depois que o flow rodar por ~14 dias, acompanha open rate / CTR / receita por fluxo direto no dashboard do [ESP] (Klaviyo → Analytics → Flows; Omnisend/MailerLite → relatório de automação). Me chama de volta com esses números (ou um screenshot) que eu analiso o que tá performando e onde ajustar."
