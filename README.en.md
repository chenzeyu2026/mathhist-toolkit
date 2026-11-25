# mathhist-toolkit

> First public release: 2026-11-23 · initial commit [`eaae8c8`](https://github.com/chenzeyu2026/mathhist-toolkit/commit/eaae8c823e093f9d92023e7be01f423352bb500d) · DOI [10.5281/zenodo.24455228](https://doi.org/10.5281/zenodo.24455228) · [priority and citation](PRIORITY.md)

Two layers for writing the history of mathematics: **an evidence-tagging specification with a linter**, and **a graph-structured ontology with a validator**.

- Document level (v0.1, usable): tag claims with `A / S / U / F`; `mathlint` checks tag syntax and whether grade and source type agree.
- Graph level (v0.2, structure frozen, content still being filled): write concepts, theorems, problems, texts, people and events as `{nodes, edges}`; `graphlint` checks 31 edge types, 7 invariants and node completeness.

> 中文版：[README.md](README.md)

## What problem it solves

Two kinds of information are hardest to check in history-of-mathematics writing:

1. **What backs a sentence** — is “Leibniz published the calculus in 1684” based on the original print, a later study, or a textbook retelling? `mathlint` turns this into parseable tags and reports contradictions between grade and source type.
2. **How one thing connects to another** — which branch does a concept belong to, who proved it, which text supports it, do two accounts conflict? `object-model` writes relations as edges carrying time, source, grade and confidence; `graphlint` checks endpoint types, direction, weights, cycles and conditionally required fields.

Both layers share the same `A / S / U / F` scale, so they can reference each other, but they answer different questions.

## Ten-minute start

Requires **Python 3.11 or newer** (tested locally with 3.13.14).

- `mathlint`: standard library only, **no third-party dependencies**, no installation needed.
- `graphlint`: requires **PyYAML ≥ 6.0** (`py -3 -m pip install "PyYAML>=6.0"`).

```bash
cd mathhist-toolkit/tools

# 1) Document level: 3 examples, all 0 error / 0 warn / 0 info, exit 0
py -3 -m mathlint check ../prompts/examples

# 2) Graph level: 10 bundles, 0 errors / 60 warnings; the 60 warnings are pre-existing missing node fields
py -3 -m graphlint check-all

# 3) Generated artifacts in sync: exit 0
py -3 -m graphlint generate --check
```

On Windows, if `py -3` is unavailable, use `python` (3.11+). If `python` opens the Microsoft Store alias, install Python and keep using `py -3`.

A failing example:

```bash
# 13 errors / 1 warning, exit 1
py -3 -m mathlint check tests/fixtures/invalid.md
```

For `graphlint` failure output, see [docs/repository-guide.en.md](docs/repository-guide.en.md) section 4.2 (Chinese: [docs/repository-guide.md](docs/repository-guide.md)): violations are grouped by `== error（N）==` / `== warning（N）==`, each with file, edge/node ID, actual value, expected value and a readable explanation.

Optional install (from the repository root; requires network for build dependencies):

```bash
pip install -e tools
mathlint check prompts/examples
graphlint check-all
```

Without installing, `py -3 -m mathlint` / `py -3 -m graphlint` are equivalent to the installed commands.

## Repository layout

| Path | What it is | Status |
|---|---|---|
| [`spec/evidence-tags.md`](spec/evidence-tags.md) / [`.en.md`](spec/evidence-tags.en.md) | Evidence-tag specification: syntax, rules, conflicts, open clauses | Formal spec |
| [`spec/object-model.md`](spec/object-model.md) | Graph ontology: 14 node types, 31 edge types, constraints, storage | Formal spec |
| [`spec/framework/edge-signatures.yaml`](spec/framework/edge-signatures.yaml) | **Single source** for 31 edge signatures, 7 invariants and glosses | Formal, machine-readable |
| [`spec/framework/graph.schema.json`](spec/framework/graph.schema.json) | Bundle schema; edge enum and conditional rules generated from the YAML | Generated, do not hand-edit |
| [`spec/framework/object-model.schema.json`](spec/framework/object-model.schema.json) | Per-node structure constraints | Formal, machine-readable |
| [`spec/framework/branches.json`](spec/framework/branches.json) | 62-branch directory plus extension slots | Formal, machine-readable |
| [`spec/framework/samples/`](spec/framework/samples) | Two minimal bundles (group theory 13 nodes/15 edges; non-Euclidean 63/94) | Sample |
| [`spec/framework/pilots/`](spec/framework/pilots) | Two full pilots (group theory 51/80; calculus 58/102) | Pilot, not full history |
| [`tools/mathlint/`](tools/mathlint) | Document-level linter (stdlib) | Tool |
| [`tools/graphlint/`](tools/graphlint) | Graph validator/generator (PyYAML) | Tool |
| [`tools/audit/`](tools/audit) | Rule-set consistency audit | Tool |
| [`prompts/`](prompts) | P1–P9 writing prompts, Chinese and English | Document |
| [`docs/`](docs) | Method, walkthrough, design drafts, regression pool, fresh-start test | Documents; includes history |
| [`corpus/`](corpus) | 41k-character acceptance corpus and minimal patch (author's own article) | Acceptance material |
| [`reports/`](reports) | Baseline/patch reports, release self-check, ILL requests | Process records; third-party PDFs excluded |
| [`research/`](research) | Independent ontology-mapping and tooling evaluations | Research notes, not spec |
| `literature/` | Local reference PDFs (not distributed with this repository) | Local only |

For entry points, dependencies, failure modes and artifact relationships, see [docs/repository-guide.en.md](docs/repository-guide.en.md) (Chinese: [docs/repository-guide.md](docs/repository-guide.md)).

## How the two specifications fit together

```
prose ──〔A/S/U/F tags〕──> mathlint
  │
  └── extract objects and relations ──> graph.json ──> graphlint
                                             │
                                   edge-signatures.yaml (single source)
                                             ├─ generates graph.schema.json
                                             └─ generates object-model.md §5.2 / §5.6
```

- **Evidence grade** answers “what backs this sentence”; **edges** answer “how are these two things related”. Edges also carry `grade` and `attestation`, so every assertion in a graph stays traceable.
- To change an edge type or an invariant's level, edit only `edge-signatures.yaml`, then run `py -3 -m graphlint generate`. The schema and the edge tables in the ontology document are generated; hand-editing them is an error.

## Current state (kept in sync with the repository)

| Item | Value |
|---|---:|
| Node types | 14 |
| Edge types | 31 |
| Global invariants | 7 |
| Branches | 62 (including proposed extension slots) |
| Graph bundles | 10 (2 samples + 8 pilots) |
| `graphlint check-all` | **0 errors / 60 warnings** (60 existing missing node fields) |
| `graphlint check-all --strict` | 60 errors / 0 warnings (existing gaps promoted) |
| Unit tests | 102, all passing (`mathlint` 77 + `graphlint` 25) |
| Tracked files | 135 |

The 60 warnings are in `pilots/calculus` (52), `pilots/group-theory` (7) and `samples/group-theory` (1): historical missing fields such as `chains` and `occurrences`, not introduced by the latest change; the newly added `pilots/pde`, `pilots/variational-calculus`, `pilots/dynamical-systems`, `pilots/lie-groups`, `pilots/stochastic-analysis` and `pilots/non-classical-logic` all report 0 errors / 0 warnings. Cross-bundle IDs are now scoped: non-branch entities in the `group-theory` sample carry a `.sample` suffix, and `PE:cauchy` / `PE:klein` in the group-theory pilot carry `.group-theory`; `BR-*` nodes and `parent_of` / `cross_class` edges are catalog projections from `branches.json` and are exempted by catalog ID.

## Tools

| Command (from `tools/`) | Purpose | Input | Output |
|---|---|---|---|
| `py -3 -m mathlint check <path>` | Document-level evidence check | `.md` file or directory | errors/warns/infos per file; exit 0/1/2 |
| `py -3 -m graphlint check <path>` | Validate one or more bundles | `graph.json` or directory | violations grouped by level; exit 0/1 |
| `py -3 -m graphlint check-all` | Validate every bundle under `samples/` and `pilots/`, with cross-file ID checks | none | per-file and total counts (files/nodes/edges) |
| `py -3 -m graphlint generate [--check]` | Generate schema/doc tables; `--check` only detects drift | none | writes artifacts or reports sync |
| `py -3 -m audit [kernel\|domain\|criticality\|all]` | Rule-set consistency audit | none | text tables |
| `py -3 tools/scripts/selfcheck.py` | Local CI equivalent: tests + fixtures + examples | none | PASS/FAIL, exit 0/1 |

## Known limitations

- **The 60 node warnings are historical debt**: samples and pilots do not fill required fields such as `chains`, `occurrences`, `name_variants`. They are warnings by default and become errors under `--strict`.
- **`graphlint` tests cover the contract, not every semantic judgment**: 17 tests cover signature endpoints, conditionally required fields, grade caps, independent time windows and `generate --check` drift; complex historical judgments still need humans.
- **CI has never run on real GitHub**: no remote is configured. `.github/workflows/ci.yml` now covers both `mathlint` and `graphlint`, but it can only be verified after the first push.
- **`graphlint` messages are Chinese prose for humans**: `--json` provides structured output, but there are no stable machine-readable error codes.
- **Docs are still mainly Chinese**: the repository guide and licensing notes now have English versions (`docs/repository-guide.en.md`, `docs/licensing.en.md`); detailed ontology and edge-signature explanations remain Chinese-only.
- **The repository directory is still `mathhist-toolkit`** while the package is `mathlint`; renaming would break path examples in the docs.

## License

- **Code** (`tools/` and related scripts): Apache License 2.0, see [LICENSE](LICENSE).
- **Documents and specifications** (`spec/`, `docs/`, `prompts/`, READMEs): CC BY 4.0, see [LICENSE-docs](LICENSE-docs).
- **`corpus/`**: the author's own acceptance article, provided under CC BY 4.0.
- **`research/`**: the author's own research notes, provided under CC BY 4.0.
- **`reports/`**: the author's own process records, provided under CC BY 4.0; they contain no third-party PDFs, scans or long excerpts.
- **`literature/`**: third-party material kept locally only, **not distributed with the repository**, and not covered by these licenses.

Per-directory rationale and third-party notices: [docs/licensing.en.md](docs/licensing.en.md) (Chinese: [docs/licensing.md](docs/licensing.md)).

Attribution example:

```
mathhist-toolkit, evidence-tagging specification and graph ontology, CC BY 4.0
```

## Status

- `mathlint` v0.1: usable, not published to PyPI.
- Graph ontology v0.2: structure frozen, content to be filled; the two pilots expose gaps but are not full history.
- The repository has **no remote, has never been pushed, and has no DOI**; CI config exists but has never run on GitHub.
