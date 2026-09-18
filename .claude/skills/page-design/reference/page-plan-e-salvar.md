# Page Design · Referência: Persistir page-plan.json, relatórios e manifest (ETAPA 4)

> O schema completo do `page-plan.json` com o bloco `strategy`, os três sinais do `page_type`, o `sections_plan` com o campo `media` obrigatório e as refs de design, as notas sobre `mechanism_name` literal e `page_type` duplicado, o dual output do `design-system.md` e a atualização do manifest pelo script. Abra na ETAPA 4.

## ETAPA 4 — Persistir `page-plan.json` + relatórios + manifest

### 4.1 `page-plan.json` (com bloco `strategy` COMPLETO)

```json
{
  "produto": "[slug]",
  "page_type": "advertorial | listicle | landing | pdp_robust | pdp_lean | quiz",
  "strategy": {
    "awareness_level": "Problem-Aware | Solution-Aware | Product-Aware | Most-Aware",
    "sophistication_stage": 4,
    "skepticism": "baixo | médio | alto",
    "product_type": "commodity | nova categoria | disruptor | incremental",
    "has_unique_mechanism": true,
    "mechanism_name": "[LITERAL do offer-builder/dados.json — nome exato do mecanismo nomeado]",
    "hero_type": "[1 dos 5 canônicos da base]",
    "decision_modalities_served": ["spontaneous", "competitive", "humanistic", "methodical"],
    "page_type": "advertorial | listicle | landing | pdp_robust | pdp_lean | quiz",
    "page_type_signals": {
      "awareness": "[o page_type que a consciência dominante pede]",
      "copy_lead": "[o page_type que o lead_type da copy-engine confirma, ou null quando o campo não existe]",
      "competitor_landing_format": "[dominant_landing_format da competitor-analysis, ou null]",
      "competitor_ads_count": 0,
      "resolved_by": "consensus | competitor_variant | member | no_competitor_data"
    },
    "hybrid": false
  },
  "sections_plan": [
    {"id": "hero", "eyebrow": "[eyebrow criativo ou null]", "blocks": ["eyebrow","heading","paragraph","button_row","stats_bar","tag"],
     "media": {"required": true, "kind": "lifestyle", "source": "ai_lifestyle", "status": "ready", "asset": "design/assets/hero-lifestyle.jpg", "acquisition_plan": null}},
    {"id": "mechanism", "eyebrow": "The pH Difference", "blocks": ["eyebrow","heading","paragraph","mechanism_card"],
     "media": {"required": false, "kind": "icon_svg", "source": "none", "status": "ready", "asset": null, "acquisition_plan": null}}
  ],
  "section_order": ["hero","mechanism","benefits","social-proof","offer","guarantee","faq","cta-final"],
  "brand_discovery": {
    "style": "minimalist-editorial",
    "brand_colors": ["#...","#..."],
    "signals_source": "refero | screenshot_vision | design_clone | manual",
    "reference": "Linear | print loja X | hex de competitor.com | preset Atelier Document"
  },
  "design_route": "claude-design | singlefile-clone | section-puzzle",
  "design_route_ref": "URL do Artifact do canvas (claude-design) | URL da página de referência (singlefile-clone) | mapa fonte→section (section-puzzle) | null",
  "destination_ref": "SÓ quando page_type=advertorial ou listicle: destino do soft CTA — handle/URL da pdp_lean gerada numa 2ª passada da cadeia, PDP existente trabalhada, ou checkout direto. null nos demais page_types",
  "design_signals_ref": "design-signals.json",
  "design_tokens_ref": "design-tokens.json",
  "design_html_ref": "design/page.html",
  "design_system_ref": "design-system.md",
  "generated_at": "2026-...Z"
}
```

> `mechanism_name` é o nome **LITERAL** de `offer-builder/dados.json` — não invente, não parafraseie. A skill `consistency-audit` compara esse campo cross-fase; drift aqui falha o gate.
> `page_type` aparece tanto no top-level quanto dentro de `strategy` (downstream lê de ambos) — mantenha idênticos.
> `page_type_signals` guarda os três sinais da 1.1 como eles foram lidos, mesmo quando concordam: `resolved_by` diz o que fechou a decisão — `consensus` (os três na mesma variante), `competitor_variant` (a skill adotou a variante do concorrente dentro da mesma família), `member` (famílias diferentes e o membro escolheu, ou ele pediu o formato direto — é sempre o caso do `quiz`) ou `no_competitor_data` (`dominant_landing_format` nulo ou fase não rodada). `competitor_ads_count` é a soma de `ads_count` das landings do formato dominante.
> **Campo `media` (ETAPA 1.6) é obrigatório em toda entry de `sections_plan`**: `required` (bool), `kind` (`lifestyle | packshot | before_after_pair | review_faces | diagram | icon_svg | none`), `source` (`member_photo | supplier_photo | ugc | ai_lifestyle | none`), `status` (`ready | placeholder`), `asset` (path em `design/assets/` ou null), `acquisition_plan` (null quando `ready`; **obrigatório e específico** quando `placeholder` — ex: "foto lifestyle com modelo, membro fotografa até sexta"). A `page-build` bloqueia deploy enquanto houver `status: "placeholder"`.

### 4.2 Relatórios (dual output — rule 6b)

Salve `design-system.md` (paleta role-tagged, tipografia, spacing, radii, shadow, density, components por section — humanizado, no `report_language`) e gere o `.html` companion com `python3 tools/render_report.py workspace/[produto]/page/design-system.md` (rule 6b: nunca escrito à mão; convenções de Markdown em `.claude/templates/aura-html-components.md`).

> Nota: `design/page.html` é a página do CONSUMIDOR (ícones SVG, sem emoji, sem logo Aura). Os relatórios internos (`design-system.html`) são documentos Aura gerados pelo `render_report.py` (logo Aura na topbar, emojis OK). Não confunda os dois.

### 4.3 Manifest

Atualize o manifest pelo script: `python3 tools/manifest.py <slug> complete page-design` (faz backup, valida e grava `updated_at`; nunca editar o JSON à mão). `page_type` e `signals_source` ficam só no `page-plan.json` (é de lá que a `page-build` e a `consistency-audit` leem); nada disso vai pro manifest.

- Regenera o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `workspace/[produto]/ABRIR-AQUI.html`).
