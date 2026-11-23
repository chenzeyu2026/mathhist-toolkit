# 全新环境上手实测记录

> 目的：按 README 从零走一遍，看会不会卡，卡在哪。方法是把仓库复制到一个干净目录（不含 `.git`、不含任何已装好的包），用一个新开的 PowerShell 会话执行 README 里的原话。

## 环境

- Windows，PowerShell 5
- 干净目录：`~\Documents\Trae-CN\temp_20261113_06\fresh\mathhist-toolkit`
- 使用系统 Python 3.11.9（`~\AppData\Local\Programs\Python\Python311`）

## 第一次走（README 初稿）

| 步骤 | 结果 | 实测耗时 |
|---|---|---|
| `python --version` | **失败**：Windows 把 `python` 指向应用商店别名，提示 "Python was not found" | 0.4 s |
| 改用 `py -3.11 --version` | 成功，Python 3.11.9 | 0.1 s |
| `py -3.11 -m mathlint check ..\prompts\examples` | 成功，`0 error / 0 warn / 0 info`，exit=0 | 0.3 s |
| `pip install -e tools`（在 `tools/` 下） | **失败**：`tools/tools` 不存在 | — |
| `pip install -e tools`（在根目录，带 `--no-build-isolation`） | **失败**：`readme = "../README.md"` 指向包目录之外，setuptools 拒绝 | 17 s |
| 同上，去掉 `--no-build-isolation` | **失败**：`invalid command 'bdist_wheel'`（venv 里没有 wheel） | 3 s |
| 改成带隔离的普通安装 | **卡住**：停在 `Installing build dependencies`，本机无外网 | 132 s 后手动终止 |

## 三个卡点与修复

**卡点 1：`python` 命令不可用。**
Windows 的"应用执行别名"会把 `python` 指向应用商店，报错信息还建议你去装 Python——但机器上明明有 3.11。
修复：README 加一行提示，改用 `py -3.11`，并给出等价命令。

**卡点 2：README 的安装命令 cd 位置自相矛盾。**
上文让读者 `cd tools`，下文却写 `pip install -e tools`，等于 `tools/tools`。
修复：安装段明确写"先回到仓库根目录"，并给出 `cd ..`。

**卡点 3：包的元数据指向了包目录之外。**
`pyproject.toml` 里 `readme = "../README.md"` 在 setuptools 下不合法（不能访问 `tools/` 之外的文件），安装直接失败。
修复：删掉该字段，改用 `description`；`build-system` 的最低 setuptools 从 68 降到 61。

**附带发现（未修复，改成了文档说明）：** 在无外网的机器上，`pip install -e` 必然卡在下载构建依赖（`wheel`）。这不是本项目能修的——除非把 `wheel` 也 vendored 进来，那会破坏"零依赖"的前提。因此 README 把安装定位为可选，并写明离线时直接用 `python -m mathlint`，功能完全一致。

## 第二次走（修复后）

| 步骤 | 结果 | 耗时 |
|---|---|---|
| `py -3.11 -m mathlint check ..\prompts\examples` | 3 个文件，全部 `0 error / 0 warn / 0 info`，exit=0 | 0.3 s |
| `py -3.11 -m mathlint check tests\fixtures\invalid.md` | 13 条 error / 1 warn，exit=1 | 0.2 s |
| 新建 `draft.md` 写一段带标记的论断 | 通过 | — |
| 把标记改成「百科标 A」 | 报 `GRADE_SOURCE_MISMATCH`，符合预期 | — |

从 `cd` 到看到第一份报告：**不到 1 分钟**（命令本身 0.3 秒，其余是读 README 的时间）。即使把三个卡点都算进去，第一次走也只用 4 分钟出头，未超过 5 分钟的上限；修复后不再需要试错。

## 结论

- 主路径（不安装、直接 `python -m mathlint`）在干净环境里 3 条命令内跑通，零依赖这一点是成立的。
- 安装路径依赖外网，属于已知限制，已在 README 标注。
- 真正会挡住新手的不是工具，而是 Windows 的 `python` 别名——这一条如果没实测，README 会一直是错的。
