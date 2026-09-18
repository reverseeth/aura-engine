# Offer Builder · Referência: SALVAR e mensagem final

> O texto integral da seção SALVAR (dual output e o conteúdo do `offer-builder.md` seção a seção) e da mensagem final. Abra ao fechar a oferta.

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Toda skill que salva `.md` em `workspace/` DEVE gerar `.html` companion** com o mesmo nome (ex: `offer-builder/offer-builder.md` → `offer-builder/offer-builder.html`). O `.md` é fonte pra AI das fases seguintes; o `.html` é visualização humana e nunca é escrito à mão: gere com `python3 tools/render_report.py <caminho do .md>` (o script aplica o design system, a topbar com a logo e o sumário; cards, números grandes e citações nascem das convenções de Markdown de `.claude/templates/aura-html-components.md`).


`workspace/[produto]/offer-builder/offer-builder.md` contendo:
1. Mecanismo único recomendado — a LÓGICA de UMP e UMS com nomes e estudos citados (Etapa 2D; sem versões de copy)
2. **Banco de provas** (Etapa 2.5) — os números, estudos e citações prontos pra copy usar como munição
3. Estrutura de oferta completa (produto principal, bundles, arquitetura de assinatura se consumível, bump, upsell, stack de valor)
4. Garantia recomendada + copy
5. Unit economics em DUAS tabelas separadas — primeiro pedido (5A) e recompra (5B) — mais o AOV blended quando as duas existem (Etapa 5). Nenhum número desta seção é chamado de "lucro"
6. AOV projetado (Etapa 6)
7. LTV e PSM explicados como conceitos separados + PSM projetado, com a frase que separa CAC de CPA (Etapa 7)
8. Simulação de budget em 2 níveis, com margem de contribuição e resultado após custos fixos como linhas distintas (Etapa 8)
9. Checagens de sanidade como afirmações do que está validado (Etapa 9)

O doc segue `.claude/rules/report-only-results.md`: só o resultado — sem narração de processo, sem descrição de ausências, sem referência à conversa.

Também salvar companion `offer-builder/research-foundation.json` conforme schema da Etapa 2.5.

## Mensagem Final

"Primeira versão da oferta pronta. Mecanismo único: **[Nome do Mecanismo]** (rota: [recombinação validada / criação original]). PSM projetado: [valor]. Viável pro seu budget: [sim/com ajustes].

Margem de contribuição por pedido: [valor] — é o que sobra depois dos custos variáveis. [SE os custos fixos não foram informados: "Sem os seus custos fixos mensais na conta, não dá pra dizer se há lucro; me passa esse número quando tiver e eu fecho a simulação."]

Revisa antes de seguir: o nome do mecanismo gruda? O pricing e o stack fazem sentido pro seu avatar? A garantia ataca o medo certo? Me diz o que não fecha e eu itero.

Quando fechar: diga **'copy'** pra escrever a copy completa da página aplicando o mecanismo, stack, garantia, e linguagem do market research."
