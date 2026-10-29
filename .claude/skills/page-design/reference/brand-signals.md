# Page Design · Referência: Marca (ETAPA 2)

> A cascata da marca até os 8 papéis de cor e as famílias que a página usa: `brand-tokens.json` do setup, dembrandt numa URL da própria marca, o gerador de 3 paletas com a comparadora na página real, ou o membro informando. A política de escrita no arquivo de marca e o resumo ao membro. Abra depois do plano (ETAPA 1).

## O que sai daqui

Só cor, tipografia, raio, sombra e densidade, nunca o layout (o layout vem da direção da ETAPA 3). O resultado são os 8 papéis de cor (background, surface, foreground, primary, on_primary, accent, muted, border) e as famílias heading e body, que a ETAPA 3 escreve no `## Paleta` e no `## Tipografia` do `direction.md` e a ETAPA 4 põe no `:root` da página.

Em página nova (`schema_version: 2`) esta etapa **não grava o `design-signals.json`**. O registro da escolha vai para `page-plan.json` → `brand_discovery` (`source`, `preset_base` quando houver, os 8 papéis e as famílias), e o `design-tokens.json` sai por código na ETAPA 6 (`reference/design-tokens.md`).

Antes de qualquer pergunta, leia `workspace/[produto]/brand.md`: posicionamento, tom e o que já estiver preenchido entram direto. Pergunte em UMA mensagem só o que faltar.

## A cascata

Arquivo de marca: `workspace/[produto]/brand/brand-tokens.json` (schema em `.claude/templates/schemas/brand.brand-tokens.schema.json`). Se ele não existir, crie na forma vazia antes de tudo:

```json
{"$extensions": {"aura": {"source": "none"}}}
```

### 1. `brand-tokens.json` do setup (quando não está vazio)

`$extensions.aura.source` diferente de `none`: os 8 papéis e as famílias vêm daqui, e nada de cor ou fonte é perguntado. A direção da ETAPA 3 roda com `--keep palette,type`. `brand_discovery.source: "brand_tokens"`.

### 2. dembrandt numa URL da própria marca

Marca vazia e o membro tem loja ou site **dele** (`store_url` do manifest, ou um link que ele confirma ser da marca dele). URL de concorrente ou de referência **nunca** vira marca: para isso existe a ETAPA 3.

1. `mcp__plugin_dembrandt_dembrandt__check_robots` na URL; proibido, pule para o caminho 3.
2. `get_design_tokens` na URL **sem** `sync` (a resposta síncrona traz a extração inteira, 60 mil caracteres, e nenhum `job_id`): ele devolve um `job_id`; acompanhe com `get_job_status` (o resultado completo é grande, então só confirme que terminou) e chame `export_dtcg` com o mesmo `job_id`. Salve o export em `workspace/[produto]/brand/dembrandt-dtcg.json`. O `tokens.py` lê o formato DTCG 2025.10 que o dembrandt exporta (`color.semantic.*`, `$value` como objeto) e completa superfície, texto secundário e borda pela paleta extraída.
3. Converta e valide:
   ```bash
   python3 tools/page-qa/tokens.py --from-dtcg workspace/[produto]/brand/dembrandt-dtcg.json --brand-out workspace/[produto]/brand/brand-tokens.json
   python3 tools/schema_validate.py .claude/templates/schemas/brand.brand-tokens.schema.json workspace/[produto]/brand/brand-tokens.json
   ```
   É a mesma extração do setup, feita aqui porque o setup não rodou com loja. `brand_discovery.source: "dembrandt"`.

Sem o dembrandt na sessão, extração vazia ou robots barrando: caminho 3.

### 3. Gerador de 3 paletas (`palette_engine.py`) e a comparadora

O único caminho que não precisa de URL. A Aura gera **3 paletas candidatas para ESTE produto**, com o motivo de cada uma, e o membro escolhe vendo a cor aplicada na página real.

1. Peça a descrição livre da vibe se ele quiser dar uma ("editorial sério, low-pressure") e converta em hex qualquer cor citada por extenso (sage green `#9CAF88`, dusty rose `#D4A5A5`, off-white `#FDFAF4`, navy `#14213D`, terracotta `#C66B3D`, olive `#6B7040`; não reconhecível, peça o hex). Isso vira semente, nunca decisão.
2. Rode o gerador:
   ```bash
   python3 .claude/lib/design-presets/palette_engine.py \
     --vertical <supplements|health|beauty|home|relationship|other> \
     --avatar "<core_avatar_line da market-research>" \
     --skepticism <baixo|médio|alto, o ceticismo da market-research> \
     [--seed "#AABBCC,#112233"] [--signals workspace/[produto]/brand/brand-tokens.json] [--lang en] [--theme dark]
   ```
   `--signals` com o `brand-tokens.json` usa como semente as cores que a marca já tem (DTCG `color.*.$value`). Saem exatamente 3 candidatas: nome, motivo em uma frase, harmonia declarada, a paleta com os 8 papéis e os trios R,G,B, e o preset base de cada uma.
3. O script confere sozinho saturação viva no `primary` e no `accent`, harmonia, contraste WCAG AA (texto e texto secundário contra fundo e superfície, texto do botão contra o botão, 3:1 da cor de apoio) e as 3 distintas entre si. Paleta que não passa é corrigida ou o script sai com erro; com erro, reporte a mensagem e siga pelo caminho 4.
4. **Prove as 3 na comparadora** (abaixo). Nunca peça a escolha por amostra de cor solta.
5. Com a escolha: `brand_discovery.source: "palette_engine"`, `preset_base` com o preset base da candidata (vai para `design-tokens.json.preset_base`; é por ele que a `page-build` acha os pesos de fonte em `presets.json`), a paleta inteira e `radius`, `shadow` e `density` literais do `non_color_tokens` dela.

Os 8 presets de `.claude/lib/design-presets/presets.json` são a base do gerador, não um menu: não ofereça a lista ao membro nem copie cor de lá à mão. Mesma entrada devolve sempre as mesmas 3 candidatas.

### 4. Manual

O membro informa as cores (hex ou nomes convertidos como acima) ou manda um print **da própria marca**, lido por visão (Read no PNG): hex aproximado de fundo, texto, primary, accent e superfícies. Os papéis que faltarem saem do `palette_engine.py` com essas cores como `--seed`, e o contraste passa pelo mesmo script. `brand_discovery.source: "manual"`.

## Tipografia

Marca com família (caminho 1 ou 2): a família é dela. Sem família na marca, a tipografia vem da direção escolhida na ETAPA 3 ou do `non_color_tokens` da candidata, e entra na comparadora como segundo eixo quando houver mais de uma. Arquivo de fonte local e licença: `reference/tipografia.md`.

## A comparadora

Sempre que sobrar mais de uma candidata em cor ou em tipografia, gere uma página comparadora self-contained: a MESMA página (ou as 2 a 3 seções mais representativas: hero, oferta e uma seção escura) com **dois seletores independentes**, um de paleta e um de tipografia. Ao lado de cada opção, o nome e o motivo da candidata.

Todo valor de cor entra como trio R,G,B (`--tk-bg: 246,245,241`) consumido como `rgb(var(--tk-bg))` ou `rgba(var(--tk-bg), .5)`. Os blocos saem prontos do gerador (`--format css` devolve um `[data-palette="p1"]` por candidata): copie os blocos, nunca converta hex a hex na mão. A tipografia usa o mesmo mecanismo num atributo próprio (`[data-type="t1"]` define `--tk-heading` e `--tk-body`). Fontes de arquivo local entram pelo bloco `data-aura-fonts` no `<head>` da comparadora, com os arquivos na pasta que o bloco aponta; sem isso a comparadora renderiza no fallback e a escolha vira chute.

**Dois temas, duas paletas:** quando o membro mantém 2 ou mais temas com paletas diferentes, o snippet de paleta é por tema, com a disciplina de push da rule `.claude/rules/shopify-theme-safety.md`.

## Política do arquivo de marca

- A page-design só escreve no `brand-tokens.json` quando ele está vazio (`source: "none"`): no caminho 2 aqui, e nos caminhos 3 e 4 na ETAPA 6, com `tokens.py --brand-out` a partir da página aprovada. A escolha do membro na comparadora conta como confirmação.
- Fora disso, nunca. O drift da página contra a marca (`tokens.py --diff`) aparece na mensagem final.
- Para mudar a marca, o membro refaz a extração do setup ou edita o arquivo.
- Página antiga (sem `schema_version`): o `design-signals.json` que já existe continua valendo para a `page-build`; o enum antigo de `source` (`refero | screenshot_vision | design_clone | manual`) só vale nela.

## Resumo ao membro

> "Marca: [do arquivo da sua marca / extraída da sua loja / paleta [Nome] que você escolheu / cores que você passou]
> - Fontes: **[heading]** (títulos) + **[body]** (corpo)
> - Paleta: fundo **[background]** · texto **[foreground]** · ação **[primary]**
> - Raio **[radius]px** · sombra **[shadow]** · densidade **[density]**
> O layout vem da direção que a gente escolhe agora, a partir de referências premiadas."
