#!/bin/bash
# Aura Engine — pre-commit guard
#
# Bloqueia commits que misturem framework (.claude/, tools/, raiz) com workspace
# (workspace/[produto]/) ou que contenham segredos. Esta é uma camada mecânica de
# proteção — mesmo se o agent ignorar a regra 11 do CLAUDE.md, o git não deixa o
# commit passar.
#
# Instalado automaticamente pelo post-start.sh em .git/hooks/pre-commit do repo.

set -u

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  exit 0  # não é um repo git — silencioso
}

# Lista staged files NUL-delimited com core.quotePath desligado.
# Motivo: com quotePath ligado (default), nomes não-ASCII saem quotados com escape
# octal ("workspace/an\303\241lise.md") — o match ^workspace/ falharia e um nome
# acentuado passaria pelo guard. NUL-delimited + quotePath=false é imune a isso.
STAGED_FILES=()
while IFS= read -r -d '' f; do
  STAGED_FILES+=("$f")
done < <(git -c core.quotePath=false diff --cached --name-only --diff-filter=ACMR -z 2>/dev/null)

[ "${#STAGED_FILES[@]}" -eq 0 ] && exit 0  # nada staged

# ============================================================================
# CHECK 1 — Workspace files
# ============================================================================
WORKSPACE_VIOLATIONS=""
for f in "${STAGED_FILES[@]}"; do
  # Permitir só workspace/.gitkeep (placeholder vazio)
  if [[ "$f" =~ ^workspace/ ]] && [ "$f" != "workspace/.gitkeep" ]; then
    WORKSPACE_VIOLATIONS+="  - $f"$'\n'
  fi
done

if [ -n "$WORKSPACE_VIOLATIONS" ]; then
  echo ""
  echo "✋  AURA ENGINE — pre-commit guard BLOQUEOU este commit"
  echo ""
  echo "Os seguintes arquivos pertencem ao seu workspace pessoal (sua marca/produto)"
  echo "e NÃO devem ir pro repositório público do framework:"
  echo ""
  echo "$WORKSPACE_VIOLATIONS"
  echo "Esses arquivos são local-only por design. O .gitignore já cobre 'workspace/*',"
  echo "então essa situação indica que algo passou pelo gitignore (ex: 'git add -f',"
  echo "edição do .gitignore, ou submódulo)."
  echo ""
  echo "Pra continuar:"
  echo "  1. Tira esses arquivos do staging: git restore --staged workspace/"
  echo "  2. Confirma com 'git status' que só os arquivos do framework ficaram"
  echo "  3. Roda 'git commit' de novo"
  echo ""
  echo "Se você TEM CERTEZA que precisa commitar mesmo assim (caso raro, ex: você"
  echo "está num fork separado da sua marca, não no aura-engine público):"
  echo "  git commit --no-verify"
  echo ""
  exit 1
fi

# ============================================================================
# CHECK 2 — Sensitive files (.env, credentials, tokens)
# ============================================================================
SECRET_VIOLATIONS=""
for f in "${STAGED_FILES[@]}"; do
  # .env.example com placeholders é OK (raiz ou aninhado)
  case "$f" in
    .env.example|*/.env.example) continue ;;
  esac
  case "$f" in
    .env|.env.*|*.env|*/.env|*/.env.*|.secrets/*|secrets/*|*/.secrets/*|*/secrets/*|*.key|*.pem|*.p12|*.pfx|credentials.json|*/credentials.json|service-account*.json|*/service-account*.json)
      SECRET_VIOLATIONS+="  - $f"$'\n'
      ;;
  esac
done

if [ -n "$SECRET_VIOLATIONS" ]; then
  echo ""
  echo "✋  AURA ENGINE — pre-commit guard BLOQUEOU este commit"
  echo ""
  echo "Os seguintes arquivos parecem conter segredos / credenciais:"
  echo ""
  echo "$SECRET_VIOLATIONS"
  echo "Esses arquivos JAMAIS devem ser commitados num repo público."
  echo ""
  echo "Pra continuar:"
  echo "  1. Tira do staging: git restore --staged <arquivo>"
  echo "  2. Confirma que está no .gitignore"
  echo "  3. Roda 'git commit' de novo"
  echo ""
  exit 1
fi

# ============================================================================
# CHECK 3 — Inline secrets (tokens reais no CONTEÚDO STAGED)
# ============================================================================
# Padrões: Facebook long-lived (EAA...), Google API (AIza/ya29), Stripe (sk_live/pk_live),
# GitHub (ghp_), Slack (xox), Shopify Admin (shpat_/shpss_/shpca_), Anthropic (sk-ant-),
# OpenAI (sk-proj-), Klaviyo private key (pk_ + hex).
# O grep roda no BLOB STAGED (git show :arquivo), não no working tree — token staged
# mas já removido do arquivo local ainda é pego.
INLINE_SECRETS=""
for f in "${STAGED_FILES[@]}"; do
  # Pular blobs vazios/ilegíveis e gigantes (binários)
  size="$(git cat-file -s ":$f" 2>/dev/null || echo 0)"
  [ "$size" -eq 0 ] && continue
  [ "$size" -gt 500000 ] && continue

  if git show ":$f" 2>/dev/null | grep -qE "EAA[A-Za-z0-9]{100,}|ya29\.[A-Za-z0-9_-]{30,}|sk_live_[A-Za-z0-9]{20,}|pk_live_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{35}|ghp_[A-Za-z0-9]{36}|xox[bp]-[A-Za-z0-9-]{20,}|shpat_[a-fA-F0-9]{32}|shpss_[a-fA-F0-9]{32}|shpca_[a-fA-F0-9]{32}|sk-ant-[A-Za-z0-9_-]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|pk_[a-f0-9]{30,}"; then
    INLINE_SECRETS+="  - $f"$'\n'
  fi
done

if [ -n "$INLINE_SECRETS" ]; then
  echo ""
  echo "✋  AURA ENGINE — pre-commit guard BLOQUEOU este commit"
  echo ""
  echo "Os seguintes arquivos contêm o que parece ser um token REAL (Facebook,"
  echo "Google, Stripe, GitHub, Slack, Shopify, Anthropic, OpenAI ou Klaviyo):"
  echo ""
  echo "$INLINE_SECRETS"
  echo "Substitui pelo placeholder (ex: YOUR_TOKEN_HERE) antes de commitar, OU"
  echo "move pro .env (que está gitignored)."
  echo ""
  exit 1
fi

# Tudo OK — commit segue
exit 0
