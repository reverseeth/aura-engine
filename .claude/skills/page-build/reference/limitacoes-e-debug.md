# Page Build · Referência: Referência técnica, limitações Shopify conhecidas e debug

> As dezoito limitações do Shopify que o conversor e a validação respeitam (incluindo a rejeição silenciosa de `richtext` sem `<p>` e o filtro encadeado em argumento nomeado) e a tabela de debug quando validação ou push falha. Abra na ETAPA 3 e em qualquer erro de push.

## Limitações Shopify conhecidas (o conversor + validação respeitam)

1. `<img>` precisa `width`+`height` — usar `image_tag` (auto-adiciona): `{{ image | image_url: width: 1600 | image_tag: loading: 'lazy' }}`.
2. `url` setting não aceita `#anchor` como default — só `http(s)://` ou `/path/`. Deixe default vazio.
3. `inline_richtext` não aceita attributes em tags — só `<em>`, `<strong>`, `<br>`, `<span>`, `<a>`, `<u>`, `<p>` sem attrs.
4. `richtext` wrapa em `<p>` automático — não envolva em `<p>` no markup (evita `<p><p>`).
5. Aspect-ratio: use `data-adapt="true"` + seletor `[data-adapt='true']` (o conversor já faz).
6. Dropdown "Theme template" do admin Pages só lista templates do tema LIVE.
7. `shopify theme duplicate` precisa `--force` em contexto não-interativo.
8. Package-lock do plugin aponta pro registry privado `npm.shopify.io` — se `validate.mjs` falha com `ERR_MODULE_NOT_FOUND`, rode no dir do plugin: `rm package-lock.json && npm install --registry=https://registry.npmjs.org/`.
9. Range settings: max 101 steps. `(max - min) / step ≤ 100`.
10. Range default deve alinhar ao step: `(default - min) % step == 0`.
11. **Preset de section ≠ blocks em template JSON.** Section entry sem `blocks` (ou `blocks: {}` vazio) renderiza ZERO blocks. O POPULATE (ETAPA 4) resolve isso emitindo `blocks: {...}` + `block_order: [...]` explícitos.
12. Blocks inline (`{% case block.type %}`) passa; theme blocks em `/blocks/*.liquid` com `{% content_for 'block' %}` dinâmico FALHA.
13. `inline_richtext` renderiza HTML no browser mas o preview editor pode mostrar raw — use `info` no setting.
14. Custom Liquid em block: `type: "liquid"` (pré-renderiza no push); `type: "html"` é estático XSS-safe.
15. `shopify page create` não existe na CLI — a criação da página é o passo 6.6 do DEPLOY (membro no admin, com handle exatamente `[produto]`, ou `pageCreate` via Admin API/MCP quando conectado). Sem a página criada, o storefront responde 404 (não é falha de push); o theme editor URL (`?template=page.[produto]`) roda mesmo sem a página existir.
16. **Default de `richtext`/`inline_richtext` sem `<p>` = arquivo inteiro rejeitado em silêncio.** O valor default de um setting `richtext` no schema (e o valor correspondente em template JSON) PRECISA ser `"<p>...</p>"` — texto puro faz o Shopify rejeitar O ARQUIVO INTEIRO em silêncio: o push reporta ok, o servidor mantém a versão velha, e nenhum erro de validação aparece. Mesmo sintoma pra setting `text` com default `""` (use ausência de default). Diagnóstico: bisection de settings — remova metade dos defaults, pushe, confira o marker `data-aura-build`; repita até isolar o campo culpado.
17. **Filtro encadeado DENTRO de argumento nomeado quebra o Liquid em runtime.** `style: 'x' | append: var | append: 'y'` dentro de `image_tag` (ou qualquer filtro com argumentos nomeados) estoura `wrong number of arguments (given 3, expected 2)` SÓ em runtime — a página quebra com o setting preenchido e funciona com ele vazio (o sintoma parece "a imagem sumiu"). Regra: assign-first SEMPRE — monte a string completa num `{%- assign -%}` e passe a variável pronta como valor do argumento.
18. **`image_picker` não aceita default de imagem arbitrária** — só datasource `shopify://shop_images/...`. Section que exige imagem trata a ausência com placeholder explícito no Liquid, nunca com default no schema.

## Debug — Quando validação ou push falha

| Mensagem (trecho) | Causa | Solução |
|---|---|---|
| `Missing width and height attributes on img tag` | `<img>` sem dimensões | `image_tag` filter (conversor já aplica) |
| `default must be a string or datasource access path` | `url` default com `#anchor`/relativo | default vazio ou absoluto |
| `invalid inline richtext: Attribute 'X' is not permitted` | `inline_richtext` com class/aria/data | strip attrs (só tags simples) |
| `Range settings must have at most 101 steps` | `(max-min)/step > 100` | aumentar step / reduzir range |
| `default must be a step in the range` | default não múltiplo do step | `(default-min) % step == 0` |
| `Opening tag does not have a matching closing tag` | HTML quebrado em `{% if %}` | atributos/classes condicionais, não tags partidas |
| `The 'id' argument should be a string` | theme block dinâmico `{% content_for 'block' %}` | refatorar pra blocks inline `{% case block.type %}` |
| `Section type 'X' does not refer to an existing section file` | template JSON referencia section não instalada | push a section antes; conferir ordem do `cp` |
| Blocks aparecem vazios na preview | `blocks: {}` no template JSON | rodar o snippet de validação da ETAPA 4 |
| Cor mudada no editor não aplica | CSS var hardcoded em `:root` em vez de inline no root | Padrão 2 da seção Padrões (conversor injeta inline; se quebrou, re-COMPILE) |
| Meta Pixel não registra AddToCart | CTA `<a href="/cart/add?id=X">` em vez de form POST | Padrão 5 da seção Padrões (conversor gera form `/cart/add` nativo) |
| Push trava esperando confirmação (tema LIVE) | falta `--allow-live` | adicionar flag |
| `ERR_MODULE_NOT_FOUND @shopify/theme-check-common` | registry privado do plugin | `rm package-lock.json && npm install --registry=https://registry.npmjs.org/` |
