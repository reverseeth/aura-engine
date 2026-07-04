# Refero MCP Integration (opcional)

Integração com o **Refero Design MCP** (package canônico: `fidgetcoding-refero-mcp`, instalado via `npx -y fidgetcoding-refero-mcp`). Catálogo curado de ~200 design systems de sites premium (Cursor, Linear, Vercel, Notion, Stripe, etc.) com cores role-tagged, typography, spacing, do/dont rules — pronto pra alimentar os brand signals da Aura sem inventar do zero nem fazer scraping.

## Quando usar

Membro tem o Refero MCP conectado E está rodando a skill **07a-page-design ETAPA 2 (Brand Signals)**. Aura procura na biblioteca curada um estilo que case com a vibe pedida (do `profile.md` ou da descrição do membro) e usa o `designSystem` retornado pra alimentar o `frontend-design` via `design-signals.json` (heading/body font, palette role-tagged, radius, shadow, density).

**Default = não-integrado.** Aura funciona 100% sem Refero (cai pro screenshot→visão, ou `tools/design-clone/` pra hex exato, ou estilo pré-definido). Integração é puro upside.

## Como o membro conecta

Tutorial completo nos passos do `docs/aura-setup-pt.html`/`docs/aura-setup-en.html` (passo opcional na seção Aura Engine). Fluxo resumido:

**Claude Code (terminal):**
```bash
claude mcp add refero -- npx -y fidgetcoding-refero-mcp
```

Opcional pra qualidade de busca:
```bash
# Pra semantic search via embeddings (default cai pra BM25 keyword)
export OPENAI_API_KEY="sk-..."
```

> **Não configure `REFERO_MCP_VAULT_DIR` apontando pra raiz de `workspace/`** — o layout canônico (`.claude/lib/workspace-index/workspace-layout.md`) não tem `DESIGN.md` solto na raiz (múltiplos produtos sobrescreveriam o mesmo arquivo, órfão do produto e invisível pro painel). A 07a consome o `designSystem` direto da tool e grava `design-signals.json` em `workspace/<slug>/07-page/`. Se o membro usar `refero_design_md` com escrita em disco, a 07a absorve o conteúdo e o arquivo vai pra `workspace/<slug>/07-page/`.

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

Integração focada na **skill 07a-page-design ETAPA 2 (Brand Signals)**. Cascade resiliente (mesma ordem da regra 10c do CLAUDE.md):

1. **Refero MCP** (preferencial) — catálogo curado, designSystems estruturados
2. **Screenshot → visão** (fallback primário) — membro tira print full-page da loja de referência e o Claude lê a imagem com visão nativa pra extrair paleta/tipografia/vibe. Imune a Cloudflare/JS/markup bagunçado
3. **`tools/design-clone/`** (caminho 3, opcional) — extração via Playwright dos computed-styles quando o membro quer **hex exato** de um concorrente nichado fora do catálogo Refero (ex: PDPs de skincare/microneedling)
4. **Manual / 8 presets** — membro descreve a referência em texto ou escolhe um estilo pré-definido

| Skill | Tools usadas | O que melhora |
|-------|--------------|---------------|
| **07a-page-design (ETAPA 2)** | `refero_search` + `refero_get` (+ opcional `refero_design_md`) | Sinais de cor/typography/spacing vêm de curadoria humana de design systems top, não scraping bruto. Convergem todos pro mesmo `design-signals.json` que alimenta o `frontend-design`. |

**Quando NÃO usar Refero:** quando o membro passa URL de concorrente nichado fora do catálogo (Refero é generalista top-200, não tem PDPs nichadas de skincare/microneedling). Nesses casos, o fallback é screenshot→visão (caminho 2) ou design-clone pra hex exato (caminho 3).

## Detecção em runtime (padrão)

Na ETAPA 2 (Brand Signals) da 07a-page-design, Aura testa (prefixo conforme `.claude/lib/mcp-detect/README.md`):

```
refero_available = qualquer tool começando com mcp__refero__ existe

if refero_available:
    # 1. tentar match por descrição/vibe do membro
    results = mcp__refero__refero_search(query="<descrição da Brand Discovery>", limit=5)
    apresentar 2-3 candidatos ao membro pra escolher
    if membro escolhe: usar refero_get(<style>) → design-signals.json (source: "refero")
elif membro tem print da loja de referência: screenshot→visão (source: "screenshot_vision")
elif membro passou URL e quer hex exato: cair pro design-clone (source: "design_clone")
else: pedir descrição manual ou escolher pré-definido (source: "manual")
```

Aura **nunca** consulta Refero sem membro confirmar a direção. Refero é fonte de inspiração + signals técnicos, não autoridade que decide design pelo membro.

## Custos / créditos

Refero MCP **não tem créditos**. O catálogo é livre. Único custo opcional: `OPENAI_API_KEY` consome embeddings quando vibe search semântica é usada (~$0.0001 por busca, irrelevante na prática).

Sem `OPENAI_API_KEY`, busca cai pra BM25 keyword scoring (zero custo, qualidade levemente menor pra queries abstratas tipo "editorial premium").

## Falhas e fallback

Se chamada Refero falha (tool não responde, catálogo offline, query sem resultado relevante), Aura cai silenciosamente pro próximo degrau da cascade: screenshot→visão (se o membro tem print), design-clone (se quer hex exato de uma URL), ou pergunta direta. Membro vê output equivalente — só perde o ganho do catálogo curado.

## Privacidade

Refero MCP é local (npm package). Não há tokens persistidos no Aura nem no workspace. O `mcp_token` que o membro vê na URL do front-end web do Refero (`styles.refero.design`) é só pra acesso browser e **não é usado pelo MCP**.

Cache local em `~/.cache/refero-mcp/` (default) com TTL 24h.

## Refero vs frontend-design (quem faz o quê)

O design da página é **HTML-first**: nasce in-session via a skill nativa `frontend-design`, que gera a página inteira como HTML+CSS self-contained com a copy real já inserida — essa é a fonte única de verdade visual que o membro aprova antes de qualquer Liquid existir. O Claude Design (app claude.ai) **saiu do caminho crítico**.

O Refero não compete com o `frontend-design`: ele só **alimenta os signals** que o `frontend-design` aplica.

| Aspecto | Refero MCP (07a ETAPA 2) | frontend-design (07a ETAPA 3) |
|---------|--------------------------|-------------------------------|
| O que entrega | `design-signals.json` (cores role-tagged, typography, spacing, radius, shadow, density) | A página inteira como HTML+CSS (2-3 variações navegáveis), copy real aplicada |
| Quando roda | Brand Signals, antes do design | Geração do design HTML-first aprovado pelo membro |
| Papel | Fonte de inspiração + signals técnicos | Fonte única de verdade visual |

Sequência: Refero (ou screenshot→visão / design-clone) fornece os signals da vibe → `frontend-design` gera a página HTML aplicando esses signals → membro aprova → 07b-page-build compila em Liquid determinístico.

## Roadmap (não implementado, ideias futuras)

- `refero_search` pra alimentar 08 (creative-engine) — buscar landing page styles que casam com hooks específicos
- `refero_design_md` cacheado cross-product em `creative-dna/registry` pra reuso de signals entre produtos da mesma marca
- Cross-reference com TrendTrack: buscar Refero estilo similar a um concorrente trackado
