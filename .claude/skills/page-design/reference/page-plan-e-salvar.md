# Page Design · Referência: Persistir page-plan.json, relatórios e manifest (ETAPA 6)

> O shape completo do `page-plan.json` (`schema_version: 2`) com o bloco `strategy`, os três sinais do `page_type`, o `sections_plan` com o campo `media` obrigatório, o bloco `commerce` com o que a página promete, o bloco `quiz` quando o funil é de quiz, o modo de construção, as refs de QA e o preview, as notas sobre `mechanism_name` literal e `page_type` duplicado, o dual output do `design-system.md` e a atualização do manifest pelo script. Abra na ETAPA 6, depois da aprovação e dos tokens.

## ETAPA 6 — Persistir `page-plan.json` + relatórios + manifest

### O `page-plan.json` (com bloco `strategy` COMPLETO)

O contrato é `.claude/templates/schemas/page-design.page-plan.schema.json`: os campos `required` são os que outra skill lê, e o `tools/page-qa/qa_gate.py` valida o arquivo nele no pré-flight da `page-build`. Valide antes de seguir:

```bash
python3 tools/schema_validate.py .claude/templates/schemas/page-design.page-plan.schema.json workspace/[produto]/page/page-plan.json
```

```json
{
  "schema_version": 2,
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
    {"id": "hero", "eyebrow": null, "blocks": ["heading","paragraph","button_row","stats_bar","tag"],
     "media": {"required": true, "kind": "lifestyle", "source": "ai_lifestyle", "status": "ready", "asset": "design/assets/hero-lifestyle.jpg", "acquisition_plan": null}},
    {"id": "mechanism", "eyebrow": "The pH Difference", "blocks": ["eyebrow","heading","paragraph","mechanism_card"],
     "media": {"required": false, "kind": "icon_svg", "source": "none", "status": "ready", "asset": null, "acquisition_plan": null}}
  ],
  "section_order": ["hero","mechanism","benefits","social-proof","offer","guarantee","faq","cta-final"],
  "commerce": {
    "buy_surfaces": [
      {"section": "hero", "kind": "single_cta", "tiers_qty": [1]},
      {"section": "offer", "kind": "pricing_tiers", "tiers_qty": [1, 3, 6]},
      {"section": "cta-final", "kind": "single_cta", "tiers_qty": [3]}
    ],
    "subscription_shown": true,
    "promised_on_page": ["gwp-travel-size", "free_shipping_over_75"],
    "discount_code_shown": null
  },
  "reference_board": {
    "references": [{ "url": "https://...", "title": "nome do site", "source": "awwwards | websearch | member", "marked": true, "image_path": "references/1/desktop-full.png", "takeaways": ["tipografia: ...", "grid: ..."] }],
    "direction": { "feel": "sensação em uma frase", "signature": ["escolha reconhecível"], "forbidden": ["o que a página nunca faz"] },
    "social_board_reused": false
  },
  "brand_discovery": {
    "style": "minimalist-editorial",
    "brand_colors": ["#...","#..."],
    "signals_source": "dembrandt | brand_tokens | palette_engine | manual",
    "reference": "brand-tokens.json do setup | URL da loja do membro | preset Atelier Document | cores informadas pelo membro"
  },
  "build_mode": "direction | reference",
  "design_route": "direction | reference",
  "design_route_ref": "URL do Artifact do canvas (direction) | URLs de referência, uma por seção quando é quebra-cabeça (reference) | null",
  "direction_ref": "direction.md",
  "reference_capture_ref": "SÓ no modo referência: reference-capture/ | null",
  "qa_metrics_ref": "qa-metrics.json",
  "review_ref": "review.md | null quando não houve subagente",
  "preview_url": "previewUrl do deploy-to-vercel | null quando o preview não rodou",
  "qa_overrides": [{"item": "horizontal_overflow | broken_images | html_css_kb", "motivo": "por que o membro liberou", "data": "2026-..."}],
  "destination_ref": "SÓ quando page_type=advertorial ou listicle: destino do soft CTA — handle/URL da pdp_lean gerada numa 2ª passada da cadeia, PDP existente trabalhada, ou checkout direto. null nos demais page_types",
  "design_signals_ref": "SÓ em página antiga (sem schema_version): design-signals.json",
  "design_tokens_ref": "design-tokens.json",
  "design_html_ref": "design/page.html",
  "design_system_ref": "design-system.md",
  "generated_at": "2026-...Z"
}
```

> **`schema_version` é sempre `2` em página nova.** É ele que diz à `page-build` que a página passou pelo QA medido: sem o campo, ela trata a página como antiga, só avisa e lê o `design-signals.json`.
> **Modo e refs da construção.** `build_mode` é o modo que a ETAPA 4 rodou, e `design_route` repete o mesmo valor (`direction | reference`) pra quem já lê esse campo; os valores antigos (`claude-design`, `singlefile-clone`, `section-puzzle`) continuam válidos na leitura de página antiga e nunca são gravados em página nova. `direction_ref` aponta pro `direction.md` da ETAPA 3, `reference_capture_ref` pra pasta de captura do modo referência, `qa_metrics_ref` e `review_ref` pros arquivos da ETAPA 5 e `preview_url` pro link do preview da ETAPA 6. O `eyebrow` de cada section é opcional (`null` quando a direção não usa).
> **`qa_overrides`: a liberação do membro.** Só existe quando um item bloqueante continuou em `fail` depois das 3 rodadas e o membro decidiu seguir. Só três itens são liberáveis (`horizontal_overflow`, `broken_images`, `html_css_kb`), cada um com `{item, motivo, data}`; o schema recusa qualquer outro. Sem liberação, o campo fica `[]`.
> **`brand_discovery.signals_source`** em página nova usa o mesmo enum do `source` do `design-tokens.json` (`dembrandt | brand_tokens | palette_engine | manual`). Em página antiga, `refero`, `screenshot_vision` e `manual` continuam válidos na leitura; `design_clone` saiu.
> `mechanism_name` é o nome **LITERAL** de `offer-builder/dados.json` — não invente, não parafraseie. A skill `consistency-audit` compara esse campo cross-fase; drift aqui falha o gate.
> `page_type` aparece tanto no top-level quanto dentro de `strategy` (downstream lê de ambos) — mantenha idênticos.
> `page_type_signals` guarda os três sinais da 1.1 como eles foram lidos, mesmo quando concordam: `resolved_by` diz o que fechou a decisão — `consensus` (os três na mesma variante), `competitor_variant` (a skill adotou a variante do concorrente dentro da mesma família), `member` (famílias diferentes e o membro escolheu, ou ele pediu o formato direto — é sempre o caso do `quiz`) ou `no_competitor_data` (`dominant_landing_format` nulo ou fase não rodada). `competitor_ads_count` é a soma de `ads_count` das landings do formato dominante.
> **Bloco `commerce`: o que a página promete e a loja precisa ter.** É uma declaração, não uma configuração — a `page-design` não cria nada no Shopify. `buy_surfaces[]` lista TODO lugar da página com botão de compra (`section`, `kind` em `pricing_tiers | single_cta | sticky_cta`, e `tiers_qty` com as quantidades que aquela superfície oferece); `subscription_shown` diz se a página mostra opção de assinatura, e tem que bater com o `subscription_architecture` do `offer-builder` (`no_subscription` obriga `false`); `promised_on_page[]` traz o id de cada bônus de `bonuses[]` que a página anuncia, mais o limite de frete grátis quando ele aparece; `discount_code_shown` é o código que a página exibe, ou `null`. A `page-build` lê esse bloco na sub-etapa 6.1b para criar o produto com uma variante por quantidade, ligar cada botão ao ID certo e reprovar no check bloqueante de IDs qualquer quantidade sem variante à venda.
>
> **Bloco `quiz`: só quando `page_type` é `quiz`.** Ele traz `profiles[]` (um por alternativa da pergunta que roteia, com `slot`, `name`, `sub_avatar`, `recommendation` e `lead_objection`) e `screens[]` (uma entry por tela, com `id`, `kind`, o `step` da barra de progresso, o `routes` que marca a única pergunta que ramifica, as `answers[]` com o `to` de cada uma e o `media` da tela). O shape completo, com as regras que ele obedece, está em `reference/quiz-funnel.md` (sub-etapa 1.7). Nesse caso o `commerce.buy_surfaces[]` ganha o campo `screen` (a tela de resultado dona daquele botão), que é o que faz o check bloqueante de IDs da `page-build` cobrir o funil inteiro, e `sections_plan` tem a entry `quiz`, o funil numa section só.
>
> **Campo `media` (ETAPA 1.6) é obrigatório em toda entry de `sections_plan`**: `required` (bool), `kind` (`lifestyle | packshot | before_after_pair | review_faces | diagram | icon_svg | none`), `source` (`member_photo | supplier_photo | ugc | ai_lifestyle | none`), `status` (`ready | placeholder`), `asset` (path em `design/assets/` ou null), `acquisition_plan` (null quando `ready`; **obrigatório e específico** quando `placeholder` — ex: "foto lifestyle com modelo, membro fotografa até sexta"). A `page-build` bloqueia deploy enquanto houver `status: "placeholder"`.

### Relatórios (dual output — rule 6b)

Salve `design-system.md` (paleta role-tagged, tipografia, spacing, radii, shadow, density, components por section — humanizado, no `report_language`; com `page_type: quiz`, ele ganha a seção **Mapa do quiz** descrita na 1.7.7 de `reference/quiz-funnel.md`) e gere o `.html` companion com `python3 tools/render_report.py workspace/[produto]/page/design-system.md` (rule 6b: nunca escrito à mão; convenções de Markdown em `.claude/templates/aura-html-components.md`).

> Nota: `design/page.html` é a página do CONSUMIDOR (ícones SVG, sem emoji, sem logo Aura). Os relatórios internos (`design-system.html`) são documentos Aura gerados pelo `render_report.py` (logo Aura na topbar, emojis OK). Não confunda os dois.

### Manifest

Atualize o manifest pelo script: `python3 tools/manifest.py <slug> complete page-design` (faz backup, valida e grava `updated_at`; nunca editar o JSON à mão). `page_type` e `signals_source` ficam só no `page-plan.json` (é de lá que a `page-build` e a `consistency-audit` leem); nada disso vai pro manifest. Se o `tokens.py` falhou depois da aprovação, não rode o `complete`: a etapa fica aberta até o `design-tokens.json` existir (`reference/design-tokens.md`).

- Regenera o painel: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza `workspace/[produto]/ABRIR-AQUI.html`).
