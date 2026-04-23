---
name: post-task-self-audit
description: Após completar QUALQUER skill importante ou tarefa de peso, AI DEVE rodar auto-auditoria profunda antes de declarar "pronto". Checa cross-artifact consistency, qualidade, gaps, erros de raciocínio, alinhamento com fases anteriores. Não é cosmético — é travamento mental que separa output medíocre de output rigoroso.
paths:
  - .claude/skills/
---

# Post-Task Self-Audit (MANDATORY)

Toda skill do Aura Engine E toda tarefa importante (deploy, geração de asset pro consumidor final, mudança estrutural, análise de diagnóstico) termina com uma **auto-auditoria profunda obrigatória**. Não é opcional. Não é "se sobrar tempo". É o último step de QUALQUER execução séria.

## Por que existe

Sem auto-auditoria, a AI entrega o que parece OK superficialmente e o membro descobre os buracos 3 semanas depois quando ad é reprovado, PDP tem drift de mecanismo, ou report contradiz market research. A auditoria interna de 60-90 segundos economiza dias de retrabalho.

## Quando dispara (automático)

- Ao completar qualquer skill (00-17)
- Após deploy de código ou asset em produção (Shopify push, Klaviyo flow, ad campaign)
- Após geração de artefato consumidor-final (copy, briefing, PDP, ad)
- Após análise/diagnóstico que vai informar decisão ($ em jogo)
- Após criar/modificar estrutura do framework (rules, skills, libs)
- **Sempre que a AI estiver prestes a dizer "pronto", "completo", "feito", "deployado"** — antes dessa palavra, roda o audit

NÃO dispara em:
- Respostas curtas conversacionais
- Confirmações simples ("sim, entendi")
- Tarefas exploratórias sem output salvo

## Protocolo — 6 gates obrigatórios

Antes de declarar conclusão, rodar mentalmente (ou em output visível, se skill é peso alto):

### Gate 1 — Cross-artifact consistency

Re-ler os artefatos relevantes das fases ANTERIORES e confirmar que o output atual **não contradiz, não duplica errado, não ignora**:

- Se gerou copy (Skill 05): mecanismo nomeado bate literal com `04-offer.json`? VOC phrases vêm de `02-market-research.json` (não inventadas)?
- Se gerou ad (Skill 07): awareness level alinha com `02`? Gaps explorados vêm de `03`? Promise bate com `04-offer`?
- Se rodou consistency audit (Skill 11): revisou TODOS os 9+ artefatos, não só os últimos 2?
- Se modificou framework (rule, skill, lib): checou impacto em skills downstream que referenciam?

Se detectar drift, **corrigir antes de entregar**. Não passar pra próxima tarefa com drift ativo.

### Gate 2 — Erros factuais e de raciocínio

Checar claims específicos que AI afirmou:

- Cálculos numéricos (AOV, CPA, ROAS, PSM, word count, percentuais) — conferir aritmética
- Referências a arquivos/paths — existem, estão acessíveis, nomes batem
- Referências a frameworks (Schwartz stages, Hormozi, Cialdini) — aplicação correta, não confusão
- Citações de estudos/fontes — rastreáveis, não inventadas
- Datas, timestamps, prazos — coerentes, futuros quando devem ser

Se qualquer item falha, **corrigir inline**. Claim sem lastro vira copy fraca vira ad reprovado.

### Gate 3 — Gaps e implementações faltantes

Perguntas que a AI faz a si mesma:

- "Algum output esperado ficou fora? (md, json, html, manifest update)"
- "Algum sanity check da skill ficou sem resposta?"
- "Algum campo schema ficou vazio ou com placeholder que eu deveria ter preenchido?"
- "Alguma integração downstream (skill X lê meu output) vai falhar por dado faltante?"
- "O próximo skill na cadeia vai encontrar tudo que precisa?"

Se resposta a qualquer pergunta = "sim, faltou", completar antes de entregar.

### Gate 4 — Qualidade extrema do doc

Output escrito passa em:

- Rigor de idioma (regra 0 do CLAUDE.md) — português claro, sem jargão não-explicado, sem inglês forçado
- Frases completas, lógica encadeada (não bullets genéricos vazios)
- Especificidade (Hopkins) — "47% de redução em 14 dias" > "resultados rápidos"
- Zero travessão em headlines (rule 8a) — em copy longa, ≤2
- Zero ad-flag words em consumer-facing (rule 8b)
- Logo SVG presente (rule 6b) se é dual output HTML
- Componentes do design system usados (callout, note, danger, winner, etc) quando cabível

Se falha de qualidade encontrada, reescrever. "Já tá bom" não é aceitável quando podia estar rigoroso.

### Gate 5 — Alinhamento com rules globais

Cross-check rápido contra rules que se aplicam:

- `shopify-theme-safety.md` (se mexeu em tema) — pull-before-edit, `--nodelete`, marker verification
- `pre-launch-gates.md` (se gerou consumer-final) — compliance pass, promise↔config
- `iteration-driven-refinement.md` — entreguei como draft + convite pra iteração, não como "pronto"?
- `member-stage-awareness.md` — tom/recomendação adaptou ao stage (starter/validating/scaling)?
- `emergency-escape-paths.md` (se falhou algo) — ofereci ≥2 paths adiante, não abortei?

### Gate 6 — Output da auto-auditoria

Se a skill é peso alto (launch, deploy, asset consumer-final), a auto-auditoria fica **visível** no output final como bloco:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## Self-audit — [Skill X]

Cross-artifact: ✓ mecanismo consistente com 04-offer.json, VOC rastreável a 02
Erros factuais: ✓ cálculos conferidos (AOV $127.50, CPA target $42)
Gaps: ✓ todos os 10 sanity checks da skill respondidos; manifest.json atualizado
Qualidade: ✓ zero travessão em headlines, zero ad-flag words, logo SVG presente
Rules alinhadas: ✓ iteration-driven (entregue como draft), compliance (PASS)

Issues detectados e corrigidos nesta rodada:
- [exemplo: corrigi word count de hook que estava em 58 palavras pra 42s de script — não cabia]
- [exemplo: atualizei manifest que estava sem last_batch_id]

Issues residuais que exigem atenção do membro:
- [exemplo: testimonial placeholder em 2 sections — membro precisa coletar reais]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Se a skill é peso baixo/médio, a auto-auditoria roda internamente (mental) — sem bloco visível — mas qualquer issue detectado vira correção inline.

## Regras específicas de rigor

1. **NÃO declarar "completo" sem auditoria** — mesmo em urgência. 60 segundos sempre cabem.
2. **NÃO ignorar drift pra "ganhar tempo"** — drift acumula e explode depois.
3. **NÃO encerrar com gap conhecido** — ou corrige, ou explicita como "issue residual" pro membro.
4. **NÃO repetir auditoria superficial** — se der clean em todos os gates na primeira rodada, provavelmente AI pulou etapas. Re-audit.
5. **NÃO mentir pro membro** — se o audit encontrou issue, reportar. Skip de audit = falta de rigor, não qualidade.

## Modo "deep audit" (skills peso crítico)

Em Skills 04 (offer), 05 (copy), 06c (deploy), 07 (creatives), 08 (ad-strategy), 11 (consistency-audit), a auto-auditoria é EXPANDIDA:

- Re-ler as skills anteriores da cadeia (não só artefatos JSON)
- Verificar se `04-research-foundation.json` sustenta todo claim forte
- Cruzar com `03-creative-patterns.json` (se existe) pra validar padrões de mercado
- Conferir que `pre-launch-gates` passaram sem override
- Testar mentalmente edge cases (member em stage 1 com $50/dia? ESP = "none"? Whisper ausente?)

Deep audit é ~3-5 minutos adicionais. Vale porque esses são os momentos caros pra errar.

## Anti-patterns (FORBIDDEN)

- "Completo!" sem audit
- Audit de 1 linha ("checklist OK") sem substância
- Auto-auditar com tom defensivo (encontrar razões pra não corrigir issue)
- Pular audit em "tarefa pequena" — muitas vezes "tarefa pequena" tem drift mais sutil
- Declarar audit passou quando sabia de issue residual sem flagrar pro membro
- Deixar próxima skill na cadeia herdar bug invisível
