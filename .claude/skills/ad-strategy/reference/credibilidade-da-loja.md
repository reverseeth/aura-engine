# Ad Strategy · Referência: Leitura de credibilidade da loja (ETAPA 2)

> Os sistemas nomeados que fundamentam a leitura, o checklist do que verificar (perfis sociais, reviews, sinais de confiança, flows de recuperação, gestão de comentários), o playbook legítimo de primeiras reviews por stage, o guardrail do que é proibido e a nota de honestidade. Abra na ETAPA 2.

### ETAPA 2 — Leitura de Credibilidade da Loja (lever de conversão, pré-launch)

Antes de gastar em tráfego, a loja precisa **parecer confiável** — isso afeta conversão direto, e tráfego pago em loja sem prova social queima budget. Esta etapa é um **checklist de leitura**, não bloqueante por default (vira WARN), mas o membro precisa ver o gap antes de ativar.

**Fundamente a leitura de credibilidade nos SISTEMAS NOMEADOS (rode a `best_query` de cada um — nunca query genérica):**
- **Cialdini's Six Weapons of Influence** (rode `Cialdini six weapons of influence reciprocity commitment social proof authority liking scarcity`) — social proof e authority são as alavancas que a PDP/página de FB precisam exibir antes do tráfego chegar.
- **Bandwagon Effect (3 Group Types)** (rode `bandwagon effect aspirational associative dissociative groups social pressure conformity`) — por que ~100 reviews em inglês move conversão (massa visível = "todo mundo compra").
- **Inoculation Theory** (rode `inoculation theory McGuire weakened attack pre-emptive defense competitor argument resistance`) — base pra responder objeção nos comentários do ad antes que o ceticismo contamine o leitor seguinte.
- **Length-Implies-Strength Heuristic** (rode `length implies strength heuristic volume of content persuasion cue numbered reasons testimonials`) — volume de review/UGC sinaliza força mesmo antes de ser lido.

Verificar (e reportar o que falta):

- **Instagram + página do Facebook ativos**, com seguidores reais e posts recentes (a página do FB é o que aparece como anunciante no ad).
- **Reviews na PDP** — alvo ~100 avaliações em inglês (do mercado US). Menos que isso, conversão sofre. (A cadeia storefront, `page-design` → `page-build`, já injeta reviews; aqui só confirmamos volume.)
- **Sinais de confiança visíveis**: brand story / About, destaques (TrustPilot se tiver), garantia clara, política de envio/retorno legível.
- **Flows de recuperação ativos (`retention-engine` Fase A)**: abandoned cart + post-purchase configurados no ESP e ATIVADOS antes do go-live — é a receita mais barata do launch (recupera parte dos ~70% de carrinhos abandonados a custo zero, free tier do ESP). Se `manifest.retention.phase_a_done != true`, recomendar rodar `'retention'` (`retention-engine` Fase A) antes de ativar a campanha — WARN, não bloqueia.
- **Gestão de comentários — o ponto mais importante**: comentário ruim num post de ad fica **visível pra todo mundo** e derruba conversão. O membro precisa de uma rotina pra **deletar/ocultar spam e responder objeção** nos comentários dos ads. Recomendar verificar comentários nos primeiros dias e responder rápido.

**Zero reviews → primeiras reviews (playbook legítimo, por stage):** loja nova não fica esperando review "acontecer" — constrói as primeiras com processo:

1. **Seeding de produto (starter/validating):** enviar 20-30 unidades pra micro-influencers e membros de comunidades do nicho em troca de **review honesta** (com disclosure de produto recebido). Custo = COGS de 20-30 unidades; retorno = as primeiras dezenas de reviews reais + UGC aproveitável nos criativos.
2. **Review request retroativo via app:** se a loja já teve QUALQUER venda (orgânica, amigos, marketplace), o app de reviews (Judge.me/Loox/Yotpo) dispara request pra compras passadas — recupera reviews que já existiam como clientes.
3. **Incentivo no pós-compra (`retention-engine` Fase A):** o Email 3 do flow post-purchase (dia 7-10) pede a review com incentivo — cada venda do launch alimenta o contador automaticamente.
4. **Brinde por foto/review (coordenar com a `bonus-delivery`):** GWP ou desconto na próxima compra em troca de foto + review honesta — foto real de cliente vale mais que texto.

**Guardrail explícito (PROIBIDO, sem exceção):** comprar reviews; importar reviews de OUTRO produto (ex: import de AliExpress de um listing diferente); ou condicionar o incentivo a review POSITIVA — incentivo é por review **honesta**, qualquer nota (condicionar a nota derruba a loja quando descoberto).

**Honestidade (não grey-hat):** NÃO recomendar comprar seguidor/comentário/review fake em volume. Além de risco pra conta e pra marca, prova social falsa não sustenta a venda — o foco é prova social **real** (reviews de clientes, UGC, depoimentos). Se a loja está fraca em prova social, isso é um sinal de que talvez seja cedo pra escalar budget — melhor começar menor e acumular review real (o playbook acima acelera exatamente isso).

Stage: pra **starter** sem prova social ainda, deixar explícito que rodar com budget pequeno enquanto acumula review é o caminho. Pra **scaling**, isso já está resolvido — só confirmação rápida.
