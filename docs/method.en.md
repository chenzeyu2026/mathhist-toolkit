# Notes on using an evidence-tagging specification

> This is not a paper, and it is not a methodological innovation. It is a tool description plus a log of one real run: we built a tagging specification and a checker for people writing history of mathematics, then ran it on a 41,000-character manuscript and recorded what it caught and what it missed.

## 1. Why grading is necessary

Anyone writing about the evolution of mathematical ideas has met the same question: "How do you know Newton thought that?" There are three usual answers. I read the original page. I read a study. I cannot remember, but everyone says so. The evidential weight of these three differs by orders of magnitude, yet in prose they look identical — all three are declarative sentences.

The reader cannot tell them apart, and the author will not be able to tell them apart a few months later. Worse, the third kind reproduces itself: popular retellings are retold in textbooks, textbooks are cited in articles, and the article becomes the new "everyone says so".

So the first thing built here was not a tool but four tags:

- `〔A｜原始文献:locator〕` — written by the author, contemporary, locatable to edition and page;
- `〔S｜二手研究:locator〕` — peer-reviewed monographs and papers, scholarly introductions;
- `〔U｜未核实:reason〕` — a lead and an identifier, but the original has not been seen;
- `〔F｜流行说法:locator〕` — textbooks, popular science, encyclopedias, lectures.

The four-way split is not the standard in historiography. It is a compromise: fewer grades cannot separate "second hand" from "unverified"; more grades cannot be remembered by authors or implemented by tools. That trade-off is written into §6 of the spec as contested, not presented as settled.

## 2. How to use the specification

Tag as you write; never leave a gap, because gaps are forgotten.

Judgement takes three steps:

1. **Who wrote it?** The author → candidate `A`. A later hand → candidate `S`. Unknown → candidate `U`. Grade it `F` only when you have read the popular text and can say which kind it is (a textbook sidebar, an encyclopedia entry, popular science, a lecture); if you cannot even say which kind it might be, it is `U`.
2. **Which copy did I actually see?** Original, facsimile, reprint, translation, someone else's quotation — this step decides the downgrade. If you saw only a secondary work quoting the original page, write "quoted at second hand from <intermediary>" and grade `S` (spec R5).
3. **Can it be located?** Edition + page, or volume/issue + page, or holding + page. If it cannot be located, it is not `A`.

The two most common misuses:

- **Treating a textbook as authority.** A textbook that is authoritative mathematically is still `F` historiographically. Its "historical note" usually retells secondary work without locators; internal consistency is not evidence.
- **Using `U` to avoid judgement.** A passage that is all `U` should not be published. `U` has exactly three legitimate uses: a lead without the original, a damaged original, oral tradition only or an unattributed retelling (spec R8).

Before finalising, run `mathlint check . --strict` so that warnings block the commit too.

## 3. What the tool can check

`mathlint` does six things, all mechanically decidable:

1. Tag syntax: full-width `〔〕`, the `｜` bar, the grade letter, an empty locator.
2. Whether a claim has no tag at all: the text is split into paragraphs and list items; a unit longer than a threshold and ending in sentence punctuation counts as a claim.
3. Whether identifiers in the locator parse: DOI prefix and suffix, ISBN check digit, URL scheme and host, ARK's `ark:/` prefix.
4. Whether grade and source type are consistent: an encyclopedia or textbook graded `A`/`S`, an editor's introduction graded `A`, a second-hand citation graded `A` — all errors.
5. Whether `U` states a reason, and whether that reason is hollow ("to be checked").
6. Whether one citation key is graded differently in two places.

`--online` additionally probes link liveness and DOI resolution, and **separates two kinds of failure**: 4xx/5xx is "link dead" (error); DNS failure or timeout is "network unreachable" (info). The latter is not evidence that the source is bad. Treating a network fault as a defect in the source is the easiest mistake for a tool like this to make.

## 4. What the tool cannot check

It has to be said plainly: **the tool verifies citation parseability and grade consistency; it does not verify historical intent or the grading judgement itself.**

Concretely, it cannot:

- decide whether a source really is a primary source. It knows a vocabulary: "wikipedia", "textbook" trigger inconsistency. But a 1684 journal article tagged `A` — it cannot confirm that the volume really is the 1684 issue.
- decide whether the author's grading is right. Grading Boyer 1949 as `A` is an error (Boyer is not contemporary). Once it is graded `S`, whether Boyer's conclusion is sound is beyond the tool.
- verify offline that the locator exists. It checks the format only.
- decide whether two differently written locators are the same work. That depends on the author keeping citation keys stable (spec R12); keys written loosely will be missed.
- decide whether the tagged sentence is really supported by that source. It can find a paragraph with no tag; it cannot find a tag on the wrong sentence.

These are not items on a roadmap. They are the boundary of this class of tool. Any checker that claims to decide evidential grade automatically is making a judgement on the author's behalf that it cannot make.

## 5. One real run

The subject was a 41,000-character manuscript (the origin of calculus, Issue 01). Baseline:

- 96 errors, all from one shorthand: `【原】`, `【研】`, `【原/研】`, `【传】`.
- 242 warnings: paragraphs that cross the claim threshold and carry no tag at all.

Why is the shorthand an error? Because it compresses grade and locator into a two-character label. `【原】` tells you the author considers this primary material, but not which edition or page — so it can neither be checked now nor compared later. That is exactly the technical form of the "primary sources scattered across repositories" problem.

The patch did three things only: replace the shorthand with specification tags, fold the bibliographic note at the end of a paragraph into the locator, and write `待补出处` (locator pending) where the original gave none. No source was invented, and no argumentative sentence was edited.

Result: errors 96 → 0; warnings 242 → 227. Warnings fell by only 15, because of the 93 new tags, 29 have an empty locator, 17 give a title but no edition or page, and 3 grade a textbook example as `S`. All of these are reported — **they are real problems, not tool noise**.

The remaining 178 warnings are paragraphs that never gave a source. Adding a tag there would mean adding a source, which is outside "format only", so they stay.

## 6. Known problems

- **Paragraph splitting is heuristic**: code blocks, tables and headings are skipped, but a "misstatement / correction" block quote counts as a claim; claims shorter than the threshold are not checked.
- **The vocabulary over-fires**: "教材" in a locator triggers a downgrade hint, but "a textbook, p. 3, reproduces the 1687 original" is a false positive.
- **Citation keys depend on the author**: as above, the tool cannot disambiguate works.
- **"Contemporary" is not decidable**: the core condition of R1 cannot be mechanised; only the author can apply it.

## 7. Who it is for

For: people writing long-form pieces, facing "how do you know", willing to spend seconds tagging while writing.

Not for: short popular pieces that need no locators; and not for anyone who wants a tool to replace judgement. This setup assumes the author judges first and the tool only leaves a trace of the judgement.
