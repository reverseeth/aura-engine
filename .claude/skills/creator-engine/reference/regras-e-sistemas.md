# Creator Engine · Referência: As sete regras que não se negociam e os sistemas nomeados a puxar

> As sete regras (inglês no material de creator, whitelisting só de vencedor, transparência por tier, contrato como referência, licença de conteúdo, remuneração nunca inventada, campanha fora do escopo), a divisão do domínio com a marketplace-engine, a lista dos sistemas da Fase A e da Fase B com as queries exatas e a nota de quais ETAPAs rodam em cada fase. Abra antes de qualquer etapa.

### Regras que não se negociam

1. **Material de creator é inglês US, sempre** — brief, mensagem, contrato, report. Relatório interno segue `report_language`.
2. **Whitelisting só de creator que já tem breakthrough com a marca, e só com os ads DELE na página dele.** As duas primeiras regras da fonte, sem exceção. Whitelisting amplifica vencedor; não procura vencedor.
3. **Transparência por tier:** creator em retainer simples NÃO vê receita/ROAS (só spend e soft metrics — senão pede aumento sem entender os outros custos); creator no programa de performance vê os números (ele ganha % deles).
4. **Contrato gerado é referência, não aconselhamento jurídico** — a própria fonte diz isso dos templates dela. Todo contrato salvo carrega esse aviso e a recomendação de revisão por advogado.
5. **Conteúdo de terceiros sem licença não vai ao ar.** A fonte pratica o "borrowed time" (rodar vídeo ripado do TikTok Shop com metadata limpa); o guard-rail desta engine é o da `creative-engine`: clipe de terceiro serve como referência de estrutura e timing, nunca entra em ad sem cessão de direitos. Conteúdo do roster É licenciado — o contrato/plataforma cede os direitos por escrito.
6. **Números de remuneração não se inventam:** ou são os defaults da fonte (declarados como referência) ou vêm do membro. Nenhum tier novo sai de estimativa.
7. **Campanha é território da `ad-strategy`/`scale-engine`.** Esta skill entrega gente, acesso e conteúdo; nunca cria campanha, ad set ou regra de budget.

### Puxe os SISTEMAS NOMEADOS da base (NUNCA query genérica)

Os domínios desta skill são `affiliate-creator-channels`, `creatives-hooks-formats`, `meta-ads-strategy`, `scaling`, `team-hiring-ops` e `competitor-positioning`; os sistemas de recrutamento pago e de ad bounties existem em mais de um domínio e apontam pro MESMO conteúdo.

**Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill creator-engine --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 10 buscas por etapa. As queries já embutidas na etapa são o mínimo garantido. Não repita busca de framework já puxado na sessão.

**Divisão do domínio `affiliate-creator-channels` com a skill `marketplace-engine`:** a `marketplace-engine` é dona do canal (TikTok Shop como canal de venda, Social Snowball, custom link, recrutamento pago de afiliados, Amazon e a regra de entrada de marketplace); esta skill é dona da pessoa (Creator Farming, Whitelist Ads e o recorte creator/afiliado dessas mesmas entradas: quem grava, como recrutar, comissão e relação). Puxe uma entrada de canal aqui só quando a pergunta for sobre a pessoa que opera o canal.

**Mínimo a carregar na Fase A:**

- **Content Engine (casting → produção → review → seeding, corte em 3 hooks)** — `content engine framework casting producao review 3 timestamps 3 hooks Insense seeding SOP`
- **UGC Creator Sourcing Engine (2 papéis + aprovação em 7 passos + tracker diário)** — `engine de 2 roles sourcer VA senior 7-step approval workflow hashtag hunting daily tracker`
- **Creator Diversity Matrix** — `creator diversity matrix idade raca genero idioma espanhol caracteristicas fisicas psicografia`
- **Creator Brief Generator (14 seções)** — `creator brief generator 14 secoes must-say must-avoid emotional memory prompts hook direction`
- **UGC Brief Prompt (perguntas sobre o creator + shot list em 2 partes)** — `UGC brief prompt perguntas sobre creator direct camera shot list b-roll`
- **Estrutura de time criativo por faturamento (o modelo de um único creator)** — `estrutura de time criativo por faturamento creative pods Leanne model um creator`
- **Creator Pipeline (hit rate 14% de creators vs 4% interno)** — `creator pipeline hit rate 14 por cento creators versus 4 por cento interno`
- **DailyVirals Workflow (sandbox / transcript / AI analysis / AB compare)** — `DailyVirals virais do dia TikTok Shop transcript downloader rewriter AB compare sandbox`
- **Rip Method + Borrowed Time (só como referência de estrutura — regra 5 acima)** — `ripar top videos tiktok shop limpar metadata borrowed time criativo proprio ao lado`
- **Operação de TikTok Shop** _(dormant até esta skill)_ — `operacao de TikTok Shop samples afiliados comissao e conteudo`
- Setup da campanha de seeding (objetivo, screening questions, valor de varejo mínimo) — `product seeding no Insense awareness reach screening questions valor de varejo minimo 30`
- Campanha paga por vídeo e o objetivo real do processo — `objetivo do product seeding achar brand ambassador nao winning ad campanha paga 100 150 por video`
- Framework em vez de script (o doc de blocos) — `frameworks vs scripts documento de 6 blocos max 9 concepts dealer's choice first-pick bias`
- Curadoria do framework por creator — `curadoria de framework por creator first-pick bias 4 a 6 conceitos freestyle script espectro`
- Follow-up e coleta — `follow-up com creator a cada 3 dias coleta conteudo drive marcar DCT corte em 3 hooks`

**Adicionalmente na Fase B:**

- **Brand Ambassador Ladder (retainer + comissão em degraus)** — `retainer 500 por video semanal performance program regra do 2-3 comissao decrescente 10 5 2.5 1`
- **Feedback Loop de Creator via Atria + benchmarks de soft metric** — `custom report por creator ad name contains thumb stop ratio 42-48% 3s ate 15s Loom`
- **Whitelisting de Creators (6 regras + Leasy + faixas de budget)** — `whitelisting rodar ads do perfil do creator Leasy custom request 6 regras over-leverage`
- **Partnership Ads (dynamic identity + pitch de 30 dias)** — `partnership ads dynamic identity 1.3% mais barato pedir acesso 30 dias creator novo`
- **Whitelist Ads / página de nicho spin-off** — `whitelist ads pagina de nicho spin-off rodar ads pelo perfil do creator`
- **Whitelisted/Affiliate Ad Discovery (espionar o ecossistema do concorrente)** — `facebook ads library buscar termos que a marca usa revela whitelisted pages creators`
- **Raw Content Campaign** — `raw content campaign creators seeding Insense flexible ads low intent brand ambassadors`
- **Full Media Buying 2026 (as 5 camadas — onde a raw content vive)** — `estrutura full media buying 2026 cinco camadas main CBO ABO zombie raw content promo`
- **Levels of Scaling (quando raw content e whitelisting entram)** — `levels of scaling zero to 50k 100k per day one campaign CBO raw content ASC whitelisting segmented`
- **Creator Farming** — `creator farming cultivar base de creators antes de precisar deles`
- **Recrutamento pago de afiliados + TikTok Shop como máquina de conteúdo** — `rodar paid ads para recrutar afiliados save 40% apply to be brand ambassador TikTok Shop conteudo` (mesma doutrina da entrada `recrutar afiliados com trafego pago apply to be brand ambassador` em `affiliate-creator-channels` — puxou uma, reuse)
- **Custom Link + atribuição de afiliado** _(dormant até esta skill)_ — `custom link de afiliado atribuicao de venda por creator`
- **Social Snowball (programa de afiliados automatizado)** _(dormant até esta skill)_ — `Social Snowball programa de afiliados automatizado comissao por cliente`
- **Ad Bounty Model + menu de sourcing de conteúdo** — `ad bounties editores performance-based Gridbank Insense Arcads film yourself B-roll sourcing`
- Onboarding do embaixador — `onboarding de brand ambassador deck contrato kickoff report mensal transparencia de numeros`

**ETAPA 1 roda sempre. ETAPAs 2-7 são da Fase A. ETAPAs 8-14 são da Fase B** e são puladas silenciosamente quando o gate de breakthrough não abriu — sem seção vazia no relatório (rule `report-only-results.md`). ETAPA 15 roda sempre.
