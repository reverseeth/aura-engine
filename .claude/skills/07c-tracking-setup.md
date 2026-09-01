---
name: tracking-setup
description: Engine de instalação e validação de tracking pré-launch. Instala o Meta Pixel + Conversions API (CAPI) na loja, valida o Event Match Quality (EMQ) ≥ 6.0 na escala 0-10 do Events Manager (com o caminho pending_traffic pra loja pré-launch sem volume: instalação verificada + pedido-teste validando o Purchase destravam o launch com emq_pending), e escolhe o analytics stack correto por member-stage (Meta App / Wetracked / Triple Whale / Aimerce). Grava o bloco manifest.tracking que destrava os pré-flights da 08 e da 10. Roda DEPOIS do deploy da página (07b) e ANTES dos criativos (08). Use quando o membro disser "tracking", "pixel", "capi", "analytics setup", "configurar tracking", ou após a página estar no ar.
---

# Tracking Setup — Pixel + CAPI + Analytics Stack

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (`frameworks.json` / `README.md`). O índice lista **21 entradas** com `use_in_skill` incluindo a 07c — o bloco de atribuição/tracking, espalhado por 6 domínios: `meta-ads-strategy` (4), `scaling` (8), `retention-email` (5), `finance-projections` (2), `market-research-voc` (1) e `page-landing-cro` (1). Esta skill puxa os SISTEMAS NOMEADOS por `search_knowledge` (`deep=true`) com a `best_query` **byte-exata** de cada um, embutida no ponto de uso das ETAPAs abaixo. NUNCA query genérica.
>
> **Contrato de cobertura (kb-index README, revisado 2026-09):** no início de cada ETAPA que consulta a base, abra `frameworks.json` e enumere TODAS as entradas cujo `use_in_skill` inclui `07c`, conferindo contra as embutidas no texto — as queries embutidas são o **núcleo mínimo garantido da etapa, nunca o teto**; entrada relevante à fase que não está embutida é para ser puxada do mesmo jeito (a fonte da verdade da contagem é sempre o `frameworks.json`, nunca o número decorado aqui). Entrada duplicada entre domínios (o survey pós-compra do KnoCommerce aparece em `scaling` E em `market-research-voc`) aponta pro MESMO conteúdo — puxe uma vez e reuse. Antes de fechar cada ETAPA, releia a lista enumerada e confirme: sobrou entrada relevante sem puxar? Se sim, puxe agora.
>
> **Três entradas ficam de fora por decisão explícita** (o índice lista a 07c nelas, mas o ponto de uso real é a skill 13): **Arquitetura Confirmation → Self-Segmenter → Welcome**, **Hot-Time Anchor** e **Métricas de SMS (EPM / CTR / UNSUB) + benchmarks** são arquitetura de flow de email, regra de horário de disparo e leitura de canal de SMS — a 07c não constrói flow nem instala SMS; quem as puxa é a 13 (retention, Fases A/B). O que esta skill toca de email é o **sinal** (captura on-site alimentando Advanced Matching/EMQ e a lista própria), coberto na ETAPA 2.

## Quando Usar

Quando a página já está deployada na loja (Skill 07b) e o membro precisa garantir que cada visita e compra seja medida ANTES de gastar dinheiro com ads. As Skills 08 (creatives) e 10 (ad-strategy) exigem no pré-flight `manifest.tracking.tracking_ready == true` (Pixel + CAPI validados, EMQ ≥ 6.0 — ou o caminho `pending_traffic` da ETAPA 3 pra loja pré-launch sem volume) — esta é a skill que constrói, valida e grava esse contrato.

É uma skill **operacional** (passo a passo pra executar no Shopify + Events Manager), não conceitual. Sem ela, os criativos da 08 e a campanha da 10 viram dinheiro queimado por falta de sinal de conversão.

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)

- [ ] `workspace/[produto]/manifest.json` existe e é parseável
- [ ] `07b-page-build` está em `skills_completed` (página no ar) — sem página deployada, ViewContent/AddToCart/Purchase não têm onde disparar
- [ ] Budget legível: `manifest.budget_daily` (campo numérico canônico, $/dia — gravado pela 00); em manifest legado sem ele, `manifest.budget_tier` e/ou o budget declarado em `workspace/profile.md` — é o que refina a decision tree do analytics stack (ETAPA 4). O `04-offer-builder/dados.json` NÃO tem campo de budget; não o exija por isso.
- [ ] Acesso ao Shopify admin da loja + uma conta Meta Business (Business Manager + ad account + um Pixel/Dataset)

**Arquivo de pré-flight faltante (escape path, rule ES1):** se `manifest.json` não parseia, NÃO aborte seco — ofereça **(A)** rebuild do manifest (inspeciona `workspace/[produto]/` e reconstrói, perguntando budget/stage), OU **(B)** restore do backup mais recente (`.manifest-backup-*.json`). Ver `.claude/rules/emergency-escape-paths.md` ES2.

Se `07b-page-build` NÃO está em `skills_completed`, ofereça: **(A)** rodar `build page` (07b) agora pra subir a página, OU **(B)** prosseguir só com a instalação do pixel + CAPI marcando `manifest.skipped_preflight += ["07b-page-build"]` e avisando no output final que a validação de eventos de funil (ViewContent/AddToCart/Purchase) fica incompleta até a página existir.

### Gate de consistência (Skill 09) — não-bloqueante aqui

A 09 gateia o **launch** (Skill 10), não o tracking. Esta skill pode rodar antes ou depois da 09. Se `09-consistency-audit/dados.json` existir com `launch_recommendation == "BLOCK"`, apenas registre no output final que o launch está bloqueado até a 09 passar — mas siga instalando o tracking normalmente (ter pixel pronto não gasta dinheiro).

### Contexto a carregar

1. **Idioma do relatório (regra 0 do CLAUDE.md — INVIOLÁVEL):** leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). **TODO output interno desta skill (relatório de setup, decision tree, instruções) e toda conversa com o membro usam esse idioma**, com a régua de linguagem simples da regra 0 (nenhuma sigla sem explicação imediata na primeira vez — EMQ, CAPI, MMM, NCPA inclusas —, zero frase de analista comprimida). Esta skill não gera copy consumidor-final, então a regra de "copy pública sempre em inglês" não tem objeto aqui.
2. Leia `manifest.json` → `stage` (starter / validating / scaling) e `budget_daily` (o valor numérico canônico de $/dia, gravado pela 00; fallback em manifest legado: `budget_tier` ou o `profile.md`). **O stage é o que define o analytics stack recomendado** (ver decision tree); o budget refina. Detecção automática de stage em `.claude/rules/member-stage-awareness.md` se o campo estiver ausente.
3. **Puxe os SISTEMAS NOMEADOS da base — NUNCA query genérica.** As queries estão embutidas no ponto de uso de cada ETAPA abaixo (blocos "Puxe antes"). Carregue JÁ, antes da ETAPA 1, o sistema-espinha desta skill:
   - **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`) — ads são um loop de feedback de dados (dado ruim entra, decisão ruim sai); os parâmetros de match de maior prioridade são **email e Click ID** (identificadores 1:1); EMQ abaixo de 5 é inutilizável pro Meta; TODOS os parâmetros de Advanced Matching ligados; e **coletar mais emails on-site é a otimização técnica de maior alavancagem** (recupera 40%+ das conversões rastreadas). É o sistema que governa as ETAPAs 1-3.

   (Deduplicação por `event_id` e os 5 eventos padrão do funil são procedimento operacional das ETAPAs 1-2, não sistema da base — não invente query pra eles. A Estrutura de Assets Anti-Ban pertence à skill 00 no índice, não a esta.)

### Detecção de MCP (cascade)

A instalação do pixel é feita no Shopify admin (a Meta gerencia o snippet via integração nativa); o MCP entra na **verificação do Event Match Quality (EMQ)** e na leitura de datasets. Cascade:

- **Caminho 1 — MCP oficial Meta** (`mcp.facebook.com/ads`): tools `mcp__meta__ads_*`. Usar `ads_get_datasets` / equivalente de insights de dataset pra ler o EMQ programaticamente, sem screenshot manual.
- **Caminho 2 — Pipeboard** (`mcp__meta-ads__*`): fallback automático quando o oficial está indisponível.
- **Caminho 3 — manual**: o membro tira screenshot do Events Manager mostrando a dupla-coluna (Browser + Server) e o Event Match Quality (escore 0-10 por evento), e cola pra você validar visualmente.

Logue qual caminho foi usado no campo `source` do JSON de saída (convenção em `.claude/lib/mcp-detect/README.md`). Se nenhum MCP estiver presente, o Caminho 3 (manual) é o normal — não é degradação.

## Fluxo da Skill

### ETAPA 1 — Instalar o Meta Pixel

A integração nativa Shopify↔Meta gerencia o pixel sem editar tema. Passos pra colar no admin:

1. **Shopify admin > Settings > Apps and sales channels > Facebook & Instagram** (instalar o canal "Facebook & Instagram" se ainda não estiver). Conectar o Business Manager e o ad account corretos.
2. Em **Settings > Customer events** (a área que SUBSTITUIU os antigos "Additional scripts"), confirmar que existe um **Meta pixel** conectado ao Dataset/Pixel ID certo. O checkout roda em Checkout Extensibility (padrão hoje pra toda loja nova): o pixel entra via o app Meta ou como **Custom pixel** — NUNCA snippet hardcoded no `theme.liquid` (duplica eventos e quebra dedup).
3. **Data sharing do pixel: "Always on", NUNCA "Optimized".** Desde 13/jan/2026 o default de data sharing dos app pixels é "Optimized" — que PAUSA o envio de dados quando o pixel fica dias sem sinal de tráfego/venda. É exatamente o cenário da loja nova pré-launch: o pixel parece instalado, mas a Shopify silenciosamente para de enviar eventos, e o membro lança ads com dataset vazio. Em **Settings > Customer events**, mude o data sharing do pixel da Meta pra **"Always on"** antes de qualquer validação.
4. Confirmar que o **Pixel ID** no Shopify bate com o Pixel/Dataset que o ad account vai usar na Skill 10. Mismatch aqui = eventos no dataset errado, campanha cega.

> **Por que não hardcodar no tema:** snippet manual no `theme.liquid` + pixel da integração nativa = evento duplicado sem `event_id` consistente, derrubando o EMQ e inflando contagem de Purchase. Deixe a integração nativa ser a única fonte do pixel.

**Eventos do funil a confirmar** (Events Manager > Test Events, navegando a loja): `PageView`, `ViewContent` (PDP), `AddToCart`, `InitiateCheckout`, `Purchase`. Se algum falta, o problema está na integração nativa (re-conectar o canal) ou no tema (PDP sem o trigger de ViewContent).

### ETAPA 2 — Ativar a Conversions API (CAPI)

CAPI envia os mesmos eventos pelo servidor (server-side), redundante ao browser, deduplicados por `event_id`. É o que mantém o tracking vivo com iOS/ad-blockers/cookie loss.

1. **No app Facebook & Instagram (dentro do Shopify admin) > Settings > Data sharing** — selecionar o nível **Maximum**. É essa escolha que ativa a Conversions API server-side + Advanced Matching (Standard = só pixel browser; Enhanced = + advanced matching; **Maximum = + CAPI**). O toggle de CAPI NÃO fica em "Customer events" — Customer events é a área de custom pixels, use-a só pra verificar duplicidade.
2. **Advanced Matching** ON (vem com o nível Maximum) — envia email/telefone/nome hasheados (SHA-256) com cada evento. É o maior driver de EMQ. Confirmar que o checkout está passando customer data pro CAPI.
3. **Events Manager > [seu Dataset] > Settings** — confirmar **"Conversions API"** ativa e a fonte (Partner Integration: Shopify) listada.

**Puxe antes de fechar esta etapa (o sinal além do Purchase):**

- **Engaged Lead / sinal digital de qualificação** (rode `engaged lead evento de conversão customizado otimizar para o sinal de qualificação offline events`) — se a loja captura email/lead on-site (popup, quiz), crie o **evento de conversão customizado do lead ENGAJADO** (não do lead bruto) e deixe-o disponível no dataset: é o sinal de qualificação pelo qual um ad set pode otimizar quando não há volume de Purchase, com offline events como reforço. Loja pré-launch no caminho `pending_traffic` é exatamente o cenário em que esse sinal intermediário mais vale.
- **Three Types of Traffic (Own / Control / Don't Control)** (rode `traffic you own traffic you control traffic you dont control brunson`) — o email capturado on-site é **tráfego que você POSSUI**: além de ser, com o Click ID, o parâmetro de match nº 1 do EMQ, é o identificador que continua seu quando iOS e ad-blockers degradam o pixel (tráfego que você não controla). É por isso que a captura de email é tratada como parte do tracking, não só de retention — a arquitetura dos flows que usam essa lista é da Skill 13.

> **Dedup (event_id):** cada evento precisa do MESMO `event_id` no browser e no servidor pra Meta não contar duas vezes. A integração nativa faz isso. Se você vir Purchase contado em dobro no Events Manager, a dedup quebrou (geralmente pixel hardcoded + nativo coexistindo — voltar à ETAPA 1).

> **Aviso — CAPI de 1 clique da Meta (abr/2026):** o Events Manager oferece um botão "Activate Conversions API" que cria uma SEGUNDA fonte server-side. Se o membro clicou nele POR CIMA da integração nativa Shopify↔Meta, os Purchase chegam duplicados SEM `event_id` pareado (a dedup não casa fontes diferentes). Pergunte se ele ativou; se sim, desative uma das duas fontes server-side (manter a nativa do Shopify) e re-verifique a contagem no Events Manager.

### ETAPA 3 — Validar o Event Match Quality: EMQ ≥ 6.0 (gate técnico)

Este é o **gate que destrava 08 e 10**. O Event Match Quality (EMQ) é um **escore de 0 a 10 por evento** no Events Manager (com faixas Poor/OK/Good/Great) — NÃO existe "match quality em %"; nunca peça porcentagem ao membro. O gate canônico do framework é **EMQ ≥ 6.0** no evento Purchase (é o que `manifest.tracking.tracking_ready` atesta e o que 08/10 verificam) — **com uma exceção estrutural:** loja pré-launch sem tráfego não tem como ter escore (o EMQ só calcula com eventos reais); pra esse caso existe o caminho `pending_traffic` na tabela abaixo, que destrava o launch com instalação verificada + pedido-teste, sem esperar um número que só o próprio tráfego produz.

**Caminho 1/2 (MCP oficial/Pipeboard):** ler o EMQ do dataset via tool de insights de dataset. Capturar o escore numérico (0-10) do Purchase (e do AddToCart como secundário).

**Caminho 3 (manual):** pedir ao membro:
> "Abre o **Events Manager > seu Dataset > Overview**. Me manda print de: (1) a dupla-coluna Browser + Server nos eventos Purchase/AddToCart, e (2) o **Event Match Quality** do Purchase (o escore de 0 a 10 no card do evento). Quero ver **6.0 ou mais**."

**Decisão do gate:**

| EMQ (Purchase, escala 0-10) | Ação |
|---|---|
| **≥ 8.0** (Great) | PASS. `tracking_ready: true`. Seguir pra ETAPA 3B. |
| **6.0–7.9** (Good/OK) | PASS com recomendação. Tracking destravado, mas sub-ótimo: recomendar Advanced Matching completo (email + phone + nome + endereço no checkout) e re-medir em 24-48h (precisa de tráfego pra recalcular). `tracking_ready: true` com `emq_warn: true`. |
| **Sem dados por falta de tráfego** (loja pré-launch: Pixel + CAPI instalados corretamente E os 5 eventos do funil confirmados no Test Events, mas dataset sem volume pro escore calcular) | **PASS condicional (`pending_traffic`)** — não é falha de configuração, é ausência de tráfego: o EMQ só existe com eventos reais, e exigir escore antes do primeiro ad criaria um impasse (sem tracking_ready a 10 não roda tráfego; sem tráfego o EMQ nunca calcula). Gravar `emq.status: "pending_traffic"`, `emq.score: null`, e no manifest `tracking_ready: true` + `emq_pending: true`. **Obrigatório antes de fechar:** validar o Purchase de ponta a ponta com um **pedido-teste real** — Bogus Gateway num tema de preview (sem cobrança) OU pedido real de ~$1 + refund — e confirmar o evento Purchase chegando com a dupla-coluna (Browser + Server) no Events Manager. A Skill 11 re-lê o EMQ no dia 3 de tráfego; EMQ < 6.0 pós-tráfego = ação corretiva (voltar a esta skill). |
| **< 6.0 COM volume de eventos** | BLOCK. Pixel ou CAPI mal configurado (o escore existe e está baixo — é config, não falta de dados). **Escape (ES1):** ofereça **(A)** rodar o diagnóstico abaixo e re-medir, OU **(B)** prosseguir marcando `manifest.skipped_preflight += ["emq_gate"]` e avisando que 08/10 vão herdar tracking fraco (`tracking_ready: false`, membro aceitou o risco). |

**Diagnóstico de EMQ baixo** (rodar antes de qualquer "prosseguir mesmo assim"):
- CAPI OFF ou sem Advanced Matching (Data sharing abaixo de Maximum) → ETAPAS 1-2.
- Data sharing em "Optimized" pausou o envio (loja sem tráfego) → ETAPA 1 passo 3 ("Always on").
- Sem volume: dataset novo precisa de ~algumas dezenas de eventos pra calcular o escore. Se a loja não teve tráfego ainda, o número pode estar vazio — não é erro, é falta de dados → caminho **`pending_traffic`** da tabela acima (exige o pedido-teste validando o Purchase).
- Pixel duplicado (hardcoded + nativo, ou CAPI 1-clique por cima da nativa) → dedup quebrada → ETAPAS 1-2.

### ETAPA 3B — Janela de atribuição + preservação do Click ID

A janela de atribuição define **o que o número do Ads Manager significa**; o Click ID define **quantas conversões conseguem ser atribuídas**. Fixar os dois aqui evita que a 10 lance com leitura incomparável e que a 12 escale com sinal furado.

**Puxe antes desta etapa:**

- **Preservação de Click ID (cross-domain + express checkout)** (rode `click id perdido cross-domain express checkout Shop Pay restaurar 40% mais conversões`)
- **Teste de troca pra 7DC-only** (rode `campanha duplicada 7-day click only view-through inflado email blast returning customers`)
- **Slots de teste não-criativo (Hard Exclusions / 1-Day Click / Incremental Attribution)** (rode `ad sets de teste não-criativo hard exclusions 1-day click incremental attribution`)

1. **Baseline de janela: `7d-click/1d-view`** (7 dias pós-clique + 1 dia pós-visualização). É a janela em que a Skill 10 cria o teste padrão e na qual as réguas de kill da Skill 11 foram calibradas. Documente-a no relatório e **deixe o setting de Incremental Attribution DESLIGADO no launch** — ele muda o que o Meta conta como conversão, torna o CPA incomparável com o baseline e trava as attribution settings (a 11 re-baseia todos os thresholds se o membro ligar).
2. **Teste 7DC-only é diagnóstico agendado, não default:** com histórico rodando, duplicar a campanha só com atribuição de **7-day click** mede quanto do resultado reportado vinha inflado por view-through, disparo de email e clientes recorrentes. Registre no relatório que esse teste existe e quando cabe — quem o executa é a **Skill 12**, num slot de teste não-criativo (a mesma família dos testes de hard exclusions, janela 1-day click e atribuição incremental), nunca por cima da campanha que está pagando as contas.
3. **Preservar o Click ID de ponta a ponta:** o Click ID (com email, o parâmetro de match 1:1 de maior prioridade) se perde na navegação entre domínios e no express checkout tipo Shop Pay — e recuperá-lo restaura **até 40% mais conversões atribuídas**. Checar: **(a)** a jornada LP → PDP → checkout não troca de domínio raiz; **(b)** no Purchase mais recente do Events Manager (ou no pedido-teste da ETAPA 3), o evento chegou COM o parâmetro de click ID; **(c)** se o stage pedir stack pago na ETAPA 4, a captura server-side do click ID (Wetracked / Sonar do Triple Whale / Aimerce) é parte do valor que justifica o custo.

### ETAPA 4 — Analytics Stack (decision tree por member-stage)

A Skill 11 (ad-analysis) depende de atribuição confiável. Antes do launch, fixar a stack certa. **Considerar APENAS estas 4 opções** — NUNCA sugerir Elevar, Stape, Littledata, Segment, GTM server-side custom, ou qualquer CDP enterprise (complexidade desnecessária / fora de escopo).

**Puxe antes desta etapa (os três sistemas que estruturam a decisão):**

- **Stack de atribuição em 3 camadas (Triple Whale / Northbeam / KnoCommerce)** (rode `stack de atribuição três camadas blended MMM post-purchase survey por estágio de receita`)
- **Hierarquia de decisão por atribuição (blended / plataforma / terceiro)** (rode `blended decide o negócio plataforma decide a otimização third-party red flag incrementalidade`)
- **Três níveis de KPI por maturidade (Blended → +In-Platform → NCPA+LTV)** (rode `três níveis de KPI blended ROAS in-platform NCPA LTV por faixa de faturamento`)

**O modelo que governa a escolha:** atribuição madura é um **empilhamento de 3 camadas por estágio de receita**, não uma ferramenta única. Camada 1 — leitura **blended** (receita total ÷ spend total): existe desde o dia 1 com Shopify + Meta App, sem custo, e é a leitura que o Triple Whale consolida num painel só quando a receita justifica a ferramenta. Camada 2 — modelos de atribuição de terceiro (os modelos do próprio Triple Whale nas 4 opções) e, em receita alta, MMM (modelagem de mix de mídia, o papel do Northbeam na fonte — **fora das 4 opções de stack desta skill**; se o membro chegar nesse estágio, a conversa é da Skill 12). Camada 3 — **survey pós-compra de atribuição** (KnoCommerce), o dado que o próprio cliente declara e que não degrada com iOS/cookie. E cada fonte tem UM papel (hierarquia de decisão): **o blended decide o negócio, a plataforma decide a otimização, e a ferramenta de terceiro serve pra levantar red flag de incrementalidade** — nunca dê à ferramenta paga o papel de decidir o negócio. Os KPIs acompanham a maturidade na mesma escada: começa **só com Blended ROAS**, soma as métricas in-platform quando há volume, e só no estágio final decide por NCPA (custo por cliente NOVO) + LTV — não cobre do starter o KPI do scaling.

| Stack | Stage / quando recomendar | Custo | Setup |
|---|---|---|---|
| **Meta App nativo na Shopify** (baseline) | `starter` — budget < ~$50/dia, pixel simples | Grátis | Baixo (1-click) |
| **Wetracked** | `validating` — quer tracking melhor que Shopify+Meta sem pagar Triple Whale | $29-99/mês | Médio |
| **Triple Whale** | `scaling` — budget $1k+/dia, múltiplos canais (Meta + TikTok + Google), precisa visão consolidada de LTV/CAC/NCROAS | $129-499/mês | Médio-Alto |
| **Aimerce** | `scaling` premium — budget > $3k/dia, capital disponível, quer atribuição AI-driven com modelagem server-side avançada | $200+/mês | Alto |

**Mapeamento por stage (default; o budget refina):**
- `starter` → **Meta App nativo** + CAPI ON. Baseline sempre. NÃO empurrar tool paga pra quem tem $500/mês.
- `validating` → **Meta App** ou **Wetracked** (se o membro quer atribuição mais precisa).
- `scaling` → **Triple Whale** vira payback claro a partir de $1k/dia; **Aimerce** entra como premium acima de $3k/dia.

**Budget mapping (refina o stage):**
- < $500/dia → Meta App basta
- $500-$1k/dia → Meta App OU Wetracked
- $1k-$3k/dia → Triple Whale
- $3k+/dia → Aimerce como opção premium

**Fluxo de decisão:**

1. Pergunte: "Você já usa Meta App (padrão Shopify), Wetracked, Triple Whale ou Aimerce — ou nenhum ainda?"
2. Se **"nenhum"** → recomendar o stack do stage (default acima) e instalar. Pra `starter`: Shopify Settings > Apps > instalar Meta App + CAPI ON (já feito nas ETAPAS 1-3 — o "Meta App nativo" É essa configuração).
3. Se o membro **já tem um dos quatro** → confirmar a configuração:
   - **Meta App**: CAPI dupla-coluna no Events Manager, EMQ ≥ 6.0 (já validado na ETAPA 3).
   - **Wetracked**: snippet enviando server-side events correlacionados ao pixel.
   - **Triple Whale**: TW Pixel instalado + **Sonar** (server-side) ON + Meta Ads conectado. **Puxe o mapa de modelos antes de confirmar** (rode `Triple Whale janela 14 dias TA click-through only NC-ROAS nunca decisão por ad`): janela default de 14 dias, modelo TA e click-through only NÃO são intercambiáveis, NC-ROAS é a leitura de cliente novo — e a regra da fonte: **nunca decidir no nível do anúncio individual** por esses números (na hierarquia, terceiro levanta red flag; quem mata/escala criativo é a régua da 11/12). Deixe os modelos escolhidos anotados no relatório pra 11 ler depois.
   - **Aimerce**: Aimerce Pixel + container server-side ativo + identity resolution funcionando. **Puxe antes de recomendar** (rode `database de 280 milhões de americanos, resolver visitante anônimo em email e endereço, 150x de ROI`): software de identity resolution que transforma visitante anônimo em email/endereço é **legal nos EUA e ILEGAL na Europa** — loja com tráfego ou entrega na União Europeia NÃO liga essa camada; a ressalva vai por escrito no relatório junto da recomendação.

Se o membro usa stack **≠** das 4 acima, PARAR e alinhar antes de seguir — dados ruins inviabilizam a Skill 11 depois.

**Camadas complementares (qualquer stage — baratas, e não competem com as 4 opções):**

- **Survey pós-compra de atribuição (camada 3 do stack)** (rode `how did you first hear about us survey pós-compra follow-ups condicionais response rate` — a mesma entrada existe indexada em `market-research-voc` como `post purchase survey how did you first hear about us follow up condicional atribuicao`; é o MESMO sistema, puxe uma vez e reuse): pergunta **"how did you first hear about us?"** na página de agradecimento, com follow-ups condicionais conforme o canal respondido, e acompanha a **response rate** como qualificador do dado. Custa quase nada, funciona em qualquer stage e é a única camada imune a cookie/iOS — recomende desde o starter. As respostas viram VOC que a Skill 02 reusa.
- **Camada on-site (comportamento na página)** (rode `bounce exit rate time on page page value comparar entre paginas similares heatmap scroll`): as **4 métricas de página** — bounce, exit rate, time on page e page value, sempre comparadas **entre páginas similares**, nunca em absoluto — cruzadas com os **3 relatórios do Hotjar** (heatmap, scroll, recording). Instalar aqui (free tier serve) é o que garante que a 09 e a 11 tenham dado de comportamento pra ler depois: o pixel mede quem chega; essa camada mede o que a página faz com quem chegou.

Gravar a escolha em `manifest.tracking.analytics_stack` (bloco aninhado — ver "Atualizar manifest").

### ETAPA 4B — Leitura: o contrato de interpretação que este setup entrega

O relatório fixa COMO os números do stack escolhido serão lidos — é o que evita a briga "o Meta diz X, o Shopify diz Y" no dia 3 de tráfego.

**Puxe antes desta seção:**

- **Blended ROAS as the P&L Metric** (rode `blended ROAS Shopify dividido por spend total atribuição first click mente`)
- **CAC vs CPA Discipline (Shopify new customer = TRUE)** (rode `CAC igual spend dividido por clientes novos Shopify não CPA de plataforma`)
- **Regra de inflação do TA no Google** (rode `Triple Whale TA infla Google branded search comparar first click last click incremental`)
- **Google Search Stronghold + setup 80-20** (rode `Google Search Stronghold branded search proteger a marca converter copy do Facebook`)

1. **Blended ROAS é a métrica de P&L (o resultado do negócio):** receita do Shopify ÷ spend total de TODAS as plataformas. A atribuição da plataforma superatribui o próprio canal ("a atribuição de first click mente") — número de plataforma serve pra otimizar DENTRO dela, nunca pra responder "o negócio dá dinheiro?". É o nível 1 dos KPIs por maturidade da ETAPA 4, e a única leitura que o starter precisa no primeiro mês.
2. **CAC ≠ CPA:** CAC = spend do período ÷ **clientes NOVOS marcados no Shopify** (`new customer = TRUE`); o CPA que a plataforma reporta conta cliente recorrente e atribuição inflada. Cânone `.claude/lib/unit-economics/README.md` §3 — o relatório de tracking deixa as duas colunas nomeadas pra ninguém misturar depois.
3. **Branded search é o ponto cego da atribuição de terceiro:** o modelo TA do Triple Whale **infla o Google — sobretudo a busca pelo nome da marca**; antes de decidir qualquer coisa por esse número, comparar first click, last click e a leitura incremental. Vale dobrado se a Skill 10 montar o **Google Search Stronghold** (o setup 80-20 que defende a branded search reaproveitando a copy que já converte no Facebook): a receita dessa campanha é em boa parte demanda que o Meta criou — leia-a como proteção de marca, não como canal incremental.

**Quem consome a decisão de atribuição desta skill (handoffs, 1 linha cada):**

- **Skill 11 (ad-analysis)** usa a **hierarquia de decisão por atribuição** (blended decide o negócio, plataforma decide a otimização, terceiro levanta red flag) como régua de leitura sobre o `manifest.tracking.analytics_stack` gravado aqui.
- **Skill 12 (scale-engine)** usa o **gate click-based** do Scaling Protocol (≥60% das purchases em 7-day click, `ad-taxonomy` §5) — o share de clique só é medível porque a ETAPA 3B fixou a janela baseline e preservou o Click ID; quando o gate falha, a 12 manda de volta pra cá re-medir.
- **Skill 15 (finance-engine)** usa **Blended ROAS como métrica de P&L** (e CAC de clientes novos do Shopify) — os números do negócio inteiro saem da leitura blended fixada nesta seção, nunca do painel da plataforma.

### ETAPA 5 — Verificação final + handoff

Antes de declarar pronto, confirmar a checklist (responde 08/10):

- [ ] Pixel conectado ao Dataset correto (bate com o ad account da 10)
- [ ] Data sharing do pixel em **"Always on"** (não "Optimized")
- [ ] 5 eventos do funil disparando (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)
- [ ] CAPI ON (Data sharing = Maximum) + Advanced Matching ON (dupla-coluna Browser + Server), sem fonte server-side duplicada (CAPI 1-clique)
- [ ] EMQ ≥ 6.0 no Purchase (ou `emq_warn` documentado; ou `pending_traffic` com Purchase validado por pedido-teste e `emq_pending: true` no manifest)
- [ ] Janela baseline `7d-click/1d-view` documentada, Incremental Attribution desligado, Click ID conferido no Purchase (ETAPA 3B)
- [ ] Analytics stack escolhido e instalado/confirmado + contrato de leitura fixado no relatório (Blended ROAS como P&L, CAC ≠ CPA — ETAPA 4B)

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/07c-tracking-setup/` antes de salvar.

`workspace/[produto]/07c-tracking-setup/tracking-setup.md` contendo:
1. Status do pixel (Dataset ID, canal nativo, data sharing "Always on", eventos confirmados — incluindo evento customizado de lead engajado, se a loja captura lead)
2. Status do CAPI (nível de Data sharing, Advanced Matching, dedup, fonte única server-side)
3. EMQ medido (escore 0-10 do Purchase) + caminho de verificação usado (MCP oficial / Pipeboard / manual)
4. Janela de atribuição baseline (`7d-click/1d-view`), status do Click ID no Purchase, e o teste 7DC-only registrado como diagnóstico futuro da 12 (ETAPA 3B)
5. Analytics stack escolhido + razão (stage + budget) + camadas complementares (survey pós-compra / on-site) + passos de setup/confirmação
6. Contrato de leitura (ETAPA 4B): Blended ROAS como P&L, CAC ≠ CPA, ponto cego de branded search na atribuição de terceiro
7. Checklist final da ETAPA 5
8. Próximos passos (checkout/AOV → criativos)

**Dual output `.html`** companion com o mesmo nome (`07c-tracking-setup/tracking-setup.html`): usar `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained), abrindo o `<body>` com o bloco SVG da logo copiado LITERALMENTE de `.claude/templates/aura-logo-snippet.html` (NUNCA substituir por texto). Usar componentes aura (callout, note, danger, table-wrap, pill) — emojis ✅⚠️❌ são OK em relatório interno (rule 7 exceção).

### JSON companion — `07c-tracking-setup/dados.json`

```json
{
  "tracking_id": "uuid",
  "product_slug": "...",
  "generated_at": "ISO-8601",
  "report_language": "pt-BR",
  "pixel": {
    "dataset_id": "...",
    "channel": "shopify_native_meta",
    "data_sharing": "always_on",
    "events_confirmed": ["PageView", "ViewContent", "AddToCart", "InitiateCheckout", "Purchase"]
  },
  "capi": {
    "enabled": true,
    "advanced_matching": true,
    "dedup_event_id": true
  },
  "attribution": {
    "window_baseline": "7d_click_1d_view",
    "click_id_on_purchase": true,
    "survey_layer": "knocommerce | none",
    "onsite_layer": "hotjar | none"
  },
  "emq": {
    "score": null,
    "scale": "0-10",
    "status": "pass | warn | pending_traffic | block",
    "source": "mcp_meta_official | pipeboard | manual"
  },
  "analytics_stack": "meta_app | wetracked | triple_whale | aimerce",
  "tracking_ready": true
}
```

(`emq.score` é numérico 0-10, ou `null` quando `pending_traffic`.)

### Atualizar manifest — bloco aninhado `manifest.tracking` (contrato canônico)

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `07c-tracking-setup` em `skills_completed`, atualizar `updated_at`
- Gravar o bloco **ANINHADO** `tracking` (nunca campos flat no top-level — o manifest-schema documenta e as skills 08/10 leem `manifest.tracking.*`):

```json
"tracking": {
  "pixel_installed": true,
  "capi_active": true,
  "emq_score": 7.2,
  "emq_pending": false,
  "analytics_stack": "meta_app",
  "tracking_ready": true
}
```

- `emq_score`: 0-10 (ou `null` se `pending_traffic`). `tracking_ready`: `true` com EMQ ≥ 6.0 medido, **OU** no caminho `pending_traffic` (Pixel + CAPI instalados, 5 eventos confirmados, Purchase validado por pedido-teste) — nesse caso gravar também `emq_pending: true` (a 10 aceita esse estado com aviso, e a 11 re-lê o EMQ no dia 3 de tráfego). Risco aceito via escape ES1 (config errada, membro seguiu mesmo assim) continua `tracking_ready: false`. As Skills 08 e 10 leem `manifest.tracking.tracking_ready` no pré-flight sem pedir screenshot de novo; a 10 e a 11 leem `manifest.tracking.analytics_stack` pra orientar leitura de dados.
- Registrar `tracking_id`
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug`; atualiza ABRIR-AQUI.html)

> Se `tracking_ready: false` foi gravado (membro escolheu prosseguir com EMQ baixo via escape ES1), a 08 e a 10 vão herdar o aviso e devem alertar que os criativos/campanha rodam com sinal degradado.

## Mensagem Final

(idioma = `report_language`)

> "Tracking pronto. Pixel `[Dataset ID]` conectado (data sharing 'Always on'), CAPI ON com Advanced Matching, e os 5 eventos do funil disparando. Event Match Quality em **[X]/10** (`[pass/warn]`) [SE `pending_traffic`: "Event Match Quality ainda **sem escore** — normal em loja pré-launch, o EMQ só calcula com tráfego real. Validei o Purchase de ponta a ponta com o pedido-teste, então o launch está destravado (`emq_pending`); no dia 3 de tráfego a análise re-lê o escore e corrige se vier abaixo de 6"]. Janela de atribuição fixada no baseline (7 dias pós-clique / 1 dia pós-visualização) e Click ID chegando junto do Purchase. Analytics stack: **[stack escolhido]** (escolhido pelo seu stage `[stage]` + budget). E o combinado de leitura já vale: o resultado do NEGÓCIO é a receita do Shopify dividida pelo spend total (Blended ROAS) — o painel da plataforma serve pra otimizar, não pra dizer se dá lucro.
>
> Isso destrava os criativos e a campanha — eles exigem exatamente esse pixel + CAPI com EMQ ≥ 6/10 que a gente acabou de validar.
>
> Próximo passo: diga **'checkout'** pra configurar upsell/bump/bundle (Skill 07d — ela ajusta o AOV e o CPA que o briefing de ad usa, então vem ANTES dos criativos). Depois dela, a ordem de launch segue: **'bonus delivery'** (05 Fase A, se a oferta tem bônus) → **'retention'** (13 Fase A — flows de recuperação: abandoned cart + post-purchase, a infraestrutura que se arma ANTES de ligar tráfego) → **'creatives'** (08).
>
> Primeira versão dos próximos passos como referência — se quiser ajustar a stack de tracking ou re-medir o EMQ depois de rodar tráfego, é só me chamar."

---

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) `manifest.tracking.tracking_ready` reflete o status REAL do EMQ (não gravar `true` com escore < 6.0 MEDIDO sem o membro ter aceitado o risco; o caminho `pending_traffic` só grava `true` com os 5 eventos confirmados + Purchase validado por pedido-teste + `emq_pending: true`); (2) `manifest.tracking.analytics_stack` é uma das 4 opções canônicas e bate com o stage; (3) `07c-tracking-setup/dados.json` + `tracking-setup.md` + `tracking-setup.html` salvos, `.html` com logo SVG, `emq.score` na escala 0-10, bloco `attribution` preenchido (janela baseline + click ID + camadas); (4) Dataset ID do pixel é consistente com o ad account que a Skill 10 vai usar; (5) manifest atualizado (`skills_completed`, bloco aninhado `tracking` completo — `pixel_installed`/`capi_active`/`emq_score`/`analytics_stack`/`tracking_ready` —, `updated_at`); (6) data sharing do pixel confirmado em "Always on" e sem fonte CAPI duplicada; (7) contrato de cobertura cumprido: a lista de entradas `07c` do `frameworks.json` foi enumerada e cada entrada relevante à sessão foi puxada pela `best_query` exata (as 3 entradas cujo ponto de uso é a 13 ficam com a 13). Issue dentro do escopo → fix inline. Conflito que exige decisão do membro (ex: dois pixels ativos, qual manter) → surface curto.
