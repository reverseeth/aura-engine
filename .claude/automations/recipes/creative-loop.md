# Recipe: Creative Loop (semi-autônomo, com gate humano)

Loop **ad → performance → nova variação** num ritual de ~15 minutos. É o playbook que operadores sérios rodam em 2026 (ciclo de ~24-48h alimentando o sistema de entrega da Meta com pool criativo diverso) — sem SaaS intermediário. A receita NÃO inventa nada novo: ela encadeia peças que já existem no framework (sync → leitura da Skill 11 → rotação da Skill 08 → upload), com **2 gates humanos obrigatórios** no meio.

**Semi-autônomo de propósito:** oferta, estrutura de conta e PUBLICAÇÃO ficam sempre sob decisão humana. O loop prepara tudo; o membro aprova e ativa.

## Triggers
- "roda o loop criativo"
- "creative loop"
- "ciclo de criativos" / agendado pelo membro (ex: toda manhã pós-teste)

## Guardrails (INEGOCIÁVEIS — checar ANTES de qualquer ação)

| Guardrail | Regra | Fonte |
|---|---|---|
| **Nunca publish autônomo** | Toda variação nova sobe em `PAUSED`; pause de ad/ad set só com confirmação do membro. O loop NUNCA ativa nada. | doutrina Skill 10 ETAPA 6 |
| **Janela de teste intocável** | Campanha com < 72h de dados → o loop SÓ observa (nenhuma recomendação de mexer). Mexer cedo destrói o sinal. | Skill 10 ETAPA 5 |
| **Spend cap** | Ler `loop_spend_cap_daily` do manifest (default = `test_budget_daily` da 10). O cap vale sobre o budget da **CAMPANHA** — é lá que o CBO vive; ad set de teste não tem budget próprio, só o `daily maximum` de proteção. O loop nunca recomenda budget total acima do cap; subir o cap é decisão explícita do membro, fora do loop. | membro |
| **Piso de ROAS** | Se ROAS da campanha < `breakeven_roas` (04 `unit_economics`), ZERO recomendação de escala — só refresh criativo + apontar diagnóstico da Skill 11. | Skill 04/12 |
| **Incrementos < 20%** | Ajuste de budget recomendado por ciclo ≤ +20% (default +5%, estilo "farmer" da Skill 12) — incremento maior reseta a learning phase. | Skill 12 |
| **Estrutura respeitada** | 1 campanha com CBO → N ad sets (1 ad set = 1 conceito) → 3 criativos cada. O loop troca CRIATIVOS **dentro do ad set do conceito correspondente**; nunca cria campanha nova nem empilha conceitos diferentes no mesmo ad set. Ad set novo existe só pra conceito NOVO, dentro do teto de capacidade (Step 5). Diversificação em campanha ABO paralela continua sendo Skill 12, pós-breakthrough. | contrato da Skill 10 + cânone `.claude/lib/ad-taxonomy/README.md` §1/§5 |
| **Compliance** | Toda variação nova passa pelos gates da Skill 08 (compliance pre-flight + disclosure "AI Info" se humano fotorrealista gerado por AI). | pre-launch-gates |

## Pre-flight
- [ ] `manifest.10_campaign_id` existe (campanha criada pela 10 / full-deploy) e campanha ATIVA
- [ ] Campanha com ≥ 72h de dados desde a última mudança estrutural
- [ ] MCP Meta conectado (cascade oficial → Pipeboard — ver `.claude/lib/mcp-detect/README.md`)
- [ ] `04-offer-builder/dados.json` (`unit_economics.breakeven_roas`, target CPA) + `10-ad-strategy/dados.json` disponíveis — deste último, `ad_sets[]` (o mapa conceito → ad set: `concept_id`, `name`, `ad_set_id`, `ad_ids`, `daily_max_spending_limit`) e `test_capacity` (`max_adsets`, `adsets_planned`, `binding_constraint`)
- [ ] `manifest.target_cpa` disponível (e `manifest.10_ad_set_ids` pra resolver os ad sets por ID, mais robusto que por nome)
- [ ] (Opcional) Higgsfield MCP (`mcp__higgsfield__*`) — com ele, as variações saem RENDERIZADAS; sem ele, saem como prompts pro membro gerar

## Fluxo (5 steps, 2 gates humanos)

### Step 1 — Pull de performance

```
invoke_recipe("sync-campaign-from-meta", {
  campaign_id: manifest.10_campaign_id,
  date_preset: "last_7d"
})
```

A receita de sync resolve o cascade sozinha e salva `raw-pull-[timestamp].json` com um **`ad_class` pré-classificado por ad** (`breakthrough` · `spend_winner` · `kpi_winner` · `loser` · `unclassified`) — as 4 classes do cânone §2, mais `unclassified` pra quem ainda não tem base pra ser lido. É esse o campo que o Step 2 consome. O `outcome` que vem ao lado (`winner|neutral|loser|zero_conversions|insufficient_data`) existe só por compatibilidade com o enum do Creative DNA Registry: **não se lê pra decidir nada** — ele achata `spend_winner` e `kpi_winner` no mesmo `neutral`, apagando justamente a distinção que decide.

O `ad_class` do pull é **pré-classificação, não veredito**: quem manda é o recálculo da Skill 11 no Step 2, com a análise completa. Ad `unclassified` é o caso normal de teste jovem, nunca sinal negativo.

### Step 2 — Leitura (doutrina da Skill 11, versão resumida)

Aplicar sobre o pull em **dois níveis**: por AD (o criativo) e por AD SET (o conceito). Com N ad sets sob CBO, onde o algoritmo concentra gasto ENTRE conceitos já é informação — e o criativo novo precisa saber a qual conceito pertence pra saber onde subir.

- **Classificação:** as 4 classes do cânone `.claude/lib/ad-taxonomy/README.md` §2 (`loser` · `kpi_winner` · `spend_winner` · `breakthrough`), calculadas pela Skill 11 e lidas em `11-ad-analysis/dados.json` (`breakthroughs[]`). **Só `breakthrough` vira variação** no Step 4: ad que bate o KPI com pouco spend é `kpi_winner`, tratado como loser pra decisão — rotacionar em cima dele multiplica ruído. O teste mental "seguraria com 3× o budget?" é a versão rápida da mesma pergunta.
- **KILL candidates:** as réguas do cânone §3 — conta madura: ad set com 7 dias sem spend e sem KPI; conta nova: ad que gastou ≥ 8× o target CPA sem nenhuma purchase; ad novo overspendando: 24-48h de carência antes de qualquer decisão. **Não existe régua "1-2× breakeven CPA sem venda"** — a essa altura a chance de zero vendas por puro acaso ainda é alta, e matar ali descarta criativo bom por ruído.
- **Sub-entrega isolada não é sentença:** sob CBO, ad set sem gasto pode ser simplesmente o algoritmo escolhendo outro conceito. Registrar como sinal, nunca como motivo de kill sozinho.
- **Sinal de fadiga:** frequency diária > 1.4 + CPA subindo → candidato a refresh mesmo sem kill.
- **Checks de precedência:** antes de culpar criativo, conferir funil (ATC→purchase), CPM da conta e `dataset_health` (EMQ < 6/10 infla CPA por undercounting). Problema estrutural → recomendar Skill 11 completa, não mexer em criativo.

> Ambiguidade em qualquer leitura (dados contraditórios, spend baixo demais pra concluir) → parar o loop e recomendar a Skill 11 completa. O loop é o ritual rápido; a 11 é o diagnóstico profundo.

### Step 3 — GATE HUMANO 1: digest de decisões

Apresentar ao membro um digest curto (não relatório — o relatório é da Skill 11):

```
LOOP CRIATIVO — ciclo de <data>

Campanha <nome> (CBO $<N>/dia) | spend 7d $<N> | ROAS <N> (breakeven <N>) | CPA médio $<N> (target $<N>)

POR CONCEITO (ad set): <concept_id> — spend $<N> (<N>% da campanha), CPA $<N>
MANTER (saudáveis): <ad> (conceito <concept_id>)
PAUSAR (régua do cânone §3 disparou): <ad> (conceito <concept_id>) — motivo: <8× target CPA sem purchase | ad set 7d sem spend e sem KPI>
GERAR VARIAÇÕES DE (breakthroughs): <ad> (conceito <concept_id>) — CPA $<N>, spend share <N>% da conta
BUDGET: <manter | sugerir +5% no budget da campanha (dentro do cap $<N>/dia) | piso de ROAS não atingido — sem escala>

Aprova? (pode aprovar parcial: "pausa só X, gera variação só de Y")
```

**Sem aprovação → nada acontece.** Com aprovação parcial, executar só o aprovado:
- Pausas aprovadas → pause de **ad individual**: `mcp__meta__ads_update_entity(entity_id=ad_id, entity_type="ad", status="PAUSED")` (ou o equivalente Pipeboard). O loop pausa o AD, nunca o ad set: pausar o ad set inteiro é matar o CONCEITO, decisão da régua de conta madura do cânone §3 e da Skill 11 — `pause-ad-set.md` é receita de emergência (ad set/conta), não deste loop.
- Ajuste de budget aprovado → aplicar no budget da **CAMPANHA** (é onde o CBO vive), ≤ +20% e dentro do cap. **Nunca** dar budget próprio a um ad set: o único número de budget no nível do ad set é o `daily maximum` de proteção, e mexer nele durante o teste é decisão do membro, não do loop.

### Step 4 — Gerar variações dos breakthroughs (Skill 08 + Higgsfield)

Pra cada breakthrough aprovado (só `ad_class == "breakthrough"` — `kpi_winner` e `spend_winner` não entram aqui):

```
invoke_recipe("rotate-winning-creative", {
  winner_creative_id: "<creative_id do AD breakthrough>",   // o criativo específico, não o conceito inteiro
  n_variations: 3   // 3-5; cada variação muda UM eixo (hook / voiceover / visual opening), preserva mecanismo + CTA + proof stack
})
```

Guardar o `parent_concept_id` de cada variação (o conceito do criativo-pai): é ele que resolve, no Step 5, em qual ad set a variação entra.

- A rotação usa o Creative DNA Registry (`creative-dna/`) pra preservar o que funcionou e o gate de diversidade da Skill 08 pra não subir 3 clones (criativos quase iguais contam como ~1 pro sistema de entrega da Meta).
- **Com Higgsfield MCP:** renderizar in-session (confirmar créditos com o membro antes — ETAPA 0.7 da Skill 08); salvar em `08-creative-engine/renders/`.
- **Sem Higgsfield MCP:** entregar prompts prontos; o loop pausa aqui e retoma quando o membro colar os .mp4.

### Step 5 — GATE HUMANO 2: aprovar variações + upload PAUSED

Mostrar as variações (briefing + hook + vídeo se renderizado). Membro aprova quais sobem.

**Onde cada criativo entra.** A variação herda o conceito-pai (a rotação é Sniper: muda UM eixo e preserva mecanismo, CTA e proof stack), então ela sobe no ad set DAQUELE conceito:

```
for variation in aprovadas:
    entry = strategy.ad_sets.find(concept_id == variation.parent_concept_id)
    invoke_recipe("upload-creative-to-meta", {
      creative_id: "<variation_id>",
      ad_set_name: entry.name,          // o ad set do conceito correspondente — nunca o de outro conceito
      video_path: "<renders/....mp4>",
      status: "PAUSED"
    })
```

**Conceito NOVO** (não é variação de nenhum conceito no ar — ex: batch novo da 08 entrando por fadiga): ele precisa do **próprio ad set** (cânone §1: 1 ad set = 1 conceito; empilhar no ad set de outro conceito ainda gasta, mas mata a leitura de qual conceito funcionou). Antes de criar, checar a capacidade que a Skill 10 já gravou em `test_capacity`:

- **Cabe** (ad sets no ar < `max_adsets`, e < 5 enquanto o budget diário está abaixo de US$ 1k): criar o ad set em PAUSED com a MESMA audiência broad/Advantage+ dos demais, **sem budget próprio**, com o `daily maximum` de proteção (~3× target CPA) — os mesmos parâmetros do Stage 2 de `full-deploy.md`.
- **Não cabe:** o conceito novo entra na FILA, ou substitui o ad set do conceito mais fraco (o membro escolhe qual sai). **Nunca** subir budget pra abrir vaga dentro do loop: mudar a capacidade é mudar o teste, e isso é decisão explícita do membro fora do loop (Skill 10 ETAPA 3.1).

Criar ad set é **mudança estrutural** — reinicia a janela intocável de 72h daquele ad set e precisa de aprovação explícita do membro aqui no GATE 2, nunca por aprovação implícita do digest.

Fechar com a mensagem:
```
✓ Ciclo fechado. <N> ads pausados, <N> variações subidas em PAUSED.
  <variação> → ad set <nome> (conceito <concept_id>)
  [se criou ad set novo] + ad set novo <nome> pro conceito <concept_id> (sem budget próprio, teto $<N>/dia)
  Ativa no Ads Manager quando quiser (ou: "ativa as variações v2-v4").
  Próximo ciclo recomendado: <data +24-48h>.
```

## Log

```json
// /workspace/[produto]/automation-log.jsonl (append)
{
  "timestamp": "<ISO>",
  "action": "creative_loop",
  "campaign_id": "<Meta ID>",
  "cycle_summary": {
    "ad_sets_reviewed": "<N>", "ads_reviewed": "<N>",
    "kills_recommended": "<N>", "kills_approved": "<N>",
    "variations_generated": "<N>", "variations_uploaded_paused": "<N>",
    "uploads_by_adset": { "<concept_id>": "<N>" },
    "adsets_created": "<0 | N>",
    "budget_change_pct": "<0 | +5 | ...>",
    "budget_change_level": "campaign_cbo",
    "roas_vs_floor": "<above|below>"
  },
  "gates": { "digest_approved": true, "variations_approved": true },
  "source": "<meta_mcp_official | meta_mcp_pipeboard>"
}
```

**Ad log (cânone `.claude/lib/ad-log/README.md`) — na MESMA execução de cada ação aprovada:** append em `workspace/[produto]/ad-log.md` (criar com o cabeçalho da tabela se não existir), uma linha por mudança que o loop executou na conta. Os uploads de variação são registrados pela sub-receita `upload-creative-to-meta.md` (não duplicar). Ciclo só de observação (nada aprovado) não escreve nada.

```
| YYYY-MM-DD HH:MM | ad:[creative_id] | pausado | recipe:creative-loop | [régua §3 que disparou, aprovada no gate 1] |
| YYYY-MM-DD HH:MM | budget | $[antes]→$[depois] (+5%) | recipe:creative-loop | ajuste aprovado, dentro do cap |
| YYYY-MM-DD HH:MM | adset:[concept_id] | criado em PAUSED (sem budget próprio, teto $[N]/dia) | recipe:creative-loop | conceito novo dentro da capacidade |
```

## Cadência recomendada

- **Durante teste (dias 1-3):** NÃO rodar (janela intocável).
- **Pós-teste com winner:** a cada 24-48h, idealmente de manhã (dados do dia anterior fechados).
- **Por stage do membro:** starter → 2×/semana (menos volume, menos ruído); validating → a cada 48h; scaling → diário.

## O que este loop NÃO faz (por design)

- Não ativa ads/campanhas (membro ativa)
- Não mexe em oferta, página ou estrutura de conta
- Não cria campanhas novas; ad set só cria quando um conceito NOVO entra e a capacidade da 10 comporta (Step 5). Escala estrutural — o ABO paralelo do breakthrough (cânone §5) — continua sendo Skill 12
- Não substitui a Skill 11 (o digest é a leitura rápida; diagnóstico profundo de losers, funil e conta é a 11)
- Não roda sem MCP Meta (sem dados confiáveis não há loop — cair pra Skill 11 manual)
