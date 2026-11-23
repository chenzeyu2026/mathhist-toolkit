# -*- coding: utf-8 -*-
"""定义域—值域式校验原型：31 类边只写一张签名表，其余靠 6 条结构不变量。

对比对象：spec/object-model.md §5.6 的 31 行"允许 from / 允许 to / 明确禁止"表。
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ANY = "*"
CONTENT = {"concept", "theorem", "problem", "theory", "text"}
OBJECT = {"concept", "theorem", "problem", "theory", "notation", "branch", "event"}

# (from 集合, to 集合, 同型?, 对称?, 额外要求)
SIG = {
    "parent_of":       ({"branch"}, {"branch"}, 0, 0, {"kind": {"taxonomic", "historical", "institutional"}, "weight": True}),
    "cross_class":     ({"branch"}, {"branch"}, 0, 0, {"kind": {"overlaps", "prerequisite", "method_source", "shared_object"}}),
    "prerequisite_of": ({"branch"}, {"branch"}, 0, 0, {}),
    "concerns":        ({"branch"}, CONTENT, 0, 0, {}),
    "generalizes":     ({"concept", "theorem"}, {"concept", "theorem"}, 1, 0, {}),
    "depends_on":      ({"theorem", "method", "problem", "concept", "theory"}, {"theorem", "concept", "notation"}, 0, 0, {}),
    "resolves":        ({"theorem", "method"}, {"problem"}, 0, 0, {}),
    "reformulates":    ({"problem"}, {"problem"}, 0, 0, {}),
    "spawned":         ({"problem"}, {"problem"}, 0, 0, {}),
    "poses":           ({"person", "text", "event"}, {"problem"}, 0, 0, {}),
    "asserted_by":     ({"theorem", "concept", "theory", "problem", "failure"}, {"statement"}, 0, 0, {}),
    "about":           ({"statement"}, OBJECT, 0, 0, {}),
    "claimed_in":      ({"statement"}, {"text", "witness", "event"}, 0, 0, {}),
    "contradicts":     ({"statement"}, {"statement"}, 1, 1, {}),
    "competes_with":   ({"notation", "statement"}, {"notation", "statement"}, 1, 1, {}),
    "denotes":         ({"notation"}, {"concept"}, 0, 0, {"time": True}),
    "supersedes":      ({"notation", "theory"}, {"notation", "theory"}, 1, 0, {}),
    "uses_notation":   ({"concept", "theorem", "method", "theory"}, {"notation"}, 0, 0, {}),
    "uses_method":     ({"theorem", "problem", "failure", "theory"}, {"method"}, 0, 0, {}),
    "targets":         ({"failure"}, {"theorem", "theory", "concept", "method", "problem"}, 0, 0, {}),
    "corrected_by":    ({"failure"}, {"person"}, 0, 0, {}),
    "contributed_to":  ({"person"}, {"text", "witness"}, 0, 0, {"role": {"author", "editor", "translator", "commentator", "compiler"}}),
    "proved":          ({"person"}, {"theorem"}, 0, 0, {}),
    "introduced":      ({"person"}, {"concept", "notation", "method"}, 0, 0, {}),
    "participates_in": ({"person"}, {"event"}, 0, 0, {}),
    "part_of":         ({"event"}, {"problem", "theorem", "theory", "failure"}, 0, 0, {}),
    "witness_of":      ({"witness"}, {"text"}, 0, 0, {}),
    "derived_from":    ({"witness"}, {"witness"}, 0, 0, {}),
    "supports":        ({"witness", "text"}, ANY, 0, 0, {}),
    "anchors":         ({"teaching_point"}, {"concept", "theorem", "problem", "notation"}, 0, 0, {}),
    "exemplifies":     ({"concept", "theorem"}, {"theory"}, 0, 0, {}),
}
ACYCLIC = {"parent_of", "derived_from", "depends_on", "part_of", "reformulates", "spawned", "supersedes"}
EXCLUSIVE = {frozenset({"parent_of", "cross_class"})}


def fmt(s):
    return "{" + ",".join(sorted(s)) + "}" if s != ANY else "任意对象"


def check(g):
    t = {n["id"]: n["type"] for n in g["nodes"]}
    errs, seen = [], defaultdict(list)
    for e in g["edges"]:
        typ, f, to = e["type"], e["from"], e["to"]
        if typ not in SIG:
            errs.append(f"{e['id']}: 未登记的边类型 {typ}")
            continue
        F, T, homo, sym, extra = SIG[typ]
        ft, tt = t.get(f), t.get(to)
        if ft is None or tt is None:
            errs.append(f"{e['id']}: 端点不在图内 ({f}, {to})")
            continue
        if ft not in F:
            errs.append(f"{e['id']}: {typ} 的 from 定义域是 {fmt(F)}，实得 {ft}（{f}）")
        if T != ANY and tt not in T:
            errs.append(f"{e['id']}: {typ} 的 to 值域是 {fmt(T)}，实得 {tt}（{to}）")
        if homo and ft != tt:
            errs.append(f"{e['id']}: {typ} 要求同型，实得 {ft}→{tt}")
        if f == to:
            errs.append(f"{e['id']}: {typ} 不允许自环")
        if sym and e["directed"]:
            errs.append(f"{e['id']}: 对称边 {typ} 必须 directed:false")
        if sym and f > to:
            errs.append(f"{e['id']}: 对称边只存一条，from 应为字典序较小者，实得 {f} > {to}")
        for k, v in extra.items():
            if k == "weight" and e.get("weight") is None:
                errs.append(f"{e['id']}: {typ} 必须带 weight")
            elif k == "time" and (e.get("time") or {}).get("precision") != "unknown" \
                    and (e["time"].get("from") is None and e["time"].get("to") is None):
                errs.append(f"{e['id']}: {typ} 的时间至少一端非 null")
            elif isinstance(v, set) and e.get(k) not in v:
                errs.append(f"{e['id']}: {typ}.{k} ∈ {sorted(v)}，实得 {e.get(k)!r}")
        seen[(f, to)].append(typ)
        if e["attestation"] == "textbook_simplification" and e["grade"] not in {"F", "U"}:
            errs.append(f"{e['id']}: attestation=textbook_simplification 时 grade 至多 F/U，实得 {e['grade']}")
        if e["attestation"] == "later_report" and e["grade"] == "A":
            errs.append(f"{e['id']}: later_report 的 grade 不得为 A")
        if e["grade"] == "U" and not e.get("note"):
            errs.append(f"{e['id']}: grade=U 必须写 note")
        if not e.get("source") and not e.get("claimant"):
            errs.append(f"{e['id']}: 边必须有 source 或 claimant")
    for (f, to), types in seen.items():
        for pair in EXCLUSIVE:
            if pair <= set(types):
                errs.append(f"{f}→{to}: 同一对端点同时出现 {'/'.join(sorted(pair))}，只能二选一")
    # 无环：只在指定关系组成的子图上判
    for rel in ACYCLIC:
        adj = defaultdict(set)
        for e in g["edges"]:
            if e["type"] == rel:
                adj[e["from"]].add(e["to"])
        color, cycles = {}, []
        def dfs(u, path):
            color[u] = 1
            for v in adj.get(u, ()):
                if color.get(v) == 1:
                    cycles.append(path[path.index(v):] + [v] if v in path else [u, v])
                elif color.get(v, 0) == 0:
                    dfs(v, path + [v])
            color[u] = 2
        for u in list(adj):
            if color.get(u, 0) == 0:
                dfs(u, [u])
        for c in cycles[:3]:
            errs.append(f"{rel} 成环: " + " → ".join(c))
    # 权重归一：每个子节点的 parent_of 入边权重和为 1（根节点除外）
    wsum = defaultdict(float)
    for e in g["edges"]:
        if e["type"] == "parent_of" and e.get("weight") is not None:
            wsum[e["to"]] += e["weight"]
    kids = {e["to"] for e in g["edges"] if e["type"] == "parent_of"}
    for k in kids:
        if abs(wsum[k] - 1.0) > 0.01:
            errs.append(f"{k}: parent_of 入边权重和 {wsum[k]:.2f} ≠ 1.00")
    # 孤立节点
    touched = {e["from"] for e in g["edges"]} | {e["to"] for e in g["edges"]}
    for n in g["nodes"]:
        if n["id"] not in touched and n.get("type") != "branch" and n.get("status") != "proposed":
            errs.append(f"{n['id']}: 非 proposed 节点没有任何边")
    return errs


if __name__ == "__main__":
    root = Path(r"<repo>\spec\framework")
    files = [root / "pilots" / "group-theory" / "graph.json",
             root / "pilots" / "calculus" / "graph.json",
             root / "samples" / "non-euclidean-geometry.json"]
    for p in files:
        errs = check(json.loads(p.read_text(encoding="utf-8")))
        print(f"{p.parent.name}/{p.name}: {len(errs)} 处")
        for e in errs[:6]:
            print("   ", e)

