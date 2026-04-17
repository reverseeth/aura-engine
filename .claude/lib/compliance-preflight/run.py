"""
Compliance Pre-flight runner — standalone CLI.

Usage:
    python run.py /path/to/copy.md [--vertical skincare] [--asset-type headline]

Output:
    - Stdout: JSON report
    - Exit 0 = low/medium risk, exit 1 = high/critical (CI-friendly)

For Claude Code integration, use the checker.md prompt directly.
This runner is for CLI usage or git pre-commit hooks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
RED_FLAGS = json.loads((HERE / "red_flags.json").read_text())


def heuristic_score(text: str, vertical: str = "beauty") -> dict:
    """
    Quick heuristic pass — NOT the full Claude check.
    Used for fast pre-flight when full LLM pass is overkill.
    Matches patterns from red_flags.json and returns partial score.
    Final decision still needs checker.md prompt for nuance.
    """
    text_lower = text.lower()
    triggers = []
    score = 0

    universal = RED_FLAGS["universal_high_risk"]["patterns"]
    for item in universal:
        if item["phrase"].lower() in text_lower:
            sev = item["severity"]
            weight = {"low": 5, "medium": 12, "high": 22, "critical": 35}[sev]
            score += weight
            triggers.append({**item, "eixo": "Universal"})

    vertical_map = {
        "beauty": "beauty_skincare",
        "skincare": "beauty_skincare",
        "supplements": "supplements_health",
        "health": "supplements_health",
        "financial": "financial",
    }
    vkey = vertical_map.get(vertical)
    if vkey and vkey in RED_FLAGS:
        for item in RED_FLAGS[vkey]["patterns"]:
            if item["phrase"].lower() in text_lower:
                sev = item["severity"]
                weight = {"low": 5, "medium": 12, "high": 22, "critical": 35}[sev]
                score += weight
                triggers.append({**item, "eixo": vkey})

    for item in RED_FLAGS["pattern_triggers"]["patterns"]:
        pat = item["pattern"].replace("\\\\", "\\")
        if re.search(pat, text, re.IGNORECASE):
            sev = item["severity"]
            weight = {"low": 5, "medium": 12, "high": 22, "critical": 35}[sev]
            score += weight
            triggers.append({
                "phrase": f"pattern:{pat}",
                "severity": sev,
                "reason": item["reason"],
                "eixo": "Pattern",
            })

    em_dash_count = text.count("—") + text.count("–")
    if em_dash_count > 2:
        score += min(em_dash_count * 3, 15)
        triggers.append({
            "phrase": f"em-dash count: {em_dash_count}",
            "severity": "low" if em_dash_count <= 4 else "medium",
            "reason": "Travessão é assinatura de AI; minimizar.",
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
        if p in text_lower:
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

    return {
        "heuristic_only": True,
        "note": "Este é passe heurístico rápido. Pra decisão final, use checker.md com Claude.",
        "risk_score": score,
        "severity": severity,
        "triggers": triggers,
        "em_dash_count": em_dash_count,
        "recommendation": (
            "REJECT — refactor completo necessário" if severity == "critical"
            else "REVISE — rewrite triggers high severity" if severity == "high"
            else "APPROVE_WITH_EDIT — ajustar warnings" if severity == "medium"
            else "APPROVE — publicar"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Compliance Pre-flight heuristic checker")
    parser.add_argument("path", type=str, help="Path to copy file (.md, .txt)")
    parser.add_argument("--vertical", default="beauty",
                        choices=["beauty", "skincare", "supplements", "health", "financial", "other"])
    parser.add_argument("--asset-type", default="unknown")
    args = parser.parse_args()

    text = Path(args.path).read_text()
    result = heuristic_score(text, vertical=args.vertical)
    result["input_file"] = args.path
    result["vertical"] = args.vertical
    result["asset_type"] = args.asset_type

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(1 if result["severity"] in ("high", "critical") else 0)


if __name__ == "__main__":
    main()
