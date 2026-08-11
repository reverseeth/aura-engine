# Drawer enriquecido (personalizar o cart-drawer do tema Impact sem fork)

## O problema

O cart-drawer do tema Impact é um web component (`<cart-drawer>`) com o miolo dentro de shadow DOM parcial e markup próprio do tema. Personalizar por fork do tema cria um custo permanente: cada update do Impact vira um merge manual. E o drawer nasce genérico — sem a identidade da página, sem reforço de valor no momento mais sensível do funil (o cliente acabou de adicionar e está decidindo se fecha), sem campo de cupom utilizável (o campo existe, mas aplicar exige sair do fluxo) e com o add-to-cart padrão navegando pra `/cart` em página cheia.

O desafio técnico central: o conteúdo do drawer é re-renderizado pelo tema a cada mudança de carrinho — qualquer nó injetado some na próxima atualização. E o momento de abertura não tem um evento público confiável pra pendurar a injeção.

## A solução

- **Theming via `::part()` + seletores internos, no snippet base da página** (não no tema): `cart-drawer::part(content)` e `::part(overlay)` pro casco; seletores diretos (`cart-drawer h2`, `cart-drawer input`, `cart-drawer .button`) pro miolo que o Impact não expõe como part. Zero arquivo do tema modificado.
- **Card de infos do produto injetado via JS**: uma função idempotente (`if (d.querySelector('.sec-cart-info')) return`) localiza o botão de checkout pelo texto e insere o card antes dele — garantia, frete, benefício, cada linha com SVG inline. A idempotência permite chamar a função quantas vezes for preciso.
- **Três gatilhos de injeção redundantes**, porque não há evento único de abertura: (1) os eventos de carrinho do tema (`cart:change`, `cart:refresh`); (2) um `MutationObserver` no próprio `<cart-drawer>` — re-injeta sempre que o tema re-renderiza o miolo; (3) clique capturado no ícone de carrinho, com uma escada de `setTimeout` (80 a 2600ms) cobrindo o tempo de render.
- **Botão "Apply" de cupom dentro do `cart-discount-field`**: o campo vira `position: relative`, o botão entra `position: absolute` na direita, e o input ganha `padding-right` pro texto não passar por baixo. O clique seta o valor e dispara `new Event('change', { bubbles: true })` — o componente do tema escuta o change e recalcula o total sem reload.
- **Interceptor de add-to-cart**: `submit` capturado nos forms de `cart/add` da página, `fetch('/cart/add.js')` com `FormData`, depois `fetch('/cart.js')` pro estado novo, dispatch de `cart:change`/`cart:refresh` e `drawer.show()`. Se o fetch falhar (rate limit 429, rede), **fallback pro submit nativo** — o cliente nunca fica sem caminho de compra.

## Código de referência

Theming (vive no snippet base de CSS da página):

```css
/* casco do drawer via ::part */
cart-drawer::part(content) { background: rgb(var(--sec-bg)); }
cart-drawer::part(overlay) { background: rgba(var(--sec-dark), 0.5); }

/* miolo via seletores internos do Impact */
cart-drawer h2, cart-drawer .drawer__title, cart-drawer strong { color: rgb(var(--sec-ink)) !important; }
cart-drawer p, cart-drawer span, cart-drawer small { color: rgb(var(--sec-body)); }
cart-drawer input, cart-drawer textarea {
  background: rgb(var(--sec-white2)) !important;
  border-color: rgb(var(--sec-line)) !important;
  color: rgb(var(--sec-ink)) !important;
}
cart-drawer .button:not(.button--secondary), cart-drawer button[type="submit"].button {
  background: rgb(var(--sec-accent)) !important;
  color: rgb(255, 255, 255) !important;
  border-radius: 999px !important;
}

/* card de infos injetado */
cart-drawer .sec-cart-info {
  display: flex;
  flex-direction: column;
  gap: 9px;
  margin: 0 0 16px;
  padding: 15px 17px;
  border: 1px solid rgb(var(--sec-line));
  border-radius: 16px;
  background: rgb(var(--sec-bg));
}
cart-drawer .sec-cart-info span {
  display: flex;
  align-items: center;
  gap: 9px;
  font-size: 13px;
  color: rgb(var(--sec-body)) !important;
}
cart-drawer .sec-cart-info svg { flex: none; color: rgb(var(--sec-accent)); }

/* botão de cupom dentro do campo de desconto */
cart-drawer cart-discount-field { position: relative; display: block; }
cart-drawer .sec-apply {
  position: absolute;
  right: 7px;
  top: 50%;
  transform: translateY(-50%);
  padding: 10px 18px;
  border: 0;
  border-radius: 999px;
  cursor: pointer;
  background: rgb(var(--sec-accent));
  color: rgb(255, 255, 255) !important;
  font-size: 13px;
  font-weight: 600;
}
cart-drawer .sec-apply:disabled { opacity: 0.6; cursor: default; }
cart-drawer cart-discount-field input:not([type="hidden"]) { padding-right: 108px !important; }
```

Injeção + cupom + interceptor (vive numa section sempre presente, ex.: o header):

```html
<script>
  (function () {
    function abrirDrawer() {
      var d = document.querySelector('cart-drawer');
      if (d && typeof d.show === 'function') { d.show(); return true; }
      return false;
    }
    function atualizar(cart) {
      document.documentElement.dispatchEvent(new CustomEvent('cart:change', { bubbles: true, detail: { baseEvent: 'product-form:submit', cart: cart } }));
      document.documentElement.dispatchEvent(new CustomEvent('cart:refresh', { bubbles: true }));
    }

    /* card de infos: idempotente, insere antes do botão de checkout */
    function infoDrawer() {
      var d = document.querySelector('cart-drawer');
      if (!d || d.querySelector('.sec-cart-info')) return;
      var btn = Array.prototype.slice.call(d.querySelectorAll('button, a'))
        .filter(function (e) { return /checkout/i.test((e.textContent || '').trim()); })[0];
      if (!btn || !btn.parentElement) return;
      var wrap = document.createElement('div');
      wrap.className = 'sec-cart-info';
      wrap.innerHTML =
        '<span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3 3"></path></svg>[benefício principal do produto]</span>' +
        '<span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.8l7.2 2.9v5.2c0 4.9-3.1 8.3-7.2 10.3-4.1-2-7.2-5.4-7.2-10.3V5.7Z"></path><path d="M8.8 11.9l2.2 2.3 4.2-4.6"></path></svg>[garantia]</span>' +
        '<span><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 8.5 12 4l8.5 4.5v7L12 20l-8.5-4.5Z"></path><path d="M3.5 8.5 12 13l8.5-4.5"></path><path d="M12 13v7"></path></svg>[frete / detalhe de confiança]</span>';
      var linha = btn.parentElement;
      if (linha.parentElement) linha.parentElement.insertBefore(wrap, linha);
    }

    /* botão Apply: seta o valor e dispara change — o tema recalcula sem reload */
    function botaoCupom() {
      var campo = document.querySelector('cart-drawer cart-discount-field');
      if (!campo || campo.querySelector('.sec-apply')) return;
      var input = campo.querySelector('input:not([type="hidden"])');
      if (!input) return;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'sec-apply';
      b.textContent = 'Apply';
      b.addEventListener('click', function () {
        if (!input.value.trim()) { input.focus(); return; }
        b.disabled = true; b.textContent = 'Applying…';
        input.dispatchEvent(new Event('change', { bubbles: true }));
        setTimeout(function () { b.disabled = false; b.textContent = 'Apply'; }, 1800);
      });
      campo.appendChild(b);
    }

    /* três gatilhos redundantes: eventos do tema, MutationObserver, clique no ícone */
    function enriquecerDrawer() {
      [80, 350, 800, 1600, 2600].forEach(function (t) {
        setTimeout(function () { infoDrawer(); botaoCupom(); }, t);
      });
    }
    document.documentElement.addEventListener('cart:change', enriquecerDrawer);
    document.documentElement.addEventListener('cart:refresh', enriquecerDrawer);
    var alvo = document.querySelector('cart-drawer');
    if (alvo && 'MutationObserver' in window) {
      new MutationObserver(function () { infoDrawer(); botaoCupom(); }).observe(alvo, { childList: true, subtree: true });
    }
    document.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('a[aria-controls="cart-drawer"]')) enriquecerDrawer();
    }, true);

    /* add-to-cart sem reload, com fallback pro submit nativo */
    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (!form.matches || !form.getAttribute('action') || form.getAttribute('action').indexOf('cart/add') === -1) return;
      if (!form.closest('[data-section^="sec-"]')) return;
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var rotulo = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.style.opacity = '.75'; btn.textContent = 'Adding…'; }
      fetch('/cart/add.js', { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function () { return fetch('/cart.js', { headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); }); })
        .then(function (cart) {
          atualizar(cart);
          if (!abrirDrawer()) window.location.href = '{{ routes.cart_url }}';
          enriquecerDrawer();
        })
        .catch(function () { form.submit(); })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.style.opacity = ''; btn.textContent = rotulo; }
        });
    });
  })();
</script>
```

## Armadilhas

- **Forkar o tema pra estilizar o drawer.** Sintoma: o próximo update do Impact chega e o merge manual quebra ou é adiado pra sempre. Tudo aqui vive em snippet e section próprios — o tema fica intocado.
- **Injetar o card uma vez só, na abertura.** Sintoma: o card aparece, o cliente muda a quantidade, o tema re-renderiza o miolo e o card some. É por isso que a injeção é idempotente E pendurada em três gatilhos (eventos de carrinho, MutationObserver, clique) — qualquer re-render é seguido de re-injeção.
- **Aplicar o cupom setando só `input.value`.** Sintoma: o valor aparece no campo e o total não muda — o componente do tema nunca soube da mudança. O `dispatchEvent(new Event('change', { bubbles: true }))` é o que liga o fio; sem `bubbles: true`, o listener do componente pai não recebe.
- **Interceptar o add-to-cart sem fallback.** Sintoma: sob rate limit (429) ou falha de rede, o clique em comprar não faz NADA — a pior falha possível numa loja. O `.catch(function () { form.submit(); })` devolve o caminho nativo.
- **Abrir o drawer sem atualizar o estado.** Sintoma: o drawer abre mostrando o carrinho antigo (sem o item recém-adicionado). A ordem é: adicionar → buscar `/cart.js` → disparar `cart:change`/`cart:refresh` → abrir.
- **Interceptar TODOS os forms de `cart/add` da página.** Sintoma: forms de outras apps ou seções do tema mudam de comportamento sem querer. O filtro `form.closest('[data-section^="sec-"]')` limita o interceptor às sections do próprio padrão.
- **Localizar o botão de checkout por classe do tema.** Classes internas mudam entre versões do Impact; o filtro por texto (`/checkout/i`) sobrevive a update. Se a loja vende em idioma sem a palavra "checkout" no botão, ajustar a regex.
