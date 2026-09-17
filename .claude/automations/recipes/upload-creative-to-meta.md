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
- `facebook_page_id` — de `manifest.meta_page_id`; se ausente, perguntar 1× ao membro (Business Suite → Settings → Pages) e gravar `manifest.meta_page_id`
- `pixel_id` — de `manifest.meta_pixel_id`; se ausente, resolver via `mcp__meta__ads_get_dataset_details` (oficial) ou perguntar 1× ao membro (Events Manager → Data Sources) e gravar `manifest.meta_pixel_id`
- `metadata_clean` — `true` só se o arquivo já saiu do Limpador de Metadados (nome `asset-xxxx.<ext>`); senão o step 1.5 limpa antes de subir

## Cascade (detecção de prefixo — ver `.claude/lib/mcp-detect/README.md`)

**Caminho 1 — MCP oficial (`mcp__meta__ads_*`):** usado SÓ pra resolver o ad set ID e checar o account. O upload do binário em si NÃO é suportado pelo oficial (o connector remoto não recebe arquivo local — ver nota abaixo).

**Caminho 2 — Pipeboard (`mcp__meta-ads__*`):** caminho de execução real. O upload do `.mp4` local precisa de um MCP com acesso ao filesystem do membro — o oficial é remoto (`mcp.facebook.com/ads`) e não tem como ler o arquivo. Logo **o upload do vídeo + criação do creative object força Pipeboard**, mesmo quando o oficial está conectado. Se o Pipeboard não estiver disponível, cair pro Playwright headless (primeira run: login manual do membro no Meta Business + `storage_state` salvo local — fluxo descrito no `setup-mcps.md` passo 6).

**Caminho 3 — manual:** membro sobe o vídeo pelo Ads Manager e cola o resultado.

> **Por que upload força Pipeboard:** o MCP oficial é remote-hosted e só recebe IDs/parâmetros, não bytes de arquivo. Upload de mídia (`.mp4`) exige um MCP local que leia `video_path` do disco. Por isso esta receita inteira roda no Pipeboard (ou Playwright), enquanto sync/pause preferem o oficial.

## Pre-flight
- [ ] MCP Meta conectado (ver cascade acima — esta receita executa via `mcp__meta-ads__*` Pipeboard)
- [ ] Video_path existe
- [ ] Ad set existe no ad account
- [ ] `facebook_page_id` + `pixel_id` resolvidos (ver Input — manifest ou pergunta única ao membro)
- [ ] Primary text + headline + CTA já em `/workspace/[produto]/08-creative-engine/`
- [ ] UTM convention definida no manifest (`utm_campaign` derivado do campaign_name da strategy)
- [ ] Arquivo com nome `asset-xxxx.<ext>` (metadados já limpos) — senão o step 1.5 roda o limpador antes de qualquer upload

## Steps

### 1. Pegar ad set ID pelo nome
```
Via MCP:
ad_sets = meta_ads.list_ad_sets(ad_account_id, filter_by_name=ad_set_name)
ad_set_id = ad_sets[0].id
```

### 1.5. Limpar metadados (obrigatório — regra 12 do CLAUDE.md)

Se o nome do arquivo em `video_path` NÃO segue `asset-xxxx.<ext>`:
```bash
bash tools/strip-metadata.sh "<video_path>"
```
O limpador remove EXIF/XMP/C2PA/tags de encoder sem re-encodar (stream copy) e renomeia no lugar — atualize `video_path` pro nome novo (`asset-xxxx.mp4`) e grave `metadata_clean: true`. Se o ffmpeg faltar, PARE aqui e avise o membro (Mac `brew install ffmpeg` · Windows `winget install Gyan.FFmpeg`) — nenhum vídeo sobe sem limpar.

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
Ler `/workspace/[produto]/08-creative-engine/concept-XX.md` pra pegar:
- `primary_text_1` — primeiro Primary Text
- `headline_1` — primeira headline
- `cta_type` — default `LEARN_MORE` (ou mapear pelo briefing)
- `destination_url` — PDP link com UTM embutida

```
creative_id_fb = meta_ads.ad_creative.create(
  ad_account_id,
  name=f"Creative_{creative_id}",
  object_story_spec={
    "page_id": facebook_page_id,   // resolvido no Input (manifest.meta_page_id)
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
  url_tags=f"utm_source=facebook&utm_medium=paid_social&utm_campaign={campaign_slug}&utm_content={creative_id}&utm_term={{{{adset.id}}}}&utm_id={{{{ad.id}}}}"
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
    {"action.type": ["offsite_conversion"], "fb_pixel": [pixel_id]}  // resolvido no Input (manifest.meta_pixel_id)
  ]
)
```

### 6. Log + reporta de volta
```json
// /workspace/[produto]/automation-log.jsonl (append) — shape
{
  "timestamp": "<ISO>",
  "action": "upload_creative",
  "source": "meta_mcp_pipeboard",
  "creative_id": "<id do briefing>",
  "ad_id_meta": "<Meta ad ID>",
  "ad_set_id": "<Meta ad set ID>",
  "video_id": "<Meta video ID>",
  "status": "PAUSED",
  "utm": "utm_source=facebook&utm_campaign=<campaign_slug>&utm_content=<creative_id>",
  "pixel_wired": true,
  "metadata_clean": true,
  "asset_file": "asset-k3p9.mp4"
}
```

**Ad log (cânone `.claude/lib/ad-log/README.md`) — na MESMA execução:** append em `workspace/[produto]/ad-log.md` (criar com o cabeçalho da tabela se não existir), uma linha por ad criado. No motivo, o contexto real da subida (quem invocou e por quê):

```
| YYYY-MM-DD HH:MM | ad:[creative_id] | criado em PAUSED no ad set [ad_set_name] | recipe:upload-creative-to-meta | [batch inicial do full-deploy · variação de rotação do [winner_id] · reposição de fadiga · pedido do membro] |
```

Modo `--dry-run` não escreve nada (nenhuma mudança real aconteceu).

Mensagem ao membro (estrutura):
```
✓ Criativo <creative_id> subido no Meta.
  Ad ID: <Meta ad ID> (paused)
  Ad set: <ad set name>
  UTM wired, pixel attached.

  Arquivo subido: asset-xxxx.mp4 (metadados limpos)

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
