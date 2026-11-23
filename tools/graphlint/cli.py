# -*- coding: utf-8 -*-
"""graphlint CLI。

用法（在 tools/ 目录）：
  py -3 -m graphlint check <文件或目录>... [--strict] [--json] [--max-items N]
  py -3 -m graphlint check-all [--strict] [--json]
  py -3 -m graphlint generate [--check]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from . import __version__
from .checks import Issue, Result, check_global_ids, check_graph, load_graph
from .generate import generate
from .signatures import GRAPH_DIRS, REPO_ROOT, Signatures, load, load_branch_ids


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _collect(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.json") if load_graph(p)))
        else:
            files.append(path)
    seen: set[Path] = set()
    out = []
    for path in files:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(path)
    return out


def _check(paths: Iterable[str], sig: Signatures, strict: bool,
           global_ids: bool = False) -> list[Result]:
    results = []
    loaded: list[tuple[str, dict]] = []
    for path in _collect(paths):
        graph = load_graph(path)
        if graph is None:
            continue
        rel = _rel(path)
        results.append(check_graph(graph, sig, rel, strict=strict))
        loaded.append((rel, graph))
    if global_ids:
        by_file = {r.file: r for r in results}
        for issue in check_global_ids(loaded, catalog_ids=load_branch_ids()):
            target = by_file.get(issue.file)
            if target is not None:
                target.add(issue)
    return results


def _print_text(sig: Signatures, results: list[Result], max_items: int) -> None:
    errors = [(r, i) for r in results for i in r.errors]
    warnings = [(r, i) for r in results for i in r.warnings]

    def dump(title: str, items: list[tuple[Result, Issue]]) -> None:
        print(f"== {title}（{len(items)}）==")
        shown = items if max_items == 0 else items[:max_items]
        for result, issue in shown:
            where = issue.edge or issue.node or "—"
            print(f"  [{issue.code}] {result.file} :: {where}")
            if issue.pointer:
                print(f"      位置: {issue.pointer}")
            print(f"      说明: {issue.message}")
            if issue.actual is not None:
                print(f"      实际: {issue.actual}")
            if issue.expected is not None:
                print(f"      期望: {issue.expected}")
            if issue.detail:
                print(f"      依据: {issue.detail}")
        if len(items) > len(shown):
            print(f"  …… 其余 {len(items) - len(shown)} 条（用 --max-items 0 全部显示）")
        print()

    print(f"graphlint {__version__} · edge-signatures v{sig.raw.get('version')} · "
          f"files={len(results)}")
    dump("error", errors)
    dump("warning", warnings)
    print("按文件：")
    for r in results:
        print(f"  {r.file}: error {len(r.errors)} / warning {len(r.warnings)}")
    total_e = sum(len(r.errors) for r in results)
    total_w = sum(len(r.warnings) for r in results)
    total_n = sum(r.node_count for r in results)
    total_edges = sum(r.edge_count for r in results)
    print(f"汇总：error {total_e} / warning {total_w} · files {len(results)} / "
          f"nodes {total_n} / edges {total_edges}")


def _json_payload(results: list[Result], strict: bool) -> dict:
    return {
        "tool": {"name": "graphlint", "version": __version__},
        "strict": strict,
        "files": [
            {
                "path": r.file,
                "nodes": r.node_count,
                "edges": r.edge_count,
                "errors": len(r.errors),
                "warnings": len(r.warnings),
                "issues": [i.as_dict() for i in r.issues],
            }
            for r in results
        ],
        "summary": {
            "files": len(results),
            "nodes": sum(r.node_count for r in results),
            "edges": sum(r.edge_count for r in results),
            "errors": sum(len(r.errors) for r in results),
            "warnings": sum(len(r.warnings) for r in results),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="graphlint", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=f"graphlint {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="校验单个文件或目录")
    check.add_argument("targets", nargs="+")
    check.add_argument("--strict", action="store_true",
                       help="节点完整性 warning 升为 error，并让 warning 也返回非零")
    check.add_argument("--json", action="store_true")
    check.add_argument("--max-items", type=int, default=25,
                       help="每个级别最多显示多少条；0 表示全部（默认 25）")

    all_parser = sub.add_parser("check-all", help="校验 spec/framework/samples 与 pilots")
    all_parser.add_argument("--strict", action="store_true")
    all_parser.add_argument("--json", action="store_true")
    all_parser.add_argument("--max-items", type=int, default=25)

    gen = sub.add_parser("generate", help="从 edge-signatures.yaml 生成 schema 与文档表格")
    gen.add_argument("--check", action="store_true", help="只检查生成物是否最新，不写文件")

    args = parser.parse_args(argv)

    if args.command == "generate":
        return generate(check=args.check)

    sig = load()
    strict = bool(getattr(args, "strict", False))
    if args.command == "check-all":
        targets = [str(p) for p in GRAPH_DIRS]
    else:
        targets = args.targets
    results = _check(targets, sig, strict, global_ids=(args.command == "check-all"))
    if not results:
        print("没有找到图包（含 nodes/edges 的 JSON）。", file=sys.stderr)
        return 2

    if getattr(args, "json", False):
        print(json.dumps(_json_payload(results, strict), ensure_ascii=False, indent=2))
    else:
        _print_text(sig, results, getattr(args, "max_items", 25))

    errors = sum(len(r.errors) for r in results)
    warnings = sum(len(r.warnings) for r in results)
    if errors:
        return 1
    if strict and warnings:
        return 1
    return 0
