# Ad Analysis · Referência: Obter dados (ETAPA 1)

> A cascade Meta MCP oficial → Pipeboard → manual, a receita `sync-campaign-from-meta.md`, o texto do pedido manual ao membro, o cabeçalho que declara o modo usado e como integrar benchmarks da vertical, anomalias, auction ranking, opportunity score e match quality quando o pull é oficial. Abra na ETAPA 1.

### ETAPA 1 — Obter Dados (cascade: oficial → Pipeboard → manual)

Aura tenta 3 caminhos em ordem. Cada falha cai pro próximo silenciosamente — o membro vê apenas a versão final com label indicando qual modo entregou os dados.

#### Caminho 1 — Meta MCP **oficial** (preferencial; em open beta desde 2026-04-29, rollout gradual sem GA — contas podem aparecer "disabled", e o cascade cobre exatamente isso)

1. Verificar se tools com prefixo `mcp__meta__ads_` estão na sessão (prefixo canônico do connector oficial — ver `.claude/lib/mcp-detect/README.md`):
   ```
   official_mcp_available = existe ≥ 1 tool com prefixo mcp__meta__ads_
   ```

2. Se sim, tentar listar contas:
   ```
   accounts = mcp__meta__ads_get_ad_accounts()
   ```
   - Sucesso E ad_account do membro NÃO marcado "disabled" → invocar a receita única `sync-campaign-from-meta.md` (o cascade interno dela resolve pelo caminho oficial)
   - Conta marcada "disabled" no rollout gradual da beta → logar `account_disabled_in_official_beta` em `mcp-errors.log` e cair pro Caminho 2
   - OAuth expirado → tentar uma única re-autorização inline; se membro recusa, cair pro Caminho 2

3. Pelo caminho oficial, a receita salva pull completo em `workspace/[produto]/ad-analysis/raw-pull-[timestamp].json` com `source: "meta_mcp_official"` + blocos extras (`dataset_health`, `market_context` com industry benchmarks, auction ranking, opportunity score, anomalies). **ZERO interação com o membro.** Vá pra ETAPA 2.

#### Caminho 2 — Meta MCP via Pipeboard (3rd party, fallback)

Acionado quando o Caminho 1 falha. Verificar se MCP legado `meta-ads` (binary local do Pipeboard) está disponível:

```
pipeboard_mcp_available = tools com prefixo mcp__meta-ads__ existem
```

Se sim, invocar a MESMA receita única `sync-campaign-from-meta.md`, passando `force_path: "pipeboard"` no input + `fallback_reason` preenchido conforme o motivo do Caminho 1 ter falhado (motivos canônicos: `account_disabled_in_official_beta` | `oauth_failed` | `official_unreachable` | `forced_by_member`). JSON resultado tem `source: "meta_mcp_pipeboard"` e o mesmo shape base (sem os blocos `dataset_health` e `market_context` exclusivos do oficial).

#### Caminho 3 — Manual (último recurso)

Quando ambos MCPs falham (não configurados, ambos token/OAuth expirados, ambos rate-limited):

1. Logar ambos os erros em `workspace/[produto]/ad-analysis/mcp-errors.log`
2. Pedir ao membro:

   > "MCP do Meta Ads não respondeu (motivo: oficial=[erro], pipeboard=[erro]). Cola os dados aqui — screenshot ou números. Preciso ver **por AD (criativo)**: Spend, Frequency, CPM, CPC, Cost per Purchase, ROAS, e (importante pro diagnóstico de funil) Adds to Cart e Checkouts Initiated além das Purchases. E quantos dias cada ad está rodando."

3. ESPERE a resposta. Parse manual. Marcar `source: "manual"` internamente (valor canônico — ver `.claude/lib/mcp-detect/README.md`).

#### Output final — declarar o modo usado

No final da análise, header do relatório indica qual modo foi usado:

- **Caminho 1 (oficial):** "Dados puxados via Meta MCP oficial em [timestamp]. Industry benchmarks incluídos."
- **Caminho 2 (Pipeboard):** "Dados via Pipeboard MCP em [timestamp] (oficial indisponível: [motivo])."
- **Caminho 3 (manual):** "Dados colados pelo membro em [timestamp]."

Esta é a diferença entre Skill `ad-analysis` totalmente autônoma (caminho 1 ou 2) vs sob demanda (caminho 3).

#### Quando dados oficiais existem, integrá-los na 4Pi analysis

Se `raw-pull.market_context.industry_benchmark` está presente:
- **Pi 3 CPM judgment:** comparar membro vs vertical em vez de absoluto. Ex: "membro CPM $42 vs vertical p50 $38 → 10% acima da mediana, dentro do esperado". Sem isso, CPM $42 sozinho não diz nada.
- **CPM subindo (fadiga vs sazonalidade):** se `anomalies_detected` confirma anomalia, decisão é mais confiante.
- **Auction ranking `below_avg` em quality OU engagement OU conversion** → marcador independente de problema do creative que entra no 19-Point Diagnostic.
- **Opportunity Score — usar como higiene, NUNCA como comando.** O score (0-100) mede aderência às best practices da Meta, não performance. Use os itens de checklist que ele expõe (audience overlap, sinal de conversão, variedade de criativo) como sinal secundário que "reforça vs contradiz" o 4Pi. **NUNCA aplique recomendações em lote pra "subir o score"** — em particular, IGNORE recomendação de mover o budget pros ad sets (desligar o CBO) ou de consolidar os conceitos num ad set só: o CBO no nível da campanha com **1 ad set por conceito** é decisão deliberada da Skill `ad-strategy` (ETAPA 3.3), e é exatamente ele que produz o sinal de escala que esta skill lê. Score alto = alinhamento com o playbook da Meta, não ROAS.

Se `dataset_health.match_quality_score < 6.0` (EMQ na escala 0-10 do Events Manager — gate canônico da `tracking-setup` é EMQ ≥ 6.0) → marcar warning no relatório: "Match quality abaixo do gate, CPAs podem estar inflados por undercounting de conversões". Antes esse contexto só vinha do Events Manager manualmente.

> Pra interpretar e corrigir match quality baixa: **CAPI & Pixel Data / Event Match Quality** (rode `CAPI pixel advanced matching event match quality email click ID below 5`). Diz quais parâmetros de advanced matching (email, click ID) elevam o EMQ e quando um EMQ baixo está inflando o CPA observado — não confunda CPA inflado por undercounting com criativo ruim antes de checar isso.
