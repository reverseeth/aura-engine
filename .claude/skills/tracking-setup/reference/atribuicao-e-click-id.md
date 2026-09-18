# Tracking Setup · Referência: Janela de atribuição e preservação do Click ID (ETAPA 3B)

> Os três sistemas a puxar, a janela baseline com o Incremental Attribution desligado, o teste 7DC-only como diagnóstico da scale-engine e as três checagens de preservação do Click ID. Abra na ETAPA 3B.

### ETAPA 3B — Janela de atribuição + preservação do Click ID

A janela de atribuição define **o que o número do Ads Manager significa**; o Click ID define **quantas conversões conseguem ser atribuídas**. Fixar os dois aqui evita que a `ad-strategy` lance com leitura incomparável e que a `scale-engine` escale com sinal furado.

**Puxe antes desta etapa:**

- **Preservação de Click ID (cross-domain + express checkout)** (rode `click id perdido cross-domain express checkout Shop Pay restaurar 40% mais conversões`)
- **Teste de troca pra 7DC-only** (rode `campanha duplicada 7-day click only view-through inflado email blast returning customers`)
- **Slots de teste não-criativo (Hard Exclusions / 1-Day Click / Incremental Attribution)** (rode `ad sets de teste não-criativo hard exclusions 1-day click incremental attribution`)

1. **Baseline de janela: `7d-click/1d-view`** (7 dias pós-clique + 1 dia pós-visualização). É a janela em que a Skill `ad-strategy` cria o teste padrão e na qual as réguas de kill da Skill `ad-analysis` foram calibradas. Documente-a no relatório e **deixe o setting de Incremental Attribution DESLIGADO no launch** — ele muda o que o Meta conta como conversão, torna o CPA incomparável com o baseline e trava as attribution settings (a `ad-analysis` re-baseia todos os thresholds se o membro ligar).
2. **Teste 7DC-only é diagnóstico agendado, não default:** com histórico rodando, duplicar a campanha só com atribuição de **7-day click** mede quanto do resultado reportado vinha inflado por view-through, disparo de email e clientes recorrentes. Registre no relatório que esse teste existe e quando cabe — quem o executa é a **Skill `scale-engine`**, num slot de teste não-criativo (a mesma família dos testes de hard exclusions, janela 1-day click e atribuição incremental), nunca por cima da campanha que está pagando as contas.
3. **Preservar o Click ID de ponta a ponta:** o Click ID (com email, o parâmetro de match 1:1 de maior prioridade) se perde na navegação entre domínios e no express checkout tipo Shop Pay — e recuperá-lo restaura **até 40% mais conversões atribuídas**. Checar: **(a)** a jornada LP → PDP → checkout não troca de domínio raiz; **(b)** no Purchase mais recente do Events Manager (ou no pedido-teste da ETAPA 3), o evento chegou COM o parâmetro de click ID; **(c)** se o stage pedir stack pago na ETAPA 4, a captura server-side do click ID (Wetracked / Sonar do Triple Whale / Aimerce) é parte do valor que justifica o custo.
