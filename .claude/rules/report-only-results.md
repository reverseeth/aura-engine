# Report Only Results (NON-NEGOTIABLE)

> Aplica a TODO relatório salvo em `workspace/` (.md e .html), de TODA skill.
> O doc é o produto final que o membro lê e que as fases seguintes consomem — não é um diário da execução.

## Regra

**Todo doc de workspace contém apenas o resultado final.** Zero meta-texto. O membro abre o doc e vê a análise, a estratégia, os números — nunca a história de como o doc foi feito, o que ele não contém, ou a conversa que o gerou.

## O que é PROIBIDO dentro do doc

### 1. Narração de processo ou de correções

O doc nunca conta o que foi feito, mudado, removido ou decidido durante a execução. Correção aplicada = o doc nasce corrigido, como se a versão anterior nunca tivesse existido.

- ❌ "Removi a seção X" / "Corrigido: o valor anterior estava errado" / "Refinamento da tese"
- ❌ "Decidi não incluir [X] aqui" / "Deixei [Y] pra fase seguinte porque..."
- ✅ (nada — a decisão simplesmente se reflete no conteúdo)

### 2. Descrição de ausências

O doc nunca descreve o que ele NÃO tem ou o que NÃO existe na estratégia. Se algo não faz parte, simplesmente não aparece.

- ❌ "tudo é físico (sem componente digital)"
- ❌ "Como o funil não tem [X], não há [Y] a gerar"
- ❌ "Esta oferta não usa [Z]"
- ✅ (descrever só o que EXISTE)

### 3. Referência ao membro ou à conversa

O doc nunca cita a conversa que o originou. Perguntas do membro são respondidas com o conteúdo em si, não com a menção à pergunta.

- ❌ "Você perguntou se..." / "Como você pediu" / "como você prefere" / "exatamente o que você pediu"
- ✅ (a resposta vira uma seção normal do doc, ex: uma explicação limpa do conceito)

### 4. Auto-referência da AI

O doc nunca fala de quem o escreveu nem justifica escolhas de escrita.

- ❌ "sem viés meu" / "não escrevi [X] aqui de propósito" / "a próxima fase vai decidir sozinha"
- ✅ (nada)

### 5. Perguntas retóricas como estrutura

Títulos de seção e itens de checagem são afirmações, não perguntas.

- ❌ "Margem sustenta tráfego pago?" · "O mecanismo é diferente?"
- ✅ "Margem sustenta tráfego pago." + a evidência em 1 frase
- (Checklists internas de skill podem ser perguntas — é formato de trabalho. Na hora de ESCREVER o doc, viram afirmações do que está validado.)

## Onde a meta-informação vive (ela não morre — muda de lugar)

| Tipo de informação | Lugar certo |
|---|---|
| O que foi corrigido/mudado nesta rodada | Mensagem de chat pro membro (curta), nunca o doc |
| Flags operacionais (dado estimado, campo pendente) | `dados.json` (machine-readable) + no doc apenas o efeito prático, sem história |
| Decisão de design da skill (o que fica pra outra fase) | A própria skill (.md da skill), nunca o doc do membro |
| Pendência que exige ação do membro | Pode aparecer no doc como "Pendência": o que falta + o efeito de destravar. Sem narrar como chegou ali. |

Exemplo de pendência bem escrita: "O produto ainda não tem cotação fechada. Com os preços exatos, [métricas X e Y] ficam mais precisas. Nenhuma conclusão muda." — informa o estado e o efeito, sem contar a história das tentativas.

## Teste final antes de salvar

Reler o doc perguntando, frase a frase: **"esta frase informa algo sobre o NEGÓCIO, ou informa algo sobre a EXECUÇÃO do doc?"** Frase sobre a execução → deletar ou mover pro chat/dados.json.

## Anti-patterns (FORBIDDEN)

- Bloco de "correções aplicadas" ou changelog dentro do doc
- Frase que existe só pra justificar a estrutura do doc ("esta seção existe porque...")
- Responder feedback do membro adicionando meta-comentário em vez de reescrever o conteúdo
- Checagens de sanidade em formato de pergunta no doc final
- Descrever o escopo pela negativa ("não inclui X, não faz Y")
