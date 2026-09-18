# Tracking Setup · Referência: Ativar a Conversions API (ETAPA 2)

> O nível Maximum de data sharing, o Advanced Matching, a confirmação no Dataset, os dois sistemas a puxar (engaged lead e os três tipos de tráfego), a dedup por event_id e o aviso do CAPI de 1 clique. Abra na ETAPA 2.

### ETAPA 2 — Ativar a Conversions API (CAPI)

CAPI envia os mesmos eventos pelo servidor (server-side), redundante ao browser, deduplicados por `event_id`. É o que mantém o tracking vivo com iOS/ad-blockers/cookie loss.

1. **No app Facebook & Instagram (dentro do Shopify admin) > Settings > Data sharing** — selecionar o nível **Maximum**. É essa escolha que ativa a Conversions API server-side + Advanced Matching (Standard = só pixel browser; Enhanced = + advanced matching; **Maximum = + CAPI**). O toggle de CAPI NÃO fica em "Customer events" — Customer events é a área de custom pixels, use-a só pra verificar duplicidade.
2. **Advanced Matching** ON (vem com o nível Maximum) — envia email/telefone/nome hasheados (SHA-256) com cada evento. É o maior driver de EMQ. Confirmar que o checkout está passando customer data pro CAPI.
3. **Events Manager > [seu Dataset] > Settings** — confirmar **"Conversions API"** ativa e a fonte (Partner Integration: Shopify) listada.

**Puxe antes de fechar esta etapa (o sinal além do Purchase):**

- **Engaged Lead / sinal digital de qualificação** (rode `engaged lead evento de conversão customizado otimizar para o sinal de qualificação offline events`) — se a loja captura email/lead on-site (popup, quiz), crie o **evento de conversão customizado do lead ENGAJADO** (não do lead bruto) e deixe-o disponível no dataset: é o sinal de qualificação pelo qual um ad set pode otimizar quando não há volume de Purchase, com offline events como reforço. Loja pré-launch no caminho `pending_traffic` é exatamente o cenário em que esse sinal intermediário mais vale.
- **Three Types of Traffic (Own / Control / Don't Control)** (rode `traffic you own traffic you control traffic you dont control brunson`) — o email capturado on-site é **tráfego que você POSSUI**: além de ser, com o Click ID, o parâmetro de match nº 1 do EMQ, é o identificador que continua seu quando iOS e ad-blockers degradam o pixel (tráfego que você não controla). É por isso que a captura de email é tratada como parte do tracking, não só de retention — a arquitetura dos flows que usam essa lista é da Skill `retention-engine`.

> **Dedup (event_id):** cada evento precisa do MESMO `event_id` no browser e no servidor pra Meta não contar duas vezes. A integração nativa faz isso. Se você vir Purchase contado em dobro no Events Manager, a dedup quebrou (geralmente pixel hardcoded + nativo coexistindo — voltar à ETAPA 1).

> **Aviso — CAPI de 1 clique da Meta (abr/2026):** o Events Manager oferece um botão "Activate Conversions API" que cria uma SEGUNDA fonte server-side. Se o membro clicou nele POR CIMA da integração nativa Shopify↔Meta, os Purchase chegam duplicados SEM `event_id` pareado (a dedup não casa fontes diferentes). Pergunte se ele ativou; se sim, desative uma das duas fontes server-side (manter a nativa do Shopify) e re-verifique a contagem no Events Manager.
