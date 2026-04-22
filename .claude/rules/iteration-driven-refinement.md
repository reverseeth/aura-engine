---
name: iteration-driven-refinement
description: Princípio operacional pra toda skill — preferir iteração rápida com feedback do membro sobre geração "perfeita na primeira rodada". Membro não consegue articular todo requisito de antemão; iteração revela o que faltava.
paths:
  - .claude/skills/
---

# Iteration-Driven Refinement

## Princípio

O membro do Aura Engine não é copywriter, não é designer, não é dev Shopify. Ele não consegue escrever brief perfeito antes de ver output — ele reage ao output e refina. Skills precisam ser otimizadas pra esse loop, não pra "gerar perfeito na primeira rodada".

## Regras operacionais

### 1. Primeira versão é draft, não final

Toda skill que gera asset (copy, briefing, página, fluxo) deve apresentar primeira versão **explicitamente como draft**:

> "Primeira versão pronta. Revisa e me diz o que ajustar — tom, estrutura, ênfase. Itero até você dizer 'tá bom'."

NÃO dizer "pronto!" ou "pode lançar" — esse framing bloqueia feedback honesto.

### 2. Checkpoint mid-run quando skill é longa

Skills que rodam > 5 minutos (ex: 06-page-engine, 07-creative-engine com 8+ conceitos) têm checkpoints:

- Antes de gerar Liquid, mostrar blueprint: "Aprova a direção ou ajusto?"
- Depois de 2-3 conceitos de ad, mostrar um: "Tom e ângulo tão OK ou roda diferente?"

Checkpoint evita 20min de geração que o membro descarta inteira.

### 3. Feedback granular

Skill NUNCA pergunta "tá bom?" genericamente. Pergunta por dimensão:

- "Tom tá certo? Mais direto ou mais editorial?"
- "Headline puxa atenção ou tá morna?"
- "A seção de proof tá convincente ou precisa de mais camada?"

Feedback binário ("sim/não") não melhora a próxima rodada.

### 4. Estado preservado entre iterações

Toda iteração salva versão nova com suffix `-v2`, `-v3`, não sobrescreve. Membro pode voltar pra versão anterior se mudar de ideia. Skill mantém log em `/workspace/[produto]/iterations-log.json`.

### 5. Max 3 iterações antes de escalate

Se depois de 3 rodadas o membro ainda não tá satisfeito, escalate:

> "Já iteramos 3x e ainda tá desalinhado. Vamos fazer ao contrário — me descreve o que você QUER ver (tom, exemplos de outras marcas, referência visual), ao invés de eu gerar e você reagir."

Reset pra prompt descritivo-primeiro, porque draft-reactivo não tá funcionando.

### 6. "Saving" é milestone, não ação silenciosa

Toda gravação de arquivo final exibe ao membro:

> "Salvando v3 como versão final. Se quiser iterar depois, roda a skill de novo — ela vai ler v3 como baseline."

Membro sabe quando algo foi "commitado" vs draft.

## Anti-patterns (FORBIDDEN)

- Gerar output e dizer "pronto, pode usar" sem convite pra iteração
- Pedir feedback genérico tipo "tá bom?" (sempre granular)
- Sobrescrever versão anterior sem versionamento
- Continuar iterando sem escalate depois de 3 rodadas sem progresso
- Assumir que silence do membro = aprovação
