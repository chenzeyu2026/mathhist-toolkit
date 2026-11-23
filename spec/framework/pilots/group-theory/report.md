# 群论分支试点报告（BR-ALG-GRP）

- 分支：`BR-ALG-GRP`（群论），父分支 `BR-FND-AALG`（抽象代数，`kind: taxonomic`）
- 图：`graph.json`（51 节点 / 80 边）
- 长文本：`text.md`（7 个锚点，43 处 `graph://` 反指，40 个不同对象）
- 校验：`graphlint check-all` **0 error**（另有 7 条 `NODE_REQUIRED` warning，为 `TX.chains` 等节点必填字段的历史欠账；`--strict` 下计为 error）；`graph://` 引用 43/43 可解析；11 个节点带 `text_ref`，锚点全部存在
- 规模：新增 51 节点、80 边、23 种边类型；未新增任何节点类型或边类型

选择群论的理由：它是三个试点里唯一"问题早已关闭、研究重心转向结构"的分支。五次方程的可解性在 1830 年代被改写，此后近七十年的主要工作是把群、子群、商群、同态、作用组织成一套互相依赖的概念体。用它来检验 R3 的问题——"研究导向的差异能否由现有 14 类节点、31 类边表达"——比再用一个几何分支更有区分度。

---

## 一、边族与边类型

本报告与论文使用同一套四族划分，族成员固定如下（与 `pilots/calculus/report.md` 及比较脚本一致）：

| 族 | 边类型 |
|---|---|
| 问题与失败 | `targets`、`uses_method`、`corrected_by`、`reformulates`、`spawned`、`poses`、`contradicts`、`competes_with` |
| 理论体系 | `exemplifies`、`depends_on`、`generalizes`、`supersedes`、`resolves` |
| 记号文本 | `uses_notation`、`denotes`、`witness_of`、`derived_from`、`contributed_to`、`supports`、`claimed_in` |
| 归属活动 | `introduced`、`proved`、`participates_in`、`part_of`、`concerns`、`parent_of`、`cross_class`、`prerequisite_of`、`anchors`、`about`、`asserted_by` |

本次实际用到 23 种，共 80 条。

| 边类型 | 次数 | 主要用途 |
|---|---:|---|
| `depends_on` | 17 | 概念链、定理依赖 |
| `supports` | 10 | 文本/印本→概念、理论、方法、主张 |
| `exemplifies` | 5 | 概念/定理→抽象群论 |
| `participates_in` | 5 | 人物→事件 |
| `part_of` | 5 | 事件→问题/定理/理论/失败 |
| `contributed_to` | 5 | 人物→文本（带 `role`） |
| `concerns` | 5 | 分支→概念/问题/理论/文本 |
| `proved` | 4 | 人物→定理 |
| `about` | 3 | 观点→被主张对象 |
| `claimed_in` | 3 | 观点→文本 |
| `resolves` | 2 | 定理/方法→问题 |
| `uses_method` | 2 | 理论/问题→方法 |
| `introduced` | 2 | 人物→概念/方法 |
| `witness_of` | 2 | 印本→书目 |
| `asserted_by` | 2 | 概念/理论→观点 |
| `parent_of` | 1 | 抽象代数→群论 |
| `generalizes` | 1 | 群→置换群 |
| `uses_notation` | 1 | 群→群记号 |
| `denotes` | 1 | 群记号→群 |
| `reformulates` | 1 | 五次方程问题→伽罗瓦判据 |
| `targets` | 1 | 鲁菲尼失败→阿贝尔–鲁菲尼定理 |
| `corrected_by` | 1 | 鲁菲尼失败→阿贝尔 |
| `anchors` | 1 | 教学挂点→群 |

族计数：问题与失败 5、理论体系 25、记号文本 22、归属活动 28。体系/问题 = 25/5 = **5.0**。

**未使用（8 种）**：

| 边类型 | 本次为什么不用 | 是否属结构缺陷 |
|---|---|---|
| `cross_class` | 试点图只展开一条父边；分支目录里的跨类项由 loader 生成，不在本图内 | 否，属取景范围 |
| `prerequisite_of` | 被 `depends_on` 覆盖（与微积分试点结论相同） | 否，重复能力 |
| `supersedes` | 本分支没有被整体取代的理论；抽象群论是扩展，不是取代 | 否，史实如此 |
| `contradicts` | 本试点没有两条互斥且都需保留的主张 | 否，史实如此 |
| `competes_with` | 只有一个记号节点，没有并行记号之争 | 否，粒度选择 |
| `spawned` | 问题演化用 `reformulates` 记"重述"，不是派生新问题 | 否，语义不同 |
| `derived_from` | 两个见证都是独立印本，没有母本—子本关系 | 否，文本链未展开 |
| `poses` | 五次方程的首提者与原始表述未核到，按 `U` 处理且未挂人 | 是，证据缺口（见第五节） |

三试点并集覆盖 29/31，仅缺 `prerequisite_of` 与 `spawned`。

---

## 二、节点类型分布

| 类型 | 数量 | 类型 | 数量 |
|---|---:|---|---:|
| `branch` | 2 | `person` | 9 |
| `concept` | 9 | `text` | 7 |
| `theorem` | 5 | `witness` | 2 |
| `problem` | 2 | `event` | 5 |
| `theory` | 2 | `statement` | 3 |
| `method` | 2 | `teaching_point` | 1 |
| `notation` | 1 | `failure` | 1 |

14 类节点全部用到。问题与失败各只有 1–2 个，不是遗漏：群论史在这一段的可指认失败主要就是鲁菲尼的缺口；把"没人做出来"写成失败节点会违反 §7.2 的判定（未证明 ≠ 失败）。

---

## 三、R3 检验：导向能否由现有结构表达

要检验的是两类研究路线——**问题导向**与**体系化导向**——能否只用现有 14 类节点、31 类边写清，而不就地扩表。

### 3.1 问题导向：能

五次方程这条线是完整的问题导向样本，全部用现有类型表达：

- 问题：`PR:quintic-solvability`；重述：`reformulates` 指向 `PR:quintic-galois-criterion`
- 解答：`TH:abel-ruffini` 与 `ME:galois-correspondence` 各有一条 `resolves`
- 失败：`FA:ruffini-1799-quintic` 用 `targets` 指向断言、`corrected_by` 指向纠正者
- 方法：`uses_method` 两条，分别从问题和理论出发

没有新增类型。唯一需要说明的是 `targets` 的落点：失败指向的是"被主张的断言"（定理），不是"问题"。这与非欧几何样板中萨凯里 `targets` 指向问题的写法不同，但两者遵循同一条规则——指向该失败路线**想确立的对象**。

### 3.2 体系化导向：能，但它是剖面不是节点

群论在 1870 年代之后的写法，在图上表现为三件事同时出现：

1. **边族配比**：`depends_on` 17 + `exemplifies` 5 + `generalizes` 1 + `resolves` 2 = 理论体系 25 条；问题与失败只有 5 条。
2. **父边 `kind`**：`BR-FND-AALG --parent_of--> BR-ALG-GRP` 是 `taxonomic`（分类包含），不是 `historical`（历史衍生）。前者说的是今天的学科结构，后者说的是从哪个领域长出来。非欧几何与微积分的父边都是 `historical`。
3. **`affected_layers` 剖面**：问题 high、失败 medium、记号 high、文本 high。

这三项都不需要新节点。也就是说，"体系化导向"不是图上的一个对象，而是**一组可复算的标注结果**。本试点据此确认：现有结构够用，不需要为"导向"新增节点类型或边类型。

### 3.3 具体纲领：能，用 `TY:` 承载

埃尔朗根纲领有一位主张者（`PE:klein`）、一份文本（`TX:klein-1872-erlangen`）、一条可归属的主张（`ST:klein-group-geometry`）、一组可由此推出的研究任务。四点齐备，正好落在 `theory` 的定义"一套假设加上它的推论体"上，因此用 `TY:erlangen-program` 承载，配 `asserted_by`/`claimed_in`/`supports`/`part_of` 四条边即可。

这与"一般导向"的差别是硬的：**有主张者、有文本、有推论体**的才建 `TY:`；只有"某学派偏重结构"这类印象的，不建节点，只记边族配比与 `affected_layers`。前者是可质疑的断言，后者是标注者的概括，两者不能混成一种对象。

### 3.4 结论与边界

- **结论**：问题导向、体系化导向、具体纲领，均可由现有 14 类节点 + 31 类边表达；未就地扩表。
- **代价**：一般导向只能以"边族比值 + 父边 kind + affected_layers"的剖面形式出现，不能作为一个可点击的节点被查询。如果将来确实需要"按导向检索分支"，得先决定它是不是一个可归属的主张；是，就建 `TY:`/`ST:`；不是，就保持剖面。
- **边界**：三试点、单标注者、四族划分为本项目自定，因此这些比值是**描述性指标**，不是史学因果结论，也不能用来判断某位数学家的主观取向。

---

## 四、真实填充时哪里别扭

1. **`targets` 的落点在"问题"与"断言"之间摇摆。** 萨凯里指向问题，鲁菲尼指向定理，两种写法都合 §5.6，但同一份图里出现两种落点，读者会以为规则不一致。建议在 §5.6 补一句判定：失败路线瞄准的是它想确立/推翻的那个对象，不是它所属的领域问题。
2. **`proved` 只记"谁证明了"，不记"哪一年、哪份文本"。** 本次把年份放在事件节点、文本放在 `TX`，再用 `participates_in`/`supports` 连起来；一条证明因此要三条边。属性缺口，不是类型缺口。
3. **埃尔朗根纲领的归属是取景决定。** 它属于几何，本试点因"用群论重写几何"挂在 `BR-ALG-GRP` 的 `concerns` 下。图上没有"借用"这类边，只能在 `note` 里说明。
4. **伽罗瓦手稿没有 `TW`。** 图上能追到"哪份手稿"，追不到 1846 年刊行与页码。文本链未展开，不是结构不支持。
5. **`introduced` 同时用于"提出概念"与"提出方法"。** 凯莱→群、伽罗瓦→伽罗瓦对应，两者语义不完全相同，靠端点类型区分。

---

## 五、证据缺口

| 项目 | 结果 |
|---|---|
| `grade` 分布 | S 20、F 60、U 0、A 0 |
| S 级定位 | 20/20 只到"Wussing 1984（章次页码待补）"，属**S 级但定位不足** |
| 有页级定位的条目 | 凯莱 1854（p.40–47）、西罗 1872（p.584–594）两处 |
| A 级 | 0，未核对任何原件或影印本 |
| 首提者缺口 | 五次方程的原始提出者与首见文本未核到，因此没有 `poses` 边 |

这份图不能说"已核实"。它说的是：每条边都有来源与等级；S 级的来源目前只到专著，页码待补；A 级需要进馆藏或影印本，本次没有做。把这一点写在报告里，比把 S 模糊成"已核实"更符合 `evidence-tags.md` 的口径。

---

## 六、校验与计数

| 项目 | 结果 |
|---|---|
| 结构校验（`graphlint check-all`） | 51 节点 / 80 边，**0 error** / 7 warning（节点必填字段历史欠账） |
| `text.md` → `graph://` 引用 | 43 处、40 个不同对象，全部可解析 |
| `graph.json` → `text.md` 锚点 | 11 个节点带 `text_ref`，7 个锚点全部存在 |
| 新增节点 | 51 |
| 新增边 | 80 |
| 新增节点类型 | 0 |
| 新增边类型 | 0（未扩表） |

校验覆盖：ID 唯一与派生格式、端点存在、端点类型白名单、必填键、时间 precision、U 必带 note、attestation↔grade 自洽、对称边 `directed:false`、`parent_of` 权重和、`witness_of` 唯一、`depends_on` 无环、孤立节点、`text_ref` 文件与锚点。
