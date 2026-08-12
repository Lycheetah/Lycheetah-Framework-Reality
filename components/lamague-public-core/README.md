# LAMAGUE Public Core Packet Validator

**Maturity:** `BOUNDED_TOOL`  
**Component ID:** `lamague.public_core_validator`  
**Claims:** `CLM-LAM-001` … `CLM-LAM-004`

## Problem

Operators need a tiny, inspectable checklist that refuses silent compression of
high-risk semantic packets and forces explicit authority, unknowns, recovery, and
yield fields before a packet is marked valid.

## Input / output

- **Input:** JSON semantic packet path
- **Output:** JSON validation report (`VALID` / `EXPAND` / `REPAIR` / `REJECT`) with findings
- **CLI:** `python3 src/public_core_validator.py <packet.json>`
- **Tests:** `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

## Quickstart

```bash
python3 src/public_core_validator.py demo/PUBLIC_DEMO_001_SEMANTIC_PACKET.json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Measured behavior (Packet 05)

| Measure | Result | Register |
|---|---|---|
| Unittest suite | 16/16 OK | `MEASURED` (`CLM-LAM-001`) |
| Demo CLI | outcome `VALID`, deterministic across two fresh copies | `MEASURED` (`CLM-LAM-002`) |
| Adversarial refusals | AUTHORITY_MISSING, COMPRESSION_REFUSED, IRREVERSIBLE_WITHOUT_RECOVERY, OUTSIDE_PUBLIC_CORE | `MEASURED` (`CLM-LAM-003`) |

## Integrity manifest

`MANIFEST.sha256.json` covers every shipped component file **except itself**
(self-hash would be circular). Verify from this directory:

```bash
python3 -c "import json,hashlib,sys; from pathlib import Path; m=json.loads(Path('MANIFEST.sha256.json').read_text()); root=Path('.'); bad=[]; [bad.append(e['path']) for e in m['files'] if not (root/e['path']).is_file() or hashlib.sha256((root/e['path']).read_bytes()).hexdigest()!=e['sha256']]; print('FAIL', bad) if bad else print('MANIFEST_OK', m['file_count']); sys.exit(1 if bad else 0)"
```

## Limits

- **`VALID` means the packet satisfied this engine's rules under the supplied inputs.**
  It is **not** ethical approval, safety certification, or legal clearance (`CLM-LAM-004`).
- Scope is the Public Core nine-operation subset only.
- Demo and tests are repository-authored synthetic packets.
- Repository self-tests are internal conformance, not independent external validation.
- Full LAMAGUE grammar, DASEXY, and symbolic extensions are **excluded** / not admitted here.

## Next external witness

Independent outsider re-run of CLI + unittest on a clean machine; optional third-party
packet corpus not authored by the project.
