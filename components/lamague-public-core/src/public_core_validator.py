from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path
import re
from typing import Any


PUBLIC_OPERATIONS = set("OE UIGVF YZ".replace(" ", ""))


class Outcome(str, Enum):
    VALID = "VALID"
    EXPAND = "EXPAND"
    REPAIR = "REPAIR"
    REJECT = "REJECT"


@dataclass
class Finding:
    law: str
    outcome: Outcome
    code: str
    message: str
    repair: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["outcome"] = self.outcome.value
        return d


def parse_expression(expression: str) -> list[str]:
    parts = [
        x.strip()
        for x in expression.replace("→", "->").split("->")
        if x.strip()
    ]
    result = []
    for part in parts:
        match = re.fullmatch(r"([A-Z])(?:<[^>]+>)?", part)
        if not match:
            raise ValueError(f"Invalid operation token: {part}")
        op = match.group(1)
        if op not in PUBLIC_OPERATIONS:
            raise ValueError(f"Operation {op} is outside the Public Core")
        result.append(op)
    if not result:
        raise ValueError("Expression is empty")
    return result


def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    findings: list[Finding] = []
    path = packet.get("operation_path", [])
    unknowns = packet.get("unknowns", [])
    authority = packet.get("authority", [])
    affected = packet.get("affected_parties", [])
    recovery = packet.get("recovery", [])
    risk = packet.get("risk_level", "low")
    irreversible = bool(packet.get("irreversible", False))
    confidence = float(packet.get("decoder_confidence", 0.0))

    invalid_ops = [op for op in path if op not in PUBLIC_OPERATIONS]
    if invalid_ops:
        findings.append(Finding(
            "SCOPE", Outcome.REJECT, "OUTSIDE_PUBLIC_CORE",
            f"Operations outside the Public Core: {invalid_ops}",
            "Use only O, E, U, I, G, V, F, Y, and Z."
        ))

    consequential = risk in {"medium", "high", "critical"} or bool(
        set(path) & {"G", "V", "Y"}
    )

    if consequential and not authority:
        findings.append(Finding(
            "L2", Outcome.REJECT, "AUTHORITY_MISSING",
            "Consequential meaning has no visible authority.",
            "Declare bounded authority before yielding a result."
        ))

    if consequential and not affected:
        findings.append(Finding(
            "L2", Outcome.REPAIR, "AFFECTED_PARTIES_MISSING",
            "Consequential meaning omits affected parties.",
            "Name directly and indirectly affected parties."
        ))

    if "U" in path and not unknowns:
        findings.append(Finding(
            "L3", Outcome.EXPAND, "UNKNOWN_UNDECLARED",
            "The expression invokes Unknown but preserves no unresolved content.",
            "Declare at least one typed unknown."
        ))

    if irreversible and not recovery:
        findings.append(Finding(
            "L1", Outcome.REJECT, "IRREVERSIBLE_WITHOUT_RECOVERY",
            "An irreversible condition has no containment or recovery path.",
            "Halt and define containment; do not yield ordinary operation."
        ))

    compression_reasons = []
    if risk in {"high", "critical"}:
        compression_reasons.append("high-impact context")
    if unknowns:
        compression_reasons.append("protected unknowns remain")
    if irreversible:
        compression_reasons.append("irreversibility is declared")
    if confidence < 0.80:
        compression_reasons.append("decoder confidence below 0.80")
    if consequential and not authority:
        compression_reasons.append("authority missing")

    compression_mode = "Z_UP" if compression_reasons else "Z_DOWN"

    if "Z" in path and compression_mode == "Z_UP":
        findings.append(Finding(
            "L1", Outcome.EXPAND, "COMPRESSION_REFUSED",
            "Compression would endanger recoverability.",
            "Expand the packet and preserve: " + ", ".join(compression_reasons)
        ))

    if "F" not in path:
        findings.append(Finding(
            "LINEAGE", Outcome.REPAIR, "MEMORY_FOLD_MISSING",
            "The path does not fold its result into recoverable memory.",
            "Add F before the final yield."
        ))

    if "Y" not in path:
        findings.append(Finding(
            "OUTPUT", Outcome.REPAIR, "YIELD_MISSING",
            "The expression has no bounded output.",
            "Add Y after audit and memory."
        ))

    severity = {
        Outcome.VALID: 0,
        Outcome.EXPAND: 1,
        Outcome.REPAIR: 2,
        Outcome.REJECT: 3,
    }
    outcome = max(
        (f.outcome for f in findings),
        key=lambda x: severity[x],
        default=Outcome.VALID,
    )

    protected_fields = {
        "unknowns": unknowns,
        "invariants": packet.get("invariants", []),
        "authority": authority,
        "affected_parties": affected,
        "dissent": packet.get("dissent", []),
        "value_flow": packet.get("value_flow", []),
        "recovery": recovery,
        "provenance": packet.get("provenance", []),
    }

    return {
        "case_id": packet.get("case_id", ""),
        "outcome": outcome.value,
        "compression_mode": compression_mode,
        "compression_reasons": compression_reasons,
        "operation_path": path,
        "findings": [f.to_dict() for f in findings],
        "protected_fields": protected_fields,
        "explanation": explain(packet, compression_mode),
    }


def explain(packet: dict[str, Any], compression_mode: str) -> str:
    path = " → ".join(packet.get("operation_path", []))
    unknowns = packet.get("unknowns", [])
    invariants = packet.get("invariants", [])
    return (
        f"Public Core path {path}. "
        f"The packet protects {len(invariants)} invariant(s) and "
        f"{len(unknowns)} unresolved unknown(s). "
        f"Compression decision: {compression_mode}. "
        f"Authority: {', '.join(packet.get('authority', [])) or 'missing'}. "
        f"Affected parties: {', '.join(packet.get('affected_parties', [])) or 'missing'}."
    )


def load_and_validate(path: str | Path) -> dict[str, Any]:
    packet = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_packet(packet)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("packet")
    args = parser.parse_args()
    print(json.dumps(load_and_validate(args.packet), indent=2, ensure_ascii=False))
