# page-qa — QA medido, captura comparada e tokens da `page-design`

Scripts de biblioteca padrão que a skill `page-design` (ETAPAS 4 a 6) e a `page-build` (pré-flight e 6.11) chamam. O desenho completo está em `docs/designs/page-design-2.md`. Os testes ficam em `tools/tests/test_{geodiff,legal_check,tokens,qa_gate}.py`.

| Script | Interface | Saída | Quem chama |
|---|---|---|---|
| `geodiff.py` | `--ref DIR... --page DIR --map REF:BANDA:SECAO,... --out geodiff.json` | nota de 0 a 100 por seção; exit 1 se alguma ficar abaixo de 70 | `page-design`, modo referência, por seção |
| `legal_check.py` | `--ref DIR... --page page.html [--allowed-fonts ...] [--ref-brand ...] --out legal.json` | `{pass, findings[]}`: texto, asset, fonte ou marca da referência no `page.html`; exit 1 se achar algo | `page-design`, modo referência, antes do QA |
| `tokens.py` | `PAGE.html --out design-tokens.json --source ENUM [--preset-base ID] [--brand-out ...]`; `--from-dtcg`; `--diff A B`; `--diff-live COMPUTED TOKENS` | `design-tokens.json`, `brand-tokens.json` (DTCG) ou `{drift, changed[]}` no stdout | `setup` (marca), `page-design` ETAPA 6, `page-build` 6.11 |
| `qa_gate.py` | `PAGE-PLAN.json [QA-METRICS.json] [--page page.html]` | exit 0 libera, 1 bloqueia, 2 página antiga (só aviso) | pré-flight da `page-build` |

As capturas que o `geodiff.py` e o `legal_check.py` leem vêm do `tools/design-clone/downloader.py --mode bands`. O `qa-metrics.json` vem do `.claude/lib/theme-verify/verify_page.py --json-out`. `legal_allowlist.txt` lista as frases genéricas de DTC que não contam como cópia (uma por linha).

**Contrato de nomes dos tokens:** `--color-<papel>` no `:root` para os 8 papéis (`background`, `surface`, `foreground`, `primary`, `on-primary`, `accent`, `muted`, `border`), `--font-heading`, `--font-body`, `--text-*`, `--space-*`, `--radius-*` e `--shadow-*`. No `brand-tokens.json`: `color.<papel>`, `typography.heading|body.fontFamily`, com `$value`/`$type` e o `source` em `$extensions.aura.source`.
