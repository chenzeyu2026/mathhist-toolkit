# Licensing scope and third-party material

This repository uses two licenses:

| Content | License | File |
|---|---|---|
| Code (`tools/` and related scripts) | Apache License 2.0 | [LICENSE](../LICENSE) |
| Documents and specifications (`spec/`, `docs/`, `prompts/`, READMEs) | CC BY 4.0 | [LICENSE-docs](../LICENSE-docs) |

The sections below explain the remaining directories. **This file does not change the copyright of any third-party material.**

## Directory-by-directory

| Path | Distributed with the public repository? | License / ownership | Basis |
|---|---|---|---|
| `spec/` | Yes | CC BY 4.0 | Specifications, schemas, edge signatures and examples written by the author |
| `docs/` | Yes | CC BY 4.0 | Method notes, walkthroughs and repository guide written by the author |
| `prompts/` | Yes | CC BY 4.0 | P1–P9 prompts written by the author |
| `tools/` | Yes | Apache-2.0 | Checkers, generator and tests written by the author |
| `corpus/` | Yes | CC BY 4.0 | **Acceptance articles written by the author** (original and minimally patched); not an anthology of collected texts |
| `reports/` | Yes | CC BY 4.0 | The author's own baseline/patch reports, release self-checks, literature-gap notes and delivery requests; see below |
| `research/` | Yes | CC BY 4.0 | The author's own ontology-mapping and tooling evaluations |
| `spec/framework/samples/`, `pilots/` | Yes | CC BY 4.0 | Example bundles and pilots written by the author; historical claims keep only bibliographic data and short quotations |
| `literature/` | **No** | Third-party copyright, not licensed | Downloaded reference PDFs for local checking only; not distributed |
| `reports/literature/` | **No** | Third-party copyright, not licensed | Same as above; also excluded from the public repository's git history |

## The `corpus/` decision

`corpus/` contains the author's own acceptance article on the origins of calculus and its `.patched.md` version. Quotations in the article are short and attributed; quotation does not change the copyright of the cited works. The article itself is offered by the author under CC BY 4.0.

If a full text, scan or long transcription of someone else's work is later added to `corpus/`, that file **is no longer covered** by this statement and must be separately licensed or removed.

## The `reports/` decision

The public copy keeps only the author's own process records:

- `baseline.json` / `patched.json` and the corresponding `*-human.txt`: check results for the author's own corpus;
- `patch-diff.txt`: edits to the author's own manuscript;
- `release-selfcheck-*.md`, `literature-gaps-*.md`, `free-fulltext-*.md`, `channel-access-test-*.md`, `ahes-ill-batch-*.md`, `ill-*-request-*.md`: workflow records and bibliographic data; personal-information fields in request forms are blank templates;
- **no** third-party PDFs, scans, database full texts or long transcriptions.

The following files **are not included** in the public repository:

- `reports/literature/*.pdf` (7 files, about 10.86 MB): at least 3 are subscription-journal or publisher typeset versions, and the redistribution terms of the remaining arXiv versions have not been checked one by one;
- `reports/ill-*.docx`: binary forms that duplicate the `.md` content; the public copy keeps the Markdown version;
- any `*.pdf`, `*.docx` or temporary files (enforced by `.gitignore`).

## Copyright of third-party material

- Author names, book titles, journal titles, DOIs and page numbers in this repository are **bibliographic facts** and are not affected by the repository licenses.
- Short quotations from others' works in bundles and documents remain under the original copyright; quotation is not a sublicense.
- `LICENSE` and `LICENSE-docs` cover only what the author has the right to license, not any third-party text, image or database content.

## If you want to reuse this material

- Code: follow Apache-2.0 (keep the copyright and license notices).
- Specifications and documents: follow CC BY 4.0 (attribute the source and license).
- Third-party literature: obtain permission from the rights holder directly; do not redistribute it from this repository.
