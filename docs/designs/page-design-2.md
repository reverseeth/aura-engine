# Page-design 2: páginas de nível agência na Aura

*   **Autor:** Gustavo (dono da Aura), com Claude Code
*   **Status:** Approved (2026-10-29)
*   **Data:** 2026-10-28

--------------------------------------------------------------------------------

## Overview

A Aura é um projeto de Claude Code que conduz uma marca DTC do produto ao
anúncio. Ela tem uma sequência de passos, e cada passo é uma skill em
`.claude/skills/`. Os membros (clientes da Aura) clonam o repo e rodam esses
passos na própria máquina. Todo arquivo de um produto fica em
`workspace/<slug>/`.

O passo 7, page-design, gera a página de venda do membro em
`page/design/page.html`. É HTML estático, sem JavaScript, com cada seção
marcada por `data-aura-section`. O passo 8, page-build, compila esse arquivo em
Liquid e publica na loja Shopify do membro.

Este doc reescreve o page-design. A intenção do dono é que a página saia no
nível de uma agência de design: que transmita a marca do membro e tenha uma
estrutura escolhida pelo membro ou pela Aura a partir do produto. Ninguém mede
"nível de agência", então o doc entrega três coisas que dá para conferir, mais
um critério de aceite (Goal 10):
*   um piso medido por script;
*   uma direção de arte tirada de referências premiadas;
*   um juiz estético que não é o modelo que gerou a página.

A reescrita usa ferramentas de terceiros (lista com versões em Additional
Resources). Cada uma entra numa etapa só:
*   dembrandt, para extrair a marca;
*   Awwwards, para achar referências premiadas e estudar movimento;
*   taste-skill, para a direção de arte;
*   o método do ai-website-cloner, para portar estrutura;
*   preview da Vercel, para conferir o layout no celular.

O doc também corta o que existe hoje e atrapalha. E leva para outras etapas da
Aura um arquivo de marca compartilhado e checagens medidas.

### Glossário

*   **Passo N:** a posição da skill na sequência da Aura. Setup é o 1,
    page-design o 7, page-build o 8.
*   **Régua:** a lista de 31 critérios de design do page-design, em
    `reference/regua-de-design.md`. Os itens têm prefixo por tema:
    *   T: tipografia;
    *   E: espaço;
    *   C: cor;
    *   M: movimento;
    *   S: sinais de página "feita por IA";
    *   D1 a D6: itens de direção.

    T1, por exemplo, limita a 7 os tamanhos de fonte distintos. M6 reprova
    marquee e contador; depois desta mudança, só o marquee feito com JavaScript.
    A consistency-audit tem um check M6 próprio, que não é este.
*   **3.8:** a sub-etapa atual do page-design que pede uma segunda opinião ao
    Codex.
*   **6.9:** a aprovação final da página no tema, com as fontes reais, no
    page-build.
*   **6.11:** a checagem de fidelidade do page-build depois do deploy, em
    `page-build/reference/deploy.md`.
*   **GATE 1:** o gate do page-build que proíbe JavaScript de runtime.
*   **Regra 11:** a regra da Aura de que material de terceiro nunca vai para
    commit.
*   **Rotas 1, 2 e 3:** as três formas atuais de construir a página:
    *   1, Claude Design: canvas pela tool `Artifact`;
    *   2, clone por SingleFile;
    *   3, quebra-cabeça de seções.
*   **Reserva:** o caminho que roda quando a ferramenta dona de uma etapa não
    está disponível.
*   **Página v2 e página antiga:** página v2 é a que tem
    `page-plan.json.schema_version: 2`. Página antiga é a que não tem
    `schema_version`.

Neste doc, **todos os caminhos de arquivo são relativos a `workspace/<slug>/`**.
Caminhos do repo começam por `.claude/`, `tools/` ou `docs/`, ou são arquivos da
raiz (`.mcp.json`, `README.md`).

## The Problem

A auditoria do page-design atual encontrou cinco causas que limitam a
qualidade. As linhas citadas são do estado atual do repo.

1.  **O QA é o modelo dando nota a si mesmo, e não fica registro.**
    *   A régua é preenchida por quem gerou a página, e "o placar não vira
        arquivo" (`regua-de-design.md:19`).
    *   A captura de tela depende da skill `webapp-testing`, que não existe no
        repo (`qualidade-e-checkpoint.md:42`).
    *   O `.claude/lib/theme-verify/verify_page.py` mede overflow e altura por
        seção e aceita `file://`, mas só roda depois do deploy.

    Os workspaces locais do dono mostram o resultado:
    *   uma página com 51 tamanhos de fonte (o T1 permite 7) e 26 gradientes;
    *   páginas aprovadas com `<script>` e com nome fora do contrato:
        `design/listicle.html` e `design/oferta.html`.
2.  **As regras dão a mesma estrutura a marcas diferentes.**
    *   O menu de seções e os blocos universais são fixos (eyebrow, heading,
        paragraph, button_row), e toda seção leva eyebrow.
    *   Toda marca abre com ABC Oracle ou Geist (`tipografia.md:7-12`). Geist é
        fonte de interface.
    *   O advertorial e o listicle trazem, além do mapa de seções, o layout, as
        URLs e as frases de uma marca específica (`page-type.md:57-69`).
3.  **As referências não são de DTC nem de design.**
    *   O board usa Pinterest via WebSearch.
    *   O Refero é um catálogo de SaaS (Cursor, Linear, Vercel).
    *   As 9 buscas de fundação na base são todas de CRO.
4.  **A marca entra tarde e se perde no caminho.**
    *   O `page/design-tokens.json` é escrito à mão depois da aprovação.
    *   O conversor de Liquid ignora esse arquivo e transforma cada hex do CSS
        em `color_1..N`, sem papel.
    *   A identidade fica em lugares diferentes:
        *   `brand.md` tem hex escritos à mão;
        *   o page-design guarda nos próprios tokens;
        *   a social-engine lê um caminho que não existe
            (`page/design/design-tokens.json`);
        *   creative-engine, retention-engine e promo-engine não leem nenhum.
5.  **A rota 2 usa o SingleFile como caminho principal.** O
    `tools/design-clone/downloader.py` já captura o DOM com estilos computados
    e caixas (`collect_computed_styles`), com proteção contra SSRF e detecção
    de Cloudflare. Mesmo assim, a rota manda o membro salvar a página pela
    extensão SingleFile, e esse arquivo não tem estilos computados. Por isso o
    esqueleto sai só com "stack/grid N" e placeholders. A rota também exige
    loja conectada, embora o page-design não escreva Liquid.

Em resumo:
*   as causas 1 e 4 pedem medição e um arquivo de marca (Goals 2, 5 e 9);
*   as causas 2 e 3 pedem direção a partir de referências melhores (Goals 3
    e 4);
*   a causa 5 pede trocar o SingleFile pelo capturador que já existe (Goal 4).

## Goals

1.  **Um dono por etapa.** Cada etapa do page-design tem uma ferramenta dona e
    uma reserva. Nenhuma etapa roda duas ferramentas para a mesma tarefa.
2.  **Marca antes da página, com uma fonte de verdade.**
    *   `brand/brand-tokens.json` (formato DTCG) é a fonte de verdade da
        marca. Nasce no setup, extraído pelo dembrandt da loja ou do site do
        próprio membro.
    *   `page/design-tokens.json` é a aplicação da marca numa página.
    *   O page-design gera a página a partir do `brand-tokens.json`. Só
        atualiza esse arquivo com a confirmação do membro (ver Technical Plan).
3.  **Direção de arte própria do produto.** A direção sai de referências
    premiadas (setor ecommerce do Awwwards) e da biblioteca de 247 sites do
    taste-skill. O membro escolhe uma entre três direções escritas. Não existe
    mais fonte padrão nem eyebrow obrigatório.
4.  **Dois modos de construção no lugar das três rotas.**
    *   **Modo direção:** absorve a rota 1. A página é feita do zero a partir
        da direção aprovada, no mesmo canvas `Artifact`.
    *   **Modo referência:** absorve as rotas 2 e 3. O `downloader.py` captura
        uma ou mais URLs. A página é construída seção por seção com o conteúdo
        e a marca do membro, e a geometria de cada seção é conferida antes da
        próxima.
5.  **QA medido e guardado antes da aprovação.**
    *   O `verify_page.py`, estendido, grava `page/qa-metrics.json`.
    *   O page-build se recusa a compilar com um item bloqueante em `fail` e
        sem liberação do membro.
    *   O julgamento estético é de um revisor sem contexto que vê as capturas
        de tela. A rubrica do próprio modelo fica só como reserva.
6.  **Checagem legal automática no modo referência.** Nenhum texto, asset,
    nome de marca ou fonte da referência pode sobrar no `page.html` final. Um
    script confere e bloqueia.
7.  **Movimento em CSS.** O movimento da referência vira CSS: scroll animado
    dentro de `@supports` (com o conteúdo visível por padrão),
    `@starting-style` e sticky. O contrato sem JavaScript continua.
8.  **Link de preview antes do Shopify.** O membro confere o layout num link
    da Vercel, aberto também no celular, junto com as capturas locais (que têm
    as fontes reais). A aprovação final de tipografia continua na 6.9 do
    page-build, no tema com as fontes de verdade.
9.  **Menos texto, não mais.**
    *   Saem as instruções duplicadas, as rotas mortas e as ferramentas
        substituídas.
    *   O `SKILL.md` continua com no máximo 12.288 bytes.
    *   Testes, `aura-check.py` e `gen_docs.py --check` passam.
10. **Critério de aceite.** O critério é atendido quando as duas condições
    abaixo valem nas mesmas 3 páginas reais dos workspaces locais, refeitas
    com o fluxo novo (uma de cada `page_type` disponível):
    *   nenhum `fail` bloqueante;
    *   o dono prefere a versão nova em pelo menos 2 das 3, numa comparação
        lado a lado sem saber qual é qual.

## Non-Goals

*   **Mudar o que o page-build consome.** Continuam iguais:
    *   `page.html` estático, sem JavaScript;
    *   `data-aura-section` em cada seção;
    *   `<style data-aura-fonts>` como primeiro bloco;
    *   os campos obrigatórios do `page-plan.json`.

    Advertorial e listicle mantêm os ids de seção fixos, ligados às 7 seções
    canônicas da copy-engine, e o botão único de compra.
*   **Gerar React, Next.js ou Tailwind.** Do 21st.dev e do cloner entra o
    método, não o código.
*   **Publicar cópia de terceiro.** O modo referência porta estrutura e layout.
*   **Movimento em JavaScript** (GSAP, Lenis, three.js).
*   **Gerar criativo de anúncio** com o plugin genjutsu ou com o brag. O plugin
    genjutsu não gera imagem nem vídeo. Não confundir com o recurso "Genjutsu"
    do Higgsfield. O Higgsfield continua sendo a rota de criativo.
*   **Rodar o EGM** (Elephant-Goldfish Model, o processo usado para escrever
    este doc) dentro da criação de página.

## Open Questions

*   **21st.dev e brag (decisão do dono, pendente).** Nenhum dos dois é dono de
    uma etapa do page-design. As opções são:
    *   (a) cortar desta mudança;
    *   (b) deixar como opcionais, instalados pelo setup só para quem quiser;
    *   (c) declarar para todos.

    Enquanto a decisão não vem, o plano trata os dois como (b).
*   **Segunda opinião no Codex, 3.8 (decisão do dono, pendente).** As opções
    são cortar, porque o revisor sem contexto cobre a mesma necessidade, ou
    manter.
*   **Outras etapas na mesma entrega (decisão do dono, pendente).** As opções
    são:
    *   (a) mesma entrega, com a Fase 5 começando só depois das Fases 1 a 4
        validadas;
    *   (b) um segundo doc.
*   **Custo de contexto dos MCPs** declarados no repo em sessões que não são
    de design. É medido na verificação. Se pesar, a mitigação é deixar as
    tools diferidas.

## Critical User Journeys (CUJs)

### CUJ 1: página nova no modo direção

*   **Given:** o membro tem `brand/brand-tokens.json` gerado no setup, o
    `page-plan.json` planejado e o MCP do Awwwards disponível.
*   **When:** ele escolhe uma direção entre as três propostas e o modo
    direção.
*   **Then:**
    *   O page-design grava `page/direction.md` e `page/design/page.html`
        construído sobre os tokens.
    *   O `page/qa-metrics.json` não tem item bloqueante em `fail`.
    *   O `page/review.md` tem a nota do revisor.
    *   Ele confere o layout num link de preview no celular e aprova a página
        pelas capturas com as fontes reais.
    *   O `page/design-tokens.json` é gerado por script.
    *   O `brand-tokens.json` não muda. A mensagem final mostra o drift da
        página contra a marca.

### CUJ 2: página nova no modo referência

*   **Given:** o membro tem uma URL de página premiada que admira e os mesmos
    arquivos do CUJ 1.
*   **When:** ele escolhe o modo referência e passa a URL.
*   **Then:**
    *   O `robots.txt` permite a captura (checado pelo próprio `downloader.py`).
    *   O `downloader.py` grava a captura em `page/reference-capture/`.
    *   Cada seção é construída com o conteúdo do membro e passa no
        `geodiff.py` antes da próxima.
    *   O `legal_check.py` passa.
    *   O resto segue como no CUJ 1.
    *   Se o robots proibir a captura, ela não roda e a skill oferece o modo
        direção.

### CUJ 3: página antiga chega ao page-build

*   **Given:** um workspace criado antes da mudança, com `page-plan.json` sem
    `schema_version` e `design_route: singlefile-clone`.
*   **When:** o membro roda o page-build.
*   **Then:** o page-build avisa que a página não tem QA medido e compila como
    hoje. Se o tema já tem a seção com settings `color_N`, os ids continuam os
    mesmos.

## Technical Plan (Architecture)

### Decisões já tomadas

*   **D1 = A (2026-10-28): dependências declaradas no repo.**
    *   As outras opções eram:
        *   B: o setup instala sob demanda;
        *   C: misto.

        Ver Alternativa D.
    *   O `.mcp.json` ganha o Awwwards (`awwwards-mcp@1.14.0`), com versão
        fixa.
    *   O `.claude/settings.json` ganha os marketplaces e plugins de
        taste-skill e dembrandt. O dembrandt entra só como plugin, que traz
        as skills e o MCP (prefixo `mcp__plugin_dembrandt_dembrandt__`), com
        versão fixa 0.3.40.
    *   O 21st.dev e o brag dependem da Open Question.
    *   A reserva continua obrigatória, porque um servidor declarado pode não
        subir na máquina do membro.
*   **D2 (2026-10-28, decisão do dono): o capturador substitui o SingleFile.**
    *   As outras opções eram:
        *   A: rota 4 nova ao lado da rota 2;
        *   C: cloner só como medição.

        Ver Alternativas B e C.
    *   As rotas 2 e 3 viram o modo referência, e a 3 é o caso de uma URL por
        seção.

### Um dono por etapa

| Etapa | Dono | Reserva | O que sai |
|---|---|---|---|
| Marca | dembrandt `get_design_tokens` + `export_dtcg`, só em URL da marca do membro | `.claude/lib/design-presets/palette_engine.py` (3 paletas, contraste AA garantido) | `brand/brand-tokens.json` |
| Referências | Awwwards `search_sites` (award `ecommerce`) + `search_elements` | Refero, depois WebSearch de concorrentes | `reference_board.references[]` com `source`; imagem das 3 marcadas tirada pelo `verify_page.py --shots-dir`; o membro marca as 3 que mais quer seguir |
| Direção | taste-skill `scripts/draw.mjs`, que sorteia 3 de 20 direções a partir da biblioteca de 247 sites, nos setores `ecommerce`, `physical-product` e `fashion`, com `--keep palette,type` quando a marca já existe | O modelo escreve 3 direções a partir do board | `page/direction.md`: tipografia, paleta, hero, blueprint por seção e o que é proibido |
| Construção, modo direção | Modelo no canvas `Artifact`, seguindo `direction.md` e as regras do taste-skill no perfil sem JS | O mesmo, sem o taste-skill | `page/design/page.html` |
| Construção, modo referência | `tools/design-clone/downloader.py --mode bands` + `tools/page-qa/geodiff.py`, seção por seção | Nenhuma necessária: é código do repo | `page/design/page.html` + `page/reference-capture/` |
| Movimento | Awwwards `get_motion_dna` / `analyze_scroll_map` na referência; receitas CSS escritas em `reference/movimento-css.md` | Item M da régua | CSS no `page.html` |
| Imagens | Higgsfield (como hoje) | `assets.mjs` do taste-skill (banco com licença comercial), depois placeholder com `acquisition_plan` (como hoje) | `page/design/assets/` |
| QA medido | `.claude/lib/theme-verify/verify_page.py` estendido | Nenhuma necessária: é código do repo | `page/qa-metrics.json` + capturas 1440/768/390 |
| QA estético | Subagente revisor sem contexto | Rubrica do modelo | `page/review.md` |
| Preview de layout | `deploy-to-vercel` sem conta (devolve `previewUrl`) | Capturas no chat | `page-plan.json.preview_url` |
| Tokens finais e drift | `tools/page-qa/tokens.py` lê as variáveis CSS do `page.html`; `tokens.py --diff` contra o `brand-tokens.json` | Nenhuma necessária: é código do repo | `page/design-tokens.json` |

Drift e contraste têm um motor só em toda a Aura: `tokens.py --diff` e
`contrast_ratio` do `palette_engine.py`. O dembrandt fica só na extração de
marca (setup e ETAPA 2).

Os **8 papéis de cor** são os que o `design-signals.json` usa hoje (`brand-signals.md:25-34`):
background, surface, foreground, primary, on_primary, accent, muted e border.

### Fluxo novo

```text
SETUP (passo 1)
  URL da loja/site do membro ─► dembrandt ─► brand/brand-tokens.json
                                              (forma vazia se não há loja)

PAGE-DESIGN (passo 7)
  ETAPA 0  leitura: fases anteriores + base (CRO e design visual)
  ETAPA 1  plano: page_type (3 sinais), sections_plan, media, commerce
           advertorial/listicle: ids fixos da copy-engine
           demais page_types: seções a partir da narrativa do produto
  ETAPA 2  marca: lê brand-tokens.json; se vazio, dembrandt numa URL da
           própria marca ou palette_engine
  ETAPA 3  referências e direção:
           awwwards.search_sites ─► board ─► membro marca 3
           taste draw.mjs ─► 3 direções ─► membro escolhe 1 ─► direction.md
  ETAPA 4  construção (membro escolhe o modo)
           direção:    canvas Artifact ─► page.html
           referência: downloader --mode bands (checa robots.txt)
                       por seção: constrói ─► geodiff ─► trava
                       legal_check ─► page.html
  ETAPA 5  QA (até 3 rodadas):
           verify_page.py ─► qa-metrics.json + capturas
           revisor sem contexto (capturas + 3 referências + direction.md)
                ─► review.md ─► correções da rodada seguinte
  ETAPA 6  preview Vercel (layout no celular) + capturas com fontes
                ─► membro aprova
           tokens.py ─► design-tokens.json; tokens.py --diff ─► drift na
                mensagem final (a marca não muda)
           page-plan.json (schema_version 2), manifest, índice

PAGE-BUILD (passo 8)
  pré-flight: qa_gate.py; schema_version 2 exige qa-metrics.json sem bloqueante em fail
              (ou com liberação em page-plan.json.qa_overrides); sem
              schema_version = legado, avisa
  6.9:        aprovação final no tema, com as fontes reais (como hoje)
  conversor:  papéis de cor nas seções novas; color_N mantido em seções já no tema
  6.11:       drift de tokens da página no ar
```

### QA: o que bloqueia

O `qa-metrics.json` tem um item por medida, cada um com `pass`, `warn` ou
`fail`.

**Itens bloqueantes:**
*   `script_tags`;
*   `section_markers`;
*   `section_ids_match_plan`;
*   `horizontal_overflow`;
*   `section_height_zero` (seção com altura 0, a medida de hoje);
*   `broken_images`;
*   `html_css_kb`: HTML+CSS sem o bloco `data-aura-fonts`, acima de 150 KB,
    que é o limite atual do page-design;
*   `legal_check`, só no modo referência. O `legal_check.py` grava o
    resultado, e o `verify_page.py --legal` o transforma em item.

Os outros itens são `warn`:
*   contraste;
*   tamanhos de fonte distintos;
*   gradientes;
*   largura de linha (45 a 75 caracteres);
*   headline com mais de 2 linhas em 390;
*   margens;
*   faixas vazias;
*   `page_total_kb` acima de 1,5 MB;
*   `console_errors` e `geodiff` (nota abaixo de 70 no modo referência).

Um item bloqueante em `fail` depois das 3 rodadas vai para o membro decidir, como
hoje.
*   **Itens de contrato, nunca liberáveis:** `script_tags`, `section_markers`,
    `section_ids_match_plan` e `legal_check`. Sem eles o page-build não
    compila ou a página expõe material de terceiro. Também não se libera
    `section_height_zero`, porque é uma seção que renderizou vazia.
*   **Liberáveis:** `horizontal_overflow`, `broken_images` e `html_css_kb`. O
    membro registra `{item, motivo, data}` em `page-plan.json.qa_overrides`.

O `verify_page.py` só mede e regrava o `qa-metrics.json` do zero a cada
rodada. Quem combina medição e liberação é o pré-flight do page-build.

### O revisor sem contexto

É um subagente com prompt fixo em
`.claude/skills/page-design/reference/revisor.md`.

*   **Recebe:**
    *   as capturas de 1440 e 390 que o `verify_page.py` tira;
    *   as imagens das 3 referências marcadas pelo membro, que a ETAPA 3 grava
        no board;
    *   o `direction.md`.

    Não recebe a conversa.
*   **Devolve** o `review.md`, com:
    *   nota de 1 a 5 em tipografia, espaço, cor, hierarquia, aderência à
        direção e sinais de "feito por IA";
    *   as 5 correções de maior impacto.
*   **Poder:** não bloqueia. As correções dele definem a rodada seguinte.

### Componentes novos e estendidos

1.  **`.claude/lib/theme-verify/verify_page.py` (estendido).** Ganha:
    *   o perfil design (`--json-out`): a largura 768 e o JSON; sem a flag, o
        comportamento usado pela loja não muda;
    *   os itens da seção "QA: o que bloqueia";
    *   uma saída `--json-out`.

    O contraste usa `relative_luminance` e `contrast_ratio` do
    `palette_engine.py`. O `verify_page.py` já aceita `file://` e conhece
    `data-aura-section`, então não nasce outro script de medição.
2.  **`tools/design-clone/downloader.py --mode bands` (estendido).** O
    downloader já captura estilos computados e caixas. O modo novo divide a
    página em faixas (filhos de primeiro nível com mais de 120px de altura) e
    grava:
    *   `bands.json`;
    *   `section-NN.json`;
    *   `texts.json`;
    *   `assets.json`.

    Continuam valendo `validate_url` (SSRF), `validate_output_path` e a
    detecção de Cloudflare. No mesmo ponto do `validate_url`, o modo novo
    checa o `robots.txt` com `urllib.robotparser` (stdlib) e não captura se
    ele proibir.
3.  **`tools/page-qa/geodiff.py` (novo).** Recebe a captura do `page.html` feita
    pelo `downloader.py` no mesmo modo `bands`. Compara cada par de seções (referência contra página): altura,
    número de colunas e posição relativa dos blocos de texto, mídia e CTA. Dá
    uma nota de 0 a 100 por seção.
4.  **`tools/page-qa/legal_check.py` (novo).** Falha quando encontra no
    `page.html`:
    *   frase de 6 palavras ou mais igual a uma frase da referência, fora da
        allowlist de frases genéricas em `tools/page-qa/legal_allowlist.txt`;
    *   URL ou nome de arquivo de asset da referência;
    *   `font-family` da referência que não veio da direção escolhida nem do
        setup;
    *   o nome da marca da referência.
5.  **`tools/page-qa/tokens.py` (novo).** Gera o `design-tokens.json` a partir
    das variáveis CSS do `:root` e do `<style data-aura-fonts>` do
    `page.html`, no schema atual, com `source` e `provision` direto no
    arquivo. Com `--brand-out`, gera DTCG (usado só quando a marca está
    vazia). Com `--diff`, dá o drift entre dois arquivos de tokens. É o único
    motor de drift da Aura.
6.  **Schemas** em `.claude/templates/schemas/`:
    *   `page-plan`, que sustenta o gate de `schema_version`;
    *   `brand-tokens`, o contrato entre as etapas.
7.  **Testes** em `tools/tests/` para os quatro scripts.

### Política do arquivo de marca

*   O setup cria o `brand-tokens.json`. O dembrandt só roda em URL da marca do
    membro. URL de terceiro nunca vira marca.
*   O page-design só escreve na marca quando ela está vazia (`source:
    "none"`): grava os tokens da página aprovada com `tokens.py --brand-out`.
    A escolha do membro na comparadora já conta como confirmação.
*   Fora desse caso, o page-design nunca escreve na marca. O drift da página
    contra a marca (`tokens.py --diff`) aparece na mensagem final.
*   Para mudar a marca, o membro refaz a extração do setup ou edita o arquivo.
*   Em página v2 o `design-signals.json` deixa de ser gravado: a ETAPA 2 lê o
    `brand-tokens.json`, e os papéis de cor e famílias da página ficam no
    `design-tokens.json`. O page-build só lê o `design-signals.json` em
    páginas sem `schema_version`.

### O que sai

| Item | Por quê | Quem cita (a ajustar) |
|---|---|---|
| `reference/rota-claude-design.md` | O modo direção absorve a rota 1 | `SKILL.md:61`, `menu-de-rotas.md` |
| `reference/rota-singlefile-clone.md` | O modo referência substitui (D2) | `SKILL.md:3,20,62,63`, `menu-de-rotas.md`, `contexto.md:9`, `page-plan-e-salvar.md:60-61`, `design-tokens.md:7`, `mensagem-final-e-self-audit.md:12`, `qualidade-e-checkpoint.md:16,59`, `normalizacao-html-externo.md:3`, `refero-integration/README.md:93`, `OVERVIEW.md:173,567`, `setup/reference/dependencias.md:43-52` |
| `reference/rota-section-puzzle.md` | Vira caso do modo referência. O teste de vizinhança é mantido. | `menu-de-rotas.md`, `SKILL.md:64` |
| `reference/menu-de-rotas.md` | Dois modos cabem em 2 linhas no `SKILL.md` | `SKILL.md:60` |
| `reference/contexto.md` | Repete o fluxo do `SKILL.md` | `SKILL.md` |
| `tools/design-clone/snapshot.py`, `analyzer.py`, `pattern-extractor.py`, `preview.py`, `aura_clone.py` | SingleFile, clone-and-adapt e sinais por design-clone. O `downloader.py` fica. | `brand-signals.md:72-80`, `SKILL.md:53`, `mcp-detect/README.md:66`, `dependencias.md:44`, `OVERVIEW.md:565` |
| Scripts descartáveis de `tools/design-clone/` (`_render*.py`, `_probe.py`, `_study.py`, `_colors.py`, `_map_assets.py`, `_gen_template*.py`) | Têm caminhos fixos em `/tmp` e ninguém usa | nenhum |
| Caminhos 2 (print lido por visão) e 3 (design-clone) de `brand-signals.md` | dembrandt + `palette_engine` cobrem | `brand-signals.md`, `mcp-detect/README.md` |
| Em `page-type.md:57-69` e `qualidade-e-checkpoint.md:21`: URLs, frases e estética de uma marca específica | Davam a mesma página a todos | os mesmos. **Ficam:** mapa de ids das 7 seções, botão único com `#offer`, parada quando falta seção na copy |
| Fonte padrão ABC Oracle/Geist e "uma família por padrão" | A tipografia vem da direção | `tipografia.md`, `design-presets/README.md` |
| Eyebrow obrigatório | Passa a ser opcional | `eyebrows.md`, `sections-e-hero.md`, `page-plan-e-salvar.md` |
| Duplicações | Travessão (3 cópias), teto de 3 rodadas (2), D6 repete o bloco S, parágrafo de 5 KB do self-audit | `regua-de-design.md`, `qualidade-e-checkpoint.md`, `mensagem-final-e-self-audit.md` |
| Referência à skill `webapp-testing` | Não existe; o `verify_page.py` tira as capturas | `qualidade-e-checkpoint.md:42`, `brand-signals.md:60` |

**Ficam:**
*   em `tools/design-clone/`:
    *   `downloader.py`, estendido;
    *   `liquid-converter.py`;
    *   `_css_utils.py`;
    *   `_venv_bootstrap.py`;
    *   o `.venv`;
    *   o `requirements.txt`.
*   no page-design:
    *   a decisão do `page_type` por três sinais;
    *   o mapa de mídia com bloqueio de placeholder;
    *   o bloco `commerce`;
    *   o `palette_engine.py`;
    *   o `local_fonts.py`;
    *   os critérios da régua, agora medidos ou julgados pelo revisor.

### Mudanças em outras etapas

Dependem da Open Question sobre a entrega. A tabela abaixo descreve o
conteúdo, não o momento em que entra.

| Etapa | Mudança | Arquivo |
|---|---|---|
| setup | Extrai a marca com o dembrandt (o fetch atual vira reserva) e grava `brand/brand-tokens.json`; o `brand.md` aponta para esse arquivo | `setup/reference/onboarding-e-extracao.md:65-68`, `profile-e-brand.md:57`, `.claude/templates/brand.md.template`, `dependencias.md` |
| page-build | Pré-flight por `schema_version`; papéis de cor nas seções novas; drift na 6.11 | `page-build/SKILL.md`, `validate.md:25`, `deploy.md:72,164-173`, `tools/design-clone/liquid-converter.py:271` |
| consistency-audit | O M6 vira drift + contraste | `consistency-audit/reference/checks-medium.md:35-37` |
| checkout-aov | Drift do `/cart` contra os tokens | `checkout-aov/reference/carrinho-e-drawer.md:54` |
| social-engine | Corrige o caminho errado; lê o `brand-tokens.json` | `social-engine/SKILL.md:27`, `skills.json:1011`, `templates-marketing-studio.md:10,40` |
| creative-engine | "Senso Estético" lê a paleta e as fontes | `creative-engine/reference/briefing.md:56` |
| retention-engine | Emails com a paleta, fontes com fallback web-safe e contraste do botão | `retention-engine/reference/salvar-e-regras.md` |
| promo-engine | O banner lê a paleta | `promo-engine/reference/criativos-da-janela.md:13-14` |
| mcp-detect | Prefixos `mcp__awwwards__` e `mcp__plugin_dembrandt_dembrandt__`; `source` novos; sai `design_clone` | `.claude/lib/mcp-detect/README.md` |

O caminho errado da social-engine é um bug e entra em qualquer caso.

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| O script mede o piso, não o teto. Uma direção fraca passa em todos os testes. | Direção a partir de referências premiadas; revisor sem contexto que vê a página; critério de aceite (Goal 10) |
| Tempo e custo por página sobem | Um dono por etapa. No modo referência, no máximo 10 seções e 2 rodadas de geometria por seção; depois disso a nota do `geodiff` vira `warn` no `qa-metrics.json` e a seção segue para o revisor. A estimativa em tokens e minutos é medida na verificação e entra aqui. |
| Ferramentas se sobrepõem (três extraem tokens, três clonam, quatro dão direção, quatro fazem QA) | Tabela "Um dono por etapa"; o capturador e o QA são do repo |
| Ferramentas assumem JavaScript (`stage.js`, gate `html.js`, GSAP, código React) | Perfil sem JS escrito no `modo-direcao.md`; o `verify_page.py` bloqueia `<script>` |
| Portar CSS real fica mais perto da cópia | `legal_check.py` bloqueante e não liberável; robots respeitado |
| MCP declarado não sobe na máquina do membro | Toda etapa tem reserva; QA e captura são código do repo |
| Plugins e MCPs de terceiros mudam de versão | Versões fixas no `.mcp.json` e nos plugins; atualização só por commit no repo |
| Gate novo trava o membro | Lista fechada de bloqueantes; os que não são de contrato aceitam liberação registrada |

## Alternatives Considered

### Alternativa A: manter as três rotas e só acrescentar ferramentas

*   **Prós:**
    *   diff pequeno;
    *   nada que os membros conhecem muda.
*   **Contras:**
    *   não mexe nas causas 2 e 5;
    *   as ferramentas rodariam por cima de regras que dão a mesma estrutura
        a todas as marcas.
*   **Por que foi rejeitada:** o dono pediu páginas de nível agência e
    autorizou cortar o que atrapalha.

### Alternativa B: rota 4 nova ao lado da rota 2 (D2-A)

*   **Prós:** não mexe numa rota em uso.
*   **Contras:**
    *   duas rotas que portam estrutura;
    *   a rota 2 continuaria sem estilos computados.
*   **Por que foi rejeitada:** decisão do dono. Com o capturador, o SingleFile
    não tem mais função.

### Alternativa C: o método do cloner só como medição (D2-C)

*   **Prós:**
    *   nenhuma rota porta CSS de terceiro;
    *   diff menor.
*   **Contras:** a medição aponta a distância até a referência, mas nenhuma
    etapa fecha essa distância.
*   **Por que foi rejeitada:** o modo referência com `legal_check.py` entrega a
    fidelidade e mantém a regra legal verificável.

### Alternativa D: dependências instaladas sob demanda (D1-B) ou misto (D1-C)

*   **Prós:** menor custo de contexto para quem não usa.
*   **Contras:**
    *   quem pula o passo roda sempre na reserva, sem aviso;
    *   o QA varia entre membros.
*   **Por que foi rejeitada:** decisão do dono (D1 = A).

### Alternativa E: plugin genjutsu (`bunshin` ou `paint`) como motor da página

*   **Prós:** pipeline pronto do brainstorm à auditoria.
*   **Contras:**
    *   o `bunshin` declara de 6 a 13 milhões de tokens e de 3 a 10 horas por
        site;
    *   o `paint` tem um gate humano por pergunta;
    *   as sub-skills padrão usam GSAP, three.js e framer-motion;
    *   o `MASTER.md` duplicaria o `direction.md`.
*   **Por que foi rejeitada:** custo e conflito com o contrato sem JS. As
    receitas de CSS dele são reescritas no `movimento-css.md`.

### Alternativa F: o `inspect.mjs` do taste-skill como QA medido

*   **Prós:** já mede headline, fontes, contraste, margens e faixas vazias.
*   **Contras:**
    *   o QA bloqueante dependeria de Node 22+ e de um plugin com versão fora
        do repo;
    *   o `MOTION_MIN = 8` reprova páginas com pouco movimento;
    *   o `verify_page.py` já existe.
*   **Por que foi rejeitada:** o piso de QA precisa ser código da Aura. Os
    critérios úteis do `inspect.mjs` entram no `verify_page.py`.

### Alternativa G: `clone-website` do dembrandt ou `section-loop` do Awwwards como método do modo referência

*   **Prós:** métodos prontos, com nota por seção (Awwwards) ou drift por token
    (dembrandt).
*   **Contras:**
    *   duplicam o `downloader.py`, que já tem captura com estilos computados e
        proteções de segurança;
    *   deixariam uma pergunta sem resposta no caminho principal: o
        `verify_build` aceita `file://`?
*   **Por que foi rejeitada:** um dono por etapa. O Awwwards fica na busca e no
    estudo de movimento.

### Alternativa H: gerar React ou Next.js e hospedar na Vercel

*   **Prós:** usa direto o código do 21st.dev e do cloner; movimento livre.
*   **Contras:** a loja é Shopify. Uma página externa quebraria:
    *   checkout;
    *   carrinho;
    *   tracking;
    *   edição pelo membro.
*   **Por que foi rejeitada:** contradiz o contrato do page-build.

### Alternativa I: movimento em JavaScript como asset do tema

*   **Prós:** movimento de site premiado.
*   **Contras:**
    *   o conversor tira `<script>` e o GATE 1 proíbe;
    *   exige pipeline novo;
    *   custo de performance no celular.
*   **Por que foi rejeitada:** CSS cobre scroll animado, `@starting-style` e
    sticky. O que não couber em CSS fica listado no `review.md` de cada
    página, e essa lista mede quanto se perde. Fica em Future Improvements.

--------------------------------------------------------------------------------

## Non-Functional Requirements

*   **Segurança e privacidade:**
    *   **Chaves:** se o 21st.dev entrar, a chave `TWENTYFIRST_API_KEY` fica
        no `.env`. A leitura desse arquivo já é negada no `settings.json`. O
        preview da Vercel roda sem conta, então não há token.
    *   **Material de terceiro:** a captura (`page/reference-capture/`) fica
        em `workspace/`, que não é commitado (regra 11), e nunca vai para o
        tema.
    *   **robots.txt:** o `downloader.py --mode bands` checa com
        `urllib.robotparser`. Se o robots proíbe, a captura não roda.
    *   **Preview:**
        *   É público para quem tem o link, e o membro é avisado disso.
        *   Usa as fontes de fallback, nunca os arquivos de
            `page/design/assets/fonts/`. Isso mantém a promessa de
            `tipografia.md:14` de que a Aura não hospeda fonte. Por isso o
            link serve para layout, e a tipografia é aprovada nas capturas
            locais e na 6.9.
        *   Depois da aprovação, o preview é removido quando a ferramenta
            permitir. Se não permitir, o aviso diz isso.
    *   **Dados que saem da máquina do membro:**

        | Serviço | O que recebe |
        |---|---|
        | Awwwards | termos de busca |
        | dembrandt | roda local e acessa só as URLs passadas |
        | Vercel | a pasta `page/design/` sem fontes |
    *   **Supply chain:** as versões são fixas no `.mcp.json` e nos plugins. A
        atualização só acontece por commit no repo.
*   **Desempenho e custo:**
    *   O `SKILL.md` continua com no máximo 12.288 bytes.
    *   As referências do caminho principal precisam somar menos que os ~140
        KB de hoje, medido com `wc -c`.
    *   Os tetos do modo referência estão em Riscos e mitigações.
*   **Rollout e rollback:**
    *   **Rollout:** os membros recebem a mudança pelo auto-update
        (fast-forward). Página nova grava `page-plan.json.schema_version: 2`.
        No page-build:
        *   página sem `schema_version` é legado e recebe só um aviso;
        *   página v2 sem `qa-metrics.json` é bloqueada.
    *   **Conversor:** usa papéis de cor só em seções novas. Seções que já
        estão no tema mantêm os ids `color_N`, para não perder edições do
        membro.
    *   **Rollback:** é um `git revert`.
        *   O código antigo ignora campos desconhecidos do `page-plan.json`.
        *   Um `design_route` novo cai no caminho padrão da validação.
        *   Os plugins instalados continuam na máquina, sem efeito na Aura
            antiga.

--------------------------------------------------------------------------------

### Additional Resources

| Ferramenta | Origem | Versão usada |
|---|---|---|
| taste-skill | plugin `Leonxlnx/taste-skill` | 2.1.5 |
| dembrandt (skills + MCP) | plugin `dembrandt/dembrandt-skills` (traz o MCP) | 0.3.40 |
| genjutsu | plugin `AThevon/genjutsu` (só como fonte das receitas de CSS) | 4.1.1 |
| brag | plugin `latent-spaces/brag` | 0.5.0 |
| Awwwards MCP + skills | `npx awwwards-mcp` (skills `awwwards-*` instaladas junto) | 1.14.0 |
| 21st.dev MCP | `https://21st.dev/api/mcp` | — |
| deploy-to-vercel | skill da Vercel | — |
| ai-website-cloner-template | https://github.com/JCodesMore/ai-website-cloner-template (o método; o código não é usado) | — |
| EGM | https://github.com/google/elephant-goldfish-model | 0.1.0 |

**Algoritmo do `geodiff.py`:**
1.  Captura referência e página com o modo `bands`.
2.  Liga cada faixa da referência à seção da página pelo mapa
    `ref-band:aura-section`.
3.  Por par de seções, compara três medidas, normalizadas pela largura da
    viewport:
    *   diferença de altura;
    *   número de colunas da grade principal;
    *   centro e tamanho das caixas de texto, mídia e CTA.
4.  Converte as diferenças numa nota de 0 a 100 e lista as 5 maiores.

### Future Improvements

*   **Interação sem JavaScript:** uma biblioteca de padrões testados com
    `:has()`, `<details>` ou radio (seletor, antes e depois).
*   **Movimento em JS como asset do tema** (Alternativa I). Gatilho: a nota
    média do revisor em movimento fica abaixo de 3 em 2 de 3 páginas do
    critério de aceite.
*   **Fechar o ciclo com conversão.** Ligar `qa-metrics.json` e `review.md` à
    taxa de conversão real (tracking-setup) para calibrar os limites com
    dados.

--------------------------------------------------------------------------------

## Detailed Implementation Plan

A implementação tem sete fases, da 0 à 6. Cada fase termina com testes e lint
passando e vira um commit. A ordem garante que nada fique quebrado entre uma
fase e outra:
*   **Fase 0:** as dependências (MCPs, plugins e skills de terceiros) ficam
    declaradas antes de qualquer etapa chamá-las.
*   **Fases 1 e 2:** os scripts novos existem antes de alguém usá-los.
*   **Fase 3:** a skill passa a usá-los.
*   **Fase 4:** o page-build passa a exigi-los, com tolerância para páginas
    antigas.
*   **Fase 5:** as outras etapas da Aura (Open Question sobre a entrega).
*   **Fase 6:** a documentação, a limpeza de citações e, por último, a
    remoção dos scripts antigos (item 47).

Antes da Fase 0, o status deste doc passa a `Approved`.

**Caminhos:** os que começam por `.claude/`, `tools/` ou `docs/`, e os arquivos
da raiz (`.mcp.json`, `README.md`), são relativos à raiz do repo. Os que
começam por `page/` ou `brand/` são relativos a `workspace/<slug>/`, como no
glossário.

**Termos:** "página v2" é a que tem `page-plan.json.schema_version: 2`.
"Página antiga" é a que não tem `schema_version`.

**Decisões abertas:** até o dono decidir, o plano segue estes padrões:
*   **Codex (3.8):** mantida (item 30, "se manter").
*   **21st.dev e brag:** opção (b). Ficam fora do `.mcp.json` e do
    `settings.json`. O `dependencias.md` (item 12) os lista como opcionais,
    com o comando de instalação de cada um.
*   **Outras etapas:** opção (a). A Fase 5 começa depois das Fases 0 a 4
    validadas.

### Fase 0: dependências declaradas

#### 0a. `.mcp.json` (modificar)

*   **Mudança:** acrescenta
    `"awwwards": {"command": "npx", "args": ["-y", "awwwards-mcp@1.14.0"]}`.
    O dembrandt não entra aqui: vem só pelo plugin do item 0b, que traz as
    skills e o MCP, para não subir dois servidores.
*   **Por quê:** D1 = A.

#### 0b. `.claude/settings.json` (modificar)

*   **Mudança:** acrescenta, sem tocar no que já existe:

    ```json
    "extraKnownMarketplaces": {
      "taste-skill": {"source": {"source": "github", "repo": "Leonxlnx/taste-skill", "ref": "v2.1.5"}},
      "dembrandt": {"source": {"source": "github", "repo": "dembrandt/dembrandt-skills"}}
    },
    "enabledPlugins": {
      "taste-skill@taste-skill": true,
      "dembrandt@dembrandt": true
    }
    ```

    *   **Versão:** o `ref` de um marketplace aceita só branch ou tag (schema
        oficial do `settings.json`). O taste-skill tem a tag `v2.1.5` e fica
        fixo nela. O dembrandt não publica tag da 0.3.40, então segue a
        branch padrão. Quando houver tag, o `ref` entra.
    *   **Prefixo:** o plugin `dembrandt@dembrandt` expõe o MCP como
        `mcp__plugin_dembrandt_dembrandt__`. Na máquina do autor, essa é a
        combinação que gera o prefixo.
    *   **genjutsu:** não entra. As receitas de CSS ficam escritas no
        `movimento-css.md`.
*   **Por quê:** D1 = A, dentro do que cada fornecedor distribui.

#### 0c. `.claude/lib/mcp-detect/README.md` (modificar)

*   **Mudança:**
    *   Linhas novas na tabela de prefixos, cada uma com a cascata:
        *   `mcp__awwwards__`: referências e movimento → Refero → WebSearch;
        *   `mcp__plugin_dembrandt_dembrandt__`: só extração de marca (setup
            e ETAPA 2) → `palette_engine.py` → manual.
    *   `source` novos: `awwwards`, `dembrandt`, `brand_tokens` e
        `palette_engine`.
    *   A tabela "onde está documentado" ganha as duas linhas novas.
    *   A linha `design_clone` (linha 66) e o design-clone na cascata do
        Refero (linha 18) só saem no item 19, quando a página deixa de usar
        esse caminho. Assim o README não descreve um fluxo que ainda não
        existe.
*   **Por quê:** é a fonte única de detecção.

### Fase 1: ferramentas de QA, captura e tokens

Nenhuma skill chama estes scripts ainda. A única mudança visível é no
`verify_page.py`, e só com `--json-out`: sem a flag, ele faz exatamente o que
faz hoje.

#### 1. `.claude/lib/theme-verify/verify_page.py` (modificar)

*   **Hoje:** roda `_bootstrap()` no import (linhas 28 a 47), mede overflow
    horizontal e altura de seção em 1440 e 390 (linhas 55 a 59) e sai com 1 se
    algo falhar. O page-build chama na loja real (`deploy.md:130`).
*   **Dois perfis:**
    *   **Sem `--json-out` (perfil loja):** igual a hoje. Mesmas larguras,
        mesma saída em texto, mesmos exit codes. Um tema Shopify sempre tem
        `<script>`, então os itens novos não rodam aqui.
    *   **Com `--json-out <qa-metrics.json>` (perfil design):** acrescenta a
        largura 768, roda todos os itens da tabela abaixo e grava o JSON.
*   **Estrutura:** o perfil loja (`check_viewport`) fica intacto. O perfil
    design é uma função à parte (`measure_design` + `design_items`): uma
    passada de JavaScript por largura devolve os dados crus, e os limites
    ficam no Python. Assim o caminho que o page-build usa hoje não muda.
*   **Flags novas:**
    *   `--json-out <qa-metrics.json>`;
    *   `--plan <page-plan.json>`, para `section_ids_match_plan`;
    *   `--legal <legal.json>`: a saída do `legal_check.py` vira o item
        `legal_check`;
    *   `--geodiff <geodiff.json>`: a saída do `geodiff.py` vira o item
        `geodiff`;
    *   `--dump-computed <computed.json>`: funciona nos dois perfis e grava,
        por `data-aura-section`, a cor de texto, o fundo efetivo, a cor do
        botão principal e a `font-family` computada de `h1`, `h2` e `p`. É a
        entrada do drift da página no ar (itens 35 e 43).

    O `--shots-dir` já existe (linhas 18 e 155). No perfil design, ele tira
    também a captura de 768.
*   **Itens do perfil design:**

    | id | Como mede | Limite | Largura | Bloqueante |
    |---|---|---|---|---|
    | `script_tags` | `<script>` no DOM, fora de `type="application/ld+json"` | 0 | 1440 | sim |
    | `section_markers` | filhos de primeiro nível do `main` (ou do `body`, se não houver `main`), com altura > 0, sem `data-aura-section`; ignora `header`, `footer`, `nav`, `style`, `link` | 0 | 1440 | sim |
    | `section_ids_match_plan` | lista de `data-aura-section` na ordem do DOM igual a `page-plan.json.section_order`; sem `--plan`, o status é `skip` | igual | 1440 | sim |
    | `horizontal_overflow` | a medida de hoje (linhas 104 a 106) | 0 px | 390, 768, 1440 | sim |
    | `section_height_zero` | a medida de hoje (linhas 125 a 133) | 0 seções | 390, 1440 | sim |
    | `broken_images` | `img` com `complete` e `naturalWidth == 0` | 0 | 1440 | sim |
    | `html_css_kb` | bytes do HTML mais os CSS locais linkados, menos o bloco `<style data-aura-fonts>` | 150 KB | — | sim |
    | `legal_check` | `pass` do `--legal`; modo referência sem `--legal` é `fail`; modo direção é `skip` | `pass` | — | sim |
    | `page_total_kb` | HTML mais todos os arquivos que ele carrega (em `file://`, o tamanho em disco) | 1.536 KB | — | não |
    | `contrast` | cada elemento com texto próprio: cor computada contra o fundo efetivo (primeiro ancestral com `background-color` opaco; fundo só de imagem é `skip`). Converte `rgb()` com `rgb_to_hex` e mede com `contrast_ratio` | 4,5 (3,0 a partir de 24 px, ou 18,66 px em negrito) | 390, 1440 | não |
    | `font_sizes_distinct` | conjunto de `font-size` computados de elementos com texto | 7 (T1) | 1440 | não |
    | `gradients` | elementos com `gradient` no `background-image` | 3 | 1440 | não |
    | `line_length` | por `p` com mais de uma linha: largura ÷ (0,5 × `font-size`), como caracteres por linha | 45 a 75 | 1440 | não |
    | `headline_lines` | linhas do primeiro `h1`: altura ÷ `line-height` | 2 | 390 | não |
    | `equal_side_margins` | por seção, diferença entre a margem esquerda e a direita do primeiro filho com conteúdo | 8 px | 1440 | não |
    | `empty_bands` | faixas verticais sem texto, imagem nem vídeo | 60% da altura da viewport | 1440 | não |
    | `geodiff` | `min_score` do `--geodiff`; sem a flag, `skip` | 70 | — | não |
    | `console_errors` | a medida de hoje (linhas 140 a 145) | 0 | 1440 | não |

*   **Imports:** `palette_engine.py` vem de `.claude/lib/design-presets/`, com
    a pasta posta no `sys.path`, como faz `tools/tests/test_palette_engine.py`
    nas linhas 24 a 26. Usa `rgb_to_hex` (linha 169), `relative_luminance` e
    `contrast_ratio`.
*   **Só mede:** regrava o JSON do zero a cada rodada e não lê liberações.
    Quem combina medição e liberação é o `qa_gate.py` (item 9a).
*   **Exit code no perfil design:** 1 se existir item bloqueante em `fail`.
*   **Saída:**
    `{version: 1, page, page_sha256, widths, items:[{id, status, blocking, value, limit, width, detail}], blocking_fail}`.
    O `page_sha256` é o hash do `page.html` medido.
*   **Por quê:** Goal 5, com um script de medição só.

#### 2. `tools/design-clone/downloader.py` (modificar)

*   **CLI:** passa a usar `argparse`, mantendo os dois posicionais de hoje
    (linhas 878 a 881):
    `downloader.py <url> <output_dir> [--mode full|bands] [--widths 1440,390]`.
    `--mode full` é o padrão e faz o que faz hoje.
*   **Viewport:** `_launch_stealth` (linhas 289 a 302) recebe a largura, em
    vez do 1440 fixo da linha 95.
*   **URL `http(s)`:** passa pelo `validate_url` como hoje. Logo depois, o
    `robots.txt` é checado com `urllib.robotparser`:
    *   se proibir, sai com exit code 2 e a mensagem que a skill mostra ao
        membro;
    *   se o `robots.txt` não existir (404), segue, como manda o padrão;
    *   se der erro de rede, segue com aviso.
*   **URL `file://`:** é um ramo à parte. O `validate_url` continua recusando
    `file` (linhas 165 e 193 a 196). O caminho local precisa estar dentro de
    `workspace/`, conferido com a mesma lógica do `validate_output_path`. Não
    checa robots.
*   **Modo `bands`:**
    *   Reaproveita `auto_scroll`, `collect_computed_styles`,
        `extract_image_urls` (linhas 554 a 579) e a detecção de Cloudflare.
    *   **Faixas:** começa no `main` (ou no `body`). Enquanto houver um filho
        só com mais de 90% da altura, desce para ele. Depois, cada filho com
        mais de 120 px de altura é uma faixa, numerada a partir de `00`.
    *   **Arquivos**, em `<output_dir>/<largura>/`:
        *   `bands.json`: `{url, width, bands:[{index, tag, selector, top, height, background}]}`;
        *   `section-NN.json`: os estilos computados que o
            `collect_computed_styles` já coleta, só os da faixa NN;
        *   `texts.json`: `[{band, tag, text}]`, todo texto visível;
        *   `assets.json`: `[{band, url}]`, a saída do `extract_image_urls`
            por faixa.
    *   Não baixa assets.
    *   **Falhas:** os exit codes 3 e 5 de hoje (desafio do Cloudflare e
        fallback de screenshot) mantêm o significado. No modo referência, a
        skill para e oferece o modo direção (item 22).
*   **Limpeza:** as linhas 8 a 10, 25, 66 e 681 deixam de citar analyzer,
    `aura_clone`, SingleFile e `snapshot.py`.
*   **Por quê:** Goal 4 e D2. É o único capturador do modo referência e
    alimenta o `geodiff.py` e o `legal_check.py`.

#### 3. `tools/page-qa/geodiff.py` (criar)

*   **Interface:**
    `geodiff.py --ref <dir>... --page <page-capture-dir> --map <ref-idx>:<band-idx>:<aura-section>,... --out <geodiff.json>`.
    *   `<ref-idx>` é a posição do diretório na lista `--ref`. Assim o modo
        quebra-cabeça, com uma URL por seção, cabe na mesma interface.
    *   `<band-idx>` é o `index` do `bands.json` da referência.
    *   Do lado da página, a seção é o elemento com aquele
        `data-aura-section`, achado pelo `selector` do `bands.json` da
        captura do `page.html`.
*   **Nota por seção e por largura (1440 e 390):**
    `100 − 40 × min(1, |Δaltura| ÷ altura_ref) − 30 × (colunas diferentes ? 1 : 0) − 30 × min(1, deslocamento_médio ÷ 0,25)`.
    *   Colunas são as da grade principal da faixa.
    *   O deslocamento é a distância média entre os centros das caixas de
        texto, mídia e CTA, normalizada pela largura da viewport.
    *   A nota da seção é a menor das duas larguras.
*   **Saída:** `{version: 1, sections:[{aura_section, ref, band, score, by_width, top_diffs}], min_score}`.
*   **Exit code:** 1 se alguma seção ficar abaixo de 70. Nota 70 passa.
*   **Por quê:** é a trava "constrói, mede, trava, próxima" do modo referência.

#### 4. `tools/page-qa/legal_check.py` e `tools/page-qa/legal_allowlist.txt` (criar)

*   **Interface:**
    `legal_check.py --ref <dir>... --page <page.html> --allowed-fonts <direction.md|brand-tokens.json>... [--ref-brand <nome>]... --out <legal.json>`.
*   **Regras** (as quatro de Technical Plan > Componentes novos e estendidos >
    `legal_check.py`):
    *   **Texto:** depois da normalização (caixa baixa, sem pontuação,
        espaços colapsados), qualquer sequência de 6 palavras seguidas que
        aparece no `texts.json` da referência e no `page.html`. Fica isenta a
        sequência contida numa linha da allowlist.
    *   **Asset:** URL ou nome de arquivo do `assets.json` da referência que
        aparece no `page.html`.
    *   **Fonte:** `font-family` dos `section-NN.json` da referência usada no
        `page.html` e ausente das fontes permitidas. As permitidas são as do
        bloco `## Tipografia` do `direction.md` (formato fixo no item 18) e as
        de `typography` do `brand-tokens.json`.
    *   **Marca:** cada `--ref-brand` encontrado no `page.html`. Sem a flag, o
        nome sai do domínio de cada `bands.json.url` (por exemplo,
        `www.loja-x.com` dá `loja x`).
*   **Allowlist:** frases genéricas de DTC, uma por linha (por exemplo,
    "30 day money back guarantee", "free shipping on all orders").
*   **Saída:** `{version: 1, pass, findings:[{rule, match, ref, where}]}`.
*   **Exit code:** 1 se encontrar algo.
*   **Por quê:** Goal 6.

#### 5. `tools/page-qa/tokens.py` (criar)

*   **Contrato de nomes:** é o mesmo no `page.html`, no `design-tokens.json`,
    no `brand-tokens.json` e no conversor (item 34).

    | Papel | Variável CSS no `:root` | Caminho DTCG no `brand-tokens.json` |
    |---|---|---|
    | background | `--color-background` | `color.background` |
    | surface | `--color-surface` | `color.surface` |
    | foreground | `--color-foreground` | `color.foreground` |
    | primary | `--color-primary` | `color.primary` |
    | on_primary | `--color-on-primary` | `color.on_primary` |
    | accent | `--color-accent` | `color.accent` |
    | muted | `--color-muted` | `color.muted` |
    | border | `--color-border` | `color.border` |
    | família de título | `--font-heading` | `typography.heading.fontFamily` |
    | família de texto | `--font-body` | `typography.body.fontFamily` |
    | escala de tipo | `--text-<n>` | `dimension.text.<n>` |
    | espaçamento | `--space-<n>` | `dimension.space.<n>` |
    | raio | `--radius-<n>` | `dimension.radius.<n>` |
    | sombra | `--shadow-<n>` | `shadow.<n>` |

    Cada valor DTCG tem `$value` e `$type`.
*   **Interface:**
    *   `tokens.py <page.html> --out <design-tokens.json> --source <enum> [--preset-base <id>] [--brand-out <brand-tokens.json>]`;
    *   `tokens.py --from-dtcg <saída do export_dtcg> --brand-out <brand-tokens.json>`;
    *   `tokens.py --diff <a.json> <b.json>`;
    *   `tokens.py --diff-live <computed.json> <design-tokens.json>`.
*   **Comportamento:**
    *   **Página:** lê as variáveis da tabela no `:root` e as famílias do
        `<style data-aura-fonts>`. O `role` vem de `--font-heading` e
        `--font-body`. O `provision` vem do próprio bloco (`@font-face` local
        ou link externo).
    *   **`design-tokens.json`:** escreve no schema atual
        (`design-tokens.md:9-37`) os blocos `colors`, `type` (com
        `families[]{name, role, provision, weights, files_dir}` obrigatório),
        `spacing`, `radius` e `shadow`, mais `source` (enum do item 19) e
        `preset_base` (o id do preset do `palette_engine`, quando houver).
        Se o arquivo já existir, preserva `produto`, `variant_chosen` e
        `components_by_section`, que o modelo escreve no rascunho da ETAPA 2
        (item 26).
    *   **Cores soltas:** conta `#rgb`, `#rrggbb`, `#rrggbbaa`, `rgb()` e
        `rgba()` no CSS e em `fill` ou `stroke` de SVG inline, fora das
        declarações `--*` e fora do bloco de fontes. Acima de 5, exit 1. A
        regex vem do `CSS_COLOR_RE` (`liquid-converter.py:246`), que passa
        para `_css_utils.py` e ganha os formatos de 8 dígitos e `rgb()`.
    *   **`--brand-out`:** recusa com exit 4 se o destino existir com
        `$extensions.aura.source` diferente de `none`. A proteção contra
        sobrescrever a marca fica no código, não só na skill.
    *   **`--from-dtcg`:** liga os tokens do dembrandt aos 8 papéis pelo nome
        (`background`, `surface`, `text` ou `foreground`, `primary`, `accent`,
        `muted`, `border`). O papel que faltar é derivado pelo
        `palette_engine.py`: `on_primary` pelo melhor contraste sobre o
        `primary`, `surface` e `border` a partir do `background`.
    *   **`--diff`:** compara os 8 papéis (hex em minúsculas, igualdade
        exata) e as famílias (nome, sem diferenciar caixa). Aceita o
        `design-tokens.json` e o `brand-tokens.json`. Escreve no stdout
        `{drift, changed:[{key, a, b}]}`, em que `drift` é o percentual de
        chaves diferentes, de 0 a 100. Sai sempre com 0: quem decide é o
        consumidor.
    *   **`--diff-live`:** o mesmo, com a saída do
        `verify_page.py --dump-computed` de um lado. Por seção, compara as
        cores computadas com os papéis e as famílias com as do tokens.
*   **Por quê:** causa 4. O `design-tokens.md:7` pede tokens por script, e o
    script nunca existiu. É o único motor de drift da Aura.

#### 6. `tools/page-qa/README.md` e `.claude/lib/theme-verify/README.md` (criar o primeiro, modificar o segundo)

*   **Mudança:**
    *   O README de `tools/page-qa/` traz uma linha por script, com interface,
        saída e a etapa que o chama.
    *   O README do theme-verify documenta os dois perfis e as flags novas.
*   **Por quê:** é o padrão das pastas de `tools/` e `.claude/lib/`.

#### 7. `tools/tests/test_verify_page_json.py` (criar)

*   **Como roda:** o `verify_page.py` não pode ser importado, porque o
    `_bootstrap()` troca o processo no import. O teste chama o script por
    `subprocess` e pula (`skipTest`) quando o exit code é 3 (Playwright
    ausente). É o primeiro teste da pasta que depende do Playwright.
*   **Fixtures** em `tools/tests/fixtures/page-qa/`:
    *   `clean.html`: passa limpa;
    *   `dirty.html`, com estes defeitos:
        *   scroll horizontal;
        *   texto #999 sobre #fff;
        *   9 tamanhos de fonte;
        *   um `<script>`;
        *   uma seção sem marcador;
        *   headline de 3 linhas em 390;
        *   HTML+CSS acima de 150 KB.
*   **Casos:**
    *   `clean` não tem `fail`;
    *   cada defeito aparece com o `id` e o `blocking` certos;
    *   rodar duas vezes gera o mesmo JSON;
    *   sem `--json-out`, a saída em texto e o exit code são os de hoje;
    *   `--legal` com `pass: false` vira `legal_check` em `fail`.

#### 8. `tools/tests/test_geodiff.py`, `test_legal_check.py`, `test_tokens.py` e `test_downloader_bands.py` (criar)

*   **Geodiff:** duas capturas sintéticas de `bands`, uma igual e uma com a
    grade trocada de 3 para 1 coluna. A primeira dá 100, a segunda fica
    abaixo de 70. Um caso com dois `--ref` (quebra-cabeça).
*   **Legal:** uma captura sintética com um texto e um `src`, e três páginas:
    *   uma reutiliza os dois e falha;
    *   uma só tem frases da allowlist e passa;
    *   uma não reutiliza nada e passa.
*   **Tokens:**
    *   um `:root` completo vira um `design-tokens.json` com os 8 papéis;
    *   6 cores soltas fazem o script falhar;
    *   `--diff` de dois arquivos iguais dá 0;
    *   `--brand-out` sobre uma marca com `source: "dembrandt"` sai com 4;
    *   `--from-dtcg` sem `on_primary` deriva um valor com contraste 4,5 ou
        mais sobre o `primary`.
*   **Downloader:** `robots.txt` que proíbe é recusado e `robots.txt`
    ausente (404) é permitido, com `requests.get` simulado (o `validate_url`
    recusa servidor local); `file://` fora de `workspace/` é recusado; a divisão de faixas
    num HTML de fixture (este caso pula sem Playwright).

#### 9. Schemas (criar)

Em `.claude/templates/schemas/`:
*   `page-design.page-plan.schema.json`
*   `brand.brand-tokens.schema.json`

**Conteúdo:**
*   **`page-plan`:**
    *   **Obrigatórios** (os que os consumidores leem): `page_type`, no topo e
        em `strategy`; `strategy.mechanism_name`; `section_order`;
        `sections_plan[].media`; `commerce`.
    *   **Novos:** `schema_version`, `build_mode`, `direction_ref`,
        `reference_capture_ref`, `qa_metrics_ref`, `review_ref`,
        `preview_url` e `qa_overrides[]{item, motivo, data}`, com `item`
        restrito a `horizontal_overflow`, `broken_images` e `html_css_kb`.
    *   **`design_route`:** aceita os valores antigos e os novos (`direction`,
        `reference`).
*   **`brand-tokens`:** `oneOf` com duas formas.
    *   **Vazia:** só `$schema` e `$extensions.aura.source: "none"`.
    *   **Completa:** os 8 papéis de `color` e as duas famílias de
        `typography`, no contrato do item 5, com o `source` em
        `$extensions.aura.source` (no topo, ferramentas DTCG o leriam como
        grupo de token).

**Quem valida:** os 13 schemas de hoje seguem o padrão `<id>.dados.schema.json`
e são validados pelo `manifest.py` (linhas 236 a 247). Estes dois não são
`dados.json`, então não entram nesse padrão.
*   O `qa_gate.py` (item 9a) valida o `page-plan.json` de página v2. Página
    antiga não é validada.
*   A ETAPA 6 do page-design e o setup validam o `brand-tokens.json` depois
    de gravar.
*   Os dois usam `tools/schema_validate.py`. O §8 do `OVERVIEW.md` (linhas 363
    e 364) ganha essa exceção (item 46).

**Por quê:** hoje esses arquivos não têm schema.

#### 9a. `tools/page-qa/qa_gate.py` e `tools/tests/test_qa_gate.py` (criar)

*   **Interface:** `qa_gate.py <page-plan.json> [<qa-metrics.json>] [--page <page.html>]`.
*   **Comportamento:**
    *   **Página antiga:** exit 2, com o aviso "página sem QA medido".
    *   **Página v2:**
        *   sem `qa-metrics.json`: exit 1;
        *   `page_sha256` diferente do hash do `--page`: exit 1, com "rode o
            QA de novo";
        *   `page-plan.json` inválido no schema do item 9: exit 1;
        *   cada item bloqueante em `fail` sem entrada em `qa_overrides`:
            exit 1;
        *   entrada em `qa_overrides` para `script_tags`, `section_markers`,
            `section_ids_match_plan` ou `legal_check`: ignorada, com aviso;
        *   nada disso: exit 0.
    *   Imprime uma linha por item reprovado e, para os liberáveis, o
        formato da entrada em `qa_overrides`.
*   **Teste:** liberar `horizontal_overflow` desbloqueia; liberar
    `script_tags` não; página antiga dá 2; página v2 sem métricas dá 1; hash
    diferente dá 1.
*   **Por quê:** o pré-flight do page-build hoje é prosa
    (`page-build/SKILL.md:14-23` e `reference/contexto.md`). Sem script, a
    regra de liberação não tem quem a aplique nem teste.

#### 9b. `.claude/lib/design-presets/palette_engine.py` e `tools/tests/test_palette_engine.py` (modificar)

*   **Mudança:** o `--signals` (linhas 681 a 685) ganha um ramo DTCG. Se o
    arquivo tiver `color.<papel>.$value`, lê os 8 papéis daí. Se não, lê
    `palette` como hoje. A docstring (linhas 36 e 44) cita os dois formatos.
*   **Teste:** um `brand-tokens.json` de fixture gera as mesmas 3 paletas que
    o `design-signals.json` equivalente.
*   **Por quê:** página v2 não grava mais o `design-signals.json`.

### Fase 2: arquivo de marca compartilhado (setup)

#### 10. `.claude/skills/setup/reference/onboarding-e-extracao.md` (modificar)

*   **Mudança:** a ETAPA 4, linhas 65 a 68, passa a ter o dembrandt como
    primeiro degrau:
    *   `check_robots` do dembrandt (é a URL da própria marca do membro);
    *   `get_design_tokens` na URL da loja ou do site;
    *   `export_dtcg`, convertido para o contrato do item 5 com
        `tokens.py --from-dtcg ... --brand-out brand/brand-tokens.json`;
    *   validação do arquivo no schema do item 9.

    O fetch atual por WebFetch ou Playwright vira reserva. Sem loja nem site, o
    arquivo nasce na forma vazia do schema (`$extensions.aura.source: "none"`).
*   **Quando o setup não tem produto:** na SITUAÇÃO A, o setup não cria o
    `brand.md` (`profile-e-brand.md:67`) e ainda não há slug. Nesse caso o
    `brand-tokens.json` não nasce no setup. A ETAPA 2 do page-design cria o
    arquivo na forma vazia quando ele não existe (item 19).
*   **Por quê:** Goal 2. A marca entra no começo da Aura.

#### 11. `.claude/skills/setup/reference/profile-e-brand.md` e `.claude/templates/brand.md.template` (modificar)

*   **Mudança:** as seções 3 (paleta) e 4 (tipografia) do `brand.md` passam a
    citar os papéis e os valores do `brand-tokens.json`, com um ponteiro para o
    arquivo, em vez de hex escritos à mão.
*   **Por quê:** acaba com a segunda fonte de verdade da identidade.

#### 12. `.claude/skills/setup/reference/dependencias.md` (modificar)

*   **Mudança:**
    *   **Sai** só a linha 44 (`single-file-cli`).
    *   **Ficam** as linhas 45 a 51 (Playwright no venv do `web-fetch`, que o
        `verify_page.py` usa) e o venv do design-clone (linha 52), que o
        `downloader.py` e o `liquid-converter.py` continuam usando.
    *   **Reescritas sem a rota 2:** a linha 43 (Python para o QA e a captura
        da `page-design`), a linha 52 (lista só `downloader` e
        `liquid-converter`) e a linha 58 (sem SingleFile nem `aura_clone.py`).
    *   **Acrescenta:**
        *   Node 22.13+ (o `awwwards-mcp` exige isso no `engines`);
        *   a primeira execução de `npx -y awwwards-mcp@1.14.0`;
        *   as skills do Awwwards, que vêm dentro do pacote:
            `npm install --prefix ~/.cache/aura/awwwards awwwards-mcp@1.14.0`
            e cópia de `node_modules/awwwards-mcp/skills/{awwwards-inspiration,awwwards-motion-study,awwwards-setup,awwwards-doctor}`
            para `~/.claude/skills/`;
        *   a skill da Vercel:
            `npx skills add vercel-labs/agent-skills --skill deploy-to-vercel`;
        *   `awwwards-setup` (cria `~/.awwwards-mcp/preferences.json`);
        *   o índice local opcional (`awwwards-index`);
        *   **opcionais**, só para quem quiser (Open Question, padrão (b)): o
            21st.dev (o MCP `https://21st.dev/api/mcp`, com a chave
            `TWENTYFIRST_API_KEY` no `.env`) e o brag
            (`claude plugin install brag@brag`, marketplace
            `latent-spaces/brag`).
    *   O preview da Vercel roda sem conta e não pede token.
    *   Sem uma das skills de terceiros, a etapa que a usa roda na reserva, e
        o setup avisa qual.
*   **Por quê:** D1 = A: o membro precisa conseguir subir o que o repo
    declara.

#### 13. `.claude/skills/setup/SKILL.md` (modificar)

*   **Mudança:**
    *   Uma linha nova na lista de saídas: `brand/brand-tokens.json`.
    *   As linhas 3 e 36 deixam de citar single-file e design-clone.
    *   Se o `SKILL.md` passar de 12.288 bytes, sai outra frase de tamanho
        igual ou maior.
*   **Por quê:** o registro e o painel mostram o que cada etapa grava.

### Fase 3: page-design reescrito

#### 14. `.claude/skills/page-design/SKILL.md` (reescrever)

*   **Estrutura:**
    *   Quando usar.
    *   Pré-flight. Sai a exigência de loja conectada.
    *   Contexto. Absorve a parte útil de `contexto.md`.
    *   ETAPA 0, Leitura.
    *   ETAPA 1, Plano.
    *   ETAPA 2, Marca.
    *   ETAPA 3, Referências e direção.
    *   ETAPA 4, Construção: modo direção ou modo referência, e o membro
        escolhe.
    *   ETAPA 5, QA.
    *   ETAPA 6, Preview, aprovação, tokens e salvar (`page-plan.json` com
        `schema_version: 2`, manifest e índice).
    *   Mensagem final.

    Cada etapa tem um parágrafo de no máximo 3 linhas e aponta para um
    `reference/*.md`.
*   **Restrições:**
    *   no máximo 12.288 bytes;
    *   `<!-- gen:title -->` intacto;
    *   a `description` do frontmatter cita os dois modos em vez de "três
        rotas";
    *   o pré-flight confere se as skills de terceiros existem
        (`awwwards-inspiration`, `awwwards-motion-study`, `deploy-to-vercel`)
        e avisa qual etapa vai rodar na reserva.
*   **Por quê:** é a reescrita do roteiro.

#### 15. `.claude/skills/page-design/reference/leitura-e-base.md` (modificar)

*   **Mudança:**
    *   Recebe a regra de busca na base que hoje mora em `contexto.md`.
    *   Às 9 buscas de CRO soma 3 de design visual:
        *   hierarquia;
        *   escala tipográfica;
        *   narrativa de landing.

        Os termos das 3 buscas vêm de três skills de conhecimento do
        dembrandt: `visual-emphasis-and-hierarchy`, `modular-scale-typography`
        e `layout-paradigms-and-consistency`.
*   **Por quê:** causa 3. A base hoje só traz conversão.

#### 16. `.claude/skills/page-design/reference/page-type.md` (modificar)

*   **Mudança:**
    *   Nas linhas 57 a 69, tira só o que é de uma marca específica: URLs,
        frases ("Skip to Special Offer", "Claim Deal"), personagem ilustrado
        e estética.
    *   **Ficam, sem mudança:**
        *   o mapa das 7 seções canônicas da copy-engine para os
            `sections_plan[].id` (`hero`, `lead`, `background-story`…
            `reveal-close`);
        *   o botão único de compra com âncora `#offer`;
        *   a parada quando falta seção na copy.
    *   A estética do advertorial e do listicle passa a vir da direção (item
        18).
*   **Por quê:** causa 2, sem quebrar o contrato com a copy-engine e o
    page-build.

#### 17. `.claude/skills/page-design/reference/sections-e-hero.md` e `eyebrows.md` (modificar)

*   **Mudança:**
    *   Nos `page_type` que não são advertorial nem listicle, as seções nascem
        da narrativa do produto: problema, mecanismo, prova, oferta,
        objeções. O menu atual vira lista de exemplos, não de opções
        fechadas.
    *   Os blocos universais deixam de ser obrigatórios.
    *   O eyebrow passa a ser opcional, decidido pela direção.
    *   O `eyebrows.md` mantém só as regras de qualidade para quando houver
        eyebrow.
*   **Por quê:** causa 2.

#### 18. `.claude/skills/page-design/reference/board-de-referencias.md` (reescrever, com o nome `referencias-e-direcao.md`)

*   **Mudança:**
    *   Caminho 1:
        *   `awwwards.search_sites` com award `ecommerce` e as tags do
            produto;
        *   `search_elements` para seções específicas;
        *   o membro marca as 3 referências que mais quer seguir.
    *   Reserva, em ordem: Refero (cada referência gravada com
        `source: "refero"`) e WebSearch de concorrentes e da categoria. O
        21st.dev depende da Open Question.
    *   **Imagem das 3 marcadas**, em qualquer caminho:
        `verify_page.py <url> --desktop-only --shots-dir page/references/<n>/`
        (perfil loja). O `desktop-full.png` é a imagem que vai para o
        revisor.
    *   **Campos de `reference_board.references[]`:** `url`, `title`,
        `source` (`awwwards | refero | websearch`), `marked` (booleano) e
        `image_path`. Ficam também os campos que a social-engine já lê.
    *   **Direções:** o `draw.mjs` do taste-skill
        (`skills/taste-skill/scripts/draw.mjs` no cache do plugin) roda com
        `node draw.mjs --sector <ecommerce|physical-product|fashion> --brief "<uma linha do produto>" --options 3`,
        mais `--keep palette,type` quando o `brand-tokens.json` não está
        vazio. O membro escolhe 1, e `--direction <id> --out page/` gera a
        folha completa.
    *   **Formato fixo do `page/direction.md`**, com estes cabeçalhos:
        *   `## Tipografia`, com uma linha `- família: <nome> (<heading|body>)`
            por fonte, lida pelo `legal_check.py`;
        *   `## Paleta`, com os 8 papéis;
        *   `## Hero`;
        *   `## Blueprint por seção`, com um subtítulo por id do
            `sections_plan`;
        *   `## Proibido nesta página`.
    *   Sem o taste-skill, o modelo escreve as 3 direções a partir do board,
        no mesmo formato.
*   **Por quê:** causa 3 e Goal 3. O nome novo deixa claro que este
    arquivo agora inclui a direção.

#### 19. `.claude/skills/page-design/reference/brand-signals.md` (reescrever)

*   **Mudança:**
    *   Cascata nova:
        1.  `brand-tokens.json` do setup, se não estiver vazio;
        2.  dembrandt numa URL da própria marca do membro. URL de terceiro
            nunca vira marca;
        3.  `palette_engine.py` com a página comparadora, que é mantida;
        4.  manual: o membro informa as cores ou manda um print, lido por
            visão.
    *   No `mcp-detect/README.md`, saem a linha `source` `design_clone` e o
        design-clone da cascata do Refero.
    *   Saem o Caminho 2 como etapa própria e o Caminho 3 (`aura_clone.py`
        signals).
    *   Se o `brand-tokens.json` não existir, a ETAPA 2 cria na forma vazia.
    *   Em página v2 a ETAPA 2 não grava mais o `design-signals.json`. Ela lê
        o `brand-tokens.json` e, se ele estiver vazio, a escolha na
        comparadora preenche a marca na ETAPA 6 (`tokens.py --brand-out`).
    *   O `source` do `design-tokens.json` aceita
        `dembrandt | brand_tokens | palette_engine | refero | manual`. O enum
        antigo (`refero | screenshot_vision | design_clone | manual`,
        `brand-signals.md:15`) continua válido só em página antiga.
    *   O preset escolhido na comparadora vai para
        `design-tokens.json.preset_base` (o `palette_engine` já devolve o
        preset de cada candidata, linhas 23 a 25).
    *   O `--signals` com `brand-tokens.json` vem do item 9b.
*   **Por quê:** causa 4 e corte do design-clone de sinais.

#### 20. `.claude/skills/page-design/reference/tipografia.md` (modificar)

*   **Mudança:**
    *   Tira o padrão ABC Oracle/Geist e a regra de "uma família por padrão".
    *   A tipografia vem da direção ou do `brand-tokens.json`.
    *   Ficam as regras de provisionamento local (`local_fonts.py`) e de
        licença, com o modo das fontes unificado em `--mode relative`.
*   **Por quê:** causa 2, e o arquivo hoje manda usar modos diferentes do
    `local_fonts.py` em lugares diferentes.

#### 21. `.claude/skills/page-design/reference/modo-direcao.md` (criar, substitui `rota-claude-design.md`)

*   **Conteúdo:**
    *   Construir o `page.html` a partir de `direction.md` e do
        `brand-tokens.json`, com todas as cores e tamanhos em variáveis CSS no
        `:root`, nos nomes do contrato do item 5.
    *   O canvas do Claude Design pela tool `Artifact` continua como superfície
        de trabalho: o modo direção absorve a rota 1.
    *   Regras do taste-skill no "perfil Aura":
        *   sem `stage.js`;
        *   sem o gate `html.js`;
        *   a "live thing" só com `:has()`, `<details>` ou radio;
        *   o `MOTION_MIN` não se aplica.
    *   A contradição de `rota-claude-design.md:24` contra `:38` é resolvida: o
        `page.html` publicado é sempre o do repo, normalizado.
*   **Por quê:** Goal 4.

#### 22. `.claude/skills/page-design/reference/modo-referencia.md` (criar, substitui `rota-singlefile-clone.md` e `rota-section-puzzle.md`)

*   **Conteúdo:**
    *   O membro passa 1 URL (página inteira) ou uma URL por seção
        (quebra-cabeça).
    *   Passo 1, mapa:
        `downloader.py <url> page/reference-capture/<n>/ --mode bands`, uma
        pasta por URL. Ele checa o `robots.txt` antes de capturar.
        *   Exit 2 (robots proíbe), 3 ou 5 (bloqueio do site): a captura não
            roda e a skill oferece o modo direção.
        *   O mapa liga as faixas da referência às seções do `sections_plan`
            no formato do `--map` do `geodiff.py`. Faixas que o plano não pede
            são descartadas. No máximo 10 seções.
    *   Passo 2, por seção:
        *   construir com copy, oferta, imagem e tokens do membro;
        *   capturar o `page.html` com
            `downloader.py file://.../page/design/page.html page/reference-capture/page/ --mode bands`
            e rodar o `geodiff.py --out page/reference-capture/geodiff.json`;
        *   até 2 rodadas; se a nota continuar abaixo de 70, a seção segue e
            a nota entra como `warn` pelo `verify_page.py --geodiff` (o
            revisor julga);
        *   travar a seção.
    *   Passo 3: o teste de vizinhança, vindo de `rota-section-puzzle.md:45-47`,
        e a unificação de tokens.
    *   Passo 4: `legal_check.py --out page/reference-capture/legal.json`. A
        ETAPA 5 passa esse arquivo ao `verify_page.py --legal`, e o item
        `legal_check` bloqueia se houver algo.
    *   A captura fica em `page/reference-capture/`.
    *   A regra legal de `rota-singlefile-clone.md:9` é copiada, trocando os
        "`design-signals` da ETAPA 2" por `brand-tokens.json`.
*   **Por quê:** Goals 4 e 6, D2.

#### 23. `.claude/skills/page-design/reference/movimento-css.md` (criar)

*   **Conteúdo:**
    *   Se houver referência: `awwwards-motion-study` (`get_motion_dna`,
        `analyze_scroll_map`) para fazer o inventário do movimento dela.
    *   A tradução para CSS, com receitas escritas neste próprio arquivo (o
        conteúdo vem do `_jutsu/css-native` do plugin genjutsu e do
        `motion.md` do taste-skill, sem depender dos plugins em runtime):
        *   `animation-timeline: view()` dentro de `@supports`, com o conteúdo
            visível por padrão (o Firefox não suporta);
        *   `@starting-style`;
        *   sticky;
        *   `prefers-reduced-motion`.
    *   O que não cabe em CSS fica de fora e vai listado no `review.md`.
    *   Substitui a contradição do marquee em `shopify-section-patterns`.
*   **Por quê:** Goal 7.

#### 24. `.claude/skills/page-design/reference/regua-de-design.md` (modificar)

*   **Mudança:**
    *   Cada item marca se é `medido` (com o `id` do item no `verify_page.py`)
        ou `julgado` (revisor).
    *   Saem os comandos grep que não medem o critério, como o do T1 (linha
        26), que conta declarações no CSS em vez de tamanhos renderizados. A
        medida passa a ser o `font_sizes_distinct`.
    *   A regra do travessão e o teto de 3 rodadas passam a existir só aqui.
    *   O M6 (linha 100) passa a permitir marquee em CSS puro.
*   **Por quê:** Goal 5 e as duplicações.

#### 25. `.claude/skills/page-design/reference/qualidade-e-checkpoint.md` (reescrever)

*   **Mudança:** a ETAPA 5 e a ETAPA 6 viram:
    *   `verify_page.py file://.../page.html --json-out page/qa-metrics.json --plan page-plan.json --shots-dir page/qa-shots/`,
        mais `--legal` e `--geodiff` no modo referência;
    *   o revisor sem contexto, como descrito no Technical Plan:
        *   chamado pela tool `Agent` com `subagent_type: "general-purpose"`,
            o conteúdo de `reference/revisor.md` (item 25a) como prompt e os
            caminhos das imagens como entrada;
        *   "não há subagente" quando a tool `Agent` não está disponível na
            sessão. Aí vale a rubrica do modelo, como reserva;
    *   até 3 rodadas de correção guiadas pelo `review.md`. Para antes da 3ª
        se não houver item bloqueante em `fail` e nenhuma nota do revisor
        abaixo de 3;
    *   item bloqueante em `fail` depois das 3 rodadas: o membro decide e
        pode registrar a liberação em `page-plan.json.qa_overrides`, só para
        `horizontal_overflow`, `broken_images` e `html_css_kb`;
    *   o preview de layout: `deploy-to-vercel` sem conta, da pasta
        `page/design/` sem as fontes, com aviso de link público. O
        `previewUrl` devolvido pela skill é gravado em
        `page-plan.json.preview_url`. Sem a skill, ficam as capturas;
    *   a aprovação do membro pelas capturas locais com as fontes reais e
        pelo link no celular. A mensagem diz que a aprovação final de
        tipografia é na 6.9 do page-build;
    *   `tokens.py` e a política do arquivo de marca:
        *   grava o `design-tokens.json`;
        *   preenche o `brand-tokens.json` só se ele estiver vazio, e valida
            no schema;
        *   mostra o drift (`tokens.py --diff`) na mensagem final;
        *   se o `tokens.py` falhar depois da aprovação, a página continua
            aprovada, a marca não é tocada, o manifest não marca a etapa como
            concluída e a mensagem diz o erro e o comando para rodar de novo.
*   **Também sai:** a referência ao `webapp-testing`, as linhas 16 e 59 sobre
    a rota 2, a linha 21, com o layout de uma marca, e o D6 (linha 32), que
    repete o bloco S da régua.
*   **Por quê:** Goals 5 e 8.

#### 25a. `.claude/skills/page-design/reference/revisor.md` (criar)

*   **Conteúdo:** o prompt fixo do revisor sem contexto.
    *   **Entradas:** as capturas de 1440 e 390 (`page/qa-shots/`), as imagens
        das 3 referências marcadas (`page/references/<n>/desktop-full.png`) e
        o `direction.md`.
    *   **Critérios:** tipografia, espaço, cor, hierarquia, aderência à
        direção e sinais de "feito por IA", cada um com nota de 1 a 5. As
        definições vêm dos itens julgados da régua.
    *   **Formato de saída** do `page/review.md`: tabela de notas e as 5
        correções de maior impacto, cada uma com seção e mudança concreta.
    *   **Regra:** não recebe a conversa nem o HTML como texto.
*   **Por quê:** Goal 5.

#### 26. `.claude/skills/page-design/reference/design-tokens.md` (modificar)

*   **Mudança:** o arquivo passa a descrever o rascunho de tokens na ETAPA 2 e
    o `tokens.py` na ETAPA 6. Tira a linha 7, sobre "gere programaticamente" e
    a rota 2.
*   **Por quê:** causa 4.

#### 27. `.claude/skills/page-design/reference/page-plan-e-salvar.md` (modificar)

*   **Mudança:**
    *   Campos novos: `schema_version` (sempre `2` em página nova),
        `build_mode` (`direction|reference`), `direction_ref`,
        `reference_capture_ref`, `qa_metrics_ref`, `review_ref`,
        `preview_url` e `qa_overrides`.
    *   O enum de `design_route` (linhas 60 e 61) vira `direction|reference`.
        Os valores antigos continuam válidos na leitura.
    *   O `eyebrow` deixa de ser obrigatório.
    *   Na linha 57, o campo `signals_source` perde só o valor
        `design_clone`; `refero` e `manual` ficam.
    *   A linha 63 (`design_signals_ref`) passa a valer só para página antiga.
    *   Aponta para o schema novo.
*   **Por quê:** contrato do `page-plan.json`.

#### 28. `.claude/skills/page-design/reference/mensagem-final-e-self-audit.md` (modificar)

*   **Mudança:**
    *   O parágrafo de 5 KB da linha 12 vira uma checklist curta. A maior parte
        dos gates passa a ser lida do `qa-metrics.json` e do `legal_check`, em
        vez de repetida em prosa.
    *   O framing da mensagem final cita o link de preview.
*   **Por quê:** duplicação e peso no contexto.

#### 29. `.claude/skills/page-design/reference/normalizacao-html-externo.md` (modificar)

*   **Mudança:** tira a citação à rota 2 (linha 3). Passa a valer para o HTML
    do canvas do Artifact e para o resultado do modo referência.
*   **Por quê:** a rota 2 saiu.

#### 30. `.claude/skills/page-design/reference/brief-codex.md` (conforme a Open Question sobre o Codex)

*   **Padrão até a decisão: manter.** O `SKILL.md` reescrito (item 14)
    inclui a 3.8 dentro da ETAPA 5, e o arquivo só ajusta as citações às
    rotas.
*   **Se cortar:**
    *   o `SKILL.md` reescrito não inclui a 3.8;
    *   apagar o arquivo;
    *   tirar `page/design/brief-codex.md` e `page/design/page-codex.html` dos
        `writes` em `.claude/skills.json`.
*   **Por quê:** depende da Open Question sobre o Codex.

#### 31. Apagar

Em `.claude/skills/page-design/reference/`:
*   `rota-singlefile-clone.md`
*   `rota-section-puzzle.md`
*   `rota-claude-design.md`
*   `menu-de-rotas.md`
*   `contexto.md`
*   `board-de-referencias.md`

**Por quê:** o conteúdo foi substituído pelos itens 18, 21 e 22, ou absorvido
pelos itens 14 e 15.

#### 32. Arquivos sem mudança no page-design

*   `imagens-higgsfield.md` e `quiz-funnel.md` ficam sem mudança, a não ser
    que o grep de rotas antigas encontre citações.
*   `assets-de-imagem.md` ganha uma linha: o `assets.mjs` do taste-skill
    busca imagem de banco com licença comercial, como reserva do Higgsfield
    e degrau antes do placeholder.

### Fase 4: page-build e o conversor

#### 33. `.claude/skills/page-build/SKILL.md`, `reference/contexto.md` e `reference/validate.md` (modificar)

*   **Mudança:** o pré-flight (`SKILL.md:14-23` e a íntegra em `contexto.md`)
    ganha um passo: rodar `tools/page-qa/qa_gate.py page-plan.json page/qa-metrics.json --page page/design/page.html`
    (item 9a).
    *   Exit 0: segue.
    *   Exit 1: para e mostra a saída do script ao membro, com cada item
        reprovado e como liberar os liberáveis.
    *   Exit 2: página antiga. Avisa que a página não tem QA medido e segue.

    A regra de liberação fica no script. A skill só o chama.
*   **`validate.md:25`:** passa a descrever o mapeamento de hex para papéis de
    cor (item 34).
*   **Por quê:** Goal 5, com compatibilidade para os workspaces antigos.

#### 34. `tools/design-clone/liquid-converter.py` e `.claude/skills/page-build/reference/padroes-do-conversor.md` (modificar)

*   **Interface:** flags novas `--design-tokens <path>` e `--theme-dir <path>`,
    e os mesmos campos (`design_tokens`, `theme_dir`) no manifest do
    `--batch` (linhas 1385 a 1394).
*   **Mudança:**
    *   `extract_colors_from_css` (linha 271) recebe o mapa hex → papel lido
        do `--design-tokens`. Cada hex que bate com um papel vira o setting
        `color_<papel>` (`color_primary`, `color_on_primary`...). Os outros
        continuam `color_N`. Sem `--design-tokens`, o comportamento é o de
        hoje.
    *   O rótulo do setting, montado em `build_section_file` (linha 1126, com
        `split('_')[1]`), passa a sair do papel: "Cor primária", "Cor do texto
        sobre a primária"... Para `color_N`, continua "Color N".
    *   **Seção já no tema:** se `--theme-dir/sections/<arquivo>` existe e
        tem settings `color_N`, essa seção mantém os ids antigos, para não
        perder as edições do membro no editor.
    *   **Sai o Modo B** (`--sections-json`, linhas 1472, 1473 e 1534), que
        lê a saída do `analyzer.py` apagado no item 47. Sai também a citação
        da linha 67.
*   **`padroes-do-conversor.md:13`:** documenta o padrão novo de cor.
*   **Teste** em `tools/tests/test_liquid_converter_roles.py`: um hex que
    bate com um papel vira `color_primary`; um que não bate continua
    `color_N`; uma seção que já existe em `--theme-dir/sections/` mantém o
    `color_N`.
*   **Por quê:** causa 4. O membro passa a ver "Cor primária" no editor da
    Shopify em vez de "Cor 7".

#### 35. `.claude/skills/page-build/reference/deploy.md` e `reference/specialists-e-referencias.md` (modificar)

*   **Mudança:**
    *   A 6.8 (linha 130) continua chamando o `verify_page.py` sem
        `--json-out`, no perfil loja. Nada muda nela.
    *   A 6.11 (linhas 164 a 173) soma o drift da página no ar:
        `verify_page.py <url> --dump-computed page/live-computed.json` e
        `tokens.py --diff-live page/live-computed.json page/design-tokens.json`.
        O resultado vai para
        `deploy-report.json.fidelity_check.token_drift`. É informativo: não
        bloqueia o deploy.
    *   A linha 72, que lia o `source_detail` como texto livre para achar o
        preset, passa a ler `design-tokens.json.preset_base` em página v2. Em
        página antiga, continua como hoje.
    *   A linha 168 de `deploy.md` e as linhas 3 e 10 de
        `specialists-e-referencias.md` deixam de citar `webapp-testing`.
*   **Por quê:** a checagem vira número, e um campo enumerado substitui o
    texto livre.

### Fase 5: as outras etapas

O item 37 (bug do caminho na social-engine) entra em qualquer caso. Os itens
38 a 43 dependem da Open Question sobre a entrega:
*   **(a), o padrão:** começam depois das Fases 0 a 4 validadas;
*   **(b):** saem deste plano e vão para um segundo doc.

#### 37. `.claude/skills/social-engine/SKILL.md` e `.claude/skills.json` (modificar)

*   **Mudança:**
    *   O caminho `page/design/design-tokens.json` (`SKILL.md:27` e
        `skills.json:1011`) passa a ser `brand/brand-tokens.json`. Se esse
        arquivo não existir, lê `page/design-tokens.json`.
    *   No `skills.json`, também:
        *   `reads` do page-design ganha `brand/brand-tokens.json`;
        *   `writes` do page-design ganha `page/direction.md`,
            `page/qa-metrics.json`, `page/review.md`, `page/references/`,
            `page/reference-capture/` e `brand/brand-tokens.json`, e perde
            `page/design-signals.json` (linha 556);
        *   `writes` do setup ganha `brand/brand-tokens.json`;
        *   `reads` da creative-engine, retention-engine, promo-engine,
            consistency-audit e checkout-aov ganham `brand/brand-tokens.json`,
            se a Fase 5 inteira entrar.
*   **Por quê:** corrige o bug e registra os artefatos novos.

#### 38. `.claude/skills/social-engine/reference/templates-marketing-studio.md` (modificar)

*   **Mudança:**
    *   As linhas 10 (`ads_studio_create_brand`) e 40 (prompts sem Higgsfield)
        e a posição 9 do grid leem os hex do `brand-tokens.json`.
    *   Se o brag ficar (Open Question): reel opcional de lançamento com
        `brag-slim --format vertical --tone polished`, a partir de
        `manifest.storefront.page_url`, fora da rotina agendada e passando
        pelo `strip-metadata.sh`. É um post único, não um formato de
        anúncio. Por isso não conflita com o Non-Goal de criativo. No padrão
        (b), o reel só aparece para quem instalou o brag.
*   **Por quê:** o post usa as mesmas cores da página.

#### 39. `.claude/skills/creative-engine/reference/briefing.md` (modificar)

*   **Mudança:** o "Senso Estético" (linha 56) e os prompts de static e overlay
    leem a paleta e as fontes do `brand-tokens.json`.
*   **Por quê:** o anúncio usa a mesma identidade da página.

#### 40. `.claude/skills/retention-engine/reference/salvar-e-regras.md` (modificar)

*   **Mudança:**
    *   O HTML dos emails usa a paleta e as fontes do `brand-tokens.json`, cada
        família com fallback web-safe.
    *   O contraste do botão é checado por `contrast_ratio` do
        `palette_engine.py`.
*   **Por quê:** os emails hoje não leem identidade nenhuma.

#### 41. `.claude/skills/promo-engine/reference/criativos-da-janela.md` (modificar)

*   **Mudança:** o brief do banner (linhas 13 e 14) lê a paleta.
*   **Por quê:** o banner usa a paleta da marca.

#### 42. `.claude/skills/consistency-audit/reference/checks-medium.md` e `load-artefatos.md` (modificar)

*   **Mudança:** o check M6 da consistency-audit (linhas 35 a 37; não é o M6
    da régua de design) usa `tokens.py --diff` entre o `design-tokens.json` e
    o `brand-tokens.json`, mais `contrast_ratio` do `palette_engine.py` para
    o CTA contra o fundo. A severidade continua a da régua da
    consistency-audit; o script só dá o número.
*   **Por quê:** o check vira número.

#### 43. `.claude/skills/checkout-aov/reference/carrinho-e-drawer.md` (modificar)

*   **Mudança:** o teste 1 (linha 54) roda
    `verify_page.py <url>/cart --dump-computed` e
    `tokens.py --diff-live` contra o `design-tokens.json`.
*   **Por quê:** detecta quando o `/cart` renderiza com a fonte de fallback
    em vez da fonte da marca.

### Fase 6: documentação, limpeza de citações e remoção

A ordem dentro da fase importa: primeiro as citações saem (itens 44 a 46),
depois os scripts são apagados (item 47), e por fim os relatórios (item 48).
Assim o grep do item 47 volta vazio e a regra `paths` do `aura-check.py` não
reprova caminhos que deixaram de existir.

#### 44. Citações aos scripts que saem (modificar)

*   `tools/design-clone/_venv_bootstrap.py:16-17`;
*   `tools/design-clone/_css_utils.py:6` (`preview.py`);
*   `README.md:57`, que está fora do bloco `gen:readme-table` (linhas 9 a 40)
    e por isso não é corrigido pela regeneração;
*   `.claude/lib/workspace-index/workspace-layout.md:34,65`: o layout ganha
    `brand/brand-tokens.json`, `page/direction.md`, `page/qa-metrics.json`,
    `page/review.md`, `page/references/` e `page/reference-capture/`, e o
    `design-signals.json` fica marcado como "só página antiga";
*   `.claude/lib/design-presets/README.md:29,61,78,127`: as citações ao
    `design-signals.json` ganham o `brand-tokens.json`.

#### 45. `.claude/lib/refero-integration/README.md` (reescrever as seções)

*   **Mudança:** as seções que citam design-clone (linhas 9, 47, 54, 69, 83 e
    103), rota (7, 52, 91, 93, 95 e 103) e `design-signals` (7, 26, 52, 67 e
    99) são reescritas. O Refero passa a ser a primeira reserva de
    referência na ETAPA 3.
*   **Por quê:** o README cita a rota 2 e o design-clone, que saem.

#### 46. `.claude/OVERVIEW.md` (modificar) e `.claude/OVERVIEW.html`, `README.md`, `.claude/CLAUDE.md` (regerar)

*   **Mudança:**
    *   A seção do page-design (linhas 173, 565 e 567) descreve os dois modos
        e o `brand-tokens.json`.
    *   Linha 299: o `shopify-section-patterns` deixa de dizer "clone fiel".
    *   Linhas 363 e 364 (§8, schemas): registram os dois schemas novos e
        quem os valida (item 9).
    *   Linha 390: o `design-signals.json` fica marcado como "só página
        antiga".
    *   Linha 545: o Refero sai da "ETAPA 2 (Brand Signals)" e vai para a
        ETAPA 3.
    *   O changelog ganha uma entrada.
    *   Os blocos `gen:` são regerados com `tools/gen_docs.py`.
*   **Por quê:** o `OVERVIEW.md` descreve as rotas que saem, e a regra `gen`
    do `aura-check.py` falha com blocos `gen:` desatualizados.

#### 47. Apagar em `tools/design-clone/` (depois dos itens 44 a 46)

*   `snapshot.py`
*   `analyzer.py`
*   `pattern-extractor.py`
*   `preview.py`
*   `aura_clone.py`
*   os scripts descartáveis: `_render_local.py`, `_render2.py`,
    `_render_preview.py`, `_probe.py`, `_study.py`, `_colors.py`,
    `_map_assets.py`, `_gen_template.py` e `_gen_template2.py`. Eles estão no
    `.gitignore` (linhas 41 a 44), então a remoção é só local e não entra no
    commit.

O README da pasta é reescrito para descrever só o que fica:
*   `downloader.py`, com o modo `bands` (item 2);
*   `liquid-converter.py`;
*   `_css_utils.py`;
*   `_venv_bootstrap.py`;
*   o venv compartilhado.

**Pré-condição:** um grep por cada nome no repo inteiro volta vazio, fora do
changelog do `OVERVIEW.md` e deste doc.

**`requirements.txt`:** sai o `chardet`, que só o `pattern-extractor.py`
usava (linhas 39 a 64). Ficam o `bs4` (`liquid-converter.py:62`), o `requests`
(`downloader.py:82`) e o `lxml`, que é a reserva do `web-fetch`.

**Por quê:** a rota 2 e os sinais por design-clone saíram; os scripts
descartáveis têm caminhos fixos em `/tmp` e ninguém os usa.

#### 48. Relatórios de revisão (apagar)

*   **Mudança:** os relatórios da raiz do repo (`zoom_out_report.md`,
    `comprehension_report.md`, `critic_report.md`,
    `goldfish_review_report.md`, `intermediate_zoom_out_report.md` e
    `implementation_readiness_report.md`) são apagados antes do grep da
    verificação, porque contêm os termos procurados.
*   **Por quê:** o doc é a referência da implementação.

### Verification Plan

*   **Testes:**
    `uv run --no-project python -m unittest discover -s tools/tests` passa,
    incluindo os testes novos. Os que dependem de Playwright pulam com aviso
    quando o venv não tem o Playwright.
*   **Lint:**
    *   `uv run --no-project python tools/aura-check.py` sem erro;
    *   `uv run --no-project python tools/gen_docs.py --check` sem diferença;
    *   `wc -c .claude/skills/*/SKILL.md` com tudo abaixo de 12.288.
*   **Referências órfãs:** um grep no repo pelos nomes abaixo volta vazio.
    As exceções são o changelog do `OVERVIEW.md`, este doc e o valor legado
    `singlefile-clone` do enum de `design_route` (schema do item 9 e
    `page-plan-e-salvar.md:60`).
    *   `singlefile` e `SingleFile`;
    *   `rota-singlefile`, `section-puzzle`, `rota-claude-design` e
        `menu-de-rotas`;
    *   `aura_clone`, `snapshot.py`, `analyzer.py`, `pattern-extractor` e
        `_gen_template`;
    *   `webapp-testing`;
    *   `page/design/design-tokens.json`.
*   **Medição contra páginas reais:** rodar `verify_page.py --json-out` em
    três páginas dos workspaces locais: a que tem 51 tamanhos de fonte e as
    duas que têm `<script>` (um listicle e uma página de oferta).
    *   Ele precisa acusar esses defeitos com o `blocking` certo.
    *   O doc as descreve só assim, sem o caminho real, porque o caminho leva
        o slug do produto (regra 11 e regra `member-data` do
        `aura-check.py`).
*   **Critério de aceite (Goal 10):** refazer 3 páginas reais com o fluxo novo
    e conferir:
    *   **modo direção:** `direction.md`, `qa-metrics.json` sem item
        bloqueante em `fail`, `review.md`, `preview_url` e
        `design-tokens.json` gerado por script;
    *   **modo referência:** em pelo menos uma das 3, com uma URL premiada,
        `geodiff` de 70 ou mais em cada seção e um `legal_check` que passa;
    *   **comparação cega:** o dono prefere a versão nova em pelo menos 2 das
        3, lado a lado, sem saber qual é qual.

    Depois, `page-build` em modo validação, sem deploy, para confirmar que o
    `qa_gate.py` libera e que o conversor lê os papéis de cor.
*   **Custo:** registrar tokens e minutos de cada uma das 3 páginas, por modo,
    e escrever os números em Riscos e mitigações.
*   **Compatibilidade:**
    *   **página antiga:** num workspace com `design_route: singlefile-clone`
        e sem `schema_version`, o `qa_gate.py` sai com 2 e o page-build avisa,
        sem bloquear;
    *   **página v2 sem QA:** uma página v2 sem `qa-metrics.json` é
        bloqueada;
    *   **smoke test da loja:** a 6.8 do page-build continua passando num tema
        com `<script>`;
    *   **tema já publicado:** recompilar com `--theme-dir` uma seção que já
        está no tema mantém os ids `color_N`.
*   **Perguntas abertas que a implementação resolve medindo:**
    *   o custo de contexto dos MCPs do `.mcp.json` numa sessão que não é de
        design, medido pelo uso de tokens no início da sessão com e sem os
        servidores.

*Drafted with EGM*
