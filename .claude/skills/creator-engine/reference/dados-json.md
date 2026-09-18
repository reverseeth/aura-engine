# Creator Engine · Referência: Output schema, o dados.json

> O schema completo do `creator-engine/dados.json` (canais, campanhas de seeding, roster, briefs, conteúdo, performance por creator, economics, recrutamento, handoff) com a nota dos números ilustrativos. Abra ao gravar o `dados.json`.

## Output Schema — `creator-engine/creator-engine.md` + `creator-engine/dados.json`

O markdown é humano; o JSON é o contrato com as skills `creative-engine`, `ad-strategy`, `ad-analysis`, `scale-engine` e `content-recycler`.

```json
{
  "creator_engine_id": "uuid-v4",
  "product_slug": "<do manifest>",
  "generated_at": "2026-09-01T00:00:00Z",
  "phase": "A_content | B_performance",
  "phase_reason": "sem breakthrough em manifest.ad_classification",
  "objective": "find_brand_ambassador",
  "operator": "member | va | other",
  "channels": {
    "platform": { "name": "insense | other | none", "brand_added": false, "license_active": false },
    "manual_outreach": false,
    "film_yourself": false,
    "tiktok_shop": { "active": false, "affiliates_count": null, "commission_pct": null, "commission_note": "dois níveis (orgânica vs ads) — a régua vive na `marketplace-engine`", "dedicated_accounts": null }
  },
  "seeding_campaigns": [
    {
      "campaign_id": "seed-01",
      "type": "seeding | paid_per_video",
      "sub_avatar_target": "<id do sub_avatar da `market-research`>",
      "pay_per_video_usd": null,
      "retail_value_check_passed": true,
      "screening_questions": ["..."],
      "status": "draft | live | closed",
      "applications_count": null
    }
  ],
  "roster": [
    {
      "creator_id": "slug-do-creator",
      "name": "",
      "handle": "",
      "platform": "instagram | tiktok | facebook",
      "source": "seeding | paid_campaign | manual_outreach | tiktok_shop | recruitment_ad | member_network",
      "sub_avatar_match": "<id>",
      "diversity_axes": { "age_band": "", "ethnicity": "", "gender": "", "language": "en", "physical_note": "", "psychographic_note": "" },
      "status": "applied | shortlisted | approved | hired | product_sent | filming | content_received | complete | dropped",
      "tier": "seeding | paid_per_video | retainer | ambassador_performance | bounty",
      "rate_per_video_usd": null,
      "retainer_monthly_usd": null,
      "videos_per_week_due": null,
      "performance_terms": {
        "basis": "ad_spend | revenue | coupon",
        "tiers": [ { "band_usd": 10000, "pct": 10 }, { "band_usd": 20000, "pct": 5 }, { "band_usd": 40000, "pct": 2.5 }, { "band_usd": null, "pct": 1 } ],
        "cap_monthly_usd": 10000,
        "coupon_code": null
      },
      "whitelisting": { "eligible": false, "access_granted": false, "access_via": "leasy | manual | none", "monthly_fee_usd": 0 },
      "partnership_access": { "granted": false, "expires_at": null },
      "contract": { "variant": "ad_spend | revenue | ad_spend_whitelisting | none", "signed_at": null, "legal_disclaimer_included": true },
      "report_visibility": "spend_only | full",
      "favorite": false,
      "shipping": { "address_confirmed": false, "product_chosen_by_creator": null, "sent_at": null, "delivered_at": null },
      "notes": ""
    }
  ],
  "briefs": [
    {
      "brief_id": "framework-creator-slug",
      "creator_id": "slug-do-creator",
      "path": "briefs/framework-creator-slug.md",
      "concepts_total": 6,
      "curated": true,
      "concepts_from_08": ["c01", "c03"],
      "angles_from_02": ["sub_avatar_2.angle"],
      "sent_at": null
    }
  ],
  "content": [
    {
      "content_id": "creator-slug-001",
      "creator_id": "slug-do-creator",
      "received_at": null,
      "files_count": 0,
      "dct_ready": false,
      "cut_hooks_timestamps": [],
      "license_source": "contract | platform_terms | none",
      "used_in": { "batch_08": null, "raw_content_campaign": false, "whitelisted": false, "partnership": false }
    }
  ],
  "performance_by_creator": [
    {
      "creator_id": "slug-do-creator",
      "ad_naming_pattern": "contains: <creator-name>",
      "ads": ["ad-id-1"],
      "classes_from_11": { "breakthrough": 0, "spend_winner": 0, "kpi_winner": 0, "loser": 0 },
      "spend_90d_usd": null,
      "soft_metrics": { "thumb_stop_pct": null, "hold_pct": null, "pct_3s_to_15s": null },
      "last_report_at": null,
      "winning_creator": false
    }
  ],
  "economics": {
    "monthly_content_budget_usd": null,
    "creative_production_pct_of_ad_spend": null,
    "hit_rate_reference": { "creators_pct": 14, "internal_pct": 4, "raw_pct": 15, "edited_pct": 5 },
    "roi_audit": { "period": null, "spent_on_creators_usd": null, "winning_ads_count": null, "spend_sustained_usd": null }
  },
  "recruitment": {
    "farming_active": false,
    "paid_recruitment_ads": { "active": false, "hook": "apply to be a brand ambassador", "profitable": null },
    "affiliate_attribution": { "custom_links": false, "app": null }
  },
  "pending_inputs": [],
  "handoff": {
    "for_skill_08": ["content[] com dct_ready=true (matéria-prima licenciada de batch)", "roster[].tier (archetype creator_human disponível)", "briefs[] (concepts já em produção com creators — não duplicar no batch)"],
    "for_skill_10": ["ad_naming_pattern por creator (convenção obrigatória)", "roster[].whitelisting.access_granted (identidades disponíveis)", "roster[].partnership_access", "content[] elegível pra raw content campaign"],
    "for_skill_11": ["performance_by_creator[].ad_naming_pattern (pra atribuir classes por creator)"],
    "for_skill_12": ["roster count por tier vs tabela de creators em retainer da ETAPA 8 da `scale-engine`", "channels.tiktok_shop (fonte incremental de conteúdo)"],
    "for_skill_14": ["roster[] + report_visibility (distribuição do creator-report do Movimento 6)"]
  },
  "sanity_checks": { "total": 12, "passed": 12, "failed": [] }
}
```

> **Os números do exemplo são ILUSTRATIVOS** — os tiers gravados são os defaults da fonte e só valem enquanto o membro não definir os dele. Campo desconhecido fica `null` e entra em `pending_inputs[]` — nunca preenchido com plausível.
