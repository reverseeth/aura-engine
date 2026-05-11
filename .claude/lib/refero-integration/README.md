# Refero MCP Integration (opcional)

Integração com o **Refero Design MCP** (`lorecraft-io/refero-design-mcp`). Catálogo curado de ~200 design systems de sites premium (Cursor, Linear, Vercel, Notion, Stripe, etc.) com cores role-tagged, typography, spacing, do/dont rules — pronto pra alimentar o design system da Aura sem inventar do zero nem fazer scraping.

## Quando usar

Membro tem o Refero MCP conectado E está rodando skill **07a (page planning)** ETAPA 2.1 Brand Discovery. Aura procura na biblioteca curada um estilo que case com a vibe pedida (do `profile.md` ou da descrição do membro) e usa o `designSystem` retornado pra alimentar os specialists `designer-color-system` + `designer-typography-scale` na ETAPA 3.

**Default = não-integrado.** Aura funciona 100% sem Refero (continua usando `tools/design-clone/` pra extração ad-hoc de URL de referência ou pedindo estilo pré-definido ao membro). Integração é puro upside.

## Como o membro conecta

Tutorial completo nos passos do `Aura.html`/`Aura-en.html` (passo opcional na seção Aura Engine). Fluxo resumido:

**Claude Code (terminal):**
```bash
claude mcp add refero -- npx -y fidgetcoding-refero-mcp
```

Opcional pra qualidade de busca:
```bash
# Pra semantic search via embeddings (default cai pra BM25 keyword)
export OPENAI_API_KEY="sk-..."

# Pra Refero escrever DESIGN.md direto no workspace
export REFERO_MCP_VAULT_DIR="$HOME/aura-engine/workspace"
```

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

## Mapping skill → tool

Integração focada na **skill 07a ETAPA 2.1 Brand Discovery**. Cascade resiliente:

1. **Refero MCP** (preferencial) — catálogo curado, designSystems estruturados
2. **`tools/design-clone/`** (fallback ad-hoc) — extração via Playwright quando o membro passa URL **fora** do catálogo Refero (ex: concorrente nichado como Qure, Seranova)
3. **Manual** — membro descreve a referência em texto ou escolhe um estilo pré-definido

| Skill | Tools usadas | O que melhora |
|-------|--------------|---------------|
| **07a page planning (ETAPA 2.1)** | `refero_search` + `refero_get` (+ opcional `refero_design_md`) | Sinais de cor/typography/spacing vêm de curadoria humana de design systems top, não scraping bruto. Eliminamos dependência forte de Playwright pra casos onde Refero cobre. |

**Quando NÃO usar Refero:** quando o membro passa URL de concorrente nichado fora do catálogo (Refero é generalista top-200, não tem PDPs nichadas de skincare/microneedling). Nesses casos, design-clone continua sendo a ferramenta certa.

## Detecção em runtime (padrão)

Na ETAPA 2.1 da skill 07a, antes de chamar design-clone, Aura testa:

```
refero_available = qualquer tool começando com mcp__refero__refero_search existe

if refero_available:
    # 1. tentar match por descrição/vibe do membro
    results = mcp__refero__refero_search(query="<descrição da Brand Discovery>", limit=5)
    apresentar 2-3 candidatos ao membro pra escolher
    if membro escolhe: usar refero_get(<style>) → alimentar specialists
elif membro passou URL: cair pro design-clone tradicional
else: pedir descrição manual ou escolher pré-definido
```

Aura **nunca** consulta Refero sem membro confirmar a direção. Refero é fonte de inspiração + signals técnicos, não autoridade que decide design pelo membro.

## Custos / créditos

Refero MCP **não tem créditos**. O catálogo é livre. Único custo opcional: `OPENAI_API_KEY` consome embeddings quando vibe search semântica é usada (~$0.0001 por busca, irrelevante na prática).

Sem `OPENAI_API_KEY`, busca cai pra BM25 keyword scoring (zero custo, qualidade levemente menor pra queries abstratas tipo "editorial premium").

## Falhas e fallback

Se chamada Refero falha (tool não responde, catálogo offline, query sem resultado relevante), Aura cai silenciosamente pro design-clone (se membro passou URL) ou pergunta direta ao membro. Membro vê output equivalente — só perde o ganho do catálogo curado.

## Privacidade

Refero MCP é local (npm package). Não há tokens persistidos no Aura nem no workspace. O `mcp_token` que o membro vê na URL do front-end web do Refero (`styles.refero.design`) é só pra acesso browser e **não é usado pelo MCP**.

Cache local em `~/.cache/refero-mcp/` (default) com TTL 24h.

## Diferença vs Claude Design (skill 07a ETAPA 0.5)

São coisas complementares, não concorrentes:

| Aspecto | Refero MCP (ETAPA 2.1) | Claude Design (ETAPA 0.5) |
|---------|------------------------|----------------------------|
| O que entrega | designSystem estruturado (cores, typography, spacing tokens) | 4 variações visuais (A/B/C/D) renderizadas como artifact |
| Quando roda | Brand Discovery, antes de gerar Liquid | Antes do membro escolher a direção visual, em formato comparável |
| Output | DESIGN.md / tokens → alimenta specialists | HTML artifact com 4 takes side-by-side pra decisão visual |
| Curadoria | Top ~200 sites premium | Geração do zero baseada em copy + brand snapshot |

Aura usa **os dois em sequência**: Refero fornece signals técnicos da vibe escolhida → Claude Design gera 4 takes visuais aplicando esses signals → membro escolhe → 07b implementa em Liquid.

## Roadmap (não implementado, ideias futuras)

- `refero_search` pra alimentar 08 (creative-engine) — buscar landing page styles que casam com hooks específicos
- `refero_design_md` integration na ETAPA 3 do 07a (Design System Orchestration) pra gerar DESIGN.md cross-product e cachear em `creative-dna/registry`
- Cross-reference com TrendTrack: buscar Refero estilo similar a um concorrente trackado
