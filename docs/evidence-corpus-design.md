# 证据库（evidence corpus）设计草案

> **状态：v0.3 提案，未实现。** v0.2 的私有索引设计保留；v0.3 在 §6 之上增加「公开层」，把可对外共享的部分单独划出。§6 对 `local-only` 的默认仍然有效。
> 现行 v0.1 的工具不认识 `corpus/` 引用；草案里的检查项均为待实现。
> Status: v0.3 proposal, not implemented. v0.2 private-index design retained; v0.3 adds a public tier on top of §6.

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

---

# v0.3　公开层：可共享、可引用、可长期积累

## 10. 三种对象，不是一个仓库

公开层不是把私有库整个推出去，而是按**权利状态**分三档。每档一个 `visibility` 值，写在 manifest 里。

| 档 | `visibility` | 公开什么 | 不公开什么 | 谁能拿到全文 |
|---|---|---|---|---|
| 元数据档 | `public-metadata` | 书目、版本、页码映射、哈希、许可声明、短引 | 扫描件、转录全文 | 按 `source.url` 或馆际互借自行获取 |
| 公有领域全文档 | `public-fulltext` | 扫描件或转录、`page_map`、校读记录 | 他人添加的导言、校注、译文（另有版权） | 任何人 |
| 授权链接档 | `link-only` | 书目、DOI/URL、许可状态 | 任何字节 | 通过出版社/图书馆 |

**硬规则：`public-fulltext` 必须同时满足**：

1. 作品本身已进入公有领域（§14 的判定）；
2. 数字化提供方没有另附使用条款，或条款允许再分发；
3. manifest 写明 `license.basis` 与判定日期；
4. 该条目放在 `corpus-public/`，与私有 `corpus/` **物理分开**。

四条缺一，退回 `public-metadata` 或 `link-only`。**默认不是公开**。

## 11. 收什么，不收什么

| 类型 | 收 | 公开档 | 说明 |
|---|---|---|---|
| 原始文献影印（公有领域） | 收 | `public-fulltext` | 需 `page_map` 与哈希；提供方条款另计 |
| 自建转录（公有领域底本） | 收 | `public-fulltext` | 注明转录者、日期、校对程度；转录本身以 CC BY 4.0 或 CC0 释出 |
| 书目与版本元数据 | 收 | `public-metadata` | 作者、书名、版次、DOI、馆藏号属事实，可公开 |
| 二手研究 | 只收书目与短引 | `public-metadata` | **不存全文**；需要全文走图书馆 |
| 代码与工具 | 收 | 随仓库 | Apache-2.0，见 `LICENSE` |
| 预印本 | 只收链接 | `link-only` | 除非作者明确授权再分发 |
| 在版书、校勘本、译本 | 只收书目 | `public-metadata` | 编者的导言、校注、标点、译文另有版权 |
| 无 LICENSE 的民间文本库 | 只收书目/链接 | `link-only` | 例：殆知阁无 LICENSE，不得转存全文 |
| 来源不明的 PDF | **不收** | — | 不进入公开仓库，也不进入 git 历史 |
| 档案影像（馆方声明权利） | 只收元数据 | `public-metadata` | 逐件看馆方条款，不赌 |

## 12. 标注：在 v0.2 manifest 上加字段

保留 v0.2 的全部字段（`provenance`、`source.sha256`、`page_map`、`license`），新增：

```yaml
visibility: public-metadata        # public-metadata | public-fulltext | link-only | private

source_type: scan                  # scan | transcription | ocr | hybrid
readability: L1                    # L1 原文可读 | L2 只有英译 | L3 只有再译 | L0 不可得

transcription:                     # 有转录时必填
  by: "chenzeyu"
  date: "2026-11-26"
  engine: "none"                   # none | tesseract-5 | 其他
  human_checked: true              # 是否逐页对过扫描
  accuracy_note: "第 3 页两字缺，已用方框标"

translation: null                  # 有译本时：译者、语种、版次、权利状态
social:                            # 社会史层可选字段，见规划 Part 5
  institution: ["BR-ORG-..."]
  journal: ["BR-JRN-..."]
  funding: []
  school: []

related:
  same_work_as: null               # 同著作的其他版本/印次
  reprint_of: null                 # 选集中重印时指向原刊条目
  supersedes: null                 # 替换旧条目时指向旧 id
```

规则：

- `visibility` 缺省为 `private`；公开是**主动声明**，不是默认。
- `readability` 与规划 Part 1.5 的 L1–L0 对齐；它描述"读者能否读原文"，不描述版本好坏。
- `supersedes` 只用于"同一件换了更好的影像"，**不删旧条目**；旧 id 永久保留，引用不失效。
- `transcription.human_checked: false` 的条目，正文引用仍须回扫描页；转录只作检索。

## 13. 可引用：三层标识

| 层 | 形式 | 断言 | 失效风险 |
|---|---|---|---|
| 条目定位 | `corpus/<id>#p467` | 我读的是这一页，哈希可核 | 仓库在则有效 |
| 版本快照 | `10.5281/zenodo.<版本号>` | 这一版字节固定 | 低 |
| 项目整体 | `10.5281/zenodo.<概念号>` | 始终指向最新版 | 低 |

做法：

1. **每个 Release 打 tag**（如 `corpus-v0.1.0`），Zenodo 自动归档并给版本 DOI；概念 DOI 指向最新版。操作见 `docs/zenodo-doi.md`。
2. **快照三件套**：git tag ＋ Zenodo deposit ＋ `manifest.sha256`；三者的日期写进 `index/snapshot.yaml`。
3. **时间戳**：MVP 用 Zenodo 的 deposit 时间＋git commit 时间；需要更强证明时，对 `index/items.jsonl` 的哈希加 RFC 3161 时间戳文件（可选，不进 MVP）。
4. **引用示例**：

```
〔A｜原始文献:corpus/leibniz-1684-nova-methodus#p467（doi:10.5281/zenodo.XXXXXXX）〕
〔S｜二手研究:corpus/grabiner-1981#p45〕
```

5. **DOI 断言的是字节，不是真理**。它证明"这一版没变"，不证明"这条史料是真的"；等级判定仍按 §4 与规划 Part 1.5。

## 14. 合规：先判权利，再谈共享

### 14.1 公有领域判定（三项都要过）

| 项 | 判据 | 注意 |
|---|---|---|
| 作品版权期 | 中国：作者逝世满 50 年；美国：2026 年时 1930 年前出版；欧盟：作者逝世满 70 年 | 逐件按最保守辖区判，别只看中国 |
| 数字化件 | 扫描/照片是否产生新权利 | 美国 *Bridgeman v. Corel* 倾向无；欧盟数据库权利、馆方条款另计 |
| 提供方条款 | 是否允许再分发 | 有条款就按 `local-only`，不赌 |

### 14.2 在版与无授权

- **在版书**：只存书目、短引、页码；全文走出版社或馆际互借。**不因为"只用于研究"就上传。**
- **无 LICENSE 的库**（殆知阁等）：只存元数据与链接；不转存全文，不打包进 Release。
- **《中华大典·数学典》《中国数学典籍集成》及一切现代点校本**：不进全文库，只作引用定位；见 §14.5（已决定，不再讨论）。
- **孤儿作品**：只存元数据；不公开全文。
- **他人给的扫描件**：默认 `local-only`，不进入公开仓库。

### 14.3 许可矩阵

| 内容 | 许可 |
|---|---|
| 代码（`tools/`） | Apache-2.0 |
| 规范、文档、索引 | CC BY 4.0 |
| 公有领域原文/影像 | Public Domain Mark（或 CC0，若由本项目释放） |
| 本项目自建转录 | CC BY 4.0（可选择 CC0） |
| 有授权的译文 | 按授权书写，manifest 记 `permission-granted` |
| 第三方短引 | 原权利人不因引用而被再许可 |

### 14.4 治理

- **贡献者声明**：提交即声明"我有权提交这些字节"，并在 `CONTRIBUTING.md` 写明；不采用口头授权。
- **下架流程**：收到权利主张 → 先把条目降为 `public-metadata` → 核验 → 恢复或永久移除；移除不删 id，标 `withdrawn` 并保留书目。
- **不做自动下载**：工具只校验已有副本；抓取与合规由人负责（沿用 §9 第 4 条）。

### 14.5 已决定：点校本不进全文库（DEC-1）

**这条是既定规则，不是待议项。** 适用对象包括《中华大典·数学典》《中国数学典籍集成》，以及任何现代点校、校勘、注释、今译、整理本。

1. **只收元数据**：书名、卷次、页码、版次、出版社、ISBN、短引；manifest 的 `visibility` 固定为 `public-metadata`。
2. **不做**：不扫描、不 OCR、不转录、不上传全文。
3. **不因底本过版权期而放行**：点校、标点、校注、导言、译文另有版权；底本属公有领域，不等于整理本可再分发。
4. **引用写法**：按规划 Part 1.5 记 `A（编订本）` 或 `S`，注明「据点校本，原文页码待核」；不得把点校本 PDF 当原文影像引用。
5. **《集成》的例外也不成立**：即使某册含影印原刊，也只引书目与页码；影印页的再分发权另判，不自动进入 `corpus-public/`。
6. **工具落点**：`visibility: public-metadata`；许可状态记 `unknown`（在版权期），或在 v0.3 schema 增 `in-copyright`；`CORPUS_LICENSE_LEAK` 负责挡「声明不可公开却被公开」的低级错误。

## 15. 组织与 MVP

### 15.1 目录

```
corpus/                     # 私有：manifest + notes，source/ 不进 git
corpus-public/              # 公开：仅 public-fulltext 条目，物理分开
  <id>/
    manifest.yaml
    source/                 # 允许公开的扫描/转录
    notes.md
index/
  items.jsonl               # 一行一条，供检索与快照
  snapshot.yaml             # tag、DOI、哈希、日期
```

- 先用**扁平文件＋JSONL 索引**，不建数据库、不起服务；
- 条目过千后再考虑 SQLite（只读镜像），仍不改变 manifest 为唯一真源；
- `index/items.jsonl` 由脚本从 manifest 生成，禁止手改。

### 15.2 最小可行版本（四步，不排时间表）

| 步 | 做什么 | 验收 |
|---|---|---|
| P0 元数据 | 50 条：中国古籍 20、17–18 世纪期刊/原刊 15、19–20 世纪专著 15；只写 manifest 与书目 | 50 条通过 schema；`visibility` 全部有值；无 `source/` 进 git |
| P1 公版全文 | 选 10 条公有领域件：扫描＋转录＋`page_map`＋哈希 | 任取 5 条，`#p<n>` 能定位到扫描页；哈希可复算 |
| P2 可引用 | 打 tag `corpus-v0.1.0`，Zenodo 归档，回填 DOI 与 `CITATION.cff` | 5 条引用在外部文档中可解析；DOI 可打开 |
| P3 检索 | 生成 `items.jsonl`，做按作者/年代/分支/许可的静态检索 | 不连数据库也能查；索引与 manifest 一致 |

### 15.3 不在 MVP 里

- OCR 自动流水线、众包校对、逐条 DOI、全文搜索服务、机构合作馆藏对接。
- 这些等到 P1 的 10 条跑通、证明 `page_map` 真能用，再谈。

## 16. 未决

| 编号 | 问题 | 现状 |
|---|---|---|
| P-2 | 馆方扫描条款与公有领域冲突时如何取证 | 逐件记录条款 URL 与日期，unknown 不放 |
| P-3 | 逐条 DOI 还是批次 DOI | MVP 用批次 DOI；条目多后再评估 DataCite |
| P-4 | 多卷本页码 `#v3-p12` 与单卷 `#p12` 是否统一 | 沿用 v0.2 T-10，暂不统一 |
| P-5 | 转录文本的校对等级如何分级 | 暂用 `human_checked: true/false`，不设更多级 |
| P-6 | 条目废弃后是否保留字节 | 保留元数据，字节按权利状态处理；id 永不复用 |

> 原 P-1（点校本版权）已升级为 §14.5 的既定规则 DEC-1，不再列为未决项。

