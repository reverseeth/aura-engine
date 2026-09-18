# Ad Strategy · Referência: Erros comuns a evitar (ETAPA 7)

> Os doze erros que a estrutura de teste existe para impedir, cada um com a razão. Abra na ETAPA 7 e ao montar o checklist do relatório.

### ETAPA 7 — Erros Comuns a Evitar

1. **NÃO subir mais conceitos do que a capacidade comporta** — `max_adsets = floor(budget ÷ (3 × target CPA))` e teto de 5 ad sets abaixo de US$ 1k/dia (cânone §1). Ad set que recebe menos que ~3× target CPA/dia devolve ruído, e ruído lido vira decisão errada.
2. **NÃO misturar conceitos dentro de um ad set** — 1 ad set = 1 conceito = 1 pack 3-2-2. Misturado, o gasto ainda acontece, mas a pergunta "qual conceito funcionou" fica sem resposta.
3. **NÃO usar detailed targeting / interests** — o criativo faz o targeting. Adicionar interest só encolhe o pool e limita o algoritmo.
4. **NÃO mexer antes de 3 dias** — cada mudança (budget, audiência, pausar criativo) reseta o sinal. Deixar rodar.
5. **NÃO usar daily MINIMUM** ("garantir $X de spend" por ad set) — força o Meta a gastar em impressão ruim pra bater meta. **Atenção pra não confundir:** o daily **maximum** da ETAPA 6 é obrigatório (é teto de proteção); o daily **minimum** continua proibido (é piso forçado). São coisas opostas.
6. **NÃO criar Automated Rule de performance** (kill ou escala por CPA/ROAS/frequency) — o Meta recusa em CBO, e mesmo onde aceitasse, decidir por metadado do Ads Manager mata winner (cânone §6). As únicas automações são as três da ETAPA 6.
7. **NÃO misturar 2 produtos numa conta** — embaralha o aprendizado. 1 conta por produto.
8. **NÃO inflar o budget "pra acelerar"** — acima do teto por ad set o dinheiro extra não compra leitura, só queima caixa. Budget maior serve pra rodar MAIS conceitos (mais ad sets), não pra empurrar os mesmos.
9. **NÃO escalar manualmente durante o teste** — escala é depois do breakthrough (Skill `scale-engine`, cânone §5).
10. **NÃO ler CTR como verdade** — CPA é o que manda; isso a Skill `ad-analysis` detalha. Aqui só não tome decisão de kill na base de CTR.
11. **NÃO re-decidir na `ad-strategy` o método que a `creative-engine` já gravou** — `concepts[].testing_method` manda: o pack foi CONSTRUÍDO naquele método (3 ângulos ou 3 execuções), e reclassificar aqui só desalinha a leitura da `ad-analysis`. A regra própria da 3.2 é fallback pra batch legado sem o campo.
12. **NÃO matar produto por calendário** — domingo é checkpoint de leitura (ETAPA 5): réguas do cânone §3 + checks de precedência da `ad-analysis` + Execution Problem (falhou o ângulo ou a execução?), e kill de PRODUTO só com ≥ 2 batches de learnings processados ou régua do cânone mandando. Data sozinha não decide nada.
