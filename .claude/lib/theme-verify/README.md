# theme-verify — gate visual e comportamental pós-deploy

Três scripts Playwright que verificam a página PUBLICADA da loja (a URL real que o visitante abre, não o preview local). É o gate de verificação da skill 07b (page-build) nas etapas 6.8/6.11, e roda de novo sempre que uma seção animada ou uma fonte custom entra no tema. O deploy só é declarado bom depois que os scripts aplicáveis à mudança passam.

| Script | O que verifica | Falha (exit 1) quando |
|---|---|---|
| `verify_page.py` | Estrutura: overflow horizontal, altura de cada seção, erros de console; screenshots desktop + mobile | há overflow > 0 ou seção com altura 0 |
| `font_census.py` | Todos os elementos visíveis com texto estão na fonte esperada | qualquer elemento fora da fonte |
| `motion_check.py` | Movimento real de seção animada (marquee/loop), com opção de rede lenta | salto na emenda, reflow da cópia, ou elemento parado |

**Exit codes (os três scripts):** `0` passou · `1` falha de verificação · `2` a página/elemento não carregou (não dá pra concluir nada — investigar antes) · `3` Playwright ausente.

## Dependência

O mesmo venv Playwright da lib web-fetch: `.claude/lib/web-fetch/.venv`. Rode com `<venv>/bin/python3` — e os scripts também se re-executam sozinhos nesse venv quando o python atual não tem Playwright. Se o venv não existe, o setup está no README da web-fetch (`.claude/lib/web-fetch/README.md`).

## verify_page.py — estrutura da página

```bash
.claude/lib/web-fetch/.venv/bin/python3 .claude/lib/theme-verify/verify_page.py \
  "https://sua-loja.com/products/seu-produto" --shots-dir /tmp/shots
```

Pra cada viewport (desktop 1440x1000 e mobile 390x844, ou só um com `--desktop-only`/`--mobile-only`):

- **Overflow horizontal** (`scrollWidth - clientWidth`) tem que ser 0 — qualquer pixel a mais significa que a página "anda de lado" no celular.
- **Altura total** e **presença + altura de cada seção** marcada com o atributo de `--sections-attr` (default `data-aura-section`, o atributo que o compile da 07b carimba em cada section; num tema de terceiros, aponte pro atributo que existir, ex. `data-section-id`). Seção presente com altura 0 = section renderizou vazia = falha.
- **Erros de console e de página**, filtrando o ruído de trackers de terceiros (pixels, apps de analytics) que não é problema do tema.
- **Screenshot full-page + um recorte por seção** na pasta de `--shots-dir`, pra conferência visual depois dos números.

Antes de medir, o script remove o popup de newsletter (`newsletter-popup`) pra ele não cobrir os screenshots, e faz rolagem progressiva até o fim da página pra disparar lazy-load e animações de reveal — sem isso, seção com reveal ainda invisível mediria altura errada.

## font_census.py — censo de fonte

```bash
.claude/lib/web-fetch/.venv/bin/python3 .claude/lib/theme-verify/font_census.py \
  "https://sua-loja.com/" --font "Nome da Fonte" --mobile
```

Percorre todos os elementos visíveis que têm texto direto e acusa cada um cujo `fontFamily` computado não começa com a fonte esperada. Imprime o total verificado, o total fora da fonte e até 20 seletores dos infratores (tag + classes), com a fonte que foi encontrada no lugar. O censo espera a fonte custom terminar de carregar (`document.fonts.ready`) antes de medir, pra não acusar falso infrator durante o swap.

Dois pontos de atenção:

- **Drawer/modal fechado não entra no censo.** Pra verificar o carrinho, o menu mobile ou qualquer modal, passe `--open-selector "<seletor do botão>"` — o script clica nele e espera a animação antes do censo. Exemplo: `--open-selector "[data-cart-toggle]"`.
- **Popup de app de terceiros entra no censo** se estiver visível — e é comum cair como infrator. Nesse caso a correção é na configuração do app, não no tema.

## motion_check.py — movimento de seção animada

```bash
.claude/lib/web-fetch/.venv/bin/python3 .claude/lib/theme-verify/motion_check.py \
  "https://sua-loja.com/" \
  --selector ".sec-marquee__track" --copy-selector ".sec-marquee__group" \
  --seconds 15 --throttle --mobile
```

Amostra a posição horizontal real do elemento (a matriz de transform lida com `DOMMatrix`, componente `m41`) a cada ~60ms e relata:

- **Velocidade média** em px/s e o sentido do movimento.
- **Wraps** — cada emenda do loop, o momento em que a posição volta pro início (detectada como um salto contra o sentido do movimento maior que metade da largura da cópia).
- **Anomalias** — qualquer delta fora do padrão que não é wrap: salto no meio do movimento, emenda de tamanho errado, elemento parado.
- Com `--copy-selector`: a **largura mínima e máxima da cópia observada durante o carregamento**. Largura que muda no meio = reflow (a página recalculou o layout porque uma imagem lazy chegou sem dimensão reservada) — é a raiz do salto na emenda.

## Por que throttling importa

O bug clássico que este teste existe pra pegar só aparece com rede lenta e cache frio. Uma faixa animada (marquee) costuma andar por transform em porcentagem da largura do próprio container, e a emenda do loop só fica invisível se essa largura for a mesma do início ao fim. Quando as imagens da faixa são lazy e não têm dimensão reservada no HTML, cada imagem que chega faz a largura da cópia crescer no meio da animação, e a emenda salta na frente do visitante. Com cache quente e rede rápida as imagens chegam antes do primeiro frame, a largura nunca muda e a medição sai limpa. O `--throttle` recria a condição real (300ms de latência, ~400 kbps de download, cache desligado, via o protocolo de automação do Chrome) e o script amostra a posição exatamente durante essa janela de carregamento.

Por isso, medição limpa em headless não é prova de mobile real. Um Chromium headless numa máquina de desenvolvimento carrega a página inteira em milissegundos, com rede de datacenter e cache aquecido pelas rodadas anteriores do próprio teste — o cenário mais favorável possível, e o oposto de um celular em rede móvel. A regra prática pra seção animada nova: rodar o `motion_check.py` duas vezes, primeiro sem `--throttle` (baseline: a animação em si está certa?) e depois com `--throttle --mobile` (a condição real). Só com as duas medições limpas a seção está aprovada.
