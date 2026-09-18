# Content Recycler · Referência: Identificação e extração da essência e do framework (ETAPAs 0 e 1)

> A nota das etapas comuns às duas trilhas, a identificação com o registro da classe lida, a divergência com a lib, e a extração da essência com os dois campos novos, os exemplos de script contra framework, como extrair e usar, e os sistemas nomeados com as queries exatas. Abra na ETAPA 0.

As ETAPAS 0 e 1 são comuns às duas trilhas. Depois delas, a **Trilha 1 roda primeiro, sempre**; a Trilha 2 só quando o membro pedir.

### ETAPA 0 — Identificação do breakthrough

Input `[creative-id]` ou `breakthrough`/`winner` (detecção do pré-flight). Registre o **`ad_class` lido** (`breakthrough` ou `spend_winner`) — é ele que define quais movimentos ficam liberados no resto da execução. Se o input é um `[creative-id]` de conceito (formato `c-NN`), abra primeiro `workspace/[produto]/creative-engine/dados.json` pros campos estruturados e use `concept-NN.md` como brief complementar (ETAPA 1 do `recycler.md`).

> **Onde a lib diverge, esta skill vence.** A ETAPA 1 do `recycler.md` ainda fala em `winner` / `outcome == "winner"`. Aquele texto é a engine dos 9 formatos, não a fonte do gatilho — o gatilho é o `breakthrough` do cânone §2, definido aqui. Nunca reciclar um criativo por ele aparecer num array chamado `winners[]`.

### ETAPA 1 — Extração da essência E do framework

Destile big idea, hook, mecanismo, avatar e voz em `essence.json` seguindo a ETAPA 2 do `.claude/lib/content-recycler/recycler.md` (fontes rastreáveis: `mechanism_name` LITERAL de `offer-builder`, `voc_refs[]` herdadas de `creative-engine`/`market-research`, sanity check de drift que PARA e surface ao membro).

**Só a essência não basta — o que viaja é o FRAMEWORK.** O script do criativo não viaja: ele é feito daquele produto, daquele avatar e daquele mecanismo. O padrão por trás do script viaja pra qualquer avatar, canal e mecanismo. Dois exemplos do que é script e do que é framework:

- Script: `"I think I just got scammed"` (tradução livre: "acho que acabei de ser passado pra trás"). Framework: `"I think [negative thing] just happened (to me)"`.
- Script: `"I ordered X but they sent me [muito mais]"`. Framework: `"I thought I was getting X, I got Y instead"`.

Hook específico gasta com uso em massa; framework não gasta. Por isso o `essence.json` ganha dois campos além do schema da lib:

```json
{
  "framework_template": "<o padrão do hook/script com o slot vazio — ex: 'I think [negative thing] just happened (to me)'. Sempre em inglês US, do mesmo jeito que roda no ad>",
  "psychological_mechanism": "<POR QUE o padrão funciona, em 1 frase: o efeito na cabeça do avatar, não a descrição do hook. Ex: 'tira do avatar o peso da culpa e do fracasso'>"
}
```

- **Como extrair (subir um nível):** pegue a frase literal do breakthrough, remova o que é específico daquele produto/avatar e deixe o slot. Se o que sobrou não faz sentido para outro avatar, você tirou específico de menos.
- **Como usar:** quem não é bom de copy piora o hook ao reescrever. Toda aplicação nova do framework sai em 3 versões — **1 controle** (o hook 1:1 do original) + **2 reescritas** com palavras próprias — e o teste decide qual fica.
- **Para que serve o `psychological_mechanism`:** é o juiz de toda iteração da Trilha 1. O aprendizado a extrair de um breakthrough nunca é "o hook é bom", é o mecanismo psicológico que ele aciona. Iteração que muda o texto e muda junto o que é COMUNICADO não é iteração, é conceito novo mal rotulado.

Puxe os SISTEMAS NOMEADOS abaixo pra sustentar a destilação (rode `search_knowledge` com a `best_query`, `deep=true`):
   - **Hook Writing Framework — 3 Functions of a Hook** (rode `hook framework 3 functions ad video stop scroll create curiosity`) — pra identificar qual das 3 funções o hook cumpre antes de reembalar.
   - **Ad Definitions — Concept / Angle / Variation / Format** (rode `ad definitions concept angle variation format 3-2-2 testing structure`) — separa o que é CONCEITO/ÂNGULO reaproveitável (viaja entre canais) do que é só FORMATO descartável.
   - **Storytelling as the Hardest-to-Replicate Angle** (rode `storytelling hardest to replicate angle founder story defensible creative`) — se a essência for narrativa de fundador/origem, ela é o ativo mais defensável; preserve-a intacta nas duas trilhas.
   - **Show Don't Tell** (rode `show don't tell behavioral change when telling aren't selling spoken language video`) — destila a demonstração central do criativo pra carregá-la pros formatos visuais.
