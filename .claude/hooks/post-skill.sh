#!/bin/bash
# Aura Engine: Stop hook (roda quando o assistente termina uma resposta)
#
# Descobre qual produto do workspace foi modificado nos últimos 30 minutos (mtime do
# manifest.json ou de qualquer <fase>/dados.json), roda `tools/aura-status.py <slug> --brief`
# e devolve até 10 linhas com prefixo [aura-status] ao membro. Silêncio total quando nada
# mudou, e cada mudança é reportada uma vez só (o hook guarda o mtime mais recente já
# reportado por produto em ~/.cache/aura/).
#
# Por que JSON com `systemMessage`: num hook Stop, texto puro no stdout não é mostrado ao
# membro (só em modo transcript); o campo `systemMessage` do JSON de saída é exibido na tela.
# Nunca bloqueia a resposta (não usa `decision: block`).
set -uo pipefail

AURA_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATUS="$AURA_HOME/tools/aura-status.py"
WS="${AURA_WORKSPACE:-$AURA_HOME/workspace}"

[ -f "$STATUS" ] || exit 0
[ -d "$WS" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0
cat >/dev/null 2>&1 || true        # consome o JSON de entrada do hook (não usado)

REPO_ID="$(printf '%s' "$AURA_HOME" | cksum | cut -d' ' -f1)"
CACHE="$HOME/.cache/aura"
mkdir -p "$CACHE" 2>/dev/null || true

# Produtos com manifest.json ou <fase>/dados.json modificados nos últimos 30 minutos.
changed="$(find "$WS" -mindepth 2 -maxdepth 3 \( -name manifest.json -o -name dados.json \) -mmin -30 2>/dev/null \
  | sed "s#^$WS/##" | cut -d/ -f1 | sort -u)"
[ -n "$changed" ] || exit 0

message=""
for slug in $changed; do
  [ -f "$WS/$slug/manifest.json" ] || continue
  # mtime mais recente (segundos) entre os arquivos observados deste produto
  newest="$(find "$WS/$slug" -mindepth 1 -maxdepth 2 \( -name manifest.json -o -name dados.json \) -exec stat -f %m {} + 2>/dev/null \
    || find "$WS/$slug" -mindepth 1 -maxdepth 2 \( -name manifest.json -o -name dados.json \) -exec stat -c %Y {} + 2>/dev/null)"
  newest="$(printf '%s\n' "$newest" | sort -n | tail -1)"
  stamp="$CACHE/status-${REPO_ID}-${slug}.stamp"
  last="$(cat "$stamp" 2>/dev/null || echo 0)"
  [ "${newest:-0}" -gt "${last:-0}" ] || continue      # já reportado
  out="$(python3 "$STATUS" "$slug" --brief 2>/dev/null | head -10)" || continue
  [ -n "$out" ] || continue
  printf '%s' "$newest" > "$stamp" 2>/dev/null || true
  message="${message}${message:+
}${out}"
done
[ -n "$message" ] || exit 0

python3 - "$message" <<'EOF'
import json, sys
print(json.dumps({"systemMessage": sys.argv[1]}, ensure_ascii=False))
EOF
exit 0
