# -*- coding: utf-8 -*-
"""图包校验：签名（定义域/值域）、不变量、节点完整性。

全部规则由 edge-signatures.yaml 驱动；本文件只实现判定方法，不重复规则文本。
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .signatures import (ANY, OBJECT_SCHEMA_PATH, EdgeSig, Signatures)

EDGE_ID_RE = re.compile(r"^E:[^>]+>[a-z_]+>[^>]+(#[0-9]+)?$")

# 目录投影边：两端都是 branches.json 里的分支时，边由目录生成，可跨图包同名。
CATALOG_EDGE_TYPES = frozenset({"parent_of", "cross_class"})


@dataclass
class Issue:
    level: str
    code: str
    message: str
    file: str
    edge: str | None = None
    node: str | None = None
    actual: str | None = None
    expected: str | None = None
    detail: str | None = None
    rule_id: str | None = None
    pointer: str | None = None
    severity: str | None = None

    def __post_init__(self) -> None:
        if self.rule_id is None:
            self.rule_id = self.code
        if self.severity is None:
            self.severity = self.level
        if self.pointer is None:
            self.pointer = ""

    def as_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class Result:
    file: str
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    node_count: int = 0
    edge_count: int = 0

    def add(self, issue: Issue) -> None:
        (self.errors if issue.level == "error" else self.warnings).append(issue)

    @property
    def issues(self) -> list[Issue]:
        return self.errors + self.warnings


def _classes(sig: Signatures, names: Iterable[str]) -> str:
    out = []
    for name in names:
        if name == ANY:
            out.append("任意对象")
        else:
            out.append(f"{sig.abbr(name)}（{sig.node_classes[name]['label']}）")
    return " / ".join(out)


def _describe_node(node_id: str | None, node_type: str | None) -> str:
    if node_id is None:
        return "（不存在）"
    if node_type is None:
        return f"{node_id}（节点不存在）"
    return f"{node_type}（{node_id}）"


def _load_object_schema() -> dict[str, Any]:
    return json.loads(OBJECT_SCHEMA_PATH.read_text(encoding="utf-8"))


def _type_required(schema: dict[str, Any]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for rule in schema.get("allOf") or ():
        cond = (rule.get("if") or {}).get("properties", {}).get("type", {}).get("const")
        if cond:
            out[cond] = list((rule.get("then") or {}).get("required") or ())
    return out


def _check_node_completeness(graph: dict[str, Any], sig: Signatures,
                             file: str, strict: bool) -> list[Issue]:
    level = sig.node_completeness.get("strict_level", "error") if strict \
        else sig.node_completeness.get("default_level", "warning")
    schema = _load_object_schema()
    base_required = list(schema.get("required") or ())
    per_type = _type_required(schema)
    issues: list[Issue] = []

    for node in graph.get("nodes") or []:
        nid = node.get("id")
        ntype = node.get("type")
        missing: list[str] = [f for f in base_required if node.get(f) is None]
        for f in per_type.get(ntype, ()):
            if node.get(f) is None:
                missing.append(f)
        labels = node.get("labels")
        if isinstance(labels, dict) and not labels.get("zh"):
            missing.append("labels.zh")
        for i, claim in enumerate(node.get("claims") or []):
            if not isinstance(claim, dict):
                missing.append(f"claims[{i}]")
                continue
            for f in ("id", "statement", "grade", "attestation", "source"):
                if claim.get(f) is None:
                    missing.append(f"claims[{i}].{f}")
            src = claim.get("source")
            if isinstance(src, dict) and not src.get("locator"):
                missing.append(f"claims[{i}].source.locator")
        prov = node.get("provenance")
        if isinstance(prov, dict):
            for f in ("created_by", "created_at", "schema_version"):
                if prov.get(f) is None:
                    missing.append(f"provenance.{f}")
        missing = list(dict.fromkeys(missing))
        if missing:
            shown = "、".join(missing[:8]) + ("…" if len(missing) > 8 else "")
            issues.append(Issue(
                level=level, code="NODE_REQUIRED", file=file, node=nid,
                message=f"节点缺少必填字段：{shown}",
                actual=f"缺失 {len(missing)} 项", expected="上述字段必填（object-model.schema.json）",
                detail="既有样例的历史欠账；默认按 warning 报告，--strict 升为 error。",
            ))
    return issues


def _check_edge_id(edge: dict[str, Any], file: str) -> Issue | None:
    eid = edge.get("id") or ""
    if not EDGE_ID_RE.match(eid):
        return Issue(level="error", code="EDGE_ID_FORMAT", file=file, edge=eid,
                     message="边 ID 不符合 E:<from>><type>><to> 形式",
                     actual=eid or "（空）", expected="E:<from>><type>><to>，平行边加 #2/#3")
    parts = eid.split(">")
    if len(parts) != 3:
        return Issue(level="error", code="EDGE_ID_FORMAT", file=file, edge=eid,
                     message="边 ID 的 > 分隔段数不为 3",
                     actual=f"{len(parts)} 段", expected="3 段：from、type、to")
    frm = parts[0][2:]
    etype = parts[1]
    to = re.sub(r"#\d+$", "", parts[2])
    if etype != edge.get("type") or frm != edge.get("from") or to != edge.get("to"):
        return Issue(level="error", code="EDGE_ID_DERIVATION", file=file, edge=eid,
                     message="边 ID 与 from/type/to 不一致",
                     actual=f"E:{frm}>{etype}>{to}",
                     expected=f"E:{edge.get('from')}>{edge.get('type')}>{edge.get('to')}")
    return None


def _try_reverse(sig: Signatures, esig: EdgeSig, ft: str, tt: str) -> Issue | None:
    """端点不合法时，判断是否为方向写反或用错边类型。"""
    if esig.accepts(tt, ft):
        return Issue(
            level="error", code="REVERSE_DIRECTION", edge=None, file="",
            message=f"方向疑似写反：{esig.type} 声明的方向是 {_classes(sig, esig.domains)} → "
                    f"{_classes(sig, esig.ranges)}，实得 {ft} → {tt}。",
            actual=f"{ft} → {tt}",
            expected=f"{_classes(sig, esig.domains)} → {_classes(sig, esig.ranges)}",
        )
    alias = sig.edges.get(esig.reverse_alias or "")
    if alias and alias.accepts(ft, tt):
        return Issue(
            level="error", code="WRONG_EDGE_TYPE", edge=None, file="",
            message=f"端点组合符合 `{alias.type}` 的签名，请确认是否用错边类型："
                    f"`{esig.type}` 声明 {_classes(sig, esig.domains)} → {_classes(sig, esig.ranges)}。",
            actual=f"{esig.type}: {ft} → {tt}",
            expected=f"若要表达这一方向，改用 `{alias.type}`",
        )
    return None


def _check_cycles(graph: dict[str, Any], sig: Signatures, file: str) -> list[Issue]:
    edges = graph.get("edges") or []
    issues: list[Issue] = []
    seen: set[tuple[str, frozenset[str]]] = set()
    for etype, esig in sig.edges.items():
        if not esig.acyclic:
            continue
        adj: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for e in edges:
            if e.get("type") == etype and e.get("from") and e.get("to"):
                adj[e["from"]].append((e["to"], e.get("id") or ""))
        color: dict[str, int] = {}

        def dfs(u: str, path_nodes: list[str], path_edges: list[str]) -> None:
            color[u] = 1
            for v, eid in adj.get(u, ()):
                if color.get(v) == 1:
                    idx = path_nodes.index(v)
                    cyc_nodes = path_nodes[idx:] + [v]
                    key = (etype, frozenset(cyc_nodes))
                    if key in seen:
                        continue
                    seen.add(key)
                    cyc_edges = path_edges[idx:] + [eid]
                    issues.append(Issue(
                        level="error", code="CYCLE", file=file, edge=eid,
                        message=f"{etype} 成环：{' → '.join(cyc_nodes)}（边 {'、'.join(cyc_edges)}）",
                        actual=f"{len(cyc_nodes) - 1} 条边闭合",
                        expected=f"{etype} 子图无环",
                    ))
                elif color.get(v, 0) == 0:
                    dfs(v, path_nodes + [v], path_edges + [eid])
            color[u] = 2

        for node in list(adj):
            if color.get(node, 0) == 0:
                dfs(node, [node], [])
    return issues


def _check_weights(graph: dict[str, Any], file: str) -> list[Issue]:
    sums: dict[str, float] = defaultdict(float)
    missing: set[str] = set()
    for e in graph.get("edges") or []:
        if e.get("type") != "parent_of":
            continue
        to = e.get("to")
        w = e.get("weight")
        if isinstance(w, (int, float)) and not isinstance(w, bool):
            sums[to] += float(w)
        else:
            missing.add(to)
    issues = []
    for child, total in sums.items():
        if child in missing:
            continue
        if abs(total - 1.0) > 0.01:
            issues.append(Issue(
                level="error", code="WEIGHT_SUM", file=file, node=child,
                message=f"parent_of 入边权重和 {total:.2f} ≠ 1.00",
                actual=f"{total:.2f}", expected="1.00（容差 ±0.01）",
                detail="同一子节点的父边必须归一；无父的根节点不参与。",
            ))
    return issues


def _check_witness(graph: dict[str, Any], file: str) -> list[Issue]:
    counts: dict[str, int] = defaultdict(int)
    for e in graph.get("edges") or []:
        if e.get("type") == "witness_of":
            counts[e.get("from")] += 1
    issues = []
    for node in graph.get("nodes") or []:
        if node.get("type") != "witness":
            continue
        n = counts.get(node.get("id"), 0)
        if n != 1:
            issues.append(Issue(
                level="error", code="WITNESS_UNIQUE", file=file, node=node.get("id"),
                message=f"见证 {node.get('id')} 的 witness_of 出边数为 {n}",
                actual=str(n), expected="正好 1",
                detail="每条见证必须且只能挂一个 TX。",
            ))
    return issues


def _check_mutex(graph: dict[str, Any], sig: Signatures, file: str) -> list[Issue]:
    by_pair: dict[tuple[str, str], set[str]] = defaultdict(set)
    for e in graph.get("edges") or []:
        if e.get("from") and e.get("to"):
            by_pair[(e["from"], e["to"])].add(e.get("type"))
    issues = []
    for rule in sig.mutex_rules:
        a, b = (rule.get("pair") or [None, None])[:2]
        if not a or not b:
            continue
        level = rule.get("level", "warning")
        reported: set[tuple[str, str]] = set()
        for (frm, to), types in by_pair.items():
            if a in types and b in types and (frm, to) not in reported:
                reported.add((frm, to))
                issues.append(Issue(
                    level=level, code=f"MUTEX_{rule.get('id', 'rule').upper()}",
                    file=file, edge=None,
                    message=rule.get("message", f"同一对端点上同时存在 {a} 与 {b}"),
                    actual=f"{frm} → {to}: {a} + {b}",
                    expected="若两者描述同一关系，只保留一条；若确为不同关系，保留并在 note 说明",
                    detail=rule.get("note"),
                ))
            if rule.get("id") == "prerequisite_vs_parent" and a in types \
                    and b in by_pair.get((to, frm), set()) and (frm, to) not in reported:
                reported.add((frm, to))
                issues.append(Issue(
                    level=level, code=f"MUTEX_{rule.get('id', 'rule').upper()}",
                    file=file, edge=None,
                    message=rule.get("message", f"同一对端点上同时存在 {a} 与反向 {b}"),
                    actual=f"{frm} → {to}: {a}；{to} → {frm}: {b}",
                    expected="先学顺序与从属关系分开表达，确认不是混用",
                    detail=rule.get("note"),
                ))
    return issues


def _check_isolation(graph: dict[str, Any], file: str) -> list[Issue]:
    touched = set()
    for e in graph.get("edges") or []:
        touched.add(e.get("from"))
        touched.add(e.get("to"))
    issues = []
    for node in graph.get("nodes") or []:
        nid = node.get("id")
        if node.get("type") == "branch" or node.get("status") == "proposed":
            continue
        if nid not in touched:
            issues.append(Issue(
                level="error", code="ISOLATED_NODE", file=file, node=nid,
                message=f"节点 {nid} 没有任何入边或出边",
                actual="0 条边", expected="至少 1 条",
                detail="只有分支根节点与 proposed 节点允许孤立。",
            ))
    return issues


def _check_claim_sources(graph: dict[str, Any], file: str) -> list[Issue]:
    ids = {n.get("id") for n in graph.get("nodes") or []}
    issues = []
    for node in graph.get("nodes") or []:
        for claim in node.get("claims") or []:
            if not isinstance(claim, dict):
                continue
            src = claim.get("source") or {}
            text = src.get("text") if isinstance(src, dict) else None
            if isinstance(text, str) and text.startswith("TX:") and text not in ids \
                    and claim.get("grade") != "U":
                issues.append(Issue(
                    level="error", code="CLAIM_TEXT_MISSING", file=file,
                    node=node.get("id"),
                    message=f"claim {claim.get('id')} 引用的 {text} 不在图包内，grade 为 {claim.get('grade')}",
                    actual=f"text={text}, grade={claim.get('grade')}",
                    expected="TX 存在，或 grade=U",
                    detail="按 §5.6 B.7：引用图外文本时该断言只能标 U。",
                ))
    return issues


def _check_attestation(edge: dict[str, Any], file: str) -> list[Issue]:
    issues = []
    eid = edge.get("id")
    att = edge.get("attestation")
    grade = edge.get("grade")
    note = edge.get("note")
    if att == "textbook_simplification" and grade not in ("F", "U"):
        issues.append(Issue(
            level="error", code="ATTESTATION_GRADE_CAP", file=file, edge=eid,
            message=f"attestation=textbook_simplification 时 grade 上限不满足：实得 {grade}"
                    "（期望 F 或 U）。教材/科普转述不能支撑 A/S 级断言。",
            actual=f"attestation={att}, grade={grade}", expected="grade ∈ {F, U}",
            detail="要么把 attestation 改成实际来源（direct/contemporary_report/later_report），"
                   "要么按教材转述把 grade 降到 F；不要为了过关冒充一手文献。",
        ))
    if att == "later_report" and grade == "A":
        issues.append(Issue(
            level="error", code="LATER_REPORT_GRADE_CAP", file=file, edge=eid,
            message="attestation=later_report 时 grade 不得为 A：实得 A（期望 S/U/F）。"
                    "后世研究者叙述不能当作亲见原件。",
            actual=f"attestation={att}, grade={grade}", expected="grade ∈ {S, U, F}",
        ))
    if grade == "U" and not (isinstance(note, str) and note.strip()):
        issues.append(Issue(
            level="error", code="UNKNOWN_GRADE_NOTE", file=file, edge=eid,
            message="grade=U 时必须写 note：说明未核实的依据缺口与下一步查证路径。",
            actual="note 为空", expected="非空 note",
        ))
    if not edge.get("source") and not edge.get("claimant"):
        issues.append(Issue(
            level="error", code="SOURCE_OR_CLAIMANT", file=file, edge=eid,
            message="边必须给出 source 或 claimant：没有来源也没有主张者的关系不可核。",
            actual="两者皆空", expected="source 或 claimant 至少一项",
        ))
    return issues


def check_graph(graph: dict[str, Any], sig: Signatures, file: str,
                strict: bool = False) -> Result:
    result = Result(file=file, node_count=len(graph.get("nodes") or []),
                    edge_count=len(graph.get("edges") or []))
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []

    node_type: dict[str, str] = {}
    for i, node in enumerate(nodes):
        nid = node.get("id")
        ntype = node.get("type")
        if nid in node_type:
            result.add(Issue(level="error", code="NODE_ID_DUPLICATE", file=file, node=nid,
                             pointer=f"/nodes/{i}",
                             message=f"节点 ID 重复：{nid}（同一图包内）",
                             actual="重复", expected="同一图包内唯一；跨文件由 check-all 判定"))
            continue
        node_type[nid] = ntype
        cls = sig.node_classes.get(ntype)
        if cls is None:
            result.add(Issue(level="error", code="NODE_TYPE_UNKNOWN", file=file, node=nid,
                             message=f"节点 {nid} 的类型 `{ntype}` 未登记",
                             actual=str(ntype), expected="14 类节点之一"))
        elif not re.match(cls["pattern"], nid or ""):
            result.add(Issue(level="error", code="NODE_ID_PREFIX", file=file, node=nid,
                             message=f"节点 ID 前缀与 type 不一致：{nid} 的类型是 {ntype}",
                             actual=str(nid), expected=cls["pattern"]))

    for issue in _check_node_completeness(graph, sig, file, strict):
        result.add(issue)

    symmetric_pairs: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    edge_ids: set[Any] = set()

    for i, edge in enumerate(edges):
        eid = edge.get("id")
        if eid in edge_ids:
            result.add(Issue(level="error", code="EDGE_ID_DUPLICATE", file=file, edge=eid,
                             pointer=f"/edges/{i}",
                             message=f"边 ID 重复：{eid}（同一图包内）",
                             actual="重复", expected="同一图包内唯一；跨文件由 check-all 判定"))
        else:
            edge_ids.add(eid)
        missing = [f for f in sig.envelope_required if edge.get(f) is None]
        if missing:
            result.add(Issue(level="error", code="EDGE_REQUIRED", file=file, edge=eid,
                             message=f"边缺少信封字段：{'、'.join(missing)}",
                             actual=f"缺失 {len(missing)} 项",
                             expected=f"必填：{'、'.join(sig.envelope_required)}"))
            continue

        id_issue = _check_edge_id(edge, file)
        if id_issue:
            result.add(id_issue)

        frm, to = edge.get("from"), edge.get("to")
        ft, tt = node_type.get(frm), node_type.get(to)
        if ft is None or tt is None:
            result.add(Issue(level="error", code="ENDPOINT_MISSING", file=file, edge=eid,
                             message=f"端点不在图包内：from={_describe_node(frm, ft)}；"
                                     f"to={_describe_node(to, tt)}",
                             actual=f"{frm} / {to}", expected="两端都必须是本图包节点"))
            continue

        esig = sig.edges.get(edge.get("type"))
        if esig is None:
            result.add(Issue(level="error", code="EDGE_TYPE_UNKNOWN", file=file, edge=eid,
                             message=f"边类型 `{edge.get('type')}` 未登记",
                             actual=str(edge.get("type")),
                             expected="edge-signatures.yaml 中 31 类之一"))
            continue

        if frm == to:
            result.add(Issue(level="error", code="SELF_LOOP", file=file, edge=eid,
                             message=f"自环：{frm} —{esig.type}→ 自身",
                             actual=frm, expected="from ≠ to"))

        if not esig.accepts(ft, tt):
            if ANY in esig.ranges and tt in esig.excluded_to:
                result.add(Issue(
                    level="error", code="RANGE_EXCLUDED", file=file, edge=eid,
                    message=f"`{esig.type}` 的 to 不接受 {tt}（{to}）",
                    actual=f"to={_describe_node(to, tt)}",
                    expected=f"任意对象，但不含 {_classes(sig, esig.excluded_to)}",
                    detail="教学挂点只做索引，不进入证据链。",
                ))
            else:
                hint = _try_reverse(sig, esig, ft, tt)
                if hint:
                    hint.file = file
                    hint.edge = eid
                    result.add(hint)
                else:
                    bad = []
                    if ft not in esig.domains:
                        bad.append(f"from 实际为 {_describe_node(frm, ft)}，期望 {_classes(sig, esig.domains)}")
                    if (tt in esig.excluded_to) or (ANY not in esig.ranges and tt not in esig.ranges):
                        bad.append(f"to 实际为 {_describe_node(to, tt)}，期望 {_classes(sig, esig.ranges)}")
                    result.add(Issue(
                        level="error", code="ENDPOINT_TYPE", file=file, edge=eid,
                        message=f"`{esig.type}` 的端点类型不满足签名：" + "；".join(bad),
                        actual=f"{ft} → {tt}",
                        expected=f"{_classes(sig, esig.domains)} → {_classes(sig, esig.ranges)}",
                        detail=f"声明方向：{esig.direction}。{esig.forbid}",
                    ))
        elif esig.same_class and ft != tt:
            result.add(Issue(
                level="error", code="HOMOTYPIC", file=file, edge=eid,
                message=f"`{esig.type}` 要求两端同型：实得 {ft} → {tt}",
                actual=f"{ft} → {tt}", expected=f"{_classes(sig, esig.domains)} → 同类型",
            ))

        if esig.symmetric:
            if edge.get("directed") is not False:
                result.add(Issue(level="error", code="SYMMETRIC_DIRECTED", file=file, edge=eid,
                                 message=f"对称边 `{esig.type}` 必须 directed: false",
                                 actual=f"directed={edge.get('directed')}", expected="false"))
            if str(frm) > str(to):
                result.add(Issue(level="error", code="SYMMETRIC_ORDER", file=file, edge=eid,
                                 message=f"对称边只存一条，from 取 ID 字典序较小者：{frm} > {to}",
                                 actual=f"{frm} → {to}", expected=f"{to} → {frm}"))
            symmetric_pairs[(edge.get("type"), frozenset((frm, to)))].append(edge)

        for attr in esig.attributes:
            value = edge.get(attr.name)
            if value is None:
                if attr.required:
                    result.add(Issue(
                        level="error", code="ATTR_REQUIRED", file=file, edge=eid,
                        message=f"`{esig.type}` 缺少必填属性 `{attr.name}`",
                        actual="未给出", expected=_attr_expected(attr.constraint),
                    ))
                continue
            if "type" in attr.constraint:
                wanted = attr.constraint["type"]
                if wanted == "number" and (not isinstance(value, (int, float)) or isinstance(value, bool)):
                    result.add(Issue(level="error", code="ATTR_TYPE", file=file, edge=eid,
                                     message=f"`{attr.name}` 必须是数值",
                                     actual=repr(value), expected="number"))
                    continue
            if "enum" in attr.constraint and value not in attr.constraint["enum"]:
                result.add(Issue(
                    level="error", code="ATTR_ENUM", file=file, edge=eid,
                    message=f"`{attr.name}` 取值不在允许集合：实得 {value}",
                    actual=str(value), expected=" / ".join(attr.constraint["enum"]),
                ))
            if "minimum" in attr.constraint and isinstance(value, (int, float)) \
                    and value < attr.constraint["minimum"]:
                result.add(Issue(level="error", code="ATTR_RANGE", file=file, edge=eid,
                                 message=f"`{attr.name}` 小于下限",
                                 actual=str(value), expected=f"≥ {attr.constraint['minimum']}"))
            if "maximum" in attr.constraint and isinstance(value, (int, float)) \
                    and value > attr.constraint["maximum"]:
                result.add(Issue(level="error", code="ATTR_RANGE", file=file, edge=eid,
                                 message=f"`{attr.name}` 大于上限",
                                 actual=str(value), expected=f"≤ {attr.constraint['maximum']}"))

        if esig.time_required:
            t = edge.get("time") or {}
            if t.get("from") is None and t.get("to") is None and t.get("precision") != "unknown":
                result.add(Issue(
                    level="error", code="TIME_REQUIRED", file=file, edge=eid,
                    message=f"`{esig.type}` 的 time 至少一端非 null，或 precision=unknown 且 note 说明原因",
                    actual=f"from={t.get('from')}, to={t.get('to')}, precision={t.get('precision')}",
                    expected="from/to 至少一端非 null；或 unknown + note",
                ))

        if tt in esig.require_note_when_to and not (isinstance(edge.get("note"), str)
                                                   and edge.get("note").strip()):
            result.add(Issue(
                level="error", code="NOTE_REQUIRED", file=file, edge=eid,
                message=f"`{esig.type}` 指向 {tt} 时 note 必填",
                actual="note 为空", expected="非空 note，写明为何不挂更具体的对象",
            ))

        if ft == "teaching_point" or tt == "teaching_point":
            if not (esig.type == "anchors" and ft == "teaching_point"):
                end = "from" if ft == "teaching_point" else "to"
                result.add(Issue(
                    level="error", code="TP_EXCLUDED", file=file, edge=eid,
                    message=f"教学挂点只做索引：`{esig.type}` 把 TP 放在 {end} 端",
                    actual=_describe_node(frm if end == "from" else to, "teaching_point"),
                    expected="TP 只能作为 anchors 的 from",
                ))

        for issue in _check_attestation(edge, file):
            result.add(issue)

    for (etype, pair), group in symmetric_pairs.items():
        if len(group) > 1:
            result.add(Issue(level="error", code="SYMMETRIC_DUPLICATE", file=file,
                             edge=group[1].get("id"),
                             message=f"对称边 `{etype}` 在同一对端点上写了 {len(group)} 条",
                             actual="、".join(str(e.get("id")) for e in group),
                             expected="只写一条"))

    for issue in _check_cycles(graph, sig, file):
        result.add(issue)
    for issue in _check_weights(graph, file):
        result.add(issue)
    for issue in _check_witness(graph, file):
        result.add(issue)
    for issue in _check_mutex(graph, sig, file):
        result.add(issue)
    for issue in _check_isolation(graph, file):
        result.add(issue)
    for issue in _check_claim_sources(graph, file):
        result.add(issue)
    _attach_pointers(result, graph)
    return result


def _attach_pointers(result: Result, graph: dict[str, Any]) -> None:
    """把 node/edge 标识换成 RFC 6901 JSON Pointer；文件级问题指向根。"""
    node_index: dict[Any, int] = {}
    for i, node in enumerate(graph.get("nodes") or []):
        nid = node.get("id")
        if nid not in node_index:
            node_index[nid] = i
    edge_index: dict[Any, int] = {}
    for i, edge in enumerate(graph.get("edges") or []):
        eid = edge.get("id")
        if eid not in edge_index:
            edge_index[eid] = i
    for issue in result.issues:
        if issue.pointer:
            continue
        if issue.edge is not None and issue.edge in edge_index:
            issue.pointer = f"/edges/{edge_index[issue.edge]}"
        elif issue.node is not None and issue.node in node_index:
            issue.pointer = f"/nodes/{node_index[issue.node]}"
        else:
            issue.pointer = ""


def check_global_ids(items: Iterable[tuple[str, dict[str, Any]]],
                     catalog_ids: frozenset[str] = frozenset()) -> list[Issue]:
    """跨图包检查节点/边 ID 是否重复；单文件内重复由 check_graph 负责。

    `catalog_ids` 是 branches.json 的分支目录 ID。分支节点是目录在各图包里的投影，
    同一分支必然出现在多个图包中；按目录 ID 豁免，避免把目录投影当成数据重复。
    `parent_of` / `cross_class` 两端都是目录分支的边同样由目录生成，一并豁免。
    """
    issues: list[Issue] = []
    node_seen: dict[Any, tuple[str, str]] = {}
    edge_seen: dict[Any, tuple[str, str]] = {}

    for file, graph in items:
        for i, node in enumerate(graph.get("nodes") or []):
            nid = node.get("id")
            if not nid or nid in catalog_ids:
                continue
            pointer = f"/nodes/{i}"
            if nid not in node_seen:
                node_seen[nid] = (file, pointer)
                continue
            first_file, first_pointer = node_seen[nid]
            if first_file == file:
                continue
            issues.append(Issue(
                level="error", code="NODE_ID_DUPLICATE", file=file, node=nid, pointer=pointer,
                message=f"节点 ID 跨文件重复：{nid}（{first_file} {first_pointer}；{file} {pointer}）",
                actual=f"{first_file} / {file}", expected="全局唯一：同一 id 只能在一个图包中定义",
                detail="单文件内重复由 check 判定；这里只报告跨图包重复。",
            ))
        for i, edge in enumerate(graph.get("edges") or []):
            eid = edge.get("id")
            if not eid:
                continue
            if edge.get("type") in CATALOG_EDGE_TYPES \
                    and edge.get("from") in catalog_ids and edge.get("to") in catalog_ids:
                continue
            pointer = f"/edges/{i}"
            if eid not in edge_seen:
                edge_seen[eid] = (file, pointer)
                continue
            first_file, first_pointer = edge_seen[eid]
            if first_file == file:
                continue
            issues.append(Issue(
                level="error", code="EDGE_ID_DUPLICATE", file=file, edge=eid, pointer=pointer,
                message=f"边 ID 跨文件重复：{eid}（{first_file} {first_pointer}；{file} {pointer}）",
                actual=f"{first_file} / {file}", expected="全局唯一：同一 id 只能在一个图包中定义",
                detail="单文件内重复由 check 判定；这里只报告跨图包重复。",
            ))
    return issues


def _attr_expected(constraint: dict[str, Any]) -> str:
    parts = []
    if "enum" in constraint:
        parts.append(" / ".join(constraint["enum"]))
    if constraint.get("type") == "number":
        parts.append("number 0–1" if constraint.get("minimum") == 0
                     and constraint.get("maximum") == 1 else "number")
    return "；".join(parts) or "必填"


def load_graph(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if isinstance(data, dict) and isinstance(data.get("nodes"), list) \
            and isinstance(data.get("edges"), list):
        return data
    return None
