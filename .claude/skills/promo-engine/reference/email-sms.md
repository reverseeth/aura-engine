# Promo Engine · Referência: Email e SMS da janela, calendário aqui e assets na retention-engine (ETAPA 7)

> A divisão explícita entre calendário e assets, as fases e prazos do playbook, a orientação de segmento, o criativo por fase seguindo awareness e os sistemas que a retention-engine puxa ao executar. Abra na ETAPA 7.

### ETAPA 7 — Email/SMS da janela (calendário da `promo-engine`, assets da `retention-engine`)

**Divisão explícita, sem órfão:** a **`promo-engine` é dona do calendário, das janelas de envio, das fases e da orientação de segmento**; a **`retention-engine` produz os assets** (emails, SMS, adaptação sazonal dos flows) e opera o ESP. Flow **nunca desliga** durante campanha — se adapta (regra da `retention-engine`). O que esta skill grava em `email_sms_calendar_13` e entrega:

**Fases e prazos (playbook de Q4 da fonte, edição 2025):** ofertas finais e pop-up novo aprovados **até 10/nov**; calendário travado e flows testados **até 15/nov**; warm-up 10-24/nov; BFCM 26-30/nov; gifting window 5-14/dez; last chance 15-21/dez — **os cutoffs de envio (~14-15/dez standard, 19-21/dez express) vêm da operação/3PL, confirme antes de prometer**; 26/dez clearance/Boxing Day; 31/dez campanha final. Rode `email tolera volume SMS é cirúrgico, engaged 30 engaged 90 dormant 120, quiet hours texas` — o princípio-mestre do playbook: **email tolera volume; SMS é cirúrgico**.

**Orientação de segmento que acompanha o calendário:** os grandes pushes vão pro público engajado (30/90 dias); dormentes de 120d+ seguram até o clearance de fim de ano; assinantes não recebem sale do que já assinam; quem comprou na janela sai da pressão de sale. **Criativo por fase segue awareness (Schwartz):** warm-up = problem/solution-aware (teaser, countdown); pico = **most aware — o desconto é o hero**, zero educação de produto; Cyber Monday = counteroffer com twist + "não haverá oferta melhor por 12 meses"; gifting = presente + deadline; last chance = o prazo de envio como argumento máximo; fim de ano = clearance + "new year, new me". Se a ETAPA 2.2 aprovou VIP: o warm-up flow VIP (sequência de 5 emails até o early access) entra no calendário — a `retention-engine` constrói.

**Sistemas que a `retention-engine` puxa ao executar** (donos dela; a `promo-engine` só aponta): `razão para a sale, stock up recommendation, sale de 24 horas não planejada` · `campanha sazonal de 4 dias com 6 templates, dia de slump, template da inveja` · `seasonal abandoned cart SMS update checklist offer details campaign close time urgency scarcity no rain check` · `MMS copy overlay imagem que engaja o coracao evitar MMS nas ultimas horas da promo` · `seis segmentacoes SMS novos versus recorrentes ultima compra VIP por produto por localizacao` · `email SMS coordination echo not collide send email first SMS follow up non-openers staggered cadence`.

Marque `email_sms_calendar_13.handed_off: true` e avise o membro que os sends nascem quando ele disser `'retention'` com a promo no ar.
