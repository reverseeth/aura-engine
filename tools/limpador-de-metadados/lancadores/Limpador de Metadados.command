#!/bin/bash
# Aura Engine — Limpador de Metadados (Mac). Dê 2 cliques pra abrir.
# Funciona na raiz da Aura (onde o hook de início de sessão deixa uma cópia)
# e na pasta original, tools/limpador-de-metadados/lancadores/.
DIR="$(cd "$(dirname "$0")" && pwd)"
APP="$DIR/tools/limpador-de-metadados/app.js"
[ -f "$APP" ] || APP="$DIR/../app.js"
if ! command -v node >/dev/null 2>&1; then
  # caminhos comuns quando o Terminal abre sem o PATH do shell de login
  for p in /opt/homebrew/bin /usr/local/bin "$HOME/.nvm/versions/node"/*/bin; do
    [ -x "$p/node" ] && export PATH="$p:$PATH" && break
  done
fi
if ! command -v node >/dev/null 2>&1; then
  echo "Node.js não encontrado. Instale com: brew install node"
  echo "(aperte qualquer tecla pra fechar)"; read -n 1 -s; exit 1
fi
node "$APP"
