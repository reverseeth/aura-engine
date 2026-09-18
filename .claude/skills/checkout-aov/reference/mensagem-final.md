# Checkout & AOV · Referência: Mensagem final e self-audit silencioso

> O texto integral da mensagem final como draft, com os próximos passos e a Fase B, e os itens do self-audit silencioso. Abra ao encerrar.

## Mensagem Final

Primeira versão como **draft**, não "pronto" (iteration-driven-refinement):

"Primeira versão do stack de checkout/AOV pronta. Implementei [N] alavancas: [lista curta — ex: bundle 3-tier na PDP, cart bump $17, free-shipping bar em $75, trust row].

Sem as alavancas, o pedido médio ficaria em **$X**; com o stack aplicado, a projeção da oferta é **$Y** de AOV — este stack é o que faz esse número acontecer de verdade. [SE `scope_diff` não-vazio: 'Como implementamos [alavanca] além do planejado, o CPA máximo que você pode pagar subiu de $A pra $B — atualizei o número que a campanha vai usar. Esse teto é calculado pra 2× o ROAS de breakeven, ou seja, metade da margem de cada pedido vira lucro.']

Revisa o pricing e a copy e me diz o que ajustar: o threshold de free-shipping tá no ponto certo? O preço do upsell faz sentido? Itero até ficar redondo.

Próximo passo: se a oferta tem bônus, diga **'bonus delivery'** (Fase A: o asset do bônus precisa existir antes do primeiro ad); depois **'retention'** (Fase A: flows de recuperação, abandoned cart e post-purchase); só então **'creatives'** pra gerar os anúncios (já com o AOV/CPA correto). Se o pixel/CAPI ainda não foi configurado, **'tracking'** vem antes de tudo isso. E quando os pedidos estiverem rodando e a análise de ads já tiver leitura de funil, me chama de novo com **'checkout'**: a Fase B re-testa o backend em ciclos (upsell, downsell, bundle, threshold) usando o tráfego que você já pagou."

> **Self-audit silencioso (rule 9 + `.claude/rules/post-task-self-audit.md`):** antes de declarar pronto, confirmar inline e sem mostrar bloco: (1) NENHUMA alavanca foi re-somada sobre `aov_expected` (contagem dupla — a reconciliação da ETAPA 4 bate: caso normal `aov_final == aov_projected_04` e `scope_diff` vazio); (2) todo bump/upsell/bundle-mate/GWP tem `complementarity_category` de uma das 4 categorias (componente sem categoria = reprovado, não aplicado); (3) copy de checkout/cart em inglês US, com o mesmo threshold, garantia e números de review que a página e a oferta usam; (3b) superfícies de assinatura obedecem `subscription_architecture` + `onetime_premium_pct` da `offer-builder` (nenhum desconto de assinatura em upsell/OTO — o framing é o prêmio do one-time; arquitetura 2 = checkout sem push de assinatura; campos ausentes = fallback legado anotado); (4) caminho recomendado respeita o plano da loja (nada de extension in-checkout ou Function custom pra não-Plus) e nenhum app instalado roda sobre Shopify Scripts; (5) operações de tema usaram `--path` + o `theme_id` do `manifest.storefront` + marker `data-aura-build`; (6) `dados.json` + `checkout-aov.md` + `checkout-aov.html` (gerado pelo `render_report.py`) salvos e manifest atualizado (`skills_completed`, `aov_baseline` se aplicado, `target_cpa`/`breakeven_roas` SÓ se `scope_diff` não-vazio). Issue dentro do escopo → fix inline. Decisão do membro (ex: trocar produto do bump, aceitar take menor por loja wallet-heavy) → surface curto.
