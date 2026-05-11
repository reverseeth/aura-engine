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
  filter={"name": ad_set_name}
)
ad_set_id = entities[0].id
```

**Caminho 2 — Pipeboard (fallback):**
```
if ad_set_name:
    ad_set = meta_ads.find_ad_set(ad_account_id, name=ad_set_name)
    ad_set_id = ad_set.id
```

### 2. Pegar snapshot de métricas (pra log)

**Caminho 1 — MCP oficial:**
```
insights = mcp__meta__ads_insights_performance_trend(
  entity_id=ad_set_id,
  date_preset="last_3d",
  fields=["cpa", "ctr", "frequency", "spend", "impressions"]
)
```

**Caminho 2 — Pipeboard:**
```
insights = meta_ads.insights(
  ad_set_id,
  date_preset="last_3d",
  fields=["cpa", "ctr", "frequency", "spend", "impressions"]
)
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
{
  "timestamp": "2026-04-17T15:30:00Z",
  "action": "pause_ad_set",
  "source": "meta_mcp_official | meta_mcp_pipeboard",
  "ad_set_id": "87654321",
  "ad_set_name": "<ad_set_name>",
  "reason": "cpa_exceeded",
  "snapshot": {
    "cpa_3d": 52.40,
    "target_cpa": 45.00,
    "frequency": 1.42,
    "ctr": 0.89,
    "spend_3d": 284.50
  }
}
```

Mensagem:
```
✓ Ad set <ad_set_name> pausado.
  Motivo: CPA $52.40 vs target $45.00 (+16%)
  Frequency estava em 1.42 (fatigue iminente)

  Sugestão: rodar Skill 11 pra analysis + Skill 08 pra refresh
```

## Reverse (reativar)
Comando: "Claude, reativa o ad set [name]"

**Caminho 1 — MCP oficial:**
```
mcp__meta__ads_activate_entity(entity_id=ad_set_id, entity_type="adset")
```

**Caminho 2 — Pipeboard:**
```
meta_ads.ad_set.update(ad_set_id, status="ACTIVE")
```

## Integração com PGS automático
Se Aura Shadow Brain (#1) estiver rodando, pode invocar esta receita sem input
humano quando triggers convergem (CPA > threshold + freq > 1.4 + spend > 80%
do daily budget). Requer flag `autonomous: true` no manifest do produto.
