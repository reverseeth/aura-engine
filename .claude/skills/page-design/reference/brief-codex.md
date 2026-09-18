# Page Design · Referência: Segunda opinião no Codex (sub-etapa 3.8, opcional)

> O briefing autossuficiente que o membro cola no Codex pra gerar uma versão concorrente da mesma página, o que ele carrega dentro (plano de seções, copy literal, paleta com os valores, tipografia, imagens, a régua inteira e o contrato do arquivo), o esqueleto pronto pra preencher, o que o membro anexa e o que a Aura faz quando o HTML volta: normalizar, limpar, pontuar as duas no mesmo placar e recomendar uma, com o motivo. Abra na sub-etapa 3.8, depois do self-review da 3.7 e antes de fechar o checkpoint.

### 3.8 Segunda opinião no Codex (opcional)

Uma segunda versão da mesma página, desenhada por outro modelo a partir do mesmo material, e as duas comparadas contra a mesma régua. Serve pra duas coisas: achar o que a primeira versão não tentou, e transformar "gostei mais dessa" numa decisão com evidência.

**Ela é opcional e o membro decide.** A skill oferece uma vez e segue sem ela na mesma velocidade.

#### Quando roda, e quando não roda

- **Depois** do self-review da 3.7, com a página da Aura já dentro da régua. Comparar uma versão auditada com um rascunho não compara nada.
- **Antes** de fechar o checkpoint de aprovação: é ali que o membro escolhe entre as duas.
- **Não é rota.** Não entra no menu da 3.2, não tem pré-requisito próprio, não muda `design_route` e não substitui nenhuma etapa anterior. A rota já rodou; isto é uma segunda leitura do mesmo plano.
- Oferecida **uma vez**. Membro diz não, nada é salvo e o assunto não volta nesta sessão.
- O custo é o tempo dele: sair daqui, rodar o Codex, voltar com um arquivo. Diga isso na oferta, pra ele decidir sabendo.

A oferta, no `report_language`, dentro da mensagem do checkpoint:

> "Quer uma segunda versão dessa página pra comparar? Eu monto um briefing pronto, você cola no Codex (o agente de programação da OpenAI), ele desenha outra versão da mesma página com a sua copy e as suas imagens, e eu comparo as duas contra a mesma régua, item por item, e te digo qual eu escolheria e por quê. A escolha é sua. Leva alguns minutos do seu lado e é opcional: se não quiser, seguimos com esta."

#### O que o briefing carrega (autossuficiência é o requisito)

O Codex não enxerga o `workspace/`, não leu a pesquisa e não acompanhou as decisões das etapas anteriores. **Tudo que ele precisa vai dentro do arquivo, em valor literal.** Oito blocos, e nenhum deles é um ponteiro pra outro arquivo:

1. **A página em cinco linhas:** `page_type` e o que isso significa, o avatar central em uma frase, a consciência dominante, a promessa central e o mecanismo nomeado LITERAL da `offer-builder`.
2. **O plano de seções:** o `section_order` na ordem, e por seção o id (que vira o marker), o eyebrow, o papel em uma frase e os block types.
3. **A copy real, seção por seção, literal e em inglês US.** Zero resumo, zero "coloque aqui a headline". A copy é da `copy-engine` e não se discute no briefing.
4. **A paleta:** os 8 roles com o hex, o nome da paleta e uma linha por role dizendo onde aquela cor entra.
5. **A tipografia:** as famílias com os pesos, e como cada uma carrega — o `<link>` do Google Fonts com os pesos exatos, ou o `@font-face` apontando pros arquivos de `assets/fonts/` (o mesmo bloco `data-aura-fonts` da 2.1).
6. **As imagens:** uma linha por slot do mapa de mídia, com o caminho relativo (`assets/...`), a proporção, o que a imagem mostra e a marcação do hero (sem lazy, com `width`/`height`).
7. **A régua de design inteira:** os cinco blocos de `reference/regua-de-design.md` (T, E, C, M e S), copiados literalmente.
8. **O que não fazer:** a lista fechada abaixo, também literal.

O briefing sai no `report_language` do membro (ele lê antes de colar); a copy dentro dele fica em inglês US, porque é a copy final da página.

**A régua entra por cópia, não por referência.** Os cinco blocos saem inteiros de `reference/regua-de-design.md`, sem a seção "Como esta régua é usada" (que descreve o fluxo interno da Aura) e sem a seção final do que ela não cobre. Os comandos de cada bloco vão junto, com o nome do arquivo trocado pelo que o Codex vai gerar:

```bash
awk '/^## Bloco T/,/^## O que esta régua não cobre/' \
  ../../../../.claude/skills/page-design/reference/regua-de-design.md \
  | sed '$d' | sed 's#design/page\.html#page-codex.html#g'
```

Confira antes de colar no briefing: os 31 itens presentes (T1 a T6, E1 a E5, C1 a C5, M1 a M7, S1 a S8) e nenhuma menção a `design/page.html` sobrando.

#### O bloco "o que não fazer" (vai literal no briefing)

- **Não reescreva, não corte e não melhore a copy.** Ela vem de pesquisa. Aqui o trabalho é de design.
- **Não acrescente aviso de nenhum tipo:** nada de disclaimer, "resultados podem variar", "consulte um médico", asterisco, nota de rodapé que enfraquece o que a copy afirma acima, nem rótulo dizendo como uma imagem foi feita. Claim forte recebe a prova que já está na copy, nunca uma ressalva. (Isto não é o texto da garantia, as condições de frete e devolução nem os links de política da loja, que são parte da oferta e continuam na página como estiverem no briefing.)
- **Não suavize claim.** "Pode ajudar a" e "feito para apoiar" não existem; o que a copy afirma, a página afirma.
- **Não invente** seção, preço, número, depoimento, selo, garantia ou logo. O que não está no briefing não existe.
- **Não use** framework de CSS, CDN, biblioteca por script, fonte fora das que o briefing nomeia, nem imagem fora da lista.
- **Nada de emoji na interface.** Ícone é SVG inline, desenhado no próprio arquivo.
- **Nenhum `<script>`.** Accordion, tabs e FAQ saem com `<details>`/`<summary>` e CSS.

#### Esqueleto do arquivo (preencha com os valores reais e salve)

Salve em `workspace/[produto]/page/design/brief-codex.md`. Ele é isento do `.html` companion da rule 6b: é texto pra colar num agente, não relatório que o membro abre no browser.

````markdown
# Briefing: página [page_type] de [marca]

Monte UMA página de vendas completa, em um arquivo HTML só. Tudo o que você precisa está
aqui. Não invente nada que não esteja neste documento.

## O que entregar

Um arquivo `page-codex.html`, salvo ao lado da pasta `assets/`:

- HTML + CSS plano, num arquivo que se basta: um `<style>` único no `<head>`, nenhuma
  dependência externa além das imagens e das fontes da pasta `assets/`. Sem framework,
  sem CDN, sem build.
- Zero `<script>`. Interação por `<details>`/`<summary>` e CSS.
- Cada seção abre com `<section data-aura-section="[id da tabela de seções]">`.
- Imagens por caminho relativo pra `assets/`, exatamente como a lista da seção 6.
- Ícones em SVG inline. Nenhum emoji.
- Uma passada só, do começo ao fim. A página inteira, todas as seções.

## 1. A página

- **Tipo:** [page_type]. [o que isso significa, em uma frase]
- **Quem lê:** [avatar central em uma frase] · já tentou [as soluções anteriores]
- **O que ele já sabe:** [consciência dominante e o que isso muda na abertura]
- **Promessa central:** [a promessa da oferta]
- **Mecanismo:** [nome LITERAL do mecanismo]. [o que ele é, em uma frase]
- **O que a página tem que fazer:** [a ação, em uma frase]

## 2. As seções, nesta ordem

| # | id (marker) | eyebrow | papel da seção | blocos |
|---|---|---|---|---|
| 1 | hero | [eyebrow] | [papel em uma frase] | [blocks] |
| 2 | ... | | | |

## 3. A copy (literal, em inglês, não reescreva)

### 1. hero · `data-aura-section="hero"`

[a copy da seção, literal, com headline, subhead, bullets e CTA marcados]

### 2. [id] · `data-aura-section="[id]"`

[...]

## 4. Cor (paleta "[nome]")

| role | hex | onde entra |
|---|---|---|
| background | #... | fundo da página |
| surface | #... | cartões e blocos elevados |
| foreground | #... | texto |
| primary | #... | botão principal e só ele |
| on_primary | #... | texto dentro do botão |
| accent | #... | o que tem que ser lido primeiro na seção (um por seção) |
| muted | #... | texto secundário |
| border | #... | linhas e contornos |

Declare os oito como custom properties no `:root` e use só elas. Nenhum hex solto no resto
do arquivo.

## 5. Tipografia

- **[Família], títulos e corpo** · pesos [400, 600]
- Carregamento: [o `<link>` do Google Fonts com esses pesos] OU [o bloco `@font-face`
  apontando pra `assets/fonts/...`, colado aqui inteiro, como primeiro bloco do `<head>`]
- Hierarquia pelo peso e pela escala, no máximo duas famílias na página.

## 6. Imagens (use só estas)

| slot | arquivo | proporção | o que mostra | observação |
|---|---|---|---|---|
| hero | assets/hero-lifestyle.jpg | 3:2 | [descrição] | LCP: sem `loading="lazy"`, com `width`/`height` |
| ... | | | | `loading="lazy"` |

## 7. A régua de design

Cada item abaixo é conferido no arquivo que você entregar. Item reprovado volta pra
correção, então desenhe já dentro dos números.

[os blocos T, E, C, M e S de `regua-de-design.md`, colados literalmente]

## 8. O que NÃO fazer

[a lista fechada da sub-etapa 3.8, colada literalmente]
````

#### O que o membro faz (diga exatamente, na hora de entregar o briefing)

Dois caminhos. Ofereça o primeiro; o segundo é pra quem usa o Codex no browser.

- **Codex com a pasta aberta (preferido).** Ele abre o Codex (linha de comando, app ou dentro do editor) apontando pra `workspace/[produto]/page/design/`, e cola o briefing. As imagens e as fontes já estão em `assets/` ali, nada precisa ser anexado, os caminhos relativos resolvem sozinhos e o arquivo nasce no lugar certo. Peça que ele salve como `page-codex.html` nessa pasta.
- **Codex no browser.** Ele cola o briefing e anexa as imagens de `design/assets/` que aparecem na tabela de slots, mais os arquivos de `design/assets/fonts/` quando a família é de arquivo local. Anexo no browser nem sempre chega ao agente como arquivo — por isso a tabela de imagens descreve cada uma por escrito, e a página tem que ficar de pé mesmo sem o binário na mão dele. Depois ele salva o HTML que voltar em `workspace/[produto]/page/design/page-codex.html`, e os caminhos relativos voltam a resolver.
- **Modelo:** o mais forte que a conta dele oferecer, no nível de raciocínio mais alto, não a opção rápida.
- **Não anexe o `design/page.html` desta skill.** Segunda opinião que começa vendo a primeira vira cópia dela, e aí não há o que comparar. Diga isso ao membro em uma linha, com o motivo.

#### Quando o HTML volta

1. **Confirme o lugar:** `design/page-codex.html`, ao lado de `assets/`. Se ele colou o HTML no chat, você salva.
2. **Normalização (3.6), obrigatória.** HTML de fora é HTML de fora: `reference/normalizacao-html-externo.md` inteiro — utilities viram CSS plano por estilos computados, `<script>` sai, assets locais, e os markers `data-aura-section` injetados com os ids do `sections_plan` quando faltarem.
3. **Limpeza de aviso, silenciosa.** Outro modelo acrescenta ressalva por conta própria mesmo com a instrução explícita. Apague o que tiver entrado (aviso, disclaimer, asterisco, nota de rodapé que enfraquece o claim de cima, rótulo de origem de imagem) e devolva ao original todo claim que voltou suavizado. Isso é correção, não vira item do placar nem assunto com o membro (rule 8b). A garantia, o frete, a devolução e os links de política da loja ficam.
4. **Copy conferida contra a `copy-engine`.** Frase reescrita, cortada ou inventada volta ao original antes de qualquer comparação: duas versões com copy diferente não comparam design, comparam texto.
5. **Self-review visual completo na versão do Codex também** (3.7): screenshots de 1440 e 390 no Playwright, lidos por visão.

#### O placar comparado e a recomendação

- **O mesmo placar da régua, os mesmos ids** (T1 a T6, E1 a E5, C1 a C5, M1 a M7, S1 a S8), com **uma coluna por versão**: a desta skill e a do Codex. Cada célula tem veredicto e evidência (o valor lido no CSS, ou o que apareceu no print e em qual seção). Célula sem evidência conta como reprovada.
- **A recomendação sai em até três linhas:** quantos itens cada versão reprovou, onde as duas diferem de verdade (hierarquia do hero, ritmo entre seções, tratamento de prova, densidade) e o que a escolhida faz melhor pro `page_type` e pra consciência desta página. "As duas estão boas" não é recomendação.
- **Desempate, nesta ordem:** (1) menos itens reprovados; (2) o hero que passa no Grunt Test no print de 390 — em cinco segundos dá pra dizer o que é o produto, o que ele faz por quem lê e como comprar; (3) fidelidade ao plano: nenhuma seção do `section_order` faltando e nenhuma inventada.
- **A escolha final é do membro**, e a recomendação é apresentada como recomendação. Se ele quiser partes das duas, isso é a unificação da rota 3 (`reference/rota-section-puzzle.md`): monte a página única e ela volta a passar pela régua inteira, não só nos itens da parte trocada.

#### Depois da escolha

- A versão escolhida vira `design/page.html`, a fonte única que a `page-build` compila. Quando é a do Codex, ela só é promovida depois de passar a régua inteira sem reprova, com os markers de todas as seções, o bloco `data-aura-fonts` quando a família é de arquivo local e as imagens do mapa de mídia nos slots — o mesmo portão de qualquer outra versão.
- A versão que não venceu fica no disco como está, sem virar assunto.
- **`design_route` não muda.** A segunda opinião não é rota; o valor continua sendo o da rota que a skill rodou, e `variant_chosen` no `design-tokens.json` registra a variação promovida. A rodada entra no `iterations-log.json` como qualquer iteração, dizendo que houve segunda opinião e qual versão venceu.
