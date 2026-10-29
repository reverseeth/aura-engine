"""liquid-converter.py: hex que bate com um papel do design-tokens.json vira `color_<papel>`,
o resto continua `color_N`, e seção já no tema mantém os `color_N`. Roda o CLI por
subprocess no venv do design-clone (o import faz bootstrap de bs4). Pula sem o venv."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from _pageqa import ROOT

SCRIPT = ROOT / "tools" / "design-clone" / "liquid-converter.py"
VENV_PY = ROOT / "tools" / "design-clone" / ".venv" / "bin" / "python3"

HTML = '<section class="hero" data-aura-section="hero"><h1 class="hero__title">Sleep better</h1></section>'
CSS = (":root{--color-primary:#C2410C;--color-foreground:#1c1917}"
       ".hero{background:var(--color-primary);border:1px solid #abcdef}"
       ".hero__title{color:var(--color-foreground)}")


@unittest.skipUnless(VENV_PY.exists(), "venv do design-clone ausente (setup/reference/dependencias.md)")
class PapeisDeCor(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "s.html").write_text(HTML)
        (self.tmp / "s.css").write_text(CSS)
        (self.tmp / "design-tokens.json").write_text(json.dumps(
            {"colors": {"primary": "#c2410c", "foreground": "#1C1917"}}))

    def convert(self, *extra):
        out = self.tmp / "theme-out" / "sections" / "page-p-hero.liquid"
        proc = subprocess.run(
            [str(VENV_PY), str(SCRIPT), "--html", str(self.tmp / "s.html"), "--css", str(self.tmp / "s.css"),
             "--type", "hero", "--output", str(out), "--namespace", "page-p-hero", "--product-slug", "p", *extra],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        text = out.read_text()
        schema = json.loads(text.split("{% schema %}")[1].split("{% endschema %}")[0])
        return {s["id"]: s.get("label") for s in schema["settings"] if s.get("type") == "color"}

    def test_hex_do_papel_vira_color_papel_e_o_resto_color_n(self):
        colors = self.convert("--design-tokens", str(self.tmp / "design-tokens.json"))
        self.assertEqual(colors.get("color_primary"), "Cor primária")
        self.assertEqual(colors.get("color_foreground"), "Cor do texto")
        self.assertEqual(colors.get("color_1"), "Color 1")
        self.assertEqual(len(colors), 3)

    def test_sem_design_tokens_fica_como_antes(self):
        self.assertEqual(set(self.convert()), {"color_1", "color_2", "color_3"})

    def test_secao_ja_no_tema_mantem_color_n(self):
        theme = self.tmp / "theme"
        (theme / "sections").mkdir(parents=True)
        (theme / "sections" / "page-p-hero.liquid").write_text('{% schema %}{"settings":[{"type":"color","id":"color_1"}]}{% endschema %}')
        colors = self.convert("--design-tokens", str(self.tmp / "design-tokens.json"), "--theme-dir", str(theme))
        self.assertEqual(set(colors), {"color_1", "color_2", "color_3"})


if __name__ == "__main__":
    unittest.main()
