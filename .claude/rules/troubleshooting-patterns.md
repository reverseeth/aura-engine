---
name: troubleshooting-patterns
description: Diagnóstico estruturado quando skill falha ou output está quebrado. Antes de assumir "isso é limitação da AI", aplicar checklist pra identificar causa real.
paths:
  - .claude/skills/
---

# Troubleshooting Patterns

Quando uma skill do Aura Engine não entrega resultado esperado, seguir esse diagnóstico estruturado antes de "desistir" ou sugerir fix paliativo.

## Árvore de diagnóstico

### 1. Output vazio ou incompleto

**Sintomas**: skill retorna sem gerar arquivo, ou gera arquivo com seções em branco

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Pré-flight falhou silenciosamente | Ver `manifest.json.skills_completed[]` — precedente presente? | Rodar skill anterior primeiro |
| Input JSON malformado | Parse dos JSONs carregados — erro de sintaxe? | Re-gerar JSON da skill fonte |
| Rate limit de API externa | Logs mostram 429/503? | Esperar 60s, retry |
| VOC insufficient (< 15 phrases) | `02-market-research/dados.json.voc_count` | Re-rodar Skill 02 com mais fontes |
| Research foundation vazia | `04-offer-builder/research-foundation.json.evidence_items[]` empty? | Voltar Skill 04 Etapa 2.5 |
| Brand snapshot ausente | `workspace/[produto]/brand.md` | Rodar Skill 00 setup + preencher |

### 2. Output drift (diferente entre rodadas)

**Sintomas**: mesma skill com mesmo input gera output significativamente diferente a cada run

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Inputs lidos em ordem/subconjunto diferente entre runs | A skill leu os MESMOS arquivos nas duas rodadas? (comparar lista de leituras) | Fixar na skill a lista explícita de arquivos que ela lê, na ordem |
| Context window pressão | Skill carregou >200k tokens? | Reduzir inputs lidos (só essencial) |
| Prompt vago com muitas interpretações | Instruções ambíguas ("bom copy", "atrativo") | Reescrever skill com exemplos concretos |
| Conflito entre rules | Rules contradizem CLAUDE.md? | Conferir hierarquia, corrigir |

### 3. Compliance gate bloqueia launch

**Sintomas**: tudo parece OK mas `pre-launch-gates.md` recusa

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Ad-flag word injetada acidentalmente | Rodar `compliance-preflight` isoladamente | Aplicar rewrite suggestion |
| Promise↔Config mismatch | `workspace/[produto]/promise-check.json` | Ajustar copy OU ajustar config da loja |
| Research foundation insuficiente pra claim forte | Claim tem evidence rastreável? | Softpen claim ou add evidence |

### 4. Shopify push silenciosamente rejeitado

**Sintomas**: `shopify theme push` retorna exit 0 mas mudanças não aparecem

**Fix**: aplicar protocolo da `shopify-theme-safety.md` Regra 5 (silent push rejection diagnosis)

### 5. Skill 08 gerou conceitos muito similares

**Sintomas**: N conceitos do batch parecem variações do mesmo conceito

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Market research raso (poucos gaps) | `02-market-research/dados.json` tem < 5 gaps? | Re-rodar Skill 02 profundo |
| Competitor analysis incompleto | `03-competitor-analysis/creative-patterns.json` ausente | Rodar Skill 03 Etapa 3C com criativos |
| Prompt de ideação sem diversity constraint | Skill 08 Etapa 3 — geração das 3 verticais | Forçar ≥ 2 emotions + ≥ 3 archetypes |
| Research foundation com 1 claim dominante só | Só 1 mecanismo anchored | Ampliar evidence base na 04 |

### 6. Ad rodou 3 dias sem gastar

**Sintomas**: ad com spend perto de zero após 72h (bem abaixo do fair share = 1/N do budget da campanha), OU a campanha inteira sem entregar

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Audience muito pequena | Advantage+ mas audience bloqueada? | Check warnings em Ads Manager |
| Creative rejected pelo Meta | Ad status "In review" há > 24h? | Appeal via "Request Review" |
| Pixel/CAPI degradou | EMQ caiu (< 6.0/10 no Events Manager)? | Re-verificar CAPI no Events Manager |
| Daily budget muito baixo pra CPA target | Budget < 2× target CPA? | Aumentar budget OU reduzir N de ads no ad set |

## Protocolo geral

1. **NUNCA diga "isso é limitação da AI/do sistema" como primeira resposta** — sempre rodar árvore de diagnóstico primeiro
2. **Log em `workspace/[produto]/troubleshooting-log.md`** cada issue encontrada + fix aplicado (pattern-matching futuro)
3. **Se nada da árvore resolve**, escalate pro membro com info concreta: "Diagnóstico rodado, X/Y/Z checados, tudo OK. Pode ser [hipótese restante]. Investigação manual necessária."
4. **NUNCA sugerir fix destrutivo** (rm -rf, git reset --hard, drop workspace) sem confirmação explícita do membro

## Princípio de exaustão

Antes de dizer "não dá" pra qualquer problema, esgote as alternativas: esta árvore cobre os problemas CONHECIDOS e recorrentes do Aura Engine; pra barreiras novas (tool inédita falhando, serviço externo bloqueando de um jeito não mapeado), pesquise workarounds e tente ≥ 3 abordagens diferentes antes de escalar pro membro.
