# 阿克曼函数线：v0.2 本体映射与分支判断

- 依据：`spec/object-model.md`（14 类节点 / 31 类边）、`spec/evidence-tags.md`、`spec/framework/branches.json`
- 史实来源：同目录 `note.md` 的 M1–M11、E1–E20、U1–U22。本文只做映射与判断，不重复证据正文。
- 状态：案例骨架，不是校验通过的 `graph.json`。节点/边数量是示例规模，不是完整图包。
- 口径：不就地扩表。发现缺口只登记，不新增节点类型或边类型。

---

## 0. 一句话结论

**数学侧能完整落进 v0.2；工程侧只能落进一半。** 落不进去的集中在五处：没有"系统/语言/实现"类型、没有"约束/适用边界"边、没有"有序等级"类型、没有"测量结果"类型、事件与方法之间缺少可用边。因此本轮判断是：**不为阿克曼开分支，也不开"计算机史"第 63 支**；先用 `BR-LOG-REC` 与 `BR-CS-TCS` 的跨类共享对象做案例，同时用 `proposed` 的"计算实践史"扩展槽跑 2–3 个案例验证缺口是否重复。

---

## 1. 节点骨架

### 1.1 核心节点（概念 / 定理 / 问题 / 方法 / 理论）

| ID | 类型 | 标签 | 依据 | 映射要点 |
|---|---|---|---|---|
| `CO:ackermann-function` | concept | 阿克曼函数 | M1–M3、E2 | 定义取 Robinson 形式；`occurrences` 记 1928，不把"希尔伯特提到"写成发明 |
| `CO:primitive-recursive-function` | concept | 原始递归函数 | M5、M6 | 与 LOOP 程序同外延，见 `TH:loop-characterizes-primitive-recursive` |
| `CO:general-recursive-function` | concept | 一般递归函数 | M5 | 阿克曼函数是它的成员，不是"不可计算"的代表 |
| `CO:loop-program` | concept | LOOP 程序 | M6、E6 | **这里已经暴露出缺口 G1**：LOOP 是一门语言，被硬塞进 concept |
| `CO:ackermann-rating` | concept | 阿克曼评级 | E16 | 有序等级无处安放，见 G3 |
| `CO:grzegorczyk-hierarchy` | concept | Grzegorczyk 层级 | E17 | 与 E0–E4 的层级对应 |
| `CO:stack-depth` | concept | 递归栈深度 | E4、E8 | 把"栈深上限"概念化；具体机器的上限值无处挂，见 G4 |
| `CO:implementation-quality` | concept | 实现质量 | E5 | Wichmann 的核心解释变量 |
| `TH:ackermann-not-primitive-recursive` | theorem | 阿克曼函数非原始递归 | M3、M5 | `proof_status: proved`；1928 |
| `TH:hilbert-primitive-recursion-conjecture` | theorem | 所有可计算函数都原始递归（猜想） | M4 | `proof_status: disproved`；反例写在 `counterexamples` 字段，图上没有反例边，见 G6 |
| `TH:loop-characterizes-primitive-recursive` | theorem | LOOP 程序恰好刻画原始递归函数 | M6、E6 | 1967；原文定理 7 |
| `TH:max-depth-equals-value-minus-one` | theorem | 朴素求值最大深度 = 函数值 − 1 | E2 | Sundblad 1971；工程换算的上游 |
| `TH:iterative-ackermann-linear-space` | theorem | 阿克曼函数可用 O(i) 空间迭代计算 | E7 | Grossman–Zeitman 1988 |
| `TH:ackermann-rating-apl-four` | theorem | 传统 APL 的 Ackermann rating 恰为 4 | E16 | Breidbart 1979 |
| `TH:apl-execute-unbounded` | theorem | 带 execute 的 APL 评级为无穷 | E16 | Breidbart 1979；Linden 1971 已主张至少 5 |
| `PR:primitive-recursion-sufficiency` | problem | 原始递归是否穷尽能行可计算函数 | M1、M5 | `status: resolved`；1928 由阿克曼回答 |
| `PR:loop-expressiveness` | problem | LOOP 程序能计算哪些函数 | M6 | `status: resolved`；1967 |
| `PR:optimize-ackermann` | problem | 如何把阿克曼函数改成可行算法 | E7、E9–E12 | `status: partially_resolved`；迭代、部分求值、增量化各给一部分 |
| `PR:language-rating` | problem | 如何按阿克曼层级给编程语言评级 | E16 | Brown 1970 提出，Breidbart 1979 给出精确结果 |
| `PR:ackermann-feasible-arguments` | problem | 给定资源下能算到哪个 n | E4、E8、E15 | 工程问题；不是"哪些参数不可计算" |
| `ME:ackermann-higher-recursion` | method | 1928 高阶递归构造 | M3 | `kind: construction`；不是现代三行定义 |
| `ME:peter-nested-recursion` | method | 1935 二元嵌套递归 | M7 | 今天教科书形式的直接来源 |
| `ME:robinson-definition` | method | 1948 标准三行定义 | M8 | 被后续文献当作"标准定义" |
| `ME:naive-recursive-evaluation` | method | 朴素递归求值 | E2 | 深度与调用次数可算，是测试载体 |
| `ME:explicit-stack-ackermann` | method | 显式栈迭代（Stackermann） | E7 | 空间 O(A(i,n))，工程上很快撞墙 |
| `ME:iterative-ackermann` | method | 计数式迭代算法 | E7 | 空间 O(i)，时间 O(i·A(i,n)) |
| `ME:memoized-ackermann` | method | 记忆化/表格化 | E11 | 空间 O(A(i,n))，只在小参数可行 |
| `ME:partial-evaluation-ackermann` | method | 程序点特化 | E12 | 固定 m=2，算术运算减半 |
| `ME:incrementalization-ackermann` | method | 增量化 | E11 | Liu–Stoller 2003；O(i) 空间 |
| `ME:tail-elimination-outer-calls` | method | 消去两个外层调用的递归 | E18 | Bliss 实测约 20%；**适用边界只能写进 `complexity_note`**，见 G2 |
| `TY:hilbert-program` | theory | 希尔伯特纲领 | M1 | 原始递归被视为有穷主义工具 |
| `TY:grzegorczyk-hierarchy` | theory | Grzegorczyk 层级理论 | E17 | E4 与 APL 单行函数对应 |
| `TY:partial-evaluation` | theory | 部分求值 | E12 | Jones 1996 的框架 |

### 1.2 记号 / 人物 / 文本 / 见证 / 事件 / 观点 / 教学

| ID | 类型 | 标签 | 依据 | 映射要点 |
|---|---|---|---|---|
| `NO:ackermann-phi` | notation | φ(x,y,z) | M3 | 1928 的三元记号；`denotes` 指向阿克曼函数 |
| `NO:ackermann-A` | notation | A(m,n) | M8 | 现代二元记号；与 φ 是 `supersedes` 关系，不是"错误" |
| `NO:ackermann-rating-term` | notation | "Ackermann rating" | E16 | 术语节点；指向 `CO:ackermann-rating` |
| `PE:hilbert` | person | 希尔伯特 | M1、M2 | `poses` 问题；`contributed_to` 《论无穷》 |
| `PE:ackermann` | person | 阿克曼 | M1–M3 | `proved` 非原始递归；`contributed_to` 1928 |
| `PE:peter` | person | 罗莎·佩特 | M7 | `contributed_to` 1935；**不要**用 `introduced` 抢阿克曼的首创 |
| `PE:sudan` | person | 苏丹 | M10 | 独立发现；用平行边，不用 `contradicts` |
| `PE:robinson` | person | 罗宾逊 | M8 | 标准化定义 |
| `PE:kleene` | person | 克莱尼 | M1 | 教科书转述；不作为一手 |
| `PE:meyer` / `PE:ritchie` | person | Meyer / Ritchie | M6、E6 | `proved` LOOP 定理 |
| `PE:brown` | person | J. A. Brown | E16 | `introduced` Ackermann rating |
| `PE:linden` | person | T. A. Linden | E16 | 主张 execute → 无穷 |
| `PE:breidbart` | person | Seth Breidbart | E16 | `proved` APL = E4 |
| `PE:sundblad` | person | Yngve Sundblad | E2 | 基准测试与评级表 |
| `PE:wichmann` | person | B. A. Wichmann | E3–E5、E18 | 40/60 系统；Bliss 20% 的记录者 |
| `PE:grossman` / `PE:zeitman` | person | Grossman / Zeitman | E7 | 迭代算法 |
| `PE:jones` | person | Neil Jones | E12 | 部分求值示例 |
| `PE:liu` / `PE:stoller` | person | Liu / Stoller | E11 | 增量化 |
| `TX:hilbert-1926` | text | 《Über das Unendliche》 | M1、M2 | 原文未读；`text_type: original` |
| `TX:ackermann-1928` | text | 《Zum Hilbertschen Aufbau der reellen Zahlen》 | M1–M3 | 书目与脚注已核；正文未通读 |
| `TX:sudan-1927` | text | 苏丹 1927 | M10 | 书目已核 |
| `TX:peter-1935` | text | 《Konstruktion nichtrekursiver Funktionen》 | M7 | 书目已核 |
| `TX:robinson-1948` | text | 罗宾逊 1948 | M8 | 书目已核 |
| `TX:kleene-1952` | text | 《Introduction to Metamathematics》 | M1 | 页码未核 |
| `TX:brown-1970` | text | 用阿克曼函数给语言评级 | E16 | 书目已核，原文未读 |
| `TX:sundblad-1971` | text | 阿克曼函数研究 | E2 | PDF 全文 |
| `TX:linden-1971` | text | 阿克曼函数在 APL 中 | E16 | 卷页有冲突，见 U11 |
| `TX:wichmann-1976` | text | 过程调用效率研究 | E3、E4 | 作者版 PDF |
| `TX:wichmann-1977` | text | 再论阿克曼函数 | E5、E18 | PDF 全文 |
| `TX:breidbart-1979` | text | APL 与 Grzegorczyk 层级 | E16 | PDF 全文 |
| `TX:grossman-zeitman-1988` | text | 固有迭代计算 | E7 | PDF 全文 |
| `TX:jones-1996` | text | 部分求值导论 | E12 | 相关节 |
| `TX:liu-stoller-2003` | text | 增量化优化阿克曼函数 | E11 | PDF 全文 |
| `TX:llvm-ackermann` | text | LLVM test-suite 基准 | E14 | 源码已核；`text_type` 无"源码/测试"档，见 G7 |
| `TX:emscripten-0007` | text | Emscripten 补丁 0007 | E14 | 补丁正文已核；`text_type` 无"补丁"档，见 G7 |
| `TW:ackermann-1928.print` | witness | 1928 印刷版 | M1 | `witness_kind: original`，`extant: true` |
| `TW:sundblad-1971.pdf` | witness | Sundblad PDF | E2 | `witness_kind: copy`；不是出版方原件 |
| `TW:wichmann-1977.pdf` | witness | Wichmann 1977 PDF | E5 | 作者页/镜像，非出版方原件 |
| `TW:emscripten-0007.patch` | witness | 补丁文件快照 | E14 | **`witness_kind` 没有"版本控制快照"档**，见 G7 |
| `EV:1926-hilbert-munster` | event | 希尔伯特明斯特讲演 | M1 | 1925 讲演 / 1926 发表，`precision: circa` 或区间 |
| `EV:1928-ackermann` | event | 阿克曼发表 | M1–M3 | 收稿 1927-01-20，刊出 1928-12 |
| `EV:1935-peter` | event | 佩特简化 | M7 | 1935 |
| `EV:1948-robinson` | event | 罗宾逊标准化 | M8 | 1948 |
| `EV:1967-meyer-ritchie` | event | LOOP 定理发表 | M6 | 1967 |
| `EV:1970-brown` | event | 评级想法提出 | E16 | 1970-04 |
| `EV:1971-sundblad` | event | Sundblad 基准发表 | E2 | 1971 |
| `EV:1976-wichmann` | event | 40 系统测试 | E3 | 1976 |
| `EV:1977-wichmann` | event | 60 系统与反思 | E5 | 1977 |
| `EV:1979-breidbart` | event | APL 评级精确化 | E16 | 1979 |
| `EV:1988-grossman-zeitman` | event | 迭代算法发表 | E7 | 1988 |
| `EV:2012-llvm` | event | 基准进入测试结果页 | E14 | 2012-12 |
| `EV:unknown-emscripten` | event | Emscripten 去递归补丁 | E14 | 日期未核；`precision: unknown` |
| `ST:hilbert-all-primitive-recursive` | statement | 希尔伯特主张"所有可计算函数都原始递归" | M4 | `stance: asserts`；`claimed_in` Hilbert 1926 |
| `ST:textbook-story` | statement | 教科书叙事："希尔伯特猜想，阿克曼推翻" | M4 | `status: superseded`；简化叙事 |
| `ST:sep-correct-account` | statement | SEP 的修正叙事 | M4 | `status: current`；与上条 `contradicts` |
| `ST:ackermann-not-implementable-iteratively` | statement | "非原始递归所以不能迭代实现" | E5、E6 | `status: contested`；与下条互斥 |
| `ST:ackermann-can-be-iterated` | statement | 阿克曼函数可以迭代实现 | E7 | `status: current`；与上条 `contradicts` |
| `ST:bliss-20-percent` | statement | Bliss 消两个外层调用，收益约 20% | E18 | `stance: reports`；`claimed_in` Wichmann 1977 |
| `ST:wichmann-quality` | statement | 实现质量比语言设计开销更重要 | E5 | `about` 实现质量 |
| `TP:computability-ackermann` | teaching_point | 可计算性课程里的阿克曼函数 | M5、M6 | 常见误解："非原始递归 = 不可计算" |
| `TP:compilers-recursion` | teaching_point | 编译课程里的深递归与 TCO | E9、E18 | 常见误解："TCO 能消掉整个阿克曼递归" |

> 说明：人物与事件只列参与主要边的一部分；完整案例还要补 Sudan、Kleene、Linden、Robinson 等对应事件，按同一规则展开，不影响本轮的缺口判断。

---

## 2. 边骨架（示例，非全量）

`grade` 用 `note.md` 的核验状态折算：A = 已核原件/原文；S = 已核书目/二手研究；F = 教材/社区/课程材料；U = 未核到。`time` 只写关系成立时间，不代替事件节点。

### 2.1 分支与核心对象

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `BR-LOG-REC` | `concerns` | `CO:ackermann-function` | 1928 | A | 递归论的核心反例 |
| `BR-LOG-REC` | `concerns` | `PR:primitive-recursion-sufficiency` | 1926–1928 | S | 问题归属 |
| `BR-LOG-REC` | `concerns` | `TH:ackermann-not-primitive-recursive` | 1928 | A | 代表结果 |
| `BR-CS-TCS` | `concerns` | `CO:loop-program` | 1967 | S | LOOP 是 TCS 的对象 |
| `BR-CS-TCS` | `concerns` | `CO:ackermann-rating` | 1970 | S | 语言表达力评级 |
| `BR-CS-TCS` | `concerns` | `ME:iterative-ackermann` | 1988 | S | 算法侧 |

### 2.2 概念、记号、理论

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `CO:ackermann-function` | `depends_on` | `CO:general-recursive-function` | 1928 | S | 属于一般递归 |
| `CO:ackermann-function` | `depends_on` | `CO:primitive-recursive-function` | 1928 | S | 作为对照类 |
| `CO:loop-program` | `depends_on` | `CO:primitive-recursive-function` | 1967 | A | LOOP 的循环上界 |
| `CO:ackermann-rating` | `depends_on` | `CO:ackermann-function` | 1970 | S | 评级的标尺 |
| `CO:ackermann-rating` | `depends_on` | `CO:grzegorczyk-hierarchy` | 1979 | A | E4 与 APL |
| `CO:stack-depth` | `depends_on` | `CO:ackermann-function` | 1971 | A | 深度由函数值决定 |
| `CO:primitive-recursive-function` | `exemplifies` | `TY:hilbert-program` | 1926 | S | 有穷主义工具 |
| `NO:ackermann-phi` | `denotes` | `CO:ackermann-function` | 1928–1948 | A | 时间窗 `valid_to` |
| `NO:ackermann-A` | `denotes` | `CO:ackermann-function` | 1948–null | A | 现代记号 |
| `NO:ackermann-A` | `supersedes` | `NO:ackermann-phi` | 1948 | S | 记号更替，不是"纠错" |
| `CO:ackermann-function` | `uses_notation` | `NO:ackermann-A` | 1948 | A | |
| `NO:ackermann-rating-term` | `denotes` | `CO:ackermann-rating` | 1970 | S | 术语节点 |

### 2.3 问题与定理

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `PE:hilbert` | `poses` | `PR:primitive-recursion-sufficiency` | 1926 | S | 原始表述未核到，见 U2 |
| `TH:ackermann-not-primitive-recursive` | `resolves` | `PR:primitive-recursion-sufficiency` | 1928 | A | 否定回答 |
| `TH:ackermann-not-primitive-recursive` | `depends_on` | `CO:ackermann-function` | 1928 | A | |
| `TH:ackermann-not-primitive-recursive` | `depends_on` | `CO:primitive-recursive-function` | 1928 | A | |
| `TH:hilbert-primitive-recursion-conjecture` | `asserted_by` | `ST:hilbert-all-primitive-recursive` | 1926 | S | 猜想节点 + 主张节点 |
| `ST:hilbert-all-primitive-recursive` | `about` | `TH:hilbert-primitive-recursion-conjecture` | 1926 | S | |
| `ST:hilbert-all-primitive-recursive` | `claimed_in` | `TX:hilbert-1926` | 1926 | S | |
| `TH:loop-characterizes-primitive-recursive` | `resolves` | `PR:loop-expressiveness` | 1967 | A | |
| `TH:loop-characterizes-primitive-recursive` | `depends_on` | `CO:loop-program` | 1967 | A | |
| `TH:loop-characterizes-primitive-recursive` | `depends_on` | `CO:primitive-recursive-function` | 1967 | A | |
| `PE:meyer` | `proved` | `TH:loop-characterizes-primitive-recursive` | 1967 | S | 与 Ritchie 并列 |
| `PE:ritchie` | `proved` | `TH:loop-characterizes-primitive-recursive` | 1967 | S | |
| `TH:max-depth-equals-value-minus-one` | `depends_on` | `CO:stack-depth` | 1971 | A | 工程换算的上游 |
| `TH:iterative-ackermann-linear-space` | `depends_on` | `CO:stack-depth` | 1988 | A | O(i) 空间 |

### 2.4 评级线

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `PR:language-rating` | `depends_on` | `CO:ackermann-rating` | 1970 | S | |
| `PE:brown` | `introduced` | `CO:ackermann-rating` | 1970 | S | 评级定义 |
| `TH:ackermann-rating-apl-four` | `resolves` | `PR:language-rating` | 1979 | A | 精确结果 |
| `TH:ackermann-rating-apl-four` | `depends_on` | `CO:grzegorczyk-hierarchy` | 1979 | A | E4 |
| `TH:apl-execute-unbounded` | `depends_on` | `TH:ackermann-rating-apl-four` | 1979 | A | 加 execute 后无穷 |
| `PE:breidbart` | `proved` | `TH:ackermann-rating-apl-four` | 1979 | S | |

### 2.5 文本与见证

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `PE:ackermann` | `contributed_to` | `TX:ackermann-1928` | 1928 | A | `role: author` |
| `PE:peter` | `contributed_to` | `TX:peter-1935` | 1935 | S | |
| `PE:sundblad` | `contributed_to` | `TX:sundblad-1971` | 1971 | S | |
| `PE:wichmann` | `contributed_to` | `TX:wichmann-1977` | 1977 | S | |
| `TW:ackermann-1928.print` | `witness_of` | `TX:ackermann-1928` | 1928 | A | 印刷版 |
| `TW:ackermann-1928.print` | `supports` | `TH:ackermann-not-primitive-recursive` | 1928 | A | 正文未通读，页级定位待补 |
| `TW:sundblad-1971.pdf` | `witness_of` | `TX:sundblad-1971` | 1971 | S | 非出版方原件 |
| `TW:wichmann-1977.pdf` | `supports` | `ST:bliss-20-percent` | 1977 | S | |

### 2.6 事件

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `PE:ackermann` | `participates_in` | `EV:1928-ackermann` | 1928 | A | |
| `EV:1928-ackermann` | `part_of` | `PR:primitive-recursion-sufficiency` | 1928 | S | 事件只能挂问题 |
| `PE:wichmann` | `participates_in` | `EV:1976-wichmann` | 1976 | A | |
| `PE:wichmann` | `participates_in` | `EV:1977-wichmann` | 1977 | A | |
| `PE:grossman` | `participates_in` | `EV:1988-grossman-zeitman` | 1988 | S | |
| `EV:1976-wichmann` | `part_of` | `PR:ackermann-feasible-arguments` | 1976 | S | **无法 `part_of` CO/ME**，见 G5 |

### 2.7 观点与教学

| from | type | to | time | grade | 备注 |
|---|---|---|---|---|---|
| `CO:ackermann-function` | `asserted_by` | `ST:ackermann-not-implementable-iteratively` | 2010s | F | 社区常见说法 |
| `ST:ackermann-not-implementable-iteratively` | `about` | `CO:ackermann-function` | 2010s | F | |
| `ST:ackermann-not-implementable-iteratively` | `contradicts` | `ST:ackermann-can-be-iterated` | null | F | 对称边，`directed: false` |
| `ST:ackermann-can-be-iterated` | `about` | `CO:ackermann-function` | 1988 | A | |
| `ST:bliss-20-percent` | `claimed_in` | `TX:wichmann-1977` | 1977 | S | |
| `ST:textbook-story` | `about` | `PR:primitive-recursion-sufficiency` | 2000s | F | 教科书简化 |
| `ST:textbook-story` | `contradicts` | `ST:sep-correct-account` | null | S | |
| `TP:computability-ackermann` | `anchors` | `TH:ackermann-not-primitive-recursive` | null | — | 教学挂点只做索引 |
| `TP:compilers-recursion` | `anchors` | `PR:optimize-ackermann` | null | — | **无法 `anchors` ME**，见 G5 |

### 2.8 边族配比（示例 49 条）

| 族 | 边类型 | 条数 |
|---|---|---:|
| 问题与失败 | `targets`、`uses_method`、`corrected_by`、`reformulates`、`spawned`、`poses`、`contradicts`、`competes_with` | 4 |
| 理论体系 | `exemplifies`、`depends_on`、`generalizes`、`supersedes`、`resolves` | 19 |
| 记号文本 | `uses_notation`、`denotes`、`witness_of`、`derived_from`、`contributed_to`、`supports`、`claimed_in` | 11 |
| 归属活动 | `introduced`、`proved`、`participates_in`、`part_of`、`concerns`、`parent_of`、`cross_class`、`prerequisite_of`、`anchors`、`about`、`asserted_by` | 15 |

**没有一个 `FA:` 节点，也没有一条 `targets` / `corrected_by`。** 这不是遗漏，而是这条线的形态：它没有"某人提出错误证明、当时被接受、后来被纠正"的失败路线；它的"失败"是**猜想被反例否证**（`TH.proof_status: disproved`）和**优化不适用**（没有边类型）。这两点分别对应 G6 与 G2。

---

## 3. 五个问题逐条回答

### 3.1 问题一："这条优化路走不通"怎么表达？

这句话在这条线上其实指三种不同的事，落点完全不同。先拆开，再判。

**（a）数学不可能性。** 例："阿克曼函数写不成只含有界 `for` 的程序"——这不是观点，是可证明的否定结论：LOOP 程序恰好刻画原始递归函数（`TH:loop-characterizes-primitive-recursive`，1967），而阿克曼函数非原始递归（`TH:ackermann-not-primitive-recursive`，1928），两条 `depends_on` 一接，否定结论自动成立。**这一类落得进去，落在 `TH` + `proof_status` 上。**

**（b）历史失败。** 判定三问（`spec/object-model.md` §2）：① 有可指认的缺陷步骤或错误前提；② 有接受史或纠正史；③ 不属于"尚未证明"。本条线逐条对不上：

- `ME:explicit-stack-ackermann`（Stackermann）在 Apple IIe 上栈溢出——这是实现选择的必然后果（空间 O(A(i,n))），不是"某人以为对、其实错"，无人接受过它作为通用方案。
- `ME:tail-elimination-outer-calls`（Bliss 消两个外层调用）收益仅约 20%——这不是缺陷步骤，是结构上限；它没被"纠正"，只是不够用。

两条都不是"当时信了、后来发现错了"，缺第②问。

所以**本条线没有合格的 `FA:`**。这也解释了 §2.8 的空缺：不是漏写，是史实形态不支持。硬造 `FA:ackermann-tail-call` 会同时违反第②③问，且 `corrected_by` 无处可指（没有纠正者），`why_accepted` 也写不出来。

**（c）局部适用边界。** 例："尾调用消除只能消两个外层调用，第三分支的内层调用不在尾位置，所以救不了这个函数"。这是**部分适用**，既不是不可能性（不是"永远做不到"），也不是失败（没人主张过它能全救）。现有 31 类边里没有 `constrains` / `applies_only_when` / `limited_by`；`FA` 又不合判定。**只能塞进 `ME.complexity_note` 或边的 `note`**，图上不可查。→ **G2**。

**结论：能表达"不可能"，不能表达"部分适用/性价比边界"。** 后者恰恰是工程史最常出现的那类事实——"这条路能走，但只值这么多"。

### 3.2 问题二：工程约束该挂节点还是边？

先分三层，因为三层的落点不一样：

| 约束 | 约束的主体 | 现有落点 | 合适吗 |
|---|---|---|---|
| 朴素求值最大深度 = 函数值 − 1 | 函数自身性质 | `TH:max-depth-equals-value-minus-one`，挂 `CO:stack-depth` | 合适，是定理 |
| PDP-11/45 栈字数上限、`stack[1:1000]` 换算、60 个系统的架构差异 | 具体机器/实现 | `TX.claims` + `EV`，或硬塞 `CO:implementation-quality.claims` | 不合适，见 G1/G4 |
| APL 无 `execute` 时评级只到 4 | 语言原语的表达力 | `CO:ackermann-rating` + `TH:ackermann-rating-apl-four` + `TX` 表格 | 结论可落，主体无处落，见 G1 |

**挂节点还是挂边，判据只有一条**：约束描述的是"某个对象自身的属性"→ 节点 `claims[]`；约束描述的是"两个对象的关系在什么条件下成立"→ 边。但边信封只有 `note`、`weight`、`confidence`，**没有 `condition` / `scope` 字段**，所以关系型约束实际只能退化成边 `note`——一条不可检索的自由文本。这是 G2 的另一面。

**现有 14 类里有"系统／语言／实现"吗？没有。** 逐类排除：

- `TW`（见证）最像，但它的定义是"`TX` 的一个具体载体"，`witness_of` 强制指向一本书目实体。APL 没有对应的 `TX`，硬挂会造出假书目；LLVM test-suite 也不是"某本书的某个版本"。
- `EV` 是离散事件，不能承载"一个长期存在的系统"。
- `CO` 可以塞（本骨架就这么做的：`CO:loop-program`、`CO:implementation-quality`），但 `CO` 的判定第②问是"本身不主张真假"、第③问是"可被别的对象依赖"——把"APL"和"阿克曼函数"放同一层，等于承认任何名词都是概念，判定标准就废了。

**短期只能落在 `CO` + `claims` + `tags`**（用 `tags: ["implementation"]` 之类区分），并在 `summary` 里写明"这是语言/系统，不是数学概念"。这是硬塞，记 **G1**，不扩表。

### 3.3 问题三：Ackermann rating 的有序等级能不能表达？

**单点能，序列不能。**

能表达的：`TH:ackermann-rating-apl-four`（传统 APL 恰为 4）+ `ST`（谁在何时这么说）+ `TX:brown-1970` / `TX:breidbart-1979`。这是一条可质疑的断言，证据等级、时间、主张者都齐。

表达不了的：**等级本身作为一个有序集合**。要支持"哪些语言 ≥ 4"这种查询，需要三样东西：等级是对象（1、2、3、4、∞ 各一个）、等级有序（1 < 2 < 3 < 4 < ∞）、语言与等级之间有 `rated_as` 边。现有结构三样都没有：

- `CO` 是单个概念，不带序；把五个等级塞进一个 `CO:ackermann-rating` 的 `claims[]` 只是把序列写成了文本。
- `TH` 只能判真假，不能排序。
- 没有 `level` / `rated_as` / `ordinal` 边（**G3**、**G10**）。

**不要用多个 `ST:` 冒充等级。** `ST` 的语义是"某人主张 X"，等级不是主张；五个 `ST` 并列没有序，遍历不出大小关系，反而把"谁说"和"等级是几"混成一层。

**折中**：`CO:ackermann-rating` + `claims[]`（每条的 `statement` 写"等级 k = 第 k 层 Grzegorczyk 函数 / 第 k 个 APL 原语"）+ `TX` 里的评级表 + `text_ref` 指到 `note.md` E16。人读得懂，检索能命中，但图查询做不了。这是可接受的临时状态，前提是**承认它不可推理**。

顺带说明为什么 Grzegorczyk 层级能落而评级不能：层级是 `TY` + `TH`（有定义、有定理、有包含关系），评级是"给语言打分"，主体（语言）本身就没有类型。

### 3.4 问题四：时间落事件节点还是边上？

**判据一句话："谁在何时做了什么"→ `EV`；"某条关系从何时到何时成立"→ 边 `time`。**

按这条判据，本条线的时间几乎全是事件：

| 时间 | 事件节点 | 为什么不是边 time |
|---|---|---|
| 1928 | `EV:1928-ackermann` | 有人、有文、有收稿与刊出两个时点 |
| 1970 | `EV:1970-brown` | Brown 提出评级定义 |
| 1971 | `EV:1971-sundblad` | Sundblad 给出评级表与 F_0–F_4 闭式 |
| 1976 / 1977 | `EV:1976-wichmann` / `EV:1977-wichmann` | 两次测量，40 系统 / 60 系统 |
| 1979 | `EV:1979-breidbart` | 精确结论：传统 APL = 4 |
| 1988 | `EV:1988-grossman-zeitman` | Apple IIe 实测 |
| 2012 | `EV:2012-llvm` | 进 LLVM test-suite |

边 `time` 只用于少数"关系有效区间"：`NO:ackermann-phi --denotes--> CO:ackermann-function` 的 `valid_from 1928 / valid_to 1948`；评级 4 的有效期（1979–今）。这类没有"行为者"，只有关系存续。

**但事件侧连接不足**：`part_of` 的合法终点是 `PR/TH/TY/FA`，**不含 `CO` 和 `ME`**（§5.3 表第 26 行）。于是"1976 年 Wichmann 测了朴素递归求值"只能 `part_of` 到 `PR:ackermann-feasible-arguments`，挂不到 `ME:naive-recursive-evaluation`；而 `TP:compilers-recursion` 也不能 `anchors` 到 `ME`。结果是：**方法有了、测量有了，中间那条边没有**。→ **G5**。

> **2026-11-23 状态更新**：G5 已按批准范围修订——`part_of` 终点加 `CO`/`ME`（指向二者时 `note` 必填），`anchors` 终点加 `ME`；未新增边类型。`about` 不含 `ME`/`TX`、`uses_method` 起点不含 `CO` 两处**未动**，故"实现 → 它实现的算法"仍连不上，留待 G1 单独立项。回归结果见 [`validation.md`](validation.md) §7。

另外提醒：事件里的数值（50.4 µs、100:1、20%）不能写成 `description` 裸文本，按 §3.1 要写成 `claims[]`，每条带 `locator`。否则"这个数字从哪来"不可追。

### 3.5 问题五：缺口清单

见 §4，共 10 条，本轮只登记不扩表。

### 3.6 四个 JSON 片段（示范"填不进去"长什么样）

**片段一：猜想被反例否证——不用 `FA`，用 `TH.proof_status` + `counterexamples`**

```json
{
  "id": "TH:hilbert-primitive-recursion-conjecture",
  "type": "theorem",
  "schema_version": "0.2",
  "labels": { "zh": "所有能行可计算函数都是原始递归的（猜想）", "en": "all effectively computable functions are primitive recursive" },
  "status": "historical",
  "summary": "希尔伯特 1926 年在连续统问题语境中把原始递归当作有穷主义工具的假定；1928 年被阿克曼函数否证。",
  "statement": "每个能行可计算的数论函数都是原始递归函数。",
  "assumptions": ["能行可计算 = 有穷步骤可判定", "原始递归 = 由零、后继、投影经复合与原始递归生成"],
  "proof_status": "disproved",
  "counterexamples": [
    { "description": "阿克曼函数可计算但非原始递归", "by": "PE:ackermann", "year": 1928,
      "source": { "text": "TX:ackermann-1928", "locator": "Math. Ann. 99:118–133，正文未通读，页级待补" } }
  ],
  "claims": [
    { "id": "CLM:TH:hilbert-primitive-recursion-conjecture.1",
      "statement": "该假定出现在希尔伯特 1926 年《论无穷》中，第 185 页附近。",
      "grade": "S", "attestation": "later_report",
      "source": { "text": "TX:ackermann-1928", "locator": "脚注引 Hilbert 1926, p.185；原文未读，见 U2" },
      "note": "阿克曼自述，非希尔伯特原文；原文未核。" }
  ],
  "occurrences": [{ "year_from": 1926, "year_to": 1926, "precision": "year" }],
  "text_ref": "doc:research/ackermann-1928/note.md#M4",
  "tags": ["proof_status:disproved"],
  "provenance": { "created_by": "agent", "created_at": "2026-11-23", "updated_at": "2026-11-23", "review": "none", "sources_checked": "partial" }
}
```

要点：否证这件事完整落进去了，**但图上没有任何一条边从 `CO:ackermann-function` 连到这个 `TH`**。`counterexamples` 是字段，不是节点；想表达"阿克曼函数是这个猜想的反例"，只能靠读者看字段。→ **G6**。

**片段二：部分适用边界——只能说在 `complexity_note` 里**

```json
{
  "id": "ME:tail-elimination-outer-calls",
  "type": "method",
  "schema_version": "0.2",
  "labels": { "zh": "消去两个外层调用的递归改写", "en": "eliminating the two outer recursive calls" },
  "status": "active",
  "summary": "在 Ackermann 的第三分支里把两个外层调用改成迭代，内层调用仍保留；Bliss 优化器实测收益约 20%。",
  "kind": "computational_technique",
  "input": "Ackermann(m,n) 的递归实现",
  "output": "少两个递归调用的等价实现",
  "correctness_basis": ["CO:ackermann-function"],
  "first_use": { "by": "PE:wichmann", "year": 1977, "text": "TX:wichmann-1977", "grade": "S" },
  "applies_to": ["PR:optimize-ackermann"],
  "complexity_note": "只适用于外层两个调用；内层 A(m, n-1) 不在尾位置，尾调用消除无效。收益上限约 20%（Wichmann 1977）。此处是适用边界，不是定理，也无对应边类型。",
  "claims": [
    { "id": "CLM:ME:tail-elimination-outer-calls.1",
      "statement": "Bliss 优化器消去两个外层调用后，收益约 20%。",
      "grade": "S", "attestation": "direct",
      "source": { "text": "TX:wichmann-1977", "locator": "见 note.md E18；页级待补" } }
  ],
  "occurrences": [],
  "text_ref": "doc:research/ackermann-1928/note.md#E18",
  "tags": ["applicability-boundary"],
  "provenance": { "created_by": "agent", "created_at": "2026-11-23", "updated_at": "2026-11-23", "review": "none", "sources_checked": "partial" }
}
```

要点：`applies_to` 能说"用来解决哪个问题"，**说不出"在什么条件下失效"**。`complexity_note` 是自由文本，无等级、无来源字段、不可查询。→ **G2**。

**片段三：评级阶梯——五个等级压在一个 `CO` 的 claims 里**

```json
{
  "id": "CO:ackermann-rating",
  "type": "concept",
  "schema_version": "0.2",
  "labels": { "zh": "阿克曼评级", "en": "Ackermann rating" },
  "status": "historical",
  "summary": "给编程语言表达力分级的量表：看某语言能用有限原语实现第 k 层阿克曼函数到多大 k，等级 1–4 及无穷。",
  "definition": "若语言仅用 k 个原语即可定义 A_k 层级函数而不能定义更高层，则评级为 k；带通用解释执行原语者评级为无穷。",
  "definition_source": { "text": "TX:brown-1970", "locator": "APL Quote-Quad 2(1):35–36，原文未读，见 U10", "grade": "S" },
  "claims": [
    { "id": "CLM:CO:ackermann-rating.1", "statement": "等级 1 对应加法层（Grzegorczyk E1）。", "grade": "S", "attestation": "later_report", "source": { "text": "TX:sundblad-1971", "locator": "评级表；页级待补" } },
    { "id": "CLM:CO:ackermann-rating.2", "statement": "等级 2 对应乘法层，等级 3 对应幂，等级 4 对应迭代幂（APL 单行）。", "grade": "S", "attestation": "later_report", "source": { "text": "TX:sundblad-1971", "locator": "评级表；页级待补" } },
    { "id": "CLM:CO:ackermann-rating.3", "statement": "带 execute 的语言评级为无穷。", "grade": "A", "attestation": "direct", "source": { "text": "TX:breidbart-1979", "locator": "原文主张；卷期待补，见 U11" } }
  ],
  "occurrences": [{ "year_from": 1970, "year_to": 1979, "precision": "decade" }],
  "text_ref": "doc:research/ackermann-1928/note.md#E16",
  "tags": ["ordinal-scale-missing"],
  "provenance": { "created_by": "agent", "created_at": "2026-11-23", "updated_at": "2026-11-23", "review": "none", "sources_checked": "partial" }
}
```

要点：五级序列被压成三条文本 claim，**彼此之间没有"大于"关系**。想加"传统 APL 评级为 4"，只能再建一个 `TH` 或一条 `ST`，与"等级 4 是什么"分居两处，连不起来。→ **G3 / G10**。

**片段四：事件时间——只能挂问题，挂不到方法**

```json
{
  "id": "EV:1976-wichmann",
  "type": "event",
  "schema_version": "0.2",
  "labels": { "zh": "Wichmann 1976 年 40 系统基准", "en": "Wichmann 1976 benchmark across 40 systems" },
  "status": "active",
  "summary": "在 40 个系统上用 21 条指令的 Ackermann 基准比较实现速度，得到约 100:1 的差距。",
  "date": { "from": 1976, "to": 1976, "precision": "year" },
  "place": "英国（具体机构未核）",
  "actors": ["PE:wichmann"],
  "description": "测量对象为朴素递归实现；具体数值见 claims。",
  "part_of": ["PR:ackermann-feasible-arguments"],
  "claims": [
    { "id": "CLM:EV:1976-wichmann.1", "statement": "40 个系统之间最大与最小耗时相差约 100:1。", "grade": "S", "attestation": "direct", "source": { "text": "TX:wichmann-1976", "locator": "见 note.md E3；页级待补" } },
    { "id": "CLM:EV:1976-wichmann.2", "statement": "C 实现 50.4 µs / 26 条指令，BCPL 5.9 µs / 19 条指令 / 9 字。", "grade": "S", "attestation": "direct", "source": { "text": "TX:wichmann-1976", "locator": "抽样数据，非全表；见 U13" } }
  ],
  "occurrences": [],
  "text_ref": "doc:research/ackermann-1928/note.md#E3",
  "tags": ["measurement"],
  "provenance": { "created_by": "agent", "created_at": "2026-11-23", "updated_at": "2026-11-23", "review": "none", "sources_checked": "partial" }
}
```

要点：`part_of` 目标只有 `PR`，**不能写 `ME:naive-recursive-evaluation`**，也不能写 `CO:implementation-quality`。"测的是哪个方法""比的是哪个属性"这两条关系在图里丢失。→ **G5**。

---

## 4. 缺口清单（G1–G10，只登记，不扩表）

| # | 缺口 | 本案例中的具体证据 | 现在只能落在哪 | 为什么不合适 | 短期 workaround | 是否需扩表 |
|---|---|---|---|---|---|---|
| **G1** | 无"系统/语言/实现/版本"节点类型 | `CO:loop-program`、APL、Bliss、PDP-11/45、LLVM test-suite、Emscripten 工具链 | 硬塞 `CO`、`TW` 或 `EV` | `TW` 必须 `witness_of` 一本书目；`CO` 判定三问第②③问不成立；`EV` 不能承载长期存在的系统 | `CO` + `claims` + `tags:["implementation"]`，`summary` 注明"非数学概念" | **是**（长期）；本轮不扩 |
| **G2** | 无"约束/适用边界"边（`constrains`、`applies_only_when`） | "TCO 只能消外层、内层不在尾位置"、"Stackermann 空间 O(A) 撞墙"、"收益上限 20%" | `ME.complexity_note`、边 `note` | 自由文本，无来源、无等级、不可查询；`FA` 判定第②③问不合 | 写 `complexity_note`，并在 `note.md` 留正文 | **是**；本轮不扩 |
| **G3** | 无"有序等级/量表"对象类型 | Ackermann rating 1–4 与 ∞、Grzegorczyk E0–E4 与语言的对应 | 一个 `CO` + 多条 `claims` | 序列被压成文本，等级之间无"大于"关系，不能查询"哪些语言 ≥ 4" | `CO:ackermann-rating` + claims + `TX` 表格 | **是**；本轮不扩 |
| **G4** | 无"测量/基准结果"类型 | 50.4 µs、100:1、约 20%、60 个系统、`A(3,5)` 栈溢出 | `EV.claims` / `TX.claims` | 测量有方法、有机器、有样本量，`claims` 只能装一个数字，装不下条件 | 全部写 `EV.claims`，`locator` 细到表/页 | 暂不扩；先看是否与 G9 合并 |
| **G5** | 事件与方法/概念之间无边 | `EV → ME:naive-recursive-evaluation`、`TP:compilers-recursion → ME`、`EV → CO` | 只能 `part_of` 到 `PR`，或干脆不连 | `part_of` 终点限 `PR/TH/TY/FA`；`anchors` 限 `CO/TH/PR/NO`；`about` 不含 `ME` | 用 `PR:ackermann-feasible-arguments` 当集线器，方法侧用 `applies_to` 反向挂问题 | **已修订（2026-11-23，部分）**：`part_of` 终点加 `CO/ME`（需 `note`），`anchors` 加 `ME`；`uses_method`/`about` 未动 |
| **G6** | 无 `disproved_by` / `counterexample_to` 边 | 阿克曼函数否证希尔伯特猜想 | `TH.counterexamples` 字段 | 字段不出边，图上无法从函数连到被否证的猜想；`targets` 只能 `FA` 发出 | `counterexamples` + `claim` 文本里写明 | **是**；本轮不扩 |
| **G7** | `text_type` 无 manual / standard / commit / patch / mailing-list | Wichmann 1976/77 内部报告、Emscripten 补丁 0007、LLVM 源码、邮件列表讨论 | `TX` + `claims` 描述 | `TW` 的 `witness_kind` 无"版本控制快照"，`witness_of` 强制指向书目，commit 不是书目 | 把仓库当 `TX`（勉强），commit 当 `TW`，`locator` 写 hash | **已修订（2026-11-23）**：`text_type` 增 standard/manual/errata/release_note/source_repository/commit/mailing_list；`witness_kind` 增 web_snapshot/commit |
| **G8** | 证据等级无"机器可复现产物"口径 | 可直接 `make` 复现的 commit、测试输出 | 按 A/S/F/U 硬判 | commit 是一手可复核但非"原件"，A 与 S 的边界不清；无快照的网页渲染结果应判 U 但常被写成 A | 自定义约定：commit hash + 构建命令 = A；仅网页无快照 = U | 需在 `evidence-tags.md` 补一条说明，不是加等级 |
| **G9** | 无集合/容器类型 | "60 个系统"、"40 个系统"、"21 条指令分解" | `claims` + `text_ref` 抽样 | 集合本身是论断的支撑，抽样后"60 个系统"这句话失去可核性；逐建 60 个节点会爆 | 抽样入图，全表留 `note.md`，`text_ref` 指过去 | 暂不扩；先靠 `text_ref` |
| **G10** | 无 `rated_as` / `level_of` 关系边 | 语言 → 等级 | 无 | 即使补了等级对象（G3），没有边也连不上语言；语言本身又缺类型（G1），三者叠在一起 | 用 `ST` 描述"某语言在某年被评为 4" | **是**；与 G1、G3 同批处理 |

**归类**：G1/G3/G10 是"对象类型缺失"，G2/G5/G6 是"边类型缺失"，G4/G9 是"复合事实无处装"，G7/G8 是"文本与证据口径不匹配"。这四类里，**G5 最伤可用性**（方法无法被事件挂住），**G2 最伤表达力**（工程史的核心事实正好是"能但不值"）。

---

## 5. "要不要开计算机史"

### 5.1 与 62 分支口径是否相容

62 支的口径是"**从当代数学分支面向过去划出的区域取景轴**"，且分支判定三问里的第①问是"有相对稳定的研究对象与方法"、第③问是"能挂到 62 视图或扩展槽"。逐条对：

- **第①问：不合。** 计算机史的研究对象是机器、语言、标准、产业与工程实践，方法偏史学与工程测量，不是数学分支的研究对象与方法。它不是一个"数学分支"。
- **第②问：合。** 有明确的从业群体（编译器工程师、语言设计者）与课程位置（编译原理、体系结构）。
- **第③问：形式合，实质不合。** 能挂到扩展槽，但 62 的槽位是为"原分类漏掉的数学分支"准备的（PDE、动力系统、应用统计），不是为非数学领域准备的。

更硬的一条：本线的核心对象已经各有归属。`CO:ackermann-function` 属 `BR-LOG-REC`（递归论，`view_classes:["逻辑与基础"]`，`cross_class` 到"计算与算法" `shared_object`）；`TH:loop-characterizes-primitive-recursive` 与复杂度问题属 `BR-CS-TCS`（理论计算机科学）。**若开第 63 支，同一批对象会有三个归属**。§5.6 原先把同一对 `BR` 上的 `parent_of` 与 `cross_class` 定为互斥；v0.2（2026-11-23）已把这条降级为 **warning**——三处归属不再判结构非法，只会触发一条"归属重叠"提示，是否开第 63 支仍由人工判断。

**判定：不相容。** 不是"多加一条"，而是要改写 62 的轴定义。

### 5.2 第 63 支，还是跨分支应用视角

**建议：都不开成第 63 支。** 用两层现有机制组合：

1. **对象归属留在现有分支**：数学对象进 `BR-LOG-REC`，可计算性与复杂度进 `BR-CS-TCS`，跨类用 `cross_class` + `view_classes` 表达"同一对象被两个领域共用"。这正是 `cross_class` 的设计用途（`relation: shared_object`）。
2. **"实现中的用法"用 `proposed` 扩展槽承载**：一个不进 62 计数、`status: proposed` 的分支条目，只收"数学对象进入实现之后发生了什么"（测量、优化、放弃），不收计算机构造史、产业史、软件工程方法论。

第 2 条是**可撤回的**：若三个案例跑下来缺口不重复，删掉这条草案即可，不影响 62 与任何现有图。

**为什么这比"第 63 支"好**：第 63 支一旦进正式表，就必须有 `affected_layers`、父边、`scope_definition`，并且会被 loader 当成结构节点生成边，从此每个"实现测量"都要往里塞；而 `proposed` 槽只作取景标签，不承担结构，撤回成本低。

### 5.3 `proposed` 草案（不进正式表，不写入 `branches.json`）

```json
{
  "id": "BR-CS-PRACHIST",
  "zh": "计算实践史",
  "en": "history of computing practice",
  "view_classes": ["计算与算法"],
  "parents": [
    { "id": "BR-CS-TCS", "kind": "historical", "primary": true },
    { "id": "BR-LOG-REC", "kind": "historical" }
  ],
  "cross_class": [
    { "view": "逻辑与基础", "relation": "shared_object" },
    { "view": "应用数学", "relation": "method_source" }
  ],
  "scope_definition": "收两类事实，判据是落脚点而不是题材：（一）数学/逻辑对象进入实现之后发生的事——测量、优化尝试、适用边界、被放弃的方案、语言原语对表达力的限制；（二）算术/数值标准与实现之间的一致性事实——某实现符合或偏离某标准条款、只有特定配置下才一致、标准改版后实现如何跟进。标准文本本身是 TX，归 BR-CS-NUM 的 concerns，不进本支；本支只收标准与实现之间发生了什么。不收：计算机硬件构造史、产业与公司史、软件工程方法论、编程语言语法史本身。判据：若一条事实的落脚点是「某数学对象在某实现中的表现」或「某实现相对某标准条款的符合/偏离」，收；若落脚点是「某机器/某公司/某方法论/某标准文本自身的内容」，不收。",
  "disputes": [
    { "issue": "与 BR-CS-TCS 的边界", "resolution": "TCS 收可计算性、复杂度、形式语义的理论结果；本支只收这些结果在实现中的测量与失效", "status": "by-design" },
    { "issue": "与 BR-CS-NUM / BR-CS-COMPMATH 的边界", "resolution": "数值算法与标准文本本身归数值分析；本支只收它们在具体机器上的表现、以及实现与标准条款的一致性", "status": "open" },
    { "issue": "与 BR-CS-NUM 在 IEEE 754 上的重叠", "resolution": "754 标准文本归 BR-CS-NUM 的 concerns；x87/SSE2 与条款的符合/偏离归本支。两处可同时出现，但边不重复：一边 concerns TX，一边 concerns 实现与测量事件", "status": "open" }
  ],
  "affected_layers": { "problem": "medium", "failure": "low", "notation": "low", "text": "high" },
  "status": "proposed",
  "reason": "取景理由优先：这类事实横跨 BR-LOG-REC（对象本体）、BR-CS-TCS（形式结果）、BR-CS-NUM（数值与标准），挂在任一分支的 concerns 下都会被打散，需要一个跨三支的取景槽。次要理由是现有结构在这些事实上的失真：G7 已于 2026-11-23 修订（标准/手册/源码/提交/邮件列表已可承载），但 G1（实现无节点类型）仍开放，实现与算法、实现与标准之间的关系仍只能靠 CO 硬塞。因此本支当前只能当取景标签用，不能当结构节点用。若 G1 立项并落地，本支应降级为纯 view_classes 标签，删除 BR 节点与 parents；若 G1 不落地，保留现状。不进 62 计数，不参与 loader 结构生成。"
}
```

注意 `parents` 权重按 `branches.json` 的规则：两父为 `0.6 / 0.4`，和 = 1；`primary: true` 给 `BR-CS-TCS`。`kind` 取 `historical` 而非 `taxonomic`——本支不是"计算与算法"的分类子项，而是从两个领域的历史实践里长出来的。

**能挂哪些对象**（以本案例为例）：`EV:1976-wichmann`、`EV:1977-wichmann`、`EV:1988-grossman-zeitman`、`CO:implementation-quality`、`CO:ackermann-rating`、`PR:ackermann-feasible-arguments`、`ME:tail-elimination-outer-calls`；`concerns` 边指向它们。**不能挂**：`CO:ackermann-function` 本身（属 `BR-LOG-REC`）、`TH:loop-characterizes-primitive-recursive`（属 `BR-CS-TCS`）。这条限制是刻意的，防止吸走纯理论对象。

### 5.4 相邻分支

| 分支 | 关系 | 边界 |
|---|---|---|
| `BR-LOG-REC` 递归论 | 父（historical 0.4）+ 共享对象 | 收函数本身与不可原始递归的证明；本支收它在实现中的命运 |
| `BR-CS-TCS` 理论计算机科学 | 父（historical 0.6，primary）+ 共享对象 | 收可计算性、复杂度、LOOP/while 的形式结果；本支收测量与失效 |
| `BR-CS-NUM` 数值分析 | 相邻，易混 | 数值算法归它；"某算法在某机器上多快"归本支 |
| `BR-CS-COMPMATH` 计算数学 | 相邻，`disputes: open` | 同上，边界未定，暂不设父子 |
| `BR-LOG-MATH` 数理逻辑 | 祖父（经两个父） | 不直接相邻 |
| `BR-CS-COMPSCI` 计算科学（伞，proposed） | 平行扩展槽 | 两槽不设父子；若将来合并，须先解决 `disputes` |

### 5.5 代价（说清，不美化）

**（1）时间尺度太短，`historical` 语义勉强。** 本线 1926–2012 只有 86 年，且对象仍活跃（LLVM 里今天还在跑）。62 支的 `historical` 父边通常指跨世纪衍生；把"2012 年的一个补丁"挂成"历史"，与"从当代面向过去"的口径反了——它还没有"过去"。后果：`supersedes` 与 `failure` 几乎用不上，`affected_layers.failure` 只能给 `low`（本草案正是如此）。

**（2）文献形态与 `TX/TW` 不匹配（G7）。** 现有文本链假定"书目实体 + 版本载体 + 传承关系"。工程侧的主力材料是：手册（有版本，勉强算 `TX`+`TW`）、源码（无书目实体）、标准（有编号与版本，可算 `TX`）、邮件列表（无固定载体）、提交记录（commit 是快照，不是版本）。三样里有两样落不进去。**现有"文本链 + 见证"不够用**，只能覆盖手册与标准。

**（3）一手材料会消失或改写。** 仓库可被 force-push、分支可被删、链接会 rot。纸质原件不会。后果：`TW` 的"馆藏/编号"字段没有对应物，替代品是 commit hash——而 hash 指向的对象可能已不可达。

**（4）证据等级 S/F/U/A 的对应需要新约定（G8）。**

| 材料 | 建议等级 | 理由 |
|---|---|---|
| commit + 可复现构建命令 | `A` | 可当场复核，等价于"亲见原件"；但不能只给网页链接 |
| 只有网页渲染、无快照无 hash | `U` | 不可复核，且可能被改写 |
| 测试输出 / 基准表 | `S` | 他人可复现的当代记录，非原始文献 |
| 官方手册、标准正文 | `A`（有版本号）/ `S`（无版本） | 有版本号即可定位 |
| 邮件列表讨论 | `S` | 同时代记录，非正式发表 |
| 教材、博客、百科对工程史的叙述 | `F` | 与数学侧的 `textbook_simplification` 同性质 |

这条表**不加等级**，只是把现有四级映射到新形态，属于 `evidence-tags.md` 的补充说明，不改结构。

**（5）规模会爆（G9）。** "60 个系统"逐建节点不现实；抽样则"60 个系统"这个论断失去图上的支撑。折中是抽样入图 + 全表留文档，但这样图就不能自证。

**（6）边界吸走风险。** 一旦有"计算实践史"，数值算法的性能、密码学实现、机器学习工程都会来挂，最后与 `BR-CS-NUM`、`BR-CS-CRYPTO`、`BR-CS-COMPMATH` 大面积重叠，分支目录膨胀，62 轴被稀释。

**（7）单标注者成本。** 工程侧材料分散在论文、手册、仓库、邮件列表，检索成本远高于数学侧（数学侧有成熟书目与全集）。本案例已留下 22 条 `U`，其中工程侧占多数（U12–U20），这就是成本的样子。

### 5.6 结论

**不开第 63 支。不为阿克曼开任何新分支。** 具体三条：

1. **阿克曼函数归属不变**：`BR-LOG-REC` 为主，`BR-CS-TCS` 跨类共享。这条线不需要新分支就能表达数学侧的全部内容。
2. **工程侧用 `proposed` 扩展槽验证，不转正**：`BR-CS-PRACHIST` 草案留在本文，不写入 `branches.json`。它只在"跑案例"时充当取景标签。
3. **验证路径（决定这条草案去留的唯一依据）**：再用两个案例跑同一套 §4 清单——
   - 快速排序：算法教科书史 + 实现测量 + 尾递归/栈深度，检验 G1/G2/G4/G5 是否重复；
   - IEEE 754：标准文本 + 硬件实现 + 语言语义，检验 G7/G8 是否重复。

   若 G1/G2/G4 在两个新案例里都重现，且 workaround 无法收敛，才考虑把"实现/测量"作为字段级提案提交修订；若只在本案例出现，说明阿克曼是特例，**连 `proposed` 草案也应删除**。

**该说不的地方**：不把"计算机史"当成一个可以加进 62 的数学分支；不因为"工程侧材料很有意思"就给它一个正式分支身份；不在证据不足时先建结构再找内容。

---

## 6. 下一步

本轮只做映射与判断，未改任何 `spec/` 文件。若要继续，顺序应是：

1. **先补 G5 的临时约定**（不改结构）：在 `note.md` 的 E 段为每条测量补"对应方法 ID"，让文档侧承担图里缺的边。
2. **再跑两个验证案例**（§5.6 第 3 条），产出一份与本文同格式的缺口对照表。这是决定 `BR-CS-PRACHIST` 去留的唯一依据。
3. **最后才谈结构修订**：`system` / `measurement` / `ordinal_scale` 三个类型若确需新增，必须先有至少两个案例的重现证据，并同步改 `object-model.md`、`graph.schema.json`、`object-model.schema.json`、loader 与三个试点的校验。**本轮不做。**
4. `note.md` 的 U1–U22 不再扩写；工程侧未核项（U12–U20）若后续要补，优先补 U15（Emscripten 日期）与 U16（LLVM 引入提交），因为这两条直接决定 G7/G8 的判例。
