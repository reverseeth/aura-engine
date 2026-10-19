# Tracking Setup · Referência: Analytics stack, a decision tree por stage (ETAPA 4)

> Os três sistemas que estruturam a decisão, o modelo das 3 camadas e a hierarquia de decisão, o Wetracked como fonte única de eventos em todo stage, a camada opcional de atribuição em scaling (Triple Whale ou Aimerce, com as queries de cada uma), o fluxo de decisão e as camadas complementares. Abra na ETAPA 4.

### ETAPA 4 — Analytics Stack (Wetracked em todo stage, camada de atribuição opcional em scaling)

A Skill `ad-analysis` depende de atribuição confiável. A fonte de eventos da Aura é **sempre o Wetracked** (instalado nas ETAPAS 1-2), do `starter` ao `scaling`. Por cima dele, só em `scaling`, cabe uma camada opcional de leitura de atribuição: **Triple Whale** ou **Aimerce**. NUNCA sugerir Elevar, Stape, Littledata, Segment, GTM server-side custom ou CDP enterprise como fonte de eventos: o Wetracked já é a fonte única, e uma segunda fonte duplica.

**Puxe antes desta etapa (os três sistemas que estruturam a decisão):**

- **Stack de atribuição em 3 camadas (Triple Whale / Northbeam / KnoCommerce)** (rode `stack de atribuição três camadas blended MMM post-purchase survey por estágio de receita`)
- **Hierarquia de decisão por atribuição (blended / plataforma / terceiro)** (rode `blended decide o negócio plataforma decide a otimização third-party red flag incrementalidade`)
- **Três níveis de KPI por maturidade (Blended → +In-Platform → NCPA+LTV)** (rode `três níveis de KPI blended ROAS in-platform NCPA LTV por faixa de faturamento`)

**O modelo que governa a escolha:** atribuição madura é um **empilhamento de 3 camadas por estágio de receita**, não uma ferramenta única. Camada 1 — leitura **blended** (receita total ÷ spend total): existe desde o dia 1 com Shopify + Wetracked. Camada 2 — modelos de atribuição de terceiro (Triple Whale ou Aimerce, em `scaling`) e, em receita alta, MMM (modelagem de mix de mídia, o papel do Northbeam na fonte; se o membro chegar nesse estágio, a conversa é da Skill `scale-engine`). Camada 3 — **survey pós-compra de atribuição** (KnoCommerce), o dado que o próprio cliente declara e que não degrada com iOS ou cookie. Cada fonte tem UM papel (hierarquia de decisão): **o blended decide o negócio, a plataforma decide a otimização, e a ferramenta de terceiro serve pra levantar red flag de incrementalidade**; nunca dê à ferramenta paga o papel de decidir o negócio. Os KPIs acompanham a maturidade na mesma escada: começa **só com Blended ROAS**, soma as métricas in-platform quando há volume, e só no estágio final decide por NCPA (custo por cliente NOVO) + LTV.

| Camada | Stage / quando | Papel |
|---|---|---|
| **Wetracked** (obrigatório) | todos os stages | Fonte única de eventos: pixel no navegador + Conversions API pelo servidor, dedup por `event_id`, Advanced Matching com dado first-party. Captura o Click ID no servidor |
| **Triple Whale** (opcional) | `scaling` — budget de mil dólares por dia ou mais, vários canais (Meta + TikTok + Google), precisa da visão consolidada de LTV, CAC e NC-ROAS | Painel e modelos de atribuição. Nunca vira segunda fonte de eventos pra Meta |
| **Aimerce** (opcional) | `scaling` premium — budget acima de 3 mil dólares por dia | Atribuição com modelagem server-side avançada e identity resolution. Nunca vira segunda fonte de eventos pra Meta |

**Fluxo de decisão:**

1. Pergunte: "Você já tem algum app de tracking ou pixel instalado na loja (Wetracked, Triple Whale, Aimerce, Elevar, Stape, outro)?"
2. **Nenhum** → o Wetracked das ETAPAS 1-2 é o stack. `analytics_stack: "wetracked"`.
3. **Outro app como fonte de eventos** (Elevar, Stape, Omega, Trackify, CAPI de outro app) → migrar pro Wetracked: instalar o Wetracked, desligar a fonte antiga, re-verificar no Events Manager que sobrou uma fonte server-side só.
4. **Membro em `scaling` com Triple Whale ou Aimerce** (ou querendo instalar) → o Wetracked continua a fonte de eventos pra Meta; a ferramenta entra só como camada de leitura, com o envio de eventos pra Meta dela DESLIGADO (o Sonar do Triple Whale e o container server-side do Aimerce mandando pra Meta junto com o Wetracked duplicam). `analytics_stack: "triple_whale"` ou `"aimerce"`.
   - **Triple Whale**: TW Pixel instalado pra leitura + Meta Ads conectado. **Puxe o mapa de modelos antes de confirmar** (rode `Triple Whale janela 14 dias TA click-through only NC-ROAS nunca decisão por ad`): janela default de 14 dias, modelo TA e click-through only NÃO são intercambiáveis, NC-ROAS é a leitura de cliente novo, e a regra da fonte: **nunca decidir no nível do anúncio individual** por esses números (quem mata ou escala criativo é a régua da `ad-analysis` e da `scale-engine`). Deixe os modelos escolhidos anotados no relatório pra `ad-analysis` ler depois.
   - **Aimerce**: Aimerce Pixel pra leitura + identity resolution funcionando. **Puxe antes de recomendar** (rode `database de 280 milhões de americanos, resolver visitante anônimo em email e endereço, 150x de ROI`): software de identity resolution que transforma visitante anônimo em email ou endereço é **legal nos EUA e ILEGAL na Europa**; loja com tráfego ou entrega na União Europeia NÃO liga essa camada, e a ressalva vai por escrito no relatório junto da recomendação.

**Camadas complementares (qualquer stage — baratas, e não competem com o Wetracked):**

- **Survey pós-compra de atribuição (camada 3 do stack)** (rode `how did you first hear about us survey pós-compra follow-ups condicionais response rate` — a mesma entrada existe indexada em `market-research-voc` como `post purchase survey how did you first hear about us follow up condicional atribuicao`; é o MESMO sistema, puxe uma vez e reuse): pergunta **"how did you first hear about us?"** na página de agradecimento, com follow-ups condicionais conforme o canal respondido, e acompanha a **response rate** como qualificador do dado. Custa quase nada, funciona em qualquer stage e é a única camada imune a cookie/iOS — recomende desde o starter. As respostas viram VOC que a Skill `market-research` reusa.
- **Camada on-site (comportamento na página)** (rode `bounce exit rate time on page page value comparar entre paginas similares heatmap scroll`): as **4 métricas de página** — bounce, exit rate, time on page e page value, sempre comparadas **entre páginas similares**, nunca em absoluto — cruzadas com os **3 relatórios do Hotjar** (heatmap, scroll, recording). Instalar aqui (free tier serve) é o que garante que a `consistency-audit` e a `ad-analysis` tenham dado de comportamento pra ler depois: o pixel mede quem chega; essa camada mede o que a página faz com quem chegou.

Gravar a escolha em `manifest.tracking.analytics_stack` (bloco aninhado — ver "Atualizar manifest").
