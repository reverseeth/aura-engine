# Recipe: Pause Ad Set (pausa manual — gatilho humano, nunca regra de performance)

**O gatilho desta receita é uma LEITURA, não uma automação.** Quem decide pausar é o membro, a partir das réguas de kill do cânone `.claude/lib/ad-taxonomy/README.md` §3 aplicadas pela Skill 11. Pausar um ad set é matar o CONCEITO inteiro (1 ad set = 1 conceito, cânone §1) — decisão que nunca acontece sozinha.

**Automação por condição de performance não existe nesta estrutura.** Regra com condição de CPA, ROAS ou frequency é **recusada pelo Meta** em campanha com CBO — o erro é literalmente *"performance-related conditions are not available for assets that use CBO"* (cânone §6). Não oferecer, não tentar criar, não prometer ao membro. As três proteções que de fato existem são montadas pela Skill 10 ETAPA 6 / `full-deploy.md` Stage 4:

| Proteção | O que é | Age sozinha? |
|---|---|---|
| **`Ad set spending limit → daily maximum`** (~3× target CPA/dia) | teto de gasto no nível do ad set — não é condição de performance, por isso passa em CBO | não pausa nada; só impede o ad set de gastar além do teto |
| **Automação obrigatória A — pico de gasto** (spend 5× em 24h → pausar) | protege contra conta comprometida e contra um zero a mais digitado no budget | sim, se o membro ativou (nasce DESATIVADA) |
| **Automação obrigatória B — URL de destino ≠ domínio da loja → desligar** | protege contra ad rodando pra página errada, removida ou de terceiro | sim, se o membro ativou (nasce DESATIVADA) |

As duas automações são doutrina, não opcionais (cânone §6). Esta receita é o caminho MANUAL — ou porque a régua de kill da Skill 11 disparou na leitura, ou porque uma das duas rules não pôde ser criada pelo MCP e o membro está executando à mão o que ela faria.

**Kill automatizado por métrica de performance não se faz.** Mesmo onde o Meta aceitasse, a métrica do Ads Manager engana: ad a 1× ROAS na plataforma pode estar excelente no 1-day click de uma ferramenta de atribuição de terceiro, e desligar por metadado mata winner.

## Triggers
- "pausa o ad set [name]" / "mata o conceito [name]"
- "a proteção de pico de gasto disparou, pausa [name]"
- "os ads do [name] tão apontando pra URL errada, desliga"
- "emergency stop [name]"

## Input
- `ad_set_name` ou `ad_set_id`
- `reason` — opcional, pra log. Valores alinhados ao cânone §3 e §6:
  - `kill_7d_no_spend_no_kpi` — conta madura: 7 dias sem spend e sem KPI (régua §3)
  - `kill_8x_cpa_no_purchase` — conta nova: acumulou 8× o target CPA sem nenhuma purchase (régua §3)
  - `spend_spike_5x_24h` — proteção A do §6, executada à mão
  - `url_mismatch` — proteção B do §6, executada à mão. A rule desliga o **ad**; pausar o ad set inteiro só quando todos os ads dele apontam pra URL errada
  - `manual` — decisão do membro fora das réguas (oferta mudou, produto sem estoque, etc.)

> **Não existe `cpa_exceeded` como motivo de pause.** "CPA acima do target" não é régua de kill: no ponto de 1× o target CPA ainda existe cerca de 37% de chance de zero vendas por puro acaso, e matar ali descarta criativo bom por ruído (cânone §3). **Fadiga também não é pause:** frequency diária acima de 1.4 com CPA subindo é candidato a **refresh criativo** (Skill 08), não a matar o conceito. E ad novo overspendando tem 24-48h de carência antes de qualquer decisão.

## Pre-flight (cascade: oficial → Pipeboard)

- [ ] Detectar MCP disponível:
  - Tentar primeiro: tools `mcp__meta__ads_update_entity` (oficial, `mcp.facebook.com/ads`)
  - Fallback: tools `mcp__meta-ads__*` (Pipeboard legacy)
- [ ] Ad set existe e está ACTIVE

## Steps

### 1. Resolver ad set

**Caminho 1 — MCP oficial:**
```
ad_account = mcp__meta__ads_get_ad_accounts()[0]  # ou filtrado por escopo do membro
entities = mcp__meta__ads_get_ad_entities(
  ad_account_id=ad_account.id,
  entity_type="adset",
  filter={"name": ad_set_name},
  fields=["id", "name", "status", "created_time"]  # created_time: o step 2 usa em derive_metrics
)
ad_set = entities[0]
ad_set_id = ad_set.id
```

**Caminho 2 — Pipeboard (fallback):**
```
if ad_set_name:
    ad_set = meta_ads.find_ad_set(ad_account_id, name=ad_set_name,
                                  fields=["id", "name", "status", "created_time"])
    ad_set_id = ad_set.id
```

### 2. Pegar snapshot de métricas (pra log)

A insights API não tem campo `cpa` — pedir os campos crus e derivar (mesma `derive_metrics` da receita `sync-campaign-from-meta.md`).

**Duas janelas, porque as réguas do cânone §3 pedem coisas diferentes:** `last_7d` cobre a régua de conta madura (7 dias sem spend e sem KPI) e `maximum` cobre a de conta nova (8× target CPA acumulado sem purchase, que se lê desde que o ad set subiu). Janela de 3 dias não sustenta nenhuma das duas.

**Caminho 1 — MCP oficial:**
```
FIELDS = ["spend", "impressions", "clicks", "ctr", "frequency",
          "cost_per_action_type", "actions"]

m7   = derive_metrics(mcp__meta__ads_insights_performance_trend(
         entity_id=ad_set_id, date_preset="last_7d", fields=FIELDS),
       ad_set.created_time)
mlife = derive_metrics(mcp__meta__ads_insights_performance_trend(
         entity_id=ad_set_id, date_preset="maximum", fields=FIELDS),
       ad_set.created_time)
```

**Caminho 2 — Pipeboard:**
```
m7    = derive_metrics(meta_ads.insights(ad_set_id, date_preset="last_7d",  fields=FIELDS), ad_set.created_time)
mlife = derive_metrics(meta_ads.insights(ad_set_id, date_preset="maximum", fields=FIELDS), ad_set.created_time)
```

O snapshot é **registro do estado no momento da pausa**, não o veredito: quem classificou o ad set foi a leitura da Skill 11. Nenhum número daqui autoriza pausar por conta própria.

### 3. Pausar

**Caminho 1 — MCP oficial:**
```
mcp__meta__ads_update_entity(
  entity_id=ad_set_id,
  entity_type="adset",
  status="PAUSED"
)
```

**Caminho 2 — Pipeboard:**
```
meta_ads.ad_set.update(ad_set_id, status="PAUSED")
```

### 4. Log
```json
// shape — valores vêm do snapshot real
{
  "timestamp": "<ISO>",
  "action": "pause_ad_set",
  "source": "meta_mcp_official | meta_mcp_pipeboard",
  "ad_set_id": "<Meta ad set ID>",
  "ad_set_name": "<ad_set_name>",
  "concept_id": "<o conceito que este ad set carrega — 10-ad-strategy/dados.json → ad_sets[]>",
  "reason": "<kill_7d_no_spend_no_kpi | kill_8x_cpa_no_purchase | spend_spike_5x_24h | url_mismatch | manual>",
  "trigger": "human_read",
  "decided_by": "<skill_11 | member>",
  "snapshot": {
    "cpa_7d": "<derivado>",
    "target_cpa": "<do manifest>",
    "spend_7d": "<N>",
    "purchases_7d": "<N>",
    "spend_lifetime": "<N — base da régua de 8× target CPA>",
    "purchases_lifetime": "<N>",
    "frequency": "<N>",
    "ctr": "<N>"
  }
}
```

`trigger` é fixo em `human_read`: não existe caminho nesta receita em que uma condição de performance dispare a pausa sozinha.

**Ad log (cânone `.claude/lib/ad-log/README.md`) — na MESMA execução:** append em `workspace/[produto]/ad-log.md` (criar com o cabeçalho da tabela se não existir):

```
| YYYY-MM-DD HH:MM | adset:[concept_id] | pausado | recipe:pause-ad-set | [reason — ex: kill 7d sem spend/KPI · 8× target CPA sem purchase · pico de gasto 5× · URL errada · manual] |
```

Mensagem (estrutura — valores reais do snapshot):
```
✓ Ad set <ad_set_name> pausado (conceito <concept_id> sai do teste).
  Motivo: <a régua do cânone §3 que disparou na leitura, em uma frase — ex:
           "7 dias sem spend e sem KPI" | "gastou $<spend_lifetime> (8× o target de
           $<target_cpa>) sem nenhuma purchase" | "pico de gasto 5× em 24h">

  Sugestão: rodar Skill 11 pra analysis + Skill 08 pra conceito novo no lugar
```

## Reverse (reativar)
Comando: "Claude, reativa o ad set [name]"

**Caminho 1 — MCP oficial** (mesma tool do pause, só muda o status):
```
mcp__meta__ads_update_entity(entity_id=ad_set_id, entity_type="adset", status="ACTIVE")
```

**Caminho 2 — Pipeboard:**
```
meta_ads.ad_set.update(ad_set_id, status="ACTIVE")
```

A reativação também entra no ad log, na mesma execução:

```
| YYYY-MM-DD HH:MM | adset:[concept_id] | religado | recipe:pause-ad-set | [motivo do membro] |
```

## Integração com o loop criativo

**O `creative-loop.md` não chama esta receita.** O loop pausa **ad individual** (`entity_type="ad"`), nunca ad set: matar o ad set é matar o CONCEITO, e essa decisão pertence às réguas do cânone §3 lidas pela Skill 11 — não ao ritual rápido de rotação de criativo. Esta receita é o caminho de ad set / conta.

Quando a leitura do loop encosta numa régua de conta madura (ad set 7 dias sem spend e sem KPI), o encaminhamento correto é **recomendar a Skill 11 completa**, e a pausa do conceito sai de lá — com confirmação explícita do membro, sempre.

Não existe pause autônomo por performance no framework: nem aqui, nem no loop, nem na 11, nem na 12 (cânone §6). As únicas pausas que acontecem sem um humano no meio são as duas proteções obrigatórias do §6, e só depois que o membro as ativa.
