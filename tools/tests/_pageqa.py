"""Ajuda compartilhada dos testes de tools/page-qa: path de import e capturas sintéticas."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE_QA = ROOT / "tools" / "page-qa"
FIXTURES = ROOT / "tools" / "tests" / "fixtures" / "page-qa"
if str(PAGE_QA) not in sys.path:
    sys.path.insert(0, str(PAGE_QA))


def band(index, height=600, columns=3, section=None, boxes=None):
    return {"index": index, "tag": "section", "selector": f"body > section:nth-child({index + 1})",
            "top": index * height, "height": height, "background": "rgb(255, 255, 255)",
            "aura_section": section, "columns": columns,
            "boxes": boxes if boxes is not None else [
                {"kind": "text", "cx": 0.3, "cy": 0.1, "w": 0.3, "h": 0.05},
                {"kind": "media", "cx": 0.7, "cy": 0.2, "w": 0.3, "h": 0.2}]}


def write_capture(root, bands, url="https://www.loja-referencia.com/p", texts=(), assets=(), styles=None):
    for w in (1440, 390):
        d = Path(root) / str(w)
        d.mkdir(parents=True, exist_ok=True)
        (d / "bands.json").write_text(json.dumps({"url": url, "width": w, "bands": bands}))
        (d / "texts.json").write_text(json.dumps([{"band": 0, "tag": "p", "text": t} for t in texts]))
        (d / "assets.json").write_text(json.dumps([{"band": 0, "url": a} for a in assets]))
        (d / "section-00.json").write_text(json.dumps(styles or []))
    return str(root)
