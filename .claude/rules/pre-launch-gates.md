---
name: pre-launch-gates
description: Gates automáticos inegociáveis antes de qualquer launch (página deploy ou ads go-live). Dois gates principais — Compliance (ad-flag words) e Promise↔Config (copy promete X, loja precisa entregar X).
paths:
  - .claude/skills/05-copy-engine.md
  - .claude/skills/06-page-engine.md
  - .claude/skills/06b-page-sections.md
  - .claude/skills/06c-page-deploy.md
  - .claude/skills/07-creative-engine.md
  - .claude/skills/08-ad-strategy.md
---

# Pre-launch Gates (NON-NEGOTIABLE)

Dois gates BLOQUEIAM qualquer deploy de página ou go-live de ad. Gate não é warning — é gate. Status FAIL = operação não prossegue.

## GATE 1 — Ad-flag Compliance (automático, blocking)

### Onde aplica

- **Skill 05** (copy-engine) — ANTES de salvar qualquer peça final de copy
- **Skill 06b** (page sections generation) — ANTES de compilar Liquid com copy injetada
- **Skill 06c** (page deploy) — ANTES do push pra Shopify
- **Skill 07** (creative-engine) — ANTES de finalizar briefing (já existe Etapa 7.5)
- **Skill 08** (ad-strategy) — ANTES de entregar instrução "colar no Ads Manager"

### Como invocar

Toda skill acima DEVE rodar:

```
.claude/lib/compliance-preflight/run.py --input <texto> --config .claude/lib/compliance-preflight/red_flags.json --schema .claude/lib/compliance-preflight/output-schema.json
```

OU invocar o `checker.md` prompt via Claude diretamente no contexto da skill.

### Decisão de gate

Parse do JSON output:

| Severity | Ação |
|----------|------|
| `critical` | **BLOCK** — não salva, não publica, não faz deploy. Apresenta ao membro com `rewrite_suggestion` e pede revisão manual |
| `high` | **BLOCK por default**. Aplicar `rewrite_suggestion` automática e **re-rodar compliance check** no texto rewriteado. Se o rewrite passar (low/medium), prosseguir. Se falhar, BLOCK até revisão manual. |
| `medium` | **WARN** — salva, mas loga em `/workspace/[produto]/compliance-warnings.json` e notifica membro no output final ("2 warnings — revise se quiser") |
| `low` | **PASS** — salva silenciosamente |

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
- **Siglas/números técnicos**: text overlay em ad, não na fala (skill 07 Etapa 4.5.D)

### Bypass emergencial

NÃO há bypass automático. Se o membro insistir em publicar copy com `severity: high` sem rewrite, marcar `manifest.json → compliance_override: { "at": "ISO", "by": "member", "risk_acknowledged": true }` e avisar que está contra policy. Registrar pra que a Skill 09 (ad-analysis) saiba que esse ad pode ter disapproval e não atribua falha a creative quality.

---

## GATE 2 — Promise ↔ Config (automático, blocking)

### O problema

A copy promete "Free shipping", "90-day money-back guarantee", "Use code AURA20 for 20% off" — mas a loja Shopify tem shipping zones que cobram frete em certos estados, a política de returns é de 30 dias (não 90), e o código `AURA20` nunca foi criado. Ad roda, tráfego chega, compra falha, refund war começa.

### Onde aplica

- **Skill 06c** (page-deploy) — ANTES de push final
- **Skill 08** (ad-strategy) — ANTES de liberar campanha pra publicação

### Promises rastreadas e validação

Pra cada promise que aparece na copy/páginas/ads, validar contra config real da loja:

| Promise detectada | Fonte na copy/ad | Validação obrigatória | Fonte da verdade |
|-------------------|------------------|------------------------|-------------------|
| "Free shipping" | headline, hero, bullet | Shipping zones Shopify cobrem 100% do target market com `price: 0` | `shopify theme shipping zones` via Admin API |
| "Free shipping over $X" | conditional promise | Threshold configurado corretamente + zona coberta | Admin API shipping rates |
| "90-day money-back guarantee" | guarantee section | Policy page da loja declara 90 dias OU membro tem workflow manual pra aceitar refunds 90d | `/policies/refund-policy` content + confirmação manual |
| "30-day money-back" | mesma regra | Declarado em policy | idem |
| "Use code XXXX for Y% off" | eyebrow, banner, CTA | Discount code existe E é ativo E expira após data da promo | Admin API discount codes |
| "Limited time — ends [date]" | eyebrow, banner | Data futura válida + schema time-bound configurado | `page.json` promo block |
| "Ships in 24h" / "Same-day shipping" | trust row | Fulfillment center consegue cumprir (pergunta explícita ao membro) | Confirmação manual documentada |
| "Made in [country]" | trust row | Produto realmente feito lá (regulatório) | COGS breakdown + manifest |
| "Clinically proven [outcome]" | hero/claim | `04-research-foundation.json` contém evidência rastreável | Research Foundation (Skill 04 Etapa 2.5) |
| "Rated 4.X stars by N customers" | social proof | Review app (Judge.me/Loox/Yotpo) tem esses números | Admin API da review app |
| "As seen on [outlet]" | trust row | Prova de aparição real (link, screenshot, PR release) | Manual confirmation com artefato |
| "FDA approved" / "FDA cleared" | authority claim | Produto realmente tem esse status | Regulatory doc obrigatório |
| "Satisfaction guarantee" vago | guarantee | Policy da loja cobre | Policy page content |

### Pipeline do gate

1. **Extração**: parse do markdown da copy + HTML das sections + JSON do ad-strategy procurando promise-patterns (regex + LLM classification)
2. **Cross-check**: pra cada promise, consultar a fonte da verdade
3. **Output `/workspace/[produto]/promise-check.json`**:
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
         "source": "05-copy.md hero section",
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
