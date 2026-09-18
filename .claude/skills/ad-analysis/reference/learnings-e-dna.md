# Ad Analysis · Referência: Learnings documentados, DNA update e redação de PII (ETAPAs 10 e 11)

> As categorias de hipóteses do feedback loop, o mapeamento `ad_class` → `outcome` do registry de DNA com o perf JSON e os comandos do `registry.py`, e a redação de PII antes de salvar qualquer dump do Ads Manager. Abra nas ETAPAs 10 e 11.

### ETAPA 10 — Learnings Documentados (Pra Feedback Loop)

Na seção final do relatório, documente learnings que vão alimentar próximos batches:

**Hipóteses confirmadas por reaplicação** (a hipótese foi aplicada num criativo novo e ele virou `breakthrough` — só aqui ela deixa de ser palpite):
**Hipóteses levantadas nesta rodada** (vieram dos breakthroughs deste batch, ainda **não** reaplicadas — continuam sendo palpite fundamentado):
**Hipóteses rejeitadas** (foram reaplicadas e não confirmaram):
**Hipóteses ainda em teste** (precisa mais dados):
**Ideias pra próximo batch:**

Isso é o "feedback loop motor de crescimento" — cada análise enriquece o próximo batch de criativos.

### ETAPA 11 — DNA Update (silent — feedback automático pro registry)

Pra cada criativo analisado nesta rodada:

1. Gravar `ad_class` (as 4 classes do cânone §2 — o mesmo valor de `ad-analysis/dados.json` — mais `unclassified` quando ainda não há base pra classificar) **e** o `outcome` legado que o registry aceita.

   O banco do registry (`.claude/lib/creative-dna/schema.sql`) valida `outcome` contra um enum próprio e **não conhece** as 4 classes — gravar `breakthrough` ali quebra o insert. Por isso o perf JSON leva os dois campos, com este mapeamento fixo:

   | `ad_class` (canônico) | `outcome` (legado, pro registry) |
   |---|---|
   | `breakthrough` | `winner` |
   | `spend_winner` | `neutral` |
   | `kpi_winner` | `neutral` |
   | `loser` **com pelo menos 1 purchase no período** | `loser` |
   | `loser` **sem nenhuma purchase no período** | `zero_conversions` |
   | `unclassified` (ainda em aprendizado / sem `campaign_cpa` estável / análise DIRECIONAL do gate de piso — PLAYBOOK item 6) | `insufficient_data` |
   | criativo em FUNIL QUEBRADO (não foi ele que falhou) | `neutral` |

   `spend_winner` e `kpi_winner` vão pra `neutral` de propósito: nenhum dos dois é evidência de acerto, e marcá-los como `winner` envenenaria as correlações de feature que o `dna-profile.json` calcula — exatamente o falso positivo que esta correção elimina. Sinal forte de breakthrough: spend > $300 E decile_rank 1-2.

   O desdobramento do `loser` em dois destinos existe porque **`zero_conversions` é o negativo mais forte do enum legado** e o registry precisa dele: gastou e não converteu nenhuma vez é um sinal de aprendizado cross-product mais nítido que "converteu mal". O que separa as duas linhas é só a contagem de purchases do período analisado: zero ou não. **Nenhum corte de spend entra nesta gravação** — quanto o criativo precisa gastar antes de ser morto é a régua de kill do cânone §3, decisão separada, tomada antes e por outro motivo. Esta é a MESMA conversão que a receita `sync-campaign-from-meta.md` aplica no `to_legacy_outcome()` dela; os dois escritores do registry usam o mesmo vocabulário, senão o mesmo criativo entra no banco com rótulo diferente conforme quem gravou.

2. Compor performance JSON:
   ```json
   {
     "cpa": 38.5, "ctr": 1.4, "roas": 2.6, "spend": 412.0,
     "thumbstop_3s": 0.31, "hold_15s": 0.12,
     "impressions": 48210, "clicks": 675, "purchases": 11,
     "days_active": 7, "decile_rank": 2,
     "ad_class": "breakthrough|spend_winner|kpi_winner|loser|unclassified",
     "outcome": "winner|loser|neutral|zero_conversions|insufficient_data"
   }
   ```
   Os números do exemplo são ilustrativos — grave os medidos deste criativo. `thumbstop_3s` recebe o **hook rate** (3-second plays ÷ impressões) e `hold_15s` recebe o **hold rate** (ThruPlays ÷ impressões), medidos na ETAPA 2 — os dois nomes de campo são legados do registry, o conteúdo é o do cânone §4. Criativo estático: `null` nos dois. Nunca grave esses campos vazios: sem eles o `dna-profile.json` não consegue correlacionar abertura e retenção com resultado.

3. Salvar em `workspace/[produto]/creative-dna/perf-[creative-id].json`

4. Invocar silenciosamente:
   ```
   python3 .claude/lib/creative-dna/registry.py update workspace/[produto] [creative-id] workspace/[produto]/creative-dna/perf-[creative-id].json
   ```

5. Se total de criativos com performance ≥ 10 E (total atual % 5 == 0):
   ```
   python3 .claude/lib/creative-dna/registry.py dna workspace/[produto] --product [slug]
   ```
   Atualiza `workspace/[produto]/creative-dna/dna-profile.json` que será usado na próxima Skill `creative-engine`.

Silent. Membro não vê. Apenas o efeito: próximo briefing começa a refletir padrões aprendidos.

### PII redaction (antes de salvar qualquer dump de Ads Manager)

Antes de persistir dados em `workspace/`:
- Substituir Account IDs por `ACC-[hash 8 chars]`
- Substituir Pixel IDs por `PX-[hash 8 chars]`
- Remover emails em UTM/audience names (regex `[\w.+-]+@[\w.-]+\.\w+` → `[EMAIL_REDACTED]`)
- Remover telefones em audience names (regex `\+?\d{10,15}` → `[PHONE_REDACTED]`)
- Nota: manter hash dos IDs consistente entre execuções para correlacionar análises
