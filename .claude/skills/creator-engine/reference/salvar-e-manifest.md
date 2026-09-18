# Creator Engine · Referência: SALVAR e atualização do manifest

> Os outputs na ordem (relatório, html, dados.json, briefs, mensagens, contratos, roster.csv), a distinção do material operacional em inglês e a atualização do manifest pelo script com o bloco `creator`. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/creator-engine/` antes de salvar.

Outputs em `workspace/[produto]/creator-engine/`:

- **`creator-engine.md`** contendo, nesta ordem: objetivo da fase e rota escolhida; a matriz sub-avatar × creator com as lacunas; o estado do funil de seeding (campanhas, aplicações, shortlist); os briefs enviados e o inventário de conteúdo com marcação de corte; a expectativa de acerto com os números de referência; **[Fase B]** winning creators identificados, contratos e escada, estado de whitelisting/partnership por creator, e o plano de recrutamento contínuo; pendências (o que falta e o que destrava, sem narrar tentativas).
- **`creator-engine.html`** — visualização humana, gerada com `python3 tools/render_report.py workspace/[produto]/creator-engine/creator-engine.md` (nunca escrita à mão). No `.md`: tabela `KPI | Valor` pros números do funil, tabelas normais pra matriz e roster, citação `**Atenção:**` pras regras de whitelisting e `**Risco:**` pro risco de over-leverage (convenções em `.claude/templates/aura-html-components.md`).
- **`dados.json`** — schema acima.
- **`briefs/framework-[creator-slug].md`** — o framework curado de cada creator (inglês US).
- **`outreach/messages.md`** — templates das mensagens (shortlist, hire, envio, oferta de retainer, oferta de ambassador, kickoff), em inglês US.
- **`contracts/ambassador-agreement-[variant].md`** — drafts das 3 variantes com o aviso jurídico (inglês US).
- **`roster.csv`** — a planilha de gestão (colunas: creator, handle, status, tier, rate, vídeos/semana, whitelisting, contrato, payout 1/15, e-mail).

**Distinção importante (mesma da `retention-engine`):** briefs, mensagens, contratos e `roster.csv` são material operacional voltado ao creator — **não geram `.html`**, não usam o design-system Aura e ficam em inglês. Só o relatório interno (`creator-engine.md`/`.html`) segue a rule 6b e o `report_language`.

### Atualizar manifest

Após salvar, atualize o manifest pelo script `tools/manifest.py` (nunca editando o JSON à mão; ele faz backup, valida contra o `manifest-schema.json` e grava `updated_at`): `python3 tools/manifest.py <slug> complete creator-engine` marca a skill em `skills_completed` (e valida o `creator-engine/dados.json` contra `.claude/templates/schemas/creator-engine.dados.schema.json` antes de marcar), e `python3 tools/manifest.py <slug> set <chave> <valor-json> [<chave> <valor-json> ...]` grava os campos abaixo:

- Adicionar `creator-engine` em `skills_completed` (na primeira fase concluída; sem duplicar)
- **Bloco `creator` (contrato de fase — espelha o padrão do bloco `retention` da `retention-engine`):**

```json
{
  "creator": {
    "phase_a_done": true,
    "phase_b_done": false,
    "roster_count": 0,
    "ambassadors_count": 0,
    "whitelisting_active": false,
    "ad_naming_pattern": "contains creator name",
    "checked_at": "2026-09-01T00:00:00Z"
  }
}
```

- **NÃO** escrever `manifest.stage` — esta skill lê o stage, nunca o altera
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `ABRIR-AQUI.html`, onde `<slug>` é o `product_slug`)
