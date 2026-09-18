# Ad Strategy · Referência: Gates de pré-launch, bloqueantes (ETAPA 1)

> O gate de consistência lido de `consistency-audit/dados.json` (BLOCK, CAUTION, GO e o default de rodar a auditoria inline quando o arquivo não existe) e o gate de metadados limpos antes de qualquer upload. Abra na ETAPA 1.

### ETAPA 1 — Gates de Pré-Launch (BLOQUEANTES)

**Gate de consistência (Skill `consistency-audit`)** — ler `workspace/[produto]/consistency-audit/dados.json`:
- `launch_recommendation == "BLOCK"` → **ABORTAR**. Drift entre criativos/copy/oferta vira disapproval ou mismatch ad↔landing. Mostrar findings críticos e pedir `consistency audit` após corrigir. Só prossegue com pedido explícito do membro (registrar em `manifest.skipped_preflight += ["consistency-audit:BLOCK"]`).
- `CAUTION` → mostrar warnings, pedir OK explícito antes de prosseguir.
- `GO` → seguir.
- **Arquivo ausente → rodar a Skill `consistency-audit` INLINE agora, por default.** A auditoria é barata (minutos, sem custo externo) e é o gate canônico de launch — não faz sentido criar campanha sem ela. Avisar o membro ("antes de montar a campanha, vou rodar a auditoria de consistência — leva uns minutos e evita ad reprovado por drift"), rodar a `consistency-audit`, e aplicar o resultado nas regras acima. Pular a auditoria só com recusa EXPLÍCITA do membro — nesse caso marcar `manifest.skipped_preflight += ["consistency-audit"]` e avisar no output final que a campanha nasce sem o gate de consistência (drift entre oferta/copy/ads vira disapproval ou mismatch ad↔landing).

**Metadados limpos (regra 12 do CLAUDE.md)** — ANTES de subir qualquer criativo: todo arquivo que vai pro Meta tem nome `asset-xxxx.<ext>` (saiu do Limpador de Metadados). Arquivo com outro nome (`c01-1.mp4`, export do CapCut, etc.) → rode `bash tools/strip-metadata.sh <arquivo>` antes (a receita `upload-creative-to-meta.md` faz isso sozinha no step 1.5). Nunca suba o export bruto do gerador ou do editor.
