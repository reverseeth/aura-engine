# Market Research · Referência: Regra de parada, validação final e fontes

> A regra dos 5 a 10 ad ideas como teto da pesquisa, os doze itens da validação final antes de salvar e a regra de que as fontes vivem só no `dados.json`. Abra antes de salvar.

### Regra de Parada — quando encerrar a pesquisa

A skill tem mínimo (35 frases de VOC) e precisa também de um teto, porque pesquisa é o lugar mais confortável do mundo pra procrastinar. O teto é o sistema **Regra dos 5–10 Ad Ideas** da base (rode `quando parar a research 5 a 10 boas ad ideas va testar blocos de uma hora` antes de decidir a parada): o teto é de resultado, não de relógio — **quando a pesquisa já produziu de 5 a 10 boas ideias de anúncio (os golden nuggets da rodada), pare e vá testar.**

- Na primeira passada, cubra todas as fontes (Amazon, Reddit, YouTube, comentários de TikTok) em blocos de aproximadamente uma hora, até o filão esgotar — o sinal de esgotamento é a thread parar de trazer coisa nova e os sub-avatares novos virarem variação dos que já existem.
- Acumular 100 ideias sem validação não é profundidade, é adiamento. Quem devolve a direção da próxima rodada é o teste: o ângulo que puxa spend diz qual sub-avatar tem mercado de verdade, e é dali que a pesquisa seguinte parte.
- Registre de onde veio cada ideia. Cada frase em `voc_evidence` leva o `id` estável (namespace `voc-NNN` da ETAPA 5) e o campo `source`, e cada label também leva `source`. Quando um anúncio vencer na Skill `ad-analysis`, essa marcação diz qual fonte de pesquisa produziu o vencedor — e é pra ela que a próxima rodada volta primeiro.
- Pesquisa não termina, ela pausa. A Skill `market-research` pode ser re-rodada a qualquer momento com o aprendizado dos testes na mão. Não tente esgotar o mercado antes de o primeiro anúncio existir.

### Validação Final

Antes de salvar, valide:
- [ ] Voice of Customer tem mínimo 35 frases EXATAS (não parafraseadas)
- [ ] `voc_top20` gravado no dados.json com id + rank + count + category (a Skill `copy-engine` lê esse campo direto)
- [ ] IDs de VOC estáveis: todo item de `voc_top20` e de `voc_evidence[]` tem `id` no formato `voc-NNN`, mesmo namespace; em re-execução, nenhum id de frase existente mudou (só append de frases novas)
- [ ] `core_avatar` gravado com UMA categoria dominante e o desejo em nível de superfície (cabe na frase "I want X")
- [ ] Cada item de `sub_avatars[]` combina 2+ das Core Five, tem pelo menos um desejo, traz demografia por último (só se refina) e carrega **um** `angle` em frase completa — a Skill `creative-engine` lê exatamente esse campo como persona/micro-persona de cada conceito
- [ ] `labels[]` gravado com os apelidos que o próprio mercado usa
- [ ] `market_vocabulary` gravado com contagem em `words_used[]` e os termos proibidos em `words_absent[]`
- [ ] A pesquisa produziu de 5 a 10 boas ideias de anúncio (regra de parada) — abaixo disso, aprofunde; acima, pare e vá testar
- [ ] Awareness distribution é numérica (não "a maioria é problem aware" — mas "45% problem aware, 30% solution aware")
- [ ] Sophistication stage tem claims saturados LISTADOS
- [ ] Cada objeção tem estratégia de quebra específica (não genérica)
- [ ] Recomendações finais são acionáveis (não "a copy deve ser emocional" — mas "lead com Story Lead sobre trigger event X, foco em desejo Y, mecanismo Z")

Se alguma validação falhar, aprofunde naquele ponto antes de salvar.

### Fontes (só no `dados.json`, nunca no relatório)

Grave em `dados.json.sources` a contagem de VOC por fonte (Amazon, Reddit, TikTok, Trustpilot, fóruns, survey, ligações) e a origem da distribuição de awareness (`user_estimate | default | hybrid | web_signals`). É informação de procedência pra AI das fases seguintes; o relatório `.md/.html` traz só o resultado (rule `report-only-results.md`).
