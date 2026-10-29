import hashlib
import unittest

import _pageqa  # noqa: F401 — põe tools/page-qa no path
import qa_gate

PLAN = {"schema_version": 2, "page_type": "landing",
        "strategy": {"page_type": "landing", "mechanism_name": "X"},
        "sections_plan": [{"id": "hero", "media": {}}], "section_order": ["hero"], "commerce": {}}


def metrics(*fails, sha=None):
    return {"page_sha256": sha, "items": [{"id": f, "status": "fail", "blocking": True, "value": 1,
                                           "limit": 0, "width": 390} for f in fails]}


class QaGate(unittest.TestCase):
    def test_pagina_antiga_so_avisa(self):
        self.assertEqual(qa_gate.gate({"page_type": "landing"}, None)[0], 2)

    def test_v2_sem_metricas_bloqueia(self):
        self.assertEqual(qa_gate.gate(PLAN, None)[0], 1)

    def test_liberar_overflow_desbloqueia(self):
        plan = dict(PLAN, qa_overrides=[{"item": "horizontal_overflow", "motivo": "carrossel", "data": "2026-10-29"}])
        self.assertEqual(qa_gate.gate(PLAN, metrics("horizontal_overflow"))[0], 1)
        self.assertEqual(qa_gate.gate(plan, metrics("horizontal_overflow"))[0], 0)

    def test_liberar_script_tags_nao_desbloqueia(self):
        plan = dict(PLAN, qa_overrides=[{"item": "script_tags", "motivo": "quero", "data": "2026-10-29"}])
        code, lines = qa_gate.gate(plan, metrics("script_tags"))
        self.assertEqual(code, 1)
        self.assertTrue(any("ignorada" in l for l in lines))

    def test_page_html_mudou_depois_do_qa_bloqueia(self):
        body = b"<html></html>"
        ok = metrics(sha=hashlib.sha256(body).hexdigest())
        self.assertEqual(qa_gate.gate(PLAN, ok, body)[0], 0)
        self.assertEqual(qa_gate.gate(PLAN, ok, body + b" ")[0], 1)

    def test_page_plan_invalido_bloqueia(self):
        self.assertEqual(qa_gate.gate({"schema_version": 2}, metrics())[0], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
