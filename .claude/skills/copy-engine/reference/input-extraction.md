# Copy Engine · Referência: Input Extraction, as oito variáveis carregadas antes de escrever

> As oito variáveis lidas direto dos `dados.json` das fases anteriores (`dominant_awareness`, `sophistication`, `voc_checklist`, `mechanism`, `guarantee` e `offer_stack`, `core_avatar` e `sub_avatars[]`, `labels[]`, `market_vocabulary`), com a regra de não recomputar o que já foi decidido e o fallback para produto legado. Abra logo depois do pré-flight.

### Input Extraction (automático)
Antes de gerar copy, carregue:
1. `dominant_awareness` = ler DIRETO o campo `dominant_awareness` de `market-research/dados.json` (a Skill `market-research` já grava esse campo decidido, com nuance de fonte). Só recompute a partir de `awareness_distribution` (stage com maior %) como FALLBACK se o campo faltar (produto legado) — recomputar quando o campo existe abre porta pra drift em distribuições apertadas. Se `dominant_awareness_secondary` presente (empate ±5pp na `market-research`), trate como híbrido: escolha um lead que sirva os DOIS níveis (ex: empate problem/solution → lead de mecanismo com abertura de problema), não só o primário
2. `sophistication` = `sophistication_stage` (1-5)
3. `voc_checklist` = ler DIRETO o campo `voc_top20` de `market-research/dados.json` (a Skill `market-research` já grava as 20 frases curadas com rank + contagem de menções — use na ordem do rank, a frequência real vale mais que re-curadoria). FALLBACK (produto legado sem `voc_top20`): achate os 3 pools de `voc_phrases` — `{problem, desire, frustration}` — num único array e selecione as 20 mais repetidas antes do substring matching. VOC permanece SEMPRE no inglês original do consumidor.
4. `mechanism` = objeto do `offer-builder/dados.json` (use `mechanism.name` pro nome; não tratar como string)
5. `guarantee` + `offer_stack` = do `offer-builder/dados.json`
6. `core_avatar` + `sub_avatars[]` = ler DIRETO de `market-research/dados.json` — a camada ACIONÁVEL de avatar da `market-research` (não confundir com o objeto descritivo `avatar`). `core_avatar` define a quem a PÁGINA inteira se dirige: `surface_desire` é a promessa no nível "I want X", `core_desire_behind` orienta o TOM. **O lead fala com UM sub-avatar — o da estratégia escolhida na ETAPA 2** (o de `angle` mais próximo do ângulo principal), nunca com "todos ao mesmo tempo".
7. `labels[]` = os apelidos com que o próprio mercado se nomeia — **matéria-prima de call-out** (headline, kicker/eyebrow, bullets). Usar o label literal gera identificação imediata.
8. `market_vocabulary` = as palavras permitidas e proibidas da `market-research`: `words_used[]` (com flag `saturated_in_market`) e `words_absent[]` (com o substituto `market_says_instead`). Consulte ANTES de escrever qualquer linha — alimenta o gate de vocabulário do sweep 2.

FALLBACK (produto legado sem os campos 6-8 — a `market-research` rodou antes de eles existirem): derive o foco do objeto `avatar` (psychographics + pain/desire hierarchy) e do `voc_top20`, escreva sem o gate de vocabulário (o sweep 2 checa só o checklist VOC) e recomende na Mensagem Final re-rodar a `market-research` pra ganhar a camada acionável de avatar.

Use ESTAS variáveis ao gerar — sem placeholders hardcoded.
