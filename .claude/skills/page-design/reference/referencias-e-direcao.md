# Page Design · Referência: Referências e direção (ETAPA 3)

> O board de referências (Awwwards, com WebSearch de reserva), as 3 referências que o membro marca, a imagem de cada uma para o revisor, as 3 direções do taste-skill, a escolhida gravada em `page/direction.md` no formato fixo, e onde tudo fica salvo. Abra depois da marca (ETAPA 2) e antes da construção (ETAPA 4).

## Por que vem antes do HTML

Página desenhada sem referência sai na média do que o modelo já viu, e a média é a cara de template. Aqui o membro escolhe o que admira entre páginas premiadas, e um sorteio fora do modelo escolhe a direção, porque o modelo, quando escolhe sozinho, devolve sempre o padrão da categoria.

## 1. Reaproveite o que já existe

- **Board da marca no Instagram:** se existir `workspace/<slug>/social-engine/` com board ou direção visual, ele é o ponto de partida. Loja e Instagram precisam parecer a mesma marca.
- **Páginas do membro:** pergunte em uma linha se ele tem páginas que admira. Link colado entra primeiro no board, com `source: "member"`.

## 2. Board (8 a 12 referências)

1. **Awwwards** (`mcp__awwwards__`): `search_sites` com `responseMode: "compact"` e `sortBy: "score"`, em 2 a 4 buscas: `award: "ecommerce"` sozinho (a coleção é pequena, cerca de 30 sites, e com `query` junto costuma voltar vazia), depois `query` com o nicho sem `award` e `tags` da categoria. Quando a busca devolve "Loose matches", abra esses slugs com `get_site_details`. Some `search_elements` para a seção que o board ainda não cobre (hero, oferta, prova, rodapé). Com a skill `awwwards-inspiration` instalada, siga o roteiro dela para as buscas.
2. **Reserva, só sem o Awwwards na sessão:** WebSearch das landings dos concorrentes de `competitor-analysis/dados.json` (`landing_formats[]`) e da categoria (`source: "websearch"`). O Refero não entra nesta busca. Sem nenhum dos dois, avise e siga com o que o membro trouxer.
3. Uma linha por referência na tabela do `design-system.md` (seção "Board de referências"): link, fonte e o que se tira dela em pelo menos um eixo concreto (tipografia, grid, paleta, tratamento de foto, componentes). Referência sem eixo concreto sai do board.

Das referências sai estrutura e linguagem visual, nunca copy, imagem, logo, marca ou claim.

## 3. O membro marca 3

Mostre o board e peça as 3 que ele mais quer seguir. Para cada marcada, tire a imagem que o revisor da ETAPA 5 vai ver:

```bash
python3 .claude/lib/theme-verify/verify_page.py "<url>" --desktop-only --shots-dir workspace/<slug>/page/references/<n>/
```

O perfil loja checa marcadores da Aura e falha numa página de terceiro; ignore o exit code e **olhe a imagem**: site com loader em JavaScript sai como uma tela de "Loading...". Nesse caso, ou quando o site bloqueia (Cloudflare, 403), baixe o "Full-size screenshot" que o `get_site_details` do Awwwards devolve para o mesmo caminho; sem ele, tente a próxima do board ou peça um print ao membro.

## 4. Três direções e a escolha

**Com o taste-skill** (plugin; o script fica em `~/.claude/plugins/cache/taste-skill/taste-skill/<versão>/skills/taste-skill/scripts/draw.mjs`):

```bash
node <draw.mjs> --sector <ecommerce|physical-product|fashion> --brief "<uma linha do produto>" --options 3 --out workspace/<slug>/page/.taste/
```

Some `--keep palette,type` quando o `brand-tokens.json` não está vazio: a marca fixa cor e tipo, o sorteio decide o resto. Setor: `fashion` para vestuário e acessório de moda, `physical-product` para produto com objeto a mostrar, `ecommerce` no resto. Mostre as 3 ao membro em 2 linhas cada, no `report_language`, e ele escolhe 1. Depois gere a folha completa e guarde a saída:

```bash
node <draw.mjs> --sector <o mesmo> --brief "<o mesmo>" [--keep palette,type] --direction <id> --out workspace/<slug>/page/.taste/ > workspace/<slug>/page/direction-sheet.md
```

**Sem o taste-skill:** escreva 3 direções a partir do board e das 3 marcadas, cada uma com uma ideia de composição que nasce do produto (não da categoria), e o membro escolhe 1.

## 5. `page/direction.md` (formato fixo)

Traduza a folha (ou a direção escrita à mão) para este formato. Os cabeçalhos são fixos, porque o `legal_check.py` e o revisor leem por eles:

```markdown
# Direção: <nome da direção>

<a ideia em 2 a 3 frases: "nesta página, <material do produto> vira <o recurso>">

## Tipografia
- família: <nome> (heading)
- família: <nome> (body)
<escala: os 5 passos de tamanho, caixa, peso>

## Paleta
- background: #...
- surface: #...
- foreground: #...
- primary: #...
- on_primary: #...
- accent: #...
- muted: #...
- border: #...
<onde o accent aparece, qual é o chão de cada faixa>

## Hero
<geometria em 1440 e em 390, onde fica a headline, a imagem e o CTA>

## Blueprint por seção
### <id do sections_plan>
<geometria: colunas, proporção, o que fica onde>

## Proibido nesta página
- <o que esta página nunca faz>
```

Regras da tradução:
- Tipografia e paleta vêm do `brand-tokens.json` quando ele não está vazio; vazio, da folha ou da comparadora da ETAPA 2.
- Um subtítulo por id do `sections_plan`, na ordem do `section_order`. Seção da folha sem par no plano sai; seção do plano sem par na folha ganha o blueprint de seção da folha mais próximo.
- A seção de imagens da folha não vale: as imagens vêm do mapa de mídia da 1.6 (fotos reais do produto, Higgsfield ou o `assets.mjs` de reserva em `reference/assets-de-imagem.md`). Nada de picsum.
- O que a folha pede em JavaScript (`stage.js`, blend, carrossel arrastável) vira a versão CSS de `reference/modo-direcao.md`, ou sai e entra em "Proibido nesta página".

Mostre o `direction.md` ao membro. Sem a aprovação da direção, a ETAPA 4 não começa.

## 6. Onde fica salvo

- `page/references/<n>/desktop-full.png`: imagem das 3 marcadas.
- `page/direction.md` (e `page/direction-sheet.md` quando veio do taste-skill).
- `page-plan.json` → `reference_board`: `{ "references": [{ "url": "...", "title": "...", "source": "awwwards | websearch | member", "marked": true, "image_path": "references/1/desktop-full.png", "takeaways": ["grid: ..."] }], "direction": { "feel": "...", "signature": ["..."], "forbidden": ["..."] }, "social_board_reused": false }` e `direction_ref: "direction.md"`. O bloco `direction` (sensação, assinatura, proibido) continua porque a `social-engine` lê.
