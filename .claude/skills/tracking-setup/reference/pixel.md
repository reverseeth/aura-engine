# Tracking Setup · Referência: Meta Pixel pelo Wetracked (ETAPA 1)

> O Dataset certo no Business Manager, o app Facebook & Instagram da Shopify com o data sharing desligado (fica só pro catálogo), a instalação do Wetracked como fonte única do pixel, o porquê de nunca hardcodar o snippet no tema e os 5 eventos do funil a confirmar. Abra na ETAPA 1.

### ETAPA 1 — Pixel pelo Wetracked

O tracking da Aura é sempre o **Wetracked** (wetracked.io, app da Shopify App Store), em todos os stages. Ele dispara o pixel no navegador e manda os mesmos eventos pelo servidor (Conversions API Gateway) a partir do backend da Shopify, com o `event_id` pareado. A regra que governa tudo: **uma fonte só de eventos pra Meta, e essa fonte é o Wetracked.**

1. **Dataset no Business Manager.** Confirme (ou crie) o Pixel/Dataset no Events Manager, dentro do Business Manager e do ad account que a Skill `ad-strategy` vai usar. Mismatch aqui = eventos no dataset errado, campanha cega.
2. **App Facebook & Instagram da Shopify: data sharing DESLIGADO.** Shopify admin > Settings > Apps and sales channels > Facebook & Instagram > Settings > Share data > Change > desligar. O app pode continuar instalado pro catálogo e pra marcação de produtos no Instagram; só para de mandar eventos. Ligado junto com o Wetracked, cada evento chega duas vezes.
3. **Nenhuma outra fonte de pixel.** Em Settings > Customer events, remova custom pixels da Meta; desinstale apps de pixel ou CAPI (Omega, Elevar, Stape, Trackify, Upstackified e afins); nenhum snippet da Meta no `theme.liquid`; nenhum CAPI de 1 clique ativado pelo Events Manager.
4. **Instalar o Wetracked.** Shopify App Store > Wetracked > instalar, seguir o onboarding do app: conectar a conta Meta, escolher o mesmo Pixel/Dataset do passo 1, ativar os eventos do funil. Pixel ID no Wetracked = Pixel ID do ad account.

> **Por que não hardcodar no tema:** snippet manual no `theme.liquid` mais o Wetracked = evento duplicado sem `event_id` consistente, derrubando o EMQ e inflando a contagem de Purchase.

**Eventos do funil a confirmar** (Events Manager > Test Events, navegando a loja, e o painel do próprio Wetracked): `PageView`, `ViewContent` (PDP), `AddToCart`, `InitiateCheckout`, `Purchase`. Se algum falta, reabra o onboarding do Wetracked; se algum aparece em dobro, sobrou outra fonte do passo 2 ou 3 ligada.
