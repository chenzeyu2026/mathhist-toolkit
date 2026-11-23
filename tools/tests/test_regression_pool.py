"""Run the wrong-answer pool (错题池).

Every case in ``regression_pool.CASES`` is fed through ``check_text`` and the
full set of (code, severity) pairs must match exactly. An empty ``expect``
therefore means "no issue of any kind", which is what stops a later check from
firing on text that is already correct.
"""

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from mathlint.checks import check_text  # noqa: E402
import regression_pool  # noqa: E402


class RegressionPoolTests(unittest.TestCase):
    def test_every_case_matches(self):
        for case in regression_pool.CASES:
            with self.subTest(case["id"]):
                result = check_text("pool.md", case["text"])
                got = sorted((i.code, i.severity) for i in result.issues)
                want = sorted(case["expect"])
                self.assertEqual(
                    got,
                    want,
                    msg=f"{case['id']} {case['title']}: 期望 {want}，实际 {got}",
                )
                if "tags" in case:
                    self.assertEqual(
                        len(result.tags),
                        case["tags"],
                        msg=f"{case['id']} {case['title']}: 顶层标记数量不符",
                    )

    def test_nested_count_where_expected(self):
        # RP-09 is the only case that asserts a nested tag; count it explicitly
        # so that a depth-pairing regression cannot hide behind a top-level count.
        case = next(c for c in regression_pool.CASES if c["id"] == "RP-09")
        result = check_text("pool.md", case["text"])
        self.assertEqual(len(result.tags), 1)
        self.assertEqual(len(result.tags[0].nested), 1)

    def test_meta_fields(self):
        ids = [c["id"] for c in regression_pool.CASES]
        self.assertEqual(len(ids), len(set(ids)), msg="用例 id 重复")
        for case in regression_pool.CASES:
            with self.subTest(case["id"]):
                self.assertIn(case["kind"], ("auto", "locked"))
                self.assertTrue(case["rule"].strip())
                self.assertTrue(case["note"].strip())
                if case["kind"] == "locked":
                    self.assertIsInstance(case["expect"], list)

    def test_semantic_only_are_documented_not_faked(self):
        for entry in regression_pool.SEMANTIC_ONLY:
            with self.subTest(entry["id"]):
                self.assertTrue(entry["why"].strip())
                self.assertTrue(entry["where"].strip())


if __name__ == "__main__":
    unittest.main()
