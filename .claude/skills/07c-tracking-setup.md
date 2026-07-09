---
name: tracking-setup
description: Engine de instalação e validação de tracking pré-launch. Instala o Meta Pixel + Conversions API (CAPI) na loja, valida o Event Match Quality (EMQ) ≥ 6.0 na escala 0-10 do Events Manager (com o caminho pending_traffic pra loja pré-launch sem volume: instalação verificada + pedido-teste validando o Purchase destravam o launch com emq_pending), e escolhe o analytics stack correto por member-stage (Meta App / Wetracked / Triple Whale / Aimerce). Grava o bloco manifest.tracking que destrava os pré-flights da 08 e da 10. Roda DEPOIS do deploy da página (07b) e ANTES dos criativos (08). Use quando o membro disser "tracking", "pixel", "capi", "analytics setup", "configurar tracking", ou após a página estar no ar.
---

# Tracking Setup — Pixel + CAPI + Analytics Stack

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

1. Leia `workspace/profile.md` — em especial `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). **TODO output interno desta skill (relatório de setup, decision tree, instruções) e toda conversa com o membro usam esse idioma.** Esta skill não gera copy consumidor-final, então a regra de "copy pública sempre em inglês" não tem objeto aqui.
2. Leia `manifest.json` → `stage` (starter / validating / scaling) e `budget_daily` (o valor numérico canônico de $/dia, gravado pela 00; fallback em manifest legado: `budget_tier` ou o `profile.md`). **O stage é o que define o analytics stack recomendado** (ver decision tree); o budget refina. Detecção automática de stage em `.claude/rules/member-stage-awareness.md` se o campo estiver ausente.
3. Consulte a base Aura sobre: CAPI e Pixel Data setup (Advanced Matching + Event Match Quality), Ad Account e Pixel-Dataset Setup, Estrutura de Assets Anti-Ban, deduplicação browser↔server (event_id), eventos padrão do funil (PageView → ViewContent → AddToCart → InitiateCheckout → Purchase). Use `deep=true`.

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
| **≥ 8.0** (Great) | PASS. `tracking_ready: true`. Seguir pra ETAPA 4. |
| **6.0–7.9** (Good/OK) | PASS com recomendação. Tracking destravado, mas sub-ótimo: recomendar Advanced Matching completo (email + phone + nome + endereço no checkout) e re-medir em 24-48h (precisa de tráfego pra recalcular). `tracking_ready: true` com `emq_warn: true`. |
| **Sem dados por falta de tráfego** (loja pré-launch: Pixel + CAPI instalados corretamente E os 5 eventos do funil confirmados no Test Events, mas dataset sem volume pro escore calcular) | **PASS condicional (`pending_traffic`)** — não é falha de configuração, é ausência de tráfego: o EMQ só existe com eventos reais, e exigir escore antes do primeiro ad criaria um impasse (sem tracking_ready a 10 não roda tráfego; sem tráfego o EMQ nunca calcula). Gravar `emq.status: "pending_traffic"`, `emq.score: null`, e no manifest `tracking_ready: true` + `emq_pending: true`. **Obrigatório antes de fechar:** validar o Purchase de ponta a ponta com um **pedido-teste real** — Bogus Gateway num tema de preview (sem cobrança) OU pedido real de ~$1 + refund — e confirmar o evento Purchase chegando com a dupla-coluna (Browser + Server) no Events Manager. A Skill 11 re-lê o EMQ no dia 3 de tráfego; EMQ < 6.0 pós-tráfego = ação corretiva (voltar a esta skill). |
| **< 6.0 COM volume de eventos** | BLOCK. Pixel ou CAPI mal configurado (o escore existe e está baixo — é config, não falta de dados). **Escape (ES1):** ofereça **(A)** rodar o diagnóstico abaixo e re-medir, OU **(B)** prosseguir marcando `manifest.skipped_preflight += ["emq_gate"]` e avisando que 08/10 vão herdar tracking fraco (`tracking_ready: false`, membro aceitou o risco). |

**Diagnóstico de EMQ baixo** (rodar antes de qualquer "prosseguir mesmo assim"):
- CAPI OFF ou sem Advanced Matching (Data sharing abaixo de Maximum) → ETAPAS 1-2.
- Data sharing em "Optimized" pausou o envio (loja sem tráfego) → ETAPA 1 passo 3 ("Always on").
- Sem volume: dataset novo precisa de ~algumas dezenas de eventos pra calcular o escore. Se a loja não teve tráfego ainda, o número pode estar vazio — não é erro, é falta de dados → caminho **`pending_traffic`** da tabela acima (exige o pedido-teste validando o Purchase).
- Pixel duplicado (hardcoded + nativo, ou CAPI 1-clique por cima da nativa) → dedup quebrada → ETAPAS 1-2.

### ETAPA 4 — Analytics Stack (decision tree por member-stage)

A Skill 11 (ad-analysis) depende de atribuição confiável. Antes do launch, fixar a stack certa. **Considerar APENAS estas 4 opções** — NUNCA sugerir Elevar, Stape, Littledata, Segment, GTM server-side custom, ou qualquer CDP enterprise (complexidade desnecessária / fora de escopo).

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
   - **Triple Whale**: TW Pixel instalado + **Sonar** (server-side) ON + Meta Ads conectado.
   - **Aimerce**: Aimerce Pixel + container server-side ativo + identity resolution funcionando.

Se o membro usa stack **≠** das 4 acima, PARAR e alinhar antes de seguir — dados ruins inviabilizam a Skill 11 depois.

Gravar a escolha em `manifest.tracking.analytics_stack` (bloco aninhado — ver "Atualizar manifest").

### ETAPA 5 — Verificação final + handoff

Antes de declarar pronto, confirmar a checklist (responde 08/10):

- [ ] Pixel conectado ao Dataset correto (bate com o ad account da 10)
- [ ] Data sharing do pixel em **"Always on"** (não "Optimized")
- [ ] 5 eventos do funil disparando (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)
- [ ] CAPI ON (Data sharing = Maximum) + Advanced Matching ON (dupla-coluna Browser + Server), sem fonte server-side duplicada (CAPI 1-clique)
- [ ] EMQ ≥ 6.0 no Purchase (ou `emq_warn` documentado; ou `pending_traffic` com Purchase validado por pedido-teste e `emq_pending: true` no manifest)
- [ ] Analytics stack escolhido e instalado/confirmado

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/07c-tracking-setup/` antes de salvar.

`workspace/[produto]/07c-tracking-setup/tracking-setup.md` contendo:
1. Status do pixel (Dataset ID, canal nativo, data sharing "Always on", eventos confirmados)
2. Status do CAPI (nível de Data sharing, Advanced Matching, dedup, fonte única server-side)
3. EMQ medido (escore 0-10 do Purchase) + caminho de verificação usado (MCP oficial / Pipeboard / manual)
4. Analytics stack escolhido + razão (stage + budget) + passos de setup/confirmação
5. Checklist final da ETAPA 5
6. Próximos passos (checkout/AOV → criativos)

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

> "Tracking pronto. Pixel `[Dataset ID]` conectado (data sharing 'Always on'), CAPI ON com Advanced Matching, e os 5 eventos do funil disparando. Event Match Quality em **[X]/10** (`[pass/warn]`) [SE `pending_traffic`: "Event Match Quality ainda **sem escore** — normal em loja pré-launch, o EMQ só calcula com tráfego real. Validei o Purchase de ponta a ponta com o pedido-teste, então o launch está destravado (`emq_pending`); no dia 3 de tráfego a análise re-lê o escore e corrige se vier abaixo de 6"]. Analytics stack: **[stack escolhido]** (escolhido pelo seu stage `[stage]` + budget).
>
> Isso destrava os criativos e a campanha — eles exigem exatamente esse pixel + CAPI com EMQ ≥ 6/10 que a gente acabou de validar.
>
> Próximo passo: diga **'checkout'** pra configurar upsell/bump/bundle (Skill 07d — ela ajusta o AOV e o CPA que o briefing de ad usa, então vem ANTES dos criativos). Depois dela, a ordem de launch segue: **'bonus delivery'** (05 Fase A, se a oferta tem bônus) → **'retention'** (13 Fase A — flows de recuperação: abandoned cart + post-purchase, a infraestrutura que se arma ANTES de ligar tráfego) → **'creatives'** (08).
>
> Primeira versão dos próximos passos como referência — se quiser ajustar a stack de tracking ou re-medir o EMQ depois de rodar tráfego, é só me chamar."

---

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) `manifest.tracking.tracking_ready` reflete o status REAL do EMQ (não gravar `true` com escore < 6.0 MEDIDO sem o membro ter aceitado o risco; o caminho `pending_traffic` só grava `true` com os 5 eventos confirmados + Purchase validado por pedido-teste + `emq_pending: true`); (2) `manifest.tracking.analytics_stack` é uma das 4 opções canônicas e bate com o stage; (3) `07c-tracking-setup/dados.json` + `tracking-setup.md` + `tracking-setup.html` salvos, `.html` com logo SVG, `emq.score` na escala 0-10; (4) Dataset ID do pixel é consistente com o ad account que a Skill 10 vai usar; (5) manifest atualizado (`skills_completed`, bloco aninhado `tracking` completo — `pixel_installed`/`capi_active`/`emq_score`/`analytics_stack`/`tracking_ready` —, `updated_at`); (6) data sharing do pixel confirmado em "Always on" e sem fonte CAPI duplicada. Issue dentro do escopo → fix inline. Conflito que exige decisão do membro (ex: dois pixels ativos, qual manter) → surface curto.
