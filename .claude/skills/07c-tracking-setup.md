---
name: tracking-setup
description: Engine de instalação e validação de tracking pré-launch. Instala o Meta Pixel + Conversions API (CAPI) na loja, valida Match Quality ≥ 80% no Events Manager, e escolhe o analytics stack correto por member-stage (Meta App / Wetracked / Triple Whale / Aimerce). Roda DEPOIS do deploy da página (07b) e ANTES dos criativos (08) — é a skill que destrava os pré-flights de pixel/CAPI da 08 e da 10. Use quando o membro disser "tracking", "pixel", "capi", "analytics setup", "configurar tracking", ou após a página estar no ar.
---

# Tracking Setup — Pixel + CAPI + Analytics Stack

## Quando Usar

Quando a página já está deployada na loja (Skill 07b) e o membro precisa garantir que cada visita e compra seja medida ANTES de gastar dinheiro com ads. Hoje as Skills 08 (creatives) e 10 (ad-strategy) exigem no pré-flight "Pixel + CAPI validados, Match Quality ≥ 80%" — mas nenhuma skill construía isso. Esta é a skill que constrói e valida.

É uma skill **operacional** (passo a passo pra executar no Shopify + Events Manager), não conceitual. Sem ela, os criativos da 08 e a campanha da 10 viram dinheiro queimado por falta de sinal de conversão.

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)

- [ ] `workspace/[produto]/manifest.json` existe e é parseável
- [ ] `07b-page-build` está em `skills_completed` (página no ar) — sem página deployada, ViewContent/AddToCart/Purchase não têm onde disparar
- [ ] `04-offer.json` existe (a skill lê `daily_budget`/`budget_tier` pra mapear o budget da decision tree do analytics stack)
- [ ] Acesso ao Shopify admin da loja + uma conta Meta Business (Business Manager + ad account + um Pixel/Dataset)

**Arquivo de pré-flight faltante (escape path, rule ES1):** se `manifest.json` não parseia, NÃO aborte seco — ofereça **(A)** rebuild do manifest (inspeciona `workspace/[produto]/` e reconstrói, perguntando budget/stage), OU **(B)** restore do backup mais recente (`.manifest-backup-*.json`). Ver `.claude/rules/emergency-escape-paths.md` ES2.

Se `07b-page-build` NÃO está em `skills_completed`, ofereça: **(A)** rodar `build page` (07b) agora pra subir a página, OU **(B)** prosseguir só com a instalação do pixel + CAPI marcando `manifest.skipped_preflight += ["07b-page-build"]` e avisando no output final que a validação de eventos de funil (ViewContent/AddToCart/Purchase) fica incompleta até a página existir.

### Gate de consistência (Skill 09) — não-bloqueante aqui

A 09 gateia o **launch** (Skill 10), não o tracking. Esta skill pode rodar antes ou depois da 09. Se `09-consistency-audit.json` existir com `launch_recommendation == "BLOCK"`, apenas registre no output final que o launch está bloqueado até a 09 passar — mas siga instalando o tracking normalmente (ter pixel pronto não gasta dinheiro).

### Contexto a carregar

1. Leia `workspace/profile.md` — em especial `report_language` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). **TODO output interno desta skill (relatório de setup, decision tree, instruções) e toda conversa com o membro usam esse idioma.** Esta skill não gera copy consumidor-final, então a regra de "copy pública sempre em inglês" não tem objeto aqui.
2. Leia `manifest.json` → `stage` (starter / validating / scaling) e `daily_budget` / `budget_tier`. **O stage é o que define o analytics stack recomendado** (ver decision tree). Detecção automática de stage em `.claude/rules/member-stage-awareness.md` se o campo estiver ausente.
3. Consulte a base Aura sobre: CAPI e Pixel Data setup (Advanced Matching + Event Match Quality), Ad Account e Pixel-Dataset Setup, Estrutura de Assets Anti-Ban, deduplicação browser↔server (event_id), eventos padrão do funil (PageView → ViewContent → AddToCart → InitiateCheckout → Purchase). Use `deep=true`.

### Detecção de MCP (cascade)

A instalação do pixel é feita no Shopify admin (a Meta gerencia o snippet via integração nativa); o MCP entra na **verificação de Match Quality** e na leitura de datasets. Cascade:

- **Caminho 1 — MCP oficial Meta** (`mcp.facebook.com/ads`): tools `mcp__meta__ads_*`. Usar `ads_get_datasets` / equivalente de insights de dataset pra ler Event Match Quality programaticamente, sem screenshot manual.
- **Caminho 2 — Pipeboard** (`mcp__meta-ads__*`): fallback automático quando o oficial está indisponível.
- **Caminho 3 — manual**: o membro tira screenshot do Events Manager mostrando a dupla-coluna (Browser + Server) e o Match Quality, e cola pra você validar visualmente.

Logue qual caminho foi usado no campo `source` do JSON de saída (convenção em `.claude/lib/mcp-detect/README.md`). Se nenhum MCP estiver presente, o Caminho 3 (manual) é o normal — não é degradação.

## Fluxo da Skill

### ETAPA 1 — Instalar o Meta Pixel

A integração nativa Shopify↔Meta gerencia o pixel sem editar tema. Passos pra colar no admin:

1. **Shopify admin > Settings > Apps and sales channels > Facebook & Instagram** (instalar o canal "Facebook & Instagram" se ainda não estiver). Conectar o Business Manager e o ad account corretos.
2. Em **Settings > Customer events** (a antiga "Customer events" do checkout), confirmar que existe um **Meta pixel** conectado ao Dataset/Pixel ID certo. Se a loja usa Checkout Extensibility, o pixel é adicionado como **Custom pixel** ou via o app Meta — NÃO colar o snippet hardcoded no `theme.liquid` (duplica eventos e quebra dedup).
3. Confirmar que o **Pixel ID** no Shopify bate com o Pixel/Dataset que o ad account vai usar na Skill 10. Mismatch aqui = eventos no dataset errado, campanha cega.

> **Por que não hardcodar no tema:** snippet manual no `theme.liquid` + pixel da integração nativa = evento duplicado sem `event_id` consistente, derrubando Match Quality e inflando contagem de Purchase. Deixe a integração nativa ser a única fonte do pixel.

**Eventos do funil a confirmar** (Events Manager > Test Events, navegando a loja): `PageView`, `ViewContent` (PDP), `AddToCart`, `InitiateCheckout`, `Purchase`. Se algum falta, o problema está na integração nativa (re-conectar o canal) ou no tema (PDP sem o trigger de ViewContent).

### ETAPA 2 — Ativar a Conversions API (CAPI)

CAPI envia os mesmos eventos pelo servidor (server-side), redundante ao browser, deduplicados por `event_id`. É o que mantém o tracking vivo com iOS/ad-blockers/cookie loss.

1. **Shopify > Settings > Customer events** (ou no app Meta) — habilitar **Conversions API** pra o pixel conectado. A integração nativa Shopify↔Meta já envia server-side events com `event_id` pareado ao browser (dedup automático) — confirmar que o toggle está ON.
2. **Advanced Matching** ON — envia email/telefone/nome hasheados (SHA-256) com cada evento. É o maior driver de Match Quality. Confirmar que o checkout está passando customer data pro CAPI.
3. **Events Manager > [seu Dataset] > Settings** — confirmar **"Conversions API"** ativa e a fonte (Partner Integration: Shopify) listada.

> **Dedup (event_id):** cada evento precisa do MESMO `event_id` no browser e no servidor pra Meta não contar duas vezes. A integração nativa faz isso. Se você vir Purchase contado em dobro no Events Manager, a dedup quebrou (geralmente pixel hardcoded + nativo coexistindo — voltar à ETAPA 1).

### ETAPA 3 — Validar Match Quality ≥ 80% (gate técnico)

Este é o **gate que destrava 08 e 10**. Sem ≥ 80%, os criativos e a campanha rodam com sinal degradado.

**Caminho 1/2 (MCP oficial/Pipeboard):** ler o Event Match Quality / dataset quality score do dataset via tool de insights de dataset. Capturar o score numérico.

**Caminho 3 (manual):** pedir ao membro:
> "Abre o **Events Manager > seu Dataset > Overview**. Me manda print de: (1) a dupla-coluna Browser + Server nos eventos Purchase/AddToCart, e (2) o **Event Match Quality** (geralmente em Settings ou no card do evento). Quero ver número ≥ 80%."

**Decisão do gate:**

| Match Quality | Ação |
|---|---|
| **≥ 80%** | PASS. `tracking_ready: true`. Seguir pra ETAPA 4. |
| **60–79%** | WARN. Tracking funciona mas sub-ótimo. Recomendar ligar Advanced Matching completo (email + phone + nome + endereço no checkout) e re-medir em 24-48h (precisa de tráfego pra recalcular). `tracking_ready: true` com `match_quality_warn: true`. |
| **< 60% ou sem dados** | BLOCK. Pixel ou CAPI mal configurado, OU ainda sem volume de eventos. **Escape (ES1):** ofereça **(A)** rodar o diagnóstico abaixo e re-medir, OU **(B)** prosseguir marcando `manifest.skipped_preflight += ["match_quality"]` e avisando que 08/10 vão herdar tracking fraco. |

**Diagnóstico de Match Quality baixo** (rodar antes de qualquer "prosseguir mesmo assim"):
- CAPI OFF ou sem Advanced Matching → ETAPAS 1-2.
- Sem volume: dataset novo precisa de ~algumas dezenas de eventos pra calcular o score. Se a loja não teve tráfego ainda, o número pode estar vazio — não é erro, é falta de dados. Nesse caso, marcar `match_quality: "pending_traffic"` e seguir (o primeiro tráfego de ad vai popular).
- Pixel duplicado (hardcoded + nativo) → dedup quebrada → ETAPA 1.

### ETAPA 4 — Analytics Stack (decision tree por member-stage)

A Skill 11 (ad-analysis) depende de atribuição confiável. Antes do launch, fixar a stack certa. **Considerar APENAS estas 4 opções** — NUNCA sugerir Elevar, Stape, Littledata, Segment, GTM server-side custom, ou qualquer CDP enterprise (complexidade desnecessária / fora de escopo).

| Stack | Stage / quando recomendar | Custo | Setup |
|---|---|---|---|
| **Meta App nativo na Shopify** (baseline) | `starter` — budget < $1k/dia, pixel simples | Grátis | Baixo (1-click) |
| **Wetracked** | `validating` — quer tracking melhor que Shopify+Meta sem pagar Triple Whale | $29-99/mês | Médio |
| **Triple Whale** | `scaling` — budget $1k+/dia, múltiplos canais (Meta + TikTok + Google), precisa visão consolidada de LTV/CAC/NCROAS | $129-499/mês | Médio-Alto |
| **Aimerce** | `scaling` premium — budget > $3k/dia, capital disponível, quer atribuição AI-driven com modelagem server-side avançada | $200+/mês | Alto |

**Mapeamento por stage (default; o budget refina):**
- `starter` → **Meta App nativo** + CAPI ON. Baseline sempre. NÃO empurrar tool paga pra quem tem $500/mês.
- `validating` → **Meta App** ou **Wetracked** (se o membro quer ficha técnica melhor de atribuição).
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
   - **Meta App**: CAPI dupla-coluna no Events Manager, Match Quality ≥ 80% (já validado na ETAPA 3).
   - **Wetracked**: snippet enviando server-side events correlacionados ao pixel.
   - **Triple Whale**: TW Pixel instalado + **Sonar** (server-side) ON + Meta Ads conectado.
   - **Aimerce**: Aimerce Pixel + container server-side ativo + identity resolution funcionando.

Se o membro usa stack **≠** das 4 acima, PARAR e alinhar antes de seguir — dados ruins inviabilizam a Skill 11 depois.

Gravar a escolha em `analytics_stack` no manifest.

### ETAPA 5 — Verificação final + handoff

Antes de declarar pronto, confirmar a checklist (responde 08/10):

- [ ] Pixel conectado ao Dataset correto (bate com o ad account da 10)
- [ ] 5 eventos do funil disparando (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)
- [ ] CAPI ON + Advanced Matching ON (dupla-coluna Browser + Server)
- [ ] Match Quality ≥ 80% (ou WARN documentado / pending_traffic)
- [ ] Analytics stack escolhido e instalado/confirmado

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/07-page/` antes de salvar.

`workspace/[produto]/07-page/07c-tracking-setup.md` contendo:
1. Status do pixel (Dataset ID, canal nativo, eventos confirmados)
2. Status do CAPI (ON/OFF, Advanced Matching, dedup)
3. Match Quality medido + caminho de verificação usado (MCP oficial / Pipeboard / manual)
4. Analytics stack escolhido + razão (stage + budget) + passos de setup/confirmação
5. Checklist final da ETAPA 5
6. Próximos passos (criativos)

**Dual output `.html`** companion com o mesmo nome (`07c-tracking-setup.html`): usar `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained), abrindo o `<body>` com o bloco SVG da logo copiado LITERALMENTE de `.claude/templates/aura-logo-snippet.html` (NUNCA substituir por texto). Usar componentes aura (callout, note, danger, table-wrap, pill) — emojis ✅⚠️❌ são OK em relatório interno (rule 7 exceção).

### JSON companion — `07c-tracking.json`

```json
{
  "tracking_id": "uuid",
  "product_slug": "...",
  "generated_at": "ISO-8601",
  "report_language": "pt-BR",
  "pixel": {
    "dataset_id": "...",
    "channel": "shopify_native_meta",
    "events_confirmed": ["PageView", "ViewContent", "AddToCart", "InitiateCheckout", "Purchase"]
  },
  "capi": {
    "enabled": true,
    "advanced_matching": true,
    "dedup_event_id": true
  },
  "match_quality": {
    "score": 0.0,
    "status": "pass | warn | pending_traffic | block",
    "source": "mcp_meta_official | pipeboard | manual"
  },
  "analytics_stack": "meta_app | wetracked | triple_whale | aimerce",
  "tracking_ready": true
}
```

### Atualizar manifest

Após salvar, atualizar `workspace/[produto]/manifest.json`:
- Adicionar `07c-tracking-setup` em `skills_completed`, atualizar `updated_at`
- Gravar **`tracking_ready: true/false`** (true só se Match Quality PASS ou WARN; false se BLOCK não resolvido) — a Skill 08 e a Skill 10 leem este campo no pré-flight pra confirmar pixel/CAPI ≥ 80% sem pedir screenshot de novo
- Gravar **`analytics_stack`** com a escolha da ETAPA 4 — a Skill 10 e a Skill 11 leem pra orientar leitura de dados
- Registrar `tracking_id`

> Se `tracking_ready: false` foi gravado (membro escolheu prosseguir com Match Quality baixo via escape ES1), a 08 e a 10 vão herdar o aviso e devem alertar que os criativos/campanha rodam com sinal degradado.

## Mensagem Final

(idioma = `report_language`)

> "Tracking pronto. Pixel `[Dataset ID]` conectado, CAPI ON com Advanced Matching, e os 5 eventos do funil disparando. Match Quality em **[X]%** (`[pass/warn]`). Analytics stack: **[stack escolhido]** (escolhido pelo seu stage `[stage]` + budget).
>
> Isso destrava os criativos e a campanha — eles exigem exatamente esse pixel + CAPI ≥ 80% que a gente acabou de validar.
>
> Próximo passo: diga **'creatives'** pra eu gerar os briefings de anúncio (Skill 08). Eles já vão herdar `tracking_ready: true` do manifest, sem precisar reconferir pixel.
>
> Primeira versão dos próximos passos como referência — se quiser ajustar a stack de tracking ou re-medir Match Quality depois de rodar tráfego, é só me chamar."

---

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) `tracking_ready` no manifest reflete o status REAL do Match Quality (não gravar `true` com score < 60% sem o membro ter aceitado o risco); (2) `analytics_stack` é uma das 4 opções canônicas e bate com o stage; (3) `07c-tracking.json` + `.md` + `.html` salvos, `.html` com logo SVG; (4) Dataset ID do pixel é consistente com o ad account que a Skill 10 vai usar; (5) manifest atualizado (`skills_completed`, `tracking_ready`, `analytics_stack`, `updated_at`). Issue dentro do escopo → fix inline. Conflito que exige decisão do membro (ex: dois pixels ativos, qual manter) → surface curto.
