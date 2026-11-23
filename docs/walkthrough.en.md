# Walkthrough: getting `mathlint` running from scratch

> For someone who has never used a command line and wants to verify this repository by hand.
> About 15 minutes end to end. Every command and every block of output below was **actually run** on a Windows machine on 2026-11-13 and pasted verbatim.
> Environment: Windows 11 · PowerShell 5.1 · Python 3.11.9 · git 2.56.0

## Step 0: open PowerShell

Either way works:

1. Press `Win`, type `powershell`, press Enter.
2. Open `<repo>` in File Explorer, type `powershell` in the address bar and press Enter. This starts you inside the repository, so you can skip Step 3.

You should see a line like:

```
PS C:\Users\yourname>
```

`PS` means PowerShell. The path inside the angle brackets is where you currently are; every relative path is resolved from it.

## Step 1: check that Python works

```powershell
python --version
```

**Three possible outcomes.**

### A: it prints `Python 3.11.x` or newer

Fine — go to Step 2.

### B: it prints an English error (this is what happened on this machine)

Actual output, unedited:

```
Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.
```

Exit code 9009. **This does not mean Python is missing — Windows' "app execution alias" has hijacked the name `python`.** The tell is the phrases `Microsoft Store` and `App execution aliases`. If you see them, it is an alias problem, not a missing interpreter.

Three fixes, any one:

1. **Fastest**: use the `py` launcher. `py -3.11 --version` prints:

   ```
   Python 3.11.9
   ```

   Every command below uses `py -3.11 -m mathlint`, which is exactly equivalent to `python -m mathlint`.
2. **Permanent**: `Settings > Apps > Advanced app settings > App execution aliases`, switch off both `python.exe` and `python3.exe`. Reopen PowerShell; `python --version` now works.
3. Install the official build from python.org and tick "Add python.exe to PATH".

### C: "is not recognized as the name of a cmdlet"

Python is genuinely absent. Install 3.11+ from python.org with "Add python.exe to PATH", then **close and reopen PowerShell** (environment variables are not refreshed in place).

## Step 2: check git (optional)

```powershell
git --version
```

On this machine:

```
git version 2.56.0.windows.2
```

**Do you need git?**

- Just **running** the tool: **no**. Copying the folder is enough.
- **Reading the change history** (e.g. how `reports/patch-diff.txt` was produced): yes.
- **Editing and committing**: yes.

Without git, nothing later in this walkthrough is blocked.

## Step 3: go to the repository

```powershell
cd "<repo>"
```

Confirm you are in the right place:

```powershell
Get-ChildItem
```

You should see `corpus  docs  prompts  reports  spec  tools` plus `README.md`, `LICENSE` and similar files.

> The path contains non-ASCII characters, so the **quotes are required** — otherwise PowerShell splits it at any space.

Now enter the tool directory (all later commands run here, because the `mathlint` package lives in it):

```powershell
cd tools
```

## Step 4: first run

```powershell
py -3.11 -m mathlint check ..\prompts\examples
```

Actual output (complete):

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

> The report lines are Chinese only in v0.1 — `--json` gives machine-readable English keys (`code`, `severity`, `line`, `col`, `message`).

How to read it:

- `mode=offline`: no network, local checks only (the default).
- `标记 N 条`: how many `〔…〕` tags were found.
- `论断 N 段（无标记 M 段）`: paragraphs judged substantive enough to need evidence, and how many have none.
- `exit=0`: exit code 0 means pass. **Exit codes are for scripts**: 0 = fine, 1 = errors, 2 = bad path.

The tool now runs. The three exercises below teach you to read its report.

## Exercise A: what a compliant document looks like

```powershell
py -3.11 -m mathlint check tests\fixtures\valid.md
```

Actual output:

```
mathlint 0.1.0 · mode=offline · files=1

<repo>\tools\tests\fixtures\valid.md
  标记 7 条 · 论断 5 段（无标记 0 段）
  无问题
  → 0 error / 0 warn / 0 info

合计：0 error / 0 warn / 0 info · exit=0
```

Open [../tools/tests/fixtures/valid.md](../tools/tests/fixtures/valid.md) alongside it: the seven tags cover primary, secondary, unverified and popular, plus nested and second-hand forms. This is what "correct" looks like.

## Exercise B: how a violating document is reported

```powershell
py -3.11 -m mathlint check tests\fixtures\invalid.md
```

Actual output (complete — this is the most important screen in the manual):

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

Anatomy of one line:

```
L5:19  error LEGACY_MARKER   说明文字  «出问题的原文片段»
 │      │     │              │
 │      │     │              └─ the offending text, truncated
 │      │     └─ stable machine-readable code; greppable in --json output
 │      └─ severity: error breaks the exit code, warn does not (unless --strict)
 └─ line 5, column 19
```

These 13 errors happen to cover all six check families: syntax (`TAG_NO_COLON`, `TAG_HALFWIDTH`, `TAG_UNCLOSED`, `TAG_EMPTY_LOCATOR`, `TAG_UNKNOWN_GRADE`, `LEGACY_MARKER`), citation parsing (`CITATION_DOI`, `CITATION_ISBN`), grade consistency (`GRADE_SOURCE_MISMATCH`, `GRADE_EDITORIAL`, `GRADE_SECONDHAND_A`, `TAG_GRADE_LABEL_MISMATCH`), and a bare `〔U〕` (`U_NO_REASON`).

Open [../tools/tests/fixtures/invalid.md](../tools/tests/fixtures/invalid.md) and match `L5`, `L15` and so on to see which sentence fired.

> Only want codes, not prose? Add `--json`:
> `py -3.11 -m mathlint check tests\fixtures\invalid.md --json`
> You get JSON; every object in `files[].issues` carries `code`, `severity`, `line`, `col`.

## Exercise C: run it on a real 41k-character draft

The draft has not been tagged at all:

```powershell
py -3.11 -m mathlint check ..\corpus\01-微积分起源.md
```

The output is **345 lines**. The opening lines and the last:

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

The key line: **0 tags, 242 claim paragraphs, 96 errors / 242 warnings.**

All 96 errors come from one habit — the old shorthand `【原】`, `【研】`, `【原/研】`, `【传】` in the draft. They carry no locator, so nothing can be checked; the tool calls that an error rather than a warning.

### Compare against the archived report

The repository keeps the report from the original run in `reports/baseline-human.txt`. Run it yourself and diff line by line:

```powershell
py -3.11 -m mathlint check ..\corpus\01-微积分起源.md > ..\reports\my-run.txt
$a = Get-Content ..\reports\my-run.txt
$b = Get-Content ..\reports\baseline-human.txt
$d = Compare-Object $a $b
if ($d) { "差异 $($d.Count) 行" } else { "两份输出完全一致（$($a.Count) 行）" }
```

Actual output:

```
两份输出完全一致（345 行）
```

And the total:

```powershell
Select-String -Path ..\reports\baseline-human.txt -Pattern '^合计'
```

Actual output:

```
<repo>\reports\baseline-human.txt:345:合计：96 error / 242 warn / 0 info · exit=1
```

If the numbers match, the tool on your machine agrees exactly with the archived report.

> Clean up afterwards: `Remove-Item ..\reports\my-run.txt`, or it will show up in `git status`.

### The patched draft

Same text, tags only added, no argument changed:

```powershell
py -3.11 -m mathlint check ..\corpus\01-微积分起源.patched.md
```

Actual result: `合计：0 error / 227 warn / 0 info · exit=0`.

Errors to zero; 227 warnings remain — those are paragraphs where **the draft never supplied a source**. The tool did not invent citations; it listed the gaps. The distance between fixing 96 errors and resolving 227 warnings is exactly the "what the tool can and cannot verify" of [`method.en.md`](method.en.md).

## Troubleshooting: if you see X, it means Y

| You see | It means | Do this |
|---|---|---|
| `Python was not found ... Microsoft Store` | app-alias hijack, not a missing install | use `py -3.11`, or turn the aliases off |
| `"python" is not recognized as the name of a cmdlet` | not installed, or not on PATH | install 3.11+, tick PATH, reopen the terminal |
| `mathlint: 路径不存在：xxx` + `exit=2` | wrong path, or not in `tools` | `Get-Location`; `cd` back; quote paths with non-ASCII characters |
| `No module named mathlint` | running outside `tools` | `cd <repo>\tools` first |
| Chinese renders as mojibake | console code page is not 65001 | run `chcp 65001` first, or use `--json` into a file |
| `合计：0 error / 0 warn / 0 info` yet `exit=1` | impossible; that is a bug | note the command and output, file an issue |
| Errors exist but the report says `0 error` | tags (or old-style markers) inside fenced code blocks and inline code spans are being shown, not used, so they are skipped | confirm the tag is outside code and not wrapped in backticks; a tag must close on the same line |
| A wall of `warn MISSING_TAG` | those paragraphs read as claims without evidence | tag them, or write "不承担推理" at the end of the paragraph |
| `--strict` suddenly fails | that flag makes warnings fatal | use `--strict` for final drafts only |

## What you still have to do

After the four steps above you have verified the tool works on your machine. What remains is the part only **you** can do:

1. **Bring your own draft** (`.md`), anywhere on disk.
2. Run `py -3.11 -m mathlint check "your-file.md"` from `tools`.
3. Fix errors first: replace `【原】`-style shorthand with `〔A｜原始文献:locator〕`; downgrade editorial introductions, second-hand quotations and encyclopedias.
4. Then handle warnings: for each `MISSING_TAG`, ask "is this a claim or a transition?" Tag claims; mark transitions "不承担推理".
5. Before finalising, add `--strict` so warnings block you too.
6. **The sources are your job.** The tool says "a locator is missing here"; it will not supply one. If you cannot find it, write `〔U｜未核实:the specific reason + how you plan to check〕` — that is better than inventing a plausible-looking citation.

## Self-check

If you can do all of this, you have learned it:

- [ ] Open PowerShell and explain what the path in `PS C:\...>` means
- [ ] Tell whether your `python` is hijacked, and name two workarounds
- [ ] Enter `tools` and explain why the command must run there
- [ ] Run `check ..\prompts\examples` and read `0 error / 0 warn`
- [ ] Parse `L5:19  error LEGACY_MARKER ...` into its five parts
- [ ] Explain the difference between `error` and `warn`, and what `--strict` changes
- [ ] Reproduce `96 error / 242 warn` on the 41k-character draft and match it with `Compare-Object`
- [ ] State what the tool **cannot** do (judge primary status, judge authorial intent)

If any item fails, return to its section and rerun it — every command above is copy-pasteable.
