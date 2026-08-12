# Claims and limits

Atomic public claims for this extraction. **MEASURED** totals require the Packet 05
witness (`clean_run_witnesses.jsonl` SHA-256
`6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`).
Repository self-tests are **not** independent external validation.

Source register: `public_claim_evidence_register.jsonl` (24 records: 14 active,
10 rejected upgrades).

## Active claims

### `CLM-LAM-001` — lamague.public_core_validator

- **Wording:** Under independent Packet 05 re-run, the Public Core repository unittest suite reported 16 tests OK in 0.002s.
- **Truth register:** `MEASURED`
- **Evidence class:** repository self-test
- **Scope:** Staged Lamague-Public@56c4a7d sources in Packet 05 environment only.
- **Non-claim:** Not independent external validation of real-world safety or ethics.
- **Falsifier:** Re-run yields failures/errors or different count without documented environment change.
- **Status:** `ACTIVE` · surface: `README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `lamague.public_core_validator`; field `self_test_totals`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-LAM-002` — lamague.public_core_validator

- **Wording:** The CLI demo packet PUBLIC_DEMO_001 produced outcome VALID and was byte-stable across two fresh copies.
- **Truth register:** `MEASURED`
- **Evidence class:** repository self-test
- **Scope:** Repository-authored demo packet only.
- **Non-claim:** VALID is not ethical approval of a deployment.
- **Falsifier:** Fresh-copy CLI stdout diverges or outcome ≠ VALID.
- **Status:** `ACTIVE` · surface: `README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `lamague.public_core_validator`; field `determinism`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-LAM-003` — lamague.public_core_validator

- **Wording:** Constructed adversarial packets triggered AUTHORITY_MISSING, COMPRESSION_REFUSED, IRREVERSIBLE_WITHOUT_RECOVERY, and OUTSIDE_PUBLIC_CORE refusal paths.
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** Synthetic adversarial packets authored for Packet 05.
- **Non-claim:** Does not prove all real-world high-risk packets are caught.
- **Falsifier:** Named refusal codes fail to fire on the recorded adversarial constructions.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `lamague.public_core_validator`; field `adversarial_cases`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-LAM-004` — lamague.public_core_validator

- **Wording:** A VALID outcome means the packet satisfied the Public Core checklist under this engine, not ethical approval, safety certification, or external validation.
- **Truth register:** `DERIVED`
- **Evidence class:** repository self-test
- **Scope:** Public wording boundary for all surfaces.
- **Non-claim:** Any reading of VALID as ethics approval is forbidden.
- **Falsifier:** Public docs describe VALID as ethical approval.
- **Status:** `ACTIVE` · surface: `README`
- **Evidence route:**
  - `clean_run_claim_corrections.jsonl`; sha256 `3690270e3ec8e2171748c0907165833fa0bf55717b944de433adf60fc1f64995`

### `CLM-TIM-001` — tim.evidence_gate_v0_3

- **Wording:** Under independent Packet 05 re-run, TIM repository tests reported 25 tests OK in 0.005s.
- **Truth register:** `MEASURED`
- **Evidence class:** repository self-test
- **Scope:** Staged time-integrity-module@587fe912.
- **Non-claim:** Not physical validation of Landauer/TUR.
- **Falsifier:** Test suite fails or count changes without documented cause.
- **Status:** `ACTIVE` · surface: `README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `tim.evidence_gate_v0_3`; field `self_test_totals`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-TIM-002` — tim.evidence_gate_v0_3

- **Wording:** Packet 05 adversarial probes held: UNKNOWN fields refuse numeric values; OPERATOR_CONFLICT is preserved; cross-source value conflict yields INCONSISTENT; missing TUR assumptions yield NOT_APPLICABLE.
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** Public API probes on structured fields only.
- **Non-claim:** Not proof of multimodal extraction quality on real papers.
- **Falsifier:** UNKNOWN accepts values or conflicts auto-pass.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `tim.evidence_gate_v0_3`; field `adversarial_cases`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-TIM-003` — tim.evidence_gate_v0_3

- **Wording:** Repository-authored synthetic benchmark summary records E008 silent operator repair failure (3/3) as a negative result motivating the Silent Repair Lock; images are synthetic, not real quantum-hardware measurements.
- **Truth register:** `HISTORICAL`
- **Evidence class:** synthetic authored evidence
- **Scope:** Synthetic multimodal study inside the TIM repository.
- **Non-claim:** Not physical validation; not independent external replication of multimodal LLM extraction.
- **Falsifier:** Docs present E008 as real hardware validation.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `priority_source_file_register.jsonl`; sha256 `46989d465b53a57a328bbe4792d00edde483aa5a32ba388aceb7d3d6f53110a6`; path `benchmark/RESULTS_SUMMARY.json`
  - `source`; sha256 `9f11a94b086a7e11c4ac74dc071e75973e80e581375e99aec0e6e310f01face1`; path `examples/E008_SILENT_REPAIR_PACKET.json`

### `CLM-PER-001` — framework_main.persona_validator_static

- **Wording:** Static mode on sol_persona.yaml completed with seven static rules passed in Packet 05; dynamic/API mode was not run.
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** public-archive/main@516850fd; PyYAML 6.0.1 preinstalled.
- **Non-claim:** Does not measure real model alignment.
- **Falsifier:** Static mode fails on the recorded example without documented cause.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `framework_main.persona_validator_static`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-PER-002` — framework_main.persona_validator_static

- **Wording:** Missing required fields, honesty/deceive heuristic contradiction, and malformed YAML were rejected or failed safe in Packet 05 fixtures.
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** Three adversarial YAML fixtures.
- **Non-claim:** Heuristics are incomplete English-string checks.
- **Falsifier:** Missing identity fields not flagged on the same fixture class.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `framework_main.persona_validator_static`; field `adversarial_cases`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-PRV-001` — framework_main.provenance_checker

- **Wording:** Packet 05 controlled probes produced composite drift scores identical=0.1, small_edit=0.1727, radical=0.5, deterministic across two fresh copies after dropping volatile IDs/timestamps.
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** Local demo/probe environment writing SQLite under tool dir.
- **Non-claim:** Not cryptographic multi-party provenance.
- **Falsifier:** Scores diverge across fresh copies under same normalization.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `framework_main.provenance_checker`; field `controlled_scores`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-PRV-002` — framework_main.provenance_checker

- **Wording:** Identical content can still score residual composite drift 0.1 because source_attribution is 0.0 when origin metadata is omitted on re-check (alert remains clean; ANOMALY_003).
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** Documented defect of the heuristic composite.
- **Non-claim:** Must not be described as perfect identical-match zero-drift.
- **Falsifier:** Docs claim identical content always yields 0.0 composite drift.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_claim_corrections.jsonl`; sha256 `3690270e3ec8e2171748c0907165833fa0bf55717b944de433adf60fc1f64995`

### `CLM-DRF-001` — framework_main.drift_scorer

- **Wording:** Pure score_conversation is deterministic offline; identical consecutive turns had velocity 0.0 on turn 2 in Packet 05, while absolute peak drift remained ~0.4875 (warning) because SA was 0.0 on short non-overlapping pairs.
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** Pure-function matrix only; UI not run.
- **Non-claim:** Channels are uncalibrated design labels, not ethics/alignment measurements.
- **Falsifier:** Identical consecutive turns show large unexplained velocity under pure functions.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `framework_main.drift_scorer`; field `exact_scores`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-CAS-001` — cascade_framework.engine

- **Wording:** Packet 05 confirmed AST syntax-ok for cascade_engine.py, domain_template.py, and run_experiments.py; a domain-neutral in-memory toy with three blocks retained its axiom (still_has_axiom true).
- **Truth register:** `MEASURED`
- **Evidence class:** deterministic probe
- **Scope:** numpy 2.4.6 preinstalled; domain germ/quantum/medical narratives not run.
- **Non-claim:** Not a scientific, medical, or historical discovery.
- **Falsifier:** Toy axiom not retained after the documented add sequence.
- **Status:** `ACTIVE` · surface: `component_README`
- **Evidence route:**
  - `clean_run_witnesses.jsonl`; component `cascade_framework.engine`; field `toy_result`; sha256 `6673e6f925448cee4998d9a8cf832000420ff4a012b44e585bbf05a781d09f44`

### `CLM-CAS-002` — cascade_framework.engine

- **Wording:** Any claim that CASCADE validated physics, medicine, paradigm-shift history, or produced peer-reviewed scientific results is outside Packet 05 evidence and is not public-front-door wording.
- **Truth register:** `DERIVED`
- **Evidence class:** none
- **Scope:** Public code tree reduced engine only.
- **Non-claim:** Manuscript formatting and synthetic experiment prose are not external validation.
- **Falsifier:** Public README imports arXiv experimental tables as MEASURED without new witness.
- **Status:** `ACTIVE` · surface: `STATUS_ONLY`
- **Evidence route:**
  - `CAELORYNTH_PACKET_05_REVIEW.md`; sha256 `a641261938691bc6f1b1cec2796749a6035c4861025335b8816a80f981fe5bf2`
  - `papers/CASCADE_ARXIV.tex`; sha256 `bcc7fb38132012d98e7e403a7b1586834ba36afe79bd2e756e89dfe42cd7562d`; manuscript claims not re-witnessed as science

## Rejected upgrades (must not re-enter by prose drift)

These ten claims are **REJECTED**. Any public surface stating them is a defect.

### `CLM-REJ-001` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** This repository or any admitted component has ethics approval or institutional ethics clearance.
- **Component:** `REPOSITORY_SHELL`
- **Rejection reason:** Ethics approval was not part of Packet 04/05 and is not evidenced.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-002` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** The admitted tools constitute general AI safety or alignment certification.
- **Component:** `REPOSITORY_SHELL`
- **Rejection reason:** No general safety property was measured; LANE shell walls failed bypass probes and are excluded.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-003` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** The work is independently externally validated by third parties.
- **Component:** `REPOSITORY_SHELL`
- **Rejection reason:** Only campaign-local independent re-runs exist; no external lab replication recorded.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-004` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** The work has completed peer review or is an accepted academic publication.
- **Component:** `REPOSITORY_SHELL`
- **Rejection reason:** arXiv plan and drafts exist; no peer-review acceptance evidence in reckoning artifacts.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-005` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** CASCADE discoveries in physics or medicine are established by the admitted engine or old manuscripts.
- **Component:** `cascade_framework.engine`
- **Rejection reason:** Packet 05 ran only a toy; historical domain modules are hand-authored narratives.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-006` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** Adoption, stars, sponsors, PyPI install metrics, or model praise prove technical correctness.
- **Component:** `REPOSITORY_SHELL`
- **Rejection reason:** Packet 04 rejected framework-main prestige README metrics as evidence.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-007` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** Persona static lint measures real model alignment or sovereignty.
- **Component:** `framework_main.persona_validator_static`
- **Rejection reason:** Static schema/heuristic only; dynamic mode unwitnessed.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-008` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** TIM validates Landauer bounds or thermodynamic uncertainty relations as physics results.
- **Component:** `tim.evidence_gate_v0_3`
- **Rejection reason:** Profiles are diagnostic; benchmark synthetic.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-009` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** LANE provides a complete no-push / no-bypass shell safety wall suitable for public extract as-is.
- **Component:** `lane.law_and_workspace_walls`
- **Rejection reason:** Packet 05 FAIL: four decision-only bypasses; REPAIR_REQUIRED; excluded from tree.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

### `CLM-REJ-010` — REJECTED

- **Rejected wording (REJECTED — not a live claim):** Repository self-tests are equivalent to independent external validation.
- **Component:** `REPOSITORY_SHELL`
- **Rejection reason:** Explicit campaign law and Packet 05 crown forbid this upgrade.
- **Public surface:** `NOT_PUBLIC` (must remain not public)

## Register note

Contextual mention of excluded systems (for example LANE) appears only as a
labelled exclusion or rejection, not as an admitted capability.
