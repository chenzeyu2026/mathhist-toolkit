import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mathlint.cli import main  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(argv)
    return code, buf.getvalue()


class CliTests(unittest.TestCase):
    def test_valid_fixture_exits_zero(self):
        code, out = run(["check", str(FIXTURES / "valid.md")])
        self.assertEqual(code, 0)
        self.assertIn("0 error", out)

    def test_invalid_fixture_exits_one(self):
        code, _ = run(["check", str(FIXTURES / "invalid.md")])
        self.assertEqual(code, 1)

    def test_json_output_is_parseable(self):
        code, out = run(["check", str(FIXTURES / "invalid.md"), "--json"])
        payload = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual(payload["tool"]["name"], "mathlint")
        self.assertEqual(payload["mode"], "offline")
        self.assertGreater(payload["summary"]["errors"], 0)
        self.assertIn("issues", payload["files"][0])

    def test_strict_promotes_warn_to_failure(self):
        code_default, _ = run(["check", str(FIXTURES / "edge.md")])
        code_strict, _ = run(["check", str(FIXTURES / "edge.md"), "--strict"])
        self.assertEqual(code_default, 0)
        self.assertEqual(code_strict, 1)

    def test_directory_target(self):
        code, out = run(["check", str(FIXTURES), "--json"])
        payload = json.loads(out)
        self.assertEqual(payload["summary"]["files"], 3)
        self.assertEqual(code, 1)

    def test_missing_path(self):
        code, _ = run(["check", str(FIXTURES / "does-not-exist.md")])
        self.assertEqual(code, 2)

    def test_offline_online_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            main(["check", str(FIXTURES / "valid.md"), "--offline", "--online"])

    def test_stats_present(self):
        _, out = run(["check", str(FIXTURES / "valid.md"), "--json"])
        stats = json.loads(out)["files"][0]["stats"]
        self.assertGreater(stats["tags"], 0)
        self.assertEqual(stats["claims_untagged"], 0)


if __name__ == "__main__":
    unittest.main()
