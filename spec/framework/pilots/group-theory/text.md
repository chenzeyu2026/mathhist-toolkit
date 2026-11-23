# 群论：从一次失败的证明到一套结构

本文是 `BR-ALG-GRP`（群论）分支的试点长文本，与同目录 `graph.json` 双向互指：本文每个关键处用 `graph://` 前缀加节点或边 ID 指向图；图节点里凡写入 `text_ref` 的，都指回本文对应小节。

讲解不按编年铺开，而按"一个问题怎样被改写、一套结构怎样长出来"组织。最后一节说明：如果用现有节点与边去标"研究导向"，图上到底能读出什么、读不出什么。

---

## 一个问题的两次改写 {#quintic}

十六到十八世纪的代数里，五次方程是一个"求公式"的问题：`graph://PR:quintic-solvability`。它与二次、三次、四次方程的问题同形——给定系数，用加减乘除与开方把根写出来。四次方程在十六世纪已被解出，五次方程却一直没有人成功，问题因此长期停留在"还没找到公式"的状态，而不是"不可能有公式"。

1832 年之后，同一个对象被换了一种提法：`graph://PR:quintic-galois-criterion`——方程根式可解，当且仅当它的伽罗瓦群可解。图里这条改写是一条边，不是一句转述：

- `graph://E:PR:quintic-solvability>reformulates>PR:quintic-galois-criterion`

`reformulates` 只表示"后世重新表述"，不表示"解决"。两个问题各自有自己的解：

- `graph://TH:abel-ruffini` 以否定方式回答第一个问题：一般五次及以上方程没有根式解。对应边 `graph://E:TH:abel-ruffini>resolves>PR:quintic-solvability`。
- `graph://ME:galois-correspondence` 回答第二个问题：它给出一套可操作的判定程序。对应边 `graph://E:ME:galois-correspondence>resolves>PR:quintic-galois-criterion`，反向还有 `graph://E:PR:quintic-galois-criterion>uses_method>ME:galois-correspondence`。

把两条 `resolves` 分开写，是为了不把"证明不可能"和"给出判据"压成"解决了五次方程问题"。前者关闭了求公式的路，后者打开了用群讨论方程的路；它们是同一个问题的两种结局。

---

## 鲁菲尼的缺口 {#ruffini}

`graph://FA:ruffini-1799-quintic` 是这次试点里唯一一个失败节点。它的 `failure_kind` 是 `false_proof`：结论对，推理不完整。缺口在于，从置换的性质推到"一般五次方程不可根式解"时，只覆盖了部分情形，没有证明对一般 $n$ 成立。

这里有一个容易写错的地方：失败节点的 `targets` 指向 `graph://TH:abel-ruffini`，而不是指向问题。原因不是"鲁菲尼预见了阿贝尔定理"，而是 `targets` 记的是**这条失败路线想确立的那个断言**。他想要的正是一般五次方程不可解；他没有做到的是把这一步证完整。问题在 `PR:quintic-solvability` 上，断言在 `TH:abel-ruffini` 上，失败发生在"断言"这一侧，所以边指向定理。这一点与萨凯里的例子结构相同：萨凯里想证明的是"第五公设可证"，失败也发生在断言侧。

失败节点还要求写"当时为什么被接受"。图里记的是：结论与当时零散的计算证据一致，而可检验的群论判据尚未出现，审阅者缺少定位缺口的语言。纠正者是阿贝尔：`graph://E:FA:ruffini-1799-quintic>corrected_by>PE:abel`，同一条链上还有 `graph://E:PE:abel>proved>TH:abel-ruffini` 与 `graph://E:EV:1799-ruffini-quintic>part_of>FA:ruffini-1799-quintic`。

---

## 伽罗瓦把"可解"改写为"群可解" {#galois}

伽罗瓦的工作在图里落在三个位置：方法 `graph://ME:galois-correspondence`、问题 `graph://PR:quintic-galois-criterion`、文本 `graph://TX:galois-manuscript-1832`。

方法依赖两个概念：`graph://E:ME:galois-correspondence>depends_on>CO:group` 与 `graph://E:ME:galois-correspondence>depends_on>CO:normal-subgroup`。前者说明它用的是群，后者说明"正规子群—商群"这条链是判据成立的关键。文本支撑方法：`graph://E:TX:galois-manuscript-1832>supports>ME:galois-correspondence`；手稿这件事本身是事件：`graph://E:EV:1832-galois-manuscript>part_of>PR:quintic-galois-criterion`。

需要说明一个证据缺口：本试点给伽罗瓦手稿只建了 `TX`，没有建 `TW` 见证节点，也没有记 1846 年李维尔在《纯数学与应用数学杂志》上的刊行。也就是说，图上能追到"哪份手稿"，追不到"哪次刊行、哪一页"。这是文本链没填满，不是结构不支持——非欧几何样板里《原本》的希腊—阿拉伯—拉丁—汉译四条链，用的就是同一套 `TX`/`TW`/`witness_of`/`derived_from`。

---

## 凯莱 1854：把群从置换里拿出来 {#cayley}

在此之前，"群"主要是置换的集合，讨论对象是具体的置换运算。凯莱 1854 年的论文换了一个写法：群可以由符号及其合成规则定义，不必先是一个置换集合。图里这条主张是观点节点，不是概念本身：

- 主张：`graph://ST:cayley-abstract-group`（"群可由生成元与关系定义"）
- 它关于哪个对象：`graph://E:ST:cayley-abstract-group>about>CO:group`
- 它写在哪：`graph://E:ST:cayley-abstract-group>claimed_in>TX:cayley-1854`
- 概念由谁提出这一主张：`graph://E:CO:group>asserted_by>ST:cayley-abstract-group`

这里必须区分"概念"和"关于概念的主张"。`CO:group` 是那个结构；`ST:cayley-abstract-group` 是"这个结构可以脱离置换来定义"这一条可归属、可质疑的主张。凯莱之后仍有人只把群当置换群用，主张被接受是后来的事。把两者分开，图上才能同时容纳"概念已存在"和"关于它的定义方式仍有争议"。

文本与实物这一侧只有两层，没有铺满：`graph://TX:cayley-1854` 有期刊印本 `graph://TW:cayley-1854.print`，`witness_of` 指回书目，`supports` 指向概念与主张。这足以说明"这句话有印本依据"，但不足以说明"这一版与后来的重印有何差异"。

---

## 体系化：西罗、若尔当、伯恩赛德 {#systematic}

从 1870 年代起，群论的写作重心从"解方程"转向"整理结构"。图上这一段最密的不是问题边，而是概念之间的依赖边：

- 子群链：`graph://E:CO:subgroup>depends_on>CO:group` → `graph://E:CO:normal-subgroup>depends_on>CO:subgroup` → `graph://E:CO:quotient-group>depends_on>CO:normal-subgroup` → `graph://E:CO:solvable-group>depends_on>CO:quotient-group`
- 作用与同态：`graph://E:CO:group-homomorphism>depends_on>CO:group`、`graph://E:CO:group-action>depends_on>CO:group`
- 西罗子群：`graph://E:CO:sylow-subgroup>depends_on>CO:subgroup`；西罗定理同时依赖柯西定理：`graph://E:TH:sylow-theorems>depends_on>TH:cauchy-theorem`

对应的史实节点是：西罗 1872 年的三条定理（`graph://TX:sylow-1872`，期刊页码 584–594）、若尔当 1870 年《置换论》（`graph://TX:jordan-1870`）、伯恩赛德 1897 年《有限群论》（`graph://TX:burnside-1897`）。若尔当那条主张被单独建成观点节点：`graph://ST:jordan-systematic`——"置换群应作为整体系统处理"，`about` 指向分支 `graph://E:ST:jordan-systematic>about>BR-ALG-GRP`。

这一段的图形态与上一段明显不同：问题只有两个，失败只有一个，而 `depends_on` 有 17 条、`exemplifies` 有 5 条。定理不是围绕"下一个未解问题"排列，而是围绕概念结构排列。第七节会把这组数字与另外两个试点放在一起看。

---

## 埃尔朗根纲领：另一种"纲领" {#erlangen}

克莱因 1872 年的就职演说把几何定义为"变换群下的不变量理论"。图里它是一个理论节点 `graph://TY:erlangen-program`，带一条可归属的主张 `graph://ST:klein-group-geometry`、一份文本 `graph://TX:klein-1872-erlangen`、一个事件 `graph://EV:1872-erlangen-program`。

"纲领"不是比喻：它有一位主张者、一份文本、一组可以由此推出的研究任务（按变换群给几何分类）。这三点齐备时，`TY:` 这一类型就能承载它，不需要新增"纲领"节点。反过来，如果只有"某学派偏重结构"这种印象，没有主张者、没有文本、没有推论体，那就不该建节点——硬建一个 `TY:` 只会得到一条无法质疑的标签。

这里还有一个建模上的取舍要说明：埃尔朗根纲领属于几何，不属于群论。本试点把它挂在 `BR-ALG-GRP` 的 `concerns` 下，是因为它**用**群论重写了几何，而不是因为群论史把它算作自己的内部成果。这是取景决定，不是史学归属；同一份材料换一个分支挂，结构不变，`concerns` 的端点会变。

---

## 导向在图上长什么样 {#orientation}

把三个试点放在一起，每个分支的边按用途分成四族（族的具体成员见 `report.md` 第一节），其中两族的比值最能区分写法：

| 分支 | 问题与失败边 | 理论体系边 | 体系/问题 |
|---|---:|---:|---:|
| 非欧几何 | 12 | 6 | 0.5 |
| 微积分 | 7 | 14 | 2.0 |
| 群论 | 5 | 25 | 5.0 |

群论这一行是 5 比 25：失败只有鲁菲尼一处，问题只有五次方程的两个提法，其余 25 条边都在概念、定理、理论、方法之间建立依赖与例示。非欧几何相反，问题与失败边是理论体系边的两倍。微积分居中。

除了边族比值，还有两个信号：

1. **父边的 `kind`**。群论的 `parent_of` 只有一条，`kind` 是 `taxonomic`（抽象代数分类包含群论）；非欧几何与微积分的父边都是 `historical`（历史衍生）。分类包含说的是"今天的学科结构"，历史衍生说的是"从哪个领域长出来"，两者不能互换。
2. **`affected_layers` 剖面**。群论是问题高、失败中、记号高、文本高；非欧几何是问题高、失败高、记号中、文本高。这是分支级的人工标注，不是从边上算出来的。

**能读出什么**：这三组数是可复算的，换一个人按同一份边表重算，会得到同一组比值；它们描述的是"这份图把多少笔墨花在问题与失败上，多少花在结构关系上"。

**读不出什么**：它不能说明某位数学家"主观上更偏体系"，也不能说明群论在 1870 年代之后不再有问题——只能说明**本次标注**把哪些关系写成了边。三个试点、同一标注者、无盲法，因此这是一组描述性指标，不是史学因果结论。要把它变成可比较的测量，至少还需要：更多分支、第二标注者、以及事先约定的边族定义。
