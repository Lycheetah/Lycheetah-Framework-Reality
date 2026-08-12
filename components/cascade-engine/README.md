# CASCADE knowledge-block reorganization engine (experimental)

**Maturity:** `EXPERIMENT`  
**Component ID:** `cascade_framework.engine`  
**Claims:** `CLM-CAS-001`, `CLM-CAS-002`  
**Rejected upgrade:** `CLM-REJ-005` (physics/medicine discovery)

## Problem

A researcher wants a small in-memory harness that reorganizes scored knowledge blocks
under constraints and compares toy baselines, without treating domain narratives as
scientific discoveries.

## Input / output

- **Input:** in-memory `KnowledgeBlock` objects
- **Output:** engine state (layers/regimes/foundations)
- **Dependency:** numpy (Packet 05: 2.4.6 already present; no install)

## Quickstart

```bash
python3 -c "import ast; ast.parse(open('cascade_engine.py').read()); print('syntax-ok')"
python3 toy_smoke.py
```

## Measured behavior (Packet 05)

| Measure | Result |
|---|---|
| AST parse | `cascade_engine.py`, `domain_template.py` syntax-ok |
| Toy | three blocks added; `still_has_axiom` true; foundations `axiom_a`, `claim_b` |
| Domain germ/quantum/medical narratives | **not run** |

## Limits

- A successful toy simulation is **not** a scientific, medical, or historical discovery
- Does not validate paradigm-shift narratives in excluded domain modules
- Does not inherit prestige metrics or arXiv experimental tables as MEASURED
- No unit suite; engine may use numpy RNG in unexercised paths

## Next external witness

Unit tests for constraint preservation; any domain experiment needs a separate sealed
evidence packet.
