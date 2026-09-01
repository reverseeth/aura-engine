# Recipe: Rotate Winning Creative

## Triggers
- "rotaciona o winner [ID]"
- "gera variações do [ID]"
- "escala o winner"

## Input
- `winner_creative_id` — criativo classificado como `breakthrough` pela Skill 11 (gate no pre-flight abaixo)
- `n_variations` — default 3

## Cascade (Meta — ver `.claude/lib/mcp-detect/README.md`)

Esta receita não chama o Meta diretamente: o único toque na plataforma é o **upload das variações**, delegado a `upload-creative-to-meta.md`, que carrega o próprio cascade (caminho 1 oficial `mcp__meta__ads_*` pra resolver ad set / caminho 2 Pipeboard `mcp__meta-ads__*` pro upload do binário — o upload força Pipeboard porque o oficial é remoto e não lê arquivo local). Logo a posição no cascade é herdada da receita de upload; aqui nada muda.

## Pre-flight
- [ ] **Gate de rotação — só `breakthrough` rotaciona (cânone `.claude/lib/ad-taxonomy/README.md` §2):** o `winner_creative_id` tem `class == "breakthrough"` em `manifest.ad_classification[]` (gravado pela Skill 11) — equivalente: o id está em `manifest.breakthroughs[]` ou em `11-ad-analysis/dados.json.breakthroughs[]`. `kpi_winner` NÃO rotaciona: bate o KPI sem puxar spend e o cânone o trata como loser para decisão — gerar variações dele multiplica um resultado de amostra pequena. `spend_winner` também não entra: o destino dele é iteração (Skill 14, Movimento 1), não rotação.
- [ ] **Fallback legado** — produto sem `ad_classification[]`/`breakthroughs[]` no manifest (análise antiga ou Skill 11 nunca rodada): aplicar o gate antigo (CPA < target × 0.8 E spend > $300 E age > 5 days) e AVISAR o membro antes de prosseguir: "esse produto ainda não tem a classificação canônica da Skill 11; usei o gate legado, que não distingue breakthrough de KPI winner — recomendo rodar `ad analysis` antes de ativar as variações". `manifest.winners[]` legado existe em dois shapes (ids string — alias de `breakthroughs[]` — ou objetos com métricas, em produto antigo); aceite ambos pra LOCALIZAR o criativo, mas presença em `winners[]` sozinha nunca substitui o gate — o array antigo pode carregar `kpi_winner` disfarçado de winner.
- [ ] Skill 08 disponível pra gerar variations
- [ ] MCP de upload disponível (Pipeboard `mcp__meta-ads__*` ou Playwright — herda de `upload-creative-to-meta.md`)

## Steps

### 1. Identificar winner + extrair DNA
```
winner = read(/workspace/[produto]/08-creative-engine/concept-XX.md)
dna = read(/workspace/[produto]/creative-dna/dna-profile.json)  # se existe
```

### 2. Gerar N variações preservando DNA (instruções diretas — não existe "modo rotation" na Skill 08)

Gere cada briefing de variação diretamente, a partir do conceito-pai:

1. Carregue o concept do winner em `08-creative-engine/dados.json` (o objeto do concept correspondente — hook, ângulo, mechanism, CTA, proof stack, formato) + o briefing `concept-XX.md` como contexto.
2. Pra variação N, mude **UM único eixo** — `["hook_text", "voiceover_tone", "visual_opening"][N-1]` — e escreva o novo briefing herdando TODO o resto do conceito-pai inalterado: mechanism (nome + posição), CTA, proof stack, estrutura 3-2-2.
3. Se `dna-profile.json` existe, use as features de maior win-rate como guia do que NÃO tocar.

O output de cada variação é um briefing novo (`concept-XX-v2.md`, `-v3`, `-v4`) no mesmo formato da Skill 08 — mas gerado aqui inline, sem re-rodar o fluxo completo da 08 (a rotação pula ideação/batch: o conceito já está validado, só o eixo varia).

### 3. Rodar compliance + DNA extraction em cada
(Automático via ETAPAs 7.5 + 7.6 da Skill 08)

### 4. Upload pro Meta (invocar `upload-creative-to-meta.md` pra cada)
```
for variation in new_variations:
  invoke_recipe("upload-creative-to-meta", {
    creative_id: variation.id,
    ad_set_name: winner.ad_set,
    status: "PAUSED"
  })
```

### 5. Log
```json
{
  "action": "rotate_winner",
  "source": "<meta_mcp_pipeboard | playwright — herdado da receita de upload>",
  "parent_creative": "<creative-id>",
  "parent_class": "<breakthrough | legacy_gate — qual gate liberou a rotação>",
  "variations_generated": ["<creative-id>-v2", "<creative-id>-v3", "<creative-id>-v4"],
  "all_paused": true,
  "dna_compliance": "preserved (+80% overlap)"
}
```

**Ad log (cânone `.claude/lib/ad-log/README.md`):** as criações na conta acontecem — e são registradas no ad-log — pela sub-receita `upload-creative-to-meta.md`, na mesma execução, uma linha por variação subida (motivo: "variação de rotação do [winner_creative_id]"). Esta receita não duplica essas linhas.

Mensagem:
```
✓ Winner <creative-id> rotacionado.
  3 variações geradas, subidas paused no Meta:
  - v2: hook variation ("At 45 I was 2 days away...")
  - v3: voiceover variation (mais educated tone)
  - v4: visual opening variation (bathroom vs kitchen)

  Pra ativar: Meta Ads Manager ou "Claude, ativa todas as v2-v4"

  DNA preserved: 85% overlap com winner (hook_type, mechanism_position, cta_tone mantidos)
```

## Integração com o loop criativo
A receita `creative-loop.md` invoca esta rotação como parte do ciclo
ad → performance → variação quando o critério de winner é batido. A execução
SEMPRE passa por aprovação do membro antes do upload — não existe rotação
autônoma no framework hoje (o "Shadow Brain" citado em versões antigas é
conceito futuro, não implementado).

## Limitação
- Não substitui análise humana. Criatividade mecânica preserva DNA mas pode
  perder spark do winner. Membro deve revisar briefings antes de ativar
