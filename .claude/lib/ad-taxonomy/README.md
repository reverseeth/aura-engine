# Ad Taxonomy — cânone único de classificação e capacidade de teste

Fonte de verdade para: quantos criativos testar, como classificar resultado, quando matar e quando escalar. Skills 08, 10, 11, 12, 14 e 17 leem **daqui**; nenhuma redefine essas classes localmente.

Origem: fonte primária 2026 (P1) + fonte primária high-ticket 2026 (P1), revisão de ~US$ 100M de spend. Queries: `taxonomia winners breakthrough spend winner KPI winner loser`, `assets budget dividido por CPA capacidade de teste`, `scaling protocol reset budget gasto real`.

## 1. Capacidade de teste (resolve antes de escolher criativo)

```
nº de assets testáveis = budget diário ÷ target CPA
```

US$ 160/dia com CPA alvo de US$ 80 = **2 assets**. Não 5, não 12. Criativo que recebe menos de ~1× CPA/dia não acumula dado suficiente para ser lido — o teste produz ruído com aparência de resultado.

- **Piso operacional:** US$ 100–150/dia. Abaixo disso não há teste, há palpite.
- **Teto por ad set:** ~3× target CPA/dia.
- **Teto de ad sets de teste:** 5, abaixo de US$ 1k/dia.
- **Estrutura:** CBO no nível da campanha; **1 ad set = 1 conceito** (3 criativos + 2 copies + 2 headlines).

## 2. As 4 classes de resultado

| Classe | Definição | Destino |
|---|---|---|
| **Loser** | ≤2% do spend da conta em 7 dias ("não fez nada pela conta") | Graveyard / zombie campaign |
| **KPI winner** | bate o KPI mas **não puxa spend** | **Tratar como loser para decisão** — não escala, não recicla |
| **Spend winner** | puxa spend mas KPI abaixo do da campanha | Iterar, não escalar |
| **Breakthrough** | **KPI do AD melhor que o KPI da CAMPANHA** *e* puxa spend | Escala + reciclagem |

> A distinção que o sistema errava: **ad que bate KPI com pouco spend não é winner.** Ele não provou nada em escala — o KPI bonito veio de amostra pequena. Só `breakthrough` libera escala e reciclagem.
>
> E o espelho dessa distinção: **ad que puxa spend sem bater KPI é `spend_winner`, nunca loser** — o destino dele é iteração (autópsia do que o algoritmo gostou), não a lixeira. A única régua em que "gastou sem vender" mata é o 8× de conta nova (§3). Classificar spend winner como loser joga fora exatamente o sinal mais caro do teste.

**Benchmarks:** super winner absorve 30–40% do spend; hit rate esperado de super winner é **1–3%** dos criativos testados.

## 3. Réguas de kill

| Situação | Régua |
|---|---|
| Conta madura | kill no nível do **ad set** após 7 dias sem spend e sem KPI |
| Conta nova | **8× target CPA** sem purchase |
| Ad novo overspendando | esperar **24–48h** antes de decidir |

Não existe régua "1–2× breakeven CPA sem venda" no material — a única régua de gasto-sem-purchase que mata é o 8× de conta nova. *(Nota de proveniência: o número a seguir é derivação estatística NOSSA, não régua do curso — a 1× CPA, até um ad saudável tem ~37% de chance de zero vendas por puro acaso [Poisson, e⁻¹]. O curso chega à mesma conclusão pelo caminho prático: "amostra pequena demais pra qualquer decisão".)* Matar ali descarta criativo bom por ruído.

## 4. Hook e Hold (diagnóstico de onde o criativo falhou)

```
Hook rate = 3-sec plays ÷ impressões
Hold rate = ThruPlays ÷ impressões
```

| Métrica | Ok | Bom | Muito bom | Excepcional |
|---|---|---|---|---|
| Hook | 21% | 30% | 40% | 50%+ |
| Hold | >5% | >10% | >15% | — |

Hook baixo = problema de abertura (3 primeiros segundos). Hook bom com Hold baixo = a promessa não sustentou. Sem essas duas, "o criativo não funcionou" não é diagnóstico.

## 5. Escala

- **ABO paralelo:** cada breakthrough ganha **1 ad set próprio** em campanha ABO, começando a **~10% do budget diário** da campanha principal. Mantém o ad original no CBO. Motivo: winner novo rouba spend do antigo dentro do CBO; o ABO garante continuidade do que já provou escalar.
- **Champions ad set:** aposentado na abordagem vigente, substituído pelo ABO acima.
- **Scaling protocol:** 48–72h acima do target → **+20%**, depois a cada 24h. Abaixo do breakeven **por 24–48h persistentes** → **−20%** (um dia ruim isolado não dispara descida).
- **Gate click-based:** só escale se ≥60% das purchases aparecem em 7-day click **OU** se o ROAS calculado só com purchases click-based já bate o KPI sozinho (as duas portas são da fonte; qualquer uma libera).
- **Exceções do protocolo (da fonte, valem sobre os degraus):** (a) **promo com data-fim** entra direto no budget planejado da promo — não sobe em degraus de +20%, porque a janela termina antes de os degraus chegarem lá (o que protege a promo é o surf + reset da meia-noite, não o protocolo); (b) **"new reason to be scaling"** — oferta nova, breakthrough novo, sazonalidade que mudou a demanda — reinicia a leitura: o histórico anterior de degraus não trava o passo novo.

> **REGRA DE RESET (crítica, risco financeiro):** ao ajustar budget à meia-noite, o novo valor é **~50% do que foi REALMENTE gasto**, nunca do budget nominal. Sem isso o Meta faz pacing para gastar o nominal inteiro no dia seguinte, e a escala vira queima de caixa.

Antes de qualquer decisão de cortar spend por queda de ROAS, aplique `.claude/lib/unit-economics/README.md` §4 — cortar pode aumentar o prejuízo.

## 6. Automações

- **PGS com condição de performance é impossível em CBO** — o Meta retorna *"performance-related conditions are not available for assets that use CBO"*. O substituto é `ad set spending limit → daily maximum`.
- **Duas automações de proteção obrigatórias:** (a) spend 5× em 24h → pausar; (b) URL de destino ≠ domínio esperado → desligar.
- Nunca automatizar **kill por métrica de performance**: a métrica do Ads Manager engana (ad a 1× ROAS na plataforma pode estar excelente no 1-day click de terceiro).

## 7. Métodos de teste

| Método | Quando | Como |
|---|---|---|
| **Marksman** | primeiro teste, ou quando a performance platôa | **3 ângulos diferentes DENTRO de um único pack 3:2:2** — as 3 variações do mesmo conceito carregam ângulos distintos |
| **Sniper** | depois que um ângulo mostra tração | **1 ângulo, 3 execuções** dentro do pack (hooks/headlines/formatos diferentes) — e toda **iteração** é Sniper |
| **Shotgun** | só no pipeline de conteúdo de creators | volume sem estratégia individual; aplica-se Marksman/Sniper por cima quando algo cola |

> **Marksman acontece DENTRO de um ad set, não entre ad sets.** O material é literal: *"Marksman (rajada de 3 tiros — testa 3 angles diferentes num único 3:2:2)"*. Exemplo real: conceito "superlatives" → variação 1 "world's first stainless steel", variação 2 "world's easiest to clean", variação 3 "world's first doctor-designed". O **conceito é a embalagem** e permanece um só (= 1 ad set); o que varia entre as 3 execuções é o ângulo. Espalhar os 3 ângulos em 3 ad sets é outra coisa, e não é Marksman.

**Sequência oficial:** Marksman (achar direção) → Sniper (extrair o máximo do ângulo vencedor) → Marksman de novo quando a performance platôa e o ângulo já foi "snipado".

Trade-off declarado de cada um: Marksman cobre mais terreno por teste, mas cada ângulo recebe só 1 execução — a falha pode ter sido a execução, não o ângulo. Sniper valida o ângulo de verdade e elimina o "execution problem", mas é lento e tem risco de *iteration overload*.

Regra prática: imagens → Marksman; vídeos → Sniper; **toda iteração → Sniper**.

**Shotgun tem escopo estreito:** só é legítimo no pipeline de conteúdo de creators (product seeding), onde chega volume sem estratégia individual. Como estratégia criativa deliberada não se usa — pós-Andromeda, micro-iterações de hook são invisíveis para o algoritmo.

**Volume de referência:** agência de 5 pessoas = ~15 conceitos/semana. Solo ou time pequeno = **1 conceito por dia** — foi o ritmo dos dois operadores do material que bateram US$ 100k/dia. Volume certo é função de manpower e intenção, não de spam.

**Ângulo ≠ conceito.** Ângulo é a razão de compra em frase ("para de virar de um lado pro outro a noite toda"). Conceito é a embalagem (comparação, depoimento, autoridade). Skill que pede "escolha o ângulo" e oferece uma lista de formatos está pedindo conceito.
