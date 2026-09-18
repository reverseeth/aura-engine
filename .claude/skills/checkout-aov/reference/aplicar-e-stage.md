# Checkout & AOV · Referência: Aplicar na loja ou entregar o blueprint, profundidade por stage e matriz de apps (ETAPAs 5, 6 e 6b)

> Os caminhos de aplicação (tema com shopify-theme-safety, admin, recipe nativa, config spec de app), o blueprint pendente sem loja, a profundidade por stage e a matriz de apps de upsell por estágio. Abra na ETAPA 5.

### ETAPA 5 — Aplicar na loja (se store_url existe) ou entregar blueprint

**Se a loja existe e o membro aprovou o blueprint** (checkpoint de iteration-driven-refinement — "Aprova a direção ou ajusto pricing/copy?"):

- **Caminhos do tema** (cart bump, free-shipping bar, trust row na PDP): operar no tema onde a página vive — `THEME_ID = manifest.storefront.theme_id` (gravado pela `page-build` na publicação; se é o live, os comandos levam `--allow-live`). Seguir `shopify-theme-safety` INTEGRAL, sempre com `--path` explícito (Regra 8 proíbe push sem `--path`):
  ```bash
  shopify theme pull --theme "$THEME_ID" --store "$STORE" --path workspace/[produto]/page/theme-clone --nodelete
  # editar → marker data-aura-build no root da section editada (Regra 4 — atributo de dados, NUNCA comentário Liquid)
  shopify theme push --theme "$THEME_ID" --store "$STORE" --path workspace/[produto]/page/theme-clone --nodelete [--allow-live se THEME_ID é o live]
  # verificação: curl -s <página> | grep data-aura-build  → depois smoke test (Regra 7)
  ```
  O iteration loop dá `pull` antes de re-push pra não sobrescrever settings do theme editor.
- **Caminhos de admin** (shipping rate, checkout branding, discount function via app): documentar os passos exatos do painel (não dá pra automatizar tudo via CLI) — ex: "Settings → Shipping → Add rate → condition Order price ≥ $75 → price $0.00".
- **Caminho nativo automatizável** (bundles fixos): recipe `.claude/automations/recipes/create-fixed-bundles.md` (Admin GraphQL `productBundleCreate` — cria os tiers e devolve variant IDs pro wire da PDP).
- **Caminhos de app**: NENHUM app de upsell tem API pública de configuração — gere o **config spec** (produto, preço, copy, downsell, IDs de variante reais) pro membro colar no painel do app. IDs de variante: pedir ao membro ou ler via Admin API/MCP se conectada.

**Se a loja NÃO existe** (`pending_store: true`): entregar o blueprint completo, marcar cada alavanca como `pending` no JSON, e avisar no output final que aplica assim que a `page-build` deployar a loja. Sem inventar IDs de variante nem aplicar nada.

### ETAPA 6 — Member-stage (profundidade da implementação)

- **Starter** (0-30 dias, budget apertado): 1-2 alavancas de maior alavancagem e menor esforço — geralmente **bundle na PDP** (zero app, já tem o pricing block) + **free-shipping bar** (tema). Post-purchase via ReConvert se o membro quiser (custo quase zero — ver matriz), nunca extension custom. Explicar o porquê de cada escolha (educação embutida).
- **Validating** (30-90 dias): adicionar **cart bump** + **um app de upsell** no-code (matriz abaixo). Trust row na PDP. Começar a medir take rates reais.
- **Scaling** ($5k+/mês): stack completo — post-purchase one-click via app (ou extension custom se houver dev), quantity-break via Function (app público; CLI custom só em Plus), checkout trust via extension (Plus), bundle nativo automatizado. A margem extra justifica o custo de app premium.

Não recomende post-purchase extension custom pra starter com $500/mês; não deixe um scaling com $20k/mês só com bundle na PDP (desperdiça a alavanca de upsell one-click).

### ETAPA 6b — Matriz de apps de upsell por estágio (curadoria 2026)

Não existe app vencedor universal — existe vencedor por superfície e estágio. Critério de decisão por preço/volume:

| Stage | App default | Preço | Por quê |
|---|---|---|---|
| **Starter / validating** | **ReConvert** | $4.99/mês + 0.75% de comissão sobre a receita de upsell | Custo alinhado ao resultado (quase zero risco); lift comprovado ~15%; cobre post-purchase + thank-you |
| **Validating / scaling** | **AfterSell** | $34.99/mês até 500 pedidos | Quando o volume faz a comissão do ReConvert passar o flat fee; A/B nativo com milhares de variações |
| **Scaling com funil multi-step** | **Zipify OCU** | flat acima de 5k pedidos | Único com lógica de funil post-purchase de múltiplos passos; aceitação 8-14% auditada em oferta bem casada |
| **Enterprise (~$1M+/mês, catálogo grande)** | **Rebuy** | $99 a $1.000+/mês por volume | Recomendação por AI só compensa com catálogo profundo; pro membro típico Aura (1-3 SKUs hero), a OFERTA da `offer-builder` decide o upsell melhor que algoritmo cego — documentar como teto, nunca default |

**Regra transversal:** nenhum desses apps expõe API pública de configuração — o setup é painel manual. Esta skill gera o **config spec** completo (produto, preço com âncora, copy, downsell, ordem das ofertas) pro membro colar no painel; a automação de verdade fica no caminho nativo (bundles via `productBundleCreate`, shipping rate via admin).
