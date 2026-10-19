# Social Engine · Referência: SALVAR, dados.json e mensagem final

> A ordem das seções do relatório, os arquivos isentos de `.html`, o schema do `dados.json`, a atualização do manifest e o texto da mensagem final. Abra ao fechar a skill.

## SALVAR (dual output, regra 6b)

`mkdir -p workspace/[produto]/social-engine/` antes de salvar. O `.html` nunca é escrito à mão: `python3 tools/render_report.py workspace/[produto]/social-engine/social-engine.md`.

Outputs em `workspace/[produto]/social-engine/`:

- **`social-engine.md`**, nesta ordem: direção do feed (as três linhas) e o board · banco de templates e fórmula do grid · o grid aprovado com as 9 legendas · publicação (o degrau, a ferramenta, a ordem, o espaçamento) · rotina (horário, teto de créditos, custo por mês) · pendências (o que falta e o que destrava). Só o resultado (`.claude/rules/report-only-results.md`).
- **`social-engine.html`**: companion.
- **`dados.json`**: schema abaixo.
- **`rotina-prompt.md`**: o texto colado na rotina. Isento de `.html` (arquivo operacional).
- **`board/`** e **`<data>/`** (um por lote, com as imagens limpas, `legendas.md` e `grid-preview.png`). Isentos de `.html`.

## dados.json

```json
{
  "resumo": {
    "feed_feel": "a sensação do feed em uma frase",
    "posts_per_day": 9,
    "publishing_path": "instagram_api | publisher | package",
    "scheduler": "schedule",
    "daily_credit_cap": 0,
    "templates_in_bank": 0
  },
  "brand_board": { "references": [], "direction": { "feel": "", "signature": [], "forbidden": [] }, "page_board_reused": false },
  "higgsfield": { "brand_id": null, "product_ids": [], "credits_per_batch": 0 },
  "templates_bank": [],
  "grid_formula": [],
  "hashtag_bank": { "high_volume": [], "niche": [], "problem_ingredient": [], "brand": [] },
  "publishing": { "path": "package", "tool": null, "hosting": "shopify_files", "spacing_minutes": 0 },
  "routine": { "scheduler": "schedule", "routine_id": null, "time_local": "07:00", "timezone": "America/New_York", "daily_credit_cap": 0, "tested_at": null },
  "posts_log": [],
  "pending_inputs": []
}
```

O `resumo` é preenchido por último e espelha os campos de origem.

## Manifest e painel

`python3 tools/manifest.py <slug> complete social-engine` e `python3 .claude/lib/workspace-index/build_index.py <slug>`.

## Mensagem final

Primeira versão é draft (rule `iteration-driven-refinement.md`):

"Instagram montado. **Direção do feed: [sensação em uma frase].** O primeiro grid de 9 está aprovado e [publicado / agendado / pronto pra postar em `social-engine/<data>/`]. A rotina roda todo dia às [hora] ([fuso]), gera 9 posts com os [N] templates do banco, escreve as legendas e publica por [ferramenta]. Custo: [X] créditos por dia, cerca de [Y] por mês, com teto diário de [Z]. [SE o degrau for o pacote: 'Pra publicação ficar 100% automática, falta conectar um publicador (Zapier, Buffer ou Metricool) ou a API do Instagram. Me diz qual você prefere e eu ligo.'] Revisa o primeiro grid comigo: a cara do feed está certa? As legendas estão no tom? Uma vez por semana eu releio o que performou e ajusto o banco."
