# Scale Engine · Referência: Scaling Protocol, a espinha única de toda subida e descida (ETAPA 3.5)

> A regra de reset da meia-noite, o ad-log verificado antes e registrado no ato, os dois gates de subida e o passo de +20%, as duas exceções do cânone, o teto de escala medido pela `finance-engine`, a descida de −20% e os sete passos de quando a escala estagna (a ação fora do ad account, incluindo o Chunk Up). Abra na ETAPA 3.5.

### ETAPA 3.5 — Scaling Protocol (a espinha única de toda subida e descida)

Antes de escolher escola, fixe a régua. **Toda mudança de budget desta skill obedece ao Scaling Protocol do cânone `.claude/lib/ad-taxonomy/README.md` §5.** As escolas da ETAPA 4 são variantes de **intensidade** dentro dele — mudam o quanto e com que mão o membro empurra, nunca os gates. Onde uma escola sugerir ritmo que conflita com o protocolo, **o protocolo vence**.

Sistemas a carregar antes de montar o plano: `scaling protocol 48-72 hours above target KPI scale every 24 hours decision tree new reason promo`, `reset da meia-noite metade do spend real nunca budget nominal explode a conta` e `the fix is outside the ad account pesquisa avatares mecanismos ofertas novas plateau`.

> ⚠️ **REGRA DE RESET DA MEIA-NOITE (crítica — risco financeiro real)**
>
> **Ao ajustar o budget à meia-noite, o novo valor é ~50% do que a campanha REALMENTE GASTOU no dia — nunca 50% do budget nominal que ficou setado na tela.** (cânone `ad-taxonomy` §5.)
>
> Um budget setado em $1.600 que gastou $300 vira **~$150** no dia seguinte, não $1.600. Sem isso, o Meta faz *pacing* pra gastar o nominal inteiro no dia seguinte: o membro dorme com um teste de $300 e acorda com $1.600 queimados sem ninguém olhando.
>
> **Vale para TODA escola e TODO salto de budget desta skill** — o surf da A, a alimentação da B, o doubling da C. Sempre que a skill instruir uma subida, ela instrui **junto** o valor de reset do dia seguinte. Grave em `dados.json.midnight_reset`.
>
> A meia-noite que conta é a do **fuso do AD ACCOUNT**, não a do membro — confirme o fuso na ETAPA 1 antes de dar horário.
>
> Em janela promocional com data-fim, quem governa o comportamento do budget é a exceção (a) do cânone §5 e a skill `promo-engine`, dona da janela — e o reset da meia-noite segue existindo lá, sobre o gasto real da promo.

**Ad log — verificar antes, registrar no ato (cânone `.claude/lib/ad-log/README.md`):**

- **Antes de qualquer degrau, leia `workspace/[produto]/ad-log.md`:** qual foi a última mudança de budget e há quanto tempo — **o gate de 24h entre degraus é verificado ali, não de memória.** Mudança recente cujo efeito ainda não foi lido é motivo pra segurar o passo mesmo com gates verdes.
- **Toda mudança de budget que esta skill instrui ou executa** — degrau de ±20%, reset da meia-noite, surf e o recuo do surf, duplicação em ABO, graduação pra ASC — **é registrada no MESMO momento da execução** (nunca "depois"), uma linha por mudança no formato do cânone: `| YYYY-MM-DD HH:MM | entidade | mudança | executor | motivo curto |`, com valores antes → depois ("budget $200→$240") e executor `skill-scale-engine` (ou `membro`, quando ele relata mudança manual). Arquivo inexistente → criar com o cabeçalho da tabela na primeira escrita. **Mudança executada e não logada é bug de processo.**

**Subida (os dois gates são cumulativos — falhou um, o passo é zero):**

1. **Gate de consistência:** a campanha precisa estar **48-72h acima do target** antes do primeiro aumento. Um dia bom não abre escala.
2. **Gate click-based (duas portas — qualquer uma libera, cânone §5):** só sobe se **≥ 60% das purchases aparecem em 7-day click** OU se **o ROAS calculado só com purchases click-based já bate o KPI sozinho**. Sinal majoritariamente view-through que não passa em nenhuma das duas não sustenta escala. (Share: `manifest.click_based_purchase_share`, gravado pela `ad-analysis`; sem o campo, o número da ETAPA 1.)
3. **Passo: +20%.** Passado o primeiro aumento, pode repetir **a cada 24h** enquanto os dois gates seguirem verdadeiros — e as 24h desde o degrau anterior se conferem no `ad-log.md`, não de memória.
4. Sem os 48-72h, ou com o gate click-based vermelho nas duas portas, não existe atalho por entusiasmo: **o passo é zero** e a ação vai pro item 7 — salvo as **duas exceções do cânone** logo abaixo.

**As DUAS exceções do protocolo (cânone §5 — são da fonte e valem sobre os degraus; nenhuma outra existe):**

- **(a) Promo com data-fim** (BFCM, lançamento, liquidação com prazo): entra **direto no budget planejado da promo** — não sobe em degraus de +20%, porque a janela termina antes de os degraus chegarem lá. O que protege a promo é o **surf + reset da meia-noite** (presença ativa no dia; à meia-noite, ~50% do gasto REAL), não o protocolo. Terminada a promo, o budget volta ao trilho dos degraus.
- **(b) "New reason to be scaling"** — oferta nova, breakthrough novo, sazonalidade que mudou a demanda: **reinicia a leitura do protocolo.** O histórico anterior de degraus não trava o passo novo — os 48-72h acima do target contam a partir do motivo novo, não do degrau velho.

Exceção usada → registre em `dados.json.scaling_protocol.active_exception` e no `ad-log.md` (motivo curto = a exceção, ex: "promo início" / "new reason: oferta nova").

> **Teto de escala medido (quando `finance-engine/dados.json` existir):** a `finance-engine` projeta o resultado operacional em faixas crescentes de spend e publica `payback.scale_ceiling_monthly_spend` — o ponto em que o resultado **para de subir e começa a cair**. Enquanto os passos de +20% acumulados estiverem abaixo desse teto, o protocolo roda normal; ao chegar perto dele, o passo é zero **mesmo com os dois gates verdes**, e a ação vai pro item 7 (fora do ad account). Escreva o teto de forma acionável no relatório: *"não passar de US$ X/mês de spend até o CAC melhorar"*. **Sem o arquivo da `finance-engine`, nada muda:** o teto continua sendo descoberto empiricamente — a escola sobe até quebrar o CPA e recua pro último nível bom.

**Descida:**

5. **Abaixo do breakeven por 24-48h persistentes → −20%** (cânone §5 — **um dia ruim isolado não dispara descida**; a leitura é da janela, não do susto do dia). Cortar, não desligar: matar o top spender reseta o aprendizado (Spend Redistribution Framework, ETAPA 10).
6. **Antes de qualquer corte motivado por queda de ROAS que ainda paga o variável**, roda o gate de custo fixo (ver "Custo fixo antes de cortar spend", unit-economics §4). Fixos desconhecidos → a saída é pergunta, não instrução de corte.

**Quando estagna (o passo que impede o membro de girar botão à toa):**

7. Se o budget não sobe mais sem quebrar o CPA, **a ação certa está FORA do ad account**. Nessa ordem:
   - **Batch novo de criativo** (skill `creative-engine`) — é o gargalo na maioria esmagadora dos platôs;
   - **Funil inteiro conferido por bug** — código de carrinho removido, produto fora de estoque, checkout quebrado, pixel caído. Checar **diariamente** depois de qualquer queda brusca, antes de culpar o leilão;
   - **Oferta re-testada** (skill `offer-builder`) e **página re-trabalhada** (`page-design`/`page-build`);
   - **Learnings processados** — o que os breakthroughs atuais têm em comum e o que ainda não foi testado;
   - **Sub-avatar esgotado → Chunk Up** (rode `plateau chunk up desejo central amplo calendario de desejos nichar acha broad escala`) — quando o platô é de mercado (o ângulo nichado do sub-avatar já foi "snipado" e não rende mais), a saída é **subir UM nível de abstração**: falar ao desejo central mais amplo por trás do sub-avatar e deixar o broad achar o público. Nichar de novo só quando o patamar novo platôar por sua vez. O briefing do nível novo vai pra `creative-engine` via `scale-directives.md`.

   Mexer em bidding, budget e estrutura quando o gargalo é criativo ou oferta só troca a forma do prejuízo. Registre a estagnação em `dados.json.scaling_protocol` e roteie explicitamente (ver "Quando a `scale-engine` recomenda voltar para a `creative-engine`").
