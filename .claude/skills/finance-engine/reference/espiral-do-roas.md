# Finance Engine · Referência: A espiral do ROAS, o número que a ad-analysis e a scale-engine consultam (ETAPA 5)

> A conta do cânone que prova o erro, as fórmulas de `breakeven_roas_with_fixed` e `spend_to_breakeven_with_fixed` com a conferência, a linha divisória entre subir e cortar spend, o gate obrigatório de saída e o contrato com as skills consumidoras. Abra na ETAPA 5.

### ETAPA 5 — A espiral do ROAS: o número que a `ad-analysis` e a `scale-engine` consultam

**Esta ETAPA é a razão principal de a skill existir.** O cânone §4 define o erro; aqui ele vira número.

ROAS é adimensional e ignora custo fixo. Maximizá-lo isoladamente inverte a decisão certa. A conta que prova isso, e que esta skill reproduz com os números do membro:

> Base: ROAS-alvo 4×, spend US$ 250k → receita US$ 1M; COGS 30% → lucro bruto US$ 700k; margem de contribuição US$ 450k; fixos US$ 300k → **lucro US$ 150k**.
> ROAS cai pra 3× com o mesmo spend: margem de contribuição US$ 275k; fixos continuam US$ 300k → **prejuízo de US$ 25k**.
> Reação intuitiva — cortar spend pra US$ 150k e "voltar ao 4×": margem de contribuição US$ 270k → **prejuízo MAIOR, US$ 30k**. O ROAS subiu e o resultado piorou, porque os fixos não encolheram.
> Reação correta: **aumentar** spend pra US$ 350k aceitando ROAS ~2,65 → volta ao breakeven.

**As fórmulas (rode com os números do membro, não com os do exemplo):**

```
margin_rate = weighted_margin_per_order / aov_expected        (= 1 / breakeven_roas da skill `offer-builder`)

breakeven_roas_with_fixed = (1 + fixed_costs_monthly / ad_spend_monthly) / margin_rate

spend_to_breakeven_with_fixed = fixed_costs_monthly / (margin_rate × roas_projected − 1)
    válido só quando  margin_rate × roas_projected > 1
```

Conferência com o exemplo do cânone (`margin_rate` = 0,70; fixos 300k): a 250k de spend, `breakeven_roas_with_fixed` = (1 + 300/250)/0,70 = **3,14** — por isso 3,0× dá prejuízo. A 350k, = (1 + 300/350)/0,70 = **2,65** — exatamente o número do material. **O breakeven com fixo CAI conforme o spend sobe.** É essa propriedade que torna o corte reflexo a decisão errada.

**A linha divisória, e é ela que decide:**

| Situação | O que cada dólar a mais de spend faz | Recomendação |
|---|---|---|
| ROAS **acima** do breakeven de variável (`1 / margin_rate`) | **Adiciona** margem de contribuição | Cortar spend **aumenta** o prejuízo. A saída costuma ser subir spend aceitando ROAS menor até `spend_to_breakeven_with_fixed`. |
| ROAS **abaixo** do breakeven de variável | **Destrói** margem de contribuição | Cortar é certo. Aqui a régua de descida do `ad-taxonomy` §5 (−20%) vale integralmente — mais volume só aprofunda o buraco. |

**Gate obrigatório de saída desta ETAPA:**

- **Fixos conhecidos** → calcule, publique `breakeven_roas_with_fixed`, `spend_to_breakeven_with_fixed` e `verdict`, e grave `cut_spend_recommendation_allowed` conforme a linha divisória acima.
- **Fixos desconhecidos** → `breakeven_roas_with_fixed: null`, `verdict: "blocked_pending_fixed_costs"`, `cut_spend_recommendation_allowed: false`. A recomendação **vira pergunta, não instrução**: "quanto você tem de custo fixo por mês?". Registre em `pending_inputs[]` e escreva isso no relatório.

Esses campos são o **contrato** com as skills `ad-analysis` e `scale-engine` (ver "Contrato de leitura" no fim). **Quando este arquivo existe**, nenhuma das duas emite corte de spend por queda de ROAS sem ler daqui — o veredito calculado aqui vence a heurística local delas. Quando não existe, elas caem no comportamento anterior: sem os custos fixos na mesa, a recomendação de corte vira pergunta ao membro (cânone `unit-economics` §4). A `finance-engine` **não é pré-requisito** de nenhuma skill; ela substitui uma pergunta por um número.
