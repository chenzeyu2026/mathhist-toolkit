# Repository guide: how the tools run and how the artifacts relate

For a first visit. Goal: within ten minutes, know **which file is the spec, which is an example, which is a research note**, and get both checkers running.

---

## 1. Three sentences first

1. `spec/` is the **specification**; `spec/framework/` is its machine-readable skeleton. `edge-signatures.yaml` is the **single source** for edges and invariants.
2. `samples/` holds **minimal examples**, `pilots/` holds **full pilots**, and `research/` holds **research notes**. The last two are not complete history and are not the spec.
3. `tools/` contains two checkers: the document-level `mathlint` and the graph-level `graphlint`. Both use the same `A / S / U / F` evidence scale.

---

## 2. Artifact map

```
spec/
├── evidence-tags.md / .en.md            Document-level evidence-tag spec (v0.1)
├── object-model.md                      Graph ontology (v0.2; includes generated edge tables)
└── framework/
    ├── edge-signatures.yaml             ★ single source: 31 edge types + 7 invariants
    ├── graph.schema.json                ← generated from edge-signatures.yaml
    ├── object-model.schema.json         Node-structure constraints (hand-written)
    ├── branches.json                    62-branch directory plus extension slots
    ├── samples/                         Two minimal bundles
    │   ├── group-theory.json            13 nodes / 15 edges
    │   └── non-euclidean-geometry.json  63 nodes / 94 edges
    └── pilots/                          Two complete pilots
        ├── group-theory/graph.json      51 nodes / 80 edges
        └── calculus/graph.json          58 nodes / 102 edges
```

| Artifact | Question it answers | Formal spec? | Machine-readable |
|---|---|---|---|
| `evidence-tags*.md` | What backs a sentence (`A/S/U/F`) | Yes | No |
| `object-model.md` | Which objects exist and which relations are allowed | Yes | No (edge tables are generated) |
| `edge-signatures.yaml` | Endpoints, direction, attributes and invariants per edge type | Yes | Yes |
| `graph.schema.json` | JSON shape of a single edge | Yes (generated) | Yes |
| `object-model.schema.json` | JSON shape of a single node | Yes | Yes |
| `branches.json` | 62 branches and extension slots | Yes | Yes |
| `samples/` | “What a minimal usable bundle looks like” | No | Yes |
| `pilots/` | “What a real branch looks like when filled, and where it strains” | No | Yes |
| `research/` | Mapping experiments and tooling evaluations | No | Partly |

**Relationship**: `edge-signatures.yaml` generates the edge list in `graph.schema.json` and the two tables in `object-model.md` §5.2 / §5.6. `graphlint` validates against the same YAML. They cannot drift apart because there is only one source.

---

## 3. Environment and dependencies

| Item | Requirement |
|---|---|
| Python | 3.11+ (tested locally with 3.13.14; CI matrix uses 3.11/3.12/3.13) |
| `mathlint` | Standard library only, no third-party dependency |
| `graphlint` | PyYAML ≥ 6.0 |
| Working directory | Run commands from `tools/` with `-m`; after installation they work anywhere |

```bash
cd mathhist-toolkit/tools
py -3 -m pip install "PyYAML>=6.0"   # needed by graphlint only
```

Windows note: if `py -3` is unavailable, use `python`. If `python` opens the Microsoft Store alias, install Python and keep using `py -3`.

---

## 4. Tools one by one

### 4.1 `mathlint`: document-level evidence tags

- **What it does**: parses `〔A｜原始文献:…〕`, `〔S｜二手研究:…〕`, `〔U｜未核实:…〕`, `〔F｜流行说法:…〕`; checks tag syntax, whether grade and source type agree, citation format, whether `U` gives a reason, and whether one citation is tagged with conflicting grades.
- **Input**: an `.md` file or a directory (recursively collects `.md`).
- **Output**: errors / warnings / infos per file, plus a total; `--json` gives structured output.
- **Failure example**:

```text
$ py -3 -m mathlint check tests/fixtures/invalid.md
...
合计：13 error / 1 warn / 0 info · exit=1
```

Common codes: `GRADE_SOURCE_MISMATCH` (grade does not fit source type), `MISSING_REASON` (`U` without a reason), `BAD_ISBN`, etc.

- **Exit codes**: 0 no error; 1 error, or `--strict` with warnings; 2 argument/path error.
- **Options**: `--offline` (default, no network), `--online` (probe DOI/URL), `--json`, `--strict`.

### 4.2 `graphlint check`: validate one or more bundles

- **What it does**: validates node-ID prefixes, edge envelope, endpoint existence and type, direction, required attributes and enums, time, evidence-grade caps, cycles, weight sums, mutex rules, isolated nodes and `claims` references.
- **Input**: one or more `graph.json` files (JSON with `nodes` / `edges`) or directories.
- **Output**: grouped as `== error（N）==` / `== warning（N）==`; each item gives file, edge/node ID, `位置:` (RFC 6901 JSON Pointer), message, actual value, expected value and rationale; per-file and total counts at the end. In `--json`, every issue carries `rule_id`, `pointer` and `severity`; each file and the summary carry `nodes` / `edges` counts.
- **Failure shape**:

```text
== error（1）==
  [ATTESTATION_GRADE_CAP] spec/framework/pilots/group-theory/graph.json :: E:TW:cayley-1854.print>witness_of>TX:cayley-1854
      说明: attestation=textbook_simplification 时 grade 上限不满足：实得 S（期望 F 或 U）。教材转述不能支撑 S 级。
      实际: attestation=textbook_simplification, grade=S
      期望: grade ∈ {F, U}
      依据: A=亲见原件；S=二手研究；F=教材/流行说法；U=未核实。不要为了过关冒充一手文献。
```

(This is an illustrative output. That edge is now `later_report` in the repository, so it no longer reports.)

- **Exit codes**: 0 no error; 1 error (or `--strict` with warnings); 2 no bundle found.
- **Options**: `--strict` (promote node-completeness warnings to errors, and let warnings fail), `--json`, `--max-items N` (default 25; 0 shows all).

### 4.3 `graphlint check-all`: run every sample and pilot

- **What it does**: equivalent to `graphlint check spec/framework/samples spec/framework/pilots`, plus a **cross-file ID check**: when the same node/edge ID appears in two bundles, it reports `NODE_ID_DUPLICATE` / `EDGE_ID_DUPLICATE` with both file paths and JSON Pointers.
- **Input**: none.
- **Current result**: 4 bundles, 185 nodes, 291 edges, **30 errors / 60 warnings**, exit 1. All 60 warnings are `NODE_REQUIRED`. The 30 errors are pre-existing data overlaps: the `group-theory` sample and pilot share IDs, and `PE:cauchy` / `PE:klein` are reused across bundles. Run `check` on a single `graph.json` to see only its local format issues.
- **Summary line**: `汇总：error N / warning N · files N / nodes N / edges N`; the `--json` `summary` has the same fields.
- **`--strict`**: promotes the 60 warnings to errors, for 90 errors in total, exit 1.

### 4.4 `graphlint generate`: generate from the single source

- **What it does**: reads `spec/framework/edge-signatures.yaml`, rewrites the edge enum, conditional constraints and `$comment` in `graph.schema.json`, and replaces the table blocks marked `<!-- GENERATED:… -->` in `spec/object-model.md`.
- **Input**: none.
- **Output**: writes two files; `--check` writes nothing and only reports whether the artifacts are in sync with the YAML.
- **Failure**:

```text
生成物与 edge-signatures.yaml 不一致：
  - spec/framework/graph.schema.json
运行 py -3 -m graphlint generate 重新生成。
```

- **Rule**: to change an edge type, endpoint or invariant level, **edit the YAML only**. Hand-editing the schema or the generated blocks is exposed by the next `generate --check` and treated as an error.

### 4.5 `audit`: rule-set consistency audit

Run `py -3 -m audit [kernel|domain|criticality|all]` from `tools/`.

- **What it does**: reproduces the internal derivation of the evidence-tag spec: conflicts and indeterminacy in v0/v1 rules, six-dimension domain elimination and deduplication, per-rule criticality.
- **Input**: none.
- **Output**: three text tables (`kernel` / `domain` / `criticality`).
- **Failure**: rule counts that disagree with the documents show up as text diffs; no fixed exit-code contract (normally 0).

### 4.6 `tools/scripts/selfcheck.py`: local CI equivalent

- **What it does**: runs the `mathlint` and `graphlint` unit tests (99 in total: 77 + 22) plus 3 fixtures and 3 sample passages, printing `PASS/FAIL` and expected counts.
- **Input**: none.
- **Output**: `self-check PASSED` or a list of failures.
- **Exit code**: 0 all pass; 1 any failure.
- **Note**: it does **not** run `graphlint check-all`; use the commands below for graph checks.

### 4.7 `tools/pyproject.toml`: installation and entry points

- **What it does**: declares package name `mathlint`, version, Python ≥ 3.11, dependency `PyYAML>=6.0`, and registers `mathlint` and `graphlint`; `packages` includes only `mathlint` and `graphlint` (`audit` and `scripts/` are not packaged).
- **Input**: none.
- **Output**: after `pip install -e tools`, both commands work anywhere.
- **Failure**: offline or missing build dependencies make `pip` fail in the isolated build step; do not install in that case — use `py -3 -m ...` from `tools/`.
- **Note**: the package is `mathlint` while the repository is `mathhist-toolkit`; decide the package boundary before publishing to PyPI.

### 4.8 Portability

The tool code contains no hard-coded local paths: `graphlint/signatures.py` derives the repository root from `Path(__file__)`, and `mathlint` only touches paths passed to it. Examples in the documentation should use relative paths so that commands can be copied and run elsewhere.

---

## 5. Common combinations

```bash
cd tools

# Minimal gate before committing
py -3 scripts/selfcheck.py
py -3 -m graphlint check-all
py -3 -m graphlint generate --check

# One bundle only
py -3 -m graphlint check ../spec/framework/pilots/calculus/graph.json

# Machine-readable results
py -3 -m graphlint check-all --json

# After changing an edge signature
py -3 -m graphlint generate
py -3 -m graphlint generate --check
py -3 -m graphlint check-all
```

---

## 6. Directory and naming conventions

- **ID prefixes**: `BR-`, `CO:`, `TH:`, `PR:`, `ME:`, `TY:`, `FA:`, `NO:`, `PE:`, `TX:`, `TW:`, `EV:`, `TP:`, `ST:`; `CLM:` appears only inside `claims[]`.
- **Edge IDs derive from endpoints**: `E:<from>><type>><to>`, with `#2`, `#3` for parallel edges.
- **File naming**: branch bundles use `graph.json`, long prose uses `text.md`, pilot notes use `report.md`; samples use `<branch>.json`.
- **Generated artifacts**: `graph.schema.json` and the generated blocks in `object-model.md` carry `GENERATED` markers, **do not hand-edit**.
- **Commit style**: one English sentence as the title; the body may be Chinese and should list changed files and reasons (see `git log`).
- **`.gitignore`** covers `__pycache__/`, `*.py[cod]`, virtual environments, build outputs, `*.egg-info/`, `.pytest_cache/`, plus `literature/`, `reports/literature/`, `*.pdf` and `*.docx`.

---

## 7. Starting a new graph

1. Read `spec/object-model.md` §3–§5 and confirm the node and edge types you actually need.
2. Use only edge types registered in `spec/framework/edge-signatures.yaml`. If a type is missing, propose a spec change; do not extend the table locally.
3. Copy `spec/framework/samples/group-theory.json` as a skeleton; keep `schema_version: "0.2"`, `nodes` and `edges`.
4. Run `py -3 -m graphlint check <your file>` and fix errors; handle warnings as needed.
5. Put long arguments and quotations in a sibling `text.md`, and point back with `text_ref: "doc:<file>#<anchor>"`; do not make the graph carry long prose.

---

## 8. What is not the specification

- `research/`: mapping experiments and tooling choices; conclusions may be revised — check the date before citing.
- `pilots/` and `samples/`: instances used to expose gaps; historical facts are not fully checked and must not be cited as historical conclusions.
- `reports/`: process records with baseline/patch numbers and document-delivery requests; see `docs/licensing.md` for third-party material.
- `corpus/`: the author's own acceptance corpus, not a general-purpose corpus.
- `literature/`: local reference PDFs, untracked, **do not commit**.
