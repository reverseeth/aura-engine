# Tracking Setup · Referência: Instalar o Meta Pixel (ETAPA 1)

> Os passos no Shopify admin pela integração nativa, a regra do data sharing em Always on, o porquê de nunca hardcodar o snippet no tema e os 5 eventos do funil a confirmar. Abra na ETAPA 1.

### ETAPA 1 — Instalar o Meta Pixel

A integração nativa Shopify↔Meta gerencia o pixel sem editar tema. Passos pra colar no admin:

1. **Shopify admin > Settings > Apps and sales channels > Facebook & Instagram** (instalar o canal "Facebook & Instagram" se ainda não estiver). Conectar o Business Manager e o ad account corretos.
2. Em **Settings > Customer events** (a área que SUBSTITUIU os antigos "Additional scripts"), confirmar que existe um **Meta pixel** conectado ao Dataset/Pixel ID certo. O checkout roda em Checkout Extensibility (padrão hoje pra toda loja nova): o pixel entra via o app Meta ou como **Custom pixel** — NUNCA snippet hardcoded no `theme.liquid` (duplica eventos e quebra dedup).
3. **Data sharing do pixel: "Always on", NUNCA "Optimized".** Desde 13/jan/2026 o default de data sharing dos app pixels é "Optimized" — que PAUSA o envio de dados quando o pixel fica dias sem sinal de tráfego/venda. É exatamente o cenário da loja nova pré-launch: o pixel parece instalado, mas a Shopify silenciosamente para de enviar eventos, e o membro lança ads com dataset vazio. Em **Settings > Customer events**, mude o data sharing do pixel da Meta pra **"Always on"** antes de qualquer validação.
4. Confirmar que o **Pixel ID** no Shopify bate com o Pixel/Dataset que o ad account vai usar na Skill `ad-strategy`. Mismatch aqui = eventos no dataset errado, campanha cega.

> **Por que não hardcodar no tema:** snippet manual no `theme.liquid` + pixel da integração nativa = evento duplicado sem `event_id` consistente, derrubando o EMQ e inflando contagem de Purchase. Deixe a integração nativa ser a única fonte do pixel.

**Eventos do funil a confirmar** (Events Manager > Test Events, navegando a loja): `PageView`, `ViewContent` (PDP), `AddToCart`, `InitiateCheckout`, `Purchase`. Se algum falta, o problema está na integração nativa (re-conectar o canal) ou no tema (PDP sem o trigger de ViewContent).
