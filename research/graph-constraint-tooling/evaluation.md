# 边约束外包给图论/图数据工具：可行性评估

评估对象：`mathhist-toolkit` 的边模型（`spec/object-model.md` §4–§5）与现有校验设施。
结论先行：**三类需求里，只有"端点白名单"能被现成工具低成本接管；"边属性"本来就是普通属性；"平行边各有条件"和"成环/互斥/权重归一"在任何候选方案里都要落到自定义查询或代码。因此彻底迁移不划算，值得做的是把 §5.6 改成"单一表格源 + 域值式校验器"，SHACL 只作为可选的标准导出层。**

评估日期：2026-11-23。文中标 unknown 的项为未取得官方文档或规范原文，未凭印象补全。

---

## 0. 现状核实（先纠正几处与提问描述不同的地方）

1. **`tools/` 下没有图校验器，也没有 loader。** 现有代码只有 `tools/mathlint/`（校验 Markdown 语料里的引文标签）与 `tools/audit/`（对"证据分级有限域"做组合分析）。§5.6 目前是**纯文档约束**，`docs/`、CI、`selfcheck.py` 都不校验 `graph.json`。`graph.schema.json` 的 description 自己也写明："JSON Schema 只能校验单条边的形状；端点是否存在、类型是否匹配、是否成环、权重是否归一等跨对象约束需由校验脚本执行（§5.6）"。所以"改三处"实际是**文档 §5.2 + 文档 §5.6 + schema 枚举**，校验器这一处至今是空缺——加边类型时没有第四处要改，但真正跑校验时必然要补。
2. **规模实测**：三个样板图分别 51 节点/80 边、58/102、63/94。距"数千节点"还差两个数量级，但结构已定型，足以做规模外推。
3. **§5.6 的实际体量**：端点表 31 行，"明确禁止"列按分号/顿号切分共 **51 条子句**；另有 12 条全局不变量（B 段）。
4. 文档 §11 明写："新增边类型：必须同时更新 §5.2 表、§5.6 约束表与 `graph.schema.json` 的 `type` 枚举；三处缺一即视为未登记。"

---

## 1. 候选方案逐项核实

评价口径固定为三问：**(a) 端点白名单**（from/to 只能是某几类节点）；**(b) 边属性**（时间区间、证据等级、confidence、source）；**(c) 平行边**（同一对实体多条边、每条各自有证据）。外加：违例说明是否可读、加类型的成本。

### 1.1 W3C SHACL（已实测，pyshacl 0.40.2 + rdflib 7.6.0）

**规范依据**：W3C Recommendation，2017-07-20。核心组件含 `sh:class`、`sh:in`、`sh:minCount/maxCount`、`sh:node`、`sh:or`、`sh:closed`、`sh:qualifiedValueShape/qualifiedMinCount/qualifiedMaxCount`；形状级 `sh:severity`、`sh:message`、`sh:deactivated`；验证报告字段固定为 `sh:focusNode`、`sh:resultPath`、`sh:value`、`sh:sourceShape`、`sh:sourceConstraintComponent`、`sh:resultMessage`、`sh:resultSeverity`；扩展部分 SHACL-SPARQL 允许在形状内写 SPARQL 约束（`sh:sparql`），消息里可嵌 `{?var}` 占位符。

**(a) 端点白名单：可以，写法比预期短。** 把边重化为节点后，用**序列路径**直接查"from 端点的类型值"：

```turtle
sh:property [ sh:path ( mh:from mh:nodeType ) ; sh:in ( "branch" ) ;
              sh:message "parent_of 的 from 必须是 branch" ] .
```

实测违例输出：

```
Violation | parent_of 的 from 必须是 branch | focus=urn:mh:edge:80 value=concept
```

`value` 就是实际类型 `concept`，读者不需要再跳去查节点。这比"枚举式硬表报一句不允许"好一档。

**(b) 边属性：可以，且是 SHACL 的强项。** 时间/等级/置信度就是边上属性；跨字段联动（`attestation=textbook_simplification` ⇒ `grade∈{F,U}`）用 `sh:sparql` 实测能命中，消息可带变量："attestation=textbook_simplification 时 grade 上限不满足：实得 S"。

**(c) 平行边：部分可以。** "每条平行边各自要有 time/source/grade/confidence" = 每条边节点的 `minCount 1`，Core 直接表达。"不能有两条完全相同的边" 用 SPARQL（实测可命中）。但**"同一对实体至多/至少几条"这类跨边计数，Core 做不到**（`sh:maxCount` 数的是某个节点的属性值，不是图上同对端点之间的边数）；`sh:qualifiedValueShape` 也只能在同一节点的属性值集合里挑子集。

**Core 覆盖不到的，实测清单**（全部改写成 `sh:sparql` 后可用）：

| §5.6 约束 | 为什么 Core 不够 | 实测是否命中 |
|---|---|---|
| `generalizes` 同型（CO→CO / TH→TH） | 要比较 from、to 两个端点的类型 | 是（消息带 `from=concept to=theorem`） |
| 同一对 BR 的 `parent_of` 与 `cross_class` 互斥 | 两个边节点的端点相同 | 是（两条边各报一次，消息带两端 ID） |
| `depends_on` 无环 | 路径上要过滤边类型 | 是（消息带"TH:cauchy-theorem 经 3 条 depends_on 回到自身"；计数用 `COUNT` 近似，语义不精确） |
| 对称边只存一条、from 取字典序小者 | 比较两个端点字符串 | 是 |
| `witness_of` 每个 TW 恰好一条 | 反向边要么过滤类型，要么物化捷径谓词 | 是（物化 `mh:isWitnessOf` 后 Core 的 min/maxCount 即可） |
| `parent_of` 权重和 = 1.00 | 聚合计算 | 需 SPARQL 聚合或代码；本轮形状集未含 |

**结论**：SHACL 能表达全部三类需求，但**约 1/3 的规则要写成嵌在形状里的 SPARQL**，且无环这类规则在没有"物化捷径谓词"时写不出来（SPARQL 1.1 属性路径不能按边类型过滤）。这不是 SHACL 独有的缺陷——下面每个方案在这一层都要付出同样的代价。

**违例说明质量：本报告候选里最好。** 结构化报告、严重级、可在规则上写文案、SPARQL 规则可插值。实测 6 个定点破坏全部命中，见附录 `pyshacl-mutations.txt`。

### 1.2 ShEx 2.1

规范为 W3C Community Group Final Report（2019-10-08），不是 W3C Recommendation。语法比 SHACL 紧凑（ShExC），验证结果表是 `node | shape | result | reason` 四列，`reason` 是失败原因。表达能力与 SHACL 同级同限：作用在 RDF 上，跨边计数/成环同样要靠扩展或外部代码；工具生态小于 SHACL（未逐项核实各实现的消息质量，**unknown**）。取舍：写起来更短，读文档和找实现的人更少。对本项目不构成优于 SHACL 的理由。

### 1.3 PG-Schema（属性图模式语言）

**这是什么**：SIGMOD 2023 最佳工业论文提出的属性图 schema 形式化，含 PG-Types（节点/边类型、多继承）与 PG-Keys（完整性约束），有形式语义；论文明确说它被用作 GQL 标准第二版 DDL 的基础。**这几乎就是本项目 §5.2/§5.6 想做的东西的理论版**——"边的源/目标类型 + 键约束"。

**但它是规范，不是工具**：本轮检索只找到学术原型（CEUR Vol-4303 的 *PG-Schema with Property Constraints validator in Rudof*，集成在 RDF 工具 rudof 里的一个 crate）。该论文 PDF 抓取为空，**原型的约束覆盖范围、报错格式均 unknown**。没有主流图库把 PG-Schema 当运行时约束语言实现。

**对项目的价值**：拿它的术语校准我们的设计（见 §4 的域值式重述），**不引入它的软件**。

### 1.4 GQL / SQL-PGQ（图模式标准）

- GQL：ISO/IEC 39075:2024，第 1 版 2024-04 发布，定位是图数据库语言（数据定义 + 查询）。schema/DDL 的丰富化被安排在后续版本（PG-Schema 论文自述其目标即为此）。各产品对 GQL 的符合度、以及"加载时是否按类型拒绝边"，**unknown**，本轮未核实到可依赖的实现清单。
- SQL/PGQ：ISO/IEC 9075-16:2023，第 1 版 2023-06。图是**定义在表之上的视图**，因此完整性仍由底层 SQL 约束（外键、CHECK）承担；标准本身不新增"图级"约束语言。具体产品支持情况 **unknown**。

**判断**：两者都是**查询/定义语言**，不是验证器。除非将来要跟外部图库交换数据，否则对"加一类边要改几处"没有任何改善。

### 1.5 RDF/OWL 推理与一致性检查

**官方口径**（OWL 2 Primer, W3C REC 2012-12-11）："OWL 2 is not a database framework…"。OWL 是开放世界语义：`maxCardinality 1` 是**推理规则**（推出"若有两个值则它们相等"），不是"发现两个值就报错"；没有唯一命名假设；缺属性不会判错，只会推出更多。因此：

- 端点类型白名单：只能表达为 `rdfs:domain/range`，用途是**推理**，不是校验；写错不会报错。
- 边属性：可做注解，不参与校验。
- 平行边：OWL 没有"边"的概念，多重边要么重化、要么丢失。
- 违例说明：一致性检查只告诉你"本体不一致/某类不可满足"，解释是**推理证明**，不是"第 42 条边的 from 写错了"。

**结论：OWL 解决的是另一个问题（蕴含），不是本项目的（校验）。不推荐。**

### 1.6 主流图数据库自带约束

- **Neo4j**：官方约束清单只有四类——属性唯一、属性存在、属性类型、key（存在+唯一）；后三类为 Enterprise 版。**没有"关系两端节点类型"约束**：关系只有类型名，端点不受限。要表达端点白名单只能写触发器/应用层代码，等于把校验器搬进服务端。另需服务端进程 + 数据导入。
- **TigerGraph**：`CREATE EDGE` 必须声明源顶点类与目标顶点类，**这是真正内建的端点白名单**；违规在加载时被拒。代价：GSQL 服务端、专有生态、错误信息是加载器口径而非领域口径（"哪条边违反哪条史学规则"要自己再包一层）。规模 10³ 节点属于"用不上的重装备"。
- **TypeDB**：关系类型的角色玩家与基数约束在设计上贴近本项目需求，但官方文档页本轮未取到（404），**具体能力与报错质量 unknown**；且同样是服务端方案。
- **嵌入式图库 Kuzu**：`CREATE REL TABLE ... FROM A TO B` 有端点类型，嵌入式无服务端，本来是"最省事"的候选；但官方仓库已公告**归档**（2025，仓库首页公告原文："We are archiving the KuzuDB project"），后续维护是社区分叉。**不建议新项目依赖。**

**共性**：图库的约束是"入库时拒绝"，适合以库为唯一真源的系统。本项目真源是 JSON 文档、边带史学证据、需要"说清为什么"，图库给的是事务级错误码，不是解释。

### 1.7 用图查询语言写"违例查询"

Cypher / GQL / SPARQL 都能把每条规则写成一条"找出违规行"的查询，列名就是解释字段：

```sparql
SELECT ?e ?t WHERE {
  ?e mh:edgeType "parent_of" ; mh:from/mh:nodeType ?t .
  FILTER (?t != "branch")
}
```

- 优点：不需要新概念，规则即查询，输出可控。
- 缺点：没有形状复用、严重级、报告结构；规则之间不共享"端点是类型"的抽象；要么跑图库（Cypher），要么跑 RDF（SPARQL，可用 rdflib 在内存里跑，无需服务端）。
- 实质：这就是"把 Python 校验器换成 SPARQL"，收益是模式语法，成本是两套数据表示。

### 1.8 补充候选：单源 schema 生成（LinkML）

LinkML 用一份 YAML 描述模型，可生成 JSON Schema、SHACL、ShEx、SPARQL 约束、SQL，并带 `linkml.validator`（官方文档 "Data Validation" 页列出上述策略）。它直接命中痛点①（改一处、生成多处），但对痛点②③没有新增能力：跨对象不变量仍要自己写，且引入了较大的工具链依赖。**作为"生成器"思路值得借鉴，作为依赖不建议现在引入。**

### 1.9 现有 JSON Schema 的边界（作为基线）

`graph.schema.json` 是 JSON Schema draft 2020-12：只能约束单条边自身的形状，跨对象（端点存在、类型匹配、成环、权重和）一律做不到；标准里也**没有**错误消息关键字（`errorMessage` 是 ajv 扩展）。这解释了为什么 §5.6 必须另写脚本——不是选型问题，是 JSON Schema 的定位问题。

---

## 2. 候选对照表

| 方案 | 端点白名单 | 边属性（时间/等级） | 平行边各有条件 | 跨边规则（成环/互斥/权重） | 违例说明质量 | 加一类边的成本 | 迁移代价 | 需要服务端 |
|---|---|---|---|---|---|---|---|---|
| 现状：JSON Schema + 文档 | 否（仅形状） | 是（单边内） | 否 | 否 | 无（无校验器） | **3 处**（§5.2、§5.6、枚举） | 0 | 否 |
| 表格驱动 + 域值校验器（本报告推荐） | 是（签名表） | 是 | 是（属性必填 + 键唯一） | 是（约 60 行代码） | 好：模板可插"期望/实得" | **1 处 1 行** | 极低（不动存储） | 否 |
| SHACL（pyshacl） | 是（序列路径 + `sh:in`） | 是 | 部分（每条边属性可必填；同对计数不可） | 部分（须 `sh:sparql` + 捷径谓词） | 最好（标准报告 + 占位符） | 1 处，但每类 8–12 行 + 保持 RDF 映射 | 中：+75 行转换器、双表示、ID 回映射 | 否（库） |
| ShEx 2.1 | 是 | 是 | 同上 | 同上 | 有 `reason` 字段，细节 unknown | 同上 | 同上 | 否 |
| PG-Schema | 是（形式语义） | 是（属性约束论文版） | 是（键） | 形式上有，工具 unknown | unknown | 规范层 1 处 | 高（无生产实现） | — |
| GQL / SQL-PGQ | 是（DDL 声明） | 是 | 是（表约束） | 依赖产品 | unknown | 1 处但受产品限制 | 高（换存储/换语言） | 视产品 |
| OWL 2 + reasoner | 否（推理，非校验） | 注解 | 否 | 否 | 差（一致性证明） | 1 处 | 高（RDF/本体） | 否（库） |
| Neo4j | **否**（无端点约束） | 是 | 是 | 触发器自写 | 事务错误码 | 1 处 + 代码 | 高（服务端 + 导入） | **是** |
| TigerGraph | 是（`CREATE EDGE` 声明端点） | 是 | 是 | 部分 | 加载器口径 | 1 处 | 高 | **是** |
| TypeDB | 是（角色玩家） | 是 | 是 | 部分 | unknown | 1 处 | 高 | **是** |
| Kuzu（已归档） | 是（`REL TABLE ... FROM/TO`） | 是 | 是 | 部分 | 库错误 | 1 处 | 中 | 否 |
| 图查询写违例 | 是（查询） | 是 | 是（查询） | 是（查询） | 自定列 | 每类 1 条查询 | 中 | Cypher 需服务端 |

---

## 3. "加一类边"的成本，最低能到多少

**最低：1 处、1 行。** 前提是把 §5.2 的表格变成机器可读的**单一真源**（例如 `spec/framework/edge-types.yaml`），其余三件产物由它生成：

| 产物 | 生成方式 |
|---|---|
| `graph.schema.json` 的 `type` 枚举与 `if/then` 分支 | 生成脚本写入固定标记块，CI 检查"生成物与源一致" |
| `object-model.md` §5.2 / §5.6 的表格 | 同上，文档里保留"本表由 … 生成"注释 |
| `tools/graphlint/` 校验器 | 直接读该表，不再有第二份规则 |

加一类边 = 在 YAML 里加一行签名（`type`、`from`、`to`、是否同型、是否对称、是否无环、专属属性、消息模板），跑一次生成。实测原型（附录 `domain-range-prototype.py`，150 行含 31 条签名）已能覆盖 §5.6 的 A 段全部类型检查与 7 类不变量。

对比：
- 现状：3 处，且其中两处是手写 Markdown 表格，容易与枚举不一致（§11 的"三处缺一即未登记"说明作者已经预见到漂移）。
- SHACL：形状本身就是规则，schema 枚举可省，但每类边 8–12 行 Turtle，且多了一个必须同步的"JSON↔RDF"表示层。等价成本约 1.5 处。
- 图数据库：schema DDL 1 处，但换来服务端、导入管道、事务错误信息，不符合"10³ 节点 + JSON 真源"。

---

## 4. 迁移代价

### 4.1 存储要不要改

**不用。** 三种路线都可以保留 `{nodes, edges}` JSON：

| 路线 | 需要新增 | 需要改现有数据 | 需要数据库 |
|---|---|---|---|
| 表格驱动校验 | 1 张 YAML + 1 个校验器 + 生成脚本 | 无 | 无 |
| SHACL（JSON 为真源，RDF 为派生） | 转换器（实测 75 行）+ shapes + pyshacl | 无 | 无（内存 rdflib） |
| 引入图库 | 导入器 + 双向同步 | 需要迁移 | 需要 |

### 4.2 校验器能不能"整体替换"

不能干净替换，三个原因都有实测依据：

1. **跨边规则仍是代码/查询。** SHACL Core 拿不到"同一对端点之间的边数"和"路径上的边类型"，这几条就得写成 SPARQL；无环还要先把边物化成"节点→节点"的捷径谓词（实测 `mh:depNext`）。
2. **错误要回指原始 JSON。** RDF 侧的 `urn:mh:edge:80` 是按序号生成的；要稳定回映射，得把边 ID 转义成 IRI 并保留映射表，否则报告里的定位对不上 `edges[]` 的下标。
3. **§5.6 有一部分本来就不是图约束**：`grade` 与 `attestation` 的上限联动、`U` 必带 `note`、`confidence<0.5 ⇒ U`、`text_ref` 锚点存在性、`claims[].source.text` 必须指向图内 `TX:`。这些是**字段联动**，JSON Schema 或几行 Python 更直接；塞进 SHACL 反而绕。

### 4.3 规模与性能

实测（pyshacl 0.40.2 + rdflib 7.6.0，本报告形状集，含 RDF 解析）：

| 节点 | 边 | JSON→RDF | 校验耗时 |
|---|---|---|---|
| 51 | 80 | 0.01 s | 1.5 s |
| 1 020 | 1 600 | 0.20 s | 34 s |
| 3 060 | 4 800 | 0.73 s | 114 s |
| 5 100 | 8 000 | 1.54 s | 194 s |

即约 **24 ms/边**、近似线性（高常数），主要开销在 6 条 SPARQL 形状的逐边求值；重复边检查是 O(n²)，边数再上一个量级会转为超线性。102 条边转出 1746 个三元组（≈17 三元组/边，含节点三元组）。

结论：本项目规模"能跑"，但 5 000 边约 2 分钟，不适合 pre-commit；放 CI 可接受。相较之下，域值式 Python 校验器在两个样板图上是毫秒级。就本项目规模而言，**任何服务端方案都不值**：Neo4j/TigerGraph/TypeDB 要守护进程、要导入管道、要备份策略，换来的约束能力不比 150 行 Python 多，而且更慢。

---

## 5. 图论视角重述现有约束（示范）

现有模型用一句话概括是：**带属性的异质有向多重图**（heterogeneous attributed directed multigraph），边类型是关系符号，每个符号有定义域与值域。

### 5.1 把 §5.6 的 A 表改成签名

以四条为例（原文 → 签名式）：

| 边 | 原文（§5.6） | 签名式 | 由签名自动排除 | 仍需单列 |
|---|---|---|---|---|
| `parent_of` | from BR；to BR；禁止"任何非 BR 端点；自环；成环" | `parent_of ⊆ BR × BR`，属性 `weight∈(0,1]`、`kind∈{taxonomic,historical,institutional}` | 非 BR 端点（含 PE/TX/CO…） | 自环、成环、入边权重和=1 |
| `concerns` | from BR；to CO/TH/PR/TY/TX；禁止"从 CO/TH 出发；指向 PE/EV/TP" | `concerns ⊆ BR × {CO,TH,PR,TY,TX}` | 从 CO/TH 出发、指向 PE/EV/TP **全部** | — |
| `generalizes` | CO/TH；同类型；禁止"CO→TH、TH→CO 混类型" | `generalizes ⊆ (CO∪TH) × (CO∪TH)`，同型 | 跨类型 | 同型（一条全局规则） |
| `supports` | TW/TX → 任意；禁止"从 FA/ST/TP 出发" | `supports ⊆ {TW,TX} × (V ∖ {FA,ST,TP})` | 从 FA/ST/TP 出发 | 目标集是否该排除 `TP` 需确认（现文 B.12 已排除） |

### 5.2 例外数怎么收敛

我对"明确禁止"列的 51 条子句逐条归类：

| 类别 | 条数 | 说明 |
|---|---|---|
| 由 from/to 集合直接推出 | **22** | "从 X 出发""指向 Y"两种句式；签名写对就自动成立，永不需要再写 |
| 自环（非自反） | 4 | `parent_of`、`reformulates`、`spawned`、`contradicts` |
| 成环（无环） | 7 | 7 种关系共享一条"该关系子图无环"规则 |
| 同型/跨类型 | 3 | `generalizes`、`competes_with`、`supersedes` |
| 对称属性 + 只存一条 | 3 | `contradicts`、`competes_with` |
| 互斥对 | 2 | `parent_of`×`cross_class`、`parent_of`×`prerequisite_of`（同对反向） |
| 反向写法约定 | 5 | 由签名方向天然限定，不需要独立规则 |
| 条件属性必填 | 3 | `parent_of.weight/kind`、`contributed_to.role`、`denotes.time` |
| 不可机器判的语义提示 | 2 | "当作 resolves 使用"、"TP 发出非 anchors 的边"（后者已被签名覆盖） |

结果：**51 条具体禁令 → 31 行签名 + 7 类不变量**。篇幅上，§5.6 A 表 31 行×4 列约 2.4 千字，重述后约 31×1 行签名（每行 ≤20 字）+ 7 行不变量，同一信息量的规则文本减少一半以上，且**新增一类边时只需要写一行签名**，不必再想"要禁止哪些组合"。

### 5.3 三个结构概念的澄清

1. **多重边 vs 简单图。** 现在允许同一 `from/type/to` 多条边、用 `#n` 区分——这就是多重图的边标识 `(from,type,to,index)`。推论：**不要**用"同对端点边数 ≤1"的约束；平行边的合法性应表达为"每条边的证据字段完整 + 不存在完全重复的边（同 from/type/to/time）"。SHACL 的 `sh:maxCount` 查节点属性，不要误用在这里。
2. **跨类归属不是类型问题。** `cross_class` 是 BR 之间的一种关系，与"节点属于多个类"无关（后者是 `branch.view_classes` 数组）。把它写成边是对的；错的是**它与 `parent_of` 互斥**这条规则——它是建模政策，不是类型约束，而且已经造成过实际冲突（`research/ackermann-1928/ontology.md` 记录：同一批对象需要三处归属，被 §5.6 的互斥卡住）。建议把互斥降级为**警告并要求 `note`**，而不是硬失败；硬失败会逼人隐藏真实关系。
3. **观点节点是"边的重化"，不是新类型。** `ST:` 节点 + `about`/`claimed_in` 本质是把"谁在何时主张了什么"从边属性提升为节点——这是**按需重化**。RDF 的代价恰恰在于它对**所有**边都强制重化（否则边不能带属性）；本模型只在认识论上需要时才重化。这一条是"不要全面迁到 RDF"的结构性理由，不只是工程口味。

---

## 6. 实测：域值式校验器 vs 枚举式约束

附录 `domain-range-prototype.py`（150 行，其中 31 行是签名表）在三个样板图上跑出的结果是：

- `calculus`、`non-euclidean-geometry`：0 处；
- `group-theory`：**1 处真实违例**——`E:TW:cayley-1854.print>witness_of>TX:cayley-1854` 的 `attestation=textbook_simplification` 却给了 `grade=S`，违反 §5.6 B.8（该组合上限为 F/U）。

同一处违例在 SHACL 形状集里补一条 `sh:sparql` 后也被命中，消息为"attestation=textbook_simplification 时 grade 上限不满足：实得 S"。**说明：这条违例在任何"跑一遍"的校验里都会暴露，只是现在没有校验器在跑。** 它是本评估里最直接的证据：约束写得再细，不执行等于零。

---

## 7. 推荐

### 路线 A（推荐，先做）：单一真源表 + 域值校验器

1. `spec/framework/edge-types.yaml`：31 行签名（type、from、to、同型、对称、无环、专属属性、消息模板）。
2. `tools/graphlint/`：读该表 → 校验 `{nodes, edges}`。域值式报错，例如
   `[E:…] concerns 的 to 值域是 {CO,TH,PR,TY,TX}，实得 PE:abel（person）`。
3. 生成：`graph.schema.json` 的枚举/分支、`object-model.md` §5.2/§5.6 的表格；CI 校验"生成物与源同步"。
4. 顺带修正：把 `parent_of`×`cross_class` 互斥降为警告；把三条样板图纳入 CI（现在它们连 JSON Schema 都没跑过）。
5. 预期效果：加边类型 = 1 行；违例说明带"期望集/实得值/所在端点"；无需数据库、无需运行时。

代价估计：新增约 200–250 行代码 + 一张表；不动存储、不动 loader 设计。

### 路线 B（可选，后做）：从同一张表生成 SHACL，作为"标准导出层"

适用条件：需要与外部工具交换 RDF、需要标准验证报告、或将来要接图查询。做法是保留 JSON 为真源，用同一张 YAML 生成 shapes（或直接由 `graphlint` 导出），pyshacl 只做二次校验。**不要让 shapes 成为第二份真源**，否则就回到"改两处"。

不选 SHACL 作为唯一方案的理由：约 1/3 规则要写 SPARQL、成环要求物化捷径谓词、错误要回映射 JSON、且多一层表示。它换来的是标准报告与生态，这对一个单人维护的史学数据集是可选而非必需。

### 明确不推荐

| 方案 | 不推荐的具体理由 |
|---|---|
| **OWL 2 + reasoner** | 开放世界语义：约束被解释成推理规则，缺数据不报错，写错端点类型也推不出矛盾；一致性检查给出的是本体证明，不是"第几条边错在哪"。解决的是蕴含问题，不是校验问题。 |
| **Neo4j** | 官方约束只有唯一/存在/类型/key，**没有关系端点类型约束**，白名单要写触发器，等于把校验搬进服务端；且存在/类型/key 为 Enterprise 版。10³ 节点上纯属增加运维面。 |
| **TigerGraph / TypeDB** | 端点白名单确实是内建能力，但都要服务端、专有加载流程，错误是引擎口径；本项目真源是带史学证据的 JSON，需要的是解释而非事务拒绝。 |
| **Kuzu** | 嵌入式 + `REL TABLE FROM/TO` 本来最贴合，但官方仓库已公告归档，下游是社区分叉，不适合作为新依赖。 |
| **PG-Schema / GQL / SQL-PGQ 作为运行时** | 规范层面完全对路（尤其 PG-Schema 的 PG-Types/PG-Keys），但没有可依赖的生产实现（PG-Schema 原型在 rudof 内，能力 unknown）；GQL/SQL-PGQ 是查询与 DDL 标准，校验能力取决于产品。**可以借术语，不要借软件。** |
| **引入图数据库/服务端** | 数千节点、JSON 真源、离线单机：任何需要守护进程、导入管道、备份与版本的方案，收益（端点白名单）已被 150 行校验器覆盖，成本不成比例。 |
| **LinkML 全量引入** | 思路（单源生成多产物）正确，但工具链依赖大；同样解决不了跨对象不变量与消息质量。除非将来要同时输出 JSON Schema/SHACL/OWL/文档四种产物，否则不值得。 |

---

## 8. unknown 清单（未核实，不作为结论依据）

1. PG-Schema + property constraints 原型（rudof crate）的约束覆盖、报告格式（CEUR 论文全文抓取为空）。
2. GQL 首版对 schema DDL 的实际覆盖，以及任何产品对"加载时端点类型校验"的符合度。
3. SQL/PGQ 的产品实现清单与约束能力。
4. TypeDB 3.x 的角色/基数约束细节与错误消息（官方文档页 404）。
5. ShEx 各实现的消息质量差异。
6. JSON Schema 2020-12 无标准错误消息关键字（依规范现状判断；未逐字引用规范原文）。
7. 边数上万（>1 万）时本形状集的耗时（已测到 8 000 边 194 s，未继续外推）。

---

## 附录：实验文件与复现

| 文件 | 内容 |
|---|---|
| `appendix/to-rdf-prototype.py` | JSON → RDF 转换（75 行），边重化 + 捷径谓词物化 |
| `appendix/shacl-shapes.ttl` | 覆盖端点白名单、边信封、同型、互斥、无环、对称、重复边、等级联动的形状集（约 120 行） |
| `appendix/pyshacl-run.txt` | 三个样板图的原样运行结果（含真实违例 1 处） |
| `appendix/pyshacl-mutations.txt` | 6 个定点破坏的命中结果与消息文本 |
| `appendix/domain-range-prototype.py` | 域值式校验器（150 行，31 行签名表 + 7 类不变量） |
| `appendix/scale-test.txt` | 80 → 8 000 边的耗时曲线 |

复现：`pip install pyshacl`（实测 0.40.2，rdflib 7.6.0），Python 3.11+；无需数据库或网络。

## 参考

- SHACL: <https://www.w3.org/TR/shacl/>（W3C REC 2017-07-20；§2.1.4 严重级、§2.1.5 消息、§3.6 验证报告、§4.7.3 qualifiedValueShape、§5–6 SPARQL）
- ShEx 2.1: <https://shex.io/shex-semantics/>（CG Final Report 2019-10-08，验证结果含 reason 列）
- OWL 2 Primer: <https://www.w3.org/TR/owl2-primer/>（W3C REC 2012-12-11，"OWL 2 is not a database framework"）
- PG-Schema: <https://arxiv.org/abs/2211.10962>（SIGMOD 2023）；rudof 原型：CEUR-WS Vol-4303, *PG-Schema with Property Constraints validator in Rudof*
- GQL: ISO/IEC 39075:2024（2024-04）
- SQL/PGQ: ISO/IEC 9075-16:2023（2023-06）
- Neo4j 约束清单: <https://neo4j.com/docs/cypher-manual/current/constraints/>
- TigerGraph schema（`CREATE EDGE` 声明源/目标顶点类）: <https://cn-doc.graphtiger.com/master/dev/gsql-ref/ddl-and-loading/define_schema>
- Kuzu 归档公告: <https://github.com/kuzudb/kuzu>
- LinkML 数据校验策略: <https://linkml.io/linkml/data/validating-data.html>
