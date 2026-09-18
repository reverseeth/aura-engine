# Agentic Readiness · Referência: robots.txt liberando os robôs de AI e o override opcional do llms.txt (ETAPAs 5 e 6)

> Os 5 user-agents que não podem estar bloqueados, o fluxo seguro de correção no tema e o conteúdo do override do llms.txt quando o membro quer controlar a descrição da marca. Abra na ETAPA 5.

### ETAPA 5 — robots.txt liberando os robôs de AI

Verificar `curl -s https://<store>/robots.txt` e confirmar que NENHUM destes user-agents está bloqueado:

`OAI-SearchBot` · `ChatGPT-User` · `PerplexityBot` · `ClaudeBot` · `Google-Extended`

O robots.txt default do Shopify não os bloqueia — o risco é customização antiga em `templates/robots.txt.liquid` (comum em temas que copiaram "bloqueie os bots de AI" de 2023). Se houver bloqueio:
1. `shopify theme pull` antes de editar (rule `shopify-theme-safety.md` — pull-before-edit, `--nodelete`).
2. Remover/ajustar só as regras que bloqueiam esses 5 agents (não mexer no resto do arquivo).
3. Push seguro + re-verificar com curl.

Status: `all_allowed` / `fixed` / `blocked_pending`.

### ETAPA 6 — llms.txt (override opcional)

O Shopify gera `/llms.txt` nativo em toda loja (desde mai/2026). Verificar com `curl -s https://<store>/llms.txt` que existe. O override via `templates/llms.txt.liquid` é **opcional** — vale quando o membro quer controlar a descrição da marca e destacar o mecanismo/claims com as palavras certas:

- Conteúdo: 1 parágrafo de marca + produto hero com mecanismo nomeado (da `offer-builder`) + links pras políticas + fatos específicos (specs, prazos, garantia). Inglês US.
- Se o membro não quiser customizar, o nativo basta — registrar `native` e seguir.
