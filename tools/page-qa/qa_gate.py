#!/usr/bin/env python3
"""
qa_gate.py — o portão de QA do page-build: combina o qa-metrics.json (medição) com as
liberações do membro (page-plan.json.qa_overrides).

USO:
    qa_gate.py PAGE-PLAN.json [QA-METRICS.json] [--page page.html]

Exit: 0 libera · 1 bloqueia · 2 página antiga (sem schema_version), só aviso.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import schema_validate  # noqa: E402

SCHEMA = ROOT / ".claude" / "templates" / "schemas" / "page-design.page-plan.schema.json"
LIBERAVEIS = {"horizontal_overflow", "broken_images", "html_css_kb"}


def gate(plan, metrics, page_bytes=None):
    """Devolve (exit_code, linhas)."""
    if plan.get("schema_version") is None:
        return 2, ["aviso: página antiga, sem QA medido. Compila como antes."]
    lines = [f"page-plan: {f}" for f in schema_validate.validate(plan, json.loads(SCHEMA.read_text()))]
    if metrics is None:
        return 1, lines + ["bloqueado: página v2 sem qa-metrics.json. Rode a ETAPA 5 da page-design."]
    if page_bytes is not None and metrics.get("page_sha256") != hashlib.sha256(page_bytes).hexdigest():
        lines.append("bloqueado: o page.html mudou depois do QA. Rode o QA de novo.")
    overrides = {o["item"]: o for o in plan.get("qa_overrides", [])}
    for item in sorted(set(overrides) - LIBERAVEIS):
        lines.append(f"aviso: liberação de {item} ignorada (item de contrato, não se libera).")
    for i in metrics.get("items", []):
        if not (i.get("blocking") and i.get("status") == "fail"):
            continue
        where = f" em {i['width']}px" if i.get("width") else ""
        if i["id"] in LIBERAVEIS and i["id"] in overrides:
            lines.append(f"liberado: {i['id']}{where} — {overrides[i['id']].get('motivo', '')}")
            continue
        lines.append(f"reprovado: {i['id']}{where} (valor {i.get('value')}, limite {i.get('limit')})")
        if i["id"] in LIBERAVEIS:
            lines.append(f'  para liberar: page-plan.json.qa_overrides += '
                         f'{{"item": "{i["id"]}", "motivo": "...", "data": "AAAA-MM-DD"}}')
    blocked = any(l.startswith(("bloqueado", "reprovado", "page-plan:")) for l in lines)
    return (1 if blocked else 0), lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("plan")
    ap.add_argument("metrics", nargs="?")
    ap.add_argument("--page")
    a = ap.parse_args(argv)
    plan = json.loads(Path(a.plan).read_text())
    mp = Path(a.metrics) if a.metrics else None
    metrics = json.loads(mp.read_text()) if mp and mp.exists() else None
    page = Path(a.page).read_bytes() if a.page else None
    code, lines = gate(plan, metrics, page)
    for l in lines:
        print(l)
    if code == 0:
        print("✅ QA liberado")
    return code


if __name__ == "__main__":
    sys.exit(main())
