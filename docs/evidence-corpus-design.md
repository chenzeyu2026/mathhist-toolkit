# 证据库（evidence corpus）设计草案

> **状态：v0.2 提案，未实现。** 本文件只写设计，不包含代码，也不承诺时间表。
> 现行 v0.1 的工具不认识 `corpus/` 引用；草案里的检查项均为待实现。
> Status: v0.2 proposal, not implemented. Design only — no code, no schedule. The v0.1 linter does not understand `corpus/` locators yet.

## 0. 问题与改法

原始提法是"构建统一论文集，把散在各库的一手文献集中起来"。方向对，做法要改。

论文集解决不了三件事：

1. **版权**：20 世纪的校勘版、译本、档案影像大多不能整本公开。
2. **指向性**：读者拿着整本《Acta Eruditorum》仍不知道你这句话对应哪一段。
3. **可复现性**：扫描件换了来源、裁了边、换了 OCR，页码就对不上，别人没法判断你读的是不是同一页。

所以改成**证据库**：不集中全文，集中**索引与校验信息**。每份文献一个条目，条目里记清楚"我读的是哪一件、从哪来、多大、什么哈希、第 12 页在哪张扫描图上、能不能公开"。全文留在本地。

一句话：**证据库把"我记得在哪看过"变成"这一页的字节指纹是这个，你自己去核"。**

## 1. 目录结构

```
corpus/
  leibniz-1684-nova-methodus/
    source/                     # 本地副本，默认不进公开仓库
      scan-01.png
      scan-02.png
      ocr.txt                   # 可选，注明 OCR 引擎与日期
    manifest.yaml
    notes.md                    # 我为什么读它、读时的问题
  newton-1687-principia-1st/
    ...
```

- `source/`：原始扫描件或**合法镜像**的本地副本。文件名不带语义，页码关系写在 manifest 里。
- `manifest.yaml`：唯一的机器可读入口，字段见 §2。
- `notes.md`：人读的笔记。允许写"第 3 页有水渍，第 2 段缺字"这类物质性观察——这类信息在别处没地方放。

仓库根放 `corpus/README.md` 说明规则，放 `corpus/index.yaml` 列出全部 id 与一句话摘要（可选，便于人浏览）。

## 2. manifest.yaml 字段

```yaml
id: leibniz-1684-nova-methodus
title: "Nova methodus pro maximis et minimis"
creator: "Gottfried Wilhelm Leibniz"
date: "1684-10"                 # 尽量到月；只有年就到年
kind: periodical-article        # periodical-article | book | manuscript |
                                # correspondence | lecture-notes | archive-item
language: la

provenance:
  is_contemporary_publication: true    # 是否同时代出版物（本人经手刊行）
  is_scholarly_edition: false          # 是否为后人编订本（全集、校勘版）
  editor: null                         # 编订者；is_scholarly_edition=true 时必填
  edition_statement: "Acta Eruditorum, Oct. 1684, pp. 467-473"
  translation: null                    # 若为译本：译者、语种、版次
  witness_note: "原刊；无编者导言"      # 这一件物质上是什么，一句话

source:
  url: "https://www.digitale-sammlungen.de/..."   # 获取入口，可多个，首个为主
  retrieved: "2026-11-02"
  sha256: "3f9c...e1"                # 对 source/ 下全部文件按序计算的清单哈希
  bytes: 18432011
  page_count: 7                      # 扫描页数
  page_map:                          # 扫描页 → 印刷页码
    - {scan: 1, printed: "467"}
    - {scan: 2, printed: "468"}
    # 无页码的件（手稿、信札）用 folio 或 "n.p."，并在 notes.md 说明定位方式
  page_map_gaps: "p. 471 右半版缺失"   # 可选，如实记录缺页

license:
  status: public-domain              # public-domain | cc-by | cc-by-sa |
                                     # permission-granted | unknown | local-only
  basis: "1684 年刊行，作者逝世逾 70 年"
  public_copy_allowed: true          # 是否允许把 source/ 放进公开仓库
  note: ""

rights_note: "数字化影像由巴伐利亚州立图书馆提供，其使用条款另计"   # 可选但建议
```

字段规则：

- `id` 全小写、连字符分隔、`作者姓-年份-短题` 形式；一经引用不再改。改名等于换 id，旧引用全部失效。
- `provenance` 四问必须回答：**是不是同时代出版物、是不是后人编订、编订者是谁、这一件物质上是什么**。这四项是防"把二手当一手"的机械抓手（§7）。
- `sha256` 算的是 `source/` 下所有文件的**清单哈希**（按文件名排序，逐个文件哈希再拼起来算一次），不是单文件哈希；换扫描件必然变。
- `page_map` 是证据库存在的核心理由：没有它，`#p12` 无从解析。

## 3. 引用格式

```
〔A｜原始文献:corpus/leibniz-1684-nova-methodus#p467〕
〔S｜二手研究:corpus/grabiner-1981#p45〕
〔A｜原始文献:corpus/newton-1687-principia-1st#p12-14〕
```

- `#p<n>` 指**印刷页码**，不是扫描页序号。理由：读者手里可能是另一个影印本，印刷页码是唯一跨副本稳定的坐标。
- 无印刷页码的件用 `#s<n>`（扫描页）、`#f<n>`（folia）、`#n<n>`（段号），三选一，manifest 的 `page_map` 里说明用哪种。
- 区间写 `#p12-14`；单页插图写 `#f3r`。

### 与外部 URL / DOI 如何共存

三种写法都合法，语义不同：

| 写法 | 断言的是 | 读者要做什么 |
|---|---|---|
| `corpus/<id>#p12` | 我读过这一页，字节指纹可核 | 向作者索取副本，或去 manifest 的 `source.url` 取 |
| `doi:10.xxxx/...` | 有一个稳定的公共入口 | 点开 DOI |
| `https://...` | 有一个入口，但可能失效 | 点开链接 |

**优先级**：`corpus/` 优先于外部 locator，因为它是唯一能校验"我读的和你是同一页"的形式。但 corpus 不改变等级——**进了证据库不等于升成 A**。等级由 §4 的判定规则决定，证据库只保证可解析。

两者可以并写。v0.2 的计划是只解析第一个 `corpus/` 前缀（v0.1 不解析任何 `corpus/` 引用，见开头状态说明）：

```
〔A｜原始文献:corpus/leibniz-1684-nova-methodus#p467（doi:10.xxxx/xxxx）〕
```

私有副本 + 公共入口并写，是最耐久的写法：公共入口失效时，corpus id 仍指向可核对的哈希。

## 4. `mathlint` 需要新增的检查

| 代码 | 级别 | 判定 |
|---|---|---|
| `CORPUS_UNKNOWN_ID` | error | locator 含 `corpus/<id>`，但 `corpus/<id>/manifest.yaml` 不存在 |
| `CORPUS_PAGE_OUT_OF_RANGE` | error | `#p467` 在 `page_map.printed` 里找不到，且不在声明的缺页范围内 |
| `CORPUS_HASH_MISMATCH` | error | `source/` 存在且清单哈希 ≠ manifest 的 `sha256` |
| `CORPUS_MISSING_FILE` | error | manifest 声明 `page_count: 7`，`source/` 里只有 5 个文件 |
| `CORPUS_LICENSE_LEAK` | error | manifest `public_copy_allowed: false`，但该文档被判定为公开 |
| `CORPUS_MANIFEST_FIELD_MISSING` | warn | `provenance` 四问有空项，或 `page_map` 为空 |
| `CORPUS_PAGE_MAP_GAP` | warn | 引用落在 `page_map` 未覆盖的页 |
| `CORPUS_GRADE_DOUBT` | warn | 标 `A` 却指向 `is_contemporary_publication: false` 的条目 |
| `CORPUS_GRADE_DOUBT_STRONG` | error | 标 `A` 却指向 `is_scholarly_edition: true` 的条目，且 `witness_note` 未声明引用的是其中影印的原始版本 |
| `CORPUS_UNUSED` | info | 条目存在但全仓库无引用 |

几点说明：

- **"是否公开"怎么判定**：新增仓库级配置 `.mathlint.yaml`，字段 `visibility: public \| private`，默认 `private`；也可在单文件 front-matter 里覆盖。这是启发式，不是安全边界——真正防止泄密靠提交前人工检查，工具只挡低级失误。
- **哈希检查只在本地 `source/` 存在时做**。公开仓库里没有 `source/`，此时跳过并给 `info`，不报错。
- `--offline` 下以上检查全部可做（除清单哈希需要读本地文件外，其余纯 YAML 解析）。`--online` 时额外用 `source.url` 探活，复用现有 `LINK_DEAD` / `NETWORK_UNREACHABLE` 区分。
- 这些检查**不**判断等级对不对。`CORPUS_GRADE_DOUBT` 只提示"你说它是同时代的，但 manifest 说不是"，最终裁决仍在人。

## 5. 边界：证据库解决什么，不解决什么

**能解决**：

- 引文可解析：`#p467` 有确定所指，不依赖"某处"。
- 可复现：哈希相同即同一份影像；换来源会立刻暴露。
- 可交接：别人接手你的稿子，能照 manifest 把同一页找出来。
- 可审计：哪一条引用指向了后人编订本，机器能列出来。

**不能解决**：

- **不能判断"这是不是原始文献"**。能不能算 A，取决于它是同时代出版物、手稿、通信还是后来的校勘本——这是史学判断，manifest 只能记录你的声明，不能替你声明。
- **不能判断"作者原意是否如此"**。现场语境、反讽、术语的时代义，任何索引都无能为力。
- **不能证明你读过**。哈希证明文件没变，不证明你理解了它。
- **不能替代版本学**。同一著作的不同版次差异，manifest 只能记录"我读的是哪一版"。

界面上要写死这句话，与规范 §5 一致：

> 工具验证引文可解析性与等级自洽，不验证历史意图与等级判定本身。

## 6. 版权边界

**公开仓库只放**：`manifest.yaml`、`notes.md`、`corpus/README.md`、引用规则。**不放 `source/` 的任何字节。**

以下情形不得把全文放进公开仓库，即使技术上能放：

1. **仍在版权期内的编订本、译本、校勘版**。正文可能已过版权期，但编者的导言、校注、标点、译文另有版权。
2. **档案机构声明权利的影像**。许多手稿的数字影像使用条款独立于作品版权，需逐件看。
3. **许可状态为 `unknown` 的件**。默认不放，直到查清。
4. **他人提供的副本**。别人私下给的扫描件，你没有再分发权。
5. **含个人信息的近代通信、未刊笔记**，涉及在世人或近亲。

**待议（T-8）**：对公有领域二维作品的"忠实复制"照片，美国（*Bridgeman v. Corel*）倾向于无新的独创性，部分欧洲司法辖区与数据库权利另有主张，中国法下亦有争议。本草案的保守做法是：**只要数字化的提供方声明了使用条款，就按 `local-only` 处理**，不赌法律解释。这条我保留意见，理由如上。

`source/` 永不提交，靠 `.gitignore` + 提交前检查双保险；`.gitignore` 里加 `corpus/*/source/`。若确实要公开某件（如自己扫描的 1684 年原刊），在 manifest 里单独写 `public_copy_allowed: true` 并给出依据，且该条目单独放入 `corpus-public/` 目录，与私有库物理分开，避免一次 `git add -A` 全泄。

## 7. 风险：汇编会沦为准二手材料

这是本设计最大的风险，必须写清楚。

**机制**：一旦有了"证据库"这个整齐的东西，写作者会自然而然地引用它，而不是引用它指向的原件。三轮之后，`corpus/xxx` 就成了新的"大家都这么引"的二手来源——它看起来比维基可靠，因为它有哈希，但**哈希只证明文件没变，不证明文件是原件**。

**四条防线**：

1. **manifest 必须自陈身份**。`is_contemporary_publication`、`is_scholarly_edition`、`editor`、`witness_note` 四项强制填写。填 `is_scholarly_edition: true` 的条目，`A` 级引用直接报 error（`CORPUS_GRADE_DOUBT_STRONG`）。
2. **引用必须落到页，不能落到条目**。只写 `corpus/<id>` 不写 `#p…` 的，报 `CORPUS_PAGE_OUT_OF_RANGE` 的同族错误 `CORPUS_NO_PAGE`（另立，暂未定级）。理由：落到条目就是"我引了这本书"，落到页才是"我引了这句话"。
3. **禁止"库内互引"**。`notes.md` 可以引用别的条目，但那不算证据；正文的标签只能指向 manifest，不能指向另一个条目的 `notes.md`。这条目前靠人工，工具只能检查 locator 是否含 `notes.md`。
4. **定期"去皮"**：写完后把 corpus id 临时替换成 manifest 里的 `edition_statement`，读一遍。如果替换后句子读不通，说明你依赖的是"库里有这件东西"，而不是这一页的内容。

另一种退化更隐蔽：**选集当全集**。把某本《数学史文选》里的一篇当作作者原文引用。防线只有一条：manifest 的 `witness_note` 必须写清"这是选集中的重印，原刊未见"，并且这种条目在 `A` 级引用时降级为 `S` 或加注。

## 8. 未决问题

- **T-9**：`id` 的稳定性。作者改名、年份修订、发现更早版本，是否允许同一 id 换 `source`？草案倾向于"允许换 source，但 `sha256` 变更需在 `notes.md` 记录日期"，因为换 id 会打断所有旧稿。
- **T-10**：多卷本页码。`#p12` 在《莱布尼茨全集》里无意义，需 `#v3-p12` 形式。草案暂定"多卷本一律写 `#v<卷>-p<页>`"，但会与单卷本格式不一致，是否统一尚未定。
- **T-11**：OCR 文本算不算"副本"。草案倾向于：`ocr.txt` 只作检索辅助，不作为引用依据；引用必须能回到扫描页。
- **T-12**：条目之间"同一著作不同版本"的关系如何表达（`same_work_as:`）。暂不设计，v0.2 若做先留空。

## 9. 若真要实现（v0.2 的最小路径）

1. 先做 manifest 的 JSON Schema 与一个 `mathlint corpus verify <dir>` 子命令，只查哈希与页码映射。
2. 再接 `corpus/` locator 解析，接入现有 `citations.py`。
3. 最后做 `CORPUS_GRADE_DOUBT` 这类跨文件判断。
4. 全程不写"下载"功能：抓取与合规由人负责，工具只校验已有副本。

第 4 条是硬约束。一旦工具开始自动下载，版权责任就从"使用者判断"滑向"工具默认"。
