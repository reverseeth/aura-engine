# Checkout & AOV · Referência: Objetivo, índice, pré-flight, quando usar e antes de começar

> O texto integral da abertura, das notas de índice, do pré-flight com os escapes (offer-builder ausente, loja não deployada, setup ausente), do quando usar com a limitação do Purchase e o OTO, e das leituras iniciais com os cinco sistemas nomeados (queries exatas). Abra antes de qualquer alavanca.

A oferta (Skill `offer-builder`) DEFINIU os bumps, upsells e bundles. Esta skill os IMPLEMENTA na loja. Aumentar o lucro por visitante aqui é o que destrava spend mais agressivo nos ads: cada $1 extra de margem por pedido é $1 a mais que você pode pagar de CPA. É a alavanca mais barata do funil porque não custa tráfego novo — só monetiza melhor o tráfego que já chega.

> **Índice completo dos frameworks desta skill:** `.claude/lib/kb-index/` (mapa skill→domínio no README). Os domínios desta skill são `page-landing-cro` (as famílias Checkout/Cart Friction Reduction, AOV Builders e Profit Optimization), `brand-building-bonus-aov` e `offer-pricing-guarantee`. Sempre que uma etapa mandar "consulte a base", rode `search_knowledge` com a `best_query` NOMEADA de cada framework relevante (`deep=true`) — **NUNCA query genérica**. As queries de maior impacto estão embutidas byte-exatas no item 3 de "Antes de Começar" e no ponto de uso de cada alavanca abaixo.
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill checkout-aov --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

### Pré-flight (OBRIGATÓRIO)

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

Valide antes de prosseguir:

- [ ] `workspace/[produto]/manifest.json` existe
- [ ] **Idioma (report_language — regra 0 do CLAUDE.md, INVIOLÁVEL).** Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`), e escreva com o rigor de linguagem simples da regra 0. TODO output interno (`checkout-aov/checkout-aov.md`/`.html`, `checkout-aov/dados.json` descritivo, perguntas e mensagens ao membro) usa esse idioma. **A copy que aparece no checkout/cart pro consumidor (texto do bump, headline do upsell, trust badges, barra de free-shipping) permanece SEMPRE em inglês US**, independente do report_language — é consumidor-final do mercado US e o Meta scraper lê.
- [ ] `offer-builder/dados.json` existe → extrair `bonuses[]`, `pricing` (`main_sku_price`, `aov_expected`), `unit_economics` (`weighted_margin_per_order`, `margin_per_unit`), `guarantee`, a string `offer_stack`, **e o contrato de assinatura: `subscription_architecture` + `onetime_premium_pct`** (governam toda superfície de checkout/upsell que toque assinatura — ver o bloco "Superfícies de assinatura" na Alavanca 1; ausentes em dados.json legado → trate como sem contrato: comportamento atual, nenhuma superfície de assinatura nova, lacuna anotada no output). O `offer-builder` já descreve **bundles** (Solo/3-pack/6-pack com savings), **checkout bump** (complemento $9-19) e **upsell pós-compra** (alto ticket $47-97+) na Etapa 3 — esta skill lê essas decisões, não as reinventa.
- [ ] `manifest.store_url` (handle .myshopify.com ou domínio custom). Se ausente, a página ainda não foi deployada — ver escape-path abaixo.
- [ ] `manifest.storefront` (bloco gravado pela `page-build` na publicação: `theme_id` + `page_url`). **É nesse `theme_id` que esta skill opera** — cart bump/bar/trust row têm que viver no MESMO tema da página. Se `manifest.storefront` não existe (página só em preview, tema não publicado), avise: "A página ainda não foi publicada (`page-build` passo 6.10). Posso gerar o blueprint e aplicar as alavancas no tema de preview, mas antes do launch a publicação precisa acontecer."
- [ ] Detectar **member-stage** (`manifest.stage` ou inferir por `member-stage-awareness.md`) — define a profundidade da implementação (starter = 1-2 alavancas no-code; scaling = stack completo).

Se faltar `offer-builder/dados.json` (a fonte dos bumps/upsells/bundles), em vez de abortar seco ofereça ≥2 caminhos (escape-path ES1):
- **(A)** Rodar a skill `offer-builder` agora pra definir bumps/upsells/bundles com base na unit economics real, OU
- **(B)** Prosseguir com defaults conservadores (bump $15 que caia numa das 4 categorias do Gate de Complementaridade, upsell more-of-same com desconto exclusivo pós-compra, free-shipping threshold ≈ 1.4× AOV) marcando `manifest.skipped_preflight += ["offer-builder/dados.json"]` e avisando no output final que recomenda re-executar quando a oferta real existir.

Se `manifest.store_url` estiver ausente (página não deployada): a config de checkout precisa de uma loja viva pra apontar variantes e thresholds. Ofereça **(A)** rodar a `page-build` (o deploy da página) primeiro, OU **(B)** gerar o blueprint completo (esta skill produz todos os specs) e deixar marcado como `pending_store: true` no output pra aplicar assim que a loja existir — sem inventar IDs de variante.

Se `manifest.json` ou `profile.md` estiverem TOTALMENTE ausentes (membro nunca rodou setup), pare — mas ofereça rodar o setup (Skill `setup`) inline.

## Quando Usar

Na fase **storefront**, depois da página estar no ar (`page-build`) e do tracking instalado (`tracking-setup`), antes dos criativos (`creative-engine`). A ordem importa: a página precisa existir pra ter variantes/produtos referenciáveis, e o pixel/CAPI precisa estar ativo pra que bump e bundle entrem no Purchase medido. **Limitação conhecida do post-purchase:** o evento Purchase da integração nativa dispara no fim do checkout, ANTES do aceite do upsell one-click — o valor do OTO aparece no Shopify mas normalmente NÃO entra no Purchase do Events Manager (o ROAS reportado fica um pouco subestimado; a Skill `ad-analysis` reconcilia com o revenue real do Shopify). Os criativos vêm depois porque o AOV configurado aqui muda o CPA que você pode pagar — e o briefing de ad usa esse número.

## Antes de Começar

1. Leia `workspace/profile.md` — `report_language`, budget, stage, e tools disponíveis (algumas alavancas dependem de app pago).
2. Leia `workspace/[produto]/offer-builder/offer-builder.md` (se não existir, leia o legado `relatorio.md`) + `offer-builder/dados.json` — bundles, bump, upsell, stack de valor, garantia, e unit economics. Os números de aceitação projetados (bump 20-35%; upsell post-purchase 3-8% média da plataforma, 8-14% em oferta bem casada) e o AOV projetado da Etapa 6 do `offer-builder` são a fonte única; aqui você os transforma em config real (sem re-somar — ver ETAPA 4).
3. Puxe os SISTEMAS NOMEADOS da base (rode a `best_query` de cada um, `deep=true` — nunca query genérica):
   - **Pricing Psychology Suite** (rode `pricing psychology anchoring decoy extremeness aversion zero price effect charm pricing mental accounting endowment`) — o kit inteiro num sistema só: **decoy effect** e **extremeness aversion** pra estruturar os tiers de bundle (3 opções, o do meio é o alvo, o premium ancora, o budget faz o meio parecer esperto), **charm pricing** (terminação em 9, left-digit effect — exceto se o posicionamento for premium/round), **zero price effect** (FREE é qualitativamente diferente de "quase grátis" — o threshold de free-shipping tem que entregar frete REALMENTE zero) e **mental accounting** (segregar ganhos: listar bônus e savings separados; integrar perdas: um pagamento só).
   - **Profit Optimization (Profit Per Visitor + 5 Levers)** (rode `profit optimization profit per visitor pricing levers AOV revenue vanity profit sanity`) — a métrica-mãe desta skill: lucro por visitante = lucro por pedido × conversão; "revenue is vanity, profit is sanity".
   - **Free-Plus-Shipping & Order Form Bump** (rode `Brunson free plus shipping buyer 10x order form bump 20 to 50 percent`) — checkbox no order form converte 20-50% porque o cliente já está em modo de compra.
   - **Three OTO Structures** (rode `Brunson three OTO structures next thing do it faster need help upsell`) — as 3 estruturas de OTO (Next Thing / Do It Faster / Need Help?).
   - **Checkout / Cart Friction Reduction** (rode `checkout cart optimization coupon field abandonment first person button glowing box`) — tirar o olho do campo de cupom, CTA em primeira pessoa, atenção gerenciada pro botão.

Não consulte o membro sobre decisões estratégicas (qual tier ancora, qual % de savings) — isso já saiu da Skill `offer-builder` e da base. Pergunte só o que é input externo que você não tem (IDs de variante, app instalado, fulfillment de in-box gift).
