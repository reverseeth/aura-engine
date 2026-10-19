# Social Engine · Referência: Publicação no Instagram (ETAPA 4)

> A limpeza de metadados antes de postar, onde hospedar o arquivo limpo, a cascade de publicação (API oficial do Instagram → Blotato ou Metricool → pacote pronto), as chamadas da API verificadas uma a uma, a ordem reversa que monta o grid e o TikTok opcional pelo Higgsfield. Abra na ETAPA 4.

## O que o Higgsfield faz e o que não faz

O Higgsfield gera as imagens. Ele não publica no Instagram: no MCP dele, a única publicação social que existe é pro TikTok (hoje `tiktok_connect`, `tiktok_prepare_publish` e `tiktok_publish_status`). A publicação no Instagram sai sempre por um dos degraus abaixo.

## 1. Limpe antes de qualquer upload (regra 12)

Imagem do Higgsfield carrega metadado de proveniência (C2PA, `hf-job-id`) que a Meta lê. Antes de publicar, sempre:

```bash
bash tools/strip-metadata.sh workspace/<slug>/social-engine/<data>/
```

O arquivo limpo substitui o original e ganha o nome `asset-xxxx.png`. Nenhum post sobe sem esse passo.

## 2. Hospede o arquivo limpo

A API do Instagram recebe a imagem por URL pública, não por arquivo. Suba o arquivo limpo nos **Shopify Files da própria loja** (MCP da Shopify ou Admin API: mutation `stagedUploadsCreate`, depois `fileCreate`). A URL do CDN da loja é pública e estável. Nunca use a URL original do Higgsfield: é o arquivo com metadado. (Blotato e Metricool aceitam o arquivo direto.)

## 3. A cascade de publicação

1. **API oficial do Instagram (padrão).** Grátis, sem intermediário, pelo mesmo System User da Meta que roda os anúncios (passo 3 de `.claude/automations/setup-mcps.md`, com o produto Instagram no app e as permissões `instagram_basic` e `instagram_content_publish`). Exige conta Business ou Creator ligada a uma página do Facebook. Limite da Meta: 50 posts por conta a cada 24 horas. Pronta quando há token disponível (segredo de rede na rotina, variável `META_ACCESS_TOKEN` na máquina) e o `ig_user_id` gravado em `dados.json`.
2. **Blotato ou Metricool conectado.** Alternativa de quem quer os 9 posts espaçados ao longo do dia: o agendamento fica do lado deles e o post sai no horário com o Claude fechado. Setup em `setup-mcps.md` (3.10). Detecção pelo prefixo de tool (`.claude/lib/mcp-detect/README.md`).
3. **Pacote pronto pra postar.** As 9 imagens limpas e um `legendas.md` com a legenda de cada uma, na ordem de publicação, em `social-engine/<data>/`. O caminho mais rápido pro membro é o agendamento em lote do Meta Business Suite (Planner), cerca de cinco minutos pros 9.

Se um degrau falhar, siga pro próximo sem drama. Nunca pedir senha, cookie, login ou token do Instagram no chat.

## 4. As chamadas da API, uma por vez e verificadas

O token nunca aparece no comando, no log nem no resumo. Na rotina na nuvem, o segredo de rede do ambiente injeta o cabeçalho sozinho em `graph.facebook.com` e o comando vai sem ele. Na máquina do membro, acrescente `-H "Authorization: Bearer $META_ACCESS_TOKEN"` (a variável, nunca o valor).

```bash
API=https://graph.facebook.com/v23.0
# uma vez, na ETAPA 4: o ID da conta do Instagram ligada à página (grava em dados.json → publishing.ig_user_id)
curl -s "$API/me/accounts?fields=name,instagram_business_account"
# por post:
curl -s -X POST "$API/<ig_user_id>/media" --data-urlencode "image_url=<url do Shopify Files>" --data-urlencode "caption=<legenda>"   # → {"id": "<creation_id>"}
curl -s "$API/<creation_id>?fields=status_code"                                    # repete até FINISHED
curl -s -X POST "$API/<ig_user_id>/media_publish" -d "creation_id=<creation_id>"   # → {"id": "<media_id>"}
curl -s "$API/<media_id>?fields=permalink"                                         # confirma que está no ar
```

Cada post só começa quando o anterior foi confirmado pelo `permalink`. Erro de limite em leitura: espera e tenta de novo com intervalo crescente. Erro no `media_publish`: confere com `GET /<ig_user_id>/media?fields=caption,timestamp&limit=3` se o post não subiu mesmo antes de qualquer nova tentativa, porque repetir às cegas duplica o post. `ERROR` no `status_code`: o arquivo ou a URL estão errados; refaça a hospedagem, não a publicação. Se a versão `v23.0` for recusada, troque pela versão corrente do changelog da Graph API.

## 5. Ordem de publicação

O Instagram mostra o post mais novo no canto superior esquerdo. Pra o grid 3x3 aparecer montado no perfil, publique na ordem reversa da fórmula: posição 9 primeiro, posição 1 por último.

## 6. TikTok (opcional)

Se o membro pedir, os mesmos posts viram carrossel ou vídeo curto no TikTok pelo Higgsfield (conectar a conta uma vez com `tiktok_connect`, depois `tiktok_prepare_publish`). Também passa pelo Limpador antes.

## 7. Onde fica salvo

`social-engine/dados.json` → `publishing`: `{ "path": "instagram_api | publisher | package", "tool": "instagram_api | blotato | metricool | null", "ig_user_id": "...", "hosting": "shopify_files | publisher_upload", "spacing_minutes": 0 }` e, a cada lote, uma linha em `posts_log[]`: `{ "date": "YYYY-MM-DD", "position": 1, "template_id": "...", "file": "asset-xxxx.png", "caption_hook": "...", "media_id": "...", "permalink": "...", "status": "published | scheduled | package" }`.
