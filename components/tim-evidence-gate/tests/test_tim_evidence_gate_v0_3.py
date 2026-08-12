from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from tim_evidence_gate_v0_3 import (
    EvidenceField,
    ExpressionEvidence,
    FieldState,
    audit_expression,
    audit_packet,
)


def observed(field_id, semantic_name, raw_text, value, unit, source_id):
    return EvidenceField(
        field_id=field_id,
        semantic_name=semantic_name,
        raw_text=raw_text,
        normalized_value=value,
        unit=unit,
        source_id=source_id,
        state=FieldState.OBSERVED,
    )


class TIMEvidenceGateTests(unittest.TestCase):
    def test_unknown_cannot_contain_value(self):
        with self.assertRaises(ValueError):
            EvidenceField("x", "variance", None, 4.0, "ticks^2", "panel", FieldState.UNKNOWN)

    def test_cross_panel_exponent_conflict_is_preserved(self):
        report = audit_packet(
            "E006",
            [
                observed("m1", "measurement_entropy", "5.0 × 10^-22", 5e-22, "J/K/window", "A"),
                observed("m2", "measurement_entropy", "5.0 × 10^-21", 5e-21, "J/K/window", "B"),
            ],
        )
        self.assertEqual(report["outcome"], "INCONSISTENT")
        codes = {item["code"] for item in report["conflicts"]}
        self.assertIn("CROSS_SOURCE_EXPONENT_CONFLICT", codes)
        self.assertFalse(report["ready_for_deterministic_engine"])
        self.assertEqual(len(report["immutable_evidence"]["fields"]), 2)

    def test_missing_data_blocks_calculations_without_invention(self):
        fields = [
            observed("mean", "mean_tick_count", "800", 800, "ticks/window", "panel"),
            EvidenceField("variance", "variance", None, None, "ticks^2", "panel", FieldState.UNKNOWN),
        ]
        report = audit_packet(
            "E007",
            fields,
            required_semantic_names=["mean_tick_count", "variance"],
            calculation_requirements={"accuracy": ["mean_tick_count", "variance"]},
        )
        self.assertEqual(report["outcome"], "PARTIAL")
        self.assertEqual(report["immutable_evidence"]["fields"][1]["normalized_value"], None)
        self.assertEqual(report["blocked_calculations"][0]["calculation"], "accuracy")

    def test_tur_operator_trap_is_not_repaired(self):
        expression = ExpressionEvidence(
            expression_id="tur",
            source_id="panel_A",
            raw_expression="100 ≥ 110 → PASS",
            left_value=100,
            raw_operator="≥",
            right_value=110,
            printed_outcome="PASS",
            canonical_operator="≤",
            canonical_scope="synthetic",
        )
        audit = audit_expression(expression)
        self.assertEqual(audit["raw_observation"]["raw_operator"], "≥")
        self.assertFalse(audit["raw_observation"]["literal_truth"])
        self.assertTrue(audit["canonical_check"]["truth"])
        codes = {item["code"] for item in audit["conflicts"]}
        self.assertIn("OPERATOR_CONFLICT", codes)
        self.assertIn("PRINTED_OUTCOME_CONFLICT", codes)

    def test_energy_time_operator_trap(self):
        expression = ExpressionEvidence(
            expression_id="energy_time",
            source_id="panel_B",
            raw_expression="6.0e-35 < 5.27e-35 → FAIL",
            left_value=6.0e-35,
            raw_operator="<",
            right_value=5.27e-35,
            printed_outcome="FAIL",
            canonical_operator="≥",
            canonical_scope="declared synthetic comparison",
        )
        audit = audit_expression(expression)
        self.assertFalse(audit["raw_observation"]["literal_truth"])
        self.assertTrue(audit["canonical_check"]["truth"])
        self.assertEqual(audit["raw_observation"]["raw_operator"], "<")

    def test_entropy_closure_failure(self):
        report = audit_packet(
            "E004",
            [
                observed("clock", "clock_entropy", "2e-21", 2e-21, "J/K/window", "panel"),
                observed("measurement", "measurement_entropy", "5e-21", 5e-21, "J/K/window", "panel"),
                observed("declared", "declared_total_entropy", "9e-21", 9e-21, "J/K/window", "panel"),
            ],
            entropy_closure={"declared_total": 9e-21, "components": [2e-21, 5e-21]},
        )
        codes = {item["code"] for item in report["conflicts"]}
        self.assertIn("ENTROPY_CLOSURE_FAILURE", codes)
        self.assertEqual(report["outcome"], "INCONSISTENT")

    def test_unit_missing_is_flagged(self):
        report = audit_packet(
            "U",
            [observed("temp", "temperature", "20", 20, None, "panel")],
        )
        codes = {item["code"] for item in report["conflicts"]}
        self.assertIn("UNIT_MISSING", codes)

    def test_evidence_hash_is_deterministic(self):
        fields = [observed("a", "accuracy", "100", 100, "dimensionless", "panel")]
        a = audit_packet("H", fields)
        b = audit_packet("H", fields)
        self.assertEqual(a["evidence_hash"], b["evidence_hash"])
        self.assertEqual(a["semantic_hash"], b["semantic_hash"])


if __name__ == "__main__":
    unittest.main()
