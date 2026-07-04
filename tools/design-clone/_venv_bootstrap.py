#!/usr/bin/env python3
"""
_venv_bootstrap.py — re-exec no python do venv do framework quando as deps de
terceiros (playwright/bs4/chardet) faltam no interpretador atual.

Mesmo padrão do `.claude/lib/web-fetch/fetch.py` (bootstrap re-exec): o membro
pode invocar qualquer entry-point do design-clone com o `python3` do sistema
que o script se re-executa sozinho no venv certo (`tools/design-clone/.venv`,
criado pela skill 00-setup; fallback `.claude/lib/web-fetch/.venv`). O python
do venv costuma ser SYMLINK pro python base (resolvem igual), então NÃO
comparamos resolve(): a env var guarda a lista de venvs JÁ TENTADOS (evita
loop e ainda tenta o próximo venv se o primeiro estiver quebrado).

Diferença pro fetch.py: aqui o bootstrap NÃO aborta quando nenhum venv serve —
apenas retorna, e o guard de import de cada script decide (mensagem de setup,
ou degradação graciosa: downloader/aura_clone precisam continuar importáveis
sem Playwright pra ingestão --from-file, e o pattern-extractor funciona sem
chardet com fallback latin-1).
"""
import importlib.util
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_ENV_VAR = "AURA_CLONE_BOOTSTRAPPED"


def bootstrap(*modules: str) -> None:
    """Se algum módulo de `modules` faltar, re-exec no python de um venv do framework."""
    if all(importlib.util.find_spec(m) is not None for m in modules):
        return
    tried = set(filter(None, os.environ.get(_ENV_VAR, "").split(":")))
    for cand in [REPO / "tools/design-clone/.venv/bin/python",
                 REPO / ".claude/lib/web-fetch/.venv/bin/python"]:
        if str(cand) in tried or not cand.exists():
            continue
        env = {**os.environ, _ENV_VAR: ":".join(sorted(tried | {str(cand)}))}
        os.execve(str(cand), [str(cand), *sys.argv], env)
    # Nenhum venv disponível/resolveu: segue no python atual — o guard de
    # import do script chamador mostra o setup ou degrada graciosamente.
