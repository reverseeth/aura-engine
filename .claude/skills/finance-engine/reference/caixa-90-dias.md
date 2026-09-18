# Finance Engine · Referência: Caixa, quanto o negócio precisa pra rodar 90 dias (ETAPA 6)

> As três perguntas de caixa, a fórmula de `cash_needed_90d`, a regra do `payout_lag_days` como campo do membro, o `runway_months` e os guard-rails. Abra na ETAPA 6.

### ETAPA 6 — Caixa: quanto o negócio precisa pra rodar 90 dias

Modelo lucrativo e caixa morto convivem. O modelo diz lucro no mês 3; o banco diz morte na semana 3. Troque a pergunta *"sou lucrativo eventualmente?"* por três: **quando o dinheiro sai da conta, quando entra, e o cohort fica positivo antes do boleto vencer?**

**Necessidade de caixa em 90 dias:**

```
caixa_necessario_90d =
      (ad_spend_diário × payout_lag_days × 1,3)      ← o buraco do descasamento (1,3 = margem de segurança)
    + (custo_fixo_mensal × 3)                         ← o fixo não espera venda entrar
    + desembolso_de_estoque_previsto_no_período       ← reposição, se houver
    − margem_de_contribuição_acumulada_projetada_90d  ← o que a operação devolve no período
```

**`payout_lag_days` é campo do membro, não default.** O lag nominal do Shopify Payments é 3-5 dias (Stripe ~2), mas processadora segura mais quando a conta é nova ou o volume dá spike — exatamente o que a escala provoca. Loja com menos de ~90 dias de processamento, ou no primeiro pico grande: use **7-14 dias** e confirme no dashboard do processador se há reserva rolante ativa. Escalar assumindo repasse em 3 dias com reserva de 30% ativa é o furo de caixa clássico da loja nova.

Publique **`runway_months`** = caixa disponível ÷ burn mensal. É o número que responde "quantos meses eu tenho pra fazer isso funcionar" — e o que transforma decisão de spend em decisão de prazo.

**Guard-rails, sempre no relatório:**
- Saber a **data exata da saída de caixa** (a data do boleto, não "mês 3").
- **Float não conserta oferta quebrada.** Prazo maior de pagamento adia o problema, não resolve.
- Nunca escalar dívida mais rápido que a capacidade de entrega — reembolso e chargeback destroem float.
- Não financiar caos operacional.

No Modo B esta ETAPA ganha o stack de float completo (ETAPA 10).
