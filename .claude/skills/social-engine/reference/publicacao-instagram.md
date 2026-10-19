# Social Engine · Referência: Publicação no Instagram (ETAPA 4)

> A limpeza de metadados antes de postar, onde hospedar o arquivo limpo, a cascade de publicação (Blotato ou Metricool → API do Instagram → pacote pronto), a ordem reversa que monta o grid no perfil e o TikTok opcional pelo Higgsfield. Abra na ETAPA 4.

## O que o Higgsfield faz e o que não faz

O Higgsfield gera as imagens. Ele não publica no Instagram: no MCP dele, a única publicação social que existe é pro TikTok (hoje `tiktok_connect`, `tiktok_prepare_publish` e `tiktok_publish_status`). A publicação no Instagram sai sempre por um dos degraus abaixo.

## 1. Limpe antes de qualquer upload (regra 12)

Imagem do Higgsfield carrega metadado de proveniência (C2PA, `hf-job-id`) que a Meta lê. Antes de publicar, sempre:

```bash
bash tools/strip-metadata.sh workspace/<slug>/social-engine/<data>/
```

O arquivo limpo substitui o original e ganha o nome `asset-xxxx.png`. Nenhum post sobe sem esse passo.

## 2. Hospede o arquivo limpo

A API de publicação do Instagram e a maioria dos MCPs de publicação recebem a imagem por URL pública, não por arquivo. Se o degrau escolhido pede URL:

- **Shopify Files da própria loja** (padrão): com o MCP da Shopify ou a Admin API, suba o arquivo limpo pela mutation `stagedUploadsCreate` e registre com `fileCreate`. A URL do CDN da loja é pública e estável.
- **Upload do próprio publicador**, quando ele aceita arquivo direto (Blotato e Metricool aceitam).

Nunca use a URL original do Higgsfield: é o arquivo com metadado.

## 3. A cascade de publicação

Detecte pelo prefixo de tool na sessão (`.claude/lib/mcp-detect/README.md`). Se um degrau falhar, siga pro próximo sem drama.

1. **Publicador conectado.** Blotato (recomendado: agenda do lado dele, então o post sai no horário mesmo com o Claude fechado, e aceita arquivo ou URL) ou Metricool (agenda no melhor horário do público). Setup em `.claude/automations/setup-mcps.md` (3.10). Publique cada post com o arquivo limpo e a legenda e agende os 9 espaçados ao longo do dia.
2. **API de publicação do Instagram.** Exige conta Business ou Creator ligada a uma página do Facebook e o System User da Meta do passo 3 de `setup-mcps.md`, com o produto Instagram no app e as permissões `instagram_basic` e `instagram_content_publish`. O fluxo é criar o container com `image_url` e `caption` e depois publicar o container. Limite da Meta: 50 posts por conta a cada 24 horas. O token do System User fica na variável de ambiente `META_ACCESS_TOKEN` da máquina do membro, nunca colado no chat.
3. **Pacote pronto pra postar.** As 9 imagens limpas e um `legendas.md` com a legenda de cada uma, na ordem de publicação, em `social-engine/<data>/`. O caminho mais rápido pro membro é o agendamento em lote do Meta Business Suite (Planner), que agenda os 9 de uma vez em cerca de cinco minutos.

Nunca pedir senha, cookie ou login do Instagram ao membro.

## 4. Ordem de publicação

O Instagram mostra o post mais novo no canto superior esquerdo. Pra o grid 3x3 aparecer montado no perfil, publique na ordem reversa da fórmula: posição 9 primeiro, posição 1 por último. Entre um post e outro, pelo menos alguns minutos, ou o horário agendado do publicador.

## 5. TikTok (opcional)

Se o membro pedir, os mesmos posts viram carrossel ou vídeo curto no TikTok pelo Higgsfield (conectar a conta uma vez com `tiktok_connect`, depois `tiktok_prepare_publish`). Também passa pelo Limpador antes.

## 6. Onde fica salvo

`social-engine/dados.json` → `publishing`: `{ "path": "mcp | graph_api | package", "tool": "blotato | metricool | null", "hosting": "shopify_files | publisher_upload", "spacing_minutes": 0 }` e, a cada lote, uma linha em `posts_log[]`: `{ "date": "YYYY-MM-DD", "position": 1, "template_id": "...", "file": "asset-xxxx.png", "caption_hook": "...", "status": "published | scheduled | package" }`.
