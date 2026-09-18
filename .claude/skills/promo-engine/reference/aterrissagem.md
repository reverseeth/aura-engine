# Promo Engine · Referência: Aterrissagem, fim da janela e volta pro evergreen (ETAPA 9)

> A regra de fim por horário criada desativada, a saída em cinco passos com a cauda degradada, a volta do budget do evergreen e o reinício limpo da leitura. Abra na ETAPA 9.

### ETAPA 9 — Aterrissagem: fim da janela e volta pro evergreen

**Fim por horário, sem depender de memória:** rode **Regra de fim de promo por horário** (`custom rule turn off condition time current time is greater than data fim promo`). Ads Manager → Rules → Create new rule → Custom rule → aplicada à(s) campanha(s) da promo → Action: turn off → Condition: **Time → current time is greater than → data/hora de término** → Time range: maximum; Schedule: continuously. A rule checa a cada ~30 min. Criada DESATIVADA pro membro revisar e **ativar antes do fim da janela** (padrão inviolável de automação da casa). O automatic discount já tem a data-fim agendada desde a ETAPA 2.5 — campanha e desconto morrem juntos; banner/announcement bar saem do site na sequência (`page-build`).

**A saída em ordem:**
1. **Pós-pico imediato:** dip esperado — budgets descem junto (ninguém acorda US$ 20k no vermelho por budget de sexta esquecido no sábado); reset da meia-noite até o fim.
2. **Cauda da janela (holiday):** oferta **degradada de propósito** (ETAPA 3) até ~16-17/dez; depois, dezembro fecha com o argumento de prazo de envio, não de desconto.
3. **Campanha de promo OFF na data-fim; evergreen segue** — ele nunca desligou. Budget realocado de volta pro evergreen no nível pré-janela (o ad-log tem o número exato de antes).
4. **Leitura do evergreen reinicia limpa:** sazonalidade que mudou a demanda é o caso (b) das exceções do §5 — "new reason to be scaling": o histórico de degraus da janela não trava nem acelera o passo novo; a `scale-engine` retoma o protocolo normal do zero de leitura.
5. **Janeiro não é férias de ads** pra supplements/health & wellness: "Q5" — o gasto de saúde sobe ~35-40% e a fonte manda não tirar o pé em dezembro.

Linha no ad-log: "promo fim — [evento], rule disparou / desligado manual". `landing` gravado no `dados.json` e `manifest.promo.active: false`.
