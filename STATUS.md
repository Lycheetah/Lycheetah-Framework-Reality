# Status — Lycheetah-Framework-Reality

**Record date:** 2026-08-12  
**Latest local admission:** 2026-08-12; six bounded component witnesses reproduced and
the provenance fail-closed regression passed 10/10 focused tests  
**Surface designation:** `HISTORICAL_EXTRACTION` — frozen at Packet 05 / 2026-08-12; boundary reviewed 2026-09-15
**Public-front-door boundary:** This repository is not the current public face of
the Lycheetah Frontier Lab. The selected public frontier release surface is
[`lycheetah-frontier-public`](https://github.com/Lycheetah/lycheetah-frontier-public),
currently limited to a reviewed SpL-X v0.2 proposal. Other frontier lanes require
their own reviewed publication decision and evidence; they are not represented by
this status record.
**External validation:** none recorded  
**Peer review:** none recorded  
**Publication remote:** https://github.com/Lycheetah/Lycheetah-Framework-Reality  

## Maturity table

| Component ID | Display name | Maturity | Packet 05 status | Disposition |
|---|---|---|---|---|
| `lamague.public_core_validator` | LAMAGUE Public Core | `BOUNDED_TOOL` | `PASS_WITH_LIMITS` | RETAIN |
| `tim.evidence_gate_v0_3` | TIM Evidence Gate | `EXPERIMENT` | `PASS_WITH_LIMITS` | RETAIN_AS_EXPERIMENT |
| `framework_main.persona_validator_static` | Persona static validator | `EXPERIMENT` | `PASS_WITH_LIMITS` | RETAIN_AS_EXPERIMENT |
| `framework_main.provenance_checker` | Provenance checker | `EXPERIMENT` | `PASS_WITH_LIMITS` | RETAIN_AS_EXPERIMENT |
| `framework_main.drift_scorer` | Drift scorer | `EXPERIMENT` | `PASS_WITH_LIMITS` | RETAIN_AS_EXPERIMENT |
| `cascade_framework.engine` | CASCADE engine | `EXPERIMENT` | `PASS_WITH_LIMITS` | RETAIN_AS_EXPERIMENT |

### Token meanings

- **`BOUNDED_TOOL`** — Admitted for use with explicit limits; only LAMAGUE Public Core holds this token.
- **`EXPERIMENT`** — Runnable; claims tightly scoped; not a production safety surface.
- **`PASS_WITH_LIMITS`** — Offline re-run succeeded; residual limits documented in claims/corrections.

## Excluded (not in tree)

| Item | Why |
|---|---|
| LANE law/workspace walls | Packet 05 `FAIL` / `REPAIR_REQUIRED` (decision-only bypass probes); private source |
| Aura document exports | Provenance pointer only (143-file identical cluster) |
| CHRYSOPOEIA, DASEXY, Living OS, Pure-Cascade monoliths | Outside technical front door |
| API benchmark / sandbox modes | Not admitted |
| CASCADE domain science modules and paper binaries | Not re-witnessed as science |

## Honest summary

One bounded tool and five experiments passed an internal offline witness with
limits. No component carries external validation, peer review, or ethics approval.

## Known debt (Packet 08 P2 — non-blocking)

Cold-outsider review Packet 08 recorded eleven P2 observations. They are **not**
release blockers and are **not** claims of fitness. Packet 09 repaired only the
seven P0/P1 findings; these remain visible so they are not silently erased.

| ID | Disposition | Reason |
|---|---|---|
| `OPUS08-P2-008` | `OPEN_NON_BLOCKING` | Drift `requirements.txt` still lists FastAPI/uvicorn/pydantic unused by shipped code. |
| `OPUS08-P2-009` | `OPEN_NON_BLOCKING` | Provenance `requirements.txt` still says “production use” for optional sentence-transformers. |
| `OPUS08-P2-010` | `OPEN_NON_BLOCKING` | CASCADE has no `requirements.txt`; numpy/scipy undeclared beyond README prose. |
| `OPUS08-P2-011` | `OPEN_NON_BLOCKING` | `domain_template.py` still carries prestige-register phrasing and names an unshipped file. |
| `OPUS08-P2-012` | `OPEN_NON_BLOCKING` | CASCADE `info_preserved` / `entropy_preserved` flags are structurally always true. |
| `OPUS08-P2-013` | `OPEN_NON_BLOCKING` | TIM `reports/TEST_RESULTS.txt` lacks a provenance header. |
| `OPUS08-P2-014` | `OPEN_NON_BLOCKING` | TIM schema + E008 example have no runtime consumer in the shipped tree. |
| `OPUS08-P2-015` | `OPEN_NON_BLOCKING` | Drift turn-1 velocity/threshold events are initialisation artifacts. |
| `OPUS08-P2-016` | `OPEN_NON_BLOCKING` | LAMAGUE `parse_expression` is library/test-only; schema vs validator key strictness differs. |
| `OPUS08-P2-017` | `OPEN_NON_BLOCKING` | TIM `energy_time_theorem: str = ()` type/default mismatch (latent). |
| `OPUS08-P2-018` | `OPEN_NON_BLOCKING` | Persona still has no dedicated unit suite in-tree (focused probes live in campaign acceptance). |

P0/P1 repair status lives in the campaign `packet09_acceptance.jsonl`, not here.
