---
name: creator-engine
description: Engine de creators da marca — a operação completa de conteúdo humano que as fontes primárias tratam como motor real de escala. Roda em DUAS fases. Fase A (Content Engine, pode começar junto com a 08 e antes do launch) = product seeding (enviar produto de graça em troca de conteúdo) em plataforma tipo Insense ou por outreach manual, casting com diversidade de creator amarrada aos sub-avatares da 02, framework de brief (nunca script fechado), B-roll de referência, follow-up e coleta, corte de cada vídeo em 3 hooks, e o pipeline TikTok Shop como fábrica de volume. Fase B (Performance Program, SÓ depois de breakthrough confirmado pela 11) = creator vencedor vira contrato recorrente, escada de embaixador com comissão em degraus, whitelisting (rodar ads do perfil do creator), partnership ads, raw content campaign, creator farming e recrutamento pago de afiliados. A 08 continua dona do QUE dizer (conceitos, roteiros, produção IA); esta skill é dona de QUEM grava e da relação com quem grava. Use quando o membro disser "creators", "ugc", "seeding", "influencer", "whitelisting", "ambassador", "insense", "conteúdo de creator".
---

# Creator Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md`) — domínios `affiliate-creator-channels` (esta skill é a consumidora que faltava, inclusive das entradas dormant), `creatives-hooks-formats` (as entradas de creator/seeding/brief), `meta-ads-strategy` (partnership ads + feedback loop), `scaling` (raw content, níveis de escala, time criativo), `team-hiring-ops` (creator pipeline) e `competitor-positioning` (descoberta de whitelisting de concorrente). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> **Cânones que governam esta skill:** `.claude/lib/ad-taxonomy/README.md` — as 4 classes de resultado (§2: só `breakthrough` libera a Fase B), o escopo estreito do Shotgun (§7: volume sem estratégia individual é legítimo SÓ no pipeline de conteúdo de creators) e a estrutura de campanha. Esta skill **não cria campanha nem mexe em budget** — quem roda o que ela produz são as skills 10 e 12, dentro do cânone.

## Quando Usar — DUAS fases

O motor de creators resolve o problema que trava a maioria das marcas: conteúdo. Content é o arquivo bruto (a foto ou o vídeo cru); creative é o content editado com headline, logo e copy. Cada peça de content rende um número finito de criativos antes de esgotar — e os maiores anunciantes testam cerca de **11x mais criativos** que o resto (dado citado por Hormozi em $100M Leads, a partir de dados do próprio Facebook). Sem abundância de conteúdo, não há volume de teste; sem volume de teste, não há winning ad. **"Você está literalmente vendendo conteúdo"** — ninguém toca o produto online.

**Fase A — Content Engine (paralela à 08, pode começar antes do launch):** montar o funil que gera conteúdo humano em escala a custo perto de zero — product seeding, casting, framework de brief, coleta — e que existe pra encontrar **um brand ambassador** (embaixador da marca: o creator contratado recorrente), não pra achar um winning ad de primeira (isso é bônus). Começar cedo importa: do momento de contratar um creator externo até o conteúdo virar ad no ar passam **~26 dias** na média da fonte (com creator da casa, ~4 dias). Quem só começa a semear quando precisa de criativo já está um mês atrasado.

**Fase B — Performance Program (SÓ depois de breakthrough confirmado pela 11):** o creator cujo ad virou breakthrough sobe de degrau — contrato recorrente, escada de comissão, whitelisting, partnership ads, raw content campaign, e o recrutamento contínuo (creator farming e ads de recrutamento). Antes de um breakthrough existir, nada disso tem base: whitelisting amplifica o que já venceu, nunca procura vencedor.

**O que esta skill responde e nenhuma outra respondia:** de onde vem o conteúdo humano em volume, quem grava, quanto se paga em cada degrau, como o creator vencedor vira ativo recorrente da marca, e como o canal TikTok Shop vira fábrica de conteúdo.

**O que ela NÃO faz:** não decide o que o ad diz nem produz criativo por IA (08); não monta campanha nem mexe em budget (10/12); não classifica criativo (11); não recicla breakthrough (14 — inclusive o `creator-report.md` do Movimento 6 continua sendo da 14). Divisão explícita:

| Artefato / decisão | Dono | Papel desta skill (16) |
|---|---|---|
| Conceitos, roteiros, prompts de IA, EDLs | **08** | Fornece o conteúdo bruto licenciado e recebe os conceitos como semente de hooks dos briefs |
| Estrutura de campanha, ad sets, budget (inclui raw content campaign e campanha de whitelisting) | **10/12** | Entrega identidades (páginas de creator com acesso), conteúdo cru e a convenção de nome com o creator |
| Classificação (loser / kpi_winner / spend_winner / breakthrough) | **11** | Lê a classificação pra saber QUAL creator venceu |
| Reciclagem de breakthrough + creator report do Movimento 6 | **14** | Fornece o roster e a regra de visibilidade de números por creator |
| Roster de creators, seeding, briefs, contratos, escada de embaixador, whitelisting/partnership como RELAÇÃO | **16 (esta)** | Dona |

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Todo output interno (`creator-engine.md`/`.html`, conversa com o membro) usa esse idioma. **Todo material que vai pro creator fica SEMPRE em inglês US** — framework/brief, mensagens de outreach, contrato, report de feedback. Creator é público dos EUA: vale a mesma regra da copy consumidor-final.

### Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] **Detecção de fase** (primeiro passo, decidida pelos dados — não perguntada):
  - **Fase A** se `manifest.creator.phase_a_done != true`. Roda em paralelo com a 08, a partir do momento em que existe produto com preço definido. Não exige campanha no ar. Com `phase_a_done: true` e ainda sem breakthrough, "creators" continua sendo Fase A — o ciclo de seeding, follow-up e coleta é contínuo (creator farming, ETAPA 14), não um evento único.
  - **Fase B** se existe ao menos um criativo `class: "breakthrough"` em `manifest.ad_classification[]` (ou `manifest.breakthroughs[]` não-vazio) — gravado pela 11. **Sem breakthrough, a Fase B não roda**: se o membro pedir "whitelisting" ou "ambassador" antes disso, explique que o programa de performance amplifica vencedor confirmado, e ofereça rodar/continuar a Fase A (que é o que produz os candidatos).
  - Membro pediu um pedaço específico (ex: "só o brief") → respeitar, avisando em uma linha se está fora da fase.
- [ ] `workspace/[produto]/02-market-research/dados.json` — fonte de `core_avatar` + `sub_avatars[]` (a variável de diversidade do casting). Se faltar, não aborte seco (rule `emergency-escape-paths.md` ES1): ofereça **(A)** rodar a 02 agora, OU **(B)** prosseguir pedindo ao membro uma descrição direta do avatar, marcando `manifest.skipped_preflight += ["02-market-research/dados.json"]`.
- [ ] `workspace/[produto]/04-offer-builder/dados.json` — preço/AOV do produto (`pricing.aov_expected`): o seeding depende do valor de varejo (regra do ≥ ~US$ 30, ETAPA 2) e a margem limita o que dá pra pagar por vídeo. Ausente → pedir preço e custo direto ao membro (mesmo escape ES1).
- [ ] **Fase A:** `07b-page-build` em `skills_completed` é o ideal (a plataforma de seeding pede o link do site — a página "vende" a marca pro creator). Sem loja no ar, a rota de outreach manual anda mesmo assim com fotos + preço; a campanha na plataforma espera o site.
- [ ] **Fase B adicionalmente:** `workspace/[produto]/11-ad-analysis/dados.json` + `manifest.ad_classification[]` carregados, e os ads de creator identificáveis (convenção de nome com o creator, ou o membro aponta qual ad é de qual creator).
- [ ] Rodadas anteriores desta skill em `workspace/[produto]/16-creator-engine/` (roster existente continua de onde parou — nunca recomeça do zero).

### Contexto a carregar

1. `workspace/profile.md` — stage e budget (`member-stage-awareness.md`). O stage muda a rota, não a regra: **starter/validating** = seeding grátis + filmar você mesmo/família (nunca recomendar creator pago pra starter — anti-pattern explícito da rule); **scaling** = campanhas pagas por vídeo, retainers, e a Fase B inteira quando o gate abrir.
2. `workspace/[produto]/02-market-research/dados.json` — `sub_avatars[]` com `angle` (cada sub-avatar pede um tipo de creator diferente — é a entrada da Creator Diversity na ETAPA 3) e `market_vocabulary`.
3. `workspace/[produto]/08-creative-engine/dados.json` **(se existir)** — os conceitos do batch atual viram a semente do bloco de hooks do framework (ETAPA 5). Sem a 08 rodada, os `angles` dos sub-avatares da 02 cumprem o papel.
4. `workspace/[produto]/11-ad-analysis/dados.json` + `NEXT_BATCH_IDEAS.md` **(Fase B)** — quem venceu, com que ângulo, e o que a análise pede pro próximo batch (vira ideia enviada ao creator).
5. `workspace/[produto]/12-scale-engine/dados.json` **(se existir)** — a sub-fase de escala calibra quantos creators em retainer o negócio comporta (tabela da ETAPA 8 da 12: de 0 no teste a 4+ na otimização) e quando raw content campaign e whitelisting entram (níveis de escala, ETAPA 14 desta skill).
6. `workspace/[produto]/14-content-recycler/` **(se existir)** — o `creator-report.md` de um breakthrough reciclado é material de kickoff pra novos ambassadors.

### Regras que não se negociam

1. **Material de creator é inglês US, sempre** — brief, mensagem, contrato, report. Relatório interno segue `report_language`.
2. **Whitelisting só de creator que já tem breakthrough com a marca, e só com os ads DELE na página dele.** As duas primeiras regras da fonte, sem exceção. Whitelisting amplifica vencedor; não procura vencedor.
3. **Transparência por tier:** creator em retainer simples NÃO vê receita/ROAS (só spend e soft metrics — senão pede aumento sem entender os outros custos); creator no programa de performance vê os números (ele ganha % deles).
4. **Contrato gerado é referência, não aconselhamento jurídico** — a própria fonte diz isso dos templates dela. Todo contrato salvo carrega esse aviso e a recomendação de revisão por advogado.
5. **Conteúdo de terceiros sem licença não vai ao ar.** A fonte pratica o "borrowed time" (rodar vídeo ripado do TikTok Shop com metadata limpa); o guard-rail desta engine é o da 08: clipe de terceiro serve como referência de estrutura e timing, nunca entra em ad sem cessão de direitos. Conteúdo do roster É licenciado — o contrato/plataforma cede os direitos por escrito.
6. **Números de remuneração não se inventam:** ou são os defaults da fonte (declarados como referência) ou vêm do membro. Nenhum tier novo sai de estimativa.
7. **Campanha é território da 10/12.** Esta skill entrega gente, acesso e conteúdo; nunca cria campanha, ad set ou regra de budget.

### Puxe os SISTEMAS NOMEADOS da base (contrato de cobertura — NUNCA query genérica)

A puxada é **cobertura do tópico, não amostra** (contrato completo: `.claude/lib/kb-index/README.md`):

1. **Abra a seção inteira dos domínios, sempre.** No início de cada ETAPA que consulta a base, abra `frameworks.json` e enumere TODAS as entradas dos domínios `affiliate-creator-channels`, `creatives-hooks-formats`, `meta-ads-strategy`, `scaling`, `team-hiring-ops` e `competitor-positioning` cujo `use_in_skill` inclua a 16 **ou** que estejam nomeadas nesta seção (o retag do índice acompanha a criação desta skill). As queries embutidas abaixo são o **núcleo mínimo garantido, nunca o teto**.
2. **Rode a `best_query` exata de cada entrada relevante, com `deep=true`** — ela traz o sistema completo (a escada de comissão com os 4 degraus e o teto, não "como pagar creators").
3. **Relevância é por FASE:** se a resposta pra "esta entrada informa a decisão desta etapa?" for "talvez", puxa. Só se descarta o que pertence a outra fase (e será puxado lá).
4. **Não repita busca de framework já puxado na mesma sessão** — os sistemas de recrutamento pago e de ad bounties existem em mais de um domínio e apontam pro MESMO conteúdo; reuse o resultado.
5. **Encerramento de etapa:** releia a lista enumerada e confirme que nenhuma entrada relevante ficou sem puxar.

**Esta skill é a consumidora que faltava do domínio `affiliate-creator-channels`** — inclusive das entradas marcadas dormant (`use_in_skill: "—"`) de TikTok Shop, custom link e programa de afiliados automatizado. A partir dela, elas são puxáveis.

**Mínimo a carregar na Fase A:**

- **Content Engine (casting → produção → review → seeding, corte em 3 hooks)** — `content engine framework casting producao review 3 timestamps 3 hooks Insense seeding SOP`
- **UGC Creator Sourcing Engine (2 papéis + aprovação em 7 passos + tracker diário)** — `engine de 2 roles sourcer VA senior 7-step approval workflow hashtag hunting daily tracker`
- **Creator Diversity Matrix** — `creator diversity matrix idade raca genero idioma espanhol caracteristicas fisicas psicografia`
- **Creator Brief Generator (14 seções)** — `creator brief generator 14 secoes must-say must-avoid emotional memory prompts hook direction`
- **UGC Brief Prompt (perguntas sobre o creator + shot list em 2 partes)** — `UGC brief prompt perguntas sobre creator direct camera shot list b-roll`
- **Estrutura de time criativo por faturamento (o modelo de um único creator)** — `estrutura de time criativo por faturamento creative pods Leanne model um creator`
- **Creator Pipeline (hit rate 14% de creators vs 4% interno)** — `creator pipeline hit rate 14 por cento creators versus 4 por cento interno`
- **DailyVirals Workflow (sandbox / transcript / AI analysis / AB compare)** — `DailyVirals virais do dia TikTok Shop transcript downloader rewriter AB compare sandbox`
- **Rip Method + Borrowed Time (só como referência de estrutura — regra 5 acima)** — `ripar top videos tiktok shop limpar metadata borrowed time criativo proprio ao lado`
- **Operação de TikTok Shop** _(dormant até esta skill)_ — `operacao de TikTok Shop samples afiliados comissao e conteudo`
- Setup da campanha de seeding (objetivo, screening questions, valor de varejo mínimo) — `product seeding no Insense awareness reach screening questions valor de varejo minimo 30`
- Campanha paga por vídeo e o objetivo real do processo — `objetivo do product seeding achar brand ambassador nao winning ad campanha paga 100 150 por video`
- Framework em vez de script (o doc de blocos) — `frameworks vs scripts documento de 6 blocos max 9 concepts dealer's choice first-pick bias`
- Curadoria do framework por creator — `curadoria de framework por creator first-pick bias 4 a 6 conceitos freestyle script espectro`
- Follow-up e coleta — `follow-up com creator a cada 3 dias coleta conteudo drive marcar DCT corte em 3 hooks`

**Adicionalmente na Fase B:**

- **Brand Ambassador Ladder (retainer + comissão em degraus)** — `retainer 500 por video semanal performance program regra do 2-3 comissao decrescente 10 5 2.5 1`
- **Feedback Loop de Creator via Atria + benchmarks de soft metric** — `custom report por creator ad name contains thumb stop ratio 42-48% 3s ate 15s Loom`
- **Whitelisting de Creators (6 regras + Leasy + faixas de budget)** — `whitelisting rodar ads do perfil do creator Leasy custom request 6 regras over-leverage`
- **Partnership Ads (dynamic identity + pitch de 30 dias)** — `partnership ads dynamic identity 1.3% mais barato pedir acesso 30 dias creator novo`
- **Whitelist Ads / página de nicho spin-off** — `whitelist ads pagina de nicho spin-off rodar ads pelo perfil do creator`
- **Whitelisted/Affiliate Ad Discovery (espionar o ecossistema do concorrente)** — `facebook ads library buscar termos que a marca usa revela whitelisted pages creators`
- **Raw Content Campaign** — `raw content campaign creators seeding Insense flexible ads low intent brand ambassadors`
- **Full Media Buying 2026 (as 5 camadas — onde a raw content vive)** — `estrutura full media buying 2026 cinco camadas main CBO ABO zombie raw content promo`
- **Levels of Scaling (quando raw content e whitelisting entram)** — `levels of scaling zero to 50k 100k per day one campaign CBO raw content ASC whitelisting segmented`
- **Creator Farming** — `creator farming cultivar base de creators antes de precisar deles`
- **Recrutamento pago de afiliados + TikTok Shop como máquina de conteúdo** — `rodar paid ads para recrutar afiliados save 40% apply to be brand ambassador TikTok Shop conteudo` (mesma doutrina da entrada `recrutar afiliados com trafego pago apply to be brand ambassador` em `affiliate-creator-channels` — puxou uma, reuse)
- **Custom Link + atribuição de afiliado** _(dormant até esta skill)_ — `custom link de afiliado atribuicao de venda por creator`
- **Social Snowball (programa de afiliados automatizado)** _(dormant até esta skill)_ — `Social Snowball programa de afiliados automatizado comissao por cliente`
- **Ad Bounty Model + menu de sourcing de conteúdo** — `ad bounties editores performance-based Gridbank Insense Arcads film yourself B-roll sourcing`
- Onboarding do embaixador — `onboarding de brand ambassador deck contrato kickoff report mensal transparencia de numeros`

## Fluxo da Skill

**ETAPA 1 roda sempre. ETAPAs 2-7 são da Fase A. ETAPAs 8-14 são da Fase B** e são puladas silenciosamente quando o gate de breakthrough não abriu — sem seção vazia no relatório (rule `report-only-results.md`). ETAPA 15 roda sempre.

### ETAPA 1 — Detectar a fase e inventariar o que já existe

Aplique a detecção do pré-flight e grave `phase` + `phase_reason`. Depois, **pré-popule tudo antes de perguntar qualquer coisa**: roster anterior (rodadas passadas desta skill), sub-avatares da 02, conceitos da 08, classificação da 11, preço da 04.

Peça numa única mensagem só o que não vive em arquivo nenhum:

- **Budget mensal de conteúdo** (separado do budget de mídia): decide a rota — seeding grátis (custa produto + frete), campanha paga por vídeo, ou os dois. Referências da fonte: campanha paga sai a **US$ 100-150 por vídeo**; budget mínimo recomendado pra rodada paga **~US$ 1.000**, ideal US$ 2-3k+ (operação madura dedica US$ 5-6k/mês a conteúdo); e a régua de cima: **investir no mínimo 5% do ad spend em produção criativa** (10%+ já é agressivo).
- **O que o membro já tem:** creators conhecidos, conteúdo cru parado, conta em plataforma de creators, operação de TikTok Shop.
- **Quem opera o dia a dia** (o próprio membro ou uma VA — assistente virtual). Grave a resposta em `operator` no `dados.json`. A operação mínima da fonte é 1 VA cuidando de achar creators, gerenciar campanhas e fazer follow-up, mais alguém mandando ideias. Estrutura de time além disso é assunto da skill 18-team-engine.

**O objetivo declarado da Fase A** (escreva no relatório): encontrar **um brand ambassador** — o creator que sozinho é estrategista + copywriter + cinegrafista + editor (contratar essas 4 funções separadas custaria US$ 10k+/mês; um creator faz por US$ 100-150 por vídeo ou de graça no seeding). Winning ad no meio do caminho é bônus, não a meta. Pra marca abaixo de 7 dígitos, esse creator único É o time criativo.

### ETAPA 2 — [Fase A] Canal de seeding e a campanha

**Product seeding** = enviar produto de graça em troca de conteúdo, sem obrigação de post no perfil do creator. É a porta de entrada do funil e custa só produto + frete.

**Cascata de canal (na ordem):**

1. **Plataforma de creators (Insense é a principal da fonte).** Licença US$ 500/mês ou US$ 1.200 por trimestre; campanhas pagas têm taxa de 10% sobre os créditos. A fonte testou e descartou alternativas: Join Brands (não recomendada) e Backstage (abandonada — creators não entregavam ads polidos).
2. **Outreach manual (custo zero de plataforma):** busca por hashtag do nicho, DM no X/Twitter e Instagram, e-mail personalizado. É a rota de quem não tem budget de plataforma — e a rota inteira da loja sem site no ar.
3. **Filmar você mesmo / família** — legítimo e provado (caso da fonte: marca foi de US$ 5k pra US$ 225k/mês com mãe e irmã filmando). Pra starter, é frequentemente a rota certa junto com o seeding.

**Checagem de viabilidade antes de abrir campanha:** valor de varejo do produto **≥ ~US$ 30** (produto barato demais atrai poucas aplicações). AOV baixo dificulta o seeding — compense vendendo visão na copy da campanha ("estamos escalando; earning potential de até US$ 10k/mês pra quem criar um winning ad") pra atrair creator com propósito, e selecione depois.

**Setup da campanha de seeding (SOP da fonte, 2025):**

1. Objetivo **Awareness & Reach** (é onde o seeding vive na plataforma; as outras opções são de mídia paga).
2. Número de creators: na prática ilimitado no seeding (ex. da fonte: 90) — é conteúdo grátis.
3. Comissão: não — "a menos que você crie um winning ad; aí vem oferta de retainer". A campanha já planta a escada.
4. Detalhes do produto: 5 fotos (screenshots do site servem), link, preço.
5. **Especificações do creator (mais importante que audiência):** só EUA; gênero/idade espelhando o avatar da 02; categorias afins; inglês fluente. **Seguidores e engagement são irrelevantes** quando o objetivo é só o conteúdo (sem obrigação de post).
6. **Screening questions** (economizam horas de triagem — filtre as aplicações pelas respostas): "What specific issue would you be talking about in your video?" (texto livre — força a pessoa a planejar); pergunta de conforto com o tema sensível do nicho quando houver (sim/não); **"Whitelisting will be required when we run your ad — do you agree?"** (sim — já deixa o acesso combinado desde o dia 1); "Are you able to provide a selfie with the product for our website?".
7. Direção criativa: cole 3-5 conceitos sugeridos + do's & don'ts (o brief completo vai depois da contratação, ETAPA 5).
8. Rode **múltiplas campanhas simultâneas** quando houver mais de um tipo de cliente — uma por sub-avatar relevante.

**Campanha paga por vídeo (US$ 100-150):** quando o seeding num nicho apertado gera pouca aplicação (a fonte viu 1-4 por campanha em nicho duro; a campanha paga gerou 10 — mais que as quatro anteriores somadas), a campanha paga destrava volume e qualidade — e exige seletividade muito maior na triagem (portfólio, foto de perfil, TikTok do creator). Sem budget, não faça: o seeding continua válido.

**Benchmark de fluxo:** campanha bem montada em produto amplo gerou **74 aplicações em ~48h** na fonte. Se creators não querem seu produto NEM DE GRAÇA, o sinal é de produto/oferta — leve essa leitura de volta pra 01/04 em vez de insistir no funil.

### ETAPA 3 — [Fase A] Casting: triagem, shortlist e Creator Diversity

**Triagem (SOP):** abra o Instagram/site da marca ao lado pra calibrar o fit. Pra cada aplicante: perfil social real (estilo de vida, idade aparente, contexto do avatar, qualidade do conteúdo) + histórico na plataforma (trabalhos anteriores, reviews de outras marcas) + engajamento.

- **Sinais positivos:** aplicação personalizada com ideia própria (vale mais que template genérico); contexto de vida compatível com o avatar (a avó que cozinha, pra marca de kit de confeitar).
- **Sinais de alerta:** perfil social indisponível/sem link (peça o link antes de decidir); histórico fraco na plataforma.
- **Regra de decisão: na dúvida, PASSE.** Só entra na shortlist quem convence. O creator não vai a lugar nenhum.
- Mensagem padrão de shortlist (inglês, sem contratar ainda): interesse + "encaminhei seu perfil pro time; te confirmo em breve" — a contratação é etapa separada.

**Creator Diversity — os 6 eixos cruzados com `sub_avatars[]` da 02.** Quem escolhe creators tem viés (aparência, dicção, iluminação) e acaba anunciando anos pro mesmo avatar com o mesmo tipo de creator. Cada sub-avatar da 02 pede um tipo de creator, e cada eixo abaixo é um teste barato que pode destravar mercado novo:

| Eixo | O que testar deliberadamente |
|---|---|
| Faixa etária | Quantas faixas você realmente testa? Produto caro pede creator com idade/cara de quem PODE pagar (caso da fonte: produto de US$ 100-120/mês rodando com creators jovens — o teste certo era 45-55+) |
| Raça/etnia | Sair da zona de conforto do creator "fácil de achar" |
| Gênero | Conforme o produto — e sem dogma: uma das maiores marcas da fonte vende produto masculino com creators mulheres ("here's why you need this as a man") |
| **Idioma** | **Espanhol nos EUA é altamente subestimado** — um único criativo em espanhol escalou a US$ 10k/dia só regravando ads já provados em inglês |
| Características físicas | Teste o espectro inteiro, inclusive quem parece com o cliente REAL e não com a aspiração — o caso da fonte: US$ 15k/dia no TikTok com um único criativo de um homem muito acima do peso, câmera tremida, dentro da caminhonete. Otimize pra identificação, não pra perfeição |
| Psicografia | O que o creator "parece fazer" sem dizer (roupa de yoga vs ambiente simples) — contexto comunica classe e estilo de vida |

**Registro:** todo creator entra no `roster[]` do `dados.json` com o sub-avatar que ele cobre e os eixos de diversidade que ele preenche. O relatório mostra a matriz: sub-avatar × creator — as células vazias são o casting que falta.

### ETAPA 4 — [Fase A] Contratação, envio e a escolha do produto

1. Aprovados → **Hire** na plataforma (libera o endereço) → mensagem padrão pós-contratação (inglês): pedir e-mail pra tracking + confirmação do endereço de envio.
2. **O creator ESCOLHE o produto** — o anti-conteúdo-inautêntico da fonte: com múltiplos SKUs, "let us know your two favorite pairs from this collection"; produto único, pergunte só a variante/cor. Nunca envie o que o creator não quer ("leads to poor and unauthentic content"). Se o catálogo está bagunçado, crie uma collection dedicada pra creators escolherem.
3. Rastreie: produto enviado → entregue → em produção. Statuses do roster: `applied | shortlisted | approved | hired | product_sent | filming | content_received | complete | dropped`.

### ETAPA 5 — [Fase A] O framework de brief (nunca script fechado)

**Framework, não script.** Peça a 10 pessoas pra venderem o mesmo óculos e cada uma escolhe o atributo que ressoa com ela — e a execução sai genuína, às vezes revelando ângulo que você nem listou. "You want creators to do what they're supposed to do: CREATE." O espectro é Freestyle ↔ Framework ↔ Script completo: **framework é o padrão**; script completo só quando você escreve muito bem, tem UMA ideia específica forte e o creator tem estilo compatível; freestyle total só pra creator excepcional. Creator micro não executa script — "let the creator cook", dê ideias.

**Estrutura do framework (1 página escaneável, em inglês):**

1. **Your Mission** — por que o vídeo importa + a oportunidade de ganho ("If your first video becomes a winning ad, you can join us on a $500 monthly retainer... This is your shot to create an ad that earns up to $10K/month."). Dá motivo pra caprichar num vídeo grátis.
2. **About the brand** — 2-3 linhas NO MÁXIMO.
3. **Do's & Don'ts** — be authentic, real-life scenarios, natural well-lit settings, fun/relatable/unscripted; DON'T overscript, don't use polished language, don't focus only on the product (nada de testimonial básico). Inclua aqui as palavras/claims proibidos da marca (compliance da rule 8b vale pro que o creator fala).
4. **Video specs** — 9:16, e o combinado de entrega (cru ou editado).
5. **Hooks & Ideas — o bloco onde você exerce o marketing.** MÁXIMO 9 concepts; cada concept = nome + UM hook escrito + 2-3 linhas de contexto de cena (sem roteirizar a fala). A semente vem dos conceitos da 08 (se existir batch) e dos `angles` dos sub-avatares da 02. Se algo já está escalando na conta, o primeiro concept aponta pra lá; se nada escala ainda, brief de apostas variadas, não iterações.
6. **Film your B-rolls** — B-roll = cenas de apoio sem fala. Cole 2+ GIFs de referência com uma linha do que filmar ("não filme exatamente isso; é referência"). Mini-SOP: Giphy Capture (macOS) sobre um winning ad ou UGC anterior → recorte o trecho → cole na tabela do framework.
7. **Learn more** — link da product page + Instagram da marca.

**Curadoria por creator (o ajuste que multiplica o acerto):** creators escolhem o primeiro conceito da lista ou o mais fácil (first-pick bias). Não mande o mesmo doc pra todos — faça uma cópia por creator e deixe só os **4-6 concepts que combinam com o perfil e o conteúdo existente daquele creator** (olhe o perfil antes e pergunte: "qual vídeo seria bom PARA ELE?"). Periodicamente, "dealer's choice": deixe o creator inventar — às vezes é o que gera o winner.

A skill gera um framework por creator contratado em `briefs/framework-[creator-slug].md` (inglês), usando o gerador de brief da base (Creator Brief Generator / UGC Brief Prompt) alimentado com: research da 02, conceito(s) escolhido(s), e as perguntas sobre o creator (sexo, idade, etnia, estilo de filmagem) — o script/hook é escrito pra pessoa que vai gravar.

### ETAPA 6 — [Fase A] Follow-up, coleta e o corte em 3 hooks

**Cadência:** produto marcado como enviado → avise o creator ("chega em 3-7 dias; me avisa ao receber"). Depois da confirmação de recebimento, **follow-up a cada ~3 dias** (com folga em fim de semana); **nunca passe de 7 dias sem contato**. Perguntas típicas: "did you receive it?", "how's the content coming along?". Creators são pessoas, não robôs — firme e humano. Qualidade fraca: dá pra pedir ajuste com jeito, calibrando a expectativa ("this is free content").

**Coleta:** ao receber, baixe TUDO ("the more content the merrier" — com e sem áudio, fotos, link do post se postou) → Drive → pasta com o nome do creator. Só marque o deal como completo com o conteúdo salvo. Creators excepcionais (entregam em dias, avisam proativamente) → marque como favoritos: são os candidatos naturais a embaixador.

**Marcação de corte:** pra cada entrega, avalie "dá pra cortar em 3 variações e rodar como ad?" → marque `dct_ready: true` (o padrão da casa: **cada vídeo cortado em 3 versões começando em 3 pontos diferentes = 3 hooks**) ou `false` se inutilizável — arquive mesmo assim ("who knows, maybe it would convert"). O conteúdo aprovado entra no inventário que a 08 lê (`content[]` no `dados.json`) — a 08 decide o empacotamento e a 10 sobe.

**Expectativa de acerto (números da fonte — calibram a paciência, não substituem os do membro):**

- Hit rate (taxa de acerto) de UGC de creators: **~14%** vs **~4%** dos ads produzidos pelo time interno — com custo de operação ~US$ 6k/mês vs ~US$ 40k/mês.
- Conteúdo cru: **~15%** de acerto vs **~5%** do conteúdo editado/polido (3x, por autenticidade).
- Win rate acima de volume, sempre: 20% de acerto em 30 criativos/mês = 6 winners; 1% em 100 = 1. **Volume desestruturado (Shotgun) só é legítimo dentro deste pipeline de creators** (cânone ad-taxonomy §7) — como estratégia criativa deliberada, mata o hit rate.
- Escala do motor: 10 creators fazendo 1-2 vídeos/semana, cortados em 3 = **~130-260 ads extras/mês**; a fonte sustenta marca a US$ 25k/dia assim, e cita marca a US$ 150k/dia com 3x+ ROAS rodando SÓ com volume de creators, sem creative strategy formal.
- O funil típico não é "winner de primeira": o creator faz um vídeo BOM → é contratado → e o SEGUNDO vídeo, já com feedback, vira o super winner.

**Auditoria de ROI (mensal/trimestral):** "gastamos US$ X em conteúdo de creators → quantos winning ads saíram → quanto spend eles sustentaram". Grave em `economics.roi_audit` — é o número que justifica (ou corta) o budget de conteúdo.

### ETAPA 7 — [Fase A] Pipeline TikTok Shop: a fábrica de volume

Opcional — roda pra quem já opera TikTok Shop ou quer o canal COMO FONTE DE CONTEÚDO. A decisão de abrir marketplace como canal de VENDA é outra conversa (regra de entrada própria — skill 20-marketplace-engine).

**O reframe da fonte: o valor do TikTok Shop não é a receita da plataforma — é ser PAGO para gerar conteúdo.** Caso citado: um operador gerou 600 vídeos num mês pra uma marca (faturando ~US$ 250-300k no canal) e passou a reutilizar o acervo como criativo de paid ads. "Most people spend money to get content; you make money to get content."

- **Operação base:** envio de samples (amostras) pra creators do canal, gestão dos afiliados, comissão definida (dois níveis — orgânica vs de ads; a régua vive na 20), e o fluxo de conteúdo que sustenta as vendas — cada afiliado postando é conteúdo novo que pode virar ad.
- **Leitura aditiva da 20 (se `20-marketplace-engine/dados.json` existir):** `channels[tiktok_shop].commission_organic_pct`, `samples_policy` e a meta de GMV definidos lá são os números que este pipeline usa — a decisão de abrir/manter o canal de venda continua na 20; aqui nada se redecide.
- **Variação agressiva da fonte:** contas TikTok dedicadas à marca (caso: 20), cada uma tocada por um creator 100% comissionado (**40-50% de comissão**), produzindo volume diário reutilizado nos paid ads; contas chegam a 20k seguidores em ~6 meses. Comissão agressiva força volume — e o conteúdo vale mais que a margem cedida.
- **Mineração de virais (DailyVirals):** os virais do dia do TikTok/TikTok Shop viram swipe file de UGC — sandbox de breakdowns, transcript downloader (cole a URL, receba o texto), análise por AI do vídeo linha a linha, e o AB compare (viral original vs seu remake, frame a frame, pra diagnosticar por que o seu flopou). O fluxo: transcript do viral → reescrever adaptado ao produto → virar concept no framework do creator (ETAPA 5). Remake próprio, nunca o vídeo alheio no ar (regra 5).
- **Influencer grande é jogada de marca, não de performance** — a fonte viu post de celebridade funcionar como whitelisted ad num caso e flopar como ad noutro. O motor daqui é micro/médio creator em volume.

## FASE B — Performance Program

**Gate:** ≥ 1 `breakthrough` em `manifest.ad_classification[]` (cânone §2 — KPI do ad melhor que o da campanha E puxando spend). `kpi_winner` não abre o gate; `spend_winner` também não (vira candidato a observação, não a contrato).

### ETAPA 8 — [Fase B] Identificar os winning creators

**Definição da fonte: winning creator = creator cujo ad ganhou spend e escalou.** "Good is something that gets spend." O contraste que calibra: creator A → ad com US$ 60k de spend a 2x ROAS (contrata); creator B, de conteúdo "mais bonito" → US$ 66 de spend (não contrata). Zero sentimentalismo estético.

Operacional:

1. **Convenção de nome:** todo ad montado com conteúdo de creator carrega o nome do creator no nome do ad. É o que permite filtrar por creator no Ads Manager e nas ferramentas de report (custom report com "ad name contains {creator}"). Sem isso, não existe atribuição por creator — defina a convenção AGORA e registre em `handoff.for_skill_10`.
2. Cruze `manifest.ad_classification[]` com o mapa creator→ads do roster: creator com breakthrough → candidato a contrato (ETAPA 9); creator com `spend_winner` → observação (o ad entra em iteração pela 14/08; o creator fica na fila); resto → continua no ciclo de seeding.
3. Meça por janelas de 90 dias por creator (ex. da fonte: US$ 26k de spend → ~US$ 93-100k gerados pelo conteúdo de uma creator de US$ 500/mês).

### ETAPA 9 — [Fase B] Contrato recorrente: retainer e a escada de embaixador

Dois modelos, por e-mail/mensagem (inglês; templates em `outreach/messages.md`):

**Modelo 1 — Retainer simples:** 1 vídeo/semana com os produtos + produtos de graça + **US$ 500/mês** (o número "simples que todo mundo aceita"; alternativa: pergunte o rate do creator primeiro — às vezes pedem menos) + convite pro canal de comunicação (Discord/Slack). Negociação é esperada (US$ 500 → US$ 750): encontre o meio-termo.

**Modelo 2 — Brand Ambassador + Performance Program:** produto grátis + base US$ 500/mês (1 vídeo/semana) + **SE o creator topar 2-3 vídeos/semana**, entra no programa de performance (a **regra do 2-3**: o programa existe pra DOBRAR/TRIPLICAR o output; quem faz 1/semana fica no retainer simples):

| Degrau | Comissão | Acumulado no exemplo |
|---|---|---|
| Primeiros US$ 10.000 | **10%** | US$ 1.000 |
| Próximos US$ 20.000 | **5%** | US$ 2.000 |
| Próximos US$ 40.000 | **2,5%** | US$ 3.000 |
| Acima de US$ 70.000 | **1%** | — |

- **Teto de payout: US$ 10.000/mês.** Apuração por mês-calendário, somando todos os vídeos do creator, com reset todo mês. Nunca comissão flat pra sempre — o degrau decrescente alinha incentivo sem corroer margem na escala (variante da fonte pra teto menor: 10% só dos primeiros US$ 5k, se o máximo desejado é US$ 500).
- **Base de cálculo: % de REVENUE ou % de AD SPEND** — troque a palavra no e-mail; a fonte split-testa os dois. Exemplos prontos no pitch fazem a conta pelo creator (vídeo gera US$ 70k → US$ 3.500 no total com a base; US$ 100k → US$ 3.800).
- **Alternativa por cupom:** código próprio do creator no ad (ex.: 20% total = 10% de desconto pro cliente + 10% pro creator), com pagamento automático via app de afiliados no Shopify — a fonte split-testa contra o modelo de %.
- **Fricção zero no pitch:** o creator NÃO precisa postar no próprio perfil — só filmar e subir no Drive (remove a maior objeção); e recebe os breakdowns dos winning ads da marca ("so you know the perfect formula").
- Pagamentos nos dias **1 e 15**; planilha de retainer (creator, nº do payout, mês, datas, valor, status) — a skill gera `roster.csv` com essas colunas.

**Incentivo alinhado é o motor:** o creator ganha quando o ad DELE escala — a qualidade sobe sem gestão.

### ETAPA 10 — [Fase B] Onboarding e comunicação contínua

1. **Onboarding deck** (boas-vindas ao time, expectativa de entrega, agenda de pagamento, report mensal no último dia do mês, como funciona o feedback, quem é o contato, a fórmula do vídeo vencedor, "always have new ideas to film").
2. **Contrato** — gere o draft congruente com o e-mail aceito, em 3 variantes: **% de AD SPEND**, **% de REVENUE**, **AD SPEND + WHITELISTING**. Cláusulas ensinadas pela fonte: mínimo 2 vídeos/semana (no performance); produtos de uso exclusivo pro conteúdo (devolução/reembolso em 14 dias se não entregar); base US$ 500/mês em 2 parcelas (dias 1 e 15); os degraus e o teto idênticos ao e-mail; confidencialidade; **propriedade total do conteúdo pela marca** (uso, modificação e distribuição em todos os canais — é isso que licencia o conteúdo pros ads); independent contractor; month-to-month com rescisão em 14 dias de aviso; na variante whitelisting, a concessão de acesso às páginas. **Com o aviso obrigatório: referência, não aconselhamento jurídico — revisar com advogado** (regra 4).
3. **Mensagem de kickoff** (inglês): breakdown atual dos winning ads + framework com os concepts novos + link do Drive + expectativa de entrega + agenda de pagamento e report.
4. **Comunicação contínua:** canal por creator (ou grupo) no Discord/Slack. Usos típicos: avisar promo com 7-10 dias de antecedência ("consegue incluir no conteúdo da semana?"); lançar ideia com direcionamento de avatar; creator forte recebe só a ideia e roda ("you wouldn't have hired them if they didn't know how to create" — microgerenciar mata o motivo de ter creators); creator que rende melhor com direção recebe guidance. Continue enviando produto novo (tamanhos, lançamentos) — logística faz parte da relação. A fonte chama esse canal de uma das melhores otimizações de ROI do programa.

### ETAPA 11 — [Fase B] Feedback loop e report mensal por creator

O erro comum é pedir conteúdo sem nunca dizer ao creator o que funcionou — e o que viraliza no perfil dele muitas vezes NÃO é o que performa como ad. O loop devolve ao creator o "cérebro de marketing" da marca:

1. **Report por creator:** custom report filtrando "ad name contains {creator}" (Atria é a ferramenta da fonte; um report em Slides/Canva com os números do Ads Manager cumpre o papel) + Loom comentando, ou o board compartilhado.
2. **Métricas que o creator vê:** thumb stop ratio (referências da fonte: **18-21% é fraco; 42-48% é ótimo**), hold rate, CTR, engajamento (shares = identificação), average play time, e a favorita da fonte: **% dos views de 3s que chegaram a 15s** (dos que pararam, quantos seguiram assistindo).
3. **Regra de transparência (regra 3):** retainer simples → esconda spend em dinheiro, receita e ROAS (mostre soft metrics); performance → números abertos.
4. **Comentários dos ads viram ideia:** puxe os comments do Meta e compartilhe ("vários comentários 'meu marido comprou pra mim' → novo vídeo: gifts my husband got me that I actually love") — 3 ideias prontas sem escrever roteiro nenhum.
5. **Report mensal pra TODOS os creators:** top 5 winning ads do mês + POR QUE venceram + ideias pro mês. Elogie o que performa e direcione ("thumbstop ótimo, hold fraco — mantenha o suspense; este está a 6x há 30 dias, faça mais como este testando outra abordagem"). É o mesmo processo de learnings da 11, aplicado à pessoa que produz. Quando a 14 gerar `creator-report.md` de um breakthrough, distribua por aqui.

### ETAPA 12 — [Fase B] Whitelisting

**Whitelisting** = rodar o ad a partir do perfil do creator em vez da página da marca — o ad parece vir de uma pessoa real. Prova da fonte: mesmo criativo, versão whitelisted sustentou mais spend com CPA/ROAS melhores que a versão na página da marca (e houve caso em que não superou — é empurrão de performance, não salvação de conta).

**As 6 regras da fonte:**

1. **Só whitelist creator que já tem winning ad com a marca.** Não use pra "achar" winner.
2. **Só os ads DAQUELE creator na página dele.** Rodar criativo alheio na página de um creator é o jeito mais rápido de perder o acesso.
3. **Preço:** muitos creators nem sabem o que é — dá pra conseguir por **US$ 0** embutindo no agreement (a variante AD SPEND + WHITELISTING da ETAPA 10, ou a screening question da ETAPA 2 que já combinou isso no dia 1). Se cobrar: **US$ 100-250/mês no máximo** (US$ 250 já é teto; US$ 1.200/mês, recuse). Rota alternativa: onboard primeiro, um mês bom, aí pergunte. Referência de mercado pra comprar post de creator estabelecido (fora do pipeline próprio): US$ 500-2.000/post — por isso o pipeline próprio é a vantagem.
4. **Risco de over-leverage:** se o top ad da conta é whitelisted e o creator revoga o acesso (ou pede aumento), a marca fica refém. Teste em separado e só "goteje" whitelisted ad entre os campeões com creators de alta confiança.
5. **Agreement assinado sempre** (a variante de contrato já cobre; considere non-compete leve — mesmo produto de outra marca com o mesmo creator confunde o público).
6. **Avise o creator:** comentários, follows e visitas de perfil acontecem na página DELE. E a marca perde esses cliques pro próprio Instagram — se construir o perfil da marca importa agora, não migre tudo.

**Setup de acesso:** ferramenta de concessão em 3 cliques (Leasy, ~US$ 99/mês, trial de 14 dias sem cartão — com 1-2 creators, conclua no trial e pause): conecte o portfólio de negócios, crie o custom request de whitelisting, envie o link ao creator. Creator de Instagram sem página no Facebook: peça pra criar uma. No Ads Manager, monte o ad selecionando página e Instagram do creator. **Copy da primary text como se fosse o creator falando — ou melhor, peça pro próprio creator reescrever a copy do jeito dele.**

**Onde testar:** os whitelisted ads começam DENTRO da campanha principal — abaixo de ~US$ 2k/dia de spend é a única casa deles ("você precisa de toda performance possível"; a raw content campaign nem existe nessa faixa). Campanha PRÓPRIA de whitelisting (funciona como segunda raw content campaign, pra ler o efeito isolado) é jogada de camada alta — a régua de quando cada camada entra é a dos níveis de escala da ETAPA 14 desta skill. Depois de provado o efeito, dá pra fundir, mantendo o cuidado da regra 4. **Quem executa a campanha é a 10/12** — esta skill entrega os acessos e a lista de ads elegíveis por creator.

**Variante da fonte high-ticket:** páginas de nicho spin-off (perfis temáticos fora da conta principal) pra veicular criativos sem carimbo da marca — mesma lógica de camuflagem, mesma regra de agreement.

**Espionagem (com a 03):** na Facebook Ads Library, busque os TERMOS que um concorrente usa (não a página dele) — aparecem as whitelisted pages e os perfis de creators rodando pra ele. Serve pros dois lados: mapear o ecossistema do concorrente e achar creators que já fazem whitelisting pra outras marcas (mais fáceis de fechar).

### ETAPA 13 — [Fase B] Partnership Ads

**Partnership ads** = formato nativo do Meta que mostra marca + creator juntos, com selo de parceria (diferente do whitelisting, que mostra só o perfil do creator). A fonte migrou a prioridade pra cá: o Meta está favorecendo o formato no leilão.

1. No ad: ative partnership ads → página da marca + o creator parceiro.
2. **Dynamic identity** ligado (o Meta alterna a identidade exibida; entrega ~1,3% mais barata) em vez de travar uma das duas.
3. Onde rodar: raw content campaign ou campanha principal — ambos funcionam (decisão da 10/12).
4. **Pitch pra creator NOVO (não só winners):** peça acesso de partnership por **30 dias**, enquadrado como benefício DELE — "o Meta está empurrando partnership ads; com o acesso, o SEU ad tem mais chance de vencer na conta — e quem vence tem chance de retainer de longo prazo". **Timing do pitch:** "já no primeiro contato" vale só pra creator recrutado na Fase B (com o gate aberto); pra creator que veio do seeding da Fase A, o pitch entra no momento do upgrade pra winning creator (ETAPAs 8-9). Remova o acesso após 30 dias se não evoluir. (É o único formato em que acesso antes de winner se justifica — o custo é zero e o teste beneficia os dois.)
5. Com ambassadors existentes: teste partnership em todos os top criativos deles. Continue testando whitelisting em paralelo.

### ETAPA 14 — [Fase B] Raw content campaign, creator farming e recrutamento contínuo

**Raw content campaign** — a campanha separada de conteúdo cru (sem edição, sem caption, sem música) que existe pra: (a) learnings limpos (conteúdo cru é imprevisível — "wacky social media stuff" que funciona sem você saber por quê); (b) forçar spend pra TESTAR CREATORS; (c) não poluir os dados da campanha principal de alta intenção. Formato clássico: 1 ad set = 1 vídeo cortado de 3 formas (os 3 hooks da ETAPA 6); atualização 2026 da fonte: um único ad set com flexible ads (3-6 visuais + 2 copies + 2 headlines + 1 LP), escalando no nível do ad. **Entra no nível 2 de escala (US$ 3-10k/dia de spend)** — antes disso, só a campanha principal; whitelisting como camada estrutural entra no nível 3 (US$ 10-50k+/dia). Creator que performa aqui → contrato (ETAPA 9). **Montagem e budget: 10/12.** Esta skill mantém o inventário de conteúdo cru elegível (`content[]` com `dct_ready`) e o mapa creator→vídeo.

**Creator farming** — cultivar a base de creators ANTES de precisar dela: o ciclo de seeding da Fase A nunca para de rodar em volume baixo, mesmo com o roster cheio. Quando uma campanha exigir volume novo, existe gente pronta pra gravar — sem os ~26 dias de fila.

**Recrutamento pago de afiliados** — usar tráfego pago pra recrutar creators/afiliados em vez de compradores: ad com chamada tipo "save 40% on your first order when you apply to be a brand ambassador" → formulário → código de desconto → primeira compra. A fonte roda esses ads com os perfis whitelisted dos melhores creators contando a própria história e opera **lucrativo na aquisição de afiliados** (o candidato também compra); caso citado: marca que não destravava ads de venda direta (0,2x) rodava recrutamento a 2,5x. Cliente que amou o produto é candidato natural — a fonte manda procurar o creator que teve transformação real com o produto.

**Atribuição e pagamento em escala:** custom link por afiliado (cada venda atribuída ao creator que originou — paga a comissão certa e compara desempenho entre parceiros); programa automatizado quando o volume de parceiros crescer (a fonte cita Social Snowball — apuração de comissão por cliente — e a alternativa com payouts automáticos e programas diferentes por link, grátis + ~1,5% de taxa).

**Ad Bounties (bounty EXTERNO — opera aqui):** pagar creators/editores DE FORA por performance — % da receita do ad enquanto ele rodar, brief aberto, volume "infinito" sem custo fixo (só paga se performar; a fonte gastou ~US$ 20k num mês em bounties no beta). A operação é desta skill: cada participante entra no `roster[]` com `tier: "bounty"`; a % e o teto seguem o default da fonte quando ela os cita — senão vêm do membro (regra 6); e todo ad montado com conteúdo dele segue a MESMA convenção de nome da ETAPA 8 (sem isso não há apuração por bounty). O que fica na **skill 18-team-engine**: o prêmio por performance pago a editor CONTRATADO do time (incentivo interno) e a mecânica de recrutar via comunidade da marca — use-a pra encher este funil.

### ETAPA 15 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Nenhum material de creator (brief, mensagem, contrato, report) em português — tudo inglês US.
2. Fase B só rodou com `breakthrough` confirmado no manifest; nenhuma etapa 8-14 aparece no relatório de uma rodada Fase A.
3. Nenhum creator marcado pra whitelisting sem breakthrough próprio; nenhum ad de um creator agendado pra página de outro (exceção única: o acesso de partnership de 30 dias da ETAPA 13, que não é whitelisting).
4. `report_visibility` é `spend_only` pra todo creator de retainer simples e `full` só pra performance.
5. Todo contrato gerado carrega o aviso de referência jurídica.
6. Nenhum valor de remuneração fora dos defaults da fonte sem ter vindo do membro; nenhum tier inventado.
7. Todo creator `hired` tem endereço confirmado e produto escolhido POR ELE registrado.
8. Todo brief tem ≤ 9 concepts e a curadoria por creator registrada (`curated: true` com a lista do que ficou).
9. A convenção de nome com o creator está definida e gravada em `handoff.for_skill_10` antes de qualquer conteúdo ir pra ad.
10. Nenhum conteúdo de terceiro (rip/borrowed) marcado como `dct_ready` — só referência de estrutura.
11. A matriz sub-avatar × creator aparece no relatório com as lacunas visíveis (célula vazia = casting que falta).
12. O relatório contém só o resultado — sem narração de processo, sem descrição de ausências (rule `report-only-results.md`).

## Output Schema — `16-creator-engine/creator-engine.md` + `16-creator-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills 08, 10, 11, 12 e 14.

```json
{
  "creator_engine_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "phase": "A_content | B_performance",
  "phase_reason": "sem breakthrough em manifest.ad_classification",
  "objective": "find_brand_ambassador",
  "operator": "member | va | other",
  "channels": {
    "platform": { "name": "insense | other | none", "brand_added": false, "license_active": false },
    "manual_outreach": false,
    "film_yourself": false,
    "tiktok_shop": { "active": false, "affiliates_count": null, "commission_pct": null, "commission_note": "dois níveis (orgânica vs ads) — a régua vive na 20", "dedicated_accounts": null }
  },
  "seeding_campaigns": [
    {
      "campaign_id": "seed-01",
      "type": "seeding | paid_per_video",
      "sub_avatar_target": "<id do sub_avatar da 02>",
      "pay_per_video_usd": null,
      "retail_value_check_passed": true,
      "screening_questions": ["..."],
      "status": "draft | live | closed",
      "applications_count": null
    }
  ],
  "roster": [
    {
      "creator_id": "slug-do-creator",
      "name": "",
      "handle": "",
      "platform": "instagram | tiktok | facebook",
      "source": "seeding | paid_campaign | manual_outreach | tiktok_shop | recruitment_ad | member_network",
      "sub_avatar_match": "<id>",
      "diversity_axes": { "age_band": "", "ethnicity": "", "gender": "", "language": "en", "physical_note": "", "psychographic_note": "" },
      "status": "applied | shortlisted | approved | hired | product_sent | filming | content_received | complete | dropped",
      "tier": "seeding | paid_per_video | retainer | ambassador_performance | bounty",
      "rate_per_video_usd": null,
      "retainer_monthly_usd": null,
      "videos_per_week_due": null,
      "performance_terms": {
        "basis": "ad_spend | revenue | coupon",
        "tiers": [ { "band_usd": 10000, "pct": 10 }, { "band_usd": 20000, "pct": 5 }, { "band_usd": 40000, "pct": 2.5 }, { "band_usd": null, "pct": 1 } ],
        "cap_monthly_usd": 10000,
        "coupon_code": null
      },
      "whitelisting": { "eligible": false, "access_granted": false, "access_via": "leasy | manual | none", "monthly_fee_usd": 0 },
      "partnership_access": { "granted": false, "expires_at": null },
      "contract": { "variant": "ad_spend | revenue | ad_spend_whitelisting | none", "signed_at": null, "legal_disclaimer_included": true },
      "report_visibility": "spend_only | full",
      "favorite": false,
      "shipping": { "address_confirmed": false, "product_chosen_by_creator": null, "sent_at": null, "delivered_at": null },
      "notes": ""
    }
  ],
  "briefs": [
    {
      "brief_id": "framework-creator-slug",
      "creator_id": "slug-do-creator",
      "path": "briefs/framework-creator-slug.md",
      "concepts_total": 6,
      "curated": true,
      "concepts_from_08": ["c01", "c03"],
      "angles_from_02": ["sub_avatar_2.angle"],
      "sent_at": null
    }
  ],
  "content": [
    {
      "content_id": "creator-slug-001",
      "creator_id": "slug-do-creator",
      "received_at": null,
      "files_count": 0,
      "dct_ready": false,
      "cut_hooks_timestamps": [],
      "license_source": "contract | platform_terms | none",
      "used_in": { "batch_08": null, "raw_content_campaign": false, "whitelisted": false, "partnership": false }
    }
  ],
  "performance_by_creator": [
    {
      "creator_id": "slug-do-creator",
      "ad_naming_pattern": "contains: <creator-name>",
      "ads": ["ad-id-1"],
      "classes_from_11": { "breakthrough": 0, "spend_winner": 0, "kpi_winner": 0, "loser": 0 },
      "spend_90d_usd": null,
      "soft_metrics": { "thumb_stop_pct": null, "hold_pct": null, "pct_3s_to_15s": null },
      "last_report_at": null,
      "winning_creator": false
    }
  ],
  "economics": {
    "monthly_content_budget_usd": null,
    "creative_production_pct_of_ad_spend": null,
    "hit_rate_reference": { "creators_pct": 14, "internal_pct": 4, "raw_pct": 15, "edited_pct": 5 },
    "roi_audit": { "period": null, "spent_on_creators_usd": null, "winning_ads_count": null, "spend_sustained_usd": null }
  },
  "recruitment": {
    "farming_active": false,
    "paid_recruitment_ads": { "active": false, "hook": "apply to be a brand ambassador", "profitable": null },
    "affiliate_attribution": { "custom_links": false, "app": null }
  },
  "pending_inputs": [],
  "handoff": {
    "for_skill_08": ["content[] com dct_ready=true (matéria-prima licenciada de batch)", "roster[].tier (archetype creator_human disponível)", "briefs[] (concepts já em produção com creators — não duplicar no batch)"],
    "for_skill_10": ["ad_naming_pattern por creator (convenção obrigatória)", "roster[].whitelisting.access_granted (identidades disponíveis)", "roster[].partnership_access", "content[] elegível pra raw content campaign"],
    "for_skill_11": ["performance_by_creator[].ad_naming_pattern (pra atribuir classes por creator)"],
    "for_skill_12": ["roster count por tier vs tabela de creators em retainer da ETAPA 8 da 12", "channels.tiktok_shop (fonte incremental de conteúdo)"],
    "for_skill_14": ["roster[] + report_visibility (distribuição do creator-report do Movimento 6)"]
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo são ILUSTRATIVOS** — os tiers gravados são os defaults da fonte e só valem enquanto o membro não definir os dele. Campo desconhecido fica `null` e entra em `pending_inputs[]` — nunca preenchido com plausível.

## Contrato de leitura (quem lê o quê)

**Quem já lê hoje:**

| Skill | Campo que já lê | O que muda |
|---|---|---|
| **11** ad-analysis | `performance_by_creator[].ad_naming_pattern` (o nome do creator no nome do ad) | A análise agrupa por creator e devolve quem venceu (fecha o loop da ETAPA 8) |

**Disponível para (leitura aditiva)** — dados publicados que as skills podem puxar quando fizer sentido, sem que já leiam hoje:

| Skill | Campo disponível | O que permite |
|---|---|---|
| **08** creative-engine | `content[].dct_ready`, `roster[].tier`, `briefs[]` | A rota B (montagem) ganha footage licenciado real do roster; o archetype `creator_human` deixa de ser "raro" quando há creator contratado; o batch não duplica concept que já está com creator |
| **10** ad-strategy | `handoff.for_skill_10` (naming, acessos, conteúdo cru) | Ads de creator sobem com o nome do creator no nome do ad; whitelisting/partnership viram opções de identidade na montagem; raw content campaign tem inventário |
| **12** scale-engine | `roster` por tier, `channels.tiktok_shop` | A coluna "Creators em retainer" da tabela de sub-fases ganha fonte real; o nível de escala consulta se há conteúdo/acessos pra abrir raw content (L2) e whitelisting (L3) |
| **14** content-recycler | `roster[]`, `report_visibility` | O creator-report do Movimento 6 sabe pra quem ir e com quais números visíveis |

Quando `16-creator-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — a leitura é aditiva, nunca pré-requisito.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/16-creator-engine/` antes de salvar.

Outputs em `workspace/[produto]/16-creator-engine/`:

- **`creator-engine.md`** contendo, nesta ordem: objetivo da fase e rota escolhida; a matriz sub-avatar × creator com as lacunas; o estado do funil de seeding (campanhas, aplicações, shortlist); os briefs enviados e o inventário de conteúdo com marcação de corte; a expectativa de acerto com os números de referência; **[Fase B]** winning creators identificados, contratos e escada, estado de whitelisting/partnership por creator, e o plano de recrutamento contínuo; pendências (o que falta e o que destrava, sem narrar tentativas).
- **`creator-engine.html`** — visualização humana usando `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto). Componentes: `kpi-grid` pros números do funil, `table-wrap` pra matriz e roster, `callout` pras regras de whitelisting, `danger` pro risco de over-leverage.
- **`dados.json`** — schema acima.
- **`briefs/framework-[creator-slug].md`** — o framework curado de cada creator (inglês US).
- **`outreach/messages.md`** — templates das mensagens (shortlist, hire, envio, oferta de retainer, oferta de ambassador, kickoff), em inglês US.
- **`contracts/ambassador-agreement-[variant].md`** — drafts das 3 variantes com o aviso jurídico (inglês US).
- **`roster.csv`** — a planilha de gestão (colunas: creator, handle, status, tier, rate, vídeos/semana, whitelisting, contrato, payout 1/15, e-mail).

**Distinção importante (mesma da 13):** briefs, mensagens, contratos e `roster.csv` são material operacional voltado ao creator — **não geram `.html`**, não usam o design-system Aura e ficam em inglês. Só o relatório interno (`creator-engine.md`/`.html`) segue a rule 6b e o `report_language`.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:

- Adicionar `16-creator-engine` em `skills_completed` (na primeira fase concluída; sem duplicar)
- **Bloco `creator` (contrato de fase — espelha o padrão do bloco `retention` da 13):**

```json
{
  "creator": {
    "phase_a_done": true,
    "phase_b_done": false,
    "roster_count": 0,
    "ambassadors_count": 0,
    "whitelisting_active": false,
    "ad_naming_pattern": "contains creator name",
    "checked_at": "2026-09-01T00:00:00Z"
  }
}
```

- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `ABRIR-AQUI.html`, onde `<slug>` é o `product_slug`)

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`).

**Fase A:**
"Content Engine montado. Rota: [seeding grátis / campanha paga a US$ 100-150 por vídeo / outreach manual / filmar você mesmo]. Campanha de seeding pronta pra [N] creators mirando [sub-avatares], com as screening questions configuradas — inclusive a de whitelisting, que já deixa o acesso combinado desde o dia 1.
[N] frameworks de brief curados por creator estão em `briefs/` — revisa o bloco de Hooks & Ideas antes de enviar (é onde o marketing acontece).
Expectativa honesta: o objetivo é conhecer creators até achar UM embaixador que produza toda semana — winning ad de primeira é bônus. Do hire ao conteúdo virar ad passam ~26 dias, então o funil começa agora e roda em paralelo com os criativos da 08.
Follow-up a cada 3 dias depois que o produto chegar; conteúdo recebido eu marco pra corte em 3 hooks e entrego pro batch da 08. Quando a análise de ads (11) confirmar o primeiro breakthrough de creator, me chama com 'creators' de novo — aí abre a Fase B: contrato recorrente, escada de comissão e whitelisting."

**Fase B:**
"Performance Program ativo. [N] winning creator(s) identificado(s) pela classificação da 11: [nomes]. Pra cada um: [oferta de retainer US$ 500/mês / escada de embaixador com a regra do 2-3] — os e-mails de oferta estão em `outreach/messages.md` e os contratos (com aviso jurídico) em `contracts/`.
Whitelisting: [N] creator(s) elegível(is) — as 6 regras estão no relatório; a que não se negocia: só ads do próprio creator na página dele, e nunca deixar o top ad da conta dependente de acesso de terceiro.
Partnership ads: pitch de 30 dias pronto pros creators novos.
A 10/12 montam as campanhas com os acessos e o inventário daqui; todo ad de creator sobe com o nome do creator no nome do ad — sem isso não existe report por creator.
Report mensal por creator no último dia do mês (retainer simples vê soft metrics; performance vê os números). Revisa as ofertas e me diz o que ajustar antes de enviar."

**Se o membro pediu Fase B sem breakthrough:**
"O programa de performance amplifica vencedor confirmado — e ainda não há breakthrough na análise de ads. O que destrava: rodar a Fase A (seeding + briefs) pra gerar conteúdo de creator, subir com a 08/10, e deixar a 11 apontar o primeiro breakthrough. Quer que eu monte a Fase A agora?"
