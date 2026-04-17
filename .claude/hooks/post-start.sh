#!/bin/bash
set -euo pipefail

# Lock pra prevenir race condition quando múltiplas sessões abrem simultâneo
LOCK=/tmp/aura-post-start.lock

# Flag daily — só roda 1x por dia (evita rodar em toda sessão Claude)
mkdir -p ~/.cache/aura 2>/dev/null || true
FLAG_DAILY="$HOME/.cache/aura/hooked-$(date +%Y%m%d)"
[ -f "$FLAG_DAILY" ] && exit 0

# flock não existe em macOS por padrão; usa fallback simples com pid-file se flock ausente
if command -v flock >/dev/null 2>&1; then
  (
    exec 200>"$LOCK"
    flock -w 2 200 2>/dev/null || exit 0
    run_hook
  ) 200>"$LOCK" || true
  # Garantir exit limpo mesmo sem flock
fi

run_hook() {
  # AURA_HOME = raiz do repo (2 níveis acima do hooks/post-start.sh)
  AURA_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

  # Detecta shell com prioridade fish > bash > zsh (baseado em SHELL env ou version vars)
  CURRENT_SHELL="$(basename "${SHELL:-}")"

  if [ "$CURRENT_SHELL" = "fish" ] || [ -n "${FISH_VERSION:-}" ]; then
    SHELL_RC="${HOME}/.config/fish/conf.d/aura.fish"
    ALIAS_LINE="alias aura='cd $AURA_HOME && claude'"
  elif [ -n "${BASH_VERSION:-}" ] || ( [ -r /proc/version ] && grep -qi microsoft /proc/version 2>/dev/null ); then
    SHELL_RC="${HOME}/.bashrc"
    ALIAS_LINE="alias aura='cd $AURA_HOME && claude'"
  else
    SHELL_RC="${HOME}/.zshrc"
    ALIAS_LINE="alias aura='cd $AURA_HOME && claude'"
  fi

  # Cria o arquivo de config se não existe (sem sobrescrever existente)
  mkdir -p "$(dirname "$SHELL_RC")" 2>/dev/null || true
  [ -e "$SHELL_RC" ] || touch "$SHELL_RC"

  # Adiciona alias apenas se ainda não existir
  if ! grep -q "alias aura=" "$SHELL_RC" 2>/dev/null; then
    {
      echo ""
      echo "# Aura Engine — added by post-start hook on $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "$ALIAS_LINE"
    } >> "$SHELL_RC"
    echo "[aura] alias 'aura' adicionado a $SHELL_RC (aponta pra $AURA_HOME)"
    [ "$CURRENT_SHELL" = "fish" ] || echo "[aura] recarregue o shell ou rode: source $SHELL_RC"
  else
    echo "[aura] alias 'aura' ja configurado em $SHELL_RC"
  fi

  # Marca que já rodou hoje — não roda de novo até o próximo dia
  touch "$FLAG_DAILY" 2>/dev/null || true
}

# Execução simples sem flock se não disponível
if ! command -v flock >/dev/null 2>&1; then
  run_hook
fi
