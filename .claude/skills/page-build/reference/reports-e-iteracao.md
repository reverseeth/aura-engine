# Page Build · Referência: Reports, iteration loop, mensagem final e self-audit (ETAPA 7)

> O conteúdo do `page-report.md` com a seção de configuração da loja, o schema do `deploy-report.json` com o bloco `store_config`, a atualização do manifest, o iteration loop por tipo de ajuste (markup, estrutural, re-compile, preço, FAQ), a mensagem final e o bloco de self-audit expandido desta skill. Abra na ETAPA 7 e antes de declarar concluído.

## ETAPA 7 — Reports (dual output — rule 6b) + iteration loop

### Reports

Salve `page-report.md` (fonte pra AI) + `deploy-report.json`, e gere `page-report.html` (humano) com `python3 tools/render_report.py workspace/[produto]/page/page-report.md` (rule 6b: o `.html` nunca é escrito à mão; convenções de Markdown em `.claude/templates/aura-html-components.md`).

Conteúdo do `.md`/`.html`: plano de sections + justificativa (de `page-plan.json`), brand signals usados (source), design system, variante aprovada, lista de arquivos com paths absolutos, settings expostos por section (resumo), **seção "Configuração da loja"** (o que a 6.1b criou, o que já existia e foi conferido, e o que o membro precisa abrir no admin — cada pendência com o que fazer lá e o que ela destrava; as de outra fase com o dono escrito), **resumo da camada GEO** (nós Schema.org gerados + fatos do bloco agent-facts + o que ganha: discovery/citação por AI search, não venda-no-chat — seja honesto com o membro), fontes provisionadas (6.4b), preview links, resultado do gate de performance e do fidelity check (6.11), issues conhecidas, histórico de iterações.

`deploy-report.json`:
```json
{
  "deploy_id": "<uuid>", "produto": "[slug]", "store": "<STORE>",
  "live_theme_id": "<LIVE_THEME_ID>", "theme_id": "<NEW_THEME_ID>",
  "cli_version": "<output de shopify version>",
  "preview_url_editor": "https://<STORE>/admin/themes/<NEW_THEME_ID>/editor?template=page.<produto>",
  "preview_url_storefront": "https://<STORE>/pages/<produto>?preview_theme_id=<NEW_THEME_ID>&view=<produto>",
  "sections_deployed": [{"id": "hero", "type": "page-<produto>-hero", "blocks_count": 0}, {"id": "benefits", "type": "page-<produto>-benefits", "blocks_count": 4}],
  "geo": {"jsonld_types": ["Product", "Offer", "AggregateRating", "BreadcrumbList", "FAQPage"], "jsonld_validated": true, "agent_facts_block": true, "schema_path": "workspace/<produto>/page/staging/geo/product-schema.json"},
  "store_config": {
    "product": {"id": "gid://shopify/Product/...", "handle": "<handle>", "status": "draft", "published_online_store": false, "action": "created | verified"},
    "variants": [{"qty": 1, "id": "gid://shopify/ProductVariant/...", "price": 49.00, "compare_at": null, "sku": "<sku>", "available_for_sale": true, "action": "created"}],
    "selling_plan": {"id": "gid://shopify/SellingPlan/...", "app": "shopify_subscriptions", "attached_to_variants": [1], "action": "created"},
    "discounts": [{"kind": "automatic | code | bxgy", "title": "<título no admin>", "starts_at": "2026-MM-DDTHH:MM:SSZ", "ends_at": "2026-MM-DDTHH:MM:SSZ", "action": "created"}],
    "already_existed": ["produto com o mesmo handle, conferido campo a campo"],
    "member_review": [{"what": "publicar o produto", "where": "admin, Products", "unlocks": "a página vende"}],
    "pending_other_phases": [{"item": "brinde <nome do bônus>", "owner": "bonus-delivery", "phase": "A"}],
    "id_check": {"passed": true, "failures": []}
  },
  "gates": {"performance": "pass"},
  "fonts_provisioned": {"method": "google_fonts | local_files | mixed | none_needed", "families": ["Geist"], "local_bytes": 0, "verified_in_html": true},
  "validation_passed": true, "validation_errors": [], "push_warnings": [],
  "marker_verified": true, "smoke_test_passed": true,
  "fidelity_check": {"passed": true, "compared_at": "2026-MM-DDTHH:MM:SSZ", "divergences_fixed": []},
  "published": false, "page_url": null,
  "staging_dir": "workspace/<produto>/page/staging",
  "deployed_at": "2026-MM-DDTHH:MM:SSZ"
}
```

Atualize o manifest pelo script (nunca editar o JSON à mão): `python3 tools/manifest.py <slug> complete page-build`; se ainda ausente, `python3 tools/manifest.py <slug> set store_url '"<loja>.myshopify.com"'`; se o 6.10 publicou, o bloco `storefront` (`theme_id`/`page_url`/`published_at`) já foi gravado lá — confira que `published`/`page_url` do deploy-report batem com ele.

Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (onde `<slug>` é o `product_slug` — atualiza o `ABRIR-AQUI.html`).

### Iteration loop (iteration-driven-refinement)

> "Página compilada, validada, gates passados e deployada (preview acima). Como o Liquid foi gerado deterministicamente do HTML que você aprovou, o theme editor é pixel-idêntico ao que você viu. Quer ajustar? Pode pedir 'hero mais apertado', 'cores mais escuras', 'features em 2 colunas', 'adicionar countdown na oferta'. Refino sem regenerar do zero."

Pra ajustes:
- **Só markup/schema/CSS de section** (spacing, layout, cor, texto, blocks novos dentro de section existente) → ajuste o HTML aprovado (`design/page.html`), re-rode SPLIT→COMPILE só da section afetada (Modo C single-section) OU edite o `{% stylesheet %}` direto → revalide → push APENAS das sections alteradas com `--only "sections/<arquivo>.liquid"`. O template JSON no ar não entra nesse push — as fotos, os textos e a ordem que o membro configurou no theme editor ficam intactos.
- **Estrutural** (section nova, remoção ou reordenação — mexe no template JSON) → NUNCA regenerar o template por cima do que está no ar: regenerar do preset apaga em silêncio as fotos e os textos que o membro configurou no editor. Fluxo da Regra 6b da `shopify-theme-safety.md`: `shopify theme pull --only` do template no ar → `python3 tools/theme-template-merge.py` (`--add`/`--remove`/`--move`) → push do template mergeado. A section nova em si compila e valida como sempre (validação de blocks — ETAPA 4) e sobe com `--only`.
- **Re-compile apaga renames, restaurações E os IDs de variante**: o conversor regenera o `.liquid` do zero — depois de qualquer re-COMPILE, re-aplique o rename semântico daquela section (ETAPA 2), re-rode a restauração de SVGs grandes dela (grep `icon-placeholder`), **refaça o wire dos IDs de variante e do plano de venda (6.1b.4) e rode o check bloqueante de IDs (6.1b.5) antes do push**, e recalcule o hash do `data-aura-build` se foi o hero.
- **Preço/rating/política mudou** → regenere o `product-schema.json` e o bloco agent-facts (ETAPA 4.5), revalide o JSON-LD, e confira que ainda bate com a config Shopify (ETAPA 4.5.1) antes do re-push. Schema e config nunca podem divergir. **Preço mudou de verdade** (não só na página): atualize a variante ou o desconto na loja pela 6.1b.3 e rode o check bloqueante de IDs de novo, senão a página anuncia um número e o carrinho cobra outro.
- **FAQ mudou (pergunta adicionada/removida/reescrita na section faq)** → regenere o nó FAQPage do `product-schema.json` e revalide — as Q&A do Schema têm que continuar idênticas às da página.
- **SEMPRE pull antes de re-push** (Regra 1) pra preservar settings que o membro mexeu no editor.
- **SEMPRE** revalide com `shopify-plugin:shopify-liquid` + rode o snippet de validação do template JSON antes de cada push.
- Atualize `deploy-report.json` (`iterations: [...]` com timestamp + mudanças). Max 3 iterações sem progresso → escalate.

### Mensagem final

> "Page-build completo. [Se publicou: 'Página no ar em `<page_url>`.' / Se não: 'Página no preview — publica quando você aprovar; sem publicar, a campanha da Skill `ad-strategy` não tem URL de destino.'] Próximo passo: 'tracking' (tracking-setup — pixel + CAPI antes dos criativos), depois 'checkout' (checkout-aov). Na sequência vêm o bônus Fase A (skill `bonus-delivery`, se a sua oferta tem bônus) e a retention Fase A (skill `retention-engine` — flows de recuperação: abandoned cart + post-purchase, infraestrutura que se arma ANTES de ligar tráfego), e só então 'creatives' (skill `creative-engine`)."

## Self-audit silencioso (rule post-task-self-audit) — deep audit (skill peso crítico)

Antes de declarar concluído, rode os 5 gates expandidos e corrija inline (sem mencionar): cada section do `section_order` virou um `.liquid` validado; template JSON tem `blocks{}` + `block_order[]` não-vazios em toda section **block-based** (schema define blocks) — sections monolíticas legitimamente ficam com `blocks: {}` (NÃO "corrija" injetando blocks fantasma); copy injetada veio de `06` (não inventada); **zero `icon-placeholder` residual nos `.liquid` (restauração de SVGs grandes da ETAPA 2 rodou) e zero placeholder `{{MAIÚSCULA}}` nas sections/template (check bloqueante da ETAPA 4)**; **nenhuma section com `media.required` sem imagem e nenhum `media.status: "placeholder"` sobrevivente do `page-plan.json`**; cores das section settings batem com `design-tokens.json`; **web fonts provisionadas (6.4b) e confirmadas no HTML servido — a tipografia aprovada não caiu pra fallback, e nenhum bloco `data-aura-fonts` em base64 sobreviveu dentro das sections**; blocks `pricing_tier` expõem `qty` + `variant_id` (contrato da recipe deploy-shopify-product); **a 6.1b rodou: produto criado ou conferido, cada formato da oferta pelo caminho nativo ou registrado como pendência com dono, IDs de variante (e o plano de venda, se a página mostra assinatura) preenchidos em TODAS as superfícies de compra do `commerce.buy_surfaces`, gravados em `manifest.storefront` pelo script, e o check bloqueante de IDs passou nos seis itens — nenhum ID de exemplo sobrevivente, nenhum ID que a loja não responde, nenhuma variante indisponível ou produto fora do canal Online Store**; **o bloco `store_config` do deploy-report separa o que foi criado, o que já existia e o que o membro precisa revisar, e a seção "Configuração da loja" do `page-report.md` diz o mesmo**; **selling plan/preços da página batem com `subscription_architecture` + `onetime_premium_pct` da `offer-builder` (assinatura = preço-base; one-time = base × (1+premium); zero "Subscribe & Save X%"); campos ausentes = fallback legado anotado**; **JSON-LD da ETAPA 4.5 valida (Product + BreadcrumbList no mínimo), todo campo vem de fonte real (nenhum rating/preço inventado — nó omitido se sem dado), e Schema + agent-facts + config são a MESMA verdade (envio/retorno/garantia/rating/preço)**; GATE 1 (performance budget) passou (sem override silencioso); marker `data-aura-build` verificado (hash atual) + smoke test OK antes de declarar "no ar"; **fidelity check do 6.11 rodou (screenshots por visão, live/preview vs design aprovado) e divergências reais foram corrigidas**; se publicou, `manifest.storefront` gravado com theme_id/page_url/published_at; `page-report.html` gerado pelo `render_report.py` a partir do `page-report.md`. Surface só o que exige decisão (rating do Schema que diverge da review app e precisa escolha de qual fonte vale, publicar ou não o tema, placeholder de imagem que só o membro pode resolver).
