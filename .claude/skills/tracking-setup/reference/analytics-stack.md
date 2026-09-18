# Tracking Setup · Referência: Analytics stack, a decision tree por stage (ETAPA 4)

> Os três sistemas que estruturam a decisão, o modelo das 3 camadas e a hierarquia de decisão, a tabela das 4 opções, o mapeamento por stage e por budget, o fluxo de decisão com as confirmações por ferramenta (inclusive as queries do Triple Whale e do Aimerce) e as camadas complementares. Abra na ETAPA 4.

### ETAPA 4 — Analytics Stack (decision tree por member-stage)

A Skill `ad-analysis` depende de atribuição confiável. Antes do launch, fixar a stack certa. **Considerar APENAS estas 4 opções** — NUNCA sugerir Elevar, Stape, Littledata, Segment, GTM server-side custom, ou qualquer CDP enterprise (complexidade desnecessária / fora de escopo).

**Puxe antes desta etapa (os três sistemas que estruturam a decisão):**

- **Stack de atribuição em 3 camadas (Triple Whale / Northbeam / KnoCommerce)** (rode `stack de atribuição três camadas blended MMM post-purchase survey por estágio de receita`)
- **Hierarquia de decisão por atribuição (blended / plataforma / terceiro)** (rode `blended decide o negócio plataforma decide a otimização third-party red flag incrementalidade`)
- **Três níveis de KPI por maturidade (Blended → +In-Platform → NCPA+LTV)** (rode `três níveis de KPI blended ROAS in-platform NCPA LTV por faixa de faturamento`)

**O modelo que governa a escolha:** atribuição madura é um **empilhamento de 3 camadas por estágio de receita**, não uma ferramenta única. Camada 1 — leitura **blended** (receita total ÷ spend total): existe desde o dia 1 com Shopify + Meta App, sem custo, e é a leitura que o Triple Whale consolida num painel só quando a receita justifica a ferramenta. Camada 2 — modelos de atribuição de terceiro (os modelos do próprio Triple Whale nas 4 opções) e, em receita alta, MMM (modelagem de mix de mídia, o papel do Northbeam na fonte — **fora das 4 opções de stack desta skill**; se o membro chegar nesse estágio, a conversa é da Skill `scale-engine`). Camada 3 — **survey pós-compra de atribuição** (KnoCommerce), o dado que o próprio cliente declara e que não degrada com iOS/cookie. E cada fonte tem UM papel (hierarquia de decisão): **o blended decide o negócio, a plataforma decide a otimização, e a ferramenta de terceiro serve pra levantar red flag de incrementalidade** — nunca dê à ferramenta paga o papel de decidir o negócio. Os KPIs acompanham a maturidade na mesma escada: começa **só com Blended ROAS**, soma as métricas in-platform quando há volume, e só no estágio final decide por NCPA (custo por cliente NOVO) + LTV — não cobre do starter o KPI do scaling.

| Stack | Stage / quando recomendar | Custo | Setup |
|---|---|---|---|
| **Meta App nativo na Shopify** (baseline) | `starter` — budget < ~$500/dia, pixel simples | Grátis | Baixo (1-click) |
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
   - **Triple Whale**: TW Pixel instalado + **Sonar** (server-side) ON + Meta Ads conectado. **Puxe o mapa de modelos antes de confirmar** (rode `Triple Whale janela 14 dias TA click-through only NC-ROAS nunca decisão por ad`): janela default de 14 dias, modelo TA e click-through only NÃO são intercambiáveis, NC-ROAS é a leitura de cliente novo — e a regra da fonte: **nunca decidir no nível do anúncio individual** por esses números (na hierarquia, terceiro levanta red flag; quem mata/escala criativo é a régua da `ad-analysis`/`scale-engine`). Deixe os modelos escolhidos anotados no relatório pra `ad-analysis` ler depois.
   - **Aimerce**: Aimerce Pixel + container server-side ativo + identity resolution funcionando. **Puxe antes de recomendar** (rode `database de 280 milhões de americanos, resolver visitante anônimo em email e endereço, 150x de ROI`): software de identity resolution que transforma visitante anônimo em email/endereço é **legal nos EUA e ILEGAL na Europa** — loja com tráfego ou entrega na União Europeia NÃO liga essa camada; a ressalva vai por escrito no relatório junto da recomendação.

Se o membro usa stack **≠** das 4 acima, PARAR e alinhar antes de seguir — dados ruins inviabilizam a Skill `ad-analysis` depois.

**Camadas complementares (qualquer stage — baratas, e não competem com as 4 opções):**

- **Survey pós-compra de atribuição (camada 3 do stack)** (rode `how did you first hear about us survey pós-compra follow-ups condicionais response rate` — a mesma entrada existe indexada em `market-research-voc` como `post purchase survey how did you first hear about us follow up condicional atribuicao`; é o MESMO sistema, puxe uma vez e reuse): pergunta **"how did you first hear about us?"** na página de agradecimento, com follow-ups condicionais conforme o canal respondido, e acompanha a **response rate** como qualificador do dado. Custa quase nada, funciona em qualquer stage e é a única camada imune a cookie/iOS — recomende desde o starter. As respostas viram VOC que a Skill `market-research` reusa.
- **Camada on-site (comportamento na página)** (rode `bounce exit rate time on page page value comparar entre paginas similares heatmap scroll`): as **4 métricas de página** — bounce, exit rate, time on page e page value, sempre comparadas **entre páginas similares**, nunca em absoluto — cruzadas com os **3 relatórios do Hotjar** (heatmap, scroll, recording). Instalar aqui (free tier serve) é o que garante que a `consistency-audit` e a `ad-analysis` tenham dado de comportamento pra ler depois: o pixel mede quem chega; essa camada mede o que a página faz com quem chegou.

Gravar a escolha em `manifest.tracking.analytics_stack` (bloco aninhado — ver "Atualizar manifest").
