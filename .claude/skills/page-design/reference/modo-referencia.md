# Page Design · Referência: Modo referência (ETAPA 4)

> Construir a página seguindo a geometria de uma página que o membro admira (uma URL inteira, ou uma URL por seção), com o conteúdo 100% dele: o mapa de faixas pelo `downloader.py --mode bands`, a construção seção por seção travada pelo `geodiff.py`, o teste de vizinhança, a unificação de tokens e o `legal_check.py`. Abra na ETAPA 4 quando o membro escolhe o modo referência.

> **REGRA LEGAL E ÉTICA (inegociável):** da referência sai só geometria (ordem, colunas, proporção, posição dos blocos, ritmo). **NÃO** reaproveite copy, imagens, logos, nome de marca, fontes ou claims dela. A copy vem SEMPRE de `copy-engine/dados.json`, a oferta de `offer-builder/dados.json`, a paleta e a tipografia do `brand-tokens.json` e do `direction.md`, as imagens do mapa de mídia da 1.6. O `legal_check.py` do passo 4 confere isso e bloqueia.

## Entrada

O membro passa **1 URL** (a página inteira vira o mapa) ou **uma URL por seção** (quebra-cabeça: cada seção do plano segue a faixa de uma página diferente). No máximo 10 seções seguem referência; o resto do plano é construído pela direção (`reference/modo-direcao.md`). O `direction.md` da ETAPA 3 continua valendo para tipografia, paleta e o proibido.

## Passo 1 · Mapa

Uma captura por URL, numerada a partir de 0 na ordem em que o membro passou:

```bash
python3 tools/design-clone/downloader.py "<url>" workspace/[produto]/page/reference-capture/<n>/ --mode bands
```

O downloader checa o `robots.txt` antes e grava, por largura (1440 e 390), `bands.json`, `section-NN.json`, `texts.json` e `assets.json`.

- **Exit 2** (robots proíbe), **3** (HTTP de erro) ou **5** (Cloudflare ou desafio): a captura não roda. Diga o motivo em uma linha e ofereça o modo direção, ou outra URL.
- Leia o `bands.json` de 1440 e a imagem da referência marcada, se houver, e ligue cada seção do `sections_plan` a uma faixa: `<n da captura>:<index da faixa>:<id da seção>`. Faixas que o plano não pede são descartadas; a ordem e os ids são sempre os do plano. Mostre o mapa ao membro em uma tabela curta antes de construir.

Grave o mapa em `page-plan.json` → `reference_capture_ref: "reference-capture/"` e o texto do `--map` em `design_route_ref`.

## Passo 2 · Por seção: construir, medir, travar

Para cada seção, na ordem do `section_order`:

1. **Construir** a seção no `page/design/page.html` com a copy, a oferta, a imagem e os tokens do membro, seguindo a geometria da faixa: número de colunas, proporção, posição de texto, mídia e CTA, altura relativa. Mesmo contrato do modo direção (`reference/modo-direcao.md`): variáveis no `:root`, zero `<script>`, `data-aura-section` com o id do plano.
2. **Medir**:
   ```bash
   python3 tools/design-clone/downloader.py "file://$PWD/workspace/[produto]/page/design/page.html" workspace/[produto]/page/reference-capture/page/ --mode bands
   python3 tools/page-qa/geodiff.py --ref workspace/[produto]/page/reference-capture/0 [--ref .../1 ...] --page workspace/[produto]/page/reference-capture/page --map "<mapa só com as seções já construídas>" --out workspace/[produto]/page/reference-capture/geodiff.json
   ```
   O `top_diffs` de cada seção diz o que corrigir (altura, colunas, deslocamento dos blocos).
3. **Até 2 rodadas** por seção. Nota abaixo de 70 depois da segunda: a seção segue, e a nota entra como `warn` no QA (`verify_page.py --geodiff`), para o revisor julgar.
4. **Travar** a seção: as próximas rodadas não mexem nela, a não ser pela unificação do passo 3.

## Passo 3 · Vizinhança e unificação

As referências contribuem com estrutura e ritmo; os tokens são da página, nunca de cada referência. Com a página inteira montada:

- **Uma escala tipográfica só** e as famílias do `direction.md`. A hierarquia lida em cada referência é traduzida para essa escala, nunca colada em pixels.
- **Uma grade de espaçamento só**, com o respiro entre seções maior que o respiro dentro delas.
- **A paleta por papel** em toda seção. Cor herdada de referência não entra.
- **Um raio, uma sombra, uma largura de contêiner e um tratamento de botão** em toda a página.
- **Proporção de imagem consistente** por família de seção.

**Teste de vizinhança (anti-colagem):** no screenshot de 1440, compare cada par de seções vizinhas (peso e tamanho do título, botão, espaço antes e depois, contêiner, tratamento de imagem). Se dá pra dizer onde uma referência termina e a outra começa, a unificação não fechou: refaça. A página tem que parecer desenhada por uma pessoa só. Depois da unificação, rode o geodiff de novo para o registro final.

## Passo 4 · Legal

```bash
python3 tools/page-qa/legal_check.py --ref workspace/[produto]/page/reference-capture/0 [--ref .../1 ...] --page workspace/[produto]/page/design/page.html --allowed-fonts workspace/[produto]/page/direction.md --allowed-fonts workspace/[produto]/brand/brand-tokens.json [--ref-brand "<nome da marca da referência>"] --out workspace/[produto]/page/reference-capture/legal.json
```

Exit 1: cada achado traz a regra (texto, asset, fonte, marca), o trecho e onde está. Troque o trecho pelo conteúdo do membro e rode de novo. Frase genérica de DTC que bate por coincidência ("30 day money back guarantee") entra numa linha de `tools/page-qa/legal_allowlist.txt` só se for de fato genérica do mercado, nunca uma frase da marca de referência. A ETAPA 5 passa o `legal.json` ao `verify_page.py --legal`, e o item `legal_check` bloqueia e não aceita liberação.

## Onde fica

`page/reference-capture/` (capturas, `geodiff.json`, `legal.json`), local como todo o `workspace/` e nunca commitado. `page-plan.json`: `build_mode: "reference"`, `design_route: "reference"`, `design_route_ref` com o mapa, `reference_capture_ref`.
