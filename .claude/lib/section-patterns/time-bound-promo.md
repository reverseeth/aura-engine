# Time-Bound Promo — schema pattern

Pattern pra banners/eyebrows/badges que aparecem condicionalmente baseado em data (ex: Black Friday, Mother's Day, launch week).

## Problema que resolve

Copy hardcoded "Limited time — ends [date]" em Liquid vira tech-debt: depois da data passar, o badge continua no ar mentindo. Pior: se o membro esquecer de desligar, Meta scraper lê, member paga ads pra promo expirada.

## Schema obrigatório

Toda section com promo time-bound expõe:

```liquid
{%- schema -%}
{
  "name": "Eyebrow promo banner",
  "settings": [
    { "type": "checkbox", "id": "promo_enabled", "label": "Enable promo", "default": false },
    { "type": "text", "id": "promo_text", "label": "Promo message", "default": "" },
    { "type": "text", "id": "promo_link_url", "label": "Link URL (optional)" },
    { "type": "text", "id": "promo_link_label", "label": "Link label", "default": "Shop now →" },
    { "type": "text", "id": "promo_start_date", "label": "Start date (YYYY-MM-DD HH:MM, shop TZ)", "info": "Banner só aparece a partir dessa data" },
    { "type": "text", "id": "promo_end_date", "label": "End date (YYYY-MM-DD HH:MM, shop TZ)", "info": "Banner desliga automaticamente" },
    { "type": "color", "id": "promo_bg_color", "label": "Background", "default": "#1A1A1A" },
    { "type": "color", "id": "promo_text_color", "label": "Text", "default": "#FFFFFF" },
    { "type": "checkbox", "id": "promo_countdown_enabled", "label": "Show countdown to end_date", "default": false }
  ]
}
{%- endschema -%}
```

## Render condicional

```liquid
{%- liquid
  assign show_promo = false
  if section.settings.promo_enabled and section.settings.promo_text != blank
    assign now_iso = 'now' | date: '%Y-%m-%dT%H:%M:%S'
    assign start_iso = section.settings.promo_start_date | default: ''
    assign end_iso = section.settings.promo_end_date | default: ''

    if start_iso != '' and end_iso != ''
      if now_iso >= start_iso and now_iso <= end_iso
        assign show_promo = true
      endif
    elsif start_iso != '' and end_iso == ''
      if now_iso >= start_iso
        assign show_promo = true
      endif
    elsif end_iso != '' and start_iso == ''
      if now_iso <= end_iso
        assign show_promo = true
      endif
    else
      assign show_promo = true
    endif
  endif
-%}

{%- if show_promo -%}
  <aside
    class="promo-bar"
    style="background: {{ section.settings.promo_bg_color }}; color: {{ section.settings.promo_text_color }};"
    data-promo-end="{{ section.settings.promo_end_date }}"
  >
    <p>{{ section.settings.promo_text }}
      {%- if section.settings.promo_link_url != blank -%}
        <a href="{{ section.settings.promo_link_url }}" style="color: inherit;">{{ section.settings.promo_link_label }}</a>
      {%- endif -%}
    </p>
    {%- if section.settings.promo_countdown_enabled -%}
      <span class="promo-countdown" data-countdown-to="{{ section.settings.promo_end_date }}"></span>
    {%- endif -%}
  </aside>
{%- endif -%}
```

## Countdown JS (opcional)

Se `promo_countdown_enabled`, injetar script minimal:

```html
<script>
  document.querySelectorAll('[data-countdown-to]').forEach(el => {
    const target = new Date(el.dataset.countdownTo).getTime();
    const tick = () => {
      const now = Date.now();
      const diff = target - now;
      if (diff <= 0) { el.closest('.promo-bar')?.remove(); return; }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      el.textContent = `${d}d ${h}h ${m}m`;
    };
    tick();
    setInterval(tick, 60000);
  });
</script>
```

## Timezone handling

`'now' | date: '%Y-%m-%dT%H:%M:%S'` retorna no timezone da LOJA Shopify (definido em Settings > Store details). NÃO timezone do visitante. Se a promo é "ends Sunday 11:59pm PT" e a loja tá configurada em EST, start/end precisam estar em EST — NUNCA em PT.

Pra promos cross-timezone, usar UTC e calcular offset no JS do countdown.

## Integração com Promise↔Config gate

O Promise↔Config gate (`.claude/rules/pre-launch-gates.md`) detecta strings tipo "ends [date]" ou "Limited time" na copy e cross-checks:

1. Existe schema `promo_enabled` configurado nessa section?
2. `promo_end_date` é data futura válida?
3. Se a copy promete "until Sunday", `promo_end_date` bate com Sunday?

Se `fail`, BLOCK deploy até fix.

## Regras operacionais

1. **NUNCA hardcode data** na copy direta de Liquid. Sempre via schema.
2. **`data-promo-end`** no DOM pra JS/analytics detectar — não usar ID único (conflita em múltiplas instâncias)
3. **`<aside>` com role implícito** é semântico pra banner de promo (não `<div>` genérico)
4. **Remover banner após expiração** via JS (`.closest('.promo-bar').remove()`) pra evitar flash de banner expirado enquanto Liquid re-renderiza
5. **Log de promo expirada** no manifest pra audit trail: `manifest.json → promos_history[]`
