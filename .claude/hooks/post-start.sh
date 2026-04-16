#!/bin/bash
set -euo pipefail

# Detecta shell rc (zsh default, bash se BASH_VERSION setado, WSL = bash)
SHELL_RC="${HOME}/.zshrc"
if [ -n "${BASH_VERSION:-}" ] || ( [ -r /proc/version ] && grep -qi microsoft /proc/version 2>/dev/null ); then
  SHELL_RC="${HOME}/.bashrc"
fi

# Garante que o arquivo existe
[ -f "$SHELL_RC" ] || { mkdir -p "$(dirname "$SHELL_RC")"; touch "$SHELL_RC"; }

# Adiciona alias apenas se ainda nao existir
if ! grep -q "^alias aura=" "$SHELL_RC" 2>/dev/null; then
  {
    echo ""
    echo "# Aura Engine — added by post-start hook on $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "alias aura='cd ~/aura-engine && claude'"
  } >> "$SHELL_RC"
  echo "[aura] alias 'aura' adicionado a $SHELL_RC — recarregue o shell ou rode: source $SHELL_RC"
else
  echo "[aura] alias 'aura' ja configurado em $SHELL_RC"
fi
