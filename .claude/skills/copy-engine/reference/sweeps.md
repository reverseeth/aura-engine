# Copy Engine · Referência: Auto-revisão, os 9 sweeps (ETAPA 6)

> Os sistemas de edição que calibram os sweeps, os sweeps 1 a 8 com o gate de VOC (60%), o gate de vocabulário, o em-dash check acionável, a dieta de copy (4.5) com o teste do pilar e o sweep de força, e o markup audit (sweep 9) com o gate de entrada, a regra de veredito, as camadas de auditoria, o loop de body copy, a folha de defeitos e o output. Abra na ETAPA 6.

### ETAPA 6 — Auto-Revisão (9 sweeps: 8 de revisão + markup audit)

Antes de entregar, faça os **8 sweeps de revisão** abaixo (1 a 8, com o 4.5 de dieta de copy no meio) — são os sweeps DESTA skill, não os "7 sweeps" clássicos de copywriting. O **markup audit (sweep 9)** roda em seguida como auditoria estrutural. Nenhum sweep suaviza claim, insere aviso ou troca palavra por "risco": a revisão deixa a copy mais forte e mais específica, nunca mais tímida (rule 8b do CLAUDE.md).

Pra calibrar o que cada sweep procura, puxe os sistemas de edição (rode cada `best_query`):
- **Seven Sweeps (Editing Ladder)** (rode `Seven Sweeps editing ladder clarity voice tone so what prove it specificity heightened emotion zero risk`) — o ladder canônico que inspira estes sweeps
- **Hopkins' Specificity Principle** (rode `Hopkins specificity principle reason-why platitudes generalities specific claims transformation`) — pro Specificity sweep (#3)
- **Mona Lisa Frame (show, don't tell)** (rode `Mona Lisa Frame show dont tell placa embaixo do quadro half the words double the examples`) — também pro Specificity sweep (#3): mostrar em vez de afirmar — metade das palavras, o dobro dos exemplos
- **Sugarman's Slippery Slide** (rode `Sugarman slippery slide every element read the next sentence frictionless`) — pro Flow sweep (#4)
- **5 Alavancas de Stakes** (rode `5 alavancas de stakes bigger witnesses urgent permanent cost more revisao`) — passada de revisão que eleva o que está em jogo (maior / testemunhas / urgente / permanente / custo); aplicar onde a peça está morna
- **Checklist do Copywriter (`retention-engine` checagens)** (rode `checklist de revisao do copywriter 13 checagens sanity check onde posso dramatizar`) — o sanity check final da peça inteira, rodado DEPOIS dos sweeps 1-7 (inclui o "onde ainda dá pra dramatizar?")
- **Reeves' USP + Vampire Claims** (rode `Reeves USP burning glass vampire claims mosaic structure single proposition unrelated claims`) — pro Originality sweep (#7), pra não cair em claim saturado/genérico:

1. **Clarity sweep**: cada frase é clara em primeira leitura? Jargão sem explicação?
2. **Customer voice sweep (cobertura de VOC)**: checklist dinâmico — passe o `voc_checklist` como lista. Para cada frase VOC:
   - [ ] Aparece LITERAL no copy? (marca se sim)
   - [ ] Aparece parafraseada? (marca se só aproximação)
   - [ ] Ausente? (marca como gap)

   Taxa mínima: >= 60% das top-20 VOC phrases presentes literais ou parafraseadas. Se < 60%, regerar seções fracas.

   **Gate de vocabulário (contrato com `market_vocabulary` da `market-research`) — roda no mesmo sweep:**
   - Ctrl+F em CADA termo de `market_vocabulary.words_absent[]`: qualquer ocorrência na copy é **PROIBIDA** — a pesquisa provou que o mercado não fala assim. Substitua pelo `market_says_instead` do próprio campo e re-cheque.
   - CADA termo com `saturated_in_market: true` NÃO pode aparecer em headline (nas variações da ETAPA 3 nem em crosshead que faz papel de headline) — mensagem fatigada serve só como prova no corpo. Se apareceu, reescreva a headline.
   - `labels[]` são matéria-prima de call-out: se a `market-research` coletou labels e NENHUM aparece na peça (call-out, kicker, bullets), corrija ou justifique no relatório do sweep.
   - FALLBACK legado: sem `market_vocabulary` no dados.json da `market-research`, o gate roda só com o checklist VOC acima — e a Mensagem Final recomenda re-rodar a `market-research`.
3. **Specificity sweep**: Hopkins — cada claim genérico foi substituído por específico? ("many customers" → "12,847 customers"; "fast results" → "visible improvement in 14 days")
4. **Flow sweep**: slippery slide de Sugarman — cada frase compele a próxima? Onde há quebra de fluxo?
   - **Em-dash check (rule 8a, ACIONÁVEL):** conte os travessões (—) por peça. Se `em_dash_count > 0` em QUALQUER headline OU `> 2` em copy longa → **REESCREVER** os trechos afetados substituindo o travessão por ponto, vírgula, parênteses, duas frases curtas, ou dois-pontos, e **re-checar** a contagem depois. Não basta medir: o sweep só passa quando headlines têm zero travessão e a copy longa tem ≤2.
4.5. **Dieta de copy (extensão sob controle)**: conte as palavras da página inteira e por seção. A força da copy vem da PROVA, não do volume — o Length-Implies-Strength continua valendo pra prova, specificity e VOC (isso NUNCA se corta). O que a dieta corta é o resto: a mesma ideia dita duas vezes em seções diferentes, adjetivo que não muda a decisão de compra, parágrafo de transição que não move a leitura, benefício reafirmado pela terceira vez sem prova nova. Processo:
   - Se a página passou do teto da categoria (PDP/landing: ~1.800 palavras é sinal de alerta; advertorial aguenta mais) OU o membro pediu "menos texto": monte a proposta de corte — percentual alvo (ex: reduzir ~25-30%) + cortes estruturais (seções que dizem a mesma coisa e podem fundir) — e mostre AO MEMBRO antes de aplicar, com o word count atual e o projetado. Extensão é decisão estratégica; dieta nunca é silenciosa.
   - Ao aplicar, teste frase a frase: cortar esta frase leva junto alguma prova, VOC literal ou claim único? Se sim, a frase fica (ou a prova migra pra outra seção antes do corte).
   - **Teste do pilar (da ETAPA 2.5C):** antes de cortar um bloco por "já foi dito", cheque qual pilar ele reforça e com que prova. Repetição de pilar **com prova nova** não é redundância — é a arquitetura de copy longa (ver `arquitetura_de_extensao` em `.claude/lib/swipe-models/specimens.json`). Só corte quando o pilar voltar sem trazer prova ou ângulo que as voltas anteriores não trouxeram.
   - Depois do corte, re-rode os sweeps 2 (a taxa de VOC continua ≥ 60%?) e 4 (o fluxo continua deslizando sem os conectivos removidos?).
5. **Objection sweep**: cada objeção do market research foi quebrada em algum lugar? Onde está omitida?
6. **CTA sweep**: CTAs são call to VALUE? Aparecem em frequência certa (não muito, não pouco)?
7. **Originality sweep**: comparar com os claims saturados do competitor analysis — onde estou usando um claim saturado? substitua por ângulo original.
8. **Sweep de força (o inverso de suavizar)**: releia cada claim forte e pergunte "dá pra dizer com mais força e mais específico, com a prova ao lado?". Claim hedged ("may help", "designed to support") vira claim direto com número, mecanismo ou depoimento ao lado. Nenhum aviso, asterisco ou disclaimer entra por iniciativa da skill (rule 8b do CLAUDE.md).

9. **Markup audit sweep (método Kyle Milligan)** — auditoria estrutural da peça, rodada DEPOIS dos sweeps 1-8:

   Leia o nó `auditoria` de `.claude/lib/swipe-models/specimens.json` (e, se precisar do detalhe, rode `auditoria markup promo codigo de cores lexico de blocos objection claim proof benefit`). Audite a copy gerada em 5 camadas:

   **Gate de entrada (roda primeiro, é bloqueante):**
   - Teste dos **4 U's** na headline escolhida: Urgent / Useful / Unique / Ultra-Specific — marque passa/reprova em cada um.
   - **Ideal Prospect** e **Big Promise** presentes no lead?
   - Distinção obrigatória: **fato do mundo não é promessa.** "X causa Y" é fato — o leitor não tem o que fazer com ele. Promessa é uma transação: o que ele ganha, em troca do quê. Se o lead abre com fato, ele reprova em Big Promise mesmo que a afirmação seja verdadeira e interessante.
   - **Regra de veredito:** se reprova em 3 dos 4 U's **e** falha em Ideal Prospect ou Big Promise → **não audite o corpo. Reescreva o lead e volte à ETAPA 3.** Auditar corpo de peça que morreu na abertura é desperdício.
   - **Teste da primeira página:** o lead inteiro precisa poder ser rotulado nos três frames (4 U's + 4 emoções + os 4 passos do Makepeace) **dentro da primeira tela/página**. Se algum frame só se resolve depois, o lead está diluído.

   **Camadas de auditoria (documente bloco a bloco)** — as 4 grades na ordem fixa vêm da base: rode `quatro grades auditoria 4 U's lead Makepeace checklist desejabilidade Beats body copy formula`:
   - **Estrutura** — a sequência de blocos bate com o `specimen_block_map` da ETAPA 2.5? Onde divergiu, foi decisão ou descuido?
   - **4 emoções** — New/Only · Safe/Predictable · Easy/Anybody · Big/Fast: marque onde cada uma é ativada. Emoção sem nenhuma ocorrência na peça é buraco.
   - **Lead de 4 passos** — grab eyeballs / expand HL / establish cred / bribe, em ordem. Nota: `cred` **não precisa vir primeiro** — no espécime control auditado, o porta-voz só se apresenta a 40% da peça, e passa; o que não pode é faltar.
   - **Psicologia** — secret knowledge, sense of power, future pacing, WIIFM. O WIIFM tem que estar respondido **antes** da primeira prova, não depois.
   - **Oferta/preço** — a escada `extreme anchor → step down → price anchor → true price` está montada? A adesão é escrita como pertencimento ou como transação? ("subscribe"/"assine" é transação; "faça parte" é pertencimento.)

   **Loop de body copy** — rastreie `Objection → Claim → Proof (3x) → Benefit` parágrafo a parágrafo. O ciclo roda dezenas de vezes numa peça longa, não uma vez por seção. Onde houver Claim sem Proof adjacente, marque.

   **Folha de defeitos** — varra os 12 defeitos catalogados no JSON (o método de rotulagem por camadas + as 12 críticas recorrentes: rode `auditoria com caneta camadas de rotulagem too vague too big too early move to end`). Os que mais aparecem em copy gerada por AI: *too vague*, *lazy copy / obligatory* (bloco escrito por obrigação), *old proof* (prova reciclada), *reads like editorial* (falta WIIFM), *vende a categoria e não o ativo* (prova pertence ao ingrediente/estudo, não ao seu produto), e **prova em ordem decrescente** (número grande antes do pequeno faz o segundo encolher — "too big too early").

   **Output do sweep:** tabela de arco (bloco → camada auditada → veredito → correção aplicada). As correções são aplicadas na hora; o que não puder ser corrigido sem novo research entra na Mensagem Final como recomendação.

Para cada sweep, documente o que mudou (as edits são o output do sweep).
