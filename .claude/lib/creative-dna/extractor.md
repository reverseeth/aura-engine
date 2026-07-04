# Creative DNA Feature Extractor — prompt structured

Usado pela Skill 08 imediatamente após gerar um briefing completo. Extrai features em formato padronizado e salva no registry.

## Fluxo de invocação (a Skill 08 executa isso internamente — ETAPA 7.6)

1. Depois de completar ETAPA 5 (briefings) e ETAPA 7.5 (compliance), pra cada criativo gerado:
2. Rodar este prompt de extração abaixo
3. Parse JSON response
4. Salvar em `workspace/[produto]/creative-dna/features-[creative-id].json`
5. Invocar (o positional `workspace/[produto]` vem PRIMEIRO; passar o caminho completo do features file):
   ```
   python3 .claude/lib/creative-dna/registry.py add workspace/[produto] [creative-id] workspace/[produto]/creative-dna/features-[creative-id].json --product [slug]
   ```
6. Silent — membro não vê

## PROMPT

```
Você é o Creative DNA Extractor. Leia o briefing do criativo abaixo e extraia features estruturadas respeitando EXATAMENTE o schema em feature_schema.json.

Schema: {conteúdo completo de feature_schema.json}

Briefing do criativo: {conteúdo do concept-XX.md ou script}

Contexto adicional:
- Awareness level alvo (do market research): {awareness_dominant}
- Funnel position (do próprio briefing): {TOF | MOF | BOF}
- Compliance risk score (do checker.md rodado antes): {0-100}
- Hook archetype declarado na geração (ETAPA 4.5.E da Skill 08): {id de archetypes.json}

Retorne APENAS JSON neste formato (nenhum texto antes ou depois):

{
  "creative_id": "[id do briefing]",
  "concept_id": "[parent concept]",
  "source_file": "[path do .md]",
  "produced_at": "[ISO timestamp]",

  "hook_type": "[valor do enum]",
  "hook_archetype": "[id do archetype declarado — enum de feature_schema.json]",
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

Valores enum DEVEM vir do schema. Se impossível classificar, use "not_used" ou
"none" (os enums onde isso é legítimo já contêm esses valores).
Numerics: inferir do briefing (ex: contar números específicos, calcular cuts/s).
avatar_age_depicted: 0 quando não há pessoa no criativo.
```

## Referência rápida da CLI do registry.py

```
python3 .claude/lib/creative-dna/registry.py init workspace/[produto]
python3 .claude/lib/creative-dna/registry.py add workspace/[produto] [creative-id] workspace/[produto]/creative-dna/features-[creative-id].json --product [slug]
python3 .claude/lib/creative-dna/registry.py update workspace/[produto] [creative-id] workspace/[produto]/creative-dna/perf-[creative-id].json
python3 .claude/lib/creative-dna/registry.py dna workspace/[produto] --product [slug]
python3 .claude/lib/creative-dna/registry.py stats workspace/[produto] --product [slug]
python3 .claude/lib/creative-dna/registry.py show workspace/[produto]
```

`update` com creative_id inexistente sai com exit 1 e erro em stderr (typo de id
nunca é no-op silencioso). `dna` com menos de 10 criativos medidos imprime
`insufficient_data` e NÃO sobrescreve um dna-profile.json anterior válido.

## Integração nas Skills (já aplicada — fonte de verdade é cada skill)

O pseudo-código de integração NÃO vive mais aqui (fonte dupla de verdade drifta):

- **Skill 08 — ETAPA 7.6 (DNA Registry Extraction)**: extração inline + validação contra o schema + `registry.py add`. Falha de extração loga em `workspace/[produto]/creative-dna/extraction-errors.log` sem bloquear a skill.
- **Skill 11 — DNA Update**: compõe `perf-[creative-id].json`, classifica outcome (winner/loser/neutral) e roda `registry.py update`; a cada rodada com dados suficientes, `registry.py dna` atualiza o `dna-profile.json`.
- **Skill 08 — PRE-STEP (DNA aprendido)**: se `workspace/[produto]/creative-dna/dna-profile.json` existe com `total_creatives >= 10`, injeta as top 5 features com maior delta winners vs losers como constraint de geração, reservando ~20% de variação pra novelty.
