# Ad Strategy · Referência: Mensagem final

> O texto integral da mensagem final, apresentada como draft pronto para revisão, com a conta de capacidade explicada, o plano de teste, o checkpoint de domingo e o handoff para a `ad-analysis`. Abra ao encerrar.

## Mensagem Final

Apresentar como **draft pronto pra revisão** (`.claude/rules/iteration-driven-refinement.md`), não como "pronto, pode escalar":

"Estrutura de teste montada: campanha `[nome]` com o budget de **$[test_budget_daily]/dia no nível da campanha**, dividido entre **[N] ad sets broad/Advantage+ — um por conceito** ([lista]), cada um com 3 criativos, 2 textos e 2 headlines, otimizando pra Purchase[, e cada conceito apontando pra página do nível de consciência dele, se os destinos diferem] ([se MCP] já criada em **PAUSED** na sua conta — revisa e ativa).

Por que [N] conceitos e não mais: com CPA alvo de **$[target_cpa]** e **$[budget]/dia**, esse budget consegue LER [max_assets] criativos ([N] conceitos). Cada criativo precisa de mais ou menos 1 CPA por dia pra acumular dado suficiente — abaixo disso o número que aparece no painel é ruído, e decisão em cima de ruído custa caro. [Se sobrou conceito: Os outros [X] conceitos ficam pro próximo batch.] [Se alguma restrição mordeu: explicar qual em uma frase.]

Plano de teste: [se conta nova: 3 dias de warmup de engajamento primeiro, depois] lançar **quarta**, deixar até **domingo**, **3 dias sem mexer**. Domingo é o nosso **checkpoint de decisão**: eu rodo a leitura da `ad-analysis` e a gente decide com dado na mesa — ad set que passou 7 dias sem gasto e sem resultado morre pela régua; ângulo que ainda tem tentativa sobrando itera no batch seguinte (antes de descartar qualquer ângulo, eu confiro se a falha foi dele ou da execução — o mesmo ângulo tem direito a 3 tentativas). Matar o PRODUTO só entra na conversa depois de pelo menos 2 batches com os aprendizados aplicados, ou antes disso se as réguas mandarem — nunca só porque o calendário virou. O checkpoint continua servindo pro mesmo propósito de sempre: impedir que você queime caixa em produto morto. Quem declara o óbito passa a ser a leitura, e ela é honesta nos dois sentidos.

Quando ativar e passarem **3 dias**, diga **'ad analysis'** e me manda os dados (ou eu puxo via MCP) — aí a `ad-analysis` lê CPA por conceito e por criativo, CPM da conta e os benchmarks de funil pra decidir o que mantém, o que mata e o que está pronto pra escalar. Kill e escala são leitura dela: eu não deixo nenhuma regra automática decidindo isso por você.

Antes de ativar: confere a credibilidade da loja (reviews, comentários dos posts) — [resumo dos gaps da ETAPA 2, se houver]. Quer que eu ajuste algo na estrutura — budget, número de criativos, mercado?"
