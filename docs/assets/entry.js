/* Preference improves the suggestion; navigation always remains a normal link. */
(() => {
  'use strict';
  let language = /^pt\b/i.test(navigator.languages?.[0] || navigator.language || '') ? 'pt' : 'en';
  try {
    const saved = localStorage.getItem('aura-lang');
    if (saved === 'pt' || saved === 'en') language = saved;
  } catch { /* Storage can be disabled without affecting the guide. */ }
  document.getElementById(`lang-${language}`)?.setAttribute('data-suggested', '');
  for (const code of ['pt', 'en']) {
    document.getElementById(`lang-${code}`)?.addEventListener('click', () => {
      try { localStorage.setItem('aura-lang', code); } catch { /* Optional preference. */ }
    });
  }
})();
