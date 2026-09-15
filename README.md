# Lycheetah Framework — Technical Reality

This directory extracts a small set of inspectable tools from a broad research
history. Each tool states the problem it addresses, the command you run, the
behavior measured in a sealed clean-run witness (Packet 05, 2026-08-12), and
what it does **not** prove.

The exploratory funnel that produced these tools was deliberately wide. This
front door is the disciplined extraction of what survived measurement—not a
claim that every prior idea was correct, and not a defence of history.

**Founder / author:** Mackenzie Conor James Clark  
**Provenance:** Lycheetah Framework  
**Licence:** MIT (see `LICENSE` and `NOTICE`)  
**Repository:** https://github.com/Lycheetah/Lycheetah-Framework-Reality  
**Status:** public historical technical extraction; repository self-tests are internal conformance,
not peer review or external validation.

## Surface status — 2026-09-15

**HISTORICAL EXTRACTION / NOT CURRENT FRONTIER FRONT DOOR**

This repository remains public as a dated record of the Packet 05 extraction
and its 2026-08-12 witness. It is not a complete or current representation of
the Lycheetah Frontier Lab, and current frontier work must not be inferred from
its age, contents or repository description. A future frontier lane may be
published only through a separate reviewed release; this tree will not silently
absorb new research or upgrade old evidence.

## Six components

| Component | Maturity | Problem (one line) | First command | Packet 05 measure |
|---|---|---|---|---|
| [LAMAGUE Public Core](components/lamague-public-core/) | `BOUNDED_TOOL` | Refuse silent compression of high-risk semantic packets | `python3 src/public_core_validator.py demo/PUBLIC_DEMO_001_SEMANTIC_PACKET.json` | 16/16 tests OK; demo outcome `VALID` |
| [TIM Evidence Gate](components/tim-evidence-gate/) | `EXPERIMENT` | Preserve unknowns/conflicts before calculation | `python3 engine/tim_evidence_gate_v0_3.py` | 25/25 tests OK |
| [Persona static validator](components/persona-static-validator/) | `EXPERIMENT` | Static lint for persona YAML fields/boundaries | `python3 persona_validator.py sol_persona.yaml` | 7/7 static rules on example; no unit suite |
| [Provenance checker](components/provenance-checker/) | `EXPERIMENT` | Local text fingerprint + heuristic drift ledger | `python3 provenance_checker.py demo` | controlled drift 0.1 / 0.1727 / 0.5 |
| [Drift scorer](components/drift-scorer/) | `EXPERIMENT` | Pure-function conversation shift heuristics | see component README | identical-turn velocity 0.0; absolute scores uncalibrated |
| [CASCADE engine](components/cascade-engine/) | `EXPERIMENT` | In-memory knowledge-block reorganization harness | `python3 toy_smoke.py` | toy retained axiom; no domain science run |

## Quickstart (first useful path — no install if Python 3 is present)

**Interpreter:** Python 3.12+ invoked as `python3` (Debian/Ubuntu and this
witness host do not provide a bare `python` executable).

```bash
cd components/lamague-public-core
python3 src/public_core_validator.py demo/PUBLIC_DEMO_001_SEMANTIC_PACKET.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
# Expect (Packet 05 witness): outcome VALID; Ran 16 tests ... OK
```

Environment facts from Packet 05 (not installs performed by this candidate):
Python 3.12.3; PyYAML 6.0.1 already present for persona; numpy 2.4.6 already
present for the CASCADE toy.

Full offline steps: [`verify/OFFLINE_VERIFICATION.md`](verify/OFFLINE_VERIFICATION.md).

## Not claimed

- Ethics approval, safety certification, or legal clearance of any real deployment
- General AI-safety certification or alignment certification (not claimed)
- Independent external laboratory validation
- Peer-reviewed publication acceptance
- Physics or medicine discovery
- Adoption, stars, sponsors, or install metrics as proof of correctness
- That repository self-tests equal external validation
- That `VALID` (LAMAGUE) means ethical approval

Atomic claim IDs and rejected upgrades: [`docs/CLAIMS_AND_LIMITS.md`](docs/CLAIMS_AND_LIMITS.md).

## Navigation

| Path | Job |
|---|---|
| [`STATUS.md`](STATUS.md) | Maturity snapshot |
| [`docs/EVIDENCE.md`](docs/EVIDENCE.md) | How measurements were produced; how to re-run |
| [`docs/CLAIMS_AND_LIMITS.md`](docs/CLAIMS_AND_LIMITS.md) | Atomic claims and non-claims |
| [`docs/PROVENANCE.md`](docs/PROVENANCE.md) | Sources, hashes, Aura pointer |
| [`docs/CORRECTIONS.md`](docs/CORRECTIONS.md) | Known defects and correction route |
| [`docs/AURA_ORIGIN_POINTER.md`](docs/AURA_ORIGIN_POINTER.md) | Single pointer to 143-file origin export |
| [`verify/`](verify/) | Offline verification expectations |
| [`components/`](components/) | Runnable bodies |

## Excluded from this tree

The following are **excluded** (not admitted capabilities): LANE (repair-required
private pattern), full Aura document corpus, CHRYSOPOEIA, full LAMAGUE grammar /
DASEXY, Living OS product trees, Pure-Cascade monoliths, API benchmark/sandbox
surfaces, prestige README metrics, session narration, and `FOUND_000` (**excluded**). See
`docs/PROVENANCE.md`.

---

Repository self-tests are **internal conformance**. Nothing here is independent
external validation unless a later sealed witness says so.
