---
name: reverse-order-insertion
description: Quando AI precisa adicionar múltiplos elementos (sections, blocks, steps) a um arquivo existente via Edit tool, inserir em ordem REVERSA pra preservar line numbers dos edits subsequentes.
paths:
  - .claude/skills/06-page-engine.md
  - .claude/skills/06b-page-sections.md
  - .claude/skills/06c-page-deploy.md
  - .claude/skills/17-content-recycler.md
---

# Reverse-Order Insertion (Technical Rule)

## Problema

Quando AI precisa inserir múltiplos elementos novos em um arquivo (ex: adicionar 5 novas sections ao `page.pdp.json` do Shopify, ou adicionar 3 novos blocks a uma section Liquid), cada Edit/insertion desloca line numbers dos elementos subsequentes.

Exemplo:
- Arquivo tem 200 linhas
- AI precisa inserir section A na linha 50, section B na linha 120, section C na linha 180
- Inserir A primeiro (adiciona 10 linhas) → linha original 120 virou 130, 180 virou 190
- Se AI tinha armazenado "insert at line 120" pra B e "insert at line 180" pra C, Edit falha ou insere no lugar errado

## Regra

**Sempre inserir em ordem REVERSA (da maior line number pra menor).**

Fluxo:

1. Planejar TODOS os inserts antes de executar (collect list of [line_number, content])
2. Ordenar DESCENDING por line_number
3. Executar Edits nessa ordem

Dessa forma cada insert não afeta line numbers dos inserts pendentes.

## Exemplo prático — inserir 3 sections em page.json

```
Planejado:
- Section A em line 50
- Section B em line 120
- Section C em line 180

Executa (reverse):
1. Insert C em line 180 (arquivo fica com 190+ linhas)
2. Insert B em line 120 (arquivo fica com 200+ linhas)
3. Insert A em line 50 (arquivo fica com 210+ linhas)

Resultado: todas sections inseridas nas posições corretas do arquivo original.
```

## Aplicável a

- `page.*.json` templates do Shopify (order matters — position: 1,2,3...)
- Sections Liquid com múltiplos `{%- liquid -%}` block additions
- Arquivos Markdown com TOC sections
- JSON schema arrays (settings[], blocks[], presets[])

## Exceção

Quando inserts são independentes (não referenciam line numbers), ordem não importa — mas manter regra pra consistência.

## Anti-patterns (FORBIDDEN)

- Inserir em ordem crescente e esperar line numbers manterem-se
- Recalcular line numbers entre cada Edit (ineficiente e propenso a erro)
- Usar offset absoluto de arquivo depois de modificar início dele
- Misturar inserts e deletes sem planejar ordem (sempre inserts primeiro em reverse, depois deletes em reverse)
