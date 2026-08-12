# Evidence

## What was measured

Packet 05 (2026-08-12) re-ran the six admitted components offline in a clean staging
tree, verified every staged file against Packet 04 content hashes, and recorded
commands, exit codes, stdout/stderr digests, and parsed totals.

- Witness ledger: campaign artifact `clean_run_witnesses.jsonl`
- Witness SHA-256: `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`
- Claim corrections SHA-256: `3690270e3ec8e2171748c0907165833fa0bf55717b944de433adf60fc1f64995`
- Environment snapshot: `clean_run_environment.json`

## Environment facts (Packet 05)

| Fact | Value |
|---|---|
| OS | Linux 7.0.9-76070009-generic (x86_64) |
| Python | 3.12.3 (`/usr/bin/python3`) |
| PyYAML | 6.0.1 already present (persona) |
| numpy | 2.4.6 already present (CASCADE toy) |
| Package install/upgrade | **false** |
| Offline only | **true** |
| API keys set/exposed | **false** |

## Evidence classes

| Class | Meaning |
|---|---|
| **Repository self-test** | Unittest or CLI demo authored with the project |
| **Deterministic probe** | Fixed inputs; scores/outcomes compared across copies |
| **Synthetic authored evidence** | Repository-authored scenarios (e.g. TIM E008) |

**Boundary:** none of the above is independent external validation, peer review,
or real-world impact proof.

## How to reproduce from this candidate tree

Follow [`verify/OFFLINE_VERIFICATION.md`](../verify/OFFLINE_VERIFICATION.md).
Compare against [`verify/expected_results.json`](../verify/expected_results.json),
which copies Packet 05 measured totals only—it does **not** pre-label a later run
as passing.

Use `PYTHONDONTWRITEBYTECODE=1` or `python3 -B` so bytecode caches are not created
inside the tree.

## Source baselines (must remain unchanged by this extraction)

| Source | Immutable ref |
|---|---|
| CODEX_AURA_PRIME HEAD | `a9bddb1fdd81d2f7975707433ba7ca772553b6c2` |
| public-archive/main | `516850fdc4e0ec3b85c121b252379644f18f20a3` |
| time-integrity-module | `587fe912e822dbf0ede4597e90a31253e63a2f3b` |
| Lamague-Public | `56c4a7d25b4d29373bd224211848ae6a02ed59bb` |
| cascade-framework | `4a935d96ae2ebe67ca9a7b3e3bda452f2d045977` |
| LANE (excluded) | `0bafbb4fd9c6784b75e27de94413137f20e6dee9` |

## Interpreting `PASS_WITH_LIMITS`

Every admitted component finished Packet 05 as `PASS_WITH_LIMITS`: the offline
path ran, and residual defects or scope limits were recorded rather than hidden.
See [`CORRECTIONS.md`](CORRECTIONS.md) and [`CLAIMS_AND_LIMITS.md`](CLAIMS_AND_LIMITS.md).
