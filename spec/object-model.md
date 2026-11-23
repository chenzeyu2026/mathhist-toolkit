# 数学史对象框架 v0.2：图结构本体（骨架，不填内容）

- 状态：结构定稿，内容待填
- 形态：**图优先**。本体说明负责定义节点、边与约束；实例直接按 `{nodes, edges}` 写，不再以表格为主
- 适用：`mathhist-toolkit` 全部语料、提示词与检索产物
- 证据口径：沿用 [`evidence-tags.md`](evidence-tags.md) 的 A / S / U / F，不另造等级；冲突时以该规范为准
- 机读骨架：`framework/edge-signatures.yaml`（**边签名与不变量的唯一真源**）、`framework/graph.schema.json`、`framework/object-model.schema.json`（节点）、`framework/branches.json`（分支目录）、`framework/samples/`

本文件只定义**节点、边、约束、存储与挂载**，不铺开写 62 个分支的史实内容。长引文、论证过程、争议评述不进图，放文档；图里只留 ID 与 `text_ref` 指针，两边互指。

---

## 0. 一句话设计

**图是本体，分类是视图，观点是节点。**

- 十类 62 分支是**从当代数学分支面向过去划出的区域取景轴**（本项目自建，源于内容分类方案）；它只作 `view_classes` 标签与检索入口，不承担本体结构，也不作史学分期。真正的结构是 `parent_of` / `cross_class` 边。
- 同一事实有多种说法时，不裁成一条边：用**平行边 + 观点节点**，让"谁在什么年代主张哪种说法"在图里可见。
- 每条边都自带时间区间、主张者/来源、证据等级、置信度；不把属性塞进节点冒充关系。
- 分歧不被"平均"掉：两个父类 = 两条 `parent_of` 边，各带权重；两次独立发现 = 两条 `discovered_by` 边，各带时间与文献。

四条贯穿规则：

1. **节点分离**：概念、定理、问题、方法/算法、理论、失败路线、记号/术语、文本见证、观点，各自是独立节点类型，不互相充数。
2. **边即断言**：边不是拓扑装饰，是一条可被质疑的主张，必须能落到来源与等级。
3. **时间可多次**：不用单一 `year`；出现、发现、接受、失效各走各的边，各自带时间窗。
4. **正反都留**：错误证明、被取代理论、未被采纳的路线与正确结论同等建节点，且必须写清"当时为什么被接受"。


---

## 1. 编号规则

ID 一旦分配永不复用；改名只改 `labels`，不改 ID。所有 ID 为 ASCII、小写、连字符，冒号只用于分隔类型前缀。

| 前缀 | 类型 | 形式 | 例 |
|---|---|---|---|
| `BR-` | 分支 | `BR-<类码>-<名>` | `BR-ALG-GRP`、`BR-GEO-NONEU` |
| `CO:` | 概念/对象 | `CO:<slug>` | `CO:group`、`CO:parallel-lines` |
| `TH:` | 定理/命题 | `TH:<slug>` | `TH:lagrange-theorem` |
| `PR:` | 问题 | `PR:<slug>` | `PR:quintic-solvability` |
| `ME:` | 方法/算法/构造 | `ME:<slug>` | `ME:galois-correspondence` |
| `TY:` | 理论/纲领 | `TY:<slug>` | `TY:infinitesimal-calculus-17c` |
| `FA:` | 失败路线 | `FA:<slug>` | `FA:kempe-1879-four-color` |
| `NO:` | 记号/术语 | `NO:<slug>` | `NO:dy-dx`、`NO:term-non-euclidean-zh` |
| `PE:` | 人物 | `PE:<slug>` | `PE:galois` |
| `TX:` | 文本（书目实体） | `TX:<slug>` | `TX:euclid-elements` |
| `TW:` | 文本见证（传承节点） | `TW:<tx-slug>.<节点>` | `TW:euclid-elements.heiberg-menge` |
| `EV:` | 时间线事件 | `EV:<yyyy>-<slug>` | `EV:1829-lobachevsky-kazan` |
| `TP:` | 教学挂点 | `TP:<course>-<chapter>` | `TP:calculus-derivative` |
| `ST:` | 观点/主张（图节点） | `ST:<slug>` | `ST:gauss-priority-claim` |
| `CLM:` | 内嵌断言（兼容保留） | `CLM:<object>.<n>` | `CLM:PR:parallel-postulate.3` |

约束：

- 分支 ID 的类码只表示**首次登记时的视图**，之后跨类不改 ID。
- `TW:` 必须挂在 `TX:` 下；一个 `TX` 可有多条并行链，节点 ID 全局唯一。
- `CLM:` 不作为独立文件存在，只存在于宿主对象的 `claims[]` 中；引用时写宿主 ID + 序号。
- 废弃对象保留记录，`status: deprecated`，并用 `superseded_by` 指向新对象；禁止删除后重用 ID。
- **边 ID 由端点与类型派生**：`E:<from>><type>><to>`。同一 `from/type/to` 出现第二条起加后缀 `#2`、`#3`。不单独发号，避免维护注册表；重命名节点时才需要批量改边 ID。

---

## 2. 对象类型与判定标准

共 14 类。判定用"三问"，避免概念与定理混用。

| 类型 | 它回答什么 | 判定三问（全过才归此类） | 粒度 |
|---|---|---|---|
| 分支 `branch` | 哪个学术共同体/领域 | ① 有相对稳定的研究对象与方法？② 有可指认的从业群体或课程位置？③ 能挂到 62 视图或扩展槽？ | 领域级，一个分支下可容纳数十概念 |
| 概念 `concept` | 是什么、如何定义 | ① 能被定义或刻画？② 本身不主张真假？③ 可被别的对象依赖？ | 单个定义单元；"群"是一个概念，"群论"是分支 |
| 定理 `theorem` | 在什么条件下是否成立 | ① 是可真假判定的陈述？② 有明确前提？③ 有证明状态？ | 单条命题；含引理、推论、不等式 |
| 问题 `problem` | 谁在问什么、解没解决 | ① 是疑问/要求而非陈述？② 能指认提出者或原始表述？③ 有状态（开放/解决/重述/放弃）？ | 一个问题可派生多个子问题 |
| 方法 `method` | 怎么做 | ① 是可按步骤执行或复用的程序？② 有适用对象与正确性依据？③ 可被多次使用？ | 含算法、构造、证明策略、计算技巧 |
| 理论 `theory` | 一套假设加上它的推论体 | ① 有明确的公理/假设集？② 有内部推导体？③ 可被整体接受、修改或取代？ | 比定理大、比分支小的内容单元；"欧氏几何公理系统"是理论，"欧氏几何"也是分支 |
| 失败路线 `failure` | 哪一步错了、当时为何被信 | ① 有可指认的缺陷步骤或错误前提？② 有接受史或纠正史？③ 不属于"尚未证明"？ | 一次具体失败；同一对象的多次失败分开记 |
| 记号/术语 `notation` | 用什么符号/词指称 | ① 是可书写的符号或可发音的词？② 有首次出现或定型时点？③ 可与所指概念分离？ | 一个符号或一个词条；同形异义拆开 |
| 人物 `person` | 谁做的、和谁有关 | ① 是可指认的个人？② 与至少一个对象有归属/纠正/传授关系？③ 不作为纯传记条目使用？ | 归属节点，不写生平轶事 |
| 文本 `text` | 哪本书/哪篇文献 | ① 是独立可引用的书目实体？② 有作者/编者与成书或刊行信息？③ 可拥有见证链？ | 书目级；同一著作的不同版本仍是一个 TX，版本是 TW |
| 见证 `witness` | 这一份实物/版本是什么 | ① 是 TX 的一个具体载体？② 有年代、编者/译者、馆藏或编号？③ 能指向它支撑的对象？ | 载体级；抄本、刻本、校勘本、译本各一个节点 |
| 事件 `event` | 何时何地发生了什么 | ① 有可定位的时间（至少年）？② 有行为者与地点？③ 不是"长期存在"而是离散发生？ | 离散事件；持续性用 `occurrences[]` |
| 教学挂点 `teaching_point` | 挂到课程哪一节、解决什么误会 | ① 能定位到课程/教材/章节？② 有学习目标与常见误解？③ 不主张历史真假？ | 教学单元级，不承担史学论断 |
| 观点 `statement` | 谁在何时主张什么 | ① 是一个可归属的断言？② 有主张者或来源文本？③ 能与被主张的对象分开？ | 一条主张一个节点；长论证放 `text_ref`，不进图 |

**易混边界**：

- 概念 vs 定理：能改写成"若…则…"且可真假判定 → 定理；否则 → 概念。例："群"是概念，"拉格朗日定理"是定理。
- 概念 vs 记号：指称对象 → 概念；书写形式或词形 → 记号。`dy/dx` 是记号，导数概念是 `CO:derivative`；一个记号可先后指称不同概念（见 §8.3）。
- 问题 vs 定理：疑问/要求 → 问题；陈述 → 定理。"五次方程根式可解吗"是问题；"五次方程一般不可根式解"是定理（阿贝尔—鲁菲尼）。
- 观点 vs 定理：`ST:` 是"某人主张 X"，`TH:` 是"X 本身"。同一个 X 可被多人以不同措辞主张，所以一个定理可挂多条 `asserted_by` 边指向不同的 `ST:` 节点。
- 失败 vs 未解：有缺陷步骤或已被取代 → 失败；只是还没证出来 → 问题（`status: open`）。
- 理论 vs 分支：内容假设集 → 理论；人群与领域 → 分支。二者用 `representative_theories` 连接。

---

## 3. 通用信封（所有对象共有）

```json
{
  "id": "PR:parallel-postulate",
  "type": "problem",
  "schema_version": "0.1",
  "labels": {
    "zh": "平行公设",
    "en": "parallel postulate",
    "aliases": ["第五公设", "Euclid's fifth postulate"]
  },
  "status": "active",
  "summary": "一句话说明该对象是什么，不含未标等级的史实判断。",
  "claims": [
    {
      "id": "CLM:PR:parallel-postulate.1",
      "statement": "该问题在欧几里得《原本》中以公设形式出现。",
      "grade": "A",
      "attestation": "direct",
      "source": { "text": "TX:euclid-elements", "witness": "TW:euclid-elements.heiberg-menge", "locator": "Book I, Postulate 5" },
      "note": ""
    }
  ],
  "occurrences": [],
  "text_ref": null,
  "tags": [],
  "provenance": {
    "created_by": "agent",
    "created_at": "2026-11-22",
    "updated_at": "2026-11-22",
    "review": "none",
    "sources_checked": "partial"
  }
}
```

### 3.1 `claim`：历史字段的唯一载体

任何会被人当作史实的字段值，都写成 `claim`，不写裸字符串。

| 字段 | 必填 | 取值 | 说明 |
|---|---|---|---|
| `id` | 是 | `CLM:<宿主>.<n>` | 宿主内唯一、稳定 |
| `statement` | 是 | 字符串 | 一句话，可独立判断真假 |
| `grade` | 是 | `A` / `S` / `U` / `F` | 按 evidence-tags.md 判定 |
| `attestation` | 是 | `direct` / `contemporary_report` / `later_report` / `textbook_simplification` / `unknown` | **本框架新增**，用于区分"原始文献直接记载"与"后世转述/教科书简化" |
| `source` | 是 | `{text, witness?, locator, url?}` | `locator` 必须细到页/节/行/卷期；`U` 时写检索线索 |
| `note` | 否 | 字符串 | 两说并存、译者按语、版本差异 |
| `supports` | 否 | 对象 ID 数组 | 该断言服务于哪些字段（便于反向索引） |

`attestation` 与 `grade` 必须自洽：

| 情形 | grade 上限 | attestation |
|---|---|---|
| 亲见原件或影印，定位到页 | `A` | `direct` |
| 同时代人记录，非作者本人 | `S` | `contemporary_report` |
| 后世研究者的叙述 | `S` | `later_report` |
| 教材/科普/百科的简化 | `F` | `textbook_simplification` |
| 不知道依据哪一份 | `U` | `unknown` |

`U` 必须写原因与下一步（同 R8），例：`locator: "未获原刊；待查 Acta Eruditorum 1684 卷"`。

### 3.2 节点不再内嵌关系

v0.2 起，关系一律写成**顶层 `edges[]`**，节点里不再有 `relations[]`。理由：边要带自己的时间、来源、等级、置信度与权重，塞进节点会变成一条无属性的字符串，无法被质疑。

节点只保留两类东西：

- 自身属性（`labels`、`status`、`definition`、`failure_kind` 等）；
- `claims[]`，节点级断言。

凡"指向另一个对象"的内容（`parents`、`depends_on`、`resolves`、`derived_from` …）都是**投影字段**，由图 loader 生成边；见 §4.0 的字段→边映射表。节点文件被单独阅读时可以保留这些字段做索引，但合并进图后以 `edges[]` 为准，不重复存。

### 3.3 长文本指针 `text_ref`

`text_ref` 是节点或边指向长文本的指针，格式 `doc:<文件>#<锚点>`，例：

```
doc:corpus/01-微积分起源.md#sec-2-2-cavalieri
```

规则：

- 图里不存超过 280 字符的引文；`summary` 也按 280 字符上限写。
- 原文引文、论证过程、争议评述、译名考订放在文档；文档侧用 `graph://<节点或边 ID>` 反指，形成双向指针。
- 没有长文本可指时写 `null`，不要写空字符串或占位符。

### 3.4 时间出现 `occurrence`

```json
{
  "civilization": "古希腊",
  "region": "亚历山大里亚",
  "language": "希腊语",
  "year_from": -300,
  "year_to": -300,
  "precision": "circa",
  "dating_basis": "传统系年",
  "independence": "unknown",
  "independence_note": "缺乏独立传播证据",
  "claims": ["CLM:TX:euclid-elements.1"]
}
```

- `year_from/year_to` 用整数，公元前为负；不确定区间就写区间，不写伪精确单点。
- `precision`：`exact` / `year` / `decade` / `century` / `circa` / `traditional`。
- `independence`：`independent` / `derived` / `contested` / `unknown`。判断"独立出现"必须给证据，不能因为时间早就算独立。
- 同一概念在不同文明/时代出现 → 多条 `occurrences`，`independence` 分别标注。

---

## 4. 各类型字段表

标记：**必** = 必填；**选** = 可选；**条件** = 视状态必填。

### 4.0 投影字段 → 边

下表字段的值是对象 ID 数组。在图形态里它们**不存于节点**，而由 loader 展开为边。保留字段名是为了让单文件样例仍可读，也为了给 loader 一个确定的映射。

| 节点字段 | 展开为边 | 方向处理 | 备注 |
|---|---|---|---|
| `branch.parents[{id,kind}]` | `parent_of` | 父→子 | 两项父 = 两条边，各带 `weight` |
| `branch.cross_class[{view}]` | `cross_class` | 按解析结果 | `view` 解析到分支 ID 才成边；解析到类名则只进 `view_classes` |
| `branch.key_problems/key_texts/representative_theories` | `concerns` | BR→目标 | 索引边，不参与推理 |
| `branch.teaching_hooks` | `anchors` | TP→目标 | 由 TP 侧生成，分支侧不存 |
| `concept.prerequisites` | `depends_on` | 概念→前置 | |
| `concept.generalizes/specializes` | `generalizes` | 一般→特殊 | 只写一边 |
| `concept.notation_refs` | `uses_notation` | 概念→记号 | |
| `concept.introduced_by` | `introduced` | 人物→概念 | |
| `theorem.dependencies` | `depends_on` | 定理→前置 | |
| `theorem.resolves` | `resolves` | 定理→问题 | |
| `theorem.failure_refs` | `targets` | 失败→定理 | 由 `FA` 侧写出 |
| `theorem.proofs[].by` | `proved` | 人物→定理 | 证明细节留在 `claims[]` |
| `problem.related_branches` | `concerns` | 分支→问题 | 反向 |
| `problem.posed_by/posed_in` | `poses` | 提出者→问题 | |
| `problem.resolutions[]` | `resolves` + `uses_method` | 定理/方法→问题 | 两条边 |
| `problem.reframings[]` | `reformulates` | 旧问题→新问题 | |
| `problem.spawned` | `spawned` | 母问题→子问题 | |
| `method.correctness_basis` | `depends_on` | 方法→依据 | |
| `method.applies_to` | `uses_method` | 使用者→方法 | 反向 |
| `theory.core_concepts` | `exemplifies` | 概念→理论 | |
| `theory.signature_results` | `exemplifies` | 定理→理论 | |
| `theory.superseded_by` | `supersedes` | 旧理论→新理论 | |
| `failure.target` | `targets` | 失败→对象 | |
| `failure.corrected_by` | `corrected_by` | 失败→人物 | |
| `failure.correction_event` | `part_of` | 事件→失败 | |
| `failure.acceptance_evidence` | `supports` | 文本/见证→失败 | |
| `notation.denotation[]` | `denotes` | 记号→概念 | 时间窗取 `valid_from/valid_to` |
| `notation.superseded_by` | `supersedes` | 旧记号→新记号 | |
| `notation.zh_term_history[]` | 升格为 `NO:` 节点 | 各自建立 | 每个译名一个节点，见 §7.3 |
| `text.chains[]` | `TW:` 节点 + `witness_of`/`derived_from` | 见 §7.4 | |
| `text.support_claims[]` | `supports` | 文本→对象 | |
| `witness.derived_from` | `derived_from` | 子→母见证 | |
| `witness.supports[]` | `supports` | 见证→对象 | |
| `event.actors` | `participates_in` | 人物→事件 | |
| `event.part_of` | `part_of` | 事件→对象 | |
| `teaching_point.history_objects` | `anchors` | 挂点→对象 | |
| `statement.about` | `about` | 观点→被主张对象 | |
| `statement.claimed_in` | `claimed_in` | 观点→文本/见证/事件 | 见 §5.2 |

**不展开的字段**：`notation.competitors` 里未建节点的竞争写法、`definition`、`proofs[].locator` 等自由文本，留在节点内；它们不是关系。

### 4.1 分支 `branch`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `id` / `labels` | 必 | 见 §1、§3 |
| `view_classes` | 必 | 数组，可多个；取值为十类视图名 + 扩展槽；**这就是"跨类"的呈现方式** |
| `parents` | 必 | 数组，0–3 项，`{id, kind, primary}`；`kind` ∈ `taxonomic` / `historical` / `institutional`；至多一个 `primary: true`；必须无环 |
| `children` | 选 | 由工具反向生成，不手写 |
| `cross_class` | 选 | `{view, relation, note}`；`relation` ∈ `overlaps` / `prerequisite` / `method_source` / `shared_object` |
| `scope_definition` | 必 | 一段，说明边界：什么算、什么不算 |
| `disputes` | 选 | 分类争议数组，`{issue, resolution, status}`；`status` ∈ `resolved` / `open` / `by-design` |
| `representative_theories` | 选 | `TY:` 数组 |
| `key_texts` | 选 | `TX:` 数组 |
| `key_problems` | 选 | `PR:` 数组 |
| `affected_layers` | 必 | `{problem, failure, notation, text}`，每项 `high` / `medium` / `low`，用于挂载表 |
| `teaching_hooks` | 选 | `TP:` 数组 |

### 4.2 概念 `concept`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `definition` | 必 | 现代定义，尽量形式化；不确定就写"教科书常用表述"并标 `F` |
| `definition_source` | 必 | `{text, locator, grade}` |
| `introduced_by` | 选 | `PE:` 数组 + 时间出现 |
| `prerequisites` | 选 | `CO:` / `TH:` 数组（概念前置） |
| `generalizes` / `specializes` | 选 | `CO:` 数组，二者互逆，只写一边 |
| `notation_refs` | 选 | `NO:` 数组 |
| `formal_mapping` | 选 | `{language, expression, note}`，如 Lean/Isabelle 中的对应写法 |
| `occurrences` | 必 | 至少一条；首次出现不等于发明 |
| `teaching_points` | 选 | `TP:` 数组 |
| `status` | 必 | `active` / `historical` / `superseded` / `disputed` |

### 4.3 定理 `theorem`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `statement` | 必 | 自然语言；有形式化版本时给 `formal_statement` |
| `assumptions` | 必 | 条件列表，逐条可检验 |
| `proof_status` | 必 | `proved` / `conjectured` / `disproved` / `invalid` / `unknown` |
| `proofs` | 条件 | `proved` 时至少一条 `{by, year, text, locator, grade}` |
| `counterexamples` | 条件 | `disproved` / `invalid` 时必填，`{description, by, year, source}` |
| `dependencies` | 选 | `{theorems: TH:[] , concepts: CO:[]}`，只指向前置 |
| `resolves` | 选 | `PR:` 数组 |
| `generalizes` / `specializes` | 选 | `TH:` 数组 |
| `failure_refs` | 选 | `FA:` 数组：曾被认为成立但证明有缺陷时，TH 保留，FA 记失败 |
| `namesake_note` | 选 | 命名是否后世追认；是则必须写 |

**规则**：定理被证伪或被判定证明无效时**不删除**，改 `proof_status`，并挂 `FA`。

### 4.4 问题 `problem`（一等对象）

| 字段 | 必/选 | 约束 |
|---|---|---|
| `original_formulation` | 必 | `{text, language, author, year, source{text,locator}, grade, attestation}`；无法找到原始表述时写 `U` 并说明 |
| `problem_kind` | 必 | `solvability` / `existence` / `uniqueness` / `construction` / `classification` / `decidability` / `estimation` / `other` |
| `asked_as` | 必 | 当时被当作哪类问题（可多选，与 `problem_kind` 区分：后者是今天的归类） |
| `status` | 必 | `open` / `resolved` / `partially_resolved` / `reformulated` / `abandoned` |
| `resolutions` | 条件 | `resolved` 时至少一条 `{by, year, theorem, method, note, grade}` |
| `reframings` | 选 | `{later_problem, by, year, equivalence, equivalence_grade, note}`；**"后世重新表述"不是解决**，必须单独记 |
| `related_branches` | 必 | `BR:` 数组，可跨类 |
| `depends_on` | 选 | `CO:` / `TH:` 数组 |
| `spawned` | 选 | `PR:` 子问题 |
| `posed_by` / `posed_in` | 选 | `PE:` / `TX:` / `EV:` |
| `still_open_note` | 条件 | `open` 时写清当前障碍，不写"很难" |

**规则**：平行公设、五次方程可解性、希尔伯特 23 问都归此类。一个问题的"重述"（如从"作平行线"变成"三角形内角和是否为 180°"）用 `reframings`，不得直接写成"已解决"。

### 4.5 方法/算法 `method`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `kind` | 必 | `algorithm` / `construction` / `proof_method` / `computational_technique` / `notation_technique` |
| `input` / `output` | 必 | 自然语言；算法要有可执行口径 |
| `correctness_basis` | 选 | `TH:` / `CO:` 数组；没有正确性依据时写 `U` |
| `first_use` | 选 | `{by, year, text, locator, grade}` |
| `variants` | 选 | `ME:` 数组 |
| `applies_to` | 选 | `PR:` / `CO:` 数组 |
| `complexity_note` | 选 | 仅算法类 |
| `failure_refs` | 选 | 方法失效的具体案例 `FA:` |

### 4.6 理论 `theory`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `assumptions` | 必 | 公理/假设列表，逐条可指认 |
| `core_concepts` | 必 | `CO:` 数组 |
| `signature_results` | 选 | `TH:` 数组 |
| `accepted_period` | 选 | `{from, to, precision}` |
| `superseded_by` | 条件 | `TY:`；被取代时必填 |
| `failure_refs` | 条件 | 被取代时必填 `FA:`，说明取代原因 |
| `residue` | 选 | 被取代后仍被沿用的部分 |

### 4.7 失败路线 `failure`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `failure_kind` | 必 | `false_proof` / `superseded_theory` / `unadopted_unfalsified` |
| `target` | 必 | `TH:` / `TY:` / `CO:` / `ME:`，被主张或被取代的对象 |
| `flawed_step` | 条件 | `false_proof` 必填：错在第几步、错在哪 |
| `why_accepted` | 必 | 当时为什么被接受：权威、审稿缺位、记法掩盖、需求驱动等，要给证据 |
| `acceptance_evidence` | 选 | `TX:` / `TW:` / `EV:` 数组 |
| `corrected_by` | 条件 | `PE:`；`unadopted_unfalsified` 可空 |
| `correction_event` | 条件 | `EV:`；无纠正时 `null` |
| `correction_text` | 选 | `TX:` / `TW:` |
| `residue` | 选 | 残留影响：术语、记号、方法、错误直觉 |
| `current_status` | 必 | `corrected` / `partially_corrected` / `still_unresolved` / `unadopted` |
| `still_open_note` | 条件 | `unadopted_unfalsified` 必填：为何至今未被采纳、也未证伪 |

**三类失败的写法差异**：

- `false_proof`：必须有 `flawed_step` 与 `corrected_by`；不得只写"证明是错的"。
- `superseded_theory`：必须有 `superseded_by` 与 `residue`；不得把被取代理论写成"从未有用"。
- `unadopted_unfalsified`：不得写"已被否定"；写清"未被采纳"与"未被证伪"两件事。

### 4.8 记号/术语 `notation`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `symbol_id` | 必 | 唯一 ASCII slug，如 `dy-dx`、`forall`、`term-group-zh`；与对象 ID 分离，便于形式化映射 |
| `kind` | 必 | `symbol` / `term` / `unit` / `name` |
| `glyph` | 条件 | 符号类必填：`{unicode, latex, plain}` |
| `denotation` | 必 | 数组 `{concept, valid_from, valid_to, note}`；同一符号可先后指称不同概念 |
| `first_occurrence` | 必 | `{text, witness, locator, year, grade}`；不确定写 `U` |
| `competitors` | 选 | `{form, user, period, source, note}` 数组 |
| `superseded_by` | 选 | `NO:`；被取代时给出取代时点与场景 |
| `modern_standard` | 必 | `{form, scope, note}`：今天在什么范围内是标准 |
| `formal_mapping` | 选 | `{language, expression, note}`，如 `lean: "deriv f x"` |
| `zh_term_history` | 条件 | 中文术语必填（见 §8.3） |
| `status` | 必 | `current` / `historical` / `regional` / `disputed` |

### 4.9 人物 `person`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `name_variants` | 必 | 原名、拉丁名、汉译名、常见误写 |
| `dates` | 选 | `{birth, death, precision}`；不确定写区间 |
| `roles` | 选 | `author` / `translator` / `commentator` / `critic` / `teacher` 等 |
| `affiliations` | 选 | 机构 + 时间 |
| `authored` / `introduced` / `proved` / `corrected` | 选 | 由工具反向生成，正文不手写 |
| `notes` | 选 | 只写与归属判断有关的内容 |

### 4.10 文本 `text` 与见证 `witness`

`text`：`title_variants`、`authors`、`date_composition`、`date_first_publication`、`language`、`genre`、`text_type`（`original` / `compilation` / `commentary` / `translation` / `textbook` / `article` / `letter` / `treatise` / `standard` / `manual` / `errata` / `release_note` / `spec_change` / `source_repository` / `commit` / `mailing_list`）、`chains[]`、`support_claims[]`、`reliability_note`。

`witness`：`witness_kind`（`original` / `copy` / `critical_edition` / `translation` / `modern_collation` / `excerpt` / `reconstruction` / `manuscript` / `printed_edition` / `web_snapshot` / `commit`）、`extant`（布尔）、`date`、`editor` / `translator`、`derived_from`（父见证）、`holding`（`{institution, shelfmark, url?}`）、`completeness`、`stemma_branch`、`supports[]`。

**枚举口径**（v0.2 修订，2026-11-23）：`standard` 指标准/规范正文（如 IEEE 754、ISO C）；`manual` 指厂商或项目手册/指南（如 Intel SDM）；`errata` 指勘误表；`release_note` 指版本发布说明；`spec_change` 指标准的修订/变更记录（如 JEP、标准修订案）；`source_repository` 指以仓库形态存在的源码；`commit` 指一次提交记录；`mailing_list` 指邮件列表/讨论档。见证侧：`web_snapshot` 指有固定快照的网页（无快照按 §5.6 判 `U`）；`commit` 指以提交为载体的见证。`article` / `letter` / `treatise` / `manuscript` / `printed_edition` 为原有样例已在使用的取值，此前未列入本行，一并补入，不废除任何旧值。

**规则**：原本已佚时仍建 `witness_kind: original` 且 `extant: false`，并挂"据…转述"的 `U` 断言；不得因为原件不存就把整条链降为 `U`——链上每个节点各自定级。

### 4.11 事件 `event`

`date {from,to,precision}`、`place`、`actors`、`description`、`causes`、`consequences`、`sources[]`、`part_of`（`PR:` / `TH:` / `TY:` / `FA:` / `CO:` / `ME:`）。

### 4.12 教学挂点 `teaching_point`

`course`、`textbook {title, edition}`、`chapter`、`learning_objective`、`prerequisite_concepts`、`common_misconception`、`history_objects`（`CO:` / `TH:` / `PR:` / `NO:` / `ME:`）、`output_form`（`card` / `lecture` / `route`）、`evidence`：固定 `not_applicable`，并写 `basis: curriculum`。

**规则**：教学挂点不承担史学论断；它的"历史依据"必须指向别的对象，不能自己写史实。

### 4.13 观点 `statement`

| 字段 | 必/选 | 约束 |
|---|---|---|
| `claim_text` | 必 | 该主张本身，一句话，≤280 字符；**不做论证**，论证进 `text_ref` |
| `claimant` | 条件 | `PE:` 或 `PE:` 数组；无可指认主张者（匿名共同体说法）写 `null` 并在 `claims[]` 说明 |
| `claimed_at` | 条件 | `{from, to, precision}`；与 `claimed_in` 至少有一个 |
| `claimed_in` | 条件 | `TX:` / `TW:` / `EV:` 数组 |
| `about` | 必 | `TH:` / `CO:` / `PR:` / `TY:` / `NO:` / `BR:` / `EV:` 数组，被主张的对象 |
| `stance` | 必 | `asserts` / `denies` / `questions` / `reports`；`denies` 专用于"某人否认 X" |
| `status` | 必 | `current` / `superseded` / `contested` / `misattributed` |
| `corrected_by` | 条件 | `PE:`；`misattributed` 时必填 |
| `text_ref` | 必 | 争论过程、原文引文放文档 |

**规则**：

- 一个定理可挂多条 `asserted_by` 边指向不同 `ST:` 节点——"谁说过"与"是否成立"是两件事。
- `ST:` 不承载真假：它只记录"某人某时主张 X"。X 的真假由 `TH:` 的 `proof_status` 决定。
- 归属错误的说法（如把后世结论安到前人头上）用 `status: misattributed`，并建一条 `contradicts` 边指向正确归属的观点节点，不直接删。
- 互斥说法用 `contradicts` 边显式化；并存说法（都成立）用平行边，见 §5.3。

---

## 5. 图：边模型与约束

### 5.1 边信封

```json
{
  "id": "E:PR:fifth-postulate-deducibility>reformulates>PR:independence-of-parallel-postulate",
  "from": "PR:fifth-postulate-deducibility",
  "to": "PR:independence-of-parallel-postulate",
  "type": "reformulates",
  "directed": true,
  "time": { "from": 1868, "to": 1868, "precision": "year", "basis": "贝尔特拉米模型发表" },
  "source": { "text": "TX:beltrami-1868-saggio", "locator": "§1" },
  "claimant": "PE:beltrami",
  "grade": "S",
  "attestation": "later_report",
  "confidence": 0.85,
  "weight": null,
  "kind": null,
  "role": null,
  "text_ref": "doc:spec/framework/samples/non-euclidean-geometry.md#reframing",
  "note": "",
  "claims": []
}
```

| 字段 | 必/选 | 取值与含义 |
|---|---|---|
| `id` | 必 | `E:<from>><type>><to>`，平行边加 `#n` |
| `from` / `to` | 必 | 节点 ID，必须存在于同一图包 |
| `type` | 必 | 见 §5.2，不得自造 |
| `directed` | 必 | 有向 `true`；对称类型固定 `false` |
| `time` | 必 | `{from, to, precision, basis?}`；`from`/`to` 允许 `null`，两端都 `null` 时 `precision` 必须为 `unknown` |
| `source` | 条件 | `{text?, witness?, locator, url?}`；与 `claimant` **至少给一个** |
| `claimant` | 条件 | `PE:` 或自由文本；主张/执行这条关系的人 |
| `grade` | 必 | `A` / `S` / `U` / `F`，判据同 `evidence-tags.md` |
| `attestation` | 必 | `direct` / `contemporary_report` / `later_report` / `textbook_simplification` / `unknown` |
| `confidence` | 必 | 0–1。与 `grade` 不同：`grade` 是证据距离，`confidence` 是"这条边成立"的判断 |
| `weight` | 条件 | `parent_of` 必填，0–1；其余边可选 |
| `kind` | 条件 | `parent_of` / `cross_class` / `contributed_to` 用；取值见 §5.2 |
| `role` | 条件 | `contributed_to` 必填：`author` / `editor` / `translator` / `commentator` / `compiler` |
| `text_ref` | 否 | 指向文档段落，格式同 §3.3 |
| `note` | 否 | ≤280 字符；长论述进 `text_ref` |
| `claims` | 否 | 指向端点节点 `claims[]` 中的 `CLM:`，用于把"边成立"挂到具体断言 |

`confidence` 口径（只是约定，不是硬校验）：

| 区间 | 含义 |
|---|---|
| 0.90–1.00 | 一手文献直接写明的同一关系 |
| 0.70–0.89 | 强二手研究一致支持，或一手文献可推出但未明说 |
| 0.50–0.69 | 学界有分歧，本图取其一 |
| < 0.50 | 推测；此时 `grade` 必须是 `U`，且 `note` 写清依据缺口 |

### 5.2 边类型表

> **由单一真源生成，勿手改。** 本表与 [`framework/edge-signatures.yaml`](framework/edge-signatures.yaml) 同步；该 YAML 是 31 类边的签名、专属属性与释义的**唯一真源**。修改边类型请改 YAML，然后在 `tools/` 目录运行 `py -3 -m graphlint generate`。手改本表视为错误。

<!-- GENERATED:edge-table BEGIN (source: framework/edge-signatures.yaml) -->
| # | `type` | 方向 | from → to | 专属属性 | 用途 |
|---:|---|---|---|---|---|
| 1 | `parent_of` | 父→子 | BR → BR | `kind` ∈ `taxonomic` / `historical` / `institutional`（必填）；`weight` 必填 | 分类包含、历史衍生、建制派生 |
| 2 | `cross_class` | 有向 | BR → BR | `kind` ∈ `overlaps` / `prerequisite` / `method_source` / `shared_object`（必填）；`weight`（可选，默认 0.5） | 跨类归属；一个分支可有多条跨类边 |
| 3 | `prerequisite_of` | 先→后 | BR → BR | — | 学习顺序，不等于从属 |
| 4 | `concerns` | 索引 | BR → CO / TH / PR / TY / TX | — | 分支的核心对象；不传递、不参与推理 |
| 5 | `generalizes` | 一般→特殊 | CO / TH → 同类型 | — | 与"特殊化"互逆，只写一边 |
| 6 | `depends_on` | 后→前 | CO / TH / PR / ME / TY → CO / TH / NO | — | 前置依赖；构成 DAG |
| 7 | `resolves` | 解决→问题 | TH / ME → PR | — | 一条边只表示"给出了答案"，不表示答案唯一 |
| 8 | `reformulates` | 旧→新 | PR → PR | — | 后世重新表述；不等于解决 |
| 9 | `spawned` | 母→子 | PR → PR | — | 派生问题 |
| 10 | `poses` | 提出者→问题 | PE / TX / EV → PR | — | 谁在何时以何表述提出 |
| 11 | `asserted_by` | 对象→观点 | CO / TH / PR / TY / FA → ST | — | 同一对象可有多条；主张者放在 ST 节点 |
| 12 | `about` | 观点→对象 | ST → BR / CO / TH / PR / TY / NO / EV | — | 观点所主张的对象 |
| 13 | `claimed_in` | 观点→出处 | ST → TX / TW / EV | — | 该主张写在哪份文本/哪个事件里 |
| 14 | `contradicts` | 对称 | ST → ST | — | 互斥说法；只写一次 |
| 15 | `competes_with` | 对称 | NO / ST → 同类型 | — | 同期竞争写法/主张 |
| 16 | `denotes` | 记号→概念 | NO → CO | `time` 必填（可一端 `null`） | 同一符号先后指称不同概念 |
| 17 | `supersedes` | 旧→新 | TY / NO → 同类型 | — | 使用范围被取代，不表示概念被淘汰 |
| 18 | `uses_notation` | 使用者→记号 | CO / TH / ME / TY → NO | — | 谁用了这套记号 |
| 19 | `uses_method` | 使用者→方法 | TH / PR / TY / FA → ME | — | 不要与方法→对象的反向边混用 |
| 20 | `targets` | 失败→对象 | FA → CO / TH / PR / ME / TY | — | 失败指向被主张或被取代者 |
| 21 | `corrected_by` | 失败→纠错者 | FA → PE | — | 纠正者可为多人，多条边 |
| 22 | `contributed_to` | 人物→文本 | PE → TX / TW | `role` ∈ `author` / `editor` / `translator` / `commentator` / `compiler`（必填） | 作者、编者、译者、注家分开 |
| 23 | `proved` | 人物→定理 | PE → TH | — | 与 claims[] 里的证明细节互补 |
| 24 | `introduced` | 人物→对象 | PE → CO / ME / NO | — | 只写可归属的首次引入 |
| 25 | `participates_in` | 人物→事件 | PE → EV | — | 角色写 note 或 kind |
| 26 | `part_of` | 事件→对象 | EV → CO / TH / PR / ME / TY / FA | — | 事件归属；指向 CO/ME 时 note 必填 |
| 27 | `witness_of` | 见证→文本 | TW → TX | — | 每条见证必须且只能挂一条 |
| 28 | `derived_from` | 子→母 | TW → TW | — | 允许一节点多子，表达并行传承 |
| 29 | `supports` | 证据→对象 | TX / TW → 任意对象（不含 TP） | — | 该见证或文本支撑了哪些断言/对象 |
| 30 | `anchors` | 挂点→对象 | TP → CO / TH / PR / ME / NO | — | 教学挂点唯一的出边类型 |
| 31 | `exemplifies` | 例→理论 | CO / TH → TY | — | 理论的核心概念与代表结果 |
<!-- GENERATED:edge-table END -->

### 5.3 平行边与观点节点

两种"多"必须分开：

| 情形 | 表达 | 例子 |
|---|---|---|
| 两件事**都成立**，只是各自有来源 | **平行边**：同 `from/type/to` 多条，ID 加 `#2` | 同一概念在巴比伦与中国独立出现 → 两条 `introduced` 边，各自带时间与文献 |
| 两种说法**互斥**，至多一真 | **观点节点 + `contradicts`** | 萨凯里"锐角假设导致矛盾" vs 罗巴切夫斯基"锐角假设可成立" |

规则：

1. 平行边只表示并存，不得拿来编码"两种对立解释"；对立必须建 `ST:` 节点并用 `contradicts`。
2. 平行边的每一条都要有自己的 `time` / `source` / `grade` / `confidence`，不允许一条有证据另一条空着。
3. 对称边（`contradicts`、`competes_with`）按端点 ID 字典序小→大写一次，`directed: false`，工具补反向索引。
4. 同一对端点之间允许不同类型的边（如 `NO→NO` 既有 `supersedes` 又有 `competes_with`），因为它们回答不同问题。

### 5.4 时间

- 节点时间：`occurrences[]`（出现）与各类型自己的 `date`/`accepted_period`（事件、接受期）。
- 边时间：`time` 记录"这条关系何时成立"。三种用法：
  - 点事件：`from = to`；
  - 区间：`from < to`；
  - 未知：`from`/`to` 为 `null`，`precision: "unknown"`。
- 边的 `time` 与端点的 `occurrences` 不得互相冒充：`introduced` 边的 `time` 是"引入行为"的时间，不是概念的"现存最早记载"。
- "现存最早"只能由 `A`/`S` 支撑的见证计算；`U` 不参与排序。

### 5.5 长文本与图的双向指针

- 图侧：`node.text_ref` / `edge.text_ref` → `doc:<file>#<anchor>`。
- 文档侧：段落里写 `graph://<node-or-edge-id>`，指向图中对象。
- 校验：`text_ref` 的文件必须存在，锚点必须在文件里出现；文档里的 `graph://` ID 必须存在于图包。
- 图里不写超过 280 字符的引文；`summary`、`claim_text`、`note` 同样受此限。

### 5.6 边约束清单

> **由单一真源生成，勿手改。** 下面的端点表与不变量由 [`framework/edge-signatures.yaml`](framework/edge-signatures.yaml) 生成；判定级别写在不变量条目上。`tools/graphlint` 每次运行直接读取同一文件。修改约束请改 YAML，然后在 `tools/` 目录运行 `py -3 -m graphlint generate`。手改生成物视为错误。

**A. 端点硬约束（级别见 B 段；默认 error，互斥为 warning）**

<!-- GENERATED:edge-constraints BEGIN (source: framework/edge-signatures.yaml) -->
| 边类型 | 允许 from | 允许 to | 明确禁止 |
|---|---|---|---|
| `parent_of` | BR | BR | 任何非 BR 端点；自环；成环；与同一对端点的 cross_class 并存（降级为 warning，见 B.5） |
| `cross_class` | BR | BR | 任何非 BR 端点；自环；与同一对端点的 parent_of 并存（降级为 warning，见 B.5） |
| `prerequisite_of` | BR | BR | 任何非 BR 端点；自环；与同对的 parent_of 混用（先学≠从属，见 B.5） |
| `concerns` | BR | CO / TH / PR / TY / TX | 从 CO/TH 出发；指向 PE/EV/TP/TW/ST |
| `generalizes` | CO / TH | CO / TH | CO→TH、TH→CO 混类型；反向重复写 |
| `depends_on` | CO / TH / PR / ME / TY | CO / TH / NO | 指向 PR（那是 resolves）；自环；成环 |
| `resolves` | TH / ME | PR | 从 ST/FA/CO 出发；指向非 PR |
| `reformulates` | PR | PR | 自环；成环；当作 resolves 使用 |
| `spawned` | PR | PR | 自环；成环；与 reformulates 混用 |
| `poses` | PE / TX / EV | PR | 从 BR/CO 出发；指向非 PR |
| `asserted_by` | CO / TH / PR / TY / FA | ST | 反向写（ST→对象请用 about）；指向非 ST |
| `about` | ST | BR / CO / TH / PR / TY / NO / EV | 对象→观点（那是 asserted_by）；指向 PE/TX/TW/TP |
| `claimed_in` | ST | TX / TW / EV | 从 PE/CO 出发；指向 PR/TH |
| `contradicts` | ST | ST | directed: true；自环；同一关系写两条 |
| `competes_with` | NO / ST | NO / ST | 跨类型（NO↔ST）；directed: true；写两条 |
| `denotes` | NO | CO | 反向（CO→NO 请用 uses_notation）；指向 TH/PR |
| `supersedes` | TY / NO | TY / NO | NO↔TY 跨类型；自环；成环 |
| `uses_notation` | CO / TH / ME / TY | NO | 反向（NO→CO 请用 denotes） |
| `uses_method` | TH / PR / TY / FA | ME | 从 ME 出发（反向）；从 CO 出发（实现→算法待 implementation 类型立项） |
| `targets` | FA | CO / TH / PR / ME / TY | 对象→失败（反向）；指向 PE/EV/BR/TP |
| `corrected_by` | FA | PE | 反向（PE→FA）；指向 EV（事件用 part_of） |
| `contributed_to` | PE | TX / TW | 从 TX 出发；缺 role |
| `proved` | PE | TH | 指向 CO/PR；反向（TH→PE） |
| `introduced` | PE | CO / ME / NO | 指向 TH/TX；反向（对象→PE） |
| `participates_in` | PE | EV | 反向（EV→PE） |
| `part_of` | EV | CO / TH / PR / ME / TY / FA | 从 BR 出发；自环；成环；指向 CO/ME 时无 note |
| `witness_of` | TW | TX | 从 TX 出发；TW→TW（那是 derived_from）；一条 TW 挂两个 TX |
| `derived_from` | TW | TW | 从 TX 出发；自环；成环 |
| `supports` | TX / TW | 任意对象（不含 TP） | 从 FA/ST/TP 出发（失败与观点不提供证据）；指向 TP |
| `anchors` | TP | CO / TH / PR / ME / NO | TP 作为 to；TP 发出非 anchors 的边 |
| `exemplifies` | CO / TH | TY | 从 TY 出发；指向非 TY |
<!-- GENERATED:edge-constraints END -->

**B. 全局不变量（7 类）**

<!-- GENERATED:invariants BEGIN (source: framework/edge-signatures.yaml) -->
1. **自反（自环）**（`no_self_loop`）· 级别 `error` · 判定：逐条边检查 from == to。任何边类型都不允许自环。
   - 规则：自环不表达任何关系；需要'自身性质'时写节点字段，不写边。
   - 适用：所有边
2. **无环**（`acyclic`）· 级别 `error` · 判定：对每个声明 acyclic: true 的边类型单独构子图，用 DFS 三色标记找环；报告环上节点序列。
   - 规则：parent_of、derived_from、depends_on、part_of、reformulates、spawned、supersedes 的无环性分别判定，不合并子图。
   - 适用：`parent_of`、`derived_from`、`depends_on`、`part_of`、`reformulates`、`spawned`、`supersedes`
3. **同型**（`homotypic`）· 级别 `error` · 判定：对声明 same_class: true 的边，比较两端节点的 type 是否相同；不同则报 from 类→to 类。
   - 规则：只用节点 type 判定，不看 ID 前缀。
   - 适用：`generalizes`、`competes_with`、`supersedes`
4. **对称**（`symmetric`）· 级别 `error` · 判定：对声明 symmetric: true 的边：directed 必须为 false；同一无向关系只存一条，from 必须取 ID 字典序较小者；若发现反向的另一条边，报重复。
   - 规则：工具补反向索引，图里不写第二条。
   - 适用：`contradicts`、`competes_with`
5. **互斥**（`mutex`）· 级别 `warning` · 判定：按 rules 逐对检查同一 from/to 上的边类型组合；命中只报 warning，不拒绝图。
   - 规则：互斥是取景提示，不是物理错误：同一对端点可以同时承载不同类型的关系，只要语义确实不同。
   - `parent_of` + `cross_class`（同一 from→to）· 级别 `warning`：同一对分支上同时有 parent_of 与 cross_class：归属重叠，请确认这是两种不同关系（分类从属 + 跨类共用），还是把同一关系写了两遍。
     - 说明：v0.2 修订（2026-11-23）由 error 降为 warning。降级后，research/ackermann-1928 里'若开第 63 支则 CO:ackermann-function 同时挂 parent_of 与 cross_class'的三处归属不再判非法，只提示归属重叠；该案例的取舍仍由人工决定。
   - `prerequisite_of` + `parent_of`（同一 from→to）· 级别 `warning`：同一对分支同时有 prerequisite_of 与 parent_of（或方向相反）：先学顺序与从属关系是两件事，请确认不是把从属写成了先修。
6. **反向写法**（`reverse_writing`）· 级别 `error` · 判定：端点类型不满足签名时，先试反向组合：若反向组合满足该类型的定义域/值域，报'方向疑似写反'并给出声明方向；若反向组合恰好符合另一登记类型（reverse_alias），点名应改用的类型。
   - 规则：方向由签名定义，不靠约定俗成；反向写法不另设边类型。
   - 适用：所有边
7. **条件必填**（`conditional_required`）· 级别 `error` · 判定：按 rules 逐条检查；每条规则自带 level，命中时给实际值与期望值。
   - 规则：条件必填不设默认值：缺省即违例，不用 0/空串兜底。
   - `attestation_grade_cap` · 级别 `error`：当 attestation = textbook_simplification，要求 grade ∈ {F, U}。消息：attestation=textbook_simplification 时 grade 上限不满足：实得 {grade}（期望 F 或 U）。教材/科普转述不能支撑 A/S 级断言。
   - `later_report_grade_cap` · 级别 `error`：当 attestation = later_report，要求 grade ∈ {S, U, F}。消息：attestation=later_report 时 grade 不得为 A：实得 A（期望 S/U/F）。后世研究者叙述不能当作亲见原件。
   - `unknown_grade_note` · 级别 `error`：当 grade = U，要求 note 非空。消息：grade=U 时必须写 note：说明未核实的依据缺口与下一步查证路径。
   - `source_or_claimant` · 级别 `error`：当 任意边，要求 source 存在，或 claimant 非空。消息：边必须给出 source 或 claimant：没有来源也没有主张者的关系不可核。
   - `parent_weight_sum` · 级别 `error`：当 某节点有 parent_of 入边，要求 这些入边的 weight 之和 = 1.00（容差 ±0.01）。消息：parent_of 入边权重和 {actual} ≠ 1.00：同一子节点的父边必须归一；无父的根节点不参与。
   - `witness_unique` · 级别 `error`：当 节点类型为 witness，要求 该 TW 恰好有一条 witness_of 出边，且只指向一个 TX。消息：见证 {node} 的 witness_of 出边数为 {actual}（期望正好 1）。
   - `tp_excluded` · 级别 `error`：当 边涉及 teaching_point，要求 TP 只能作为 anchors 的 from；不得出现在 supports/depends_on/part_of 的任何一端。消息：教学挂点只做索引：{type} 边把 TP 放在 {end} 端。
   - `denotes_time` · 级别 `error`：当 边类型为 denotes，要求 time.from 与 time.to 至少一端非 null；或 precision=unknown 且 note 说明原因。消息：denotes 的时间至少一端非 null，或 precision=unknown 且 note 说明未知原因；实得 from={from}, to={to}, precision={precision}。
   - `part_of_note` · 级别 `error`：当 边类型为 part_of 且 to 节点类型 ∈ {concept, method}，要求 note 非空。消息：part_of 指向 CO/ME 时 note 必填：写明为何不挂更具体的 PR/TH/TY/FA。
   - `claims_text_exists` · 级别 `error`：当 节点 claim.source.text 以 TX: 开头，要求 该 TX 存在于此图包；否则该 claim 的 grade 必须是 U。消息：claim {claim} 引用的 {text} 不在图包内，grade 却为 {grade}（期望 U）。
   - `non_isolated` · 级别 `error`：当 节点 status 不是 proposed，且 type 不是 branch，要求 至少有一条入边或出边。消息：节点 {node} 没有任何边：非 proposed 的非分支节点必须挂到图上。
<!-- GENERATED:invariants END -->

**C. 反例（标 error 的会被校验拒绝；标 warning 的只提示）**

- `CO:group —denotes→ NO:group-notation`：方向反了，应为 `NO —denotes→ CO`。
- `TX:euclid-elements —derived_from→ TW:euclid-elements.heath-1908`：`derived_from` 只在 `TW` 之间。
- `FA:saccheri-1733 —supports→ PR:fifth-postulate-deducibility`：失败路线不能提供证据。
- `TP:geometry-parallel-postulate —asserted_by→ ST:...`：教学挂点不主张史实。
- 同一对 `BR` 同时有 `parent_of` 与 `cross_class`：**v0.2 修订（2026-11-23）后只报 warning**，提示"归属重叠"。`research/ackermann-1928` 里"若开第 63 支，阿克曼那批对象会有三处归属"因此在结构上不再判非法，只作为人工取舍提示；是否真的开分支不由校验器决定。
- 两条 `contradicts` 边互为反向：对称边只写一次。
- `EV:... —part_of→ CO:...`（或 `ME:...`）而 `note` 为空：放宽后仍拒绝，须写明"为何不挂 PR/TH/TY/FA"。
- `CO:glibc-qsort —uses_method→ ME:introsort`：`uses_method` 起点不含 `CO`，实现→算法需等 `implementation` 类型立项后再定，本轮不放开。

---

## 6. 时间模型

- 不用 `year` 单值；用 `occurrences[]`（§3.4）。
- 三档时间：**出现**（某概念/记号在某文本出现）、**事件**（离散发生）、**接受期**（理论/方法被广泛使用的区间）。
- 同一概念多次出现时，每条 occurrence 独立给 `independence`：`independent` / `derived` / `contested` / `unknown`。判"独立"至少要有"无传播路径证据"或"同期文献未互引"，否则只能 `unknown`。
- "首次"只能由 `occurrences` 计算，并受证据等级限制：只有 `A`/`S` 支撑的出现才可作"现存最早"；`U` 不参与排序。
- 禁止把"现存最早记载"写成"发明时间"；需要区分时用字段 `first_attested` 与 `first_claimed`。

---

## 7. 内容四层（问题 / 失败 / 记号 / 文本）

**命名约定（全文唯一口径）**：「四层」在本框架里只指**内容四层**——问题层、失败层、记号层、文本层，它们是 `affected_layers` 的四个字段，用来描述一个分支主要被哪类内容撑起。论文里另有一套**结构四层**——领域层、概念与理论层、问题与失败层、依据与解释层，那是按节点类型分的结构分层，不是本节的四层，两者不得混用同一个说法。

### 7.1 问题层

问题是一等对象（§4.4），不再挂"争议"字段。关键区分：

- `problem_kind` 是**今天的归类**，`asked_as` 是**当时被当作什么**。两者不一致时必须都写。例：平行公设当时被当作"公设可否证明"，今天归为"几何公理的独立性问题"。
- `reframings` 记"后世重新表述"，**不等于解决**。例：五次方程从"求根式公式"重述为"群是否可解"，只有后者被伽罗瓦理论解决，前者仍是"无根式通解"。
- `status` 与 `resolutions` 必须一致：`resolved` 无 `resolutions` 视为校验错误。

希尔伯特 23 问这类"问题集合"建一个 `PR:hilbert-23` 作为容器，子问题用 `spawned` 挂出，不把 23 条塞进一个对象。

### 7.2 失败层

三类失败（§4.7）在字段上强制不同：`false_proof` 必须有 `flawed_step`；`superseded_theory` 必须有 `superseded_by` + `residue`；`unadopted_unfalsified` 必须有 `still_open_note` 且 `corrected_by` 可空。

"当时为什么被接受"必填，且要挂证据：审稿制度缺位、记号掩盖了问题、权威背书、实际计算有效，都算理由，但都要能指认来源。

### 7.3 记号/术语层

- 符号与概念分离：`NO:dy-dx` 与 `CO:derivative` 是两个对象，用 `denotes` 连接并带时间窗。
- `symbol_id` 为形式化对接准备：符号本身有稳定标识，`formal_mapping` 给出现代语言（Lean/Isabelle/LaTeX）中的对应写法。
- 竞争写法用 `competes_with`，取代用 `supersedes`；**不要**把"今天不用了"写成"错误"。
- 中文译名史（`zh_term_history`）每条：`{term, source_text, translator, year, place, earlier_terms[], note, grade}`。译名不是"翻译"，是术语定型事件，必须有译著与页码。
- 译名与符号分开：一个中文词可能对应多个西文词，反之亦然；不要一对一强行映射。

### 7.4 文本传承链

- 一条链是一张图，不是列表：`TX` 下可有多个 `chains[]`，每个链是一个 `root_witness` + 节点 + `derived_from` 边。
- 并行传承：同一 TX 允许希腊文本链、阿拉伯—拉丁链、汉译链并存；`stemma_branch` 标分支名。
- 每个节点记：年代、编者/译者、馆藏与编号、完整度、支撑了哪些对象。
- 原本已佚：建 `extant: false` 的根节点，链不断；不要用"失传"代替结构。
- 辑佚本、校勘本、点校本都是见证节点，不是新 TX；除非它是独立著作（如辑佚产生的汇编）。

### 7.5 内容四层在同一张图里怎么连

内容四层不是四张表，而是共用同一套节点与边的四条路径。固定连接方式：

| 层次 | 入口节点 | 关键边 | 与其他层的接点 |
|---|---|---|---|
| 问题层 | `PR:` | `poses` 入、`resolves` 入、`reformulates` 出 | 指向 `TH`（解决）、`PE`（提出）、`BR`（归属） |
| 失败层 | `FA:` | `targets` 出、`corrected_by` 出 | 指向 `PR`（所要求的证明）、`TH`/`TY`（被主张者）、`TX`/`TW`（依据） |
| 记号层 | `NO:` | `denotes` 出、`supersedes`/`competes_with` 互连 | 指向 `CO`（所指概念）、`TX`（首次出现） |
| 文本链 | `TX:`/`TW:` | `witness_of`、`derived_from`、`supports` | `supports` 指向任意层，把"这条话有版本依据"落到具体节点 |

协同的最小闭环（样板见 `samples/non-euclidean-geometry.json`）：

```
PR ←FA→ TH/TY
 │        ↑
 └→ NO → CO ← TW → TX
```

即：问题被一次失败尝试指向；失败所需的命题与理论由 `TH`/`TY` 承担；记号层说明这些命题当时用什么词与符号称呼；文本链给出该说法出自哪一份实物，以及这份实物怎么传下来。内容四层任一环缺失，图上就会出现断头，校验时应能报出来。

---

## 8. 62 分支挂载表（区域取景轴）

**口径**：62 分支是从当代数学分支面向过去划出的**区域取景轴**，由本项目自建、源于内容分类方案。它只作 `view_classes` 标签与检索入口，不承担本体结构，也不作史学分期；结构一律由 `parent_of` / `cross_class` 边承担。本章表格里的「内容四层影响」指 §7 的问题/失败/记号/文本四个字段，与论文的结构四层无关。

### 8.1 分类争议的处理原则

1. **视图与本体分离**：十类只是 `view_classes`；结构由 `parents` 决定。
2. **允许双重登记**：同一分支可同时出现在两个视图类，不设"唯一归属"。
3. **父子分三种**：`taxonomic`（分类包含）、`historical`（历史衍生）、`institutional`（建制派生）。"抽象代数 → 群论"是分类，"微积分 → 实分析"是历史。
4. **缺失分支不硬塞**：偏微分方程、动力系统、统计学等作为 `proposed` 扩展槽，不进 62 计数，保留可追溯性。
5. **争议留痕**：每处争议写 `{issue, resolution, status}`，不静默改结构。
6. **父关系即边**：表里"父（kind）"一列的每一项都展开为一条 `parent_of` 边。两项父 = 两条边，各带 `weight`；默认首个父权重 0.6、其余均分 0.4（`branches.json` 的 `edge_projection` 固化此规则），不写 `primary` 字段也能得到确定图。
7. **跨类即边**：`cross_class` 里的 `view` 若解析到某个分支 ID，展开为 `cross_class` 边；若只解析到十类类名，则只进 `view_classes`，不生成边。这样不会出现"指向类名的悬空边"。
8. **父与跨类互斥**：同一对分支只能有一条 `parent_of` 或一条 `cross_class`，不允许两者并存（§5.6）。

### 8.2 第一类 基础数学（8）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 1 | 算术 | `BR-FND-ARITH` | 根 | 基础；跨 数论 | — | T 高、N 中 |
| 2 | 初等代数 | `BR-FND-EALG` | 算术（历史） | 基础；跨 抽象代数 | — | N 高、T 中 |
| 3 | 欧氏几何 | `BR-FND-EGEOM` | 根 | 基础；跨 几何与拓扑 | 与"几何"总称区分：此处指《原本》体系 | T 高、P 高、F 高 |
| 4 | 初等数论 | `BR-FND-ENT` | 算术（历史） | 基础；跨 代数与数论 | — | P 高、T 中 |
| 5 | 三角学 | `BR-FND-TRIG` | 欧氏几何（历史） | 基础；跨 分析/调和 | 常被当独立分支，实为几何—天文派生 | N 高、T 中 |
| 6 | 解析几何 | `BR-FND-AGEO` | 欧氏几何（历史） | 基础；跨 代数/几何 | — | N 高、T 中 |
| 7 | 线性代数 | `BR-FND-LALG` | 初等代数（历史） | 基础；跨 抽象代数/泛函/数值 | — | N 高、P 中 |
| 8 | 抽象代数 | `BR-FND-AALG` | 初等代数（历史） | 基础；跨 代数与数论 | **嵌套争议**：作为群/环/域的伞概念，视图留在基础类，结构上作父节点 | P 高、N 中 |

### 8.3 第二类 分析学（7）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 9 | 微积分 | `BR-ANA-CALC` | 解析几何（历史） | 分析；跨 应用 | — | N 高、F 高、T 高 |
| 10 | 实分析 | `BR-ANA-REAL` | 微积分（历史） | 分析；跨 逻辑与基础 | — | N 高、P 中、F 高 |
| 11 | 复分析 | `BR-ANA-COMPLEX` | 微积分（历史） | 分析 | — | N 中、T 中 |
| 12 | 泛函分析 | `BR-ANA-FUNC` | 实分析+线性代数（历史） | 分析；跨 代数 | — | P 中、N 中 |
| 13 | 调和分析 | `BR-ANA-HARM` | 实分析+表示论（历史） | 分析；跨 代数 | — | N 高、T 中 |
| 14 | 测度论 | `BR-ANA-MEAS` | 实分析（历史） | 分析；跨 概率 | — | N 高、P 中 |
| 15 | 常微分方程 | `BR-ANA-ODE` | 微积分（历史） | 分析；跨 应用/动力系统 | 与"动力系统"分界：ODE 是方程类，动力系统是演化观点 | N 中、P 高、F 中 |

### 8.4 第三类 几何与拓扑（7）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 16 | 非欧几何 | `BR-GEO-NONEU` | 欧氏几何（历史） | 几何；跨 微分几何/逻辑 | 与双曲/椭圆几何是"总称—特例"，不并列 | P 高、F 高、N 高、T 高 |
| 17 | 射影几何 | `BR-GEO-PROJ` | 解析几何（历史） | 几何；跨 代数 | — | P 中、N 高 |
| 18 | 微分几何 | `BR-GEO-DIFF` | 微积分+欧氏几何（历史） | 几何；跨 拓扑/物理 | — | N 高、T 中 |
| 19 | 代数几何 | `BR-GEO-ALG` | 解析几何+抽象代数（历史） | 几何；跨 代数 | — | P 高、T 中 |
| 20 | 拓扑学 | `BR-TOP-GEN` | 根 | 几何与拓扑；跨 分析/代数 | — | N 高、P 中 |
| 21 | 代数拓扑 | `BR-TOP-ALG` | 拓扑学+抽象代数（分类） | 几何与拓扑；跨 代数 | — | N 高、P 高 |
| 22 | 微分拓扑 | `BR-TOP-DIFF` | 拓扑学+微分几何（分类） | 几何与拓扑 | — | P 中、N 中 |

### 8.5 第四类 代数与数论（7）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 23 | 群论 | `BR-ALG-GRP` | 抽象代数（分类） | 代数；跨 几何/表示论 | 历史早于"抽象代数"命名，另挂 `historical_origin` | P 高、F 高、N 高、T 中 |
| 24 | 环论 | `BR-ALG-RING` | 抽象代数（分类） | 代数；跨 数论 | — | N 中、P 中 |
| 25 | 域论 | `BR-ALG-FIELD` | 抽象代数+环论（分类） | 代数；跨 数论 | — | P 高、N 中 |
| 26 | 伽罗瓦理论 | `BR-ALG-GAL` | 域论+群论（分类） | 代数；跨 逻辑 | 是"理论"也是分支：`TY` 与 `BR` 双登记 | P 高、F 高、N 中、T 高 |
| 27 | 代数数论 | `BR-NT-ALG` | 初等数论+域论（历史） | 代数与数论 | — | P 中、T 中 |
| 28 | 解析数论 | `BR-NT-ANA` | 初等数论+复分析（历史） | 代数与数论；跨 分析 | — | P 高、N 中 |
| 29 | 表示论 | `BR-ALG-REP` | 群论+环论（分类） | 代数；跨 分析/物理 | — | N 高、T 中 |

### 8.6 第五类 组合与离散（7）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 30 | 组合数学 | `BR-DIS-COMB` | 根 | 组合与离散；跨 数论/计算 | — | P 高、T 中 |
| 31 | 图论 | `BR-DIS-GRAPH` | 组合数学（分类） | 组合与离散；跨 计算 | — | P 高、F 高、N 中 |
| 32 | 数理逻辑 | `BR-LOG-MATH` | 根 | **组合与离散 + 逻辑与基础（双登记）** | **谱系拆分争议**：与第 9 类同源，视图双挂，结构上作模型论/递归论/证明论的父 | N 高、P 高、F 中 |
| 33 | 集合论 | `BR-LOG-SET` | 根 | **组合与离散 + 逻辑与基础（双登记）** | **谱系拆分争议**：与数理逻辑为"共享基础"而非父子 | P 高、F 高、T 高 |
| 34 | 范畴论 | `BR-DIS-CAT` | 根 | 组合与离散；跨 代数/拓扑/逻辑 | **与高阶范畴论拆分**：后者为子，视图另挂前沿 | N 高、T 中 |
| 35 | 格论 | `BR-DIS-LATT` | 抽象代数+组合数学（分类） | 组合与离散；跨 代数 | — | N 中 |
| 36 | 编码理论 | `BR-DIS-CODE` | 信息论+抽象代数（历史） | 组合与离散；跨 计算 | — | N 中、P 中 |

### 8.7 第六类 概率与统计（6）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 37 | 概率论 | `BR-PROB` | 微积分（历史） | 概率与统计；跨 测度 | — | P 高、F 高、N 中 |
| 38 | 数理统计 | `BR-STAT-MATH` | 概率论（历史） | 概率与统计 | 与"统计学"分界：此处指数理部分，应用统计入扩展槽 | P 中、N 中 |
| 39 | 随机过程 | `BR-PROB-STOCH` | 概率论+测度论（分类） | 概率与统计；跨 分析 | — | P 高、N 中 |
| 40 | 信息论 | `BR-INFO` | 概率论（历史） | 概率与统计；跨 计算 | — | N 高、P 中 |
| 41 | 博弈论 | `BR-GAME` | 根 | 概率与统计；跨 运筹/经济 | 学科归属有争议（数学/经济），`disputes.status: open` | P 高、N 中 |
| 42 | 金融数学 | `BR-FIN` | 概率论+随机过程（历史） | 概率与统计；跨 应用 | — | P 中、N 中 |

### 8.8 第七类 计算与算法（5）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 43 | 数值分析 | `BR-CS-NUM` | 微积分+线性代数（历史） | 计算；跨 分析 | 与计算数学边界含混，见 #44 | P 中、F 高、N 高 |
| 44 | 计算数学 | `BR-CS-COMPMATH` | 根（不设父） | 计算；跨 分析/数值 | **边界争议**：常与数值分析互称；暂不设父子，标 `overlaps` + `status: open` | N 高、T 中 |
| 45 | 密码学 | `BR-CS-CRYPTO` | 初等数论+理论计算机科学（历史） | 计算；跨 代数 | — | P 中、N 中、T 中 |
| 46 | 理论计算机科学 | `BR-CS-TCS` | 数理逻辑（历史） | 计算；跨 逻辑/组合 | — | P 高、N 高、F 中 |
| 47 | 离散数学 | `BR-CS-DM` | 组合数学+数理逻辑（分类） | 计算；跨 组合 | 伞形课程名，非严格分支：`status: umbrella` | N 中 |

### 8.9 第八类 应用数学（6）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 48 | 力学 | `BR-APP-MECH` | 微积分（历史） | 应用；跨 数学物理 | — | P 高、T 高、N 中 |
| 49 | 流体力学 | `BR-APP-FLUID` | 力学+（PDE 扩展槽）（历史） | 应用；跨 分析 | 依赖缺失分支 PDE，先挂扩展槽 | P 高、T 中 |
| 50 | 数学物理 | `BR-APP-MPHYS` | 微积分+（PDE 扩展槽）（历史） | 应用；跨 分析/几何 | 同上 | P 高、N 高、T 中 |
| 51 | 生物数学 | `BR-APP-BIO` | 常微分方程+概率论（历史） | 应用；跨 统计 | — | P 中、T 低 |
| 52 | 运筹学 | `BR-APP-OR` | 组合数学+概率论（历史） | 应用；跨 计算/博弈 | — | P 高、T 中 |
| 53 | 控制论 | `BR-APP-CYBER` | 常微分方程+泛函分析（历史） | 应用；跨 计算 | 与"控制理论"混用，标 `disputes` | P 中、N 中 |

### 8.10 第九类 逻辑与基础（4）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 54 | 公理化集合论 | `BR-FND-AXIOSET` | 集合论（分类） | 逻辑与基础；跨 组合与离散 | 与 #33 是父子，不是并列 | P 高、F 高、T 高 |
| 55 | 模型论 | `BR-LOG-MODEL` | 数理逻辑（分类） | 逻辑与基础；跨 组合与离散 | 双登记，不改父 | P 中、N 中 |
| 56 | 递归论 | `BR-LOG-REC` | 数理逻辑（分类） | 逻辑与基础；跨 计算 | 双登记 | P 高、N 高 |
| 57 | 证明论 | `BR-LOG-PROOF` | 数理逻辑（分类） | 逻辑与基础；跨 计算 | 双登记 | P 高、N 高、T 中 |

### 8.11 第十类 前沿与交叉（5）

| # | 分支 | ID | 父（kind） | 视图/跨类 | 争议处理 | 内容四层影响 |
|---|---|---|---|---|---|---|
| 58 | 高阶范畴论 | `BR-X-HCAT` | 范畴论（分类） | 前沿；跨 组合与离散 | 不作为独立根；前沿视图另挂 | N 高、T 低 |
| 59 | 几何群论 | `BR-X-GEOGRP` | 群论+微分几何（分类） | 前沿；跨 几何 | — | P 中、N 中 |
| 60 | 随机矩阵 | `BR-X-RANDMAT` | 概率论+线性代数（分类） | 前沿；跨 分析 | — | P 高、N 中 |
| 61 | 拓扑数据分析 | `BR-X-TDA` | 拓扑学+数理统计（分类） | 前沿；跨 计算 | — | P 中、N 中 |
| 62 | 量子计算 | `BR-X-QC` | 理论计算机科学+线性代数（分类） | 前沿；跨 信息/代数 | — | P 中、N 中、T 低 |

### 8.12 扩展槽（不在 62 内，`status: proposed`）

| 分支 | ID | 父 | 原因 |
|---|---|---|---|
| 偏微分方程 | `BR-ANA-PDE` | 微积分+数学物理 | 原分类缺失，但被流体/数学物理依赖 |
| 动力系统 | `BR-ANA-DYN` | 常微分方程 | 原分类缺失；与 ODE 是观点差异 |
| 统计学（应用） | `BR-STAT-APPL` | 数理统计 | 原分类把统计压缩成"数理统计" |
| 计算科学 | `BR-CS-COMPSCI` | — | 若确认"计算数学/数值分析"是同一领域，用此伞节点收拢 |

### 8.13 受影响最重的分支（用于优先填充）

- **内容四层全高**：欧氏几何、非欧几何——问题（平行公设）、失败（萨凯里/勒让德）、记号（术语与译名）、文本链（希腊—阿拉伯—拉丁—汉译）。
- **问题+失败重**：群论、伽罗瓦理论、集合论、微积分、实分析、数值分析。
- **记号+文本重**：算术、三角学、解析几何、线性代数、数理逻辑。
- **文本链重**：欧氏几何、算术（《九章算术》类）、代数（花拉子米类）、力学。

排序依据是"是否有可指认的原始问题/著名失败/记号改革/多语种传承"，不是分支大小。

---

## 9. 样例（结构验证，非完整条目）

两个样板都是 `{nodes, edges}` 图包，可用 `framework/graph.schema.json` 校验：

| 文件 | 类型 | 节点 | 边 | 验证什么 |
|---|---|---|---|---|
| `framework/samples/group-theory.json` | 概念谱系清晰型 | 13 | 15 | 分支→概念→定理→问题→方法→记号→失败→事件能否串成一条链 |
| `framework/samples/non-euclidean-geometry.json` | 争议型 | 63 | 94 | 问题/失败/记号/文本链四层能否在同一张图里闭合；含 5 个观点节点与 2 组平行说法 |

### 9.1 群论样板

主链：`BR-ALG-GRP` →(concerns)→ `CO:group` →(depends_on)→ `TH:abel-ruffini` →(resolves)→ `PR:quintic-solvability`；`ME:galois-correspondence` 由问题 `uses_method` 连入；`NO:group-notation` 由 `CO:group` `uses_notation` 连入；失败侧 `FA:ruffini-1799-quintic` 用 `targets` 指向定理，用 `corrected_by` 指向阿贝尔。

要点：

- 群论的 `parent_of` 父是抽象代数（taxonomic），历史来源另用 `concerns`/`notes` 记"方程求解"，不把 19 世纪建制倒推回 18 世纪。
- 拉格朗日定理的命名是后世追认，`namesake_note` 必填，`attestation: later_report`。
- 五次方程的可解性用 `reformulates` 记"根式公式 → 群可解性"，不写成"同一个问题被解决"；两条 `resolves` 边分别指向两个问题。

### 9.2 非欧几何样板（内容四层协同）

内容四层在同一张图里的实际走法（每一跳都是真实边）：

1. **问题**：`PR:fifth-postulate-deducibility`。`original_formulation` 指《原本》第一卷第 5 公设（`A`，见证 `TW:euclid-elements.heiberg-menge`，定位 Book I, Post. 5）；`asked_as` 记"能否由其余公设证明"，`problem_kind` 记 `solvability`。最早把它当问题讨论的是普罗克洛斯（`poses` 边，来源 `TX:proclus-commentary`），不是欧几里得本人——这一点在图上是"提出者≠文本作者"的结构，不靠脚注。
2. **失败**：`FA:saccheri-1733` 用 `targets` 指向该问题，`failure_kind: false_proof`；`flawed_step` 写"以直线无限长为由排除锐角假设"；`why_accepted` 写当时对无限长的共识；`corrected_by` 指贝尔特拉米，`part_of` 把 `EV:1733-saccheri-euclides` 挂进来。另一条 `FA:euclid-a-priori` 是 `superseded_theory`，`targets` 指向 `TY:euclidean-uniqueness`——两种失败类型在同一张图里并存。
3. **记号**：`NO:term-imaginary-geometry`（罗巴切夫斯基"想象几何"）与 `NO:term-hyperbolic-geometry`（克莱因 1871 定名）都 `denotes` `CO:hyperbolic-geometry`，两条边各有时间窗；前者被后者 `supersedes`，同时二者 `competes_with`。中文侧 `NO:term-non-euclidean-zh` 指 `CO:non-euclidean-geometry`，译名史写 `U` 并给检索线索，不硬填译者。
4. **文本链**：`TX:euclid-elements` 下四条并行链——`original`(已佚) → `heiberg-menge`（希腊校勘本）→ `heath-1908`；`original` → `arabic-tradition` → `clavius-1574` → `xu-ricci-1607`（汉译）；另一条 `TX:proclus-commentary` 走 `original`(已佚) → `friedlein-1873`。每个 `TW` 只 `witness_of` 一个 `TX`，`derived_from` 指母本。

**内容四层如何真正咬合**（不是各建一组）：

- `FA:saccheri-1733` 的 `supports` 来源是 `TW:saccheri-1733-euclides.print`，同时该 `TW` 经 `witness_of` 挂到 `TX:saccheri-1733-euclides`；于是"失败"与"文本实物"是同一条链上的两个节点。
- `NO:term-imaginary-geometry` 的 `denotes` 边时间窗下界 1829，正是 `ST:lobachevsky-1829` 的 `claimed_in` 文本年份；记号首次出现与主张首次发表共用同一份 `TX`，不重复造证。
- `ST:saccheri-refutation` 与 `ST:lobachevsky-1829` 用 `contradicts` 相连（对称边只存一条），把"两种互斥说法"显式化；而两人的工作都 `about` 同一个 `PR` 与 `CO`，所以争议可被定位到同一对象上。
- `TW:euclid-elements.xu-ricci-1607` 的 `supports` 指向 `CO:parallel-postulate`，使"汉译本里这条公设怎么译"有落点，而不是只在文档里说一句。

### 9.3 一个必须避免的写法

不要写："萨凯里证明了非欧几何不可能，后来被罗巴切夫斯基推翻。"

图上的正确结构：`FA:saccheri-1733` 是**有缺陷的证明**，`targets` 指向的是"第五公设可证"这个问题，不是"非欧几何不存在"；罗巴切夫斯基 1829 是**构造**（`ST` + `CO` + `TX`），不是"推翻"；两者通过同一个 `PR` 与 `CO` 相连，不是简单的对错接力。

### 9.4 样板不是模板

样板里的每个 `claim` 都保留了 `grade` 与 `attestation`，包括 `U`。填充 62 分支时**不得**把样板里的 `U` 抄成 `S`，也不得因为样板有 61 个节点就按同样粒度铺开——节点粒度由 §2 的判定三问决定，不由样板行数决定。

---

## 10. 填充流程（后续按此执行）

1. **建分支图**：loader 读 `framework/branches.json`，生成 `BR` 节点与 `parent_of`、`cross_class` 边；补 `scope_definition` 与 `affected_layers`。
2. **建文本链**：先 `TX`，再 `TW`，再 `witness_of` / `derived_from`。原本已佚也建根节点（`extant: false`），链不断。
3. **建概念与定理**：每个概念先写现代定义 + `definition_source`，再补 `occurrences`；每个定理先写 `assumptions` 与 `proof_status`。
4. **建问题层**：先找原始表述，找不到就 `U` 并写线索；不要用后世教科书表述冒充原始表述。重述用 `reformulates`，不写成解决。
5. **建失败层**：只在有具体缺陷步骤时建；三类失败各自补齐强制字段（§4.7）。
6. **建记号层**：与概念分开建；每个译名一个 `NO:` 节点，中文译名必须落到译著与页码，查不到就 `U`。
7. **建观点层**：有争议的说法建 `ST:`，用 `contradicts` 互连；不要把两种说法压成一条边。
8. **跑校验**：JSON 解析 → ID 唯一 → 边端点存在 → 端点类型符合 §5.6 → 无环 → 权重归一 → `U` 原因非空 → `text_ref` 可解析。任一项失败不合并。
9. 所有文本产物仍按 `mathlint` 检查；`0 error` 才合并。

校验可先用 `py -3.11 -c` 快速跑结构检查；不引入图数据库。

---

## 11. 版本与扩展

- 新增对象类型：必须同时更新本文件 §2、§4、§5 与 `object-model.schema.json`，并升 `schema_version`。
- 新增边类型：**只改一处**——在 `framework/edge-signatures.yaml` 的 `edges` 列表加一条签名，然后在 `tools/` 目录运行 `py -3 -m graphlint generate`。§5.2 表、§5.6 表与 `graph.schema.json` 的 `type` 枚举/条件约束会一起重新生成；三处生成物不得手改，手改视为错误。生成后运行 `py -3 -m graphlint check-all`，确认 error 为 0。
- 新增分支：优先挂 `proposed` 扩展槽，不直接改 62 计数；确认后再修订视图。
- 拆分对象：保留旧 ID 并 `status: deprecated` + `superseded_by`；禁止原地改名重用。
- 关系新增：先在 `edge-signatures.yaml` 登记方向与约束，再生成；禁止先用 `related_to` 兜底。
- 当前 `schema_version`：节点与图包均为 `0.2`。两者分文件（`object-model.schema.json` / `graph.schema.json`），但同步升版：加节点类型必须同时改两处；加边类型只改签名表，其余由生成器处理。
- v0.2 内部修订：`targets` 的允许终结点加入 `PR`（失败路线可指向它所试图解决的问题），与 §7.5 的失败层入口说明一致；`FA→PR` 不再是非法边。
- v0.2 内部修订（2026-11-23）：同一对 `BR` 上的 `parent_of` 与 `cross_class` 互斥由 error 降为 warning（见 §5.6 B.5）。降级后 `research/ackermann-1928` 的"三处归属"从结构非法变为归属重叠提示，取舍仍由人工决定。

## 12. 存储与规模

- **量级假设**：62 分支 + 数千年事件 + 数千节点、约 1–2 万条边。
- **单文件**：`graph.json`，结构 `{schema_version, meta, nodes[], edges[]}`，边按 `type` 排序、节点按 ID 排序，便于 diff。数千节点仍在单文件可维护范围内。
- **分片**：超过约 5000 条边时按十类视图切 `graph/<class>.json`，每片自带 `nodes`/`edges`，ID 全局唯一；加载时合并再校验跨片边。
- **SQLite 备选**：三张表 `nodes(id, type, json)`、`edges(id, from, to, type, json)`、`claims(...)`，配 `from`/`to`/`type` 索引。适合需要按关系查询而不想全量载入的场景。**不需要图数据库**：查询模式是"取子图/邻域"，SQLite 递归 CTE 足够。
- **前端**：复用 StudyHub 已有图谱渲染。只在中间加一层适配，把 `{nodes, edges}` 映射为它既有的 node/link 结构（节点标签取 `labels.zh`，边标签取 `type`，样式按 `grade` 区分）；不另起可视化方案，不改它的数据契约。
- **一致性**：`branches.json` 是分支目录的唯一真源；图包里的 `BR` 节点由它投影生成，不手改，避免两处漂移。
