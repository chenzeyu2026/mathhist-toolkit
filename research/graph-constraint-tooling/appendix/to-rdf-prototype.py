# -*- coding: utf-8 -*-
"""把 mathhist 图包 (nodes/edges JSON) 转成 RDF 三元组，供 SHACL 校验。

目的：评估 SHACL 能否表达现有 §5.6 约束。
- 每条边重化为一个节点 urn:mh:edge:<n>，并 rdf:type mh:<edge_type> 便于按类型设形状；
- 边属性 (time/grade/source/confidence) 变成该节点的属性；
- 为无环检查物化前面化谓词 mh:depNext / mh:parentNext。
"""
import json
import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, XSD

MH = Namespace("urn:mh:")


def convert(path: Path) -> Graph:
    data = json.loads(path.read_text(encoding="utf-8"))
    g = Graph()
    g.bind("mh", MH)
    objs = {}
    for n in data["nodes"]:
        o = MH["node:" + n["id"]]
        objs[n["id"]] = o
        g.add((o, RDF.type, MH.Node))
        g.add((o, RDF.type, MH["T_" + n["type"]]))
        g.add((o, MH.nodeType, Literal(n["type"])))
        g.add((o, MH.key, Literal(n["id"])))
        g.add((o, MH.status, Literal(n.get("status") or "")))
    for i, e in enumerate(data["edges"]):
        o = MH["edge:" + str(i)]
        g.add((o, RDF.type, MH.Edge))
        g.add((o, RDF.type, MH[e["type"]]))
        g.add((o, MH.key, Literal(e["id"])))
        g.add((o, MH.edgeType, Literal(e["type"])))
        g.add((o, MH["from"], objs[e["from"]]))
        g.add((o, MH["to"], objs[e["to"]]))
        g.add((o, MH.directed, Literal(bool(e["directed"]))))
        g.add((o, MH.grade, Literal(e["grade"])))
        g.add((o, MH.attestation, Literal(e["attestation"])))
        g.add((o, MH.confidence, Literal(float(e["confidence"]), datatype=XSD.decimal)))
        t = e.get("time") or {}
        if t.get("from") is not None:
            g.add((o, MH.timeFrom, Literal(int(t["from"]), datatype=XSD.integer)))
        if t.get("to") is not None:
            g.add((o, MH.timeTo, Literal(int(t["to"]), datatype=XSD.integer)))
        g.add((o, MH.precision, Literal(t.get("precision") or "unknown")))
        if e.get("source"):
            g.add((o, MH.hasSource, Literal(True)))
        if e.get("claimant"):
            g.add((o, MH.hasClaimant, Literal(True)))
        if e.get("weight") is not None:
            g.add((o, MH.weight, Literal(float(e["weight"]), datatype=XSD.decimal)))
        if e.get("kind"):
            g.add((o, MH.kind, Literal(e["kind"])))
        if e.get("role"):
            g.add((o, MH.role, Literal(e["role"])))
        if e.get("note"):
            g.add((o, MH.note, Literal(e["note"])))
        if e["type"] == "depends_on":
            g.add((objs[e["from"]], MH.depNext, objs[e["to"]]))
        if e["type"] == "parent_of":
            g.add((objs[e["from"]], MH.parentNext, objs[e["to"]]))
        if e["type"] == "witness_of":
            g.add((objs[e["from"]], MH.isWitnessOf, objs[e["to"]]))
    return g


if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    g = convert(src)
    g.serialize(destination=str(dst), format="turtle")
    print(f"{src.name}: {len(g)} triples -> {dst}")

