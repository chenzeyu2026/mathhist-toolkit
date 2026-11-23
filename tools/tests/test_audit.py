"""Lock the audit baselines quoted in ``docs/spec-audit*.md``.

The three audit scripts print; these tests take the same numbers back from the
functions so that a documentation edit cannot silently drift away from what
``python -m tools.audit`` actually computes.
"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit import criticality, grading_kernel  # noqa: E402
from audit.audit_domain import CONSTRAINTS, dedup, judge, raw  # noqa: E402
from audit.grading_kernel import (  # noqa: E402
    RULES_V0,
    RULES_V1,
    W,
    W_V1,
)


def kept(witnesses):
    """Configurations that survive C1/P1/P2 (E1/E3/E4 in the specification)."""
    pool = [c for c in raw(witnesses) if all(p(c) for _, p, _ in CONSTRAINTS)]
    return pool


def tally(rules, domain):
    out = {"unique": 0, "under": 0, "conflict": 0}
    for c in domain:
        out[judge(rules, c)[0]] += 1
    return out


class DomainTests(unittest.TestCase):
    def test_v0_space(self):
        pool = kept(list(W))
        self.assertEqual(len(pool), 376)
        self.assertEqual(len(dedup(pool, True)), 168)
        self.assertEqual(len(dedup(pool, False)), 90)

    def test_v1_space(self):
        pool = kept(W_V1)
        self.assertEqual(len(pool), 356)
        self.assertEqual(len(dedup(pool, True)), 160)
        self.assertEqual(len(dedup(pool, False)), 86)

    def test_v0_verdicts(self):
        pool = kept(list(W))
        self.assertEqual(tally(RULES_V0, dedup(pool, True)),
                         {"unique": 118, "under": 16, "conflict": 34})
        self.assertEqual(tally(RULES_V0, dedup(pool, False)),
                         {"unique": 64, "under": 8, "conflict": 18})

    def test_v1_is_fully_determined(self):
        pool = kept(W_V1)
        for wide in (True, False):
            self.assertEqual(tally(RULES_V1, dedup(pool, wide)),
                             {"unique": len(dedup(pool, wide)), "under": 0, "conflict": 0})

    def test_v1_has_fourteen_carriers(self):
        self.assertEqual(len(W_V1), 14)
        self.assertNotIn(grading_kernel.W.CRIT_EDITION, W_V1)


class KernelTests(unittest.TestCase):
    def run_quietly(self, rules, witnesses):
        with contextlib.redirect_stdout(io.StringIO()):
            return grading_kernel.analyze(rules, "test", witnesses=witnesses)

    def test_v0_raw_conflicts(self):
        self.assertEqual(self.run_quietly(RULES_V0, list(W)), (612, 138, 72))

    def test_v1_raw_is_clean(self):
        self.assertEqual(self.run_quietly(RULES_V1, W_V1), (576, 0, 0))


class CriticalityTests(unittest.TestCase):
    def test_v1_wide(self):
        dom = dedup(kept(W_V1), True)
        got = {rid: criticality.pivotal(RULES_V1, dom, rid) for rid, _ in RULES_V1}
        self.assertEqual(got, {
            "R1/R9": 12, "R2": 0, "R3": 0, "R5": 50,
            "R8": 0, "R6/S-6": 2, "R7": 6,
        })

    def test_v1_narrow(self):
        dom = dedup(kept(W_V1), False)
        got = {rid: criticality.pivotal(RULES_V1, dom, rid) for rid, _ in RULES_V1}
        self.assertEqual(got, {
            "R1/R9": 6, "R2": 0, "R3": 0, "R5": 25,
            "R8": 0, "R6/S-6": 1, "R7": 3,
        })


if __name__ == "__main__":
    unittest.main()
