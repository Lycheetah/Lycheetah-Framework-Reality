# Offline verification

Ordered steps derived from Packet 05 commands for the six retained components.
**Do not treat this file as a pre-labelled pass for a later run.** Compare your
results to `expected_results.json`.

Prerequisites (facts from Packet 05, not installs):

- Python 3 (Packet 05 used 3.12.3)
- PyYAML already importable for persona (Packet 05: 6.0.1)
- numpy already importable for CASCADE toy (Packet 05: 2.4.6)
- No network; no package manager; no API keys

Always set `PYTHONDONTWRITEBYTECODE=1` (or use `python3 -B`).

Working directory for each block is the component directory under `components/`.

## 1. LAMAGUE Public Core (`BOUNDED_TOOL`)

```bash
cd components/lamague-public-core
python3 src/public_core_validator.py demo/PUBLIC_DEMO_001_SEMANTIC_PACKET.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Packet 05 expectation: CLI outcome `VALID`; `Ran 16 tests` … `OK`.

## 2. TIM Evidence Gate (`EXPERIMENT`)

```bash
cd components/tim-evidence-gate
python3 engine/tim_evidence_gate_v0_3.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Packet 05 expectation: gate demo exit 0; `Ran 25 tests` … `OK`.

## 3. Persona static validator (`EXPERIMENT`)

```bash
cd components/persona-static-validator
python3 persona_validator.py sol_persona.yaml
```

Packet 05 expectation: static path exit 0; seven static rules passed on the example;
dynamic/API mode not run. Adversarial fixtures (missing fields / contradiction /
malformed YAML) are described in Packet 05; re-create fixtures if testing refusals.

## 4. Provenance checker (`EXPERIMENT`)

```bash
cd components/provenance-checker
python3 provenance_checker.py demo
```

Controlled probes (Packet 05): composite drift identical=0.1, small_edit=0.1727,
radical=0.5. Residual: identical text does not yield 0.0 composite drift.

Example probe expression (illustrative only — not runnable as written; there is no
`ProvenanceChecker` class on the public surface):

```bash
# ILLUSTRATIVE / NON-RUNNABLE — use `python3 provenance_checker.py demo` instead
python3 - <<'PY'
from provenance_checker import ProvenanceChecker  # not shipped; use CLI demo / library functions
PY
```

Prefer the built-in `demo` and library calls documented in the component README.

## 5. Drift scorer (`EXPERIMENT`)

```bash
cd components/drift-scorer
python3 -c "from drift_scorer import score_conversation; import json; print(json.dumps(score_conversation([{'prompt':'What is 2+2?','response':'I value honesty, care, and careful reasoning.'},{'prompt':'What is 2+2?','response':'I value honesty, care, and careful reasoning.'}])))"
```

Packet 05 expectation: identical consecutive turns velocity 0.0 on turn 2; absolute
peak drift may remain ~0.4875 (warning) because SA is 0.0 on short non-overlapping pairs.

## 6. CASCADE engine (`EXPERIMENT`)

```bash
cd components/cascade-engine
python3 -c "import ast; ast.parse(open('cascade_engine.py').read()); print('syntax-ok')"
python3 -c "import ast; ast.parse(open('domain_template.py').read()); print('syntax-ok')"
python3 toy_smoke.py
```

Packet 05 expectation: `still_has_axiom` true; `n_blocks_after` 3; no domain science.

## Evidence boundary

Repository self-tests and deterministic probes are **internal conformance**.
They are not external validation, peer review, ethics approval, or scientific discovery.
