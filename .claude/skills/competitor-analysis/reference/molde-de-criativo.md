# Competitor Analysis · Referência: O molde do criativo escalado, slot a slot (ETAPA 3C)

> A descoberta do vídeo escalado pelo TrendTrack (duas passadas e as armadilhas da ferramenta), a escolha de 1 a 3 peças, a transcrição cronometrada, o corte em slots com tempo e orçamento de palavras, a leitura da imagem por visão, o `ad-molds.json` e o status no `dados.json`. Abra na ETAPA 3C, junto com `reference/criativos-escalados.md`. O cânone do molde é `.claude/lib/ad-molds/README.md`.

### ETAPA 3C — Molde do criativo escalado (a anatomia de UMA peça)

A agregação da 3C entrega estatística do mercado: quantos por cento dos criativos abrem com rosto em close, que afirmações se repetem, que faixa de duração concentra os escalados. O molde é outra coisa, e as duas convivem. O molde é a anatomia de UMA peça que roda e paga a própria conta: em que ordem os blocos vêm, que trabalho cada um faz na cabeça de quem assiste e quanto tempo cada um ocupa.

Antes de cortar o primeiro slot, leia `.claude/lib/ad-molds/README.md` e carregue os três vocabulários fechados de `.claude/lib/ad-molds/molds.json`. A regra que manda em tudo aqui é a de lá: **modelar estrutura e mecânica, nunca conteúdo.** Nenhum campo do molde guarda a fala do concorrente — a fala fica no transcript, que a 3C já salva.

A extração é opcional, como a 3C inteira. Sem TrendTrack, sem crédito, sem mídia ou sem transcrição com marcação de tempo, ela cai pro caminho que a 3C já usa e segue em silêncio, sem avisar o membro e sem travar a skill.

#### 1. Descoberta — achar o vídeo que vale modelar

Com tools `mcp__trendtrack__*` na sessão, a descoberta é por TrendTrack. A intenção é **Discover → ads em lote** (hoje `search_ads`), casada em runtime pelo que a sessão expõe e nunca por nome fixo de tool (`.claude/lib/trendtrack-integration/README.md`). Antes da primeira chamada, rode a intenção **Account → créditos** e diga ao membro, em uma linha, quantas chamadas esta etapa vai fazer: **1 a 2 por concorrente, em no máximo 3 concorrentes**. Saldo que não cobre, chamada que falha ou MCP ausente: silent fallback pro parágrafo final deste bloco.

Escopo no concorrente: `search_in: "brand"` com o nome da marca em `query`, ou `tracked_pages` com o id da página quando ele já é conhecido. Em toda passada, `media_type: "video"` e `status: "active"`.

**Passada 1 — vencedor recente. É o padrão.** `created_after` na data de 30 dias atrás, `sort_by: "longestRunning"`, `order: "desc"`. Entre os anúncios que nasceram no último mês, ela traz os que já sobreviveram quase o mês inteiro. É exatamente o que se quer modelar: estrutura de criativo envelhece, e o que escalou há um ano pode não escalar hoje.

**Passada 1b — a volta do alcance zero.** A Meta só publica alcance de anúncio veiculado na União Europeia, e a ordenação por mais tempo rodando carrega um guard de alcance zero para conter artefato de data de indexação. Resultado prático: marca que escala só nos EUA e no Canadá pode devolver lista vazia na Passada 1 mesmo tendo vencedor no ar. Voltou vazia, repita a mesma passada trocando só a ordenação, para `sort_by: "adOrder"` com `order: "asc"` (valor menor é rank mais forte), mantendo o `created_after`. O recorte de vencedor recente continua o mesmo; só o critério de ordenação muda.

**Passada 2 — o perene. Só com menos de 3 candidatos depois da 1 e da 1b.** Sem `created_after`, com `min_days_running: 60`, `sort_by: "adOrder"` e `order: "asc"`. Ela responde outra pergunta: não o que escalou agora, e sim o que atravessa trimestres.

**As armadilhas da ferramenta, as três obrigatórias:**

1. **`sort_by` sempre definido.** Omitir cai no padrão de crescimento de sete dias, que injeta por conta própria janela de alcance recente e alcance mínimo de 1 — dois filtros que ninguém pediu e que zeram anúncio de fora da União Europeia.
2. **Data de primeira aparição tem artefato de indexação**, e a própria documentação da ferramenta avisa. Confirme linha por linha que o tipo de mídia é vídeo e que o tempo de veiculação bate com o filtro pedido; linha que não bate sai da lista, em vez de confiar na ordenação.
3. **Alcance não é régua de escala aqui.** Alcance zero em anúncio só dos EUA não é gasto zero. A escala se lê por dias no ar, duplicatas e rank do anúncio, a mesma régua da ETAPA 3F.

Da linha escolhida, guarde: id do anúncio, link da mídia (o campo de Media URL; o de Thumbnail URL não serve, porque molde precisa do vídeo e não do quadro parado), dias no ar, duplicatas e rank. Quando a linha vier como agregado de criativos, a intenção **Brief → decompor 1 ad** (hoje `scan_ad`) aceita o id da collation e devolve hook, estrutura e veredito de escala do conjunto: ela ajuda a pré-selecionar, e não substitui a transcrição.

**Sem TrendTrack**, os candidatos são os que a 3C já tem em mão: os criativos que o membro curou com um dos 3 sinais de escala e os vídeos do top 10 da ETAPA 3, com a mídia vinda do cartão da Meta Ad Library.

#### 2. Escolha — de 1 a 3 moldes por produto

Escolha as peças de maior evidência de escala, no máximo três. O limite é de qualidade, não de custo: um molde é um esqueleto inteiro, e empilhar moldes faz a skill misturar estruturas em vez de modelar uma. Três já cobre os formatos distintos que um concorrente costuma rodar ao mesmo tempo (o depoimento, a demonstração e a peça de mecanismo, por exemplo).

Ordem de preferência quando há mais candidatos que vaga: mais dias no ar dentro do recorte da passada, depois mais duplicatas, depois rank mais forte. Dois candidatos com a mesma estrutura aparente contam como um: fique com o de mais evidência e use a vaga livre num formato diferente.

#### 3. Pré-seleção pelo texto corrido (quando a marca está no Brand Tracker)

A intenção **Brief → transcrições de marca trackada** (hoje `get_brandtracker_transcripts`, que exige o id da marca no Brand Tracker do membro) devolve o texto corrido dos vídeos daquela marca, com o número de usos de cada um. Serve para ler antes de gastar transcrição: dá para ver qual peça tem estrutura de oferta inteira e qual é só um corte de dez segundos.

Ela **não** substitui a transcrição cronometrada, porque não tem tempo nenhum. Molde sem tempo não é molde.

#### 4. Transcrição cronometrada

A cascade é a que a 3C já usa, sem degrau novo: Groq, Whisper local `medium` ou `turbo`, transcript do membro. Sempre com marcação de tempo por palavra, que é o insumo do corte em slots.

Baixe a mídia antes: `curl -sL "<media_url>" -o workspace/[produto]/competitor-analysis/creatives-inbox/<ad-id>.mp4`. O arquivo local serve à transcrição e à leitura dos quadros do item 6.

**Transcript sem marcação de tempo não gera molde.** Nesse caso grave o status `no_timed_transcript` no `dados.json` e siga: estimar tempo por posição no texto produziria um ritmo inventado, que é o único ativo que o molde tem para entregar. O transcript continua onde a 3C o salva, em `creatives-inbox/transcripts/`; o molde referencia o arquivo e não copia a fala.

#### 5. Corte em slots

Slot é unidade funcional: um trecho com função psicológica própria. Não é frase e não é parágrafo. Duas frases que fazem o mesmo trabalho são um slot só; uma frase que faz um trabalho novo é um slot novo.

- **A fronteira fica na palavra em que o trabalho muda**, com o segundo vindo da marcação de tempo daquela palavra. Uma casa decimal.
- **`t_in` do slot seguinte é o `t_out` do anterior**: sem buraco e sem sobreposição. Abertura só com imagem, ou pausa longa no meio, é slot de `sem_fala` com `words_budget` zero, nunca um buraco na linha do tempo.
- **`words_budget` é medido**, não estimado: a contagem de palavras faladas dentro da janela do slot. É número, então não carrega conteúdo do concorrente.
- **`function` e `sentence_type` saem dos vocabulários fechados** do `molds.json`. Valor fora da lista significa slot mal classificado: confira se o trabalho dele não é um dos que já existem com outro nome antes de propor valor novo.
- **`duration_s`** é o `t_out` do último slot, e o vídeo inteiro tem de estar coberto.

Três checagens de sanidade do corte, todas com ação:

| Sinal | O que significa | O que fazer |
|---|---|---|
| Menos de 6 slots num vídeo de 30 segundos | O corte reproduziu os quatro baldes grossos (hook, bridge, hold, CTA) | Recortar, procurando a troca de trabalho dentro de cada balde |
| Mais de 14 slots num vídeo de 30 segundos | O corte foi por frase, não por função | Juntar as frases vizinhas que fazem o mesmo trabalho |
| Slot fora da faixa de 2,5 a 3 palavras por segundo | Marcação de tempo errada, ou fronteira no lugar errado | Reabrir o transcript naquele trecho antes de aceitar o slot |

#### 6. Imagem — a função visual sai da mídia, não da imaginação

Com o arquivo em mão, extraia um quadro no meio de cada slot e leia os quadros por visão:

```bash
mkdir -p workspace/[produto]/competitor-analysis/creatives-inbox/frames
ffmpeg -ss <segundo do meio do slot> -i <arquivo.mp4> -frames:v 1 -q:v 3 \
  workspace/[produto]/competitor-analysis/creatives-inbox/frames/<ad-id>-slot-<n>.jpg
```

Classifique cada quadro num dos dez valores de `visual_function` do `molds.json`, sempre como função ("rosto em close", "prova na tela"), nunca como descrição da cena do concorrente. Slot com corte visível no meio recebe a função que ocupa mais tempo dele.

**Sem acesso à mídia** — link morto, download barrado, ffmpeg ausente — o campo fica `null` em todos os slots, e o molde declara o vazio. Inventar a cena é pior que não ter o eixo: a `creative-engine` escreveria a imagem do briefing em cima de uma suposição.

#### 7. Salvar o molde e registrar o status

O molde vai para `workspace/[produto]/competitor-analysis/ad-molds.json`, no schema do cânone:

```json
{
  "generated": "ISO timestamp",
  "molds": [
    {
      "mold_id": "",
      "source": { "concorrente": "", "ad_id": "", "media_url": "" },
      "evidence": { "dias_em_veiculacao": 0, "sinal": "rank_do_anuncio|longest_running|aparicoes_repetidas|metrica_direta_de_spend", "detalhe": "" },
      "duration_s": 0,
      "transcription_model": "groq-whisper-large-v3-turbo|whisper-medium|whisper-large-v3-turbo|member_provided",
      "slots": [
        { "n": 1, "t_in": 0.0, "t_out": 0.0, "function": "", "sentence_type": "", "visual_function": null, "words_budget": 0 }
      ]
    }
  ]
}
```

E o status entra no `dados.json`, ao lado do que a 3C já grava:

```json
"ad_molds": {
  "status": "completed|skipped|no_timed_transcript",
  "molds_count": 0,
  "molds": [ { "mold_id": "", "competitor": "", "scale_signal": "", "days_running": 0 } ],
  "molds_file": "workspace/[produto]/competitor-analysis/ad-molds.json"
}
```

Assim a `creative-engine` sabe se existe molde antes de abrir o arquivo. Nenhum molde extraído entra no relatório do membro como transcrição: no `.md`, a seção de criativos escalados ganha uma linha dizendo quantos moldes saíram, de quais concorrentes e por qual sinal de escala.

Os moldes vivem no workspace do produto, nunca no framework: eles nomeiam concorrente, anúncio e nicho, então são pesquisa do membro (regra 11 do `CLAUDE.md`).

#### Checagem antes de fechar a etapa

- Cada molde tem de 8 a 14 slots num vídeo de 30 segundos, e a faixa acompanha a duração nos vídeos mais curtos ou mais longos.
- A linha do tempo está coberta de ponta a ponta, sem buraco e sem sobreposição, e o último `t_out` é o `duration_s`.
- Todo `function`, `sentence_type` e `visual_function` está no vocabulário do `molds.json`, com `null` só onde a mídia não abriu.
- Nenhum campo do `ad-molds.json` guarda frase, afirmação, número ou nome de mecanismo do concorrente.
- O `words_budget` de cada slot é contagem real da transcrição, e a leitura por segundo passou na checagem de sanidade.
- O `evidence` nomeia o sinal de escala com o número que o sustenta.
- O `dados.json` tem o bloco `ad_molds` com o status, a contagem e o caminho do arquivo.
