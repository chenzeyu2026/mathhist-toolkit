# 阿克曼函数：史实与时间线

- 任务段：第一段（史实与时间线）。本体映射、缺口清单、分支判断不在本文件，留到下一段。
- 日期：2026-11-23
- 检索：最初设 15 次 WebSearch 上限，后由委托方撤回；改为按需补检，优先读原件/全文。实际检索记录见 §6。写作按"断点续写"执行，每节完成即落盘。
- 结论先行：
  1. 数学侧，它不是"希尔伯特猜想所有可计算函数都原始递归、然后被阿克曼一举推翻"这么简单。希尔伯特 1926 年在连续统问题的语境里已经描述了这类函数，并把证明归给阿克曼；阿克曼 1928 年给出精确证明；佩特 1935 年把它改成二元形式；罗宾逊 1948 年简化初始条件。教科书叙事是一层简化。
  2. 工程侧，没有一条成体系的"阿克曼函数工程史"。实际证据散落在五类材料里：过程调用基准（Sundblad、Wichmann）、语言表达力评级（Brown、Linden、Breidbart）、递归消除与优化（Meyer–Ritchie、Grossman–Zeitman、Liu–Stoller、Wichmann 记录的 Bliss）、部分求值（Jones）、编译器测试套件与补丁（LLVM、Emscripten、Cornell）。没有找到编译器工程师集体讨论它的会议记录、邮件列表或内部报告。

## 0. 核验状态图例

| 标记 | 含义 |
|---|---|
| 【原文】 | 已读该文献的全文或相关节原文（PDF / 扫描 / 网页正文） |
| 【书目】 | 只核到题名、作者、卷期、页码、DOI 等书目信息，未读正文 |
| 【摘要】 | 已读出版方摘要或原文片段，未读全文 |
| 【二手】 | 仅通过他人转述、综述、百科或教科书了解，未接触原文献 |
| 【分析】 | 本文按定义或结构做的推理，不是文献史实 |
| 【未核到】 | 检索后没有找到可靠来源 |

---

## 1. 时间线

| 年份 | 事件 | 类别 | 来源 | 核验状态 |
|---|---|---|---|---|
| 1925 / 1926 | 希尔伯特在明斯特讲演《论无穷》（1926 年发表）。他引入后来被称为阿克曼函数的层级，指出以 n 为变量的函数不能由通常递归定义，并把证明归给阿克曼。 | 数学 | Hilbert 1926, *Math. Ann.* 95:161–190；SEP 附录 | 【二手】SEP / Grossman–Zeitman 转述；原文未读 |
| 1927 | 苏丹（Gabriel Sudan）发表另一个非原始递归的可计算函数，与阿克曼的工作独立而同时。 | 数学 | Sudan 1927, *Bull. Math. Soc. Roumaine Sci.* 30:11–30；Calude–Marcus–Tevy 1979 | 史学论文【原文】；苏丹原文未读 |
| 1928 | 阿克曼发表《Zum Hilbertschen Aufbau der reellen Zahlen》（论希尔伯特实数构造），给出 φ(x,y,z) 及同时递归版本，证明 φ(x,x,x) 不是原始递归。原文 1927-01-20 收稿，1928 年 12 月号刊出。文中脚注自述：这个函数"已见于希尔伯特《论无穷》，见该书第 185 页"；另一脚注提到苏丹即将发表的同类工作。 | 数学 | Ackermann 1928, *Math. Ann.* 99:118–133, DOI 10.1007/BF01459088 | 【书目+原文脚注】Springer 页面核到题名、收稿/刊出日期与脚注原文；正文未通读 |
| 1935 | 佩特（Rózsa Péter）发表《Konstruktion nichtrekursiver Funktionen》，把构造简化为二元嵌套递归。今天通常所称"阿克曼函数"多指这一形式。同年她还有一篇《Über den Zusammenhang der verschiedenen Begriffe der rekursiven Funktion》（*Math. Ann.* 110:612–632），两篇不要混。 | 数学 | Péter 1935, *Math. Ann.* 111:42–60；Péter 1935, *Math. Ann.* 110:612–632 | 【书目】两篇题名与卷页已核；正文未读 |
| 1937 | 佩特研究多重递归。 | 数学 | Péter 1937（据 SEP 附录） | 【二手】原文未读 |
| 1948 | 罗宾逊（Raphael M. Robinson）简化初始条件，得到今天常见的三行定义。 | 数学 | Robinson 1948, *Bull. Amer. Math. Soc.* 54:987–993, DOI 10.1090/S0002-9904-1948-09121-2 | 【二手】NIST / Grossman–Zeitman；原文未读 |
| 1952 | 克莱尼《元数学导论》把该问题表述为"希尔伯特 1926 年关于连续统问题的猜想"，并说它由阿克曼 1928 年回答。 | 数学 | Kleene 1952, *Introduction to Metamathematics*（PDF 片段） | 【二手】片段；页码未核 |
| 1956 | 佩特给出判定一个递归函数是否原始递归的条件。 | 数学 | Péter 1956（据 SEP 附录） | 【二手】原文未读 |
| 1967 | Meyer 与 Ritchie 发表《循环程序的复杂性》，证明 LOOP 程序类恰好刻画原始递归函数（原文定理 7）。 | 工程 / 理论 | Meyer–Ritchie 1967, *Proc. ACM 22nd Natl Conf.*, 465–469, DOI 10.1145/800196.806014 | 【原文片段】定理 7；全文未通读 |
| 1970 | J. A. Brown 在 *APL Quote-Quad* 2(1)（1970 年 4 月）提出"用阿克曼函数给编程语言评级"：Ackermann rating 是最大的 j，使得该语言存在一个封闭、非递归的表达式能写出第 j 层函数（记作 j A n）。 | 工程 / 理论 | Brown 1970, "Using the Ackermann Function to Rate Programming Languages", *APL Quote-Quad* 2(1):35–36；转引自 Breidbart 1979 与 Sundblad 1971 参考文献 | 【书目】经两条独立引文核到卷期页码；原文未读 |
| 1970 | Sundblad 报告 NA70.18：用阿克曼函数测试 ALGOL / PL/I / SYMBAL 的递归过程实现与公式操作。 | 工程 | Sundblad 1970, Report NA70.18, Royal Institute of Technology, Stockholm | 【书目】据 1971 论文参考文献 |
| 1971 | Sundblad 在 BIT 发表《The Ackermann function. A theoretical, computational, and formula manipulative study》：ALGOL 60、ALGOL W、PL/I、SIMULA 67 在 IBM 360/75 与 CDC 6600 上的调用次数、最大递归深度与计时；给出 F_0–F_4 的闭式、调用次数 C_m(n)、"最大深度 = 函数值 − 1"，并讨论 Ackermann rating。 | 工程 | Sundblad 1971, *BIT* 11(1), DOI 10.1007/BF01935330 | 【原文】PDF 全文 |
| 1971 | T. A. Linden 发表《The Ackermann Function in APL》，接过 Brown 的评级想法，主张支持 execute 的 APL 评级为无穷。 | 工程 / 理论 | Linden 1971, *APL Quote-Quad*（亦见 *SIGPLAN Notices* 6(4):34–35, 1971） | 【原文片段】PDF 首段；两种引文卷页不一致，见 §4 |
| 1975 | Tarjan 用反阿克曼函数分析并查集复杂度，阿克曼的"反向"进入算法分析。 | 工程 / 算法 | Tarjan 1975, *J. ACM* 22:215–225（据 Grossman–Zeitman 参考文献） | 【书目】 |
| 1976 | Wichmann 用六行递归过程测 40 个系统的过程调用效率，报告 100:1 的性能差异、每次调用的指令数与栈字数。 | 工程 | Wichmann 1976, *BIT* 16(1):103–110, DOI 10.1007/BF01940783 | 【原文】作者版 PDF |
| 1977 | Wichmann 扩大并反思该测试：60 个系统、六种体系结构（IBM 360/370、ICL 1900、PDP-11、DEC-10、Burroughs 栈机、CDC Cyber）；结论"实现质量比语言设计带来的开销更重要"；Bliss 优化器用跳转消掉两个外层调用的递归，收益约 20%；并指出测试栈用量不典型。 | 工程 | Wichmann 1977, *Software: Practice and Experience* 7(3):317–329, DOI 10.1002/spe.4380070303 | 【原文】PDF 全文 |
| 1979 | Breidbart 发表《APL and the Grzegorczyk Hierarchy》：APL 单行函数（仅算术）恰好算 E4；不带 execute 的 APL 的 Ackermann rating 恰为 4，带 execute 则为无穷。 | 工程 / 理论 | Breidbart 1979, *APL Quote-Quad* 9(4):271–273（ACM 1979） | 【原文】PDF 全文 |
| 1988 | Grossman 与 Zeitman 给出迭代算法：O(i) 空间、O(i·A(i,n)) 时间；报告 Apple IIe 上递归版栈溢出。 | 工程 | Grossman–Zeitman 1988, *Theoret. Comput. Sci.* 57(2–3):327–330, DOI 10.1016/0304-3975(88)90046-1 | 【原文】出版版 PDF；收稿日期未核 |
| 1993 | Jones、Gomard、Sestoft 的《部分求值与自动程序生成》以阿克曼函数为示例。 | 工程 | Jones–Gomard–Sestoft 1993, *Partial Evaluation and Automatic Program Generation*, Prentice Hall | 【摘要】示例片段；书未通读 |
| 1996 | Jones 在《ACM Computing Surveys》综述中称阿克曼函数"对实际计算无用，却是说明程序点特化的绝佳载体"。 | 工程 | Jones 1996, *ACM Comput. Surv.* 28(3):480– | 【原文】相关节；止页未核 |
| 2000 | Liu 与 Stoller 系统讨论"从递归到迭代"的优化，以增量化作为统一方法。 | 工程 | Liu–Stoller 2000, PEPM'00, DOI 10.1145/328690.328700 | 【摘要】摘要；页码未核 |
| 2003 | Liu 与 Stoller 用增量化导出优化版阿克曼函数：O(i) 空间、O(A(i,n)) 时间。 | 工程 | Liu–Stoller 2003, *SIGPLAN Notices* 38(10):85–91, DOI 10.1145/966049.777398 | 【原文】出版版 PDF |
| 2012 | LLVM test-suite 的 `Shootout-C++/ackermann` 基准出现在测试结果页；`SMALL_PROBLEM_SIZE` 参考输出 `Ack(3,11): 16381`，默认参数输出 `Ack(3,12): 32765`。 | 工程 | LLVM testresults 2012-12；LLVM test-suite 源码 `ackermann.cpp` | 【原文】仓库文件 / 结果页 |
| 年份未核 | Emscripten 补丁 0007 标题为 "ackermann-remove-recursion-to-avoid-stack-overflow"，把基准中的递归整体改成显式栈迭代，提交信息写 "We were overflowing the trusted stack: 'Fix' by removing recursion."。 | 工程 | emscripten-releases, `patches/llvm-test-suite/0007-...patch` | 【原文】补丁正文；原始提交日期【未核到】 |

---

## 2. 数学侧事实

**M1. 1928 年的语境是希尔伯特纲领与连续统问题，不是"造一个大数函数"。**
斯坦福哲学百科（SEP）的专节说得很直接：希尔伯特在 1926 年《论无穷》里已经引入后来被称为"阿克曼函数"的东西，背景是他试图证明连续统假设（CH）；希尔伯特把原始递归视为有穷主义可接受的方法，而这类以 n 为变量的函数不能用通常的原始递归定义。阿克曼 1928 年的论文题为《论希尔伯特实数构造》，是在这个纲领内部回答"希尔伯特式构造能走多远"。
- 来源：SEP, "History of the Ackermann and Péter functions"（附录）；Hilbert 1926, *Math. Ann.* 95:161–190。
- 状态：【二手】SEP 全文；Hilbert 原文未读。

**M2. 希尔伯特先描述了函数，阿克曼给出了精确证明。**
Grossman–Zeitman 1988 原文写道：希尔伯特在阿克曼发表证明前两年就描述了这个函数，并把证明归给阿克曼；他们半开玩笑地说，"也许它也应当冠上希尔伯特的名字"。
- 来源：Grossman–Zeitman 1988, TCS 57:327–330，正文历史注记。
- 状态：【原文】。

**M3. 阿克曼 1928 年的技术路线是"高阶递归 + 同时递归 + 支配论证"。**
按 SEP 的转述：阿克曼先定义 φ(x,y,z)，其中 z 是索引变量，用高阶递归 ρ_z 定义；再给出一个用同时递归（simultaneous recursion）得到同一扩张的版本；最后证明 φ(x,x,x) 不是原始递归。证明的关键是构造一个支配所有原始递归函数的函数，再用对角线式论证排除原始递归性。
- 来源：SEP 附录；Ackermann 1928。
- 状态：【二手】SEP 全文；原文未读。

**M4. "希尔伯特猜想所有可计算函数都原始递归，阿克曼推翻了它"是教科书简化。**
SEP 明确说，教科书式的讲法"有时暗示这些函数一被提出就是'直观可计算但非原始递归'的例子"，这种理解忽略了 Ackermann 1928 与 Péter 1935 的具体语境，以及它们所引发的各种递归形式的研究。更准确的说法是：希尔伯特在连续统问题的构造中已经碰到这类函数；阿克曼给出了"它不是原始递归"的精确证明；佩特随后把它整理成更标准的二元形式。
- 来源：SEP 附录开篇。
- 状态：【二手】SEP 全文。这条是史学修正，不是一手史料。

**M5. 它在这条线上的位置：原始递归 ⊂ 一般递归，阿克曼函数在全可计算但非原始递归的那一格。**
原始递归函数由零函数、后继函数、投影，经复合与原始递归模式生成；一般递归（µ-递归）再加入无界最小化。阿克曼函数是全可计算的（对每个 m,n 都有值），但不是原始递归；它增长得比任何原始递归函数都快，因此常被用作"原始递归不够用"的标准反例。
- 来源：SEP；MathWorld "Ackermann Function"；Grossman–Zeitman 1988 引言。
- 状态：【二手】多源一致；数学陈述可按定义核验。

**M6. LOOP 程序 = 原始递归函数，所以阿克曼函数不能由有界 for 循环程序计算。**
Meyer 与 Ritchie 1967 年的《循环程序的复杂性》证明：只用有界循环（循环次数在进入前确定）的 LOOP 程序，其可计算函数类恰好是原始递归函数类。阿克曼函数不是原始递归，因此不存在一个 LOOP 程序对一切 m,n 计算它。这条结论是工程侧"不能把递归改写成 for 循环"的理论根据。
- 来源：Meyer–Ritchie 1967, Proc. ACM 22nd Natl Conf., 465–469；CHM 博客对 Ritchie 博士论文的说明；UTEP 课程讲义 "Not All Computable Functions Are Primitive Recursive"。
- 状态：【原文片段】定理 7 原话；"LOOP = 原始递归"的完整证明未通读。

**M7. 佩特 1935 年的二元形式成为标准；1937 年研究多重递归；1956 年给出原始递归性判定条件。**
佩特把阿克曼的构造简化为二元嵌套递归 π(x,y)：π(0,n)=n+1；π(m+1,0)=π(m,1)；π(m+1,n+1)=π(m,π(m+1,n))。今天教科书里的"阿克曼函数"通常指这一形式（或罗宾逊 1948 年的等价变体）。她后来还研究多重递归，并在 1956 年给出判定条件。
- 来源：SEP 附录；NIST DADS "Ackermann's function"；Péter 1935, *Math. Ann.* 111:42–60。
- 状态：【二手】三源一致；原文未读。

**M8. 罗宾逊 1948 年简化初始条件，形成今天最常见的三行定义。**
Grossman–Zeitman 说：据他们所知，标准定义最早由 Raphael Robinson 在阿克曼论文二十年后使用；佩特在阿克曼之后七年已有几乎相同的函数；希尔伯特更早描述过它。罗宾逊的贡献主要是把初始条件整理成今天教科书里的形式。
- 来源：Grossman–Zeitman 1988 历史注记；NIST DADS；Robinson 1948, *Bull. AMS* 54:987–993。
- 状态：【原文】Grossman–Zeitman；Robinson 原文未读。

**M9. 名字：Ackermann function / Ackermann–Péter function；反阿克曼是另一件事。**
NIST 与多数教科书把二元形式称为 "Ackermann's function"，也有文献称 "Ackermann–Péter function"。算法分析里的反阿克曼函数 α(n) 是它的某种反函数，用于并查集等近乎线性复杂度的界；它不是"阿克曼函数算不出来"的意思。
- 来源：NIST DADS；Grossman–Zeitman 1988（提到 Tarjan 1975 的并查集用法）；Tarjan 1975, *J. ACM* 22:215–225。
- 状态：【书目】/【二手】。

**M10. 苏丹 1927 年独立发现了同类例子，阿克曼当时已知情。**
Calude、Marcus、Tevy 1979 年在 *Historia Mathematica* 的论文论证：最早的非原始递归可计算函数例子由阿克曼 1928 与苏丹 1927 同时发现；苏丹知道阿克曼的想法（通过希尔伯特 1926 的描述），阿克曼在 1928 论文中也提到苏丹即将发表的工作。因此"第一个例子"的归属是双人的，不是阿克曼独占。
- 来源：Calude–Marcus–Tevy 1979, *Historia Mathematica* 6:380–384；Sudan 1927, *Bull. Math. Soc. Roumaine Sci.* 30:11–30。
- 状态：史学论文【原文】；苏丹原文未读。

**M11. "阿克曼函数不可计算"是误读。**
它是全可计算的；不可原始递归不等于不可计算。真正"不可计算"的是停机问题那类函数。工程语境里把"不是原始递归"误说成"不能实现/不可计算"，是后面 E6 要处理的混淆。
- 来源：SEP；NIST；本文分析。
- 状态：【分析】+ 多源。

---

## 3. 工程侧事实

> 先给结论：**没有一条成体系的"阿克曼函数工程史"**。找不到编译器团队或语言实现者集体讨论它的会议记录、邮件列表、内部设计文档。实际能找到的是五类零散材料：（a）1970 年代的过程调用基准；（b）用它给语言表达力评级的文献；（c）递归消除与优化；（d）部分求值；（e）现代编译器测试套件里的一条基准与若干补丁。下面逐条列证据，再把"哪些常见说法站不住"分开写。

**E1. 它进入工程语境的身份是"短小、深递归、可跨语言移植"的测试载体，不是"不可计算的怪物"。**
1970 年代前后，过程调用的实现开销（参数传递、栈帧、返回地址、寄存器保存）是语言实现比较的热点。阿克曼函数满足三个条件：代码只有几行；递归深度随参数指数增长，能压出栈实现的问题；定义在各语言间几乎逐字可移植。Wichmann 1976 的测试程序就是一个六行的递归过程。因此它被当作"过程调用开销的探针"，而不是被当作数学奇观。
- 来源：Wichmann 1976, *BIT* 16(1):103–110；Sundblad 1971, *BIT* 11(1)。
- 状态：【原文】Wichmann 1976 作者版 PDF；Sundblad 1971 PDF 全文。

**E2. Sundblad 1971：把阿克曼函数同时用作"理论对象 + 实现测试 + 符号计算练习"的一篇关键文献。**
Sundblad 的 BIT 论文标题就是《The Ackermann function. A theoretical, computational, and formula manipulative study》。他把二元函数看成"一族一元函数" F_m(n)，给出 F_0(n)=n+1、F_1(n)=n+2、F_2(n)=2n+3、F_3(n)=2^(n+3)−3、F_4(n)=ITPOW(2,n+3)−3（其中 ITPOW(x,0)=1，ITPOW(x,y+1)=x^ITPOW(x,y)），并给出 F_4(1)=65533、F_4(2)≈10^20000。他定义 C_m(n) 为朴素递归求值所需调用次数，给出 C_0–C_4 的公式，指出 C_4(1)≈(2/3)·2^65536≈10^20000、C_5(0)=C_4(1)+1。他指出并论证"朴素求值的最大递归深度 = 函数值 − 1"。
工程测试部分：ALGOL 60、ALGOL W、PL/I、SIMULA 67 在 IBM 360/75 与 CDC 6600 上，1970 年 8 月在斯德哥尔摩实测；指标是 capability（能算出 F_3(n) 的最大 n）与 efficiency（每毫秒调用次数）。原文一句话把定位说得很清楚："The straightforward definition of Ackermann's function is not a very good algorithm for actual computation, but it provides a method for testing how recursive procedures are handled by programming languages and their compilers." 另外记录：按名调用（call by name）会让 Ackermann(2,4) 的调用次数与时间约为按值调用的 250 倍。
- 来源：Sundblad 1971, *BIT* 11(1), DOI 10.1007/BF01935330，PDF 全文；Sundblad 1970, Report NA70.18。
- 状态：【原文】PDF 全文；报告 NA70.18 仅据参考文献【书目】。

**E3. Wichmann 1976：40 个系统、约 100:1 的性能差异、逐项拆到指令与栈字。**
Wichmann 用同一个六行递归过程测了 40 个系统，覆盖 ALGOL 68、PL/I、Pascal、C、BCPL、Bliss、Coral 66、RTL/2 以及手写机器码。报告的性能差异约 100:1。他记录每次调用的时间、指令数与栈字数。具体数字：C（PDP-11/45）每次调用 50.4 µs、26 条指令；BCPL（IBM 370/165）5.9 µs、19 条指令、9 个字；手写机器码 5–14 条指令、1–2 个字。他还把一次调用的 21 条指令拆成：入口 2、压返回地址与建立环境 3+1、栈溢出检查 2、恢复现场 3、参数 2、函数体 8。
- 来源：Wichmann 1976, *BIT* 16(1):103–110，作者版 PDF。
- 状态：【原文】。

**E4. Wichmann 1976 同时给出了"深度上限"的定量关系，引用的是 Sundblad。**
对 A(3,n)，朴素递归的最大栈深度为 A(3,n)−1 = 2^(n+3)−4。Wichmann 据此换算：在 26K words 的栈上，这个测试能跑到 n=11。同一篇里还记录 PL516 不支持递归，必须用子程序手工压栈才能实现。
- 来源：Wichmann 1976，正文引用 Sundblad。
- 状态：【原文】。

**E5. Wichmann 1977：60 个系统，同时把"能优化到什么程度"写成了一份清单。**
Wichmann 在 *Software: Practice and Experience* 上把测试扩大到约 60 个系统，覆盖 IBM 360/370、ICL 1900、DEC PDP-11、DEC-10、Burroughs 栈机、CDC Cyber 六类体系结构。结论是"实现质量远比语言设计所隐含的开销重要"。他列出四条反对意见并逐条回应，其中第三条直接涉及优化：**Bliss 的优化编译器把两个外层递归调用改成跳转到过程开头，收益约 20%**；他还提到 Wortman 在 360 上做过更激进的版本，但那已经"本质上没有子程序机制"（返回变成无条件跳转），因此不算合法优化。文中还记录一个编码技巧：交换两个参数可以避免在第三层内层调用前压栈。对测试本身的批评包括：只用值参数；第三分支的嵌套调用"certainly not typical"，可能让编译器生成较差代码；需要过量栈空间；360 的 4K 寻址限制会让聪明编译器占便宜。论文给出的机器码等价物本身就是用 `stack[1:1000]` 加一个内部过程手工管理递归的版本。
- 来源：Wichmann 1977, *Software: Practice and Experience* 7(3):317–329, DOI 10.1002/spe.4380070303，PDF 全文。
- 状态：【原文】。

**E6. "非原始递归"对"递归改写成循环"的确切含义：不能改写成有界 for，可以改写成 while + 显式栈。**
这是整个工程侧最容易被说错的一条。Meyer–Ritchie 1967 证明 LOOP 程序（循环次数在进入前确定）的可计算函数类恰好是原始递归函数；原文定理 7 的措辞是："The functions computable by Loop programs are precisely the primitive recursive functions." 阿克曼函数不是原始递归，所以不存在对一切 (m,n) 计算它的 LOOP 程序。但这只排除了"有界 for 循环"。用 while 加一个显式栈（或用计数式迭代）完全可以实现它，只是循环次数事先无界。换句话说：**不可原始递归 ≠ 不可计算 ≠ 不能用迭代写**；被排除的只是"循环上界可由输入在进入循环前算出"这一种改写。
- 来源：Meyer–Ritchie 1967, *Proc. ACM 22nd Natl Conf.*, 465–469, DOI 10.1145/800196.806014，原文定理 7 片段；Grossman–Zeitman 1988 的迭代算法（E7）；本文分析。
- 状态：Meyer–Ritchie【原文片段】定理 7 原话；"while+栈可实现"由 E7 的算法【原文】支撑；其余【分析】。

**E7. Grossman–Zeitman 1988 给了两个明确的迭代算法，并给出复杂度。**
他们采用罗宾逊式定义：A(0,n)=n+1；A(i,0)=A(i−1,1)；A(i,n)=A(i−1,A(i,n−1))。论文里有两个算法：
- 朴素显式栈算法（他们戏称 Stackermann）：最大栈长等于 A(i,n)，空间 O(A(i,n))，时间更差；
- 计数式迭代算法：空间 O(i)，时间 O(i·A(i,n))。
两者都说明"非原始递归"只是说递归深度无法用原始递归函数在进入前界定，不是说不能迭代。
- 来源：Grossman–Zeitman 1988, *Theoret. Comput. Sci.* 57(2–3):327–330, DOI 10.1016/0304-3975(88)90046-1，出版版 PDF。
- 状态：【原文】。

**E8. 这篇论文还留下了当时机器上的实测，可作为"递归实现会炸栈"的直接证据。**
在 Apple IIe / UCSD Pascal 上：递归版算 A(3,5) 栈溢出；Stackermann 跑 A(3,5) 超过 3 分钟、超过 42,000 次 while 循环才得 253；计数式迭代算法 3 秒得同一结果；计数式算法算 A(4,1)=65533 用不到 12 分钟，而 Stackermann 需要数月。这些数字是 1980 年代中期个人机与 Pascal 实现的真实约束，不是理论估计。
- 来源：Grossman–Zeitman 1988，正文实测节。
- 状态：【原文】。

**E9. 尾调用消除在它身上只能消掉一部分帧链，不能把整个递归压平。**
第三分支是 `A(m−1, A(m,n−1))`：内层 `A(m,n−1)` 位于外层调用的参数位置，**不是尾位置**；只有外层 `A(m−1, ·)` 在返回后直接返回。因此尾调用优化最多能把"外层这一串"折叠，内层调用仍要保留帧来接收返回值。Wichmann 1977 也指出这种嵌套调用不典型、容易让编译器生成较差代码。Cornell CS412 的课程材料则从另一面说：如果实现支持尾调用，这类深递归测试会有很大性能收益——但那是"部分收益"，不是"把阿克曼变成循环"。
- 来源：函数定义（Robinson 1948 形式）；Wichmann 1977；Cornell CS412 课程页 `courses.cs.cornell.edu/cs412/2001SP/hw/bench/ack.html`。
- 状态：【分析】+ Wichmann【摘要】+ Cornell【二手，课程材料】。

**E10. 内联与有限展开对它基本无效，因为递归深度事先无界。**
A(3,n) 的朴素递归深度是 2^(n+3)−4，朴素栈算法的最大栈长是 A(i,n)；这两个量都随参数爆炸，且不能用一个原始递归函数在展开前给出上界。所以"把函数体展开 k 层"只能覆盖固定的小参数区域，对一般输入没有帮助；编译器若强行展开，代码体积会随 k 指数增长而收益有限。这也是它被用作"展开优化边界"教学例子的原因。
- 来源：Wichmann 1976（深度公式，引 Sundblad）；Grossman–Zeitman 1988（栈长 = A(i,n)）；本文分析。
- 状态：【原文】数据 + 【分析】结论。

**E11. 记忆化/表格化在它身上空间代价等于函数值本身，因此只在小参数上有意义。**
Liu–Stoller 2003 明确指出：直接递归求值需要 O(A(i,n)) 栈空间且重复计算；用记忆化/表格化（memoization / tabulation）避免重复计算，但需要 O(A(i,n)) 空间。由于 A(i,n) 本身就是爆炸增长的值，缓存表的规模与结果同阶，工程上只对很小的 i,n 可行。这条不是"没人试过"，而是"试过，代价写在论文里"。
- 来源：Liu–Stoller 2003, *SIGPLAN Notices* 38(10):85–91, DOI 10.1145/966049.777398，出版版 PDF。
- 状态：【原文】。

**E12. 部分求值确实拿它当标准示例，而且能给出定量收益。**
Jones 1996 在 *ACM Computing Surveys* 的综述里写得很直白："Ackermann's function is useless for practical computation but an excellent vehicle to illustrate program point specialization." 他把 m 固定为 2，特化出 ack_2 / ack_1 / ack_0 三层残差程序，报告算术运算次数"不到一半"（less than half as many arithmetic operations），并指出程序点特化在这里"相当于记忆化"（amounting to memoization）。更早的 Jones–Gomard–Sestoft 1993《Partial Evaluation and Automatic Program Generation》也以它为例。
- 来源：Jones 1996, *ACM Comput. Surv.* 28(3):480–（止页未核），PDF 相关节；Jones–Gomard–Sestoft 1993, Prentice Hall，示例片段。
- 状态：【原文】Jones 1996 相关节；1993 书【摘要】。

**E13. "预计算/查表"这条线上，能找到的是算法内部的表化与符号求解，不是生产系统的查表。**
Grossman–Zeitman 的计数式迭代本质上是用一个小数组保存各层当前值，等价于把递归栈改成显式表；Sundblad 用 SYMBAL 的公式操作自动求解递推，属于符号层面的"预计算"。但没有找到哪家编译器或运行时为阿克曼函数预置查表、或把它纳入常量折叠/预计算管线的公开记录。
- 来源：Grossman–Zeitman 1988；Sundblad 1971 PDF。
- 状态：【原文】；"没有生产查表"是【未核到】的负面结论，不等于证明不存在。

**E14. 作为基准程序与递归深度测试用例，它在现代测试套件里有可指认的痕迹。**
- LLVM test-suite：`SingleSource/Benchmarks/Shootout-C++/ackermann.cpp`。源码来自 Doug Bagley 的 shootout，核心就是一行 `int Ack(int M, int N) { return(M ? (Ack(M-1,N ? Ack(M,(N-1)) : 1)) : N+1); }`；`SMALL_PROBLEM_SIZE` 时 LENGTH=11，否则 LENGTH=12，输出 `Ack(3,n)`。因此参考输出分别是 16381 与 32765（A(3,11)=2^14−3，A(3,12)=2^15−3）。
- Emscripten：补丁 0007 把上述递归版整体替换成显式栈迭代版（`int stack[100000]` + `while (top > 0)`），提交信息写 "We were overflowing the trusted stack: 'Fix' by removing recursion."，作者 Derek Schuff。这是"实现层真的被它压爆、于是改成迭代"的直接书面证据。镜像页头日期显示 2026-02-03，与该补丁所属的早期版本明显不符，原始提交日期未核。
- Cornell CS412：课程作业页给出 A(3,k)=2^(k+3)−3、至少 4^(k+1) 次调用、递归深度 2^(k+3)−1，用来压编译器的深递归能力。
- GCC 社区：2005 年 java 邮件列表有人用 shootout 的 ackermann 比较 `java -server` 与 gcj，运行 `ackermann 12` 得 `Ack(3,12): 32765`，耗时约 4.3 秒。这属于零散使用，不是测试套件。
这些用例的共同点是"用递归深度压实现"，而不是"验证数学性质"。
- 来源：LLVM test-suite 仓库 `ackermann.cpp` 与 2012-12 testresults；emscripten-releases 补丁 0007 正文；Cornell CS412 课程页；gcc.gnu.org/pipermail/java/2005-April/021104.html。
- 状态：LLVM【原文】仓库文件；Emscripten【原文】补丁正文，日期【未核到】；Cornell【二手，课程材料】；GCC 邮件列表【原文片段】。

**E15. "哪些参数组合算得出来、哪些算不出来"——问题前提要先修正，但确实有人系统研究过"前几个成员"。**
按定义，所有 A(m,n) 都是全可计算的，没有"算不出来"的参数组合；差别只是资源可行性。已知可写出精确值的：A(0,n)=n+1；A(1,n)=n+2；A(2,n)=2n+3；A(3,n)=2^(n+3)−3；A(4,0)=13；A(4,1)=65533；A(4,2)=2^65536−3（19729 位十进制）；A(5,0)=65533。A(4,3) 及以上只能给递归定义或巨大数描述。
系统研究是有的，但研究对象不是"可算性"而是"前几个成员的闭式、调用次数与最大深度"：Sundblad 1971 给出 F_0–F_4 的闭式、C_0–C_4 的调用次数公式、F_4(1)/F_4(2) 的量级，以及"最大深度 = 函数值 − 1"。工程上则把问题换成"在给定机器/栈/时间下能算到哪个 n"：Sundblad 的 capability 指标、Wichmann 的 26K words → n=11 换算、Grossman–Zeitman 的 Apple IIe 实测。没有核到把"参数空间"整体当作可计算性分类来研究的文献；这在数学上也不成立，因为全体参数都可计算。
- 来源：Sundblad 1971 PDF；Wichmann 1976；Grossman–Zeitman 1988；定义与上述数值（可按定义核验）。
- 状态：Sundblad/Wichmann/Grossman–Zeitman【原文】；数值【分析，可由定义核验】；"没有可算性分类研究"为【未核到】。

**E16. 确实存在一支成体系的"Ackermann rating"文献，但它问的是语言表达力，不是参数可算性。**
J. A. Brown 1970 在 *APL Quote-Quad* 提出：给每个编程语言一个评级 j，j 是"该语言存在封闭、非递归的表达式能写出第 j 层阿克曼函数"的最大整数（Linden 的转述是 "a closed, non-recursive expression for j A n"）。Sundblad 1971 接过这个定义并给出对照表：评级 1 对应只有加法（简单汇编器）、2 对应乘法（较高级汇编器）、3 对应幂（ALGOL 60、FORTRAN、PL/I）、4 对应迭代幂（APL）。Linden 1971 主张带 execute 的 APL 评级至少为 5，并论证可为无穷。Breidbart 1979 证明传统 APL 单行函数（只用算术）恰好算 Grzegorczyk 类 E4，因此不带 execute 的 APL 评级恰为 4；带 execute 则为无穷。
这条线的意义：它把"这门语言能表达多高阶的函数"变成了一个可判定的层级问题，而阿克曼函数正是标尺。它不是"哪些参数算得出来"的研究，而是"语言的原语能爬到 Ackermann 层级的第几层"的研究。
- 来源：Brown 1970, *APL Quote-Quad* 2(1):35–36（转引）；Sundblad 1971 PDF；Linden 1971 PDF 首段；Breidbart 1979 PDF 全文。
- 状态：Brown【书目】；Sundblad【原文】；Linden【原文片段】；Breidbart【原文】。Sundblad 评级表来自 PDF 抓取片段，表头与四行内容清楚，但未逐页核对排版。

**E17. 评级线与 Grzegorczyk 层级对接，因而和"原始递归 vs 一般递归"是同一套坐标。**
Breidbart 用 Repeat（有界循环）语言定义原始递归函数，并指出 E4 恰好是"循环嵌套深度不超过 3"的程序类；APL 的 `/`（归约/迭代）提供了比原语高一层的迭代能力，所以"若 APL 把定义 Ek 的函数作为原语，则单行函数可算 Ek+1"。原始递归函数是 Grzegorczyk 各层 Ek 的并；阿克曼函数不在任何一层里。于是"Ackermann rating 为无穷"就有了精确含义：该语言能表达非原始递归的函数。
- 来源：Breidbart 1979，正文与定理 1、定理 2、推论；Grzegorczyk 1953（据其参考文献）。
- 状态：【原文】Breidbart；Grzegorczyk 原文【书目】。

**E18. 优化侧最硬的原始证据是 Bliss 的约 20%：两个外层递归可消，内层嵌套调用不可消。**
Wichmann 1977 记录：Bliss 的优化编译器"removes the recursion on the two outer calls by performing a jump to the beginning of the procedure"，收益约 20%。这与 E9 的结构分析一致：`A(m−1,1)` 和 `A(m−1, ·)` 这两个外层调用在返回后直接返回，可以改成跳转；而第三分支的内层 `A(m,n−1)` 位于参数位置，必须保留帧接收返回值，不能这样消。Wichmann 还提到 Wortman 在 360 上做出过更彻底的版本（把返回也变成无条件跳转），但他认为那已经不算合法优化，因为"本质上没有子程序机制了"。
- 来源：Wichmann 1977, SPE 7(3):317–329，PDF 全文，第 319–320 页。
- 状态：【原文】。

**E19. 内联、展开、记忆化在生产编译器里的直接记录仍然很少；能找到的是论文级推导。**
除 Emscripten 的"去递归"补丁外，没有找到哪份编译器手册、提交记录或设计文档明确说"对阿克曼函数做内联/展开/记忆化"。能找到的是论文级工作：Jones 1996 的程序点特化（固定 m=2，算术运算减半）、Liu–Stoller 2003 的增量化（O(i) 空间）、Grossman–Zeitman 1988 的计数式迭代。Liu–Stoller 还明确说部分求值"可以为 i=3 特化阿克曼函数，但不能像增量化那样导出优化版"。因此这一块的证据等级是"论文有、生产记录无"，不能写成"编译器普遍这样处理"。
- 来源：Jones 1996；Liu–Stoller 2003 PDF 相关节；Grossman–Zeitman 1988；Emscripten 补丁 0007。
- 状态：【原文】论文；生产编译器记录【未核到】。

**E20. 工程侧的负面结论要写清楚：这一层是散落的。**
把上面证据按类型归拢，有五类：（a）过程调用基准（Sundblad 1971、Wichmann 1976/1977）；（b）语言表达力评级（Brown 1970、Linden 1971、Breidbart 1979）；（c）递归消除与优化（Meyer–Ritchie 1967、Wichmann 记录的 Bliss/Wortman、Grossman–Zeitman 1988、Liu–Stoller 2000/2003）；（d）部分求值（Jones–Gomard–Sestoft 1993、Jones 1996）；（e）测试套件与补丁（LLVM、Emscripten、Cornell、GCC 邮件列表）。它们彼此引用不多，时间跨度从 1967 到 2012，没有共同的术语框架，也没有"阿克曼函数工程处理史"这样的综述。因此不能写成一条连贯的工程史；只能写成"五类证据 + 各自能支撑的结论"。
- 来源：本文对上述文献的归纳。
- 状态：【分析】。

---

## 4. 未核到 / unknown

> 这一节只列"查过但没有拿到可靠原件或完整信息"的条目。已经能用二手材料支撑的事实放在 §2、§3，不在这里重复。编号 U1–U22。

**U1. Ackermann 1928 正文未通读。**
已核到：题名《Zum Hilbertschen Aufbau der reellen Zahlen》、*Math. Ann.* 99:118–133、DOI 10.1007/BF01459088、1927-01-20 收稿、1928 年 12 月号、两条脚注原文（提到 Hilbert《论无穷》第 185 页；提到 Sudan 即将发表）。未读：φ(x,y,z) 的完整定义、ρ_z 高阶递归的形式规则、同时递归版本、φ(x,x,x) 非原始递归的证明细节。GDZ 有该卷数字化（PPN235181684_0099），本次只取到卷元数据，未逐页读。
- 状态：【书目+原文脚注】，正文【未核到】。

**U2. Hilbert 1926 第 185 页的原始表述未读。**
"该函数已在 Hilbert 文中提及"目前有阿克曼 1928 脚注这一手证据，但 Hilbert 原文怎么写的、用什么符号、在连续统问题的哪一步出现，未核到。SEP 与 Grossman–Zeitman 的转述只能算【二手】。
- 状态：【未核到】。

**U3. Péter 1935《Konstruktion nichtrekursiver Funktionen》正文未读。**
题名、*Math. Ann.* 111:42–60 已核。二元形式 π(x,y) 的具体定义（π(0,n)=n+1；π(m+1,0)=π(m,1)；π(m+1,n+1)=π(m,π(m+1,n))）只据 SEP/NIST 的转述，未与原文逐式核对。
- 状态：【书目】+【二手】。

**U4. Péter 1935 两篇论文的分工未核。**
同年另有《Über den Zusammenhang der verschiedenen Begriffe der rekursiven Funktion》，*Math. Ann.* 110:612–632，DOI 10.1007/BF01448046。哪一篇首次给出二元形式、哪一篇讨论一般递归概念，未读原文，未核到。
- 状态：【书目】。

**U5. Péter 1937 多重递归、1956 原始递归性判定条件的精确出处未核到。**
SEP 附录提到这两项工作，但没有给出可核的卷页/DOI；本次未补到。
- 状态：【未核到】。

**U6. Robinson 1948 正文未读。**
题名、*Bull. Amer. Math. Soc.* 54:987–993、DOI 10.1090/S0002-9904-1948-09121-2 已核。"今天常见三行定义最早由 Robinson 使用"是 Grossman–Zeitman 的说法（【原文】），Robinson 原文的表述未读。
- 状态：【书目】+【二手】。

**U7. Sudan 1927 正文未读。**
卷页（*Bull. Math. Soc. Roumaine Sci.* 30:11–30）与"独立同时发现"的论证据 Calude–Marcus–Tevy 1979（【原文】）；Sudan 原文的函数定义未读。
- 状态：【书目】+【二手】。

**U8. Kleene 1952 的具体页码未核到。**
只读到 PDF 片段："希尔伯特 1926 关于连续统问题的猜想，由阿克曼 1928 回答"；页码未记。
- 状态：【未核到】。

**U9. Grzegorczyk 1953 原文未读。**
E0–E4 的定义、E4 与"循环嵌套深度 3"的对应，据 Breidbart 1979 的转述；Grzegorczyk 原文（*Rozprawy Matematyczne*，波兰国家科学院，1953）未读。
- 状态：【书目】+【二手】。

**U10. Brown 1970 原文未读。**
定义（评级 j = 能写 j A n 的最大 j）与卷页（*APL Quote-Quad* 2(1):35–36，1970 年 4 月）由两条独立引文核到：Sundblad 1971 参考文献与 Breidbart 1979 参考文献。Brown 原文的论证与例子未读。
- 状态：【书目】。

**U11. Linden 1971 的卷页有冲突，未解。**
Breidbart 1979 引作 "APL Quote-Quad, II (1971), pp. 130–131"；dblp 与 Utah 的 SIGPLAN Notices 目录记作 *SIGPLAN Notices* 6(4), May 1971, pp. 34–35（属 APL Quote Quad 栏目）。两种引文可能是不同版本/重印，也可能是引文误差。PDF 首段内容（"J. A. Brown in the April 1970 APL Quote-Quad raised the idea..."）已读。
- 状态：内容【原文片段】，卷页【未核到】。

**U12. Sundblad 1970 报告 NA70.18 未读。**
只据 Sundblad 1971 的参考文献知道它存在（斯德哥尔摩皇家理工学院）。
- 状态：【书目】。

**U13. Wichmann 1976 的 40 个系统完整数据未逐项抄录。**
已读作者版全文，但本笔记只摘了 C（PDP-11/45）50.4 µs/26 指令、BCPL（370/165）5.9 µs/19 指令/9 字、机器码 5–14 指令/1–2 字，以及 21 条指令的分解。其余系统未逐项记录。
- 状态：【原文】但抽样摘录。

**U14. Wichmann 1977 的 60 个系统完整表未逐项抄录。**
已读全文；六类体系结构与 Bliss 20%、参数交换技巧、四条反对意见已核。逐系统指令数/字节数未抄。
- 状态：【原文】但抽样摘录。

**U15. Emscripten 补丁 d52782e 的原始提交日期未核到。**
补丁正文、作者（Derek Schuff）、提交信息已核；镜像页头写 "Date: Tue, 3 Feb 2026"，与补丁所属的早期 LLVM test-suite 版本明显不符，判断为镜像重写日期。GitHub 提交页抓取只返回导航壳，未取到提交元数据。
- 状态：【未核到】。

**U16. LLVM test-suite 引入 ackermann 的具体提交与年份未核到。**
已核：当前 main 分支源码、`Ack(3,11)`/`Ack(3,12)` 的输出逻辑、2012-12 testresults 出现该基准。何时、由谁引入未核到。
- 状态：【未核到】。

**U17. GCC 是否有正式的 ackermann testsuite 用例未核到。**
只核到 GCC Internals 对 c-torture 的描述，以及 2005 年 java 邮件列表的零散使用（`ackermann 12` → `Ack(3,12): 32765`，约 4.3 秒）。没有在 gcc/testsuite 下核到名为 ackermann 的用例。
- 状态：【未核到】。

**U18. 生产编译器/运行时对 Ackermann 做内联、展开、记忆化、常量折叠的明确记录未核到。**
能找到的是论文级推导（Jones、Liu–Stoller、Grossman–Zeitman）和 Emscripten 的"去递归"补丁；没有编译器手册、提交记录或设计文档说"对该函数做内联/展开/记忆化"。
- 状态：【未核到】。

**U19. A(4,3) 的精确十进制位数未核到。**
已知 A(4,2)=2^65536−3 有 19729 位；A(4,3) 只需按定义写成迭代幂塔，精确位数没有查。
- 状态：【未核到】。

**U20. 是否存在"阿克曼函数工程史/接受史"的综述未核到。**
本次检索没有找到；判断是"没有"，但这是负面结论，不能证明不存在。
- 状态：【未核到】。

**U21. "哪些参数组合算不出来"作为独立研究问题未核到，且前提不成立。**
所有 A(m,n) 全可计算；文献里没有"可算性分类"，只有"给定资源下能算到哪"的工程边界（Sundblad 的 capability、Wichmann 的栈换算、Grossman–Zeitman 的实测）。若下一轮要坚持这个问法，需要改写为"在什么资源模型下、算到哪个 n 是可行的"。
- 状态：【未核到】+【分析】。

**U22. Tarjan 1975 反阿克曼的精确定义与界未核。**
只据 Grossman–Zeitman 参考文献知道 *J. ACM* 22:215–225；α(n) 的原始定义与并查集界的表述未读。
- 状态：【书目】。

---

## 5. 文献与来源表

> 按"能支撑哪条事实"排列。核验状态沿用 §0 图例；同一文献在不同条目里可能状态不同（例如书目已核、正文未读）。

### 5.1 数学侧

| 文献 | 出处 | 核验状态 | 用途 |
|---|---|---|---|
| Hilbert 1926, 《Über das Unendliche》 | *Math. Ann.* 95:161–190 | 【二手】SEP / Grossman–Zeitman / Ackermann 1928 脚注；原文未读 | M1、M2、U2 |
| Ackermann 1928, 《Zum Hilbertschen Aufbau der reellen Zahlen》 | *Math. Ann.* 99:118–133, DOI 10.1007/BF01459088；收稿 1927-01-20，刊出 1928-12 | 【书目+原文脚注】 | M1–M3、M10、U1 |
| Sudan 1927 | *Bull. Math. Soc. Roumaine Sci.* 30:11–30 | 【书目】 | M10、U7 |
| Péter 1935, 《Konstruktion nichtrekursiver Funktionen》 | *Math. Ann.* 111:42–60 | 【书目】 | M7、U3 |
| Péter 1935, 《Über den Zusammenhang der verschiedenen Begriffe der rekursiven Funktion》 | *Math. Ann.* 110:612–632, DOI 10.1007/BF01448046 | 【书目】 | U4 |
| Péter 1937 / 1956 | 出处未核到 | 【未核到】 | U5 |
| Robinson 1948 | *Bull. Amer. Math. Soc.* 54:987–993, DOI 10.1090/S0002-9904-1948-09121-2 | 【书目】 | M8、U6 |
| Kleene 1952, *Introduction to Metamathematics* | 页码未核 | 【二手】片段 | M1 旁证、U8 |
| Calude–Marcus–Tevy 1979 | *Historia Mathematica* 6:380–384；PDF: cs.auckland.ac.nz/~cristian/crispapers/sudan.pdf | 【原文】 | M10 |
| Grzegorczyk 1953 | *Rozprawy Matematyczne*（波兰国家科学院） | 【书目】 | E17、U9 |
| SEP, "Recursive Functions" 附录 "History of the Ackermann and Péter functions" | plato.stanford.edu/archives/fall2025/entries/recursive-functions/ackermann-peter.html | 【原文】 | M1–M4、M7 |
| NIST DADS, "Ackermann's function" | xlinux.nist.gov/dads/HTML/ackermann.html | 【原文】 | M7、M8 |
| MathWorld, "Ackermann Function" | mathworld.wolfram.com/AckermannFunction.html | 【原文】 | M5 |

### 5.2 工程侧

| 文献 | 出处 | 核验状态 | 用途 |
|---|---|---|---|
| Meyer–Ritchie 1967, 《The Complexity of Loop Programs》 | *Proc. ACM 22nd Natl Conf.*, 465–469, DOI 10.1145/800196.806014 | 【原文片段】定理 7；全文未通读 | E6、E17 |
| Brown 1970, 《Using the Ackermann Function to Rate Programming Languages》 | *APL Quote-Quad* 2(1):35–36（1970-04） | 【书目】两条独立引文 | E16、U10 |
| Sundblad 1970, Report NA70.18 | 斯德哥尔摩皇家理工学院 | 【书目】 | E2、U12 |
| Sundblad 1971, 《The Ackermann function. A theoretical, computational, and formula manipulative study》 | *BIT* 11(1), DOI 10.1007/BF01935330 | 【原文】PDF 全文 | E2、E15、E16 |
| Linden 1971, 《The Ackermann Function in APL》 | *SIGPLAN Notices* 6(4):34–35 / *APL Quote-Quad* II:130–131（冲突） | 【原文片段】 | E16、U11 |
| Tarjan 1975 | *J. ACM* 22:215–225 | 【书目】 | M9、U22 |
| Wichmann 1976, 《Ackermann's function: a study in the efficiency of calling procedures》 | *BIT* 16(1):103–110, DOI 10.1007/BF01940783；作者版 PDF: gtoal.com/history.dcs.ed.ac.uk/archive/docs/Imp_Benchmarks/ack.pdf | 【原文】 | E1、E3、E4 |
| Wichmann 1977, 《How to Call Procedures, or Second Thoughts on Ackermann's Function》 | *Software: Practice and Experience* 7(3):317–329, DOI 10.1002/spe.4380070303；PDF: cs.tufts.edu/~nr/cs257/archive/brian-wichmann/calls.pdf | 【原文】 | E5、E9、E18 |
| Breidbart 1979, 《APL and the Grzegorczyk Hierarchy》 | *APL Quote-Quad* 9(4):271–273（ACM 1979）；PDF: dl.acm.org/doi/pdf/10.1145/390009.804472 | 【原文】 | E16、E17 |
| Grossman–Zeitman 1988, 《An inherently iterative computation of Ackermann's function》 | *Theoret. Comput. Sci.* 57(2–3):327–330, DOI 10.1016/0304-3975(88)90046-1 | 【原文】 | E7、E8、E10、E11、E13 |
| Jones–Gomard–Sestoft 1993, *Partial Evaluation and Automatic Program Generation* | Prentice Hall | 【摘要】示例片段 | E12 |
| Jones 1996, 《An introduction to partial evaluation》 | *ACM Comput. Surv.* 28(3):480–（止页未核） | 【原文】相关节 | E12、E19 |
| Liu–Stoller 2000 | PEPM'00, DOI 10.1145/328690.328700 | 【摘要】 | E19 |
| Liu–Stoller 2003, 《Optimizing Ackermann's Function by Incrementalization》 | *SIGPLAN Notices* 38(10):85–91, DOI 10.1145/966049.777398；PDF: cs.stonybrook.edu/~stoller/papers/Ackermann-PEPM03.pdf | 【原文】 | E11、E19 |
| LLVM test-suite, `SingleSource/Benchmarks/Shootout-C++/ackermann.cpp` | raw.githubusercontent.com/llvm/llvm-test-suite/main/... | 【原文】 | E14、U16 |
| Emscripten patch 0007, `ackermann-remove-recursion-to-avoid-stack-overflow` | chromium.googlesource.com/emscripten-releases/.../patches/llvm-test-suite/0007-...patch | 【原文】补丁正文；日期【未核到】 | E14、E19、U15 |
| Cornell CS412, `hw/bench/ack.html` | courses.cs.cornell.edu/cs412/2001SP/hw/bench/ack.html | 【二手，课程材料】 | E9、E14 |
| GCC java 邮件列表, "Slow recursive functions" | gcc.gnu.org/pipermail/java/2005-April/021104.html | 【原文片段】 | E14、U17 |
| GCC Internals, "C Tests" / c-torture | gcc.gnu.org/onlinedocs/gccint/C-Tests.html | 【原文】 | U17 |
| CHM 博客, "Discovering Dennis Ritchie's Lost Dissertation" | computerhistory.org/blog/discovering-dennis-ritchies-lost-dissertation/ | 【原文】 | M6 旁证 |
| UTEP 课程讲义 | 未记 URL | 【二手】 | M6 旁证 |

---

## 6. 检索记录

> 预算撤回后按需补检。下列检索按"目的—得到什么—还缺什么"记，不逐条抄返回结果。

1. **Ackermann 1928 书目与原文线索**：Springer DOI 页核到题名、卷页、收稿/刊出日期与两条脚注原文；GDZ 卷元数据核到 1928 年与 PPN。未取到正文 PDF。
2. **Péter 1935 题名**：一条参考文献目录核到《Konstruktion nichtrekursiver Funktionen》，*Math. Ann.* 111:42–60；另一条核到同年的 110:612–632 论文，确认是两篇。
3. **Sundblad 1971 全文**：出版方摘要给出"一元函数族、前几个成员、调用次数、最大深度、Ackermann rating"；另取得 PDF 全文，核到 F_0–F_4、C_0–C_4、F_4(1)=65533、F_4(2)≈10^20000、测试表与"最大深度 = 函数值 − 1"。
4. **Wichmann 1976 全文**：作者版 PDF 核到 40 系统、100:1、C/BCPL/机器码数字、21 条指令分解、26K words → n=11。
5. **Wichmann 1977 全文**：Tufts 镜像 PDF 核到 60 系统、六类架构、四条反对意见、Bliss 20%、参数交换、`stack[1:1000]` 机器码等价物。
6. **Meyer–Ritchie 1967**：检索到 PDF 片段，核到定理 7 原话；全文未通读（scispace 二次抓取触发人机验证）。
7. **Ackermann rating 线**：由 Breidbart 1979 全文（ACM PDF）核到 Brown 1970 定义、Linden 1971 主张、APL = E4、rating 4/无穷；Sundblad 1971 的评级表由 PDF 片段核到四行（1 加法 / 2 乘法 / 3 幂 / 4 迭代幂）。
8. **LLVM 基准源码**：raw.githubusercontent.com 取到 `ackermann.cpp` 全文，核到 `Ack(3,n)`、LENGTH 11/12、输出格式。
9. **Emscripten 补丁**：googlesource 的 `?format=TEXT` 返回 base64，解码后核到补丁正文、作者、提交信息、显式栈实现；GitHub 提交页只返回导航壳，原始日期未核到。
10. **GCC 线索**：GCC Internals 的 c-torture 说明核到；2005 java 邮件列表核到 `ackermann 12` → `Ack(3,12): 32765`、约 4.3 秒；未核到 gcc/testsuite 下的正式用例。
11. **Cornell CS412**：课程页核到 A(3,k) 公式、调用次数下界、递归深度、TCO 讨论（课程材料，按【二手】处理）。
12. **Combinator 侧**：检索超编译/去森林化是否拿阿克曼当例子，未找到直接证据；找到的是 Liu–Stoller 对部分求值"只能特化 i=3、不能导出优化版"的说明，已写入 E19。
13. **社区材料**：Hacker News 等出现"非原始递归 ⇒ 不能转成迭代"的说法，可作为"常见误读"的旁证，但未写入正式事实条目（等级太低）。
14. **未做的检索**：没有系统扫 IEEE Xplore / ACM DL 的全部编译器会议录，也没有查俄语/匈牙利语文献；这是本轮的范围限制，不是"已穷尽"。

**检索侧的失败与限制**：
- GitHub 提交页抓取失败（只返回导航壳），导致 Emscripten 补丁原始日期未核。
- scispace 的 Meyer–Ritchie PDF 二次抓取触发人机验证，只保留第一次的片段。
- 部分 PDF（Sundblad、Wichmann）通过镜像/作者页取得，非出版方原件；已在条目里注明"PDF 全文"，未把它升级为"出版方原件"。
- 没有找到任何"阿克曼函数工程史"综述；这是负面结果，已写入 E20/U20。


