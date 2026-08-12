from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from public_core_validator import parse_expression, validate_packet


DEMO = json.loads(
    (ROOT / "demo" / "PUBLIC_DEMO_001_SEMANTIC_PACKET.json")
    .read_text(encoding="utf-8")
)


class ParserTests(unittest.TestCase):
    def test_ascii_path(self):
        self.assertEqual(
            parse_expression("O -> E -> U<cause> -> I -> G -> F -> Y"),
            ["O", "E", "U", "I", "G", "F", "Y"],
        )

    def test_unicode_path(self):
        self.assertEqual(parse_expression("O → E → F → Y"), ["O", "E", "F", "Y"])

    def test_unknown_operation_rejected(self):
        with self.assertRaises(ValueError):
            parse_expression("O -> A -> Y")

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            parse_expression("")


class ConstitutionalTests(unittest.TestCase):
    def test_demo_is_valid(self):
        result = validate_packet(DEMO)
        self.assertEqual(result["outcome"], "VALID")

    def test_demo_expands(self):
        result = validate_packet(DEMO)
        self.assertEqual(result["compression_mode"], "Z_UP")

    def test_missing_authority_rejected(self):
        p = copy.deepcopy(DEMO)
        p["authority"] = []
        self.assertEqual(validate_packet(p)["outcome"], "REJECT")

    def test_missing_affected_parties_repaired(self):
        p = copy.deepcopy(DEMO)
        p["affected_parties"] = []
        self.assertEqual(validate_packet(p)["outcome"], "REPAIR")

    def test_unknown_op_without_unknown_expands(self):
        p = copy.deepcopy(DEMO)
        p["unknowns"] = []
        self.assertEqual(validate_packet(p)["outcome"], "EXPAND")

    def test_irreversible_without_recovery_rejected(self):
        p = copy.deepcopy(DEMO)
        p["irreversible"] = True
        p["recovery"] = []
        self.assertEqual(validate_packet(p)["outcome"], "REJECT")

    def test_low_risk_known_context_compresses(self):
        p = copy.deepcopy(DEMO)
        p["risk_level"] = "low"
        p["unknowns"] = []
        p["decoder_confidence"] = 0.98
        p["operation_path"] = ["O", "E", "I", "G", "Z", "F", "Y"]
        result = validate_packet(p)
        self.assertEqual(result["compression_mode"], "Z_DOWN")
        self.assertEqual(result["outcome"], "VALID")

    def test_z_refused_under_high_risk(self):
        p = copy.deepcopy(DEMO)
        p["operation_path"] = ["O", "E", "U", "I", "G", "Z", "F", "Y"]
        result = validate_packet(p)
        self.assertEqual(result["outcome"], "EXPAND")
        self.assertTrue(any(x["code"] == "COMPRESSION_REFUSED" for x in result["findings"]))

    def test_missing_fold_repaired(self):
        p = copy.deepcopy(DEMO)
        p["operation_path"] = ["O", "E", "U", "I", "G", "Y"]
        self.assertEqual(validate_packet(p)["outcome"], "REPAIR")

    def test_missing_yield_repaired(self):
        p = copy.deepcopy(DEMO)
        p["operation_path"] = ["O", "E", "U", "I", "G", "F"]
        self.assertEqual(validate_packet(p)["outcome"], "REPAIR")

    def test_protected_fields_returned(self):
        result = validate_packet(DEMO)
        self.assertEqual(result["protected_fields"]["unknowns"], DEMO["unknowns"])
        self.assertEqual(result["protected_fields"]["authority"], DEMO["authority"])
        self.assertEqual(result["protected_fields"]["dissent"], DEMO["dissent"])

    def test_explanation_names_authority(self):
        result = validate_packet(DEMO)
        self.assertIn("human operator", result["explanation"])


if __name__ == "__main__":
    unittest.main()
