# Ad Log — registro de mudanças na conta (cânone)

O artefato que faltava do sistema de learnings: **um registro cronológico de toda MUDANÇA executada na conta de ads**, separado das leituras. As análises datadas da skill 11 registram o que foi *lido*; este log registra o que foi *feito*. Sem ele, o caso clássico fica indiagnosticável: performance cai numa semana e ninguém lembra que um high spender foi desligado três semanas antes.

## Arquivo

`workspace/[produto]/ad-log.md` — **append-only** (nunca reescrever linhas antigas), uma linha por mudança, mais recente por último. Isento de dual output (arquivo operacional de handoff, como `dados.json`).

## Formato da linha

```
| YYYY-MM-DD HH:MM | entidade | mudança | executor | motivo curto |
```

- **entidade**: `campaign:[nome]` · `adset:[concept_id]` · `ad:[creative_id]` · `automation:[nome]` · `budget` · `page:[url]` · `oferta`
- **mudança**: o que mudou, com valores (antes → depois quando fizer sentido): "budget $200→$240", "pausado", "religado", "criado em PAUSED", "daily maximum $240 aplicado", "LP trocada para /v2"
- **executor**: `skill-10` · `skill-12` · `skill-14` · `recipe:full-deploy` · `recipe:creative-loop` · `recipe:pause-ad-set` · `membro` (quando ele relata mudança manual)
- **motivo curto**: a régua/decisão que motivou ("scaling protocol +20%", "kill 7d sem spend/KPI", "reset da meia-noite", "promo início")

## Quem ESCREVE (obrigatório, no momento da execução)

- **Skill 10** — criação de campanha/ad sets/ads (mesmo em PAUSED) e automações de proteção.
- **Skill 12** — todo ajuste de budget (subida, descida, reset da meia-noite), duplicação em ABO, graduação pra ASC.
- **Skill 14** — duplicações e novos ad sets/LPs criados pela amplificação.
- **Skill 17** — tudo que a janela promocional muda na conta: campanha promo, budget direto da promo, surf/recuo intradiário, resets da janela, rule de fim de promo, religada do evergreen.
- **Receitas** `full-deploy`, `creative-loop`, `pause-ad-set`, `upload-creative-to-meta` — cada ação executada via MCP.
- **Qualquer skill** que souber de mudança manual do membro ("desliguei o ad X ontem") registra com executor `membro`.

## Quem LÊ

- **Skill 11** — SEMPRE, no início da análise: cruzar a janela de leitura com as mudanças do período ("a queda de quinta coincide com o quê?"). Mudança sem efeito esperado e efeito sem mudança conhecida são os dois achados que só este log revela.
- **Skill 12** — antes de escalar: a última mudança de budget e há quanto tempo (o gate de 24h entre degraus é verificado aqui, não de memória).

## Regra

Mudança executada e não logada é bug de processo — as receitas devem logar na MESMA execução que faz a mudança, nunca "depois". Se o arquivo não existir, criar com o cabeçalho da tabela na primeira escrita.
