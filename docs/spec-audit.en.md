# Specification consistency audit (internal document)

> Status: **internal maintenance document, not part of the published specification.** The published specification is `spec/evidence-tags.en.md`; this file carries the numbers that move with the rule-set version, and the maintainer-tool plan.
> Audience: whoever maintains the rule set. Writers do not need this document.
> Snapshot: 2026-11-16, against specification v0.1.

---

## 0. Why these parts are not in the specification

`spec/evidence-tags.en.md` gained three sections: §1.5 (situational validity), the clause-class and criticality section at the end of §2, and §5.1 (reporting caliber). All three stayed in the body. Three things were moved out:

1. **The per-clause number table** — it drifts with the rule-set version and carries no information for a writer;
2. **The Alloy 6.2.0 second-implementation plan** — a maintainer tool; putting it in the specification would suggest that using this zero-dependency toolkit requires installing Alloy;
3. **The reproduction method and its gap** — an engineering matter.

The dividing line: the specification answers "how do I tag this", this document answers "does the rule set still hold up". Different readers.

---

## 1. The finite domain and its correspondence to §1.5

§1.5 defines six dimensions. Expand them into a Cartesian product and compress by E1–E6:

| Stage | Combinations | Note |
|---|---|---|
| Six-dimensional Cartesian product | 1620 | 15 carriers × 3 locator states × 3 depths × 2 original-page states × 2 intermediary states × 3 blockage states |
| Eliminated by E1 | −1008 | a non-secondary carrier carrying a non-zero quotation depth |
| Eliminated by E3 | −168 | a non-secondary carrier claiming "lead but original not seen" |
| Eliminated by E4 | −68 | blockage "page missing" with "edition + page complete" |
| Remaining | 376 | every situation is possible |
| Merged by E2 / E5 / E6 | 168 (wide) / 90 (narrow) | wide: a dimension counts as live if it has a referent; narrow: only dimensions the rules read |

The fifth carrier value, "punctuated edition (undivided)", is an artefact of the v0 encoding: R2 grades a punctuated edition `S` while R3 allows its body text `A`, so leaving it undivided makes two clauses give opposite verdicts on one carrier. §1.5 now requires the writer to say body or collation notes; once said, there are 14 carriers. The audit keeps 15 so that the ambiguity stays visible instead of being papered over.

Note: 168 / 90 are an **upper bound**. The original page of a same-format facsimile is semantically just as redundant as that of the original issue, but the audit only treated the original issue as having no referent on that dimension and did not merge the facsimile, so the true figure is slightly lower (not measured). E6 of §1.5 states this caliber.

The v1 baseline (adopted 2026-11-16) removes the undivided punctuated edition from the carrier table (§1.5 already requires body or collation note), giving 1512 → 356 → **160 (wide) / 86 (narrow)**. The 168 / 90 figures are kept as the v0.1 encoding's comparison values and are no longer the outward baseline.

---

## 2. Per-clause criticality

The caliber is defined at the end of §2. Measured values: the v0.1 encoding's space is 168 (wide) / 90 (narrow); the adopted v1 baseline is 160 (wide) / 86 (narrow).

**Current v0.1 clauses** (168: unique 118 / underdetermined 16 / conflicting 34; 90: unique 64 / underdetermined 8 / conflicting 18)

| Clause | Criticality (wide) | Rows touched (wide) | Criticality (narrow) | Rows touched (narrow) |
|---|---|---|---|---|
| R1 / R9 | 24 | 36 | 12 | 20 |
| R2 | 9 | 40 | 5 | 24 |
| R3 | 16 | 28 | 8 | 16 |
| R5 | 61 | 92 | 31 | 50 |
| R8 | 27 | 109 | 14 | 59 |
| R7 | 19 | 168 | 10 | 90 |

v0.1 has no vacuous clause: all six have criticality above 0. R5 dominates (61 of 92 wide rows change because of it); the conflicts come mostly from its overlap with R2/R3 on translations and punctuated editions.

**The adopted v1 baseline** (160: all unique; 86: all unique)

| Clause | Criticality (wide) | Rows touched (wide) | Criticality (narrow) | Rows touched (narrow) |
|---|---|---|---|---|
| R1 / R9 | 12 | 60 | 6 | 32 |
| R2 | 0 | 32 | 0 | 20 |
| R3 | 0 | 20 | 0 | 12 |
| R5 | 50 | 116 | 25 | 62 |
| R8 | 0 | 58 | 0 | 32 |
| S-6 (placeholder → `U`) | 2 | 35 | 1 | 19 |
| R7 | 6 | 160 | 3 | 86 |

In v1, R2, R3 and R8 are **absorbed**, not vacuous: they still touch 32 / 20 / 58 rows, but R5 already implies their restrictions. Under §2 rule 2 they should be **kept and annotated "absorbed by R5"**, not deleted — shrink R5 and they become decisive again immediately.

> Naming note: the kernel labels that clause `R6/S-6`, but its content is S-6 (a placeholder locator is graded `U`), which is not the specification's R6 (conflict handling, procedural class). It is recorded here as S-6.

---

## 3. Convergence

| Version | Carriers | Cartesian → after elimination | Wide | Narrow | Conflicting | Underdetermined |
|---|---|---|---|---|---|---|
| v0.1 encoding (kept for comparison) | 15 | 1620 → 376 | 168 | 90 | 34 / 18 (20.2% / 20.0%) | 16 / 8 (9.5% / 8.9%) |
| **v1 baseline (adopted 2026-11-16)** | 14 | 1512 → 356 | **160** | **86** | 0 / 0 (0%) | 0 / 0 (0%) |

Report rates, not counts; give both calibers; report conflicts and underdetermination together. Same reasoning as §5.1 of the specification.

**160 and 86 are the current baseline and may be cited externally**, provided four things are given at the same time: both calibers, the 14 carriers (the undivided punctuated edition is excluded), the two elimination steps 1512 → 356, and the denominators themselves (160 / 86). "Zero conflicts" on its own, with no denominator, is still not citable — the number is fine; what is missing is the space it holds in.

The v0.1 figures 168 / 90 stay in the first row to answer "how much did v1 change": conflict rate 20.2% → 0% wide, 20.0% → 0% narrow.

The clause wording in the published specification (R2 on translations, R3 on punctuated editions, R8's `U` situations) still differs from S-1–S-6; it will be synchronised in the next revision. Until then, clauses follow the v1 table in §2 and numbers follow this table.

The Alloy second implementation in §4 has not been run. Cite these figures as "what this implementation computes on the v1 baseline", not as "the rule set has been independently verified".

---

## 4. Alloy 6.2.0: an independent second implementation

### Purpose

Rewrite the same rules through a different mechanism, in order to expose **encoding errors** — not to validate historical judgement.

There is concrete grounds for this. The first Python kernel contained `s = ALL` followed by `s &= {...}`, which mutated the global set in place and made a whole batch of results spuriously conflict. A mistake of that kind is invisible no matter how many times you read the prose specification, and a different representation (relational constraints plus automatic counterexample enumeration) surfaces it at once. The same risk applies to the translation step itself: nobody has independently checked the mapping from R1–R13 into the kernel.

### Trigger

**Run it only when "zero conflicts" is about to go into an outward-facing document as evidence.** Otherwise it does not run; not in CI, not in the published specification, not as a runtime dependency.

Concretely, any of the following triggers it:

- "the rule set has no conflicts" is to appear in the README, release notes, an external report or a paper;
- the rule set changes structurally (a new dimension, a deleted clause, a change of clause class);
- someone disputes a conflict conclusion and the Python implementation cannot prove it is not an encoding error.

### Method and limits

- Write the six dimensions as `sig`s, the grade as a single-valued relation, each decisive clause as a `pred`, and E1–E6 as `fact`s. Every `fact` is explicit: Alloy does not know that "the carrier determines which dimensions are meaningful", so all six clauses of §1.5 must be translated one by one, or half the counterexamples it enumerates will be E1–E6 violations.
- `run` for "a situation satisfying all preds whose grade set is empty" — a solution *is* a conflict, and the instance is a human-readable counterexample.
- Scale: 5–10 lines per clause, about 60 lines for the six decisive kernels. Alloy 6.2.0 needs a JVM, which is the practical reason it cannot go into CI and the reason it cannot go into the specification body.
- **Limit**: Alloy can only show that *this encoding* of the rules is self-consistent; it cannot show that R1–R13 match historiographical practice. Agreement between two implementations rules out translation errors, not errors in the specification itself.

### What is deliberately not done

- Alloy is not added to `tools/` dependencies and `pyproject.toml` is unchanged;
- Alloy does not appear in the README quick-start path;
- the Alloy version is not forced into line-by-line isomorphism with the Python version — different idioms are fine, provided both produce the same verdict row by row on the same situation set.

---

## 5. How to reproduce

The kernel (`grading_kernel.py`), the domain audit (`audit_domain.py`) and the criticality calculation (`criticality.py`) now live in [`tools/audit/`](../tools/audit), zero-dependency and shipped with the repository — no longer temporary files outside the workspace.

Run either form:

```bash
py -3.11 -m tools.audit              # from the repo root: all three sections
py -3.11 -m audit criticality        # with cwd = tools/: one section
```

Besides `all`, the sections are `kernel` / `domain` / `criticality`. What each prints:

- **`kernel`**: the raw valid-configuration count, conflict count and underdetermination count for v0 and v1, grouped by "which clauses speak at once", each group showing every clause's allowed set.
- **`domain`**: how the six-dimensional product is cut down by C1/P1/P2 (i.e. E1/E3/E4 of §1.5) — v0: 1620 → 376, v1: 1512 → 356; deduplicated situation counts under both calibers — v0: 168 / 90, v1: 160 / 86; the unique/underdetermined/conflicting recount on the deduplicated space; vacuity and criticality summary; the S-12 sensitivity test; the judgement-signature distribution.
- **`criticality`**: one table per caliber, giving for each clause "how many situations change their verdict when the clause is deleted" (v1 wide: R1/R9 12, R5 50, S-6 2, R7 6; R2/R3/R8 are 0).

Output is plain text on stdout only: no files written, no network, no third-party packages. The baseline numbers are pinned by `tools/tests/test_audit.py` (v0's 168/90/34/16 and v1's 160/86/0/0, 14 carriers), so this document cannot drift away from what the scripts actually print.

Steps (matching the sections of `domain`):

1. expand the six-dimensional Cartesian product → 1620; v1 drops the undivided punctuated edition, giving 1512;
2. eliminate by C1/P1/P2 → 376 (v1: 356);
3. deduplicate by E2/E5/E6 → 168 / 90 for v0, 160 / 86 for v1;
4. intersect the allowed sets of all clauses per situation: empty → conflict, multi-valued → underdetermined, single → unique;
5. delete each clause in turn and recount the rows whose judgement changes → criticality.
