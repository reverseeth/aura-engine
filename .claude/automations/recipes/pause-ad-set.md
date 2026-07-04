# Recipe: Pause Ad Set (PGS guard)

## Triggers
- "pausa o ad set [name]"
- "PGS disparou, pausa [name]"
- "emergency stop [name]"

## Input
- `ad_set_name` ou `ad_set_id`
- `reason` — opcional, pra log ("cpa_exceeded", "frequency_high", "manual")

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

A insights API não tem campo `cpa` — pedir os campos crus e derivar (mesma `derive_metrics` da receita `sync-campaign-from-meta.md`):

**Caminho 1 — MCP oficial:**
```
insights = mcp__meta__ads_insights_performance_trend(
  entity_id=ad_set_id,
  date_preset="last_3d",
  fields=["spend", "impressions", "clicks", "ctr", "frequency",
          "cost_per_action_type", "actions"]
)
cpa_3d = derive_metrics(insights, ad_set.created_time)["cpa"]
```

**Caminho 2 — Pipeboard:**
```
insights = meta_ads.insights(
  ad_set_id,
  date_preset="last_3d",
  fields=["spend", "impressions", "clicks", "ctr", "frequency",
          "cost_per_action_type", "actions"]
)
cpa_3d = derive_metrics(insights, ad_set.created_time)["cpa"]
```

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
  "reason": "<cpa_exceeded | frequency_high | manual>",
  "snapshot": {
    "cpa_3d": "<derivado>",
    "target_cpa": "<do manifest>",
    "frequency": "<N>",
    "ctr": "<N>",
    "spend_3d": "<N>"
  }
}
```

Mensagem (estrutura — valores reais do snapshot):
```
✓ Ad set <ad_set_name> pausado.
  Motivo: CPA $<cpa_3d> vs target $<target_cpa> (+<pct>%)
  Frequency estava em <freq> (fatigue iminente se > 1.4)

  Sugestão: rodar Skill 11 pra analysis + Skill 08 pra refresh
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

## Integração com o loop criativo
A receita `creative-loop.md` pode RECOMENDAR esta pausa quando os triggers
convergem (CPA > threshold + freq > 1.4 + spend > 80% do daily budget) — mas a
execução SEMPRE passa por confirmação do membro. Não existe pause autônomo no
framework hoje (o "Shadow Brain" citado em versões antigas é conceito futuro,
não implementado).
