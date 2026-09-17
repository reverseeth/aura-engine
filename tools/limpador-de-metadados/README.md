# Limpador de Metadados

Remove todo metadado de proveniência dos criativos antes do upload (EXIF, XMP, IPTC, C2PA/JUMBF, chunks de texto como o `hf-job-id` do Higgsfield, comentários, tags de encoder) e renomeia cada arquivo pra `asset-xxxx.<ext>`. **Zero perda de qualidade**: imagem é reescrita byte a byte mantendo só pixel e cor; vídeo e áudio saem por stream copy do ffmpeg, sem re-encodar um frame.

## Dois jeitos de usar

**Programa (arrastar e soltar)** — 2 cliques em `Limpador de Metadados.command` (Mac) ou `Limpador de Metadados.cmd` (Windows), na pasta principal da Aura. Abre uma janela no navegador, só na sua máquina. Arraste arquivos ou pastas, ou clique pra escolher. Os limpos vão pra `Área de Trabalho/Aura Limpos` (dá pra mudar). Pra vídeo grande, use o campo "limpar uma pasta direto do computador" (não copia nada).

**Linha de comando** (o que as skills e receitas rodam):

```bash
bash tools/strip-metadata.sh <arquivo|pasta>              # limpa NO LUGAR e renomeia
bash tools/strip-metadata.sh <pasta> --saida <dir>        # originais intactos, limpos em <dir>
bash tools/strip-metadata.sh <pasta> --recursivo
bash tools/strip-metadata.sh <arquivo> --verificar        # só relata o que ainda existe
bash tools/strip-metadata.sh <pasta> --json
```

## Requisitos

- Node.js 18+ (já vem com o Claude Code) — imagens funcionam só com isso.
- ffmpeg pra vídeo/áudio: Mac `brew install ffmpeg` · Windows `winget install Gyan.FFmpeg`.

## Formatos

PNG · JPG/JPEG · WebP · GIF · MP4 · MOV · M4V · WebM · MKV · AVI · MP3 · M4A · AAC · WAV · FLAC · OGG.
HEIC/AVIF/TIFF não entram: exporte como PNG/JPG antes.

## Arquivos

- `limpar.js` — núcleo + CLI (sem dependências)
- `app.js` — servidor local + abre o navegador
- `ui.html` — a interface
