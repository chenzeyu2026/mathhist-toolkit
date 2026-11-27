# 变更记录 / Changelog

本文件记录对外可见的变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循语义化版本。
All notable changes are recorded here. Format loosely follows Keep a Changelog; versions follow semantic versioning.

## [Unreleased]

### 新增 / Added

- **社会史 schema 与 `resembles` 非证据边**：节点类型由 14 增至 16（新增 `org` / `journal`，前缀 `ORG:` / `JRN:`）；边类型由 31 增至 36。新增 `member_of`、`employed_by`、`publishes_in`（person→journal）、`published_in`（text→journal）与 `resembles`（TH/ME，无向、非证据、provisional）。`resembles` 当前闸门为 0/3，`check` 在 `samples/` 与 `pilots/` 中遇到它直接报 `EDGE_PROVISIONAL`，不写入任何实例。`publishes_in` 是人物级渠道，`published_in` 是具体篇目，两者不可混用。测试 102 → 107。

- **分支扩建第二批（P1）**：新增 `pilots/lie-groups`（14 节点 / 22 边）、`pilots/stochastic-analysis`（12 节点 / 20 边）、`pilots/non-classical-logic`（13 节点 / 19 边），分别承载李群与李代数、随机分析、非经典逻辑；三条分支仍为 `proposed`。`branches.json` 的 `proposed` 由 5 条增至 8 条。`check-all` 现为 10 个图包 / 264 节点 / 417 边，warning 仍为 60 条（全部来自既有图包）。
- **分支扩建第一批**：新增三个试点图包 `pilots/pde`（15 节点 / 26 边）、`pilots/variational-calculus`（12 节点 / 18 边）、`pilots/dynamical-systems`（13 节点 / 21 边），分别承载偏微分方程、变分法、动力系统；三条分支仍为 `proposed` 扩展槽，不进 62 计数。`branches.json` 的 `proposed` 由 4 条增至 5 条（新增 `BR-ANA-VAR`）。`check-all` 由 4 个图包 / 185 节点 / 291 边变为 7 个图包 / 225 节点 / 356 边，warning 仍为 60 条（全部来自既有图包）。
- **Issue 结构化**：每条 `Issue` 增加 `rule_id`、`pointer`（RFC 6901 JSON Pointer）与 `severity`；`--json` 输出同步包含，文本输出增加一行 `位置:`。既有 60 条 warning 的 `rule_id` 全部有值。
- **跨文件 ID 判重**：`check-all` 在单文件检查之外，检查同一节点/边 ID 是否出现在不同图包；报错信息同时给出两个文件与各自的 pointer。
- **check-all 汇总**：文本与 `--json` 都输出文件数、节点总数、边总数与各严重级计数。

### 变更 / Changed

- **边级 schema 规则单源化**：`source`/`claimant`、`attestation` 等级上限、`grade=U` 必填 `note` 的 JSON Schema 片段迁入 `edge-signatures.yaml` 的 `schema` 块，由顶层 `edge_schema_rules` 排序；`generate.py` 不再含这些常量。生成物字节未变。
- **重复 ID 文案**：单文件检查的 `NODE_ID_DUPLICATE` / `EDGE_ID_DUPLICATE` 明确写“同一图包内”，跨文件由 `check-all` 判定。
- **跨图 ID 去重**：样例 `group-theory` 的 11 个非分支实体加 `.sample` 作用域后缀（如 `CO:group.sample`、`TH:abel-ruffini.sample`），群论试点中共用的 `PE:cauchy`、`PE:klein` 加 `.group-theory`（微积分试点与非欧样例保留原名）；15 条重复边随端点同步改名。`BR-*` 分支节点是 `branches.json` 的目录投影，保持目录 ID 不变。
- **分支目录投影豁免**：`check_global_ids` 按 `branches.json` 的目录 ID 豁免分支节点，以及两端都是目录分支的 `parent_of` / `cross_class` 边；其余节点与边仍要求全局唯一。`check-all` 因此回到 0 error。
- **测试**：新增 `Issue` 字段、单文件边 ID 判重、跨文件节点/边判重与 CLI 集成用例；新增目录投影豁免用例与“全部图包全局唯一”回归断言；总数 94 → 102。

### 已知 / Known

- `check-all` 现为 **0 error / 60 warning**。60 条 warning 是既有节点缺字段（`NODE_REQUIRED`），`--strict` 下升为 error。

## [0.2.0] — 2026-11-23

图级规范与校验器落地。文档级 `mathlint` 的行为不变；本版新增 `graphlint` 与图包产物。

### 新增 / Added

- **图结构本体 v0.2**：`spec/object-model.md` 定义 14 类节点、31 类边、7 类全局不变量与 62 个分支目录（含 proposed 扩展槽）；单条节点结构由 `spec/framework/object-model.schema.json` 约束。
- **唯一真源**：`spec/framework/edge-signatures.yaml` 保存每类边的端点、方向、属性、条件必填、等级上限与释义。`graph.schema.json` 的边枚举与 `object-model.md` §5.2 / §5.6 的表格都由它生成，不再各写一份。
- **`graphlint`**：`check` / `check-all` / `generate [--check]` 三个子命令。校验节点 ID 前缀、边信封、端点类型与方向、必填属性与枚举、时间、证据等级上限、环、`parent_of` 权重和、互斥关系、孤立节点与 `claims` 引用；`--json` 输出结构化结果。
- **两个试点**：`pilots/group-theory/`（51 节点 / 80 边）与 `pilots/calculus/`（58 节点 / 102 边），用于暴露边类型与端点约束的缺口，不是全量史实。
- **样例**：`samples/group-theory.json`（13 / 15）与 `samples/non-euclidean-geometry.json`（63 / 94），作为最小图包样板。
- **测试**：`tools/tests/test_graphlint.py` 覆盖签名端点判定、`part_of` 条件必填、等级上限、时间窗独立性与 `generate --check` 漂移检测；`tools/tests/fixtures/graph_*.json` 提供四类失败反例（未知边类型、端点非法、等级超限、条件必填缺失）。
- **文档**：`docs/repository-guide.md` / `.en.md`（工具、产物地图、命名约定）、`docs/licensing.md` / `.en.md`（逐目录许可判断与第三方材料说明）。

### 变更 / Changed

- **G5 修订**：`part_of` 的终点增加 `concept` 与 `method`，指向这两类时 `note` 必填；`anchors` 的终点增加 `method`。未新增边类型。
- **G7 修订**：`text_type` 与 `witness_kind` 枚举扩充，覆盖标准、手册、勘误、发布说明、源码仓库、网页快照与提交等材料形态。
- **互斥规则降级**：`parent_of` 与 `cross_class`、`prerequisite_of` 与反向 `parent_of` 的冲突由 error 降为 warning；同一对端点上的两类关系可能都成立，先提示人工确认。
- **节点完整性**：缺字段默认按 warning 报告，`--strict` 才升为 error；既有样例与试点的历史欠账不再阻断 `check-all`。
- **CI**：安装 PyYAML 后同时运行 `mathlint` 单测、`graphlint check-all` 与 `graphlint generate --check`。

### 修复 / Fixed

- 群论试点中 Cayley 见证边的 `attestation` 与 `grade` 冲突（教材转述标成 S）→ 改为 `later_report`，`ATTESTATION_GRADE_CAP` 归零。
- `edge-signatures.yaml` 中 `abbr: NO` 被 YAML 解析为布尔值，导致生成器 `TypeError` → 全部缩写加引号。
- 缺少 PyYAML 时不再抛栈：`graphlint` 输出一句说明与安装命令，退出码为 1。
- 手改 `graph.schema.json` 或 `object-model.md` 的生成块会被 `generate --check` 报为不一致，并给出重新生成命令。

## [0.1.0] — 2026-11-14

首个版本。工具、规范、指令集、短文四件套，中英双语。
First release: linter, spec, prompt set and method note, in Chinese and English.

### 新增 / Added

- **规范**：`spec/evidence-tags.md` 与 `evidence-tags.en.md`。四级标记 `〔A｜原始文献:出处〕`、`〔S｜二手研究:出处〕`、`〔U｜未核实:原因〕`、`〔F｜流行说法:出处〕`；13 条判定规则各带正例与反例；冲突处理；T-1~T-7 待议条款。
- **工具**：`tools/mathlint`（Python 3.11，标准库实现，零第三方依赖）。`mathlint check <文件或目录> [--offline|--online] [--json] [--strict]`，六类检查、error/warn/info 三级、退出码 0/1/2。
- **指令集**：`prompts/zh/P1–P9.md`、`prompts/en/P1–P9.md`，以及三个真实段落的"改前／改后"样例（`prompts/examples/`）。
- **文档**：方法论短文（`docs/method.md` / `.en.md`）、跟练手册（`docs/walkthrough.md` / `.en.md`）、证据库设计草案（`docs/evidence-corpus-design.md` / `.en.md`，v0.2 提案，未实现）、阈值敏感性记录（`docs/threshold-sensitivity.md` / `.en.md`）。
- **验收材料**：`corpus/` 下的 4.1 万字原稿与最小修补稿，`reports/` 下的基线报告、修补报告与统一 diff。
- **工程**：`tools/scripts/selfcheck.py`（本地自检，等价于 CI）、GitHub Actions 矩阵工作流（三系统 × Python 3.11/3.12/3.13）、`CHANGELOG.md`、`CONTRIBUTING.md`、`RELEASE-CHECKLIST.md`。

### 修复 / Fixed

- 围栏代码块内的示例标签被当作真标签解析 → 增加围栏遮蔽。
- 行内代码（反引号）里的示例标签与 `【原】` 类旧写法被误报。`docs/` 上因此有 29 个假 error，现为 0。
- 未闭合标签曾中断整篇扫描 → 报错后继续。
- 目录目标被相对路径 `..` 误过滤 → 修正 `collect_files`。
- `pip install -e tools` 三处失败（`readme` 字段越界、`bdist_wheel` 缺失、离线构建依赖）→ 修正 `pyproject.toml`，README 注明安装需回仓库根目录。

### 变更 / Changed

- 九条提示词的等级字母统一为 A/S/U/F（原 `B`→`S`、`C`→`F`、`T` 改为 `S` 的必填字段）。旧字母只保留在 `prompts/README.md` 的变更记录一节。
- 仓库关闭 `core.autocrlf`，统一按 LF 存储。

### 已知限制 / Known limitations

- `--online` 只做了单元测试，未在真实网络下验证；`LINK_DEAD` 与 `NETWORK_UNREACHABLE` 的区分没有实网样本。
- 仅在 Windows 11 + Python 3.11.9 上实跑；CI 矩阵尚未执行过第一次。
- `MISSING_TAG` 的阈值（40/24）只在一份语料上观察过，没有人工标注，未校准。
- 规范的 T-1~T-7、英文文档的母语校对、`mathlint` 在 PyPI 的包名占用，均未处理。见 `RELEASE-CHECKLIST.md`。
- 证据库（`corpus/<id>#p12` 引用与相应检查）只有设计草案，工具不支持。
