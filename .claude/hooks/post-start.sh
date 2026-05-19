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

  # Instala o pre-commit guard local (proteção mecânica contra commit do workspace)
  install_pre_commit_guard "$AURA_HOME"

  # Marca que já rodou hoje — não roda de novo até o próximo dia
  touch "$FLAG_DAILY" 2>/dev/null || true
}

# Instala o hook git pre-commit local apontando pro guard versionado.
# Idempotente: se já está instalado e correto, não faz nada.
install_pre_commit_guard() {
  local aura_home="$1"
  local hook_target="$aura_home/.git/hooks/pre-commit"
  local guard_source="$aura_home/.claude/hooks/pre-commit-guard.sh"

  # Só age se estamos num clone git válido com hooks dir
  [ -d "$aura_home/.git/hooks" ] || return 0
  [ -f "$guard_source" ] || return 0

  # Garante que o guard tem permissão de execução
  chmod +x "$guard_source" 2>/dev/null || true

  # Se já existe e aponta pro guard, nada a fazer
  if [ -f "$hook_target" ] && grep -q "pre-commit-guard.sh" "$hook_target" 2>/dev/null; then
    return 0
  fi

  # Se existe outro pre-commit (de outra ferramenta tipo husky/pre-commit framework),
  # preserva ele e adiciona chamada ao guard como ESTÁGIO ADICIONAL
  if [ -f "$hook_target" ]; then
    # Backup e wrap
    cp "$hook_target" "${hook_target}.aura-backup"
    cat > "$hook_target" <<EOF
#!/bin/bash
# Aura Engine + hook original combinados
set -e

# 1. Roda hook original primeiro
if [ -f "${hook_target}.aura-backup" ]; then
  bash "${hook_target}.aura-backup" "\$@" || exit \$?
fi

# 2. Roda guard da Aura
bash "$guard_source" "\$@"
EOF
  else
    # Cria hook novo apontando pro guard
    cat > "$hook_target" <<EOF
#!/bin/bash
# Aura Engine pre-commit guard
exec bash "$guard_source" "\$@"
EOF
  fi

  chmod +x "$hook_target"
  echo "[aura] pre-commit guard instalado em .git/hooks/pre-commit (protege workspace/ e segredos)"
}

# Execução simples sem flock se não disponível
if ! command -v flock >/dev/null 2>&1; then
  run_hook
fi
