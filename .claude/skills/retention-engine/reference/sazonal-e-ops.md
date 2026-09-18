# Retention Engine · Referência: Sazonal (handoff com a promo-engine) e OPS pós-launch (ETAPA 5)

> A divisão entre flows e campanhas sazonais, o Desire Calendar, os sistemas dos assets sazonais, o checklist do abandoned cart na promo e as três rotinas de ops (chargeback, refund da garantia, CS básico). Abra na ETAPA 5.

## Sazonal (Fase B) — handoff

Dois donos, ninguém órfão: a `retention-engine` executa os **FLOWS** (sempre-ligados, disparados por evento) e a adaptação sazonal deles; as **CAMPANHAS** sazonais (Q4, Black Friday/Cyber Monday, promos datadas — sends agendados pra lista) são orquestradas pela skill **promo-engine**, que chama a `retention-engine` pra gerar os assets de email de cada send. Na prática: pedido de "campanha de email" / "Black Friday" / "promo" → a `promo-engine` é a dona do calendário, da mecânica da promo e dos segmentos; a `retention-engine` entrega os emails e mantém os flows coerentes com a promo no ar (flow NUNCA desliga durante campanha — se adapta). A copy dos emails sazonais permanece **inglês US** (regra de rigor 2); o handoff e o relatório seguem o `report_language`.

**Timing — quando religar/adaptar mensagens por época:**
- **Desire Calendar** — decide QUANDO adaptar a mensagem dos flows por época: como os 6 desejos flutuam mês a mês, Fresh Start Effect (janeiro e setembro) e Early Shopping Migration (antecipar a mensagem em 4-6 semanas) (rode `calendario sazonal de desejos health sex status belonging control comfort por mes`)

**Sistemas dos assets sazonais (puxar quando a `promo-engine` chamar — ou quando o membro pedir a campanha direto):**
- **Playbook Q4 de Email & SMS** — targeting pyramid (engaged 30 / engaged 90 / dormant 120), email tolera volume e SMS é cirúrgico, quiet hours (rode `email tolera volume SMS é cirúrgico, engaged 30 engaged 90 dormant 120, quiet hours texas`)
- **Campanha de 4 Dias e os 6 templates** — a estrutura de promo curta, incluindo o dia de slump e o template da inveja (rode `campanha sazonal de 4 dias com 6 templates, dia de slump, template da inveja`)
- **Sequências promocionais formulaicas (Holiday 3 / Black Friday 6 / Flash Sale 24h 3)** — os esqueletos por tipo de sale: razão pra sale, stock-up recommendation, sale de 24h "não planejada" (rode `razão para a sale, stock up recommendation, sale de 24 horas não planejada`)

**O lado dos FLOWS durante a campanha (trabalho da `retention-engine`, sem esperar a `promo-engine`):**
- **Seasonal Abandoned-Cart SMS Update Checklist** — atualizar o abandoned cart durante a janela da promo: detalhes da oferta, hora exata de fechamento, urgência/escassez reais e sem "rain check" (rode `seasonal abandoned cart SMS update checklist offer details campaign close time urgency scarcity no rain check`)

## OPS pós-launch (Fase B — seção compacta, junto dos flows de retenção)

Retenção não é só email: com pedidos rodando, três rotinas operacionais protegem a conta de pagamento e a margem. Entregar como checklist curto no relatório da Fase B (não é skill separada — é higiene):

**1. Chargeback (alvo: taxa < 1% dos pedidos):**
- **Responder TODA disputa com evidência** — tracking com entrega confirmada, screenshot da PDP com a promessa exata, log do email de confirmação, histórico de contato. Disputa não-respondida é derrota automática.
- **Refund proativo > disputa perdida:** cliente irritado ameaçando chargeback → reembolsar ANTES da disputa abrir. Chargeback custa a taxa + o produto + o strike na conta; refund custa só o pedido. Acima de ~1% de taxa, o processador aplica reserve/hold — exatamente o cenário que trava a escala (ver Skill `scale-engine`, ETAPA 6).
- Sinais que previnem: descriptor de cartão reconhecível (nome da marca, não LLC genérica), email de confirmação imediato, tracking enviado assim que existe.

**2. Refund da garantia (macro de processo — a promessa da `offer-builder` sendo honrada):**
- A garantia definida na `offer-builder` e prometida na página é operação, não copy: definir o passo-a-passo UMA vez (macro) — pedido chega → conferir elegibilidade (janela/condição da garantia) → reembolsar sem fricção → registrar o motivo.
- Refund da garantia SEM interrogatório: garantia "sem perguntas" que na prática exige 5 emails vira chargeback + review negativa. O motivo registrado alimenta a iteração da oferta na `offer-builder` (padrão de motivo = sinal de produto/promessa desalinhados).
- Se a garantia é Level-2 (keep-the-premium, da `bonus-delivery`/`offer-builder`): o cliente fica com o bônus — a macro lembra de NÃO pedir devolução dele.

**3. CS básico (o mínimo que segura a nota):**
- Caixa de suporte monitorada (o reply-to dos flows aponta pra ela) com resposta em < 24h úteis — atraso de resposta é o maior gerador de disputa "item not received".
- 5 macros prontas: onde está meu pedido (tracking + prazo), quero reembolso (macro da garantia acima), produto chegou danificado (reenvio direto, foto opcional), como usar (link do how-to do post-purchase), cancelar assinatura (se houver — sem fricção, com oferta de pausa).
- Comentários dos ads NÃO são CS — são gestão de comentários (rotina da Skill `ad-strategy` ETAPA 2), mas reclamação real que aparece lá entra no funil de CS.
