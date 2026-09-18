# Content Recycler · Referência: O gatilho, as duas trilhas, a fonte de cada uma e quando usar

> O texto integral da abertura, da nota de que o gatilho é breakthrough e nunca winner, da ordem das duas trilhas, da fonte primária de cada trilha com a consulta à base pelo índice, e de quando a skill é acionada. Abra antes da ETAPA 0.

Skill auxiliar invocável. Pega um criativo que **já provou escalar** e tira dele tudo que ele ainda pode dar — primeiro dentro do tráfego pago (Trilha 1), depois nos canais próprios (Trilha 2).

> **O gatilho é `breakthrough`, não "winner".** As 4 classes de resultado são definidas no cânone `.claude/lib/ad-taxonomy/README.md` §2 e medidas pela skill `ad-analysis` — esta skill LÊ a classificação e nunca a recomputa. Só `breakthrough` (KPI do AD melhor que o KPI da CAMPANHA **e** puxando spend) libera reciclagem. `KPI winner` bate o KPI mas não puxa spend, e o cânone o trata como **loser para decisão**: reciclar um KPI winner é multiplicar um criativo que nunca provou nada em escala — o KPI bonito veio de amostra pequena.

> **Duas trilhas, nesta ordem.** **Trilha 1 — Amplificação** roda primeiro, sempre: é o que se faz de verdade com um ad que venceu (iterar, portar, dar página própria, levar pra outro canal, dar budget dedicado, devolver pro pipeline criativo). **Trilha 2 — Derivadas de formato** são as 9 peças de canal próprio; continuam disponíveis, mas como jogada de **marca e de LTV**, não de performance. Quem escala a conta é a Trilha 1.

> **Fonte primária da Trilha 2 é a lib, não a base.** A estrutura "1 criativo → 9 formatos" (specs, length, tom de cada derivada) vem INTEIRA de `.claude/lib/content-recycler/` (`recycler.md` = engine do fluxo, `formats.json` = specs dos 9 formatos) — não existe framework "9 derivadas" na base de conhecimento, então NUNCA busque isso lá. A Trilha 1 não vem da lib: ela vem do cânone `.claude/lib/ad-taxonomy/README.md` (§2 classes, §5 escala, §7 Sniper) mais os movimentos descritos aqui. A base entra só pros **frameworks de copy NOMEADOS**: os domínios desta skill no índice `.claude/lib/kb-index/` (mapa skill→domínio no README) são **creatives-hooks-formats** (principal) e **page-landing-cro** (relevante pra LP/prelander da Trilha 1 e pras derivadas advertorial e blog SEO). Quando uma etapa pede "consultar a base", NUNCA use query genérica — puxe os SISTEMAS NOMEADOS rodando `search_knowledge` com a `best_query` de cada framework relevante pra aquela etapa (`deep=true`).
>
> **Consulta à base pelo índice:** rode `python3 .claude/lib/kb-index/kb_lookup.py --skill content-recycler --domain <domínio desta etapa>` e trabalhe com a lista impressa (omita o `--domain` quando a etapa cruza vários domínios). Puxe as entradas relevantes à etapa com a `best_query` exata e `deep=true`, no máximo 6 buscas adicionais por etapa. As queries já embutidas na etapa são piso obrigatório: rodam sempre e não contam no teto, que vale só para as buscas adicionais que a etapa pedir. Não repita busca de framework já puxado na sessão.

## Quando usar

**Manual**: membro diz `recycle [creative-id]`, `recycle breakthrough` ou `recycle winner` (as três entradas caem na mesma detecção abaixo).

**Automático** (futuro): disparada automaticamente quando a skill `ad-analysis` classifica um criativo como `breakthrough`. Hoje o trigger é sempre manual.
