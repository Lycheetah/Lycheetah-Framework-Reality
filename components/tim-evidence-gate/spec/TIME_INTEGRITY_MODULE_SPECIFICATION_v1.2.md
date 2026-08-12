# Time Integrity Module — specification digest (public extract)

**Maturity:** `EXPERIMENT`  
**Rewrite:** demoted documentation for the public technical front door.  
**Upstream context:** `spec/TIME_INTEGRITY_MODULE_SPECIFICATION_v1.2.md` at
`587fe912e822dbf0ede4597e90a31253e63a2f3b` (source bytes not re-asserted as physics).

## Scope admitted here

- EvidenceField / ExpressionEvidence models that refuse normalized values on UNKNOWN
- `audit_packet` conflict codes (operator, cross-source value, printed outcome, etc.)
- Deterministic engine paths only when inputs and assumptions are explicit
- Silent Repair Lock motivated by synthetic E008

## Explicit non-scope

- Landauer / TUR as established physics results
- Multimodal OCR/LLM extraction quality on real papers
- Ethics or safety certification

Runnable code lives in `engine/`. Schema: `schema/tim_v1_2_evidence_packet.schema.json`.
Measured totals: Packet 05 witness only.
