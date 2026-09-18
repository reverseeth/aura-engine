# Ad Strategy · Referência: SALVAR, o conteúdo do relatório e a atualização do manifest

> O diretório, os doze itens do `ad-strategy.md`, o dual output pelo `render_report.py` e a atualização do manifest pelo script com os campos gravados (inclusive `10_campaign_name`, `10_campaign_id`, `10_ad_set_ids` e `pgs_enabled`). Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/ad-strategy/` antes de salvar.

`workspace/[produto]/ad-strategy/ad-strategy.md` (no `report_language`) contendo:
1. Estrutura de teste completa: 1 campanha com CBO → N ad sets (1 por conceito) → 3 criativos + 2 primary texts + 2 headlines cada (ETAPA 3.3)
2. A conta de capacidade explicada com os números REAIS deste produto (ETAPA 3.1): target CPA, budget diário, `max_assets`, `max_adsets`, quantos conceitos entraram, quantos ficaram pro batch seguinte, e o `test_budget_daily` resultante. Se alguma restrição mordeu (piso de budget, teto de 5 ad sets, tamanho do batch, `margin_warning`), dizer qual e o efeito prático. Se o CPA-alvo ficou **abaixo do piso físico de CAC** (item 1b), mostrar as duas capacidades lado a lado — a do alvo e a do piso — e dizer que a correção é de AOV, na `offer-builder`
3. Método de teste POR AD SET — lido de `concepts[].testing_method` da `creative-engine` (ou o fallback da 3.2 pra batch legado, com `data_gap`) — com o resumo do batch e o que cada pack varia por dentro (ETAPA 3.2)
4. Warmup de conta (se aplicável), cadência quarta→domingo e o **checkpoint de decisão de domingo** — réguas do cânone §3, checks de precedência, Execution Problem, e a régua de ≥ 2 batches com learnings antes de qualquer kill de produto (ETAPAS 4-5)
5. Naming convention aplicada (Campaign / Ad Set / Ad)
6. UTM schema preenchido
7. Destino por ad set (mapeamento de congruência da `creative-engine` ETAPA 6, fallback = URL canônica do manifest), gaps de congruência se houver, e o eixo de página 3:2:2:2 quando o gate de US$ 2k/dia liberou (ETAPA 3.3)
8. Janela de decisão e handoff pra Skill `ad-analysis` (ETAPA 5)
9. Checklist de credibilidade da loja com os gaps encontrados (ETAPA 2)
10. Status da criação via MCP (criado em PAUSED / fallback manual) + IDs retornados + criações registradas no `ad-log.md`
11. Proteções configuradas: daily maximum por ad set + as duas automações obrigatórias, com o status de cada uma (ETAPA 6)
12. Checklist de erros a evitar (ETAPA 7)

**Dual output (rule 6b):** escreva o `.md` e gere o `ad-strategy/ad-strategy.html` companion (mesmo diretório) com `python3 tools/render_report.py workspace/[produto]/ad-strategy/ad-strategy.md` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`). O `.md` é fonte pra AI; o `.html` é visualização humana e nunca é escrito à mão.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete ad-strategy` marca a skill em `skills_completed` (e valida o `ad-strategy/dados.json` contra `.claude/templates/schemas/ad-strategy.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:
- Adicionar `ad-strategy` em `skills_completed`
- Registrar `strategy_id`, `creative_batch_ref`, `test_budget_daily`, `target_cpa`, `breakeven_cpa`
- **Gravar `10_campaign_name`** com o nome da campanha gerado (naming convention). A Skill `ad-analysis` lê via `read_manifest("10_campaign_name")` pra cruzar com dados do Meta.
- Se criou via MCP, gravar `10_campaign_id` e **`10_ad_set_ids`** (lista — um ID por conceito; a Skill `ad-analysis` puxa insights por ID, mais robusto que por nome). Gravar também `10_ad_set_id` com o ID do PRIMEIRO ad set, só por compatibilidade com as receitas que ainda esperam o campo único.
- Registrar `pgs_enabled: false` (fixo — Automated Rule de performance não existe em CBO, ETAPA 6). A Skill `ad-analysis` lê esse campo antes de falar em "escala automática"; com `false`, ela não promete.
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza ABRIR-AQUI.html).
