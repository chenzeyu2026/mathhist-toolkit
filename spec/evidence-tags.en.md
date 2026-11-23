# Evidence Tagging Specification v0.1

> Scope: writing on the history of mathematics and the evolution of mathematical ideas.
> Status: v0.1 draft. Clauses may be contested (see §6).
> Companion tool: `tools/mathlint`. Every rule states whether the tool can decide it automatically. This is deliberate: it prevents the project from claiming that the tool does what it cannot.

---

## 0. What this specification is for

Three concrete problems:

1. **Claims carry no evidence grade.** "Newton thought that…", "scholars agree that…" and "I read the original page" sit in the same paragraph, so the reader cannot tell which sentence is checkable.
2. **Primary sources are scattered across repositories.** The same source is written in three different ways in three different sections, so it cannot be reconciled afterwards, and it is impossible to see which passages rest on different grades.
3. **Historical fact and popular misstatement are mixed.** Popular narratives, textbook sidebars and encyclopedia entries sit next to primary sources, and the misstatement is inherited as fact.

The point of a tag is not to make the prose look rigorous. It is to make every checkable claim carry its source, so that a machine and a human can check different things about it.

---

## 1. Tag syntax

```
〔<grade>｜<source-type>:<locator>〕
```

- Brackets: full-width tortoise-shell brackets `〔` `〕` (U+3014 / U+3015). Not `【】`, not `[]`, not `()`.
- Separator between grade and source type: full-width vertical bar `｜` (U+FF5C).
- Separator between source type and locator: a colon, **ASCII `:` preferred**; the full-width `：` is also accepted by the parser, but one document should use one form.
- The grade is a single character: `A`, `S`, `U`, `F`.
- The locator must not be empty.

### 1.1 The four grades

| Grade | Name | Meaning | May it support a claim alone? |
|---|---|---|---|
| `A` | Primary source | The author's own work, manuscript, letter, the original volume/issue of a contemporary journal, the author's own preface or marginal note | Yes |
| `S` | Secondary | Peer-reviewed monographs and papers, scholarly editor's introduction, authoritative reference entries (e.g. DSB), research appendices in a critical edition | Yes, but must be read against `A` |
| `U` | Unverified | There is a lead (bibliography, holding, identifier) but the original object or page has not been seen | No; it must stay on the to-do ledger |
| `F` | Popular | Textbooks, popular science, encyclopedias, lectures, blogs, videos, textbook sidebars | No; lead only |

Note: this specification does not use `B`, `C` or `T`. Where an older draft or an external prompt set uses B (authoritative secondary), read `S`; where it uses C (popular retelling), read `F`. `T` (quotation at second hand) is not a grade here but a required field on `S` (see R5). Reason: a grade answers "how far is this evidence from the original object", while second-hand quotation answers "through whom did this evidence pass". These are two dimensions. Collapsing them into one letter leaves "a secondary work known only at second hand" with nowhere to go.

### 1.2 Examples

```
〔A｜原始文献:Leibniz, "Nova methodus pro maximis et minimis", Acta Eruditorum, Oct. 1684, pp. 467–473〕
〔S｜二手研究:Grabiner 1981, pp. 45–52〕
〔U｜未核实:仅见 19 世纪书目著录，未见 1684 年原刊影像；待查 Acta Eruditorum 1684 年卷〕
〔F｜流行说法:某高数教材「历史注记」边栏：柯西消灭了无穷小〕
```

The source-type word inside the tag is fixed by grade in the Chinese edition (`原始文献` / `二手研究` / `未核实` / `流行说法`). English-language documents may use the same four Chinese labels, or the English equivalents `primary` / `secondary` / `unverified` / `popular`; the linter accepts both sets and requires that the label match the grade.

### 1.3 Multiple sources, nesting, second-hand quotation

- **Several sources for one sentence**: write the tags side by side, with no comma between them. `〔A｜...〕〔S｜...〕`
- **Nesting**: a tag may appear inside another tag's locator, to record that the secondary work itself quotes a primary source. The parser pairs brackets by depth; it does not use a greedy regular expression.
  ```
  〔S｜二手研究:Boyer 1949, p. 212（其注引〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II〕）〕
  ```
- **Second-hand quotation**: when you have seen only the intermediary and not the page of the cited work, the locator must name both the intermediary and the final source, and the grade must not be `A`.
  ```
  〔S｜二手研究:转引自 Boyer 1949, p. 212；原文献 Cantor 1894, Bd. III, p. 89（未见原页）〕
  ```
  The "intermediary" is **the book you actually opened** (Boyer), not the work being cited (Cantor).

### 1.4 Four machine-parseable identifiers in the locator

`mathlint` attempts to parse the following. A malformed identifier is an `error`:

| Type | Form | Check |
|---|---|---|
| DOI | `DOI:10.1093/...` | prefix `10.` + registrant + `/` + suffix; no spaces |
| ISBN | `ISBN:978-0-387-...` | 10 or 13 digits; check digit must be correct |
| URL | `https://...` | must have a scheme and a host |
| Archival ID | `ARK:ark:/12148/bpt6k205444w`, `E212`, `MS:<holding id>` | `ARK:` followed by `ark:/`; Eneström numbers are `E` + digits |

### 1.5 Situational validity: fields that cannot co-occur

A locator is not a free-text box. It is described by six dimensions:

| Dimension | Values | Defined by |
|---|---|---|
| Carrier | original, same-format facsimile, reset reprint, translation, punctuated edition (undivided), punctuated-edition body, editor's collation notes, modern critical transcript, author-approved notes, unauthorised student notes, late memoir, named marginalia, anonymous marginalia, secondary retelling, popular account | §1.1, R1–R4, R7, R9 |
| Locator completeness | edition + page complete / edition without page / placeholder | R1(c), R3 |
| Quotation depth | 0 / 1 / ≥2 | §1.3, R5 |
| Original page | given / not given | R2, R3 |
| Intermediary | named / anonymous / none | §1.3, R5 |
| Blockage | none / lead but no original seen / original page missing | R8 |

These six are **not always independent**: **the carrier determines which dimensions are meaningful.** The clauses below are hard constraints. Violating one is not "bad style" — it describes a situation that does not exist.

**E1 Quotation depth is meaningful only for "retold by someone else".**
Only when the carrier is a secondary retelling does "how many layers were quoted" state a fact. Whenever you hold the carrier yourself (original, facsimile, translation, punctuated edition, transcript, notes, marginalia, memoir), depth is 0.
- Test: `carrier ≠ secondary retelling ⇒ depth = 0`.
- Consequence: `〔A｜原始文献:Euler 1755, p. 12〕` can neither claim "quoted from X" nor claim two layers.

**E2 An intermediary exists only when depth ≥ 1.**
- Test: `depth = 0 ⇒ intermediary field empty`; `locator contains "转引自 / quoted from" ⇒ depth ≥ 1`.
- Consequence: at depth 0, "anonymous intermediary" has no referent.

**E3 A held carrier cannot also claim "original not seen".**
"Has a lead but has not seen the original" contradicts "carrier is the original / a facsimile / a punctuated edition / a transcript": if you filled in that carrier, you have it.
- Test: `blockage = lead but no original seen ⇒ carrier = secondary retelling`. The same blockage on any other carrier is invalid.
- Writing consequence: to say "I know this original exists but have not looked at it", set the carrier to `U｜未核实` directly, rather than writing `A` and appending "original not seen".

**E4 A missing page is incompatible with "edition + page complete".**
"Original page missing / damaged / illegible" means that page cannot be had, so the locator cannot be complete at the same time.
- Test: `blockage = original page missing ⇒ locator completeness ≠ complete`.
- The admissible combination is "edition without page": you know the volume and edition, but that page is missing.

**E5 When the locator is a placeholder, blockage has no referent.**
- Test: `locator completeness = placeholder ⇒ blockage field empty`; such a situation is graded `U` (see R8).

**E6 The original-page field is meaningful only when the carrier points at another original.**
Translations, secondary retellings and the body of a collected or punctuated edition may also give the original page (the double locator of R2 and R3); when the carrier *is* the original (the original issue), the page is the original page and the field is empty.
- Test: `carrier = original ⇒ original-page field empty`.
- A same-format facsimile usually falls under the same case, but to avoid confusion with pagination the facsimile itself adds, the audit counts it as an independent field; every situation count the audit reports (168 / 90 for the v0.1 encoding, 160 / 86 for the v1 baseline) is therefore an **upper bound**.

**How to use these six.** E1, E3 and E4 are **eliminating**: a violation means the situation does not exist, and together they remove 1244 combinations. E2, E5 and E6 are **merging**: a violation does not remove the situation, it only leaves that dimension empty, so different spellings of one situation count once. With 15 carriers × 3 locator states × 3 depths × 2 original-page states × 2 intermediary states × 3 blockage states = 1620, eliminating E1/E3/E4 leaves 376; merging by E2/E5/E6 leaves 168 (a dimension counts as live if it has a referent) and 90 (only dimensions the rules actually read). The v1 baseline drops the undivided fifth carrier (next paragraph), giving 1512 → 356 → 160 / 86; §5.1 reports this set.

The fifth carrier value, "punctuated edition (undivided)", is a known ambiguity: R2 treats punctuation and collation as editorial work and grades the whole volume `S`, while R3 allows the author's body text in a punctuated edition to be `A`. The two do not conflict — they describe two layers of one book — but the distinction exists in the text only if you write "punctuated-edition body" or "editor's collation notes". Left undivided, it remains a fifth carrier value and the grade will wobble. Therefore: **always state whether a punctuated edition is being cited for its body or for its collation notes**; once stated, the carrier value is one of 14.

The point of the compression is not prettier numbers. The eliminated combinations describe things that do not exist: they can support no claim and refute no claim, so using them as a denominator only inflates the conflict rate. `mathlint` does not yet implement E1–E6; it only pairs brackets and matches vocabularies. Suggested codes when implemented: `INVALID_CONTEXT` (eliminating) and `DEGENERATE_FIELD` (merging).

---

## 2. The thirteen rules

Each rule gives: the decision, a positive example, a negative example, and whether the tool can decide it (automatic / partial / impossible).

### R1 What counts as a primary source

**Decision**: all three conditions must hold for `A` — (a) the text was produced by the author, or by a contemporary recorder acting with the author's authority; (b) the text is contemporary with the event it reports (written soon after, during the author's lifetime); (c) it can be located in a specific carrier: edition/volume/issue/page, manuscript number, or the date and recipient of a letter.

Border cases:
- The **original volume/issue** of a journal, even if later reprinted → `A`.
- Lecture notes written and delivered by the author → `A`. **Student lecture notes** → contested (see T-1).
- Letters: holograph or signed by the author → `A`. In a posthumous edition of correspondence, the letters → `A`, the editor's annotations → `S` (see R4).

**Positive**: `〔A｜原始文献:Leibniz, "Nova methodus pro maximis et minimis", Acta Eruditorum, Oct. 1684, pp. 467–473〕`
**Negative**: `〔A｜原始文献:Boyer 1949, p. 212〕` — Boyer is a 1949 study, two and a half centuries after 1684; not a contemporary text.
**Negative**: `〔A｜原始文献:某百科「Acta Eruditorum」条目〕` — an encyclopedia entry is not the original issue.

**Tool**: partial. The tool can flag grade/source-type inconsistency against a vocabulary (an entry labelled "wikipedia/encyclopedia/textbook" but graded `A`), but cannot decide whether a text is contemporary.

### R2 What grade a translation gets

**Decision**: a translation is **not** a primary source; citing a translation on its own → `S`. If the original edition and original page are also given, the claim may be graded `A`, but the locator must then carry **two locators** (original page + translation page). A single translation page is treated as inconsistent.
In a punctuated and collated edition of a classical text (点校本), the punctuation and collation are editorial work, i.e. `S`; a **facsimile** reproduces the original object, so its text may be used as `A`, but it cannot support codicological judgements about paper, watermark or provenance (see T-3).

**Positive**: `〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II（Motte 1729 英译本, p. 41）〕`
**Negative**: `〔A｜原始文献:牛顿《自然哲学的数学原理》中译本, p. 41〕` — translation page only; the claim cannot be traced back to the original.
**Negative**: `〔A｜原始文献:Heath 英译《阿基米德全集》, p. 91〕` — a twentieth-century translation is `S`, unless the Greek critical-edition page is given alongside.

**Tool**: partial. When the locator contains "译 / trans. / translation" and is graded `A` with only one page locator, the tool emits `warn`.

### R3 Reprints and collected works

**Decision**: first edition, revised edition and reprint are different **witnesses** of one work. Grade `A` requires an "edition–page" pair; mixing pages across editions is an error.
- A scholarly **collected edition** (e.g. Euler, *Opera omnia*) is a compiled text: its text may be `A`, but if the original journal volume and page are known, give those first and the collected-edition page as a supplement.
- A modern **reprint** (Dover, Cambridge) is not new evidence, and the fact that you saw a 1999 reprint does not change the edition statement. The reprint is an access route only (see R11).

**Positive**: `〔A｜原始文献:Euler, Institutiones calculi differentialis, 1755, Pars I, cap. I, p. 12（Opera omnia, Ser. 1, Vol. X, p. 96）〕`
**Negative**: `〔A｜原始文献:Euler, 微分学原理〕` — no edition, no page: not a locator.
**Negative**: `〔A｜原始文献:Euler, Institutiones, 1755, p. 96〕` — the page comes from the reprint but is attributed to the 1755 edition.

**Tool**: partial. A locator with no digits at all triggers `warn` (heuristic: no page, no edition year).

### R4 Why an editor's introduction is not a primary source

**Decision**: introductions, prefaces, editorial notes, headnotes and chronologies are written by later hands. They are `S` even when bound in the same volume as the primary text.
The only exception: a preface **by the author** → `A`, and the locator must say "author's preface" so that it can be told apart from an editor's introduction.
Reason: an introduction is an **interpretation** of the primary text. Its reliability depends on the editor's judgement, which is a different question from whether the original is reliable. Grading an introduction `A` means using one interpretation to vouch for another.

**Positive**: `〔S｜二手研究:Opera omnia, Ser. 1, Vol. X, 编者导言, p. vii〕`
**Negative**: `〔A｜原始文献:同上, 编者导言, p. vii〕` — in the same volume the text is `A` and the introduction is `S`; they cannot be merged.

**Tool**: partial. A locator containing "导言/前言/编者按/introduction/editor's note" graded `A` → `error`, unless the locator also contains "作者自序/author's preface".

### R5 How second-hand quotation is downgraded

**Decision**: if you have seen only a secondary work quoting a primary source, and not the original page, you **must not** grade `A`. Grade `S` and write "转引自 <intermediary> <locator>" (quoted at second hand from …).
- The intermediary is **the work you actually read**.
- If the intermediary is itself `F` (popular science, encyclopedia), the whole item drops to `F` or `U`.
- A chain longer than one step (A quoted by B, and you only saw C quoting B) → `U`, with the note "have seen neither A nor B's original page" (see T-5).

**Positive**: `〔S｜二手研究:转引自 Boyer 1949, p. 212；原文献 Cantor 1894, Bd. III, p. 89（未见原页）〕`
**Negative**: `〔A｜原始文献:Cantor 1894, Bd. III, p. 89〕` — the item is known only through Boyer, yet is graded as if the original had been read.
**Negative**: `〔S｜二手研究:转引自某文献〕` — the intermediary is unnamed and cannot be checked.

**Tool**: automatic (syntax level). A locator containing "转引" graded `A`, or "转引自" with no named object after it → `error`.

### R6 When two secondary works contradict each other

**Decision**:
1. **State both.** Neither may be silently dropped.
2. **Give a reason for the choice**: closer to the primary source; later and directly responding to the earlier; more reproducible method. At least one of the three.
3. **If you cannot decide, say so**: write "the question is unsettled", keep both `S` tags, and add one `U` recording why it is unsettled and what would settle it.
4. "Scholars agree that…" is not allowed as a substitute for evidence: agreement is itself a claim that needs evidence.

**Positive**:
```
Whether Cauchy already commanded epsilon-style arguments: Grabiner (1981, pp. 45–52) says yes; Katz & Katz (2012, §4) partly disagree. This article follows the former, because Grabiner collated the variant readings of the 1821 and 1823 lecture texts line by line.
〔S｜二手研究:Grabiner 1981, pp. 45–52〕〔S｜二手研究:Katz & Katz 2012, §4（相反解读）〕
```
**Negative**: one `S` tag plus "this is the scholarly consensus", with the rival reading omitted.

**Tool**: impossible. The tool cannot tell whether two secondary works contradict each other; it can only check whether one citation key is graded differently in two places (R12).

### R7 How textbooks and popular science are classified

**Decision**: textbook body text, textbook "historical note" sidebars, popular science books, encyclopedia entries, public lectures, blogs and videos are all `F`.
`F` is a lead only: to use it in support of a claim you must also supply the `A` or `S` it points to; if there is none, downgrade to `U`.
One counter-intuitive point: **a mathematically authoritative textbook is still `F` historiographically**. Textbook historical notes usually retell secondary work without locators; their internal consistency is not evidence.

**Positive**: `〔F｜流行说法:某高数教材「历史注记」边栏：柯西消灭了无穷小〕〔S｜二手研究:Grabiner 1981, ch. 2（结论相反）〕`
**Negative**: `〔S｜二手研究:维基百科「Non-standard analysis」条目〕` — an encyclopedia is `F`; grading it `S` inflates it.
**Negative**: `〔A｜原始文献:某微积分教材, p. 233〕`

**Tool**: automatic (vocabulary level). A locator matching the encyclopedia/textbook/popular-science vocabulary while graded `A` or `S` → `error`.

### R8 When "unverified" is allowed to appear

**Decision**: `U` is allowed in exactly three situations —
(a) there is a specific lead (bibliography, holding number, journal issue) but the original has not been obtained;
(b) the original is available but the key pages are missing, damaged or illegible;
(c) only oral tradition, later recollection, or an unattributed retelling exists.

The line between (c) and `F`: grade `F` only when **you have read the popular text and can say which kind it is** (a textbook's "historical note" sidebar, an encyclopedia entry, popular science, a lecture). If you merely do not know who wrote it, and cannot even say which kind of popular text it might be, the grade is `U`, not `F`. `F` presupposes a citable popular text; `U` presupposes the absence of a citable carrier.

`U` must state the **reason** and **where to look next**. Two abuses are forbidden:
- using `U` to avoid judgement: a passage whose every claim is `U` is a passage that should not be published yet;
- `U` with no reason, or with a hollow reason ("to be checked", "unclear", "n/a") — that is not a tag.

**Positive**: `〔U｜未核实:仅见 19 世纪书目著录，未见 1684 年原刊影像；待查 Acta Eruditorum 1684 年卷（Erlangen 大学数字化本）〕`
**Negative**: `〔U｜未核实:待查〕`
**Negative**: `〔U｜未核实:〕`

**Tool**: automatic. `U` with an empty locator, or with one containing only "待查/不详/未知/TODO/n/a" → `error`.

### R9 Marginalia and sidebar material

**Decision**: three kinds, never to be merged:
1. **The author's own notes** (footnotes or marginalia printed in the same edition, the author's preface) → `A`, locator marked "author's note".
2. **Later marginalia** (collector's inscriptions, pencil notes, inserted leaves) → the annotator and the carrier must be named (which copy, which holding, which shelfmark). If the annotator is identifiable and a significant contemporary, grade `A`; if anonymous → `U` (see T-6).
3. **Modern editorial insertions** → `S` (as in R4).

There is a fourth kind that is **not** historical evidence: the present author's own explanatory sidebar. It carries no grade, but it must be explicitly declared in the text with the literal marker "不承担推理" (the linter matches this exact string, and also exempts a paragraph that begins with "旁栏"); otherwise readers will take it for fact.

**Positive**: `〔A｜原始文献:Euler E212, §..., 作者自注〕`
**Positive**: `〔U｜未核实:某藏本边注，批注者佚名，仅见馆藏目录著录（Cambridge, Trinity College, N.4.2）〕`
**Negative**: `〔A｜原始文献:某藏书家铅笔边注〕` — no annotator, no holding, no carrier.

**Tool**: partial. A locator containing "边注/批注/题跋/marginalia" with no holding or identifier → `warn`.

### R10 Citation format for online archives

**Decision**: citing a digitised archival object requires four elements — **site name + persistent identifier + page/plate number + access date**.
Site home pages, search-result pages and shortened links are forbidden: they rot, and they let different scans of different editions collapse into one.
Order of machine-parseability (high to low): `DOI` > `ARK` > `handle` > site permanent link > ordinary URL.

**Positive**: `〔A｜原始文献:L'Hôpital, Analyse des infiniment petits, 1696, p. 3；ARK:ark:/12148/bpt6k205444w（Gallica，访问 2026-11-13）〕`
**Negative**: `〔A｜原始文献:https://gallica.bnf.fr/ 上搜到的 1696 年版〕` — no persistent identifier, no page, no access date.
**Negative**: `〔A｜原始文献:某短链 https://t.cn/xxxx〕`

**Tool**: partial. A URL without scheme or host → `error`; a URL with no access date → `warn`; liveness is probed only under `--online` (see the tool documentation).

### R11 Choosing among several access routes to one source

**Decision**: the locator names **one** primary route, chosen by the R10 priority. Other routes live in the bibliographic ledger (a Zotero item, say), not in the tag.
Two reasons: parallel routes break the "one key, one grade" check (one key carrying three different locators); and the reader needs to know **which copy you actually used**, not which copies exist.

**Positive**: `〔A｜原始文献:Newton, Principia, 1687, Lib. I, Lem. II；URL:https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00056（访问 2026-11-13）〕`
**Negative**: `〔A｜原始文献:Newton, Principia, 1687（archive.org / Gallica / Newton Project 均可查）〕`

**Tool**: partial. Two or more URLs in one locator → `warn`.

### R12 Stability of citation keys

**Decision**: one work must use **one citation key** throughout the document. Suggested forms: `<Author surname> <year>` (`Grabiner 1981`) or `<collected-works number>` (`Euler E212`). Pages may vary per sentence; the key may not.
This is the precondition for the "same source graded differently in two places" check: the tool does not know that "Grabiner 1981" and "Judith Grabiner, *The Origins of Cauchy's Rigorous Calculus*" are the same work unless the author keeps the key stable.

**Positive**: `Grabiner 1981` in both places.
**Negative**: `Grabiner 1981` in one place, `Judith V. Grabiner, The Origins of Cauchy's Rigorous Calculus, MIT Press, 1981` in another, `Grabiner, Origins` in a third.

**Tool**: partial. The tool normalises the locator by stripping page numbers and years and comparing prefixes. Keys written very differently are not matched, so the check under-reports. This is a known limitation of the specification.

### R13 Where the tag goes

**Decision**: the tag goes at the end of **the sentence or paragraph it supports**, adjacent to the full stop (immediately before or after it).
- A paragraph containing claims from several sources must be split into sentences, each tagged.
- One tag at the end of a paragraph is allowed only when the whole paragraph has one source.
- In a table cell, the tag goes at the end of the cell text.
- Headings, code blocks and pure transitional sentences carry no tag.

**Positive**:
```
莱布尼茨 1684 年的论文里，$dx$ 未被定义为无穷小。〔S｜二手研究:Cantor 1894, Bd. III, p. 89〕
```
**Negative**: a paragraph narrating Euler, Cauchy and Weierstrass in turn, ending with a single `〔S｜二手研究:Grabiner 1981〕`.

**Tool**: partial. The tool can detect a paragraph with no tag at all; it cannot check whether a tag sits on the right sentence.

### Clause classes and criticality

R1–R13 are not the same kind of thing. Listing them flatly suggests every clause decides a grade. They fall into three classes:

| Class | What it does | Clauses |
|---|---|---|
| **Decisive** | reads the six dimensions of §1.5 and restricts the set of admissible grades | R1, R2, R3, R4, R5, R7, R8, R9 |
| **Procedural** | says how to write up a conflict; produces no grade itself | R6 |
| **Format** | constrains only locator form and tag placement; never changes a grade | R10, R11, R12, R13 |

Delete a format clause and no row's grade changes. That does not make them deletable: they govern whether the text can be checked at all, which is a different question from which grade it gets — delete R13 and the tool cannot locate the tag; delete R12 and the `MULTI_GRADE` check stops working. **A format clause's criticality is "not applicable", not 0.**

**Criticality** is defined as: on the situation set compressed by §1.5, the number of rows whose judgement changes when the clause is deleted. "Judgement changes" covers two cases: the status changes (unique / underdetermined / conflicting), or it stays unique but with a different grade.

A criticality of 0 has two causes, and they must be written differently rather than lumped into "contributes nothing":

1. **Vacuous (explanatory)**: the clause returns the full set on every row and never takes part in a judgement. Such a clause is explanatory only; it **must not be listed alongside decisive clauses**, and the specification must mark it "explanatory clause only, does not take part in the judgement".
2. **Absorbed**: the clause does restrict some rows, but those restrictions are already implied by other clauses, so deleting it changes nothing. It **is still a decisive clause**, merely redundant under the current rule set; annotate it "absorbed by R<n>" and keep it where it is — change the rule set and it may become decisive again.

Every decisive clause therefore reports two numbers together: **rows touched** (rows where it returns something smaller than the full set) and **criticality**. Only "criticality 0 and rows touched 0" counts as vacuous.

In the current v0.1 none of the decisive clauses is vacuous: the six measured individually all have criticality above 0 (R4 is not measured separately — its case is covered by the punctuated-edition and collation branches of R2/R5). In the v1 baseline R2, R3 and R8 show "criticality 0 but rows touched above 0"; those are absorbed, handled by rule 2, and must not be deleted.

> Per-clause numbers, both calibers (v1 baseline 160 / 86; v0.1 encoding 168 / 90), and the plan for an independent second implementation in Alloy 6.2.0 are in `docs/spec-audit.md`. The numbers move with the rule-set version and are not stable specification text; Alloy is a maintainer tool, not a prerequisite for using this specification.

---

## 3. Quick grading table

| What you have in hand | Grade |
|---|---|
| The author's holograph manuscript or signed letter | `A` |
| The 1684 issue of *Acta Eruditorum* | `A` |
| A twentieth-century English translation of that paper | `S` (unless the original page is given too) |
| The text in a scholarly collected edition, with its page | `A` (plus the original journal page if known) |
| The editor's introduction to that volume | `S` |
| A peer-reviewed monograph's reading of the 1684 paper | `S` |
| The 2011 second edition of the same monograph | `S` (state the edition) |
| You saw only B quoting A, not A's page | `S` + "quoted at second hand" |
| You saw only C (popular) quoting A | `F` or `U` |
| A textbook "historical note" sidebar | `F` |
| Wikipedia / Baidu Baike entry | `F` |
| Public lecture video, blog post | `F` |
| A bibliographic lead, original not obtained | `U` (state reason and next step) |

---

## 4. Conflict handling

### 4.1 One claim carrying two grades

Write **the lower first, the higher second, and say why the higher does not cover everything**:

```
〔S｜二手研究:Grabiner 1981, p. 47〕〔A｜原始文献:Cauchy 1823, p. 12（原文只给出这一句，未给证明）〕
```

Criteria:
- If `A` fully supports the claim, keep only `A` and delete the `S`. If the `S` is doing explanatory work, move it into the prose rather than into the tag.
- If `A` supports only half (the original asserts but does not prove), keep both and say in one sentence which half rests on which.
- `A` together with `F` usually means **a misstatement is being corrected**: `F` first (recording the misstatement), `A` second (the correction). The prose must then contain an explicit "misstatement / correction" structure; tags alone are not enough.
- `U` alongside any grade is always legitimate: `U` records a remaining gap.

### 4.2 One source graded differently in two places

This is an **error**, not "two perspectives". Only two legitimate causes exist: the two citations are to different parts of the same work (body text vs editor's introduction), or one is second-hand and the other is the original page. Both causes must be written into the locator ("editor's introduction", "quoted at second hand") so that the tool can separate them; otherwise the tool reports `MULTI_GRADE` and the text must be fixed.

---

## 5. What the machine can and cannot check

| Can | Cannot |
|---|---|
| Whether the tag syntax is legal (brackets, bar, colon, grade letter) | Whether the cited work really is a primary source |
| Whether DOI / ISBN / URL / archival IDs are well formed | Whether the locator exists at all (offline mode) |
| Whether grade and source type are consistent (encyclopedia graded `A`, introduction graded `A`, second-hand graded `A`) | Whether the author's grading judgement is correct |
| Whether `U` states a reason | Whether that reason holds |
| Whether one citation key is graded differently in two places | Whether two differently written locators are the same work |
| Which paragraphs carry no tag at all | Whether a tag sits on the sentence that the source actually supports |
| (`--online`) whether a link is alive and a DOI resolves | Whether the linked content matches the claim |

In one sentence: **the tool verifies citation parseability and grade consistency; it does not verify historical intent or the grading judgement itself.**

### 5.1 How to report a consistency audit

The rule set will be revised repeatedly, and "did the revision reduce conflicts?" must be answered with a fixed caliber, or the numbers are not comparable. Three rules:

1. **Report the conflict rate, not the number of conflicts.** The denominator moves with the compression of §1.5, so counts are not comparable across versions.
2. **Report after deduplication, in both calibers.** The wide caliber (a dimension counts as live if it has a referent) is the outward-facing one; the narrow caliber (only dimensions the rules actually read) is a conservative lower bound. Different spellings of one situation (the duplicates caused by E2 / E5 / E6) count once.
3. **Report conflicts and underdetermination together.** Zero conflicts with non-zero underdetermination means the rule set cannot produce a grade; that is not "consistency".

Baseline (the arithmetic consequence of §1.5):

| Stage | Wide | Narrow |
|---|---|---|
| Six-dimensional Cartesian product | 1620 | 1620 |
| After eliminating by E1 / E3 / E4 | 376 | 376 |
| After merging by E2 / E5 / E6 | 168 | 90 |

That is the result for the v0.1 encoding (15 carriers, including the undivided punctuated edition): unique 118 / 64, underdetermined 16 / 8 (9.5% / 8.9%), conflicting 34 / 18 (20.2% / 20.0%). It is a **problem list, not a pass mark** — its use is to judge whether a rule change really reduces conflicts.

Since 2026-11-16 the v1 revision proposed by the audit (S-1–S-6) is adopted as the baseline. The following caliber must always be given with the numbers:

- **14 carriers**: per §1.5, a punctuated edition must say body text or collation note; the undivided variant is no longer part of the situation space.
- **Denominator**: v1's Cartesian product is 1512, cut to 356 by E1 / E3 / E4, and deduplicated by E2 / E5 / E6 to **160 (wide) / 86 (narrow)**; the compression against 1512 is about 9.5× (wide) and 17.6× (narrow).
- **Result**: all 160 and all 86 are unique — conflicts 0 / 0, underdetermination 0 / 0 (0% / 0%).
- **Never write "zero conflicts" alone**: without the denominator, both calibers and the two elimination steps, the "0" does not hold — in another space it would not be zero.

These numbers are reproduced by `tools/audit/` (`python -m tools.audit`, see §5 of the internal document), and pinned by `tools/tests/test_audit.py`.

---

## 6. Clauses I am not sure about

The following are marked **contested**. The reason is that I do not have enough grounds to fix them as hard rules. They are not "to be decided later"; they are "this is how it works now, and I know it can be overturned".

**T-1 Are student lecture notes `A` or `S`?**
Leaning `S`: the notes pass through a recorder and often mishear. But if the notes were corrected by the author, or if the author used them as the basis of a lecture course, they should be `A`. I cannot offer an operational criterion, so the question stays open.

**T-2 Is an author's late-life recollection `A` or `S`?**
This is the clause I am least confident about. Memoirs, late letters and retrospective accounts are written by the author, so by the letter of R1 they are `A`; but memory reconstruction, retrospective rationalisation and self-defence push their evidential weight towards `S`.
Current provisional rule: **grade `A` and write "retrospective account" in the locator**, leaving the discount to the reader. I concede that the alternative (always downgrade to `S`) is equally defensible. Note that the first issue of the essay series handles Leibniz's "a light suddenly came on" recollection as `S`, which contradicts this provisional rule. The inconsistency is real and is not hidden.

**T-3 Is a facsimile `A`?**
A facsimile can stand in for the original for **textual collation**, but not for codicological judgements about paper, watermark, binding or provenance. This specification permits `A` for facsimiles within that limit; if your claim is "this is the first edition", a facsimile is not enough.

**T-4 What if only a reprint survives, not the original issue?**
Say a nineteenth-century paper is known only from a 1960s reprint. By R3 it may still be `A` (same content), but the locator must say "from the 19xx reprint; original issue to be checked", otherwise the reader will assume the original was collated. This is in tension with R10's "one primary route" principle; I favour the former (state the access route honestly).

**T-5 Threshold for downgrading a chain of second-hand quotation**
The rule is "one step → `S`, two steps → `U`". Two steps may be too strict: for some canonical works a two-step chain is normal scholarly practice and still fairly reliable. I have no data for a finer threshold, so I take the conservative end.

**T-6 Grade of anonymous marginalia**
See R9. `U` is the conservative choice. But if the annotation is itself independent evidence (it records a conversation, say), perhaps it should be graded by content rather than by author. There is no settled answer.

**T-7 This specification itself**
The four-way `A/S/U/F` split is not a standard in historiography (the field more often uses the primary/secondary dichotomy, or the three dimensions of authenticity, reliability and relevance). The four-way split is a compromise designed for **machine checking**: fewer grades cannot separate "second hand" from "unverified"; more grades cannot be remembered by authors or implemented by tools. If four turns out to be insufficient, the specification should change — not the tool be patched.

---

## 7. Minimal workflow

1. Tag as you write. When in doubt, use `U` rather than nothing.
2. After each section, run `mathlint check section.md`. Clear the `error`s (syntax and consistency) first, then read the `warn`s (missing tags, vague `U`).
3. Before finalising, run `mathlint check . --strict` so that `warn`s fail the build too.
4. Run `--online` when link checking is needed. It distinguishes "link dead" (4xx/5xx) from "network unreachable" (DNS, timeout); the latter is not evidence that the source is bad.
