# Product Research · Referência: JSON companion, o schema do dados.json

> O schema completo do `product-research/dados.json` (`brands[]`, `validated_elements[]`, `plays[]`, `ranking[]`, `winner`), lido pela `market-research`, pela `competitor-analysis` e pela `offer-builder`. Abra ao gravar o `dados.json`.

### 3. `product-research/dados.json` (AI-only, lido por `market-research`/`competitor-analysis`/`offer-builder`)

```json
{
  "generated_at": "ISO-8601 UTC",
  "niche": "health & supplements",
  "source": "trendtrack_mcp | manual | mixed",
  "notion_url": "https://... | null",
  "filters_used": { "image": { }, "video": { } },
  "brands": [
    {
      "brand": "...", "domain": "...", "monthly_visits": 0, "niche": "...", "product": "...", "format": "...",
      "price_base": 0, "aov_estimated": 0, "offer_structure": { "bundles": [], "subscription_pct": 0, "bump": "...", "upsell": "...", "guarantee": "..." },
      "lp_url": "...", "lp_type": "advertorial|listicle|pdp|landing|quiz",
      "top_ads": [ { "url": "...", "media_url": "...", "days_running": 0, "ad_rank": 0, "duplicates": 0, "format": "image|video", "hook": "...", "angle": "..." } ],
      "creative_format": "...", "problem_mechanism": "...", "solution_mechanism": "...", "ingredient": "...", "angle": "...", "avatar": "...",
      "trustpilot": { "url": "...", "rating": 0, "reviews": 0, "complaint_mix": { "billing": 0, "delivery": 0, "support": 0, "efficacy": 0 }, "verdict": "ok|billing_delivery|efficacy_eliminate|no_source", "quotes": ["..."] },
      "trends": { "problem_term": "...", "problem_class": "rising|flat|recent_peak|hype|decline", "ingredient_term": "...", "ingredient_class": "...", "scenario": "..." },
      "status": "pre_selected|finalist|eliminated", "elimination_reason": "... | null"
    }
  ],
  "validated_elements": [
    { "type": "problem_mechanism|solution_mechanism|angle|product_format|positioning|creative_format|offer_structure", "name": "...", "brands": ["..."], "evidence": "...", "saturation": "open|saturated" }
  ],
  "plays": [
    { "id": "play-01", "base_brand": "...", "pattern": 1, "description": "...", "elements": [ { "type": "...", "name": "...", "from_brand": "...", "evidence": "..." } ], "why_it_wins": "...", "offer_structure": "..." }
  ],
  "ranking": [ { "rank": 1, "brand": "...", "play_id": "play-01", "scores": { "magnitude": 0, "sophistication": 0, "awareness_fit": 0, "um_potential": 0, "avatar_fit": 0, "offer_potential": 0, "creative_potential": 0, "trend_fit": 0 }, "total": 0, "verdict": "TESTAR|TALVEZ|DESCARTAR" } ],
  "winner": { "brand": "...", "play_id": "...", "mechanism_name": "...", "avatar": "...", "offer": { }, "hooks": ["..."] }
}
```
