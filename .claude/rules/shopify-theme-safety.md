---
name: shopify-theme-safety
description: Regras inegociáveis pra qualquer operação em theme Shopify (pull, push, deploy, edit). Aplica na skill 07b-page-build (deploy da página), 07c-tracking-setup e 07d-checkout-aov (config de loja/checkout) e qualquer automação que toque tema LIVE.
paths:
  - .claude/skills/07b-page-build.md
  - .claude/skills/07c-tracking-setup.md
  - .claude/skills/07d-checkout-aov.md
  - .claude/skills/14-content-recycler.md
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

1. O marker de build é um ATRIBUTO DE DADOS no elemento raiz da section: `data-aura-build="<slug>-<hash8>"` (a skill 07b já gera esse atributo no compile). **NUNCA use comentário Liquid `{% comment %}` como marker de verificação** — o renderizador Liquid remove o bloco e ele jamais chega ao HTML servido, então o grep falharia SEMPRE, mesmo com push 100% ok. (Um comentário Liquid pode existir como marca no código-fonte do tema, verificável via `shopify theme pull` — mas a verificação pós-deploy usa o data-attribute, que renderiza no DOM.)
2. Após push, rode `curl -s "https://<shop>.myshopify.com/products/<handle>?preview_theme_id=<id>" | grep data-aura-build`
3. Se grep encontra o marker (e o hash bate com o build atual) → push OK, seguro pullar
4. Se grep NÃO encontra → push rejeitado silenciosamente, investigar (rate limit? theme lock? compile error?) antes de qualquer pull
5. O atributo é inerte e identifica o build — NÃO precisa ser removido depois (sem re-push de limpeza)

## Regra 5 — Silent push rejection diagnosis

Push silenciosamente rejeitado é cenário comum. Checklist de diagnóstico:

| Sintoma | Causa provável | Fix |
|---------|----------------|-----|
| `data-aura-build` não aparece no storefront após push "ok" | Theme lock ativo (outro CLI/editor aberto) | Fechar sessões duplicadas, retry |
| `data-aura-build` não aparece + erro 429 em curl | Rate limit Shopify CLI | Esperar 60s, retry |
| `data-aura-build` aparece mas CSS/JS quebrado | Compile error silencioso | `shopify theme check` local antes de re-push |
| `data-aura-build` aparece intermitentemente | CDN propagation (raro, mas acontece) | Esperar 120s e re-verificar |
| `data-aura-build` aparece mas com hash ANTIGO | Push subiu versão stale (arquivo local errado) | Recompilar a section e re-push |
| Push ok mas UM arquivo específico continua na versão antiga (marker/mudança ausente só nele) | Conteúdo do arquivo rejeitado por validação silenciosa no servidor da Shopify — casos conhecidos: setting `richtext` com default sem `<p>…</p>`, setting `text` com default vazio `""` | Bisection de settings (cortar pela metade até isolar): remova metade dos defaults, pushe, confira; repita até isolar o campo; corrija o default (richtext SEMPRE `<p>…</p>`) e re-pushe |
| Push retorna warning "live theme" sem confirmar | Faltou `--allow-live` | Re-push com flag correto |
| Deploy que funcionava quebra com "command not found" / flag inválida | **Auto-upgrade do Shopify CLI 4.x** (ver nota abaixo) | Checar `shopify version` + changelog do CLI antes de debugar o tema |

Nunca assuma sucesso baseado apenas em exit code 0.

**Nota — auto-upgrade do Shopify CLI 4.x (mai/2026+):** a CLI se atualiza sozinha via package manager entre sessões e a série 4.x removeu comandos/flags legados. Se um deploy que funcionava ontem quebra hoje com "command not found" ou flag inválida, o primeiro suspeito é upgrade automático da CLI — NÃO o tema. Rode `shopify version`, compare com o changelog oficial, e só depois debug o tema. A skill 07b já loga `shopify version` no início do deploy (ETAPA 6.1 da 07b) exatamente pra esse diff ser trivial.

## Regra 6 — Backup antes de qualquer edit massivo

Antes de editar ≥ 3 arquivos de section ou qualquer template crítico (`theme.liquid`, `product.json`, `cart.json`):

O backup precisa ser uma cópia do tema **LIVE** — nunca do estado local (que pode estar stale). Dois caminhos:

**Caminho A — via CLI** (pull do live pra um diretório temporário, depois push desse diretório pra um tema novo unpublished):

```bash
shopify theme pull --live --path=<tmp-backup-dir> --nodelete
shopify theme push --unpublished --path=<tmp-backup-dir> --theme "BACKUP-<data>-pre-edit"
```

**ATENÇÃO:** rodar `shopify theme push --unpublished` direto no diretório de trabalho NÃO é backup — isso sobe o estado LOCAL pra um tema novo, não o live que você quer proteger. E redirecionar o output com `> backup.json` grava só o metadata JSON do CLI (id/nome do tema), não os arquivos.

**Caminho B — manual:** Admin → Themes → ⋯ → Duplicate. Nomear como `BACKUP-<data>-pre-edit`.

Em ambos os casos, o duplicado fica como rollback point.

## Regra 6b — NUNCA regenerar template JSON por cima do que está no ar

`templates/*.json` guarda **o que o membro configurou no theme editor**: fotos escolhidas em `image_picker`, textos editados, ordem dos blocks, variant IDs preenchidos. Regenerar esse arquivo a partir dos presets das sections e pushar **apaga tudo isso em silêncio** — a página volta pros defaults e o membro descobre pelas fotos que sumiram.

**Proibido:** montar `templates/index.json` do zero (a partir de `presets`) e pushar por cima.

**Fluxo correto** ao adicionar, remover ou reordenar section:

```bash
shopify theme pull --theme "$ID" --store "$STORE" --path "$DIR" --nodelete --only "templates/index.json"
python3 tools/theme-template-merge.py "$DIR/templates/index.json" --add faq:page-produto-faq --after hero
shopify theme push --theme "$ID" --store "$STORE" --path "$DIR" --nodelete --only "templates/index.json"
```

O merge preserva byte a byte as sections existentes e mexe só no pedido. Mudança apenas em markup/schema de section (`sections/*.liquid`) ou em assets **não exige tocar no template** — pushe só os arquivos alterados com `--only`.

**Regra prática:** antes de qualquer push que inclua um template JSON, rode o merge a partir do pull mais recente. Se o push não precisa do template, não inclua o template.

## Regra 6c — Temas paralelos com paletas diferentes (arquivo de identidade é POR-TEMA)

Quando a loja mantém 2 ou mais temas com identidades visuais diferentes (A/B test de paleta, tema de campanha sazonal), o snippet ou asset que carrega os tokens de cor é DIFERENTE em cada tema **mesmo tendo o MESMO nome de arquivo**. Exemplo: `snippets/sec-tokens.liquid` define `--sec-bg: rgb(246, 245, 241)` (areia) no tema A e um fundo grafite no tema B — mesmo path, conteúdo divergente por design.

**O erro que esta regra previne:** um push em lote genérico manda o arquivo de identidade do tema A por cima do tema B. Como esse arquivo alimenta a paleta da página inteira, o tema PUBLICADO muda de identidade completa num único push, e o membro descobre pela loja no ar.

**Protocolo:**

a) Antes de qualquer push que inclua o arquivo de identidade, declarar explicitamente QUAL paleta pertence ao tema alvo.

b) Fluxo de atualização em par: regenerar o arquivo com a paleta do tema B → push SÓ desse arquivo pro tema B (`--allow-live` se for o publicado) → restaurar a versão do tema A no diretório de trabalho local antes de continuar:

```bash
shopify theme push --theme "$ID_B" --store "$STORE" --path "$DIR" --nodelete --only "snippets/sec-tokens.liquid"
```

c) Push em lote (`--only` com vários arquivos, ou push sem `--only`) NUNCA inclui o arquivo de identidade quando há 2+ temas divergentes — ele sai do lote e vai em push próprio por tema.

d) Em caso de troca acidental: re-push imediato da paleta correta. O arquivo local certo é a fonte; se ele se perdeu, `shopify theme pull` do tema certo ANTES de qualquer novo push.

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
- Rate limits: bucket de 40 requests, vazão sustentada de 2 req/s (Admin API REST, modelo leaky bucket)
