# Corrections and residual defects

How claims are demoted, residual defects from Packet 05, and how to report new ones.

Corrections ledger SHA-256: `3690270e3ec8e2171748c0907165833fa0bf55717b944de433adf60fc1f64995`

## Correction route

1. **Do not silently edit admitted code** to make a verification pass.
2. Record the mismatch (command, expected, actual) under the component section.
3. Claim ownership: **Mackenzie Conor James Clark** for identity/publication;
   **Caelorynth** for independent claim admission review.
4. Prefer demoting the claim or marking `PASS_WITH_DIFFERENCE` / `FAIL` over
   laundering a failure through documentation.

## Component corrections (Packet 05)

### `lamague.public_core_validator`

- **Claim id:** `lamague.valid_is_not_ethics`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** CLI demo exit 0; unittest Ran 16 tests OK; adversarial AUTHORITY_MISSING/COMPRESSION_REFUSED/IRREVERSIBLE_WITHOUT_RECOVERY/OUTSIDE_PUBLIC_CORE hold; CLI deterministic across fresh copies.
- **Public wording now permitted:** LAMAGUE Public Core is a stdlib deterministic rule engine over JSON semantic packets. A VALID outcome means the packet satisfied the Public Core checklist under this engine, not ethical approval, safety certification, or external validation.

### `lamague.public_core_validator`

- **Claim id:** `lamague.self_tests_internal_only`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** Independent re-run: 16/16 OK in 0.002s.
- **Public wording now permitted:** Repository self-tests establish internal conformance after independent re-run only; they are not independent external validation.

### `tim.evidence_gate_v0_3`

- **Claim id:** `tim.gate_and_tests`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** Gate demo exit 0 deterministic across copies; unittest Ran 25 tests OK; UNKNOWN+value raises ValueError; OPERATOR_CONFLICT preserved; CROSS_SOURCE_VALUE_CONFLICT → INCONSISTENT; missing TUR assumptions → NOT_APPLICABLE with TUR_ASSUMPTIONS_MISSING.
- **Public wording now permitted:** TIM evidence gate v0.3 and engine v0.2 are offline deterministic tools for structured evidence fields. Passing self-tests and toy calculations do not validate Landauer/TUR physics or multimodal extraction quality. Benchmark assets remain repository-authored and synthetic.

### `framework_main.persona_validator_static`

- **Claim id:** `persona.static_lint_only`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** PyYAML 6.0.1 present; sol_persona.yaml static run exit 0; missing-fields → REJECTED with IDENTITY_VOID; honesty/deceiv contradiction → VALUE_CONTRADICTION; malformed YAML exits 1 with parse error. Dynamic/API mode not run.
- **Public wording now permitted:** Persona validator static mode is a YAML schema/heuristic lint (seven rule functions). It does not measure real model alignment, ethics, or sovereignty. Dynamic LLM-as-judge mode was not witnessed and is not a safety proof.

### `framework_main.provenance_checker`

- **Claim id:** `provenance.local_not_crypto`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** demo exit 0 writes SQLite; identical text semantic_sim=1.0 but composite drift=0.1 (source_attribution=0.0, alert clean, ANOMALY_003); small edit 0.1727; radical 0.5; scores deterministic across copies after dropping volatile IDs/timestamps.
- **Public wording now permitted:** Provenance checker is a local SHA-256 + token-set similarity ledger with SQLite. Composite drift mixes content similarity with attribution/lineage heuristics; it is not cryptographic multi-party provenance or CASCADE scientific truth dynamics.
- **Residual defects / failures:**
  - Identical content does not yield 0.0 composite drift; residual 0.1 from source_attribution when re-check omits origin source metadata.

### `framework_main.drift_scorer`

- **Claim id:** `drift.uncalibrated_channels`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** Pure functions ran offline; identical consecutive turns boundary held; scores deterministic across fresh copies; empty and single-turn conversations handled.
- **Public wording now permitted:** Drift scorer pure functions compute uncalibrated design-label channels (SA/VA/IS/EI) from token/keyword heuristics. They are visualization aids, not calibrated measures of alignment, ethics, or identity.

### `lane.law_and_workspace_walls` (EXCLUDED FROM TREE)

- **Claim id:** `lane.tool_layer_walls_not_general_safety`
- **Status:** `FAIL`
- **Measured:** test_law.py ALL LAW TESTS PASSED; test_workspace_wall.py ALL OFFLINE TESTS PASSED; direct git push blocked; workspace escape/symlink/protected write blocked; eval git push blocked; BYPASSES (decision-only, never executed): `git -C . push origin main`, `curl … | /bin/bash`, `CMD=push; git $CMD …`, `$G $P` variable indirection.
- **Public wording now permitted (LANE remains EXCLUDED from this tree):** LANE law.py tool-layer guards block several dangerous bash/path forms and pass their offline self-tests. They do not provide general AI safety. Known regex/argv bypasses include `git -C … push`, `/bin/bash` pipe forms, and shell variable indirection for push. Any public extract must document these limits or repair them first.
- **Residual defects / failures:**
  - BYPASS: git -C . push origin main allowed by guard_bash
  - BYPASS: curl URL | /bin/bash allowed by guard_bash
  - BYPASS: CMD=push; git $CMD origin main allowed
  - BYPASS: G=git; P=push; $G $P origin main allowed

### `lane.law_and_workspace_walls` (EXCLUDED FROM TREE)

- **Claim id:** `lane.private_secrets`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** .env was not staged (git archive of tracked files only); no secret values recorded.
- **Public wording now permitted (LANE remains EXCLUDED from this tree):** LANE remains a private-source pattern candidate. Secrets in local .env are out of scope and must never be exported.

### `cascade_framework.engine`

- **Claim id:** `cascade.engine_not_science`
- **Status:** `PASS_WITH_LIMITS`
- **Measured:** AST syntax-ok for cascade_engine.py, domain_template.py, run_experiments.py; numpy 2.4.6 present; empty engine + toy in-memory blocks ran; axiom retained after adds; germ/quantum/medical narratives not run.
- **Public wording now permitted:** cascade_engine.py is a numpy in-memory KnowledgeBlock reorganization harness. A successful toy simulation is not a scientific, medical, or historical discovery. Domain experiment modules remain theory surfaces.

## Known residual limits (summary)

| Area | Limit |
|---|---|
| Provenance checker | Identical text can score composite drift **0.1** (attribution component when origin metadata omitted); alert remains clean |
| Drift scorer | Absolute scores near ~0.49/warning on short non-overlapping pairs; channels uncalibrated |
| LAMAGUE `VALID` | Checklist pass only — not ethics approval |
| TIM E008 | Synthetic negative result — not hardware/physics validation |
| CASCADE | Toy axiom retention only — not science discovery |
| LANE | **Excluded**; shell bypasses documented privately for repair; not a public exploit cookbook |

## Demotion rule

If a re-run falsifies a MEASURED claim, the claim is demoted or corrected in
`docs/CLAIMS_AND_LIMITS.md` and this file. Prestige, mythology, and unreproduced
tables do not re-enter through README prose.
