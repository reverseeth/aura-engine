// Tira de cena popup, modal e banner de cookies de uma página de terceiro antes da captura.
// Remove (não clica em "aceitar"): nenhum consentimento é dado em nome de ninguém.
// Usado pelo verify_page.py (imagem da referência) e pelo downloader.py --mode bands.
() => {
  const vw = innerWidth, vh = innerHeight;
  const words = /cookie|consent|gdpr|lgpd|newsletter|subscribe|inscreva|sign up for/i;
  const modal = 'dialog[open],[role="dialog"],[role="alertdialog"],[aria-modal="true"]';
  let removed = 0;
  for (const el of [...document.querySelectorAll('body *')]) {
    if (!el.isConnected) continue;
    const s = getComputedStyle(el);
    if (s.position !== 'fixed' && !el.matches(modal)) continue;
    if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) continue;
    const r = el.getBoundingClientRect();
    const area = Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)) *
                 Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
    if (!area) continue;
    // header fixo no topo fica: é parte da página, não um overlay
    if (r.top <= 0 && r.height < 200 && el.querySelector('nav, a[href="/"]')) continue;
    // wrapper de smooth scroll (fixo, com a página inteira dentro) também fica
    if (el.querySelector('main') || el.scrollHeight > 1.5 * vh) continue;
    if (area > 0.25 * vw * vh || el.matches(modal) || words.test(el.textContent || '')) {
      el.remove(); removed++;
    }
  }
  // modal aberto costuma travar o scroll do documento
  for (const e of [document.documentElement, document.body]) e.style.setProperty('overflow', 'visible', 'important');
  return removed;
}
