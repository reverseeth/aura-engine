# Retention Engine · Referência: Flow 5, Replenishment (Fase B)

> Os quatro sistemas a puxar, a definição da janela de reorder em quatro passos (pergunta ao membro, cálculo, benchmark, curva medida), os 3 emails e a arquitetura de assinatura que governa o Email 2. Abra ao escrever o replenishment.

### 5. Replenishment (consumíveis — trigger baseado na janela de reorder) — FASE B (pós-launch)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Day Zero Triggered-Email Method** — replenishment é behavior-triggered mini-funnel (dispara pelo timing real de consumo), não drip por tempo fixo (rode `Day Zero behavior-triggered email mini-funnel outperforms time-based drip cap day 4`)
- **Fibonacci Drip-Cadence Sequence** — espaçamento dos nudges antes/depois do produto acabar (day 0/1/2/3/5/8) (rode `Fibonacci sequence drip campaign email cadence day 0 1 2 3 5 8 spacing Copyhackers`)
- **Door-Closing Aversion** — enquadrar a janela de reorder como opção que expira (subscription/2-pack antes de acabar o estoque dele) (rode `door-closing aversion loss of options Shin Ariely expires midnight only 3 spots disappearing bonus`)
- **Subscription Economics Playbook (8 passos)** — a economia da assinatura que o Email 2 oferece: take rate, one-click upsell pós-compra e produto dimensionado pra supply de 1 mês; ler junto do bloco "Arquitetura de assinatura" abaixo antes de escrever o Email 2 (rode `playbook de subscription take rate one-click upsell pós-compra supply de 1 mês`)

A janela de reorder não vem pronta do `offer-builder/dados.json` (ele não produz um `reorder_rate` legível por máquina). Defina a fonte assim, antes de configurar o fluxo:

1. PERGUNTAR ao membro: "Em quantos dias um cliente típico **acaba** uma unidade do produto?" (ex: um sérum de 30ml dura ~30 dias).
2. Calcular o timing dos emails a partir disso: Email 1 dispara ~5-7 dias **antes** do produto acabar (ex: produto dura 30 dias → Email 1 no dia 23-25 pós-compra), Email 2 perto do fim, Email 3 logo após o fim estimado.
3. Cruzar com benchmark: a 2ª compra ideal cai **antes de 65 dias** pós-primeira-compra. Se a duração informada empurrar o reorder pra além disso, antecipar o nudge (oferecer subscription/2-pack) pra não perder a janela.
4. **Cruzar com a curva medida, quando existir** (`finance-engine/dados.json` → `cohorts`): `ltv_pct_by_month` mostra em qual mês a recompra de fato acontece nesse negócio, e `decay_factor` diz o quanto ela decai de um mês pro seguinte. Se a janela declarada pelo membro no passo 1 não bate com o mês em que a curva medida acusa recompra, **a curva medida vence** — ela é o comportamento real, a estimativa dele é memória. Se a recompra medida vier depois de `cohorts.crossover_month`, o Email 2 é o momento de empurrar assinatura/2-pack com mais força: sem isso o cohort demora demais pra pagar o CAC. **Sem o arquivo da `finance-engine` (ou com `cohorts.calibrated: false`), os passos 1-3 decidem sozinhos**, como hoje.

- Email 1 (~5-7 dias antes do acabar): "seu [produto] tá acabando — reorder aqui"
- Email 2 (perto do fim): subscription option pelo preço-base (o one-time é que custa mais)
- Email 3 (pós-acabar): "hora de reabastecer"

**Arquitetura de assinatura (ler `offer-builder/dados.json.subscription_architecture`):**
- `onetime_plus_sub_no_reorder` → o **Email 2 deste fluxo é O momento canônico** de oferecer a assinatura (a PDP vendeu one-time de propósito; a conversão pra assinatura foi delegada pra cá).
  > **Framing corrigido (2026-09-01):** a `offer-builder` não dá mais desconto ao assinante — ela cobra um **prêmio de ~15% no one-time**. Leia `onetime_premium_pct` (o campo antigo `sub_discount_pct` existe só por compatibilidade e é **sempre 0**; usá-lo faria o email prometer "0% de desconto"). O framing correto é *"você paga mais por NÃO assinar"*: a assinatura é o preço-base, o avulso é que carrega o prêmio. Razão econômica: o desconto entregaria margem exatamente na recompra, que é onde ela é melhor.
- `subscription_first` → o fluxo mira só quem comprou one-time (assinante já tem reorder automático — mandar replenishment pra assinante é ruído); filtrar por não-assinante no trigger.
- `no_subscription` (ou campo ausente) → Email 2 oferece o 2-pack/bundle no lugar da assinatura.
