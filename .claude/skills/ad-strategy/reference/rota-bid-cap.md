# Ad Strategy · Referência: Rota de teste com bid cap (ETAPA 3.0)

> A escolha entre as duas rotas de teste, o setup da rota bid cap (lance inicial, teto, budget, estrutura), a escada de lance quando nada gasta, a regra de não migrar criativo que não gastou e o que gravar no `dados.json`. Cânone: `.claude/lib/ad-taxonomy/README.md` §8, que vence onde divergir. Abra na ETAPA 3, antes da 3.1.

### ETAPA 3.0 — Rota de teste: Max Conversion ou bid cap

Pergunte ao membro, em uma linha, antes de calcular a capacidade:

> "Quer subir o teste no padrão da Aura (Max Conversion, o Meta gasta o budget e a leitura decide) ou em bid cap (o lance segura o gasto: o Meta só gasta quando acha comprador abaixo do seu CPA alvo, e criativo que não gasta sai de graça)?"

Sem preferência, o default é Max Conversion. Grave `test_route: "max_conversion" | "bid_cap"`.

**Rota bid cap, setup:**

1. **Lance inicial = target CPA** (`manifest.target_cpa`, senão `unit_economics.target_cpa_primary_2x`). **Teto = breakeven CPA** (`unit_economics.weighted_margin_per_order`, o mesmo `breakeven_cpa` da 3.1). Mostre os dois números ao membro.
2. **Estrutura igual à 3.3:** uma campanha CBO, um conceito por ad set, pack 3-2-2, audiência broad, otimização Purchase. Na campanha, bid strategy = **Bid cap**; o mesmo lance em todos os ad sets.
3. **Budget da campanha = 10× o lance por dia** (lance US$ 30 → US$ 300/dia). Diga ao membro que o budget é espaço, não meta: o lance segura o gasto, e num dia sem comprador abaixo do lance o gasto fica perto de zero. Confirme que ele aceita ver esse valor gasto num dia bom; se não aceita, o budget é o que ele aceita (nunca abaixo de 3× o lance).
4. **Capacidade (3.1) pelo budget real do membro** (`manifest.budget_daily`), não pelo nominal de 10×: o número de conceitos continua o da fórmula do cânone §1.
5. **Proteções da ETAPA 6 continuam:** daily maximum por ad set (cerca de 3× o target CPA), automação A (spend 5× em 24h pausa) e automação B (URL fora do domínio desliga).
6. Campanha `[Produto]_[YYYYMMDD]_TestBid`.

**Leitura, que a `ad-analysis` aplica (escreva no relatório pro membro já saber):**

- Gasto zero num ad set = não achou comprador abaixo do lance = teste de graça. Causas, na ordem: lance baixo, criativo fraco, oferta ruim.
- **Escada:** 48h sem entrega na campanha inteira → +10% do target CPA no lance, um degrau a cada 48h, até o teto do breakeven. Gastou, para de subir.
- No teto e sem gasto: ad set que não gastou enquanto outros gastam é `loser` (conceito novo no lugar); nada gasta no teto = oferta ou página antes de criativo (`offer` e `copy`).
- **Nunca** mover criativo que não gastou no bid cap pra campanha sem lance (Max Conversion): é muito improvável performar com ROAS alto fora do lance, e o teste só sai mais caro.

**Gravar no `dados.json`:**

```json
"test_route": "bid_cap",
"bid_cap": {
  "bid_initial": 40,
  "bid_ceiling": 80,
  "bid_step": 4,
  "step_interval_hours": 48,
  "campaign_daily_budget_nominal": 400,
  "member_daily_budget": 240
}
```

Na rota Max Conversion, `test_route: "max_conversion"` e `bid_cap: null`. Toda mudança de lance executada vira linha no `ad-log.md` (cânone `.claude/lib/ad-log/README.md`).
