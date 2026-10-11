# Before the Validator

**Numeric Wire Fidelity in LLM Tool Pipelines** — research manuscript and executable artifact, October 12, 2026.

**Status: not submitted or peer reviewed.** The experiments were executed locally. This is a focused systems audit, not a claim to invent lossless JSON, discover floating-point precision limits, establish production prevalence, or guarantee conference acceptance. Substantive author verification and revision are still required. See [submission assessment](docs/SUBMISSION_ASSESSMENT.md).

The paper is [here](paper/main.pdf); an anonymous formatting draft is [here](paper/anonymous.pdf). The source uses the official, unmodified ACL style files. The main content ends on page 6; limitations, ethics, references, and appendices follow. The authored manuscript names Shivam Gupta as requested and transparently documents research assistance. The anonymous formatting draft omits acknowledgments under the venue's review-format instructions; this is not permission to omit required declarations during submission.

## What was actually run

- All 9,558 files in a pinned JSONSchemaBench revision were inspected. Two duplicate-key files were excluded.
- Exact reference validation of 8,207 distinct schema–value pairs from 34,357 **local numeric projections**. A projection witness need not satisfy its enclosing full schema.
- The published TypeScript MCP SDK 1.32.1 parser and Ajv 8.20.0, plus existing lossless-json 4.3.1 baselines.
- A separate 15,265-token differential family with a Python rational reference.
- 162 requests to actual local MCP server processes: 54 native numeric, 54 guarded numeric, and 54 explicitly string-typed identifier requests.
- Local timing batches, recorded with variability and no production latency claim.

Native transport changed 2,600 primary values; 2,349 changes passed Ajv. Native local lookup selected the wrong fixture record for 25/54 requests. The guard rejected those requests; string identifiers resolved all 54 correctly. Existing lossless JSON preserved all primary values. These are stress-test outcomes, not a distribution of real model emissions.

## Reproduce

Use Node 24+ and Python 3.9+ (published Python results used 3.9.6). A Python virtual environment is recommended. No model credentials or paid inference are needed.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
npm ci
python3 scripts/fetch_corpus.py --dest ../corpus
python3 scripts/build_cases.py ../corpus/data
node scripts/run_transport.mjs
node scripts/audit_literals.mjs ../corpus/data
python3 scripts/analyze.py
export NODE=node
python3 scripts/run_demo.py
python3 scripts/property_check.py
node scripts/schema_witnesses.mjs
python3 -m unittest discover -s tests -v
python3 scripts/verify_results.py
node scripts/benchmark.mjs
python3 scripts/figures.py
```

To compile the documents, install Tectonic and run `tectonic main.tex` and `tectonic anonymous.tex` from `paper/`. Timing measurements will vary. Numeric results are deterministic at pinned versions. The download script verifies both the archive hash and all 9,558 schema hashes. It downloads third-party schemas into a separate directory and retains their provenance README. Review their upstream terms before redistribution.

`src/fidelity.mjs` contains the reference guard. It is **not a complete security gateway**: it addresses numeric parse–serialize fidelity, assumes duplicate-free input, and does not establish schema-validator arithmetic correctness, authorization, or safe business actions. The ingress demo is a local fixture, not production infrastructure. Lossless numeric wrappers require compatible downstream handling.

## Evidence and provenance

- `data/cases.json`: exact numeric projections and source tokens, deduplicated.
- `data/corpus_manifest.json`: source revision's file hashes.
- `results/transports.json`: raw actual parser/guard outputs.
- `results/literal_audit.json`: source literals that changed, with file and pointer.
- `results/demo.json`: complete local protocol requests and responses.
- `results/schema_witnesses.json`: four source-invalid/changed-schema counterexamples.
- `results/property_outputs.json`: independent differential outputs.
- `results/summary.json`: measured aggregates, environment and package versions.
- `docs/LITERATURE_AND_OVERLAP.md`: relevant prior work and novelty boundary.

The large repeated local-projection index is generated rather than committed. The primary inputs contain numeric schema fragments; entire upstream schemas and model conversations are not redistributed here. Newly authored code is MIT licensed; upstream dependencies, templates, and datasets retain their own terms. Research assistance is disclosed in the authored paper and submission assessment. No external service operations or account credentials are included.
