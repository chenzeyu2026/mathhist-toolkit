# -*- coding: utf-8 -*-
"""逐规则关键度：删掉该条后，判定结果改变的行数。

口径：
- 空间 = 过 C1/P1/P2 后、按同一去重规则压缩的情境集
- 「判定改变」= 状态改变（unique/under/conflict 互换），
  或同为 unique 但唯一等级不同
- 宽口径去重：轴只要有指称就算活
- 窄口径去重：只有规则真正读取的轴才算活
"""
from collections import Counter

from .grading_kernel import W, L, G, ALL, RULES_V0, RULES_V1, W_V1
from .audit_domain import raw, dedup, judge, CONSTRAINTS


def pivotal(rules, dom, rid):
    n = 0
    reduced = [(r, f) for r, f in rules if r != rid]
    for c in dom:
        b_st, _, b_allowed = judge(rules, c)
        a_st, _, a_allowed = judge(reduced, c)
        if a_st != b_st or (b_st == "unique" and a_allowed != b_allowed):
            n += 1
    return n


def report(name, rules, ws, wide, tag):
    kept = [c for c in raw(ws) if all(p(c) for _, p, _ in CONSTRAINTS)]
    dom = dedup(kept, wide)
    st = Counter(judge(rules, c)[0] for c in dom)
    print(f"\n### {name} | {tag} | 空间 {len(dom)} "
          f"(unique {st['unique']} / under {st['under']} / conflict {st['conflict']})")
    print(f"{'规则':10s} {'关键度':>6s} {'返回ALL':>7s} {'非ALL':>6s}")
    for rid, f in rules:
        p = pivotal(rules, dom, rid)
        vac = sum(1 for c in dom if f(c) == ALL)
        print(f"{rid:10s} {p:6d} {vac:7d} {len(dom)-vac:6d}")


def main():
    w_all = list(W)
    w_v1 = list(W_V1)
    print("=" * 66)
    print("现状 v0（规范 v0.1 逐条编码）")
    print("=" * 66)
    for wide, tag in ((True, "宽口径"), (False, "窄口径")):
        report("v0", RULES_V0, w_all, wide, tag)
    print()
    print("=" * 66)
    print("修订 v1（S-1..S-6）")
    print("=" * 66)
    for wide, tag in ((True, "宽口径"), (False, "窄口径")):
        report("v1", RULES_V1, w_v1, wide, tag)


if __name__ == "__main__":
    main()
