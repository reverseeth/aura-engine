"""downloader.py: robots.txt, file:// fora da allowlist e divisão em faixas. Roda por
subprocess no venv do design-clone (o import faz bootstrap de venv). Pula sem o venv."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from _pageqa import FIXTURES, ROOT

SCRIPT = ROOT / "tools" / "design-clone" / "downloader.py"
VENV_PY = next((p for p in (ROOT / "tools/design-clone/.venv/bin/python3",
                            ROOT / ".claude/lib/web-fetch/.venv/bin/python3") if p.exists()), None)


@unittest.skipUnless(VENV_PY, "venv com Playwright ausente (setup/reference/dependencias.md)")
class DownloaderBands(unittest.TestCase):
    def py(self, code):
        return subprocess.run([str(VENV_PY), "-c", code], capture_output=True, text=True, timeout=60,
                              cwd=str(SCRIPT.parent))

    def test_robots_que_proibe_bloqueia(self):
        code = (
            "import downloader as d\n"
            "class R:\n status_code=200\n text='User-agent: *\\nDisallow: /p'\n"
            "d.requests.get=lambda *a,**k: R()\n"
            "print(d.robots_allows('https://example.com/p/x'), d.robots_allows('https://example.com/ok'))\n")
        out = self.py(code)
        self.assertEqual(out.stdout.split()[-2:], ["False", "True"], out.stderr)

    def test_robots_ausente_permite(self):
        code = ("import downloader as d\n"
                "class R:\n status_code=404\n text=''\n"
                "d.requests.get=lambda *a,**k: R()\nprint(d.robots_allows('https://example.com/p'))\n")
        self.assertEqual(self.py(code).stdout.split()[-1], "True")

    def test_file_fora_da_allowlist_e_recusado(self):
        proc = subprocess.run([str(VENV_PY), str(SCRIPT), "file:///etc/hosts", tempfile.mkdtemp(), "--mode", "bands"],
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("allowlist", proc.stderr)

    def test_divide_a_pagina_em_faixas(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            page = tmp / "clean.html"
            shutil.copy(FIXTURES / "clean.html", page)
            proc = subprocess.run([str(VENV_PY), str(SCRIPT), f"file://{page}", str(tmp / "cap"),
                                   "--mode", "bands", "--widths", "1440"], capture_output=True, text=True, timeout=180)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            bands = json.loads((tmp / "cap/1440/bands.json").read_text())["bands"]
            self.assertEqual([b["aura_section"] for b in bands], ["hero", "offer"])
            texts = json.loads((tmp / "cap/1440/texts.json").read_text())
            self.assertIn("Calm sleep", [t["text"] for t in texts])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
