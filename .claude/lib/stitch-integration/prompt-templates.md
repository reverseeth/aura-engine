# Prompt Templates pra Stitch

Prompts otimizados pra gerar mockups de alta qualidade no Stitch, por tipo de página.
Usar o template correspondente ao que a Skill 05 produziu + substituir `{{ }}` pelos dados reais do produto.

## Template 1 — PDP (Product Detail Page)

Pra produtos mid-high ticket com copy pronta. Skill 05 deu output `05-copy.md`.

```
Design a premium Product Detail Page (PDP) for Shopify.

PRODUCT CONTEXT:
- Brand: {{brand_name}}
- Product: {{product_name}}
- Category: {{category}}
- Price range: {{price_range}}
- Target audience: {{avatar_description}}

SECTIONS NEEDED (in order):
1. Hero — product image + headline "{{headline}}" + subheadline + 2 CTAs (add to cart + learn more)
2. Trust bar — 4 trust indicators with SVG icons (not emojis)
3. Mechanism section — 3-step visual breakdown of how {{mechanism_name}} works
4. Benefits grid — 4 benefit cards with icons + descriptions
5. Before/After section — split comparison with captions
6. Social proof — 3 testimonials with avatars + review count "{{review_count}}"
7. Ingredients/features deep dive
8. Comparison table — product vs alternatives (5 rows)
9. Offer section — 3 pricing tiers (Starter/Popular/BestValue) with "Most Popular" badge
10. Guarantee — money-back badge + 3 guarantee points
11. FAQ accordion — 7 questions
12. Final CTA — mini hero repeat with stronger action

VISUAL STYLE:
- Editorial, clean, premium (think: Apothekary, Medik8, Crown Affair)
- {{brand_primary_color}} as text default (dark neutral)
- {{brand_accent_color}} as accent (use sparingly in CTAs and highlights)
- Off-white #FAFAFA background
- Generous whitespace, no cluttered feel
- SVG icons only (Lucide/Heroicons outline style, stroke 1.5, neutral opacity 0.7)
- Typography: modern serif for headlines (Fraunces or similar), clean sans for body (Inter or similar)
- Subtle shadows, border radius 12-16px on cards
- NO emojis anywhere

CONSTRAINTS:
- Mobile-first responsive (360px min)
- Each section fits logically on screen
- Scroll rhythm: dense → breathing room → dense
- CTAs visually prominent but not aggressive
- NO stock-photo-looking imagery (prefer editorial style)

Generate 3 variations with different hero approaches:
Variation A: Product-hero (product dominant, lifestyle subordinate)
Variation B: Lifestyle-hero (person using product, product in corner)
Variation C: Problem-agitate hero (emotional before-state, product reveal mid-hero)
```

## Template 2 — Landing Page (dedicated)

Pra tráfego de ads, single-purpose, decisão rápida.

```
Design a high-converting Landing Page for cold/warm paid traffic.

PRODUCT CONTEXT:
- Brand: {{brand_name}}
- Product: {{product_name}}
- Awareness level: {{awareness}} (solution-aware/product-aware)
- Big idea: "{{big_idea}}"
- Target CPA: ${{target_cpa}}

STRUCTURE (NESP framework — Novelty/Exclusivity/Simplicity/Proof):
1. Above-fold hero — massive headline, subheadline, 1 hero CTA, trust bar below
2. Mechanism reveal — explain {{mechanism_name}} with 3-step visual + "Here's why this is different"
3. Proof stack — 3-4 forms of proof (clinical, testimonial, press, data)
4. Stack of value — bullet list of everything included + visual of offer components
5. Pricing reveal — single primary offer (or 2-3 tiers if Hormozi-style)
6. Guarantee section — big badge + breakdown of what's guaranteed
7. FAQ — 5-7 key objections handled
8. Final CTA + urgency element (scarcity timer optional)

VISUAL STYLE:
- Modern DTC aesthetic (think: Hims, Ro, Athletic Greens)
- Brand: {{brand_primary_color}} + {{brand_accent_color}}
- Off-white background
- SVG icons (never emojis)
- Generous headline sizes (fluid type, clamp())
- Typography: {{font_choice}}
- Photography: editorial, not stock-photo

Generate 3 variations:
A: Conservative layout (familiar patterns, high conversion risk-averse)
B: Editorial magazine-style (narrative, advertorial-feeling)
C: Bold disruptive (unconventional hero, pattern-interrupt visual)
```

## Template 3 — Advertorial (editorial long-form)

Pra unaware/problem-aware, narrativa primeiro, produto depois.

```
Design an Advertorial / Editorial article page (Zakaria 7-section blueprint).

CONTEXT:
- Product: {{product_name}}
- Target audience: {{avatar}} at awareness level {{awareness}}
- Positioning: educational journalism-style (not ad-feeling)

STRUCTURE (7 sections Zakaria):
1. Magazine-style headline + byline + date + hero image
2. Story lead — personal/relatable opening (narrative, not pitch)
3. Background — "Why [problem] happens" education
4. Root cause reveal — the unknown mechanism problem
5. Unique mechanism (product) — introduce product as the answer
6. Product build-up — proof + testimonials + specs
7. Reveal offer + close — tier pricing + guarantee + final CTA

VISUAL STYLE:
- Magazine/editorial (think: NYT Magazine, The Cut, Outside Online)
- Serif headlines (Playfair, Fraunces, Recoleta)
- Generous line-height for body (1.7-1.8)
- Pull-quotes in italic
- Small author byline + publish date feel
- Images integrated into text (not hero-only)
- SVG icons only in pricing/guarantee section
- {{brand_accent_color}} used sparingly (CTA only)
- Off-white background with subtle warm tint

CONSTRAINTS:
- Reading experience FIRST, selling feel last
- Long-form but scannable (crossheads, pull-quotes, short paragraphs 2-3 lines)
- Mobile-first (advertorials converte 70%+ mobile)
- Feel credible — no ad-style badges or aggressive CTAs early

Generate 2 variations:
A: Classic magazine feel (New Yorker-ish)
B: Modern digital magazine (The Verge-ish)
```

## Template 4 — Quick Iteration Mode

Quando já tem um design base e quer explorar variações:

```
Iterate on the attached design [drag-drop current mockup].

Changes requested:
- {{change_1}} (ex: "make hero more editorial, less product-hero")
- {{change_2}} (ex: "tighten CTA section — currently too busy")
- {{change_3}} (ex: "add proof bar below hero")

Keep the same:
- {{preserve_1}} (ex: "color palette and typography")
- {{preserve_2}} (ex: "overall section order")

Generate 3 iterations.
```

## Pro tips do Stitch

1. **Iteração > perfeição no prompt inicial.** Melhor gerar 3 variações com prompt OK e refinar do que tentar prompt ultra-específico primeiro.

2. **Use referências visuais.** "Style of Apothekary" funciona melhor que descrição abstrata. Stitch conhece brands famosas.

3. **Seja específico sobre o que NÃO quer.** "No emojis, no stock photos, no aggressive colors" previne saída ruim.

4. **Salve variações que gostou mesmo se não são a final.** Partes podem ser mescladas.

5. **Prompt em inglês é melhor.** Stitch foi treinado majoritariamente em corpus inglês, responde melhor a prompts em inglês mesmo se teu target é outro idioma.

6. **Use Gemini 2.5 Pro pra output final.** Flash é pra exploração rápida, Pro pra qualidade final.

## Como trazer de volta pra Aura

Depois de gerar, iterar, aprovar mockup final:

```bash
# 1. Export HTML standalone do Stitch
# 2. Descompacta em workspace do produto:
cd /Users/gustavo/aura-engine/workspace/[produto]/06-page/
unzip ~/Downloads/stitch-export.zip -d stitch-blueprint/

# 3. Invoca Aura skill 06 normalmente:
aura run 06
# ou
"Claude, roda a skill 06 pra gerar a PDP do [produto]"

# Aura detecta stitch-blueprint/ e usa como visual reference.
```
