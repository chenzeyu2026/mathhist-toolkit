# 微积分：一次跨越三百年的讲解

本文是 `BR-ANA-CALC`（微积分）分支的试点长文本，与同目录 `graph.json` 双向互指：本文每个关键处用 `graph://` 前缀加节点或边 ID 指向图；图节点里凡写入 `text_ref` 的，都指回本文对应小节。

讲解按"一个可讲清的单元"组织，不按编年史铺陈。四层（问题、失败、记号、文本）在最后一节合并看一次。

---

## 牛顿与莱布尼茨：两条独立路径 {#newton-leibniz}

17 世纪的求切线问题与求积问题，长期分属两套技术传统：切线靠几何作图和运动学直觉，求积靠穷竭法与不可分法。`graph://PR:tangent-problem` 与 `graph://PR:quadrature-problem` 是两条并行的入口，而不是同一个"导数问题"的两种说法——把两者提前统一，是后世教科书最常见的倒放。

牛顿的流数法把"量"与"量的变化率"分开，用时间作隐含自变量：`graph://ME:fluxion-method`。莱布尼茨的微分法直接操作微分 dy、dx 及其商：`graph://ME:leibniz-differential-method`。两条路线在结果上高度重合，在表述上互不相通。

"各自独立"这件事在图里由两条 `introduced` 边承载：

- `graph://E:PE:newton>introduced>CO:derivative`
- `graph://E:PE:leibniz>introduced>CO:derivative`

两条边各带自己的时间与文献，这是框架允许的（同一概念可被多次"引入"）。但"这两次引入相互独立"本身没有专门边类型，只能写在 `note` 里——见文末说明与 `report.md` 的缺口第 1 条。

两人都触到了微分与求积的互逆关系，即后来的 `graph://TH:fundamental-theorem-of-calculus`；但"基本定理"是后世命名，当时无人这样称呼。本次试点没有为"牛顿表述过互逆关系"单独建观点节点，所以图上没有对应的 `asserted_by` 边——这本身就是框架的一个提醒：**观点层可以很细，但只在需要区分"谁主张的"时才值得建节点**，否则会膨胀成一人一句。试点里唯一一条 `asserted_by` 是理论级的：`graph://E:TY:infinitesimal-calculus-17c>asserted_by>ST:infinitesimal-legitimacy`。

---

## 记号之争：dy/dx 与点记法 {#notation}

`graph://NO:dy-dx` 与 `graph://NO:fluxion-dot` 是一对竞争记号：

- `graph://E:NO:dy-dx>competes_with>NO:fluxion-dot`（无向，只存一条，from 取字典序较小者）

竞争的结果不是一方消灭另一方，而是按领域分工：英国长期沿用它点记法，欧陆解析力学与后来分析学沿用微分记号。图里只能记一条 `competes_with`，无法表达"各自在哪些领域胜出"——这是缺口第 5 条。

微分记号还有一个副作用：它长得像"两个微分相除"，而现代导数定义是差商取极限。这个"形似实非"的残留，被写进了失败节点的 `residue`：`graph://FA:infinitesimals-as-finite-quantities`。

积分号 `graph://NO:integral-sign` 是另一条独立的记号线，与 dy/dx 不同源，也不同步定型。

---

## 贝克莱的责难 {#berkeley}

1734 年贝克莱在《分析学家》里抓住的不是"无穷小算错了"，而是"同一步里 dx 既被当作非零（用来约分）又被当作零（用来消项）"。这就是 `graph://FA:infinitesimals-as-finite-quantities` 的 `flawed_step`。

图里这条批评走的是"观点节点"路线，而不是直接连"人批理论"：

- 批评内容本身：`graph://ST:berkeley-ghosts`（观点节点，`status: critical`）
- 被批评方对无穷小合法性的辩护：`graph://ST:infinitesimal-legitimacy`
- 两者对立：`graph://E:ST:berkeley-ghosts>contradicts>ST:infinitesimal-legitimacy`
- 观点落在哪本书：`graph://E:ST:berkeley-ghosts>claimed_in>TX:berkeley-1734-analyst`
- 观点针对哪个对象：`graph://E:ST:berkeley-ghosts>about>TY:infinitesimal-calculus-17c`

注意这里为什么绕：`contradicts` 只允许 ST↔ST，所以"贝克莱批评无穷小演算"必须借一个观点节点中转。这是缺口第 4 条。

当时为什么没人因此停用微积分？失败节点的 `why_accepted` 写的是：算法在大量问题上给出正确结果，而函数与极限的严格概念尚未出现，实际有效性压过了基础疑虑。这一点是本框架"正反都留"规则最直接的落点——错误路线不是脚注，而是与正确结论同等建节点。

---

## 四层同时看 {#four-layers}

把四层叠在同一个分支上，`BR-ANA-CALC` 的结构是这样：

1. **问题层**：`graph://PR:tangent-problem`、`graph://PR:quadrature-problem` → 贝克莱之后浮出的 `graph://PR:infinitesimal-foundations` → 由极限路线重述的 `graph://PR:limit-foundations`。
2. **失败层**：`graph://FA:infinitesimals-as-finite-quantities`，指向被取代的理论 `graph://TY:infinitesimal-calculus-17c`，`corrected_by` 指向 `graph://PE:cauchy`，纠正事件是 `graph://EV:1821-cauchy-cours`。
3. **记号层**：dy/dx、点记法、∫、ε-δ 四套写法分别挂到各自所指的概念上（`denotes`）。
4. **文本层**：从 1671 手稿到 1859 汉译，见下一节。

问题层的演变不是"一个问题换了个说法"，而是三次重述：

- `graph://E:PR:infinitesimal-foundations>reformulates>PR:limit-foundations`
- 理论层面：`graph://E:TY:infinitesimal-calculus-17c>supersedes>TY:limit-calculus`（按 §5.6，from 是旧理论、to 是新理论）

这里有一个真实的别扭：`supersedes` 的 from 是**被取代的旧对象**，而英文 "X supersedes Y" 的直觉是 X 为新、Y 为旧。两种读法方向相反，填图时极易写反；§5.6 的"旧→新"约定必须靠查表记住，不能靠语感。

"瞬时速度到底是什么"这个问题本身的演变，落在概念层：`graph://CO:instantaneous-velocity` 从"某一段的平均速度在段长趋零时的极限"变成"位移对时间的导数"，再变成"导数的物理解释之一"。图里用 `depends_on` 与 `uses_notation` 表达它和导数、微分记号的关系，但"同一概念的解释权重随时间转移"没有边可写。

---

## 文本链：从手稿到汉译 {#text-chain}

`TX:` 是书目实体，`TW:` 是具体载体，二者用 `witness_of` 连；载体之间用 `derived_from` 连。本次试点实际建成两条链：

**牛顿链**

- `graph://TX:newton-1671-methodus` ← `graph://TW:newton-1671-methodus.ms`（1671 手稿）
- `graph://TX:newton-1671-methodus` ← `graph://TW:newton-1671-methodus.print-1736`（1736 英译刊本，晚于手稿 65 年）

**莱布尼茨—洛必达—柯西链**

- `graph://TX:leibniz-1684-nova-methodus` ← `graph://TW:leibniz-1684-nova-methodus.print`（《学者纪事》1684）
- `graph://TX:lhopital-1696-analyse` ← `graph://TW:lhopital-1696-analyse.print`（1696 教科书化）
- `graph://TX:cauchy-1821-cours` ← `graph://TW:cauchy-1821-cours.print`（1821 重述基础）

链上每一环都带 `role`（author/translator/…），人物用 `contributed_to` 挂到文本或载体：`graph://E:PE:loomis>contributed_to>TX:loomis-1850-elements`。这里 `contributed_to` 与 `introduced` 的分工是清楚的：前者是"对文本做了什么"，后者是"对概念/方法做了什么"。

手稿与刊本之间**没有**建 `derived_from`——因为 1736 英译究竟据哪份手稿，本次未核实。宁缺勿造，这条留空本身就是记录。

---

## 译名：微分与积分 {#translation}

1859 年《代微积拾级》是微积分进入中文的第一个完整载体：

- 书目：`graph://TX:loomis-1850-elements`
- 原刊本：`graph://TW:loomis-1850-elements.original`
- 汉译本：`graph://TW:loomis-1850-elements.xu-li-1859`
- 汉译事件：`graph://EV:1859-xu-li-translation`
- 两位参与者：`graph://PE:loomis`（原作者）、`graph://PE:wylie`（口译）、`graph://PE:li-shanlan`（笔述）

译名本身被升格为独立节点，而不是塞进文本节点的字符串：

- `graph://NO:term-weifen-zh`（「微分」）
- `graph://NO:term-jifen-zh`（「积分」）

理由是 `denotes` 只允许 NO→CO，而译名要指称的是概念，不是文本。但这里立刻遇到一个缺口：**"某人 + 某译本 + 某译名"是三元组**，图里只能拆成 `introduced`（人→译名）+ `contributed_to`（人→文本）+ `supports`（文本→译名）三条边，读图时要自己拼回去。这是缺口第 3 条。

---

## 附：图中未覆盖的部分

- 英国与欧陆记号分工的长期并存：`competes_with` 无法表达"领地分工"。
- "独立发现"的证据强度：只能靠 `note`，没有边属性。
- 批评者与被批评理论之间的直接边：必须借 ST 中转。
- 学科名"微积分"本身作为术语：`denotes` 只能指向 concept，无法挂到 branch。

以上四条都写进了 `report.md` 的缺口清单，未就地扩表。
