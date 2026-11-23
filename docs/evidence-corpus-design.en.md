# Evidence corpus: design draft

> **Status: v0.2 proposal, not implemented.** Design only — no code, no schedule.
> The v0.1 linter does not understand `corpus/` locators; every check below is future work.
> 状态：v0.2 提案，未实现。只有设计，没有代码，也没有时间表。

## 0. The problem, and a different answer

The original idea was: "build one unified collection of primary texts, so that material scattered across libraries sits in one place." The direction is right; the shape has to change.

A collection of full texts solves none of three problems:

1. **Copyright.** Twentieth-century critical editions, translations and archival images mostly cannot be published in full.
2. **Pointing.** Handing a reader the whole volume of *Acta Eruditorum* still does not tell them which passage your sentence rests on.
3. **Reproducibility.** Re-scan, re-crop, re-OCR, and the page numbers no longer line up; nobody can tell whether they are looking at the same page you read.

So: an **evidence corpus**. Do not collect texts; collect **index data and verification data**. One entry per document, recording which physical object I read, where it came from, how big it is, what its hash is, which scan image carries page 12, and whether it may be published. The bytes stay local.

One sentence: **the corpus turns "I think I saw it somewhere" into "this page's byte fingerprint is X — go check it yourself."**

## 1. Directory layout

```
corpus/
  leibniz-1684-nova-methodus/
    source/                     # local copy, not committed by default
      scan-01.png
      scan-02.png
      ocr.txt                   # optional; record engine and date
    manifest.yaml
    notes.md                    # why I read it, what I noticed
  newton-1687-principia-1st/
    ...
```

- `source/`: the scan, or a **lawful mirror** of it, kept locally. Filenames carry no meaning; the page relationship lives in the manifest.
- `manifest.yaml`: the only machine-readable entry point; fields in §2.
- `notes.md`: human notes. This is the right place for material observations such as "water stain on p. 3, second paragraph has missing characters" — there is nowhere else to put them.

At the repository root, `corpus/README.md` states the rules; `corpus/index.yaml` may list every id with a one-line summary for human browsing.

## 2. manifest.yaml fields

```yaml
id: leibniz-1684-nova-methodus
title: "Nova methodus pro maximis et minimis"
creator: "Gottfried Wilhelm Leibniz"
date: "1684-10"                 # month if known, year otherwise
kind: periodical-article        # periodical-article | book | manuscript |
                                # correspondence | lecture-notes | archive-item
language: la

provenance:
  is_contemporary_publication: true    # published in the author's lifetime, by the author
  is_scholarly_edition: false          # a later editor's edition (collected works, critical edition)
  editor: null                         # required when is_scholarly_edition: true
  edition_statement: "Acta Eruditorum, Oct. 1684, pp. 467-473"
  translation: null                    # if a translation: translator, language, edition
  witness_note: "original printing; no editorial introduction"

source:
  url: "https://www.digitale-sammlungen.de/..."   # one or more; the first is primary
  retrieved: "2026-11-02"
  sha256: "3f9c...e1"                # manifest hash over all files in source/, in name order
  bytes: 18432011
  page_count: 7                      # number of scan images
  page_map:                          # scan image -> printed page
    - {scan: 1, printed: "467"}
    - {scan: 2, printed: "468"}
    # unnumbered items (manuscripts, letters): use folio or "n.p." and explain in notes.md
  page_map_gaps: "p. 471 right half missing"   # optional, record gaps honestly

license:
  status: public-domain              # public-domain | cc-by | cc-by-sa |
                                     # permission-granted | unknown | local-only
  basis: "published 1684; author dead more than 70 years"
  public_copy_allowed: true          # may source/ go into a public repository?
  note: ""

rights_note: "digitisation by the Bavarian State Library; their terms apply separately"
```

Rules:

- `id`: lowercase, hyphenated, `author-year-shorttitle`. Once cited, never changed. Renaming means a new id and breaks every existing citation.
- `provenance` answers four questions that must not be left blank: **is it a contemporary publication, is it a later editor's edition, who edited it, what is this object materially.** These four are the mechanical handle against treating second-hand material as primary (§7).
- `sha256` is a **manifest hash**: sort files by name, hash each, concatenate, hash the result. Swapping any scan changes it.
- `page_map` is the reason the corpus exists. Without it, `#p12` cannot be resolved.

## 3. Citation syntax

```
〔A｜原始文献:corpus/leibniz-1684-nova-methodus#p467〕
〔S｜二手研究:corpus/grabiner-1981#p45〕
〔A｜原始文献:corpus/newton-1687-principia-1st#p12-14〕
```

- `#p<n>` means the **printed page**, not the scan index. Printed page numbers are the only coordinate that stays stable across copies; the reader may hold a different facsimile.
- For unnumbered items use `#s<n>` (scan), `#f<n>` (folio) or `#n<n>` (paragraph), one of the three, declared in `page_map`.
- Ranges: `#p12-14`. A single plate: `#f3r`.

### Coexisting with external URL / DOI locators

All three forms are legal and mean different things:

| Form | What it asserts | What the reader does |
|---|---|---|
| `corpus/<id>#p12` | I read this page; its bytes can be checked | ask the author for a copy, or fetch `source.url` from the manifest |
| `doi:10.xxxx/...` | a stable public entry point | follow the DOI |
| `https://...` | an entry point that may rot | follow the link |

**Precedence**: `corpus/` outranks external locators, because it is the only form that verifies "I read the same page you are reading". But the corpus does **not** change the grade — **being in the corpus is not an upgrade to `A`**. The grade is decided by the rules in the spec; the corpus only guarantees resolvability.

The two may be written together. The v0.2 plan is to parse only the first `corpus/` prefix (v0.1 parses no `corpus/` locator at all; see the status note at the top):

```
〔A｜原始文献:corpus/leibniz-1684-nova-methodus#p467（doi:10.xxxx/xxxx）〕
```

A private copy plus a public entry point is the most durable form: when the public entry rots, the corpus id still names a verifiable hash.

## 4. New checks for `mathlint`

| Code | Severity | Condition |
|---|---|---|
| `CORPUS_UNKNOWN_ID` | error | locator contains `corpus/<id>` but `corpus/<id>/manifest.yaml` does not exist |
| `CORPUS_PAGE_OUT_OF_RANGE` | error | `#p467` not found in `page_map.printed` and not inside a declared gap |
| `CORPUS_HASH_MISMATCH` | error | `source/` exists and its manifest hash ≠ `sha256` |
| `CORPUS_MISSING_FILE` | error | manifest says `page_count: 7`, `source/` contains 5 files |
| `CORPUS_LICENSE_LEAK` | error | manifest has `public_copy_allowed: false` but the document is marked public |
| `CORPUS_MANIFEST_FIELD_MISSING` | warn | any of the four provenance answers is blank, or `page_map` is empty |
| `CORPUS_PAGE_MAP_GAP` | warn | the citation falls on a page `page_map` does not cover |
| `CORPUS_GRADE_DOUBT` | warn | tagged `A` but the entry has `is_contemporary_publication: false` |
| `CORPUS_GRADE_DOUBT_STRONG` | error | tagged `A` but the entry has `is_scholarly_edition: true`, and `witness_note` does not say the cited part reproduces the original |
| `CORPUS_UNUSED` | info | entry exists but nothing cites it |

Notes:

- **How "public" is decided**: a repository-level `.mathlint.yaml` with `visibility: public | private`, defaulting to `private`, overridable per file via front-matter. This is a heuristic, not a security boundary. Preventing leaks still depends on a human check before commit; the tool only stops careless mistakes.
- **Hash checks run only when `source/` exists locally.** A public repository has no `source/`; the check is skipped with an `info`, not an error.
- Under `--offline` everything above still runs (the manifest hash needs local files; the rest is pure YAML). Under `--online`, `source.url` is also probed, reusing the existing `LINK_DEAD` / `NETWORK_UNREACHABLE` distinction.
- None of these checks judge whether the grade is *right*. `CORPUS_GRADE_DOUBT` only says "you call it contemporary, the manifest says otherwise". The verdict stays with a person.

## 5. Boundary: what the corpus does and does not do

**It does:**

- Make citations resolvable: `#p467` has a definite referent, not "somewhere".
- Make them reproducible: identical hashes mean the same image; changing the source shows up immediately.
- Make them transferable: whoever inherits the draft can find the same page from the manifest.
- Make them auditable: a machine can list every citation pointing at a later editor's edition.

**It does not:**

- **Decide whether something is a primary source.** Whether it counts as `A` depends on whether it is a contemporary publication, a manuscript, a letter, or a later critical edition. That is a historical judgement. The manifest records your claim; it cannot make it for you.
- **Decide what the author meant.** Context, irony, period senses of a term — no index helps.
- **Prove you read it.** A hash proves the file is unchanged, not that you understood it.
- **Replace bibliography.** Different editions of the same work differ; the manifest can only record which one you read.

The user-facing text must state this, matching the spec §5:

> The tool verifies that citations resolve and that grades are internally consistent; it does not verify historical intent or the grade judgement itself.

## 6. Copyright boundary

**A public repository contains**: `manifest.yaml`, `notes.md`, `corpus/README.md`, and the citation rules. **No bytes of `source/` at all.**

The following must not go into a public repository, even when it is technically possible:

1. **Critical editions, translations, scholarly editions still in copyright.** The author's text may be out of copyright while the editor's introduction, notes, punctuation and translation are not.
2. **Images whose holding institution asserts rights.** Terms for digitised manuscripts are often independent of the work's copyright and must be checked item by item.
3. **Items whose licence status is `unknown`.** Excluded by default until resolved.
4. **Copies supplied by someone else.** A scan handed to you privately carries no right to redistribute.
5. **Modern correspondence and unpublished notes containing personal data**, concerning living people or their immediate families.

**Open question (T-8)**: for faithful photographic reproductions of two-dimensional public-domain works, US practice (*Bridgeman v. Corel*) leans towards no new originality, while some European jurisdictions and database rights claim otherwise, and Chinese law is contested. The conservative rule here: **if the digitising provider asserts terms of use, treat the item as `local-only`** and do not bet on a legal reading. I hold this tentatively, for the reason just given.

`source/` is never committed: `.gitignore` plus a pre-commit check, two locks. Add `corpus/*/source/` to `.gitignore`. If an item genuinely may be published (say, your own scan of the 1684 printing), set `public_copy_allowed: true` with its basis in the manifest **and** place that entry in a separate `corpus-public/` directory, physically apart from the private corpus, so that one `git add -A` cannot leak the rest.

## 7. Risk: a corpus decays into quasi-secondary material

This is the largest risk in the design and has to be stated plainly.

**Mechanism**: once a tidy "evidence corpus" exists, writers will cite it instead of the document it points to. Three rounds later `corpus/xxx` is the new "everyone cites it this way" secondary source — it looks more reliable than Wikipedia because it has hashes, yet **a hash proves the file did not change, not that the file is the original**.

**Four defences**:

1. **The manifest must declare its own status.** `is_contemporary_publication`, `is_scholarly_edition`, `editor` and `witness_note` are mandatory. An `A` citation pointing at an entry with `is_scholarly_edition: true` is an error (`CORPUS_GRADE_DOUBT_STRONG`).
2. **Citations must land on a page, not on an entry.** A locator of `corpus/<id>` with no `#p…` raises `CORPUS_NO_PAGE`, a sibling of `CORPUS_PAGE_OUT_OF_RANGE` (severity not yet assigned). Landing on an entry says "I cited this book"; landing on a page says "I cited this sentence".
3. **No intra-corpus citation.** `notes.md` may reference other entries, but that is not evidence; body tags may point only at a manifest, never at another entry's `notes.md`. This is manual today; the linter can at least flag locators containing `notes.md`.
4. **Periodic stripping.** When a draft is done, temporarily replace each corpus id with the manifest's `edition_statement` and read it again. If the sentence stops making sense, what you relied on was the existence of the item in the corpus, not the content of the page.

A subtler decay: **treating an anthology as the complete works**, citing a piece in a *Source Book in the History of Mathematics* as the author's own text. The only defence is a `witness_note` that says "reprint in an anthology; the original printing was not seen", plus downgrading such an entry to `S` or annotating it when cited at `A`.

## 8. Open questions

- **T-9**: id stability. If the author's name is corrected, the year revised, or an earlier version found, may the same id change its `source`? The draft leans towards "yes, but any change of `sha256` must be dated in `notes.md`", because changing the id breaks every old draft.
- **T-10**: page numbers in multi-volume works. `#p12` is meaningless inside the Leibniz *Sämtliche Schriften*; it needs `#v3-p12`. The draft proposes "multi-volume works always use `#v<vol>-p<page>`", which is inconsistent with the single-volume form; whether to unify is undecided.
- **T-11**: does OCR text count as a copy? The draft leans towards: `ocr.txt` is a search aid only, never a basis for citation; citations must return to the scan.
- **T-12**: how to express "different editions of the same work" between entries (`same_work_as:`). Not designed; leave empty if v0.2 happens.

## 9. If this is built (minimum v0.2 path)

1. A JSON Schema for the manifest plus `mathlint corpus verify <dir>`, checking only hashes and page mapping.
2. Then parse `corpus/` locators, wired into the existing `citations.py`.
3. Only then the cross-file judgements such as `CORPUS_GRADE_DOUBT`.
4. Never implement downloading: acquisition and compliance stay with the human; the tool only verifies copies that already exist.

Item 4 is a hard constraint. The moment the tool starts fetching files, responsibility for copyright slides from "the user judged" to "the tool defaulted".
