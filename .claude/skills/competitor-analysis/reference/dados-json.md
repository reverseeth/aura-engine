# Competitor Analysis · Referência: JSON companion, o schema do dados.json

> O schema completo do `competitor-analysis/dados.json` (concorrentes analisados e descartados, saturação de claims, funil, gaps, top criativos, formatos de ad, landings com o formato de cada página, radar, soluções alternativas, validated library, swipe, recomendação de posicionamento, status da análise profunda e fontes). Abra ao gravar o `dados.json`.

## O `resumo`, o bloco que a próxima fase lê primeiro

O `dados.json` abre com um objeto `resumo`: até doze campos curtos com o que a fase seguinte precisa saber de primeira, sem abrir o arquivo inteiro. Ele não guarda dado novo, é espelho do que já está mais abaixo: cada campo copia o valor literal do campo de origem, e onde diverge, o campo de origem vence. Preencha por último, depois que o resto do arquivo estiver fechado.

```json
{
  "resumo": {
    "competitors_count": 0,
    "top_competitor": "nome, e em meia linha por que é o que importa",
    "positioning_recommendation_line": "o posicionamento recomendado em uma frase",
    "saturated_claims_top3": ["claim que o mercado inteiro já diz"],
    "open_gaps_top3": ["a lacuna aberta, com a dimensão entre parênteses"],
    "dominant_format": "o formato de ad que domina o nicho",
    "dominant_landing_format": "o formato de página pra onde os ads escalados mandam o tráfego, ou null com menos de três landings classificadas",
    "swipe_adapt_top3": ["o que vale modelar, com a fonte"],
    "swipe_avoid_top3": ["o que não vale, e por quê"],
    "price_range_market": "faixa de preço praticada",
    "hook_archetypes_top3": ["arquétipo de hook recorrente"]
  },
  "competitors_analyzed": [
    { "name": "", "url": "", "accessible": true, "price_base": 0, "mechanism": "", "main_claim": "", "positioning": "", "strengths": [], "weaknesses": [] }
  ],
  "competitors_discarded": [
    { "url": "", "reason": "http_403|timeout|no_snapshot", "fallbacks_tried": ["wayback","archive_today"], "checked_at": "" }
  ],
  "claims_saturation": [
    { "claim": "", "count": 0, "total": 0, "saturation": "HIGH|MEDIUM|LOW|ABSENT" }
  ],
  "funnel_classification": { "TOF": 0, "MOF": 0, "BOF": 0, "classification_confidence": "speculative" },
  "gaps": { "audience": [], "messaging": [], "format": [], "offer": [], "mechanism": [] },
  "top_creatives": [
    { "creative_id": "", "competitor": "", "angle": "", "hook_literal": "", "appearances": 0, "funnel_position": "TOF|MOF|BOF", "ad_library_url": "https://www.facebook.com/ads/library/?id=<ad_id> (opcional — preenchido pela ETAPA 3F ou pela coleta manual)" }
  ],
  "ad_formats": [
    { "format": "", "competitor": "", "duration_s": 0, "structure_notes": "", "iteration_pattern": "", "scale_evidence": "", "scale_signal": "high|medium|low" }
  ],
  "traffic_landings": [
    { "competitor": "", "url": "", "evidence": "", "source": "" }
  ],
  "landing_formats": [
    { "url": "", "competitor": "", "format": "advertorial|listicle|landing|pdp_robust|pdp_lean|quiz|vsl|home", "ads_count": 0, "evidence": "o elemento da página que decidiu a classificação" }
  ],
  "monitoring_radar": [
    { "what": "", "where": "", "trigger_signal": "", "action_if_triggered": "" }
  ],
  "alternative_solutions": [
    { "category": "", "price_range": "", "why_abandoned": "" }
  ],
  "validated_library": {
    "mechanisms": [
      { "name": "", "competitor": "", "mechanization_stage": "name|describe|feature", "sophistication_stage_represented": 3, "angle_paired": "", "validation_evidence": { "days_running": 0, "creatives_same_angle": 0, "appearances_top10": 0, "scale_signal": "high|medium|low" } }
    ],
    "angles": [
      { "angle": "", "competitors": [], "creatives_count": 0, "appearances_total": 0, "funnel_position": "TOF|MOF|BOF", "scale_signal": "high|medium|low" }
    ]
  },
  "swipe_adapt": [ { "item": "", "why": "", "how_to_adapt": "", "where_to_use": "" } ],
  "swipe_avoid": [ { "item": "", "why_avoid": "", "alternative": "" } ],
  "positioning_recommendation": { "angle": "", "mechanism": "", "avatar_segment": "", "page_type": "" },
  "creative_deep_analysis": { "status": "completed|skipped|whisper_unavailable", "creatives_analyzed_count": 0, "patterns_file": "workspace/[produto]/competitor-analysis/creative-patterns.json" },
  "sources": { "collected_at": "", "competitors_analyzed": 0, "meta_ad_library_ads_count": 0, "trendtrack_calls": 0, "wayback_hits": 0, "archive_today_hits": 0 }
}
```
