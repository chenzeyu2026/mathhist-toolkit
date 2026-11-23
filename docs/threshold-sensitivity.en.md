# `MISSING_TAG` threshold sensitivity (v0.1.0 record)

> Purpose: a reproducible sensitivity check on the heuristic behind "claim without a tag".
> Conclusion up front: **the current values (40 characters for a paragraph, 24 for a list item) sit mid-slope, not at a natural breakpoint. Nothing here justifies changing them; nothing here disproves them either.**

## 1. How the check decides

`MISSING_TAG` fires on a "unit" (a paragraph or a list item) only when all three hold:

1. the unit does not contain `不承担推理` and does not start with `旁栏`;
2. it contains at least one sentence-final mark `。！？`;
3. it contains at least *N* CJK characters plus Latin letters.

*N* is hard-coded in `_looks_like_claim()` in [`tools/mathlint/checks.py`](../tools/mathlint/checks.py): 40 for a paragraph, 24 for a list item (about 0.6 of the paragraph value).

## 2. How the sweep was run

One corpus: `corpus/01-微积分起源.md` (41,070 characters) and its patched version `corpus/01-微积分起源.patched.md` (43,669 characters). The paragraph threshold sweeps 20→80; the list-item threshold is fixed at 0.6× the paragraph value; every other condition is unchanged. Script in §5.

"Judged a claim" = units passing all three conditions. "Untagged" = of those, units with no tag on any of their lines — i.e. the `MISSING_TAG` count.

## 3. Results

| Paragraph threshold | List-item threshold | Original: judged claims | Original: untagged | Patched: judged claims | Patched: untagged |
|---:|---:|---:|---:|---:|---:|
| 20 | 12 | 277 | 277 | 277 | 211 |
| 25 | 15 | 272 | 272 | 272 | 206 |
| 30 | 18 | 265 | 265 | 265 | 199 |
| 35 | 21 | 256 | 256 | 256 | 190 |
| **40** | **24** | **242** | **242** | **244** | **178** |
| 45 | 27 | 228 | 228 | 233 | 167 |
| 50 | 30 | 209 | 209 | 214 | 149 |
| 60 | 36 | 179 | 179 | 185 | 121 |
| 80 | 48 | 123 | 123 | 131 | 72 |

The original has no tags at all, so "judged claims" and "untagged" coincide there — the two columns must be identical. At 40 the patched column reads 178, matching the `MISSING_TAG 178` the linter actually reports: the counting here and the implementation are the same.

## 4. Reading the table

- **No plateau.** From 20 to 80 the counts fall smoothly; there is no band where nudging the threshold leaves the count unchanged. Character count and "is this a claim" have no natural cliff in this corpus, so the threshold can only ever be a convention.
- **Local slope.** Near 40, +5 characters removes 8–14 units (about 3–6%); −5 adds 5–9. A user would notice a five-character change.
- **Where 40 sits.** It cuts 277 down to 242, discarding about 13%. At 30 it keeps almost everything (265), including more transitional sentences; at 50 it would miss 33 shorter claims. **40 is a compromise between "report too much" and "don't be noisy", not an optimum.**
- **The patched text runs slightly higher.** At the same threshold it yields 2–8 more claims than the original, because inserting tags changes unit lengths. That boundary wobble cannot be removed, only accepted.

## 5. Reproduce

```python
# Run from anywhere; point ROOT at the repository.
import re, sys
sys.path.insert(0, r"<repo>\tools")
from mathlint import checks

def count(text, para_th):
    item_th = round(para_th * 0.6)
    tags, _ = checks.scan(checks.mask_non_prose(text))
    tagged = {t.line for t in tags}
    claims = untagged = 0
    for start, end, unit, is_item in checks.iter_units(text):
        if not unit or "不承担推理" in unit or unit.startswith("旁栏"):
            continue
        if not re.search(r"[。！？]", unit):
            continue
        if checks._cjk_letters(unit) < (item_th if is_item else para_th):
            continue
        claims += 1
        if not any(line in tagged for line in range(start, end + 1)):
            untagged += 1
    return claims, untagged

text = open(r"<repo>\corpus\01-微积分起源.md", encoding="utf-8").read()
for th in (20, 30, 40, 50, 60, 80):
    print(th, count(text, th))
```

## 6. What was not done

- **No second corpus.** One author, one topic, one register (continuous exposition for first-year undergraduates). A review essay, a terminological study or a chronology could have a completely different slope.
- **No human labels.** There is no gold set saying "of these 242 units, a person considers *k* to be claims", so accuracy and recall cannot be computed — only counts can be compared.
- **No default change.** Until a second corpus and a labelled sample exist, 40/24 stays.

Real calibration needs a small annotation run: sample 100 units, have two people independently mark claim / not-claim, then compute F1 across thresholds. That task is on [`RELEASE-CHECKLIST.md`](../RELEASE-CHECKLIST.md) and must be finished before a public release.
