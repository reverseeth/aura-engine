# Page Build · Referência: VALIDATE e validação do template JSON populado (ETAPAs 3 e 4)

> O protocolo de 3 tentativas com o `shopify-plugin:shopify-liquid` (ETAPA 3), o modelo de blocks vs settings, a checklist do template JSON, o snippet de validação cruzada contra os schemas dos `.liquid` e o check bloqueante de imagens do mapa de mídia e de placeholders textuais residuais (ETAPA 4). Abra nas ETAPAs 3 e 4.

## ETAPA 3 — VALIDATE (shopify-plugin:shopify-liquid, 3 retries)

Cada `.liquid` gerado passa pelo skill `shopify-plugin:shopify-liquid` (modo validate). Protocolo determinístico (3 tentativas):

1. **Validate** — se OK, próxima section.
2. **Auto-fix + revalidate** — modo `fix` do plugin, revalida.
3. **Leitura manual do erro** — consulte a tabela **Debug — Quando validação falha** (abaixo), aplique o fix, revalide. Se ainda falhar → **PARE e reporte** ao membro (arquivo, erro exato, tentativas, ação manual sugerida).

Se o plugin estiver indisponível, **instale antes de seguir** (`/plugin marketplace add Shopify/shopify-ai-toolkit` + `/plugin install shopify-plugin@shopify-plugin`) — não existe fallback manual confiável; validar Liquid "no olho" é exatamente o modo de falha que esta skill elimina.

## ETAPA 4 — Validação do template JSON populado

O POPULATE já aconteceu na ETAPA 2 (o `--emit-template-json`/batch monta o `templates/page.[produto].json` com `blocks{}` + `block_order[]` + `settings{}` populados, usando a copy real do HTML como `default` de cada setting). Esta etapa valida o resultado — não re-roda o conversor.

**Modelo de blocks vs settings:** o conversor emite conteúdo ÚNICO (hero headline, eyebrow, sub, CTA único) como **section settings** (grupo Content — editável no theme editor) e conteúdo REPETÍVEL (benefit cards, pricing tiers, review cards, FAQ items, ingredients, steps) como **blocks** arrastáveis/reordenáveis, com UMA instância por item real do HTML (FAQ de 5 perguntas = 5 instâncias distintas). Sections monolíticas (só settings) são válidas e comuns (ex: hero).

**Erro #1 histórico (vale só pra sections COM blocks):** quando uma section É block-based (schema define block types repetíveis), o `templates/page.[produto].json` precisa ter `blocks: {...}` + `block_order: [...]` EXPLÍCITOS — senão renderiza ZERO daqueles blocks (o Shopify só popula preset blocks quando o membro adiciona a section manualmente via "Add section"). O POPULATE resolve isso. Sections monolíticas (settings-only) legitimamente têm `blocks: {}` e renderizam do markup direto.

Notas pra ajustes manuais no JSON:
- **Inserção em ordem reversa** (rule `reverse-order-insertion`): quando o Claude insere múltiplas sections no `order[]`/`sections{}` à mão, insere da maior posição pra menor pra não deslocar índices. No modo batch/merge o conversor já cuida disso.
- As cores das section settings vêm de `design-tokens.json` (role-tagged: background/surface/foreground/primary/accent/border).

### Validação do template JSON (OBRIGATÓRIA antes do deploy)

Pra cada section em `sections`:
- [ ] Se a section é **block-based** (schema do `.liquid` define block types), `blocks` é objeto **não-vazio** com `block_order`. Sections **monolíticas** (só settings, ex: hero) legitimamente têm `blocks: {}` — não é erro (o snippet abaixo já distingue os dois casos)
- [ ] `block_order` referencia apenas chaves de `blocks`; todo block de `block_order` existe em `blocks`
- [ ] Todo block tem `type` válido presente no schema da section `.liquid` correspondente
- [ ] `order[]` lista todas as sections na sequência persuasiva (`section_order` de `page-plan.json`)
- [ ] Copy REAL populada (hero headline, sub, CTAs, stats, benefits VOC, tiers, FAQ Q+A, CTA final) — tudo de `copy-engine`
- [ ] **Se `page_type = advertorial` ou `listicle`:** o href dos soft CTAs aponta pro destino de `page-plan.json.destination_ref` (a `page-design` define obrigatoriamente: handle/URL da pdp_lean de 2ª passada, PDP existente trabalhada, ou checkout direto). Os dois são pré-lander — o soft CTA é `<a href>` de navegação pro destino, NUNCA form `/cart/add` (o fechamento acontece na página de destino). Se `destination_ref` estiver `null` num dos dois, PARE e mande o membro de volta pra `page-design` ETAPA 1 — pré-lander no ar com CTA sem destino manda tráfego pago pro vazio.

Snippet de validação cruzada (roda antes de todo push — cruza template JSON contra os schemas dos `.liquid`):

```python
import json, re
from pathlib import Path
PRODUTO = "[slug]"
STAGING = Path(f"workspace/{PRODUTO}/page/staging")
TEMPLATE_JSON = STAGING / "templates" / f"page.{PRODUTO}.json"
SECTIONS_DIR = STAGING / "sections"
data = json.loads(TEMPLATE_JSON.read_text(encoding="utf-8"))
errors = []
section_block_types = {}
for lf in SECTIONS_DIR.glob("*.liquid"):
    m = re.search(r"\{% schema %\}(.*?)\{% endschema %\}", lf.read_text(encoding="utf-8"), re.DOTALL)
    if not m: continue
    try: schema = json.loads(m.group(1).strip())
    except json.JSONDecodeError:
        errors.append(f"{lf.name}: schema JSON invalido"); continue
    section_block_types[lf.stem] = {b["type"] for b in schema.get("blocks", [])}
for sid, section in data["sections"].items():
    st = section.get("type"); blocks = section.get("blocks", {}); order = section.get("block_order", [])
    allowed = section_block_types.get(st, set())  # block types definidos no schema do .liquid
    # Section monolitica (schema SEM blocks) pode ter blocks vazio — conteudo unico vive em settings.
    # So e erro se o schema DEFINE blocks (conteudo repetivel: cards/tiers/reviews/faq) mas o template nao populou.
    if allowed and not blocks: errors.append(f"{sid} ({st}): schema define blocks mas template tem blocks vazio — 0 blocks renderizados")
    if blocks and not order: errors.append(f"{sid} ({st}): tem blocks mas block_order ausente")
    for bk in order:
        if bk not in blocks: errors.append(f"{sid}: block_order referencia '{bk}' inexistente")
    for bk, bi in blocks.items():
        bt = bi.get("type")
        if allowed and bt not in allowed:
            errors.append(f"{sid}.{bk}: type '{bt}' nao existe no schema de '{st}' (allowed: {sorted(allowed)})")
for sid in data.get("order", []):
    if sid not in data["sections"]: errors.append(f"order: '{sid}' nao existe em sections")
if errors: print("\n".join(errors)); raise SystemExit(1)
print(f"Template JSON valido: {len(data['sections'])} sections, order OK.")
```

Se qualquer erro → **ABORTE o push**, corrija (adicione o block type faltante no `.liquid` via re-COMPILE, ou corrija o template JSON).

### Check bloqueante — imagens e placeholders residuais (roda junto da validação acima)

Dois vazamentos históricos que esta validação mata antes do deploy: página no ar com slot de imagem vazio, e placeholder de template (`{{TESTIMONIAL_1}}`, `{{IMAGE_URL}}`) renderizando literal pro consumidor.

**1. Imagens do mapa de mídia (bloqueante).** Leia `page-plan.json.sections_plan[].media` — e, com `page_type: quiz`, também o `media` de cada tela em `page-plan.json.quiz.screens[]`, que obedece às mesmas duas regras abaixo:
- Qualquer section com `media.status: "placeholder"` → **BLOCK**: o plano de obtenção da `page-design` não foi cumprido. Fix paths (ES1-style): **(A)** membro fornece a imagem agora (salvar em `design/assets/`, atualizar o HTML aprovado + re-COMPILE da section, ou subir via admin → Files e apontar a setting), ou **(B)** voltar à `page-design` ETAPA 1.6 pra redecidir a mídia daquela section (ex: rebaixar pra `required: false` se a section vive de ícone). Não existe path (C) "deploya assim mesmo".
- Pra toda section com `media.required: true` e `status: "ready"`: confira que a setting de imagem correspondente no template JSON não está vazia (valor `shopify://shop_images/...` ou asset real). Setting `image_picker` vazia numa section que exige imagem = **BLOCK** com os mesmos fix paths. (Plano legado sem campo `media`: aplique o check no mínimo ao hero — hero sem imagem em landing/pdp é sempre erro.)

**2. Placeholders textuais residuais (bloqueante).** Liquid legítimo usa minúsculas com namespace (`{{ section.settings.x }}`); placeholder de template usa MAIÚSCULAS (`{{TESTIMONIAL_1}}`). Grep obrigatório:

```bash
grep -rnE '\{\{ ?[A-Z][A-Z0-9_]* ?\}\}' "${STAGING_DIR}/sections" "${STAGING_DIR}/templates" && echo "BLOCK: placeholder residual"
```

Qualquer match → **BLOCK**: substitua pelo conteúdo real da `copy-engine` (testimonial/copy de verdade) ou remova o elemento se o conteúdo não existe (nunca inventar um depoimento pra preencher). Zero matches = prossegue.
