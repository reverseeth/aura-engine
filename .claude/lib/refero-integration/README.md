# Refero MCP Integration (opcional)

Integração com o **Refero Design MCP** (package canônico: `fidgetcoding-refero-mcp`, instalado via `npx -y fidgetcoding-refero-mcp`). Catálogo curado de ~200 design systems de sites premium (Cursor, Linear, Vercel, Notion, Stripe, etc.) com cores role-tagged, typography, spacing e do/dont rules.

## Quando usar

**Hoje, nenhuma skill da Aura usa o Refero.** Até 2026-10 ele era o primeiro degrau dos brand signals da `page-design`. Na page-design nova (`schema_version: 2`), por decisão do dono em 2026-10-29, ele não entra em etapa nenhuma:

- **Marca (ETAPA 2):** sai do `brand/brand-tokens.json` (dembrandt numa URL da própria marca, no setup ou na ETAPA 2), do gerador de paletas `.claude/lib/design-presets/palette_engine.py` ou do membro. O catálogo do Refero é de sites de SaaS (Cursor, Linear, Vercel), não de marcas de e-commerce.
- **Referências (ETAPA 3):** saem do Awwwards, com WebSearch de reserva.

O `source: "refero"` continua válido só na leitura de página antiga, cujo `design-signals.json` foi gravado assim. O MCP pode continuar instalado; a Aura só não o consulta.

## Como o membro conecta

Tutorial completo nos passos do `docs/aura-setup-pt.html` (passo opcional na seção Aura Engine). Fluxo resumido:

**Claude Code (terminal):**
```bash
claude mcp add refero -- npx -y fidgetcoding-refero-mcp
```

Opcional pra qualidade de busca:
```bash
# Pra semantic search via embeddings (default cai pra BM25 keyword)
export OPENAI_API_KEY="sk-..."
```

> **Não configure `REFERO_MCP_VAULT_DIR` apontando pra raiz de `workspace/`** — o layout canônico (`.claude/lib/workspace-index/workspace-layout.md`) não tem `DESIGN.md` solto na raiz (múltiplos produtos sobrescreveriam o mesmo arquivo, órfão do produto e invisível pro painel). A `page-design` consome o `designSystem` direto da tool e grava `design-signals.json` em `workspace/<slug>/page/`. Se o membro usar `refero_design_md` com escrita em disco, a `page-design` absorve o conteúdo e o arquivo vai pra `workspace/<slug>/page/`.

Reinicie o Claude Code. Tools com prefixo `mcp__refero__` aparecem.

## Tools disponíveis (6)

| Tool | Categoria | O que faz |
|------|-----------|-----------|
| `refero_search` | Discover | Vibe search natural ("editorial premium magazine 45+", "techy clean SaaS dark") retorna sites do catálogo |
| `refero_get` | Inspect | Pega designSystem completo de 1 site (por UUID, hostname tipo `cursor.com`, ou nome tipo "Cursor") |
| `refero_similar` | Inspect | Similar styles ranking nativo do Refero pra um site dado |
| `refero_list` | Browse | Catálogo com filtros opcionais (tema, tag) — útil pra exploração ampla |
| `refero_design_md` | Generate | Renderiza um style como `DESIGN.md`. Se `REFERO_MCP_VAULT_DIR` setado, escreve direto em disco |
| `refero_refresh` | Maintenance | Bypassa cache 24h e re-fetch (raramente necessário) |

## Custos / créditos

Refero MCP **não tem créditos**. O catálogo é livre. Único custo opcional: `OPENAI_API_KEY` consome embeddings quando vibe search semântica é usada (~$0.0001 por busca, irrelevante na prática).

Sem `OPENAI_API_KEY`, busca cai pra BM25 keyword scoring (zero custo, qualidade levemente menor pra queries abstratas tipo "editorial premium").

## Privacidade

Refero MCP é local (npm package). Não há tokens persistidos no Aura nem no workspace. O `mcp_token` que o membro vê na URL do front-end web do Refero (`styles.refero.design`) é só pra acesso browser e **não é usado pelo MCP**.

Cache local em `~/.cache/refero-mcp/` (default) com TTL 24h.

## Roadmap (não implementado, ideias futuras)

- `refero_search` pra alimentar 08 (creative-engine) — buscar landing page styles que casam com hooks específicos
- `refero_design_md` cacheado cross-product em `creative-dna/registry` pra reuso de signals entre produtos da mesma marca
- Cross-reference com TrendTrack: buscar Refero estilo similar a um concorrente trackado
