# Ops Engine · Referência: Output schema, o dados.json

> O schema completo do `ops-engine/dados.json` (constraint, checklist de backups, pessoa-chave, bloco legal, negócio como ativo, riscos abertos, diferença com a rodada anterior e handoff) e a lista dos campos que a skill nunca preenche por dedução. Abra ao gravar o `dados.json`.

## Output Schema — `ops-engine/ops-engine.md` + `ops-engine/dados.json`

O markdown é humano; o JSON é o registro que as rodadas futuras desta skill comparam.

```json
{
  "ops_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "stage_at_run": "starter | validating | scaling",
  "constraint_12m": {
    "type": "estoque | caixa | plataforma | pessoa_chave | outro",
    "statement": "frase declarada pelo membro",
    "why_now": "o sinal que aponta pra ela",
    "action_before": "a ação que remove, com prazo",
    "declared_at": "2026-09-01",
    "review_date": "2027-09-01"
  },
  "backups_checklist": [
    { "item": "bm_conta_reserva", "status": "ready | in_progress | missing | not_applicable | pending", "note": "" },
    { "item": "tres_admins_reais", "status": "pending", "note": "" },
    { "item": "pagina_fora_do_bm", "status": "pending", "note": "" },
    { "item": "processadora_reserva", "status": "pending", "note": "" },
    { "item": "banco_reserva", "status": "pending", "note": "" },
    { "item": "dominio_reserva", "status": "pending", "note": "" },
    { "item": "fornecedor_reserva", "status": "pending", "note": "ver sourcing/dados.json" },
    { "item": "preorder_pronto", "status": "pending", "note": "" },
    { "item": "cs_dimensionado_pico", "status": "pending", "note": "" }
  ],
  "key_man": {
    "founder_one_week_out": "degringola | segura | nao_sei",
    "single_person_dependencies": [],
    "marketing_concentration": { "top_ad_spend_share": null, "single_landing_page": null, "single_channel": null },
    "headaches_per_dollar_worst_line": null
  },
  "legal": {
    "trademark_us": "registered | filed | missing | pending",
    "trademark_eu": "pending",
    "trademark_cn": "pending",
    "brp_active": null,
    "enforcement_log": [
      { "date": "", "action": "takedown_violador | resposta_dmca_falso | dmca_contra_competidor", "target": "", "result": "" }
    ]
  },
  "business_asset": {
    "moat_test_answer": "cresce | encolhe | nao_sei",
    "moat_note": "1 frase",
    "memo_habit_active": null,
    "memos_written": [],
    "exit_ready_gaps": []
  },
  "open_risks": [
    { "risk": "", "likelihood": "baixa | media | alta", "impact": "baixo | medio | alto", "mitigation": "", "owner": "membro | aura | terceiro", "opened_at": "", "closed_at": null }
  ],
  "pending_inputs": [],
  "previous_run_diff": { "items_resolved": [], "items_new": [] },
  "handoff": { "readers": ["promo-engine", "marketplace-engine"], "note": "a `promo-engine` lê o status dos backups de conta, processadora e operação na preparação da janela promocional; a `marketplace-engine` lê o bloco legal (proteção de marca) antes de listar em marketplace; o resto é leitura das rodadas futuras desta skill e do membro" }
}
```

**Campos que a skill NUNCA preenche por dedução:** todos os `status` do checklist, `legal.*` e `key_man.founder_one_week_out`. Sem resposta do membro → `pending` + `pending_inputs[]`.
