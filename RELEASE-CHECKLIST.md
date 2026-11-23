# 公开发布前检查清单 / Release checklist

> 这份清单只列**必须由人完成**的事。机器能做的（单测、fixture、样例）已经在 `tools/scripts/selfcheck.py` 里，跑一条命令即可。
> 勾选前请确认你能说出"我做了什么、看到什么结果"，而不是"应该没问题"。
>
> Only human-only tasks are listed. Anything a machine can verify is already in `tools/scripts/selfcheck.py`.
> Tick an item only if you can state what you did and what you saw.

## 0. 机器可验证部分 / Machine-checkable

- [ ] `cd tools && python scripts/selfcheck.py` 全部 PASS
- [ ] `python -m mathlint check ../prompts/examples --strict` → 0 error / 0 warn
- [ ] `python -m mathlint --version` 输出 `mathlint 0.1.0`，与 `tools/pyproject.toml` 的 `version` 一致
- [ ] `git tag -n` 里 `v0.1.0` 指向的提交与 `CHANGELOG.md` 的条目对应
- [ ] 仓库内无 `__pycache__`、无 `.venv`、无临时文件被提交（`git ls-files | grep -E 'pycache|\.venv'` 应为空）

## 1. 规范的第二人审 / Second-person review of the spec

编号与 `spec/evidence-tags.md` §6（`spec/evidence-tags.en.md` §6 同）逐条对应，改这一节时必须同步改规范，不要只改一边。

- [ ] **T-1 学生课堂笔记**算 `A` 还是 `S`：规范倾向 `S`，但若笔记经作者校订、或作者以笔记为讲义底本则应算 `A`——判据未定
- [ ] **T-2 作者晚年回忆**：规范暂定"标 `A` 并注明『事后追述』"，但第一期正文把莱布尼茨"一道光突然照进来"那段按 `S` 处理，两者相反；必须解决，或明确写为"两说并存"
- [ ] **T-3 影印本**：能否标 `A`（规范允许，但限定于文字核对，不得用于纸张、水印、递藏等版本学判断）
- [ ] **T-4 只见重印本**：无原刊时能否标 `A`（规范按 R3 允许，但出处须写"据 19xx 年重印本，原刊卷期待查"）
- [ ] **T-5 转引链阈值**：现定"一层降 `S`、两层降 `U`"，两层是否过严
- [ ] **T-6 佚名批注**：按批注者定级（现定 `U`）还是按批注内容定级
- [ ] **T-7 四分法本身**：`A/S/U/F` 是否够用（它不是史学界通用标准，是为机器可检查做的折中）
- [ ] 审阅者姓名与日期记入 `spec/evidence-tags.md` 的版本说明

> 这七条在文中都标了"待议"。公开版本里保留待议是可以的，但必须有第二个人读过并留下意见；一个人写的规范不能直接对外当成标准。
> 译本等级不在这七条里——它已由规范 R2 定死（单独引译本标 `S`，双定位才可标 `A`）。

## 2. 英文文档 / English text

- [ ] `spec/evidence-tags.en.md` 由英语母语者或同等水平读者逐条校对
- [ ] `docs/method.en.md`、`docs/walkthrough.en.md`、`docs/evidence-corpus-design.en.md`、`docs/threshold-sensitivity.en.md` 同上
- [ ] 确认中英两版内容等价（不是摘要式翻译）：抽查 §4 冲突处理、§6 待议条款两处，逐段对照
- [ ] `README.en.md` 与 `README.md` 的命令、数字、链接一致

## 3. `--online` 实网验证 / Online mode against the real network

- [ ] 至少 5 个真实 DOI 能解析（含 1 个故意写错的，确认报 `DOI_UNRESOLVED`）
- [ ] 至少 5 个真实 URL：2 个存活、1 个 404（`LINK_DEAD`）、1 个 403 或 429（`LINK_BLOCKED`）、1 个不可达域名（`NETWORK_UNREACHABLE`）
- [ ] 在无网络环境下跑 `--online`，确认报的是"网络不可达"而不是"链接失效"
- [ ] 把实测样本与结果记入 `docs/`（新建一节或单独文件），注明日期与网络环境

> 目前 `--online` 只有单元测试，没有一次实网记录。这是公开发布前最容易被质疑的一项。

## 4. `MISSING_TAG` 阈值校准 / Threshold calibration

- [ ] 准备第二份语料：文体与第一期不同（建议书评或术语考据，2 万字以上）
- [ ] 随机抽 100 个单元，两人独立标注"是论断 / 不是论断"，计算标注者一致性
- [ ] 在 30/35/40/45/50 五个阈值上算准确率与召回率，把表补进 `docs/threshold-sensitivity.md`
- [ ] 决定是否改默认值；无论改不改，把理由写进文档
- [ ] 若改动，同步更新 `tools/scripts/selfcheck.py` 的期望条数

## 5. 命名与分发 / Naming and distribution

- [x] 查 PyPI 上 `mathlint` 是否已被占用（2026-11-16 实测：404，未占用；`mathhist`、`mathhist-toolkit` 同样空闲）
- [x] 包名定为 `mathlint`（取短、取特殊）；「被占用时改名或加前缀」分支作废
- [x] `tools/pyproject.toml` 的 `name` 为 `mathlint`，`classifiers` 覆盖 3.11–3.13；仓库目录名**定稿为暂不改**，等将来托管远程时一次性处理（代价见 `reports/release-selfcheck-2026-11-16.md` §六）
- [ ] 决定是否发布到 PyPI；本仓库当前只做本地安装（`pip install -e tools`）
- [ ] 若发布，补 `tools/README.md` 或 PyPI 长描述，并确认 `license` 字段与 `LICENSE` 一致

## 6. CI 首发 / First CI run

- [ ] 推送前确认 `.github/workflows/ci.yml` 的矩阵（3 系统 × 3 版本）在本机无法验证，需以第一次运行结果为准
- [ ] 首次运行后，把实际通过/失败情况记入 `CHANGELOG.md` 或 issue
- [ ] 若 Python 3.13 出现不兼容，记录并决定是否从矩阵移除
- [ ] 确认 Actions 的 `checkout`/`setup-python` 版本号仍是当前推荐版本

## 7. 法务与元数据 / Legal and metadata

- [ ] `LICENSE`（Apache-2.0）与 `LICENSE-docs`（CC BY 4.0）正文完整，未被截断
- [ ] `README.md` 顶部的许可说明与实际文件一致
- [ ] `corpus/01-微积分起源.md` 的转载/引用权限已确认（若作者非仓库所有者）
- [ ] 仓库内无个人信息、无凭证、无第三方未授权材料
- [ ] 决定是否加 `SECURITY.md`（本工具不联网处理敏感数据，可写"不适用"）

## 8. 发布动作 / Release actions

- [ ] 打 tag：`git tag -a v0.1.0 -m "mathlint 0.1.0"`（**不在本机推送到任何远程**）
- [ ] 确认 tag 指向的提交已包含本清单所有勾选项
- [ ] 若日后推送：先推分支，再推 tag；不要 force push 到 main
- [ ] 发布说明直接引用 `CHANGELOG.md` 的 0.1.0 一节

## 当前状态（2026-11-14）

- 已完成：§0 全部；tag `v0.1.0` 已在本机打好。
- 未完成：§1–§7 全部。也就是说，**代码层面可以发布，内容与合规层面还不可以。**
