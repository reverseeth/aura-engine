# Recipe: Rotate Winning Creative

## Triggers
- "rotaciona o winner [ID]"
- "gera variações do [ID]"
- "escala o winner"

## Input
- `winner_creative_id` — ad que tá performando (top decile CPA)
- `n_variations` — default 3

## Cascade (Meta — ver `.claude/lib/mcp-detect/README.md`)

Esta receita não chama o Meta diretamente: o único toque na plataforma é o **upload das variações**, delegado a `upload-creative-to-meta.md`, que carrega o próprio cascade (caminho 1 oficial `mcp__meta__ads_*` pra resolver ad set / caminho 2 Pipeboard `mcp__meta-ads__*` pro upload do binário — o upload força Pipeboard porque o oficial é remoto e não lê arquivo local). Logo a posição no cascade é herdada da receita de upload; aqui nada muda.

## Pre-flight
- [ ] Winner tem CPA < target × 0.8 E spend > $300 E age > 5 days
- [ ] Skill 08 disponível pra gerar variations
- [ ] Content Recycler disponível (#17)
- [ ] MCP de upload disponível (Pipeboard `mcp__meta-ads__*` ou Playwright — herda de `upload-creative-to-meta.md`)

## Steps

### 1. Identificar winner + extrair DNA
```
winner = read(/workspace/[produto]/08-creatives/08-concept-XX.md)
dna = read(/workspace/[produto]/creative-dna/dna-profile.json)  # se existe
```

### 2. Gerar N variações preservando DNA
Invocar Skill 08 em modo "rotation":
```
Pra cada N:
  briefing = skill_07.generate_rotation(
    parent_creative=winner,
    dna_profile=dna,
    variation_axis=["hook_text", "voiceover_tone", "visual_opening"][N-1]
  )
```

Cada variação muda UM eixo; preserva mechanism, CTA, proof stack.

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
  "source": "meta_mcp_pipeboard",
  "parent_creative": "<creative-id>",
  "variations_generated": ["<creative-id>-v2", "<creative-id>-v3", "<creative-id>-v4"],
  "all_paused": true,
  "dna_compliance": "preserved (+80% overlap)"
}
```

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

## Integração com Shadow Brain (#1)
Se Shadow Brain rodando e critério de winner batido automaticamente:
- Alert pra membro com recomendação
- Se `autonomous_rotate: true` no manifest: executa receita sem input

## Limitação
- Não substitui análise humana. Criatividade mecânica preserva DNA mas pode
  perder spark do winner. Membro deve revisar briefings antes de ativar
