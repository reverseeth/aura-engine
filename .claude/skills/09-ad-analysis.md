---
name: ad-analysis
description: Engine de análise de performance de Meta Ads usando 4Pi Analysis (Spend → Frequency → CPM → Cost per Result), 19-point diagnostic pra losers, extração de learnings de winners, framework de 12 perguntas (feedback loops), e recomendações acionáveis imediato/curto/médio prazo. Use quando o membro disser "ad analysis", "análise de ads", "analisar performance", "ver resultado", "diagnóstico", ou após 3-7+ dias rodando a campanha da Skill 07. Entrega decisões concretas — escalar, pausar, refresh de criativos, ou ajustar oferta/página.
---

# Ad Analysis Engine

## Quando Usar
Quando a campanha está rodando há 3+ dias e o membro precisa diagnosticar o que está acontecendo e decidir próximos passos. Esta skill NÃO é "reportar dados" — é **diagnóstico + decisão**. Sai com ações concretas (hoje / 3-7 dias / 2-4 semanas).

## Antes de Começar

### Pré-flight
- [ ] `08-ad-strategy.json` existe
- [ ] Dir `/workspace/[produto]/09-analysis/` existe (`mkdir -p`)
- [ ] Se houver análises anteriores, ler AS 2 MAIS RECENTES (para delta/trend analysis)

### Contexto a carregar

1. Leia `/workspace/profile.md` (budget — contexto pra decisões de scale)
2. Leia `/workspace/[produto]/04-offer.md` (target CPA, breakeven ROAS, margem — benchmarks pra avaliar performance)
3. Leia `/workspace/[produto]/08-ad-strategy.md` (estrutura da campanha, conceitos testados, regras de decisão)
4. Leia `/workspace/[produto]/09-analysis/` — **SE EXISTIR**, leia análises anteriores em ordem cronológica (pra ver evolução, identificar tendências, comparar com análises passadas)
5. Consulte a base Aura extensivamente sobre 4Pi Analysis (Spend/Frequency/CPM/Cost per Result completo), 4Pi Dashboard Setup (custom metrics), creative fatigue (sinais e tratamento), revisão de Ads Perdedores (diagnostic 19 pontos), revisão de Ads Vencedores e extração de ideias, Framework de 12 Perguntas pra Feedback Loops, Aplicação de Learnings pra Novos Ads, Complete a Feedback Loop, Feedback Loops como Motor de Crescimento, ROAS Targets e Scaling, Minimum Daily Spend (por que ads ruins geram gasto), PGS, winning ad rate, funnel creative playbook (positions e signatures TOF/MOF/BOF). Cada framework que existir, aplique.

## Fluxo da Skill

### ETAPA 1 — Obter Dados (AUTO via MCP, fallback manual)

**PRIMEIRO TENTE AUTO-PULL via Meta MCP (preferível):**

1. Verificar se MCP `meta-ads` está disponível:
   ```
   test_mcp = invoke("meta-ads", "ping") ou equivalente
   ```

2. Se MCP disponível:
   a. Invocar receita `sync-campaign-from-meta.md`:
      ```
      invoke_recipe("sync-campaign-from-meta", {
        campaign_name: read_manifest("08_campaign_name"),
        date_preset: "last_7d"
      })
      ```
   b. Receita salva pull completo em `/workspace/[produto]/09-analysis/raw-pull-[timestamp].json`
   c. Parse JSON em tabela estruturada internamente:

   | Ad Set | Days Running | Spend | Freq | CPM | CPC | CTR | CPA | ROAS | Thumbstop | Hold15s |
   |---|---|---|---|---|---|---|---|---|---|---|

   d. **ZERO interação com o membro nesse fluxo.** Silent pull, pronto pra ETAPA 2.

3. Se MCP falhar (não configurado, token expirado, rate limit):
   a. Logar erro em `/workspace/[produto]/09-analysis/mcp-errors.log`
   b. Fallback ao modo manual: pedir ao membro:

      "MCP do Meta Ads não respondeu (motivo: [erro]). Cola os dados aqui — screenshot ou números. Preciso ver por ad set: Spend, Frequency, CPM, CPC, Cost per Purchase, ROAS. E quantos dias cada ad set está rodando."

      ESPERE a resposta. Parse manual.

**Indicar ao membro no output final qual modo foi usado:**
- Modo auto: "Dados puxados via MCP em [timestamp]"
- Modo manual: "Dados via print do membro em [timestamp]"

Esta é a diferença entre Skill 09 sob demanda vs Skill 09 autônoma.

### ETAPA 2 — 4Pi Analysis (Ordem EXATA)

Aplique os 4 Pi's **NA ORDEM** (Spend → Frequency → CPM → Cost per Result). A ordem importa — cada Pi contextualiza o próximo.

#### Dados insuficientes — como proceder

- **Ad set rodou < 24h**: análise 4Pi é **inválida**; apenas diagnóstico qualitativo. Marque "PRELIMINAR" no output.
- **Ad set < 50 conversions**: CPA é ruído; use Spend + Freq + CPM apenas. CPA column = "insufficient data".
- **Dados faltando Frequency ou CPM** (API error): tentar refetch; se persistir, documentar como `data_gap` e pular aquele Pi.

#### CPM subindo: fadiga OU sazonalidade?

Antes de declarar "fadiga" (que justifica creative refresh), checar:
- Calendário: Q2-Q4 geralmente vê CPM subindo (holiday prep, Black Friday, Xmas)
- Benchmark setor: olhe CPM médio do seu vertical na semana atual (Meta insights ou reports de terceiros)
- Delta relativo: se seu CPM subiu 15% mas vertical subiu 20%, você está na média — NÃO é fadiga
- Só declare fadiga se CPM subiu > 20% VS vertical e freq > 1.3

#### Winner picking — ROAS ou CPA?

Para decisões de "qual ad set é melhor":
- Use ROAS quando AOV varia entre ad sets (ex: um ad set traz upsells mais)
- Use CPA quando AOV é ~estável
- **Regra**: Profit per ad spend = (AOV × CVR − CPA) — use isto se disponível

#### Pi 1: SPEND

"Quanto cada ad set recebeu de budget?"

Observação-chave: **Meta distribui spend pra onde ele ACREDITA que está funcionando**. Se o ad set A recebeu 40% do spend total e o B só 10%, o algoritmo tá "votando" que A é melhor (independente de CPA).

- **Ad set que recebeu muito spend** (share > 25% do total) → Meta tá confiante nele
- **Ad set com spend < 10% do seu share esperado** → Meta não tá confiante OU ad não foi aprovado OU audience muito pequena

Se um ad set "não gastou" em 3+ dias: verificar Ads Manager > Delivery insights + Review status. Pode ter sido pausado por policy.

#### Pi 2: FREQUENCY (Sinaliza Posição no Funil)

Aplicar as signatures:

- **Freq < 1.1** → **TOF** (Top of Funnel) — novas impressões, cold traffic
- **Freq 1.15-1.3** → **MOF** (Middle) — starting to warm up
- **Freq > 1.3** → **BOF** (Bottom) — retargeting-like, mesmas pessoas vendo várias vezes

Se a campanha tem TODOS os ad sets com freq > 1.3, falta **diversidade no funil** — você tá esgotando a audience retargetada sem abrir pra TOF novo. Recomendação: adicionar conceito TOF-friendly (hook problem, angle curiosity).

Se TODOS estão com freq < 1.1 e a campanha tá há 14+ dias, algo tá preventing Meta de re-engajar — geralmente CPM baixo + CTR muito baixo = audience não resonando.

#### Pi 3: CPM (Contexto Combinado com Freq)

**CPM isolado diz pouco. CPM + Freq diz muito:**

- **CPM alto (acima da média do nicho) + Freq alta (>1.3)** → Meta tá mandando pra audience cara (prime-time, premium placements) porque POUCA audience nova está disponível. Sinal de BOF / possível fadiga.
- **CPM alto + Freq baixa (<1.1)** → audience premium/cara mas fresca. Pode ser normal em nicho competitivo (skincare, finance, luxury).
- **CPM baixo + Freq alta** → Meta tá procurando impressões baratas com audience repetida. Frequência tá alta mas CPM não subiu = Meta não tá pagando caro pra forçar. Pode ser fadiga mas também pode ser só stabilidade.
- **CPM subindo no tempo** (comparar com análises anteriores se houver) → **possível fadiga**. Combinar com CTR falling pra confirmar.

#### Pi 4: COST PER RESULT (O Que Realmente Importa)

Compare CPA de cada ad set contra o **target CPA da oferta** (do `04-offer.md`):

- **CPA ≤ target** → WINNER (vai pro diagnóstico "scale")
- **CPA ≤ 2× target mas > target** → NEEDS OPTIMIZATION (iteração, não pausar ainda)
- **CPA > 2× target após 7 dias** → LOSER (pausar)

Contexto importante: **CPA de um ad set isolado não é tudo**. "a campanha overall melhorou?". Se campanha total está dentro de CPA target mesmo com 1-2 ad sets fora, a maquina tá OK. Otimiza os outliers, não destrua campanha.

#### LOSER threshold (dinâmico — NOVO)

**Antigo** (hardcoded): CPA > 2× target → LOSER.

**Novo** (dinâmico, do `04-offer.json`):
- `breakeven_cpa = offer.unit_economics.margin_per_unit`
- `target_cpa_1x = breakeven_cpa × 1.0`  → loss
- `target_cpa_2x = offer.unit_economics.target_cpa_for_2x`
- LOSER threshold = `breakeven_cpa × 0.8` (80% do breakeven — já tá queimando dinheiro com buffer)
- Se offer tem PSM ≥ 1.5 (high-margin), threshold = `breakeven × 0.7` (mais tolerância)
- Se offer tem PSM < 1.2, threshold = `breakeven × 0.95` (zero tolerância)

Fórmula monotônica decrescente:
```
loser_cpa = breakeven_cpa × (0.95 − 0.05 × max(0, min(3, offer.psm − 1)))
```

### ETAPA 3 — Diagnóstico Por Ad Set

Pra CADA ad set, classifique:

**WINNER:** recebeu spend, CPA ≤ target, campanha overall melhorou.
→ Ação: escala automática via PGS. Se quer escalar mais agressivo, considera promover criativo a Champion (Post ID) e adicionar ad set dedicado.

**IN FATIGUE:** CPM subindo + CTR caindo + Freq subindo ao longo dos dias (comparar com análises anteriores).
→ Ação: refresh criativo (trocar 1-2 dos 3 criativos do 3-2-2) OU adicionar novo batch de conceitos (Skill 07). **Não pausar ainda** — pode ainda estar performando acima do breakeven mesmo com sinais de fadiga.

**LOSER:** sem spend em 7 dias OU CPA > 2× target após 7 dias.
→ Ação: PAUSAR. Fazer diagnóstico profundo (Etapa 4) pra entender por que falhou.

**EM APRENDIZADO:** < 7 dias rodando, spend baixo.
→ Ação: aguardar mais 3-4 dias antes de decidir. Learning phase do Meta precisa mínimo 50 conversions.

### ETAPA 4 — Diagnóstico Profundo de LOSERS (19-Point Diagnostic)

### 19-Point Loser Diagnostic

**Camada 1: Targeting (4 pontos)**
1. Audience muito broad — CTR alto, CVR baixo
2. Audience muito narrow — CPM alto, volume baixo
3. Exclusões conflitantes (ex: excluir compradores mas campaign é de aquisição — conflito)
4. Lookalike source com baixa qualidade (seed < 500 de alta qualidade)

**Camada 2: Hook (4 pontos)**
5. Hook não promete ganho específico
6. Hook sem pattern interrupt visual (3 primeiros segundos)
7. Hook não casa com awareness stage dominante
8. Hook saturado (claim idêntico a 5+ concorrentes)

**Camada 3: Copy (4 pontos)**
9. Primary text > 125 chars (corta em mobile)
10. CTA vago ("saiba mais" vs "ativar desconto 30%")
11. Zero social proof específico
12. Benefício listado sem transformação (feature, não benefit)

**Camada 4: Offer (4 pontos)**
13. Preço quebra o budget do awareness stage
14. Garantia fraca ou ausente
15. Urgência artificial óbvia
16. Bundle não faz sentido para o público

**Camada 5: Técnico (3 pontos)**
17. Pixel Match Quality < 80%
18. Landing page carrega > 3s (mobile)
19. Mismatch ad → landing (visual/copy)

Pra cada loser, identifique **a camada onde falhou** e a hipótese específica. Documente.

### ETAPA 5 — Diagnóstico de WINNERS (Extração de Learnings)

Pra cada WINNER, extraia learnings aplicando o framework:

- **O que funcionou?** (hook específico, ângulo, formato, CTA, LP)
- **Por que funcionou?** (hipótese causal — ex: "hook de curiosity pattern interrupt em audience Problem Aware onde concorrentes usam authority-first")
- **Como replicar?** (quais elementos isolar pra usar em próximos batches — ex: "o hook 'POV: você acorda com X' pode ser template pra outros conceitos")

Learnings vão alimentar Skill 07 (creatives) no próximo batch — escreva de forma utilizável.

### ETAPA 6 — Balanço de Funil

Veja distribuição por posição de funil (dos Pi 2 — frequency signatures):
- Todos os ad sets em TOF? → funil raso, falta converter warm audience
- Todos em BOF? → falta trazer volume novo, tá escalando sobre a mesma audience
- Distribuído em TOF + MOF + BOF? → saudável

Recomendação baseada em desbalanço:
- Falta TOF → próximo batch inclui conceitos de awareness building (hook problem, curiosity, authority)
- Falta BOF → próximo batch inclui retargeting-style (offer-focused, urgency, comparison)

### ETAPA 7 — Framework de 12 Perguntas (Feedback Loops)

Aplique os princípios de "Framework de 12 Perguntas pra Feedback Loops". Aplique as perguntas aos dados:

1. Qual ad set teve maior ROAS e por quê?
2. Qual teve menor ROAS e por quê?
3. Qual criativo específico dentro dos winners tá puxando mais?
4. Houve variação significativa de performance por primary text?
5. Alguma headline se destacou?
6. Qual URL (se 3-2-2-2) converte melhor?
7. Frequency subiu mais rápido que esperado em algum ad set? (sinal de audience pequena)
8. CPM variou muito entre ad sets? (aponta pra diferenças de audience ou bidding)
9. CTR variou muito? (indicador de hook strength)
10. Conversão CTR→Purchase variou? (indicador de message match)
11. Retention no site (se tiver) — quanto tempo ficam?
12. Qual a hipótese causal principal pro resultado?

Compile respostas num bloco objetivo.

### ETAPA 8 — Recomendações Acionáveis (Imediato / Curto Prazo / Médio Prazo)

**AÇÕES IMEDIATAS (hoje/24h):**
- Pausar losers identificados na Etapa 3 (especificar quais ad sets)
- Consertar problemas técnicos identificados no 19-point (se houver)
- Verificar se PGS está ativo e disparou nos últimos dias (Automated Rules history)

**CURTO PRAZO (3-7 dias):**
- Se tem fadiga: refresh de criativos nos ad sets afetados (trocar 1-2 dos 3 no 3-2-2)
- Se falta diversidade de funil: gerar novo batch de conceitos (Skill 07) com foco na posição faltante
- Ajuste de URLs se 3-2-2-2 mostrou preferência clara de LP

**MÉDIO PRAZO (2-4 semanas):**
- Se winners estáveis: promover pra Champion (Post ID separado)
- Se CPA está melhor que target consistentemente: reavaliar se dá pra escalar mais (vertical + horizontal — delegar pra Skill 10)
- Se oferta parece ser o bloqueio: voltar pra Skill 04 e ajustar (bundle structure, guarantee, stack)
- Se página parece ser o bloqueio: voltar pra Skill 05/06 e iterar

### ETAPA 9 — Decisão de Scaling (Recomendação Clara)

Baseado no diagnóstico completo, dê uma recomendação clara:

**SE CPA dentro do target E winning ads estáveis:**
"Continue rodando. PGS vai escalar automaticamente. Se quer escalar mais agressivo OU adicionar canais novos, diga **'scale'** pra eu montar o plano."

**SE CPA ≤ 0.7× target E winning ad claro:**
"Oferta forte, ads matando. Diga **'scale'** pra montar plano de escala vertical + horizontal. Pode considerar scaling aggressive em paralelo ao PGS."

**SE CPA acima do target mas ainda abaixo de 2×:**
"Não escala. Foco em iteração. Diga **'creatives'** pra gerar novo batch baseado nos learnings desta análise."

**SE CPA > 2× target após 7+ dias:**
"Bloqueio não é só ad — pode ser oferta, página, ou audience. Vou sugerir investigação: [indicar onde está o bloqueio mais provável baseado no 19-point]. Depois de ajuste, re-roda análise em mais 7 dias."

### ETAPA 10 — Learnings Documentados (Pra Feedback Loop)

Na seção final do relatório, documente learnings que vão alimentar próximos batches:

**Hipóteses validadas** (o que ficou confirmado pelos dados):
**Hipóteses rejeitadas** (o que não confirmou):
**Hipóteses ainda em teste** (precisa mais dados):
**Ideias pra próximo batch:**

Isso é o "feedback loop motor de crescimento" — cada análise enriquece o próximo batch de criativos.

### ETAPA 11 — DNA Update (silent — feedback automático pro registry)

Pra cada criativo analisado nesta rodada:

1. Classificar outcome:
   - `winner`: CPA < target × 0.8 E spend > $300 E decile_rank 1-2
   - `loser`: CPA > target × 1.5 OU killed antes de $100 spend
   - `neutral`: demais

2. Compor performance JSON:
   ```json
   {
     "cpa": X, "ctr": Y, "roas": Z, "spend": W,
     "thumbstop_3s": A, "hold_15s": B,
     "impressions": N, "clicks": M, "purchases": P,
     "days_active": D, "decile_rank": R,
     "outcome": "winner|loser|neutral"
   }
   ```

3. Salvar em `/workspace/[produto]/creative-dna/perf-[creative-id].json`

4. Invocar silenciosamente:
   ```
   python3 .claude/lib/creative-dna/registry.py update /workspace/[produto] [creative-id] /workspace/[produto]/creative-dna/perf-[creative-id].json
   ```

5. Se total de criativos com performance ≥ 10 E (total atual % 5 == 0):
   ```
   python3 .claude/lib/creative-dna/registry.py dna /workspace/[produto] --product [slug]
   ```
   Atualiza `/workspace/[produto]/creative-dna/dna-profile.json` que será usado na próxima Skill 07.

Silent. Membro não vê. Apenas o efeito: próximo briefing começa a refletir padrões aprendidos.

### PII redaction (antes de salvar qualquer dump de Ads Manager)

Antes de persistir dados em `/workspace/`:
- Substituir Account IDs por `ACC-[hash 8 chars]`
- Substituir Pixel IDs por `PX-[hash 8 chars]`
- Remover emails em UTM/audience names (regex `[\w.+-]+@[\w.-]+\.\w+` → `[EMAIL_REDACTED]`)
- Remover telefones em audience names (regex `\+?\d{10,15}` → `[PHONE_REDACTED]`)
- Nota: manter hash dos IDs consistente entre execuções para correlacionar análises

### Output adicional — NEXT_BATCH_IDEAS.md (fecha loop 09→07)

Além de `[YYYYMMDD]-analysis.md`, gerar OBRIGATORIAMENTE:
`/workspace/[produto]/09-analysis/NEXT_BATCH_IDEAS.md`

**Critério de parada pra evitar loop infinito 09↔07:**

Antes de gerar ideias novas:
1. Se `NEXT_BATCH_IDEAS.md` já existe:
   - Ler versão anterior + ler `07-creatives.json` (criativos gerados desde última rodada)
   - Comparar: quantas ideias propostas na versão anterior **foram testadas** (viraram criativos em 07-creatives.json com performance em 09)?
   - Se `testadas < 50%` das ideias propostas na última rodada → **Não gerar novas ideias.** Retornar versão anterior intacta + adicionar seção "Validation pending: {ideia1}, {ideia2} ainda não foram testadas — priorize antes de gerar novos angles."
   - Se `testadas >= 50%` → proceder com novas ideias (baseadas em learnings das testadas)
2. Se arquivo não existe: gerar do zero normalmente.

Conteúdo (quando gerar):
- **Ângulos a testar no próximo batch de creatives** (2-3 bullets específicos)
- **Ângulos a EVITAR** (identificados como saturados ou já losers)
- **VOC phrases não usadas ainda** que aparecem em learning de review mining
- **Formatos a priorizar** (UGC vs studio vs static vs video — baseado em performance)
- **Awareness stage para focar** (se campanha atual oversserve um stage)
- **Ideias carry-over** (propostas antes, ainda não testadas)

**Skill 07 DEVE ler este arquivo no pre-flight.** Isto fecha o loop 09→07 **com critério de parada.**

### Panorama para skill 10 (scale) — handoff

Se ações próximas = 'scale', skill 10 lerá este JSON SEM precisar perguntar:
`/workspace/[produto]/09-analysis/latest.json` (cópia do último análise) com campos:

```json
{
  "current_daily_spend": 0,
  "current_cpa_avg": 0,
  "current_roas_avg": 0,
  "active_winners_count": 0,
  "active_losers_count": 0,
  "health_signals": {
    "frequency_max": 0,
    "cpm_trend": "up|flat|down",
    "creative_age_days": 0
  },
  "psm_real": 0,
  "recommended_action": "continue|scale|refresh_creatives|kill"
}
```

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `/workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `04-offer.md` → `04-offer.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana — use `.claude/templates/aura-report-template.html` como base (CSS inline, self-contained, logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html` — NUNCA substituir por texto), componentes aura).

**Garantir diretório:** `mkdir -p /workspace/[produto]/09-analysis/` antes de salvar.

Outputs em `/workspace/[produto]/09-analysis/`:
- `[YYYYMMDD]-analysis.md` (contendo todas as 10 etapas — histórico cumulativo)
- `[YYYYMMDD]-analysis.html` (companion visual)
- `NEXT_BATCH_IDEAS.md` (input pra skill 07 no próximo batch — fecha loop)
- `latest.json` (handoff pra skill 10 — schema acima)

A pasta `09-analysis/` acumula histórico — análises anteriores servem de input pra comparar evolução nas análises seguintes.

### Atualizar manifest

Após salvar, atualizar `/workspace/[produto]/manifest.json`:
- Adicionar `09-ad-analysis` em `skills_completed` (primeira vez) ou incrementar `analysis_count`
- Registrar `last_analysis_date`, `psm_real` (calculado), `recommended_action`

## Mensagem Final

Adapte baseado no diagnóstico (ver Etapa 9 — recomendação de scaling). Termine sempre com uma próxima-ação CLARA:

- Continua rodando + PGS → monitora, próxima análise em 3-7 dias
- Escala → diga `'scale'`
- Iteração de criativos → diga `'creatives'`
- Ajuste de oferta → diga `'offer'`
- Ajuste de página → diga `'copy'` ou `'page'`
- Bloqueio técnico → resolução específica + nova análise depois
