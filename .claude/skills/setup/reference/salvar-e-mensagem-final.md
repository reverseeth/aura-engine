# Setup · Referência: SALVAR e mensagem final

> Os quatro arquivos a salvar, a geração do `profile.html` pelo `render_report.py`, os backups de profile e manifest ao refazer o setup, a geração do painel pelo `build_index.py` e a nota final sobre o manifest como fonte única. Abra ao fechar a skill.

## SALVAR (dual output — rule 6b do CLAUDE.md)

Garanta `mkdir -p workspace/` e `mkdir -p workspace/[produto]/` antes de qualquer write.

Salve os quatro arquivos abaixo e, no passo 5, gere o painel:
1. **`workspace/profile.md`** (formato da Etapa 5 — a AI lê nas fases seguintes)
2. **`workspace/profile.html`** (visualização humana, gerada com `python3 tools/render_report.py workspace/profile.md`)
3. **`workspace/[produto]/manifest.json`** (Etapa 5B — fonte única de verdade para todas as próximas skills)
4. **`workspace/[produto]/brand.md`** (Etapa 5A — apenas se SITUACAO ≠ A; copiado de `.claude/templates/brand.md.template` com fields auto-extraídos preenchidos)

**Geração do `profile.html`**: depois de gravar o `profile.md`, rode `python3 tools/render_report.py workspace/profile.md`. Se o script falhar (clone incompleto, sem o script ou sem o template), avise o membro em 1 linha, siga só com o `.md` e peça um `git pull` no fim; nunca escreva o HTML à mão (regra 6b do CLAUDE.md) e nunca aborte o setup por isso.

Se o membro já tinha um profile anterior e está refazendo, faça backup em `workspace/.profile-backup-[YYYYMMDD-HHMMSS].md` e do manifest em `workspace/[produto]/.manifest-backup-[YYYYMMDD-HHMMSS].json` antes de sobrescrever.

**5. Gerar o painel do produto.** Depois de salvar o manifest, rode via Bash pra criar a porta de entrada do membro:

```bash
python3 .claude/lib/workspace-index/build_index.py [product_slug]
```

Isso gera `workspace/[produto]/ABRIR-AQUI.html` — o painel que lista cada fase, o que já foi feito e o próximo passo. Toda skill seguinte regenera esse painel ao terminar, então ele está sempre atualizado. Estrutura canônica das pastas do produto em `.claude/lib/workspace-index/workspace-layout.md`.

## Mensagem Final

Já coberta na Etapa 6 — roteamento específico pela situação (A/B/C/D).

Adicione ao final da confirmação:

> O `manifest.json` em `workspace/[produto]/manifest.json` é a **fonte única de verdade**. Todas as próximas skills leem e atualizam este arquivo automaticamente. **NUNCA edite manualmente** — isso corrompe a coordenação entre skills. Daqui em diante toda alteração passa por `python3 tools/manifest.py <slug> set|complete` (backup + validação contra o schema), e o estado verificado do produto sai de `python3 tools/aura-status.py <slug>`.
