# Shocking Stats Vault

Repositório de estatísticas "shocking" (surpreendentes, memoráveis, com autoridade) usadas em hooks, advertoriais, e press releases pra estabelecer credibilidade instantânea.

## Por que isso existe

Hook com número específico + fonte autorizada converte 2-3x melhor que hook vago. Exemplo:

- Fraco: "Most people don't get enough sleep"
- Forte: "The CDC says 1 in 3 American adults sleeps less than 7 hours — [source]"

Stats memoráveis são caros de garimpar (precisa fonte institucional + dado recente + relevância pro pitch). Vault evita refazer esse trabalho a cada skill run.

## Estrutura

Por nicho/tema, o membro acumula stats no arquivo:

```
/workspace/[produto]/shocking-stats.json
```

Cada entry:

```json
{
  "id": "stat-0042",
  "statement": "frase exata com número",
  "numeric_value": "1 in 3",
  "unit": "adults",
  "topic": "sleep deprivation",
  "source_name": "CDC",
  "source_url": "https://www.cdc.gov/sleep/data_statistics.html",
  "source_type": "government|peer_reviewed_study|institutional_report|industry_report|book|news_outlet",
  "source_date": "2024-06-15",
  "credibility": "high|medium|low",
  "emotional_charge": "fear|surprise|anger|curiosity",
  "best_for": ["hook", "advertorial_intro", "proof_block", "pr_release"],
  "do_not_use_if": ["avatar muito educado já sabe desse stat (usar como baseline, não revelation)"],
  "used_in_creatives": ["c-01", "c-07"],
  "verified_at": "2026-04-20",
  "verification_frequency": "annual",
  "next_verification_due": "2027-04-20"
}
```

## Como alimentar a vault (processo recomendado)

1. **Skill 02 (market research)** extrai frases de review/post que MENCIONAM stats → tentar rastrear fonte original
2. **Skill 04 (Research Foundation Etapa 2.5)** já coleta evidence pra mecanismo — stats relacionados ao mecanismo vão pra vault
3. **Skill 07 (creative-engine)** consulta vault quando precisa de hook com número autoritativo
4. **Skill 09 (ad-analysis)** registra quais stats apareceram em winners vs losers — pattern-matching ao longo do tempo

## Regras de rigor (NON-NEGOTIABLE)

1. **NUNCA inventar stat**. Se a frase tem número, precisa de fonte rastreável com URL.
2. **NUNCA usar stat sem verificar frescor**. Stats expiram — um CDC report de 2015 citado em ad de 2026 é enganoso. Verificar se há update mais recente.
3. **`credibility: high` só pra** governos, peer-reviewed, institutional reports bem-conhecidos. Industry reports self-published são `medium`. Blog posts/news aggregators são `low` (evitar).
4. **Source URL obrigatória** — se a URL expira (paywall, remoção), re-verificar trimestralmente via Wayback Machine.
5. **Contextualizar**: stat fora de contexto é fake news. Incluir `statement` completo com framing honesto.

## Anti-patterns (FORBIDDEN)

- "Studies show 90% of people..." (sem fonte = inventado)
- "Experts agree..." (sem nomear o expert)
- Dados de pesquisa paga pela própria marca sem disclosure
- Extrapolar de amostra pequena pra population claim
- Mudar unidades pra fazer parecer mais dramático ("1 in 3" vira "33%" vira "33 million" sem validar denominador)

## Integração

- **Hook-taxonomy**: archetype `secret_reveal` e `contrarian` frequentemente usam shocking stat como abertura
- **Promise↔Config gate**: se ad claim ou copy claim usa stat, o gate verifica que ele existe na vault E tem `credibility: high|medium` E `verified_at` < 12 meses
- **Compliance pre-flight**: stat sem fonte rastreável = `severity: high` (Meta requires claim substantiation)

## Template inicial (genérico, não brand-specific)

Quando o produto entra pela Skill 01, inicializar vault vazia com skeleton:

```json
{
  "product_slug": "[slug]",
  "topic_cluster": "[vertical — ex: skincare / fitness / sleep / finance]",
  "initialized_at": "ISO",
  "stats": []
}
```

Skills populam a vault ao longo do funil — não existe "vault inicial pronta" pro membro; é construída incrementalmente com rigor.
