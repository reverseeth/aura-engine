#!/usr/bin/env bash
# Aura Engine — strip-metadata
# Remove metadados de proveniência (EXIF / XMP / IPTC / C2PA-JUMBF / chunks de texto,
# ex: hf-job-id do Higgsfield) de criativos ANTES do upload, sem alterar os pixels,
# e renomeia o arquivo pra asset-XXXXXXXX.<ext>.
#
# Uso:
#   bash tools/strip-metadata.sh <arquivo|pasta>
#
# Notas:
# - O perfil ICC é PRESERVADO (removê-lo mudaria a renderização de cor).
# - PNG com manifesto C2PA em chunk que o exiftool não alcança ganha um
#   re-encode lossless via sips (mesmo raster, chunks estranhos descartados).
# - O rótulo "AI Info" do Ads Manager continua obrigatório pra criativo com
#   humano fotorrealista gerado por IA (gate das skills 08/10) — este script
#   não substitui esse disclosure.
set -euo pipefail

if ! command -v exiftool >/dev/null 2>&1; then
  echo "erro: exiftool não encontrado. Instale com: brew install exiftool" >&2
  exit 3
fi

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "uso: bash tools/strip-metadata.sh <arquivo|pasta>" >&2
  exit 2
fi

collect() {
  if [[ -d "$1" ]]; then
    find "$1" -maxdepth 1 -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \
      -o -iname '*.webp' -o -iname '*.heic' -o -iname '*.tif' -o -iname '*.tiff' \
      -o -iname '*.mp4' -o -iname '*.mov' \)
  else
    echo "$1"
  fi
}

residual() {
  # metadados de proveniência que sobraram (ignora propriedades estruturais da imagem)
  exiftool -a -G1 -s "$1" 2>/dev/null \
    | grep -Ei '\[(JUMBF|XMP[^]]*|IPTC|ExifIFD|IFD0|C2PA)\]|hf-job|jobid|prompt|generator|ai[-_ ]?generated|c2pa' \
    || true
}

strip_one() {
  local f="$1"
  local dir base ext newname
  dir="$(dirname "$f")"
  ext="${f##*.}"

  echo "── $f"
  local before
  before="$(residual "$f")"
  if [[ -z "$before" ]]; then
    echo "   metadata de proveniência: nenhuma encontrada"
  else
    echo "   removendo:"
    echo "$before" | sed 's/^/     /' | head -12
  fi

  # 1º passe: exiftool remove EXIF/XMP/IPTC/text chunks (ICC preservado por padrão)
  exiftool -all= -overwrite_original -q "$f"

  # 2º passe: PNG com JUMBF/C2PA residual → re-encode lossless (sips) descarta chunks estranhos
  local left
  left="$(residual "$f")"
  if [[ -n "$left" && "$(echo "$ext" | tr '[:upper:]' '[:lower:]')" == "png" ]] && command -v sips >/dev/null 2>&1; then
    sips -s format png "$f" --out "$f.tmp.png" >/dev/null
    mv "$f.tmp.png" "$f"
    exiftool -all= -overwrite_original -q "$f"
    left="$(residual "$f")"
  fi

  if [[ -n "$left" ]]; then
    echo "   AVISO: metadata residual (revisar manualmente):"
    echo "$left" | sed 's/^/     /' | head -6
  else
    echo "   limpo ✓"
  fi

  # renomeia pra asset-XXXXXXXX (a menos que já siga o padrão)
  base="$(basename "$f")"
  if [[ "$base" == asset-* ]]; then
    echo "   nome mantido: $base"
  else
    newname="asset-$(openssl rand -hex 4 2>/dev/null || printf '%04x%04x' "$RANDOM" "$RANDOM").$ext"
    mv "$f" "$dir/$newname"
    echo "   renomeado: $newname"
  fi
}

count=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  strip_one "$f"
  count=$((count + 1))
done < <(collect "$TARGET")

echo "concluído: $count arquivo(s) processado(s)"
