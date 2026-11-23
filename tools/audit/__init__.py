"""规则集一致性审计（零依赖，Python 3.11）。

三个模块：

- ``grading_kernel``：把 R1–R13 中可判定的部分编码成全函数，枚举
  witness × 定位 × 转引 组合，求各规则允许等级集合的交集。
- ``audit_domain``：对同一有限域做约束剔除、宽/窄两套去重，并在去重空间上重算。
- ``criticality``：逐条删除规则，统计判定改变的情境数。

入口：``python -m tools.audit``（仓库根）或 ``python -m audit``（cwd 为 ``tools/``）。
输出是纯文本报表，不写文件、不联网。数字口径见 ``spec/evidence-tags.md`` §5.1。
"""
