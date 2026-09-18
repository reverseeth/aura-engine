# Retention Engine · Referência: Flow 4, Win-Back (Fase B)

> Os cinco sistemas a puxar, os 3 emails e o gatilho pelo número medido quando os cohorts existem. Abra ao escrever o win-back.

### 4. Win-Back (60+ dias sem purchase, subscriber ativo) — FASE B (pós-launch, ≥ 50 compras)

**Frameworks a puxar (rode a query de cada um antes de escrever):**
- **Hormozi's 9-Word Email** — reativação curta ("are you still interested in [resultado]?") como abertura mais barata e de maior reply (rode `Hormozi 9-word email are you still interested reactivation dormant leads $100M Leads`)
- **Kennedy's Collection Agency Model** — escalada de urgência em intervalos com mudança de formato a cada email (rode `Kennedy collection agency model multi-step mailing format change urgency intervals`)
- **Collier's Ruffle-Smooth-Ruffle** — alternar tom emocional (tensão → alívio → tensão) pra furar a habituação de quem ignora (rode `Collier ruffle smooth ruffle alternating emotional tone collection series habituation`)
- **Fórmula de Reorder + Winback com desconto progressivo** — a escada dos 3 emails: abrir pelo frame de progresso do cliente (está progredindo → vai progredir mais → vai perder o progresso) e só escalar o desconto quando o frame não converter; o mesmo sistema traz a fórmula de reorder ("7 dias antes de acabar o estoque") que alimenta o timing do Email 1 do Fluxo 5 — puxou aqui, reuse lá (rode `você está progredindo vai progredir mais continue vai perder o progresso, 7 dias antes de acabar o estoque`)
- **Engagement Suppression / Sunset & Double-Opt-In Re-engagement** — definir o ponto de corte: quem não reativar vai pra sunset/suppression pra proteger deliverability (rode `engagement suppression sunset re-engagement double opt-in unsubscribe non-engaged deliverability 30 day`)

- Email 1: "sentimos sua falta" + novidade do produto
- Email 2 (7 dias depois): oferta especial com código de win-back
- Email 3 (14 dias depois): final call + feedback survey pra entender porque churn

**Gatilho com número medido (se `finance-engine/dados.json` existir):** os "60+ dias sem purchase" são um default de mercado. Com a curva medida na mão, o disparo certo é logo depois de `cohorts.churn_spike_day` (quem passou do pico sem recomprar é inativo de fato, não alguém ainda dentro da janela normal de consumo) — e o tamanho do incentivo do Email 2 se calibra por `cohorts.crossover_month`: cliente que ainda não cruzou pra positivo não comporta desconto agressivo, porque o cohort dele nem pagou o CAC. **Sem o arquivo, mantenha os 60+ dias**, como hoje.
