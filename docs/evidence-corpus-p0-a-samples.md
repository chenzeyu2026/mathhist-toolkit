# P0 十条样板核验报告（B 级为主，A 级 0 条）

- 日期：2026-11-27
- 产物：`corpus/p0/verified-samples.yaml`（10 条，含每条的 `verification` 块与 `blockers`）
- 依据：`docs/evidence-corpus-design.md` §2（八项字段）、§14.1（三项判据）、§15.2（P1 验收：`#p<n>` 可定位、哈希可复算）
- 纪律：**只把已核的写成已核**；预览件单列 `held_files`，不当整件副本；未核字段仍为 `null`

## 0. 结论

| 等级 | 条数 | 含义 |
|---|---|---|
| A | **0** | 八项齐全（含完整字节、清单哈希、逐页核过的 `page_map`） |
| B+ | 1 | 有完整节选的字节与哈希、页码偏移区间已定位（Gauss） |
| B | 8 | 版次、馆藏、DOI、扫描页数、许可已核；缺字节、哈希、`page_map` |
| B− | 1 | 有节选字节与 DOI，但卷次与目录条目不符（Euler 1769） |

**一句话**：这十条都能回答“是哪一版、藏在哪、多少页、能不能公开”；Gauss 那一条还能回答“593–665 页在这 75 张扫描图里”。其余九条仍不能回答“第 12 页在哪张扫描图上”——A 级卡在全本字节与逐页页码映射。

## 1. 十条清单

| # | id | 版次（已核） | 入口 | 扫描页数 | 等级 |
|---|---|---|---|---|---|
| 1 | euler-1748-introductio | Lausannae: Bousquet, 1748（2 卷） | doi:10.3931/e-rara-8740 | 799 | B |
| 2 | euler-1755-institutiones-differentialis | St. Petersburg: Acad. Imp. Sci., 1755 | doi:10.3931/e-rara-3788 | 916 | B |
| 3 | newton-1687-principia-1st | Londini: Streater, 1687 | doi:10.3931/e-rara-440 | 515（节选 41） | B |
| 4 | lhopital-1696-analyse | Paris: Imprimerie Royale, 1696 | doi:10.3931/e-rara-10415 | 221 | B |
| 5 | legendre-1798-essai-theorie-nombres | Paris: Duprat, an VI [1798] | doi:10.3931/e-rara-3663 | 560 | B |
| 6 | cauchy-1821-cours-analyse | Paris: Imprimerie Royale / Debure, 1821 | doi:10.3931/e-rara-26182 | 604 | B |
| 7 | jbernoulli-1713-ars-conjectandi | Basileae: Thurnisiorum, 1713 | doi:10.3931/e-rara-9001 | 357 | B |
| 8 | newton-1704-opticks | London: S. Smith & B. Walford, 1704 | Wellcome d445akky / b30412316 | 406 | B |
| 9 | gauss-1801-disquisitiones | Lipsiae: Fleischer, 1801（Sectio septima 节选） | doi:10.3931/e-rara-4025 | 75（节选） | B+ |
| 10 | euler-1768-institutionum-integralis | Petropoli, 1769（第 2 卷 Caput II 节选，卷次待定） | doi:10.3931/e-rara-29420 | 31（节选） | B− |

为什么选这十条：20 条中国古籍按 DEC-1 全是点校本，`A（编订本）` 封顶且需登录馆藏；这十条都是 1900 年前西文原刊，公有领域明确、有开放数字化件，最可能补齐八项。

## 2. 八项字段的补齐情况

| 字段 | 已补 | 未补 | 说明 |
|---|---|---|---|
| `source.url` | 10/10 | — | 9 条 e-rara DOI，1 条 Wellcome 条目 |
| `source.retrieved` | 10/10 | — | 全部 2026-11-27 |
| `source.page_count` | 10/10 | — | 10 条均填；Gauss 75、Newton 41、Euler 31 是节选页数，整书页数另记在 note |
| `provenance.edition_statement` | 10/10 | — | 逐条取自 manifest/封面（出版地、社、年、卷页、开本）；Euler 1769 与目录 1768 不符，已注明 |
| `license.status` | 10/10 | — | e-rara 条目页 Public Domain Mark；Wellcome PDM |
| `license.basis` | 10/10 | — | 写明判定来源（页面标记 / manifest 许可 URL） |
| `source.page_map` | **0/10** | 10 条 | 未建；Gauss 只有“推定区间”，见 §3 |
| `source.sha256` / `source.bytes` | 3/10（均节选） | 7 条 | Gauss 75 页、Newton 1687 41 页、Euler 31 页；只对节选成立，不冒充整书 |

补充：`public_copy_allowed` 只有 Newton 1704 记 `true`（Wellcome 明示可再分发），其余全部 `false`。作品公版 ≠ 影像可再分发，仍按 §6 保守处理。

## 3. 为什么 0 条 A：卡在字节与页码映射

1. **免费下到的是预览，不是全本。** e-rara 的 `/download/pdf/<id>.pdf` 对多数条目返回 9–33 页的预览（Euler 1748 共 11 页、Legendre 9 页、Cauchy 19 页、l'Hôpital 33 页）。全本书的预览哈希不能当整件哈希。
2. **全本太大、链路太慢。** 实测 e-rara 下行约 **22 KB/s**，全本体积 45–165 MB：l'Hôpital 44.9 MB ≈ 35 分钟，Newton 1687 106 MB ≈ 80 分钟，Euler 1748 154 MB / Euler 1755 164 MB ≈ 2 小时，Cauchy 149 MB ≈ 2 小时，Bernoulli 70.5 MB ≈ 55 分钟。本轮已把能下的都试过，未能在合理时间内取全。
3. **`page_map` 比哈希更难。** 即使拿到全本，还要逐页把“扫描页序号 → 印刷页码”对上；e-rara 的 IIIF manifest 只给画布序号（`[1]…[n]`）和章节标题，不给印刷页码。预览件有 OCR 文本，可人工对几页，但覆盖不了整本。
4. **GDZ、DDB 没有可用的检索/页数接口。** GDZ 站内搜索是 JS 应用，SRU 端口不可达；DDB 需要 API key，条目页返回的是重定向页。Wellcome 的 API 最好用，但只能给元数据，页码映射仍要逐页做。
5. **节选例外只到节选。** 有三条拿到了真实节选：Gauss 75 页（Sectio septima，印刷页 593–665）、Newton 1687 41 页（Propositiones XXXI–XL，起页 44 已核、终点未核）、Euler 31 页（1769 年第 2 卷 Caput II）。字节与哈希是真的，但都不是整书，也没有逐页 `page_map`；Gauss 只因页码偏移算得通记 B+。Euler 那条连卷次都与目录的 1768 年不符，记 B−。

按用户口径：**“填了但没核”不算 A**。十条里没有一条的整件字节与逐页页码同时核过，所以 A 级为 0。

## 4. 已核部分的可复核证据

- **版次**：e-rara IIIF manifest 的 `metadata.Titel` / `Impressum` / `Umfang`，例如 Euler 1748 记 `Lausannae : apud Marcum-Michaelem Bousquet & socios, 1748`、`2 Bände (XVI, 320 S.; 398 S.)`。
- **馆藏**：`Besitzende Institution`，例如 `ETH-Bibliothek Zürich, Rar 5512`。
- **页数**：manifest 画布数（Euler 1748 = 799），与 `Umfang` 的印刷页数不是一回事，已在 `note` 里区分。
- **许可**：e-rara 条目页的 `Public Domain Mark` + `Nutzung` 两栏；l'Hôpital 的 manifest 还直接给了 `creativecommons.org/publicdomain/mark/1.0` URL；Wellcome manifest 的 `Attribution and usage` 明示可再分发。
- **Wellcome 版本**：`Publication/creation = London: Printed for S. Smith and B. Walford, 1704`，`ESTC T82019`，`144, 211 (i.e. 213) p.`，与 1704 初版相符。

复核方式：对每条 `verification.manifest` 取 JSON，比对 `metadata.Impressum`、`metadata.Besitzende Institution` 与 `num canvases`；DOI 用 `https://doi.org/<doi>` 解析回 e-rara 记录页。

## 5. 每条卡在哪、卡在谁

| 条 | 卡点 | 卡在谁 |
|---|---|---|
| Euler 1748 / 1755 | 全本 154/164 MB；预览 11 页 | 本机到 e-rara 的带宽（~22 KB/s） |
| Newton 1687 | 全本 106 MB | 同上 |
| l'Hôpital / Legendre / Cauchy | 全本 45/93/149 MB | 同上 |
| Bernoulli 1713 | 全本 70.5 MB；另需核编印者 | 带宽 + 人工核编者 |
| Newton 1704 | 全本无 Content-Length，需整流传 | Wellcome 下载方式；页数映射需人工 |
| Gauss 1801 | 全书未下；节选 `page_map` 仅 26/73 页 OCR 复核 | 带宽 + 人工逐页核 |
| Euler 1768 | 目录写 1768，取到的是 1769 年第 2 卷节选 | 人工先定卷次 |

## 6. 下一步（按性价比排序）

1. **Wellcome 优先**：图片下行 ~67 KB/s，是 e-rara 的 3 倍，且 Newton 1704 已明示可再分发。先拿它做第一条真 A：逐页取 406 张影像 → 清单哈希 → 人工对 3 页 `page_map` → 升级。
2. **e-rara 只取所需页**：用 IIIF 单页影像（每页约 170 KB）替代整本 PDF，先服务“要引的那几页”，把 `page_map` 做成“已核区间”而不是全本。
3. **Gauss 先补小步**：Sectio septima 的 73 页逐页核一遍（图像 OCR 或人工），把 B+ 推到 A（该节）；其余章节再按需取。
4. **Euler 先定卷次**：目录写 1768，现有 DOI 是 1769 年第 2 卷；先确认引用哪一卷，再取该卷全本。
5. **补 manifest schema**：这十条已具备字段形状，下一步把它写成 JSON Schema，让 `verified-samples.yaml` 过校验；否则仍只是人工核过的 YAML。

## 7. 未做的事（明确边界）

- 没有把任何预览件写进 `source.sha256` / `source.bytes`。
- 没有把 e-rara 的 `page_count` 当成“印刷页数”。
- 没有把 Wellcome 的 `public_copy_allowed: true` 当作已可进 `public-fulltext`——`page_map` 未建，仍停在 `public-metadata`。
- 没有把三条节选的哈希写进整书断言；Euler 的卷次不符已显式记出。
