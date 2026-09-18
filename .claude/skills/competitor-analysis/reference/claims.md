# Competitor Analysis · Referência: Claims compilation completa e matriz de saturação (ETAPA 4)

> Os dois sistemas a puxar, os quatro tipos de claim com exemplos, a classificação em SATURADO, COMUM, RARO e AUSENTE, a tabela e a matriz Claims Saturation com a regra de conversão por percentual. Abra na ETAPA 4.

### ETAPA 4 — Claims Compilation Completa

**Frameworks a puxar da base ANTES de classificar (rode cada `best_query`):**
- **The Preemptive Claim (Schlitz / Live Steam)** (rode `preemptive claim Hopkins Schlitz live steam own common claim first to say`) — um claim COMUM (não único) que ninguém ainda CRAVOU como dono pode virar oportunidade forte se você for o primeiro a explicá-lo. Aplique ao classificar claims COMUM/RARO: existe claim que todos têm mas ninguém "possui"?
- **Schwartz Market Sophistication — 5 Stages** (rode `market sophistication five stages Schwartz enlarge claim new mechanism identity skepticism`) — a saturação de claims é o sintoma direto do stage de sofisticação. Stage 3-5 exige mecanismo novo/identidade, não claim ampliado.

Compile TODOS os claims que os concorrentes fazem, classificados por tipo:

**Claims diretos** (promessa de resultado):
- "Reduz rugas em 30 dias"
- "Resultados visíveis em 1 semana"
- "Perde 5kg em 30 dias"

**Claims de mecanismo** (como funciona):
- "Tecnologia de micro-corrente"
- "Infusão de ácido hialurônico"
- "Fórmula com peptídeos patenteada"

**Claims de autoridade** (credencial):
- "Recomendado por dermatologistas"
- "Aprovado pela FDA"
- "Desenvolvido por cientistas de Harvard"

**Claims de prova social** (evidência):
- "50.000+ clientes satisfeitas"
- "4.8 estrelas em 12.000 reviews"
- "Featured in Forbes, Vogue, NYT"

**Classifique cada claim:**

| Classificação | Significado | Ação |
|---|---|---|
| **SATURADO** | Todos ou quase todos usam | EVITAR — o público não acredita mais |
| **COMUM** | Maioria usa | USAR com twist próprio (especificidade de Hopkins) |
| **RARO** | Poucos usam | OPORTUNIDADE — diferenciação moderada |
| **AUSENTE** | Ninguém usa | OPORTUNIDADE FORTE — diferenciação máxima |

Apresente em tabela:

| Claim | Categoria | Quantos usam | Classificação | Ação |
|---|---|---|---|---|

**Claims Saturation matrix (output obrigatório)**: além da tabela acima, gere uma matriz enxuta focada em saturação — usada pelas skills `offer-builder` e `copy-engine` para escolher/evitar claims:

```
## Claims Saturation
| Claim | # Concorrentes usando | Saturação |
|-------|----------------------|-----------|
| "Clinically proven"   | 9/10 | ALTA — evitar |
| "30-day results"      | 4/10 | MÉDIA — usar com twist |
| "Doctor-formulated"   | 2/10 | BAIXA — oportunidade |
```

Regra de conversão: ≥70% dos concorrentes → ALTA / evitar; 30-69% → MÉDIA / usar com twist; < 30% → BAIXA / oportunidade; 0% → AUSENTE / oportunidade forte (destaque).
