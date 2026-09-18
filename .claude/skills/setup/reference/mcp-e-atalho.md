# Setup · Referência: Verificação do MCP Aura e confirmação do atalho (ETAPAs 2 e 2.5)

> O teste do MCP com query real, o diagnóstico em ordem quando falha (aprovação recusada e registro manual do servidor) e a confirmação do alias `aura` criado pelo hook de início de sessão. Abra na ETAPA 2.

### ETAPA 2 — Verificação do MCP Aura

O sistema depende do MCP `aura` pra acessar a base de conhecimento. Teste com uma query real e relevante, não "test connection". Rode:

```
search_knowledge("market sophistication stages")
```

Verifique que a resposta retorna conteúdo real (não vazio, não erro). Se funcionar, mostre ✅ "Aura conectada e respondendo." (sem inventar números — a tool não retorna contagem de conteúdo). Se não:

O acesso à base já vem registrado no próprio Aura Engine (arquivo `.mcp.json` na raiz do repo) — na primeira abertura do Claude Code nesta pasta o Claude pede aprovação do servidor `aura`. Quando o teste falha, diagnostique nesta ordem:

1. **Aprovação recusada** (causa mais comum): instrua o membro a rodar no terminal, FORA do Claude Code: `claude mcp reset-project-choices` — depois reiniciar o Claude Code (digitar `aura`), aprovar o servidor quando perguntar, e digitar 'setup' de novo.
2. **Registro manual** (se o passo 1 não resolver): registrar o servidor direto, no terminal FORA do Claude Code:

```
claude mcp add aura --transport http "https://aura-mcp-production.up.railway.app/mcp"
```

Depois reiniciar o Claude Code e digitar 'setup' novamente.

NÃO prossiga sem o MCP funcionando.

### ETAPA 2.5 — Confirmação do Atalho `aura`

O alias `aura` (`cd ~/aura-engine && claude`) é criado automaticamente pelo hook de início de sessão (`.claude/hooks/post-start.sh`) em toda sessão — membros novos e antigos recebem sem precisar refazer setup. Aqui, apenas confirme visualmente ao membro que já pode usar:

> "Atalho criado. Da próxima vez, basta abrir o Terminal e digitar: **aura**"

O hook cobre zsh, bash e fish (cada um recebe o alias no arquivo de config certo). Só oculte a mensagem acima se o shell do membro não for nenhum desses (ex: nushell) — nesse caso o hook pula silenciosamente.
