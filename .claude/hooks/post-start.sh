#!/bin/bash
# Aura Engine — SessionStart hook
#
# Toda sessão: instala o pre-commit guard (barato e idempotente — se o hook git
# sumiu num re-clone/git clean, volta na próxima sessão, não no dia seguinte).
# 1x por dia POR CLONE: configura o alias `aura` no shell do membro + auto-update
# do framework (fetch + merge fast-forward only, ver auto_update abaixo).
set -euo pipefail

# AURA_HOME = raiz do repo (2 níveis acima do hooks/post-start.sh)
AURA_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Identificador do clone — quem mantém 2+ clones na mesma máquina (ex: 2 contas
# Shopify) tem flag e lock separados; um clone não "rouba" o flag diário do outro.
REPO_ID="$(printf '%s' "$AURA_HOME" | cksum | cut -d' ' -f1)"

# Lock pra prevenir race condition quando múltiplas sessões abrem simultâneo
LOCK="/tmp/aura-post-start-${REPO_ID}.lock"

# Flag daily — alias/auto-update só rodam 1x por dia por clone
mkdir -p "$HOME/.cache/aura" 2>/dev/null || true
FLAG_DAILY="$HOME/.cache/aura/hooked-$(date +%Y%m%d)-${REPO_ID}"

# ============================================================================
# Funções (definidas ANTES de qualquer chamada — bash resolve funções em runtime)
# ============================================================================

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

# Adiciona o alias `aura` no rc do shell DO USUÁRIO.
# A decisão vem de $SHELL (shell de login do membro) — NUNCA de BASH_VERSION,
# que está sempre setado dentro de um script #!/bin/bash e mandaria o alias
# pro ~/.bashrc mesmo em macOS/zsh (onde ele nunca carrega).
setup_alias() {
  local current_shell shell_rc alias_line
  current_shell="$(basename "${SHELL:-}")"

  case "$current_shell" in
    fish)
      shell_rc="${HOME}/.config/fish/conf.d/aura.fish"
      ;;
    bash)
      shell_rc="${HOME}/.bashrc"
      ;;
    zsh)
      shell_rc="${HOME}/.zshrc"
      ;;
    *)
      # $SHELL ausente/desconhecido: WSL costuma ser bash; macOS moderno é zsh
      if [ -r /proc/version ] && grep -qi microsoft /proc/version 2>/dev/null; then
        shell_rc="${HOME}/.bashrc"
      else
        shell_rc="${HOME}/.zshrc"
      fi
      ;;
  esac

  alias_line="alias aura='cd $AURA_HOME && claude'"

  # Cria o arquivo de config se não existe (sem sobrescrever existente)
  mkdir -p "$(dirname "$shell_rc")" 2>/dev/null || true
  [ -e "$shell_rc" ] || touch "$shell_rc"

  # Adiciona alias apenas se ainda não existir
  if ! grep -q "alias aura=" "$shell_rc" 2>/dev/null; then
    {
      echo ""
      echo "# Aura Engine — added by post-start hook on $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo "$alias_line"
    } >> "$shell_rc"
    echo "[aura] alias 'aura' adicionado a $shell_rc (aponta pra $AURA_HOME)"
    [ "$current_shell" = "fish" ] || echo "[aura] recarregue o shell ou rode: source $shell_rc"
  else
    echo "[aura] alias 'aura' ja configurado em $shell_rc"
  fi
}

# Auto-update do framework — mantém o membro na última versão sem gesto manual.
# Só APLICA o update quando TODAS as condições valem:
#   - repo git com remote `origin` e branch atual == main
#   - working tree limpo (arquivos RASTREADOS — workspace/ é gitignored e nunca é tocado)
#   - atrás do origin/main e fast-forwardable
# NUNCA: merge não-ff, stash, reset, tocar em workspace/.
# Opt-out: arquivo .claude/.no-auto-update OU env AURA_AUTO_UPDATE=0.
#
# TRANSPARÊNCIA (essencial): quando há update disponível mas alguma condição
# bloqueia, o membro é AVISADO com o motivo específico — nunca silêncio.
# O agente da sessão vê o aviso e resolve com segurança (protocolo no CLAUDE.md,
# seção AUTO-UPDATE). Silêncio total só em: já atualizado, opt-out, ou rede
# indisponível (aí tenta de novo no dia seguinte).
auto_update() {
  [ -f "$AURA_HOME/.claude/.no-auto-update" ] && return 0
  [ "${AURA_AUTO_UPDATE:-1}" = "0" ] && return 0

  git -C "$AURA_HOME" rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 0
  git -C "$AURA_HOME" remote get-url origin >/dev/null 2>&1 || return 0

  # O fetch roda ANTES dos gates locais: mesmo com o clone "travado" (branch
  # errada, arquivos mexidos), o membro fica sabendo que existe versão nova.
  local fetch_err
  fetch_err="$(git -C "$AURA_HOME" fetch --quiet origin main 2>&1)" || {
    # Sem rede/DNS = silêncio (tenta amanhã). Qualquer outra falha = aviso,
    # porque é um clone que NUNCA vai se atualizar sozinho até alguém agir.
    if printf '%s' "$fetch_err" | grep -qiE 'could not resolve|unable to access|timed out|network'; then
      return 0
    fi
    echo "[aura] Aviso: não consegui verificar atualizações (git fetch falhou)."
    echo "[aura] Peça na sessão: \"aura, resolve o update\" — o agente diagnostica e corrige."
    return 0
  }

  local behind pl
  behind="$(git -C "$AURA_HOME" rev-list --count HEAD..origin/main 2>/dev/null)" || return 0
  [ "${behind:-0}" -gt 0 ] || return 0
  pl=""; [ "$behind" -gt 1 ] && pl="s"

  local branch
  branch="$(git -C "$AURA_HOME" symbolic-ref --short -q HEAD 2>/dev/null)" || branch=""
  if [ "$branch" != "main" ]; then
    echo "[aura] Atualização disponível ($behind commit$pl novo$pl), mas seu clone está na branch '${branch:-desconhecida}' em vez de 'main'."
    echo "[aura] Peça na sessão: \"aura, resolve o update\" — o agente volta pra main com segurança."
    return 0
  fi

  # Working tree limpo? (só arquivos rastreados; untracked como workspace/ não bloqueia)
  local sujo
  sujo="$(git -C "$AURA_HOME" status --porcelain --untracked-files=no 2>/dev/null)"
  if [ -n "$sujo" ]; then
    echo "[aura] Atualização disponível ($behind commit$pl novo$pl), mas há mudanças locais em arquivos do framework:"
    printf '%s\n' "$sujo" | head -3 | sed 's/^/[aura]   /'
    echo "[aura] Peça na sessão: \"aura, resolve o update\" — o agente guarda ou descarta com você e atualiza."
    return 0
  fi

  if git -C "$AURA_HOME" merge --ff-only origin/main >/dev/null 2>&1; then
    echo "[aura] Aura atualizada ($behind commit$pl novo$pl)"
  else
    # Divergiu do origin (commits locais ou histórico reescrito) — nunca forçar.
    echo "[aura] Aviso: seu clone divergiu do origin/main — update automático pausado."
    echo "[aura] Peça na sessão: \"aura, resolve o update\" — re-sincroniza sem perder o workspace/."
  fi
}

run_hook() {
  # Guard roda TODA sessão (idempotente e barato)
  install_pre_commit_guard "$AURA_HOME"

  # Alias + auto-update: 1x por dia por clone
  [ -f "$FLAG_DAILY" ] && return 0

  setup_alias
  auto_update

  # Marca que já rodou hoje — não roda de novo até o próximo dia
  touch "$FLAG_DAILY" 2>/dev/null || true
}

# ============================================================================
# Execução — com flock quando disponível (Linux/WSL); fallback direto (macOS)
# ============================================================================

if command -v flock >/dev/null 2>&1; then
  (
    flock -w 2 200 2>/dev/null || exit 0
    run_hook
  ) 200>"$LOCK" || true
else
  run_hook
fi
