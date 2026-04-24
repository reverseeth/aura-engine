---
name: content-recycler
description: Pega 1 criativo winner e gera 9 derivadas adaptadas a canais diferentes (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube pre-roll, SMS, package insert, podcast ad). Multiplica ROI do mesmo criativo por 5-10× sem produção nova. Use quando o membro disser "recycle [id]", "reaproveitar winner", "content recycler", "tirar mais dos ads". Zero infra externa, só Claude + Python.
---

# Content Recycler (Skill 17)

Skill auxiliar invocável. Reutiliza criativos vencedores em 9 formatos diferentes.

## Quando usar

**Manual**: membro diz `recycle [creative-id]` ou `recycle winner`.

**Automático** (futuro, com Shadow Brain #1 rodando): disparada quando critério de winner é atingido (CPA < target × 0.7, spend > $300, idade > 5 dias).

## Pré-flight

- [ ] `manifest.json` existe
- [ ] Pelo menos 1 criativo em `/workspace/[produto]/07-creatives/` OU membro forneceu fonte alternativa
- [ ] `.claude/lib/content-recycler/recycler.md` existe (este lib é o engine)
- [ ] `.claude/lib/content-recycler/formats.json` existe (specs dos 9 formatos)
- [ ] `.claude/lib/compliance-preflight/` existe (pra rodar check em cada derivada)

**Detecção de winner (quando input é `recycle winner`):**

Se membro digitou `recycle winner` (sem ID específico):
1. Ler `/workspace/[produto]/09-analysis/latest.json` (produzido pela Skill 09)
2. Extrair `latest.winners[]` (array populado pela skill 09 com `outcome == "winner"` — critério: CPA < target × 0.7, spend_total > $300, days_active > 5)
3. Se `winners.length === 1` → usar `winners[0].creative_id`
4. Se `winners.length >= 2` → apresentar lista (id + cpa + roas + spend) e perguntar qual reciclar
5. Se `winners.length === 0` OU campo `winners` ausente (versão antiga do latest.json) → responder:
   > "Campanha ainda não tem winner identificado. Critério: CPA < target × 0.7 + spend > $300 + idade > 5 dias.
   >
   > Opções:
   > 1. Aguardar mais dados (normalmente 5-10 dias após launch)
   > 2. Rodar skill 09 de novo pra atualizar análise
   > 3. Forçar reciclagem de um criativo específico: `recycle [creative-id]`"
6. Se `latest.json` não existir (skill 09 nunca rodou) → responder:
   > "Skill 09 não foi rodada ainda. Preciso de dados de performance pra identificar winner automaticamente. Rode `run analysis` primeiro OU reciclar criativo específico: `recycle [creative-id]`"

## Fluxo

Siga exatamente o fluxo descrito em `.claude/lib/content-recycler/recycler.md`:

1. **Identificação do winner** — input `[creative-id]` ou `winner` (top CPA recente)
2. **Extração de essência** — destilar big idea, hook, mechanism, avatar, voice em `essence.json`
3. **Consultar base Aura** — frameworks por formato (advertorial, email, TikTok, blog, etc)
4. **Gerar 9 derivadas** em paralelo (advertorial, email sequence, organic TikTok, blog SEO, Pinterest carousel, YouTube preroll, SMS, package insert, podcast ad)
5. **Compliance Pre-flight em cada** — severity >= high dispara auto-rewrite
6. **Gerar README.md + compliance-log.json** consolidados

## Output

Pasta `/workspace/[produto]/17-recycled/[source-id]/` com:
- `README.md` — índice + instruções de distribuição
- `essence.json` — essência extraída (reusável)
- `compliance-log.json` — log consolidado
- 9 arquivos `.md`, um por formato

## Sucesso

- [ ] 9 arquivos gerados
- [ ] Cada um passa compliance check (severity ≤ medium)
- [ ] Essence.json salvo
- [ ] README.md com índice pronto
- [ ] HTML companion (se aplicável a advertorial/blog)

## Customização

Pra adicionar novo formato (ex: LinkedIn post, Substack newsletter, Twitter thread), editar `.claude/lib/content-recycler/formats.json` adicionando entry com:
- `id`, `name`, `output_file`
- `length_words` range
- `structure` template
- `tone`
- `compliance_notes`

Próxima rodada da skill gera automaticamente também esse formato.

## Mensagem final ao membro

```
✓ Content Recycler rodou em [source-id]
  9 formatos gerados em /workspace/[produto]/17-recycled/[source-id]/

  Compliance: [X críticos, Y high, Z medium, W low]
  Rewrites aplicados: [N]

  Distribuição sugerida:
  → Advertorial: publicar como LP secundária pra cold traffic
  → Email sequence: importar no Klaviyo como welcome flow
  → TikTok orgânico: post na conta da marca
  → Blog: publicar pra SEO, registrar no Search Console
  → Pinterest: criar board, pin semanal
  → YouTube pre-roll: campaign separada
  → SMS: wire no Postscript como opt-in trigger
  → Package insert: enviar pro fornecedor imprimir
  → Podcast: outreach pra shows do nicho

  Abra o README.md da pasta pra ver índice completo.
```
