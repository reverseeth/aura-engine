# Agentic Readiness · Referência: SALVAR, dados.json, atualização do manifest e self-audit

> Os outputs (relatório, html, dados.json com o schema completo do checklist), o bloco `agentic` do manifest com quem o lê e os cinco itens do self-audit silencioso. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/agentic-readiness/` antes de salvar.

**`agentic-readiness/agentic-readiness.md`** (humano, no `report_language`) contendo:
1. Score de AI visibility + leitura executiva
2. Tabela do checklist (item → status → o que foi feito/o que falta → quem resolve)
3. Gaps de dados estruturados com a lista exata pra iteração da `page-build`
4. Pendências que dependem do membro (registro Perplexity, Merchant Center, policies)
5. O que esperar do canal (honesto: descoberta e citação por AI search, não venda mágica no chat — canal novo sem autoridade rankeia devagar)

**`agentic-readiness/agentic-readiness.html`** — companion humano, gerado com `python3 tools/render_report.py workspace/[produto]/agentic-readiness/agentic-readiness.md` (nunca escrito à mão). No `.md`, use as convenções de `.claude/templates/aura-html-components.md`: tabela `KPI | Valor` pro score, tabela normal pro checklist, citações `**Atenção:**`/`**Risco:**` pros gaps e `**Nota:**` pras pendências. Emojis ✅⚠️❌ OK aqui (relatório interno).

**`agentic-readiness/dados.json`** (estruturado):

```json
{
  "product_slug": "<do manifest>",
  "generated_at": "ISO-8601",
  "report_language": "pt-BR",
  "page_url": "<manifest.storefront.page_url>",
  "checklist": {
    "agentic_channel": { "status": "pass|pending|blocked_pending|na", "policies_complete": true, "notes": "" },
    "storefront_mcp_endpoint": { "status": "pass|pending", "notes": "" },
    "knowledge_base_app": { "status": "pass|pending", "notes": "" },
    "structured_data": { "status": "pass|blocked_pending", "jsonld_types_live": ["Product", "Offer"], "gtin_present": false, "gaps": [] },
    "agent_facts_block": { "status": "pass|pending", "specs_covered": ["materials", "shipping", "guarantee"] },
    "robots_txt": { "status": "all_allowed|fixed|blocked_pending", "bots_checked": ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Google-Extended"] },
    "llms_txt": { "status": "native|overridden|pending" },
    "perplexity_merchant": { "status": "registered|pending" },
    "merchant_center_feed": { "status": "pass|pending|na", "title_ok": true, "description_ok": true, "images_ok": true, "gtin_in_feed": false }
  },
  "ai_visibility_score": 0,
  "pending_actions": []
}
```

### Atualizar manifest

- `python3 tools/manifest.py <slug> complete agentic-readiness` (marca a skill com backup e grava `updated_at`; nunca editar o JSON à mão)
- Bloco **`agentic`**, gravado com `python3 tools/manifest.py <slug> set agentic '<bloco em JSON>'`: `{ "ready": <score ≥ 80 e sem blocked_pending>, "channel_enabled": <bool>, "score": <0-100>, "checked_at": "ISO-8601" }` — a Skill `consistency-audit` lê como contexto informativo (não gate) e a Skill `scale-engine` lê pra tratar tráfego de referral de AI como fonte incremental de scale.
- Regenerar o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html).

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) todo status `pass` foi VERIFICADO na loja viva (curl/print), não assumido — item não verificado é `pending`, nunca `pass`; (2) nenhum dado inventado (GTIN, rating, review count — se não existe, o gap está documentado, não preenchido); (3) score bate com a aritmética do checklist (pass/aplicáveis); (4) conteúdo público gerado (specs, llms.txt, Knowledge Base) está em inglês US, sem aviso ou suavização (rule 8b) e consistente com `offer-builder`/`copy-engine`/config real; (5) `agentic-readiness.md` + `.html` (gerado pelo `render_report.py`) + `dados.json` salvos, manifest atualizado (`skills_completed`, bloco `agentic`, `updated_at`), painel regenerado. Issue dentro do escopo → fix inline. Divergência entre policy da loja e promessa da página (precisa decisão do membro) → surface curto.
