# -*- coding: utf-8 -*-
"""graphlint 的单元测试：签名判定、条件必填、等级上限、时间窗与生成物漂移。"""
from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))

from graphlint import generate as gen  # noqa: E402
from graphlint import signatures  # noqa: E402
from graphlint.checks import check_graph  # noqa: E402
from graphlint.signatures import load  # noqa: E402

FIXTURES = TOOLS_DIR / "tests" / "fixtures"


def codes(result):
    return [i.code for i in result.issues]


def node(node_id: str, node_type: str, **extra):
    base = {
        "id": node_id,
        "type": node_type,
        "schema_version": "0.2",
        "labels": {"zh": node_id},
        "status": "historical",
        "claims": [],
        "provenance": {
            "created_by": "graphlint-tests",
            "created_at": "2026-11-23",
            "schema_version": "0.2",
        },
    }
    base.update(extra)
    return base


def event():
    return node("EV:fixture-event", "event", date={"from": 1799, "to": 1799, "precision": "year"},
                place="意大利", actors=["PE:fixture-author"])


def concept():
    return node("CO:fixture-concept", "concept", definition="测试定义",
                definition_source={"grade": "F", "locator": "fixture"}, occurrences=[])


def problem():
    return node(
        "PR:fixture-problem", "problem", status="resolved",
        original_formulation={"text": "测试表述", "source": {"locator": "fixture"},
                              "grade": "F", "attestation": "textbook_simplification"},
        problem_kind="solvability", asked_as=["测试"], related_branches=[],
    )


def notation(tag: str):
    return node(
        f"NO:fixture-{tag}", "notation", symbol_id=f"fixture-{tag}", kind="term",
        denotation=[], first_occurrence={"by": "PE:fixture-author", "year": 1799},
        modern_standard="fixture",
    )


def edge(edge_id: str, frm: str, etype: str, to: str, **extra):
    data = {
        "id": f"E:{frm}>{etype}>{to}",
        "from": frm,
        "to": to,
        "type": etype,
        "directed": True,
        "time": {"from": 1799, "to": 1799, "precision": "year"},
        "source": {"locator": "fixture"},
        "grade": "F",
        "attestation": "textbook_simplification",
        "confidence": 0.5,
    }
    if edge_id.endswith("#2") or edge_id.endswith("#3"):
        data["id"] = data["id"] + edge_id[-2:]
    data.update(extra)
    return data


class SignatureAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sig = load()

    def test_part_of_accepts_declared_endpoints(self):
        part_of = self.sig.edges["part_of"]
        self.assertTrue(part_of.accepts("event", "problem"))
        self.assertTrue(part_of.accepts("event", "concept"))
        self.assertTrue(part_of.accepts("event", "method"))

    def test_part_of_rejects_undeclared_endpoints(self):
        part_of = self.sig.edges["part_of"]
        self.assertFalse(part_of.accepts("concept", "event"))
        self.assertFalse(part_of.accepts("event", "teaching_point"))
        self.assertFalse(part_of.accepts("branch", "problem"))

    def test_supports_excludes_teaching_point(self):
        supports = self.sig.edges["supports"]
        self.assertTrue(supports.accepts("witness", "concept"))
        self.assertFalse(supports.accepts("witness", "teaching_point"))


class ConditionalNoteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sig = load()

    def test_part_of_to_concept_requires_note(self):
        graph = {"nodes": [event(), concept()],
                 "edges": [edge("", "EV:fixture-event", "part_of", "CO:fixture-concept")]}
        result = check_graph(graph, self.sig, "inline.json")
        self.assertIn("NOTE_REQUIRED", codes(result))
        issue = next(i for i in result.errors if i.code == "NOTE_REQUIRED")
        self.assertEqual(issue.expected, "非空 note，写明为何不挂更具体的对象")

    def test_part_of_to_concept_with_note_passes(self):
        graph = {"nodes": [event(), concept()],
                 "edges": [edge("", "EV:fixture-event", "part_of", "CO:fixture-concept",
                                note="该事件先于概念定名，只能挂在概念上。")]}
        self.assertNotIn("NOTE_REQUIRED", codes(check_graph(graph, self.sig, "inline.json")))

    def test_part_of_to_problem_has_no_note_requirement(self):
        graph = {"nodes": [event(), problem()],
                 "edges": [edge("", "EV:fixture-event", "part_of", "PR:fixture-problem")]}
        self.assertNotIn("NOTE_REQUIRED", codes(check_graph(graph, self.sig, "inline.json")))


class GradeCapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sig = load()

    def test_textbook_simplification_reports_actual_and_expected(self):
        graph = {"nodes": [event(), problem()],
                 "edges": [edge("", "EV:fixture-event", "part_of", "PR:fixture-problem",
                                grade="S")]}
        result = check_graph(graph, self.sig, "inline.json")
        issue = next(i for i in result.errors if i.code == "ATTESTATION_GRADE_CAP")
        self.assertEqual(issue.actual, "attestation=textbook_simplification, grade=S")
        self.assertEqual(issue.expected, "grade ∈ {F, U}")

    def test_textbook_simplification_with_f_is_allowed(self):
        graph = {"nodes": [event(), problem()],
                 "edges": [edge("", "EV:fixture-event", "part_of", "PR:fixture-problem")]}
        self.assertNotIn("ATTESTATION_GRADE_CAP", codes(check_graph(graph, self.sig, "inline.json")))

    def test_later_report_cannot_be_a(self):
        graph = {"nodes": [event(), problem()],
                 "edges": [edge("", "EV:fixture-event", "part_of", "PR:fixture-problem",
                                grade="A", attestation="later_report")]}
        result = check_graph(graph, self.sig, "inline.json")
        self.assertIn("LATER_REPORT_GRADE_CAP", codes(result))


class TimeWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sig = load()

    def test_multiple_windows_do_not_interfere(self):
        """同一对端点、不同时间段的边各自独立；窗口不应触发缺时间或条件必填。"""
        first = edge("", "EV:fixture-event", "part_of", "PR:fixture-problem",
                     time={"from": 1799, "to": 1800, "precision": "year"})
        second = edge("#2", "EV:fixture-event", "part_of", "PR:fixture-problem",
                      time={"from": 1829, "to": 1871, "precision": "year"})
        graph = {"nodes": [event(), problem()], "edges": [first, second]}
        result = check_graph(graph, self.sig, "inline.json")
        self.assertEqual(codes(result), [])

    def test_denotes_window_forms(self):
        precise = edge("", "NO:fixture-one", "denotes", "CO:fixture-concept",
                       time={"from": 1829, "to": 1871, "precision": "year"})
        unknown = edge("", "NO:fixture-two", "denotes", "CO:fixture-concept",
                       time={"from": None, "to": None, "precision": "unknown"},
                       note="首次使用时间待考。")
        graph = {"nodes": [notation("one"), notation("two"), concept()],
                 "edges": [precise, unknown]}
        result = check_graph(graph, self.sig, "inline.json")
        self.assertNotIn("TIME_REQUIRED", codes(result))
        self.assertEqual(codes(result), [])


class GenerateCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.schema = root / "graph.schema.json"
        self.doc = root / "object-model.md"
        shutil.copy2(signatures.GRAPH_SCHEMA_PATH, self.schema)
        shutil.copy2(signatures.DOC_PATH, self.doc)
        self.patches = [
            mock.patch.object(gen, "GRAPH_SCHEMA_PATH", self.schema),
            mock.patch.object(gen, "DOC_PATH", self.doc),
        ]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in self.patches:
            patch.stop()
        self.tmp.cleanup()

    def run_check(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = gen.generate(check=True)
        return code, out.getvalue()

    def test_clean_copies_are_in_sync(self):
        code, out = self.run_check()
        self.assertEqual(code, 0)
        self.assertIn("一致", out)

    def test_hand_edited_schema_is_detected(self):
        self.schema.write_text(self.schema.read_text(encoding="utf-8") + "\n",
                               encoding="utf-8")
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("不一致", out)
        self.assertIn(str(self.schema), out)

    def test_hand_edited_doc_is_detected(self):
        text = self.doc.read_text(encoding="utf-8")
        marker = "<!-- GENERATED:edge-table BEGIN"
        begin = text.index(marker)
        changed = text[:begin] + text[begin:].replace("`part_of`", "`part_of_typo`", 1)
        self.doc.write_text(changed, encoding="utf-8")
        code, out = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("不一致", out)
        self.assertIn(str(self.doc), out)


class FailureFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sig = load()

    def test_fixtures_trigger_expected_codes(self):
        expected = {
            "graph_unknown_type.json": "EDGE_TYPE_UNKNOWN",
            "graph_bad_endpoint.json": "ENDPOINT_TYPE",
            "graph_grade_cap.json": "ATTESTATION_GRADE_CAP",
            "graph_missing_note.json": "NOTE_REQUIRED",
        }
        for name, code in expected.items():
            with self.subTest(fixture=name):
                graph = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
                result = check_graph(graph, self.sig, name)
                self.assertIn(code, [i.code for i in result.errors])


class MissingPyYAMLTests(unittest.TestCase):
    def test_load_explains_missing_pyyaml(self):
        with mock.patch.object(signatures, "yaml", None):
            with self.assertRaises(SystemExit) as caught:
                signatures.load()
        message = str(caught.exception.code)
        self.assertIn("PyYAML", message)
        self.assertIn("pip install", message)

    def test_cli_exits_nonzero_without_traceback(self):
        code = (
            "import sys\n"
            "sys.modules['yaml'] = None\n"
            "from graphlint.cli import main\n"
            "sys.exit(main(['check-all']))\n"
        )
        proc = subprocess.run([sys.executable, "-c", code], cwd=str(TOOLS_DIR),
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertIn("PyYAML", proc.stderr)
        self.assertIn("pip install", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
