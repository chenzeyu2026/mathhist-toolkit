# `resembles` 入图闸门状态

日期：2026-11-27
状态：**schema 已落地；实例不入图**
上游设计：`d:\AI本地\mathhist-branches-expand\outputs\论证规范化_展开简化重封装_设计稿.md` §6、§8

---

## 1. 闸门当前值

| 条件 | 要求 | 当前 | 判定 |
|---|---|---|---|
| 连续三对 N1–N7 稳定 | 3 对 | **0 对** | 未过 |
| N1 结论/前提屏蔽 | 通过 | 窄义通过（结论屏蔽 ≤0.03；前提影响更大） | 部分 |
| N2 同结论异论证 | 成功对高于控制组 | **失败**（Gauss 1799/1816 仍高于 Bolzano–Cauchy） | 未过 |
| N4 骨架特异性 | 背景出现率 ≤5% | **失败**（语料仅 4 条，5% 不可判） | 未过 |
| 视图口径修订 | 62 + 扩展槽口径已改 | **未修订**（6 条 proposed 仍挂扩展槽） | 未过 |

结论：闸门 **0/3**，不满足“可入图”条件。

## 2. 处理决定

采取“**先落地、标为不入图**”，不采取“先跑够闸门再落地”：

- 落地的是**边定义与校验器**，不是图数据；
- `resembles` 在 `edge-signatures.yaml` 标 `evidence: false`、`provisional: true`、`gate: "连续三对 N1–N7 稳定 + 视图口径修订；当前 0/3"`；
- `graphlint check` 在 `samples/` 与 `pilots/` 中遇到任何 `resembles` 实例，直接报 `EDGE_PROVISIONAL`；
- 当前仓库内 **0 条 `resembles` 实例**，`check-all` 的节点/边/warning 数不变；
- 非证据边不得带 `grade` / `attestation` / `confidence` / `time` / `claims` / `weight`，由 `NON_EVIDENCE_FIELD` 拦截。

这样既能让 schema/validator 先接受评审与测试，又不会把未稳定的相似性结论偷带进图。

## 3. 什么条件下解除 provisional

必须同时满足：

1. 连续三对历史证明在 N1–N7 下稳定；
2. N2、N4 失败项有修正结果，且新结果复现；
3. 视图口径一次性修订完成（62 + 扩展槽）；
4. 至少一对通过双人独立编码（不是同一模型隔离运行）。

解除时改 `provisional: false`，同步 `object-model.md`、README 计数与测试；在此之前不得在 `samples/`/`pilots/` 写实例。

## 4. 本次改动的文件

- `spec/framework/edge-signatures.yaml`：新增 `resembles` 签名与非证据信封字段；
- `tools/graphlint/signatures.py`：`EdgeSig.evidence/provisional/gate`，`non_evidence_required`；
- `tools/graphlint/checks.py`：非证据信封、禁字段、布尔/数组属性、`EDGE_PROVISIONAL`；
- `tools/graphlint/generate.py`：证据/非证据条件 schema、属性声明；
- `spec/framework/graph.schema.json`：重新生成；
- `tools/tests/test_graphlint.py`：5 个新用例；
- 文档计数：README / README.en / docs/repository-guide / PRIORITY / CONTRIBUTING / object-model / CHANGELOG。
