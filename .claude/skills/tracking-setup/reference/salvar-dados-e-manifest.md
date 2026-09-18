# Tracking Setup · Referência: SALVAR, o schema do dados.json e o bloco manifest.tracking

> Os oito blocos do relatório, o dual output, o schema do `tracking-setup/dados.json`, o bloco aninhado `manifest.tracking` com as regras de `tracking_ready` e `emq_pending` e a atualização pelo script. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/tracking-setup/` antes de salvar.

`workspace/[produto]/tracking-setup/tracking-setup.md` contendo:
1. Status do pixel (Dataset ID, canal nativo, data sharing "Always on", eventos confirmados — incluindo evento customizado de lead engajado, se a loja captura lead)
2. Status do CAPI (nível de Data sharing, Advanced Matching, dedup, fonte única server-side)
3. EMQ medido (escore 0-10 do Purchase) + caminho de verificação usado (MCP oficial / Pipeboard / manual)
4. Janela de atribuição baseline (`7d-click/1d-view`), status do Click ID no Purchase, e o teste 7DC-only registrado como diagnóstico futuro da `scale-engine` (ETAPA 3B)
5. Analytics stack escolhido + razão (stage + budget) + camadas complementares (survey pós-compra / on-site) + passos de setup/confirmação
6. Contrato de leitura (ETAPA 4B): Blended ROAS como P&L, CAC ≠ CPA, ponto cego de branded search na atribuição de terceiro
7. Checklist final da ETAPA 5
8. Próximos passos (checkout/AOV → criativos)

**Dual output `.html`** companion com o mesmo nome (`tracking-setup/tracking-setup.html`): gere com `python3 tools/render_report.py workspace/[produto]/tracking-setup/tracking-setup.md` (nunca escrito à mão; cards e tabelas nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`). Emojis ✅⚠️❌ são OK em relatório interno (rule 7 exceção).

### JSON companion — `tracking-setup/dados.json`

```json
{
  "tracking_id": "uuid",
  "product_slug": "...",
  "generated_at": "ISO-8601",
  "report_language": "pt-BR",
  "pixel": {
    "dataset_id": "...",
    "channel": "shopify_native_meta",
    "data_sharing": "always_on",
    "events_confirmed": ["PageView", "ViewContent", "AddToCart", "InitiateCheckout", "Purchase"]
  },
  "capi": {
    "enabled": true,
    "advanced_matching": true,
    "dedup_event_id": true
  },
  "attribution": {
    "window_baseline": "7d_click_1d_view",
    "click_id_on_purchase": true,
    "survey_layer": "knocommerce | none",
    "onsite_layer": "hotjar | none"
  },
  "emq": {
    "score": null,
    "scale": "0-10",
    "status": "pass | warn | pending_traffic | block",
    "source": "mcp_meta_official | pipeboard | manual"
  },
  "analytics_stack": "meta_app | wetracked | triple_whale | aimerce",
  "tracking_ready": true
}
```

(`emq.score` é numérico 0-10, ou `null` quando `pending_traffic`.)

### Atualizar manifest — bloco aninhado `manifest.tracking` (contrato canônico)

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete tracking-setup` marca a skill em `skills_completed`, e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:
- Adicionar `tracking-setup` em `skills_completed`, atualizar `updated_at`
- Gravar o bloco **ANINHADO** `tracking` (nunca campos flat no top-level — o manifest-schema documenta e as skills `creative-engine`/`ad-strategy` leem `manifest.tracking.*`):

```json
"tracking": {
  "pixel_installed": true,
  "capi_active": true,
  "emq_score": 7.2,
  "emq_pending": false,
  "analytics_stack": "meta_app",
  "tracking_ready": true
}
```

- `emq_score`: 0-10 (ou `null` se `pending_traffic`). `tracking_ready`: `true` com EMQ ≥ 6.0 medido, **OU** no caminho `pending_traffic` (Pixel + CAPI instalados, 5 eventos confirmados, Purchase validado por pedido-teste) — nesse caso gravar também `emq_pending: true` (a `ad-strategy` aceita esse estado com aviso, e a `ad-analysis` re-lê o EMQ no dia 3 de tráfego). Risco aceito via escape ES1 (config errada, membro seguiu mesmo assim) continua `tracking_ready: false`. As Skills `creative-engine` e `ad-strategy` leem `manifest.tracking.tracking_ready` no pré-flight sem pedir screenshot de novo; a `ad-strategy` e a `ad-analysis` leem `manifest.tracking.analytics_stack` pra orientar leitura de dados.
- Registrar `tracking_id`
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug`; atualiza ABRIR-AQUI.html)

> Se `tracking_ready: false` foi gravado (membro escolheu prosseguir com EMQ baixo via escape ES1), a `creative-engine` e a `ad-strategy` vão herdar o aviso e devem alertar que os criativos/campanha rodam com sinal degradado.
