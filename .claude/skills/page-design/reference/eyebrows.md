# Page Design · Referência: Eyebrows, quando houver

> O eyebrow é opcional: quem decide se a página usa e em quais sections é a direção da ETAPA 3. Este arquivo traz só a regra de qualidade pra quando houver eyebrow: por que rótulo de framework nunca aparece na página, a tabela de eyebrows ruins e bons por section e as regras de tamanho, idioma e Big Idea. Abra ao montar `sections_plan[].eyebrow`.

### Eyebrow é opcional, e quando existe é criativo

Página sem eyebrow é válida, e `sections_plan[].eyebrow` fica `null` nas sections sem ele. Muitas direções dispensam o rótulo acima do título; usar em toda section por hábito é um dos sinais de página gerada.

"Mechanism", "Offer Stack", "Guarantee", "Social Proof", "FAQ" são LABELS INTERNOS do framework de copy (nomes de pasta). **Nunca** aparecem literal na página — soa template genérico. Quando a section tiver eyebrow, use uma tag CRIATIVA e específica do produto.

| Framework (interno) | Eyebrow RUIM (literal) | Eyebrow BOM (criativo, produto-específico) |
|---|---|---|
| Mechanism | "The Mechanism" | "The Science", "Why [Produto] Works", "Inside the Formula", "The [Ingrediente]® Difference" |
| Offer / Stack | "Offer Stack" | "Choose Your Kit", "Build Your Stack", "Pick Your Glow", "Start Here" |
| Guarantee | "Guarantee" | "The Promise", "Zero Risk", "Glow or Get Back", "60 Days, No Excuses" |
| Benefits | "Benefits" | "Why [Produto]", "Five Things Change", "The Difference" |
| Social Proof | "Social Proof" | "Real Results", "Why They Switched", "500+ Stories" |
| FAQ | "FAQ" | "You Asked", "Before You Buy", "The Real Questions" |
| CTA Final | "CTA Final" | "One Last Thing", "Ready?", "Your Glow Starts Here" |

Regras pra eyebrows: 2-5 palavras, específico do produto ("The pH Difference" > "The Science"), **em inglês** (copy pública), nunca rotule o framework, pode pular (trust-bar/hero/cta-final podem não precisar). Se o copy tem um Big Idea, USE ("It's Not the Fragrance. It's the pH.", com a regra do travessão do item S4 de `reference/regua-de-design.md`). Esses eyebrows vão pro `page-plan.json` (`sections_plan[].eyebrow`) e são inseridos no HTML na ETAPA 4.
