# Limpador de Metadados

Remove todo metadado de proveniência dos criativos antes do upload (EXIF, XMP, IPTC, C2PA/JUMBF, chunks de texto como o `hf-job-id` do Higgsfield, comentários, tags de encoder) e renomeia cada arquivo pra `asset-xxxx.<ext>`. **Zero perda de qualidade**: imagem é reescrita byte a byte mantendo só pixel e cor; vídeo e áudio saem por stream copy do ffmpeg, sem re-encodar um frame.

**O arquivo limpo ocupa o lugar do original**, na mesma pasta. A troca é segura: o limpo é escrito inteiro num arquivo temporário e só então entra no lugar, então falha no meio do caminho não deixa arquivo corrompido.

## Dois jeitos de usar

**Programa (arrastar e soltar)** — 2 cliques em `Limpador de Metadados` na pasta principal da Aura. Abre uma janela no navegador, só na sua máquina. Arraste arquivos ou uma pasta, ou clique em **Escolher arquivos** / **Escolher pasta** pra abrir o seletor do próprio sistema. Pasta limpa tudo que está dentro dela, inclusive as subpastas. Nenhum caminho é digitado e nada é copiado pra lugar nenhum, então vídeo grande roda na mesma velocidade.

**Português e inglês.** A janela abre no idioma do `report_language` do `workspace/profile.md`; sem perfil, segue o idioma do navegador. O botão PT/EN no topo troca a qualquer momento, e a escolha fica guardada na máquina. O texto do terminal também sai nos dois idiomas.

**Linha de comando** (o que as skills e receitas rodam):

```bash
bash tools/strip-metadata.sh <arquivo|pasta>              # limpa NO LUGAR e renomeia
bash tools/strip-metadata.sh <pasta> --saida <dir>        # originais intactos, limpos em <dir>
bash tools/strip-metadata.sh <pasta> --recursivo
bash tools/strip-metadata.sh <arquivo> --verificar        # só relata o que ainda existe
bash tools/strip-metadata.sh <pasta> --sem-renomear       # limpa mantendo o nome do arquivo
bash tools/strip-metadata.sh <pasta> --json
```

O `--sem-renomear` existe pro arquivo que já está sendo apontado por um caminho: as imagens da página em `page/design/assets/`, por exemplo, são citadas pelo `src` do HTML e pelo `media.asset` do plano, então trocar o nome pra `asset-xxxx` quebraria os dois. Criativo que vai subir pra plataforma de ads continua no padrão: limpa e renomeia.

## O lançador de 2 cliques

Os dois lançadores são versionados em `lancadores/`. O hook de início de sessão (`.claude/hooks/post-start.sh`) copia pra raiz da Aura o do sistema que o membro está usando, e tira o outro do caminho: no Mac fica só o `.command`, no Windows só o `.cmd`. A cópia da raiz é ignorada pelo git. Dá pra usar o lançador direto de `lancadores/` também.

## Requisitos

- Node.js 18+ (já vem com o Claude Code) — imagens funcionam só com isso.
- ffmpeg pra vídeo/áudio: Mac `brew install ffmpeg` · Windows `winget install Gyan.FFmpeg`.

## Formatos

PNG · JPG/JPEG · WebP · GIF · MP4 · MOV · M4V · WebM · MKV · AVI · MP3 · M4A · AAC · WAV · FLAC · OGG.
HEIC/AVIF/TIFF não entram: exporte como PNG/JPG antes.

## Arquivos

- `limpar.js` — núcleo + CLI (sem dependências)
- `app.js` — servidor local: serve a janela e é quem mexe no disco, sempre por caminho absoluto
- `ui.html` — a interface, no design system dos relatórios da Aura
- `lancadores/` — os dois atalhos de 2 cliques

## Como o programa sabe onde o arquivo está

O navegador entrega o conteúdo do que foi arrastado, nunca o local dele no disco, e sem o local não dá pra substituir o original. Por isso:

- **Escolher arquivos / Escolher pasta** abre o seletor do próprio sistema (AppleScript no Mac, PowerShell no Windows, zenity ou kdialog no Linux), que devolve o caminho real. É o caminho mais direto.
- **Arrastar e soltar** tenta, em ordem: o caminho que alguns navegadores mandam junto (`text/uri-list`); e, se não vier, uma busca por nome, tamanho e data de modificação nas pastas de uso comum (Desktop, Downloads, Documentos, Imagens, Vídeos). Casou com um arquivo só, é ele. Casou com vários ou nenhum, o programa não age e diz pra usar o botão.
