# Promo Engine · Referência: Estrutura de campanha da janela (ETAPA 5)

> A campanha única com os três ad sets e a tabela das audiências, o budget da janela pela exceção do cânone, as três regras de estrutura e a execução opcional por MCP com tudo nascendo pausado. Abra na ETAPA 5.

### ETAPA 5 — Estrutura de campanha da janela

Rode **Promo Campaign (Broad / WARM60 / HOT90)** (`promo campaign CBO três ad sets broad WARM60 HOT90 retargeting só em sale`) e **Full Media Buying 2026** (`estrutura full media buying 2026 cinco camadas main CBO ABO zombie raw content promo` — a Promo CBO é a camada satélite que só nasce com data de fim; quem monta é esta skill, nunca a `ad-strategy`).

**A estrutura (a única ocasião de retargeting do sistema):** fora de sale, retargeting não paga; em sale, o público quente tem urgência real e merece frequência alta. **1 campanha CBO, 3 ad sets:**

| Ad set | Audiência | Detalhe |
|---|---|---|
| **Broad** | só idade, gênero e país | sem lookalike, sem interesse |
| **WARM60** (meio de funil) | engajadores da página do FB 60d + engajadores do IG 60d + 95% video viewers 60d (todos os vídeos com 1.000+ views) | **excluindo** as audiências do HOT90 |
| **HOT90** (fundo de funil) | visitantes do site, view content, add to cart, initiate checkout — 90 dias | — |

Audiências em Audiences → Create Audience → Custom Audience (fontes: página do FB / conta do IG / vídeo / site), retenções 60/90. CBO com budget alto — o Meta aloca onde performa (a estrutura levou contas de US$ 10k pra US$ 70k/dia em 24h na fonte). **O evergreen continua rodando em paralelo, sempre** — a promo é um sistema paralelo temporário; criativos de sale ficam NA campanha de promo (não misturar com os post IDs do evergreen).

**Budget da janela (cânone §5, exceção (a) — cite, não redefina):** promo com data-fim **entra direto no budget planejado** — não sobe em degraus de +20%, porque a janela termina antes de os degraus chegarem lá. O que protege a promo é o **surf + o reset da meia-noite** (ETAPA 8). Referências da fonte pro tamanho inicial: **não há fórmula** — até ~10% do spend diário total é conservador e ok; no máximo ~50% se extremamente confiante; num dia de US$ 100k de spend, a referência citada foi US$ 25k evergreen + US$ 75k promo (no pico, com a promo provada). De quinta pra sexta **não dobre preventivamente** "porque é Black Friday" — mantenha e escale intraday quando os dados aparecerem. Rode `promo campaign separada do evergreen timing início de novembro budget inicial 10 por cento conservador 50 máximo realocação`.

Mais três regras de estrutura da fonte: 1 campanha de promo + 1 evergreen (+ promo por país, se multi-país) — **não** pulverizar em campanhas separadas por formato (dilui e derruba o retorno); produto de ticket muito diferente ganha campanha própria (objetivo diferente pro algoritmo); e a campanha nomeada com o nome da sale + ano, seguindo a convenção de nomes da `ad-strategy`.

**Execução opcional via Meta MCP (mesma cascade da `ad-strategy`/`scale-engine`):** oficial `mcp__meta__ads_*` → Pipeboard `mcp__meta-ads__*` → manual (detecção por prefixo, `.claude/lib/mcp-detect/README.md`). Criar campanha + 3 ad sets + audiências em `status: PAUSED` — **o membro revisa e ativa; a skill NUNCA ativa nada sozinha.** A automated rule de fim de janela (ETAPA 9) nasce DESATIVADA pro membro revisar e ativar antes do fim. Falha de API → `emergency-escape-paths.md` ES6. Sem MCP → passo a passo manual campo a campo. IDs criados em `dados.json.campaigns[]` e **linha no `ad-log.md` na mesma execução** ("criado em PAUSED", executor `skill-promo-engine`, motivo "promo início — [evento]").
