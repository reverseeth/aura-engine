# Aura HTML Components: as convenções de Markdown do render

Todo relatório `.md` voltado ao membro ganha um `.html` companion (regra 6b do CLAUDE.md). O `.html` nunca é escrito à mão: o `tools/render_report.py` lê o `.md` e monta o `.html` sobre `.claude/templates/aura-report-template.html` (design "Editorial Intelligence": o `<style>` completo, a topbar com a logo SVG canônica, o hero, a meta-bar, o sumário gerado dos `##`, as bandas escuras alternadas, o rodapé e o script de interação). Este arquivo lista o que o conversor entende e como cada construção de Markdown vira um componente do design system.

```
python3 tools/render_report.py workspace/<slug>/market-research/market-research.md
python3 tools/render_report.py <arquivo.md> --lang en --out <saida.html>
python3 tools/render_report.py <arquivo.md> --no-dark
```

Sem `--out`, o `.html` nasce ao lado do `.md`, com o mesmo nome. Sem `--lang`, o idioma do chrome (sumário, rótulos da meta-bar, textos de acessibilidade) vem do frontmatter (`lang`), depois do `report_language` do manifest do produto, e por fim `pt-BR`. A copy do relatório sai exatamente como está no `.md`: o render só troca o chrome de idioma.

## O que o render faz sozinho

| Parte do `.html` | De onde vem |
|---|---|
| Título (hero) | O primeiro `# Título` do `.md` (ou `titulo` no frontmatter) |
| Deck abaixo do título | O primeiro parágrafo depois do `#` (ou `subtitulo` no frontmatter) |
| Eyebrow (linha pequena acima do título) | `eyebrow` no frontmatter; sem ele, "Aura Engine / nome da skill", reconhecida pela pasta onde o `.md` está |
| Selo da topbar ("Relatório · 2026") | `tipo` no frontmatter; sem ele, o nome da skill; o ano vem de `data` ou da data de hoje |
| Meta-bar | O frontmatter (`produto`, `mercado`, `data`, `alimenta`); sem frontmatter, o manifest do produto (`product_name`, `market`), a data de hoje e os consumidores da skill no `.claude/skills.json` |
| Sumário | Um item por `##`, com âncora `#s1`, `#s2`... |
| Seções numeradas | Cada `##` vira uma seção com o número (`01`, `02`...); um "1. " na frente do título é removido, porque o número já aparece |
| Bandas escuras | As seções pares saem em banda escura (`--no-dark` desliga) |
| Logo | A topbar do template, com o mesmo `<svg>` de `.claude/templates/aura-logo-snippet.html`; o render avisa se os dois divergirem |
| Rodapé | "Aura © ano" |
| Robustez mobile | Vem do `<style>` do template: sem `backdrop-filter` abaixo de 860px, reveal com failsafe, zero overflow horizontal |

## Frontmatter (opcional)

Linhas `chave: valor` entre duas linhas `---` no topo do `.md`. Sem frontmatter, a meta-bar sai do manifest.

```
---
produto: Creme de barreira para pele seca
mercado: Estados Unidos
data: 24 jul 2026
alimenta: Competitor Analysis · Offer Builder · Copy Engine
---
```

Chaves reconhecidas: `produto`, `mercado`, `data`, `alimenta` (a meta-bar, com os rótulos traduzidos em `en`: Product, Market, Date, Feeds); `titulo`, `subtitulo`, `eyebrow`, `tipo` (o hero e o selo da topbar); `lang` (`pt-BR` ou `en`). Qualquer outra chave vira um item extra da meta-bar, com a própria chave como rótulo (inicial maiúscula). Quando o frontmatter existe, a meta-bar mostra só o que está nele; nada é preenchido por fora.

## Convenções que viram componentes

| No `.md` | No `.html` | Quando usar |
|---|---|---|
| `## Título` | Seção numerada com label e régua | Toda seção de primeiro nível do relatório |
| `### Título` | Subseção com título grande | Divisão dentro da seção |
| `#### Título` | Parágrafo em negrito | Divisão menor (sem estilo próprio no design system) |
| `> **Nota:** texto` | Card `.note` (neutro) | Contexto auxiliar, pendência, observação |
| `> **Atenção:** texto` | Card `.callout` (marca preta) | Recomendação, ponto de atenção, decisão |
| `> **Oportunidade:** texto` | Card `.opportunity` | Lacuna de mercado, espaço aberto |
| `> **Risco:** texto` | Card `.danger` (vermelho) | Risco, erro a evitar; o único componente com cor |
| `> **Vencedor:** Nome` + parágrafo | Card `.winner` com o nome em destaque | Mecanismo ou conceito vencedor |
| `> "frase do cliente"` | Citação `.quote` (VOC) | Frase exata de cliente; a linha `Tradução livre: ...` vira a tradução pequena e a linha `Fonte: ...` (ou `— origem`) vira a fonte |
| Tabela `KPI \| Valor` (duas colunas) | `.kpi-grid` com números grandes | Até 3 ou 6 números que resumem a seção; o valor anima quando é numérico (`58%`, `$67.90`, `2.4`) |
| Qualquer outra tabela | `.table-wrap` com a tabela do design system | Comparações, checklists, mapas de alavancas |
| Lista `-` ou `1.` | `<ul>` / `<ol>`, com aninhamento por recuo | Itens paralelos; uma citação recuada dentro do item vira `.quote` dentro dele |
| `- [ ]` e `- [x]` | Item com ☐ ou ☑ | Checklists |
| Bloco entre ` ``` ` | `<pre>` com rolagem horizontal | Árvores de pastas, comandos, JSON |
| `---` | Régua horizontal | Separação forte dentro da seção |
| `**negrito**`, `*itálico*`, `` `código` ``, `[texto](url)`, `![alt](src)`, `~~riscado~~` | O equivalente em HTML | Texto corrido |

Os rótulos dos cards são aceitos em português e em inglês, sem distinção de maiúsculas: `Nota`/`Note`, `Atenção`/`Attention`/`Warning`/`Aviso`, `Oportunidade`/`Opportunity`, `Risco`/`Risk`/`Perigo`/`Danger`, `Vencedor`/`Winner`. O rótulo escrito no `.md` é o que aparece no card.

Um card pode ter mais de um parágrafo e listas dentro: basta manter o `>` em todas as linhas (linha `>` vazia separa parágrafos).

```
> **Oportunidade:** nenhum concorrente cita um estudo pelo nome.
>
> Ser o único com o estudo na página ataca essa lacuna de uma vez.
> - Andersen 2016 (meia-vida da melatonina oral)
> - Gooneratne 2012 (timing, não dose)
```

Citação de cliente completa:

```
> *"My skin feels tight and flaky an hour after I moisturize."*
> Tradução livre: minha pele fica repuxada e descamando uma hora depois de passar hidratante.
> Fonte: Reddit r/SkincareAddiction
```

Números grandes:

```
| KPI | Valor |
|---|---|
| frases reais de cliente coletadas | 199 |
| da população acorda 3+ noites por semana | 31% |
| meia-vida da pílula de melatonina | 54 min |
```

Uma parte dos componentes do template não tem convenção de Markdown e o render não os produz: `faq`, `check-row`, `pill`, `score`, `voc-words`, `script-block`. No `.md`, o mesmo conteúdo sai como lista, tabela ou texto com negrito; o resultado continua dentro do design system.

## Regras

1. **Nunca escrever o `.html` à mão.** Nem copiar `<style>`, nem topbar, nem logo: o render faz tudo isso a partir do template, e é o único caminho que garante a logo SVG em todo relatório.
2. **Nunca truncar conteúdo.** O render nunca corta texto; o `.md` também não deve cortar célula, hook ou claim com "...". Célula longa se resolve com quebra de linha ou com um card.
3. **HTML cru no `.md` vira texto.** O conversor escapa tudo que não é Markdown reconhecido; comentários HTML (`<!-- -->`) são descartados.
4. **Emojis ✅ ⚠️ ❌ são aceitos** em relatório interno (exceção da regra 7 do CLAUDE.md); em página voltada ao consumidor final valem ícones SVG, e essa página não passa por este render.
5. **Idioma do chrome segue o `report_language`.** Membro `en`: `lang="en"`, "Contents", Product/Market/Date/Feeds. A copy do relatório sai como está no `.md`.
6. **O `.claude/OVERVIEW.html` é gerado pelo mesmo render**, via `python3 tools/gen_docs.py` (alvo `overview-html`), a partir do `OVERVIEW.md`; nunca é editado à mão, e o `gen_docs.py --check` acusa se ficar para trás.

## Extensão

Componente novo entra em três lugares: (1) o CSS em `aura-report-template.html`, dentro do `<style>`; (2) a convenção de Markdown correspondente no `tools/render_report.py`; (3) a linha desta tabela. Componente sem convenção no conversor não existe para as skills, porque nenhuma skill escreve HTML.
