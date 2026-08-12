# Time Integrity Module — Evidence Gate (experimental)

**Maturity:** `EXPERIMENT`  
**Component ID:** `tim.evidence_gate_v0_3`  
**Claims:** `CLM-TIM-001` … `CLM-TIM-003`  
**Rejected upgrade:** `CLM-REJ-008` (Landauer/TUR as physics results)

## Problem

When numbers and operators are extracted from messy scientific artifacts, systems
often silently repair operators or invent missing values. Operators need a gate that
preserves contradictions, unknowns, and printed outcomes before any calculation runs.

## Input / output

- **Input:** structured evidence fields/expressions (not raw images inside the engine)
- **Output:** gate report and/or engine profile results
- **CLI:** `python3 engine/tim_evidence_gate_v0_3.py`
- **Tests:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

## Quickstart

```bash
python3 engine/tim_evidence_gate_v0_3.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Measured behavior (Packet 05)

| Measure | Result |
|---|---|
| Unittest suite | 25/25 OK (`CLM-TIM-001`) |
| UNKNOWN + numeric value | `ValueError` (`CLM-TIM-002`) |
| Operator raw vs canonical | `OPERATOR_CONFLICT` preserved |
| Cross-source value conflict | outcome `INCONSISTENT` |
| Missing TUR assumptions | `NOT_APPLICABLE` / `TUR_ASSUMPTIONS_MISSING` |

## Synthetic negative result (E008)

Repository-authored synthetic benchmark summary records E008 silent operator repair
failure as a **negative result** motivating the Silent Repair Lock. Images/assets are
synthetic, not real quantum-hardware measurements (`CLM-TIM-003`, register `HISTORICAL`).

## Limits

- Does **not** validate Landauer/TUR physics.
- Does **not** prove multimodal extraction quality on real literature.
- Not ethics, safety, or alignment certification.
- Benchmark is synthetic multimodal study summary.

## Next external witness

Independent re-run of unittest + gate demo; optional external labelled extraction corpus.
