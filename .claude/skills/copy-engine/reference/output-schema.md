# Copy Engine · Referência: Output Schema, as seções canônicas do copy-engine.md

> Os nomes exatos e case-sensitive das seções H2 do relatório para PDP e landing page e para advertorial, com o mapeamento 1:1 das 7 seções do blueprint e as duas seções obrigatórias no fim de qualquer página. Abra ao montar o `copy-engine.md`.

## Output Schema — Seções Canônicas (`copy-engine/copy-engine.md`)

O markdown DEVE ter as seções NOMEADAS ASSIM (case-sensitive, H2). Cada seção contém texto pronto pra colar, SEM comentários de instrução no output final.

**PDP / Landing Page (ETAPA 4):**

```
## Hero
### Headlines (ranked)
### Subheadline
### CTA Primary
### CTA Secondary

## Mechanism
## Benefits
## Social Proof
## Offer Stack
## Guarantee
## FAQ
## Specs
## Urgency/Scarcity
## Email Follow-up Hooks
```

**ADVERTORIAL (ETAPA 5):** o corpo da página usa estas seções canônicas no LUGAR do bloco `## Hero`→`## FAQ` acima — EXATAMENTE estes nomes, case-sensitive (a `page-design` localiza o advertorial por eles):

```
## Advertorial Headline
## Lead
## Background Story
## Root Cause
## Mechanism Reveal
## Product Build-Up
## Reveal + Close

## Urgency/Scarcity
## Email Follow-up Hooks
```

As 7 seções mapeiam 1:1 pro blueprint da ETAPA 5 (Irresistible Headline → `## Advertorial Headline`; Root Cause Explanation → `## Root Cause`; Unique Mechanism Reveal → `## Mechanism Reveal`; Product Reveal + Close → `## Reveal + Close`). `## Urgency/Scarcity` e `## Email Follow-up Hooks` continuam obrigatórias no fim do relatório em qualquer tipo de página — a urgência do advertorial vive dentro de `## Reveal + Close` E é extraída pra seção canônica, como a ETAPA 5 já define.
