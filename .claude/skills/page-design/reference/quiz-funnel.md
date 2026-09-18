# Page Design · Referência: O funil de quiz inteiro (sub-etapa 1.7)

> O funil completo quando o `page_type` é `quiz`: o mapa de telas, de onde sai cada pergunta e cada perfil de resultado, a oferta ancorada no resultado, o mecanismo que faz o funil andar sem JavaScript e sem app, o bloco `quiz` do `page-plan.json`, o movimento entre telas e o mapa que o membro lê. Abra na sub-etapa 1.7, logo depois de o `page_type` fechar como `quiz` na 1.1.

## Quando esta sub-etapa roda

Só com `page_type: "quiz"`, que nunca sai sozinho da consciência dominante nem do lead da copy: ele chega pelo formato do concorrente ou por pedido direto do membro, e nos dois casos quem decide é ele (`page_type_signals.resolved_by: "member"`, regra da 1.1). Fechado o `quiz`, esta sub-etapa substitui a 1.2 (menu de sections): o que se planeja não é uma página com seções empilhadas, é um funil de telas.

O resto da skill continua igual. A ETAPA 2 (tipografia, cor, comparadora) roda como sempre, a rota de design da ETAPA 3 é escolhida pelo membro do mesmo menu, a régua de `reference/regua-de-design.md` é a mesma e continua bloqueante, e o entregável continua sendo um `design/page.html` aprovado por ele.

**Puxe estes sistemas antes de escrever a primeira pergunta** (piso obrigatório desta sub-etapa, `deep=true`, não contam no teto da etapa):

- **Medical Closing (quiz funnel pós-clique)** (rode `medical closing quiz funnel pos-clique dosagem personalizada urgencia`): é o fechamento da tela de resultado, em que a recomendação chega em registro de diagnóstico, personalizada, e a urgência nasce do próprio resultado.
- **Transformation Message Map** (rode `transformation message map before state path messages dream state por persona`): uma trilha de mensagem por perfil, que é exatamente o que separa as telas de resultado.
- **Iyengar Choice Overload (Narrow the Options)** (rode `Iyengar choice overload narrow options jam study landing page categories`): governa quantas alternativas cada pergunta oferece.
- **Direct vs Transitional CTA** (rode `direct vs transitional CTA Miller buy now download guide stepping stone`): o quiz é o CTA de transição em pessoa, e a tela de resultado é onde o CTA vira direto.

## O que o funil é, em quatro princípios

1. **Uma tela por vez.** O visitante vê a pergunta atual e nada mais. Nada do que vem depois aparece antes da hora, e a oferta não vaza para as telas de pergunta.
2. **O caminho é o estado.** Cada resposta é um link para a próxima tela, e o endereço da página guarda onde a pessoa está. Sem JavaScript, sem app, sem cookie, sem servidor.
3. **Toda pergunta trabalha.** Ou ela separa um sub-avatar (e decide o perfil), ou ela trata uma objeção ranqueada da `market-research`. Pergunta decorativa não entra.
4. **O resultado é a venda.** A tela de resultado recomenda um produto ou pacote real da `offer-builder` e leva o botão de compra. Nenhuma tela pede email antes do resultado.

## 1.7.1 O mapa de telas

O funil tem quatro tipos de tela, nesta ordem:

| Tipo | Quantas | O que carrega |
|---|---|---|
| `intro` | 1 | A promessa do resultado, quantas perguntas e quanto tempo leva, e um botão que começa. É o único `<h1>` da página |
| `question` | 4 a 6 | A pergunta, de 2 a 4 alternativas e a barra de progresso. Menos de 4 não justifica o formato; mais de 6 perde gente no meio |
| `result` | 2 a 4 | O perfil nomeado, por que aquele perfil, a recomendação com a oferta e o botão de compra |
| `read` | 1 por resultado | A leitura do resultado, que é uma camada dentro da própria tela de resultado (1.7.4), não uma tela separada |

**Uma pergunta é a que roteia.** É ela que separa os sub-avatares, e cada alternativa dela leva a um perfil de resultado. As outras não ramificam: seguem em linha até a que roteia. Ponha a que roteia por último quando der, porque assim nenhuma pergunta precisa existir em duas versões.

**Quando a ramificação é real** (a pergunta que roteia vem no meio, e depois dela cada perfil tem perguntas próprias), cada braço carrega as telas dele. O funil ramifica para frente e nunca volta a se juntar: duas respostas diferentes não desembocam na mesma tela seguinte, porque a tela seguinte é justamente o que guarda a diferença.

## 1.7.2 De onde sai cada pergunta

**A pergunta que roteia sai dos sub-avatares.** Leia `market-research/dados.json`, pegue os sub-avatares e escolha o eixo que de fato os separa (o problema dominante, o estágio da vida, o que já tentou). Cada alternativa é um sub-avatar, escrita no vocabulário dele: use a frase de VOC que a `market-research` registrou, não a sua descrição do segmento. Quatro alternativas é o teto, e três é o normal.

**As outras saem das objeções ranqueadas.** Cada pergunta restante nomeia uma objeção da `market-research` (ou do gap analysis da `competitor-analysis`) e devolve, nas alternativas, as posições reais que as pessoas têm sobre ela. Duas coisas acontecem ao mesmo tempo: a pessoa se compromete com a própria resposta, e a tela de resultado já sabe qual objeção derrubar primeiro naquele perfil.

**O que nunca entra:** pergunta de dado que o funil não usa (idade sem consequência, nome, email), pergunta cuja resposta não muda nada no resultado, pergunta com alternativa que ninguém escolheria (a alternativa de enfeite entrega o jogo), e pergunta que já vende ("você quer parar de sofrer com X?").

**O limite honesto do mecanismo:** as respostas das perguntas que não roteiam não chegam à tela de resultado. O caminho guarda o perfil, não o histórico. Então a tela de resultado nunca cita a resposta de uma pergunta específica ("como você disse que dorme mal..."), e a objeção que a pergunta levantou é tratada no resultado do perfil inteiro, não da pessoa. Escrever o contrário produz uma tela que mente.

## 1.7.3 Os perfis e a oferta de cada um

Um perfil por alternativa da pergunta que roteia, de 2 a 4. Cada perfil tem:

- **Nome próprio**, curto, em inglês, que a pessoa reconheça como sendo sobre ela. Nunca "Perfil A" nem "Tipo 2".
- **O sub-avatar de origem**, registrado no plano, para a `consistency-audit` conseguir cruzar depois.
- **A recomendação**: um pacote de `aov_levers.bundles[]` da `offer-builder`, pela quantidade. Perfil que recomenda quantidade sem pacote correspondente na oferta reprova, porque a `page-build` não vai ter variante para ligar no botão.
- **A ordem da prova**: qual objeção aquele perfil carrega mais forte, e portanto qual prova aparece primeiro na tela dele.

**Dois perfis podem recomendar o mesmo pacote.** O que muda entre eles é o argumento, não obrigatoriamente o produto. O que não pode é a página dizer a mesma coisa em duas telas: se o texto dos dois resultados é intercambiável, os perfis não existem e a pergunta que roteia não está separando ninguém.

**A tela de resultado, em ordem:** o perfil nomeado, a leitura em uma frase (por que o resultado deu isso, ligada à resposta que roteou), o mecanismo nomeado LITERAL da `offer-builder`, a recomendação com o pacote e o preço, a prova na ordem do perfil, a garantia e o botão. Nada de aviso, ressalva ou nota antes da recomendação: o resultado vai direto ao que a pessoa deve fazer (rule 8b).

## 1.7.4 O caminho é o estado (o mecanismo)

Todas as telas existem no mesmo documento. Cada uma tem um `id`, cada alternativa é um link para o `id` da próxima, e o CSS mostra a tela apontada pelo endereço. São três regras, nesta ordem:

```css
.quiz-screen:not([data-first]){ display: none }                        /* 1 */
.quiz-screen:target{ display: block }                                  /* 2 */
.quiz:has(.quiz-screen:target) .quiz-screen[data-first]{ display: none } /* 3 */
```

1. Só a tela de abertura nasce visível.
2. A tela apontada pelo endereço aparece (mesma especificidade da regra 1, declarada depois, então vence).
3. A abertura sai de cena assim que a navegação começa.

**A regra 3 é a única que usa `:has()`, e isso é proposital.** Navegador que não entende `:has()` descarta essa regra e mantém as outras duas: o visitante vê a abertura mais a tela atual, uma embaixo da outra. Feio e inteiro, nunca em branco. É a mesma disciplina do item M4 da régua: o estado inicial nunca depende de um seletor que o navegador pode não entender.

**A leitura do resultado é uma camada dentro da tela de resultado, não uma tela própria.** Assim o endereço já é o do resultado desde o clique, e a altura da tela não muda quando a leitura termina.

```css
.quiz-screen{ position: relative; min-height: 26rem; scroll-margin-top: var(--space-8) }
.quiz-read{ position: absolute; inset: 0; background: var(--background);
            animation: quiz-read-out .3s 1.8s ease-out forwards }
.quiz-body{ animation: quiz-in .4s 1.8s ease-out backwards }
@keyframes quiz-read-out{ to { opacity: 0; visibility: hidden } }
@keyframes quiz-in{ from { opacity: 0; transform: translateY(12px) } to { opacity: 1; transform: none } }
@media (prefers-reduced-motion: reduce){
  .quiz-read, .quiz-body, .quiz-read [data-quiz-bar]{ animation-delay: 0s; animation-duration: 1ms }
}
```

A barra da leitura preenche uma vez em 1,8s e para (`width` de 0 a 100% com `forwards`). Não é laço, então o item M6 continua valendo inteiro.

**O que este mecanismo entrega, medido no Chromium:** endereço que abre direto no resultado (`#result-a` mostra o resultado de quem chega por link ou por anúncio), botão voltar do navegador andando uma tela por vez, navegação só por teclado, altura idêntica entre as perguntas e zero rolagem lateral em 390 pixels.

**O que ele não entrega:** memória das respostas que não roteiam (1.7.2), e nenhum cálculo de pontuação somando perguntas. Quiz que precisa somar pontos não é este formato.

**Regras de construção que o HTML obedece:**

- A tela de abertura é a primeira do documento e leva `data-first`. Todas as telas levam `data-aura-screen="[id]"`, que é o que a `page-build` usa para virar block e o que o self-review usa para medir altura.
- O funil inteiro vive dentro de um `<section data-aura-section="quiz">`, um só. O marker de section é o contrato do split e ele não muda: uma section, um funil.
- Cada alternativa é um `<a href="#[id da próxima]">` dentro de uma lista. Nunca um botão com JavaScript.
- Cada tela de pergunta tem um link de voltar para a tela anterior, além do botão do navegador.
- Cada tela de pergunta mostra a barra de progresso com a posição dela (`passo N de M`), sempre visível.
- Toda tela que não a abertura carrega imagem com `loading="lazy"`: o funil inteiro está no documento, e sem isso a abertura paga o peso de todas as telas.
- A tela de resultado leva o formulário de compra nativo (`/cart/add` por POST) com o ID da variante recomendada. Ele nasce vazio aqui e é preenchido pela `page-build` na 6.1b.

## 1.7.5 O bloco `quiz` do `page-plan.json`

Além do bloco `strategy` de sempre, o plano ganha o bloco `quiz`. O `sections_plan` continua sendo a lista de sections do split e tem a entry `quiz`; o mapa de telas mora aqui, e é daqui que a `page-build` compila.

```json
"quiz": {
  "read_ms": 1800,
  "profiles": [
    {"slot": "a", "name": "Barrier Rebuild", "sub_avatar": "[id ou nome do sub-avatar da market-research]",
     "recommendation": {"tier_qty": 3, "bundle_label": "[label do bundle em aov_levers.bundles[]]"},
     "lead_objection": "[a objeção que este perfil carrega mais forte]"}
  ],
  "screens": [
    {"id": "intro", "kind": "intro", "step": null,
     "media": {"required": true, "kind": "lifestyle", "source": "ai_lifestyle", "status": "ready", "asset": "design/assets/quiz-intro.jpg", "acquisition_plan": null}},
    {"id": "q1", "kind": "question", "step": 1, "steps_total": 4, "routes": false,
     "source": "objection", "research_ref": "market-research/dados.json#objections[0]",
     "answers": [{"label": "[frase de VOC]", "to": "q2"}, {"label": "[frase de VOC]", "to": "q2"}],
     "media": {"required": false, "kind": "none", "source": "none", "status": "ready", "asset": null, "acquisition_plan": null}},
    {"id": "q4", "kind": "question", "step": 4, "steps_total": 4, "routes": true,
     "source": "sub_avatar_split", "research_ref": "market-research/dados.json#sub_avatars",
     "answers": [{"label": "[frase de VOC]", "to": "result-a"}, {"label": "[frase de VOC]", "to": "result-b"}],
     "media": {"required": false, "kind": "none", "source": "none", "status": "ready", "asset": null, "acquisition_plan": null}},
    {"id": "result-a", "kind": "result", "profile": "a",
     "media": {"required": true, "kind": "packshot", "source": "member_photo", "status": "ready", "asset": "design/assets/bundle-3.jpg", "acquisition_plan": null}}
  ]
}
```

- `routes: true` em **exatamente uma** tela de pergunta, e as alternativas dela apontam para telas de resultado. Toda outra alternativa aponta para uma tela de pergunta.
- Todo `to` existe como `id` de tela, e toda tela é alcançável a partir da abertura. Tela órfã é tela que ninguém vê.
- `media` por tela tem o mesmo shape do `sections_plan[].media` (schema na 4.1) e obedece ao mesmo gate: imagem real no slot ou placeholder explícito com `acquisition_plan`. A `page-build` bloqueia o deploy com placeholder vivo aqui também.
- O bloco `commerce` ganha uma superfície de compra por tela de resultado, com a tela nomeada: `{"section": "quiz", "screen": "result-a", "kind": "single_cta", "tiers_qty": [3]}`. É isso que faz o check bloqueante de IDs da 6.1b cobrir o funil inteiro, sem régua nova.
- `sections_plan` tem a entry `quiz` (a section do funil) e, opcionalmente, sections depois dela. **Só entra abaixo do funil o que vale para todo perfil** (garantia, FAQ, rodapé de marca). Tudo que muda por perfil mora dentro da tela de resultado, senão o funil entrega a oferta antes da pessoa responder.

## 1.7.6 Movimento e imagem

**Movimento:** a transição entre telas é o item M8 de `reference/regua-de-design.md`, e é lá que ele se confere. Nada aqui inventa régua paralela.

**Imagem:** o mapa de mídia de cada tela sai da 1.6, e com as tools do Higgsfield na sessão as telas entram na mesma rodada de geração da 1.6.3 (`reference/imagens-higgsfield.md`), com a mesma régua lida por visão, o mesmo teto de 3 tentativas por slot e a mesma limpeza de metadados. O que é desta sub-etapa: a tela de abertura pede imagem que mostra o resultado desejado, e as telas de pergunta em geral não pedem imagem nenhuma, porque a imagem compete com a pergunta.

**Movimento em arquivo** (demonstração do produto na tela de resultado) entra como `<video>` com `poster` e `controls`, nunca com reprodução automática e nunca como GIF: o GIF roda em laço e nenhuma folha de estilo o pausa, então ele atropela o M6 e quem pediu menos movimento. O `poster` é a primeira imagem que a pessoa vê e obedece à mesma régua de imagem.

## 1.7.7 O mapa do quiz para o membro

O `design-system.md` ganha a seção **Mapa do quiz**, que é o que o membro lê para entender o funil sem abrir o JSON:

1. **As perguntas**, na ordem, cada uma com a pergunta escrita, as alternativas e de onde ela saiu (o sub-avatar que ela separa, ou a objeção que ela trata).
2. **As ramificações**, em uma linha por alternativa da pergunta que roteia: qual resposta leva a qual perfil.
3. **Os perfis**, um bloco cada: nome, de quem é, o que a tela diz e qual objeção ela derruba primeiro.
4. **A oferta de cada perfil**, em tabela: perfil, pacote recomendado, quantidade e preço.

Escreva só o resultado, como todo doc de workspace (`report-only-results.md`): o mapa mostra o funil que existe, sem narrar como ele foi montado. O `.html` sai do `render_report.py` junto do resto do arquivo, como sempre.

## O que reprova, antes de o membro ver

- Mais de uma tela com `routes: true`, ou nenhuma.
- `to` apontando para tela que não existe, ou tela que nenhum caminho alcança.
- Perfil cuja recomendação não existe em `aov_levers.bundles[]`.
- Dois resultados com texto intercambiável.
- Pergunta que não separa sub-avatar nem trata objeção ranqueada.
- Tela de resultado que cita a resposta de uma pergunta que não roteia.
- Qualquer aviso, ressalva, asterisco ou claim suavizado antes da recomendação.
- `<script>` no `design/page.html`, ou alternativa que não é link.
- Altura variando entre as telas de pergunta (item M8).
