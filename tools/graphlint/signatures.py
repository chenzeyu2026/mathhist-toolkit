# -*- coding: utf-8 -*-
"""加载 edge-signatures.yaml —— 边签名与不变量的唯一真源。"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[2]
SIGNATURES_PATH = REPO_ROOT / "spec" / "framework" / "edge-signatures.yaml"
GRAPH_SCHEMA_PATH = REPO_ROOT / "spec" / "framework" / "graph.schema.json"
OBJECT_SCHEMA_PATH = REPO_ROOT / "spec" / "framework" / "object-model.schema.json"
DOC_PATH = REPO_ROOT / "spec" / "object-model.md"
GRAPH_DIRS = (REPO_ROOT / "spec" / "framework" / "samples",
              REPO_ROOT / "spec" / "framework" / "pilots")

ANY = "*"
LEVELS = ("error", "warning")


@dataclass(frozen=True)
class AttrSpec:
    name: str
    required: bool
    constraint: dict[str, Any]


@dataclass(frozen=True)
class EdgeSig:
    type: str
    gloss: str
    direction: str
    domains: tuple[str, ...]
    ranges: tuple[str, ...]
    directed: bool
    same_class: bool
    symmetric: bool
    acyclic: bool
    weight_sum: bool
    forbid: str
    attributes: tuple[AttrSpec, ...]
    time_required: bool
    require_note_when_to: tuple[str, ...]
    excluded_to: tuple[str, ...]
    reverse_alias: str | None

    def accepts(self, from_type: str, to_type: str) -> bool:
        if from_type not in self.domains:
            return False
        if ANY in self.ranges:
            return to_type not in self.excluded_to
        return to_type in self.ranges


@dataclass(frozen=True)
class Signatures:
    raw: dict[str, Any]
    node_classes: dict[str, dict[str, Any]]
    edges: dict[str, EdgeSig]
    invariants: tuple[dict[str, Any], ...]
    envelope_required: tuple[str, ...]
    structural_checks: tuple[dict[str, Any], ...]
    node_completeness: dict[str, Any]

    @property
    def mutex_rules(self) -> tuple[dict[str, Any], ...]:
        for inv in self.invariants:
            if inv.get("id") == "mutex":
                return tuple(inv.get("rules") or ())
        return ()

    @property
    def conditional_rules(self) -> tuple[dict[str, Any], ...]:
        for inv in self.invariants:
            if inv.get("id") == "conditional_required":
                return tuple(inv.get("rules") or ())
        return ()

    def abbr(self, class_name: str) -> str:
        if class_name == ANY:
            return "任意对象"
        return self.node_classes[class_name]["abbr"]


def _fail(message: str) -> "None":
    raise SystemExit(f"edge-signatures.yaml: {message}")


def load(path: Path = SIGNATURES_PATH) -> Signatures:
    if yaml is None:
        raise SystemExit(
            "缺少 PyYAML，graphlint 无法读取 edge-signatures.yaml；"
            "安装命令：py -3 -m pip install \"PyYAML>=6.0\"（在 tools/ 目录执行）。"
        )
    if not path.exists():
        _fail(f"找不到 {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    node_classes = raw.get("node_classes") or {}
    if not node_classes:
        _fail("node_classes 为空")

    edges: dict[str, EdgeSig] = {}
    for item in raw.get("edges") or []:
        etype = item.get("type")
        if not etype:
            _fail("存在缺少 type 的边签名")
        if etype in edges:
            _fail(f"边类型重复：{etype}")
        domains = tuple(item.get("from") or ())
        ranges = tuple(item.get("to") or ())
        if not domains or not ranges:
            _fail(f"{etype} 的 from/to 不能为空")
        for cls in domains:
            if cls != ANY and cls not in node_classes:
                _fail(f"{etype}.from 引用了未知节点类 {cls}")
        for cls in ranges:
            if cls != ANY and cls not in node_classes:
                _fail(f"{etype}.to 引用了未知节点类 {cls}")
        if ANY in domains:
            _fail(f"{etype}.from 不允许使用 *（from 必须是具体类）")
        attributes = []
        for name, spec in (item.get("attributes") or {}).items():
            spec = dict(spec or {})
            required = bool(spec.pop("required", False))
            attributes.append(AttrSpec(name=name, required=required, constraint=spec))
        edges[etype] = EdgeSig(
            type=etype,
            gloss=item.get("gloss", ""),
            direction=item.get("direction", "有向"),
            domains=domains,
            ranges=ranges,
            directed=bool(item.get("directed", True)),
            same_class=bool(item.get("same_class", False)),
            symmetric=bool(item.get("symmetric", False)),
            acyclic=bool(item.get("acyclic", False)),
            weight_sum=bool(item.get("weight_sum", False)),
            forbid=item.get("forbid", ""),
            attributes=tuple(attributes),
            time_required=bool(item.get("time_required", False)),
            require_note_when_to=tuple(item.get("require_note_when_to") or ()),
            excluded_to=tuple(item.get("excluded_to") or ()),
            reverse_alias=item.get("reverse_alias"),
        )

    invariants = tuple(raw.get("invariants") or ())
    for inv in invariants:
        if inv.get("level") not in LEVELS:
            _fail(f"不变量 {inv.get('id')} 的 level 必须是 error/warning")
        for rule in inv.get("rules") or ():
            if rule.get("level", "error") not in LEVELS:
                _fail(f"规则 {rule.get('id')} 的 level 必须是 error/warning")

    return Signatures(
        raw=raw,
        node_classes=node_classes,
        edges=edges,
        invariants=invariants,
        envelope_required=tuple((raw.get("edge_envelope") or {}).get("required") or ()),
        structural_checks=tuple(raw.get("structural_checks") or ()),
        node_completeness=raw.get("node_completeness") or {"default_level": "warning",
                                                           "strict_level": "error"},
    )


def main() -> int:  # 便于直接自检 YAML
    sig = load()
    print(f"edge-signatures: {len(sig.edges)} 类边，{len(sig.invariants)} 类不变量，"
          f"{len(sig.node_classes)} 类节点")
    return 0


if __name__ == "__main__":
    sys.exit(main())
