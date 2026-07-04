---
name: pre-launch-gates
description: Gates automáticos inegociáveis antes de qualquer launch (página deploy ou ads go-live). Dois gates principais — Compliance (ad-flag words) e Promise↔Config (copy promete X, loja precisa entregar X).
paths:
  - .claude/skills/06-copy-engine.md
  - .claude/skills/07b-page-build.md
  - .claude/skills/07d-checkout-aov.md
  - .claude/skills/08-creative-engine.md
  - .claude/skills/10-ad-strategy.md
---

# Pre-launch Gates (NON-NEGOTIABLE)

Dois gates BLOQUEIAM qualquer deploy de página ou go-live de ad. Gate não é warning — é gate. Status FAIL = operação não prossegue.

## GATE 1 — Ad-flag Compliance (automático, blocking)

### Onde aplica

- **Skill 06** (copy-engine) — ANTES de salvar qualquer peça final de copy
- **Skill 07b** (page-build) — ANTES de compilar Liquid com copy injetada E ANTES do push pra Shopify
- **Skill 08** (creative-engine) — ANTES de finalizar briefing (já existe Etapa 7.5)
- **Skill 10** (ad-strategy) — ANTES de entregar instrução "colar no Ads Manager"

### Como invocar (interface canônica — usar EXATAMENTE esta)

**Skills 07b e 10 (gates mecânicos de deploy/go-live) DEVEM rodar a CLI canônica:**

```bash
python3 .claude/lib/compliance-preflight/run.py --file <path> [--vertical <enum do manifest-schema>] [--stage pre_ad|pre_page] --json
```

Alternativa pra texto solto (sem arquivo): `--text "<string>"` no lugar de `--file`.

**Skills 06 e 08 (e 14)** rodam o gate pelo passe Claude da MESMA lib (`checker.md` + `red_flags.json` — avaliação com nuance peça a peça), que retorna JSON conforme o MESMO `output-schema.json`. Os dois passes são intercambiáveis no formato do output; a decisão de gate abaixo vale igual pros dois (ver `.claude/lib/compliance-preflight/README.md`, "Onde é invocado").

O output é JSON conforme `output-schema.json`, SEMPRE incluindo `overall_verdict` (`pass|warning|critical`) e `rewrite_suggestions[]` (uma por flag encontrada). Na CLI (`run.py`), o matching é por word-boundary, case-insensitive — nunca substring pura ("secure" não casa "cure").

### Decisão de gate

Parse do JSON output, decisão pelo `overall_verdict`:

| `overall_verdict` | Ação |
|-------------------|------|
| `critical` | **BLOCK** — não salva, não publica, não faz deploy. Apresenta ao membro as flags com suas `rewrite_suggestions[]` e pede revisão manual |
| `warning` | **BLOCK por default**. Aplicar as `rewrite_suggestions[]` automáticas e **re-rodar o compliance check** no texto rewriteado. Se o rewrite passar (`pass`), prosseguir. Se continuar `warning`/`critical`, salvar com log em `workspace/[produto]/compliance-warnings.json` e notificar o membro no output final ("N warnings — revise se quiser") — deploy/go-live só com decisão explícita dele |
| `pass` | **PASS** — salva silenciosamente |

### Palavras ad-flag cobertas (baseline mínimo, ver `red_flags.json` pra completo)

Meta/TikTok ad policy (aplicam a copy pra consumidor final, incluindo landing pages que o Meta scraper lê):

- Botox / Filler / Injection / Inject
- Cure / Treat (claims médicos)
- Anti-aging como claim central
- Weight loss / lose weight (supplement/fitness)
- Medical-grade (substituir por cosmetic-grade)
- Guaranteed isolado (substituir por "90-day money-back")
- Before & After literal em headlines
- Nomes de drogas prescritas
- Condition médicas nomeadas (diabetes, cancer, etc)

### Disciplinas cruzadas

- **Em dash (—)**: zero em headlines, ≤2 em copy longa (regra 8a do CLAUDE.md)
- **Siglas/números técnicos**: text overlay em ad, não na fala (skill 08 Etapa 4.5.D)
- **Disclosure "AI Info" (Meta)**: criativo com humano fotorrealista gerado por AI (avatar sintético, UGC gerado, talking head com lip-sync) EXIGE o label "AI Info" da Meta ao publicar. A Skill 08 grava `ai_disclosure_required: true` por concept no `08-creative-engine/dados.json` (gate I da ETAPA 4.5); antes do go-live, o gate valida que TODO concept com esse flag teve o label marcado no Ads Manager (nível do ad → marcação de conteúdo gerado por AI). Skills 08/10 marcam a exigência no briefing; a campanha não vai ao ar sem o membro confirmar que ativou o label

### Bypass emergencial

NÃO há bypass automático. Se o membro insistir em publicar copy com `severity: high` sem rewrite, marcar `manifest.json → compliance_override: { "at": "ISO", "by": "member", "risk_acknowledged": true }` e avisar que está contra policy. Registrar pra que a Skill 11 (ad-analysis) saiba que esse ad pode ter disapproval e não atribua falha a creative quality.

---

## GATE 2 — Promise ↔ Config (automático, blocking)

### O problema

A copy promete "Free shipping", "90-day money-back guarantee", "Use code AURA20 for 20% off" — mas a loja Shopify tem shipping zones que cobram frete em certos estados, a política de returns é de 30 dias (não 90), e o código `AURA20` nunca foi criado. Ad roda, tráfego chega, compra falha, refund war começa.

### Onde aplica

- **Skill 07b** (page-build) — ANTES do push do template/deploy da página
- **Skill 07d** (checkout-aov) — ANTES de aplicar config de checkout/upsell que promete algo
- **Skill 10** (ad-strategy) — ANTES de liberar campanha pra publicação

### Promises rastreadas e validação

Pra cada promise que aparece na copy/páginas/ads, validar contra config real da loja:

| Promise detectada | Fonte na copy/ad | Validação obrigatória | Fonte da verdade |
|-------------------|------------------|------------------------|-------------------|
| "Free shipping" | headline, hero, bullet | Shipping zones Shopify cobrem 100% do target market com `price: 0` | Admin API GraphQL `deliveryProfiles` (ou REST `/admin/api/shipping_zones.json`) |
| "Free shipping over $X" | conditional promise | Threshold configurado corretamente + zona coberta | Admin API shipping rates |
| "90-day money-back guarantee" | guarantee section | Policy page da loja declara 90 dias OU membro tem workflow manual pra aceitar refunds 90d | `/policies/refund-policy` content + confirmação manual |
| "30-day money-back" | mesma regra | Declarado em policy | idem |
| "Use code XXXX for Y% off" | eyebrow, banner, CTA | Discount code existe E é ativo E expira após data da promo | Admin API discount codes |
| "Limited time — ends [date]" | eyebrow, banner | Data futura válida + schema time-bound configurado | `page.json` promo block |
| "Ships in 24h" / "Same-day shipping" | trust row | Fulfillment center consegue cumprir (pergunta explícita ao membro) | Confirmação manual documentada |
| "Made in [country]" | trust row | Produto realmente feito lá (regulatório) | COGS breakdown + manifest |
| "Free [bonus] with purchase" / GWP prometido na PDP | offer stack, bonus section, banner | Fase A da Skill 05 completa: asset gerado + GWP/delivery configurado na loja + link na thank-you page; `condition` do `bonuses[]` bate com a copy da página ("FREE over $X" = `cart_threshold`; sem condição = `unconditional`) | `05-bonus-delivery/` assets + `04-offer-builder/dados.json.bonuses[]` + config GWP (app/Function) |
| "Clinically proven [outcome]" | hero/claim | `04-offer-builder/research-foundation.json` contém evidência rastreável | Research Foundation (Skill 04 Etapa 2.5) |
| "Rated 4.X stars by N customers" | social proof | Review app (Judge.me/Loox/Yotpo) tem esses números | Admin API da review app |
| "As seen on [outlet]" | trust row | Prova de aparição real (link, screenshot, PR release) | Manual confirmation com artefato |
| "FDA approved" / "FDA cleared" | authority claim | Produto realmente tem esse status | Regulatory doc obrigatório |
| "Satisfaction guarantee" vago | guarantee | Policy da loja cobre | Policy page content |

### Pipeline do gate

1. **Extração**: parse do markdown da copy + HTML das sections + JSON do ad-strategy procurando promise-patterns (regex + LLM classification)
2. **Cross-check**: pra cada promise, consultar a fonte da verdade
3. **Output `workspace/[produto]/promise-check.json`**:
   ```json
   {
     "checked_at": "ISO",
     "promises_total": 7,
     "pass": 5,
     "warn": 1,
     "fail": 1,
     "items": [
       {
         "promise": "Free shipping worldwide",
         "source": "06-copy-engine/copy-engine.md hero section",
         "validation": "shipping_zones",
         "status": "fail",
         "reason": "Shipping zone 'Rest of world' tem $24.99 rate; apenas US é free",
         "fix": "Reescrever como 'Free US shipping' OU configurar free rate nas outras zonas"
       }
     ]
   }
   ```
4. **Decisão**:
   - `fail` ≥ 1 → **BLOCK deploy**, reportar ao membro com `fix` sugerido
   - `warn` ≥ 1 → apresentar ao membro pra decidir (PASS manual)
   - `pass` em todos → prosseguir

### Fix paths

A skill que detecta `fail` oferece DOIS caminhos pro membro:

1. **Ajustar copy** pra alinhar com config atual (mais rápido, mas perde força de promessa)
2. **Ajustar config** da loja pra cumprir a promessa (mais trabalho, mais poderoso) — a skill documenta passos específicos (ex: "criar discount code AURA20 no Shopify admin > Discounts")

Membro escolhe 1 ou 2. Skill re-valida depois da mudança.

### Bypass

Zero bypass automático. Promise não-cumprida → chargeback/refund war/FTC complaint. O gate salva o membro de si mesmo.
