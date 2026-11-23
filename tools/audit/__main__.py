# -*- coding: utf-8 -*-
"""命令行入口：``python -m tools.audit [kernel|domain|criticality|all]``。

四节的输出：

- ``kernel``：v0 / v1 两套规则的原始有效配置数、冲突条数、不定条数；
- ``domain``：六维笛卡尔积如何被 C1/P1/P2 剔除、宽窄两套口径去重后的情境数、
  以及在去重空间上的冲突/不定重算；
- ``criticality``：删掉每一条规则后判定改变的情境数（宽口径与窄口径各一张表）；
- ``all``（默认）：以上三节依次输出。
"""

import argparse

from . import audit_domain, criticality, grading_kernel

SECTIONS = {
    "kernel": "判定核：v0 / v1 的原始冲突与不定",
    "domain": "域审计：剔除、去重与去重空间重算",
    "criticality": "关键度：逐条删除规则后的判定改变行数",
}


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m tools.audit",
        description="规则集一致性审计（只输出文本，不写文件、不联网）",
    )
    parser.add_argument(
        "section",
        nargs="?",
        default="all",
        choices=["all", *SECTIONS],
        help="要跑的一节，默认全部",
    )
    args = parser.parse_args(argv)

    if args.section in ("all", "kernel"):
        print(f"# {SECTIONS['kernel']}")
        grading_kernel.main()
    if args.section in ("all", "domain"):
        print(f"\n# {SECTIONS['domain']}")
        audit_domain.main()
    if args.section in ("all", "criticality"):
        print(f"\n# {SECTIONS['criticality']}")
        criticality.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
