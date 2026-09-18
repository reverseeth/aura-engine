# Ad Analysis · Referência: NEXT_BATCH_IDEAS.md (fecha o loop com a creative-engine)

> O critério de parada (menos de 50% das ideias anteriores testadas = não gerar novas) e o conteúdo obrigatório do arquivo: ângulos, variável por breakthrough, método da iteração, re-research, hook vs hold, governador de volume, ângulos a evitar, VOC não usada, formatos, awareness e carry-over. Abra antes de gerar o arquivo.

### Output adicional — NEXT_BATCH_IDEAS.md (fecha loop `ad-analysis`→`creative-engine`)

Além de `[YYYYMMDD]-analysis.md`, gerar OBRIGATORIAMENTE:
`workspace/[produto]/ad-analysis/NEXT_BATCH_IDEAS.md`

**Critério de parada pra evitar loop infinito entre `ad-analysis` e `creative-engine`:**

Antes de gerar ideias novas:
1. Se `NEXT_BATCH_IDEAS.md` já existe:
   - Ler versão anterior + ler `creative-engine/dados.json` (criativos gerados desde última rodada)
   - Comparar: quantas ideias propostas na versão anterior **foram testadas** (viraram criativos em creative-engine/dados.json com performance registrada nas análises desta skill)?
   - Se `testadas < 50%` das ideias propostas na última rodada → **Não gerar novas ideias.** Retornar versão anterior intacta + adicionar seção "Validation pending: {ideia1}, {ideia2} ainda não foram testadas — priorize antes de gerar novos angles."
   - Se `testadas >= 50%` → proceder com novas ideias (baseadas em learnings das testadas)
2. Se arquivo não existe: gerar do zero normalmente.

Conteúdo (quando gerar):
- **Ângulos a testar no próximo batch de creatives** (2-3 bullets específicos)
- **Variável a testar na iteração de cada breakthrough** (1 bullet por breakthrough: qual variável única muda mantendo o resto — ex: "c-03: mesma estrutura, testar a micro-persona X no lugar da Y"). `spend_winner` também ganha um bullet de iteração; `kpi_winner` não entra aqui.
- **Método da iteração (contrato com a `creative-engine`):** vencedor de pack `marksman` entra como iteração **`sniper` sobre o ângulo vencedor** (nomeado pela frase de `angles[]` + `winning_sub_avatar_id`); ângulo que perdeu com UMA execução só entra como re-teste (os 3 strikes do Execution Problem — ETAPA 3) antes de ir pra lista de evitar. Iteração que trocou de zona emocional (`iteration_zone_check`, ETAPA 4) entra refeita **na zona original**, mudando só a variável pretendida.
- **Re-research do ângulo vencedor** (ETAPA 5): registre aqui que a mini-passada da `market-research` no sub-avatar/ângulo vencedor precede o próximo swing grande — o batch derivado do breakthrough espera essa pesquisa quando ela foi recomendada.
- **Onde os losers perderam a audiência** (hook vs hold, com os números medidos): hook baixo → o próximo batch reescreve a abertura do mesmo conceito; hook bom + hold baixo → mantém a abertura e refaz o corpo.
- **Governador de volume:** se o `breakthrough_rate` caiu quando o volume de criativos subiu, o próximo batch deve ser **menor e mais deliberado** — a diretiva pra `creative-engine` é intenção, não quantidade.
- **Ângulos a EVITAR** (identificados como saturados ou já losers)
- **VOC phrases não usadas ainda** que aparecem em learning de review mining
- **Formatos a priorizar** (UGC vs studio vs static vs video — baseado em performance)
- **Awareness stage para focar** (se campanha atual oversserve um stage)
- **Ideias carry-over** (propostas antes, ainda não testadas)

**Skill `creative-engine` DEVE ler este arquivo no pre-flight.** Isto fecha o loop `ad-analysis`→`creative-engine` **com critério de parada.**
