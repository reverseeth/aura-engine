#!/usr/bin/env bash
# Aura Engine — strip-metadata
# Remove todo metadado de proveniência dos criativos ANTES do upload (EXIF / XMP /
# IPTC / C2PA-JUMBF / chunks de texto como o hf-job-id do Higgsfield / tags de
# encoder), sem alterar um pixel nem um frame, e renomeia pra asset-xxxx.<ext>.
#
# Uso:
#   bash tools/strip-metadata.sh <arquivo|pasta> [...]          (limpa NO LUGAR e renomeia)
#   bash tools/strip-metadata.sh <pasta> --saida <dir>          (originais intactos)
#   bash tools/strip-metadata.sh <pasta> --recursivo
#   bash tools/strip-metadata.sh <arquivo> --verificar          (só relata)
#   bash tools/strip-metadata.sh ... --json
#
# Núcleo: tools/limpador-de-metadados/limpar.js (Node, sem dependências).
# Vídeo/áudio exigem ffmpeg (brew install ffmpeg · winget install Gyan.FFmpeg).
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v node >/dev/null 2>&1; then
  echo "erro: Node.js não encontrado (é requisito do Claude Code — Mac: brew install node · Windows: winget install OpenJS.NodeJS.LTS)" >&2
  exit 3
fi

exec node "$DIR/limpador-de-metadados/limpar.js" "$@"
