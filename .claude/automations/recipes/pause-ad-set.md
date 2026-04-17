# Recipe: Pause Ad Set (PGS guard)

## Triggers
- "pausa o ad set [name]"
- "PGS disparou, pausa [name]"
- "emergency stop [name]"

## Input
- `ad_set_name` ou `ad_set_id`
- `reason` — opcional, pra log ("cpa_exceeded", "frequency_high", "manual")

## Pre-flight
- [ ] MCP `meta-ads` conectado
- [ ] Ad set existe e está ACTIVE

## Steps

### 1. Resolver ad set
```
if ad_set_name:
    ad_set = meta_ads.find_ad_set(ad_account_id, name=ad_set_name)
    ad_set_id = ad_set.id
```

### 2. Pegar snapshot de métricas (pra log)
```
insights = meta_ads.insights(
  ad_set_id,
  date_preset="last_3d",
  fields=["cpa", "ctr", "frequency", "spend", "impressions"]
)
```

### 3. Pausar
```
meta_ads.ad_set.update(ad_set_id, status="PAUSED")
```

### 4. Log
```json
{
  "timestamp": "2026-04-17T15:30:00Z",
  "action": "pause_ad_set",
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

  Sugestão: rodar Skill 09 pra analysis + Skill 07 pra refresh
```

## Reverse (reativar)
Comando: "Claude, reativa o ad set [name]"
```
meta_ads.ad_set.update(ad_set_id, status="ACTIVE")
```

## Integração com PGS automático
Se Aura Shadow Brain (#1) estiver rodando, pode invocar esta receita sem input
humano quando triggers convergem (CPA > threshold + freq > 1.4 + spend > 80%
do daily budget). Requer flag `autonomous: true` no manifest do produto.
