---
name: creator-engine
description: Engine de creators da marca, a operação de conteúdo humano como motor de escala, em duas fases. Fase A, Content Engine (paralela à creative-engine, pode começar antes do launch), monta o funil de product seeding em plataforma tipo Insense ou por outreach manual, o casting com diversidade amarrada aos sub-avatares da market-research, o framework de brief (nunca script fechado), o follow-up e a coleta, o corte de cada vídeo em 3 hooks e o pipeline TikTok Shop como fábrica de volume, tudo pra achar um brand ambassador. Fase B, Performance Program (só depois de breakthrough confirmado pela ad-analysis), sobe o creator vencedor pra contrato recorrente, escada de embaixador com comissão em degraus, whitelisting, partnership ads, raw content campaign, creator farming e recrutamento pago de afiliados. A creative-engine continua dona do que dizer; esta skill é dona de quem grava e da relação com quem grava. Use quando o membro disser "creators", "ugc", "seeding", "influencer", "whitelisting", "ambassador", "insense", "conteúdo de creator".
---

# Creator Engine · Lateral · apelido antigo: 16 <!-- gen:title -->

## Quando usar

Content é o arquivo bruto; creative é o content editado; sem abundância de conteúdo não há volume de teste nem winning ad. Fase A, Content Engine: monta o funil de conteúdo humano a custo perto de zero pra encontrar um brand ambassador; do hire ao ad no ar passam cerca de 26 dias, então começa cedo. Fase B, Performance Program: só depois de breakthrough confirmado o creator vencedor sobe de degrau; whitelisting amplifica o que já venceu, nunca procura vencedor. Divisão de donos em `reference/contexto.md`: a `creative-engine` decide o que o ad diz, a `ad-strategy` e a `scale-engine` montam campanha e budget, a `ad-analysis` classifica; esta skill é dona do roster, do seeding, dos briefs, dos contratos, da escada e do whitelisting como relação. Cânone `.claude/lib/ad-taxonomy/README.md`: só `breakthrough` abre a Fase B.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. `workspace/[produto]/manifest.json` existe. Fase pelos dados: Fase A enquanto `manifest.creator.phase_a_done` não é `true` e enquanto não há breakthrough (ciclo contínuo); Fase B só com ao menos um `class: "breakthrough"` em `manifest.ad_classification[]`; pedido de whitelisting ou ambassador sem breakthrough recebe a explicação e a oferta de rodar a Fase A.
2. `market-research/dados.json` (`core_avatar`, `sub_avatars[]` com `angle`) e `offer-builder/dados.json` (`pricing.aov_expected`, valor de varejo e margem); faltando, escape ES1.
3. Fase A: `page-build` em `skills_completed` é o ideal; sem loja, o outreach manual anda. Fase B: `ad-analysis/dados.json`, `manifest.ad_classification[]` e os ads de creator identificáveis pela convenção de nome.
4. Rodadas anteriores em `creator-engine/`: o roster continua de onde parou.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`) no relatório e na conversa; todo material que vai pro creator (brief, outreach, contrato, report) fica sempre em inglês US.
2. `profile.md` (starter e validating com seeding grátis e filmar você mesmo, nunca creator pago; scaling com campanha paga, retainers e a Fase B), `creative-engine/dados.json` se existir, `ad-analysis/dados.json` e `NEXT_BATCH_IDEAS.md` na Fase B, `scale-engine/dados.json` e `content-recycler/`.
3. As sete regras que não se negociam, em `reference/regras-e-sistemas.md`: material de creator em inglês; whitelisting só de creator com breakthrough próprio e só com os ads dele; transparência por tier; contrato é referência, não aconselhamento jurídico; conteúdo de terceiro sem licença não vai ao ar; remuneração nunca inventada; campanha é território da `ad-strategy` e da `scale-engine`.
4. Base pelo índice: `python3 .claude/lib/kb-index/kb_lookup.py --skill creator-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa (as queries embutidas na etapa são piso obrigatório, rodam sempre e não contam no teto); o mínimo da Fase A e o adicional da Fase B estão em `reference/regras-e-sistemas.md`; nunca query genérica nem busca repetida.

## Fluxo da skill

ETAPA 1 roda sempre; ETAPAs 2 a 7 são da Fase A; ETAPAs 8 a 14 são da Fase B e são puladas em silêncio sem breakthrough (sem seção vazia no relatório); ETAPA 15 roda sempre.

### ETAPA 1 · Detectar a fase e inventariar o que já existe

Leia `reference/fase-e-inventario.md`. Grave `phase` e `phase_reason`; pré-popule tudo dos artefatos e peça numa única mensagem só o que não vive em arquivo: budget mensal de conteúdo (com as referências da fonte), o que o membro já tem (creators, conteúdo parado, plataforma, TikTok Shop) e quem opera o dia a dia. Escreva no relatório o objetivo da Fase A: um brand ambassador.

### ETAPA 2 · [Fase A] Canal de seeding e a campanha

Leia `reference/seeding.md`. Cascata de canal: plataforma de creators, outreach manual (custo zero, a rota sem site), filmar você mesmo. Viabilidade pelo valor de varejo (cerca de 30 dólares ou mais). Setup da campanha de seeding pelo SOP, com as screening questions (a de whitelisting já no dia 1) e uma campanha por sub-avatar. Campanha paga por vídeo quando o seeding rende pouco. Creators que não querem o produto nem de graça é sinal de produto ou oferta.

### ETAPA 3 · [Fase A] Casting, triagem e Creator Diversity

Leia `reference/casting-e-diversidade.md`. Triagem com o perfil social real, o histórico na plataforma e o engajamento; na dúvida, passe; mensagem padrão de shortlist. Os 6 eixos de diversidade cruzados com os `sub_avatars[]`; todo creator entra no `roster[]` com o sub-avatar que cobre, e o relatório mostra a matriz sub-avatar por creator com as células vazias como casting que falta.

### ETAPA 4 · [Fase A] Contratação, envio e a escolha do produto

Leia `reference/contratacao-e-brief.md`. Hire na plataforma, mensagem pós-contratação, o creator escolhe o produto (nunca envie o que ele não quer) e os statuses do roster.

### ETAPA 5 · [Fase A] O framework de brief (nunca script fechado)

Mesmo arquivo. Framework é o padrão; script só com uma ideia forte e creator compatível; freestyle só pra creator excepcional. Estrutura de 1 página em inglês nos 7 blocos, com Hooks & Ideas de no máximo 9 concepts (semente da `creative-engine` ou dos `angles`). Curadoria por creator: cópia com os 4 a 6 concepts que combinam com o perfil. Um `briefs/framework-[creator-slug].md` por creator contratado, pelo gerador de brief da base.

### ETAPA 6 · [Fase A] Follow-up, coleta e o corte em 3 hooks

Leia `reference/follow-up-e-coleta.md`. Follow-up a cada 3 dias depois da entrega, nunca mais de 7 sem contato; coleta no Drive por creator, favoritos como candidatos a embaixador; marcação `dct_ready` (cada vídeo em 3 versões com 3 hooks) no inventário `content[]` que a `creative-engine` lê. As expectativas de acerto da fonte e a auditoria de ROI em `economics.roi_audit`.

### ETAPA 7 · [Fase A] Pipeline TikTok Shop, a fábrica de volume

Leia `reference/tiktok-shop.md`. Opcional, pra quem opera ou quer o canal como fonte de conteúdo; operação com os números da `marketplace-engine` quando existem; a variante de contas dedicadas; mineração de virais (remake próprio, nunca o vídeo alheio); o motor é micro e médio creator em volume.

### ETAPA 8 · [Fase B] Identificar os winning creators

Leia `reference/winning-creators-e-contrato.md`. Gate: ao menos um `breakthrough` no manifest. Winning creator é o creator cujo ad ganhou spend e escalou. Convenção de nome com o creator no nome do ad (gravada em `handoff.for_skill_10`); cruze a classificação com o mapa creator e ads; meça por janelas de 90 dias.

### ETAPA 9 · [Fase B] Contrato recorrente, retainer e a escada de embaixador

Mesmo arquivo. Modelo 1, retainer simples (1 vídeo por semana, produto grátis, 500 dólares por mês). Modelo 2, brand ambassador com performance (2 a 3 vídeos por semana): comissão em degraus decrescentes sobre revenue ou ad spend, teto mensal com reset, alternativa por cupom, pagamentos nos dias 1 e 15 e a planilha `roster.csv`.

### ETAPA 10 · [Fase B] Onboarding e comunicação contínua

Leia `reference/onboarding-e-feedback.md`. Onboarding deck, contrato em 3 variantes com as cláusulas da fonte e o aviso jurídico obrigatório, mensagem de kickoff e canal por creator (promo avisada com 7 a 10 dias, produto novo sempre).

### ETAPA 11 · [Fase B] Feedback loop e report mensal por creator

Mesmo arquivo. Report por creator com as métricas que ele vê sob a regra de transparência por tier; comentários dos ads viram ideias; report mensal pra todos com os top 5 e o porquê; o `creator-report.md` da `content-recycler` se distribui por aqui.

### ETAPA 12 · [Fase B] Whitelisting

Leia `reference/whitelisting-e-partnership.md`. As 6 regras da fonte (só creator com winning ad; só os ads dele na página dele; preço zero ou quase; agreement assinado; avisar o creator). Setup de acesso e copy como se fosse o creator falando. Onde testar por nível de spend; execução pela `ad-strategy` e `scale-engine`. Variante de páginas de nicho e a espionagem na Ads Library.

### ETAPA 13 · [Fase B] Partnership ads

Mesmo arquivo. Formato nativo marca mais creator com dynamic identity; pitch de acesso por 30 dias pra creator novo, com o timing certo por fase; teste em todos os top criativos dos ambassadors.

### ETAPA 14 · [Fase B] Raw content campaign, creator farming e recrutamento contínuo

Leia `reference/raw-content-e-recrutamento.md`. Raw content campaign (montagem e budget da `ad-strategy` e `scale-engine`); creator farming com o seeding sempre rodando; recrutamento pago de afiliados; atribuição por custom link; ad bounties externos no `roster[]` com `tier: "bounty"` e a mesma convenção de nome.

### ETAPA 15 · Checagens de sanidade

Leia `reference/sanity-checks.md`: os doze itens. Falha bloqueia o `.md`.

## SALVAR

Leia `reference/salvar-e-manifest.md`. `mkdir -p workspace/[produto]/creator-engine/`; `creator-engine.md` na ordem do arquivo, `creator-engine.html` por `python3 tools/render_report.py workspace/[produto]/creator-engine/creator-engine.md`, `dados.json` no schema de `reference/dados-json.md` (quem lê o quê em `reference/contrato-de-leitura.md`), mais o material operacional em inglês sem `.html`: `briefs/framework-[creator-slug].md`, `outreach/messages.md`, `contracts/ambassador-agreement-[variant].md` e `roster.csv`. Manifest pelo script: `python3 tools/manifest.py <slug> complete creator-engine`, `set creator` com o bloco de fase, nunca `manifest.stage`, e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Íntegra em `reference/mensagem-final.md`, como draft: Fase A (rota, campanha de seeding, briefs curados, expectativa honesta dos 26 dias e do embaixador, follow-up e corte); Fase B (winning creators, contratos, whitelisting com as 6 regras, partnership, convenção de nome, report mensal); e a resposta a quem pede Fase B sem breakthrough.
