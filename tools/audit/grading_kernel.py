# -*- coding: utf-8 -*-
"""证据分级判定核：有限域穷举一致性检查（零依赖，Python 3.11）。

用途：把 R1-R13 中"可判定"的部分压成一张全函数表，
      枚举所有 witness × 定位 × 转引 组合，
      检查每个组合是否恰好得到一个等级。
      交集为空 = 两条规则互相否定；交集多值 = 规则不足以判定。
"""

from enum import Enum
from itertools import product


class G(Enum):
    A = "A"; S = "S"; U = "U"; F = "F"


class W(Enum):
    ORIGINAL = "原文/原刊"
    FACSIMILE = "同版式影印"
    RESET = "重排重印"
    TRANSLATION = "译本"
    CRIT_EDITION = "点校本(未分层)"      # 仅 v0：R2/R3 对同一对象给出相反判定
    CRIT_BODY = "点校本正文"
    CRIT_APP = "点校者校记"
    TRANSCRIPT = "现代校勘转录"
    STUDENT_OK = "经作者校订的笔记"
    STUDENT = "未授权学生笔记"
    MEMOIR = "作者晚年回忆"
    ANNOT_NAMED = "实名后人批注"
    ANNOT_ANON = "佚名批注"
    SECONDARY = "二手研究转述"
    POPULAR = "流行说法(教材/百科/科普)"


class L(Enum):
    COMPLETE = "版次+页码齐全"
    PARTIAL = "有版次无页码"
    PLACEHOLDER = "待补/无出处"


class Cfg:
    __slots__ = ("w", "loc", "d", "orig_page", "named", "blocked")

    def __init__(self, w, loc, d, orig_page, named, blocked):
        self.w, self.loc, self.d = w, loc, d
        self.orig_page, self.named, self.blocked = orig_page, named, blocked

    def __repr__(self):
        return (f"{self.w.value} | {self.loc.value} | 深度{self.d} "
                f"| 原文页码{'有' if self.orig_page else '无'} "
                f"| 中转者{'具名' if self.named else '佚名'} | {self.blocked}")


ALL = set(G)
DIRECT = {W.ORIGINAL, W.FACSIMILE, W.RESET, W.TRANSLATION, W.CRIT_EDITION,
          W.CRIT_BODY, W.CRIT_APP, W.TRANSCRIPT, W.STUDENT_OK, W.STUDENT,
          W.MEMOIR, W.ANNOT_NAMED, W.ANNOT_ANON, W.POPULAR}


def valid(c):
    # 深度只对"二手转述"有意义；直接持有的载体必须深度 0
    return c.w is W.SECONDARY or c.d == 0


def u_reason(c):
    if c.loc is L.PLACEHOLDER:
        return "NO_CARRIER"          # 有断言、无任何可核载体
    if c.w is W.ANNOT_ANON:
        return "ORAL"                # 来源不明的转述
    if c.w is W.SECONDARY and c.d >= 2:
        return "NO_CARRIER" if c.named else "ORAL"
    if c.blocked == "CLUE":
        return "CLUE"                # 有线索未取原件
    if c.blocked == "DAMAGED":
        return "DAMAGED"             # 原件缺页/污损
    return None


# ---------------- v0：规范现有条款，逐条编码 ----------------

def r1_v0(c):
    # R1：作者本人著作/手稿/同时代原刊/自序自注 -> A（无定位则不得 A）
    if c.w in {W.ORIGINAL, W.MEMOIR, W.STUDENT_OK, W.CRIT_BODY}:
        return {G.A} if c.loc is not L.PLACEHOLDER else {G.U, G.F}
    # R9 第 2 款：后人批注可考且属同时代重要人物 -> A
    if c.w is W.ANNOT_NAMED:
        return {G.A} if c.loc is not L.PLACEHOLDER else {G.U, G.F}
    return ALL


def r2_v0(c):
    # R2：译本 + 原文版次与页码双定位 -> A；否则 S
    if c.w is W.TRANSLATION:
        if c.orig_page and c.loc is L.COMPLETE:
            return {G.A}
        return {G.S}
    # R2：点校本"点校属编纂" -> S（整本当 S；点校者校记同此）
    if c.w in {W.CRIT_EDITION, W.CRIT_APP}:
        return {G.S}
    if c.w in {W.RESET, W.TRANSCRIPT}:
        return {G.S}
    return ALL


def r3_v0(c):
    # R3：全集/点校本的作者正文 -> A
    if c.w in {W.ORIGINAL, W.FACSIMILE, W.CRIT_BODY, W.CRIT_EDITION}:
        return {G.A} if c.loc is not L.PLACEHOLDER else {G.U, G.F}
    return ALL


def r5_v0(c):
    # R5：只见二手引用 -> S；转引超过一层 -> U；未见原页的译本/重排 -> S
    s = set(ALL)  # 必须复制，否则 &= 会就地改写全局 ALL
    if c.w in {W.TRANSLATION, W.RESET, W.TRANSCRIPT, W.CRIT_EDITION}:
        s &= {G.S}
    if c.w is W.SECONDARY:
        s &= {G.S} if c.d <= 1 else {G.U}
    return s


ALLOWED_U_V0 = {"CLUE", "DAMAGED", "ORAL"}


def r8_v0(c):
    # R8：U 只允许三种情形
    return ALL if u_reason(c) in ALLOWED_U_V0 else (ALL - {G.U})


def r_f_v0(c):
    # R7：流行说法只能是 F；但连流行文本都指不出（占位）时交给 S-6 判 U
    if c.w is W.POPULAR:
        return {G.F} if c.loc is not L.PLACEHOLDER else {G.F, G.U}
    return ALL - {G.F}


RULES_V0 = [("R1/R9", r1_v0), ("R2", r2_v0), ("R3", r3_v0),
            ("R5", r5_v0), ("R8", r8_v0), ("R7", r_f_v0)]


# ---------------- v1：按 S-1/S-2/S-3/S-4/S-5/S-6 修订 ----------------

def r1_v1(c):
    # S-1：等级描述"实际使用的载体"，不再按文本作者判 A
    if c.w in {W.ORIGINAL, W.FACSIMILE, W.MEMOIR, W.STUDENT_OK, W.CRIT_BODY}:
        return {G.A} if c.loc is not L.PLACEHOLDER else {G.U}
    # S-3：实名后人批注最高 S；佚名 U
    if c.w in {W.STUDENT, W.ANNOT_NAMED}:
        return {G.S} if c.loc is not L.PLACEHOLDER else {G.U}
    if c.w is W.ANNOT_ANON:
        return {G.U}
    return ALL


def r2_v1(c):
    # S-2：译本一律 S，双定位只是必填项，不升级
    if c.w in {W.TRANSLATION, W.RESET, W.TRANSCRIPT, W.CRIT_APP}:
        return {G.S} if c.loc is not L.PLACEHOLDER else {G.U}
    return ALL


def r3_v1(c):
    # S-5：点校本正文 A；点校层 S（已拆成两个载体）
    if c.w in {W.ORIGINAL, W.FACSIMILE, W.CRIT_BODY}:
        return {G.A} if c.loc is not L.PLACEHOLDER else {G.U}
    return ALL


def r5_v1(c):
    s = set(ALL)
    if c.w in {W.TRANSLATION, W.RESET, W.TRANSCRIPT, W.CRIT_APP}:
        s &= {G.U} if c.loc is L.PLACEHOLDER else {G.S}
    if c.w in {W.STUDENT, W.ANNOT_NAMED}:
        s &= {G.U} if c.loc is L.PLACEHOLDER else {G.S}
    if c.w is W.ANNOT_ANON:
        s &= {G.U}
    if c.w is W.SECONDARY:
        s &= {G.U} if (c.loc is L.PLACEHOLDER or c.d >= 2) else {G.S}
    return s


ALLOWED_U_V1 = {"CLUE", "DAMAGED", "ORAL", "NO_CARRIER"}


def r8_v1(c):
    # S-4：U 的四种情形，含"有断言但无可核载体"
    return ALL if u_reason(c) in ALLOWED_U_V1 else (ALL - {G.U})


def r_loc_v1(c):
    # S-6：占位出处 -> U，不得留在 A/S
    return {G.U} if c.loc is L.PLACEHOLDER else ALL


RULES_V1 = [("R1/R9", r1_v1), ("R2", r2_v1), ("R3", r3_v1),
            ("R5", r5_v1), ("R8", r8_v1), ("R6/S-6", r_loc_v1), ("R7", r_f_v0)]


def analyze(rules, label, witnesses=None):
    ws = witnesses if witnesses is not None else list(W)
    domain = [Cfg(w, l, d, op, nm, bl)
              for w, l, d, op, nm, bl in product(
                  ws, L, (0, 1, 2), (True, False), (True, False),
                  ("NONE", "CLUE", "DAMAGED"))]
    total = 0
    conflicts, under = {}, {}
    for c in domain:
        if not valid(c):
            continue
        total += 1
        allowed, detail = set(G), []
        for rid, f in rules:
            s = f(c)
            if s != ALL:
                detail.append((rid, "".join(sorted(g.value for g in s))))
            allowed &= s
        if not allowed:
            conflicts.setdefault((c.w.name, tuple(detail)), []).append(c)
        elif len(allowed) > 1:
            under.setdefault((c.w.name, tuple(detail),
                              "".join(sorted(g.value for g in allowed))), []).append(c)

    print(f"\n===== {label} =====")
    print(f"有效配置 {total}；冲突（交集为空）{sum(map(len, conflicts.values()))} 条；"
          f"不定（多值）{sum(map(len, under.values()))} 条")
    print(f"冲突类别 {len(conflicts)}；不定类别 {len(under)}")
    for key, cs in sorted(conflicts.items(), key=lambda kv: -len(kv[1])):
        name, detail = key
        print(f"\n  [{name}] x{len(cs)}  例：{cs[0]}")
        for rid, gs in detail:
            print(f"      {rid:8s} 允许 {{{gs}}}")
        print("      => 无任何等级同时满足以上规则")
    for key, cs in sorted(under.items(), key=lambda kv: -len(kv[1])):
        name, detail, left = key
        print(f"\n  [不定:{name}] x{len(cs)} 剩余 {{{left}}} 例：{cs[0]}")
    return total, sum(map(len, conflicts.values())), sum(map(len, under.values()))


W_V1 = [w for w in W if w is not W.CRIT_EDITION]


def main():
    analyze(RULES_V0, "v0 现状条款逐条编码")
    analyze(RULES_V1, "v1 修订后（S-1/2/3/4/5/6）", witnesses=W_V1)


if __name__ == "__main__":
    main()
