# Local text provenance / drift ledger (experimental)

**Maturity:** `EXPERIMENT`  
**Component ID:** `framework_main.provenance_checker`  
**Claims:** `CLM-PRV-001`, `CLM-PRV-002`

## Problem

Editors need a local way to fingerprint text, track edits across a small ledger, and
score rough content drift **without** claiming cryptographic multi-party provenance.

## Input / output

- **Input:** text content and optional metadata
- **Output:** node ids, drift scores, alert level, anomaly codes; demo writes SQLite
- **CLI:** `python3 provenance_checker.py demo`

## Quickstart

```bash
python3 provenance_checker.py demo
```

## Runtime state (ledger)

By default `demo`, `fingerprint`, and `check` write a local SQLite ledger at
`components/provenance-checker/provenance_ledger.db` (next to the script;
`DB_PATH`). Library calls with `conn=None` open, write, and close that same
ledger — a node id is never returned without a durable store.

- **Override:** pass an explicit `sqlite3.Connection` from `init_db(path)` for
  batch or alternate paths.
- **Clean:** `rm components/provenance-checker/provenance_ledger.db` (also
  covered by the repository root `.gitignore`).

## Fail-closed contract (`check` and `chain`)

Unknown or truncated node ids fail closed with structured status
`NODE_NOT_FOUND` on **both** advertised lookup paths:

| Path | Behaviour on unknown/truncated id |
|---|---|
| `check <node_id> <content>` | Structured `NODE_NOT_FOUND`; no CLEAN/drift score; CLI exit **nonzero** |
| `chain <id>… --contents …` | Same for **every** id at **every** position (including origin); no partial chain report; no `action_required: none` success signal; CLI exit **nonzero** |

`list` prints the full 64-character node id for copy/paste into `check` / `chain`.

### Focused regression (Packet 13 / OPUS12-P1-025)

```bash
cd components/provenance-checker
python3 -m unittest test_chain_fail_closed -v
```

## Measured behavior (Packet 05)

Controlled composite drift scores (deterministic across two fresh copies after
dropping volatile IDs/timestamps):

| Case | Composite drift |
|---|---|
| Identical text | 0.1 |
| Small edit | 0.1727 |
| Radical rewrite | 0.5 |

## Residual limitation (documented defect)

Identical content does **not** yield 0.0 composite drift. Residual **0.1** comes from
`source_attribution=0.0` when origin metadata is omitted on re-check (alert remains
`clean`; `ANOMALY_003`). Do not describe the tool as perfect zero-drift identical match.

## Limits

- Not cryptographic multi-party provenance
- Not CASCADE scientific truth dynamics
- Not calibrated semantic similarity independent of token overlap + attribution heuristics

## Next external witness

Document attribution component in tests; independent demo re-run.
