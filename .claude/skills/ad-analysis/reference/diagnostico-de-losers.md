# Ad Analysis · Referência: Diagnóstico profundo de losers (ETAPA 4)

> O 19-Point Loser Diagnostic em cinco camadas (targeting, hook, copy, oferta, técnico) e o diagnóstico de valência da iteração que trocou de zona emocional (`iteration_zone_check`). Abra na ETAPA 4.

### ETAPA 4 — Diagnóstico Profundo de LOSERS (19-Point Diagnostic)

Roda pra todo criativo com `ad_class` = `loser`. Roda **também** pra `kpi_winner` (que é loser para decisão) e pra `spend_winner` — nos dois casos a pergunta muda: no `kpi_winner`, por que ele não puxou spend (hipótese primária: audiência pequena demais); no `spend_winner`, por que o KPI ficou abaixo do da campanha apesar do volume.

### 19-Point Loser Diagnostic

**Camada 1: Targeting (4 pontos) — só se aplica a estruturas CUSTOM.** A estrutura padrão da `ad-strategy` é broad/Advantage+ sem exclusões e sem lookalike — nela, pule direto pra Camada 2. Use esta camada só se o membro montou targeting manual por fora do fluxo.
1. Audience muito broad — CTR alto, CVR baixo
2. Audience muito narrow — CPM alto, volume baixo
3. Exclusões conflitantes (ex: excluir compradores mas campaign é de aquisição — conflito)
4. Lookalike source com baixa qualidade (seed < 500 de alta qualidade)

**Camada 2: Hook (4 pontos)** — entre nesta camada **com os números de Hook e Hold já medidos** (bloco da ETAPA 2). Hook baixo confirma que a falha é aqui; hook bom com hold baixo joga o diagnóstico pra Camada 3 (a promessa do hook não foi sustentada pelo corpo). Pra loser que **gastou sem vender**, a ordem do diagnóstico é sistema nomeado da base: **Diagnóstico de Spend Sem Venda** (rode `spend sem venda hook traz gente errada beliefs gradualization average watch time`) — primeiro cheque se o hook está trazendo a **pessoa errada** (spend e clique com zero intenção), só depois a camada de crenças/gradualization; o **average watch time** é o sinal que separa os dois casos.
5. Hook não promete ganho específico
6. Hook sem pattern interrupt visual (3 primeiros segundos)
7. Hook não casa com awareness stage dominante
8. Hook saturado (claim idêntico a 5+ concorrentes)

**Camada 3: Copy (4 pontos)**
9. Primary text > 125 chars (corta em mobile)
10. CTA vago ("saiba mais" vs "ativar desconto 30%")
11. Zero social proof específico
12. Benefício listado sem transformação (feature, não benefit)

**Camada 4: Offer (4 pontos)**
13. Preço quebra o budget do awareness stage
14. Garantia fraca ou ausente
15. Urgência artificial óbvia
16. Bundle não faz sentido para o público

**Camada 5: Técnico (3 pontos)**
17. EMQ < 6/10 (Event Match Quality do Events Manager — gate canônico da `tracking-setup` é ≥ 6.0)
18. Landing page carrega > 3s (mobile)
19. Mismatch ad → landing (visual/copy)

Pra cada loser, identifique **a camada onde falhou** e a hipótese específica. Documente.

### Diagnóstico de valência — iteração que trocou de zona (`iteration_zone_check`)

Roda pra **toda iteração que fracassou** (criativo cujo conceito nasceu de `NEXT_BATCH_IDEAS.md` ou é iteração declarada — `testing_method: "sniper"` de batch derivado). **Quem é o original:** leia `concepts[].iteration_of` da `creative-engine` (creative_id do original — a linhagem declarada); só quando o campo não existe (batch legado), paree original↔iteração pela prosa do briefing, como sempre. Compare, em `creative-engine/dados.json`, a zona emocional do ORIGINAL vs a da ITERAÇÃO — `valence` × `intensity` de abertura (do conceito e do hook) e o arco `valence_open` → `valence_close`:

- **Zona igual, elemento iterado diferente** → a variável testada explica o resultado; o diagnóstico segue nas camadas do 19-point.
- **Zona MUDOU** (ex: a iteração abre em negative/high onde o original abria em positive/low) → a iteração **trocou de zona emocional sem perceber** — o flop inexplicável que a `creative-engine` (ETAPA 4.5.E) documenta: trocou a palavra, trocou junto o sentimento, e o ad deixou de falar com o mesmo estado emocional. A causa provável do fracasso é a ZONA, não o elemento editado; a diretiva pro próximo batch é refazer a iteração **na zona original**, mudando só a variável pretendida.

Registre em `iteration_zone_check[]` no `dados.json` (um item por iteração analisada): referência do original e da iteração, as duas zonas, `zone_changed` e o veredito. **Fallback legado:** original ou iteração sem `valence`/`intensity` gravados (batch anterior ao schema da `creative-engine`) → registre `"unknown"` no lado sem dado e **não conclua troca de zona** — o item sai com `verdict: "no_data"`.
