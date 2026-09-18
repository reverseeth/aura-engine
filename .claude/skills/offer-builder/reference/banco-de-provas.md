# Offer Builder · Referência: Banco de provas (ETAPA 2.5)

> As fontes de números, estudos, patentes e citações que deixam o mecanismo mais específico, o formato de cada item e o schema do `research-foundation.json`. Abra na ETAPA 2.5.

### ETAPA 2.5 — Banco de provas (munição pra copy, nunca teto)

Claim específico vende mais que claim genérico (Hopkins): "47% menos inchaço em 14 dias" bate "reduz o inchaço". Esta etapa junta a **munição** que deixa o mecanismo mais específico e mais crível — números, estudos, citações, patentes, o que os concorrentes escalados citam. É um banco pra copy puxar, não uma régua que limita o que a copy pode afirmar.

**Fontes (web search rápido — 15-20 min, não uma tese):**

1. **Estudos e resumos de estudo** — PubMed, Google Scholar, ScienceDirect; queries: ingrediente/processo + "study", "trial", "mechanism of action". Pra estudo atrás de paywall, `WebSearch "PMC <título>"` costuma ter o texto integral.
2. **Comunicados e press releases** — Harvard Health, Mayo Clinic, Cleveland Clinic; whitepapers de fornecedores de ingrediente (Lonza, DSM, BASF).
3. **Patentes** — Google Patents (ingrediente/processo com nome próprio).
4. **O que os concorrentes escalados já citam** — números e estudos que aparecem nas LPs do `product-research/banco-de-marcas.md` e da `competitor-analysis`: se uma marca que escala usa um número, o mercado já aceitou esse número.

**Pra cada item, registre:**

```json
{
  "claim": "o claim que o item sustenta",
  "number": "o número pronto pra copy (ex: '47% em 14 dias') | null",
  "source_title": "título",
  "source_url": "url",
  "quote_or_summary": "trecho literal ou resumo em 1-2 frases",
  "used_by_competitors": ["marca A", "marca B"]
}
```

**Output:** `workspace/[produto]/offer-builder/research-foundation.json`:
```json
{
  "mechanism_name": "...",
  "proof_items": [ { ... } ],
  "best_numbers": ["os 3-5 números mais fortes, prontos pra headline/hook"]
}
```

A `copy-engine` e a `creative-engine` (creatives) leem o arquivo pra dar número e nome à prova. O que não está no banco não trava nada: claim forte que o mecanismo sustenta entra na copy do mesmo jeito, e o banco só deixa ele mais específico.
