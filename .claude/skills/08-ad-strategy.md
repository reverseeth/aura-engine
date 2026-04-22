---
name: ad-strategy
description: Engine de configuração da estrutura completa de campanha no Meta Ads Manager — One Campaign Method (CBO + Advantage+ placements + Broad), ad sets por conceito (3-2-2 flexible ads), naming convention rigorosa, regras de decisão por dia (1/3/7/14), PGS automated rule (5% 3x/semana), e plano de próximos batches. Use quando o membro disser "ad strategy", "estratégia de ads", "montar campanha", "setup Meta Ads", "configurar campanha", ou após os briefings de criativos estarem prontos. A skill entrega instruções STEP-BY-STEP exatas pra executar no Ads Manager.
---

# Ad Strategy Engine

## Quando Usar
Quando o membro tem criativos editados (da Skill 07) + página pronta na loja (da Skill 07) + oferta ativa (Skill 04), e precisa configurar a estrutura completa no Meta Ads Manager. Essa skill não é "estratégia conceitual" — é **executional playbook**, passo a passo.

## Antes de Começar

### Pré-flight (OBRIGATÓRIO)
- [ ] `07-creatives.json` existe
- [ ] `04-offer.json` existe (target_cpa, breakeven_roas)
- [ ] Pixel + CAPI **validados tecnicamente** (screenshot Events Manager, Match Quality ≥ 80%)
- [ ] Ads Manager acess: confirmar versao **Meta Marketing API ≥ v21.0 (Q1 2026)**
- [ ] Attribution setting validado: 7d-click, 1d-view é padrão 2026 para BR/US; em EU pode ser 28d-default — confirmar com membro
- [ ] **Analytics stack definido** — ver decision tree abaixo (sem isso o membro não vai conseguir ler dados corretamente depois)

### Analytics stack — decision tree

A Skill 09 (ad-analysis) depende de dados confiáveis de atribuição. Antes de lançar, escolher a stack correta. **Considerar APENAS 4 opções** — não sugerir Elevar, Stape, Littledata, Segment, ou qualquer outra:

| Stack | Quando recomendar | Custo | Complexidade de setup |
|-------|-------------------|-------|-----------------------|
| **Meta App nativo na Shopify** (padrão) | Budget < $1k/dia, membro early-stage, pixel simples | Grátis | Baixa (1-click install) |
| **Wetracked** | Membro quer tracking melhor que o padrão Shopify+Meta, sem pagar Triple Whale | $29-99/mês | Média |
| **Triple Whale** | Budget $1k+/dia, múltiplos canais (Meta + TikTok + Google), precisa de visão consolidada de LTV/CAC/NCROAS | $129-499/mês | Média-Alta |
| **Aimerce** | Budget > $3k/dia, membro com capital, quer AI-driven attribution com modelagem server-side avançada | $200+/mês | Alta |

**Fluxo de decisão no Pré-flight:**

1. Pergunte: "Você usa Meta App (padrão Shopify), Wetracked, Triple Whale ou Aimerce?"
2. Se "nenhum" → recomendar **Meta App nativo** (Shopify Settings > Apps > Install Meta) + CAPI ON. Baseline sempre.
3. Se membro já tem um dos quatro ativo → confirmar configuração:
   - Meta App: verificar CAPI dupla-coluna no Events Manager, match quality ≥ 80%
   - Wetracked: confirmar que pixel tá snippet enviando server-side events correlacionados
   - Triple Whale: confirmar que Pixel da TW tá instalado + Sonar (server-side) ON + Meta Ads conectado
   - Aimerce: confirmar Aimerce Pixel + server-side container ativo + identity resolution funcionando

**NUNCA** sugerir:
- Elevar / Stape / Littledata (complexidade desnecessária pro perfil do membro)
- GTM server-side custom setup (suporte inexistente)
- Segment ou CDPs (enterprise, fora do escopo do Aura Engine)

**Budget mapping (regra simples):**
- < $500/dia → Meta App bastam
- $500-$1k/dia → Meta App OU Wetracked (se membro quer ficha técnica melhor)
- $1k-$3k/dia → Triple Whale vira payback claro
- $3k+/dia → Aimerce entra como opção premium

Se o membro usa stack ≠ das 4 acima, PARAR e alinhar antes de rodar esta skill — dados ruins depois inviabilizam Skill 09.

### Compatibilidade
Esta skill foi testada em:
- Meta Ads Manager **abril 2026**
- Meta Marketing API **v21.0+**
Se membro usa interface legada (Business Suite antigo), adaptar manualmente passos visuais.

### Contexto a carregar

1. Leia `/workspace/profile.md` (budget diário — define tamanho da campanha; Meta Ads Manager conta ativa)
2. Leia `/workspace/[produto]/04-offer.md` (CPA target vem daqui — Margem / 2 pra 2× ROAS, Margem / 2.5 pra 2.5× ROAS)
3. Leia `/workspace/[produto]/05-copy.md` (URLs de destino — 1 ou múltiplas LPs)
4. Leia `/workspace/[produto]/07-creatives/` (conceitos + briefings — cada conceito vira 1 ad set)
5. Consulte a base Aura extensivamente sobre: One Campaign Method, Andromeda System (o que mudou no Meta e por que), Scientific Method for Meta Ads (control vs variable), 3-2-2 Flexible Ads format (estrutura e regras de teste), Performance Gate Scaling (PGS — regra automatizada de 5%), budget scaling methods (farmer/aggressive/operator), 4Pi Analysis signatures pra interpretação de dados depois, naming conventions, CAPI e Pixel Data setup (Advanced Matching + Event Quality), Ad Account e Pixel-Dataset Setup, Estrutura de Assets Anti-Ban, Automated Rules pra Lead Gen Campaigns, Minimum Daily Spend (por que ads ruins geram gasto), Scientific Method (control vs variable), Profitable Scaling Margin (PSM — Golden Ratio of Growth), Overview e Estratégia de Media Buying, ROAS Targets e Scaling (vertical vs horizontal). Aprofunde em cada sub-conceito. Operacional é detalhe — errar naming convention ou deixar "daily minimums" ativo mata campanhas.

## Fluxo da Skill

### ETAPA 1 — Verificação de Pré-Requisitos

Pergunte em UMA única mensagem:

"Antes de montar a campanha, confirma: Pixel + CAPI funcionando? Produto ativo na loja? Criativos prontos? Me diz 'sim' ou o que ainda falta."

**Se o membro disser "sim":** vai direto pra Etapa 2.

**Se disser o que falta:** aponte resolução por item:

- **Pixel não funcionando** → Events Manager do Meta > Test Events. Deve mostrar PageView, ViewContent, AddToCart, InitiateCheckout, Purchase. Se algum falta, verificar instalação no tema Shopify (Settings > Customer events > Meta pixel).
- **CAPI não configurada** → No Shopify (ou via Triple Whale se o membro tem), habilitar "Conversions API" no Pixel. Meta > Events Manager > Settings > Set up Conversions API. Deve mostrar dupla-coluna (Browser + Server) com ≥80% de match quality.
- **Produto não ativo** → Shopify > Products — verificar status "Active" + inventário > 0 + imagem + descrição. Link do checkout funcional.
- **Criativos não prontos** → redirecionar pra `'creatives'` (Skill 07).

Não prossiga pra Etapa 2 enquanto os 3 itens não estiverem "sim".

### ETAPA 2 — Estrutura da Campanha (One Campaign Method)

Aplique os princípios de One Campaign Method. A estrutura padrão:

**Configuração da campanha:**
- **Campaign Name**: `[Produto]_[YYYYMMDD]_Main` (ex: `CollagenSerum_20260415_Main`)
- **Objective**: **Sales** (anteriormente "Conversions" / "Purchase")
- **Budget**: **CBO** (Campaign Budget Optimization) — coloque o budget diário do membro no nível da campanha
- **Special Ad Categories**: nenhum (a menos que saúde/finanças/emprego — aí marque)
- **Advantage Campaign Budget**: ON
- **Bid strategy**: Highest Volume (padrão) — não use Cost Cap nem Bid Cap no início
- **Attribution setting**: 7-day click, 1-day view (default em 2024+)

**IMPORTANTE**: UMA ÚNICA campanha por produto. Não criar múltiplas campanhas. One Campaign Method = todos os ad sets dentro de 1 campanha CBO, Meta distribui budget.

### ETAPA 3 — Estrutura dos Ad Sets

Calcule o número máximo de ad sets ativos:

**Fórmula:** `Budget diário / Target CPA = max ad sets`

Exemplo:
- Budget $100/dia, CPA target $20 → max 5 ad sets
- Budget $300/dia, CPA target $30 → max 10 ad sets

⚠️ **Warning — distribuição CBO não-uniforme**: CBO distribui para winners, não uniformemente. Com 10 ad sets e $200/dia, se 1 winner pegar 60% ($120), os outros 9 dividem $80 ($8.8 cada — insuficiente pra learning phase).
Recomendação: começar com 3-5 ad sets, monitorar distribuição no Dia 2, podar underperformers antes de adicionar novos.

Com esse limite, distribua os ad sets:

**Tipos de ad set (dependendo do estágio do membro):**

1. **Champions** (se houver — tem winning ads anteriores): ad sets com **Post IDs dos winning creatives** (use "Use existing post" pra reaproveitar social proof acumulado — likes, shares, comments)
2. **Creative Batches**: UM ad set por conceito da Skill 07 (ex: 5 conceitos = 5 ad sets)
3. **Page Test** (se houver múltiplas LPs pra testar): ad set adicional com 3-2-2-2 (detalhe na Etapa 5)

Se o total exceder o max, priorize: Champions > Creative Batches > Page Test. Fique dentro do limite.

**Configuração de cada ad set:**

- **Ad Set Name**: `[Conceito]_[AdsetType]_[YYYYMMDD]` (ex: `RootCauseAngle_Batch_20260415`, `Champion_PostID-abc123_20260415`)
- **Conversion Event**: **Purchase** (ou sub-evento como ViewContent se estágio de teste inicial sem dados)
- **Budget**: deixar no nível da campanha (CBO distribui)
- **Schedule**: "Run set continuously starting today"
- **Audience**:
  - **Location**: mercado geográfico principal (do market research — US/UK/EU/global)
  - **Age**: **18-65+** (broad — deixar Meta otimizar por idade)
  - **Gender**: **All** (a menos que o produto seja genuinamente gênero-específico com dados claros)
  - **Detailed targeting**: **Advantage+** (automatic) — **NÃO** adicionar interests manuais. Importante: advantage+ audience está batendo manual targeting em 90%+ dos casos.
  - **Languages**: idioma do mercado
  - **Excluded**: nenhum (a menos que você tenha uma razão forte — ex: clientes existentes pra ads de aquisição)
- **Placements**: **Advantage+ Placements** (automatic) — Meta distribui entre Feed/Stories/Reels/Audience Network. Não usar manual placements.
- **Optimization goal**: Conversions > Purchase
- **Attribution**: 7-day click, 1-day view

### ETAPA 4 — Setup do 3-2-2 no Nível do Ad (Flexible Ad Format)

Para CADA ad set (exceto Champions que usam Post IDs), configure o ad usando o formato **Flexible Ad** do Meta:

- **Ad Name**: `[Conceito]_322_[YYYYMMDD]` (ex: `RootCauseAngle_322_20260415`)
- **Format**: Single Image or Video > Flexible ad > toggle ON
- **Identity**: sua Facebook Page + Instagram (mesmo handle ideal)

**3-2-2 configuration (flexible ad):**
- **3 Creatives**: upload dos 3 criativos do conceito (do briefing da Skill 07)
- **2 Primary texts**: os 2 primary texts do briefing
- **2 Headlines**: as 2 headlines do briefing
- **Descriptions**: **deixar vazio** (— descriptions raramente melhoram performance em Flexible Ad)
- **CTA Button**: "Shop Now" ou "Learn More" (Shop Now pra PDP direto, Learn More pra advertorial/LP)
- **URL**: URL da LP do conceito (do briefing)
- **URL parameters**: UTMs completos (schema obrigatório):
  ```
  utm_source=facebook
  utm_medium=paid_social
  utm_campaign=[product-slug]_[YYYYMMDD]_main
  utm_content=[concept-id]
  utm_term=[ad-set-id]
  utm_id=[meta-ad-id]   (dinâmico via {{ad.id}} macro)
  ```

### Flexible Ads vs Champion Post ID

Flexible Ads não geram Post ID único — cada criativo tem Post ID separado. Para "champion" de Flexible:
- Identificar o criativo com maior volume dentro do Flexible Ad
- Recriar esse criativo como single ad (não flexible) em novo ad set
- Rodar como "Champion" em campanha paralela
Não tente extrair Post ID do Flexible Ad — não existe.

### ETAPA 5 — 3-2-2-2 (Se Houver Teste de LPs)

Se você tem 2+ LPs pra testar (ex: PDP vs advertorial, ou 2 hero headlines diferentes), configure o 3-2-2 COM 2 URLs:

- 3 creatives + 2 primary texts + 2 headlines + **2 URLs** = 3-2-2-2
- Meta vai rotacionar as URLs automaticamente
- Após 7-14 dias, olhe os dados no breakdown por URL pra identificar qual LP converte melhor

### ETAPA 6 — Naming Convention (Standard)

Aplicar naming convention consistente em todos os níveis pra análise fácil depois:

| Nível | Format | Exemplo |
|---|---|---|
| **Campaign** | `[Product]_[Date]_Main` | `CollagenSerum_20260415_Main` |
| **Ad Set** | `[Concept]_[Type]_[Date]` | `RootCauseAngle_Batch_20260415` |
| **Ad** | `[Concept]_322_[Date]_v[N]` | `RootCauseAngle_322_20260415_v1` |

Types: `Batch` (new test), `Champion` (winning ad), `PageTest` (LP test), `Retargeting` (warm audience).

### ETAPA 7 — Regras de Decisão (Timeline Dia 1/3/7/14)

Aplique as regras. **Cada timeline tem ação específica:**

**DIA 1 (0-24h):**
- Deixar rodar. Não pausar. Não escalar.
- Verificar apenas: ads ACTIVE (não em review há > 24h), delivery rodando, spend acontecendo
- Se algum ad set não gastou nada em 24h → verificar ad set para warnings (Meta audience rejection, creative policy)

**DIA 3 (24-72h):**
- Primeiro check real. Rodar 4Pi Analysis (Spend → Frequency → CPM → Cost per Result) — mas só pra indicadores diretivos, não ação agressiva.
- **Ad set sem spend (< 10% do seu share)** em 72h → verificar se é review problema ou creative policy; se limpo, aguarde mais 48h.
- **Ad set com CPA > 3× target** em 72h → pode ser considerado pra pausa se tiver outros ad sets rodando ok (mas não pause tudo impulsivamente).

**DIA 7 (7 dias):**
- Primeira avaliação completa. Rodar Skill 09 (ad-analysis) com os dados.
- **Critério de WINNER:** CPA ≤ target + CAMPAIGN overall improved (não olha só um ad set — olha a campanha inteira) + escalou spend nos últimos 3 dias consistentemente.
- **Critério de LOSER:** sem spend em 7 dias OU CPA > 2× target após 7 dias. Pausar.
- **Critério de FADIGA:** CPM subindo + CTR caindo + frequency subindo ao longo dos 7 dias. Monitorar; pode virar fadiga em 14 dias.

**DIA 14 (2 semanas):**
- Avaliação aprofundada. Rodar Skill 09 completa.
- Ad sets que pararam de performar → pausar ou iterar (trocar criativos, refresh do conceito)
- Ad sets que escalaram bem → promover a Champion (post ID separado no próximo batch) e continuar
- Planejar próximo batch de conceitos (Skill 07 de novo)

### ETAPA 8 — Performance Gate Scaling (PGS) — Regra Automatizada Exata

Aplique os princípios de PGS.

**Configure no Ads Manager:**

Menu: **Automated Rules** > **Create New Rule** > Apply to: **All active ad sets in campaign `[Nome da Campanha]`**

**Conditions (IF) — sintaxe exata do operador no Ads Manager:**
1. CPA **is less than** `{target_cpa * 0.9}` nos últimos 3 dias
2. AND Spend **is greater than** `{target_cpa * 2}` nos últimos 3 dias
3. AND Frequency **is less than or equal to** `1.3` nos últimos 7 dias

**Action (THEN):**
- **Increase daily budget by** — `5%`
- **Apply to**: `Ad set`

**Schedule:**
- **Run rule**: **3x/semana** — Monday / Wednesday / Friday (ou Tue/Thu/Sat)
- **Time window**: Last 3 days
- **Time**: 10:00 AM local

**Notifications:** ON (receber email quando a regra dispara pra auditar)

**Resultado prático**: ad sets que estão performando dentro do target recebem aumento de 5% no budget em cada trigger. 5% × 3× semana = ~15% por semana = dobra em ~30 dias. Escala vertical sistemática sem reativar fase de aprendizado.

**IMPORTANTE** (): PGS é SEGURO porque só escala ad sets que JÁ estão dentro do target. Não escala impulsivamente. Não desestabiliza algoritmo.

### ETAPA 9 — Próximos Batches

Documente pro membro como operar o ciclo:

**Quando adicionar conceito novo:**
- Sempre que um conceito existente pausar (LOSER) ou entrar em fadiga
- Sempre que quiser expandir pra novo ângulo (ex: champion já tá MOF, adicionar TOF novo)
- Gerar novo batch via Skill 07 (gera briefings) e adicionar como novo ad set na mesma campanha

**Quando promover Winner pra Champion:**
- Ad set tem CPA consistentemente dentro do target por 14+ dias E escalou spend E PGS vem subindo budget
- Ação: gerar Post ID do criativo vencedor (o "campeão" do 3-2-2), criar novo ad set "Champion" apontando pra esse Post ID, mesmo audience + placement, mesmo URL. Pausar o ad set Creative Batch original.
- Por que: Post ID acumula social proof (likes, shares, comments) que melhora performance adiante.

**Quando substituir Loser:**
- CPA > 2× target por 7 dias → pausar imediatamente
- Aumentar budget dos ad sets que estão performando bem (via PGS) OU adicionar conceito novo da próxima fase de criativos

### ETAPA 10 — Erros Comuns a Evitar ()

### Unit de decisão (importante)
- **Ad level** (criativo individual): só pause se rejeitado por policy ou claramente broken (CTR < 0.3% em 48h com spend > 2× CPA target)
- **Ad set level** (audience + placement + budget): unit primária de pause/scale. Tome decisões aqui baseado em CPA/ROAS.
- **Campaign level**: raramente pause; só se campanha inteira tá off-brand ou conflito com outra campanha

Regra de ouro: **pause ad set, não ad individual**, a menos que seja erro crítico no ad.

1. **NÃO escalar budget sem razão** — se o ad set tá dentro do target, PGS cuida. Se você subir budget manualmente +50% em um dia, desestabiliza o aprendizado. PGS a 5% é o caminho.
2. **NÃO usar daily minimums** ("atingir $X de spend") — essa regra força Meta a gastar em impressões ruins pra cumprir meta. Deixa a fluidez de CBO operar.
3. **NÃO pausar no ad level, pause no ad SET** — desligar ads individuais dentro de um 3-2-2 faz Meta re-balancear estranhamente. Se quer matar criativo, pause o ad set inteiro e lance outro com os criativos melhores.
4. **NÃO mudar audiência depois de 2-3 dias** — cada mudança reseta learning phase. Deixe rodar 7 dias antes de qualquer tweak de audience.
5. **NÃO usar interests detailed targeting** (a não ser razão muito específica) — Advantage+ está batendo manual targeting em 90%+ dos casos. Adicionar interests só reduz o pool e limita algoritmo.
6. **NÃO testar demais de uma vez** — respeitar o `budget / CPA target` limit. Mais ad sets do que isso = cada um recebe pouco spend, learning phase nunca completa, decisão impossível.

### Screenshots do Ads Manager

Nota: screenshots visuais do Ads Manager 2026 Q1 devem ser mantidos em `.claude/templates/ads-manager-screenshots/` — atualizar semestralmente. Se a interface mudar significativamente, adaptar passos da skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p /workspace/[produto]/` antes de salvar.

`/workspace/[produto]/08-ad-strategy.md` contendo:
1. Estrutura da campanha completa (Etapa 2)
2. Lista detalhada de ad sets com config de audience, placement, budget (Etapa 3)
3. Configuração 3-2-2 ou 3-2-2-2 por ad set (Etapas 4-5)
4. Naming convention aplicada a todos os nomes
5. Timeline de decisões dia 1/3/7/14 (Etapa 7)
6. PGS automated rule — setup literal pra colar no Ads Manager (Etapa 8)
7. Plano de próximos batches (Etapa 9)
8. Checklist de erros a evitar (Etapa 10)

### JSON companion — `08-ad-strategy.json`

```json
{
  "strategy_id": "uuid",
  "product_slug": "...",
  "creative_batch_ref": "07-creatives batch_id",
  "campaign": {
    "name": "...",
    "objective": "conversions",
    "budget_type": "cbo",
    "daily_budget": 150,
    "attribution": "7d_click_1d_view",
    "placements": "advantage_plus"
  },
  "ad_sets": [],
  "pgs_rules": [],
  "utm_schema": {}
}
```

### Atualizar manifest

Após salvar, atualizar `/workspace/[produto]/manifest.json`:
- Adicionar `08-ad-strategy` em `skills_completed`
- Registrar `strategy_id`, `creative_batch_ref`, e `pgs_enabled: true/false`

## Mensagem Final

"Estrutura de ads pronta. Campanha `[nome]` montada com [N] ad sets em 3-2-2. PGS ativo (5% × 3×/semana).

Próximo passo: deixa rodar. Em **3-7 dias**, diga **'ad analysis'** e me manda os dados do Ads Manager pra rodar 4Pi completa + diagnóstico + decisões de iteração.

Enquanto isso: **não escale manualmente**. PGS cuida do que tá ganhando. Quando um conceito ganhar e tiver estável por 14 dias, a gente promove pra Champion."
