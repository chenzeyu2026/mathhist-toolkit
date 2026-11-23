# 非欧几何—平行公设：样板的长文本侧

> 配套图包：`non-euclidean-geometry.json`。
> 本文件只放原文引文、论证过程与争议评述；图里只保留 ID 与锚点。
> 图侧用 `text_ref: doc:spec/framework/samples/non-euclidean-geometry.md#<锚点>` 指到这里；
> 本文用 `graph://<节点或边 ID>` 指回图。

## saccheri

萨凯里 1733 年《欧几里得无瑕获释》（*Euclides ab omni naevo vindicatus*）用反证法处理第五公设。
他设"锐角假设"与"钝角假设"，试图从两者推出矛盾。钝角假设较容易被排除；锐角假设下他推出一长串与欧氏几何不同的命题，但未得到逻辑矛盾。

他的关键一步是：以"直线可无限延长/无限长"为由，判定锐角假设不可能。
这一步不是逻辑推导，而是引入了欧氏几何的直觉前提——恰恰是要证明的东西。

图侧：`graph://FA:saccheri-1733`、`graph://PR:fifth-postulate-deducibility`。

## reframing

19 世纪把问题从"证明第五公设"改写为"第五公设是否独立"。
改写不等于解决：原问题要求一个推导，新问题要求一个模型。

图侧：`graph://PR:fifth-postulate-deducibility`、`graph://PR:independence-of-parallel-postulate`、
`graph://E:PR:fifth-postulate-deducibility>reformulates>PR:independence-of-parallel-postulate`。

## beltrami

贝尔特拉米 1868 年在《非欧几何的解释》（*Saggio di interpretazione della geometria non-euclidea*）中，
把双曲平面实现为欧氏空间中的伪球面（常负曲率曲面）。

这一步的作用是**相对一致性**：若欧氏几何无矛盾，则双曲几何也无矛盾。
它没有"证明欧氏几何无矛盾"，也不构成对第五公设的直接推导。

图侧：`graph://TH:non-euclidean-relative-consistency`、`graph://ME:model-construction`、`graph://EV:1868-beltrami-model`。

## gauss-priority

高斯在 1832 年致 F. 鲍耶的信中称，自己三十余年前已得到同样结果，但未发表。
这是一条**主张**，不是一条已核实的发表记录：

- 支持者：信件文本本身，以及高斯其他通信中的旁证；
- 反对者：未刊手稿的独立可核性不足，"先于"只能按写作时间主张，不能按公共知识主张。

图里因此建 `ST:gauss-priority`（`status: contested`），不把它写成 `CO:hyperbolic-geometry` 的首次出现。

图侧：`graph://ST:gauss-priority`、`graph://TX:gauss-letter-1832`。

## notation

罗巴切夫斯基 1829 年用"想象几何"（воображаемая геометрия）称呼他的体系。
克莱因 1871 年在《论所谓非欧几何》（"Ueber die sogenannte Nicht-Euclidische Geometrie"）中
把常负曲率的情形定名为"双曲几何"。

记号层要记的不是"谁对"，而是：同一个概念先后被哪些词指称、各自有效到什么时候、今天标准形式是什么。
中文"非欧几何"的定名文献与更早译法尚未核到，图里标 `U`，不硬填译者与年份。

图侧：`graph://NO:term-imaginary-geometry`、`graph://NO:term-hyperbolic-geometry`、`graph://NO:term-non-euclidean-zh`。

## text-chain

《原本》没有作者手稿存世。现存结构是：

- 希腊文本：晚期抄本 → 海贝格校勘本（Heiberg–Menge, 1883–1888）；
- 阿拉伯—拉丁链：希腊文本 → 阿拉伯译本 → 克拉维乌斯 1574 拉丁本；
- 汉译链：克拉维乌斯拉丁本 → 徐光启、利玛窦《几何原本》1607（前六卷）；
- 英译链：海贝格校勘本 → 希思 1908 英译本。

四条链并行，不是一条直线；每条链的节点各自记年代、编者/译者、馆藏。
辑佚本与传世本并列时，同样建并行链，不合并成一个"版本"。

图侧：`graph://TX:euclid-elements`、`graph://TW:euclid-elements.heiberg-menge`、
`graph://TW:euclid-elements.xu-ricci-1607`、`graph://TW:euclid-elements.heath-1908`。

## four-layers

四层在同一张图上的闭合路径：

```
PR:fifth-postulate-deducibility
  ←targets— FA:saccheri-1733 —uses_method→ ME:proof-by-contradiction
  ←about— ST:saccheri-refutation —claimed_in→ TX:saccheri-1733-euclides
                                              ←witness_of— TW:...print
NO:term-imaginary-geometry —denotes→ CO:hyperbolic-geometry ←— ST:lobachevsky-1829
                                            ↑
                                 TH:non-euclidean-relative-consistency
                                            ↑
                                 TW:beltrami-1868-saggio.print
```

判读规则：任一层的节点若没有连到其他层，就说明该条只是"标签"，不是史实。
