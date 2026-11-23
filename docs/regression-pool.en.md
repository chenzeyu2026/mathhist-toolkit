# Wrong-answer pool (regression pool)

> Every problem already found becomes a case that can be re-run. Two purposes: an old problem must not be lost by a later check (false negative), and correct text must not be rejected by a new check (false positive).
>
> Cases live in `tools/tests/regression_pool.py`; `tools/tests/test_regression_pool.py` runs them.

## How to run

```bash
cd tools
py -3.11 -m unittest discover -s tests -p "test_regression_pool.py" -v
```

Or run `py -3.11 tools/scripts/selfcheck.py` — its first step is `unittest discover`, so the pool runs with the rest of the suite and needs no separate expected counts.

## Two kinds of case

| Kind | Meaning | What to do when it fails |
|---|---|---|
| `auto` | The spec settles this; current behaviour is the intended behaviour | Treat it as a regression and fix the code. If the spec really changed, change the spec, the case and this file together |
| `locked` | Current behaviour is a **known deviation, heuristic false positive or implementation quirk** — not a satisfied clause | Decide whether the change fixed or broke it, then update the expectation, the spec and this file |

A `locked` case is not a fake passing test. It pins today's fact; its comment states what the spec asks, what the tool does, and why it is not changed here. Turning `locked` into `auto` means the deviation has been dealt with.

## Cases

| ID | Rule | Input (summary) | Expected | Kind |
|---|---|---|---|---|
| RP-01 | R3 / §1 locator must be usable | `〔A｜原始文献:待补〕` | `LOCATOR_PLACEHOLDER` warn | auto |
| RP-02 | R8 reason must not be hollow | `〔U｜未核实:待补〕` | `LOCATOR_PLACEHOLDER` warn + `U_NO_REASON` error | auto |
| RP-03 | R7 textbooks are `F` | `〔S｜二手研究:某高数教材, p. 233〕` | `GRADE_SOURCE_WEAK` warn | locked |
| RP-04 | R7 lectures are `F` | `〔S｜二手研究:某公开讲座, 2020〕` | `GRADE_SOURCE_WEAK` warn | locked |
| RP-05 | R2 translation cited alone | `〔A｜原始文献:牛顿《原理》中译本, p. 41〕` | `GRADE_TRANSLATION` warn | auto |
| RP-06 | R2 **positive example** | `〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II（Motte 1729 英译本, p. 41）〕` | `GRADE_TRANSLATION` warn | locked |
| RP-07 | R2 / §4.2 one book, two layers | collated edition: body `A` + collation note `S`, layers named in the locator | no issue | auto |
| RP-08 | §4.2 one citation key | same, but the first three segments are identical | `MULTI_GRADE` warn | locked |
| RP-09 | §1.3 nesting | `S` locator with an `A` tag nested inside | no issue; 1 top-level tag + 1 nested | auto |
| RP-10 | §1.3 invalid nested tag | inner tag written `〔X｜原始文献:…〕` | `TAG_UNKNOWN_GRADE` error (only) | locked |
| RP-11 | R13 / same-line closing | tag broken across a newline | `TAG_UNCLOSED` + `TAG_STRAY_CLOSE` error | locked |
| RP-12 | §1 full-width bar | `〔A|原始文献:Leibniz 1684, p. 467〕` | no issue | locked |
| RP-13 | R1(c) / R3 edition–page pair | `〔A｜原始文献:Leibniz 1684〕` | no issue | locked |
| RP-14 | R8 missing next step | `〔U｜未核实:仅见书目著录，未见 1684 年原刊影像〕` | `U_NO_NEXT_STEP` warn | auto |
| RP-15 | §1 legacy shorthand | `【原】` in the body | `LEGACY_MARKER` error | auto |
| RP-16 | R4 exception | `〔A｜原始文献:Euler E212, 作者自序, p. iii〕` | no issue | auto |
| RP-17 | R4 editor's introduction | `〔A｜原始文献:Opera omnia, Ser. 1, Vol. X, 编者导言, p. vii〕` | `GRADE_EDITORIAL` error | auto |

## Why eight cases are locked

1. **RP-03 / RP-04** — R7's "Tool" paragraph says a textbook or lecture graded `A`/`S` is an `error`; the implementation puts both words in `WEAK_POPULAR` and emits `warn`. Recorded, not changed.
2. **RP-06** — the tag is R2's own positive example, yet `GRADE_TRANSLATION` warns because its locator lacks the literal word 「原文」. Spec says compliant, tool says suspicious; pinned so nobody deletes it as a false positive.
3. **RP-08** — `citation_key` keeps only the first three comma-separated segments, so 「卷一」 / 「校记」 are dropped and two layers collapse into one key. §4.2 asks authors to write the difference into the locator, but writing it does not help. The message already says "confirm manually".
4. **RP-10** — line/column of a nested issue are computed against the locator substring, not the document, so the case asserts the code and severity only.
5. **RP-11** — the parser gives up at `\n`, so one cross-line tag yields two errors and a message that says the `〕` is missing when it is on the next line. R13 fixes the tag's position, not its line span.
6. **RP-12** — `parser.BARS` accepts `｜` and `|` alike, and no check targets the half-width bar (`TAG_HALFWIDTH` covers half-width brackets only). §1 requires the full-width bar. A future `TAG_HALF_BAR` should fail this case on purpose.
7. **RP-13** — `LOCATOR_NO_LOCATION` only asks whether any digit is present. 「1684」 is a digit, so the tag passes; whether a year is a sufficient locator is a historiographical judgement.

## What cannot be asserted

These have no executable case and are registered in `SEMANTIC_ONLY`. Do not invent a passing test for them:

| ID | Item | Why it cannot be automated |
|---|---|---|
| SP-01 | "Source unknown" is graded `U` (decided 2026-11-16; `docs/method*.md:26` and R8(c) now agree) | The decision is a semantic judgement; the tool cannot tell "unknown" from "known but unwritten" |
| SP-02 | Is a year a sufficient locator? | Depends on the work; a historiographical judgement (RP-13 only pins "no warning today") |
| SP-03 | Do the body and the collation note really belong to two layers? | Needs the physical book; RP-08 only pins "warns, confirm manually" |
| SP-04 | `corpus/` locator parsing | v0.2 work; v0.1 has no code, so no case can be built |
| SP-05 | Does an `F` tag come with the `A`/`S` it points to? | Needs reading the prose, not the tag layer |

## Rules for adding a case

1. One defect, one case; IDs are never reused.
2. Write down the rule and the expected result, then run it — **expectations come from an actual run**, never from reading the spec.
3. If reality disagrees with the spec, mark the case `locked`, state both sides in the comment and register it above. Do not fake an `auto` pass.
4. Semantic questions go to `SEMANTIC_ONLY`, not `CASES`.
5. After adding or changing a case, `selfcheck.py` must pass as a whole; §0 of `RELEASE-CHECKLIST.md` is ticked on that basis.
