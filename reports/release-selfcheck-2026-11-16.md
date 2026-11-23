# 发布前自检报告（v0.1.0）

> 日期：2026-11-16
> 范围：`mathlint` 项目（仓库目录名仍为 `mathhist-toolkit`），三项自检——CI 实跑核查、PyPI 包名核查、中英一致性自查。
> 约束：不改规则语义，不动 R1–R13 判定逻辑，不改 `tools/mathlint/` 的检查行为。本次改动全部落在文档与包元数据。
> 环境：Windows 11 · PowerShell 5.1 · Python 3.11.9 / 3.12.9 / 3.13.14 · git 2.56.1

## 结论摘要

| 项 | 结论 | 是否阻塞发布 |
|---|---|---|
| 1. CI 实跑 | 三个 step 在 3 个 Python 版本上**全部通过**，无会失败、无环境不匹配；发现 4 个缺口（无 lint 阶段、classifiers 漏版本、CI 不装包、无长描述），其中 1 个已就地修掉 | 不阻塞代码发布；CI 覆盖面需你决定是否补 |
| 2. PyPI 包名 | `mathlint`、`mathhist`、`mathhist-toolkit` 在 PyPI 上**均未被占用**，可直接使用 | 不阻塞；包名已定为 `mathlint`（见 §六），长描述仍缺 |
| 3. 中英一致性 | 规范与 13 条规则逐条等价，A/S/U/F 四级表述一致；抓到 13 处事实性/术语性不一致，已全部就地修掉；另 7 处留待裁决的项已全部处理（§3.6）：6 项就地修改，第 7 项「来源不明」于 2026-11-16 裁决为 `U`，规范 R8(c) 与 method 文档已对齐 | 无未决项 |

`RELEASE-CHECKLIST.md` §0「机器可验证部分」五项现已全部可打勾：selfcheck 全 PASS、`--strict` 0/0、`--version` 与 `pyproject.toml` 一致（0.1.0）、tag `v0.1.0` 指向提交 `6ee89fb`（对应 CHANGELOG 的 0.1.0 节）、`git ls-files` 无 `__pycache__`/`.venv`。

---

## 一、CI 实跑核查

### 1.1 复现方式

`.github/workflows/ci.yml` 的矩阵是 3 系统 × Python 3.11/3.12/3.13，三个 step 都 `working-directory: tools`，且**全程没有安装步骤**——包是从工作目录直接导入的。因此本地可以逐字复现，不需要网络：

| workflow step | 命令（cwd=`tools`） | 3.11 | 3.12 | 3.13 |
|---|---|---|---|---|
| Unit tests | `python -m unittest discover -s tests -v` | ✅ 68 tests OK | ✅ | ✅ |
| Acceptance checks | `python scripts/selfcheck.py` | ✅ PASS | ✅ PASS | ✅ PASS |
| CLI smoke test | `python -m mathlint check tests/fixtures/valid.md --strict` | ✅ 0/0，exit=0 | ✅ | ✅ |

`selfcheck.py` 的四项断言（脚本实跑输出）：

```
PASS  tests/fixtures/valid.md      expected 0 error / 0 warn, got 0 / 0
PASS  tests/fixtures/invalid.md    expected 13 error / 1 warn, got 13 / 1
PASS  tests/fixtures/edge.md       expected 0 error / 4 warn, got 0 / 4
PASS  ../prompts/examples          expected 0 error / 0 warn, got 0 / 0
```

### 1.2 结论：workflow 本身不会失败

逐项排查了跨平台风险，没有发现会红的点：

- 零第三方依赖，只用标准库；`tools/pyproject.toml` 的 `dependencies = []` 与实现相符。
- 路径全部走 `pathlib`/`os.path`，测试通过 `sys.path.insert(0, parents[1])` 定位 `tools/`，不依赖 cwd 之外的东西。
- 读写文件处显式 `encoding="utf-8"`，不会因 Linux/macOS 默认编码或 Windows cp936 而崩。
- 无 `sys.platform` / `os.sep` 分支，无子进程调用外部命令。
- `.gitattributes` 是 `* text=auto eol=lf`，checkout 到 ubuntu 后不会因 CRLF 影响 fixture 比对。

**唯一的环境不匹配发生在本机而非 CI**：本机 `python` 被 Windows「应用商店别名」劫持（退出码 9009），必须改 `py -3.11`；CI 上 `setup-python` 会提供真实的 `python`，不受影响。这条 README 与 `docs/quickstart-check.md` 都已写明。

### 1.3 发现的缺口（不是失败项）

1. **workflow 里没有 lint 阶段。** 三个 step 分别是单测、selfcheck、CLI 冒烟，没有任何 ruff/flake8/pyflakes 步骤。你要求核查「lint 步骤」，实际是不存在。我没有擅自加：加 ruff 等于新增一个仅开发期使用的第三方依赖，与仓库「零依赖」的定位有张力，需要你拍板。若要加，最小形态是 `pip install ruff && ruff check mathlint tests scripts`（可只用默认规则集）。
2. **矩阵测 3.12/3.13，但元数据只声明 3.11。** 已修（见 §四-12）。
3. **CI 从不安装包，`[project.scripts]` 入口完全没被覆盖。** 我在临时 venv 里手工验证过：`pip install -e tools` 能构建，`mathlint --version` 输出 `mathlint 0.1.0`，`python -c "import mathlint"` 正常。所以入口本身是好的，只是 CI 不测。建议后续加一步 `pip install -e .` + `mathlint --version`；代价是 CI 首次需要联网取 `setuptools`/`wheel`。
4. **`license = { text = "Apache-2.0" }` 与 `License :: OSI Approved :: …` classifier 属 PEP 639 之前的写法**，新版 setuptools 会告警（本次本地安装未失败）。低优先级。
5. **workflow 顶部注释已过时**：写着「this machine has no network」，但本机现在能访问 PyPI（见 §二）。该注释不影响运行，仅影响读者判断。
6. `actions/checkout@v4`、`actions/setup-python@v5` 均可正常工作；`setup-python` 是否已到 v6、v5 是否仍在推荐列表，我无法离线确认，发布前在 GitHub Marketplace 上核一眼（清单 §6 已列此项）。

> 说明：CI 至今没在真实 GitHub 上跑过，这一点 README 第 73 行写得很清楚。本次能做的是「工作流语法可解析 + 每条命令本地绿」，**不能**替代第一次真机运行。

---

## 二、PyPI 包名核查

### 2.1 方法

不靠搜索页（可能被缓存或改版），直接打 PyPI 的 JSON API，看 HTTP 状态码：项目存在返回 200，不存在返回 404。

```powershell
curl.exe -s -o NUL -w "%{http_code}" "https://pypi.org/pypi/<name>/json"
```

### 2.2 结果

| 候选名 | HTTP | 判定 |
|---|---|---|
| `mathlint`（当前 `pyproject.toml` 的 `name`） | 404 | 未被占用 |
| `mathhist` | 404 | 未被占用 |
| `mathhist-toolkit` | 404 | 未被占用 |
| `requests`（对照组） | 200 | 说明网络与判定方法有效 |

同时用 `pip index versions <name>` 复核，三个名字均为 `No matching distribution found`，与 404 一致。

### 2.3 结论与注意事项

- **三个候选名现在都可以直接使用**，不存在被抢注的问题。
- PyPI 的 `-`/`_`/`.` 归一化后同名：`mathhist-toolkit` 与 `mathhist_toolkit` 是同一个名字，注册一个即占住两个。
- 404 只证明「此刻没有这个项目」。PyPI 上传时还会对「与既有项目过于相似」的名字做拦截，这一层无法事先查询；若要保险，先上传一个 0.0.1 占位版本。
- **命名已定**：distribution 名、`import` 名、控制台命令统一为 `mathlint`（理由：短、特殊、好搜）。仓库目录名暂不改，代价与取舍见 §六。
- **缺长描述**：我检查了安装后的元数据，`Description` 长度为 0（`pyproject.toml` 没有 `readme` 字段，因为 setuptools 不允许指向包目录之外的 `../README.md`，这是 `docs/quickstart-check.md` 卡点 3 的遗留）。若真要上 PyPI，项目页会是一片空白。最小做法是在 `tools/` 下放一份 `README.md` 并加 `readme = "README.md"`。

---

## 三、中英一致性自查

### 3.1 方法与覆盖范围

逐对比对：`spec/evidence-tags.md` ↔ `.en.md`、`docs/{method,walkthrough,threshold-sensitivity,evidence-corpus-design}.md` ↔ `.en.md`、`prompts/zh/P1–P9.md` ↔ `prompts/en/P1–P9.md`（共 23 对文件）。除人工逐段读，另用脚本做了机械核对：

- 标题层级与数量、代码块数量、行数：23 对**全部一致**，无缺章、无错级。
- 数字集合：只存在「41 070 / 41,070」这类千分位写法差异，无实质数字冲突。
- `〔…〕` 片段逐条比对：两套文档内的标记示例逐字相同。
- `T-*` / `R*` 交叉引用集合：一致。
- **记录输出 vs 实跑输出**：把 `docs/walkthrough{,en}.md` 里的代码块抽出来，用当前代码重跑同命令，逐行比对——3 个完整块**逐字一致**（18/18、8/8、21/21 行）；第 4 块是节选，首 4 行与末 2 行一致（实际 345 行）。
- 文档里的统计数字全部复算：96 个 `LEGACY_MARKER`、93 条新标记、`warn` 242→227、缺口 29+17+3=49、`MISSING_TAG` 178、阈值表 20/30/40/50/60/80 的六组数（277/265/242/209/179/123 → 277/265/244/214/185/131）——**全部与文档一致**。

### 3.2 A/S/U/F 四级标签：表述一致

这是本次重点，逐条核对结果：

| 核对点 | 结果 |
|---|---|
| 四级名称与含义（§1.1 表 4 行 × 4 列） | 一致。差异仅在英文散文名，见 §3.4-3 |
| 「可否单独支撑论断」（可以／须与 A 对读／不可以） | 逐格一致 |
| 语法（`〔〕`、`｜` U+FF5C、冒号优先半角、单字符等级、出处非空） | 一致 |
| 来源类型词与等级的绑定（原始文献↔A、二手研究↔S、未核实↔U、流行说法↔F） | 一致；解析器两套词表 `原始文献/二手研究/未核实/流行说法` 与 `primary/secondary/unverified/popular` 均已支持 |
| 关于 B/C/T 的说明（B→S、C→F、T 是 S 的必填字段） | 一致 |
| R1–R13 的条数、编号、判定、(a)(b)(c) 分项、正例/反例/Tool 判定（自动/部分/不可） | 逐条一致，无缺条、无错位 |
| §3 速查表 13 行 | 行数与取值一致 |
| §4 冲突处理（先低后高、A+F 的「误说/纠正」结构、U 可与任意等级并存） | 一致 |
| §5 能验/不能验 7 行 | 一致 |
| §6 T-1…T-7 | 一致，含 T-2 自陈「与第一期做法相反」这句 |
| P1–P9 的步骤编号、表格列、禁止项 | 逐份一致；P5 两版都声明「不涉及分级字母」 |

结论：**A/S/U/F 在规范两版之间没有表述漂移**。下面的问题都出在「规范 ↔ 提示词/使用文档」之间，或纯粹是翻译与事实性笔误。

### 3.3 已就地修掉的不一致（13 处）

| # | 文件:行 | 原文 | 改后 | 依据 |
|---|---|---|---|---|
| 1 | `docs/walkthrough.md:116` | `标记 2 条 · 论断 1 段（无标记 0 段）` | `标记 1 条 · …` | `example-1.md` 实跑只有 1 条标记；改后该代码块与实跑逐字一致 |
| 2 | `docs/walkthrough.en.md:114` | 同上 | 同上 | 同上 |
| 3 | `docs/walkthrough.md:212` | …`issues` 数组里每条都有… | …`files[].issues` 数组里每条都有… | `--json` 顶层键是 `files/summary`，问题列表在 `files[].issues` |
| 4 | `docs/walkthrough.en.md:212` | …every object in `issues` carries… | …every object in `files[].issues` carries… | 同上 |
| 5 | `prompts/zh/P6.md:13` | 给不出就标 U 并写检索路径**知**。 | 给不出就标 U 并写检索路径。 | 笔误，多一个字 |
| 6 | `prompts/en/P2.md:23` | `"S\|secondary: as quoted in …"` | `"S｜secondary: as quoted in …"` | 规范要求全角 `｜`（U+FF5C），此处用了半角 `\|`；中文版 P2 本来就是全角 |
| 7 | `spec/evidence-tags.md:53` | （无此段，代码块后直接进 §1.3） | 新增一段：来源类型词由等级决定，中文用四个标签，英文可用 `primary/secondary/unverified/popular`，解析器两套都接受但要求与等级匹配 | 英文版第 53 行早有这段，中文版缺；解析器实际行为（`tests` 里有英文标签用例）与之相符 |
| 8 | `spec/evidence-tags.en.md:200` | …declared in the text as "not part of the argument"… | …declared with the literal marker "不承担推理"（解析器按此字符串匹配，另豁免以「旁栏」开头的段落）… | `checks.py:114` 只认 `不承担推理` 与段首 `旁栏`；照英文版原文写英文句子会被判 `MISSING_TAG` |
| 9 | `README.md:72` | 三个 fixture 与**两段**样例 | 三个 fixture 与**三段**样例 | `prompts/examples/` 实为 3 个文件 |
| 10 | `README.en.md:72` | …and the **two** example files | …and the **three** example files | 同上 |
| 11 | `docs/quickstart-check.md:44` | `15 条 error，exit=1` | `13 条 error / 1 warn，exit=1` | 当前与上一个提交（`6ee89fb^`）实跑均为 13/1；15 从未复现过 |
| 12 | `prompts/en/P4.md:1` | `…a problem of its own time?` | `…a problem of its own time, or of a later one?` | 中文标题是「解决的是当年问题，还是后来问题」，英文标题丢了后半；正文第 4 点本来就写了两问 |
| 13 | `tools/pyproject.toml:14-17` | classifiers 只有 `3.11` | 增加 `3.12`、`3.13` | CI 矩阵就在测 3.12/3.13，声明与实测对齐；重装后元数据已含三行 |

（第 1、2 条与第 3、4 条各算一处，合计 13 处编辑、11 个文件。）

### 3.4 当时仍存在的 7 项不一致（当日已全部有结论；第 2–7 项见 §3.6，第 1 项见下）

按影响从大到小：

1. **「来源不明」该标 F 还是 U**：`docs/method.md:26` 与 `docs/method.en.md:26` 的三步判断法写「不知道谁写的 → **F 的候选**」；规范 R8(c) 明确「来源不明的转述」属 `U`，R7 的 `F` 是「流行说法」（教科书写法），两者前提不同。这是语义冲突，不是翻译问题，当时按约定未改。**2026-11-16 裁决为 `U`**：能指出那份流行文本属于哪一类才归 `F`，连"可能是哪一类"都指不出就是 `U`；method 文档与 R8(c) 已按此对齐（见错题池 SP-01）。
2. **清单的 T 编号与规范 §6 对不上**：`RELEASE-CHECKLIST.md:20` 的「T-2 译本等级」在规范里不存在（译本归 R2）；规范的 T-2 是「作者晚年回忆」，清单却写成 T-4（`:22`），并把它描述为「与正文『作者自序不算原始』冲突」——真正的冲突是 T-2 暂定标 A、而第一期正文按 S 处理。T-5/T-6/T-7 随之整体错位一位。建议按规范 §6 重写这一节的编号与描述。
3. **英文术语三处不统一**：`spec/evidence-tags.en.md` 用 `Secondary scholarship` / `Popular account`；`prompts/README.md:27,29` 与 `prompts/en/P2.md:17,19` 用 `secondary work` / `popular claim`；而标签字面是 `secondary` / `popular`。三种叫法指同一件事，读者不会误解，但对外发布时属于「同一概念两种译名」。建议二选一（我倾向向标签字面靠：`secondary` / `popular`）。
4. **`F` 的定性偏强**：`prompts/README.md:29` 写「F 流行说法 popular claim（**待纠正的误说** / a claim to be corrected）」。规范 R7 只说 `F` **只能作线索**，必须补 A 或 S，并没有「待纠正」这层预设；而 R7 正例里的教材边栏确实是要纠正的误说，所以这处不算硬冲突，但会引导使用者把 `F` 当成「错的东西」。两版提示词一致，属「跨文档」而非「跨语言」问题。
5. **R2 的中英不等价**：`spec/evidence-tags.md:103` 讲的是「**古籍点校本**的点校属编纂工作」；`spec/evidence-tags.en.md:103` 译成「A **modern critical edition**'s editorial work」。点校本（如中华书局点校本）与西方 modern critical edition 大体对应，但英文读者会把它理解成「19–20 世纪西方校勘版」，中文读者则想到「古籍整理本」。含义接近，范畴不同，未改。
6. **证据库文档自相矛盾**：`docs/evidence-corpus-design.md:4` 与 `.en.md:4` 说「v0.1 工具不认识 `corpus/` 引用」，但同文件 `:114`（en 同）又写「`mathlint` 只解析第一个 `corpus/` 前缀」。后者描述的是 v0.2 的目标行为，应改成「将只解析」或「草案中只解析」。
7. **英文版 §1.2 的标签示例全是中文标签**：现在两版都声明「英文文档可用英文来源类型词」，但没有一个 `〔A｜primary:…〕` 的示范。建议补一行示例（纯文档，不涉语义）。

另有两条轻微非对称，仅供知悉、不建议动：

- `docs/walkthrough.en.md:131` 有一句中文版没有的说明（「报告行是中文，`--json` 给英文键」）——对英文读者有用，属翻译性补充。
- `docs/walkthrough.en.md` 的 chcp/乱码一行比中文版多解释了「行内代码里的标签会被跳过」，属信息更全的一侧。

### 3.5 顺带发现（不属于三项，但影响发布体验）

- `reports/baseline.json` 与 `reports/patched.json` 带 **UTF-8 BOM**（PowerShell 重定向写出），`json.load` 直接读会抛 `Unexpected UTF-8 BOM`，需 `utf-8-sig`。**已处理**（见 §3.6 第 7 项）。CLI 自身输出（管道/`--json`）是干净的 UTF-8，无 BOM。`docs/walkthrough.md:295` 与 `.en.md:295` 在各系统提醒用户用 `--json` 重定向到文件，Windows 上应注明用 `Out-File -Encoding utf8`。
- `docs/quickstart-check.md` 是 2026-11-13 的实测流水账，其中的耗时与路径属历史记录，本次只改了与事实冲突的数字（第 11 条），未重写。

### 3.6 遗留项处理结果（2026-11-16 追加）

| # | 遗留项 | 处理 | 文件 |
|---|---|---|---|
| 1 | 清单 §1 的 T 编号与规范 §6 错位 | 按规范 §6 重写为 T-1…T-7（学生笔记、晚年回忆、影印本、重印本、转引链、佚名批注、四分法本身）；删掉规范里不存在的「T-2 译本等级」，改在节末注明译本归 R2 | `RELEASE-CHECKLIST.md:19-31` |
| 2 | T-4 描述失准 | 归位为 T-2「作者晚年回忆」，冲突改准：不是「与作者自序不算原始冲突」，而是规范暂定标 `A`、第一期正文按 `S` 处理，两者相反 | 同上 |
| 3 | 英文术语不统一 | 三处统一到标签字面：`Secondary scholarship` → `Secondary`、`Popular account` → `Popular`、`secondary work` → `secondary`、`popular claim` → `popular` | `spec/evidence-tags.en.md:38,40`、`prompts/README.md:27,29`、`prompts/en/P2.md:17,19` |
| 4 | `F` 定性偏强 | `prompts/README.md:29` 去掉「待纠正的误说 / a claim to be corrected」，改为 R7 的「只能作线索，不能单独支撑论断；要支撑须同时给出它指向的 A 或 S / lead only…」 | `prompts/README.md:29` |
| 5 | R2「古籍点校本」译成 `modern critical edition` | 改为 `In a punctuated and collated edition of a classical text (点校本)…`，与中文范畴对齐，不再让英文读者误以为是 19–20 世纪西方校勘版 | `spec/evidence-tags.en.md:103` |
| 6 | 证据库文档 §3 与开头声明矛盾 | 改为「v0.2 的计划是只解析第一个 `corpus/` 前缀（v0.1 不解析任何 `corpus/` 引用）」 | `docs/evidence-corpus-design.md:114`、`.en.md:114` |
| 7 | `reports/*.json` 带 UTF-8 BOM | 去 BOM（内容逐字节保留），`json.load` 直接可读；实读 summary 仍为 baseline 96/242、patched 0/227 | `reports/baseline.json`、`reports/patched.json` |

§3.4 第 1 项（「来源不明」标 `F` 还是 `U`）于 2026-11-16 裁决为 `U`：`docs/method*.md:26` 与 `spec/evidence-tags*.md` R8(c) 已对齐，`F` 只留给能指认具体流行文本的情形。裁决本身是语义判断，工具仍不能自动断言，故继续留在错题池的 `SEMANTIC_ONLY`（SP-01，已标注裁决结果）。

### 3.7 错题池（2026-11-16 追加）

已建 `tools/tests/regression_pool.py`（17 条用例 + 5 条语义登记）、`tools/tests/test_regression_pool.py`（随 `unittest discover` 跑，`selfcheck.py` 自动带上）、`docs/regression-pool.md` 与 `.en.md`（逐条说明规则、期望、类型）。

17 条覆盖你点名的 9 个种子，并顺带锁住 R2 正例被误报、旧式简写、R4 正例/反例。其中 8 条标为 `locked`：教材/讲座标 `S` 只报 warn（R7 文字说 error）、R2 正例被报 warn、同一引用键的启发式误报、嵌套错误行列号相对 locator、跨行标记报两条错且文案失真、半角竖线静默接受、只有年份不报。`locked` 只锁当前事实，不声称规范已满足。5 条语义项（method 文档的 F/U 冲突已于当日裁决为 `U`、年份是否足以定位、点校层次是否真属两层、`corpus/` 未实现、`F` 是否给出线索）明确不做假用例。

---

## 四、修了什么：总览

- 改动文件 11 个，编辑 13 处：`docs/walkthrough.md`、`docs/walkthrough.en.md`（各 2 处）、`docs/quickstart-check.md`、`prompts/zh/P6.md`、`prompts/en/P2.md`、`prompts/en/P4.md`、`spec/evidence-tags.md`、`spec/evidence-tags.en.md`、`README.md`、`README.en.md`、`tools/pyproject.toml`。
- 没有触碰：`tools/mathlint/`（任何文件）、`spec` 的 R1–R13 判定文字、`tools/scripts/selfcheck.py` 的期望值、`.github/workflows/ci.yml`。
- 改后复核：3.11/3.12/3.13 `selfcheck.py` 全 PASS；68 条单测全过（含错题池 17 条）；`pip install -e tools` 在 3.12 venv 中安装成功，元数据含三个 Python classifier；`docs/walkthrough` 的记录输出与实跑仍逐字一致。当日稍后审计脚本入库并新增 `tools/tests/test_audit.py` 9 条，单测总数为 77，仍全绿。

## 五、还剩什么需要人决定

| 事项 | 位置 | 建议 |
|---|---|---|
| 是否给 CI 加 lint 阶段 | `.github/workflows/ci.yml` | 加 ruff（默认规则）即可；否则在 README 说明「本项目不做静态检查」 |
| CI 是否加「安装 + 入口」步骤 | 同上 | 建议加，这是唯一未覆盖的发布物形态 |
| 仓库/目录是否改名（可选） | `<repo>` | **定稿：暂不改**。包名已是唯一对外身份；等将来托管远程时一次性处理，见 §六 |
| 长描述缺失 | `tools/pyproject.toml` + 新建 `tools/README.md` | 上 PyPI 前必须补，否则项目页空白 |
| `license` 字段现代化（PEP 639） | `tools/pyproject.toml` | 改为 `license = "Apache-2.0"` + `license-files`，低优先级 |
| 「来源不明」标 F 还是 U | `docs/method.md:26` / `.en.md:26` | **已裁决：标 `U`**（2026-11-16）。规范 R8(c) 与 method 文档已对齐，错题池 SP-01 标注为已裁决 |
| 清单 §1 的 T 编号整体错位 | `RELEASE-CHECKLIST.md:19-31` | 已按规范 §6 重写，T-2 的冲突描述已改准（§3.6 第 1、2 项） |
| 英文术语统一（secondary work/scholarship、popular claim/account） | spec en + `prompts/README.md` + `prompts/en/P2.md` | 已统一到 `secondary` / `popular`（§3.6 第 3 项） |
| F 的「待纠正的误说」定性 | `prompts/README.md:29` | 已改为「只能作线索」（§3.6 第 4 项） |
| R2 中英范畴不等价 | `spec/evidence-tags.en.md:103` | 已与「古籍点校本」对齐（§3.6 第 5 项） |
| 证据库文档 v0.1/v0.2 时态矛盾 | `docs/evidence-corpus-design*.md:4/114` | 已改为「v0.2 将只解析」（§3.6 第 6 项） |
| `reports/*.json` 的 UTF-8 BOM | `reports/baseline.json`、`patched.json` | 已去 BOM，`json.load` 可直读（§3.6 第 7 项） |
| `--json` 重定向的 Windows 编码提示 | `docs/walkthrough.md:295` / `.en.md:295` | 补一句 `Out-File -Encoding utf8` |
| 英文/母语校对、`--online` 实网记录、阈值第二语料 | `RELEASE-CHECKLIST.md` §2–§4 | 本次未覆盖，仍按清单执行 |

---

## 六、命名收口（2026-11-16 追加）

### 6.1 决定

包名定为 **`mathlint`**，理由是短、特殊、好搜。distribution 名、`import` 名、控制台命令三者从此一致。曾经的候选 `mathhist`、`mathhist-toolkit` 不再使用。

### 6.2 已统一的地方

| 文件:行 | 原文 | 改后 |
|---|---|---|
| `README.md:1` | `# mathhist-toolkit` | `# mathlint` |
| `README.md:3`（新增） | — | 一行说明：项目与包名统一为 `mathlint`，仓库目录名暂仍为 `mathhist-toolkit` |
| `README.md:136` | `mathhist-toolkit v0.1, 证据标记规范…` | `mathlint v0.1, 证据标记规范…`（引用示例） |
| `README.en.md:1` | `# mathhist-toolkit` | `# mathlint` |
| `README.en.md:3`（新增） | — | 同义英文说明 |
| `README.en.md:136` | `mathhist-toolkit v0.1, evidence-tagging…` | `mathlint v0.1, evidence-tagging…` |
| `tools/pyproject.toml:11` | `authors = [{ name = "mathhist-toolkit contributors" }]` | `authors = [{ name = "mathlint contributors" }]` |
| `tools/mathlint/online.py:21` | UA 串里的 `+https://example.invalid/mathhist-toolkit` | `+https://example.invalid/mathlint`（仅 User-Agent 元数据，不参与判定；无单测断言此串） |
| `RELEASE-CHECKLIST.md:56-58` | 三条待办 | 改为已办：PyPI 实测 404、包名定为 `mathlint`、元数据已核对 |

`distribution name` 本来就是 `mathlint`，`[project.scripts] mathlint = "mathlint.cli:main"` 与 `import mathlint` 均未变，所以这次收口不影响任何调用方式，三个 Python 版本的 `selfcheck` 仍然全 PASS。

### 6.3 故意保留、未改的 `mathhist-toolkit`

这些是**目录名/历史记录**，不是项目身份，改了会让命令或记录变成假的：

- 路径类，共 28 处：`README.md:22/29`、`README.en.md:22/29`、`docs/walkthrough.md` 10 处（12、85、115、120、125、153、174、227、268、294）、`docs/walkthrough.en.md` 10 处（12、83、113、118、123、153、174、227、268、294）、`docs/threshold-sensitivity.md:50/70` 与 `.en.md:50/70`。
- 历史流水账：`docs/quickstart-check.md:8`（2026-11-13 临时目录，属实测记录）。
- 本报告 §一/§六本身对仓库名的引用。

### 6.4 仓库目录改名的代价（定稿：暂不改）

现状：本地裸仓库，`git remote -v` 为空，`.git/config` 里 `user.name = mathhist-toolkit`，`v0.1.0` tag 指向提交 `6ee89fb`。

若把 `<repo>` 改名为 `mathlint`：

1. **必改字符串约 30 处 / 8 个文件**：上文 28 处路径 + `docs/quickstart-check.md:8` 的历史路径 + 另一处内部记录。纯文本替换即可，风险低。
2. **walkthrough 必须重跑**：它的「记录输出与实跑逐字一致」是卖点，输出里嵌了绝对路径（`<repo>\...`），改名后 4 个代码块全部失效，需要重跑并核对 18/8/21 行加 345 行节选。
3. **不涉及的项**：无远程仓库，所以没有 clone URL、README 徽章、issue/PR 永久链接、其他机器的工作副本要同步；CI 全部用相对路径与 `working-directory`，不受影响；tag/提交历史与目录名无关。
4. **会被打断的项**：正在用该目录的终端/编辑器会话、其他会话里写死的路径（目前查到 1 处记忆文件）、任何按绝对路径打开的快捷方式或书签。
5. **可选连带项**：`.git/config` 的 `user.name` 是否一并改为 `mathlint`（只影响未来提交的作者名，历史不追溯）。

估算：字符串替换 15 分钟内完成，walkthrough 重跑与复核约 10 分钟；总工作量小，但收益仅是「目录名与包名一致」。

**定稿：暂不改。** 仓库目录名保持 `mathhist-toolkit`。理由：包名 `mathlint` 已是唯一对外身份，目录名只是本地路径；改名要重跑 walkthrough 的 4 个代码块、并同步 1 处记忆文件里写死的路径。等将来把仓库托管到远程时一次性处理（那时本来就要设远程 URL、可能还要建新目录），不在发布前做两次。
