#!/usr/bin/env python3
"""Cross-platform self-check: run the tests and every acceptance check.

This is the local equivalent of the CI matrix. Run it from anywhere:

    py -3.11 tools/scripts/selfcheck.py      # Windows
    python3 tools/scripts/selfcheck.py       # Linux / macOS

It exits 0 only if the unit tests pass and every fixture reports exactly the
expected error/warn counts.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]

# (target, expected errors, expected warnings)
EXPECTED = [
    ("tests/fixtures/valid.md", 0, 0),
    ("tests/fixtures/invalid.md", 13, 1),
    ("tests/fixtures/edge.md", 0, 4),
    ("../prompts/examples", 0, 0),
]


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        args, cwd=TOOLS, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def main() -> int:
    failures: list[str] = []

    print(f"python {sys.version.split()[0]} on {sys.platform}")
    print("== unit tests ==")
    tests = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"])
    tail = (tests.stderr or tests.stdout).strip().splitlines()[-1:]
    print(f"  {'OK' if tests.returncode == 0 else 'FAILED'}  {tail[0] if tail else ''}")
    if tests.returncode != 0:
        failures.append("unit tests")

    print("== fixtures and examples ==")
    for target, want_err, want_warn in EXPECTED:
        proc = run([sys.executable, "-m", "mathlint", "check", target, "--json"])
        try:
            payload = json.loads(proc.stdout)
            summary = payload["summary"]
            got_err, got_warn = summary["errors"], summary["warns"]
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"  FAIL  {target}: cannot parse JSON ({exc})")
            failures.append(target)
            continue
        ok = (got_err, got_warn) == (want_err, want_warn)
        print(
            f"  {'PASS' if ok else 'FAIL'}  {target:<28} "
            f"expected {want_err} error / {want_warn} warn, got {got_err} / {got_warn}"
        )
        if not ok:
            failures.append(target)

    print()
    if failures:
        print(f"self-check FAILED: {', '.join(failures)}")
        return 1
    print("self-check PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
