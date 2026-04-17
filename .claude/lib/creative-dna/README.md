# Creative DNA Registry (#2)

Sistema de memória que aprende, a cada criativo produzido e medido, **qual combinação de elementos funciona pro mercado/avatar específico do membro**. Compounding proprietário.

## O que faz

1. **Extract** — quando Skill 07 gera briefing, extrai 15-20 features estruturadas
2. **Store** — salva em SQLite local (ou JSON) no workspace do produto
3. **Update** — quando Skill 09 roda, atualiza cada criativo com performance real
4. **Learn** — calcula correlações entre features e outcome (winner/loser)
5. **Inject** — próxima Skill 07 recebe DNA aprendido como constraint no briefing

## Arquitetura

```
/workspace/[produto]/creative-dna/
├── registry.db                  # SQLite com criativos + features + performance
├── dna-profile.json              # Perfil DNA atualizado a cada N criativos
├── dna-report.html               # Visualização humana (radar chart + tabela)
└── extraction-log.json           # Log de cada extração
```

## Integração silenciosa com Skills

- **Skill 07 (generate briefing)** → extrai features + salva no DB (sem membro ver)
- **Skill 09 (ad analysis)** → atualiza performance + outcome (sem membro ver)
- **Skill 07 (próxima rodada)** → carrega dna-profile.json e enviesa briefing

Silent end-to-end. Membro só vê o benefício via criativos que performam melhor.

## Ver status do DNA

```
dna show          # printa dna-profile.json atual
dna report        # gera dna-report.html com radar chart
dna stats         # total de criativos, % winners, top 10 features
dna reset         # wipe do registry (cuidado)
```

## Custo

Zero. SQLite é local, Claude tokens da assinatura.

## Quando começa a compensar

- **1-5 criativos**: só registra, nenhum insight ainda
- **6-15 criativos**: primeiras correlações aparecem, ainda noisy
- **16-30 criativos**: DNA estabilizado, briefings começam a refletir padrões
- **30+ criativos**: moat proprietário estabelecido, hit rate sobe visivelmente
