# -*- coding: utf-8 -*-
"""审计 §1.5 这个有限域：轴独立性、真矛盾、无意义、去重后的真实有效组合数。

不改动 grading_kernel，只 import 它。
"""
import itertools
from collections import Counter, defaultdict

from .grading_kernel import (
    W, L, G, Cfg, ALL, RULES_V0, RULES_V1, W_V1, u_reason, r_f_v0,
)

AXES = ["w", "loc", "d", "orig_page", "named", "blocked"]


def raw(witnesses):
    out = []
    for w, l, d, op, nm, bl in itertools.product(
            list(witnesses), list(L), (0, 1, 2), (True, False),
            (True, False), ("NONE", "CLUE", "DAMAGED")):
        out.append(Cfg(w, l, d, op, nm, bl))
    return out


# ---------------------------------------------------------------- 约束表
CONSTRAINTS = [
    ("C1 深度轴只对「经人转述」有指称",
     lambda c: c.w is W.SECONDARY or c.d == 0,
     "直接持有载体时不存在「转引了几层」；d≠0 与载体定义冲突"),
    ("P1 已持有载体却称「有线索未取原件」",
     lambda c: not (c.blocked == "CLUE" and c.w is not W.SECONDARY),
     "CLUE 的内容就是「原件没拿到」，与「载体=原文/影印/点校本」互否；"
     "只有载体本身是二手转述时才可能"),
    ("P2 「缺页」却「版次+页码齐全」",
     lambda c: not (c.blocked == "DAMAGED" and c.loc is L.COMPLETE),
     "缺页使页码层定位在事实上不成立，与 COMPLETE 互否"),
]


def dead_axes(c, wide):
    """wide=True：只要轴有指称就算活；False：只有规则真正读取才算活。"""
    dead = set()
    if c.d == 0:
        dead.add("named")
    if c.w is W.ORIGINAL:
        dead.add("orig_page")
    elif not wide and c.w is not W.TRANSLATION:
        dead.add("orig_page")
    if c.loc is L.PLACEHOLDER:
        dead.add("blocked")
    return dead


def canon(c, wide):
    dead = dead_axes(c, wide)
    return tuple(None if a in dead else getattr(c, a) for a in AXES)


# ---------------------------------------------------------------- 判定
def judge(rules, c):
    allowed = set(G)
    detail = []
    for rid, f in rules:
        s = f(c)
        if s != ALL:
            detail.append((rid, "".join(sorted(g.value for g in s))))
        allowed &= s
    if not allowed:
        return "conflict", detail, allowed
    if len(allowed) > 1:
        return "under", detail, allowed
    return "unique", detail, allowed


def summarize(rules, domain, label):
    res = Counter()
    buckets = defaultdict(list)
    for c in domain:
        st, detail, allowed = judge(rules, c)
        res[st] += 1
        buckets[st].append((c, detail, allowed))
    print(f"  {label}: 总数 {len(domain)} | 唯一 {res['unique']} | "
          f"不定 {res['under']} | 冲突 {res['conflict']}")
    return res, buckets


def dedup(cs, wide):
    seen, out = set(), []
    for c in cs:
        k = canon(c, wide)
        if k not in seen:
            seen.add(k)
            out.append(c)
    return out


def main():
    w_all = list(W)
    w_v1 = list(W_V1)

    print("=" * 78)
    print("一、原始域")
    print("=" * 78)
    for name, ws in (("v0（15 载体）", w_all),
                     ("v1（14 载体，去掉未分层的 CRIT_EDITION）", w_v1)):
        r = raw(ws)
        kept = [c for c in r if all(p(c) for _, p, _ in CONSTRAINTS)]
        print(f"  {name}: 笛卡尔积 {len(r)} → 过 C1/P1/P2 后 {len(kept)}")

    print()
    print("  各约束剔除量（在 15 载体 × 1620 上）：")
    pool = raw(w_all)
    removed_any = set()
    for nm, pred, why in CONSTRAINTS:
        hit = [c for c in pool if not pred(c)]
        print(f"    {nm}: {len(hit)} 条")
        print(f"      理由：{why}")
        removed_any.update(id(c) for c in hit)
        pool = [c for c in pool if pred(c)]
    print(f"    三条合计剔除 {len(removed_any)} 条（互不重叠）")

    print()
    print("=" * 78)
    print("二、去重：轴落空造成的重复")
    print("=" * 78)
    for wide, tag in ((True, "宽口径：轴只要有指称就算活"),
                      (False, "窄口径：只有规则真正读取的轴才算活")):
        for name, ws in (("v0", w_all), ("v1", w_v1)):
            kept = [c for c in raw(ws) if all(p(c) for _, p, _ in CONSTRAINTS)]
            keys = {canon(c, wide) for c in kept}
            print(f"  [{tag}] {name}: {len(kept)} → 去重后 {len(keys)} 个不同情境")

    print()
    print("  重复来源明细（v1，宽口径）：")
    kept = [c for c in raw(w_v1) if all(p(c) for _, p, _ in CONSTRAINTS)]
    dead_count = Counter()
    for c in kept:
        for a in dead_axes(c, True):
            dead_count[a] += 1
    for a, n in dead_count.most_common():
        sub = [c for c in kept if a in dead_axes(c, True)]
        print(f"    {a}: {n} 条配置上该轴落空，去重后剩 {len({canon(c, True) for c in sub})} 组")
    per = Counter()
    for c in kept:
        per[c.w.name] += 1
    per_canon = Counter()
    for k in {canon(c, True) for c in kept}:
        per_canon[k[0].name] += 1
    print()
    print(f"  {'载体':22s} {'原始组合':>8s} {'去重后':>8s} {'倍数':>8s}")
    for w in w_v1:
        a, b = per[w.name], per_canon[w.name]
        print(f"  {w.name:22s} {a:8d} {b:8d} {a/b:7.1f}x")

    # ------------------------------------------------------------ 三、重算
    print()
    print("=" * 78)
    print("三、在去重后的空间上重算")
    print("=" * 78)
    for wide, tag in ((True, "宽口径"), (False, "窄口径")):
        print(f"\n[{tag}]")
        for name, rules, ws in (("现状 v0", RULES_V0, w_all),
                                ("修订 v1", RULES_V1, w_v1)):
            kept = [c for c in raw(ws) if all(p(c) for _, p, _ in CONSTRAINTS)]
            summarize(rules, kept, f"{name} 原始空间")
            summarize(rules, dedup(kept, wide), f"{name} 去重空间")

    # ------------------------------------------------------------ 四、分解
    print()
    print("=" * 78)
    print("四、138 与 72 的分解是否还成立")
    print("=" * 78)
    kept0 = [c for c in raw(w_all) if all(p(c) for _, p, _ in CONSTRAINTS)]
    for label, dom in (("v0 原始 612", kept0), ("v0 去重后", dedup(kept0, True))):
        res, buckets = summarize(RULES_V0, dom, label)
        conf = Counter()
        under = Counter()
        for c, detail, allowed in buckets["conflict"]:
            conf[(c.w.name, "+".join(r for r, _ in detail))] += 1
        for c, detail, allowed in buckets["under"]:
            under[(c.w.name, "+".join(r for r, _ in detail),
                   "".join(sorted(g.value for g in allowed)))] += 1
        print("    冲突分解：")
        for (wn, ids), n in conf.most_common():
            print(f"      {n:4d}  {wn:20s} 由 {ids} 触发")
        print("    不定分解：")
        for (wn, ids, left), n in under.most_common():
            print(f"      {n:4d}  {wn:20s} 由 {ids} 触发，剩 {{{left}}}")

    # ------------------------------------------------------------ 五、空转
    print()
    print("=" * 78)
    print("五、空转规则与「仅一条规则说话」的配置")
    print("=" * 78)
    for name, rules, ws in (("现状 v0", RULES_V0, w_all), ("修订 v1", RULES_V1, w_v1)):
        kept = [c for c in raw(ws) if all(p(c) for _, p, _ in CONSTRAINTS)]
        dom = dedup(kept, True)
        print(f"\n  [{name}] 去重空间 {len(dom)} 个情境")
        print(f"  {'规则':12s} {'返回ALL':>7s} {'唯一决定':>7s} {'参与':>5s} {'关键':>5s}")
        for rid, f in rules:
            vac = sum(1 for c in dom if f(c) == ALL)
            dec = sum(1 for c in dom if len(f(c)) == 1)
            part = sum(1 for c in dom if f(c) != ALL)
            pivotal = 0
            reduced = [(r, g) for r, g in rules if r != rid]
            for c in dom:
                b_st, _, b_allowed = judge(rules, c)
                a_st, _, a_allowed = judge(reduced, c)
                if a_st != b_st or (b_st == "unique" and a_allowed != b_allowed):
                    pivotal += 1
            print(f"  {rid:12s} {vac:7d} {dec:7d} {part:5d} {pivotal:5d}")
        dist = Counter()
        for c in dom:
            n = sum(1 for rid, f in rules if f(c) != ALL)
            dist[n] += 1
        print("    每个情境上「返回非 ALL」的条数分布：" +
              ", ".join(f"{k}条:{v}" for k, v in sorted(dist.items())))

    # ------------------------------------------------------------ 六、敏感度
    print()
    print("=" * 78)
    print("六、脆弱性测试：加入「任何 A 都必须有完整定位」(S-12) 后的 v1")
    print("=" * 78)

    def r_page(c):
        return ALL - {G.A} if c.loc is not L.COMPLETE else ALL

    rules_plus = RULES_V1 + [("S-12页码", r_page)]
    kept = [c for c in raw(w_v1) if all(p(c) for _, p, _ in CONSTRAINTS)]
    dom = dedup(kept, True)
    summarize(rules_plus, dom, "v1 + S-12")
    summarize(RULES_V1, dom, "对照：v1")

    # ------------------------------------------------------------ 七、判定签名
    print()
    print("=" * 78)
    print("七、去重空间里，多少个情境共用同一个「判定签名」")
    print("=" * 78)
    kept = [c for c in raw(w_v1) if all(p(c) for _, p, _ in CONSTRAINTS)]
    dom = dedup(kept, True)
    sig = defaultdict(list)
    for c in dom:
        st, detail, allowed = judge(RULES_V1, c)
        sig[(st, tuple(detail), "".join(sorted(g.value for g in allowed)))].append(c)
    print(f"  情境 {len(dom)} 个 → 不同判定签名 {len(sig)} 种")
    for k, cs in sorted(sig.items(), key=lambda kv: -len(kv[1])):
        st, detail, left = k
        print(f"    x{len(cs):3d} {st:8s} 剩{{{left}}} 由 {[d[0] for d in detail]} 例：{cs[0]}")


if __name__ == "__main__":
    main()
