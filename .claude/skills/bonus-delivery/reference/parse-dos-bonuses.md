# Bonus Delivery · Referência: Parse dos bonuses definidos na offer-builder (ETAPA 1)

> O enum canônico de `bonuses[]` (type, format_hint, condition, delivery_trigger) e a regra de corrigir `type` fora do enum na offer-builder. Abra na ETAPA 1.

### ETAPA 1 — Parse dos bonuses definidos na `offer-builder`

Ler `offer-builder/dados.json.bonuses[]`. Schema esperado — este é o **enum canônico** (fonte: Output Schema da Skill `offer-builder`, reproduzido idêntico lá e aqui):

```json
{
  "id": "bonus-01",
  "name": "nome humano do bônus",
  "description": "1-2 frases: o que é / por que vale",
  "value_anchored": 49,
  "type": "gift_with_purchase | free_complementary_sku | free_ebook | gift_wrapping | digital_guide | discount_code | workbook | checklist | community_access | video_series | consultation_call | trial_extension",
  "format_hint": "in_box | shopify_function | gift_app | pdf | notion | figma | wistia | klaviyo_email | shopify_discount | circle_invite",
  "condition": "unconditional | cart_threshold | tier_specific",
  "delivery_trigger": "post_purchase | on_signup | day_7_post_purchase | on_first_reorder"
}
```

Se o `dados.json` da `offer-builder` tiver um `type` fora dessa lista, volte pra `offer-builder` e corrija LÁ (não inventar mapeamento local — o enum é único).

Pra cada bonus, identificar o playbook correspondente na ETAPA 2.
