# mathhist-toolkit

> 首次公开：2026-11-23 · 首发 commit [`eaae8c8`](https://github.com/chenzeyu2026/mathhist-toolkit/commit/eaae8c823e093f9d92023e7be01f423352bb500d) · [优先权与引用说明](PRIORITY.md)

写数学史、数学思想演化时用的两件套：**证据标记规范 + 检查器**，以及**图结构本体 + 校验器**。

- 文档级（v0.1，可用）：给论断挂 `A / S / U / F` 证据标记，`mathlint` 检查标记语法、来源类型与等级是否自洽。
- 图级（v0.2，结构定稿、内容待填）：把概念、定理、问题、文本、人物、事件写成 `{nodes, edges}`，`graphlint` 校验 31 类边、7 类不变量与节点完整性。

> English: [README.en.md](README.en.md)

## 它解决什么问题

数学史写作里有两类信息最难检查：

1. **一句话凭什么**——"莱布尼茨 1684 年发表了微积分"是亲见原刊、二手研究，还是教材转述？`mathlint` 把这件事变成可解析的标记，并在等级与来源类型冲突时报错。
2. **一件事和另一件事怎么连**——某个概念属于哪个分支、谁证明了它、哪份文本支撑它、两种说法是否冲突？`object-model` 把关系写成带时间、来源、等级、置信度的边，`graphlint` 检查端点类型、方向、权重、环与条件必填。

两者共用同一套 `A / S / U / F` 口径，可以互相引用，但解决的是不同层的问题。

## 十分钟上手

需要 **Python 3.11 或更高**（本机用 3.13.14 实测）。

- `mathlint`：仅标准库，**零第三方依赖**，不需要安装。
- `graphlint`：需要 **PyYAML ≥ 6.0**（`py -3 -m pip install "PyYAML>=6.0"`）。

```bash
cd mathhist-toolkit/tools

# 1) 文档级检查：3 个样例，全部 0 error / 0 warn / 0 info，退出码 0
py -3 -m mathlint check ../prompts/examples

# 2) 图级检查：4 个图包，0 error / 60 warning，退出码 0
py -3 -m graphlint check-all

# 3) 生成物同步检查：schema 与文档表格是否与唯一真源一致，退出码 0
py -3 -m graphlint generate --check
```

Windows 上如果 `py -3` 不可用，用 `python`（需 3.11+）；如果 `python` 被指向应用商店别名，装好 Python 后仍可用 `py -3`。

再看两个会失败的例子：

```bash
# 13 条 error / 1 warn，退出码 1（旧式简写、未知等级、ISBN 校验位错、编者导言标成 A 等）
py -3 -m mathlint check tests/fixtures/invalid.md
```

`graphlint` 的失败形态见 [docs/repository-guide.md](docs/repository-guide.md) 第 4.2 节：它按 `== error（N）==` / `== warning（N）==` 分组，逐条给出文件、边/节点 ID、实际值、期望值与可读说明。

可选安装（从仓库根目录执行；需要能取到构建依赖）：

```bash
pip install -e tools
mathlint check prompts/examples
graphlint check-all
```

不安装时，`py -3 -m mathlint` / `py -3 -m graphlint` 与安装后的命令等价。

## 仓库结构

| 路径 | 是什么 | 性质 |
|---|---|---|
| [`spec/evidence-tags.md`](spec/evidence-tags.md) / [`.en.md`](spec/evidence-tags.en.md) | 证据标记规范：语法、判定规则、冲突处理、待议条款 | 正式规范 |
| [`spec/object-model.md`](spec/object-model.md) | 图结构本体：14 类节点、31 类边、约束、存储与挂载 | 正式规范 |
| [`spec/framework/edge-signatures.yaml`](spec/framework/edge-signatures.yaml) | 31 类边签名、7 类不变量、释义的**唯一真源** | 正式规范（机读） |
| [`spec/framework/graph.schema.json`](spec/framework/graph.schema.json) | 图包 JSON Schema；边枚举与条件约束由上面 YAML 生成 | 生成物，勿手改 |
| [`spec/framework/object-model.schema.json`](spec/framework/object-model.schema.json) | 单条节点记录的结构约束 | 正式规范（机读） |
| [`spec/framework/branches.json`](spec/framework/branches.json) | 62 分支目录与扩展槽 | 正式规范（机读） |
| [`spec/framework/samples/`](spec/framework/samples) | 两个最小图包样板（群论 13 节点/15 边，非欧几何 63 节点/94 边） | 示例 |
| [`spec/framework/pilots/`](spec/framework/pilots) | 两个完整试点（群论 51 节点/80 边，微积分 58 节点/102 边） | 试点，不是全量史实 |
| [`tools/mathlint/`](tools/mathlint) | 文档级检查器（标准库） | 工具 |
| [`tools/graphlint/`](tools/graphlint) | 图级校验/生成器（PyYAML） | 工具 |
| [`tools/audit/`](tools/audit) | 规则集一致性审计（冲突、去重、关键度） | 工具 |
| [`prompts/`](prompts) | P1–P9 写作提示词，中英各一套 | 文档 |
| [`docs/`](docs) | 方法论、跟练、设计草案、回归池、上手实测 | 文档；含历史记录 |
| [`corpus/`](corpus) | 4.1 万字验收原稿与最小修补稿（作者本人文章） | 验收材料 |
| [`reports/`](reports) | 基线/修补报告、发布自检、文献传递申请 | 过程记录；公开副本已排除他人 PDF |
| [`research/`](research) | 本体映射与约束工具选型的独立研究记录 | 研究记录，非规范 |
| `literature/` | 本地参考 PDF（不随公开仓库分发） | 仅本地 |

更细的入口、依赖、失败形态与产物关系见 [docs/repository-guide.md](docs/repository-guide.md)；英文版见 [docs/repository-guide.en.md](docs/repository-guide.en.md)。

## 两套规范怎么配合

```
写作正文 ──〔A/S/U/F 标记〕──> mathlint 检查
   │
   └── 抽成对象与关系 ──> graph.json ──> graphlint 检查
                              │
                        edge-signatures.yaml（唯一真源）
                              ├─ 生成 graph.schema.json
                              └─ 生成 object-model.md §5.2 / §5.6 表格
```

- **证据等级**回答"这句话凭什么"；**边**回答"这两件事是什么关系"。边也带 `grade` 与 `attestation`，所以图里的每一条断言同样可追溯。
- 改边类型或不变量的级别，只改 `edge-signatures.yaml`，再跑 `py -3 -m graphlint generate`。`graph.schema.json` 与本体文档里的边表都是生成物，手改视为错误。

## 现状（随仓库同步）

| 项 | 数值 |
|---|---:|
| 节点类型 | 14 |
| 边类型 | 31 |
| 全局不变量 | 7 |
| 分支目录 | 62（含 proposed 扩展槽） |
| 图包 | 4（2 样例 + 2 试点） |
| `graphlint check-all` | **0 error / 60 warning**（warning 均为既有节点缺字段） |
| `graphlint check-all --strict` | 60 error / 0 warning（历史欠账被提升） |
| 单元测试 | 94 个，全部通过（`mathlint` 77 + `graphlint` 17） |
| 受跟踪文件 | 124 |

60 条 warning 集中在 `pilots/calculus`（52）、`pilots/group-theory`（7）与 `samples/group-theory`（1），都是 `chains`、`occurrences` 等历史缺字段，不是本轮引入。

## 工具

| 命令（在 `tools/` 下） | 作用 | 输入 | 输出 |
|---|---|---|---|
| `py -3 -m mathlint check <路径>` | 文档级证据标记检查 | `.md` 文件或目录 | error/warn/info 按文件汇总；退出码 0/1/2 |
| `py -3 -m graphlint check <路径>` | 校验单个/多个图包 | `graph.json` 或目录 | 按级别分组的违例；退出码 0/1 |
| `py -3 -m graphlint check-all` | 校验 `samples/` 与 `pilots/` 全部图包 | 无 | 按文件与汇总计数 |
| `py -3 -m graphlint generate [--check]` | 生成 schema 与文档表格；`--check` 只测漂移 | 无 | 写入生成物，或报告是否一致 |
| `py -3 -m audit [kernel\|domain\|criticality\|all]` | 规则集一致性审计 | 无 | 文本表格 |
| `py -3 tools/scripts/selfcheck.py` | 本地等价 CI：单测 + fixture + 样例 | 无 | PASS/FAIL，退出码 0/1 |

## 已知限制

- **60 条节点 warning 是历史欠账**：样例与试点没有补齐 `chains`、`occurrences`、`name_variants` 等必填字段。默认按 warning 报告，`--strict` 下计 error。
- **`graphlint` 的单元测试覆盖契约，不覆盖全部语义**：17 个测试覆盖签名端点、条件必填、等级上限、时间窗独立性与 `generate --check` 漂移；更复杂的史实判断仍靠人工。
- **CI 尚未在真实 GitHub 上运行过**：仓库无远端；`.github/workflows/ci.yml` 已覆盖 `mathlint` 与 `graphlint`，但首次推送后才能验证。
- **`graphlint` 的错误信息是给人读的中文**：适合当前阶段，未提供稳定的机器可读错误码（`--json` 已提供结构化输出）。
- **文档仍以中文为主**：仓库指南与许可说明已有英文版（`docs/repository-guide.en.md`、`docs/licensing.en.md`），本体与边签名的细部说明仍只有中文。
- **仓库目录名仍是 `mathhist-toolkit`**，包名是 `mathlint`；改名会影响文档中的路径示例。

## 许可

- **代码**（`tools/` 及相关脚本）：Apache License 2.0，见 [LICENSE](LICENSE)。
- **文档与规范**（`spec/`、`docs/`、`prompts/`、README）：CC BY 4.0，见 [LICENSE-docs](LICENSE-docs)。
- **`corpus/`**：作者本人撰写的验收文章，随仓库以 CC BY 4.0 提供。
- **`research/`**：作者本人的研究记录，随仓库以 CC BY 4.0 提供。
- **`reports/`**：作者本人的过程记录，随仓库以 CC BY 4.0 提供；不含他人 PDF、扫描件或长引文。
- **`literature/`**：他人文献，只作本地参考，**不随仓库分发**，不在上述许可范围内。

逐项判断依据与第三方材料说明见 [docs/licensing.md](docs/licensing.md)；英文版见 [docs/licensing.en.md](docs/licensing.en.md)。

引用示例：

```
mathhist-toolkit, 证据标记规范与图结构本体, CC BY 4.0
```

## 状态

- `mathlint` v0.1：可用，未发布到 PyPI。
- 图结构本体 v0.2：结构定稿，内容待填；两个试点用来暴露缺口，不代表全量史实。
- 仓库**无远端、未推送、未申请 DOI**；CI 配置存在但未在真实 GitHub 运行。
