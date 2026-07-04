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
| **Spend cap** | Ler `loop_spend_cap_daily` do manifest (default = `test_budget_daily` da 10). O loop nunca recomenda budget total acima do cap; subir o cap é decisão explícita do membro, fora do loop. | membro |
| **Piso de ROAS** | Se ROAS da campanha < `breakeven_roas` (04 `unit_economics`), ZERO recomendação de escala — só refresh criativo + apontar diagnóstico da Skill 11. | Skill 04/12 |
| **Incrementos < 20%** | Ajuste de budget recomendado por ciclo ≤ +20% (default +5%, estilo "farmer" da Skill 12) — incremento maior reseta a learning phase. | Skill 12 |
| **Estrutura congelada** | 1 campanha → 1 ad set → N ads. O loop troca CRIATIVOS, nunca cria ad set/campanha nova (diversificação de estrutura é Skill 12, pós-winner). | contrato da Skill 10 |
| **Compliance** | Toda variação nova passa pelos gates da Skill 08 (compliance pre-flight + disclosure "AI Info" se humano fotorrealista gerado por AI). | pre-launch-gates |

## Pre-flight
- [ ] `manifest.10_campaign_id` existe (campanha criada pela 10 / full-deploy) e campanha ATIVA
- [ ] Campanha com ≥ 72h de dados desde a última mudança estrutural
- [ ] MCP Meta conectado (cascade oficial → Pipeboard — ver `.claude/lib/mcp-detect/README.md`)
- [ ] `04-offer-builder/dados.json` (`unit_economics.breakeven_roas`, target CPA) + `10-ad-strategy/dados.json` disponíveis
- [ ] `manifest.target_cpa` disponível
- [ ] (Opcional) Higgsfield MCP (`mcp__higgsfield__*`) — com ele, as variações saem RENDERIZADAS; sem ele, saem como prompts pro membro gerar

## Fluxo (5 steps, 2 gates humanos)

### Step 1 — Pull de performance

```
invoke_recipe("sync-campaign-from-meta", {
  campaign_id: manifest.10_campaign_id,
  date_preset: "last_7d"
})
```

A receita de sync resolve o cascade sozinha e salva `raw-pull-[timestamp].json` com outcomes pré-classificados por ad (winner / loser / neutral / zero_conversions / insufficient_data).

### Step 2 — Leitura (doutrina da Skill 11, versão resumida)

Aplicar sobre o pull, POR AD (nunca por ad set):

- **KILL candidates:** gastou 1-2× o breakeven CPA sem venda, OU sub-entrega (spend < 50% do fair share após 72h com entrega geral saudável), OU CPA > 2× target sustentado após 7 dias.
- **Winner candidates:** spend ≥ 50% do fair share, CPA ≤ target, campanha overall não piorou. Aplicar o teste mental "seguraria com 3× o budget?" antes de tratar como winner (pouco spend + ROAS alto pode ser ruído).
- **Sinal de fadiga:** frequency > 1.4 + CPA subindo → candidato a refresh mesmo sem kill.
- **Checks de precedência:** antes de culpar criativo, conferir funil (ATC→purchase), CPM da conta e `dataset_health` (EMQ < 6/10 infla CPA por undercounting). Problema estrutural → recomendar Skill 11 completa, não mexer em criativo.

> Ambiguidade em qualquer leitura (dados contraditórios, spend baixo demais pra concluir) → parar o loop e recomendar a Skill 11 completa. O loop é o ritual rápido; a 11 é o diagnóstico profundo.

### Step 3 — GATE HUMANO 1: digest de decisões

Apresentar ao membro um digest curto (não relatório — o relatório é da Skill 11):

```
LOOP CRIATIVO — ciclo de <data>

Campanha <nome> | spend 7d $<N> | ROAS <N> (breakeven <N>) | CPA médio $<N> (target $<N>)

MANTER (saudáveis): <lista>
PAUSAR (kill rule disparou): <ad> — motivo: <gastou $X sem venda | sub-entrega | CPA 2× target>
GERAR VARIAÇÕES DE (winners): <ad> — CPA $<N>, spend share <N>× o fair share
BUDGET: <manter | sugerir +5% (dentro do cap $<N>/dia) | piso de ROAS não atingido — sem escala>

Aprova? (pode aprovar parcial: "pausa só X, gera variação só de Y")
```

**Sem aprovação → nada acontece.** Com aprovação parcial, executar só o aprovado:
- Pausas aprovadas → pause de **ad individual**: `mcp__meta__ads_update_entity(entity_id=ad_id, entity_type="ad", status="PAUSED")` (ou o equivalente Pipeboard). Na estrutura 1-1-N pausa-se o AD, nunca o ad set inteiro — `pause-ad-set.md` é receita de emergência (ad set/conta), não deste loop.
- Ajuste de budget aprovado → aplicar no ad set (≤ +20%, dentro do cap).

### Step 4 — Gerar variações dos winners (Skill 08 + Higgsfield)

Pra cada winner aprovado:

```
invoke_recipe("rotate-winning-creative", {
  winner_creative_id: "<concept_id>",
  n_variations: 3   // 3-5; cada variação muda UM eixo (hook / voiceover / visual opening), preserva mecanismo + CTA + proof stack
})
```

- A rotação usa o Creative DNA Registry (`creative-dna/`) pra preservar o que funcionou e o gate de diversidade da Skill 08 pra não subir 3 clones (criativos quase iguais contam como ~1 pro sistema de entrega da Meta).
- **Com Higgsfield MCP:** renderizar in-session (confirmar créditos com o membro antes — ETAPA 0.7 da Skill 08); salvar em `08-creative-engine/renders/`.
- **Sem Higgsfield MCP:** entregar prompts prontos; o loop pausa aqui e retoma quando o membro colar os .mp4.

### Step 5 — GATE HUMANO 2: aprovar variações + upload PAUSED

Mostrar as variações (briefing + hook + vídeo se renderizado). Membro aprova quais sobem. Pra cada aprovada:

```
invoke_recipe("upload-creative-to-meta", {
  creative_id: "<variation_id>",
  ad_set_name: strategy.ad_set.name,   // o MESMO ad set — estrutura congelada
  video_path: "<renders/....mp4>",
  status: "PAUSED"
})
```

Fechar com a mensagem:
```
✓ Ciclo fechado. <N> ads pausados, <N> variações subidas em PAUSED no ad set <nome>.
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
    "ads_reviewed": "<N>",
    "kills_recommended": "<N>", "kills_approved": "<N>",
    "variations_generated": "<N>", "variations_uploaded_paused": "<N>",
    "budget_change_pct": "<0 | +5 | ...>",
    "roas_vs_floor": "<above|below>"
  },
  "gates": { "digest_approved": true, "variations_approved": true },
  "source": "<meta_mcp_official | meta_mcp_pipeboard>"
}
```

## Cadência recomendada

- **Durante teste (dias 1-3):** NÃO rodar (janela intocável).
- **Pós-teste com winner:** a cada 24-48h, idealmente de manhã (dados do dia anterior fechados).
- **Por stage do membro:** starter → 2×/semana (menos volume, menos ruído); validating → a cada 48h; scaling → diário.

## O que este loop NÃO faz (por design)

- Não ativa ads/campanhas (membro ativa)
- Não mexe em oferta, página ou estrutura de conta
- Não cria ad sets/campanhas novas (escala estrutural = Skill 12)
- Não substitui a Skill 11 (o digest é a leitura rápida; diagnóstico profundo de losers, funil e conta é a 11)
- Não roda sem MCP Meta (sem dados confiáveis não há loop — cair pra Skill 11 manual)
