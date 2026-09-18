# Consistency Audit · Referência: Decisão de launch e mensagem final (ETAPA 4)

> As regras de BLOCK, CAUTION e GO, inclusive o piso do input parcial, e o texto integral da mensagem final. Abra na ETAPA 4.

### ETAPA 4 — Decisão

- `issues_critical > 0` → `launch_recommendation: "BLOCK"` (mostrar ao membro como **BLOQUEAR**) → mensagem pro membro: "BLOQUEADO. [N] issues críticas. Corrige antes de lançar."
- `issues_high > 0 E critical == 0` → `CAUTION` (mostrar ao membro como **CUIDADO**) → "CUIDADO. Dá pra lançar, mas [N] issues high — fix recomendado."
- `artefacts_missing` inclui `copy-engine` E `creative-engine` (input parcial) → força no mínimo `CAUTION`, nunca `GO`, mesmo sem critical/high — não dá pra atestar coerência de copy/ad que ainda não existe.
- Tudo limpo E nenhum artefato essencial faltando → `GO` (mostrar ao membro como **PODE LANÇAR**) → "PODE LANÇAR. Auditoria passou. Próximo passo: diga **'ad strategy'** pra montar a campanha."

## Mensagem Final

"Auditoria completa. Recomendação de lançamento: [BLOQUEAR/CUIDADO/PODE LANÇAR].

- Critical: [N]
- High: [N]
- Medium: [N]

Report salvo em `workspace/[produto]/consistency-audit/consistency-audit.html`. Abre no browser pra revisar cada issue com fix sugerido.

[Se BLOQUEAR/CUIDADO:] Depois de corrigir, rode `consistency-audit` de novo pra re-validar.
[Se PODE LANÇAR:] **GO → próximo passo: diga 'ad strategy'** (Skill `ad-strategy`) pra montar a campanha de teste."
