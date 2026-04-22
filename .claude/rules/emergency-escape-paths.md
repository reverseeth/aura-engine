---
name: emergency-escape-paths
description: Paths de saída de emergência quando skill falha ou estado do workspace fica corrupto. Garante que membro nunca fique "preso" sem caminho adiante.
paths:
  - .claude/skills/
---

# Emergency Escape Paths

Membro do Aura Engine não é dev. Se skill trava ou workspace fica em estado ruim, ele não sabe recuperar sozinho. Essas rotas existem pra NUNCA deixar membro sem saída.

## Situações cobertas

### ES1 — Skill travada em pré-flight

**Sintoma**: skill pede arquivo X que "deveria existir", mas arquivo sumiu/corrompeu

**Path**:
1. Skill detecta file missing/corrupted em pré-flight
2. Em vez de abortar com "rode skill Y primeiro", oferece 2 opções:
   - **(A) Re-rodar skill Y** pra regenerar arquivo
   - **(B) Proceder com default genérico** (placeholder) E MARCAR no manifest `{"skipped_preflight": ["file_X"], "risk_acknowledged": true}`
3. Membro escolhe
4. Se (B), skill segue mas output final avisa: "Gerado com defaults — recomendo rodar skill Y e re-executar esta pra ter output real"

### ES2 — Workspace corrompido (manifest quebrado)

**Sintoma**: `manifest.json` não parse, ou missing fields críticos

**Path**:
1. Skill tenta ler manifest → erro
2. Em vez de abortar, oferece:
   - **(A) Rebuild manifest** — skill inspeciona `/workspace/[produto]/` e reconstrói manifest com base nos arquivos presentes. Asks user questions pra preencher fields não-inferíveis (budget, stage, etc)
   - **(B) Restore from backup** — se `/workspace/[produto]/manifest.backup-*.json` existe, restaurar o mais recente
   - **(C) Start fresh** — reinicializar workspace (membro explicitamente confirma data loss)
3. Default = (A) se nenhum backup existe; (B) se backup < 24h

### ES3 — Compliance gate bloqueia launch crítico

**Sintoma**: membro precisa lançar HOJE mas gate retorna `critical`

**Path**:
1. Skill lista exatamente qual palavra/promessa é problema
2. Oferece:
   - **(A) Aplicar rewrite suggestion automática** (1-click)
   - **(B) Editar manualmente** — skill abre arquivo no editor com marker na linha
   - **(C) Override com risk acknowledgment** — escrever no manifest `{"compliance_override": {...}, "risk": "...", "reason": "..."}`, proceder, mas aceita risco de disapproval/ban
3. (C) requer membro digitar literalmente "EU ACEITO O RISCO" (confirmation barrier)

### ES4 — Shopify push travado (silent rejection persistente)

**Sintoma**: aplicou protocolo de `shopify-theme-safety.md` Regra 5, ainda rejeita

**Path**:
1. Skill detecta marker ausente após N tentativas (3 max)
2. Oferece:
   - **(A) Duplicar theme no admin** e pushear pro duplicado (não-live) pra validar fora do live
   - **(B) Export manual via Shopify admin** (themes > actions > download theme file) pro membro fazer diff local
   - **(C) Rollback pra backup duplicado** (criado na Regra 6)
3. Se nada funciona, escalate: "Shopify CLI tá com issue não-standard. Passos manuais no admin: [link docs]. Me avisa quando resolvido."

### ES5 — Klaviyo session cookie expirado mid-skill

**Sintoma**: Skill 12 (retention-engine) falha autenticação no meio

**Path**:
1. Salvar progresso parcial em `/workspace/[produto]/12-retention/[fluxo]/.partial-state.json`
2. Avisar: "Cookie Klaviyo expirou. Loga de novo, copia novo cookie, e me manda. Retomo de onde parei."
3. Next run, skill lê `.partial-state.json` e continua

### ES6 — API rate limit (qualquer serviço)

**Sintoma**: 429/503 consistente

**Path**:
1. Skill detecta rate limit, pausa automaticamente
2. Wait exponential backoff (30s, 60s, 120s, 300s — max 5 retries)
3. Se persiste, oferece:
   - **(A) Pausar skill** — salva progresso, retoma em 1h
   - **(B) Continuar em modo offline** — processa com dados já carregados, pula calls restantes
   - **(C) Switch pra fallback** — se o serviço tem alternativa (ex: OpenAI API ↔ local Whisper)

### ES7 — Conflito de edição em tema Shopify (outro user editou simultâneo)

**Sintoma**: `shopify theme pull` mostra mudanças remotas que AI não fez + lock error no push

**Path**:
1. Skill detecta diff inesperado no pull
2. Lista arquivos que mudaram com hash diff
3. Oferece:
   - **(A) Preservar mudanças remotas** (merge) — skill tenta 3-way merge; se conflito não-resolvível, escalate
   - **(B) Forçar override com mudanças locais** (requer confirmation "SOBRESCREVER REMOTO")
   - **(C) Pause e resolver manualmente** no theme editor + re-rodar skill depois

## Princípios gerais

1. **Never leave member stuck** — toda situação de erro oferece ≥ 2 paths adiante
2. **Default seguro** — quando membro não escolhe explicitamente, skill toma decisão mais conservadora (não-destrutiva)
3. **State preservation** — antes de qualquer operação arriscada, snapshot do estado atual em `/workspace/[produto]/.snapshots/[timestamp]/`
4. **Confirmation barrier pra destrutivo** — operações que perdem dado/tempo exigem membro digitar frase explícita
5. **Log escapes usados** — `/workspace/[produto]/escape-paths-log.json` pra pattern-matching (se certas escapes recorrem, skill tem bug a consertar)

## Anti-patterns (FORBIDDEN)

- Abortar skill sem oferecer alternativa
- Oferecer só "rerun Skill X" quando X vai ter o mesmo erro
- Operação destrutiva sem confirmation barrier
- Perder progresso parcial sem salvar snapshot
- Default agressivo (override, force) em vez de conservador
