# 参与贡献 / Contributing

这个仓库有两类东西：**规范**（判断依据）与**工具**（把判断依据变成可执行的检查）。两者都欢迎修改，但要求不同。
There are two kinds of material here: the **spec** (what counts as evidence) and the **tool** (checks that make the spec executable). Both are welcome, with different requirements.

## 快速开始 / Quick start

1. `mathlint` 不需要安装依赖，Python 3.11+ 即可；`graphlint` 需要 PyYAML ≥ 6.0：

```bash
cd tools
py -3 -m pip install "PyYAML>=6.0"
```

2. 改完跑一遍本地闸门：

```bash
cd tools
py -3 scripts/selfcheck.py
py -3 -m unittest discover -s tests
py -3 -m graphlint check-all
py -3 -m graphlint generate --check
```

3. 全部 PASS 再提交。`selfcheck.py` 只覆盖 `mathlint`；`graphlint` 靠后三条命令。

## 提交一条新规则 / Adding a spec rule

规范里的每条规则，必须同时给出三样东西，缺一不可：

1. **正例**：一条符合该规则的标记写法，能通过 `mathlint`。
2. **反例**：一条违反该规则的写法，并写明 `mathlint` 实际报出的错误代码。
3. **工具可判定性**：明确写"这条规则能否被工具检查"。
   - 能：说明由哪个检查项覆盖（如 `GRADE_SECONDHAND_A`）。
   - 不能：说明为什么不能，归入规范的 §5"机器不能验"表。
   - 部分能：写清能验到哪一步、剩下哪一步必须人工裁决。

**只写"应该这样"而没有正例与反例的规则不予合入。** 理由是：没有反例的规则无法被检验，最终会退化成口号。

如果你对某条规则的判定没有把握，请按现有 T-1~T-7 的格式新增一条"待议条款"，写清：你不确定的是什么、两种可能的读法、你倾向哪一种及理由。**不要把不确定写成定论。**

## 新增一个检查项 / Adding a check

除了上面三样，还必须有：

1. **fixture**：在 `tools/tests/fixtures/` 里给出能触发该检查的最小文档。优先复用现有三个 fixture；确实需要新场景时再加文件。
2. **单元测试**：在 `tools/tests/test_checks.py`（语义类）或 `test_parser.py`（语法类）里加用例，断言错误代码与级别。
3. **级别论证**：说明为什么是 error 而不是 warn（或反之）。判据是："这条错误会让读者无法核查吗？" 会 → error；只是可疑 → warn。
4. **对既有编号的影响**：新增检查会改变 fixture 的期望条数。请同步更新 `tools/scripts/selfcheck.py` 里的 `EXPECTED` 表，并在 PR 说明里写明"从 N 条变为 M 条"。

## 新增一类边 / Adding an edge type

边的契约只有一处真源：`spec/framework/edge-signatures.yaml`。`spec/framework/graph.schema.json` 与 `spec/object-model.md` 里的边表、约束表都是生成物，**不要手改**。

完整流程：

1. **改 YAML**。在 `edges:` 下新增一条，至少写清：
   - `type`、`gloss`、`direction`；
   - `from` / `to`（`from` 必须是具体节点类；`to` 可用 `*` 配合 `excluded_to`）；
   - `directed`、`same_class`、`symmetric`、`acyclic`、`weight_sum`；
   - 专属属性（`attributes`）与是否需要 `time`；
   - 条件必填（如 `require_note_when_to`）、反向别名（`reverse_alias`）与 `forbid`。
2. **跑生成**：

```bash
cd tools
py -3 -m graphlint generate
```

这会把边枚举与条件约束写进 `graph.schema.json`，并重写 `object-model.md` 中带 `GENERATED` 标记的两张表。提交时必须把生成物一起带上。

3. **跑校验**：

```bash
py -3 -m graphlint generate --check   # 生成物是否最新
py -3 -m graphlint check-all         # 是否有新增错误（当前基线：30 error / 60 warning）
```

4. **补测试**（与新增检查项同样的标准）：
   - 在 `tools/tests/test_graphlint.py` 加签名判定的正例与反例：至少一条合法端点组合、一条非法组合；
   - 若新边引入新的失败方式，在 `tools/tests/fixtures/` 放一个最小失败图包（`graph_*.json`），并在 `FailureFixtureTests` 里断言错误码；
   - 若新边有等级上限或条件必填，补一条断言 `actual` / `expected` 的用例。
5. **同步计数与文档**：`README.md`、`README.en.md`、`docs/repository-guide.md` / `.en.md` 中的边类型数量、`check-all` 计数若变化，一并更新；`CHANGELOG.md` 记一条。
6. **最后再跑一遍** `py -3 -m unittest discover -s tests` 与 `py -3 scripts/selfcheck.py`。

判据：新边必须能回答“它比现有 31 类边多表达了什么关系”。只是换个说法的边不加；先开 issue 说明缺口与两个真实图包中的用例。

## 新增或修改边级规则 / Adding or changing edge-level rules

`source` / `claimant` 二选一、`attestation` 等级上限、`grade=U` 必填 `note` 这类边级规则，schema 侧只有一处真源：`spec/framework/edge-signatures.yaml` 的 `invariants.conditional_required.rules`。

1. **改 YAML**：在对应规则下维护 `when` / `require` / `message`，并补 `schema:` 块。`schema` 是 JSON Schema 片段，会被原样放进 `graph.schema.json` 的 `allOf`。
2. **登记顺序**：新增规则时，把它的 `id` 加进顶层 `edge_schema_rules:`。列表顺序就是 `allOf` 前段的顺序；重复引用、引用不存在的 id、或规则缺少 `schema`，`generate` 都会直接报错。
3. **跑生成与校验**：

```bash
cd tools
py -3 -m graphlint generate
py -3 -m graphlint generate --check
py -3 -m graphlint check-all
```

4. **补测试**：在 `tools/tests/test_graphlint.py` 断言新规则的合法/非法样例；若引入新的失败方式，按下一节加 fixture。
5. **不要改 `generate.py` 来加规则**：它只按 `edge_schema_rules` 搬运 `schema` 块，不再包含任何 attestation/grade 常量。

运行时的错误文案与 `detail` 仍在 `checks.py`；改文案不需要动 YAML。改判定条件时，以 YAML 的 `schema` 为准，并确认 `checks.py` 的对应运行时分支与它一致。

## 改契约：先改文档还是先改表 / Doc first or table first?

先问一句：**这条改动能不能被机器判定？**

| 改动 | 先改哪里 | 理由 |
|---|---|---|
| 边的端点、方向、必填属性、枚举、等级上限、条件必填、不变量级别 | **先改 `edge-signatures.yaml`**，再 `generate` | 这些是机读契约；文档表格是生成物，先改文档会被下次 `generate --check` 覆盖 |
| 新增边类型的释义、适用场景、与既有边的区别 | **先写规范说明**（`object-model.md` 正文或 issue / PR 描述），再改 YAML | `gloss` 只能是一句话；判断依据、反例与取舍必须写在人能读的地方 |
| 纯解释性文字（为什么这样建模、历史背景、举例） | **直接改文档** | 不影响校验器，也不进入生成块 |
| 新增节点类或其必填字段 | 先改 `object-model.schema.json` 与 `object-model.md`，再补 `graphlint` 检查与测试 | 节点结构是手写 schema，不由边表生成 |
| 只改错误消息、提示文案 | 直接改 `checks.py`，补/改单测 | 不改变契约，但要让测试断言新文案 |

两条硬规则：

- **生成块里的内容永远不手改。** 手改后 `py -3 -m graphlint generate --check` 必须报不一致；这是故意的。
- **改表必须带测试。** 只改 YAML 不改测试，等于把契约交给下一个人猜。

如果你不确定某条规则该放 YAML 还是文档，按这个顺序判断：能被 `graphlint` 判定的 → YAML；需要人读理由的 → 文档；两者都需要 → 两边都写，但 YAML 是唯一可执行版本。

## 修改阈值或启发式 / Changing a threshold

`MISSING_TAG` 这类启发式不能凭感觉改。改之前请：

1. 用 `docs/threshold-sensitivity.md` 里的脚本在至少两份语料上跑出新旧对比；
2. 把对比表附在 PR 里；
3. 说明改动会让多少段落多报或少报。

## 文档 / Docs

- 中英双语文档内容必须等价，不是摘要式翻译。改了中文请同步英文，反之亦然。
- 不声称学术贡献，不用"首创""首次提出"这类措辞。写"我用的是这个办法"，不写"这个办法是我发明的"。
- 引文示例一律放在代码块或行内代码里，避免被自己的工具误判。

## 许可 / Licensing

提交即表示你同意：代码与工具脚本按 [Apache-2.0](LICENSE) 授权，文档与规范按 [CC BY 4.0](LICENSE-docs) 授权。
By submitting, you agree that code is licensed under Apache-2.0 and documentation under CC BY 4.0.

## 不接受的贡献 / What will be rejected

- 没有 fixture 的新检查项。
- 把"不确定"写成定论的规则。
- 声称工具能判断"是否原始文献"或"作者原意"的改动——它不能，也不应该假装能。
- 引入第三方运行时依赖的改动（标准库够用；确有必要的，先开 issue 讨论）。
