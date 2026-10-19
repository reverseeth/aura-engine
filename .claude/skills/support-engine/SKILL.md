---
name: support-engine
description: Suporte ao cliente da loja Shopify, pronto antes do primeiro ad. Explica ao membro o que a Brandwise faz (helpdesk de IA pra marcas DTC, ligado à Shopify, que responde e resolve sozinho rastreio, troca de endereço, reembolso, devolução e cancelamento, e junta email, chat, comentários e DMs numa caixa só), mostra o passo a passo pra configurar e entrega a base de conhecimento em inglês, montada com o que a Aura já sabe do produto, pronta pra colar. É consulta lateral, roda junto do checkout e da retenção, antes do launch. Use quando o membro disser "suporte", "atendimento", "customer support", "SAC", "brandwise", "helpdesk", "responder cliente", "reembolso", "comentários dos ads", "DM".
---

# Support Engine · Lateral <!-- gen:title -->

## Quando usar

Antes do primeiro ad, junto da `checkout-aov` e da `retention-engine`. Quando o tráfego pago liga, as perguntas chegam no mesmo dia: "where is my order?", "can I change my address?", "how do I cancel?". Pergunta sem resposta vira chargeback, review de uma estrela e comentário negativo embaixo do anúncio. A skill explica a ferramenta, mostra como ligar e entrega o texto que a IA de suporte precisa pra responder certo.

Volta a rodar quando a oferta muda (garantia, bônus, prazo de envio), pra atualizar a base. Material de apoio em `reference/`; abra só o arquivo da etapa atual.

## Pré-flight

1. `workspace/[produto]/manifest.json` existe. Sem ele, escape ES1: ofereça rodar a `setup` inline.
2. `offer-builder/dados.json` (garantia, bônus, `fulfillment_model`, `delivery_days_estimate`) e o FAQ da `copy-engine/copy-engine.md`. Faltando a oferta, siga com política de 30 dias e registre em `pending_inputs[]`.
3. `report_language` do profile (default `pt-BR`) na explicação; a base de conhecimento sai em inglês US (ou na língua do público).

## Fluxo da skill

### ETAPA 1 · O que a Brandwise faz e como ligar

Leia `reference/brandwise-setup.md`. Explique em linguagem simples o que a ferramenta resolve e como ela se liga à Shopify, e entregue o passo a passo da conta e das conexões. Se o membro já usa outro helpdesk (Gorgias, Zendesk, Richpanel), não force a troca: a base da ETAPA 2 serve igual.

### ETAPA 2 · Base de conhecimento pronta pra colar

Leia `reference/base-de-conhecimento.md`. Monte, a partir do workspace, os textos em inglês que a IA da Brandwise usa pra responder: produto, envio, garantia e reembolso, trocas, pedidos, assinatura e bônus quando existem, FAQ e tom da marca.

## SALVAR e mensagem final

Leia `reference/salvar-e-mensagem-final.md`. Em `workspace/[produto]/support-engine/`: `support-engine.md`, o `.html` por `python3 tools/render_report.py`, `dados.json` e a pasta `base-de-conhecimento/`. Depois `python3 tools/manifest.py <slug> complete support-engine` e `python3 .claude/lib/workspace-index/build_index.py <slug>`.
