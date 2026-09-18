# Bonus Delivery · Referência: Email de entrega, a integração com a retention-engine (ETAPA 3)

> A divisão de papéis (a retention-engine é o único executor de email), o mapa de `delivery_trigger` pro email que entrega, o timing entre as Fases A e o template base do email em inglês. Abra na ETAPA 3.

### ETAPA 3 — Email de entrega (integra com Skill `retention-engine`)

**Divisão de papéis (fonte única de verdade):** a `bonus-delivery` **gera o ASSET do bônus** (PDF, link, config GWP) e define o `delivery_trigger`. A **Skill `retention-engine` é o ÚNICO executor de email** (Klaviyo/ESP) — ela monta o flow e entrega. A `bonus-delivery` **não dispara email sozinha nem duplica lógica de email**: produz o **conteúdo do email + o trigger** como um payload que a `retention-engine` consome. Toda a mecânica de flow (trigger técnico, delays, draft/ativação, HTML do email no ESP) mora na `retention-engine`. Ver a tabela "Divisão de papéis pós-compra" na Skill `retention-engine`.

Mapear `delivery_trigger` → fluxo da `retention-engine` (espelho literal da tabela "delivery_trigger → email que entrega" da Skill `retention-engine`, que é a fonte única):

| `delivery_trigger` | Fluxo / email que entrega o bonus (Skill `retention-engine`) |
|---|---|
| `post_purchase` | Post-Purchase Welcome — Email 1 (obrigado) |
| `day_7_post_purchase` | Post-Purchase Welcome — Email 3 (~dia 7) |
| `on_first_reorder` | Replenishment — Email 2/3 (no reorder) |
| `on_signup` | Welcome Series — Email 1 (boas-vindas) |

(Win-back é OUTRO flow na `retention-engine` — reativação de cliente inativo, não entrega de bônus. Nenhum `delivery_trigger` mapeia pra ele.)

GWP físico e gift-wrapping geralmente **não precisam de email de entrega** (vão na caixa). E-book, discount_code, community e digital precisam.

**Timing (Fase A vs Fase B):** o payload (template abaixo + trigger) é produzido na **Fase A da `bonus-delivery`**, antes do go-live — e a **Fase A da `retention-engine` roda logo em seguida na ordem canônica** (flows de recuperação pré-launch), montando o flow post-purchase que carrega este email já com o `{{BONUS_LINK}}` preenchido. O link na thank-you page / order status (config da Fase A) segue como rede de segurança: garante o acesso do comprador do dia 1 mesmo se o membro ainda não ativou o flow no ESP.

Template base do email (gerado em inglês, repassado pra `retention-engine`):

```
Subject: Your [bonus name] is ready

Hey [First Name],

Thanks for ordering [product]. Here's the bonus you unlocked:

[BONUS NAME] (a [value-anchored] value)

[Description — 1-2 sentences toward the dream outcome]

Access it here: [CTA link or instructions]

Questions? Just reply to this email.

— [Brand]
```

Formato do email: subject < 50 chars, 1 CTA só, reply-to monitorado, unsubscribe link. Sem emoji no subject (consistência com o tom da marca; opcional, decisão do membro).
