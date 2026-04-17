# Recipe: Upload Creative to Meta Ads

## Triggers (linguagem natural)
- "sobe o criativo [ID] pro Meta"
- "upload [ID] no ad set [name]"
- "publica o criativo [ID] pausado"

## Input esperado
- `creative_id` — do workspace ou filename (ex: `<creative-id>`)
- `ad_set_name` — nome do ad set destino (ou ID)
- `video_path` — caminho local do .mp4 final (opcional se já uploaded)
- `status` — default `PAUSED` (sempre pausado, humano ativa)

## Pre-flight
- [ ] MCP `meta-ads` conectado
- [ ] Video_path existe
- [ ] Ad set existe no ad account
- [ ] Primary text + headline + CTA já em `/workspace/[produto]/07-creatives/`
- [ ] UTM convention definida no manifest (`utm_campaign` derivado do campaign_name da strategy)

## Steps

### 1. Pegar ad set ID pelo nome
```
Via MCP:
ad_sets = meta_ads.list_ad_sets(ad_account_id, filter_by_name=ad_set_name)
ad_set_id = ad_sets[0].id
```

### 2. Upload do vídeo
```
video_id = meta_ads.video.upload(
  ad_account_id,
  source_file=video_path,
  title=creative_id,
  description=f"Aura Engine creative {creative_id}"
)
# retorna video_id, aguarda processing ~60s
```

### 3. Criar thumbnail (frame s1 do vídeo)
```
thumbnail_id = meta_ads.video.generate_thumbnail(video_id, frame_seconds=1)
```

### 4. Criar Ad Creative object
Ler `/workspace/[produto]/07-creatives/07-concept-XX.md` pra pegar:
- `primary_text_1` — primeiro Primary Text
- `headline_1` — primeira headline
- `cta_type` — default `LEARN_MORE` (ou mapear pelo briefing)
- `destination_url` — PDP link com UTM embutida

```
creative_id_fb = meta_ads.ad_creative.create(
  ad_account_id,
  name=f"Creative_{creative_id}",
  object_story_spec={
    "page_id": FACEBOOK_PAGE_ID,
    "video_data": {
      "video_id": video_id,
      "image_hash": thumbnail_id,
      "call_to_action": {
        "type": cta_type,
        "value": {"link": destination_url_with_utm}
      },
      "message": primary_text_1,
      "title": headline_1
    }
  },
  url_tags=f"utm_source=facebook&utm_medium=paid&utm_campaign={campaign_slug}&utm_content={creative_id}&utm_id={{{{ad.id}}}}"
)
```

### 5. Criar Ad (vincular creative ao ad set)
```
ad = meta_ads.ad.create(
  ad_account_id,
  name=f"Ad_{creative_id}",
  adset_id=ad_set_id,
  creative={"creative_id": creative_id_fb},
  status="PAUSED",  # sempre pausado pelo humano aprovar
  tracking_specs=[
    {"action.type": ["offsite_conversion"], "fb_pixel": [PIXEL_ID]}
  ]
)
```

### 6. Log + reporta de volta
```json
// /workspace/[produto]/automation-log.jsonl (append) — shape
{
  "timestamp": "<ISO>",
  "action": "upload_creative",
  "creative_id": "<id do briefing>",
  "ad_id_meta": "<Meta ad ID>",
  "ad_set_id": "<Meta ad set ID>",
  "video_id": "<Meta video ID>",
  "status": "PAUSED",
  "utm": "utm_source=facebook&utm_campaign=<campaign_slug>&utm_content=<creative_id>",
  "pixel_wired": true
}
```

Mensagem ao membro (estrutura):
```
✓ Criativo <creative_id> subido no Meta.
  Ad ID: <Meta ad ID> (paused)
  Ad set: <ad set name>
  UTM wired, pixel attached.

  Pra ativar: Meta Ads Manager → selecionar ad → toggle ON.
  Ou: "Claude, ativa o ad <ad_id>"
```

## Rollback
Se der erro depois de creative object criado:
```
meta_ads.ad_creative.delete(creative_id_fb)
meta_ads.video.delete(video_id)
```

## Dry-run mode
Adicionar `--dry-run` no comando simula todos os steps sem criar objetos reais
no Meta. Útil pra testar primeira vez.
