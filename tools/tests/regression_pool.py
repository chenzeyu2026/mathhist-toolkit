"""Wrong-answer pool (错题池): one case per problem already found.

The pool exists so that a later change to the checks cannot silently bring an
old problem back, and cannot quietly start rejecting text that is correct.

Two kinds of case:

``kind="auto"``
    The expected behaviour is settled by the spec. A change here is a
    regression, or a spec change that must be made deliberately.

``kind="locked"``
    The current behaviour is a known deviation, a heuristic gap or an
    implementation quirk. The test pins today's behaviour so that changing it
    is a decision, not an accident. **A locked case is not a claim that the
    behaviour satisfies the spec.** Each one says what the spec asks for and
    what the tool actually does.

Problems that need a human reading cannot be asserted at all. They are listed
in ``SEMANTIC_ONLY`` and are deliberately not turned into tests.

Run via ``tools/scripts/selfcheck.py`` (it runs ``unittest discover``) or:

    cd tools && py -3.11 -m unittest discover -s tests -p "test_regression_pool.py" -v
"""

from __future__ import annotations

CASES = [
    {
        "id": "RP-01",
        "title": "出处只写「待补」占位",
        "rule": "R3 / §1（出处不得为空，且须可定位）",
        "kind": "auto",
        "text": "此说见于原刊。〔A｜原始文献:待补〕",
        "expect": [("LOCATOR_PLACEHOLDER", "warn")],
        "tags": 1,
        "note": "占位不是出处。这条锁住「写了占位仍然要提醒」的行为。",
    },
    {
        "id": "RP-02",
        "title": "〔U〕只写「待补」",
        "rule": "R8（U 必须写原因，空话不算）",
        "kind": "auto",
        "text": "未见原页。〔U｜未核实:待补〕",
        "expect": [("LOCATOR_PLACEHOLDER", "warn"), ("U_NO_REASON", "error")],
        "tags": 1,
        "note": "同一条出处同时触发两条检查：占位（warn）与空原因（error）。两条都要在，不能只留一条。",
    },
    {
        "id": "RP-03",
        "title": "教材被标 S",
        "rule": "R7（教材属 F）/ 词表 WEAK_POPULAR",
        "kind": "locked",
        "text": "这一说法通行。〔S｜二手研究:某高数教材, p. 233〕",
        "expect": [("GRADE_SOURCE_WEAK", "warn")],
        "tags": 1,
        "note": (
            "规范 R7 的「工具」一段写的是「命中教材词表却标 A 或 S → error」；"
            "实现把「教材」放在 WEAK_POPULAR，只报 warn。这是已确认的规范—实现不一致，"
            "按约定未改判定逻辑，只在此锁住当前行为。"
        ),
    },
    {
        "id": "RP-04",
        "title": "讲座被标 S",
        "rule": "R7 / 词表 WEAK_POPULAR",
        "kind": "locked",
        "text": "这一说法通行。〔S｜二手研究:某公开讲座, 2020〕",
        "expect": [("GRADE_SOURCE_WEAK", "warn")],
        "tags": 1,
        "note": "与 RP-03 同一处偏差：「讲座」也在 WEAK_POPULAR，只报 warn。",
    },
    {
        "id": "RP-05",
        "title": "译本单独标 A",
        "rule": "R2（单独引译本 → S）",
        "kind": "auto",
        "text": "牛顿写过这句话。〔A｜原始文献:牛顿《原理》中译本, p. 41〕",
        "expect": [("GRADE_TRANSLATION", "warn")],
        "tags": 1,
        "note": "出处含「译」、标 A、且没有第二个原文定位 → warn。",
    },
    {
        "id": "RP-06",
        "title": "R2 的正例被工具报 warn",
        "rule": "R2 正例 / GRADE_TRANSLATION",
        "kind": "locked",
        "text": "牛顿原文如此。〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II（Motte 1729 英译本, p. 41）〕",
        "expect": [("GRADE_TRANSLATION", "warn")],
        "tags": 1,
        "note": (
            "`spec/evidence-tags.md` R2 的正例就是这一条，规范认为它合规；"
            "但实现只看出处里有没有字面「原文」，没有就报 warn。"
            "这是规范正例与实现的直接冲突，锁在这里，不允许悄悄变成 error，"
            "也不允许在不改规范的情况下被当成误报删掉。"
        ),
    },
    {
        "id": "RP-07",
        "title": "点校本：正文 A 与校记 S 并存（层次写清）",
        "rule": "R2 + §4.2（同一著作不同部分可分级不同）",
        "kind": "auto",
        "text": (
            "《九章算术》本文此句作「置一而十之」。"
            "〔A｜原始文献:《九章算术》, 郭书春点校本, 1990, 卷一, p. 12〕\n\n"
            "点校者于此出校记。〔S｜二手研究:《九章算术》, 郭书春点校本, 校记, p. 12〕"
        ),
        "expect": [],
        "tags": 2,
        "note": "两处出处写出了不同层次（卷一 / 校记），引用键不同，不应有任何告警。",
    },
    {
        "id": "RP-08",
        "title": "点校本：两处引用键归一化后相同",
        "rule": "§4.2 / MULTI_GRADE",
        "kind": "locked",
        "text": (
            "《九章算术》本文。〔A｜原始文献:《九章算术》, 郭书春点校本, 1990, 卷一, p. 12〕\n\n"
            "点校者校记。〔S｜二手研究:《九章算术》, 郭书春点校本, 1990, 校记, p. 12〕"
        ),
        "expect": [("MULTI_GRADE", "warn")],
        "tags": 2,
        "note": (
            "§4.2 要求把差异写进出处，让工具能分开；但引用键只取前三个逗号段，"
            "「卷一」「校记」在第四段，被截掉，于是仍被告警。"
            "告警文案已写「请人工确认」，所以这是可接受的启发式误报，锁住而非修改。"
        ),
    },
    {
        "id": "RP-09",
        "title": "嵌套标记不得误伤外层",
        "rule": "§1.3（按括号深度配对）",
        "kind": "auto",
        "text": "转引一条。〔S｜二手研究:Boyer 1949, p. 212（其注引〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II〕）〕",
        "expect": [],
        "tags": 1,
        "note": "顶层只有 1 个标记，内层 1 个；外层不得报 TAG_UNCLOSED，内层不得报 TAG_STRAY_CLOSE。",
    },
    {
        "id": "RP-10",
        "title": "嵌套内层等级非法",
        "rule": "§1 / §1.3",
        "kind": "locked",
        "text": "转引。〔S｜二手研究:Boyer 1949, p. 212（其注引〔X｜原始文献:Newton, Principia, 1687〕）〕",
        "expect": [("TAG_UNKNOWN_GRADE", "error")],
        "tags": 1,
        "note": (
            "内层错误必须报，且只报一次；但报出的行号/列号是相对 locator 子串算的，不是相对整篇文档，"
            "所以本用例只断言代码与级别，不断言位置。"
        ),
    },
    {
        "id": "RP-11",
        "title": "标记跨行",
        "rule": "R13 / `_find_close`（标记须同行闭合）",
        "kind": "locked",
        "text": "跨行标记。〔A｜原始文献:Leibniz, Acta Eruditorum, 1684,\np. 467〕",
        "expect": [("TAG_UNCLOSED", "error"), ("TAG_STRAY_CLOSE", "error")],
        "tags": 0,
        "note": (
            "实现遇到换行即放弃配对，于是同一个跨行标记报两条错，且文案说「缺少〕」——"
            "其实 〕 在下一行。规范 R13 只规定挂载位置，没有明文要求单行，属实现比规范更严。"
            "锁住现状；若将来改成支持跨行，须同步改本用例与规范文字。"
        ),
    },
    {
        "id": "RP-12",
        "title": "半角竖线被静默接受",
        "rule": "§1（分隔符必须是全角 ｜ U+FF5C）",
        "kind": "locked",
        "text": "半角竖线。〔A|原始文献:Leibniz 1684, p. 467〕",
        "expect": [],
        "tags": 1,
        "note": (
            "`parser.BARS` 同时接受 `｜` 与 `|`，没有任何检查项针对半角竖线（TAG_HALFWIDTH 只管半角方括号）。"
            "规范要求全角，实现不报——已确认的偏差。若将来新增 TAG_HALF_BAR，本用例会失败，"
            "那时应把本用例改成 expect 新代码，并同步改规范或实现说明。"
        ),
    },
    {
        "id": "RP-13",
        "title": "只有年份、没有页码却标 A",
        "rule": "R1(c) / R3（A 要求版次—页码成对）",
        "kind": "locked",
        "text": "只有年份。〔A｜原始文献:Leibniz 1684〕",
        "expect": [],
        "tags": 1,
        "note": (
            "`LOCATOR_NO_LOCATION` 只看出处里有没有数字；「1684」是数字，于是通过。"
            "「年份算不算足够定位」是史学判断，工具做不到——锁住当前不报的行为，"
            "同时把它登记在文档的「无法自动断言」一节。"
        ),
    },
    {
        "id": "RP-14",
        "title": "〔U〕缺「下一步去哪查」",
        "rule": "R8（U 必须写原因和下一步）",
        "kind": "auto",
        "text": "未见原页。〔U｜未核实:仅见书目著录，未见 1684 年原刊影像〕",
        "expect": [("U_NO_NEXT_STEP", "warn")],
        "tags": 1,
        "note": "原因成立（不是空话）只报缺下一步；不得升级为 U_NO_REASON。",
    },
    {
        "id": "RP-15",
        "title": "旧式简写【原】",
        "rule": "§1 / LEGACY_MARKERS",
        "kind": "auto",
        "text": "旧稿写法【原】仍在。",
        "expect": [("LEGACY_MARKER", "error")],
        "tags": 0,
        "note": "没有出处的旧式简写必须报 error，防止「看起来标了」的假标记回流。",
    },
    {
        "id": "RP-16",
        "title": "作者自序标 A（R4 例外）",
        "rule": "R4 例外",
        "kind": "auto",
        "text": "欧拉在自序里这样写。〔A｜原始文献:Euler E212, 作者自序, p. iii〕",
        "expect": [],
        "tags": 1,
        "note": "护住 R4 的例外，防止将来扩大 EDITORIAL 词表时把「作者自序」一起判掉。",
    },
    {
        "id": "RP-17",
        "title": "编者导言标 A",
        "rule": "R4",
        "kind": "auto",
        "text": "全集编者这样解释。〔A｜原始文献:Opera omnia, Ser. 1, Vol. X, 编者导言, p. vii〕",
        "expect": [("GRADE_EDITORIAL", "error")],
        "tags": 1,
        "note": "与 RP-16 成对：同一卷里正文可 A、导言必须 S。",
    },
]

#: Problems that cannot be asserted automatically. Each entry says why, and
#: what a human has to look at. These are *not* run as tests on purpose.
SEMANTIC_ONLY = [
    {
        "id": "SP-01",
        "title": "「来源不明」标 U（2026-11-16 已裁决）",
        "where": "docs/method.md:26 / docs/method.en.md:26 vs spec R8(c)",
        "why": (
            "原登记为语义冲突：method 的三步判断法写「不知道谁写的 → F 的候选」，规范 R8(c) 把"
            "「来源不明的转述」归入 U。现统一按 U 裁决二者：读过那份流行文本、能指出它是哪一类"
            "才归 F；连「可能是哪一类」都指不出就是 U。method 与 R8(c) 的文字均已对齐。"
            "工具仍看不出作者是「不知道」还是「知道但没写」，所以不设可执行用例。"
        ),
    },
    {
        "id": "SP-02",
        "title": "只有年份是否构成足够定位",
        "where": "spec R1(c) / R3 vs RP-13",
        "why": (
            "「Leibniz 1684」有没有定位到具体载体，取决于所引文献的实际情况（是否只有一卷、"
            "是否另有页码体系），工具只能看有没有数字。RP-13 只锁「当前不报」，不代表规范已满足。"
        ),
    },
    {
        "id": "SP-03",
        "title": "点校本的正文与点校层是否真的分属两层",
        "where": "spec R2 / §4.2 vs RP-07、RP-08",
        "why": (
            "工具按引用键前缀比对，分不清「同一页的正文」与「同一页的校记」；"
            "是否真的分属两层，要人看原书。RP-08 只锁「会告警、须人工确认」。"
        ),
    },
    {
        "id": "SP-04",
        "title": "`corpus/` 前缀的解析",
        "where": "docs/evidence-corpus-design.md §3 / §4",
        "why": "v0.2 未实现，v0.1 没有任何 corpus 相关代码，无法构造用例。",
    },
    {
        "id": "SP-05",
        "title": "标了 F 是否同时给出了它指向的 A 或 S",
        "where": "spec R7（F 只能作线索）",
        "why": (
            "工具能查标记语法与等级自洽，看不出正文有没有给出线索，"
            "也看不出那条线索是否真的支持该句。"
        ),
    },
]
