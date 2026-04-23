---
name: retention-engine
description: Setup automático de fluxos de retenção/lifecycle email via ESP (Klaviyo primário, Omnisend/MailerLite secundários). Gera sequências (welcome, abandoned-cart, post-purchase, win-back, replenishment) via internal API reverse-engineered quando public API não expõe a funcionalidade. Use quando o membro disser "retention", "email flows", "automation", "lifecycle", "Klaviyo", ou após launch da primeira campanha de ads com tráfego rodando.
---

# Retention Engine

## Quando Usar

Depois que a campanha de ads está rodando e o membro tem tráfego chegando (≥ 50 compras no ESP). Sem dados mínimos, não há o que segmentar — retenção prematura vira noise.

## Pré-flight

- [ ] `/workspace/[produto]/manifest.json` com `08-ad-strategy` em `skills_completed`
- [ ] ESP identificado no `profile.md` (`esp: "klaviyo" | "omnisend" | "mailerlite" | "none"`)
- [ ] Se ESP = "none" → PARAR e recomendar Klaviyo (free tier até 250 contatos + Shopify integration nativa)
- [ ] `04-offer.md` carregado (pra saber reorder rate, guarantee period, bonuses entregáveis)
- [ ] `02-market-research.md` carregado (objeções = hooks de win-back; dores = hooks de abandoned cart)

## Fluxos base (templates — adaptam ao produto)

### 1. Welcome Series (novo subscriber, sem compra ainda)

- Email 1 (imediato): boas-vindas + reforço do motivo do opt-in + code do welcome offer (se houver)
- Email 2 (dia 2): educação sobre o mecanismo único (do `04-offer.md`) + soft CTA
- Email 3 (dia 4): social proof stack + trust reinforcement
- Email 4 (dia 7): urgency layer (expiração do welcome code) + hard CTA

### 2. Abandoned Cart (viewed product, added to cart, didn't checkout)

- Email 1 (1h após abandon): "Esqueceu de algo?" + produto no cart + 1 benefício-chave
- Email 2 (24h): objeção quebrada (escolher objeção #1 do market research) + testimonial
- Email 3 (72h): urgência (stock/time) + discount code se margem permite
- Email 4 (7d, opcional): "last call" + reforço de garantia

### 3. Post-Purchase Welcome (comprou pela primeira vez)

- Email 1 (30min pós-purchase): obrigado + unboxing tips + delivery ETA
- Email 2 (dia da entrega estimada): "chegou?" + how-to-use tutorial
- Email 3 (dia 7-10): request review (com incentivo)
- Email 4 (dia 21-30): cross-sell ou replenishment trigger (se consumível)

### 4. Win-Back (60+ dias sem purchase, subscriber ativo)

- Email 1: "sentimos sua falta" + novidade do produto
- Email 2 (7 dias depois): oferta especial com código de win-back
- Email 3 (14 dias depois): final call + feedback survey pra entender porque churn

### 5. Replenishment (consumíveis — trigger baseado em reorder rate)

- Email 1 (dias antes do acabar): "seu [produto] tá acabando — reorder aqui"
- Email 2: subscription option com desconto
- Email 3 (pós-acabar): "hora de reabastecer"

## Setup Pipeline — Klaviyo

Klaviyo tem public API (`https://a.klaviyo.com/api/...`) que cobre list management + profile updates + events + campaigns. **Mas** flow creation/configuration é exposto apenas via internal API (UI-facing endpoints). Skill usa esses endpoints pro setup automático.

### Endpoints internal usados (reverse-engineered)

⚠️ Esses endpoints NÃO são oficialmente documentados — podem mudar. Skill testa com head request antes de usar.

```
POST /ajax/flows/create              → cria flow vazio
POST /ajax/flow/{id}/configure       → define trigger + filters
POST /ajax/flow/path/{pid}/action/add → adiciona action (email, delay, branch)
POST /ajax/flow/action/{aid}/timing  → configura delay/time
POST /ajax/flow/message/{mid}/content → define subject + preview + content
POST /ajax/email-editor/{tid}/html   → substitui HTML do template
POST /ajax/flow/action/{aid}/status  → ativa/desativa action
```

### Auth via session cookie

Internal API usa session cookie do Klaviyo (login no dashboard). Pedir ao membro:

1. Login no Klaviyo (https://www.klaviyo.com)
2. DevTools → Application → Cookies → copiar valor de `_klaviyo_session`
3. Paste no prompt da skill (salvar em `.env.local` dentro do `/workspace/[produto]/` — gitignored)
4. Cookie tem validade de ~7 dias; re-pedir se expirado

### Fluxo de execução

1. Skill pergunta: "Qual fluxo configurar primeiro?" (lista 5 templates acima)
2. Membro escolhe
3. Skill gera HTML de cada email adaptando ao produto (usa `05-copy.md` como base de copy + `02-market-research.md` pra VOC + `04-offer.md` pra mecanismo)
4. Skill chama `/ajax/flows/create` → obtém `flow_id`
5. Skill configura trigger apropriado (`/ajax/flow/{id}/configure`)
6. Pra cada email do fluxo:
   - `/ajax/flow/path/{pid}/action/add` com type=email
   - `/ajax/flow/action/{aid}/timing` com delay
   - `/ajax/flow/message/{mid}/content` com subject + preview
   - `/ajax/email-editor/{tid}/html` com HTML final
7. Fluxo inicia em draft (não ativa automaticamente)
8. Skill notifica membro: "Flow X criado em DRAFT no Klaviyo. Abre o dashboard, revisa os emails, e ativa quando tiver OK."

### NUNCA ativar automaticamente

Ativar flow via skill = risco de spam se algum email tiver bug. Skill SEMPRE deixa em draft. Membro revisa no Klaviyo UI antes de ativar.

## Fallback pra ESPs sem internal API acessível

Se ESP = Omnisend/MailerLite/outro que não expõe flow internal API, skill gera:

1. `/workspace/[produto]/12-retention/[fluxo]/email-1.html`, `email-2.html`, etc (HTML pronto)
2. `/workspace/[produto]/12-retention/[fluxo]/setup-guide.md` com step-by-step manual no dashboard do ESP

Membro faz setup manual, skill entrega os materiais prontos.

## Compliance & deliverability

Pra cada email gerado:

- **Subject line**: < 50 chars ideal; sem ALL CAPS; sem emoji excessivo
- **Preview text**: 40-70 chars
- **Unsubscribe link**: obrigatório no footer (CAN-SPAM + GDPR)
- **From name**: "[Brand Name]" — não email genérico tipo "noreply@"
- **Reply-to**: endereço monitorado (replies de cliente vão pra algum lugar)
- **Spam trigger words check**: rodar `compliance-preflight` no subject + body. Palavras tipo "FREE!!!", "ACT NOW", "GUARANTEED" no subject reduzem inbox rate

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p /workspace/[produto]/12-retention/` antes de salvar.

Salvar:

1. **`/workspace/[produto]/12-retention/[fluxo]/email-N.html`** — HTML pronto de cada email do fluxo (consumidor final; responsive table-based email HTML, NÃO o design-system Aura)
2. **`/workspace/[produto]/12-retention/[fluxo]/flow-metadata.json`** — metadata de cada email (subject, preview, trigger, delay)
3. **`/workspace/[produto]/12-retention.md`** — relatório operacional do setup pra AI ler em skills futuras (resumo dos fluxos criados, triggers, status)
4. **`/workspace/[produto]/12-retention.html`** — visualização humana (AI report) usando `.claude/templates/aura-report-template.html` como base. Logo SVG do Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html`). Componentes: `.section-label` por fluxo, `.pill` pra status (DRAFT/ACTIVE), `.callout` pra avisos de compliance.
5. **`/workspace/[produto]/12-retention-log.json`** — log de flows criados + timestamps + status + delivery results

**Distinção importante:** os emails em si (item 1) são HTML de email marketing (table-based, inline styles pra ESP compatibility) — NÃO usam o design-system Aura, NÃO têm logo Aura. Já os relatórios internos (itens 3-4) seguem a rule 6b do CLAUDE.md normalmente.

Atualizar `manifest.json.skills_completed` com `"12-retention-engine"`.

## Regras de rigor

1. **NUNCA ativar flow sem revisão humana** — risco de spam em escala
2. **NUNCA enviar emails em português pra mercado US** (e vice-versa) — flag language no `profile.md`
3. **Replenishment trigger requer reorder rate estimada** — se o produto é one-time (não consumível), pular Fluxo 5
4. **Welcome offer code precisa existir** — cross-check com Promise↔Config gate antes de enviar
5. **Rate limit**: Klaviyo internal API tem limite não-documentado — spacing 500ms entre requests pra não derrubar

## Mensagem Final

"Fluxo [X] configurado no [ESP] em DRAFT. [N] emails gerados. Próximos passos:

1. Abre o dashboard do [ESP]
2. Revisa cada email (subject + preview + body)
3. Ativa o flow quando estiver OK

Depois que o flow rodar por 14 dias com dados, diz `retention metrics` pra analisar open rate / CTR / revenue attribution."
