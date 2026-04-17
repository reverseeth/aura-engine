# Creative DNA Feature Extractor — prompt structured

Usado pela Skill 07 imediatamente após gerar um briefing completo. Extrai features em formato padronizado e salva no registry.

## Fluxo de invocação (a Skill 07 executa isso internamente)

1. Depois de completar ETAPA 5 (briefings) e ETAPA 7.5 (compliance), pra cada criativo gerado:
2. Rodar este prompt de extração abaixo
3. Parse JSON response
4. Salvar em `/workspace/[produto]/creative-dna/features-[creative-id].json`
5. Invocar `python .claude/lib/creative-dna/registry.py add [creative-id] features-[creative-id].json --product [slug]`
6. Silent — membro não vê

## PROMPT

```
Você é o Creative DNA Extractor. Leia o briefing do criativo abaixo e extraia features estruturadas respeitando EXATAMENTE o schema em feature_schema.json.

Schema: {conteúdo completo de feature_schema.json}

Briefing do criativo: {conteúdo do 07-concept-XX.md ou script}

Contexto adicional:
- Awareness level alvo (do market research): {awareness_dominant}
- Funnel position (do próprio briefing): {TOF | MOF | BOF}
- Compliance risk score (do checker.md rodado antes): {0-100}

Retorne APENAS JSON neste formato (nenhum texto antes ou depois):

{
  "creative_id": "[id do briefing]",
  "concept_id": "[parent concept]",
  "source_file": "[path do .md]",
  "produced_at": "[ISO timestamp]",

  "hook_type": "[valor do enum]",
  "hook_duration_seconds": N,
  "hook_has_specific_number": true|false,
  "pain_agitation_position": "[enum]",
  "mechanism_reveal_position": "[enum]",
  "social_proof_density": "[enum]",
  "cta_tone": "[enum]",
  "voice_profile": "[enum]",
  "voiceover_pause_avg_ms": N,
  "text_overlay_frequency": "[enum]",
  "visual_cuts_per_second": N,
  "numbers_in_copy_count": N,
  "avatar_age_depicted": N,
  "format": "[enum]",
  "duration_total_seconds": N,
  "big_idea_explicit": true|false,
  "objection_addressed_count": N,
  "guarantee_mentioned": true|false,
  "price_mentioned": true|false,
  "urgency_mechanism": "[enum]",
  "compliance_risk_score": N,

  "awareness_level_target": "[enum]",
  "funnel_position": "[enum]",
  "angle_vertical": "[enum]",
  "big_4_emotion_dominant": "[enum]"
}

Valores enum DEVEM vir do schema. Se impossível classificar, use "not_used" ou "none".
Numerics: inferir do briefing (ex: contar números específicos, calcular cuts/s).
```

## Integração na Skill 07 (patch a adicionar na ETAPA 7.5)

Após o compliance check passar, adicionar:

```
### ETAPA 7.6 — DNA Registry (silent)

Pra cada criativo gerado:
1. Ler .claude/lib/creative-dna/feature_schema.json
2. Rodar o extractor.md prompt com:
   - briefing completo
   - awareness_dominant do market research
   - compliance_risk_score do Pre-flight
3. Parse JSON response
4. Salvar features em /workspace/[produto]/creative-dna/features-[creative-id].json
5. Invocar registry.py add (init registry se primeira vez)

Silent. Sem output pro membro.
Se falhar extração, logar erro mas não bloquear a skill.
```

## Integração na Skill 09 (patch a adicionar)

Quando Skill 09 roda análise de performance:

```
### ETAPA X — DNA Update (silent)

Pra cada criativo analisado:
1. Compor performance JSON:
   {
     "cpa": X, "ctr": Y, "roas": Z, "spend": W,
     "thumbstop_3s": A, "hold_15s": B,
     "days_active": D,
     "outcome": "winner" | "loser" | "neutral"
   }
2. Classificar outcome:
   - winner: cpa < target × 0.8 E spend > $300 E decile_rank top 2
   - loser: cpa > target × 1.5 OU killed before $100 spend
   - neutral: tudo entre
3. Salvar em /workspace/[produto]/creative-dna/perf-[creative-id].json
4. Invocar registry.py update [creative-id] perf-[creative-id].json

Se for a 10ª rodada (ou múltiplo de 10), rodar também:
5. registry.py dna [slug] → atualiza dna-profile.json

Silent.
```

## Integração na Skill 07 próxima rodada

Antes de gerar briefings (ETAPA 3 ou 5):

```
### PRE-STEP — Carregar DNA aprendido

Se existir /workspace/[produto]/creative-dna/dna-profile.json:
1. Ler o profile
2. Se total_creatives >= 10:
   - Extrair top 5 features com maior delta winners vs losers
   - Injetar como constraint no prompt de geração:

   "Baseado em DNA de {N} criativos anteriores, priorizar:
   - {feature_1}: {valor vencedor}
   - {feature_2}: {valor vencedor}
   - ...
   Reservar 20% de variação pra novelty (não over-fit no DNA)."

Se não existir ou total < 10: gerar normalmente sem bias.
```
