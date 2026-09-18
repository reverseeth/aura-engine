# Retention Engine · Referência: SALVAR, o bloco manifest.retention e as regras de rigor

> Os cinco artefatos com a distinção entre HTML de email e relatório interno, a atualização do manifest pelo script com o bloco `retention` de contrato de fase e as cinco regras de rigor. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/retention-engine/` antes de salvar.

Salvar:

1. **`workspace/[produto]/retention-engine/[fluxo]/email-N.html`** — HTML pronto de cada email do fluxo (consumidor final; responsive table-based email HTML, NÃO o design-system Aura)
2. **`workspace/[produto]/retention-engine/[fluxo]/flow-metadata.json`** — metadata de cada email (subject, preview, trigger, delay)
3. **`workspace/[produto]/retention-engine/retention-engine.md`** — relatório operacional do setup pra AI ler em skills futuras (resumo dos fluxos criados, triggers, status)
4. **`workspace/[produto]/retention-engine/retention-engine.html`** — visualização humana, gerada com `python3 tools/render_report.py workspace/[produto]/retention-engine/retention-engine.md` (nunca escrita à mão). No `.md`: uma seção `##` por fluxo, o status (DRAFT/ACTIVE) em negrito e citação `**Nota:**` pras notas de setup (convenções em `.claude/templates/aura-html-components.md`).
5. **`workspace/[produto]/retention-engine/dados.json`** — log de flows criados + timestamps + status + delivery results + `phase` (`"A" | "B"`) por flow

**Distinção importante:** os emails em si (item 1) são HTML de email marketing (table-based, inline styles pra ESP compatibility) — NÃO usam o design-system Aura, NÃO têm logo Aura e NÃO passam pelo `render_report.py`. Já os relatórios internos (itens 3-4) seguem a rule 6b do CLAUDE.md normalmente.

Atualizar o manifest pelo script `tools/manifest.py` (nunca editar o JSON à mão):
- `skills_completed` ← `python3 tools/manifest.py <slug> complete retention-engine` (na primeira fase concluída; o script não duplica, faz backup e grava `updated_at`).
- O bloco `retention` abaixo entra com `python3 tools/manifest.py <slug> set retention '<bloco em JSON>'`.
- **Bloco `retention` (contrato de fase — é o que a Skill `ad-strategy` lê no checklist de credibilidade e o que a detecção de fase desta skill usa):**

```json
"retention": {
  "phase_a_done": true,
  "phase_a_flows": ["abandoned_cart", "post_purchase"],
  "phase_b_done": false
}
```

(`phase_a_flows` inclui `"welcome_email_1"` quando o condicional se aplicou; a Fase B atualiza `phase_b_done: true` e adiciona os flows dela.)

- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html), onde `<slug>` é o `product_slug`.

## Regras de rigor

1. **NUNCA ativar flow sem revisão humana** — risco de spam em escala
2. **Dois idiomas, dois papéis.** A copy dos emails (subject, preview, body, CTA) é consumidor-final do mercado US e fica SEMPRE em **inglês**, independente do `report_language`. Já o relatório interno (`retention-engine/retention-engine.md`/`.html`), o setup-guide e a conversa com o membro seguem o `report_language` do `profile.md` (default `pt-BR`). Nunca misturar: nunca email em português, nunca relatório interno forçado em inglês quando o membro escolheu pt-BR.
3. **Replenishment requer a janela de reorder definida** — perguntar ao membro em quantos dias o produto acaba (ver Fluxo 5). Se o produto é one-time (não consumível), pular Fluxo 5.
4. **Welcome offer code precisa existir no Shopify antes de enviar** — se ainda não existe, crie em Discounts (ou peça ao membro) com a mesma expiração que o email anuncia
5. **Rate limit**: ao criar flows via Klaviyo MCP oficial, respeitar o rate limit da API pública (spacing entre chamadas; ao receber 429, backoff conforme ES6). No fallback (assets + guide) não há chamada de API, então não se aplica.
