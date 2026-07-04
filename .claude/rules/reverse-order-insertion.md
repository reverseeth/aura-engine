---
name: reverse-order-insertion
description: Segurança em inserções múltiplas num mesmo arquivo. Em arrays indexados por posição (order[], block_order de templates Shopify), inserir em ordem reversa pra não deslocar índices pendentes. Em edits por anchor de texto (Edit tool), o risco real é anchor ambíguo/sobreposto — planejar anchors disjuntos antes.
paths:
  - .claude/skills/07b-page-build.md
  - .claude/skills/14-content-recycler.md
---

# Multi-Insert Safety (Technical Rule)

Duas situações diferentes com riscos diferentes. Não confundir.

## Caso 1 — Inserção por ÍNDICE em arrays (order[], block_order, settings[])

**Problema real:** em arrays posicionais (ex: `order[]` do `page.*.json` do Shopify, `block_order` de uma section), inserir na posição 2 desloca tudo que vem depois. Se você planejou "inserir X na posição 2, Y na posição 5, Z na posição 8" e executa em ordem crescente, as posições 5 e 8 já não são as que você calculou.

**Regra:** inserir em ordem REVERSA (da maior posição pra menor).

1. Planejar TODOS os inserts antes de executar (lista de `[posição, conteúdo]`)
2. Ordenar DESCENDING por posição
3. Executar nessa ordem — cada insert não afeta as posições dos pendentes

```
Planejado (posições do array original):
- Section A na posição 2
- Section B na posição 5
- Section C na posição 8

Executa (reverse): C na 8 → B na 5 → A na 2
Resultado: todas nas posições corretas do array original.
```

No modo batch da skill 07b o conversor já cuida disso; a regra vale quando o Claude ajusta o JSON à mão.

## Caso 2 — Edits por ANCHOR de texto (Edit tool)

O Edit tool ancora em `old_string` (match de string única), **não em números de linha** — inserir cedo no arquivo NÃO invalida um edit posterior por "deslocamento de linha". Os riscos reais são outros:

| Risco | Como acontece | Prevenção |
|-------|---------------|-----------|
| Anchor deixa de ser ÚNICO | Um edit anterior inseriu conteúdo parecido com o anchor do próximo edit | Escolher anchors longos e específicos; planejar todos os edits antes |
| Anchors SOBREPOSTOS | Dois edits mexem no mesmo trecho; o primeiro altera o texto que o segundo usava de anchor | Anchors disjuntos (regiões que não se tocam); se dois edits tocam o mesmo trecho, fundir num edit só |
| Offset stale em Read | Depois de editar, um `Read` com offset/limit calculado ANTES do edit lê a região errada | Re-ler a região após edits se for usar offset; preferir anchors de texto a offsets |

**Regra prática:** planejar todos os edits antes de executar, usar anchors disjuntos e únicos, e se um Edit falhar ("string not found" ou "not unique"), re-ler o arquivo antes de tentar de novo — nunca "chutar" uma variação do anchor.

Inserir de baixo pra cima (fim do arquivo primeiro) continua sendo um bom default: conteúdo já inserido nunca vira parte do contexto de um anchor seguinte.

## Anti-patterns (FORBIDDEN)

- Em arrays posicionais: inserir em ordem crescente e esperar os índices se manterem
- Raciocinar por número de linha com o Edit tool (o mecanismo é string match — pensar em anchors, não em linhas)
- Re-tentar um Edit falhado variando o anchor no chute, sem re-ler o arquivo
- Misturar inserts e deletes sem planejar ordem (inserts primeiro em reverse, depois deletes em reverse)
