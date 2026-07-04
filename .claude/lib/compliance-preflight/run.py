"""
Compliance Pre-flight runner — standalone CLI (passe heurístico).

CLI canônica (a MESMA usada pelas Skills 07b e 10 e pela rule pre-launch-gates):

    python3 .claude/lib/compliance-preflight/run.py --file <path> [--vertical <v>] [--stage pre_ad|pre_page] --json
    python3 .claude/lib/compliance-preflight/run.py --text "<copy>" [--vertical <v>] [--stage pre_ad|pre_page] --json

Flags:
    --file <path>      Arquivo de copy (.md, .txt). Mutuamente exclusivo com --text.
    --text "<string>"  Copy inline. Mutuamente exclusivo com --file.
    --vertical <v>     Enum do manifest-schema (product_vertical): beauty, skincare,
                       supplements, health, fitness, fashion, home, pet, food,
                       financial, tech, education, other. Default: other.
    --stage <s>        pre_ad | pre_page — contexto do gate (registrado no output).
    --json             Imprime o report JSON completo (conforme output-schema.json).
                       Sem a flag: resumo humano curto.

Output (--json), conforme output-schema.json:
    - overall_verdict: pass (low) | warning (medium) | critical (high/critical)
    - rewrite_suggestions[]: uma por flag encontrada, com a substituição padrão
      da rule 8b (safe_substitutions do red_flags.json) quando houver.

Exit codes: 0 = pass/warning · 1 = critical (CI-friendly).

Matching por word-boundary case-insensitive ("secure" NÃO casa "cure").
Este é o passe heurístico rápido; pra decisão final com nuance, use o prompt
checker.md com Claude.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
RED_FLAGS = json.loads((HERE / "red_flags.json").read_text())

SEVERITY_WEIGHT = {"low": 5, "medium": 12, "high": 22, "critical": 35}
SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}

# Verticais do manifest-schema → categoria de red flags
VERTICAL_MAP = {
    "beauty": "beauty_skincare",
    "skincare": "beauty_skincare",
    "supplements": "supplements_health",
    "health": "supplements_health",
    "fitness": "supplements_health",
    "food": "supplements_health",
    "pet": "supplements_health",
    "financial": "financial",
    # fashion, home, tech, education, other → só universal + pattern_triggers
}

MANIFEST_VERTICALS = [
    "beauty", "skincare", "supplements", "health", "fitness", "fashion",
    "home", "pet", "food", "financial", "tech", "education", "other",
]


def phrase_regex(phrase: str) -> re.Pattern:
    """Word-boundary matcher, tolerante a espaço/hífen entre palavras.

    'cure' → \\bcure\\b (não casa 'secure'); 'risk-free' casa 'risk free'.
    """
    parts = [re.escape(p) for p in re.split(r"[\s\-]+", phrase.strip()) if p]
    return re.compile(r"\b" + r"[\s\-]+".join(parts) + r"\b", re.IGNORECASE)


def find_substitution(phrase: str) -> list[str] | None:
    """Substituição padrão da rule 8b (safe_substitutions), com fallback singular."""
    mappings = {k.lower(): v for k, v in RED_FLAGS["safe_substitutions"]["mappings"].items()}
    key = phrase.lower()
    if key in mappings:
        return mappings[key]
    if key.endswith("s") and key[:-1] in mappings:
        return mappings[key[:-1]]
    return None


def verdict_from_severity(severity: str) -> str:
    return {"low": "pass", "medium": "warning"}.get(severity, "critical")


def heuristic_score(text: str, vertical: str = "other", stage: str | None = None) -> dict:
    """
    Passe heurístico rápido — NÃO é o check completo do Claude.
    Faz matching word-boundary contra red_flags.json e retorna score parcial.
    Decisão final com nuance ainda precisa do prompt checker.md.
    """
    triggers = []
    score = 0

    def add_phrase_triggers(patterns: list[dict], eixo: str):
        nonlocal score
        for item in patterns:
            if phrase_regex(item["phrase"]).search(text):
                sev = item["severity"]
                score += SEVERITY_WEIGHT[sev]
                triggers.append({**item, "eixo": eixo})

    add_phrase_triggers(RED_FLAGS["universal_high_risk"]["patterns"], "Universal")

    vkey = VERTICAL_MAP.get(vertical)
    if vkey and vkey in RED_FLAGS:
        add_phrase_triggers(RED_FLAGS[vkey]["patterns"], vkey)

    for item in RED_FLAGS["pattern_triggers"]["patterns"]:
        # JSON double-encodes backslashes; after json.loads the pattern already has the real escapes
        pat = item["pattern"]
        try:
            compiled = re.compile(pat, re.IGNORECASE)
        except re.error:
            continue
        if compiled.search(text):
            sev = item["severity"]
            informational = bool(item.get("informational"))
            if not informational:
                score += SEVERITY_WEIGHT[sev]
            triggers.append({
                "phrase": f"pattern:{pat}",
                "severity": sev,
                "reason": item["reason"],
                "eixo": "Pattern",
                "informational": informational,
            })

    em_dash_count = text.count("—") + text.count("–")
    if em_dash_count > 2:
        score += min(em_dash_count * 3, 15)
        triggers.append({
            "phrase": f"em-dash count: {em_dash_count}",
            "severity": "low" if em_dash_count <= 4 else "medium",
            "reason": "Travessão é assinatura de AI; minimizar (rule 8a: 0 em headlines, ≤2 em copy longa).",
            "eixo": "AI Style",
        })

    ai_phrases = [
        "are you tired of",
        "have you ever",
        "imagine a world",
        "in today's world",
        "in our modern",
        "revolutionary",
        "game-changing",
        "cutting-edge",
    ]
    for p in ai_phrases:
        if phrase_regex(p).search(text):
            score += 5
            triggers.append({
                "phrase": p,
                "severity": "low",
                "reason": "Frase genérica assinatura de LLM",
                "eixo": "AI Style",
            })

    score = min(score, 100)
    severity = (
        "critical" if score >= 71
        else "high" if score >= 41
        else "medium" if score >= 21
        else "low"
    )
    # Piso de severity: um único trigger critical/high já é red flag de
    # auto-disapproval — o gate não pode deixar passar como "warning" só
    # porque o score agregado ficou baixo.
    scored = [t for t in triggers if not t.get("informational")]
    if scored:
        max_trigger_sev = max((t["severity"] for t in scored), key=SEVERITY_ORDER.get)
        if SEVERITY_ORDER[max_trigger_sev] > SEVERITY_ORDER[severity]:
            severity = max_trigger_sev

    rewrite_suggestions = []
    for t in scored:
        if t["eixo"] == "Pattern":
            phrase_for_lookup = None
        else:
            phrase_for_lookup = t["phrase"]
        subs = find_substitution(phrase_for_lookup) if phrase_for_lookup else None
        rewrite_suggestions.append({
            "phrase": t["phrase"],
            "severity": t["severity"],
            "suggested_replacement": subs[0] if subs else None,
            "alternatives": subs or [],
            "reason": t["reason"],
        })

    overall_verdict = verdict_from_severity(severity)

    return {
        "heuristic_only": True,
        "note": "Este é passe heurístico rápido. Pra decisão final, use checker.md com Claude.",
        "risk_score": score,
        "severity": severity,
        "overall_verdict": overall_verdict,
        "triggers": triggers,
        "rewrite_suggestions": rewrite_suggestions,
        "rewrite_suggestion": None,
        "em_dash_count": em_dash_count,
        "vertical": vertical,
        "stage": stage,
        "recommendation": (
            "critical — aplicar rewrite_suggestions e re-rodar antes de submeter"
            if overall_verdict == "critical"
            else "warning — ajustar itens medium e logar" if overall_verdict == "warning"
            else "pass — publicar"
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compliance Pre-flight heuristic checker (CLI canônica: --file/--text, --vertical, --stage, --json)"
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=str, help="Path do arquivo de copy (.md, .txt)")
    source.add_argument("--text", type=str, help="Copy inline como string")
    parser.add_argument("--vertical", default="other", choices=MANIFEST_VERTICALS,
                        help="product_vertical do manifest (default: other)")
    parser.add_argument("--stage", default=None, choices=["pre_ad", "pre_page"],
                        help="Contexto do gate (metadata no output)")
    parser.add_argument("--json", action="store_true",
                        help="Imprime o report JSON completo (conforme output-schema.json)")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        if not path.exists():
            sys.stderr.write(f"ERROR: file not found: {path}\n")
            sys.exit(2)
        text = path.read_text()
    else:
        text = args.text

    result = heuristic_score(text, vertical=args.vertical, stage=args.stage)
    result["input_file"] = args.file

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"verdict: {result['overall_verdict']} · severity: {result['severity']} · risk_score: {result['risk_score']}")
        for t in result["triggers"]:
            marker = "(info)" if t.get("informational") else t["severity"]
            print(f"  - [{marker}] {t['phrase']} — {t['reason']}")
        for s in result["rewrite_suggestions"]:
            if s["suggested_replacement"]:
                print(f"  fix: '{s['phrase']}' → '{s['suggested_replacement']}'")

    sys.exit(1 if result["overall_verdict"] == "critical" else 0)


if __name__ == "__main__":
    main()
