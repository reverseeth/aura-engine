---
name: retention-engine
description: Flows de retenção e lifecycle por email via ESP (Klaviyo primário; Omnisend, MailerLite e Shopify Email por assets mais setup-guide), em duas fases detectadas no pré-flight. Fase A, pré-launch, depois da checkout-aov e da bonus-delivery e antes dos criativos, arma os flows de recuperação disparados por evento (abandoned cart e post-purchase welcome, mais o Email 1 do welcome só se a página promete oferta ou bônus no cadastro), infraestrutura de cash flow que custa zero e não é email marketing. Fase B, pós-launch com 50 compras ou mais, entra com o welcome completo, win-back, replenishment com a janela de reorder, adaptação sazonal dos flows e as ops básicas (chargeback, refund da garantia, CS). Cria os flows pelo Klaviyo MCP oficial quando existe, sempre em draft, com fallback pra HTML mais setup-guide que o membro importa; é o único executor de email do pós-compra. Use quando o membro disser "retention", "email flows", "automation", "lifecycle", "Klaviyo".
---

# Retention Engine · Passo 12 (Fase A) · Passo 19 (Fase B) · apelido antigo: 13 <!-- gen:title -->

## Quando usar

Em dois momentos, com escopos diferentes (`reference/contexto.md`). Fase A, pré-launch: operador de elite nunca liga tráfego pago sem o abandoned cart armado; entram só os flows por evento que recuperam dinheiro do launch (abandoned cart, post-purchase welcome e o Email 1 do welcome se a página promete oferta ou bônus `on_signup`), sem segmentação, porque não há base pra segmentar. Fase B, pós-launch com 50 compras ou mais: welcome completo, win-back, replenishment, cadência e as ops pós-launch; antes disso, segmentação é ruído.

Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight (obrigatório)

Pastas do produto sem número; se faltar a pasta nova de uma fase anterior, rode `python3 tools/migrate.py --product [slug]` e leia da nova. Íntegra em `reference/contexto.md`.

1. Fase pelo `manifest.retention` e `skills_completed`: Fase A se `phase_a_done` não é `true` e a loja está no ar (`page-build`); Fase B se `phase_a_done` é `true`, a campanha está ativa e há 50 compras ou mais; com menos, oferecer revisar os flows da Fase A ou esperar. Flow específico pedido pelo membro é respeitado, com aviso se estiver fora da fase.
2. Gate da `consistency-audit`, phase-aware: ausente na Fase A é o normal; `BLOCK` oferece rodar a auditoria ou seguir marcando `skipped_preflight`; `CAUTION` pede OK; `GO` segue.
3. ESP em `manifest.esp` (enum exato; `shopify_email` com underscore): ausente, perguntar e gravar; `shopify_email` vai direto pro caminho de assets; `none` recomenda o Klaviyo no free tier e, se o membro preferir decidir depois, gera os assets pra importar.
4. `offer-builder/offer-builder.md` e `dados.json` (janela de reorder, garantia, `bonuses[]` com `delivery_trigger`, `subscription_architecture`), `market-research/market-research.md` (objeções e dores viram hooks), `copy-engine/dados.json.email_hooks[]` se existir (seed dos subject lines) e `finance-engine/dados.json.cohorts` se existir e calibrado (troca benchmark por número em três lugares); a `finance-engine` nunca é pré-requisito.

## Contexto a carregar

1. `report_language` do profile (default `pt-BR`) no relatório, no setup-guide e na conversa; a copy dos emails (subject, preview, body, CTA) fica sempre em inglês US.
2. Base pelo índice (domínios `retention-email` e `persuasion-psychology`, mais Desire Calendar e Subscription Economics Playbook embutidos): `python3 .claude/lib/kb-index/kb_lookup.py --skill retention-engine --domain <domínio desta etapa>`; `best_query` exata com `deep=true`, no máximo 10 buscas adicionais por etapa; as queries embutidas nos arquivos de `reference/` são piso obrigatório, rodam sempre e não contam no teto; nunca query genérica nem busca repetida.
3. TrendTrack opcional: padrões de cadência e subject lines de 1 a 3 concorrentes como referência de timing, nunca copiados (`reference/papeis-e-bonuses.md`).

## Fluxo da skill

### ETAPA 0 · Detectar a fase e o ESP

É o pré-flight acima; o texto integral está em `reference/contexto.md`.

### ETAPA 1 · Papéis do pós-compra e conexão com os bônus

Leia `reference/papeis-e-bonuses.md`. Cada artefato tem um dono: a `bonus-delivery` produz o asset e o trigger; esta skill é o único executor de email (monta o flow e injeta `{{BONUS_LINK}}`); a `content-recycler` produz variação de nutrição derivada do winner, em flow separado. Case o `delivery_trigger` de cada bônus com o email que entrega (`on_signup` no Email 1 do welcome, `post_purchase` no Email 1 do post-purchase, `day_7_post_purchase` no Email 3, `on_first_reorder` no replenishment); asset ainda não gerado fica como placeholder avisado.

### ETAPA 2 · Governança dos flows e seed de subject lines

Leia `reference/governanca-dos-flows.md`. Mapa flow e fase (abandoned cart e post-purchase na A; welcome só o Email 1 na A e a série na B; win-back e replenishment na B). Puxe uma vez os quatro frameworks de governança (Rule of 1, 3-to-1, coordenação email e SMS, email como carta de uma pessoa real) e aplique em todos. Seed de subject lines: os `email_hooks[]` da `copy-engine`, adaptados ao contexto de cada flow, sempre em inglês US, diretos e sem aviso; ausentes, derive das headlines da copy.

### ETAPA 3 · Flows da Fase A (pré-launch)

Abandoned cart (`reference/flow-abandoned-cart.md`): puxe os quatro sistemas (curva de decaimento e os dois estilos de sequência, os 5 motivos de abandono cruzados com as objeções do market research, o follow-up de 4 passos do Kennedy, inoculação); 4 emails em 1 hora, 24 horas, 72 horas e 7 dias, com a objeção número 1 quebrada no segundo e desconto só se a margem permite. Post-purchase welcome (`reference/flow-post-purchase.md`): puxe os quatro sistemas (reassurance do Kennedy, re-sell do Collier, zero-party data, janela 30-60-90); 4 emails (obrigado, chegou?, review, cross-sell ou replenishment), com o Email 4 posicionado alguns dias antes de `cohorts.churn_spike_day` quando a curva medida existe (o conteúdo segue a leitura da curva) e no dia 21 a 30 sem ela, tratando o dia 45 como referência de mercado dita ao membro, nunca escrita no doc como número dele. Welcome Email 1 (`reference/flow-welcome.md`) só com welcome offer ou bônus `on_signup`.

### ETAPA 4 · Flows da Fase B (pós-launch, 50 compras ou mais)

Welcome completo (`reference/flow-welcome.md`): puxe os cinco sistemas; emails 2 a 4 (mecanismo, prova social, urgência), com o branch obrigatório do Email 4 (urgência pela expiração real do code; sem code, urgência legítima, nunca deadline inventado). Win-back (`reference/flow-win-back.md`): puxe os cinco sistemas; 3 emails (sentimos sua falta, oferta com code, final call com survey); com cohorts medidos, dispare logo depois de `churn_spike_day` e calibre o incentivo por `crossover_month`; sem eles, 60 dias ou mais. Replenishment (`reference/flow-replenishment.md`): puxe os quatro sistemas; pergunte em quantos dias o produto acaba, dispare o Email 1 de 5 a 7 dias antes, cruze com a segunda compra ideal antes de 65 dias e com a curva medida (a curva vence a memória do membro); o Email 2 obedece `subscription_architecture` (`onetime_plus_sub_no_reorder` é o momento canônico da assinatura, com o framing "você paga mais por não assinar" por `onetime_premium_pct`, nunca `sub_discount_pct`; `subscription_first` filtra assinantes; `no_subscription` oferece o 2-pack). Produto não consumível pula o replenishment.

### ETAPA 5 · Sazonal e OPS pós-launch (Fase B)

Leia `reference/sazonal-e-ops.md`. Campanhas sazonais são da `promo-engine`, que chama esta skill pra gerar os emails; os flows nunca desligam durante a campanha, se adaptam (Desire Calendar pro timing; o checklist de atualização do abandoned cart na janela da promo). Ops como checklist curto no relatório: chargeback abaixo de 1% (toda disputa respondida com evidência, refund proativo, descriptor reconhecível), refund da garantia como macro sem interrogatório (com o Level-2 lembrando de não pedir o bônus de volta) e CS básico (caixa monitorada com resposta em menos de 24 horas úteis e 5 macros).

### ETAPA 6 · Setup pipeline e deliverability

Leia `reference/setup-pipeline.md`. Dois caminhos só: Klaviyo MCP oficial (`mcp__klaviyo__*`), criando os flows da fase ativa com trigger, filtros, ações e HTML, sempre em draft, com `source: "klaviyo_mcp"` e os assets salvos em paralelo; e assets mais setup-guide (fallback silencioso em qualquer falha, default sem MCP e pra todo outro ESP, com a nota de limitações do Shopify Email). Nenhum caminho de session cookie. Nunca ativar automaticamente. Deliverability em cada email: subject abaixo de 50 caracteres, preview de 40 a 70, unsubscribe, from name de pessoa ou marca, reply-to monitorado e o checklist de padrões que derrubam a inbox.

## SALVAR

Leia `reference/salvar-e-regras.md`. `mkdir -p workspace/[produto]/retention-engine/`; por flow, `email-N.html` (HTML de email table-based, sem o design system da Aura e sem passar pelo render) e `flow-metadata.json`; `retention-engine.md` (uma seção por flow com status DRAFT ou ACTIVE) e `retention-engine.html` por `python3 tools/render_report.py workspace/[produto]/retention-engine/retention-engine.md`; `dados.json` com os flows, timestamps, status, `source` e `phase`. Manifest pelo script: `python3 tools/manifest.py <slug> complete retention-engine` na primeira fase concluída e `set retention` com o bloco de contrato (`phase_a_done`, `phase_a_flows`, `phase_b_done`), que a `ad-strategy` lê; `python3 .claude/lib/workspace-index/build_index.py <slug>`. Regras de rigor: nunca ativar sem revisão humana; emails em inglês e relatório no `report_language`; replenishment só com a janela definida; welcome code existindo no Shopify com a mesma expiração; rate limit da API no MCP.

## Mensagem final

Íntegra em `reference/mensagem-final.md`: Fase A com os flows em draft no ESP, o pedido de revisar e ativar antes de ligar a campanha e o próximo passo 'creatives' (Fase B com cerca de 50 compras); Fase B com o flow configurado em draft, o checklist de ops e a volta com os números depois de cerca de 14 dias.
