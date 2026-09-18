# Setup · Referência: Idioma dos relatórios e como a Aura funciona (ETAPAs 2.6 e 2.7)

> A pergunta bilíngue do idioma dos relatórios com a captura de `REPORT_LANGUAGE`, a regra de que a conversa segue no idioma escolhido e a copy consumidor-final fica em inglês, e o resumo de 30 segundos das cinco fases da Aura em pt-BR com a estrutura para `en`. Abra na ETAPA 2.6.

### ETAPA 2.6 — Idioma dos Relatórios (PERGUNTA 1, ANTES DE QUALQUER OUTRA)

**ANTES de qualquer outra pergunta, pergunte o idioma.** Os relatórios internos (market research, competitor analysis, offer briefs, copy docs, ad strategy, audits, etc.) precisam ser gerados num idioma que o membro entenda — sem isso ele não consegue usar nada do que a Aura produz.

Pergunte exatamente assim, em português E em inglês na mesma mensagem (membro escolhe sem precisar entender uma das línguas):

> **Antes de tudo / Before we start:**
>
> Em qual idioma você quer os relatórios internos (market research, briefings, análises)?
> Which language do you want for internal reports (market research, briefings, analyses)?
>
> **1.** Português (padrão Brasil)
> **2.** English (international members)
>
> Responda só `1` ou `2` / Reply just `1` or `2`.

Capture a resposta em `REPORT_LANGUAGE`:
- `1` → `"pt-BR"`
- `2` → `"en"`

**A partir desse ponto, TODA conversa com o membro acontece no idioma escolhido.** Se ele escolheu inglês, faça as 4 perguntas da ETAPA 3 traduzidas, gere o `profile.md` em inglês, e a partir dali todas as skills futuras vão respeitar essa escolha lendo `profile.md.report_language`.

**Importante:** copy pro consumidor final (ads, landing pages, PDPs do mercado US) **continua sempre em inglês** independente dessa escolha. Essa escolha vale só pra documentação INTERNA do membro (relatórios, análises, briefings que ele lê pra entender o trabalho). A regra 0 do CLAUDE.md detalha.

### ETAPA 2.7 — Como a Aura funciona (só na primeira vez, no idioma escolhido)

Logo depois da escolha de idioma e ANTES das 4 perguntas, dê ao membro um resumo curto de como o sistema funciona — só na primeira vez (sem `workspace/profile.md`). Use o `REPORT_LANGUAGE` escolhido. Mantenha leve e claro, sem jargão.

**Se `pt-BR`:**

> Antes das perguntas, 30 segundos sobre como isso funciona:
>
> O Aura Engine é o seu time de marca e marketing num lugar só. Ele constrói sua operação **em fases**, e cada fase usa o que a anterior descobriu — você nunca repete informação:
>
> 1. **Pesquisa** (produto → mercado → concorrência): o que vender, pra quem, e o que os concorrentes deixam na mesa.
> 2. **Estratégia** (oferta → copy): a oferta irresistível e o texto que vende.
> 3. **Loja** (página → tracking → checkout → bônus → flows de recuperação): tudo numa página que converte, com medição certa, os bônus prometidos já prontos, e os emails de carrinho abandonado e pós-compra armados antes do primeiro anúncio.
> 4. **Tráfego** (criativos → visibilidade pra agentes de AI → auditoria → ads → análise → escala): os anúncios, a loja visível pros assistentes de compra com AI (ChatGPT, Perplexity), a checagem de coerência, subir e escalar.
> 5. **Pós-venda** (retenção completa → medição dos bônus → reciclagem): win-back e reposição por email/SMS, medição dos brindes, e o anúncio que provou escalar rendendo o máximo que ele ainda pode dar.
>
> Você dispara qualquer fase só falando o nome dela. Eu sempre te digo qual é o próximo passo. E cada produto ganha um painel — o **ABRIR-AQUI.html** — que mostra o que já está pronto e o que abrir.

**Se `en`:** mesma estrutura, traduzida naturalmente (Research → Strategy → Store (page → tracking → checkout → bonuses → recovery flows) → Traffic (creatives → AI-agent visibility → audit → ads → analysis → scale) → Post-purchase; "every product gets a dashboard — **ABRIR-AQUI.html** — showing what's done and what to open").

Se NÃO for primeira vez (membro refazendo setup), pule esta etapa.
