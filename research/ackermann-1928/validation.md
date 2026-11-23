# G1–G10 双案例验证：快速排序 / IEEE 754

- 验证对象：[`ontology.md`](ontology.md) §4 的十条缺口清单
- 判据：先定义可判定问题，再逐案例判"重现 / 部分重现 / 未重现"，三态定义见 §0
- 证据口径：沿用 `spec/evidence-tags.md`（A/S/F/U）；本文件只做结构判定，史实细节标到"已核 / 待补 / unknown"
- 纪律：不为了证明框架有问题而硬造缺口，也不为了证明没问题而回避。**未重现就写未重现。**
- 状态：已完成（§0 判据、§1 快速排序、§2 IEEE 754、§3 矩阵、§4 结论、§5 证据状态）

---

## 0. 判据：把十条缺口变成可判定的问题

判定只有三种结果，先定义清楚，免得后面各说各话：

| 结果 | 判定条件（三条同时满足） |
|---|---|
| **重现** | ① 本案例**必须**安置该对象/关系，缺了它论证不成立；② 用现有 14 类节点/31 类边只能落到错误类型或自由文本；③ 该失真**不是标注者偷懒**造成的，换个人也得这么塞 |
| **部分重现** | ① 对象/关系真实存在且必须表达；② 现有字段能无损装下内容，但装法使**图查询失效**（只能人读）；③ 或：对象存在但可通过不违背定义的方式绕开 |
| **未重现** | ① 本案例没有这类对象；或 ② 有，但现有类型能无损承载，不需要任何 workaround |

| # | 可判定问题 |
|---|---|
| G1 | 本案例是否必须安置一个真实存在的系统/语言/标准库实现，而 14 类里**没有一类**能无损承载它？ |
| G2 | 是否存在"某方法/实现**在某条件下**失效或偏离"的事实，必须作为**关系**表达，而 31 类边无一能承载？ |
| G3 | 是否存在必须**按序排列**的等级/量表（1<2<3<…）是论证的一部分？ |
| G4 | 是否存在"数值 + 机器 + 样本 + 条件"四元组构成的测量结果，必须作为**独立对象**才能被质疑？ |
| G5 | 是否存在"事件 → 方法/概念"的连接是论证必需，而现有边端点不允许？ |
| G6 | 是否存在"曾被接受、后被**另一个独立对象**（不是数值例）否证"的命题，且该反例本身是图上的主角？ |
| G7 | 是否存在至少一种一手材料，其形态在 `text_type` / `witness_kind` 枚举里**没有值可用**？ |
| G8 | 是否存在"机器可复现产物"是**核心证据**，且按现有 S/A 口径会系统性判错等级？ |
| G9 | 是否存在**不可穷举**的集合，且其规模本身是论断的一部分（不抽样就失去可核性）？ |
| G10 | 是否存在"对象 → 等级"的赋值关系是论证必需，而现有边无一能承载？ |

---

## 1. 案例 A：快速排序（实现中的算法）

选它的理由：它是"算法在真实实现里被反复改写"的典型——同一算法有 Hoare 原始版、median-of-three、introsort、dual-pivot、pdqsort 五代实现，每代都因**上一代在某类输入上退化**而出现。这正是阿克曼线里"优化—撞墙—换路"的放大版。

### 1.1 最小骨架（25 节点，边表为节选）

节点：

| ID | 类型 | 说明 | 备注 |
|---|---|---|---|
| `BR-CS-TCS` | branch | 理论计算机科学（已有） | 排序的理论侧归它 |
| `CO:quicksort` | concept | 快速排序 | |
| `CO:partition-scheme` | concept | 划分方案 | |
| `CO:pivot-selection` | concept | 枢轴选择 | |
| `CO:killer-input` | concept | 对抗性输入族 | McIlroy 1999 的构造 |
| `CO:in-place-sorting` | concept | 原地排序 | |
| `TH:quicksort-average-nlogn` | theorem | 平均 O(n log n) | |
| `TH:quicksort-worst-quadratic` | theorem | 最坏 O(n²)（首/末元素作枢轴） | |
| `TH:median-of-three-adversarial` | theorem | 存在对抗输入使 median-of-three 退化 | McIlroy 1999；**注意：这是存在性定理，不是"猜想被否证"** |
| `TH:introsort-worst-nlogn` | theorem | introsort 最坏 O(n log n) | |
| `PR:general-sorting` | problem | 通用排序问题 | 事件集线器 |
| `ME:hoare-partition` | method | Hoare 原始划分 | |
| `ME:median-of-three` | method | 三数取中 | |
| `ME:introsort` | method | 深度超限转堆排序 | |
| `ME:dual-pivot` | method | 双枢轴 | |
| `ME:pdqsort` | method | 模式击败排序 | |
| `CO:glibc-qsort` | concept（硬塞） | glibc 的 `qsort` 实现 | **G1 证据：这是库实现，不是概念** |
| `CO:go-sort-slice` | concept（硬塞） | Go `sort.Slice` | 同上 |
| `TX:hoare-1961-alg64` | text | Hoare, Algorithm 64: Quicksort, CACM 4(7):321–322 | 卷期已核，页码待复核 |
| `TX:bentley-mcilroy-1993` | text | Engineering a Sort Function, SPE 23(11):1249–1265 | 卷期已核 |
| `TX:mcilroy-1999-killer` | text | A Killer Adversary for Quicksort | 卷期待补 |
| `TX:glibc-2.39-notes` | text | glibc 2.39 release notes（qsort 改 introsort） | 网页材料，见 G7/G8 |
| `EV:1961-hoare` | event | 1961 Hoare 发表 | |
| `EV:1997-musser` | event | 1997 introsort 发表 | |
| `EV:2024-glibc-introsort` | event | 2024 glibc 2.39 换算法 | |

边（节选，均为真实连接）：

| from | type | to | 备注 |
|---|---|---|---|
| `BR-CS-TCS` | `concerns` | `CO:quicksort` | |
| `ME:hoare-partition` | `depends_on` | `CO:partition-scheme` | |
| `TH:quicksort-worst-quadratic` | `depends_on` | `CO:pivot-selection` | |
| `TH:median-of-three-adversarial` | `depends_on` | `CO:killer-input` | 定理依赖"反例对象" |
| `TH:introsort-worst-nlogn` | `depends_on` | `ME:introsort` | |
| `PR:general-sorting` | `uses_method` | `ME:hoare-partition` | |
| `PE:hoare` | `introduced` | `ME:hoare-partition` | |
| `PE:hoare` | `participates_in` | `EV:1961-hoare` | |
| `EV:1961-hoare` | `part_of` | `PR:general-sorting` | **无法 `part_of` 到 `ME:hoare-partition`**，G5 |
| `EV:2024-glibc-introsort` | `part_of` | `PR:general-sorting` | 同上；真正的对象是 `CO:glibc-qsort` |
| `CO:glibc-qsort` | `uses_method` | `ME:introsort` | **这条边其实非法**：`uses_method` 起点限 `TH/PR/FA/TY`，`CO` 不在内。即"库实现 → 它实现的算法"没有合法边，这是 G1 的下游后果 |
| `TX:glibc-2.39-notes` | `supports` | `CO:glibc-qsort` | 唯一能挂的地方 |
| `TW:glibc-2.39-notes.web` | `witness_of` | `TX:glibc-2.39-notes` | `witness_kind` 无"网页/发布说明"值，G7 |
| `TX:mcilroy-1999-killer` | `supports` | `TH:median-of-three-adversarial` | |
| `TX:bentley-mcilroy-1993` | `supports` | `CO:glibc-qsort` | 文中的实现成为后来 glibc/BSD 的基础 |

### 1.2 逐缺口判定

| # | 判定 | 证据（对象 / 想挂在哪 / 实际落在哪 / 失真） |
|---|---|---|
| **G1** | **重现** | `glibc-qsort`、`go-sort-slice`、JDK `Arrays.sort` 都是**真实存在、有版本、有 commit 的系统组件**。想挂"实现/库"类型；14 类里没有，只能建 `CO:glibc-qsort`。失真：`CO` 判定三问第②问（本身不主张真假）勉强过，第③问（可被别的对象依赖）过，但**"实现"与"概念"同层**导致 `concerns`、`depends_on` 的语义漂移——`CO:quicksort`（数学对象）和 `CO:glibc-qsort`（一段 C 代码）在查询里无法区分。`TW` 不行：它必须 `witness_of` 一个书目 `TX`，而 glibc 不是一个书目。 |
| **G2** | **部分重现** | 真实边界事实有三条：①首元素作枢轴在已排序输入上退化（这条**能落**，是 `TH:quicksort-worst-quadratic`）；②median-of-three 仍可被对抗输入击败（这条也**能落**，是存在性定理 `TH:median-of-three-adversarial`）；③introsort 的"深度阈值 2⌊log₂n⌋ + 堆排序兜底"是**工程折中**，既非定理也非失败。③只能写进 `ME.complexity_note`。判定部分重现：核心边界能用 `TH` 表达，只有"折中参数为什么取这个值"落不进去，且它本来也不该是图上的硬事实。 |
| **G3** | **未重现** | 本案例没有任何按序等级。五代实现是**演化**（`supersedes`/`variants`），不是"1<2<3"的量表。`ME.variants` 字段足够。 |
| **G4** | **部分重现** | Bentley–McIlroy 1993 有实测（不同 qsort 实现与手写排序的耗时比、元素移动次数），带机器与编译器条件。想作为独立"测量"对象以便质疑；实际只能写 `EV.claims`（每条一个数字 + locator）。失真：**同一组测量的条件（机器、编译器、输入分布）无法归组**，读者要自己从三条 claim 里拼。但本案例的论证不依赖这些数字，故不是"重现"。 |
| **G5** | **重现** | 三处必需连接缺失：①`EV:1961-hoare` → `ME:hoare-partition`（"哪年提出哪个方法"）；②`EV:1997-musser` → `ME:introsort`；③`EV:2024-glibc-introsort` → `CO:glibc-qsort`（"哪个版本换了哪个算法"）。`part_of` 终点限 `PR/TH/TY/FA`，只能全部挂到 `PR:general-sorting`，于是**五代实现的时间线在图上是同一条边指向同一个问题**，"谁取代谁"必须靠 `variants` 字段补，而 `variants` 不出边。**【已修订 2026-11-23】** 见 §7：`EV → CO/ME` 三处全部合法（① `EV:1961-hoare → ME:hoare-partition`，② `EV:1997-musser → ME:introsort`，③ `EV:2024-glibc-introsort → CO:glibc-qsort`），且 ① 另可用 `introduced`（PE→ME）表达"谁提出"，两条并存不冲突。 |
| **G6** | **未重现** | 本案例最像"否证"的是 McIlroy 的对抗输入，但它否证的不是一条曾被接受的定理，而是"median-of-three 够用"这种**工程信念**；而且反例本身是**构造**（算法），已经以 `CO:killer-input` + 存在性定理 `TH:median-of-three-adversarial` 完整表达，`depends_on` 把两者连起来了。**不需要 `disproved_by` 边**。这与阿克曼不同：那里反例是主角函数，且被否证的是一条正式猜想。 |
| **G7** | **重现** | 一手材料四种形态全部无值可用：①C 标准正文（ISO/IEC 9899 §7.22.5，`text_type` 无 `standard`）；②库源码（无书目实体）；③release notes（无 `release_note`）；④代码评审/邮件列表（无 `mailing_list`）。现在只能把 release notes 写成 `TX` + `TW:...web`，`witness_kind` 里没有对应值。失真：**"标准要求"与"某库某版本这么做"在类型上无法区分**，而这正是本案例的核心区别。**【已修订 2026-11-23】** 五类形态现均有值可用，见 §7。 |
| **G8** | **重现** | "glibc 2.39 起 qsort 改 introsort"这条事实，证据是 commit + release notes + 可 `apt source` 复核的源码。按现有口径只能判 `S`（后世叙述），但它**可当场复核**，应等价于 `A`。反过来，只有网页渲染、无 commit hash 的转述应判 `U`，现在却容易被写成 `A`。**两个方向都判错**，这是系统性偏差，不是个案。 |
| **G9** | **未重现** | 涉及的实现集合可枚举（glibc / JDK / Go / Rust / libc++，个位数），逐个建节点不会爆，也不需要"集合对象"。阿克曼线的"60 个系统"是**基准调查**这种特殊文体，本案例没有对应物。 |
| **G10** | **未重现** | 没有"对象→等级"的赋值。实现之间是 `supersedes` / `variants`，不是评级。 |

**本案例小结**：真问题三条（G1/G5/G7）+ 一条证据口径（G8）+ 两条部分（G2/G4）。G3/G6/G9/G10 未重现。

**"不扩表就必须造假"的具体位置**：`CO:glibc-qsort` 这个节点本身。它既不是概念（是一段代码），也不是文本（没有书目），也不是事件（长期存在）。把它写成 `CO` 之后，`CO:quicksort` 与它在同一类型下并存，任何"给所有 concept 做统计"的脚本都会把库实现算进数学概念。这是硬失真，不是风格问题。

---

## 2. 案例 B：IEEE 754（标准文本与实现一致性）

选它的理由：与案例 A 互补。A 的主角是**算法**，B 的主角是**规范文本**——标准的条款不是定理（标准想定什么就定什么，没有独立真假），而"某处理器是否照做"是另一类关系。这条线正好压 `TX/TW` 与"实现"两个薄弱处。

### 2.1 最小骨架（24 节点，边表为节选）

| ID | 类型 | 说明 | 备注 |
|---|---|---|---|
| `BR-CS-NUM` | branch | 数值分析（已有） | 浮点算术的历史归属 |
| `CO:floating-point-arithmetic` | concept | 浮点算术模型 | |
| `CO:binary32` / `CO:binary64` | concept | 两种二进制格式 | |
| `CO:rounding-mode` | concept | 舍入模式（就近、向上…） | |
| `CO:subnormal` | concept | 次正规数 / 渐进下溢 | |
| `CO:nan` | concept | NaN 与载荷 | |
| `CO:fma` | concept | 融合乘加 | |
| `CO:extended-precision` | concept | 扩展精度（x87 80 位） | |
| `TH:double-rounding-differs` | theorem | 先舍入到扩展精度再舍入到 binary64，可与直接舍入结果不同 | 经典结果；具体表述待核 |
| `PR:portable-floating-point` | problem | 如何让浮点结果跨机器可复现 | 事件集线器 |
| `ME:correctly-rounded-libm` | method | 正确舍入的初等函数库 | |
| `ME:softfloat` | method | 软件浮点仿真 | |
| `TX:ieee754-1985` | text | IEEE 754-1985 标准 | **`text_type` 无 `standard` 值** |
| `TX:ieee754-2008` | text | IEEE 754-2008（合并 854） | |
| `TX:ieee754-2019` | text | IEEE 754-2019 | |
| `TX:kahan-1981-why` | text | Kahan《Why do we need a floating-point arithmetic standard?》 | 未正式发表，形态特殊 |
| `TX:intel-sdm` | text | Intel SDM（x87/SSE 章节） | 厂商手册 |
| `CO:x87` | concept（硬塞） | x87 FPU 实现 | **G1 证据：这是硬件** |
| `CO:sse2` | concept（硬塞） | SSE2 实现 | 同上 |
| `CO:gcc-ffast-math` | concept（硬塞） | 编译器选项 | 同上；它不是一个概念 |
| `EV:1980-8087` | event | Intel 8087 发布 | |
| `EV:1985-754` | event | IEEE 754-1985 通过 | |
| `EV:2013-haswell-fma` | event | Haswell 引入 FMA3 | |
| `EV:2021-jep306` | event | JEP 306 恢复 always-strict 浮点 | |

边（节选）：

| from | type | to | 备注 |
|---|---|---|---|
| `BR-CS-NUM` | `concerns` | `TX:ieee754-1985` | 分支的核心文本 |
| `TX:ieee754-1985` | `supports` | `CO:rounding-mode` | 标准规定了舍入模式 |
| `TX:ieee754-2008` | `supports` | `CO:fma` | FMA 进标准 |
| `TH:double-rounding-differs` | `depends_on` | `CO:extended-precision` | |
| `TH:double-rounding-differs` | `depends_on` | `CO:binary64` | |
| `PE:kahan` | `contributed_to` | `TX:kahan-1981-why` | `role: author` |
| `PE:kahan` | `participates_in` | `EV:1985-754` | |
| `TW:ieee754-1985.print` | `witness_of` | `TX:ieee754-1985` | |
| `TW:ieee754-2019.pdf` | `witness_of` | `TX:ieee754-2019` | 付费墙，`locator` 只能写"标准号"，见 G8 |
| `CO:x87` | `depends_on` | `CO:extended-precision` | 唯一合法的连接 |
| `CO:x87` | `uses_method` | `ME:softfloat` | **非法且无意义**：`uses_method` 起点限 `TH/PR/FA/TY`；这里是为了示范"实现连不到它用的方法" |
| `EV:1980-8087` | `part_of` | `PR:portable-floating-point` | 真实对象是 `CO:x87`，挂不上，G5 |
| `EV:2013-haswell-fma` | `part_of` | `PR:portable-floating-point` | 真实对象是 `CO:fma`，G5 |
| `EV:2021-jep306` | `part_of` | `PR:portable-floating-point` | 真实对象是 `CO:extended-precision`，G5 |
| `ST:x87-more-precision-better` | `about` | `CO:extended-precision` | |
| `ST:all-implementations-conform` | `about` | `CO:floating-point-arithmetic` | **想指 `TX:ieee754-2019` 但 `about` 终点不含 `TX`**；见 G6：这条全称断言被 FTZ 等反例推翻，但反例是配置状态，不是节点 |

**尝试过但被边约束拒绝的四条**（这是案例 B 的核心发现）：

- `CO:x87 --conforms_to--> TX:ieee754-1985`：**没有 `conforms_to` 边**。
- `CO:x87 --supports--> TX:ieee754-1985`：`supports` 的起点限 `TW`/`TX`，实现节点不能"支持"标准。
- `CO:gcc-ffast-math --constrains--> CO:fma`：**没有 `constrains` 边**；写进 `CO:gcc-ffast-math` 的 `definition` 又变成"用定义装关系"。
- `ST:all-implementations-conform --about--> TX:ieee754-2019`：`about` 的终点不含 `TX`，**观点无法直接"关于某份标准"**，只能改指一个概念，指向被稀释。

### 2.2 逐缺口判定

| # | 判定 | 证据 |
|---|---|---|
| **G1** | **重现** | `x87`、`SSE2`、`RISC-V F/D`、`gcc -ffast-math` 都是真实存在的**处理器实现或工具链行为**，有版本、有手册、有 errata。只能塞 `CO`。失真比案例 A 更重：`CO:x87` 与 `CO:fma`（数学概念）同层，而 x87 的属性是"80 位扩展、8 个寄存器栈、双舍入"，这些不是定义而是**产品事实**，`CO.definition` 装不下。`TW` 更不行：x87 不是任何书的一个版本。 |
| **G2** | **部分重现** | 真实的"条件"事实：①`-ffast-math` 打开后不再保证 IEEE 语义；②`FTZ/DAZ` 置位后次正规数被清零；③只有 `MXCSR` 特定配置下才与标准一致。这些是**条件**，不是定理。现在只能写 `definition` 或 `note`。判定部分重现，但要指出：本案例真正缺的不是 `constrains`，而是 **`conforms_to`（实现↔标准）**——即使补了 `constrains`，x87 与 754 的关系仍无处写。这一条属清单外观察，不新增编号（见 §2.3）。 |
| **G3** | **未重现** | 格式族 `binary16/32/64/128` 有序（精度递增），但序可由 `generalizes` 表达（`CO:binary64 --generalizes--> CO:binary32`），`concept.generalizes` 已允许 `CO`。**不需要等级对象**。 |
| **G4** | **部分重现** | 有量化事实：某些实现的 ULP 偏差计数、一致性测试用例数（TestFloat 类）、`x87` 双舍入导致的末位差异。想作为独立测量以便质疑；实际写 `EV.claims` / `TX.claims`。但本案例的论证主体是**规范要求**，测量只是佐证，故不是"重现"。 |
| **G5** | **重现** | 三处必需连接缺失，且比案例 A 更硬：`EV:1980-8087` → `CO:x87`（"哪年出现哪个实现"）、`EV:2013-haswell-fma` → `CO:fma`（"哪个微架构加了哪条指令"）、`EV:2021-jep306` → `CO:extended-precision`（"哪个版本取消了扩展精度"）。`part_of` 只到 `PR`，三条都挂到 `PR:portable-floating-point`，于是**三个不同对象的时间线共用一条边**，图上读不出"8087 早于 754 六年"这种关系。`EV.part_of` 的注释也承认"事件只能挂问题"。**【已修订 2026-11-23】** 三条现在都合法：`EV:1980-8087 → CO:x87`、`EV:2013-haswell-fma → CO:fma`、`EV:2021-jep306 → CO:extended-precision`（均须 `note`），见 §7。 |
| **G6** | **未重现** | 最像反例的是"所有实现都符合标准"被 FTZ/DAZ 推翻，但反例是**寄存器配置状态**，不是独立对象，写在 `ST` 的 `note` 或 `claims` 里就够；`contradicts` 还能连"两派说法"。双舍入的反例是**一对具体数值**，同样不需要建节点。与阿克曼不同：那里反例是具名函数，本身是整条线的主角。 |
| **G7** | **重现（最强）** | 一手材料的四种形态全部无值：①标准正文（`text_type` 无 `standard`）；②厂商手册（无 `manual`）；③勘误表 errata（无 `errata`）；④JEP / 缺陷跟踪（无 `spec_change` / `issue`）。`TW.witness_kind` 也无"付费墙 PDF 的标准号定位"。更根本的一层：**标准的条款不是定理**——"舍入必须就近"没有独立真假，它是规范；写进 `TH` 是类型错误，写进 `TX.claims` 才对，但这样"标准要求 X"与"某人说标准要求 X"在图上无法区分。**【已修订 2026-11-23】** `standard` / `manual` / `errata` / `release_note` / `mailing_list` 等值已入枚举；`witness_kind` 增 `web_snapshot`/`commit`。但"规范条款不是定理"这一层**不在 G7 范围内，未修**（仍靠 `TX.claims`），见 §7。 |
| **G8** | **部分重现** | 标准本身：有原件 → `A`；付费墙只能看二手摘要 → `U`，现有四级**够用**，只要诚实标 `U`。测试输出 → `S` 合理。真正判不准的是"某编译器在某版本下的行为"，可复现但无"原件"，与案例 A 的 G8 同源。故部分重现。 |
| **G9** | **未重现** | 格式 8 种、标准 3 版，可枚举。符合 754 的处理器不可穷举，但论证不需要枚举——引标准即可，这与"60 个系统"的基准调查文体不同。`TX:ieee754-*` + `claims` 足够。 |
| **G10** | **未重现** | 没有"对象→等级"。一致性程度（完全/部分实现可选操作）不是有序量表，且标准 2019 已把多数可选操作转正，等级说法本身不成立。 |

**本案例小结**：真问题三条（G1/G5/G7）+ 两条部分（G2/G4/G8）。G3/G6/G9/G10 未重现。**与案例 A 的判定集合完全一致。**

### 2.3 清单外观察（不新增 G 编号，只记录）

1. **规范条款不是定理。** 标准的"必须/应当"句式没有真假，只有是否被遵守。现有 `TH` 装不下（它要求 `proof_status`），`ST` 也不对（不是"某人主张"），只能进 `TX.claims`。这不是缺口清单里任何一条，但它是 G7 的根因：文本形态不匹配，导致规范内容无处安放。
2. **实现↔标准的一致性关系缺失。** 案例 B 的中心关系是 `conforms_to` / `deviates_from`，比 G2 的 `constrains` 更基本。若只按 G2 补 `constrains`，本案例仍写不出来。此条留待字段级提案时与 G1 合并考虑（实现有了类型，才谈得上"实现符合标准"这条边）。
3. **`CO` 装不下的"产品事实"。** x87 的寄存器栈深度、8087 的微码规模，是产品属性而非定义。即使把 `CO:x87` 改成 `implementation` 类型，也需要一组新字段（厂商、版本、规格），不是换个前缀就完事。
4. **`about` 不含 `TX` / `ME`。** 观点无法直接"关于某份标准"或"关于某个方法"，只能改指概念，指向被稀释。阿克曼线里已记为 G5 的一部分（`about` 不含 `ME`），本案例补上 `TX` 这一例，说明这不是单点遗漏。

---

## 3. 三案例 × 十缺口矩阵

"阿克曼"列取自 [`ontology.md`](ontology.md) §4 的结论，两列新结论为本文件判定。

| # | 阿克曼 | 快速排序 | IEEE 754 | 交集判定 |
|---|---|---|---|---|
| G1 系统/语言/实现无类型 | 重现 | **重现** | **重现** | **真问题** |
| G2 约束/适用边界无边 | 重现 | 部分重现 | 部分重现 | 真问题（但形态不一，见 §4） |
| G3 有序等级无类型 | 重现 | 未重现 | 未重现 | 阿克曼特例 |
| G4 测量结果无类型 | 重现 | 部分重现 | 部分重现 | 非论证必需，降级 |
| G5 事件挂不到方法/概念 | 重现 | **重现** | **重现** | **真问题** |
| G6 反例无 `disproved_by` | 重现 | 未重现 | 未重现 | 阿克曼特例 |
| G7 文本形态枚举不足 | 重现 | **重现** | **重现（最强）** | **真问题** |
| G8 机器可复现产物无等级口径 | 重现 | **重现** | 部分重现 | 真问题（改文档即可） |
| G9 集合/容器无类型 | 重现 | 未重现 | 未重现 | 阿克曼特例（基准调查文体） |
| G10 对象→等级无边 | 重现 | 未重现 | 未重现 | 阿克曼特例 |

三态计数：

| 结果 | 条目 |
|---|---|
| 两案例均**重现** | G1、G5、G7（G8 在 A 为重现、B 为部分，按"至少部分"计入下一档） |
| 两案例均**至少部分重现** | G2、G4、G8 |
| 两案例均**未重现** | G3、G6、G9、G10 |

**这不是巧合。** 三条真问题对应同一个结构性事实：v0.2 是为"纸上的数学"设计的——对象是概念/定理，证据是文献与见证，事件围绕人物与文本。一旦把"实现"放进来，三处同时崩：实现没有类型（G1）、实现的时间线无处连（G5）、实现的证据不是书目（G7）。G8 是 G7 的判级版本。

---

## 4. 三句话结论

**第一句（哪些真、哪些特殊）**：G1、G5、G7 在两个案例里都重现，是真问题；G2、G4、G8 在两案例里都至少部分重现，属"可绕但失真"；G3、G6、G9、G10 只在阿克曼出现（分别是评级量表、具名函数作反例、60 系统基准调查、评级赋值），属该案例的特殊性，**不应据它们改本体**。

**第二句（动不动、动哪几条）**：值得做字段级修订，只动三处，按成本从低到高排序（**2026-11-23 已执行第 1、2 处，第 3 处留作单独立项**，见 §7）——
1. **G7（枚举扩展，最便宜）**：`text_type` 增 `standard` / `manual` / `errata` / `spec_change` / `release_note` / `source_repository`；`witness_kind` 增 `web_snapshot` / `commit`。不改任何类型，只改枚举值。
2. **G5（端点放宽，次便宜）**：`part_of` 的终点加 `CO` / `ME`（`EV → CO/ME`），`anchors` 的终点加 `ME`（`TP → ME`）。不加边类型，只改两张约束表。
3. **G1（新增类型，最贵）**：新增 `implementation` 节点类型（硬件/库/工具链/运行时），配两条边 `implements`（实现 → 标准文本或算法）与 `conforms_to`（实现 → 标准）。这一条要动 schema、loader、校验脚本和三份试点，必须单独立项，不能顺手改。

**暂不改的三条**：G2 不单独补 `constrains`——案例 B 证明真正的需求是 `conforms_to`，已并入第 3 条；G2 剩下那点"折中参数为什么取这个值"本来就该留在 `complexity_note`。G4 不建测量类型——两个案例都显示数字装进 `claims` 就够，测量不是论证主体。G8 只改 `evidence-tags.md`（加一句"可复现构建产物按 A 处理，须给 commit hash 与构建命令；仅网页无快照按 U"），不动 schema。

**第三句（`BR-CS-PRACHIST` 去留）**：**保留为 `proposed`，`scope_definition` 与 `reason` 已按此修改（2026-11-23，见 [`ontology.md`](ontology.md) §5.3）**——`scope` 已补"算术/数值标准的文本与实现一致性"（否则 IEEE 754 挂不进去），`reason` 已改以"跨分支取景"为首要理由，不再以"实现对象无处落"为主；降级条件写为：**若第 3 条（G1）落地，本支降为纯 `view_classes` 取景标签**，不建 `BR` 节点、不生成结构边。理由是它的存在依据从"无处安放"变成"跨分支取景"，前者可以靠字段解决，后者不值得一条正式分支。

---

## 5. 证据状态与 unknown

本文件只做结构判定，史实以"够支撑映射"为准。凡是会影响判定成立的，列在这里：

| 项 | 状态 | 影响 |
|---|---|---|
| Hoare 1961, Algorithm 64, CACM 4(7):321–322 | 卷期已核，页码待复核（S） | 不影响 G1/G5/G7 |
| Hoare 1962, Quicksort, Computer J. 5(1):10–16 | 未核原件（S） | 同上 |
| Bentley & McIlroy 1993, SPE 23(11):1249–1265 | 卷期已核，正文未读（S） | G4 的测量细节待补 |
| Musser 1997, introsort, SPE 27(8):983–993 | 卷期待复核（S） | 不影响结论 |
| McIlroy 1999, A Killer Adversary for Quicksort | 卷期待补（S） | G6 判"未重现"依赖"反例是构造而非具名对象"，此判断不依赖卷期 |
| glibc 2.39 release notes（qsort 改 introsort） | 网页已见，未固定 commit hash（S） | G7/G8 的直接证据；正式引用前须补 hash |
| IEEE 754-1985 通过年份 | 1985 年，未核原件（S） | 不影响结论 |
| IEEE 754-2008 / 2019 出版年月 | 未核（S，月份待补） | 不影响结论 |
| Intel 8087 发布年份 1980 | 未核（S） | 不影响结论 |
| JEP 306 / Java 17 | 未核（S） | 不影响结论 |
| 双舍入定理的精确表述 | 未核（U） | 只用作"存在此类定理"的例子，具体条件未写进骨架 |
| x87 寄存器栈深度、8087 微码规模 | 未核（U） | 只用于说明"产品事实"性质，未给数值 |

**明确不写的东西**：不给任何未核的版本号、性能数字、页码。文中出现的卷期只用于标识文献，其核验状态已在上表注明；凡标"待补"的，正文只保留对象名与关系。

---

## 6. 本轮边界

- **2026-11-23 之后**：G7、G5 已在 `spec/` 落地（见 §7），本文件 §1–§4 保留修订前判定与理由，作为证据；改动处已就地标注。未写入 `branches.json`；两个骨架仍是本文件内的表，不是可校验的 `graph.json`。
- 与 [`ontology.md`](ontology.md) 的关系：那份是单案例映射与缺口登记；本文件是三案例对照与"改不改"的决定依据。
- 若批准修订，下一步是按 §4 第二句的 1→2→3 顺序做，每一步都要同步 `object-model.md`、`graph.schema.json`、`object-model.schema.json`、loader 与三个试点校验；本轮不做。

---

## 7. 2026-11-23 修订落地（G7 + G5）

按批准范围只做前两处；第 3 处（`implementation` 类型 + `implements`/`conforms_to`）未动。

### 7.1 改了哪些文件

| 文件 | 改动 |
|---|---|
| `spec/object-model.md` | §4.10 `text_type` / `witness_kind` 枚举与口径说明；§4.11 `event.part_of` 取值；§4.12 `teaching_point.history_objects` 加 `ME:`；§5.1 表第 26/30 行；§5.6 表第 26/30 行；不变量新增第 13 条（`part_of` 落点收窄 + `note` 必填）；§5.6 C 反例补两条 |
| `spec/framework/object-model.schema.json` | 顶层 `properties` 新增 `text_type`、`witness_kind` 两个 enum（原先只有字段描述、无枚举） |
| `spec/framework/graph.schema.json` | 边 `allOf` 新增条件：`type=part_of` 且 `to` 匹配 `^(CO\|ME):` 时强制 `note` 非空。未新增边类型，`type` 枚举未变 |
| `research/ackermann-1928/validation.md` | G5/G7 判定行就地标注已修订；§4 第二、三句改为"已执行"；本 §7 |
| `research/ackermann-1928/ontology.md` | G5/G7 缺口行标注已修订；§3.4 状态更新；§5.3 `BR-CS-PRACHIST` 的 `scope_definition` / `disputes` / `reason` 按上轮结论改写 |

**未改**：`branches.json`（正式表）、任何 `graph.json` 样例与试点内容、`evidence-tags.md`（G8 本轮未动）、`tools/`。

**枚举最终值**：

- `text_type`（16）：原有 5 + 样例在用 3（`article`/`letter`/`treatise`，原说明漏列，本次补入）+ 新增 8（`standard`/`manual`/`errata`/`release_note`/`spec_change`/`source_repository`/`commit`/`mailing_list`）。旧值一个未废。
- `witness_kind`（11）：原有 7 + 样例在用 2（`manuscript`/`printed_edition`）+ 新增 2（`web_snapshot`/`commit`）。

### 7.2 校验结果

**说明**：仓库内**没有** `check_graphs.py` 或等价校验器（`Grep`/`Glob`/`git log --all` 均未找到；此前"0 错误"是会话内临时检查）。本轮用临时脚本 `%TEMP%\mgcheck.mjs` 按 `object-model.md` §4 必填字段、§5.6 端点表与不变量逐条实现，分为"结构 + schema-lite"与"strict（完整 per-type 必填）"两档；脚本未入库。

| 对象 | 节点/边 | 结构 + schema-lite | strict（完整字段） |
|---|---|---|---|
| `samples/non-euclidean-geometry.json` | 63 / 94 | **0** | 0 |
| `samples/group-theory.json` | 13 / 15 | **0** | 1（既存：`EV` 缺 `date`） |
| `pilots/calculus/graph.json` | 58 / 102 | **0** | 129（既存：`branch.scope_definition` 等字段缺） |
| `pilots/group-theory/graph.json` | 51 / 80 | 1（既存） | 8（既存） |

- 要求通过的 `samples/`（两个）与 `pilots/calculus/`：**结构 + schema-lite 全部 0 错误**。
- `pilots/group-theory/` 的 1 条 lite 错误是既存问题：`E:TW:cayley-1854.print>witness_of>TX:cayley-1854` 的 `attestation: later_report` 配 `grade: A`，违反 §5.2 等级上限。**与本轮改动无关，未改样例。**
- strict 的 138 条全部是"节点缺 §4 必填字段"，与本轮枚举/端点无关：对 strict 输出过滤 `text_type|witness_kind|not allowed|needs note|cycle|weight`，命中 **0** 条。说明**没有引入新的 schema 违规**；同时也说明现有试点从未通过完整 schema，只通过 lite——这是既存欠账，本轮按"不改样例"的要求不动它。

### 7.3 回归测试（修订前 vs 修订后）

测试图：11 个节点、6 条边，逐条对应 `validation.md` §1.1 / §2.1 里被拒的连法。

| # | 连法 | 修订前 | 修订后 |
|---|---|---|---|
| 1 | `EV:2024-glibc-introsort —part_of→ CO:glibc-qsort` | 拒：`to type concept not allowed` | **通过**（`note` 必填） |
| 2 | `EV:1980-8087 —part_of→ CO:x87` | 拒：同上 | **通过** |
| 3 | `EV:2013-haswell-fma —part_of→ CO:fma` | 拒：同上 | **通过** |
| 4 | `TP:compilers-recursion —anchors→ ME:tail-elimination-outer-calls` | 拒：`to type method not allowed` | **通过** |
| 5 | `EV:1928-ackermann —part_of→ CO:ackermann-function` | 拒：同上 | **通过** |
| 6 | `CO:glibc-qsort —uses_method→ ME:introsort` | 拒：`from type concept not allowed` | **仍拒**（本轮未放开 `uses_method` 起点） |

总计：修订前 6 错，修订后 1 错。另验：第 1 条去掉 `note` 后仍被拒（`part_of->concept needs note`），说明新增条件确实在拦。

**必须说明的偏差**：上一轮把"`glibc-qsort --uses_method--> introsort` 应该通过"写进了预期，但 G5 只放宽 `part_of`/`anchors`，`uses_method` 的起点仍是 `TH/PR/FA/TY`。要让"实现→它实现的算法"合法，需要 `implementation` 类型（第 3 处，已批准暂缓）。本轮不把它偷偷塞进 `uses_method`，因为那会让 `CO:quicksort`（概念）也能 `uses_method`，等于绕开类型问题、制造新的错误连法。等价的合法表达是 `EV:版本事件 —part_of→ CO:实现`，回归第 1 条已覆盖。

### 7.4 放宽后的副作用检查

`part_of` 从 4 个终点扩到 6 个，`anchors` 从 4 个扩到 5 个。逐条查"原本被这两条约束挡住的错误连法"：

| 原本被挡、现在合法的写法 | 是否真错误 | 处理 |
|---|---|---|
| `EV —part_of→ CO/ME`，但事件其实应挂某问题/定理 | 可能错（粒度放错） | 不变量 13 要求 `note` 写明理由；机械校验无法判语义，只能人工复核。已在 §5.6 B13 写明"挡不住这一类" |
| `EV —part_of→ CO` 当作"事件属于概念" | 多数场合是真错误（类别错） | 同上；`note` 会暴露写法。若某分支出现滥用，可在该分支自查里加"CO/ME 落点不得超过 EV 总数 X%"的软阈值，但不入本体 |
| `TP —anchors→ ME` | **不是错误** | 教学挂点本就该能挂到算法；不变量 12 仍禁止 `TP` 参与 `supports`/`depends_on`/`part_of`，索引性质未变 |
| `EV —part_of→ CO` 用于"测量属于某实现" | **不是错误**，正是本次目的 | — |

**结论**：放宽只让一类错误变合法（事件粒度放错），且这类错误本来就无法用端点表判定，只能靠 `note` + 人工；因此用"`note` 必填"补上机械可查的那一半，剩下的一半留在 B13 明说。`anchors` 的放宽没有产生新的错误类。

### 7.5 G5/G7 状态

- **G7：关闭。** 两个案例需要的五种材料形态均有值可用；"规范条款不是定理"这一层不在 G7 定义内，仍按 `TX.claims` 处理，记为清单外观察（§2.3 第 1 条），不另立缺口。
- **G5：部分关闭。** `EV → CO/ME` 与 `TP → ME` 已通；`about` 不含 `ME`/`TX`、`uses_method` 不含 `CO` 仍未动。前者不影响本轮两个案例的骨架（观点可指向概念），后者要等 `implementation` 类型。缺口行相应改为"部分修订"。
- 其余 G1/G2/G3/G4/G6/G8/G9/G10 状态不变。

