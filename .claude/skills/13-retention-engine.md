---
name: retention-engine
description: Setup automático de fluxos de retenção/lifecycle email via ESP (Klaviyo primário, Omnisend/MailerLite secundários). Gera sequências (welcome, abandoned-cart, post-purchase, win-back, replenishment) e cria os flows via Klaviyo MCP oficial quando disponível, com fallback pra assets HTML + setup-guide que o membro importa. Use quando o membro disser "retention", "email flows", "automation", "lifecycle", "Klaviyo", ou após launch da primeira campanha de ads com tráfego rodando.
---

# Retention Engine

## Quando Usar

Depois que a campanha de ads está rodando e o membro tem tráfego chegando (≥ 50 compras no ESP). Sem dados mínimos, não há o que segmentar — retenção prematura vira noise.

## Base de conhecimento (NUNCA query genérica)

Esta skill puxa SISTEMAS NOMEADOS de email lifecycle e psicologia de persuasão da base — não query genérica tipo "email flows" ou "abandoned cart". Em cada ETAPA/fluxo abaixo, rode `search_knowledge` com a `best_query` exata de cada framework relevante listado ali (deep=true), puxando o sistema completo (ex: a curva de decaimento de abandoned cart com os 5 motivos de abandono, não "dicas de cart recovery"). **Índice completo dos frameworks desta skill (domínios `retention-email` + `persuasion-psychology`): `.claude/lib/kb-index/` — `frameworks.json` (machine-readable) e `README.md` (mapa skill→domínio).** Os frameworks de maior impacto estão embutidos direto nos fluxos onde são usados; o resto do catálogo do domínio fica disponível no índice.

## Pré-flight

**Idioma (report_language).** Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). Todo output interno (`13-retention-engine/relatorio.md`/`.html`, `flow-metadata.json` descritivo, mensagens e perguntas ao membro) usa esse idioma. **A copy dos emails em si (subject, preview, body, CTA) permanece SEMPRE em inglês US**, independente do report_language — é consumidor-final do mercado US.

### Gate de consistência (Skill 09)
Antes das checagens abaixo, ler `workspace/[produto]/09-consistency-audit/dados.json` se existir:
- Se `launch_recommendation == "BLOCK"` → os fluxos de email vão herdar o drift detectado (mecanismo divergente, VOC sem rastreio, oferta diferente da página) e propagar inconsistência pra base de subscribers. Oferecer ≥2 caminhos: **(A)** rodar a skill 09 agora pra corrigir o drift, OU **(B)** prosseguir mesmo assim marcando `manifest.skipped_preflight += ["09-consistency-audit"]` e avisando no output final que recomenda re-executar após corrigir.
- Se `CAUTION` → exibir warnings e pedir OK do membro antes de gerar fluxos.
- Se `GO` ou arquivo não existe → prosseguir.

- [ ] `workspace/[produto]/manifest.json` com `10-ad-strategy` em `skills_completed`
- [ ] **ESP identificado.** Ler `manifest.esp` (e `profile.md` → `esp: "klaviyo" | "omnisend" | "mailerlite" | "none"`). Se o campo estiver **ausente** (membro nunca rodou setup completo), PERGUNTAR inline ao membro qual ESP ele usa e gravar a resposta em `manifest.esp`. Se `esp: "none"` (membro não tem ESP), **não abortar** — recomendar Klaviyo (free tier até 250 contatos + Shopify integration nativa), e se o membro topar, gravar `manifest.esp = "klaviyo"` e seguir; se ele preferir decidir depois, gerar os fluxos no fallback HTML + setup-guide (seção abaixo) pra ele importar quando escolher.
- [ ] `04-offer-builder/relatorio.md` + `04-offer-builder/dados.json` carregados (pra saber a janela de reorder, guarantee period, e os `bonuses[]` com seus `delivery_trigger`)
- [ ] `02-market-research/relatorio.md` carregado (objeções = hooks de win-back; dores = hooks de abandoned cart)

## TrendTrack MCP (opcional, se conectado)

Se há tools com prefixo `mcp__trendtrack__` disponíveis:

- **`mcp__trendtrack__analyze_shop_emails`** com domínio de 1-3 concorrentes do `03-competitor-analysis/relatorio.md` → retorna padrões reais de cadência, subject lines e content categories da concorrência. Use como referência (não copy-paste) pra calibrar timing dos fluxos abaixo (welcome series, abandoned cart, post-purchase) com benchmark de mercado.

Se TrendTrack NÃO estiver disponível, segue templates abaixo direto, baseados em VOC + offer.

## Divisão de papéis pós-compra (05 / 13 / 14) — fonte única de verdade

Três skills tocam o pós-compra. Pra não duplicar nem sobrescrever, cada artefato tem UM dono:

| Artefato | Quem PRODUZ | Quem ENTREGA | Nota |
|---|---|---|---|
| Asset do bônus (PDF/e-book, config GWP, link) | **Skill 05** | — | A 05 gera o asset e define o `delivery_trigger`. Não monta email. |
| **Email de entrega de bônus** | **Skill 13** (este) | **Skill 13** | A 13 é o ÚNICO executor de email. A 05 fornece conteúdo + trigger; a 13 monta o flow e injeta o `{{BONUS_LINK}}`. Nunca duplicar lógica de email na 05. |
| Flows de lifecycle (welcome, abandoned-cart, post-purchase, win-back, replenishment) | **Skill 13** | **Skill 13** | Fonte única dos flows de retenção. |
| Email-sequence derivada do winner (recycler) | **Skill 14** | Membro (importa manual) | É **variação A/B de nutrição** derivada do criativo winner, NÃO um flow de lifecycle. Não colide nem sobrescreve o welcome/post-purchase da 13 — entra como flow separado/teste paralelo. Ver nota na Skill 14. |

Regra prática: se é email que dispara por evento de ciclo de vida (signup, cart, compra, inatividade, reorder) → é flow da 13. Se é peça de nutrição reaproveitada de um winner pra testar contra o que já roda → é a 14, e o membro decide onde plugar sem desligar os flows da 13.

## Conexão com bonuses da oferta (Skill 04)

Antes de gerar os fluxos, ler `04-offer-builder/dados.json.bonuses[]` e casar o `delivery_trigger` de cada bonus com o email do fluxo que entrega:

| `delivery_trigger` | Fluxo / email que entrega o bonus |
|--------------------|-----------------------------------|
| `on_signup` | Welcome Series — Email 1 (boas-vindas) |
| `post_purchase` | Post-Purchase Welcome — Email 1 (obrigado) |
| `day_7` | Post-Purchase Welcome — Email 3 (~dia 7) |
| `on_first_reorder` | Replenishment — Email 2/3 (no reorder) |

Incluir o asset/link do bonus (PDF, Circle invite, código de acesso — produzidos na Skill 05) no corpo do email correspondente. Se a Skill 05 ainda não gerou o asset, deixar placeholder `{{BONUS_LINK}}` no HTML e avisar no output final que o link precisa ser colado antes de ativar.

## Fluxos base (templates — adaptam ao produto)

**Frameworks de governança que valem pra TODOS os fluxos** (puxe uma vez, aplique em todos):
- **The Rule of 1** — cada email tem UM objetivo, UM job por elemento, UM leitor; escrever o CTA primeiro (rode `Rule of 1 email one goal one job per element one reader write CTA first`)
- **3-to-1 Value-to-Sales Rule** — equilíbrio de cadência entre emails de valor e de venda, pra não queimar a lista (rode `3 to 1 rule value emails sales email balance newsletter cadence`)
- **Email/SMS Coordination Rule (echo, don't collide)** — se o membro também roda SMS, escalonar (email primeiro, SMS follow-up pra não-openers), nunca colidir (rode `email SMS coordination echo not collide send email first SMS follow up non-openers staggered cadence`)
- **Drayton Bird's Email = Direct Mail Principle** — tratar cada email como carta de uma pessoa real, subject = headline, copy longa quando o argumento exige (rode `Drayton Bird email direct mail principle long copy real person subject line headline`)


### 1. Welcome Series (novo subscriber, sem compra ainda)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **5-Step Welcome Sequence Process** — welcome = lead-nurturing, não "bem-vindo" genérico (rode `welcome sequence lead nurturing 5 step process VOC research plan automate not a template`)
- **DotCom Secrets' Soap Opera Sequence** — 5-email bonding (set the stage → high drama → epiphany → hidden benefits → urgency) pra estruturar o arco da série (rode `DotCom Secrets soap opera sequence 5 email set the stage high drama epiphany hidden benefits urgency`)
- **Expert Secrets' Email Epiphany Funnels** — quebrar as 3 false beliefs (vehicle / internal / external) ao longo dos emails 2-3 (rode `Expert Secrets email epiphany funnels vehicle internal external false belief epiphany bridge`)
- **From-Name as Inbox Filter** — definir o From name como pessoa real, não brand genérica, pra deliverability (rode `From name inbox filter mobile Gmail gatekeeper real person test from line deliverability`)
- **Restock / Testimonial / Anniversary Coupon Welcome Beats** — batidas de ecommerce pra calibrar o conteúdo de cada email (rode `ecommerce welcome series restock coupon testimonial week 5 anniversary coupon weekly post-purchase beats`)

- Email 1 (imediato): boas-vindas + reforço do motivo do opt-in + code do welcome offer (se houver)
- Email 2 (dia 2): educação sobre o mecanismo único (do `04-offer-builder/relatorio.md`) + soft CTA
- Email 3 (dia 4): social proof stack + trust reinforcement
- Email 4 (dia 7): urgency layer (expiração do welcome code) + hard CTA

### 2. Abandoned Cart (viewed product, added to cart, didn't checkout)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Abandoned-Cart Decay Curve + Two Sequence Styles** — quando disparar (curva de decaimento, Baymard 69.8%) e escolher entre estilo Discount-focused vs Emotion-focused conforme margem (rode `abandoned cart decay curve Baymard 69.8% discount-focused emotion-focused sequence escalating discount day 0 6 hours`)
- **5 Reasons People Abandon (objection map)** — mapear o motivo real de abandono pra Email 2 (preço / urgência / experiência negativa / info incompleta / ceticismo), cruzando com objeções do `02-market-research/relatorio.md` (rode `five reasons people abandon cart price urgency negative experience incomplete information skepticism objection map`)
- **Kennedy's 4-Step Follow-Up Campaign** — Re-state / Second Notice / Final Notice / Change Offer pra estruturar a escalada dos 4 emails (rode `Kennedy 4-step follow-up campaign re-state second notice final notice change offer No BS Direct Marketing`)
- **Inoculation Theory** — pré-armar a objeção #1 antes que o cliente a verbalize (rode `inoculation theory McGuire weakened attack pre-emptive defense competitor argument resistance`)

- Email 1 (1h após abandon): "Esqueceu de algo?" + produto no cart + 1 benefício-chave
- Email 2 (24h): objeção quebrada (escolher objeção #1 do market research) + testimonial
- Email 3 (72h): urgência (stock/time) + discount code se margem permite
- Email 4 (7d, opcional): "last call" + reforço de garantia

### 3. Post-Purchase Welcome (comprou pela primeira vez)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Kennedy's Post-Purchase Reassurance Letter** — pós-compra como profit center: matar buyer's remorse no Email 1 (rode `Kennedy post-purchase reassurance letter buyer remorse profit center order confirmation`)
- **Collier's Re-Sell After Shipment (Acknowledgment Letter)** — revender o que já foi comprado, reduzir returns, construir antecipação até a entrega (rode `Collier re-sell after shipment acknowledgment letter reduce returns build anticipation testimonial`)
- **Zero-Party Data Moat** — usar o Email 2/3 pra coletar dado de preferência (post-purchase survey/quiz) que alimenta personalização futura (rode `zero-party data moat post-purchase survey onboarding quiz preference center unreplicable personalization`)
- **30-60-90 Day LTV Email+SMS Flow Hacks** — janela da segunda compra; estruturar os emails 3-4 pra cair dentro dela (rode `30-60-90 day LTV email SMS flow hacks second purchase window zero-party data force multiplier`)

- Email 1 (30min pós-purchase): obrigado + unboxing tips + delivery ETA
- Email 2 (dia da entrega estimada): "chegou?" + how-to-use tutorial
- Email 3 (dia 7-10): request review (com incentivo)
- Email 4 (dia 21-30): cross-sell ou replenishment trigger (se consumível)

### 4. Win-Back (60+ dias sem purchase, subscriber ativo)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Hormozi's 9-Word Email** — reativação curta ("are you still interested in [resultado]?") como abertura mais barata e de maior reply (rode `Hormozi 9-word email are you still interested reactivation dormant leads $100M Leads`)
- **Kennedy's Collection Agency Model** — escalada de urgência em intervalos com mudança de formato a cada email (rode `Kennedy collection agency model multi-step mailing format change urgency intervals`)
- **Collier's Ruffle-Smooth-Ruffle** — alternar tom emocional (tensão → alívio → tensão) pra furar a habituação de quem ignora (rode `Collier ruffle smooth ruffle alternating emotional tone collection series habituation`)
- **Engagement Suppression / Sunset & Double-Opt-In Re-engagement** — definir o ponto de corte: quem não reativar vai pra sunset/suppression pra proteger deliverability (rode `engagement suppression sunset re-engagement double opt-in unsubscribe non-engaged deliverability 30 day`)

- Email 1: "sentimos sua falta" + novidade do produto
- Email 2 (7 dias depois): oferta especial com código de win-back
- Email 3 (14 dias depois): final call + feedback survey pra entender porque churn

### 5. Replenishment (consumíveis — trigger baseado na janela de reorder)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Day Zero Triggered-Email Method** — replenishment é behavior-triggered mini-funnel (dispara pelo timing real de consumo), não drip por tempo fixo (rode `Day Zero behavior-triggered email mini-funnel outperforms time-based drip cap day 4 Copy School`)
- **Fibonacci Drip-Cadence Sequence** — espaçamento dos nudges antes/depois do produto acabar (day 0/1/2/3/5/8) (rode `Fibonacci sequence drip campaign email cadence day 0 1 2 3 5 8 spacing Copyhackers`)
- **Door-Closing Aversion** — enquadrar a janela de reorder como opção que expira (subscription/2-pack antes de acabar o estoque dele) (rode `door-closing aversion loss of options Shin Ariely expires midnight only 3 spots disappearing bonus`)

A janela de reorder não vem pronta do `04-offer-builder/dados.json` (ele não produz um `reorder_rate` legível por máquina). Defina a fonte assim, antes de configurar o fluxo:

1. PERGUNTAR ao membro: "Em quantos dias um cliente típico **acaba** uma unidade do produto?" (ex: um sérum de 30ml dura ~30 dias).
2. Calcular o timing dos emails a partir disso: Email 1 dispara ~5-7 dias **antes** do produto acabar (ex: produto dura 30 dias → Email 1 no dia 23-25 pós-compra), Email 2 perto do fim, Email 3 logo após o fim estimado.
3. Cruzar com benchmark: a 2ª compra ideal cai **antes de 65 dias** pós-primeira-compra. Se a duração informada empurrar o reorder pra além disso, antecipar o nudge (oferecer subscription/2-pack) pra não perder a janela.

- Email 1 (~5-7 dias antes do acabar): "seu [produto] tá acabando — reorder aqui"
- Email 2 (perto do fim): subscription option com desconto
- Email 3 (pós-acabar): "hora de reabastecer"

## Setup Pipeline — Klaviyo

Cascade resiliente (detecção de prefixo conforme `.claude/lib/mcp-detect/README.md`), **dois caminhos só**: **Klaviyo MCP oficial → HTML + setup-guide**. Não há caminho de session-cookie/internal-API — foi removido por risco de segurança (cookie dava acesso full à conta) e fragilidade (endpoints sem contrato público). Automação confiável = MCP oficial; sem MCP, fallback é assets + guia que o membro importa.

### Caminho 1 (PREFERENCIAL) — Klaviyo MCP oficial

Detecte se há tools com prefixo `mcp__klaviyo__` na sessão (Klaviyo MCP oficial, 25 tools, 2026):

```
klaviyo_mcp_available = existe ao menos 1 tool com prefixo `mcp__klaviyo__` na sessão
```

Se **disponível**, CRIE os flows direto via MCP (com contrato estável, sem scraping):

1. Gerar o HTML de cada email adaptando ao produto (usa `06-copy-engine/relatorio.md` pra copy + `02-market-research/relatorio.md` pra VOC + `04-offer-builder/relatorio.md` pra mecanismo), mesma geração do caminho de assets.
2. Criar cada flow (welcome series, abandoned-cart, post-purchase, win-back, replenishment) via as tools `mcp__klaviyo__*` de flow creation/configuration: trigger, filtros, ações (email/delay/branch), subject + preview + conteúdo HTML.
3. **Flows criados SEMPRE em draft/manual** — nunca ativar automaticamente (regra "NUNCA ativar automaticamente" abaixo vale igual aqui: risco de spam se um email tiver bug). Membro revisa no Klaviyo UI e ativa.
4. Logar `source: "klaviyo_mcp"` no `13-retention-engine/dados.json` e no `automation-log.jsonl`.
5. Salvar os assets (HTML + flow-metadata.json) em paralelo, pra o membro ter material mesmo que queira ajustar fora do MCP.

Se uma chamada MCP falhar (auth, rate limit, tool indisponível), cair silenciosamente pro **Caminho 2** sem insistir — o membro vê os fluxos prontos pra importar do mesmo jeito.

### Caminho 2 (FALLBACK confiável) — assets + setup-guide

Gerar os assets prontos + setup-guide e o membro importa no Klaviyo UI. Veja a seção "Caminho 2 detalhado — assets + setup-guide" abaixo. Default quando não há Klaviyo MCP. Logar `source: "klaviyo_assets_guide"`. Vale também pra Omnisend/MailerLite/outros ESPs (que não têm MCP).

### NUNCA ativar automaticamente (vale pros dois caminhos)

Ativar flow via skill — por MCP ou de qualquer outra forma — = risco de spam se algum email tiver bug. Skill SEMPRE deixa em draft/manual. Membro revisa no UI do ESP antes de ativar.

## Caminho 2 detalhado — assets + setup-guide (todos os ESPs)

Este é o caminho confiável e o fallback da skill quando não há MCP — vale pra Klaviyo e pra Omnisend/MailerLite/outros. Skill gera:

1. `workspace/[produto]/13-retention-engine/[fluxo]/email-1.html`, `email-2.html`, etc (HTML pronto)
2. `workspace/[produto]/13-retention-engine/[fluxo]/setup-guide.md` com step-by-step manual no dashboard do ESP (trigger, delays, subject/preview de cada email, onde colar o HTML)

Membro faz o setup manual seguindo o guia, skill entrega os materiais prontos.

## Compliance & deliverability

Pra cada email gerado:

- **Subject line**: < 50 chars ideal; sem ALL CAPS; sem emoji excessivo
- **Preview text**: 40-70 chars
- **Unsubscribe link**: obrigatório no footer (CAN-SPAM + GDPR)
- **From name**: "[Brand Name]" — não email genérico tipo "noreply@"
- **Reply-to**: endereço monitorado (replies de cliente vão pra algum lugar)
- **Spam trigger words check**: rodar `compliance-preflight` no subject + body. Palavras tipo "FREE!!!", "ACT NOW", "GUARANTEED" no subject reduzem inbox rate

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p workspace/[produto]/13-retention-engine/` antes de salvar.

Salvar:

1. **`workspace/[produto]/13-retention-engine/[fluxo]/email-N.html`** — HTML pronto de cada email do fluxo (consumidor final; responsive table-based email HTML, NÃO o design-system Aura)
2. **`workspace/[produto]/13-retention-engine/[fluxo]/flow-metadata.json`** — metadata de cada email (subject, preview, trigger, delay)
3. **`workspace/[produto]/13-retention-engine/relatorio.md`** — relatório operacional do setup pra AI ler em skills futuras (resumo dos fluxos criados, triggers, status)
4. **`workspace/[produto]/13-retention-engine/relatorio.html`** — visualização humana (AI report) usando `.claude/templates/aura-report-template.html` como base. Logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html`). Componentes: `.section-label` por fluxo, `.pill` pra status (DRAFT/ACTIVE), `.callout` pra avisos de compliance.
5. **`workspace/[produto]/13-retention-engine/dados.json`** — log de flows criados + timestamps + status + delivery results

**Distinção importante:** os emails em si (item 1) são HTML de email marketing (table-based, inline styles pra ESP compatibility) — NÃO usam o design-system Aura, NÃO têm logo Aura. Já os relatórios internos (itens 3-4) seguem a rule 6b do CLAUDE.md normalmente.

Atualizar `manifest.json.skills_completed` com `"13-retention-engine"`.

- Regenera o painel do produto: `python3 .claude/lib/workspace-index/build_index.py <slug>` (atualiza ABRIR-AQUI.html), onde `<slug>` é o `product_slug`.

## Regras de rigor

1. **NUNCA ativar flow sem revisão humana** — risco de spam em escala
2. **Dois idiomas, dois papéis.** A copy dos emails (subject, preview, body, CTA) é consumidor-final do mercado US e fica SEMPRE em **inglês**, independente do `report_language`. Já o relatório interno (`13-retention-engine/relatorio.md`/`.html`), o setup-guide e a conversa com o membro seguem o `report_language` do `profile.md` (default `pt-BR`). Nunca misturar: nunca email em português, nunca relatório interno forçado em inglês quando o membro escolheu pt-BR.
3. **Replenishment requer a janela de reorder definida** — perguntar ao membro em quantos dias o produto acaba (ver Fluxo 5). Se o produto é one-time (não consumível), pular Fluxo 5.
4. **Welcome offer code precisa existir** — cross-check com Promise↔Config gate antes de enviar
5. **Rate limit**: ao criar flows via Klaviyo MCP oficial, respeitar o rate limit da API pública (spacing entre chamadas; ao receber 429, backoff conforme ES6). No fallback (assets + guide) não há chamada de API, então não se aplica.

## Mensagem Final

"Fluxo [X] configurado no [ESP] em DRAFT. [N] emails gerados. Próximos passos:

1. Abre o dashboard do [ESP]
2. Revisa cada email (subject + preview + body)
3. Ativa o flow quando estiver OK

Depois que o flow rodar por ~14 dias, acompanha open rate / CTR / receita por fluxo direto no dashboard do [ESP] (Klaviyo → Analytics → Flows; Omnisend/MailerLite → relatório de automação). Me chama de volta com esses números (ou um screenshot) que eu analiso o que tá performando e onde ajustar."
