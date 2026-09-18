# Marketplace Engine · Referência: O gate de expansão (ETAPA 1)

> A regra de não abrir canal que não se domina, as duas condições do gate, a tabela dos quatro sinais de demanda transbordando na ordem de força, o anti-sinal que bloqueia sozinho e o timing por faixa de faturamento. Abra na ETAPA 1.

### ETAPA 1 — O gate de expansão (a decisão que vem antes de toda tática)

Canal secundário é agenda de quem já provou o canal primário. A regra da fonte primária é direta: **não abra canal que você não domina enquanto ainda há espaço no Meta** — antes de escala real, multi-canal é ruído, e um canal bem feito vale mais que três pela metade.

**Condição 1 — Meta + site provados.** Pelo menos um `breakthrough` classificado pela `ad-analysis` (cânone `.claude/lib/ad-taxonomy/README.md` §2) OU mês fechado saudável na `finance-engine` (margem de contribuição cobrindo os fixos). Sem prova, o veredito é `blocked_pending_proof` e o relatório diz exatamente o que destrava.

**Condição 2 — sinal de demanda transbordando.** O canal secundário certo captura demanda que o canal primário já criou e não está convertendo. Os quatro sinais, na ordem de força:

| Sinal | Como ler |
|---|---|
| **Busca de marca subindo** | Gente pesquisando o NOME da marca no Google/TikTok é demanda que o ad criou. Se ela cresce, parte dela está indo comprar onde você não está. É o mesmo sinal que sustenta a campanha de busca de marca (Google Search Stronghold) — quando ele fica forte, marketplace é o próximo lugar onde essa demanda vaza. |
| **Cliente perguntando pelo canal** | Comentário e DM do tipo "tem na Amazon?" é o transbordo dito com todas as letras. |
| **Revendedor ou sequestro de listagem** | Alguém já vende seu produto na Amazon sem você. Além de sinal de demanda, é urgência de defesa (ETAPA 2). |
| **Lift cruzado observado** | Quem já tem um segundo canal vê o efeito: anúncio num canal eleva venda no outro. Ads de TikTok Shop elevam vendas na Amazon; marca com varejo físico vê o varejo subir por dólar gasto no TikTok Shop. |

**Anti-sinal (bloqueia sozinho):** abrir canal novo pra **fugir** de CAC ruim, criativo cansado ou oferta que não converte no Meta. Canal novo herda a oferta — não a conserta. Se o motivo declarado do membro é esse, o veredito é `not_yet` com o encaminhamento certo (`ad-analysis` pra diagnóstico, 04 pra oferta, 15 pra conta).

**Timing por referência de faixa:** operadores em escala colocam a entrada na Amazon tipicamente entre o DTC validado e a faixa de US$ 1-3M/mês — e o arrependimento mais comum relatado é ter aberto **tarde**, porque com volume no DTC a busca orgânica da marca na Amazon já performa sem anúncio (margem quase pura sendo perdida todo mês). O sinal que manda é a busca de marca, não a receita em si.

Grave `gate.verdict` (`expand` / `not_yet` / `blocked_pending_proof`) e os sinais marcados. Só `expand` libera as ETAPAs 2-4 como avaliação de entrada; com `not_yet`, as etapas seguintes só rodam para canais JÁ abertos (atualização de status).
