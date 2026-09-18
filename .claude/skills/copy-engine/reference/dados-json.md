# Copy Engine · Referência: JSON companion obrigatório, o schema do dados.json

> O schema completo do `copy-engine/dados.json` (hero com headlines, top 5, picks de A/B e variants, `cta_variants`, benefits, social proof, specs, urgency, email hooks, `voc_coverage`, `voc_forced_continue`, espécime e `markup_audit`) e as notas sobre quem lê cada campo. Abra ao gravar o `dados.json`.

## JSON Companion Obrigatório — `copy-engine/dados.json`

## O `resumo`, o bloco que a próxima fase lê primeiro

O `dados.json` abre com um objeto `resumo`: até doze campos curtos com o que a fase seguinte precisa saber de primeira, sem abrir o arquivo inteiro. Ele não guarda dado novo, é espelho do que já está mais abaixo: cada campo copia o valor literal do campo de origem, e onde diverge, o campo de origem vence. Preencha por último, depois que o resto do arquivo estiver fechado.

Schema:
```json
{
  "resumo": {
    "lead_type": "story|big_idea|problem_agitation|mechanism|secret|proclamation|offer|direct",
    "headline_primary": "a headline que foi pro hero",
    "subheadline": "a subheadline do hero",
    "mechanism_sentence": "a frase que explica o mecanismo",
    "top3_benefits": ["o benefício como está escrito na página"],
    "primary_cta": "o texto do botão principal",
    "guarantee_line": "a garantia como está escrita",
    "proof_highlights": ["o número ou depoimento que carrega a prova"],
    "urgency_line": "a linha de urgência, se existe",
    "faq_count": 0,
    "voc_coverage_pct": 0,
    "specimen_primary": "o espécime estrutural usado"
  },
  "copy_id": "uuid-v4",
  "product_slug": "...",
  "offer_id": "ref ao offer-builder/dados.json",
  "lead_type": "story | big_idea | problem_agitation | mechanism | secret | proclamation | offer | direct",
  "hero": {
    "headlines": [
      {"id": "h-01", "text": "...", "type": "benefit|curiosity|authority|contrarian|big_idea", "score": 9.2, "reasoning": "..."}
    ],
    "top_5_ranked": ["h-01", "h-07", "h-12", "h-03", "h-18"],
    "ab_test_picks": ["h-01", "h-07", "h-12"],
    "subheadline": "...",
    "cta_primary": "...",
    "cta_secondary": "...",
    "variants": [{"id": "hero-A", "approach": "authority | problem_agitate | ...", "subheadline": "...", "hypothesis": "..."}]
  },
  "cta_variants": [{"id": "cta-A", "text": "...", "hypothesis": "..."}],
  "mechanism_copy": "...",
  "benefits": [{"title": "...", "body": "...", "voc_refs": ["..."]}],
  "social_proof": {"testimonials": [...], "proof_stack": [...]},
  "offer_stack": "...",
  "guarantee_copy": "...",
  "faq": [{"q": "...", "a": "..."}],
  "specs": [{"label": "...", "value": "..."}],
  "urgency": "...",
  "email_hooks": ["..."],
  "voc_coverage": { "total_checked": 20, "literal_hits": 14, "paraphrased": 5, "missing": 1 },
  "voc_forced_continue": false,
  "decision_modalities_covered": ["spontaneous", "competitive", "humanistic", "methodical"],
  "specimen_primary": "agora-11-blocos",
  "specimen_secondary": null,
  "specimen_block_map": [
    {"n": 1, "bloco": "saudacao qualificada", "trabalho": "pre-qualifica o leitor pelo estado emocional", "conteudo_origem": "voc_top20 #3 + persona da `market-research`"}
  ],
  "markup_audit": {
    "four_us": {"urgent": true, "useful": true, "unique": false, "ultra_specific": true},
    "ideal_prospect": true,
    "big_promise": true,
    "first_page_test": true,
    "four_emotions": {"new_only": true, "safe_predictable": false, "easy_anybody": true, "big_fast": true},
    "makepeace_4": {"grab_eyeballs": true, "expand_hl": true, "cred": true, "bribe": true},
    "defects_found": ["too vague (secao Benefits, corrigido)"],
    "verdict": "pass | rewrite_lead"
  }
}
```

> `specimen_primary`/`specimen_block_map` vêm da ETAPA 2.5 e `markup_audit` do sweep 9. A skill `ad-analysis` usa os dois pra diagnosticar: quando uma página converte mal, a primeira pergunta é se o espécime escolhido era o certo pro avatar, e a segunda é qual camada do audit já tinha reprovado antes do launch.

`lead_type` é o campo **top-level** decidido na ETAPA 2 — contrato com a `page-design` (que o lê pra confirmar `page_type`). `voc_forced_continue` é o flag do pré-flight (só `true` quando o membro escolheu prosseguir com VOC insuficiente).

**A `page-design` (pré-flight/PLAN) e a `page-build` (populate/GEO) leem diretamente este JSON** — se inválido, a fase STOREFRONT não prossegue.
