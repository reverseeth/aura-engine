# Content Recycler (#17)

Pega 1 criativo winner e gera 9 derivadas adaptadas a canais diferentes.
Multiplica ROI do criativo por 5-10x sem produção nova.

## Quando usar

**Automaticamente** (quando Shadow Brain tiver rodando): quando um ad atinge
critérios de winner — CPA < target × 0.7 E spend > $300 E idade > 5 dias.

**Manual**: membro invoca com `recycle [creative-id]`.

## Input

Um criativo de referência — qualquer um destes:
- Briefing completo de `/workspace/[produto]/07-creatives/07-concept-XX.md`
- Ad script + primary text + headlines
- Copy de advertorial ou PDP

## Output — 9 formatos derivados

Salvos em `/workspace/[produto]/17-recycled/[source-id]/`:

1. **advertorial-1500w.md** — advertorial editorial longa pra LP ou blog
2. **email-sequence.md** — 5 emails (welcome → mechanism → social proof → objection → CTA)
3. **organic-tiktok-20s.md** — script pra post orgânico (sem pixel, sem CTA link direto)
4. **blog-seo-post.md** — 1500-2000w post com keyword target + schema markup
5. **pinterest-carousel-8.md** — 8 slides (problem → mechanism → proof)
6. **youtube-preroll-15s.md** — versão condensada 15s non-skippable
7. **sms-welcome.md** — mensagem pós-opt-in 160 chars
8. **package-insert.md** — card físico pra caixa (onboarding + secondary benefit)
9. **podcast-ad-30s.md** — áudio-only host-read style

## Compliance integrado

Cada formato gerado passa pelo Compliance Pre-flight antes de ser salvo.
Derivadas de winner podem herdar termos que funcionaram no ad original mas
podem não ser safe em outros formatos (ex: Pinterest é mais rígido com
before/after que Meta Ads).

## Custo

Zero. Só tokens Claude.

## Roda assim

```
recycle <creative-id>-plateau-confession
```

O sistema lê o concept, consulta base Aura sobre formato de cada derivada,
gera 9 versões, passa compliance em cada, salva tudo em pasta dedicada.
Entrega: "9 derivadas prontas em /workspace/<product-slug>/17-recycled/<creative-id>/"
