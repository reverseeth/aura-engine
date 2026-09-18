---
name: troubleshooting-patterns
description: Diagnóstico estruturado quando skill falha ou output está quebrado. Antes de assumir "isso é limitação da AI", aplicar checklist pra identificar causa real.
paths:
  - .claude/skills/**/SKILL.md
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
| VOC insufficient (< 15 phrases) | `market-research/dados.json.voc_count` | Re-rodar Skill `market-research` com mais fontes |
| Brand snapshot ausente | `workspace/[produto]/brand.md` | Rodar Skill `setup` setup + preencher |

### 2. Output drift (diferente entre rodadas)

**Sintomas**: mesma skill com mesmo input gera output significativamente diferente a cada run

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Inputs lidos em ordem/subconjunto diferente entre runs | A skill leu os MESMOS arquivos nas duas rodadas? (comparar lista de leituras) | Fixar na skill a lista explícita de arquivos que ela lê, na ordem |
| Context window pressão | Skill carregou >200k tokens? | Reduzir inputs lidos (só essencial) |
| Prompt vago com muitas interpretações | Instruções ambíguas ("bom copy", "atrativo") | Reescrever skill com exemplos concretos |
| Conflito entre rules | Rules contradizem CLAUDE.md? | Conferir hierarquia, corrigir |

### 3. Shopify push silenciosamente rejeitado

**Sintomas**: `shopify theme push` retorna exit 0 mas mudanças não aparecem

**Fix**: aplicar protocolo da `shopify-theme-safety.md` Regra 5 (silent push rejection diagnosis)

### 4. Skill `creative-engine` gerou conceitos muito similares

**Sintomas**: N conceitos do batch parecem variações do mesmo conceito

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Market research raso (poucos gaps) | `market-research/dados.json` tem < 5 gaps? | Re-rodar Skill `market-research` profundo |
| Competitor analysis incompleto | `competitor-analysis/creative-patterns.json` ausente | Rodar Skill `competitor-analysis` Etapa 3C com criativos |
| Prompt de ideação sem diversity constraint | Skill `creative-engine` Etapa 3 — geração das 3 verticais | Forçar ≥ 2 emotions + ≥ 3 archetypes |
| Banco de provas com 1 número só | `offer-builder/research-foundation.json.best_numbers[]` tem 1 item | Ampliar o banco de provas na `offer-builder` (ETAPA 2.5) |

### 5. Ad rodou 3 dias sem gastar

**Sintomas**: ad com spend perto de zero após 72h (bem abaixo da régua mínima de leitura do cânone `.claude/lib/ad-taxonomy/README.md` §1 — criativo abaixo de ~1× target CPA/dia não acumula dado suficiente pra ser lido), OU a campanha inteira sem entregar

> **Antes de diagnosticar:** sob CBO (budget na campanha), **ad set sem gasto não é necessariamente erro** — pode ser o algoritmo concentrando no conceito que ele julga melhor, e isso já é informação (Skill `ad-strategy` ETAPA 5). O que exige investigação é a CAMPANHA inteira sem gasto em 24-48h, ou um ad set travado com os ads ainda "In review".

**Causas prováveis:**

| Causa | Check | Fix |
|-------|-------|-----|
| Audience muito pequena | Advantage+ mas audience bloqueada? | Check warnings em Ads Manager |
| Creative rejected pelo Meta | Ad status "In review" há > 24h? | Appeal via "Request Review" |
| Pixel/CAPI degradou | EMQ caiu (< 6.0/10 no Events Manager)? | Re-verificar CAPI no Events Manager |
| Capacidade de teste estourada (mais criativo no ar do que o budget consegue ler) | Régua do cânone `.claude/lib/ad-taxonomy/README.md` §1: `max_assets = budget diário ÷ target CPA` e `max_adsets = budget diário ÷ (3 × target CPA)`. Nº de ads no ar > `max_assets`? Confrontar com `test_capacity` do `ad-strategy/dados.json` | Reduzir pra capacidade real — menos conceitos no ar, o resto na fila do próximo batch (Skill `ad-strategy` ETAPA 3.1) |
| Budget abaixo do piso operacional | Budget diário < US$ 100-150/dia (piso do cânone §1)? | Subir até o piso, OU rodar 1 conceito por vez sabendo que o resultado é direcional e não autoriza kill nem escala |
| Teto por ad set estourado ("inflei o budget pra acelerar") | Ad set recebendo muito acima de ~3× target CPA/dia (teto do cânone §1)? | Dinheiro acima do teto não compra leitura: usar o excedente pra rodar MAIS conceitos (mais ad sets, respeitando `max_adsets` e o teto de 5 abaixo de US$ 1k/dia), nunca pra empurrar os mesmos |

## Protocolo geral

1. **NUNCA diga "isso é limitação da AI/do sistema" como primeira resposta** — sempre rodar árvore de diagnóstico primeiro
2. **Log em `workspace/[produto]/troubleshooting-log.md`** cada issue encontrada + fix aplicado (pattern-matching futuro)
3. **Se nada da árvore resolve**, escalate pro membro com info concreta: "Diagnóstico rodado, X/Y/Z checados, tudo OK. Pode ser [hipótese restante]. Investigação manual necessária."
4. **NUNCA sugerir fix destrutivo** (rm -rf, git reset --hard, drop workspace) sem confirmação explícita do membro

## Princípio de exaustão

Antes de dizer "não dá" pra qualquer problema, esgote as alternativas: esta árvore cobre os problemas CONHECIDOS e recorrentes do Aura Engine; pra barreiras novas (tool inédita falhando, serviço externo bloqueando de um jeito não mapeado), pesquise workarounds e tente ≥ 3 abordagens diferentes antes de escalar pro membro.
