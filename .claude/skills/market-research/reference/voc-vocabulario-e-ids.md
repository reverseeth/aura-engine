# Market Research · Referência: Voice of Customer, o teste do Ctrl+F, o top 20, os ids estáveis e o fallback (ETAPA 5, segunda parte)

> O teste do Ctrl+F que gera `market_vocabulary` (`words_used[]`, `words_absent[]`, `saturated_in_market`), a curadoria obrigatória do `voc_top20`, o contrato de ids estáveis `voc-NNN` com as regras de cunhagem e re-execução, e o fallback com menos de 35 frases (nunca frases sintéticas; `voc_adequacy` e `skills_blocked`). Abra na ETAPA 5.

**O teste do Ctrl+F — o vocabulário real do mercado (obrigatório):**

A proibição de parafrasear vira uma checagem verificável aqui. Depois de coletar as frases, conte quantas vezes cada termo relevante aparece na base de pesquisa e, principalmente, **rode a busca inversa**: pegue os termos que a marca, a indústria e os concorrentes usam e procure cada um dentro da base. Termo que aparece zero vez está proibido na copy.

O caso que ancora a regra vem de uma marca de colágeno. O cliente escreveu "I was tired of my skin looking dry no matter my skincare routine" — o desejo dele é "I want smoother and less dry skin". Ninguém escreveu "hydrated"; o Ctrl+F confirmou zero ocorrências. Um anúncio que diz "hydrated" está falando a língua da indústria, não a do mercado, e não ressoa.

Grave em **`market_vocabulary`** no `dados.json`:
- **`words_used[]`** — o termo real, a contagem de ocorrências na base e a categoria (problema / desejo / frustração)
- **`words_absent[]`** — o termo que a marca ou a indústria usa, quem o usa, a confirmação de zero (ou quase zero) ocorrências na base, e o substituto que o mercado usa no lugar dele

A contagem tem um segundo uso. Termo muito repetido **na base de pesquisa** é vocabulário real e deve ser usado; termo muito repetido **nos claims dos concorrentes** (os 10-15 coletados na ETAPA 3, contados pelo Buzzword Tally de lá) é mensagem fatigada e serve como prova no corpo do texto, nunca como headline. Marque esses com `saturated_in_market: true` — foi assim que um claim aparentemente ótimo ("fast hair drying without heat damage") morreu no feed: sete concorrentes diziam exatamente a mesma coisa. **As Skills `copy-engine` e `creative-engine` consultam `market_vocabulary` ANTES de escrever qualquer linha.**

**Curadoria top 20 (obrigatória):** das frases coletadas, monte o ranking das **20 mais fortes** — critério primário: frequência de menção na base de pesquisa; desempate: força emocional/especificidade. Cada entrada leva `id`, `rank`, `count` (quantas vezes a frase ou variação próxima apareceu) e `category` (problem/desire/frustration). Grave o ranking em **`voc_top20`** no `dados.json` (schema abaixo). **A Skill `copy-engine` lê exatamente esse campo** pro checklist de VOC da copy — sem ele, a `copy-engine` tem que re-curar do zero e a informação de frequência se perde. Se coletou menos de 20 frases, grave as que tem (o `voc_adequacy` já sinaliza o déficit).

**IDs estáveis de VOC (contrato com as Skills `copy-engine`/`creative-engine`/`content-recycler`):** cada frase VOC ganha um `id` sequencial no formato `voc-001`, `voc-002`… O id identifica a **FRASE**, não a posição no ranking. Regras de cunhagem:

- **Primeira execução:** cunhe os ids na ordem do rank do `voc_top20` (`voc-001` pro rank 1, `voc-002` pro rank 2…). Frases citadas em `voc_evidence[]` (core_avatar e sub_avatars da ETAPA 4.5) usam o MESMO namespace: quote que já está no top20 repete o id dela; quote que não está cunha o próximo número livre.
- **Re-execução (a skill roda de novo com aprendizado dos testes):** antes de gravar, leia o `dados.json` anterior. Frase que já tem id **MANTÉM o id pra sempre**, mesmo que o rank, o count ou a category mudem. Frase nova recebe o próximo número livre da sequência (append). Frase que saiu do top20 não libera o número dela — id nunca é renumerado nem reaproveitado.
- **Por quê:** a copy (`copy-engine`), os hooks dos criativos (`creative-engine` — o `voc_source.ref_id` de cada hook/headline aponta pra cá) e o content recycler (`content-recycler` — herda `voc_refs[]` via `creative-engine`) rastreiam cada linha até a frase de origem por esse id. Id que muda entre execuções quebra a rastreabilidade de tudo que já foi produzido.

**Fallback quando < 35 frases reais foram coletadas**: **NUNCA** gere frases artificiais/sintéticas/plausíveis. Em vez disso:

1. Registre o déficit no `dados.json` (`voc_count` real e `voc_adequacy`); o relatório traz só as frases reais que existem, sem narrar o déficit (rule `report-only-results`).
2. Registre em `dados.json.sources.blocked_sources` as fontes tentadas que bloquearam acesso.
3. **Classificar severidade do déficit pra alertar skills downstream** (`voc_adequacy` e `skills_blocked` são gravados SEMPRE no `dados.json`, inclusive no caminho feliz — a skill `copy-engine` lê esses campos):
   - `voc_count >= 35` → `voc_adequacy: "ok"`, `skills_blocked: []`, segue normal
   - `15 <= voc_count < 35` → `voc_adequacy: "medium"`, `skills_blocked: []`, skill `copy-engine` emite warning mas procede
   - `voc_count < 15` → `voc_adequacy: "insufficient"`. Skill `copy-engine` DEVE bloquear no pré-flight — copy sem VOC real não é copy, é invenção. Salvar em `market-research/dados.json`: `"voc_adequacy": "insufficient", "skills_blocked": ["copy-engine"]`
4. Siga com as etapas restantes (awareness, sophistication, root cause) — essas não dependem de VOC quantity.

Esse déficit é rastreado em `voc_count` + `voc_adequacy` do manifest e do JSON companion (`market-research/dados.json`).
