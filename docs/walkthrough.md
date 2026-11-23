# 跟练手册：从零把 mathlint 跑起来

> 对象：没跑过命令行、要亲手验收这个仓库的人。
> 全程约 15 分钟。所有命令与输出都是 2026-11-13 在一台 Windows 机器上**实际跑出来的**，逐字粘贴，没有改写。
> 环境：Windows 11 · PowerShell 5.1 · Python 3.11.9 · git 2.56.0

## 第 0 步：打开 PowerShell

两种方法，任选：

1. 按 `Win` 键，输入 `powershell`，回车。
2. 在文件资源管理器中打开 `<repo>`，在地址栏输入 `powershell` 后回车（这样打开时已经在仓库目录，可跳过第 3 步）。

看到类似这样的一行，说明成功了：

```
PS C:\Users\你的用户名>
```

`PS` 开头表示当前是 PowerShell。后面尖括号里的路径是"你现在在哪"，所有相对路径都从这里算。

## 第 1 步：确认 Python 可用

输入：

```powershell
python --version
```

**分三种结果**：

### 结果 A：显示 `Python 3.11.x` 或更高

正常，跳到第 2 步。

### 结果 B：跳出一段英文并报错（本机就是这种）

实际输出，一字不改：

```
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

退出码 9009。**这不是"没装 Python"，而是 Windows 的"应用商店别名"劫持了 `python` 这个名字**。判断方法：这段话里出现 `Microsoft Store` 和 `App execution aliases`，就是别名问题，不是解释器缺失。

修复，三种任选：

1. **最省事**：改用 `py` 启动器。输入 `py -3.11 --version`，正常会显示：

   ```
   Python 3.11.9
   ```

   本手册后面所有命令都用 `py -3.11 -m mathlint`，与 `python -m mathlint` 完全等价。
2. **彻底修**：`设置 > 应用 > 高级应用设置 > 应用执行别名`，把 `python.exe` 和 `python3.exe` 两个开关关掉。然后重开 PowerShell，`python --version` 就正常了。
3. 从 python.org 安装官方版本，安装时勾选 "Add python.exe to PATH"。

### 结果 C：提示"不是内部或外部命令"

说明这台机器没装 Python。去 python.org 下载 3.11 或更高版本，安装时勾选 "Add python.exe to PATH"。装完**关掉 PowerShell 再重开**（环境变量不会热更新）。

## 第 2 步：确认 git（可选）

```powershell
git --version
```

本机输出：

```
git version 2.56.0.windows.2
```

**你需要 git 吗？**

- 只是想**跑一遍**这个工具：**不需要**。把仓库文件夹拷过来即可。
- 想**看改动历史**（比如 `reports/patch-diff.txt` 是怎么生成的）：需要。
- 想**改内容并提交**：需要。

没装 git 又不打算装，不影响后面任何一步。

## 第 3 步：进入仓库

```powershell
cd "<repo>"
```

确认来对地方了：

```powershell
Get-ChildItem
```

应能看到 `corpus  docs  prompts  reports  spec  tools` 六个目录，以及 `README.md`、`LICENSE` 等文件。

> 路径带中文，**必须加引号**，否则 PowerShell 会在空格处断开。

再进工具目录（后面的命令都在这里跑，因为 `mathlint` 包就在当前目录下）：

```powershell
cd tools
```

## 第 4 步：跑第一次

```powershell
py -3.11 -m mathlint check ..\prompts\examples
```

实际输出（完整）：

```
mathlint 0.1.0 · mode=offline · files=3

<repo>\prompts\examples\example-1.md
  标记 1 条 · 论断 1 段（无标记 0 段）
  无问题
  → 0 error / 0 warn / 0 info

<repo>\prompts\examples\example-2.md
  标记 1 条 · 论断 1 段（无标记 0 段）
  无问题
  → 0 error / 0 warn / 0 info

<repo>\prompts\examples\example-3.md
  标记 1 条 · 论断 1 段（无标记 0 段）
  无问题
  → 0 error / 0 warn / 0 info

合计：0 error / 0 warn / 0 info · exit=0
```

读法：

- `mode=offline`：没联网，只做本地校验（默认行为）。
- `标记 N 条`：识别到几个 `〔…〕`。
- `论断 N 段（无标记 M 段）`：按段落判定的"有实质内容、该有证据"的段落数。
- 最后一行 `exit=0`：退出码 0，表示通过。**退出码是给脚本看的**，0 = 没问题，1 = 有 error，2 = 路径写错。

到这里，工具已经跑通了。剩下的三个练习是学会读它的报告。

## 练习 A：合规文档长什么样

```powershell
py -3.11 -m mathlint check tests\fixtures\valid.md
```

实际输出：

```
mathlint 0.1.0 · mode=offline · files=1

<repo>\tools\tests\fixtures\valid.md
  标记 7 条 · 论断 5 段（无标记 0 段）
  无问题
  → 0 error / 0 warn / 0 info

合计：0 error / 0 warn / 0 info · exit=0
```

打开 [../tools/tests/fixtures/valid.md](../tools/tests/fixtures/valid.md) 对照看：7 条标记里有原文、二手、未核实、流行说法四种，还有嵌套与转引的写法。这是"标准答案"的样子。

## 练习 B：违规文档怎么报错

```powershell
py -3.11 -m mathlint check tests\fixtures\invalid.md
```

实际输出（完整，这一屏是本手册最重要的一屏）：

```
mathlint 0.1.0 · mode=offline · files=1

<repo>\tools\tests\fixtures\invalid.md
  标记 10 条 · 论断 2 段（无标记 0 段）
  L5:19  error LEGACY_MARKER          旧式简写「【原】」不合规范：它不含出处，无法核查；应改写为 〔A｜原始文献:出处〕 等形式  «【原】»
  L7:22  error GRADE_SOURCE_MISMATCH  来源含「维基」，属流行转述（F 级），不能标 A  «〔A｜原始文献:维基百科「Non-standard analysis」条目〕»
  L7:22  warn  LOCATOR_NO_LOCATION    出处里没有任何数字（无版次、年份或页码），无法定位（规范 R3）  «〔A｜原始文献:维基百科「Non-standard analysis」条目〕»
  L9:18  error CITATION_DOI           DOI 格式不合法：「10.1234」（应为 10.<注册号>/<后缀>，不含空格）  «〔S｜二手研究:Smith 2019, DOI:10.1234 bad doi〕»
  L11:16  error CITATION_ISBN          ISBN 校验失败：「978-0-387-12345-6」（位数或校验位不正确）  «〔S｜二手研究:Some Book, ISBN:978-0-387-12345-6〕»
  L13:9  error TAG_EMPTY_LOCATOR      标记的出处为空  «〔S｜二手研究:〕»
  L15:11  error TAG_UNKNOWN_GRADE      未知等级「B」，只允许 A/S/U/F  «〔B｜二手研究:Grabiner 1981〕»
  L17:8  error TAG_NO_COLON           标记缺少冒号，应为 〔A｜原始文献:出处〕  «〔S｜二手研究 Grabiner 1981〕»
  L19:12  error GRADE_SECONDHAND_A     转引不能标 A（规范 R5）：应标 S 并写明「转引自 <中转者>」  «〔A｜原始文献:转引自 Boyer 1949, p. 212；原文献 Cantor 1894, Bd. III, p. 89〕»
  L21:11  error U_NO_REASON            〔U〕必须写出未核实的原因，不能只写「待查」一类的空话（规范 R8）  «〔U｜未核实:待查〕»
  L23:13  error GRADE_EDITORIAL        编者导言/前言由后人撰写，属 S 级（规范 R4）；若为作者自序请写明「作者自序」  «〔A｜原始文献:Opera omnia, Ser. 1, Vol. X, 编者导言, p. vii〕»
  L25:14  error TAG_GRADE_LABEL_MISMATCH 等级 A 的来源类型应为「primary/原始文献」，实际写的是「二手研究」  «〔A｜二手研究:Boyer 1949, p. 212〕»
  L27:11  error TAG_HALFWIDTH          使用了半角方括号，应为全角〔〕  «[A｜原始文献:Leibniz 1684]»
  L29:9  error TAG_UNCLOSED           标记未闭合：缺少「〕」  «〔A｜原始文献:Leibniz 1684  这条 URL 结构不合法。〔A｜原始»
  → 13 error / 1 warn / 0 info

合计：13 error / 1 warn / 0 info · exit=1
```

每行怎么读：

```
L5:19  error LEGACY_MARKER   说明文字  «出问题的原文片段»
 │      │     │              │
 │      │     │              └─ 被判定有问题的原文（截断显示）
 │      │     └─ 机器可读的错误代码，可在 --json 输出里 grep
 │      └─ 级别：error 会让退出码变 1，warn 不会（除非加 --strict）
 └─ 第 5 行第 19 列
```

这 13 条 error 恰好覆盖了六类检查：语法（`TAG_NO_COLON`、`TAG_HALFWIDTH`、`TAG_UNCLOSED`、`TAG_EMPTY_LOCATOR`、`TAG_UNKNOWN_GRADE`、`LEGACY_MARKER`）、引文解析（`CITATION_DOI`、`CITATION_ISBN`）、等级自洽（`GRADE_SOURCE_MISMATCH`、`GRADE_EDITORIAL`、`GRADE_SECONDHAND_A`、`TAG_GRADE_LABEL_MISMATCH`）、`〔U〕` 缺原因（`U_NO_REASON`）。

打开 [../tools/tests/fixtures/invalid.md](../tools/tests/fixtures/invalid.md)，把 `L5`、`L15` 这些行号对上去，能看到是哪些句子触发的。

> 想只看错误码、不看长句子？加 `--json`：
> `py -3.11 -m mathlint check tests\fixtures\invalid.md --json`
> 输出是一段 JSON，`files[].issues` 数组里每条都有 `code`、`severity`、`line`、`col`。

## 练习 C：拿真实稿件跑一遍

这一篇是 4.1 万字的真实稿子，原稿没做过任何标记：

```powershell
py -3.11 -m mathlint check ..\corpus\01-微积分起源.md
```

输出共 **345 行**，这里给开头几行和结尾：

```
mathlint 0.1.0 · mode=offline · files=1

<repo>\corpus\01-微积分起源.md
  标记 0 条 · 论断 242 段（无标记 242 段）
  L3:1  warn  MISSING_TAG            该段/条目是论断但没有证据标记（规范 R13）；若是过渡或评价性文字，请显式写「不承担推理」  «系列：数学思想的演化（第 1 期 / 共 9 期） 读者设定：大一计算机专业，高»
  L12:1  warn  MISSING_TAG            该段/条目是论断但没有证据标记（规范 R13）；若是过渡或评价性文字，请显式写「不承担推理」  «微积分的故事通常被讲成一条直线：古代求积 → 牛顿和莱布尼茨发明微积分 → 贝克»
  ...
  → 96 error / 242 warn / 0 info

合计：96 error / 242 warn / 0 info · exit=1
```

关键信息：**标记 0 条，论断 242 段，96 error / 242 warn**。

96 个 error 全部来自一种写法——旧稿里的 `【原】`、`【研】`、`【原/研】`、`【传】`。它们不含出处，工具无法核查，所以判 error，而不是 warn。

### 与存档报告对照

仓库里存了当时跑出来的完整报告 `reports/baseline-human.txt`。你自己跑一遍，可以逐行比对：

```powershell
py -3.11 -m mathlint check ..\corpus\01-微积分起源.md > ..\reports\my-run.txt
$a = Get-Content ..\reports\my-run.txt
$b = Get-Content ..\reports\baseline-human.txt
$d = Compare-Object $a $b
if ($d) { "差异 $($d.Count) 行" } else { "两份输出完全一致（$($a.Count) 行）" }
```

实际输出：

```
两份输出完全一致（345 行）
```

再确认一下总分：

```powershell
Select-String -Path ..\reports\baseline-human.txt -Pattern '^合计'
```

实际输出：

```
<repo>\reports\baseline-human.txt:345:合计：96 error / 242 warn / 0 info · exit=1
```

如果两边数字一样，说明你这台机器上的工具与存档报告完全一致。

> 跑完记得删掉临时文件：`Remove-Item ..\reports\my-run.txt`，否则它会出现在 `git status` 里。

### 再看修补后的稿子

同一篇，只补标记、不改论证，修完的样子：

```powershell
py -3.11 -m mathlint check ..\corpus\01-微积分起源.patched.md
```

实际结果：`合计：0 error / 227 warn / 0 info · exit=0`。

error 归零，warn 还剩 227——这些是**原稿本来就没给出处**的段落。工具没有替你编文献，只是把问题列出来。补完 96 个 error 与看完这 227 条 warn 的差别，就是 [`method.md`](method.md) 里说的"工具能验与不能验"。

## 常见问题：看到 X 就说明 Y

| 你看到 | 说明 | 怎么办 |
|---|---|---|
| `Python was not found ... Microsoft Store` | 被应用商店别名劫持，不是没装 | 改用 `py -3.11`，或关掉"应用执行别名" |
| `python : 无法将"python"项识别为...` | 确实没装，或 PATH 没配 | 装 Python 3.11+，勾 PATH，重开终端 |
| `mathlint: 路径不存在：xxx` + `exit=2` | 文件/目录名写错，或当前不在 `tools` 目录 | `Get-Location` 看当前位置；`cd` 回来；路径含中文要加引号 |
| `No module named mathlint` | 不在 `tools` 目录下跑 | `cd <repo>\tools` 再跑 |
| 中文显示成乱码 | 终端代码页不是 65001 | 先跑 `chcp 65001`；或 `--json` 重定向到文件再看 |
| `合计：0 error / 0 warn / 0 info` 但仍 `exit=1` | 不可能，这是 bug | 记下命令与输出提 issue |
| 明明有错误却说 `0 error` | 写在围栏代码块或行内代码（反引号）里的标签/旧写法，是在"展示"而不是"使用"，会被跳过 | 确认要检查的标签不在代码块内，也没被反引号包住；标签必须与正文同行闭合 |
| `warn MISSING_TAG` 一大片 | 这些段落被判为"论断但没有标记" | 要么补标记，要么在段末写"不承担推理" |
| `--strict` 后突然失败 | 该参数把 warn 也算作失败 | 定稿用 `--strict`，草稿别用 |

## 你还要做什么

跑完上面四步，你已经验证了这个工具在本机可用。接下来是**你**才需要做的部分：

1. **准备一篇自己的稿子**（`.md`），放在任意目录。
2. 跑 `py -3.11 -m mathlint check "你的文件.md"`（在 `tools` 目录下）。
3. 先修 error：旧写法 `【原】` 一律换成 `〔A｜原始文献:出处〕`，编者导言/转引/百科一律降级。
4. 再处理 warn：每条 `MISSING_TAG` 问自己"这句是论断还是过渡"。论断补标记；过渡写"不承担推理"。
5. 定稿前加 `--strict`，让 warn 也拦住你。
6. **出处要你自己查**。工具只会说"这里缺出处"，不会替你补。补不出来就写 `〔U｜未核实:具体原因 + 打算怎么查〕`——这比编一个看起来像真的出处要好。

## 自检清单

全部能做到，就算学会了：

- [ ] 能打开 PowerShell，并说出 `PS C:\...>` 这一行里的路径是什么意思
- [ ] 能判断自己的 `python` 是不是被应用商店劫持，并知道两种绕过办法
- [ ] 能进入 `tools` 目录，并解释为什么必须在这里跑
- [ ] 能跑通 `check ..\prompts\examples` 并读出 `0 error / 0 warn` 的含义
- [ ] 能读懂 `L5:19  error LEGACY_MARKER ...` 这一行的五个部分
- [ ] 知道 `error` 与 `warn` 的区别，以及 `--strict` 改变的是什么
- [ ] 能跑出 4.1 万字稿子的 `96 error / 242 warn`，并用 `Compare-Object` 与存档报告对上
- [ ] 能说出这个工具**不能**做什么（判断原始文献、判断作者原意）

做不到其中任何一条，回到对应小节重跑一次；命令都在上面，可以直接复制。
