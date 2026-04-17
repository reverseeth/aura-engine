# Stitch Setup — 5 minutos, uma vez só

## Requisitos
- Conta Google (gmail)
- Browser atualizado (Chrome/Edge/Firefox)
- **Zero** cartão de crédito necessário

## Passo a passo

### 1. Acessar Google Labs (1min)

Ir em https://labs.google/stitch

Login com conta Google.

### 2. Habilitar Stitch (30s)

Clicar em "Try Stitch" → aceitar terms → pronto.

No free tier tu tem:
- 350 standard generations/mês (Gemini 2.5 Pro — qualidade máxima)
- 200 experimental generations/mês (Gemini 2.5 Flash — mais rápido, menos polido)

### 3. Testar com 1 prompt simples (2min)

No campo de input, cola:

```
Generate a modern product detail page (PDP).
Audience: [descrição curta do avatar do seu produto].
Style: clean, premium, editorial.
Components needed: hero with product shot, benefit section, mechanism explanation,
social proof, 3-tier pricing, guarantee, FAQ, final CTA.
Color palette: dark text on off-white background, single accent color.
Typography: modern serif for headlines, clean sans-serif for body.
```

(Substitua os colchetes pelos valores do seu produto antes de colar no Stitch.)

Clicar "Generate". Em ~45-60s, Stitch gera 1 screen.

### 4. Explorar o multi-canvas (1min)

- Clicar "Generate more variations" — 3 novas direções aparecem lado a lado
- Arrastar pra comparar
- Clicar em qualquer variação pra "lock" e iterar só nela

### 5. Export HTML standalone (30s)

Com mockup aprovado:
1. Botão "Export" (top-right)
2. Escolher "HTML standalone" (não Tailwind, não React — quer o HTML puro mais clean)
3. Baixar .zip contendo `index.html` + `assets/`

### 6. Preparar workspace (30s)

Quando for usar na Aura:
```bash
cd /Users/gustavo/aura-engine/workspace/[produto]/06-page/
unzip ~/Downloads/stitch-export.zip -d stitch-blueprint/
# resultado: workspace/[produto]/06-page/stitch-blueprint/index.html + assets
```

A skill 06a vai detectar automaticamente a pasta `stitch-blueprint/` e usar como visual reference.

## Troubleshooting

**"Generation limit reached"**
→ Esgotou 350/mês. Espera próximo ciclo ou usa experimental mode (200 adicionais).

**Stitch não aparece no Google Labs**
→ Labs às vezes é gated por região. VPN US resolve. Ou esperar — Google vem expandindo acesso.

**Export HTML trava**
→ Grandes páginas (>10 sections) podem demorar. Aguardar até 2min. Se falhar, reduzir complexidade do prompt ou gerar em 2 partes.

**Assets exportados não abrem locally**
→ Se abrir `index.html` direto e imagens falharem, servir localmente:
```bash
cd stitch-blueprint/
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Checklist de setup

- [ ] Conta Google Labs criada
- [ ] Stitch habilitado
- [ ] 1 generation de teste funcionou
- [ ] Export HTML testado + descompactado
- [ ] Entendi que preciso exportar manualmente (não é API automática)

Pronto. Próximo passo: `prompt-templates.md` pra usar em produção.
