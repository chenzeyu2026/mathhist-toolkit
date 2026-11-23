# 仓库指南：工具怎么跑，产物是什么关系

面向第一次打开这个仓库的人。目标是：十分钟内知道**哪个文件是规范、哪个是示例、哪个是研究记录**，并跑通两个检查器。

---

## 1. 先看三句话

1. `spec/` 是**规范**，`spec/framework/` 是它的机读骨架；其中 `edge-signatures.yaml` 是边与不变量的**唯一真源**。
2. `samples/` 是**最小示例**，`pilots/` 是**完整试点**，`research/` 是**研究记录**。后两者不是全量史实，也不代表规范。
3. `tools/` 下有两套检查器：文档级 `mathlint`，图级 `graphlint`。二者共用 `A / S / U / F` 证据等级。

---

## 2. 产物地图

```
spec/
├── evidence-tags.md / .en.md            文档级证据标记规范（v0.1）
├── object-model.md                      图结构本体（v0.2，含生成的边表）
└── framework/
    ├── edge-signatures.yaml             ★ 唯一真源：31 类边 + 7 类不变量
    ├── graph.schema.json                ← 由 edge-signatures.yaml 生成
    ├── object-model.schema.json         节点结构约束（手写）
    ├── branches.json                    62 分支目录 + 扩展槽
    ├── samples/                         两个最小图包
    │   ├── group-theory.json            13 节点 / 15 边
    │   └── non-euclidean-geometry.json  63 节点 / 94 边
    └── pilots/                          两个完整试点
        ├── group-theory/graph.json      51 节点 / 80 边
        └── calculus/graph.json          58 节点 / 102 边
```

| 产物 | 回答什么 | 是否正式规范 | 机器可读 |
|---|---|---|---|
| `evidence-tags*.md` | 一句话凭什么（A/S/U/F） | 是 | 否 |
| `object-model.md` | 有哪些对象、对象间允许什么关系 | 是 | 否（边表由 YAML 生成） |
| `edge-signatures.yaml` | 每类边的端点、方向、属性、不变量 | 是 | 是 |
| `graph.schema.json` | 单条边的 JSON 结构 | 是（生成物） | 是 |
| `object-model.schema.json` | 单条节点的 JSON 结构 | 是 | 是 |
| `branches.json` | 62 个分支与扩展槽 | 是 | 是 |
| `samples/` | “最小可用图包长什么样” | 否 | 是 |
| `pilots/` | “真实分支压满后长什么样、哪里别扭” | 否 | 是 |
| `research/` | 映射实验、约束工具选型 | 否 | 部分 |

**关系**：`edge-signatures.yaml` 生成 `graph.schema.json` 与 `object-model.md` 的 §5.2 / §5.6 表格；`graphlint` 用同一份 YAML 做校验。三者不会各说各话，因为只有一个真源。

---

## 3. 环境与依赖

| 项 | 要求 |
|---|---|
| Python | 3.11+（本机 3.13.14 实测；CI 矩阵写的是 3.11/3.12/3.13） |
| `mathlint` | 仅标准库，无第三方依赖 |
| `graphlint` | PyYAML ≥ 6.0 |
| 运行位置 | 命令都在 `tools/` 下用 `-m` 调用；包安装后可在任意目录调用 |

```bash
cd mathhist-toolkit/tools
py -3 -m pip install "PyYAML>=6.0"   # 仅 graphlint 需要
```

Windows 提示：如果 `py -3` 不存在，用 `python`；如果 `python` 被指向应用商店别名，装好 Python 后用 `py -3`。

---

## 4. 工具逐条说明

### 4.1 `mathlint`：文档级证据标记检查

- **做什么**：解析 `〔A｜原始文献:…〕`、`〔S｜二手研究:…〕`、`〔U｜未核实:…〕`、`〔F｜流行说法:…〕`，检查标记语法、来源类型与等级是否自洽、引文格式、`U` 是否写原因、同一引用是否被标成不同等级。
- **输入**：`.md` 文件或目录（递归收集 `.md`）。
- **输出**：按文件列 error / warn / info，末尾汇总；`--json` 输出结构化结果。
- **失败**：

```text
$ py -3 -m mathlint check tests/fixtures/invalid.md
...
合计：13 error / 1 warn / 0 info · exit=1
```

常见错误码：`GRADE_SOURCE_MISMATCH`（等级与来源类型不符）、`MISSING_REASON`（`U` 没写原因）、`BAD_ISBN` 等。

- **退出码**：0 无 error；1 有 error，或 `--strict` 且有 warn；2 参数/路径错误。
- **参数**：`--offline`（默认，不联网）、`--online`（额外探测 DOI/URL）、`--json`、`--strict`。

### 4.2 `graphlint check`：校验单个或多个图包

- **做什么**：按 `edge-signatures.yaml` 校验节点 ID、边信封、端点存在与类型、方向、属性必填与枚举、时间、证据等级上限、环、权重和、互斥、孤立节点、`claims` 引用等。
- **输入**：一个或多个 `graph.json`（含 `nodes` / `edges` 的 JSON）或目录。
- **输出**：按 `== error（N）==` / `== warning（N）==` 分组；每条给出文件、边/节点 ID、`位置:`（RFC 6901 JSON Pointer）、说明、实际值、期望值、依据；末尾按文件与总计。`--json` 每条 issue 含 `rule_id`、`pointer`、`severity`，并含 `nodes` / `edges` 计数。
- **失败长什么样**：

```text
== error（1）==
  [ATTESTATION_GRADE_CAP] spec/framework/pilots/group-theory/graph.json :: E:TW:cayley-1854.print>witness_of>TX:cayley-1854
      说明: attestation=textbook_simplification 时 grade 上限不满足：实得 S（期望 F 或 U）。教材转述不能支撑 S 级。
      实际: attestation=textbook_simplification, grade=S
      期望: grade ∈ {F, U}
      依据: A=亲见原件；S=二手研究；F=教材/流行说法；U=未核实。不要为了过关冒充一手文献。
```

（这是构造出来的示意输出；仓库里该边现已改为 `later_report`，实际不再报错。）

- **退出码**：0 无 error；1 有 error（或 `--strict` 且有 warning）；2 没找到图包。
- **参数**：`--strict`（节点完整性 warning 升 error，并让 warning 返回非零）、`--json`、`--max-items N`（默认 25，0 显示全部）。

### 4.3 `graphlint check-all`：跑全部样例与试点

- **做什么**：等价于 `graphlint check spec/framework/samples spec/framework/pilots`，并额外做**跨文件 ID 判重**：同一节点/边 ID 出现在两个图包时，报 `NODE_ID_DUPLICATE` / `EDGE_ID_DUPLICATE`，消息给出两个文件与各自的 JSON Pointer。
- **输入**：无。
- **当前结果**：4 个图包、185 个节点、291 条边，**0 error / 60 warning**，退出码 0。60 条 warning 全部是 `NODE_REQUIRED`。跨图 ID 已按作用域区分：样例 `group-theory` 的非分支实体带 `.sample`，群论试点中的 `PE:cauchy`、`PE:klein` 带 `.group-theory`；`BR-*` 与 `parent_of`/`cross_class` 是 `branches.json` 的目录投影，按目录 ID 豁免判重。
- **汇总行**：`汇总：error N / warning N · files N / nodes N / edges N`；`--json` 的 `summary` 同名字段。
- **`--strict`**：60 条 warning 升为 error，合计 60 error，退出码 1。

### 4.4 `graphlint generate`：从唯一真源生成

- **做什么**：读 `spec/framework/edge-signatures.yaml`，重写 `graph.schema.json` 的边枚举、条件约束与 `$comment`，并替换 `spec/object-model.md` 中带 `<!-- GENERATED:… -->` 标记的表格块。
- **输入**：无。
- **输出**：写入两个文件；`--check` 不写文件，只报告生成物是否与 YAML 一致。
- **失败**：

```text
生成物与 edge-signatures.yaml 不一致：
  - spec/framework/graph.schema.json
运行 py -3 -m graphlint generate 重新生成。
```

- **规则**：改边类型、端点、不变量级别，**只改 YAML**。手改 schema 或文档里的生成块会在下一次 `generate --check` 中暴露，并被视为错误。

### 4.5 `audit`：规则集一致性审计

在 `tools/` 下运行 `py -3 -m audit [kernel|domain|criticality|all]`。

- **做什么**：复现证据标记规范内部推导：v0/v1 规则的冲突与不定、六维域剔除与去重、逐条规则的关键度。
- **输入**：无。
- **输出**：`kernel` / `domain` / `criticality` 三节文本表。
- **失败**：规则计数与文档不一致时以文本差异体现；无固定退出码约定（正常返回 0）。

### 4.6 `tools/scripts/selfcheck.py`：本地等价 CI

- **做什么**：跑全部单元测试（102 个：`mathlint` 77 + `graphlint` 25）+ 3 个 fixture + 3 段样例，逐项打印 `PASS/FAIL` 与期望计数。
- **输入**：无。
- **输出**：`self-check PASSED` 或失败项列表。
- **退出码**：0 全过；1 有失败。
- **注意**：它**不跑 `graphlint check-all`**；图检查目前靠 `check-all` 与 `generate --check`。

### 4.7 `tools/pyproject.toml`：安装与入口

- **做什么**：声明包名 `mathlint`、版本、Python ≥ 3.11、依赖 `PyYAML>=6.0`，并注册两个命令 `mathlint` 与 `graphlint`；`packages` 只含 `mathlint` 与 `graphlint`（`audit` 与 `scripts/` 不打包）。
- **输入**：无。
- **输出**：`pip install -e tools` 后可在任意目录调用 `mathlint` / `graphlint`。
- **失败**：离线或取不到构建依赖时，`pip` 会在构建隔离阶段失败；此时不要安装，直接在 `tools/` 下用 `py -3 -m ...`。
- **注意**：包名是 `mathlint`，仓库名是 `mathhist-toolkit`；发布 PyPI 前需要决定包边界。

### 4.8 硬编码路径与可移植性

工具代码本身没有硬编码本机路径：`graphlint/signatures.py` 用 `Path(__file__)` 推导仓库根，`mathlint` 只处理传入路径。公开副本中的文档示例已统一改为占位符：

- `<repo>` 表示仓库根目录；
- `<workspace>` 表示仓库所在的上一级目录；
- `~` 表示当前用户主目录。

`docs/walkthrough*.md`、`docs/threshold-sensitivity*.md`、`docs/quickstart-check.md` 与 `research/graph-constraint-tooling/appendix/domain-range-prototype.py` 中的本机路径已替换。照抄示例前，请先把占位符换成本机实际路径。

---

## 5. 常用组合

```bash
cd tools

# 提交前最小闸门
py -3 tools/scripts/selfcheck.py
py -3 -m graphlint check-all
py -3 -m graphlint generate --check

# 只看某个图包
py -3 -m graphlint check ../spec/framework/pilots/calculus/graph.json

# 机器可读结果
py -3 -m graphlint check-all --json

# 改完边签名后
py -3 -m graphlint generate
py -3 -m graphlint generate --check
py -3 -m graphlint check-all
```

---

## 6. 目录与命名约定

- **ID 前缀**：`BR-`、`CO:`、`TH:`、`PR:`、`ME:`、`TY:`、`FA:`、`NO:`、`PE:`、`TX:`、`TW:`、`EV:`、`TP:`、`ST:`；`CLM:` 只存在于 `claims[]`。
- **边 ID 由端点派生**：`E:<from>><type>><to>`，重复时加 `#2`、`#3`。
- **文件命名**：分支图包用 `graph.json`，长文本用 `text.md`，试点说明用 `report.md`；样例用 `<branch>.json`。
- **生成物**：`graph.schema.json` 与 `object-model.md` 的生成块带 `GENERATED` 标记，**勿手改**。
- **提交信息风格**：英文一句话标题，正文可中文，列改动文件与理由（见 `git log`）。
- **`.gitignore` 当前覆盖** `__pycache__/`、`*.py[cod]`、虚拟环境、构建产物、`*.egg-info/`、`.pytest_cache/`，以及 `literature/`、`reports/literature/`、`*.pdf`、`*.docx` 与临时文件。

---

## 7. 想加一张新图，从哪开始

1. 读 `spec/object-model.md` §3–§5，确认真实需要的节点类型与边类型。
2. 只用 `spec/framework/edge-signatures.yaml` 里已登记的边；缺类型先提规范变更，不要就地扩表。
3. 复制 `spec/framework/samples/group-theory.json` 当骨架，保持 `schema_version: "0.2"`、`nodes`、`edges` 三个顶层键。
4. 跑 `py -3 -m graphlint check <你的文件>`，按 error 修；warning 按需处理。
5. 长论证、引文放在同目录 `text.md`，节点用 `text_ref: "doc:<文件名>#<锚点>"` 指回；不要让图承载长文。

---

## 8. 哪些东西不是规范

- `research/`：映射实验与工具选型，结论可能被推翻，引用前先看日期。
- `pilots/` 与 `samples/`：用来暴露缺口的实例，史实未全量核对，不能当史学结论引用。
- `reports/`：过程记录，含基线/修补数字与文献传递申请；公开仓库不包含 `reports/literature/` 下的他人 PDF。
- `corpus/`：作者本人文章的验收语料，不是通用语料库。
- `literature/`：本地参考 PDF，未跟踪，**不要提交**。
