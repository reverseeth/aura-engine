# Content Recycler · Referência: Pré-flight e detecção do breakthrough

> O pré-flight completo com o idioma e a checklist de arquivos, a detecção por classe com as fontes em ordem e o fallback legado, as regras de quem entra e quem não entra, e as respostas prontas pros casos sem breakthrough e sem análise. Abra no pré-flight.

## Pré-flight

**Pastas do produto (fallback por um ciclo):** cada fase mora numa pasta com o nome da skill, sem número (`market-research/`, `page/`). Produto criado antes dessa mudança pode ainda ter a pasta numerada antiga (o `legacy_folder` da skill no `.claude/skills.json`); o hook de início de sessão migra sozinho. Se mesmo assim a pasta nova de uma fase anterior não existir e a numerada existir, rode `python3 tools/migrate.py --product [slug]` e leia da pasta nova. Só leia da pasta numerada se a migração não puder rodar; escreva sempre na pasta sem número.

Leia `report_language` de `workspace/profile.md` (default `pt-BR` se ausente; também disponível em `manifest.report_language`). TODO output interno (README.md/.html, `essence.json` descritivo, `amplification-plan.md`, `creator-report.md`) e toda conversa com o membro usam esse idioma. **As 9 derivadas consumidor-final (advertorial, email, TikTok, blog, Pinterest, YouTube, SMS, package insert, podcast), o `framework_template`, os hooks/scripts citados nos briefs da Trilha 1, a copy de end card e a VOC literal permanecem SEMPRE em inglês US**, independente do report_language.

- [ ] `manifest.json` existe
- [ ] Pelo menos 1 criativo em `workspace/[produto]/creative-engine/` OU membro forneceu fonte alternativa
- [ ] `.claude/lib/ad-taxonomy/README.md` existe (cânone das 4 classes — o gatilho e a régua de ABO saem daqui)
- [ ] `.claude/lib/content-recycler/recycler.md` existe (engine da Trilha 2)
- [ ] `.claude/lib/content-recycler/formats.json` existe (specs dos 9 formatos)

**Detecção de breakthrough (quando o input não traz ID específico):**

1. Ler `workspace/[produto]/ad-analysis/dados.json` (produzido pela Skill `ad-analysis`).
2. Selecionar os criativos que a skill `ad-analysis` classificou como **`breakthrough`** no campo canônico **`ad_class`** (enum do cânone §2: `breakthrough` | `spend_winner` | `kpi_winner` | `loser`). Fonte, nesta ordem:
   - **Primária:** o array **`breakthroughs[]`** do `dados.json` (contém apenas `ad_class == "breakthrough"`). `manifest.breakthroughs[]` espelha o mesmo conteúdo como estado consolidado, e `manifest.ad_classification[]` (também gravado pela `ad-analysis`) traz a classe de CADA criativo — é nele que se confere a classe de um id específico quando o `dados.json` da rodada não estiver à mão.
   - **Fallback legado**, só se nenhum dos três existir (análise antiga): `winners[]`, aceitando os DOIS shapes — **ids string** (o alias moderno: conteúdo idêntico a `breakthroughs[]`) ou **objetos com métricas** (produto antigo; extrair o id de `creative_id`/`id`). No shape objeto, use `ad_class == "breakthrough"` se o campo existir; sem ele, o rótulo positivo das análises velhas era `outcome == "winner"` — e esse rótulo NÃO distingue breakthrough de `kpi_winner`. Nesse caso, avise o membro de que a classificação canônica não existe e recomende re-rodar a Skill `ad-analysis` antes de reciclar. **`winners[]` está DEPRECADO**: nunca fonte nova. Nunca reciclar um criativo só por ele aparecer num array chamado `winners[]`.
   - Os outros dois arrays da `ad-analysis` (`spend_winners[]` e `kpi_winners[]`) **não** são fonte de reciclagem — entram só nas regras 3 e 4 abaixo.

   A `content-recycler` **NÃO recomputa critério** (classificar é responsabilidade exclusiva da `ad-analysis`); apenas ordena por `spend_total` desc (tiebreak `days_active` desc). Se precisar de target pra exibir, leia explícito de `manifest.target_cpa`.
3. **`kpi_winner` nunca entra** — nem quando aparece em `kpi_winners[]`, nem quando o membro pede pelo id. O cânone §2 o trata como loser para decisão. Se o membro insistir, explique em uma linha (bateu o KPI com pouco spend, não provou escala) e ofereça o caminho certo: iterar via Skill `creative-engine`.
4. **`spend_winner` entra só pela porta estreita** (o array `spend_winners[]` da `ad-analysis`). O cânone §2 manda **iterar, não escalar**: ele libera exclusivamente o **Movimento 1** da Trilha 1 (iteração pelos 4 elementos). Sem LP dedicada, sem port de canal, sem duplicação em ABO, sem Trilha 2. Diga isso ao membro antes de começar.
5. Se houver 1 breakthrough → usar ele. Se houver ≥2 → apresentar a lista ordenada (id + cpa + roas + spend) e perguntar qual amplificar primeiro.
6. Se `breakthroughs[]` vier vazio (nenhum criativo com `ad_class == "breakthrough"`) → a resposta honesta não é "aguardar mais dados". Diga quantos criativos caíram em cada classe e responda:
   > "Você ainda não tem um ad que escala: nenhum criativo foi classificado como breakthrough (KPI do ad melhor que o da campanha **e** puxando spend). [Se houver KPI winners: X criativos bateram o KPI sem puxar spend — e ad que não puxa spend não provou nada em escala, então multiplicá-lo só multiplica um teste pequeno.]
   >
   > O próximo passo é a Skill `creative-engine` (mais criativo), não a `content-recycler`. Opções:
   > 1. Rodar `creatives` pra gerar o próximo batch
   > 2. Rodar `run analysis` de novo, se a campanha andou desde a última leitura
   > 3. Se existe `spend_winner`, rodar só a iteração pelos 4 elementos: `recycle [creative-id]`"
7. Se `dados.json` não existir (skill `ad-analysis` nunca rodou) → oferecer 2 caminhos (não abortar seco):
   > "Skill `ad-analysis` não foi rodada ainda, então não tenho a classificação dos criativos. Opções:
   > (A) Rodar `run analysis` agora pra classificar, OU
   > (B) trabalhar um criativo específico direto: `recycle [creative-id]`."

Quando o membro passa `[creative-id]` direto, cheque a classe desse id (`ad_class` no `dados.json` da `ad-analysis`, ou `manifest.ad_classification[]`) antes de rodar: `breakthrough` → tudo liberado; `spend_winner` → só o Movimento 1; `kpi_winner` ou `loser` → recusa com a explicação do item 3. Se o id não estiver em nenhuma análise (criativo nunca rodado), avise que não há classificação e que o plano sai sem lastro de performance — o membro decide se segue.
