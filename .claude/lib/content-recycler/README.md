# Content Recycler (Skill `content-recycler`)

Engine da Trilha 2 da skill `content-recycler`: pega 1 criativo classificado como breakthrough pela skill `ad-analysis` (cânone `.claude/lib/ad-taxonomy/README.md` §2) e gera 9 derivadas adaptadas a canais diferentes.
Reaproveita o breakthrough em 9 canais sem produção nova. A Trilha 1 (amplificação, o default da `content-recycler`) vive na skill `content-recycler` e no cânone, não nesta lib.

## Quando usar

**Manual** (hoje): membro invoca com `recycle [creative-id]` ou `recycle breakthrough`
(usa `breakthroughs[]` do `ad-analysis/dados.json`; `kpi_winner` não entra).

**Automático** (futuro): disparo direto quando a skill `ad-analysis` marcar um breakthrough novo.
Hoje o gatilho é sempre manual — a `ad-analysis` recomenda, o membro invoca.

## Input

Um criativo de referência — qualquer um destes:
- Briefing completo de `workspace/[produto]/creative-engine/concept-XX.md`
- Ad script + primary text + headlines
- Copy de advertorial ou PDP

## Output — 9 formatos derivados

Salvos em `workspace/[produto]/content-recycler/[source-id]/`:

1. **advertorial-1500w.md** — advertorial editorial longa pra LP ou blog
2. **email-sequence.md** — 5 emails (welcome → mechanism → social proof → objection → CTA)
3. **organic-tiktok-20s.md** — script pra post orgânico (sem pixel, sem CTA link direto)
4. **blog-seo-post.md** — 1500-2000w post com keyword target + schema markup
5. **pinterest-carousel-8.md** — 8 slides (problem → mechanism → proof)
6. **youtube-preroll-15s.md** — versão condensada 15s non-skippable
7. **sms-welcome.md** — mensagem pós-opt-in 160 chars
8. **package-insert.md** — card físico pra caixa (onboarding + secondary benefit)
9. **podcast-ad-30s.md** — áudio-only host-read style

## Idioma

README, essence.json descritivo e mensagens ao membro seguem o `report_language`
de `workspace/profile.md` (default `pt-BR`). As 9 derivadas consumidor-final
(advertorial, email, TikTok, blog, etc.) permanecem SEMPRE em inglês US.

## Estilo

Cada derivada sai na força do criativo-fonte: claim direto, específico, sem
aviso ou suavização inserida por conta própria (rule 8b do CLAUDE.md), com
travessão zero em headlines e subject lines (rule 8a).

## Custo

Zero custo extra — só tokens da assinatura Claude (~40-60k por rodada).

## Roda assim

```
recycle <creative-id>
```

O sistema lê o concept, consulta base Aura sobre formato de cada derivada,
gera 9 versões e salva tudo em pasta dedicada.
Entrega: "9 derivadas prontas em workspace/[produto]/content-recycler/[creative-id]/"
