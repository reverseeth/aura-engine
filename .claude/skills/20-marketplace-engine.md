---
name: marketplace-engine
description: Expansão de CANAL DE VENDA além do site próprio — decide quando (e se) a marca abre Amazon, TikTok Shop e programa de afiliados, e acompanha cada canal aberto. Roda um GATE antes de qualquer tática — Meta + site provados primeiro (breakthrough na 11, conta fechando na 15) e sinal de demanda transbordando (busca de marca subindo, cliente procurando a marca na Amazon, revendedor aparecendo na listagem) — porque canal novo não conserta oferta quebrada. Amazon como captura da demanda que o ad já criou (SEO da listagem, defesa de marca, lances baixos, preço riscado, custom link, TACOS); TikTok Shop como canal de venda operado por afiliados (comissão orgânica vs de ads, samples, GMV, incentivos de plataforma — o conteúdo em si é da skill 16); afiliados via tráfego pago (funil "apply to be brand ambassador", comissão decrescente por faixa) e clientes virando afiliados automaticamente. Portar campanha paga pra AppLovin/Axon/TikTok Ads é a skill 14 (Movimento 4), não esta. Use quando o membro disser "amazon", "tiktok shop", "marketplace", "afiliados", "expandir canal", "vender fora do site".
---

# Marketplace Engine

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md` — domínio `affiliate-creator-channels`, mais entradas de canal em `meta-ads-strategy`, `scaling` e `creatives-hooks-formats` marcadas pra esta skill). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` com a `best_query` curada de cada um. NUNCA query genérica.
>
> **Fronteira com as skills vizinhas — decorar antes de rodar:** esta skill é dona do **canal de venda** (onde o produto é vendido além do site). O que é **conteúdo e creator** (recrutar, gerenciar, produzir, testar volume orgânico) é da **skill 16 (creator-engine)**. O que é **portar campanha paga pra outra plataforma de mídia** (AppLovin/Axon, TikTok Ads) é da **skill 14, Movimento 4**. O que é **conta financeira por canal** (margem com comissão e fee dentro) é da **skill 15**. Esta skill decide e opera o canal; ela não produz criativo, não compra mídia e não fecha a conta financeira de canal nenhum.

## Quando Usar

Quando a pergunta é sobre **vender fora do site próprio**: "vale abrir Amazon?", "e TikTok Shop?", "como monto programa de afiliados?", "tem gente revendendo meu produto na Amazon". Gatilhos: "amazon", "tiktok shop", "marketplace", "afiliados", "expandir canal", "vender fora do site".

**Não é fase do pipeline — é consulta lateral, como a 15.** O momento natural é o estágio **scaling**: depois que a 11 classificou pelo menos um breakthrough estável e a 15 mostrou a conta fechando com o custo fixo dentro. Re-rodar é normal: a primeira rodada avalia canais (go/no-go); as seguintes atualizam status e métricas dos canais abertos.

**O que esta skill responde e nenhuma outra respondia:** quando abrir um canal de venda secundário, qual abrir primeiro, o que é preciso ter pronto antes de entrar, e como acompanhar cada canal aberto sem misturar a régua dele com a régua do Meta.

**O que ela NÃO faz:** não recruta nem gerencia creators (16), não escreve copy de listagem (06 dá as regras de escrita; aqui só a estrutura do canal), não estrutura campanha de mídia em plataforma nova (14 M4), não recalcula margem (15), não decide escala dentro do Meta (12).

## Antes de Começar

### report_language

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno usa esse idioma. Copy que vai pro consumidor final (texto de listagem, mensagem a creator em marketplace US) permanece em inglês, como sempre.

### Pré-flight

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] Prova de canal primário localizada: `manifest.ad_classification[]` com pelo menos um `breakthrough` (gravado pela 11), OU `manifest.finance` mostrando mês fechado saudável (gravado pela 15). **Sem nenhuma das duas, a skill RODA mesmo assim** — mas o gate da ETAPA 1 só pode sair `not_yet` ou `blocked_pending_proof`, nunca `expand`. Não é caso de abortar (rule `emergency-escape-paths.md`): a resposta honesta "ainda não, e falta X" é um output válido e útil.

### Contexto a carregar

1. `workspace/profile.md` — stage e budget (linguagem e apetite; ver `member-stage-awareness.md`). Membro `starter` ou `validating`: o veredito quase sempre é "ainda não" — dito sem rodeio, com o que destrava.
2. `workspace/[produto]/manifest.json` — `stage`, `ad_classification[]`, `manifest.finance` (se existir), `manifest.marketplace` (rodadas anteriores desta skill — canais já avaliados/abertos).
3. `workspace/[produto]/11-ad-analysis/dados.json` **(se existir)** — breakthroughs e winners: são a prova de que existe demanda criada pelo Meta pra transbordar.
4. `workspace/[produto]/15-finance-engine/dados.json` **(se existir)** — margem de contribuição e runway. A comissão de afiliado e a fee de marketplace entram como **custo variável do canal**: quem fecha essa conta é a 15, nunca esta skill.
5. `workspace/[produto]/03-competitor-analysis/dados.json` **(se existir)** — concorrentes já presentes em Amazon/TikTok Shop são leitura de sofisticação do canal.
6. Rodadas anteriores em `workspace/[produto]/20-marketplace-engine/`.

### Dados que a skill pede e nunca estima

| Dado | Onde o membro encontra |
|---|---|
| Busca de marca (volume/tendência) | Google Search Console (queries com o nome da marca) ou Google Trends do termo de marca; busca do nome da marca dentro do TikTok |
| Revendedor na Amazon | Buscar o nome da marca/produto na Amazon e olhar quem vende (o membro cola o que vê) |
| Fees reais do canal | Painel do canal (fee de venda da Amazon por categoria, fee do TikTok Shop) |
| GMV e métricas de canal aberto | Painel do canal — GMV é o total vendido dentro do canal |

Ferramentas pagas (Kalodata, FastMoss) seguem a regra dura da skill 01: **a AI nunca finge acessar ferramenta paga** — diz exatamente o que olhar e trata o retorno como dado colado pelo membro.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema. Abra o `frameworks.json` e enumere as entradas do domínio `affiliate-creator-channels` cujo `use_in_skill` inclui esta skill — 6 das 8 (Creator Farming e Whitelist Ads são território da 16/08/10 e não se puxam aqui). **Esta skill é a consumidora que faltava** dos sistemas de marketplace marcados como dormant no índice (`use_in_skill: "—"`) — a partir dela, eles são puxáveis.

**Do domínio `affiliate-creator-channels`:**

- **Marketplace como canal secundário (regra de entrada)** — `quando abrir marketplace como canal secundario Amazon TikTok Shop regra de entrada`
- **Amazon Playbook (SEO, ninja low-bid, slash-through, custom link, TACOS)** — `playbook Amazon SEO de listagem ninja low bid slash through custom link TACOS`
- **Operação de TikTok Shop** — `operacao de TikTok Shop samples afiliados comissao e conteudo`
- **Social Snowball (programa de afiliados automatizado)** — `Social Snowball programa de afiliados automatizado comissao por cliente`
- **Recrutamento pago de afiliados** — `recrutar afiliados com trafego pago apply to be brand ambassador`
- **Custom Link + atribuição de afiliado** — `custom link de afiliado atribuicao de venda por creator`

**De domínios vizinhos (entradas de canal marcadas também pra esta skill):**

- **"Não abra canal que você não domina"** _(meta-ads-strategy)_ — `não abra canal que você não domina enquanto há espaço no Meta branded search é defesa`
- **Google Search Stronghold + setup 80-20** _(meta-ads-strategy — o sinal de busca de marca)_ — `Google Search Stronghold branded search proteger a marca converter copy do Facebook`
- **Trademark + Facebook Brand Rights Protection** _(meta-ads-strategy — compartilhada com a 00)_ — `trademark registrado brand rights protection fake DMCA derrubou 300 ads`
- **Affiliate Recruitment via Paid Ads + TikTok Shop como máquina de conteúdo** _(scaling)_ — `rodar paid ads para recrutar afiliados save 40% apply to be brand ambassador TikTok Shop conteudo`
- **Brand Ambassador Ladder (retainer + comissão em degraus)** _(creatives-hooks-formats)_ — `retainer 500 por video semanal performance program regra do 2-3 comissao decrescente 10 5 2.5 1`
- **Creative Strategy em 9 Dimensões (a dimensão de canal de venda)** _(meta-ads-strategy)_ — `9 dimensoes self-audit business brand creative sales channel funnel production testing measurement`

## Fluxo da Skill

### ETAPA 1 — O gate de expansão (a decisão que vem antes de toda tática)

Canal secundário é agenda de quem já provou o canal primário. A regra da fonte primária é direta: **não abra canal que você não domina enquanto ainda há espaço no Meta** — antes de escala real, multi-canal é ruído, e um canal bem feito vale mais que três pela metade.

**Condição 1 — Meta + site provados.** Pelo menos um `breakthrough` classificado pela 11 (cânone `.claude/lib/ad-taxonomy/README.md` §2) OU mês fechado saudável na 15 (margem de contribuição cobrindo os fixos). Sem prova, o veredito é `blocked_pending_proof` e o relatório diz exatamente o que destrava.

**Condição 2 — sinal de demanda transbordando.** O canal secundário certo captura demanda que o canal primário já criou e não está convertendo. Os quatro sinais, na ordem de força:

| Sinal | Como ler |
|---|---|
| **Busca de marca subindo** | Gente pesquisando o NOME da marca no Google/TikTok é demanda que o ad criou. Se ela cresce, parte dela está indo comprar onde você não está. É o mesmo sinal que sustenta a campanha de busca de marca (Google Search Stronghold) — quando ele fica forte, marketplace é o próximo lugar onde essa demanda vaza. |
| **Cliente perguntando pelo canal** | Comentário e DM do tipo "tem na Amazon?" é o transbordo dito com todas as letras. |
| **Revendedor ou sequestro de listagem** | Alguém já vende seu produto na Amazon sem você. Além de sinal de demanda, é urgência de defesa (ETAPA 2). |
| **Lift cruzado observado** | Quem já tem um segundo canal vê o efeito: anúncio num canal eleva venda no outro. Ads de TikTok Shop elevam vendas na Amazon; marca com varejo físico vê o varejo subir por dólar gasto no TikTok Shop. |

**Anti-sinal (bloqueia sozinho):** abrir canal novo pra **fugir** de CAC ruim, criativo cansado ou oferta que não converte no Meta. Canal novo herda a oferta — não a conserta. Se o motivo declarado do membro é esse, o veredito é `not_yet` com o encaminhamento certo (11 pra diagnóstico, 04 pra oferta, 15 pra conta).

**Timing por referência de faixa:** operadores em escala colocam a entrada na Amazon tipicamente entre o DTC validado e a faixa de US$ 1-3M/mês — e o arrependimento mais comum relatado é ter aberto **tarde**, porque com volume no DTC a busca orgânica da marca na Amazon já performa sem anúncio (margem quase pura sendo perdida todo mês). O sinal que manda é a busca de marca, não a receita em si.

Grave `gate.verdict` (`expand` / `not_yet` / `blocked_pending_proof`) e os sinais marcados. Só `expand` libera as ETAPAs 2-4 como avaliação de entrada; com `not_yet`, as etapas seguintes só rodam para canais JÁ abertos (atualização de status).

### ETAPA 2 — Amazon: capturar a demanda que o ad criou

**O racional.** O pool de compradores da Amazon é quase separado do seu site: a maioria dos compradores de Amazon só compra lá. Seu ad no Meta cria a demanda, a pessoa pesquisa na Amazon — e 9 em cada 10 visitas ao app terminam em compra. Sem listagem sua, essa venda vai pro concorrente ou pro revendedor, paga com o SEU ad. Por isso adicionar Amazon costuma somar na casa de +50% sobre a receita do site sem canibalizar, e a margem do canal é quase pura quando a busca orgânica da marca já existe.

**O essencial de entrada (nesta ordem):**

1. **Marca protegida ANTES da listagem.** Registro de marca + Brand Registry (o cadastro oficial de marca da Amazon, que exige a marca registrada) são o que permite tirar revendedor da sua listagem e travar sequestro. Uma listagem famosa de água engarrafada chega a ter ~148 vendedores diferentes — sem registro, esse é o teto do risco. A régua de proteção é das skills **00 (setup) e 19 (proteção de marca)**: se `trademark` não consta no manifest, esta skill marca a pendência e aponta pra lá, sem duplicar o protocolo.
2. **Listagem com SEO primeiro, anúncio depois.** O orgânico carrega mais que o pago no canal — busca com intenção de compra e custo por venda zero (só a fee). A mecânica do algoritmo tem 3 camadas: a keyword precisa bater com o produto → a imagem principal decide o clique → o produto alinhado com a busca decide a compra (imagem chamativa com produto desalinhado é punido como enganoso). Selos criativos na imagem principal ("viral on TikTok") sobem o clique.
3. **Base de prova.** Amazon exige construção de marca real: reviews, logística FBA (o braço da Amazon que armazena e entrega por você), cadastro de marca. Chegue com o plano de reviews definido antes de ligar tráfego pro canal — listagem sem prova perde a compra pra quem tem.
4. **Preço riscado (slash-through).** Configurar preço de tabela + preço promocional no painel: concorrente a US$ 9 sem desconto perde pra US$ 15 riscado por US$ 9 — percepção de premium e de negócio ao mesmo tempo.
5. **Anúncios internos com lance baixo (ninja low-bid).** O leilão da Amazon tem buracos sem competição: lance de metade do sugerido ainda pega volume (referências reais: US$ 0,25-0,55 de custo por clique pagando 8-35× de retorno). Alvos: página do produto concorrente, os 10 termos de busca principais, **a própria listagem** (defesa de marca — senão o concorrente paga centavos pelas SUAS keywords), o resto do próprio catálogo e o bloco "comprados juntos".
6. **Custom link pra tráfego externo.** A Amazon reduz a fee da venda atribuída a link seu (ex.: de 25% pra 8%) — e a listagem costuma converter melhor que o site (7% vs 5% é referência da fonte). Mandar ad direto pra Amazon vira decisão de rota legítima; quem fecha essa conta (fee menor vs margem do site) é a 15.
7. **Régua do canal.** TACOS — o gasto com anúncio como porcentagem da receita TOTAL do canal — é a métrica de eficiência da Amazon; TROAS (o retorno sobre gasto de anúncio medido DENTRO da Amazon) de 15-25× é rotina lá **e não se compara com ROAS do Meta** (leilões e papéis diferentes). Acompanhar também LTV/CAC do canal (referência saudável: ~6×) e separar cliente de promoção de cliente que volta.
8. **Dois aproveitamentos que quase ninguém usa:** a Amazon é obrigada a entregar, uma vez por ano, a lista de compradores com nome e endereço — cruzada com busca de email, vira lista própria (handoff pra 13). E a operação não exige olhar 5× ao dia como o Meta — exige conhecer os botões certos: internalizar a gestão cedo demais já custou US$ 700k num mês a uma marca de referência; até dominar, especialista/agência.

### ETAPA 3 — TikTok Shop: o canal de venda operado por afiliados

**O que é.** Venda nativa dentro do app, movida por uma rede gigante de afiliados: creators publicam com a tag do produto, a venda é rastreada na plataforma e a comissão é paga por lá. Categorias fortes: consumíveis, beleza, saúde/bem-estar, casa. Difícil: moda (competição de preço). Só produto físico.

**A mecânica que esta skill opera:**

- **Comissão em dois níveis:** orgânica ALTA (~40% — equivale a ~2,5× de retorno) pra atrair creator bom; comissão de ads BAIXA (5-10%), porque a amplificação paga já custa. Trate a comissão como o **CAC permitido do canal**: cada venda deve ser lucrativa ou empatar como aquisição. Comissão agressiva é deliberada — força volume de conteúdo, e o conteúdo vale mais que a margem cedida.
- **Samples:** envio de produto pra creator gravar é o custo de entrada do fluxo; sem sample não há vídeo.
- **GMV transparente e bootstrap:** todo creator vê quanto sua loja vendeu nos últimos 30 dias — loja zerada não atrai ninguém. Bootstrap: rodar promo pra lista própria de email empurrando a transação pro TikTok Shop + um pouco de ads da plataforma, até o número destravar creator maior.
- **Limite de contatos de recrutamento (outreach — ~1.000/semana pra marca nova):** cada creator contatado vale mais — nutrir e extrair mais vídeos de cada um em vez de testar e descartar.
- **Incentivos de plataforma (janela que fecha):** co-financiamento do desconto (você dá 20% off, a plataforma paga metade), campanhas de busca no Google pagas pela plataforma pro seu produto, onboarding assistido pra marcas maiores. Quanto mais cedo entrar, mais se aproveita — o histórico das plataformas mostra que incentivo de fase inicial some.

**Expectativa honesta (a fonte é explícita):** TikTok Shop raramente é centro de lucro. É canal de venda **e** máquina de demanda: o retorno composto vem de (a) **halo de busca** — o volume de conteúdo faz a busca do nome da marca subir dentro do TikTok, e as gerações mais novas pesquisam produto lá antes do Google; (b) **lift cruzado** — ads do canal elevam vendas na Amazon e no varejo; (c) **acervo de criativo** — a operação é PAGA pra gerar conteúdo (600 vídeos num mês, num caso de referência) que abastece os ads do Meta. "A maioria gasta dinheiro pra ter conteúdo; aqui você ganha dinheiro pra ter conteúdo."

**Divisão de trabalho com a 16 (creator-engine):** a 16 recruta, gerencia e produz — creator farming, o teste de volume orgânico (spam test) que valida conceito antes de mídia paga, whitelisting. Esta skill define comissão, samples, meta de GMV e o go/no-go do canal. Quando as duas rodam, é o mesmo exército de creators servindo os dois lados: a 16 entrega o conteúdo que sustenta as vendas daqui; daqui saem os winners orgânicos que a 16 devolve pro Meta.

### ETAPA 4 — Afiliados via tráfego pago (e clientes virando afiliados)

**O sistema de recrutamento pago.** Rodar ad que vende a **oportunidade**, não o produto: "save 40% on your first order when you apply to be a brand ambassador" → formulário de candidatura → código de desconto → primeira compra. A aquisição de afiliado vira um funil pago próprio — e pode ser **lucrativa na aquisição**, porque o candidato também compra. Referências da fonte: marca de skincare que não crackeava ads de resposta direta (0,2× de ROAS) rodava recrutamento de afiliadas a 2,5×; o melhor criativo de recrutamento é o creator bem-sucedido contando a própria história pelo perfil dele (whitelisting — ponte com 16/08).

**Quando vale:** depois do funil próprio provado (gate da ETAPA 1), e especialmente em **marca de identidade** (moda, joias, lifestyle) — nesses nichos o motor de crescimento dominante é marca + produto + exército de afiliados, e insistir no playbook de resposta direta de supplement é lutar a luta errada.

**Comissão decrescente por faixa — nunca % fixa pra sempre:**

- **10% dos primeiros US$ 10.000** gerados (receita ou ad spend da whitelisted ad do creator) → **5%** da faixa seguinte → **2,5%** → **1%** acima, com **teto mensal** (ex.: US$ 10.000). Versão simplificada com cap: "10% dos primeiros US$ 5k".
- A base pode ser % de RECEITA ou % de AD SPEND — split-testar as duas.
- O desenho protege os dois lados: o creator ganha forte nos primeiros dólares (motivação), a marca protege a margem quando o ad explode. Em volume alto, retainer simples escala melhor que % do spend.

**Clientes viram afiliados sem fricção.** A versão orgânica do mesmo jogo: conta de afiliado criada automaticamente na compra, código exibido na thank-you page (sem formulário, sem aprovação manual), lembretes por email/SMS e pelo atendimento depois de resolver um problema. Benchmark da fonte: só com clientes, 5-9% do GMV com ~5× de retorno do programa (caso de referência: marca de meias). Ferramenta que automatiza a apuração por cliente: Social Snowball (também cobre o programa do TikTok Shop).

**Atribuição é pré-condição:** link/código único por afiliado — sem isso não há comissão certa nem comparação entre parceiros, e o programa apodrece em disputa.

**A conta:** comissão é **custo variável do canal** — muda breakeven e CPA-alvo daquele canal, e não sai daqui: handoff pra 15 com as taxas registradas.

### ETAPA 5 — Sequência, plano por canal e veredito

**Um canal novo por vez.** Abrir dois ao mesmo tempo divide atenção e mata os dois. A ordem default quando mais de um canal passou no gate:

1. **Amazon primeiro** quando a busca de marca já cresce — é captura de demanda existente, o retorno mais rápido e a defesa mais urgente (revendedor não espera).
2. **TikTok Shop** quando a categoria é forte no social e a operação suporta o fluxo de creators (com a 16 rodando) — é geração de demanda + acervo, retorno mais composto e mais lento.
3. **Programa de afiliados** como camada sobre canal já rodando (site ou TikTok Shop) — em marca de identidade, pode subir na fila.

Para cada canal com `go`: registrar o plano de entrada resumido (requisitos, fees/comissões, dono, primeira meta), e para cada canal já aberto: atualizar status e métricas com a régua DO CANAL (TACOS/LTV-CAC na Amazon; GMV/comissão efetiva/afiliados ativos no TikTok Shop; % do GMV e retorno no programa de afiliados). Métrica que o membro não passou fica `null` e entra em `pending_inputs[]` — nunca preenchida com plausível.

**Fora do escopo — dito no relatório quando o membro pedir:** levar a CAMPANHA paga pra AppLovin/Axon ou TikTok Ads é expansão de canal de **mídia**, não de venda — é a skill **14, Movimento 4** (régua de US$ 250-1.000/dia por 60-90 dias pra crackear canal de mídia). Se o pedido do membro é esse, encaminhe sem rodar esta skill inteira.

### ETAPA 6 — Checagens de sanidade

Antes de salvar, confirme cada item. Falha em qualquer um bloqueia o salvamento do `.md` até correção.

1. Nenhum canal com `verdict: "go"` sem `gate.verdict: "expand"` na mesma rodada.
2. O anti-sinal foi checado: nenhuma recomendação de canal novo motivada por fuga de CAC/criativo/oferta ruim no Meta.
3. Amazon com `go` e marca sem registro → a pendência de proteção (00/19) está marcada e aparece no relatório antes de qualquer tática de listagem.
4. Toda comissão e fee de canal com `go` está registrada em `fees_and_commissions` e no handoff pra 15 — e nenhuma frase do relatório chama de "lucro do canal" um número que não passou pela 15.
5. Nenhuma métrica de canal foi estimada; ausentes estão em `pending_inputs[]`.
6. Nada de plano de creator/conteúdo aqui (recrutamento, roteiro, volume de posts) — só requisitos de canal; conteúdo aponta pra 16.
7. TROAS/retorno de anúncio interno da Amazon não foi comparado com ROAS do Meta em nenhuma tabela.
8. O relatório contém só o resultado (rule `report-only-results.md`) — sem narração de processo, sem descrição de ausências.

## Output Schema — `20-marketplace-engine/marketplace-engine.md` + `20-marketplace-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills 12, 13, 15 e 16.

```json
{
  "marketplace_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "run_type": "evaluation | status_update",
  "gate": {
    "meta_site_proven": null,
    "proof_source": "manifest.ad_classification | 15-finance-engine | member_declared | none",
    "signals": {
      "brand_search_rising": null,
      "customers_asking_marketplace": null,
      "resellers_or_hijack_detected": null,
      "cross_channel_lift_observed": null
    },
    "anti_signal_flight_from_meta": false,
    "verdict": "expand | not_yet | blocked_pending_proof",
    "verdict_reason": "frase em report_language com o sinal decisivo",
    "next_review_trigger": "ex.: busca de marca no Search Console > X/mês, ou 1º breakthrough na 11"
  },
  "channels": [
    {
      "channel": "amazon",
      "verdict": "go | no_go | not_yet | not_evaluated",
      "reasons": [],
      "entry_requirements": {
        "trademark_registered": null,
        "brand_registry_active": null,
        "reviews_plan_defined": null,
        "fulfillment": "fba | fbm | undefined"
      },
      "fees_and_commissions": {
        "referral_fee_pct": null,
        "custom_link_fee_pct": null,
        "fulfillment_cost_per_order": null
      },
      "status": "not_evaluated | preparing | live | paused",
      "metrics": { "revenue_monthly": null, "tacos_pct": null, "ltv_to_cac": null, "organic_share_pct": null },
      "owner": "member | agency | specialist | undefined",
      "opened_at": null
    },
    {
      "channel": "tiktok_shop",
      "verdict": "go | no_go | not_yet | not_evaluated",
      "reasons": [],
      "commission_organic_pct": null,
      "commission_ads_pct": null,
      "samples_policy": null,
      "bootstrap_plan": null,
      "status": "not_evaluated | preparing | live | paused",
      "metrics": { "gmv_monthly": null, "active_affiliates": null, "effective_commission_pct": null, "brand_search_in_platform": null },
      "content_dependency": "16-creator-engine",
      "opened_at": null
    },
    {
      "channel": "affiliate_program",
      "verdict": "go | no_go | not_yet | not_evaluated",
      "reasons": [],
      "paid_recruitment": { "active": null, "recruitment_offer": null, "recruitment_roas": null },
      "customer_affiliates": { "active": null, "enrollment": "thank_you_page_auto | manual | none" },
      "commission_ladder": [
        { "tier": "primeiros_usd", "up_to_usd": 10000, "pct": 10 },
        { "tier": "faixa_2", "up_to_usd": null, "pct": 5 },
        { "tier": "faixa_3", "up_to_usd": null, "pct": 2.5 },
        { "tier": "acima", "up_to_usd": null, "pct": 1 }
      ],
      "commission_base": "revenue | ad_spend | undefined",
      "monthly_cap_usd": null,
      "attribution": "per_affiliate_link_or_code | undefined",
      "status": "not_evaluated | preparing | live | paused",
      "metrics": { "affiliate_gmv_share_pct": null, "program_roi": null },
      "opened_at": null
    }
  ],
  "sequence_recommendation": [],
  "out_of_scope_redirects": [
    { "request": "portar campanha pra AppLovin/Axon/TikTok Ads", "goto": "14-content-recycler (Movimento 4)" }
  ],
  "handoff": {
    "for_skill_15": ["channels[].fees_and_commissions", "channels[].commission_organic_pct", "channels[].commission_ladder"],
    "for_skill_16": ["channels[tiktok_shop].commission_organic_pct", "channels[tiktok_shop].samples_policy", "channels[tiktok_shop].metrics.gmv_monthly"],
    "for_skill_12": ["gate.verdict", "channels[].status"],
    "for_skill_13": ["amazon buyer list anual (cross-match de email)", "compradores de marketplace pro ecossistema de email/SMS"]
  },
  "pending_inputs": [],
  "sanity_checks": { "total": 8, "passed": 8, "failed": [] }
}
```

Os valores do exemplo (escada de comissão inclusive) são o default da fonte — ajuste às faixas reais que o membro definir.

## Contrato de leitura (quem lê o quê)

| Skill | Campo que passa a ler | O que muda |
|---|---|---|
| **12** scale-engine | `gate.verdict`, `channels[].status` | Canal `live` entra nas projeções como fonte incremental (mesmo padrão do `manifest.agentic`), nunca como premissa de caixa. |
| **15** finance-engine | `channels[].fees_and_commissions`, comissões | A margem por canal (fee/comissão como custo variável) entra no modelo — cada canal age como um mini negócio com a própria conta. |
| **16** creator-engine | comissão orgânica, política de samples, GMV do TikTok Shop | O motor de creators da 16 opera com os números de canal definidos aqui. |
| **13** retention-engine | handoff de compradores de marketplace | Lista anual de compradores da Amazon e clientes de TikTok Shop entram no ecossistema de email/SMS. |

Quando `20-marketplace-engine/dados.json` não existir, cada consumidora mantém o comportamento atual — a leitura é aditiva, nunca pré-requisito.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Todo relatório `.md` voltado ao membro DEVE gerar `.html` companion** com o mesmo nome (aqui: `marketplace-engine.md` → `marketplace-engine.html`). **Isento:** `dados.json`. Use `.claude/templates/aura-report-template.html` (CSS inline, self-contained, **logo SVG copiada LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto**).

**Garantir diretório:** `mkdir -p workspace/[produto]/20-marketplace-engine/` antes de salvar.

- **`marketplace-engine.md`** contendo, nesta ordem: (1) o veredito do gate com o sinal decisivo; (2) um bloco por canal avaliado — go/no-go, requisitos de entrada, fees/comissões e primeira meta (canal `not_evaluated` simplesmente não aparece); (3) sequência recomendada; (4) status e métricas dos canais abertos (rodadas de atualização); (5) pendências — o que falta e o que destrava, sem narrar tentativas.
- **`dados.json`** — schema acima.

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:

- Adicionar `20-marketplace-engine` em `skills_completed` (id canônico desta skill)
- Gravar `manifest.marketplace` = `{ gate_verdict, channels_live: [], amazon_status, tiktok_shop_status, affiliate_program_status, checked_at }` — o resumo que as outras skills leem sem abrir o `dados.json` inteiro
- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenerar o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>`

## Mensagem Final

Primeira versão é draft, não decreto (rule `iteration-driven-refinement.md`).

**Gate `expand`, com canal aprovado:**
"Avaliação de canais pronta. O sinal que abre a porta: **[sinal decisivo com número]**. Recomendo começar por **[canal]** — [razão em 1 frase]. Antes de listar qualquer coisa: [requisito pendente, ex.: registro de marca — skills 00/19]. A comissão/fee de **[X]%** muda a conta desse canal; diga **'finanças'** pra 15 fechar a margem por canal antes do primeiro dólar. Revisa o plano e me diz o que ajustar — abro um canal por vez, e o segundo só entra quando o primeiro estiver rodando sozinho."

**Gate `not_yet` / `blocked_pending_proof`:**
"Ainda não é hora de canal novo — e isso é uma conclusão, não um consolo. Falta: **[prova/sinal ausente]**. Canal secundário captura demanda que transborda; hoje a demanda ainda [não existe em volume / está sendo criada]. O que destrava: [ex.: primeiro breakthrough na análise de ads; busca de marca subindo no Search Console]. Quando qualquer um desses aparecer, roda **'marketplace'** de novo que eu reavalio."

**Rodada de status (canais abertos):**
"Status dos canais atualizado. [Canal]: [métrica-chave vs meta]. [Alerta ou próximo passo em 1 frase]. Me traz [dado pendente] do painel do canal que eu fecho a leitura do mês."
