---
name: shopify-theme-safety
description: Regras inegociáveis pra qualquer operação em theme Shopify (pull, push, deploy, edit). Aplica nas skills 06, 06c e qualquer automação que toque tema LIVE.
paths:
  - .claude/skills/06a-page-planning.md
  - .claude/skills/06b-page-sections.md
  - .claude/skills/06c-page-deploy.md
  - .claude/skills/17-content-recycler.md
---

# Shopify Theme Safety (NON-NEGOTIABLE)

Applica a **toda** operação Shopify CLI contra tema live (`--live`, `--theme`, `--allow-live`). Membros do Aura Engine não são devs Shopify — a skill carrega toda responsabilidade de não quebrar loja em produção.

## Regra 1 — Pull antes de qualquer edit

Antes de modificar **um único arquivo** do tema local, rode:

```bash
shopify theme pull --live --path=<theme-clone-dir> --nodelete
```

**Motivo:** o tema live pode ter sido editado via theme editor pelo membro, por app instalado (Judge.me, Klaviyo, Loox, Shop Pay), ou por outro colaborador desde o último pull. Editar sem pull = sobrescrever essas mudanças no próximo push.

**Exceção:** se o pull já foi feito há menos de 10 minutos E nenhum push ocorreu entre pull e edit, pode pular. Caso contrário, SEMPRE pull.

## Regra 2 — Sempre usar `--nodelete` em pull

O flag `--nodelete` impede que o pull remova localmente arquivos que não existem no tema remoto. Isso protege arquivos locais recém-criados (nova section Liquid, snippet custom) que ainda não foram pushados.

```bash
shopify theme pull --live --path=<dir> --nodelete
```

**NUNCA** use pull sem `--nodelete` num workflow ativo. Pull destrutivo só em cenário de reset deliberado.

## Regra 3 — Pra push: `--allow-live` + `--nodelete`

Ao subir mudanças pro tema live:

```bash
shopify theme push --live --path=<dir> --allow-live --nodelete
```

**Por que `--nodelete` no push também:** se localmente alguém deletou um arquivo por acidente (comum depois de git reset, merge conflict mal resolvido, ou checkout de branch), push sem `--nodelete` vai deletar o arquivo remoto também. Com `--nodelete`, arquivos faltantes localmente permanecem no remoto.

Pra deletar intencionalmente um arquivo no remoto, fazer delete separado via Admin API ou CLI delete command explícito.

## Regra 4 — NUNCA pull depois de push não verificado

Se você acabou de rodar `shopify theme push` e o comando retornou sem erro MAS você não verificou que as mudanças subiram (via curl no storefront, ou via admin check), **NÃO** rode pull imediatamente depois.

**Motivo:** pushes Shopify podem ser silenciosamente rejeitados (rate limiting, theme lock, rollback automático). Se você pull após push rejeitado, o tema remoto antigo sobrescreve suas mudanças locais — trabalho perdido.

**Verificação obrigatória antes de pull pós-push:**

1. Insira um marker único no arquivo editado antes do push — comentário Liquid `{%- comment -%}AURA-PUSH-MARKER-{timestamp}{%- endcomment -%}` no topo da section
2. Após push, rode `curl -s https://<shop>.myshopify.com/products/<handle>?preview_theme_id=<id> | grep AURA-PUSH-MARKER`
3. Se grep encontra o marker → push OK, seguro pullar
4. Se grep NÃO encontra → push rejeitado silenciosamente, investigar (rate limit? theme lock? compile error?) antes de qualquer pull
5. Após confirmar, remover o marker do arquivo local E rerun push (limpeza)

## Regra 5 — Silent push rejection diagnosis

Push silenciosamente rejeitado é cenário comum. Checklist de diagnóstico:

| Sintoma | Causa provável | Fix |
|---------|----------------|-----|
| Marker não aparece no storefront após push "ok" | Theme lock ativo (outro CLI/editor aberto) | Fechar sessões duplicadas, retry |
| Marker não aparece + erro 429 em curl | Rate limit Shopify CLI | Esperar 60s, retry com `--force` |
| Marker aparece mas CSS/JS quebrado | Compile error silencioso | `shopify theme check` local antes de re-push |
| Marker aparece intermitentemente | CDN propagation (raro, mas acontece) | Esperar 120s e re-verificar |
| Push retorna warning "live theme" sem confirmar | Faltou `--allow-live` | Re-push com flag correto |

Nunca assuma sucesso baseado apenas em exit code 0.

## Regra 6 — Backup antes de qualquer edit massivo

Antes de editar ≥ 3 arquivos de section ou qualquer template crítico (`theme.liquid`, `product.json`, `cart.json`):

```bash
# Duplicate theme no admin antes do pull local
# Via Shopify CLI:
shopify theme push --unpublished --path=<dir> --json > backup-<timestamp>.json
```

Ou manualmente: Admin → Themes → ⋯ → Duplicate. Nomear como `BACKUP-<data>-pre-edit`. Esse duplicado fica como rollback point.

## Regra 7 — Após deploy, smoke test obrigatório

Depois de push bem-sucedido, rodar smoke test automático antes de notificar membro "tá no ar":

1. `curl -sI https://<shop>/products/<handle>` → esperar 200
2. `curl -s https://<shop>/products/<handle> | grep -E "(404|500|Liquid error)"` → esperar zero matches
3. Verificar cart endpoint: `curl -sI https://<shop>/cart.js` → esperar 200
4. Verificar que SVG/fonts/assets custom carregam (curl no asset URL)

Se qualquer smoke test falha, rollback automático pro BACKUP duplicado (Regra 6) e reportar ao membro antes de tentar de novo.

## Regra 8 — Proibido pra sempre

- `shopify theme push --live` sem `--allow-live` (bloqueado pela CLI, mas agent NÃO deve tentar bypassar)
- `shopify theme push` sem explicit `--path` (risco de pushear diretório errado)
- `rm -rf theme-clone/` sem backup de hot-fix locais não-commitados
- Edits diretos em `theme.liquid` sem pull recente (Regra 1)
- Pulls em loop pra "monitorar" mudança remota — usa webhook ou Admin API check, não pull
- Editar `product.json` ou `cart.json` sem entender que esses templates afetam 100% da loja, não uma PDP específica

## Referências

- `shopify theme --help`
- Shopify theme check: `shopify theme check --path=<dir>`
- Rate limits: 2 req/s burst, 40 req/min sustained (Shopify CLI)
