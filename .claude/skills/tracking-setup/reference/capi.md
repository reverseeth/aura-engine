# Tracking Setup · Referência: Conversions API pelo Wetracked (ETAPA 2)

> O lado servidor do Wetracked, o Advanced Matching com dado first-party, a confirmação no Dataset, os dois sistemas a puxar (engaged lead e os três tipos de tráfego), a dedup por event_id e a regra da fonte server-side única. Abra na ETAPA 2.

### ETAPA 2 — Conversions API (CAPI) pelo Wetracked

CAPI envia os mesmos eventos pelo servidor (server-side), redundante ao navegador, deduplicados por `event_id`. É o que mantém o tracking vivo com iOS, ad-blockers e perda de cookie. No Wetracked, o servidor lê os pedidos direto do backend da Shopify (a loja é a fonte da verdade, não o navegador) e manda pra Meta.

1. **No Wetracked**, confirme a Conversions API ativa pro Dataset da ETAPA 1 (o onboarding liga por padrão).
2. **Advanced Matching**: o Wetracked enriquece cada evento com dado first-party do pedido e do cliente (email, telefone, nome, endereço, hasheados em SHA-256). É o maior motor do EMQ. Confirme que o checkout passa o dado do cliente (pedido-teste da ETAPA 3 mostra).
3. **Events Manager > [seu Dataset] > Overview**: cada evento do funil aparece como **Browser + Server**, e a fonte server-side listada é uma só (o Wetracked). Só Browser = servidor desligado; duas fontes server-side = duplicação.

**Puxe antes de fechar esta etapa (o sinal além do Purchase):**

- **Engaged Lead / sinal digital de qualificação** (rode `engaged lead evento de conversão customizado otimizar para o sinal de qualificação offline events`) — se a loja captura email ou lead on-site (popup, quiz), crie o **evento de conversão customizado do lead ENGAJADO** (não do lead bruto) e deixe-o disponível no dataset: é o sinal de qualificação pelo qual um ad set pode otimizar quando não há volume de Purchase, com offline events como reforço. Loja pré-launch no caminho `pending_traffic` é exatamente o cenário em que esse sinal intermediário mais vale.
- **Three Types of Traffic (Own / Control / Don't Control)** (rode `traffic you own traffic you control traffic you dont control brunson`) — o email capturado on-site é **tráfego que você POSSUI**: além de ser, com o Click ID, o parâmetro de match número 1 do EMQ, é o identificador que continua seu quando iOS e ad-blockers degradam o pixel. Por isso a captura de email é tratada como parte do tracking, não só de retention; a arquitetura dos flows que usam essa lista é da Skill `retention-engine`.

> **Dedup (event_id):** cada evento precisa do MESMO `event_id` no navegador e no servidor pra Meta não contar duas vezes. O Wetracked faz o pareamento. Purchase contado em dobro no Events Manager = sobrou outra fonte ligada (data sharing do app Facebook & Instagram, app de pixel, snippet no tema ou CAPI de 1 clique): voltar à ETAPA 1, desligar a fonte extra e re-verificar a contagem.
