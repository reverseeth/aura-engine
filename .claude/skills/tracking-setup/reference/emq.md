# Tracking Setup · Referência: Validar o Event Match Quality, o gate técnico (ETAPA 3)

> A escala de 0 a 10, os caminhos de leitura (MCP e manual), a tabela de decisão do gate com o caminho pending_traffic e o pedido-teste, e o diagnóstico de EMQ baixo. Abra na ETAPA 3.

### ETAPA 3 — Validar o Event Match Quality: EMQ ≥ 6.0 (gate técnico)

Este é o **gate que destrava `creative-engine` e `ad-strategy`**. O Event Match Quality (EMQ) é um **escore de 0 a 10 por evento** no Events Manager (com faixas Poor/OK/Good/Great) — NÃO existe "match quality em %"; nunca peça porcentagem ao membro. O gate canônico do framework é **EMQ ≥ 6.0** no evento Purchase (é o que `manifest.tracking.tracking_ready` atesta e o que `creative-engine`/`ad-strategy` verificam) — **com uma exceção estrutural:** loja pré-launch sem tráfego não tem como ter escore (o EMQ só calcula com eventos reais); pra esse caso existe o caminho `pending_traffic` na tabela abaixo, que destrava o launch com instalação verificada + pedido-teste, sem esperar um número que só o próprio tráfego produz.

**Caminho 1/2 (MCP oficial/Pipeboard):** ler o EMQ do dataset via tool de insights de dataset. Capturar o escore numérico (0-10) do Purchase (e do AddToCart como secundário).

**Caminho 3 (manual):** pedir ao membro:
> "Abre o **Events Manager > seu Dataset > Overview**. Me manda print de: (1) a dupla-coluna Browser + Server nos eventos Purchase/AddToCart, e (2) o **Event Match Quality** do Purchase (o escore de 0 a 10 no card do evento). Quero ver **6.0 ou mais**."

**Decisão do gate:**

| EMQ (Purchase, escala 0-10) | Ação |
|---|---|
| **≥ 8.0** (Great) | PASS. `tracking_ready: true`. Seguir pra ETAPA 3B. |
| **6.0–7.9** (Good/OK) | PASS com recomendação. Tracking destravado, mas sub-ótimo: recomendar Advanced Matching completo (email + phone + nome + endereço no checkout) e re-medir em 24-48h (precisa de tráfego pra recalcular). `tracking_ready: true` com `emq_warn: true`. |
| **Sem dados por falta de tráfego** (loja pré-launch: Pixel + CAPI instalados corretamente E os 5 eventos do funil confirmados no Test Events, mas dataset sem volume pro escore calcular) | **PASS condicional (`pending_traffic`)** — não é falha de configuração, é ausência de tráfego: o EMQ só existe com eventos reais, e exigir escore antes do primeiro ad criaria um impasse (sem tracking_ready a `ad-strategy` não roda tráfego; sem tráfego o EMQ nunca calcula). Gravar `emq.status: "pending_traffic"`, `emq.score: null`, e no manifest `tracking_ready: true` + `emq_pending: true`. **Obrigatório antes de fechar:** validar o Purchase de ponta a ponta com um **pedido-teste real** — Bogus Gateway num tema de preview (sem cobrança) OU pedido real de ~$1 + refund — e confirmar o evento Purchase chegando com a dupla-coluna (Browser + Server) no Events Manager. A Skill `ad-analysis` re-lê o EMQ no dia 3 de tráfego; EMQ < 6.0 pós-tráfego = ação corretiva (voltar a esta skill). |
| **< 6.0 COM volume de eventos** | BLOCK. Pixel ou CAPI mal configurado (o escore existe e está baixo — é config, não falta de dados). **Escape (ES1):** ofereça **(A)** rodar o diagnóstico abaixo e re-medir, OU **(B)** prosseguir marcando `manifest.skipped_preflight += ["emq_gate"]` e avisando que `creative-engine`/`ad-strategy` vão herdar tracking fraco (`tracking_ready: false`, membro aceitou o risco). |

**Diagnóstico de EMQ baixo** (rodar antes de qualquer "prosseguir mesmo assim"):
- CAPI OFF ou sem Advanced Matching (Data sharing abaixo de Maximum) → ETAPAS 1-2.
- Data sharing em "Optimized" pausou o envio (loja sem tráfego) → ETAPA 1 passo 3 ("Always on").
- Sem volume: dataset novo precisa de ~algumas dezenas de eventos pra calcular o escore. Se a loja não teve tráfego ainda, o número pode estar vazio — não é erro, é falta de dados → caminho **`pending_traffic`** da tabela acima (exige o pedido-teste validando o Purchase).
- Pixel duplicado (hardcoded + nativo, ou CAPI 1-clique por cima da nativa) → dedup quebrada → ETAPAS 1-2.
