---
name: promo-engine
description: Engine de janela promocional — dona da promoção de ponta a ponta (Q4/BFCM, datas sazonais e sales datadas). Orquestra o calendário da janela (quando começar, com as datas e prazos da fonte primária — começar cedo é a tese central), a preparação (momentum do evergreen antes da janela, decisão de lead-gen VIP pelo critério de returning customers, estoque via 01b e backups via 19-ops-engine), a oferta da promo (hierarquia de ofertas BFCM, store credit, stacking e linguagem), o GATE inegociável de recálculo do breakeven ROAS e CPA com a margem promocional antes de ligar qualquer campanha (sem números recalculados, a skill PARA), a execução (Promo Campaign Broad/WARM60/HOT90 em paralelo ao evergreen, criativos "best ad + banner" via handoff pra 08, calendário de email/SMS que a 13 transforma em assets, surf scaling e reset da meia-noite pelo cânone ad-taxonomy §5, tudo logado no ad-log) e a aterrissagem (regra de fim por horário, volta pro evergreen, leitura pós-promo com a 11 e a 15, revival sazonal de winners pelo Desire Calendar). Lateral/sazonal — não é etapa da sequência 00→14; dispara por época ou pedido. Use quando o membro disser "black friday", "bfcm", "promo", "promoção", "sale", "q4", "cyber monday", "desconto sazonal", "mother's day", "valentine's", "flash sale".
---

# Promo Engine

> **Índice de frameworks:** os sistemas desta skill vivem espalhados em VÁRIOS domínios de `.claude/lib/kb-index/` (`frameworks.json` / `README.md`) — `meta-ads-strategy`, `scaling`, `finance-projections`, `creatives-hooks-formats`, `retention-email`, `offer-pricing-guarantee`, `page-landing-cro`, `brand-building-bonus-aov`, `market-research-voc` e `supply-chain-sourcing`. Não existe domínio "promo" dedicado. Contrato de cobertura: no início de cada ETAPA, enumere as entradas desses domínios cujo `use_in_skill` inclui a 17 e puxe cada uma pela `best_query` exata com `deep=true` — o núcleo nomeado embutido nas ETAPAs é o mínimo garantido, nunca o teto.
>
> **Cânones que governam esta skill:** `.claude/lib/ad-taxonomy/README.md` **§5** (Scaling Protocol e as duas exceções — **(a) promo com data-fim entra direto no budget planejado**, e o que protege a promo é o surf + o reset da meia-noite; **(b) "new reason to be scaling"** reinicia a leitura) e `.claude/lib/unit-economics/README.md` **§1** (margem de contribuição ≠ lucro) e **§4** (espiral do ROAS). Esta skill **referencia** os cânones, nunca os redefine — onde o texto daqui divergir, o cânone vence e a divergência é bug desta skill. Todo registro de mudança na conta segue o cânone `.claude/lib/ad-log/README.md`.

## Quando Usar

Quando existe (ou vai existir) uma **janela promocional com data de fim**: Black Friday/Cyber Monday e o Q4 inteiro, datas sazonais (Valentine's, Mother's Day, Memorial Day, Labor Day, Halloween) ou uma flash sale. Gatilhos: "black friday", "bfcm", "promo", "promoção", "sale", "q4", "cyber monday", "desconto sazonal".

**Não é fase do pipeline — é skill lateral, como a 15.** Dispara por pedido do membro; a época é o motivo natural de chamar (setembro-outubro pra montar o Q4; meados de janeiro pro Valentine's — o Desire Calendar dá o timing de cada data). Pode rodar mais de uma vez por ano, uma rodada por janela.

**O que esta skill é dona e nenhuma outra era:** o calendário da janela, a mecânica da oferta promocional, o gate de números recalculados, a estrutura de campanha de promo, o plano de escala DENTRO da janela e a aterrissagem de volta pro evergreen.

**O que ela NÃO faz (divisão explícita com as vizinhas):**

| Trabalho | Dona | O que a 17 entrega pra ela |
|---|---|---|
| Produzir os assets de criativo (banners, statics, vídeos) | **08** | Brief de criativo de sale (ETAPA 6) |
| Escrever os emails/SMS e montar os sends no ESP | **13** | Calendário, janelas e segmentos (ETAPA 7) — a 13 executa os assets e mantém os flows coerentes com a promo no ar (flow nunca desliga durante campanha; se adapta) |
| Estrutura de campanha evergreen e teste de criativo | **10** | Nada — o evergreen segue intocado em paralelo |
| Escala evergreen fora de janela | **12** | O registro da janela (a exceção (a) do §5 só vale com data-fim) |
| Modelo financeiro completo | **15** | O flag de cohort de promo pra calibragem (ETAPA 10) |
| Estoque e fornecedor | **01b** | A cobrança da confirmação de volume antes da janela |
| Backups de conta, processadora e operação | **19-ops-engine** | Pointer na preparação |

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também em `manifest.report_language`). TODO output interno (.md/.html/.json descritivo) e toda conversa com o membro usam esse idioma. **Copy consumidor-final permanece SEMPRE em inglês US** — nome da sale ("Black Friday Sale"), texto de banner ("25% off EVERYTHING"), headlines, emails. A escolha de idioma vale só pra documentação interna.

### Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] `workspace/[produto]/04-offer-builder/dados.json` existe — é a fonte do stack de custos (`cogs_breakdown`, 8 campos), do `unit_economics.weighted_margin_per_order` e do `pricing.aov_expected`. Sem esses números o gate da ETAPA 4 não fecha
- [ ] Loja no ar (`manifest.storefront.page_url` ou confirmação do membro) — promoção pressupõe página publicada; sem loja, o caminho é o pipeline normal (00→10), não esta skill

Se `04-offer-builder/dados.json` faltar, não aborte seco (rule `emergency-escape-paths.md` ES1). Ofereça **(A)** rodar a skill 04 agora, **OU (B)** prosseguir pedindo direto ao membro o AOV e o custo por pedido item a item, marcando `manifest.skipped_preflight += ["04-offer-builder/dados.json"]`. O gate da ETAPA 4 aceita números vindos do membro — o que ele **não** aceita é número estimado.

**Histórico de ads (10/11) NÃO é pré-requisito**, mas muda a rota de criativo: com winners provados, a doutrina é "best ad + banner"; sem nenhum winner, a rota é a outra metade do blueprint — statics de foto do produto + oferta (ETAPA 6). **Loja nova na semana da BF é não** (CPM de US$ 300+ na semana): sem conta rodando, a recomendação honesta é não estrear na janela mais cara do ano.

### Contexto a carregar

1. `workspace/profile.md` — stage e budget (`member-stage-awareness.md`: os gates do protocolo não mudam por stage; o que muda é o apetite dentro deles — surf é coisa de `scaling`, starter roda a janela sem surf)
2. `workspace/[produto]/manifest.json` — **`target_cpa` e `breakeven_roas`** (se existirem, carregam o recálculo mais recente e prevalecem sobre o `dados.json` da 04 — mesma precedência das skills 10 e 12), `budget_daily`, `stage`, `breakthroughs[]`/`ad_classification[]` (matéria-prima do banner), `fixed_costs_monthly`, `esp`, `storefront.page_url`, `retention.phase_a_done`
3. `workspace/[produto]/04-offer-builder/dados.json` — `cogs_breakdown` (os custos em % do preço encolhem junto com o desconto; os custos em dinheiro por pedido não — a diferença é o que espreme a margem), `unit_economics` completo, `pricing.aov_expected`
4. `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** — `handoff.for_skill_12` (custo fixo, teto de escala, caixa pra 90 dias, veredito da espiral) + `monthly_model.fixed_costs_monthly` + `roas_spiral` (a fórmula do breakeven com fixo vive na ETAPA 5 da 15 — esta skill a reaplica com a margem promocional, nunca a redefine) + `cohorts` (baseline pra leitura pós-promo). Leitura aditiva: sem o arquivo, a janela roda com margem de contribuição e a frase honesta do §1
5. `workspace/[produto]/sourcing/dados.json` **(se existir)** — `calendar.volume_confirmation_30_60_90` e `calendar.reorder_point_days` (a confirmação de volume por escrito que a janela vai consumir)
6. `workspace/[produto]/11-ad-analysis/dados.json` + `workspace/[produto]/ad-log.md` — classificação por criativo (o "best ad" do banner é `breakthrough` ou, na falta, o `spend_winner` mais estável), CPM da conta, trajetória
7. `workspace/[produto]/12-scale-engine/dados.json` **(se existir)** — escola de escala em uso, `scale_phase`, hábito de reset da meia-noite já instalado
8. `workspace/[produto]/10-ad-strategy/dados.json` **(se existir)** — estrutura evergreen atual, convenção de nomes, URL de destino
9. `workspace/[produto]/13-retention-engine/dados.json` **(se existir)** — flows ativos (o que a promo precisa adaptar, nunca desligar)
10. Rodadas anteriores desta skill em `workspace/[produto]/17-promo-engine/` — em especial `seasonal_vault[]` de janelas passadas: winners sazonais guardados são a primeira coisa a religar (ETAPA 6)
11. Os três cânones do header — leitura obrigatória antes de qualquer recomendação

### O gate que não se negocia

**Recalcular o breakeven ROAS e o CPA-alvo com a margem promocional ANTES de ligar qualquer campanha.** É o erro nº 1 da temporada segundo a fonte primária (P1): lançar oferta melhor (margem menor) e continuar escalando no MESMO ROAS-alvo de antes — mais receita, menos lucro. A ETAPA 4 é esse gate. Sem `promo_economics` calculado com os números do membro, as ETAPAs 5 a 8 **não rodam**: nenhuma campanha é criada, nenhum brief vai pra 08, nenhum calendário vai pra 13. A skill para e diz o que falta. Número de margem **nunca se estima** — vem da 04, do manifest ou do membro.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema, agrupado por ETAPA (o mapa fino está nas ETAPAs). Núcleo mínimo a carregar antes de montar qualquer plano de janela:

- **Promo Campaign (Broad / WARM60 / HOT90)** — `promo campaign CBO três ad sets broad WARM60 HOT90 retargeting só em sale`
- **Offer-Change Break-Even Reset** — `nova oferta recalcular break-even ROAS e CPA-alvo antes de escalar promo`
- **Scaling Protocol & Decision Tree (fonte primária 2026)** — `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo` (é dele que vem a exceção de promo do §5)
- **Curva BFCM + Cyber Monday Nightcap** — `curva BFCM sexta é sempre o maior dia sábado de manhã nightcap Cyber Monday 15h EST`
- **Surf Scaling (escala intradiária)** — `surf scaling escala intradiária planilha por período blended ROAS dobrar 20%`
- **Reset da meia-noite (~50% do spend REAL)** — `reset da meia-noite metade do spend real nunca budget nominal explode a conta`
- **Blueprint de criativo de sale** — `criativos de sale banner sobre o melhor ad foto do produto com oferta statics BFCM`
- **Desire Calendar (calendário sazonal de desejos)** — `calendario sazonal de desejos health sex status belonging control comfort por mes`
- **Regra de fim de promo por horário** — `custom rule turn off condition time current time is greater than data fim promo`
- **Revival de winner sazonal / calendário de desejos** — `religar seasonal winners ads que morreram voltam no mesmo período calendário de desejos`

Aprofunde. Uma janela de promo concentra num fim de semana o volume de decisões de um trimestre — errar a margem ou o reset custa o mês mais importante do ano.

## Fluxo da Skill

### ETAPA 1 — A janela: qual data, quando começar, como se chama

Pergunte (ou confirme) numa mensagem só: **qual evento**, **estoque disponível** e **quanto do budget o membro topa dedicar à janela**. O resto sai dos artefatos.

**A tese central da fonte (P1): comece a sale cedo.** Sem um diferencial de marca fortíssimo, o consumidor compra do primeiro que abrir a sale — e a compra de Black Friday começa a ser planejada meses antes (listas de presente montadas a partir de ads vistos desde o começo do ano). Três benefícios de abrir antes: captura quem vai comprar de qualquer jeito; permite testar oferta, criativo e site ANTES do pico; e gera momentum na conta. Começar cedo **não** drena o pico: marca que tem BF grande tem BF grande mesmo abrindo 1-2 semanas antes.

**Âncoras de calendário (playbook de Q4 da fonte, edição 2025 — a estrutura relativa se mantém de ano pra ano):**

| Janela | Quando (edição 2025) | Nota da fonte |
|---|---|---|
| Labor Day | sale imediata, rodar até a segunda | data menor, opcional |
| Fall/Halloween sale | ~20/out a 2/nov (~2 semanas) | teste geral de oferta+criativo+site antes da BF |
| **Black Friday sale** | **começar 3/nov (ideal) ou 10/nov; 24/nov é tarde demais** | ramp de 2-3 semanas basta — ads de sale não precisam de meses de dados |
| BF weekend + Cyber Monday | o pico | **só escalar** — todos os split tests desligados e finalizados antes |
| Holiday sale | até ~16-17/dez | oferta degradada de propósito (urgência real) |
| Janeiro ("Q5") | mês inteiro | pra supplements/health & wellness, "new year new me" — não tirar o pé em dezembro |

Datas menores (Veterans Day etc.): só se fizerem sentido pra audiência; na dúvida, chame de "early BFCM". Regionalização (do playbook de Q4 da fonte): Singles' Day (11/11) eclipsa a BFCM na Ásia; Boxing Day (26/12) é forte em Austrália/NZ, UK e Canadá — cruze com `manifest.market`.

**Nome da sale: não complicar.** "Black Friday Sale" é o que as pessoas procuram — use a linguagem do cliente, não um nome criativo interno. Nome e copy da sale em inglês US.

**O ângulo do mês vem do Desire Calendar** (rode a query do núcleo): outubro = expressão de identidade/status (dá pra vender status sem vender fantasia — "look good at the party"); novembro = família e pertencimento; dezembro = gifting + urgência de entrega; janeiro = saúde/recomeço (gasto de saúde sobe ~35-40%); fevereiro = Valentine's, e a regra da fonte é **"people don't buy gifts ON Valentine's Day, they buy gifts FOR Valentine's Day"** — a janela abre em meados de janeiro, não na semana do dia 14.

Complemento — rode `calendário Q4 comece a sale cedo início de novembro tarde demais 24 progressão de oferta holiday`.

Grave `window` no `dados.json` (evento, início, fim, fases, fuso do ad account) e `manifest.promo` (ver SALVAR).

### ETAPA 2 — Preparação: o que precisa estar de pé ANTES da janela

**2.1 — Momentum do evergreen (o teto pré-BF).** A BF multiplica o que a conta já é: *"se a conta está morta, a BF te dá escala, não mega escala"*. Chegar a dias grandes no pico exige winners provados e momentum ANTES da janela — o trabalho de setembro/outubro é a 08 (batches), a 11 (leitura) e a 12 (protocolo) empurrando o evergreen pro teto, não esta skill. Durante o Q4 o teste de evergreen **continua** (com viés mais product-aware; menos vídeo longo de venda em novembro). E administre o **contraste de oferta** o ano todo: oferta promocional só existe em contraste com a evergreen. Se a evergreen já está na melhor oferta possível, as saídas da fonte são: store credit/presente como camada extra na janela; subir o preço agora e "baixar" na data (testando o preço maior desde já); ou aceitar degradar a evergreen depois da janela pra reabrir distância. Rode `escalar evergreen antes da janela momentum winners contraste de oferta evergreen no teto store credit camada extra`.

**2.2 — Lead-gen VIP: decisão explícita (o default é NÃO fazer).** Posição da fonte na edição 2025 (mudança vs. o ano anterior): a maioria das marcas de resposta direta não deve captar lista antes da promo — melhor vender direto começando a sale cedo. Lead-gen VIP só faz sentido com **pelo menos um** destes: **taxa de clientes que voltam a comprar ≥ 30%**, OU parte grande das vendas vindo de orgânico verdadeiro (boca a boca), OU posicionamento de marca muito único (ex.: fashion com drops) — e nunca sem operação de email/SMS forte. Se os critérios fecharem: funil VIP (ads → opt-in pra oferta VIP melhor que a pública, ou early access), rodando ~2 semanas antes da abertura, projetado pela **Calculadora de lead gen VIP** (rode `VIP lead gen calculator pré-BF CPL AOV CVR dos leads break-even projetado`) — 5 entradas: spend total, custo por lead aceitável, AOV da oferta específica, taxa de conversão dos leads (referências da fonte: AOV > US$ 200 → 2-4%; AOV < US$ 200 → 6-10%; há quem reporte 10-15%, não conte com isso) e **a margem JÁ com o desconto VIP dentro** (não o custo do produto puro). Filosofia declarada: **sempre subestimar**. Os leads que não converterem ficam na lista pra 13 trabalhar depois. Complemento do critério: `lead gen VIP quando não fazer returning customer rate 30 por cento vender direto começando cedo`.

**2.3 — Estoque.** Leia `sourcing/dados.json` → `calendar.volume_confirmation_30_60_90` (a confirmação POR ESCRITO do fornecedor de que entrega o volume projetado) e `calendar.reorder_point_days`. Sem a confirmação, a janela roda no escuro — cobre antes de abrir. Regras da fonte: comprar estoque com antecedência (a fábrica lota no Q4); se subestimou, **pre-order com expectativas claras** vence encalhe (com prazo comunicado, a conversão quase não cai). Depois da janela, o planejamento integrado de Q1+Q2 evita a armadilha de concentrar tudo no Q4 (rode `planejamento Q1 Q2 armadilha Q4-heavy front-load SKUs janelas de negociação janeiro março` — domínio da 01b, aqui só a cobrança).

**2.4 — Backups e pior cenário → skill 19-ops-engine.** Conta de anúncio reserva com campanhas pré-montadas e desligadas, processadora e banco backup, CS dimensionado pra 3-10× o volume de tickets, prazos de envio de dezembro comunicados — esse plano de redundância é da 19: se o checklist de continuidade dela ainda não rodou (ou está com pendência), recomende rodá-la ANTES da janela. Registre em `prep.ops_backups` o status que a 19 reportar (ou o que o membro declarar), sem virar dono do assunto.

**2.5 — Site pronto ANTES (o pico é pra escalar, nunca pra otimizar site).** O elemento nº 1 de conversão de sale segundo a fonte: mostrar em todo lugar **quanto** a pessoa está economizando — *"make sure the customers aren't doing math"*. Direções (execução com 07a/07b/07d):
- **Automatic discount** sempre que a sale é do site inteiro: aplica sozinho, aparece no carrinho, zero fricção de cupom — com a trava "only apply discount once per order" marcada e **data/hora de início e fim agendadas**. Rode `automatic discount aparece no carrinho, only apply discount once per order, economia visível em cada etapa`.
- Sale visível na homepage e nas PDPs mesmo mandando tráfego direto pra landing; **otimizar a página existente** em vez de criar página nova da sale (uma ferramenta de A/B com redirecionamento 100% pra versão de sale na mesma URL resolve a troca no dia).
- **QA total da loja em outubro**: pegar o celular, clicar em tudo, tentar quebrar o site — e **desenvolvedor de plantão** no pico (um bug não pode arruinar o maior dia do ano).
- Teste de messaging/hero da BF com antecedência só pra quem fatura US$ 400-500k+/mês (Intelligems) — é um dos motivos de começar a sale cedo.
- Fotos festivas profissionais (produto + contexto de Natal) servem mais pra site e landing do que pra ads.

Rode `preparação de site pra sale QA outubro developer de plantão economia visível photoshoot sazonal agendar tema`.

### ETAPA 3 — A oferta da promo

Carregue antes: **Offer Type Menu** (`offer types percent off dollar off buy one get one free gift free ebook free shipping threshold margin`), **Scarcity & Urgency Framework** (`scarcity urgency limited quantity deadline price increase bonus removal consequence of delay real reason` — urgência sempre real, nunca inventada) e **Breakage & Slippage** (`40% dos rebates nunca são resgatados, gift card não usado, custo efetivo do desconto`).

**A hierarquia da fonte (P1) — as duas melhores, disparado: percentage off e dollar off.** Porque qualquer pessoa entende, e porque barateiam exatamente o produto que a pessoa já veio comprar. Regra de escolha: **use o número que PARECE maior** — ticket baixo, percentual soa maior ("25% off" > "save $5" num produto de US$ 20); ticket alto, valor absoluto soa maior ("save $500" > "save 10%" num produto de US$ 5.000).

| Oferta | Papel na janela | Nota da fonte |
|---|---|---|
| **% off / $ off** | **core** | o número que parece maior; desconto uniforme merece "X% off EVERYTHING" |
| **Buy X Get X Free** | core alternativo | se já roda "compre 1 leve 2" no evergreen, escale pra "buy 1 get 2 free" na data; "free" converte melhor que "buy X get X% off" (esta a fonte não recomenda) |
| Free gift, free shipping, bundle & save | **add-ons de stack, nunca core** | *"não quero sua tote bag; quero $15 off do produto que eu vim comprar"* |
| **Buy X, GIFT X free** | teste | mesmo mecanismo do leve-2, enquadrado como presente: mecânica visível por estágio ("compre 1 pra você, adicione o 2º e nós embrulhamos"), razão logística ("resolva seu Natal agora"), resultado em dupla ("treine com um amigo"), embrulho cortesia |
| **Store credit / gift card** | teste de alto potencial | em vez de US$ 20 off, um gift card de US$ 66: custa ~os mesmos US$ 20 (você só paga a margem do valor de face) com valor percebido ~3×; parte nunca é resgatada (a quebra joga a favor — Breakage & Slippage); quem resgata volta a comprar; dá pra presentear |
| Oferta por avatar | teste em landing | simplificar a escolha pela vida do avatar ("comprando pra 1 ou 2 pessoas?" em vez de "1, 2 ou 3 packs") |
| Quiz offer | teste (gifting) | "encontre o presente certo" como funil |

**Stacking e linguagem (regras duras da fonte):**
- Empilhar desconto embutido de bundle + % extra da data e comunicar o total ("save up to 40%") é legítimo — mas **recalcule o preço final a partir do compare-at**: 10% + 20% em cima NÃO é 30%. A matemática errada no banner é bug de compliance e de confiança.
- Desconto uniforme → **"X% off EVERYTHING"** (mais forte que "site-wide"). **"Up to X% off" só quando o desconto NÃO é uniforme** — e saiba que o consumidor já desconfia do padrão "up to 70%" com 70% só no estoque encalhado. "Biggest sale of the year/ever" só quando for verdade.
- **NUNCA inflar o compare-at price** pra fabricar desconto: *"as pessoas viram seus ads o ano todo; você não está sendo um bom vendedor, está enganando."* É gate ético e de conta.
- Aceitável o ad dizer 25% e o site dar 40% (surpresa positiva); **o inverso destrói a conversão**.
- Toda sale precisa de **razão declarada** — data sem razão vira ruído (a razão é o que a 13 escreve nos emails).

**Progressão dentro da janela (recomendação 2025 da fonte):** rodar a MELHOR oferta a janela inteira e, no fim de semana do pico, adicionar um bônus por cima ("free gift / gift card — BF weekend only"). Depois da Cyber Monday, **degradar de propósito** pra oferta média no holiday sale — é isso que torna a urgência do pico real. Objeção clássica "cliente novo nunca viu a oferta antiga, por que melhorar?": com CTR de ~2%, 98% de quem viu o ad não clicou, e jornadas de compra de 2-7 meses são comuns — "cliente novo" ≠ "nunca te viu"; oferta melhor gera salto maior.

**Dezembro:** alternativa que preserva margem — **free express shipping "get it by Christmas"** em vez de % off (exige estoque no país); "priority processing" pago (US$ 5-10) só se o backend priorizar de verdade, senão vira chargeback.

Hierarquia e ofertas — rode `hierarquia de ofertas BFCM percentage off dollar off número que parece maior everything site-wide up to compare-at` e `store credit gift card 66 custa 20 valor percebido buy x gift x oferta por avatar quiz`.

Grave `offer` no `dados.json`: tipo core, stack, desconto efetivo total (com a matemática do compare-at conferida), bônus do pico, oferta degradada da cauda, oferta VIP (se ETAPA 2.2 aprovou).

### ETAPA 4 — GATE: recálculo do breakeven com a margem promocional

**Esta ETAPA é a razão de a skill existir como dona da janela.** Rode **Offer-Change Break-Even Reset** (`nova oferta recalcular break-even ROAS e CPA-alvo antes de escalar promo`) e, se a 15 existir, releia `roas_spiral` e `handoff.for_skill_12`.

O exemplo canônico da fonte, pra calibrar a leitura antes da conta: base com ROAS-alvo 2,0×, breakeven 1,43×, 70% de margem bruta — US$ 100k de spend → US$ 200k de receita → ~US$ 40k de lucro. Entra 30% off → a margem cai pra ~55% e o breakeven vira ~1,82×. Quem mantém o alvo de 2,0× e sobe o spend pra US$ 150k termina com US$ 15k. **"Você fez US$ 100k a mais de receita e US$ 25k a menos de lucro."**

**A conta, com os números do membro (mesma família de fórmulas da 04/15 — nada novo):**

```
desconto_efetivo         = desconto total por pedido, em dinheiro, com o stack inteiro dentro
                           (recalculado a partir do compare-at; store credit entra pelo CUSTO REAL:
                            a margem do valor de face, ajustada pela quebra esperada — não o valor de face)

aov_promo                = aov_esperado − desconto_efetivo

margem_promo_por_pedido  = recomputar o stack da 04 sobre o preço promocional:
                           custos em % do preço (processamento, provisão de reembolso, fee variável)
                           encolhem junto; custos em dinheiro (produto entregue, frete, pick/pack) NÃO —
                           é por isso que a margem % cai mais do que o desconto sugere

margin_rate_promo        = margem_promo_por_pedido ÷ aov_promo
breakeven_roas_promo     = 1 ÷ margin_rate_promo          (= aov_promo ÷ margem_promo_por_pedido)
breakeven_cpa_promo      = margem_promo_por_pedido
target_cpa_promo         = breakeven_cpa_promo − lucro desejado por pedido na janela
```

Com `15-finance-engine/dados.json` na mão, reaplique a fórmula da ETAPA 5 da 15 com o `margin_rate_promo` pra publicar `breakeven_roas_with_fixed_promo` — mesma fórmula, margem nova; esta skill não a redefine. Sem a 15, os números da janela são **margem de contribuição**, e o relatório diz isso com todas as letras (unit-economics §1) — nunca "lucro".

**Réguas de margem da fonte:** piso absoluto ~**55%** de margem bruta na oferta promocional; tente ficar **acima de 60%**. AOV baixo (< US$ 60) exige margem % mais alta; AOV alto tolera % menor. Furou o piso → volte pra ETAPA 3 e redesenhe a oferta (store credit e Buy X Gift X existem exatamente pra dar generosidade percebida sem furar margem).

**Métrica da janela:** o que manda é o **blended ROAS** — receita do Shopify ÷ spend total (rode `blended ROAS Shopify dividido por spend total atribuição first click mente` e `blended decide o negócio plataforma decide a otimização third-party red flag incrementalidade`). Marca com orgânico forte (ex.: metade da receita) **não escala por blended** — olha dado click-based/incremental; no surf, olhe também 1-day click (compradores de agora). *"Screenshot de US$ 500k/mês não paga boleto: olhe o P&L, não o dashboard."* Melhor um dia menor com margem do que um dia recorde sem lucro.

**Saída do gate (binária):**
- **Números completos** → grave `promo_economics` com `status: "computed"` e siga pra ETAPA 5.
- **Falta qualquer número** (margem, AOV, desconto definido) → `status: "blocked_pending_inputs"`, `pending_inputs[]` preenchido, **as ETAPAs 5-8 não rodam** — nenhuma campanha criada, nenhum brief pra 08, nenhum calendário pra 13. A skill para e pede o que falta, em uma mensagem. Nunca preencher com plausível.

### ETAPA 5 — Estrutura de campanha da janela

Rode **Promo Campaign (Broad / WARM60 / HOT90)** (`promo campaign CBO três ad sets broad WARM60 HOT90 retargeting só em sale`) e **Full Media Buying 2026** (`estrutura full media buying 2026 cinco camadas main CBO ABO zombie raw content promo` — a Promo CBO é a camada satélite que só nasce com data de fim; quem monta é esta skill, nunca a 10).

**A estrutura (a única ocasião de retargeting do sistema):** fora de sale, retargeting não paga; em sale, o público quente tem urgência real e merece frequência alta. **1 campanha CBO, 3 ad sets:**

| Ad set | Audiência | Detalhe |
|---|---|---|
| **Broad** | só idade, gênero e país | sem lookalike, sem interesse |
| **WARM60** (meio de funil) | engajadores da página do FB 60d + engajadores do IG 60d + 95% video viewers 60d (todos os vídeos com 1.000+ views) | **excluindo** as audiências do HOT90 |
| **HOT90** (fundo de funil) | visitantes do site, view content, add to cart, initiate checkout — 90 dias | — |

Audiências em Audiences → Create Audience → Custom Audience (fontes: página do FB / conta do IG / vídeo / site), retenções 60/90. CBO com budget alto — o Meta aloca onde performa (a estrutura levou contas de US$ 10k pra US$ 70k/dia em 24h na fonte). **O evergreen continua rodando em paralelo, sempre** — a promo é um sistema paralelo temporário; criativos de sale ficam NA campanha de promo (não misturar com os post IDs do evergreen).

**Budget da janela (cânone §5, exceção (a) — cite, não redefina):** promo com data-fim **entra direto no budget planejado** — não sobe em degraus de +20%, porque a janela termina antes de os degraus chegarem lá. O que protege a promo é o **surf + o reset da meia-noite** (ETAPA 8). Referências da fonte pro tamanho inicial: **não há fórmula** — até ~10% do spend diário total é conservador e ok; no máximo ~50% se extremamente confiante; num dia de US$ 100k de spend, a referência citada foi US$ 25k evergreen + US$ 75k promo (no pico, com a promo provada). De quinta pra sexta **não dobre preventivamente** "porque é Black Friday" — mantenha e escale intraday quando os dados aparecerem. Rode `promo campaign separada do evergreen timing início de novembro budget inicial 10 por cento conservador 50 máximo realocação`.

Mais três regras de estrutura da fonte: 1 campanha de promo + 1 evergreen (+ promo por país, se multi-país) — **não** pulverizar em campanhas separadas por formato (dilui e derruba o retorno); produto de ticket muito diferente ganha campanha própria (objetivo diferente pro algoritmo); e a campanha nomeada com o nome da sale + ano, seguindo a convenção de nomes da 10.

**Execução opcional via Meta MCP (mesma cascade da 10/12):** oficial `mcp__meta__ads_*` → Pipeboard `mcp__meta-ads__*` → manual (detecção por prefixo, `.claude/lib/mcp-detect/README.md`). Criar campanha + 3 ad sets + audiências em `status: PAUSED` — **o membro revisa e ativa; a skill NUNCA ativa nada sozinha.** A automated rule de fim de janela (ETAPA 9) nasce DESATIVADA pro membro revisar e ativar antes do fim. Falha de API → `emergency-escape-paths.md` ES6. Sem MCP → passo a passo manual campo a campo. IDs criados em `dados.json.campaigns[]` e **linha no `ad-log.md` na mesma execução** ("criado em PAUSED", executor `skill-17`, motivo "promo início — [evento]").

### ETAPA 6 — Criativos da janela (brief pra 08)

Rode **Blueprint de criativo de sale** (`criativos de sale banner sobre o melhor ad foto do produto com oferta statics BFCM`) e **Revival de winner sazonal** (`religar seasonal winners ads que morreram voltam no mesmo período calendário de desejos`).

**A doutrina da fonte é anticlimática e comprovada ano após ano: os melhores anúncios de sale são (1) o seu melhor ad existente com um banner de oferta por cima e (2) foto simples do produto + oferta.** Statics superam vídeos no pico — o público está em modo most aware, procurando produto + oferta (o melhor ad de um dia de US$ 700k na fonte foi uma FOTO do produto com a oferta). **Não gaste semanas em UGC customizado de sale** — "essas ads nunca ganham spend".

O brief que esta skill entrega pra 08 (`creative_brief_08` no `dados.json`), em ordem de prioridade:

1. **Winner + banner:** o melhor vídeo da conta (breakthrough do `manifest.ad_classification`; na falta, o spend_winner mais estável) com banner de sale no topo/rodapé (geralmente rolando) ou sticker "Black Friday Sale Live". **Exceção:** se a headline do winner é o que fisga, NÃO cobrir com banner gigante — call-out discreto ("BF 52% off") ao lado; testar as duas vias e dobrar na que ganhar.
2. **Statics de produto + oferta:** call-out grande e claro da sale + produto + prova social + urgência guiando o olho; text-heavy simples deixando claro O QUE se vende; multi-SKU/fashion mostra variantes e cores (+ catalog ads).
3. **Revival sazonal:** religar o que performou out-dez do ano passado (leia `seasonal_vault[]` de rodadas anteriores e a 11) — **com re-banner, porque a oferta mudou** (case da fonte: marca a US$ 500-600/dia religou um ad sazonal de dois anos antes e foi a US$ 3-4k/dia).
4. **Scarcity ads pra early sale:** a única razão de comprar ANTES do pico é escassez real ("sold out 12 times") — filmável com o produto e um post-it; versão pre-order pra quem vai estourar estoque ("due to extreme demand, limited pre-run").
5. **Complementos:** static → GIF (banner animado vira "vídeo" e alimenta a audiência de 95% viewers do WARM60); founder text ad (texto puro, estilo carta, pra quem está em cima do muro — rodar nos 3 ad sets); bundle ads ("life is better when you bundle" — quem clica em bundle leva bundle); whitelisted ad na página de creator.

Escreva já nos criativos da sexta **"Black Friday Cyber Monday Sale"** — os ads de BF **continuam rodando na Cyber Monday** (não desligue no domingo pra lançar campanha nova: o momentum e os dados da semana valem mais; marcas grandes fazem exatamente isso; pode ciclar criativo novo na segunda sem desligar o que roda). Rode `não desligar ads de black friday na cyber monday momentum black friday cyber monday sale no criativo`.

**Volume:** começar com 2-3 batches (~9-12 statics/semana; 3-4 batches pra resposta direta), ver o que roda e fazer mais do que funcionou — swings maiores entre conceitos. Texto do banner conferido contra a matemática da ETAPA 3/4 (o "save up to X%" é o desconto efetivo real) e contra as regras 8a/8b do CLAUDE.md. Copy em inglês US.

A 08 produz os assets a partir deste brief — handoff nomeado, com o `creative_brief_08.handed_off: true` e a data.

### ETAPA 7 — Email/SMS da janela (calendário da 17, assets da 13)

**Divisão explícita, sem órfão:** a **17 é dona do calendário, das janelas de envio, das fases e da orientação de segmento**; a **13 produz os assets** (emails, SMS, adaptação sazonal dos flows) e opera o ESP. Flow **nunca desliga** durante campanha — se adapta (regra da 13). O que esta skill grava em `email_sms_calendar_13` e entrega:

**Fases e prazos (playbook de Q4 da fonte, edição 2025):** ofertas finais e pop-up novo aprovados **até 10/nov**; calendário travado e flows testados **até 15/nov**; warm-up 10-24/nov; BFCM 26-30/nov; gifting window 5-14/dez; last chance 15-21/dez — **os cutoffs de envio (~14-15/dez standard, 19-21/dez express) vêm da operação/3PL, confirme antes de prometer**; 26/dez clearance/Boxing Day; 31/dez campanha final. Rode `email tolera volume SMS é cirúrgico, engaged 30 engaged 90 dormant 120, quiet hours texas` — o princípio-mestre do playbook: **email tolera volume; SMS é cirúrgico**.

**Orientação de segmento que acompanha o calendário:** os grandes pushes vão pro público engajado (30/90 dias); dormentes de 120d+ seguram até o clearance de fim de ano; assinantes não recebem sale do que já assinam; quem comprou na janela sai da pressão de sale. **Criativo por fase segue awareness (Schwartz):** warm-up = problem/solution-aware (teaser, countdown); pico = **most aware — o desconto é o hero**, zero educação de produto; Cyber Monday = counteroffer com twist + "não haverá oferta melhor por 12 meses"; gifting = presente + deadline; last chance = o prazo de envio como argumento máximo; fim de ano = clearance + "new year, new me". Se a ETAPA 2.2 aprovou VIP: o warm-up flow VIP (sequência de 5 emails até o early access) entra no calendário — a 13 constrói.

**Sistemas que a 13 puxa ao executar** (donos dela; a 17 só aponta): `razão para a sale, stock up recommendation, sale de 24 horas não planejada` · `campanha sazonal de 4 dias com 6 templates, dia de slump, template da inveja` · `seasonal abandoned cart SMS update checklist offer details campaign close time urgency scarcity no rain check` · `MMS copy overlay imagem que engaja o coracao evitar MMS nas ultimas horas da promo` · `seis segmentacoes SMS novos versus recorrentes ultima compra VIP por produto por localizacao` · `email SMS coordination echo not collide send email first SMS follow up non-openers staggered cadence`.

Marque `email_sms_calendar_13.handed_off: true` e avise o membro que os sends nascem quando ele disser `'retention'` com a promo no ar.

### ETAPA 8 — Escalar DENTRO da janela (surf, curva, reset)

**Governança: cânone `.claude/lib/ad-taxonomy/README.md` §5 — leia antes, cite sempre, não redefina.** A exceção (a) já colocou a promo direto no budget; a partir daqui a proteção é operacional. Rode **Surf Scaling** (`surf scaling escala intradiária planilha por período blended ROAS dobrar 20%`), **Reset da meia-noite** (`reset da meia-noite metade do spend real nunca budget nominal explode a conta`) e **Curva BFCM + Cyber Monday Nightcap** (`curva BFCM sexta é sempre o maior dia sábado de manhã nightcap Cyber Monday 15h EST`).

**Surf scaling (a escala intradiária da janela):**
- **Pré-requisito:** atribuição em tempo quase real de terceiro (Triple Whale; Hyros/Northbeam citados) — o dado nativo atrasa. Em spend baixo (~US$ 2k/dia) dá pra surfar só com o dado do Meta.
- **Cadência por spend** (não cheque demais — o algoritmo precisa de volume por período): poucas centenas/dia → a cada 6h; ~US$ 5k/dia → 4h; ~US$ 20k/dia → 2-4h; perto de US$ 100k/dia → 1h. Nunca menos de 1h.
- **Régua por período** (contra o KPI da ETAPA 4): 50-100%+ acima → **dobrar** o budget (triplicar se agressivo); 20-50% acima → **+20%**; no KPI → manter; abaixo → **−20%**. Madrugada gasta pouco → contexto, não pânico. Spend saltou de US$ 1k pra US$ 4k numa hora → segure.
- **Planilha por período no fuso do AD ACCOUNT** (a meia-noite que importa é a da conta): spend, receita Shopify, receita da plataforma e blended por janela. Comece a trackear **na quinta**, pra conhecer o padrão noturno da SUA conta antes do pico.
- **Ordem de decisão: blended primeiro.** Blended abaixo do KPI → não escala nada, mesmo com campanha individual bonita (pode ser atraso de atribuição). Blended ok → campanha por campanha, escalando forte a que está entregando (até +100%) e reduzindo a que não está — muitas vezes é só **realocação** entre evergreen e promo. Não escale o Meta por pico de receita de email blast (olhe 1-day click).
- Duplo objetivo declarado: extrair o máximo dos dias bons E proteger o lucro nos fracos (reduzir cedo). **O objetivo da janela é lucro, não receita.**
- Cost caps na janela: suba o **budget**, não o bid — e monitore, porque às vezes disparam gasto.

> ⚠️ **RESET DA MEIA-NOITE (cânone §5 — risco financeiro real):** ao fim de cada dia surfado, o budget do dia seguinte é **~50% do que foi REALMENTE GASTO — nunca o nominal que ficou na tela.** Budget surfado até US$ 150k com gasto real de US$ 70k → o dia seguinte começa em ~US$ 35k, não em US$ 75k do nominal. Sem isso, o pacing do Meta persegue o nominal inteiro e o membro acorda no vermelho. O reset vale TODA noite da janela, sem exceção — o que a exceção (a) do §5 muda é a ENTRADA do budget (direto no valor planejado, sem degraus), nunca o reset; se o dia seguinte pedir, o surf da manhã recupera o nível. **Toda instrução de subida desta skill sai com o valor do reset junto**, gravado em `dados.json.scaling_window.midnight_resets[]`. É melhor começar baixo: com 1-2 dobras você recupera a escala em horas.

**A curva do fim de semana (3+ anos de dados da fonte):** **sexta é SEMPRE o maior dia** — nunca um sábado superou a sexta (ex. real: US$ 800k sex → ~US$ 600k sáb → US$ 450-500k dom → ~US$ 400k seg). **Sábado de manhã é onde a maioria se destrói**: budget alto deixado da sexta + demanda caindo = receita parecida com lucro despencando — reduza na manhã de sábado sem dó. Não persiga o high da sexta. **Cyber Monday:** flatline até ~15h EST e um repique noturno de compradores de última hora que vai até a meia-noite (candles de US$ 50k/h em contas grandes) — como o Meta leva 1-2h pra acelerar o pacing, **o bump de budget é às ~15h EST**, não quando o rally já apareceu. Pós-Cyber: espere o dip e desça os budgets junto.

**Duas regras que atravessam a janela:** (1) **split tests desligados no pico** — o fim de semana é pra UMA coisa: escalar; (2) **cash pronto** — pagamento do Meta recusado por limite no meio do pico = conta restrita no pior momento possível; confira limite de cartão/fatura antes (a 15 responde quanto caixa a janela consome; backups são a 19).

**Registro (cânone ad-log — obrigatório):** TODA mudança executada na janela — criação, ativação, surf pra cima, recuo, reset da meia-noite, desligamento — vira linha em `workspace/[produto]/ad-log.md` **no momento da execução**, formato do cânone (`| data hora | entidade | mudança com valores antes → depois | executor | motivo |`), executor `skill-17` (ou `membro` quando ele relata). Motivos curtos padrão: "promo início", "surf +100% janela 14-16h", "reset da meia-noite", "curva sáb manhã −20%", "nightcap bump 15h EST", "promo fim". Mudança não logada é bug de processo — e é o que torna a leitura da 11 possível depois.

### ETAPA 9 — Aterrissagem: fim da janela e volta pro evergreen

**Fim por horário, sem depender de memória:** rode **Regra de fim de promo por horário** (`custom rule turn off condition time current time is greater than data fim promo`). Ads Manager → Rules → Create new rule → Custom rule → aplicada à(s) campanha(s) da promo → Action: turn off → Condition: **Time → current time is greater than → data/hora de término** → Time range: maximum; Schedule: continuously. A rule checa a cada ~30 min. Criada DESATIVADA pro membro revisar e **ativar antes do fim da janela** (padrão inviolável de automação da casa). O automatic discount já tem a data-fim agendada desde a ETAPA 2.5 — campanha e desconto morrem juntos; banner/announcement bar saem do site na sequência (07b).

**A saída em ordem:**
1. **Pós-pico imediato:** dip esperado — budgets descem junto (ninguém acorda US$ 20k no vermelho por budget de sexta esquecido no sábado); reset da meia-noite até o fim.
2. **Cauda da janela (holiday):** oferta **degradada de propósito** (ETAPA 3) até ~16-17/dez; depois, dezembro fecha com o argumento de prazo de envio, não de desconto.
3. **Campanha de promo OFF na data-fim; evergreen segue** — ele nunca desligou. Budget realocado de volta pro evergreen no nível pré-janela (o ad-log tem o número exato de antes).
4. **Leitura do evergreen reinicia limpa:** sazonalidade que mudou a demanda é o caso (b) das exceções do §5 — "new reason to be scaling": o histórico de degraus da janela não trava nem acelera o passo novo; a 12 retoma o protocolo normal do zero de leitura.
5. **Janeiro não é férias de ads** pra supplements/health & wellness: "Q5" — o gasto de saúde sobe ~35-40% e a fonte manda não tirar o pé em dezembro.

Linha no ad-log: "promo fim — [evento], rule disparou / desligado manual". `landing` gravado no `dados.json` e `manifest.promo.active: false`.

### ETAPA 10 — Leitura pós-promo e o cofre sazonal

**Handoff nomeado pra 11 (a leitura):** a análise datada da janela é da 11 — esta skill entrega a janela demarcada (`window`) e o ad-log completo (é ele que separa "efeito da promo" de "mudança sem efeito"). Duas lentes obrigatórias no brief pra 11: (a) CPM de temporada — novembro encarece tudo, queda de eficiência pós-janela não é fadiga automática; (b) **Lucky vs Durable** (rode `lucky wins vs durable wins spend concentration promote to control`) — winner de promo nasceu em condição temporária (oferta + urgência + demanda de data): **não promova a control evergreen automaticamente**; o que sobrevive com a oferta normal é durable, o resto é sazonal.

**Handoff nomeado pra 15 (o cohort da promo):** clientes adquiridos em nov/dez se comportam diferente — compram presente, e o LTV é atípico (pior, na experiência da fonte). Ao fechar o mês: (a) o mês da janela entra nas `monthly_notes[]` da 15 ("promoção no site inteiro" é literalmente o exemplo canônico da 15); (b) o cohort da janela é marcado pra **não calibrar o decay** sem a nota — comparar cohort de promo com cohort de junho quebra o modelo; (c) assinaturas vendidas na janela sem histórico de LTV → a decisão foi por lucro no pedido, e a régua de payback normal volta a valer nos meses seguintes. Rode `cohort de promo novembro dezembro LTV atípico clientes de presente calibragem`.

**Forecast do ano seguinte (o dado da SUA marca vence o da fonte):** grave em `result` o que funcionou — oferta (se dollar-off ganhou de percentage-off NA SUA marca, ano que vem use o seu dado), criativos, datas reais de abertura, curva por dia, novos vs. recorrentes. É a primeira coisa que a próxima rodada desta skill lê.

**O cofre sazonal (`seasonal_vault[]`):** todo criativo que performou na janela entra com `creative_id`, época, mês de religar e nota — porque **ads sazonais que morreram voltam no mesmo período do ano** (rode a query de Revival do núcleo). O timing de religar vem do **Desire Calendar**: outubro-dezembro pro Q4; meados de janeiro pro Valentine's (a compra é FOR, não ON); e assim por diante. Religar = re-banner (a oferta do ano novo é outra). A 12 e a 14 leem o cofre — é o handoff que transforma uma janela boa em patrimônio recorrente.

### ETAPA 11 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. `promo_economics.status` é `computed` antes de qualquer item em `campaigns[]`, brief pra 08 ou calendário pra 13 — ou é `blocked_pending_inputs` com `pending_inputs[]` preenchido e as ETAPAs 5-8 ausentes do relatório (sem seção vazia narrando a ausência — rule `report-only-results.md`).
2. `breakeven_roas_promo` > `breakeven_roas` evergreen sempre que `desconto_efetivo > 0` (se não for, a conta está errada).
3. Nenhum número sem custo fixo subtraído foi rotulado "lucro" — sem a 15, o rótulo é margem de contribuição, dito com todas as letras (§1).
4. Toda instrução de subida de budget da janela saiu com o valor de reset da meia-noite junto, e os resets estão em `scaling_window.midnight_resets[]`.
5. Nenhuma régua do Scaling Protocol foi redefinida — exceções e reset citam `.claude/lib/ad-taxonomy/README.md` §5.
6. `window.end` > `window.start`; a rule de desligamento aponta exatamente pra `window.end`; o automatic discount tem início e fim agendados.
7. Divisão respeitada: zero asset de email/SMS gerado aqui (13) e zero asset de criativo gerado aqui (08) — só brief e calendário.
8. Copy consumidor-final em inglês US; texto de banner/oferta confere com a matemática do desconto efetivo (stacking recalculado do compare-at); compare-at price não inflado; "up to" só com desconto não-uniforme; regras 8a/8b aplicadas.
9. Toda mudança executada na conta durante a rodada tem linha correspondente no `ad-log.md`, gravada no momento da execução.
10. Estruturas criadas via MCP nasceram PAUSED e rules nasceram desativadas; nada foi ativado pela skill.
11. Queries à base usam `best_query` byte-exata do índice; conteúdo ainda sem entrada usa o marcador `[query provisória — indexar]` — nunca query genérica inventada.
12. O relatório contém só o resultado (rule `report-only-results.md`) e o dual output foi gerado (.md + .html; `dados.json` isento).

## Output Schema — `17-promo-engine/promo-engine.md` + `17-promo-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills 08, 11, 12, 13, 14 e 15.

```json
{
  "promo_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "currency": "USD",
  "event": "bfcm | holiday_tail | valentines | mothers_day | labor_day | fall_halloween | flash | custom",
  "event_name": "Black Friday Sale 2026",
  "window": {
    "start": "2026-11-02",
    "end": "2026-12-01T00:00:00",
    "ad_account_timezone": null,
    "phases": [
      { "phase": "early_sale | bf_weekend | cyber_monday | holiday_tail", "start": "", "end": "" }
    ]
  },
  "prep": {
    "evergreen_momentum": { "breakthroughs_live": 0, "assessment": "conta com momentum | conta fria — expectativa ajustada" },
    "offer_contrast": { "evergreen_offer": "", "distance_plan": "store_credit_layer | price_up_then_down | degrade_after | ok" },
    "vip_leadgen": {
      "decision": "skip | run",
      "criteria": { "returning_rate": null, "organic_share_high": null, "unique_brand": null },
      "calculator": { "total_spend": null, "cpl_max": null, "aov_vip": null, "cvr_assumed": null, "offer_margin_with_vip_discount": null, "breakeven_roas": null, "projected_leads": null, "projected_revenue": null }
    },
    "inventory": { "source": "sourcing/dados.json", "volume_confirmation_30_60_90": null, "reorder_point_days": null, "fallback": "none | preorder" },
    "ops_backups": { "owner": "19-ops-engine", "member_has": [], "gaps": [] },
    "site_ready": { "automatic_discount_scheduled": false, "savings_visible_everywhere": false, "qa_done": false, "dev_on_standby": false }
  },
  "offer": {
    "core_type": "percent_off | dollar_off | buy_x_get_x_free | buy_x_gift_x | store_credit | avatar_specific | quiz | free_express_shipping",
    "headline_language_en": "25% off EVERYTHING",
    "stack": [],
    "discount_effective_pct": null,
    "compare_at_math_verified": false,
    "bf_weekend_bonus": null,
    "holiday_tail_offer": null,
    "vip_offer": null,
    "store_credit": { "face_value": null, "real_cost": null, "breakage_assumed_pct": null },
    "sale_reason_declared": ""
  },
  "promo_economics": {
    "status": "computed | blocked_pending_inputs",
    "source_fields": ["manifest.target_cpa | 04-offer-builder/dados.json | member"],
    "aov_expected_full": null,
    "discount_effective_per_order": null,
    "aov_promo": null,
    "margin_per_order_promo": null,
    "margin_rate_promo": null,
    "gross_margin_promo_pct": null,
    "floor_check": "above_60 | between_55_60 | below_55_redesign",
    "breakeven_roas_promo": null,
    "breakeven_cpa_promo": null,
    "target_cpa_promo": null,
    "breakeven_roas_with_fixed_promo": null,
    "kpi_of_the_window": "blended_roas",
    "blended_caveat": "organic_share_high → decidir por click-based/incremental"
  },
  "campaigns": [
    {
      "name": "", "role": "promo_cbo", "ad_sets": ["broad", "warm60", "hot90"],
      "budget_initial_daily": null, "budget_share_of_total_pct": null,
      "created_via": "mcp_official | mcp_pipeboard | manual", "status": "PAUSED",
      "end_rule": { "created": false, "active": false, "fires_at": "" },
      "campaign_id": null, "ad_set_ids": []
    }
  ],
  "creative_brief_08": {
    "priority": ["winner_plus_banner", "product_photo_plus_offer_statics", "seasonal_revival_rebanner", "early_scarcity", "complements"],
    "best_ad_source": "manifest.ad_classification breakthrough | spend_winner | none → statics only",
    "banner_copy_en": "", "subtle_callout_test": true,
    "bfcm_wording_on_friday_creatives": "Black Friday Cyber Monday Sale",
    "batches_planned": "2-3 (~9-12 statics/semana)",
    "revival_candidates": [],
    "handed_off": false
  },
  "email_sms_calendar_13": {
    "phases": [], "send_windows": [], "segments_guidance": "", "creative_by_phase_awareness": "",
    "vip_warmup_flow_included": false, "cutoffs_confirmed_with_ops": false, "handed_off": false
  },
  "scaling_window": {
    "governed_by": ".claude/lib/ad-taxonomy/README.md §5 (exceção a; surf + reset)",
    "attribution_tool": "triple_whale | northbeam | hyros | meta_only_low_spend",
    "surf_cadence_hours": null,
    "period_sheet_timezone": "ad_account",
    "decision_order": "blended_first_then_per_campaign",
    "midnight_resets": [ { "date": "", "spent_real": null, "reset_to": null, "logged_in_ad_log": true } ]
  },
  "landing": {
    "end_rule_fired_or_manual": null, "post_cyber_dip_managed": null,
    "holiday_tail_offer_live": null, "evergreen_budget_restored_to": null,
    "protocol_restart_note": "sazonalidade = new reason (§5 exceção b) — leitura do evergreen reinicia limpa"
  },
  "result": {
    "revenue_window": null, "spend_window": null, "blended_roas_window": null,
    "contribution_margin_window": null, "operating_income_window": null,
    "new_customers": null, "returning_share": null,
    "offer_winner_note": "", "curve_by_day": [],
    "promo_cohort_flagged_for_15": false,
    "next_year_notes": ""
  },
  "seasonal_vault": [
    { "creative_id": "", "period": "bfcm", "revive_month": "novembro", "rebanner_required": true, "note": "" }
  ],
  "handoff": {
    "for_skill_08": ["creative_brief_08"],
    "for_skill_11": ["window", "scaling_window.midnight_resets", "result.curve_by_day"],
    "for_skill_12": ["window", "promo_economics.breakeven_roas_promo", "landing.evergreen_budget_restored_to", "seasonal_vault"],
    "for_skill_13": ["email_sms_calendar_13", "offer", "window.phases"],
    "for_skill_14": ["seasonal_vault"],
    "for_skill_15": ["result.promo_cohort_flagged_for_15", "result.revenue_window", "result.spend_window"]
  },
  "pending_inputs": [],
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

**Campos que a skill NUNCA preenche por estimativa:** `promo_economics.margin_per_order_promo` (e derivados), `prep.vip_leadgen.calculator.offer_margin_with_vip_discount` e `prep.inventory.volume_confirmation_30_60_90`. Faltando, o campo fica `null`, entra em `pending_inputs[]` e o bloco dependente fica bloqueado — nunca preenchido com plausível.

## Contrato de leitura (quem lê o quê)

**Quem já lê hoje:**

| Skill | Campo que já lê | O que muda |
|---|---|---|
| **12** scale-engine | `manifest.promo.active` (+ o resumo `manifest.promo`) | A exceção (a) do §5 só vale com janela registrada e ativa; na aterrissagem (`active: false`) a leitura do evergreen reinicia limpa |
| **15** finance | `result.promo_cohort_flagged_for_15` + números da janela | O mês da promo ganha nota obrigatória e o cohort não calibra decay sem ela |

**Disponível para (leitura aditiva)** — dados publicados que as skills podem puxar quando fizer sentido, sem que já leiam hoje:

| Skill | Campo disponível | O que permite |
|---|---|---|
| **08** creatives | `creative_brief_08` | O batch de sale nasce do brief (banner sobre o winner + statics de oferta), não de ideação evergreen |
| **11** ad-analysis | `window`, `scaling_window.midnight_resets`, `result.curve_by_day` | A janela demarcada separa efeito de promo de fadiga (o `ad-log.md` a 11 já lê sempre, por cânone); winner de janela passa pelo filtro Lucky vs Durable antes de virar control |
| **12** scale-engine | `window`, `promo_economics.breakeven_roas_promo`, `landing.evergreen_budget_restored_to`, `seasonal_vault` | A volta pro evergreen usa o budget pré-janela do ad-log; o cofre alimenta revival |
| **13** retention | `email_sms_calendar_13`, `offer`, `window.phases` | Os sends sazonais nascem do calendário desta skill quando o membro roda 'retention'; flows se adaptam à promo sem desligar |
| **14** content-recycler | `seasonal_vault` | Winners sazonais entram na reciclagem com timing de religar |

Quando `17-promo-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — leitura aditiva, nunca pré-requisito.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `promo-engine.md` → `promo-engine.html`). **Isento** (arquivo operacional — rule 6b): `dados.json`. Use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, **logo SVG do Aura na topbar copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**, componentes aura).

**Garantir diretório:** `mkdir -p workspace/[produto]/17-promo-engine/` antes de salvar.

Outputs em `workspace/[produto]/17-promo-engine/`:

- **`promo-engine.md`** contendo, nesta ordem:
  1. A janela: evento, datas, fases e o porquê do início cedo (ETAPA 1)
  2. Preparação: momentum, decisão VIP com a calculadora, estoque, pointer de backups, site (ETAPA 2)
  3. A oferta: core, stack com a matemática conferida, linguagem, bônus do pico e cauda degradada (ETAPA 3)
  4. **Os números recalculados da janela** — margem promocional, breakeven ROAS/CPA promo, target, piso de margem (ETAPA 4)
  5. Estrutura de campanha e budget inicial, com o status PAUSED e o que o membro ativa (ETAPA 5)
  6. Brief de criativo entregue à 08 (ETAPA 6)
  7. Calendário de email/SMS entregue à 13 (ETAPA 7)
  8. Plano de escala da janela: cadência de surf, curva do fim de semana, resets (ETAPA 8)
  9. Aterrissagem: rule de fim, cauda, volta pro evergreen (ETAPA 9)
  10. Pós-promo: leitura, cohort flagado, cofre sazonal e notas pro ano que vem (ETAPA 10)
  11. Pendências: o que falta e o que destrava — sem narrar tentativas

  Rodada bloqueada no gate: os itens 5 a 9 simplesmente não aparecem (rule `report-only-results.md` — sem seção vazia, sem descrever ausência).

- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:

- Adicionar `17-promo-engine` em `skills_completed` (id canônico desta skill, padrão `NN-nome` do schema)
- Gravar **`manifest.promo`** = `{ event_name, window_start, window_end, breakeven_roas_promo, target_cpa_promo, active, checked_at }` — o resumo que a 11 e a 12 leem sem abrir o `dados.json` inteiro; `active: true` na abertura, `false` na aterrissagem
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- **NÃO** sobrescrever `manifest.target_cpa`/`manifest.breakeven_roas` (são os números do EVERGREEN; os da janela vivem em `manifest.promo` e morrem com ela)
- Regenerar o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>`

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`). Adapte ao stage (`member-stage-awareness.md`): starter recebe a explicação do porquê; scaling recebe o plano direto.

**Rodada completa (gate fechado):**
"Janela montada: **[evento]**, de **[início]** a **[fim]** — começando cedo de propósito: quem abre primeiro captura quem já ia comprar, e o pico fica só pra escalar.
A oferta é **[oferta]**, e o número que muda tudo: com ela, seu breakeven ROAS deixa de ser **[X]×** e vira **[Y]×** (CPA máximo de **US$ [Z]**). É esse número que a janela inteira respeita — receita recorde com margem furada é o erro clássico da temporada, e a gente já o tirou da mesa.
A campanha de promo (Broad/WARM60/HOT90) está criada **em PAUSED** — revisa e ativa; o evergreen não muda. O brief de criativo está pronto pra 08 (**'creatives'**) e o calendário de email pra 13 (**'retention'**).
Durante a janela: me chama **todo dia** — a régua de surf e o reset da meia-noite saem daqui com o número exato, e cada mudança fica registrada. Na data-fim, a rule desliga tudo sozinha (ativa ela antes) e eu te devolvo pro evergreen com a leitura do que a janela ensinou."

**Rodada bloqueada no gate:**
"Calendário e oferta desenhados — mas **não vou ligar nada ainda**, e o motivo é o único inegociável desta skill: sem recalcular sua margem com o desconto dentro, escalar a promo é fazer mais receita com menos lucro sem perceber. Me falta: **[pending_inputs]**. Me passa que eu fecho o breakeven da janela e destravo campanha, criativos e emails na mesma rodada."

**Membro chega em cima da hora (janela a dias de abrir):**
"Dá pra rodar, com as prioridades certas pra quem está em cima da hora: números recalculados primeiro (inegociável), campanha de promo com winner + banner (criativo de sale não precisa de semanas), automatic discount agendado e a rule de fim criada. O que não dá mais tempo de fazer bem — [lead-gen VIP / teste de messaging / photoshoot] — fica registrado pro ano que vem, que começa em setembro."
