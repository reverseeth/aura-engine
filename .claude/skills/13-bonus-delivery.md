---
name: bonus-delivery
description: Pipeline técnica de entrega de bônus associados à oferta (digital guides, códigos, acessos a comunidade, trials, produto físico, call 1-on-1, template files, etc). Implementa entrega sem viesar AI pra "PDF bonus" automático — AI deve pensar em formato que realmente agrega ao avatar. Use quando o membro disser "bonus delivery", "como entregar bônus", "setup de entrega", "fulfillment bonus", ou após a skill 04 (offer) definir o stack de valor com bônus.
---

# Bonus Delivery Pipeline

## Premissa crítica

**Bônus NÃO é sempre PDF.** Eco ecommerce AI bota PDF como default porque é fácil de gerar — isso vira bonus commodity que o cliente ignora. Bônus forte é específico pro avatar:

- Template de routine personalizada baseada em concern
- Acesso a comunidade privada (Circle, Discord, Skool)
- Call 30min 1-on-1 com membro do time (se escalável)
- Código de desconto em produto complementar
- Physical freebie dentro da caixa (stickerpack, sample size, card printed)
- Trial extended de subscription
- Workbook interativo (Notion template, Figma file, Google Doc)
- Video series privado (Wistia/Vimeo com password)
- Checklist específica (impressa ou digital)

Essa skill **NÃO decide o formato** — a Skill 04 (offer-builder) decide (ela já tem o contexto de avatar + budget). Essa skill **implementa a entrega** do que foi decidido.

## Pré-flight

- [ ] `04-offer.json` existe com `bonuses[]` preenchido
- [ ] Pra cada bonus em `bonuses[]`, exists `type` claro (NÃO default "pdf")

## Fluxo da Skill

### ETAPA 1 — Parse dos bonuses definidos

Ler `04-offer.json.bonuses[]`. Pra cada bonus:

```json
{
  "id": "bonus-01",
  "name": "nome do bonus",
  "description": "o que é / por que vale",
  "value_anchored": 47,
  "type": "digital_guide|digital_template|physical_freebie|community_access|video_series|consultation_call|discount_code|trial_extension|workbook|checklist",
  "format_hint": "pdf|notion|figma|wistia|in_box|klaviyo_email|shopify_discount|circle_invite|...",
  "delivery_trigger": "post_purchase|on_signup|day_7_post_purchase|on_first_reorder"
}
```

### ETAPA 2 — Per-type delivery playbook

#### `digital_guide` / `digital_template` / `workbook` / `checklist`

- **PDF**: gerar via Markdown → HTML → PDF (weasyprint ou headless Chrome). Output em `/workspace/[produto]/bonuses/[id].pdf`
- **Notion template**: criar template no workspace do membro (se houver Notion API setup), gerar public share link
- **Figma file**: Figma community template + link público
- **Google Docs/Sheets**: criar doc, compartilhar com "anyone with link: view"
- **Delivery**: link no email post-purchase (Klaviyo ou ESP equivalente) + thank-you page

#### `physical_freebie`

- Adicionar SKU do freebie como free line item no order draft (Shopify Admin API ou app como "Free Gift")
- Configurar trigger: "Add to cart when cart subtotal ≥ $X"
- Documentar pro membro: "peça pro fulfillment center incluir X em toda caixa"

#### `community_access`

- Plataforma: Circle / Discord / Skool / Facebook Group privado
- Setup invite link perpétuo (Discord) ou single-use invite (Circle — mais seguro)
- Delivery: link no email post-purchase + PDF one-pager explicando o que tem na comunidade

#### `video_series`

- Hospedar em Wistia/Vimeo Pro com password protection
- Email post-purchase com link + password
- Gated page: criar página Shopify `/pages/your-bonus-videos` com password prompt

#### `consultation_call`

- Calendly / Cal.com link privado (event type) com quota diária (não overwhelm)
- Delivery: link no email post-purchase
- **Importante**: documentar pro membro que isso escala mal — se vender >50 unidades/dia, desligar esse bonus ou cobrar fee simbólico

#### `discount_code`

- Criar code na Shopify Admin (`/admin/discounts/...`) via Admin API
- Code único por customer (use `uniqueCode` tag) OU code compartilhado (mais simples, mas menos controlável)
- Expiração: 30-60 dias pós-purchase tipicamente
- Delivery: email + thank-you page com copy-to-clipboard button

#### `trial_extension`

- Se subscription: extender via Shopify Subscription app
- Se standalone trial: gerar license key único (UUID) com expiração

### ETAPA 3 — Email de entrega (template)

Gerar email que entrega bonus pós-purchase. Template base:

```
Subject: Your [bonus name] is ready 🎁

Hey [First Name],

Thanks for ordering [product]. Here's the bonus you unlocked:

[BONUS NAME] — [value-anchored price]

[Description — 1-2 sentences]

→ Access here: [CTA link or instructions]

If you have questions, just reply to this email.

— [Brand]
```

Compliance:
- Subject < 50 chars
- 1 CTA claro (não múltiplos)
- Reply-to monitorado
- Unsubscribe link

### ETAPA 4 — Tracking

Registrar em `/workspace/[produto]/bonus-delivery-log.json`:

```json
{
  "bonus_id": "bonus-01",
  "type": "community_access",
  "delivery_channel": "klaviyo_email",
  "customer_id": "shopify-customer-id",
  "delivered_at": "ISO",
  "accessed_at": "ISO or null",
  "access_confirmation": "link_clicked|code_redeemed|invite_accepted|not_tracked"
}
```

Métrica crítica: % de customers que REALMENTE acessam o bonus. Se < 30%, bonus não tá agregando valor percebido — revisar na próxima iteração da oferta.

### ETAPA 5 — Integrações obrigatórias

Skill integra com:

- **Shopify Admin API** (criar discount code, add free line item)
- **Klaviyo/ESP** (trigger email post-purchase — usa Skill 12 retention-engine como executor)
- **File hosting** (S3, R2, ou Shopify Files API pra PDFs/digital assets)

## Anti-patterns (FORBIDDEN)

- **Default "free PDF bonus"** sem justificar por que esse avatar quer PDF (geralmente não quer)
- Bonus sem delivery trigger definido (fica em limbo, nunca entregue)
- Discount code sem expiração (vira eternal promo)
- Free physical freebie sem coordenar com fulfillment center (acaba não indo na caixa)
- Community invite link perpétuo em Discord público (vira spam bait)
- Bonus value inflado artificialmente (anchored $97, mas avatar não valoriza isso)

## Regras de rigor

1. **Bonus real** — cada entrega precisa ser tangível e útil. Skill recusa gerar bonus genérico tipo "daily motivation PDF" sem justificar relevância.
2. **Promise↔Config check** — bonus prometido no stack de valor (Skill 04) precisa ter delivery setup completa. Senão, gate bloqueia launch (`.claude/rules/pre-launch-gates.md`).
3. **Access tracking** — sempre que possível, medir se o bonus foi acessado. Bonus nunca acessado é indicador de offer fraca.
4. **Fallback graceful** — se Notion API/Figma API falha, skill gera PDF como último recurso E avisa membro pra manual setup do formato original depois.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Garantir diretório:** `mkdir -p /workspace/[produto]/bonuses/` antes de salvar.

Salvar:

1. **`/workspace/[produto]/bonuses/[bonus-id]/`** — assets do bonus (PDF, scripts, screenshots, templates, etc — formato conforme type do bonus)
2. **`/workspace/[produto]/13-bonus-delivery.md`** — doc operacional pra AI ler em skills futuras: cada bonus com type, delivery channel, trigger, assets path
3. **`/workspace/[produto]/13-bonus-delivery.html`** — visualização humana usando `.claude/templates/aura-report-template.html` como base. Logo SVG Aura no topo (copiar LITERALMENTE de `.claude/templates/aura-logo-snippet.html`). Componentes: `.section-label` por bonus, `.pill` pra type tag, `.kpi-grid` pra access rate (quando disponível).
4. **`/workspace/[produto]/13-bonus-delivery-log.json`** — log running de deliveries + access tracking

**Distinção importante:** os assets do bonus em si (item 1) seguem o design da marca do membro (não do Aura) — PDF do bonus, email HTML, template Notion, etc. Já o relatório interno (itens 2-3) segue rule 6b do CLAUDE.md.

Atualizar `manifest.json.skills_completed` com `"13-bonus-delivery"`.

## Mensagem Final

"Pipeline de entrega setupada pros [N] bônus da oferta:

1. [Bonus 1 — tipo — canal de entrega]
2. [Bonus 2 — tipo — canal de entrega]

Testa comprando 1 unidade pra validar que os emails/links/códigos tão chegando. Depois de 30 dias com dados, roda `bonus metrics` pra ver access rate por bonus e iterar."
