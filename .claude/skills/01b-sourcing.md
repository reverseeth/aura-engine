---
name: sourcing
description: Fornecedor, cotação e logística do produto físico. Use quando o membro disser "sourcing", "fornecedor", "supplier", "cotação", "Alibaba", "3PL", "frete da China", ou quando um produto escolhido precisar de custo real antes da oferta. Explica a operação em linguagem simples (MOQ, OEM, DDP, 3PL...), analisa anúncios/fornecedores, monta a mensagem de cotação, aciona os agentes parceiros da Aura, compara cotações e entrega o custo real pro COGS da Skill 04.
---

# Sourcing Engine

## Quando Usar

Depois que o produto foi escolhido (Skill 01) e antes da oferta ter custo real (Skill 04). É uma fase **opcional e paralela**: pode rodar ao mesmo tempo que as Skills 02/03 (a pesquisa não depende do fornecedor). Membro com fornecedor privado ou operação dropship usa as partes que servem (cotação, logística, comparação) e pula o resto.

O objetivo de saída: **fornecedor escolhido + custo por unidade real (produto + frete) + rota logística definida** — os três números que transformam o COGS estimado da Skill 04 em COGS de verdade.

## Antes de Começar

0. **Idioma do relatório (rule 0 — INVIOLÁVEL)**: leia `report_language` de `workspace/profile.md` (default `pt-BR`). Todo output interno e conversa com o membro usam esse idioma. A mensagem de cotação pro fornecedor é em **inglês** (é comunicação comercial externa, não copy de consumidor).
1. Leia `workspace/profile.md` — em especial a seção de sourcing (fornecedor privado? preferência de SKU simples? budget).
2. Leia `workspace/[produto]/manifest.json` e o output da Skill 01 (produto escolhido, formato, mecanismo pretendido) — a cotação precisa perguntar EXATAMENTE o que o posicionamento promete (dose, material, duração, especificação).

## Fluxo da Skill

### ETAPA 0 — Pré-flight

1. Se `workspace/profile.md` ou o `manifest.json` do produto não existirem, ofereça rodar o `setup` inline antes de seguir. Se houver mais de um manifest com `setup_complete: true` e o membro não nomeou o produto no pedido, liste os `product_name` e pergunte em 1 linha qual é o alvo.
2. Identifique o que o membro JÁ tem: links de anúncio (Alibaba/1688/AliExpress), fornecedor privado com contato, cotações antigas, nada. A skill entra no ponto certo — não repete o que está feito.
3. Se a Skill 04 já rodou com custo estimado, anote: o fechamento desta skill atualiza o `cogs_breakdown` de lá.

### ETAPA 1 — A Operação Explicada (linguagem simples, sempre incluir no relatório)

O membro não é comprador profissional. Antes de qualquer análise, o relatório explica os termos da operação como se fosse a primeira vez — ele relê quando precisar. Adapte os exemplos ao produto dele:

**Sobre o fornecedor:**
- **MOQ** — o pedido mínimo que a fábrica aceita. "MOQ 500" = ela só produz a partir de 500 unidades.
- **OEM** — a fábrica produz a fórmula/produto DELA com a SUA marca na embalagem. O caminho mais comum pra começar.
- **ODM** — a fábrica desenvolve um produto NOVO ou ajustado pra você (sua fórmula, sua especificação). Mais caro, MOQ maior, mais controle.
- **Private label / white label** — nomes comerciais pro mesmo conceito do OEM: produto pronto de fábrica, rótulo seu.
- **Fabricante vs trading company** — fabricante é a fábrica de verdade (preço melhor, controle de qualidade direto); trading company é um intermediário que revende de várias fábricas (mais variedade, menos controle, margem dele embutida). No Alibaba, o selo "Manufacturer" e a idade da empresa ajudam a distinguir.
- **Spec sheet** — a ficha técnica: cada ingrediente/material COM quantidade, dimensões, peso. Sem spec sheet completa, não há pedido.
- **CoA** — certificado de análise: o laudo de laboratório de cada lote provando que o que está no rótulo está no produto. É o documento que sustenta claims na página.
- **GMP** — certificação de boas práticas de fabricação. O mínimo aceitável pra qualquer coisa que encosta no corpo (suplemento, cosmético, tópico).
- **Lead time** — o prazo entre aprovar a arte e ter o produto pronto pra embarcar.
- **Sample** — a amostra. Custa pouco (US$ 5-30 + frete) e evita comprar volume de um produto que você nunca tocou.
- **COGS** — o custo total pra ter 1 unidade pronta pra vender: produto + frete + impostos de importação, tudo somado. É o número que define quanta margem sobra pra pagar anúncio — e é o que esta fase existe pra fechar.

**Sobre o frete internacional (os 3 regimes que importam):**
- **EXW / FOB** — você assume o frete (e a dor de cabeça) desde a fábrica ou desde o porto. Só faz sentido com um agente cuidando.
- **DDU / DAP** — o fornecedor entrega no destino, mas os impostos de importação chegam DEPOIS, na surpresa, pro destinatário pagar.
- **DDP** — porta a porta com impostos inclusos: o fornecedor cota um preço único que já cobre frete + alfândega + entrega no endereço final. **É o regime recomendado pra quem está começando** — o custo real fica visível na cotação, sem surpresa.

**Sobre quem guarda e envia o produto (as 4 rotas):**

| Rota | O que é | Prós | Contras |
|---|---|---|---|
| **Dropship direto** | O fornecedor envia da China pro cliente final, pedido a pedido | Zero estoque, zero risco de capital | Entrega de 1-3 semanas mata review e recompra; sem controle de unboxing |
| **3PL** | Um armazém terceirizado no país de venda recebe seu estoque e envia cada pedido por você (ex. nos EUA: ShipBob, ShipMonk) | Entrega rápida local, unboxing seu, você nunca toca no produto | Custo por pedido (pick & pack) + mensalidade de armazenagem |
| **FBA (Amazon)** | O 3PL da Amazon — obrigatório pra vender com Prime | Logística resolvida dentro da Amazon | Taxas maiores, regras rígidas, faz sentido só se o canal Amazon importa |
| **Estoque em casa** | Você mesmo recebe e envia | Custo mínimo, controle total | Vira seu trabalho diário; não escala |

**O caminho recomendado pra loja própria vendendo nos EUA: comprar da China SEM "mandar da China"** — pedir envio **DDP direto pro 3PL americano**. O produto sai da fábrica e entra no armazém; o cliente recebe em 2-5 dias com a sua embalagem; o membro nunca toca uma caixa.

### ETAPA 2 — Analisar Fornecedores/Anúncios

Pra cada candidato (link do membro, busca no Alibaba, fornecedor privado), leia como analista:

- **Confiança**: anos de operação, nota e VOLUME de reviews da loja, taxa de recompra de clientes (%), selo de fabricante, mercado principal (exportar pro país de venda é sinal forte).
- **Encaixe com o posicionamento**: o produto do anúncio entrega o que o NOSSO mecanismo promete? (formato, duração, material, dose). Anúncio bonito com produto que contradiz o mecanismo = descarte, não adaptação.
- **Custo real por unidade**: preço do anúncio ÷ unidades por caixa/pacote, nas faixas de quantidade. Anúncios escondem o "por unidade" de propósito.
- **O que o anúncio NUNCA responde** (vira pergunta da cotação): especificação com quantidades, dados de qualidade, material de contato com a pele/corpo, laudo por lote.

Classifique cada candidato: **começar** (MOQ baixo, resposta rápida, frete simples) vs **escalar** (fabricante real, OEM/ODM, preço que despenca no volume) vs **descartar** (com o motivo).

### ETAPA 3 — Mensagem de Cotação (inglês, pronta pra enviar)

Monte UMA mensagem com os 7 blocos abaixo, adaptada ao produto (a mesma pra todos os canais — Alibaba chat, fornecedor privado, agente). Cotação boa é a que força o fornecedor a responder o que o anúncio esconde:

1. **SPEC SHEET** — lista completa de ingredientes/materiais COM quantidades por unidade. Se o posicionamento depende de um número (dose, gramatura, potência), pergunte EXPLICITAMENTE se há versões diferentes em estoque e o custo de ajustar só esse número.
2. **PERFORMANCE** — o dado que sustenta a promessa central (duração, liberação, resistência, capacidade — o que o mecanismo do produto promete).
3. **MATERIAL DE CONTATO** — do que é feito o que encosta no cliente (adesivo, tecido, plástico): segurança, resíduo, reclamações de irritação.
4. **COUNT & PACKAGING** — unidades por embalagem no padrão de fábrica; capacidade de produzir a SUA embalagem impressa (private label); preço unitário em 3-4 degraus de quantidade.
5. **COMPLIANCE** — exporta regularmente pro país de venda? GMP, CoA por lote, orientação de rótulo conforme a regulação local, validade (shelf life).
6. **SAMPLES & LEAD TIME** — custo e prazo da amostra; prazo de produção após aprovar a arte.
7. **SHIPPING** — cotação **DDP** até o endereço do 3PL, em 2 quantidades (ex: 500 e 1.000 unidades): custo e prazo de trânsito.

Feche com pressão saudável: "We're comparing suppliers and will order from whoever answers these points clearly."

### ETAPA 4 — Agentes de Sourcing Parceiros da Aura

Quando o membro precisa de mais do que um anúncio do Alibaba — produto custom, negociação de preço, inspeção de fábrica, consolidação de mais de um fornecedor num embarque só — a Aura tem agentes de sourcing parceiros na China. Contato direto por WhatsApp, conversa em inglês:

| Agente | WhatsApp |
|---|---|
| Yohn Ding | +86 185 5268 5200 |
| Josie | +86 193 2642 1242 |
| Brain Lee | +86 178 3718 2265 |
| Mark | +86 193 9607 4873 |

**Quando o agente vale a pena:** (a) o produto exige customização que anúncio de estoque não cobre; (b) o volume justifica negociar direto com fábrica; (c) o membro quer inspeção antes do embarque (agente visita a fábrica e confere o lote); (d) vários itens de fornecedores diferentes num contêiner só. **Como abordar:** mandar a mesma mensagem de cotação da ETAPA 3 + 1 parágrafo de contexto (produto, mercado de venda, volume inicial pretendido). O agente cobra comissão sobre o pedido ou taxa por serviço — perguntar o modelo na primeira conversa.

### ETAPA 5 — Comparar Cotações e Decidir

Quando as respostas voltarem, monte a tabela comparativa (uma linha por fornecedor):

| Fornecedor | Custo/un | MOQ | DDP até o 3PL | Lead time | Spec confirmada | Compliance (GMP/CoA) | Papel |
|---|---|---|---|---|---|---|---|

- **Fornecedor de COMEÇO** ≠ **fornecedor de ESCALA** — e está tudo bem ter os dois. Começo: MOQ mínimo, frete simples, entrega rápida (validar com dinheiro pequeno). Escala: fabricante real, preço que cai no volume, OEM completo (migrar depois que o produto vende).
- **Antes de qualquer pedido de volume: amostras.** Peça de 2-3 finalistas e TESTE pessoalmente no uso real do produto. Produto que falha no seu próprio teste falharia no cliente com review pública.
- Checagem de sanidade da margem: custo landed (produto + DDP rateado) ÷ preço de venda pretendido — abaixo de ~30% do preço de venda é confortável pra tráfego pago; acima disso, renegociar ou repensar preço (a régua fina é da Skill 04).

### ETAPA 6 — Contrato com a Skill 04 (COGS real)

Ao fechar a cotação, grave os números e avise o membro pra atualizar a oferta:

- Se `04-offer-builder/dados.json` já existe com `cogs_estimated: true` → atualize o `cogs_breakdown` com os custos reais, recalcule unit economics/AOV/PSM e regrave (a Skill 04 define as fórmulas; os inputs vêm daqui).
- Se a Skill 04 ainda não rodou → ela lê `sourcing/dados.json` no pré-flight e nasce com COGS real (sem estimativa).

## SALVAR (dual output — rule 6b do CLAUDE.md)

**Antes de qualquer write**: `mkdir -p workspace/[produto]/sourcing/`.

1. **`workspace/[produto]/sourcing/sourcing.md`** — relatório no report_language: a operação explicada (ETAPA 1), análise dos candidatos, mensagem de cotação pronta, agentes (se recomendados pro caso), tabela comparativa (quando houver cotações), decisão e próximos passos. Segue `.claude/rules/report-only-results.md`.
2. **`workspace/[produto]/sourcing/sourcing.html`** — companion no template `.claude/templates/aura-report-template.html` (logo SVG, componentes aura).
3. **`workspace/[produto]/sourcing/dados.json`**:

```json
{
  "product_slug": "",
  "status": "quoting|samples|closed",
  "suppliers": [
    { "name": "", "channel": "alibaba|1688|private|us_manufacturer|agent", "contact": "", "unit_cost": 0, "moq": 0, "ddp_to_3pl": 0, "lead_time_days": 0, "spec_confirmed": false, "compliance": { "gmp": false, "coa_per_batch": false }, "role": "start|scale|discarded", "notes": "" }
  ],
  "chosen_supplier": "",
  "logistics_route": "ddp_to_3pl|dropship_direct|fba|home",
  "three_pl": { "provider": "", "pick_pack_per_order": 0, "storage_monthly": 0 },
  "landed_cost_per_unit": 0,
  "quote_message_sent_at": "",
  "pending_from_supplier": []
}
```

**Atualize o `manifest.json`**: `skills_completed` ← `"01b-sourcing"` (quando `status: "closed"`), `updated_at`, e regenere o painel (`python3 .claude/lib/workspace-index/build_index.py <slug>`).

## Mensagem Final

(Adaptar ao ponto em que a skill parou — cotação enviada vs fechada:)

"Sourcing estruturado: [N] fornecedores analisados, mensagem de cotação pronta [+ agentes parceiros recomendados, se for o caso]. Enquanto as respostas não chegam, dá pra avançar com market research / competitor analysis — a pesquisa não depende do fornecedor. Quando os preços chegarem, me passa que eu comparo, fecho a recomendação e atualizo o custo real na oferta."
