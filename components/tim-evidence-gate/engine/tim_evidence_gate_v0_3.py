from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import json
import math
from typing import Any, Iterable, Optional


class GateOutcome(str, Enum):
    VALID = "VALID"
    PARTIAL = "PARTIAL"
    INCONSISTENT = "INCONSISTENT"
    REJECTED = "REJECTED"


class FieldState(str, Enum):
    OBSERVED = "OBSERVED"
    UNKNOWN = "UNKNOWN"


class ConflictCode(str, Enum):
    CROSS_SOURCE_VALUE_CONFLICT = "CROSS_SOURCE_VALUE_CONFLICT"
    CROSS_SOURCE_EXPONENT_CONFLICT = "CROSS_SOURCE_EXPONENT_CONFLICT"
    UNIT_MISSING = "UNIT_MISSING"
    UNIT_CONFLICT = "UNIT_CONFLICT"
    OPERATOR_CONFLICT = "OPERATOR_CONFLICT"
    PRINTED_OUTCOME_CONFLICT = "PRINTED_OUTCOME_CONFLICT"
    MISSING_REQUIRED_INPUT = "MISSING_REQUIRED_INPUT"
    ENTROPY_CLOSURE_FAILURE = "ENTROPY_CLOSURE_FAILURE"


@dataclass(frozen=True)
class EvidenceField:
    field_id: str
    semantic_name: str
    raw_text: Optional[str]
    normalized_value: Optional[float]
    unit: Optional[str]
    source_id: str
    state: FieldState
    confidence: Optional[float] = None

    def __post_init__(self) -> None:
        if self.state is FieldState.UNKNOWN:
            if self.normalized_value is not None:
                raise ValueError("UNKNOWN evidence must not contain a normalized value.")
        elif self.raw_text is None:
            raise ValueError("OBSERVED evidence requires raw_text.")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be within [0, 1].")


@dataclass(frozen=True)
class ExpressionEvidence:
    expression_id: str
    source_id: str
    raw_expression: str
    left_value: float
    raw_operator: str
    right_value: float
    printed_outcome: Optional[str]
    canonical_operator: Optional[str]
    canonical_scope: Optional[str] = None


_OPERATOR_MAP = {
    "<": "<",
    "<=": "<=",
    "≤": "<=",
    ">": ">",
    ">=": ">=",
    "≥": ">=",
    "=": "==",
    "==": "==",
    "≠": "!=",
    "!=": "!=",
}


def _normalise_operator(operator: str) -> str:
    token = operator.strip()
    if token not in _OPERATOR_MAP:
        raise ValueError(f"Unsupported operator: {operator!r}")
    return _OPERATOR_MAP[token]


def _evaluate(left: float, operator: str, right: float) -> bool:
    op = _normalise_operator(operator)
    if op == "<":
        return left < right
    if op == "<=":
        return left <= right
    if op == ">":
        return left > right
    if op == ">=":
        return left >= right
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    raise AssertionError(op)


def _sha256_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _is_power_of_ten_ratio(a: float, b: float, tolerance: float = 1e-9) -> bool:
    if a == 0 or b == 0:
        return False
    ratio = abs(a / b)
    exponent = round(math.log10(ratio))
    return exponent != 0 and math.isclose(ratio, 10.0 ** exponent, rel_tol=tolerance, abs_tol=0.0)


def audit_expression(expression: ExpressionEvidence) -> dict[str, Any]:
    raw_op = _normalise_operator(expression.raw_operator)
    raw_truth = _evaluate(expression.left_value, raw_op, expression.right_value)

    canonical_op = None
    canonical_truth = None
    operator_conflict = False
    if expression.canonical_operator is not None:
        canonical_op = _normalise_operator(expression.canonical_operator)
        canonical_truth = _evaluate(expression.left_value, canonical_op, expression.right_value)
        operator_conflict = raw_op != canonical_op

    printed = expression.printed_outcome.upper() if expression.printed_outcome else None
    printed_truth = None if printed is None else printed == "PASS"
    printed_outcome_conflict = printed_truth is not None and printed_truth != raw_truth

    conflicts: list[dict[str, Any]] = []
    if operator_conflict:
        conflicts.append({
            "code": ConflictCode.OPERATOR_CONFLICT.value,
            "raw_operator": expression.raw_operator,
            "canonical_operator": expression.canonical_operator,
            "message": "Printed and canonical operators differ. Both branches are preserved.",
        })
    if printed_outcome_conflict:
        conflicts.append({
            "code": ConflictCode.PRINTED_OUTCOME_CONFLICT.value,
            "printed_outcome": printed,
            "raw_expression_truth": raw_truth,
            "message": "Printed PASS/FAIL label conflicts with the literal printed expression.",
        })

    return {
        "expression_id": expression.expression_id,
        "source_id": expression.source_id,
        "raw_observation": {
            "raw_expression": expression.raw_expression,
            "left_value": expression.left_value,
            "raw_operator": expression.raw_operator,
            "right_value": expression.right_value,
            "printed_outcome": printed,
            "literal_truth": raw_truth,
        },
        "canonical_check": {
            "operator": expression.canonical_operator,
            "truth": canonical_truth,
            "scope": expression.canonical_scope,
        },
        "conflicts": conflicts,
        "evidence_hash": _sha256_json(asdict(expression)),
    }


def audit_packet(
    experiment_id: str,
    fields: Iterable[EvidenceField],
    expressions: Iterable[ExpressionEvidence] = (),
    required_semantic_names: Iterable[str] = (),
    calculation_requirements: Optional[dict[str, list[str]]] = None,
    entropy_closure: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    field_list = list(fields)
    expression_list = list(expressions)
    conflicts: list[dict[str, Any]] = []

    by_semantic: dict[str, list[EvidenceField]] = {}
    for field in field_list:
        by_semantic.setdefault(field.semantic_name, []).append(field)
        if field.state is FieldState.OBSERVED and field.normalized_value is not None and not field.unit:
            conflicts.append({
                "code": ConflictCode.UNIT_MISSING.value,
                "semantic_name": field.semantic_name,
                "source_id": field.source_id,
                "message": "Observed numeric evidence has no explicit unit.",
            })

    for semantic_name, observations in by_semantic.items():
        known = [x for x in observations if x.state is FieldState.OBSERVED and x.normalized_value is not None]
        values = {x.normalized_value for x in known}
        units = {x.unit for x in known}
        if len(units) > 1:
            conflicts.append({
                "code": ConflictCode.UNIT_CONFLICT.value,
                "semantic_name": semantic_name,
                "units": sorted(str(x) for x in units),
                "message": "The same semantic field was observed with conflicting units.",
            })
        if len(values) > 1:
            code = ConflictCode.CROSS_SOURCE_VALUE_CONFLICT
            pair = list(values)
            if len(pair) == 2 and _is_power_of_ten_ratio(pair[0], pair[1]):
                code = ConflictCode.CROSS_SOURCE_EXPONENT_CONFLICT
            conflicts.append({
                "code": code.value,
                "semantic_name": semantic_name,
                "observations": [
                    {
                        "source_id": item.source_id,
                        "raw_text": item.raw_text,
                        "value": item.normalized_value,
                        "unit": item.unit,
                    }
                    for item in known
                ],
                "message": "Conflicting observations were preserved without canonical selection.",
            })

    required = set(required_semantic_names)
    known_names = {
        field.semantic_name
        for field in field_list
        if field.state is FieldState.OBSERVED and field.normalized_value is not None
    }
    unit_missing_names = {
        field.semantic_name
        for field in field_list
        if field.state is FieldState.OBSERVED
        and field.normalized_value is not None
        and not field.unit
    }

    missing_required = sorted(required - known_names)
    for name in missing_required:
        conflicts.append({
            "code": ConflictCode.MISSING_REQUIRED_INPUT.value,
            "semantic_name": name,
            "message": "Required evidence is unknown; dependent calculations must remain blocked.",
        })

    if entropy_closure is not None:
        declared = entropy_closure.get("declared_total")
        components = entropy_closure.get("components", [])
        tolerance = float(entropy_closure.get("relative_tolerance", 1e-9))
        if declared is not None and all(x is not None for x in components):
            component_sum = float(sum(components))
            denom = max(abs(float(declared)), 1e-300)
            relative_error = abs(float(declared) - component_sum) / denom
            if relative_error > tolerance:
                conflicts.append({
                    "code": ConflictCode.ENTROPY_CLOSURE_FAILURE.value,
                    "declared_total": declared,
                    "component_sum": component_sum,
                    "relative_error": relative_error,
                    "message": "Declared entropy total conflicts with the preserved component sum.",
                })

    expression_audits = [audit_expression(item) for item in expression_list]
    for item in expression_audits:
        conflicts.extend(item["conflicts"])

    requirements = calculation_requirements or {}
    blocked_calculations: list[dict[str, Any]] = []
    for calculation, needed in requirements.items():
        absent = sorted((set(needed) - known_names) | (set(needed) & unit_missing_names))
        if absent:
            blocked_calculations.append({
                "calculation": calculation,
                "missing_inputs": absent,
                "reason": "MISSING_REQUIRED_INPUT",
            })

    hard_conflict_codes = {
        ConflictCode.CROSS_SOURCE_VALUE_CONFLICT.value,
        ConflictCode.CROSS_SOURCE_EXPONENT_CONFLICT.value,
        ConflictCode.UNIT_CONFLICT.value,
        ConflictCode.OPERATOR_CONFLICT.value,
        ConflictCode.PRINTED_OUTCOME_CONFLICT.value,
        ConflictCode.ENTROPY_CLOSURE_FAILURE.value,
        ConflictCode.UNIT_MISSING.value,
    }
    has_hard_conflict = any(item["code"] in hard_conflict_codes for item in conflicts)
    has_missing = bool(missing_required or blocked_calculations)

    if has_hard_conflict:
        outcome = GateOutcome.INCONSISTENT
    elif has_missing:
        outcome = GateOutcome.PARTIAL
    else:
        outcome = GateOutcome.VALID

    immutable_evidence = {
        "fields": [asdict(field) for field in field_list],
        "expressions": [asdict(expression) for expression in expression_list],
    }

    report = {
        "specification": "TIM v1.2",
        "gate": "TIM Evidence Gate v0.3",
        "experiment_id": experiment_id,
        "outcome": outcome.value,
        "immutable_evidence": immutable_evidence,
        "evidence_hash": _sha256_json(immutable_evidence),
        "conflicts": conflicts,
        "expression_audits": expression_audits,
        "blocked_calculations": blocked_calculations,
        "ready_for_deterministic_engine": outcome is GateOutcome.VALID,
        "silent_repair_lock": {
            "enabled": True,
            "rule": "Raw observations are immutable and cannot be replaced by canonical interpretations.",
        },
    }
    report["semantic_hash"] = _sha256_json(report)
    return report


if __name__ == "__main__":
    fields = [
        EvidenceField("A", "accuracy", "100", 100.0, "dimensionless", "panel_A", FieldState.OBSERVED),
        EvidenceField("RHS", "tur_rhs", "110", 110.0, "dimensionless", "panel_A", FieldState.OBSERVED),
    ]
    expressions = [
        ExpressionEvidence(
            expression_id="TUR_PRINTED",
            source_id="panel_A",
            raw_expression="100 ≥ 110 → PASS",
            left_value=100.0,
            raw_operator="≥",
            right_value=110.0,
            printed_outcome="PASS",
            canonical_operator="≤",
            canonical_scope="declared synthetic TUR profile",
        )
    ]
    print(json.dumps(audit_packet("E008-DEMO", fields, expressions), indent=2, default=str))
