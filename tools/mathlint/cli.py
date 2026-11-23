"""Command line interface: mathlint check <path> [--offline|--online] [--json] [--strict]."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path

from . import __version__
from .checks import check_file
from .parser import Issue

SEVERITIES = ("error", "warn", "info")


def _setup_console() -> None:
    if os.name == "nt" and sys.stdout.isatty():
        try:
            import ctypes

            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        except Exception:  # noqa: BLE001 - best effort only
            pass
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass


def collect_files(target: Path) -> list[Path]:
    target = target.resolve()
    if target.is_file():
        return [target]
    files = [
        p
        for p in target.rglob("*.md")
        if not any(part.startswith(".") and part not in (".", "..") for part in p.relative_to(target).parts)
    ]
    return sorted(files)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mathlint",
        description="证据标记检查器（A/S/U/F）。规范见 spec/evidence-tags.md。",
    )
    parser.add_argument("--version", action="version", version=f"mathlint {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="检查文件或目录里的证据标记")
    check.add_argument("target", help="Markdown 文件或目录")
    mode = check.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true", help="只做本地校验（默认）")
    mode.add_argument("--online", action="store_true", help="额外探测链接存活与 DOI 解析")
    check.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    check.add_argument("--strict", action="store_true", help="warn 也视为失败（非零退出码）")
    return parser


def run_check(args: argparse.Namespace) -> int:
    target = Path(args.target)
    if not target.exists():
        print(f"mathlint: 路径不存在：{target}", file=sys.stderr)
        return 2

    files = collect_files(target)
    if not files:
        print(f"mathlint: 没有找到 Markdown 文件：{target}", file=sys.stderr)
        return 2

    mode = "online" if args.online else "offline"
    file_reports = []
    probe_log: list[dict] = []
    totals = {sev: 0 for sev in SEVERITIES}

    for path in files:
        result = check_file(str(path))
        issues: list[Issue] = list(result.issues)
        if args.online:
            from .online import probe

            online_issues, log = probe(str(path), result.tags)
            issues.extend(online_issues)
            probe_log.extend({"file": str(path), **entry} for entry in log)
        issues.sort(key=lambda i: (i.line, i.col, i.code))

        counts = {sev: sum(1 for i in issues if i.severity == sev) for sev in SEVERITIES}
        for sev in SEVERITIES:
            totals[sev] += counts[sev]
        file_reports.append(
            {
                "path": str(path),
                "stats": {
                    "errors": counts["error"],
                    "warns": counts["warn"],
                    "infos": counts["info"],
                    "tags": len(result.tags),
                    "claims_total": result.units_total,
                    "claims_untagged": result.units_untagged,
                },
                "issues": [
                    {
                        "code": i.code,
                        "severity": i.severity,
                        "line": i.line,
                        "col": i.col,
                        "message": i.message,
                        "evidence": i.evidence,
                    }
                    for i in issues
                ],
            }
        )

    exit_code = 1 if totals["error"] else (1 if (args.strict and totals["warn"]) else 0)

    if args.json:
        payload = {
            "tool": {"name": "mathlint", "version": __version__},
            "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "mode": mode,
            "strict": bool(args.strict),
            "files": file_reports,
            "summary": {
                "files": len(file_reports),
                "errors": totals["error"],
                "warns": totals["warn"],
                "infos": totals["info"],
                "exit_code": exit_code,
            },
            "probes": probe_log,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return exit_code

    print(f"mathlint {__version__} · mode={mode} · files={len(file_reports)}")
    for report in file_reports:
        stats = report["stats"]
        print(f"\n{report['path']}")
        print(
            f"  标记 {stats['tags']} 条 · 论断 {stats['claims_total']} 段"
            f"（无标记 {stats['claims_untagged']} 段）"
        )
        if not report["issues"]:
            print("  无问题")
        for issue in report["issues"]:
            evidence = f"  «{issue['evidence']}»" if issue["evidence"] else ""
            print(f"  L{issue['line']}:{issue['col']}  {issue['severity']:<5} {issue['code']:<22} {issue['message']}{evidence}")
        print(f"  → {stats['errors']} error / {stats['warns']} warn / {stats['infos']} info")

    print(
        f"\n合计：{totals['error']} error / {totals['warn']} warn / {totals['info']} info"
        f" · exit={exit_code}"
    )
    if args.strict:
        print("--strict 已启用：warn 也会导致非零退出码")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    _setup_console()
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        return run_check(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
