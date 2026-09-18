# Content Recycler · Referência: Critérios de sucesso e como adicionar um formato novo

> As checagens do gatilho e de cada trilha, e o passo a passo para acrescentar um décimo formato ao arquivo de specs da lib. Abra antes de encerrar.

## Sucesso

**Gatilho (bloqueia tudo):**
- [ ] O criativo fonte está classificado como `breakthrough` pela skill `ad-analysis` — ou como `spend_winner`, e nesse caso só o Movimento 1 rodou
- [ ] Nenhum `kpi_winner` foi reciclado

**Trilha 1:**
- [ ] `essence.json` salvo com `framework_template` e `psychological_mechanism` preenchidos (nenhum dos dois vazio ou parafraseando o script)
- [ ] `amplification-plan.md` + `.html` com os 6 movimentos endereçados (os que a classe libera; os bloqueados aparecem com o motivo)
- [ ] Cada movimento tem handoff explícito (`creative-engine` / `page-design` / `scale-engine`) — nenhum movimento fica sem dono
- [ ] `creator-report.md` + `.html` gerados

**Trilha 2 (se rodada):**
- [ ] 9 arquivos `.md` gerados
- [ ] 9 arquivos `.html` companion gerados (rule 6b)
- [ ] Cada um passou na passada de estilo (rule 8a/8b)
- [ ] README.md + README.html com índice pronto

## Customização (Trilha 2)

Pra adicionar novo formato (ex: LinkedIn post, Substack newsletter, Twitter thread), editar `.claude/lib/content-recycler/formats.json` adicionando entry com:
- `id`, `name`, `output_file`
- `length_words_total` range (+ opcional `length_words_per_email`/`length_words_per_pin` quando o formato tem unidades, seguindo as entries existentes)
- `structure` template
- `tone`

Próxima rodada da skill gera automaticamente também esse formato.
