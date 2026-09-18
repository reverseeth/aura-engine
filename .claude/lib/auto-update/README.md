# Auto-update do framework (protocolo do agente)

O update automático é feito pelo hook de início de sessão `.claude/hooks/post-start.sh` (função `auto_update`). Este arquivo é o protocolo completo que o agente segue quando o hook avisa que algo bloqueou o update ou quando o membro pede ("aura, resolve o update"). O `.claude/CLAUDE.md` traz só o resumo e aponta para cá.

AUTO-UPDATE DO FRAMEWORK (protegido contra perda de dados locais):

O update automático é DETERMINÍSTICO: o hook `.claude/hooks/post-start.sh` roda 1x por dia por clone e, se o repo está em `main`, com working tree limpo e atrás de `origin/main`, faz `git merge --ff-only origin/main` sozinho. Quando existe versão nova mas algo bloqueia o update, o hook AVISA com o motivo (nunca silêncio) e instrui o membro a pedir **"aura, resolve o update"**. Opt-out: arquivo `.claude/.no-auto-update` ou env `AURA_AUTO_UPDATE=0`. Você (o modelo) NÃO repete essa rotina a cada sessão — só age quando vê um aviso `[aura]` de update na sessão OU quando o membro pede ("resolve o update", "atualiza a aura", etc.). Protocolo por caso:

1. **Aviso de mudanças locais em arquivos do framework** ("há mudanças locais em arquivos do framework") → rode `git status --porcelain --untracked-files=no` e `git diff --stat`. Mostre ao membro em linguagem simples O QUE está modificado e pergunte se ele quer manter (aí você guarda com `git stash push -m "aura-local-<data>"` e reaplica depois do update, resolvendo conflito se houver) ou descartar (só com confirmação explícita: `git checkout -- <arquivos>`). Depois: `git merge --ff-only origin/main`. NUNCA descarte sem confirmação.
2. **Aviso de branch errada** ("seu clone está na branch 'X' em vez de 'main'") → `git status --porcelain` primeiro. Se limpo: `git checkout main && git merge --ff-only origin/main` (a branch antiga fica preservada, não delete). Se sujo: trate como caso 1 antes de trocar de branch.
3. **Membro pediu update manual e não há aviso** → rode `git status --porcelain` primeiro. Se houver mudança local não-commitada, trate como caso 1. Se limpo → `git fetch origin main && git merge --ff-only origin/main`. Sucesso ou "já atualizado" = responda em 1 linha ("Aura atualizada" / "já está na última versão").
4. **Aviso "git fetch falhou"** (com internet funcionando) → diagnostique: `git remote get-url origin` (URL certa? `https://github.com/reverseeth/aura-engine.git`), depois `git fetch origin main` e leia o erro real. Corrija a causa (URL errada → `git remote set-url`; problema de credencial → oriente o membro). Não invente causa: reporte o erro literal se não conseguir resolver.
5. Se o merge falhar ("Not possible to fast-forward" / "unrelated histories") → o histórico divergiu de verdade. **Um clone novo traz de volta só o que está no GitHub. Tudo que é local-only mora dentro da pasta do clone e precisa ser carregado à mão: o `workspace/` inteiro, o `docs/historico/` (documentos internos de trabalho) e os arquivos de configuração local. O caso 5 preserva tudo que é local-only, não só o workspace.** Por isso o clone antigo é renomeado, nunca apagado. Explique ao membro que precisa re-sincronizar o repo e, com a confirmação explícita dele, rode nesta ordem:

       mv ~/aura-engine ~/aura-engine-antigo
       git clone https://github.com/reverseeth/aura-engine.git ~/aura-engine
       rm -rf ~/aura-engine/workspace
       mv ~/aura-engine-antigo/workspace ~/aura-engine/workspace
       [ -d ~/aura-engine-antigo/docs/historico ] && mv ~/aura-engine-antigo/docs/historico ~/aura-engine/docs/historico

   Enquanto `~/aura-engine-antigo` existir, nada se perdeu. Confirme com `ls ~/aura-engine/workspace` que os produtos voltaram e, se a pasta existia antes, com `ls ~/aura-engine/docs/historico` que os documentos internos voltaram. Depois, de dentro de `~/aura-engine-antigo`, rode `git status --ignored --porcelain | grep '^!!'` para listar o que mais era local-only ali (configuração local, `.env`, notas internas do índice) e leve o que o membro quiser. A pasta antiga só é apagada com pedido explícito dele, depois dessa conferência. (A mesma sequência está na seção Updates do README.)

Regras invioláveis:
- NUNCA rode `git pull` sem verificar `git status` primeiro (pode perder trabalho).
- NUNCA rode `git reset --hard`, `git clean -f` ou merge não-fast-forward automaticamente.
- NUNCA apague a pasta do clone. `rm -rf ~/aura-engine` destrói o `workspace/` e o `docs/historico/`, que não existem no GitHub e não voltam por `git clone`. O caso 5 renomeia o clone antigo e restaura o que é local-only a partir dele.
- NUNCA mostre output cru de git pro membro — os casos 1, 2, 4 e 5 são conversa em linguagem simples ("tem uma versão nova da Aura; posso guardar suas mudanças locais e atualizar?"), nunca despejo de terminal.
- Membro com clone ANTIGO (de antes do auto-update existir) não tem este mecanismo: se o membro relatar que está desatualizado e o hook nunca imprime nada, o caminho é o update manual do caso 3 — uma vez atualizado, o mecanismo passa a existir pra ele.
