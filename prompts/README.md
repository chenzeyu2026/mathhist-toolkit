# 指令集 P1–P9 / Prompt set P1–P9

这九条提示词取自既有写作流程的附录，中文在 `zh/`，英文在 `en/`。除等级字母外，正文未做改写。
The nine prompts are taken from an existing writing workflow appendix. Chinese in `zh/`, English in `en/`. Apart from the grade letters, the text is unedited.

| 编号 | 用途 / Purpose | 文件 |
|---|---|---|
| P1 | 一手文献精读：问题—记号—反例 / Close reading of a primary source | [`zh/P1.md`](zh/P1.md) · [`en/P1.md`](en/P1.md) |
| P2 | 证据分级标注 / Evidence grading of a paragraph | [`zh/P2.md`](zh/P2.md) · [`en/P2.md`](en/P2.md) |
| P3 | 「未能核实」台账 / Ledger of unverified claims | [`zh/P3.md`](zh/P3.md) · [`en/P3.md`](en/P3.md) |
| P4 | 反向验证：解决的是当年问题吗 / Reverse test | [`zh/P4.md`](zh/P4.md) · [`en/P4.md`](en/P4.md) |
| P5 | 反辉格史自检 / Whig-history self-check | [`zh/P5.md`](zh/P5.md) · [`en/P5.md`](en/P5.md) |
| P6 | 双语术语对齐 / Cross-linguistic alignment | [`zh/P6.md`](zh/P6.md) · [`en/P6.md`](en/P6.md) |
| P7 | 「误说—纠正」对写 / Misstatement and correction | [`zh/P7.md`](zh/P7.md) · [`en/P7.md`](en/P7.md) |
| P8 | 一手文献互证 / Cross-checking two sources | [`zh/P8.md`](zh/P8.md) · [`en/P8.md`](en/P8.md) |
| P9 | 章节收尾：结论压回证据 / Compress conclusions back to evidence | [`zh/P9.md`](zh/P9.md) · [`en/P9.md`](en/P9.md) |

## 等级字母 / Grade letters

九条提示词与规范、工具使用同一套四级：**A / S / U / F**。语法见
[`spec/evidence-tags.md`](../spec/evidence-tags.md)（英文：[`spec/evidence-tags.en.md`](../spec/evidence-tags.en.md)）。

All nine prompts now use the same four levels as the spec and the linter: **A / S / U / F**.
Syntax: [`spec/evidence-tags.md`](../spec/evidence-tags.md) / [`spec/evidence-tags.en.md`](../spec/evidence-tags.en.md).

- `A` 原始文献 primary source
- `S` 二手研究 secondary（转引时在出处置写中转者 / name the intermediary in the locator）
- `U` 未核实 unverified（必须写原因 / must give a reason）
- `F` 流行说法 popular（只能作线索，不能单独支撑论断；要支撑须同时给出它指向的 A 或 S / lead only; to support a claim you must also give the `A` or `S` it points to）

## 与工具衔接 / Using with the linter

1. 用 P2 把段落拆成断言并分级 → 得到 A/S/U/F 表。
2. 把表写成 `〔A｜原始文献:…〕`、`〔S｜二手研究:…〕` 等标记，写回正文。
3. `mathlint check 章节.md` 检查语法、自洽、缺标记。`mathlint` 不看 P2 的表格，只看最终标记。
4. 用 P9 复核结论，再用 `--strict` 定稿。

1. Run P2 to split a paragraph into graded claims (A/S/U/F).
2. Write them back as `〔A｜原始文献:…〕` / `〔S｜二手研究:…〕` tags.
3. Run `mathlint check chapter.md` for syntax, consistency and missing tags.
4. Run P9 on the conclusions, then finalise with `--strict`.

## 样例 / Examples

[`examples/`](examples/) 里是从第一期正文抽出的三段真实段落，给出「改前／改后」对照；改后版本可通过 `mathlint`（0 error / 0 warn）。
`examples/` contains three real passages from Issue 01 in "before / after" form; each "after" file passes `mathlint` with 0 errors and 0 warnings.

## 变更记录 / Change log

### 2026-11，v0.1：提示词等级统一为四级

提示词原先用五字母分级，与本仓库规范不一致。现已统一，正文里不再出现旧字母：

| 旧 / old | 现 / now | 说明 / note |
|---|---|---|
| A 原始文献 | `A` 原始文献 | 不变 / unchanged |
| B 权威二手研究 | `S` 二手研究 | 只换字母 / letter only |
| C 流行转述 | `F` 流行说法 | 只换字母 / letter only |
| U 未核实 | `U` 未核实 | 不变 / unchanged |
| T 转引 | 不再是等级 / no longer a grade | 成为 S 的必填字段：出处里必须写出中转者 / now a required field on `S` |

改动范围：P2 的分级表与两条注意项、P4 与 P6 要求标注等级的括号、各文件头部说明。P5 不涉及分级字母。
Scope: the grading table and two notes in P2, the bracketed grade lists in P4 and P6, and the header note of every file. P5 uses no grade letters.

旧字母只在本节出现，用于对读旧稿与旧台账。如果你手上的旧文稿仍用旧字母，按上表逐条替换即可；`mathlint` 只认新字母。
The old letters appear only in this section, so old drafts and ledgers can still be read against the new scheme. If your draft still uses them, substitute per the table above; `mathlint` accepts only the new letters.
