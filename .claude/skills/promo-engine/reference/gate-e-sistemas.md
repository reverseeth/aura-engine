# Promo Engine · Referência: O gate que não se negocia e os sistemas nomeados a puxar

> A razão do gate de recálculo do breakeven antes de qualquer campanha e a lista do núcleo mínimo de sistemas, com a query exata de cada um. Abra antes de montar qualquer plano de janela.

### O gate que não se negocia

**Recalcular o breakeven ROAS e o CPA-alvo com a margem promocional ANTES de ligar qualquer campanha.** É o erro nº 1 da temporada segundo a fonte primária (P1): lançar oferta melhor (margem menor) e continuar escalando no MESMO ROAS-alvo de antes — mais receita, menos lucro. A ETAPA 4 é esse gate. Sem `promo_economics` calculado com os números do membro, as ETAPAs 5 a 8 **não rodam**: nenhuma campanha é criada, nenhum brief vai pra `creative-engine`, nenhum calendário vai pra `retention-engine`. A skill para e diz o que falta. Número de margem **nunca se estima** — vem da `offer-builder`, do manifest ou do membro.

### Puxe os SISTEMAS NOMEADOS da base

Rode `search_knowledge` (deep=true) com a `best_query` exata de cada sistema, agrupado por ETAPA (o mapa fino está nas ETAPAs). Núcleo mínimo a carregar antes de montar qualquer plano de janela:

- **Promo Campaign (Broad / WARM60 / HOT90)** — `promo campaign CBO três ad sets broad WARM60 HOT90 retargeting só em sale`
- **Offer-Change Break-Even Reset** — `nova oferta recalcular break-even ROAS e CPA-alvo antes de escalar promo`
- **Scaling Protocol & Decision Tree (fonte primária 2026)** — `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo` (é dele que vem a exceção de promo do §5)
- **Curva BFCM + Cyber Monday Nightcap** — `curva BFCM sexta é sempre o maior dia sábado de manhã nightcap Cyber Monday 15h EST`
- **Surf Scaling (escala intradiária)** — `surf scaling escala intradiária planilha por período blended ROAS dobrar 20%`
- **Reset da meia-noite (~50% do spend REAL)** — `reset da meia-noite metade do spend real nunca budget nominal explode a conta`
- **Blueprint de criativo de sale** — `criativos de sale banner sobre o melhor ad foto do produto com oferta statics BFCM`
- **Desire Calendar (calendário sazonal de desejos)** — `calendario sazonal de desejos health sex status belonging control comfort por mes`
- **Regra de fim de promo por horário** — `custom rule turn off condition time current time is greater than data fim promo`
- **Revival de winner sazonal / calendário de desejos** — `religar seasonal winners ads que morreram voltam no mesmo período calendário de desejos`

Aprofunde. Uma janela de promo concentra num fim de semana o volume de decisões de um trimestre — errar a margem ou o reset custa o mês mais importante do ano.
