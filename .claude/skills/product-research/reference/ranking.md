# Product Research · Referência: Ranking final pelos eixos de score (ETAPA 7)

> O cabeçalho com timestamp e fórmula, a definição literal de cada sub-score, a tabela do ranking, os dois cross-checks pela query exata, a validação de mínimo bloqueadora e o bloco por oportunidade com o veredicto. Abra na ETAPA 7.

### ETAPA 7 — Ranking Final (eixos de score)

Inclua no topo do output desta etapa:

```
Ranking Generated at: YYYY-MM-DDTHH:MM:SSZ   (ISO-8601 UTC)
Formula:
  Total = (Magnitude × 2 + Sophistication × 2 + AwarenessFit + UMPotential + AvatarFit + OfferPotential + CreativePotential + TrendFit) / 10
  — Magnitude e Sophistication pesam 2× (filtros mais decisivos).
  — Todos os sub-scores são 1-10 inteiros ou com 1 casa.
  — Min aceitável pra TESTAR: ≥ 7.5. Min aceitável pra TALVEZ: 6.0-7.4. Abaixo de 6.0 → DESCARTA.
```

O objeto rankeado é a **oportunidade**: a marca finalista **com a sua melhor jogada** (ETAPA 6). Uma marca pode aparecer duas vezes se duas jogadas dela forem realmente distintas.

**Definição de cada sub-score (use literalmente):**

- **Magnitude** (ETAPA 5.1): FRACO = 2-3 · MÉDIO = 5-7 · FORTE = 8-10.
- **Sophistication** = FACILIDADE de diferenciação dado o estágio (sentido INVERTIDO): Stage 1-2 = 9-10 · Stage 3 = 6-7 · Stage 4 = 4-5 · Stage 5 = 2-3.
- **AwarenessFit** = quão bem o funil viável bate com a distribuição dominante (ETAPA 5.2) e o budget do membro: Most/Product Aware (PDP direta) = 8-10 · Solution Aware (landing com mecanismo) = 6-7 · Problem Aware (advertorial, TAM maior, conversão mais cara) = 4-6 · Unaware = 2-3.
- **UMPotential** = média S.I.N. (Simple / Intuitive / New, 1-10 cada) do mecanismo da jogada, **ajustado pelo padrão de recombinação**: padrão 1 ou 2 (duas pontas validadas) fica no topo da faixa; padrão 3 (troca) no meio; padrão 4 (aprimoramento) no topo se o aprimoramento for específico e demonstrável, senão no meio.
- **AvatarFit** = força do avatar underserved (ETAPA 5.5): segmento ignorado claro e alcançável = alto; todos já falam com o mesmo público sem brecha = baixo.
- **OfferPotential** = stack/bundle/bump e AOV projetado (ETAPA 5.6).
- **CreativePotential** = ângulos abertos + demonstrabilidade + viabilidade de UGC (ETAPA 5.7).
- **TrendFit** (cenário da ETAPA 2 → número): problema SUBINDO + ingrediente ESTÁVEL ou SUBINDO 6+ meses = 9-10 · ESTÁVEL + ESTÁVEL = 6 · problema SUBINDO + ingrediente em PICO RECENTE = 5 (a jogada precisa ser padrão 3 ou 4) · HYPE (subida vertical 1-3 meses) = 4 · QUEDA de 12+ meses em qualquer termo = a marca já foi eliminada antes do ranking.

Tabela do ranking:

| # | Marca (oportunidade) | Jogada recomendada | Magnitude | Awareness | Sophist. | UM | Avatar | Offer | Creative | Trend | **Total** | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Apresente o cálculo numericamente pra pelo menos o Top 3.

> **Cross-check do Top 3 com o sistema de validação final** (rode `final validation Gemini GPT Perplexity Kimi rank products scale potential unique mechanism`): o **AI Final-Validation Ranking** cruza potencial de escala × mecanismo único — use os critérios dele pra confirmar que a #1 tem escala E diferenciação, não só um dos dois.

> **Segundo cross-check — template de go/no-go** (rode `avaliar produto magnitude de desejo awareness 1 a 5 competition 1 a 5 go no go`): o **Product Evaluation Framework (Desire × Awareness × Sophistication)** em notas de 1 a 5. Rode pro Top 3; se o go/no-go divergir do veredicto, re-examine o score antes de cravar.

**Validação de mínimo (bloqueadora):** se NENHUMA oportunidade atingiu ≥ 6.0, **NÃO** declare "research completo". Liste por que cada uma falhou (o filtro ou score dominante), volte ao TrendTrack com o filtro de nicho ajustado (sub-nicho vizinho, ou o mesmo nicho com `Growth rank` em `last30d`) e repita a partir da ETAPA 0.5 até haver pelo menos 1 TESTAR — ou o membro optar por parar.

Pra CADA oportunidade do ranking:

**[Marca → Jogada] — Score: X.X/10 — Veredicto: TESTAR / TALVEZ / DESCARTAR**

- **O que fazer diferente** (a jogada em 2-4 frases, com os elementos e as marcas de origem)
- **Por que tem potencial** (o texto corrido da ETAPA 6)
- **3 riscos principais** (com o que fazer sobre cada um)
- **Nível de dificuldade**: FÁCIL / MÉDIO / DIFÍCIL (sophistication stage + budget do membro)

Veredicto: **TESTAR** ≥ 7.5 e sem eliminação em Trends/Trustpilot · **TALVEZ** 6.0-7.4 · **DESCARTAR** < 6.0.
