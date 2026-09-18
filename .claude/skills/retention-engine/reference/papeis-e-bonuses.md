# Retention Engine · Referência: TrendTrack opcional, divisão de papéis pós-compra e conexão com os bônus da oferta (ETAPA 1)

> O uso opcional do TrendTrack pra calibrar timing, a tabela de donos de cada artefato pós-compra (bonus-delivery, retention-engine, content-recycler) e o mapa de `delivery_trigger` pro email que entrega cada bônus. Abra na ETAPA 1.

## TrendTrack MCP (opcional, se conectado)

Se há tools com prefixo `mcp__trendtrack__` disponíveis:

- **`mcp__trendtrack__analyze_shop_emails`** com domínio de 1-3 concorrentes do `competitor-analysis/competitor-analysis.md` → retorna padrões reais de cadência, subject lines e content categories da concorrência. Use como referência (não copy-paste) pra calibrar timing dos fluxos abaixo (welcome series, abandoned cart, post-purchase) com benchmark de mercado.

Se TrendTrack NÃO estiver disponível, segue templates abaixo direto, baseados em VOC + offer.

## Divisão de papéis pós-compra (`bonus-delivery` / `retention-engine` / `content-recycler`) — fonte única de verdade

Três skills tocam o pós-compra. Pra não duplicar nem sobrescrever, cada artefato tem UM dono:

| Artefato | Quem PRODUZ | Quem ENTREGA | Nota |
|---|---|---|---|
| Asset do bônus (PDF/e-book, config GWP, link) | **Skill `bonus-delivery`** | — | A `bonus-delivery` gera o asset e define o `delivery_trigger`. Não monta email. |
| **Email de entrega de bônus** | **Skill `retention-engine`** (este) | **Skill `retention-engine`** | A `retention-engine` é o ÚNICO executor de email. A `bonus-delivery` fornece conteúdo + trigger; a `retention-engine` monta o flow e injeta o `{{BONUS_LINK}}`. Nunca duplicar lógica de email na `bonus-delivery`. |
| Flows de lifecycle (welcome, abandoned-cart, post-purchase, win-back, replenishment) | **Skill `retention-engine`** | **Skill `retention-engine`** | Fonte única dos flows de retenção. |
| Email-sequence derivada do winner (recycler) | **Skill `content-recycler`** | Membro (importa manual) | É **variação A/B de nutrição** derivada do criativo winner, NÃO um flow de lifecycle. Não colide nem sobrescreve o welcome/post-purchase da `retention-engine` — entra como flow separado/teste paralelo. Ver nota na Skill `content-recycler`. |

Regra prática: se é email que dispara por evento de ciclo de vida (signup, cart, compra, inatividade, reorder) → é flow da `retention-engine`. Se é peça de nutrição reaproveitada de um winner pra testar contra o que já roda → é a `content-recycler`, e o membro decide onde plugar sem desligar os flows da `retention-engine`.

## Conexão com bonuses da oferta (Skill `offer-builder`)

Antes de gerar os fluxos, ler `offer-builder/dados.json.bonuses[]` e casar o `delivery_trigger` de cada bonus com o email do fluxo que entrega:

| `delivery_trigger` | Fluxo / email que entrega o bonus |
|--------------------|-----------------------------------|
| `on_signup` | Welcome Series — Email 1 (boas-vindas) |
| `post_purchase` | Post-Purchase Welcome — Email 1 (obrigado) |
| `day_7_post_purchase` | Post-Purchase Welcome — Email 3 (~dia 7) |
| `on_first_reorder` | Replenishment — Email 2/3 (no reorder) |

Incluir o asset/link do bonus (PDF, Circle invite, código de acesso — produzidos na Skill `bonus-delivery`) no corpo do email correspondente. Se a Skill `bonus-delivery` ainda não gerou o asset, deixar placeholder `{{BONUS_LINK}}` no HTML e avisar no output final que o link precisa ser colado antes de ativar.
