"""verify_page.py no perfil design. Roda por subprocess: o _bootstrap() troca o processo no
import. Pula quando o Playwright não está em nenhum venv (exit 3)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _pageqa import FIXTURES, ROOT

SCRIPT = ROOT / ".claude" / "lib" / "theme-verify" / "verify_page.py"


def run(name, *extra):
    tmp = Path(tempfile.mkdtemp())
    out = tmp / "qa.json"
    proc = subprocess.run([sys.executable, str(SCRIPT), f"file://{FIXTURES / name}", "--json-out", str(out),
                           "--shots-dir", str(tmp / "shots"), *extra], capture_output=True, text=True, timeout=300)
    if proc.returncode == 3:
        raise unittest.SkipTest("Playwright ausente nos venvs (.claude/lib/web-fetch/README.md)")
    return proc, (json.loads(out.read_text()) if out.exists() else None), tmp


def by_id(metrics):
    out = {}
    for i in metrics["items"]:
        out.setdefault(i["id"], []).append(i)
    return out


class VerifyPageDesign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean = run("clean.html")
        cls.dirty = run("dirty.html")

    def test_clean_nao_tem_fail_e_sai_com_zero(self):
        proc, m, _ = self.clean
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual([i["id"] for i in m["items"] if i["status"] == "fail"], [])
        self.assertTrue(m["page_sha256"])

    def test_cada_defeito_aparece_com_id_e_blocking_certos(self):
        proc, m, _ = self.dirty
        self.assertEqual(proc.returncode, 1)
        items = by_id(m)
        for id_ in ("script_tags", "section_markers", "horizontal_overflow", "html_css_kb"):
            self.assertTrue(any(i["status"] == "fail" and i["blocking"] for i in items[id_]), id_)
        for id_ in ("contrast", "font_sizes_distinct", "headline_lines"):
            self.assertTrue(any(i["status"] == "warn" and not i["blocking"] for i in items[id_]), id_)

    def test_rodar_duas_vezes_da_o_mesmo_resultado(self):
        _, again, _ = run("clean.html")
        strip = lambda m: [(i["id"], i["status"], i["width"]) for i in m["items"]]
        self.assertEqual(strip(self.clean[1]), strip(again))

    def test_legal_reprovado_vira_legal_check_em_fail(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "plan.json").write_text(json.dumps({"build_mode": "reference", "section_order": ["hero", "offer"]}))
        (tmp / "legal.json").write_text(json.dumps({"pass": False, "findings": [{"rule": "texto"}]}))
        proc, m, _ = run("clean.html", "--plan", str(tmp / "plan.json"), "--legal", str(tmp / "legal.json"))
        items = by_id(m)
        self.assertEqual(items["legal_check"][0]["status"], "fail")
        self.assertEqual(items["section_ids_match_plan"][0]["status"], "pass")
        self.assertEqual(proc.returncode, 1)

    def test_sem_json_out_e_o_perfil_loja_de_sempre(self):
        tmp = Path(tempfile.mkdtemp())
        proc = subprocess.run([sys.executable, str(SCRIPT), f"file://{FIXTURES / 'dirty.html'}",
                               "--shots-dir", str(tmp)], capture_output=True, text=True, timeout=300)
        self.assertEqual(proc.returncode, 1)
        self.assertIn("overflow horizontal", proc.stdout)
        self.assertNotIn("script_tags", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
