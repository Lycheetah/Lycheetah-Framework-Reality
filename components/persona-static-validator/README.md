# Persona YAML static lint (experimental)

**Maturity:** `EXPERIMENT`  
**Component ID:** `framework_main.persona_validator_static`  
**Claims:** `CLM-PER-001`, `CLM-PER-002`  
**Rejected upgrade:** `CLM-REJ-007` (real model alignment / sovereignty)

## Problem

Authors of AI persona or system-prompt YAML files need a static check for missing
identity fields, weak boundaries, and crude value contradictions before runtime.

## Input / output

- **Input:** persona YAML path
- **Output:** console or JSON report of static violations and a non-authoritative
  `static_pass` / `static_fail_*` result
- **CLI:** `python3 persona_validator.py <persona.yaml>`
- **Dependency:** PyYAML only (Packet 05 environment had 6.0.1 already present; no install)

## Quickstart

```bash
python3 persona_validator.py sol_persona.yaml
```

### Exact success console shape (valid input)

```
══════════════════════════════════════════════════════════════
  PERSONA YAML STATIC LINT
  Lycheetah Foundation | static extraction (no dynamic mode)
══════════════════════════════════════════════════════════════
  Persona :  Sol v3.0.0
  Run ID  :  ppv-<timestamp>
  File    :  sol_persona.yaml
  Mode    :  static_only

── STATIC CHECK ─────────────────────────────────────────────
  Rules checked : 7
  Rules passed  : 7
  Violations    : none

── RESULT ───────────────────────────────────────────────────
  ✓  STATIC LINT PASSED
  STATIC LINT PASSED — YAML satisfied the seven static heuristics. Static YAML lint only. Not deployment approval, safety certification, or model-alignment evidence.

  SCOPE
  Static YAML lint only. Not deployment approval, safety certification, or model-alignment evidence.
══════════════════════════════════════════════════════════════
```

Exit code: **0** on `static_pass`; **1** on any critical/high static failure or parse error.

### Exact success JSON shape (`--json-only`)

Key fields (non-authoritative):

```json
{
  "mode": "static_only",
  "static_result": "static_pass",
  "result_explanation": "STATIC LINT PASSED — YAML satisfied the seven static heuristics. Static YAML lint only. Not deployment approval, safety certification, or model-alignment evidence.",
  "scope_notice": "Static YAML lint only. Not deployment approval, safety certification, or model-alignment evidence.",
  "not_claims": [
    "deployment_approval",
    "safety_certification",
    "model_alignment_evidence",
    "ethics_approval",
    "production_readiness"
  ],
  "static_check": {
    "passed": true,
    "rules_checked": 7,
    "rules_passed": 7
  }
}
```

Success uses the non-authoritative token `static_pass` only. There is no
`deployment_recommendation` field and no network/LLM-judge block in this file.

## Measured behavior (Packet 05 / re-witnessed Packet 07A)

| Case | Result |
|---|---|
| `sol_persona.yaml` static | exit 0; seven static rules passed; `static_result=static_pass` |
| Missing required fields | exit 1; IDENTITY_VOID / `static_fail_critical` |
| Honesty vs deceive heuristic | exit 1; VALUE_CONTRADICTION |
| Malformed YAML | exit 1 with parse error on stderr |
| unknown flag `--dynamic` | argparse rejects it; exit nonzero |

## Why this extraction is static-only

The upstream lineage still contains an unwitnessed LLM-as-judge path. **This public
extraction intentionally removes that path**: no network mode, no credential CLI
arguments or examples, no third-party LLM client import, and no install suggestion
for any LLM client. The admitted claim surface is seven static YAML heuristics.
Runtime model-alignment evaluation is a rejected upgrade (`CLM-REJ-007`), not a
feature of this file.

## Limits

- Static schema/heuristic lint only — **does not measure real model alignment**
- A `static_pass` is **not** deployment approval, safety certification, or ethics clearance
- English-string contradiction heuristics are incomplete by design
- No unit test suite on the source branch

## Next external witness

Add a minimal unit suite; independent static-mode re-run of the seven rules.
