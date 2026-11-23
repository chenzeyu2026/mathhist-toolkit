# 微积分分支试点报告（BR-ANA-CALC）

- 分支：`BR-ANA-CALC`（微积分），父分支 `BR-FND-AGEO`（解析几何），跨类到 `BR-APP-MECH`（力学）
- 图：`graph.json`（58 节点 / 102 边）
- 长文本：`text.md`（6 个锚点，50 处 `graph://` 反指）
- 校验：结构校验 0 错误，schema-lite 0 错误，`graph://` 引用 50/50 可解析
- 规模：新增 58 节点、102 边、27 种边类型；未新增任何边类型

选择微积分的理由：它是少数能把四层同时压满的分支——问题层（切线/求积 → 无穷小合法性 → 极限基础）、失败层（贝克莱批评与无穷小演算被取代）、记号层（dy/dx vs 点记法、∫、ε-δ）、文本层（1671 手稿 → 1684 刊行 → 1696 教科书 → 1859 汉译）。群论与非欧几何两个样板中，前者的失败层与记号层偏薄，后者的问题层偏单一，都不如微积分能同时检验四条边线。

---

## 一、边类型使用频次

本次实际用到 27 种，共 102 条。

| 边类型 | 次数 | 主要用途 |
|---|---:|---|
| `concerns` | 10 | 分支挂概念/问题/定理/理论/文本 |
| `introduced` | 9 | 人物→概念/记号/方法 |
| `contributed_to` | 8 | 人物→文本/见证（带 `role`） |
| `witness_of` | 8 | 载体→书目 |
| `supports` | 8 | 文本/载体→被支撑对象 |
| `depends_on` | 7 | 概念/定理/方法→前置 |
| `anchors` | 7 | 教学挂点→概念/问题/记号 |
| `uses_notation` | 6 | 概念/理论/方法→记号 |
| `denotes` | 6 | 记号→概念 |
| `participates_in` | 5 | 人物→事件 |
| `resolves` | 4 | 方法/定理→问题 |
| `part_of` | 4 | 事件→问题/失败 |
| `parent_of` | 2 | 分支父子 |
| `exemplifies` | 2 | 概念→理论 |
| `derived_from` | 2 | 子载体→母载体 |
| `about` | 2 | 观点→被主张对象 |
| `claimed_in` | 2 | 观点→文本 |
| `cross_class` | 1 | 微积分↔力学（`method_source`） |
| `poses` | 1 | 贝克莱→无穷小合法性问题 |
| `reformulates` | 1 | 无穷小问题→极限问题 |
| `supersedes` | 1 | 旧理论→新理论 |
| `targets` | 1 | 失败路线→被批评理论 |
| `corrected_by` | 1 | 失败路线→柯西 |
| `uses_method` | 1 | 失败路线的纠正所用方法 |
| `competes_with` | 1 | dy/dx ↔ 点记法 |
| `contradicts` | 1 | 贝克莱观点 ↔ 无穷小辩护观点 |
| `asserted_by` | 1 | 理论→观点 |

**未使用（4 种）**：`prerequisite_of`（被 `depends_on` 覆盖）、`generalizes`（本次无一般/特殊概念对）、`proved`（本次不单独记证明归属，写在 `claims[]`）、`spawned`（问题演化用 `reformulates`，不是派生）。

使用率 27/31，说明**边类型大体够用**；真实填充时缺的主要是**边的属性**，不是新的边类型。按用户要求，只记录、不裁剪。

时间与证据分布（供裁剪判断参考）：

- `grade`：S 77、F 24、U 1、A 0 —— 本次未核任何原件，A 级不可达。`attestation` 相应为 `later_report` 77、`textbook_simplification` 24、`unknown` 1。
- 22 条边的时间两端为 null（`precision: unknown`），主要是"现代教科书定义"类结构性断言。
- 58 个节点的 `occurrences[]` **全部为空**：时间信息都挂在边上，节点级的 occurrence 在本分支没有被用到。

---

## 二、缺口清单（未就地扩表）

| # | 缺口 | 本次怎么绕的 | 建议（仅记录，不实施） |
|---|---|---|---|
| 1 | 无法表达两次发现"相互独立" | 两条 `introduced` 边各带时间与文献，独立性写在 `note` | 可考虑边属性 `independence: independent/derived/contested/unknown`，复用 `occurrence` 已有的取值域 |
| 2 | `denotes` 只能 NO→CO，学科名"微积分"作为术语无处可挂 | 只给"微分/积分"建译名节点，分支名不进记号线 | 允许 `denotes` 的 to 为 `branch`，或另建 `names` 边 |
| 3 | "某人 + 某译本 + 某译名"是三元组 | 拆成 `introduced`（人→译名）+ `contributed_to`（人→译本）+ `supports`（译本→译名） | 三元组关系不适合用二元边硬拼；可考虑给 `introduced` 加 `via` 指向载体 |
| 4 | 批评者与被批评理论缺直接边（`contradicts` 仅 ST↔ST） | 建两个 `ST:` 观点节点，用 `contradicts` 连观点，再各自 `about` 理论 | 若要保留"谁批谁"的简洁表达，需允许 `PE/ST → TY/TH` 的批评边 |
| 5 | `competes_with` 无法表达"两套记号在不同领域各自胜出" | 只记一条无向竞争边，分工写进 `note` | 可加边属性 `outcome: coexist/partition/replace` |
| 6 | `failure` 节点无"提出者/作者"字段 | 借事件节点 + `participates_in` 挂人 | 与 #1 类似，属属性缺口而非类型缺口 |
| 7 | `targets` 原约束禁止 `FA→PR`，与 §7.5 冲突 | 已在 v0.2 修订为允许 `FA→PR`（§11 有记录） | 已解决，保留在此备查 |
| 8 | "同一概念的解释权重随时间转移"（如瞬时速度）无表达 | 只能靠 `depends_on` 的时间窗近似 | 暂不建议加边；加一条边只能表达一次转移，容易退化成时间线 |

---

## 三、真实填充时哪里别扭

1. **`supersedes` 方向反直觉。** §5.6 规定 from 为旧、to 为新；英文 "X supersedes Y" 的语感是 X 新、Y 旧。本次填充时就写反过一次，靠对照 §4.0 的 `superseded_by` 映射才纠正。建议在 §5.6 该行补一句"边名读作『旧被新取代』"。
2. **边 ID 由端点派生，改端点必须改 ID。** 上述方向翻转同时要改 `id`，没有工具辅助时容易漏。优点是无需注册表，代价是任何端点修订都是字符串手术。
3. **`corrected_by` 只指向人，不指向理论或方法。** 本次用 `FA→uses_method>ME:epsilon-delta-method` 表达"纠正所采用的方法"，但这与"失败路线本身用过该方法"同形，只能靠 `note` 区分。这一格语义偏挤。
4. **`concerns` 只能从分支出。** 填图时思路常是"这个概念属于哪个分支"，但要反向找分支 ID 再连，节点侧没有对应入口。
5. **`occurrences[]` 在本分支完全冗余。** 微积分的对象几乎都是"事件型"或"文本型"，时间天然落在边和事件节点上；节点级 occurrence 只在跨文明传播（如非欧几何样板）时才划算。

## 四、哪条约束其实用不上

- **`occurrences[]` 的存在性要求**（非 proposed 节点不必填，实际 58/58 全空）：对单一文明内演化的分支，这套字段是负担。
- **`claimant`（无 source 的边）**：本次 0 条。所有边都能给 `source`（哪怕是 `source.locator` 的弱来源），`claimant` 这条备用通路没有被触发。
- **边级 `text_ref`**：本次 0 条。边都是一句话断言，长论证放在节点 `text_ref` 指向的文档里更自然；边级指针目前是空置能力。
- **`prerequisite_of` / `generalizes` / `proved` / `spawned`**：见第一节，均被现有边或 `claims[]` 覆盖，本次没有使用场景。

---

## 五、校验与计数

| 项目 | 结果 |
|---|---|
| 结构校验（`validate_mathhist_graph.py`） | 58 节点 / 102 边，**0 错误** |
| schema-lite（`schema_lite_mathhist.py`） | 58 节点 / 102 边，**0 错误** |
| `text.md` → `graph://` 引用 | 50 处，全部可解析（含节点与边 ID） |
| `graph.json` → `text.md` 锚点 | 7 个节点带 `text_ref`，6 个锚点全部存在 |
| 新增节点 | 58 |
| 新增边 | 102 |
| 新增边类型 | 0（未扩表） |

校验覆盖：ID 唯一与派生格式、端点存在、端点类型白名单、必填键、时间 precision、U 必带 note、attestation↔grade 自洽、对称边 `directed:false`、`parent_of` 权重和、7 类边无环、孤立节点、`text_ref` 文件与锚点、`claims[].source.text` 必须在图内。
