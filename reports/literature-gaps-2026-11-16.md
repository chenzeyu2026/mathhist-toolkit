# 语料「待补出处」文献检索与缺口清单

- 日期：2026-11-16
- 对象：`corpus/01-微积分起源.patched.md` 中 29 条标注「待补出处（原稿未给出处）」的证据标记
- 状态：**第一轮检索 + 2026-11-16 回填（6 处，见 §7）；未回填的仍保持「待补」**
- 配套文件：`reports/literature/` 下 7 个 PDF（见 §2）

## 0. 结论摘要

| 项 | 数量 | 说明 |
|---|---|---|
| 待补标记总数 | 29 | 27 条 `S`、2 条 `A`；原稿 `01-微积分起源.md` 中为 0，占位是打标时新加的 |
| 已取得全文 | 7 条 | L03、L04、L12、L16、L17、L21、L22；7 个 PDF。逐条核对正文后 **4 条通过、已回填**（L04、L12、L16、L17），3 条核对不上保持待补（L03、L21、L22） |
| 原文可自取、无需申请 | 1 条 | L06 莱布尼茨 1684，候选来源 archive.org `s1id13206500` p. 467；本轮该站超时，未取到，保持待补 |
| 书目确定、需文献传递 | 15 条 | 除 Enros 1983 为期刊论文外均为专著，建议按书申请馆际互借 |
| 仅有题录线索、不能直接当出处 | 4 条 | L14、L19、L27、L29；中文期刊题录与日文史料，需人工确认作者/年期 |
| 需要你决策 | 2 条 | L13（教材算不算 `S`）、L15（史学叙述还是教材反例）——**均已按决定处置**，见 §7 |
| 知网 | 0 条 | 检索页触发滑动安全验证，按约定停止，未尝试绕过 |

> 7 + 1 + 15 + 4 + 2 = 29。分类以 §3 的「状态」列为准，§4 是同一批条目的展开，§7 是回填记录。

## 1. 方法与判定口径

**渠道与结果**

| 渠道 | 结果 |
|---|---|
| 知网 `kns.cnki.net` | 打开检索页即要求「请完成安全验证（向右滑动）」，按约束停止，未登录、未绕过 |
| 维普 `qikan.cqvip.com` | 部分题录与摘要可见，全文需登录 |
| arXiv / Numdam / 大学课程页 / 出版社开放页 | 可直连下载，7 篇落盘 |
| `scholarship.claremont.edu` | 被 Cloudflare「Just a moment…」拦截，改由 `matharticles.com` 取得同一篇 |
| `cfraser.artsci.utoronto.ca` | 链接已失效（返回停放页 HTML），未取得 |
| archive.org / Wikimedia Commons | 莱布尼茨 1684 年原刊可定位到具体页（`s1id13206500`，p. 467） |

**匹配分级**（写进每条的状态列）

- **已获取**：全文已落盘，且论题与该句直接对应，只需核对页码即可回填。
- **书目已核**：书目信息有独立来源可查，但全文未取得；不能仅凭书名回填，须等拿到正文确认对应段落。
- **线索不足**：只找到题录、转载或教学讲义，**不作为出处**，需要再查或人工确认。
- **待决策**：文献本身可得，但「该用什么等级」需要你定。

## 2. 已下载文献

目录：`reports/literature/`（均为开放获取，已校验 `%PDF` 头与 `%%EOF` 尾）

| 文件 | 篇目 | 来源 | 对应条目 |
|---|---|---|---|
| `grabiner-1983-epsilon.pdf` | Grabiner, "Who Gave You the Epsilon? Cauchy and the Origins of Rigorous Calculus", *American Mathematical Monthly* 90(3), 1983, 185–194 | matharticles.com | L299、L431、L462、L569 |
| `grabiner-cauchy-derivative.pdf` | Grabiner, "The Origins of Cauchy's Theory of the Derivative" | Harvard 课程页 | L299、L410、L462 |
| `fermat-quadrature-rhm-2008.pdf` | "Fermat's Method of Quadrature", *Revue d'histoire des mathématiques* 14(1), 2008, 5– | Numdam | L159 |
| `barrow-leibniz-ftc-arxiv-1111.6145.pdf` | "Barrow and Leibniz on the Fundamental Theorem of the Calculus", arXiv:1111.6145 | arXiv | L185 |
| `cauchy-continuum-arxiv-1108.4201.pdf` | "Cauchy's Continuum", arXiv:1108.4201 | arXiv | L462、L569 |
| `historical-infinitesimalists-arxiv-2210.14504.pdf` | "Historical Infinitesimalists and Modern Historiography of Infinitesimals", arXiv:2210.14504 | arXiv | L509 |
| `madhava-correction-terms-arxiv-2405.11134.pdf` | "On Mādhava and his Correction Terms for the Mādhava–Leibniz Series for π", arXiv:2405.11134 | arXiv | L95 |

> 注：以上 arXiv 篇目是预印本/综述性论文，可作 `S`，但正式发表信息需在回填时补；硕士论文、课程讲义类一律未计入「已获取」。

## 3. 汇总表（29 条）

「需要」列指该句按规范应配的证据类型；「状态」按 §1 分级。

| ID | 行 | 现等级 | 论断（缩写） | 需要 | 建议文献 | 状态 |
|---|---|---|---|---|---|---|
| L01 | 77 | S | 割圆术有极限思想与逼近算法，但未抽象为算子 | S | 郭书春《中国科学技术史·数学卷》；Needham, *SCC* Vol. 3 (1959) | 书目已核 |
| L02 | 95 | S | 喀拉拉学派无穷级数早于欧洲，但未形成系统 | S | Plofker, *Mathematics in India* (2009)；Joseph, *A Passage to Infinity* (2009) | 书目已核（另有 OA 论文 1 篇） |
| L03 | 159 | S | 费马用不等式夹逼得到 ∫xⁿ | S | Mahoney, *The Mathematical Career of Pierre de Fermat* (1994)；RHM 14(1) 2008 论文 | 核对不上，保持待补（§7.2） |
| L04 | 185 | S | 巴罗 1670 已有几何形式，格雷戈里接近 | S | arXiv:1111.6145（内引 Baron 1969, 232；Gregory 1668, Prop. VI） | **已回填**（§7.1） |
| L05 | 203 | S | 牛顿《原理》用首末比，回避无穷小实体 | S | Guicciardini, *Reading the Principia* (1999)；Pourciau 2002 | 书目已核 |
| L06 | 216 | **A** | 1684 年论文给的是纯形式规则 | A | Leibniz, "Nova methodus…", *Acta Eruditorum* 3 (1684), 467–473 | 未取到原页，保持待补（§7.2） |
| L07 | 228 | S | 1684 发表、1660s–1671 写成、1711–1713 申诉与报告 | S | Hall, *Philosophers at War* (1980) | 书目已核 |
| L08 | 230 | S | 双方并列说法，今日通行判断为独立发明 | S | Hall (1980)；Bertoloni Meli, *Equivalence and Priority* (1993) | 书目已核 |
| L09 | 232 | S | 争论使记号身份化，导致英欧分流 | S | Hall (1980)；Cajori, *A History of the Conceptions of Limits and Fluxions* (1919) | 书目已核 |
| L10 | 284 | S | 洛必达教材内容多来自与约翰·伯努利的通信 | S | Katz, *A History of Mathematics* (3rd ed. 2009), §11；1696 原书（A） | 书目已核（另有开放文章） |
| L11 | 287 | S | 伯努利发展分离变量、积分因子、等周问题 | S | Boyer, *The History of the Calculus* (1959)；Edwards (1979) | 书目已核 |
| L12 | 299 | S | 柯西把 dx 解释为趋于零的变量 | S | Grabiner, "The Origins of Cauchy's Theory of the Derivative", *Historia Mathematica* 5 (1978), 382–383 | **已回填**（§7.1） |
| L13 | 304 | S→**F** | dx 是余切空间的基向量（线性泛函） | F（教材标准表述） | Spivak, *Calculus on Manifolds* (1965), ch. 4 | **已处置**：改写为说明句并降为 F（§7.1） |
| L14 | 309 | S | 嘉当外微分使 d²=0，FTC 成为 Stokes 特例 | S | Hawkins, *The Emergence of the Theory of Lie Groups* (2000) | 线索不足 |
| L15 | 410 | S | 拉格朗日假设幂级数展开；收敛半径为零或不等于原函数 | S | Grabiner, "Who Gave You the Epsilon?", *Amer. Math. Monthly* 90 (1983), p. 192 | **已回填**（§7.1） |
| L16 | 431 | S | 柯西 1823 的「无穷小」定义 | S | Grabiner 1978, *Historia Mathematica* 5, p. 382 | **已回填**（§7.1） |
| L17 | 462 | S | ε-δ 表述是「存在」断言，无运动 | S | Grabiner 1983, *Amer. Math. Monthly* 90, p. 185 | **已回填**（§7.1） |
| L18 | 465 | S | ∀、∃ 记号由皮亚诺 1889 定型 | S | Kennedy, *Peano: Life and Works* (1980)；Cajori, *Notations* Vol. 2 | 书目已核 |
| L19 | 468 | S | 魏尔斯特拉斯 1872 构造处处连续处处不可导函数 | S | Thim, *Continuous Nowhere Differentiable Functions* (2003)；Pinkus (2000) | 线索不足 |
| L20 | 503 | **A** | 1966 年 North-Holland 出版《Non-Standard Analysis》，含长篇历史部分 | A | Robinson, *Non-Standard Analysis*, Amsterdam: North-Holland, 1966 | 书目已核 |
| L21 | 509 | S | 鲁滨逊自称「恢复」而非「证实原文」 | S | arXiv:2210.14504；Fraser & Dauben 长文（原链接失效） | 核对不上，保持待补（§7.2） |
| L22 | 569 | S | 柯西曾倾向认为连续蕴涵可导 | S | Grabiner, *The Origins of Cauchy's Rigorous Calculus* (1981) | 核对不上，保持待补（§7.2） |
| L23 | 611 | S | 赫歇尔、巴贝奇、皮科克成立学会，推行莱布尼茨记号 | S | Enros, "The Analytical Society (1812–1813)", *Historia Mathematica* 10 (1983), 24–47 | 书目已核 |
| L24 | 622 | S | 记号只是表层，深层是教育制度、传播方式、方法论立场 | S | Warwick, *Masters of Theory* (2003)；Enros (1983) | 书目已核 |
| L25 | 654 | S | 柯西讲义出自工程师教育语境 | S | Belhoste, *Augustin-Louis Cauchy: A Biography* (1991)；Grattan-Guinness (1990) | 书目已核 |
| L26 | 692 | S | 皮亚诺 1890 构造空间填充曲线 | S | Sagan, *Space-Filling Curves* (1994)；Peano 1890 原文（宜补 A） | 书目已核 |
| L27 | 704 | S | 宋元天元术、四元术是符号化尝试 | S | 郭世荣、魏雪刚《40 年来的宋元数学史研究》；钱宝琮《中国数学史》 | 线索不足 |
| L28 | 710 | S | 花拉子米代数以 al-jabr 为核心；伊本·海赛姆求积 | S | Rashed, *The Development of Arabic Mathematics* (1994)；MacTutor 条目 | 书目已核 |
| L29 | 712 | S | 关孝和开创円理，用无穷级数处理弧、球；遗题文化 | S | Horiuchi, *Japanese Mathematics in the Edo Period* (2010)；中文《关孝和与关流学派》 | 线索不足 |

## 4. 分类明细

### 4.1 已取得全文（7 条；逐条核对后 4 条已回填）

- **L04 巴罗/格雷戈里**：arXiv:1111.6145 p. 1 直接给出巴罗《几何讲义》(1670) Lect. X, Prop. 11 的命题结构与格雷戈里《Geometriae pars universalis》(1668) Prop. VI 的对应，注 3 另引 Baron 1969, 232。已回填。
- **L12 / L16 / L17 柯西**：Grabiner 1978（*Historia Mathematica* 5）pp. 382–383 覆盖 $dx$ 的解释与无穷小定义；Grabiner 1983（*Amer. Math. Monthly* 90）p. 185 讲 ε-δ 的静态化。三条均已回填。
- **L15 拉格朗日**：Grabiner 1983 p. 192 是同一史学叙述（幂级数假设及其失败），已回填；Edwards/Boyer 未取得正文。
- **L03 费马**（未回填）：RHM 2008 讲的是费马 1644 年的抛物线与双曲线求积，证明细节指向 Mahoney 1994, pp. 245–254；全文没有「不等式夹逼」的叙述。不能仅凭同讲费马求积就回填。
- **L21 鲁滨逊**（未回填）：arXiv:2210.14504 只支持「另造模型、不证明历史原文为真」这半句；「鲁滨逊自称 rehabilitation」无据，Fraser & Dauben 链接失效、Robinson 1966 未取得。
- **L22 柯西倾向连续蕴涵可导**（未回填）：Grabiner 1978/1983 均未讨论这一点，出处应是 Grabiner 1981 书，未取得正文。

### 4.2 书目确定、需获取（15 条，下表按文献聚合为 17 行）

这些条目名字与论题对得上，但**没有读到正文**，回填前必须核对具体页码/段落，否则只能算「疑似相关」。多数是专著，建议走馆际互借或文献传递。下表按文献聚合，同一本书覆盖多条时会重复出现条目 ID；L06 不在此列（archive.org 可直接取原页）。

| 需要申请 | 对应 |
|---|---|
| Needham, *Science and Civilisation in China*, Vol. 3 (CUP 1959)；郭书春《中国科学技术史·数学卷》 | L01 |
| Hall, *Philosophers at War* (CUP 1980) | L07、L08、L09 |
| Boyer, *The History of the Calculus and its Conceptual Development* (Dover 1959) | L11、L15 |
| Edwards, *The Historical Development of the Calculus* (Springer 1979) | L11、L15 |
| Katz, *A History of Mathematics*, 3rd ed. (2009) | L10 |
| Guicciardini, *Reading the Principia* (CUP 1999) | L05 |
| Plofker, *Mathematics in India* (Princeton 2009) | L02 |
| Joseph, *A Passage to Infinity* (SAGE 2009) | L02 |
| Kennedy, *Peano: Life and Works* (Reidel 1980) | L18 |
| Sagan, *Space-Filling Curves* (Springer 1994) | L26 |
| Hawkins, *The Emergence of the Theory of Lie Groups* (Springer 2000) | L14 |
| Belhoste, *Augustin-Louis Cauchy: A Biography* (Springer 1991) | L25 |
| Grattan-Guinness, *Convolutions in French Mathematics, 1800–1840* (1990) | L25 |
| Warwick, *Masters of Theory* (Chicago 2003) | L24 |
| Enros 1983, *Historia Mathematica* 10: 24–47 | L23、L24 |
| Rashed, *The Development of Arabic Mathematics* (Kluwer 1994) | L28 |
| Robinson, *Non-Standard Analysis* (North-Holland 1966) | L20（A 级，需核历史部分页码） |

另：**L06 莱布尼茨 1684** 不需要传递，archive.org 的 `s1id13206500` 第 467 页起即为原文；回填时写全「*Acta Eruditorum* 3 (1684), 467–473」即可。

### 4.3 仅线索、不能当出处（4 条）

- **L14 嘉当**：只找到哈佛课程讲义与科普页，均非可引文献。建议改引 Hawkins (2000) 的相关章节（待核）。
- **L19 魏尔斯特拉斯**：找到多份课程讲义复述 1872 年证明，但缺一手文献的完整书目（1872 年柏林科学院报告的出处与 1875 年正式发表信息需核）。Thim (2003) 硕士论文可作辅助，不宜单独作 `S`。
- **L27 天元术/四元术**：检索到郭世荣、魏雪刚《40 年来的宋元数学史研究》（内蒙古师大科技史研究院网页转载）与维普《重审元明之际中国数学的转变》题录；前者是综述，适合做 `S`，但期刊名、年卷期待核。
- **L29 关孝和**：中文《关孝和与关流学派》只见豆丁转载，原刊信息不明；日文 `wasan.jp` 的 PDF 是早期研究，可读但引用信息不全。建议以 Horiuchi (2010) 为准（待核）。

### 4.4 需要你决策（2 条）

- **L13（dx 作为余切空间基向量）**：这句是数学定义，不是史学论断。按规范 R7，教材/教科书属 `F`。**已按决定处置**：改写为说明句并降为 `F`，见 §7.1。
- **L15（拉格朗日幂级数假设的失败）**：走 `S`，用史学叙述。**已按决定处置**：引 Grabiner 1983, p. 192，见 §7.1。

## 5. 按邮箱申请文献传递的建议清单

优先级从高到低（先补论证链主干，再补背景）：

1. Hall 1980（L07–L09，优先权之争三段事实）
2. Guicciardini 1999（L05，牛顿首末比）
3. Plofker 2009 + Joseph 2009（L02，喀拉拉）
4. Boyer 1959 + Edwards 1979（L11、L15，伯努利与拉格朗日）
5. Enros 1983（L23–L24，剑桥分析学会）
6. Belhoste 1991 或 Grattan-Guinness 1990（L25，柯西与工程师教育）
7. Hawkins 2000（L14，嘉当）
8. Sagan 1994（L26，空间填充曲线）
9. Kennedy 1980（L18，皮亚诺记号）
10. Rashed 1994（L28，花拉子米）
11. 中文与外文汉学：Needham *SCC* Vol. 3 或郭书春《中国科学技术史·数学卷》（L01）、郭世荣/魏雪刚综述与钱宝琮《中国数学史》（L27）、Horiuchi 2010（L29）

申请时建议注明：**只用于学术引用核对，需要包含指定页码的扫描件**；书目信息以本文件 §3 为准，若馆藏版本不同，以能覆盖对应段落的版次为准。

## 6. 未做的事与风险

- 第一轮未改任何语料标记与正文；第二轮（2026-11-16）按确认处置改了 6 处，见 §7，其余 23 条仍为「待补」。
- 未用「疑似相关」充数：§4.2 的 15 条在拿到正文前**不能**直接回填；已取得全文的 7 条里有 3 条核对后判定不支持原句，同样保持待补（§7.2）。
- 知网、维普全文均需登录；只到题录层。
- 部分中文文献的作者/年期来自转载页，标为「线索不足」，需在申请前用馆藏目录核实。
- `Fraser & Dauben` 那篇（最贴 L21）链接已失效，若申请不到 arXiv 版，可改引其正式发表版。

## 7. 2026-11-16 回填记录

### 7.1 已回填（6 处）

| 条目 | 行 | 处置 | 依据与核对点 |
|---|---|---|---|
| L04 巴罗/格雷戈里 | 185 | `S` 待补 → `S` Nauenberg 2011 | arXiv:1111.6145 p. 1：Barrow《Lectiones geometricae》(1670) Lect. X, Prop. 11 已给出基本定理的几何形式证明；注 3 指出 James Gregory《Geometriae pars universalis》(1668) Prop. VI 有类似几何证明。与「几何形式在巴罗那里已明确、格雷戈里也有接近表述」直接对应 |
| L12 柯西的 $dx$ | 299 | `S` 待补 → `S` Grabiner 1978 | *Historia Mathematica* 5, pp. 382–383：p. 383 引柯西 1823 原文，$\Delta x=i$ 同时趋于零时差商「converge toward another limit」，支撑「$dx$ 是趋于零的变量、$dy/dx$ 是比的极限」 |
| L13 余切空间基向量 | 304 | 正文改写 + `S` → `F` | 句子改为「用现代微分几何的语言说，$dx$…可视为…」，等级按 R7 定为 `F`（现代微分几何教材的标准表述，Spivak 1965, ch. 4）。保留其解释作用，不再要求原始/研究文献 |
| L15 拉格朗日幂级数假设 | 410 | `S` 待补 → `S` Grabiner 1983 | *Amer. Math. Monthly* 90, p. 192：明确叙述拉格朗日「假定任何函数都有唯一的幂级数展开」，并指出该假设后来被反例推翻。属史学二手研究（`S`）；Edwards/Boyer 未取得正文，故用已核对的 Grabiner |
| L16 柯西的无穷小定义 | 431 | `S` 待补 → `S` Grabiner 1978 | 同刊 p. 382：转述柯西把「无穷小」定义为极限为零的变量（引 Cauchy 1821, p. 19），与「变量、绝对值可小于任意给定正数」对应 |
| L17 ε-δ 的静态性 | 462 | `S` 待补 → `S` Grabiner 1983 | p. 185：严格化建立在「不等式的代数」上，ε-δ 是可逐字检验的静态表述，不含「趋于」的运动隐喻 |

### 7.2 核对不上、保持待补（4 条）

- **L03 费马「不等式夹逼」**：RHM 2008 全篇只讨论费马 1644 年已给出高于抛物线与双曲线的求积，证明细节指向 Mahoney 1994, pp. 245–254；文章没有「基于不等式的夹逼论证」这类叙述。不能因「都讲费马求积」就回填。
- **L21 鲁滨逊「rehabilitation」**：arXiv:2210.14504 支持前半句（不证明历史上的无穷小为真，而是另造模型，并批评把现代概念读回过去），但没有「鲁滨逊自称 rehabilitation」的依据；Fraser & Dauben 链接失效、Robinson 1966 原书未取得。整句缺后半句支撑。
- **L22 柯西倾向「连续蕴涵可导」**：Grabiner 1983 与 1978 都没有讨论这一点；该说法出自 Grabiner 1981 书（未获取正文）。
- **L06 莱布尼茨 1684**：本轮 `archive.org` 与 `web.archive.org` 均超时（curl 返回 000），没能取到 `s1id13206500` 的 p. 467 影像；上一轮「可自取」的判断本轮无法复核。建议你在能访问该站的网络里自取，或并入文献传递。

### 7.3 计数

| 指标 | 回填前 | 回填后 |
|---|---|---|
| mathlint error | 0 | 0 |
| mathlint warn | 227 | 221 |
| `LOCATOR_PLACEHOLDER` | 29 | 23 |
| `MISSING_TAG` | 178 | 178 |
| `LOCATOR_NO_LOCATION` | 17 | 17 |
| `GRADE_SOURCE_WEAK` | 3 | 3 |
| 单测（含错题池 17+5 条） | 68 通过 | 68 通过 |
| `selfcheck.py` | 4/4 PASS | 4/4 PASS |

只减少 6 条 `LOCATOR_PLACEHOLDER`，没有新增任何检查项；`F` 标记未触发新告警（R7「`F` 须同时给出 A 或 S」这一条工具尚未实现自动判定）。

### 7.4 剩余 23 条

15 条需文献传递（§4.2）+ 4 条仅线索（§4.3）+ 3 条已取得全文但核对不上（L03、L21、L22）+ 1 条未取到原页（L06）。
