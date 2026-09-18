# Consistency Audit · Referência: Output, priorização por ICE, manifest e o schema do dados.json (ETAPA 3)

> Os três artefatos com as convenções do relatório, a priorização dos fixes pelo ICE, a atualização do manifest, o schema completo do `dados.json` e quem lê o arquivo. Abra na ETAPA 3.

### ETAPA 3 — Output (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/consistency-audit/` antes de salvar.

Salvar TRÊS artefatos em `workspace/[produto]/consistency-audit/`:

1. **`consistency-audit/consistency-audit.md`** — fonte legível pela AI e pelo membro
2. **`consistency-audit/consistency-audit.html`** — visualização humana, gerada com `python3 tools/render_report.py workspace/[produto]/consistency-audit/consistency-audit.md` (nunca escrita à mão). No `.md`, use as convenções de `.claude/templates/aura-html-components.md`:
   - citação `**Risco:**` pra critical issues (vira o card vermelho)
   - citação `**Atenção:**` pra high
   - citação `**Nota:**` pra medium
   - o status (BLOCK/CAUTION/GO) em negrito no título da seção do veredito
   - tabela `KPI | Valor` pros counters (critical/high/medium)
3. **`consistency-audit/dados.json`** — machine-readable schema abaixo

**Priorização dos fixes (sistema nomeado):** antes de salvar, puxe **ICE Hypothesis Prioritization** (rode `hipotese if then because ICE score impacto confianca facilidade priorizar recomendacoes`) e aplique aos findings: cada `fix_suggested` escrito como hipótese se-então-porque ("SE alinharmos o nome do mecanismo no hero, ENTÃO o message match do funil fecha, PORQUE o consumidor vê o mesmo nome do ad à página"), e a fila de correção do report ordenada por severity primeiro e score ICE (impacto × confiança × facilidade) como desempate dentro da mesma severity — o membro ataca primeiro o fix de maior impacto que custa menos. A severity continua sendo o que decide o gate (ETAPA 4); o ICE só ordena o trabalho.

Atualizar o manifest e regenerar o painel:

- `python3 tools/manifest.py <slug> complete consistency-audit` (marca a skill com backup, validação e `updated_at`; nunca editar o JSON à mão).
- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html, onde `<slug>` é o `product_slug`).

Schema do JSON:

```json
{
  "audit_id": "uuid",
  "audited_at": "ISO",
  "artefacts_loaded": ["product-research", "..."],
  "artefacts_missing": [],
  "checks_run": 18,
  "issues_critical": 2,
  "issues_high": 3,
  "issues_medium": 4,
  "launch_recommendation": "BLOCK|CAUTION|GO",
  "findings": [
    {
      "check_id": "C2",
      "severity": "high",
      "status": "fail",
      "artifact": "copy-engine/copy-engine.md hero section",
      "issue": "Claim 'visibly firmer skin in 14 days' está no hero sem nenhuma prova nas duas seções seguintes",
      "fix_suggested": "Trazer pro bloco abaixo do hero o número do banco de provas (research-foundation.json.best_numbers[0]) ou um depoimento com resultado em 14 dias — o claim fica como está",
      "auto_fixable": false
    }
  ]
}
```

> O array de problemas chama-se `findings[]` — é o nome que as leitoras abaixo leem. Cada finding tem `status` ∈ `pass|fail|skipped`; checks não-rodáveis por artefato ausente entram como `"skipped"`, nunca `"pass"`. `artefacts_missing[]` lista os inputs esperados que não existiam.

Markdown com o mesmo conteúdo em formato humano (componentes `.danger` pra critical, `.callout` pra high, `.note` pra medium).

**Quem lê este arquivo:** a skill `ad-strategy`, como gate bloqueante de launch (`BLOCK` aborta a criação da campanha); a `page-build`, como gate de deploy informativo (`BLOCK` não impede o deploy da página, que por si não gasta dinheiro, mas o membro é avisado dos itens críticos); e a `retention-engine`, na Fase A, se o arquivo já existir (`BLOCK` oferece corrigir o drift antes de gerar os flows).
