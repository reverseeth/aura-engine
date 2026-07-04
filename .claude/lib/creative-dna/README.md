# Creative DNA Registry (#2)

Sistema de memória que aprende, a cada criativo produzido e medido, **qual combinação de elementos funciona pro mercado/avatar específico do membro**. Compounding proprietário.

## O que faz

1. **Extract** — quando Skill 08 gera briefing, extrai 26 features estruturadas (22 do criativo + 4 contextuais — ver `feature_schema.json`)
2. **Store** — salva em SQLite local no workspace do produto
3. **Update** — quando Skill 11 roda, atualiza cada criativo com performance real
4. **Learn** — calcula correlações entre features e outcome (winner/loser)
5. **Inject** — próxima Skill 08 recebe DNA aprendido como constraint no briefing

## Arquitetura

```
workspace/[produto]/creative-dna/
├── registry.db                    # SQLite com criativos + features + performance
├── dna-profile.json               # Perfil DNA atualizado a cada N criativos
├── features-[creative-id].json    # Features extraídas por criativo (Skill 08)
├── perf-[creative-id].json        # Performance por criativo (Skill 11)
└── extraction-errors.log          # Log de falhas de extração (não bloqueia a skill)
```

## Integração silenciosa com Skills

- **Skill 08 (generate briefing)** → extrai features + salva no DB (sem membro ver)
- **Skill 11 (ad analysis)** → atualiza performance + outcome (sem membro ver)
- **Skill 08 (próxima rodada)** → carrega dna-profile.json e enviesa briefing

Silent end-to-end. Membro só vê o benefício via criativos que performam melhor.

## CLI (registry.py)

```bash
python3 .claude/lib/creative-dna/registry.py init workspace/[produto]
python3 .claude/lib/creative-dna/registry.py add workspace/[produto] <creative-id> <features.json> --product <slug>
python3 .claude/lib/creative-dna/registry.py update workspace/[produto] <creative-id> <perf.json>
python3 .claude/lib/creative-dna/registry.py stats workspace/[produto] --product <slug>   # total, % por outcome
python3 .claude/lib/creative-dna/registry.py dna workspace/[produto] --product <slug>     # recalcula e salva dna-profile.json
python3 .claude/lib/creative-dna/registry.py show workspace/[produto]                     # printa dna-profile.json atual
```

Guardrails: `update` em creative_id inexistente falha com exit 1 (nunca no-op
silencioso); `dna` com menos de 10 criativos medidos não sobrescreve profile
anterior. Campos de identificação (creative_id, source_file, etc.) nunca entram
no DNA.

## Custo

Zero. SQLite é local, Claude tokens da assinatura.

## Quando começa a compensar

- **1-5 criativos**: só registra, nenhum insight ainda
- **6-15 criativos**: primeiras correlações aparecem, ainda noisy
- **16-30 criativos**: DNA estabilizado, briefings começam a refletir padrões
- **30+ criativos**: moat proprietário estabelecido, hit rate sobe visivelmente
